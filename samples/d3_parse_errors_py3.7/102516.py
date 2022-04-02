# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: urllib3\response.py
from __future__ import absolute_import
import io, logging, zlib
from contextlib import contextmanager
from socket import error as SocketError
from socket import timeout as SocketTimeout
try:
    import brotli
except ImportError:
    brotli = None

from ._collections import HTTPHeaderDict
from .connection import BaseSSLError, HTTPException
from .exceptions import BodyNotHttplibCompatible, DecodeError, HTTPError, IncompleteRead, InvalidChunkLength, InvalidHeader, ProtocolError, ReadTimeoutError, ResponseNotChunked, SSLError
from .packages import six
from util.response import is_fp_closed, is_response_to_head
log = logging.getLogger(__name__)

class DeflateDecoder(object):

    def __init__(self):
        self._first_try = True
        self._data = ''
        self._obj = zlib.decompressobj()

    def __getattr__(self, name):
        return getattr(self._obj, name)

    def decompress(self, data):
        if not data:
            return data
        if not self._first_try:
            return self._obj.decompress(data)
        self._data += data
        try:
            decompressed = self._obj.decompress(data)
            if decompressed:
                self._first_try = False
                self._data = None
            return decompressed
        except zlib.error:
            self._first_try = False
            self._obj = zlib.decompressobj(-zlib.MAX_WBITS)
            try:
                return self.decompress(self._data)
            finally:
                self._data = None


class GzipDecoderState(object):
    FIRST_MEMBER = 0
    OTHER_MEMBERS = 1
    SWALLOW_DATA = 2


class GzipDecoder(object):

    def __init__(self):
        self._obj = zlib.decompressobj(16 + zlib.MAX_WBITS)
        self._state = GzipDecoderState.FIRST_MEMBER

    def __getattr__(self, name):
        return getattr(self._obj, name)

    def decompress(self, data):
        ret = bytearray()
        if not (self._state == GzipDecoderState.SWALLOW_DATA or data):
            return bytes(ret)
        while True:
            try:
                ret += self._obj.decompress(data)
            except zlib.error:
                previous_state = self._state
                self._state = GzipDecoderState.SWALLOW_DATA
                if previous_state == GzipDecoderState.OTHER_MEMBERS:
                    return bytes(ret)
                raise

            data = self._obj.unused_data
            if not data:
                return bytes(ret)
            else:
                self._state = GzipDecoderState.OTHER_MEMBERS
                self._obj = zlib.decompressobj(16 + zlib.MAX_WBITS)


if brotli is not None:

    class BrotliDecoder(object):

        def __init__(self):
            self._obj = brotli.Decompressor()
            if hasattr(self._obj, 'decompress'):
                self.decompress = self._obj.decompress
            else:
                self.decompress = self._obj.process

        def flush(self):
            if hasattr(self._obj, 'flush'):
                return self._obj.flush()
            return ''


class MultiDecoder(object):
    __doc__ = '\n    From RFC7231:\n        If one or more encodings have been applied to a representation, the\n        sender that applied the encodings MUST generate a Content-Encoding\n        header field that lists the content codings in the order in which\n        they were applied.\n    '

    def __init__(self, modes):
        self._decoders = [_get_decoder(m.strip()) for m in modes.split(',')]

    def flush(self):
        return self._decoders[0].flush()

    def decompress(self, data):
        for d in reversed(self._decoders):
            data = d.decompress(data)

        return data


def _get_decoder(mode):
    if ',' in mode:
        return MultiDecoder(mode)
    if mode == 'gzip':
        return GzipDecoder()
    if brotli is not None:
        if mode == 'br':
            return BrotliDecoder()
    return DeflateDecoder()


class HTTPResponse(io.IOBase):
    __doc__ = "\n    HTTP Response container.\n\n    Backwards-compatible with :class:`http.client.HTTPResponse` but the response ``body`` is\n    loaded and decoded on-demand when the ``data`` property is accessed.  This\n    class is also compatible with the Python standard library's :mod:`io`\n    module, and can hence be treated as a readable object in the context of that\n    framework.\n\n    Extra parameters for behaviour not present in :class:`http.client.HTTPResponse`:\n\n    :param preload_content:\n        If True, the response's body will be preloaded during construction.\n\n    :param decode_content:\n        If True, will attempt to decode the body based on the\n        'content-encoding' header.\n\n    :param original_response:\n        When this HTTPResponse wrapper is generated from an :class:`http.client.HTTPResponse`\n        object, it's convenient to include the original for debug purposes. It's\n        otherwise unused.\n\n    :param retries:\n        The retries contains the last :class:`~urllib3.util.retry.Retry` that\n        was used during the request.\n\n    :param enforce_content_length:\n        Enforce content length checking. Body returned by server must match\n        value of Content-Length header, if present. Otherwise, raise error.\n    "
    CONTENT_DECODERS = [
     'gzip', 'deflate']
    if brotli is not None:
        CONTENT_DECODERS += ['br']
    REDIRECT_STATUSES = [
     301, 302, 303, 307, 308]

    def __init__(self, body='', headers=None, status=0, version=0, reason=None, strict=0, preload_content=True, decode_content=True, original_response=None, pool=None, connection=None, msg=None, retries=None, enforce_content_length=False, request_method=None, request_url=None, auto_close=True):
        if isinstance(headers, HTTPHeaderDict):
            self.headers = headers
        else:
            self.headers = HTTPHeaderDict(headers)
        self.status = status
        self.version = version
        self.reason = reason
        self.strict = strict
        self.decode_content = decode_content
        self.retries = retries
        self.enforce_content_length = enforce_content_length
        self.auto_close = auto_close
        self._decoder = None
        self._body = None
        self._fp = None
        self._original_response = original_response
        self._fp_bytes_read = 0
        self.msg = msg
        self._request_url = request_url
        if body:
            if isinstance(body, (six.string_types, bytes)):
                self._body = body
        self._pool = pool
        self._connection = connection
        if hasattr(body, 'read'):
            self._fp = body
        self.chunked = False
        self.chunk_left = None
        tr_enc = self.headers.get('transfer-encoding', '').lower()
        encodings = (enc.strip() for enc in tr_enc.split(','))
        if 'chunked' in encodings:
            self.chunked = True
        self.length_remaining = self._init_length(request_method)
        if preload_content:
            if not self._body:
                self._body = self.read(decode_content=decode_content)

    def get_redirect_location(self):
        """
        Should we redirect and where to?

        :returns: Truthy redirect location string if we got a redirect status
            code and valid location. ``None`` if redirect status and no
            location. ``False`` if not a redirect status code.
        """
        if self.status in self.REDIRECT_STATUSES:
            return self.headers.get('location')
        return False

    def release_conn(self):
        if not (self._pool and self._connection):
            return
        self._pool._put_conn(self._connection)
        self._connection = None

    def drain_conn(self):
        """
        Read and discard any remaining HTTP response data in the response connection.

        Unread data in the HTTPResponse connection blocks the connection from being released back to the pool.
        """
        try:
            self.read()
        except (HTTPError, SocketError, BaseSSLError, HTTPException):
            pass

    @property
    def data(self):
        if self._body:
            return self._body
        if self._fp:
            return self.read(cache_content=True)

    @property
    def connection(self):
        return self._connection

    def isclosed(self):
        return is_fp_closed(self._fp)

    def tell(self):
        """
        Obtain the number of bytes pulled over the wire so far. May differ from
        the amount of content returned by :meth:``urllib3.response.HTTPResponse.read``
        if bytes are encoded on the wire (e.g, compressed).
        """
        return self._fp_bytes_read

    def _init_length--- This code section failed: ---

 L. 321         0  LOAD_FAST                'self'
                2  LOAD_ATTR                headers
                4  LOAD_METHOD              get
                6  LOAD_STR                 'content-length'
                8  CALL_METHOD_1         1  '1 positional argument'
               10  STORE_FAST               'length'

 L. 323        12  LOAD_FAST                'length'
               14  LOAD_CONST               None
               16  COMPARE_OP               is-not
               18  POP_JUMP_IF_FALSE   138  'to 138'

 L. 324        20  LOAD_FAST                'self'
               22  LOAD_ATTR                chunked
               24  POP_JUMP_IF_FALSE    40  'to 40'

 L. 328        26  LOAD_GLOBAL              log
               28  LOAD_METHOD              warning

 L. 329        30  LOAD_STR                 'Received response with both Content-Length and Transfer-Encoding set. This is expressly forbidden by RFC 7230 sec 3.3.2. Ignoring Content-Length and attempting to process response as Transfer-Encoding: chunked.'
               32  CALL_METHOD_1         1  '1 positional argument'
               34  POP_TOP          

 L. 335        36  LOAD_CONST               None
               38  RETURN_VALUE     
             40_0  COME_FROM            24  '24'

 L. 337        40  SETUP_EXCEPT        102  'to 102'

 L. 343        42  LOAD_GLOBAL              set
               44  LOAD_LISTCOMP            '<code_object <listcomp>>'
               46  LOAD_STR                 'HTTPResponse._init_length.<locals>.<listcomp>'
               48  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               50  LOAD_FAST                'length'
               52  LOAD_METHOD              split
               54  LOAD_STR                 ','
               56  CALL_METHOD_1         1  '1 positional argument'
               58  GET_ITER         
               60  CALL_FUNCTION_1       1  '1 positional argument'
               62  CALL_FUNCTION_1       1  '1 positional argument'
               64  STORE_FAST               'lengths'

 L. 344        66  LOAD_GLOBAL              len
               68  LOAD_FAST                'lengths'
               70  CALL_FUNCTION_1       1  '1 positional argument'
               72  LOAD_CONST               1
               74  COMPARE_OP               >
               76  POP_JUMP_IF_FALSE    90  'to 90'

 L. 345        78  LOAD_GLOBAL              InvalidHeader

 L. 346        80  LOAD_STR                 'Content-Length contained multiple unmatching values (%s)'

 L. 347        82  LOAD_FAST                'length'
               84  BINARY_MODULO    
               86  CALL_FUNCTION_1       1  '1 positional argument'
               88  RAISE_VARARGS_1       1  'exception instance'
             90_0  COME_FROM            76  '76'

 L. 349        90  LOAD_FAST                'lengths'
               92  LOAD_METHOD              pop
               94  CALL_METHOD_0         0  '0 positional arguments'
               96  STORE_FAST               'length'
               98  POP_BLOCK        
              100  JUMP_FORWARD        126  'to 126'
            102_0  COME_FROM_EXCEPT     40  '40'

 L. 350       102  DUP_TOP          
              104  LOAD_GLOBAL              ValueError
              106  COMPARE_OP               exception-match
              108  POP_JUMP_IF_FALSE   124  'to 124'
              110  POP_TOP          
              112  POP_TOP          
              114  POP_TOP          

 L. 351       116  LOAD_CONST               None
              118  STORE_FAST               'length'
              120  POP_EXCEPT       
              122  JUMP_FORWARD        138  'to 138'
            124_0  COME_FROM           108  '108'
              124  END_FINALLY      
            126_0  COME_FROM           100  '100'

 L. 353       126  LOAD_FAST                'length'
              128  LOAD_CONST               0
              130  COMPARE_OP               <
              132  POP_JUMP_IF_FALSE   138  'to 138'

 L. 354       134  LOAD_CONST               None
              136  STORE_FAST               'length'
            138_0  COME_FROM           132  '132'
            138_1  COME_FROM           122  '122'
            138_2  COME_FROM            18  '18'

 L. 358       138  SETUP_EXCEPT        154  'to 154'

 L. 359       140  LOAD_GLOBAL              int
              142  LOAD_FAST                'self'
              144  LOAD_ATTR                status
              146  CALL_FUNCTION_1       1  '1 positional argument'
              148  STORE_FAST               'status'
              150  POP_BLOCK        
              152  JUMP_FORWARD        178  'to 178'
            154_0  COME_FROM_EXCEPT    138  '138'

 L. 360       154  DUP_TOP          
              156  LOAD_GLOBAL              ValueError
              158  COMPARE_OP               exception-match
              160  POP_JUMP_IF_FALSE   176  'to 176'
              162  POP_TOP          
              164  POP_TOP          
              166  POP_TOP          

 L. 361       168  LOAD_CONST               0
              170  STORE_FAST               'status'
              172  POP_EXCEPT       
              174  JUMP_FORWARD        178  'to 178'
            176_0  COME_FROM           160  '160'
              176  END_FINALLY      
            178_0  COME_FROM           174  '174'
            178_1  COME_FROM           152  '152'

 L. 364       178  LOAD_FAST                'status'
              180  LOAD_CONST               (204, 304)
              182  COMPARE_OP               in
              184  POP_JUMP_IF_TRUE    216  'to 216'
              186  LOAD_CONST               100
              188  LOAD_FAST                'status'
              190  DUP_TOP          
              192  ROT_THREE        
              194  COMPARE_OP               <=
              196  POP_JUMP_IF_FALSE   206  'to 206'
              198  LOAD_CONST               200
              200  COMPARE_OP               <
              202  POP_JUMP_IF_TRUE    216  'to 216'
              204  JUMP_FORWARD        208  'to 208'
            206_0  COME_FROM           196  '196'
              206  POP_TOP          
            208_0  COME_FROM           204  '204'
              208  LOAD_FAST                'request_method'
              210  LOAD_STR                 'HEAD'
              212  COMPARE_OP               ==
              214  POP_JUMP_IF_FALSE   220  'to 220'
            216_0  COME_FROM           202  '202'
            216_1  COME_FROM           184  '184'

 L. 365       216  LOAD_CONST               0
              218  STORE_FAST               'length'
            220_0  COME_FROM           214  '214'

 L. 367       220  LOAD_FAST                'length'
              222  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 216

    def _init_decoder(self):
        """
        Set-up the _decoder attribute if necessary.
        """
        content_encoding = self.headers.get('content-encoding', '').lower()
        if self._decoder is None:
            if content_encoding in self.CONTENT_DECODERS:
                self._decoder = _get_decoder(content_encoding)
            elif ',' in content_encoding:
                encodings = [e.strip() for e in content_encoding.split(',') if e.strip() in self.CONTENT_DECODERS]
                if len(encodings):
                    self._decoder = _get_decoder(content_encoding)

    DECODER_ERROR_CLASSES = (
     IOError, zlib.error)
    if brotli is not None:
        DECODER_ERROR_CLASSES += (brotli.error,)

    def _decode(self, data, decode_content, flush_decoder):
        """
        Decode the data passed in and potentially flush the decoder.
        """
        if not decode_content:
            return data
        try:
            if self._decoder:
                data = self._decoder.decompress(data)
        except self.DECODER_ERROR_CLASSES as e:
            try:
                content_encoding = self.headers.get('content-encoding', '').lower()
                raise DecodeError('Received response with content-encoding: %s, but failed to decode it.' % content_encoding, e)
            finally:
                e = None
                del e

        if flush_decoder:
            data += self._flush_decoder()
        return data

    def _flush_decoder(self):
        """
        Flushes the decoder. Should only be called if the decoder is actually
        being used.
        """
        if self._decoder:
            buf = self._decoder.decompress('')
            return buf + self._decoder.flush()
        return ''

    @contextmanager
    def _error_catcher(self):
        """
        Catch low-level python exceptions, instead re-raising urllib3
        variants, so that low-level exceptions are not leaked in the
        high-level api.

        On exit, release the connection back to the pool.
        """
        clean_exit = False
        try:
            try:
                yield
            except SocketTimeout:
                raise ReadTimeoutError(self._pool, None, 'Read timed out.')
            except BaseSSLError as e:
                try:
                    if 'read operation timed out' not in str(e):
                        raise SSLError(e)
                    raise ReadTimeoutError(self._pool, None, 'Read timed out.')
                finally:
                    e = None
                    del e

            except (HTTPException, SocketError) as e:
                try:
                    raise ProtocolError('Connection broken: %r' % e, e)
                finally:
                    e = None
                    del e

            clean_exit = True
        finally:
            if not clean_exit:
                if self._original_response:
                    self._original_response.close()
                if self._connection:
                    self._connection.close()
            if self._original_response:
                if self._original_response.isclosed():
                    self.release_conn()

    def read(self, amt=None, decode_content=None, cache_content=False):
        """
        Similar to :meth:`http.client.HTTPResponse.read`, but with two additional
        parameters: ``decode_content`` and ``cache_content``.

        :param amt:
            How much of the content to read. If specified, caching is skipped
            because it doesn't make sense to cache partial content as the full
            response.

        :param decode_content:
            If True, will attempt to decode the body based on the
            'content-encoding' header.

        :param cache_content:
            If True, will save the returned data such that the same result is
            returned despite of the state of the underlying file object. This
            is useful if you want the ``.data`` property to continue working
            after having ``.read()`` the file object. (Overridden if ``amt`` is
            set.)
        """
        self._init_decoder()
        if decode_content is None:
            decode_content = self.decode_content
        if self._fp is None:
            return
        flush_decoder = False
        fp_closed = getattr(self._fp, 'closed', False)
        with self._error_catcher():
            if amt is None:
                data = self._fp.read() if (not fp_closed) else ''
                flush_decoder = True
            else:
                cache_content = False
                data = self._fp.read(amt) if (not fp_closed) else ''
                if amt != 0:
                    if not data:
                        self._fp.close()
                        flush_decoder = True
                        if self.enforce_content_length:
                            if self.length_remaining not in (0, None):
                                raise IncompleteRead(self._fp_bytes_read, self.length_remaining)
        if data:
            self._fp_bytes_read += len(data)
            if self.length_remaining is not None:
                self.length_remaining -= len(data)
            data = self._decode(data, decode_content, flush_decoder)
            if cache_content:
                self._body = data
        return data

    def stream(self, amt=65536, decode_content=None):
        """
        A generator wrapper for the read() method. A call will block until
        ``amt`` bytes have been read from the connection or until the
        connection is closed.

        :param amt:
            How much of the content to read. The generator will return up to
            much data per iteration, but may return less. This is particularly
            likely when using compressed data. However, the empty string will
            never be returned.

        :param decode_content:
            If True, will attempt to decode the body based on the
            'content-encoding' header.
        """
        if self.chunked and self.supports_chunked_reads():
            for line in self.read_chunked(amt, decode_content=decode_content):
                yield line

        else:
            while not is_fp_closed(self._fp):
                data = self.read(amt=amt, decode_content=decode_content)
                if data:
                    yield data

    @classmethod
    def from_httplib(ResponseCls, r, **response_kw):
        """
        Given an :class:`http.client.HTTPResponse` instance ``r``, return a
        corresponding :class:`urllib3.response.HTTPResponse` object.

        Remaining parameters are passed to the HTTPResponse constructor, along
        with ``original_response=r``.
        """
        headers = r.msg
        if not isinstance(headers, HTTPHeaderDict):
            if six.PY2:
                headers = HTTPHeaderDict.from_httplib(headers)
            else:
                headers = HTTPHeaderDict(headers.items())
        strict = getattr(r, 'strict', 0)
        resp = ResponseCls(body=r, 
         headers=headers, 
         status=r.status, 
         version=r.version, 
         reason=r.reason, 
         strict=strict, 
         original_response=r, **response_kw)
        return resp

    def getheaders(self):
        return self.headers

    def getheader(self, name, default=None):
        return self.headers.get(name, default)

    def info(self):
        return self.headers

    def close(self):
        if not self.closed:
            self._fp.close()
        if self._connection:
            self._connection.close()
        if not self.auto_close:
            io.IOBase.close(self)

    @property
    def closed(self):
        if not self.auto_close:
            return io.IOBase.closed.__get__(self)
        if self._fp is None:
            return True
        if hasattr(self._fp, 'isclosed'):
            return self._fp.isclosed()
        if hasattr(self._fp, 'closed'):
            return self._fp.closed
        return True

    def fileno(self):
        if self._fp is None:
            raise IOError('HTTPResponse has no file to get a fileno from')
        else:
            if hasattr(self._fp, 'fileno'):
                return self._fp.fileno()
            raise IOError('The file-like object this HTTPResponse is wrapped around has no file descriptor')

    def flush(self):
        if self._fp is not None:
            if hasattr(self._fp, 'flush'):
                if not getattr(self._fp, 'closed', False):
                    return self._fp.flush()

    def readable(self):
        return True

    def readinto(self, b):
        temp = self.read(len(b))
        if len(temp) == 0:
            return 0
        b[:len(temp)] = temp
        return len(temp)

    def supports_chunked_reads(self):
        """
        Checks if the underlying file-like object looks like a
        :class:`http.client.HTTPResponse` object. We do this by testing for
        the fp attribute. If it is present we assume it returns raw chunks as
        processed by read_chunked().
        """
        return hasattr(self._fp, 'fp')

    def _update_chunk_length(self):
        if self.chunk_left is not None:
            return
        line = self._fp.fp.readline()
        line = line.split(';', 1)[0]
        try:
            self.chunk_left = int(line, 16)
        except ValueError:
            self.close()
            raise InvalidChunkLength(self, line)

    def _handle_chunk(self, amt):
        returned_chunk = None
        if amt is None:
            chunk = self._fp._safe_read(self.chunk_left)
            returned_chunk = chunk
            self._fp._safe_read(2)
            self.chunk_left = None
        elif amt < self.chunk_left:
            value = self._fp._safe_read(amt)
            self.chunk_left = self.chunk_left - amt
            returned_chunk = value
        elif amt == self.chunk_left:
            value = self._fp._safe_read(amt)
            self._fp._safe_read(2)
            self.chunk_left = None
            returned_chunk = value
        else:
            returned_chunk = self._fp._safe_read(self.chunk_left)
            self._fp._safe_read(2)
            self.chunk_left = None
        return returned_chunk

    def read_chunked(self, amt=None, decode_content=None):
        """
        Similar to :meth:`HTTPResponse.read`, but with an additional
        parameter: ``decode_content``.

        :param amt:
            How much of the content to read. If specified, caching is skipped
            because it doesn't make sense to cache partial content as the full
            response.

        :param decode_content:
            If True, will attempt to decode the body based on the
            'content-encoding' header.
        """
        self._init_decoder()
        if not self.chunked:
            raise ResponseNotChunked("Response is not chunked. Header 'transfer-encoding: chunked' is missing.")
        if not self.supports_chunked_reads():
            raise BodyNotHttplibCompatible('Body should be http.client.HTTPResponse like. It should have have an fp attribute which returns raw chunks.')
        with self._error_catcher():
            if self._original_response:
                if is_response_to_head(self._original_response):
                    self._original_response.close()
                    return
            if self._fp.fp is None:
                return
            while 1:
                self._update_chunk_length()
                if self.chunk_left == 0:
                    break
                else:
                    chunk = self._handle_chunk(amt)
                    decoded = self._decode(chunk,
                      decode_content=decode_content, flush_decoder=False)
                if decoded:
                    yield decoded

            if decode_content:
                decoded = self._flush_decoder()
                if decoded:
                    yield decoded
            while 1:
                line = self._fp.fp.readline()
                if not line:
                    break
                if line == '\r\n':
                    break

            if self._original_response:
                self._original_response.close()

    def geturl(self):
        """
        Returns the URL that was the source of this response.
        If the request that generated this response redirected, this method
        will return the final redirect location.
        """
        if self.retries is not None:
            if len(self.retries.history):
                return self.retries.history[(-1)].redirect_location
        return self._request_url

    def __iter__(self):
        buffer = []
        for chunk in self.stream(decode_content=True):
            if '\n' in chunk:
                chunk = chunk.split('\n')
                yield ''.join(buffer) + chunk[0] + '\n'
                for x in chunk[1:-1]:
                    yield x + '\n'

                if chunk[(-1)]:
                    buffer = [
                     chunk[(-1)]]
                else:
                    buffer = []
            else:
                buffer.append(chunk)

        if buffer:
            yield ''.join(buffer)