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
    return is_local_appengine() or is_prod_appengine()


def is_appengine_sandbox():
    """Reports if the app is running in the first generation sandbox.

    The second generation runtimes are technically still in a sandbox, but it
    is much less restrictive, so generally you shouldn't need to check for it.
    see https://cloud.google.com/appengine/docs/standard/runtimes
    """
    return is_appengine() and os.environ['APPENGINE_RUNTIME'] == 'python27'


def is_local_appengine--- This code section failed: ---

 L.  23         0  LOAD_STR                 'APPENGINE_RUNTIME'
                2  LOAD_GLOBAL              os
                4  LOAD_ATTR                environ
                6  <118>                 0  ''
                8  JUMP_IF_FALSE_OR_POP    28  'to 28'
               10  LOAD_GLOBAL              os
               12  LOAD_ATTR                environ
               14  LOAD_METHOD              get

 L.  24        16  LOAD_STR                 'SERVER_SOFTWARE'
               18  LOAD_STR                 ''

 L.  23        20  CALL_METHOD_2         2  ''
               22  LOAD_METHOD              startswith

 L.  25        24  LOAD_STR                 'Development/'

 L.  23        26  CALL_METHOD_1         1  ''
             28_0  COME_FROM             8  '8'
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def is_prod_appengine--- This code section failed: ---

 L.  29         0  LOAD_STR                 'APPENGINE_RUNTIME'
                2  LOAD_GLOBAL              os
                4  LOAD_ATTR                environ
                6  <118>                 0  ''
                8  JUMP_IF_FALSE_OR_POP    28  'to 28'
               10  LOAD_GLOBAL              os
               12  LOAD_ATTR                environ
               14  LOAD_METHOD              get

 L.  30        16  LOAD_STR                 'SERVER_SOFTWARE'
               18  LOAD_STR                 ''

 L.  29        20  CALL_METHOD_2         2  ''
               22  LOAD_METHOD              startswith

 L.  31        24  LOAD_STR                 'Google App Engine/'

 L.  29        26  CALL_METHOD_1         1  ''
             28_0  COME_FROM             8  '8'
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def is_prod_appengine_mvms():
    """Deprecated."""
    return False