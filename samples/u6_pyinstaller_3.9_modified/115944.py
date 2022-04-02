# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: setuptools\command\install_scripts.py
from distutils import log
import distutils.command.install_scripts as orig
import os, sys
from pkg_resources import Distribution, PathMetadata, ensure_directory

class install_scripts(orig.install_scripts):
    __doc__ = 'Do normal script install, plus any egg_info wrapper scripts'

    def initialize_options(self):
        orig.install_scripts.initialize_options(self)
        self.no_ep = False

    def run--- This code section failed: ---

 L.  17         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME_ATTR         setuptools.command.easy_install
                6  IMPORT_FROM              command
                8  ROT_TWO          
               10  POP_TOP          
               12  IMPORT_FROM              easy_install
               14  STORE_FAST               'ei'
               16  POP_TOP          

 L.  19        18  LOAD_FAST                'self'
               20  LOAD_METHOD              run_command
               22  LOAD_STR                 'egg_info'
               24  CALL_METHOD_1         1  ''
               26  POP_TOP          

 L.  20        28  LOAD_FAST                'self'
               30  LOAD_ATTR                distribution
               32  LOAD_ATTR                scripts
               34  POP_JUMP_IF_FALSE    50  'to 50'

 L.  21        36  LOAD_GLOBAL              orig
               38  LOAD_ATTR                install_scripts
               40  LOAD_METHOD              run
               42  LOAD_FAST                'self'
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          
               48  JUMP_FORWARD         56  'to 56'
             50_0  COME_FROM            34  '34'

 L.  23        50  BUILD_LIST_0          0 
               52  LOAD_FAST                'self'
               54  STORE_ATTR               outfiles
             56_0  COME_FROM            48  '48'

 L.  24        56  LOAD_FAST                'self'
               58  LOAD_ATTR                no_ep
               60  POP_JUMP_IF_FALSE    66  'to 66'

 L.  26        62  LOAD_CONST               None
               64  RETURN_VALUE     
             66_0  COME_FROM            60  '60'

 L.  28        66  LOAD_FAST                'self'
               68  LOAD_METHOD              get_finalized_command
               70  LOAD_STR                 'egg_info'
               72  CALL_METHOD_1         1  ''
               74  STORE_FAST               'ei_cmd'

 L.  29        76  LOAD_GLOBAL              Distribution

 L.  30        78  LOAD_FAST                'ei_cmd'
               80  LOAD_ATTR                egg_base
               82  LOAD_GLOBAL              PathMetadata
               84  LOAD_FAST                'ei_cmd'
               86  LOAD_ATTR                egg_base
               88  LOAD_FAST                'ei_cmd'
               90  LOAD_ATTR                egg_info
               92  CALL_FUNCTION_2       2  ''

 L.  31        94  LOAD_FAST                'ei_cmd'
               96  LOAD_ATTR                egg_name
               98  LOAD_FAST                'ei_cmd'
              100  LOAD_ATTR                egg_version

 L.  29       102  CALL_FUNCTION_4       4  ''
              104  STORE_FAST               'dist'

 L.  33       106  LOAD_FAST                'self'
              108  LOAD_METHOD              get_finalized_command
              110  LOAD_STR                 'build_scripts'
              112  CALL_METHOD_1         1  ''
              114  STORE_FAST               'bs_cmd'

 L.  34       116  LOAD_GLOBAL              getattr
              118  LOAD_FAST                'bs_cmd'
              120  LOAD_STR                 'executable'
              122  LOAD_CONST               None
              124  CALL_FUNCTION_3       3  ''
              126  STORE_FAST               'exec_param'

 L.  35       128  SETUP_FINALLY       156  'to 156'

 L.  36       130  LOAD_FAST                'self'
              132  LOAD_METHOD              get_finalized_command
              134  LOAD_STR                 'bdist_wininst'
              136  CALL_METHOD_1         1  ''
              138  STORE_FAST               'bw_cmd'

 L.  37       140  LOAD_GLOBAL              getattr
              142  LOAD_FAST                'bw_cmd'
              144  LOAD_STR                 '_is_running'
              146  LOAD_CONST               False
              148  CALL_FUNCTION_3       3  ''
              150  STORE_FAST               'is_wininst'
              152  POP_BLOCK        
              154  JUMP_FORWARD        178  'to 178'
            156_0  COME_FROM_FINALLY   128  '128'

 L.  38       156  DUP_TOP          
              158  LOAD_GLOBAL              ImportError
              160  <121>               176  ''
              162  POP_TOP          
              164  POP_TOP          
              166  POP_TOP          

 L.  39       168  LOAD_CONST               False
              170  STORE_FAST               'is_wininst'
              172  POP_EXCEPT       
              174  JUMP_FORWARD        178  'to 178'
              176  <48>             
            178_0  COME_FROM           174  '174'
            178_1  COME_FROM           154  '154'

 L.  40       178  LOAD_FAST                'ei'
              180  LOAD_ATTR                ScriptWriter
              182  STORE_FAST               'writer'

 L.  41       184  LOAD_FAST                'is_wininst'
              186  POP_JUMP_IF_FALSE   198  'to 198'

 L.  42       188  LOAD_STR                 'python.exe'
              190  STORE_FAST               'exec_param'

 L.  43       192  LOAD_FAST                'ei'
              194  LOAD_ATTR                WindowsScriptWriter
              196  STORE_FAST               'writer'
            198_0  COME_FROM           186  '186'

 L.  44       198  LOAD_FAST                'exec_param'
              200  LOAD_GLOBAL              sys
              202  LOAD_ATTR                executable
              204  COMPARE_OP               ==
              206  POP_JUMP_IF_FALSE   214  'to 214'

 L.  47       208  LOAD_FAST                'exec_param'
              210  BUILD_LIST_1          1 
              212  STORE_FAST               'exec_param'
            214_0  COME_FROM           206  '206'

 L.  49       214  LOAD_FAST                'writer'
              216  LOAD_METHOD              best
              218  CALL_METHOD_0         0  ''
              220  STORE_FAST               'writer'

 L.  50       222  LOAD_FAST                'writer'
              224  LOAD_ATTR                command_spec_class
              226  LOAD_METHOD              best
              228  CALL_METHOD_0         0  ''
              230  LOAD_METHOD              from_param
              232  LOAD_FAST                'exec_param'
              234  CALL_METHOD_1         1  ''
              236  STORE_FAST               'cmd'

 L.  51       238  LOAD_FAST                'writer'
              240  LOAD_METHOD              get_args
              242  LOAD_FAST                'dist'
              244  LOAD_FAST                'cmd'
              246  LOAD_METHOD              as_header
              248  CALL_METHOD_0         0  ''
              250  CALL_METHOD_2         2  ''
              252  GET_ITER         
              254  FOR_ITER            270  'to 270'
              256  STORE_FAST               'args'

 L.  52       258  LOAD_FAST                'self'
              260  LOAD_ATTR                write_script
              262  LOAD_FAST                'args'
              264  CALL_FUNCTION_EX      0  'positional arguments only'
              266  POP_TOP          
              268  JUMP_BACK           254  'to 254'

Parse error at or near `<121>' instruction at offset 160

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