# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: gallery_dl\__init__.py
from __future__ import unicode_literals, print_function
__author__ = 'Mike Fährmann'
__copyright__ = 'Copyright 2014-2020 Mike Fährmann'
__license__ = 'GPLv2'
__maintainer__ = 'Mike Fährmann'
__email__ = 'mike_faehrmann@web.de'
import sys
if sys.hexversion < 50593792:
    sys.exit('Python 3.4+ required')
import json, logging
from . import version, config, option, output, extractor, job, util, exception
__version__ = version.__version__

def progress(urls, pformat):
    """Wrapper around urls to output a simple progress indicator"""
    if pformat is True:
        pformat = '[{current}/{total}] {url}'
    pinfo = {'total': len(urls)}
    for pinfo['current'], pinfo['url'] in enumerate(urls, 1):
        print((pformat.format_map(pinfo)), file=(sys.stderr))
        yield pinfo['url']


def parse_inputfile(file, log):
    """Filter and process strings from an input file.

    Lines starting with '#' and empty lines will be ignored.
    Lines starting with '-' will be interpreted as a key-value pair separated
      by an '='. where 'key' is a dot-separated option name and 'value' is a
      JSON-parsable value for it. These config options will be applied while
      processing the next URL.
    Lines starting with '-G' are the same as above, except these options will
      be valid for all following URLs, i.e. they are Global.
    Everything else will be used as potential URL.

    Example input file:

    # settings global options
    -G base-directory = "/tmp/"
    -G skip = false

    # setting local options for the next URL
    -filename="spaces_are_optional.jpg"
    -skip    = true

    https://example.org/

    # next URL uses default filename and 'skip' is false.
    https://example.com/index.htm
    """
    gconf = []
    lconf = []
    for line in file:
        line = line.strip()
        if line:
            if line[0] == '#':
                continue
            elif line[0] == '-':
                if len(line) >= 2:
                    if line[1] == 'G':
                        conf = gconf
                        line = line[2:]
                    else:
                        conf = lconf
                        line = line[1:]
                    key, sep, value = line.partition('=')
                    if not sep:
                        log.warning('input file: invalid <key>=<value> pair: %s', line)
                        continue
                else:
                    try:
                        value = json.loads(value.strip())
                    except ValueError as exc:
                        try:
                            log.warning("input file: unable to parse '%s': %s", value, exc)
                            continue
                        finally:
                            exc = None
                            del exc

                key = key.strip().split('.')
                conf.append((key[:-1], key[(-1)], value))
            elif gconf or lconf:
                yield util.ExtendedUrl(line, gconf, lconf)
                gconf = []
                lconf = []
            else:
                yield line


def main--- This code section failed: ---

 L. 110       0_2  SETUP_EXCEPT       1310  'to 1310'

 L. 111         4  LOAD_GLOBAL              sys
                6  LOAD_ATTR                stdout
                8  POP_JUMP_IF_FALSE    34  'to 34'
               10  LOAD_GLOBAL              sys
               12  LOAD_ATTR                stdout
               14  LOAD_ATTR                encoding
               16  LOAD_METHOD              lower
               18  CALL_METHOD_0         0  '0 positional arguments'
               20  LOAD_STR                 'utf-8'
               22  COMPARE_OP               !=
               24  POP_JUMP_IF_FALSE    34  'to 34'

 L. 112        26  LOAD_GLOBAL              output
               28  LOAD_METHOD              replace_std_streams
               30  CALL_METHOD_0         0  '0 positional arguments'
               32  POP_TOP          
             34_0  COME_FROM            24  '24'
             34_1  COME_FROM             8  '8'

 L. 114        34  LOAD_GLOBAL              option
               36  LOAD_METHOD              build_parser
               38  CALL_METHOD_0         0  '0 positional arguments'
               40  STORE_FAST               'parser'

 L. 115        42  LOAD_FAST                'parser'
               44  LOAD_METHOD              parse_args
               46  CALL_METHOD_0         0  '0 positional arguments'
               48  STORE_FAST               'args'

 L. 116        50  LOAD_GLOBAL              output
               52  LOAD_METHOD              initialize_logging
               54  LOAD_FAST                'args'
               56  LOAD_ATTR                loglevel
               58  CALL_METHOD_1         1  '1 positional argument'
               60  STORE_FAST               'log'

 L. 119        62  LOAD_FAST                'args'
               64  LOAD_ATTR                load_config
               66  POP_JUMP_IF_FALSE    76  'to 76'

 L. 120        68  LOAD_GLOBAL              config
               70  LOAD_METHOD              load
               72  CALL_METHOD_0         0  '0 positional arguments'
               74  POP_TOP          
             76_0  COME_FROM            66  '66'

 L. 121        76  LOAD_FAST                'args'
               78  LOAD_ATTR                cfgfiles
               80  POP_JUMP_IF_FALSE    98  'to 98'

 L. 122        82  LOAD_GLOBAL              config
               84  LOAD_ATTR                load
               86  LOAD_FAST                'args'
               88  LOAD_ATTR                cfgfiles
               90  LOAD_CONST               True
               92  LOAD_CONST               ('strict',)
               94  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               96  POP_TOP          
             98_0  COME_FROM            80  '80'

 L. 123        98  LOAD_FAST                'args'
              100  LOAD_ATTR                yamlfiles
              102  POP_JUMP_IF_FALSE   122  'to 122'

 L. 124       104  LOAD_GLOBAL              config
              106  LOAD_ATTR                load
              108  LOAD_FAST                'args'
              110  LOAD_ATTR                yamlfiles
              112  LOAD_CONST               True
              114  LOAD_STR                 'yaml'
              116  LOAD_CONST               ('strict', 'fmt')
              118  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              120  POP_TOP          
            122_0  COME_FROM           102  '102'

 L. 125       122  LOAD_FAST                'args'
              124  LOAD_ATTR                postprocessors
              126  POP_JUMP_IF_FALSE   144  'to 144'

 L. 126       128  LOAD_GLOBAL              config
              130  LOAD_METHOD              set
              132  LOAD_CONST               ()
              134  LOAD_STR                 'postprocessors'
              136  LOAD_FAST                'args'
              138  LOAD_ATTR                postprocessors
              140  CALL_METHOD_3         3  '3 positional arguments'
              142  POP_TOP          
            144_0  COME_FROM           126  '126'

 L. 127       144  LOAD_FAST                'args'
              146  LOAD_ATTR                abort
              148  POP_JUMP_IF_FALSE   174  'to 174'

 L. 128       150  LOAD_GLOBAL              config
              152  LOAD_METHOD              set
              154  LOAD_CONST               ()
              156  LOAD_STR                 'skip'
              158  LOAD_STR                 'abort:'
              160  LOAD_GLOBAL              str
              162  LOAD_FAST                'args'
              164  LOAD_ATTR                abort
              166  CALL_FUNCTION_1       1  '1 positional argument'
              168  BINARY_ADD       
              170  CALL_METHOD_3         3  '3 positional arguments'
              172  POP_TOP          
            174_0  COME_FROM           148  '148'

 L. 129       174  SETUP_LOOP          200  'to 200'
              176  LOAD_FAST                'args'
              178  LOAD_ATTR                options
              180  GET_ITER         
              182  FOR_ITER            198  'to 198'
              184  STORE_FAST               'opts'

 L. 130       186  LOAD_GLOBAL              config
              188  LOAD_ATTR                set
              190  LOAD_FAST                'opts'
              192  CALL_FUNCTION_EX      0  'positional arguments only'
              194  POP_TOP          
              196  JUMP_BACK           182  'to 182'
              198  POP_BLOCK        
            200_0  COME_FROM_LOOP      174  '174'

 L. 133       200  LOAD_GLOBAL              config
              202  LOAD_METHOD              get
              204  LOAD_CONST               ('extractor',)
              206  LOAD_STR                 'modules'
              208  CALL_METHOD_2         2  '2 positional arguments'
              210  STORE_FAST               'modules'

 L. 134       212  LOAD_FAST                'modules'
              214  LOAD_CONST               None
              216  COMPARE_OP               is-not
              218  POP_JUMP_IF_FALSE   236  'to 236'

 L. 135       220  LOAD_FAST                'modules'
              222  LOAD_GLOBAL              extractor
              224  STORE_ATTR               modules

 L. 136       226  LOAD_GLOBAL              iter
              228  LOAD_FAST                'modules'
              230  CALL_FUNCTION_1       1  '1 positional argument'
              232  LOAD_GLOBAL              extractor
              234  STORE_ATTR               _module_iter
            236_0  COME_FROM           218  '218'

 L. 139       236  LOAD_GLOBAL              output
              238  LOAD_METHOD              configure_logging
              240  LOAD_FAST                'args'
              242  LOAD_ATTR                loglevel
              244  CALL_METHOD_1         1  '1 positional argument'
              246  POP_TOP          

 L. 140       248  LOAD_FAST                'args'
              250  LOAD_ATTR                loglevel
              252  LOAD_GLOBAL              logging
              254  LOAD_ATTR                ERROR
              256  COMPARE_OP               >=
          258_260  POP_JUMP_IF_FALSE   278  'to 278'

 L. 141       262  LOAD_GLOBAL              config
              264  LOAD_METHOD              set
              266  LOAD_CONST               ('output',)
              268  LOAD_STR                 'mode'
              270  LOAD_STR                 'null'
              272  CALL_METHOD_3         3  '3 positional arguments'
              274  POP_TOP          
              276  JUMP_FORWARD        522  'to 522'
            278_0  COME_FROM           258  '258'

 L. 142       278  LOAD_FAST                'args'
              280  LOAD_ATTR                loglevel
              282  LOAD_GLOBAL              logging
              284  LOAD_ATTR                DEBUG
              286  COMPARE_OP               <=
          288_290  POP_JUMP_IF_FALSE   522  'to 522'

 L. 143       292  LOAD_CONST               0
              294  LOAD_CONST               None
              296  IMPORT_NAME              platform
              298  STORE_FAST               'platform'

 L. 144       300  LOAD_CONST               0
              302  LOAD_CONST               None
              304  IMPORT_NAME              subprocess
              306  STORE_FAST               'subprocess'

 L. 145       308  LOAD_CONST               0
              310  LOAD_CONST               None
              312  IMPORT_NAME_ATTR         os.path
              314  STORE_FAST               'os'

 L. 146       316  LOAD_CONST               0
              318  LOAD_CONST               None
              320  IMPORT_NAME              requests
              322  STORE_FAST               'requests'

 L. 148       324  LOAD_STR                 ''
              326  STORE_FAST               'head'

 L. 149       328  SETUP_EXCEPT        408  'to 408'

 L. 150       330  LOAD_FAST                'subprocess'
              332  LOAD_ATTR                Popen

 L. 151       334  LOAD_CONST               ('git', 'rev-parse', '--short', 'HEAD')

 L. 152       336  LOAD_FAST                'subprocess'
              338  LOAD_ATTR                PIPE

 L. 153       340  LOAD_FAST                'subprocess'
              342  LOAD_ATTR                PIPE

 L. 154       344  LOAD_FAST                'os'
              346  LOAD_ATTR                path
              348  LOAD_METHOD              dirname
              350  LOAD_FAST                'os'
              352  LOAD_ATTR                path
              354  LOAD_METHOD              abspath
              356  LOAD_GLOBAL              __file__
              358  CALL_METHOD_1         1  '1 positional argument'
              360  CALL_METHOD_1         1  '1 positional argument'
              362  LOAD_CONST               ('stdout', 'stderr', 'cwd')
              364  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              366  LOAD_METHOD              communicate
              368  CALL_METHOD_0         0  '0 positional arguments'
              370  UNPACK_SEQUENCE_2     2 
              372  STORE_FAST               'out'
              374  STORE_FAST               'err'

 L. 156       376  LOAD_FAST                'out'
          378_380  POP_JUMP_IF_FALSE   404  'to 404'
              382  LOAD_FAST                'err'
          384_386  POP_JUMP_IF_TRUE    404  'to 404'

 L. 157       388  LOAD_STR                 ' - Git HEAD: '
              390  LOAD_FAST                'out'
              392  LOAD_METHOD              decode
              394  CALL_METHOD_0         0  '0 positional arguments'
              396  LOAD_METHOD              rstrip
              398  CALL_METHOD_0         0  '0 positional arguments'
              400  BINARY_ADD       
              402  STORE_FAST               'head'
            404_0  COME_FROM           384  '384'
            404_1  COME_FROM           378  '378'
              404  POP_BLOCK        
              406  JUMP_FORWARD        436  'to 436'
            408_0  COME_FROM_EXCEPT    328  '328'

 L. 158       408  DUP_TOP          
              410  LOAD_GLOBAL              OSError
              412  LOAD_FAST                'subprocess'
              414  LOAD_ATTR                SubprocessError
              416  BUILD_TUPLE_2         2 
              418  COMPARE_OP               exception-match
          420_422  POP_JUMP_IF_FALSE   434  'to 434'
              424  POP_TOP          
              426  POP_TOP          
              428  POP_TOP          

 L. 159       430  POP_EXCEPT       
              432  JUMP_FORWARD        436  'to 436'
            434_0  COME_FROM           420  '420'
              434  END_FINALLY      
            436_0  COME_FROM           432  '432'
            436_1  COME_FROM           406  '406'

 L. 161       436  LOAD_FAST                'log'
              438  LOAD_METHOD              debug
              440  LOAD_STR                 'Version %s%s'
              442  LOAD_GLOBAL              __version__
              444  LOAD_FAST                'head'
              446  CALL_METHOD_3         3  '3 positional arguments'
              448  POP_TOP          

 L. 162       450  LOAD_FAST                'log'
              452  LOAD_METHOD              debug
              454  LOAD_STR                 'Python %s - %s'

 L. 163       456  LOAD_FAST                'platform'
              458  LOAD_METHOD              python_version
              460  CALL_METHOD_0         0  '0 positional arguments'
              462  LOAD_FAST                'platform'
              464  LOAD_METHOD              platform
              466  CALL_METHOD_0         0  '0 positional arguments'
              468  CALL_METHOD_3         3  '3 positional arguments'
              470  POP_TOP          

 L. 164       472  SETUP_EXCEPT        500  'to 500'

 L. 165       474  LOAD_FAST                'log'
              476  LOAD_METHOD              debug
              478  LOAD_STR                 'requests %s - urllib3 %s'

 L. 166       480  LOAD_FAST                'requests'
              482  LOAD_ATTR                __version__

 L. 167       484  LOAD_FAST                'requests'
              486  LOAD_ATTR                packages
              488  LOAD_ATTR                urllib3
              490  LOAD_ATTR                __version__
              492  CALL_METHOD_3         3  '3 positional arguments'
              494  POP_TOP          
              496  POP_BLOCK        
              498  JUMP_FORWARD        522  'to 522'
            500_0  COME_FROM_EXCEPT    472  '472'

 L. 168       500  DUP_TOP          
              502  LOAD_GLOBAL              AttributeError
              504  COMPARE_OP               exception-match
          506_508  POP_JUMP_IF_FALSE   520  'to 520'
              510  POP_TOP          
              512  POP_TOP          
              514  POP_TOP          

 L. 169       516  POP_EXCEPT       
              518  JUMP_FORWARD        522  'to 522'
            520_0  COME_FROM           506  '506'
              520  END_FINALLY      
            522_0  COME_FROM           518  '518'
            522_1  COME_FROM           498  '498'
            522_2  COME_FROM           288  '288'
            522_3  COME_FROM           276  '276'

 L. 171       522  LOAD_FAST                'args'
              524  LOAD_ATTR                list_modules
          526_528  POP_JUMP_IF_FALSE   560  'to 560'

 L. 172       530  SETUP_LOOP          556  'to 556'
              532  LOAD_GLOBAL              extractor
              534  LOAD_ATTR                modules
              536  GET_ITER         
              538  FOR_ITER            554  'to 554'
              540  STORE_FAST               'module_name'

 L. 173       542  LOAD_GLOBAL              print
              544  LOAD_FAST                'module_name'
              546  CALL_FUNCTION_1       1  '1 positional argument'
              548  POP_TOP          
          550_552  JUMP_BACK           538  'to 538'
              554  POP_BLOCK        
            556_0  COME_FROM_LOOP      530  '530'
          556_558  JUMP_FORWARD       1306  'to 1306'
            560_0  COME_FROM           526  '526'

 L. 174       560  LOAD_FAST                'args'
              562  LOAD_ATTR                list_extractors
          564_566  POP_JUMP_IF_FALSE   682  'to 682'

 L. 175       568  SETUP_LOOP          678  'to 678'
              570  LOAD_GLOBAL              extractor
              572  LOAD_METHOD              extractors
              574  CALL_METHOD_0         0  '0 positional arguments'
              576  GET_ITER         
              578  FOR_ITER            676  'to 676'
              580  STORE_FAST               'extr'

 L. 176       582  LOAD_FAST                'extr'
              584  LOAD_ATTR                __doc__
          586_588  POP_JUMP_IF_TRUE    594  'to 594'

 L. 177   590_592  CONTINUE            578  'to 578'
            594_0  COME_FROM           586  '586'

 L. 178       594  LOAD_GLOBAL              print
              596  LOAD_FAST                'extr'
              598  LOAD_ATTR                __name__
              600  CALL_FUNCTION_1       1  '1 positional argument'
              602  POP_TOP          

 L. 179       604  LOAD_GLOBAL              print
              606  LOAD_FAST                'extr'
              608  LOAD_ATTR                __doc__
              610  CALL_FUNCTION_1       1  '1 positional argument'
              612  POP_TOP          

 L. 180       614  LOAD_GLOBAL              print
              616  LOAD_STR                 'Category:'
              618  LOAD_FAST                'extr'
              620  LOAD_ATTR                category

 L. 181       622  LOAD_STR                 '- Subcategory:'
              624  LOAD_FAST                'extr'
              626  LOAD_ATTR                subcategory
              628  CALL_FUNCTION_4       4  '4 positional arguments'
              630  POP_TOP          

 L. 182       632  LOAD_GLOBAL              next
              634  LOAD_FAST                'extr'
              636  LOAD_METHOD              _get_tests
              638  CALL_METHOD_0         0  '0 positional arguments'
              640  LOAD_CONST               None
              642  CALL_FUNCTION_2       2  '2 positional arguments'
              644  STORE_FAST               'test'

 L. 183       646  LOAD_FAST                'test'
          648_650  POP_JUMP_IF_FALSE   666  'to 666'

 L. 184       652  LOAD_GLOBAL              print
              654  LOAD_STR                 'Example :'
              656  LOAD_FAST                'test'
              658  LOAD_CONST               0
              660  BINARY_SUBSCR    
              662  CALL_FUNCTION_2       2  '2 positional arguments'
              664  POP_TOP          
            666_0  COME_FROM           648  '648'

 L. 185       666  LOAD_GLOBAL              print
              668  CALL_FUNCTION_0       0  '0 positional arguments'
              670  POP_TOP          
          672_674  JUMP_BACK           578  'to 578'
              676  POP_BLOCK        
            678_0  COME_FROM_LOOP      568  '568'
          678_680  JUMP_FORWARD       1306  'to 1306'
            682_0  COME_FROM           564  '564'

 L. 186       682  LOAD_FAST                'args'
              684  LOAD_ATTR                clear_cache
          686_688  POP_JUMP_IF_FALSE   780  'to 780'

 L. 187       690  LOAD_CONST               1
              692  LOAD_CONST               ('cache',)
              694  IMPORT_NAME              
              696  IMPORT_FROM              cache
              698  STORE_FAST               'cache'
              700  POP_TOP          

 L. 188       702  LOAD_GLOBAL              logging
              704  LOAD_METHOD              getLogger
              706  LOAD_STR                 'cache'
              708  CALL_METHOD_1         1  '1 positional argument'
              710  STORE_FAST               'log'

 L. 189       712  LOAD_FAST                'cache'
              714  LOAD_METHOD              clear
              716  CALL_METHOD_0         0  '0 positional arguments'
              718  STORE_FAST               'cnt'

 L. 191       720  LOAD_FAST                'cnt'
              722  LOAD_CONST               None
              724  COMPARE_OP               is
          726_728  POP_JUMP_IF_FALSE   742  'to 742'

 L. 192       730  LOAD_FAST                'log'
              732  LOAD_METHOD              error
              734  LOAD_STR                 'Database file not available'
              736  CALL_METHOD_1         1  '1 positional argument'
              738  POP_TOP          
              740  JUMP_FORWARD       1306  'to 1306'
            742_0  COME_FROM           726  '726'

 L. 194       742  LOAD_FAST                'log'
              744  LOAD_METHOD              info

 L. 195       746  LOAD_STR                 "Deleted %d %s from '%s'"

 L. 196       748  LOAD_FAST                'cnt'
              750  LOAD_FAST                'cnt'
              752  LOAD_CONST               1
              754  COMPARE_OP               ==
          756_758  POP_JUMP_IF_FALSE   764  'to 764'
              760  LOAD_STR                 'entry'
              762  JUMP_FORWARD        766  'to 766'
            764_0  COME_FROM           756  '756'
              764  LOAD_STR                 'entries'
            766_0  COME_FROM           762  '762'
              766  LOAD_FAST                'cache'
              768  LOAD_METHOD              _path
              770  CALL_METHOD_0         0  '0 positional arguments'
              772  CALL_METHOD_4         4  '4 positional arguments'
              774  POP_TOP          
          776_778  JUMP_FORWARD       1306  'to 1306'
            780_0  COME_FROM           686  '686'

 L. 199       780  LOAD_FAST                'args'
              782  LOAD_ATTR                urls
          784_786  POP_JUMP_IF_TRUE    806  'to 806'
              788  LOAD_FAST                'args'
              790  LOAD_ATTR                inputfile
          792_794  POP_JUMP_IF_TRUE    806  'to 806'

 L. 200       796  LOAD_FAST                'parser'
              798  LOAD_METHOD              error

 L. 201       800  LOAD_STR                 "The following arguments are required: URL\nUse 'gallery-dl --help' to get a list of all options."
              802  CALL_METHOD_1         1  '1 positional argument'
              804  POP_TOP          
            806_0  COME_FROM           792  '792'
            806_1  COME_FROM           784  '784'

 L. 204       806  LOAD_FAST                'args'
              808  LOAD_ATTR                list_urls
          810_812  POP_JUMP_IF_FALSE   830  'to 830'

 L. 205       814  LOAD_GLOBAL              job
              816  LOAD_ATTR                UrlJob
              818  STORE_FAST               'jobtype'

 L. 206       820  LOAD_FAST                'args'
              822  LOAD_ATTR                list_urls
              824  LOAD_FAST                'jobtype'
              826  STORE_ATTR               maxdepth
              828  JUMP_FORWARD        844  'to 844'
            830_0  COME_FROM           810  '810'

 L. 208       830  LOAD_FAST                'args'
              832  LOAD_ATTR                jobtype
          834_836  JUMP_IF_TRUE_OR_POP   842  'to 842'
              838  LOAD_GLOBAL              job
              840  LOAD_ATTR                DownloadJob
            842_0  COME_FROM           834  '834'
              842  STORE_FAST               'jobtype'
            844_0  COME_FROM           828  '828'

 L. 210       844  LOAD_FAST                'args'
              846  LOAD_ATTR                urls
              848  STORE_FAST               'urls'

 L. 211       850  LOAD_FAST                'args'
              852  LOAD_ATTR                inputfile
          854_856  POP_JUMP_IF_FALSE  1002  'to 1002'

 L. 212       858  SETUP_EXCEPT        954  'to 954'

 L. 213       860  LOAD_FAST                'args'
              862  LOAD_ATTR                inputfile
              864  LOAD_STR                 '-'
              866  COMPARE_OP               ==
          868_870  POP_JUMP_IF_FALSE   910  'to 910'

 L. 214       872  LOAD_GLOBAL              sys
              874  LOAD_ATTR                stdin
          876_878  POP_JUMP_IF_FALSE   898  'to 898'

 L. 215       880  LOAD_FAST                'urls'
              882  LOAD_GLOBAL              parse_inputfile
              884  LOAD_GLOBAL              sys
              886  LOAD_ATTR                stdin
              888  LOAD_FAST                'log'
              890  CALL_FUNCTION_2       2  '2 positional arguments'
              892  INPLACE_ADD      
              894  STORE_FAST               'urls'
              896  JUMP_FORWARD        908  'to 908'
            898_0  COME_FROM           876  '876'

 L. 217       898  LOAD_FAST                'log'
              900  LOAD_METHOD              warning
              902  LOAD_STR                 'input file: stdin is not readable'
              904  CALL_METHOD_1         1  '1 positional argument'
              906  POP_TOP          
            908_0  COME_FROM           896  '896'
              908  JUMP_FORWARD        950  'to 950'
            910_0  COME_FROM           868  '868'

 L. 219       910  LOAD_GLOBAL              open
              912  LOAD_FAST                'args'
              914  LOAD_ATTR                inputfile
              916  LOAD_STR                 'utf-8'
              918  LOAD_CONST               ('encoding',)
              920  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              922  SETUP_WITH          944  'to 944'
              924  STORE_FAST               'file'

 L. 220       926  LOAD_FAST                'urls'
              928  LOAD_GLOBAL              parse_inputfile
              930  LOAD_FAST                'file'
              932  LOAD_FAST                'log'
              934  CALL_FUNCTION_2       2  '2 positional arguments'
              936  INPLACE_ADD      
              938  STORE_FAST               'urls'
              940  POP_BLOCK        
              942  LOAD_CONST               None
            944_0  COME_FROM_WITH      922  '922'
              944  WITH_CLEANUP_START
              946  WITH_CLEANUP_FINISH
              948  END_FINALLY      
            950_0  COME_FROM           908  '908'
              950  POP_BLOCK        
              952  JUMP_FORWARD       1002  'to 1002'
            954_0  COME_FROM_EXCEPT    858  '858'

 L. 221       954  DUP_TOP          
              956  LOAD_GLOBAL              OSError
              958  COMPARE_OP               exception-match
          960_962  POP_JUMP_IF_FALSE  1000  'to 1000'
              964  POP_TOP          
              966  STORE_FAST               'exc'
              968  POP_TOP          
              970  SETUP_FINALLY       988  'to 988'

 L. 222       972  LOAD_FAST                'log'
              974  LOAD_METHOD              warning
              976  LOAD_STR                 'input file: %s'
              978  LOAD_FAST                'exc'
              980  CALL_METHOD_2         2  '2 positional arguments'
              982  POP_TOP          
              984  POP_BLOCK        
              986  LOAD_CONST               None
            988_0  COME_FROM_FINALLY   970  '970'
              988  LOAD_CONST               None
              990  STORE_FAST               'exc'
              992  DELETE_FAST              'exc'
              994  END_FINALLY      
              996  POP_EXCEPT       
              998  JUMP_FORWARD       1002  'to 1002'
           1000_0  COME_FROM           960  '960'
             1000  END_FINALLY      
           1002_0  COME_FROM           998  '998'
           1002_1  COME_FROM           952  '952'
           1002_2  COME_FROM           854  '854'

 L. 225      1002  LOAD_GLOBAL              output
             1004  LOAD_ATTR                setup_logging_handler

 L. 226      1006  LOAD_STR                 'unsupportedfile'
             1008  LOAD_STR                 '{message}'
             1010  LOAD_CONST               ('fmt',)
             1012  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1014  STORE_FAST               'handler'

 L. 227      1016  LOAD_FAST                'handler'
         1018_1020  POP_JUMP_IF_FALSE  1056  'to 1056'

 L. 228      1022  LOAD_GLOBAL              logging
             1024  LOAD_METHOD              getLogger
             1026  LOAD_STR                 'unsupported'
             1028  CALL_METHOD_1         1  '1 positional argument'
             1030  STORE_FAST               'ulog'

 L. 229      1032  LOAD_FAST                'ulog'
             1034  LOAD_METHOD              addHandler
             1036  LOAD_FAST                'handler'
             1038  CALL_METHOD_1         1  '1 positional argument'
             1040  POP_TOP          

 L. 230      1042  LOAD_CONST               False
             1044  LOAD_FAST                'ulog'
             1046  STORE_ATTR               propagate

 L. 231      1048  LOAD_FAST                'ulog'
             1050  LOAD_GLOBAL              job
             1052  LOAD_ATTR                Job
             1054  STORE_ATTR               ulog
           1056_0  COME_FROM          1018  '1018'

 L. 233      1056  LOAD_GLOBAL              config
             1058  LOAD_METHOD              get
             1060  LOAD_CONST               ('output',)
             1062  LOAD_STR                 'progress'
             1064  LOAD_CONST               True
             1066  CALL_METHOD_3         3  '3 positional arguments'
             1068  STORE_FAST               'pformat'

 L. 234      1070  LOAD_FAST                'pformat'
         1072_1074  POP_JUMP_IF_FALSE  1114  'to 1114'
             1076  LOAD_GLOBAL              len
             1078  LOAD_FAST                'urls'
             1080  CALL_FUNCTION_1       1  '1 positional argument'
             1082  LOAD_CONST               1
             1084  COMPARE_OP               >
         1086_1088  POP_JUMP_IF_FALSE  1114  'to 1114'
             1090  LOAD_FAST                'args'
             1092  LOAD_ATTR                loglevel
             1094  LOAD_GLOBAL              logging
             1096  LOAD_ATTR                ERROR
             1098  COMPARE_OP               <
         1100_1102  POP_JUMP_IF_FALSE  1114  'to 1114'

 L. 235      1104  LOAD_GLOBAL              progress
             1106  LOAD_FAST                'urls'
             1108  LOAD_FAST                'pformat'
             1110  CALL_FUNCTION_2       2  '2 positional arguments'
             1112  STORE_FAST               'urls'
           1114_0  COME_FROM          1100  '1100'
           1114_1  COME_FROM          1086  '1086'
           1114_2  COME_FROM          1072  '1072'

 L. 237      1114  LOAD_CONST               0
             1116  STORE_FAST               'retval'

 L. 238      1118  SETUP_LOOP         1302  'to 1302'
             1120  LOAD_FAST                'urls'
             1122  GET_ITER         
             1124  FOR_ITER           1300  'to 1300'
             1126  STORE_FAST               'url'

 L. 239      1128  SETUP_EXCEPT       1252  'to 1252'

 L. 240      1130  LOAD_FAST                'log'
             1132  LOAD_METHOD              debug
             1134  LOAD_STR                 "Starting %s for '%s'"
             1136  LOAD_FAST                'jobtype'
             1138  LOAD_ATTR                __name__
             1140  LOAD_FAST                'url'
             1142  CALL_METHOD_3         3  '3 positional arguments'
             1144  POP_TOP          

 L. 241      1146  LOAD_GLOBAL              isinstance
             1148  LOAD_FAST                'url'
             1150  LOAD_GLOBAL              util
             1152  LOAD_ATTR                ExtendedUrl
             1154  CALL_FUNCTION_2       2  '2 positional arguments'
         1156_1158  POP_JUMP_IF_FALSE  1232  'to 1232'

 L. 242      1160  SETUP_LOOP         1188  'to 1188'
             1162  LOAD_FAST                'url'
             1164  LOAD_ATTR                gconfig
             1166  GET_ITER         
             1168  FOR_ITER           1186  'to 1186'
             1170  STORE_FAST               'opts'

 L. 243      1172  LOAD_GLOBAL              config
             1174  LOAD_ATTR                set
             1176  LOAD_FAST                'opts'
             1178  CALL_FUNCTION_EX      0  'positional arguments only'
             1180  POP_TOP          
         1182_1184  JUMP_BACK          1168  'to 1168'
             1186  POP_BLOCK        
           1188_0  COME_FROM_LOOP     1160  '1160'

 L. 244      1188  LOAD_GLOBAL              config
             1190  LOAD_METHOD              apply
             1192  LOAD_FAST                'url'
             1194  LOAD_ATTR                lconfig
             1196  CALL_METHOD_1         1  '1 positional argument'
             1198  SETUP_WITH         1224  'to 1224'
             1200  POP_TOP          

 L. 245      1202  LOAD_FAST                'retval'
             1204  LOAD_FAST                'jobtype'
             1206  LOAD_FAST                'url'
             1208  LOAD_ATTR                value
             1210  CALL_FUNCTION_1       1  '1 positional argument'
             1212  LOAD_METHOD              run
             1214  CALL_METHOD_0         0  '0 positional arguments'
             1216  INPLACE_OR       
             1218  STORE_FAST               'retval'
             1220  POP_BLOCK        
             1222  LOAD_CONST               None
           1224_0  COME_FROM_WITH     1198  '1198'
             1224  WITH_CLEANUP_START
             1226  WITH_CLEANUP_FINISH
             1228  END_FINALLY      
             1230  JUMP_FORWARD       1248  'to 1248'
           1232_0  COME_FROM          1156  '1156'

 L. 247      1232  LOAD_FAST                'retval'
             1234  LOAD_FAST                'jobtype'
             1236  LOAD_FAST                'url'
             1238  CALL_FUNCTION_1       1  '1 positional argument'
             1240  LOAD_METHOD              run
             1242  CALL_METHOD_0         0  '0 positional arguments'
             1244  INPLACE_OR       
             1246  STORE_FAST               'retval'
           1248_0  COME_FROM          1230  '1230'
             1248  POP_BLOCK        
             1250  JUMP_BACK          1124  'to 1124'
           1252_0  COME_FROM_EXCEPT   1128  '1128'

 L. 248      1252  DUP_TOP          
             1254  LOAD_GLOBAL              exception
             1256  LOAD_ATTR                NoExtractorError
             1258  COMPARE_OP               exception-match
         1260_1262  POP_JUMP_IF_FALSE  1294  'to 1294'
             1264  POP_TOP          
             1266  POP_TOP          
           1268_0  COME_FROM           740  '740'
             1268  POP_TOP          

 L. 249      1270  LOAD_FAST                'log'
             1272  LOAD_METHOD              error
             1274  LOAD_STR                 "No suitable extractor found for '%s'"
             1276  LOAD_FAST                'url'
             1278  CALL_METHOD_2         2  '2 positional arguments'
             1280  POP_TOP          

 L. 250      1282  LOAD_FAST                'retval'
             1284  LOAD_CONST               64
             1286  INPLACE_OR       
             1288  STORE_FAST               'retval'
             1290  POP_EXCEPT       
             1292  JUMP_BACK          1124  'to 1124'
           1294_0  COME_FROM          1260  '1260'
             1294  END_FINALLY      
         1296_1298  JUMP_BACK          1124  'to 1124'
             1300  POP_BLOCK        
           1302_0  COME_FROM_LOOP     1118  '1118'

 L. 251      1302  LOAD_FAST                'retval'
             1304  RETURN_VALUE     
           1306_0  COME_FROM           776  '776'
           1306_1  COME_FROM           678  '678'
           1306_2  COME_FROM           556  '556'
             1306  POP_BLOCK        
             1308  JUMP_FORWARD       1420  'to 1420'
           1310_0  COME_FROM_EXCEPT      0  '0'

 L. 253      1310  DUP_TOP          
             1312  LOAD_GLOBAL              KeyboardInterrupt
             1314  COMPARE_OP               exception-match
         1316_1318  POP_JUMP_IF_FALSE  1340  'to 1340'
             1320  POP_TOP          
             1322  POP_TOP          
             1324  POP_TOP          

 L. 254      1326  LOAD_GLOBAL              sys
             1328  LOAD_METHOD              exit
             1330  LOAD_STR                 '\nKeyboardInterrupt'
             1332  CALL_METHOD_1         1  '1 positional argument'
             1334  POP_TOP          
             1336  POP_EXCEPT       
             1338  JUMP_FORWARD       1420  'to 1420'
           1340_0  COME_FROM          1316  '1316'

 L. 255      1340  DUP_TOP          
             1342  LOAD_GLOBAL              BrokenPipeError
             1344  COMPARE_OP               exception-match
         1346_1348  POP_JUMP_IF_FALSE  1360  'to 1360'
             1350  POP_TOP          
             1352  POP_TOP          
             1354  POP_TOP          

 L. 256      1356  POP_EXCEPT       
             1358  JUMP_FORWARD       1420  'to 1420'
           1360_0  COME_FROM          1346  '1346'

 L. 257      1360  DUP_TOP          
             1362  LOAD_GLOBAL              OSError
             1364  COMPARE_OP               exception-match
         1366_1368  POP_JUMP_IF_FALSE  1418  'to 1418'
             1370  POP_TOP          
             1372  STORE_FAST               'exc'
             1374  POP_TOP          
             1376  SETUP_FINALLY      1406  'to 1406'

 L. 258      1378  LOAD_CONST               0
             1380  LOAD_CONST               None
             1382  IMPORT_NAME              errno
             1384  STORE_FAST               'errno'

 L. 259      1386  LOAD_FAST                'exc'
             1388  LOAD_ATTR                errno
             1390  LOAD_FAST                'errno'
             1392  LOAD_ATTR                EPIPE
             1394  COMPARE_OP               !=
         1396_1398  POP_JUMP_IF_FALSE  1402  'to 1402'

 L. 260      1400  RAISE_VARARGS_0       0  'reraise'
           1402_0  COME_FROM          1396  '1396'
             1402  POP_BLOCK        
             1404  LOAD_CONST               None
           1406_0  COME_FROM_FINALLY  1376  '1376'
             1406  LOAD_CONST               None
             1408  STORE_FAST               'exc'
             1410  DELETE_FAST              'exc'
             1412  END_FINALLY      
             1414  POP_EXCEPT       
             1416  JUMP_FORWARD       1420  'to 1420'
           1418_0  COME_FROM          1366  '1366'
             1418  END_FINALLY      
           1420_0  COME_FROM          1416  '1416'
           1420_1  COME_FROM          1358  '1358'
           1420_2  COME_FROM          1338  '1338'
           1420_3  COME_FROM          1308  '1308'

 L. 261      1420  LOAD_CONST               1
             1422  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 1268_0