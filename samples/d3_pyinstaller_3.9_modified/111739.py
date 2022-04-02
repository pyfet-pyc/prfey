# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PyInstaller\fake-modules\site.py
"""
This is a fake 'site' module available in default Python Library.

The real 'site' does some magic to find paths to other possible
Python modules. We do not want this behaviour for frozen applications.

Fake 'site' makes PyInstaller to work with distutils and to work inside
virtualenv environment.
"""
__pyinstaller__faked__site__module__ = True
PREFIXES = []
ENABLE_USER_SITE = False
USER_SITE = ''
USER_BASE = ''

class _Helper(object):
    __doc__ = "\n     Define the builtin 'help'.\n     This is a wrapper around pydoc.help (with a twist).\n     "

    def __repr__(self):
        return 'Type help() for interactive help, or help(object) for help about object.'

    def __call__--- This code section failed: ---

 L.  60         0  LOAD_GLOBAL              __import__
                2  LOAD_STR                 ''
                4  LOAD_METHOD              join
                6  LOAD_STR                 'pydoc'
                8  CALL_METHOD_1         1  ''
               10  CALL_FUNCTION_1       1  ''
               12  STORE_FAST               'pydoc'

 L.  61        14  LOAD_FAST                'pydoc'
               16  LOAD_ATTR                help
               18  LOAD_FAST                'args'
               20  BUILD_MAP_0           0 
               22  LOAD_FAST                'kwds'
               24  <164>                 1  ''
               26  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 24