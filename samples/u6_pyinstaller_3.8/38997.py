# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: dropbox\stone_serializers.py
"""
Serializers for Stone data types.

Currently, only JSON is officially supported, but there's an experimental
msgpack integration. If possible, serializers should be kept separate from the
RPC format.

This module should be dropped into a project that requires the use of Stone. In
the future, this could be imported from a pre-installed Python package, rather
than being added to a project.
"""
from __future__ import absolute_import, unicode_literals
import base64, binascii, collections, datetime, functools, json, re, six, time
try:
    from . import stone_base as bb
    from . import stone_validators as bv
except (ImportError, SystemError, ValueError):
    import stone_validators as bb, stone_validators as bv
else:
    _MYPY = False
    if _MYPY:
        import typing

    class CallerPermissionsInterface(object):

        @property
        def permissions(self):
            """
        Returns the list of permissions this caller has access to.
        """
            raise NotImplementedError


    class CallerPermissionsDefault(CallerPermissionsInterface):

        @property
        def permissions(self):
            return []


    class StoneEncoderInterface(object):
        __doc__ = '\n    Interface defining a stone object encoder.\n    '

        def encode(self, validator, value):
            """
        Validate ``value`` using ``validator`` and return the encoding.

        Args:
            validator: the ``stone_validators.Validator`` used to validate
                ``value``
            value: the object to encode

        Returns:
            The encoded object. This is implementation-defined.

        Raises:
            stone_validators.ValidationError: Raised if ``value`` (or one
                of its sub-values).
        """
            raise NotImplementedError


    class StoneSerializerBase(StoneEncoderInterface):

        def __init__(self, caller_permissions, alias_validators):
            """
        Constructor, `obviously
        <http://www.geekalerts.com/ew-hand-sanitizer/>`.

        Args:
            caller_permissions (list): The list of raw-string caller permissions with which
                to serialize.
            alias_validators (``typing.Mapping``, optional): A mapping of
                custom validation callables in the format
                ``{stone_validators.Validator:
                typing.Callable[[typing.Any], None], ...}``. These callables must
                raise a ``stone_validators.ValidationError`` on failure.
                Defaults to ``None``.
        """
            self.caller_permissions = caller_permissions if caller_permissions else CallerPermissionsDefault()
            self._alias_validators = {}
            if alias_validators is not None:
                self._alias_validators.update(alias_validators)

        @property
        def alias_validators(self):
            """
        A ``typing.Mapping`` of custom validation callables in the format
        ``{stone_validators.Validator: typing.Callable[typing.Any],
        ...}``.
        """
            return self._alias_validators

        def encode(self, validator, value):
            return self.encode_sub(validator, value)

        def encode_sub(self, validator, value):
            """
        Callback intended to be called by other ``encode`` methods to
        delegate encoding of sub-values. Arguments have the same semantics
        as with the ``encode`` method.
        """
            if isinstance(validator, bv.List):
                validate_f = validator.validate
                encode_f = self.encode_list
            else:
                if isinstance(validator, bv.Map):
                    validate_f = validator.validate
                    encode_f = self.encode_map
                else:
                    if isinstance(validator, bv.Nullable):
                        validate_f = validator.validate
                        encode_f = self.encode_nullable
                    else:
                        if isinstance(validator, bv.Primitive):
                            validate_f = validator.validate
                            encode_f = self.encode_primitive
                        else:
                            if isinstance(validator, bv.Struct):
                                if isinstance(validator, bv.StructTree):
                                    if self.caller_permissions.permissions:

                                        def validate_with_permissions(val):
                                            validator.validate_with_permissions(val, self.caller_permissions)

                                        validate_f = validate_with_permissions
                                    else:
                                        validate_f = validator.validate
                                    encode_f = self.encode_struct_tree
                                else:
                                    if self.caller_permissions.permissions:

                                        def validate_with_permissions(val):
                                            validator.validate_with_permissions(val, self.caller_permissions)

                                        validate_f = validate_with_permissions
                                    else:
                                        validate_f = validator.validate_type_only
                                    encode_f = self.encode_struct
                            else:
                                if isinstance(validator, bv.Union):
                                    validate_f = validator.validate_type_only
                                    encode_f = self.encode_union
                                else:
                                    raise bv.ValidationError('Unsupported data type {}'.format(type(validator).__name__))
            validate_f(value)
            return encode_f(validator, value)

        def encode_list(self, validator, value):
            """
        Callback for serializing a ``stone_validators.List``. Arguments
        have the same semantics as with the ``encode`` method.
        """
            raise NotImplementedError

        def encode_map(self, validator, value):
            """
        Callback for serializing a ``stone_validators.Map``. Arguments
        have the same semantics as with the ``encode`` method.
        """
            raise NotImplementedError

        def encode_nullable(self, validator, value):
            """
        Callback for serializing a ``stone_validators.Nullable``.
        Arguments have the same semantics as with the ``encode`` method.
        """
            raise NotImplementedError

        def encode_primitive(self, validator, value):
            """
        Callback for serializing a ``stone_validators.Primitive``.
        Arguments have the same semantics as with the ``encode`` method.
        """
            raise NotImplementedError

        def encode_struct(self, validator, value):
            """
        Callback for serializing a ``stone_validators.Struct``. Arguments
        have the same semantics as with the ``encode`` method.
        """
            raise NotImplementedError

        def encode_struct_tree(self, validator, value):
            """
        Callback for serializing a ``stone_validators.StructTree``.
        Arguments have the same semantics as with the ``encode`` method.
        """
            raise NotImplementedError

        def encode_union(self, validator, value):
            """
        Callback for serializing a ``stone_validators.Union``. Arguments
        have the same semantics as with the ``encode`` method.
        """
            raise NotImplementedError


    class StoneToPythonPrimitiveSerializer(StoneSerializerBase):

        def __init__(self, caller_permissions, alias_validators, for_msgpack, old_style, should_redact):
            super(StoneToPythonPrimitiveSerializer, self).__init__(caller_permissions,
              alias_validators=alias_validators)
            self._for_msgpack = for_msgpack
            self._old_style = old_style
            self.should_redact = should_redact

        @property
        def for_msgpack(self):
            """
        EXPERIMENTAL: A flag associated with the serializer indicating
        whether objects produced by the ``encode`` method should be
        encoded for msgpack.

        """
            return self._for_msgpack

        @property
        def old_style(self):
            """
        A flag associated with the serializer indicating whether objects
        produced by the ``encode`` method should be encoded according to
        Dropbox's old or new API styles.
        """
            return self._old_style

        def encode_sub--- This code section failed: ---

 L. 271         0  LOAD_FAST                'self'
                2  LOAD_ATTR                should_redact
                4  POP_JUMP_IF_FALSE    88  'to 88'
                6  LOAD_GLOBAL              hasattr
                8  LOAD_DEREF               'validator'
               10  LOAD_STR                 '_redact'
               12  CALL_FUNCTION_2       2  ''
               14  POP_JUMP_IF_FALSE    88  'to 88'

 L. 272        16  LOAD_GLOBAL              isinstance
               18  LOAD_FAST                'value'
               20  LOAD_GLOBAL              list
               22  CALL_FUNCTION_2       2  ''
               24  POP_JUMP_IF_FALSE    44  'to 44'

 L. 273        26  LOAD_CLOSURE             'validator'
               28  BUILD_TUPLE_1         1 
               30  LOAD_LISTCOMP            '<code_object <listcomp>>'
               32  LOAD_STR                 'StoneToPythonPrimitiveSerializer.encode_sub.<locals>.<listcomp>'
               34  MAKE_FUNCTION_8          'closure'
               36  LOAD_FAST                'value'
               38  GET_ITER         
               40  CALL_FUNCTION_1       1  ''
               42  RETURN_VALUE     
             44_0  COME_FROM            24  '24'

 L. 274        44  LOAD_GLOBAL              isinstance
               46  LOAD_FAST                'value'
               48  LOAD_GLOBAL              dict
               50  CALL_FUNCTION_2       2  ''
               52  POP_JUMP_IF_FALSE    76  'to 76'

 L. 275        54  LOAD_CLOSURE             'validator'
               56  BUILD_TUPLE_1         1 
               58  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               60  LOAD_STR                 'StoneToPythonPrimitiveSerializer.encode_sub.<locals>.<dictcomp>'
               62  MAKE_FUNCTION_8          'closure'
               64  LOAD_FAST                'value'
               66  LOAD_METHOD              items
               68  CALL_METHOD_0         0  ''
               70  GET_ITER         
               72  CALL_FUNCTION_1       1  ''
               74  RETURN_VALUE     
             76_0  COME_FROM            52  '52'

 L. 277        76  LOAD_DEREF               'validator'
               78  LOAD_ATTR                _redact
               80  LOAD_METHOD              apply
               82  LOAD_FAST                'value'
               84  CALL_METHOD_1         1  ''
               86  RETURN_VALUE     
             88_0  COME_FROM            14  '14'
             88_1  COME_FROM             4  '4'

 L. 280        88  LOAD_GLOBAL              super
               90  LOAD_GLOBAL              StoneToPythonPrimitiveSerializer
               92  LOAD_FAST                'self'
               94  CALL_FUNCTION_2       2  ''
               96  LOAD_METHOD              encode_sub
               98  LOAD_DEREF               'validator'
              100  LOAD_FAST                'value'
              102  CALL_METHOD_2         2  ''
              104  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 58

        def encode_list(self, validator, value):
            validated_value = validator.validate(value)
            return [self.encode_sub(validator.item_validator, value_item) for value_item in validated_value]

        def encode_map--- This code section failed: ---

 L. 289         0  LOAD_DEREF               'validator'
                2  LOAD_METHOD              validate
                4  LOAD_FAST                'value'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'validated_value'

 L. 291        10  LOAD_CLOSURE             'self'
               12  LOAD_CLOSURE             'validator'
               14  BUILD_TUPLE_2         2 
               16  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               18  LOAD_STR                 'StoneToPythonPrimitiveSerializer.encode_map.<locals>.<dictcomp>'
               20  MAKE_FUNCTION_8          'closure'

 L. 294        22  LOAD_FAST                'validated_value'
               24  LOAD_METHOD              items
               26  CALL_METHOD_0         0  ''

 L. 291        28  GET_ITER         
               30  CALL_FUNCTION_1       1  ''
               32  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 16

        def encode_nullable(self, validator, value):
            if value is None:
                return
            return self.encode_sub(validator.validator, value)

        def encode_primitive(self, validator, value):
            if validator in self.alias_validators:
                self.alias_validators[validator](value)
            elif isinstance(validator, bv.Void):
                return
                if isinstance(validator, bv.Timestamp):
                    return _strftime(value, validator.format)
                if isinstance(validator, bv.Bytes):
                    if self.for_msgpack:
                        return value
                    return base64.b64encode(value).decode('ascii')
            else:
                if isinstance(validator, bv.Integer):
                    if isinstance(value, bool):
                        return int(value)
                return value

        def encode_struct(self, validator, value):
            d = collections.OrderedDict
            all_fields = validator.definition._all_fields_
            for extra_permission in self.caller_permissions.permissions:
                all_fields_name = '_all_{}_fields_'.format(extra_permission)
                all_fields = all_fields + getattr(validator.definition, all_fields_name, [])
            else:
                for field_name, field_validator in all_fields:
                    try:
                        field_value = getattr(value, field_name)
                    except AttributeError as exc:
                        try:
                            raise bv.ValidationError(exc.args[0])
                        finally:
                            exc = None
                            del exc

                    else:
                        presence_key = '_%s_present' % field_name
                        if field_value is not None and getattr(value, presence_key):
                            try:
                                d[field_name] = self.encode_sub(field_validator, field_value)
                            except bv.ValidationError as exc:
                                try:
                                    exc.add_parent(field_name)
                                    raise
                                finally:
                                    exc = None
                                    del exc

                        return d

        def encode_struct_tree(self, validator, value):
            if not type(value) in validator.definition._pytype_to_tag_and_subtype_:
                raise AssertionError('%r is not a serializable subtype of %r.' % (type(value), validator.definition))
            else:
                tags, subtype = validator.definition._pytype_to_tag_and_subtype_[type(value)]
                assert len(tags) == 1, tags
                if isinstance(subtype, bv.StructTree):
                    raise AssertionError('Cannot serialize type %r because it enumerates subtypes.' % subtype.definition)
                if self.old_style:
                    d = {tags[0]: self.encode_struct(subtype, value)}
                else:
                    d = collections.OrderedDict
                d['.tag'] = tags[0]
                d.update(self.encode_struct(subtype, value))
            return d

        def encode_union(self, validator, value):
            if value._tag is None:
                raise bv.ValidationError('no tag set')
            else:
                if not validator.definition._is_tag_present(value._tag, self.caller_permissions):
                    raise bv.ValidationError("caller does not have access to '{}' tag".format(value._tag))
                field_validator = validator.definition._get_val_data_type(value._tag, self.caller_permissions)
                is_none = isinstance(field_validator, bv.Void) or isinstance(field_validator, bv.Nullable) and value._value is None

                def encode_sub(sub_validator, sub_value, parent_tag):
                    try:
                        encoded_val = self.encode_sub(sub_validator, sub_value)
                    except bv.ValidationError as exc:
                        try:
                            exc.add_parent(parent_tag)
                            raise
                        finally:
                            exc = None
                            del exc

                    else:
                        return encoded_val

                if self.old_style:
                    if field_validator is None:
                        return value._tag
                    if is_none:
                        return value._tag
                    encoded_val = encode_sub(field_validator, value._value, value._tag)
                    return {value._tag: encoded_val}
                else:
                    if is_none:
                        return {'.tag': value._tag}
                    else:
                        encoded_val = encode_sub(field_validator, value._value, value._tag)
                        if isinstance(field_validator, bv.Nullable):
                            field_validator = field_validator.validator
                        if isinstance(field_validator, bv.Struct):
                            d = isinstance(field_validator, bv.StructTree) or collections.OrderedDict
                            d['.tag'] = value._tag
                            d.update(encoded_val)
                            return d
                    return collections.OrderedDict((
                     (
                      '.tag', value._tag),
                     (
                      value._tag, encoded_val)))


    class StoneToJsonSerializer(StoneToPythonPrimitiveSerializer):

        def encode(self, validator, value):
            return json.dumps(super(StoneToJsonSerializer, self).encode(validator, value))


    def json_encode(data_type, obj, caller_permissions=None, alias_validators=None, old_style=False, should_redact=False):
        """Encodes an object into JSON based on its type.

    Args:
        data_type (Validator): Validator for obj.
        obj (object): Object to be serialized.
        caller_permissions (list): The list of raw-string caller permissions with which
                to serialize.
        alias_validators (Optional[Mapping[bv.Validator, Callable[[], None]]]):
            Custom validation functions. These must raise bv.ValidationError on
            failure.

    Returns:
        str: JSON-encoded object.

    This function will also do additional validation that wasn't done by the
    objects themselves:

    1. The passed in obj may not have been validated with data_type yet.
    2. If an object that should be a Struct was assigned to a field, its
       type has been validated, but the presence of all required fields
       hasn't been.
    3. If an object that should be a Union was assigned to a field, whether
       or not a tag has been set has not been validated.
    4. A list may have passed validation initially, but been mutated since.

    Example of serializing a struct to JSON:

    struct FileRef
       path String
       rev String

    > fr = FileRef()
    > fr.path = 'a/b/c'
    > fr.rev = '1234'
    > JsonEncoder.encode(fr)
    "{'path': 'a/b/c', 'rev': '1234'}"

    Example of serializing a union to JSON:

    union UploadMode
        add
        overwrite
        update FileRef

    > um = UploadMode()
    > um.set_add()
    > JsonEncoder.encode(um)
    '"add"'
    > um.update = fr
    > JsonEncoder.encode(um)
    "{'update': {'path': 'a/b/c', 'rev': '1234'}}"
    """
        for_msgpack = False
        serializer = StoneToJsonSerializer(caller_permissions, alias_validators, for_msgpack, old_style, should_redact)
        return serializer.encode(data_type, obj)


    def json_compat_obj_encode(data_type, obj, caller_permissions=None, alias_validators=None, old_style=False, for_msgpack=False, should_redact=False):
        """Encodes an object into a JSON-compatible dict based on its type.

    Args:
        data_type (Validator): Validator for obj.
        obj (object): Object to be serialized.
        caller_permissions (list): The list of raw-string caller permissions
            with which to serialize.

    Returns:
        An object that when passed to json.dumps() will produce a string
        giving the JSON-encoded object.

    See json_encode() for additional information about validation.
    """
        serializer = StoneToPythonPrimitiveSerializer(caller_permissions, alias_validators, for_msgpack, old_style, should_redact)
        return serializer.encode(data_type, obj)


    class PythonPrimitiveToStoneDecoder(object):

        def __init__(self, caller_permissions, alias_validators, for_msgpack, old_style, strict):
            self.caller_permissions = caller_permissions if caller_permissions else CallerPermissionsDefault()
            self.alias_validators = alias_validators
            self.strict = strict
            self._old_style = old_style
            self._for_msgpack = for_msgpack

        @property
        def for_msgpack(self):
            """
        EXPERIMENTAL: A flag associated with the serializer indicating
        whether objects produced by the ``encode`` method should be
        encoded for msgpack.
        """
            return self._for_msgpack

        @property
        def old_style(self):
            """
        A flag associated with the serializer indicating whether objects
        produced by the ``encode`` method should be encoded according to
        Dropbox's old or new API styles.
        """
            return self._old_style

        def json_compat_obj_decode_helper(self, data_type, obj):
            """
        See json_compat_obj_decode() for argument descriptions.
        """
            if isinstance(data_type, bv.StructTree):
                return self.decode_struct_tree(data_type, obj)
            elif isinstance(data_type, bv.Struct):
                return self.decode_struct(data_type, obj)
                if isinstance(data_type, bv.Union):
                    if self.old_style:
                        return self.decode_union_old(data_type, obj)
                    return self.decode_union(data_type, obj)
            else:
                if isinstance(data_type, bv.List):
                    return self.decode_list(data_type, obj)
                if isinstance(data_type, bv.Map):
                    return self.decode_map(data_type, obj)
                if isinstance(data_type, bv.Nullable):
                    return self.decode_nullable(data_type, obj)
                if isinstance(data_type, bv.Primitive):
                    return self.make_stone_friendly(data_type, obj, False)
                raise AssertionError('Cannot handle type %r.' % data_type)

        def decode_struct(self, data_type, obj):
            """
        The data_type argument must be a Struct.
        See json_compat_obj_decode() for argument descriptions.
        """
            if obj is None:
                if data_type.has_default:
                    return data_type.get_default
            if not isinstance(obj, dict):
                raise bv.ValidationError('expected object, got %s' % bv.generic_type_name(obj))
            all_fields = data_type.definition._all_fields_
            for extra_permission in self.caller_permissions.permissions:
                all_extra_fields = '_all_{}_fields_'.format(extra_permission)
                all_fields = all_fields + getattr(data_type.definition, all_extra_fields, [])
            else:
                if self.strict:
                    all_field_names = data_type.definition._all_field_names_
                    for extra_permission in self.caller_permissions.permissions:
                        all_extra_field_names = '_all_{}_field_names_'.format(extra_permission)
                        all_field_names = all_field_names.union(getattr(data_type.definition, all_extra_field_names, {}))
                    else:
                        for key in obj:
                            if key not in all_field_names:
                                raise (key.startswith('.tag') or bv.ValidationError)("unknown field '%s'" % key)

                ins = data_type.definition
                self.decode_struct_fields(ins, all_fields, obj)
                data_type.validate_fields_only_with_permissions(ins, self.caller_permissions)
                return ins

        def decode_struct_fields(self, ins, fields, obj):
            """
        Args:
            ins: An instance of the class representing the data type being decoded.
                The object will have its fields set.
            fields: A tuple of (field_name: str, field_validator: Validator)
            obj (dict): JSON-compatible dict that is being decoded.
            strict (bool): See :func:`json_compat_obj_decode`.
        Returns:
            None: `ins` has its fields set based on the contents of `obj`.
        """
            for name, field_data_type in fields:
                if name in obj:
                    try:
                        v = self.json_compat_obj_decode_helper(field_data_type, obj[name])
                        setattr(ins, name, v)
                    except bv.ValidationError as e:
                        try:
                            e.add_parent(name)
                            raise
                        finally:
                            e = None
                            del e

                elif field_data_type.has_default:
                    setattr(ins, name, field_data_type.get_default)

        def decode_union(self, data_type, obj):
            """
        The data_type argument must be a Union.
        See json_compat_obj_decode() for argument descriptions.
        """
            val = None
            if isinstance(obj, six.string_types):
                tag = obj
                if data_type.definition._is_tag_present(tag, self.caller_permissions):
                    val_data_type = data_type.definition._get_val_data_type(tag, self.caller_permissions)
                    if not isinstance(val_data_type, (bv.Void, bv.Nullable)):
                        raise bv.ValidationError("expected object for '%s', got symbol" % tag)
                    if tag == data_type.definition._catch_all:
                        raise bv.ValidationError("unexpected use of the catch-all tag '%s'" % tag)
                    elif not self.strict:
                        if data_type.definition._catch_all:
                            tag = data_type.definition._catch_all
                else:
                    raise bv.ValidationError("unknown tag '%s'" % tag)
            else:
                if isinstance(obj, dict):
                    tag, val = self.decode_union_dict(data_type, obj)
                else:
                    raise bv.ValidationError('expected string or object, got %s' % bv.generic_type_name(obj))
            return data_type.definition(six.ensure_str(tag), val)

        def decode_union_dict(self, data_type, obj):
            if '.tag' not in obj:
                raise bv.ValidationError("missing '.tag' key")
            else:
                tag = obj['.tag']
                if not isinstance(tag, six.string_types):
                    raise bv.ValidationError('tag must be string, got %s' % bv.generic_type_name(tag))
                if not data_type.definition._is_tag_present(tag, self.caller_permissions):
                    if not self.strict:
                        if data_type.definition._catch_all:
                            return (
                             data_type.definition._catch_all, None)
                    raise bv.ValidationError("unknown tag '%s'" % tag)
                if tag == data_type.definition._catch_all:
                    raise bv.ValidationError("unexpected use of the catch-all tag '%s'" % tag)
                val_data_type = data_type.definition._get_val_data_type(tag, self.caller_permissions)
                if isinstance(val_data_type, bv.Nullable):
                    val_data_type = val_data_type.validator
                    nullable = True
                else:
                    nullable = False
            if isinstance(val_data_type, bv.Void):
                if self.strict:
                    if tag in obj:
                        if obj[tag] is not None:
                            raise bv.ValidationError('expected null, got %s' % bv.generic_type_name(obj[tag]))
                    for key in obj:
                        if key != tag:
                            if key != '.tag':
                                raise bv.ValidationError("unexpected key '%s'" % key)
                            else:
                                val = None

                else:
                    pass
            if isinstance(val_data_type, (
             bv.Primitive, bv.List, bv.StructTree, bv.Union, bv.Map)):
                if tag in obj:
                    raw_val = obj[tag]
                    try:
                        val = self.json_compat_obj_decode_helper(val_data_type, raw_val)
                    except bv.ValidationError as e:
                        try:
                            e.add_parent(tag)
                            raise
                        finally:
                            e = None
                            del e

                else:
                    if nullable:
                        val = None
                    else:
                        raise bv.ValidationError("missing '%s' key" % tag)
                for key in obj:
                    if key != tag and key != '.tag':
                        raise bv.ValidationError("unexpected key '%s'" % key)

            else:
                if isinstance(val_data_type, bv.Struct):
                    if nullable and len(obj) == 1:
                        val = None
                    else:
                        raw_val = obj
                    try:
                        val = self.json_compat_obj_decode_helper(val_data_type, raw_val)
                    except bv.ValidationError as e:
                        try:
                            e.add_parent(tag)
                            raise
                        finally:
                            e = None
                            del e

                else:
                    assert False, type(val_data_type)
                    return (tag, val)

        def decode_union_old--- This code section failed: ---

 L. 742         0  LOAD_CONST               None
                2  STORE_FAST               'val'

 L. 743         4  LOAD_GLOBAL              isinstance
                6  LOAD_FAST                'obj'
                8  LOAD_GLOBAL              six
               10  LOAD_ATTR                string_types
               12  CALL_FUNCTION_2       2  ''
               14  POP_JUMP_IF_FALSE   128  'to 128'

 L. 745        16  LOAD_FAST                'obj'
               18  STORE_FAST               'tag'

 L. 746        20  LOAD_FAST                'data_type'
               22  LOAD_ATTR                definition
               24  LOAD_METHOD              _is_tag_present
               26  LOAD_FAST                'tag'
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                caller_permissions
               32  CALL_METHOD_2         2  ''
               34  POP_JUMP_IF_FALSE    86  'to 86'

 L. 747        36  LOAD_FAST                'data_type'
               38  LOAD_ATTR                definition
               40  LOAD_METHOD              _get_val_data_type
               42  LOAD_FAST                'tag'

 L. 748        44  LOAD_FAST                'self'
               46  LOAD_ATTR                caller_permissions

 L. 747        48  CALL_METHOD_2         2  ''
               50  STORE_FAST               'val_data_type'

 L. 749        52  LOAD_GLOBAL              isinstance
               54  LOAD_FAST                'val_data_type'
               56  LOAD_GLOBAL              bv
               58  LOAD_ATTR                Void
               60  LOAD_GLOBAL              bv
               62  LOAD_ATTR                Nullable
               64  BUILD_TUPLE_2         2 
               66  CALL_FUNCTION_2       2  ''
               68  POP_JUMP_IF_TRUE    124  'to 124'

 L. 750        70  LOAD_GLOBAL              bv
               72  LOAD_METHOD              ValidationError

 L. 751        74  LOAD_STR                 "expected object for '%s', got symbol"
               76  LOAD_FAST                'tag'
               78  BINARY_MODULO    

 L. 750        80  CALL_METHOD_1         1  ''
               82  RAISE_VARARGS_1       1  'exception instance'
               84  JUMP_FORWARD        444  'to 444'
             86_0  COME_FROM            34  '34'

 L. 753        86  LOAD_FAST                'self'
               88  LOAD_ATTR                strict
               90  POP_JUMP_IF_TRUE    110  'to 110'
               92  LOAD_FAST                'data_type'
               94  LOAD_ATTR                definition
               96  LOAD_ATTR                _catch_all
               98  POP_JUMP_IF_FALSE   110  'to 110'

 L. 754       100  LOAD_FAST                'data_type'
              102  LOAD_ATTR                definition
              104  LOAD_ATTR                _catch_all
              106  STORE_FAST               'tag'
              108  JUMP_FORWARD        444  'to 444'
            110_0  COME_FROM            98  '98'
            110_1  COME_FROM            90  '90'

 L. 756       110  LOAD_GLOBAL              bv
              112  LOAD_METHOD              ValidationError
              114  LOAD_STR                 "unknown tag '%s'"
              116  LOAD_FAST                'tag'
              118  BINARY_MODULO    
              120  CALL_METHOD_1         1  ''
              122  RAISE_VARARGS_1       1  'exception instance'
            124_0  COME_FROM            68  '68'
          124_126  JUMP_FORWARD        444  'to 444'
            128_0  COME_FROM            14  '14'

 L. 757       128  LOAD_GLOBAL              isinstance
              130  LOAD_FAST                'obj'
              132  LOAD_GLOBAL              dict
              134  CALL_FUNCTION_2       2  ''
          136_138  POP_JUMP_IF_FALSE   424  'to 424'

 L. 759       140  LOAD_GLOBAL              len
              142  LOAD_FAST                'obj'
              144  CALL_FUNCTION_1       1  ''
              146  LOAD_CONST               1
              148  COMPARE_OP               !=
              150  POP_JUMP_IF_FALSE   170  'to 170'

 L. 760       152  LOAD_GLOBAL              bv
              154  LOAD_METHOD              ValidationError
              156  LOAD_STR                 'expected 1 key, got %s'
              158  LOAD_GLOBAL              len
              160  LOAD_FAST                'obj'
              162  CALL_FUNCTION_1       1  ''
              164  BINARY_MODULO    
              166  CALL_METHOD_1         1  ''
              168  RAISE_VARARGS_1       1  'exception instance'
            170_0  COME_FROM           150  '150'

 L. 761       170  LOAD_GLOBAL              list
              172  LOAD_FAST                'obj'
              174  CALL_FUNCTION_1       1  ''
              176  LOAD_CONST               0
              178  BINARY_SUBSCR    
              180  STORE_FAST               'tag'

 L. 762       182  LOAD_FAST                'obj'
              184  LOAD_FAST                'tag'
              186  BINARY_SUBSCR    
              188  STORE_FAST               'raw_val'

 L. 763       190  LOAD_FAST                'data_type'
              192  LOAD_ATTR                definition
              194  LOAD_METHOD              _is_tag_present
              196  LOAD_FAST                'tag'
              198  LOAD_FAST                'self'
              200  LOAD_ATTR                caller_permissions
              202  CALL_METHOD_2         2  ''
          204_206  POP_JUMP_IF_FALSE   380  'to 380'

 L. 764       208  LOAD_FAST                'data_type'
              210  LOAD_ATTR                definition
              212  LOAD_METHOD              _get_val_data_type
              214  LOAD_FAST                'tag'

 L. 765       216  LOAD_FAST                'self'
              218  LOAD_ATTR                caller_permissions

 L. 764       220  CALL_METHOD_2         2  ''
              222  STORE_FAST               'val_data_type'

 L. 766       224  LOAD_GLOBAL              isinstance
              226  LOAD_FAST                'val_data_type'
              228  LOAD_GLOBAL              bv
              230  LOAD_ATTR                Nullable
              232  CALL_FUNCTION_2       2  ''
              234  POP_JUMP_IF_FALSE   250  'to 250'
              236  LOAD_FAST                'raw_val'
              238  LOAD_CONST               None
              240  COMPARE_OP               is
              242  POP_JUMP_IF_FALSE   250  'to 250'

 L. 767       244  LOAD_CONST               None
              246  STORE_FAST               'val'
              248  JUMP_FORWARD        378  'to 378'
            250_0  COME_FROM           242  '242'
            250_1  COME_FROM           234  '234'

 L. 768       250  LOAD_GLOBAL              isinstance
              252  LOAD_FAST                'val_data_type'
              254  LOAD_GLOBAL              bv
              256  LOAD_ATTR                Void
              258  CALL_FUNCTION_2       2  ''
          260_262  POP_JUMP_IF_FALSE   310  'to 310'

 L. 769       264  LOAD_FAST                'raw_val'
              266  LOAD_CONST               None
              268  COMPARE_OP               is
          270_272  POP_JUMP_IF_TRUE    282  'to 282'
              274  LOAD_FAST                'self'
              276  LOAD_ATTR                strict
          278_280  POP_JUMP_IF_TRUE    288  'to 288'
            282_0  COME_FROM           270  '270'

 L. 774       282  LOAD_CONST               None
              284  STORE_FAST               'val'
              286  JUMP_FORWARD        308  'to 308'
            288_0  COME_FROM           278  '278'

 L. 776       288  LOAD_GLOBAL              bv
              290  LOAD_METHOD              ValidationError
              292  LOAD_STR                 'expected null, got %s'

 L. 777       294  LOAD_GLOBAL              bv
              296  LOAD_METHOD              generic_type_name
              298  LOAD_FAST                'raw_val'
              300  CALL_METHOD_1         1  ''

 L. 776       302  BINARY_MODULO    
              304  CALL_METHOD_1         1  ''
              306  RAISE_VARARGS_1       1  'exception instance'
            308_0  COME_FROM           286  '286'
              308  JUMP_FORWARD        378  'to 378'
            310_0  COME_FROM           260  '260'

 L. 779       310  SETUP_FINALLY       328  'to 328'

 L. 780       312  LOAD_FAST                'self'
              314  LOAD_METHOD              json_compat_obj_decode_helper
              316  LOAD_FAST                'val_data_type'
              318  LOAD_FAST                'raw_val'
              320  CALL_METHOD_2         2  ''
              322  STORE_FAST               'val'
              324  POP_BLOCK        
              326  JUMP_FORWARD        378  'to 378'
            328_0  COME_FROM_FINALLY   310  '310'

 L. 781       328  DUP_TOP          
              330  LOAD_GLOBAL              bv
              332  LOAD_ATTR                ValidationError
              334  COMPARE_OP               exception-match
          336_338  POP_JUMP_IF_FALSE   376  'to 376'
              340  POP_TOP          
              342  STORE_FAST               'e'
              344  POP_TOP          
              346  SETUP_FINALLY       364  'to 364'

 L. 782       348  LOAD_FAST                'e'
              350  LOAD_METHOD              add_parent
              352  LOAD_FAST                'tag'
              354  CALL_METHOD_1         1  ''
              356  POP_TOP          

 L. 783       358  RAISE_VARARGS_0       0  'reraise'
              360  POP_BLOCK        
              362  BEGIN_FINALLY    
            364_0  COME_FROM_FINALLY   346  '346'
              364  LOAD_CONST               None
              366  STORE_FAST               'e'
              368  DELETE_FAST              'e'
              370  END_FINALLY      
              372  POP_EXCEPT       
              374  JUMP_FORWARD        378  'to 378'
            376_0  COME_FROM           336  '336'
              376  END_FINALLY      
            378_0  COME_FROM           374  '374'
            378_1  COME_FROM           326  '326'
            378_2  COME_FROM           308  '308'
            378_3  COME_FROM           248  '248'
              378  JUMP_FORWARD        422  'to 422'
            380_0  COME_FROM           204  '204'

 L. 785       380  LOAD_FAST                'self'
              382  LOAD_ATTR                strict
          384_386  POP_JUMP_IF_TRUE    408  'to 408'
              388  LOAD_FAST                'data_type'
              390  LOAD_ATTR                definition
              392  LOAD_ATTR                _catch_all
          394_396  POP_JUMP_IF_FALSE   408  'to 408'

 L. 786       398  LOAD_FAST                'data_type'
              400  LOAD_ATTR                definition
            402_0  COME_FROM            84  '84'
              402  LOAD_ATTR                _catch_all
              404  STORE_FAST               'tag'
              406  JUMP_FORWARD        422  'to 422'
            408_0  COME_FROM           394  '394'
            408_1  COME_FROM           384  '384'

 L. 788       408  LOAD_GLOBAL              bv
              410  LOAD_METHOD              ValidationError
              412  LOAD_STR                 "unknown tag '%s'"
              414  LOAD_FAST                'tag'
              416  BINARY_MODULO    
              418  CALL_METHOD_1         1  ''
              420  RAISE_VARARGS_1       1  'exception instance'
            422_0  COME_FROM           406  '406'
            422_1  COME_FROM           378  '378'
              422  JUMP_FORWARD        444  'to 444'
            424_0  COME_FROM           136  '136'

 L. 790       424  LOAD_GLOBAL              bv
            426_0  COME_FROM           108  '108'
              426  LOAD_METHOD              ValidationError
              428  LOAD_STR                 'expected string or object, got %s'

 L. 791       430  LOAD_GLOBAL              bv
              432  LOAD_METHOD              generic_type_name
              434  LOAD_FAST                'obj'
              436  CALL_METHOD_1         1  ''

 L. 790       438  BINARY_MODULO    
              440  CALL_METHOD_1         1  ''
              442  RAISE_VARARGS_1       1  'exception instance'
            444_0  COME_FROM           422  '422'
            444_1  COME_FROM           124  '124'

 L. 792       444  LOAD_FAST                'data_type'
              446  LOAD_METHOD              definition
              448  LOAD_GLOBAL              six
              450  LOAD_METHOD              ensure_str
              452  LOAD_FAST                'tag'
              454  CALL_METHOD_1         1  ''
              456  LOAD_FAST                'val'
              458  CALL_METHOD_2         2  ''
              460  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_ATTR' instruction at offset 402

        def decode_struct_tree(self, data_type, obj):
            """
        The data_type argument must be a StructTree.
        See json_compat_obj_decode() for argument descriptions.
        """
            subtype = self.determine_struct_tree_subtype(data_type, obj)
            return self.decode_struct(subtype, obj)

        def determine_struct_tree_subtype(self, data_type, obj):
            """
        Searches through the JSON-object-compatible dict using the data type
        definition to determine which of the enumerated subtypes `obj` is.
        """
            if '.tag' not in obj:
                raise bv.ValidationError("missing '.tag' key")
            else:
                if not isinstance(obj['.tag'], six.string_types):
                    raise bv.ValidationError(('expected string, got %s' % bv.generic_type_name(obj['.tag'])),
                      parent='.tag')
                full_tags_tuple = (
                 obj['.tag'],)
                if full_tags_tuple in data_type.definition._tag_to_subtype_:
                    subtype = data_type.definition._tag_to_subtype_[full_tags_tuple]
                    if isinstance(subtype, bv.StructTree):
                        raise bv.ValidationError("tag '%s' refers to non-leaf subtype" % '.'.join(full_tags_tuple))
                    return subtype
                    if self.strict:
                        raise bv.ValidationError("unknown subtype '%s'" % '.'.join(full_tags_tuple))
                elif data_type.definition._is_catch_all_:
                    return data_type
                raise bv.ValidationError("unknown subtype '%s' and '%s' is not a catch-all" % (
                 '.'.join(full_tags_tuple), data_type.definition.__name__))

        def decode_list(self, data_type, obj):
            """
        The data_type argument must be a List.
        See json_compat_obj_decode() for argument descriptions.
        """
            if not isinstance(obj, list):
                raise bv.ValidationError('expected list, got %s' % bv.generic_type_name(obj))
            return [self.json_compat_obj_decode_helper(data_type.item_validator, item) for item in obj]

        def decode_map--- This code section failed: ---

 L. 854         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'obj'
                4  LOAD_GLOBAL              dict
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     30  'to 30'

 L. 855        10  LOAD_GLOBAL              bv
               12  LOAD_METHOD              ValidationError

 L. 856        14  LOAD_STR                 'expected dict, got %s'
               16  LOAD_GLOBAL              bv
               18  LOAD_METHOD              generic_type_name
               20  LOAD_FAST                'obj'
               22  CALL_METHOD_1         1  ''
               24  BINARY_MODULO    

 L. 855        26  CALL_METHOD_1         1  ''
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM             8  '8'

 L. 857        30  LOAD_CLOSURE             'data_type'
               32  LOAD_CLOSURE             'self'
               34  BUILD_TUPLE_2         2 
               36  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               38  LOAD_STR                 'PythonPrimitiveToStoneDecoder.decode_map.<locals>.<dictcomp>'
               40  MAKE_FUNCTION_8          'closure'

 L. 860        42  LOAD_FAST                'obj'
               44  LOAD_METHOD              items
               46  CALL_METHOD_0         0  ''

 L. 857        48  GET_ITER         
               50  CALL_FUNCTION_1       1  ''
               52  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 36

        def decode_nullable(self, data_type, obj):
            """
        The data_type argument must be a Nullable.
        See json_compat_obj_decode() for argument descriptions.
        """
            if obj is not None:
                return self.json_compat_obj_decode_helper(data_type.validator, obj)
            return

        def make_stone_friendly(self, data_type, val, validate):
            """
        Convert a Python object to a type that will pass validation by its
        validator.
        Validation by ``alias_validators`` is performed even if ``validate`` is
        false.
        """
            if isinstance(data_type, bv.Timestamp):
                try:
                    ret = datetime.datetime.strptime(val, data_type.format)
                except (TypeError, ValueError) as e:
                    try:
                        raise bv.ValidationError(e.args[0])
                    finally:
                        e = None
                        del e

            else:
                if isinstance(data_type, bv.Bytes):
                    if self.for_msgpack:
                        if isinstance(val, six.text_type):
                            ret = val.encode('utf-8')
                        else:
                            ret = val
                    else:
                        try:
                            ret = base64.b64decode(val)
                        except (TypeError, binascii.Error):
                            raise bv.ValidationError('invalid base64-encoded bytes')

                else:
                    if isinstance(data_type, bv.Void):
                        if self.strict:
                            if val is not None:
                                raise bv.ValidationError('expected null, got value')
                        else:
                            return
                            if validate:
                                if self.caller_permissions.permissions:
                                    data_type.validate_with_permissions(val, self.caller_permissions)
                                else:
                                    data_type.validate(val)
                        ret = val
                    elif self.alias_validators is not None and data_type in self.alias_validators:
                        self.alias_validators[data_type](ret)
                    return ret


    def json_decode(data_type, serialized_obj, caller_permissions=None, alias_validators=None, strict=True, old_style=False):
        """Performs the reverse operation of json_encode.

    Args:
        data_type (Validator): Validator for serialized_obj.
        serialized_obj (str): The JSON string to deserialize.
        caller_permissions (list): The list of raw-string caller permissions
            with which to serialize.
        alias_validators (Optional[Mapping[bv.Validator, Callable[[], None]]]):
            Custom validation functions. These must raise bv.ValidationError on
            failure.
        strict (bool): If strict, then unknown struct fields will raise an
            error, and unknown union variants will raise an error even if a
            catch all field is specified. strict should only be used by a
            recipient of serialized JSON if it's guaranteed that its Stone
            specs are at least as recent as the senders it receives messages
            from.

    Returns:
        The returned object depends on the input data_type.
            - Boolean -> bool
            - Bytes -> bytes
            - Float -> float
            - Integer -> long
            - List -> list
            - Map -> dict
            - Nullable -> None or its wrapped type.
            - String -> unicode (PY2) or str (PY3)
            - Struct -> An instance of its definition attribute.
            - Timestamp -> datetime.datetime
            - Union -> An instance of its definition attribute.
    """
        try:
            deserialized_obj = json.loads(serialized_obj)
        except ValueError:
            raise bv.ValidationError('could not decode input as JSON')
        else:
            return json_compat_obj_decode(data_type,
              deserialized_obj, caller_permissions=caller_permissions, alias_validators=alias_validators,
              strict=strict,
              old_style=old_style)


    def json_compat_obj_decode(data_type, obj, caller_permissions=None, alias_validators=None, strict=True, old_style=False, for_msgpack=False):
        """
    Decodes a JSON-compatible object based on its data type into a
    representative Python object.

    Args:
        data_type (Validator): Validator for serialized_obj.
        obj: The JSON-compatible object to decode based on data_type.
        caller_permissions (list): The list of raw-string caller permissions
            with which to serialize.
        strict (bool): If strict, then unknown struct fields will raise an
            error, and unknown union variants will raise an error even if a
            catch all field is specified. See json_decode() for more.

    Returns:
        See json_decode().
    """
        decoder = PythonPrimitiveToStoneDecoder(caller_permissions, alias_validators, for_msgpack, old_style, strict)
        if isinstance(data_type, bv.Primitive):
            return decoder.make_stone_friendly(data_type, obj, True)
        return decoder.json_compat_obj_decode_helper(data_type, obj)


    _ILLEGAL_S = re.compile('((^|[^%])(%%)*%s)')

    def _findall(text, substr):
        sites = []
        i = 0
        while True:
            j = text.find(substr, i)
            if j == -1:
                break
            sites.append(j)
            i = j + 1

        return sites


    def _strftime--- This code section failed: ---

 L.1010         0  SETUP_FINALLY        14  'to 14'

 L.1011         2  LOAD_FAST                'dt'
                4  LOAD_METHOD              strftime
                6  LOAD_FAST                'fmt'
                8  CALL_METHOD_1         1  ''
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L.1012        14  DUP_TOP          
               16  LOAD_GLOBAL              ValueError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    50  'to 50'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L.1013        28  LOAD_GLOBAL              six
               30  LOAD_ATTR                PY2
               32  POP_JUMP_IF_FALSE    44  'to 44'
               34  LOAD_FAST                'dt'
               36  LOAD_ATTR                year
               38  LOAD_CONST               1900
               40  COMPARE_OP               >
               42  POP_JUMP_IF_FALSE    46  'to 46'
             44_0  COME_FROM            32  '32'

 L.1014        44  RAISE_VARARGS_0       0  'reraise'
             46_0  COME_FROM            42  '42'
               46  POP_EXCEPT       
               48  JUMP_FORWARD         52  'to 52'
             50_0  COME_FROM            20  '20'
               50  END_FINALLY      
             52_0  COME_FROM            48  '48'

 L.1016        52  LOAD_GLOBAL              _ILLEGAL_S
               54  LOAD_METHOD              search
               56  LOAD_FAST                'fmt'
               58  CALL_METHOD_1         1  ''
               60  POP_JUMP_IF_FALSE    70  'to 70'

 L.1017        62  LOAD_GLOBAL              TypeError
               64  LOAD_STR                 'This strftime implementation does not handle %s'
               66  CALL_FUNCTION_1       1  ''
               68  RAISE_VARARGS_1       1  'exception instance'
             70_0  COME_FROM            60  '60'

 L.1019        70  LOAD_FAST                'dt'
               72  LOAD_ATTR                year
               74  STORE_FAST               'year'

 L.1023        76  LOAD_CONST               2000
               78  LOAD_FAST                'year'
               80  BINARY_SUBTRACT  
               82  STORE_FAST               'delta'

 L.1024        84  LOAD_CONST               6
               86  LOAD_FAST                'delta'
               88  LOAD_CONST               100
               90  BINARY_FLOOR_DIVIDE
               92  LOAD_FAST                'delta'
               94  LOAD_CONST               400
               96  BINARY_FLOOR_DIVIDE
               98  BINARY_ADD       
              100  BINARY_MULTIPLY  
              102  STORE_FAST               'off'

 L.1025       104  LOAD_FAST                'year'
              106  LOAD_FAST                'off'
              108  BINARY_ADD       
              110  STORE_FAST               'year'

 L.1028       112  LOAD_FAST                'year'
              114  LOAD_CONST               2000
              116  LOAD_FAST                'year'
              118  BINARY_SUBTRACT  
              120  LOAD_CONST               28
              122  BINARY_FLOOR_DIVIDE
              124  LOAD_CONST               28
              126  BINARY_MULTIPLY  
              128  BINARY_ADD       
              130  STORE_FAST               'year'

 L.1029       132  LOAD_FAST                'dt'
              134  LOAD_METHOD              timetuple
              136  CALL_METHOD_0         0  ''
              138  STORE_FAST               'timetuple'

 L.1030       140  LOAD_GLOBAL              time
              142  LOAD_METHOD              strftime
              144  LOAD_FAST                'fmt'
              146  LOAD_FAST                'year'
              148  BUILD_TUPLE_1         1 
              150  LOAD_FAST                'timetuple'
              152  LOAD_CONST               1
              154  LOAD_CONST               None
              156  BUILD_SLICE_2         2 
              158  BINARY_SUBSCR    
              160  BINARY_ADD       
              162  CALL_METHOD_2         2  ''
              164  STORE_FAST               's1'

 L.1031       166  LOAD_GLOBAL              _findall
              168  LOAD_FAST                's1'
              170  LOAD_GLOBAL              str
              172  LOAD_FAST                'year'
              174  CALL_FUNCTION_1       1  ''
              176  CALL_FUNCTION_2       2  ''
              178  STORE_FAST               'sites1'

 L.1033       180  LOAD_GLOBAL              time
              182  LOAD_METHOD              strftime
              184  LOAD_FAST                'fmt'
              186  LOAD_FAST                'year'
              188  LOAD_CONST               28
              190  BINARY_ADD       
              192  BUILD_TUPLE_1         1 
              194  LOAD_FAST                'timetuple'
              196  LOAD_CONST               1
              198  LOAD_CONST               None
              200  BUILD_SLICE_2         2 
              202  BINARY_SUBSCR    
              204  BINARY_ADD       
              206  CALL_METHOD_2         2  ''
              208  STORE_FAST               's2'

 L.1034       210  LOAD_GLOBAL              _findall
              212  LOAD_FAST                's2'
              214  LOAD_GLOBAL              str
              216  LOAD_FAST                'year'
              218  LOAD_CONST               28
              220  BINARY_ADD       
              222  CALL_FUNCTION_1       1  ''
              224  CALL_FUNCTION_2       2  ''
              226  STORE_FAST               'sites2'

 L.1036       228  BUILD_LIST_0          0 
              230  STORE_FAST               'sites'

 L.1038       232  LOAD_FAST                'sites1'
              234  GET_ITER         
            236_0  COME_FROM           246  '246'
              236  FOR_ITER            260  'to 260'
              238  STORE_FAST               'site'

 L.1039       240  LOAD_FAST                'site'
              242  LOAD_FAST                'sites2'
              244  COMPARE_OP               in
              246  POP_JUMP_IF_FALSE   236  'to 236'

 L.1040       248  LOAD_FAST                'sites'
              250  LOAD_METHOD              append
              252  LOAD_FAST                'site'
              254  CALL_METHOD_1         1  ''
              256  POP_TOP          
              258  JUMP_BACK           236  'to 236'

 L.1042       260  LOAD_FAST                's1'
              262  STORE_FAST               's'

 L.1043       264  LOAD_STR                 '%4d'
              266  LOAD_FAST                'dt'
              268  LOAD_ATTR                year
              270  BUILD_TUPLE_1         1 
              272  BINARY_MODULO    
              274  STORE_FAST               'syear'

 L.1045       276  LOAD_FAST                'sites'
              278  GET_ITER         
              280  FOR_ITER            320  'to 320'
              282  STORE_FAST               'site'

 L.1046       284  LOAD_FAST                's'
              286  LOAD_CONST               None
              288  LOAD_FAST                'site'
              290  BUILD_SLICE_2         2 
              292  BINARY_SUBSCR    
              294  LOAD_FAST                'syear'
              296  BINARY_ADD       
              298  LOAD_FAST                's'
              300  LOAD_FAST                'site'
              302  LOAD_CONST               4
              304  BINARY_ADD       
              306  LOAD_CONST               None
              308  BUILD_SLICE_2         2 
              310  BINARY_SUBSCR    
              312  BINARY_ADD       
              314  STORE_FAST               's'
          316_318  JUMP_BACK           280  'to 280'

 L.1048       320  LOAD_FAST                's'
              322  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 24


    try:
        import msgpack
    except ImportError:
        pass
    else:
        msgpack_compat_obj_encode = functools.partial(json_compat_obj_encode, for_msgpack=True)

        def msgpack_encode(data_type, obj):
            return msgpack.dumps((msgpack_compat_obj_encode(data_type, obj)),
              encoding='utf-8')


        msgpack_compat_obj_decode = functools.partial(json_compat_obj_decode, for_msgpack=True)

        def msgpack_decode(data_type, serialized_obj, alias_validators=None, strict=True):
            deserialized_obj = msgpack.loads(serialized_obj,
              encoding='utf-8', unicode_errors='ignore')
            return msgpack_compat_obj_decode(data_type, deserialized_obj, alias_validators, strict)