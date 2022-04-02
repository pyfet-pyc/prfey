# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: numpy\distutils\cpuinfo.py
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
__all__ = [
 'cpu']
import os, platform, re, sys, types, warnings
from subprocess import getstatusoutput

def getoutput(cmd, successful_status=(0,), stacklevel=1):
    try:
        status, output = getstatusoutput(cmd)
    except EnvironmentError as e:
        try:
            warnings.warn((str(e)), UserWarning, stacklevel=stacklevel)
            return (False, '')
        finally:
            e = None
            del e

    if os.WIFEXITED(status):
        if os.WEXITSTATUS(status) in successful_status:
            return (
             True, output)
    return (
     False, output)


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
        yield line.strip()


def key_value_from_command(cmd, sep, successful_status=(0,), stacklevel=1):
    d = {}
    for line in command_by_line(cmd, successful_status=successful_status, stacklevel=(stacklevel + 1)):
        l = [s.strip() for s in line.split(sep, 1)]
        if len(l) == 2:
            d[l[0]] = l[1]

    return d


class CPUInfoBase:
    __doc__ = 'Holds CPU information and provides methods for requiring\n    the availability of various CPU features.\n    '

    def _try_call(self, func):
        try:
            return func()
        except Exception:
            pass

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
        except EnvironmentError as e:
            try:
                warnings.warn((str(e)), UserWarning, stacklevel=2)
            finally:
                e = None
                del e

        else:
            for line in fo:
                name_value = [s.strip() for s in line.split(':', 1)]
                if len(name_value) != 2:
                    continue
                name, value = name_value
                if not info or name in info[(-1)]:
                    info.append({})
                info[(-1)][name] = value

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

 L. 238         0  LOAD_FAST                'self'
                2  LOAD_METHOD              is_Intel
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  JUMP_IF_FALSE_OR_POP    86  'to 86'

 L. 239         8  LOAD_FAST                'self'
               10  LOAD_ATTR                info
               12  LOAD_CONST               0
               14  BINARY_SUBSCR    
               16  LOAD_STR                 'cpu family'
               18  BINARY_SUBSCR    
               20  LOAD_STR                 '6'
               22  COMPARE_OP               ==
               24  POP_JUMP_IF_TRUE     44  'to 44'

 L. 240        26  LOAD_FAST                'self'
               28  LOAD_ATTR                info
               30  LOAD_CONST               0
               32  BINARY_SUBSCR    
               34  LOAD_STR                 'cpu family'
               36  BINARY_SUBSCR    
               38  LOAD_STR                 '15'
               40  COMPARE_OP               ==
               42  JUMP_IF_FALSE_OR_POP    86  'to 86'
             44_0  COME_FROM            24  '24'

 L. 241        44  LOAD_FAST                'self'
               46  LOAD_METHOD              has_sse3
               48  CALL_METHOD_0         0  '0 positional arguments'
               50  JUMP_IF_FALSE_OR_POP    86  'to 86'
               52  LOAD_FAST                'self'
               54  LOAD_METHOD              has_ssse3
               56  CALL_METHOD_0         0  '0 positional arguments'
               58  UNARY_NOT        
               60  JUMP_IF_FALSE_OR_POP    86  'to 86'

 L. 242        62  LOAD_GLOBAL              re
               64  LOAD_METHOD              match
               66  LOAD_STR                 '.*?\\blm\\b'
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                info
               72  LOAD_CONST               0
               74  BINARY_SUBSCR    
               76  LOAD_STR                 'flags'
               78  BINARY_SUBSCR    
               80  CALL_METHOD_2         2  '2 positional arguments'
               82  LOAD_CONST               None
               84  COMPARE_OP               is-not
             86_0  COME_FROM            60  '60'
             86_1  COME_FROM            50  '50'
             86_2  COME_FROM            42  '42'
             86_3  COME_FROM             6  '6'
               86  RETURN_VALUE     
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

    def get_ip(self):
        try:
            return self.info.get('MACHINE')
        except Exception:
            pass

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

    def __init__(self):
        if self.info is not None:
            return
        info = []
        try:
            import winreg
            prgx = re.compile('family\\s+(?P<FML>\\d+)\\s+model\\s+(?P<MDL>\\d+)\\s+stepping\\s+(?P<STP>\\d+)', re.IGNORECASE)
            chnd = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self.pkey)
            pnum = 0
            while 1:
                try:
                    proc = winreg.EnumKey(chnd, pnum)
                except winreg.error:
                    break
                else:
                    pnum += 1
                    info.append({'Processor': proc})
                    phnd = winreg.OpenKey(chnd, proc)
                    pidx = 0
                    while True:
                        try:
                            name, value, vtpe = winreg.EnumValue(phnd, pidx)
                        except winreg.error:
                            break
                        else:
                            pidx = pidx + 1
                            info[(-1)][name] = value
                            if name == 'Identifier':
                                srch = prgx.search(value)
                                if srch:
                                    info[(-1)]['Family'] = int(srch.group('FML'))
                                    info[(-1)]['Model'] = int(srch.group('MDL'))
                                    info[(-1)]['Stepping'] = int(srch.group('STP'))

        except Exception as e:
            try:
                print(e, '(ignoring)')
            finally:
                e = None
                del e

        self.__class__.info = info

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