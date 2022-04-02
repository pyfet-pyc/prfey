# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: ctypes\macholib\framework.py
"""
Generic framework path manipulation
"""
import re
__all__ = [
 'framework_info']
STRICT_FRAMEWORK_RE = re.compile('(?x)\n(?P<location>^.*)(?:^|/)\n(?P<name>\n    (?P<shortname>\\w+).framework/\n    (?:Versions/(?P<version>[^/]+)/)?\n    (?P=shortname)\n    (?:_(?P<suffix>[^_]+))?\n)$\n')

def framework_info(filename):
    """
    A framework name can take one of the following four forms:
        Location/Name.framework/Versions/SomeVersion/Name_Suffix
        Location/Name.framework/Versions/SomeVersion/Name
        Location/Name.framework/Name_Suffix
        Location/Name.framework/Name

    returns None if not found, or a mapping equivalent to:
        dict(
            location='Location',
            name='Name.framework/Versions/SomeVersion/Name_Suffix',
            shortname='Name',
            version='SomeVersion',
            suffix='Suffix',
        )

    Note that SomeVersion and Suffix are optional and may be None
    if not present
    """
    is_framework = STRICT_FRAMEWORK_RE.match(filename)
    if not is_framework:
        return
    return is_framework.groupdict()


def test_framework_info--- This code section failed: ---

 L.  45         0  LOAD_CONST               (None, None, None, None, None)
                2  LOAD_CODE                <code_object d>
                4  LOAD_STR                 'test_framework_info.<locals>.d'
                6  MAKE_FUNCTION_1          'default'
                8  STORE_FAST               'd'

 L.  53        10  LOAD_GLOBAL              framework_info
               12  LOAD_STR                 'completely/invalid'
               14  CALL_FUNCTION_1       1  ''
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_TRUE     26  'to 26'
               22  <74>             
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            20  '20'

 L.  54        26  LOAD_GLOBAL              framework_info
               28  LOAD_STR                 'completely/invalid/_debug'
               30  CALL_FUNCTION_1       1  ''
               32  LOAD_CONST               None
               34  <117>                 0  ''
               36  POP_JUMP_IF_TRUE     42  'to 42'
               38  <74>             
               40  RAISE_VARARGS_1       1  'exception instance'
             42_0  COME_FROM            36  '36'

 L.  55        42  LOAD_GLOBAL              framework_info
               44  LOAD_STR                 'P/F.framework'
               46  CALL_FUNCTION_1       1  ''
               48  LOAD_CONST               None
               50  <117>                 0  ''
               52  POP_JUMP_IF_TRUE     58  'to 58'
               54  <74>             
               56  RAISE_VARARGS_1       1  'exception instance'
             58_0  COME_FROM            52  '52'

 L.  56        58  LOAD_GLOBAL              framework_info
               60  LOAD_STR                 'P/F.framework/_debug'
               62  CALL_FUNCTION_1       1  ''
               64  LOAD_CONST               None
               66  <117>                 0  ''
               68  POP_JUMP_IF_TRUE     74  'to 74'
               70  <74>             
               72  RAISE_VARARGS_1       1  'exception instance'
             74_0  COME_FROM            68  '68'

 L.  57        74  LOAD_GLOBAL              framework_info
               76  LOAD_STR                 'P/F.framework/F'
               78  CALL_FUNCTION_1       1  ''
               80  LOAD_FAST                'd'
               82  LOAD_STR                 'P'
               84  LOAD_STR                 'F.framework/F'
               86  LOAD_STR                 'F'
               88  CALL_FUNCTION_3       3  ''
               90  COMPARE_OP               ==
               92  POP_JUMP_IF_TRUE     98  'to 98'
               94  <74>             
               96  RAISE_VARARGS_1       1  'exception instance'
             98_0  COME_FROM            92  '92'

 L.  58        98  LOAD_GLOBAL              framework_info
              100  LOAD_STR                 'P/F.framework/F_debug'
              102  CALL_FUNCTION_1       1  ''
              104  LOAD_FAST                'd'
              106  LOAD_STR                 'P'
              108  LOAD_STR                 'F.framework/F_debug'
              110  LOAD_STR                 'F'
              112  LOAD_STR                 'debug'
              114  LOAD_CONST               ('suffix',)
              116  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_TRUE    126  'to 126'
              122  <74>             
              124  RAISE_VARARGS_1       1  'exception instance'
            126_0  COME_FROM           120  '120'

 L.  59       126  LOAD_GLOBAL              framework_info
              128  LOAD_STR                 'P/F.framework/Versions'
              130  CALL_FUNCTION_1       1  ''
              132  LOAD_CONST               None
              134  <117>                 0  ''
              136  POP_JUMP_IF_TRUE    142  'to 142'
              138  <74>             
              140  RAISE_VARARGS_1       1  'exception instance'
            142_0  COME_FROM           136  '136'

 L.  60       142  LOAD_GLOBAL              framework_info
              144  LOAD_STR                 'P/F.framework/Versions/A'
              146  CALL_FUNCTION_1       1  ''
              148  LOAD_CONST               None
              150  <117>                 0  ''
              152  POP_JUMP_IF_TRUE    158  'to 158'
              154  <74>             
              156  RAISE_VARARGS_1       1  'exception instance'
            158_0  COME_FROM           152  '152'

 L.  61       158  LOAD_GLOBAL              framework_info
              160  LOAD_STR                 'P/F.framework/Versions/A/F'
              162  CALL_FUNCTION_1       1  ''
              164  LOAD_FAST                'd'
              166  LOAD_STR                 'P'
              168  LOAD_STR                 'F.framework/Versions/A/F'
              170  LOAD_STR                 'F'
              172  LOAD_STR                 'A'
              174  CALL_FUNCTION_4       4  ''
              176  COMPARE_OP               ==
              178  POP_JUMP_IF_TRUE    184  'to 184'
              180  <74>             
              182  RAISE_VARARGS_1       1  'exception instance'
            184_0  COME_FROM           178  '178'

 L.  62       184  LOAD_GLOBAL              framework_info
              186  LOAD_STR                 'P/F.framework/Versions/A/F_debug'
              188  CALL_FUNCTION_1       1  ''
              190  LOAD_FAST                'd'
              192  LOAD_STR                 'P'
              194  LOAD_STR                 'F.framework/Versions/A/F_debug'
              196  LOAD_STR                 'F'
              198  LOAD_STR                 'A'
              200  LOAD_STR                 'debug'
              202  CALL_FUNCTION_5       5  ''
              204  COMPARE_OP               ==
              206  POP_JUMP_IF_TRUE    212  'to 212'
              208  <74>             
              210  RAISE_VARARGS_1       1  'exception instance'
            212_0  COME_FROM           206  '206'

Parse error at or near `<117>' instruction at offset 18


if __name__ == '__main__':
    test_framework_info()