# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: aiohttp\web_middlewares.py
import re
from typing import TYPE_CHECKING, Awaitable, Callable, Tuple, Type, TypeVar
from .web_exceptions import HTTPPermanentRedirect, _HTTPMove
from .web_request import Request
from .web_response import StreamResponse
from .web_urldispatcher import SystemRoute
__all__ = ('middleware', 'normalize_path_middleware')
if TYPE_CHECKING:
    from .web_app import Application
_Func = TypeVar('_Func')

async def _check_request_resolves--- This code section failed: ---

 L.  21         0  LOAD_FAST                'request'
                2  LOAD_ATTR                clone
                4  LOAD_FAST                'path'
                6  LOAD_CONST               ('rel_url',)
                8  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               10  STORE_FAST               'alt_request'

 L.  23        12  LOAD_FAST                'request'
               14  LOAD_ATTR                app
               16  LOAD_ATTR                router
               18  LOAD_METHOD              resolve
               20  LOAD_FAST                'alt_request'
               22  CALL_METHOD_1         1  ''
               24  GET_AWAITABLE    
               26  LOAD_CONST               None
               28  YIELD_FROM       
               30  STORE_FAST               'match_info'

 L.  24        32  LOAD_FAST                'match_info'
               34  LOAD_FAST                'alt_request'
               36  STORE_ATTR               _match_info

 L.  26        38  LOAD_FAST                'match_info'
               40  LOAD_ATTR                http_exception
               42  LOAD_CONST               None
               44  <117>                 0  ''
               46  POP_JUMP_IF_FALSE    56  'to 56'

 L.  27        48  LOAD_CONST               True
               50  LOAD_FAST                'alt_request'
               52  BUILD_TUPLE_2         2 
               54  RETURN_VALUE     
             56_0  COME_FROM            46  '46'

 L.  29        56  LOAD_CONST               False
               58  LOAD_FAST                'request'
               60  BUILD_TUPLE_2         2 
               62  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 44


def middleware(f: _Func) -> _Func:
    f.__middleware_version__ = 1
    return f


_Handler = Callable[([Request], Awaitable[StreamResponse])]
_Middleware = Callable[([Request, _Handler], Awaitable[StreamResponse])]

def normalize_path_middleware--- This code section failed: ---

 L.  78         0  LOAD_DEREF               'append_slash'
                2  JUMP_IF_FALSE_OR_POP     6  'to 6'
                4  LOAD_DEREF               'remove_slash'
              6_0  COME_FROM             2  '2'
                6  UNARY_NOT        
                8  STORE_FAST               'correct_configuration'

 L.  79        10  LOAD_FAST                'correct_configuration'
               12  POP_JUMP_IF_TRUE     22  'to 22'
               14  <74>             
               16  LOAD_STR                 'Cannot both remove and append slash'
               18  CALL_FUNCTION_1       1  ''
               20  RAISE_VARARGS_1       1  'exception instance'
             22_0  COME_FROM            12  '12'

 L.  81        22  LOAD_GLOBAL              middleware

 L.  82        24  LOAD_GLOBAL              Request
               26  LOAD_GLOBAL              _Handler
               28  LOAD_GLOBAL              StreamResponse
               30  LOAD_CONST               ('request', 'handler', 'return')
               32  BUILD_CONST_KEY_MAP_3     3 
               34  LOAD_CLOSURE             'append_slash'
               36  LOAD_CLOSURE             'merge_slashes'
               38  LOAD_CLOSURE             'redirect_class'
               40  LOAD_CLOSURE             'remove_slash'
               42  BUILD_TUPLE_4         4 
               44  LOAD_CODE                <code_object impl>
               46  LOAD_STR                 'normalize_path_middleware.<locals>.impl'
               48  MAKE_FUNCTION_12         'annotation, closure'
               50  CALL_FUNCTION_1       1  ''
               52  STORE_FAST               'impl'

 L. 112        54  LOAD_FAST                'impl'
               56  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 14


def _fix_request_current_app(app: 'Application') -> _Middleware:

    @middleware
    async def impl--- This code section failed: ---

 L. 118         0  LOAD_FAST                'request'
                2  LOAD_ATTR                match_info
                4  LOAD_METHOD              set_current_app
                6  LOAD_DEREF               'app'
                8  CALL_METHOD_1         1  ''
               10  SETUP_WITH           42  'to 42'
               12  POP_TOP          

 L. 119        14  LOAD_FAST                'handler'
               16  LOAD_FAST                'request'
               18  CALL_FUNCTION_1       1  ''
               20  GET_AWAITABLE    
               22  LOAD_CONST               None
               24  YIELD_FROM       
               26  POP_BLOCK        
               28  ROT_TWO          
               30  LOAD_CONST               None
               32  DUP_TOP          
               34  DUP_TOP          
               36  CALL_FUNCTION_3       3  ''
               38  POP_TOP          
               40  RETURN_VALUE     
             42_0  COME_FROM_WITH       10  '10'
               42  <49>             
               44  POP_JUMP_IF_TRUE     48  'to 48'
               46  <48>             
             48_0  COME_FROM            44  '44'
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          
               54  POP_EXCEPT       
               56  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 30

    return impl