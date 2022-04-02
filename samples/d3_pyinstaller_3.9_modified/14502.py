# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: urllib3\contrib\_appengine_environ.py
"""
This module provides means to detect the App Engine environment.
"""
import os

def is_appengine():
    return is_local_appengine() or is_prod_appengine() or is_prod_appengine_mvms()


def is_appengine_sandbox():
    return is_appengine() and not is_prod_appengine_mvms()


def is_local_appengine--- This code section failed: ---

 L.  19         0  LOAD_STR                 'APPENGINE_RUNTIME'
                2  LOAD_GLOBAL              os
                4  LOAD_ATTR                environ
                6  <118>                 0  ''
                8  JUMP_IF_FALSE_OR_POP    22  'to 22'

 L.  20        10  LOAD_STR                 'Development/'
               12  LOAD_GLOBAL              os
               14  LOAD_ATTR                environ
               16  LOAD_STR                 'SERVER_SOFTWARE'
               18  BINARY_SUBSCR    
               20  <118>                 0  ''
             22_0  COME_FROM             8  '8'

 L.  19        22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def is_prod_appengine--- This code section failed: ---

 L.  24         0  LOAD_STR                 'APPENGINE_RUNTIME'
                2  LOAD_GLOBAL              os
                4  LOAD_ATTR                environ
                6  <118>                 0  ''
                8  JUMP_IF_FALSE_OR_POP    30  'to 30'

 L.  25        10  LOAD_STR                 'Google App Engine/'
               12  LOAD_GLOBAL              os
               14  LOAD_ATTR                environ
               16  LOAD_STR                 'SERVER_SOFTWARE'
               18  BINARY_SUBSCR    
               20  <118>                 0  ''

 L.  24        22  JUMP_IF_FALSE_OR_POP    30  'to 30'

 L.  26        24  LOAD_GLOBAL              is_prod_appengine_mvms
               26  CALL_FUNCTION_0       0  ''
               28  UNARY_NOT        
             30_0  COME_FROM            22  '22'
             30_1  COME_FROM             8  '8'

 L.  24        30  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def is_prod_appengine_mvms():
    return os.environ.get('GAE_VM', False) == 'true'