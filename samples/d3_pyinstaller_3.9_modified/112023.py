# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: setuptools\command\install_scripts.py
from distutils import log
import distutils.command.install_scripts as orig
from distutils.errors import DistutilsModuleError
import os, sys
from pkg_resources import Distribution, PathMetadata, ensure_directory

class install_scripts(orig.install_scripts):
    __doc__ = 'Do normal script install, plus any egg_info wrapper scripts'

    def initialize_options(self):
        orig.install_scripts.initialize_options(self)
        self.no_ep = False

    def run--- This code section failed: ---

 L.  18         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME_ATTR         setuptools.command.easy_install
                6  IMPORT_FROM              command
                8  ROT_TWO          
               10  POP_TOP          
               12  IMPORT_FROM              easy_install
               14  STORE_FAST               'ei'
               16  POP_TOP          

 L.  20        18  LOAD_FAST                'self'
               20  LOAD_METHOD              run_command
               22  LOAD_STR                 'egg_info'
               24  CALL_METHOD_1         1  ''
               26  POP_TOP          

 L.  21        28  LOAD_FAST                'self'
               30  LOAD_ATTR                distribution
               32  LOAD_ATTR                scripts
               34  POP_JUMP_IF_FALSE    50  'to 50'

 L.  22        36  LOAD_GLOBAL              orig
               38  LOAD_ATTR                install_scripts
               40  LOAD_METHOD              run
               42  LOAD_FAST                'self'
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          
               48  JUMP_FORWARD         56  'to 56'
             50_0  COME_FROM            34  '34'

 L.  24        50  BUILD_LIST_0          0 
               52  LOAD_FAST                'self'
               54  STORE_ATTR               outfiles
             56_0  COME_FROM            48  '48'

 L.  25        56  LOAD_FAST                'self'
               58  LOAD_ATTR                no_ep
               60  POP_JUMP_IF_FALSE    66  'to 66'

 L.  27        62  LOAD_CONST               None
               64  RETURN_VALUE     
             66_0  COME_FROM            60  '60'

 L.  29        66  LOAD_FAST                'self'
               68  LOAD_METHOD              get_finalized_command
               70  LOAD_STR                 'egg_info'
               72  CALL_METHOD_1         1  ''
               74  STORE_FAST               'ei_cmd'

 L.  30        76  LOAD_GLOBAL              Distribution

 L.  31        78  LOAD_FAST                'ei_cmd'
               80  LOAD_ATTR                egg_base
               82  LOAD_GLOBAL              PathMetadata
               84  LOAD_FAST                'ei_cmd'
               86  LOAD_ATTR                egg_base
               88  LOAD_FAST                'ei_cmd'
               90  LOAD_ATTR                egg_info
               92  CALL_FUNCTION_2       2  ''

 L.  32        94  LOAD_FAST                'ei_cmd'
               96  LOAD_ATTR                egg_name
               98  LOAD_FAST                'ei_cmd'
              100  LOAD_ATTR                egg_version

 L.  30       102  CALL_FUNCTION_4       4  ''
              104  STORE_FAST               'dist'

 L.  34       106  LOAD_FAST                'self'
              108  LOAD_METHOD              get_finalized_command
              110  LOAD_STR                 'build_scripts'
              112  CALL_METHOD_1         1  ''
              114  STORE_FAST               'bs_cmd'

 L.  35       116  LOAD_GLOBAL              getattr
              118  LOAD_FAST                'bs_cmd'
              120  LOAD_STR                 'executable'
              122  LOAD_CONST               None
              124  CALL_FUNCTION_3       3  ''
              126  STORE_FAST               'exec_param'

 L.  36       128  SETUP_FINALLY       156  'to 156'

 L.  37       130  LOAD_FAST                'self'
              132  LOAD_METHOD              get_finalized_command
              134  LOAD_STR                 'bdist_wininst'
              136  CALL_METHOD_1         1  ''
              138  STORE_FAST               'bw_cmd'

 L.  38       140  LOAD_GLOBAL              getattr
              142  LOAD_FAST                'bw_cmd'
              144  LOAD_STR                 '_is_running'
              146  LOAD_CONST               False
              148  CALL_FUNCTION_3       3  ''
              150  STORE_FAST               'is_wininst'
              152  POP_BLOCK        
              154  JUMP_FORWARD        182  'to 182'
            156_0  COME_FROM_FINALLY   128  '128'

 L.  39       156  DUP_TOP          
              158  LOAD_GLOBAL              ImportError
              160  LOAD_GLOBAL              DistutilsModuleError
              162  BUILD_TUPLE_2         2 
              164  <121>               180  ''
              166  POP_TOP          
              168  POP_TOP          
              170  POP_TOP          

 L.  40       172  LOAD_CONST               False
              174  STORE_FAST               'is_wininst'
              176  POP_EXCEPT       
              178  JUMP_FORWARD        182  'to 182'
              180  <48>             
            182_0  COME_FROM           178  '178'
            182_1  COME_FROM           154  '154'

 L.  41       182  LOAD_FAST                'ei'
              184  LOAD_ATTR                ScriptWriter
              186  STORE_FAST               'writer'

 L.  42       188  LOAD_FAST                'is_wininst'
              190  POP_JUMP_IF_FALSE   202  'to 202'

 L.  43       192  LOAD_STR                 'python.exe'
              194  STORE_FAST               'exec_param'

 L.  44       196  LOAD_FAST                'ei'
              198  LOAD_ATTR                WindowsScriptWriter
              200  STORE_FAST               'writer'
            202_0  COME_FROM           190  '190'

 L.  45       202  LOAD_FAST                'exec_param'
              204  LOAD_GLOBAL              sys
              206  LOAD_ATTR                executable
              208  COMPARE_OP               ==
              210  POP_JUMP_IF_FALSE   218  'to 218'

 L.  48       212  LOAD_FAST                'exec_param'
              214  BUILD_LIST_1          1 
              216  STORE_FAST               'exec_param'
            218_0  COME_FROM           210  '210'

 L.  50       218  LOAD_FAST                'writer'
              220  LOAD_METHOD              best
              222  CALL_METHOD_0         0  ''
              224  STORE_FAST               'writer'

 L.  51       226  LOAD_FAST                'writer'
              228  LOAD_ATTR                command_spec_class
              230  LOAD_METHOD              best
              232  CALL_METHOD_0         0  ''
              234  LOAD_METHOD              from_param
              236  LOAD_FAST                'exec_param'
              238  CALL_METHOD_1         1  ''
              240  STORE_FAST               'cmd'

 L.  52       242  LOAD_FAST                'writer'
              244  LOAD_METHOD              get_args
              246  LOAD_FAST                'dist'
              248  LOAD_FAST                'cmd'
              250  LOAD_METHOD              as_header
              252  CALL_METHOD_0         0  ''
              254  CALL_METHOD_2         2  ''
              256  GET_ITER         
            258_0  COME_FROM           272  '272'
              258  FOR_ITER            276  'to 276'
              260  STORE_FAST               'args'

 L.  53       262  LOAD_FAST                'self'
              264  LOAD_ATTR                write_script
              266  LOAD_FAST                'args'
              268  CALL_FUNCTION_EX      0  'positional arguments only'
              270  POP_TOP          
          272_274  JUMP_BACK           258  'to 258'
            276_0  COME_FROM           258  '258'

Parse error at or near `<121>' instruction at offset 164

    def write_script(self, script_name, contents, mode='t', *ignored):
        """Write an executable file to the scripts directory"""
        from setuptools.command.easy_install import chmod, current_umask
        log.info('Installing %s script to %s', script_name, self.install_dir)
        target = os.path.joinself.install_dirscript_name
        self.outfiles.append(target)
        mask = current_umask()
        if not self.dry_run:
            ensure_directory(target)
            f = opentarget('w' + mode)
            f.write(contents)
            f.close
            chmodtarget(511 - mask)