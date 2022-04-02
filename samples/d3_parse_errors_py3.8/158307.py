# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: dropbox\stone_validators.py
"""
Defines classes to represent each Stone type in Python. These classes should
be used to validate Python objects and normalize them for a given type.

The data types defined here should not be specific to an RPC or serialization
format.

This module should be dropped into a project that requires the use of Stone. In
the future, this could be imported from a pre-installed Python package, rather
than being added to a project.
"""
from __future__ import absolute_import, unicode_literals
from abc import ABCMeta, abstractmethod
import datetime, hashlib, math, numbers, re, six
_MYPY = False
if _MYPY:
    import typing
if six.PY3:
    _binary_types = (
     bytes, memoryview)
else:
    _binary_types = (
     bytes, buffer)

class ValidationError(Exception):
    __doc__ = "Raised when a value doesn't pass validation by its validator."

    def __init__(self, message, parent=None):
        """
        Args:
            message (str): Error message detailing validation failure.
            parent (str): Adds the parent as the closest reference point for
                the error. Use :meth:`add_parent` to add more.
        """
        super(ValidationError, self).__init__(message)
        self.message = message
        self._parents = []
        if parent:
            self._parents.append(parent)

    def add_parent(self, parent):
        """
        Args:
            parent (str): Adds the parent to the top of the tree of references
                that lead to the validator that failed.
        """
        self._parents.append(parent)

    def __str__(self):
        """
        Returns:
            str: A descriptive message of the validation error that may also
                include the path to the validator that failed.
        """
        if self._parents:
            return '{}: {}'.format('.'.join(self._parents[::-1]), self.message)
        return self.message

    def __repr__(self):
        return 'ValidationError(%r)' % six.text_type(self)


def generic_type_name(v):
    """Return a descriptive type name that isn't Python specific. For example,
    an int value will return 'integer' rather than 'int'."""
    if isinstance(v, bool):
        return 'boolean'
    if isinstance(v, numbers.Integral):
        return 'integer'
    if isinstance(v, numbers.Real):
        return 'float'
    if isinstance(v, (tuple, list)):
        return 'list'
    if isinstance(v, six.string_types):
        return 'string'
    if v is None:
        return 'null'
    return type(v).__name__


class Validator(six.with_metaclass(ABCMeta, object)):
    __doc__ = 'All primitive and composite data types should be a subclass of this.'

    @abstractmethod
    def validate(self, val):
        """Validates that val is of this data type.

        Returns: A normalized value if validation succeeds.
        Raises: ValidationError
        """
        pass

    def has_default(self):
        return False

    def get_default(self):
        raise AssertionError('No default available.')


class Primitive(Validator):
    __doc__ = 'A basic type that is defined by Stone.'


class Boolean(Primitive):

    def validate(self, val):
        if not isinstance(val, bool):
            raise ValidationError('%r is not a valid boolean' % val)
        return val


class Integer(Primitive):
    __doc__ = "\n    Do not use this class directly. Extend it and specify a 'minimum' and\n    'maximum' value as class variables for a more restrictive integer range.\n    "
    minimum = None
    maximum = None

    def __init__(self, min_value=None, max_value=None):
        """
        A more restrictive minimum or maximum value can be specified than the
        range inherent to the defined type.
        """
        if min_value is not None:
            assert isinstance(min_value, numbers.Integral), 'min_value must be an integral number'
            assert min_value >= self.minimum, 'min_value cannot be less than the minimum value for this type (%d < %d)' % (
             min_value, self.minimum)
            self.minimum = min_value
        if max_value is not None:
            assert isinstance(max_value, numbers.Integral), 'max_value must be an integral number'
            assert max_value <= self.maximum, 'max_value cannot be greater than the maximum value for this type (%d < %d)' % (
             max_value, self.maximum)
            self.maximum = max_value

    def validate(self, val):
        if not isinstance(val, numbers.Integral):
            raise ValidationError('expected integer, got %s' % generic_type_name(val))
        elif not self.minimum <= val <= self.maximum:
            raise ValidationError('%d is not within range [%d, %d]' % (
             val, self.minimum, self.maximum))
        return val

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class Int32(Integer):
    minimum = -2147483648
    maximum = 2147483647


class UInt32(Integer):
    minimum = 0
    maximum = 4294967295


class Int64(Integer):
    minimum = -9223372036854775808
    maximum = 9223372036854775807


class UInt64(Integer):
    minimum = 0
    maximum = 18446744073709551615


class Real(Primitive):
    __doc__ = "\n    Do not use this class directly. Extend it and optionally set a 'minimum'\n    and 'maximum' value to enforce a range that's a subset of the Python float\n    implementation. Python floats are doubles.\n    "
    minimum = None
    maximum = None

    def __init__(self, min_value=None, max_value=None):
        """
        A more restrictive minimum or maximum value can be specified than the
        range inherent to the defined type.
        """
        if min_value is not None:
            assert isinstance(min_value, numbers.Real), 'min_value must be a real number'
            if not isinstance(min_value, float):
                try:
                    min_value = float(min_value)
                except OverflowError:
                    raise AssertionError('min_value is too small for a float')

            if self.minimum is not None:
                if min_value < self.minimum:
                    raise AssertionError('min_value cannot be less than the minimum value for this type (%f < %f)' % (
                     min_value, self.minimum))
            self.minimum = min_value
        if max_value is not None:
            assert isinstance(max_value, numbers.Real), 'max_value must be a real number'
            if not isinstance(max_value, float):
                try:
                    max_value = float(max_value)
                except OverflowError:
                    raise AssertionError('max_value is too large for a float')

            if self.maximum is not None:
                if max_value > self.maximum:
                    raise AssertionError('max_value cannot be greater than the maximum value for this type (%f < %f)' % (
                     max_value, self.maximum))
            self.maximum = max_value

    def validate(self, val):
        if not isinstance(val, numbers.Real):
            raise ValidationError('expected real number, got %s' % generic_type_name(val))
        if not isinstance(val, float):
            try:
                val = float(val)
            except OverflowError:
                raise ValidationError('too large for float')
            else:
                if math.isnan(val) or (math.isinf(val)):
                    raise ValidationError('%f values are not supported' % val)
                if self.minimum is not None:
                    if val < self.minimum:
                        raise ValidationError('%f is not greater than %f' % (
                         val, self.minimum))
                if self.maximum is not None:
                    if val > self.maximum:
                        raise ValidationError('%f is not less than %f' % (
                         val, self.maximum))
            return val

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class Float32(Real):
    minimum = -3.40282 * 10 ** 38
    maximum = 3.40282 * 10 ** 38


class Float64(Real):
    pass


class String(Primitive):
    __doc__ = 'Represents a unicode string.'

    def __init__(self, min_length=None, max_length=None, pattern=None):
        if min_length is not None:
            assert isinstance(min_length, numbers.Integral), 'min_length must be an integral number'
            assert min_length >= 0, 'min_length must be >= 0'
            if max_length is not None:
                assert isinstance(max_length, numbers.Integral), 'max_length must be an integral number'
                assert max_length > 0, 'max_length must be > 0'
                if min_length:
                    if max_length:
                        assert max_length >= min_length, 'max_length must be >= min_length'
                        if pattern is not None:
                            if not isinstance(pattern, six.string_types):
                                raise AssertionError('pattern must be a string')
                    self.min_length = min_length
                    self.max_length = max_length
                    self.pattern = pattern
                    self.pattern_re = None
                    if pattern:
                        try:
                            self.pattern_re = re.compile('\\A(?:' + pattern + ')\\Z')
                        except re.error as e:
                            try:
                                raise AssertionError('Regex {!r} failed: {}'.format(pattern, e.args[0]))
                            finally:
                                e = None
                                del e

    def validate(self, val):
        """
        A unicode string of the correct length and pattern will pass validation.
        In PY2, we enforce that a str type must be valid utf-8, and a unicode
        string will be returned.
        """
        if not isinstance(val, six.string_types):
            raise ValidationError("'%s' expected to be a string, got %s" % (
             val, generic_type_name(val)))
        if not six.PY3 or isinstance(val, str):
            try:
                val = val.decode('utf-8')
            except UnicodeDecodeError:
                raise ValidationError("'%s' was not valid utf-8" % val)
            else:
                if self.max_length is not None:
                    if len(val) > self.max_length:
                        raise ValidationError("'%s' must be at most %d characters, got %d" % (
                         val, self.max_length, len(val)))
                if self.min_length is not None:
                    if len(val) < self.min_length:
                        raise ValidationError("'%s' must be at least %d characters, got %d" % (
                         val, self.min_length, len(val)))
        if self.pattern:
            if not self.pattern_re.match(val):
                raise ValidationError("'%s' did not match pattern '%s'" % (
                 val, self.pattern))
            return val


class Bytes(Primitive):

    def __init__(self, min_length=None, max_length=None):
        if min_length is not None:
            assert isinstance(min_length, numbers.Integral), 'min_length must be an integral number'
            assert min_length >= 0, 'min_length must be >= 0'
            if max_length is not None:
                assert isinstance(max_length, numbers.Integral), 'max_length must be an integral number'
                if not max_length > 0:
                    raise AssertionError('max_length must be > 0')
        if not min_length is not None or max_length is not None:
            assert max_length >= min_length, 'max_length must be >= min_length'
            self.min_length = min_length
            self.max_length = max_length

    def validate(self, val):
        if not isinstance(val, _binary_types):
            raise ValidationError('expected bytes type, got %s' % generic_type_name(val))
        elif self.max_length is not None and len(val) > self.max_length:
            raise ValidationError("'%s' must have at most %d bytes, got %d" % (
             val, self.max_length, len(val)))
        elif self.min_length is not None:
            if len(val) < self.min_length:
                raise ValidationError("'%s' has fewer than %d bytes, got %d" % (
                 val, self.min_length, len(val)))
        return val


class Timestamp(Primitive):
    __doc__ = "Note that while a format is specified, it isn't used in validation\n    since a native Python datetime object is preferred. The format, however,\n    can and should be used by serializers."

    def __init__(self, fmt):
        """fmt must be composed of format codes that the C standard (1989)
        supports, most notably in its strftime() function."""
        assert isinstance(fmt, six.text_type), 'format must be a string'
        self.format = fmt

    def validate(self, val):
        if not isinstance(val, datetime.datetime):
            raise ValidationError('expected timestamp, got %s' % generic_type_name(val))
        elif val.tzinfo is not None:
            if val.tzinfo.utcoffset(val).total_seconds() != 0:
                raise ValidationError('timestamp should have either a UTC timezone or none set at all')
        return val


class Composite(Validator):
    __doc__ = 'Validator for a type that builds on other primitive and composite\n    types.'


class List(Composite):
    __doc__ = 'Assumes list contents are homogeneous with respect to types.'

    def __init__(self, item_validator, min_items=None, max_items=None):
        """Every list item will be validated with item_validator."""
        self.item_validator = item_validator
        if min_items is not None:
            assert isinstance(min_items, numbers.Integral), 'min_items must be an integral number'
            assert min_items >= 0, 'min_items must be >= 0'
            if max_items is not None:
                assert isinstance(max_items, numbers.Integral), 'max_items must be an integral number'
                if not max_items > 0:
                    raise AssertionError('max_items must be > 0')
        if not min_items is not None or max_items is not None:
            assert max_items >= min_items, 'max_items must be >= min_items'
            self.min_items = min_items
            self.max_items = max_items

    def validate(self, val):
        if not isinstance(val, (tuple, list)):
            raise ValidationError('%r is not a valid list' % val)
        elif self.max_items is not None and len(val) > self.max_items:
            raise ValidationError('%r has more than %s items' % (
             val, self.max_items))
        elif self.min_items is not None:
            if len(val) < self.min_items:
                raise ValidationError('%r has fewer than %s items' % (
                 val, self.min_items))
        return [self.item_validator.validate(item) for item in val]


class Map(Composite):
    __doc__ = 'Assumes map keys and values are homogeneous with respect to types.'

    def __init__(self, key_validator, value_validator):
        """
        Every Map key/value pair will be validated with item_validator.
        key validators must be a subclass of a String validator
        """
        self.key_validator = key_validator
        self.value_validator = value_validator

    def validate(self, val):
        if not isinstance(val, dict):
            raise ValidationError('%r is not a valid dict' % val)
        return {self.value_validator.validate(value):self.key_validator.validate(key) for key, value in val.items()}


class Struct(Composite):

    def __init__(self, definition):
        super(Struct, self).__init__()
        self.definition = definition

    def validate(self, val):
        """
        For a val to pass validation, val must be of the correct type and have
        all required fields present.
        """
        self.validate_type_only(val)
        self.validate_fields_only(val)
        return val

    def validate_with_permissions(self, val, caller_permissions):
        """
        For a val to pass validation, val must be of the correct type and have
        all required permissioned fields present. Should only be called
        for callers with extra permissions.
        """
        self.validate(val)
        self.validate_fields_only_with_permissions(val, caller_permissions)
        return val

    def validate_fields_only(self, val):
        """
        To pass field validation, no required field should be missing.

        This method assumes that the contents of each field have already been
        validated on assignment, so it's merely a presence check.

        FIXME(kelkabany): Since the definition object does not maintain a list
        of which fields are required, all fields are scanned.
        """
        for field_name in self.definition._all_field_names_:
            if not hasattr(val, field_name):
                raise ValidationError("missing required field '%s'" % field_name)

    def validate_fields_only_with_permissions(self, val, caller_permissions):
        """
        To pass field validation, no required field should be missing.
        This method assumes that the contents of each field have already been
        validated on assignment, so it's merely a presence check.
        Should only be called for callers with extra permissions.
        """
        self.validate_fields_only(val)
        for extra_permission in caller_permissions.permissions:
            all_field_names = '_all_{}_field_names_'.format(extra_permission)
            for field_name in getattr(self.definition, all_field_names, set()):
                if not hasattr(val, field_name):
                    raise ValidationError("missing required field '%s'" % field_name)

    def validate_type_only(self, val):
        """
        Use this when you only want to validate that the type of an object
        is correct, but not yet validate each field.
        """
        if not isinstance(val, self.definition):
            raise ValidationError('expected type %s, got %s' % (
             self.definition.__name__, generic_type_name(val)))

    def has_default(self):
        return not self.definition._has_required_fields

    def get_default(self):
        if self.definition._has_required_fields:
            raise AssertionError('No default available.')
        return self.definition()


class StructTree(Struct):
    __doc__ = 'Validator for structs with enumerated subtypes.\n\n    NOTE: validate_fields_only() validates the fields known to this base\n    struct, but does not do any validation specific to the subtype.\n    '

    def __init__(self, definition):
        super(StructTree, self).__init__(definition)


class Union(Composite):

    def __init__(self, definition):
        """
        Args:
            definition (class): A generated class representing a Stone union
                from a spec. Must have a _tagmap attribute with the following
                structure:

                _tagmap = {field_name: validator, ...}

                where
                    field_name (str): Tag name.
                    validator (Validator): Tag value validator.
        """
        self.definition = definition

    def validate(self, val):
        """
        For a val to pass validation, it must have a _tag set. This assumes
        that the object validated that _tag is a valid tag, and that any
        associated value has also been validated.
        """
        self.validate_type_only(val)
        if not hasattr(val, '_tag') or val._tag is None:
            raise ValidationError('no tag set')
        return val

    def validate_type_only(self, val):
        """
        Use this when you only want to validate that the type of an object
        is correct, but not yet validate each field.

        We check whether val is a Python parent class of the definition. This
        is because Union subtyping works in the opposite direction of Python
        inheritance. For example, if a union U2 extends U1 in Python, this
        validator will accept U1 in places where U2 is expected.
        """
        if not issubclass(self.definition, type(val)):
            raise ValidationError('expected type %s or subtype, got %s' % (
             self.definition.__name__, generic_type_name(val)))


class Void(Primitive):

    def validate(self, val):
        if val is not None:
            raise ValidationError('expected NoneType, got %s' % generic_type_name(val))

    def has_default(self):
        return True

    def get_default(self):
        pass


class Nullable(Validator):

    def __init__(self, validator):
        assert isinstance(validator, (Primitive, Composite)), 'validator must be for a primitive or composite type'
        if isinstance(validator, Nullable):
            raise AssertionError('nullables cannot be stacked')
        if isinstance(validator, Void):
            raise AssertionError('void cannot be made nullable')
        self.validator = validator

    def validate(self, val):
        if val is None:
            return
        return self.validator.validate(val)

    def validate_type_only(self, val):
        """Use this only if Nullable is wrapping a Composite."""
        if val is None:
            return
        return self.validator.validate_type_only(val)

    def has_default(self):
        return True

    def get_default(self):
        pass


class Redactor(object):

    def __init__(self, regex):
        """
        Args:
            regex: What parts of the field to redact.
        """
        self.regex = regex

    @abstractmethod
    def apply(self, val):
        """Redacts information from annotated field.
        Returns: A redacted version of the string provided.
        """
        pass

    def _get_matches--- This code section failed: ---

 L. 639         0  LOAD_FAST                'self'
                2  LOAD_ATTR                regex
                4  POP_JUMP_IF_TRUE     10  'to 10'

 L. 640         6  LOAD_CONST               None
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L. 641        10  SETUP_FINALLY        28  'to 28'

 L. 642        12  LOAD_GLOBAL              re
               14  LOAD_METHOD              search
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                regex
               20  LOAD_FAST                'val'
               22  CALL_METHOD_2         2  ''
               24  POP_BLOCK        
               26  RETURN_VALUE     
             28_0  COME_FROM_FINALLY    10  '10'

 L. 643        28  DUP_TOP          
               30  LOAD_GLOBAL              TypeError
               32  COMPARE_OP               exception-match
               34  POP_JUMP_IF_FALSE    48  'to 48'
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 644        42  POP_EXCEPT       
               44  LOAD_CONST               None
               46  RETURN_VALUE     
             48_0  COME_FROM            34  '34'
               48  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 44


class HashRedactor(Redactor):

    def apply(self, val):
        matches = self._get_matches(val)
        val_to_hash = str(val) if (isinstance(val, int) or isinstance(val, float)) else val
        try:
            hashed = hashlib.md5(val_to_hash.encode('utf-8')).hexdigest() + ''
        except [AttributeError, ValueError]:
            hashed = None
        else:
            if matches:
                blotted = '***'.join(matches.groups())
                if hashed:
                    return '{} ({})'.format(hashed, blotted)
                else:
                    return blotted
            else:
                return hashed


class BlotRedactor(Redactor):

    def apply(self, val):
        matches = self._get_matches(val)
        if matches:
            return '***'.join(matches.groups())
        return '********'