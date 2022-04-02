# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.11 (default, Sep  3 2021, 20:46:09) 
# [GCC 10.2.1 20210110]
# Embedded file name: distutils\command\build_scripts.py
"""distutils.command.build_scripts

Implements the Distutils 'build_scripts' command."""
import os, re
from stat import ST_MODE
from distutils import sysconfig
from distutils.core import Command
from distutils.dep_util import newer
from distutils.util import convert_path, Mixin2to3
from distutils import log
import tokenize
first_line_re = re.compile(b'^#!.*python[0-9.]*([ \t].*)?$')

class build_scripts(Command):
    description = '"build" scripts (copy and fixup #! line)'
    user_options = [
     ('build-dir=', 'd', 'directory to "build" (copy) to'),
     ('force', 'f', 'forcibly build everything (ignore file timestamps'),
     ('executable=', 'e', 'specify final destination interpreter path')]
    boolean_options = [
     'force']

    def initialize_options(self):
        self.build_dir = None
        self.scripts = None
        self.force = None
        self.executable = None
        self.outfiles = None

    def finalize_options(self):
        self.set_undefined_options('build', ('build_scripts', 'build_dir'), ('force',
                                                                             'force'), ('executable',
                                                                                        'executable'))
        self.scripts = self.distribution.scripts

    def get_source_files(self):
        return self.scripts

    def run(self):
        if not self.scripts:
            return
        self.copy_scripts()

    def copy_scripts--- This code section failed: ---

 L.  59         0  LOAD_FAST                'self'
                2  LOAD_METHOD              mkpath
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                build_dir
                8  CALL_METHOD_1         1  '1 positional argument'
               10  POP_TOP          

 L.  60        12  BUILD_LIST_0          0 
               14  STORE_FAST               'outfiles'

 L.  61        16  BUILD_LIST_0          0 
               18  STORE_FAST               'updated_files'

 L.  62     20_22  SETUP_LOOP          576  'to 576'
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                scripts
               28  GET_ITER         
             30_0  COME_FROM           572  '572'
             30_1  COME_FROM           534  '534'
             30_2  COME_FROM           212  '212'
             30_3  COME_FROM           110  '110'
            30_32  FOR_ITER            574  'to 574'
               34  STORE_FAST               'script'

 L.  63        36  LOAD_CONST               False
               38  STORE_FAST               'adjust'

 L.  64        40  LOAD_GLOBAL              convert_path
               42  LOAD_FAST                'script'
               44  CALL_FUNCTION_1       1  '1 positional argument'
               46  STORE_FAST               'script'

 L.  65        48  LOAD_GLOBAL              os
               50  LOAD_ATTR                path
               52  LOAD_METHOD              join
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                build_dir
               58  LOAD_GLOBAL              os
               60  LOAD_ATTR                path
               62  LOAD_METHOD              basename
               64  LOAD_FAST                'script'
               66  CALL_METHOD_1         1  '1 positional argument'
               68  CALL_METHOD_2         2  '2 positional arguments'
               70  STORE_FAST               'outfile'

 L.  66        72  LOAD_FAST                'outfiles'
               74  LOAD_METHOD              append
               76  LOAD_FAST                'outfile'
               78  CALL_METHOD_1         1  '1 positional argument'
               80  POP_TOP          

 L.  68        82  LOAD_FAST                'self'
               84  LOAD_ATTR                force
               86  POP_JUMP_IF_TRUE    112  'to 112'
               88  LOAD_GLOBAL              newer
               90  LOAD_FAST                'script'
               92  LOAD_FAST                'outfile'
               94  CALL_FUNCTION_2       2  '2 positional arguments'
               96  POP_JUMP_IF_TRUE    112  'to 112'

 L.  69        98  LOAD_GLOBAL              log
              100  LOAD_METHOD              debug
              102  LOAD_STR                 'not copying %s (up-to-date)'
              104  LOAD_FAST                'script'
              106  CALL_METHOD_2         2  '2 positional arguments'
              108  POP_TOP          

 L.  70       110  CONTINUE             30  'to 30'
            112_0  COME_FROM            96  '96'
            112_1  COME_FROM            86  '86'

 L.  75       112  SETUP_EXCEPT        128  'to 128'

 L.  76       114  LOAD_GLOBAL              open
              116  LOAD_FAST                'script'
              118  LOAD_STR                 'rb'
              120  CALL_FUNCTION_2       2  '2 positional arguments'
              122  STORE_FAST               'f'
              124  POP_BLOCK        
              126  JUMP_FORWARD        160  'to 160'
            128_0  COME_FROM_EXCEPT    112  '112'

 L.  77       128  DUP_TOP          
              130  LOAD_GLOBAL              OSError
              132  COMPARE_OP               exception-match
              134  POP_JUMP_IF_FALSE   158  'to 158'
              136  POP_TOP          
              138  POP_TOP          
              140  POP_TOP          

 L.  78       142  LOAD_FAST                'self'
              144  LOAD_ATTR                dry_run
              146  POP_JUMP_IF_TRUE    150  'to 150'

 L.  79       148  RAISE_VARARGS_0       0  'reraise'
            150_0  COME_FROM           146  '146'

 L.  80       150  LOAD_CONST               None
              152  STORE_FAST               'f'
              154  POP_EXCEPT       
              156  JUMP_FORWARD        246  'to 246'
            158_0  COME_FROM           134  '134'
              158  END_FINALLY      
            160_0  COME_FROM           126  '126'

 L.  82       160  LOAD_GLOBAL              tokenize
              162  LOAD_METHOD              detect_encoding
              164  LOAD_FAST                'f'
              166  LOAD_ATTR                readline
              168  CALL_METHOD_1         1  '1 positional argument'
              170  UNPACK_SEQUENCE_2     2 
              172  STORE_FAST               'encoding'
              174  STORE_FAST               'lines'

 L.  83       176  LOAD_FAST                'f'
              178  LOAD_METHOD              seek
              180  LOAD_CONST               0
              182  CALL_METHOD_1         1  '1 positional argument'
              184  POP_TOP          

 L.  84       186  LOAD_FAST                'f'
              188  LOAD_METHOD              readline
              190  CALL_METHOD_0         0  '0 positional arguments'
              192  STORE_FAST               'first_line'

 L.  85       194  LOAD_FAST                'first_line'
              196  POP_JUMP_IF_TRUE    214  'to 214'

 L.  86       198  LOAD_FAST                'self'
              200  LOAD_METHOD              warn
              202  LOAD_STR                 '%s is an empty file (skipping)'
              204  LOAD_FAST                'script'
              206  BINARY_MODULO    
              208  CALL_METHOD_1         1  '1 positional argument'
              210  POP_TOP          

 L.  87       212  CONTINUE             30  'to 30'
            214_0  COME_FROM           196  '196'

 L.  89       214  LOAD_GLOBAL              first_line_re
              216  LOAD_METHOD              match
              218  LOAD_FAST                'first_line'
              220  CALL_METHOD_1         1  '1 positional argument'
              222  STORE_FAST               'match'

 L.  90       224  LOAD_FAST                'match'
              226  POP_JUMP_IF_FALSE   246  'to 246'

 L.  91       228  LOAD_CONST               True
              230  STORE_FAST               'adjust'

 L.  92       232  LOAD_FAST                'match'
              234  LOAD_METHOD              group
              236  LOAD_CONST               1
              238  CALL_METHOD_1         1  '1 positional argument'
              240  JUMP_IF_TRUE_OR_POP   244  'to 244'
              242  LOAD_CONST               b''
            244_0  COME_FROM           240  '240'
              244  STORE_FAST               'post_interp'
            246_0  COME_FROM           226  '226'
            246_1  COME_FROM           156  '156'

 L.  94       246  LOAD_FAST                'adjust'
          248_250  POP_JUMP_IF_FALSE   536  'to 536'

 L.  95       252  LOAD_GLOBAL              log
              254  LOAD_METHOD              info
              256  LOAD_STR                 'copying and adjusting %s -> %s'
              258  LOAD_FAST                'script'

 L.  96       260  LOAD_FAST                'self'
              262  LOAD_ATTR                build_dir
              264  CALL_METHOD_3         3  '3 positional arguments'
              266  POP_TOP          

 L.  97       268  LOAD_FAST                'updated_files'
              270  LOAD_METHOD              append
              272  LOAD_FAST                'outfile'
              274  CALL_METHOD_1         1  '1 positional argument'
              276  POP_TOP          

 L.  98       278  LOAD_FAST                'self'
              280  LOAD_ATTR                dry_run
          282_284  POP_JUMP_IF_TRUE    520  'to 520'

 L.  99       286  LOAD_GLOBAL              sysconfig
              288  LOAD_ATTR                python_build
          290_292  POP_JUMP_IF_TRUE    302  'to 302'

 L. 100       294  LOAD_FAST                'self'
              296  LOAD_ATTR                executable
              298  STORE_FAST               'executable'
              300  JUMP_FORWARD        342  'to 342'
            302_0  COME_FROM           290  '290'

 L. 102       302  LOAD_GLOBAL              os
              304  LOAD_ATTR                path
              306  LOAD_METHOD              join

 L. 103       308  LOAD_GLOBAL              sysconfig
              310  LOAD_METHOD              get_config_var
              312  LOAD_STR                 'BINDIR'
              314  CALL_METHOD_1         1  '1 positional argument'

 L. 104       316  LOAD_STR                 'python%s%s'
              318  LOAD_GLOBAL              sysconfig
              320  LOAD_METHOD              get_config_var
              322  LOAD_STR                 'VERSION'
              324  CALL_METHOD_1         1  '1 positional argument'

 L. 105       326  LOAD_GLOBAL              sysconfig
              328  LOAD_METHOD              get_config_var
              330  LOAD_STR                 'EXE'
              332  CALL_METHOD_1         1  '1 positional argument'
              334  BUILD_TUPLE_2         2 
              336  BINARY_MODULO    
              338  CALL_METHOD_2         2  '2 positional arguments'
              340  STORE_FAST               'executable'
            342_0  COME_FROM           300  '300'

 L. 106       342  LOAD_GLOBAL              os
              344  LOAD_METHOD              fsencode
              346  LOAD_FAST                'executable'
              348  CALL_METHOD_1         1  '1 positional argument'
              350  STORE_FAST               'executable'

 L. 107       352  LOAD_CONST               b'#!'
              354  LOAD_FAST                'executable'
              356  BINARY_ADD       
              358  LOAD_FAST                'post_interp'
              360  BINARY_ADD       
              362  LOAD_CONST               b'\n'
              364  BINARY_ADD       
              366  STORE_FAST               'shebang'

 L. 113       368  SETUP_EXCEPT        384  'to 384'

 L. 114       370  LOAD_FAST                'shebang'
              372  LOAD_METHOD              decode
              374  LOAD_STR                 'utf-8'
              376  CALL_METHOD_1         1  '1 positional argument'
              378  POP_TOP          
              380  POP_BLOCK        
              382  JUMP_FORWARD        420  'to 420'
            384_0  COME_FROM_EXCEPT    368  '368'

 L. 115       384  DUP_TOP          
              386  LOAD_GLOBAL              UnicodeDecodeError
              388  COMPARE_OP               exception-match
          390_392  POP_JUMP_IF_FALSE   418  'to 418'
              394  POP_TOP          
              396  POP_TOP          
              398  POP_TOP          

 L. 116       400  LOAD_GLOBAL              ValueError

 L. 117       402  LOAD_STR                 'The shebang ({!r}) is not decodable from utf-8'
              404  LOAD_METHOD              format

 L. 118       406  LOAD_FAST                'shebang'
              408  CALL_METHOD_1         1  '1 positional argument'
              410  CALL_FUNCTION_1       1  '1 positional argument'
              412  RAISE_VARARGS_1       1  'exception instance'
              414  POP_EXCEPT       
              416  JUMP_FORWARD        420  'to 420'
            418_0  COME_FROM           390  '390'
              418  END_FINALLY      
            420_0  COME_FROM           416  '416'
            420_1  COME_FROM           382  '382'

 L. 122       420  SETUP_EXCEPT        436  'to 436'

 L. 123       422  LOAD_FAST                'shebang'
              424  LOAD_METHOD              decode
              426  LOAD_FAST                'encoding'
              428  CALL_METHOD_1         1  '1 positional argument'
              430  POP_TOP          
              432  POP_BLOCK        
              434  JUMP_FORWARD        474  'to 474'
            436_0  COME_FROM_EXCEPT    420  '420'

 L. 124       436  DUP_TOP          
              438  LOAD_GLOBAL              UnicodeDecodeError
              440  COMPARE_OP               exception-match
          442_444  POP_JUMP_IF_FALSE   472  'to 472'
              446  POP_TOP          
              448  POP_TOP          
              450  POP_TOP          

 L. 125       452  LOAD_GLOBAL              ValueError

 L. 126       454  LOAD_STR                 'The shebang ({!r}) is not decodable from the script encoding ({})'
              456  LOAD_METHOD              format

 L. 128       458  LOAD_FAST                'shebang'
              460  LOAD_FAST                'encoding'
              462  CALL_METHOD_2         2  '2 positional arguments'
              464  CALL_FUNCTION_1       1  '1 positional argument'
              466  RAISE_VARARGS_1       1  'exception instance'
              468  POP_EXCEPT       
              470  JUMP_FORWARD        474  'to 474'
            472_0  COME_FROM           442  '442'
              472  END_FINALLY      
            474_0  COME_FROM           470  '470'
            474_1  COME_FROM           434  '434'

 L. 129       474  LOAD_GLOBAL              open
              476  LOAD_FAST                'outfile'
              478  LOAD_STR                 'wb'
              480  CALL_FUNCTION_2       2  '2 positional arguments'
              482  SETUP_WITH          514  'to 514'
              484  STORE_FAST               'outf'

 L. 130       486  LOAD_FAST                'outf'
              488  LOAD_METHOD              write
              490  LOAD_FAST                'shebang'
              492  CALL_METHOD_1         1  '1 positional argument'
              494  POP_TOP          

 L. 131       496  LOAD_FAST                'outf'
              498  LOAD_METHOD              writelines
              500  LOAD_FAST                'f'
              502  LOAD_METHOD              readlines
              504  CALL_METHOD_0         0  '0 positional arguments'
              506  CALL_METHOD_1         1  '1 positional argument'
              508  POP_TOP          
              510  POP_BLOCK        
              512  LOAD_CONST               None
            514_0  COME_FROM_WITH      482  '482'
              514  WITH_CLEANUP_START
              516  WITH_CLEANUP_FINISH
              518  END_FINALLY      
            520_0  COME_FROM           282  '282'

 L. 132       520  LOAD_FAST                'f'
          522_524  POP_JUMP_IF_FALSE   572  'to 572'

 L. 133       526  LOAD_FAST                'f'
              528  LOAD_METHOD              close
              530  CALL_METHOD_0         0  '0 positional arguments'
              532  POP_TOP          
              534  JUMP_BACK            30  'to 30'
            536_0  COME_FROM           248  '248'

 L. 135       536  LOAD_FAST                'f'
          538_540  POP_JUMP_IF_FALSE   550  'to 550'

 L. 136       542  LOAD_FAST                'f'
              544  LOAD_METHOD              close
              546  CALL_METHOD_0         0  '0 positional arguments'
              548  POP_TOP          
            550_0  COME_FROM           538  '538'

 L. 137       550  LOAD_FAST                'updated_files'
              552  LOAD_METHOD              append
              554  LOAD_FAST                'outfile'
              556  CALL_METHOD_1         1  '1 positional argument'
              558  POP_TOP          

 L. 138       560  LOAD_FAST                'self'
              562  LOAD_METHOD              copy_file
              564  LOAD_FAST                'script'
              566  LOAD_FAST                'outfile'
              568  CALL_METHOD_2         2  '2 positional arguments'
              570  POP_TOP          
            572_0  COME_FROM           522  '522'
              572  JUMP_BACK            30  'to 30'
              574  POP_BLOCK        
            576_0  COME_FROM_LOOP       20  '20'

 L. 140       576  LOAD_GLOBAL              os
              578  LOAD_ATTR                name
              580  LOAD_STR                 'posix'
              582  COMPARE_OP               ==
          584_586  POP_JUMP_IF_FALSE   694  'to 694'

 L. 141       588  SETUP_LOOP          694  'to 694'
              590  LOAD_FAST                'outfiles'
              592  GET_ITER         
            594_0  COME_FROM           688  '688'
            594_1  COME_FROM           656  '656'
            594_2  COME_FROM           618  '618'
              594  FOR_ITER            692  'to 692'
              596  STORE_FAST               'file'

 L. 142       598  LOAD_FAST                'self'
              600  LOAD_ATTR                dry_run
          602_604  POP_JUMP_IF_FALSE   620  'to 620'

 L. 143       606  LOAD_GLOBAL              log
              608  LOAD_METHOD              info
              610  LOAD_STR                 'changing mode of %s'
              612  LOAD_FAST                'file'
              614  CALL_METHOD_2         2  '2 positional arguments'
              616  POP_TOP          
              618  JUMP_BACK           594  'to 594'
            620_0  COME_FROM           602  '602'

 L. 145       620  LOAD_GLOBAL              os
              622  LOAD_METHOD              stat
              624  LOAD_FAST                'file'
              626  CALL_METHOD_1         1  '1 positional argument'
              628  LOAD_GLOBAL              ST_MODE
              630  BINARY_SUBSCR    
              632  LOAD_CONST               4095
              634  BINARY_AND       
              636  STORE_FAST               'oldmode'

 L. 146       638  LOAD_FAST                'oldmode'
              640  LOAD_CONST               365
              642  BINARY_OR        
              644  LOAD_CONST               4095
              646  BINARY_AND       
              648  STORE_FAST               'newmode'

 L. 147       650  LOAD_FAST                'newmode'
              652  LOAD_FAST                'oldmode'
              654  COMPARE_OP               !=
          656_658  POP_JUMP_IF_FALSE_BACK   594  'to 594'

 L. 148       660  LOAD_GLOBAL              log
              662  LOAD_METHOD              info
              664  LOAD_STR                 'changing mode of %s from %o to %o'

 L. 149       666  LOAD_FAST                'file'
              668  LOAD_FAST                'oldmode'
              670  LOAD_FAST                'newmode'
              672  CALL_METHOD_4         4  '4 positional arguments'
              674  POP_TOP          

 L. 150       676  LOAD_GLOBAL              os
              678  LOAD_METHOD              chmod
              680  LOAD_FAST                'file'
              682  LOAD_FAST                'newmode'
              684  CALL_METHOD_2         2  '2 positional arguments'
              686  POP_TOP          
          688_690  JUMP_BACK           594  'to 594'
              692  POP_BLOCK        
            694_0  COME_FROM_LOOP      588  '588'
            694_1  COME_FROM           584  '584'

 L. 152       694  LOAD_FAST                'outfiles'
              696  LOAD_FAST                'updated_files'
              698  BUILD_TUPLE_2         2 
              700  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 534


class build_scripts_2to3(build_scripts, Mixin2to3):

    def copy_scripts(self):
        outfiles, updated_files = build_scripts.copy_scripts(self)
        if not self.dry_run:
            self.run_2to3(updated_files)
        return (outfiles, updated_files)