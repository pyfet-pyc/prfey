# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
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

def getoutput--- This code section failed: ---

 L.  28         0  SETUP_FINALLY        18  'to 18'

 L.  29         2  LOAD_GLOBAL              getstatusoutput
                4  LOAD_FAST                'cmd'
                6  CALL_FUNCTION_1       1  ''
                8  UNPACK_SEQUENCE_2     2 
               10  STORE_FAST               'status'
               12  STORE_FAST               'output'
               14  POP_BLOCK        
               16  JUMP_FORWARD         78  'to 78'
             18_0  COME_FROM_FINALLY     0  '0'

 L.  30        18  DUP_TOP          
               20  LOAD_GLOBAL              EnvironmentError
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    76  'to 76'
               26  POP_TOP          
               28  STORE_FAST               'e'
               30  POP_TOP          
               32  SETUP_FINALLY        64  'to 64'

 L.  31        34  LOAD_GLOBAL              warnings
               36  LOAD_ATTR                warn
               38  LOAD_GLOBAL              str
               40  LOAD_FAST                'e'
               42  CALL_FUNCTION_1       1  ''
               44  LOAD_GLOBAL              UserWarning
               46  LOAD_FAST                'stacklevel'
               48  LOAD_CONST               ('stacklevel',)
               50  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               52  POP_TOP          

 L.  32        54  POP_BLOCK        
               56  POP_EXCEPT       
               58  CALL_FINALLY         64  'to 64'
               60  LOAD_CONST               (False, '')
               62  RETURN_VALUE     
             64_0  COME_FROM            58  '58'
             64_1  COME_FROM_FINALLY    32  '32'
               64  LOAD_CONST               None
               66  STORE_FAST               'e'
               68  DELETE_FAST              'e'
               70  END_FINALLY      
               72  POP_EXCEPT       
               74  JUMP_FORWARD         78  'to 78'
             76_0  COME_FROM            24  '24'
               76  END_FINALLY      
             78_0  COME_FROM            74  '74'
             78_1  COME_FROM            16  '16'

 L.  33        78  LOAD_GLOBAL              os
               80  LOAD_METHOD              WIFEXITED
               82  LOAD_FAST                'status'
               84  CALL_METHOD_1         1  ''
               86  POP_JUMP_IF_FALSE   110  'to 110'
               88  LOAD_GLOBAL              os
               90  LOAD_METHOD              WEXITSTATUS
               92  LOAD_FAST                'status'
               94  CALL_METHOD_1         1  ''
               96  LOAD_FAST                'successful_status'
               98  COMPARE_OP               in
              100  POP_JUMP_IF_FALSE   110  'to 110'

 L.  34       102  LOAD_CONST               True
              104  LOAD_FAST                'output'
              106  BUILD_TUPLE_2         2 
              108  RETURN_VALUE     
            110_0  COME_FROM           100  '100'
            110_1  COME_FROM            86  '86'

 L.  35       110  LOAD_CONST               False
              112  LOAD_FAST                'output'
              114  BUILD_TUPLE_2         2 
              116  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 58


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


class CPUInfoBase:
    __doc__ = 'Holds CPU information and provides methods for requiring\n    the availability of various CPU features.\n    '

    def _try_call--- This code section failed: ---

 L.  70         0  SETUP_FINALLY        10  'to 10'

 L.  71         2  LOAD_FAST                'func'
                4  CALL_FUNCTION_0       0  ''
                6  POP_BLOCK        
                8  RETURN_VALUE     
             10_0  COME_FROM_FINALLY     0  '0'

 L.  72        10  DUP_TOP          
               12  LOAD_GLOBAL              Exception
               14  COMPARE_OP               exception-match
               16  POP_JUMP_IF_FALSE    28  'to 28'
               18  POP_TOP          
               20  POP_TOP          
               22  POP_TOP          

 L.  73        24  POP_EXCEPT       
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

 L. 238         0  LOAD_FAST                'self'
                2  LOAD_METHOD              is_Intel
                4  CALL_METHOD_0         0  ''
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

 L. 238        42  JUMP_IF_FALSE_OR_POP    86  'to 86'
             44_0  COME_FROM            24  '24'

 L. 241        44  LOAD_FAST                'self'
               46  LOAD_METHOD              has_sse3
               48  CALL_METHOD_0         0  ''
               50  JUMP_IF_FALSE_OR_POP    86  'to 86'
               52  LOAD_FAST                'self'
               54  LOAD_METHOD              has_ssse3
               56  CALL_METHOD_0         0  ''
               58  UNARY_NOT        

 L. 238        60  JUMP_IF_FALSE_OR_POP    86  'to 86'

 L. 242        62  LOAD_GLOBAL              re
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

 L. 238        86  RETURN_VALUE     
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

 L. 331         0  SETUP_FINALLY        16  'to 16'

 L. 331         2  LOAD_FAST                'self'
                4  LOAD_ATTR                info
                6  LOAD_METHOD              get
                8  LOAD_STR                 'MACHINE'
               10  CALL_METHOD_1         1  ''
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L. 332        16  DUP_TOP          
               18  LOAD_GLOBAL              Exception
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    34  'to 34'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 332        30  POP_EXCEPT       
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

 L. 481         0  LOAD_FAST                'self'
                2  LOAD_ATTR                info
                4  LOAD_CONST               None
                6  COMPARE_OP               is-not
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 482        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 483        14  BUILD_LIST_0          0 
               16  STORE_FAST               'info'

 L. 484     18_20  SETUP_FINALLY       314  'to 314'

 L. 486        22  LOAD_CONST               0
               24  LOAD_CONST               None
               26  IMPORT_NAME              winreg
               28  STORE_FAST               'winreg'

 L. 488        30  LOAD_GLOBAL              re
               32  LOAD_METHOD              compile
               34  LOAD_STR                 'family\\s+(?P<FML>\\d+)\\s+model\\s+(?P<MDL>\\d+)\\s+stepping\\s+(?P<STP>\\d+)'

 L. 489        36  LOAD_GLOBAL              re
               38  LOAD_ATTR                IGNORECASE

 L. 488        40  CALL_METHOD_2         2  ''
               42  STORE_FAST               'prgx'

 L. 490        44  LOAD_FAST                'winreg'
               46  LOAD_METHOD              OpenKey
               48  LOAD_FAST                'winreg'
               50  LOAD_ATTR                HKEY_LOCAL_MACHINE
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                pkey
               56  CALL_METHOD_2         2  ''
               58  STORE_FAST               'chnd'

 L. 491        60  LOAD_CONST               0
               62  STORE_FAST               'pnum'

 L. 493        64  SETUP_FINALLY        82  'to 82'

 L. 494        66  LOAD_FAST                'winreg'
               68  LOAD_METHOD              EnumKey
               70  LOAD_FAST                'chnd'
               72  LOAD_FAST                'pnum'
               74  CALL_METHOD_2         2  ''
               76  STORE_FAST               'proc'
               78  POP_BLOCK        
               80  JUMP_FORWARD        110  'to 110'
             82_0  COME_FROM_FINALLY    64  '64'

 L. 495        82  DUP_TOP          
               84  LOAD_FAST                'winreg'
               86  LOAD_ATTR                error
               88  COMPARE_OP               exception-match
               90  POP_JUMP_IF_FALSE   108  'to 108'
               92  POP_TOP          
               94  POP_TOP          
               96  POP_TOP          

 L. 496        98  POP_EXCEPT       
          100_102  BREAK_LOOP          310  'to 310'
              104  POP_EXCEPT       
              106  JUMP_BACK            64  'to 64'
            108_0  COME_FROM            90  '90'
              108  END_FINALLY      
            110_0  COME_FROM            80  '80'

 L. 498       110  LOAD_FAST                'pnum'
              112  LOAD_CONST               1
              114  INPLACE_ADD      
              116  STORE_FAST               'pnum'

 L. 499       118  LOAD_FAST                'info'
              120  LOAD_METHOD              append
              122  LOAD_STR                 'Processor'
              124  LOAD_FAST                'proc'
              126  BUILD_MAP_1           1 
              128  CALL_METHOD_1         1  ''
              130  POP_TOP          

 L. 500       132  LOAD_FAST                'winreg'
              134  LOAD_METHOD              OpenKey
              136  LOAD_FAST                'chnd'
              138  LOAD_FAST                'proc'
              140  CALL_METHOD_2         2  ''
              142  STORE_FAST               'phnd'

 L. 501       144  LOAD_CONST               0
              146  STORE_FAST               'pidx'
            148_0  COME_FROM           238  '238'
            148_1  COME_FROM           224  '224'

 L. 503       148  SETUP_FINALLY       172  'to 172'

 L. 504       150  LOAD_FAST                'winreg'
              152  LOAD_METHOD              EnumValue
              154  LOAD_FAST                'phnd'
              156  LOAD_FAST                'pidx'
              158  CALL_METHOD_2         2  ''
              160  UNPACK_SEQUENCE_3     3 
              162  STORE_FAST               'name'
              164  STORE_FAST               'value'
              166  STORE_FAST               'vtpe'
              168  POP_BLOCK        
              170  JUMP_FORWARD        198  'to 198'
            172_0  COME_FROM_FINALLY   148  '148'

 L. 505       172  DUP_TOP          
              174  LOAD_FAST                'winreg'
              176  LOAD_ATTR                error
              178  COMPARE_OP               exception-match
              180  POP_JUMP_IF_FALSE   196  'to 196'
              182  POP_TOP          
              184  POP_TOP          
              186  POP_TOP          

 L. 506       188  POP_EXCEPT       
              190  JUMP_BACK            64  'to 64'
              192  POP_EXCEPT       
              194  JUMP_BACK           148  'to 148'
            196_0  COME_FROM           180  '180'
              196  END_FINALLY      
            198_0  COME_FROM           170  '170'

 L. 508       198  LOAD_FAST                'pidx'
              200  LOAD_CONST               1
              202  BINARY_ADD       
              204  STORE_FAST               'pidx'

 L. 509       206  LOAD_FAST                'value'
              208  LOAD_FAST                'info'
              210  LOAD_CONST               -1
              212  BINARY_SUBSCR    
              214  LOAD_FAST                'name'
              216  STORE_SUBSCR     

 L. 510       218  LOAD_FAST                'name'
              220  LOAD_STR                 'Identifier'
              222  COMPARE_OP               ==
              224  POP_JUMP_IF_FALSE   148  'to 148'

 L. 511       226  LOAD_FAST                'prgx'
              228  LOAD_METHOD              search
              230  LOAD_FAST                'value'
              232  CALL_METHOD_1         1  ''
              234  STORE_FAST               'srch'

 L. 512       236  LOAD_FAST                'srch'
              238  POP_JUMP_IF_FALSE   148  'to 148'

 L. 513       240  LOAD_GLOBAL              int
              242  LOAD_FAST                'srch'
              244  LOAD_METHOD              group
              246  LOAD_STR                 'FML'
              248  CALL_METHOD_1         1  ''
              250  CALL_FUNCTION_1       1  ''
              252  LOAD_FAST                'info'
              254  LOAD_CONST               -1
              256  BINARY_SUBSCR    
              258  LOAD_STR                 'Family'
              260  STORE_SUBSCR     

 L. 514       262  LOAD_GLOBAL              int
              264  LOAD_FAST                'srch'
              266  LOAD_METHOD              group
              268  LOAD_STR                 'MDL'
              270  CALL_METHOD_1         1  ''
              272  CALL_FUNCTION_1       1  ''
              274  LOAD_FAST                'info'
              276  LOAD_CONST               -1
              278  BINARY_SUBSCR    
              280  LOAD_STR                 'Model'
              282  STORE_SUBSCR     

 L. 515       284  LOAD_GLOBAL              int
              286  LOAD_FAST                'srch'
              288  LOAD_METHOD              group
              290  LOAD_STR                 'STP'
              292  CALL_METHOD_1         1  ''
              294  CALL_FUNCTION_1       1  ''
              296  LOAD_FAST                'info'
              298  LOAD_CONST               -1
              300  BINARY_SUBSCR    
              302  LOAD_STR                 'Stepping'
              304  STORE_SUBSCR     
              306  JUMP_BACK           148  'to 148'
              308  JUMP_BACK            64  'to 64'
              310  POP_BLOCK        
              312  JUMP_FORWARD        360  'to 360'
            314_0  COME_FROM_FINALLY    18  '18'

 L. 516       314  DUP_TOP          
              316  LOAD_GLOBAL              Exception
              318  COMPARE_OP               exception-match
          320_322  POP_JUMP_IF_FALSE   358  'to 358'
              324  POP_TOP          
              326  STORE_FAST               'e'
              328  POP_TOP          
              330  SETUP_FINALLY       346  'to 346'

 L. 517       332  LOAD_GLOBAL              print
              334  LOAD_FAST                'e'
              336  LOAD_STR                 '(ignoring)'
              338  CALL_FUNCTION_2       2  ''
              340  POP_TOP          
              342  POP_BLOCK        
              344  BEGIN_FINALLY    
            346_0  COME_FROM_FINALLY   330  '330'
              346  LOAD_CONST               None
              348  STORE_FAST               'e'
              350  DELETE_FAST              'e'
              352  END_FINALLY      
              354  POP_EXCEPT       
              356  JUMP_FORWARD        360  'to 360'
            358_0  COME_FROM           320  '320'
              358  END_FINALLY      
            360_0  COME_FROM           356  '356'
            360_1  COME_FROM           312  '312'

 L. 518       360  LOAD_FAST                'info'
              362  LOAD_FAST                'self'
              364  LOAD_ATTR                __class__
              366  STORE_ATTR               info

Parse error at or near `POP_EXCEPT' instruction at offset 192

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