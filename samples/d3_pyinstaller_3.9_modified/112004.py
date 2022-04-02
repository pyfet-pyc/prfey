# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: setuptools\extension.py
import re, functools, distutils.core, distutils.errors, distutils.extension
from .monkey import get_unpatched

def _have_cython--- This code section failed: ---

 L.  14         0  LOAD_STR                 'Cython.Distutils.build_ext'
                2  STORE_FAST               'cython_impl'

 L.  15         4  SETUP_FINALLY        28  'to 28'

 L.  17         6  LOAD_GLOBAL              __import__
                8  LOAD_FAST                'cython_impl'
               10  LOAD_STR                 'build_ext'
               12  BUILD_LIST_1          1 
               14  LOAD_CONST               ('fromlist',)
               16  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               18  LOAD_ATTR                build_ext
               20  POP_TOP          

 L.  18        22  POP_BLOCK        
               24  LOAD_CONST               True
               26  RETURN_VALUE     
             28_0  COME_FROM_FINALLY     4  '4'

 L.  19        28  DUP_TOP          
               30  LOAD_GLOBAL              Exception
               32  <121>                44  ''
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L.  20        40  POP_EXCEPT       
               42  JUMP_FORWARD         46  'to 46'
               44  <48>             
             46_0  COME_FROM            42  '42'

 L.  21        46  LOAD_CONST               False
               48  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 28


have_pyrex = _have_cython
_Extension = get_unpatched(distutils.core.Extension)

class Extension(_Extension):
    __doc__ = "Extension that uses '.c' files in place of '.pyx' files"

    def __init__--- This code section failed: ---

 L.  36         0  LOAD_FAST                'kw'
                2  LOAD_METHOD              pop
                4  LOAD_STR                 'py_limited_api'
                6  LOAD_CONST               False
                8  CALL_METHOD_2         2  ''
               10  LOAD_FAST                'self'
               12  STORE_ATTR               py_limited_api

 L.  37        14  LOAD_GLOBAL              _Extension
               16  LOAD_ATTR                __init__
               18  LOAD_FAST                'self'
               20  LOAD_FAST                'name'
               22  LOAD_FAST                'sources'
               24  BUILD_LIST_3          3 
               26  LOAD_FAST                'args'
               28  CALL_FINALLY         31  'to 31'
               30  WITH_CLEANUP_FINISH
               32  BUILD_MAP_0           0 
               34  LOAD_FAST                'kw'
               36  <164>                 1  ''
               38  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               40  POP_TOP          

Parse error at or near `CALL_FINALLY' instruction at offset 28

    def _convert_pyx_sources_to_lang(self):
        """
        Replace sources with .pyx extensions to sources with the target
        language extension. This mechanism allows language authors to supply
        pre-converted sources but to prefer the .pyx sources.
        """
        if _have_cython():
            return
        lang = self.language or ''
        target_ext = '.cpp' if lang.lower() == 'c++' else '.c'
        sub = functools.partial(re.sub, '.pyx$', target_ext)
        self.sources = list(map(sub, self.sources))


class Library(Extension):
    __doc__ = 'Just like a regular Extension, but built as a library instead'