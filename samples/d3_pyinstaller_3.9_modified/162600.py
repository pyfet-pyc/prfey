# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: numpy\__config__.py
__all__ = [
 'get_info', 'show']
import os, sys
extra_dll_dir = os.path.join(os.path.dirname(__file__), '.libs')
if sys.platform == 'win32':
    if os.path.isdir(extra_dll_dir):
        if sys.version_info >= (3, 8):
            os.add_dll_directory(extra_dll_dir)
        else:
            os.environ.setdefault('PATH', '')
            os.environ['PATH'] += os.pathsep + extra_dll_dir
blas_mkl_info = {}
blis_info = {}
openblas_info = {'library_dirs':[
  'D:\\a\\1\\s\\numpy\\build\\openblas_info'], 
 'libraries':['openblas_info'],  'language':'f77',  'define_macros':[('HAVE_CBLAS', None)]}
blas_opt_info = {'library_dirs':['D:\\a\\1\\s\\numpy\\build\\openblas_info'],  'libraries':['openblas_info'],  'language':'f77',  'define_macros':[('HAVE_CBLAS', None)]}
lapack_mkl_info = {}
openblas_lapack_info = {'library_dirs':['D:\\a\\1\\s\\numpy\\build\\openblas_lapack_info'],  'libraries':['openblas_lapack_info'],  'language':'f77',  'define_macros':[('HAVE_CBLAS', None)]}
lapack_opt_info = {'library_dirs':['D:\\a\\1\\s\\numpy\\build\\openblas_lapack_info'],  'libraries':['openblas_lapack_info'],  'language':'f77',  'define_macros':[('HAVE_CBLAS', None)]}

def get_info(name):
    g = globals()
    return g.get(name, g.get(name + '_info', {}))


def show--- This code section failed: ---

 L.  69         0  LOAD_GLOBAL              globals
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_METHOD              items
                6  CALL_METHOD_0         0  ''
                8  GET_ITER         
             10_0  COME_FROM           162  '162'
             10_1  COME_FROM            46  '46'
             10_2  COME_FROM            28  '28'
               10  FOR_ITER            164  'to 164'
               12  UNPACK_SEQUENCE_2     2 
               14  STORE_FAST               'name'
               16  STORE_FAST               'info_dict'

 L.  70        18  LOAD_FAST                'name'
               20  LOAD_CONST               0
               22  BINARY_SUBSCR    
               24  LOAD_STR                 '_'
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_TRUE_BACK    10  'to 10'
               30  LOAD_GLOBAL              type
               32  LOAD_FAST                'info_dict'
               34  CALL_FUNCTION_1       1  ''
               36  LOAD_GLOBAL              type
               38  BUILD_MAP_0           0 
               40  CALL_FUNCTION_1       1  ''
               42  <117>                 1  ''
               44  POP_JUMP_IF_FALSE    48  'to 48'
               46  JUMP_BACK            10  'to 10'
             48_0  COME_FROM            44  '44'

 L.  71        48  LOAD_GLOBAL              print
               50  LOAD_FAST                'name'
               52  LOAD_STR                 ':'
               54  BINARY_ADD       
               56  CALL_FUNCTION_1       1  ''
               58  POP_TOP          

 L.  72        60  LOAD_FAST                'info_dict'
               62  POP_JUMP_IF_TRUE     72  'to 72'

 L.  73        64  LOAD_GLOBAL              print
               66  LOAD_STR                 '  NOT AVAILABLE'
               68  CALL_FUNCTION_1       1  ''
               70  POP_TOP          
             72_0  COME_FROM            62  '62'

 L.  74        72  LOAD_FAST                'info_dict'
               74  LOAD_METHOD              items
               76  CALL_METHOD_0         0  ''
               78  GET_ITER         
             80_0  COME_FROM           160  '160'
               80  FOR_ITER            162  'to 162'
               82  UNPACK_SEQUENCE_2     2 
               84  STORE_FAST               'k'
               86  STORE_FAST               'v'

 L.  75        88  LOAD_GLOBAL              str
               90  LOAD_FAST                'v'
               92  CALL_FUNCTION_1       1  ''
               94  STORE_FAST               'v'

 L.  76        96  LOAD_FAST                'k'
               98  LOAD_STR                 'sources'
              100  COMPARE_OP               ==
              102  POP_JUMP_IF_FALSE   144  'to 144'
              104  LOAD_GLOBAL              len
              106  LOAD_FAST                'v'
              108  CALL_FUNCTION_1       1  ''
              110  LOAD_CONST               200
              112  COMPARE_OP               >
              114  POP_JUMP_IF_FALSE   144  'to 144'

 L.  77       116  LOAD_FAST                'v'
              118  LOAD_CONST               None
              120  LOAD_CONST               60
              122  BUILD_SLICE_2         2 
              124  BINARY_SUBSCR    
              126  LOAD_STR                 ' ...\n... '
              128  BINARY_ADD       
              130  LOAD_FAST                'v'
              132  LOAD_CONST               -60
              134  LOAD_CONST               None
              136  BUILD_SLICE_2         2 
              138  BINARY_SUBSCR    
              140  BINARY_ADD       
              142  STORE_FAST               'v'
            144_0  COME_FROM           114  '114'
            144_1  COME_FROM           102  '102'

 L.  78       144  LOAD_GLOBAL              print
              146  LOAD_STR                 '    %s = %s'
              148  LOAD_FAST                'k'
              150  LOAD_FAST                'v'
              152  BUILD_TUPLE_2         2 
              154  BINARY_MODULO    
              156  CALL_FUNCTION_1       1  ''
              158  POP_TOP          
              160  JUMP_BACK            80  'to 80'
            162_0  COME_FROM            80  '80'
              162  JUMP_BACK            10  'to 10'
            164_0  COME_FROM            10  '10'

Parse error at or near `<117>' instruction at offset 42