# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: numpy\distutils\system_info.py
"""
This file defines a set of system_info classes for getting
information about various resources (libraries, library directories,
include directories, etc.) in the system. Usage:
    info_dict = get_info(<name>)
  where <name> is a string 'atlas','x11','fftw','lapack','blas',
  'lapack_src', 'blas_src', etc. For a complete list of allowed names,
  see the definition of get_info() function below.

  Returned info_dict is a dictionary which is compatible with
  distutils.setup keyword arguments. If info_dict == {}, then the
  asked resource is not available (system_info could not find it).

  Several *_info classes specify an environment variable to specify
  the locations of software. When setting the corresponding environment
  variable to 'None' then the software will be ignored, even when it
  is available in system.

Global parameters:
  system_info.search_static_first - search static libraries (.a)
             in precedence to shared ones (.so, .sl) if enabled.
  system_info.verbosity - output the results to stdout if enabled.

The file 'site.cfg' is looked for in

1) Directory of main setup.py file being run.
2) Home directory of user running the setup.py file as ~/.numpy-site.cfg
3) System wide directory (location of this file...)

The first one found is used to get system configuration options The
format is that used by ConfigParser (i.e., Windows .INI style). The
section ALL is not intended for general use.

Appropriate defaults are used if nothing is specified.

The order of finding the locations of resources is the following:
 1. environment variable
 2. section in site.cfg
 3. DEFAULT section in site.cfg
 4. System default search paths (see ``default_*`` variables below).
Only the first complete match is returned.

Currently, the following classes are available, along with their section names:

    Numeric_info:Numeric
    _numpy_info:Numeric
    _pkg_config_info:None
    accelerate_info:accelerate
    agg2_info:agg2
    amd_info:amd
    atlas_3_10_blas_info:atlas
    atlas_3_10_blas_threads_info:atlas
    atlas_3_10_info:atlas
    atlas_3_10_threads_info:atlas
    atlas_blas_info:atlas
    atlas_blas_threads_info:atlas
    atlas_info:atlas
    atlas_threads_info:atlas
    blas64__opt_info:ALL               # usage recommended (general ILP64 BLAS, 64_ symbol suffix)
    blas_ilp64_opt_info:ALL            # usage recommended (general ILP64 BLAS)
    blas_ilp64_plain_opt_info:ALL      # usage recommended (general ILP64 BLAS, no symbol suffix)
    blas_info:blas
    blas_mkl_info:mkl
    blas_opt_info:ALL                  # usage recommended
    blas_src_info:blas_src
    blis_info:blis
    boost_python_info:boost_python
    dfftw_info:fftw
    dfftw_threads_info:fftw
    djbfft_info:djbfft
    f2py_info:ALL
    fft_opt_info:ALL
    fftw2_info:fftw
    fftw3_info:fftw3
    fftw_info:fftw
    fftw_threads_info:fftw
    flame_info:flame
    freetype2_info:freetype2
    gdk_2_info:gdk_2
    gdk_info:gdk
    gdk_pixbuf_2_info:gdk_pixbuf_2
    gdk_pixbuf_xlib_2_info:gdk_pixbuf_xlib_2
    gdk_x11_2_info:gdk_x11_2
    gtkp_2_info:gtkp_2
    gtkp_x11_2_info:gtkp_x11_2
    lapack64__opt_info:ALL             # usage recommended (general ILP64 LAPACK, 64_ symbol suffix)
    lapack_atlas_3_10_info:atlas
    lapack_atlas_3_10_threads_info:atlas
    lapack_atlas_info:atlas
    lapack_atlas_threads_info:atlas
    lapack_ilp64_opt_info:ALL          # usage recommended (general ILP64 LAPACK)
    lapack_ilp64_plain_opt_info:ALL    # usage recommended (general ILP64 LAPACK, no symbol suffix)
    lapack_info:lapack
    lapack_mkl_info:mkl
    lapack_opt_info:ALL                # usage recommended
    lapack_src_info:lapack_src
    mkl_info:mkl
    numarray_info:numarray
    numerix_info:numerix
    numpy_info:numpy
    openblas64__info:openblas64_
    openblas64__lapack_info:openblas64_
    openblas_clapack_info:openblas
    openblas_ilp64_info:openblas_ilp64
    openblas_ilp64_lapack_info:openblas_ilp64
    openblas_info:openblas
    openblas_lapack_info:openblas
    sfftw_info:fftw
    sfftw_threads_info:fftw
    system_info:ALL
    umfpack_info:umfpack
    wx_info:wx
    x11_info:x11
    xft_info:xft

Example:
----------
[DEFAULT]
# default section
library_dirs = /usr/lib:/usr/local/lib:/opt/lib
include_dirs = /usr/include:/usr/local/include:/opt/include
src_dirs = /usr/local/src:/opt/src
# search static libraries (.a) in preference to shared ones (.so)
search_static_first = 0

[fftw]
libraries = rfftw, fftw

[atlas]
library_dirs = /usr/lib/3dnow:/usr/lib/3dnow/atlas
# for overriding the names of the atlas libraries
libraries = lapack, f77blas, cblas, atlas

[x11]
library_dirs = /usr/X11R6/lib
include_dirs = /usr/X11R6/include
----------

Note that the ``libraries`` key is the default setting for libraries.

Authors:
  Pearu Peterson <pearu@cens.ioc.ee>, February 2002
  David M. Cooke <cookedm@physics.mcmaster.ca>, April 2002

Copyright 2002 Pearu Peterson all rights reserved,
Pearu Peterson <pearu@cens.ioc.ee>
Permission to use, modify, and distribute this software is given under the
terms of the NumPy (BSD style) license.  See LICENSE.txt that came with
this distribution for specifics.

NO WARRANTY IS EXPRESSED OR IMPLIED.  USE AT YOUR OWN RISK.

"""
import sys, os, re, copy, warnings, subprocess, textwrap
from glob import glob
from functools import reduce
from configparser import NoOptionError
from configparser import RawConfigParser as ConfigParser
from distutils.errors import DistutilsError
from distutils.dist import Distribution
import sysconfig
from numpy.distutils import log
from distutils.util import get_platform
from numpy.distutils.exec_command import find_executable, filepath_from_subprocess_output
from numpy.distutils.misc_util import is_sequence, is_string, get_shared_lib_extension
import numpy.distutils.command.config as cmd_config
import numpy.distutils as _customized_ccompiler
from numpy.distutils import _shell_utils
import distutils.ccompiler, tempfile, shutil
__all__ = [
 'system_info']
import platform
_bits = {'32bit':32, 
 '64bit':64}
platform_bits = _bits[platform.architecture()[0]]
global_compiler = None

def customized_ccompiler():
    global global_compiler
    if not global_compiler:
        global_compiler = _customized_ccompiler()
    return global_compiler


def _c_string_literal(s):
    """
    Convert a python string into a literal suitable for inclusion into C code
    """
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    s = s.replace('\n', '\\n')
    return '"{}"'.format(s)


def libpaths(paths, bits):
    """Return a list of library paths valid on 32 or 64 bit systems.

    Inputs:
      paths : sequence
        A sequence of strings (typically paths)
      bits : int
        An integer, the only valid values are 32 or 64.  A ValueError exception
      is raised otherwise.

    Examples:

    Consider a list of directories
    >>> paths = ['/usr/X11R6/lib','/usr/X11/lib','/usr/lib']

    For a 32-bit platform, this is already valid:
    >>> np.distutils.system_info.libpaths(paths,32)
    ['/usr/X11R6/lib', '/usr/X11/lib', '/usr/lib']

    On 64 bits, we prepend the '64' postfix
    >>> np.distutils.system_info.libpaths(paths,64)
    ['/usr/X11R6/lib64', '/usr/X11R6/lib', '/usr/X11/lib64', '/usr/X11/lib',
    '/usr/lib64', '/usr/lib']
    """
    if bits not in (32, 64):
        raise ValueError('Invalid bit size in libpaths: 32 or 64 only')
    if bits == 32:
        return paths
    out = []
    for p in paths:
        out.extend([p + '64', p])

    return out


if sys.platform == 'win32':
    default_lib_dirs = [
     'C:\\',
     os.path.join(sysconfig.get_config_var('exec_prefix'), 'libs')]
    default_runtime_dirs = []
    default_include_dirs = []
    default_src_dirs = ['.']
    default_x11_lib_dirs = []
    default_x11_include_dirs = []
    _include_dirs = [
     'include',
     'include/suitesparse']
    _lib_dirs = [
     'lib']
    _include_dirs = [d.replace('/', os.sep) for d in _include_dirs]
    _lib_dirs = [d.replace('/', os.sep) for d in _lib_dirs]

    def add_system_root(library_root):
        """Add a package manager root to the include directories"""
        global default_include_dirs
        global default_lib_dirs
        library_root = os.path.normpath(library_root)
        default_lib_dirs.extend((os.path.join(library_root, d) for d in _lib_dirs))
        default_include_dirs.extend((os.path.join(library_root, d) for d in _include_dirs))


    vcpkg = shutil.which('vcpkg')
    if vcpkg:
        vcpkg_dir = os.path.dirname(vcpkg)
        if platform.architecture()[0] == '32bit':
            specifier = 'x86'
        else:
            specifier = 'x64'
        vcpkg_installed = os.path.join(vcpkg_dir, 'installed')
        for vcpkg_root in [
         os.path.join(vcpkg_installed, specifier + '-windows'),
         os.path.join(vcpkg_installed, specifier + '-windows-static')]:
            add_system_root(vcpkg_root)

    conda = shutil.which('conda')
    if conda:
        conda_dir = os.path.dirname(conda)
        add_system_root(os.path.join(conda_dir, '..', 'Library'))
        add_system_root(os.path.join(conda_dir, 'Library'))
else:
    default_lib_dirs = libpaths(['/usr/local/lib', '/opt/lib', '/usr/lib',
     '/opt/local/lib', '/sw/lib'], platform_bits)
    default_runtime_dirs = []
    default_include_dirs = ['/usr/local/include',
     '/opt/include', '/usr/include',
     '/opt/local/include/ufsparse',
     '/opt/local/include', '/sw/include',
     '/usr/include/suitesparse']
    default_src_dirs = ['.', '/usr/local/src', '/opt/src', '/sw/src']
    default_x11_lib_dirs = libpaths(['/usr/X11R6/lib', '/usr/X11/lib',
     '/usr/lib'], platform_bits)
    default_x11_include_dirs = ['/usr/X11R6/include', '/usr/X11/include',
     '/usr/include']
    if os.path.exists('/usr/lib/X11'):
        globbed_x11_dir = glob('/usr/lib/*/libX11.so')
        if globbed_x11_dir:
            x11_so_dir = os.path.split(globbed_x11_dir[0])[0]
            default_x11_lib_dirs.extend([x11_so_dir, '/usr/lib/X11'])
            default_x11_include_dirs.extend(['/usr/lib/X11/include',
             '/usr/include/X11'])
    with open(os.devnull, 'w') as (tmp):
        try:
            p = subprocess.Popen(['gcc', '-print-multiarch'], stdout=(subprocess.PIPE), stderr=tmp)
        except (OSError, DistutilsError):
            pass
        else:
            triplet = str(p.communicate()[0].decode().strip())
            if p.returncode == 0:
                default_x11_lib_dirs += [os.path.join('/usr/lib/', triplet)]
                default_lib_dirs += [os.path.join('/usr/lib/', triplet)]
if os.path.join(sys.prefix, 'lib') not in default_lib_dirs:
    default_lib_dirs.insert(0, os.path.join(sys.prefix, 'lib'))
    default_include_dirs.append(os.path.join(sys.prefix, 'include'))
    default_src_dirs.append(os.path.join(sys.prefix, 'src'))
default_lib_dirs = [_m for _m in default_lib_dirs if os.path.isdir(_m)]
default_runtime_dirs = [_m for _m in default_runtime_dirs if os.path.isdir(_m)]
default_include_dirs = [_m for _m in default_include_dirs if os.path.isdir(_m)]
default_src_dirs = [_m for _m in default_src_dirs if os.path.isdir(_m)]
so_ext = get_shared_lib_extension()

def is_symlink_to_accelerate(filename):
    accelpath = '/System/Library/Frameworks/Accelerate.framework'
    return sys.platform == 'darwin' and os.path.islink(filename) and os.path.realpath(filename).startswith(accelpath)


_accel_msg = 'Found {filename}, but that file is a symbolic link to the MacOS Accelerate framework, which is not supported by NumPy. You must configure the build to use a different optimized library, or disable the use of optimized BLAS and LAPACK by setting the environment variables NPY_BLAS_ORDER="" and NPY_LAPACK_ORDER="" before building NumPy.'

def get_standard_file(fname):
    """Returns a list of files named 'fname' from
    1) System-wide directory (directory-location of this module)
    2) Users HOME directory (os.environ['HOME'])
    3) Local directory
    """
    filenames = []
    try:
        f = __file__
    except NameError:
        f = sys.argv[0]
    else:
        sysfile = os.path.join(os.path.split(os.path.abspath(f))[0], fname)
        if os.path.isfile(sysfile):
            filenames.append(sysfile)
        else:
            try:
                f = os.path.expanduser('~')
            except KeyError:
                pass
            else:
                user_file = os.path.join(f, fname)
                if os.path.isfile(user_file):
                    filenames.append(user_file)
        if os.path.isfile(fname):
            filenames.append(os.path.abspath(fname))
        return filenames


def _parse_env_order(base_order, env):
    """ Parse an environment variable `env` by splitting with "," and only returning elements from `base_order`

    This method will sequence the environment variable and check for their invidual elements in `base_order`.

    The items in the environment variable may be negated via '^item' or '!itema,itemb'.
    It must start with ^/! to negate all options.

    Raises
    ------
    ValueError: for mixed negated and non-negated orders or multiple negated orders

    Parameters
    ----------
    base_order : list of str
       the base list of orders
    env : str
       the environment variable to be parsed, if none is found, `base_order` is returned

    Returns
    -------
    allow_order : list of str
        allowed orders in lower-case
    unknown_order : list of str
        for values not overlapping with `base_order`
    """
    order_str = os.environ.get(env, None)
    base_order = [order.lower() for order in base_order]
    if order_str is None:
        return (
         base_order, [])
    else:
        neg = order_str.startswith('^') or order_str.startswith('!')
        order_str_l = list(order_str)
        sum_neg = order_str_l.count('^') + order_str_l.count('!')
        if neg:
            if sum_neg > 1:
                raise ValueError(f"Environment variable '{env}' may only contain a single (prefixed) negation: {order_str}")
            order_str = order_str[1:]
        else:
            if sum_neg > 0:
                raise ValueError(f"Environment variable '{env}' may not mix negated an non-negated items: {order_str}")
    orders = order_str.lower().split(',')
    unknown_order = []
    if neg:
        allow_order = base_order.copy()
        for order in orders:
            if not order:
                continue
            if order not in base_order:
                unknown_order.append(order)
                continue
            if order in allow_order:
                allow_order.remove(order)

    else:
        allow_order = []
        for order in orders:
            if not order:
                continue
            if order not in base_order:
                unknown_order.append(order)
                continue
            if order not in allow_order:
                allow_order.append(order)

    return (
     allow_order, unknown_order)


def get_info(name, notfound_action=0):
    """
    notfound_action:
      0 - do nothing
      1 - display warning message
      2 - raise error
    """
    cl = {'atlas':atlas_info, 
     'atlas_threads':atlas_threads_info, 
     'atlas_blas':atlas_blas_info, 
     'atlas_blas_threads':atlas_blas_threads_info, 
     'lapack_atlas':lapack_atlas_info, 
     'lapack_atlas_threads':lapack_atlas_threads_info, 
     'atlas_3_10':atlas_3_10_info, 
     'atlas_3_10_threads':atlas_3_10_threads_info, 
     'atlas_3_10_blas':atlas_3_10_blas_info, 
     'atlas_3_10_blas_threads':atlas_3_10_blas_threads_info, 
     'lapack_atlas_3_10':lapack_atlas_3_10_info, 
     'lapack_atlas_3_10_threads':lapack_atlas_3_10_threads_info, 
     'flame':flame_info, 
     'mkl':mkl_info, 
     'openblas':openblas_info, 
     'openblas_lapack':openblas_lapack_info, 
     'openblas_clapack':openblas_clapack_info, 
     'blis':blis_info, 
     'lapack_mkl':lapack_mkl_info, 
     'blas_mkl':blas_mkl_info, 
     'openblas64_':openblas64__info, 
     'openblas64__lapack':openblas64__lapack_info, 
     'openblas_ilp64':openblas_ilp64_info, 
     'openblas_ilp64_lapack':openblas_ilp64_lapack_info, 
     'x11':x11_info, 
     'fft_opt':fft_opt_info, 
     'fftw':fftw_info, 
     'fftw2':fftw2_info, 
     'fftw3':fftw3_info, 
     'dfftw':dfftw_info, 
     'sfftw':sfftw_info, 
     'fftw_threads':fftw_threads_info, 
     'dfftw_threads':dfftw_threads_info, 
     'sfftw_threads':sfftw_threads_info, 
     'djbfft':djbfft_info, 
     'blas':blas_info, 
     'lapack':lapack_info, 
     'lapack_src':lapack_src_info, 
     'blas_src':blas_src_info, 
     'numpy':numpy_info, 
     'f2py':f2py_info, 
     'Numeric':Numeric_info, 
     'numeric':Numeric_info, 
     'numarray':numarray_info, 
     'numerix':numerix_info, 
     'lapack_opt':lapack_opt_info, 
     'lapack_ilp64_opt':lapack_ilp64_opt_info, 
     'lapack_ilp64_plain_opt':lapack_ilp64_plain_opt_info, 
     'lapack64__opt':lapack64__opt_info, 
     'blas_opt':blas_opt_info, 
     'blas_ilp64_opt':blas_ilp64_opt_info, 
     'blas_ilp64_plain_opt':blas_ilp64_plain_opt_info, 
     'blas64__opt':blas64__opt_info, 
     'boost_python':boost_python_info, 
     'agg2':agg2_info, 
     'wx':wx_info, 
     'gdk_pixbuf_xlib_2':gdk_pixbuf_xlib_2_info, 
     'gdk-pixbuf-xlib-2.0':gdk_pixbuf_xlib_2_info, 
     'gdk_pixbuf_2':gdk_pixbuf_2_info, 
     'gdk-pixbuf-2.0':gdk_pixbuf_2_info, 
     'gdk':gdk_info, 
     'gdk_2':gdk_2_info, 
     'gdk-2.0':gdk_2_info, 
     'gdk_x11_2':gdk_x11_2_info, 
     'gdk-x11-2.0':gdk_x11_2_info, 
     'gtkp_x11_2':gtkp_x11_2_info, 
     'gtk+-x11-2.0':gtkp_x11_2_info, 
     'gtkp_2':gtkp_2_info, 
     'gtk+-2.0':gtkp_2_info, 
     'xft':xft_info, 
     'freetype2':freetype2_info, 
     'umfpack':umfpack_info, 
     'amd':amd_info}.get(name.lower(), system_info)
    return cl().get_info(notfound_action)


class NotFoundError(DistutilsError):
    __doc__ = 'Some third-party program or library is not found.'


class AliasedOptionError(DistutilsError):
    __doc__ = "\n    Aliases entries in config files should not be existing.\n    In section '{section}' we found multiple appearances of options {options}."


class AtlasNotFoundError(NotFoundError):
    __doc__ = '\n    Atlas (http://github.com/math-atlas/math-atlas) libraries not found.\n    Directories to search for the libraries can be specified in the\n    numpy/distutils/site.cfg file (section [atlas]) or by setting\n    the ATLAS environment variable.'


class FlameNotFoundError(NotFoundError):
    __doc__ = '\n    FLAME (http://www.cs.utexas.edu/~flame/web/) libraries not found.\n    Directories to search for the libraries can be specified in the\n    numpy/distutils/site.cfg file (section [flame]).'


class LapackNotFoundError(NotFoundError):
    __doc__ = '\n    Lapack (http://www.netlib.org/lapack/) libraries not found.\n    Directories to search for the libraries can be specified in the\n    numpy/distutils/site.cfg file (section [lapack]) or by setting\n    the LAPACK environment variable.'


class LapackSrcNotFoundError(LapackNotFoundError):
    __doc__ = '\n    Lapack (http://www.netlib.org/lapack/) sources not found.\n    Directories to search for the sources can be specified in the\n    numpy/distutils/site.cfg file (section [lapack_src]) or by setting\n    the LAPACK_SRC environment variable.'


class LapackILP64NotFoundError(NotFoundError):
    __doc__ = '\n    64-bit Lapack libraries not found.\n    Known libraries in numpy/distutils/site.cfg file are:\n    openblas64_, openblas_ilp64\n    '


class BlasOptNotFoundError(NotFoundError):
    __doc__ = '\n    Optimized (vendor) Blas libraries are not found.\n    Falls back to netlib Blas library which has worse performance.\n    A better performance should be easily gained by switching\n    Blas library.'


class BlasNotFoundError(NotFoundError):
    __doc__ = '\n    Blas (http://www.netlib.org/blas/) libraries not found.\n    Directories to search for the libraries can be specified in the\n    numpy/distutils/site.cfg file (section [blas]) or by setting\n    the BLAS environment variable.'


class BlasILP64NotFoundError(NotFoundError):
    __doc__ = '\n    64-bit Blas libraries not found.\n    Known libraries in numpy/distutils/site.cfg file are:\n    openblas64_, openblas_ilp64\n    '


class BlasSrcNotFoundError(BlasNotFoundError):
    __doc__ = '\n    Blas (http://www.netlib.org/blas/) sources not found.\n    Directories to search for the sources can be specified in the\n    numpy/distutils/site.cfg file (section [blas_src]) or by setting\n    the BLAS_SRC environment variable.'


class FFTWNotFoundError(NotFoundError):
    __doc__ = '\n    FFTW (http://www.fftw.org/) libraries not found.\n    Directories to search for the libraries can be specified in the\n    numpy/distutils/site.cfg file (section [fftw]) or by setting\n    the FFTW environment variable.'


class DJBFFTNotFoundError(NotFoundError):
    __doc__ = '\n    DJBFFT (https://cr.yp.to/djbfft.html) libraries not found.\n    Directories to search for the libraries can be specified in the\n    numpy/distutils/site.cfg file (section [djbfft]) or by setting\n    the DJBFFT environment variable.'


class NumericNotFoundError(NotFoundError):
    __doc__ = '\n    Numeric (https://www.numpy.org/) module not found.\n    Get it from above location, install it, and retry setup.py.'


class X11NotFoundError(NotFoundError):
    __doc__ = 'X11 libraries not found.'


class UmfpackNotFoundError(NotFoundError):
    __doc__ = '\n    UMFPACK sparse solver (https://www.cise.ufl.edu/research/sparse/umfpack/)\n    not found. Directories to search for the libraries can be specified in the\n    numpy/distutils/site.cfg file (section [umfpack]) or by setting\n    the UMFPACK environment variable.'


class system_info:
    __doc__ = " get_info() is the only public method. Don't use others.\n    "
    dir_env_var = None
    search_static_first = 0
    section = 'ALL'
    saved_results = {}
    notfounderror = NotFoundError

    def __init__(self, default_lib_dirs=default_lib_dirs, default_include_dirs=default_include_dirs):
        self.__class__.info = {}
        self.local_prefixes = []
        defaults = {'library_dirs':os.pathsep.join(default_lib_dirs), 
         'include_dirs':os.pathsep.join(default_include_dirs), 
         'runtime_library_dirs':os.pathsep.join(default_runtime_dirs), 
         'rpath':'', 
         'src_dirs':os.pathsep.join(default_src_dirs), 
         'search_static_first':str(self.search_static_first), 
         'extra_compile_args':'', 
         'extra_link_args':''}
        self.cp = ConfigParser(defaults)
        self.files = []
        self.files.extend(get_standard_file('.numpy-site.cfg'))
        self.files.extend(get_standard_file('site.cfg'))
        self.parse_config_files()
        if self.section is not None:
            self.search_static_first = self.cp.getboolean(self.section, 'search_static_first')
        assert isinstance(self.search_static_first, int)

    def parse_config_files(self):
        self.cp.read(self.files)
        if not self.cp.has_section(self.section):
            if self.section is not None:
                self.cp.add_section(self.section)

    def calc_libraries_info(self):
        libs = self.get_libraries()
        dirs = self.get_lib_dirs()
        r_dirs = self.get_runtime_lib_dirs()
        r_dirs.extend(self.get_runtime_lib_dirs(key='rpath'))
        info = {}
        for lib in libs:
            i = self.check_libs(dirs, [lib])
            if i is not None:
                dict_append(info, **i)
            else:
                log.info('Library %s was not found. Ignoring' % lib)
            if r_dirs:
                i = self.check_libs(r_dirs, [lib])
                if i is not None:
                    del i['libraries']
                    i['runtime_library_dirs'] = i.pop('library_dirs')
                    dict_append(info, **i)
                else:
                    log.info('Runtime library %s was not found. Ignoring' % lib)

        return info

    def set_info(self, **info):
        if info:
            lib_info = self.calc_libraries_info()
            dict_append(info, **lib_info)
            extra_info = self.calc_extra_info()
            dict_append(info, **extra_info)
        self.saved_results[self.__class__.__name__] = info

    def get_option_single(self, *options):
        """ Ensure that only one of `options` are found in the section

        Parameters
        ----------
        *options : list of str
           a list of options to be found in the section (``self.section``)

        Returns
        -------
        str :
            the option that is uniquely found in the section

        Raises
        ------
        AliasedOptionError :
            in case more than one of the options are found
        """
        found = [self.cp.has_option(self.section, opt) for opt in options]
        if sum(found) == 1:
            return options[found.index(True)]
        if sum(found) == 0:
            return options[0]
        if AliasedOptionError.__doc__ is None:
            raise AliasedOptionError()
        raise AliasedOptionError(AliasedOptionError.__doc__.format(section=(self.section),
          options=('[{}]'.format(', '.join(options)))))

    def has_info(self):
        return self.__class__.__name__ in self.saved_results

    def calc_extra_info(self):
        """ Updates the information in the current information with
        respect to these flags:
          extra_compile_args
          extra_link_args
        """
        info = {}
        for key in ('extra_compile_args', 'extra_link_args'):
            opt = self.cp.get(self.section, key)
            opt = _shell_utils.NativeParser.split(opt)
            if opt:
                tmp = {key: opt}
                dict_append(info, **tmp)

        return info

    def get_info(self, notfound_action=0):
        """ Return a dictionary with items that are compatible
            with numpy.distutils.setup keyword arguments.
        """
        flag = 0
        if not self.has_info():
            flag = 1
            log.info(self.__class__.__name__ + ':')
            if hasattr(self, 'calc_info'):
                self.calc_info()
            else:
                if notfound_action:
                    if not self.has_info():
                        if notfound_action == 1:
                            warnings.warn((self.notfounderror.__doc__), stacklevel=2)
                        else:
                            if notfound_action == 2:
                                raise self.notfounderror(self.notfounderror.__doc__)
                            else:
                                raise ValueError(repr(notfound_action))
                if not self.has_info():
                    log.info('  NOT AVAILABLE')
                    self.set_info()
                else:
                    log.info('  FOUND:')
        res = self.saved_results.get(self.__class__.__name__)
        if log.get_threshold() <= log.INFO:
            if flag:
                for k, v in res.items():
                    v = str(v)
                    if k in ('sources', 'libraries'):
                        if len(v) > 270:
                            v = v[:120] + '...\n...\n...' + v[-120:]
                    log.info('    %s = %s', k, v)

                log.info('')
        return copy.deepcopy(res)

    def get_paths(self, section, key):
        dirs = self.cp.get(section, key).split(os.pathsep)
        env_var = self.dir_env_var
        if env_var:
            if is_sequence(env_var):
                e0 = env_var[(-1)]
                for e in env_var:
                    if e in os.environ:
                        e0 = e
                        break

                if not env_var[0] == e0:
                    log.info('Setting %s=%s' % (env_var[0], e0))
                env_var = e0
        elif env_var:
            if env_var in os.environ:
                d = os.environ[env_var]
                if d == 'None':
                    log.info('Disabled %s: %s', self.__class__.__name__, '(%s is None)' % (
                     env_var,))
                    return []
                    if os.path.isfile(d):
                        dirs = [
                         os.path.dirname(d)] + dirs
                        l = getattr(self, '_lib_names', [])
                        if len(l) == 1:
                            b = os.path.basename(d)
                            b = os.path.splitext(b)[0]
                            if b[:3] == 'lib':
                                log.info('Replacing _lib_names[0]==%r with %r' % (
                                 self._lib_names[0], b[3:]))
                                self._lib_names[0] = b[3:]
                else:
                    ds = d.split(os.pathsep)
                    ds2 = []
                    for d in ds:
                        if os.path.isdir(d):
                            ds2.append(d)
                            for dd in ('include', 'lib'):
                                d1 = os.path.join(d, dd)
                                if os.path.isdir(d1):
                                    ds2.append(d1)

                    dirs = ds2 + dirs
        default_dirs = self.cp.get(self.section, key).split(os.pathsep)
        dirs.extend(default_dirs)
        ret = []
        for d in dirs:
            if len(d) > 0:
                if not os.path.isdir(d):
                    warnings.warn(('Specified path %s is invalid.' % d), stacklevel=2)
                    continue
                if d not in ret:
                    ret.append(d)

        log.debug('( %s = %s )', key, ':'.join(ret))
        return ret

    def get_lib_dirs(self, key='library_dirs'):
        return self.get_paths(self.section, key)

    def get_runtime_lib_dirs(self, key='runtime_library_dirs'):
        path = self.get_paths(self.section, key)
        if path == ['']:
            path = []
        return path

    def get_include_dirs(self, key='include_dirs'):
        return self.get_paths(self.section, key)

    def get_src_dirs(self, key='src_dirs'):
        return self.get_paths(self.section, key)

    def get_libs(self, key, default):
        try:
            libs = self.cp.get(self.section, key)
        except NoOptionError:
            if not default:
                return []
            if is_string(default):
                return [
                 default]
            return default
        else:
            return [b for b in [a.strip() for a in libs.split(',')] if b]

    def get_libraries(self, key='libraries'):
        if hasattr(self, '_lib_names'):
            return self.get_libs(key, default=(self._lib_names))
        return self.get_libs(key, '')

    def library_extensions(self):
        c = customized_ccompiler()
        static_exts = []
        if c.compiler_type != 'msvc':
            static_exts.append('.a')
        else:
            if sys.platform == 'win32':
                static_exts.append('.lib')
            if self.search_static_first:
                exts = static_exts + [so_ext]
            else:
                exts = [
                 so_ext] + static_exts
        if sys.platform == 'cygwin':
            exts.append('.dll.a')
        if sys.platform == 'darwin':
            exts.append('.dylib')
        return exts

    def check_libs(self, lib_dirs, libs, opt_libs=[]):
        """If static or shared libraries are available then return
        their info dictionary.

        Checks for all libraries as shared libraries first, then
        static (or vice versa if self.search_static_first is True).
        """
        exts = self.library_extensions()
        info = None
        for ext in exts:
            info = self._check_libs(lib_dirs, libs, opt_libs, [ext])
            if info is not None:
                break

        if not info:
            log.info('  libraries %s not found in %s', ','.join(libs), lib_dirs)
        return info

    def check_libs2(self, lib_dirs, libs, opt_libs=[]):
        """If static or shared libraries are available then return
        their info dictionary.

        Checks each library for shared or static.
        """
        exts = self.library_extensions()
        info = self._check_libs(lib_dirs, libs, opt_libs, exts)
        if not info:
            log.info('  libraries %s not found in %s', ','.join(libs), lib_dirs)
        return info

    def _find_lib(self, lib_dir, lib, exts):
        if not is_string(lib_dir):
            raise AssertionError
        elif sys.platform == 'win32':
            lib_prefixes = [
             '', 'lib']
        else:
            lib_prefixes = [
             'lib']
        for ext in exts:
            for prefix in lib_prefixes:
                p = self.combine_paths(lib_dir, prefix + lib + ext)
                if p:
                    if is_symlink_to_accelerate(p[0]):
                        raise RuntimeError(_accel_msg.format(filename=(p[0])))
                    break

            if p:
                assert len(p) == 1
                if ext == '.dll.a':
                    lib += '.dll'
                if ext == '.lib':
                    lib = prefix + lib
                return lib

        return False

    def _find_libs(self, lib_dirs, libs, exts):
        found_dirs, found_libs = [], []
        for lib in libs:
            for lib_dir in lib_dirs:
                found_lib = self._find_lib(lib_dir, lib, exts)
                if found_lib:
                    found_libs.append(found_lib)
                    if lib_dir not in found_dirs:
                        found_dirs.append(lib_dir)
                    break

        return (
         found_dirs, found_libs)

    def _check_libs(self, lib_dirs, libs, opt_libs, exts):
        """Find mandatory and optional libs in expected paths.

        Missing optional libraries are silently forgotten.
        """
        if not is_sequence(lib_dirs):
            lib_dirs = [
             lib_dirs]
        found_dirs, found_libs = self._find_libs(lib_dirs, libs, exts)
        if len(found_libs) > 0:
            if len(found_libs) == len(libs):
                opt_found_dirs, opt_found_libs = self._find_libs(lib_dirs, opt_libs, exts)
                found_libs.extend(opt_found_libs)
                for lib_dir in opt_found_dirs:
                    if lib_dir not in found_dirs:
                        found_dirs.append(lib_dir)

                info = {'libraries':found_libs, 
                 'library_dirs':found_dirs}
                return info
        return

    def combine_paths(self, *args):
        """Return a list of existing paths composed by all combinations
        of items from the arguments.
        """
        return combine_paths(*args)


class fft_opt_info(system_info):

    def calc_info(self):
        info = {}
        fftw_info = get_info('fftw3') or get_info('fftw2') or get_info('dfftw')
        djbfft_info = get_info('djbfft')
        if fftw_info:
            dict_append(info, **fftw_info)
            if djbfft_info:
                dict_append(info, **djbfft_info)
            (self.set_info)(**info)
            return


class fftw_info(system_info):
    section = 'fftw'
    dir_env_var = 'FFTW'
    notfounderror = FFTWNotFoundError
    ver_info = [
     {'name':'fftw3',  'libs':[
       'fftw3'], 
      'includes':[
       'fftw3.h'], 
      'macros':[
       ('SCIPY_FFTW3_H', None)]},
     {'name':'fftw2', 
      'libs':[
       'rfftw', 'fftw'], 
      'includes':[
       'fftw.h', 'rfftw.h'], 
      'macros':[
       ('SCIPY_FFTW_H', None)]}]

    def calc_ver_info(self, ver_param):
        """Returns True on successful version detection, else False"""
        lib_dirs = self.get_lib_dirs()
        incl_dirs = self.get_include_dirs()
        opt = self.get_option_single(self.section + '_libs', 'libraries')
        libs = self.get_libs(opt, ver_param['libs'])
        info = self.check_libs(lib_dirs, libs)
        if info is not None:
            flag = 0
            for d in incl_dirs:
                if len(self.combine_paths(d, ver_param['includes'])) == len(ver_param['includes']):
                    dict_append(info, include_dirs=[d])
                    flag = 1
                    break

            if flag:
                dict_append(info, define_macros=(ver_param['macros']))
            else:
                info = None
        if info is not None:
            (self.set_info)(**info)
            return True
        log.info('  %s not found' % ver_param['name'])
        return False

    def calc_info(self):
        for i in self.ver_info:
            if self.calc_ver_info(i):
                break


class fftw2_info(fftw_info):
    section = 'fftw'
    dir_env_var = 'FFTW'
    notfounderror = FFTWNotFoundError
    ver_info = [
     {'name':'fftw2',  'libs':[
       'rfftw', 'fftw'], 
      'includes':[
       'fftw.h', 'rfftw.h'], 
      'macros':[
       ('SCIPY_FFTW_H', None)]}]


class fftw3_info(fftw_info):
    section = 'fftw3'
    dir_env_var = 'FFTW3'
    notfounderror = FFTWNotFoundError
    ver_info = [
     {'name':'fftw3',  'libs':[
       'fftw3'], 
      'includes':[
       'fftw3.h'], 
      'macros':[
       ('SCIPY_FFTW3_H', None)]}]


class dfftw_info(fftw_info):
    section = 'fftw'
    dir_env_var = 'FFTW'
    ver_info = [
     {'name':'dfftw',  'libs':[
       'drfftw', 'dfftw'], 
      'includes':[
       'dfftw.h', 'drfftw.h'], 
      'macros':[
       ('SCIPY_DFFTW_H', None)]}]


class sfftw_info(fftw_info):
    section = 'fftw'
    dir_env_var = 'FFTW'
    ver_info = [
     {'name':'sfftw',  'libs':[
       'srfftw', 'sfftw'], 
      'includes':[
       'sfftw.h', 'srfftw.h'], 
      'macros':[
       ('SCIPY_SFFTW_H', None)]}]


class fftw_threads_info(fftw_info):
    section = 'fftw'
    dir_env_var = 'FFTW'
    ver_info = [
     {'name':'fftw threads',  'libs':[
       'rfftw_threads', 'fftw_threads'], 
      'includes':[
       'fftw_threads.h', 'rfftw_threads.h'], 
      'macros':[
       ('SCIPY_FFTW_THREADS_H', None)]}]


class dfftw_threads_info(fftw_info):
    section = 'fftw'
    dir_env_var = 'FFTW'
    ver_info = [
     {'name':'dfftw threads',  'libs':[
       'drfftw_threads', 'dfftw_threads'], 
      'includes':[
       'dfftw_threads.h', 'drfftw_threads.h'], 
      'macros':[
       ('SCIPY_DFFTW_THREADS_H', None)]}]


class sfftw_threads_info(fftw_info):
    section = 'fftw'
    dir_env_var = 'FFTW'
    ver_info = [
     {'name':'sfftw threads',  'libs':[
       'srfftw_threads', 'sfftw_threads'], 
      'includes':[
       'sfftw_threads.h', 'srfftw_threads.h'], 
      'macros':[
       ('SCIPY_SFFTW_THREADS_H', None)]}]


class djbfft_info(system_info):
    section = 'djbfft'
    dir_env_var = 'DJBFFT'
    notfounderror = DJBFFTNotFoundError

    def get_paths(self, section, key):
        pre_dirs = system_info.get_paths(self, section, key)
        dirs = []
        for d in pre_dirs:
            dirs.extend(self.combine_paths(d, ['djbfft']) + [d])

        return [d for d in dirs if os.path.isdir(d)]

    def calc_info(self):
        lib_dirs = self.get_lib_dirs()
        incl_dirs = self.get_include_dirs()
        info = None
        for d in lib_dirs:
            p = self.combine_paths(d, ['djbfft.a'])
            if p:
                info = {'extra_objects': p}
                break
            p = self.combine_paths(d, ['libdjbfft.a', 'libdjbfft' + so_ext])
            if p:
                info = {'libraries':[
                  'djbfft'], 
                 'library_dirs':[d]}
                break

        if info is None:
            return
        for d in incl_dirs:
            if len(self.combine_paths(d, ['fftc8.h', 'fftfreq.h'])) == 2:
                dict_append(info, include_dirs=[d], define_macros=[
                 ('SCIPY_DJBFFT_H', None)])
                (self.set_info)(**info)
                return


class mkl_info(system_info):
    section = 'mkl'
    dir_env_var = 'MKLROOT'
    _lib_mkl = ['mkl_rt']

    def get_mkl_rootdir(self):
        mklroot = os.environ.get('MKLROOT', None)
        if mklroot is not None:
            return mklroot
        paths = os.environ.get('LD_LIBRARY_PATH', '').split(os.pathsep)
        ld_so_conf = '/etc/ld.so.conf'
        if os.path.isfile(ld_so_conf):
            with open(ld_so_conf, 'r') as (f):
                for d in f:
                    d = d.strip()
                    if d:
                        paths.append(d)

        intel_mkl_dirs = []
        for path in paths:
            path_atoms = path.split(os.sep)
            for m in path_atoms:
                if m.startswith('mkl'):
                    d = os.sep.join(path_atoms[:path_atoms.index(m) + 2])
                    intel_mkl_dirs.append(d)
                    break

        for d in paths:
            dirs = glob(os.path.join(d, 'mkl', '*'))
            dirs += glob(os.path.join(d, 'mkl*'))
            for sub_dir in dirs:
                if os.path.isdir(os.path.join(sub_dir, 'lib')):
                    return sub_dir

    def __init__(self):
        mklroot = self.get_mkl_rootdir()
        if mklroot is None:
            system_info.__init__(self)
        else:
            from .cpuinfo import cpu
            if cpu.is_Itanium():
                plt = '64'
            else:
                if cpu.is_Intel() and cpu.is_64bit():
                    plt = 'intel64'
                else:
                    plt = '32'
            system_info.__init__(self,
              default_lib_dirs=[
             os.path.join(mklroot, 'lib', plt)],
              default_include_dirs=[
             os.path.join(mklroot, 'include')])

    def calc_info(self):
        lib_dirs = self.get_lib_dirs()
        incl_dirs = self.get_include_dirs()
        opt = self.get_option_single('mkl_libs', 'libraries')
        mkl_libs = self.get_libs(opt, self._lib_mkl)
        info = self.check_libs2(lib_dirs, mkl_libs)
        if info is None:
            return
        else:
            dict_append(info, define_macros=[
             ('SCIPY_MKL_H', None),
             ('HAVE_CBLAS', None)],
              include_dirs=incl_dirs)
            if sys.platform == 'win32':
                pass
            else:
                dict_append(info, libraries=['pthread'])
        (self.set_info)(**info)


class lapack_mkl_info(mkl_info):
    pass


class blas_mkl_info(mkl_info):
    pass


class atlas_info(system_info):
    section = 'atlas'
    dir_env_var = 'ATLAS'
    _lib_names = ['f77blas', 'cblas']
    if sys.platform[:7] == 'freebsd':
        _lib_atlas = [
         'atlas_r']
        _lib_lapack = ['alapack_r']
    else:
        _lib_atlas = [
         'atlas']
        _lib_lapack = ['lapack']
    notfounderror = AtlasNotFoundError

    def get_paths(self, section, key):
        pre_dirs = system_info.get_paths(self, section, key)
        dirs = []
        for d in pre_dirs:
            dirs.extend(self.combine_paths(d, ['atlas*', 'ATLAS*',
             'sse', '3dnow', 'sse2']) + [d])

        return [d for d in dirs if os.path.isdir(d)]

    def calc_info(self):
        lib_dirs = self.get_lib_dirs()
        info = {}
        opt = self.get_option_single('atlas_libs', 'libraries')
        atlas_libs = self.get_libs(opt, self._lib_names + self._lib_atlas)
        lapack_libs = self.get_libs('lapack_libs', self._lib_lapack)
        atlas = None
        lapack = None
        atlas_1 = None
        for d in lib_dirs:
            lapack_atlas = self.check_libs2(d, ['lapack_atlas'], [])
            atlas = self.check_libs2(d, atlas_libs, [])
            if atlas is not None:
                lib_dirs2 = [
                 d] + self.combine_paths(d, ['atlas*', 'ATLAS*'])
                lapack = self.check_libs2(lib_dirs2, lapack_libs, [])
                if lapack is not None:
                    break
            if atlas:
                atlas_1 = atlas

        log.info(self.__class__)
        if atlas is None:
            atlas = atlas_1
        if atlas is None:
            return
        include_dirs = self.get_include_dirs()
        h = self.combine_paths(lib_dirs + include_dirs, 'cblas.h') or [None]
        h = h[0]
        if h:
            h = os.path.dirname(h)
            dict_append(info, include_dirs=[h])
        info['language'] = 'c'
        if lapack is not None:
            dict_append(info, **lapack)
            dict_append(info, **atlas)
        else:
            if 'lapack_atlas' in atlas['libraries']:
                dict_append(info, **atlas)
                dict_append(info, define_macros=[
                 ('ATLAS_WITH_LAPACK_ATLAS', None)])
                (self.set_info)(**info)
                return
                dict_append(info, **atlas)
                dict_append(info, define_macros=[('ATLAS_WITHOUT_LAPACK', None)])
                message = textwrap.dedent('\n                *********************************************************************\n                    Could not find lapack library within the ATLAS installation.\n                *********************************************************************\n                ')
                warnings.warn(message, stacklevel=2)
                (self.set_info)(**info)
                return
                lapack_dir = lapack['library_dirs'][0]
                lapack_name = lapack['libraries'][0]
                lapack_lib = None
                lib_prefixes = ['lib']
                if sys.platform == 'win32':
                    lib_prefixes.append('')
                for e in self.library_extensions():
                    for prefix in lib_prefixes:
                        fn = os.path.join(lapack_dir, prefix + lapack_name + e)
                        if os.path.exists(fn):
                            lapack_lib = fn
                            break

                    if lapack_lib:
                        break

                if lapack_lib is not None:
                    sz = os.stat(lapack_lib)[6]
                    if sz <= 4096000:
                        message = textwrap.dedent('\n                    *********************************************************************\n                        Lapack library (from ATLAS) is probably incomplete:\n                          size of %s is %sk (expected >4000k)\n\n                        Follow the instructions in the KNOWN PROBLEMS section of the file\n                        numpy/INSTALL.txt.\n                    *********************************************************************\n                    ') % (lapack_lib, sz / 1024)
                        warnings.warn(message, stacklevel=2)
            else:
                info['language'] = 'f77'
            atlas_version, atlas_extra_info = get_atlas_version(**atlas)
            dict_append(info, **atlas_extra_info)
            (self.set_info)(**info)


class atlas_blas_info(atlas_info):
    _lib_names = [
     'f77blas', 'cblas']

    def calc_info(self):
        lib_dirs = self.get_lib_dirs()
        info = {}
        opt = self.get_option_single('atlas_libs', 'libraries')
        atlas_libs = self.get_libs(opt, self._lib_names + self._lib_atlas)
        atlas = self.check_libs2(lib_dirs, atlas_libs, [])
        if atlas is None:
            return
        include_dirs = self.get_include_dirs()
        h = self.combine_paths(lib_dirs + include_dirs, 'cblas.h') or [None]
        h = h[0]
        if h:
            h = os.path.dirname(h)
            dict_append(info, include_dirs=[h])
        info['language'] = 'c'
        info['define_macros'] = [('HAVE_CBLAS', None)]
        atlas_version, atlas_extra_info = get_atlas_version(**atlas)
        dict_append(atlas, **atlas_extra_info)
        dict_append(info, **atlas)
        (self.set_info)(**info)


class atlas_threads_info(atlas_info):
    dir_env_var = [
     'PTATLAS', 'ATLAS']
    _lib_names = ['ptf77blas', 'ptcblas']


class atlas_blas_threads_info(atlas_blas_info):
    dir_env_var = [
     'PTATLAS', 'ATLAS']
    _lib_names = ['ptf77blas', 'ptcblas']


class lapack_atlas_info(atlas_info):
    _lib_names = [
     'lapack_atlas'] + atlas_info._lib_names


class lapack_atlas_threads_info(atlas_threads_info):
    _lib_names = [
     'lapack_atlas'] + atlas_threads_info._lib_names


class atlas_3_10_info(atlas_info):
    _lib_names = [
     'satlas']
    _lib_atlas = _lib_names
    _lib_lapack = _lib_names


class atlas_3_10_blas_info(atlas_3_10_info):
    _lib_names = [
     'satlas']

    def calc_info(self):
        lib_dirs = self.get_lib_dirs()
        info = {}
        opt = self.get_option_single('atlas_lib', 'libraries')
        atlas_libs = self.get_libs(opt, self._lib_names)
        atlas = self.check_libs2(lib_dirs, atlas_libs, [])
        if atlas is None:
            return
        include_dirs = self.get_include_dirs()
        h = self.combine_paths(lib_dirs + include_dirs, 'cblas.h') or [None]
        h = h[0]
        if h:
            h = os.path.dirname(h)
            dict_append(info, include_dirs=[h])
        info['language'] = 'c'
        info['define_macros'] = [('HAVE_CBLAS', None)]
        atlas_version, atlas_extra_info = get_atlas_version(**atlas)
        dict_append(atlas, **atlas_extra_info)
        dict_append(info, **atlas)
        (self.set_info)(**info)


class atlas_3_10_threads_info(atlas_3_10_info):
    dir_env_var = [
     'PTATLAS', 'ATLAS']
    _lib_names = ['tatlas']
    _lib_atlas = _lib_names
    _lib_lapack = _lib_names


class atlas_3_10_blas_threads_info(atlas_3_10_blas_info):
    dir_env_var = [
     'PTATLAS', 'ATLAS']
    _lib_names = ['tatlas']


class lapack_atlas_3_10_info(atlas_3_10_info):
    pass


class lapack_atlas_3_10_threads_info(atlas_3_10_threads_info):
    pass


class lapack_info(system_info):
    section = 'lapack'
    dir_env_var = 'LAPACK'
    _lib_names = ['lapack']
    notfounderror = LapackNotFoundError

    def calc_info(self):
        lib_dirs = self.get_lib_dirs()
        opt = self.get_option_single('lapack_libs', 'libraries')
        lapack_libs = self.get_libs(opt, self._lib_names)
        info = self.check_libs(lib_dirs, lapack_libs, [])
        if info is None:
            return
        info['language'] = 'f77'
        (self.set_info)(**info)


class lapack_src_info(system_info):
    section = 'lapack_src'
    dir_env_var = 'LAPACK_SRC'
    notfounderror = LapackSrcNotFoundError

    def get_paths(self, section, key):
        pre_dirs = system_info.get_paths(self, section, key)
        dirs = []
        for d in pre_dirs:
            dirs.extend([d] + self.combine_paths(d, ['LAPACK*/SRC', 'SRC']))

        return [d for d in dirs if os.path.isdir(d)]

    def calc_info(self):
        src_dirs = self.get_src_dirs()
        src_dir = ''
        for d in src_dirs:
            if os.path.isfile(os.path.join(d, 'dgesv.f')):
                src_dir = d
                break

        if not src_dir:
            return
        allaux = '\n        ilaenv ieeeck lsame lsamen xerbla\n        iparmq\n        '
        laux = '\n        bdsdc bdsqr disna labad lacpy ladiv lae2 laebz laed0 laed1\n        laed2 laed3 laed4 laed5 laed6 laed7 laed8 laed9 laeda laev2\n        lagtf lagts lamch lamrg lanst lapy2 lapy3 larnv larrb larre\n        larrf lartg laruv las2 lascl lasd0 lasd1 lasd2 lasd3 lasd4\n        lasd5 lasd6 lasd7 lasd8 lasd9 lasda lasdq lasdt laset lasq1\n        lasq2 lasq3 lasq4 lasq5 lasq6 lasr lasrt lassq lasv2 pttrf\n        stebz stedc steqr sterf\n\n        larra larrc larrd larr larrk larrj larrr laneg laisnan isnan\n        lazq3 lazq4\n        '
        lasrc = '\n        gbbrd gbcon gbequ gbrfs gbsv gbsvx gbtf2 gbtrf gbtrs gebak\n        gebal gebd2 gebrd gecon geequ gees geesx geev geevx gegs gegv\n        gehd2 gehrd gelq2 gelqf gels gelsd gelss gelsx gelsy geql2\n        geqlf geqp3 geqpf geqr2 geqrf gerfs gerq2 gerqf gesc2 gesdd\n        gesv gesvd gesvx getc2 getf2 getrf getri getrs ggbak ggbal\n        gges ggesx ggev ggevx ggglm gghrd gglse ggqrf ggrqf ggsvd\n        ggsvp gtcon gtrfs gtsv gtsvx gttrf gttrs gtts2 hgeqz hsein\n        hseqr labrd lacon laein lags2 lagtm lahqr lahrd laic1 lals0\n        lalsa lalsd langb lange langt lanhs lansb lansp lansy lantb\n        lantp lantr lapll lapmt laqgb laqge laqp2 laqps laqsb laqsp\n        laqsy lar1v lar2v larf larfb larfg larft larfx largv larrv\n        lartv larz larzb larzt laswp lasyf latbs latdf latps latrd\n        latrs latrz latzm lauu2 lauum pbcon pbequ pbrfs pbstf pbsv\n        pbsvx pbtf2 pbtrf pbtrs pocon poequ porfs posv posvx potf2\n        potrf potri potrs ppcon ppequ pprfs ppsv ppsvx pptrf pptri\n        pptrs ptcon pteqr ptrfs ptsv ptsvx pttrs ptts2 spcon sprfs\n        spsv spsvx sptrf sptri sptrs stegr stein sycon syrfs sysv\n        sysvx sytf2 sytrf sytri sytrs tbcon tbrfs tbtrs tgevc tgex2\n        tgexc tgsen tgsja tgsna tgsy2 tgsyl tpcon tprfs tptri tptrs\n        trcon trevc trexc trrfs trsen trsna trsyl trti2 trtri trtrs\n        tzrqf tzrzf\n\n        lacn2 lahr2 stemr laqr0 laqr1 laqr2 laqr3 laqr4 laqr5\n        '
        sd_lasrc = '\n        laexc lag2 lagv2 laln2 lanv2 laqtr lasy2 opgtr opmtr org2l\n        org2r orgbr orghr orgl2 orglq orgql orgqr orgr2 orgrq orgtr\n        orm2l orm2r ormbr ormhr orml2 ormlq ormql ormqr ormr2 ormr3\n        ormrq ormrz ormtr rscl sbev sbevd sbevx sbgst sbgv sbgvd sbgvx\n        sbtrd spev spevd spevx spgst spgv spgvd spgvx sptrd stev stevd\n        stevr stevx syev syevd syevr syevx sygs2 sygst sygv sygvd\n        sygvx sytd2 sytrd\n        '
        cz_lasrc = '\n        bdsqr hbev hbevd hbevx hbgst hbgv hbgvd hbgvx hbtrd hecon heev\n        heevd heevr heevx hegs2 hegst hegv hegvd hegvx herfs hesv\n        hesvx hetd2 hetf2 hetrd hetrf hetri hetrs hpcon hpev hpevd\n        hpevx hpgst hpgv hpgvd hpgvx hprfs hpsv hpsvx hptrd hptrf\n        hptri hptrs lacgv lacp2 lacpy lacrm lacrt ladiv laed0 laed7\n        laed8 laesy laev2 lahef lanhb lanhe lanhp lanht laqhb laqhe\n        laqhp larcm larnv lartg lascl laset lasr lassq pttrf rot spmv\n        spr stedc steqr symv syr ung2l ung2r ungbr unghr ungl2 unglq\n        ungql ungqr ungr2 ungrq ungtr unm2l unm2r unmbr unmhr unml2\n        unmlq unmql unmqr unmr2 unmr3 unmrq unmrz unmtr upgtr upmtr\n        '
        sclaux = laux + ' econd '
        dzlaux = laux + ' secnd '
        slasrc = lasrc + sd_lasrc
        dlasrc = lasrc + sd_lasrc
        clasrc = lasrc + cz_lasrc + ' srot srscl '
        zlasrc = lasrc + cz_lasrc + ' drot drscl '
        oclasrc = ' icmax1 scsum1 '
        ozlasrc = ' izmax1 dzsum1 '
        sources = ['s%s.f' % f for f in (sclaux + slasrc).split()] + ['d%s.f' % f for f in (dzlaux + dlasrc).split()] + ['c%s.f' % f for f in clasrc.split()] + ['z%s.f' % f for f in zlasrc.split()] + ['%s.f' % f for f in (allaux + oclasrc + ozlasrc).split()]
        sources = [os.path.join(src_dir, f) for f in sources]
        src_dir2 = os.path.join(src_dir, '..', 'INSTALL')
        sources += [os.path.join(src_dir2, p + 'lamch.f') for p in 'sdcz']
        sources += [os.path.join(src_dir, p + 'larfp.f') for p in 'sdcz']
        sources += [os.path.join(src_dir, 'ila' + p + 'lr.f') for p in 'sdcz']
        sources += [os.path.join(src_dir, 'ila' + p + 'lc.f') for p in 'sdcz']
        sources = [f for f in sources if os.path.isfile(f)]
        info = {'sources':sources,  'language':'f77'}
        (self.set_info)(**info)


atlas_version_c_text = '\n/* This file is generated from numpy/distutils/system_info.py */\nvoid ATL_buildinfo(void);\nint main(void) {\n  ATL_buildinfo();\n  return 0;\n}\n'
_cached_atlas_version = {}

def get_atlas_version(**config):
    libraries = config.get('libraries', [])
    library_dirs = config.get('library_dirs', [])
    key = (tuple(libraries), tuple(library_dirs))
    if key in _cached_atlas_version:
        return _cached_atlas_version[key]
    c = cmd_config(Distribution())
    atlas_version = None
    info = {}
    try:
        s, o = c.get_output(atlas_version_c_text, libraries=libraries,
          library_dirs=library_dirs)
        if s:
            if re.search('undefined reference to `_gfortran', o, re.M):
                s, o = c.get_output(atlas_version_c_text, libraries=(libraries + ['gfortran']),
                  library_dirs=library_dirs)
                if not s:
                    warnings.warn((textwrap.dedent('\n                    *****************************************************\n                    Linkage with ATLAS requires gfortran. Use\n\n                      python setup.py config_fc --fcompiler=gnu95 ...\n\n                    when building extension libraries that use ATLAS.\n                    Make sure that -lgfortran is used for C++ extensions.\n                    *****************************************************\n                    ')),
                      stacklevel=2)
                    dict_append(info, language='f90', define_macros=[
                     ('ATLAS_REQUIRES_GFORTRAN', None)])
    except Exception:
        for o in library_dirs:
            m = re.search('ATLAS_(?P<version>\\d+[.]\\d+[.]\\d+)_', o)
            if m:
                atlas_version = m.group('version')
            if atlas_version is not None:
                break

        if atlas_version is None:
            atlas_version = os.environ.get('ATLAS_VERSION', None)
        elif atlas_version:
            dict_append(info, define_macros=[
             (
              'ATLAS_INFO', _c_string_literal(atlas_version))])
        else:
            dict_append(info, define_macros=[('NO_ATLAS_INFO', -1)])
        return (
         atlas_version or '?.?.?', info)
    else:
        m = s or re.search('ATLAS version (?P<version>\\d+[.]\\d+[.]\\d+)', o)
        if m:
            atlas_version = m.group('version')
        if atlas_version is None:
            if re.search('undefined symbol: ATL_buildinfo', o, re.M):
                atlas_version = '3.2.1_pre3.3.6'
            else:
                log.info('Status: %d', s)
                log.info('Output: %s', o)
        else:
            if atlas_version == '3.2.1_pre3.3.6':
                dict_append(info, define_macros=[('NO_ATLAS_INFO', -2)])
            else:
                dict_append(info, define_macros=[
                 (
                  'ATLAS_INFO', _c_string_literal(atlas_version))])
        result = _cached_atlas_version[key] = (
         atlas_version, info)
        return result


class lapack_opt_info(system_info):
    notfounderror = LapackNotFoundError
    lapack_order = [
     'mkl', 'openblas', 'flame', 'atlas', 'lapack']
    order_env_var_name = 'NPY_LAPACK_ORDER'

    def _calc_info_mkl(self):
        info = get_info('lapack_mkl')
        if info:
            (self.set_info)(**info)
            return True
        return False

    def _calc_info_openblas(self):
        info = get_info('openblas_lapack')
        if info:
            (self.set_info)(**info)
            return True
        info = get_info('openblas_clapack')
        if info:
            (self.set_info)(**info)
            return True
        return False

    def _calc_info_flame(self):
        info = get_info('flame')
        if info:
            (self.set_info)(**info)
            return True
        return False

    def _calc_info_atlas(self):
        info = get_info('atlas_3_10_threads')
        if not info:
            info = get_info('atlas_3_10')
        if not info:
            info = get_info('atlas_threads')
        if not info:
            info = get_info('atlas')
        if info:
            l = info.get('define_macros', [])
            if ('ATLAS_WITH_LAPACK_ATLAS', None) in l or ('ATLAS_WITHOUT_LAPACK', None) in l:
                lapack_info = self._get_info_lapack()
                if not lapack_info:
                    return False
                dict_append(info, **lapack_info)
            (self.set_info)(**info)
            return True
        return False

    def _calc_info_accelerate(self):
        info = get_info('accelerate')
        if info:
            (self.set_info)(**info)
            return True
        return False

    def _get_info_blas(self):
        info = get_info('blas_opt')
        if not info:
            warnings.warn((BlasNotFoundError.__doc__ or ''), stacklevel=3)
            info_src = get_info('blas_src')
            if not info_src:
                warnings.warn((BlasSrcNotFoundError.__doc__ or ''), stacklevel=3)
                return {}
            dict_append(info, libraries=[('fblas_src', info_src)])
        return info

    def _get_info_lapack(self):
        info = get_info('lapack')
        if not info:
            warnings.warn((LapackNotFoundError.__doc__ or ''), stacklevel=3)
            info_src = get_info('lapack_src')
            if not info_src:
                warnings.warn((LapackSrcNotFoundError.__doc__ or ''), stacklevel=3)
                return {}
            dict_append(info, libraries=[('flapack_src', info_src)])
        return info

    def _calc_info_lapack(self):
        info = self._get_info_lapack()
        if info:
            info_blas = self._get_info_blas()
            dict_append(info, **info_blas)
            dict_append(info, define_macros=[('NO_ATLAS_INFO', 1)])
            (self.set_info)(**info)
            return True
        return False

    def _calc_info(self, name):
        return getattr(self, '_calc_info_{}'.format(name))()

    def calc_info(self):
        lapack_order, unknown_order = _parse_env_order(self.lapack_order, self.order_env_var_name)
        if len(unknown_order) > 0:
            raise ValueError('lapack_opt_info user defined LAPACK order has unacceptable values: {}'.format(unknown_order))
        for lapack in lapack_order:
            if self._calc_info(lapack):
                return

        if 'lapack' not in lapack_order:
            warnings.warn((LapackNotFoundError.__doc__ or ''), stacklevel=2)
            warnings.warn((LapackSrcNotFoundError.__doc__ or ''), stacklevel=2)


class _ilp64_opt_info_mixin:
    symbol_suffix = None
    symbol_prefix = None

    def _check_info(self, info):
        macros = dict(info.get('define_macros', []))
        prefix = macros.get('BLAS_SYMBOL_PREFIX', '')
        suffix = macros.get('BLAS_SYMBOL_SUFFIX', '')
        if self.symbol_prefix not in (None, prefix):
            return False
        if self.symbol_suffix not in (None, suffix):
            return False
        return bool(info)


class lapack_ilp64_opt_info(lapack_opt_info, _ilp64_opt_info_mixin):
    notfounderror = LapackILP64NotFoundError
    lapack_order = ['openblas64_', 'openblas_ilp64']
    order_env_var_name = 'NPY_LAPACK_ILP64_ORDER'

    def _calc_info(self, name):
        info = get_info(name + '_lapack')
        if self._check_info(info):
            (self.set_info)(**info)
            return True
        return False


class lapack_ilp64_plain_opt_info(lapack_ilp64_opt_info):
    symbol_prefix = ''
    symbol_suffix = ''


class lapack64__opt_info(lapack_ilp64_opt_info):
    symbol_prefix = ''
    symbol_suffix = '64_'


class blas_opt_info(system_info):
    notfounderror = BlasNotFoundError
    blas_order = [
     'mkl', 'blis', 'openblas', 'atlas', 'blas']
    order_env_var_name = 'NPY_BLAS_ORDER'

    def _calc_info_mkl(self):
        info = get_info('blas_mkl')
        if info:
            (self.set_info)(**info)
            return True
        return False

    def _calc_info_blis(self):
        info = get_info('blis')
        if info:
            (self.set_info)(**info)
            return True
        return False

    def _calc_info_openblas(self):
        info = get_info('openblas')
        if info:
            (self.set_info)(**info)
            return True
        return False

    def _calc_info_atlas(self):
        info = get_info('atlas_3_10_blas_threads')
        if not info:
            info = get_info('atlas_3_10_blas')
        if not info:
            info = get_info('atlas_blas_threads')
        if not info:
            info = get_info('atlas_blas')
        if info:
            (self.set_info)(**info)
            return True
        return False

    def _calc_info_accelerate(self):
        info = get_info('accelerate')
        if info:
            (self.set_info)(**info)
            return True
        return False

    def _calc_info_blas(self):
        warnings.warn((BlasOptNotFoundError.__doc__ or ''), stacklevel=3)
        info = {}
        dict_append(info, define_macros=[('NO_ATLAS_INFO', 1)])
        blas = get_info('blas')
        if blas:
            dict_append(info, **blas)
        else:
            warnings.warn((BlasNotFoundError.__doc__ or ''), stacklevel=3)
            blas_src = get_info('blas_src')
            if not blas_src:
                warnings.warn((BlasSrcNotFoundError.__doc__ or ''), stacklevel=3)
                return False
            dict_append(info, libraries=[('fblas_src', blas_src)])
        (self.set_info)(**info)
        return True

    def _calc_info(self, name):
        return getattr(self, '_calc_info_{}'.format(name))()

    def calc_info(self):
        blas_order, unknown_order = _parse_env_order(self.blas_order, self.order_env_var_name)
        if len(unknown_order) > 0:
            raise ValueError('blas_opt_info user defined BLAS order has unacceptable values: {}'.format(unknown_order))
        for blas in blas_order:
            if self._calc_info(blas):
                return

        if 'blas' not in blas_order:
            warnings.warn((BlasNotFoundError.__doc__ or ''), stacklevel=2)
            warnings.warn((BlasSrcNotFoundError.__doc__ or ''), stacklevel=2)


class blas_ilp64_opt_info(blas_opt_info, _ilp64_opt_info_mixin):
    notfounderror = BlasILP64NotFoundError
    blas_order = ['openblas64_', 'openblas_ilp64']
    order_env_var_name = 'NPY_BLAS_ILP64_ORDER'

    def _calc_info(self, name):
        info = get_info(name)
        if self._check_info(info):
            (self.set_info)(**info)
            return True
        return False


class blas_ilp64_plain_opt_info(blas_ilp64_opt_info):
    symbol_prefix = ''
    symbol_suffix = ''


class blas64__opt_info(blas_ilp64_opt_info):
    symbol_prefix = ''
    symbol_suffix = '64_'


class cblas_info(system_info):
    section = 'cblas'
    dir_env_var = 'CBLAS'
    _lib_names = []
    notfounderror = BlasNotFoundError


class blas_info(system_info):
    section = 'blas'
    dir_env_var = 'BLAS'
    _lib_names = ['blas']
    notfounderror = BlasNotFoundError

    def calc_info(self):
        lib_dirs = self.get_lib_dirs()
        opt = self.get_option_single('blas_libs', 'libraries')
        blas_libs = self.get_libs(opt, self._lib_names)
        info = self.check_libs(lib_dirs, blas_libs, [])
        if info is None:
            return
            info['include_dirs'] = self.get_include_dirs()
            if platform.system() == 'Windows':
                info['language'] = 'f77'
                cblas_info_obj = cblas_info()
                cblas_opt = cblas_info_obj.get_option_single('cblas_libs', 'libraries')
                cblas_libs = cblas_info_obj.get_libs(cblas_opt, None)
                if cblas_libs:
                    info['libraries'] = cblas_libs + blas_libs
                    info['define_macros'] = [('HAVE_CBLAS', None)]
        else:
            lib = self.get_cblas_libs(info)
            if lib is not None:
                info['language'] = 'c'
                info['libraries'] = lib
                info['define_macros'] = [('HAVE_CBLAS', None)]
        (self.set_info)(**info)

    def get_cblas_libs(self, info):
        """ Check whether we can link with CBLAS interface

        This method will search through several combinations of libraries
        to check whether CBLAS is present:

        1. Libraries in ``info['libraries']``, as is
        2. As 1. but also explicitly adding ``'cblas'`` as a library
        3. As 1. but also explicitly adding ``'blas'`` as a library
        4. Check only library ``'cblas'``
        5. Check only library ``'blas'``

        Parameters
        ----------
        info : dict
           system information dictionary for compilation and linking

        Returns
        -------
        libraries : list of str or None
            a list of libraries that enables the use of CBLAS interface.
            Returns None if not found or a compilation error occurs.

            Since 1.17 returns a list.
        """
        c = customized_ccompiler()
        tmpdir = tempfile.mkdtemp()
        s = textwrap.dedent('            #include <cblas.h>\n            int main(int argc, const char *argv[])\n            {\n                double a[4] = {1,2,3,4};\n                double b[4] = {5,6,7,8};\n                return cblas_ddot(4, a, 1, b, 1) > 10;\n            }')
        src = os.path.join(tmpdir, 'source.c')
        try:
            with open(src, 'wt') as (f):
                f.write(s)
            try:
                obj = c.compile([src], output_dir=tmpdir, include_dirs=(self.get_include_dirs()))
            except (distutils.ccompiler.CompileError, distutils.ccompiler.LinkError):
                return
            else:
                for libs in [info['libraries'], ['cblas'] + info['libraries'],
                 [
                  'blas'] + info['libraries'], ['cblas'], ['blas']]:
                    try:
                        c.link_executable(obj, (os.path.join(tmpdir, 'a.out')), libraries=libs,
                          library_dirs=(info['library_dirs']),
                          extra_postargs=(info.get('extra_link_args', [])))
                        return libs
                    except distutils.ccompiler.LinkError:
                        pass

        finally:
            shutil.rmtree(tmpdir)


class openblas_info(blas_info):
    section = 'openblas'
    dir_env_var = 'OPENBLAS'
    _lib_names = ['openblas']
    _require_symbols = []
    notfounderror = BlasNotFoundError

    @property
    def symbol_prefix(self):
        try:
            return self.cp.get(self.section, 'symbol_prefix')
        except NoOptionError:
            return ''

    @property
    def symbol_suffix(self):
        try:
            return self.cp.get(self.section, 'symbol_suffix')
        except NoOptionError:
            return ''

    def _calc_info(self):
        c = customized_ccompiler()
        lib_dirs = self.get_lib_dirs()
        opt = self.get_option_single('openblas_libs', 'libraries')
        openblas_libs = self.get_libs(opt, self._lib_names)
        info = self.check_libs(lib_dirs, openblas_libs, [])
        if c.compiler_type == 'msvc' and info is None:
            from numpy.distutils.fcompiler import new_fcompiler
            f = new_fcompiler(c_compiler=c)
            if f and f.compiler_type == 'gnu95':
                info = self.check_msvc_gfortran_libs(lib_dirs, openblas_libs)
                skip_symbol_check = True
        elif info:
            skip_symbol_check = False
            info['language'] = 'c'
        if info is None:
            return
        extra_info = self.calc_extra_info()
        dict_append(info, **extra_info)
        if not skip_symbol_check:
            if not self.check_symbols(info):
                return
        info['define_macros'] = [
         ('HAVE_CBLAS', None)]
        if self.symbol_prefix:
            info['define_macros'] += [('BLAS_SYMBOL_PREFIX', self.symbol_prefix)]
        if self.symbol_suffix:
            info['define_macros'] += [('BLAS_SYMBOL_SUFFIX', self.symbol_suffix)]
        return info

    def calc_info(self):
        info = self._calc_info()
        if info is not None:
            (self.set_info)(**info)

    def check_msvc_gfortran_libs(self, library_dirs, libraries):
        library_paths = []
        for library in libraries:
            for library_dir in library_dirs:
                fullpath = os.path.join(library_dir, library + '.a')
                if os.path.isfile(fullpath):
                    library_paths.append(fullpath)
                    break
            else:
                return

        basename = self.__class__.__name__
        tmpdir = os.path.join(os.getcwd(), 'build', basename)
        if not os.path.isdir(tmpdir):
            os.makedirs(tmpdir)
        info = {'library_dirs':[tmpdir],  'libraries':[
          basename], 
         'language':'f77'}
        fake_lib_file = os.path.join(tmpdir, basename + '.fobjects')
        fake_clib_file = os.path.join(tmpdir, basename + '.cobjects')
        with open(fake_lib_file, 'w') as (f):
            f.write('\n'.join(library_paths))
        with open(fake_clib_file, 'w') as (f):
            pass
        return info

    def check_symbols(self, info):
        res = False
        c = customized_ccompiler()
        tmpdir = tempfile.mkdtemp()
        prototypes = '\n'.join(('void %s%s%s();' % (self.symbol_prefix, symbol_name, self.symbol_suffix) for symbol_name in self._require_symbols))
        calls = '\n'.join(('%s%s%s();' % (self.symbol_prefix, symbol_name, self.symbol_suffix) for symbol_name in self._require_symbols))
        s = textwrap.dedent('            %(prototypes)s\n            int main(int argc, const char *argv[])\n            {\n                %(calls)s\n                return 0;\n            }') % dict(prototypes=prototypes, calls=calls)
        src = os.path.join(tmpdir, 'source.c')
        out = os.path.join(tmpdir, 'a.out')
        try:
            extra_args = info['extra_link_args']
        except Exception:
            extra_args = []

        try:
            with open(src, 'wt') as (f):
                f.write(s)
            obj = c.compile([src], output_dir=tmpdir)
            try:
                c.link_executable(obj, out, libraries=(info['libraries']), library_dirs=(info['library_dirs']),
                  extra_postargs=extra_args)
                res = True
            except distutils.ccompiler.LinkError:
                res = False

        finally:
            shutil.rmtree(tmpdir)

        return res


class openblas_lapack_info(openblas_info):
    section = 'openblas'
    dir_env_var = 'OPENBLAS'
    _lib_names = ['openblas']
    _require_symbols = ['zungqr_']
    notfounderror = BlasNotFoundError


class openblas_clapack_info(openblas_lapack_info):
    _lib_names = [
     'openblas', 'lapack']


class openblas_ilp64_info(openblas_info):
    section = 'openblas_ilp64'
    dir_env_var = 'OPENBLAS_ILP64'
    _lib_names = ['openblas64']
    _require_symbols = ['dgemm_', 'cblas_dgemm']
    notfounderror = BlasILP64NotFoundError

    def _calc_info(self):
        info = super()._calc_info()
        if info is not None:
            info['define_macros'] += [('HAVE_BLAS_ILP64', None)]
        return info


class openblas_ilp64_lapack_info(openblas_ilp64_info):
    _require_symbols = [
     'dgemm_', 'cblas_dgemm', 'zungqr_', 'LAPACKE_zungqr']

    def _calc_info(self):
        info = super()._calc_info()
        if info:
            info['define_macros'] += [('HAVE_LAPACKE', None)]
        return info


class openblas64__info(openblas_ilp64_info):
    section = 'openblas64_'
    dir_env_var = 'OPENBLAS64_'
    _lib_names = ['openblas64_']
    symbol_suffix = '64_'
    symbol_prefix = ''


class openblas64__lapack_info(openblas_ilp64_lapack_info, openblas64__info):
    pass


class blis_info(blas_info):
    section = 'blis'
    dir_env_var = 'BLIS'
    _lib_names = ['blis']
    notfounderror = BlasNotFoundError

    def calc_info(self):
        lib_dirs = self.get_lib_dirs()
        opt = self.get_option_single('blis_libs', 'libraries')
        blis_libs = self.get_libs(opt, self._lib_names)
        info = self.check_libs2(lib_dirs, blis_libs, [])
        if info is None:
            return
        incl_dirs = self.get_include_dirs()
        dict_append(info, language='c',
          define_macros=[
         ('HAVE_CBLAS', None)],
          include_dirs=incl_dirs)
        (self.set_info)(**info)


class flame_info(system_info):
    __doc__ = ' Usage of libflame for LAPACK operations\n\n    This requires libflame to be compiled with lapack wrappers:\n\n    ./configure --enable-lapack2flame ...\n\n    Be aware that libflame 5.1.0 has some missing names in the shared library, so\n    if you have problems, try the static flame library.\n    '
    section = 'flame'
    _lib_names = ['flame']
    notfounderror = FlameNotFoundError

    def check_embedded_lapack(self, info):
        """ libflame does not necessarily have a wrapper for fortran LAPACK, we need to check """
        c = customized_ccompiler()
        tmpdir = tempfile.mkdtemp()
        s = textwrap.dedent('            void zungqr_();\n            int main(int argc, const char *argv[])\n            {\n                zungqr_();\n                return 0;\n            }')
        src = os.path.join(tmpdir, 'source.c')
        out = os.path.join(tmpdir, 'a.out')
        extra_args = info.get('extra_link_args', [])
        try:
            with open(src, 'wt') as (f):
                f.write(s)
            obj = c.compile([src], output_dir=tmpdir)
            try:
                c.link_executable(obj, out, libraries=(info['libraries']), library_dirs=(info['library_dirs']),
                  extra_postargs=extra_args)
                return True
            except distutils.ccompiler.LinkError:
                return False

        finally:
            shutil.rmtree(tmpdir)

    def calc_info(self):
        lib_dirs = self.get_lib_dirs()
        flame_libs = self.get_libs('libraries', self._lib_names)
        info = self.check_libs2(lib_dirs, flame_libs, [])
        if info is None:
            return
        if self.check_embedded_lapack(info):
            (self.set_info)(**info)
        else:
            blas_info = get_info('blas_opt')
            if not blas_info:
                return
            for key in blas_info:
                if isinstance(blas_info[key], list):
                    info[key] = info.get(key, []) + blas_info[key]
                elif isinstance(blas_info[key], tuple):
                    info[key] = info.get(key, ()) + blas_info[key]
                else:
                    info[key] = info.get(key, '') + blas_info[key]

            if self.check_embedded_lapack(info):
                (self.set_info)(**info)


class accelerate_info(system_info):
    section = 'accelerate'
    _lib_names = ['accelerate', 'veclib']
    notfounderror = BlasNotFoundError

    def calc_info--- This code section failed: ---

 L.2423         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                environ
                4  LOAD_METHOD              get
                6  LOAD_STR                 'ACCELERATE'
                8  CALL_METHOD_1         1  '1 positional argument'
               10  STORE_FAST               'libraries'

 L.2424        12  LOAD_FAST                'libraries'
               14  POP_JUMP_IF_FALSE    24  'to 24'

 L.2425        16  LOAD_FAST                'libraries'
               18  BUILD_LIST_1          1 
               20  STORE_FAST               'libraries'
               22  JUMP_FORWARD         38  'to 38'
             24_0  COME_FROM            14  '14'

 L.2427        24  LOAD_FAST                'self'
               26  LOAD_METHOD              get_libs
               28  LOAD_STR                 'libraries'
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                _lib_names
               34  CALL_METHOD_2         2  '2 positional arguments'
               36  STORE_FAST               'libraries'
             38_0  COME_FROM            22  '22'

 L.2428        38  LOAD_LISTCOMP            '<code_object <listcomp>>'
               40  LOAD_STR                 'accelerate_info.calc_info.<locals>.<listcomp>'
               42  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               44  LOAD_FAST                'libraries'
               46  GET_ITER         
               48  CALL_FUNCTION_1       1  '1 positional argument'
               50  STORE_FAST               'libraries'

 L.2430        52  LOAD_GLOBAL              sys
               54  LOAD_ATTR                platform
               56  LOAD_STR                 'darwin'
               58  COMPARE_OP               ==
            60_62  POP_JUMP_IF_FALSE   332  'to 332'

 L.2431        64  LOAD_GLOBAL              os
               66  LOAD_METHOD              getenv
               68  LOAD_STR                 '_PYTHON_HOST_PLATFORM'
               70  LOAD_CONST               None
               72  CALL_METHOD_2         2  '2 positional arguments'
            74_76  POP_JUMP_IF_TRUE    332  'to 332'

 L.2433        78  BUILD_LIST_0          0 
               80  STORE_FAST               'args'

 L.2434        82  BUILD_LIST_0          0 
               84  STORE_FAST               'link_args'

 L.2435        86  LOAD_GLOBAL              get_platform
               88  CALL_FUNCTION_0       0  '0 positional arguments'
               90  LOAD_CONST               -4
               92  LOAD_CONST               None
               94  BUILD_SLICE_2         2 
               96  BINARY_SUBSCR    
               98  LOAD_STR                 'i386'
              100  COMPARE_OP               ==
              102  POP_JUMP_IF_TRUE    136  'to 136'
              104  LOAD_STR                 'intel'
              106  LOAD_GLOBAL              get_platform
              108  CALL_FUNCTION_0       0  '0 positional arguments'
              110  COMPARE_OP               in
              112  POP_JUMP_IF_TRUE    136  'to 136'

 L.2436       114  LOAD_STR                 'x86_64'
              116  LOAD_GLOBAL              get_platform
              118  CALL_FUNCTION_0       0  '0 positional arguments'
              120  COMPARE_OP               in
              122  POP_JUMP_IF_TRUE    136  'to 136'

 L.2437       124  LOAD_STR                 'i386'
              126  LOAD_GLOBAL              platform
              128  LOAD_METHOD              platform
              130  CALL_METHOD_0         0  '0 positional arguments'
              132  COMPARE_OP               in
              134  POP_JUMP_IF_FALSE   142  'to 142'
            136_0  COME_FROM           122  '122'
            136_1  COME_FROM           112  '112'
            136_2  COME_FROM           102  '102'

 L.2438       136  LOAD_CONST               1
              138  STORE_FAST               'intel'
              140  JUMP_FORWARD        146  'to 146'
            142_0  COME_FROM           134  '134'

 L.2440       142  LOAD_CONST               0
              144  STORE_FAST               'intel'
            146_0  COME_FROM           140  '140'

 L.2441       146  LOAD_GLOBAL              os
              148  LOAD_ATTR                path
              150  LOAD_METHOD              exists
              152  LOAD_STR                 '/System/Library/Frameworks/Accelerate.framework/'
              154  CALL_METHOD_1         1  '1 positional argument'
              156  POP_JUMP_IF_FALSE   224  'to 224'

 L.2443       158  LOAD_STR                 'accelerate'
              160  LOAD_FAST                'libraries'
              162  COMPARE_OP               in
              164  POP_JUMP_IF_FALSE   224  'to 224'

 L.2444       166  LOAD_FAST                'intel'
              168  POP_JUMP_IF_FALSE   184  'to 184'

 L.2445       170  LOAD_FAST                'args'
              172  LOAD_METHOD              extend
              174  LOAD_STR                 '-msse3'
              176  BUILD_LIST_1          1 
              178  CALL_METHOD_1         1  '1 positional argument'
              180  POP_TOP          
              182  JUMP_FORWARD        196  'to 196'
            184_0  COME_FROM           168  '168'

 L.2447       184  LOAD_FAST                'args'
              186  LOAD_METHOD              extend
              188  LOAD_STR                 '-faltivec'
              190  BUILD_LIST_1          1 
              192  CALL_METHOD_1         1  '1 positional argument'
              194  POP_TOP          
            196_0  COME_FROM           182  '182'

 L.2448       196  LOAD_FAST                'args'
              198  LOAD_METHOD              extend

 L.2449       200  LOAD_STR                 '-I/System/Library/Frameworks/vecLib.framework/Headers'
              202  BUILD_LIST_1          1 
              204  CALL_METHOD_1         1  '1 positional argument'
              206  POP_TOP          

 L.2450       208  LOAD_FAST                'link_args'
              210  LOAD_METHOD              extend
              212  LOAD_STR                 '-Wl,-framework'
              214  LOAD_STR                 '-Wl,Accelerate'
              216  BUILD_LIST_2          2 
              218  CALL_METHOD_1         1  '1 positional argument'
              220  POP_TOP          
              222  JUMP_FORWARD        306  'to 306'
            224_0  COME_FROM           164  '164'
            224_1  COME_FROM           156  '156'

 L.2451       224  LOAD_GLOBAL              os
              226  LOAD_ATTR                path
              228  LOAD_METHOD              exists
              230  LOAD_STR                 '/System/Library/Frameworks/vecLib.framework/'
              232  CALL_METHOD_1         1  '1 positional argument'
          234_236  POP_JUMP_IF_FALSE   306  'to 306'

 L.2453       238  LOAD_STR                 'veclib'
              240  LOAD_FAST                'libraries'
              242  COMPARE_OP               in
          244_246  POP_JUMP_IF_FALSE   306  'to 306'

 L.2454       248  LOAD_FAST                'intel'
          250_252  POP_JUMP_IF_FALSE   268  'to 268'

 L.2455       254  LOAD_FAST                'args'
              256  LOAD_METHOD              extend
              258  LOAD_STR                 '-msse3'
              260  BUILD_LIST_1          1 
              262  CALL_METHOD_1         1  '1 positional argument'
              264  POP_TOP          
              266  JUMP_FORWARD        280  'to 280'
            268_0  COME_FROM           250  '250'

 L.2457       268  LOAD_FAST                'args'
              270  LOAD_METHOD              extend
              272  LOAD_STR                 '-faltivec'
              274  BUILD_LIST_1          1 
              276  CALL_METHOD_1         1  '1 positional argument'
              278  POP_TOP          
            280_0  COME_FROM           266  '266'

 L.2458       280  LOAD_FAST                'args'
              282  LOAD_METHOD              extend

 L.2459       284  LOAD_STR                 '-I/System/Library/Frameworks/vecLib.framework/Headers'
              286  BUILD_LIST_1          1 
              288  CALL_METHOD_1         1  '1 positional argument'
              290  POP_TOP          

 L.2460       292  LOAD_FAST                'link_args'
              294  LOAD_METHOD              extend
              296  LOAD_STR                 '-Wl,-framework'
              298  LOAD_STR                 '-Wl,vecLib'
              300  BUILD_LIST_2          2 
              302  CALL_METHOD_1         1  '1 positional argument'
              304  POP_TOP          
            306_0  COME_FROM           244  '244'
            306_1  COME_FROM           234  '234'
            306_2  COME_FROM           222  '222'

 L.2462       306  LOAD_FAST                'args'
          308_310  POP_JUMP_IF_FALSE   332  'to 332'

 L.2463       312  LOAD_FAST                'self'
              314  LOAD_ATTR                set_info
              316  LOAD_FAST                'args'

 L.2464       318  LOAD_FAST                'link_args'

 L.2465       320  LOAD_CONST               ('NO_ATLAS_INFO', 3)

 L.2466       322  LOAD_CONST               ('HAVE_CBLAS', None)
              324  BUILD_LIST_2          2 
              326  LOAD_CONST               ('extra_compile_args', 'extra_link_args', 'define_macros')
              328  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              330  POP_TOP          
            332_0  COME_FROM           308  '308'
            332_1  COME_FROM            74  '74'
            332_2  COME_FROM            60  '60'

Parse error at or near `JUMP_FORWARD' instruction at offset 140


class blas_src_info(system_info):
    section = 'blas_src'
    dir_env_var = 'BLAS_SRC'
    notfounderror = BlasSrcNotFoundError

    def get_paths(self, section, key):
        pre_dirs = system_info.get_paths(self, section, key)
        dirs = []
        for d in pre_dirs:
            dirs.extend([d] + self.combine_paths(d, ['blas']))

        return [d for d in dirs if os.path.isdir(d)]

    def calc_info(self):
        src_dirs = self.get_src_dirs()
        src_dir = ''
        for d in src_dirs:
            if os.path.isfile(os.path.join(d, 'daxpy.f')):
                src_dir = d
                break

        if not src_dir:
            return
        blas1 = '\n        caxpy csscal dnrm2 dzasum saxpy srotg zdotc ccopy cswap drot\n        dznrm2 scasum srotm zdotu cdotc dasum drotg icamax scnrm2\n        srotmg zdrot cdotu daxpy drotm idamax scopy sscal zdscal crotg\n        dcabs1 drotmg isamax sdot sswap zrotg cscal dcopy dscal izamax\n        snrm2 zaxpy zscal csrot ddot dswap sasum srot zcopy zswap\n        scabs1\n        '
        blas2 = '\n        cgbmv chpmv ctrsv dsymv dtrsv sspr2 strmv zhemv ztpmv cgemv\n        chpr dgbmv dsyr lsame ssymv strsv zher ztpsv cgerc chpr2 dgemv\n        dsyr2 sgbmv ssyr xerbla zher2 ztrmv cgeru ctbmv dger dtbmv\n        sgemv ssyr2 zgbmv zhpmv ztrsv chbmv ctbsv dsbmv dtbsv sger\n        stbmv zgemv zhpr chemv ctpmv dspmv dtpmv ssbmv stbsv zgerc\n        zhpr2 cher ctpsv dspr dtpsv sspmv stpmv zgeru ztbmv cher2\n        ctrmv dspr2 dtrmv sspr stpsv zhbmv ztbsv\n        '
        blas3 = '\n        cgemm csymm ctrsm dsyrk sgemm strmm zhemm zsyr2k chemm csyr2k\n        dgemm dtrmm ssymm strsm zher2k zsyrk cher2k csyrk dsymm dtrsm\n        ssyr2k zherk ztrmm cherk ctrmm dsyr2k ssyrk zgemm zsymm ztrsm\n        '
        sources = [os.path.join(src_dir, f + '.f') for f in (blas1 + blas2 + blas3).split()]
        sources = [f for f in sources if os.path.isfile(f)]
        info = {'sources':sources,  'language':'f77'}
        (self.set_info)(**info)


class x11_info(system_info):
    section = 'x11'
    notfounderror = X11NotFoundError
    _lib_names = ['X11']

    def __init__(self):
        system_info.__init__(self, default_lib_dirs=default_x11_lib_dirs,
          default_include_dirs=default_x11_include_dirs)

    def calc_info(self):
        if sys.platform in ('win32', ):
            return
        lib_dirs = self.get_lib_dirs()
        include_dirs = self.get_include_dirs()
        opt = self.get_option_single('x11_libs', 'libraries')
        x11_libs = self.get_libs(opt, self._lib_names)
        info = self.check_libs(lib_dirs, x11_libs, [])
        if info is None:
            return
        inc_dir = None
        for d in include_dirs:
            if self.combine_paths(d, 'X11/X.h'):
                inc_dir = d
                break

        if inc_dir is not None:
            dict_append(info, include_dirs=[inc_dir])
        (self.set_info)(**info)


class _numpy_info(system_info):
    section = 'Numeric'
    modulename = 'Numeric'
    notfounderror = NumericNotFoundError

    def __init__(self):
        include_dirs = []
        try:
            module = __import__(self.modulename)
            prefix = []
            for name in module.__file__.split(os.sep):
                if name == 'lib':
                    break
                prefix.append(name)

            try:
                include_dirs.append(getattr(module, 'get_include')())
            except AttributeError:
                pass

            include_dirs.append(sysconfig.get_path('include'))
        except ImportError:
            pass

        py_incl_dir = sysconfig.get_path('include')
        include_dirs.append(py_incl_dir)
        py_pincl_dir = sysconfig.get_path('platinclude')
        if py_pincl_dir not in include_dirs:
            include_dirs.append(py_pincl_dir)
        for d in default_include_dirs:
            d = os.path.join(d, os.path.basename(py_incl_dir))
            if d not in include_dirs:
                include_dirs.append(d)

        system_info.__init__(self, default_lib_dirs=[], default_include_dirs=include_dirs)

    def calc_info(self):
        try:
            module = __import__(self.modulename)
        except ImportError:
            return
        else:
            info = {}
            macros = []
            for v in ('__version__', 'version'):
                vrs = getattr(module, v, None)
                if vrs is None:
                    continue
                macros = [
                 (
                  self.modulename.upper() + '_VERSION',
                  _c_string_literal(vrs)),
                 (
                  self.modulename.upper(), None)]
                break

            dict_append(info, define_macros=macros)
            include_dirs = self.get_include_dirs()
            inc_dir = None
            for d in include_dirs:
                if self.combine_paths(d, os.path.join(self.modulename, 'arrayobject.h')):
                    inc_dir = d
                    break

            if inc_dir is not None:
                dict_append(info, include_dirs=[inc_dir])
            if info:
                (self.set_info)(**info)


class numarray_info(_numpy_info):
    section = 'numarray'
    modulename = 'numarray'


class Numeric_info(_numpy_info):
    section = 'Numeric'
    modulename = 'Numeric'


class numpy_info(_numpy_info):
    section = 'numpy'
    modulename = 'numpy'


class numerix_info(system_info):
    section = 'numerix'

    def calc_info(self):
        which = (None, None)
        if os.getenv('NUMERIX'):
            which = (
             os.getenv('NUMERIX'), 'environment var')
        if which[0] is None:
            which = ('numpy', 'defaulted')
            try:
                import numpy
                which = ('numpy', 'defaulted')
            except ImportError as e:
                try:
                    msg1 = str(e)
                    try:
                        import Numeric
                        which = ('numeric', 'defaulted')
                    except ImportError as e:
                        try:
                            msg2 = str(e)
                            try:
                                import numarray
                                which = ('numarray', 'defaulted')
                            except ImportError as e:
                                try:
                                    msg3 = str(e)
                                    log.info(msg1)
                                    log.info(msg2)
                                    log.info(msg3)
                                finally:
                                    e = None
                                    del e

                        finally:
                            e = None
                            del e

                finally:
                    e = None
                    del e

        which = (
         which[0].strip().lower(), which[1])
        if which[0] not in ('numeric', 'numarray', 'numpy'):
            raise ValueError("numerix selector must be either 'Numeric' or 'numarray' or 'numpy' but the value obtained from the %s was '%s'." % (
             which[1], which[0]))
        os.environ['NUMERIX'] = which[0]
        (self.set_info)(**get_info(which[0]))


class f2py_info(system_info):

    def calc_info(self):
        try:
            import numpy.f2py as f2py
        except ImportError:
            return
        else:
            f2py_dir = os.path.join(os.path.dirname(f2py.__file__), 'src')
            self.set_info(sources=[os.path.join(f2py_dir, 'fortranobject.c')], include_dirs=[
             f2py_dir])


class boost_python_info(system_info):
    section = 'boost_python'
    dir_env_var = 'BOOST'

    def get_paths(self, section, key):
        pre_dirs = system_info.get_paths(self, section, key)
        dirs = []
        for d in pre_dirs:
            dirs.extend([d] + self.combine_paths(d, ['boost*']))

        return [d for d in dirs if os.path.isdir(d)]

    def calc_info(self):
        src_dirs = self.get_src_dirs()
        src_dir = ''
        for d in src_dirs:
            if os.path.isfile(os.path.join(d, 'libs', 'python', 'src', 'module.cpp')):
                src_dir = d
                break

        if not src_dir:
            return
        py_incl_dirs = [
         sysconfig.get_path('include')]
        py_pincl_dir = sysconfig.get_path('platinclude')
        if py_pincl_dir not in py_incl_dirs:
            py_incl_dirs.append(py_pincl_dir)
        srcs_dir = os.path.join(src_dir, 'libs', 'python', 'src')
        bpl_srcs = glob(os.path.join(srcs_dir, '*.cpp'))
        bpl_srcs += glob(os.path.join(srcs_dir, '*', '*.cpp'))
        info = {'libraries':[
          ('boost_python_src',
           {'include_dirs':[
             src_dir] + py_incl_dirs, 
            'sources':bpl_srcs})], 
         'include_dirs':[
          src_dir]}
        if info:
            (self.set_info)(**info)


class agg2_info(system_info):
    section = 'agg2'
    dir_env_var = 'AGG2'

    def get_paths(self, section, key):
        pre_dirs = system_info.get_paths(self, section, key)
        dirs = []
        for d in pre_dirs:
            dirs.extend([d] + self.combine_paths(d, ['agg2*']))

        return [d for d in dirs if os.path.isdir(d)]

    def calc_info(self):
        src_dirs = self.get_src_dirs()
        src_dir = ''
        for d in src_dirs:
            if os.path.isfile(os.path.join(d, 'src', 'agg_affine_matrix.cpp')):
                src_dir = d
                break

        if not src_dir:
            return
        if sys.platform == 'win32':
            agg2_srcs = glob(os.path.join(src_dir, 'src', 'platform', 'win32', 'agg_win32_bmp.cpp'))
        else:
            agg2_srcs = glob(os.path.join(src_dir, 'src', '*.cpp'))
            agg2_srcs += [
             os.path.join(src_dir, 'src', 'platform', 'X11', 'agg_platform_support.cpp')]
        info = {'libraries':[
          (
           'agg2_src',
           {'sources':agg2_srcs, 
            'include_dirs':[
             os.path.join(src_dir, 'include')]})], 
         'include_dirs':[
          os.path.join(src_dir, 'include')]}
        if info:
            (self.set_info)(**info)


class _pkg_config_info(system_info):
    section = None
    config_env_var = 'PKG_CONFIG'
    default_config_exe = 'pkg-config'
    append_config_exe = ''
    version_macro_name = None
    release_macro_name = None
    version_flag = '--modversion'
    cflags_flag = '--cflags'

    def get_config_exe(self):
        if self.config_env_var in os.environ:
            return os.environ[self.config_env_var]
        return self.default_config_exe

    def get_config_output(self, config_exe, option):
        cmd = config_exe + ' ' + self.append_config_exe + ' ' + option
        try:
            o = subprocess.check_output(cmd)
        except (OSError, subprocess.CalledProcessError):
            pass
        else:
            o = filepath_from_subprocess_output(o)
            return o

    def calc_info(self):
        config_exe = find_executable(self.get_config_exe())
        if not config_exe:
            log.warn('File not found: %s. Cannot determine %s info.' % (
             config_exe, self.section))
            return
        info = {}
        macros = []
        libraries = []
        library_dirs = []
        include_dirs = []
        extra_link_args = []
        extra_compile_args = []
        version = self.get_config_output(config_exe, self.version_flag)
        if version:
            macros.append((self.__class__.__name__.split('.')[(-1)].upper(),
             _c_string_literal(version)))
            if self.version_macro_name:
                macros.append((
                 self.version_macro_name + '_%s' % version.replace('.', '_'), None))
        if self.release_macro_name:
            release = self.get_config_output(config_exe, '--release')
            if release:
                macros.append((
                 self.release_macro_name + '_%s' % release.replace('.', '_'), None))
        opts = self.get_config_output(config_exe, '--libs')
        if opts:
            for opt in opts.split():
                if opt[:2] == '-l':
                    libraries.append(opt[2:])
                elif opt[:2] == '-L':
                    library_dirs.append(opt[2:])
                else:
                    extra_link_args.append(opt)

        opts = self.get_config_output(config_exe, self.cflags_flag)
        if opts:
            for opt in opts.split():
                if opt[:2] == '-I':
                    include_dirs.append(opt[2:])
                elif opt[:2] == '-D':
                    if '=' in opt:
                        n, v = opt[2:].split('=')
                        macros.append((n, v))
                    else:
                        macros.append((opt[2:], None))
                else:
                    extra_compile_args.append(opt)

        if macros:
            dict_append(info, define_macros=macros)
        if libraries:
            dict_append(info, libraries=libraries)
        if library_dirs:
            dict_append(info, library_dirs=library_dirs)
        if include_dirs:
            dict_append(info, include_dirs=include_dirs)
        if extra_link_args:
            dict_append(info, extra_link_args=extra_link_args)
        if extra_compile_args:
            dict_append(info, extra_compile_args=extra_compile_args)
        if info:
            (self.set_info)(**info)


class wx_info(_pkg_config_info):
    section = 'wx'
    config_env_var = 'WX_CONFIG'
    default_config_exe = 'wx-config'
    append_config_exe = ''
    version_macro_name = 'WX_VERSION'
    release_macro_name = 'WX_RELEASE'
    version_flag = '--version'
    cflags_flag = '--cxxflags'


class gdk_pixbuf_xlib_2_info(_pkg_config_info):
    section = 'gdk_pixbuf_xlib_2'
    append_config_exe = 'gdk-pixbuf-xlib-2.0'
    version_macro_name = 'GDK_PIXBUF_XLIB_VERSION'


class gdk_pixbuf_2_info(_pkg_config_info):
    section = 'gdk_pixbuf_2'
    append_config_exe = 'gdk-pixbuf-2.0'
    version_macro_name = 'GDK_PIXBUF_VERSION'


class gdk_x11_2_info(_pkg_config_info):
    section = 'gdk_x11_2'
    append_config_exe = 'gdk-x11-2.0'
    version_macro_name = 'GDK_X11_VERSION'


class gdk_2_info(_pkg_config_info):
    section = 'gdk_2'
    append_config_exe = 'gdk-2.0'
    version_macro_name = 'GDK_VERSION'


class gdk_info(_pkg_config_info):
    section = 'gdk'
    append_config_exe = 'gdk'
    version_macro_name = 'GDK_VERSION'


class gtkp_x11_2_info(_pkg_config_info):
    section = 'gtkp_x11_2'
    append_config_exe = 'gtk+-x11-2.0'
    version_macro_name = 'GTK_X11_VERSION'


class gtkp_2_info(_pkg_config_info):
    section = 'gtkp_2'
    append_config_exe = 'gtk+-2.0'
    version_macro_name = 'GTK_VERSION'


class xft_info(_pkg_config_info):
    section = 'xft'
    append_config_exe = 'xft'
    version_macro_name = 'XFT_VERSION'


class freetype2_info(_pkg_config_info):
    section = 'freetype2'
    append_config_exe = 'freetype2'
    version_macro_name = 'FREETYPE2_VERSION'


class amd_info(system_info):
    section = 'amd'
    dir_env_var = 'AMD'
    _lib_names = ['amd']

    def calc_info(self):
        lib_dirs = self.get_lib_dirs()
        opt = self.get_option_single('amd_libs', 'libraries')
        amd_libs = self.get_libs(opt, self._lib_names)
        info = self.check_libs(lib_dirs, amd_libs, [])
        if info is None:
            return
        include_dirs = self.get_include_dirs()
        inc_dir = None
        for d in include_dirs:
            p = self.combine_paths(d, 'amd.h')
            if p:
                inc_dir = os.path.dirname(p[0])
                break

        if inc_dir is not None:
            dict_append(info, include_dirs=[inc_dir], define_macros=[
             ('SCIPY_AMD_H', None)],
              swig_opts=[
             '-I' + inc_dir])
        (self.set_info)(**info)


class umfpack_info(system_info):
    section = 'umfpack'
    dir_env_var = 'UMFPACK'
    notfounderror = UmfpackNotFoundError
    _lib_names = ['umfpack']

    def calc_info(self):
        lib_dirs = self.get_lib_dirs()
        opt = self.get_option_single('umfpack_libs', 'libraries')
        umfpack_libs = self.get_libs(opt, self._lib_names)
        info = self.check_libs(lib_dirs, umfpack_libs, [])
        if info is None:
            return
        include_dirs = self.get_include_dirs()
        inc_dir = None
        for d in include_dirs:
            p = self.combine_paths(d, ['', 'umfpack'], 'umfpack.h')
            if p:
                inc_dir = os.path.dirname(p[0])
                break

        if inc_dir is not None:
            dict_append(info, include_dirs=[inc_dir], define_macros=[
             ('SCIPY_UMFPACK_H', None)],
              swig_opts=[
             '-I' + inc_dir])
        dict_append(info, **get_info('amd'))
        (self.set_info)(**info)


def combine_paths(*args, **kws):
    """ Return a list of existing paths composed by all combinations of
        items from arguments.
    """
    r = []
    for a in args:
        if not a:
            continue
        if is_string(a):
            a = [
             a]
        r.append(a)

    args = r
    if not args:
        return []
    elif len(args) == 1:
        result = reduce(lambda a, b: a + b, map(glob, args[0]), [])
    else:
        if len(args) == 2:
            result = []
            for a0 in args[0]:
                for a1 in args[1]:
                    result.extend(glob(os.path.join(a0, a1)))

        else:
            result = combine_paths(*combine_paths(args[0], args[1]) + args[2:])
    log.debug('(paths: %s)', ','.join(result))
    return result


language_map = {'c':0, 
 'c++':1,  'f77':2,  'f90':3}
inv_language_map = {0:'c',  1:'c++',  2:'f77',  3:'f90'}

def dict_append(d, **kws):
    languages = []
    for k, v in kws.items():
        if k == 'language':
            languages.append(v)
            continue
        if k in d:
            if k in ('library_dirs', 'include_dirs', 'extra_compile_args', 'extra_link_args',
                     'runtime_library_dirs', 'define_macros'):
                [d[k].append(vv) for vv in v if vv not in d[k]]
            else:
                d[k].extend(v)
        else:
            d[k] = v

    if languages:
        l = inv_language_map[max([language_map.get(l, 0) for l in languages])]
        d['language'] = l


def parseCmdLine(argv=(None,)):
    import optparse
    parser = optparse.OptionParser('usage: %prog [-v] [info objs]')
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose', default=False,
      help='be verbose and print more messages')
    opts, args = parser.parse_args(args=(argv[1:]))
    return (opts, args)


def show_all(argv=None):
    import inspect
    if argv is None:
        argv = sys.argv
    else:
        opts, args = parseCmdLine(argv)
        if opts.verbose:
            log.set_threshold(log.DEBUG)
        else:
            log.set_threshold(log.INFO)
    show_only = []
    for n in args:
        if n[-5:] != '_info':
            n = n + '_info'
        show_only.append(n)

    show_all = not show_only
    _gdict_ = globals().copy()
    for name, c in _gdict_.items():
        if not inspect.isclass(c):
            continue
        if issubclass(c, system_info):
            if c is system_info:
                continue
            if not show_all:
                if name not in show_only:
                    continue
                del show_only[show_only.index(name)]
            conf = c()
            conf.verbosity = 2
            r = conf.get_info()

    if show_only:
        log.info('Info classes not defined: %s', ','.join(show_only))


if __name__ == '__main__':
    show_all()