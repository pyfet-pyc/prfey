# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\numpy\distutils\cpuinfo.py
"""
cpuinfo

Copyright 2002 Pearu Peterson all rights reserved,
Pearu Peterson <pearu@cens.ioc.ee>
Permission to use, modify, and distribute this software is given under the
terms of the NumPy (BSD style) license.  See LICENSE.txt that came with
this distribution for specifics.

NO WARRANTY IS EXPRESSED OR IMPLIED.  USE AT YOUR OWN RISK.
Pearu Peterson

"""
from __future__ import division, absolute_import, print_function
__all__ = [
 'cpu']
import sys, re, types, os
if sys.version_info[0] >= 3:
    from subprocess import getstatusoutput
else:
    from commands import getstatusoutput
import warnings, platform
from numpy.distutils.compat import get_exception

def getoutput--- This code section failed: ---

 L.  33         0  SETUP_FINALLY        18  'to 18'

 L.  34         2  LOAD_GLOBAL              getstatusoutput
                4  LOAD_FAST                'cmd'
                6  CALL_FUNCTION_1       1  ''
                8  UNPACK_SEQUENCE_2     2 
               10  STORE_FAST               'status'
               12  STORE_FAST               'output'
               14  POP_BLOCK        
               16  JUMP_FORWARD         66  'to 66'
             18_0  COME_FROM_FINALLY     0  '0'

 L.  35        18  DUP_TOP          
               20  LOAD_GLOBAL              EnvironmentError
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    64  'to 64'
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L.  36        32  LOAD_GLOBAL              get_exception
               34  CALL_FUNCTION_0       0  ''
               36  STORE_FAST               'e'

 L.  37        38  LOAD_GLOBAL              warnings
               40  LOAD_ATTR                warn
               42  LOAD_GLOBAL              str
               44  LOAD_FAST                'e'
               46  CALL_FUNCTION_1       1  ''
               48  LOAD_GLOBAL              UserWarning
               50  LOAD_FAST                'stacklevel'
               52  LOAD_CONST               ('stacklevel',)
               54  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               56  POP_TOP          

 L.  38        58  POP_EXCEPT       
               60  LOAD_CONST               (False, '')
               62  RETURN_VALUE     
             64_0  COME_FROM            24  '24'
               64  END_FINALLY      
             66_0  COME_FROM            16  '16'

 L.  39        66  LOAD_GLOBAL              os
               68  LOAD_METHOD              WIFEXITED
               70  LOAD_FAST                'status'
               72  CALL_METHOD_1         1  ''
               74  POP_JUMP_IF_FALSE    98  'to 98'
               76  LOAD_GLOBAL              os
               78  LOAD_METHOD              WEXITSTATUS
               80  LOAD_FAST                'status'
               82  CALL_METHOD_1         1  ''
               84  LOAD_FAST                'successful_status'
               86  COMPARE_OP               in
               88  POP_JUMP_IF_FALSE    98  'to 98'

 L.  40        90  LOAD_CONST               True
               92  LOAD_FAST                'output'
               94  BUILD_TUPLE_2         2 
               96  RETURN_VALUE     
             98_0  COME_FROM            88  '88'
             98_1  COME_FROM            74  '74'

 L.  41        98  LOAD_CONST               False
              100  LOAD_FAST                'output'
              102  BUILD_TUPLE_2         2 
              104  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 60


def command_info(successful_status=(0,), stacklevel=1, **kw):
    info = {}
    for key in kw:
        ok, output = getoutput((kw[key]), successful_status=successful_status, stacklevel=(stacklevel + 1))
        if ok:
            info[key] = output.strip()
        return info


def command_by_line(cmd, successful_status=(0,), stacklevel=1):
    ok, output = getoutput(cmd, successful_status=successful_status, stacklevel=(stacklevel + 1))
    if not ok:
        return
    for line in output.splitlines():
        (yield line.strip())


def key_value_from_command(cmd, sep, successful_status=(0,), stacklevel=1):
    d = {}
    for line in command_by_line(cmd, successful_status=successful_status, stacklevel=(stacklevel + 1)):
        l = [s.strip() for s in line.split(sep, 1)]
        if len(l) == 2:
            d[l[0]] = l[1]
        return d


class CPUInfoBase(object):
    __doc__ = 'Holds CPU information and provides methods for requiring\n    the availability of various CPU features.\n    '

    def _try_call--- This code section failed: ---

 L.  76         0  SETUP_FINALLY        10  'to 10'

 L.  77         2  LOAD_FAST                'func'
                4  CALL_FUNCTION_0       0  ''
                6  POP_BLOCK        
                8  RETURN_VALUE     
             10_0  COME_FROM_FINALLY     0  '0'

 L.  78        10  DUP_TOP          
               12  LOAD_GLOBAL              Exception
               14  COMPARE_OP               exception-match
               16  POP_JUMP_IF_FALSE    28  'to 28'
               18  POP_TOP          
               20  POP_TOP          
               22  POP_TOP          

 L.  79        24  POP_EXCEPT       
               26  JUMP_FORWARD         30  'to 30'
             28_0  COME_FROM            16  '16'
               28  END_FINALLY      
             30_0  COME_FROM            26  '26'

Parse error at or near `POP_TOP' instruction at offset 20

    def __getattr__(self, name):
        if not name.startswith('_'):
            if hasattr(self, '_' + name):
                attr = getattr(self, '_' + name)
                if isinstance(attr, types.MethodType):
                    return lambda func=self._try_call, attr=attr: func(attr)
            else:
                return lambda : None
        raise AttributeError(name)

    def _getNCPUs(self):
        return 1

    def __get_nbits(self):
        abits = platform.architecture()[0]
        nbits = re.compile('(\\d+)bit').search(abits).group(1)
        return nbits

    def _is_32bit(self):
        return self._CPUInfoBase__get_nbits() == '32'

    def _is_64bit(self):
        return self._CPUInfoBase__get_nbits() == '64'


class LinuxCPUInfo(CPUInfoBase):
    info = None

    def __init__(self):
        if self.info is not None:
            return
        info = [{}]
        ok, output = getoutput('uname -m')
        if ok:
            info[0]['uname_m'] = output.strip()
        try:
            fo = open('/proc/cpuinfo')
        except EnvironmentError:
            e = get_exception()
            warnings.warn((str(e)), UserWarning, stacklevel=2)
        else:
            for line in fo:
                name_value = [s.strip() for s in line.split(':', 1)]
                if len(name_value) != 2:
                    pass
                else:
                    name, value = name_value
                    if not info or name in info[(-1)]:
                        info.append({})
                    info[(-1)][name] = value
            else:
                fo.close()

        self.__class__.info = info

    def _not_impl(self):
        pass

    def _is_AMD(self):
        return self.info[0]['vendor_id'] == 'AuthenticAMD'

    def _is_AthlonK6_2(self):
        return self._is_AMD() and self.info[0]['model'] == '2'

    def _is_AthlonK6_3(self):
        return self._is_AMD() and self.info[0]['model'] == '3'

    def _is_AthlonK6(self):
        return re.match('.*?AMD-K6', self.info[0]['model name']) is not None

    def _is_AthlonK7(self):
        return re.match('.*?AMD-K7', self.info[0]['model name']) is not None

    def _is_AthlonMP(self):
        return re.match('.*?Athlon\\(tm\\) MP\\b', self.info[0]['model name']) is not None

    def _is_AMD64(self):
        return self.is_AMD() and self.info[0]['family'] == '15'

    def _is_Athlon64(self):
        return re.match('.*?Athlon\\(tm\\) 64\\b', self.info[0]['model name']) is not None

    def _is_AthlonHX(self):
        return re.match('.*?Athlon HX\\b', self.info[0]['model name']) is not None

    def _is_Opteron(self):
        return re.match('.*?Opteron\\b', self.info[0]['model name']) is not None

    def _is_Hammer(self):
        return re.match('.*?Hammer\\b', self.info[0]['model name']) is not None

    def _is_Alpha(self):
        return self.info[0]['cpu'] == 'Alpha'

    def _is_EV4(self):
        return self.is_Alpha() and self.info[0]['cpu model'] == 'EV4'

    def _is_EV5(self):
        return self.is_Alpha() and self.info[0]['cpu model'] == 'EV5'

    def _is_EV56(self):
        return self.is_Alpha() and self.info[0]['cpu model'] == 'EV56'

    def _is_PCA56(self):
        return self.is_Alpha() and self.info[0]['cpu model'] == 'PCA56'

    _is_i386 = _not_impl

    def _is_Intel(self):
        return self.info[0]['vendor_id'] == 'GenuineIntel'

    def _is_i486(self):
        return self.info[0]['cpu'] == 'i486'

    def _is_i586(self):
        return self.is_Intel() and self.info[0]['cpu family'] == '5'

    def _is_i686(self):
        return self.is_Intel() and self.info[0]['cpu family'] == '6'

    def _is_Celeron(self):
        return re.match('.*?Celeron', self.info[0]['model name']) is not None

    def _is_Pentium(self):
        return re.match('.*?Pentium', self.info[0]['model name']) is not None

    def _is_PentiumII(self):
        return re.match('.*?Pentium.*?II\\b', self.info[0]['model name']) is not None

    def _is_PentiumPro(self):
        return re.match('.*?PentiumPro\\b', self.info[0]['model name']) is not None

    def _is_PentiumMMX(self):
        return re.match('.*?Pentium.*?MMX\\b', self.info[0]['model name']) is not None

    def _is_PentiumIII(self):
        return re.match('.*?Pentium.*?III\\b', self.info[0]['model name']) is not None

    def _is_PentiumIV(self):
        return re.match('.*?Pentium.*?(IV|4)\\b', self.info[0]['model name']) is not None

    def _is_PentiumM(self):
        return re.match('.*?Pentium.*?M\\b', self.info[0]['model name']) is not None

    def _is_Prescott(self):
        return self.is_PentiumIV() and self.has_sse3()

    def _is_Nocona--- This code section failed: ---

 L. 245         0  LOAD_FAST                'self'
                2  LOAD_METHOD              is_Intel
                4  CALL_METHOD_0         0  ''
                6  JUMP_IF_FALSE_OR_POP    86  'to 86'

 L. 246         8  LOAD_FAST                'self'
               10  LOAD_ATTR                info
               12  LOAD_CONST               0
               14  BINARY_SUBSCR    
               16  LOAD_STR                 'cpu family'
               18  BINARY_SUBSCR    
               20  LOAD_STR                 '6'
               22  COMPARE_OP               ==
               24  POP_JUMP_IF_TRUE     44  'to 44'

 L. 247        26  LOAD_FAST                'self'
               28  LOAD_ATTR                info
               30  LOAD_CONST               0
               32  BINARY_SUBSCR    
               34  LOAD_STR                 'cpu family'
               36  BINARY_SUBSCR    
               38  LOAD_STR                 '15'
               40  COMPARE_OP               ==

 L. 245        42  JUMP_IF_FALSE_OR_POP    86  'to 86'
             44_0  COME_FROM            24  '24'

 L. 248        44  LOAD_FAST                'self'
               46  LOAD_METHOD              has_sse3
               48  CALL_METHOD_0         0  ''
               50  JUMP_IF_FALSE_OR_POP    86  'to 86'
               52  LOAD_FAST                'self'
               54  LOAD_METHOD              has_ssse3
               56  CALL_METHOD_0         0  ''
               58  UNARY_NOT        

 L. 245        60  JUMP_IF_FALSE_OR_POP    86  'to 86'

 L. 249        62  LOAD_GLOBAL              re
               64  LOAD_METHOD              match
               66  LOAD_STR                 '.*?\\blm\\b'
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                info
               72  LOAD_CONST               0
               74  BINARY_SUBSCR    
               76  LOAD_STR                 'flags'
               78  BINARY_SUBSCR    
               80  CALL_METHOD_2         2  ''
               82  LOAD_CONST               None
               84  COMPARE_OP               is-not
             86_0  COME_FROM            60  '60'
             86_1  COME_FROM            50  '50'
             86_2  COME_FROM            42  '42'
             86_3  COME_FROM             6  '6'

 L. 245        86  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 86_3

    def _is_Core2(self):
        return self.is_64bit() and self.is_Intel() and re.match('.*?Core\\(TM\\)2\\b', self.info[0]['model name']) is not None

    def _is_Itanium(self):
        return re.match('.*?Itanium\\b', self.info[0]['family']) is not None

    def _is_XEON(self):
        return re.match('.*?XEON\\b', self.info[0]['model name'], re.IGNORECASE) is not None

    _is_Xeon = _is_XEON

    def _is_singleCPU(self):
        return len(self.info) == 1

    def _getNCPUs(self):
        return len(self.info)

    def _has_fdiv_bug(self):
        return self.info[0]['fdiv_bug'] == 'yes'

    def _has_f00f_bug(self):
        return self.info[0]['f00f_bug'] == 'yes'

    def _has_mmx(self):
        return re.match('.*?\\bmmx\\b', self.info[0]['flags']) is not None

    def _has_sse(self):
        return re.match('.*?\\bsse\\b', self.info[0]['flags']) is not None

    def _has_sse2(self):
        return re.match('.*?\\bsse2\\b', self.info[0]['flags']) is not None

    def _has_sse3(self):
        return re.match('.*?\\bpni\\b', self.info[0]['flags']) is not None

    def _has_ssse3(self):
        return re.match('.*?\\bssse3\\b', self.info[0]['flags']) is not None

    def _has_3dnow(self):
        return re.match('.*?\\b3dnow\\b', self.info[0]['flags']) is not None

    def _has_3dnowext(self):
        return re.match('.*?\\b3dnowext\\b', self.info[0]['flags']) is not None


class IRIXCPUInfo(CPUInfoBase):
    info = None

    def __init__(self):
        if self.info is not None:
            return
        info = key_value_from_command('sysconf', sep=' ', successful_status=(0, 1))
        self.__class__.info = info

    def _not_impl(self):
        pass

    def _is_singleCPU(self):
        return self.info.get('NUM_PROCESSORS') == '1'

    def _getNCPUs(self):
        return int(self.info.get('NUM_PROCESSORS', 1))

    def __cputype(self, n):
        return self.info.get('PROCESSORS').split()[0].lower() == 'r%s' % n

    def _is_r2000(self):
        return self._IRIXCPUInfo__cputype(2000)

    def _is_r3000(self):
        return self._IRIXCPUInfo__cputype(3000)

    def _is_r3900(self):
        return self._IRIXCPUInfo__cputype(3900)

    def _is_r4000(self):
        return self._IRIXCPUInfo__cputype(4000)

    def _is_r4100(self):
        return self._IRIXCPUInfo__cputype(4100)

    def _is_r4300(self):
        return self._IRIXCPUInfo__cputype(4300)

    def _is_r4400(self):
        return self._IRIXCPUInfo__cputype(4400)

    def _is_r4600(self):
        return self._IRIXCPUInfo__cputype(4600)

    def _is_r4650(self):
        return self._IRIXCPUInfo__cputype(4650)

    def _is_r5000(self):
        return self._IRIXCPUInfo__cputype(5000)

    def _is_r6000(self):
        return self._IRIXCPUInfo__cputype(6000)

    def _is_r8000(self):
        return self._IRIXCPUInfo__cputype(8000)

    def _is_r10000(self):
        return self._IRIXCPUInfo__cputype(10000)

    def _is_r12000(self):
        return self._IRIXCPUInfo__cputype(12000)

    def _is_rorion(self):
        return self._IRIXCPUInfo__cputype('orion')

    def get_ip--- This code section failed: ---

 L. 338         0  SETUP_FINALLY        16  'to 16'

 L. 338         2  LOAD_FAST                'self'
                4  LOAD_ATTR                info
                6  LOAD_METHOD              get
                8  LOAD_STR                 'MACHINE'
               10  CALL_METHOD_1         1  ''
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L. 339        16  DUP_TOP          
               18  LOAD_GLOBAL              Exception
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    34  'to 34'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 339        30  POP_EXCEPT       
               32  JUMP_FORWARD         36  'to 36'
             34_0  COME_FROM            22  '22'
               34  END_FINALLY      
             36_0  COME_FROM            32  '32'

Parse error at or near `POP_TOP' instruction at offset 26

    def __machine(self, n):
        return self.info.get('MACHINE').lower() == 'ip%s' % n

    def _is_IP19(self):
        return self._IRIXCPUInfo__machine(19)

    def _is_IP20(self):
        return self._IRIXCPUInfo__machine(20)

    def _is_IP21(self):
        return self._IRIXCPUInfo__machine(21)

    def _is_IP22(self):
        return self._IRIXCPUInfo__machine(22)

    def _is_IP22_4k(self):
        return self._IRIXCPUInfo__machine(22) and self._is_r4000()

    def _is_IP22_5k(self):
        return self._IRIXCPUInfo__machine(22) and self._is_r5000()

    def _is_IP24(self):
        return self._IRIXCPUInfo__machine(24)

    def _is_IP25(self):
        return self._IRIXCPUInfo__machine(25)

    def _is_IP26(self):
        return self._IRIXCPUInfo__machine(26)

    def _is_IP27(self):
        return self._IRIXCPUInfo__machine(27)

    def _is_IP28(self):
        return self._IRIXCPUInfo__machine(28)

    def _is_IP30(self):
        return self._IRIXCPUInfo__machine(30)

    def _is_IP32(self):
        return self._IRIXCPUInfo__machine(32)

    def _is_IP32_5k(self):
        return self._IRIXCPUInfo__machine(32) and self._is_r5000()

    def _is_IP32_10k(self):
        return self._IRIXCPUInfo__machine(32) and self._is_r10000()


class DarwinCPUInfo(CPUInfoBase):
    info = None

    def __init__(self):
        if self.info is not None:
            return
        info = command_info(arch='arch', machine='machine')
        info['sysctl_hw'] = key_value_from_command('sysctl hw', sep='=')
        self.__class__.info = info

    def _not_impl(self):
        pass

    def _getNCPUs(self):
        return int(self.info['sysctl_hw'].get('hw.ncpu', 1))

    def _is_Power_Macintosh(self):
        return self.info['sysctl_hw']['hw.machine'] == 'Power Macintosh'

    def _is_i386(self):
        return self.info['arch'] == 'i386'

    def _is_ppc(self):
        return self.info['arch'] == 'ppc'

    def __machine(self, n):
        return self.info['machine'] == 'ppc%s' % n

    def _is_ppc601(self):
        return self._DarwinCPUInfo__machine(601)

    def _is_ppc602(self):
        return self._DarwinCPUInfo__machine(602)

    def _is_ppc603(self):
        return self._DarwinCPUInfo__machine(603)

    def _is_ppc603e(self):
        return self._DarwinCPUInfo__machine('603e')

    def _is_ppc604(self):
        return self._DarwinCPUInfo__machine(604)

    def _is_ppc604e(self):
        return self._DarwinCPUInfo__machine('604e')

    def _is_ppc620(self):
        return self._DarwinCPUInfo__machine(620)

    def _is_ppc630(self):
        return self._DarwinCPUInfo__machine(630)

    def _is_ppc740(self):
        return self._DarwinCPUInfo__machine(740)

    def _is_ppc7400(self):
        return self._DarwinCPUInfo__machine(7400)

    def _is_ppc7450(self):
        return self._DarwinCPUInfo__machine(7450)

    def _is_ppc750(self):
        return self._DarwinCPUInfo__machine(750)

    def _is_ppc403(self):
        return self._DarwinCPUInfo__machine(403)

    def _is_ppc505(self):
        return self._DarwinCPUInfo__machine(505)

    def _is_ppc801(self):
        return self._DarwinCPUInfo__machine(801)

    def _is_ppc821(self):
        return self._DarwinCPUInfo__machine(821)

    def _is_ppc823(self):
        return self._DarwinCPUInfo__machine(823)

    def _is_ppc860(self):
        return self._DarwinCPUInfo__machine(860)


class SunOSCPUInfo(CPUInfoBase):
    info = None

    def __init__(self):
        if self.info is not None:
            return
        info = command_info(arch='arch', mach='mach',
          uname_i='uname_i',
          isainfo_b='isainfo -b',
          isainfo_n='isainfo -n')
        info['uname_X'] = key_value_from_command('uname -X', sep='=')
        for line in command_by_line('psrinfo -v 0'):
            m = re.match('\\s*The (?P<p>[\\w\\d]+) processor operates at', line)
            if m:
                info['processor'] = m.group('p')
                break
            self.__class__.info = info

    def _not_impl(self):
        pass

    def _is_i386(self):
        return self.info['isainfo_n'] == 'i386'

    def _is_sparc(self):
        return self.info['isainfo_n'] == 'sparc'

    def _is_sparcv9(self):
        return self.info['isainfo_n'] == 'sparcv9'

    def _getNCPUs(self):
        return int(self.info['uname_X'].get('NumCPU', 1))

    def _is_sun4(self):
        return self.info['arch'] == 'sun4'

    def _is_SUNW(self):
        return re.match('SUNW', self.info['uname_i']) is not None

    def _is_sparcstation5(self):
        return re.match('.*SPARCstation-5', self.info['uname_i']) is not None

    def _is_ultra1(self):
        return re.match('.*Ultra-1', self.info['uname_i']) is not None

    def _is_ultra250(self):
        return re.match('.*Ultra-250', self.info['uname_i']) is not None

    def _is_ultra2(self):
        return re.match('.*Ultra-2', self.info['uname_i']) is not None

    def _is_ultra30(self):
        return re.match('.*Ultra-30', self.info['uname_i']) is not None

    def _is_ultra4(self):
        return re.match('.*Ultra-4', self.info['uname_i']) is not None

    def _is_ultra5_10(self):
        return re.match('.*Ultra-5_10', self.info['uname_i']) is not None

    def _is_ultra5(self):
        return re.match('.*Ultra-5', self.info['uname_i']) is not None

    def _is_ultra60(self):
        return re.match('.*Ultra-60', self.info['uname_i']) is not None

    def _is_ultra80(self):
        return re.match('.*Ultra-80', self.info['uname_i']) is not None

    def _is_ultraenterprice(self):
        return re.match('.*Ultra-Enterprise', self.info['uname_i']) is not None

    def _is_ultraenterprice10k(self):
        return re.match('.*Ultra-Enterprise-10000', self.info['uname_i']) is not None

    def _is_sunfire(self):
        return re.match('.*Sun-Fire', self.info['uname_i']) is not None

    def _is_ultra(self):
        return re.match('.*Ultra', self.info['uname_i']) is not None

    def _is_cpusparcv7(self):
        return self.info['processor'] == 'sparcv7'

    def _is_cpusparcv8(self):
        return self.info['processor'] == 'sparcv8'

    def _is_cpusparcv9(self):
        return self.info['processor'] == 'sparcv9'


class Win32CPUInfo(CPUInfoBase):
    info = None
    pkey = 'HARDWARE\\DESCRIPTION\\System\\CentralProcessor'

    def __init__--- This code section failed: ---

 L. 488         0  LOAD_FAST                'self'
                2  LOAD_ATTR                info
                4  LOAD_CONST               None
                6  COMPARE_OP               is-not
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 489        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 490        14  BUILD_LIST_0          0 
               16  STORE_FAST               'info'

 L. 491     18_20  SETUP_FINALLY       338  'to 338'

 L. 493        22  LOAD_GLOBAL              sys
               24  LOAD_ATTR                version_info
               26  LOAD_CONST               0
               28  BINARY_SUBSCR    
               30  LOAD_CONST               3
               32  COMPARE_OP               >=
               34  POP_JUMP_IF_FALSE    46  'to 46'

 L. 494        36  LOAD_CONST               0
               38  LOAD_CONST               None
               40  IMPORT_NAME              winreg
               42  STORE_FAST               'winreg'
               44  JUMP_FORWARD         54  'to 54'
             46_0  COME_FROM            34  '34'

 L. 496        46  LOAD_CONST               0
               48  LOAD_CONST               None
               50  IMPORT_NAME              _winreg
               52  STORE_FAST               'winreg'
             54_0  COME_FROM            44  '44'

 L. 498        54  LOAD_GLOBAL              re
               56  LOAD_METHOD              compile
               58  LOAD_STR                 'family\\s+(?P<FML>\\d+)\\s+model\\s+(?P<MDL>\\d+)\\s+stepping\\s+(?P<STP>\\d+)'

 L. 499        60  LOAD_GLOBAL              re
               62  LOAD_ATTR                IGNORECASE

 L. 498        64  CALL_METHOD_2         2  ''
               66  STORE_FAST               'prgx'

 L. 500        68  LOAD_FAST                'winreg'
               70  LOAD_METHOD              OpenKey
               72  LOAD_FAST                'winreg'
               74  LOAD_ATTR                HKEY_LOCAL_MACHINE
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                pkey
               80  CALL_METHOD_2         2  ''
               82  STORE_FAST               'chnd'

 L. 501        84  LOAD_CONST               0
               86  STORE_FAST               'pnum'

 L. 503        88  SETUP_FINALLY       106  'to 106'

 L. 504        90  LOAD_FAST                'winreg'
               92  LOAD_METHOD              EnumKey
               94  LOAD_FAST                'chnd'
               96  LOAD_FAST                'pnum'
               98  CALL_METHOD_2         2  ''
              100  STORE_FAST               'proc'
              102  POP_BLOCK        
              104  JUMP_FORWARD        134  'to 134'
            106_0  COME_FROM_FINALLY    88  '88'

 L. 505       106  DUP_TOP          
              108  LOAD_FAST                'winreg'
              110  LOAD_ATTR                error
              112  COMPARE_OP               exception-match
              114  POP_JUMP_IF_FALSE   132  'to 132'
              116  POP_TOP          
              118  POP_TOP          
              120  POP_TOP          

 L. 506       122  POP_EXCEPT       
          124_126  BREAK_LOOP          334  'to 334'
              128  POP_EXCEPT       
              130  JUMP_BACK            88  'to 88'
            132_0  COME_FROM           114  '114'
              132  END_FINALLY      
            134_0  COME_FROM           104  '104'

 L. 508       134  LOAD_FAST                'pnum'
              136  LOAD_CONST               1
              138  INPLACE_ADD      
              140  STORE_FAST               'pnum'

 L. 509       142  LOAD_FAST                'info'
              144  LOAD_METHOD              append
              146  LOAD_STR                 'Processor'
              148  LOAD_FAST                'proc'
              150  BUILD_MAP_1           1 
              152  CALL_METHOD_1         1  ''
              154  POP_TOP          

 L. 510       156  LOAD_FAST                'winreg'
              158  LOAD_METHOD              OpenKey
              160  LOAD_FAST                'chnd'
              162  LOAD_FAST                'proc'
              164  CALL_METHOD_2         2  ''
              166  STORE_FAST               'phnd'

 L. 511       168  LOAD_CONST               0
              170  STORE_FAST               'pidx'
            172_0  COME_FROM           262  '262'
            172_1  COME_FROM           248  '248'

 L. 513       172  SETUP_FINALLY       196  'to 196'

 L. 514       174  LOAD_FAST                'winreg'
              176  LOAD_METHOD              EnumValue
              178  LOAD_FAST                'phnd'
              180  LOAD_FAST                'pidx'
              182  CALL_METHOD_2         2  ''
              184  UNPACK_SEQUENCE_3     3 
              186  STORE_FAST               'name'
              188  STORE_FAST               'value'
              190  STORE_FAST               'vtpe'
              192  POP_BLOCK        
              194  JUMP_FORWARD        222  'to 222'
            196_0  COME_FROM_FINALLY   172  '172'

 L. 515       196  DUP_TOP          
              198  LOAD_FAST                'winreg'
              200  LOAD_ATTR                error
              202  COMPARE_OP               exception-match
              204  POP_JUMP_IF_FALSE   220  'to 220'
              206  POP_TOP          
              208  POP_TOP          
              210  POP_TOP          

 L. 516       212  POP_EXCEPT       
              214  JUMP_BACK            88  'to 88'
              216  POP_EXCEPT       
              218  JUMP_BACK           172  'to 172'
            220_0  COME_FROM           204  '204'
              220  END_FINALLY      
            222_0  COME_FROM           194  '194'

 L. 518       222  LOAD_FAST                'pidx'
              224  LOAD_CONST               1
              226  BINARY_ADD       
              228  STORE_FAST               'pidx'

 L. 519       230  LOAD_FAST                'value'
              232  LOAD_FAST                'info'
              234  LOAD_CONST               -1
              236  BINARY_SUBSCR    
              238  LOAD_FAST                'name'
              240  STORE_SUBSCR     

 L. 520       242  LOAD_FAST                'name'
              244  LOAD_STR                 'Identifier'
              246  COMPARE_OP               ==
              248  POP_JUMP_IF_FALSE   172  'to 172'

 L. 521       250  LOAD_FAST                'prgx'
              252  LOAD_METHOD              search
              254  LOAD_FAST                'value'
              256  CALL_METHOD_1         1  ''
              258  STORE_FAST               'srch'

 L. 522       260  LOAD_FAST                'srch'
              262  POP_JUMP_IF_FALSE   172  'to 172'

 L. 523       264  LOAD_GLOBAL              int
              266  LOAD_FAST                'srch'
              268  LOAD_METHOD              group
              270  LOAD_STR                 'FML'
              272  CALL_METHOD_1         1  ''
              274  CALL_FUNCTION_1       1  ''
              276  LOAD_FAST                'info'
              278  LOAD_CONST               -1
              280  BINARY_SUBSCR    
              282  LOAD_STR                 'Family'
              284  STORE_SUBSCR     

 L. 524       286  LOAD_GLOBAL              int
              288  LOAD_FAST                'srch'
              290  LOAD_METHOD              group
              292  LOAD_STR                 'MDL'
              294  CALL_METHOD_1         1  ''
              296  CALL_FUNCTION_1       1  ''
              298  LOAD_FAST                'info'
              300  LOAD_CONST               -1
              302  BINARY_SUBSCR    
              304  LOAD_STR                 'Model'
              306  STORE_SUBSCR     

 L. 525       308  LOAD_GLOBAL              int
              310  LOAD_FAST                'srch'
              312  LOAD_METHOD              group
              314  LOAD_STR                 'STP'
              316  CALL_METHOD_1         1  ''
              318  CALL_FUNCTION_1       1  ''
              320  LOAD_FAST                'info'
              322  LOAD_CONST               -1
              324  BINARY_SUBSCR    
              326  LOAD_STR                 'Stepping'
              328  STORE_SUBSCR     
              330  JUMP_BACK           172  'to 172'
              332  JUMP_BACK            88  'to 88'
              334  POP_BLOCK        
              336  JUMP_FORWARD        378  'to 378'
            338_0  COME_FROM_FINALLY    18  '18'

 L. 526       338  DUP_TOP          
              340  LOAD_GLOBAL              Exception
              342  COMPARE_OP               exception-match
          344_346  POP_JUMP_IF_FALSE   376  'to 376'
              348  POP_TOP          
              350  POP_TOP          
              352  POP_TOP          

 L. 527       354  LOAD_GLOBAL              print
              356  LOAD_GLOBAL              sys
              358  LOAD_METHOD              exc_info
              360  CALL_METHOD_0         0  ''
              362  LOAD_CONST               1
              364  BINARY_SUBSCR    
              366  LOAD_STR                 '(ignoring)'
              368  CALL_FUNCTION_2       2  ''
              370  POP_TOP          
              372  POP_EXCEPT       
              374  JUMP_FORWARD        378  'to 378'
            376_0  COME_FROM           344  '344'
              376  END_FINALLY      
            378_0  COME_FROM           374  '374'
            378_1  COME_FROM           336  '336'

 L. 528       378  LOAD_FAST                'info'
              380  LOAD_FAST                'self'
              382  LOAD_ATTR                __class__
              384  STORE_ATTR               info

Parse error at or near `POP_EXCEPT' instruction at offset 216

    def _not_impl(self):
        pass

    def _is_AMD(self):
        return self.info[0]['VendorIdentifier'] == 'AuthenticAMD'

    def _is_Am486(self):
        return self.is_AMD() and self.info[0]['Family'] == 4

    def _is_Am5x86(self):
        return self.is_AMD() and self.info[0]['Family'] == 4

    def _is_AMDK5(self):
        return self.is_AMD() and self.info[0]['Family'] == 5 and self.info[0]['Model'] in (0,
                                                                                           1,
                                                                                           2,
                                                                                           3)

    def _is_AMDK6(self):
        return self.is_AMD() and self.info[0]['Family'] == 5 and self.info[0]['Model'] in (6,
                                                                                           7)

    def _is_AMDK6_2(self):
        return self.is_AMD() and self.info[0]['Family'] == 5 and self.info[0]['Model'] == 8

    def _is_AMDK6_3(self):
        return self.is_AMD() and self.info[0]['Family'] == 5 and self.info[0]['Model'] == 9

    def _is_AMDK7(self):
        return self.is_AMD() and self.info[0]['Family'] == 6

    def _is_AMD64(self):
        return self.is_AMD() and self.info[0]['Family'] == 15

    def _is_Intel(self):
        return self.info[0]['VendorIdentifier'] == 'GenuineIntel'

    def _is_i386(self):
        return self.info[0]['Family'] == 3

    def _is_i486(self):
        return self.info[0]['Family'] == 4

    def _is_i586(self):
        return self.is_Intel() and self.info[0]['Family'] == 5

    def _is_i686(self):
        return self.is_Intel() and self.info[0]['Family'] == 6

    def _is_Pentium(self):
        return self.is_Intel() and self.info[0]['Family'] == 5

    def _is_PentiumMMX(self):
        return self.is_Intel() and self.info[0]['Family'] == 5 and self.info[0]['Model'] == 4

    def _is_PentiumPro(self):
        return self.is_Intel() and self.info[0]['Family'] == 6 and self.info[0]['Model'] == 1

    def _is_PentiumII(self):
        return self.is_Intel() and self.info[0]['Family'] == 6 and self.info[0]['Model'] in (3,
                                                                                             5,
                                                                                             6)

    def _is_PentiumIII(self):
        return self.is_Intel() and self.info[0]['Family'] == 6 and self.info[0]['Model'] in (7,
                                                                                             8,
                                                                                             9,
                                                                                             10,
                                                                                             11)

    def _is_PentiumIV(self):
        return self.is_Intel() and self.info[0]['Family'] == 15

    def _is_PentiumM(self):
        return self.is_Intel() and self.info[0]['Family'] == 6 and self.info[0]['Model'] in (9,
                                                                                             13,
                                                                                             14)

    def _is_Core2(self):
        return self.is_Intel() and self.info[0]['Family'] == 6 and self.info[0]['Model'] in (15,
                                                                                             16,
                                                                                             17)

    def _is_singleCPU(self):
        return len(self.info) == 1

    def _getNCPUs(self):
        return len(self.info)

    def _has_mmx(self):
        if self.is_Intel():
            return self.info[0]['Family'] == 5 and self.info[0]['Model'] == 4 or self.info[0]['Family'] in (6,
                                                                                                            15)
        if self.is_AMD():
            return self.info[0]['Family'] in (5, 6, 15)
        return False

    def _has_sse(self):
        if self.is_Intel():
            return self.info[0]['Family'] == 6 and self.info[0]['Model'] in (7, 8,
                                                                             9, 10,
                                                                             11) or self.info[0]['Family'] == 15
        if self.is_AMD():
            return self.info[0]['Family'] == 6 and self.info[0]['Model'] in (6, 7,
                                                                             8, 10) or self.info[0]['Family'] == 15
        return False

    def _has_sse2(self):
        if self.is_Intel():
            return self.is_Pentium4() or self.is_PentiumM() or self.is_Core2()
        if self.is_AMD():
            return self.is_AMD64()
        return False

    def _has_3dnow(self):
        return self.is_AMD() and self.info[0]['Family'] in (5, 6, 15)

    def _has_3dnowext(self):
        return self.is_AMD() and self.info[0]['Family'] in (6, 15)


if sys.platform.startswith('linux'):
    cpuinfo = LinuxCPUInfo
else:
    if sys.platform.startswith('irix'):
        cpuinfo = IRIXCPUInfo
    else:
        if sys.platform == 'darwin':
            cpuinfo = DarwinCPUInfo
        else:
            if sys.platform.startswith('sunos'):
                cpuinfo = SunOSCPUInfo
            else:
                if sys.platform.startswith('win32'):
                    cpuinfo = Win32CPUInfo
                else:
                    if sys.platform.startswith('cygwin'):
                        cpuinfo = LinuxCPUInfo
                    else:
                        cpuinfo = CPUInfoBase
cpu = cpuinfo()