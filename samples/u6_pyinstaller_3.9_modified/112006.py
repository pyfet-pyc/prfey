# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: setuptools\installer.py
import glob, os, subprocess, sys, tempfile
from distutils import log
from distutils.errors import DistutilsError
import pkg_resources
from setuptools.wheel import Wheel

def _fixup_find_links--- This code section failed: ---

 L.  15         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'find_links'
                4  LOAD_GLOBAL              str
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L.  16        10  LOAD_FAST                'find_links'
               12  LOAD_METHOD              split
               14  CALL_METHOD_0         0  ''
               16  RETURN_VALUE     
             18_0  COME_FROM             8  '8'

 L.  17        18  LOAD_GLOBAL              isinstance
               20  LOAD_FAST                'find_links'
               22  LOAD_GLOBAL              tuple
               24  LOAD_GLOBAL              list
               26  BUILD_TUPLE_2         2 
               28  CALL_FUNCTION_2       2  ''
               30  POP_JUMP_IF_TRUE     36  'to 36'
               32  <74>             
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            30  '30'

 L.  18        36  LOAD_FAST                'find_links'
               38  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 32


def fetch_build_egg--- This code section failed: ---

 L.  26         0  SETUP_FINALLY        16  'to 16'

 L.  27         2  LOAD_GLOBAL              pkg_resources
                4  LOAD_METHOD              get_distribution
                6  LOAD_STR                 'wheel'
                8  CALL_METHOD_1         1  ''
               10  POP_TOP          
               12  POP_BLOCK        
               14  JUMP_FORWARD         50  'to 50'
             16_0  COME_FROM_FINALLY     0  '0'

 L.  28        16  DUP_TOP          
               18  LOAD_GLOBAL              pkg_resources
               20  LOAD_ATTR                DistributionNotFound
               22  <121>                48  ''
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L.  29        30  LOAD_FAST                'dist'
               32  LOAD_METHOD              announce
               34  LOAD_STR                 'WARNING: The wheel package is not available.'
               36  LOAD_GLOBAL              log
               38  LOAD_ATTR                WARN
               40  CALL_METHOD_2         2  ''
               42  POP_TOP          
               44  POP_EXCEPT       
               46  JUMP_FORWARD         50  'to 50'
               48  <48>             
             50_0  COME_FROM            46  '46'
             50_1  COME_FROM            14  '14'

 L.  31        50  LOAD_GLOBAL              strip_marker
               52  LOAD_FAST                'req'
               54  CALL_FUNCTION_1       1  ''
               56  STORE_FAST               'req'

 L.  35        58  LOAD_FAST                'dist'
               60  LOAD_METHOD              get_option_dict
               62  LOAD_STR                 'easy_install'
               64  CALL_METHOD_1         1  ''
               66  STORE_FAST               'opts'

 L.  36        68  LOAD_STR                 'allow_hosts'
               70  LOAD_FAST                'opts'
               72  <118>                 0  ''
               74  POP_JUMP_IF_FALSE    84  'to 84'

 L.  37        76  LOAD_GLOBAL              DistutilsError
               78  LOAD_STR                 'the `allow-hosts` option is not supported when using pip to install requirements.'
               80  CALL_FUNCTION_1       1  ''
               82  RAISE_VARARGS_1       1  'exception instance'
             84_0  COME_FROM            74  '74'

 L.  39        84  LOAD_STR                 'PIP_QUIET'
               86  LOAD_GLOBAL              os
               88  LOAD_ATTR                environ
               90  <118>                 1  ''
               92  JUMP_IF_FALSE_OR_POP   102  'to 102'
               94  LOAD_STR                 'PIP_VERBOSE'
               96  LOAD_GLOBAL              os
               98  LOAD_ATTR                environ
              100  <118>                 1  ''
            102_0  COME_FROM            92  '92'
              102  STORE_FAST               'quiet'

 L.  40       104  LOAD_STR                 'PIP_INDEX_URL'
              106  LOAD_GLOBAL              os
              108  LOAD_ATTR                environ
              110  <118>                 0  ''
              112  POP_JUMP_IF_FALSE   120  'to 120'

 L.  41       114  LOAD_CONST               None
              116  STORE_FAST               'index_url'
              118  JUMP_FORWARD        146  'to 146'
            120_0  COME_FROM           112  '112'

 L.  42       120  LOAD_STR                 'index_url'
              122  LOAD_FAST                'opts'
              124  <118>                 0  ''
              126  POP_JUMP_IF_FALSE   142  'to 142'

 L.  43       128  LOAD_FAST                'opts'
              130  LOAD_STR                 'index_url'
              132  BINARY_SUBSCR    
              134  LOAD_CONST               1
              136  BINARY_SUBSCR    
              138  STORE_FAST               'index_url'
              140  JUMP_FORWARD        146  'to 146'
            142_0  COME_FROM           126  '126'

 L.  45       142  LOAD_CONST               None
              144  STORE_FAST               'index_url'
            146_0  COME_FROM           140  '140'
            146_1  COME_FROM           118  '118'

 L.  47       146  LOAD_STR                 'find_links'
              148  LOAD_FAST                'opts'
              150  <118>                 0  ''
              152  POP_JUMP_IF_FALSE   178  'to 178'
              154  LOAD_GLOBAL              _fixup_find_links
              156  LOAD_FAST                'opts'
              158  LOAD_STR                 'find_links'
              160  BINARY_SUBSCR    
              162  LOAD_CONST               1
              164  BINARY_SUBSCR    
              166  CALL_FUNCTION_1       1  ''
              168  LOAD_CONST               None
              170  LOAD_CONST               None
              172  BUILD_SLICE_2         2 
              174  BINARY_SUBSCR    
              176  JUMP_FORWARD        180  'to 180'
            178_0  COME_FROM           152  '152'

 L.  48       178  BUILD_LIST_0          0 
            180_0  COME_FROM           176  '176'

 L.  46       180  STORE_FAST               'find_links'

 L.  50       182  LOAD_FAST                'dist'
              184  LOAD_ATTR                dependency_links
              186  POP_JUMP_IF_FALSE   200  'to 200'

 L.  51       188  LOAD_FAST                'find_links'
              190  LOAD_METHOD              extend
              192  LOAD_FAST                'dist'
              194  LOAD_ATTR                dependency_links
              196  CALL_METHOD_1         1  ''
              198  POP_TOP          
            200_0  COME_FROM           186  '186'

 L.  52       200  LOAD_GLOBAL              os
              202  LOAD_ATTR                path
              204  LOAD_METHOD              realpath
              206  LOAD_FAST                'dist'
              208  LOAD_METHOD              get_egg_cache_dir
              210  CALL_METHOD_0         0  ''
              212  CALL_METHOD_1         1  ''
              214  STORE_FAST               'eggs_dir'

 L.  53       216  LOAD_GLOBAL              pkg_resources
              218  LOAD_METHOD              Environment
              220  CALL_METHOD_0         0  ''
              222  STORE_FAST               'environment'

 L.  54       224  LOAD_GLOBAL              pkg_resources
              226  LOAD_METHOD              find_distributions
              228  LOAD_FAST                'eggs_dir'
              230  CALL_METHOD_1         1  ''
              232  GET_ITER         
            234_0  COME_FROM           254  '254'
            234_1  COME_FROM           244  '244'
              234  FOR_ITER            266  'to 266'
              236  STORE_FAST               'egg_dist'

 L.  55       238  LOAD_FAST                'egg_dist'
              240  LOAD_FAST                'req'
              242  <118>                 0  ''
              244  POP_JUMP_IF_FALSE   234  'to 234'
              246  LOAD_FAST                'environment'
              248  LOAD_METHOD              can_add
              250  LOAD_FAST                'egg_dist'
              252  CALL_METHOD_1         1  ''
              254  POP_JUMP_IF_FALSE   234  'to 234'

 L.  56       256  LOAD_FAST                'egg_dist'
              258  ROT_TWO          
              260  POP_TOP          
              262  RETURN_VALUE     
              264  JUMP_BACK           234  'to 234'

 L.  57       266  LOAD_GLOBAL              tempfile
              268  LOAD_METHOD              TemporaryDirectory
              270  CALL_METHOD_0         0  ''
          272_274  SETUP_WITH          576  'to 576'
              276  STORE_FAST               'tmpdir'

 L.  59       278  LOAD_GLOBAL              sys
              280  LOAD_ATTR                executable
              282  LOAD_STR                 '-m'
              284  LOAD_STR                 'pip'

 L.  60       286  LOAD_STR                 '--disable-pip-version-check'

 L.  61       288  LOAD_STR                 'wheel'
              290  LOAD_STR                 '--no-deps'

 L.  62       292  LOAD_STR                 '-w'
              294  LOAD_FAST                'tmpdir'

 L.  58       296  BUILD_LIST_8          8 
              298  STORE_FAST               'cmd'

 L.  64       300  LOAD_FAST                'quiet'
          302_304  POP_JUMP_IF_FALSE   316  'to 316'

 L.  65       306  LOAD_FAST                'cmd'
              308  LOAD_METHOD              append
              310  LOAD_STR                 '--quiet'
              312  CALL_METHOD_1         1  ''
              314  POP_TOP          
            316_0  COME_FROM           302  '302'

 L.  66       316  LOAD_FAST                'index_url'
              318  LOAD_CONST               None
              320  <117>                 1  ''
          322_324  POP_JUMP_IF_FALSE   340  'to 340'

 L.  67       326  LOAD_FAST                'cmd'
              328  LOAD_METHOD              extend
              330  LOAD_STR                 '--index-url'
              332  LOAD_FAST                'index_url'
              334  BUILD_TUPLE_2         2 
              336  CALL_METHOD_1         1  ''
              338  POP_TOP          
            340_0  COME_FROM           322  '322'

 L.  68       340  LOAD_FAST                'find_links'
          342_344  JUMP_IF_TRUE_OR_POP   348  'to 348'
              346  BUILD_LIST_0          0 
            348_0  COME_FROM           342  '342'
              348  GET_ITER         
              350  FOR_ITER            372  'to 372'
              352  STORE_FAST               'link'

 L.  69       354  LOAD_FAST                'cmd'
              356  LOAD_METHOD              extend
              358  LOAD_STR                 '--find-links'
              360  LOAD_FAST                'link'
              362  BUILD_TUPLE_2         2 
              364  CALL_METHOD_1         1  ''
              366  POP_TOP          
          368_370  JUMP_BACK           350  'to 350'

 L.  73       372  LOAD_FAST                'cmd'
              374  LOAD_METHOD              append
              376  LOAD_FAST                'req'
              378  LOAD_ATTR                url
          380_382  JUMP_IF_TRUE_OR_POP   390  'to 390'
              384  LOAD_GLOBAL              str
              386  LOAD_FAST                'req'
              388  CALL_FUNCTION_1       1  ''
            390_0  COME_FROM           380  '380'
              390  CALL_METHOD_1         1  ''
              392  POP_TOP          

 L.  74       394  SETUP_FINALLY       410  'to 410'

 L.  75       396  LOAD_GLOBAL              subprocess
              398  LOAD_METHOD              check_call
              400  LOAD_FAST                'cmd'
              402  CALL_METHOD_1         1  ''
              404  POP_TOP          
              406  POP_BLOCK        
              408  JUMP_FORWARD        464  'to 464'
            410_0  COME_FROM_FINALLY   394  '394'

 L.  76       410  DUP_TOP          
              412  LOAD_GLOBAL              subprocess
              414  LOAD_ATTR                CalledProcessError
          416_418  <121>               462  ''
              420  POP_TOP          
              422  STORE_FAST               'e'
              424  POP_TOP          
              426  SETUP_FINALLY       454  'to 454'

 L.  77       428  LOAD_GLOBAL              DistutilsError
              430  LOAD_GLOBAL              str
              432  LOAD_FAST                'e'
              434  CALL_FUNCTION_1       1  ''
              436  CALL_FUNCTION_1       1  ''
              438  LOAD_FAST                'e'
              440  RAISE_VARARGS_2       2  'exception instance with __cause__'
              442  POP_BLOCK        
              444  POP_EXCEPT       
              446  LOAD_CONST               None
              448  STORE_FAST               'e'
              450  DELETE_FAST              'e'
              452  JUMP_FORWARD        464  'to 464'
            454_0  COME_FROM_FINALLY   426  '426'
              454  LOAD_CONST               None
              456  STORE_FAST               'e'
              458  DELETE_FAST              'e'
              460  <48>             
              462  <48>             
            464_0  COME_FROM           452  '452'
            464_1  COME_FROM           408  '408'

 L.  78       464  LOAD_GLOBAL              Wheel
              466  LOAD_GLOBAL              glob
              468  LOAD_METHOD              glob
              470  LOAD_GLOBAL              os
              472  LOAD_ATTR                path
              474  LOAD_METHOD              join
              476  LOAD_FAST                'tmpdir'
              478  LOAD_STR                 '*.whl'
              480  CALL_METHOD_2         2  ''
              482  CALL_METHOD_1         1  ''
              484  LOAD_CONST               0
              486  BINARY_SUBSCR    
              488  CALL_FUNCTION_1       1  ''
              490  STORE_FAST               'wheel'

 L.  79       492  LOAD_GLOBAL              os
              494  LOAD_ATTR                path
              496  LOAD_METHOD              join
              498  LOAD_FAST                'eggs_dir'
              500  LOAD_FAST                'wheel'
              502  LOAD_METHOD              egg_name
              504  CALL_METHOD_0         0  ''
              506  CALL_METHOD_2         2  ''
              508  STORE_FAST               'dist_location'

 L.  80       510  LOAD_FAST                'wheel'
              512  LOAD_METHOD              install_as_egg
              514  LOAD_FAST                'dist_location'
              516  CALL_METHOD_1         1  ''
              518  POP_TOP          

 L.  81       520  LOAD_GLOBAL              pkg_resources
              522  LOAD_METHOD              PathMetadata

 L.  82       524  LOAD_FAST                'dist_location'
              526  LOAD_GLOBAL              os
              528  LOAD_ATTR                path
              530  LOAD_METHOD              join
              532  LOAD_FAST                'dist_location'
              534  LOAD_STR                 'EGG-INFO'
              536  CALL_METHOD_2         2  ''

 L.  81       538  CALL_METHOD_2         2  ''
              540  STORE_FAST               'dist_metadata'

 L.  83       542  LOAD_GLOBAL              pkg_resources
              544  LOAD_ATTR                Distribution
              546  LOAD_ATTR                from_filename

 L.  84       548  LOAD_FAST                'dist_location'
              550  LOAD_FAST                'dist_metadata'

 L.  83       552  LOAD_CONST               ('metadata',)
              554  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              556  STORE_FAST               'dist'

 L.  85       558  LOAD_FAST                'dist'
              560  POP_BLOCK        
              562  ROT_TWO          
              564  LOAD_CONST               None
              566  DUP_TOP          
              568  DUP_TOP          
              570  CALL_FUNCTION_3       3  ''
              572  POP_TOP          
              574  RETURN_VALUE     
            576_0  COME_FROM_WITH      272  '272'
              576  <49>             
          578_580  POP_JUMP_IF_TRUE    584  'to 584'
              582  <48>             
            584_0  COME_FROM           578  '578'
              584  POP_TOP          
              586  POP_TOP          
              588  POP_TOP          
              590  POP_EXCEPT       
              592  POP_TOP          

Parse error at or near `<121>' instruction at offset 22


def strip_marker(req):
    """
    Return a new requirement without the environment marker to avoid
    calling pip with something like `babel; extra == "i18n"`, which
    would always be ignored.
    """
    req = pkg_resources.Requirement.parsestr(req)
    req.marker = None
    return req