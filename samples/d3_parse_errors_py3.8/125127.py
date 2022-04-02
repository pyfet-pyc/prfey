# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: distutils\dist.py
"""distutils.dist

Provides the Distribution class, which represents the module distribution
being built/installed/distributed.
"""
import sys, os, re
from email import message_from_file
try:
    import warnings
except ImportError:
    warnings = None
else:
    from distutils.errors import *
    from distutils.fancy_getopt import FancyGetopt, translate_longopt
    from distutils.util import check_environ, strtobool, rfc822_escape
    from distutils import log
    from distutils.debug import DEBUG
    command_re = re.compile('^[a-zA-Z]([a-zA-Z0-9_]*)$')

    def _ensure_list(value, fieldname):
        if isinstance(value, str):
            pass
        else:
            if not isinstance(value, list):
                typename = type(value).__name__
                msg = f"Warning: '{fieldname}' should be a list, got type '{typename}'"
                log.log(log.WARN, msg)
                value = list(value)
            return value


    class Distribution:
        __doc__ = "The core of the Distutils.  Most of the work hiding behind 'setup'\n    is really done within a Distribution instance, which farms the work out\n    to the Distutils commands specified on the command line.\n\n    Setup scripts will almost never instantiate Distribution directly,\n    unless the 'setup()' function is totally inadequate to their needs.\n    However, it is conceivable that a setup script might wish to subclass\n    Distribution for some specialized purpose, and then pass the subclass\n    to 'setup()' as the 'distclass' keyword argument.  If so, it is\n    necessary to respect the expectations that 'setup' has of Distribution.\n    See the code for 'setup()', in core.py, for details.\n    "
        global_options = [
         ('verbose', 'v', 'run verbosely (default)', 1),
         ('quiet', 'q', 'run quietly (turns verbosity off)'),
         ('dry-run', 'n', "don't actually do anything"),
         ('help', 'h', 'show detailed help message'),
         ('no-user-cfg', None, 'ignore pydistutils.cfg in your home directory')]
        common_usage = "Common commands: (see '--help-commands' for more)\n\n  setup.py build      will build the package underneath 'build/'\n  setup.py install    will install the package\n"
        display_options = [
         ('help-commands', None, 'list all available commands'),
         ('name', None, 'print package name'),
         ('version', 'V', 'print package version'),
         ('fullname', None, 'print <package name>-<version>'),
         ('author', None, "print the author's name"),
         ('author-email', None, "print the author's email address"),
         ('maintainer', None, "print the maintainer's name"),
         ('maintainer-email', None, "print the maintainer's email address"),
         ('contact', None, "print the maintainer's name if known, else the author's"),
         ('contact-email', None, "print the maintainer's email address if known, else the author's"),
         ('url', None, 'print the URL for this package'),
         ('license', None, 'print the license of the package'),
         ('licence', None, 'alias for --license'),
         ('description', None, 'print the package description'),
         ('long-description', None, 'print the long package description'),
         ('platforms', None, 'print the list of platforms'),
         ('classifiers', None, 'print the list of classifiers'),
         ('keywords', None, 'print the list of keywords'),
         ('provides', None, 'print the list of packages/modules provided'),
         ('requires', None, 'print the list of packages/modules required'),
         ('obsoletes', None, 'print the list of packages/modules made obsolete')]
        display_option_names = [translate_longopt(x[0]) for x in display_options]
        negative_opt = {'quiet': 'verbose'}

        def __init__--- This code section failed: ---

 L. 148         0  LOAD_CONST               1
                2  LOAD_FAST                'self'
                4  STORE_ATTR               verbose

 L. 149         6  LOAD_CONST               0
                8  LOAD_FAST                'self'
               10  STORE_ATTR               dry_run

 L. 150        12  LOAD_CONST               0
               14  LOAD_FAST                'self'
               16  STORE_ATTR               help

 L. 151        18  LOAD_FAST                'self'
               20  LOAD_ATTR                display_option_names
               22  GET_ITER         
             24_0  COME_FROM            40  '40'
               24  FOR_ITER             42  'to 42'
               26  STORE_FAST               'attr'

 L. 152        28  LOAD_GLOBAL              setattr
               30  LOAD_FAST                'self'
               32  LOAD_FAST                'attr'
               34  LOAD_CONST               0
               36  CALL_FUNCTION_3       3  ''
               38  POP_TOP          
               40  JUMP_BACK            24  'to 24'
             42_0  COME_FROM            24  '24'

 L. 159        42  LOAD_GLOBAL              DistributionMetadata
               44  CALL_FUNCTION_0       0  ''
               46  LOAD_FAST                'self'
               48  STORE_ATTR               metadata

 L. 160        50  LOAD_FAST                'self'
               52  LOAD_ATTR                metadata
               54  LOAD_ATTR                _METHOD_BASENAMES
               56  GET_ITER         
             58_0  COME_FROM            90  '90'
               58  FOR_ITER             92  'to 92'
               60  STORE_FAST               'basename'

 L. 161        62  LOAD_STR                 'get_'
               64  LOAD_FAST                'basename'
               66  BINARY_ADD       
               68  STORE_FAST               'method_name'

 L. 162        70  LOAD_GLOBAL              setattr
               72  LOAD_FAST                'self'
               74  LOAD_FAST                'method_name'
               76  LOAD_GLOBAL              getattr
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                metadata
               82  LOAD_FAST                'method_name'
               84  CALL_FUNCTION_2       2  ''
               86  CALL_FUNCTION_3       3  ''
               88  POP_TOP          
               90  JUMP_BACK            58  'to 58'
             92_0  COME_FROM            58  '58'

 L. 168        92  BUILD_MAP_0           0 
               94  LOAD_FAST                'self'
               96  STORE_ATTR               cmdclass

 L. 176        98  LOAD_CONST               None
              100  LOAD_FAST                'self'
              102  STORE_ATTR               command_packages

 L. 181       104  LOAD_CONST               None
              106  LOAD_FAST                'self'
              108  STORE_ATTR               script_name

 L. 182       110  LOAD_CONST               None
              112  LOAD_FAST                'self'
              114  STORE_ATTR               script_args

 L. 189       116  BUILD_MAP_0           0 
              118  LOAD_FAST                'self'
              120  STORE_ATTR               command_options

 L. 200       122  BUILD_LIST_0          0 
              124  LOAD_FAST                'self'
              126  STORE_ATTR               dist_files

 L. 205       128  LOAD_CONST               None
              130  LOAD_FAST                'self'
              132  STORE_ATTR               packages

 L. 206       134  BUILD_MAP_0           0 
              136  LOAD_FAST                'self'
              138  STORE_ATTR               package_data

 L. 207       140  LOAD_CONST               None
              142  LOAD_FAST                'self'
              144  STORE_ATTR               package_dir

 L. 208       146  LOAD_CONST               None
              148  LOAD_FAST                'self'
              150  STORE_ATTR               py_modules

 L. 209       152  LOAD_CONST               None
              154  LOAD_FAST                'self'
              156  STORE_ATTR               libraries

 L. 210       158  LOAD_CONST               None
              160  LOAD_FAST                'self'
              162  STORE_ATTR               headers

 L. 211       164  LOAD_CONST               None
              166  LOAD_FAST                'self'
              168  STORE_ATTR               ext_modules

 L. 212       170  LOAD_CONST               None
              172  LOAD_FAST                'self'
              174  STORE_ATTR               ext_package

 L. 213       176  LOAD_CONST               None
              178  LOAD_FAST                'self'
              180  STORE_ATTR               include_dirs

 L. 214       182  LOAD_CONST               None
              184  LOAD_FAST                'self'
              186  STORE_ATTR               extra_path

 L. 215       188  LOAD_CONST               None
              190  LOAD_FAST                'self'
              192  STORE_ATTR               scripts

 L. 216       194  LOAD_CONST               None
              196  LOAD_FAST                'self'
              198  STORE_ATTR               data_files

 L. 217       200  LOAD_STR                 ''
              202  LOAD_FAST                'self'
              204  STORE_ATTR               password

 L. 223       206  BUILD_MAP_0           0 
              208  LOAD_FAST                'self'
              210  STORE_ATTR               command_obj

 L. 235       212  BUILD_MAP_0           0 
              214  LOAD_FAST                'self'
              216  STORE_ATTR               have_run

 L. 241       218  LOAD_FAST                'attrs'
          220_222  POP_JUMP_IF_FALSE   520  'to 520'

 L. 246       224  LOAD_FAST                'attrs'
              226  LOAD_METHOD              get
              228  LOAD_STR                 'options'
              230  CALL_METHOD_1         1  ''
              232  STORE_FAST               'options'

 L. 247       234  LOAD_FAST                'options'
              236  LOAD_CONST               None
              238  COMPARE_OP               is-not
          240_242  POP_JUMP_IF_FALSE   312  'to 312'

 L. 248       244  LOAD_FAST                'attrs'
              246  LOAD_STR                 'options'
              248  DELETE_SUBSCR    

 L. 249       250  LOAD_FAST                'options'
              252  LOAD_METHOD              items
              254  CALL_METHOD_0         0  ''
              256  GET_ITER         
            258_0  COME_FROM           308  '308'
              258  FOR_ITER            312  'to 312'
              260  UNPACK_SEQUENCE_2     2 
              262  STORE_FAST               'command'
              264  STORE_FAST               'cmd_options'

 L. 250       266  LOAD_FAST                'self'
              268  LOAD_METHOD              get_option_dict
              270  LOAD_FAST                'command'
              272  CALL_METHOD_1         1  ''
              274  STORE_FAST               'opt_dict'

 L. 251       276  LOAD_FAST                'cmd_options'
              278  LOAD_METHOD              items
              280  CALL_METHOD_0         0  ''
              282  GET_ITER         
            284_0  COME_FROM           304  '304'
              284  FOR_ITER            308  'to 308'
              286  UNPACK_SEQUENCE_2     2 
              288  STORE_FAST               'opt'
              290  STORE_FAST               'val'

 L. 252       292  LOAD_STR                 'setup script'
              294  LOAD_FAST                'val'
              296  BUILD_TUPLE_2         2 
              298  LOAD_FAST                'opt_dict'
              300  LOAD_FAST                'opt'
              302  STORE_SUBSCR     
          304_306  JUMP_BACK           284  'to 284'
            308_0  COME_FROM           284  '284'
          308_310  JUMP_BACK           258  'to 258'
            312_0  COME_FROM           258  '258'
            312_1  COME_FROM           240  '240'

 L. 254       312  LOAD_STR                 'licence'
              314  LOAD_FAST                'attrs'
              316  COMPARE_OP               in
          318_320  POP_JUMP_IF_FALSE   382  'to 382'

 L. 255       322  LOAD_FAST                'attrs'
              324  LOAD_STR                 'licence'
              326  BINARY_SUBSCR    
              328  LOAD_FAST                'attrs'
              330  LOAD_STR                 'license'
              332  STORE_SUBSCR     

 L. 256       334  LOAD_FAST                'attrs'
              336  LOAD_STR                 'licence'
              338  DELETE_SUBSCR    

 L. 257       340  LOAD_STR                 "'licence' distribution option is deprecated; use 'license'"
              342  STORE_FAST               'msg'

 L. 258       344  LOAD_GLOBAL              warnings
              346  LOAD_CONST               None
              348  COMPARE_OP               is-not
          350_352  POP_JUMP_IF_FALSE   366  'to 366'

 L. 259       354  LOAD_GLOBAL              warnings
              356  LOAD_METHOD              warn
              358  LOAD_FAST                'msg'
              360  CALL_METHOD_1         1  ''
              362  POP_TOP          
              364  JUMP_FORWARD        382  'to 382'
            366_0  COME_FROM           350  '350'

 L. 261       366  LOAD_GLOBAL              sys
              368  LOAD_ATTR                stderr
              370  LOAD_METHOD              write
              372  LOAD_FAST                'msg'
              374  LOAD_STR                 '\n'
              376  BINARY_ADD       
              378  CALL_METHOD_1         1  ''
              380  POP_TOP          
            382_0  COME_FROM           364  '364'
            382_1  COME_FROM           318  '318'

 L. 265       382  LOAD_FAST                'attrs'
              384  LOAD_METHOD              items
              386  CALL_METHOD_0         0  ''
              388  GET_ITER         
            390_0  COME_FROM           516  '516'
            390_1  COME_FROM           492  '492'
            390_2  COME_FROM           466  '466'
            390_3  COME_FROM           436  '436'
              390  FOR_ITER            520  'to 520'
              392  UNPACK_SEQUENCE_2     2 
              394  STORE_FAST               'key'
              396  STORE_FAST               'val'

 L. 266       398  LOAD_GLOBAL              hasattr
              400  LOAD_FAST                'self'
              402  LOAD_ATTR                metadata
              404  LOAD_STR                 'set_'
              406  LOAD_FAST                'key'
              408  BINARY_ADD       
              410  CALL_FUNCTION_2       2  ''
          412_414  POP_JUMP_IF_FALSE   438  'to 438'

 L. 267       416  LOAD_GLOBAL              getattr
              418  LOAD_FAST                'self'
              420  LOAD_ATTR                metadata
              422  LOAD_STR                 'set_'
              424  LOAD_FAST                'key'
              426  BINARY_ADD       
              428  CALL_FUNCTION_2       2  ''
              430  LOAD_FAST                'val'
              432  CALL_FUNCTION_1       1  ''
              434  POP_TOP          
              436  JUMP_BACK           390  'to 390'
            438_0  COME_FROM           412  '412'

 L. 268       438  LOAD_GLOBAL              hasattr
              440  LOAD_FAST                'self'
              442  LOAD_ATTR                metadata
              444  LOAD_FAST                'key'
              446  CALL_FUNCTION_2       2  ''
          448_450  POP_JUMP_IF_FALSE   468  'to 468'

 L. 269       452  LOAD_GLOBAL              setattr
              454  LOAD_FAST                'self'
              456  LOAD_ATTR                metadata
              458  LOAD_FAST                'key'
              460  LOAD_FAST                'val'
              462  CALL_FUNCTION_3       3  ''
              464  POP_TOP          
              466  JUMP_BACK           390  'to 390'
            468_0  COME_FROM           448  '448'

 L. 270       468  LOAD_GLOBAL              hasattr
              470  LOAD_FAST                'self'
              472  LOAD_FAST                'key'
              474  CALL_FUNCTION_2       2  ''
          476_478  POP_JUMP_IF_FALSE   494  'to 494'

 L. 271       480  LOAD_GLOBAL              setattr
              482  LOAD_FAST                'self'
              484  LOAD_FAST                'key'
              486  LOAD_FAST                'val'
              488  CALL_FUNCTION_3       3  ''
              490  POP_TOP          
              492  JUMP_BACK           390  'to 390'
            494_0  COME_FROM           476  '476'

 L. 273       494  LOAD_STR                 'Unknown distribution option: %s'
              496  LOAD_GLOBAL              repr
              498  LOAD_FAST                'key'
              500  CALL_FUNCTION_1       1  ''
              502  BINARY_MODULO    
              504  STORE_FAST               'msg'

 L. 274       506  LOAD_GLOBAL              warnings
              508  LOAD_METHOD              warn
              510  LOAD_FAST                'msg'
              512  CALL_METHOD_1         1  ''
              514  POP_TOP          
          516_518  JUMP_BACK           390  'to 390'
            520_0  COME_FROM           390  '390'
            520_1  COME_FROM           220  '220'

 L. 282       520  LOAD_CONST               True
              522  LOAD_FAST                'self'
              524  STORE_ATTR               want_user_cfg

 L. 284       526  LOAD_FAST                'self'
              528  LOAD_ATTR                script_args
              530  LOAD_CONST               None
              532  COMPARE_OP               is-not
          534_536  POP_JUMP_IF_FALSE   592  'to 592'

 L. 285       538  LOAD_FAST                'self'
              540  LOAD_ATTR                script_args
              542  GET_ITER         
            544_0  COME_FROM           588  '588'
            544_1  COME_FROM           572  '572'
              544  FOR_ITER            592  'to 592'
              546  STORE_FAST               'arg'

 L. 286       548  LOAD_FAST                'arg'
              550  LOAD_METHOD              startswith
              552  LOAD_STR                 '-'
              554  CALL_METHOD_1         1  ''
          556_558  POP_JUMP_IF_TRUE    566  'to 566'

 L. 287       560  POP_TOP          
          562_564  BREAK_LOOP          592  'to 592'
            566_0  COME_FROM           556  '556'

 L. 288       566  LOAD_FAST                'arg'
              568  LOAD_STR                 '--no-user-cfg'
              570  COMPARE_OP               ==
          572_574  POP_JUMP_IF_FALSE_BACK   544  'to 544'

 L. 289       576  LOAD_CONST               False
              578  LOAD_FAST                'self'
              580  STORE_ATTR               want_user_cfg

 L. 290       582  POP_TOP          
          584_586  BREAK_LOOP          592  'to 592'
          588_590  JUMP_BACK           544  'to 544'
            592_0  COME_FROM           584  '584'
            592_1  COME_FROM           562  '562'
            592_2  COME_FROM           544  '544'
            592_3  COME_FROM           534  '534'

 L. 292       592  LOAD_FAST                'self'
              594  LOAD_METHOD              finalize_options
              596  CALL_METHOD_0         0  ''
              598  POP_TOP          

Parse error at or near `CALL_METHOD_0' instruction at offset 596

        def get_option_dict(self, command):
            """Get the option dictionary for a given command.  If that
        command's option dictionary hasn't been created yet, then create it
        and return the new dictionary; otherwise, return the existing
        option dictionary.
        """
            dict = self.command_options.get(command)
            if dict is None:
                dict = self.command_options[command] = {}
            return dict

        def dump_option_dicts(self, header=None, commands=None, indent=''):
            from pprint import pformat
            if commands is None:
                commands = sorted(self.command_options.keys)
            if header is not None:
                self.announce(indent + header)
                indent = indent + '  '
            if not commands:
                self.announce(indent + 'no commands known yet')
                return
            for cmd_name in commands:
                opt_dict = self.command_options.get(cmd_name)
                if opt_dict is None:
                    self.announce(indent + "no option dict for '%s' command" % cmd_name)
                else:
                    self.announce(indent + "option dict for '%s' command:" % cmd_name)
                    out = pformat(opt_dict)
                    for line in out.split('\n'):
                        self.announce(indent + '  ' + line)

        def find_config_files(self):
            """Find as many configuration files as should be processed for this
        platform, and return a list of filenames in the order in which they
        should be parsed.  The filenames returned are guaranteed to exist
        (modulo nasty race conditions).

        There are three possible config files: distutils.cfg in the
        Distutils installation directory (ie. where the top-level
        Distutils __inst__.py file lives), a file in the user's home
        directory named .pydistutils.cfg on Unix and pydistutils.cfg
        on Windows/Mac; and setup.cfg in the current directory.

        The file in the user's home directory can be disabled with the
        --no-user-cfg option.
        """
            files = []
            check_environ
            sys_dir = os.path.dirname(sys.modules['distutils'].__file__)
            sys_file = os.path.join(sys_dir, 'distutils.cfg')
            if os.path.isfile(sys_file):
                files.append(sys_file)
            if os.name == 'posix':
                user_filename = '.pydistutils.cfg'
            else:
                user_filename = 'pydistutils.cfg'
            if self.want_user_cfg:
                user_file = os.path.join(os.path.expanduser('~'), user_filename)
                if os.path.isfile(user_file):
                    files.append(user_file)
            local_file = 'setup.cfg'
            if os.path.isfile(local_file):
                files.append(local_file)
            if DEBUG:
                self.announce('using config files: %s' % ', '.join(files))
            return files

        def parse_config_files(self, filenames=None):
            from configparser import ConfigParser
            if sys.prefix != sys.base_prefix:
                ignore_options = ['install-base', 'install-platbase', 'install-lib',
                 'install-platlib', 'install-purelib', 'install-headers',
                 'install-scripts', 'install-data', 'prefix', 'exec-prefix',
                 'home', 'user', 'root']
            else:
                ignore_options = []
            ignore_options = frozenset(ignore_options)
            if filenames is None:
                filenames = self.find_config_files
            if DEBUG:
                self.announce('Distribution.parse_config_files():')
            parser = ConfigParser
            for filename in filenames:
                if DEBUG:
                    self.announce('  reading %s' % filename)
                else:
                    parser.read(filename)
                    for section in parser.sections:
                        options = parser.options(section)
                        opt_dict = self.get_option_dict(section)
                        for opt in options:
                            if opt != '__name__':
                                if opt not in ignore_options:
                                    val = parser.get(section, opt)
                                    opt = opt.replace('-', '_')
                                    opt_dict[opt] = (filename, val)

                    else:
                        parser.__init__

            else:
                if 'global' in self.command_options:
                    for opt, (src, val) in self.command_options['global'].items:
                        alias = self.negative_opt.get(opt)
                        try:
                            if alias:
                                setattrselfalias(not strtobool(val))
                            elif opt in ('verbose', 'dry_run'):
                                setattrselfoptstrtobool(val)
                            else:
                                setattrselfoptval
                        except ValueError as msg:
                            try:
                                raise DistutilsOptionError(msg)
                            finally:
                                msg = None
                                del msg

        def parse_command_line(self):
            """Parse the setup script's command line, taken from the
        'script_args' instance attribute (which defaults to 'sys.argv[1:]'
        -- see 'setup()' in core.py).  This list is first processed for
        "global options" -- options that set attributes of the Distribution
        instance.  Then, it is alternately scanned for Distutils commands
        and options for that command.  Each new command terminates the
        options for the previous command.  The allowed options for a
        command are determined by the 'user_options' attribute of the
        command class -- thus, we have to be able to load command classes
        in order to parse the command line.  Any error in that 'options'
        attribute raises DistutilsGetoptError; any error on the
        command-line raises DistutilsArgError.  If no Distutils commands
        were found on the command line, raises DistutilsArgError.  Return
        true if command-line was successfully parsed and we should carry
        on with executing commands; false if no errors but we shouldn't
        execute commands (currently, this only happens if user asks for
        help).
        """
            toplevel_options = self._get_toplevel_options
            self.commands = []
            parser = FancyGetopt(toplevel_options + self.display_options)
            parser.set_negative_aliases(self.negative_opt)
            parser.set_aliases({'licence': 'license'})
            args = parser.getopt(args=(self.script_args), object=self)
            option_order = parser.get_option_order
            log.set_verbosity(self.verbose)
            if self.handle_display_options(option_order):
                return
                while True:
                    if args:
                        args = self._parse_command_opts(parser, args)
                        if args is None:
                            return

                if self.help:
                    self._show_help(parser, display_options=(len(self.commands) == 0),
                      commands=(self.commands))
                    return
                if not self.commands:
                    raise DistutilsArgError('no commands supplied')
                return True

        def _get_toplevel_options(self):
            """Return the non-display options recognized at the top level.

        This includes options that are recognized *only* at the top
        level as well as options recognized for commands.
        """
            return self.global_options + [
             ('command-packages=', None, 'list of packages that provide distutils commands')]

        def _parse_command_opts(self, parser, args):
            """Parse the command-line options for a single command.
        'parser' must be a FancyGetopt instance; 'args' must be the list
        of arguments, starting with the current command (whose options
        we are about to parse).  Returns a new version of 'args' with
        the next command at the front of the list; will be the empty
        list if there are no more commands on the command line.  Returns
        None if the user asked for help on this command.
        """
            from distutils.cmd import Command
            command = args[0]
            if not command_re.match(command):
                raise SystemExit("invalid command name '%s'" % command)
            self.commands.append(command)
            try:
                cmd_class = self.get_command_class(command)
            except DistutilsModuleError as msg:
                try:
                    raise DistutilsArgError(msg)
                finally:
                    msg = None
                    del msg

            else:
                if not issubclass(cmd_class, Command):
                    raise DistutilsClassError('command class %s must subclass Command' % cmd_class)
                else:
                    if not (hasattr(cmd_class, 'user_options') and isinstance(cmd_class.user_options, list)):
                        msg = "command class %s must provide 'user_options' attribute (a list of tuples)"
                        raise DistutilsClassError(msg % cmd_class)
                    negative_opt = self.negative_opt
                    if hasattr(cmd_class, 'negative_opt'):
                        negative_opt = negative_opt.copy
                        negative_opt.update(cmd_class.negative_opt)
                    if hasattr(cmd_class, 'help_options') and isinstance(cmd_class.help_options, list):
                        help_options = fix_help_options(cmd_class.help_options)
                    else:
                        help_options = []
                    parser.set_option_table(self.global_options + cmd_class.user_options + help_options)
                    parser.set_negative_aliases(negative_opt)
                    args, opts = parser.getopt(args[1:])
                    if hasattr(opts, 'help'):
                        if opts.help:
                            self._show_help(parser, display_options=0, commands=[cmd_class])
                            return
                    if hasattr(cmd_class, 'help_options'):
                        if isinstance(cmd_class.help_options, list):
                            help_option_found = 0
                            for help_option, short, desc, func in cmd_class.help_options:
                                if hasattr(opts, parser.get_attr_name(help_option)):
                                    help_option_found = 1
                                    if callable(func):
                                        func
                                    else:
                                        raise DistutilsClassError("invalid help function %r for help option '%s': must be a callable object (function, etc.)" % (
                                         func, help_option))
                            else:
                                if help_option_found:
                                    return

                    opt_dict = self.get_option_dict(command)
                    for name, value in vars(opts).items:
                        opt_dict[name] = (
                         'command line', value)
                    else:
                        return args

        def finalize_options(self):
            """Set final values for all the options on the Distribution
        instance, analogous to the .finalize_options() method of Command
        objects.
        """
            for attr in ('keywords', 'platforms'):
                value = getattr(self.metadata, attr)
                if value is None:
                    pass
                else:
                    if isinstance(value, str):
                        value = [elm.strip for elm in value.split(',')]
                        setattrself.metadataattrvalue

        def _show_help(self, parser, global_options=1, display_options=1, commands=[]):
            """Show help for the setup script command-line in the form of
        several lists of command-line options.  'parser' should be a
        FancyGetopt instance; do not expect it to be returned in the
        same state, as its option table will be reset to make it
        generate the correct help text.

        If 'global_options' is true, lists the global options:
        --verbose, --dry-run, etc.  If 'display_options' is true, lists
        the "display-only" options: --name, --version, etc.  Finally,
        lists per-command help for every command name or command class
        in 'commands'.
        """
            from distutils.core import gen_usage
            from distutils.cmd import Command
            if global_options:
                if display_options:
                    options = self._get_toplevel_options
                else:
                    options = self.global_options
                parser.set_option_table(options)
                parser.print_help(self.common_usage + '\nGlobal options:')
                print('')
            if display_options:
                parser.set_option_table(self.display_options)
                parser.print_help('Information display options (just display information, ignore any commands)')
                print('')
            for command in self.commands:
                if isinstance(command, type) and issubclass(command, Command):
                    klass = command
                else:
                    klass = self.get_command_class(command)
                if hasattr(klass, 'help_options') and isinstance(klass.help_options, list):
                    parser.set_option_table(klass.user_options + fix_help_options(klass.help_options))
                else:
                    parser.set_option_table(klass.user_options)
                parser.print_help("Options for '%s' command:" % klass.__name__)
                print('')
            else:
                print(gen_usage(self.script_name))

        def handle_display_options(self, option_order):
            """If there were any non-global "display-only" options
        (--help-commands or the metadata display options) on the command
        line, display the requested info and return true; else return
        false.
        """
            from distutils.core import gen_usage
            if self.help_commands:
                self.print_commands
                print('')
                print(gen_usage(self.script_name))
                return 1
            any_display_options = 0
            is_display_option = {}
            for option in self.display_options:
                is_display_option[option[0]] = 1
            else:
                for opt, val in option_order:
                    if val:
                        if is_display_option.get(opt):
                            opt = translate_longopt(opt)
                            value = getattr(self.metadata, 'get_' + opt)
                            if opt in ('keywords', 'platforms'):
                                print(','.join(value))
                            elif opt in ('classifiers', 'provides', 'requires', 'obsoletes'):
                                print('\n'.join(value))
                            else:
                                print(value)
                            any_display_options = 1
                else:
                    return any_display_options

        def print_command_list(self, commands, header, max_length):
            """Print a subset of the list of all commands -- used by
        'print_commands()'.
        """
            print(header + ':')
            for cmd in commands:
                klass = self.cmdclass.get(cmd)
                if not klass:
                    klass = self.get_command_class(cmd)
                else:
                    try:
                        description = klass.description
                    except AttributeError:
                        description = '(no description available)'
                    else:
                        print('  %-*s  %s' % (max_length, cmd, description))

        def print_commands(self):
            """Print out a help message listing all available commands with a
        description of each.  The list is divided into "standard commands"
        (listed in distutils.command.__all__) and "extra commands"
        (mentioned in self.cmdclass, but not a standard command).  The
        descriptions come from the command class attribute
        'description'.
        """
            import distutils.command
            std_commands = distutils.command.__all__
            is_std = {}
            for cmd in std_commands:
                is_std[cmd] = 1
            else:
                extra_commands = []
                for cmd in self.cmdclass.keys:
                    if not is_std.get(cmd):
                        extra_commands.append(cmd)
                else:
                    max_length = 0
                    for cmd in std_commands + extra_commands:
                        if len(cmd) > max_length:
                            max_length = len(cmd)
                    else:
                        self.print_command_list(std_commands, 'Standard commands', max_length)
                        if extra_commands:
                            print
                            self.print_command_list(extra_commands, 'Extra commands', max_length)

        def get_command_list(self):
            """Get a list of (command, description) tuples.
        The list is divided into "standard commands" (listed in
        distutils.command.__all__) and "extra commands" (mentioned in
        self.cmdclass, but not a standard command).  The descriptions come
        from the command class attribute 'description'.
        """
            import distutils.command
            std_commands = distutils.command.__all__
            is_std = {}
            for cmd in std_commands:
                is_std[cmd] = 1
            else:
                extra_commands = []
                for cmd in self.cmdclass.keys:
                    if not is_std.get(cmd):
                        extra_commands.append(cmd)
                else:
                    rv = []
                    for cmd in std_commands + extra_commands:
                        klass = self.cmdclass.get(cmd)
                        if not klass:
                            klass = self.get_command_class(cmd)
                        else:
                            try:
                                description = klass.description
                            except AttributeError:
                                description = '(no description available)'
                            else:
                                rv.append((cmd, description))
                    else:
                        return rv

        def get_command_packages(self):
            """Return a list of packages from which commands are loaded."""
            pkgs = self.command_packages
            if not isinstance(pkgs, list):
                if pkgs is None:
                    pkgs = ''
                pkgs = [pkg.strip for pkg in pkgs.split(',') if pkg != '']
                if 'distutils.command' not in pkgs:
                    pkgs.insert(0, 'distutils.command')
                self.command_packages = pkgs
            return pkgs

        def get_command_class--- This code section failed: ---

 L. 819         0  LOAD_FAST                'self'
                2  LOAD_ATTR                cmdclass
                4  LOAD_METHOD              get
                6  LOAD_FAST                'command'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'klass'

 L. 820        12  LOAD_FAST                'klass'
               14  POP_JUMP_IF_FALSE    20  'to 20'

 L. 821        16  LOAD_FAST                'klass'
               18  RETURN_VALUE     
             20_0  COME_FROM            14  '14'

 L. 823        20  LOAD_FAST                'self'
               22  LOAD_METHOD              get_command_packages
               24  CALL_METHOD_0         0  ''
               26  GET_ITER         
             28_0  COME_FROM            88  '88'
               28  FOR_ITER            168  'to 168'
               30  STORE_FAST               'pkgname'

 L. 824        32  LOAD_STR                 '%s.%s'
               34  LOAD_FAST                'pkgname'
               36  LOAD_FAST                'command'
               38  BUILD_TUPLE_2         2 
               40  BINARY_MODULO    
               42  STORE_FAST               'module_name'

 L. 825        44  LOAD_FAST                'command'
               46  STORE_FAST               'klass_name'

 L. 827        48  SETUP_FINALLY        72  'to 72'

 L. 828        50  LOAD_GLOBAL              __import__
               52  LOAD_FAST                'module_name'
               54  CALL_FUNCTION_1       1  ''
               56  POP_TOP          

 L. 829        58  LOAD_GLOBAL              sys
               60  LOAD_ATTR                modules
               62  LOAD_FAST                'module_name'
               64  BINARY_SUBSCR    
               66  STORE_FAST               'module'
               68  POP_BLOCK        
               70  JUMP_FORWARD         96  'to 96'
             72_0  COME_FROM_FINALLY    48  '48'

 L. 830        72  DUP_TOP          
               74  LOAD_GLOBAL              ImportError
               76  COMPARE_OP               exception-match
               78  POP_JUMP_IF_FALSE    94  'to 94'
               80  POP_TOP          
               82  POP_TOP          
               84  POP_TOP          

 L. 831        86  POP_EXCEPT       
               88  JUMP_BACK            28  'to 28'
               90  POP_EXCEPT       
               92  JUMP_FORWARD         96  'to 96'
             94_0  COME_FROM            78  '78'
               94  END_FINALLY      
             96_0  COME_FROM            92  '92'
             96_1  COME_FROM            70  '70'

 L. 833        96  SETUP_FINALLY       112  'to 112'

 L. 834        98  LOAD_GLOBAL              getattr
              100  LOAD_FAST                'module'
              102  LOAD_FAST                'klass_name'
              104  CALL_FUNCTION_2       2  ''
              106  STORE_FAST               'klass'
              108  POP_BLOCK        
              110  JUMP_FORWARD        150  'to 150'
            112_0  COME_FROM_FINALLY    96  '96'

 L. 835       112  DUP_TOP          
              114  LOAD_GLOBAL              AttributeError
              116  COMPARE_OP               exception-match
              118  POP_JUMP_IF_FALSE   148  'to 148'
              120  POP_TOP          
              122  POP_TOP          
              124  POP_TOP          

 L. 836       126  LOAD_GLOBAL              DistutilsModuleError

 L. 837       128  LOAD_STR                 "invalid command '%s' (no class '%s' in module '%s')"

 L. 838       130  LOAD_FAST                'command'
              132  LOAD_FAST                'klass_name'
              134  LOAD_FAST                'module_name'
              136  BUILD_TUPLE_3         3 

 L. 837       138  BINARY_MODULO    

 L. 836       140  CALL_FUNCTION_1       1  ''
              142  RAISE_VARARGS_1       1  'exception instance'
              144  POP_EXCEPT       
              146  JUMP_FORWARD        150  'to 150'
            148_0  COME_FROM           118  '118'
              148  END_FINALLY      
            150_0  COME_FROM           146  '146'
            150_1  COME_FROM           110  '110'

 L. 840       150  LOAD_FAST                'klass'
              152  LOAD_FAST                'self'
              154  LOAD_ATTR                cmdclass
              156  LOAD_FAST                'command'
              158  STORE_SUBSCR     

 L. 841       160  LOAD_FAST                'klass'
              162  ROT_TWO          
              164  POP_TOP          
              166  RETURN_VALUE     
            168_0  COME_FROM            28  '28'

 L. 843       168  LOAD_GLOBAL              DistutilsModuleError
              170  LOAD_STR                 "invalid command '%s'"
              172  LOAD_FAST                'command'
              174  BINARY_MODULO    
              176  CALL_FUNCTION_1       1  ''
              178  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `COME_FROM' instruction at offset 94_0

        def get_command_obj(self, command, create=1):
            """Return the command object for 'command'.  Normally this object
        is cached on a previous call to 'get_command_obj()'; if no command
        object for 'command' is in the cache, then we either create and
        return it (if 'create' is true) or return None.
        """
            cmd_obj = self.command_obj.get(command)
            if not cmd_obj:
                if create:
                    if DEBUG:
                        self.announce("Distribution.get_command_obj(): creating '%s' command object" % command)
                    klass = self.get_command_class(command)
                    cmd_obj = self.command_obj[command] = klass(self)
                    self.have_run[command] = 0
                    options = self.command_options.get(command)
                    if options:
                        self._set_command_options(cmd_obj, options)
            return cmd_obj

        def _set_command_options(self, command_obj, option_dict=None):
            """Set the options for 'command_obj' from 'option_dict'.  Basically
        this means copying elements of a dictionary ('option_dict') to
        attributes of an instance ('command').

        'command_obj' must be a Command instance.  If 'option_dict' is not
        supplied, uses the standard option dictionary for this command
        (from 'self.command_options').
        """
            command_name = command_obj.get_command_name
            if option_dict is None:
                option_dict = self.get_option_dict(command_name)
            if DEBUG:
                self.announce("  setting options for '%s' command:" % command_name)
            for option, (source, value) in option_dict.items:
                if DEBUG:
                    self.announce('    %s = %s (from %s)' % (option, value,
                     source))
                else:
                    try:
                        bool_opts = [translate_longopt(o) for o in command_obj.boolean_options]
                    except AttributeError:
                        bool_opts = []
                    else:
                        try:
                            neg_opt = command_obj.negative_opt
                        except AttributeError:
                            neg_opt = {}
                        else:
                            try:
                                is_string = isinstance(value, str)
                                if option in neg_opt and is_string:
                                    setattrcommand_objneg_opt[option](not strtobool(value))
                                elif option in bool_opts and is_string:
                                    setattrcommand_objoptionstrtobool(value)
                                elif hasattr(command_obj, option):
                                    setattrcommand_objoptionvalue
                                else:
                                    raise DistutilsOptionError("error in %s: command '%s' has no such option '%s'" % (
                                     source, command_name, option))
                            except ValueError as msg:
                                try:
                                    raise DistutilsOptionError(msg)
                                finally:
                                    msg = None
                                    del msg

        def reinitialize_command(self, command, reinit_subcommands=0):
            """Reinitializes a command to the state it was in when first
        returned by 'get_command_obj()': ie., initialized but not yet
        finalized.  This provides the opportunity to sneak option
        values in programmatically, overriding or supplementing
        user-supplied values from the config files and command line.
        You'll have to re-finalize the command object (by calling
        'finalize_options()' or 'ensure_finalized()') before using it for
        real.

        'command' should be a command name (string) or command object.  If
        'reinit_subcommands' is true, also reinitializes the command's
        sub-commands, as declared by the 'sub_commands' class attribute (if
        it has one).  See the "install" command for an example.  Only
        reinitializes the sub-commands that actually matter, ie. those
        whose test predicates return true.

        Returns the reinitialized command object.
        """
            from distutils.cmd import Command
            if not isinstance(command, Command):
                command_name = command
                command = self.get_command_obj(command_name)
            else:
                command_name = command.get_command_name
            if not command.finalized:
                return command
            command.initialize_options
            command.finalized = 0
            self.have_run[command_name] = 0
            self._set_command_options(command)
            if reinit_subcommands:
                for sub in command.get_sub_commands:
                    self.reinitialize_command(sub, reinit_subcommands)

                return command

        def announce(self, msg, level=log.INFO):
            log.log(level, msg)

        def run_commands(self):
            """Run each command that was seen on the setup script command line.
        Uses the list of commands found and cache of command objects
        created by 'get_command_obj()'.
        """
            for cmd in self.commands:
                self.run_command(cmd)

        def run_command(self, command):
            """Do whatever it takes to run a command (including nothing at all,
        if the command has already been run).  Specifically: if we have
        already created and run the command named by 'command', return
        silently without doing anything.  If the command named by 'command'
        doesn't even have a command object yet, create one.  Then invoke
        'run()' on that command object (or an existing one).
        """
            if self.have_run.get(command):
                return
            log.info('running %s', command)
            cmd_obj = self.get_command_obj(command)
            cmd_obj.ensure_finalized
            cmd_obj.run
            self.have_run[command] = 1

        def has_pure_modules(self):
            return len(self.packages or self.py_modules or []) > 0

        def has_ext_modules(self):
            return self.ext_modules and len(self.ext_modules) > 0

        def has_c_libraries(self):
            return self.libraries and len(self.libraries) > 0

        def has_modules(self):
            return self.has_pure_modules or self.has_ext_modules

        def has_headers(self):
            return self.headers and len(self.headers) > 0

        def has_scripts(self):
            return self.scripts and len(self.scripts) > 0

        def has_data_files(self):
            return self.data_files and len(self.data_files) > 0

        def is_pure(self):
            return self.has_pure_modules and not self.has_ext_modules and not self.has_c_libraries


    class DistributionMetadata:
        __doc__ = 'Dummy class to hold the distribution meta-data: name, version,\n    author, and so forth.\n    '
        _METHOD_BASENAMES = ('name', 'version', 'author', 'author_email', 'maintainer',
                             'maintainer_email', 'url', 'license', 'description',
                             'long_description', 'keywords', 'platforms', 'fullname',
                             'contact', 'contact_email', 'classifiers', 'download_url',
                             'provides', 'requires', 'obsoletes')

        def __init__(self, path=None):
            if path is not None:
                self.read_pkg_file(open(path))
            else:
                self.name = None
                self.version = None
                self.author = None
                self.author_email = None
                self.maintainer = None
                self.maintainer_email = None
                self.url = None
                self.license = None
                self.description = None
                self.long_description = None
                self.keywords = None
                self.platforms = None
                self.classifiers = None
                self.download_url = None
                self.provides = None
                self.requires = None
                self.obsoletes = None

        def read_pkg_file(self, file):
            """Reads the metadata values from a file object."""
            msg = message_from_file(file)

            def _read_field(name):
                value = msg[name]
                if value == 'UNKNOWN':
                    return
                return value

            def _read_list(name):
                values = msg.get_all(name, None)
                if values == []:
                    return
                return values

            metadata_version = msg['metadata-version']
            self.name = _read_field('name')
            self.version = _read_field('version')
            self.description = _read_field('summary')
            self.author = _read_field('author')
            self.maintainer = None
            self.author_email = _read_field('author-email')
            self.maintainer_email = None
            self.url = _read_field('home-page')
            self.license = _read_field('license')
            if 'download-url' in msg:
                self.download_url = _read_field('download-url')
            else:
                self.download_url = None
            self.long_description = _read_field('description')
            self.description = _read_field('summary')
            if 'keywords' in msg:
                self.keywords = _read_field('keywords').split(',')
            self.platforms = _read_list('platform')
            self.classifiers = _read_list('classifier')
            if metadata_version == '1.1':
                self.requires = _read_list('requires')
                self.provides = _read_list('provides')
                self.obsoletes = _read_list('obsoletes')
            else:
                self.requires = None
                self.provides = None
                self.obsoletes = None

        def write_pkg_info(self, base_dir):
            """Write the PKG-INFO file into the release tree.
        """
            with open((os.path.join(base_dir, 'PKG-INFO')), 'w', encoding='UTF-8') as pkg_info:
                self.write_pkg_file(pkg_info)

        def write_pkg_file(self, file):
            """Write the PKG-INFO format data to a file object.
        """
            version = '1.0'
            if self.provides or (self.requires or self.obsoletes or self.classifiers or self.download_url):
                version = '1.1'
            file.write('Metadata-Version: %s\n' % version)
            file.write('Name: %s\n' % self.get_name)
            file.write('Version: %s\n' % self.get_version)
            file.write('Summary: %s\n' % self.get_description)
            file.write('Home-page: %s\n' % self.get_url)
            file.write('Author: %s\n' % self.get_contact)
            file.write('Author-email: %s\n' % self.get_contact_email)
            file.write('License: %s\n' % self.get_license)
            if self.download_url:
                file.write('Download-URL: %s\n' % self.download_url)
            long_desc = rfc822_escape(self.get_long_description)
            file.write('Description: %s\n' % long_desc)
            keywords = ','.join(self.get_keywords)
            if keywords:
                file.write('Keywords: %s\n' % keywords)
            self._write_list(file, 'Platform', self.get_platforms)
            self._write_list(file, 'Classifier', self.get_classifiers)
            self._write_list(file, 'Requires', self.get_requires)
            self._write_list(file, 'Provides', self.get_provides)
            self._write_list(file, 'Obsoletes', self.get_obsoletes)

        def _write_list(self, file, name, values):
            for value in values:
                file.write('%s: %s\n' % (name, value))

        def get_name(self):
            return self.name or 'UNKNOWN'

        def get_version(self):
            return self.version or '0.0.0'

        def get_fullname(self):
            return '%s-%s' % (self.get_name, self.get_version)

        def get_author(self):
            return self.author or 'UNKNOWN'

        def get_author_email(self):
            return self.author_email or 'UNKNOWN'

        def get_maintainer(self):
            return self.maintainer or 'UNKNOWN'

        def get_maintainer_email(self):
            return self.maintainer_email or 'UNKNOWN'

        def get_contact(self):
            return self.maintainer or self.author or 'UNKNOWN'

        def get_contact_email(self):
            return self.maintainer_email or self.author_email or 'UNKNOWN'

        def get_url(self):
            return self.url or 'UNKNOWN'

        def get_license(self):
            return self.license or 'UNKNOWN'

        get_licence = get_license

        def get_description(self):
            return self.description or 'UNKNOWN'

        def get_long_description(self):
            return self.long_description or 'UNKNOWN'

        def get_keywords(self):
            return self.keywords or []

        def set_keywords(self, value):
            self.keywords = _ensure_list(value, 'keywords')

        def get_platforms(self):
            return self.platforms or ['UNKNOWN']

        def set_platforms(self, value):
            self.platforms = _ensure_list(value, 'platforms')

        def get_classifiers(self):
            return self.classifiers or []

        def set_classifiers(self, value):
            self.classifiers = _ensure_list(value, 'classifiers')

        def get_download_url(self):
            return self.download_url or 'UNKNOWN'

        def get_requires(self):
            return self.requires or []

        def set_requires(self, value):
            import distutils.versionpredicate
            for v in value:
                distutils.versionpredicate.VersionPredicate(v)
            else:
                self.requires = list(value)

        def get_provides(self):
            return self.provides or []

        def set_provides(self, value):
            value = [v.strip for v in value]
            for v in value:
                import distutils.versionpredicate
                distutils.versionpredicate.split_provision(v)
            else:
                self.provides = value

        def get_obsoletes(self):
            return self.obsoletes or []

        def set_obsoletes(self, value):
            import distutils.versionpredicate
            for v in value:
                distutils.versionpredicate.VersionPredicate(v)
            else:
                self.obsoletes = list(value)


    def fix_help_options(options):
        """Convert a 4-tuple 'help_options' list as found in various command
    classes to the 3-tuple form required by FancyGetopt.
    """
        new_options = []
        for help_tuple in options:
            new_options.append(help_tuple[0:3])
        else:
            return new_options