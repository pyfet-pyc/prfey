# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: ctypes\macholib\dylib.py
"""
Generic dylib path manipulation
"""
import re
__all__ = [
 'dylib_info']
DYLIB_RE = re.compile('(?x)\n(?P<location>^.*)(?:^|/)\n(?P<name>\n    (?P<shortname>\\w+?)\n    (?:\\.(?P<version>[^._]+))?\n    (?:_(?P<suffix>[^._]+))?\n    \\.dylib$\n)\n')

def dylib_info(filename):
    """
    A dylib name can take one of the following four forms:
        Location/Name.SomeVersion_Suffix.dylib
        Location/Name.SomeVersion.dylib
        Location/Name_Suffix.dylib
        Location/Name.dylib

    returns None if not found or a mapping equivalent to:
        dict(
            location='Location',
            name='Name.SomeVersion_Suffix.dylib',
            shortname='Name',
            version='SomeVersion',
            suffix='Suffix',
        )

    Note that SomeVersion and Suffix are optional and may be None
    if not present.
    """
    is_dylib = DYLIB_RE.match(filename)
    if not is_dylib:
        return
    return is_dylib.groupdict()


def test_dylib_info--- This code section failed: ---

 L.  46         0  LOAD_CONST               (None, None, None, None, None)
                2  LOAD_CODE                <code_object d>
                4  LOAD_STR                 'test_dylib_info.<locals>.d'
                6  MAKE_FUNCTION_1          'default'
                8  STORE_FAST               'd'

 L.  54        10  LOAD_GLOBAL              dylib_info
               12  LOAD_STR                 'completely/invalid'
               14  CALL_FUNCTION_1       1  ''
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_TRUE     26  'to 26'
               22  <74>             
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            20  '20'

 L.  55        26  LOAD_GLOBAL              dylib_info
               28  LOAD_STR                 'completely/invalide_debug'
               30  CALL_FUNCTION_1       1  ''
               32  LOAD_CONST               None
               34  <117>                 0  ''
               36  POP_JUMP_IF_TRUE     42  'to 42'
               38  <74>             
               40  RAISE_VARARGS_1       1  'exception instance'
             42_0  COME_FROM            36  '36'

 L.  56        42  LOAD_GLOBAL              dylib_info
               44  LOAD_STR                 'P/Foo.dylib'
               46  CALL_FUNCTION_1       1  ''
               48  LOAD_FAST                'd'
               50  LOAD_STR                 'P'
               52  LOAD_STR                 'Foo.dylib'
               54  LOAD_STR                 'Foo'
               56  CALL_FUNCTION_3       3  ''
               58  COMPARE_OP               ==
               60  POP_JUMP_IF_TRUE     66  'to 66'
               62  <74>             
               64  RAISE_VARARGS_1       1  'exception instance'
             66_0  COME_FROM            60  '60'

 L.  57        66  LOAD_GLOBAL              dylib_info
               68  LOAD_STR                 'P/Foo_debug.dylib'
               70  CALL_FUNCTION_1       1  ''
               72  LOAD_FAST                'd'
               74  LOAD_STR                 'P'
               76  LOAD_STR                 'Foo_debug.dylib'
               78  LOAD_STR                 'Foo'
               80  LOAD_STR                 'debug'
               82  LOAD_CONST               ('suffix',)
               84  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               86  COMPARE_OP               ==
               88  POP_JUMP_IF_TRUE     94  'to 94'
               90  <74>             
               92  RAISE_VARARGS_1       1  'exception instance'
             94_0  COME_FROM            88  '88'

 L.  58        94  LOAD_GLOBAL              dylib_info
               96  LOAD_STR                 'P/Foo.A.dylib'
               98  CALL_FUNCTION_1       1  ''
              100  LOAD_FAST                'd'
              102  LOAD_STR                 'P'
              104  LOAD_STR                 'Foo.A.dylib'
              106  LOAD_STR                 'Foo'
              108  LOAD_STR                 'A'
              110  CALL_FUNCTION_4       4  ''
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_TRUE    120  'to 120'
              116  <74>             
              118  RAISE_VARARGS_1       1  'exception instance'
            120_0  COME_FROM           114  '114'

 L.  59       120  LOAD_GLOBAL              dylib_info
              122  LOAD_STR                 'P/Foo_debug.A.dylib'
              124  CALL_FUNCTION_1       1  ''
              126  LOAD_FAST                'd'
              128  LOAD_STR                 'P'
              130  LOAD_STR                 'Foo_debug.A.dylib'
              132  LOAD_STR                 'Foo_debug'
              134  LOAD_STR                 'A'
              136  CALL_FUNCTION_4       4  ''
              138  COMPARE_OP               ==
              140  POP_JUMP_IF_TRUE    146  'to 146'
              142  <74>             
              144  RAISE_VARARGS_1       1  'exception instance'
            146_0  COME_FROM           140  '140'

 L.  60       146  LOAD_GLOBAL              dylib_info
              148  LOAD_STR                 'P/Foo.A_debug.dylib'
              150  CALL_FUNCTION_1       1  ''
              152  LOAD_FAST                'd'
              154  LOAD_STR                 'P'
              156  LOAD_STR                 'Foo.A_debug.dylib'
              158  LOAD_STR                 'Foo'
              160  LOAD_STR                 'A'
              162  LOAD_STR                 'debug'
              164  CALL_FUNCTION_5       5  ''
              166  COMPARE_OP               ==
              168  POP_JUMP_IF_TRUE    174  'to 174'
              170  <74>             
              172  RAISE_VARARGS_1       1  'exception instance'
            174_0  COME_FROM           168  '168'

Parse error at or near `<117>' instruction at offset 18


if __name__ == '__main__':
    test_dylib_info()