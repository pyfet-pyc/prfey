# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: urllib3\util\request.py
from __future__ import absolute_import
from base64 import b64encode
from packages.six import b, integer_types
from ..exceptions import UnrewindableBodyError
ACCEPT_ENCODING = 'gzip,deflate'
_FAILEDTELL = object()

def make_headers(keep_alive=None, accept_encoding=None, user_agent=None, basic_auth=None, proxy_basic_auth=None, disable_cache=None):
    """
    Shortcuts for generating request headers.

    :param keep_alive:
        If ``True``, adds 'connection: keep-alive' header.

    :param accept_encoding:
        Can be a boolean, list, or string.
        ``True`` translates to 'gzip,deflate'.
        List will get joined by comma.
        String will be used as provided.

    :param user_agent:
        String representing the user-agent you want, such as
        "python-urllib3/0.6"

    :param basic_auth:
        Colon-separated username:password string for 'authorization: basic ...'
        auth header.

    :param proxy_basic_auth:
        Colon-separated username:password string for 'proxy-authorization: basic ...'
        auth header.

    :param disable_cache:
        If ``True``, adds 'cache-control: no-cache' header.

    Example::

        >>> make_headers(keep_alive=True, user_agent="Batman/1.0")
        {'connection': 'keep-alive', 'user-agent': 'Batman/1.0'}
        >>> make_headers(accept_encoding=True)
        {'accept-encoding': 'gzip,deflate'}
    """
    headers = {}
    if accept_encoding:
        if isinstance(accept_encoding, str):
            pass
        elif isinstance(accept_encoding, list):
            accept_encoding = ','.join(accept_encoding)
        else:
            accept_encoding = ACCEPT_ENCODING
        headers['accept-encoding'] = accept_encoding
    if user_agent:
        headers['user-agent'] = user_agent
    if keep_alive:
        headers['connection'] = 'keep-alive'
    if basic_auth:
        headers['authorization'] = 'Basic ' + b64encode(b(basic_auth)).decode('utf-8')
    if proxy_basic_auth:
        headers['proxy-authorization'] = 'Basic ' + b64encode(b(proxy_basic_auth)).decode('utf-8')
    if disable_cache:
        headers['cache-control'] = 'no-cache'
    return headers


def set_file_position--- This code section failed: ---

 L.  82         0  LOAD_FAST                'pos'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    20  'to 20'

 L.  83         8  LOAD_GLOBAL              rewind_body
               10  LOAD_FAST                'body'
               12  LOAD_FAST                'pos'
               14  CALL_FUNCTION_2       2  ''
               16  POP_TOP          
               18  JUMP_FORWARD         76  'to 76'
             20_0  COME_FROM             6  '6'

 L.  84        20  LOAD_GLOBAL              getattr
               22  LOAD_FAST                'body'
               24  LOAD_STR                 'tell'
               26  LOAD_CONST               None
               28  CALL_FUNCTION_3       3  ''
               30  LOAD_CONST               None
               32  <117>                 1  ''
               34  POP_JUMP_IF_FALSE    76  'to 76'

 L.  85        36  SETUP_FINALLY        50  'to 50'

 L.  86        38  LOAD_FAST                'body'
               40  LOAD_METHOD              tell
               42  CALL_METHOD_0         0  ''
               44  STORE_FAST               'pos'
               46  POP_BLOCK        
               48  JUMP_FORWARD         76  'to 76'
             50_0  COME_FROM_FINALLY    36  '36'

 L.  87        50  DUP_TOP          
               52  LOAD_GLOBAL              IOError
               54  LOAD_GLOBAL              OSError
               56  BUILD_TUPLE_2         2 
               58  <121>                74  ''
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L.  90        66  LOAD_GLOBAL              _FAILEDTELL
               68  STORE_FAST               'pos'
               70  POP_EXCEPT       
               72  JUMP_FORWARD         76  'to 76'
               74  <48>             
             76_0  COME_FROM            72  '72'
             76_1  COME_FROM            48  '48'
             76_2  COME_FROM            34  '34'
             76_3  COME_FROM            18  '18'

 L.  92        76  LOAD_FAST                'pos'
               78  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def rewind_body--- This code section failed: ---

 L. 106         0  LOAD_GLOBAL              getattr
                2  LOAD_FAST                'body'
                4  LOAD_STR                 'seek'
                6  LOAD_CONST               None
                8  CALL_FUNCTION_3       3  ''
               10  STORE_FAST               'body_seek'

 L. 107        12  LOAD_FAST                'body_seek'
               14  LOAD_CONST               None
               16  <117>                 1  ''
               18  POP_JUMP_IF_FALSE    76  'to 76'
               20  LOAD_GLOBAL              isinstance
               22  LOAD_FAST                'body_pos'
               24  LOAD_GLOBAL              integer_types
               26  CALL_FUNCTION_2       2  ''
               28  POP_JUMP_IF_FALSE    76  'to 76'

 L. 108        30  SETUP_FINALLY        44  'to 44'

 L. 109        32  LOAD_FAST                'body_seek'
               34  LOAD_FAST                'body_pos'
               36  CALL_FUNCTION_1       1  ''
               38  POP_TOP          
               40  POP_BLOCK        
               42  JUMP_ABSOLUTE       110  'to 110'
             44_0  COME_FROM_FINALLY    30  '30'

 L. 110        44  DUP_TOP          
               46  LOAD_GLOBAL              IOError
               48  LOAD_GLOBAL              OSError
               50  BUILD_TUPLE_2         2 
               52  <121>                72  ''
               54  POP_TOP          
               56  POP_TOP          
               58  POP_TOP          

 L. 111        60  LOAD_GLOBAL              UnrewindableBodyError
               62  LOAD_STR                 'An error occurred when rewinding request body for redirect/retry.'
               64  CALL_FUNCTION_1       1  ''
               66  RAISE_VARARGS_1       1  'exception instance'
               68  POP_EXCEPT       
               70  JUMP_ABSOLUTE       110  'to 110'
               72  <48>             
               74  JUMP_FORWARD        110  'to 110'
             76_0  COME_FROM            28  '28'
             76_1  COME_FROM            18  '18'

 L. 113        76  LOAD_FAST                'body_pos'
               78  LOAD_GLOBAL              _FAILEDTELL
               80  <117>                 0  ''
               82  POP_JUMP_IF_FALSE    94  'to 94'

 L. 114        84  LOAD_GLOBAL              UnrewindableBodyError
               86  LOAD_STR                 'Unable to record file position for rewinding request body during a redirect/retry.'
               88  CALL_FUNCTION_1       1  ''
               90  RAISE_VARARGS_1       1  'exception instance'
               92  JUMP_FORWARD        110  'to 110'
             94_0  COME_FROM            82  '82'

 L. 117        94  LOAD_GLOBAL              ValueError
               96  LOAD_STR                 'body_pos must be of type integer, instead it was %s.'

 L. 118        98  LOAD_GLOBAL              type
              100  LOAD_FAST                'body_pos'
              102  CALL_FUNCTION_1       1  ''

 L. 117       104  BINARY_MODULO    
              106  CALL_FUNCTION_1       1  ''
              108  RAISE_VARARGS_1       1  'exception instance'
            110_0  COME_FROM_EXCEPT_CLAUSE    92  '92'
            110_1  COME_FROM_EXCEPT_CLAUSE    74  '74'
            110_2  COME_FROM_EXCEPT_CLAUSE    70  '70'

Parse error at or near `<117>' instruction at offset 16