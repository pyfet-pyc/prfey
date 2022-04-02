# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: distutils\config.py
"""distutils.pypirc

Provides the PyPIRCCommand class, the base class for the command classes
that uses .pypirc in the distutils.command package.
"""
import os
from configparser import RawConfigParser
from distutils.cmd import Command
DEFAULT_PYPIRC = '[distutils]\nindex-servers =\n    pypi\n\n[pypi]\nusername:%s\npassword:%s\n'

class PyPIRCCommand(Command):
    __doc__ = 'Base command that knows how to handle the .pypirc file\n    '
    DEFAULT_REPOSITORY = 'https://upload.pypi.org/legacy/'
    DEFAULT_REALM = 'pypi'
    repository = None
    realm = None
    user_options = [
     (
      'repository=', 'r',
      'url of repository [default: %s]' % DEFAULT_REPOSITORY),
     ('show-response', None, 'display full response text from server')]
    boolean_options = [
     'show-response']

    def _get_rc_file(self):
        """Returns rc file path."""
        return os.path.join(os.path.expanduser('~'), '.pypirc')

    def _store_pypirc--- This code section failed: ---

 L.  44         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _get_rc_file
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'rc'

 L.  45         8  LOAD_GLOBAL              os
               10  LOAD_METHOD              fdopen
               12  LOAD_GLOBAL              os
               14  LOAD_METHOD              open
               16  LOAD_FAST                'rc'
               18  LOAD_GLOBAL              os
               20  LOAD_ATTR                O_CREAT
               22  LOAD_GLOBAL              os
               24  LOAD_ATTR                O_WRONLY
               26  BINARY_OR        
               28  LOAD_CONST               384
               30  CALL_METHOD_3         3  ''
               32  LOAD_STR                 'w'
               34  CALL_METHOD_2         2  ''
               36  SETUP_WITH           72  'to 72'
               38  STORE_FAST               'f'

 L.  46        40  LOAD_FAST                'f'
               42  LOAD_METHOD              write
               44  LOAD_GLOBAL              DEFAULT_PYPIRC
               46  LOAD_FAST                'username'
               48  LOAD_FAST                'password'
               50  BUILD_TUPLE_2         2 
               52  BINARY_MODULO    
               54  CALL_METHOD_1         1  ''
               56  POP_TOP          
               58  POP_BLOCK        
               60  LOAD_CONST               None
               62  DUP_TOP          
               64  DUP_TOP          
               66  CALL_FUNCTION_3       3  ''
               68  POP_TOP          
               70  JUMP_FORWARD         88  'to 88'
             72_0  COME_FROM_WITH       36  '36'
               72  <49>             
               74  POP_JUMP_IF_TRUE     78  'to 78'
               76  <48>             
             78_0  COME_FROM            74  '74'
               78  POP_TOP          
               80  POP_TOP          
               82  POP_TOP          
               84  POP_EXCEPT       
               86  POP_TOP          
             88_0  COME_FROM            70  '70'

Parse error at or near `DUP_TOP' instruction at offset 62

    def _read_pypirc--- This code section failed: ---

 L.  50         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _get_rc_file
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'rc'

 L.  51         8  LOAD_GLOBAL              os
               10  LOAD_ATTR                path
               12  LOAD_METHOD              exists
               14  LOAD_FAST                'rc'
               16  CALL_METHOD_1         1  ''
            18_20  POP_JUMP_IF_FALSE   408  'to 408'

 L.  52        22  LOAD_FAST                'self'
               24  LOAD_METHOD              announce
               26  LOAD_STR                 'Using PyPI login from %s'
               28  LOAD_FAST                'rc'
               30  BINARY_MODULO    
               32  CALL_METHOD_1         1  ''
               34  POP_TOP          

 L.  53        36  LOAD_FAST                'self'
               38  LOAD_ATTR                repository
               40  JUMP_IF_TRUE_OR_POP    46  'to 46'
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                DEFAULT_REPOSITORY
             46_0  COME_FROM            40  '40'
               46  STORE_FAST               'repository'

 L.  55        48  LOAD_GLOBAL              RawConfigParser
               50  CALL_FUNCTION_0       0  ''
               52  STORE_FAST               'config'

 L.  56        54  LOAD_FAST                'config'
               56  LOAD_METHOD              read
               58  LOAD_FAST                'rc'
               60  CALL_METHOD_1         1  ''
               62  POP_TOP          

 L.  57        64  LOAD_FAST                'config'
               66  LOAD_METHOD              sections
               68  CALL_METHOD_0         0  ''
               70  STORE_FAST               'sections'

 L.  58        72  LOAD_STR                 'distutils'
               74  LOAD_FAST                'sections'
               76  <118>                 0  ''
            78_80  POP_JUMP_IF_FALSE   326  'to 326'

 L.  60        82  LOAD_FAST                'config'
               84  LOAD_METHOD              get
               86  LOAD_STR                 'distutils'
               88  LOAD_STR                 'index-servers'
               90  CALL_METHOD_2         2  ''
               92  STORE_FAST               'index_servers'

 L.  61        94  LOAD_LISTCOMP            '<code_object <listcomp>>'
               96  LOAD_STR                 'PyPIRCCommand._read_pypirc.<locals>.<listcomp>'
               98  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.  62       100  LOAD_FAST                'index_servers'
              102  LOAD_METHOD              split
              104  LOAD_STR                 '\n'
              106  CALL_METHOD_1         1  ''

 L.  61       108  GET_ITER         
              110  CALL_FUNCTION_1       1  ''
              112  STORE_FAST               '_servers'

 L.  64       114  LOAD_FAST                '_servers'
              116  BUILD_LIST_0          0 
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_FALSE   142  'to 142'

 L.  66       122  LOAD_STR                 'pypi'
              124  LOAD_FAST                'sections'
              126  <118>                 0  ''
              128  POP_JUMP_IF_FALSE   138  'to 138'

 L.  67       130  LOAD_STR                 'pypi'
              132  BUILD_LIST_1          1 
              134  STORE_FAST               '_servers'
              136  JUMP_FORWARD        142  'to 142'
            138_0  COME_FROM           128  '128'

 L.  71       138  BUILD_MAP_0           0 
              140  RETURN_VALUE     
            142_0  COME_FROM           136  '136'
            142_1  COME_FROM           120  '120'

 L.  72       142  LOAD_FAST                '_servers'
              144  GET_ITER         
            146_0  COME_FROM           322  '322'
            146_1  COME_FROM           312  '312'
              146  FOR_ITER            324  'to 324'
              148  STORE_FAST               'server'

 L.  73       150  LOAD_STR                 'server'
              152  LOAD_FAST                'server'
              154  BUILD_MAP_1           1 
              156  STORE_FAST               'current'

 L.  74       158  LOAD_FAST                'config'
              160  LOAD_METHOD              get
              162  LOAD_FAST                'server'
              164  LOAD_STR                 'username'
              166  CALL_METHOD_2         2  ''
              168  LOAD_FAST                'current'
              170  LOAD_STR                 'username'
              172  STORE_SUBSCR     

 L.  77       174  LOAD_STR                 'repository'

 L.  78       176  LOAD_FAST                'self'
              178  LOAD_ATTR                DEFAULT_REPOSITORY

 L.  77       180  BUILD_TUPLE_2         2 

 L.  79       182  LOAD_STR                 'realm'
              184  LOAD_FAST                'self'
              186  LOAD_ATTR                DEFAULT_REALM
              188  BUILD_TUPLE_2         2 

 L.  80       190  LOAD_CONST               ('password', None)

 L.  77       192  BUILD_TUPLE_3         3 
              194  GET_ITER         
            196_0  COME_FROM           242  '242'
            196_1  COME_FROM           232  '232'
              196  FOR_ITER            244  'to 244'
              198  UNPACK_SEQUENCE_2     2 
              200  STORE_FAST               'key'
              202  STORE_FAST               'default'

 L.  81       204  LOAD_FAST                'config'
              206  LOAD_METHOD              has_option
              208  LOAD_FAST                'server'
              210  LOAD_FAST                'key'
              212  CALL_METHOD_2         2  ''
              214  POP_JUMP_IF_FALSE   234  'to 234'

 L.  82       216  LOAD_FAST                'config'
              218  LOAD_METHOD              get
              220  LOAD_FAST                'server'
              222  LOAD_FAST                'key'
              224  CALL_METHOD_2         2  ''
              226  LOAD_FAST                'current'
              228  LOAD_FAST                'key'
              230  STORE_SUBSCR     
              232  JUMP_BACK           196  'to 196'
            234_0  COME_FROM           214  '214'

 L.  84       234  LOAD_FAST                'default'
              236  LOAD_FAST                'current'
              238  LOAD_FAST                'key'
              240  STORE_SUBSCR     
              242  JUMP_BACK           196  'to 196'
            244_0  COME_FROM           196  '196'

 L.  89       244  LOAD_FAST                'server'
              246  LOAD_STR                 'pypi'
              248  COMPARE_OP               ==
          250_252  POP_JUMP_IF_FALSE   288  'to 288'

 L.  90       254  LOAD_FAST                'repository'
              256  LOAD_FAST                'self'
              258  LOAD_ATTR                DEFAULT_REPOSITORY
              260  LOAD_STR                 'pypi'
              262  BUILD_TUPLE_2         2 
              264  <118>                 0  ''

 L.  89   266_268  POP_JUMP_IF_FALSE   288  'to 288'

 L.  91       270  LOAD_FAST                'self'
              272  LOAD_ATTR                DEFAULT_REPOSITORY
              274  LOAD_FAST                'current'
              276  LOAD_STR                 'repository'
              278  STORE_SUBSCR     

 L.  92       280  LOAD_FAST                'current'
              282  ROT_TWO          
              284  POP_TOP          
              286  RETURN_VALUE     
            288_0  COME_FROM           266  '266'
            288_1  COME_FROM           250  '250'

 L.  94       288  LOAD_FAST                'current'
              290  LOAD_STR                 'server'
              292  BINARY_SUBSCR    
              294  LOAD_FAST                'repository'
              296  COMPARE_OP               ==
          298_300  POP_JUMP_IF_TRUE    314  'to 314'

 L.  95       302  LOAD_FAST                'current'
              304  LOAD_STR                 'repository'
              306  BINARY_SUBSCR    
              308  LOAD_FAST                'repository'
              310  COMPARE_OP               ==

 L.  94       312  POP_JUMP_IF_FALSE_BACK   146  'to 146'
            314_0  COME_FROM           298  '298'

 L.  96       314  LOAD_FAST                'current'
              316  ROT_TWO          
              318  POP_TOP          
              320  RETURN_VALUE     
              322  JUMP_BACK           146  'to 146'
            324_0  COME_FROM           146  '146'
              324  JUMP_FORWARD        408  'to 408'
            326_0  COME_FROM            78  '78'

 L.  97       326  LOAD_STR                 'server-login'
              328  LOAD_FAST                'sections'
              330  <118>                 0  ''
          332_334  POP_JUMP_IF_FALSE   408  'to 408'

 L.  99       336  LOAD_STR                 'server-login'
              338  STORE_FAST               'server'

 L. 100       340  LOAD_FAST                'config'
              342  LOAD_METHOD              has_option
              344  LOAD_FAST                'server'
              346  LOAD_STR                 'repository'
              348  CALL_METHOD_2         2  ''
          350_352  POP_JUMP_IF_FALSE   368  'to 368'

 L. 101       354  LOAD_FAST                'config'
              356  LOAD_METHOD              get
              358  LOAD_FAST                'server'
              360  LOAD_STR                 'repository'
              362  CALL_METHOD_2         2  ''
              364  STORE_FAST               'repository'
              366  JUMP_FORWARD        374  'to 374'
            368_0  COME_FROM           350  '350'

 L. 103       368  LOAD_FAST                'self'
              370  LOAD_ATTR                DEFAULT_REPOSITORY
              372  STORE_FAST               'repository'
            374_0  COME_FROM           366  '366'

 L. 104       374  LOAD_FAST                'config'
              376  LOAD_METHOD              get
              378  LOAD_FAST                'server'
              380  LOAD_STR                 'username'
              382  CALL_METHOD_2         2  ''

 L. 105       384  LOAD_FAST                'config'
              386  LOAD_METHOD              get
              388  LOAD_FAST                'server'
              390  LOAD_STR                 'password'
              392  CALL_METHOD_2         2  ''

 L. 106       394  LOAD_FAST                'repository'

 L. 107       396  LOAD_FAST                'server'

 L. 108       398  LOAD_FAST                'self'
              400  LOAD_ATTR                DEFAULT_REALM

 L. 104       402  LOAD_CONST               ('username', 'password', 'repository', 'server', 'realm')
              404  BUILD_CONST_KEY_MAP_5     5 
              406  RETURN_VALUE     
            408_0  COME_FROM           332  '332'
            408_1  COME_FROM           324  '324'
            408_2  COME_FROM            18  '18'

 L. 110       408  BUILD_MAP_0           0 
              410  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 76

    def _read_pypi_response(self, response):
        """Read and decode a PyPI HTTP response."""
        import cgi
        content_type = response.getheader('content-type', 'text/plain')
        encoding = cgi.parse_header(content_type)[1].get('charset', 'ascii')
        return response.read.decode(encoding)

    def initialize_options(self):
        """Initialize options."""
        self.repository = None
        self.realm = None
        self.show_response = 0

    def finalize_options--- This code section failed: ---

 L. 127         0  LOAD_FAST                'self'
                2  LOAD_ATTR                repository
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 128        10  LOAD_FAST                'self'
               12  LOAD_ATTR                DEFAULT_REPOSITORY
               14  LOAD_FAST                'self'
               16  STORE_ATTR               repository
             18_0  COME_FROM             8  '8'

 L. 129        18  LOAD_FAST                'self'
               20  LOAD_ATTR                realm
               22  LOAD_CONST               None
               24  <117>                 0  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 130        28  LOAD_FAST                'self'
               30  LOAD_ATTR                DEFAULT_REALM
               32  LOAD_FAST                'self'
               34  STORE_ATTR               realm
             36_0  COME_FROM            26  '26'

Parse error at or near `None' instruction at offset -1