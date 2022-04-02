# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\openpyxl\descriptors\base.py
"""
Based on Python Cookbook 3rd Edition, 8.13
http://chimera.labs.oreilly.com/books/1230000000393/ch08.html#_discussiuncion_130
"""
import datetime, re
from openpyxl.utils.datetime import from_ISO8601
from .namespace import namespaced

class Descriptor(object):

    def __init__(self, name=None, **kw):
        self.name = name
        for k, v in kw.items():
            setattr(self, k, v)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value


class Typed(Descriptor):
    __doc__ = 'Values must of a particular type'
    expected_type = type(None)
    allow_none = False
    nested = False

    def __init__(self, *args, **kw):
        (super(Typed, self).__init__)(*args, **kw)
        self.__doc__ = 'Values must be of type {0}'.format(self.expected_type)

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            if self.allow_none:
                if not self.allow_none or value is not None:
                    raise TypeError('expected ' + str(self.expected_type))
        super(Typed, self).__set__(instance, value)

    def __repr__(self):
        return self.__doc__


def _convert(expected_type, value):
    """
    Check value is of or can be converted to expected type.
    """
    if not isinstance(value, expected_type):
        try:
            value = expected_type(value)
        except:
            raise TypeError('expected ' + str(expected_type))

    return value


class Convertible(Typed):
    __doc__ = 'Values must be convertible to a particular type'

    def __set__--- This code section failed: ---

 L.  65         0  LOAD_FAST                'self'
                2  LOAD_ATTR                allow_none
                4  POP_JUMP_IF_FALSE    14  'to 14'
                6  LOAD_FAST                'value'
                8  LOAD_CONST               None
               10  COMPARE_OP               is-not
               12  POP_JUMP_IF_TRUE     20  'to 20'
             14_0  COME_FROM             4  '4'

 L.  66        14  LOAD_FAST                'self'
               16  LOAD_ATTR                allow_none

 L.  65        18  POP_JUMP_IF_TRUE     32  'to 32'
             20_0  COME_FROM            12  '12'

 L.  67        20  LOAD_GLOBAL              _convert
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                expected_type
               26  LOAD_FAST                'value'
               28  CALL_FUNCTION_2       2  ''
               30  STORE_FAST               'value'
             32_0  COME_FROM            18  '18'

 L.  68        32  LOAD_GLOBAL              super
               34  LOAD_GLOBAL              Convertible
               36  LOAD_FAST                'self'
               38  CALL_FUNCTION_2       2  ''
               40  LOAD_METHOD              __set__
               42  LOAD_FAST                'instance'
               44  LOAD_FAST                'value'
               46  CALL_METHOD_2         2  ''
               48  POP_TOP          

Parse error at or near `CALL_METHOD_2' instruction at offset 46


class Max(Convertible):
    __doc__ = 'Values must be less than a `max` value'
    expected_type = float
    allow_none = False

    def __init__(self, **kw):
        if 'max' not in kw:
            if not hasattr(self, 'max'):
                raise TypeError('missing max value')
        (super(Max, self).__init__)(**kw)

    def __set__--- This code section failed: ---

 L.  83         0  LOAD_FAST                'self'
                2  LOAD_ATTR                allow_none
                4  POP_JUMP_IF_FALSE    14  'to 14'
                6  LOAD_FAST                'value'
                8  LOAD_CONST               None
               10  COMPARE_OP               is-not
               12  POP_JUMP_IF_TRUE     20  'to 20'
             14_0  COME_FROM             4  '4'

 L.  84        14  LOAD_FAST                'self'
               16  LOAD_ATTR                allow_none

 L.  83        18  POP_JUMP_IF_TRUE     58  'to 58'
             20_0  COME_FROM            12  '12'

 L.  85        20  LOAD_GLOBAL              _convert
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                expected_type
               26  LOAD_FAST                'value'
               28  CALL_FUNCTION_2       2  ''
               30  STORE_FAST               'value'

 L.  86        32  LOAD_FAST                'value'
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                max
               38  COMPARE_OP               >
               40  POP_JUMP_IF_FALSE    58  'to 58'

 L.  87        42  LOAD_GLOBAL              ValueError
               44  LOAD_STR                 'Max value is {0}'
               46  LOAD_METHOD              format
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                max
               52  CALL_METHOD_1         1  ''
               54  CALL_FUNCTION_1       1  ''
               56  RAISE_VARARGS_1       1  'exception instance'
             58_0  COME_FROM            40  '40'
             58_1  COME_FROM            18  '18'

 L.  88        58  LOAD_GLOBAL              super
               60  LOAD_GLOBAL              Max
               62  LOAD_FAST                'self'
               64  CALL_FUNCTION_2       2  ''
               66  LOAD_METHOD              __set__
               68  LOAD_FAST                'instance'
               70  LOAD_FAST                'value'
               72  CALL_METHOD_2         2  ''
               74  POP_TOP          

Parse error at or near `CALL_METHOD_2' instruction at offset 72


class Min(Convertible):
    __doc__ = 'Values must be greater than a `min` value'
    expected_type = float
    allow_none = False

    def __init__(self, **kw):
        if 'min' not in kw:
            if not hasattr(self, 'min'):
                raise TypeError('missing min value')
        (super(Min, self).__init__)(**kw)

    def __set__--- This code section failed: ---

 L. 103         0  LOAD_FAST                'self'
                2  LOAD_ATTR                allow_none
                4  POP_JUMP_IF_FALSE    14  'to 14'
                6  LOAD_FAST                'value'
                8  LOAD_CONST               None
               10  COMPARE_OP               is-not
               12  POP_JUMP_IF_TRUE     20  'to 20'
             14_0  COME_FROM             4  '4'

 L. 104        14  LOAD_FAST                'self'
               16  LOAD_ATTR                allow_none

 L. 103        18  POP_JUMP_IF_TRUE     58  'to 58'
             20_0  COME_FROM            12  '12'

 L. 105        20  LOAD_GLOBAL              _convert
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                expected_type
               26  LOAD_FAST                'value'
               28  CALL_FUNCTION_2       2  ''
               30  STORE_FAST               'value'

 L. 106        32  LOAD_FAST                'value'
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                min
               38  COMPARE_OP               <
               40  POP_JUMP_IF_FALSE    58  'to 58'

 L. 107        42  LOAD_GLOBAL              ValueError
               44  LOAD_STR                 'Min value is {0}'
               46  LOAD_METHOD              format
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                min
               52  CALL_METHOD_1         1  ''
               54  CALL_FUNCTION_1       1  ''
               56  RAISE_VARARGS_1       1  'exception instance'
             58_0  COME_FROM            40  '40'
             58_1  COME_FROM            18  '18'

 L. 108        58  LOAD_GLOBAL              super
               60  LOAD_GLOBAL              Min
               62  LOAD_FAST                'self'
               64  CALL_FUNCTION_2       2  ''
               66  LOAD_METHOD              __set__
               68  LOAD_FAST                'instance'
               70  LOAD_FAST                'value'
               72  CALL_METHOD_2         2  ''
               74  POP_TOP          

Parse error at or near `CALL_METHOD_2' instruction at offset 72


class MinMax(Min, Max):
    __doc__ = 'Values must be greater than `min` value and less than a `max` one'


class Set(Descriptor):
    __doc__ = 'Value can only be from a set of know values'

    def __init__(self, name=None, **kw):
        if 'values' not in kw:
            raise TypeError('missing set of values')
        kw['values'] = set(kw['values'])
        (super(Set, self).__init__)(name, **kw)
        self.__doc__ = 'Value must be one of {0}'.format(self.values)

    def __set__(self, instance, value):
        if value not in self.values:
            raise ValueError(self.__doc__)
        super(Set, self).__set__(instance, value)


class NoneSet(Set):
    __doc__ = "'none' will be treated as None"

    def __init__(self, name=None, **kw):
        (super(NoneSet, self).__init__)(name, **kw)
        self.values.add(None)

    def __set__(self, instance, value):
        if value == 'none':
            value = None
        super(NoneSet, self).__set__(instance, value)


class Integer(Convertible):
    expected_type = int


class Float(Convertible):
    expected_type = float


class Bool(Convertible):
    expected_type = bool

    def __set__(self, instance, value):
        if isinstance(value, str):
            if value in ('false', 'f', '0'):
                value = False
        super(Bool, self).__set__(instance, value)


class String(Typed):
    expected_type = str


class Text(String, Convertible):
    pass


class ASCII(Typed):
    expected_type = bytes


class Tuple(Typed):
    expected_type = tuple


class Length(Descriptor):

    def __init__(self, name=None, **kw):
        if 'length' not in kw:
            raise TypeError('value length must be supplied')
        (super(Length, self).__init__)(**kw)

    def __set__(self, instance, value):
        if len(value) != self.length:
            raise ValueError('Value must be length {0}'.format(self.length))
        super(Length, self).__set__(instance, value)


class Default(Typed):
    __doc__ = '\n    When called returns an instance of the expected type.\n    Additional default values can be passed in to the descriptor\n    '

    def __init__(self, name=None, **kw):
        if 'defaults' not in kw:
            kw['defaults'] = {}
        (super(Default, self).__init__)(**kw)

    def __call__(self):
        return self.expected_type()


class Alias(Descriptor):
    __doc__ = '\n    Aliases can be used when either the desired attribute name is not allowed\n    or confusing in Python (eg. "type") or a more descriptve name is desired\n    (eg. "underline" for "u")\n    '

    def __init__(self, alias):
        self.alias = alias

    def __set__(self, instance, value):
        setattr(instance, self.alias, value)

    def __get__(self, instance, cls):
        return getattr(instance, self.alias)


class MatchPattern(Descriptor):
    __doc__ = 'Values must match a regex pattern '
    allow_none = False

    def __init__(self, name=None, **kw):
        if 'pattern' not in kw:
            if not hasattr(self, 'pattern'):
                raise TypeError('missing pattern value')
        (super(MatchPattern, self).__init__)(name, **kw)
        self.test_pattern = re.compile(self.pattern, re.VERBOSE)

    def __set__(self, instance, value):
        if value is None:
            if not self.allow_none:
                raise ValueError('Value must not be none')
        elif self.allow_none and not value is not None or self.allow_none or self.test_pattern.match(value):
            raise ValueError('Value does not match pattern {0}'.format(self.pattern))
        super(MatchPattern, self).__set__(instance, value)


class DateTime(Typed):
    expected_type = datetime.datetime

    def __set__(self, instance, value):
        if value is not None:
            if isinstance(value, str):
                try:
                    value = from_ISO8601(value)
                except ValueError:
                    raise ValueError('Value must be ISO datetime format')

        super(DateTime, self).__set__(instance, value)