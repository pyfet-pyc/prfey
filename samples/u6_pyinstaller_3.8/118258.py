# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pymongo\bulk.py
"""The bulk write operations interface.

.. versionadded:: 2.7
"""
import copy
from itertools import islice
from bson.objectid import ObjectId
from bson.raw_bson import RawBSONDocument
from bson.son import SON
from pymongo.client_session import _validate_session_write_concern
from pymongo.common import validate_is_mapping, validate_is_document_type, validate_ok_for_replace, validate_ok_for_update
from pymongo.helpers import _RETRYABLE_ERROR_CODES
from pymongo.collation import validate_collation_or_none
from pymongo.errors import BulkWriteError, ConfigurationError, InvalidOperation, OperationFailure
from pymongo.message import _INSERT, _UPDATE, _DELETE, _do_batched_insert, _randint, _BulkWriteContext, _EncryptedBulkWriteContext
from pymongo.read_preferences import ReadPreference
from pymongo.write_concern import WriteConcern
_DELETE_ALL = 0
_DELETE_ONE = 1
_BAD_VALUE = 2
_UNKNOWN_ERROR = 8
_WRITE_CONCERN_ERROR = 64
_COMMANDS = ('insert', 'update', 'delete')
_UOP = 'op'

class _Run(object):
    __doc__ = 'Represents a batch of write operations.\n    '

    def __init__(self, op_type):
        """Initialize a new Run object.
        """
        self.op_type = op_type
        self.index_map = []
        self.ops = []
        self.idx_offset = 0

    def index(self, idx):
        """Get the original index of an operation in this run.

        :Parameters:
          - `idx`: The Run index that maps to the original index.
        """
        return self.index_map[idx]

    def add(self, original_index, operation):
        """Add an operation to this Run instance.

        :Parameters:
          - `original_index`: The original index of this operation
            within a larger bulk operation.
          - `operation`: The operation document.
        """
        self.index_map.append(original_index)
        self.ops.append(operation)


def _merge_command(run, full_result, offset, result):
    """Merge a write command result into the full bulk result.
    """
    affected = result.get('n', 0)
    if run.op_type == _INSERT:
        full_result['nInserted'] += affected
    else:
        if run.op_type == _DELETE:
            full_result['nRemoved'] += affected
        else:
            if run.op_type == _UPDATE:
                upserted = result.get('upserted')
                if upserted:
                    n_upserted = len(upserted)
                    for doc in upserted:
                        doc['index'] = run.index(doc['index'] + offset)
                    else:
                        full_result['upserted'].extend(upserted)
                        full_result['nUpserted'] += n_upserted
                        full_result['nMatched'] += affected - n_upserted

                else:
                    full_result['nMatched'] += affected
                full_result['nModified'] += result['nModified']
            else:
                write_errors = result.get('writeErrors')
                if write_errors:
                    for doc in write_errors:
                        replacement = doc.copy()
                        idx = doc['index'] + offset
                        replacement['index'] = run.index(idx)
                        replacement[_UOP] = run.ops[idx]
                        full_result['writeErrors'].append(replacement)

            wc_error = result.get('writeConcernError')
            if wc_error:
                full_result['writeConcernErrors'].append(wc_error)


def _raise_bulk_write_error(full_result):
    """Raise a BulkWriteError from the full bulk api result.
    """
    if full_result['writeErrors']:
        full_result['writeErrors'].sort(key=(lambda error: error['index']))
    raise BulkWriteError(full_result)


class _Bulk(object):
    __doc__ = 'The private guts of the bulk write API.\n    '

    def __init__(self, collection, ordered, bypass_document_validation):
        """Initialize a _Bulk instance.
        """
        self.collection = collection.with_options(codec_options=collection.codec_options._replace(unicode_decode_error_handler='replace',
          document_class=dict))
        self.ordered = ordered
        self.ops = []
        self.executed = False
        self.bypass_doc_val = bypass_document_validation
        self.uses_collation = False
        self.uses_array_filters = False
        self.is_retryable = True
        self.retrying = False
        self.started_retryable_write = False
        self.current_run = None

    @property
    def bulk_ctx_class(self):
        encrypter = self.collection.database.client._encrypter
        if encrypter:
            if not encrypter._bypass_auto_encryption:
                return _EncryptedBulkWriteContext
        return _BulkWriteContext

    def add_insert(self, document):
        """Add an insert document to the list of ops.
        """
        validate_is_document_type('document', document)
        if not isinstance(document, RawBSONDocument):
            if not '_id' in document:
                document['_id'] = ObjectId()
        self.ops.append((_INSERT, document))

    def add_update(self, selector, update, multi=False, upsert=False, collation=None, array_filters=None):
        """Create an update document and add it to the list of ops.
        """
        validate_ok_for_update(update)
        cmd = SON([('q', selector), ('u', update),
         (
          'multi', multi), ('upsert', upsert)])
        collation = validate_collation_or_none(collation)
        if collation is not None:
            self.uses_collation = True
            cmd['collation'] = collation
        if array_filters is not None:
            self.uses_array_filters = True
            cmd['arrayFilters'] = array_filters
        if multi:
            self.is_retryable = False
        self.ops.append((_UPDATE, cmd))

    def add_replace(self, selector, replacement, upsert=False, collation=None):
        """Create a replace document and add it to the list of ops.
        """
        validate_ok_for_replace(replacement)
        cmd = SON([('q', selector), ('u', replacement),
         ('multi', False), ('upsert', upsert)])
        collation = validate_collation_or_none(collation)
        if collation is not None:
            self.uses_collation = True
            cmd['collation'] = collation
        self.ops.append((_UPDATE, cmd))

    def add_delete(self, selector, limit, collation=None):
        """Create a delete document and add it to the list of ops.
        """
        cmd = SON([('q', selector), ('limit', limit)])
        collation = validate_collation_or_none(collation)
        if collation is not None:
            self.uses_collation = True
            cmd['collation'] = collation
        if limit == _DELETE_ALL:
            self.is_retryable = False
        self.ops.append((_DELETE, cmd))

    def gen_ordered(self):
        """Generate batches of operations, batched by type of
        operation, in the order **provided**.
        """
        run = None
        for idx, (op_type, operation) in enumerate(self.ops):
            if run is None:
                run = _Run(op_type)
            else:
                if run.op_type != op_type:
                    (yield run)
                    run = _Run(op_type)
            run.add(idx, operation)
        else:
            (yield run)

    def gen_unordered(self):
        """Generate batches of operations, batched by type of
        operation, in arbitrary order.
        """
        operations = [
         _Run(_INSERT), _Run(_UPDATE), _Run(_DELETE)]
        for idx, (op_type, operation) in enumerate(self.ops):
            operations[op_type].add(idx, operation)
        else:
            for run in operations:
                if run.ops:
                    (yield run)

    def _execute_command(self, generator, write_concern, session, sock_info, op_id, retryable, full_result):
        if sock_info.max_wire_version < 5:
            if self.uses_collation:
                raise ConfigurationError('Must be connected to MongoDB 3.4+ to use a collation.')
        else:
            if sock_info.max_wire_version < 6:
                if self.uses_array_filters:
                    raise ConfigurationError('Must be connected to MongoDB 3.6+ to use arrayFilters.')
            db_name = self.collection.database.name
            client = self.collection.database.client
            listeners = client._event_listeners
            if not self.current_run:
                self.current_run = next(generator)
            run = self.current_run
            sock_info.validate_session(client, session)
            while True:
                if run:
                    cmd = SON([(_COMMANDS[run.op_type], self.collection.name),
                     (
                      'ordered', self.ordered)])
                    if not write_concern.is_server_default:
                        cmd['writeConcern'] = write_concern.document
                    if self.bypass_doc_val:
                        if sock_info.max_wire_version >= 4:
                            cmd['bypassDocumentValidation'] = True
                    bwc = self.bulk_ctx_class(db_name, cmd, sock_info, op_id, listeners, session, run.op_type, self.collection.codec_options)
                    if run.idx_offset < len(run.ops):
                        if session:
                            if retryable:
                                if not self.started_retryable_write:
                                    session._start_retryable_write()
                                    self.started_retryable_write = True
                            session._apply_to(cmd, retryable, ReadPreference.PRIMARY)
                        else:
                            sock_info.send_cluster_time(cmd, session, client)
                            ops = islice(run.ops, run.idx_offset, None)
                            result, to_send = bwc.execute(ops, client)
                            wce = result.get('writeConcernError', {})
                            if wce.get('code', 0) in _RETRYABLE_ERROR_CODES:
                                full = copy.deepcopy(full_result)
                                _merge_command(run, full, run.idx_offset, result)
                                _raise_bulk_write_error(full)
                            _merge_command(run, full_result, run.idx_offset, result)
                            self.retrying = False
                            self.started_retryable_write = False
                            if self.ordered and 'writeErrors' in result:
                                break
                        run.idx_offset += len(to_send)
                else:
                    if self.ordered:
                        if full_result['writeErrors']:
                            break
                    self.current_run = run = next(generator, None)

    def execute_command(self, generator, write_concern, session):
        """Execute using write commands.
        """
        full_result = {'writeErrors':[],  'writeConcernErrors':[],  'nInserted':0, 
         'nUpserted':0, 
         'nMatched':0, 
         'nModified':0, 
         'nRemoved':0, 
         'upserted':[]}
        op_id = _randint()

        def retryable_bulk(session, sock_info, retryable):
            self._execute_command(generator, write_concern, session, sock_info, op_id, retryable, full_result)

        client = self.collection.database.client
        with client._tmp_session(session) as (s):
            client._retry_with_session(self.is_retryable, retryable_bulk, s, self)
        if full_result['writeErrors'] or full_result['writeConcernErrors']:
            _raise_bulk_write_error(full_result)
        return full_result

    def execute_insert_no_results(self, sock_info, run, op_id, acknowledged):
        """Execute insert, returning no results.
        """
        command = SON([('insert', self.collection.name),
         (
          'ordered', self.ordered)])
        concern = {'w': int(self.ordered)}
        command['writeConcern'] = concern
        if self.bypass_doc_val:
            if sock_info.max_wire_version >= 4:
                command['bypassDocumentValidation'] = True
        db = self.collection.database
        bwc = _BulkWriteContext(db.name, command, sock_info, op_id, db.client._event_listeners, None, _INSERT, self.collection.codec_options)
        _do_batched_insert(self.collection.full_name, run.ops, True, acknowledged, concern, not self.ordered, self.collection.codec_options, bwc)

    def execute_op_msg_no_results(self, sock_info, generator):
        """Execute write commands with OP_MSG and w=0 writeConcern, unordered.
        """
        db_name = self.collection.database.name
        client = self.collection.database.client
        listeners = client._event_listeners
        op_id = _randint()
        if not self.current_run:
            self.current_run = next(generator)
        else:
            run = self.current_run
            while True:
                if run:
                    cmd = SON([(_COMMANDS[run.op_type], self.collection.name),
                     ('ordered', False),
                     (
                      'writeConcern', {'w': 0})])
                    bwc = self.bulk_ctx_class(db_name, cmd, sock_info, op_id, listeners, None, run.op_type, self.collection.codec_options)
                    if run.idx_offset < len(run.ops):
                        ops = islice(run.ops, run.idx_offset, None)
                        to_send = bwc.execute_unack(ops, client)
                        run.idx_offset += len(to_send)
                else:
                    self.current_run = run = next(generator, None)

    def execute_command_no_results(self, sock_info, generator):
        """Execute write commands with OP_MSG and w=0 WriteConcern, ordered.
        """
        full_result = {'writeErrors':[],  'writeConcernErrors':[],  'nInserted':0, 
         'nUpserted':0, 
         'nMatched':0, 
         'nModified':0, 
         'nRemoved':0, 
         'upserted':[]}
        write_concern = WriteConcern()
        op_id = _randint()
        try:
            self._execute_command(generator, write_concern, None, sock_info, op_id, False, full_result)
        except OperationFailure:
            pass

    def execute_no_results--- This code section failed: ---

 L. 425         0  LOAD_FAST                'self'
                2  LOAD_ATTR                uses_collation
                4  POP_JUMP_IF_FALSE    14  'to 14'

 L. 426         6  LOAD_GLOBAL              ConfigurationError

 L. 427         8  LOAD_STR                 'Collation is unsupported for unacknowledged writes.'

 L. 426        10  CALL_FUNCTION_1       1  ''
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             4  '4'

 L. 428        14  LOAD_FAST                'self'
               16  LOAD_ATTR                uses_array_filters
               18  POP_JUMP_IF_FALSE    28  'to 28'

 L. 429        20  LOAD_GLOBAL              ConfigurationError

 L. 430        22  LOAD_STR                 'arrayFilters is unsupported for unacknowledged writes.'

 L. 429        24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            18  '18'

 L. 432        28  LOAD_FAST                'self'
               30  LOAD_ATTR                bypass_doc_val
               32  POP_JUMP_IF_FALSE    52  'to 52'
               34  LOAD_FAST                'sock_info'
               36  LOAD_ATTR                max_wire_version
               38  LOAD_CONST               4
               40  COMPARE_OP               >=
               42  POP_JUMP_IF_FALSE    52  'to 52'

 L. 433        44  LOAD_GLOBAL              OperationFailure
               46  LOAD_STR                 'Cannot set bypass_document_validation with unacknowledged write concern'
               48  CALL_FUNCTION_1       1  ''
               50  RAISE_VARARGS_1       1  'exception instance'
             52_0  COME_FROM            42  '42'
             52_1  COME_FROM            32  '32'

 L. 437        52  LOAD_FAST                'sock_info'
               54  LOAD_ATTR                max_wire_version
               56  LOAD_CONST               5
               58  COMPARE_OP               >
               60  POP_JUMP_IF_FALSE    92  'to 92'

 L. 438        62  LOAD_FAST                'self'
               64  LOAD_ATTR                ordered
               66  POP_JUMP_IF_FALSE    80  'to 80'

 L. 439        68  LOAD_FAST                'self'
               70  LOAD_METHOD              execute_command_no_results
               72  LOAD_FAST                'sock_info'
               74  LOAD_FAST                'generator'
               76  CALL_METHOD_2         2  ''
               78  RETURN_VALUE     
             80_0  COME_FROM            66  '66'

 L. 440        80  LOAD_FAST                'self'
               82  LOAD_METHOD              execute_op_msg_no_results
               84  LOAD_FAST                'sock_info'
               86  LOAD_FAST                'generator'
               88  CALL_METHOD_2         2  ''
               90  RETURN_VALUE     
             92_0  COME_FROM            60  '60'

 L. 442        92  LOAD_FAST                'self'
               94  LOAD_ATTR                collection
               96  STORE_FAST               'coll'

 L. 445        98  LOAD_GLOBAL              WriteConcern
              100  LOAD_GLOBAL              int
              102  LOAD_FAST                'self'
              104  LOAD_ATTR                ordered
              106  CALL_FUNCTION_1       1  ''
              108  LOAD_CONST               ('w',)
              110  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              112  STORE_FAST               'write_concern'

 L. 446       114  LOAD_GLOBAL              _randint
              116  CALL_FUNCTION_0       0  ''
              118  STORE_FAST               'op_id'

 L. 448       120  LOAD_GLOBAL              next
              122  LOAD_FAST                'generator'
              124  CALL_FUNCTION_1       1  ''
              126  STORE_FAST               'next_run'

 L. 449       128  LOAD_FAST                'next_run'
          130_132  POP_JUMP_IF_FALSE   390  'to 390'

 L. 453       134  LOAD_FAST                'next_run'
              136  STORE_FAST               'run'

 L. 454       138  LOAD_GLOBAL              next
              140  LOAD_FAST                'generator'
              142  LOAD_CONST               None
              144  CALL_FUNCTION_2       2  ''
              146  STORE_FAST               'next_run'

 L. 455       148  LOAD_FAST                'self'
              150  LOAD_ATTR                ordered
              152  JUMP_IF_FALSE_OR_POP   160  'to 160'
              154  LOAD_FAST                'next_run'
              156  LOAD_CONST               None
              158  COMPARE_OP               is-not
            160_0  COME_FROM           152  '152'
              160  STORE_FAST               'needs_ack'

 L. 456       162  SETUP_FINALLY       352  'to 352'

 L. 457       164  LOAD_FAST                'run'
              166  LOAD_ATTR                op_type
              168  LOAD_GLOBAL              _INSERT
              170  COMPARE_OP               ==
              172  POP_JUMP_IF_FALSE   192  'to 192'

 L. 458       174  LOAD_FAST                'self'
              176  LOAD_METHOD              execute_insert_no_results

 L. 459       178  LOAD_FAST                'sock_info'

 L. 459       180  LOAD_FAST                'run'

 L. 459       182  LOAD_FAST                'op_id'

 L. 459       184  LOAD_FAST                'needs_ack'

 L. 458       186  CALL_METHOD_4         4  ''
              188  POP_TOP          
              190  JUMP_FORWARD        348  'to 348'
            192_0  COME_FROM           172  '172'

 L. 460       192  LOAD_FAST                'run'
              194  LOAD_ATTR                op_type
              196  LOAD_GLOBAL              _UPDATE
              198  COMPARE_OP               ==
          200_202  POP_JUMP_IF_FALSE   302  'to 302'

 L. 461       204  LOAD_FAST                'run'
              206  LOAD_ATTR                ops
              208  GET_ITER         
              210  FOR_ITER            300  'to 300'
              212  STORE_FAST               'operation'

 L. 462       214  LOAD_FAST                'operation'
              216  LOAD_STR                 'u'
              218  BINARY_SUBSCR    
              220  STORE_FAST               'doc'

 L. 463       222  LOAD_CONST               True
              224  STORE_FAST               'check_keys'

 L. 464       226  LOAD_FAST                'doc'
              228  POP_JUMP_IF_FALSE   252  'to 252'
              230  LOAD_GLOBAL              next
              232  LOAD_GLOBAL              iter
              234  LOAD_FAST                'doc'
              236  CALL_FUNCTION_1       1  ''
              238  CALL_FUNCTION_1       1  ''
              240  LOAD_METHOD              startswith
              242  LOAD_STR                 '$'
              244  CALL_METHOD_1         1  ''
              246  POP_JUMP_IF_FALSE   252  'to 252'

 L. 465       248  LOAD_CONST               False
              250  STORE_FAST               'check_keys'
            252_0  COME_FROM           246  '246'
            252_1  COME_FROM           228  '228'

 L. 466       252  LOAD_FAST                'coll'
              254  LOAD_ATTR                _update

 L. 467       256  LOAD_FAST                'sock_info'

 L. 468       258  LOAD_FAST                'operation'
              260  LOAD_STR                 'q'
              262  BINARY_SUBSCR    

 L. 469       264  LOAD_FAST                'doc'

 L. 470       266  LOAD_FAST                'operation'
              268  LOAD_STR                 'upsert'
              270  BINARY_SUBSCR    

 L. 471       272  LOAD_FAST                'check_keys'

 L. 472       274  LOAD_FAST                'operation'
              276  LOAD_STR                 'multi'
              278  BINARY_SUBSCR    

 L. 473       280  LOAD_FAST                'write_concern'

 L. 474       282  LOAD_FAST                'op_id'

 L. 475       284  LOAD_FAST                'self'
              286  LOAD_ATTR                ordered

 L. 476       288  LOAD_FAST                'self'
              290  LOAD_ATTR                bypass_doc_val

 L. 466       292  LOAD_CONST               ('write_concern', 'op_id', 'ordered', 'bypass_doc_val')
              294  CALL_FUNCTION_KW_10    10  '10 total positional and keyword args'
              296  POP_TOP          
              298  JUMP_BACK           210  'to 210'
              300  JUMP_FORWARD        348  'to 348'
            302_0  COME_FROM           200  '200'

 L. 478       302  LOAD_FAST                'run'
              304  LOAD_ATTR                ops
              306  GET_ITER         
              308  FOR_ITER            348  'to 348'
              310  STORE_FAST               'operation'

 L. 479       312  LOAD_FAST                'coll'
              314  LOAD_METHOD              _delete
              316  LOAD_FAST                'sock_info'

 L. 480       318  LOAD_FAST                'operation'
              320  LOAD_STR                 'q'
              322  BINARY_SUBSCR    

 L. 481       324  LOAD_FAST                'operation'
              326  LOAD_STR                 'limit'
              328  BINARY_SUBSCR    
              330  UNARY_NOT        

 L. 482       332  LOAD_FAST                'write_concern'

 L. 483       334  LOAD_FAST                'op_id'

 L. 484       336  LOAD_FAST                'self'
              338  LOAD_ATTR                ordered

 L. 479       340  CALL_METHOD_6         6  ''
              342  POP_TOP          
          344_346  JUMP_BACK           308  'to 308'
            348_0  COME_FROM           300  '300'
            348_1  COME_FROM           190  '190'
              348  POP_BLOCK        
              350  JUMP_BACK           128  'to 128'
            352_0  COME_FROM_FINALLY   162  '162'

 L. 485       352  DUP_TOP          
              354  LOAD_GLOBAL              OperationFailure
              356  COMPARE_OP               exception-match
          358_360  POP_JUMP_IF_FALSE   386  'to 386'
              362  POP_TOP          
              364  POP_TOP          
              366  POP_TOP          

 L. 486       368  LOAD_FAST                'self'
              370  LOAD_ATTR                ordered
          372_374  POP_JUMP_IF_FALSE   382  'to 382'

 L. 487       376  POP_EXCEPT       
          378_380  JUMP_ABSOLUTE       390  'to 390'
            382_0  COME_FROM           372  '372'
              382  POP_EXCEPT       
              384  JUMP_BACK           128  'to 128'
            386_0  COME_FROM           358  '358'
              386  END_FINALLY      
              388  JUMP_BACK           128  'to 128'
            390_0  COME_FROM           130  '130'

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 378_380

    def execute(self, write_concern, session):
        """Execute operations.
        """
        if not self.ops:
            raise InvalidOperation('No operations to execute')
        else:
            if self.executed:
                raise InvalidOperation('Bulk operations can only be executed once.')
            else:
                self.executed = True
                write_concern = write_concern or self.collection.write_concern
                session = _validate_session_write_concern(session, write_concern)
                if self.ordered:
                    generator = self.gen_ordered()
                else:
                    generator = self.gen_unordered()
            client = self.collection.database.client
            if not write_concern.acknowledged:
                with client._socket_for_writes(session) as (sock_info):
                    self.execute_no_results(sock_info, generator)
            else:
                return self.execute_command(generator, write_concern, session)


class BulkUpsertOperation(object):
    __doc__ = 'An interface for adding upsert operations.\n    '
    __slots__ = ('__selector', '__bulk', '__collation')

    def __init__(self, selector, bulk, collation):
        self._BulkUpsertOperation__selector = selector
        self._BulkUpsertOperation__bulk = bulk
        self._BulkUpsertOperation__collation = collation

    def update_one(self, update):
        """Update one document matching the selector.

        :Parameters:
          - `update` (dict): the update operations to apply
        """
        self._BulkUpsertOperation__bulk.add_update((self._BulkUpsertOperation__selector), update,
          multi=False, upsert=True, collation=(self._BulkUpsertOperation__collation))

    def update(self, update):
        """Update all documents matching the selector.

        :Parameters:
          - `update` (dict): the update operations to apply
        """
        self._BulkUpsertOperation__bulk.add_update((self._BulkUpsertOperation__selector), update,
          multi=True, upsert=True, collation=(self._BulkUpsertOperation__collation))

    def replace_one(self, replacement):
        """Replace one entire document matching the selector criteria.

        :Parameters:
          - `replacement` (dict): the replacement document
        """
        self._BulkUpsertOperation__bulk.add_replace((self._BulkUpsertOperation__selector), replacement, upsert=True, collation=(self._BulkUpsertOperation__collation))


class BulkWriteOperation(object):
    __doc__ = 'An interface for adding update or remove operations.\n    '
    __slots__ = ('__selector', '__bulk', '__collation')

    def __init__(self, selector, bulk, collation):
        self._BulkWriteOperation__selector = selector
        self._BulkWriteOperation__bulk = bulk
        self._BulkWriteOperation__collation = collation

    def update_one(self, update):
        """Update one document matching the selector criteria.

        :Parameters:
          - `update` (dict): the update operations to apply
        """
        self._BulkWriteOperation__bulk.add_update((self._BulkWriteOperation__selector), update, multi=False, collation=(self._BulkWriteOperation__collation))

    def update(self, update):
        """Update all documents matching the selector criteria.

        :Parameters:
          - `update` (dict): the update operations to apply
        """
        self._BulkWriteOperation__bulk.add_update((self._BulkWriteOperation__selector), update, multi=True, collation=(self._BulkWriteOperation__collation))

    def replace_one(self, replacement):
        """Replace one entire document matching the selector criteria.

        :Parameters:
          - `replacement` (dict): the replacement document
        """
        self._BulkWriteOperation__bulk.add_replace((self._BulkWriteOperation__selector), replacement, collation=(self._BulkWriteOperation__collation))

    def remove_one(self):
        """Remove a single document matching the selector criteria.
        """
        self._BulkWriteOperation__bulk.add_delete((self._BulkWriteOperation__selector), _DELETE_ONE, collation=(self._BulkWriteOperation__collation))

    def remove(self):
        """Remove all documents matching the selector criteria.
        """
        self._BulkWriteOperation__bulk.add_delete((self._BulkWriteOperation__selector), _DELETE_ALL, collation=(self._BulkWriteOperation__collation))

    def upsert(self):
        """Specify that all chained update operations should be
        upserts.

        :Returns:
          - A :class:`BulkUpsertOperation` instance, used to add
            update operations to this bulk operation.
        """
        return BulkUpsertOperation(self._BulkWriteOperation__selector, self._BulkWriteOperation__bulk, self._BulkWriteOperation__collation)


class BulkOperationBuilder(object):
    __doc__ = '**DEPRECATED**: An interface for executing a batch of write operations.\n    '
    __slots__ = '__bulk'

    def __init__(self, collection, ordered=True, bypass_document_validation=False):
        """**DEPRECATED**: Initialize a new BulkOperationBuilder instance.

        :Parameters:
          - `collection`: A :class:`~pymongo.collection.Collection` instance.
          - `ordered` (optional): If ``True`` all operations will be executed
            serially, in the order provided, and the entire execution will
            abort on the first error. If ``False`` operations will be executed
            in arbitrary order (possibly in parallel on the server), reporting
            any errors that occurred after attempting all operations. Defaults
            to ``True``.
          - `bypass_document_validation`: (optional) If ``True``, allows the
            write to opt-out of document level validation. Default is
            ``False``.

        .. note:: `bypass_document_validation` requires server version
          **>= 3.2**

        .. versionchanged:: 3.5
           Deprecated. Use :meth:`~pymongo.collection.Collection.bulk_write`
           instead.

        .. versionchanged:: 3.2
          Added bypass_document_validation support
        """
        self._BulkOperationBuilder__bulk = _Bulk(collection, ordered, bypass_document_validation)

    def find(self, selector, collation=None):
        """Specify selection criteria for bulk operations.

        :Parameters:
          - `selector` (dict): the selection criteria for update
            and remove operations.
          - `collation` (optional): An instance of
            :class:`~pymongo.collation.Collation`. This option is only
            supported on MongoDB 3.4 and above.

        :Returns:
          - A :class:`BulkWriteOperation` instance, used to add
            update and remove operations to this bulk operation.

        .. versionchanged:: 3.4
           Added the `collation` option.

        """
        validate_is_mapping('selector', selector)
        return BulkWriteOperation(selector, self._BulkOperationBuilder__bulk, collation)

    def insert(self, document):
        """Insert a single document.

        :Parameters:
          - `document` (dict): the document to insert

        .. seealso:: :ref:`writes-and-ids`
        """
        self._BulkOperationBuilder__bulk.add_insert(document)

    def execute(self, write_concern=None):
        """Execute all provided operations.

        :Parameters:
          - write_concern (optional): the write concern for this bulk
            execution.
        """
        if write_concern is not None:
            write_concern = WriteConcern(**write_concern)
        return self._BulkOperationBuilder__bulk.execute(write_concern, session=None)