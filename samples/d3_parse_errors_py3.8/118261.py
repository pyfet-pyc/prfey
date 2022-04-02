# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pymongo\client_session.py
"""Logical sessions for ordering sequential operations.

Requires MongoDB 3.6.

.. versionadded:: 3.6

Causally Consistent Reads
=========================

.. code-block:: python

  with client.start_session(causal_consistency=True) as session:
      collection = client.db.collection
      collection.update_one({'_id': 1}, {'$set': {'x': 10}}, session=session)
      secondary_c = collection.with_options(
          read_preference=ReadPreference.SECONDARY)

      # A secondary read waits for replication of the write.
      secondary_c.find_one({'_id': 1}, session=session)

If `causal_consistency` is True (the default), read operations that use
the session are causally after previous read and write operations. Using a
causally consistent session, an application can read its own writes and is
guaranteed monotonic reads, even when reading from replica set secondaries.

.. mongodoc:: causal-consistency

.. _transactions-ref:

Transactions
============

MongoDB 4.0 adds support for transactions on replica set primaries. A
transaction is associated with a :class:`ClientSession`. To start a transaction
on a session, use :meth:`ClientSession.start_transaction` in a with-statement.
Then, execute an operation within the transaction by passing the session to the
operation:

.. code-block:: python

  orders = client.db.orders
  inventory = client.db.inventory
  with client.start_session() as session:
      with session.start_transaction():
          orders.insert_one({"sku": "abc123", "qty": 100}, session=session)
          inventory.update_one({"sku": "abc123", "qty": {"$gte": 100}},
                               {"$inc": {"qty": -100}}, session=session)

Upon normal completion of ``with session.start_transaction()`` block, the
transaction automatically calls :meth:`ClientSession.commit_transaction`.
If the block exits with an exception, the transaction automatically calls
:meth:`ClientSession.abort_transaction`.

For multi-document transactions, you can only specify read/write (CRUD)
operations on existing collections. For example, a multi-document transaction
cannot include a create or drop collection/index operations, including an
insert operation that would result in the creation of a new collection.

A session may only have a single active transaction at a time, multiple
transactions on the same session can be executed in sequence.

.. versionadded:: 3.7

Sharded Transactions
^^^^^^^^^^^^^^^^^^^^

PyMongo 3.9 adds support for transactions on sharded clusters running MongoDB
4.2. Sharded transactions have the same API as replica set transactions.
When running a transaction against a sharded cluster, the session is
pinned to the mongos server selected for the first operation in the
transaction. All subsequent operations that are part of the same transaction
are routed to the same mongos server. When the transaction is completed, by
running either commitTransaction or abortTransaction, the session is unpinned.

.. versionadded:: 3.9

.. mongodoc:: transactions

Classes
=======
"""
import collections, os, sys, uuid
from bson.binary import Binary
from bson.int64 import Int64
from bson.py3compat import abc, integer_types, reraise_instance
from bson.son import SON
from bson.timestamp import Timestamp
from pymongo import monotonic
from pymongo.errors import ConfigurationError, ConnectionFailure, InvalidOperation, OperationFailure, PyMongoError, ServerSelectionTimeoutError, WTimeoutError
from pymongo.helpers import _RETRYABLE_ERROR_CODES
from pymongo.read_concern import ReadConcern
from pymongo.read_preferences import ReadPreference, _ServerMode
from pymongo.write_concern import WriteConcern

class SessionOptions(object):
    __doc__ = 'Options for a new :class:`ClientSession`.\n\n    :Parameters:\n      - `causal_consistency` (optional): If True (the default), read\n        operations are causally ordered within the session.\n      - `default_transaction_options` (optional): The default\n        TransactionOptions to use for transactions started on this session.\n    '

    def __init__(self, causal_consistency=True, default_transaction_options=None):
        self._causal_consistency = causal_consistency
        if default_transaction_options is not None:
            if not isinstance(default_transaction_options, TransactionOptions):
                raise TypeError('default_transaction_options must be an instance of pymongo.client_session.TransactionOptions, not: %r' % (
                 default_transaction_options,))
        self._default_transaction_options = default_transaction_options

    @property
    def causal_consistency(self):
        """Whether causal consistency is configured."""
        return self._causal_consistency

    @property
    def default_transaction_options(self):
        """The default TransactionOptions to use for transactions started on
        this session.

        .. versionadded:: 3.7
        """
        return self._default_transaction_options


class TransactionOptions(object):
    __doc__ = 'Options for :meth:`ClientSession.start_transaction`.\n    \n    :Parameters:\n      - `read_concern` (optional): The\n        :class:`~pymongo.read_concern.ReadConcern` to use for this transaction.\n        If ``None`` (the default) the :attr:`read_preference` of\n        the :class:`MongoClient` is used.\n      - `write_concern` (optional): The\n        :class:`~pymongo.write_concern.WriteConcern` to use for this\n        transaction. If ``None`` (the default) the :attr:`read_preference` of\n        the :class:`MongoClient` is used.\n      - `read_preference` (optional): The read preference to use. If\n        ``None`` (the default) the :attr:`read_preference` of this\n        :class:`MongoClient` is used. See :mod:`~pymongo.read_preferences`\n        for options. Transactions which read must use\n        :attr:`~pymongo.read_preferences.ReadPreference.PRIMARY`.\n      - `max_commit_time_ms` (optional): The maximum amount of time to allow a\n        single commitTransaction command to run. This option is an alias for\n        maxTimeMS option on the commitTransaction command. If ``None`` (the\n        default) maxTimeMS is not used.\n\n    .. versionchanged:: 3.9\n       Added the ``max_commit_time_ms`` option.\n\n    .. versionadded:: 3.7\n    '

    def __init__(self, read_concern=None, write_concern=None, read_preference=None, max_commit_time_ms=None):
        self._read_concern = read_concern
        self._write_concern = write_concern
        self._read_preference = read_preference
        self._max_commit_time_ms = max_commit_time_ms
        if read_concern is not None:
            if not isinstance(read_concern, ReadConcern):
                raise TypeError('read_concern must be an instance of pymongo.read_concern.ReadConcern, not: %r' % (
                 read_concern,))
            if write_concern is not None:
                if not isinstance(write_concern, WriteConcern):
                    raise TypeError('write_concern must be an instance of pymongo.write_concern.WriteConcern, not: %r' % (
                     write_concern,))
                assert write_concern.acknowledged, 'transactions do not support unacknowledged write concern: %r' % (
                 write_concern,)
        if read_preference is not None:
            if not isinstance(read_preference, _ServerMode):
                raise TypeError('%r is not valid for read_preference. See pymongo.read_preferences for valid options.' % (
                 read_preference,))
            if max_commit_time_ms is not None and not isinstance(max_commit_time_ms, integer_types):
                raise TypeError('max_commit_time_ms must be an integer or None')

    @property
    def read_concern(self):
        """This transaction's :class:`~pymongo.read_concern.ReadConcern`."""
        return self._read_concern

    @property
    def write_concern(self):
        """This transaction's :class:`~pymongo.write_concern.WriteConcern`."""
        return self._write_concern

    @property
    def read_preference(self):
        """This transaction's :class:`~pymongo.read_preferences.ReadPreference`.
        """
        return self._read_preference

    @property
    def max_commit_time_ms(self):
        """The maxTimeMS to use when running a commitTransaction command.

        .. versionadded:: 3.9
        """
        return self._max_commit_time_ms


def _validate_session_write_concern(session, write_concern):
    """Validate that an explicit session is not used with an unack'ed write.

    Returns the session to use for the next operation.
    """
    if not session or write_concern is not None:
        if not write_concern.acknowledged:
            if session._implicit:
                return
            raise ConfigurationError('Explicit sessions are incompatible with unacknowledged write concern: %r' % (
             write_concern,))
        return session


class _TransactionContext(object):
    __doc__ = 'Internal transaction context manager for start_transaction.'

    def __init__(self, session):
        self._TransactionContext__session = session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._TransactionContext__session.in_transaction:
            if exc_val is None:
                self._TransactionContext__session.commit_transaction()
            else:
                self._TransactionContext__session.abort_transaction()


class _TxnState(object):
    NONE = 1
    STARTING = 2
    IN_PROGRESS = 3
    COMMITTED = 4
    COMMITTED_EMPTY = 5
    ABORTED = 6


class _Transaction(object):
    __doc__ = 'Internal class to hold transaction information in a ClientSession.'

    def __init__(self, opts):
        self.opts = opts
        self.state = _TxnState.NONE
        self.sharded = False
        self.pinned_address = None
        self.recovery_token = None

    def active(self):
        return self.state in (_TxnState.STARTING, _TxnState.IN_PROGRESS)

    def reset(self):
        self.state = _TxnState.NONE
        self.sharded = False
        self.pinned_address = None
        self.recovery_token = None


def _reraise_with_unknown_commit(exc):
    """Re-raise an exception with the UnknownTransactionCommitResult label."""
    exc._add_error_label('UnknownTransactionCommitResult')
    reraise_instance(exc, trace=(sys.exc_info()[2]))


def _max_time_expired_error(exc):
    """Return true if exc is a MaxTimeMSExpired error."""
    return isinstance(exc, OperationFailure) and exc.code == 50


_UNKNOWN_COMMIT_ERROR_CODES = _RETRYABLE_ERROR_CODES | frozenset([
 64,
 50])
_WITH_TRANSACTION_RETRY_TIME_LIMIT = 120

def _within_time_limit(start_time):
    """Are we within the with_transaction retry limit?"""
    return monotonic.time() - start_time < _WITH_TRANSACTION_RETRY_TIME_LIMIT


class ClientSession(object):
    __doc__ = 'A session for ordering sequential operations.'

    def __init__(self, client, server_session, options, authset, implicit):
        self._client = client
        self._server_session = server_session
        self._options = options
        self._authset = authset
        self._cluster_time = None
        self._operation_time = None
        self._implicit = implicit
        self._transaction = _Transaction(None)

    def end_session(self):
        """Finish this session. If a transaction has started, abort it.

        It is an error to use the session after the session has ended.
        """
        self._end_session(lock=True)

    def _end_session(self, lock):
        if self._server_session is not None:
            try:
                if self.in_transaction:
                    self.abort_transaction()
            finally:
                self._client._return_server_session(self._server_session, lock)
                self._server_session = None

    def _check_ended(self):
        if self._server_session is None:
            raise InvalidOperation('Cannot use ended session')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._end_session(lock=True)

    @property
    def client(self):
        """The :class:`~pymongo.mongo_client.MongoClient` this session was
        created from.
        """
        return self._client

    @property
    def options(self):
        """The :class:`SessionOptions` this session was created with."""
        return self._options

    @property
    def session_id(self):
        """A BSON document, the opaque server session identifier."""
        self._check_ended()
        return self._server_session.session_id

    @property
    def cluster_time(self):
        """The cluster time returned by the last operation executed
        in this session.
        """
        return self._cluster_time

    @property
    def operation_time(self):
        """The operation time returned by the last operation executed
        in this session.
        """
        return self._operation_time

    def _inherit_option(self, name, val):
        """Return the inherited TransactionOption value."""
        if val:
            return val
        txn_opts = self.options.default_transaction_options
        val = txn_opts and getattr(txn_opts, name)
        if val:
            return val
        return getattr(self.client, name)

    def with_transaction--- This code section failed: ---

 L. 501         0  LOAD_GLOBAL              monotonic
                2  LOAD_METHOD              time
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'start_time'
              8_0  COME_FROM           248  '248'
              8_1  COME_FROM           222  '222'
              8_2  COME_FROM           102  '102'

 L. 503         8  LOAD_FAST                'self'
               10  LOAD_METHOD              start_transaction

 L. 504        12  LOAD_FAST                'read_concern'

 L. 504        14  LOAD_FAST                'write_concern'

 L. 504        16  LOAD_FAST                'read_preference'

 L. 505        18  LOAD_FAST                'max_commit_time_ms'

 L. 503        20  CALL_METHOD_4         4  ''
               22  POP_TOP          

 L. 506        24  SETUP_FINALLY        38  'to 38'

 L. 507        26  LOAD_FAST                'callback'
               28  LOAD_FAST                'self'
               30  CALL_FUNCTION_1       1  ''
               32  STORE_FAST               'ret'
               34  POP_BLOCK        
               36  JUMP_FORWARD        124  'to 124'
             38_0  COME_FROM_FINALLY    24  '24'

 L. 508        38  DUP_TOP          
               40  LOAD_GLOBAL              Exception
               42  COMPARE_OP               exception-match
               44  POP_JUMP_IF_FALSE   122  'to 122'
               46  POP_TOP          
               48  STORE_FAST               'exc'
               50  POP_TOP          
               52  SETUP_FINALLY       110  'to 110'

 L. 509        54  LOAD_FAST                'self'
               56  LOAD_ATTR                in_transaction
               58  POP_JUMP_IF_FALSE    68  'to 68'

 L. 510        60  LOAD_FAST                'self'
               62  LOAD_METHOD              abort_transaction
               64  CALL_METHOD_0         0  ''
               66  POP_TOP          
             68_0  COME_FROM            58  '58'

 L. 511        68  LOAD_GLOBAL              isinstance
               70  LOAD_FAST                'exc'
               72  LOAD_GLOBAL              PyMongoError
               74  CALL_FUNCTION_2       2  ''
               76  POP_JUMP_IF_FALSE   104  'to 104'

 L. 512        78  LOAD_FAST                'exc'
               80  LOAD_METHOD              has_error_label
               82  LOAD_STR                 'TransientTransactionError'
               84  CALL_METHOD_1         1  ''

 L. 511        86  POP_JUMP_IF_FALSE   104  'to 104'

 L. 513        88  LOAD_GLOBAL              _within_time_limit
               90  LOAD_FAST                'start_time'
               92  CALL_FUNCTION_1       1  ''

 L. 511        94  POP_JUMP_IF_FALSE   104  'to 104'

 L. 515        96  POP_BLOCK        
               98  POP_EXCEPT       
              100  CALL_FINALLY        110  'to 110'
              102  JUMP_BACK             8  'to 8'
            104_0  COME_FROM            94  '94'
            104_1  COME_FROM            86  '86'
            104_2  COME_FROM            76  '76'

 L. 516       104  RAISE_VARARGS_0       0  'reraise'
              106  POP_BLOCK        
              108  BEGIN_FINALLY    
            110_0  COME_FROM           100  '100'
            110_1  COME_FROM_FINALLY    52  '52'
              110  LOAD_CONST               None
              112  STORE_FAST               'exc'
              114  DELETE_FAST              'exc'
              116  END_FINALLY      
              118  POP_EXCEPT       
              120  JUMP_FORWARD        124  'to 124'
            122_0  COME_FROM            44  '44'
              122  END_FINALLY      
            124_0  COME_FROM           120  '120'
            124_1  COME_FROM            36  '36'

 L. 518       124  LOAD_FAST                'self'
              126  LOAD_ATTR                in_transaction
              128  POP_JUMP_IF_TRUE    134  'to 134'

 L. 520       130  LOAD_FAST                'ret'
              132  RETURN_VALUE     
            134_0  COME_FROM           196  '196'
            134_1  COME_FROM           128  '128'

 L. 523       134  SETUP_FINALLY       148  'to 148'

 L. 524       136  LOAD_FAST                'self'
              138  LOAD_METHOD              commit_transaction
              140  CALL_METHOD_0         0  ''
              142  POP_TOP          
              144  POP_BLOCK        
              146  JUMP_FORWARD        244  'to 244'
            148_0  COME_FROM_FINALLY   134  '134'

 L. 525       148  DUP_TOP          
              150  LOAD_GLOBAL              PyMongoError
              152  COMPARE_OP               exception-match
              154  POP_JUMP_IF_FALSE   242  'to 242'
              156  POP_TOP          
              158  STORE_FAST               'exc'
              160  POP_TOP          
              162  SETUP_FINALLY       230  'to 230'

 L. 526       164  LOAD_FAST                'exc'
              166  LOAD_METHOD              has_error_label
              168  LOAD_STR                 'UnknownTransactionCommitResult'
              170  CALL_METHOD_1         1  ''
              172  POP_JUMP_IF_FALSE   198  'to 198'

 L. 527       174  LOAD_GLOBAL              _within_time_limit
              176  LOAD_FAST                'start_time'
              178  CALL_FUNCTION_1       1  ''

 L. 526       180  POP_JUMP_IF_FALSE   198  'to 198'

 L. 528       182  LOAD_GLOBAL              _max_time_expired_error
              184  LOAD_FAST                'exc'
              186  CALL_FUNCTION_1       1  ''

 L. 526       188  POP_JUMP_IF_TRUE    198  'to 198'

 L. 530       190  POP_BLOCK        
              192  POP_EXCEPT       
              194  CALL_FINALLY        230  'to 230'
              196  JUMP_BACK           134  'to 134'
            198_0  COME_FROM           188  '188'
            198_1  COME_FROM           180  '180'
            198_2  COME_FROM           172  '172'

 L. 532       198  LOAD_FAST                'exc'
              200  LOAD_METHOD              has_error_label
              202  LOAD_STR                 'TransientTransactionError'
              204  CALL_METHOD_1         1  ''
              206  POP_JUMP_IF_FALSE   224  'to 224'

 L. 533       208  LOAD_GLOBAL              _within_time_limit
              210  LOAD_FAST                'start_time'
              212  CALL_FUNCTION_1       1  ''

 L. 532       214  POP_JUMP_IF_FALSE   224  'to 224'

 L. 535       216  POP_BLOCK        
              218  POP_EXCEPT       
              220  CALL_FINALLY        230  'to 230'
              222  JUMP_BACK             8  'to 8'
            224_0  COME_FROM           214  '214'
            224_1  COME_FROM           206  '206'

 L. 536       224  RAISE_VARARGS_0       0  'reraise'
              226  POP_BLOCK        
              228  BEGIN_FINALLY    
            230_0  COME_FROM           220  '220'
            230_1  COME_FROM           194  '194'
            230_2  COME_FROM_FINALLY   162  '162'
              230  LOAD_CONST               None
              232  STORE_FAST               'exc'
              234  DELETE_FAST              'exc'
              236  END_FINALLY      
              238  POP_EXCEPT       
              240  JUMP_FORWARD        244  'to 244'
            242_0  COME_FROM           154  '154'
              242  END_FINALLY      
            244_0  COME_FROM           240  '240'
            244_1  COME_FROM           146  '146'

 L. 539       244  LOAD_FAST                'ret'
              246  RETURN_VALUE     
              248  JUMP_BACK             8  'to 8'

Parse error at or near `POP_EXCEPT' instruction at offset 98

    def start_transaction(self, read_concern=None, write_concern=None, read_preference=None, max_commit_time_ms=None):
        """Start a multi-statement transaction.

        Takes the same arguments as :class:`TransactionOptions`.

        .. versionchanged:: 3.9
           Added the ``max_commit_time_ms`` option.

        .. versionadded:: 3.7
        """
        self._check_ended()
        if self.in_transaction:
            raise InvalidOperation('Transaction already in progress')
        read_concern = self._inherit_option('read_concern', read_concern)
        write_concern = self._inherit_option('write_concern', write_concern)
        read_preference = self._inherit_option('read_preference', read_preference)
        if max_commit_time_ms is None:
            opts = self.options.default_transaction_options
            if opts:
                max_commit_time_ms = opts.max_commit_time_ms
        self._transaction.opts = TransactionOptions(read_concern, write_concern, read_preference, max_commit_time_ms)
        self._transaction.reset()
        self._transaction.state = _TxnState.STARTING
        self._start_retryable_write()
        return _TransactionContext(self)

    def commit_transaction(self):
        """Commit a multi-statement transaction.

        .. versionadded:: 3.7
        """
        self._check_ended()
        retry = False
        state = self._transaction.state
        if state is _TxnState.NONE:
            raise InvalidOperation('No transaction started')
        else:
            if state in (_TxnState.STARTING, _TxnState.COMMITTED_EMPTY):
                self._transaction.state = _TxnState.COMMITTED_EMPTY
                return
            if state is _TxnState.ABORTED:
                raise InvalidOperation('Cannot call commitTransaction after calling abortTransaction')
            elif state is _TxnState.COMMITTED:
                self._transaction.state = _TxnState.IN_PROGRESS
                retry = True
        try:
            try:
                self._finish_transaction_with_retry('commitTransaction', retry)
            except ConnectionFailure as exc:
                try:
                    exc._remove_error_label('TransientTransactionError')
                    _reraise_with_unknown_commit(exc)
                finally:
                    exc = None
                    del exc

            except WTimeoutError as exc:
                try:
                    _reraise_with_unknown_commit(exc)
                finally:
                    exc = None
                    del exc

            except OperationFailure as exc:
                try:
                    if exc.code not in _UNKNOWN_COMMIT_ERROR_CODES:
                        raise
                    _reraise_with_unknown_commit(exc)
                finally:
                    exc = None
                    del exc

        finally:
            self._transaction.state = _TxnState.COMMITTED

    def abort_transaction(self):
        """Abort a multi-statement transaction.

        .. versionadded:: 3.7
        """
        self._check_ended()
        state = self._transaction.state
        if state is _TxnState.NONE:
            raise InvalidOperation('No transaction started')
        else:
            if state is _TxnState.STARTING:
                self._transaction.state = _TxnState.ABORTED
                return
            if state is _TxnState.ABORTED:
                raise InvalidOperation('Cannot call abortTransaction twice')
            elif state in (_TxnState.COMMITTED, _TxnState.COMMITTED_EMPTY):
                raise InvalidOperation('Cannot call abortTransaction after calling commitTransaction')
        try:
            try:
                self._finish_transaction_with_retry('abortTransaction', False)
            except (OperationFailure, ConnectionFailure):
                pass

        finally:
            self._transaction.state = _TxnState.ABORTED

    def _finish_transaction_with_retry--- This code section failed: ---

 L. 656         0  SETUP_FINALLY        16  'to 16'

 L. 657         2  LOAD_FAST                'self'
                4  LOAD_METHOD              _finish_transaction
                6  LOAD_FAST                'command_name'
                8  LOAD_FAST                'explict_retry'
               10  CALL_METHOD_2         2  ''
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L. 658        16  DUP_TOP          
               18  LOAD_GLOBAL              ServerSelectionTimeoutError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    36  'to 36'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 659        30  RAISE_VARARGS_0       0  'reraise'
               32  POP_EXCEPT       
               34  JUMP_FORWARD        210  'to 210'
             36_0  COME_FROM            22  '22'

 L. 660        36  DUP_TOP          
               38  LOAD_GLOBAL              ConnectionFailure
               40  COMPARE_OP               exception-match
               42  POP_JUMP_IF_FALSE   116  'to 116'
               44  POP_TOP          
               46  STORE_FAST               'exc'
               48  POP_TOP          
               50  SETUP_FINALLY       104  'to 104'

 L. 661        52  SETUP_FINALLY        76  'to 76'

 L. 662        54  LOAD_FAST                'self'
               56  LOAD_METHOD              _finish_transaction
               58  LOAD_FAST                'command_name'
               60  LOAD_CONST               True
               62  CALL_METHOD_2         2  ''
               64  POP_BLOCK        
               66  ROT_FOUR         
               68  POP_BLOCK        
               70  POP_EXCEPT       
               72  CALL_FINALLY        104  'to 104'
               74  RETURN_VALUE     
             76_0  COME_FROM_FINALLY    52  '52'

 L. 663        76  DUP_TOP          
               78  LOAD_GLOBAL              ServerSelectionTimeoutError
               80  COMPARE_OP               exception-match
               82  POP_JUMP_IF_FALSE    98  'to 98'
               84  POP_TOP          
               86  POP_TOP          
               88  POP_TOP          

 L. 666        90  LOAD_FAST                'exc'
               92  RAISE_VARARGS_1       1  'exception instance'
               94  POP_EXCEPT       
               96  JUMP_FORWARD        100  'to 100'
             98_0  COME_FROM            82  '82'
               98  END_FINALLY      
            100_0  COME_FROM            96  '96'
              100  POP_BLOCK        
              102  BEGIN_FINALLY    
            104_0  COME_FROM            72  '72'
            104_1  COME_FROM_FINALLY    50  '50'
              104  LOAD_CONST               None
              106  STORE_FAST               'exc'
              108  DELETE_FAST              'exc'
              110  END_FINALLY      
              112  POP_EXCEPT       
              114  JUMP_FORWARD        210  'to 210'
            116_0  COME_FROM            42  '42'

 L. 667       116  DUP_TOP          
              118  LOAD_GLOBAL              OperationFailure
              120  COMPARE_OP               exception-match
              122  POP_JUMP_IF_FALSE   208  'to 208'
              124  POP_TOP          
              126  STORE_FAST               'exc'
              128  POP_TOP          
              130  SETUP_FINALLY       196  'to 196'

 L. 668       132  LOAD_FAST                'exc'
              134  LOAD_ATTR                code
              136  LOAD_GLOBAL              _RETRYABLE_ERROR_CODES
              138  COMPARE_OP               not-in
              140  POP_JUMP_IF_FALSE   144  'to 144'

 L. 669       142  RAISE_VARARGS_0       0  'reraise'
            144_0  COME_FROM           140  '140'

 L. 670       144  SETUP_FINALLY       168  'to 168'

 L. 671       146  LOAD_FAST                'self'
              148  LOAD_METHOD              _finish_transaction
              150  LOAD_FAST                'command_name'
              152  LOAD_CONST               True
              154  CALL_METHOD_2         2  ''
              156  POP_BLOCK        
              158  ROT_FOUR         
              160  POP_BLOCK        
              162  POP_EXCEPT       
              164  CALL_FINALLY        196  'to 196'
              166  RETURN_VALUE     
            168_0  COME_FROM_FINALLY   144  '144'

 L. 672       168  DUP_TOP          
              170  LOAD_GLOBAL              ServerSelectionTimeoutError
              172  COMPARE_OP               exception-match
              174  POP_JUMP_IF_FALSE   190  'to 190'
              176  POP_TOP          
              178  POP_TOP          
              180  POP_TOP          

 L. 675       182  LOAD_FAST                'exc'
              184  RAISE_VARARGS_1       1  'exception instance'
              186  POP_EXCEPT       
              188  JUMP_FORWARD        192  'to 192'
            190_0  COME_FROM           174  '174'
              190  END_FINALLY      
            192_0  COME_FROM           188  '188'
              192  POP_BLOCK        
              194  BEGIN_FINALLY    
            196_0  COME_FROM           164  '164'
            196_1  COME_FROM_FINALLY   130  '130'
              196  LOAD_CONST               None
              198  STORE_FAST               'exc'
              200  DELETE_FAST              'exc'
              202  END_FINALLY      
              204  POP_EXCEPT       
              206  JUMP_FORWARD        210  'to 210'
            208_0  COME_FROM           122  '122'
              208  END_FINALLY      
            210_0  COME_FROM           206  '206'
            210_1  COME_FROM           114  '114'
            210_2  COME_FROM            34  '34'

Parse error at or near `DUP_TOP' instruction at offset 36

    def _finish_transaction(self, command_name, retrying):
        opts = self._transaction.opts
        wc = opts.write_concern
        cmd = SON([(command_name, 1)])
        if command_name == 'commitTransaction':
            if opts.max_commit_time_ms:
                cmd['maxTimeMS'] = opts.max_commit_time_ms
            if retrying:
                wc_doc = wc.document
                wc_doc['w'] = 'majority'
                wc_doc.setdefault('wtimeout', 10000)
                wc = WriteConcern(**wc_doc)
        if self._transaction.recovery_token:
            cmd['recoveryToken'] = self._transaction.recovery_token
        with self._client._socket_for_writes(self) as sock_info:
            return self._client.admin._command(sock_info,
              cmd,
              session=self,
              write_concern=wc,
              parse_write_concern_error=True)

    def _advance_cluster_time(self, cluster_time):
        """Internal cluster time helper."""
        if self._cluster_time is None:
            self._cluster_time = cluster_time
        elif cluster_time is not None:
            if cluster_time['clusterTime'] > self._cluster_time['clusterTime']:
                self._cluster_time = cluster_time

    def advance_cluster_time(self, cluster_time):
        """Update the cluster time for this session.

        :Parameters:
          - `cluster_time`: The
            :data:`~pymongo.client_session.ClientSession.cluster_time` from
            another `ClientSession` instance.
        """
        if not isinstance(cluster_time, abc.Mapping):
            raise TypeError('cluster_time must be a subclass of collections.Mapping')
        if not isinstance(cluster_time.get('clusterTime'), Timestamp):
            raise ValueError('Invalid cluster_time')
        self._advance_cluster_time(cluster_time)

    def _advance_operation_time(self, operation_time):
        """Internal operation time helper."""
        if self._operation_time is None:
            self._operation_time = operation_time
        elif operation_time is not None:
            if operation_time > self._operation_time:
                self._operation_time = operation_time

    def advance_operation_time(self, operation_time):
        """Update the operation time for this session.

        :Parameters:
          - `operation_time`: The
            :data:`~pymongo.client_session.ClientSession.operation_time` from
            another `ClientSession` instance.
        """
        if not isinstance(operation_time, Timestamp):
            raise TypeError('operation_time must be an instance of bson.timestamp.Timestamp')
        self._advance_operation_time(operation_time)

    def _process_response(self, reply):
        """Process a response to a command that was run with this session."""
        self._advance_cluster_time(reply.get('$clusterTime'))
        self._advance_operation_time(reply.get('operationTime'))
        if self.in_transaction:
            if self._transaction.sharded:
                recovery_token = reply.get('recoveryToken')
                if recovery_token:
                    self._transaction.recovery_token = recovery_token

    @property
    def has_ended(self):
        """True if this session is finished."""
        return self._server_session is None

    @property
    def in_transaction(self):
        """True if this session has an active multi-statement transaction.

        .. versionadded:: 3.10
        """
        return self._transaction.active()

    @property
    def _pinned_address(self):
        """The mongos address this transaction was created on."""
        if self._transaction.active():
            return self._transaction.pinned_address

    def _pin_mongos(self, server):
        """Pin this session to the given mongos Server."""
        self._transaction.sharded = True
        self._transaction.pinned_address = server.description.address

    def _unpin_mongos(self):
        """Unpin this session from any pinned mongos address."""
        self._transaction.pinned_address = None

    def _txn_read_preference(self):
        """Return read preference of this transaction or None."""
        if self.in_transaction:
            return self._transaction.opts.read_preference

    def _apply_to(self, command, is_retryable, read_preference):
        self._check_ended()
        self._server_session.last_use = monotonic.time()
        command['lsid'] = self._server_session.session_id
        if not self.in_transaction:
            self._transaction.reset()
        if is_retryable:
            command['txnNumber'] = self._server_session.transaction_id
            return
        if self.in_transaction:
            if read_preference != ReadPreference.PRIMARY:
                raise InvalidOperation('read preference in a transaction must be primary, not: %r' % (
                 read_preference,))
            if self._transaction.state == _TxnState.STARTING:
                self._transaction.state = _TxnState.IN_PROGRESS
                command['startTransaction'] = True
                if self._transaction.opts.read_concern:
                    rc = self._transaction.opts.read_concern.document
                else:
                    rc = {}
                if self.options.causal_consistency:
                    if self.operation_time is not None:
                        rc['afterClusterTime'] = self.operation_time
                if rc:
                    command['readConcern'] = rc
            command['txnNumber'] = self._server_session.transaction_id
            command['autocommit'] = False

    def _start_retryable_write(self):
        self._check_ended()
        self._server_session.inc_transaction_id()


class _ServerSession(object):

    def __init__(self, pool_id):
        self.session_id = {'id': Binary(uuid.uuid4().bytes, 4)}
        self.last_use = monotonic.time()
        self._transaction_id = 0
        self.dirty = False
        self.pool_id = pool_id

    def mark_dirty(self):
        """Mark this session as dirty.

        A server session is marked dirty when a command fails with a network
        error. Dirty sessions are later discarded from the server session pool.
        """
        self.dirty = True

    def timed_out(self, session_timeout_minutes):
        idle_seconds = monotonic.time() - self.last_use
        return idle_seconds > (session_timeout_minutes - 1) * 60

    @property
    def transaction_id(self):
        """Positive 64-bit integer."""
        return Int64(self._transaction_id)

    def inc_transaction_id(self):
        self._transaction_id += 1


class _ServerSessionPool(collections.deque):
    __doc__ = 'Pool of _ServerSession objects.\n\n    This class is not thread-safe, access it while holding the Topology lock.\n    '

    def __init__(self, *args, **kwargs):
        (super(_ServerSessionPool, self).__init__)(*args, **kwargs)
        self.pool_id = 0

    def reset(self):
        self.pool_id += 1
        self.clear()

    def pop_all(self):
        ids = []
        while True:
            if self:
                ids.append(self.pop().session_id)

        return ids

    def get_server_session(self, session_timeout_minutes):
        self._clear_stale(session_timeout_minutes)
        while True:
            if self:
                s = self.popleft()
                if not s.timed_out(session_timeout_minutes):
                    return s

        return _ServerSession(self.pool_id)

    def return_server_session(self, server_session, session_timeout_minutes):
        self._clear_stale(session_timeout_minutes)
        if not server_session.timed_out(session_timeout_minutes):
            self.return_server_session_no_lock(server_session)

    def return_server_session_no_lock(self, server_session):
        if server_session.pool_id == self.pool_id:
            if not server_session.dirty:
                self.appendleft(server_session)

    def _clear_stale--- This code section failed: ---
              0_0  COME_FROM            30  '30'
              0_1  COME_FROM            26  '26'

 L. 917         0  LOAD_FAST                'self'
                2  POP_JUMP_IF_FALSE    32  'to 32'

 L. 918         4  LOAD_FAST                'self'
                6  LOAD_CONST               -1
                8  BINARY_SUBSCR    
               10  LOAD_METHOD              timed_out
               12  LOAD_FAST                'session_timeout_minutes'
               14  CALL_METHOD_1         1  ''
               16  POP_JUMP_IF_FALSE    32  'to 32'

 L. 919        18  LOAD_FAST                'self'
               20  LOAD_METHOD              pop
               22  CALL_METHOD_0         0  ''
               24  POP_TOP          
               26  JUMP_BACK             0  'to 0'

 L. 922        28  JUMP_FORWARD         32  'to 32'
               30  JUMP_BACK             0  'to 0'
             32_0  COME_FROM            28  '28'
             32_1  COME_FROM            16  '16'
             32_2  COME_FROM             2  '2'

Parse error at or near `JUMP_FORWARD' instruction at offset 28