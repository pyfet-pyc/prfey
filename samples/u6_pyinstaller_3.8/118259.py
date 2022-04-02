# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pymongo\change_stream.py
"""Watch changes on a collection, a database, or the entire cluster."""
import copy
from bson import _bson_to_dict
from bson.raw_bson import RawBSONDocument
from pymongo import common
from pymongo.aggregation import _CollectionAggregationCommand, _DatabaseAggregationCommand
from pymongo.collation import validate_collation_or_none
from pymongo.command_cursor import CommandCursor
from pymongo.errors import ConnectionFailure, InvalidOperation, OperationFailure, PyMongoError
_NON_RESUMABLE_GETMORE_ERRORS = frozenset([
 11601,
 136,
 237,
 None])

class ChangeStream(object):
    __doc__ = 'The internal abstract base class for change stream cursors.\n\n    Should not be called directly by application developers. Use \n    :meth:`pymongo.collection.Collection.watch`,\n    :meth:`pymongo.database.Database.watch`, or\n    :meth:`pymongo.mongo_client.MongoClient.watch` instead.\n\n    .. versionadded:: 3.6\n    .. mongodoc:: changeStreams\n    '

    def __init__(self, target, pipeline, full_document, resume_after, max_await_time_ms, batch_size, collation, start_at_operation_time, session, start_after):
        if pipeline is None:
            pipeline = []
        else:
            if not isinstance(pipeline, list):
                raise TypeError('pipeline must be a list')
            else:
                common.validate_string_or_none('full_document', full_document)
                validate_collation_or_none(collation)
                common.validate_non_negative_integer_or_none('batchSize', batch_size)
                self._decode_custom = False
                self._orig_codec_options = target.codec_options
                if target.codec_options.type_registry._decoder_map:
                    self._decode_custom = True
                    self._target = target.with_options(codec_options=target.codec_options.with_options(document_class=RawBSONDocument))
                else:
                    self._target = target
            self._pipeline = copy.deepcopy(pipeline)
            self._full_document = full_document
            self._uses_start_after = start_after is not None
            self._uses_resume_after = resume_after is not None
            self._resume_token = copy.deepcopy(start_after or resume_after)
            self._max_await_time_ms = max_await_time_ms
            self._batch_size = batch_size
            self._collation = collation
            self._start_at_operation_time = start_at_operation_time
            self._session = session
            self._cursor = self._create_cursor()

    @property
    def _aggregation_command_class(self):
        """The aggregation command class to be used."""
        raise NotImplementedError

    @property
    def _client(self):
        """The client against which the aggregation commands for
        this ChangeStream will be run. """
        raise NotImplementedError

    def _change_stream_options(self):
        """Return the options dict for the $changeStream pipeline stage."""
        options = {}
        if self._full_document is not None:
            options['fullDocument'] = self._full_document
        resume_token = self.resume_token
        if resume_token is not None:
            if self._uses_start_after:
                options['startAfter'] = resume_token
            if self._uses_resume_after:
                options['resumeAfter'] = resume_token
        if self._start_at_operation_time is not None:
            options['startAtOperationTime'] = self._start_at_operation_time
        return options

    def _command_options(self):
        """Return the options dict for the aggregation command."""
        options = {}
        if self._max_await_time_ms is not None:
            options['maxAwaitTimeMS'] = self._max_await_time_ms
        if self._batch_size is not None:
            options['batchSize'] = self._batch_size
        return options

    def _aggregation_pipeline(self):
        """Return the full aggregation pipeline for this ChangeStream."""
        options = self._change_stream_options()
        full_pipeline = [{'$changeStream': options}]
        full_pipeline.extend(self._pipeline)
        return full_pipeline

    def _process_result(self, result, session, server, sock_info, slave_ok):
        """Callback that caches the startAtOperationTime from a changeStream
        aggregate command response containing an empty batch of change
        documents.

        This is implemented as a callback because we need access to the wire
        version in order to determine whether to cache this value.
        """
        if not result['cursor']['firstBatch']:
            if self._start_at_operation_time is None:
                if self.resume_token is None:
                    if sock_info.max_wire_version >= 7:
                        self._start_at_operation_time = result['operationTime']

    def _run_aggregation_cmd(self, session, explicit_session):
        """Run the full aggregation pipeline for this ChangeStream and return
        the corresponding CommandCursor.
        """
        cmd = self._aggregation_command_class((self._target),
          CommandCursor, (self._aggregation_pipeline()), (self._command_options()),
          explicit_session, result_processor=(self._process_result))
        return self._client._retryable_read(cmd.get_cursor, self._target._read_preference_for(session), session)

    def _create_cursor--- This code section failed: ---

 L. 164         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _client
                4  LOAD_ATTR                _tmp_session
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                _session
               10  LOAD_CONST               False
               12  LOAD_CONST               ('close',)
               14  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               16  SETUP_WITH           52  'to 52'
               18  STORE_FAST               's'

 L. 165        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _run_aggregation_cmd

 L. 166        24  LOAD_FAST                's'

 L. 167        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _session
               30  LOAD_CONST               None
               32  COMPARE_OP               is-not

 L. 165        34  LOAD_CONST               ('session', 'explicit_session')
               36  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               38  POP_BLOCK        
               40  ROT_TWO          
               42  BEGIN_FINALLY    
               44  WITH_CLEANUP_START
               46  WITH_CLEANUP_FINISH
               48  POP_FINALLY           0  ''
               50  RETURN_VALUE     
             52_0  COME_FROM_WITH       16  '16'
               52  WITH_CLEANUP_START
               54  WITH_CLEANUP_FINISH
               56  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 40

    def _resume(self):
        """Reestablish this change stream after a resumable error."""
        try:
            self._cursor.close()
        except PyMongoError:
            pass
        else:
            self._cursor = self._create_cursor()

    def close(self):
        """Close this ChangeStream."""
        self._cursor.close()

    def __iter__(self):
        return self

    @property
    def resume_token(self):
        """The cached resume token that will be used to resume after the most
        recently returned change.

        .. versionadded:: 3.9
        """
        return copy.deepcopy(self._resume_token)

    def next(self):
        """Advance the cursor.

        This method blocks until the next change document is returned or an
        unrecoverable error is raised. This method is used when iterating over
        all changes in the cursor. For example::

            try:
                resume_token = None
                pipeline = [{'$match': {'operationType': 'insert'}}]
                with db.collection.watch(pipeline) as stream:
                    for insert_change in stream:
                        print(insert_change)
                        resume_token = stream.resume_token
            except pymongo.errors.PyMongoError:
                # The ChangeStream encountered an unrecoverable error or the
                # resume attempt failed to recreate the cursor.
                if resume_token is None:
                    # There is no usable resume token because there was a
                    # failure during ChangeStream initialization.
                    logging.error('...')
                else:
                    # Use the interrupted ChangeStream's resume token to create
                    # a new ChangeStream. The new stream will continue from the
                    # last seen insert change without missing any events.
                    with db.collection.watch(
                            pipeline, resume_after=resume_token) as stream:
                        for insert_change in stream:
                            print(insert_change)

        Raises :exc:`StopIteration` if this ChangeStream is closed.
        """
        while self.alive:
            doc = self.try_next()
            if doc is not None:
                return doc

        raise StopIteration

    __next__ = next

    @property
    def alive(self):
        """Does this cursor have the potential to return more data?

        .. note:: Even if :attr:`alive` is ``True``, :meth:`next` can raise
            :exc:`StopIteration` and :meth:`try_next` can return ``None``.

        .. versionadded:: 3.8
        """
        return self._cursor.alive

    def try_next(self):
        """Advance the cursor without blocking indefinitely.

        This method returns the next change document without waiting
        indefinitely for the next change. For example::

            with db.collection.watch() as stream:
                while stream.alive:
                    change = stream.try_next()
                    # Note that the ChangeStream's resume token may be updated
                    # even when no changes are returned.
                    print("Current resume token: %r" % (stream.resume_token,))
                    if change is not None:
                        print("Change document: %r" % (change,))
                        continue
                    # We end up here when there are no recent changes.
                    # Sleep for a while before trying again to avoid flooding
                    # the server with getMore requests when no changes are
                    # available.
                    time.sleep(10)

        If no change document is cached locally then this method runs a single
        getMore command. If the getMore yields any documents, the next
        document is returned, otherwise, if the getMore returns no documents
        (because there have been no changes) then ``None`` is returned.

        :Returns:
          The next change document or ``None`` when no document is available
          after running a single getMore or when the cursor is closed.

        .. versionadded:: 3.8
        """
        try:
            change = self._cursor._try_next(True)
        except ConnectionFailure:
            self._resume()
            change = self._cursor._try_next(False)
        except OperationFailure as exc:
            try:
                if exc.code in _NON_RESUMABLE_GETMORE_ERRORS or exc.has_error_label('NonResumableChangeStreamError'):
                    raise
                self._resume()
                change = self._cursor._try_next(False)
            finally:
                exc = None
                del exc

        else:
            if change is None:
                if self._cursor._post_batch_resume_token is not None:
                    self._resume_token = self._cursor._post_batch_resume_token
                    self._start_at_operation_time = None
                return change
            try:
                resume_token = change['_id']
            except KeyError:
                self.close()
                raise InvalidOperation('Cannot provide resume functionality when the resume token is missing.')
            else:
                if not self._cursor._has_next():
                    if self._cursor._post_batch_resume_token:
                        resume_token = self._cursor._post_batch_resume_token
                self._uses_start_after = False
                self._uses_resume_after = True
                self._resume_token = resume_token
                self._start_at_operation_time = None
                if self._decode_custom:
                    return _bson_to_dict(change.raw, self._orig_codec_options)
                return change

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class CollectionChangeStream(ChangeStream):
    __doc__ = 'A change stream that watches changes on a single collection.\n\n    Should not be called directly by application developers. Use\n    helper method :meth:`pymongo.collection.Collection.watch` instead.\n\n    .. versionadded:: 3.7\n    '

    @property
    def _aggregation_command_class(self):
        return _CollectionAggregationCommand

    @property
    def _client(self):
        return self._target.database.client


class DatabaseChangeStream(ChangeStream):
    __doc__ = 'A change stream that watches changes on all collections in a database.\n\n    Should not be called directly by application developers. Use\n    helper method :meth:`pymongo.database.Database.watch` instead.\n\n    .. versionadded:: 3.7\n    '

    @property
    def _aggregation_command_class(self):
        return _DatabaseAggregationCommand

    @property
    def _client(self):
        return self._target.client


class ClusterChangeStream(DatabaseChangeStream):
    __doc__ = 'A change stream that watches changes on all collections in the cluster.\n\n    Should not be called directly by application developers. Use\n    helper method :meth:`pymongo.mongo_client.MongoClient.watch` instead.\n\n    .. versionadded:: 3.7\n    '

    def _change_stream_options(self):
        options = super(ClusterChangeStream, self)._change_stream_options()
        options['allChangesForCluster'] = True
        return options