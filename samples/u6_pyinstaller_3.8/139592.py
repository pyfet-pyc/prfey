# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: setuptools\installer.py
import glob, os, subprocess, sys, tempfile
from distutils import log
from distutils.errors import DistutilsError
import pkg_resources
from setuptools.wheel import Wheel

def _fixup_find_links(find_links):
    """Ensure find-links option end-up being a list of strings."""
    if isinstance(find_links, str):
        return find_links.split()
    assert isinstance(find_links, (tuple, list))
    return find_links


def fetch_build_egg--- This code section failed: ---

 L.  26         0  SETUP_FINALLY        16  'to 16'

 L.  27         2  LOAD_GLOBAL              pkg_resources
                4  LOAD_METHOD              get_distribution
                6  LOAD_STR                 'wheel'
                8  CALL_METHOD_1         1  ''
               10  POP_TOP          
               12  POP_BLOCK        
               14  JUMP_FORWARD         52  'to 52'
             16_0  COME_FROM_FINALLY     0  '0'

 L.  28        16  DUP_TOP          
               18  LOAD_GLOBAL              pkg_resources
               20  LOAD_ATTR                DistributionNotFound
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    50  'to 50'
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L.  29        32  LOAD_FAST                'dist'
               34  LOAD_METHOD              announce
               36  LOAD_STR                 'WARNING: The wheel package is not available.'
               38  LOAD_GLOBAL              log
               40  LOAD_ATTR                WARN
               42  CALL_METHOD_2         2  ''
               44  POP_TOP          
               46  POP_EXCEPT       
               48  JUMP_FORWARD         52  'to 52'
             50_0  COME_FROM            24  '24'
               50  END_FINALLY      
             52_0  COME_FROM            48  '48'
             52_1  COME_FROM            14  '14'

 L.  31        52  LOAD_GLOBAL              strip_marker
               54  LOAD_FAST                'req'
               56  CALL_FUNCTION_1       1  ''
               58  STORE_FAST               'req'

 L.  35        60  LOAD_FAST                'dist'
               62  LOAD_METHOD              get_option_dict
               64  LOAD_STR                 'easy_install'
               66  CALL_METHOD_1         1  ''
               68  STORE_FAST               'opts'

 L.  36        70  LOAD_STR                 'allow_hosts'
               72  LOAD_FAST                'opts'
               74  COMPARE_OP               in
               76  POP_JUMP_IF_FALSE    86  'to 86'

 L.  37        78  LOAD_GLOBAL              DistutilsError
               80  LOAD_STR                 'the `allow-hosts` option is not supported when using pip to install requirements.'
               82  CALL_FUNCTION_1       1  ''
               84  RAISE_VARARGS_1       1  'exception instance'
             86_0  COME_FROM            76  '76'

 L.  39        86  LOAD_STR                 'PIP_QUIET'
               88  LOAD_GLOBAL              os
               90  LOAD_ATTR                environ
               92  COMPARE_OP               not-in
               94  JUMP_IF_FALSE_OR_POP   104  'to 104'
               96  LOAD_STR                 'PIP_VERBOSE'
               98  LOAD_GLOBAL              os
              100  LOAD_ATTR                environ
              102  COMPARE_OP               not-in
            104_0  COME_FROM            94  '94'
              104  STORE_FAST               'quiet'

 L.  40       106  LOAD_STR                 'PIP_INDEX_URL'
              108  LOAD_GLOBAL              os
              110  LOAD_ATTR                environ
              112  COMPARE_OP               in
              114  POP_JUMP_IF_FALSE   122  'to 122'

 L.  41       116  LOAD_CONST               None
              118  STORE_FAST               'index_url'
              120  JUMP_FORWARD        148  'to 148'
            122_0  COME_FROM           114  '114'

 L.  42       122  LOAD_STR                 'index_url'
              124  LOAD_FAST                'opts'
              126  COMPARE_OP               in
              128  POP_JUMP_IF_FALSE   144  'to 144'

 L.  43       130  LOAD_FAST                'opts'
              132  LOAD_STR                 'index_url'
              134  BINARY_SUBSCR    
              136  LOAD_CONST               1
              138  BINARY_SUBSCR    
              140  STORE_FAST               'index_url'
              142  JUMP_FORWARD        148  'to 148'
            144_0  COME_FROM           128  '128'

 L.  45       144  LOAD_CONST               None
              146  STORE_FAST               'index_url'
            148_0  COME_FROM           142  '142'
            148_1  COME_FROM           120  '120'

 L.  47       148  LOAD_STR                 'find_links'
              150  LOAD_FAST                'opts'
              152  COMPARE_OP               in
              154  POP_JUMP_IF_FALSE   180  'to 180'
              156  LOAD_GLOBAL              _fixup_find_links
              158  LOAD_FAST                'opts'
              160  LOAD_STR                 'find_links'
              162  BINARY_SUBSCR    
              164  LOAD_CONST               1
              166  BINARY_SUBSCR    
              168  CALL_FUNCTION_1       1  ''
              170  LOAD_CONST               None
              172  LOAD_CONST               None
              174  BUILD_SLICE_2         2 
              176  BINARY_SUBSCR    
              178  JUMP_FORWARD        182  'to 182'
            180_0  COME_FROM           154  '154'

 L.  48       180  BUILD_LIST_0          0 
            182_0  COME_FROM           178  '178'

 L.  46       182  STORE_FAST               'find_links'

 L.  50       184  LOAD_FAST                'dist'
              186  LOAD_ATTR                dependency_links
              188  POP_JUMP_IF_FALSE   202  'to 202'

 L.  51       190  LOAD_FAST                'find_links'
              192  LOAD_METHOD              extend
              194  LOAD_FAST                'dist'
              196  LOAD_ATTR                dependency_links
              198  CALL_METHOD_1         1  ''
              200  POP_TOP          
            202_0  COME_FROM           188  '188'

 L.  52       202  LOAD_GLOBAL              os
              204  LOAD_ATTR                path
              206  LOAD_METHOD              realpath
              208  LOAD_FAST                'dist'
              210  LOAD_METHOD              get_egg_cache_dir
              212  CALL_METHOD_0         0  ''
              214  CALL_METHOD_1         1  ''
              216  STORE_FAST               'eggs_dir'

 L.  53       218  LOAD_GLOBAL              pkg_resources
              220  LOAD_METHOD              Environment
              222  CALL_METHOD_0         0  ''
              224  STORE_FAST               'environment'

 L.  54       226  LOAD_GLOBAL              pkg_resources
              228  LOAD_METHOD              find_distributions
              230  LOAD_FAST                'eggs_dir'
              232  CALL_METHOD_1         1  ''
              234  GET_ITER         
            236_0  COME_FROM           256  '256'
            236_1  COME_FROM           246  '246'
              236  FOR_ITER            268  'to 268'
              238  STORE_FAST               'egg_dist'

 L.  55       240  LOAD_FAST                'egg_dist'
              242  LOAD_FAST                'req'
              244  COMPARE_OP               in
              246  POP_JUMP_IF_FALSE   236  'to 236'
              248  LOAD_FAST                'environment'
              250  LOAD_METHOD              can_add
              252  LOAD_FAST                'egg_dist'
              254  CALL_METHOD_1         1  ''
              256  POP_JUMP_IF_FALSE   236  'to 236'

 L.  56       258  LOAD_FAST                'egg_dist'
              260  ROT_TWO          
              262  POP_TOP          
              264  RETURN_VALUE     
              266  JUMP_BACK           236  'to 236'

 L.  57       268  LOAD_GLOBAL              tempfile
              270  LOAD_METHOD              TemporaryDirectory
              272  CALL_METHOD_0         0  ''
          274_276  SETUP_WITH          574  'to 574'
              278  STORE_FAST               'tmpdir'

 L.  59       280  LOAD_GLOBAL              sys
              282  LOAD_ATTR                executable

 L.  59       284  LOAD_STR                 '-m'

 L.  59       286  LOAD_STR                 'pip'

 L.  60       288  LOAD_STR                 '--disable-pip-version-check'

 L.  61       290  LOAD_STR                 'wheel'

 L.  61       292  LOAD_STR                 '--no-deps'

 L.  62       294  LOAD_STR                 '-w'

 L.  62       296  LOAD_FAST                'tmpdir'

 L.  58       298  BUILD_LIST_8          8 
              300  STORE_FAST               'cmd'

 L.  64       302  LOAD_FAST                'quiet'
          304_306  POP_JUMP_IF_FALSE   318  'to 318'

 L.  65       308  LOAD_FAST                'cmd'
              310  LOAD_METHOD              append
              312  LOAD_STR                 '--quiet'
              314  CALL_METHOD_1         1  ''
              316  POP_TOP          
            318_0  COME_FROM           304  '304'

 L.  66       318  LOAD_FAST                'index_url'
              320  LOAD_CONST               None
              322  COMPARE_OP               is-not
          324_326  POP_JUMP_IF_FALSE   342  'to 342'

 L.  67       328  LOAD_FAST                'cmd'
              330  LOAD_METHOD              extend
              332  LOAD_STR                 '--index-url'
              334  LOAD_FAST                'index_url'
              336  BUILD_TUPLE_2         2 
              338  CALL_METHOD_1         1  ''
              340  POP_TOP          
            342_0  COME_FROM           324  '324'

 L.  68       342  LOAD_FAST                'find_links'
          344_346  JUMP_IF_TRUE_OR_POP   350  'to 350'
              348  BUILD_LIST_0          0 
            350_0  COME_FROM           344  '344'
              350  GET_ITER         
              352  FOR_ITER            374  'to 374'
              354  STORE_FAST               'link'

 L.  69       356  LOAD_FAST                'cmd'
              358  LOAD_METHOD              extend
              360  LOAD_STR                 '--find-links'
              362  LOAD_FAST                'link'
              364  BUILD_TUPLE_2         2 
              366  CALL_METHOD_1         1  ''
              368  POP_TOP          
          370_372  JUMP_BACK           352  'to 352'

 L.  73       374  LOAD_FAST                'cmd'
              376  LOAD_METHOD              append
              378  LOAD_FAST                'req'
              380  LOAD_ATTR                url
          382_384  JUMP_IF_TRUE_OR_POP   392  'to 392'
              386  LOAD_GLOBAL              str
              388  LOAD_FAST                'req'
              390  CALL_FUNCTION_1       1  ''
            392_0  COME_FROM           382  '382'
              392  CALL_METHOD_1         1  ''
              394  POP_TOP          

 L.  74       396  SETUP_FINALLY       412  'to 412'

 L.  75       398  LOAD_GLOBAL              subprocess
              400  LOAD_METHOD              check_call
              402  LOAD_FAST                'cmd'
              404  CALL_METHOD_1         1  ''
              406  POP_TOP          
              408  POP_BLOCK        
              410  JUMP_FORWARD        464  'to 464'
            412_0  COME_FROM_FINALLY   396  '396'

 L.  76       412  DUP_TOP          
              414  LOAD_GLOBAL              subprocess
              416  LOAD_ATTR                CalledProcessError
              418  COMPARE_OP               exception-match
          420_422  POP_JUMP_IF_FALSE   462  'to 462'
              424  POP_TOP          
              426  STORE_FAST               'e'
              428  POP_TOP          
              430  SETUP_FINALLY       450  'to 450'

 L.  77       432  LOAD_GLOBAL              DistutilsError
              434  LOAD_GLOBAL              str
              436  LOAD_FAST                'e'
              438  CALL_FUNCTION_1       1  ''
              440  CALL_FUNCTION_1       1  ''
              442  LOAD_FAST                'e'
              444  RAISE_VARARGS_2       2  'exception instance with __cause__'
              446  POP_BLOCK        
              448  BEGIN_FINALLY    
            450_0  COME_FROM_FINALLY   430  '430'
              450  LOAD_CONST               None
              452  STORE_FAST               'e'
              454  DELETE_FAST              'e'
              456  END_FINALLY      
              458  POP_EXCEPT       
              460  JUMP_FORWARD        464  'to 464'
            462_0  COME_FROM           420  '420'
              462  END_FINALLY      
            464_0  COME_FROM           460  '460'
            464_1  COME_FROM           410  '410'

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

 L.  82       526  LOAD_GLOBAL              os
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

 L.  84       550  LOAD_FAST                'dist_metadata'

 L.  83       552  LOAD_CONST               ('metadata',)
              554  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              556  STORE_FAST               'dist'

 L.  85       558  LOAD_FAST                'dist'
              560  POP_BLOCK        
              562  ROT_TWO          
              564  BEGIN_FINALLY    
              566  WITH_CLEANUP_START
              568  WITH_CLEANUP_FINISH
              570  POP_FINALLY           0  ''
              572  RETURN_VALUE     
            574_0  COME_FROM_WITH      274  '274'
              574  WITH_CLEANUP_START
              576  WITH_CLEANUP_FINISH
              578  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 562


def strip_marker(req):
    """
    Return a new requirement without the environment marker to avoid
    calling pip with something like `babel; extra == "i18n"`, which
    would always be ignored.
    """
    req = pkg_resources.Requirement.parsestr(req)
    req.marker = None
    return req