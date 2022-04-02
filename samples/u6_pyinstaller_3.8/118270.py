# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pymongo\database.py
"""Database level operations."""
import warnings
from bson.code import Code
from bson.codec_options import DEFAULT_CODEC_OPTIONS
from bson.dbref import DBRef
from bson.py3compat import iteritems, string_type, _unicode
from bson.son import SON
from pymongo import auth, common
from pymongo.aggregation import _DatabaseAggregationCommand
from pymongo.change_stream import DatabaseChangeStream
from pymongo.collection import Collection
from pymongo.command_cursor import CommandCursor
from pymongo.errors import CollectionInvalid, ConfigurationError, InvalidName, OperationFailure
from pymongo.message import _first_batch
from pymongo.read_preferences import ReadPreference
from pymongo.son_manipulator import SONManipulator
from pymongo.write_concern import DEFAULT_WRITE_CONCERN
_INDEX_REGEX = {'name': {'$regex': '^(?!.*\\$)'}}
_SYSTEM_FILTER = {'filter': {'name': {'$regex': '^(?!system\\.)'}}}

def _check_name(name):
    """Check if a database name is valid.
    """
    if not name:
        raise InvalidName('database name cannot be the empty string')
    for invalid_char in (' ', '.', '$', '/', '\\', '\x00', '"'):
        if invalid_char in name:
            raise InvalidName('database names cannot contain the character %r' % invalid_char)


class Database(common.BaseObject):
    __doc__ = 'A Mongo database.\n    '

    def __init__(self, client, name, codec_options=None, read_preference=None, write_concern=None, read_concern=None):
        """Get a database by client and name.

        Raises :class:`TypeError` if `name` is not an instance of
        :class:`basestring` (:class:`str` in python 3). Raises
        :class:`~pymongo.errors.InvalidName` if `name` is not a valid
        database name.

        :Parameters:
          - `client`: A :class:`~pymongo.mongo_client.MongoClient` instance.
          - `name`: The database name.
          - `codec_options` (optional): An instance of
            :class:`~bson.codec_options.CodecOptions`. If ``None`` (the
            default) client.codec_options is used.
          - `read_preference` (optional): The read preference to use. If
            ``None`` (the default) client.read_preference is used.
          - `write_concern` (optional): An instance of
            :class:`~pymongo.write_concern.WriteConcern`. If ``None`` (the
            default) client.write_concern is used.
          - `read_concern` (optional): An instance of
            :class:`~pymongo.read_concern.ReadConcern`. If ``None`` (the
            default) client.read_concern is used.

        .. mongodoc:: databases

        .. versionchanged:: 3.2
           Added the read_concern option.

        .. versionchanged:: 3.0
           Added the codec_options, read_preference, and write_concern options.
           :class:`~pymongo.database.Database` no longer returns an instance
           of :class:`~pymongo.collection.Collection` for attribute names
           with leading underscores. You must use dict-style lookups instead::

               db['__my_collection__']

           Not:

               db.__my_collection__
        """
        super(Database, self).__init__(codec_options or client.codec_options, read_preference or client.read_preference, write_concern or client.write_concern, read_concern or client.read_concern)
        if not isinstance(name, string_type):
            raise TypeError('name must be an instance of %s' % (
             string_type.__name__,))
        if name != '$external':
            _check_name(name)
        self._Database__name = _unicode(name)
        self._Database__client = client
        self._Database__incoming_manipulators = []
        self._Database__incoming_copying_manipulators = []
        self._Database__outgoing_manipulators = []
        self._Database__outgoing_copying_manipulators = []

    def add_son_manipulator(self, manipulator):
        """Add a new son manipulator to this database.

        **DEPRECATED** - `add_son_manipulator` is deprecated.

        .. versionchanged:: 3.0
          Deprecated add_son_manipulator.
        """
        warnings.warn('add_son_manipulator is deprecated', DeprecationWarning,
          stacklevel=2)
        base = SONManipulator()

        def method_overwritten(instance, method):
            return getattr(instance, method).__func__ != getattr(base, method).__func__

        if manipulator.will_copy():
            if method_overwritten(manipulator, 'transform_incoming'):
                self._Database__incoming_copying_manipulators.insert(0, manipulator)
            if method_overwritten(manipulator, 'transform_outgoing'):
                self._Database__outgoing_copying_manipulators.insert(0, manipulator)
        else:
            if method_overwritten(manipulator, 'transform_incoming'):
                self._Database__incoming_manipulators.insert(0, manipulator)
            if method_overwritten(manipulator, 'transform_outgoing'):
                self._Database__outgoing_manipulators.insert(0, manipulator)

    @property
    def system_js(self):
        """**DEPRECATED**: :class:`SystemJS` helper for this :class:`Database`.

        See the documentation for :class:`SystemJS` for more details.
        """
        return SystemJS(self)

    @property
    def client(self):
        """The client instance for this :class:`Database`."""
        return self._Database__client

    @property
    def name(self):
        """The name of this :class:`Database`."""
        return self._Database__name

    @property
    def incoming_manipulators(self):
        """**DEPRECATED**: All incoming SON manipulators.

        .. versionchanged:: 3.5
          Deprecated.

        .. versionadded:: 2.0
        """
        warnings.warn('Database.incoming_manipulators() is deprecated', DeprecationWarning,
          stacklevel=2)
        return [manipulator.__class__.__name__ for manipulator in self._Database__incoming_manipulators]

    @property
    def incoming_copying_manipulators(self):
        """**DEPRECATED**: All incoming SON copying manipulators.

        .. versionchanged:: 3.5
          Deprecated.

        .. versionadded:: 2.0
        """
        warnings.warn('Database.incoming_copying_manipulators() is deprecated', DeprecationWarning,
          stacklevel=2)
        return [manipulator.__class__.__name__ for manipulator in self._Database__incoming_copying_manipulators]

    @property
    def outgoing_manipulators(self):
        """**DEPRECATED**: All outgoing SON manipulators.

        .. versionchanged:: 3.5
          Deprecated.

        .. versionadded:: 2.0
        """
        warnings.warn('Database.outgoing_manipulators() is deprecated', DeprecationWarning,
          stacklevel=2)
        return [manipulator.__class__.__name__ for manipulator in self._Database__outgoing_manipulators]

    @property
    def outgoing_copying_manipulators(self):
        """**DEPRECATED**: All outgoing SON copying manipulators.

        .. versionchanged:: 3.5
          Deprecated.

        .. versionadded:: 2.0
        """
        warnings.warn('Database.outgoing_copying_manipulators() is deprecated', DeprecationWarning,
          stacklevel=2)
        return [manipulator.__class__.__name__ for manipulator in self._Database__outgoing_copying_manipulators]

    def with_options(self, codec_options=None, read_preference=None, write_concern=None, read_concern=None):
        """Get a clone of this database changing the specified settings.

          >>> db1.read_preference
          Primary()
          >>> from pymongo import ReadPreference
          >>> db2 = db1.with_options(read_preference=ReadPreference.SECONDARY)
          >>> db1.read_preference
          Primary()
          >>> db2.read_preference
          Secondary(tag_sets=None)

        :Parameters:
          - `codec_options` (optional): An instance of
            :class:`~bson.codec_options.CodecOptions`. If ``None`` (the
            default) the :attr:`codec_options` of this :class:`Collection`
            is used.
          - `read_preference` (optional): The read preference to use. If
            ``None`` (the default) the :attr:`read_preference` of this
            :class:`Collection` is used. See :mod:`~pymongo.read_preferences`
            for options.
          - `write_concern` (optional): An instance of
            :class:`~pymongo.write_concern.WriteConcern`. If ``None`` (the
            default) the :attr:`write_concern` of this :class:`Collection`
            is used.
          - `read_concern` (optional): An instance of
            :class:`~pymongo.read_concern.ReadConcern`. If ``None`` (the
            default) the :attr:`read_concern` of this :class:`Collection`
            is used.

        .. versionadded:: 3.8
        """
        return Database(self.client, self._Database__name, codec_options or self.codec_options, read_preference or self.read_preference, write_concern or self.write_concern, read_concern or self.read_concern)

    def __eq__(self, other):
        if isinstance(other, Database):
            return self._Database__client == other.client and self._Database__name == other.name
        return NotImplemented

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return 'Database(%r, %r)' % (self._Database__client, self._Database__name)

    def __getattr__(self, name):
        """Get a collection of this database by name.

        Raises InvalidName if an invalid collection name is used.

        :Parameters:
          - `name`: the name of the collection to get
        """
        if name.startswith('_'):
            raise AttributeError('Database has no attribute %r. To access the %s collection, use database[%r].' % (
             name, name, name))
        return self.__getitem__(name)

    def __getitem__(self, name):
        """Get a collection of this database by name.

        Raises InvalidName if an invalid collection name is used.

        :Parameters:
          - `name`: the name of the collection to get
        """
        return Collection(self, name)

    def get_collection(self, name, codec_options=None, read_preference=None, write_concern=None, read_concern=None):
        """Get a :class:`~pymongo.collection.Collection` with the given name
        and options.

        Useful for creating a :class:`~pymongo.collection.Collection` with
        different codec options, read preference, and/or write concern from
        this :class:`Database`.

          >>> db.read_preference
          Primary()
          >>> coll1 = db.test
          >>> coll1.read_preference
          Primary()
          >>> from pymongo import ReadPreference
          >>> coll2 = db.get_collection(
          ...     'test', read_preference=ReadPreference.SECONDARY)
          >>> coll2.read_preference
          Secondary(tag_sets=None)

        :Parameters:
          - `name`: The name of the collection - a string.
          - `codec_options` (optional): An instance of
            :class:`~bson.codec_options.CodecOptions`. If ``None`` (the
            default) the :attr:`codec_options` of this :class:`Database` is
            used.
          - `read_preference` (optional): The read preference to use. If
            ``None`` (the default) the :attr:`read_preference` of this
            :class:`Database` is used. See :mod:`~pymongo.read_preferences`
            for options.
          - `write_concern` (optional): An instance of
            :class:`~pymongo.write_concern.WriteConcern`. If ``None`` (the
            default) the :attr:`write_concern` of this :class:`Database` is
            used.
          - `read_concern` (optional): An instance of
            :class:`~pymongo.read_concern.ReadConcern`. If ``None`` (the
            default) the :attr:`read_concern` of this :class:`Database` is
            used.
        """
        return Collection(self, name, False, codec_options, read_preference, write_concern, read_concern)

    def create_collection--- This code section failed: ---

 L. 404         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _Database__client
                4  LOAD_METHOD              _tmp_session
                6  LOAD_FAST                'session'
                8  CALL_METHOD_1         1  ''
               10  SETUP_WITH           92  'to 92'
               12  STORE_FAST               's'

 L. 405        14  LOAD_FAST                'name'
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                list_collection_names

 L. 406        20  LOAD_STR                 'name'
               22  LOAD_FAST                'name'
               24  BUILD_MAP_1           1 

 L. 406        26  LOAD_FAST                's'

 L. 405        28  LOAD_CONST               ('filter', 'session')
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  COMPARE_OP               in
               34  POP_JUMP_IF_FALSE    48  'to 48'

 L. 407        36  LOAD_GLOBAL              CollectionInvalid
               38  LOAD_STR                 'collection %s already exists'
               40  LOAD_FAST                'name'
               42  BINARY_MODULO    
               44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            34  '34'

 L. 409        48  LOAD_GLOBAL              Collection
               50  LOAD_FAST                'self'
               52  LOAD_FAST                'name'
               54  LOAD_CONST               True
               56  LOAD_FAST                'codec_options'

 L. 410        58  LOAD_FAST                'read_preference'

 L. 410        60  LOAD_FAST                'write_concern'

 L. 411        62  LOAD_FAST                'read_concern'

 L. 409        64  BUILD_TUPLE_7         7 
               66  LOAD_STR                 'session'

 L. 411        68  LOAD_FAST                's'

 L. 409        70  BUILD_MAP_1           1 

 L. 411        72  LOAD_FAST                'kwargs'

 L. 409        74  BUILD_MAP_UNPACK_WITH_CALL_2     2 
               76  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               78  POP_BLOCK        
               80  ROT_TWO          
               82  BEGIN_FINALLY    
               84  WITH_CLEANUP_START
               86  WITH_CLEANUP_FINISH
               88  POP_FINALLY           0  ''
               90  RETURN_VALUE     
             92_0  COME_FROM_WITH       10  '10'
               92  WITH_CLEANUP_START
               94  WITH_CLEANUP_FINISH
               96  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 80

    def _apply_incoming_manipulators(self, son, collection):
        """Apply incoming manipulators to `son`."""
        for manipulator in self._Database__incoming_manipulators:
            son = manipulator.transform_incoming(son, collection)
        else:
            return son

    def _apply_incoming_copying_manipulators(self, son, collection):
        """Apply incoming copying manipulators to `son`."""
        for manipulator in self._Database__incoming_copying_manipulators:
            son = manipulator.transform_incoming(son, collection)
        else:
            return son

    def _fix_incoming(self, son, collection):
        """Apply manipulators to an incoming SON object before it gets stored.

        :Parameters:
          - `son`: the son object going into the database
          - `collection`: the collection the son object is being saved in
        """
        son = self._apply_incoming_manipulators(son, collection)
        son = self._apply_incoming_copying_manipulators(son, collection)
        return son

    def _fix_outgoing(self, son, collection):
        """Apply manipulators to a SON object as it comes out of the database.

        :Parameters:
          - `son`: the son object coming out of the database
          - `collection`: the collection the son object was saved in
        """
        for manipulator in reversed(self._Database__outgoing_manipulators):
            son = manipulator.transform_outgoing(son, collection)
        else:
            for manipulator in reversed(self._Database__outgoing_copying_manipulators):
                son = manipulator.transform_outgoing(son, collection)
            else:
                return son

    def aggregate--- This code section failed: ---

 L. 508         0  LOAD_FAST                'self'
                2  LOAD_ATTR                client
                4  LOAD_ATTR                _tmp_session
                6  LOAD_FAST                'session'
                8  LOAD_CONST               False
               10  LOAD_CONST               ('close',)
               12  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               14  SETUP_WITH           94  'to 94'
               16  STORE_FAST               's'

 L. 509        18  LOAD_GLOBAL              _DatabaseAggregationCommand

 L. 510        20  LOAD_FAST                'self'

 L. 510        22  LOAD_GLOBAL              CommandCursor

 L. 510        24  LOAD_FAST                'pipeline'

 L. 510        26  LOAD_FAST                'kwargs'

 L. 510        28  LOAD_FAST                'session'
               30  LOAD_CONST               None
               32  COMPARE_OP               is-not

 L. 511        34  LOAD_STR                 'cursor'
               36  LOAD_STR                 'firstBatch'
               38  LOAD_CONST               1
               40  BUILD_MAP_1           1 
               42  BUILD_MAP_1           1 

 L. 509        44  LOAD_CONST               ('user_fields',)
               46  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
               48  STORE_FAST               'cmd'

 L. 512        50  LOAD_FAST                'self'
               52  LOAD_ATTR                client
               54  LOAD_ATTR                _retryable_read

 L. 513        56  LOAD_FAST                'cmd'
               58  LOAD_ATTR                get_cursor

 L. 513        60  LOAD_FAST                'cmd'
               62  LOAD_METHOD              get_read_preference
               64  LOAD_FAST                's'
               66  CALL_METHOD_1         1  ''

 L. 513        68  LOAD_FAST                's'

 L. 514        70  LOAD_FAST                'cmd'
               72  LOAD_ATTR                _performs_write
               74  UNARY_NOT        

 L. 512        76  LOAD_CONST               ('retryable',)
               78  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               80  POP_BLOCK        
               82  ROT_TWO          
               84  BEGIN_FINALLY    
               86  WITH_CLEANUP_START
               88  WITH_CLEANUP_FINISH
               90  POP_FINALLY           0  ''
               92  RETURN_VALUE     
             94_0  COME_FROM_WITH       14  '14'
               94  WITH_CLEANUP_START
               96  WITH_CLEANUP_FINISH
               98  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 82

    def watch(self, pipeline=None, full_document=None, resume_after=None, max_await_time_ms=None, batch_size=None, collation=None, start_at_operation_time=None, session=None, start_after=None):
        """Watch changes on this database.

        Performs an aggregation with an implicit initial ``$changeStream``
        stage and returns a
        :class:`~pymongo.change_stream.DatabaseChangeStream` cursor which
        iterates over changes on all collections in this database.

        Introduced in MongoDB 4.0.

        .. code-block:: python

           with db.watch() as stream:
               for change in stream:
                   print(change)

        The :class:`~pymongo.change_stream.DatabaseChangeStream` iterable
        blocks until the next change document is returned or an error is
        raised. If the
        :meth:`~pymongo.change_stream.DatabaseChangeStream.next` method
        encounters a network error when retrieving a batch from the server,
        it will automatically attempt to recreate the cursor such that no
        change events are missed. Any error encountered during the resume
        attempt indicates there may be an outage and will be raised.

        .. code-block:: python

            try:
                with db.watch(
                        [{'$match': {'operationType': 'insert'}}]) as stream:
                    for insert_change in stream:
                        print(insert_change)
            except pymongo.errors.PyMongoError:
                # The ChangeStream encountered an unrecoverable error or the
                # resume attempt failed to recreate the cursor.
                logging.error('...')

        For a precise description of the resume process see the
        `change streams specification`_.

        :Parameters:
          - `pipeline` (optional): A list of aggregation pipeline stages to
            append to an initial ``$changeStream`` stage. Not all
            pipeline stages are valid after a ``$changeStream`` stage, see the
            MongoDB documentation on change streams for the supported stages.
          - `full_document` (optional): The fullDocument to pass as an option
            to the ``$changeStream`` stage. Allowed values: 'updateLookup'.
            When set to 'updateLookup', the change notification for partial
            updates will include both a delta describing the changes to the
            document, as well as a copy of the entire document that was
            changed from some time after the change occurred.
          - `resume_after` (optional): A resume token. If provided, the
            change stream will start returning changes that occur directly
            after the operation specified in the resume token. A resume token
            is the _id value of a change document.
          - `max_await_time_ms` (optional): The maximum time in milliseconds
            for the server to wait for changes before responding to a getMore
            operation.
          - `batch_size` (optional): The maximum number of documents to return
            per batch.
          - `collation` (optional): The :class:`~pymongo.collation.Collation`
            to use for the aggregation.
          - `start_at_operation_time` (optional): If provided, the resulting
            change stream will only return changes that occurred at or after
            the specified :class:`~bson.timestamp.Timestamp`. Requires
            MongoDB >= 4.0.
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.
          - `start_after` (optional): The same as `resume_after` except that
            `start_after` can resume notifications after an invalidate event.
            This option and `resume_after` are mutually exclusive.

        :Returns:
          A :class:`~pymongo.change_stream.DatabaseChangeStream` cursor.

        .. versionchanged:: 3.9
           Added the ``start_after`` parameter.

        .. versionadded:: 3.7

        .. mongodoc:: changeStreams

        .. _change streams specification:
            https://github.com/mongodb/specifications/blob/master/source/change-streams/change-streams.rst
        """
        return DatabaseChangeStream(self, pipeline, full_document, resume_after, max_await_time_ms, batch_size, collation, start_at_operation_time, session, start_after)

    def _command--- This code section failed: ---

 L. 614         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'command'
                4  LOAD_GLOBAL              string_type
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    24  'to 24'

 L. 615        10  LOAD_GLOBAL              SON
               12  LOAD_FAST                'command'
               14  LOAD_FAST                'value'
               16  BUILD_TUPLE_2         2 
               18  BUILD_LIST_1          1 
               20  CALL_FUNCTION_1       1  ''
               22  STORE_FAST               'command'
             24_0  COME_FROM             8  '8'

 L. 617        24  LOAD_FAST                'command'
               26  LOAD_METHOD              update
               28  LOAD_FAST                'kwargs'
               30  CALL_METHOD_1         1  ''
               32  POP_TOP          

 L. 618        34  LOAD_FAST                'self'
               36  LOAD_ATTR                _Database__client
               38  LOAD_METHOD              _tmp_session
               40  LOAD_FAST                'session'
               42  CALL_METHOD_1         1  ''
               44  SETUP_WITH           96  'to 96'
               46  STORE_FAST               's'

 L. 619        48  LOAD_FAST                'sock_info'
               50  LOAD_ATTR                command

 L. 620        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _Database__name

 L. 621        56  LOAD_FAST                'command'

 L. 622        58  LOAD_FAST                'slave_ok'

 L. 623        60  LOAD_FAST                'read_preference'

 L. 624        62  LOAD_FAST                'codec_options'

 L. 625        64  LOAD_FAST                'check'

 L. 626        66  LOAD_FAST                'allowable_errors'

 L. 627        68  LOAD_FAST                'write_concern'

 L. 628        70  LOAD_FAST                'parse_write_concern_error'

 L. 629        72  LOAD_FAST                's'

 L. 630        74  LOAD_FAST                'self'
               76  LOAD_ATTR                _Database__client

 L. 619        78  LOAD_CONST               ('write_concern', 'parse_write_concern_error', 'session', 'client')
               80  CALL_FUNCTION_KW_11    11  '11 total positional and keyword args'
               82  POP_BLOCK        
               84  ROT_TWO          
               86  BEGIN_FINALLY    
               88  WITH_CLEANUP_START
               90  WITH_CLEANUP_FINISH
               92  POP_FINALLY           0  ''
               94  RETURN_VALUE     
             96_0  COME_FROM_WITH       44  '44'
               96  WITH_CLEANUP_START
               98  WITH_CLEANUP_FINISH
              100  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 84

    def command--- This code section failed: ---

 L. 726         0  LOAD_FAST                'read_preference'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    26  'to 26'

 L. 727         8  LOAD_FAST                'session'
               10  POP_JUMP_IF_FALSE    20  'to 20'
               12  LOAD_FAST                'session'
               14  LOAD_METHOD              _txn_read_preference
               16  CALL_METHOD_0         0  ''
               18  JUMP_IF_TRUE_OR_POP    24  'to 24'
             20_0  COME_FROM            10  '10'

 L. 728        20  LOAD_GLOBAL              ReadPreference
               22  LOAD_ATTR                PRIMARY
             24_0  COME_FROM            18  '18'

 L. 727        24  STORE_FAST               'read_preference'
             26_0  COME_FROM             6  '6'

 L. 729        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _Database__client
               30  LOAD_METHOD              _socket_for_reads

 L. 730        32  LOAD_FAST                'read_preference'

 L. 730        34  LOAD_FAST                'session'

 L. 729        36  CALL_METHOD_2         2  ''
               38  SETUP_WITH           94  'to 94'

 L. 730        40  UNPACK_SEQUENCE_2     2 
               42  STORE_FAST               'sock_info'
               44  STORE_FAST               'slave_ok'

 L. 731        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _command
               50  LOAD_FAST                'sock_info'
               52  LOAD_FAST                'command'
               54  LOAD_FAST                'slave_ok'
               56  LOAD_FAST                'value'

 L. 732        58  LOAD_FAST                'check'

 L. 732        60  LOAD_FAST                'allowable_errors'

 L. 732        62  LOAD_FAST                'read_preference'

 L. 733        64  LOAD_FAST                'codec_options'

 L. 731        66  BUILD_TUPLE_8         8 
               68  LOAD_STR                 'session'

 L. 733        70  LOAD_FAST                'session'

 L. 731        72  BUILD_MAP_1           1 

 L. 733        74  LOAD_FAST                'kwargs'

 L. 731        76  BUILD_MAP_UNPACK_WITH_CALL_2     2 
               78  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               80  POP_BLOCK        
               82  ROT_TWO          
               84  BEGIN_FINALLY    
               86  WITH_CLEANUP_START
               88  WITH_CLEANUP_FINISH
               90  POP_FINALLY           0  ''
               92  RETURN_VALUE     
             94_0  COME_FROM_WITH       38  '38'
               94  WITH_CLEANUP_START
               96  WITH_CLEANUP_FINISH
               98  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 82

    def _retryable_read_command(self, command, value=1, check=True, allowable_errors=None, read_preference=None, codec_options=DEFAULT_CODEC_OPTIONS, session=None, **kwargs):
        """Same as command but used for retryable read commands."""
        if read_preference is None:
            read_preference = session and session._txn_read_preference() or ReadPreference.PRIMARY

        def _cmd(session, server, sock_info, slave_ok):
            return (self._command)(sock_info, command, slave_ok, value,
 check, allowable_errors, read_preference,
 codec_options, session=session, **kwargs)

        return self._Database__client._retryable_read(_cmd, read_preference, session)

    def _list_collections--- This code section failed: ---

 L. 755         0  LOAD_FAST                'self'
                2  LOAD_ATTR                get_collection

 L. 756         4  LOAD_STR                 '$cmd'

 L. 756         6  LOAD_FAST                'read_preference'

 L. 755         8  LOAD_CONST               ('read_preference',)
               10  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               12  STORE_FAST               'coll'

 L. 757        14  LOAD_FAST                'sock_info'
               16  LOAD_ATTR                max_wire_version
               18  LOAD_CONST               2
               20  COMPARE_OP               >
               22  POP_JUMP_IF_FALSE   136  'to 136'

 L. 758        24  LOAD_GLOBAL              SON
               26  LOAD_CONST               ('listCollections', 1)

 L. 759        28  LOAD_STR                 'cursor'
               30  BUILD_MAP_0           0 
               32  BUILD_TUPLE_2         2 

 L. 758        34  BUILD_LIST_2          2 
               36  CALL_FUNCTION_1       1  ''
               38  STORE_FAST               'cmd'

 L. 760        40  LOAD_FAST                'cmd'
               42  LOAD_METHOD              update
               44  LOAD_FAST                'kwargs'
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          

 L. 761        50  LOAD_FAST                'self'
               52  LOAD_ATTR                _Database__client
               54  LOAD_ATTR                _tmp_session

 L. 762        56  LOAD_FAST                'session'

 L. 762        58  LOAD_CONST               False

 L. 761        60  LOAD_CONST               ('close',)
               62  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               64  SETUP_WITH          128  'to 128'

 L. 762        66  STORE_FAST               'tmp_session'

 L. 763        68  LOAD_FAST                'self'
               70  LOAD_ATTR                _command

 L. 764        72  LOAD_FAST                'sock_info'

 L. 764        74  LOAD_FAST                'cmd'

 L. 764        76  LOAD_FAST                'slave_okay'

 L. 765        78  LOAD_FAST                'read_preference'

 L. 766        80  LOAD_FAST                'tmp_session'

 L. 763        82  LOAD_CONST               ('read_preference', 'session')
               84  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'

 L. 766        86  LOAD_STR                 'cursor'

 L. 763        88  BINARY_SUBSCR    
               90  STORE_FAST               'cursor'

 L. 767        92  LOAD_GLOBAL              CommandCursor

 L. 768        94  LOAD_FAST                'coll'

 L. 769        96  LOAD_FAST                'cursor'

 L. 770        98  LOAD_FAST                'sock_info'
              100  LOAD_ATTR                address

 L. 771       102  LOAD_FAST                'tmp_session'

 L. 772       104  LOAD_FAST                'session'
              106  LOAD_CONST               None
              108  COMPARE_OP               is-not

 L. 767       110  LOAD_CONST               ('session', 'explicit_session')
              112  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              114  POP_BLOCK        
              116  ROT_TWO          
              118  BEGIN_FINALLY    
              120  WITH_CLEANUP_START
              122  WITH_CLEANUP_FINISH
              124  POP_FINALLY           0  ''
              126  RETURN_VALUE     
            128_0  COME_FROM_WITH       64  '64'
              128  WITH_CLEANUP_START
              130  WITH_CLEANUP_FINISH
              132  END_FINALLY      
              134  JUMP_FORWARD        278  'to 278'
            136_0  COME_FROM            22  '22'

 L. 774       136  LOAD_GLOBAL              _INDEX_REGEX
              138  STORE_FAST               'match'

 L. 775       140  LOAD_STR                 'filter'
              142  LOAD_FAST                'kwargs'
              144  COMPARE_OP               in
              146  POP_JUMP_IF_FALSE   164  'to 164'

 L. 776       148  LOAD_STR                 '$and'
              150  LOAD_GLOBAL              _INDEX_REGEX
              152  LOAD_FAST                'kwargs'
              154  LOAD_STR                 'filter'
              156  BINARY_SUBSCR    
              158  BUILD_LIST_2          2 
              160  BUILD_MAP_1           1 
              162  STORE_FAST               'match'
            164_0  COME_FROM           146  '146'

 L. 777       164  LOAD_GLOBAL              len
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                name
              170  LOAD_METHOD              encode
              172  LOAD_STR                 'utf8'
              174  CALL_METHOD_1         1  ''
              176  LOAD_CONST               b'.'
              178  BINARY_ADD       
              180  CALL_FUNCTION_1       1  ''
              182  STORE_FAST               'dblen'

 L. 779       184  LOAD_STR                 '$project'
              186  LOAD_STR                 '$substr'
              188  LOAD_STR                 '$name'
              190  LOAD_FAST                'dblen'
              192  LOAD_CONST               -1
              194  BUILD_LIST_3          3 
              196  BUILD_MAP_1           1 

 L. 780       198  LOAD_CONST               1

 L. 779       200  LOAD_CONST               ('name', 'options')
              202  BUILD_CONST_KEY_MAP_2     2 
              204  BUILD_MAP_1           1 

 L. 781       206  LOAD_STR                 '$match'
              208  LOAD_FAST                'match'
              210  BUILD_MAP_1           1 

 L. 778       212  BUILD_LIST_2          2 
              214  STORE_FAST               'pipeline'

 L. 783       216  LOAD_GLOBAL              SON
              218  LOAD_CONST               ('aggregate', 'system.namespaces')

 L. 784       220  LOAD_STR                 'pipeline'
              222  LOAD_FAST                'pipeline'
              224  BUILD_TUPLE_2         2 

 L. 785       226  LOAD_STR                 'cursor'
              228  LOAD_FAST                'kwargs'
              230  LOAD_METHOD              get
              232  LOAD_STR                 'cursor'
              234  BUILD_MAP_0           0 
              236  CALL_METHOD_2         2  ''
              238  BUILD_TUPLE_2         2 

 L. 783       240  BUILD_LIST_3          3 
              242  CALL_FUNCTION_1       1  ''
              244  STORE_FAST               'cmd'

 L. 786       246  LOAD_FAST                'self'
              248  LOAD_METHOD              _command
              250  LOAD_FAST                'sock_info'
              252  LOAD_FAST                'cmd'
              254  LOAD_FAST                'slave_okay'
              256  CALL_METHOD_3         3  ''
              258  LOAD_STR                 'cursor'
              260  BINARY_SUBSCR    
              262  STORE_FAST               'cursor'

 L. 787       264  LOAD_GLOBAL              CommandCursor
              266  LOAD_FAST                'coll'
              268  LOAD_FAST                'cursor'
              270  LOAD_FAST                'sock_info'
              272  LOAD_ATTR                address
              274  CALL_FUNCTION_3       3  ''
              276  RETURN_VALUE     
            278_0  COME_FROM           134  '134'

Parse error at or near `ROT_TWO' instruction at offset 116

    def list_collections(self, session=None, filter=None, **kwargs):
        """Get a cursor over the collectons of this database.

        :Parameters:
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.
          - `filter` (optional):  A query document to filter the list of
            collections returned from the listCollections command.
          - `**kwargs` (optional): Optional parameters of the
            `listCollections command
            <https://docs.mongodb.com/manual/reference/command/listCollections/>`_
            can be passed as keyword arguments to this method. The supported
            options differ by server version.

        :Returns:
          An instance of :class:`~pymongo.command_cursor.CommandCursor`.

        .. versionadded:: 3.6
        """
        if filter is not None:
            kwargs['filter'] = filter
        read_pref = session and session._txn_read_preference() or ReadPreference.PRIMARY

        def _cmd(session, server, sock_info, slave_okay):
            return (self._list_collections)(
 sock_info, slave_okay, session, read_preference=read_pref, **kwargs)

        return self._Database__client._retryable_read(_cmd, read_pref, session)

    def list_collection_names--- This code section failed: ---

 L. 845         0  LOAD_FAST                'filter'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    18  'to 18'

 L. 846         8  LOAD_CONST               True
               10  LOAD_FAST                'kwargs'
               12  LOAD_STR                 'nameOnly'
               14  STORE_SUBSCR     
               16  JUMP_FORWARD         70  'to 70'
             18_0  COME_FROM             6  '6'

 L. 850        18  LOAD_GLOBAL              common
               20  LOAD_METHOD              validate_is_mapping
               22  LOAD_STR                 'filter'
               24  LOAD_FAST                'filter'
               26  CALL_METHOD_2         2  ''
               28  POP_TOP          

 L. 851        30  LOAD_FAST                'filter'
               32  LOAD_FAST                'kwargs'
               34  LOAD_STR                 'filter'
               36  STORE_SUBSCR     

 L. 852        38  LOAD_FAST                'filter'
               40  POP_JUMP_IF_FALSE    62  'to 62'
               42  LOAD_GLOBAL              len
               44  LOAD_FAST                'filter'
               46  CALL_FUNCTION_1       1  ''
               48  LOAD_CONST               1
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    70  'to 70'
               54  LOAD_STR                 'name'
               56  LOAD_FAST                'filter'
               58  COMPARE_OP               in
               60  POP_JUMP_IF_FALSE    70  'to 70'
             62_0  COME_FROM            40  '40'

 L. 853        62  LOAD_CONST               True
               64  LOAD_FAST                'kwargs'
               66  LOAD_STR                 'nameOnly'
               68  STORE_SUBSCR     
             70_0  COME_FROM            60  '60'
             70_1  COME_FROM            52  '52'
             70_2  COME_FROM            16  '16'

 L. 855        70  LOAD_LISTCOMP            '<code_object <listcomp>>'
               72  LOAD_STR                 'Database.list_collection_names.<locals>.<listcomp>'
               74  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 856        76  LOAD_FAST                'self'
               78  LOAD_ATTR                list_collections
               80  BUILD_TUPLE_0         0 
               82  LOAD_STR                 'session'
               84  LOAD_FAST                'session'
               86  BUILD_MAP_1           1 
               88  LOAD_FAST                'kwargs'
               90  BUILD_MAP_UNPACK_WITH_CALL_2     2 
               92  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'

 L. 855        94  GET_ITER         
               96  CALL_FUNCTION_1       1  ''
               98  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 98

    def collection_names(self, include_system_collections=True, session=None):
        """**DEPRECATED**: Get a list of all the collection names in this
        database.

        :Parameters:
          - `include_system_collections` (optional): if ``False`` list
            will not include system collections (e.g ``system.indexes``)
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.

        .. versionchanged:: 3.7
           Deprecated. Use :meth:`list_collection_names` instead.

        .. versionchanged:: 3.6
           Added ``session`` parameter.
        """
        warnings.warn('collection_names is deprecated. Use list_collection_names instead.', DeprecationWarning,
          stacklevel=2)
        kws = {} if include_system_collections else _SYSTEM_FILTER
        return [result['name'] for result in (self.list_collections)(session=session, nameOnly=True, **kws)]

    def drop_collection--- This code section failed: ---

 L. 904         0  LOAD_FAST                'name_or_collection'
                2  STORE_FAST               'name'

 L. 905         4  LOAD_GLOBAL              isinstance
                6  LOAD_FAST                'name'
                8  LOAD_GLOBAL              Collection
               10  CALL_FUNCTION_2       2  ''
               12  POP_JUMP_IF_FALSE    20  'to 20'

 L. 906        14  LOAD_FAST                'name'
               16  LOAD_ATTR                name
               18  STORE_FAST               'name'
             20_0  COME_FROM            12  '12'

 L. 908        20  LOAD_GLOBAL              isinstance
               22  LOAD_FAST                'name'
               24  LOAD_GLOBAL              string_type
               26  CALL_FUNCTION_2       2  ''
               28  POP_JUMP_IF_TRUE     46  'to 46'

 L. 909        30  LOAD_GLOBAL              TypeError
               32  LOAD_STR                 'name_or_collection must be an instance of %s'

 L. 910        34  LOAD_GLOBAL              string_type
               36  LOAD_ATTR                __name__
               38  BUILD_TUPLE_1         1 

 L. 909        40  BINARY_MODULO    
               42  CALL_FUNCTION_1       1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
             46_0  COME_FROM            28  '28'

 L. 912        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _Database__client
               50  LOAD_METHOD              _purge_index
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                _Database__name
               56  LOAD_FAST                'name'
               58  CALL_METHOD_2         2  ''
               60  POP_TOP          

 L. 914        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _Database__client
               66  LOAD_METHOD              _socket_for_writes
               68  LOAD_FAST                'session'
               70  CALL_METHOD_1         1  ''
               72  SETUP_WITH          124  'to 124'
               74  STORE_FAST               'sock_info'

 L. 915        76  LOAD_FAST                'self'
               78  LOAD_ATTR                _command

 L. 916        80  LOAD_FAST                'sock_info'

 L. 916        82  LOAD_STR                 'drop'

 L. 916        84  LOAD_GLOBAL              _unicode
               86  LOAD_FAST                'name'
               88  CALL_FUNCTION_1       1  ''

 L. 917        90  LOAD_STR                 'ns not found'
               92  BUILD_LIST_1          1 

 L. 918        94  LOAD_FAST                'self'
               96  LOAD_METHOD              _write_concern_for
               98  LOAD_FAST                'session'
              100  CALL_METHOD_1         1  ''

 L. 919       102  LOAD_CONST               True

 L. 920       104  LOAD_FAST                'session'

 L. 915       106  LOAD_CONST               ('value', 'allowable_errors', 'write_concern', 'parse_write_concern_error', 'session')
              108  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              110  POP_BLOCK        
              112  ROT_TWO          
              114  BEGIN_FINALLY    
              116  WITH_CLEANUP_START
              118  WITH_CLEANUP_FINISH
              120  POP_FINALLY           0  ''
              122  RETURN_VALUE     
            124_0  COME_FROM_WITH       72  '72'
              124  WITH_CLEANUP_START
              126  WITH_CLEANUP_FINISH
              128  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 112

    def validate_collection(self, name_or_collection, scandata=False, full=False, session=None):
        """Validate a collection.

        Returns a dict of validation info. Raises CollectionInvalid if
        validation fails.

        :Parameters:
          - `name_or_collection`: A Collection object or the name of a
            collection to validate.
          - `scandata`: Do extra checks beyond checking the overall
            structure of the collection.
          - `full`: Have the server do a more thorough scan of the
            collection. Use with `scandata` for a thorough scan
            of the structure of the collection and the individual
            documents.
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.

        .. versionchanged:: 3.6
           Added ``session`` parameter.
        """
        name = name_or_collection
        if isinstance(name, Collection):
            name = name.name
        if not isinstance(name, string_type):
            raise TypeError('name_or_collection must be an instance of %s or Collection' % (
             string_type.__name__,))
        result = self.command('validate', (_unicode(name)), scandata=scandata,
          full=full,
          session=session)
        valid = True
        if 'result' in result:
            info = result['result']
            if info.find('exception') != -1 or info.find('corrupt') != -1:
                raise CollectionInvalid('%s invalid: %s' % (name, info))
        else:
            if 'raw' in result:
                for _, res in iteritems(result['raw']):
                    if 'result' in res:
                        info = res['result']
                        if info.find('exception') != -1 or info.find('corrupt') != -1:
                            raise CollectionInvalid('%s invalid: %s' % (
                             name, info))
                        elif not res.get('valid', False):
                            valid = False
                            break

            else:
                if not result.get('valid', False):
                    valid = False
                if not valid:
                    raise CollectionInvalid('%s invalid: %r' % (name, result))
                return result

    def _current_op--- This code section failed: ---

 L. 984         0  LOAD_GLOBAL              SON
                2  LOAD_CONST               ('currentOp', 1)
                4  LOAD_STR                 '$all'
                6  LOAD_FAST                'include_all'
                8  BUILD_TUPLE_2         2 
               10  BUILD_LIST_2          2 
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'cmd'

 L. 985        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _Database__client
               20  LOAD_METHOD              _socket_for_writes
               22  LOAD_FAST                'session'
               24  CALL_METHOD_1         1  ''
               26  SETUP_WITH          142  'to 142'
               28  STORE_FAST               'sock_info'

 L. 986        30  LOAD_FAST                'sock_info'
               32  LOAD_ATTR                max_wire_version
               34  LOAD_CONST               4
               36  COMPARE_OP               >=
               38  POP_JUMP_IF_FALSE    76  'to 76'

 L. 987        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _Database__client
               44  LOAD_ATTR                admin
               46  LOAD_ATTR                _command

 L. 988        48  LOAD_FAST                'sock_info'

 L. 988        50  LOAD_FAST                'cmd'

 L. 988        52  LOAD_FAST                'self'
               54  LOAD_ATTR                codec_options

 L. 989        56  LOAD_FAST                'session'

 L. 987        58  LOAD_CONST               ('codec_options', 'session')
               60  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               62  POP_BLOCK        
               64  ROT_TWO          
               66  BEGIN_FINALLY    
               68  WITH_CLEANUP_START
               70  WITH_CLEANUP_FINISH
               72  POP_FINALLY           0  ''
               74  RETURN_VALUE     
             76_0  COME_FROM            38  '38'

 L. 991        76  LOAD_FAST                'include_all'
               78  POP_JUMP_IF_FALSE    88  'to 88'
               80  LOAD_STR                 '$all'
               82  LOAD_CONST               True
               84  BUILD_MAP_1           1 
               86  JUMP_FORWARD         90  'to 90'
             88_0  COME_FROM            78  '78'
               88  BUILD_MAP_0           0 
             90_0  COME_FROM            86  '86'
               90  STORE_FAST               'spec'

 L. 992        92  LOAD_GLOBAL              _first_batch
               94  LOAD_FAST                'sock_info'
               96  LOAD_STR                 'admin'
               98  LOAD_STR                 '$cmd.sys.inprog'

 L. 993       100  LOAD_FAST                'spec'

 L. 993       102  LOAD_CONST               -1

 L. 993       104  LOAD_CONST               True

 L. 993       106  LOAD_FAST                'self'
              108  LOAD_ATTR                codec_options

 L. 994       110  LOAD_GLOBAL              ReadPreference
              112  LOAD_ATTR                PRIMARY

 L. 994       114  LOAD_FAST                'cmd'

 L. 995       116  LOAD_FAST                'self'
              118  LOAD_ATTR                client
              120  LOAD_ATTR                _event_listeners

 L. 992       122  CALL_FUNCTION_10     10  ''
              124  POP_BLOCK        
              126  ROT_TWO          
              128  BEGIN_FINALLY    
              130  WITH_CLEANUP_START
              132  WITH_CLEANUP_FINISH
              134  POP_FINALLY           0  ''
              136  RETURN_VALUE     
              138  POP_BLOCK        
              140  BEGIN_FINALLY    
            142_0  COME_FROM_WITH       26  '26'
              142  WITH_CLEANUP_START
              144  WITH_CLEANUP_FINISH
              146  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 64

    def current_op(self, include_all=False, session=None):
        """**DEPRECATED**: Get information on operations currently running.

        Starting with MongoDB 3.6 this helper is obsolete. The functionality
        provided by this helper is available in MongoDB 3.6+ using the
        `$currentOp aggregation pipeline stage`_, which can be used with
        :meth:`aggregate`. Note that, while this helper can only return
        a single document limited to a 16MB result, :meth:`aggregate`
        returns a cursor avoiding that limitation.

        Users of MongoDB versions older than 3.6 can use the `currentOp command`_
        directly::

          # MongoDB 3.2 and 3.4
          client.admin.command("currentOp")

        Or query the "inprog" virtual collection::

          # MongoDB 2.6 and 3.0
          client.admin["$cmd.sys.inprog"].find_one()

        :Parameters:
          - `include_all` (optional): if ``True`` also list currently
            idle operations in the result
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.

        .. versionchanged:: 3.9
           Deprecated.

        .. versionchanged:: 3.6
           Added ``session`` parameter.

        .. _$currentOp aggregation pipeline stage: https://docs.mongodb.com/manual/reference/operator/aggregation/currentOp/
        .. _currentOp command: https://docs.mongodb.com/manual/reference/command/currentOp/
        """
        warnings.warn('current_op() is deprecated. See the documentation for more information', DeprecationWarning,
          stacklevel=2)
        return self._current_op(include_all, session)

    def profiling_level(self, session=None):
        """Get the database's current profiling level.

        Returns one of (:data:`~pymongo.OFF`,
        :data:`~pymongo.SLOW_ONLY`, :data:`~pymongo.ALL`).

        :Parameters:
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.

        .. versionchanged:: 3.6
           Added ``session`` parameter.

        .. mongodoc:: profiling
        """
        result = self.command('profile', (-1), session=session)
        if not (result['was'] >= 0 and result['was'] <= 2):
            raise AssertionError
        return result['was']

    def set_profiling_level(self, level, slow_ms=None, session=None):
        """Set the database's profiling level.

        :Parameters:
          - `level`: Specifies a profiling level, see list of possible values
            below.
          - `slow_ms`: Optionally modify the threshold for the profile to
            consider a query or operation.  Even if the profiler is off queries
            slower than the `slow_ms` level will get written to the logs.
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.

        Possible `level` values:

        +----------------------------+------------------------------------+
        | Level                      | Setting                            |
        +============================+====================================+
        | :data:`~pymongo.OFF`       | Off. No profiling.                 |
        +----------------------------+------------------------------------+
        | :data:`~pymongo.SLOW_ONLY` | On. Only includes slow operations. |
        +----------------------------+------------------------------------+
        | :data:`~pymongo.ALL`       | On. Includes all operations.       |
        +----------------------------+------------------------------------+

        Raises :class:`ValueError` if level is not one of
        (:data:`~pymongo.OFF`, :data:`~pymongo.SLOW_ONLY`,
        :data:`~pymongo.ALL`).

        .. versionchanged:: 3.6
           Added ``session`` parameter.

        .. mongodoc:: profiling
        """
        if isinstance(level, int):
            if level < 0 or level > 2:
                raise ValueError('level must be one of (OFF, SLOW_ONLY, ALL)')
            if slow_ms is not None:
                if not isinstance(slow_ms, int):
                    raise TypeError('slow_ms must be an integer')
        elif slow_ms is not None:
            self.command('profile', level, slowms=slow_ms, session=session)
        else:
            self.command('profile', level, session=session)

    def profiling_info(self, session=None):
        """Returns a list containing current profiling information.

        :Parameters:
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.

        .. versionchanged:: 3.6
           Added ``session`` parameter.

        .. mongodoc:: profiling
        """
        return list(self['system.profile'].find(session=session))

    def error(self):
        """**DEPRECATED**: Get the error if one occurred on the last operation.

        This method is obsolete: all MongoDB write operations (insert, update,
        remove, and so on) use the write concern ``w=1`` and report their
        errors by default.

        .. versionchanged:: 2.8
           Deprecated.
        """
        warnings.warn('Database.error() is deprecated', DeprecationWarning,
          stacklevel=2)
        error = self.command('getlasterror')
        error_msg = error.get('err', '')
        if error_msg is None:
            return
        if error_msg.startswith('not master'):
            primary = self._Database__client.primary
            if primary:
                self._Database__client._reset_server_and_request_check(primary)
        return error

    def last_status(self):
        """**DEPRECATED**: Get status information from the last operation.

        This method is obsolete: all MongoDB write operations (insert, update,
        remove, and so on) use the write concern ``w=1`` and report their
        errors by default.

        Returns a SON object with status information.

        .. versionchanged:: 2.8
           Deprecated.
        """
        warnings.warn('last_status() is deprecated', DeprecationWarning,
          stacklevel=2)
        return self.command('getlasterror')

    def previous_error(self):
        """**DEPRECATED**: Get the most recent error on this database.

        This method is obsolete: all MongoDB write operations (insert, update,
        remove, and so on) use the write concern ``w=1`` and report their
        errors by default.

        Only returns errors that have occurred since the last call to
        :meth:`reset_error_history`. Returns None if no such errors have
        occurred.

        .. versionchanged:: 2.8
           Deprecated.
        """
        warnings.warn('previous_error() is deprecated', DeprecationWarning,
          stacklevel=2)
        error = self.command('getpreverror')
        if error.get('err', 0) is None:
            return
        return error

    def reset_error_history(self):
        """**DEPRECATED**: Reset the error history of this database.

        This method is obsolete: all MongoDB write operations (insert, update,
        remove, and so on) use the write concern ``w=1`` and report their
        errors by default.

        Calls to :meth:`previous_error` will only return errors that have
        occurred since the most recent call to this method.

        .. versionchanged:: 2.8
           Deprecated.
        """
        warnings.warn('reset_error_history() is deprecated', DeprecationWarning,
          stacklevel=2)
        self.command('reseterror')

    def __iter__(self):
        return self

    def __next__(self):
        raise TypeError("'Database' object is not iterable")

    next = __next__

    def _default_role(self, read_only):
        """Return the default user role for this database."""
        if self.name == 'admin':
            if read_only:
                return 'readAnyDatabase'
            return 'root'
        else:
            if read_only:
                return 'read'
            return 'dbOwner'

    def _create_or_update_user(self, create, name, password, read_only, session=None, **kwargs):
        """Use a command to create (if create=True) or modify a user.
        """
        opts = {}
        if not read_only:
            if create:
                if 'roles' not in kwargs:
                    warnings.warn('Creating a user with the read_only option or without roles is deprecated in MongoDB >= 2.6', DeprecationWarning)
                    opts['roles'] = [
                     self._default_role(read_only)]
            if read_only:
                warnings.warn("The read_only option is deprecated in MongoDB >= 2.6, use 'roles' instead", DeprecationWarning)
            if password is not None:
                if 'digestPassword' in kwargs:
                    raise ConfigurationError("The digestPassword option is not supported via add_user. Please use db.command('createUser', ...) instead for this option.")
                opts['pwd'] = password
        else:
            if self.write_concern.acknowledged:
                if self.write_concern.document:
                    opts['writeConcern'] = self.write_concern.document
            opts.update(kwargs)
            if create:
                command_name = 'createUser'
            else:
                command_name = 'updateUser'
        (self.command)(command_name, name, session=session, **opts)

    def add_user(self, name, password=None, read_only=None, session=None, **kwargs):
        """**DEPRECATED**: Create user `name` with password `password`.

        Add a new user with permissions for this :class:`Database`.

        .. note:: Will change the password if user `name` already exists.

        .. note:: add_user is deprecated and will be removed in PyMongo
          4.0. Starting with MongoDB 2.6 user management is handled with four
          database commands, createUser_, usersInfo_, updateUser_, and
          dropUser_.

          To create a user::

            db.command("createUser", "admin", pwd="password", roles=["root"])

          To create a read-only user::

            db.command("createUser", "user", pwd="password", roles=["read"])

          To change a password::

            db.command("updateUser", "user", pwd="newpassword")

          Or change roles::

            db.command("updateUser", "user", roles=["readWrite"])

        .. _createUser: https://docs.mongodb.com/manual/reference/command/createUser/
        .. _usersInfo: https://docs.mongodb.com/manual/reference/command/usersInfo/
        .. _updateUser: https://docs.mongodb.com/manual/reference/command/updateUser/
        .. _dropUser: https://docs.mongodb.com/manual/reference/command/createUser/

        .. warning:: Never create or modify users over an insecure network without
          the use of TLS. See :doc:`/examples/tls` for more information.

        :Parameters:
          - `name`: the name of the user to create
          - `password` (optional): the password of the user to create. Can not
            be used with the ``userSource`` argument.
          - `read_only` (optional): if ``True`` the user will be read only
          - `**kwargs` (optional): optional fields for the user document
            (e.g. ``userSource``, ``otherDBRoles``, or ``roles``). See
            `<http://docs.mongodb.org/manual/reference/privilege-documents>`_
            for more information.
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.

        .. versionchanged:: 3.7
           Added support for SCRAM-SHA-256 users with MongoDB 4.0 and later.

        .. versionchanged:: 3.6
           Added ``session`` parameter. Deprecated add_user.

        .. versionchanged:: 2.5
           Added kwargs support for optional fields introduced in MongoDB 2.4

        .. versionchanged:: 2.2
           Added support for read only users
        """
        warnings.warn('add_user is deprecated and will be removed in PyMongo 4.0. Use db.command with createUser or updateUser instead', DeprecationWarning,
          stacklevel=2)
        if not isinstance(name, string_type):
            raise TypeError('name must be an instance of %s' % (
             string_type.__name__,))
        if password is not None:
            if not isinstance(password, string_type):
                raise TypeError('password must be an instance of %s' % (
                 string_type.__name__,))
            if len(password) == 0:
                raise ValueError("password can't be empty")
        if read_only is not None:
            read_only = common.validate_boolean('read_only', read_only)
            if 'roles' in kwargs:
                raise ConfigurationError('Can not use read_only and roles together')
        try:
            uinfo = self.command('usersInfo', name, session=session)
            (self._create_or_update_user)(
 not uinfo['users'], name, password, read_only, session=session, **kwargs)
        except OperationFailure as exc:
            try:
                if exc.code == 13:
                    (self._create_or_update_user)(True, name, password, read_only, session=session, **kwargs)
                else:
                    raise
            finally:
                exc = None
                del exc

    def remove_user(self, name, session=None):
        """**DEPRECATED**: Remove user `name` from this :class:`Database`.

        User `name` will no longer have permissions to access this
        :class:`Database`.

        .. note:: remove_user is deprecated and will be removed in PyMongo
          4.0. Use the dropUser command instead::

            db.command("dropUser", "user")

        :Parameters:
          - `name`: the name of the user to remove
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.

        .. versionchanged:: 3.6
           Added ``session`` parameter. Deprecated remove_user.
        """
        warnings.warn('remove_user is deprecated and will be removed in PyMongo 4.0. Use db.command with dropUser instead', DeprecationWarning,
          stacklevel=2)
        cmd = SON([('dropUser', name)])
        if self.write_concern.acknowledged:
            if self.write_concern.document:
                cmd['writeConcern'] = self.write_concern.document
        self.command(cmd, session=session)

    def authenticate(self, name=None, password=None, source=None, mechanism='DEFAULT', **kwargs):
        """**DEPRECATED**: Authenticate to use this database.

        .. warning:: Starting in MongoDB 3.6, calling :meth:`authenticate`
          invalidates all existing cursors. It may also leave logical sessions
          open on the server for up to 30 minutes until they time out.

        Authentication lasts for the life of the underlying client
        instance, or until :meth:`logout` is called.

        Raises :class:`TypeError` if (required) `name`, (optional) `password`,
        or (optional) `source` is not an instance of :class:`basestring`
        (:class:`str` in python 3).

        .. note::
          - This method authenticates the current connection, and
            will also cause all new :class:`~socket.socket` connections
            in the underlying client instance to be authenticated automatically.

          - Authenticating more than once on the same database with different
            credentials is not supported. You must call :meth:`logout` before
            authenticating with new credentials.

          - When sharing a client instance between multiple threads, all
            threads will share the authentication. If you need different
            authentication profiles for different purposes you must use
            distinct client instances.

        :Parameters:
          - `name`: the name of the user to authenticate. Optional when
            `mechanism` is MONGODB-X509 and the MongoDB server version is
            >= 3.4.
          - `password` (optional): the password of the user to authenticate.
            Not used with GSSAPI or MONGODB-X509 authentication.
          - `source` (optional): the database to authenticate on. If not
            specified the current database is used.
          - `mechanism` (optional): See :data:`~pymongo.auth.MECHANISMS` for
            options. If no mechanism is specified, PyMongo automatically uses
            MONGODB-CR when connected to a pre-3.0 version of MongoDB,
            SCRAM-SHA-1 when connected to MongoDB 3.0 through 3.6, and
            negotiates the mechanism to use (SCRAM-SHA-1 or SCRAM-SHA-256) when
            connected to MongoDB 4.0+.
          - `authMechanismProperties` (optional): Used to specify
            authentication mechanism specific options. To specify the service
            name for GSSAPI authentication pass
            authMechanismProperties='SERVICE_NAME:<service name>'

        .. versionchanged:: 3.7
           Added support for SCRAM-SHA-256 with MongoDB 4.0 and later.

        .. versionchanged:: 3.5
           Deprecated. Authenticating multiple users conflicts with support for
           logical sessions in MongoDB 3.6. To authenticate as multiple users,
           create multiple instances of MongoClient.

        .. versionadded:: 2.8
           Use SCRAM-SHA-1 with MongoDB 3.0 and later.

        .. versionchanged:: 2.5
           Added the `source` and `mechanism` parameters. :meth:`authenticate`
           now raises a subclass of :class:`~pymongo.errors.PyMongoError` if
           authentication fails due to invalid credentials or configuration
           issues.

        .. mongodoc:: authenticate
        """
        if name is not None:
            if not isinstance(name, string_type):
                raise TypeError('name must be an instance of %s' % (
                 string_type.__name__,))
        else:
            if password is not None:
                if not isinstance(password, string_type):
                    raise TypeError('password must be an instance of %s' % (
                     string_type.__name__,))
            if source is not None and not isinstance(source, string_type):
                raise TypeError('source must be an instance of %s' % (
                 string_type.__name__,))
        common.validate_auth_mechanism('mechanism', mechanism)
        validated_options = {}
        for option, value in iteritems(kwargs):
            normalized, val = common.validate_auth_option(option, value)
            validated_options[normalized] = val
        else:
            credentials = auth._build_credentials_tuple(mechanism, source, name, password, validated_options, self.name)
            self.client._cache_credentials((self.name),
              credentials,
              connect=True)
            return True

    def logout(self):
        """**DEPRECATED**: Deauthorize use of this database.

        .. warning:: Starting in MongoDB 3.6, calling :meth:`logout`
          invalidates all existing cursors. It may also leave logical sessions
          open on the server for up to 30 minutes until they time out.
        """
        warnings.warn('Database.logout() is deprecated', DeprecationWarning,
          stacklevel=2)
        self.client._purge_credentials(self.name)

    def dereference(self, dbref, session=None, **kwargs):
        """Dereference a :class:`~bson.dbref.DBRef`, getting the
        document it points to.

        Raises :class:`TypeError` if `dbref` is not an instance of
        :class:`~bson.dbref.DBRef`. Returns a document, or ``None`` if
        the reference does not point to a valid document.  Raises
        :class:`ValueError` if `dbref` has a database specified that
        is different from the current database.

        :Parameters:
          - `dbref`: the reference
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.
          - `**kwargs` (optional): any additional keyword arguments
            are the same as the arguments to
            :meth:`~pymongo.collection.Collection.find`.

        .. versionchanged:: 3.6
           Added ``session`` parameter.
        """
        if not isinstance(dbref, DBRef):
            raise TypeError('cannot dereference a %s' % type(dbref))
        if dbref.database is not None:
            if dbref.database != self._Database__name:
                raise ValueError('trying to dereference a DBRef that points to another database (%r not %r)' % (
                 dbref.database,
                 self._Database__name))
        return (self[dbref.collection].find_one)(
 {'_id': dbref.id}, session=session, **kwargs)

    def eval(self, code, *args):
        """**DEPRECATED**: Evaluate a JavaScript expression in MongoDB.

        :Parameters:
          - `code`: string representation of JavaScript code to be
            evaluated
          - `args` (optional): additional positional arguments are
            passed to the `code` being evaluated

        .. warning:: the eval command is deprecated in MongoDB 3.0 and
          will be removed in a future server version.
        """
        warnings.warn('Database.eval() is deprecated', DeprecationWarning,
          stacklevel=2)
        if not isinstance(code, Code):
            code = Code(code)
        result = self.command('$eval', code, args=args)
        return result.get('retval', None)

    def __call__(self, *args, **kwargs):
        """This is only here so that some API misusages are easier to debug.
        """
        raise TypeError("'Database' object is not callable. If you meant to call the '%s' method on a '%s' object it is failing because no such method exists." % (
         self._Database__name, self._Database__client.__class__.__name__))


class SystemJS(object):
    __doc__ = '**DEPRECATED**: Helper class for dealing with stored JavaScript.\n    '

    def __init__(self, database):
        """**DEPRECATED**: Get a system js helper for the database `database`.

        SystemJS will be removed in PyMongo 4.0.
        """
        warnings.warn('SystemJS is deprecated', DeprecationWarning,
          stacklevel=2)
        if not database.write_concern.acknowledged:
            database = database.client.get_database((database.name),
              write_concern=DEFAULT_WRITE_CONCERN)
        object.__setattr__(self, '_db', database)

    def __setattr__(self, name, code):
        self._db.system.js.replace_one({'_id': name}, {'_id':name,  'value':Code(code)}, True)

    def __setitem__(self, name, code):
        self.__setattr__(name, code)

    def __delattr__(self, name):
        self._db.system.js.delete_one({'_id': name})

    def __delitem__(self, name):
        self.__delattr__(name)

    def __getattr__(self, name):
        return lambda *args: (self._db.eval)(Code('function() { return this[name].apply(this, arguments); }', scope={'name': name}), *args)

    def __getitem__(self, name):
        return self.__getattr__(name)

    def list(self):
        """Get a list of the names of the functions stored in this database."""
        return [x['_id'] for x in self._db.system.js.find(projection=['_id'])]