# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: setuptools\installer.py
import glob, os, subprocess, sys
from distutils import log
from distutils.errors import DistutilsError
import pkg_resources
import setuptools.command.easy_install as easy_install
from setuptools.extern import six
from setuptools.wheel import Wheel
from .py31compat import TemporaryDirectory

def _fixup_find_links--- This code section failed: ---

 L.  18         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'find_links'
                4  LOAD_GLOBAL              six
                6  LOAD_ATTR                string_types
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L.  19        12  LOAD_FAST                'find_links'
               14  LOAD_METHOD              split
               16  CALL_METHOD_0         0  ''
               18  RETURN_VALUE     
             20_0  COME_FROM            10  '10'

 L.  20        20  LOAD_GLOBAL              isinstance
               22  LOAD_FAST                'find_links'
               24  LOAD_GLOBAL              tuple
               26  LOAD_GLOBAL              list
               28  BUILD_TUPLE_2         2 
               30  CALL_FUNCTION_2       2  ''
               32  POP_JUMP_IF_TRUE     38  'to 38'
               34  <74>             
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            32  '32'

 L.  21        38  LOAD_FAST                'find_links'
               40  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 34


def _legacy_fetch_build_egg--- This code section failed: ---

 L.  29         0  LOAD_FAST                'dist'
                2  LOAD_METHOD              __class__
                4  LOAD_STR                 'script_args'
                6  LOAD_STR                 'easy_install'
                8  BUILD_LIST_1          1 
               10  BUILD_MAP_1           1 
               12  CALL_METHOD_1         1  ''
               14  STORE_FAST               'tmp_dist'

 L.  30        16  LOAD_FAST                'tmp_dist'
               18  LOAD_METHOD              get_option_dict
               20  LOAD_STR                 'easy_install'
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'opts'

 L.  31        26  LOAD_FAST                'opts'
               28  LOAD_METHOD              clear
               30  CALL_METHOD_0         0  ''
               32  POP_TOP          

 L.  32        34  LOAD_FAST                'opts'
               36  LOAD_METHOD              update
               38  LOAD_GENEXPR             '<code_object <genexpr>>'
               40  LOAD_STR                 '_legacy_fetch_build_egg.<locals>.<genexpr>'
               42  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.  34        44  LOAD_FAST                'dist'
               46  LOAD_METHOD              get_option_dict
               48  LOAD_STR                 'easy_install'
               50  CALL_METHOD_1         1  ''
               52  LOAD_METHOD              items
               54  CALL_METHOD_0         0  ''

 L.  32        56  GET_ITER         
               58  CALL_FUNCTION_1       1  ''
               60  CALL_METHOD_1         1  ''
               62  POP_TOP          

 L.  40        64  LOAD_FAST                'dist'
               66  LOAD_ATTR                dependency_links
               68  POP_JUMP_IF_FALSE   124  'to 124'

 L.  41        70  LOAD_FAST                'dist'
               72  LOAD_ATTR                dependency_links
               74  LOAD_CONST               None
               76  LOAD_CONST               None
               78  BUILD_SLICE_2         2 
               80  BINARY_SUBSCR    
               82  STORE_FAST               'links'

 L.  42        84  LOAD_STR                 'find_links'
               86  LOAD_FAST                'opts'
               88  <118>                 0  ''
               90  POP_JUMP_IF_FALSE   112  'to 112'

 L.  43        92  LOAD_GLOBAL              _fixup_find_links
               94  LOAD_FAST                'opts'
               96  LOAD_STR                 'find_links'
               98  BINARY_SUBSCR    
              100  LOAD_CONST               1
              102  BINARY_SUBSCR    
              104  CALL_FUNCTION_1       1  ''
              106  LOAD_FAST                'links'
              108  BINARY_ADD       
              110  STORE_FAST               'links'
            112_0  COME_FROM            90  '90'

 L.  44       112  LOAD_STR                 'setup'
              114  LOAD_FAST                'links'
              116  BUILD_TUPLE_2         2 
              118  LOAD_FAST                'opts'
              120  LOAD_STR                 'find_links'
              122  STORE_SUBSCR     
            124_0  COME_FROM            68  '68'

 L.  45       124  LOAD_FAST                'dist'
              126  LOAD_METHOD              get_egg_cache_dir
              128  CALL_METHOD_0         0  ''
              130  STORE_FAST               'install_dir'

 L.  46       132  LOAD_GLOBAL              easy_install

 L.  47       134  LOAD_FAST                'tmp_dist'
              136  LOAD_STR                 'x'
              138  BUILD_LIST_1          1 
              140  LOAD_FAST                'install_dir'

 L.  48       142  LOAD_CONST               True

 L.  49       144  LOAD_CONST               False
              146  LOAD_CONST               None
              148  LOAD_CONST               False

 L.  50       150  LOAD_CONST               False
              152  LOAD_CONST               True
              154  LOAD_CONST               True
              156  LOAD_CONST               False

 L.  46       158  LOAD_CONST               ('args', 'install_dir', 'exclude_scripts', 'always_copy', 'build_directory', 'editable', 'upgrade', 'multi_version', 'no_report', 'user')
              160  CALL_FUNCTION_KW_11    11  '11 total positional and keyword args'
              162  STORE_FAST               'cmd'

 L.  52       164  LOAD_FAST                'cmd'
              166  LOAD_METHOD              ensure_finalized
              168  CALL_METHOD_0         0  ''
              170  POP_TOP          

 L.  53       172  LOAD_FAST                'cmd'
              174  LOAD_METHOD              easy_install
              176  LOAD_FAST                'req'
              178  CALL_METHOD_1         1  ''
              180  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 88


def fetch_build_egg--- This code section failed: ---

 L.  61         0  SETUP_FINALLY        16  'to 16'

 L.  62         2  LOAD_GLOBAL              pkg_resources
                4  LOAD_METHOD              get_distribution
                6  LOAD_STR                 'pip'
                8  CALL_METHOD_1         1  ''
               10  POP_TOP          
               12  POP_BLOCK        
               14  JUMP_FORWARD         60  'to 60'
             16_0  COME_FROM_FINALLY     0  '0'

 L.  63        16  DUP_TOP          
               18  LOAD_GLOBAL              pkg_resources
               20  LOAD_ATTR                DistributionNotFound
               22  <121>                58  ''
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L.  64        30  LOAD_FAST                'dist'
               32  LOAD_METHOD              announce

 L.  65        34  LOAD_STR                 'WARNING: The pip package is not available, falling back to EasyInstall for handling setup_requires/test_requires; this is deprecated and will be removed in a future version.'

 L.  68        36  LOAD_GLOBAL              log
               38  LOAD_ATTR                WARN

 L.  64        40  CALL_METHOD_2         2  ''
               42  POP_TOP          

 L.  70        44  LOAD_GLOBAL              _legacy_fetch_build_egg
               46  LOAD_FAST                'dist'
               48  LOAD_FAST                'req'
               50  CALL_FUNCTION_2       2  ''
               52  ROT_FOUR         
               54  POP_EXCEPT       
               56  RETURN_VALUE     
               58  <48>             
             60_0  COME_FROM            14  '14'

 L.  72        60  SETUP_FINALLY        76  'to 76'

 L.  73        62  LOAD_GLOBAL              pkg_resources
               64  LOAD_METHOD              get_distribution
               66  LOAD_STR                 'wheel'
               68  CALL_METHOD_1         1  ''
               70  POP_TOP          
               72  POP_BLOCK        
               74  JUMP_FORWARD        110  'to 110'
             76_0  COME_FROM_FINALLY    60  '60'

 L.  74        76  DUP_TOP          
               78  LOAD_GLOBAL              pkg_resources
               80  LOAD_ATTR                DistributionNotFound
               82  <121>               108  ''
               84  POP_TOP          
               86  POP_TOP          
               88  POP_TOP          

 L.  75        90  LOAD_FAST                'dist'
               92  LOAD_METHOD              announce
               94  LOAD_STR                 'WARNING: The wheel package is not available.'
               96  LOAD_GLOBAL              log
               98  LOAD_ATTR                WARN
              100  CALL_METHOD_2         2  ''
              102  POP_TOP          
              104  POP_EXCEPT       
              106  JUMP_FORWARD        110  'to 110'
              108  <48>             
            110_0  COME_FROM           106  '106'
            110_1  COME_FROM            74  '74'

 L.  77       110  LOAD_GLOBAL              strip_marker
              112  LOAD_FAST                'req'
              114  CALL_FUNCTION_1       1  ''
              116  STORE_FAST               'req'

 L.  81       118  LOAD_FAST                'dist'
              120  LOAD_METHOD              get_option_dict
              122  LOAD_STR                 'easy_install'
              124  CALL_METHOD_1         1  ''
              126  STORE_FAST               'opts'

 L.  82       128  LOAD_STR                 'allow_hosts'
              130  LOAD_FAST                'opts'
              132  <118>                 0  ''
              134  POP_JUMP_IF_FALSE   144  'to 144'

 L.  83       136  LOAD_GLOBAL              DistutilsError
              138  LOAD_STR                 'the `allow-hosts` option is not supported when using pip to install requirements.'
              140  CALL_FUNCTION_1       1  ''
              142  RAISE_VARARGS_1       1  'exception instance'
            144_0  COME_FROM           134  '134'

 L.  85       144  LOAD_STR                 'PIP_QUIET'
              146  LOAD_GLOBAL              os
              148  LOAD_ATTR                environ
              150  <118>                 0  ''
              152  POP_JUMP_IF_TRUE    164  'to 164'
              154  LOAD_STR                 'PIP_VERBOSE'
              156  LOAD_GLOBAL              os
              158  LOAD_ATTR                environ
              160  <118>                 0  ''
              162  POP_JUMP_IF_FALSE   170  'to 170'
            164_0  COME_FROM           152  '152'

 L.  86       164  LOAD_CONST               False
              166  STORE_FAST               'quiet'
              168  JUMP_FORWARD        174  'to 174'
            170_0  COME_FROM           162  '162'

 L.  88       170  LOAD_CONST               True
              172  STORE_FAST               'quiet'
            174_0  COME_FROM           168  '168'

 L.  89       174  LOAD_STR                 'PIP_INDEX_URL'
              176  LOAD_GLOBAL              os
              178  LOAD_ATTR                environ
              180  <118>                 0  ''
              182  POP_JUMP_IF_FALSE   190  'to 190'

 L.  90       184  LOAD_CONST               None
              186  STORE_FAST               'index_url'
              188  JUMP_FORWARD        216  'to 216'
            190_0  COME_FROM           182  '182'

 L.  91       190  LOAD_STR                 'index_url'
              192  LOAD_FAST                'opts'
              194  <118>                 0  ''
              196  POP_JUMP_IF_FALSE   212  'to 212'

 L.  92       198  LOAD_FAST                'opts'
              200  LOAD_STR                 'index_url'
              202  BINARY_SUBSCR    
              204  LOAD_CONST               1
              206  BINARY_SUBSCR    
              208  STORE_FAST               'index_url'
              210  JUMP_FORWARD        216  'to 216'
            212_0  COME_FROM           196  '196'

 L.  94       212  LOAD_CONST               None
              214  STORE_FAST               'index_url'
            216_0  COME_FROM           210  '210'
            216_1  COME_FROM           188  '188'

 L.  95       216  LOAD_STR                 'find_links'
              218  LOAD_FAST                'opts'
              220  <118>                 0  ''
              222  POP_JUMP_IF_FALSE   250  'to 250'

 L.  96       224  LOAD_GLOBAL              _fixup_find_links
              226  LOAD_FAST                'opts'
              228  LOAD_STR                 'find_links'
              230  BINARY_SUBSCR    
              232  LOAD_CONST               1
              234  BINARY_SUBSCR    
              236  CALL_FUNCTION_1       1  ''
              238  LOAD_CONST               None
              240  LOAD_CONST               None
              242  BUILD_SLICE_2         2 
              244  BINARY_SUBSCR    
              246  STORE_FAST               'find_links'
              248  JUMP_FORWARD        254  'to 254'
            250_0  COME_FROM           222  '222'

 L.  98       250  BUILD_LIST_0          0 
              252  STORE_FAST               'find_links'
            254_0  COME_FROM           248  '248'

 L.  99       254  LOAD_FAST                'dist'
              256  LOAD_ATTR                dependency_links
          258_260  POP_JUMP_IF_FALSE   274  'to 274'

 L. 100       262  LOAD_FAST                'find_links'
              264  LOAD_METHOD              extend
              266  LOAD_FAST                'dist'
              268  LOAD_ATTR                dependency_links
              270  CALL_METHOD_1         1  ''
              272  POP_TOP          
            274_0  COME_FROM           258  '258'

 L. 101       274  LOAD_GLOBAL              os
              276  LOAD_ATTR                path
              278  LOAD_METHOD              realpath
              280  LOAD_FAST                'dist'
              282  LOAD_METHOD              get_egg_cache_dir
              284  CALL_METHOD_0         0  ''
              286  CALL_METHOD_1         1  ''
              288  STORE_FAST               'eggs_dir'

 L. 102       290  LOAD_GLOBAL              pkg_resources
              292  LOAD_METHOD              Environment
              294  CALL_METHOD_0         0  ''
              296  STORE_FAST               'environment'

 L. 103       298  LOAD_GLOBAL              pkg_resources
              300  LOAD_METHOD              find_distributions
              302  LOAD_FAST                'eggs_dir'
              304  CALL_METHOD_1         1  ''
              306  GET_ITER         
            308_0  COME_FROM           330  '330'
            308_1  COME_FROM           318  '318'
              308  FOR_ITER            346  'to 346'
              310  STORE_FAST               'egg_dist'

 L. 104       312  LOAD_FAST                'egg_dist'
              314  LOAD_FAST                'req'
              316  <118>                 0  ''
          318_320  POP_JUMP_IF_FALSE   308  'to 308'
              322  LOAD_FAST                'environment'
              324  LOAD_METHOD              can_add
              326  LOAD_FAST                'egg_dist'
              328  CALL_METHOD_1         1  ''
          330_332  POP_JUMP_IF_FALSE   308  'to 308'

 L. 105       334  LOAD_FAST                'egg_dist'
              336  ROT_TWO          
              338  POP_TOP          
              340  RETURN_VALUE     
          342_344  JUMP_BACK           308  'to 308'

 L. 106       346  LOAD_GLOBAL              TemporaryDirectory
              348  CALL_FUNCTION_0       0  ''
          350_352  SETUP_WITH          672  'to 672'
              354  STORE_FAST               'tmpdir'

 L. 108       356  LOAD_GLOBAL              sys
              358  LOAD_ATTR                executable
              360  LOAD_STR                 '-m'
              362  LOAD_STR                 'pip'

 L. 109       364  LOAD_STR                 '--disable-pip-version-check'

 L. 110       366  LOAD_STR                 'wheel'
              368  LOAD_STR                 '--no-deps'

 L. 111       370  LOAD_STR                 '-w'
              372  LOAD_FAST                'tmpdir'

 L. 107       374  BUILD_LIST_8          8 
              376  STORE_FAST               'cmd'

 L. 113       378  LOAD_FAST                'quiet'
          380_382  POP_JUMP_IF_FALSE   394  'to 394'

 L. 114       384  LOAD_FAST                'cmd'
              386  LOAD_METHOD              append
              388  LOAD_STR                 '--quiet'
              390  CALL_METHOD_1         1  ''
              392  POP_TOP          
            394_0  COME_FROM           380  '380'

 L. 115       394  LOAD_FAST                'index_url'
              396  LOAD_CONST               None
              398  <117>                 1  ''
          400_402  POP_JUMP_IF_FALSE   418  'to 418'

 L. 116       404  LOAD_FAST                'cmd'
              406  LOAD_METHOD              extend
              408  LOAD_STR                 '--index-url'
              410  LOAD_FAST                'index_url'
              412  BUILD_TUPLE_2         2 
              414  CALL_METHOD_1         1  ''
              416  POP_TOP          
            418_0  COME_FROM           400  '400'

 L. 117       418  LOAD_FAST                'find_links'
              420  LOAD_CONST               None
              422  <117>                 1  ''
          424_426  POP_JUMP_IF_FALSE   454  'to 454'

 L. 118       428  LOAD_FAST                'find_links'
              430  GET_ITER         
              432  FOR_ITER            454  'to 454'
              434  STORE_FAST               'link'

 L. 119       436  LOAD_FAST                'cmd'
              438  LOAD_METHOD              extend
              440  LOAD_STR                 '--find-links'
              442  LOAD_FAST                'link'
              444  BUILD_TUPLE_2         2 
              446  CALL_METHOD_1         1  ''
              448  POP_TOP          
          450_452  JUMP_BACK           432  'to 432'
            454_0  COME_FROM           424  '424'

 L. 123       454  LOAD_FAST                'req'
              456  LOAD_ATTR                url
          458_460  POP_JUMP_IF_FALSE   476  'to 476'

 L. 124       462  LOAD_FAST                'cmd'
              464  LOAD_METHOD              append
              466  LOAD_FAST                'req'
              468  LOAD_ATTR                url
              470  CALL_METHOD_1         1  ''
              472  POP_TOP          
              474  JUMP_FORWARD        490  'to 490'
            476_0  COME_FROM           458  '458'

 L. 126       476  LOAD_FAST                'cmd'
              478  LOAD_METHOD              append
              480  LOAD_GLOBAL              str
              482  LOAD_FAST                'req'
              484  CALL_FUNCTION_1       1  ''
              486  CALL_METHOD_1         1  ''
              488  POP_TOP          
            490_0  COME_FROM           474  '474'

 L. 127       490  SETUP_FINALLY       506  'to 506'

 L. 128       492  LOAD_GLOBAL              subprocess
              494  LOAD_METHOD              check_call
              496  LOAD_FAST                'cmd'
              498  CALL_METHOD_1         1  ''
              500  POP_TOP          
              502  POP_BLOCK        
              504  JUMP_FORWARD        560  'to 560'
            506_0  COME_FROM_FINALLY   490  '490'

 L. 129       506  DUP_TOP          
              508  LOAD_GLOBAL              subprocess
              510  LOAD_ATTR                CalledProcessError
          512_514  <121>               558  ''
              516  POP_TOP          
              518  STORE_FAST               'e'
              520  POP_TOP          
              522  SETUP_FINALLY       550  'to 550'

 L. 130       524  LOAD_GLOBAL              DistutilsError
              526  LOAD_GLOBAL              str
              528  LOAD_FAST                'e'
              530  CALL_FUNCTION_1       1  ''
              532  CALL_FUNCTION_1       1  ''
              534  LOAD_FAST                'e'
              536  RAISE_VARARGS_2       2  'exception instance with __cause__'
              538  POP_BLOCK        
              540  POP_EXCEPT       
              542  LOAD_CONST               None
              544  STORE_FAST               'e'
              546  DELETE_FAST              'e'
              548  JUMP_FORWARD        560  'to 560'
            550_0  COME_FROM_FINALLY   522  '522'
              550  LOAD_CONST               None
              552  STORE_FAST               'e'
              554  DELETE_FAST              'e'
              556  <48>             
              558  <48>             
            560_0  COME_FROM           548  '548'
            560_1  COME_FROM           504  '504'

 L. 131       560  LOAD_GLOBAL              Wheel
              562  LOAD_GLOBAL              glob
              564  LOAD_METHOD              glob
              566  LOAD_GLOBAL              os
              568  LOAD_ATTR                path
              570  LOAD_METHOD              join
              572  LOAD_FAST                'tmpdir'
              574  LOAD_STR                 '*.whl'
              576  CALL_METHOD_2         2  ''
              578  CALL_METHOD_1         1  ''
              580  LOAD_CONST               0
              582  BINARY_SUBSCR    
              584  CALL_FUNCTION_1       1  ''
              586  STORE_FAST               'wheel'

 L. 132       588  LOAD_GLOBAL              os
              590  LOAD_ATTR                path
              592  LOAD_METHOD              join
              594  LOAD_FAST                'eggs_dir'
              596  LOAD_FAST                'wheel'
              598  LOAD_METHOD              egg_name
              600  CALL_METHOD_0         0  ''
              602  CALL_METHOD_2         2  ''
              604  STORE_FAST               'dist_location'

 L. 133       606  LOAD_FAST                'wheel'
              608  LOAD_METHOD              install_as_egg
              610  LOAD_FAST                'dist_location'
              612  CALL_METHOD_1         1  ''
              614  POP_TOP          

 L. 134       616  LOAD_GLOBAL              pkg_resources
              618  LOAD_METHOD              PathMetadata

 L. 135       620  LOAD_FAST                'dist_location'
              622  LOAD_GLOBAL              os
              624  LOAD_ATTR                path
              626  LOAD_METHOD              join
              628  LOAD_FAST                'dist_location'
              630  LOAD_STR                 'EGG-INFO'
              632  CALL_METHOD_2         2  ''

 L. 134       634  CALL_METHOD_2         2  ''
              636  STORE_FAST               'dist_metadata'

 L. 136       638  LOAD_GLOBAL              pkg_resources
              640  LOAD_ATTR                Distribution
              642  LOAD_ATTR                from_filename

 L. 137       644  LOAD_FAST                'dist_location'
              646  LOAD_FAST                'dist_metadata'

 L. 136       648  LOAD_CONST               ('metadata',)
              650  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              652  STORE_FAST               'dist'

 L. 138       654  LOAD_FAST                'dist'
              656  POP_BLOCK        
              658  ROT_TWO          
              660  LOAD_CONST               None
              662  DUP_TOP          
              664  DUP_TOP          
              666  CALL_FUNCTION_3       3  ''
              668  POP_TOP          
              670  RETURN_VALUE     
            672_0  COME_FROM_WITH      350  '350'
              672  <49>             
          674_676  POP_JUMP_IF_TRUE    680  'to 680'
              678  <48>             
            680_0  COME_FROM           674  '674'
              680  POP_TOP          
              682  POP_TOP          
              684  POP_TOP          
              686  POP_EXCEPT       
              688  POP_TOP          

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