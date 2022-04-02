# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: multiprocessing\popen_forkserver.py
import io, os
from .context import reduction, set_spawning_popen
if not reduction.HAVE_SEND_HANDLE:
    raise ImportError('No support for sending fds between processes')
from . import forkserver
from . import popen_fork
from . import spawn
from . import util
__all__ = [
 'Popen']

class _DupFd(object):

    def __init__(self, ind):
        self.ind = ind

    def detach(self):
        return forkserver.get_inherited_fds()[self.ind]


class Popen(popen_fork.Popen):
    method = 'forkserver'
    DupFd = _DupFd

    def __init__(self, process_obj):
        self._fds = []
        super().__init__(process_obj)

    def duplicate_for_child(self, fd):
        self._fds.append(fd)
        return len(self._fds) - 1

    def _launch--- This code section failed: ---

 L.  42         0  LOAD_GLOBAL              spawn
                2  LOAD_METHOD              get_preparation_data
                4  LOAD_FAST                'process_obj'
                6  LOAD_ATTR                _name
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'prep_data'

 L.  43        12  LOAD_GLOBAL              io
               14  LOAD_METHOD              BytesIO
               16  CALL_METHOD_0         0  ''
               18  STORE_FAST               'buf'

 L.  44        20  LOAD_GLOBAL              set_spawning_popen
               22  LOAD_FAST                'self'
               24  CALL_FUNCTION_1       1  ''
               26  POP_TOP          

 L.  45        28  SETUP_FINALLY        66  'to 66'

 L.  46        30  LOAD_GLOBAL              reduction
               32  LOAD_METHOD              dump
               34  LOAD_FAST                'prep_data'
               36  LOAD_FAST                'buf'
               38  CALL_METHOD_2         2  ''
               40  POP_TOP          

 L.  47        42  LOAD_GLOBAL              reduction
               44  LOAD_METHOD              dump
               46  LOAD_FAST                'process_obj'
               48  LOAD_FAST                'buf'
               50  CALL_METHOD_2         2  ''
               52  POP_TOP          
               54  POP_BLOCK        

 L.  49        56  LOAD_GLOBAL              set_spawning_popen
               58  LOAD_CONST               None
               60  CALL_FUNCTION_1       1  ''
               62  POP_TOP          
               64  JUMP_FORWARD         76  'to 76'
             66_0  COME_FROM_FINALLY    28  '28'
               66  LOAD_GLOBAL              set_spawning_popen
               68  LOAD_CONST               None
               70  CALL_FUNCTION_1       1  ''
               72  POP_TOP          
               74  <48>             
             76_0  COME_FROM            64  '64'

 L.  51        76  LOAD_GLOBAL              forkserver
               78  LOAD_METHOD              connect_to_new_process
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                _fds
               84  CALL_METHOD_1         1  ''
               86  UNPACK_SEQUENCE_2     2 
               88  LOAD_FAST                'self'
               90  STORE_ATTR               sentinel
               92  STORE_FAST               'w'

 L.  54        94  LOAD_GLOBAL              os
               96  LOAD_METHOD              dup
               98  LOAD_FAST                'w'
              100  CALL_METHOD_1         1  ''
              102  STORE_FAST               '_parent_w'

 L.  55       104  LOAD_GLOBAL              util
              106  LOAD_METHOD              Finalize
              108  LOAD_FAST                'self'
              110  LOAD_GLOBAL              util
              112  LOAD_ATTR                close_fds

 L.  56       114  LOAD_FAST                '_parent_w'
              116  LOAD_FAST                'self'
              118  LOAD_ATTR                sentinel
              120  BUILD_TUPLE_2         2 

 L.  55       122  CALL_METHOD_3         3  ''
              124  LOAD_FAST                'self'
              126  STORE_ATTR               finalizer

 L.  57       128  LOAD_GLOBAL              open
              130  LOAD_FAST                'w'
              132  LOAD_STR                 'wb'
              134  LOAD_CONST               True
              136  LOAD_CONST               ('closefd',)
              138  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              140  SETUP_WITH          172  'to 172'
              142  STORE_FAST               'f'

 L.  58       144  LOAD_FAST                'f'
              146  LOAD_METHOD              write
              148  LOAD_FAST                'buf'
              150  LOAD_METHOD              getbuffer
              152  CALL_METHOD_0         0  ''
              154  CALL_METHOD_1         1  ''
              156  POP_TOP          
              158  POP_BLOCK        
              160  LOAD_CONST               None
              162  DUP_TOP          
              164  DUP_TOP          
              166  CALL_FUNCTION_3       3  ''
              168  POP_TOP          
              170  JUMP_FORWARD        188  'to 188'
            172_0  COME_FROM_WITH      140  '140'
              172  <49>             
              174  POP_JUMP_IF_TRUE    178  'to 178'
              176  <48>             
            178_0  COME_FROM           174  '174'
              178  POP_TOP          
              180  POP_TOP          
              182  POP_TOP          
              184  POP_EXCEPT       
              186  POP_TOP          
            188_0  COME_FROM           170  '170'

 L.  59       188  LOAD_GLOBAL              forkserver
              190  LOAD_METHOD              read_signed
              192  LOAD_FAST                'self'
              194  LOAD_ATTR                sentinel
              196  CALL_METHOD_1         1  ''
              198  LOAD_FAST                'self'
              200  STORE_ATTR               pid

Parse error at or near `POP_TOP' instruction at offset 62

    def poll--- This code section failed: ---

 L.  62         0  LOAD_FAST                'self'
                2  LOAD_ATTR                returncode
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE   106  'to 106'

 L.  63        10  LOAD_CONST               0
               12  LOAD_CONST               ('wait',)
               14  IMPORT_NAME_ATTR         multiprocessing.connection
               16  IMPORT_FROM              wait
               18  STORE_FAST               'wait'
               20  POP_TOP          

 L.  64        22  LOAD_FAST                'flag'
               24  LOAD_GLOBAL              os
               26  LOAD_ATTR                WNOHANG
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_FALSE    36  'to 36'
               32  LOAD_CONST               0
               34  JUMP_FORWARD         38  'to 38'
             36_0  COME_FROM            30  '30'
               36  LOAD_CONST               None
             38_0  COME_FROM            34  '34'
               38  STORE_FAST               'timeout'

 L.  65        40  LOAD_FAST                'wait'
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                sentinel
               46  BUILD_LIST_1          1 
               48  LOAD_FAST                'timeout'
               50  CALL_FUNCTION_2       2  ''
               52  POP_JUMP_IF_TRUE     58  'to 58'

 L.  66        54  LOAD_CONST               None
               56  RETURN_VALUE     
             58_0  COME_FROM            52  '52'

 L.  67        58  SETUP_FINALLY        78  'to 78'

 L.  68        60  LOAD_GLOBAL              forkserver
               62  LOAD_METHOD              read_signed
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                sentinel
               68  CALL_METHOD_1         1  ''
               70  LOAD_FAST                'self'
               72  STORE_ATTR               returncode
               74  POP_BLOCK        
               76  JUMP_FORWARD        106  'to 106'
             78_0  COME_FROM_FINALLY    58  '58'

 L.  69        78  DUP_TOP          
               80  LOAD_GLOBAL              OSError
               82  LOAD_GLOBAL              EOFError
               84  BUILD_TUPLE_2         2 
               86  <121>               104  ''
               88  POP_TOP          
               90  POP_TOP          
               92  POP_TOP          

 L.  72        94  LOAD_CONST               255
               96  LOAD_FAST                'self'
               98  STORE_ATTR               returncode
              100  POP_EXCEPT       
              102  JUMP_FORWARD        106  'to 106'
              104  <48>             
            106_0  COME_FROM           102  '102'
            106_1  COME_FROM            76  '76'
            106_2  COME_FROM             8  '8'

 L.  74       106  LOAD_FAST                'self'
              108  LOAD_ATTR                returncode
              110  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1