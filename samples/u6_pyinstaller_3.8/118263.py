# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pymongo\collection.py
"""Collection level utilities for Mongo."""
import datetime, warnings
from bson.code import Code
from bson.objectid import ObjectId
from bson.py3compat import _unicode, abc, integer_types, string_type
from bson.raw_bson import RawBSONDocument
from bson.codec_options import CodecOptions
from bson.son import SON
from pymongo import common, helpers, message
from pymongo.aggregation import _CollectionAggregationCommand, _CollectionRawAggregationCommand
from pymongo.bulk import BulkOperationBuilder, _Bulk
from pymongo.command_cursor import CommandCursor, RawBatchCommandCursor
from pymongo.common import ORDERED_TYPES
from pymongo.collation import validate_collation_or_none
from pymongo.change_stream import CollectionChangeStream
from pymongo.cursor import Cursor, RawBatchCursor
from pymongo.errors import BulkWriteError, ConfigurationError, InvalidName, InvalidOperation, OperationFailure
from pymongo.helpers import _check_write_command_response, _raise_last_error
from pymongo.message import _UNICODE_REPLACE_CODEC_OPTIONS
from pymongo.operations import IndexModel
from pymongo.read_preferences import ReadPreference
from pymongo.results import BulkWriteResult, DeleteResult, InsertOneResult, InsertManyResult, UpdateResult
from pymongo.write_concern import WriteConcern
_NO_OBJ_ERROR = 'No matching object found'
_UJOIN = '%s.%s'
_FIND_AND_MODIFY_DOC_FIELDS = {'value': 1}

class ReturnDocument(object):
    __doc__ = 'An enum used with\n    :meth:`~pymongo.collection.Collection.find_one_and_replace` and\n    :meth:`~pymongo.collection.Collection.find_one_and_update`.\n    '
    BEFORE = False
    AFTER = True


class Collection(common.BaseObject):
    __doc__ = 'A Mongo collection.\n    '

    def __init__(self, database, name, create=False, codec_options=None, read_preference=None, write_concern=None, read_concern=None, session=None, **kwargs):
        """Get / create a Mongo collection.

        Raises :class:`TypeError` if `name` is not an instance of
        :class:`basestring` (:class:`str` in python 3). Raises
        :class:`~pymongo.errors.InvalidName` if `name` is not a valid
        collection name. Any additional keyword arguments will be used
        as options passed to the create command. See
        :meth:`~pymongo.database.Database.create_collection` for valid
        options.

        If `create` is ``True``, `collation` is specified, or any additional
        keyword arguments are present, a ``create`` command will be
        sent, using ``session`` if specified. Otherwise, a ``create`` command
        will not be sent and the collection will be created implicitly on first
        use. The optional ``session`` argument is *only* used for the ``create``
        command, it is not associated with the collection afterward.

        :Parameters:
          - `database`: the database to get a collection from
          - `name`: the name of the collection to get
          - `create` (optional): if ``True``, force collection
            creation even without options being set
          - `codec_options` (optional): An instance of
            :class:`~bson.codec_options.CodecOptions`. If ``None`` (the
            default) database.codec_options is used.
          - `read_preference` (optional): The read preference to use. If
            ``None`` (the default) database.read_preference is used.
          - `write_concern` (optional): An instance of
            :class:`~pymongo.write_concern.WriteConcern`. If ``None`` (the
            default) database.write_concern is used.
          - `read_concern` (optional): An instance of
            :class:`~pymongo.read_concern.ReadConcern`. If ``None`` (the
            default) database.read_concern is used.
          - `collation` (optional): An instance of
            :class:`~pymongo.collation.Collation`. If a collation is provided,
            it will be passed to the create collection command. This option is
            only supported on MongoDB 3.4 and above.
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession` that is used with
            the create collection command
          - `**kwargs` (optional): additional keyword arguments will
            be passed as options for the create collection command

        .. versionchanged:: 3.6
           Added ``session`` parameter.

        .. versionchanged:: 3.4
           Support the `collation` option.

        .. versionchanged:: 3.2
           Added the read_concern option.

        .. versionchanged:: 3.0
           Added the codec_options, read_preference, and write_concern options.
           Removed the uuid_subtype attribute.
           :class:`~pymongo.collection.Collection` no longer returns an
           instance of :class:`~pymongo.collection.Collection` for attribute
           names with leading underscores. You must use dict-style lookups
           instead::

               collection['__my_collection__']

           Not:

               collection.__my_collection__

        .. versionchanged:: 2.2
           Removed deprecated argument: options

        .. versionadded:: 2.1
           uuid_subtype attribute

        .. mongodoc:: collections
        """
        super(Collection, self).__init__(codec_options or database.codec_options, read_preference or database.read_preference, write_concern or database.write_concern, read_concern or database.read_concern)
        if not isinstance(name, string_type):
            raise TypeError('name must be an instance of %s' % (
             string_type.__name__,))
        if not name or '..' in name:
            raise InvalidName('collection names cannot be empty')
        if '$' in name:
            if not name.startswith('oplog.$main'):
                if not name.startswith('$cmd'):
                    raise InvalidName("collection names must not contain '$': %r" % name)
        if name[0] == '.' or name[(-1)] == '.':
            raise InvalidName("collection names must not start or end with '.': %r" % name)
        if '\x00' in name:
            raise InvalidName('collection names must not contain the null character')
        collation = validate_collation_or_none(kwargs.pop('collation', None))
        self._Collection__database = database
        self._Collection__name = _unicode(name)
        self._Collection__full_name = _UJOIN % (self._Collection__database.name, self._Collection__name)
        if create or kwargs or collation:
            self._Collection__create(kwargs, collation, session)
        self._Collection__write_response_codec_options = self.codec_options._replace(unicode_decode_error_handler='replace',
          document_class=dict)

    def _socket_for_reads(self, session):
        return self._Collection__database.client._socket_for_reads(self._read_preference_for(session), session)

    def _socket_for_writes(self, session):
        return self._Collection__database.client._socket_for_writes(session)

    def _command--- This code section failed: ---

 L. 234         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _Collection__database
                4  LOAD_ATTR                client
                6  LOAD_METHOD              _tmp_session
                8  LOAD_FAST                'session'
               10  CALL_METHOD_1         1  ''
               12  SETUP_WITH           92  'to 92'
               14  STORE_FAST               's'

 L. 235        16  LOAD_FAST                'sock_info'
               18  LOAD_ATTR                command

 L. 236        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _Collection__database
               24  LOAD_ATTR                name

 L. 237        26  LOAD_FAST                'command'

 L. 238        28  LOAD_FAST                'slave_ok'

 L. 239        30  LOAD_FAST                'read_preference'
               32  JUMP_IF_TRUE_OR_POP    42  'to 42'
               34  LOAD_FAST                'self'
               36  LOAD_METHOD              _read_preference_for
               38  LOAD_FAST                'session'
               40  CALL_METHOD_1         1  ''
             42_0  COME_FROM            32  '32'

 L. 240        42  LOAD_FAST                'codec_options'
               44  JUMP_IF_TRUE_OR_POP    50  'to 50'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                codec_options
             50_0  COME_FROM            44  '44'

 L. 241        50  LOAD_FAST                'check'

 L. 242        52  LOAD_FAST                'allowable_errors'

 L. 243        54  LOAD_FAST                'read_concern'

 L. 244        56  LOAD_FAST                'write_concern'

 L. 245        58  LOAD_CONST               True

 L. 246        60  LOAD_FAST                'collation'

 L. 247        62  LOAD_FAST                's'

 L. 248        64  LOAD_FAST                'self'
               66  LOAD_ATTR                _Collection__database
               68  LOAD_ATTR                client

 L. 249        70  LOAD_FAST                'retryable_write'

 L. 250        72  LOAD_FAST                'user_fields'

 L. 235        74  LOAD_CONST               ('read_concern', 'write_concern', 'parse_write_concern_error', 'collation', 'session', 'client', 'retryable_write', 'user_fields')
               76  CALL_FUNCTION_KW_15    15  '15 total positional and keyword args'
               78  POP_BLOCK        
               80  ROT_TWO          
               82  BEGIN_FINALLY    
               84  WITH_CLEANUP_START
               86  WITH_CLEANUP_FINISH
               88  POP_FINALLY           0  ''
               90  RETURN_VALUE     
             92_0  COME_FROM_WITH       12  '12'
               92  WITH_CLEANUP_START
               94  WITH_CLEANUP_FINISH
               96  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 80

    def __create(self, options, collation, session):
        """Sends a create command with the given options.
        """
        cmd = SON([('create', self._Collection__name)])
        if options:
            if 'size' in options:
                options['size'] = float(options['size'])
            cmd.update(options)
        with self._socket_for_writes(session) as (sock_info):
            self._command(sock_info,
              cmd, read_preference=(ReadPreference.PRIMARY), write_concern=(self._write_concern_for(session)),
              collation=collation,
              session=session)

    def __getattr__(self, name):
        """Get a sub-collection of this collection by name.

        Raises InvalidName if an invalid collection name is used.

        :Parameters:
          - `name`: the name of the collection to get
        """
        if name.startswith('_'):
            full_name = _UJOIN % (self._Collection__name, name)
            raise AttributeError("Collection has no attribute %r. To access the %s collection, use database['%s']." % (
             name, full_name, full_name))
        return self.__getitem__(name)

    def __getitem__(self, name):
        return Collection(self._Collection__database, _UJOIN % (self._Collection__name, name), False, self.codec_options, self.read_preference, self.write_concern, self.read_concern)

    def __repr__(self):
        return 'Collection(%r, %r)' % (self._Collection__database, self._Collection__name)

    def __eq__(self, other):
        if isinstance(other, Collection):
            return self._Collection__database == other.database and self._Collection__name == other.name
        return NotImplemented

    def __ne__(self, other):
        return not self == other

    @property
    def full_name(self):
        """The full name of this :class:`Collection`.

        The full name is of the form `database_name.collection_name`.
        """
        return self._Collection__full_name

    @property
    def name(self):
        """The name of this :class:`Collection`."""
        return self._Collection__name

    @property
    def database(self):
        """The :class:`~pymongo.database.Database` that this
        :class:`Collection` is a part of.
        """
        return self._Collection__database

    def with_options(self, codec_options=None, read_preference=None, write_concern=None, read_concern=None):
        """Get a clone of this collection changing the specified settings.

          >>> coll1.read_preference
          Primary()
          >>> from pymongo import ReadPreference
          >>> coll2 = coll1.with_options(read_preference=ReadPreference.SECONDARY)
          >>> coll1.read_preference
          Primary()
          >>> coll2.read_preference
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
        """
        return Collection(self._Collection__database, self._Collection__name, False, codec_options or self.codec_options, read_preference or self.read_preference, write_concern or self.write_concern, read_concern or self.read_concern)

    def initialize_unordered_bulk_op(self, bypass_document_validation=False):
        """**DEPRECATED** - Initialize an unordered batch of write operations.

        Operations will be performed on the server in arbitrary order,
        possibly in parallel. All operations will be attempted.

        :Parameters:
          - `bypass_document_validation`: (optional) If ``True``, allows the
            write to opt-out of document level validation. Default is
            ``False``.

        Returns a :class:`~pymongo.bulk.BulkOperationBuilder` instance.

        See :ref:`unordered_bulk` for examples.

        .. note:: `bypass_document_validation` requires server version
          **>= 3.2**

        .. versionchanged:: 3.5
           Deprecated. Use :meth:`~pymongo.collection.Collection.bulk_write`
           instead.

        .. versionchanged:: 3.2
           Added bypass_document_validation support

        .. versionadded:: 2.7
        """
        warnings.warn('initialize_unordered_bulk_op is deprecated', DeprecationWarning,
          stacklevel=2)
        return BulkOperationBuilder(self, False, bypass_document_validation)

    def initialize_ordered_bulk_op(self, bypass_document_validation=False):
        """**DEPRECATED** - Initialize an ordered batch of write operations.

        Operations will be performed on the server serially, in the
        order provided. If an error occurs all remaining operations
        are aborted.

        :Parameters:
          - `bypass_document_validation`: (optional) If ``True``, allows the
            write to opt-out of document level validation. Default is
            ``False``.

        Returns a :class:`~pymongo.bulk.BulkOperationBuilder` instance.

        See :ref:`ordered_bulk` for examples.

        .. note:: `bypass_document_validation` requires server version
          **>= 3.2**

        .. versionchanged:: 3.5
           Deprecated. Use :meth:`~pymongo.collection.Collection.bulk_write`
           instead.

        .. versionchanged:: 3.2
           Added bypass_document_validation support

        .. versionadded:: 2.7
        """
        warnings.warn('initialize_ordered_bulk_op is deprecated', DeprecationWarning,
          stacklevel=2)
        return BulkOperationBuilder(self, True, bypass_document_validation)

    def bulk_write(self, requests, ordered=True, bypass_document_validation=False, session=None):
        """Send a batch of write operations to the server.

        Requests are passed as a list of write operation instances (
        :class:`~pymongo.operations.InsertOne`,
        :class:`~pymongo.operations.UpdateOne`,
        :class:`~pymongo.operations.UpdateMany`,
        :class:`~pymongo.operations.ReplaceOne`,
        :class:`~pymongo.operations.DeleteOne`, or
        :class:`~pymongo.operations.DeleteMany`).

          >>> for doc in db.test.find({}):
          ...     print(doc)
          ...
          {u'x': 1, u'_id': ObjectId('54f62e60fba5226811f634ef')}
          {u'x': 1, u'_id': ObjectId('54f62e60fba5226811f634f0')}
          >>> # DeleteMany, UpdateOne, and UpdateMany are also available.
          ...
          >>> from pymongo import InsertOne, DeleteOne, ReplaceOne
          >>> requests = [InsertOne({'y': 1}), DeleteOne({'x': 1}),
          ...             ReplaceOne({'w': 1}, {'z': 1}, upsert=True)]
          >>> result = db.test.bulk_write(requests)
          >>> result.inserted_count
          1
          >>> result.deleted_count
          1
          >>> result.modified_count
          0
          >>> result.upserted_ids
          {2: ObjectId('54f62ee28891e756a6e1abd5')}
          >>> for doc in db.test.find({}):
          ...     print(doc)
          ...
          {u'x': 1, u'_id': ObjectId('54f62e60fba5226811f634f0')}
          {u'y': 1, u'_id': ObjectId('54f62ee2fba5226811f634f1')}
          {u'z': 1, u'_id': ObjectId('54f62ee28891e756a6e1abd5')}

        :Parameters:
          - `requests`: A list of write operations (see examples above).
          - `ordered` (optional): If ``True`` (the default) requests will be
            performed on the server serially, in the order provided. If an error
            occurs all remaining operations are aborted. If ``False`` requests
            will be performed on the server in arbitrary order, possibly in
            parallel, and all operations will be attempted.
          - `bypass_document_validation`: (optional) If ``True``, allows the
            write to opt-out of document level validation. Default is
            ``False``.
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.

        :Returns:
          An instance of :class:`~pymongo.results.BulkWriteResult`.

        .. seealso:: :ref:`writes-and-ids`

        .. note:: `bypass_document_validation` requires server version
          **>= 3.2**

        .. versionchanged:: 3.6
           Added ``session`` parameter.

        .. versionchanged:: 3.2
          Added bypass_document_validation support

        .. versionadded:: 3.0
        """
        common.validate_list('requests', requests)
        blk = _Bulk(self, ordered, bypass_document_validation)
        for request in requests:
            try:
                request._add_to_bulk(blk)
            except AttributeError:
                raise TypeError('%r is not a valid request' % (request,))

        else:
            write_concern = self._write_concern_for(session)
            bulk_api_result = blk.execute(write_concern, session)
            if bulk_api_result is not None:
                return BulkWriteResult(bulk_api_result, True)
            return BulkWriteResult({}, False)

    def _legacy_write(self, sock_info, name, cmd, op_id, bypass_doc_val, func, *args):
        """Internal legacy unacknowledged write helper."""
        if bypass_doc_val:
            if sock_info.max_wire_version >= 4:
                raise OperationFailure('Cannot set bypass_document_validation with unacknowledged write concern')
        listeners = self.database.client._event_listeners
        publish = listeners.enabled_for_commands
        if publish:
            start = datetime.datetime.now()
        args = args + (sock_info.compression_context,)
        rqst_id, msg, max_size = func(*args)
        if publish:
            duration = datetime.datetime.now() - start
            listeners.publish_command_start(cmd, self._Collection__database.name, rqst_id, sock_info.address, op_id)
            start = datetime.datetime.now()
        try:
            result = sock_info.legacy_write(rqst_id, msg, max_size, False)
        except Exception as exc:
            try:
                if publish:
                    dur = datetime.datetime.now() - start + duration
                    if isinstance(exc, OperationFailure):
                        details = exc.details
                        if details.get('ok') and 'n' in details:
                            reply = message._convert_write_result(name, cmd, details)
                            listeners.publish_command_success(dur, reply, name, rqst_id, sock_info.address, op_id)
                            raise
                    else:
                        details = message._convert_exception(exc)
                    listeners.publish_command_failure(dur, details, name, rqst_id, sock_info.address, op_id)
                raise
            finally:
                exc = None
                del exc

        else:
            if publish:
                if result is not None:
                    reply = message._convert_write_result(name, cmd, result)
                else:
                    reply = {'ok': 1}
                duration = datetime.datetime.now() - start + duration
                listeners.publish_command_success(duration, reply, name, rqst_id, sock_info.address, op_id)
            return result

    def _insert_one(self, doc, ordered, check_keys, manipulate, write_concern, op_id, bypass_doc_val, session):
        """Internal helper for inserting a single document."""
        if manipulate:
            doc = self._Collection__database._apply_incoming_manipulators(doc, self)
            if not isinstance(doc, RawBSONDocument):
                if '_id' not in doc:
                    doc['_id'] = ObjectId()
            doc = self._Collection__database._apply_incoming_copying_manipulators(doc, self)
        else:
            write_concern = write_concern or self.write_concern
            acknowledged = write_concern.acknowledged
            command = SON([('insert', self.name),
             (
              'ordered', ordered),
             (
              'documents', [doc])])
            if not write_concern.is_server_default:
                command['writeConcern'] = write_concern.document

            def _insert_command(session, sock_info, retryable_write):
                if not sock_info.op_msg_enabled:
                    if not acknowledged:
                        return self._legacy_write(sock_info, 'insert', command, op_id, bypass_doc_val, message.insert, self._Collection__full_name, [
                         doc], check_keys, False, write_concern.document, False, self._Collection__write_response_codec_options)
                if bypass_doc_val:
                    if sock_info.max_wire_version >= 4:
                        command['bypassDocumentValidation'] = True
                result = sock_info.command((self._Collection__database.name),
                  command,
                  write_concern=write_concern,
                  codec_options=(self._Collection__write_response_codec_options),
                  check_keys=check_keys,
                  session=session,
                  client=(self._Collection__database.client),
                  retryable_write=retryable_write)
                _check_write_command_response(result)

            self._Collection__database.client._retryable_write(acknowledged, _insert_command, session)
            return isinstance(doc, RawBSONDocument) or doc.get('_id')

    def _insert(self, docs, ordered=True, check_keys=True, manipulate=False, write_concern=None, op_id=None, bypass_doc_val=False, session=None):
        """Internal insert helper."""
        if isinstance(docs, abc.Mapping):
            return self._insert_one(docs, ordered, check_keys, manipulate, write_concern, op_id, bypass_doc_val, session)
        else:
            ids = []
            if manipulate:

                def gen():
                    _db = self._Collection__database
                    for doc in docs:
                        doc = _db._apply_incoming_manipulators(doc, self)
                        if not isinstance(doc, RawBSONDocument):
                            if not '_id' in doc:
                                doc['_id'] = ObjectId()
                        doc = _db._apply_incoming_copying_manipulators(doc, self)
                        ids.append(doc['_id'])
                        (yield doc)

            else:

                def gen():
                    for doc in docs:
                        if not isinstance(doc, RawBSONDocument):
                            ids.append(doc.get('_id'))
                        (yield doc)

        write_concern = write_concern or self._write_concern_for(session)
        blk = _Bulk(self, ordered, bypass_doc_val)
        blk.ops = [(message._INSERT, doc) for doc in gen()]
        try:
            blk.execute(write_concern, session=session)
        except BulkWriteError as bwe:
            try:
                _raise_last_error(bwe.details)
            finally:
                bwe = None
                del bwe

        else:
            return ids

    def insert_one(self, document, bypass_document_validation=False, session=None):
        """Insert a single document.

          >>> db.test.count_documents({'x': 1})
          0
          >>> result = db.test.insert_one({'x': 1})
          >>> result.inserted_id
          ObjectId('54f112defba522406c9cc208')
          >>> db.test.find_one({'x': 1})
          {u'x': 1, u'_id': ObjectId('54f112defba522406c9cc208')}

        :Parameters:
          - `document`: The document to insert. Must be a mutable mapping
            type. If the document does not have an _id field one will be
            added automatically.
          - `bypass_document_validation`: (optional) If ``True``, allows the
            write to opt-out of document level validation. Default is
            ``False``.
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.

        :Returns:
          - An instance of :class:`~pymongo.results.InsertOneResult`.

        .. seealso:: :ref:`writes-and-ids`

        .. note:: `bypass_document_validation` requires server version
          **>= 3.2**

        .. versionchanged:: 3.6
           Added ``session`` parameter.

        .. versionchanged:: 3.2
          Added bypass_document_validation support

        .. versionadded:: 3.0
        """
        common.validate_is_document_type('document', document)
        if not isinstance(document, RawBSONDocument):
            if not '_id' in document:
                document['_id'] = ObjectId()
        write_concern = self._write_concern_for(session)
        return InsertOneResult(self._insert(document, write_concern=write_concern,
          bypass_doc_val=bypass_document_validation,
          session=session), write_concern.acknowledged)

    def insert_many(self, documents, ordered=True, bypass_document_validation=False, session=None):
        """Insert an iterable of documents.

          >>> db.test.count_documents({})
          0
          >>> result = db.test.insert_many([{'x': i} for i in range(2)])
          >>> result.inserted_ids
          [ObjectId('54f113fffba522406c9cc20e'), ObjectId('54f113fffba522406c9cc20f')]
          >>> db.test.count_documents({})
          2

        :Parameters:
          - `documents`: A iterable of documents to insert.
          - `ordered` (optional): If ``True`` (the default) documents will be
            inserted on the server serially, in the order provided. If an error
            occurs all remaining inserts are aborted. If ``False``, documents
            will be inserted on the server in arbitrary order, possibly in
            parallel, and all document inserts will be attempted.
          - `bypass_document_validation`: (optional) If ``True``, allows the
            write to opt-out of document level validation. Default is
            ``False``.
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.

        :Returns:
          An instance of :class:`~pymongo.results.InsertManyResult`.

        .. seealso:: :ref:`writes-and-ids`

        .. note:: `bypass_document_validation` requires server version
          **>= 3.2**

        .. versionchanged:: 3.6
           Added ``session`` parameter.

        .. versionchanged:: 3.2
          Added bypass_document_validation support

        .. versionadded:: 3.0
        """
        if not (isinstance(documents, abc.Iterable) and documents):
            raise TypeError('documents must be a non-empty list')
        inserted_ids = []

        def gen():
            for document in documents:
                common.validate_is_document_type('document', document)
                if not isinstance(document, RawBSONDocument):
                    if '_id' not in document:
                        document['_id'] = ObjectId()
                    inserted_ids.append(document['_id'])
                (yield (
                 message._INSERT, document))

        write_concern = self._write_concern_for(session)
        blk = _Bulk(self, ordered, bypass_document_validation)
        blk.ops = [doc for doc in gen()]
        blk.execute(write_concern, session=session)
        return InsertManyResult(inserted_ids, write_concern.acknowledged)

    def _update(self, sock_info, criteria, document, upsert=False, check_keys=True, multi=False, manipulate=False, write_concern=None, op_id=None, ordered=True, bypass_doc_val=False, collation=None, array_filters=None, session=None, retryable_write=False):
        """Internal update / replace helper."""
        common.validate_boolean('upsert', upsert)
        if manipulate:
            document = self._Collection__database._fix_incoming(document, self)
        else:
            collation = validate_collation_or_none(collation)
            write_concern = write_concern or self.write_concern
            acknowledged = write_concern.acknowledged
            update_doc = SON([('q', criteria),
             (
              'u', document),
             (
              'multi', multi),
             (
              'upsert', upsert)])
            if collation is not None:
                if sock_info.max_wire_version < 5:
                    raise ConfigurationError('Must be connected to MongoDB 3.4+ to use collations.')
                else:
                    if not acknowledged:
                        raise ConfigurationError('Collation is unsupported for unacknowledged writes.')
                    else:
                        update_doc['collation'] = collation
            if array_filters is not None:
                if sock_info.max_wire_version < 6:
                    raise ConfigurationError('Must be connected to MongoDB 3.6+ to use array_filters.')
                else:
                    assert acknowledged, 'arrayFilters is unsupported for unacknowledged writes.'
            else:
                update_doc['arrayFilters'] = array_filters
        command = SON([('update', self.name),
         (
          'ordered', ordered),
         (
          'updates', [update_doc])])
        if not write_concern.is_server_default:
            command['writeConcern'] = write_concern.document
        if not sock_info.op_msg_enabled:
            if not acknowledged:
                return self._legacy_write(sock_info, 'update', command, op_id, bypass_doc_val, message.update, self._Collection__full_name, upsert, multi, criteria, document, False, write_concern.document, check_keys, self._Collection__write_response_codec_options)
        if bypass_doc_val:
            if sock_info.max_wire_version >= 4:
                command['bypassDocumentValidation'] = True
        result = sock_info.command((self._Collection__database.name),
          command,
          write_concern=write_concern,
          codec_options=(self._Collection__write_response_codec_options),
          session=session,
          client=(self._Collection__database.client),
          retryable_write=retryable_write).copy()
        _check_write_command_response(result)
        if result.get('n') and 'upserted' not in result:
            result['updatedExisting'] = True
        else:
            result['updatedExisting'] = False
            if 'upserted' in result:
                result['upserted'] = result['upserted'][0]['_id']
            if not acknowledged:
                return
            return result

    def _update_retryable(self, criteria, document, upsert=False, check_keys=True, multi=False, manipulate=False, write_concern=None, op_id=None, ordered=True, bypass_doc_val=False, collation=None, array_filters=None, session=None):
        """Internal update / replace helper."""

        def _update(session, sock_info, retryable_write):
            return self._update(sock_info,
              criteria, document, upsert=upsert, check_keys=check_keys,
              multi=multi,
              manipulate=manipulate,
              write_concern=write_concern,
              op_id=op_id,
              ordered=ordered,
              bypass_doc_val=bypass_doc_val,
              collation=collation,
              array_filters=array_filters,
              session=session,
              retryable_write=retryable_write)

        return self._Collection__database.client._retryable_write((write_concern or self.write_concern).acknowledged and not multi, _update, session)

    def replace_one(self, filter, replacement, upsert=False, bypass_document_validation=False, collation=None, session=None):
        """Replace a single document matching the filter.

          >>> for doc in db.test.find({}):
          ...     print(doc)
          ...
          {u'x': 1, u'_id': ObjectId('54f4c5befba5220aa4d6dee7')}
          >>> result = db.test.replace_one({'x': 1}, {'y': 1})
          >>> result.matched_count
          1
          >>> result.modified_count
          1
          >>> for doc in db.test.find({}):
          ...     print(doc)
          ...
          {u'y': 1, u'_id': ObjectId('54f4c5befba5220aa4d6dee7')}

        The *upsert* option can be used to insert a new document if a matching
        document does not exist.

          >>> result = db.test.replace_one({'x': 1}, {'x': 1}, True)
          >>> result.matched_count
          0
          >>> result.modified_count
          0
          >>> result.upserted_id
          ObjectId('54f11e5c8891e756a6e1abd4')
          >>> db.test.find_one({'x': 1})
          {u'x': 1, u'_id': ObjectId('54f11e5c8891e756a6e1abd4')}

        :Parameters:
          - `filter`: A query that matches the document to replace.
          - `replacement`: The new document.
          - `upsert` (optional): If ``True``, perform an insert if no documents
            match the filter.
          - `bypass_document_validation`: (optional) If ``True``, allows the
            write to opt-out of document level validation. Default is
            ``False``.
          - `collation` (optional): An instance of
            :class:`~pymongo.collation.Collation`. This option is only supported
            on MongoDB 3.4 and above.
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.

        :Returns:
          - An instance of :class:`~pymongo.results.UpdateResult`.

        .. note:: `bypass_document_validation` requires server version
          **>= 3.2**

        .. versionchanged:: 3.6
           Added ``session`` parameter.

        .. versionchanged:: 3.4
          Added the `collation` option.

        .. versionchanged:: 3.2
          Added bypass_document_validation support

        .. versionadded:: 3.0
        """
        common.validate_is_mapping('filter', filter)
        common.validate_ok_for_replace(replacement)
        write_concern = self._write_concern_for(session)
        return UpdateResult(self._update_retryable(filter,
          replacement, upsert, write_concern=write_concern,
          bypass_doc_val=bypass_document_validation,
          collation=collation,
          session=session), write_concern.acknowledged)

    def update_one(self, filter, update, upsert=False, bypass_document_validation=False, collation=None, array_filters=None, session=None):
        """Update a single document matching the filter.

          >>> for doc in db.test.find():
          ...     print(doc)
          ...
          {u'x': 1, u'_id': 0}
          {u'x': 1, u'_id': 1}
          {u'x': 1, u'_id': 2}
          >>> result = db.test.update_one({'x': 1}, {'$inc': {'x': 3}})
          >>> result.matched_count
          1
          >>> result.modified_count
          1
          >>> for doc in db.test.find():
          ...     print(doc)
          ...
          {u'x': 4, u'_id': 0}
          {u'x': 1, u'_id': 1}
          {u'x': 1, u'_id': 2}

        :Parameters:
          - `filter`: A query that matches the document to update.
          - `update`: The modifications to apply.
          - `upsert` (optional): If ``True``, perform an insert if no documents
            match the filter.
          - `bypass_document_validation`: (optional) If ``True``, allows the
            write to opt-out of document level validation. Default is
            ``False``.
          - `collation` (optional): An instance of
            :class:`~pymongo.collation.Collation`. This option is only supported
            on MongoDB 3.4 and above.
          - `array_filters` (optional): A list of filters specifying which
            array elements an update should apply. Requires MongoDB 3.6+.
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.

        :Returns:
          - An instance of :class:`~pymongo.results.UpdateResult`.

        .. note:: `bypass_document_validation` requires server version
          **>= 3.2**

        .. versionchanged:: 3.9
           Added the ability to accept a pipeline as the `update`.

        .. versionchanged:: 3.6
           Added the `array_filters` and ``session`` parameters.

        .. versionchanged:: 3.4
          Added the `collation` option.

        .. versionchanged:: 3.2
          Added bypass_document_validation support

        .. versionadded:: 3.0
        """
        common.validate_is_mapping('filter', filter)
        common.validate_ok_for_update(update)
        common.validate_list_or_none('array_filters', array_filters)
        write_concern = self._write_concern_for(session)
        return UpdateResult(self._update_retryable(filter,
          update, upsert, check_keys=False, write_concern=write_concern,
          bypass_doc_val=bypass_document_validation,
          collation=collation,
          array_filters=array_filters,
          session=session), write_concern.acknowledged)

    def update_many(self, filter, update, upsert=False, array_filters=None, bypass_document_validation=False, collation=None, session=None):
        """Update one or more documents that match the filter.

          >>> for doc in db.test.find():
          ...     print(doc)
          ...
          {u'x': 1, u'_id': 0}
          {u'x': 1, u'_id': 1}
          {u'x': 1, u'_id': 2}
          >>> result = db.test.update_many({'x': 1}, {'$inc': {'x': 3}})
          >>> result.matched_count
          3
          >>> result.modified_count
          3
          >>> for doc in db.test.find():
          ...     print(doc)
          ...
          {u'x': 4, u'_id': 0}
          {u'x': 4, u'_id': 1}
          {u'x': 4, u'_id': 2}

        :Parameters:
          - `filter`: A query that matches the documents to update.
          - `update`: The modifications to apply.
          - `upsert` (optional): If ``True``, perform an insert if no documents
            match the filter.
          - `bypass_document_validation` (optional): If ``True``, allows the
            write to opt-out of document level validation. Default is
            ``False``.
          - `collation` (optional): An instance of
            :class:`~pymongo.collation.Collation`. This option is only supported
            on MongoDB 3.4 and above.
          - `array_filters` (optional): A list of filters specifying which
            array elements an update should apply. Requires MongoDB 3.6+.
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.

        :Returns:
          - An instance of :class:`~pymongo.results.UpdateResult`.

        .. note:: `bypass_document_validation` requires server version
          **>= 3.2**

        .. versionchanged:: 3.9
           Added the ability to accept a pipeline as the `update`.

        .. versionchanged:: 3.6
           Added ``array_filters`` and ``session`` parameters.

        .. versionchanged:: 3.4
          Added the `collation` option.

        .. versionchanged:: 3.2
          Added bypass_document_validation support

        .. versionadded:: 3.0
        """
        common.validate_is_mapping('filter', filter)
        common.validate_ok_for_update(update)
        common.validate_list_or_none('array_filters', array_filters)
        write_concern = self._write_concern_for(session)
        return UpdateResult(self._update_retryable(filter,
          update, upsert, check_keys=False, multi=True, write_concern=write_concern,
          bypass_doc_val=bypass_document_validation,
          collation=collation,
          array_filters=array_filters,
          session=session), write_concern.acknowledged)

    def drop(self, session=None):
        """Alias for :meth:`~pymongo.database.Database.drop_collection`.

        :Parameters:
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.

        The following two calls are equivalent:

          >>> db.foo.drop()
          >>> db.drop_collection("foo")

        .. versionchanged:: 3.7
           :meth:`drop` now respects this :class:`Collection`'s :attr:`write_concern`.

        .. versionchanged:: 3.6
           Added ``session`` parameter.
        """
        dbo = self._Collection__database.client.get_database(self._Collection__database.name, self.codec_options, self.read_preference, self.write_concern, self.read_concern)
        dbo.drop_collection((self._Collection__name), session=session)

    def _delete(self, sock_info, criteria, multi, write_concern=None, op_id=None, ordered=True, collation=None, session=None, retryable_write=False):
        """Internal delete helper."""
        common.validate_is_mapping('filter', criteria)
        write_concern = write_concern or self.write_concern
        acknowledged = write_concern.acknowledged
        delete_doc = SON([('q', criteria),
         (
          'limit', int(not multi))])
        collation = validate_collation_or_none(collation)
        if collation is not None:
            if sock_info.max_wire_version < 5:
                raise ConfigurationError('Must be connected to MongoDB 3.4+ to use collations.')
            else:
                if not acknowledged:
                    raise ConfigurationError('Collation is unsupported for unacknowledged writes.')
                else:
                    delete_doc['collation'] = collation
        command = SON([('delete', self.name),
         (
          'ordered', ordered),
         (
          'deletes', [delete_doc])])
        if not write_concern.is_server_default:
            command['writeConcern'] = write_concern.document
        if not sock_info.op_msg_enabled:
            if not acknowledged:
                return self._legacy_write(sock_info, 'delete', command, op_id, False, message.delete, self._Collection__full_name, criteria, False, write_concern.document, self._Collection__write_response_codec_options, int(not multi))
        result = sock_info.command((self._Collection__database.name),
          command,
          write_concern=write_concern,
          codec_options=(self._Collection__write_response_codec_options),
          session=session,
          client=(self._Collection__database.client),
          retryable_write=retryable_write)
        _check_write_command_response(result)
        return result

    def _delete_retryable(self, criteria, multi, write_concern=None, op_id=None, ordered=True, collation=None, session=None):
        """Internal delete helper."""

        def _delete(session, sock_info, retryable_write):
            return self._delete(sock_info,
              criteria, multi, write_concern=write_concern,
              op_id=op_id,
              ordered=ordered,
              collation=collation,
              session=session,
              retryable_write=retryable_write)

        return self._Collection__database.client._retryable_write((write_concern or self.write_concern).acknowledged and not multi, _delete, session)

    def delete_one(self, filter, collation=None, session=None):
        """Delete a single document matching the filter.

          >>> db.test.count_documents({'x': 1})
          3
          >>> result = db.test.delete_one({'x': 1})
          >>> result.deleted_count
          1
          >>> db.test.count_documents({'x': 1})
          2

        :Parameters:
          - `filter`: A query that matches the document to delete.
          - `collation` (optional): An instance of
            :class:`~pymongo.collation.Collation`. This option is only supported
            on MongoDB 3.4 and above.
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.

        :Returns:
          - An instance of :class:`~pymongo.results.DeleteResult`.

        .. versionchanged:: 3.6
           Added ``session`` parameter.

        .. versionchanged:: 3.4
          Added the `collation` option.

        .. versionadded:: 3.0
        """
        write_concern = self._write_concern_for(session)
        return DeleteResult(self._delete_retryable(filter,
          False, write_concern=write_concern,
          collation=collation,
          session=session), write_concern.acknowledged)

    def delete_many(self, filter, collation=None, session=None):
        """Delete one or more documents matching the filter.

          >>> db.test.count_documents({'x': 1})
          3
          >>> result = db.test.delete_many({'x': 1})
          >>> result.deleted_count
          3
          >>> db.test.count_documents({'x': 1})
          0

        :Parameters:
          - `filter`: A query that matches the documents to delete.
          - `collation` (optional): An instance of
            :class:`~pymongo.collation.Collation`. This option is only supported
            on MongoDB 3.4 and above.
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.

        :Returns:
          - An instance of :class:`~pymongo.results.DeleteResult`.

        .. versionchanged:: 3.6
           Added ``session`` parameter.

        .. versionchanged:: 3.4
          Added the `collation` option.

        .. versionadded:: 3.0
        """
        write_concern = self._write_concern_for(session)
        return DeleteResult(self._delete_retryable(filter,
          True, write_concern=write_concern,
          collation=collation,
          session=session), write_concern.acknowledged)

    def find_one(self, filter=None, *args, **kwargs):
        """Get a single document from the database.

        All arguments to :meth:`find` are also valid arguments for
        :meth:`find_one`, although any `limit` argument will be
        ignored. Returns a single document, or ``None`` if no matching
        document is found.

        The :meth:`find_one` method obeys the :attr:`read_preference` of
        this :class:`Collection`.

        :Parameters:

          - `filter` (optional): a dictionary specifying
            the query to be performed OR any other type to be used as
            the value for a query for ``"_id"``.

          - `*args` (optional): any additional positional arguments
            are the same as the arguments to :meth:`find`.

          - `**kwargs` (optional): any additional keyword arguments
            are the same as the arguments to :meth:`find`.

              >>> collection.find_one(max_time_ms=100)
        """
        if filter is not None:
            if not isinstance(filter, abc.Mapping):
                filter = {'_id': filter}
        cursor = (self.find)(filter, *args, **kwargs)
        for result in cursor.limit(-1):
            return result

    def find(self, *args, **kwargs):
        """Query the database.

        The `filter` argument is a prototype document that all results
        must match. For example:

        >>> db.test.find({"hello": "world"})

        only matches documents that have a key "hello" with value
        "world".  Matches can have other keys *in addition* to
        "hello". The `projection` argument is used to specify a subset
        of fields that should be included in the result documents. By
        limiting results to a certain subset of fields you can cut
        down on network traffic and decoding time.

        Raises :class:`TypeError` if any of the arguments are of
        improper type. Returns an instance of
        :class:`~pymongo.cursor.Cursor` corresponding to this query.

        The :meth:`find` method obeys the :attr:`read_preference` of
        this :class:`Collection`.

        :Parameters:
          - `filter` (optional): a SON object specifying elements which
            must be present for a document to be included in the
            result set
          - `projection` (optional): a list of field names that should be
            returned in the result set or a dict specifying the fields
            to include or exclude. If `projection` is a list "_id" will
            always be returned. Use a dict to exclude fields from
            the result (e.g. projection={'_id': False}).
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.
          - `skip` (optional): the number of documents to omit (from
            the start of the result set) when returning the results
          - `limit` (optional): the maximum number of results to
            return. A limit of 0 (the default) is equivalent to setting no
            limit.
          - `no_cursor_timeout` (optional): if False (the default), any
            returned cursor is closed by the server after 10 minutes of
            inactivity. If set to True, the returned cursor will never
            time out on the server. Care should be taken to ensure that
            cursors with no_cursor_timeout turned on are properly closed.
          - `cursor_type` (optional): the type of cursor to return. The valid
            options are defined by :class:`~pymongo.cursor.CursorType`:

            - :attr:`~pymongo.cursor.CursorType.NON_TAILABLE` - the result of
              this find call will return a standard cursor over the result set.
            - :attr:`~pymongo.cursor.CursorType.TAILABLE` - the result of this
              find call will be a tailable cursor - tailable cursors are only
              for use with capped collections. They are not closed when the
              last data is retrieved but are kept open and the cursor location
              marks the final document position. If more data is received
              iteration of the cursor will continue from the last document
              received. For details, see the `tailable cursor documentation
              <http://www.mongodb.org/display/DOCS/Tailable+Cursors>`_.
            - :attr:`~pymongo.cursor.CursorType.TAILABLE_AWAIT` - the result
              of this find call will be a tailable cursor with the await flag
              set. The server will wait for a few seconds after returning the
              full result set so that it can capture and return additional data
              added during the query.
            - :attr:`~pymongo.cursor.CursorType.EXHAUST` - the result of this
              find call will be an exhaust cursor. MongoDB will stream batched
              results to the client without waiting for the client to request
              each batch, reducing latency. See notes on compatibility below.

          - `sort` (optional): a list of (key, direction) pairs
            specifying the sort order for this query. See
            :meth:`~pymongo.cursor.Cursor.sort` for details.
          - `allow_partial_results` (optional): if True, mongos will return
            partial results if some shards are down instead of returning an
            error.
          - `oplog_replay` (optional): If True, set the oplogReplay query
            flag.
          - `batch_size` (optional): Limits the number of documents returned in
            a single batch.
          - `manipulate` (optional): **DEPRECATED** - If True (the default),
            apply any outgoing SON manipulators before returning.
          - `collation` (optional): An instance of
            :class:`~pymongo.collation.Collation`. This option is only supported
            on MongoDB 3.4 and above.
          - `return_key` (optional): If True, return only the index keys in
            each document.
          - `show_record_id` (optional): If True, adds a field ``$recordId`` in
            each document with the storage engine's internal record identifier.
          - `snapshot` (optional): **DEPRECATED** - If True, prevents the
            cursor from returning a document more than once because of an
            intervening write operation.
          - `hint` (optional): An index, in the same format as passed to
            :meth:`~pymongo.collection.Collection.create_index` (e.g.
            ``[('field', ASCENDING)]``). Pass this as an alternative to calling
            :meth:`~pymongo.cursor.Cursor.hint` on the cursor to tell Mongo the
            proper index to use for the query.
          - `max_time_ms` (optional): Specifies a time limit for a query
            operation. If the specified time is exceeded, the operation will be
            aborted and :exc:`~pymongo.errors.ExecutionTimeout` is raised. Pass
            this as an alternative to calling
            :meth:`~pymongo.cursor.Cursor.max_time_ms` on the cursor.
          - `max_scan` (optional): **DEPRECATED** - The maximum number of
            documents to scan. Pass this as an alternative to calling
            :meth:`~pymongo.cursor.Cursor.max_scan` on the cursor.
          - `min` (optional): A list of field, limit pairs specifying the
            inclusive lower bound for all keys of a specific index in order.
            Pass this as an alternative to calling
            :meth:`~pymongo.cursor.Cursor.min` on the cursor. ``hint`` must
            also be passed to ensure the query utilizes the correct index.
          - `max` (optional): A list of field, limit pairs specifying the
            exclusive upper bound for all keys of a specific index in order.
            Pass this as an alternative to calling
            :meth:`~pymongo.cursor.Cursor.max` on the cursor. ``hint`` must
            also be passed to ensure the query utilizes the correct index.
          - `comment` (optional): A string to attach to the query to help
            interpret and trace the operation in the server logs and in profile
            data. Pass this as an alternative to calling
            :meth:`~pymongo.cursor.Cursor.comment` on the cursor.
          - `modifiers` (optional): **DEPRECATED** - A dict specifying
            additional MongoDB query modifiers. Use the keyword arguments listed
            above instead.

        .. note:: There are a number of caveats to using
          :attr:`~pymongo.cursor.CursorType.EXHAUST` as cursor_type:

          - The `limit` option can not be used with an exhaust cursor.

          - Exhaust cursors are not supported by mongos and can not be
            used with a sharded cluster.

          - A :class:`~pymongo.cursor.Cursor` instance created with the
            :attr:`~pymongo.cursor.CursorType.EXHAUST` cursor_type requires an
            exclusive :class:`~socket.socket` connection to MongoDB. If the
            :class:`~pymongo.cursor.Cursor` is discarded without being
            completely iterated the underlying :class:`~socket.socket`
            connection will be closed and discarded without being returned to
            the connection pool.

        .. versionchanged:: 3.7
           Deprecated the `snapshot` option, which is deprecated in MongoDB
           3.6 and removed in MongoDB 4.0.
           Deprecated the `max_scan` option. Support for this option is
           deprecated in MongoDB 4.0. Use `max_time_ms` instead to limit server
           side execution time.

        .. versionchanged:: 3.6
           Added ``session`` parameter.

        .. versionchanged:: 3.5
           Added the options `return_key`, `show_record_id`, `snapshot`,
           `hint`, `max_time_ms`, `max_scan`, `min`, `max`, and `comment`.
           Deprecated the option `modifiers`.

        .. versionchanged:: 3.4
           Support the `collation` option.

        .. versionchanged:: 3.0
           Changed the parameter names `spec`, `fields`, `timeout`, and
           `partial` to `filter`, `projection`, `no_cursor_timeout`, and
           `allow_partial_results` respectively.
           Added the `cursor_type`, `oplog_replay`, and `modifiers` options.
           Removed the `network_timeout`, `read_preference`, `tag_sets`,
           `secondary_acceptable_latency_ms`, `max_scan`, `snapshot`,
           `tailable`, `await_data`, `exhaust`, `as_class`, and slave_okay
           parameters. Removed `compile_re` option: PyMongo now always
           represents BSON regular expressions as :class:`~bson.regex.Regex`
           objects. Use :meth:`~bson.regex.Regex.try_compile` to attempt to
           convert from a BSON regular expression to a Python regular
           expression object. Soft deprecated the `manipulate` option.

        .. versionchanged:: 2.7
           Added `compile_re` option. If set to False, PyMongo represented BSON
           regular expressions as :class:`~bson.regex.Regex` objects instead of
           attempting to compile BSON regular expressions as Python native
           regular expressions, thus preventing errors for some incompatible
           patterns, see `PYTHON-500`_.

        .. versionadded:: 2.3
           The `tag_sets` and `secondary_acceptable_latency_ms` parameters.

        .. _PYTHON-500: https://jira.mongodb.org/browse/PYTHON-500

        .. mongodoc:: find

        """
        return Cursor(self, *args, **kwargs)

    def find_raw_batches(self, *args, **kwargs):
        """Query the database and retrieve batches of raw BSON.

        Similar to the :meth:`find` method but returns a
        :class:`~pymongo.cursor.RawBatchCursor`.

        This example demonstrates how to work with raw batches, but in practice
        raw batches should be passed to an external library that can decode
        BSON into another data type, rather than used with PyMongo's
        :mod:`bson` module.

          >>> import bson
          >>> cursor = db.test.find_raw_batches()
          >>> for batch in cursor:
          ...     print(bson.decode_all(batch))

        .. note:: find_raw_batches does not support sessions or auto
           encryption.

        .. versionadded:: 3.6
        """
        if 'session' in kwargs:
            raise ConfigurationError('find_raw_batches does not support sessions')
        if self._Collection__database.client._encrypter:
            raise InvalidOperation('find_raw_batches does not support auto encryption')
        return RawBatchCursor(self, *args, **kwargs)

    def parallel_scan(self, num_cursors, session=None, **kwargs):
        """**DEPRECATED**: Scan this entire collection in parallel.

        Returns a list of up to ``num_cursors`` cursors that can be iterated
        concurrently. As long as the collection is not modified during
        scanning, each document appears once in one of the cursors result
        sets.

        For example, to process each document in a collection using some
        thread-safe ``process_document()`` function:

          >>> def process_cursor(cursor):
          ...     for document in cursor:
          ...     # Some thread-safe processing function:
          ...     process_document(document)
          >>>
          >>> # Get up to 4 cursors.
          ...
          >>> cursors = collection.parallel_scan(4)
          >>> threads = [
          ...     threading.Thread(target=process_cursor, args=(cursor,))
          ...     for cursor in cursors]
          >>>
          >>> for thread in threads:
          ...     thread.start()
          >>>
          >>> for thread in threads:
          ...     thread.join()
          >>>
          >>> # All documents have now been processed.

        The :meth:`parallel_scan` method obeys the :attr:`read_preference` of
        this :class:`Collection`.

        :Parameters:
          - `num_cursors`: the number of cursors to return
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.
          - `**kwargs`: additional options for the parallelCollectionScan
            command can be passed as keyword arguments.

        .. note:: Requires server version **>= 2.5.5**.

        .. versionchanged:: 3.7
           Deprecated.

        .. versionchanged:: 3.6
           Added ``session`` parameter.

        .. versionchanged:: 3.4
           Added back support for arbitrary keyword arguments. MongoDB 3.4
           adds support for maxTimeMS as an option to the
           parallelCollectionScan command.

        .. versionchanged:: 3.0
           Removed support for arbitrary keyword arguments, since
           the parallelCollectionScan command has no optional arguments.
        """
        warnings.warn('parallel_scan is deprecated. MongoDB 4.2 will remove the parallelCollectionScan command.', DeprecationWarning,
          stacklevel=2)
        cmd = SON([('parallelCollectionScan', self._Collection__name),
         (
          'numCursors', num_cursors)])
        cmd.update(kwargs)
        with self._socket_for_reads(session) as (sock_info, slave_ok):
            result = sock_info.command((self._Collection__database.name),
              cmd,
              slave_ok,
              (self._read_preference_for(session)),
              (self.codec_options),
              read_concern=(self.read_concern),
              parse_write_concern_error=True,
              session=session,
              client=(self._Collection__database.client))
        cursors = []
        for cursor in result['cursors']:
            cursors.append(CommandCursor(self,
              (cursor['cursor']), (sock_info.address), session=session,
              explicit_session=(session is not None)))
        else:
            return cursors

    def _count(self, cmd, collation=None, session=None):
        """Internal count helper."""

        def _cmd(session, server, sock_info, slave_ok):
            res = self._command(sock_info,
              cmd,
              slave_ok,
              allowable_errors=[
             'ns missing'],
              codec_options=(self._Collection__write_response_codec_options),
              read_concern=(self.read_concern),
              collation=collation,
              session=session)
            if res.get('errmsg', '') == 'ns missing':
                return 0
            return int(res['n'])

        return self._Collection__database.client._retryable_read(_cmd, self._read_preference_for(session), session)

    def _aggregate_one_result(self, sock_info, slave_ok, cmd, collation=None, session=None):
        """Internal helper to run an aggregate that returns a single result."""
        result = self._command(sock_info,
          cmd,
          slave_ok,
          codec_options=(self._Collection__write_response_codec_options),
          read_concern=(self.read_concern),
          collation=collation,
          session=session)
        batch = result['cursor']['firstBatch']
        if batch:
            return batch[0]

    def estimated_document_count(self, **kwargs):
        """Get an estimate of the number of documents in this collection using
        collection metadata.

        The :meth:`estimated_document_count` method is **not** supported in a
        transaction.

        All optional parameters should be passed as keyword arguments
        to this method. Valid options include:

          - `maxTimeMS` (int): The maximum amount of time to allow this
            operation to run, in milliseconds.

        :Parameters:
          - `**kwargs` (optional): See list of options above.

        .. versionadded:: 3.7
        """
        if 'session' in kwargs:
            raise ConfigurationError('estimated_document_count does not support sessions')
        cmd = SON([('count', self._Collection__name)])
        cmd.update(kwargs)
        return self._count(cmd)

    def count_documents(self, filter, session=None, **kwargs):
        """Count the number of documents in this collection.

        .. note:: For a fast count of the total documents in a collection see
           :meth:`estimated_document_count`.

        The :meth:`count_documents` method is supported in a transaction.

        All optional parameters should be passed as keyword arguments
        to this method. Valid options include:

          - `skip` (int): The number of matching documents to skip before
            returning results.
          - `limit` (int): The maximum number of documents to count. Must be
            a positive integer. If not provided, no limit is imposed.
          - `maxTimeMS` (int): The maximum amount of time to allow this
            operation to run, in milliseconds.
          - `collation` (optional): An instance of
            :class:`~pymongo.collation.Collation`. This option is only supported
            on MongoDB 3.4 and above.
          - `hint` (string or list of tuples): The index to use. Specify either
            the index name as a string or the index specification as a list of
            tuples (e.g. [('a', pymongo.ASCENDING), ('b', pymongo.ASCENDING)]).
            This option is only supported on MongoDB 3.6 and above.

        The :meth:`count_documents` method obeys the :attr:`read_preference` of
        this :class:`Collection`.

        .. note:: When migrating from :meth:`count` to :meth:`count_documents`
           the following query operators must be replaced:

           +-------------+-------------------------------------+
           | Operator    | Replacement                         |
           +=============+=====================================+
           | $where      | `$expr`_                            |
           +-------------+-------------------------------------+
           | $near       | `$geoWithin`_ with `$center`_       |
           +-------------+-------------------------------------+
           | $nearSphere | `$geoWithin`_ with `$centerSphere`_ |
           +-------------+-------------------------------------+

           $expr requires MongoDB 3.6+

        :Parameters:
          - `filter` (required): A query document that selects which documents
            to count in the collection. Can be an empty document to count all
            documents.
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.
          - `**kwargs` (optional): See list of options above.

        .. versionadded:: 3.7

        .. _$expr: https://docs.mongodb.com/manual/reference/operator/query/expr/
        .. _$geoWithin: https://docs.mongodb.com/manual/reference/operator/query/geoWithin/
        .. _$center: https://docs.mongodb.com/manual/reference/operator/query/center/#op._S_center
        .. _$centerSphere: https://docs.mongodb.com/manual/reference/operator/query/centerSphere/#op._S_centerSphere
        """
        pipeline = [
         {'$match': filter}]
        if 'skip' in kwargs:
            pipeline.append({'$skip': kwargs.pop('skip')})
        if 'limit' in kwargs:
            pipeline.append({'$limit': kwargs.pop('limit')})
        pipeline.append({'$group': {'_id':1,  'n':{'$sum': 1}}})
        cmd = SON([('aggregate', self._Collection__name),
         (
          'pipeline', pipeline),
         (
          'cursor', {})])
        if 'hint' in kwargs:
            if not isinstance(kwargs['hint'], string_type):
                kwargs['hint'] = helpers._index_document(kwargs['hint'])
        collation = validate_collation_or_none(kwargs.pop('collation', None))
        cmd.update(kwargs)

        def _cmd(session, server, sock_info, slave_ok):
            result = self._aggregate_one_result(sock_info, slave_ok, cmd, collation, session)
            if not result:
                return 0
            return result['n']

        return self._Collection__database.client._retryable_read(_cmd, self._read_preference_for(session), session)

    def count(self, filter=None, session=None, **kwargs):
        """**DEPRECATED** - Get the number of documents in this collection.

        The :meth:`count` method is deprecated and **not** supported in a
        transaction. Please use :meth:`count_documents` or
        :meth:`estimated_document_count` instead.

        All optional count parameters should be passed as keyword arguments
        to this method. Valid options include:

          - `skip` (int): The number of matching documents to skip before
            returning results.
          - `limit` (int): The maximum number of documents to count. A limit
            of 0 (the default) is equivalent to setting no limit.
          - `maxTimeMS` (int): The maximum amount of time to allow the count
            command to run, in milliseconds.
          - `collation` (optional): An instance of
            :class:`~pymongo.collation.Collation`. This option is only supported
            on MongoDB 3.4 and above.
          - `hint` (string or list of tuples): The index to use. Specify either
            the index name as a string or the index specification as a list of
            tuples (e.g. [('a', pymongo.ASCENDING), ('b', pymongo.ASCENDING)]).

        The :meth:`count` method obeys the :attr:`read_preference` of
        this :class:`Collection`.

        .. note:: When migrating from :meth:`count` to :meth:`count_documents`
           the following query operators must be replaced:

           +-------------+-------------------------------------+
           | Operator    | Replacement                         |
           +=============+=====================================+
           | $where      | `$expr`_                            |
           +-------------+-------------------------------------+
           | $near       | `$geoWithin`_ with `$center`_       |
           +-------------+-------------------------------------+
           | $nearSphere | `$geoWithin`_ with `$centerSphere`_ |
           +-------------+-------------------------------------+

           $expr requires MongoDB 3.6+

        :Parameters:
          - `filter` (optional): A query document that selects which documents
            to count in the collection.
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.
          - `**kwargs` (optional): See list of options above.

        .. versionchanged:: 3.7
           Deprecated.

        .. versionchanged:: 3.6
           Added ``session`` parameter.

        .. versionchanged:: 3.4
           Support the `collation` option.

        .. _$expr: https://docs.mongodb.com/manual/reference/operator/query/expr/
        .. _$geoWithin: https://docs.mongodb.com/manual/reference/operator/query/geoWithin/
        .. _$center: https://docs.mongodb.com/manual/reference/operator/query/center/#op._S_center
        .. _$centerSphere: https://docs.mongodb.com/manual/reference/operator/query/centerSphere/#op._S_centerSphere
        """
        warnings.warn('count is deprecated. Use estimated_document_count or count_documents instead. Please note that $where must be replaced by $expr, $near must be replaced by $geoWithin with $center, and $nearSphere must be replaced by $geoWithin with $centerSphere', DeprecationWarning,
          stacklevel=2)
        cmd = SON([('count', self._Collection__name)])
        if filter is not None:
            if 'query' in kwargs:
                raise ConfigurationError("can't pass both filter and query")
            kwargs['query'] = filter
        if 'hint' in kwargs:
            if not isinstance(kwargs['hint'], string_type):
                kwargs['hint'] = helpers._index_document(kwargs['hint'])
        collation = validate_collation_or_none(kwargs.pop('collation', None))
        cmd.update(kwargs)
        return self._count(cmd, collation, session)

    def create_indexes(self, indexes, session=None, **kwargs):
        """Create one or more indexes on this collection.

          >>> from pymongo import IndexModel, ASCENDING, DESCENDING
          >>> index1 = IndexModel([("hello", DESCENDING),
          ...                      ("world", ASCENDING)], name="hello_world")
          >>> index2 = IndexModel([("goodbye", DESCENDING)])
          >>> db.test.create_indexes([index1, index2])
          ["hello_world", "goodbye_-1"]

        :Parameters:
          - `indexes`: A list of :class:`~pymongo.operations.IndexModel`
            instances.
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.
          - `**kwargs` (optional): optional arguments to the createIndexes
            command (like maxTimeMS) can be passed as keyword arguments.

        .. note:: `create_indexes` uses the `createIndexes`_ command
           introduced in MongoDB **2.6** and cannot be used with earlier
           versions.

        .. note:: The :attr:`~pymongo.collection.Collection.write_concern` of
           this collection is automatically applied to this operation when using
           MongoDB >= 3.4.

        .. versionchanged:: 3.6
           Added ``session`` parameter. Added support for arbitrary keyword
           arguments.

        .. versionchanged:: 3.4
           Apply this collection's write concern automatically to this operation
           when connected to MongoDB >= 3.4.
        .. versionadded:: 3.0

        .. _createIndexes: https://docs.mongodb.com/manual/reference/command/createIndexes/
        """
        common.validate_list('indexes', indexes)
        names = []
        with self._socket_for_writes(session) as (sock_info):
            supports_collations = sock_info.max_wire_version >= 5

            def gen_indexes():
                for index in indexes:
                    if not isinstance(index, IndexModel):
                        raise TypeError('%r is not an instance of pymongo.operations.IndexModel' % (
                         index,))
                    document = index.document
                    if 'collation' in document:
                        if not supports_collations:
                            raise ConfigurationError('Must be connected to MongoDB 3.4+ to use collations.')
                    names.append(document['name'])
                    (yield document)

            cmd = SON([('createIndexes', self.name),
             (
              'indexes', list(gen_indexes()))])
            cmd.update(kwargs)
            self._command(sock_info,
              cmd, read_preference=(ReadPreference.PRIMARY), codec_options=_UNICODE_REPLACE_CODEC_OPTIONS,
              write_concern=(self._write_concern_for(session)),
              session=session)
        return names

    def __create_index(self, keys, index_options, session, **kwargs):
        """Internal create index helper.

        :Parameters:
          - `keys`: a list of tuples [(key, type), (key, type), ...]
          - `index_options`: a dict of index options.
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.
        """
        index_doc = helpers._index_document(keys)
        index = {'key': index_doc}
        collation = validate_collation_or_none(index_options.pop('collation', None))
        index.update(index_options)
        with self._socket_for_writes(session) as (sock_info):
            if collation is not None:
                if sock_info.max_wire_version < 5:
                    raise ConfigurationError('Must be connected to MongoDB 3.4+ to use collations.')
                else:
                    index['collation'] = collation
            cmd = SON([('createIndexes', self.name), ('indexes', [index])])
            cmd.update(kwargs)
            self._command(sock_info,
              cmd, read_preference=(ReadPreference.PRIMARY), codec_options=_UNICODE_REPLACE_CODEC_OPTIONS,
              write_concern=(self._write_concern_for(session)),
              session=session)

    def create_index(self, keys, session=None, **kwargs):
        """Creates an index on this collection.

        Takes either a single key or a list of (key, direction) pairs.
        The key(s) must be an instance of :class:`basestring`
        (:class:`str` in python 3), and the direction(s) must be one of
        (:data:`~pymongo.ASCENDING`, :data:`~pymongo.DESCENDING`,
        :data:`~pymongo.GEO2D`, :data:`~pymongo.GEOHAYSTACK`,
        :data:`~pymongo.GEOSPHERE`, :data:`~pymongo.HASHED`,
        :data:`~pymongo.TEXT`).

        To create a single key ascending index on the key ``'mike'`` we just
        use a string argument::

          >>> my_collection.create_index("mike")

        For a compound index on ``'mike'`` descending and ``'eliot'``
        ascending we need to use a list of tuples::

          >>> my_collection.create_index([("mike", pymongo.DESCENDING),
          ...                             ("eliot", pymongo.ASCENDING)])

        All optional index creation parameters should be passed as
        keyword arguments to this method. For example::

          >>> my_collection.create_index([("mike", pymongo.DESCENDING)],
          ...                            background=True)

        Valid options include, but are not limited to:

          - `name`: custom name to use for this index - if none is
            given, a name will be generated.
          - `unique`: if ``True`` creates a uniqueness constraint on the index.
          - `background`: if ``True`` this index should be created in the
            background.
          - `sparse`: if ``True``, omit from the index any documents that lack
            the indexed field.
          - `bucketSize`: for use with geoHaystack indexes.
            Number of documents to group together within a certain proximity
            to a given longitude and latitude.
          - `min`: minimum value for keys in a :data:`~pymongo.GEO2D`
            index.
          - `max`: maximum value for keys in a :data:`~pymongo.GEO2D`
            index.
          - `expireAfterSeconds`: <int> Used to create an expiring (TTL)
            collection. MongoDB will automatically delete documents from
            this collection after <int> seconds. The indexed field must
            be a UTC datetime or the data will not expire.
          - `partialFilterExpression`: A document that specifies a filter for
            a partial index. Requires server version >=3.2.
          - `collation` (optional): An instance of
            :class:`~pymongo.collation.Collation`. This option is only supported
            on MongoDB 3.4 and above.
          - `wildcardProjection`: Allows users to include or exclude specific
            field paths from a `wildcard index`_ using the { "$**" : 1} key
            pattern. Requires server version >= 4.2.

        See the MongoDB documentation for a full list of supported options by
        server version.

        .. warning:: `dropDups` is not supported by MongoDB 3.0 or newer. The
          option is silently ignored by the server and unique index builds
          using the option will fail if a duplicate value is detected.

        .. note:: The :attr:`~pymongo.collection.Collection.write_concern` of
           this collection is automatically applied to this operation when using
           MongoDB >= 3.4.

        :Parameters:
          - `keys`: a single key or a list of (key, direction)
            pairs specifying the index to create
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.
          - `**kwargs` (optional): any additional index creation
            options (see the above list) should be passed as keyword
            arguments

        .. versionchanged:: 3.6
           Added ``session`` parameter. Added support for passing maxTimeMS
           in kwargs.
        .. versionchanged:: 3.4
           Apply this collection's write concern automatically to this operation
           when connected to MongoDB >= 3.4. Support the `collation` option.
        .. versionchanged:: 3.2
            Added partialFilterExpression to support partial indexes.
        .. versionchanged:: 3.0
            Renamed `key_or_list` to `keys`. Removed the `cache_for` option.
            :meth:`create_index` no longer caches index names. Removed support
            for the drop_dups and bucket_size aliases.

        .. mongodoc:: indexes

        .. _wildcard index: https://docs.mongodb.com/master/core/index-wildcard/#wildcard-index-core
        """
        keys = helpers._index_list(keys)
        name = kwargs.setdefault('name', helpers._gen_index_name(keys))
        cmd_options = {}
        if 'maxTimeMS' in kwargs:
            cmd_options['maxTimeMS'] = kwargs.pop('maxTimeMS')
        (self._Collection__create_index)(keys, kwargs, session, **cmd_options)
        return name

    def ensure_index(self, key_or_list, cache_for=300, **kwargs):
        """**DEPRECATED** - Ensures that an index exists on this collection.

        .. versionchanged:: 3.0
            **DEPRECATED**
        """
        warnings.warn('ensure_index is deprecated. Use create_index instead.', DeprecationWarning,
          stacklevel=2)
        if not isinstance(cache_for, integer_types):
            if not isinstance(cache_for, float):
                raise TypeError('cache_for must be an integer or float.')
        if 'drop_dups' in kwargs:
            kwargs['dropDups'] = kwargs.pop('drop_dups')
        if 'bucket_size' in kwargs:
            kwargs['bucketSize'] = kwargs.pop('bucket_size')
        keys = helpers._index_list(key_or_list)
        name = kwargs.setdefault('name', helpers._gen_index_name(keys))
        if not self._Collection__database.client._cached(self._Collection__database.name, self._Collection__name, name):
            self._Collection__create_index(keys, kwargs, session=None)
            self._Collection__database.client._cache_index(self._Collection__database.name, self._Collection__name, name, cache_for)
            return name

    def drop_indexes(self, session=None, **kwargs):
        """Drops all indexes on this collection.

        Can be used on non-existant collections or collections with no indexes.
        Raises OperationFailure on an error.

        :Parameters:
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.
          - `**kwargs` (optional): optional arguments to the createIndexes
            command (like maxTimeMS) can be passed as keyword arguments.

        .. note:: The :attr:`~pymongo.collection.Collection.write_concern` of
           this collection is automatically applied to this operation when using
           MongoDB >= 3.4.

        .. versionchanged:: 3.6
           Added ``session`` parameter. Added support for arbitrary keyword
           arguments.

        .. versionchanged:: 3.4
           Apply this collection's write concern automatically to this operation
           when connected to MongoDB >= 3.4.

        """
        self._Collection__database.client._purge_index(self._Collection__database.name, self._Collection__name)
        (self.drop_index)('*', session=session, **kwargs)

    def drop_index(self, index_or_name, session=None, **kwargs):
        """Drops the specified index on this collection.

        Can be used on non-existant collections or collections with no
        indexes.  Raises OperationFailure on an error (e.g. trying to
        drop an index that does not exist). `index_or_name`
        can be either an index name (as returned by `create_index`),
        or an index specifier (as passed to `create_index`). An index
        specifier should be a list of (key, direction) pairs. Raises
        TypeError if index is not an instance of (str, unicode, list).

        .. warning::

          if a custom name was used on index creation (by
          passing the `name` parameter to :meth:`create_index` or
          :meth:`ensure_index`) the index **must** be dropped by name.

        :Parameters:
          - `index_or_name`: index (or name of index) to drop
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.
          - `**kwargs` (optional): optional arguments to the createIndexes
            command (like maxTimeMS) can be passed as keyword arguments.

        .. note:: The :attr:`~pymongo.collection.Collection.write_concern` of
           this collection is automatically applied to this operation when using
           MongoDB >= 3.4.

        .. versionchanged:: 3.6
           Added ``session`` parameter. Added support for arbitrary keyword
           arguments.

        .. versionchanged:: 3.4
           Apply this collection's write concern automatically to this operation
           when connected to MongoDB >= 3.4.

        """
        name = index_or_name
        if isinstance(index_or_name, list):
            name = helpers._gen_index_name(index_or_name)
        if not isinstance(name, string_type):
            raise TypeError('index_or_name must be an index name or list')
        self._Collection__database.client._purge_index(self._Collection__database.name, self._Collection__name, name)
        cmd = SON([('dropIndexes', self._Collection__name), ('index', name)])
        cmd.update(kwargs)
        with self._socket_for_writes(session) as (sock_info):
            self._command(sock_info, cmd,
              read_preference=(ReadPreference.PRIMARY),
              allowable_errors=[
             'ns not found'],
              write_concern=(self._write_concern_for(session)),
              session=session)

    def reindex--- This code section failed: ---

 L.2144         0  LOAD_GLOBAL              SON
                2  LOAD_STR                 'reIndex'
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _Collection__name
                8  BUILD_TUPLE_2         2 
               10  BUILD_LIST_1          1 
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'cmd'

 L.2145        16  LOAD_FAST                'cmd'
               18  LOAD_METHOD              update
               20  LOAD_FAST                'kwargs'
               22  CALL_METHOD_1         1  ''
               24  POP_TOP          

 L.2146        26  LOAD_FAST                'self'
               28  LOAD_METHOD              _socket_for_writes
               30  LOAD_FAST                'session'
               32  CALL_METHOD_1         1  ''
               34  SETUP_WITH           70  'to 70'
               36  STORE_FAST               'sock_info'

 L.2147        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _command

 L.2148        42  LOAD_FAST                'sock_info'

 L.2148        44  LOAD_FAST                'cmd'

 L.2148        46  LOAD_GLOBAL              ReadPreference
               48  LOAD_ATTR                PRIMARY

 L.2149        50  LOAD_FAST                'session'

 L.2147        52  LOAD_CONST               ('read_preference', 'session')
               54  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               56  POP_BLOCK        
               58  ROT_TWO          
               60  BEGIN_FINALLY    
               62  WITH_CLEANUP_START
               64  WITH_CLEANUP_FINISH
               66  POP_FINALLY           0  ''
               68  RETURN_VALUE     
             70_0  COME_FROM_WITH       34  '34'
               70  WITH_CLEANUP_START
               72  WITH_CLEANUP_FINISH
               74  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 58

    def list_indexes(self, session=None):
        """Get a cursor over the index documents for this collection.

          >>> for index in db.test.list_indexes():
          ...     print(index)
          ...
          SON([(u'v', 1), (u'key', SON([(u'_id', 1)])),
               (u'name', u'_id_'), (u'ns', u'test.test')])

        :Parameters:
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.

        :Returns:
          An instance of :class:`~pymongo.command_cursor.CommandCursor`.

        .. versionchanged:: 3.6
           Added ``session`` parameter.

        .. versionadded:: 3.0
        """
        codec_options = CodecOptions(SON)
        coll = self.with_options(codec_options=codec_options, read_preference=(ReadPreference.PRIMARY))
        read_pref = session and session._txn_read_preference() or ReadPreference.PRIMARY

        def _cmd(session, server, sock_info, slave_ok):
            cmd = SON([('listIndexes', self._Collection__name), ('cursor', {})])
            if sock_info.max_wire_version > 2:
                with self._Collection__database.client._tmp_session(session, False) as (s):
                    try:
                        cursor = self._command(sock_info, cmd, slave_ok, read_pref,
                          codec_options,
                          session=s)['cursor']
                    except OperationFailure as exc:
                        try:
                            if exc.code != 26:
                                raise
                            cursor = {'id':0, 
                             'firstBatch':[]}
                        finally:
                            exc = None
                            del exc

                return CommandCursor(coll, cursor, (sock_info.address), session=s,
                  explicit_session=(session is not None))
            res = message._first_batch(sock_info, self._Collection__database.name, 'system.indexes', {'ns': self._Collection__full_name}, 0, slave_ok, codec_options, read_pref, cmd, self.database.client._event_listeners)
            cursor = res['cursor']
            return CommandCursor(coll, cursor, sock_info.address)

        return self._Collection__database.client._retryable_read(_cmd, read_pref, session)

    def index_information(self, session=None):
        """Get information on this collection's indexes.

        Returns a dictionary where the keys are index names (as
        returned by create_index()) and the values are dictionaries
        containing information about each index. The dictionary is
        guaranteed to contain at least a single key, ``"key"`` which
        is a list of (key, direction) pairs specifying the index (as
        passed to create_index()). It will also contain any other
        metadata about the indexes, except for the ``"ns"`` and
        ``"name"`` keys, which are cleaned. Example output might look
        like this:

        >>> db.test.create_index("x", unique=True)
        u'x_1'
        >>> db.test.index_information()
        {u'_id_': {u'key': [(u'_id', 1)]},
         u'x_1': {u'unique': True, u'key': [(u'x', 1)]}}

        :Parameters:
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.

        .. versionchanged:: 3.6
           Added ``session`` parameter.
        """
        cursor = self.list_indexes(session=session)
        info = {}
        for index in cursor:
            index['key'] = index['key'].items()
            index = dict(index)
            info[index.pop('name')] = index
        else:
            return info

    def options(self, session=None):
        """Get the options set on this collection.

        Returns a dictionary of options and their values - see
        :meth:`~pymongo.database.Database.create_collection` for more
        information on the possible options. Returns an empty
        dictionary if the collection has not been created yet.

        :Parameters:
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.

        .. versionchanged:: 3.6
           Added ``session`` parameter.
        """
        dbo = self._Collection__database.client.get_database(self._Collection__database.name, self.codec_options, self.read_preference, self.write_concern, self.read_concern)
        cursor = dbo.list_collections(session=session,
          filter={'name': self._Collection__name})
        result = None
        for doc in cursor:
            result = doc
            break
        else:
            if not result:
                return {}
            options = result.get('options', {})
            if 'create' in options:
                del options['create']
            return options

    def _aggregate(self, aggregation_command, pipeline, cursor_class, session, explicit_session, **kwargs):
        use_cursor = True
        if 'useCursor' in kwargs:
            warnings.warn('The useCursor option is deprecated and will be removed in PyMongo 4.0',
              DeprecationWarning,
              stacklevel=2)
            use_cursor = common.validate_boolean('useCursor', kwargs.pop('useCursor', True))
        cmd = aggregation_command(self,
          cursor_class, pipeline, kwargs, explicit_session, user_fields={'cursor': {'firstBatch': 1}},
          use_cursor=use_cursor)
        return self._Collection__database.client._retryable_read((cmd.get_cursor),
          (cmd.get_read_preference(session)), session, retryable=(not cmd._performs_write))

    def aggregate--- This code section failed: ---

 L.2374         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _Collection__database
                4  LOAD_ATTR                client
                6  LOAD_ATTR                _tmp_session
                8  LOAD_FAST                'session'
               10  LOAD_CONST               False
               12  LOAD_CONST               ('close',)
               14  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               16  SETUP_WITH           64  'to 64'
               18  STORE_FAST               's'

 L.2375        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _aggregate
               24  LOAD_GLOBAL              _CollectionAggregationCommand

 L.2376        26  LOAD_FAST                'pipeline'

 L.2377        28  LOAD_GLOBAL              CommandCursor

 L.2375        30  BUILD_TUPLE_3         3 

 L.2378        32  LOAD_FAST                's'

 L.2379        34  LOAD_FAST                'session'
               36  LOAD_CONST               None
               38  COMPARE_OP               is-not

 L.2375        40  LOAD_CONST               ('session', 'explicit_session')
               42  BUILD_CONST_KEY_MAP_2     2 

 L.2380        44  LOAD_FAST                'kwargs'

 L.2375        46  BUILD_MAP_UNPACK_WITH_CALL_2     2 
               48  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               50  POP_BLOCK        
               52  ROT_TWO          
               54  BEGIN_FINALLY    
               56  WITH_CLEANUP_START
               58  WITH_CLEANUP_FINISH
               60  POP_FINALLY           0  ''
               62  RETURN_VALUE     
             64_0  COME_FROM_WITH       16  '16'
               64  WITH_CLEANUP_START
               66  WITH_CLEANUP_FINISH
               68  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 52

    def aggregate_raw_batches(self, pipeline, **kwargs):
        """Perform an aggregation and retrieve batches of raw BSON.

        Similar to the :meth:`aggregate` method but returns a
        :class:`~pymongo.cursor.RawBatchCursor`.

        This example demonstrates how to work with raw batches, but in practice
        raw batches should be passed to an external library that can decode
        BSON into another data type, rather than used with PyMongo's
        :mod:`bson` module.

          >>> import bson
          >>> cursor = db.test.aggregate_raw_batches([
          ...     {'$project': {'x': {'$multiply': [2, '$x']}}}])
          >>> for batch in cursor:
          ...     print(bson.decode_all(batch))

        .. note:: aggregate_raw_batches does not support sessions or auto
           encryption.

        .. versionadded:: 3.6
        """
        if 'session' in kwargs:
            raise ConfigurationError('aggregate_raw_batches does not support sessions')
        if self._Collection__database.client._encrypter:
            raise InvalidOperation('aggregate_raw_batches does not support auto encryption')
        return (self._aggregate)(_CollectionRawAggregationCommand,
 pipeline,
 RawBatchCommandCursor, session=None, 
         explicit_session=False, **kwargs)

    def watch(self, pipeline=None, full_document=None, resume_after=None, max_await_time_ms=None, batch_size=None, collation=None, start_at_operation_time=None, session=None, start_after=None):
        """Watch changes on this collection.

        Performs an aggregation with an implicit initial ``$changeStream``
        stage and returns a
        :class:`~pymongo.change_stream.CollectionChangeStream` cursor which
        iterates over changes on this collection.

        Introduced in MongoDB 3.6.

        .. code-block:: python

           with db.collection.watch() as stream:
               for change in stream:
                   print(change)

        The :class:`~pymongo.change_stream.CollectionChangeStream` iterable
        blocks until the next change document is returned or an error is
        raised. If the
        :meth:`~pymongo.change_stream.CollectionChangeStream.next` method
        encounters a network error when retrieving a batch from the server,
        it will automatically attempt to recreate the cursor such that no
        change events are missed. Any error encountered during the resume
        attempt indicates there may be an outage and will be raised.

        .. code-block:: python

            try:
                with db.collection.watch(
                        [{'$match': {'operationType': 'insert'}}]) as stream:
                    for insert_change in stream:
                        print(insert_change)
            except pymongo.errors.PyMongoError:
                # The ChangeStream encountered an unrecoverable error or the
                # resume attempt failed to recreate the cursor.
                logging.error('...')

        For a precise description of the resume process see the
        `change streams specification`_.

        .. note:: Using this helper method is preferred to directly calling
            :meth:`~pymongo.collection.Collection.aggregate` with a
            ``$changeStream`` stage, for the purpose of supporting
            resumability.

        .. warning:: This Collection's :attr:`read_concern` must be
            ``ReadConcern("majority")`` in order to use the ``$changeStream``
            stage.

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
          A :class:`~pymongo.change_stream.CollectionChangeStream` cursor.

        .. versionchanged:: 3.9
           Added the ``start_after`` parameter.

        .. versionchanged:: 3.7
           Added the ``start_at_operation_time`` parameter.

        .. versionadded:: 3.6

        .. mongodoc:: changeStreams

        .. _change streams specification:
            https://github.com/mongodb/specifications/blob/master/source/change-streams/change-streams.rst
        """
        return CollectionChangeStream(self, pipeline, full_document, resume_after, max_await_time_ms, batch_size, collation, start_at_operation_time, session, start_after)

    def group--- This code section failed: ---

 L.2541         0  LOAD_GLOBAL              warnings
                2  LOAD_ATTR                warn
                4  LOAD_STR                 'The group method is deprecated and will be removed in PyMongo 4.0. Use the aggregate method with the $group stage or the map_reduce method instead.'

 L.2544         6  LOAD_GLOBAL              DeprecationWarning

 L.2544         8  LOAD_CONST               2

 L.2541        10  LOAD_CONST               ('stacklevel',)
               12  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               14  POP_TOP          

 L.2545        16  BUILD_MAP_0           0 
               18  STORE_FAST               'group'

 L.2546        20  LOAD_GLOBAL              isinstance
               22  LOAD_FAST                'key'
               24  LOAD_GLOBAL              string_type
               26  CALL_FUNCTION_2       2  ''
               28  POP_JUMP_IF_FALSE    44  'to 44'

 L.2547        30  LOAD_GLOBAL              Code
               32  LOAD_FAST                'key'
               34  CALL_FUNCTION_1       1  ''
               36  LOAD_FAST                'group'
               38  LOAD_STR                 '$keyf'
               40  STORE_SUBSCR     
               42  JUMP_FORWARD         68  'to 68'
             44_0  COME_FROM            28  '28'

 L.2548        44  LOAD_FAST                'key'
               46  LOAD_CONST               None
               48  COMPARE_OP               is-not
               50  POP_JUMP_IF_FALSE    68  'to 68'

 L.2549        52  LOAD_STR                 'key'
               54  LOAD_GLOBAL              helpers
               56  LOAD_METHOD              _fields_list_to_dict
               58  LOAD_FAST                'key'
               60  LOAD_STR                 'key'
               62  CALL_METHOD_2         2  ''
               64  BUILD_MAP_1           1 
               66  STORE_FAST               'group'
             68_0  COME_FROM            50  '50'
             68_1  COME_FROM            42  '42'

 L.2550        68  LOAD_FAST                'self'
               70  LOAD_ATTR                _Collection__name
               72  LOAD_FAST                'group'
               74  LOAD_STR                 'ns'
               76  STORE_SUBSCR     

 L.2551        78  LOAD_GLOBAL              Code
               80  LOAD_FAST                'reduce'
               82  CALL_FUNCTION_1       1  ''
               84  LOAD_FAST                'group'
               86  LOAD_STR                 '$reduce'
               88  STORE_SUBSCR     

 L.2552        90  LOAD_FAST                'condition'
               92  LOAD_FAST                'group'
               94  LOAD_STR                 'cond'
               96  STORE_SUBSCR     

 L.2553        98  LOAD_FAST                'initial'
              100  LOAD_FAST                'group'
              102  LOAD_STR                 'initial'
              104  STORE_SUBSCR     

 L.2554       106  LOAD_FAST                'finalize'
              108  LOAD_CONST               None
              110  COMPARE_OP               is-not
              112  POP_JUMP_IF_FALSE   126  'to 126'

 L.2555       114  LOAD_GLOBAL              Code
              116  LOAD_FAST                'finalize'
              118  CALL_FUNCTION_1       1  ''
              120  LOAD_FAST                'group'
              122  LOAD_STR                 'finalize'
              124  STORE_SUBSCR     
            126_0  COME_FROM           112  '112'

 L.2557       126  LOAD_GLOBAL              SON
              128  LOAD_STR                 'group'
              130  LOAD_FAST                'group'
              132  BUILD_TUPLE_2         2 
              134  BUILD_LIST_1          1 
              136  CALL_FUNCTION_1       1  ''
              138  STORE_FAST               'cmd'

 L.2558       140  LOAD_GLOBAL              validate_collation_or_none
              142  LOAD_FAST                'kwargs'
              144  LOAD_METHOD              pop
              146  LOAD_STR                 'collation'
              148  LOAD_CONST               None
              150  CALL_METHOD_2         2  ''
              152  CALL_FUNCTION_1       1  ''
              154  STORE_FAST               'collation'

 L.2559       156  LOAD_FAST                'cmd'
              158  LOAD_METHOD              update
              160  LOAD_FAST                'kwargs'
              162  CALL_METHOD_1         1  ''
              164  POP_TOP          

 L.2561       166  LOAD_FAST                'self'
              168  LOAD_ATTR                _socket_for_reads
              170  LOAD_CONST               None
              172  LOAD_CONST               ('session',)
              174  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              176  SETUP_WITH          224  'to 224'
              178  UNPACK_SEQUENCE_2     2 
              180  STORE_FAST               'sock_info'
              182  STORE_FAST               'slave_ok'

 L.2562       184  LOAD_FAST                'self'
              186  LOAD_ATTR                _command
              188  LOAD_FAST                'sock_info'
              190  LOAD_FAST                'cmd'
              192  LOAD_FAST                'slave_ok'

 L.2563       194  LOAD_FAST                'collation'

 L.2564       196  LOAD_STR                 'retval'
              198  LOAD_CONST               1
              200  BUILD_MAP_1           1 

 L.2562       202  LOAD_CONST               ('collation', 'user_fields')
              204  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'

 L.2564       206  LOAD_STR                 'retval'

 L.2562       208  BINARY_SUBSCR    
              210  POP_BLOCK        
              212  ROT_TWO          
              214  BEGIN_FINALLY    
              216  WITH_CLEANUP_START
              218  WITH_CLEANUP_FINISH
              220  POP_FINALLY           0  ''
              222  RETURN_VALUE     
            224_0  COME_FROM_WITH      176  '176'
              224  WITH_CLEANUP_START
              226  WITH_CLEANUP_FINISH
              228  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 212

    def rename--- This code section failed: ---

 L.2595         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'new_name'
                4  LOAD_GLOBAL              string_type
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     26  'to 26'

 L.2596        10  LOAD_GLOBAL              TypeError
               12  LOAD_STR                 'new_name must be an instance of %s'

 L.2597        14  LOAD_GLOBAL              string_type
               16  LOAD_ATTR                __name__
               18  BUILD_TUPLE_1         1 

 L.2596        20  BINARY_MODULO    
               22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM             8  '8'

 L.2599        26  LOAD_FAST                'new_name'
               28  POP_JUMP_IF_FALSE    38  'to 38'
               30  LOAD_STR                 '..'
               32  LOAD_FAST                'new_name'
               34  COMPARE_OP               in
               36  POP_JUMP_IF_FALSE    46  'to 46'
             38_0  COME_FROM            28  '28'

 L.2600        38  LOAD_GLOBAL              InvalidName
               40  LOAD_STR                 'collection names cannot be empty'
               42  CALL_FUNCTION_1       1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
             46_0  COME_FROM            36  '36'

 L.2601        46  LOAD_FAST                'new_name'
               48  LOAD_CONST               0
               50  BINARY_SUBSCR    
               52  LOAD_STR                 '.'
               54  COMPARE_OP               ==
               56  POP_JUMP_IF_TRUE     70  'to 70'
               58  LOAD_FAST                'new_name'
               60  LOAD_CONST               -1
               62  BINARY_SUBSCR    
               64  LOAD_STR                 '.'
               66  COMPARE_OP               ==
               68  POP_JUMP_IF_FALSE    78  'to 78'
             70_0  COME_FROM            56  '56'

 L.2602        70  LOAD_GLOBAL              InvalidName
               72  LOAD_STR                 "collecion names must not start or end with '.'"
               74  CALL_FUNCTION_1       1  ''
               76  RAISE_VARARGS_1       1  'exception instance'
             78_0  COME_FROM            68  '68'

 L.2603        78  LOAD_STR                 '$'
               80  LOAD_FAST                'new_name'
               82  COMPARE_OP               in
               84  POP_JUMP_IF_FALSE   104  'to 104'
               86  LOAD_FAST                'new_name'
               88  LOAD_METHOD              startswith
               90  LOAD_STR                 'oplog.$main'
               92  CALL_METHOD_1         1  ''
               94  POP_JUMP_IF_TRUE    104  'to 104'

 L.2604        96  LOAD_GLOBAL              InvalidName
               98  LOAD_STR                 "collection names must not contain '$'"
              100  CALL_FUNCTION_1       1  ''
              102  RAISE_VARARGS_1       1  'exception instance'
            104_0  COME_FROM            94  '94'
            104_1  COME_FROM            84  '84'

 L.2606       104  LOAD_STR                 '%s.%s'
              106  LOAD_FAST                'self'
              108  LOAD_ATTR                _Collection__database
              110  LOAD_ATTR                name
              112  LOAD_FAST                'new_name'
              114  BUILD_TUPLE_2         2 
              116  BINARY_MODULO    
              118  STORE_FAST               'new_name'

 L.2607       120  LOAD_GLOBAL              SON
              122  LOAD_STR                 'renameCollection'
              124  LOAD_FAST                'self'
              126  LOAD_ATTR                _Collection__full_name
              128  BUILD_TUPLE_2         2 
              130  LOAD_STR                 'to'
              132  LOAD_FAST                'new_name'
              134  BUILD_TUPLE_2         2 
              136  BUILD_LIST_2          2 
              138  CALL_FUNCTION_1       1  ''
              140  STORE_FAST               'cmd'

 L.2608       142  LOAD_FAST                'cmd'
              144  LOAD_METHOD              update
              146  LOAD_FAST                'kwargs'
              148  CALL_METHOD_1         1  ''
              150  POP_TOP          

 L.2609       152  LOAD_FAST                'self'
              154  LOAD_METHOD              _write_concern_for_cmd
              156  LOAD_FAST                'cmd'
              158  LOAD_FAST                'session'
              160  CALL_METHOD_2         2  ''
              162  STORE_FAST               'write_concern'

 L.2611       164  LOAD_FAST                'self'
              166  LOAD_METHOD              _socket_for_writes
              168  LOAD_FAST                'session'
              170  CALL_METHOD_1         1  ''
              172  SETUP_WITH          252  'to 252'
              174  STORE_FAST               'sock_info'

 L.2612       176  LOAD_FAST                'self'
              178  LOAD_ATTR                _Collection__database
              180  LOAD_ATTR                client
              182  LOAD_METHOD              _tmp_session
              184  LOAD_FAST                'session'
              186  CALL_METHOD_1         1  ''
              188  SETUP_WITH          242  'to 242'
              190  STORE_FAST               's'

 L.2613       192  LOAD_FAST                'sock_info'
              194  LOAD_ATTR                command

 L.2614       196  LOAD_STR                 'admin'

 L.2614       198  LOAD_FAST                'cmd'

 L.2615       200  LOAD_FAST                'write_concern'

 L.2616       202  LOAD_CONST               True

 L.2617       204  LOAD_FAST                's'

 L.2617       206  LOAD_FAST                'self'
              208  LOAD_ATTR                _Collection__database
              210  LOAD_ATTR                client

 L.2613       212  LOAD_CONST               ('write_concern', 'parse_write_concern_error', 'session', 'client')
              214  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              216  POP_BLOCK        
              218  ROT_TWO          
              220  BEGIN_FINALLY    
              222  WITH_CLEANUP_START
              224  WITH_CLEANUP_FINISH
              226  POP_FINALLY           0  ''
              228  POP_BLOCK        
              230  ROT_TWO          
              232  BEGIN_FINALLY    
              234  WITH_CLEANUP_START
              236  WITH_CLEANUP_FINISH
              238  POP_FINALLY           0  ''
              240  RETURN_VALUE     
            242_0  COME_FROM_WITH      188  '188'
              242  WITH_CLEANUP_START
              244  WITH_CLEANUP_FINISH
              246  END_FINALLY      
              248  POP_BLOCK        
              250  BEGIN_FINALLY    
            252_0  COME_FROM_WITH      172  '172'
              252  WITH_CLEANUP_START
              254  WITH_CLEANUP_FINISH
              256  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 218

    def distinct(self, key, filter=None, session=None, **kwargs):
        """Get a list of distinct values for `key` among all documents
        in this collection.

        Raises :class:`TypeError` if `key` is not an instance of
        :class:`basestring` (:class:`str` in python 3).

        All optional distinct parameters should be passed as keyword arguments
        to this method. Valid options include:

          - `maxTimeMS` (int): The maximum amount of time to allow the count
            command to run, in milliseconds.
          - `collation` (optional): An instance of
            :class:`~pymongo.collation.Collation`. This option is only supported
            on MongoDB 3.4 and above.

        The :meth:`distinct` method obeys the :attr:`read_preference` of
        this :class:`Collection`.

        :Parameters:
          - `key`: name of the field for which we want to get the distinct
            values
          - `filter` (optional): A query document that specifies the documents
            from which to retrieve the distinct values.
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.
          - `**kwargs` (optional): See list of options above.

        .. versionchanged:: 3.6
           Added ``session`` parameter.

        .. versionchanged:: 3.4
           Support the `collation` option.

        """
        if not isinstance(key, string_type):
            raise TypeError('key must be an instance of %s' % (
             string_type.__name__,))
        cmd = SON([('distinct', self._Collection__name),
         (
          'key', key)])
        if filter is not None:
            if 'query' in kwargs:
                raise ConfigurationError("can't pass both filter and query")
            kwargs['query'] = filter
        collation = validate_collation_or_none(kwargs.pop('collation', None))
        cmd.update(kwargs)

        def _cmd(session, server, sock_info, slave_ok):
            return self._command(sock_info,
              cmd, slave_ok, read_concern=(self.read_concern), collation=collation,
              session=session,
              user_fields={'values': 1})['values']

        return self._Collection__database.client._retryable_read(_cmd, self._read_preference_for(session), session)

    def _map_reduce--- This code section failed: ---

 L.2676         0  LOAD_GLOBAL              SON
                2  LOAD_STR                 'mapReduce'
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _Collection__name
                8  BUILD_TUPLE_2         2 

 L.2677        10  LOAD_STR                 'map'
               12  LOAD_FAST                'map'
               14  BUILD_TUPLE_2         2 

 L.2678        16  LOAD_STR                 'reduce'
               18  LOAD_FAST                'reduce'
               20  BUILD_TUPLE_2         2 

 L.2679        22  LOAD_STR                 'out'
               24  LOAD_FAST                'out'
               26  BUILD_TUPLE_2         2 

 L.2676        28  BUILD_LIST_4          4 
               30  CALL_FUNCTION_1       1  ''
               32  STORE_FAST               'cmd'

 L.2680        34  LOAD_GLOBAL              validate_collation_or_none
               36  LOAD_FAST                'kwargs'
               38  LOAD_METHOD              pop
               40  LOAD_STR                 'collation'
               42  LOAD_CONST               None
               44  CALL_METHOD_2         2  ''
               46  CALL_FUNCTION_1       1  ''
               48  STORE_FAST               'collation'

 L.2681        50  LOAD_FAST                'cmd'
               52  LOAD_METHOD              update
               54  LOAD_FAST                'kwargs'
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          

 L.2683        60  LOAD_STR                 'inline'
               62  LOAD_FAST                'out'
               64  COMPARE_OP               in
               66  STORE_FAST               'inline'

 L.2685        68  LOAD_FAST                'inline'
               70  POP_JUMP_IF_FALSE    82  'to 82'

 L.2686        72  LOAD_STR                 'results'
               74  LOAD_CONST               1
               76  BUILD_MAP_1           1 
               78  STORE_FAST               'user_fields'
               80  JUMP_FORWARD         86  'to 86'
             82_0  COME_FROM            70  '70'

 L.2688        82  LOAD_CONST               None
               84  STORE_FAST               'user_fields'
             86_0  COME_FROM            80  '80'

 L.2690        86  LOAD_FAST                'session'
               88  POP_JUMP_IF_FALSE    98  'to 98'
               90  LOAD_FAST                'session'
               92  LOAD_METHOD              _txn_read_preference
               94  CALL_METHOD_0         0  ''
               96  JUMP_IF_TRUE_OR_POP   100  'to 100'
             98_0  COME_FROM            88  '88'

 L.2691        98  LOAD_FAST                'read_pref'
            100_0  COME_FROM            96  '96'

 L.2690       100  STORE_FAST               'read_pref'

 L.2693       102  LOAD_FAST                'self'
              104  LOAD_ATTR                _Collection__database
              106  LOAD_ATTR                client
              108  LOAD_METHOD              _socket_for_reads
              110  LOAD_FAST                'read_pref'
              112  LOAD_FAST                'session'
              114  CALL_METHOD_2         2  ''
              116  SETUP_WITH          226  'to 226'
              118  UNPACK_SEQUENCE_2     2 

 L.2694       120  STORE_FAST               'sock_info'

 L.2694       122  STORE_FAST               'slave_ok'

 L.2695       124  LOAD_FAST                'sock_info'
              126  LOAD_ATTR                max_wire_version
              128  LOAD_CONST               4
              130  COMPARE_OP               >=
              132  POP_JUMP_IF_FALSE   154  'to 154'

 L.2696       134  LOAD_STR                 'readConcern'
              136  LOAD_FAST                'cmd'
              138  COMPARE_OP               not-in

 L.2695       140  POP_JUMP_IF_FALSE   154  'to 154'

 L.2697       142  LOAD_FAST                'inline'

 L.2695       144  POP_JUMP_IF_FALSE   154  'to 154'

 L.2698       146  LOAD_FAST                'self'
              148  LOAD_ATTR                read_concern
              150  STORE_FAST               'read_concern'
              152  JUMP_FORWARD        158  'to 158'
            154_0  COME_FROM           144  '144'
            154_1  COME_FROM           140  '140'
            154_2  COME_FROM           132  '132'

 L.2700       154  LOAD_CONST               None
              156  STORE_FAST               'read_concern'
            158_0  COME_FROM           152  '152'

 L.2701       158  LOAD_STR                 'writeConcern'
              160  LOAD_FAST                'cmd'
              162  COMPARE_OP               not-in
              164  POP_JUMP_IF_FALSE   182  'to 182'
              166  LOAD_FAST                'inline'
              168  POP_JUMP_IF_TRUE    182  'to 182'

 L.2702       170  LOAD_FAST                'self'
              172  LOAD_METHOD              _write_concern_for
              174  LOAD_FAST                'session'
              176  CALL_METHOD_1         1  ''
              178  STORE_FAST               'write_concern'
              180  JUMP_FORWARD        186  'to 186'
            182_0  COME_FROM           168  '168'
            182_1  COME_FROM           164  '164'

 L.2704       182  LOAD_CONST               None
              184  STORE_FAST               'write_concern'
            186_0  COME_FROM           180  '180'

 L.2706       186  LOAD_FAST                'self'
              188  LOAD_ATTR                _command

 L.2707       190  LOAD_FAST                'sock_info'

 L.2707       192  LOAD_FAST                'cmd'

 L.2707       194  LOAD_FAST                'slave_ok'

 L.2707       196  LOAD_FAST                'read_pref'

 L.2708       198  LOAD_FAST                'read_concern'

 L.2709       200  LOAD_FAST                'write_concern'

 L.2710       202  LOAD_FAST                'collation'

 L.2710       204  LOAD_FAST                'session'

 L.2711       206  LOAD_FAST                'user_fields'

 L.2706       208  LOAD_CONST               ('read_concern', 'write_concern', 'collation', 'session', 'user_fields')
              210  CALL_FUNCTION_KW_9     9  '9 total positional and keyword args'
              212  POP_BLOCK        
              214  ROT_TWO          
              216  BEGIN_FINALLY    
              218  WITH_CLEANUP_START
              220  WITH_CLEANUP_FINISH
              222  POP_FINALLY           0  ''
              224  RETURN_VALUE     
            226_0  COME_FROM_WITH      116  '116'
              226  WITH_CLEANUP_START
              228  WITH_CLEANUP_FINISH
              230  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 214

    def map_reduce(self, map, reduce, out, full_response=False, session=None, **kwargs):
        """Perform a map/reduce operation on this collection.

        If `full_response` is ``False`` (default) returns a
        :class:`~pymongo.collection.Collection` instance containing
        the results of the operation. Otherwise, returns the full
        response from the server to the `map reduce command`_.

        :Parameters:
          - `map`: map function (as a JavaScript string)
          - `reduce`: reduce function (as a JavaScript string)
          - `out`: output collection name or `out object` (dict). See
            the `map reduce command`_ documentation for available options.
            Note: `out` options are order sensitive. :class:`~bson.son.SON`
            can be used to specify multiple options.
            e.g. SON([('replace', <collection name>), ('db', <database name>)])
          - `full_response` (optional): if ``True``, return full response to
            this command - otherwise just return the result collection
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.
          - `**kwargs` (optional): additional arguments to the
            `map reduce command`_ may be passed as keyword arguments to this
            helper method, e.g.::

            >>> db.test.map_reduce(map, reduce, "myresults", limit=2)

        .. note:: The :meth:`map_reduce` method does **not** obey the
           :attr:`read_preference` of this :class:`Collection`. To run
           mapReduce on a secondary use the :meth:`inline_map_reduce` method
           instead.

        .. note:: The :attr:`~pymongo.collection.Collection.write_concern` of
           this collection is automatically applied to this operation (if the
           output is not inline) when using MongoDB >= 3.4.

        .. versionchanged:: 3.6
           Added ``session`` parameter.

        .. versionchanged:: 3.4
           Apply this collection's write concern automatically to this operation
           when connected to MongoDB >= 3.4.

        .. seealso:: :doc:`/examples/aggregation`

        .. versionchanged:: 3.4
           Added the `collation` option.
        .. versionchanged:: 2.2
           Removed deprecated arguments: merge_output and reduce_output

        .. _map reduce command: http://docs.mongodb.org/manual/reference/command/mapReduce/

        .. mongodoc:: mapreduce

        """
        if not isinstance(out, (string_type, abc.Mapping)):
            raise TypeError("'out' must be an instance of %s or a mapping" % (
             string_type.__name__,))
        else:
            response = (self._map_reduce)(map, reduce, out, session, 
             (ReadPreference.PRIMARY), **kwargs)
            return full_response or response.get('result') or response
        if isinstance(response['result'], dict):
            dbase = response['result']['db']
            coll = response['result']['collection']
            return self._Collection__database.client[dbase][coll]
        return self._Collection__database[response['result']]

    def inline_map_reduce(self, map, reduce, full_response=False, session=None, **kwargs):
        """Perform an inline map/reduce operation on this collection.

        Perform the map/reduce operation on the server in RAM. A result
        collection is not created. The result set is returned as a list
        of documents.

        If `full_response` is ``False`` (default) returns the
        result documents in a list. Otherwise, returns the full
        response from the server to the `map reduce command`_.

        The :meth:`inline_map_reduce` method obeys the :attr:`read_preference`
        of this :class:`Collection`.

        :Parameters:
          - `map`: map function (as a JavaScript string)
          - `reduce`: reduce function (as a JavaScript string)
          - `full_response` (optional): if ``True``, return full response to
            this command - otherwise just return the result collection
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.
          - `**kwargs` (optional): additional arguments to the
            `map reduce command`_ may be passed as keyword arguments to this
            helper method, e.g.::

            >>> db.test.inline_map_reduce(map, reduce, limit=2)

        .. versionchanged:: 3.6
           Added ``session`` parameter.

        .. versionchanged:: 3.4
           Added the `collation` option.

        """
        res = (self._map_reduce)(map, reduce, {'inline': 1}, session, 
         (self.read_preference), **kwargs)
        if full_response:
            return res
        return res.get('results')

    def _write_concern_for_cmd(self, cmd, session):
        raw_wc = cmd.get('writeConcern')
        if raw_wc is not None:
            return WriteConcern(**raw_wc)
        return self._write_concern_for(session)

    def __find_and_modify(self, filter, projection, sort, upsert=None, return_document=ReturnDocument.BEFORE, array_filters=None, session=None, **kwargs):
        """Internal findAndModify helper."""
        common.validate_is_mapping('filter', filter)
        if not isinstance(return_document, bool):
            raise ValueError('return_document must be ReturnDocument.BEFORE or ReturnDocument.AFTER')
        collation = validate_collation_or_none(kwargs.pop('collation', None))
        cmd = SON([('findAndModify', self._Collection__name),
         (
          'query', filter),
         (
          'new', return_document)])
        cmd.update(kwargs)
        if projection is not None:
            cmd['fields'] = helpers._fields_list_to_dict(projection, 'projection')
        if sort is not None:
            cmd['sort'] = helpers._index_document(sort)
        if upsert is not None:
            common.validate_boolean('upsert', upsert)
            cmd['upsert'] = upsert
        write_concern = self._write_concern_for_cmd(cmd, session)

        def _find_and_modify(session, sock_info, retryable_write):
            if array_filters is not None:
                if sock_info.max_wire_version < 6:
                    raise ConfigurationError('Must be connected to MongoDB 3.6+ to use arrayFilters.')
                if not write_concern.acknowledged:
                    raise ConfigurationError('arrayFilters is unsupported for unacknowledged writes.')
                cmd['arrayFilters'] = array_filters
            if sock_info.max_wire_version >= 4:
                if not write_concern.is_server_default:
                    cmd['writeConcern'] = write_concern.document
            out = self._command(sock_info, cmd, read_preference=(ReadPreference.PRIMARY),
              write_concern=write_concern,
              allowable_errors=[
             _NO_OBJ_ERROR],
              collation=collation,
              session=session,
              retryable_write=retryable_write,
              user_fields=_FIND_AND_MODIFY_DOC_FIELDS)
            _check_write_command_response(out)
            return out.get('value')

        return self._Collection__database.client._retryable_write(write_concern.acknowledged, _find_and_modify, session)

    def find_one_and_delete(self, filter, projection=None, sort=None, session=None, **kwargs):
        """Finds a single document and deletes it, returning the document.

          >>> db.test.count_documents({'x': 1})
          2
          >>> db.test.find_one_and_delete({'x': 1})
          {u'x': 1, u'_id': ObjectId('54f4e12bfba5220aa4d6dee8')}
          >>> db.test.count_documents({'x': 1})
          1

        If multiple documents match *filter*, a *sort* can be applied.

          >>> for doc in db.test.find({'x': 1}):
          ...     print(doc)
          ...
          {u'x': 1, u'_id': 0}
          {u'x': 1, u'_id': 1}
          {u'x': 1, u'_id': 2}
          >>> db.test.find_one_and_delete(
          ...     {'x': 1}, sort=[('_id', pymongo.DESCENDING)])
          {u'x': 1, u'_id': 2}

        The *projection* option can be used to limit the fields returned.

          >>> db.test.find_one_and_delete({'x': 1}, projection={'_id': False})
          {u'x': 1}

        :Parameters:
          - `filter`: A query that matches the document to delete.
          - `projection` (optional): a list of field names that should be
            returned in the result document or a mapping specifying the fields
            to include or exclude. If `projection` is a list "_id" will
            always be returned. Use a mapping to exclude fields from
            the result (e.g. projection={'_id': False}).
          - `sort` (optional): a list of (key, direction) pairs
            specifying the sort order for the query. If multiple documents
            match the query, they are sorted and the first is deleted.
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.
          - `**kwargs` (optional): additional command arguments can be passed
            as keyword arguments (for example maxTimeMS can be used with
            recent server versions).

        .. versionchanged:: 3.6
           Added ``session`` parameter.

        .. versionchanged:: 3.2
           Respects write concern.

        .. warning:: Starting in PyMongo 3.2, this command uses the
           :class:`~pymongo.write_concern.WriteConcern` of this
           :class:`~pymongo.collection.Collection` when connected to MongoDB >=
           3.2. Note that using an elevated write concern with this command may
           be slower compared to using the default write concern.

        .. versionchanged:: 3.4
           Added the `collation` option.
        .. versionadded:: 3.0

        """
        kwargs['remove'] = True
        return (self._Collection__find_and_modify)(filter, projection, sort, session=session, **kwargs)

    def find_one_and_replace(self, filter, replacement, projection=None, sort=None, upsert=False, return_document=ReturnDocument.BEFORE, session=None, **kwargs):
        """Finds a single document and replaces it, returning either the
        original or the replaced document.

        The :meth:`find_one_and_replace` method differs from
        :meth:`find_one_and_update` by replacing the document matched by
        *filter*, rather than modifying the existing document.

          >>> for doc in db.test.find({}):
          ...     print(doc)
          ...
          {u'x': 1, u'_id': 0}
          {u'x': 1, u'_id': 1}
          {u'x': 1, u'_id': 2}
          >>> db.test.find_one_and_replace({'x': 1}, {'y': 1})
          {u'x': 1, u'_id': 0}
          >>> for doc in db.test.find({}):
          ...     print(doc)
          ...
          {u'y': 1, u'_id': 0}
          {u'x': 1, u'_id': 1}
          {u'x': 1, u'_id': 2}

        :Parameters:
          - `filter`: A query that matches the document to replace.
          - `replacement`: The replacement document.
          - `projection` (optional): A list of field names that should be
            returned in the result document or a mapping specifying the fields
            to include or exclude. If `projection` is a list "_id" will
            always be returned. Use a mapping to exclude fields from
            the result (e.g. projection={'_id': False}).
          - `sort` (optional): a list of (key, direction) pairs
            specifying the sort order for the query. If multiple documents
            match the query, they are sorted and the first is replaced.
          - `upsert` (optional): When ``True``, inserts a new document if no
            document matches the query. Defaults to ``False``.
          - `return_document`: If
            :attr:`ReturnDocument.BEFORE` (the default),
            returns the original document before it was replaced, or ``None``
            if no document matches. If
            :attr:`ReturnDocument.AFTER`, returns the replaced
            or inserted document.
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.
          - `**kwargs` (optional): additional command arguments can be passed
            as keyword arguments (for example maxTimeMS can be used with
            recent server versions).

        .. versionchanged:: 3.6
           Added ``session`` parameter.
        .. versionchanged:: 3.4
           Added the `collation` option.
        .. versionchanged:: 3.2
           Respects write concern.

        .. warning:: Starting in PyMongo 3.2, this command uses the
           :class:`~pymongo.write_concern.WriteConcern` of this
           :class:`~pymongo.collection.Collection` when connected to MongoDB >=
           3.2. Note that using an elevated write concern with this command may
           be slower compared to using the default write concern.

        .. versionadded:: 3.0
        """
        common.validate_ok_for_replace(replacement)
        kwargs['update'] = replacement
        return (self._Collection__find_and_modify)(filter, projection,
 sort, upsert, return_document, session=session, **kwargs)

    def find_one_and_update(self, filter, update, projection=None, sort=None, upsert=False, return_document=ReturnDocument.BEFORE, array_filters=None, session=None, **kwargs):
        """Finds a single document and updates it, returning either the
        original or the updated document.

          >>> db.test.find_one_and_update(
          ...    {'_id': 665}, {'$inc': {'count': 1}, '$set': {'done': True}})
          {u'_id': 665, u'done': False, u'count': 25}}

        Returns ``None`` if no document matches the filter.

          >>> db.test.find_one_and_update(
          ...    {'_exists': False}, {'$inc': {'count': 1}})

        When the filter matches, by default :meth:`find_one_and_update`
        returns the original version of the document before the update was
        applied. To return the updated (or inserted in the case of
        *upsert*) version of the document instead, use the *return_document*
        option.

          >>> from pymongo import ReturnDocument
          >>> db.example.find_one_and_update(
          ...     {'_id': 'userid'},
          ...     {'$inc': {'seq': 1}},
          ...     return_document=ReturnDocument.AFTER)
          {u'_id': u'userid', u'seq': 1}

        You can limit the fields returned with the *projection* option.

          >>> db.example.find_one_and_update(
          ...     {'_id': 'userid'},
          ...     {'$inc': {'seq': 1}},
          ...     projection={'seq': True, '_id': False},
          ...     return_document=ReturnDocument.AFTER)
          {u'seq': 2}

        The *upsert* option can be used to create the document if it doesn't
        already exist.

          >>> db.example.delete_many({}).deleted_count
          1
          >>> db.example.find_one_and_update(
          ...     {'_id': 'userid'},
          ...     {'$inc': {'seq': 1}},
          ...     projection={'seq': True, '_id': False},
          ...     upsert=True,
          ...     return_document=ReturnDocument.AFTER)
          {u'seq': 1}

        If multiple documents match *filter*, a *sort* can be applied.

          >>> for doc in db.test.find({'done': True}):
          ...     print(doc)
          ...
          {u'_id': 665, u'done': True, u'result': {u'count': 26}}
          {u'_id': 701, u'done': True, u'result': {u'count': 17}}
          >>> db.test.find_one_and_update(
          ...     {'done': True},
          ...     {'$set': {'final': True}},
          ...     sort=[('_id', pymongo.DESCENDING)])
          {u'_id': 701, u'done': True, u'result': {u'count': 17}}

        :Parameters:
          - `filter`: A query that matches the document to update.
          - `update`: The update operations to apply.
          - `projection` (optional): A list of field names that should be
            returned in the result document or a mapping specifying the fields
            to include or exclude. If `projection` is a list "_id" will
            always be returned. Use a dict to exclude fields from
            the result (e.g. projection={'_id': False}).
          - `sort` (optional): a list of (key, direction) pairs
            specifying the sort order for the query. If multiple documents
            match the query, they are sorted and the first is updated.
          - `upsert` (optional): When ``True``, inserts a new document if no
            document matches the query. Defaults to ``False``.
          - `return_document`: If
            :attr:`ReturnDocument.BEFORE` (the default),
            returns the original document before it was updated. If
            :attr:`ReturnDocument.AFTER`, returns the updated
            or inserted document.
          - `array_filters` (optional): A list of filters specifying which
            array elements an update should apply. Requires MongoDB 3.6+.
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.
          - `**kwargs` (optional): additional command arguments can be passed
            as keyword arguments (for example maxTimeMS can be used with
            recent server versions).

        .. versionchanged:: 3.9
           Added the ability to accept a pipeline as the `update`.
        .. versionchanged:: 3.6
           Added the `array_filters` and `session` options.
        .. versionchanged:: 3.4
           Added the `collation` option.
        .. versionchanged:: 3.2
           Respects write concern.

        .. warning:: Starting in PyMongo 3.2, this command uses the
           :class:`~pymongo.write_concern.WriteConcern` of this
           :class:`~pymongo.collection.Collection` when connected to MongoDB >=
           3.2. Note that using an elevated write concern with this command may
           be slower compared to using the default write concern.

        .. versionadded:: 3.0
        """
        common.validate_ok_for_update(update)
        common.validate_list_or_none('array_filters', array_filters)
        kwargs['update'] = update
        return (self._Collection__find_and_modify)(filter, projection,
 sort, upsert, return_document,
 array_filters, session=session, **kwargs)

    def save(self, to_save, manipulate=True, check_keys=True, **kwargs):
        """Save a document in this collection.

        **DEPRECATED** - Use :meth:`insert_one` or :meth:`replace_one` instead.

        .. versionchanged:: 3.0
           Removed the `safe` parameter. Pass ``w=0`` for unacknowledged write
           operations.
        """
        warnings.warn('save is deprecated. Use insert_one or replace_one instead', DeprecationWarning,
          stacklevel=2)
        common.validate_is_document_type('to_save', to_save)
        write_concern = None
        collation = validate_collation_or_none(kwargs.pop('collation', None))
        if kwargs:
            write_concern = WriteConcern(**kwargs)
        if not isinstance(to_save, RawBSONDocument):
            if not '_id' in to_save:
                return self._insert(to_save, True, check_keys, manipulate, write_concern)
        self._update_retryable({'_id': to_save['_id']},
          to_save, True, check_keys,
          False, manipulate, write_concern, collation=collation)
        return to_save.get('_id')

    def insert(self, doc_or_docs, manipulate=True, check_keys=True, continue_on_error=False, **kwargs):
        """Insert a document(s) into this collection.

        **DEPRECATED** - Use :meth:`insert_one` or :meth:`insert_many` instead.

        .. versionchanged:: 3.0
           Removed the `safe` parameter. Pass ``w=0`` for unacknowledged write
           operations.
        """
        warnings.warn('insert is deprecated. Use insert_one or insert_many instead.', DeprecationWarning,
          stacklevel=2)
        write_concern = None
        if kwargs:
            write_concern = WriteConcern(**kwargs)
        return self._insert(doc_or_docs, not continue_on_error, check_keys, manipulate, write_concern)

    def update(self, spec, document, upsert=False, manipulate=False, multi=False, check_keys=True, **kwargs):
        """Update a document(s) in this collection.

        **DEPRECATED** - Use :meth:`replace_one`, :meth:`update_one`, or
        :meth:`update_many` instead.

        .. versionchanged:: 3.0
           Removed the `safe` parameter. Pass ``w=0`` for unacknowledged write
           operations.
        """
        warnings.warn('update is deprecated. Use replace_one, update_one or update_many instead.', DeprecationWarning,
          stacklevel=2)
        common.validate_is_mapping('spec', spec)
        common.validate_is_mapping('document', document)
        if document:
            first = next(iter(document))
            if first.startswith('$'):
                check_keys = False
        write_concern = None
        collation = validate_collation_or_none(kwargs.pop('collation', None))
        if kwargs:
            write_concern = WriteConcern(**kwargs)
        return self._update_retryable(spec,
          document, upsert, check_keys, multi, manipulate, write_concern,
          collation=collation)

    def remove(self, spec_or_id=None, multi=True, **kwargs):
        """Remove a document(s) from this collection.

        **DEPRECATED** - Use :meth:`delete_one` or :meth:`delete_many` instead.

        .. versionchanged:: 3.0
           Removed the `safe` parameter. Pass ``w=0`` for unacknowledged write
           operations.
        """
        warnings.warn('remove is deprecated. Use delete_one or delete_many instead.', DeprecationWarning,
          stacklevel=2)
        if spec_or_id is None:
            spec_or_id = {}
        if not isinstance(spec_or_id, abc.Mapping):
            spec_or_id = {'_id': spec_or_id}
        write_concern = None
        collation = validate_collation_or_none(kwargs.pop('collation', None))
        if kwargs:
            write_concern = WriteConcern(**kwargs)
        return self._delete_retryable(spec_or_id,
          multi, write_concern, collation=collation)

    def find_and_modify(self, query={}, update=None, upsert=False, sort=None, full_response=False, manipulate=False, **kwargs):
        """Update and return an object.

        **DEPRECATED** - Use :meth:`find_one_and_delete`,
        :meth:`find_one_and_replace`, or :meth:`find_one_and_update` instead.
        """
        warnings.warn('find_and_modify is deprecated, use find_one_and_delete, find_one_and_replace, or find_one_and_update instead', DeprecationWarning,
          stacklevel=2)
        if not update:
            if not kwargs.get('remove', None):
                raise ValueError('Must either update or remove')
        if update:
            if kwargs.get('remove', None):
                raise ValueError("Can't do both update and remove")
        elif query:
            kwargs['query'] = query
        else:
            if update:
                kwargs['update'] = update
            if upsert:
                kwargs['upsert'] = upsert
            if sort:
                if isinstance(sort, list):
                    kwargs['sort'] = helpers._index_document(sort)
                else:
                    if not (isinstance(sort, ORDERED_TYPES) or isinstance)(sort, dict) or len(sort) == 1:
                        warnings.warn('Passing mapping types for `sort` is deprecated, use a list of (key, direction) pairs instead', DeprecationWarning,
                          stacklevel=2)
                        kwargs['sort'] = sort
                    else:
                        raise TypeError('sort must be a list of (key, direction) pairs, a dict of len 1, or an instance of SON or OrderedDict')
        fields = kwargs.pop('fields', None)
        if fields is not None:
            kwargs['fields'] = helpers._fields_list_to_dict(fields, 'fields')
        collation = validate_collation_or_none(kwargs.pop('collation', None))
        cmd = SON([('findAndModify', self._Collection__name)])
        cmd.update(kwargs)
        write_concern = self._write_concern_for_cmd(cmd, None)

        def _find_and_modify(session, sock_info, retryable_write):
            if sock_info.max_wire_version >= 4:
                if not write_concern.is_server_default:
                    cmd['writeConcern'] = write_concern.document
            result = self._command(sock_info,
              cmd, read_preference=(ReadPreference.PRIMARY), allowable_errors=[
             _NO_OBJ_ERROR],
              collation=collation,
              session=session,
              retryable_write=retryable_write,
              user_fields=_FIND_AND_MODIFY_DOC_FIELDS)
            _check_write_command_response(result)
            return result

        out = self._Collection__database.client._retryable_write(write_concern.acknowledged, _find_and_modify, None)
        if not out['ok']:
            if out['errmsg'] == _NO_OBJ_ERROR:
                return
            raise ValueError('Unexpected Error: %s' % (out,))
        if full_response:
            return out
        document = out.get('value')
        if manipulate:
            document = self._Collection__database._fix_outgoing(document, self)
        return document

    def __iter__(self):
        return self

    def __next__(self):
        raise TypeError("'Collection' object is not iterable")

    next = __next__

    def __call__(self, *args, **kwargs):
        """This is only here so that some API misusages are easier to debug.
        """
        if '.' not in self._Collection__name:
            raise TypeError("'Collection' object is not callable. If you meant to call the '%s' method on a 'Database' object it is failing because no such method exists." % self._Collection__name)
        raise TypeError("'Collection' object is not callable. If you meant to call the '%s' method on a 'Collection' object it is failing because no such method exists." % self._Collection__name.split('.')[(-1)])