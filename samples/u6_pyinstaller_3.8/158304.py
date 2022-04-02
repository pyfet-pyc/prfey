# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: dropbox\stone_base.py
"""
Helpers for representing Stone data types in Python.

This module should be dropped into a project that requires the use of Stone. In
the future, this could be imported from a pre-installed Python package, rather
than being added to a project.
"""
from __future__ import absolute_import, unicode_literals
import functools
try:
    from . import stone_validators as bv
except (ImportError, SystemError, ValueError):
    import stone_validators as bv
else:
    _MYPY = False
    if _MYPY:
        import typing

    class AnnotationType(object):
        pass


    if _MYPY:
        T = typing.TypeVar('T', bound=AnnotationType)
        U = typing.TypeVar('U')

    class Struct(object):
        _all_field_names_ = set()

        def __eq__(self, other):
            if not isinstance(other, Struct):
                return False
            elif self._all_field_names_ != other._all_field_names_:
                return False
            else:
                return isinstance(other, self.__class__) or isinstance(self, other.__class__) or False
            for field_name in self._all_field_names_:
                if getattr(self, field_name) != getattr(other, field_name):
                    return False
                return True

        def __ne__(self, other):
            return not self == other

        def _process_custom_annotations(self, annotation_type, field_path, processor):
            pass


    class Union(object):
        __slots__ = [
         '_tag', '_value']
        _tagmap = {}
        _permissioned_tagmaps = set()

        def __init__(self, tag, value=None):
            validator = None
            tagmap_names = ['_{}_tagmap'.format(map_name) for map_name in self._permissioned_tagmaps]
            for tagmap_name in ['_tagmap'] + tagmap_names:
                if tag in getattr(self, tagmap_name):
                    validator = getattr(self, tagmap_name)[tag]
            else:
                if not validator is not None:
                    raise AssertionError('Invalid tag %r.' % tag)
                elif isinstance(validator, bv.Void) and not value is None:
                    raise AssertionError('Void type union member must have None value.')
                else:
                    if isinstance(validator, (bv.Struct, bv.Union)):
                        validator.validate_type_only(value)
                    else:
                        validator.validate(value)
                self._tag = tag
                self._value = value

        def __eq__--- This code section failed: ---

 L.  89         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'other'
                4  LOAD_GLOBAL              Union
                6  CALL_FUNCTION_2       2  ''
                8  JUMP_IF_FALSE_OR_POP    56  'to 56'

 L.  90        10  LOAD_GLOBAL              isinstance
               12  LOAD_FAST                'self'
               14  LOAD_FAST                'other'
               16  LOAD_ATTR                __class__
               18  CALL_FUNCTION_2       2  ''
               20  POP_JUMP_IF_TRUE     34  'to 34'
               22  LOAD_GLOBAL              isinstance
               24  LOAD_FAST                'other'
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                __class__
               30  CALL_FUNCTION_2       2  ''

 L.  89        32  JUMP_IF_FALSE_OR_POP    56  'to 56'
             34_0  COME_FROM            20  '20'

 L.  91        34  LOAD_FAST                'self'
               36  LOAD_ATTR                _tag
               38  LOAD_FAST                'other'
               40  LOAD_ATTR                _tag
               42  COMPARE_OP               ==

 L.  89        44  JUMP_IF_FALSE_OR_POP    56  'to 56'

 L.  91        46  LOAD_FAST                'self'
               48  LOAD_ATTR                _value
               50  LOAD_FAST                'other'
               52  LOAD_ATTR                _value
               54  COMPARE_OP               ==
             56_0  COME_FROM            44  '44'
             56_1  COME_FROM            32  '32'
             56_2  COME_FROM             8  '8'

 L.  88        56  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 56_2

        def __ne__(self, other):
            return not self == other

        def __hash__(self):
            return hash((self._tag, self._value))

        def _process_custom_annotations(self, annotation_type, field_path, processor):
            pass

        @classmethod
        def _is_tag_present(cls, tag, caller_permissions):
            assert tag is not None, 'tag value should not be None'
            if tag in cls._tagmap:
                return True
            for extra_permission in caller_permissions.permissions:
                tagmap_name = '_{}_tagmap'.format(extra_permission)
                if hasattr(cls, tagmap_name) and tag in getattr(cls, tagmap_name):
                    return True
                return False

        @classmethod
        def _get_val_data_type(cls, tag, caller_permissions):
            assert tag is not None, 'tag value should not be None'
            for extra_permission in caller_permissions.permissions:
                tagmap_name = '_{}_tagmap'.format(extra_permission)
                if hasattr(cls, tagmap_name) and tag in getattr(cls, tagmap_name):
                    return getattr(cls, tagmap_name)[tag]
                return cls._tagmap[tag]


    class Route(object):

        def __init__(self, name, version, deprecated, arg_type, result_type, error_type, attrs):
            self.name = name
            self.version = version
            self.deprecated = deprecated
            self.arg_type = arg_type
            self.result_type = result_type
            self.error_type = error_type
            assert isinstance(attrs, dict), 'Expected dict, got %r' % attrs
            self.attrs = attrs

        def __repr__(self):
            return 'Route({!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r})'.format(self.name, self.version, self.deprecated, self.arg_type, self.result_type, self.error_type, self.attrs)


    partially_apply = functools.partial

    def make_struct_annotation_processor(annotation_type, processor):

        def g(field_path, struct):
            if struct is None:
                return struct
            struct._process_custom_annotations(annotation_type, field_path, processor)
            return struct

        return g


    def make_list_annotation_processor(processor):

        def g(field_path, list_):
            if list_ is None:
                return list_
            return [processor('{}[{}]'.format(field_path, idx), x) for idx, x in enumerate(list_)]

        return g


    def make_map_value_annotation_processor(processor):

        def g--- This code section failed: ---

 L. 173         0  LOAD_FAST                'map_'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 174         8  LOAD_FAST                'map_'
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L. 175        12  LOAD_CLOSURE             'field_path'
               14  LOAD_CLOSURE             'processor'
               16  BUILD_TUPLE_2         2 
               18  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               20  LOAD_STR                 'make_map_value_annotation_processor.<locals>.g.<locals>.<dictcomp>'
               22  MAKE_FUNCTION_8          'closure'
               24  LOAD_FAST                'map_'
               26  LOAD_METHOD              items
               28  CALL_METHOD_0         0  ''
               30  GET_ITER         
               32  CALL_FUNCTION_1       1  ''
               34  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 18

        return g