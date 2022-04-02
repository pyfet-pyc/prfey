# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: numpy\distutils\command\build_src.py
""" Build swig and f2py sources.
"""
import os, re, sys, shlex, copy
from distutils.command import build_ext
from distutils.dep_util import newer_group, newer
from distutils.util import get_platform
from distutils.errors import DistutilsError, DistutilsSetupError
from numpy.distutils import log
from numpy.distutils.misc_util import fortran_ext_match, appendpath, is_string, is_sequence, get_cmd
import numpy.distutils.from_template as process_f_file
import numpy.distutils.conv_template as process_c_file

def subst_vars(target, source, d):
    """Substitute any occurrence of @foo@ by d['foo'] from source file into
    target."""
    var = re.compile('@([a-zA-Z_]+)@')
    with open(source, 'r') as fs:
        with open(target, 'w') as ft:
            for l in fs:
                m = var.search(l)
                if m:
                    ft.write(l.replace('@%s@' % m.group(1), d[m.group(1)]))
                else:
                    ft.write(l)


class build_src(build_ext.build_ext):
    description = 'build sources from SWIG, F2PY files or a function'
    user_options = [
     ('build-src=', 'd', 'directory to "build" sources to'),
     ('f2py-opts=', None, 'list of f2py command line options'),
     ('swig=', None, 'path to the SWIG executable'),
     ('swig-opts=', None, 'list of SWIG command line options'),
     ('swig-cpp', None, 'make SWIG create C++ files (default is autodetected from sources)'),
     ('f2pyflags=', None, 'additional flags to f2py (use --f2py-opts= instead)'),
     ('swigflags=', None, 'additional flags to swig (use --swig-opts= instead)'),
     ('force', 'f', 'forcibly build everything (ignore file timestamps)'),
     ('inplace', 'i', 'ignore build-lib and put compiled extensions into the source directory alongside your pure Python modules'),
     ('verbose-cfg', None, 'change logging level from WARN to INFO which will show all compiler output')]
    boolean_options = [
     'force', 'inplace', 'verbose-cfg']
    help_options = []

    def initialize_options(self):
        self.extensions = None
        self.package = None
        self.py_modules = None
        self.py_modules_dict = None
        self.build_src = None
        self.build_lib = None
        self.build_base = None
        self.force = None
        self.inplace = None
        self.package_dir = None
        self.f2pyflags = None
        self.f2py_opts = None
        self.swigflags = None
        self.swig_opts = None
        self.swig_cpp = None
        self.swig = None
        self.verbose_cfg = None

    def finalize_options(self):
        self.set_undefined_options('build', ('build_base', 'build_base'), ('build_lib',
                                                                           'build_lib'), ('force',
                                                                                          'force'))
        if self.package is None:
            self.package = self.distribution.ext_package
        self.extensions = self.distribution.ext_modules
        self.libraries = self.distribution.libraries or []
        self.py_modules = self.distribution.py_modules or []
        self.data_files = self.distribution.data_files or []
        if self.build_src is None:
            plat_specifier = ('.{}-{}.{}'.format)(get_platform(), *sys.version_info[:2])
            self.build_src = os.path.join(self.build_base, 'src' + plat_specifier)
        self.py_modules_dict = {}
        if self.f2pyflags:
            if self.f2py_opts:
                log.warn('ignoring --f2pyflags as --f2py-opts already used')
            else:
                self.f2py_opts = self.f2pyflags
            self.f2pyflags = None
        if self.f2py_opts is None:
            self.f2py_opts = []
        else:
            self.f2py_opts = shlex.split(self.f2py_opts)
        if self.swigflags:
            if self.swig_opts:
                log.warn('ignoring --swigflags as --swig-opts already used')
            else:
                self.swig_opts = self.swigflags
            self.swigflags = None
        if self.swig_opts is None:
            self.swig_opts = []
        else:
            self.swig_opts = shlex.split(self.swig_opts)
        build_ext = self.get_finalized_command('build_ext')
        if self.inplace is None:
            self.inplace = build_ext.inplace
        if self.swig_cpp is None:
            self.swig_cpp = build_ext.swig_cpp
        for c in ('swig', 'swig_opt'):
            o = '--' + c.replace('_', '-')
            v = getattr(build_ext, c, None)
            if v:
                if getattr(self, c):
                    log.warn('both build_src and build_ext define %s option' % o)
                else:
                    log.info('using "%s=%s" option from build_ext command' % (o, v))
                    setattr(self, c, v)

    def run(self):
        log.info('build_src')
        if not self.extensions:
            if not self.libraries:
                return
        self.build_sources()

    def build_sources(self):
        if self.inplace:
            self.get_package_dir = self.get_finalized_command('build_py').get_package_dir
        self.build_py_modules_sources()
        for libname_info in self.libraries:
            (self.build_library_sources)(*libname_info)

        if self.extensions:
            self.check_extensions_list(self.extensions)
            for ext in self.extensions:
                self.build_extension_sources(ext)

        self.build_data_files_sources()
        self.build_npy_pkg_config()

    def build_data_files_sources(self):
        if not self.data_files:
            return
        log.info('building data_files sources')
        from numpy.distutils.misc_util import get_data_files
        new_data_files = []
        for data in self.data_files:
            if isinstance(data, str):
                new_data_files.append(data)
            else:
                if isinstance(data, tuple):
                    d, files = data
                    if self.inplace:
                        build_dir = self.get_package_dir('.'.join(d.split(os.sep)))
                    else:
                        build_dir = os.path.join(self.build_src, d)
                    funcs = [f for f in files if hasattr(f, '__call__')]
                    files = [f for f in files if not hasattr(f, '__call__')]
                    for f in funcs:
                        if f.__code__.co_argcount == 1:
                            s = f(build_dir)
                        else:
                            s = f()
                        if s is not None:
                            if isinstance(s, list):
                                files.extend(s)
                            else:
                                if isinstance(s, str):
                                    files.append(s)
                                else:
                                    raise TypeError(repr(s))

                    filenames = get_data_files((d, files))
                    new_data_files.append((d, filenames))
                else:
                    raise TypeError(repr(data))

        self.data_files[:] = new_data_files

    def _build_npy_pkg_config(self, info, gd):
        template, install_dir, subst_dict = info
        template_dir = os.path.dirname(template)
        for k, v in gd.items():
            subst_dict[k] = v

        if self.inplace == 1:
            generated_dir = os.path.join(template_dir, install_dir)
        else:
            generated_dir = os.path.join(self.build_src, template_dir, install_dir)
        generated = os.path.basename(os.path.splitext(template)[0])
        generated_path = os.path.join(generated_dir, generated)
        if not os.path.exists(generated_dir):
            os.makedirs(generated_dir)
        subst_vars(generated_path, template, subst_dict)
        full_install_dir = os.path.join(template_dir, install_dir)
        return (
         full_install_dir, generated_path)

    def build_npy_pkg_config(self):
        log.info('build_src: building npy-pkg config files')
        install_cmd = copy.copy(get_cmd('install'))
        if not install_cmd.finalized == 1:
            install_cmd.finalize_options()
        build_npkg = False
        if self.inplace == 1:
            top_prefix = '.'
            build_npkg = True
        elif hasattr(install_cmd, 'install_libbase'):
            top_prefix = install_cmd.install_libbase
            build_npkg = True
        if build_npkg:
            for pkg, infos in self.distribution.installed_pkg_config.items():
                pkg_path = self.distribution.package_dir[pkg]
                prefix = os.path.join(os.path.abspath(top_prefix), pkg_path)
                d = {'prefix': prefix}
                for info in infos:
                    install_dir, generated = self._build_npy_pkg_config(info, d)
                    self.distribution.data_files.append((install_dir,
                     [
                      generated]))

    def build_py_modules_sources(self):
        if not self.py_modules:
            return
        log.info('building py_modules sources')
        new_py_modules = []
        for source in self.py_modules:
            if is_sequence(source) and len(source) == 3:
                package, module_base, source = source
                if self.inplace:
                    build_dir = self.get_package_dir(package)
                else:
                    build_dir = os.path.join(self.build_src, (os.path.join)(*package.split('.')))
                if hasattr(source, '__call__'):
                    target = os.path.join(build_dir, module_base + '.py')
                    source = source(target)
                if source is None:
                    continue
                else:
                    modules = [
                     (
                      package, module_base, source)]
                    if package not in self.py_modules_dict:
                        self.py_modules_dict[package] = []
                    self.py_modules_dict[package] += modules
            else:
                new_py_modules.append(source)

        self.py_modules[:] = new_py_modules

    def build_library_sources(self, lib_name, build_info):
        sources = list(build_info.get('sources', []))
        if not sources:
            return
        log.info('building library "%s" sources' % lib_name)
        sources = self.generate_sources(sources, (lib_name, build_info))
        sources = self.template_sources(sources, (lib_name, build_info))
        sources, h_files = self.filter_h_files(sources)
        if h_files:
            log.info('%s - nothing done with h_files = %s', self.package, h_files)
        build_info['sources'] = sources

    def build_extension_sources(self, ext):
        sources = list(ext.sources)
        log.info('building extension "%s" sources' % ext.name)
        fullname = self.get_ext_fullname(ext.name)
        modpath = fullname.split('.')
        package = '.'.join(modpath[0:-1])
        if self.inplace:
            self.ext_target_dir = self.get_package_dir(package)
        sources = self.generate_sources(sources, ext)
        sources = self.template_sources(sources, ext)
        sources = self.swig_sources(sources, ext)
        sources = self.f2py_sources(sources, ext)
        sources = self.pyrex_sources(sources, ext)
        sources, py_files = self.filter_py_files(sources)
        if package not in self.py_modules_dict:
            self.py_modules_dict[package] = []
        modules = []
        for f in py_files:
            module = os.path.splitext(os.path.basename(f))[0]
            modules.append((package, module, f))

        self.py_modules_dict[package] += modules
        sources, h_files = self.filter_h_files(sources)
        if h_files:
            log.info('%s - nothing done with h_files = %s', package, h_files)
        ext.sources = sources

    def generate_sources(self, sources, extension):
        new_sources = []
        func_sources = []
        for source in sources:
            if is_string(source):
                new_sources.append(source)
            else:
                func_sources.append(source)

        if not func_sources:
            return new_sources
        if self.inplace and not is_sequence(extension):
            build_dir = self.ext_target_dir
        else:
            if is_sequence(extension):
                name = extension[0]
            else:
                name = extension.name
            build_dir = (os.path.join)(*[self.build_src] + name.split('.')[:-1])
        self.mkpath(build_dir)
        if self.verbose_cfg:
            new_level = log.INFO
        else:
            new_level = log.WARN
        old_level = log.set_threshold(new_level)
        for func in func_sources:
            source = func(extension, build_dir)
            if not source:
                continue
            if is_sequence(source):
                [log.info("  adding '%s' to sources." % (s,)) for s in source]
                new_sources.extend(source)
            else:
                log.info("  adding '%s' to sources." % (source,))
                new_sources.append(source)

        log.set_threshold(old_level)
        return new_sources

    def filter_py_files(self, sources):
        return self.filter_files(sources, ['.py'])

    def filter_h_files(self, sources):
        return self.filter_files(sources, ['.h', '.hpp', '.inc'])

    def filter_files(self, sources, exts=[]):
        new_sources = []
        files = []
        for source in sources:
            base, ext = os.path.splitext(source)
            if ext in exts:
                files.append(source)
            else:
                new_sources.append(source)

        return (
         new_sources, files)

    def template_sources(self, sources, extension):
        new_sources = []
        if is_sequence(extension):
            depends = extension[1].get('depends')
            include_dirs = extension[1].get('include_dirs')
        else:
            depends = extension.depends
            include_dirs = extension.include_dirs
        for source in sources:
            base, ext = os.path.splitext(source)
            if ext == '.src':
                if self.inplace:
                    target_dir = os.path.dirname(base)
                else:
                    target_dir = appendpath(self.build_src, os.path.dirname(base))
                self.mkpath(target_dir)
                target_file = os.path.join(target_dir, os.path.basename(base))
                if self.force or newer_group([source] + depends, target_file):
                    if _f_pyf_ext_match(base):
                        log.info('from_template:> %s' % target_file)
                        outstr = process_f_file(source)
                    else:
                        log.info('conv_template:> %s' % target_file)
                        outstr = process_c_file(source)
                    with open(target_file, 'w') as fid:
                        fid.write(outstr)
                else:
                    if _header_ext_match(target_file):
                        d = os.path.dirname(target_file)
                        if d not in include_dirs:
                            log.info("  adding '%s' to include_dirs." % d)
                            include_dirs.append(d)
                    new_sources.append(target_file)
            else:
                new_sources.append(source)

        return new_sources

    def pyrex_sources(self, sources, extension):
        """Pyrex not supported; this remains for Cython support (see below)"""
        new_sources = []
        ext_name = extension.name.split('.')[(-1)]
        for source in sources:
            base, ext = os.path.splitext(source)
            if ext == '.pyx':
                target_file = self.generate_a_pyrex_source(base, ext_name, source, extension)
                new_sources.append(target_file)
            else:
                new_sources.append(source)

        return new_sources

    def generate_a_pyrex_source(self, base, ext_name, source, extension):
        """Pyrex is not supported, but some projects monkeypatch this method.

        That allows compiling Cython code, see gh-6955.
        This method will remain here for compatibility reasons.
        """
        return []

    def f2py_sources--- This code section failed: ---

 L. 467         0  BUILD_LIST_0          0 
                2  STORE_FAST               'new_sources'

 L. 468         4  BUILD_LIST_0          0 
                6  STORE_FAST               'f2py_sources'

 L. 469         8  BUILD_LIST_0          0 
               10  STORE_FAST               'f_sources'

 L. 470        12  BUILD_MAP_0           0 
               14  STORE_FAST               'f2py_targets'

 L. 471        16  BUILD_LIST_0          0 
               18  STORE_FAST               'target_dirs'

 L. 472        20  LOAD_FAST                'extension'
               22  LOAD_ATTR                name
               24  LOAD_METHOD              split
               26  LOAD_STR                 '.'
               28  CALL_METHOD_1         1  '1 positional argument'
               30  LOAD_CONST               -1
               32  BINARY_SUBSCR    
               34  STORE_FAST               'ext_name'

 L. 473        36  LOAD_CONST               0
               38  STORE_FAST               'skip_f2py'

 L. 475     40_42  SETUP_LOOP          406  'to 406'
               44  LOAD_FAST                'sources'
               46  GET_ITER         
             48_0  COME_FROM           402  '402'
             48_1  COME_FROM           390  '390'
             48_2  COME_FROM           368  '368'
            48_50  FOR_ITER            404  'to 404'
               52  STORE_FAST               'source'

 L. 476        54  LOAD_GLOBAL              os
               56  LOAD_ATTR                path
               58  LOAD_METHOD              splitext
               60  LOAD_FAST                'source'
               62  CALL_METHOD_1         1  '1 positional argument'
               64  UNPACK_SEQUENCE_2     2 
               66  STORE_FAST               'base'
               68  STORE_FAST               'ext'

 L. 477        70  LOAD_FAST                'ext'
               72  LOAD_STR                 '.pyf'
               74  COMPARE_OP               ==
            76_78  POP_JUMP_IF_FALSE   370  'to 370'

 L. 478        80  LOAD_FAST                'self'
               82  LOAD_ATTR                inplace
               84  POP_JUMP_IF_FALSE   100  'to 100'

 L. 479        86  LOAD_GLOBAL              os
               88  LOAD_ATTR                path
               90  LOAD_METHOD              dirname
               92  LOAD_FAST                'base'
               94  CALL_METHOD_1         1  '1 positional argument'
               96  STORE_FAST               'target_dir'
               98  JUMP_FORWARD        120  'to 120'
            100_0  COME_FROM            84  '84'

 L. 481       100  LOAD_GLOBAL              appendpath
              102  LOAD_FAST                'self'
              104  LOAD_ATTR                build_src
              106  LOAD_GLOBAL              os
              108  LOAD_ATTR                path
              110  LOAD_METHOD              dirname
              112  LOAD_FAST                'base'
              114  CALL_METHOD_1         1  '1 positional argument'
              116  CALL_FUNCTION_2       2  '2 positional arguments'
              118  STORE_FAST               'target_dir'
            120_0  COME_FROM            98  '98'

 L. 482       120  LOAD_GLOBAL              os
              122  LOAD_ATTR                path
              124  LOAD_METHOD              isfile
              126  LOAD_FAST                'source'
              128  CALL_METHOD_1         1  '1 positional argument'
              130  POP_JUMP_IF_FALSE   186  'to 186'

 L. 483       132  LOAD_GLOBAL              get_f2py_modulename
              134  LOAD_FAST                'source'
              136  CALL_FUNCTION_1       1  '1 positional argument'
              138  STORE_FAST               'name'

 L. 484       140  LOAD_FAST                'name'
              142  LOAD_FAST                'ext_name'
              144  COMPARE_OP               !=
              146  POP_JUMP_IF_FALSE   166  'to 166'

 L. 485       148  LOAD_GLOBAL              DistutilsSetupError
              150  LOAD_STR                 'mismatch of extension names: %s provides %r but expected %r'

 L. 487       152  LOAD_FAST                'source'
              154  LOAD_FAST                'name'
              156  LOAD_FAST                'ext_name'
              158  BUILD_TUPLE_3         3 
              160  BINARY_MODULO    
              162  CALL_FUNCTION_1       1  '1 positional argument'
              164  RAISE_VARARGS_1       1  'exception instance'
            166_0  COME_FROM           146  '146'

 L. 488       166  LOAD_GLOBAL              os
              168  LOAD_ATTR                path
              170  LOAD_METHOD              join
              172  LOAD_FAST                'target_dir'
              174  LOAD_FAST                'name'
              176  LOAD_STR                 'module.c'
              178  BINARY_ADD       
              180  CALL_METHOD_2         2  '2 positional arguments'
              182  STORE_FAST               'target_file'
              184  JUMP_FORWARD        330  'to 330'
            186_0  COME_FROM           130  '130'

 L. 490       186  LOAD_GLOBAL              log
              188  LOAD_METHOD              debug
              190  LOAD_STR                 "  source %s does not exist: skipping f2py'ing."

 L. 491       192  LOAD_FAST                'source'
              194  BINARY_MODULO    
              196  CALL_METHOD_1         1  '1 positional argument'
              198  POP_TOP          

 L. 492       200  LOAD_FAST                'ext_name'
              202  STORE_FAST               'name'

 L. 493       204  LOAD_CONST               1
              206  STORE_FAST               'skip_f2py'

 L. 494       208  LOAD_GLOBAL              os
              210  LOAD_ATTR                path
              212  LOAD_METHOD              join
              214  LOAD_FAST                'target_dir'
              216  LOAD_FAST                'name'
              218  LOAD_STR                 'module.c'
              220  BINARY_ADD       
              222  CALL_METHOD_2         2  '2 positional arguments'
              224  STORE_FAST               'target_file'

 L. 495       226  LOAD_GLOBAL              os
              228  LOAD_ATTR                path
              230  LOAD_METHOD              isfile
              232  LOAD_FAST                'target_file'
              234  CALL_METHOD_1         1  '1 positional argument'
          236_238  POP_JUMP_IF_TRUE    330  'to 330'

 L. 496       240  LOAD_GLOBAL              log
              242  LOAD_METHOD              warn
              244  LOAD_STR                 '  target %s does not exist:\n   Assuming %smodule.c was generated with "build_src --inplace" command.'

 L. 499       246  LOAD_FAST                'target_file'
              248  LOAD_FAST                'name'
              250  BUILD_TUPLE_2         2 
              252  BINARY_MODULO    
              254  CALL_METHOD_1         1  '1 positional argument'
              256  POP_TOP          

 L. 500       258  LOAD_GLOBAL              os
              260  LOAD_ATTR                path
              262  LOAD_METHOD              dirname
              264  LOAD_FAST                'base'
              266  CALL_METHOD_1         1  '1 positional argument'
              268  STORE_FAST               'target_dir'

 L. 501       270  LOAD_GLOBAL              os
              272  LOAD_ATTR                path
              274  LOAD_METHOD              join
              276  LOAD_FAST                'target_dir'
              278  LOAD_FAST                'name'
              280  LOAD_STR                 'module.c'
              282  BINARY_ADD       
              284  CALL_METHOD_2         2  '2 positional arguments'
              286  STORE_FAST               'target_file'

 L. 502       288  LOAD_GLOBAL              os
              290  LOAD_ATTR                path
              292  LOAD_METHOD              isfile
              294  LOAD_FAST                'target_file'
              296  CALL_METHOD_1         1  '1 positional argument'
          298_300  POP_JUMP_IF_TRUE    316  'to 316'

 L. 503       302  LOAD_GLOBAL              DistutilsSetupError
              304  LOAD_STR                 '%r missing'
              306  LOAD_FAST                'target_file'
              308  BUILD_TUPLE_1         1 
              310  BINARY_MODULO    
              312  CALL_FUNCTION_1       1  '1 positional argument'
              314  RAISE_VARARGS_1       1  'exception instance'
            316_0  COME_FROM           298  '298'

 L. 504       316  LOAD_GLOBAL              log
              318  LOAD_METHOD              info
              320  LOAD_STR                 '   Yes! Using %r as up-to-date target.'

 L. 505       322  LOAD_FAST                'target_file'
              324  BINARY_MODULO    
              326  CALL_METHOD_1         1  '1 positional argument'
              328  POP_TOP          
            330_0  COME_FROM           236  '236'
            330_1  COME_FROM           184  '184'

 L. 506       330  LOAD_FAST                'target_dirs'
              332  LOAD_METHOD              append
              334  LOAD_FAST                'target_dir'
              336  CALL_METHOD_1         1  '1 positional argument'
              338  POP_TOP          

 L. 507       340  LOAD_FAST                'f2py_sources'
              342  LOAD_METHOD              append
              344  LOAD_FAST                'source'
              346  CALL_METHOD_1         1  '1 positional argument'
              348  POP_TOP          

 L. 508       350  LOAD_FAST                'target_file'
              352  LOAD_FAST                'f2py_targets'
              354  LOAD_FAST                'source'
              356  STORE_SUBSCR     

 L. 509       358  LOAD_FAST                'new_sources'
              360  LOAD_METHOD              append
              362  LOAD_FAST                'target_file'
              364  CALL_METHOD_1         1  '1 positional argument'
              366  POP_TOP          
              368  JUMP_BACK            48  'to 48'
            370_0  COME_FROM            76  '76'

 L. 510       370  LOAD_GLOBAL              fortran_ext_match
              372  LOAD_FAST                'ext'
              374  CALL_FUNCTION_1       1  '1 positional argument'
          376_378  POP_JUMP_IF_FALSE   392  'to 392'

 L. 511       380  LOAD_FAST                'f_sources'
              382  LOAD_METHOD              append
              384  LOAD_FAST                'source'
              386  CALL_METHOD_1         1  '1 positional argument'
              388  POP_TOP          
              390  JUMP_BACK            48  'to 48'
            392_0  COME_FROM           376  '376'

 L. 513       392  LOAD_FAST                'new_sources'
              394  LOAD_METHOD              append
              396  LOAD_FAST                'source'
              398  CALL_METHOD_1         1  '1 positional argument'
              400  POP_TOP          
              402  JUMP_BACK            48  'to 48'
              404  POP_BLOCK        
            406_0  COME_FROM_LOOP       40  '40'

 L. 515       406  LOAD_FAST                'f2py_sources'
          408_410  POP_JUMP_IF_TRUE    422  'to 422'
              412  LOAD_FAST                'f_sources'
          414_416  POP_JUMP_IF_TRUE    422  'to 422'

 L. 516       418  LOAD_FAST                'new_sources'
              420  RETURN_VALUE     
            422_0  COME_FROM           414  '414'
            422_1  COME_FROM           408  '408'

 L. 518       422  SETUP_LOOP          448  'to 448'
              424  LOAD_FAST                'target_dirs'
              426  GET_ITER         
            428_0  COME_FROM           442  '442'
              428  FOR_ITER            446  'to 446'
              430  STORE_FAST               'd'

 L. 519       432  LOAD_FAST                'self'
              434  LOAD_METHOD              mkpath
              436  LOAD_FAST                'd'
              438  CALL_METHOD_1         1  '1 positional argument'
              440  POP_TOP          
          442_444  JUMP_BACK           428  'to 428'
              446  POP_BLOCK        
            448_0  COME_FROM_LOOP      422  '422'

 L. 521       448  LOAD_FAST                'extension'
              450  LOAD_ATTR                f2py_options
              452  LOAD_FAST                'self'
              454  LOAD_ATTR                f2py_opts
              456  BINARY_ADD       
              458  STORE_FAST               'f2py_options'

 L. 523       460  LOAD_FAST                'self'
              462  LOAD_ATTR                distribution
              464  LOAD_ATTR                libraries
          466_468  POP_JUMP_IF_FALSE   524  'to 524'

 L. 524       470  SETUP_LOOP          524  'to 524'
              472  LOAD_FAST                'self'
              474  LOAD_ATTR                distribution
              476  LOAD_ATTR                libraries
              478  GET_ITER         
            480_0  COME_FROM           518  '518'
            480_1  COME_FROM           496  '496'
              480  FOR_ITER            522  'to 522'
              482  UNPACK_SEQUENCE_2     2 
              484  STORE_FAST               'name'
              486  STORE_FAST               'build_info'

 L. 525       488  LOAD_FAST                'name'
              490  LOAD_FAST                'extension'
              492  LOAD_ATTR                libraries
              494  COMPARE_OP               in
          496_498  POP_JUMP_IF_FALSE_BACK   480  'to 480'

 L. 526       500  LOAD_FAST                'f2py_options'
              502  LOAD_METHOD              extend
              504  LOAD_FAST                'build_info'
              506  LOAD_METHOD              get
              508  LOAD_STR                 'f2py_options'
              510  BUILD_LIST_0          0 
              512  CALL_METHOD_2         2  '2 positional arguments'
              514  CALL_METHOD_1         1  '1 positional argument'
              516  POP_TOP          
          518_520  JUMP_BACK           480  'to 480'
              522  POP_BLOCK        
            524_0  COME_FROM_LOOP      470  '470'
            524_1  COME_FROM           466  '466'

 L. 528       524  LOAD_GLOBAL              log
              526  LOAD_METHOD              info
              528  LOAD_STR                 'f2py options: %s'
              530  LOAD_FAST                'f2py_options'
              532  BINARY_MODULO    
              534  CALL_METHOD_1         1  '1 positional argument'
              536  POP_TOP          

 L. 530       538  LOAD_FAST                'f2py_sources'
          540_542  POP_JUMP_IF_FALSE   708  'to 708'

 L. 531       544  LOAD_GLOBAL              len
              546  LOAD_FAST                'f2py_sources'
              548  CALL_FUNCTION_1       1  '1 positional argument'
              550  LOAD_CONST               1
              552  COMPARE_OP               !=
          554_556  POP_JUMP_IF_FALSE   572  'to 572'

 L. 532       558  LOAD_GLOBAL              DistutilsSetupError

 L. 533       560  LOAD_STR                 'only one .pyf file is allowed per extension module but got more: %r'

 L. 534       562  LOAD_FAST                'f2py_sources'
              564  BUILD_TUPLE_1         1 
              566  BINARY_MODULO    
              568  CALL_FUNCTION_1       1  '1 positional argument'
              570  RAISE_VARARGS_1       1  'exception instance'
            572_0  COME_FROM           554  '554'

 L. 535       572  LOAD_FAST                'f2py_sources'
              574  LOAD_CONST               0
              576  BINARY_SUBSCR    
              578  STORE_FAST               'source'

 L. 536       580  LOAD_FAST                'f2py_targets'
              582  LOAD_FAST                'source'
              584  BINARY_SUBSCR    
              586  STORE_FAST               'target_file'

 L. 537       588  LOAD_GLOBAL              os
              590  LOAD_ATTR                path
              592  LOAD_METHOD              dirname
              594  LOAD_FAST                'target_file'
              596  CALL_METHOD_1         1  '1 positional argument'
          598_600  JUMP_IF_TRUE_OR_POP   604  'to 604'
              602  LOAD_STR                 '.'
            604_0  COME_FROM           598  '598'
              604  STORE_FAST               'target_dir'

 L. 538       606  LOAD_FAST                'source'
              608  BUILD_LIST_1          1 
              610  LOAD_FAST                'extension'
              612  LOAD_ATTR                depends
              614  BINARY_ADD       
              616  STORE_FAST               'depends'

 L. 539       618  LOAD_FAST                'self'
              620  LOAD_ATTR                force
          622_624  POP_JUMP_IF_TRUE    640  'to 640'
              626  LOAD_GLOBAL              newer_group
              628  LOAD_FAST                'depends'
              630  LOAD_FAST                'target_file'
              632  LOAD_STR                 'newer'
              634  CALL_FUNCTION_3       3  '3 positional arguments'
          636_638  POP_JUMP_IF_FALSE   692  'to 692'
            640_0  COME_FROM           622  '622'

 L. 540       640  LOAD_FAST                'skip_f2py'
          642_644  POP_JUMP_IF_TRUE    692  'to 692'

 L. 541       646  LOAD_GLOBAL              log
              648  LOAD_METHOD              info
              650  LOAD_STR                 'f2py: %s'
              652  LOAD_FAST                'source'
              654  BINARY_MODULO    
              656  CALL_METHOD_1         1  '1 positional argument'
              658  POP_TOP          

 L. 542       660  LOAD_CONST               0
              662  LOAD_CONST               None
              664  IMPORT_NAME_ATTR         numpy.f2py
              666  STORE_FAST               'numpy'

 L. 543       668  LOAD_FAST                'numpy'
              670  LOAD_ATTR                f2py
              672  LOAD_METHOD              run_main
              674  LOAD_FAST                'f2py_options'

 L. 544       676  LOAD_STR                 '--build-dir'
              678  LOAD_FAST                'target_dir'
              680  LOAD_FAST                'source'
              682  BUILD_LIST_3          3 
              684  BINARY_ADD       
              686  CALL_METHOD_1         1  '1 positional argument'
              688  POP_TOP          
              690  JUMP_FORWARD        706  'to 706'
            692_0  COME_FROM           642  '642'
            692_1  COME_FROM           636  '636'

 L. 546       692  LOAD_GLOBAL              log
              694  LOAD_METHOD              debug
              696  LOAD_STR                 "  skipping '%s' f2py interface (up-to-date)"
              698  LOAD_FAST                'source'
              700  BINARY_MODULO    
              702  CALL_METHOD_1         1  '1 positional argument'
              704  POP_TOP          
            706_0  COME_FROM           690  '690'
              706  JUMP_FORWARD        916  'to 916'
            708_0  COME_FROM           540  '540'

 L. 549       708  LOAD_GLOBAL              is_sequence
              710  LOAD_FAST                'extension'
              712  CALL_FUNCTION_1       1  '1 positional argument'
          714_716  POP_JUMP_IF_FALSE   728  'to 728'

 L. 550       718  LOAD_FAST                'extension'
              720  LOAD_CONST               0
              722  BINARY_SUBSCR    
              724  STORE_FAST               'name'
              726  JUMP_FORWARD        734  'to 734'
            728_0  COME_FROM           714  '714'

 L. 551       728  LOAD_FAST                'extension'
              730  LOAD_ATTR                name
              732  STORE_FAST               'name'
            734_0  COME_FROM           726  '726'

 L. 552       734  LOAD_GLOBAL              os
              736  LOAD_ATTR                path
              738  LOAD_ATTR                join
              740  LOAD_FAST                'self'
              742  LOAD_ATTR                build_src
              744  BUILD_LIST_1          1 

 L. 553       746  LOAD_FAST                'name'
              748  LOAD_METHOD              split
              750  LOAD_STR                 '.'
              752  CALL_METHOD_1         1  '1 positional argument'
              754  LOAD_CONST               None
              756  LOAD_CONST               -1
              758  BUILD_SLICE_2         2 
              760  BINARY_SUBSCR    
              762  BINARY_ADD       
              764  CALL_FUNCTION_EX      0  'positional arguments only'
              766  STORE_FAST               'target_dir'

 L. 554       768  LOAD_GLOBAL              os
              770  LOAD_ATTR                path
              772  LOAD_METHOD              join
              774  LOAD_FAST                'target_dir'
              776  LOAD_FAST                'ext_name'
              778  LOAD_STR                 'module.c'
              780  BINARY_ADD       
              782  CALL_METHOD_2         2  '2 positional arguments'
              784  STORE_FAST               'target_file'

 L. 555       786  LOAD_FAST                'new_sources'
              788  LOAD_METHOD              append
              790  LOAD_FAST                'target_file'
              792  CALL_METHOD_1         1  '1 positional argument'
              794  POP_TOP          

 L. 556       796  LOAD_FAST                'f_sources'
              798  LOAD_FAST                'extension'
              800  LOAD_ATTR                depends
              802  BINARY_ADD       
              804  STORE_FAST               'depends'

 L. 557       806  LOAD_FAST                'self'
              808  LOAD_ATTR                force
          810_812  POP_JUMP_IF_TRUE    828  'to 828'
              814  LOAD_GLOBAL              newer_group
              816  LOAD_FAST                'depends'
              818  LOAD_FAST                'target_file'
              820  LOAD_STR                 'newer'
              822  CALL_FUNCTION_3       3  '3 positional arguments'
          824_826  POP_JUMP_IF_FALSE   902  'to 902'
            828_0  COME_FROM           810  '810'

 L. 558       828  LOAD_FAST                'skip_f2py'
          830_832  POP_JUMP_IF_TRUE    902  'to 902'

 L. 559       834  LOAD_GLOBAL              log
              836  LOAD_METHOD              info
              838  LOAD_STR                 'f2py:> %s'
              840  LOAD_FAST                'target_file'
              842  BINARY_MODULO    
              844  CALL_METHOD_1         1  '1 positional argument'
              846  POP_TOP          

 L. 560       848  LOAD_FAST                'self'
              850  LOAD_METHOD              mkpath
              852  LOAD_FAST                'target_dir'
              854  CALL_METHOD_1         1  '1 positional argument'
              856  POP_TOP          

 L. 561       858  LOAD_CONST               0
              860  LOAD_CONST               None
              862  IMPORT_NAME_ATTR         numpy.f2py
              864  STORE_FAST               'numpy'

 L. 562       866  LOAD_FAST                'numpy'
              868  LOAD_ATTR                f2py
              870  LOAD_METHOD              run_main

 L. 564       872  LOAD_FAST                'f2py_options'
              874  LOAD_STR                 '--lower'
              876  LOAD_STR                 '--build-dir'
              878  LOAD_FAST                'target_dir'
              880  BUILD_LIST_3          3 
              882  BINARY_ADD       
              884  LOAD_STR                 '-m'
              886  LOAD_FAST                'ext_name'
              888  BUILD_LIST_2          2 
              890  BINARY_ADD       
              892  LOAD_FAST                'f_sources'
              894  BINARY_ADD       
              896  CALL_METHOD_1         1  '1 positional argument'
              898  POP_TOP          
              900  JUMP_FORWARD        916  'to 916'
            902_0  COME_FROM           830  '830'
            902_1  COME_FROM           824  '824'

 L. 566       902  LOAD_GLOBAL              log
              904  LOAD_METHOD              debug
              906  LOAD_STR                 "  skipping f2py fortran files for '%s' (up-to-date)"

 L. 567       908  LOAD_FAST                'target_file'
              910  BINARY_MODULO    
              912  CALL_METHOD_1         1  '1 positional argument'
              914  POP_TOP          
            916_0  COME_FROM           900  '900'
            916_1  COME_FROM           706  '706'

 L. 569       916  LOAD_GLOBAL              os
              918  LOAD_ATTR                path
              920  LOAD_METHOD              isfile
              922  LOAD_FAST                'target_file'
              924  CALL_METHOD_1         1  '1 positional argument'
          926_928  POP_JUMP_IF_TRUE    944  'to 944'

 L. 570       930  LOAD_GLOBAL              DistutilsError
              932  LOAD_STR                 'f2py target file %r not generated'
              934  LOAD_FAST                'target_file'
              936  BUILD_TUPLE_1         1 
              938  BINARY_MODULO    
              940  CALL_FUNCTION_1       1  '1 positional argument'
              942  RAISE_VARARGS_1       1  'exception instance'
            944_0  COME_FROM           926  '926'

 L. 572       944  LOAD_GLOBAL              os
              946  LOAD_ATTR                path
              948  LOAD_METHOD              join
              950  LOAD_FAST                'self'
              952  LOAD_ATTR                build_src
              954  LOAD_FAST                'target_dir'
              956  CALL_METHOD_2         2  '2 positional arguments'
              958  STORE_FAST               'build_dir'

 L. 573       960  LOAD_GLOBAL              os
              962  LOAD_ATTR                path
              964  LOAD_METHOD              join
              966  LOAD_FAST                'build_dir'
              968  LOAD_STR                 'fortranobject.c'
              970  CALL_METHOD_2         2  '2 positional arguments'
              972  STORE_FAST               'target_c'

 L. 574       974  LOAD_GLOBAL              os
              976  LOAD_ATTR                path
              978  LOAD_METHOD              join
              980  LOAD_FAST                'build_dir'
              982  LOAD_STR                 'fortranobject.h'
              984  CALL_METHOD_2         2  '2 positional arguments'
              986  STORE_FAST               'target_h'

 L. 575       988  LOAD_GLOBAL              log
              990  LOAD_METHOD              info
              992  LOAD_STR                 "  adding '%s' to sources."
              994  LOAD_FAST                'target_c'
              996  BINARY_MODULO    
              998  CALL_METHOD_1         1  '1 positional argument'
             1000  POP_TOP          

 L. 576      1002  LOAD_FAST                'new_sources'
             1004  LOAD_METHOD              append
             1006  LOAD_FAST                'target_c'
             1008  CALL_METHOD_1         1  '1 positional argument'
             1010  POP_TOP          

 L. 577      1012  LOAD_FAST                'build_dir'
             1014  LOAD_FAST                'extension'
             1016  LOAD_ATTR                include_dirs
             1018  COMPARE_OP               not-in
         1020_1022  POP_JUMP_IF_FALSE  1050  'to 1050'

 L. 578      1024  LOAD_GLOBAL              log
             1026  LOAD_METHOD              info
             1028  LOAD_STR                 "  adding '%s' to include_dirs."
             1030  LOAD_FAST                'build_dir'
             1032  BINARY_MODULO    
             1034  CALL_METHOD_1         1  '1 positional argument'
             1036  POP_TOP          

 L. 579      1038  LOAD_FAST                'extension'
             1040  LOAD_ATTR                include_dirs
             1042  LOAD_METHOD              append
             1044  LOAD_FAST                'build_dir'
             1046  CALL_METHOD_1         1  '1 positional argument'
             1048  POP_TOP          
           1050_0  COME_FROM          1020  '1020'

 L. 581      1050  LOAD_FAST                'skip_f2py'
         1052_1054  POP_JUMP_IF_TRUE   1180  'to 1180'

 L. 582      1056  LOAD_CONST               0
             1058  LOAD_CONST               None
             1060  IMPORT_NAME_ATTR         numpy.f2py
             1062  STORE_FAST               'numpy'

 L. 583      1064  LOAD_GLOBAL              os
             1066  LOAD_ATTR                path
             1068  LOAD_METHOD              dirname
             1070  LOAD_FAST                'numpy'
             1072  LOAD_ATTR                f2py
             1074  LOAD_ATTR                __file__
             1076  CALL_METHOD_1         1  '1 positional argument'
             1078  STORE_FAST               'd'

 L. 584      1080  LOAD_GLOBAL              os
             1082  LOAD_ATTR                path
             1084  LOAD_METHOD              join
             1086  LOAD_FAST                'd'
             1088  LOAD_STR                 'src'
             1090  LOAD_STR                 'fortranobject.c'
             1092  CALL_METHOD_3         3  '3 positional arguments'
             1094  STORE_FAST               'source_c'

 L. 585      1096  LOAD_GLOBAL              os
             1098  LOAD_ATTR                path
             1100  LOAD_METHOD              join
             1102  LOAD_FAST                'd'
             1104  LOAD_STR                 'src'
             1106  LOAD_STR                 'fortranobject.h'
             1108  CALL_METHOD_3         3  '3 positional arguments'
             1110  STORE_FAST               'source_h'

 L. 586      1112  LOAD_GLOBAL              newer
             1114  LOAD_FAST                'source_c'
             1116  LOAD_FAST                'target_c'
             1118  CALL_FUNCTION_2       2  '2 positional arguments'
         1120_1122  POP_JUMP_IF_TRUE   1136  'to 1136'
             1124  LOAD_GLOBAL              newer
             1126  LOAD_FAST                'source_h'
             1128  LOAD_FAST                'target_h'
             1130  CALL_FUNCTION_2       2  '2 positional arguments'
         1132_1134  POP_JUMP_IF_FALSE  1236  'to 1236'
           1136_0  COME_FROM          1120  '1120'

 L. 587      1136  LOAD_FAST                'self'
             1138  LOAD_METHOD              mkpath
             1140  LOAD_GLOBAL              os
             1142  LOAD_ATTR                path
             1144  LOAD_METHOD              dirname
             1146  LOAD_FAST                'target_c'
             1148  CALL_METHOD_1         1  '1 positional argument'
             1150  CALL_METHOD_1         1  '1 positional argument'
             1152  POP_TOP          

 L. 588      1154  LOAD_FAST                'self'
             1156  LOAD_METHOD              copy_file
             1158  LOAD_FAST                'source_c'
             1160  LOAD_FAST                'target_c'
             1162  CALL_METHOD_2         2  '2 positional arguments'
             1164  POP_TOP          

 L. 589      1166  LOAD_FAST                'self'
             1168  LOAD_METHOD              copy_file
             1170  LOAD_FAST                'source_h'
             1172  LOAD_FAST                'target_h'
             1174  CALL_METHOD_2         2  '2 positional arguments'
             1176  POP_TOP          
             1178  JUMP_FORWARD       1236  'to 1236'
           1180_0  COME_FROM          1052  '1052'

 L. 591      1180  LOAD_GLOBAL              os
             1182  LOAD_ATTR                path
             1184  LOAD_METHOD              isfile
             1186  LOAD_FAST                'target_c'
             1188  CALL_METHOD_1         1  '1 positional argument'
         1190_1192  POP_JUMP_IF_TRUE   1208  'to 1208'

 L. 592      1194  LOAD_GLOBAL              DistutilsSetupError
             1196  LOAD_STR                 'f2py target_c file %r not found'
             1198  LOAD_FAST                'target_c'
             1200  BUILD_TUPLE_1         1 
             1202  BINARY_MODULO    
             1204  CALL_FUNCTION_1       1  '1 positional argument'
             1206  RAISE_VARARGS_1       1  'exception instance'
           1208_0  COME_FROM          1190  '1190'

 L. 593      1208  LOAD_GLOBAL              os
             1210  LOAD_ATTR                path
             1212  LOAD_METHOD              isfile
             1214  LOAD_FAST                'target_h'
             1216  CALL_METHOD_1         1  '1 positional argument'
         1218_1220  POP_JUMP_IF_TRUE   1236  'to 1236'

 L. 594      1222  LOAD_GLOBAL              DistutilsSetupError
             1224  LOAD_STR                 'f2py target_h file %r not found'
             1226  LOAD_FAST                'target_h'
             1228  BUILD_TUPLE_1         1 
             1230  BINARY_MODULO    
             1232  CALL_FUNCTION_1       1  '1 positional argument'
             1234  RAISE_VARARGS_1       1  'exception instance'
           1236_0  COME_FROM          1218  '1218'
           1236_1  COME_FROM          1178  '1178'
           1236_2  COME_FROM          1132  '1132'

 L. 596      1236  SETUP_LOOP         1308  'to 1308'
             1238  LOAD_CONST               ('-f2pywrappers.f', '-f2pywrappers2.f90')
             1240  GET_ITER         
           1242_0  COME_FROM          1302  '1302'
           1242_1  COME_FROM          1274  '1274'
             1242  FOR_ITER           1306  'to 1306'
             1244  STORE_FAST               'name_ext'

 L. 597      1246  LOAD_GLOBAL              os
             1248  LOAD_ATTR                path
             1250  LOAD_METHOD              join
             1252  LOAD_FAST                'target_dir'
             1254  LOAD_FAST                'ext_name'
             1256  LOAD_FAST                'name_ext'
             1258  BINARY_ADD       
             1260  CALL_METHOD_2         2  '2 positional arguments'
             1262  STORE_FAST               'filename'

 L. 598      1264  LOAD_GLOBAL              os
             1266  LOAD_ATTR                path
             1268  LOAD_METHOD              isfile
             1270  LOAD_FAST                'filename'
             1272  CALL_METHOD_1         1  '1 positional argument'
         1274_1276  POP_JUMP_IF_FALSE_BACK  1242  'to 1242'

 L. 599      1278  LOAD_GLOBAL              log
             1280  LOAD_METHOD              info
             1282  LOAD_STR                 "  adding '%s' to sources."
             1284  LOAD_FAST                'filename'
             1286  BINARY_MODULO    
             1288  CALL_METHOD_1         1  '1 positional argument'
             1290  POP_TOP          

 L. 600      1292  LOAD_FAST                'f_sources'
             1294  LOAD_METHOD              append
             1296  LOAD_FAST                'filename'
             1298  CALL_METHOD_1         1  '1 positional argument'
             1300  POP_TOP          
         1302_1304  JUMP_BACK          1242  'to 1242'
             1306  POP_BLOCK        
           1308_0  COME_FROM_LOOP     1236  '1236'

 L. 602      1308  LOAD_FAST                'new_sources'
             1310  LOAD_FAST                'f_sources'
             1312  BINARY_ADD       
             1314  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 706

    def swig_sources(self, sources, extension):
        new_sources = []
        swig_sources = []
        swig_targets = {}
        target_dirs = []
        py_files = []
        target_ext = '.c'
        if '-c++' in extension.swig_opts:
            typ = 'c++'
            is_cpp = True
            extension.swig_opts.remove('-c++')
        elif self.swig_cpp:
            typ = 'c++'
            is_cpp = True
        else:
            typ = None
            is_cpp = False
        skip_swig = 0
        ext_name = extension.name.split('.')[(-1)]
        for source in sources:
            base, ext = os.path.splitext(source)
            if ext == '.i':
                if self.inplace:
                    target_dir = os.path.dirname(base)
                    py_target_dir = self.ext_target_dir
                else:
                    target_dir = appendpath(self.build_src, os.path.dirname(base))
                    py_target_dir = target_dir
                if os.path.isfile(source):
                    name = get_swig_modulename(source)
                    if name != ext_name[1:]:
                        raise DistutilsSetupError('mismatch of extension names: %s provides %r but expected %r' % (
                         source, name, ext_name[1:]))
                    if typ is None:
                        typ = get_swig_target(source)
                        is_cpp = typ == 'c++'
                    else:
                        typ2 = get_swig_target(source)
                        if typ2 is None:
                            log.warn('source %r does not define swig target, assuming %s swig target' % (
                             source, typ))
                        elif typ != typ2:
                            log.warn('expected %r but source %r defines %r swig target' % (
                             typ, source, typ2))
                            if typ2 == 'c++':
                                log.warn('resetting swig target to c++ (some targets may have .c extension)')
                                is_cpp = True
                            else:
                                log.warn('assuming that %r has c++ swig target' % source)
                    if is_cpp:
                        target_ext = '.cpp'
                    target_file = os.path.join(target_dir, '%s_wrap%s' % (
                     name, target_ext))
                else:
                    log.warn("  source %s does not exist: skipping swig'ing." % source)
                    name = ext_name[1:]
                    skip_swig = 1
                    target_file = _find_swig_target(target_dir, name)
                    if not os.path.isfile(target_file):
                        log.warn('  target %s does not exist:\n   Assuming %s_wrap.{c,cpp} was generated with "build_src --inplace" command.' % (
                         target_file, name))
                        target_dir = os.path.dirname(base)
                        target_file = _find_swig_target(target_dir, name)
                        if not os.path.isfile(target_file):
                            raise DistutilsSetupError('%r missing' % (target_file,))
                        log.warn('   Yes! Using %r as up-to-date target.' % target_file)
                    target_dirs.append(target_dir)
                    new_sources.append(target_file)
                    py_files.append(os.path.join(py_target_dir, name + '.py'))
                    swig_sources.append(source)
                    swig_targets[source] = new_sources[(-1)]
            else:
                new_sources.append(source)

        if not swig_sources:
            return new_sources
        if skip_swig:
            return new_sources + py_files
        for d in target_dirs:
            self.mkpath(d)

        swig = self.swig or self.find_swig()
        swig_cmd = [swig, '-python'] + extension.swig_opts
        if is_cpp:
            swig_cmd.append('-c++')
        for d in extension.include_dirs:
            swig_cmd.append('-I' + d)

        for source in swig_sources:
            target = swig_targets[source]
            depends = [source] + extension.depends
            if not self.force or newer_group(depends, target, 'newer'):
                log.info('%s: %s' % (
                 os.path.basename(swig) + is_cpp and '++' or '', source))
                self.spawn(swig_cmd + self.swig_opts + ['-o', target, '-outdir', py_target_dir, source])
            else:
                log.debug("  skipping '%s' swig interface (up-to-date)" % source)

        return new_sources + py_files


_f_pyf_ext_match = re.compile('.*[.](f90|f95|f77|for|ftn|f|pyf)\\Z', re.I).match
_header_ext_match = re.compile('.*[.](inc|h|hpp)\\Z', re.I).match
_swig_module_name_match = re.compile('\\s*%module\\s*(.*\\(\\s*package\\s*=\\s*"(?P<package>[\\w_]+)".*\\)|)\\s*(?P<name>[\\w_]+)', re.I).match
_has_c_header = re.compile('-[*]-\\s*c\\s*-[*]-', re.I).search
_has_cpp_header = re.compile('-[*]-\\s*c[+][+]\\s*-[*]-', re.I).search

def get_swig_target(source):
    with open(source, 'r') as f:
        result = None
        line = f.readline()
        if _has_cpp_header(line):
            result = 'c++'
        if _has_c_header(line):
            result = 'c'
    return result


def get_swig_modulename(source):
    with open(source, 'r') as f:
        name = None
        for line in f:
            m = _swig_module_name_match(line)
            if m:
                name = m.group('name')
                break

    return name


def _find_swig_target(target_dir, name):
    for ext in ('.cpp', '.c'):
        target = os.path.join(target_dir, '%s_wrap%s' % (name, ext))
        if os.path.isfile(target):
            break

    return target


_f2py_module_name_match = re.compile('\\s*python\\s*module\\s*(?P<name>[\\w_]+)', re.I).match
_f2py_user_module_name_match = re.compile('\\s*python\\s*module\\s*(?P<name>[\\w_]*?__user__[\\w_]*)', re.I).match

def get_f2py_modulename(source):
    name = None
    with open(source) as f:
        for line in f:
            m = _f2py_module_name_match(line)
            if m:
                if _f2py_user_module_name_match(line):
                    continue
                else:
                    name = m.group('name')
                break

    return name