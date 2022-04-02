# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: comtypes\client\_generate.py
import types, os, sys, comtypes.client, comtypes.tools.codegenerator, importlib, logging
logger = logging.getLogger(__name__)
PATH = os.environ['PATH'].split(os.pathsep)

def _my_import--- This code section failed: ---

 L.  15         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME_ATTR         comtypes.gen
                6  STORE_FAST               'comtypes'

 L.  16         8  LOAD_FAST                'comtypes'
               10  LOAD_ATTR                client
               12  LOAD_ATTR                gen_dir
               14  POP_JUMP_IF_FALSE    50  'to 50'

 L.  17        16  LOAD_FAST                'comtypes'
               18  LOAD_ATTR                client
               20  LOAD_ATTR                gen_dir
               22  LOAD_FAST                'comtypes'
               24  LOAD_ATTR                gen
               26  LOAD_ATTR                __path__
               28  <118>                 1  ''

 L.  16        30  POP_JUMP_IF_FALSE    50  'to 50'

 L.  18        32  LOAD_FAST                'comtypes'
               34  LOAD_ATTR                gen
               36  LOAD_ATTR                __path__
               38  LOAD_METHOD              append
               40  LOAD_FAST                'comtypes'
               42  LOAD_ATTR                client
               44  LOAD_ATTR                gen_dir
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          
             50_0  COME_FROM            30  '30'
             50_1  COME_FROM            14  '14'

 L.  19        50  LOAD_GLOBAL              __import__
               52  LOAD_FAST                'fullname'
               54  LOAD_GLOBAL              globals
               56  CALL_FUNCTION_0       0  ''
               58  LOAD_GLOBAL              locals
               60  CALL_FUNCTION_0       0  ''
               62  LOAD_STR                 'DUMMY'
               64  BUILD_LIST_1          1 
               66  CALL_FUNCTION_4       4  ''
               68  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 28


def _name_module(tlib):
    libattr = tlib.GetLibAttr()
    modname = '_%s_%s_%s_%s' % (
     str(libattr.guid)[1:-1].replace('-', '_'),
     libattr.lcid,
     libattr.wMajorVerNum,
     libattr.wMinorVerNum)
    return 'comtypes.gen.' + modname


def GetModule--- This code section failed: ---

 L.  72         0  LOAD_CONST               None
                2  STORE_FAST               'pathname'

 L.  73         4  LOAD_GLOBAL              isinstance
                6  LOAD_FAST                'tlib'
                8  LOAD_GLOBAL              str
               10  CALL_FUNCTION_2       2  ''
               12  POP_JUMP_IF_FALSE   148  'to 148'

 L.  75        14  LOAD_GLOBAL              os
               16  LOAD_ATTR                path
               18  LOAD_METHOD              isabs
               20  LOAD_FAST                'tlib'
               22  CALL_METHOD_1         1  ''
               24  POP_JUMP_IF_TRUE    116  'to 116'

 L.  78        26  LOAD_GLOBAL              sys
               28  LOAD_METHOD              _getframe
               30  LOAD_CONST               1
               32  CALL_METHOD_1         1  ''
               34  STORE_FAST               'frame'

 L.  79        36  LOAD_FAST                'frame'
               38  LOAD_ATTR                f_globals
               40  LOAD_METHOD              get
               42  LOAD_STR                 '__file__'
               44  LOAD_CONST               None
               46  CALL_METHOD_2         2  ''
               48  STORE_FAST               '_file_'

 L.  80        50  LOAD_FAST                '_file_'
               52  LOAD_CONST               None
               54  <117>                 1  ''
               56  POP_JUMP_IF_FALSE   116  'to 116'

 L.  81        58  LOAD_GLOBAL              os
               60  LOAD_ATTR                path
               62  LOAD_METHOD              dirname
               64  LOAD_GLOBAL              os
               66  LOAD_ATTR                path
               68  LOAD_METHOD              abspath
               70  LOAD_FAST                '_file_'
               72  CALL_METHOD_1         1  ''
               74  CALL_METHOD_1         1  ''
               76  STORE_FAST               'directory'

 L.  82        78  LOAD_GLOBAL              os
               80  LOAD_ATTR                path
               82  LOAD_METHOD              normpath
               84  LOAD_GLOBAL              os
               86  LOAD_ATTR                path
               88  LOAD_METHOD              join
               90  LOAD_FAST                'directory'
               92  LOAD_FAST                'tlib'
               94  CALL_METHOD_2         2  ''
               96  CALL_METHOD_1         1  ''
               98  STORE_FAST               'abspath'

 L.  86       100  LOAD_GLOBAL              os
              102  LOAD_ATTR                path
              104  LOAD_METHOD              isfile
              106  LOAD_FAST                'abspath'
              108  CALL_METHOD_1         1  ''
              110  POP_JUMP_IF_FALSE   116  'to 116'

 L.  87       112  LOAD_FAST                'abspath'
              114  STORE_FAST               'tlib'
            116_0  COME_FROM           110  '110'
            116_1  COME_FROM            56  '56'
            116_2  COME_FROM            24  '24'

 L.  88       116  LOAD_GLOBAL              logger
              118  LOAD_METHOD              debug
              120  LOAD_STR                 'GetModule(%s)'
              122  LOAD_FAST                'tlib'
              124  CALL_METHOD_2         2  ''
              126  POP_TOP          

 L.  89       128  LOAD_FAST                'tlib'
              130  STORE_FAST               'pathname'

 L.  90       132  LOAD_GLOBAL              comtypes
              134  LOAD_ATTR                typeinfo
              136  LOAD_METHOD              LoadTypeLibEx
              138  LOAD_FAST                'tlib'
              140  CALL_METHOD_1         1  ''
              142  STORE_FAST               'tlib'
          144_146  JUMP_FORWARD        526  'to 526'
            148_0  COME_FROM            12  '12'

 L.  91       148  LOAD_GLOBAL              isinstance
              150  LOAD_FAST                'tlib'
              152  LOAD_GLOBAL              comtypes
              154  LOAD_ATTR                GUID
              156  CALL_FUNCTION_2       2  ''
          158_160  POP_JUMP_IF_FALSE   384  'to 384'

 L.  93       162  LOAD_GLOBAL              str
              164  LOAD_FAST                'tlib'
              166  CALL_FUNCTION_1       1  ''
              168  STORE_FAST               'clsid'

 L.  96       170  LOAD_CONST               0
              172  LOAD_CONST               None
              174  IMPORT_NAME              winreg
              176  STORE_FAST               'winreg'

 L.  97       178  LOAD_FAST                'winreg'
              180  LOAD_METHOD              OpenKey
              182  LOAD_FAST                'winreg'
              184  LOAD_ATTR                HKEY_CLASSES_ROOT
              186  LOAD_STR                 'CLSID\\%s\\TypeLib'
              188  LOAD_FAST                'clsid'
              190  BINARY_MODULO    
              192  LOAD_CONST               0
              194  LOAD_FAST                'winreg'
              196  LOAD_ATTR                KEY_READ
              198  CALL_METHOD_4         4  ''
              200  SETUP_WITH          234  'to 234'
              202  STORE_FAST               'key'

 L.  98       204  LOAD_FAST                'winreg'
              206  LOAD_METHOD              EnumValue
              208  LOAD_FAST                'key'
              210  LOAD_CONST               0
              212  CALL_METHOD_2         2  ''
              214  LOAD_CONST               1
              216  BINARY_SUBSCR    
              218  STORE_FAST               'typelib'
              220  POP_BLOCK        
              222  LOAD_CONST               None
              224  DUP_TOP          
              226  DUP_TOP          
              228  CALL_FUNCTION_3       3  ''
              230  POP_TOP          
              232  JUMP_FORWARD        250  'to 250'
            234_0  COME_FROM_WITH      200  '200'
              234  <49>             
              236  POP_JUMP_IF_TRUE    240  'to 240'
              238  <48>             
            240_0  COME_FROM           236  '236'
              240  POP_TOP          
              242  POP_TOP          
              244  POP_TOP          
              246  POP_EXCEPT       
              248  POP_TOP          
            250_0  COME_FROM           232  '232'

 L.  99       250  LOAD_FAST                'winreg'
              252  LOAD_METHOD              OpenKey
              254  LOAD_FAST                'winreg'
              256  LOAD_ATTR                HKEY_CLASSES_ROOT
              258  LOAD_STR                 'CLSID\\%s\\Version'
              260  LOAD_FAST                'clsid'
              262  BINARY_MODULO    
              264  LOAD_CONST               0
              266  LOAD_FAST                'winreg'
              268  LOAD_ATTR                KEY_READ
              270  CALL_METHOD_4         4  ''
              272  SETUP_WITH          312  'to 312'
              274  STORE_FAST               'key'

 L. 100       276  LOAD_FAST                'winreg'
              278  LOAD_METHOD              EnumValue
              280  LOAD_FAST                'key'
              282  LOAD_CONST               0
              284  CALL_METHOD_2         2  ''
              286  LOAD_CONST               1
              288  BINARY_SUBSCR    
              290  LOAD_METHOD              split
              292  LOAD_STR                 '.'
              294  CALL_METHOD_1         1  ''
              296  STORE_FAST               'version'
              298  POP_BLOCK        
              300  LOAD_CONST               None
              302  DUP_TOP          
              304  DUP_TOP          
              306  CALL_FUNCTION_3       3  ''
              308  POP_TOP          
              310  JUMP_FORWARD        330  'to 330'
            312_0  COME_FROM_WITH      272  '272'
              312  <49>             
          314_316  POP_JUMP_IF_TRUE    320  'to 320'
              318  <48>             
            320_0  COME_FROM           314  '314'
              320  POP_TOP          
              322  POP_TOP          
              324  POP_TOP          
              326  POP_EXCEPT       
              328  POP_TOP          
            330_0  COME_FROM           310  '310'

 L. 102       330  LOAD_GLOBAL              logger
              332  LOAD_METHOD              debug
              334  LOAD_STR                 'GetModule(%s)'
              336  LOAD_FAST                'typelib'
              338  CALL_METHOD_2         2  ''
              340  POP_TOP          

 L. 103       342  LOAD_GLOBAL              comtypes
              344  LOAD_ATTR                typeinfo
              346  LOAD_METHOD              LoadRegTypeLib
              348  LOAD_GLOBAL              comtypes
              350  LOAD_METHOD              GUID
              352  LOAD_FAST                'typelib'
              354  CALL_METHOD_1         1  ''
              356  LOAD_GLOBAL              int
              358  LOAD_FAST                'version'
              360  LOAD_CONST               0
              362  BINARY_SUBSCR    
              364  CALL_FUNCTION_1       1  ''
              366  LOAD_GLOBAL              int
              368  LOAD_FAST                'version'
              370  LOAD_CONST               1
              372  BINARY_SUBSCR    
              374  CALL_FUNCTION_1       1  ''
              376  LOAD_CONST               0
              378  CALL_METHOD_4         4  ''
              380  STORE_FAST               'tlib'
              382  JUMP_FORWARD        526  'to 526'
            384_0  COME_FROM           158  '158'

 L. 104       384  LOAD_GLOBAL              isinstance
              386  LOAD_FAST                'tlib'
              388  LOAD_GLOBAL              tuple
              390  LOAD_GLOBAL              list
              392  BUILD_TUPLE_2         2 
              394  CALL_FUNCTION_2       2  ''
          396_398  POP_JUMP_IF_FALSE   454  'to 454'

 L. 106       400  LOAD_GLOBAL              logger
              402  LOAD_METHOD              debug
              404  LOAD_STR                 'GetModule(%s)'
              406  LOAD_FAST                'tlib'
              408  BUILD_TUPLE_1         1 
              410  CALL_METHOD_2         2  ''
              412  POP_TOP          

 L. 107       414  LOAD_GLOBAL              comtypes
              416  LOAD_ATTR                typeinfo
              418  LOAD_ATTR                LoadRegTypeLib
              420  LOAD_GLOBAL              comtypes
              422  LOAD_METHOD              GUID
              424  LOAD_FAST                'tlib'
              426  LOAD_CONST               0
              428  BINARY_SUBSCR    
              430  CALL_METHOD_1         1  ''
              432  BUILD_LIST_1          1 
              434  LOAD_FAST                'tlib'
              436  LOAD_CONST               1
              438  LOAD_CONST               None
              440  BUILD_SLICE_2         2 
              442  BINARY_SUBSCR    
              444  CALL_FINALLY        447  'to 447'
              446  WITH_CLEANUP_FINISH
              448  CALL_FUNCTION_EX      0  'positional arguments only'
              450  STORE_FAST               'tlib'
              452  JUMP_FORWARD        526  'to 526'
            454_0  COME_FROM           396  '396'

 L. 108       454  LOAD_GLOBAL              hasattr
              456  LOAD_FAST                'tlib'
              458  LOAD_STR                 '_reg_libid_'
              460  CALL_FUNCTION_2       2  ''
          462_464  POP_JUMP_IF_FALSE   510  'to 510'

 L. 110       466  LOAD_GLOBAL              logger
              468  LOAD_METHOD              debug
              470  LOAD_STR                 'GetModule(%s)'
              472  LOAD_FAST                'tlib'
              474  CALL_METHOD_2         2  ''
              476  POP_TOP          

 L. 111       478  LOAD_GLOBAL              comtypes
              480  LOAD_ATTR                typeinfo
              482  LOAD_ATTR                LoadRegTypeLib
              484  LOAD_GLOBAL              comtypes
              486  LOAD_METHOD              GUID
              488  LOAD_FAST                'tlib'
              490  LOAD_ATTR                _reg_libid_
              492  CALL_METHOD_1         1  ''
              494  BUILD_LIST_1          1 

 L. 112       496  LOAD_FAST                'tlib'
              498  LOAD_ATTR                _reg_version_

 L. 111       500  CALL_FINALLY        503  'to 503'
              502  WITH_CLEANUP_FINISH
              504  CALL_FUNCTION_EX      0  'positional arguments only'
              506  STORE_FAST               'tlib'
              508  JUMP_FORWARD        526  'to 526'
            510_0  COME_FROM           462  '462'

 L. 115       510  LOAD_GLOBAL              logger
              512  LOAD_METHOD              debug
              514  LOAD_STR                 'GetModule(%s)'
              516  LOAD_FAST                'tlib'
              518  LOAD_METHOD              GetLibAttr
              520  CALL_METHOD_0         0  ''
              522  CALL_METHOD_2         2  ''
              524  POP_TOP          
            526_0  COME_FROM           508  '508'
            526_1  COME_FROM           452  '452'
            526_2  COME_FROM           382  '382'
            526_3  COME_FROM           144  '144'

 L. 118       526  LOAD_GLOBAL              _CreateWrapper
              528  LOAD_FAST                'tlib'
              530  LOAD_FAST                'pathname'
              532  CALL_FUNCTION_2       2  ''
              534  STORE_FAST               'mod'

 L. 119       536  SETUP_FINALLY       556  'to 556'

 L. 120       538  LOAD_FAST                'tlib'
              540  LOAD_METHOD              GetDocumentation
              542  LOAD_CONST               -1
              544  CALL_METHOD_1         1  ''
              546  LOAD_CONST               0
              548  BINARY_SUBSCR    
              550  STORE_FAST               'modulename'
              552  POP_BLOCK        
              554  JUMP_FORWARD        582  'to 582'
            556_0  COME_FROM_FINALLY   536  '536'

 L. 121       556  DUP_TOP          
              558  LOAD_GLOBAL              comtypes
              560  LOAD_ATTR                COMError
          562_564  <121>               580  ''
              566  POP_TOP          
              568  POP_TOP          
              570  POP_TOP          

 L. 122       572  LOAD_FAST                'mod'
              574  ROT_FOUR         
              576  POP_EXCEPT       
              578  RETURN_VALUE     
              580  <48>             
            582_0  COME_FROM           554  '554'

 L. 123       582  LOAD_FAST                'modulename'
              584  LOAD_CONST               None
              586  <117>                 0  ''
          588_590  POP_JUMP_IF_FALSE   596  'to 596'

 L. 124       592  LOAD_FAST                'mod'
              594  RETURN_VALUE     
            596_0  COME_FROM           588  '588'

 L. 125       596  LOAD_GLOBAL              sys
              598  LOAD_ATTR                version_info
              600  LOAD_CONST               (3, 0)
              602  COMPARE_OP               <
          604_606  POP_JUMP_IF_FALSE   618  'to 618'

 L. 126       608  LOAD_FAST                'modulename'
              610  LOAD_METHOD              encode
              612  LOAD_STR                 'mbcs'
              614  CALL_METHOD_1         1  ''
              616  STORE_FAST               'modulename'
            618_0  COME_FROM           604  '604'

 L. 129       618  SETUP_FINALLY       636  'to 636'

 L. 130       620  LOAD_GLOBAL              _my_import
              622  LOAD_STR                 'comtypes.gen.'
              624  LOAD_FAST                'modulename'
              626  BINARY_ADD       
              628  CALL_FUNCTION_1       1  ''
              630  STORE_FAST               'mod'
              632  POP_BLOCK        
              634  JUMP_FORWARD        688  'to 688'
            636_0  COME_FROM_FINALLY   618  '618'

 L. 131       636  DUP_TOP          
              638  LOAD_GLOBAL              Exception
          640_642  <121>               686  ''
              644  POP_TOP          
              646  STORE_FAST               'details'
              648  POP_TOP          
              650  SETUP_FINALLY       678  'to 678'

 L. 132       652  LOAD_GLOBAL              logger
              654  LOAD_METHOD              info
              656  LOAD_STR                 'Could not import comtypes.gen.%s: %s'
              658  LOAD_FAST                'modulename'
              660  LOAD_FAST                'details'
              662  CALL_METHOD_3         3  ''
              664  POP_TOP          
              666  POP_BLOCK        
              668  POP_EXCEPT       
              670  LOAD_CONST               None
              672  STORE_FAST               'details'
              674  DELETE_FAST              'details'
              676  JUMP_FORWARD        692  'to 692'
            678_0  COME_FROM_FINALLY   650  '650'
              678  LOAD_CONST               None
              680  STORE_FAST               'details'
              682  DELETE_FAST              'details'
              684  <48>             
              686  <48>             
            688_0  COME_FROM           634  '634'

 L. 134       688  LOAD_FAST                'mod'
              690  RETURN_VALUE     
            692_0  COME_FROM           676  '676'

 L. 136       692  LOAD_GLOBAL              logger
              694  LOAD_METHOD              info
              696  LOAD_STR                 '# Generating comtypes.gen.%s'
              698  LOAD_FAST                'modulename'
              700  CALL_METHOD_2         2  ''
              702  POP_TOP          

 L. 138       704  LOAD_GLOBAL              _name_module
              706  LOAD_FAST                'tlib'
              708  CALL_FUNCTION_1       1  ''
              710  STORE_FAST               'fullname'

 L. 139       712  LOAD_FAST                'fullname'
              714  LOAD_METHOD              split
              716  LOAD_STR                 '.'
              718  CALL_METHOD_1         1  ''
              720  LOAD_CONST               -1
              722  BINARY_SUBSCR    
              724  STORE_FAST               'modname'

 L. 140       726  LOAD_STR                 'from comtypes.gen import %s\nglobals().update(%s.__dict__)\n'
              728  LOAD_FAST                'modname'
              730  LOAD_FAST                'modname'
              732  BUILD_TUPLE_2         2 
              734  BINARY_MODULO    
              736  STORE_FAST               'code'

 L. 141       738  LOAD_FAST                'code'
              740  LOAD_STR                 "__name__ = 'comtypes.gen.%s'"
              742  LOAD_FAST                'modulename'
              744  BINARY_MODULO    
              746  INPLACE_ADD      
              748  STORE_FAST               'code'

 L. 142       750  LOAD_GLOBAL              comtypes
              752  LOAD_ATTR                client
              754  LOAD_ATTR                gen_dir
              756  LOAD_CONST               None
              758  <117>                 0  ''
          760_762  POP_JUMP_IF_FALSE   854  'to 854'

 L. 143       764  LOAD_GLOBAL              types
              766  LOAD_METHOD              ModuleType
              768  LOAD_STR                 'comtypes.gen.'
              770  LOAD_FAST                'modulename'
              772  BINARY_ADD       
              774  CALL_METHOD_1         1  ''
              776  STORE_FAST               'mod'

 L. 144       778  LOAD_GLOBAL              os
              780  LOAD_ATTR                path
              782  LOAD_METHOD              join
              784  LOAD_GLOBAL              os
              786  LOAD_ATTR                path
              788  LOAD_METHOD              abspath
              790  LOAD_GLOBAL              comtypes
              792  LOAD_ATTR                gen
              794  LOAD_ATTR                __path__
              796  LOAD_CONST               0
              798  BINARY_SUBSCR    
              800  CALL_METHOD_1         1  ''

 L. 145       802  LOAD_STR                 '<memory>'

 L. 144       804  CALL_METHOD_2         2  ''
              806  LOAD_FAST                'mod'
              808  STORE_ATTR               __file__

 L. 146       810  LOAD_GLOBAL              exec
              812  LOAD_FAST                'code'
              814  LOAD_FAST                'mod'
              816  LOAD_ATTR                __dict__
              818  CALL_FUNCTION_2       2  ''
              820  POP_TOP          

 L. 147       822  LOAD_FAST                'mod'
              824  LOAD_GLOBAL              sys
              826  LOAD_ATTR                modules
              828  LOAD_STR                 'comtypes.gen.'
              830  LOAD_FAST                'modulename'
              832  BINARY_ADD       
              834  STORE_SUBSCR     

 L. 148       836  LOAD_GLOBAL              setattr
              838  LOAD_GLOBAL              comtypes
              840  LOAD_ATTR                gen
              842  LOAD_FAST                'modulename'
              844  LOAD_FAST                'mod'
              846  CALL_FUNCTION_3       3  ''
              848  POP_TOP          

 L. 149       850  LOAD_FAST                'mod'
              852  RETURN_VALUE     
            854_0  COME_FROM           760  '760'

 L. 151       854  LOAD_GLOBAL              open
              856  LOAD_GLOBAL              os
              858  LOAD_ATTR                path
              860  LOAD_METHOD              join
              862  LOAD_GLOBAL              comtypes
              864  LOAD_ATTR                client
              866  LOAD_ATTR                gen_dir
              868  LOAD_FAST                'modulename'
              870  LOAD_STR                 '.py'
              872  BINARY_ADD       
              874  CALL_METHOD_2         2  ''
              876  LOAD_STR                 'w'
              878  CALL_FUNCTION_2       2  ''
              880  STORE_FAST               'ofi'

 L. 152       882  LOAD_FAST                'ofi'
              884  LOAD_METHOD              write
              886  LOAD_FAST                'code'
              888  CALL_METHOD_1         1  ''
              890  POP_TOP          

 L. 153       892  LOAD_FAST                'ofi'
              894  LOAD_METHOD              close
              896  CALL_METHOD_0         0  ''
              898  POP_TOP          

 L. 155       900  LOAD_GLOBAL              hasattr
              902  LOAD_GLOBAL              importlib
              904  LOAD_STR                 'invalidate_caches'
              906  CALL_FUNCTION_2       2  ''
          908_910  POP_JUMP_IF_FALSE   920  'to 920'

 L. 156       912  LOAD_GLOBAL              importlib
              914  LOAD_METHOD              invalidate_caches
              916  CALL_METHOD_0         0  ''
              918  POP_TOP          
            920_0  COME_FROM           908  '908'

 L. 157       920  LOAD_GLOBAL              _my_import
              922  LOAD_STR                 'comtypes.gen.'
              924  LOAD_FAST                'modulename'
              926  BINARY_ADD       
              928  CALL_FUNCTION_1       1  ''
              930  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 54


def _CreateWrapper--- This code section failed: ---

 L. 161         0  LOAD_GLOBAL              _name_module
                2  LOAD_FAST                'tlib'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'fullname'

 L. 162         8  SETUP_FINALLY        22  'to 22'

 L. 163        10  LOAD_GLOBAL              sys
               12  LOAD_ATTR                modules
               14  LOAD_FAST                'fullname'
               16  BINARY_SUBSCR    
               18  POP_BLOCK        
               20  RETURN_VALUE     
             22_0  COME_FROM_FINALLY     8  '8'

 L. 164        22  DUP_TOP          
               24  LOAD_GLOBAL              KeyError
               26  <121>                38  ''
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 165        34  POP_EXCEPT       
               36  JUMP_FORWARD         40  'to 40'
               38  <48>             
             40_0  COME_FROM            36  '36'

 L. 167        40  LOAD_FAST                'fullname'
               42  LOAD_METHOD              split
               44  LOAD_STR                 '.'
               46  CALL_METHOD_1         1  ''
               48  LOAD_CONST               -1
               50  BINARY_SUBSCR    
               52  STORE_FAST               'modname'

 L. 169        54  SETUP_FINALLY        66  'to 66'

 L. 170        56  LOAD_GLOBAL              _my_import
               58  LOAD_FAST                'fullname'
               60  CALL_FUNCTION_1       1  ''
               62  POP_BLOCK        
               64  RETURN_VALUE     
             66_0  COME_FROM_FINALLY    54  '54'

 L. 171        66  DUP_TOP          
               68  LOAD_GLOBAL              Exception
               70  <121>               114  ''
               72  POP_TOP          
               74  STORE_FAST               'details'
               76  POP_TOP          
               78  SETUP_FINALLY       106  'to 106'

 L. 172        80  LOAD_GLOBAL              logger
               82  LOAD_METHOD              info
               84  LOAD_STR                 'Could not import %s: %s'
               86  LOAD_FAST                'fullname'
               88  LOAD_FAST                'details'
               90  CALL_METHOD_3         3  ''
               92  POP_TOP          
               94  POP_BLOCK        
               96  POP_EXCEPT       
               98  LOAD_CONST               None
              100  STORE_FAST               'details'
              102  DELETE_FAST              'details'
              104  JUMP_FORWARD        116  'to 116'
            106_0  COME_FROM_FINALLY    78  '78'
              106  LOAD_CONST               None
              108  STORE_FAST               'details'
              110  DELETE_FAST              'details'
              112  <48>             
              114  <48>             
            116_0  COME_FROM           104  '104'

 L. 175       116  LOAD_CONST               0
              118  LOAD_CONST               ('generate_module',)
              120  IMPORT_NAME_ATTR         comtypes.tools.tlbparser
              122  IMPORT_FROM              generate_module
              124  STORE_FAST               'generate_module'
              126  POP_TOP          

 L. 176       128  LOAD_GLOBAL              comtypes
              130  LOAD_ATTR                client
              132  LOAD_ATTR                gen_dir
              134  LOAD_CONST               None
              136  <117>                 0  ''
              138  POP_JUMP_IF_FALSE   158  'to 158'

 L. 177       140  LOAD_CONST               0
              142  LOAD_CONST               None
              144  IMPORT_NAME              io
              146  STORE_FAST               'io'

 L. 178       148  LOAD_FAST                'io'
              150  LOAD_METHOD              StringIO
              152  CALL_METHOD_0         0  ''
              154  STORE_FAST               'ofi'
              156  JUMP_FORWARD        186  'to 186'
            158_0  COME_FROM           138  '138'

 L. 180       158  LOAD_GLOBAL              open
              160  LOAD_GLOBAL              os
              162  LOAD_ATTR                path
              164  LOAD_METHOD              join
              166  LOAD_GLOBAL              comtypes
              168  LOAD_ATTR                client
              170  LOAD_ATTR                gen_dir
              172  LOAD_FAST                'modname'
              174  LOAD_STR                 '.py'
              176  BINARY_ADD       
              178  CALL_METHOD_2         2  ''
              180  LOAD_STR                 'w'
              182  CALL_FUNCTION_2       2  ''
              184  STORE_FAST               'ofi'
            186_0  COME_FROM           156  '156'

 L. 182       186  LOAD_GLOBAL              logger
              188  LOAD_METHOD              info
              190  LOAD_STR                 '# Generating comtypes.gen.%s'
              192  LOAD_FAST                'modname'
              194  CALL_METHOD_2         2  ''
              196  POP_TOP          

 L. 183       198  LOAD_FAST                'generate_module'
              200  LOAD_FAST                'tlib'
              202  LOAD_FAST                'ofi'
              204  LOAD_FAST                'pathname'
              206  CALL_FUNCTION_3       3  ''
              208  POP_TOP          

 L. 185       210  LOAD_GLOBAL              comtypes
              212  LOAD_ATTR                client
              214  LOAD_ATTR                gen_dir
              216  LOAD_CONST               None
              218  <117>                 0  ''
          220_222  POP_JUMP_IF_FALSE   312  'to 312'

 L. 186       224  LOAD_FAST                'ofi'
              226  LOAD_METHOD              getvalue
              228  CALL_METHOD_0         0  ''
              230  STORE_FAST               'code'

 L. 187       232  LOAD_GLOBAL              types
              234  LOAD_METHOD              ModuleType
              236  LOAD_FAST                'fullname'
              238  CALL_METHOD_1         1  ''
              240  STORE_FAST               'mod'

 L. 188       242  LOAD_GLOBAL              os
              244  LOAD_ATTR                path
              246  LOAD_METHOD              join
              248  LOAD_GLOBAL              os
              250  LOAD_ATTR                path
              252  LOAD_METHOD              abspath
              254  LOAD_GLOBAL              comtypes
              256  LOAD_ATTR                gen
              258  LOAD_ATTR                __path__
              260  LOAD_CONST               0
              262  BINARY_SUBSCR    
              264  CALL_METHOD_1         1  ''

 L. 189       266  LOAD_STR                 '<memory>'

 L. 188       268  CALL_METHOD_2         2  ''
              270  LOAD_FAST                'mod'
              272  STORE_ATTR               __file__

 L. 190       274  LOAD_GLOBAL              exec
              276  LOAD_FAST                'code'
              278  LOAD_FAST                'mod'
              280  LOAD_ATTR                __dict__
              282  CALL_FUNCTION_2       2  ''
              284  POP_TOP          

 L. 191       286  LOAD_FAST                'mod'
              288  LOAD_GLOBAL              sys
              290  LOAD_ATTR                modules
              292  LOAD_FAST                'fullname'
              294  STORE_SUBSCR     

 L. 192       296  LOAD_GLOBAL              setattr
              298  LOAD_GLOBAL              comtypes
              300  LOAD_ATTR                gen
              302  LOAD_FAST                'modname'
              304  LOAD_FAST                'mod'
              306  CALL_FUNCTION_3       3  ''
              308  POP_TOP          
              310  JUMP_FORWARD        348  'to 348'
            312_0  COME_FROM           220  '220'

 L. 194       312  LOAD_FAST                'ofi'
              314  LOAD_METHOD              close
              316  CALL_METHOD_0         0  ''
              318  POP_TOP          

 L. 196       320  LOAD_GLOBAL              hasattr
              322  LOAD_GLOBAL              importlib
              324  LOAD_STR                 'invalidate_caches'
              326  CALL_FUNCTION_2       2  ''
          328_330  POP_JUMP_IF_FALSE   340  'to 340'

 L. 197       332  LOAD_GLOBAL              importlib
              334  LOAD_METHOD              invalidate_caches
              336  CALL_METHOD_0         0  ''
              338  POP_TOP          
            340_0  COME_FROM           328  '328'

 L. 198       340  LOAD_GLOBAL              _my_import
              342  LOAD_FAST                'fullname'
              344  CALL_FUNCTION_1       1  ''
              346  STORE_FAST               'mod'
            348_0  COME_FROM           310  '310'

 L. 199       348  LOAD_FAST                'mod'
              350  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 26


if __name__ == '__main__':
    GetModule(sys.argv[1])