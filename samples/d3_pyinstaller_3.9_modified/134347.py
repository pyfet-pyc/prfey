# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: aiohttp\web_log.py
import datetime, functools, logging, os, re
from collections import namedtuple
from typing import Any, Callable, Dict, Iterable, List, Tuple
from .abc import AbstractAccessLogger
from .web_request import BaseRequest
from .web_response import StreamResponse
KeyMethod = namedtuple('KeyMethod', 'key method')

class AccessLogger(AbstractAccessLogger):
    __doc__ = 'Helper object to log access.\n\n    Usage:\n        log = logging.getLogger("spam")\n        log_format = "%a %{User-Agent}i"\n        access_logger = AccessLogger(log, log_format)\n        access_logger.log(request, response, time)\n\n    Format:\n        %%  The percent sign\n        %a  Remote IP-address (IP-address of proxy if using reverse proxy)\n        %t  Time when the request was started to process\n        %P  The process ID of the child that serviced the request\n        %r  First line of request\n        %s  Response status code\n        %b  Size of response in bytes, including HTTP headers\n        %T  Time taken to serve the request, in seconds\n        %Tf Time taken to serve the request, in seconds with floating fraction\n            in .06f format\n        %D  Time taken to serve the request, in microseconds\n        %{FOO}i  request.headers[\'FOO\']\n        %{FOO}o  response.headers[\'FOO\']\n        %{FOO}e  os.environ[\'FOO\']\n\n    '
    LOG_FORMAT_MAP = {'a':'remote_address', 
     't':'request_start_time', 
     'P':'process_id', 
     'r':'first_request_line', 
     's':'response_status', 
     'b':'response_size', 
     'T':'request_time', 
     'Tf':'request_time_frac', 
     'D':'request_time_micro', 
     'i':'request_header', 
     'o':'response_header'}
    LOG_FORMAT = '%a %t "%r" %s %b "%{Referer}i" "%{User-Agent}i"'
    FORMAT_RE = re.compile('%(\\{([A-Za-z0-9\\-_]+)\\}([ioe])|[atPrsbOD]|Tf?)')
    CLEANUP_RE = re.compile('(%[^s])')
    _FORMAT_CACHE = {}

    def __init__(self, logger, log_format=LOG_FORMAT):
        """Initialise the logger.

        logger is a logger object to be used for logging.
        log_format is a string with apache compatible log format description.

        """
        super().__init__(logger, log_format=log_format)
        _compiled_format = AccessLogger._FORMAT_CACHE.get(log_format)
        if not _compiled_format:
            _compiled_format = self.compile_format(log_format)
            AccessLogger._FORMAT_CACHE[log_format] = _compiled_format
        self._log_format, self._methods = _compiled_format

    def compile_format(self, log_format: str) -> Tuple[(str, List[KeyMethod])]:
        """Translate log_format into form usable by modulo formatting

        All known atoms will be replaced with %s
        Also methods for formatting of those atoms will be added to
        _methods in appropriate order

        For example we have log_format = "%a %t"
        This format will be translated to "%s %s"
        Also contents of _methods will be
        [self._format_a, self._format_t]
        These method will be called and results will be passed
        to translated string format.

        Each _format_* method receive 'args' which is list of arguments
        given to self.log

        Exceptions are _format_e, _format_i and _format_o methods which
        also receive key name (by functools.partial)

        """
        methods = list()
        for atom in self.FORMAT_RE.findall(log_format):
            if atom[1] == '':
                format_key1 = self.LOG_FORMAT_MAP[atom[0]]
                m = getattr(AccessLogger, '_format_%s' % atom[0])
                key_method = KeyMethod(format_key1, m)
            else:
                format_key2 = (
                 self.LOG_FORMAT_MAP[atom[2]], atom[1])
                m = getattr(AccessLogger, '_format_%s' % atom[2])
                key_method = KeyMethod(format_key2, functools.partial(m, atom[1]))
            methods.append(key_method)
        else:
            log_format = self.FORMAT_RE.sub('%s', log_format)
            log_format = self.CLEANUP_RE.sub('%\\1', log_format)
            return (
             log_format, methods)

    @staticmethod
    def _format_i--- This code section failed: ---

 L. 123         0  LOAD_FAST                'request'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 124         8  LOAD_STR                 '(no headers)'
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L. 127        12  LOAD_FAST                'request'
               14  LOAD_ATTR                headers
               16  LOAD_METHOD              get
               18  LOAD_FAST                'key'
               20  LOAD_STR                 '-'
               22  CALL_METHOD_2         2  ''
               24  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @staticmethod
    def _format_o(key: str, request: BaseRequest, response: StreamResponse, time: float) -> str:
        return response.headers.get(key, '-')

    @staticmethod
    def _format_a--- This code section failed: ---

 L. 138         0  LOAD_FAST                'request'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 139         8  LOAD_STR                 '-'
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L. 140        12  LOAD_FAST                'request'
               14  LOAD_ATTR                remote
               16  STORE_FAST               'ip'

 L. 141        18  LOAD_FAST                'ip'
               20  LOAD_CONST               None
               22  <117>                 1  ''
               24  POP_JUMP_IF_FALSE    30  'to 30'
               26  LOAD_FAST                'ip'
               28  RETURN_VALUE     
             30_0  COME_FROM            24  '24'
               30  LOAD_STR                 '-'
               32  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @staticmethod
    def _format_t(request: BaseRequest, response: StreamResponse, time: float) -> str:
        now = datetime.datetime.utcnow()
        start_time = now - datetime.timedelta(seconds=time)
        return start_time.strftime('[%d/%b/%Y:%H:%M:%S +0000]')

    @staticmethod
    def _format_P(request: BaseRequest, response: StreamResponse, time: float) -> str:
        return '<%s>' % os.getpid()

    @staticmethod
    def _format_r--- This code section failed: ---

 L. 155         0  LOAD_FAST                'request'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 156         8  LOAD_STR                 '-'
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L. 157        12  LOAD_STR                 '{} {} HTTP/{}.{}'
               14  LOAD_METHOD              format

 L. 158        16  LOAD_FAST                'request'
               18  LOAD_ATTR                method

 L. 159        20  LOAD_FAST                'request'
               22  LOAD_ATTR                path_qs

 L. 160        24  LOAD_FAST                'request'
               26  LOAD_ATTR                version
               28  LOAD_ATTR                major

 L. 161        30  LOAD_FAST                'request'
               32  LOAD_ATTR                version
               34  LOAD_ATTR                minor

 L. 157        36  CALL_METHOD_4         4  ''
               38  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @staticmethod
    def _format_s(request: BaseRequest, response: StreamResponse, time: float) -> int:
        return response.status

    @staticmethod
    def _format_b(request: BaseRequest, response: StreamResponse, time: float) -> int:
        return response.body_length

    @staticmethod
    def _format_T(request: BaseRequest, response: StreamResponse, time: float) -> str:
        return str(round(time))

    @staticmethod
    def _format_Tf(request: BaseRequest, response: StreamResponse, time: float) -> str:
        return '%06f' % time

    @staticmethod
    def _format_D(request: BaseRequest, response: StreamResponse, time: float) -> str:
        return str(round(time * 1000000))

    def _format_line(self, request: BaseRequest, response: StreamResponse, time: float) -> Iterable[Tuple[(str, Callable[([BaseRequest, StreamResponse, float], str)])]]:
        return [(key, method(request, response, time)) for key, method in self._methods]

    def log--- This code section failed: ---

 L. 190         0  SETUP_FINALLY       138  'to 138'

 L. 191         2  LOAD_FAST                'self'
                4  LOAD_METHOD              _format_line
                6  LOAD_FAST                'request'
                8  LOAD_FAST                'response'
               10  LOAD_FAST                'time'
               12  CALL_METHOD_3         3  ''
               14  STORE_FAST               'fmt_info'

 L. 193        16  LOAD_GLOBAL              list
               18  CALL_FUNCTION_0       0  ''
               20  STORE_FAST               'values'

 L. 194        22  LOAD_GLOBAL              dict
               24  CALL_FUNCTION_0       0  ''
               26  STORE_FAST               'extra'

 L. 195        28  LOAD_FAST                'fmt_info'
               30  GET_ITER         
             32_0  COME_FROM           106  '106'
             32_1  COME_FROM            68  '68'
               32  FOR_ITER            108  'to 108'
               34  UNPACK_SEQUENCE_2     2 
               36  STORE_FAST               'key'
               38  STORE_FAST               'value'

 L. 196        40  LOAD_FAST                'values'
               42  LOAD_METHOD              append
               44  LOAD_FAST                'value'
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          

 L. 198        50  LOAD_FAST                'key'
               52  LOAD_ATTR                __class__
               54  LOAD_GLOBAL              str
               56  <117>                 0  ''
               58  POP_JUMP_IF_FALSE    70  'to 70'

 L. 199        60  LOAD_FAST                'value'
               62  LOAD_FAST                'extra'
               64  LOAD_FAST                'key'
               66  STORE_SUBSCR     
               68  JUMP_BACK            32  'to 32'
             70_0  COME_FROM            58  '58'

 L. 201        70  LOAD_FAST                'key'
               72  UNPACK_SEQUENCE_2     2 
               74  STORE_FAST               'k1'
               76  STORE_FAST               'k2'

 L. 202        78  LOAD_FAST                'extra'
               80  LOAD_METHOD              get
               82  LOAD_FAST                'k1'
               84  BUILD_MAP_0           0 
               86  CALL_METHOD_2         2  ''
               88  STORE_FAST               'dct'

 L. 203        90  LOAD_FAST                'value'
               92  LOAD_FAST                'dct'
               94  LOAD_FAST                'k2'
               96  STORE_SUBSCR     

 L. 204        98  LOAD_FAST                'dct'
              100  LOAD_FAST                'extra'
              102  LOAD_FAST                'k1'
              104  STORE_SUBSCR     
              106  JUMP_BACK            32  'to 32'
            108_0  COME_FROM            32  '32'

 L. 206       108  LOAD_FAST                'self'
              110  LOAD_ATTR                logger
              112  LOAD_ATTR                info
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                _log_format
              118  LOAD_GLOBAL              tuple
              120  LOAD_FAST                'values'
              122  CALL_FUNCTION_1       1  ''
              124  BINARY_MODULO    
              126  LOAD_FAST                'extra'
              128  LOAD_CONST               ('extra',)
              130  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              132  POP_TOP          
              134  POP_BLOCK        
              136  JUMP_FORWARD        168  'to 168'
            138_0  COME_FROM_FINALLY     0  '0'

 L. 207       138  DUP_TOP          
              140  LOAD_GLOBAL              Exception
              142  <121>               166  ''
              144  POP_TOP          
              146  POP_TOP          
              148  POP_TOP          

 L. 208       150  LOAD_FAST                'self'
              152  LOAD_ATTR                logger
              154  LOAD_METHOD              exception
              156  LOAD_STR                 'Error in logging'
              158  CALL_METHOD_1         1  ''
              160  POP_TOP          
              162  POP_EXCEPT       
              164  JUMP_FORWARD        168  'to 168'
              166  <48>             
            168_0  COME_FROM           164  '164'
            168_1  COME_FROM           136  '136'

Parse error at or near `<117>' instruction at offset 56