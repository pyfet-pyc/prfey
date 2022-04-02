# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: runpy.py
"""runpy.py - locating and running Python code using the module namespace

Provides support for locating and running Python scripts using the Python
module namespace instead of the native filesystem.

This allows Python code to play nicely with non-filesystem based PEP 302
importers when locating support scripts as well as when importing modules.
"""
import sys, importlib.machinery, importlib.util, io, types, os
from pkgutil import read_code, get_importer
__all__ = [
 'run_module', 'run_path']

class _TempModule(object):
    __doc__ = 'Temporarily replace a module in sys.modules with an empty namespace'

    def __init__(self, mod_name):
        self.mod_name = mod_name
        self.module = types.ModuleType(mod_name)
        self._saved_module = []

    def __enter__--- This code section failed: ---

 L.  33         0  LOAD_FAST                'self'
                2  LOAD_ATTR                mod_name
                4  STORE_FAST               'mod_name'

 L.  34         6  SETUP_FINALLY        30  'to 30'

 L.  35         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _saved_module
               12  LOAD_METHOD              append
               14  LOAD_GLOBAL              sys
               16  LOAD_ATTR                modules
               18  LOAD_FAST                'mod_name'
               20  BINARY_SUBSCR    
               22  CALL_METHOD_1         1  ''
               24  POP_TOP          
               26  POP_BLOCK        
               28  JUMP_FORWARD         48  'to 48'
             30_0  COME_FROM_FINALLY     6  '6'

 L.  36        30  DUP_TOP          
               32  LOAD_GLOBAL              KeyError
               34  <121>                46  ''
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L.  37        42  POP_EXCEPT       
               44  JUMP_FORWARD         48  'to 48'
               46  <48>             
             48_0  COME_FROM            44  '44'
             48_1  COME_FROM            28  '28'

 L.  38        48  LOAD_FAST                'self'
               50  LOAD_ATTR                module
               52  LOAD_GLOBAL              sys
               54  LOAD_ATTR                modules
               56  LOAD_FAST                'mod_name'
               58  STORE_SUBSCR     

 L.  39        60  LOAD_FAST                'self'
               62  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 34

    def __exit__(self, *args):
        if self._saved_module:
            sys.modules[self.mod_name] = self._saved_module[0]
        else:
            del sys.modules[self.mod_name]
        self._saved_module = []


class _ModifiedArgv0(object):

    def __init__(self, value):
        self.value = value
        self._saved_value = self._sentinel = object()

    def __enter__--- This code section failed: ---

 L.  54         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _saved_value
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _sentinel
                8  <117>                 1  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L.  55        12  LOAD_GLOBAL              RuntimeError
               14  LOAD_STR                 'Already preserving saved value'
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            10  '10'

 L.  56        20  LOAD_GLOBAL              sys
               22  LOAD_ATTR                argv
               24  LOAD_CONST               0
               26  BINARY_SUBSCR    
               28  LOAD_FAST                'self'
               30  STORE_ATTR               _saved_value

 L.  57        32  LOAD_FAST                'self'
               34  LOAD_ATTR                value
               36  LOAD_GLOBAL              sys
               38  LOAD_ATTR                argv
               40  LOAD_CONST               0
               42  STORE_SUBSCR     

Parse error at or near `None' instruction at offset -1

    def __exit__(self, *args):
        self.value = self._sentinel
        sys.argv[0] = self._saved_value


def _run_code--- This code section failed: ---

 L.  68         0  LOAD_FAST                'init_globals'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    18  'to 18'

 L.  69         8  LOAD_FAST                'run_globals'
               10  LOAD_METHOD              update
               12  LOAD_FAST                'init_globals'
               14  CALL_METHOD_1         1  ''
               16  POP_TOP          
             18_0  COME_FROM             6  '6'

 L.  70        18  LOAD_FAST                'mod_spec'
               20  LOAD_CONST               None
               22  <117>                 0  ''
               24  POP_JUMP_IF_FALSE    40  'to 40'

 L.  71        26  LOAD_CONST               None
               28  STORE_FAST               'loader'

 L.  72        30  LOAD_FAST                'script_name'
               32  STORE_FAST               'fname'

 L.  73        34  LOAD_CONST               None
               36  STORE_FAST               'cached'
               38  JUMP_FORWARD         72  'to 72'
             40_0  COME_FROM            24  '24'

 L.  75        40  LOAD_FAST                'mod_spec'
               42  LOAD_ATTR                loader
               44  STORE_FAST               'loader'

 L.  76        46  LOAD_FAST                'mod_spec'
               48  LOAD_ATTR                origin
               50  STORE_FAST               'fname'

 L.  77        52  LOAD_FAST                'mod_spec'
               54  LOAD_ATTR                cached
               56  STORE_FAST               'cached'

 L.  78        58  LOAD_FAST                'pkg_name'
               60  LOAD_CONST               None
               62  <117>                 0  ''
               64  POP_JUMP_IF_FALSE    72  'to 72'

 L.  79        66  LOAD_FAST                'mod_spec'
               68  LOAD_ATTR                parent
               70  STORE_FAST               'pkg_name'
             72_0  COME_FROM            64  '64'
             72_1  COME_FROM            38  '38'

 L.  80        72  LOAD_FAST                'run_globals'
               74  LOAD_ATTR                update
               76  LOAD_FAST                'mod_name'

 L.  81        78  LOAD_FAST                'fname'

 L.  82        80  LOAD_FAST                'cached'

 L.  83        82  LOAD_CONST               None

 L.  84        84  LOAD_FAST                'loader'

 L.  85        86  LOAD_FAST                'pkg_name'

 L.  86        88  LOAD_FAST                'mod_spec'

 L.  80        90  LOAD_CONST               ('__name__', '__file__', '__cached__', '__doc__', '__loader__', '__package__', '__spec__')
               92  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
               94  POP_TOP          

 L.  87        96  LOAD_GLOBAL              exec
               98  LOAD_FAST                'code'
              100  LOAD_FAST                'run_globals'
              102  CALL_FUNCTION_2       2  ''
              104  POP_TOP          

 L.  88       106  LOAD_FAST                'run_globals'
              108  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def _run_module_code--- This code section failed: ---

 L.  94         0  LOAD_FAST                'mod_spec'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'
                8  LOAD_FAST                'script_name'
               10  JUMP_FORWARD         16  'to 16'
             12_0  COME_FROM             6  '6'
               12  LOAD_FAST                'mod_spec'
               14  LOAD_ATTR                origin
             16_0  COME_FROM            10  '10'
               16  STORE_FAST               'fname'

 L.  95        18  LOAD_GLOBAL              _TempModule
               20  LOAD_FAST                'mod_name'
               22  CALL_FUNCTION_1       1  ''
               24  SETUP_WITH          110  'to 110'
               26  STORE_FAST               'temp_module'
               28  LOAD_GLOBAL              _ModifiedArgv0
               30  LOAD_FAST                'fname'
               32  CALL_FUNCTION_1       1  ''
               34  SETUP_WITH           80  'to 80'
               36  POP_TOP          

 L.  96        38  LOAD_FAST                'temp_module'
               40  LOAD_ATTR                module
               42  LOAD_ATTR                __dict__
               44  STORE_FAST               'mod_globals'

 L.  97        46  LOAD_GLOBAL              _run_code
               48  LOAD_FAST                'code'
               50  LOAD_FAST                'mod_globals'
               52  LOAD_FAST                'init_globals'

 L.  98        54  LOAD_FAST                'mod_name'
               56  LOAD_FAST                'mod_spec'
               58  LOAD_FAST                'pkg_name'
               60  LOAD_FAST                'script_name'

 L.  97        62  CALL_FUNCTION_7       7  ''
               64  POP_TOP          
               66  POP_BLOCK        
               68  LOAD_CONST               None
               70  DUP_TOP          
               72  DUP_TOP          
               74  CALL_FUNCTION_3       3  ''
               76  POP_TOP          
               78  JUMP_FORWARD         96  'to 96'
             80_0  COME_FROM_WITH       34  '34'
               80  <49>             
               82  POP_JUMP_IF_TRUE     86  'to 86'
               84  <48>             
             86_0  COME_FROM            82  '82'
               86  POP_TOP          
               88  POP_TOP          
               90  POP_TOP          
               92  POP_EXCEPT       
               94  POP_TOP          
             96_0  COME_FROM            78  '78'
               96  POP_BLOCK        
               98  LOAD_CONST               None
              100  DUP_TOP          
              102  DUP_TOP          
              104  CALL_FUNCTION_3       3  ''
              106  POP_TOP          
              108  JUMP_FORWARD        126  'to 126'
            110_0  COME_FROM_WITH       24  '24'
              110  <49>             
              112  POP_JUMP_IF_TRUE    116  'to 116'
              114  <48>             
            116_0  COME_FROM           112  '112'
              116  POP_TOP          
              118  POP_TOP          
              120  POP_TOP          
              122  POP_EXCEPT       
              124  POP_TOP          
            126_0  COME_FROM           108  '108'

 L. 101       126  LOAD_FAST                'mod_globals'
              128  LOAD_METHOD              copy
              130  CALL_METHOD_0         0  ''
              132  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def _get_module_details--- This code section failed: ---

 L. 105         0  LOAD_FAST                'mod_name'
                2  LOAD_METHOD              startswith
                4  LOAD_STR                 '.'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 106        10  LOAD_FAST                'error'
               12  LOAD_STR                 'Relative module names not supported'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 107        18  LOAD_FAST                'mod_name'
               20  LOAD_METHOD              rpartition
               22  LOAD_STR                 '.'
               24  CALL_METHOD_1         1  ''
               26  UNPACK_SEQUENCE_3     3 
               28  STORE_FAST               'pkg_name'
               30  STORE_FAST               '_'
               32  STORE_FAST               '_'

 L. 108        34  LOAD_FAST                'pkg_name'
               36  POP_JUMP_IF_FALSE   194  'to 194'

 L. 110        38  SETUP_FINALLY        52  'to 52'

 L. 111        40  LOAD_GLOBAL              __import__
               42  LOAD_FAST                'pkg_name'
               44  CALL_FUNCTION_1       1  ''
               46  POP_TOP          
               48  POP_BLOCK        
               50  JUMP_FORWARD        126  'to 126'
             52_0  COME_FROM_FINALLY    38  '38'

 L. 112        52  DUP_TOP          
               54  LOAD_GLOBAL              ImportError
               56  <121>               124  ''
               58  POP_TOP          
               60  STORE_FAST               'e'
               62  POP_TOP          
               64  SETUP_FINALLY       116  'to 116'

 L. 116        66  LOAD_FAST                'e'
               68  LOAD_ATTR                name
               70  LOAD_CONST               None
               72  <117>                 0  ''
               74  POP_JUMP_IF_TRUE    102  'to 102'
               76  LOAD_FAST                'e'
               78  LOAD_ATTR                name
               80  LOAD_FAST                'pkg_name'
               82  COMPARE_OP               !=
               84  POP_JUMP_IF_FALSE   104  'to 104'

 L. 117        86  LOAD_FAST                'pkg_name'
               88  LOAD_METHOD              startswith
               90  LOAD_FAST                'e'
               92  LOAD_ATTR                name
               94  LOAD_STR                 '.'
               96  BINARY_ADD       
               98  CALL_METHOD_1         1  ''

 L. 116       100  POP_JUMP_IF_TRUE    104  'to 104'
            102_0  COME_FROM            74  '74'

 L. 118       102  RAISE_VARARGS_0       0  'reraise'
            104_0  COME_FROM           100  '100'
            104_1  COME_FROM            84  '84'
              104  POP_BLOCK        
              106  POP_EXCEPT       
              108  LOAD_CONST               None
              110  STORE_FAST               'e'
              112  DELETE_FAST              'e'
              114  JUMP_FORWARD        126  'to 126'
            116_0  COME_FROM_FINALLY    64  '64'
              116  LOAD_CONST               None
              118  STORE_FAST               'e'
              120  DELETE_FAST              'e'
              122  <48>             
              124  <48>             
            126_0  COME_FROM           114  '114'
            126_1  COME_FROM            50  '50'

 L. 120       126  LOAD_GLOBAL              sys
              128  LOAD_ATTR                modules
              130  LOAD_METHOD              get
              132  LOAD_FAST                'mod_name'
              134  CALL_METHOD_1         1  ''
              136  STORE_FAST               'existing'

 L. 121       138  LOAD_FAST                'existing'
              140  LOAD_CONST               None
              142  <117>                 1  ''
              144  POP_JUMP_IF_FALSE   194  'to 194'
              146  LOAD_GLOBAL              hasattr
              148  LOAD_FAST                'existing'
              150  LOAD_STR                 '__path__'
              152  CALL_FUNCTION_2       2  ''
              154  POP_JUMP_IF_TRUE    194  'to 194'

 L. 122       156  LOAD_CONST               0
              158  LOAD_CONST               ('warn',)
              160  IMPORT_NAME              warnings
              162  IMPORT_FROM              warn
              164  STORE_FAST               'warn'
              166  POP_TOP          

 L. 123       168  LOAD_STR                 '{mod_name!r} found in sys.modules after import of package {pkg_name!r}, but prior to execution of {mod_name!r}; this may result in unpredictable behaviour'
              170  LOAD_ATTR                format

 L. 126       172  LOAD_FAST                'mod_name'
              174  LOAD_FAST                'pkg_name'

 L. 123       176  LOAD_CONST               ('mod_name', 'pkg_name')
              178  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              180  STORE_FAST               'msg'

 L. 127       182  LOAD_FAST                'warn'
              184  LOAD_GLOBAL              RuntimeWarning
              186  LOAD_FAST                'msg'
              188  CALL_FUNCTION_1       1  ''
              190  CALL_FUNCTION_1       1  ''
              192  POP_TOP          
            194_0  COME_FROM           154  '154'
            194_1  COME_FROM           144  '144'
            194_2  COME_FROM            36  '36'

 L. 129       194  SETUP_FINALLY       212  'to 212'

 L. 130       196  LOAD_GLOBAL              importlib
              198  LOAD_ATTR                util
              200  LOAD_METHOD              find_spec
              202  LOAD_FAST                'mod_name'
              204  CALL_METHOD_1         1  ''
              206  STORE_FAST               'spec'
              208  POP_BLOCK        
              210  JUMP_FORWARD        330  'to 330'
            212_0  COME_FROM_FINALLY   194  '194'

 L. 131       212  DUP_TOP          
              214  LOAD_GLOBAL              ImportError
              216  LOAD_GLOBAL              AttributeError
              218  LOAD_GLOBAL              TypeError
              220  LOAD_GLOBAL              ValueError
              222  BUILD_TUPLE_4         4 
          224_226  <121>               328  ''
              228  POP_TOP          
              230  STORE_FAST               'ex'
              232  POP_TOP          
              234  SETUP_FINALLY       320  'to 320'

 L. 135       236  LOAD_STR                 'Error while finding module specification for {!r} ({}: {})'
              238  STORE_FAST               'msg'

 L. 136       240  LOAD_FAST                'mod_name'
              242  LOAD_METHOD              endswith
              244  LOAD_STR                 '.py'
              246  CALL_METHOD_1         1  ''
          248_250  POP_JUMP_IF_FALSE   282  'to 282'

 L. 137       252  LOAD_FAST                'msg'
              254  LOAD_STR                 ". Try using '"
              256  LOAD_FAST                'mod_name'
              258  LOAD_CONST               None
              260  LOAD_CONST               -3
              262  BUILD_SLICE_2         2 
              264  BINARY_SUBSCR    
              266  FORMAT_VALUE          0  ''
              268  LOAD_STR                 "' instead of '"

 L. 138       270  LOAD_FAST                'mod_name'

 L. 137       272  FORMAT_VALUE          0  ''
              274  LOAD_STR                 "' as the module name."
              276  BUILD_STRING_5        5 
              278  INPLACE_ADD      
              280  STORE_FAST               'msg'
            282_0  COME_FROM           248  '248'

 L. 139       282  LOAD_FAST                'error'
              284  LOAD_FAST                'msg'
              286  LOAD_METHOD              format
              288  LOAD_FAST                'mod_name'
              290  LOAD_GLOBAL              type
              292  LOAD_FAST                'ex'
              294  CALL_FUNCTION_1       1  ''
              296  LOAD_ATTR                __name__
              298  LOAD_FAST                'ex'
              300  CALL_METHOD_3         3  ''
              302  CALL_FUNCTION_1       1  ''
              304  LOAD_FAST                'ex'
              306  RAISE_VARARGS_2       2  'exception instance with __cause__'
              308  POP_BLOCK        
              310  POP_EXCEPT       
              312  LOAD_CONST               None
              314  STORE_FAST               'ex'
              316  DELETE_FAST              'ex'
              318  JUMP_FORWARD        330  'to 330'
            320_0  COME_FROM_FINALLY   234  '234'
              320  LOAD_CONST               None
              322  STORE_FAST               'ex'
              324  DELETE_FAST              'ex'
              326  <48>             
              328  <48>             
            330_0  COME_FROM           318  '318'
            330_1  COME_FROM           210  '210'

 L. 140       330  LOAD_FAST                'spec'
              332  LOAD_CONST               None
              334  <117>                 0  ''
          336_338  POP_JUMP_IF_FALSE   352  'to 352'

 L. 141       340  LOAD_FAST                'error'
              342  LOAD_STR                 'No module named %s'
              344  LOAD_FAST                'mod_name'
              346  BINARY_MODULO    
              348  CALL_FUNCTION_1       1  ''
              350  RAISE_VARARGS_1       1  'exception instance'
            352_0  COME_FROM           336  '336'

 L. 142       352  LOAD_FAST                'spec'
              354  LOAD_ATTR                submodule_search_locations
              356  LOAD_CONST               None
              358  <117>                 1  ''
          360_362  POP_JUMP_IF_FALSE   484  'to 484'

 L. 143       364  LOAD_FAST                'mod_name'
              366  LOAD_STR                 '__main__'
              368  COMPARE_OP               ==
          370_372  POP_JUMP_IF_TRUE    386  'to 386'
              374  LOAD_FAST                'mod_name'
              376  LOAD_METHOD              endswith
              378  LOAD_STR                 '.__main__'
              380  CALL_METHOD_1         1  ''
          382_384  POP_JUMP_IF_FALSE   394  'to 394'
            386_0  COME_FROM           370  '370'

 L. 144       386  LOAD_FAST                'error'
              388  LOAD_STR                 'Cannot use package as __main__ module'
              390  CALL_FUNCTION_1       1  ''
              392  RAISE_VARARGS_1       1  'exception instance'
            394_0  COME_FROM           382  '382'

 L. 145       394  SETUP_FINALLY       416  'to 416'

 L. 146       396  LOAD_FAST                'mod_name'
              398  LOAD_STR                 '.__main__'
              400  BINARY_ADD       
              402  STORE_FAST               'pkg_main_name'

 L. 147       404  LOAD_GLOBAL              _get_module_details
              406  LOAD_FAST                'pkg_main_name'
              408  LOAD_FAST                'error'
              410  CALL_FUNCTION_2       2  ''
              412  POP_BLOCK        
              414  RETURN_VALUE     
            416_0  COME_FROM_FINALLY   394  '394'

 L. 148       416  DUP_TOP          
              418  LOAD_FAST                'error'
          420_422  <121>               482  ''
              424  POP_TOP          
              426  STORE_FAST               'e'
              428  POP_TOP          
              430  SETUP_FINALLY       474  'to 474'

 L. 149       432  LOAD_FAST                'mod_name'
              434  LOAD_GLOBAL              sys
              436  LOAD_ATTR                modules
              438  <118>                 1  ''
          440_442  POP_JUMP_IF_FALSE   446  'to 446'

 L. 150       444  RAISE_VARARGS_0       0  'reraise'
            446_0  COME_FROM           440  '440'

 L. 151       446  LOAD_FAST                'error'
              448  LOAD_STR                 '%s; %r is a package and cannot be directly executed'

 L. 152       450  LOAD_FAST                'e'
              452  LOAD_FAST                'mod_name'
              454  BUILD_TUPLE_2         2 

 L. 151       456  BINARY_MODULO    
              458  CALL_FUNCTION_1       1  ''
              460  RAISE_VARARGS_1       1  'exception instance'
              462  POP_BLOCK        
              464  POP_EXCEPT       
              466  LOAD_CONST               None
              468  STORE_FAST               'e'
              470  DELETE_FAST              'e'
              472  JUMP_FORWARD        484  'to 484'
            474_0  COME_FROM_FINALLY   430  '430'
              474  LOAD_CONST               None
              476  STORE_FAST               'e'
              478  DELETE_FAST              'e'
              480  <48>             
              482  <48>             
            484_0  COME_FROM           472  '472'
            484_1  COME_FROM           360  '360'

 L. 153       484  LOAD_FAST                'spec'
              486  LOAD_ATTR                loader
              488  STORE_FAST               'loader'

 L. 154       490  LOAD_FAST                'loader'
              492  LOAD_CONST               None
              494  <117>                 0  ''
          496_498  POP_JUMP_IF_FALSE   512  'to 512'

 L. 155       500  LOAD_FAST                'error'
              502  LOAD_STR                 '%r is a namespace package and cannot be executed'

 L. 156       504  LOAD_FAST                'mod_name'

 L. 155       506  BINARY_MODULO    
              508  CALL_FUNCTION_1       1  ''
              510  RAISE_VARARGS_1       1  'exception instance'
            512_0  COME_FROM           496  '496'

 L. 157       512  SETUP_FINALLY       528  'to 528'

 L. 158       514  LOAD_FAST                'loader'
              516  LOAD_METHOD              get_code
              518  LOAD_FAST                'mod_name'
              520  CALL_METHOD_1         1  ''
              522  STORE_FAST               'code'
              524  POP_BLOCK        
              526  JUMP_FORWARD        580  'to 580'
            528_0  COME_FROM_FINALLY   512  '512'

 L. 159       528  DUP_TOP          
              530  LOAD_GLOBAL              ImportError
          532_534  <121>               578  ''
              536  POP_TOP          
              538  STORE_FAST               'e'
              540  POP_TOP          
              542  SETUP_FINALLY       570  'to 570'

 L. 160       544  LOAD_FAST                'error'
              546  LOAD_GLOBAL              format
              548  LOAD_FAST                'e'
              550  CALL_FUNCTION_1       1  ''
              552  CALL_FUNCTION_1       1  ''
              554  LOAD_FAST                'e'
              556  RAISE_VARARGS_2       2  'exception instance with __cause__'
              558  POP_BLOCK        
              560  POP_EXCEPT       
              562  LOAD_CONST               None
              564  STORE_FAST               'e'
              566  DELETE_FAST              'e'
              568  JUMP_FORWARD        580  'to 580'
            570_0  COME_FROM_FINALLY   542  '542'
              570  LOAD_CONST               None
              572  STORE_FAST               'e'
              574  DELETE_FAST              'e'
              576  <48>             
              578  <48>             
            580_0  COME_FROM           568  '568'
            580_1  COME_FROM           526  '526'

 L. 161       580  LOAD_FAST                'code'
              582  LOAD_CONST               None
              584  <117>                 0  ''
          586_588  POP_JUMP_IF_FALSE   602  'to 602'

 L. 162       590  LOAD_FAST                'error'
              592  LOAD_STR                 'No code object available for %s'
              594  LOAD_FAST                'mod_name'
              596  BINARY_MODULO    
              598  CALL_FUNCTION_1       1  ''
              600  RAISE_VARARGS_1       1  'exception instance'
            602_0  COME_FROM           586  '586'

 L. 163       602  LOAD_FAST                'mod_name'
              604  LOAD_FAST                'spec'
              606  LOAD_FAST                'code'
              608  BUILD_TUPLE_3         3 
              610  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 56


class _Error(Exception):
    __doc__ = 'Error that _run_module_as_main() should report without a traceback'


def _run_module_as_main--- This code section failed: ---

 L. 186         0  SETUP_FINALLY        50  'to 50'

 L. 187         2  LOAD_FAST                'alter_argv'
                4  POP_JUMP_IF_TRUE     14  'to 14'
                6  LOAD_FAST                'mod_name'
                8  LOAD_STR                 '__main__'
               10  COMPARE_OP               !=
               12  POP_JUMP_IF_FALSE    32  'to 32'
             14_0  COME_FROM             4  '4'

 L. 188        14  LOAD_GLOBAL              _get_module_details
               16  LOAD_FAST                'mod_name'
               18  LOAD_GLOBAL              _Error
               20  CALL_FUNCTION_2       2  ''
               22  UNPACK_SEQUENCE_3     3 
               24  STORE_FAST               'mod_name'
               26  STORE_FAST               'mod_spec'
               28  STORE_FAST               'code'
               30  JUMP_FORWARD         46  'to 46'
             32_0  COME_FROM            12  '12'

 L. 190        32  LOAD_GLOBAL              _get_main_module_details
               34  LOAD_GLOBAL              _Error
               36  CALL_FUNCTION_1       1  ''
               38  UNPACK_SEQUENCE_3     3 
               40  STORE_FAST               'mod_name'
               42  STORE_FAST               'mod_spec'
               44  STORE_FAST               'code'
             46_0  COME_FROM            30  '30'
               46  POP_BLOCK        
               48  JUMP_FORWARD        110  'to 110'
             50_0  COME_FROM_FINALLY     0  '0'

 L. 191        50  DUP_TOP          
               52  LOAD_GLOBAL              _Error
               54  <121>               108  ''
               56  POP_TOP          
               58  STORE_FAST               'exc'
               60  POP_TOP          
               62  SETUP_FINALLY       100  'to 100'

 L. 192        64  LOAD_STR                 '%s: %s'
               66  LOAD_GLOBAL              sys
               68  LOAD_ATTR                executable
               70  LOAD_FAST                'exc'
               72  BUILD_TUPLE_2         2 
               74  BINARY_MODULO    
               76  STORE_FAST               'msg'

 L. 193        78  LOAD_GLOBAL              sys
               80  LOAD_METHOD              exit
               82  LOAD_FAST                'msg'
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          
               88  POP_BLOCK        
               90  POP_EXCEPT       
               92  LOAD_CONST               None
               94  STORE_FAST               'exc'
               96  DELETE_FAST              'exc'
               98  JUMP_FORWARD        110  'to 110'
            100_0  COME_FROM_FINALLY    62  '62'
              100  LOAD_CONST               None
              102  STORE_FAST               'exc'
              104  DELETE_FAST              'exc'
              106  <48>             
              108  <48>             
            110_0  COME_FROM            98  '98'
            110_1  COME_FROM            48  '48'

 L. 194       110  LOAD_GLOBAL              sys
              112  LOAD_ATTR                modules
              114  LOAD_STR                 '__main__'
              116  BINARY_SUBSCR    
              118  LOAD_ATTR                __dict__
              120  STORE_FAST               'main_globals'

 L. 195       122  LOAD_FAST                'alter_argv'
              124  POP_JUMP_IF_FALSE   138  'to 138'

 L. 196       126  LOAD_FAST                'mod_spec'
              128  LOAD_ATTR                origin
              130  LOAD_GLOBAL              sys
              132  LOAD_ATTR                argv
              134  LOAD_CONST               0
              136  STORE_SUBSCR     
            138_0  COME_FROM           124  '124'

 L. 197       138  LOAD_GLOBAL              _run_code
              140  LOAD_FAST                'code'
              142  LOAD_FAST                'main_globals'
              144  LOAD_CONST               None

 L. 198       146  LOAD_STR                 '__main__'
              148  LOAD_FAST                'mod_spec'

 L. 197       150  CALL_FUNCTION_5       5  ''
              152  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 54


def run_module--- This code section failed: ---

 L. 206         0  LOAD_GLOBAL              _get_module_details
                2  LOAD_FAST                'mod_name'
                4  CALL_FUNCTION_1       1  ''
                6  UNPACK_SEQUENCE_3     3 
                8  STORE_FAST               'mod_name'
               10  STORE_FAST               'mod_spec'
               12  STORE_FAST               'code'

 L. 207        14  LOAD_FAST                'run_name'
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_FALSE    26  'to 26'

 L. 208        22  LOAD_FAST                'mod_name'
               24  STORE_FAST               'run_name'
             26_0  COME_FROM            20  '20'

 L. 209        26  LOAD_FAST                'alter_sys'
               28  POP_JUMP_IF_FALSE    44  'to 44'

 L. 210        30  LOAD_GLOBAL              _run_module_code
               32  LOAD_FAST                'code'
               34  LOAD_FAST                'init_globals'
               36  LOAD_FAST                'run_name'
               38  LOAD_FAST                'mod_spec'
               40  CALL_FUNCTION_4       4  ''
               42  RETURN_VALUE     
             44_0  COME_FROM            28  '28'

 L. 213        44  LOAD_GLOBAL              _run_code
               46  LOAD_FAST                'code'
               48  BUILD_MAP_0           0 
               50  LOAD_FAST                'init_globals'
               52  LOAD_FAST                'run_name'
               54  LOAD_FAST                'mod_spec'
               56  CALL_FUNCTION_5       5  ''
               58  RETURN_VALUE     

Parse error at or near `<117>' instruction at offset 18


def _get_main_module_details--- This code section failed: ---

 L. 220         0  LOAD_STR                 '__main__'
                2  STORE_FAST               'main_name'

 L. 221         4  LOAD_GLOBAL              sys
                6  LOAD_ATTR                modules
                8  LOAD_FAST                'main_name'
               10  BINARY_SUBSCR    
               12  STORE_FAST               'saved_main'

 L. 222        14  LOAD_GLOBAL              sys
               16  LOAD_ATTR                modules
               18  LOAD_FAST                'main_name'
               20  DELETE_SUBSCR    

 L. 223        22  SETUP_FINALLY       136  'to 136'
               24  SETUP_FINALLY        48  'to 48'

 L. 224        26  LOAD_GLOBAL              _get_module_details
               28  LOAD_FAST                'main_name'
               30  CALL_FUNCTION_1       1  ''
               32  POP_BLOCK        
               34  POP_BLOCK        

 L. 231        36  LOAD_FAST                'saved_main'
               38  LOAD_GLOBAL              sys
               40  LOAD_ATTR                modules
               42  LOAD_FAST                'main_name'
               44  STORE_SUBSCR     

 L. 224        46  RETURN_VALUE     
             48_0  COME_FROM_FINALLY    24  '24'

 L. 225        48  DUP_TOP          
               50  LOAD_GLOBAL              ImportError
               52  <121>               120  ''
               54  POP_TOP          
               56  STORE_FAST               'exc'
               58  POP_TOP          
               60  SETUP_FINALLY       112  'to 112'

 L. 226        62  LOAD_FAST                'main_name'
               64  LOAD_GLOBAL              str
               66  LOAD_FAST                'exc'
               68  CALL_FUNCTION_1       1  ''
               70  <118>                 0  ''
               72  POP_JUMP_IF_FALSE    98  'to 98'

 L. 227        74  LOAD_FAST                'error'
               76  LOAD_STR                 "can't find %r module in %r"

 L. 228        78  LOAD_FAST                'main_name'
               80  LOAD_GLOBAL              sys
               82  LOAD_ATTR                path
               84  LOAD_CONST               0
               86  BINARY_SUBSCR    
               88  BUILD_TUPLE_2         2 

 L. 227        90  BINARY_MODULO    
               92  CALL_FUNCTION_1       1  ''

 L. 228        94  LOAD_FAST                'exc'

 L. 227        96  RAISE_VARARGS_2       2  'exception instance with __cause__'
             98_0  COME_FROM            72  '72'

 L. 229        98  RAISE_VARARGS_0       0  'reraise'
              100  POP_BLOCK        
              102  POP_EXCEPT       
              104  LOAD_CONST               None
              106  STORE_FAST               'exc'
              108  DELETE_FAST              'exc'
              110  JUMP_FORWARD        122  'to 122'
            112_0  COME_FROM_FINALLY    60  '60'
              112  LOAD_CONST               None
              114  STORE_FAST               'exc'
              116  DELETE_FAST              'exc'
              118  <48>             
              120  <48>             
            122_0  COME_FROM           110  '110'
              122  POP_BLOCK        

 L. 231       124  LOAD_FAST                'saved_main'
              126  LOAD_GLOBAL              sys
              128  LOAD_ATTR                modules
              130  LOAD_FAST                'main_name'
              132  STORE_SUBSCR     
              134  JUMP_FORWARD        148  'to 148'
            136_0  COME_FROM_FINALLY    22  '22'
              136  LOAD_FAST                'saved_main'
              138  LOAD_GLOBAL              sys
              140  LOAD_ATTR                modules
              142  LOAD_FAST                'main_name'
              144  STORE_SUBSCR     
              146  <48>             
            148_0  COME_FROM           134  '134'

Parse error at or near `POP_BLOCK' instruction at offset 34


def _get_code_from_file--- This code section failed: ---

 L. 236         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              abspath
                6  LOAD_GLOBAL              os
                8  LOAD_METHOD              fsdecode
               10  LOAD_FAST                'fname'
               12  CALL_METHOD_1         1  ''
               14  CALL_METHOD_1         1  ''
               16  STORE_FAST               'decoded_path'

 L. 237        18  LOAD_GLOBAL              io
               20  LOAD_METHOD              open_code
               22  LOAD_FAST                'decoded_path'
               24  CALL_METHOD_1         1  ''
               26  SETUP_WITH           52  'to 52'
               28  STORE_FAST               'f'

 L. 238        30  LOAD_GLOBAL              read_code
               32  LOAD_FAST                'f'
               34  CALL_FUNCTION_1       1  ''
               36  STORE_FAST               'code'
               38  POP_BLOCK        
               40  LOAD_CONST               None
               42  DUP_TOP          
               44  DUP_TOP          
               46  CALL_FUNCTION_3       3  ''
               48  POP_TOP          
               50  JUMP_FORWARD         68  'to 68'
             52_0  COME_FROM_WITH       26  '26'
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

 L. 239        68  LOAD_FAST                'code'
               70  LOAD_CONST               None
               72  <117>                 0  ''
               74  POP_JUMP_IF_FALSE   134  'to 134'

 L. 241        76  LOAD_GLOBAL              io
               78  LOAD_METHOD              open_code
               80  LOAD_FAST                'decoded_path'
               82  CALL_METHOD_1         1  ''
               84  SETUP_WITH          118  'to 118'
               86  STORE_FAST               'f'

 L. 242        88  LOAD_GLOBAL              compile
               90  LOAD_FAST                'f'
               92  LOAD_METHOD              read
               94  CALL_METHOD_0         0  ''
               96  LOAD_FAST                'fname'
               98  LOAD_STR                 'exec'
              100  CALL_FUNCTION_3       3  ''
              102  STORE_FAST               'code'
              104  POP_BLOCK        
              106  LOAD_CONST               None
              108  DUP_TOP          
              110  DUP_TOP          
              112  CALL_FUNCTION_3       3  ''
              114  POP_TOP          
              116  JUMP_FORWARD        134  'to 134'
            118_0  COME_FROM_WITH       84  '84'
              118  <49>             
              120  POP_JUMP_IF_TRUE    124  'to 124'
              122  <48>             
            124_0  COME_FROM           120  '120'
              124  POP_TOP          
              126  POP_TOP          
              128  POP_TOP          
              130  POP_EXCEPT       
              132  POP_TOP          
            134_0  COME_FROM           116  '116'
            134_1  COME_FROM            74  '74'

 L. 243       134  LOAD_FAST                'code'
              136  LOAD_FAST                'fname'
              138  BUILD_TUPLE_2         2 
              140  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 42


def run_path--- This code section failed: ---

 L. 255         0  LOAD_FAST                'run_name'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 256         8  LOAD_STR                 '<run_path>'
               10  STORE_FAST               'run_name'
             12_0  COME_FROM             6  '6'

 L. 257        12  LOAD_FAST                'run_name'
               14  LOAD_METHOD              rpartition
               16  LOAD_STR                 '.'
               18  CALL_METHOD_1         1  ''
               20  LOAD_CONST               0
               22  BINARY_SUBSCR    
               24  STORE_FAST               'pkg_name'

 L. 258        26  LOAD_GLOBAL              get_importer
               28  LOAD_FAST                'path_name'
               30  CALL_FUNCTION_1       1  ''
               32  STORE_FAST               'importer'

 L. 260        34  LOAD_CONST               False
               36  STORE_FAST               'is_NullImporter'

 L. 261        38  LOAD_GLOBAL              type
               40  LOAD_FAST                'importer'
               42  CALL_FUNCTION_1       1  ''
               44  LOAD_ATTR                __module__
               46  LOAD_STR                 'imp'
               48  COMPARE_OP               ==
               50  POP_JUMP_IF_FALSE    70  'to 70'

 L. 262        52  LOAD_GLOBAL              type
               54  LOAD_FAST                'importer'
               56  CALL_FUNCTION_1       1  ''
               58  LOAD_ATTR                __name__
               60  LOAD_STR                 'NullImporter'
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_FALSE    70  'to 70'

 L. 263        66  LOAD_CONST               True
               68  STORE_FAST               'is_NullImporter'
             70_0  COME_FROM            64  '64'
             70_1  COME_FROM            50  '50'

 L. 264        70  LOAD_GLOBAL              isinstance
               72  LOAD_FAST                'importer'
               74  LOAD_GLOBAL              type
               76  LOAD_CONST               None
               78  CALL_FUNCTION_1       1  ''
               80  CALL_FUNCTION_2       2  ''
               82  POP_JUMP_IF_TRUE     88  'to 88'
               84  LOAD_FAST                'is_NullImporter'
               86  POP_JUMP_IF_FALSE   120  'to 120'
             88_0  COME_FROM            82  '82'

 L. 267        88  LOAD_GLOBAL              _get_code_from_file
               90  LOAD_FAST                'run_name'
               92  LOAD_FAST                'path_name'
               94  CALL_FUNCTION_2       2  ''
               96  UNPACK_SEQUENCE_2     2 
               98  STORE_FAST               'code'
              100  STORE_FAST               'fname'

 L. 268       102  LOAD_GLOBAL              _run_module_code
              104  LOAD_FAST                'code'
              106  LOAD_FAST                'init_globals'
              108  LOAD_FAST                'run_name'

 L. 269       110  LOAD_FAST                'pkg_name'
              112  LOAD_FAST                'fname'

 L. 268       114  LOAD_CONST               ('pkg_name', 'script_name')
              116  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              118  RETURN_VALUE     
            120_0  COME_FROM            86  '86'

 L. 273       120  LOAD_GLOBAL              sys
              122  LOAD_ATTR                path
              124  LOAD_METHOD              insert
              126  LOAD_CONST               0
              128  LOAD_FAST                'path_name'
              130  CALL_METHOD_2         2  ''
              132  POP_TOP          

 L. 274       134  SETUP_FINALLY       358  'to 358'

 L. 281       136  LOAD_GLOBAL              _get_main_module_details
              138  CALL_FUNCTION_0       0  ''
              140  UNPACK_SEQUENCE_3     3 
              142  STORE_FAST               'mod_name'
              144  STORE_FAST               'mod_spec'
              146  STORE_FAST               'code'

 L. 282       148  LOAD_GLOBAL              _TempModule
              150  LOAD_FAST                'run_name'
              152  CALL_FUNCTION_1       1  ''
              154  SETUP_WITH          298  'to 298'
              156  STORE_FAST               'temp_module'

 L. 283       158  LOAD_GLOBAL              _ModifiedArgv0
              160  LOAD_FAST                'path_name'
              162  CALL_FUNCTION_1       1  ''

 L. 282       164  SETUP_WITH          266  'to 266'
              166  POP_TOP          

 L. 284       168  LOAD_FAST                'temp_module'
              170  LOAD_ATTR                module
              172  LOAD_ATTR                __dict__
              174  STORE_FAST               'mod_globals'

 L. 285       176  LOAD_GLOBAL              _run_code
              178  LOAD_FAST                'code'
              180  LOAD_FAST                'mod_globals'
              182  LOAD_FAST                'init_globals'

 L. 286       184  LOAD_FAST                'run_name'
              186  LOAD_FAST                'mod_spec'
              188  LOAD_FAST                'pkg_name'

 L. 285       190  CALL_FUNCTION_6       6  ''
              192  LOAD_METHOD              copy
              194  CALL_METHOD_0         0  ''
              196  POP_BLOCK        
              198  ROT_TWO          
              200  LOAD_CONST               None
              202  DUP_TOP          
              204  DUP_TOP          
              206  CALL_FUNCTION_3       3  ''
              208  POP_TOP          
              210  POP_BLOCK        
              212  ROT_TWO          
              214  LOAD_CONST               None
              216  DUP_TOP          
              218  DUP_TOP          
              220  CALL_FUNCTION_3       3  ''
              222  POP_TOP          
              224  POP_BLOCK        

 L. 288       226  SETUP_FINALLY       244  'to 244'

 L. 289       228  LOAD_GLOBAL              sys
              230  LOAD_ATTR                path
              232  LOAD_METHOD              remove
              234  LOAD_FAST                'path_name'
              236  CALL_METHOD_1         1  ''
              238  POP_TOP          
              240  POP_BLOCK        
              242  RETURN_VALUE     
            244_0  COME_FROM_FINALLY   226  '226'

 L. 290       244  DUP_TOP          
              246  LOAD_GLOBAL              ValueError
          248_250  <121>               262  ''
              252  POP_TOP          
              254  POP_TOP          
              256  POP_TOP          

 L. 291       258  POP_EXCEPT       
              260  RETURN_VALUE     
              262  <48>             

 L. 285       264  RETURN_VALUE     
            266_0  COME_FROM_WITH      164  '164'
              266  <49>             
          268_270  POP_JUMP_IF_TRUE    274  'to 274'
              272  <48>             
            274_0  COME_FROM           268  '268'
              274  POP_TOP          
              276  POP_TOP          
              278  POP_TOP          
              280  POP_EXCEPT       
              282  POP_TOP          
              284  POP_BLOCK        
              286  LOAD_CONST               None
              288  DUP_TOP          
              290  DUP_TOP          
              292  CALL_FUNCTION_3       3  ''
              294  POP_TOP          
              296  JUMP_FORWARD        316  'to 316'
            298_0  COME_FROM_WITH      154  '154'
              298  <49>             
          300_302  POP_JUMP_IF_TRUE    306  'to 306'
              304  <48>             
            306_0  COME_FROM           300  '300'
              306  POP_TOP          
              308  POP_TOP          
              310  POP_TOP          
              312  POP_EXCEPT       
              314  POP_TOP          
            316_0  COME_FROM           296  '296'
              316  POP_BLOCK        

 L. 288       318  SETUP_FINALLY       336  'to 336'

 L. 289       320  LOAD_GLOBAL              sys
              322  LOAD_ATTR                path
              324  LOAD_METHOD              remove
              326  LOAD_FAST                'path_name'
              328  CALL_METHOD_1         1  ''
              330  POP_TOP          
              332  POP_BLOCK        
              334  JUMP_FORWARD        356  'to 356'
            336_0  COME_FROM_FINALLY   318  '318'

 L. 290       336  DUP_TOP          
              338  LOAD_GLOBAL              ValueError
          340_342  <121>               354  ''
              344  POP_TOP          
              346  POP_TOP          
              348  POP_TOP          

 L. 291       350  POP_EXCEPT       
              352  JUMP_FORWARD        356  'to 356'
              354  <48>             
            356_0  COME_FROM           352  '352'
            356_1  COME_FROM           334  '334'
              356  JUMP_FORWARD        398  'to 398'
            358_0  COME_FROM_FINALLY   134  '134'

 L. 288       358  SETUP_FINALLY       376  'to 376'

 L. 289       360  LOAD_GLOBAL              sys
              362  LOAD_ATTR                path
              364  LOAD_METHOD              remove
              366  LOAD_FAST                'path_name'
              368  CALL_METHOD_1         1  ''
              370  POP_TOP          
              372  POP_BLOCK        
              374  JUMP_FORWARD        396  'to 396'
            376_0  COME_FROM_FINALLY   358  '358'

 L. 290       376  DUP_TOP          
              378  LOAD_GLOBAL              ValueError
          380_382  <121>               394  ''
              384  POP_TOP          
              386  POP_TOP          
              388  POP_TOP          

 L. 291       390  POP_EXCEPT       
              392  JUMP_FORWARD        396  'to 396'
              394  <48>             
            396_0  COME_FROM           392  '392'
            396_1  COME_FROM           374  '374'
              396  <48>             
            398_0  COME_FROM           356  '356'

Parse error at or near `None' instruction at offset -1


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('No module specified for execution', file=(sys.stderr))
    else:
        del sys.argv[0]
        _run_module_as_main(sys.argv[0])