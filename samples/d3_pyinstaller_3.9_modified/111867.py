# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: distutils\cmd.py
"""distutils.cmd

Provides the Command class, the base class for the command classes
in the distutils.command package.
"""
import sys, os, re
from distutils.errors import DistutilsOptionError
from distutils import util, dir_util, file_util, archive_util, dep_util
from distutils import log

class Command:
    __doc__ = 'Abstract base class for defining command classes, the "worker bees"\n    of the Distutils.  A useful analogy for command classes is to think of\n    them as subroutines with local variables called "options".  The options\n    are "declared" in \'initialize_options()\' and "defined" (given their\n    final values, aka "finalized") in \'finalize_options()\', both of which\n    must be defined by every command class.  The distinction between the\n    two is necessary because option values might come from the outside\n    world (command line, config file, ...), and any options dependent on\n    other options must be computed *after* these outside influences have\n    been processed -- hence \'finalize_options()\'.  The "body" of the\n    subroutine, where it does all its work based on the values of its\n    options, is the \'run()\' method, which must also be implemented by every\n    command class.\n    '
    sub_commands = []

    def __init__--- This code section failed: ---

 L.  54         0  LOAD_CONST               0
                2  LOAD_CONST               ('Distribution',)
                4  IMPORT_NAME_ATTR         distutils.dist
                6  IMPORT_FROM              Distribution
                8  STORE_FAST               'Distribution'
               10  POP_TOP          

 L.  56        12  LOAD_GLOBAL              isinstance
               14  LOAD_FAST                'dist'
               16  LOAD_FAST                'Distribution'
               18  CALL_FUNCTION_2       2  ''
               20  POP_JUMP_IF_TRUE     30  'to 30'

 L.  57        22  LOAD_GLOBAL              TypeError
               24  LOAD_STR                 'dist must be a Distribution instance'
               26  CALL_FUNCTION_1       1  ''
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            20  '20'

 L.  58        30  LOAD_FAST                'self'
               32  LOAD_ATTR                __class__
               34  LOAD_GLOBAL              Command
               36  <117>                 0  ''
               38  POP_JUMP_IF_FALSE    48  'to 48'

 L.  59        40  LOAD_GLOBAL              RuntimeError
               42  LOAD_STR                 'Command is an abstract class'
               44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            38  '38'

 L.  61        48  LOAD_FAST                'dist'
               50  LOAD_FAST                'self'
               52  STORE_ATTR               distribution

 L.  62        54  LOAD_FAST                'self'
               56  LOAD_METHOD              initialize_options
               58  CALL_METHOD_0         0  ''
               60  POP_TOP          

 L.  72        62  LOAD_CONST               None
               64  LOAD_FAST                'self'
               66  STORE_ATTR               _dry_run

 L.  76        68  LOAD_FAST                'dist'
               70  LOAD_ATTR                verbose
               72  LOAD_FAST                'self'
               74  STORE_ATTR               verbose

 L.  82        76  LOAD_CONST               None
               78  LOAD_FAST                'self'
               80  STORE_ATTR               force

 L.  86        82  LOAD_CONST               0
               84  LOAD_FAST                'self'
               86  STORE_ATTR               help

 L.  92        88  LOAD_CONST               0
               90  LOAD_FAST                'self'
               92  STORE_ATTR               finalized

Parse error at or near `<117>' instruction at offset 36

    def __getattr__--- This code section failed: ---

 L.  96         0  LOAD_FAST                'attr'
                2  LOAD_STR                 'dry_run'
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE    48  'to 48'

 L.  97         8  LOAD_GLOBAL              getattr
               10  LOAD_FAST                'self'
               12  LOAD_STR                 '_'
               14  LOAD_FAST                'attr'
               16  BINARY_ADD       
               18  CALL_FUNCTION_2       2  ''
               20  STORE_FAST               'myval'

 L.  98        22  LOAD_FAST                'myval'
               24  LOAD_CONST               None
               26  <117>                 0  ''
               28  POP_JUMP_IF_FALSE    42  'to 42'

 L.  99        30  LOAD_GLOBAL              getattr
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                distribution
               36  LOAD_FAST                'attr'
               38  CALL_FUNCTION_2       2  ''
               40  RETURN_VALUE     
             42_0  COME_FROM            28  '28'

 L. 101        42  LOAD_FAST                'myval'
               44  RETURN_VALUE     
               46  JUMP_FORWARD         56  'to 56'
             48_0  COME_FROM             6  '6'

 L. 103        48  LOAD_GLOBAL              AttributeError
               50  LOAD_FAST                'attr'
               52  CALL_FUNCTION_1       1  ''
               54  RAISE_VARARGS_1       1  'exception instance'
             56_0  COME_FROM            46  '46'

Parse error at or near `<117>' instruction at offset 26

    def ensure_finalized(self):
        if not self.finalized:
            self.finalize_options
        self.finalized = 1

    def initialize_options(self):
        """Set default values for all the options that this command
        supports.  Note that these defaults may be overridden by other
        commands, by the setup script, by config files, or by the
        command-line.  Thus, this is not the place to code dependencies
        between options; generally, 'initialize_options()' implementations
        are just a bunch of "self.foo = None" assignments.

        This method must be implemented by all command classes.
        """
        raise RuntimeError('abstract method -- subclass %s must override' % self.__class__)

    def finalize_options(self):
        """Set final values for all the options that this command supports.
        This is always called as late as possible, ie.  after any option
        assignments from the command-line or from other commands have been
        done.  Thus, this is the place to code option dependencies: if
        'foo' depends on 'bar', then it is safe to set 'foo' from 'bar' as
        long as 'foo' still has the same value it was assigned in
        'initialize_options()'.

        This method must be implemented by all command classes.
        """
        raise RuntimeError('abstract method -- subclass %s must override' % self.__class__)

    def dump_options--- This code section failed: ---

 L. 152         0  LOAD_CONST               0
                2  LOAD_CONST               ('longopt_xlate',)
                4  IMPORT_NAME_ATTR         distutils.fancy_getopt
                6  IMPORT_FROM              longopt_xlate
                8  STORE_FAST               'longopt_xlate'
               10  POP_TOP          

 L. 153        12  LOAD_FAST                'header'
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    32  'to 32'

 L. 154        20  LOAD_STR                 "command options for '%s':"
               22  LOAD_FAST                'self'
               24  LOAD_METHOD              get_command_name
               26  CALL_METHOD_0         0  ''
               28  BINARY_MODULO    
               30  STORE_FAST               'header'
             32_0  COME_FROM            18  '18'

 L. 155        32  LOAD_FAST                'self'
               34  LOAD_ATTR                announce
               36  LOAD_FAST                'indent'
               38  LOAD_FAST                'header'
               40  BINARY_ADD       
               42  LOAD_GLOBAL              log
               44  LOAD_ATTR                INFO
               46  LOAD_CONST               ('level',)
               48  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               50  POP_TOP          

 L. 156        52  LOAD_FAST                'indent'
               54  LOAD_STR                 '  '
               56  BINARY_ADD       
               58  STORE_FAST               'indent'

 L. 157        60  LOAD_FAST                'self'
               62  LOAD_ATTR                user_options
               64  GET_ITER         
             66_0  COME_FROM           148  '148'
               66  FOR_ITER            150  'to 150'
               68  UNPACK_SEQUENCE_3     3 
               70  STORE_FAST               'option'
               72  STORE_FAST               '_'
               74  STORE_FAST               '_'

 L. 158        76  LOAD_FAST                'option'
               78  LOAD_METHOD              translate
               80  LOAD_FAST                'longopt_xlate'
               82  CALL_METHOD_1         1  ''
               84  STORE_FAST               'option'

 L. 159        86  LOAD_FAST                'option'
               88  LOAD_CONST               -1
               90  BINARY_SUBSCR    
               92  LOAD_STR                 '='
               94  COMPARE_OP               ==
               96  POP_JUMP_IF_FALSE   110  'to 110'

 L. 160        98  LOAD_FAST                'option'
              100  LOAD_CONST               None
              102  LOAD_CONST               -1
              104  BUILD_SLICE_2         2 
              106  BINARY_SUBSCR    
              108  STORE_FAST               'option'
            110_0  COME_FROM            96  '96'

 L. 161       110  LOAD_GLOBAL              getattr
              112  LOAD_FAST                'self'
              114  LOAD_FAST                'option'
              116  CALL_FUNCTION_2       2  ''
              118  STORE_FAST               'value'

 L. 162       120  LOAD_FAST                'self'
              122  LOAD_ATTR                announce
              124  LOAD_FAST                'indent'
              126  LOAD_STR                 '%s = %s'
              128  LOAD_FAST                'option'
              130  LOAD_FAST                'value'
              132  BUILD_TUPLE_2         2 
              134  BINARY_MODULO    
              136  BINARY_ADD       

 L. 163       138  LOAD_GLOBAL              log
              140  LOAD_ATTR                INFO

 L. 162       142  LOAD_CONST               ('level',)
              144  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              146  POP_TOP          
              148  JUMP_BACK            66  'to 66'
            150_0  COME_FROM            66  '66'

Parse error at or near `<117>' instruction at offset 16

    def run(self):
        """A command's raison d'etre: carry out the action it exists to
        perform, controlled by the options initialized in
        'initialize_options()', customized by other commands, the setup
        script, the command-line, and config files, and finalized in
        'finalize_options()'.  All terminal output and filesystem
        interaction should be done by 'run()'.

        This method must be implemented by all command classes.
        """
        raise RuntimeError('abstract method -- subclass %s must override' % self.__class__)

    def announce(self, msg, level=1):
        """If the current verbosity level is of greater than or equal to
        'level' print 'msg' to stdout.
        """
        log.log(level, msg)

    def debug_print(self, msg):
        """Print 'msg' to stdout if the global DEBUG (taken from the
        DISTUTILS_DEBUG environment variable) flag is true.
        """
        from distutils.debug import DEBUG
        if DEBUG:
            print(msg)
            sys.stdout.flush

    def _ensure_stringlike--- This code section failed: ---

 L. 208         0  LOAD_GLOBAL              getattr
                2  LOAD_FAST                'self'
                4  LOAD_FAST                'option'
                6  CALL_FUNCTION_2       2  ''
                8  STORE_FAST               'val'

 L. 209        10  LOAD_FAST                'val'
               12  LOAD_CONST               None
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    34  'to 34'

 L. 210        18  LOAD_GLOBAL              setattr
               20  LOAD_FAST                'self'
               22  LOAD_FAST                'option'
               24  LOAD_FAST                'default'
               26  CALL_FUNCTION_3       3  ''
               28  POP_TOP          

 L. 211        30  LOAD_FAST                'default'
               32  RETURN_VALUE     
             34_0  COME_FROM            16  '16'

 L. 212        34  LOAD_GLOBAL              isinstance
               36  LOAD_FAST                'val'
               38  LOAD_GLOBAL              str
               40  CALL_FUNCTION_2       2  ''
               42  POP_JUMP_IF_TRUE     62  'to 62'

 L. 213        44  LOAD_GLOBAL              DistutilsOptionError
               46  LOAD_STR                 "'%s' must be a %s (got `%s`)"

 L. 214        48  LOAD_FAST                'option'
               50  LOAD_FAST                'what'
               52  LOAD_FAST                'val'
               54  BUILD_TUPLE_3         3 

 L. 213        56  BINARY_MODULO    
               58  CALL_FUNCTION_1       1  ''
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            42  '42'

 L. 215        62  LOAD_FAST                'val'
               64  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 14

    def ensure_string(self, option, default=None):
        """Ensure that 'option' is a string; if not defined, set it to
        'default'.
        """
        self._ensure_stringlike(option, 'string', default)

    def ensure_string_list--- This code section failed: ---

 L. 229         0  LOAD_GLOBAL              getattr
                2  LOAD_FAST                'self'
                4  LOAD_FAST                'option'
                6  CALL_FUNCTION_2       2  ''
                8  STORE_FAST               'val'

 L. 230        10  LOAD_FAST                'val'
               12  LOAD_CONST               None
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    22  'to 22'

 L. 231        18  LOAD_CONST               None
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L. 232        22  LOAD_GLOBAL              isinstance
               24  LOAD_FAST                'val'
               26  LOAD_GLOBAL              str
               28  CALL_FUNCTION_2       2  ''
               30  POP_JUMP_IF_FALSE    54  'to 54'

 L. 233        32  LOAD_GLOBAL              setattr
               34  LOAD_FAST                'self'
               36  LOAD_FAST                'option'
               38  LOAD_GLOBAL              re
               40  LOAD_METHOD              split
               42  LOAD_STR                 ',\\s*|\\s+'
               44  LOAD_FAST                'val'
               46  CALL_METHOD_2         2  ''
               48  CALL_FUNCTION_3       3  ''
               50  POP_TOP          
               52  JUMP_FORWARD        108  'to 108'
             54_0  COME_FROM            30  '30'

 L. 235        54  LOAD_GLOBAL              isinstance
               56  LOAD_FAST                'val'
               58  LOAD_GLOBAL              list
               60  CALL_FUNCTION_2       2  ''
               62  POP_JUMP_IF_FALSE    84  'to 84'

 L. 236        64  LOAD_GLOBAL              all
               66  LOAD_GENEXPR             '<code_object <genexpr>>'
               68  LOAD_STR                 'Command.ensure_string_list.<locals>.<genexpr>'
               70  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               72  LOAD_FAST                'val'
               74  GET_ITER         
               76  CALL_FUNCTION_1       1  ''
               78  CALL_FUNCTION_1       1  ''
               80  STORE_FAST               'ok'
               82  JUMP_FORWARD         88  'to 88'
             84_0  COME_FROM            62  '62'

 L. 238        84  LOAD_CONST               False
               86  STORE_FAST               'ok'
             88_0  COME_FROM            82  '82'

 L. 239        88  LOAD_FAST                'ok'
               90  POP_JUMP_IF_TRUE    108  'to 108'

 L. 240        92  LOAD_GLOBAL              DistutilsOptionError

 L. 241        94  LOAD_STR                 "'%s' must be a list of strings (got %r)"

 L. 242        96  LOAD_FAST                'option'
               98  LOAD_FAST                'val'
              100  BUILD_TUPLE_2         2 

 L. 241       102  BINARY_MODULO    

 L. 240       104  CALL_FUNCTION_1       1  ''
              106  RAISE_VARARGS_1       1  'exception instance'
            108_0  COME_FROM            90  '90'
            108_1  COME_FROM            52  '52'

Parse error at or near `<117>' instruction at offset 14

    def _ensure_tested_string--- This code section failed: ---

 L. 246         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _ensure_stringlike
                4  LOAD_FAST                'option'
                6  LOAD_FAST                'what'
                8  LOAD_FAST                'default'
               10  CALL_METHOD_3         3  ''
               12  STORE_FAST               'val'

 L. 247        14  LOAD_FAST                'val'
               16  LOAD_CONST               None
               18  <117>                 1  ''
               20  POP_JUMP_IF_FALSE    50  'to 50'
               22  LOAD_FAST                'tester'
               24  LOAD_FAST                'val'
               26  CALL_FUNCTION_1       1  ''
               28  POP_JUMP_IF_TRUE     50  'to 50'

 L. 248        30  LOAD_GLOBAL              DistutilsOptionError
               32  LOAD_STR                 "error in '%s' option: "
               34  LOAD_FAST                'error_fmt'
               36  BINARY_ADD       

 L. 249        38  LOAD_FAST                'option'
               40  LOAD_FAST                'val'
               42  BUILD_TUPLE_2         2 

 L. 248        44  BINARY_MODULO    
               46  CALL_FUNCTION_1       1  ''
               48  RAISE_VARARGS_1       1  'exception instance'
             50_0  COME_FROM            28  '28'
             50_1  COME_FROM            20  '20'

Parse error at or near `<117>' instruction at offset 18

    def ensure_filename(self, option):
        """Ensure that 'option' is the name of an existing file."""
        self._ensure_tested_string(option, os.path.isfile, 'filename', "'%s' does not exist or is not a file")

    def ensure_dirname(self, option):
        self._ensure_tested_string(option, os.path.isdir, 'directory name', "'%s' does not exist or is not a directory")

    def get_command_name(self):
        if hasattr(self, 'command_name'):
            return self.command_name
        return self.__class__.__name__

    def set_undefined_options--- This code section failed: ---

 L. 286         0  LOAD_FAST                'self'
                2  LOAD_ATTR                distribution
                4  LOAD_METHOD              get_command_obj
                6  LOAD_FAST                'src_cmd'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'src_cmd_obj'

 L. 287        12  LOAD_FAST                'src_cmd_obj'
               14  LOAD_METHOD              ensure_finalized
               16  CALL_METHOD_0         0  ''
               18  POP_TOP          

 L. 288        20  LOAD_FAST                'option_pairs'
               22  GET_ITER         
             24_0  COME_FROM            64  '64'
             24_1  COME_FROM            44  '44'
               24  FOR_ITER             66  'to 66'
               26  UNPACK_SEQUENCE_2     2 
               28  STORE_FAST               'src_option'
               30  STORE_FAST               'dst_option'

 L. 289        32  LOAD_GLOBAL              getattr
               34  LOAD_FAST                'self'
               36  LOAD_FAST                'dst_option'
               38  CALL_FUNCTION_2       2  ''
               40  LOAD_CONST               None
               42  <117>                 0  ''
               44  POP_JUMP_IF_FALSE_BACK    24  'to 24'

 L. 290        46  LOAD_GLOBAL              setattr
               48  LOAD_FAST                'self'
               50  LOAD_FAST                'dst_option'
               52  LOAD_GLOBAL              getattr
               54  LOAD_FAST                'src_cmd_obj'
               56  LOAD_FAST                'src_option'
               58  CALL_FUNCTION_2       2  ''
               60  CALL_FUNCTION_3       3  ''
               62  POP_TOP          
               64  JUMP_BACK            24  'to 24'
             66_0  COME_FROM            24  '24'

Parse error at or near `<117>' instruction at offset 42

    def get_finalized_command(self, command, create=1):
        """Wrapper around Distribution's 'get_command_obj()' method: find
        (create if necessary and 'create' is true) the command object for
        'command', call its 'ensure_finalized()' method, and return the
        finalized command object.
        """
        cmd_obj = self.distribution.get_command_obj(command, create)
        cmd_obj.ensure_finalized
        return cmd_obj

    def reinitialize_command(self, command, reinit_subcommands=0):
        return self.distribution.reinitialize_command(command, reinit_subcommands)

    def run_command(self, command):
        """Run some other command: uses the 'run_command()' method of
        Distribution, which creates and finalizes the command object if
        necessary and then invokes its 'run()' method.
        """
        self.distribution.run_commandcommand

    def get_sub_commands--- This code section failed: ---

 L. 322         0  BUILD_LIST_0          0 
                2  STORE_FAST               'commands'

 L. 323         4  LOAD_FAST                'self'
                6  LOAD_ATTR                sub_commands
                8  GET_ITER         
             10_0  COME_FROM            44  '44'
             10_1  COME_FROM            32  '32'
               10  FOR_ITER             46  'to 46'
               12  UNPACK_SEQUENCE_2     2 
               14  STORE_FAST               'cmd_name'
               16  STORE_FAST               'method'

 L. 324        18  LOAD_FAST                'method'
               20  LOAD_CONST               None
               22  <117>                 0  ''
               24  POP_JUMP_IF_TRUE     34  'to 34'
               26  LOAD_FAST                'method'
               28  LOAD_FAST                'self'
               30  CALL_FUNCTION_1       1  ''
               32  POP_JUMP_IF_FALSE_BACK    10  'to 10'
             34_0  COME_FROM            24  '24'

 L. 325        34  LOAD_FAST                'commands'
               36  LOAD_METHOD              append
               38  LOAD_FAST                'cmd_name'
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          
               44  JUMP_BACK            10  'to 10'
             46_0  COME_FROM            10  '10'

 L. 326        46  LOAD_FAST                'commands'
               48  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 22

    def warn(self, msg):
        log.warn('warning: %s: %s\n', self.get_command_name, msg)

    def execute(self, func, args, msg=None, level=1):
        util.execute(func, args, msg, dry_run=(self.dry_run))

    def mkpath(self, name, mode=511):
        dir_util.mkpath(name, mode, dry_run=(self.dry_run))

    def copy_file(self, infile, outfile, preserve_mode=1, preserve_times=1, link=None, level=1):
        """Copy a file respecting verbose, dry-run and force flags.  (The
        former two default to whatever is in the Distribution object, and
        the latter defaults to false for commands that don't define it.)"""
        return file_util.copy_file(infile, outfile, preserve_mode, preserve_times,
          (not self.force), link, dry_run=(self.dry_run))

    def copy_tree(self, infile, outfile, preserve_mode=1, preserve_times=1, preserve_symlinks=0, level=1):
        """Copy an entire directory tree respecting verbose, dry-run,
        and force flags.
        """
        return dir_util.copy_tree(infile, outfile, preserve_mode, preserve_times,
          preserve_symlinks, (not self.force),
          dry_run=(self.dry_run))

    def move_file(self, src, dst, level=1):
        """Move a file respecting dry-run flag."""
        return file_util.move_file(src, dst, dry_run=(self.dry_run))

    def spawn(self, cmd, search_path=1, level=1):
        """Spawn an external command respecting dry-run flag."""
        import distutils.spawn as spawn
        spawn(cmd, search_path, dry_run=(self.dry_run))

    def make_archive(self, base_name, format, root_dir=None, base_dir=None, owner=None, group=None):
        return archive_util.make_archive(base_name, format, root_dir, base_dir, dry_run=(self.dry_run),
          owner=owner,
          group=group)

    def make_file--- This code section failed: ---

 L. 383         0  LOAD_FAST                'skip_msg'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 384         8  LOAD_STR                 'skipping %s (inputs unchanged)'
               10  LOAD_FAST                'outfile'
               12  BINARY_MODULO    
               14  STORE_FAST               'skip_msg'
             16_0  COME_FROM             6  '6'

 L. 387        16  LOAD_GLOBAL              isinstance
               18  LOAD_FAST                'infiles'
               20  LOAD_GLOBAL              str
               22  CALL_FUNCTION_2       2  ''
               24  POP_JUMP_IF_FALSE    34  'to 34'

 L. 388        26  LOAD_FAST                'infiles'
               28  BUILD_TUPLE_1         1 
               30  STORE_FAST               'infiles'
               32  JUMP_FORWARD         56  'to 56'
             34_0  COME_FROM            24  '24'

 L. 389        34  LOAD_GLOBAL              isinstance
               36  LOAD_FAST                'infiles'
               38  LOAD_GLOBAL              list
               40  LOAD_GLOBAL              tuple
               42  BUILD_TUPLE_2         2 
               44  CALL_FUNCTION_2       2  ''
               46  POP_JUMP_IF_TRUE     56  'to 56'

 L. 390        48  LOAD_GLOBAL              TypeError

 L. 391        50  LOAD_STR                 "'infiles' must be a string, or a list or tuple of strings"

 L. 390        52  CALL_FUNCTION_1       1  ''
               54  RAISE_VARARGS_1       1  'exception instance'
             56_0  COME_FROM            46  '46'
             56_1  COME_FROM            32  '32'

 L. 393        56  LOAD_FAST                'exec_msg'
               58  LOAD_CONST               None
               60  <117>                 0  ''
               62  POP_JUMP_IF_FALSE    82  'to 82'

 L. 394        64  LOAD_STR                 'generating %s from %s'
               66  LOAD_FAST                'outfile'
               68  LOAD_STR                 ', '
               70  LOAD_METHOD              join
               72  LOAD_FAST                'infiles'
               74  CALL_METHOD_1         1  ''
               76  BUILD_TUPLE_2         2 
               78  BINARY_MODULO    
               80  STORE_FAST               'exec_msg'
             82_0  COME_FROM            62  '62'

 L. 399        82  LOAD_FAST                'self'
               84  LOAD_ATTR                force
               86  POP_JUMP_IF_TRUE    100  'to 100'
               88  LOAD_GLOBAL              dep_util
               90  LOAD_METHOD              newer_group
               92  LOAD_FAST                'infiles'
               94  LOAD_FAST                'outfile'
               96  CALL_METHOD_2         2  ''
               98  POP_JUMP_IF_FALSE   118  'to 118'
            100_0  COME_FROM            86  '86'

 L. 400       100  LOAD_FAST                'self'
              102  LOAD_METHOD              execute
              104  LOAD_FAST                'func'
              106  LOAD_FAST                'args'
              108  LOAD_FAST                'exec_msg'
              110  LOAD_FAST                'level'
              112  CALL_METHOD_4         4  ''
              114  POP_TOP          
              116  JUMP_FORWARD        128  'to 128'
            118_0  COME_FROM            98  '98'

 L. 403       118  LOAD_GLOBAL              log
              120  LOAD_METHOD              debug
              122  LOAD_FAST                'skip_msg'
              124  CALL_METHOD_1         1  ''
              126  POP_TOP          
            128_0  COME_FROM           116  '116'

Parse error at or near `None' instruction at offset -1