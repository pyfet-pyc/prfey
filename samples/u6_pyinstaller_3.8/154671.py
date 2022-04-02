# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\openpyxl\descriptors\serialisable.py
from copy import copy
from keyword import kwlist
KEYWORDS = frozenset(kwlist)
from . import Descriptor
from . import _Serialiasable
from .sequence import Sequence, NestedSequence, MultiSequencePart
from .namespace import namespaced
from openpyxl.compat import safe_string
from openpyxl.xml.functions import Element, localname
seq_types = (
 list, tuple)

class Serialisable(_Serialiasable):
    __doc__ = '\n    Objects can serialise to XML their attributes and child objects.\n    The following class attributes are created by the metaclass at runtime:\n    __attrs__ = attributes\n    __nested__ = single-valued child treated as an attribute\n    __elements__ = child elements\n    '
    __attrs__ = None
    __nested__ = None
    __elements__ = None
    __namespaced__ = None
    idx_base = 0

    @property
    def tagname(self):
        raise NotImplementedError

    namespace = None

    @classmethod
    def from_tree(cls, node):
        """
        Create object from XML
        """
        attrib = dict(node.attrib)
        for key, ns in cls.__namespaced__:
            if ns in attrib:
                attrib[key] = attrib[ns]
                del attrib[ns]

        for key in list(attrib):
            if key.startswith('{'):
                del attrib[key]
            elif key in KEYWORDS:
                attrib['_' + key] = attrib[key]
                del attrib[key]
            else:
                if '-' in key:
                    n = key.replace('-', '_')
                    attrib[n] = attrib[key]
                    del attrib[key]
                if node.text:
                    if 'attr_text' in cls.__attrs__:
                        attrib['attr_text'] = node.text
                for el in node:
                    tag = localname(el)
                    if tag in KEYWORDS:
                        tag = '_' + tag
                    desc = getattr(cls, tag, None)
                    if not desc is None:
                        if isinstance(desc, property):
                            pass
                        else:
                            if hasattr(desc, 'from_tree'):
                                obj = desc.from_tree(el)
                            else:
                                if hasattr(desc.expected_type, 'from_tree'):
                                    obj = desc.expected_type.from_tree(el)
                                else:
                                    obj = el.text
                            if isinstance(desc, NestedSequence):
                                attrib[tag] = obj
                            elif isinstance(desc, Sequence):
                                attrib.setdefault(tag, [])
                                attrib[tag].append(obj)
                            elif isinstance(desc, MultiSequencePart):
                                attrib.setdefault(desc.store, [])
                                attrib[desc.store].append(obj)
                            else:
                                attrib[tag] = obj
                    return cls(**attrib)

    def to_tree--- This code section failed: ---

 L. 108         0  LOAD_FAST                'tagname'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 109         8  LOAD_FAST                'self'
               10  LOAD_ATTR                tagname
               12  STORE_FAST               'tagname'
             14_0  COME_FROM             6  '6'

 L. 112        14  LOAD_FAST                'tagname'
               16  LOAD_METHOD              startswith
               18  LOAD_STR                 '_'
               20  CALL_METHOD_1         1  ''
               22  POP_JUMP_IF_FALSE    36  'to 36'

 L. 113        24  LOAD_FAST                'tagname'
               26  LOAD_CONST               1
               28  LOAD_CONST               None
               30  BUILD_SLICE_2         2 
               32  BINARY_SUBSCR    
               34  STORE_FAST               'tagname'
             36_0  COME_FROM            22  '22'

 L. 115        36  LOAD_GLOBAL              namespaced
               38  LOAD_FAST                'self'
               40  LOAD_FAST                'tagname'
               42  LOAD_DEREF               'namespace'
               44  CALL_FUNCTION_3       3  ''
               46  STORE_FAST               'tagname'

 L. 116        48  LOAD_GLOBAL              getattr
               50  LOAD_FAST                'self'
               52  LOAD_STR                 'namespace'
               54  LOAD_DEREF               'namespace'
               56  CALL_FUNCTION_3       3  ''
               58  STORE_DEREF              'namespace'

 L. 118        60  LOAD_GLOBAL              dict
               62  LOAD_FAST                'self'
               64  CALL_FUNCTION_1       1  ''
               66  STORE_FAST               'attrs'

 L. 119        68  LOAD_FAST                'self'
               70  LOAD_ATTR                __namespaced__
               72  GET_ITER         
             74_0  COME_FROM            88  '88'
               74  FOR_ITER            110  'to 110'
               76  UNPACK_SEQUENCE_2     2 
               78  STORE_FAST               'key'
               80  STORE_FAST               'ns'

 L. 120        82  LOAD_FAST                'key'
               84  LOAD_FAST                'attrs'
               86  COMPARE_OP               in
               88  POP_JUMP_IF_FALSE    74  'to 74'

 L. 121        90  LOAD_FAST                'attrs'
               92  LOAD_FAST                'key'
               94  BINARY_SUBSCR    
               96  LOAD_FAST                'attrs'
               98  LOAD_FAST                'ns'
              100  STORE_SUBSCR     

 L. 122       102  LOAD_FAST                'attrs'
              104  LOAD_FAST                'key'
              106  DELETE_SUBSCR    
              108  JUMP_BACK            74  'to 74'

 L. 124       110  LOAD_GLOBAL              Element
              112  LOAD_FAST                'tagname'
              114  LOAD_FAST                'attrs'
              116  CALL_FUNCTION_2       2  ''
              118  STORE_FAST               'el'

 L. 125       120  LOAD_STR                 'attr_text'
              122  LOAD_FAST                'self'
              124  LOAD_ATTR                __attrs__
              126  COMPARE_OP               in
              128  POP_JUMP_IF_FALSE   146  'to 146'

 L. 126       130  LOAD_GLOBAL              safe_string
              132  LOAD_GLOBAL              getattr
              134  LOAD_FAST                'self'
              136  LOAD_STR                 'attr_text'
              138  CALL_FUNCTION_2       2  ''
              140  CALL_FUNCTION_1       1  ''
              142  LOAD_FAST                'el'
              144  STORE_ATTR               text
            146_0  COME_FROM           128  '128'

 L. 128       146  LOAD_FAST                'self'
              148  LOAD_ATTR                __elements__
              150  GET_ITER         
            152_0  COME_FROM           392  '392'
              152  FOR_ITER            406  'to 406'
              154  STORE_DEREF              'child_tag'

 L. 129       156  LOAD_GLOBAL              getattr
              158  LOAD_FAST                'self'
              160  LOAD_ATTR                __class__
              162  LOAD_DEREF               'child_tag'
              164  LOAD_CONST               None
              166  CALL_FUNCTION_3       3  ''
              168  STORE_FAST               'desc'

 L. 130       170  LOAD_GLOBAL              getattr
              172  LOAD_FAST                'self'
              174  LOAD_DEREF               'child_tag'
              176  CALL_FUNCTION_2       2  ''
              178  STORE_FAST               'obj'

 L. 131       180  LOAD_GLOBAL              hasattr
              182  LOAD_FAST                'desc'
              184  LOAD_STR                 'namespace'
              186  CALL_FUNCTION_2       2  ''
              188  POP_JUMP_IF_FALSE   208  'to 208'
              190  LOAD_GLOBAL              hasattr
              192  LOAD_FAST                'obj'
              194  LOAD_STR                 'namespace'
              196  CALL_FUNCTION_2       2  ''
              198  POP_JUMP_IF_FALSE   208  'to 208'

 L. 132       200  LOAD_FAST                'desc'
              202  LOAD_ATTR                namespace
              204  LOAD_FAST                'obj'
              206  STORE_ATTR               namespace
            208_0  COME_FROM           198  '198'
            208_1  COME_FROM           188  '188'

 L. 134       208  LOAD_GLOBAL              isinstance
              210  LOAD_FAST                'obj'
              212  LOAD_GLOBAL              seq_types
              214  CALL_FUNCTION_2       2  ''
          216_218  POP_JUMP_IF_FALSE   334  'to 334'

 L. 135       220  LOAD_GLOBAL              isinstance
              222  LOAD_FAST                'desc'
              224  LOAD_GLOBAL              NestedSequence
              226  CALL_FUNCTION_2       2  ''
              228  POP_JUMP_IF_FALSE   254  'to 254'

 L. 137       230  LOAD_FAST                'obj'
              232  POP_JUMP_IF_TRUE    236  'to 236'

 L. 138       234  JUMP_BACK           152  'to 152'
            236_0  COME_FROM           232  '232'

 L. 139       236  LOAD_FAST                'desc'
              238  LOAD_METHOD              to_tree
              240  LOAD_DEREF               'child_tag'
              242  LOAD_FAST                'obj'
              244  LOAD_DEREF               'namespace'
              246  CALL_METHOD_3         3  ''
              248  BUILD_LIST_1          1 
              250  STORE_FAST               'nodes'
              252  JUMP_FORWARD        310  'to 310'
            254_0  COME_FROM           228  '228'

 L. 140       254  LOAD_GLOBAL              isinstance
              256  LOAD_FAST                'desc'
              258  LOAD_GLOBAL              Sequence
              260  CALL_FUNCTION_2       2  ''
          262_264  POP_JUMP_IF_FALSE   290  'to 290'

 L. 142       266  LOAD_FAST                'self'
              268  LOAD_ATTR                idx_base
              270  LOAD_FAST                'desc'
              272  STORE_ATTR               idx_base

 L. 143       274  LOAD_FAST                'desc'
              276  LOAD_METHOD              to_tree
              278  LOAD_DEREF               'child_tag'
              280  LOAD_FAST                'obj'
              282  LOAD_DEREF               'namespace'
              284  CALL_METHOD_3         3  ''
              286  STORE_FAST               'nodes'
              288  JUMP_FORWARD        310  'to 310'
            290_0  COME_FROM           262  '262'

 L. 145       290  LOAD_CLOSURE             'child_tag'
              292  LOAD_CLOSURE             'namespace'
              294  BUILD_TUPLE_2         2 
              296  LOAD_GENEXPR             '<code_object <genexpr>>'
              298  LOAD_STR                 'Serialisable.to_tree.<locals>.<genexpr>'
              300  MAKE_FUNCTION_8          'closure'
              302  LOAD_FAST                'obj'
              304  GET_ITER         
              306  CALL_FUNCTION_1       1  ''
              308  STORE_FAST               'nodes'
            310_0  COME_FROM           288  '288'
            310_1  COME_FROM           252  '252'

 L. 146       310  LOAD_FAST                'nodes'
              312  GET_ITER         
              314  FOR_ITER            332  'to 332'
              316  STORE_FAST               'node'

 L. 147       318  LOAD_FAST                'el'
              320  LOAD_METHOD              append
              322  LOAD_FAST                'node'
              324  CALL_METHOD_1         1  ''
              326  POP_TOP          
          328_330  JUMP_BACK           314  'to 314'
              332  JUMP_BACK           152  'to 152'
            334_0  COME_FROM           216  '216'

 L. 149       334  LOAD_DEREF               'child_tag'
              336  LOAD_FAST                'self'
              338  LOAD_ATTR                __nested__
              340  COMPARE_OP               in
          342_344  POP_JUMP_IF_FALSE   362  'to 362'

 L. 150       346  LOAD_FAST                'desc'
              348  LOAD_METHOD              to_tree
              350  LOAD_DEREF               'child_tag'
              352  LOAD_FAST                'obj'
              354  LOAD_DEREF               'namespace'
              356  CALL_METHOD_3         3  ''
              358  STORE_FAST               'node'
              360  JUMP_FORWARD        386  'to 386'
            362_0  COME_FROM           342  '342'

 L. 151       362  LOAD_FAST                'obj'
              364  LOAD_CONST               None
              366  COMPARE_OP               is
          368_370  POP_JUMP_IF_FALSE   376  'to 376'

 L. 152       372  JUMP_BACK           152  'to 152'
              374  JUMP_FORWARD        386  'to 386'
            376_0  COME_FROM           368  '368'

 L. 154       376  LOAD_FAST                'obj'
              378  LOAD_METHOD              to_tree
              380  LOAD_DEREF               'child_tag'
              382  CALL_METHOD_1         1  ''
              384  STORE_FAST               'node'
            386_0  COME_FROM           374  '374'
            386_1  COME_FROM           360  '360'

 L. 155       386  LOAD_FAST                'node'
              388  LOAD_CONST               None
              390  COMPARE_OP               is-not
              392  POP_JUMP_IF_FALSE   152  'to 152'

 L. 156       394  LOAD_FAST                'el'
              396  LOAD_METHOD              append
              398  LOAD_FAST                'node'
              400  CALL_METHOD_1         1  ''
              402  POP_TOP          
              404  JUMP_BACK           152  'to 152'

 L. 157       406  LOAD_FAST                'el'
              408  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 374

    def __iter__(self):
        for attr in self.__attrs__:
            value = getattr(self, attr)
            if attr.startswith('_'):
                attr = attr[1:]
            else:
                if attr != 'attr_text' and '_' in attr:
                    desc = getattr(self.__class__, attr)
                    if getattr(desc, 'hyphenated', False):
                        attr = attr.replace('_', '-')
            if attr != 'attr_text' and value is not None:
                (yield (
                 attr, safe_string(value)))

    def __eq__(self, other):
        if not self.__class__ == other.__class__:
            return False
        else:
            return dict(self) == dict(other) or False
        for el in self.__elements__:
            if getattr(self, el) != getattr(other, el):
                return False
            return True

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        s = '<{0}.{1} object>\nParameters:'.format(self.__module__, self.__class__.__name__)
        args = []
        for k in self.__attrs__ + self.__elements__:
            v = getattr(self, k)
            if isinstance(v, Descriptor):
                v = None
            args.append('{0}={1}'.format(k, repr(v)))
        else:
            args = ', '.join(args)
            return '\n'.join([s, args])

    def __hash__(self):
        fields = []
        for attr in self.__attrs__ + self.__elements__:
            val = getattr(self, attr)
            if isinstance(val, list):
                val = tuple(val)
            fields.append(val)
        else:
            return hash(tuple(fields))

    def __add__(self, other):
        if type(self) != type(other):
            raise TypeError('Cannot combine instances of different types')
        vals = {}
        for attr in self.__attrs__:
            vals[attr] = getattr(self, attr) or getattr(other, attr)
        else:
            for el in self.__elements__:
                a = getattr(self, el)
                b = getattr(other, el)
                if a and b:
                    vals[el] = a + b
                else:
                    vals[el] = a or b
            else:
                return (self.__class__)(**vals)

    def __copy__(self):
        xml = self.to_tree(tagname='dummy')
        cp = self.__class__.from_tree(xml)
        for k in self.__dict__:
            if k not in self.__attrs__ + self.__elements__:
                v = copy(getattr(self, k))
                setattr(cp, k, v)
            return cp