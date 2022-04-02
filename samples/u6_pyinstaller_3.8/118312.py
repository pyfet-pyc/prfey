# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pymysql\cursors.py
from __future__ import print_function, absolute_import
from functools import partial
import re, warnings
from ._compat import range_type, text_type, PY2
from . import err
RE_INSERT_VALUES = re.compile('\\s*((?:INSERT|REPLACE)\\b.+\\bVALUES?\\s*)(\\(\\s*(?:%s|%\\(.+\\)s)\\s*(?:,\\s*(?:%s|%\\(.+\\)s)\\s*)*\\))(\\s*(?:ON DUPLICATE.*)?);?\\s*\\Z', re.IGNORECASE | re.DOTALL)

class Cursor(object):
    __doc__ = '\n    This is the object you use to interact with the database.\n\n    Do not create an instance of a Cursor yourself. Call\n    connections.Connection.cursor().\n\n    See `Cursor <https://www.python.org/dev/peps/pep-0249/#cursor-objects>`_ in\n    the specification.\n    '
    max_stmt_length = 1024000
    _defer_warnings = False

    def __init__(self, connection):
        self.connection = connection
        self.description = None
        self.rownumber = 0
        self.rowcount = -1
        self.arraysize = 1
        self._executed = None
        self._result = None
        self._rows = None
        self._warnings_handled = False

    def close(self):
        """
        Closing a cursor just exhausts all remaining data.
        """
        conn = self.connection
        if conn is None:
            return
        try:
            while self.nextset():
                pass

        finally:
            self.connection = None

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        del exc_info
        self.close()

    def _get_db(self):
        if not self.connection:
            raise err.ProgrammingError('Cursor closed')
        return self.connection

    def _check_executed(self):
        if not self._executed:
            raise err.ProgrammingError('execute() first')

    def _conv_row(self, row):
        return row

    def setinputsizes(self, *args):
        """Does nothing, required by DB API."""
        pass

    def setoutputsizes(self, *args):
        """Does nothing, required by DB API."""
        pass

    def _nextset(self, unbuffered=False):
        """Get the next query set"""
        conn = self._get_db()
        current_result = self._result
        if unbuffered:
            self._show_warnings()
        else:
            if current_result is None or current_result is not conn._result:
                return
            return current_result.has_next or None
        self._result = None
        self._clear_result()
        conn.next_result(unbuffered=unbuffered)
        self._do_get_result()
        return True

    def nextset(self):
        return self._nextset(False)

    def _ensure_bytes(self, x, encoding=None):
        if isinstance(x, text_type):
            x = x.encode(encoding)
        else:
            if isinstance(x, (tuple, list)):
                x = type(x)((self._ensure_bytes(v, encoding=encoding) for v in x))
        return x

    def _escape_args--- This code section failed: ---

 L. 117         0  LOAD_GLOBAL              partial
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _ensure_bytes
                6  LOAD_DEREF               'conn'
                8  LOAD_ATTR                encoding
               10  LOAD_CONST               ('encoding',)
               12  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               14  STORE_DEREF              'ensure_bytes'

 L. 119        16  LOAD_GLOBAL              isinstance
               18  LOAD_FAST                'args'
               20  LOAD_GLOBAL              tuple
               22  LOAD_GLOBAL              list
               24  BUILD_TUPLE_2         2 
               26  CALL_FUNCTION_2       2  ''
               28  POP_JUMP_IF_FALSE    70  'to 70'

 L. 120        30  LOAD_GLOBAL              PY2
               32  POP_JUMP_IF_FALSE    48  'to 48'

 L. 121        34  LOAD_GLOBAL              tuple
               36  LOAD_GLOBAL              map
               38  LOAD_DEREF               'ensure_bytes'
               40  LOAD_FAST                'args'
               42  CALL_FUNCTION_2       2  ''
               44  CALL_FUNCTION_1       1  ''
               46  STORE_FAST               'args'
             48_0  COME_FROM            32  '32'

 L. 122        48  LOAD_GLOBAL              tuple
               50  LOAD_CLOSURE             'conn'
               52  BUILD_TUPLE_1         1 
               54  LOAD_GENEXPR             '<code_object <genexpr>>'
               56  LOAD_STR                 'Cursor._escape_args.<locals>.<genexpr>'
               58  MAKE_FUNCTION_8          'closure'
               60  LOAD_FAST                'args'
               62  GET_ITER         
               64  CALL_FUNCTION_1       1  ''
               66  CALL_FUNCTION_1       1  ''
               68  RETURN_VALUE     
             70_0  COME_FROM            28  '28'

 L. 123        70  LOAD_GLOBAL              isinstance
               72  LOAD_FAST                'args'
               74  LOAD_GLOBAL              dict
               76  CALL_FUNCTION_2       2  ''
               78  POP_JUMP_IF_FALSE   128  'to 128'

 L. 124        80  LOAD_GLOBAL              PY2
               82  POP_JUMP_IF_FALSE   106  'to 106'

 L. 125        84  LOAD_CLOSURE             'ensure_bytes'
               86  BUILD_TUPLE_1         1 
               88  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               90  LOAD_STR                 'Cursor._escape_args.<locals>.<dictcomp>'
               92  MAKE_FUNCTION_8          'closure'

 L. 126        94  LOAD_FAST                'args'
               96  LOAD_METHOD              items
               98  CALL_METHOD_0         0  ''

 L. 125       100  GET_ITER         
              102  CALL_FUNCTION_1       1  ''
              104  STORE_FAST               'args'
            106_0  COME_FROM            82  '82'

 L. 127       106  LOAD_CLOSURE             'conn'
              108  BUILD_TUPLE_1         1 
              110  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              112  LOAD_STR                 'Cursor._escape_args.<locals>.<dictcomp>'
              114  MAKE_FUNCTION_8          'closure'
              116  LOAD_FAST                'args'
              118  LOAD_METHOD              items
              120  CALL_METHOD_0         0  ''
              122  GET_ITER         
              124  CALL_FUNCTION_1       1  ''
              126  RETURN_VALUE     
            128_0  COME_FROM            78  '78'

 L. 131       128  LOAD_GLOBAL              PY2
              130  POP_JUMP_IF_FALSE   140  'to 140'

 L. 132       132  LOAD_DEREF               'ensure_bytes'
              134  LOAD_FAST                'args'
              136  CALL_FUNCTION_1       1  ''
              138  STORE_FAST               'args'
            140_0  COME_FROM           130  '130'

 L. 133       140  LOAD_DEREF               'conn'
              142  LOAD_METHOD              escape
              144  LOAD_FAST                'args'
              146  CALL_METHOD_1         1  ''
              148  RETURN_VALUE     

Parse error at or near `LOAD_DICTCOMP' instruction at offset 88

    def mogrify(self, query, args=None):
        """
        Returns the exact string that is sent to the database by calling the
        execute() method.

        This method follows the extension to the DB API 2.0 followed by Psycopg.
        """
        conn = self._get_db()
        if PY2:
            query = self._ensure_bytes(query, encoding=(conn.encoding))
        if args is not None:
            query = query % self._escape_args(args, conn)
        return query

    def execute(self, query, args=None):
        """Execute a query

        :param str query: Query to execute.

        :param args: parameters used with query. (optional)
        :type args: tuple, list or dict

        :return: Number of affected rows
        :rtype: int

        If args is a list or tuple, %s can be used as a placeholder in the query.
        If args is a dict, %(name)s can be used as a placeholder in the query.
        """
        while self.nextset():
            pass

        query = self.mogrify(query, args)
        result = self._query(query)
        self._executed = query
        return result

    def executemany(self, query, args):
        """Run several data against one query

        :param query: query to execute on server
        :param args:  Sequence of sequences or mappings.  It is used as parameter.
        :return: Number of rows affected, if any.

        This method improves performance on multiple-row INSERT and
        REPLACE. Otherwise it is equivalent to looping over args with
        execute().
        """
        if not args:
            return
        m = RE_INSERT_VALUES.match(query)
        if m:
            q_prefix = m.group(1) % ()
            q_values = m.group(2).rstrip()
            q_postfix = m.group(3) or ''
            if not (q_values[0] == '(' and q_values[(-1)] == ')'):
                raise AssertionError
            return self._do_execute_many(q_prefix, q_values, q_postfix, args, self.max_stmt_length, self._get_db().encoding)
        self.rowcount = sum((self.execute(query, arg) for arg in args))
        return self.rowcount

    def _do_execute_many(self, prefix, values, postfix, args, max_stmt_length, encoding):
        conn = self._get_db()
        escape = self._escape_args
        if isinstance(prefix, text_type):
            prefix = prefix.encode(encoding)
        else:
            if PY2:
                if isinstance(values, text_type):
                    values = values.encode(encoding)
            if isinstance(postfix, text_type):
                postfix = postfix.encode(encoding)
            sql = bytearray(prefix)
            args = iter(args)
            v = values % escape(next(args), conn)
            if isinstance(v, text_type):
                if PY2:
                    v = v.encode(encoding)
                else:
                    v = v.encode(encoding, 'surrogateescape')
        sql += v
        rows = 0
        for arg in args:
            v = values % escape(arg, conn)
            if isinstance(v, text_type):
                if PY2:
                    v = v.encode(encoding)
                else:
                    v = v.encode(encoding, 'surrogateescape')
            elif len(sql) + len(v) + len(postfix) + 1 > max_stmt_length:
                rows += self.execute(sql + postfix)
                sql = bytearray(prefix)
            else:
                sql += b','
            sql += v
        else:
            rows += self.execute(sql + postfix)
            self.rowcount = rows
            return rows

    def callproc(self, procname, args=()):
        """Execute stored procedure procname with args

        procname -- string, name of procedure to execute on server

        args -- Sequence of parameters to use with procedure

        Returns the original args.

        Compatibility warning: PEP-249 specifies that any modified
        parameters must be returned. This is currently impossible
        as they are only available by storing them in a server
        variable and then retrieved by a query. Since stored
        procedures return zero or more result sets, there is no
        reliable way to get at OUT or INOUT parameters via callproc.
        The server variables are named @_procname_n, where procname
        is the parameter above and n is the position of the parameter
        (from zero). Once all result sets generated by the procedure
        have been fetched, you can issue a SELECT @_procname_0, ...
        query using .execute() to get any OUT or INOUT values.

        Compatibility warning: The act of calling a stored procedure
        itself creates an empty result set. This appears after any
        result sets generated by the procedure. This is non-standard
        behavior with respect to the DB-API. Be sure to use nextset()
        to advance through all result sets; otherwise you may get
        disconnected.
        """
        conn = self._get_db()
        if args:
            fmt = '@_{0}_%d=%s'.format(procname)
            self._query('SET %s' % ','.join((fmt % (index, conn.escape(arg)) for index, arg in enumerate(args))))
            self.nextset()
        q = 'CALL %s(%s)' % (procname,
         ','.join(['@_%s_%d' % (procname, i) for i in range_type(len(args))]))
        self._query(q)
        self._executed = q
        return args

    def fetchone(self):
        """Fetch the next row"""
        self._check_executed()
        if self._rows is None or self.rownumber >= len(self._rows):
            return
        result = self._rows[self.rownumber]
        self.rownumber += 1
        return result

    def fetchmany(self, size=None):
        """Fetch several rows"""
        self._check_executed()
        if self._rows is None:
            return ()
        end = self.rownumber + (size or self.arraysize)
        result = self._rows[self.rownumber:end]
        self.rownumber = min(end, len(self._rows))
        return result

    def fetchall(self):
        """Fetch all the rows"""
        self._check_executed()
        if self._rows is None:
            return ()
        elif self.rownumber:
            result = self._rows[self.rownumber:]
        else:
            result = self._rows
        self.rownumber = len(self._rows)
        return result

    def scroll(self, value, mode='relative'):
        self._check_executed()
        if mode == 'relative':
            r = self.rownumber + value
        else:
            if mode == 'absolute':
                r = value
            else:
                raise err.ProgrammingError('unknown scroll mode %s' % mode)
        if not 0 <= r < len(self._rows):
            raise IndexError('out of range')
        self.rownumber = r

    def _query(self, q):
        conn = self._get_db()
        self._last_executed = q
        self._clear_result()
        conn.query(q)
        self._do_get_result()
        return self.rowcount

    def _clear_result(self):
        self.rownumber = 0
        self._result = None
        self.rowcount = 0
        self.description = None
        self.lastrowid = None
        self._rows = None

    def _do_get_result(self):
        conn = self._get_db()
        self._result = result = conn._result
        self.rowcount = result.affected_rows
        self.description = result.description
        self.lastrowid = result.insert_id
        self._rows = result.rows
        self._warnings_handled = False
        if not self._defer_warnings:
            self._show_warnings()

    def _show_warnings(self):
        if self._warnings_handled:
            return
        self._warnings_handled = True
        if self._result:
            return self._result.has_next or self._result.warning_count or None
        ws = self._get_db().show_warnings()
        if ws is None:
            return
        for w in ws:
            msg = w[(-1)]
            if PY2:
                if isinstance(msg, unicode):
                    msg = msg.encode('utf-8', 'replace')
            warnings.warn((err.Warning)(*w[1:3]), stacklevel=4)

    def __iter__(self):
        return iter(self.fetchone, None)

    Warning = err.Warning
    Error = err.Error
    InterfaceError = err.InterfaceError
    DatabaseError = err.DatabaseError
    DataError = err.DataError
    OperationalError = err.OperationalError
    IntegrityError = err.IntegrityError
    InternalError = err.InternalError
    ProgrammingError = err.ProgrammingError
    NotSupportedError = err.NotSupportedError


class DictCursorMixin(object):
    dict_type = dict

    def _do_get_result(self):
        super(DictCursorMixin, self)._do_get_result()
        fields = []
        if self.description:
            for f in self._result.fields:
                name = f.name
                if name in fields:
                    name = f.table_name + '.' + name
                fields.append(name)
            else:
                self._fields = fields

        if fields:
            if self._rows:
                self._rows = [self._conv_row(r) for r in self._rows]

    def _conv_row(self, row):
        if row is None:
            return
        return self.dict_type(zip(self._fields, row))


class DictCursor(DictCursorMixin, Cursor):
    __doc__ = 'A cursor which returns results as a dictionary'


class SSCursor(Cursor):
    __doc__ = "\n    Unbuffered Cursor, mainly useful for queries that return a lot of data,\n    or for connections to remote servers over a slow network.\n\n    Instead of copying every row of data into a buffer, this will fetch\n    rows as needed. The upside of this is the client uses much less memory,\n    and rows are returned much faster when traveling over a slow network\n    or if the result set is very big.\n\n    There are limitations, though. The MySQL protocol doesn't support\n    returning the total number of rows, so the only way to tell how many rows\n    there are is to iterate over every row returned. Also, it currently isn't\n    possible to scroll backwards, as only the current row is held in memory.\n    "
    _defer_warnings = True

    def _conv_row(self, row):
        return row

    def close(self):
        conn = self.connection
        if conn is None:
            return
        if self._result is not None:
            if self._result is conn._result:
                self._result._finish_unbuffered_query()
        try:
            while self.nextset():
                pass

        finally:
            self.connection = None

    __del__ = close

    def _query(self, q):
        conn = self._get_db()
        self._last_executed = q
        self._clear_result()
        conn.query(q, unbuffered=True)
        self._do_get_result()
        return self.rowcount

    def nextset(self):
        return self._nextset(unbuffered=True)

    def read_next(self):
        """Read next row"""
        return self._conv_row(self._result._read_rowdata_packet_unbuffered())

    def fetchone(self):
        """Fetch next row"""
        self._check_executed()
        row = self.read_next()
        if row is None:
            self._show_warnings()
            return None
        self.rownumber += 1
        return row

    def fetchall(self):
        """
        Fetch all, as per MySQLdb. Pretty useless for large queries, as
        it is buffered. See fetchall_unbuffered(), if you want an unbuffered
        generator version of this method.
        """
        return list(self.fetchall_unbuffered())

    def fetchall_unbuffered(self):
        """
        Fetch all, implemented as a generator, which isn't to standard,
        however, it doesn't make sense to return everything in a list, as that
        would use ridiculous memory for large result sets.
        """
        return iter(self.fetchone, None)

    def __iter__(self):
        return self.fetchall_unbuffered()

    def fetchmany(self, size=None):
        """Fetch many"""
        self._check_executed()
        if size is None:
            size = self.arraysize
        rows = []
        for i in range_type(size):
            row = self.read_next()
            if row is None:
                self._show_warnings()
                break
            rows.append(row)
            self.rownumber += 1
        else:
            return rows

    def scroll(self, value, mode='relative'):
        self._check_executed()
        if mode == 'relative':
            if value < 0:
                raise err.NotSupportedError('Backwards scrolling not supported by this cursor')
            for _ in range_type(value):
                self.read_next()
            else:
                self.rownumber += value

        else:
            if mode == 'absolute':
                if value < self.rownumber:
                    raise err.NotSupportedError('Backwards scrolling not supported by this cursor')
                end = value - self.rownumber
                for _ in range_type(end):
                    self.read_next()
                else:
                    self.rownumber = value

            else:
                raise err.ProgrammingError('unknown scroll mode %s' % mode)


class SSDictCursor(DictCursorMixin, SSCursor):
    __doc__ = 'An unbuffered cursor, which returns results as a dictionary'