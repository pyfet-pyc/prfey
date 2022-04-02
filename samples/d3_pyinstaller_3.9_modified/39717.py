# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: requests\api.py
"""
requests.api
~~~~~~~~~~~~

This module implements the Requests API.

:copyright: (c) 2012 by Kenneth Reitz.
:license: Apache2, see LICENSE for more details.
"""
from . import sessions

def request--- This code section failed: ---

 L.  60         0  LOAD_GLOBAL              sessions
                2  LOAD_METHOD              Session
                4  CALL_METHOD_0         0  ''
                6  SETUP_WITH           46  'to 46'
                8  STORE_FAST               'session'

 L.  61        10  LOAD_FAST                'session'
               12  LOAD_ATTR                request
               14  BUILD_TUPLE_0         0 
               16  LOAD_FAST                'method'
               18  LOAD_FAST                'url'
               20  LOAD_CONST               ('method', 'url')
               22  BUILD_CONST_KEY_MAP_2     2 
               24  LOAD_FAST                'kwargs'
               26  <164>                 1  ''
               28  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               30  POP_BLOCK        
               32  ROT_TWO          
               34  LOAD_CONST               None
               36  DUP_TOP          
               38  DUP_TOP          
               40  CALL_FUNCTION_3       3  ''
               42  POP_TOP          
               44  RETURN_VALUE     
             46_0  COME_FROM_WITH        6  '6'
               46  <49>             
               48  POP_JUMP_IF_TRUE     52  'to 52'
               50  <48>             
             52_0  COME_FROM            48  '48'
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          
               58  POP_EXCEPT       
               60  POP_TOP          

Parse error at or near `<164>' instruction at offset 26


def get--- This code section failed: ---

 L.  75         0  LOAD_GLOBAL              request
                2  LOAD_STR                 'get'
                4  LOAD_FAST                'url'
                6  BUILD_TUPLE_2         2 
                8  LOAD_STR                 'params'
               10  LOAD_FAST                'params'
               12  BUILD_MAP_1           1 
               14  LOAD_FAST                'kwargs'
               16  <164>                 1  ''
               18  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               20  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def options--- This code section failed: ---

 L.  87         0  LOAD_GLOBAL              request
                2  LOAD_STR                 'options'
                4  LOAD_FAST                'url'
                6  BUILD_TUPLE_2         2 
                8  BUILD_MAP_0           0 
               10  LOAD_FAST                'kwargs'
               12  <164>                 1  ''
               14  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               16  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def head--- This code section failed: ---

 L. 101         0  LOAD_FAST                'kwargs'
                2  LOAD_METHOD              setdefault
                4  LOAD_STR                 'allow_redirects'
                6  LOAD_CONST               False
                8  CALL_METHOD_2         2  ''
               10  POP_TOP          

 L. 102        12  LOAD_GLOBAL              request
               14  LOAD_STR                 'head'
               16  LOAD_FAST                'url'
               18  BUILD_TUPLE_2         2 
               20  BUILD_MAP_0           0 
               22  LOAD_FAST                'kwargs'
               24  <164>                 1  ''
               26  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 24


def post--- This code section failed: ---

 L. 117         0  LOAD_GLOBAL              request
                2  LOAD_STR                 'post'
                4  LOAD_FAST                'url'
                6  BUILD_TUPLE_2         2 
                8  LOAD_FAST                'data'
               10  LOAD_FAST                'json'
               12  LOAD_CONST               ('data', 'json')
               14  BUILD_CONST_KEY_MAP_2     2 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def put--- This code section failed: ---

 L. 132         0  LOAD_GLOBAL              request
                2  LOAD_STR                 'put'
                4  LOAD_FAST                'url'
                6  BUILD_TUPLE_2         2 
                8  LOAD_STR                 'data'
               10  LOAD_FAST                'data'
               12  BUILD_MAP_1           1 
               14  LOAD_FAST                'kwargs'
               16  <164>                 1  ''
               18  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               20  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def patch--- This code section failed: ---

 L. 147         0  LOAD_GLOBAL              request
                2  LOAD_STR                 'patch'
                4  LOAD_FAST                'url'
                6  BUILD_TUPLE_2         2 
                8  LOAD_STR                 'data'
               10  LOAD_FAST                'data'
               12  BUILD_MAP_1           1 
               14  LOAD_FAST                'kwargs'
               16  <164>                 1  ''
               18  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               20  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def delete--- This code section failed: ---

 L. 159         0  LOAD_GLOBAL              request
                2  LOAD_STR                 'delete'
                4  LOAD_FAST                'url'
                6  BUILD_TUPLE_2         2 
                8  BUILD_MAP_0           0 
               10  LOAD_FAST                'kwargs'
               12  <164>                 1  ''
               14  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               16  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1