# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cffi\verifier.py
import sys, os, binascii, shutil, io
from . import __version_verifier_modules__
from . import ffiplatform
from .error import VerificationError
if sys.version_info >= (3, 3):
    import importlib.machinery

    def _extension_suffixes():
        return importlib.machinery.EXTENSION_SUFFIXES[:]


else:
    import imp

    def _extension_suffixes():
        return [suffix for suffix, _, type in imp.get_suffixes() if type == imp.C_EXTENSION]


if sys.version_info >= (3, ):
    NativeIO = io.StringIO
else:

    class NativeIO(io.BytesIO):

        def write(self, s):
            if isinstance(s, unicode):
                s = s.encode('ascii')
            super(NativeIO, self).write(s)


class Verifier(object):

    def __init__(self, ffi, preamble, tmpdir=None, modulename=None, ext_package=None, tag='', force_generic_engine=False, source_extension='.c', flags=None, relative_to=None, **kwds):
        if ffi._parser._uses_new_feature:
            raise VerificationError('feature not supported with ffi.verify(), but only with ffi.set_source(): %s' % (
             ffi._parser._uses_new_feature,))
        self.ffi = ffi
        self.preamble = preamble
        if not modulename:
            flattened_kwds = ffiplatform.flatten(kwds)
        vengine_class = _locate_engine_class(ffi, force_generic_engine)
        self._vengine = vengine_class(self)
        self._vengine.patch_extension_kwds(kwds)
        self.flags = flags
        self.kwds = self.make_relative_to(kwds, relative_to)
        if modulename:
            if tag:
                raise TypeError("can't specify both 'modulename' and 'tag'")
        else:
            key = '\x00'.join([sys.version[:3], __version_verifier_modules__,
             preamble, flattened_kwds] + ffi._cdefsources)
            if sys.version_info >= (3, ):
                key = key.encode('utf-8')
            k1 = hex(binascii.crc32(key[0::2]) & 4294967295)
            k1 = k1.lstrip('0x').rstrip('L')
            k2 = hex(binascii.crc32(key[1::2]) & 4294967295)
            k2 = k2.lstrip('0').rstrip('L')
            modulename = '_cffi_%s_%s%s%s' % (tag, self._vengine._class_key,
             k1, k2)
        suffix = _get_so_suffixes()[0]
        self.tmpdir = tmpdir or _caller_dir_pycache()
        self.sourcefilename = os.path.join(self.tmpdir, modulename + source_extension)
        self.modulefilename = os.path.join(self.tmpdir, modulename + suffix)
        self.ext_package = ext_package
        self._has_source = False
        self._has_module = False

    def write_source--- This code section failed: ---

 L.  75         0  LOAD_FAST                'self'
                2  LOAD_ATTR                ffi
                4  LOAD_ATTR                _lock
                6  SETUP_WITH           56  'to 56'
                8  POP_TOP          

 L.  76        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _has_source
               14  POP_JUMP_IF_FALSE    32  'to 32'
               16  LOAD_FAST                'file'
               18  LOAD_CONST               None
               20  <117>                 0  ''
               22  POP_JUMP_IF_FALSE    32  'to 32'

 L.  77        24  LOAD_GLOBAL              VerificationError

 L.  78        26  LOAD_STR                 'source code already written'

 L.  77        28  CALL_FUNCTION_1       1  ''
               30  RAISE_VARARGS_1       1  'exception instance'
             32_0  COME_FROM            22  '22'
             32_1  COME_FROM            14  '14'

 L.  79        32  LOAD_FAST                'self'
               34  LOAD_METHOD              _write_source
               36  LOAD_FAST                'file'
               38  CALL_METHOD_1         1  ''
               40  POP_TOP          
               42  POP_BLOCK        
               44  LOAD_CONST               None
               46  DUP_TOP          
               48  DUP_TOP          
               50  CALL_FUNCTION_3       3  ''
               52  POP_TOP          
               54  JUMP_FORWARD         72  'to 72'
             56_0  COME_FROM_WITH        6  '6'
               56  <49>             
               58  POP_JUMP_IF_TRUE     62  'to 62'
               60  <48>             
             62_0  COME_FROM            58  '58'
               62  POP_TOP          
               64  POP_TOP          
               66  POP_TOP          
               68  POP_EXCEPT       
               70  POP_TOP          
             72_0  COME_FROM            54  '54'

Parse error at or near `<117>' instruction at offset 20

    def compile_module--- This code section failed: ---

 L.  84         0  LOAD_FAST                'self'
                2  LOAD_ATTR                ffi
                4  LOAD_ATTR                _lock
                6  SETUP_WITH           60  'to 60'
                8  POP_TOP          

 L.  85        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _has_module
               14  POP_JUMP_IF_FALSE    24  'to 24'

 L.  86        16  LOAD_GLOBAL              VerificationError
               18  LOAD_STR                 'module already compiled'
               20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            14  '14'

 L.  87        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _has_source
               28  POP_JUMP_IF_TRUE     38  'to 38'

 L.  88        30  LOAD_FAST                'self'
               32  LOAD_METHOD              _write_source
               34  CALL_METHOD_0         0  ''
               36  POP_TOP          
             38_0  COME_FROM            28  '28'

 L.  89        38  LOAD_FAST                'self'
               40  LOAD_METHOD              _compile_module
               42  CALL_METHOD_0         0  ''
               44  POP_TOP          
               46  POP_BLOCK        
               48  LOAD_CONST               None
               50  DUP_TOP          
               52  DUP_TOP          
               54  CALL_FUNCTION_3       3  ''
               56  POP_TOP          
               58  JUMP_FORWARD         76  'to 76'
             60_0  COME_FROM_WITH        6  '6'
               60  <49>             
               62  POP_JUMP_IF_TRUE     66  'to 66'
               64  <48>             
             66_0  COME_FROM            62  '62'
               66  POP_TOP          
               68  POP_TOP          
               70  POP_TOP          
               72  POP_EXCEPT       
               74  POP_TOP          
             76_0  COME_FROM            58  '58'

Parse error at or near `DUP_TOP' instruction at offset 50

    def load_library--- This code section failed: ---

 L.  98         0  LOAD_FAST                'self'
                2  LOAD_ATTR                ffi
                4  LOAD_ATTR                _lock
                6  SETUP_WITH           74  'to 74'
                8  POP_TOP          

 L.  99        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _has_module
               14  POP_JUMP_IF_TRUE     52  'to 52'

 L. 100        16  LOAD_FAST                'self'
               18  LOAD_METHOD              _locate_module
               20  CALL_METHOD_0         0  ''
               22  POP_TOP          

 L. 101        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _has_module
               28  POP_JUMP_IF_TRUE     52  'to 52'

 L. 102        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _has_source
               34  POP_JUMP_IF_TRUE     44  'to 44'

 L. 103        36  LOAD_FAST                'self'
               38  LOAD_METHOD              _write_source
               40  CALL_METHOD_0         0  ''
               42  POP_TOP          
             44_0  COME_FROM            34  '34'

 L. 104        44  LOAD_FAST                'self'
               46  LOAD_METHOD              _compile_module
               48  CALL_METHOD_0         0  ''
               50  POP_TOP          
             52_0  COME_FROM            28  '28'
             52_1  COME_FROM            14  '14'

 L. 105        52  LOAD_FAST                'self'
               54  LOAD_METHOD              _load_library
               56  CALL_METHOD_0         0  ''
               58  POP_BLOCK        
               60  ROT_TWO          
               62  LOAD_CONST               None
               64  DUP_TOP          
               66  DUP_TOP          
               68  CALL_FUNCTION_3       3  ''
               70  POP_TOP          
               72  RETURN_VALUE     
             74_0  COME_FROM_WITH        6  '6'
               74  <49>             
               76  POP_JUMP_IF_TRUE     80  'to 80'
               78  <48>             
             80_0  COME_FROM            76  '76'
               80  POP_TOP          
               82  POP_TOP          
               84  POP_TOP          
               86  POP_EXCEPT       
               88  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 62

    def get_module_name(self):
        basename = os.path.basename(self.modulefilename)
        basename = basename.split('.', 1)[0]
        if basename.endswith('_d'):
            if hasattr(sys, 'gettotalrefcount'):
                basename = basename[:-2]
        return basename

    def get_extension--- This code section failed: ---

 L. 119         0  LOAD_GLOBAL              ffiplatform
                2  LOAD_METHOD              _hack_at_distutils
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 120         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _has_source
               12  POP_JUMP_IF_TRUE     68  'to 68'

 L. 121        14  LOAD_FAST                'self'
               16  LOAD_ATTR                ffi
               18  LOAD_ATTR                _lock
               20  SETUP_WITH           52  'to 52'
               22  POP_TOP          

 L. 122        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _has_source
               28  POP_JUMP_IF_TRUE     38  'to 38'

 L. 123        30  LOAD_FAST                'self'
               32  LOAD_METHOD              _write_source
               34  CALL_METHOD_0         0  ''
               36  POP_TOP          
             38_0  COME_FROM            28  '28'
               38  POP_BLOCK        
               40  LOAD_CONST               None
               42  DUP_TOP          
               44  DUP_TOP          
               46  CALL_FUNCTION_3       3  ''
               48  POP_TOP          
               50  JUMP_FORWARD         68  'to 68'
             52_0  COME_FROM_WITH       20  '20'
               52  <49>             
               54  POP_JUMP_IF_TRUE     58  'to 58'
               56  <48>             
             58_0  COME_FROM            54  '54'
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          
               64  POP_EXCEPT       
               66  POP_TOP          
             68_0  COME_FROM            50  '50'
             68_1  COME_FROM            12  '12'

 L. 124        68  LOAD_GLOBAL              ffiplatform
               70  LOAD_METHOD              maybe_relative_path
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                sourcefilename
               76  CALL_METHOD_1         1  ''
               78  STORE_FAST               'sourcename'

 L. 125        80  LOAD_FAST                'self'
               82  LOAD_METHOD              get_module_name
               84  CALL_METHOD_0         0  ''
               86  STORE_FAST               'modname'

 L. 126        88  LOAD_GLOBAL              ffiplatform
               90  LOAD_ATTR                get_extension
               92  LOAD_FAST                'sourcename'
               94  LOAD_FAST                'modname'
               96  BUILD_TUPLE_2         2 
               98  BUILD_MAP_0           0 
              100  LOAD_FAST                'self'
              102  LOAD_ATTR                kwds
              104  <164>                 1  ''
              106  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              108  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 42

    def generates_python_module(self):
        return self._vengine._gen_python_module

    def make_relative_to--- This code section failed: ---

 L. 132         0  LOAD_FAST                'relative_to'
                2  POP_JUMP_IF_FALSE   118  'to 118'
                4  LOAD_GLOBAL              os
                6  LOAD_ATTR                path
                8  LOAD_METHOD              dirname
               10  LOAD_FAST                'relative_to'
               12  CALL_METHOD_1         1  ''
               14  POP_JUMP_IF_FALSE   118  'to 118'

 L. 133        16  LOAD_GLOBAL              os
               18  LOAD_ATTR                path
               20  LOAD_METHOD              dirname
               22  LOAD_FAST                'relative_to'
               24  CALL_METHOD_1         1  ''
               26  STORE_DEREF              'dirname'

 L. 134        28  LOAD_FAST                'kwds'
               30  LOAD_METHOD              copy
               32  CALL_METHOD_0         0  ''
               34  STORE_FAST               'kwds'

 L. 135        36  LOAD_GLOBAL              ffiplatform
               38  LOAD_ATTR                LIST_OF_FILE_NAMES
               40  GET_ITER         
             42_0  COME_FROM           116  '116'
             42_1  COME_FROM            52  '52'
               42  FOR_ITER            118  'to 118'
               44  STORE_FAST               'key'

 L. 136        46  LOAD_FAST                'key'
               48  LOAD_FAST                'kwds'
               50  <118>                 0  ''
               52  POP_JUMP_IF_FALSE_BACK    42  'to 42'

 L. 137        54  LOAD_FAST                'kwds'
               56  LOAD_FAST                'key'
               58  BINARY_SUBSCR    
               60  STORE_FAST               'lst'

 L. 138        62  LOAD_GLOBAL              isinstance
               64  LOAD_FAST                'lst'
               66  LOAD_GLOBAL              list
               68  LOAD_GLOBAL              tuple
               70  BUILD_TUPLE_2         2 
               72  CALL_FUNCTION_2       2  ''
               74  POP_JUMP_IF_TRUE     90  'to 90'

 L. 139        76  LOAD_GLOBAL              TypeError
               78  LOAD_STR                 "keyword '%s' should be a list or tuple"

 L. 140        80  LOAD_FAST                'key'
               82  BUILD_TUPLE_1         1 

 L. 139        84  BINARY_MODULO    
               86  CALL_FUNCTION_1       1  ''
               88  RAISE_VARARGS_1       1  'exception instance'
             90_0  COME_FROM            74  '74'

 L. 141        90  LOAD_CLOSURE             'dirname'
               92  BUILD_TUPLE_1         1 
               94  LOAD_LISTCOMP            '<code_object <listcomp>>'
               96  LOAD_STR                 'Verifier.make_relative_to.<locals>.<listcomp>'
               98  MAKE_FUNCTION_8          'closure'
              100  LOAD_FAST                'lst'
              102  GET_ITER         
              104  CALL_FUNCTION_1       1  ''
              106  STORE_FAST               'lst'

 L. 142       108  LOAD_FAST                'lst'
              110  LOAD_FAST                'kwds'
              112  LOAD_FAST                'key'
              114  STORE_SUBSCR     
              116  JUMP_BACK            42  'to 42'
            118_0  COME_FROM            42  '42'
            118_1  COME_FROM            14  '14'
            118_2  COME_FROM             2  '2'

 L. 143       118  LOAD_FAST                'kwds'
              120  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 50

    def _locate_module--- This code section failed: ---

 L. 148         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              isfile
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                modulefilename
               10  CALL_METHOD_1         1  ''
               12  POP_JUMP_IF_TRUE    116  'to 116'

 L. 149        14  LOAD_FAST                'self'
               16  LOAD_ATTR                ext_package
               18  POP_JUMP_IF_FALSE    72  'to 72'

 L. 150        20  SETUP_FINALLY        44  'to 44'

 L. 151        22  LOAD_GLOBAL              __import__
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                ext_package
               28  LOAD_CONST               None
               30  LOAD_CONST               None
               32  LOAD_STR                 '__doc__'
               34  BUILD_LIST_1          1 
               36  CALL_FUNCTION_4       4  ''
               38  STORE_FAST               'pkg'
               40  POP_BLOCK        
               42  JUMP_FORWARD         64  'to 64'
             44_0  COME_FROM_FINALLY    20  '20'

 L. 152        44  DUP_TOP          
               46  LOAD_GLOBAL              ImportError
               48  <121>                62  ''
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L. 153        56  POP_EXCEPT       
               58  LOAD_CONST               None
               60  RETURN_VALUE     
               62  <48>             
             64_0  COME_FROM            42  '42'

 L. 155        64  LOAD_FAST                'pkg'
               66  LOAD_ATTR                __path__
               68  STORE_FAST               'path'
               70  JUMP_FORWARD         76  'to 76'
             72_0  COME_FROM            18  '18'

 L. 157        72  LOAD_CONST               None
               74  STORE_FAST               'path'
             76_0  COME_FROM            70  '70'

 L. 158        76  LOAD_FAST                'self'
               78  LOAD_ATTR                _vengine
               80  LOAD_METHOD              find_module
               82  LOAD_FAST                'self'
               84  LOAD_METHOD              get_module_name
               86  CALL_METHOD_0         0  ''
               88  LOAD_FAST                'path'

 L. 159        90  LOAD_GLOBAL              _get_so_suffixes
               92  CALL_FUNCTION_0       0  ''

 L. 158        94  CALL_METHOD_3         3  ''
               96  STORE_FAST               'filename'

 L. 160        98  LOAD_FAST                'filename'
              100  LOAD_CONST               None
              102  <117>                 0  ''
              104  POP_JUMP_IF_FALSE   110  'to 110'

 L. 161       106  LOAD_CONST               None
              108  RETURN_VALUE     
            110_0  COME_FROM           104  '104'

 L. 162       110  LOAD_FAST                'filename'
              112  LOAD_FAST                'self'
              114  STORE_ATTR               modulefilename
            116_0  COME_FROM            12  '12'

 L. 163       116  LOAD_FAST                'self'
              118  LOAD_ATTR                _vengine
              120  LOAD_METHOD              collect_types
              122  CALL_METHOD_0         0  ''
              124  POP_TOP          

 L. 164       126  LOAD_CONST               True
              128  LOAD_FAST                'self'
              130  STORE_ATTR               _has_module

Parse error at or near `<121>' instruction at offset 48

    def _write_source_to--- This code section failed: ---

 L. 167         0  LOAD_FAST                'file'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _vengine
                6  STORE_ATTR               _f

 L. 168         8  SETUP_FINALLY        30  'to 30'

 L. 169        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _vengine
               14  LOAD_METHOD              write_source_to_f
               16  CALL_METHOD_0         0  ''
               18  POP_TOP          
               20  POP_BLOCK        

 L. 171        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _vengine
               26  DELETE_ATTR              _f
               28  JUMP_FORWARD         38  'to 38'
             30_0  COME_FROM_FINALLY     8  '8'
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                _vengine
               34  DELETE_ATTR              _f
               36  <48>             
             38_0  COME_FROM            28  '28'

Parse error at or near `DELETE_ATTR' instruction at offset 26

    def _write_source--- This code section failed: ---

 L. 174         0  LOAD_FAST                'file'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    20  'to 20'

 L. 175         8  LOAD_FAST                'self'
               10  LOAD_METHOD              _write_source_to
               12  LOAD_FAST                'file'
               14  CALL_METHOD_1         1  ''
               16  POP_TOP          
               18  JUMP_FORWARD        196  'to 196'
             20_0  COME_FROM             6  '6'

 L. 178        20  LOAD_GLOBAL              NativeIO
               22  CALL_FUNCTION_0       0  ''
               24  STORE_FAST               'f'

 L. 179        26  LOAD_FAST                'self'
               28  LOAD_METHOD              _write_source_to
               30  LOAD_FAST                'f'
               32  CALL_METHOD_1         1  ''
               34  POP_TOP          

 L. 180        36  LOAD_FAST                'f'
               38  LOAD_METHOD              getvalue
               40  CALL_METHOD_0         0  ''
               42  STORE_FAST               'source_data'

 L. 183        44  LOAD_GLOBAL              os
               46  LOAD_ATTR                path
               48  LOAD_METHOD              exists
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                sourcefilename
               54  CALL_METHOD_1         1  ''
               56  POP_JUMP_IF_FALSE   118  'to 118'

 L. 184        58  LOAD_GLOBAL              open
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                sourcefilename
               64  LOAD_STR                 'r'
               66  CALL_FUNCTION_2       2  ''
               68  SETUP_WITH          100  'to 100'
               70  STORE_FAST               'fp'

 L. 185        72  LOAD_FAST                'fp'
               74  LOAD_METHOD              read
               76  CALL_METHOD_0         0  ''
               78  LOAD_FAST                'source_data'
               80  COMPARE_OP               ==
               82  UNARY_NOT        
               84  STORE_FAST               'needs_written'
               86  POP_BLOCK        
               88  LOAD_CONST               None
               90  DUP_TOP          
               92  DUP_TOP          
               94  CALL_FUNCTION_3       3  ''
               96  POP_TOP          
               98  JUMP_FORWARD        122  'to 122'
            100_0  COME_FROM_WITH       68  '68'
              100  <49>             
              102  POP_JUMP_IF_TRUE    106  'to 106'
              104  <48>             
            106_0  COME_FROM           102  '102'
              106  POP_TOP          
              108  POP_TOP          
              110  POP_TOP          
              112  POP_EXCEPT       
              114  POP_TOP          
              116  JUMP_FORWARD        122  'to 122'
            118_0  COME_FROM            56  '56'

 L. 187       118  LOAD_CONST               True
              120  STORE_FAST               'needs_written'
            122_0  COME_FROM           116  '116'
            122_1  COME_FROM            98  '98'

 L. 190       122  LOAD_FAST                'needs_written'
              124  POP_JUMP_IF_FALSE   190  'to 190'

 L. 191       126  LOAD_GLOBAL              _ensure_dir
              128  LOAD_FAST                'self'
              130  LOAD_ATTR                sourcefilename
              132  CALL_FUNCTION_1       1  ''
              134  POP_TOP          

 L. 192       136  LOAD_GLOBAL              open
              138  LOAD_FAST                'self'
              140  LOAD_ATTR                sourcefilename
              142  LOAD_STR                 'w'
              144  CALL_FUNCTION_2       2  ''
              146  SETUP_WITH          174  'to 174'
              148  STORE_FAST               'fp'

 L. 193       150  LOAD_FAST                'fp'
              152  LOAD_METHOD              write
              154  LOAD_FAST                'source_data'
              156  CALL_METHOD_1         1  ''
              158  POP_TOP          
              160  POP_BLOCK        
              162  LOAD_CONST               None
              164  DUP_TOP          
              166  DUP_TOP          
              168  CALL_FUNCTION_3       3  ''
              170  POP_TOP          
              172  JUMP_FORWARD        190  'to 190'
            174_0  COME_FROM_WITH      146  '146'
              174  <49>             
              176  POP_JUMP_IF_TRUE    180  'to 180'
              178  <48>             
            180_0  COME_FROM           176  '176'
              180  POP_TOP          
              182  POP_TOP          
              184  POP_TOP          
              186  POP_EXCEPT       
              188  POP_TOP          
            190_0  COME_FROM           172  '172'
            190_1  COME_FROM           124  '124'

 L. 196       190  LOAD_CONST               True
              192  LOAD_FAST                'self'
              194  STORE_ATTR               _has_source
            196_0  COME_FROM            18  '18'

Parse error at or near `None' instruction at offset -1

    def _compile_module--- This code section failed: ---

 L. 200         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              dirname
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                sourcefilename
               10  CALL_METHOD_1         1  ''
               12  STORE_FAST               'tmpdir'

 L. 201        14  LOAD_GLOBAL              ffiplatform
               16  LOAD_METHOD              compile
               18  LOAD_FAST                'tmpdir'
               20  LOAD_FAST                'self'
               22  LOAD_METHOD              get_extension
               24  CALL_METHOD_0         0  ''
               26  CALL_METHOD_2         2  ''
               28  STORE_FAST               'outputfilename'

 L. 202        30  SETUP_FINALLY        50  'to 50'

 L. 203        32  LOAD_GLOBAL              ffiplatform
               34  LOAD_METHOD              samefile
               36  LOAD_FAST                'outputfilename'
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                modulefilename
               42  CALL_METHOD_2         2  ''
               44  STORE_FAST               'same'
               46  POP_BLOCK        
               48  JUMP_FORWARD         72  'to 72'
             50_0  COME_FROM_FINALLY    30  '30'

 L. 204        50  DUP_TOP          
               52  LOAD_GLOBAL              OSError
               54  <121>                70  ''
               56  POP_TOP          
               58  POP_TOP          
               60  POP_TOP          

 L. 205        62  LOAD_CONST               False
               64  STORE_FAST               'same'
               66  POP_EXCEPT       
               68  JUMP_FORWARD         72  'to 72'
               70  <48>             
             72_0  COME_FROM            68  '68'
             72_1  COME_FROM            48  '48'

 L. 206        72  LOAD_FAST                'same'
               74  POP_JUMP_IF_TRUE    100  'to 100'

 L. 207        76  LOAD_GLOBAL              _ensure_dir
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                modulefilename
               82  CALL_FUNCTION_1       1  ''
               84  POP_TOP          

 L. 208        86  LOAD_GLOBAL              shutil
               88  LOAD_METHOD              move
               90  LOAD_FAST                'outputfilename'
               92  LOAD_FAST                'self'
               94  LOAD_ATTR                modulefilename
               96  CALL_METHOD_2         2  ''
               98  POP_TOP          
            100_0  COME_FROM            74  '74'

 L. 209       100  LOAD_CONST               True
              102  LOAD_FAST                'self'
              104  STORE_ATTR               _has_module

Parse error at or near `<121>' instruction at offset 54

    def _load_library--- This code section failed: ---

 L. 212         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _has_module
                4  POP_JUMP_IF_TRUE     10  'to 10'
                6  <74>             
                8  RAISE_VARARGS_1       1  'exception instance'
             10_0  COME_FROM             4  '4'

 L. 213        10  LOAD_FAST                'self'
               12  LOAD_ATTR                flags
               14  LOAD_CONST               None
               16  <117>                 1  ''
               18  POP_JUMP_IF_FALSE    34  'to 34'

 L. 214        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _vengine
               24  LOAD_METHOD              load_library
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                flags
               30  CALL_METHOD_1         1  ''
               32  RETURN_VALUE     
             34_0  COME_FROM            18  '18'

 L. 216        34  LOAD_FAST                'self'
               36  LOAD_ATTR                _vengine
               38  LOAD_METHOD              load_library
               40  CALL_METHOD_0         0  ''
               42  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1


_FORCE_GENERIC_ENGINE = False

def _locate_engine_class--- This code section failed: ---

 L. 223         0  LOAD_GLOBAL              _FORCE_GENERIC_ENGINE
                2  POP_JUMP_IF_FALSE     8  'to 8'

 L. 224         4  LOAD_CONST               True
                6  STORE_FAST               'force_generic_engine'
              8_0  COME_FROM             2  '2'

 L. 225         8  LOAD_FAST                'force_generic_engine'
               10  POP_JUMP_IF_TRUE     78  'to 78'

 L. 226        12  LOAD_STR                 '__pypy__'
               14  LOAD_GLOBAL              sys
               16  LOAD_ATTR                builtin_module_names
               18  <118>                 0  ''
               20  POP_JUMP_IF_FALSE    28  'to 28'

 L. 227        22  LOAD_CONST               True
               24  STORE_FAST               'force_generic_engine'
               26  JUMP_FORWARD         78  'to 78'
             28_0  COME_FROM            20  '20'

 L. 229        28  SETUP_FINALLY        42  'to 42'

 L. 230        30  LOAD_CONST               0
               32  LOAD_CONST               None
               34  IMPORT_NAME              _cffi_backend
               36  STORE_FAST               '_cffi_backend'
               38  POP_BLOCK        
               40  JUMP_FORWARD         64  'to 64'
             42_0  COME_FROM_FINALLY    28  '28'

 L. 231        42  DUP_TOP          
               44  LOAD_GLOBAL              ImportError
               46  <121>                62  ''
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L. 232        54  LOAD_STR                 '?'
               56  STORE_FAST               '_cffi_backend'
               58  POP_EXCEPT       
               60  JUMP_FORWARD         64  'to 64'
               62  <48>             
             64_0  COME_FROM            60  '60'
             64_1  COME_FROM            40  '40'

 L. 233        64  LOAD_FAST                'ffi'
               66  LOAD_ATTR                _backend
               68  LOAD_FAST                '_cffi_backend'
               70  <117>                 1  ''
               72  POP_JUMP_IF_FALSE    78  'to 78'

 L. 234        74  LOAD_CONST               True
               76  STORE_FAST               'force_generic_engine'
             78_0  COME_FROM            72  '72'
             78_1  COME_FROM            26  '26'
             78_2  COME_FROM            10  '10'

 L. 235        78  LOAD_FAST                'force_generic_engine'
               80  POP_JUMP_IF_FALSE   100  'to 100'

 L. 236        82  LOAD_CONST               1
               84  LOAD_CONST               ('vengine_gen',)
               86  IMPORT_NAME              
               88  IMPORT_FROM              vengine_gen
               90  STORE_FAST               'vengine_gen'
               92  POP_TOP          

 L. 237        94  LOAD_FAST                'vengine_gen'
               96  LOAD_ATTR                VGenericEngine
               98  RETURN_VALUE     
            100_0  COME_FROM            80  '80'

 L. 239       100  LOAD_CONST               1
              102  LOAD_CONST               ('vengine_cpy',)
              104  IMPORT_NAME              
              106  IMPORT_FROM              vengine_cpy
              108  STORE_FAST               'vengine_cpy'
              110  POP_TOP          

 L. 240       112  LOAD_FAST                'vengine_cpy'
              114  LOAD_ATTR                VCPythonEngine
              116  RETURN_VALUE     

Parse error at or near `<118>' instruction at offset 18


_TMPDIR = None

def _caller_dir_pycache():
    global _TMPDIR
    if _TMPDIR:
        return _TMPDIR
    result = os.environ.get('CFFI_TMPDIR')
    if result:
        return result
    filename = sys._getframe(2).f_code.co_filename
    return os.path.abspath(os.path.join(os.path.dirname(filename), '__pycache__'))


def set_tmpdir(dirname):
    """Set the temporary directory to use instead of __pycache__."""
    global _TMPDIR
    _TMPDIR = dirname


def cleanup_tmpdir--- This code section failed: ---

 L. 264         0  LOAD_FAST                'tmpdir'
                2  JUMP_IF_TRUE_OR_POP     8  'to 8'
                4  LOAD_GLOBAL              _caller_dir_pycache
                6  CALL_FUNCTION_0       0  ''
              8_0  COME_FROM             2  '2'
                8  STORE_FAST               'tmpdir'

 L. 265        10  SETUP_FINALLY        26  'to 26'

 L. 266        12  LOAD_GLOBAL              os
               14  LOAD_METHOD              listdir
               16  LOAD_FAST                'tmpdir'
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'filelist'
               22  POP_BLOCK        
               24  JUMP_FORWARD         46  'to 46'
             26_0  COME_FROM_FINALLY    10  '10'

 L. 267        26  DUP_TOP          
               28  LOAD_GLOBAL              OSError
               30  <121>                44  ''
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L. 268        38  POP_EXCEPT       
               40  LOAD_CONST               None
               42  RETURN_VALUE     
               44  <48>             
             46_0  COME_FROM            24  '24'

 L. 269        46  LOAD_FAST                'keep_so'
               48  POP_JUMP_IF_FALSE    56  'to 56'

 L. 270        50  LOAD_STR                 '.c'
               52  STORE_FAST               'suffix'
               54  JUMP_FORWARD         70  'to 70'
             56_0  COME_FROM            48  '48'

 L. 272        56  LOAD_GLOBAL              _get_so_suffixes
               58  CALL_FUNCTION_0       0  ''
               60  LOAD_CONST               0
               62  BINARY_SUBSCR    
               64  LOAD_METHOD              lower
               66  CALL_METHOD_0         0  ''
               68  STORE_FAST               'suffix'
             70_0  COME_FROM            54  '54'

 L. 273        70  LOAD_FAST                'filelist'
               72  GET_ITER         
             74_0  COME_FROM           164  '164'
             74_1  COME_FROM           160  '160'
             74_2  COME_FROM           144  '144'
             74_3  COME_FROM           118  '118'
             74_4  COME_FROM            90  '90'
               74  FOR_ITER            166  'to 166'
               76  STORE_FAST               'fn'

 L. 274        78  LOAD_FAST                'fn'
               80  LOAD_METHOD              lower
               82  CALL_METHOD_0         0  ''
               84  LOAD_METHOD              startswith
               86  LOAD_STR                 '_cffi_'
               88  CALL_METHOD_1         1  ''
               90  POP_JUMP_IF_FALSE_BACK    74  'to 74'

 L. 275        92  LOAD_FAST                'fn'
               94  LOAD_METHOD              lower
               96  CALL_METHOD_0         0  ''
               98  LOAD_METHOD              endswith
              100  LOAD_FAST                'suffix'
              102  CALL_METHOD_1         1  ''

 L. 274       104  POP_JUMP_IF_TRUE    120  'to 120'

 L. 275       106  LOAD_FAST                'fn'
              108  LOAD_METHOD              lower
              110  CALL_METHOD_0         0  ''
              112  LOAD_METHOD              endswith
              114  LOAD_STR                 '.c'
              116  CALL_METHOD_1         1  ''

 L. 274       118  POP_JUMP_IF_FALSE_BACK    74  'to 74'
            120_0  COME_FROM           104  '104'

 L. 276       120  SETUP_FINALLY       146  'to 146'

 L. 277       122  LOAD_GLOBAL              os
              124  LOAD_METHOD              unlink
              126  LOAD_GLOBAL              os
              128  LOAD_ATTR                path
              130  LOAD_METHOD              join
              132  LOAD_FAST                'tmpdir'
              134  LOAD_FAST                'fn'
              136  CALL_METHOD_2         2  ''
              138  CALL_METHOD_1         1  ''
              140  POP_TOP          
              142  POP_BLOCK        
              144  JUMP_BACK            74  'to 74'
            146_0  COME_FROM_FINALLY   120  '120'

 L. 278       146  DUP_TOP          
              148  LOAD_GLOBAL              OSError
              150  <121>               162  ''
              152  POP_TOP          
              154  POP_TOP          
              156  POP_TOP          

 L. 279       158  POP_EXCEPT       
              160  JUMP_BACK            74  'to 74'
              162  <48>             
              164  JUMP_BACK            74  'to 74'
            166_0  COME_FROM            74  '74'

 L. 280       166  LOAD_GLOBAL              os
              168  LOAD_ATTR                path
              170  LOAD_METHOD              join
              172  LOAD_FAST                'tmpdir'
              174  LOAD_STR                 'build'
              176  CALL_METHOD_2         2  ''
              178  BUILD_LIST_1          1 
              180  STORE_FAST               'clean_dir'

 L. 281       182  LOAD_FAST                'clean_dir'
              184  GET_ITER         
            186_0  COME_FROM           280  '280'
            186_1  COME_FROM           276  '276'
            186_2  COME_FROM           258  '258'
              186  FOR_ITER            282  'to 282'
              188  STORE_FAST               'dir'

 L. 282       190  SETUP_FINALLY       260  'to 260'

 L. 283       192  LOAD_GLOBAL              os
              194  LOAD_METHOD              listdir
              196  LOAD_FAST                'dir'
              198  CALL_METHOD_1         1  ''
              200  GET_ITER         
            202_0  COME_FROM           254  '254'
            202_1  COME_FROM           242  '242'
              202  FOR_ITER            256  'to 256'
              204  STORE_FAST               'fn'

 L. 284       206  LOAD_GLOBAL              os
              208  LOAD_ATTR                path
              210  LOAD_METHOD              join
              212  LOAD_FAST                'dir'
              214  LOAD_FAST                'fn'
              216  CALL_METHOD_2         2  ''
              218  STORE_FAST               'fn'

 L. 285       220  LOAD_GLOBAL              os
              222  LOAD_ATTR                path
              224  LOAD_METHOD              isdir
              226  LOAD_FAST                'fn'
              228  CALL_METHOD_1         1  ''
              230  POP_JUMP_IF_FALSE   244  'to 244'

 L. 286       232  LOAD_FAST                'clean_dir'
              234  LOAD_METHOD              append
              236  LOAD_FAST                'fn'
              238  CALL_METHOD_1         1  ''
              240  POP_TOP          
              242  JUMP_BACK           202  'to 202'
            244_0  COME_FROM           230  '230'

 L. 288       244  LOAD_GLOBAL              os
              246  LOAD_METHOD              unlink
              248  LOAD_FAST                'fn'
              250  CALL_METHOD_1         1  ''
              252  POP_TOP          
              254  JUMP_BACK           202  'to 202'
            256_0  COME_FROM           202  '202'
              256  POP_BLOCK        
              258  JUMP_BACK           186  'to 186'
            260_0  COME_FROM_FINALLY   190  '190'

 L. 289       260  DUP_TOP          
              262  LOAD_GLOBAL              OSError
          264_266  <121>               278  ''
              268  POP_TOP          
              270  POP_TOP          
              272  POP_TOP          

 L. 290       274  POP_EXCEPT       
              276  JUMP_BACK           186  'to 186'
              278  <48>             
              280  JUMP_BACK           186  'to 186'
            282_0  COME_FROM           186  '186'

Parse error at or near `<121>' instruction at offset 30


def _get_so_suffixes():
    suffixes = _extension_suffixes()
    if not suffixes:
        if sys.platform == 'win32':
            suffixes = [
             '.pyd']
        else:
            suffixes = [
             '.so']
    return suffixes


def _ensure_dir(filename):
    dirname = os.path.dirname(filename)
    if dirname:
        if not os.path.isdir(dirname):
            os.makedirs(dirname)