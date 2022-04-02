# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: setuptools\installer.py
import glob, os, subprocess, sys
from distutils import log
from distutils.errors import DistutilsError
import pkg_resources
import setuptools.command.easy_install as easy_install
from setuptools.extern import six
from setuptools.wheel import Wheel
from .py31compat import TemporaryDirectory

def _fixup_find_links(find_links):
    """Ensure find-links option end-up being a list of strings."""
    if isinstance(find_links, six.string_types):
        return find_links.split()
    assert isinstance(find_links, (tuple, list))
    return find_links


def _legacy_fetch_build_egg(dist, req):
    """Fetch an egg needed for building.

    Legacy path using EasyInstall.
    """
    tmp_dist = dist.__class__({'script_args': ['easy_install']})
    opts = tmp_dist.get_option_dict('easy_install')
    opts.clear()
    opts.update(((
     k, v) for k, v in dist.get_option_dict('easy_install').items() if k in ('find_links',
                                                                             'site_dirs',
                                                                             'index_url',
                                                                             'optimize',
                                                                             'site_dirs',
                                                                             'allow_hosts')))
    if dist.dependency_links:
        links = dist.dependency_links[:]
        if 'find_links' in opts:
            links = _fixup_find_links(opts['find_links'][1]) + links
        opts['find_links'] = (
         'setup', links)
    install_dir = dist.get_egg_cache_dir()
    cmd = easy_install(tmp_dist,
      args=['x'], install_dir=install_dir, exclude_scripts=True,
      always_copy=False,
      build_directory=None,
      editable=False,
      upgrade=False,
      multi_version=True,
      no_report=True,
      user=False)
    cmd.ensure_finalized()
    return cmd.easy_install(req)


def fetch_build_egg--- This code section failed: ---

 L.  61         0  SETUP_FINALLY        16  'to 16'

 L.  62         2  LOAD_GLOBAL              pkg_resources
                4  LOAD_METHOD              get_distribution
                6  LOAD_STR                 'pip'
                8  CALL_METHOD_1         1  ''
               10  POP_TOP          
               12  POP_BLOCK        
               14  JUMP_FORWARD         62  'to 62'
             16_0  COME_FROM_FINALLY     0  '0'

 L.  63        16  DUP_TOP          
               18  LOAD_GLOBAL              pkg_resources
               20  LOAD_ATTR                DistributionNotFound
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    60  'to 60'
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L.  64        32  LOAD_FAST                'dist'
               34  LOAD_METHOD              announce

 L.  65        36  LOAD_STR                 'WARNING: The pip package is not available, falling back to EasyInstall for handling setup_requires/test_requires; this is deprecated and will be removed in a future version.'

 L.  68        38  LOAD_GLOBAL              log
               40  LOAD_ATTR                WARN

 L.  64        42  CALL_METHOD_2         2  ''
               44  POP_TOP          

 L.  70        46  LOAD_GLOBAL              _legacy_fetch_build_egg
               48  LOAD_FAST                'dist'
               50  LOAD_FAST                'req'
               52  CALL_FUNCTION_2       2  ''
               54  ROT_FOUR         
               56  POP_EXCEPT       
               58  RETURN_VALUE     
             60_0  COME_FROM            24  '24'
               60  END_FINALLY      
             62_0  COME_FROM            14  '14'

 L.  72        62  SETUP_FINALLY        78  'to 78'

 L.  73        64  LOAD_GLOBAL              pkg_resources
               66  LOAD_METHOD              get_distribution
               68  LOAD_STR                 'wheel'
               70  CALL_METHOD_1         1  ''
               72  POP_TOP          
               74  POP_BLOCK        
               76  JUMP_FORWARD        114  'to 114'
             78_0  COME_FROM_FINALLY    62  '62'

 L.  74        78  DUP_TOP          
               80  LOAD_GLOBAL              pkg_resources
               82  LOAD_ATTR                DistributionNotFound
               84  COMPARE_OP               exception-match
               86  POP_JUMP_IF_FALSE   112  'to 112'
               88  POP_TOP          
               90  POP_TOP          
               92  POP_TOP          

 L.  75        94  LOAD_FAST                'dist'
               96  LOAD_METHOD              announce
               98  LOAD_STR                 'WARNING: The wheel package is not available.'
              100  LOAD_GLOBAL              log
              102  LOAD_ATTR                WARN
              104  CALL_METHOD_2         2  ''
              106  POP_TOP          
              108  POP_EXCEPT       
              110  JUMP_FORWARD        114  'to 114'
            112_0  COME_FROM            86  '86'
              112  END_FINALLY      
            114_0  COME_FROM           110  '110'
            114_1  COME_FROM            76  '76'

 L.  77       114  LOAD_GLOBAL              strip_marker
              116  LOAD_FAST                'req'
              118  CALL_FUNCTION_1       1  ''
              120  STORE_FAST               'req'

 L.  81       122  LOAD_FAST                'dist'
              124  LOAD_METHOD              get_option_dict
              126  LOAD_STR                 'easy_install'
              128  CALL_METHOD_1         1  ''
              130  STORE_FAST               'opts'

 L.  82       132  LOAD_STR                 'allow_hosts'
              134  LOAD_FAST                'opts'
              136  COMPARE_OP               in
              138  POP_JUMP_IF_FALSE   148  'to 148'

 L.  83       140  LOAD_GLOBAL              DistutilsError
              142  LOAD_STR                 'the `allow-hosts` option is not supported when using pip to install requirements.'
              144  CALL_FUNCTION_1       1  ''
              146  RAISE_VARARGS_1       1  'exception instance'
            148_0  COME_FROM           138  '138'

 L.  85       148  LOAD_STR                 'PIP_QUIET'
              150  LOAD_GLOBAL              os
              152  LOAD_ATTR                environ
              154  COMPARE_OP               in
              156  POP_JUMP_IF_TRUE    168  'to 168'
              158  LOAD_STR                 'PIP_VERBOSE'
              160  LOAD_GLOBAL              os
              162  LOAD_ATTR                environ
              164  COMPARE_OP               in
              166  POP_JUMP_IF_FALSE   174  'to 174'
            168_0  COME_FROM           156  '156'

 L.  86       168  LOAD_CONST               False
              170  STORE_FAST               'quiet'
              172  JUMP_FORWARD        178  'to 178'
            174_0  COME_FROM           166  '166'

 L.  88       174  LOAD_CONST               True
              176  STORE_FAST               'quiet'
            178_0  COME_FROM           172  '172'

 L.  89       178  LOAD_STR                 'PIP_INDEX_URL'
              180  LOAD_GLOBAL              os
              182  LOAD_ATTR                environ
              184  COMPARE_OP               in
              186  POP_JUMP_IF_FALSE   194  'to 194'

 L.  90       188  LOAD_CONST               None
              190  STORE_FAST               'index_url'
              192  JUMP_FORWARD        220  'to 220'
            194_0  COME_FROM           186  '186'

 L.  91       194  LOAD_STR                 'index_url'
              196  LOAD_FAST                'opts'
              198  COMPARE_OP               in
              200  POP_JUMP_IF_FALSE   216  'to 216'

 L.  92       202  LOAD_FAST                'opts'
              204  LOAD_STR                 'index_url'
              206  BINARY_SUBSCR    
              208  LOAD_CONST               1
              210  BINARY_SUBSCR    
              212  STORE_FAST               'index_url'
              214  JUMP_FORWARD        220  'to 220'
            216_0  COME_FROM           200  '200'

 L.  94       216  LOAD_CONST               None
              218  STORE_FAST               'index_url'
            220_0  COME_FROM           214  '214'
            220_1  COME_FROM           192  '192'

 L.  95       220  LOAD_STR                 'find_links'
              222  LOAD_FAST                'opts'
              224  COMPARE_OP               in
          226_228  POP_JUMP_IF_FALSE   256  'to 256'

 L.  96       230  LOAD_GLOBAL              _fixup_find_links
              232  LOAD_FAST                'opts'
              234  LOAD_STR                 'find_links'
              236  BINARY_SUBSCR    
              238  LOAD_CONST               1
              240  BINARY_SUBSCR    
              242  CALL_FUNCTION_1       1  ''
              244  LOAD_CONST               None
              246  LOAD_CONST               None
              248  BUILD_SLICE_2         2 
              250  BINARY_SUBSCR    
              252  STORE_FAST               'find_links'
              254  JUMP_FORWARD        260  'to 260'
            256_0  COME_FROM           226  '226'

 L.  98       256  BUILD_LIST_0          0 
              258  STORE_FAST               'find_links'
            260_0  COME_FROM           254  '254'

 L.  99       260  LOAD_FAST                'dist'
              262  LOAD_ATTR                dependency_links
          264_266  POP_JUMP_IF_FALSE   280  'to 280'

 L. 100       268  LOAD_FAST                'find_links'
              270  LOAD_METHOD              extend
              272  LOAD_FAST                'dist'
              274  LOAD_ATTR                dependency_links
              276  CALL_METHOD_1         1  ''
              278  POP_TOP          
            280_0  COME_FROM           264  '264'

 L. 101       280  LOAD_GLOBAL              os
              282  LOAD_ATTR                path
              284  LOAD_METHOD              realpath
              286  LOAD_FAST                'dist'
              288  LOAD_METHOD              get_egg_cache_dir
              290  CALL_METHOD_0         0  ''
              292  CALL_METHOD_1         1  ''
              294  STORE_FAST               'eggs_dir'

 L. 102       296  LOAD_GLOBAL              pkg_resources
              298  LOAD_METHOD              Environment
              300  CALL_METHOD_0         0  ''
              302  STORE_FAST               'environment'

 L. 103       304  LOAD_GLOBAL              pkg_resources
              306  LOAD_METHOD              find_distributions
              308  LOAD_FAST                'eggs_dir'
              310  CALL_METHOD_1         1  ''
              312  GET_ITER         
            314_0  COME_FROM           336  '336'
            314_1  COME_FROM           324  '324'
              314  FOR_ITER            352  'to 352'
              316  STORE_FAST               'egg_dist'

 L. 104       318  LOAD_FAST                'egg_dist'
              320  LOAD_FAST                'req'
              322  COMPARE_OP               in
          324_326  POP_JUMP_IF_FALSE   314  'to 314'
              328  LOAD_FAST                'environment'
              330  LOAD_METHOD              can_add
              332  LOAD_FAST                'egg_dist'
              334  CALL_METHOD_1         1  ''
          336_338  POP_JUMP_IF_FALSE   314  'to 314'

 L. 105       340  LOAD_FAST                'egg_dist'
              342  ROT_TWO          
              344  POP_TOP          
              346  RETURN_VALUE     
          348_350  JUMP_BACK           314  'to 314'

 L. 106       352  LOAD_GLOBAL              TemporaryDirectory
              354  CALL_FUNCTION_0       0  ''
          356_358  SETUP_WITH          674  'to 674'
              360  STORE_FAST               'tmpdir'

 L. 108       362  LOAD_GLOBAL              sys
              364  LOAD_ATTR                executable

 L. 108       366  LOAD_STR                 '-m'

 L. 108       368  LOAD_STR                 'pip'

 L. 109       370  LOAD_STR                 '--disable-pip-version-check'

 L. 110       372  LOAD_STR                 'wheel'

 L. 110       374  LOAD_STR                 '--no-deps'

 L. 111       376  LOAD_STR                 '-w'

 L. 111       378  LOAD_FAST                'tmpdir'

 L. 107       380  BUILD_LIST_8          8 
              382  STORE_FAST               'cmd'

 L. 113       384  LOAD_FAST                'quiet'
          386_388  POP_JUMP_IF_FALSE   400  'to 400'

 L. 114       390  LOAD_FAST                'cmd'
              392  LOAD_METHOD              append
              394  LOAD_STR                 '--quiet'
              396  CALL_METHOD_1         1  ''
              398  POP_TOP          
            400_0  COME_FROM           386  '386'

 L. 115       400  LOAD_FAST                'index_url'
              402  LOAD_CONST               None
              404  COMPARE_OP               is-not
          406_408  POP_JUMP_IF_FALSE   424  'to 424'

 L. 116       410  LOAD_FAST                'cmd'
              412  LOAD_METHOD              extend
              414  LOAD_STR                 '--index-url'
              416  LOAD_FAST                'index_url'
              418  BUILD_TUPLE_2         2 
              420  CALL_METHOD_1         1  ''
              422  POP_TOP          
            424_0  COME_FROM           406  '406'

 L. 117       424  LOAD_FAST                'find_links'
              426  LOAD_CONST               None
              428  COMPARE_OP               is-not
          430_432  POP_JUMP_IF_FALSE   460  'to 460'

 L. 118       434  LOAD_FAST                'find_links'
              436  GET_ITER         
              438  FOR_ITER            460  'to 460'
              440  STORE_FAST               'link'

 L. 119       442  LOAD_FAST                'cmd'
              444  LOAD_METHOD              extend
              446  LOAD_STR                 '--find-links'
              448  LOAD_FAST                'link'
              450  BUILD_TUPLE_2         2 
              452  CALL_METHOD_1         1  ''
              454  POP_TOP          
          456_458  JUMP_BACK           438  'to 438'
            460_0  COME_FROM           430  '430'

 L. 123       460  LOAD_FAST                'req'
              462  LOAD_ATTR                url
          464_466  POP_JUMP_IF_FALSE   482  'to 482'

 L. 124       468  LOAD_FAST                'cmd'
              470  LOAD_METHOD              append
              472  LOAD_FAST                'req'
              474  LOAD_ATTR                url
              476  CALL_METHOD_1         1  ''
              478  POP_TOP          
              480  JUMP_FORWARD        496  'to 496'
            482_0  COME_FROM           464  '464'

 L. 126       482  LOAD_FAST                'cmd'
              484  LOAD_METHOD              append
              486  LOAD_GLOBAL              str
              488  LOAD_FAST                'req'
              490  CALL_FUNCTION_1       1  ''
              492  CALL_METHOD_1         1  ''
              494  POP_TOP          
            496_0  COME_FROM           480  '480'

 L. 127       496  SETUP_FINALLY       512  'to 512'

 L. 128       498  LOAD_GLOBAL              subprocess
              500  LOAD_METHOD              check_call
              502  LOAD_FAST                'cmd'
              504  CALL_METHOD_1         1  ''
              506  POP_TOP          
              508  POP_BLOCK        
              510  JUMP_FORWARD        564  'to 564'
            512_0  COME_FROM_FINALLY   496  '496'

 L. 129       512  DUP_TOP          
              514  LOAD_GLOBAL              subprocess
              516  LOAD_ATTR                CalledProcessError
              518  COMPARE_OP               exception-match
          520_522  POP_JUMP_IF_FALSE   562  'to 562'
              524  POP_TOP          
              526  STORE_FAST               'e'
              528  POP_TOP          
              530  SETUP_FINALLY       550  'to 550'

 L. 130       532  LOAD_GLOBAL              DistutilsError
              534  LOAD_GLOBAL              str
              536  LOAD_FAST                'e'
              538  CALL_FUNCTION_1       1  ''
              540  CALL_FUNCTION_1       1  ''
              542  LOAD_FAST                'e'
              544  RAISE_VARARGS_2       2  'exception instance with __cause__'
              546  POP_BLOCK        
              548  BEGIN_FINALLY    
            550_0  COME_FROM_FINALLY   530  '530'
              550  LOAD_CONST               None
              552  STORE_FAST               'e'
              554  DELETE_FAST              'e'
              556  END_FINALLY      
              558  POP_EXCEPT       
              560  JUMP_FORWARD        564  'to 564'
            562_0  COME_FROM           520  '520'
              562  END_FINALLY      
            564_0  COME_FROM           560  '560'
            564_1  COME_FROM           510  '510'

 L. 131       564  LOAD_GLOBAL              Wheel
              566  LOAD_GLOBAL              glob
              568  LOAD_METHOD              glob
              570  LOAD_GLOBAL              os
              572  LOAD_ATTR                path
              574  LOAD_METHOD              join
              576  LOAD_FAST                'tmpdir'
              578  LOAD_STR                 '*.whl'
              580  CALL_METHOD_2         2  ''
              582  CALL_METHOD_1         1  ''
              584  LOAD_CONST               0
              586  BINARY_SUBSCR    
              588  CALL_FUNCTION_1       1  ''
              590  STORE_FAST               'wheel'

 L. 132       592  LOAD_GLOBAL              os
              594  LOAD_ATTR                path
              596  LOAD_METHOD              join
              598  LOAD_FAST                'eggs_dir'
              600  LOAD_FAST                'wheel'
              602  LOAD_METHOD              egg_name
              604  CALL_METHOD_0         0  ''
              606  CALL_METHOD_2         2  ''
              608  STORE_FAST               'dist_location'

 L. 133       610  LOAD_FAST                'wheel'
              612  LOAD_METHOD              install_as_egg
              614  LOAD_FAST                'dist_location'
              616  CALL_METHOD_1         1  ''
              618  POP_TOP          

 L. 134       620  LOAD_GLOBAL              pkg_resources
              622  LOAD_METHOD              PathMetadata

 L. 135       624  LOAD_FAST                'dist_location'

 L. 135       626  LOAD_GLOBAL              os
              628  LOAD_ATTR                path
              630  LOAD_METHOD              join
              632  LOAD_FAST                'dist_location'
              634  LOAD_STR                 'EGG-INFO'
              636  CALL_METHOD_2         2  ''

 L. 134       638  CALL_METHOD_2         2  ''
              640  STORE_FAST               'dist_metadata'

 L. 136       642  LOAD_GLOBAL              pkg_resources
              644  LOAD_ATTR                Distribution
              646  LOAD_ATTR                from_filename

 L. 137       648  LOAD_FAST                'dist_location'

 L. 137       650  LOAD_FAST                'dist_metadata'

 L. 136       652  LOAD_CONST               ('metadata',)
              654  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              656  STORE_FAST               'dist'

 L. 138       658  LOAD_FAST                'dist'
              660  POP_BLOCK        
              662  ROT_TWO          
              664  BEGIN_FINALLY    
              666  WITH_CLEANUP_START
              668  WITH_CLEANUP_FINISH
              670  POP_FINALLY           0  ''
              672  RETURN_VALUE     
            674_0  COME_FROM_WITH      356  '356'
              674  WITH_CLEANUP_START
              676  WITH_CLEANUP_FINISH
              678  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 662


def strip_marker(req):
    """
    Return a new requirement without the environment marker to avoid
    calling pip with something like `babel; extra == "i18n"`, which
    would always be ignored.
    """
    req = pkg_resources.Requirement.parse(str(req))
    req.marker = None
    return req