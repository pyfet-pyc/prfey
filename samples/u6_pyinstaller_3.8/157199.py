# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\numpy\distutils\ccompiler_opt.py
"""Provides the `CCompilerOpt` class, used for handling the CPU/hardware
optimization, starting from parsing the command arguments, to managing the
relation between the CPU baseline and dispatch-able features,
also generating the required C headers and ending with compiling
the sources with proper compiler's flags.

`CCompilerOpt` doesn't provide runtime detection for the CPU features,
instead only focuses on the compiler side, but it creates abstract C headers
that can be used later for the final runtime dispatching process."""
import sys, io, os, re, textwrap, pprint, inspect, atexit, subprocess

class _Config:
    __doc__ = 'An abstract class holds all configurable attributes of `CCompilerOpt`,\n    these class attributes can be used to change the default behavior\n    of `CCompilerOpt` in order to fit other requirements.\n\n    Attributes\n    ----------\n    conf_nocache : bool\n        Set True to disable memory and file cache.\n        Default is False.\n\n    conf_noopt : bool\n        Set True to forces the optimization to be disabled,\n        in this case `CCompilerOpt` tends to generate all\n        expected headers in order to \'not\' break the build.\n        Default is False.\n\n    conf_cache_factors : list\n        Add extra factors to the primary caching factors. The caching factors\n        are utilized to determine if there are changes had happened that\n        requires to discard the cache and re-updating it. The primary factors\n        are the arguments of `CCompilerOpt` and `CCompiler`\'s properties(type, flags, etc).\n        Default is list of two items, containing the time of last modification\n        of `ccompiler_opt` and value of attribute "conf_noopt"\n\n    conf_tmp_path : str,\n        The path of temporary directory. Default is auto-created\n        temporary directory via ``tempfile.mkdtemp()``.\n\n    conf_check_path : str\n        The path of testing files. Each added CPU feature must have a\n        **C** source file contains at least one intrinsic or instruction that\n        related to this feature, so it can be tested against the compiler.\n        Default is ``./distutils/checks``.\n\n    conf_target_groups : dict\n        Extra tokens that can be reached from dispatch-able sources through\n        the special mark ``@targets``. Default is an empty dictionary.\n\n        **Notes**:\n            - case-insensitive for tokens and group names\n            - sign \'#\' must stick in the begin of group name and only within ``@targets``\n\n        **Example**:\n            .. code-block:: console\n\n                $ "@targets #avx_group other_tokens" > group_inside.c\n\n            >>> CCompilerOpt.conf_target_groups["avx_group"] = \\\n            "$werror $maxopt avx2 avx512f avx512_skx"\n            >>> cco = CCompilerOpt(cc_instance)\n            >>> cco.try_dispatch(["group_inside.c"])\n\n    conf_c_prefix : str\n        The prefix of public C definitions. Default is ``"NPY_"``.\n\n    conf_c_prefix_ : str\n        The prefix of internal C definitions. Default is ``"NPY__"``.\n\n    conf_cc_flags : dict\n        Nested dictionaries defining several compiler flags\n        that linked to some major functions, the main key\n        represent the compiler name and sub-keys represent\n        flags names. Default is already covers all supported\n        **C** compilers.\n\n        Sub-keys explained as follows:\n\n        "native": str or None\n            used by argument option `native`, to detect the current\n            machine support via the compiler.\n        "werror": str or None\n            utilized to treat warning as errors during testing CPU features\n            against the compiler and also for target\'s policy `$werror`\n            via dispatch-able sources.\n        "maxopt": str or None\n            utilized for target\'s policy \'$maxopt\' and the value should\n            contains the maximum acceptable optimization by the compiler.\n            e.g. in gcc `\'-O3\'`\n\n        **Notes**:\n            * case-sensitive for compiler names and flags\n            * use space to separate multiple flags\n            * any flag will tested against the compiler and it will skipped\n              if it\'s not applicable.\n\n    conf_min_features : dict\n        A dictionary defines the used CPU features for\n        argument option `\'min\'`, the key represent the CPU architecture\n        name e.g. `\'x86\'`. Default values provide the best effort\n        on wide range of users platforms.\n\n        **Note**: case-sensitive for architecture names.\n\n    conf_features : dict\n        Nested dictionaries used for identifying the CPU features.\n        the primary key is represented as a feature name or group name\n        that gathers several features. Default values covers all\n        supported features but without the major options like "flags",\n        these undefined options handle it by method `conf_features_partial()`.\n        Default value is covers almost all CPU features for *X86*, *IBM/Power64*\n        and *ARM 7/8*.\n\n        Sub-keys explained as follows:\n\n        "implies" : str or list, optional,\n            List of CPU feature names to be implied by it,\n            the feature name must be defined within `conf_features`.\n            Default is None.\n\n        "flags": str or list, optional\n            List of compiler flags. Default is None.\n\n        "detect": str or list, optional\n            List of CPU feature names that required to be detected\n            in runtime. By default, its the feature name or features\n            in "group" if its specified.\n\n        "implies_detect": bool, optional\n            If True, all "detect" of implied features will be combined.\n            Default is True. see `feature_detect()`.\n\n        "group": str or list, optional\n            Same as "implies" but doesn\'t require the feature name to be\n            defined within `conf_features`.\n\n        "interest": int, required\n            a key for sorting CPU features\n\n        "headers": str or list, optional\n            intrinsics C header file\n\n        "disable": str, optional\n            force disable feature, the string value should contains the\n            reason of disabling.\n\n        "autovec": bool or None, optional\n            True or False to declare that CPU feature can be auto-vectorized\n            by the compiler.\n            By default(None), treated as True if the feature contains at\n            least one applicable flag. see `feature_can_autovec()`\n\n        "extra_checks": str or list, optional\n            Extra test case names for the CPU feature that need to be tested\n            against the compiler.\n\n            Each test case must have a C file named ``extra_xxxx.c``, where\n            ``xxxx`` is the case name in lower case, under \'conf_check_path\'.\n            It should contain at least one intrinsic or function related to the test case.\n\n            If the compiler able to successfully compile the C file then `CCompilerOpt`\n            will add a C ``#define`` for it into the main dispatch header, e.g.\n            ```#define {conf_c_prefix}_XXXX`` where ``XXXX`` is the case name in upper case.\n\n        **NOTES**:\n            * space can be used as separator with options that supports "str or list"\n            * case-sensitive for all values and feature name must be in upper-case.\n            * if flags aren\'t applicable, its will skipped rather than disable the\n              CPU feature\n            * the CPU feature will disabled if the compiler fail to compile\n              the test file\n    '
    conf_nocache = False
    conf_noopt = False
    conf_cache_factors = None
    conf_tmp_path = None
    conf_check_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'checks')
    conf_target_groups = {}
    conf_c_prefix = 'NPY_'
    conf_c_prefix_ = 'NPY__'
    conf_cc_flags = dict(gcc=dict(native='-march=native',
      opt='-O3',
      werror='-Werror'),
      clang=dict(native='-march=native',
      opt='-O3',
      werror='-Werror'),
      icc=dict(native='-xHost',
      opt='-O3',
      werror='-Werror'),
      iccw=dict(native='/QxHost',
      opt='/O3',
      werror='/Werror'),
      msvc=dict(native=None,
      opt='/O2',
      werror='/WX'))
    conf_min_features = dict(x86='SSE SSE2',
      x64='SSE SSE2 SSE3',
      ppc64='',
      ppc64le='VSX VSX2',
      armhf='',
      aarch64='NEON NEON_FP16 NEON_VFPV4 ASIMD')
    conf_features = dict(SSE=dict(interest=1,
      headers='xmmintrin.h',
      implies='SSE2'),
      SSE2=dict(interest=2, implies='SSE', headers='emmintrin.h'),
      SSE3=dict(interest=3, implies='SSE2', headers='pmmintrin.h'),
      SSSE3=dict(interest=4, implies='SSE3', headers='tmmintrin.h'),
      SSE41=dict(interest=5, implies='SSSE3', headers='smmintrin.h'),
      POPCNT=dict(interest=6, implies='SSE41', headers='popcntintrin.h'),
      SSE42=dict(interest=7, implies='POPCNT'),
      AVX=dict(interest=8,
      implies='SSE42',
      headers='immintrin.h',
      implies_detect=False),
      XOP=dict(interest=9, implies='AVX', headers='x86intrin.h'),
      FMA4=dict(interest=10, implies='AVX', headers='x86intrin.h'),
      F16C=dict(interest=11, implies='AVX'),
      FMA3=dict(interest=12, implies='F16C'),
      AVX2=dict(interest=13, implies='F16C'),
      AVX512F=dict(interest=20,
      implies='FMA3 AVX2',
      implies_detect=False,
      extra_checks='AVX512F_REDUCE'),
      AVX512CD=dict(interest=21, implies='AVX512F'),
      AVX512_KNL=dict(interest=40,
      implies='AVX512CD',
      group='AVX512ER AVX512PF',
      detect='AVX512_KNL',
      implies_detect=False),
      AVX512_KNM=dict(interest=41,
      implies='AVX512_KNL',
      group='AVX5124FMAPS AVX5124VNNIW AVX512VPOPCNTDQ',
      detect='AVX512_KNM',
      implies_detect=False),
      AVX512_SKX=dict(interest=42,
      implies='AVX512CD',
      group='AVX512VL AVX512BW AVX512DQ',
      detect='AVX512_SKX',
      implies_detect=False,
      extra_checks='AVX512BW_MASK AVX512DQ_MASK'),
      AVX512_CLX=dict(interest=43,
      implies='AVX512_SKX',
      group='AVX512VNNI',
      detect='AVX512_CLX'),
      AVX512_CNL=dict(interest=44,
      implies='AVX512_SKX',
      group='AVX512IFMA AVX512VBMI',
      detect='AVX512_CNL',
      implies_detect=False),
      AVX512_ICL=dict(interest=45,
      implies='AVX512_CLX AVX512_CNL',
      group='AVX512VBMI2 AVX512BITALG AVX512VPOPCNTDQ',
      detect='AVX512_ICL',
      implies_detect=False),
      VSX=dict(interest=1, headers='altivec.h'),
      VSX2=dict(interest=2, implies='VSX', implies_detect=False),
      VSX3=dict(interest=3, implies='VSX2', implies_detect=False),
      NEON=dict(interest=1, headers='arm_neon.h'),
      NEON_FP16=dict(interest=2, implies='NEON'),
      NEON_VFPV4=dict(interest=3, implies='NEON_FP16'),
      ASIMD=dict(interest=4, implies='NEON_FP16 NEON_VFPV4', implies_detect=False),
      ASIMDHP=dict(interest=5, implies='ASIMD'),
      ASIMDDP=dict(interest=6, implies='ASIMD'),
      ASIMDFHM=dict(interest=7, implies='ASIMDHP'))

    def conf_features_partial(self):
        """Return a dictionary of supported CPU features by the platform,
        and accumulate the rest of undefined options in `conf_features`,
        the returned dict has same rules and notes in
        class attribute `conf_features`, also its override
        any options that been set in 'conf_features'.
        """
        if self.cc_noopt:
            return {}
            on_x86 = self.cc_on_x86 or self.cc_on_x64
            is_unix = self.cc_is_gcc or self.cc_is_clang
            if on_x86:
                if is_unix:
                    return dict(SSE=dict(flags='-msse'),
                      SSE2=dict(flags='-msse2'),
                      SSE3=dict(flags='-msse3'),
                      SSSE3=dict(flags='-mssse3'),
                      SSE41=dict(flags='-msse4.1'),
                      POPCNT=dict(flags='-mpopcnt'),
                      SSE42=dict(flags='-msse4.2'),
                      AVX=dict(flags='-mavx'),
                      F16C=dict(flags='-mf16c'),
                      XOP=dict(flags='-mxop'),
                      FMA4=dict(flags='-mfma4'),
                      FMA3=dict(flags='-mfma'),
                      AVX2=dict(flags='-mavx2'),
                      AVX512F=dict(flags='-mavx512f'),
                      AVX512CD=dict(flags='-mavx512cd'),
                      AVX512_KNL=dict(flags='-mavx512er -mavx512pf'),
                      AVX512_KNM=dict(flags='-mavx5124fmaps -mavx5124vnniw -mavx512vpopcntdq'),
                      AVX512_SKX=dict(flags='-mavx512vl -mavx512bw -mavx512dq'),
                      AVX512_CLX=dict(flags='-mavx512vnni'),
                      AVX512_CNL=dict(flags='-mavx512ifma -mavx512vbmi'),
                      AVX512_ICL=dict(flags='-mavx512vbmi2 -mavx512bitalg -mavx512vpopcntdq'))
            if on_x86:
                if self.cc_is_icc:
                    return dict(SSE=dict(flags='-msse'),
                      SSE2=dict(flags='-msse2'),
                      SSE3=dict(flags='-msse3'),
                      SSSE3=dict(flags='-mssse3'),
                      SSE41=dict(flags='-msse4.1'),
                      POPCNT={},
                      SSE42=dict(flags='-msse4.2'),
                      AVX=dict(flags='-mavx'),
                      F16C={},
                      XOP=dict(disable="Intel Compiler doesn't support it"),
                      FMA4=dict(disable="Intel Compiler doesn't support it"),
                      FMA3=dict(implies='F16C AVX2',
                      flags='-march=core-avx2'),
                      AVX2=dict(implies='FMA3', flags='-march=core-avx2'),
                      AVX512F=dict(implies='AVX2 AVX512CD',
                      flags='-march=common-avx512'),
                      AVX512CD=dict(implies='AVX2 AVX512F',
                      flags='-march=common-avx512'),
                      AVX512_KNL=dict(flags='-xKNL'),
                      AVX512_KNM=dict(flags='-xKNM'),
                      AVX512_SKX=dict(flags='-xSKYLAKE-AVX512'),
                      AVX512_CLX=dict(flags='-xCASCADELAKE'),
                      AVX512_CNL=dict(flags='-xCANNONLAKE'),
                      AVX512_ICL=dict(flags='-xICELAKE-CLIENT'))
            if on_x86:
                if self.cc_is_iccw:
                    return dict(SSE=dict(flags='/arch:SSE'),
                      SSE2=dict(flags='/arch:SSE2'),
                      SSE3=dict(flags='/arch:SSE3'),
                      SSSE3=dict(flags='/arch:SSSE3'),
                      SSE41=dict(flags='/arch:SSE4.1'),
                      POPCNT={},
                      SSE42=dict(flags='/arch:SSE4.2'),
                      AVX=dict(flags='/arch:AVX'),
                      F16C={},
                      XOP=dict(disable="Intel Compiler doesn't support it"),
                      FMA4=dict(disable="Intel Compiler doesn't support it"),
                      FMA3=dict(implies='F16C AVX2',
                      flags='/arch:CORE-AVX2'),
                      AVX2=dict(implies='FMA3',
                      flags='/arch:CORE-AVX2'),
                      AVX512F=dict(implies='AVX2 AVX512CD',
                      flags='/Qx:COMMON-AVX512'),
                      AVX512CD=dict(implies='AVX2 AVX512F',
                      flags='/Qx:COMMON-AVX512'),
                      AVX512_KNL=dict(flags='/Qx:KNL'),
                      AVX512_KNM=dict(flags='/Qx:KNM'),
                      AVX512_SKX=dict(flags='/Qx:SKYLAKE-AVX512'),
                      AVX512_CLX=dict(flags='/Qx:CASCADELAKE'),
                      AVX512_CNL=dict(flags='/Qx:CANNONLAKE'),
                      AVX512_ICL=dict(flags='/Qx:ICELAKE-CLIENT'))
            if on_x86:
                if self.cc_is_msvc:
                    return dict(SSE=dict(flags='/arch:SSE'),
                      SSE2=dict(flags='/arch:SSE2'),
                      SSE3={},
                      SSSE3={},
                      SSE41={},
                      POPCNT=dict(headers='nmmintrin.h'),
                      SSE42={},
                      AVX=dict(flags='/arch:AVX'),
                      F16C={},
                      XOP=dict(headers='ammintrin.h'),
                      FMA4=dict(headers='ammintrin.h'),
                      FMA3=dict(implies='F16C AVX2',
                      flags='/arch:AVX2'),
                      AVX2=dict(implies='F16C FMA3',
                      flags='/arch:AVX2'),
                      AVX512F=dict(implies='AVX2 AVX512CD AVX512_SKX',
                      flags='/arch:AVX512'),
                      AVX512CD=dict(implies='AVX512F AVX512_SKX',
                      flags='/arch:AVX512'),
                      AVX512_KNL=dict(disable="MSVC compiler doesn't support it"),
                      AVX512_KNM=dict(disable="MSVC compiler doesn't support it"),
                      AVX512_SKX=dict(flags='/arch:AVX512'),
                      AVX512_CLX={},
                      AVX512_CNL={},
                      AVX512_ICL={})
            on_power = self.cc_on_ppc64le or self.cc_on_ppc64
            if on_power:
                partial = dict(VSX=dict(implies=('VSX2' if self.cc_on_ppc64le else ''),
                  flags='-mvsx'),
                  VSX2=dict(flags='-mcpu=power8',
                  implies_detect=False),
                  VSX3=dict(flags='-mcpu=power9 -mtune=power9',
                  implies_detect=False))
                if self.cc_is_clang:
                    partial['VSX']['flags'] = '-maltivec -mvsx'
                    partial['VSX2']['flags'] = '-mpower8-vector'
                    partial['VSX3']['flags'] = '-mpower9-vector'
                return partial
        else:
            if self.cc_on_aarch64:
                if is_unix:
                    return dict(NEON=dict(implies='NEON_FP16 NEON_VFPV4 ASIMD',
                      autovec=True),
                      NEON_FP16=dict(implies='NEON NEON_VFPV4 ASIMD',
                      autovec=True),
                      NEON_VFPV4=dict(implies='NEON NEON_FP16 ASIMD',
                      autovec=True),
                      ASIMD=dict(implies='NEON NEON_FP16 NEON_VFPV4',
                      autovec=True),
                      ASIMDHP=dict(flags='-march=armv8.2-a+fp16'),
                      ASIMDDP=dict(flags='-march=armv8.2-a+dotprod'),
                      ASIMDFHM=dict(flags='-march=armv8.2-a+fp16fml'))
            if self.cc_on_armhf and is_unix:
                return dict(NEON=dict(flags='-mfpu=neon'),
                  NEON_FP16=dict(flags='-mfpu=neon-fp16 -mfp16-format=ieee'),
                  NEON_VFPV4=dict(flags='-mfpu=neon-vfpv4'),
                  ASIMD=dict(flags='-mfpu=neon-fp-armv8 -march=armv8-a+simd'),
                  ASIMDHP=dict(flags='-march=armv8.2-a+fp16'),
                  ASIMDDP=dict(flags='-march=armv8.2-a+dotprod'),
                  ASIMDFHM=dict(flags='-march=armv8.2-a+fp16fml'))
        return {}

    def __init__(self):
        if self.conf_tmp_path is None:
            import tempfile, shutil
            tmp = tempfile.mkdtemp()

            def rm_temp():
                try:
                    shutil.rmtree(tmp)
                except IOError:
                    pass

            atexit.register(rm_temp)
            self.conf_tmp_path = tmp
        if self.conf_cache_factors is None:
            self.conf_cache_factors = [os.path.getmtime(__file__),
             self.conf_nocache]


class _Distutils:
    __doc__ = "A helper class that provides a collection of fundamental methods\n    implemented in a top of Python and NumPy Distutils.\n\n    The idea behind this class is to gather all methods that it may\n    need to override in case of reuse 'CCompilerOpt' in environment\n    different than of what NumPy has.\n\n    Parameters\n    ----------\n    ccompiler : `CCompiler`\n        The generate instance that returned from `distutils.ccompiler.new_compiler()`.\n    "

    def __init__(self, ccompiler):
        self._ccompiler = ccompiler

    def dist_compile(self, sources, flags, **kwargs):
        """Wrap CCompiler.compile()"""
        assert isinstance(sources, list)
        assert isinstance(flags, list)
        flags = kwargs.pop('extra_postargs', []) + flags
        return (self._ccompiler.compile)(
 sources, extra_postargs=flags, **kwargs)

    def dist_test(self, source, flags):
        """Return True if 'CCompiler.compile()' able to compile
        a source file with certain flags.
        """
        if not isinstance(source, str):
            raise AssertionError
        else:
            from distutils.errors import CompileError
            cc = self._ccompiler
            bk_spawn = getattr(cc, 'spawn', None)
            if bk_spawn:
                cc_type = getattr(self._ccompiler, 'compiler_type', '')
                if cc_type in ('msvc', ):
                    setattr(cc, 'spawn', self._dist_test_spawn_paths)
                else:
                    setattr(cc, 'spawn', self._dist_test_spawn)
        test = False
        try:
            self.dist_compile([
             source],
              flags, output_dir=(self.conf_tmp_path))
            test = True
        except CompileError as e:
            try:
                self.dist_log((str(e)), stderr=True)
            finally:
                e = None
                del e

        else:
            if bk_spawn:
                setattr(cc, 'spawn', bk_spawn)
            return test

    def dist_info(self):
        """
        Return a tuple containing info about (platform, compiler, extra_args),
        required by the abstract class '_CCompiler' for discovering the
        platform environment. This is also used as a cache factor in order
        to detect any changes happening from outside.
        """
        if hasattr(self, '_dist_info'):
            return self._dist_info
        else:
            cc_type = getattr(self._ccompiler, 'compiler_type', '')
            if cc_type in ('intelem', 'intelemw'):
                platform = 'x86_64'
            else:
                if cc_type in ('intel', 'intelw', 'intele'):
                    platform = 'x86'
                else:
                    from distutils.util import get_platform
                    platform = get_platform()
            cc_info = getattr(self._ccompiler, 'compiler', getattr(self._ccompiler, 'compiler_so', ''))
            if not cc_type or cc_type == 'unix':
                if hasattr(cc_info, '__iter__'):
                    compiler = cc_info[0]
                else:
                    compiler = str(cc_info)
            else:
                compiler = cc_type
        if hasattr(cc_info, '__iter__') and len(cc_info) > 1:
            extra_args = ' '.join(cc_info[1:])
        else:
            extra_args = os.environ.get('CFLAGS', '')
            extra_args += os.environ.get('CPPFLAGS', '')
        self._dist_info = (platform, compiler, extra_args)
        return self._dist_info

    @staticmethod
    def dist_error(*args):
        """Raise a compiler error"""
        from distutils.errors import CompileError
        raise CompileError((_Distutils._dist_str)(*args))

    @staticmethod
    def dist_fatal(*args):
        """Raise a distutils error"""
        from distutils.errors import DistutilsError
        raise DistutilsError((_Distutils._dist_str)(*args))

    @staticmethod
    def dist_log(*args, stderr=False):
        """Print a console message"""
        from numpy.distutils import log
        out = (_Distutils._dist_str)(*args)
        if stderr:
            log.warn(out)
        else:
            log.info(out)

    @staticmethod
    def dist_load_module(name, path):
        """Load a module from file, required by the abstract class '_Cache'."""
        from numpy.compat import npy_load_module
        try:
            return npy_load_module(name, path)
            except Exception as e:
            try:
                _Distutils.dist_log(e, stderr=True)
            finally:
                e = None
                del e

    @staticmethod
    def _dist_str(*args):
        """Return a string to print by log and errors."""

        def to_str(arg):
            if not isinstance(arg, str):
                if hasattr(arg, '__iter__'):
                    ret = []
                    for a in arg:
                        ret.append(to_str(a))
                    else:
                        return '(' + ' '.join(ret) + ')'

            return str(arg)

        stack = inspect.stack()[2]
        start = 'CCompilerOpt.%s[%d] : ' % (stack.function, stack.lineno)
        out = ' '.join([to_str(a) for a in (*args,)])
        return start + out

    def _dist_test_spawn_paths(self, cmd, display=None):
        """
        Fix msvc SDK ENV path same as distutils do
        without it we get c1: fatal error C1356: unable to find mspdbcore.dll
        """
        if not hasattr(self._ccompiler, '_paths'):
            self._dist_test_spawn(cmd)
            return None
        old_path = os.getenv('path')
        try:
            os.environ['path'] = self._ccompiler._paths
            self._dist_test_spawn(cmd)
        finally:
            os.environ['path'] = old_path

    _dist_warn_regex = re.compile('.*(warning D9002|invalid argument for option).*')

    @staticmethod
    def _dist_test_spawn(cmd, display=None):
        from distutils.errors import CompileError
        try:
            o = subprocess.check_output(cmd, stderr=(subprocess.STDOUT), universal_newlines=True)
            if o:
                if re.match(_Distutils._dist_warn_regex, o):
                    _Distutils.dist_error('Flags in command', cmd, "aren't supported by the compiler, output -> \n%s" % o)
        except subprocess.CalledProcessError as exc:
            try:
                o = exc.output
                s = exc.returncode
            finally:
                exc = None
                del exc

        except OSError:
            o = b''
            s = 127
        else:
            return
        _Distutils.dist_error('Command', cmd, 'failed with exit status %d output -> \n%s' % (
         s, o))


_share_cache = {}

class _Cache:
    __doc__ = 'An abstract class handles caching functionality, provides two\n    levels of caching, in-memory by share instances attributes among\n    each other and by store attributes into files.\n\n    **Note**:\n        any attributes that start with ``_`` or ``conf_`` will be ignored.\n\n    Parameters\n    ----------\n    cache_path: str or None\n        The path of cache file, if None then cache in file will disabled.\n\n    *factors:\n        The caching factors that need to utilize next to `conf_cache_factors`.\n\n    Attributes\n    ----------\n    cache_private: set\n        Hold the attributes that need be skipped from "in-memory cache".\n\n    cache_infile: bool\n        Utilized during initializing this class, to determine if the cache was able\n        to loaded from the specified cache path in \'cache_path\'.\n    '
    _cache_ignore = re.compile('^(_|conf_)')

    def __init__(self, cache_path=None, *factors):
        self.cache_me = {}
        self.cache_private = set()
        self.cache_infile = False
        if self.conf_nocache:
            self.dist_log('cache is disabled by `Config`')
            return None
        chash = (self.cache_hash)(*factors, *self.conf_cache_factors)
        if cache_path:
            if os.path.exists(cache_path):
                self.dist_log('load cache from file ->', cache_path)
                cache_mod = self.dist_load_module('cache', cache_path)
                if not cache_mod:
                    self.dist_log('unable to load the cache file as a module',
                      stderr=True)
                else:
                    if hasattr(cache_mod, 'hash'):
                        hasattr(cache_mod, 'data') or self.dist_log('invalid cache file', stderr=True)
                    else:
                        if chash == cache_mod.hash:
                            self.dist_log('hit the file cache')
                            for attr, val in cache_mod.data.items():
                                setattr(self, attr, val)
                            else:
                                self.cache_infile = True

                        else:
                            self.dist_log('miss the file cache')
            atexit.register(self._cache_write, cache_path, chash)
        other_cache = self.cache_infile or _share_cache.get(chash)
        if other_cache:
            self.dist_log('hit the memory cache')
            for attr, val in other_cache.__dict__.items():
                if attr in other_cache.cache_private or re.match(self._cache_ignore, attr):
                    pass
                else:
                    setattr(self, attr, val)

        _share_cache[chash] = self

    def __del__(self):
        pass

    def _cache_write(self, cache_path, cache_hash):
        self.dist_log('write cache to path ->', cache_path)
        for attr in list(self.__dict__.keys()):
            if re.match(self._cache_ignore, attr):
                self.__dict__.pop(attr)
        else:
            d = os.path.dirname(cache_path)
            if not os.path.exists(d):
                os.makedirs(d)
            repr_dict = pprint.pformat((self.__dict__), compact=True)
            with open(cache_path, 'w') as (f):
                f.write(textwrap.dedent("            # AUTOGENERATED DON'T EDIT\n            # Please make changes to the code generator             (distutils/ccompiler_opt.py)\n            hash = {}\n            data = \\\n            ").format(cache_hash))
                f.write(repr_dict)

    def cache_hash(self, *factors):
        chash = 0
        for f in factors:
            for char in str(f):
                chash = ord(char) + (chash << 6) + (chash << 16) - chash
                chash &= 4294967295
            else:
                return chash

    @staticmethod
    def me(cb):
        """
        A static method that can be treated as a decorator to
        dynamically cache certain methods.
        """

        def cache_wrap_me(self, *args, **kwargs):
            cache_key = str((
             
              cb.__name__, *args, *kwargs.keys(), *kwargs.values()))
            if cache_key in self.cache_me:
                return self.cache_me[cache_key]
            ccb = cb(self, *args, **kwargs)
            self.cache_me[cache_key] = ccb
            return ccb

        return cache_wrap_me


class _CCompiler(object):
    __doc__ = 'A helper class for `CCompilerOpt` containing all utilities that\n    related to the fundamental compiler\'s functions.\n\n    Attributes\n    ----------\n    cc_on_x86 : bool\n        True when the target architecture is 32-bit x86\n    cc_on_x64 : bool\n        True when the target architecture is 64-bit x86\n    cc_on_ppc64 : bool\n        True when the target architecture is 64-bit big-endian PowerPC\n    cc_on_armhf : bool\n        True when the target architecture is 32-bit ARMv7+\n    cc_on_aarch64 : bool\n        True when the target architecture is 64-bit Armv8-a+\n    cc_on_noarch : bool\n        True when the target architecture is unknown or not supported\n    cc_is_gcc : bool\n        True if the compiler is GNU or\n        if the compiler is unknown\n    cc_is_clang : bool\n        True if the compiler is Clang\n    cc_is_icc : bool\n        True if the compiler is Intel compiler (unix like)\n    cc_is_iccw : bool\n        True if the compiler is Intel compiler (msvc like)\n    cc_is_nocc : bool\n        True if the compiler isn\'t supported directly,\n        Note: that cause a fail-back to gcc\n    cc_has_debug : bool\n        True if the compiler has debug flags\n    cc_has_native : bool\n        True if the compiler has native flags\n    cc_noopt : bool\n        True if the compiler has definition \'DISABLE_OPT*\',\n        or \'cc_on_noarch\' is True\n    cc_march : str\n        The target architecture name, or "unknown" if\n        the architecture isn\'t supported\n    cc_name : str\n        The compiler name, or "unknown" if the compiler isn\'t supported\n    cc_flags : dict\n        Dictionary containing the initialized flags of `_Config.conf_cc_flags`\n    '

    def __init__--- This code section failed: ---

 L. 890         0  LOAD_GLOBAL              hasattr
                2  LOAD_FAST                'self'
                4  LOAD_STR                 'cc_is_cached'
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 891        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 893        14  LOAD_CONST               (('cc_on_x64', '.*(x|x86_|amd)64.*'), ('cc_on_x86', '.*(win32|x86|i386|i686).*'), ('cc_on_ppc64le', '.*(powerpc|ppc)64(el|le).*'), ('cc_on_ppc64', '.*(powerpc|ppc)64.*'), ('cc_on_aarch64', '.*(aarch64|arm64).*'), ('cc_on_armhf', '.*arm.*'), ('cc_on_noarch', ''))
               16  STORE_FAST               'detect_arch'

 L. 903        18  LOAD_CONST               (('cc_is_gcc', '.*(gcc|gnu\\-g).*'), ('cc_is_clang', '.*clang.*'), ('cc_is_iccw', '.*(intelw|intelemw|iccw).*'), ('cc_is_icc', '.*(intel|icc).*'), ('cc_is_msvc', '.*msvc.*'), ('cc_is_nocc', ''))
               20  STORE_FAST               'detect_compiler'

 L. 912        22  LOAD_CONST               (('cc_has_debug', '.*(O0|Od|ggdb|coverage|debug:full).*'), ('cc_has_native', '.*(-march=native|-xHost|/QxHost).*'), ('cc_noopt', '.*DISABLE_OPT.*'))
               24  STORE_FAST               'detect_args'

 L. 919        26  LOAD_FAST                'self'
               28  LOAD_METHOD              dist_info
               30  CALL_METHOD_0         0  ''
               32  STORE_FAST               'dist_info'

 L. 920        34  LOAD_FAST                'dist_info'
               36  UNPACK_SEQUENCE_3     3 
               38  STORE_FAST               'platform'
               40  STORE_FAST               'compiler_info'
               42  STORE_FAST               'extra_args'

 L. 922        44  LOAD_FAST                'detect_arch'
               46  LOAD_FAST                'detect_compiler'
               48  LOAD_FAST                'detect_args'
               50  BUILD_TUPLE_3         3 
               52  GET_ITER         
               54  FOR_ITER             86  'to 86'
               56  STORE_FAST               'section'

 L. 923        58  LOAD_FAST                'section'
               60  GET_ITER         
               62  FOR_ITER             84  'to 84'
               64  UNPACK_SEQUENCE_2     2 
               66  STORE_FAST               'attr'
               68  STORE_FAST               'rgex'

 L. 924        70  LOAD_GLOBAL              setattr
               72  LOAD_FAST                'self'
               74  LOAD_FAST                'attr'
               76  LOAD_CONST               False
               78  CALL_FUNCTION_3       3  ''
               80  POP_TOP          
               82  JUMP_BACK            62  'to 62'
               84  JUMP_BACK            54  'to 54'

 L. 926        86  LOAD_FAST                'detect_arch'
               88  LOAD_FAST                'platform'
               90  BUILD_TUPLE_2         2 
               92  LOAD_FAST                'detect_compiler'
               94  LOAD_FAST                'compiler_info'
               96  BUILD_TUPLE_2         2 
               98  BUILD_TUPLE_2         2 
              100  GET_ITER         
              102  FOR_ITER            164  'to 164'
              104  UNPACK_SEQUENCE_2     2 
              106  STORE_FAST               'detect'
              108  STORE_FAST               'searchin'

 L. 927       110  LOAD_FAST                'detect'
              112  GET_ITER         
              114  FOR_ITER            162  'to 162'
              116  UNPACK_SEQUENCE_2     2 
              118  STORE_FAST               'attr'
              120  STORE_FAST               'rgex'

 L. 928       122  LOAD_FAST                'rgex'
              124  POP_JUMP_IF_FALSE   144  'to 144'
              126  LOAD_GLOBAL              re
              128  LOAD_METHOD              match
              130  LOAD_FAST                'rgex'
              132  LOAD_FAST                'searchin'
              134  LOAD_GLOBAL              re
              136  LOAD_ATTR                IGNORECASE
              138  CALL_METHOD_3         3  ''
              140  POP_JUMP_IF_TRUE    144  'to 144'

 L. 929       142  JUMP_BACK           114  'to 114'
            144_0  COME_FROM           140  '140'
            144_1  COME_FROM           124  '124'

 L. 930       144  LOAD_GLOBAL              setattr
              146  LOAD_FAST                'self'
              148  LOAD_FAST                'attr'
              150  LOAD_CONST               True
              152  CALL_FUNCTION_3       3  ''
              154  POP_TOP          

 L. 931       156  POP_TOP          
              158  CONTINUE            102  'to 102'
              160  JUMP_BACK           114  'to 114'
              162  JUMP_BACK           102  'to 102'

 L. 933       164  LOAD_FAST                'detect_args'
              166  GET_ITER         
              168  FOR_ITER            212  'to 212'
              170  UNPACK_SEQUENCE_2     2 
              172  STORE_FAST               'attr'
              174  STORE_FAST               'rgex'

 L. 934       176  LOAD_FAST                'rgex'
              178  POP_JUMP_IF_FALSE   198  'to 198'
              180  LOAD_GLOBAL              re
              182  LOAD_METHOD              match
              184  LOAD_FAST                'rgex'
              186  LOAD_FAST                'extra_args'
              188  LOAD_GLOBAL              re
              190  LOAD_ATTR                IGNORECASE
              192  CALL_METHOD_3         3  ''
              194  POP_JUMP_IF_TRUE    198  'to 198'

 L. 935       196  JUMP_BACK           168  'to 168'
            198_0  COME_FROM           194  '194'
            198_1  COME_FROM           178  '178'

 L. 936       198  LOAD_GLOBAL              setattr
              200  LOAD_FAST                'self'
              202  LOAD_FAST                'attr'
              204  LOAD_CONST               True
              206  CALL_FUNCTION_3       3  ''
              208  POP_TOP          
              210  JUMP_BACK           168  'to 168'

 L. 938       212  LOAD_FAST                'self'
              214  LOAD_ATTR                cc_on_noarch
              216  POP_JUMP_IF_FALSE   246  'to 246'

 L. 939       218  LOAD_FAST                'self'
              220  LOAD_ATTR                dist_log

 L. 940       222  LOAD_STR                 'unable to detect CPU architecture which lead to disable the optimization. check dist_info:<<\n'
              224  LOAD_FAST                'dist_info'
              226  FORMAT_VALUE          0  ''
              228  LOAD_STR                 '\n>>'
              230  BUILD_STRING_3        3 

 L. 942       232  LOAD_CONST               True

 L. 939       234  LOAD_CONST               ('stderr',)
              236  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              238  POP_TOP          

 L. 944       240  LOAD_CONST               True
              242  LOAD_FAST                'self'
              244  STORE_ATTR               cc_noopt
            246_0  COME_FROM           216  '216'

 L. 946       246  LOAD_FAST                'self'
              248  LOAD_ATTR                conf_noopt
          250_252  POP_JUMP_IF_FALSE   274  'to 274'

 L. 947       254  LOAD_FAST                'self'
              256  LOAD_ATTR                dist_log
              258  LOAD_STR                 'Optimization is disabled by the Config'
              260  LOAD_CONST               True
              262  LOAD_CONST               ('stderr',)
              264  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              266  POP_TOP          

 L. 948       268  LOAD_CONST               True
              270  LOAD_FAST                'self'
              272  STORE_ATTR               cc_noopt
            274_0  COME_FROM           250  '250'

 L. 950       274  LOAD_FAST                'self'
              276  LOAD_ATTR                cc_is_nocc
          278_280  POP_JUMP_IF_FALSE   310  'to 310'

 L. 955       282  LOAD_FAST                'self'
              284  LOAD_ATTR                dist_log

 L. 956       286  LOAD_STR                 "unable to detect compiler type which leads to treating it as GCC. this is a normal behavior if you're using gcc-like compiler such as MinGW or IBM/XLC.check dist_info:<<\n"
              288  LOAD_FAST                'dist_info'
              290  FORMAT_VALUE          0  ''
              292  LOAD_STR                 '\n>>'
              294  BUILD_STRING_3        3 

 L. 959       296  LOAD_CONST               True

 L. 955       298  LOAD_CONST               ('stderr',)
              300  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              302  POP_TOP          

 L. 961       304  LOAD_CONST               True
              306  LOAD_FAST                'self'
              308  STORE_ATTR               cc_is_gcc
            310_0  COME_FROM           278  '278'

 L. 963       310  LOAD_STR                 'unknown'
              312  LOAD_FAST                'self'
              314  STORE_ATTR               cc_march

 L. 964       316  LOAD_CONST               ('x86', 'x64', 'ppc64', 'ppc64le', 'armhf', 'aarch64')
              318  GET_ITER         
            320_0  COME_FROM           336  '336'
              320  FOR_ITER            356  'to 356'
              322  STORE_FAST               'arch'

 L. 965       324  LOAD_GLOBAL              getattr
              326  LOAD_FAST                'self'
              328  LOAD_STR                 'cc_on_'
              330  LOAD_FAST                'arch'
              332  BINARY_ADD       
              334  CALL_FUNCTION_2       2  ''
          336_338  POP_JUMP_IF_FALSE   320  'to 320'

 L. 966       340  LOAD_FAST                'arch'
              342  LOAD_FAST                'self'
              344  STORE_ATTR               cc_march

 L. 967       346  POP_TOP          
          348_350  BREAK_LOOP          356  'to 356'
          352_354  JUMP_BACK           320  'to 320'

 L. 969       356  LOAD_STR                 'unknown'
              358  LOAD_FAST                'self'
              360  STORE_ATTR               cc_name

 L. 970       362  LOAD_CONST               ('gcc', 'clang', 'iccw', 'icc', 'msvc')
              364  GET_ITER         
            366_0  COME_FROM           382  '382'
              366  FOR_ITER            402  'to 402'
              368  STORE_FAST               'name'

 L. 971       370  LOAD_GLOBAL              getattr
              372  LOAD_FAST                'self'
              374  LOAD_STR                 'cc_is_'
              376  LOAD_FAST                'name'
              378  BINARY_ADD       
              380  CALL_FUNCTION_2       2  ''
          382_384  POP_JUMP_IF_FALSE   366  'to 366'

 L. 972       386  LOAD_FAST                'name'
              388  LOAD_FAST                'self'
              390  STORE_ATTR               cc_name

 L. 973       392  POP_TOP          
          394_396  BREAK_LOOP          402  'to 402'
          398_400  JUMP_BACK           366  'to 366'

 L. 975       402  BUILD_MAP_0           0 
              404  LOAD_FAST                'self'
              406  STORE_ATTR               cc_flags

 L. 976       408  LOAD_FAST                'self'
              410  LOAD_ATTR                conf_cc_flags
              412  LOAD_METHOD              get
              414  LOAD_FAST                'self'
              416  LOAD_ATTR                cc_name
              418  CALL_METHOD_1         1  ''
              420  STORE_FAST               'compiler_flags'

 L. 977       422  LOAD_FAST                'compiler_flags'
              424  LOAD_CONST               None
              426  COMPARE_OP               is
          428_430  POP_JUMP_IF_FALSE   448  'to 448'

 L. 978       432  LOAD_FAST                'self'
              434  LOAD_METHOD              dist_fatal

 L. 979       436  LOAD_STR                 "undefined flag for compiler '%s', leave an empty dict instead"

 L. 980       438  LOAD_FAST                'self'
              440  LOAD_ATTR                cc_name

 L. 979       442  BINARY_MODULO    

 L. 978       444  CALL_METHOD_1         1  ''
              446  POP_TOP          
            448_0  COME_FROM           428  '428'

 L. 982       448  LOAD_FAST                'compiler_flags'
              450  LOAD_METHOD              items
              452  CALL_METHOD_0         0  ''
              454  GET_ITER         
            456_0  COME_FROM           480  '480'
              456  FOR_ITER            548  'to 548'
              458  UNPACK_SEQUENCE_2     2 
              460  STORE_FAST               'name'
              462  STORE_FAST               'flags'

 L. 983       464  BUILD_LIST_0          0 
              466  DUP_TOP          
              468  LOAD_FAST                'self'
              470  LOAD_ATTR                cc_flags
              472  LOAD_FAST                'name'
              474  STORE_SUBSCR     
              476  STORE_FAST               'nflags'

 L. 984       478  LOAD_FAST                'flags'
          480_482  POP_JUMP_IF_FALSE   456  'to 456'

 L. 985       484  LOAD_GLOBAL              isinstance
              486  LOAD_FAST                'flags'
              488  LOAD_GLOBAL              str
              490  CALL_FUNCTION_2       2  ''
          492_494  POP_JUMP_IF_TRUE    500  'to 500'
              496  LOAD_ASSERT              AssertionError
              498  RAISE_VARARGS_1       1  'exception instance'
            500_0  COME_FROM           492  '492'

 L. 986       500  LOAD_FAST                'flags'
              502  LOAD_METHOD              split
              504  CALL_METHOD_0         0  ''
              506  STORE_FAST               'flags'

 L. 987       508  LOAD_FAST                'flags'
              510  GET_ITER         
            512_0  COME_FROM           526  '526'
              512  FOR_ITER            544  'to 544'
              514  STORE_FAST               'f'

 L. 988       516  LOAD_FAST                'self'
              518  LOAD_METHOD              cc_test_flags
              520  LOAD_FAST                'f'
              522  BUILD_LIST_1          1 
              524  CALL_METHOD_1         1  ''
          526_528  POP_JUMP_IF_FALSE   512  'to 512'

 L. 989       530  LOAD_FAST                'nflags'
              532  LOAD_METHOD              append
              534  LOAD_FAST                'f'
              536  CALL_METHOD_1         1  ''
              538  POP_TOP          
          540_542  JUMP_BACK           512  'to 512'
          544_546  JUMP_BACK           456  'to 456'

 L. 991       548  LOAD_CONST               True
              550  LOAD_FAST                'self'
              552  STORE_ATTR               cc_is_cached

Parse error at or near `CONTINUE' instruction at offset 158

    @_Cache.me
    def cc_test_flags(self, flags):
        """
        Returns True if the compiler supports 'flags'.
        """
        assert isinstance(flags, list)
        self.dist_log('testing flags', flags)
        test_path = os.path.join(self.conf_check_path, 'test_flags.c')
        test = self.dist_test(test_path, flags)
        if not test:
            self.dist_log('testing failed', stderr=True)
        return test

    def cc_normalize_flags(self, flags):
        """
        Remove the conflicts that caused due gathering implied features flags.

        Parameters
        ----------
        'flags' list, compiler flags
            flags should be sorted from the lowest to the highest interest.

        Returns
        -------
        list, filtered from any conflicts.

        Examples
        --------
        >>> self.cc_normalize_flags(['-march=armv8.2-a+fp16', '-march=armv8.2-a+dotprod'])
        ['armv8.2-a+fp16+dotprod']

        >>> self.cc_normalize_flags(
            ['-msse', '-msse2', '-msse3', '-mssse3', '-msse4.1', '-msse4.2', '-mavx', '-march=core-avx2']
        )
        ['-march=core-avx2']
        """
        assert isinstance(flags, list)
        if self.cc_is_gcc or self.cc_is_clang or self.cc_is_icc:
            return self._cc_normalize_unix(flags)
        if self.cc_is_msvc or self.cc_is_iccw:
            return self._cc_normalize_win(flags)
        return flags

    _cc_normalize_unix_mrgx = re.compile('^(-mcpu=|-march=|-x[A-Z0-9\\-])')
    _cc_normalize_unix_frgx = re.compile('^(?!(-mcpu=|-march=|-x[A-Z0-9\\-]))(?!-m[a-z0-9\\-\\.]*.$)')
    _cc_normalize_unix_krgx = re.compile('^(-mfpu|-mtune)')
    _cc_normalize_arch_ver = re.compile('[0-9.]')

    def _cc_normalize_unix--- This code section failed: ---

 L.1054         0  LOAD_CLOSURE             'self'
                2  BUILD_TUPLE_1         1 
                4  LOAD_CODE                <code_object ver_flags>
                6  LOAD_STR                 '_CCompiler._cc_normalize_unix.<locals>.ver_flags'
                8  MAKE_FUNCTION_8          'closure'
               10  STORE_FAST               'ver_flags'

 L.1063        12  LOAD_GLOBAL              len
               14  LOAD_FAST                'flags'
               16  CALL_FUNCTION_1       1  ''
               18  LOAD_CONST               1
               20  COMPARE_OP               <=
               22  POP_JUMP_IF_FALSE    28  'to 28'

 L.1064        24  LOAD_FAST                'flags'
               26  RETURN_VALUE     
             28_0  COME_FROM            22  '22'

 L.1066        28  LOAD_GLOBAL              enumerate
               30  LOAD_GLOBAL              reversed
               32  LOAD_FAST                'flags'
               34  CALL_FUNCTION_1       1  ''
               36  CALL_FUNCTION_1       1  ''
               38  GET_ITER         
               40  FOR_ITER            238  'to 238'
               42  UNPACK_SEQUENCE_2     2 
               44  STORE_FAST               'i'
               46  STORE_FAST               'cur_flag'

 L.1067        48  LOAD_GLOBAL              re
               50  LOAD_METHOD              match
               52  LOAD_DEREF               'self'
               54  LOAD_ATTR                _cc_normalize_unix_mrgx
               56  LOAD_FAST                'cur_flag'
               58  CALL_METHOD_2         2  ''
               60  POP_JUMP_IF_TRUE     64  'to 64'

 L.1068        62  JUMP_BACK            40  'to 40'
             64_0  COME_FROM            60  '60'

 L.1069        64  LOAD_FAST                'flags'
               66  LOAD_CONST               None
               68  LOAD_FAST                'i'
               70  LOAD_CONST               1
               72  BINARY_ADD       
               74  UNARY_NEGATIVE   
               76  BUILD_SLICE_2         2 
               78  BINARY_SUBSCR    
               80  STORE_FAST               'lower_flags'

 L.1070        82  LOAD_FAST                'flags'
               84  LOAD_FAST                'i'
               86  UNARY_NEGATIVE   
               88  LOAD_CONST               None
               90  BUILD_SLICE_2         2 
               92  BINARY_SUBSCR    
               94  STORE_FAST               'upper_flags'

 L.1071        96  LOAD_GLOBAL              list
               98  LOAD_GLOBAL              filter

 L.1072       100  LOAD_DEREF               'self'
              102  LOAD_ATTR                _cc_normalize_unix_frgx
              104  LOAD_ATTR                search

 L.1072       106  LOAD_FAST                'lower_flags'

 L.1071       108  CALL_FUNCTION_2       2  ''
              110  CALL_FUNCTION_1       1  ''
              112  STORE_FAST               'filterd'

 L.1075       114  LOAD_FAST                'ver_flags'
              116  LOAD_FAST                'cur_flag'
              118  CALL_FUNCTION_1       1  ''
              120  UNPACK_SEQUENCE_3     3 
              122  STORE_FAST               'ver'
              124  STORE_FAST               'arch'
              126  STORE_FAST               'subflags'

 L.1076       128  LOAD_FAST                'ver'
              130  LOAD_CONST               0
              132  COMPARE_OP               >
              134  POP_JUMP_IF_FALSE   206  'to 206'
              136  LOAD_GLOBAL              len
              138  LOAD_FAST                'subflags'
              140  CALL_FUNCTION_1       1  ''
              142  LOAD_CONST               0
              144  COMPARE_OP               >
              146  POP_JUMP_IF_FALSE   206  'to 206'

 L.1077       148  LOAD_FAST                'lower_flags'
              150  GET_ITER         
            152_0  COME_FROM           176  '176'
              152  FOR_ITER            188  'to 188'
              154  STORE_FAST               'xflag'

 L.1078       156  LOAD_FAST                'ver_flags'
              158  LOAD_FAST                'xflag'
              160  CALL_FUNCTION_1       1  ''
              162  UNPACK_SEQUENCE_3     3 
              164  STORE_FAST               'xver'
              166  STORE_FAST               '_'
              168  STORE_FAST               'xsubflags'

 L.1079       170  LOAD_FAST                'ver'
              172  LOAD_FAST                'xver'
              174  COMPARE_OP               ==
              176  POP_JUMP_IF_FALSE   152  'to 152'

 L.1080       178  LOAD_FAST                'xsubflags'
              180  LOAD_FAST                'subflags'
              182  BINARY_ADD       
              184  STORE_FAST               'subflags'
              186  JUMP_BACK           152  'to 152'

 L.1081       188  LOAD_FAST                'arch'
              190  LOAD_STR                 '+'
              192  BINARY_ADD       
              194  LOAD_STR                 '+'
              196  LOAD_METHOD              join
              198  LOAD_FAST                'subflags'
              200  CALL_METHOD_1         1  ''
              202  BINARY_ADD       
              204  STORE_FAST               'cur_flag'
            206_0  COME_FROM           146  '146'
            206_1  COME_FROM           134  '134'

 L.1083       206  LOAD_FAST                'filterd'
              208  LOAD_FAST                'cur_flag'
              210  BUILD_LIST_1          1 
              212  BINARY_ADD       
              214  STORE_FAST               'flags'

 L.1084       216  LOAD_FAST                'i'
              218  LOAD_CONST               0
              220  COMPARE_OP               >
              222  POP_JUMP_IF_FALSE   232  'to 232'

 L.1085       224  LOAD_FAST                'flags'
              226  LOAD_FAST                'upper_flags'
              228  INPLACE_ADD      
              230  STORE_FAST               'flags'
            232_0  COME_FROM           222  '222'

 L.1086       232  POP_TOP          
              234  BREAK_LOOP          238  'to 238'
              236  JUMP_BACK            40  'to 40'

 L.1089       238  BUILD_LIST_0          0 
              240  STORE_FAST               'final_flags'

 L.1090       242  LOAD_GLOBAL              set
              244  CALL_FUNCTION_0       0  ''
              246  STORE_FAST               'matched'

 L.1091       248  LOAD_GLOBAL              reversed
              250  LOAD_FAST                'flags'
              252  CALL_FUNCTION_1       1  ''
              254  GET_ITER         
              256  FOR_ITER            332  'to 332'
              258  STORE_FAST               'f'

 L.1092       260  LOAD_GLOBAL              re
              262  LOAD_METHOD              match
              264  LOAD_DEREF               'self'
              266  LOAD_ATTR                _cc_normalize_unix_krgx
              268  LOAD_FAST                'f'
              270  CALL_METHOD_2         2  ''
              272  STORE_FAST               'match'

 L.1093       274  LOAD_FAST                'match'
          276_278  POP_JUMP_IF_TRUE    282  'to 282'

 L.1094       280  BREAK_LOOP          316  'to 316'
            282_0  COME_FROM           276  '276'

 L.1095       282  LOAD_FAST                'match'
              284  LOAD_CONST               0
              286  BINARY_SUBSCR    
              288  LOAD_FAST                'matched'
              290  COMPARE_OP               in
          292_294  POP_JUMP_IF_FALSE   302  'to 302'

 L.1096   296_298  JUMP_BACK           256  'to 256'
              300  JUMP_FORWARD        316  'to 316'
            302_0  COME_FROM           292  '292'

 L.1098       302  LOAD_FAST                'matched'
              304  LOAD_METHOD              add
              306  LOAD_FAST                'match'
              308  LOAD_CONST               0
              310  BINARY_SUBSCR    
              312  CALL_METHOD_1         1  ''
              314  POP_TOP          
            316_0  COME_FROM           300  '300'
            316_1  COME_FROM           280  '280'

 L.1099       316  LOAD_FAST                'final_flags'
              318  LOAD_METHOD              insert
              320  LOAD_CONST               0
              322  LOAD_FAST                'f'
              324  CALL_METHOD_2         2  ''
              326  POP_TOP          
          328_330  JUMP_BACK           256  'to 256'

 L.1100       332  LOAD_FAST                'final_flags'
              334  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 300

    _cc_normalize_win_frgx = re.compile('^(?!(/arch\\:|/Qx\\:))')
    _cc_normalize_win_mrgx = re.compile('^(/arch|/Qx:)')

    def _cc_normalize_win(self, flags):
        for i, f in enumerate(reversed(flags)):
            if not re.match(self._cc_normalize_win_mrgx, f):
                pass
            else:
                i += 1
                return list(filter(self._cc_normalize_win_frgx.search, flags[:-i])) + flags[-i:]
                return flags


class _Feature:
    __doc__ = 'A helper class for `CCompilerOpt` that managing CPU features.\n\n    Attributes\n    ----------\n    feature_supported : dict\n        Dictionary containing all CPU features that supported\n        by the platform, according to the specified values in attribute\n        `_Config.conf_features` and `_Config.conf_features_partial()`\n\n    feature_min : set\n        The minimum support of CPU features, according to\n        the specified values in attribute `_Config.conf_min_features`.\n    '

    def __init__--- This code section failed: ---

 L.1133         0  LOAD_GLOBAL              hasattr
                2  LOAD_FAST                'self'
                4  LOAD_STR                 'feature_is_cached'
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L.1134        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L.1135        14  LOAD_FAST                'self'
               16  LOAD_METHOD              conf_features_partial
               18  CALL_METHOD_0         0  ''
               20  DUP_TOP          
               22  LOAD_FAST                'self'
               24  STORE_ATTR               feature_supported
               26  STORE_FAST               'pfeatures'

 L.1136        28  LOAD_GLOBAL              list
               30  LOAD_FAST                'pfeatures'
               32  LOAD_METHOD              keys
               34  CALL_METHOD_0         0  ''
               36  CALL_FUNCTION_1       1  ''
               38  GET_ITER         
               40  FOR_ITER            184  'to 184'
               42  STORE_FAST               'feature_name'

 L.1137        44  LOAD_FAST                'pfeatures'
               46  LOAD_FAST                'feature_name'
               48  BINARY_SUBSCR    
               50  STORE_DEREF              'feature'

 L.1138        52  LOAD_FAST                'self'
               54  LOAD_ATTR                conf_features
               56  LOAD_FAST                'feature_name'
               58  BINARY_SUBSCR    
               60  STORE_FAST               'cfeature'

 L.1139        62  LOAD_DEREF               'feature'
               64  LOAD_METHOD              update
               66  LOAD_CLOSURE             'feature'
               68  BUILD_TUPLE_1         1 
               70  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               72  LOAD_STR                 '_Feature.__init__.<locals>.<dictcomp>'
               74  MAKE_FUNCTION_8          'closure'

 L.1140        76  LOAD_FAST                'cfeature'
               78  LOAD_METHOD              items
               80  CALL_METHOD_0         0  ''

 L.1139        82  GET_ITER         
               84  CALL_FUNCTION_1       1  ''
               86  CALL_METHOD_1         1  ''
               88  POP_TOP          

 L.1142        90  LOAD_DEREF               'feature'
               92  LOAD_METHOD              get
               94  LOAD_STR                 'disable'
               96  CALL_METHOD_1         1  ''
               98  STORE_FAST               'disabled'

 L.1143       100  LOAD_FAST                'disabled'
              102  LOAD_CONST               None
              104  COMPARE_OP               is-not
              106  POP_JUMP_IF_FALSE   140  'to 140'

 L.1144       108  LOAD_FAST                'pfeatures'
              110  LOAD_METHOD              pop
              112  LOAD_FAST                'feature_name'
              114  CALL_METHOD_1         1  ''
              116  POP_TOP          

 L.1145       118  LOAD_FAST                'self'
              120  LOAD_ATTR                dist_log

 L.1146       122  LOAD_STR                 "feature '%s' is disabled,"
              124  LOAD_FAST                'feature_name'
              126  BINARY_MODULO    

 L.1147       128  LOAD_FAST                'disabled'

 L.1147       130  LOAD_CONST               True

 L.1145       132  LOAD_CONST               ('stderr',)
              134  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              136  POP_TOP          

 L.1149       138  JUMP_BACK            40  'to 40'
            140_0  COME_FROM           106  '106'

 L.1151       140  LOAD_CONST               ('implies', 'group', 'detect', 'headers', 'flags', 'extra_checks')
              142  GET_ITER         
            144_0  COME_FROM           166  '166'
              144  FOR_ITER            182  'to 182'
              146  STORE_FAST               'option'

 L.1154       148  LOAD_DEREF               'feature'
              150  LOAD_METHOD              get
              152  LOAD_FAST                'option'
              154  CALL_METHOD_1         1  ''
              156  STORE_FAST               'oval'

 L.1155       158  LOAD_GLOBAL              isinstance
              160  LOAD_FAST                'oval'
              162  LOAD_GLOBAL              str
              164  CALL_FUNCTION_2       2  ''
              166  POP_JUMP_IF_FALSE   144  'to 144'

 L.1156       168  LOAD_FAST                'oval'
              170  LOAD_METHOD              split
              172  CALL_METHOD_0         0  ''
              174  LOAD_DEREF               'feature'
              176  LOAD_FAST                'option'
              178  STORE_SUBSCR     
              180  JUMP_BACK           144  'to 144'
              182  JUMP_BACK            40  'to 40'

 L.1158       184  LOAD_GLOBAL              set
              186  CALL_FUNCTION_0       0  ''
              188  LOAD_FAST                'self'
              190  STORE_ATTR               feature_min

 L.1159       192  LOAD_FAST                'self'
              194  LOAD_ATTR                conf_min_features
              196  LOAD_METHOD              get
              198  LOAD_FAST                'self'
              200  LOAD_ATTR                cc_march
              202  LOAD_STR                 ''
              204  CALL_METHOD_2         2  ''
              206  STORE_FAST               'min_f'

 L.1160       208  LOAD_FAST                'min_f'
              210  LOAD_METHOD              upper
              212  CALL_METHOD_0         0  ''
              214  LOAD_METHOD              split
              216  CALL_METHOD_0         0  ''
              218  GET_ITER         
            220_0  COME_FROM           232  '232'
              220  FOR_ITER            248  'to 248'
              222  STORE_FAST               'F'

 L.1161       224  LOAD_FAST                'F'
              226  LOAD_FAST                'self'
              228  LOAD_ATTR                feature_supported
              230  COMPARE_OP               in
              232  POP_JUMP_IF_FALSE   220  'to 220'

 L.1162       234  LOAD_FAST                'self'
              236  LOAD_ATTR                feature_min
              238  LOAD_METHOD              add
              240  LOAD_FAST                'F'
              242  CALL_METHOD_1         1  ''
              244  POP_TOP          
              246  JUMP_BACK           220  'to 220'

 L.1164       248  LOAD_CONST               True
              250  LOAD_FAST                'self'
              252  STORE_ATTR               feature_is_cached

Parse error at or near `LOAD_DICTCOMP' instruction at offset 70

    def feature_names(self, names=None, force_flags=None):
        """
        Returns a set of CPU feature names that supported by platform and the **C** compiler.

        Parameters
        ----------
        'names': sequence or None, optional
            Specify certain CPU features to test it against the **C** compiler.
            if None(default), it will test all current supported features.
            **Note**: feature names must be in upper-case.

        'force_flags': list or None, optional
            If None(default), default compiler flags for every CPU feature will be used
            during the test.
        """
        if not names is None:
            raise isinstance(names, str) or hasattr(names, '__iter__') or AssertionError
        if not force_flags is None:
            assert isinstance(force_flags, list)
        if names is None:
            names = self.feature_supported.keys()
        supported_names = set()
        for f in names:
            if self.feature_is_supported(f, force_flags=force_flags):
                supported_names.add(f)
            return supported_names

    def feature_is_exist(self, name):
        """
        Returns True if a certain feature is exist and covered within
        `_Config.conf_features`.

        Parameters
        ----------
        'name': str
            feature name in uppercase.
        """
        assert name.isupper()
        return name in self.conf_features

    def feature_sorted(self, names, reverse=False):
        """
        Sort a list of CPU features ordered by the lowest interest.

        Parameters
        ----------
        'names': sequence
            sequence of supported feature names in uppercase.
        'reverse': bool, optional
            If true, the sorted features is reversed. (highest interest)

        Returns
        -------
        list, sorted CPU features
        """

        def sort_cb(k):
            if isinstance(k, str):
                return self.feature_supported[k]['interest']
            rank = max([self.feature_supported[f]['interest'] for f in k])
            rank += len(k) - 1
            return rank

        return sorted(names, reverse=reverse, key=sort_cb)

    def feature_implies(self, names, keep_origins=False):
        """
        Return a set of CPU features that implied by 'names'

        Parameters
        ----------
        names: str or sequence of str
            CPU feature name(s) in uppercase.

        keep_origins: bool
            if False(default) then the returned set will not contain any
            features from 'names'. This case happens only when two features
            imply each other.

        Examples
        --------
        >>> self.feature_implies("SSE3")
        {'SSE', 'SSE2'}
        >>> self.feature_implies("SSE2")
        {'SSE'}
        >>> self.feature_implies("SSE2", keep_origins=True)
        # 'SSE2' found here since 'SSE' and 'SSE2' imply each other
        {'SSE', 'SSE2'}
        """

        def get_implies(name, _caller=set()):
            implies = set()
            d = self.feature_supported[name]
            for i in d.get('implies', []):
                implies.add(i)
                if i in _caller:
                    pass
                else:
                    _caller.add(name)
                    implies = implies.union(get_implies(i, _caller))
            else:
                return implies

        if isinstance(names, str):
            implies = get_implies(names)
            names = [names]
        else:
            assert hasattr(names, '__iter__')
            implies = set()
            for n in names:
                implies = implies.union(get_implies(n))
            else:
                if not keep_origins:
                    implies.difference_update(names)
                return implies

    def feature_implies_c(self, names):
        """same as feature_implies() but combining 'names'"""
        if isinstance(names, str):
            names = set((names,))
        else:
            names = set(names)
        return names.union(self.feature_implies(names))

    def feature_ahead(self, names):
        """
        Return list of features in 'names' after remove any
        implied features and keep the origins.

        Parameters
        ----------
        'names': sequence
            sequence of CPU feature names in uppercase.

        Returns
        -------
        list of CPU features sorted as-is 'names'

        Examples
        --------
        >>> self.feature_ahead(["SSE2", "SSE3", "SSE41"])
        ["SSE41"]
        # assume AVX2 and FMA3 implies each other and AVX2
        # is the highest interest
        >>> self.feature_ahead(["SSE2", "SSE3", "SSE41", "AVX2", "FMA3"])
        ["AVX2"]
        # assume AVX2 and FMA3 don't implies each other
        >>> self.feature_ahead(["SSE2", "SSE3", "SSE41", "AVX2", "FMA3"])
        ["AVX2", "FMA3"]
        """
        if not (isinstance(names, str) or hasattr(names, '__iter__')):
            raise AssertionError
        implies = self.feature_implies(names, keep_origins=True)
        ahead = [n for n in names if n not in implies]
        if len(ahead) == 0:
            ahead = self.feature_sorted(names, reverse=True)[:1]
        return ahead

    def feature_untied(self, names):
        """
        same as 'feature_ahead()' but if both features implied each other
        and keep the highest interest.

        Parameters
        ----------
        'names': sequence
            sequence of CPU feature names in uppercase.

        Returns
        -------
        list of CPU features sorted as-is 'names'

        Examples
        --------
        >>> self.feature_untied(["SSE2", "SSE3", "SSE41"])
        ["SSE2", "SSE3", "SSE41"]
        # assume AVX2 and FMA3 implies each other
        >>> self.feature_untied(["SSE2", "SSE3", "SSE41", "FMA3", "AVX2"])
        ["SSE2", "SSE3", "SSE41", "AVX2"]
        """
        if not (isinstance(names, str) or hasattr(names, '__iter__')):
            raise AssertionError
        final = []
        for n in names:
            implies = self.feature_implies(n)
            tied = [nn for nn in final if nn in implies if n in self.feature_implies(nn)]
            if tied:
                tied = self.feature_sorted(tied + [n])
                if n not in tied[1:]:
                    pass
                else:
                    final.remove(tied[:1][0])
            final.append(n)
        else:
            return final

    def feature_get_til--- This code section failed: ---

 L.1378         0  LOAD_CLOSURE             'keyisfalse'
                2  LOAD_CLOSURE             'self'
                4  BUILD_TUPLE_2         2 
                6  LOAD_CODE                <code_object til>
                8  LOAD_STR                 '_Feature.feature_get_til.<locals>.til'
               10  MAKE_FUNCTION_8          'closure'
               12  STORE_DEREF              'til'

 L.1388        14  LOAD_GLOBAL              isinstance
               16  LOAD_FAST                'names'
               18  LOAD_GLOBAL              str
               20  CALL_FUNCTION_2       2  ''
               22  POP_JUMP_IF_TRUE     36  'to 36'
               24  LOAD_GLOBAL              len
               26  LOAD_FAST                'names'
               28  CALL_FUNCTION_1       1  ''
               30  LOAD_CONST               1
               32  COMPARE_OP               <=
               34  POP_JUMP_IF_FALSE    56  'to 56'
             36_0  COME_FROM            22  '22'

 L.1389        36  LOAD_DEREF               'til'
               38  LOAD_FAST                'names'
               40  CALL_FUNCTION_1       1  ''
               42  STORE_FAST               'names'

 L.1391        44  LOAD_FAST                'names'
               46  LOAD_METHOD              reverse
               48  CALL_METHOD_0         0  ''
               50  POP_TOP          

 L.1392        52  LOAD_FAST                'names'
               54  RETURN_VALUE     
             56_0  COME_FROM            34  '34'

 L.1394        56  LOAD_DEREF               'self'
               58  LOAD_METHOD              feature_ahead
               60  LOAD_FAST                'names'
               62  CALL_METHOD_1         1  ''
               64  STORE_FAST               'names'

 L.1395        66  LOAD_CLOSURE             'til'
               68  BUILD_TUPLE_1         1 
               70  LOAD_SETCOMP             '<code_object <setcomp>>'
               72  LOAD_STR                 '_Feature.feature_get_til.<locals>.<setcomp>'
               74  MAKE_FUNCTION_8          'closure'
               76  LOAD_FAST                'names'
               78  GET_ITER         
               80  CALL_FUNCTION_1       1  ''
               82  STORE_FAST               'names'

 L.1396        84  LOAD_DEREF               'self'
               86  LOAD_METHOD              feature_sorted
               88  LOAD_FAST                'names'
               90  CALL_METHOD_1         1  ''
               92  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_SETCOMP' instruction at offset 70

    def feature_detect(self, names):
        """
        Return a list of CPU features that required to be detected
        sorted from the lowest to highest interest.
        """
        names = self.feature_get_til(names, 'implies_detect')
        detect = []
        for n in names:
            d = self.feature_supported[n]
            detect += d.get('detect', d.get('group', [n]))
        else:
            return detect

    @_Cache.me
    def feature_flags(self, names):
        """
        Return a list of CPU features flags sorted from the lowest
        to highest interest.
        """
        names = self.feature_sorted(self.feature_implies_c(names))
        flags = []
        for n in names:
            d = self.feature_supported[n]
            f = d.get('flags', [])
            if f:
                if not self.cc_test_flags(f):
                    pass
                else:
                    flags += f
            return self.cc_normalize_flags(flags)

    @_Cache.me
    def feature_test(self, name, force_flags=None):
        """
        Test a certain CPU feature against the compiler through its own
        check file.

        Parameters
        ----------
        'name': str
            Supported CPU feature name.

        'force_flags': list or None, optional
            If None(default), the returned flags from `feature_flags()`
            will be used.
       """
        if force_flags is None:
            force_flags = self.feature_flags(name)
        else:
            self.dist_log("testing feature '%s' with flags (%s)" % (
             name, ' '.join(force_flags)))
            test_path = os.path.join(self.conf_check_path, 'cpu_%s.c' % name.lower())
            if not os.path.exists(test_path):
                self.dist_fatal('feature test file is not exist', test_path)
            test = self.dist_test(test_path, force_flags + self.cc_flags['werror'])
            test or self.dist_log('testing failed', stderr=True)
        return test

    @_Cache.me
    def feature_is_supported(self, name, force_flags=None):
        """
        Check if a certain CPU feature is supported by the platform and compiler.

        Parameters
        ----------
        'name': str
            CPU feature name in uppercase.

        'force_flags': list or None, optional
            If None(default), default compiler flags for every CPU feature will be used
            during test.
        """
        if not name.isupper():
            raise AssertionError
        else:
            if not force_flags is None:
                assert isinstance(force_flags, list)
            supported = name in self.feature_supported
            if supported:
                for impl in self.feature_implies(name):
                    if not self.feature_test(impl, force_flags):
                        return False

                if not self.feature_test(name, force_flags):
                    return False
        return supported

    @_Cache.me
    def feature_can_autovec(self, name):
        """
        check if the feature can be auto-vectorized by the compiler
        """
        assert isinstance(name, str)
        d = self.feature_supported[name]
        can = d.get('autovec', None)
        if can is None:
            valid_flags = [self.cc_test_flags([f]) for f in d.get('flags', [])]
            can = valid_flags and any(valid_flags)
        return can

    @_Cache.me
    def feature_extra_checks(self, name):
        """
        Return a list of supported extra checks after testing them against
        the compiler.

        Parameters
        ----------
        names: str
            CPU feature name in uppercase.
        """
        if not isinstance(name, str):
            raise AssertionError
        else:
            d = self.feature_supported[name]
            extra_checks = d.get('extra_checks', [])
            return extra_checks or []
        self.dist_log("Testing extra checks for feature '%s'" % name, extra_checks)
        flags = self.feature_flags(name)
        available = []
        not_available = []
        for chk in extra_checks:
            test_path = os.path.join(self.conf_check_path, 'extra_%s.c' % chk.lower())
            if not os.path.exists(test_path):
                self.dist_fatal('extra check file does not exist', test_path)
            is_supported = self.dist_test(test_path, flags + self.cc_flags['werror'])
            if is_supported:
                available.append(chk)
            else:
                not_available.append(chk)
        else:
            if not_available:
                self.dist_log('testing failed for checks', not_available, stderr=True)
            return available

    def feature_c_preprocessor(self, feature_name, tabs=0):
        """
        Generate C preprocessor definitions and include headers of a CPU feature.

        Parameters
        ----------
        'feature_name': str
            CPU feature name in uppercase.
        'tabs': int
            if > 0, align the generated strings to the right depend on number of tabs.

        Returns
        -------
        str, generated C preprocessor

        Examples
        --------
        >>> self.feature_c_preprocessor("SSE3")
        /** SSE3 **/
        #define NPY_HAVE_SSE3 1
        #include <pmmintrin.h>
        """
        assert feature_name.isupper()
        feature = self.feature_supported.get(feature_name)
        assert feature is not None
        prepr = [
         '/** %s **/' % feature_name,
         '#define %sHAVE_%s 1' % (self.conf_c_prefix, feature_name)]
        prepr += ['#include <%s>' % h for h in feature.get('headers', [])]
        extra_defs = feature.get('group', [])
        extra_defs += self.feature_extra_checks(feature_name)
        for edef in extra_defs:
            prepr += [
             '#ifndef %sHAVE_%s' % (self.conf_c_prefix, edef),
             '\t#define %sHAVE_%s 1' % (self.conf_c_prefix, edef),
             '#endif']
        else:
            if tabs > 0:
                prepr = ['\t' * tabs + l for l in prepr]
            return '\n'.join(prepr)


class _Parse:
    __doc__ = "A helper class that parsing main arguments of `CCompilerOpt`,\n    also parsing configuration statements in dispatch-able sources.\n\n    Parameters\n    ----------\n    cpu_baseline: str or None\n        minimal set of required CPU features or special options.\n\n    cpu_dispatch: str or None\n        dispatched set of additional CPU features or special options.\n\n    Special options can be:\n        - **MIN**: Enables the minimum CPU features that utilized via `_Config.conf_min_features`\n        - **MAX**: Enables all supported CPU features by the Compiler and platform.\n        - **NATIVE**: Enables all CPU features that supported by the current machine.\n        - **NONE**: Enables nothing\n        - **Operand +/-**: remove or add features, useful with options **MAX**, **MIN** and **NATIVE**.\n            NOTE: operand + is only added for nominal reason.\n\n    NOTES:\n        - Case-insensitive among all CPU features and special options.\n        - Comma or space can be used as a separator.\n        - If the CPU feature is not supported by the user platform or compiler,\n          it will be skipped rather than raising a fatal error.\n        - Any specified CPU features to 'cpu_dispatch' will be skipped if its part of CPU baseline features\n        - 'cpu_baseline' force enables implied features.\n\n    Attributes\n    ----------\n    parse_baseline_names : list\n        Final CPU baseline's feature names(sorted from low to high)\n    parse_baseline_flags : list\n        Compiler flags of baseline features\n    parse_dispatch_names : list\n        Final CPU dispatch-able feature names(sorted from low to high)\n    parse_target_groups : dict\n        Dictionary containing initialized target groups that configured\n        through class attribute `conf_target_groups`.\n\n        The key is represent the group name and value is a tuple\n        contains three items :\n            - bool, True if group has the 'baseline' option.\n            - list, list of CPU features.\n            - list, list of extra compiler flags.\n\n    "

    def __init__--- This code section failed: ---

 L.1638         0  LOAD_GLOBAL              dict

 L.1641         2  LOAD_CONST               None

 L.1641         4  LOAD_DEREF               'self'
                6  LOAD_ATTR                _parse_policy_not_keepbase

 L.1642         8  BUILD_LIST_0          0 

 L.1640        10  BUILD_TUPLE_3         3 

 L.1645        12  LOAD_DEREF               'self'
               14  LOAD_ATTR                _parse_policy_keepsort

 L.1646        16  LOAD_DEREF               'self'
               18  LOAD_ATTR                _parse_policy_not_keepsort

 L.1647        20  BUILD_LIST_0          0 

 L.1644        22  BUILD_TUPLE_3         3 

 L.1650        24  LOAD_DEREF               'self'
               26  LOAD_ATTR                _parse_policy_maxopt

 L.1650        28  LOAD_CONST               None

 L.1651        30  BUILD_LIST_0          0 

 L.1649        32  BUILD_TUPLE_3         3 

 L.1654        34  LOAD_DEREF               'self'
               36  LOAD_ATTR                _parse_policy_werror

 L.1654        38  LOAD_CONST               None

 L.1655        40  BUILD_LIST_0          0 

 L.1653        42  BUILD_TUPLE_3         3 

 L.1658        44  LOAD_DEREF               'self'
               46  LOAD_ATTR                _parse_policy_autovec

 L.1658        48  LOAD_CONST               None

 L.1659        50  LOAD_STR                 'MAXOPT'
               52  BUILD_LIST_1          1 

 L.1657        54  BUILD_TUPLE_3         3 

 L.1638        56  LOAD_CONST               ('KEEP_BASELINE', 'KEEP_SORT', 'MAXOPT', 'WERROR', 'AUTOVEC')
               58  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
               60  LOAD_DEREF               'self'
               62  STORE_ATTR               _parse_policies

 L.1662        64  LOAD_GLOBAL              hasattr
               66  LOAD_DEREF               'self'
               68  LOAD_STR                 'parse_is_cached'
               70  CALL_FUNCTION_2       2  ''
               72  POP_JUMP_IF_FALSE    78  'to 78'

 L.1663        74  LOAD_CONST               None
               76  RETURN_VALUE     
             78_0  COME_FROM            72  '72'

 L.1665        78  BUILD_LIST_0          0 
               80  LOAD_DEREF               'self'
               82  STORE_ATTR               parse_baseline_names

 L.1666        84  BUILD_LIST_0          0 
               86  LOAD_DEREF               'self'
               88  STORE_ATTR               parse_baseline_flags

 L.1667        90  BUILD_LIST_0          0 
               92  LOAD_DEREF               'self'
               94  STORE_ATTR               parse_dispatch_names

 L.1668        96  BUILD_MAP_0           0 
               98  LOAD_DEREF               'self'
              100  STORE_ATTR               parse_target_groups

 L.1670       102  LOAD_DEREF               'self'
              104  LOAD_ATTR                cc_noopt
              106  POP_JUMP_IF_FALSE   116  'to 116'

 L.1672       108  LOAD_CONST               None
              110  DUP_TOP          
              112  STORE_FAST               'cpu_baseline'
              114  STORE_FAST               'cpu_dispatch'
            116_0  COME_FROM           106  '106'

 L.1674       116  LOAD_DEREF               'self'
              118  LOAD_METHOD              dist_log
              120  LOAD_STR                 'check requested baseline'
              122  CALL_METHOD_1         1  ''
              124  POP_TOP          

 L.1675       126  LOAD_FAST                'cpu_baseline'
              128  LOAD_CONST               None
              130  COMPARE_OP               is-not
              132  POP_JUMP_IF_FALSE   186  'to 186'

 L.1676       134  LOAD_DEREF               'self'
              136  LOAD_METHOD              _parse_arg_features
              138  LOAD_STR                 'cpu_baseline'
              140  LOAD_FAST                'cpu_baseline'
              142  CALL_METHOD_2         2  ''
              144  STORE_FAST               'cpu_baseline'

 L.1677       146  LOAD_DEREF               'self'
              148  LOAD_METHOD              feature_names
              150  LOAD_FAST                'cpu_baseline'
              152  CALL_METHOD_1         1  ''
              154  STORE_FAST               'baseline_names'

 L.1678       156  LOAD_DEREF               'self'
              158  LOAD_METHOD              feature_flags
              160  LOAD_FAST                'baseline_names'
              162  CALL_METHOD_1         1  ''
              164  LOAD_DEREF               'self'
              166  STORE_ATTR               parse_baseline_flags

 L.1679       168  LOAD_DEREF               'self'
              170  LOAD_METHOD              feature_sorted

 L.1680       172  LOAD_DEREF               'self'
              174  LOAD_METHOD              feature_implies_c
              176  LOAD_FAST                'baseline_names'
              178  CALL_METHOD_1         1  ''

 L.1679       180  CALL_METHOD_1         1  ''
              182  LOAD_DEREF               'self'
              184  STORE_ATTR               parse_baseline_names
            186_0  COME_FROM           132  '132'

 L.1683       186  LOAD_DEREF               'self'
              188  LOAD_METHOD              dist_log
              190  LOAD_STR                 'check requested dispatch-able features'
              192  CALL_METHOD_1         1  ''
              194  POP_TOP          

 L.1684       196  LOAD_FAST                'cpu_dispatch'
              198  LOAD_CONST               None
              200  COMPARE_OP               is-not
          202_204  POP_JUMP_IF_FALSE   292  'to 292'

 L.1685       206  LOAD_DEREF               'self'
              208  LOAD_METHOD              _parse_arg_features
              210  LOAD_STR                 'cpu_dispatch'
              212  LOAD_FAST                'cpu_dispatch'
              214  CALL_METHOD_2         2  ''
              216  STORE_FAST               'cpu_dispatch_'

 L.1686       218  LOAD_CLOSURE             'self'
              220  BUILD_TUPLE_1         1 
              222  LOAD_SETCOMP             '<code_object <setcomp>>'
              224  LOAD_STR                 '_Parse.__init__.<locals>.<setcomp>'
              226  MAKE_FUNCTION_8          'closure'

 L.1687       228  LOAD_FAST                'cpu_dispatch_'

 L.1686       230  GET_ITER         
              232  CALL_FUNCTION_1       1  ''
              234  STORE_FAST               'cpu_dispatch'

 L.1690       236  LOAD_FAST                'cpu_dispatch_'
              238  LOAD_METHOD              difference
              240  LOAD_FAST                'cpu_dispatch'
              242  CALL_METHOD_1         1  ''
              244  STORE_FAST               'conflict_baseline'

 L.1691       246  LOAD_DEREF               'self'
              248  LOAD_METHOD              feature_sorted

 L.1692       250  LOAD_DEREF               'self'
              252  LOAD_METHOD              feature_names
              254  LOAD_FAST                'cpu_dispatch'
              256  CALL_METHOD_1         1  ''

 L.1691       258  CALL_METHOD_1         1  ''
              260  LOAD_DEREF               'self'
              262  STORE_ATTR               parse_dispatch_names

 L.1694       264  LOAD_GLOBAL              len
              266  LOAD_FAST                'conflict_baseline'
              268  CALL_FUNCTION_1       1  ''
              270  LOAD_CONST               0
              272  COMPARE_OP               >
          274_276  POP_JUMP_IF_FALSE   292  'to 292'

 L.1695       278  LOAD_DEREF               'self'
              280  LOAD_METHOD              dist_log

 L.1696       282  LOAD_STR                 'skip features'

 L.1696       284  LOAD_FAST                'conflict_baseline'

 L.1696       286  LOAD_STR                 'since its part of baseline'

 L.1695       288  CALL_METHOD_3         3  ''
              290  POP_TOP          
            292_0  COME_FROM           274  '274'
            292_1  COME_FROM           202  '202'

 L.1699       292  LOAD_DEREF               'self'
              294  LOAD_METHOD              dist_log
              296  LOAD_STR                 'initialize targets groups'
              298  CALL_METHOD_1         1  ''
              300  POP_TOP          

 L.1700       302  LOAD_DEREF               'self'
              304  LOAD_ATTR                conf_target_groups
              306  LOAD_METHOD              items
              308  CALL_METHOD_0         0  ''
              310  GET_ITER         
              312  FOR_ITER            412  'to 412'
              314  UNPACK_SEQUENCE_2     2 
              316  STORE_FAST               'group_name'
              318  STORE_FAST               'tokens'

 L.1701       320  LOAD_DEREF               'self'
              322  LOAD_METHOD              dist_log
              324  LOAD_STR                 'parse target group'
              326  LOAD_FAST                'group_name'
              328  CALL_METHOD_2         2  ''
              330  POP_TOP          

 L.1702       332  LOAD_FAST                'group_name'
              334  LOAD_METHOD              upper
              336  CALL_METHOD_0         0  ''
              338  STORE_FAST               'GROUP_NAME'

 L.1703       340  LOAD_FAST                'tokens'
          342_344  POP_JUMP_IF_FALSE   356  'to 356'
              346  LOAD_FAST                'tokens'
              348  LOAD_METHOD              strip
              350  CALL_METHOD_0         0  ''
          352_354  POP_JUMP_IF_TRUE    376  'to 376'
            356_0  COME_FROM           342  '342'

 L.1708       356  LOAD_CONST               False

 L.1708       358  BUILD_LIST_0          0 

 L.1708       360  BUILD_LIST_0          0 

 L.1707       362  BUILD_TUPLE_3         3 
              364  LOAD_DEREF               'self'
              366  LOAD_ATTR                parse_target_groups
              368  LOAD_FAST                'GROUP_NAME'
              370  STORE_SUBSCR     

 L.1710   372_374  JUMP_BACK           312  'to 312'
            376_0  COME_FROM           352  '352'

 L.1712       376  LOAD_DEREF               'self'
              378  LOAD_METHOD              _parse_target_tokens
              380  LOAD_FAST                'tokens'
              382  CALL_METHOD_1         1  ''

 L.1711       384  UNPACK_SEQUENCE_3     3 
              386  STORE_FAST               'has_baseline'
              388  STORE_FAST               'features'
              390  STORE_FAST               'extra_flags'

 L.1714       392  LOAD_FAST                'has_baseline'

 L.1714       394  LOAD_FAST                'features'

 L.1714       396  LOAD_FAST                'extra_flags'

 L.1713       398  BUILD_TUPLE_3         3 
              400  LOAD_DEREF               'self'
              402  LOAD_ATTR                parse_target_groups
              404  LOAD_FAST                'GROUP_NAME'
              406  STORE_SUBSCR     
          408_410  JUMP_BACK           312  'to 312'

 L.1717       412  LOAD_CONST               True
              414  LOAD_DEREF               'self'
              416  STORE_ATTR               parse_is_cached

Parse error at or near `LOAD_SETCOMP' instruction at offset 222

    def parse_targets(self, source):
        """
        Fetch and parse configuration statements that required for
        defining the targeted CPU features, statements should be declared
        in the top of source in between **C** comment and start
        with a special mark **@targets**.

        Configuration statements are sort of keywords representing
        CPU features names, group of statements and policies, combined
        together to determine the required optimization.

        Parameters
        ----------
        source: str
            the path of **C** source file.

        Returns
        -------
        - bool, True if group has the 'baseline' option
        - list, list of CPU features
        - list, list of extra compiler flags
        """
        self.dist_log("looking for '@targets' inside -> ", source)
        with open(source) as (fd):
            tokens = ''
            max_to_reach = 1000
            start_with = '@targets'
            start_pos = -1
            end_with = '*/'
            end_pos = -1
            for current_line, line in enumerate(fd):
                if current_line == max_to_reach:
                    self.dist_fatal('reached the max of lines')
                    break
                if start_pos == -1:
                    start_pos = line.find(start_with)
                    if start_pos == -1:
                        pass
                    else:
                        start_pos += len(start_with)
                tokens += line
                end_pos = line.find(end_with)
                if end_pos != -1:
                    end_pos += len(tokens) - len(line)
                    break

        if start_pos == -1:
            self.dist_fatal("expected to find '%s' within a C comment" % start_with)
        if end_pos == -1:
            self.dist_fatal("expected to end with '%s'" % end_with)
        tokens = tokens[start_pos:end_pos]
        return self._parse_target_tokens(tokens)

    _parse_regex_arg = re.compile('\\s|[,]|([+-])')

    def _parse_arg_features(self, arg_name, req_features):
        if not isinstance(req_features, str):
            self.dist_fatal("expected a string in '%s'" % arg_name)
        final_features = set()
        tokens = list(filter(None, re.split(self._parse_regex_arg, req_features)))
        append = True
        for tok in tokens:
            if tok[0] in ('#', '$'):
                self.dist_fatal(arg_name, "target groups and policies aren't allowed from arguments, only from dispatch-able sources")
            if tok == '+':
                append = True
            elif tok == '-':
                append = False
            else:
                TOK = tok.upper()
                features_to = set()
                if TOK == 'NONE':
                    break
                if TOK == 'NATIVE':
                    native = self.cc_flags['native']
                    if not native:
                        self.dist_fatal(arg_name, "native option isn't supported by the compiler")
                    features_to = self.feature_names(force_flags=native)
                else:
                    if TOK == 'MAX':
                        features_to = self.feature_supported.keys()
                    else:
                        if TOK == 'MIN':
                            features_to = self.feature_min
                        else:
                            if TOK in self.feature_supported:
                                features_to.add(TOK)
                            else:
                                if not self.feature_is_exist(TOK):
                                    self.dist_fatal(arg_name, ", '%s' isn't a known feature or option" % tok)
                                elif append:
                                    final_features = final_features.union(features_to)
                                else:
                                    final_features = final_features.difference(features_to)
                append = True
        else:
            return final_features

    _parse_regex_target = re.compile('\\s|[*,/]|([()])')

    def _parse_target_tokens(self, tokens):
        assert isinstance(tokens, str)
        final_targets = []
        extra_flags = []
        has_baseline = False
        skipped = set()
        policies = set()
        multi_target = None
        tokens = list(filter(None, re.split(self._parse_regex_target, tokens)))
        if not tokens:
            self.dist_fatal('expected one token at least')
        for tok in tokens:
            TOK = tok.upper()
            ch = tok[0]
            if ch in ('+', '-'):
                self.dist_fatal("+/- are 'not' allowed from target's groups or @targets, only from cpu_baseline and cpu_dispatch parms")
            elif ch == '$':
                if multi_target is not None:
                    self.dist_fatal("policies aren't allowed inside multi-target '()', only CPU features")
                policies.add(self._parse_token_policy(TOK))
            elif ch == '#':
                if multi_target is not None:
                    self.dist_fatal("target groups aren't allowed inside multi-target '()', only CPU features")
                has_baseline, final_targets, extra_flags = self._parse_token_group(TOK, has_baseline, final_targets, extra_flags)
            elif ch == '(':
                if multi_target is not None:
                    self.dist_fatal("unclosed multi-target, missing ')'")
                multi_target = set()
            elif ch == ')':
                if multi_target is None:
                    self.dist_fatal("multi-target opener '(' wasn't found")
                else:
                    targets = self._parse_multi_target(multi_target)
                    if targets is None:
                        skipped.add(tuple(multi_target))
                    else:
                        if len(targets) == 1:
                            targets = targets[0]
                    if targets:
                        if targets not in final_targets:
                            final_targets.append(targets)
                multi_target = None
            elif TOK == 'BASELINE':
                if multi_target is not None:
                    self.dist_fatal("baseline isn't allowed inside multi-target '()'")
                has_baseline = True
            elif multi_target is not None:
                multi_target.add(TOK)
        else:
            if not self.feature_is_exist(TOK):
                self.dist_fatal("invalid target name '%s'" % TOK)
            is_enabled = TOK in self.parse_baseline_names or TOK in self.parse_dispatch_names
            if is_enabled:
                if TOK not in final_targets:
                    final_targets.append(TOK)
                else:
                    skipped.add(TOK)
            if multi_target is not None:
                self.dist_fatal("unclosed multi-target, missing ')'")
            if skipped:
                self.dist_log('skip targets', skipped, 'not part of baseline or dispatch-able features')
            final_targets = self.feature_untied(final_targets)
            for p in list(policies):
                _, _, deps = self._parse_policies[p]

        for d in deps:
            if d in policies:
                pass
            else:
                self.dist_log("policy '%s' force enables '%s'" % (
                 p, d))
                policies.add(d)
        else:
            for p, (have, nhave, _) in self._parse_policies.items():
                func = None
                if p in policies:
                    func = have
                    self.dist_log("policy '%s' is ON" % p)
                else:
                    func = nhave
                if not func:
                    pass
                else:
                    has_baseline, final_targets, extra_flags = func(has_baseline, final_targets, extra_flags)
            else:
                return (
                 has_baseline, final_targets, extra_flags)

    def _parse_token_policy(self, token):
        """validate policy token"""
        if len(token) <= 1 or token[-1:] == token[0]:
            self.dist_fatal("'$' must stuck in the begin of policy name")
        token = token[1:]
        if token not in self._parse_policies:
            self.dist_fatal("'%s' is an invalid policy name, available policies are" % token, self._parse_policies.keys())
        return token

    def _parse_token_group(self, token, has_baseline, final_targets, extra_flags):
        """validate group token"""
        if len(token) <= 1 or token[-1:] == token[0]:
            self.dist_fatal("'#' must stuck in the begin of group name")
        token = token[1:]
        ghas_baseline, gtargets, gextra_flags = self.parse_target_groups.get(token, (False, None, []))
        if gtargets is None:
            self.dist_fatal("'%s' is an invalid target group name, " % token + 'available target groups are', self.parse_target_groups.keys())
        if ghas_baseline:
            has_baseline = True
        final_targets += [f for f in gtargets if f not in final_targets]
        extra_flags += [f for f in gextra_flags if f not in extra_flags]
        return (has_baseline, final_targets, extra_flags)

    def _parse_multi_target(self, targets):
        """validate multi targets that defined between parentheses()"""
        if not targets:
            self.dist_fatal("empty multi-target '()'")
        else:
            if not all([self.feature_is_exist(tar) for tar in targets]):
                self.dist_fatal('invalid target name in multi-target', targets)
            else:
                return all([tar in self.parse_baseline_names or tar in self.parse_dispatch_names for tar in targets]) or None
            targets = self.feature_ahead(targets)
            return targets or None
        targets = self.feature_sorted(targets)
        targets = tuple(targets)
        return targets

    def _parse_policy_not_keepbase(self, has_baseline, final_targets, extra_flags):
        """skip all baseline features"""
        skipped = []
        for tar in final_targets[:]:
            is_base = False
            if isinstance(tar, str):
                is_base = tar in self.parse_baseline_names
            else:
                is_base = all([f in self.parse_baseline_names for f in tar])
            if is_base:
                skipped.append(tar)
                final_targets.remove(tar)
            if skipped:
                self.dist_log('skip baseline features', skipped)
            return (has_baseline, final_targets, extra_flags)

    def _parse_policy_keepsort(self, has_baseline, final_targets, extra_flags):
        """leave a notice that $keep_sort is on"""
        self.dist_log("policy 'keep_sort' is on, dispatch-able targets", final_targets, "\nare 'not' sorted depend on the highest interest butas specified in the dispatch-able source or the extra group")
        return (
         has_baseline, final_targets, extra_flags)

    def _parse_policy_not_keepsort(self, has_baseline, final_targets, extra_flags):
        """sorted depend on the highest interest"""
        final_targets = self.feature_sorted(final_targets, reverse=True)
        return (has_baseline, final_targets, extra_flags)

    def _parse_policy_maxopt(self, has_baseline, final_targets, extra_flags):
        """append the compiler optimization flags"""
        if self.cc_has_debug:
            self.dist_log("debug mode is detected, policy 'maxopt' is skipped.")
        else:
            if self.cc_noopt:
                self.dist_log("optimization is disabled, policy 'maxopt' is skipped.")
            else:
                flags = self.cc_flags['opt']
                if not flags:
                    self.dist_log("current compiler doesn't support optimization flags, policy 'maxopt' is skipped",
                      stderr=True)
                else:
                    extra_flags += flags
        return (
         has_baseline, final_targets, extra_flags)

    def _parse_policy_werror(self, has_baseline, final_targets, extra_flags):
        """force warnings to treated as errors"""
        flags = self.cc_flags['werror']
        if not flags:
            self.dist_log("current compiler doesn't support werror flags, warnings will 'not' treated as errors",
              stderr=True)
        else:
            self.dist_log('compiler warnings are treated as errors')
            extra_flags += flags
        return (
         has_baseline, final_targets, extra_flags)

    def _parse_policy_autovec(self, has_baseline, final_targets, extra_flags):
        """skip features that has no auto-vectorized support by compiler"""
        skipped = []
        for tar in final_targets[:]:
            if isinstance(tar, str):
                can = self.feature_can_autovec(tar)
            else:
                can = all([self.feature_can_autovec(t) for t in tar])
            if not can:
                final_targets.remove(tar)
                skipped.append(tar)
            if skipped:
                self.dist_log('skip non auto-vectorized features', skipped)
            return (has_baseline, final_targets, extra_flags)


class CCompilerOpt(_Config, _Distutils, _Cache, _CCompiler, _Feature, _Parse):
    __doc__ = '\n    A helper class for `CCompiler` aims to provide extra build options\n    to effectively control of compiler optimizations that are directly\n    related to CPU features.\n    '

    def __init__(self, ccompiler, cpu_baseline='min', cpu_dispatch='max', cache_path=None):
        _Config.__init__(self)
        _Distutils.__init__(self, ccompiler)
        _Cache.__init__(self, cache_path, self.dist_info(), cpu_baseline, cpu_dispatch)
        _CCompiler.__init__(self)
        _Feature.__init__(self)
        if not self.cc_noopt:
            if self.cc_has_native:
                self.dist_log("native flag is specified through environment variables. force cpu-baseline='native'")
                cpu_baseline = 'native'
        _Parse.__init__(self, cpu_baseline, cpu_dispatch)
        self._requested_baseline = cpu_baseline
        self._requested_dispatch = cpu_dispatch
        self.sources_status = getattr(self, 'sources_status', {})
        self.cache_private.add('sources_status')
        self.hit_cache = hasattr(self, 'hit_cache')

    def is_cached(self):
        """
        Returns True if the class loaded from the cache file
        """
        return self.cache_infile and self.hit_cache

    def cpu_baseline_flags(self):
        """
        Returns a list of final CPU baseline compiler flags
        """
        return self.parse_baseline_flags

    def cpu_baseline_names(self):
        """
        return a list of final CPU baseline feature names
        """
        return self.parse_baseline_names

    def cpu_dispatch_names(self):
        """
        return a list of final CPU dispatch feature names
        """
        return self.parse_dispatch_names

    def try_dispatch(self, sources, src_dir=None, **kwargs):
        """
        Compile one or more dispatch-able sources and generates object files,
        also generates abstract C config headers and macros that
        used later for the final runtime dispatching process.

        The mechanism behind it is to takes each source file that specified
        in 'sources' and branching it into several files depend on
        special configuration statements that must be declared in the
        top of each source which contains targeted CPU features,
        then it compiles every branched source with the proper compiler flags.

        Parameters
        ----------
        sources : list
            Must be a list of dispatch-able sources file paths,
            and configuration statements must be declared inside
            each file.

        src_dir : str
            Path of parent directory for the generated headers and wrapped sources.
            If None(default) the files will generated in-place.

        **kwargs : any
            Arguments to pass on to the `CCompiler.compile()`

        Returns
        -------
        list : generated object files

        Raises
        ------
        CompileError
            Raises by `CCompiler.compile()` on compiling failure.
        DistutilsError
            Some errors during checking the sanity of configuration statements.

        See Also
        --------
        parse_targets :
            Parsing the configuration statements of dispatch-able sources.
        """
        to_compile = {}
        baseline_flags = self.cpu_baseline_flags()
        include_dirs = kwargs.setdefault('include_dirs', [])
        for src in sources:
            output_dir = os.path.dirname(src)
            if src_dir:
                if not output_dir.startswith(src_dir):
                    output_dir = os.path.join(src_dir, output_dir)
                if output_dir not in include_dirs:
                    include_dirs.append(output_dir)
            has_baseline, targets, extra_flags = self.parse_targets(src)
            nochange = self._generate_config(output_dir, src, targets, has_baseline)
            for tar in targets:
                tar_src = self._wrap_target(output_dir, src, tar, nochange=nochange)
                flags = tuple(extra_flags + self.feature_flags(tar))
                to_compile.setdefault(flags, []).append(tar_src)
            else:
                if has_baseline:
                    flags = tuple(extra_flags + baseline_flags)
                    to_compile.setdefault(flags, []).append(src)
                self.sources_status[src] = (has_baseline, targets)

        else:
            objects = []
            for flags, srcs in to_compile.items():
                objects += (self.dist_compile)(srcs, (list(flags)), **kwargs)
            else:
                return objects

    def generate_dispatch_header(self, header_path):
        """
        Generate the dispatch header which contains the #definitions and headers
        for platform-specific instruction-sets for the enabled CPU baseline and
        dispatch-able features.

        Its highly recommended to take a look at the generated header
        also the generated source files via `try_dispatch()`
        in order to get the full picture.
        """
        self.dist_log('generate CPU dispatch header: (%s)' % header_path)
        baseline_names = self.cpu_baseline_names()
        dispatch_names = self.cpu_dispatch_names()
        baseline_len = len(baseline_names)
        dispatch_len = len(dispatch_names)
        header_dir = os.path.dirname(header_path)
        if not os.path.exists(header_dir):
            self.dist_log(f"dispatch header dir {header_dir} does not exist, creating it",
              stderr=True)
            os.makedirs(header_dir)
        with open(header_path, 'w') as (f):
            baseline_calls = ' \\\n'.join(['\t%sWITH_CPU_EXPAND_(MACRO_TO_CALL(%s, __VA_ARGS__))' % (
             self.conf_c_prefix, f) for f in baseline_names])
            dispatch_calls = ' \\\n'.join(['\t%sWITH_CPU_EXPAND_(MACRO_TO_CALL(%s, __VA_ARGS__))' % (
             self.conf_c_prefix, f) for f in dispatch_names])
            f.write(textwrap.dedent('                /*\n                 * AUTOGENERATED DON\'T EDIT\n                 * Please make changes to the code generator (distutils/ccompiler_opt.py)\n                */\n                #define {pfx}WITH_CPU_BASELINE  "{baseline_str}"\n                #define {pfx}WITH_CPU_DISPATCH  "{dispatch_str}"\n                #define {pfx}WITH_CPU_BASELINE_N {baseline_len}\n                #define {pfx}WITH_CPU_DISPATCH_N {dispatch_len}\n                #define {pfx}WITH_CPU_EXPAND_(X) X\n                #define {pfx}WITH_CPU_BASELINE_CALL(MACRO_TO_CALL, ...) \\\n                {baseline_calls}\n                #define {pfx}WITH_CPU_DISPATCH_CALL(MACRO_TO_CALL, ...) \\\n                {dispatch_calls}\n            ').format(pfx=(self.conf_c_prefix),
              baseline_str=(' '.join(baseline_names)),
              dispatch_str=(' '.join(dispatch_names)),
              baseline_len=baseline_len,
              dispatch_len=dispatch_len,
              baseline_calls=baseline_calls,
              dispatch_calls=dispatch_calls))
            baseline_pre = ''
            for name in baseline_names:
                baseline_pre += self.feature_c_preprocessor(name, tabs=1) + '\n'
            else:
                dispatch_pre = ''
                for name in dispatch_names:
                    dispatch_pre += textwrap.dedent('                #ifdef {pfx}CPU_TARGET_{name}\n                {pre}\n                #endif /*{pfx}CPU_TARGET_{name}*/\n                ').format(pfx=(self.conf_c_prefix_),
                      name=name,
                      pre=self.feature_c_preprocessor(name,
                      tabs=1))
                else:
                    f.write(textwrap.dedent('            /******* baseline features *******/\n            {baseline_pre}\n            /******* dispatch features *******/\n            {dispatch_pre}\n            ').format(pfx=(self.conf_c_prefix_),
                      baseline_pre=baseline_pre,
                      dispatch_pre=dispatch_pre))

    def report(self, full=False):
        report = []
        platform_rows = []
        baseline_rows = []
        dispatch_rows = []
        report.append(('Platform', platform_rows))
        report.append(('', ''))
        report.append(('CPU baseline', baseline_rows))
        report.append(('', ''))
        report.append(('CPU dispatch', dispatch_rows))
        platform_rows.append(('Architecture',
         'unsupported' if self.cc_on_noarch else self.cc_march))
        platform_rows.append(('Compiler',
         'unix-like' if self.cc_is_nocc else self.cc_name))
        if self.cc_noopt:
            baseline_rows.append(('Requested', 'optimization disabled'))
        else:
            baseline_rows.append(('Requested', repr(self._requested_baseline)))
        baseline_names = self.cpu_baseline_names()
        baseline_rows.append((
         'Enabled', ' '.join(baseline_names) if baseline_names else 'none'))
        baseline_flags = self.cpu_baseline_flags()
        baseline_rows.append((
         'Flags', ' '.join(baseline_flags) if baseline_flags else 'none'))
        extra_checks = []
        for name in baseline_names:
            extra_checks += self.feature_extra_checks(name)
        else:
            baseline_rows.append((
             'Extra checks', ' '.join(extra_checks) if extra_checks else 'none'))
            if self.cc_noopt:
                baseline_rows.append(('Requested', 'optimization disabled'))
            else:
                dispatch_rows.append(('Requested', repr(self._requested_dispatch)))
            dispatch_names = self.cpu_dispatch_names()
            dispatch_rows.append((
             'Enabled', ' '.join(dispatch_names) if dispatch_names else 'none'))
            target_sources = {}
            for source, (_, targets) in self.sources_status.items():
                for tar in targets:
                    target_sources.setdefault(tar, []).append(source)

        if full:
            generated = target_sources or ''
            for tar in self.feature_sorted(target_sources):
                sources = target_sources[tar]
                name = tar if isinstance(tar, str) else '(%s)' % ' '.join(tar)
                generated += name + '[%d] ' % len(sources)
            else:
                dispatch_rows.append(('Generated', generated[:-1] if generated else 'none'))

        else:
            dispatch_rows.append(('Generated', ''))
            for tar in self.feature_sorted(target_sources):
                sources = target_sources[tar]
                pretty_name = tar if isinstance(tar, str) else '(%s)' % ' '.join(tar)
                flags = ' '.join(self.feature_flags(tar))
                implies = ' '.join(self.feature_sorted(self.feature_implies(tar)))
                detect = ' '.join(self.feature_detect(tar))
                extra_checks = []

            for name in (tar,) if isinstance(tar, str) else tar:
                extra_checks += self.feature_extra_checks(name)
            else:
                extra_checks = ' '.join(extra_checks) if extra_checks else 'none'
                dispatch_rows.append(('', ''))
                dispatch_rows.append((pretty_name, implies))
                dispatch_rows.append(('Flags', flags))
                dispatch_rows.append(('Extra checks', extra_checks))
                dispatch_rows.append(('Detect', detect))
                for src in sources:
                    dispatch_rows.append(('', src))
                else:
                    text = []
                    secs_len = [len(secs) for secs, _ in report]
                    cols_len = [len(col) for _, rows in report for col, _ in rows]
                    tab = '  '
                    pad = max(max(secs_len), max(cols_len))

            for sec, rows in report:
                if not sec:
                    text.append('')
                else:
                    sec += ' ' * (pad - len(sec))
                    text.append(sec + tab + ': ')
                    for col, val in rows:
                        col += ' ' * (pad - len(col))
                        text.append(tab + col + ': ' + val)
                    else:
                        return '\n'.join(text)

    def _wrap_target(self, output_dir, dispatch_src, target, nochange=False):
        if not isinstance(target, (str, tuple)):
            raise AssertionError
        elif isinstance(target, str):
            ext_name = target_name = target
        else:
            ext_name = '.'.join(target)
            target_name = '__'.join(target)
        wrap_path = os.path.join(output_dir, os.path.basename(dispatch_src))
        wrap_path = ('{0}.{2}{1}'.format)(*os.path.splitext(wrap_path), *(ext_name.lower(),))
        if nochange:
            if os.path.exists(wrap_path):
                return wrap_path
        self.dist_log('wrap dispatch-able target -> ', wrap_path)
        features = self.feature_sorted(self.feature_implies_c(target))
        target_join = '#define %sCPU_TARGET_' % self.conf_c_prefix_
        target_defs = [target_join + f for f in features]
        target_defs = '\n'.join(target_defs)
        with open(wrap_path, 'w') as (fd):
            fd.write(textwrap.dedent('            /**\n             * AUTOGENERATED DON\'T EDIT\n             * Please make changes to the code generator              (distutils/ccompiler_opt.py)\n             */\n            #define {pfx}CPU_TARGET_MODE\n            #define {pfx}CPU_TARGET_CURRENT {target_name}\n            {target_defs}\n            #include "{path}"\n            ').format(pfx=(self.conf_c_prefix_),
              target_name=target_name,
              path=(os.path.abspath(dispatch_src)),
              target_defs=target_defs))
        return wrap_path

    def _generate_config--- This code section failed: ---

 L.2457         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              basename
                6  LOAD_FAST                'dispatch_src'
                8  CALL_METHOD_1         1  ''
               10  LOAD_METHOD              replace
               12  LOAD_STR                 '.c'
               14  LOAD_STR                 '.h'
               16  CALL_METHOD_2         2  ''
               18  STORE_FAST               'config_path'

 L.2458        20  LOAD_GLOBAL              os
               22  LOAD_ATTR                path
               24  LOAD_METHOD              join
               26  LOAD_FAST                'output_dir'
               28  LOAD_FAST                'config_path'
               30  CALL_METHOD_2         2  ''
               32  STORE_FAST               'config_path'

 L.2460        34  LOAD_FAST                'self'
               36  LOAD_METHOD              cache_hash
               38  LOAD_FAST                'targets'
               40  LOAD_FAST                'has_baseline'
               42  CALL_METHOD_2         2  ''
               44  STORE_FAST               'cache_hash'

 L.2461        46  SETUP_FINALLY       130  'to 130'

 L.2462        48  LOAD_GLOBAL              open
               50  LOAD_FAST                'config_path'
               52  CALL_FUNCTION_1       1  ''
               54  SETUP_WITH          120  'to 120'
               56  STORE_FAST               'f'

 L.2463        58  LOAD_FAST                'f'
               60  LOAD_METHOD              readline
               62  CALL_METHOD_0         0  ''
               64  LOAD_METHOD              split
               66  LOAD_STR                 'cache_hash:'
               68  CALL_METHOD_1         1  ''
               70  STORE_FAST               'last_hash'

 L.2464        72  LOAD_GLOBAL              len
               74  LOAD_FAST                'last_hash'
               76  CALL_FUNCTION_1       1  ''
               78  LOAD_CONST               2
               80  COMPARE_OP               ==
               82  POP_JUMP_IF_FALSE   116  'to 116'
               84  LOAD_GLOBAL              int
               86  LOAD_FAST                'last_hash'
               88  LOAD_CONST               1
               90  BINARY_SUBSCR    
               92  CALL_FUNCTION_1       1  ''
               94  LOAD_FAST                'cache_hash'
               96  COMPARE_OP               ==
               98  POP_JUMP_IF_FALSE   116  'to 116'

 L.2465       100  POP_BLOCK        
              102  BEGIN_FINALLY    
              104  WITH_CLEANUP_START
              106  WITH_CLEANUP_FINISH
              108  POP_FINALLY           0  ''
              110  POP_BLOCK        
              112  LOAD_CONST               True
              114  RETURN_VALUE     
            116_0  COME_FROM            98  '98'
            116_1  COME_FROM            82  '82'
              116  POP_BLOCK        
              118  BEGIN_FINALLY    
            120_0  COME_FROM_WITH       54  '54'
              120  WITH_CLEANUP_START
              122  WITH_CLEANUP_FINISH
              124  END_FINALLY      
              126  POP_BLOCK        
              128  JUMP_FORWARD        150  'to 150'
            130_0  COME_FROM_FINALLY    46  '46'

 L.2466       130  DUP_TOP          
              132  LOAD_GLOBAL              IOError
              134  COMPARE_OP               exception-match
              136  POP_JUMP_IF_FALSE   148  'to 148'
              138  POP_TOP          
              140  POP_TOP          
              142  POP_TOP          

 L.2467       144  POP_EXCEPT       
              146  JUMP_FORWARD        150  'to 150'
            148_0  COME_FROM           136  '136'
              148  END_FINALLY      
            150_0  COME_FROM           146  '146'
            150_1  COME_FROM           128  '128'

 L.2469       150  LOAD_FAST                'self'
              152  LOAD_METHOD              dist_log
              154  LOAD_STR                 'generate dispatched config -> '
              156  LOAD_FAST                'config_path'
              158  CALL_METHOD_2         2  ''
              160  POP_TOP          

 L.2470       162  BUILD_LIST_0          0 
              164  STORE_FAST               'dispatch_calls'

 L.2471       166  LOAD_FAST                'targets'
              168  GET_ITER         
              170  FOR_ITER            264  'to 264'
              172  STORE_FAST               'tar'

 L.2472       174  LOAD_GLOBAL              isinstance
              176  LOAD_FAST                'tar'
              178  LOAD_GLOBAL              str
              180  CALL_FUNCTION_2       2  ''
              182  POP_JUMP_IF_FALSE   190  'to 190'

 L.2473       184  LOAD_FAST                'tar'
              186  STORE_FAST               'target_name'
              188  JUMP_FORWARD        210  'to 210'
            190_0  COME_FROM           182  '182'

 L.2475       190  LOAD_STR                 '__'
              192  LOAD_METHOD              join
              194  LOAD_LISTCOMP            '<code_object <listcomp>>'
              196  LOAD_STR                 'CCompilerOpt._generate_config.<locals>.<listcomp>'
              198  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              200  LOAD_FAST                'tar'
              202  GET_ITER         
              204  CALL_FUNCTION_1       1  ''
              206  CALL_METHOD_1         1  ''
              208  STORE_FAST               'target_name'
            210_0  COME_FROM           188  '188'

 L.2476       210  LOAD_FAST                'self'
              212  LOAD_METHOD              feature_detect
              214  LOAD_FAST                'tar'
              216  CALL_METHOD_1         1  ''
              218  STORE_FAST               'req_detect'

 L.2477       220  LOAD_STR                 '&&'
              222  LOAD_METHOD              join
              224  LOAD_LISTCOMP            '<code_object <listcomp>>'
              226  LOAD_STR                 'CCompilerOpt._generate_config.<locals>.<listcomp>'
              228  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.2478       230  LOAD_FAST                'req_detect'

 L.2477       232  GET_ITER         
              234  CALL_FUNCTION_1       1  ''
              236  CALL_METHOD_1         1  ''
              238  STORE_FAST               'req_detect'

 L.2480       240  LOAD_FAST                'dispatch_calls'
              242  LOAD_METHOD              append

 L.2481       244  LOAD_STR                 '\t%sCPU_DISPATCH_EXPAND_(CB((%s), %s, __VA_ARGS__))'

 L.2482       246  LOAD_FAST                'self'
              248  LOAD_ATTR                conf_c_prefix_

 L.2482       250  LOAD_FAST                'req_detect'

 L.2482       252  LOAD_FAST                'target_name'

 L.2481       254  BUILD_TUPLE_3         3 
              256  BINARY_MODULO    

 L.2480       258  CALL_METHOD_1         1  ''
              260  POP_TOP          
              262  JUMP_BACK           170  'to 170'

 L.2484       264  LOAD_STR                 ' \\\n'
              266  LOAD_METHOD              join
              268  LOAD_FAST                'dispatch_calls'
              270  CALL_METHOD_1         1  ''
              272  STORE_FAST               'dispatch_calls'

 L.2486       274  LOAD_FAST                'has_baseline'
          276_278  POP_JUMP_IF_FALSE   292  'to 292'

 L.2488       280  LOAD_STR                 '\t%sCPU_DISPATCH_EXPAND_(CB(__VA_ARGS__))'

 L.2489       282  LOAD_FAST                'self'
              284  LOAD_ATTR                conf_c_prefix_

 L.2487       286  BINARY_MODULO    
              288  STORE_FAST               'baseline_calls'
              290  JUMP_FORWARD        296  'to 296'
            292_0  COME_FROM           276  '276'

 L.2491       292  LOAD_STR                 ''
              294  STORE_FAST               'baseline_calls'
            296_0  COME_FROM           290  '290'

 L.2493       296  LOAD_GLOBAL              open
              298  LOAD_FAST                'config_path'
              300  LOAD_STR                 'w'
              302  CALL_FUNCTION_2       2  ''
              304  SETUP_WITH          344  'to 344'
              306  STORE_FAST               'fd'

 L.2494       308  LOAD_FAST                'fd'
              310  LOAD_METHOD              write
              312  LOAD_GLOBAL              textwrap
              314  LOAD_METHOD              dedent
              316  LOAD_STR                 "            // cache_hash:{cache_hash}\n            /**\n             * AUTOGENERATED DON'T EDIT\n             * Please make changes to the code generator (distutils/ccompiler_opt.py)\n             */\n            #ifndef {pfx}CPU_DISPATCH_EXPAND_\n                #define {pfx}CPU_DISPATCH_EXPAND_(X) X\n            #endif\n            #undef {pfx}CPU_DISPATCH_BASELINE_CALL\n            #undef {pfx}CPU_DISPATCH_CALL\n            #define {pfx}CPU_DISPATCH_BASELINE_CALL(CB, ...) \\\n            {baseline_calls}\n            #define {pfx}CPU_DISPATCH_CALL(CHK, CB, ...) \\\n            {dispatch_calls}\n            "
              318  CALL_METHOD_1         1  ''
              320  LOAD_ATTR                format

 L.2510       322  LOAD_FAST                'self'
              324  LOAD_ATTR                conf_c_prefix_

 L.2510       326  LOAD_FAST                'baseline_calls'

 L.2511       328  LOAD_FAST                'dispatch_calls'

 L.2511       330  LOAD_FAST                'cache_hash'

 L.2494       332  LOAD_CONST               ('pfx', 'baseline_calls', 'dispatch_calls', 'cache_hash')
              334  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              336  CALL_METHOD_1         1  ''
              338  POP_TOP          
              340  POP_BLOCK        
              342  BEGIN_FINALLY    
            344_0  COME_FROM_WITH      304  '304'
              344  WITH_CLEANUP_START
              346  WITH_CLEANUP_FINISH
              348  END_FINALLY      

 L.2513       350  LOAD_CONST               False
              352  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `BEGIN_FINALLY' instruction at offset 102


def new_ccompiler_opt(compiler, dispatch_hpath, **kwargs):
    """
    Create a new instance of 'CCompilerOpt' and generate the dispatch header
    which contains the #definitions and headers of platform-specific instruction-sets for
    the enabled CPU baseline and dispatch-able features.

    Parameters
    ----------
    compiler : CCompiler instance
    dispatch_hpath : str
        path of the dispatch header

    **kwargs: passed as-is to `CCompilerOpt(...)`
    Returns
    -------
    new instance of CCompilerOpt
    """
    opt = CCompilerOpt(compiler, **kwargs)
    if not (os.path.exists(dispatch_hpath) and opt.is_cached()):
        opt.generate_dispatch_header(dispatch_hpath)
    return opt