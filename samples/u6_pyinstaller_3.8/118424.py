# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\websockets\http.py
"""
:mod:`websockets.http` module provides basic HTTP/1.1 support. It is merely
:adequate for WebSocket handshake messages.

These APIs cannot be imported from :mod:`websockets`. They must be imported
from :mod:`websockets.http`.

"""
import asyncio, re, sys
from typing import Any, Dict, Iterable, Iterator, List, Mapping, MutableMapping, Tuple, Union
from .version import version as websockets_version
__all__ = [
 'read_request',
 'read_response',
 'Headers',
 'MultipleValuesError',
 'USER_AGENT']
MAX_HEADERS = 256
MAX_LINE = 4096
USER_AGENT = f"Python/{sys.version[:3]} websockets/{websockets_version}"

def d(value: bytes) -> str:
    """
    Decode a bytestring for interpolating into an error message.

    """
    return value.decode(errors='backslashreplace')


_token_re = re.compile(b"[-!#$%&\\'*+.^_`|~0-9a-zA-Z]+")
_value_re = re.compile(b'[\\x09\\x20-\\x7e\\x80-\\xff]*')

async def read_request(stream: asyncio.StreamReader) -> Tuple[(str, 'Headers')]:
    """
    Read an HTTP/1.1 GET request and return ``(path, headers)``.

    ``path`` isn't URL-decoded or validated in any way.

    ``path`` and ``headers`` are expected to contain only ASCII characters.
    Other characters are represented with surrogate escapes.

    :func:`read_request` doesn't attempt to read the request body because
    WebSocket handshake requests don't have one. If the request contains a
    body, it may be read from ``stream`` after this coroutine returns.

    :param stream: input to read the request from
    :raises EOFError: if the connection is closed without a full HTTP request
    :raises SecurityError: if the request exceeds a security limit
    :raises ValueError: if the request isn't well formatted

    """
    try:
        request_line = await read_line(stream)
    except EOFError as exc:
        try:
            raise EOFError('connection closed while reading HTTP request line') from exc
        finally:
            exc = None
            del exc

    else:
        try:
            method, raw_path, version = request_line.split(b' ', 2)
        except ValueError:
            raise ValueError(f"invalid HTTP request line: {d(request_line)}") from None
        else:
            if method != b'GET':
                raise ValueError(f"unsupported HTTP method: {d(method)}")
            if version != b'HTTP/1.1':
                raise ValueError(f"unsupported HTTP version: {d(version)}")
            path = raw_path.decode('ascii', 'surrogateescape')
            headers = await read_headers(stream)
            return (
             path, headers)


async def read_response(stream: asyncio.StreamReader) -> Tuple[(int, str, 'Headers')]:
    """
    Read an HTTP/1.1 response and return ``(status_code, reason, headers)``.

    ``reason`` and ``headers`` are expected to contain only ASCII characters.
    Other characters are represented with surrogate escapes.

    :func:`read_request` doesn't attempt to read the response body because
    WebSocket handshake responses don't have one. If the response contains a
    body, it may be read from ``stream`` after this coroutine returns.

    :param stream: input to read the response from
    :raises EOFError: if the connection is closed without a full HTTP response
    :raises SecurityError: if the response exceeds a security limit
    :raises ValueError: if the response isn't well formatted

    """
    try:
        status_line = await read_line(stream)
    except EOFError as exc:
        try:
            raise EOFError('connection closed while reading HTTP status line') from exc
        finally:
            exc = None
            del exc

    else:
        try:
            version, raw_status_code, raw_reason = status_line.split(b' ', 2)
        except ValueError:
            raise ValueError(f"invalid HTTP status line: {d(status_line)}") from None
        else:
            if version != b'HTTP/1.1':
                raise ValueError(f"unsupported HTTP version: {d(version)}")
            try:
                status_code = int(raw_status_code)
            except ValueError:
                raise ValueError(f"invalid HTTP status code: {d(raw_status_code)}") from None
            else:
                if not 100 <= status_code < 1000:
                    raise ValueError(f"unsupported HTTP status code: {d(raw_status_code)}")
                if not _value_re.fullmatch(raw_reason):
                    raise ValueError(f"invalid HTTP reason phrase: {d(raw_reason)}")
                reason = raw_reason.decode()
                headers = await read_headers(stream)
                return (
                 status_code, reason, headers)


async def read_headers--- This code section failed: ---

 L. 176         0  LOAD_GLOBAL              Headers
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'headers'

 L. 177         6  LOAD_GLOBAL              range
                8  LOAD_GLOBAL              MAX_HEADERS
               10  LOAD_CONST               1
               12  BINARY_ADD       
               14  CALL_FUNCTION_1       1  ''
               16  GET_ITER         
               18  FOR_ITER            260  'to 260'
               20  STORE_FAST               '_'

 L. 178        22  SETUP_FINALLY        42  'to 42'

 L. 179        24  LOAD_GLOBAL              read_line
               26  LOAD_FAST                'stream'
               28  CALL_FUNCTION_1       1  ''
               30  GET_AWAITABLE    
               32  LOAD_CONST               None
               34  YIELD_FROM       
               36  STORE_FAST               'line'
               38  POP_BLOCK        
               40  JUMP_FORWARD         86  'to 86'
             42_0  COME_FROM_FINALLY    22  '22'

 L. 180        42  DUP_TOP          
               44  LOAD_GLOBAL              EOFError
               46  COMPARE_OP               exception-match
               48  POP_JUMP_IF_FALSE    84  'to 84'
               50  POP_TOP          
               52  STORE_FAST               'exc'
               54  POP_TOP          
               56  SETUP_FINALLY        72  'to 72'

 L. 181        58  LOAD_GLOBAL              EOFError
               60  LOAD_STR                 'connection closed while reading HTTP headers'
               62  CALL_FUNCTION_1       1  ''
               64  LOAD_FAST                'exc'
               66  RAISE_VARARGS_2       2  'exception instance with __cause__'
               68  POP_BLOCK        
               70  BEGIN_FINALLY    
             72_0  COME_FROM_FINALLY    56  '56'
               72  LOAD_CONST               None
               74  STORE_FAST               'exc'
               76  DELETE_FAST              'exc'
               78  END_FINALLY      
               80  POP_EXCEPT       
               82  JUMP_FORWARD         86  'to 86'
             84_0  COME_FROM            48  '48'
               84  END_FINALLY      
             86_0  COME_FROM            82  '82'
             86_1  COME_FROM            40  '40'

 L. 182        86  LOAD_FAST                'line'
               88  LOAD_CONST               b''
               90  COMPARE_OP               ==
               92  POP_JUMP_IF_FALSE   100  'to 100'

 L. 183        94  POP_TOP          
            96_98  JUMP_ABSOLUTE       272  'to 272'
            100_0  COME_FROM            92  '92'

 L. 185       100  SETUP_FINALLY       122  'to 122'

 L. 186       102  LOAD_FAST                'line'
              104  LOAD_METHOD              split
              106  LOAD_CONST               b':'
              108  LOAD_CONST               1
              110  CALL_METHOD_2         2  ''
              112  UNPACK_SEQUENCE_2     2 
              114  STORE_FAST               'raw_name'
              116  STORE_FAST               'raw_value'
              118  POP_BLOCK        
              120  JUMP_FORWARD        162  'to 162'
            122_0  COME_FROM_FINALLY   100  '100'

 L. 187       122  DUP_TOP          
              124  LOAD_GLOBAL              ValueError
              126  COMPARE_OP               exception-match
              128  POP_JUMP_IF_FALSE   160  'to 160'
              130  POP_TOP          
              132  POP_TOP          
              134  POP_TOP          

 L. 188       136  LOAD_GLOBAL              ValueError
              138  LOAD_STR                 'invalid HTTP header line: '
              140  LOAD_GLOBAL              d
              142  LOAD_FAST                'line'
              144  CALL_FUNCTION_1       1  ''
              146  FORMAT_VALUE          0  ''
              148  BUILD_STRING_2        2 
              150  CALL_FUNCTION_1       1  ''
              152  LOAD_CONST               None
              154  RAISE_VARARGS_2       2  'exception instance with __cause__'
              156  POP_EXCEPT       
              158  JUMP_FORWARD        162  'to 162'
            160_0  COME_FROM           128  '128'
              160  END_FINALLY      
            162_0  COME_FROM           158  '158'
            162_1  COME_FROM           120  '120'

 L. 189       162  LOAD_GLOBAL              _token_re
              164  LOAD_METHOD              fullmatch
              166  LOAD_FAST                'raw_name'
              168  CALL_METHOD_1         1  ''
              170  POP_JUMP_IF_TRUE    190  'to 190'

 L. 190       172  LOAD_GLOBAL              ValueError
              174  LOAD_STR                 'invalid HTTP header name: '
              176  LOAD_GLOBAL              d
              178  LOAD_FAST                'raw_name'
              180  CALL_FUNCTION_1       1  ''
              182  FORMAT_VALUE          0  ''
              184  BUILD_STRING_2        2 
              186  CALL_FUNCTION_1       1  ''
              188  RAISE_VARARGS_1       1  'exception instance'
            190_0  COME_FROM           170  '170'

 L. 191       190  LOAD_FAST                'raw_value'
              192  LOAD_METHOD              strip
              194  LOAD_CONST               b' \t'
              196  CALL_METHOD_1         1  ''
              198  STORE_FAST               'raw_value'

 L. 192       200  LOAD_GLOBAL              _value_re
              202  LOAD_METHOD              fullmatch
              204  LOAD_FAST                'raw_value'
              206  CALL_METHOD_1         1  ''
              208  POP_JUMP_IF_TRUE    228  'to 228'

 L. 193       210  LOAD_GLOBAL              ValueError
              212  LOAD_STR                 'invalid HTTP header value: '
              214  LOAD_GLOBAL              d
              216  LOAD_FAST                'raw_value'
              218  CALL_FUNCTION_1       1  ''
              220  FORMAT_VALUE          0  ''
              222  BUILD_STRING_2        2 
              224  CALL_FUNCTION_1       1  ''
              226  RAISE_VARARGS_1       1  'exception instance'
            228_0  COME_FROM           208  '208'

 L. 195       228  LOAD_FAST                'raw_name'
              230  LOAD_METHOD              decode
              232  LOAD_STR                 'ascii'
              234  CALL_METHOD_1         1  ''
              236  STORE_FAST               'name'

 L. 196       238  LOAD_FAST                'raw_value'
              240  LOAD_METHOD              decode
              242  LOAD_STR                 'ascii'
              244  LOAD_STR                 'surrogateescape'
              246  CALL_METHOD_2         2  ''
              248  STORE_FAST               'value'

 L. 197       250  LOAD_FAST                'value'
              252  LOAD_FAST                'headers'
              254  LOAD_FAST                'name'
              256  STORE_SUBSCR     
              258  JUMP_BACK            18  'to 18'

 L. 200       260  LOAD_GLOBAL              websockets
              262  LOAD_ATTR                exceptions
              264  LOAD_METHOD              SecurityError
              266  LOAD_STR                 'too many HTTP headers'
              268  CALL_METHOD_1         1  ''
              270  RAISE_VARARGS_1       1  'exception instance'

 L. 202       272  LOAD_FAST                'headers'
              274  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 96_98


async def read_line(stream: asyncio.StreamReader) -> bytes:
    """
    Read a single line from ``stream``.

    CRLF is stripped from the return value.

    """
    line = await stream.readline()
    if len(line) > MAX_LINE:
        raise websockets.exceptions.SecurityError('line too long')
    if not line.endswith(b'\r\n'):
        raise EOFError('line without CRLF')
    return line[:-2]


class MultipleValuesError(LookupError):
    __doc__ = '\n    Exception raised when :class:`Headers` has more than one value for a key.\n\n    '

    def __str__(self):
        if len(self.args) == 1:
            return repr(self.args[0])
        return super.__str__()


class Headers(MutableMapping[(str, str)]):
    __doc__ = "\n    Efficient data structure for manipulating HTTP headers.\n\n    A :class:`list` of ``(name, values)`` is inefficient for lookups.\n\n    A :class:`dict` doesn't suffice because header names are case-insensitive\n    and multiple occurrences of headers with the same name are possible.\n\n    :class:`Headers` stores HTTP headers in a hybrid data structure to provide\n    efficient insertions and lookups while preserving the original data.\n\n    In order to account for multiple values with minimal hassle,\n    :class:`Headers` follows this logic:\n\n    - When getting a header with ``headers[name]``:\n        - if there's no value, :exc:`KeyError` is raised;\n        - if there's exactly one value, it's returned;\n        - if there's more than one value, :exc:`MultipleValuesError` is raised.\n\n    - When setting a header with ``headers[name] = value``, the value is\n      appended to the list of values for that header.\n\n    - When deleting a header with ``del headers[name]``, all values for that\n      header are removed (this is slow).\n\n    Other methods for manipulating headers are consistent with this logic.\n\n    As long as no header occurs multiple times, :class:`Headers` behaves like\n    :class:`dict`, except keys are lower-cased to provide case-insensitivity.\n\n    Two methods support support manipulating multiple values explicitly:\n\n    - :meth:`get_all` returns a list of all values for a header;\n    - :meth:`raw_items` returns an iterator of ``(name, values)`` pairs.\n\n    "
    __slots__ = [
     '_dict', '_list']

    def __init__(self, *args: Any, **kwargs: str) -> None:
        self._dict = {}
        self._list = []
        (self.update)(*args, **kwargs)

    def __str__(self) -> str:
        return ''.join((f"{key}: {value}\r\n" for key, value in self._list)) + '\r\n'

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._list!r})"

    def copy(self) -> 'Headers':
        copy = self.__class__()
        copy._dict = self._dict.copy()
        copy._list = self._list.copy()
        return copy

    def __contains__(self, key: object) -> bool:
        return isinstance(key, str) and key.lower() in self._dict

    def __iter__(self) -> Iterator[str]:
        return iter(self._dict)

    def __len__(self) -> int:
        return len(self._dict)

    def __getitem__(self, key: str) -> str:
        value = self._dict[key.lower()]
        if len(value) == 1:
            return value[0]
        raise MultipleValuesError(key)

    def __setitem__(self, key: str, value: str) -> None:
        self._dict.setdefault(key.lower(), []).append(value)
        self._list.append((key, value))

    def __delitem__(self, key: str) -> None:
        key_lower = key.lower()
        self._dict.__delitem__(key_lower)
        self._list = [(
         k, v) for k, v in self._list if k.lower() != key_lower]

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Headers):
            return NotImplemented
        return self._list == other._list

    def clear(self) -> None:
        """
        Remove all headers.

        """
        self._dict = {}
        self._list = []

    def get_all(self, key: str) -> List[str]:
        """
        Return the (possibly empty) list of all values for a header.

        :param key: header name

        """
        return self._dict.get(key.lower(), [])

    def raw_items(self) -> Iterator[Tuple[(str, str)]]:
        """
        Return an iterator of all values as ``(name, value)`` pairs.

        """
        return iter(self._list)


HeadersLike = Union[(Headers, Mapping[(str, str)], Iterable[Tuple[(str, str)]])]
import websockets.exceptions