# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: distutils\version.py
"""Provides classes to represent module version numbers (one class for
each style of version numbering).  There are currently two such classes
implemented: StrictVersion and LooseVersion.

Every version number class implements the following interface:
  * the 'parse' method takes a string and parses it to some internal
    representation; if the string is an invalid version number,
    'parse' raises a ValueError exception
  * the class constructor takes an optional string argument which,
    if supplied, is passed to 'parse'
  * __str__ reconstructs the string that was passed to 'parse' (or
    an equivalent string -- ie. one that will generate an equivalent
    version number instance)
  * __repr__ generates Python code to recreate the version number instance
  * _cmp compares the current instance with either another instance
    of the same class or a string (which will be parsed to an instance
    of the same class, thus must follow the same rules)
"""
import re

class Version:
    __doc__ = 'Abstract base class for version numbering classes.  Just provides\n    constructor (__init__) and reproducer (__repr__), because those\n    seem to be the same for all version numbering classes; and route\n    rich comparisons to _cmp.\n    '

    def __init__(self, vstring=None):
        if vstring:
            self.parse(vstring)

    def __repr__(self):
        return "%s ('%s')" % (self.__class__.__name__, str(self))

    def __eq__--- This code section failed: ---

 L.  46         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _cmp
                4  LOAD_FAST                'other'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'c'

 L.  47        10  LOAD_FAST                'c'
               12  LOAD_GLOBAL              NotImplemented
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    22  'to 22'

 L.  48        18  LOAD_FAST                'c'
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L.  49        22  LOAD_FAST                'c'
               24  LOAD_CONST               0
               26  COMPARE_OP               ==
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 14

    def __lt__--- This code section failed: ---

 L.  52         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _cmp
                4  LOAD_FAST                'other'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'c'

 L.  53        10  LOAD_FAST                'c'
               12  LOAD_GLOBAL              NotImplemented
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    22  'to 22'

 L.  54        18  LOAD_FAST                'c'
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L.  55        22  LOAD_FAST                'c'
               24  LOAD_CONST               0
               26  COMPARE_OP               <
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 14

    def __le__--- This code section failed: ---

 L.  58         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _cmp
                4  LOAD_FAST                'other'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'c'

 L.  59        10  LOAD_FAST                'c'
               12  LOAD_GLOBAL              NotImplemented
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    22  'to 22'

 L.  60        18  LOAD_FAST                'c'
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L.  61        22  LOAD_FAST                'c'
               24  LOAD_CONST               0
               26  COMPARE_OP               <=
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 14

    def __gt__--- This code section failed: ---

 L.  64         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _cmp
                4  LOAD_FAST                'other'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'c'

 L.  65        10  LOAD_FAST                'c'
               12  LOAD_GLOBAL              NotImplemented
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    22  'to 22'

 L.  66        18  LOAD_FAST                'c'
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L.  67        22  LOAD_FAST                'c'
               24  LOAD_CONST               0
               26  COMPARE_OP               >
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 14

    def __ge__--- This code section failed: ---

 L.  70         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _cmp
                4  LOAD_FAST                'other'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'c'

 L.  71        10  LOAD_FAST                'c'
               12  LOAD_GLOBAL              NotImplemented
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    22  'to 22'

 L.  72        18  LOAD_FAST                'c'
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L.  73        22  LOAD_FAST                'c'
               24  LOAD_CONST               0
               26  COMPARE_OP               >=
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 14


class StrictVersion(Version):
    __doc__ = 'Version numbering for anal retentives and software idealists.\n    Implements the standard interface for version number classes as\n    described above.  A version number consists of two or three\n    dot-separated numeric components, with an optional "pre-release" tag\n    on the end.  The pre-release tag consists of the letter \'a\' or \'b\'\n    followed by a number.  If the numeric components of two version\n    numbers are equal, then one with a pre-release tag will always\n    be deemed earlier (lesser) than one without.\n\n    The following are valid version numbers (shown in the order that\n    would be obtained by sorting according to the supplied cmp function):\n\n        0.4       0.4.0  (these two are equivalent)\n        0.4.1\n        0.5a1\n        0.5b3\n        0.5\n        0.9.6\n        1.0\n        1.0.4a3\n        1.0.4b1\n        1.0.4\n\n    The following are examples of invalid version numbers:\n\n        1\n        2.7.2.2\n        1.3.a4\n        1.3pl1\n        1.3c4\n\n    The rationale for this version numbering system will be explained\n    in the distutils documentation.\n    '
    version_re = re.compile('^(\\d+) \\. (\\d+) (\\. (\\d+))? ([ab](\\d+))?$', re.VERBOSE | re.ASCII)

    def parse(self, vstring):
        match = self.version_re.match(vstring)
        if not match:
            raise ValueError("invalid version number '%s'" % vstring)
        else:
            major, minor, patch, prerelease, prerelease_num = match.group(1, 2, 4, 5, 6)
            if patch:
                self.version = tuple(map(int, [major, minor, patch]))
            else:
                self.version = tuple(map(int, [major, minor])) + (0, )
            if prerelease:
                self.prerelease = (
                 prerelease[0], int(prerelease_num))
            else:
                self.prerelease = None

    def __str__(self):
        if self.version[2] == 0:
            vstring = '.'.join(map(str, self.version[0:2]))
        else:
            vstring = '.'.join(map(str, self.version))
        if self.prerelease:
            vstring = vstring + self.prerelease[0] + str(self.prerelease[1])
        return vstring

    def _cmp--- This code section failed: ---

 L. 167         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'other'
                4  LOAD_GLOBAL              str
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    20  'to 20'

 L. 168        10  LOAD_GLOBAL              StrictVersion
               12  LOAD_FAST                'other'
               14  CALL_FUNCTION_1       1  ''
               16  STORE_FAST               'other'
               18  JUMP_FORWARD         34  'to 34'
             20_0  COME_FROM             8  '8'

 L. 169        20  LOAD_GLOBAL              isinstance
               22  LOAD_FAST                'other'
               24  LOAD_GLOBAL              StrictVersion
               26  CALL_FUNCTION_2       2  ''
               28  POP_JUMP_IF_TRUE     34  'to 34'

 L. 170        30  LOAD_GLOBAL              NotImplemented
               32  RETURN_VALUE     
             34_0  COME_FROM            28  '28'
             34_1  COME_FROM            18  '18'

 L. 172        34  LOAD_FAST                'self'
               36  LOAD_ATTR                version
               38  LOAD_FAST                'other'
               40  LOAD_ATTR                version
               42  COMPARE_OP               !=
               44  POP_JUMP_IF_FALSE    66  'to 66'

 L. 175        46  LOAD_FAST                'self'
               48  LOAD_ATTR                version
               50  LOAD_FAST                'other'
               52  LOAD_ATTR                version
               54  COMPARE_OP               <
               56  POP_JUMP_IF_FALSE    62  'to 62'

 L. 176        58  LOAD_CONST               -1
               60  RETURN_VALUE     
             62_0  COME_FROM            56  '56'

 L. 178        62  LOAD_CONST               1
               64  RETURN_VALUE     
             66_0  COME_FROM            44  '44'

 L. 186        66  LOAD_FAST                'self'
               68  LOAD_ATTR                prerelease
               70  POP_JUMP_IF_TRUE     82  'to 82'
               72  LOAD_FAST                'other'
               74  LOAD_ATTR                prerelease
               76  POP_JUMP_IF_TRUE     82  'to 82'

 L. 187        78  LOAD_CONST               0
               80  RETURN_VALUE     
             82_0  COME_FROM            76  '76'
             82_1  COME_FROM            70  '70'

 L. 188        82  LOAD_FAST                'self'
               84  LOAD_ATTR                prerelease
               86  POP_JUMP_IF_FALSE    98  'to 98'
               88  LOAD_FAST                'other'
               90  LOAD_ATTR                prerelease
               92  POP_JUMP_IF_TRUE     98  'to 98'

 L. 189        94  LOAD_CONST               -1
               96  RETURN_VALUE     
             98_0  COME_FROM            92  '92'
             98_1  COME_FROM            86  '86'

 L. 190        98  LOAD_FAST                'self'
              100  LOAD_ATTR                prerelease
              102  POP_JUMP_IF_TRUE    114  'to 114'
              104  LOAD_FAST                'other'
              106  LOAD_ATTR                prerelease
              108  POP_JUMP_IF_FALSE   114  'to 114'

 L. 191       110  LOAD_CONST               1
              112  RETURN_VALUE     
            114_0  COME_FROM           108  '108'
            114_1  COME_FROM           102  '102'

 L. 192       114  LOAD_FAST                'self'
              116  LOAD_ATTR                prerelease
              118  POP_JUMP_IF_FALSE   164  'to 164'
              120  LOAD_FAST                'other'
              122  LOAD_ATTR                prerelease
              124  POP_JUMP_IF_FALSE   164  'to 164'

 L. 193       126  LOAD_FAST                'self'
              128  LOAD_ATTR                prerelease
              130  LOAD_FAST                'other'
              132  LOAD_ATTR                prerelease
              134  COMPARE_OP               ==
              136  POP_JUMP_IF_FALSE   142  'to 142'

 L. 194       138  LOAD_CONST               0
              140  RETURN_VALUE     
            142_0  COME_FROM           136  '136'

 L. 195       142  LOAD_FAST                'self'
              144  LOAD_ATTR                prerelease
              146  LOAD_FAST                'other'
              148  LOAD_ATTR                prerelease
              150  COMPARE_OP               <
              152  POP_JUMP_IF_FALSE   158  'to 158'

 L. 196       154  LOAD_CONST               -1
              156  RETURN_VALUE     
            158_0  COME_FROM           152  '152'

 L. 198       158  LOAD_CONST               1
              160  RETURN_VALUE     
              162  JUMP_FORWARD        176  'to 176'
            164_0  COME_FROM           124  '124'
            164_1  COME_FROM           118  '118'

 L. 200       164  LOAD_CONST               False
              166  POP_JUMP_IF_TRUE    176  'to 176'
              168  <74>             
              170  LOAD_STR                 'never get here'
              172  CALL_FUNCTION_1       1  ''
              174  RAISE_VARARGS_1       1  'exception instance'
            176_0  COME_FROM           166  '166'
            176_1  COME_FROM           162  '162'

Parse error at or near `<74>' instruction at offset 168


class LooseVersion(Version):
    __doc__ = 'Version numbering for anarchists and software realists.\n    Implements the standard interface for version number classes as\n    described above.  A version number consists of a series of numbers,\n    separated by either periods or strings of letters.  When comparing\n    version numbers, the numeric components will be compared\n    numerically, and the alphabetic components lexically.  The following\n    are all valid version numbers, in no particular order:\n\n        1.5.1\n        1.5.2b2\n        161\n        3.10a\n        8.02\n        3.4j\n        1996.07.12\n        3.2.pl0\n        3.1.1.6\n        2g6\n        11g\n        0.960923\n        2.2beta29\n        1.13++\n        5.5.kw\n        2.0b1pl0\n\n    In fact, there is no such thing as an invalid version number under\n    this scheme; the rules for comparison are simple and predictable,\n    but may not always give the results you want (for some definition\n    of "want").\n    '
    component_re = re.compile('(\\d+ | [a-z]+ | \\.)', re.VERBOSE)

    def __init__(self, vstring=None):
        if vstring:
            self.parse(vstring)

    def parse--- This code section failed: ---

 L. 313         0  LOAD_FAST                'vstring'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               vstring

 L. 314         6  LOAD_LISTCOMP            '<code_object <listcomp>>'
                8  LOAD_STR                 'LooseVersion.parse.<locals>.<listcomp>'
               10  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                component_re
               16  LOAD_METHOD              split
               18  LOAD_FAST                'vstring'
               20  CALL_METHOD_1         1  ''
               22  GET_ITER         
               24  CALL_FUNCTION_1       1  ''
               26  STORE_FAST               'components'

 L. 316        28  LOAD_GLOBAL              enumerate
               30  LOAD_FAST                'components'
               32  CALL_FUNCTION_1       1  ''
               34  GET_ITER         
               36  FOR_ITER             82  'to 82'
               38  UNPACK_SEQUENCE_2     2 
               40  STORE_FAST               'i'
               42  STORE_FAST               'obj'

 L. 317        44  SETUP_FINALLY        62  'to 62'

 L. 318        46  LOAD_GLOBAL              int
               48  LOAD_FAST                'obj'
               50  CALL_FUNCTION_1       1  ''
               52  LOAD_FAST                'components'
               54  LOAD_FAST                'i'
               56  STORE_SUBSCR     
               58  POP_BLOCK        
               60  JUMP_BACK            36  'to 36'
             62_0  COME_FROM_FINALLY    44  '44'

 L. 319        62  DUP_TOP          
               64  LOAD_GLOBAL              ValueError
               66  <121>                78  ''
               68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          

 L. 320        74  POP_EXCEPT       
               76  JUMP_BACK            36  'to 36'
               78  <48>             
               80  JUMP_BACK            36  'to 36'

 L. 322        82  LOAD_FAST                'components'
               84  LOAD_FAST                'self'
               86  STORE_ATTR               version

Parse error at or near `<121>' instruction at offset 66

    def __str__(self):
        return self.vstring

    def __repr__(self):
        return "LooseVersion ('%s')" % str(self)

    def _cmp(self, other):
        if isinstance(other, str):
            other = LooseVersion(other)
        else:
            return isinstance(other, LooseVersion) or NotImplemented
        if self.version == other.version:
            return 0
        if self.version < other.version:
            return -1
        if self.version > other.version:
            return 1