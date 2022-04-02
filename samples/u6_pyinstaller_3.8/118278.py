# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pymongo\message.py
"""Tools for creating `messages
<http://www.mongodb.org/display/DOCS/Mongo+Wire+Protocol>`_ to be sent to
MongoDB.

.. note:: This module is for internal use and is generally not needed by
   application developers.
"""
import datetime, random, struct, bson
from bson import CodecOptions, decode, encode, _dict_to_bson, _make_c_string
from bson.codec_options import DEFAULT_CODEC_OPTIONS
from bson.raw_bson import _inflate_bson, DEFAULT_RAW_BSON_OPTIONS
from bson.py3compat import b, StringIO
from bson.son import SON
try:
    from pymongo import _cmessage
    _use_c = True
except ImportError:
    _use_c = False
else:
    from pymongo.errors import ConfigurationError, CursorNotFound, DocumentTooLarge, ExecutionTimeout, InvalidOperation, NotMasterError, OperationFailure, ProtocolError
    from pymongo.read_concern import DEFAULT_READ_CONCERN
    from pymongo.read_preferences import ReadPreference
    from pymongo.write_concern import WriteConcern
    MAX_INT32 = 2147483647
    MIN_INT32 = -2147483648
    _COMMAND_OVERHEAD = 16382
    _INSERT = 0
    _UPDATE = 1
    _DELETE = 2
    _EMPTY = b''
    _BSONOBJ = b'\x03'
    _ZERO_8 = b'\x00'
    _ZERO_16 = b'\x00\x00'
    _ZERO_32 = b'\x00\x00\x00\x00'
    _ZERO_64 = b'\x00\x00\x00\x00\x00\x00\x00\x00'
    _SKIPLIM = b'\x00\x00\x00\x00\xff\xff\xff\xff'
    _OP_MAP = {_INSERT: b'\x04documents\x00\x00\x00\x00\x00', 
     _UPDATE: b'\x04updates\x00\x00\x00\x00\x00', 
     _DELETE: b'\x04deletes\x00\x00\x00\x00\x00'}
    _FIELD_MAP = {'insert':'documents', 
     'update':'updates', 
     'delete':'deletes'}
    _UJOIN = '%s.%s'
    _UNICODE_REPLACE_CODEC_OPTIONS = CodecOptions(unicode_decode_error_handler='replace')

    def _randint():
        """Generate a pseudo random 32 bit integer."""
        return random.randint(MIN_INT32, MAX_INT32)


    def _maybe_add_read_preference(spec, read_preference):
        """Add $readPreference to spec when appropriate."""
        mode = read_preference.mode
        tag_sets = read_preference.tag_sets
        max_staleness = read_preference.max_staleness
        if mode:
            if mode != ReadPreference.SECONDARY_PREFERRED.mode or tag_sets != [{}] or max_staleness != -1:
                if '$query' not in spec:
                    spec = SON([('$query', spec)])
                spec['$readPreference'] = read_preference.document
        return spec


    def _convert_exception(exception):
        """Convert an Exception into a failure document for publishing."""
        return {'errmsg':str(exception), 
         'errtype':exception.__class__.__name__}


    def _convert_write_result(operation, command, result):
        """Convert a legacy write result to write commmand format."""
        affected = result.get('n', 0)
        res = {'ok':1,  'n':affected}
        errmsg = result.get('errmsg', result.get('err', ''))
        if errmsg:
            if result.get('wtimeout'):
                res['writeConcernError'] = {'errmsg':errmsg, 
                 'code':64, 
                 'errInfo':{'wtimeout': True}}
            else:
                error = {'index':0, 
                 'code':result.get('code', 8), 
                 'errmsg':errmsg}
                if 'errInfo' in result:
                    error['errInfo'] = result['errInfo']
                res['writeErrors'] = [
                 error]
                return res
        if operation == 'insert':
            res['n'] = len(command['documents'])
        else:
            if operation == 'update':
                if 'upserted' in result:
                    res['upserted'] = [
                     {'index':0, 
                      '_id':result['upserted']}]
                else:
                    if result.get('updatedExisting') is False:
                        if affected == 1:
                            update = command['updates'][0]
                            _id = update['u'].get('_id', update['q'].get('_id'))
                            res['upserted'] = [{'index':0,  '_id':_id}]
            return res


    _OPTIONS = SON([
     ('tailable', 2),
     ('oplogReplay', 8),
     ('noCursorTimeout', 16),
     ('awaitData', 32),
     ('allowPartialResults', 128)])
    _MODIFIERS = SON([
     ('$query', 'filter'),
     ('$orderby', 'sort'),
     ('$hint', 'hint'),
     ('$comment', 'comment'),
     ('$maxScan', 'maxScan'),
     ('$maxTimeMS', 'maxTimeMS'),
     ('$max', 'max'),
     ('$min', 'min'),
     ('$returnKey', 'returnKey'),
     ('$showRecordId', 'showRecordId'),
     ('$showDiskLoc', 'showRecordId'),
     ('$snapshot', 'snapshot')])

    def _gen_find_command(coll, spec, projection, skip, limit, batch_size, options, read_concern, collation=None, session=None):
        """Generate a find command document."""
        cmd = SON([('find', coll)])
        if '$query' in spec:
            cmd.update([(_MODIFIERS[key], val) if key in _MODIFIERS else (key, val) for key, val in spec.items()])
            if '$explain' in cmd:
                cmd.pop('$explain')
            if '$readPreference' in cmd:
                cmd.pop('$readPreference')
        else:
            cmd['filter'] = spec
        if projection:
            cmd['projection'] = projection
        if skip:
            cmd['skip'] = skip
        if limit:
            cmd['limit'] = abs(limit)
            if limit < 0:
                cmd['singleBatch'] = True
        if batch_size:
            cmd['batchSize'] = batch_size
        if read_concern.level:
            cmd['readConcern'] = session and session.in_transaction or read_concern.document
        if collation:
            cmd['collation'] = collation
        if options:
            cmd.update([(opt, True) for opt, val in _OPTIONS.items() if options & val])
        return cmd


    def _gen_get_more_command(cursor_id, coll, batch_size, max_await_time_ms):
        """Generate a getMore command document."""
        cmd = SON([('getMore', cursor_id),
         (
          'collection', coll)])
        if batch_size:
            cmd['batchSize'] = batch_size
        if max_await_time_ms is not None:
            cmd['maxTimeMS'] = max_await_time_ms
        return cmd


    class _Query(object):
        __doc__ = 'A query operation.'
        __slots__ = ('flags', 'db', 'coll', 'ntoskip', 'spec', 'fields', 'codec_options',
                     'read_preference', 'limit', 'batch_size', 'name', 'read_concern',
                     'collation', 'session', 'client', '_as_command')
        exhaust_mgr = None
        cursor_id = None

        def __init__(self, flags, db, coll, ntoskip, spec, fields, codec_options, read_preference, limit, batch_size, read_concern, collation, session, client):
            self.flags = flags
            self.db = db
            self.coll = coll
            self.ntoskip = ntoskip
            self.spec = spec
            self.fields = fields
            self.codec_options = codec_options
            self.read_preference = read_preference
            self.read_concern = read_concern
            self.limit = limit
            self.batch_size = batch_size
            self.collation = collation
            self.session = session
            self.client = client
            self.name = 'find'
            self._as_command = None

        def namespace(self):
            return _UJOIN % (self.db, self.coll)

        def use_command(self, sock_info, exhaust):
            use_find_cmd = False
            if sock_info.max_wire_version >= 4:
                use_find_cmd = exhaust or True
            else:
                if not self.read_concern.ok_for_legacy:
                    raise ConfigurationError('read concern level of %s is not valid with a max wire version of %d.' % (
                     self.read_concern.level,
                     sock_info.max_wire_version))
                elif sock_info.max_wire_version < 5 and self.collation is not None:
                    raise ConfigurationError('Specifying a collation is unsupported with a max wire version of %d.' % (
                     sock_info.max_wire_version,))
                sock_info.validate_session(self.client, self.session)
                return use_find_cmd

        def as_command(self, sock_info):
            """Return a find command document for this query."""
            if self._as_command is not None:
                return self._as_command
                explain = '$explain' in self.spec
                cmd = _gen_find_command(self.coll, self.spec, self.fields, self.ntoskip, self.limit, self.batch_size, self.flags, self.read_concern, self.collation, self.session)
                if explain:
                    self.name = 'explain'
                    cmd = SON([('explain', cmd)])
            else:
                session = self.session
                if session:
                    session._apply_to(cmd, False, self.read_preference)
                    if not explain:
                        if session.options.causal_consistency:
                            if session.operation_time is not None:
                                if not session.in_transaction:
                                    cmd.setdefault('readConcern', {})['afterClusterTime'] = session.operation_time
                sock_info.send_cluster_time(cmd, session, self.client)
                client = self.client
                if client._encrypter:
                    cmd = client._encrypter._bypass_auto_encryption or client._encrypter.encrypt(self.db, cmd, False, self.codec_options)
            self._as_command = (
             cmd, self.db)
            return self._as_command

        def get_message(self, set_slave_ok, sock_info, use_cmd=False):
            """Get a query message, possibly setting the slaveOk bit."""
            if set_slave_ok:
                flags = self.flags | 4
            else:
                flags = self.flags
            ns = self.namespace()
            spec = self.spec
            if use_cmd:
                spec = self.as_command(sock_info)[0]
                if sock_info.op_msg_enabled:
                    request_id, msg, size, _ = _op_msg(0,
                      spec, (self.db), (self.read_preference), set_slave_ok,
                      False, (self.codec_options), ctx=(sock_info.compression_context))
                    return (request_id, msg, size)
                ns = _UJOIN % (self.db, '$cmd')
                ntoreturn = -1
            else:
                ntoreturn = self.batch_size == 1 and 2 or self.batch_size
                if self.limit:
                    if ntoreturn:
                        ntoreturn = min(self.limit, ntoreturn)
                    else:
                        ntoreturn = self.limit
            if sock_info.is_mongos:
                spec = _maybe_add_read_preference(spec, self.read_preference)
            return query(flags, ns, (self.ntoskip), ntoreturn, spec,
              (None if use_cmd else self.fields), (self.codec_options),
              ctx=(sock_info.compression_context))


    class _GetMore(object):
        __doc__ = 'A getmore operation.'
        __slots__ = ('db', 'coll', 'ntoreturn', 'cursor_id', 'max_await_time_ms', 'codec_options',
                     'read_preference', 'session', 'client', 'exhaust_mgr', '_as_command')
        name = 'getMore'

        def __init__(self, db, coll, ntoreturn, cursor_id, codec_options, read_preference, session, client, max_await_time_ms, exhaust_mgr):
            self.db = db
            self.coll = coll
            self.ntoreturn = ntoreturn
            self.cursor_id = cursor_id
            self.codec_options = codec_options
            self.read_preference = read_preference
            self.session = session
            self.client = client
            self.max_await_time_ms = max_await_time_ms
            self.exhaust_mgr = exhaust_mgr
            self._as_command = None

        def namespace(self):
            return _UJOIN % (self.db, self.coll)

        def use_command(self, sock_info, exhaust):
            sock_info.validate_session(self.client, self.session)
            return sock_info.max_wire_version >= 4 and not exhaust

        def as_command(self, sock_info):
            """Return a getMore command document for this query."""
            if self._as_command is not None:
                return self._as_command
            else:
                cmd = _gen_get_more_command(self.cursor_id, self.coll, self.ntoreturn, self.max_await_time_ms)
                if self.session:
                    self.session._apply_to(cmd, False, self.read_preference)
                sock_info.send_cluster_time(cmd, self.session, self.client)
                client = self.client
                if client._encrypter:
                    cmd = client._encrypter._bypass_auto_encryption or client._encrypter.encrypt(self.db, cmd, False, self.codec_options)
            self._as_command = (
             cmd, self.db)
            return self._as_command

        def get_message(self, dummy0, sock_info, use_cmd=False):
            """Get a getmore message."""
            ns = self.namespace()
            ctx = sock_info.compression_context
            if use_cmd:
                spec = self.as_command(sock_info)[0]
                if sock_info.op_msg_enabled:
                    request_id, msg, size, _ = _op_msg(0,
                      spec, (self.db), None, False,
                      False, (self.codec_options), ctx=(sock_info.compression_context))
                    return (request_id, msg, size)
                ns = _UJOIN % (self.db, '$cmd')
                return query(0, ns, 0, (-1), spec, None, (self.codec_options), ctx=ctx)
            return get_more(ns, self.ntoreturn, self.cursor_id, ctx)


    class _RawBatchQuery(_Query):

        def use_command(self, socket_info, exhaust):
            super(_RawBatchQuery, self).use_command(socket_info, exhaust)
            return False

        def get_message(self, set_slave_ok, sock_info, use_cmd=False):
            return super(_RawBatchQuery, self).get_message(set_slave_ok, sock_info, False)


    class _RawBatchGetMore(_GetMore):

        def use_command(self, socket_info, exhaust):
            return False

        def get_message(self, set_slave_ok, sock_info, use_cmd=False):
            return super(_RawBatchGetMore, self).get_message(set_slave_ok, sock_info, False)


    class _CursorAddress(tuple):
        __doc__ = 'The server address (host, port) of a cursor, with namespace property.'

        def __new__(cls, address, namespace):
            self = tuple.__new__(cls, address)
            self._CursorAddress__namespace = namespace
            return self

        @property
        def namespace(self):
            """The namespace this cursor."""
            return self._CursorAddress__namespace

        def __hash__(self):
            return (self + (self._CursorAddress__namespace,)).__hash__()

        def __eq__(self, other):
            if isinstance(other, _CursorAddress):
                return tuple(self) == tuple(other) and self.namespace == other.namespace
            return NotImplemented

        def __ne__(self, other):
            return not self == other


    _pack_compression_header = struct.Struct('<iiiiiiB').pack
    _COMPRESSION_HEADER_SIZE = 25

    def _compress(operation, data, ctx):
        """Takes message data, compresses it, and adds an OP_COMPRESSED header."""
        compressed = ctx.compress(data)
        request_id = _randint()
        header = _pack_compression_header(_COMPRESSION_HEADER_SIZE + len(compressed), request_id, 0, 2012, operation, len(data), ctx.compressor_id)
        return (request_id, header + compressed)


    def __last_error(namespace, args):
        """Data to send to do a lastError.
    """
        cmd = SON([('getlasterror', 1)])
        cmd.update(args)
        splitns = namespace.split('.', 1)
        return query(0, splitns[0] + '.$cmd', 0, -1, cmd, None, DEFAULT_CODEC_OPTIONS)


    _pack_header = struct.Struct('<iiii').pack

    def __pack_message(operation, data):
        """Takes message data and adds a message header based on the operation.

    Returns the resultant message string.
    """
        rid = _randint()
        message = _pack_header(16 + len(data), rid, 0, operation)
        return (rid, message + data)


    _pack_int = struct.Struct('<i').pack

    def _insert(collection_name, docs, check_keys, flags, opts):
        """Get an OP_INSERT message"""
        encode = _dict_to_bson
        if len(docs) == 1:
            encoded = encode(docs[0], check_keys, opts)
            return (
             (b'').join([
              b'\x00\x00\x00\x00',
              _make_c_string(collection_name),
              encoded]), len(encoded))
        encoded = [encode(doc, check_keys, opts) for doc in docs]
        if not encoded:
            raise InvalidOperation('cannot do an empty bulk insert')
        return (
         (b'').join([
          _pack_int(flags),
          _make_c_string(collection_name),
          (b'').join(encoded)]), max(map(len, encoded)))


    def _insert_compressed(collection_name, docs, check_keys, continue_on_error, opts, ctx):
        """Internal compressed unacknowledged insert message helper."""
        op_insert, max_bson_size = _insert(collection_name, docs, check_keys, continue_on_error, opts)
        rid, msg = _compress(2002, op_insert, ctx)
        return (rid, msg, max_bson_size)


    def _insert_uncompressed(collection_name, docs, check_keys, safe, last_error_args, continue_on_error, opts):
        """Internal insert message helper."""
        op_insert, max_bson_size = _insert(collection_name, docs, check_keys, continue_on_error, opts)
        rid, msg = __pack_message(2002, op_insert)
        if safe:
            rid, gle, _ = __last_error(collection_name, last_error_args)
            return (rid, msg + gle, max_bson_size)
        return (
         rid, msg, max_bson_size)


    if _use_c:
        _insert_uncompressed = _cmessage._insert_message

    def insert(collection_name, docs, check_keys, safe, last_error_args, continue_on_error, opts, ctx=None):
        """Get an **insert** message."""
        if ctx:
            return _insert_compressed(collection_name, docs, check_keys, continue_on_error, opts, ctx)
        return _insert_uncompressed(collection_name, docs, check_keys, safe, last_error_args, continue_on_error, opts)


    def _update(collection_name, upsert, multi, spec, doc, check_keys, opts):
        """Get an OP_UPDATE message."""
        flags = 0
        if upsert:
            flags += 1
        if multi:
            flags += 2
        encode = _dict_to_bson
        encoded_update = encode(doc, check_keys, opts)
        return (
         (b'').join([
          _ZERO_32,
          _make_c_string(collection_name),
          _pack_int(flags),
          encode(spec, False, opts),
          encoded_update]), len(encoded_update))


    def _update_compressed(collection_name, upsert, multi, spec, doc, check_keys, opts, ctx):
        """Internal compressed unacknowledged update message helper."""
        op_update, max_bson_size = _update(collection_name, upsert, multi, spec, doc, check_keys, opts)
        rid, msg = _compress(2001, op_update, ctx)
        return (rid, msg, max_bson_size)


    def _update_uncompressed(collection_name, upsert, multi, spec, doc, safe, last_error_args, check_keys, opts):
        """Internal update message helper."""
        op_update, max_bson_size = _update(collection_name, upsert, multi, spec, doc, check_keys, opts)
        rid, msg = __pack_message(2001, op_update)
        if safe:
            rid, gle, _ = __last_error(collection_name, last_error_args)
            return (rid, msg + gle, max_bson_size)
        return (
         rid, msg, max_bson_size)


    if _use_c:
        _update_uncompressed = _cmessage._update_message

    def update(collection_name, upsert, multi, spec, doc, safe, last_error_args, check_keys, opts, ctx=None):
        """Get an **update** message."""
        if ctx:
            return _update_compressed(collection_name, upsert, multi, spec, doc, check_keys, opts, ctx)
        return _update_uncompressed(collection_name, upsert, multi, spec, doc, safe, last_error_args, check_keys, opts)


    _pack_op_msg_flags_type = struct.Struct('<IB').pack
    _pack_byte = struct.Struct('<B').pack

    def _op_msg_no_header(flags, command, identifier, docs, check_keys, opts):
        """Get a OP_MSG message.

    Note: this method handles multiple documents in a type one payload but
    it does not perform batch splitting and the total message size is
    only checked *after* generating the entire message.
    """
        encoded = _dict_to_bson(command, False, opts)
        flags_type = _pack_op_msg_flags_type(flags, 0)
        total_size = len(encoded)
        max_doc_size = 0
        if identifier:
            type_one = _pack_byte(1)
            cstring = _make_c_string(identifier)
            encoded_docs = [_dict_to_bson(doc, check_keys, opts) for doc in docs]
            size = len(cstring) + sum((len(doc) for doc in encoded_docs)) + 4
            encoded_size = _pack_int(size)
            total_size += size
            max_doc_size = max((len(doc) for doc in encoded_docs))
            data = [flags_type, encoded, type_one, encoded_size, cstring] + encoded_docs
        else:
            data = [
             flags_type, encoded]
        return (
         (b'').join(data), total_size, max_doc_size)


    def _op_msg_compressed(flags, command, identifier, docs, check_keys, opts, ctx):
        """Internal OP_MSG message helper."""
        msg, total_size, max_bson_size = _op_msg_no_header(flags, command, identifier, docs, check_keys, opts)
        rid, msg = _compress(2013, msg, ctx)
        return (rid, msg, total_size, max_bson_size)


    def _op_msg_uncompressed(flags, command, identifier, docs, check_keys, opts):
        """Internal compressed OP_MSG message helper."""
        data, total_size, max_bson_size = _op_msg_no_header(flags, command, identifier, docs, check_keys, opts)
        request_id, op_message = __pack_message(2013, data)
        return (request_id, op_message, total_size, max_bson_size)


    if _use_c:
        _op_msg_uncompressed = _cmessage._op_msg

    def _op_msg--- This code section failed: ---

 L. 687         0  LOAD_FAST                'dbname'
                2  LOAD_FAST                'command'
                4  LOAD_STR                 '$db'
                6  STORE_SUBSCR     

 L. 689         8  LOAD_FAST                'read_preference'
               10  LOAD_CONST               None
               12  COMPARE_OP               is-not
               14  POP_JUMP_IF_FALSE    58  'to 58'
               16  LOAD_STR                 '$readPreference'
               18  LOAD_FAST                'command'
               20  COMPARE_OP               not-in
               22  POP_JUMP_IF_FALSE    58  'to 58'

 L. 690        24  LOAD_FAST                'slave_ok'
               26  POP_JUMP_IF_FALSE    48  'to 48'
               28  LOAD_FAST                'read_preference'
               30  LOAD_ATTR                mode
               32  POP_JUMP_IF_TRUE     48  'to 48'

 L. 692        34  LOAD_GLOBAL              ReadPreference
               36  LOAD_ATTR                PRIMARY_PREFERRED
               38  LOAD_ATTR                document

 L. 691        40  LOAD_FAST                'command'
               42  LOAD_STR                 '$readPreference'
               44  STORE_SUBSCR     
               46  JUMP_FORWARD         58  'to 58'
             48_0  COME_FROM            32  '32'
             48_1  COME_FROM            26  '26'

 L. 694        48  LOAD_FAST                'read_preference'
               50  LOAD_ATTR                document
               52  LOAD_FAST                'command'
               54  LOAD_STR                 '$readPreference'
               56  STORE_SUBSCR     
             58_0  COME_FROM            46  '46'
             58_1  COME_FROM            22  '22'
             58_2  COME_FROM            14  '14'

 L. 695        58  LOAD_GLOBAL              next
               60  LOAD_GLOBAL              iter
               62  LOAD_FAST                'command'
               64  CALL_FUNCTION_1       1  ''
               66  CALL_FUNCTION_1       1  ''
               68  STORE_FAST               'name'

 L. 696        70  SETUP_FINALLY        96  'to 96'

 L. 697        72  LOAD_GLOBAL              _FIELD_MAP
               74  LOAD_METHOD              get
               76  LOAD_FAST                'name'
               78  CALL_METHOD_1         1  ''
               80  STORE_FAST               'identifier'

 L. 698        82  LOAD_FAST                'command'
               84  LOAD_METHOD              pop
               86  LOAD_FAST                'identifier'
               88  CALL_METHOD_1         1  ''
               90  STORE_FAST               'docs'
               92  POP_BLOCK        
               94  JUMP_FORWARD        124  'to 124'
             96_0  COME_FROM_FINALLY    70  '70'

 L. 699        96  DUP_TOP          
               98  LOAD_GLOBAL              KeyError
              100  COMPARE_OP               exception-match
              102  POP_JUMP_IF_FALSE   122  'to 122'
              104  POP_TOP          
              106  POP_TOP          
              108  POP_TOP          

 L. 700       110  LOAD_STR                 ''
              112  STORE_FAST               'identifier'

 L. 701       114  LOAD_CONST               None
              116  STORE_FAST               'docs'
              118  POP_EXCEPT       
              120  JUMP_FORWARD        124  'to 124'
            122_0  COME_FROM           102  '102'
              122  END_FINALLY      
            124_0  COME_FROM           120  '120'
            124_1  COME_FROM            94  '94'

 L. 702       124  SETUP_FINALLY       176  'to 176'

 L. 703       126  LOAD_FAST                'ctx'
              128  POP_JUMP_IF_FALSE   154  'to 154'

 L. 704       130  LOAD_GLOBAL              _op_msg_compressed

 L. 705       132  LOAD_FAST                'flags'

 L. 705       134  LOAD_FAST                'command'

 L. 705       136  LOAD_FAST                'identifier'

 L. 705       138  LOAD_FAST                'docs'

 L. 705       140  LOAD_FAST                'check_keys'

 L. 705       142  LOAD_FAST                'opts'

 L. 705       144  LOAD_FAST                'ctx'

 L. 704       146  CALL_FUNCTION_7       7  ''
              148  POP_BLOCK        
              150  CALL_FINALLY        176  'to 176'
              152  RETURN_VALUE     
            154_0  COME_FROM           128  '128'

 L. 706       154  LOAD_GLOBAL              _op_msg_uncompressed

 L. 707       156  LOAD_FAST                'flags'

 L. 707       158  LOAD_FAST                'command'

 L. 707       160  LOAD_FAST                'identifier'

 L. 707       162  LOAD_FAST                'docs'

 L. 707       164  LOAD_FAST                'check_keys'

 L. 707       166  LOAD_FAST                'opts'

 L. 706       168  CALL_FUNCTION_6       6  ''
              170  POP_BLOCK        
              172  CALL_FINALLY        176  'to 176'
              174  RETURN_VALUE     
            176_0  COME_FROM           172  '172'
            176_1  COME_FROM           150  '150'
            176_2  COME_FROM_FINALLY   124  '124'

 L. 710       176  LOAD_FAST                'identifier'
              178  POP_JUMP_IF_FALSE   188  'to 188'

 L. 711       180  LOAD_FAST                'docs'
              182  LOAD_FAST                'command'
              184  LOAD_FAST                'identifier'
              186  STORE_SUBSCR     
            188_0  COME_FROM           178  '178'
              188  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 150


    def _query(options, collection_name, num_to_skip, num_to_return, query, field_selector, opts, check_keys):
        """Get an OP_QUERY message."""
        encoded = _dict_to_bson(query, check_keys, opts)
        if field_selector:
            efs = _dict_to_bson(field_selector, False, opts)
        else:
            efs = b''
        max_bson_size = max(len(encoded), len(efs))
        return (
         (b'').join([
          _pack_int(options),
          _make_c_string(collection_name),
          _pack_int(num_to_skip),
          _pack_int(num_to_return),
          encoded,
          efs]), max_bson_size)


    def _query_compressed(options, collection_name, num_to_skip, num_to_return, query, field_selector, opts, check_keys=False, ctx=None):
        """Internal compressed query message helper."""
        op_query, max_bson_size = _query(options, collection_name, num_to_skip, num_to_return, query, field_selector, opts, check_keys)
        rid, msg = _compress(2004, op_query, ctx)
        return (rid, msg, max_bson_size)


    def _query_uncompressed(options, collection_name, num_to_skip, num_to_return, query, field_selector, opts, check_keys=False):
        """Internal query message helper."""
        op_query, max_bson_size = _query(options, collection_name, num_to_skip, num_to_return, query, field_selector, opts, check_keys)
        rid, msg = __pack_message(2004, op_query)
        return (rid, msg, max_bson_size)


    if _use_c:
        _query_uncompressed = _cmessage._query_message

    def query(options, collection_name, num_to_skip, num_to_return, query, field_selector, opts, check_keys=False, ctx=None):
        """Get a **query** message."""
        if ctx:
            return _query_compressed(options, collection_name, num_to_skip, num_to_return, query, field_selector, opts, check_keys, ctx)
        return _query_uncompressed(options, collection_name, num_to_skip, num_to_return, query, field_selector, opts, check_keys)


    _pack_long_long = struct.Struct('<q').pack

    def _get_more(collection_name, num_to_return, cursor_id):
        """Get an OP_GET_MORE message."""
        return (b'').join([
         _ZERO_32,
         _make_c_string(collection_name),
         _pack_int(num_to_return),
         _pack_long_long(cursor_id)])


    def _get_more_compressed(collection_name, num_to_return, cursor_id, ctx):
        """Internal compressed getMore message helper."""
        return _compress(2005, _get_more(collection_name, num_to_return, cursor_id), ctx)


    def _get_more_uncompressed(collection_name, num_to_return, cursor_id):
        """Internal getMore message helper."""
        return __pack_message(2005, _get_more(collection_name, num_to_return, cursor_id))


    if _use_c:
        _get_more_uncompressed = _cmessage._get_more_message

    def get_more(collection_name, num_to_return, cursor_id, ctx=None):
        """Get a **getMore** message."""
        if ctx:
            return _get_more_compressed(collection_name, num_to_return, cursor_id, ctx)
        return _get_more_uncompressed(collection_name, num_to_return, cursor_id)


    def _delete(collection_name, spec, opts, flags):
        """Get an OP_DELETE message."""
        encoded = _dict_to_bson(spec, False, opts)
        return (
         (b'').join([
          _ZERO_32,
          _make_c_string(collection_name),
          _pack_int(flags),
          encoded]), len(encoded))


    def _delete_compressed(collection_name, spec, opts, flags, ctx):
        """Internal compressed unacknowledged delete message helper."""
        op_delete, max_bson_size = _delete(collection_name, spec, opts, flags)
        rid, msg = _compress(2006, op_delete, ctx)
        return (rid, msg, max_bson_size)


    def _delete_uncompressed(collection_name, spec, safe, last_error_args, opts, flags=0):
        """Internal delete message helper."""
        op_delete, max_bson_size = _delete(collection_name, spec, opts, flags)
        rid, msg = __pack_message(2006, op_delete)
        if safe:
            rid, gle, _ = __last_error(collection_name, last_error_args)
            return (rid, msg + gle, max_bson_size)
        return (
         rid, msg, max_bson_size)


    def delete(collection_name, spec, safe, last_error_args, opts, flags=0, ctx=None):
        """Get a **delete** message.

    `opts` is a CodecOptions. `flags` is a bit vector that may contain
    the SingleRemove flag or not:

    http://docs.mongodb.org/meta-driver/latest/legacy/mongodb-wire-protocol/#op-delete
    """
        if ctx:
            return _delete_compressed(collection_name, spec, opts, flags, ctx)
        return _delete_uncompressed(collection_name, spec, safe, last_error_args, opts, flags)


    def kill_cursors(cursor_ids):
        """Get a **killCursors** message.
    """
        num_cursors = len(cursor_ids)
        pack = struct.Struct('<ii' + 'q' * num_cursors).pack
        op_kill_cursors = pack(0, num_cursors, *cursor_ids)
        return __pack_message(2007, op_kill_cursors)


    class _BulkWriteContext(object):
        __doc__ = 'A wrapper around SocketInfo for use with write splitting functions.'
        __slots__ = ('db_name', 'command', 'sock_info', 'op_id', 'name', 'field', 'publish',
                     'start_time', 'listeners', 'session', 'compress', 'op_type',
                     'codec')

        def __init__(self, database_name, command, sock_info, operation_id, listeners, session, op_type, codec):
            self.db_name = database_name
            self.command = command
            self.sock_info = sock_info
            self.op_id = operation_id
            self.listeners = listeners
            self.publish = listeners.enabled_for_commands
            self.name = next(iter(command))
            self.field = _FIELD_MAP[self.name]
            self.start_time = datetime.datetime.now() if self.publish else None
            self.session = session
            self.compress = True if sock_info.compression_context else False
            self.op_type = op_type
            self.codec = codec

        def _batch_command(self, docs):
            namespace = self.db_name + '.$cmd'
            request_id, msg, to_send = _do_bulk_write_command(namespace, self.op_type, self.command, docs, self.check_keys, self.codec, self)
            if not to_send:
                raise InvalidOperation('cannot do an empty bulk write')
            return (
             request_id, msg, to_send)

        def execute(self, docs, client):
            request_id, msg, to_send = self._batch_command(docs)
            result = self.write_command(request_id, msg, to_send)
            client._process_response(result, self.session)
            return (result, to_send)

        def execute_unack(self, docs, client):
            request_id, msg, to_send = self._batch_command(docs)
            self.legacy_write(request_id, msg, 0, False, to_send)
            return to_send

        @property
        def check_keys(self):
            """Should we check keys for this operation type?"""
            return self.op_type == _INSERT

        @property
        def max_bson_size(self):
            """A proxy for SockInfo.max_bson_size."""
            return self.sock_info.max_bson_size

        @property
        def max_message_size(self):
            """A proxy for SockInfo.max_message_size."""
            if self.compress:
                return self.sock_info.max_message_size - 16
            return self.sock_info.max_message_size

        @property
        def max_write_batch_size(self):
            """A proxy for SockInfo.max_write_batch_size."""
            return self.sock_info.max_write_batch_size

        @property
        def max_split_size(self):
            """The maximum size of a BSON command before batch splitting."""
            return self.max_bson_size

        def legacy_bulk_insert(self, request_id, msg, max_doc_size, acknowledged, docs, compress):
            if compress:
                request_id, msg = _compress(2002, msg, self.sock_info.compression_context)
            return self.legacy_write(request_id, msg, max_doc_size, acknowledged, docs)

        def legacy_write(self, request_id, msg, max_doc_size, acknowledged, docs):
            """A proxy for SocketInfo.legacy_write that handles event publishing.
        """
            if self.publish:
                duration = datetime.datetime.now() - self.start_time
                cmd = self._start(request_id, docs)
                start = datetime.datetime.now()
            try:
                try:
                    result = self.sock_info.legacy_write(request_id, msg, max_doc_size, acknowledged)
                    if self.publish:
                        duration = datetime.datetime.now() - start + duration
                        if result is not None:
                            reply = _convert_write_result(self.name, cmd, result)
                        else:
                            reply = {'ok': 1}
                        self._succeed(request_id, reply, duration)
                except OperationFailure as exc:
                    try:
                        if self.publish:
                            duration = datetime.datetime.now() - start + duration
                            self._fail(request_id, _convert_write_result(self.name, cmd, exc.details), duration)
                        raise
                    finally:
                        exc = None
                        del exc

            finally:
                self.start_time = datetime.datetime.now()

            return result

        def write_command(self, request_id, msg, docs):
            """A proxy for SocketInfo.write_command that handles event publishing.
        """
            if self.publish:
                duration = datetime.datetime.now() - self.start_time
                self._start(request_id, docs)
                start = datetime.datetime.now()
            try:
                try:
                    reply = self.sock_info.write_command(request_id, msg)
                    if self.publish:
                        duration = datetime.datetime.now() - start + duration
                        self._succeed(request_id, reply, duration)
                except OperationFailure as exc:
                    try:
                        if self.publish:
                            duration = datetime.datetime.now() - start + duration
                            self._fail(request_id, exc.details, duration)
                        raise
                    finally:
                        exc = None
                        del exc

            finally:
                self.start_time = datetime.datetime.now()

            return reply

        def _start(self, request_id, docs):
            """Publish a CommandStartedEvent."""
            cmd = self.command.copy()
            cmd[self.field] = docs
            self.listeners.publish_command_start(cmd, self.db_name, request_id, self.sock_info.address, self.op_id)
            return cmd

        def _succeed(self, request_id, reply, duration):
            """Publish a CommandSucceededEvent."""
            self.listeners.publish_command_success(duration, reply, self.name, request_id, self.sock_info.address, self.op_id)

        def _fail(self, request_id, failure, duration):
            """Publish a CommandFailedEvent."""
            self.listeners.publish_command_failure(duration, failure, self.name, request_id, self.sock_info.address, self.op_id)


    _MAX_SPLIT_SIZE_ENC = 2097152

    class _EncryptedBulkWriteContext(_BulkWriteContext):
        __slots__ = ()

        def _batch_command(self, docs):
            namespace = self.db_name + '.$cmd'
            msg, to_send = _encode_batched_write_command(namespace, self.op_type, self.command, docs, self.check_keys, self.codec, self)
            if not to_send:
                raise InvalidOperation('cannot do an empty bulk write')
            cmd_start = msg.index(b'\x00', 4) + 9
            cmd = _inflate_bson(memoryview(msg)[cmd_start:], DEFAULT_RAW_BSON_OPTIONS)
            return (cmd, to_send)

        def execute(self, docs, client):
            cmd, to_send = self._batch_command(docs)
            result = self.sock_info.command((self.db_name),
              cmd, codec_options=_UNICODE_REPLACE_CODEC_OPTIONS, session=(self.session),
              client=client)
            return (result, to_send)

        def execute_unack(self, docs, client):
            cmd, to_send = self._batch_command(docs)
            self.sock_info.command((self.db_name),
              cmd, write_concern=WriteConcern(w=0), session=(self.session),
              client=client)
            return to_send

        @property
        def max_split_size(self):
            """Reduce the batch splitting size."""
            return _MAX_SPLIT_SIZE_ENC


    def _raise_document_too_large(operation, doc_size, max_size):
        """Internal helper for raising DocumentTooLarge."""
        if operation == 'insert':
            raise DocumentTooLarge('BSON document too large (%d bytes) - the connected server supports BSON document sizes up to %d bytes.' % (
             doc_size, max_size))
        else:
            raise DocumentTooLarge('%r command document too large' % (operation,))


    def _do_batched_insert--- This code section failed: ---

 L.1085         0  LOAD_CLOSURE             'collection_name'
                2  LOAD_CLOSURE             'last_error_args'
                4  BUILD_TUPLE_2         2 
                6  LOAD_CODE                <code_object _insert_message>
                8  LOAD_STR                 '_do_batched_insert.<locals>._insert_message'
               10  MAKE_FUNCTION_8          'closure'
               12  STORE_FAST               '_insert_message'

 L.1095        14  LOAD_FAST                'safe'
               16  JUMP_IF_TRUE_OR_POP    22  'to 22'
               18  LOAD_FAST                'continue_on_error'
               20  UNARY_NOT        
             22_0  COME_FROM            16  '16'
               22  STORE_FAST               'send_safe'

 L.1096        24  LOAD_CONST               None
               26  STORE_FAST               'last_error'

 L.1097        28  LOAD_GLOBAL              StringIO
               30  CALL_FUNCTION_0       0  ''
               32  STORE_FAST               'data'

 L.1098        34  LOAD_FAST                'data'
               36  LOAD_METHOD              write
               38  LOAD_GLOBAL              struct
               40  LOAD_METHOD              pack
               42  LOAD_STR                 '<i'
               44  LOAD_GLOBAL              int
               46  LOAD_FAST                'continue_on_error'
               48  CALL_FUNCTION_1       1  ''
               50  CALL_METHOD_2         2  ''
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          

 L.1099        56  LOAD_FAST                'data'
               58  LOAD_METHOD              write
               60  LOAD_GLOBAL              _make_c_string
               62  LOAD_DEREF               'collection_name'
               64  CALL_FUNCTION_1       1  ''
               66  CALL_METHOD_1         1  ''
               68  POP_TOP          

 L.1100        70  LOAD_FAST                'data'
               72  LOAD_METHOD              tell
               74  CALL_METHOD_0         0  ''
               76  DUP_TOP          
               78  STORE_FAST               'message_length'
               80  STORE_FAST               'begin_loc'

 L.1101        82  LOAD_CONST               False
               84  STORE_FAST               'has_docs'

 L.1102        86  BUILD_LIST_0          0 
               88  STORE_FAST               'to_send'

 L.1103        90  LOAD_GLOBAL              _dict_to_bson
               92  STORE_FAST               'encode'

 L.1104        94  LOAD_FAST                'ctx'
               96  LOAD_ATTR                compress
               98  JUMP_IF_FALSE_OR_POP   108  'to 108'
              100  LOAD_FAST                'safe'
              102  JUMP_IF_TRUE_OR_POP   106  'to 106'
              104  LOAD_FAST                'send_safe'
            106_0  COME_FROM           102  '102'
              106  UNARY_NOT        
            108_0  COME_FROM            98  '98'
              108  STORE_FAST               'compress'

 L.1105       110  LOAD_FAST                'docs'
              112  GET_ITER         
          114_116  FOR_ITER            400  'to 400'
              118  STORE_FAST               'doc'

 L.1106       120  LOAD_FAST                'encode'
              122  LOAD_FAST                'doc'
              124  LOAD_FAST                'check_keys'
              126  LOAD_FAST                'opts'
              128  CALL_FUNCTION_3       3  ''
              130  STORE_FAST               'encoded'

 L.1107       132  LOAD_GLOBAL              len
              134  LOAD_FAST                'encoded'
              136  CALL_FUNCTION_1       1  ''
              138  STORE_FAST               'encoded_length'

 L.1108       140  LOAD_FAST                'encoded_length'
              142  LOAD_FAST                'ctx'
              144  LOAD_ATTR                max_bson_size
              146  COMPARE_OP               >
              148  STORE_FAST               'too_large'

 L.1110       150  LOAD_FAST                'message_length'
              152  LOAD_FAST                'encoded_length'
              154  INPLACE_ADD      
              156  STORE_FAST               'message_length'

 L.1111       158  LOAD_FAST                'message_length'
              160  LOAD_FAST                'ctx'
              162  LOAD_ATTR                max_message_size
              164  COMPARE_OP               <
              166  POP_JUMP_IF_FALSE   198  'to 198'
              168  LOAD_FAST                'too_large'
              170  POP_JUMP_IF_TRUE    198  'to 198'

 L.1112       172  LOAD_FAST                'data'
              174  LOAD_METHOD              write
              176  LOAD_FAST                'encoded'
              178  CALL_METHOD_1         1  ''
              180  POP_TOP          

 L.1113       182  LOAD_FAST                'to_send'
              184  LOAD_METHOD              append
              186  LOAD_FAST                'doc'
              188  CALL_METHOD_1         1  ''
              190  POP_TOP          

 L.1114       192  LOAD_CONST               True
              194  STORE_FAST               'has_docs'

 L.1115       196  JUMP_BACK           114  'to 114'
            198_0  COME_FROM           170  '170'
            198_1  COME_FROM           166  '166'

 L.1117       198  LOAD_FAST                'has_docs'
          200_202  POP_JUMP_IF_FALSE   336  'to 336'

 L.1119       204  SETUP_FINALLY       268  'to 268'

 L.1120       206  LOAD_FAST                'compress'
              208  POP_JUMP_IF_FALSE   226  'to 226'

 L.1121       210  LOAD_CONST               None
              212  LOAD_FAST                'data'
              214  LOAD_METHOD              getvalue
              216  CALL_METHOD_0         0  ''
              218  ROT_TWO          
              220  STORE_FAST               'rid'
              222  STORE_FAST               'msg'
              224  JUMP_FORWARD        244  'to 244'
            226_0  COME_FROM           208  '208'

 L.1123       226  LOAD_FAST                '_insert_message'
              228  LOAD_FAST                'data'
              230  LOAD_METHOD              getvalue
              232  CALL_METHOD_0         0  ''
              234  LOAD_FAST                'send_safe'
              236  CALL_FUNCTION_2       2  ''
              238  UNPACK_SEQUENCE_2     2 
              240  STORE_FAST               'rid'
              242  STORE_FAST               'msg'
            244_0  COME_FROM           224  '224'

 L.1124       244  LOAD_FAST                'ctx'
              246  LOAD_METHOD              legacy_bulk_insert

 L.1125       248  LOAD_FAST                'rid'

 L.1125       250  LOAD_FAST                'msg'

 L.1125       252  LOAD_CONST               0

 L.1125       254  LOAD_FAST                'send_safe'

 L.1125       256  LOAD_FAST                'to_send'

 L.1125       258  LOAD_FAST                'compress'

 L.1124       260  CALL_METHOD_6         6  ''
              262  POP_TOP          
              264  POP_BLOCK        
              266  JUMP_FORWARD        336  'to 336'
            268_0  COME_FROM_FINALLY   204  '204'

 L.1128       268  DUP_TOP          
              270  LOAD_GLOBAL              OperationFailure
              272  COMPARE_OP               exception-match
          274_276  POP_JUMP_IF_FALSE   334  'to 334'
              278  POP_TOP          
              280  STORE_FAST               'exc'
              282  POP_TOP          
              284  SETUP_FINALLY       322  'to 322'

 L.1130       286  LOAD_FAST                'continue_on_error'
          288_290  POP_JUMP_IF_FALSE   298  'to 298'

 L.1132       292  LOAD_FAST                'exc'
              294  STORE_FAST               'last_error'
              296  JUMP_FORWARD        318  'to 318'
            298_0  COME_FROM           288  '288'

 L.1134       298  LOAD_FAST                'safe'
          300_302  POP_JUMP_IF_TRUE    316  'to 316'

 L.1135       304  POP_BLOCK        
              306  POP_EXCEPT       
              308  CALL_FINALLY        322  'to 322'
              310  POP_TOP          
              312  LOAD_CONST               None
              314  RETURN_VALUE     
            316_0  COME_FROM           300  '300'

 L.1138       316  RAISE_VARARGS_0       0  'reraise'
            318_0  COME_FROM           296  '296'
              318  POP_BLOCK        
              320  BEGIN_FINALLY    
            322_0  COME_FROM           308  '308'
            322_1  COME_FROM_FINALLY   284  '284'
              322  LOAD_CONST               None
              324  STORE_FAST               'exc'
              326  DELETE_FAST              'exc'
              328  END_FINALLY      
              330  POP_EXCEPT       
              332  JUMP_FORWARD        336  'to 336'
            334_0  COME_FROM           274  '274'
              334  END_FINALLY      
            336_0  COME_FROM           332  '332'
            336_1  COME_FROM           266  '266'
            336_2  COME_FROM           200  '200'

 L.1140       336  LOAD_FAST                'too_large'
          338_340  POP_JUMP_IF_FALSE   356  'to 356'

 L.1141       342  LOAD_GLOBAL              _raise_document_too_large

 L.1142       344  LOAD_STR                 'insert'

 L.1142       346  LOAD_FAST                'encoded_length'

 L.1142       348  LOAD_FAST                'ctx'
              350  LOAD_ATTR                max_bson_size

 L.1141       352  CALL_FUNCTION_3       3  ''
              354  POP_TOP          
            356_0  COME_FROM           338  '338'

 L.1144       356  LOAD_FAST                'begin_loc'
              358  LOAD_FAST                'encoded_length'
              360  BINARY_ADD       
              362  STORE_FAST               'message_length'

 L.1145       364  LOAD_FAST                'data'
              366  LOAD_METHOD              seek
              368  LOAD_FAST                'begin_loc'
              370  CALL_METHOD_1         1  ''
              372  POP_TOP          

 L.1146       374  LOAD_FAST                'data'
              376  LOAD_METHOD              truncate
              378  CALL_METHOD_0         0  ''
              380  POP_TOP          

 L.1147       382  LOAD_FAST                'data'
              384  LOAD_METHOD              write
              386  LOAD_FAST                'encoded'
              388  CALL_METHOD_1         1  ''
              390  POP_TOP          

 L.1148       392  LOAD_FAST                'doc'
              394  BUILD_LIST_1          1 
              396  STORE_FAST               'to_send'
              398  JUMP_BACK           114  'to 114'

 L.1150       400  LOAD_FAST                'has_docs'
          402_404  POP_JUMP_IF_TRUE    414  'to 414'

 L.1151       406  LOAD_GLOBAL              InvalidOperation
              408  LOAD_STR                 'cannot do an empty bulk insert'
              410  CALL_FUNCTION_1       1  ''
              412  RAISE_VARARGS_1       1  'exception instance'
            414_0  COME_FROM           402  '402'

 L.1153       414  LOAD_FAST                'compress'
          416_418  POP_JUMP_IF_FALSE   436  'to 436'

 L.1154       420  LOAD_CONST               None
              422  LOAD_FAST                'data'
              424  LOAD_METHOD              getvalue
              426  CALL_METHOD_0         0  ''
              428  ROT_TWO          
              430  STORE_FAST               'request_id'
              432  STORE_FAST               'msg'
              434  JUMP_FORWARD        454  'to 454'
            436_0  COME_FROM           416  '416'

 L.1156       436  LOAD_FAST                '_insert_message'
              438  LOAD_FAST                'data'
              440  LOAD_METHOD              getvalue
              442  CALL_METHOD_0         0  ''
              444  LOAD_FAST                'safe'
              446  CALL_FUNCTION_2       2  ''
              448  UNPACK_SEQUENCE_2     2 
              450  STORE_FAST               'request_id'
              452  STORE_FAST               'msg'
            454_0  COME_FROM           434  '434'

 L.1157       454  LOAD_FAST                'ctx'
              456  LOAD_METHOD              legacy_bulk_insert
              458  LOAD_FAST                'request_id'
              460  LOAD_FAST                'msg'
              462  LOAD_CONST               0
              464  LOAD_FAST                'safe'
              466  LOAD_FAST                'to_send'
              468  LOAD_FAST                'compress'
              470  CALL_METHOD_6         6  ''
              472  POP_TOP          

 L.1160       474  LOAD_FAST                'last_error'
              476  LOAD_CONST               None
              478  COMPARE_OP               is-not
          480_482  POP_JUMP_IF_FALSE   488  'to 488'

 L.1161       484  LOAD_FAST                'last_error'
              486  RAISE_VARARGS_1       1  'exception instance'
            488_0  COME_FROM           480  '480'

Parse error at or near `POP_EXCEPT' instruction at offset 306


    if _use_c:
        _do_batched_insert = _cmessage._do_batched_insert
    _OP_MSG_MAP = {_INSERT: b'documents\x00', 
     _UPDATE: b'updates\x00', 
     _DELETE: b'deletes\x00'}

    def _batched_op_msg_impl(operation, command, docs, check_keys, ack, opts, ctx, buf):
        """Create a batched OP_MSG write."""
        max_bson_size = ctx.max_bson_size
        max_write_batch_size = ctx.max_write_batch_size
        max_message_size = ctx.max_message_size
        flags = b'\x00\x00\x00\x00' if ack else b'\x02\x00\x00\x00'
        buf.write(flags)
        buf.write(b'\x00')
        buf.write(_dict_to_bson(command, False, opts))
        buf.write(b'\x01')
        size_location = buf.tell()
        buf.write(b'\x00\x00\x00\x00')
        try:
            buf.write(_OP_MSG_MAP[operation])
        except KeyError:
            raise InvalidOperation('Unknown command')
        else:
            if operation in (_UPDATE, _DELETE):
                check_keys = False
            to_send = []
            idx = 0
            for doc in docs:
                value = _dict_to_bson(doc, check_keys, opts)
                doc_length = len(value)
                new_message_size = buf.tell() + doc_length
                doc_too_large = idx == 0 and new_message_size > max_message_size
                unacked_doc_too_large = not ack and doc_length > max_bson_size
                if not doc_too_large:
                    if unacked_doc_too_large:
                        write_op = list(_FIELD_MAP.keys())[operation]
                        _raise_document_too_large(write_op, len(value), max_bson_size)
                    if new_message_size > max_message_size:
                        break
                    buf.write(value)
                    to_send.append(doc)
                    idx += 1
                    if idx == max_write_batch_size:
                        break
                length = buf.tell()
                buf.seek(size_location)
                buf.write(_pack_int(length - size_location))
                return (
                 to_send, length)


    def _encode_batched_op_msg(operation, command, docs, check_keys, ack, opts, ctx):
        """Encode the next batched insert, update, or delete operation
    as OP_MSG.
    """
        buf = StringIO()
        to_send, _ = _batched_op_msg_impl(operation, command, docs, check_keys, ack, opts, ctx, buf)
        return (buf.getvalue(), to_send)


    if _use_c:
        _encode_batched_op_msg = _cmessage._encode_batched_op_msg

    def _batched_op_msg_compressed(operation, command, docs, check_keys, ack, opts, ctx):
        """Create the next batched insert, update, or delete operation
    with OP_MSG, compressed.
    """
        data, to_send = _encode_batched_op_msg(operation, command, docs, check_keys, ack, opts, ctx)
        request_id, msg = _compress(2013, data, ctx.sock_info.compression_context)
        return (request_id, msg, to_send)


    def _batched_op_msg(operation, command, docs, check_keys, ack, opts, ctx):
        """OP_MSG implementation entry point."""
        buf = StringIO()
        buf.write(_ZERO_64)
        buf.write(b'\x00\x00\x00\x00\xdd\x07\x00\x00')
        to_send, length = _batched_op_msg_impl(operation, command, docs, check_keys, ack, opts, ctx, buf)
        buf.seek(4)
        request_id = _randint()
        buf.write(_pack_int(request_id))
        buf.seek(0)
        buf.write(_pack_int(length))
        return (
         request_id, buf.getvalue(), to_send)


    if _use_c:
        _batched_op_msg = _cmessage._batched_op_msg

    def _do_batched_op_msg(namespace, operation, command, docs, check_keys, opts, ctx):
        """Create the next batched insert, update, or delete operation
    using OP_MSG.
    """
        command['$db'] = namespace.split('.', 1)[0]
        if 'writeConcern' in command:
            ack = bool(command['writeConcern'].get('w', 1))
        else:
            ack = True
        if ctx.sock_info.compression_context:
            return _batched_op_msg_compressed(operation, command, docs, check_keys, ack, opts, ctx)
        return _batched_op_msg(operation, command, docs, check_keys, ack, opts, ctx)


    def _batched_write_command_compressed(namespace, operation, command, docs, check_keys, opts, ctx):
        """Create the next batched insert, update, or delete command, compressed.
    """
        data, to_send = _encode_batched_write_command(namespace, operation, command, docs, check_keys, opts, ctx)
        request_id, msg = _compress(2004, data, ctx.sock_info.compression_context)
        return (request_id, msg, to_send)


    def _encode_batched_write_command(namespace, operation, command, docs, check_keys, opts, ctx):
        """Encode the next batched insert, update, or delete command.
    """
        buf = StringIO()
        to_send, _ = _batched_write_command_impl(namespace, operation, command, docs, check_keys, opts, ctx, buf)
        return (buf.getvalue(), to_send)


    if _use_c:
        _encode_batched_write_command = _cmessage._encode_batched_write_command

    def _batched_write_command(namespace, operation, command, docs, check_keys, opts, ctx):
        """Create the next batched insert, update, or delete command.
    """
        buf = StringIO()
        buf.write(_ZERO_64)
        buf.write(b'\x00\x00\x00\x00\xd4\x07\x00\x00')
        to_send, length = _batched_write_command_impl(namespace, operation, command, docs, check_keys, opts, ctx, buf)
        buf.seek(4)
        request_id = _randint()
        buf.write(_pack_int(request_id))
        buf.seek(0)
        buf.write(_pack_int(length))
        return (
         request_id, buf.getvalue(), to_send)


    if _use_c:
        _batched_write_command = _cmessage._batched_write_command

    def _do_batched_write_command(namespace, operation, command, docs, check_keys, opts, ctx):
        """Batched write commands entry point."""
        if ctx.sock_info.compression_context:
            return _batched_write_command_compressed(namespace, operation, command, docs, check_keys, opts, ctx)
        return _batched_write_command(namespace, operation, command, docs, check_keys, opts, ctx)


    def _do_bulk_write_command(namespace, operation, command, docs, check_keys, opts, ctx):
        """Bulk write commands entry point."""
        if ctx.sock_info.max_wire_version > 5:
            return _do_batched_op_msg(namespace, operation, command, docs, check_keys, opts, ctx)
        return _do_batched_write_command(namespace, operation, command, docs, check_keys, opts, ctx)


    def _batched_write_command_impl(namespace, operation, command, docs, check_keys, opts, ctx, buf):
        """Create a batched OP_QUERY write command."""
        max_bson_size = ctx.max_bson_size
        max_write_batch_size = ctx.max_write_batch_size
        max_cmd_size = max_bson_size + _COMMAND_OVERHEAD
        max_split_size = ctx.max_split_size
        buf.write(_ZERO_32)
        buf.write(b(namespace))
        buf.write(_ZERO_8)
        buf.write(_SKIPLIM)
        command_start = buf.tell()
        buf.write(encode(command))
        buf.seek(-1, 2)
        buf.truncate()
        try:
            buf.write(_OP_MAP[operation])
        except KeyError:
            raise InvalidOperation('Unknown command')
        else:
            if operation in (_UPDATE, _DELETE):
                check_keys = False
            list_start = buf.tell() - 4
            to_send = []
            idx = 0
            for doc in docs:
                key = b(str(idx))
                value = encode(doc, check_keys, opts)
                doc_too_large = len(value) > max_cmd_size
                if doc_too_large:
                    write_op = list(_FIELD_MAP.keys())[operation]
                    _raise_document_too_large(write_op, len(value), max_bson_size)
                enough_data = idx >= 1 and buf.tell() + len(key) + len(value) >= max_split_size
                enough_documents = idx >= max_write_batch_size
                if not enough_data:
                    if enough_documents:
                        break
                    buf.write(_BSONOBJ)
                    buf.write(key)
                    buf.write(_ZERO_8)
                    buf.write(value)
                    to_send.append(doc)
                    idx += 1
                buf.write(_ZERO_16)
                length = buf.tell()
                buf.seek(list_start)
                buf.write(_pack_int(length - list_start - 1))
                buf.seek(command_start)
                buf.write(_pack_int(length - command_start))
                return (
                 to_send, length)


    class _OpReply(object):
        __doc__ = 'A MongoDB OP_REPLY response message.'
        __slots__ = ('flags', 'cursor_id', 'number_returned', 'documents')
        UNPACK_FROM = struct.Struct('<iqii').unpack_from
        OP_CODE = 1

        def __init__(self, flags, cursor_id, number_returned, documents):
            self.flags = flags
            self.cursor_id = cursor_id
            self.number_returned = number_returned
            self.documents = documents

        def raw_response(self, cursor_id=None):
            """Check the response header from the database, without decoding BSON.

        Check the response for errors and unpack.

        Can raise CursorNotFound, NotMasterError, ExecutionTimeout, or
        OperationFailure.

        :Parameters:
          - `cursor_id` (optional): cursor_id we sent to get this response -
            used for raising an informative exception when we get cursor id not
            valid at server response.
        """
            if self.flags & 1:
                if cursor_id is None:
                    raise ProtocolError('No cursor id for getMore operation')
                msg = 'Cursor not found, cursor id: %d' % (cursor_id,)
                errobj = {'ok':0,  'errmsg':msg,  'code':43}
                raise CursorNotFound(msg, 43, errobj)
            else:
                if self.flags & 2:
                    error_object = bson.BSON(self.documents).decode()
                    error_object.setdefault('ok', 0)
                    if error_object['$err'].startswith('not master'):
                        raise NotMasterError(error_object['$err'], error_object)
                    else:
                        if error_object.get('code') == 50:
                            raise ExecutionTimeout(error_object.get('$err'), error_object.get('code'), error_object)
                    raise OperationFailure('database error: %s' % error_object.get('$err'), error_object.get('code'), error_object)
            return [
             self.documents]

        def unpack_response(self, cursor_id=None, codec_options=_UNICODE_REPLACE_CODEC_OPTIONS, user_fields=None, legacy_response=False):
            """Unpack a response from the database and decode the BSON document(s).

        Check the response for errors and unpack, returning a dictionary
        containing the response data.

        Can raise CursorNotFound, NotMasterError, ExecutionTimeout, or
        OperationFailure.

        :Parameters:
          - `cursor_id` (optional): cursor_id we sent to get this response -
            used for raising an informative exception when we get cursor id not
            valid at server response
          - `codec_options` (optional): an instance of
            :class:`~bson.codec_options.CodecOptions`
        """
            self.raw_response(cursor_id)
            if legacy_response:
                return bson.decode_all(self.documents, codec_options)
            return bson._decode_all_selective(self.documents, codec_options, user_fields)

        def command_response(self):
            """Unpack a command response."""
            docs = self.unpack_response()
            assert self.number_returned == 1
            return docs[0]

        def raw_command_response(self):
            """Return the bytes of the command response."""
            raise NotImplementedError

        @classmethod
        def unpack(cls, msg):
            """Construct an _OpReply from raw bytes."""
            flags, cursor_id, _, number_returned = cls.UNPACK_FROM(msg)
            documents = bytes(msg[20:])
            return cls(flags, cursor_id, number_returned, documents)


    class _OpMsg(object):
        __doc__ = 'A MongoDB OP_MSG response message.'
        __slots__ = ('flags', 'cursor_id', 'number_returned', 'payload_document')
        UNPACK_FROM = struct.Struct('<IBi').unpack_from
        OP_CODE = 2013

        def __init__(self, flags, payload_document):
            self.flags = flags
            self.payload_document = payload_document

        def raw_response(self, cursor_id=None):
            raise NotImplementedError

        def unpack_response(self, cursor_id=None, codec_options=_UNICODE_REPLACE_CODEC_OPTIONS, user_fields=None, legacy_response=False):
            """Unpack a OP_MSG command response.

        :Parameters:
          - `cursor_id` (optional): Ignored, for compatibility with _OpReply.
          - `codec_options` (optional): an instance of
            :class:`~bson.codec_options.CodecOptions`
        """
            assert not legacy_response
            return bson._decode_all_selective(self.payload_document, codec_options, user_fields)

        def command_response(self):
            """Unpack a command response."""
            return self.unpack_response()[0]

        def raw_command_response(self):
            """Return the bytes of the command response."""
            return self.payload_document

        @classmethod
        def unpack(cls, msg):
            """Construct an _OpMsg from raw bytes."""
            flags, first_payload_type, first_payload_size = cls.UNPACK_FROM(msg)
            if flags != 0:
                raise ProtocolError('Unsupported OP_MSG flags (%r)' % (flags,))
            if first_payload_type != 0:
                raise ProtocolError('Unsupported OP_MSG payload type (%r)' % (first_payload_type,))
            if len(msg) != first_payload_size + 5:
                raise ProtocolError('Unsupported OP_MSG reply: >1 section')
            payload_document = bytes(msg[5:])
            return cls(flags, payload_document)


    _UNPACK_REPLY = {_OpReply.OP_CODE: _OpReply.unpack, 
     _OpMsg.OP_CODE: _OpMsg.unpack}

    def _first_batch(sock_info, db, coll, query, ntoreturn, slave_ok, codec_options, read_preference, cmd, listeners):
        """Simple query helper for retrieving a first (and possibly only) batch."""
        query = _Query(0, db, coll, 0, query, None, codec_options, read_preference, ntoreturn, 0, DEFAULT_READ_CONCERN, None, None, None)
        name = next(iter(cmd))
        publish = listeners.enabled_for_commands
        if publish:
            start = datetime.datetime.now()
        request_id, msg, max_doc_size = query.get_message(slave_ok, sock_info)
        if publish:
            encoding_duration = datetime.datetime.now() - start
            listeners.publish_command_start(cmd, db, request_id, sock_info.address)
            start = datetime.datetime.now()
        sock_info.send_message(msg, max_doc_size)
        reply = sock_info.receive_message(request_id)
        try:
            docs = reply.unpack_response(None, codec_options)
        except Exception as exc:
            try:
                if publish:
                    duration = datetime.datetime.now() - start + encoding_duration
                    if isinstance(exc, (NotMasterError, OperationFailure)):
                        failure = exc.details
                    else:
                        failure = _convert_exception(exc)
                    listeners.publish_command_failure(duration, failure, name, request_id, sock_info.address)
                raise
            finally:
                exc = None
                del exc

        else:
            if 'cursor' in cmd:
                result = {'cursor':{'firstBatch':docs, 
                  'id':reply.cursor_id, 
                  'ns':'%s.%s' % (db, coll)}, 
                 'ok':1.0}
            else:
                result = docs[0] if docs else {}
                result['ok'] = 1.0
            if publish:
                duration = datetime.datetime.now() - start + encoding_duration
                listeners.publish_command_success(duration, result, name, request_id, sock_info.address)
            return result