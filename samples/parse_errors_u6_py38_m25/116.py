# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: string.py
"""A collection of string constants.

Public module variables:

whitespace -- a string containing all ASCII whitespace
ascii_lowercase -- a string containing all ASCII lowercase letters
ascii_uppercase -- a string containing all ASCII uppercase letters
ascii_letters -- a string containing all ASCII letters
digits -- a string containing all ASCII decimal digits
hexdigits -- a string containing all ASCII hexadecimal digits
octdigits -- a string containing all ASCII octal digits
punctuation -- a string containing all ASCII punctuation characters
printable -- a string containing all ASCII characters considered printable

"""
__all__ = [
 'ascii_letters', 'ascii_lowercase', 'ascii_uppercase', 'capwords',
 'digits', 'hexdigits', 'octdigits', 'printable', 'punctuation',
 'whitespace', 'Formatter', 'Template']
import _string
whitespace = ' \t\n\r\x0b\x0c'
ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ascii_letters = ascii_lowercase + ascii_uppercase
digits = '0123456789'
hexdigits = digits + 'abcdef' + 'ABCDEF'
octdigits = '01234567'
punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
printable = digits + ascii_letters + punctuation + whitespace

def capwords(s, sep=None):
    """capwords(s [,sep]) -> string

    Split the argument into words using split, capitalize each
    word using capitalize, and join the capitalized words using
    join.  If the optional second argument sep is absent or None,
    runs of whitespace characters are replaced by a single space
    and leading and trailing whitespace are removed, otherwise
    sep is used to split and join the words.

    """
    return (sep or ' ').join((x.capitalize() for x in s.split(sep)))


import re as _re
from collections import ChainMap as _ChainMap
_sentinel_dict = {}

class _TemplateMetaclass(type):
    pattern = '\n    %(delim)s(?:\n      (?P<escaped>%(delim)s) |   # Escape sequence of two delimiters\n      (?P<named>%(id)s)      |   # delimiter and a Python identifier\n      {(?P<braced>%(bid)s)}  |   # delimiter and a braced identifier\n      (?P<invalid>)              # Other ill-formed delimiter exprs\n    )\n    '

    def __init__(cls, name, bases, dct):
        super(_TemplateMetaclass, cls).__init__(name, bases, dct)
        if 'pattern' in dct:
            pattern = cls.pattern
        else:
            pattern = _TemplateMetaclass.pattern % {'delim':_re.escape(cls.delimiter), 
             'id':cls.idpattern, 
             'bid':cls.braceidpattern or cls.idpattern}
        cls.pattern = _re.compile(pattern, cls.flags | _re.VERBOSE)


class Template(metaclass=_TemplateMetaclass):
    __doc__ = 'A string class for supporting $-substitutions.'
    delimiter = '$'
    idpattern = '(?a:[_a-z][_a-z0-9]*)'
    braceidpattern = None
    flags = _re.IGNORECASE

    def __init__(self, template):
        self.template = template

    def _invalid(self, mo):
        i = mo.start('invalid')
        lines = self.template[:i].splitlines(keepends=True)
        if not lines:
            colno = 1
            lineno = 1
        else:
            colno = i - len(''.join(lines[:-1]))
            lineno = len(lines)
        raise ValueError('Invalid placeholder in string: line %d, col %d' % (
         lineno, colno))

    def substitute(self, mapping=_sentinel_dict, **kws):
        if mapping is _sentinel_dict:
            mapping = kws
        else:
            if kws:
                mapping = _ChainMap(kws, mapping)

        def convert(mo):
            named = mo.group('named') or mo.group('braced')
            if named is not None:
                return str(mapping[named])
            if mo.group('escaped') is not None:
                return self.delimiter
            if mo.group('invalid') is not None:
                self._invalid(mo)
            raise ValueError('Unrecognized named group in pattern', self.pattern)

        return self.pattern.sub(convert, self.template)

    def safe_substitute(self, mapping=_sentinel_dict, **kws):
        if mapping is _sentinel_dict:
            mapping = kws
        else:
            if kws:
                mapping = _ChainMap(kws, mapping)

        def convert--- This code section failed: ---

 L. 135         0  LOAD_FAST                'mo'
                2  LOAD_METHOD              group
                4  LOAD_STR                 'named'
                6  CALL_METHOD_1         1  ''
                8  JUMP_IF_TRUE_OR_POP    18  'to 18'
               10  LOAD_FAST                'mo'
               12  LOAD_METHOD              group
               14  LOAD_STR                 'braced'
               16  CALL_METHOD_1         1  ''
             18_0  COME_FROM             8  '8'
               18  STORE_FAST               'named'

 L. 136        20  LOAD_FAST                'named'
               22  LOAD_CONST               None
               24  COMPARE_OP               is-not
               26  POP_JUMP_IF_FALSE    72  'to 72'

 L. 137        28  SETUP_FINALLY        44  'to 44'

 L. 138        30  LOAD_GLOBAL              str
               32  LOAD_DEREF               'mapping'
               34  LOAD_FAST                'named'
               36  BINARY_SUBSCR    
               38  CALL_FUNCTION_1       1  ''
               40  POP_BLOCK        
               42  RETURN_VALUE     
             44_0  COME_FROM_FINALLY    28  '28'

 L. 139        44  DUP_TOP          
               46  LOAD_GLOBAL              KeyError
               48  COMPARE_OP               exception-match
               50  POP_JUMP_IF_FALSE    70  'to 70'
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          

 L. 140        58  LOAD_FAST                'mo'
               60  LOAD_METHOD              group
               62  CALL_METHOD_0         0  ''
               64  ROT_FOUR         
               66  POP_EXCEPT       
               68  RETURN_VALUE     
             70_0  COME_FROM            50  '50'
               70  END_FINALLY      
             72_0  COME_FROM            26  '26'

 L. 141        72  LOAD_FAST                'mo'
               74  LOAD_METHOD              group
               76  LOAD_STR                 'escaped'
               78  CALL_METHOD_1         1  ''
               80  LOAD_CONST               None
               82  COMPARE_OP               is-not
               84  POP_JUMP_IF_FALSE    92  'to 92'

 L. 142        86  LOAD_DEREF               'self'
               88  LOAD_ATTR                delimiter
               90  RETURN_VALUE     
             92_0  COME_FROM            84  '84'

 L. 143        92  LOAD_FAST                'mo'
               94  LOAD_METHOD              group
               96  LOAD_STR                 'invalid'
               98  CALL_METHOD_1         1  ''
              100  LOAD_CONST               None
              102  COMPARE_OP               is-not
              104  POP_JUMP_IF_FALSE   114  'to 114'

 L. 144       106  LOAD_FAST                'mo'
              108  LOAD_METHOD              group
              110  CALL_METHOD_0         0  ''
              112  RETURN_VALUE     
            114_0  COME_FROM           104  '104'

 L. 145       114  LOAD_GLOBAL              ValueError
              116  LOAD_STR                 'Unrecognized named group in pattern'

 L. 146       118  LOAD_DEREF               'self'
              120  LOAD_ATTR                pattern

 L. 145       122  CALL_FUNCTION_2       2  ''
              124  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `POP_TOP' instruction at offset 54

        return self.pattern.sub(convert, self.template)


class Formatter:

    def format(self, format_string, *args, **kwargs):
        return self.vformat(format_string, args, kwargs)

    def vformat(self, format_string, args, kwargs):
        used_args = set()
        result, _ = self._vformat(format_string, args, kwargs, used_args, 2)
        self.check_unused_args(used_args, args, kwargs)
        return result

    def _vformat(self, format_string, args, kwargs, used_args, recursion_depth, auto_arg_index=0):
        if recursion_depth < 0:
            raise ValueError('Max string recursion exceeded')
        result = []
        for literal_text, field_name, format_spec, conversion in self.parse(format_string):
            if literal_text:
                result.append(literal_text)
            if field_name is not None:
                if field_name == '':
                    if auto_arg_index is False:
                        raise ValueError('cannot switch from manual field specification to automatic field numbering')
                    field_name = str(auto_arg_index)
                    auto_arg_index += 1
                else:
                    if field_name.isdigit():
                        if auto_arg_index:
                            raise ValueError('cannot switch from manual field specification to automatic field numbering')
                        auto_arg_index = False
                obj, arg_used = self.get_field(field_name, args, kwargs)
                used_args.add(arg_used)
                obj = self.convert_field(obj, conversion)
                format_spec, auto_arg_index = self._vformat(format_spec,
                  args, kwargs, used_args,
                  (recursion_depth - 1), auto_arg_index=auto_arg_index)
                result.append(self.format_field(obj, format_spec))
            return (''.join(result), auto_arg_index)

    def get_value(self, key, args, kwargs):
        if isinstance(key, int):
            return args[key]
        return kwargs[key]

    def check_unused_args(self, used_args, args, kwargs):
        pass

    def format_field(self, value, format_spec):
        return format(value, format_spec)

    def convert_field(self, value, conversion):
        if conversion is None:
            return value
        if conversion == 's':
            return str(value)
        if conversion == 'r':
            return repr(value)
        if conversion == 'a':
            return ascii(value)
        raise ValueError('Unknown conversion specifier {0!s}'.format(conversion))

    def parse(self, format_string):
        return _string.formatter_parser(format_string)

    def get_field(self, field_name, args, kwargs):
        first, rest = _string.formatter_field_name_split(field_name)
        obj = self.get_value(first, args, kwargs)
        for is_attr, i in rest:
            if is_attr:
                obj = getattr(obj, i)
            else:
                obj = obj[i]
        else:
            return (
             obj, first)