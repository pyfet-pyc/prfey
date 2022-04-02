# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: multiprocessing\popen_spawn_posix.py
import io, os
from .context import reduction, set_spawning_popen
from . import popen_fork
from . import spawn
from . import util
__all__ = [
 'Popen']

class _DupFd(object):

    def __init__(self, fd):
        self.fd = fd

    def detach(self):
        return self.fd


class Popen(popen_fork.Popen):
    method = 'spawn'
    DupFd = _DupFd

    def __init__(self, process_obj):
        self._fds = []
        super().__init__(process_obj)

    def duplicate_for_child(self, fd):
        self._fds.append(fd)
        return fd

    def _launch--- This code section failed: ---

 L.  39         0  LOAD_CONST               1
                2  LOAD_CONST               ('resource_tracker',)
                4  IMPORT_NAME              
                6  IMPORT_FROM              resource_tracker
                8  STORE_FAST               'resource_tracker'
               10  POP_TOP          

 L.  40        12  LOAD_FAST                'resource_tracker'
               14  LOAD_METHOD              getfd
               16  CALL_METHOD_0         0  ''
               18  STORE_FAST               'tracker_fd'

 L.  41        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _fds
               24  LOAD_METHOD              append
               26  LOAD_FAST                'tracker_fd'
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L.  42        32  LOAD_GLOBAL              spawn
               34  LOAD_METHOD              get_preparation_data
               36  LOAD_FAST                'process_obj'
               38  LOAD_ATTR                _name
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'prep_data'

 L.  43        44  LOAD_GLOBAL              io
               46  LOAD_METHOD              BytesIO
               48  CALL_METHOD_0         0  ''
               50  STORE_FAST               'fp'

 L.  44        52  LOAD_GLOBAL              set_spawning_popen
               54  LOAD_FAST                'self'
               56  CALL_FUNCTION_1       1  ''
               58  POP_TOP          

 L.  45        60  SETUP_FINALLY        98  'to 98'

 L.  46        62  LOAD_GLOBAL              reduction
               64  LOAD_METHOD              dump
               66  LOAD_FAST                'prep_data'
               68  LOAD_FAST                'fp'
               70  CALL_METHOD_2         2  ''
               72  POP_TOP          

 L.  47        74  LOAD_GLOBAL              reduction
               76  LOAD_METHOD              dump
               78  LOAD_FAST                'process_obj'
               80  LOAD_FAST                'fp'
               82  CALL_METHOD_2         2  ''
               84  POP_TOP          
               86  POP_BLOCK        

 L.  49        88  LOAD_GLOBAL              set_spawning_popen
               90  LOAD_CONST               None
               92  CALL_FUNCTION_1       1  ''
               94  POP_TOP          
               96  JUMP_FORWARD        108  'to 108'
             98_0  COME_FROM_FINALLY    60  '60'
               98  LOAD_GLOBAL              set_spawning_popen
              100  LOAD_CONST               None
              102  CALL_FUNCTION_1       1  ''
              104  POP_TOP          
              106  <48>             
            108_0  COME_FROM            96  '96'

 L.  51       108  LOAD_CONST               None
              110  DUP_TOP          
              112  STORE_FAST               'parent_r'
              114  DUP_TOP          
              116  STORE_FAST               'child_w'
              118  DUP_TOP          
              120  STORE_FAST               'child_r'
              122  STORE_FAST               'parent_w'

 L.  52       124  SETUP_FINALLY       368  'to 368'

 L.  53       126  LOAD_GLOBAL              os
              128  LOAD_METHOD              pipe
              130  CALL_METHOD_0         0  ''
              132  UNPACK_SEQUENCE_2     2 
              134  STORE_FAST               'parent_r'
              136  STORE_FAST               'child_w'

 L.  54       138  LOAD_GLOBAL              os
              140  LOAD_METHOD              pipe
              142  CALL_METHOD_0         0  ''
              144  UNPACK_SEQUENCE_2     2 
              146  STORE_FAST               'child_r'
              148  STORE_FAST               'parent_w'

 L.  55       150  LOAD_GLOBAL              spawn
              152  LOAD_ATTR                get_command_line
              154  LOAD_FAST                'tracker_fd'

 L.  56       156  LOAD_FAST                'child_r'

 L.  55       158  LOAD_CONST               ('tracker_fd', 'pipe_handle')
              160  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              162  STORE_FAST               'cmd'

 L.  57       164  LOAD_FAST                'self'
              166  LOAD_ATTR                _fds
              168  LOAD_METHOD              extend
              170  LOAD_FAST                'child_r'
              172  LOAD_FAST                'child_w'
              174  BUILD_LIST_2          2 
              176  CALL_METHOD_1         1  ''
              178  POP_TOP          

 L.  58       180  LOAD_GLOBAL              util
              182  LOAD_METHOD              spawnv_passfds
              184  LOAD_GLOBAL              spawn
              186  LOAD_METHOD              get_executable
              188  CALL_METHOD_0         0  ''

 L.  59       190  LOAD_FAST                'cmd'
              192  LOAD_FAST                'self'
              194  LOAD_ATTR                _fds

 L.  58       196  CALL_METHOD_3         3  ''
              198  LOAD_FAST                'self'
              200  STORE_ATTR               pid

 L.  60       202  LOAD_FAST                'parent_r'
              204  LOAD_FAST                'self'
              206  STORE_ATTR               sentinel

 L.  61       208  LOAD_GLOBAL              open
              210  LOAD_FAST                'parent_w'
              212  LOAD_STR                 'wb'
              214  LOAD_CONST               False
              216  LOAD_CONST               ('closefd',)
              218  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              220  SETUP_WITH          252  'to 252'
              222  STORE_FAST               'f'

 L.  62       224  LOAD_FAST                'f'
              226  LOAD_METHOD              write
              228  LOAD_FAST                'fp'
              230  LOAD_METHOD              getbuffer
              232  CALL_METHOD_0         0  ''
              234  CALL_METHOD_1         1  ''
              236  POP_TOP          
              238  POP_BLOCK        
              240  LOAD_CONST               None
              242  DUP_TOP          
              244  DUP_TOP          
              246  CALL_FUNCTION_3       3  ''
              248  POP_TOP          
              250  JUMP_FORWARD        270  'to 270'
            252_0  COME_FROM_WITH      220  '220'
              252  <49>             
          254_256  POP_JUMP_IF_TRUE    260  'to 260'
              258  <48>             
            260_0  COME_FROM           254  '254'
              260  POP_TOP          
              262  POP_TOP          
              264  POP_TOP          
              266  POP_EXCEPT       
              268  POP_TOP          
            270_0  COME_FROM           250  '250'
              270  POP_BLOCK        

 L.  64       272  BUILD_LIST_0          0 
              274  STORE_FAST               'fds_to_close'

 L.  65       276  LOAD_FAST                'parent_r'
              278  LOAD_FAST                'parent_w'
              280  BUILD_TUPLE_2         2 
              282  GET_ITER         
            284_0  COME_FROM           308  '308'
            284_1  COME_FROM           294  '294'
              284  FOR_ITER            312  'to 312'
              286  STORE_FAST               'fd'

 L.  66       288  LOAD_FAST                'fd'
              290  LOAD_CONST               None
              292  <117>                 1  ''
          294_296  POP_JUMP_IF_FALSE_BACK   284  'to 284'

 L.  67       298  LOAD_FAST                'fds_to_close'
              300  LOAD_METHOD              append
              302  LOAD_FAST                'fd'
              304  CALL_METHOD_1         1  ''
              306  POP_TOP          
          308_310  JUMP_BACK           284  'to 284'
            312_0  COME_FROM           284  '284'

 L.  68       312  LOAD_GLOBAL              util
              314  LOAD_METHOD              Finalize
              316  LOAD_FAST                'self'
              318  LOAD_GLOBAL              util
              320  LOAD_ATTR                close_fds
              322  LOAD_FAST                'fds_to_close'
              324  CALL_METHOD_3         3  ''
              326  LOAD_FAST                'self'
              328  STORE_ATTR               finalizer

 L.  70       330  LOAD_FAST                'child_r'
              332  LOAD_FAST                'child_w'
              334  BUILD_TUPLE_2         2 
              336  GET_ITER         
            338_0  COME_FROM           362  '362'
            338_1  COME_FROM           348  '348'
              338  FOR_ITER            366  'to 366'
              340  STORE_FAST               'fd'

 L.  71       342  LOAD_FAST                'fd'
              344  LOAD_CONST               None
              346  <117>                 1  ''
          348_350  POP_JUMP_IF_FALSE_BACK   338  'to 338'

 L.  72       352  LOAD_GLOBAL              os
              354  LOAD_METHOD              close
              356  LOAD_FAST                'fd'
              358  CALL_METHOD_1         1  ''
              360  POP_TOP          
          362_364  JUMP_BACK           338  'to 338'
            366_0  COME_FROM           338  '338'
              366  JUMP_FORWARD        464  'to 464'
            368_0  COME_FROM_FINALLY   124  '124'

 L.  64       368  BUILD_LIST_0          0 
              370  STORE_FAST               'fds_to_close'

 L.  65       372  LOAD_FAST                'parent_r'
              374  LOAD_FAST                'parent_w'
              376  BUILD_TUPLE_2         2 
              378  GET_ITER         
            380_0  COME_FROM           404  '404'
            380_1  COME_FROM           390  '390'
              380  FOR_ITER            408  'to 408'
              382  STORE_FAST               'fd'

 L.  66       384  LOAD_FAST                'fd'
              386  LOAD_CONST               None
              388  <117>                 1  ''
          390_392  POP_JUMP_IF_FALSE_BACK   380  'to 380'

 L.  67       394  LOAD_FAST                'fds_to_close'
              396  LOAD_METHOD              append
              398  LOAD_FAST                'fd'
              400  CALL_METHOD_1         1  ''
              402  POP_TOP          
          404_406  JUMP_BACK           380  'to 380'
            408_0  COME_FROM           380  '380'

 L.  68       408  LOAD_GLOBAL              util
              410  LOAD_METHOD              Finalize
              412  LOAD_FAST                'self'
              414  LOAD_GLOBAL              util
              416  LOAD_ATTR                close_fds
              418  LOAD_FAST                'fds_to_close'
              420  CALL_METHOD_3         3  ''
              422  LOAD_FAST                'self'
              424  STORE_ATTR               finalizer

 L.  70       426  LOAD_FAST                'child_r'
              428  LOAD_FAST                'child_w'
              430  BUILD_TUPLE_2         2 
              432  GET_ITER         
            434_0  COME_FROM           458  '458'
            434_1  COME_FROM           444  '444'
              434  FOR_ITER            462  'to 462'
              436  STORE_FAST               'fd'

 L.  71       438  LOAD_FAST                'fd'
              440  LOAD_CONST               None
              442  <117>                 1  ''
          444_446  POP_JUMP_IF_FALSE_BACK   434  'to 434'

 L.  72       448  LOAD_GLOBAL              os
              450  LOAD_METHOD              close
              452  LOAD_FAST                'fd'
              454  CALL_METHOD_1         1  ''
              456  POP_TOP          
          458_460  JUMP_BACK           434  'to 434'
            462_0  COME_FROM           434  '434'
              462  <48>             
            464_0  COME_FROM           366  '366'

Parse error at or near `POP_TOP' instruction at offset 94