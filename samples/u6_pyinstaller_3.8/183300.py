# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\win32\lib\pywintypes.py
import imp, sys, os

def __import_pywin32_system_module__--- This code section failed: ---

 L.  20         0  LOAD_GLOBAL              sys
                2  LOAD_ATTR                platform
                4  LOAD_METHOD              startswith
                6  LOAD_STR                 'win32'
                8  CALL_METHOD_1         1  ''
               10  POP_JUMP_IF_TRUE    142  'to 142'

 L.  25        12  LOAD_GLOBAL              imp
               14  LOAD_METHOD              get_suffixes
               16  CALL_METHOD_0         0  ''
               18  GET_ITER         
             20_0  COME_FROM            38  '38'
               20  FOR_ITER            130  'to 130'
               22  UNPACK_SEQUENCE_3     3 
               24  STORE_FAST               'ext'
               26  STORE_FAST               'mode'
               28  STORE_FAST               'ext_type'

 L.  26        30  LOAD_FAST                'ext_type'
               32  LOAD_GLOBAL              imp
               34  LOAD_ATTR                C_EXTENSION
               36  COMPARE_OP               ==
               38  POP_JUMP_IF_FALSE    20  'to 20'

 L.  27        40  LOAD_GLOBAL              sys
               42  LOAD_ATTR                path
               44  GET_ITER         
             46_0  COME_FROM            82  '82'
               46  FOR_ITER            128  'to 128'
               48  STORE_FAST               'path'

 L.  28        50  LOAD_GLOBAL              os
               52  LOAD_ATTR                path
               54  LOAD_METHOD              join
               56  LOAD_FAST                'path'
               58  LOAD_STR                 'lib'
               60  LOAD_FAST                'modname'
               62  BINARY_ADD       
               64  LOAD_FAST                'ext'
               66  BINARY_ADD       
               68  CALL_METHOD_2         2  ''
               70  STORE_FAST               'look'

 L.  29        72  LOAD_GLOBAL              os
               74  LOAD_ATTR                path
               76  LOAD_METHOD              isfile
               78  LOAD_FAST                'look'
               80  CALL_METHOD_1         1  ''
               82  POP_JUMP_IF_FALSE    46  'to 46'

 L.  30        84  LOAD_GLOBAL              imp
               86  LOAD_METHOD              load_module
               88  LOAD_FAST                'modname'
               90  LOAD_CONST               None
               92  LOAD_FAST                'look'

 L.  31        94  LOAD_FAST                'ext'
               96  LOAD_FAST                'mode'
               98  LOAD_FAST                'ext_type'
              100  BUILD_TUPLE_3         3 

 L.  30       102  CALL_METHOD_4         4  ''
              104  STORE_FAST               'mod'

 L.  35       106  LOAD_FAST                'globs'
              108  LOAD_METHOD              update
              110  LOAD_FAST                'mod'
              112  LOAD_ATTR                __dict__
              114  CALL_METHOD_1         1  ''
              116  POP_TOP          

 L.  36       118  POP_TOP          
              120  POP_TOP          
              122  LOAD_CONST               None
              124  RETURN_VALUE     
              126  JUMP_BACK            46  'to 46'
              128  JUMP_BACK            20  'to 20'

 L.  37       130  LOAD_GLOBAL              ImportError
              132  LOAD_STR                 'No dynamic module '
              134  LOAD_FAST                'modname'
              136  BINARY_ADD       
              138  CALL_FUNCTION_1       1  ''
              140  RAISE_VARARGS_1       1  'exception instance'
            142_0  COME_FROM            10  '10'

 L.  39       142  LOAD_GLOBAL              imp
              144  LOAD_METHOD              get_suffixes
              146  CALL_METHOD_0         0  ''
              148  GET_ITER         
            150_0  COME_FROM           164  '164'
              150  FOR_ITER            176  'to 176'
              152  STORE_FAST               'suffix_item'

 L.  40       154  LOAD_FAST                'suffix_item'
              156  LOAD_CONST               0
              158  BINARY_SUBSCR    
              160  LOAD_STR                 '_d.pyd'
              162  COMPARE_OP               ==
              164  POP_JUMP_IF_FALSE   150  'to 150'

 L.  41       166  LOAD_STR                 '_d'
              168  STORE_FAST               'suffix'

 L.  42       170  POP_TOP          
              172  BREAK_LOOP          180  'to 180'
              174  JUMP_BACK           150  'to 150'

 L.  44       176  LOAD_STR                 ''
              178  STORE_FAST               'suffix'

 L.  45       180  LOAD_STR                 '%s%d%d%s.dll'

 L.  46       182  LOAD_FAST                'modname'
              184  LOAD_GLOBAL              sys
              186  LOAD_ATTR                version_info
              188  LOAD_CONST               0
              190  BINARY_SUBSCR    
              192  LOAD_GLOBAL              sys
              194  LOAD_ATTR                version_info
              196  LOAD_CONST               1
              198  BINARY_SUBSCR    
              200  LOAD_FAST                'suffix'
              202  BUILD_TUPLE_4         4 

 L.  45       204  BINARY_MODULO    
              206  STORE_FAST               'filename'

 L.  47       208  LOAD_GLOBAL              hasattr
              210  LOAD_GLOBAL              sys
              212  LOAD_STR                 'frozen'
              214  CALL_FUNCTION_2       2  ''
          216_218  POP_JUMP_IF_FALSE   308  'to 308'

 L.  52       220  LOAD_GLOBAL              sys
              222  LOAD_ATTR                path
              224  GET_ITER         
            226_0  COME_FROM           278  '278'
              226  FOR_ITER            288  'to 288'
              228  STORE_FAST               'look'

 L.  55       230  LOAD_GLOBAL              os
              232  LOAD_ATTR                path
              234  LOAD_METHOD              isfile
              236  LOAD_FAST                'look'
              238  CALL_METHOD_1         1  ''
              240  POP_JUMP_IF_FALSE   254  'to 254'

 L.  56       242  LOAD_GLOBAL              os
              244  LOAD_ATTR                path
              246  LOAD_METHOD              dirname
              248  LOAD_FAST                'look'
              250  CALL_METHOD_1         1  ''
              252  STORE_FAST               'look'
            254_0  COME_FROM           240  '240'

 L.  57       254  LOAD_GLOBAL              os
              256  LOAD_ATTR                path
              258  LOAD_METHOD              join
              260  LOAD_FAST                'look'
              262  LOAD_FAST                'filename'
              264  CALL_METHOD_2         2  ''
              266  STORE_FAST               'found'

 L.  58       268  LOAD_GLOBAL              os
              270  LOAD_ATTR                path
              272  LOAD_METHOD              isfile
              274  LOAD_FAST                'found'
              276  CALL_METHOD_1         1  ''
              278  POP_JUMP_IF_FALSE   226  'to 226'

 L.  59       280  POP_TOP          
          282_284  BREAK_LOOP          550  'to 550'
              286  JUMP_BACK           226  'to 226'

 L.  61       288  LOAD_GLOBAL              ImportError
              290  LOAD_STR                 "Module '%s' isn't in frozen sys.path %s"
              292  LOAD_FAST                'modname'
              294  LOAD_GLOBAL              sys
              296  LOAD_ATTR                path
              298  BUILD_TUPLE_2         2 
              300  BINARY_MODULO    
              302  CALL_FUNCTION_1       1  ''
              304  RAISE_VARARGS_1       1  'exception instance'
              306  JUMP_FORWARD        550  'to 550'
            308_0  COME_FROM           216  '216'

 L.  64       308  LOAD_CONST               0
              310  LOAD_CONST               None
              312  IMPORT_NAME              _win32sysloader
              314  STORE_FAST               '_win32sysloader'

 L.  65       316  LOAD_FAST                '_win32sysloader'
              318  LOAD_METHOD              GetModuleFilename
              320  LOAD_FAST                'filename'
              322  CALL_METHOD_1         1  ''
              324  STORE_FAST               'found'

 L.  66       326  LOAD_FAST                'found'
              328  LOAD_CONST               None
              330  COMPARE_OP               is
          332_334  POP_JUMP_IF_FALSE   346  'to 346'

 L.  79       336  LOAD_FAST                '_win32sysloader'
              338  LOAD_METHOD              LoadModule
              340  LOAD_FAST                'filename'
              342  CALL_METHOD_1         1  ''
              344  STORE_FAST               'found'
            346_0  COME_FROM           332  '332'

 L.  80       346  LOAD_FAST                'found'
              348  LOAD_CONST               None
              350  COMPARE_OP               is
          352_354  POP_JUMP_IF_FALSE   398  'to 398'

 L.  89       356  LOAD_GLOBAL              os
              358  LOAD_ATTR                path
              360  LOAD_METHOD              isfile
              362  LOAD_GLOBAL              os
              364  LOAD_ATTR                path
              366  LOAD_METHOD              join
              368  LOAD_GLOBAL              sys
              370  LOAD_ATTR                prefix
              372  LOAD_FAST                'filename'
              374  CALL_METHOD_2         2  ''
              376  CALL_METHOD_1         1  ''
          378_380  POP_JUMP_IF_FALSE   398  'to 398'

 L.  90       382  LOAD_GLOBAL              os
              384  LOAD_ATTR                path
              386  LOAD_METHOD              join
              388  LOAD_GLOBAL              sys
              390  LOAD_ATTR                prefix
              392  LOAD_FAST                'filename'
              394  CALL_METHOD_2         2  ''
              396  STORE_FAST               'found'
            398_0  COME_FROM           378  '378'
            398_1  COME_FROM           352  '352'

 L.  91       398  LOAD_FAST                'found'
              400  LOAD_CONST               None
              402  COMPARE_OP               is
          404_406  POP_JUMP_IF_FALSE   462  'to 462'

 L.  94       408  LOAD_GLOBAL              os
              410  LOAD_ATTR                path
              412  LOAD_METHOD              isfile
              414  LOAD_GLOBAL              os
              416  LOAD_ATTR                path
              418  LOAD_METHOD              join
              420  LOAD_GLOBAL              os
              422  LOAD_ATTR                path
              424  LOAD_METHOD              dirname
              426  LOAD_GLOBAL              __file__
              428  CALL_METHOD_1         1  ''
              430  LOAD_FAST                'filename'
              432  CALL_METHOD_2         2  ''
              434  CALL_METHOD_1         1  ''
          436_438  POP_JUMP_IF_FALSE   462  'to 462'

 L.  95       440  LOAD_GLOBAL              os
              442  LOAD_ATTR                path
              444  LOAD_METHOD              join
              446  LOAD_GLOBAL              os
              448  LOAD_ATTR                path
              450  LOAD_METHOD              dirname
              452  LOAD_GLOBAL              __file__
              454  CALL_METHOD_1         1  ''
              456  LOAD_FAST                'filename'
              458  CALL_METHOD_2         2  ''
              460  STORE_FAST               'found'
            462_0  COME_FROM           436  '436'
            462_1  COME_FROM           404  '404'

 L.  96       462  LOAD_FAST                'found'
              464  LOAD_CONST               None
              466  COMPARE_OP               is
          468_470  POP_JUMP_IF_FALSE   524  'to 524'

 L. 103       472  LOAD_CONST               0
              474  LOAD_CONST               None
              476  IMPORT_NAME_ATTR         distutils.sysconfig
              478  STORE_FAST               'distutils'

 L. 104       480  LOAD_GLOBAL              os
              482  LOAD_ATTR                path
              484  LOAD_METHOD              join
              486  LOAD_FAST                'distutils'
              488  LOAD_ATTR                sysconfig
              490  LOAD_ATTR                get_python_lib
              492  LOAD_CONST               1
              494  LOAD_CONST               ('plat_specific',)
              496  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L. 105       498  LOAD_STR                 'pywin32_system32'

 L. 105       500  LOAD_FAST                'filename'

 L. 104       502  CALL_METHOD_3         3  ''
              504  STORE_FAST               'maybe'

 L. 106       506  LOAD_GLOBAL              os
              508  LOAD_ATTR                path
              510  LOAD_METHOD              isfile
              512  LOAD_FAST                'maybe'
              514  CALL_METHOD_1         1  ''
          516_518  POP_JUMP_IF_FALSE   524  'to 524'

 L. 107       520  LOAD_FAST                'maybe'
              522  STORE_FAST               'found'
            524_0  COME_FROM           516  '516'
            524_1  COME_FROM           468  '468'

 L. 108       524  LOAD_FAST                'found'
              526  LOAD_CONST               None
              528  COMPARE_OP               is
          530_532  POP_JUMP_IF_FALSE   550  'to 550'

 L. 110       534  LOAD_GLOBAL              ImportError
              536  LOAD_STR                 "No system module '%s' (%s)"
              538  LOAD_FAST                'modname'
              540  LOAD_FAST                'filename'
              542  BUILD_TUPLE_2         2 
              544  BINARY_MODULO    
              546  CALL_FUNCTION_1       1  ''
              548  RAISE_VARARGS_1       1  'exception instance'
            550_0  COME_FROM           530  '530'
            550_1  COME_FROM           306  '306'

 L. 121       550  LOAD_GLOBAL              sys
              552  LOAD_ATTR                modules
              554  LOAD_FAST                'modname'
              556  BINARY_SUBSCR    
              558  STORE_FAST               'old_mod'

 L. 123       560  LOAD_GLOBAL              imp
              562  LOAD_METHOD              load_dynamic
              564  LOAD_FAST                'modname'
              566  LOAD_FAST                'found'
              568  CALL_METHOD_2         2  ''
              570  STORE_FAST               'mod'

 L. 125       572  LOAD_GLOBAL              sys
              574  LOAD_ATTR                version_info
              576  LOAD_CONST               (3, 0)
              578  COMPARE_OP               <
          580_582  POP_JUMP_IF_FALSE   620  'to 620'

 L. 126       584  LOAD_GLOBAL              sys
              586  LOAD_ATTR                modules
              588  LOAD_FAST                'modname'
              590  BINARY_SUBSCR    
              592  LOAD_FAST                'old_mod'
              594  COMPARE_OP               is
          596_598  POP_JUMP_IF_TRUE    604  'to 604'
              600  LOAD_ASSERT              AssertionError
              602  RAISE_VARARGS_1       1  'exception instance'
            604_0  COME_FROM           596  '596'

 L. 127       604  LOAD_FAST                'mod'
              606  LOAD_FAST                'old_mod'
              608  COMPARE_OP               is
          610_612  POP_JUMP_IF_TRUE    682  'to 682'
              614  LOAD_GLOBAL              AssertionError
              616  RAISE_VARARGS_1       1  'exception instance'
              618  JUMP_FORWARD        682  'to 682'
            620_0  COME_FROM           580  '580'

 L. 129       620  LOAD_GLOBAL              sys
              622  LOAD_ATTR                modules
              624  LOAD_FAST                'modname'
              626  BINARY_SUBSCR    
              628  LOAD_FAST                'old_mod'
              630  COMPARE_OP               is-not
          632_634  POP_JUMP_IF_TRUE    640  'to 640'
              636  LOAD_ASSERT              AssertionError
              638  RAISE_VARARGS_1       1  'exception instance'
            640_0  COME_FROM           632  '632'

 L. 130       640  LOAD_GLOBAL              sys
              642  LOAD_ATTR                modules
              644  LOAD_FAST                'modname'
              646  BINARY_SUBSCR    
              648  LOAD_FAST                'mod'
              650  COMPARE_OP               is
          652_654  POP_JUMP_IF_TRUE    660  'to 660'
              656  LOAD_ASSERT              AssertionError
              658  RAISE_VARARGS_1       1  'exception instance'
            660_0  COME_FROM           652  '652'

 L. 132       660  LOAD_FAST                'old_mod'
              662  LOAD_GLOBAL              sys
              664  LOAD_ATTR                modules
              666  LOAD_FAST                'modname'
              668  STORE_SUBSCR     

 L. 133       670  LOAD_FAST                'globs'
              672  LOAD_METHOD              update
              674  LOAD_FAST                'mod'
              676  LOAD_ATTR                __dict__
              678  CALL_METHOD_1         1  ''
              680  POP_TOP          
            682_0  COME_FROM           618  '618'
            682_1  COME_FROM           610  '610'

Parse error at or near `POP_TOP' instruction at offset 120


__import_pywin32_system_module__('pywintypes', globals())