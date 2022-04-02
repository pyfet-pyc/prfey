# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pymongo\cursor.py
"""Cursor class to iterate over Mongo query results."""
import copy, warnings
from collections import deque
from bson import RE_TYPE
from bson.code import Code
from bson.py3compat import iteritems, integer_types, string_type
from bson.son import SON
from pymongo import helpers
from pymongo.common import validate_boolean, validate_is_mapping
from pymongo.collation import validate_collation_or_none
from pymongo.errors import ConnectionFailure, InvalidOperation, NotMasterError, OperationFailure
from pymongo.message import _CursorAddress, _GetMore, _RawBatchGetMore, _Query, _RawBatchQuery
from pymongo.monitoring import ConnectionClosedReason
_QUERY_OPTIONS = {'tailable_cursor':2, 
 'slave_okay':4, 
 'oplog_replay':8, 
 'no_timeout':16, 
 'await_data':32, 
 'exhaust':64, 
 'partial':128}

class CursorType(object):
    NON_TAILABLE = 0
    TAILABLE = _QUERY_OPTIONS['tailable_cursor']
    TAILABLE_AWAIT = TAILABLE | _QUERY_OPTIONS['await_data']
    EXHAUST = _QUERY_OPTIONS['exhaust']


class _SocketManager:
    __doc__ = 'Used with exhaust cursors to ensure the socket is returned.\n    '

    def __init__(self, sock, pool):
        self.sock = sock
        self.pool = pool
        self._SocketManager__closed = False

    def __del__(self):
        self.close()

    def close(self):
        """Return this instance's socket to the connection pool.
        """
        if not self._SocketManager__closed:
            self._SocketManager__closed = True
            self.pool.return_socket(self.sock)
            self.sock, self.pool = (None, None)


class Cursor(object):
    __doc__ = 'A cursor / iterator over Mongo query results.\n    '
    _query_class = _Query
    _getmore_class = _GetMore

    def __init__(self, collection, filter=None, projection=None, skip=0, limit=0, no_cursor_timeout=False, cursor_type=CursorType.NON_TAILABLE, sort=None, allow_partial_results=False, oplog_replay=False, modifiers=None, batch_size=0, manipulate=True, collation=None, hint=None, max_scan=None, max_time_ms=None, max=None, min=None, return_key=False, show_record_id=False, snapshot=False, comment=None, session=None):
        """Create a new cursor.

        Should not be called directly by application developers - see
        :meth:`~pymongo.collection.Collection.find` instead.

        .. mongodoc:: cursors
        """
        self._Cursor__id = None
        self._Cursor__exhaust = False
        self._Cursor__exhaust_mgr = None
        self._Cursor__killed = False
        if session:
            self._Cursor__session = session
            self._Cursor__explicit_session = True
        else:
            self._Cursor__session = None
            self._Cursor__explicit_session = False
        spec = filter
        if spec is None:
            spec = {}
        validate_is_mapping('filter', spec)
        if not isinstance(skip, int):
            raise TypeError('skip must be an instance of int')
        if not isinstance(limit, int):
            raise TypeError('limit must be an instance of int')
        validate_boolean('no_cursor_timeout', no_cursor_timeout)
        if cursor_type not in (CursorType.NON_TAILABLE, CursorType.TAILABLE,
         CursorType.TAILABLE_AWAIT, CursorType.EXHAUST):
            raise ValueError('not a valid value for cursor_type')
        validate_boolean('allow_partial_results', allow_partial_results)
        validate_boolean('oplog_replay', oplog_replay)
        if modifiers is not None:
            warnings.warn("the 'modifiers' parameter is deprecated", DeprecationWarning,
              stacklevel=2)
            validate_is_mapping('modifiers', modifiers)
        if not isinstance(batch_size, integer_types):
            raise TypeError('batch_size must be an integer')
        if batch_size < 0:
            raise ValueError('batch_size must be >= 0')
        if projection is not None:
            if not projection:
                projection = {'_id': 1}
            projection = helpers._fields_list_to_dict(projection, 'projection')
        self._Cursor__collection = collection
        self._Cursor__spec = spec
        self._Cursor__projection = projection
        self._Cursor__skip = skip
        self._Cursor__limit = limit
        self._Cursor__batch_size = batch_size
        self._Cursor__modifiers = modifiers and modifiers.copy() or {}
        self._Cursor__ordering = sort and helpers._index_document(sort) or None
        self._Cursor__max_scan = max_scan
        self._Cursor__explain = False
        self._Cursor__comment = comment
        self._Cursor__max_time_ms = max_time_ms
        self._Cursor__max_await_time_ms = None
        self._Cursor__max = max
        self._Cursor__min = min
        self._Cursor__manipulate = manipulate
        self._Cursor__collation = validate_collation_or_none(collation)
        self._Cursor__return_key = return_key
        self._Cursor__show_record_id = show_record_id
        self._Cursor__snapshot = snapshot
        self._Cursor__set_hint(hint)
        if cursor_type == CursorType.EXHAUST:
            if self._Cursor__collection.database.client.is_mongos:
                raise InvalidOperation('Exhaust cursors are not supported by mongos')
            if limit:
                raise InvalidOperation("Can't use limit and exhaust together.")
            self._Cursor__exhaust = True
        self._Cursor__empty = False
        self._Cursor__data = deque()
        self._Cursor__address = None
        self._Cursor__retrieved = 0
        self._Cursor__codec_options = collection.codec_options
        self._Cursor__read_preference = None
        self._Cursor__read_concern = collection.read_concern
        self._Cursor__query_flags = cursor_type
        if no_cursor_timeout:
            self._Cursor__query_flags |= _QUERY_OPTIONS['no_timeout']
        if allow_partial_results:
            self._Cursor__query_flags |= _QUERY_OPTIONS['partial']
        if oplog_replay:
            self._Cursor__query_flags |= _QUERY_OPTIONS['oplog_replay']

    @property
    def collection(self):
        """The :class:`~pymongo.collection.Collection` that this
        :class:`Cursor` is iterating.
        """
        return self._Cursor__collection

    @property
    def retrieved(self):
        """The number of documents retrieved so far.
        """
        return self._Cursor__retrieved

    def __del__(self):
        self._Cursor__die()

    def rewind(self):
        """Rewind this cursor to its unevaluated state.

        Reset this cursor if it has been partially or completely evaluated.
        Any options that are present on the cursor will remain in effect.
        Future iterating performed on this cursor will cause new queries to
        be sent to the server, even if the resultant data has already been
        retrieved by this cursor.
        """
        self._Cursor__data = deque()
        self._Cursor__id = None
        self._Cursor__address = None
        self._Cursor__retrieved = 0
        self._Cursor__killed = False
        return self

    def clone(self):
        """Get a clone of this cursor.

        Returns a new Cursor instance with options matching those that have
        been set on the current instance. The clone will be completely
        unevaluated, even if the current instance has been partially or
        completely evaluated.
        """
        return self._clone(True)

    def _clone(self, deepcopy=True, base=None):
        """Internal clone helper."""
        if not base:
            if self._Cursor__explicit_session:
                base = self._clone_base(self._Cursor__session)
            else:
                base = self._clone_base(None)
        values_to_clone = ('spec', 'projection', 'skip', 'limit', 'max_time_ms', 'max_await_time_ms',
                           'comment', 'max', 'min', 'ordering', 'explain', 'hint',
                           'batch_size', 'max_scan', 'manipulate', 'query_flags',
                           'modifiers', 'collation')
        data = dict(((k, v) for k, v in iteritems(self.__dict__) if k.startswith('_Cursor__') if k[9:] in values_to_clone))
        if deepcopy:
            data = self._deepcopy(data)
        base.__dict__.update(data)
        return base

    def _clone_base(self, session):
        """Creates an empty Cursor object for information to be copied into.
        """
        return self.__class__((self._Cursor__collection), session=session)

    def __die(self, synchronous=False):
        """Closes this cursor.
        """
        try:
            already_killed = self._Cursor__killed
        except AttributeError:
            return
        else:
            self._Cursor__killed = True
            if self._Cursor__id:
                if not already_killed:
                    if self._Cursor__exhaust and self._Cursor__exhaust_mgr:
                        self._Cursor__exhaust_mgr.sock.close_socket(ConnectionClosedReason.ERROR)
                    else:
                        address = _CursorAddress(self._Cursor__address, self._Cursor__collection.full_name)
                        if synchronous:
                            self._Cursor__collection.database.client._close_cursor_now((self._Cursor__id),
                              address, session=(self._Cursor__session))
                        else:
                            self._Cursor__collection.database.client._close_cursor(self._Cursor__id, address)
            if self._Cursor__exhaust:
                if self._Cursor__exhaust_mgr:
                    self._Cursor__exhaust_mgr.close()
            if self._Cursor__session:
                if not self._Cursor__explicit_session:
                    self._Cursor__session._end_session(lock=synchronous)
                    self._Cursor__session = None

    def close(self):
        """Explicitly close / kill this cursor.
        """
        self._Cursor__die(True)

    def __query_spec(self):
        """Get the spec to use for a query.
        """
        operators = self._Cursor__modifiers.copy()
        if self._Cursor__ordering:
            operators['$orderby'] = self._Cursor__ordering
        if self._Cursor__explain:
            operators['$explain'] = True
        if self._Cursor__hint:
            operators['$hint'] = self._Cursor__hint
        if self._Cursor__comment:
            operators['$comment'] = self._Cursor__comment
        if self._Cursor__max_scan:
            operators['$maxScan'] = self._Cursor__max_scan
        if self._Cursor__max_time_ms is not None:
            operators['$maxTimeMS'] = self._Cursor__max_time_ms
        if self._Cursor__max:
            operators['$max'] = self._Cursor__max
        if self._Cursor__min:
            operators['$min'] = self._Cursor__min
        if self._Cursor__return_key:
            operators['$returnKey'] = self._Cursor__return_key
        if self._Cursor__show_record_id:
            operators['$showDiskLoc'] = self._Cursor__show_record_id
        if self._Cursor__snapshot:
            operators['$snapshot'] = self._Cursor__snapshot
        if operators:
            spec = self._Cursor__spec.copy()
            if '$query' not in spec:
                spec = SON([('$query', spec)])
            if not isinstance(spec, SON):
                spec = SON(spec)
            spec.update(operators)
            return spec
        if 'query' in self._Cursor__spec and not len(self._Cursor__spec) == 1:
            if next(iter(self._Cursor__spec)) == 'query':
                return SON({'$query': self._Cursor__spec})
        return self._Cursor__spec

    def __check_okay_to_chain(self):
        """Check if it is okay to chain more options onto this cursor.
        """
        if self._Cursor__retrieved or self._Cursor__id is not None:
            raise InvalidOperation('cannot set options after executing query')

    def add_option(self, mask):
        """Set arbitrary query flags using a bitmask.

        To set the tailable flag:
        cursor.add_option(2)
        """
        if not isinstance(mask, int):
            raise TypeError('mask must be an int')
        self._Cursor__check_okay_to_chain()
        if mask & _QUERY_OPTIONS['exhaust']:
            if self._Cursor__limit:
                raise InvalidOperation("Can't use limit and exhaust together.")
            if self._Cursor__collection.database.client.is_mongos:
                raise InvalidOperation('Exhaust cursors are not supported by mongos')
            self._Cursor__exhaust = True
        self._Cursor__query_flags |= mask
        return self

    def remove_option(self, mask):
        """Unset arbitrary query flags using a bitmask.

        To unset the tailable flag:
        cursor.remove_option(2)
        """
        if not isinstance(mask, int):
            raise TypeError('mask must be an int')
        self._Cursor__check_okay_to_chain()
        if mask & _QUERY_OPTIONS['exhaust']:
            self._Cursor__exhaust = False
        self._Cursor__query_flags &= ~mask
        return self

    def limit(self, limit):
        """Limits the number of results to be returned by this cursor.

        Raises :exc:`TypeError` if `limit` is not an integer. Raises
        :exc:`~pymongo.errors.InvalidOperation` if this :class:`Cursor`
        has already been used. The last `limit` applied to this cursor
        takes precedence. A limit of ``0`` is equivalent to no limit.

        :Parameters:
          - `limit`: the number of results to return

        .. mongodoc:: limit
        """
        if not isinstance(limit, integer_types):
            raise TypeError('limit must be an integer')
        if self._Cursor__exhaust:
            raise InvalidOperation("Can't use limit and exhaust together.")
        self._Cursor__check_okay_to_chain()
        self._Cursor__empty = False
        self._Cursor__limit = limit
        return self

    def batch_size(self, batch_size):
        """Limits the number of documents returned in one batch. Each batch
        requires a round trip to the server. It can be adjusted to optimize
        performance and limit data transfer.

        .. note:: batch_size can not override MongoDB's internal limits on the
           amount of data it will return to the client in a single batch (i.e
           if you set batch size to 1,000,000,000, MongoDB will currently only
           return 4-16MB of results per batch).

        Raises :exc:`TypeError` if `batch_size` is not an integer.
        Raises :exc:`ValueError` if `batch_size` is less than ``0``.
        Raises :exc:`~pymongo.errors.InvalidOperation` if this
        :class:`Cursor` has already been used. The last `batch_size`
        applied to this cursor takes precedence.

        :Parameters:
          - `batch_size`: The size of each batch of results requested.
        """
        if not isinstance(batch_size, integer_types):
            raise TypeError('batch_size must be an integer')
        if batch_size < 0:
            raise ValueError('batch_size must be >= 0')
        self._Cursor__check_okay_to_chain()
        self._Cursor__batch_size = batch_size
        return self

    def skip(self, skip):
        """Skips the first `skip` results of this cursor.

        Raises :exc:`TypeError` if `skip` is not an integer. Raises
        :exc:`ValueError` if `skip` is less than ``0``. Raises
        :exc:`~pymongo.errors.InvalidOperation` if this :class:`Cursor` has
        already been used. The last `skip` applied to this cursor takes
        precedence.

        :Parameters:
          - `skip`: the number of results to skip
        """
        if not isinstance(skip, integer_types):
            raise TypeError('skip must be an integer')
        if skip < 0:
            raise ValueError('skip must be >= 0')
        self._Cursor__check_okay_to_chain()
        self._Cursor__skip = skip
        return self

    def max_time_ms(self, max_time_ms):
        """Specifies a time limit for a query operation. If the specified
        time is exceeded, the operation will be aborted and
        :exc:`~pymongo.errors.ExecutionTimeout` is raised. If `max_time_ms`
        is ``None`` no limit is applied.

        Raises :exc:`TypeError` if `max_time_ms` is not an integer or ``None``.
        Raises :exc:`~pymongo.errors.InvalidOperation` if this :class:`Cursor`
        has already been used.

        :Parameters:
          - `max_time_ms`: the time limit after which the operation is aborted
        """
        if not isinstance(max_time_ms, integer_types):
            if max_time_ms is not None:
                raise TypeError('max_time_ms must be an integer or None')
        self._Cursor__check_okay_to_chain()
        self._Cursor__max_time_ms = max_time_ms
        return self

    def max_await_time_ms(self, max_await_time_ms):
        """Specifies a time limit for a getMore operation on a
        :attr:`~pymongo.cursor.CursorType.TAILABLE_AWAIT` cursor. For all other
        types of cursor max_await_time_ms is ignored.

        Raises :exc:`TypeError` if `max_await_time_ms` is not an integer or
        ``None``. Raises :exc:`~pymongo.errors.InvalidOperation` if this
        :class:`Cursor` has already been used.

        .. note:: `max_await_time_ms` requires server version **>= 3.2**

        :Parameters:
          - `max_await_time_ms`: the time limit after which the operation is
            aborted

        .. versionadded:: 3.2
        """
        if not isinstance(max_await_time_ms, integer_types):
            if max_await_time_ms is not None:
                raise TypeError('max_await_time_ms must be an integer or None')
        self._Cursor__check_okay_to_chain()
        if self._Cursor__query_flags & CursorType.TAILABLE_AWAIT:
            self._Cursor__max_await_time_ms = max_await_time_ms
        return self

    def __getitem__(self, index):
        """Get a single document or a slice of documents from this cursor.

        Raises :class:`~pymongo.errors.InvalidOperation` if this
        cursor has already been used.

        To get a single document use an integral index, e.g.::

          >>> db.test.find()[50]

        An :class:`IndexError` will be raised if the index is negative
        or greater than the amount of documents in this cursor. Any
        limit previously applied to this cursor will be ignored.

        To get a slice of documents use a slice index, e.g.::

          >>> db.test.find()[20:25]

        This will return this cursor with a limit of ``5`` and skip of
        ``20`` applied.  Using a slice index will override any prior
        limits or skips applied to this cursor (including those
        applied through previous calls to this method). Raises
        :class:`IndexError` when the slice has a step, a negative
        start value, or a stop value less than or equal to the start
        value.

        :Parameters:
          - `index`: An integer or slice index to be applied to this cursor
        """
        self._Cursor__check_okay_to_chain()
        self._Cursor__empty = False
        if isinstance(index, slice):
            if index.step is not None:
                raise IndexError('Cursor instances do not support slice steps')
            else:
                skip = 0
                if index.start is not None:
                    if index.start < 0:
                        raise IndexError('Cursor instances do not support negative indices')
                    skip = index.start
                elif index.stop is not None:
                    limit = index.stop - skip
                    if limit < 0:
                        raise IndexError('stop index must be greater than start index for slice %r' % index)
                    if limit == 0:
                        self._Cursor__empty = True
                else:
                    limit = 0
            self._Cursor__skip = skip
            self._Cursor__limit = limit
            return self
        if isinstance(index, integer_types):
            if index < 0:
                raise IndexError('Cursor instances do not support negative indices')
            clone = self.clone()
            clone.skip(index + self._Cursor__skip)
            clone.limit(-1)
            clone._Cursor__query_flags &= ~CursorType.TAILABLE_AWAIT
            for doc in clone:
                return doc
                raise IndexError('no such item for Cursor instance')

        raise TypeError('index %r cannot be applied to Cursor instances' % index)

    def max_scan(self, max_scan):
        """**DEPRECATED** - Limit the number of documents to scan when
        performing the query.

        Raises :class:`~pymongo.errors.InvalidOperation` if this
        cursor has already been used. Only the last :meth:`max_scan`
        applied to this cursor has any effect.

        :Parameters:
          - `max_scan`: the maximum number of documents to scan

        .. versionchanged:: 3.7
          Deprecated :meth:`max_scan`. Support for this option is deprecated in
          MongoDB 4.0. Use :meth:`max_time_ms` instead to limit server side
          execution time.
        """
        self._Cursor__check_okay_to_chain()
        self._Cursor__max_scan = max_scan
        return self

    def max(self, spec):
        """Adds ``max`` operator that specifies upper bound for specific index.

        When using ``max``, :meth:`~hint` should also be configured to ensure
        the query uses the expected index and starting in MongoDB 4.2
        :meth:`~hint` will be required.

        :Parameters:
          - `spec`: a list of field, limit pairs specifying the exclusive
            upper bound for all keys of a specific index in order.

        .. versionchanged:: 3.8
           Deprecated cursors that use ``max`` without a :meth:`~hint`.

        .. versionadded:: 2.7
        """
        if not isinstance(spec, (list, tuple)):
            raise TypeError('spec must be an instance of list or tuple')
        self._Cursor__check_okay_to_chain()
        self._Cursor__max = SON(spec)
        return self

    def min(self, spec):
        """Adds ``min`` operator that specifies lower bound for specific index.

        When using ``min``, :meth:`~hint` should also be configured to ensure
        the query uses the expected index and starting in MongoDB 4.2
        :meth:`~hint` will be required.

        :Parameters:
          - `spec`: a list of field, limit pairs specifying the inclusive
            lower bound for all keys of a specific index in order.

        .. versionchanged:: 3.8
           Deprecated cursors that use ``min`` without a :meth:`~hint`.

        .. versionadded:: 2.7
        """
        if not isinstance(spec, (list, tuple)):
            raise TypeError('spec must be an instance of list or tuple')
        self._Cursor__check_okay_to_chain()
        self._Cursor__min = SON(spec)
        return self

    def sort(self, key_or_list, direction=None):
        """Sorts this cursor's results.

        Pass a field name and a direction, either
        :data:`~pymongo.ASCENDING` or :data:`~pymongo.DESCENDING`::

            for doc in collection.find().sort('field', pymongo.ASCENDING):
                print(doc)

        To sort by multiple fields, pass a list of (key, direction) pairs::

            for doc in collection.find().sort([
                    ('field1', pymongo.ASCENDING),
                    ('field2', pymongo.DESCENDING)]):
                print(doc)

        Beginning with MongoDB version 2.6, text search results can be
        sorted by relevance::

            cursor = db.test.find(
                {'$text': {'$search': 'some words'}},
                {'score': {'$meta': 'textScore'}})

            # Sort by 'score' field.
            cursor.sort([('score', {'$meta': 'textScore'})])

            for doc in cursor:
                print(doc)

        Raises :class:`~pymongo.errors.InvalidOperation` if this cursor has
        already been used. Only the last :meth:`sort` applied to this
        cursor has any effect.

        :Parameters:
          - `key_or_list`: a single key or a list of (key, direction)
            pairs specifying the keys to sort on
          - `direction` (optional): only used if `key_or_list` is a single
            key, if not given :data:`~pymongo.ASCENDING` is assumed
        """
        self._Cursor__check_okay_to_chain()
        keys = helpers._index_list(key_or_list, direction)
        self._Cursor__ordering = helpers._index_document(keys)
        return self

    def count(self, with_limit_and_skip=False):
        """**DEPRECATED** - Get the size of the results set for this query.

        The :meth:`count` method is deprecated and **not** supported in a
        transaction. Please use
        :meth:`~pymongo.collection.Collection.count_documents` instead.

        Returns the number of documents in the results set for this query. Does
        not take :meth:`limit` and :meth:`skip` into account by default - set
        `with_limit_and_skip` to ``True`` if that is the desired behavior.
        Raises :class:`~pymongo.errors.OperationFailure` on a database error.

        When used with MongoDB >= 2.6, :meth:`~count` uses any :meth:`~hint`
        applied to the query. In the following example the hint is passed to
        the count command:

          collection.find({'field': 'value'}).hint('field_1').count()

        The :meth:`count` method obeys the
        :attr:`~pymongo.collection.Collection.read_preference` of the
        :class:`~pymongo.collection.Collection` instance on which
        :meth:`~pymongo.collection.Collection.find` was called.

        :Parameters:
          - `with_limit_and_skip` (optional): take any :meth:`limit` or
            :meth:`skip` that has been applied to this cursor into account when
            getting the count

        .. note:: The `with_limit_and_skip` parameter requires server
           version **>= 1.1.4-**

        .. versionchanged:: 3.7
           Deprecated.

        .. versionchanged:: 2.8
           The :meth:`~count` method now supports :meth:`~hint`.
        """
        warnings.warn('count is deprecated. Use Collection.count_documents instead.', DeprecationWarning,
          stacklevel=2)
        validate_boolean('with_limit_and_skip', with_limit_and_skip)
        cmd = SON([('count', self._Cursor__collection.name),
         (
          'query', self._Cursor__spec)])
        if self._Cursor__max_time_ms is not None:
            cmd['maxTimeMS'] = self._Cursor__max_time_ms
        if self._Cursor__comment:
            cmd['comment'] = self._Cursor__comment
        if self._Cursor__hint is not None:
            cmd['hint'] = self._Cursor__hint
        if with_limit_and_skip:
            if self._Cursor__limit:
                cmd['limit'] = self._Cursor__limit
            if self._Cursor__skip:
                cmd['skip'] = self._Cursor__skip
        return self._Cursor__collection._count(cmd,
          (self._Cursor__collation), session=(self._Cursor__session))

    def distinct(self, key):
        """Get a list of distinct values for `key` among all documents
        in the result set of this query.

        Raises :class:`TypeError` if `key` is not an instance of
        :class:`basestring` (:class:`str` in python 3).

        The :meth:`distinct` method obeys the
        :attr:`~pymongo.collection.Collection.read_preference` of the
        :class:`~pymongo.collection.Collection` instance on which
        :meth:`~pymongo.collection.Collection.find` was called.

        :Parameters:
          - `key`: name of key for which we want to get the distinct values

        .. seealso:: :meth:`pymongo.collection.Collection.distinct`
        """
        options = {}
        if self._Cursor__spec:
            options['query'] = self._Cursor__spec
        if self._Cursor__max_time_ms is not None:
            options['maxTimeMS'] = self._Cursor__max_time_ms
        if self._Cursor__comment:
            options['comment'] = self._Cursor__comment
        if self._Cursor__collation is not None:
            options['collation'] = self._Cursor__collation
        return (self._Cursor__collection.distinct)(
 key, session=self._Cursor__session, **options)

    def explain(self):
        """Returns an explain plan record for this cursor.

        .. note:: Starting with MongoDB 3.2 :meth:`explain` uses
          the default verbosity mode of the `explain command
          <https://docs.mongodb.com/manual/reference/command/explain/>`_,
          ``allPlansExecution``. To use a different verbosity use
          :meth:`~pymongo.database.Database.command` to run the explain
          command directly.

        .. mongodoc:: explain
        """
        c = self.clone()
        c._Cursor__explain = True
        if c._Cursor__limit:
            c._Cursor__limit = -abs(c._Cursor__limit)
        return next(c)

    def __set_hint(self, index):
        if index is None:
            self._Cursor__hint = None
            return
        elif isinstance(index, string_type):
            self._Cursor__hint = index
        else:
            self._Cursor__hint = helpers._index_document(index)

    def hint(self, index):
        """Adds a 'hint', telling Mongo the proper index to use for the query.

        Judicious use of hints can greatly improve query
        performance. When doing a query on multiple fields (at least
        one of which is indexed) pass the indexed field as a hint to
        the query. Raises :class:`~pymongo.errors.OperationFailure` if the
        provided hint requires an index that does not exist on this collection,
        and raises :class:`~pymongo.errors.InvalidOperation` if this cursor has
        already been used.

        `index` should be an index as passed to
        :meth:`~pymongo.collection.Collection.create_index`
        (e.g. ``[('field', ASCENDING)]``) or the name of the index.
        If `index` is ``None`` any existing hint for this query is
        cleared. The last hint applied to this cursor takes precedence
        over all others.

        :Parameters:
          - `index`: index to hint on (as an index specifier)

        .. versionchanged:: 2.8
           The :meth:`~hint` method accepts the name of the index.
        """
        self._Cursor__check_okay_to_chain()
        self._Cursor__set_hint(index)
        return self

    def comment(self, comment):
        """Adds a 'comment' to the cursor.

        http://docs.mongodb.org/manual/reference/operator/comment/

        :Parameters:
          - `comment`: A string to attach to the query to help interpret and
            trace the operation in the server logs and in profile data.

        .. versionadded:: 2.7
        """
        self._Cursor__check_okay_to_chain()
        self._Cursor__comment = comment
        return self

    def where(self, code):
        """Adds a $where clause to this query.

        The `code` argument must be an instance of :class:`basestring`
        (:class:`str` in python 3) or :class:`~bson.code.Code`
        containing a JavaScript expression. This expression will be
        evaluated for each document scanned. Only those documents
        for which the expression evaluates to *true* will be returned
        as results. The keyword *this* refers to the object currently
        being scanned.

        Raises :class:`TypeError` if `code` is not an instance of
        :class:`basestring` (:class:`str` in python 3). Raises
        :class:`~pymongo.errors.InvalidOperation` if this
        :class:`Cursor` has already been used. Only the last call to
        :meth:`where` applied to a :class:`Cursor` has any effect.

        :Parameters:
          - `code`: JavaScript expression to use as a filter
        """
        self._Cursor__check_okay_to_chain()
        if not isinstance(code, Code):
            code = Code(code)
        self._Cursor__spec['$where'] = code
        return self

    def collation(self, collation):
        """Adds a :class:`~pymongo.collation.Collation` to this query.

        This option is only supported on MongoDB 3.4 and above.

        Raises :exc:`TypeError` if `collation` is not an instance of
        :class:`~pymongo.collation.Collation` or a ``dict``. Raises
        :exc:`~pymongo.errors.InvalidOperation` if this :class:`Cursor` has
        already been used. Only the last collation applied to this cursor has
        any effect.

        :Parameters:
          - `collation`: An instance of :class:`~pymongo.collation.Collation`.
        """
        self._Cursor__check_okay_to_chain()
        self._Cursor__collation = validate_collation_or_none(collation)
        return self

    def __send_message--- This code section failed: ---

 L. 946         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _Cursor__collection
                4  LOAD_ATTR                database
                6  LOAD_ATTR                client
                8  STORE_FAST               'client'

 L. 948        10  LOAD_FAST                'client'
               12  LOAD_ATTR                _encrypter
               14  POP_JUMP_IF_FALSE    30  'to 30'
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _Cursor__exhaust
               20  POP_JUMP_IF_FALSE    30  'to 30'

 L. 949        22  LOAD_GLOBAL              InvalidOperation

 L. 950        24  LOAD_STR                 'exhaust cursors do not support auto encryption'

 L. 949        26  CALL_FUNCTION_1       1  ''
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            20  '20'
             30_1  COME_FROM            14  '14'

 L. 952        30  SETUP_FINALLY        60  'to 60'

 L. 953        32  LOAD_FAST                'client'
               34  LOAD_ATTR                _run_operation_with_response

 L. 954        36  LOAD_FAST                'operation'

 L. 954        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _unpack_response

 L. 954        42  LOAD_FAST                'self'
               44  LOAD_ATTR                _Cursor__exhaust

 L. 955        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _Cursor__address

 L. 953        50  LOAD_CONST               ('exhaust', 'address')
               52  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               54  STORE_FAST               'response'
               56  POP_BLOCK        
               58  JUMP_FORWARD        212  'to 212'
             60_0  COME_FROM_FINALLY    30  '30'

 L. 956        60  DUP_TOP          
               62  LOAD_GLOBAL              OperationFailure
               64  COMPARE_OP               exception-match
               66  POP_JUMP_IF_FALSE   114  'to 114'
               68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          

 L. 957        74  LOAD_CONST               True
               76  LOAD_FAST                'self'
               78  STORE_ATTR               _Cursor__killed

 L. 960        80  LOAD_FAST                'self'
               82  LOAD_METHOD              _Cursor__die
               84  CALL_METHOD_0         0  ''
               86  POP_TOP          

 L. 966        88  LOAD_FAST                'self'
               90  LOAD_ATTR                _Cursor__query_flags
               92  LOAD_GLOBAL              _QUERY_OPTIONS
               94  LOAD_STR                 'tailable_cursor'
               96  BINARY_SUBSCR    
               98  BINARY_AND       
              100  POP_JUMP_IF_FALSE   108  'to 108'

 L. 967       102  POP_EXCEPT       
              104  LOAD_CONST               None
              106  RETURN_VALUE     
            108_0  COME_FROM           100  '100'

 L. 968       108  RAISE_VARARGS_0       0  'reraise'
              110  POP_EXCEPT       
              112  JUMP_FORWARD        212  'to 212'
            114_0  COME_FROM            66  '66'

 L. 969       114  DUP_TOP          
              116  LOAD_GLOBAL              NotMasterError
              118  COMPARE_OP               exception-match
              120  POP_JUMP_IF_FALSE   148  'to 148'
              122  POP_TOP          
              124  POP_TOP          
              126  POP_TOP          

 L. 972       128  LOAD_CONST               True
              130  LOAD_FAST                'self'
              132  STORE_ATTR               _Cursor__killed

 L. 975       134  LOAD_FAST                'self'
              136  LOAD_METHOD              _Cursor__die
              138  CALL_METHOD_0         0  ''
              140  POP_TOP          

 L. 977       142  RAISE_VARARGS_0       0  'reraise'
              144  POP_EXCEPT       
              146  JUMP_FORWARD        212  'to 212'
            148_0  COME_FROM           120  '120'

 L. 978       148  DUP_TOP          
              150  LOAD_GLOBAL              ConnectionFailure
              152  COMPARE_OP               exception-match
              154  POP_JUMP_IF_FALSE   182  'to 182'
              156  POP_TOP          
              158  POP_TOP          
              160  POP_TOP          

 L. 983       162  LOAD_CONST               True
              164  LOAD_FAST                'self'
              166  STORE_ATTR               _Cursor__killed

 L. 984       168  LOAD_FAST                'self'
              170  LOAD_METHOD              _Cursor__die
              172  CALL_METHOD_0         0  ''
              174  POP_TOP          

 L. 985       176  RAISE_VARARGS_0       0  'reraise'
              178  POP_EXCEPT       
              180  JUMP_FORWARD        212  'to 212'
            182_0  COME_FROM           154  '154'

 L. 986       182  DUP_TOP          
              184  LOAD_GLOBAL              Exception
              186  COMPARE_OP               exception-match
              188  POP_JUMP_IF_FALSE   210  'to 210'
              190  POP_TOP          
              192  POP_TOP          
              194  POP_TOP          

 L. 988       196  LOAD_FAST                'self'
              198  LOAD_METHOD              _Cursor__die
              200  CALL_METHOD_0         0  ''
              202  POP_TOP          

 L. 989       204  RAISE_VARARGS_0       0  'reraise'
              206  POP_EXCEPT       
              208  JUMP_FORWARD        212  'to 212'
            210_0  COME_FROM           188  '188'
              210  END_FINALLY      
            212_0  COME_FROM           208  '208'
            212_1  COME_FROM           180  '180'
            212_2  COME_FROM           146  '146'
            212_3  COME_FROM           112  '112'
            212_4  COME_FROM            58  '58'

 L. 991       212  LOAD_FAST                'response'
              214  LOAD_ATTR                address
              216  LOAD_FAST                'self'
              218  STORE_ATTR               _Cursor__address

 L. 992       220  LOAD_FAST                'self'
              222  LOAD_ATTR                _Cursor__exhaust
              224  POP_JUMP_IF_FALSE   248  'to 248'
              226  LOAD_FAST                'self'
              228  LOAD_ATTR                _Cursor__exhaust_mgr
              230  POP_JUMP_IF_TRUE    248  'to 248'

 L. 994       232  LOAD_GLOBAL              _SocketManager
              234  LOAD_FAST                'response'
              236  LOAD_ATTR                socket_info

 L. 995       238  LOAD_FAST                'response'
              240  LOAD_ATTR                pool

 L. 994       242  CALL_FUNCTION_2       2  ''
              244  LOAD_FAST                'self'
              246  STORE_ATTR               _Cursor__exhaust_mgr
            248_0  COME_FROM           230  '230'
            248_1  COME_FROM           224  '224'

 L. 997       248  LOAD_FAST                'operation'
              250  LOAD_ATTR                name
              252  STORE_FAST               'cmd_name'

 L. 998       254  LOAD_FAST                'response'
              256  LOAD_ATTR                docs
              258  STORE_FAST               'docs'

 L. 999       260  LOAD_FAST                'response'
              262  LOAD_ATTR                from_command
          264_266  POP_JUMP_IF_FALSE   394  'to 394'

 L.1000       268  LOAD_FAST                'cmd_name'
              270  LOAD_STR                 'explain'
              272  COMPARE_OP               !=
          274_276  POP_JUMP_IF_FALSE   358  'to 358'

 L.1001       278  LOAD_FAST                'docs'
              280  LOAD_CONST               0
              282  BINARY_SUBSCR    
              284  LOAD_STR                 'cursor'
              286  BINARY_SUBSCR    
              288  STORE_FAST               'cursor'

 L.1002       290  LOAD_FAST                'cursor'
              292  LOAD_STR                 'id'
              294  BINARY_SUBSCR    
              296  LOAD_FAST                'self'
              298  STORE_ATTR               _Cursor__id

 L.1003       300  LOAD_FAST                'cmd_name'
              302  LOAD_STR                 'find'
              304  COMPARE_OP               ==
          306_308  POP_JUMP_IF_FALSE   320  'to 320'

 L.1004       310  LOAD_FAST                'cursor'
              312  LOAD_STR                 'firstBatch'
              314  BINARY_SUBSCR    
              316  STORE_FAST               'documents'
              318  JUMP_FORWARD        328  'to 328'
            320_0  COME_FROM           306  '306'

 L.1006       320  LOAD_FAST                'cursor'
              322  LOAD_STR                 'nextBatch'
              324  BINARY_SUBSCR    
              326  STORE_FAST               'documents'
            328_0  COME_FROM           318  '318'

 L.1007       328  LOAD_GLOBAL              deque
              330  LOAD_FAST                'documents'
              332  CALL_FUNCTION_1       1  ''
              334  LOAD_FAST                'self'
              336  STORE_ATTR               _Cursor__data

 L.1008       338  LOAD_FAST                'self'
              340  DUP_TOP          
              342  LOAD_ATTR                _Cursor__retrieved
              344  LOAD_GLOBAL              len
              346  LOAD_FAST                'documents'
              348  CALL_FUNCTION_1       1  ''
              350  INPLACE_ADD      
              352  ROT_TWO          
              354  STORE_ATTR               _Cursor__retrieved
              356  JUMP_FORWARD        392  'to 392'
            358_0  COME_FROM           274  '274'

 L.1010       358  LOAD_CONST               0
              360  LOAD_FAST                'self'
              362  STORE_ATTR               _Cursor__id

 L.1011       364  LOAD_GLOBAL              deque
              366  LOAD_FAST                'docs'
              368  CALL_FUNCTION_1       1  ''
              370  LOAD_FAST                'self'
              372  STORE_ATTR               _Cursor__data

 L.1012       374  LOAD_FAST                'self'
              376  DUP_TOP          
              378  LOAD_ATTR                _Cursor__retrieved
              380  LOAD_GLOBAL              len
              382  LOAD_FAST                'docs'
              384  CALL_FUNCTION_1       1  ''
              386  INPLACE_ADD      
              388  ROT_TWO          
              390  STORE_ATTR               _Cursor__retrieved
            392_0  COME_FROM           356  '356'
              392  JUMP_FORWARD        432  'to 432'
            394_0  COME_FROM           264  '264'

 L.1014       394  LOAD_FAST                'response'
              396  LOAD_ATTR                data
              398  LOAD_ATTR                cursor_id
              400  LOAD_FAST                'self'
              402  STORE_ATTR               _Cursor__id

 L.1015       404  LOAD_GLOBAL              deque
              406  LOAD_FAST                'docs'
              408  CALL_FUNCTION_1       1  ''
              410  LOAD_FAST                'self'
              412  STORE_ATTR               _Cursor__data

 L.1016       414  LOAD_FAST                'self'
              416  DUP_TOP          
              418  LOAD_ATTR                _Cursor__retrieved
              420  LOAD_FAST                'response'
              422  LOAD_ATTR                data
              424  LOAD_ATTR                number_returned
              426  INPLACE_ADD      
              428  ROT_TWO          
              430  STORE_ATTR               _Cursor__retrieved
            432_0  COME_FROM           392  '392'

 L.1018       432  LOAD_FAST                'self'
              434  LOAD_ATTR                _Cursor__id
              436  LOAD_CONST               0
              438  COMPARE_OP               ==
          440_442  POP_JUMP_IF_FALSE   458  'to 458'

 L.1019       444  LOAD_CONST               True
              446  LOAD_FAST                'self'
              448  STORE_ATTR               _Cursor__killed

 L.1022       450  LOAD_FAST                'self'
              452  LOAD_METHOD              _Cursor__die
              454  CALL_METHOD_0         0  ''
              456  POP_TOP          
            458_0  COME_FROM           440  '440'

 L.1024       458  LOAD_FAST                'self'
              460  LOAD_ATTR                _Cursor__limit
          462_464  POP_JUMP_IF_FALSE   496  'to 496'
              466  LOAD_FAST                'self'
              468  LOAD_ATTR                _Cursor__id
          470_472  POP_JUMP_IF_FALSE   496  'to 496'
              474  LOAD_FAST                'self'
              476  LOAD_ATTR                _Cursor__limit
              478  LOAD_FAST                'self'
              480  LOAD_ATTR                _Cursor__retrieved
              482  COMPARE_OP               <=
          484_486  POP_JUMP_IF_FALSE   496  'to 496'

 L.1025       488  LOAD_FAST                'self'
              490  LOAD_METHOD              _Cursor__die
              492  CALL_METHOD_0         0  ''
              494  POP_TOP          
            496_0  COME_FROM           484  '484'
            496_1  COME_FROM           470  '470'
            496_2  COME_FROM           462  '462'

Parse error at or near `LOAD_CONST' instruction at offset 104

    def _unpack_response(self, response, cursor_id, codec_options, user_fields=None, legacy_response=False):
        return response.unpack_response(cursor_id, codec_options, user_fields, legacy_response)

    def _read_preference(self):
        if self._Cursor__read_preference is None:
            self._Cursor__read_preference = self._Cursor__collection._read_preference_for(self.session)
        return self._Cursor__read_preference

    def _refresh(self):
        """Refreshes the cursor with more data from Mongo.

        Returns the length of self.__data after refresh. Will exit early if
        self.__data is already non-empty. Raises OperationFailure when the
        cursor cannot be refreshed due to an error on the query.
        """
        if len(self._Cursor__data) or self._Cursor__killed:
            return len(self._Cursor__data)
        if not self._Cursor__session:
            self._Cursor__session = self._Cursor__collection.database.client._ensure_session()
        if self._Cursor__id is None:
            if self._Cursor__min or self._Cursor__max:
                if not self._Cursor__hint:
                    warnings.warn('using a min/max query operator without specifying a Cursor.hint is deprecated. A hint will be required when using min/max in PyMongo 4.0', DeprecationWarning,
                      stacklevel=3)
            q = self._query_class(self._Cursor__query_flags, self._Cursor__collection.database.name, self._Cursor__collection.name, self._Cursor__skip, self._Cursor__query_spec(), self._Cursor__projection, self._Cursor__codec_options, self._read_preference(), self._Cursor__limit, self._Cursor__batch_size, self._Cursor__read_concern, self._Cursor__collation, self._Cursor__session, self._Cursor__collection.database.client)
            self._Cursor__send_message(q)
        else:
            if self._Cursor__id:
                if self._Cursor__limit:
                    limit = self._Cursor__limit - self._Cursor__retrieved
                    if self._Cursor__batch_size:
                        limit = min(limit, self._Cursor__batch_size)
                else:
                    limit = self._Cursor__batch_size
                g = self._getmore_class(self._Cursor__collection.database.name, self._Cursor__collection.name, limit, self._Cursor__id, self._Cursor__codec_options, self._read_preference(), self._Cursor__session, self._Cursor__collection.database.client, self._Cursor__max_await_time_ms, self._Cursor__exhaust_mgr)
                self._Cursor__send_message(g)
            return len(self._Cursor__data)

    @property
    def alive(self):
        """Does this cursor have the potential to return more data?

        This is mostly useful with `tailable cursors
        <http://www.mongodb.org/display/DOCS/Tailable+Cursors>`_
        since they will stop iterating even though they *may* return more
        results in the future.

        With regular cursors, simply use a for loop instead of :attr:`alive`::

            for doc in collection.find():
                print(doc)

        .. note:: Even if :attr:`alive` is True, :meth:`next` can raise
          :exc:`StopIteration`. :attr:`alive` can also be True while iterating
          a cursor from a failed server. In this case :attr:`alive` will
          return False after :meth:`next` fails to retrieve the next batch
          of results from the server.
        """
        return bool(len(self._Cursor__data) or not self._Cursor__killed)

    @property
    def cursor_id(self):
        """Returns the id of the cursor

        Useful if you need to manage cursor ids and want to handle killing
        cursors manually using
        :meth:`~pymongo.mongo_client.MongoClient.kill_cursors`

        .. versionadded:: 2.2
        """
        return self._Cursor__id

    @property
    def address(self):
        """The (host, port) of the server used, or None.

        .. versionchanged:: 3.0
           Renamed from "conn_id".
        """
        return self._Cursor__address

    @property
    def session(self):
        """The cursor's :class:`~pymongo.client_session.ClientSession`, or None.

        .. versionadded:: 3.6
        """
        if self._Cursor__explicit_session:
            return self._Cursor__session

    def __iter__(self):
        return self

    def next(self):
        """Advance the cursor."""
        if self._Cursor__empty:
            raise StopIteration
        elif len(self._Cursor__data) or self._refresh():
            if self._Cursor__manipulate:
                _db = self._Cursor__collection.database
                return _db._fix_outgoing(self._Cursor__data.popleft(), self._Cursor__collection)
            return self._Cursor__data.popleft()
        else:
            raise StopIteration

    __next__ = next

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __copy__(self):
        """Support function for `copy.copy()`.

        .. versionadded:: 2.4
        """
        return self._clone(deepcopy=False)

    def __deepcopy__(self, memo):
        """Support function for `copy.deepcopy()`.

        .. versionadded:: 2.4
        """
        return self._clone(deepcopy=True)

    def _deepcopy(self, x, memo=None):
        """Deepcopy helper for the data dictionary or list.

        Regular expressions cannot be deep copied but as they are immutable we
        don't have to copy them when cloning.
        """
        if not hasattr(x, 'items'):
            y, is_list, iterator = [], True, enumerate(x)
        else:
            y, is_list, iterator = {}, False, iteritems(x)
        if memo is None:
            memo = {}
        val_id = id(x)
        if val_id in memo:
            return memo.get(val_id)
        memo[val_id] = y
        for key, value in iterator:
            if isinstance(value, (dict, list)):
                value = isinstance(value, SON) or self._deepcopy(value, memo)
            else:
                if not isinstance(value, RE_TYPE):
                    value = copy.deepcopy(value, memo)
                else:
                    if is_list:
                        y.append(value)
                if not isinstance(key, RE_TYPE):
                    key = copy.deepcopy(key, memo)
                y[key] = value
        else:
            return y


class RawBatchCursor(Cursor):
    __doc__ = 'A cursor / iterator over raw batches of BSON data from a query result.'
    _query_class = _RawBatchQuery
    _getmore_class = _RawBatchGetMore

    def __init__(self, *args, **kwargs):
        manipulate = kwargs.get('manipulate')
        kwargs['manipulate'] = False
        (super(RawBatchCursor, self).__init__)(*args, **kwargs)
        if manipulate:
            raise InvalidOperation('Cannot use RawBatchCursor with manipulate=True')

    def _unpack_response(self, response, cursor_id, codec_options, user_fields=None, legacy_response=False):
        return response.raw_response(cursor_id)

    def explain(self):
        """Returns an explain plan record for this cursor.

        .. mongodoc:: explain
        """
        clone = self._clone(deepcopy=True, base=(Cursor(self.collection)))
        return clone.explain()

    def __getitem__(self, index):
        raise InvalidOperation('Cannot call __getitem__ on RawBatchCursor')