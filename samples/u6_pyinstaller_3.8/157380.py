# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\setuptools\extension.py
import re, functools, distutils.core, distutils.errors, distutils.extension
from setuptools.extern.six.moves import map
from .monkey import get_unpatched

def _have_cython--- This code section failed: ---

 L.  16         0  LOAD_STR                 'Cython.Distutils.build_ext'
                2  STORE_FAST               'cython_impl'

 L.  17         4  SETUP_FINALLY        28  'to 28'

 L.  19         6  LOAD_GLOBAL              __import__
                8  LOAD_FAST                'cython_impl'
               10  LOAD_STR                 'build_ext'
               12  BUILD_LIST_1          1 
               14  LOAD_CONST               ('fromlist',)
               16  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               18  LOAD_ATTR                build_ext
               20  POP_TOP          

 L.  20        22  POP_BLOCK        
               24  LOAD_CONST               True
               26  RETURN_VALUE     
             28_0  COME_FROM_FINALLY     4  '4'

 L.  21        28  DUP_TOP          
               30  LOAD_GLOBAL              Exception
               32  COMPARE_OP               exception-match
               34  POP_JUMP_IF_FALSE    46  'to 46'
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L.  22        42  POP_EXCEPT       
               44  JUMP_FORWARD         48  'to 48'
             46_0  COME_FROM            34  '34'
               46  END_FINALLY      
             48_0  COME_FROM            44  '44'

 L.  23        48  LOAD_CONST               False
               50  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 26


have_pyrex = _have_cython
_Extension = get_unpatched(distutils.core.Extension)

class Extension(_Extension):
    __doc__ = "Extension that uses '.c' files in place of '.pyx' files"

    def __init__(self, name, sources, *args, **kw):
        self.py_limited_api = kw.pop('py_limited_api', False)
        (_Extension.__init__)(self, name, sources, *args, **kw)

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