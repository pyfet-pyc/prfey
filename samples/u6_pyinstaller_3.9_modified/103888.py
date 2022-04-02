# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\x509\general_name.py
from __future__ import absolute_import, division, print_function
import abc, ipaddress
from email.utils import parseaddr
import six
from cryptography import utils
from cryptography.x509.name import Name
from cryptography.x509.oid import ObjectIdentifier
_GENERAL_NAMES = {0:'otherName', 
 1:'rfc822Name', 
 2:'dNSName', 
 3:'x400Address', 
 4:'directoryName', 
 5:'ediPartyName', 
 6:'uniformResourceIdentifier', 
 7:'iPAddress', 
 8:'registeredID'}

class UnsupportedGeneralNameType(Exception):

    def __init__(self, msg, type):
        super(UnsupportedGeneralNameType, self).__init__(msg)
        self.type = type


@six.add_metaclass(abc.ABCMeta)
class GeneralName(object):

    @abc.abstractproperty
    def value(self):
        """
        Return the value of the object
        """
        pass


@utils.register_interface(GeneralName)
class RFC822Name(object):

    def __init__--- This code section failed: ---

 L.  49         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'value'
                4  LOAD_GLOBAL              six
                6  LOAD_ATTR                text_type
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_FALSE    56  'to 56'

 L.  50        12  SETUP_FINALLY        28  'to 28'

 L.  51        14  LOAD_FAST                'value'
               16  LOAD_METHOD              encode
               18  LOAD_STR                 'ascii'
               20  CALL_METHOD_1         1  ''
               22  POP_TOP          
               24  POP_BLOCK        
               26  JUMP_ABSOLUTE        64  'to 64'
             28_0  COME_FROM_FINALLY    12  '12'

 L.  52        28  DUP_TOP          
               30  LOAD_GLOBAL              UnicodeEncodeError
               32  <121>                52  ''
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L.  53        40  LOAD_GLOBAL              ValueError

 L.  54        42  LOAD_STR                 'RFC822Name values should be passed as an A-label string. This means unicode characters should be encoded via a library like idna.'

 L.  53        44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  'exception instance'
               48  POP_EXCEPT       
               50  JUMP_ABSOLUTE        64  'to 64'
               52  <48>             
               54  JUMP_FORWARD         64  'to 64'
             56_0  COME_FROM            10  '10'

 L.  59        56  LOAD_GLOBAL              TypeError
               58  LOAD_STR                 'value must be string'
               60  CALL_FUNCTION_1       1  ''
               62  RAISE_VARARGS_1       1  'exception instance'
             64_0  COME_FROM_EXCEPT_CLAUSE    54  '54'
             64_1  COME_FROM_EXCEPT_CLAUSE    50  '50'

 L.  61        64  LOAD_GLOBAL              parseaddr
               66  LOAD_FAST                'value'
               68  CALL_FUNCTION_1       1  ''
               70  UNPACK_SEQUENCE_2     2 
               72  STORE_FAST               'name'
               74  STORE_FAST               'address'

 L.  62        76  LOAD_FAST                'name'
               78  POP_JUMP_IF_TRUE     84  'to 84'
               80  LOAD_FAST                'address'
               82  POP_JUMP_IF_TRUE     92  'to 92'
             84_0  COME_FROM            78  '78'

 L.  65        84  LOAD_GLOBAL              ValueError
               86  LOAD_STR                 'Invalid rfc822name value'
               88  CALL_FUNCTION_1       1  ''
               90  RAISE_VARARGS_1       1  'exception instance'
             92_0  COME_FROM            82  '82'

 L.  67        92  LOAD_FAST                'value'
               94  LOAD_FAST                'self'
               96  STORE_ATTR               _value

Parse error at or near `<121>' instruction at offset 32

    value = utils.read_only_property('_value')

    @classmethod
    def _init_without_validation(cls, value):
        instance = cls.__new__(cls)
        instance._value = value
        return instance

    def __repr__(self):
        return '<RFC822Name(value={0!r})>'.format(self.value)

    def __eq__(self, other):
        if not isinstance(other, RFC822Name):
            return NotImplemented
        return self.value == other.value

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.value)


@utils.register_interface(GeneralName)
class DNSName(object):

    def __init__--- This code section failed: ---

 L.  96         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'value'
                4  LOAD_GLOBAL              six
                6  LOAD_ATTR                text_type
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_FALSE    56  'to 56'

 L.  97        12  SETUP_FINALLY        28  'to 28'

 L.  98        14  LOAD_FAST                'value'
               16  LOAD_METHOD              encode
               18  LOAD_STR                 'ascii'
               20  CALL_METHOD_1         1  ''
               22  POP_TOP          
               24  POP_BLOCK        
               26  JUMP_ABSOLUTE        64  'to 64'
             28_0  COME_FROM_FINALLY    12  '12'

 L.  99        28  DUP_TOP          
               30  LOAD_GLOBAL              UnicodeEncodeError
               32  <121>                52  ''
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L. 100        40  LOAD_GLOBAL              ValueError

 L. 101        42  LOAD_STR                 'DNSName values should be passed as an A-label string. This means unicode characters should be encoded via a library like idna.'

 L. 100        44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  'exception instance'
               48  POP_EXCEPT       
               50  JUMP_ABSOLUTE        64  'to 64'
               52  <48>             
               54  JUMP_FORWARD         64  'to 64'
             56_0  COME_FROM            10  '10'

 L. 106        56  LOAD_GLOBAL              TypeError
               58  LOAD_STR                 'value must be string'
               60  CALL_FUNCTION_1       1  ''
               62  RAISE_VARARGS_1       1  'exception instance'
             64_0  COME_FROM_EXCEPT_CLAUSE    54  '54'
             64_1  COME_FROM_EXCEPT_CLAUSE    50  '50'

 L. 108        64  LOAD_FAST                'value'
               66  LOAD_FAST                'self'
               68  STORE_ATTR               _value

Parse error at or near `<121>' instruction at offset 32

    value = utils.read_only_property('_value')

    @classmethod
    def _init_without_validation(cls, value):
        instance = cls.__new__(cls)
        instance._value = value
        return instance

    def __repr__(self):
        return '<DNSName(value={0!r})>'.format(self.value)

    def __eq__(self, other):
        if not isinstance(other, DNSName):
            return NotImplemented
        return self.value == other.value

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.value)


@utils.register_interface(GeneralName)
class UniformResourceIdentifier(object):

    def __init__--- This code section failed: ---

 L. 137         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'value'
                4  LOAD_GLOBAL              six
                6  LOAD_ATTR                text_type
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_FALSE    56  'to 56'

 L. 138        12  SETUP_FINALLY        28  'to 28'

 L. 139        14  LOAD_FAST                'value'
               16  LOAD_METHOD              encode
               18  LOAD_STR                 'ascii'
               20  CALL_METHOD_1         1  ''
               22  POP_TOP          
               24  POP_BLOCK        
               26  JUMP_ABSOLUTE        64  'to 64'
             28_0  COME_FROM_FINALLY    12  '12'

 L. 140        28  DUP_TOP          
               30  LOAD_GLOBAL              UnicodeEncodeError
               32  <121>                52  ''
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L. 141        40  LOAD_GLOBAL              ValueError

 L. 142        42  LOAD_STR                 'URI values should be passed as an A-label string. This means unicode characters should be encoded via a library like idna.'

 L. 141        44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  'exception instance'
               48  POP_EXCEPT       
               50  JUMP_ABSOLUTE        64  'to 64'
               52  <48>             
               54  JUMP_FORWARD         64  'to 64'
             56_0  COME_FROM            10  '10'

 L. 147        56  LOAD_GLOBAL              TypeError
               58  LOAD_STR                 'value must be string'
               60  CALL_FUNCTION_1       1  ''
               62  RAISE_VARARGS_1       1  'exception instance'
             64_0  COME_FROM_EXCEPT_CLAUSE    54  '54'
             64_1  COME_FROM_EXCEPT_CLAUSE    50  '50'

 L. 149        64  LOAD_FAST                'value'
               66  LOAD_FAST                'self'
               68  STORE_ATTR               _value

Parse error at or near `<121>' instruction at offset 32

    value = utils.read_only_property('_value')

    @classmethod
    def _init_without_validation(cls, value):
        instance = cls.__new__(cls)
        instance._value = value
        return instance

    def __repr__(self):
        return '<UniformResourceIdentifier(value={0!r})>'.format(self.value)

    def __eq__(self, other):
        if not isinstance(other, UniformResourceIdentifier):
            return NotImplemented
        return self.value == other.value

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.value)


@utils.register_interface(GeneralName)
class DirectoryName(object):

    def __init__(self, value):
        if not isinstance(value, Name):
            raise TypeError('value must be a Name')
        self._value = value

    value = utils.read_only_property('_value')

    def __repr__(self):
        return '<DirectoryName(value={})>'.format(self.value)

    def __eq__(self, other):
        if not isinstance(other, DirectoryName):
            return NotImplemented
        return self.value == other.value

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.value)


@utils.register_interface(GeneralName)
class RegisteredID(object):

    def __init__(self, value):
        if not isinstance(value, ObjectIdentifier):
            raise TypeError('value must be an ObjectIdentifier')
        self._value = value

    value = utils.read_only_property('_value')

    def __repr__(self):
        return '<RegisteredID(value={})>'.format(self.value)

    def __eq__(self, other):
        if not isinstance(other, RegisteredID):
            return NotImplemented
        return self.value == other.value

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.value)


@utils.register_interface(GeneralName)
class IPAddress(object):

    def __init__(self, value):
        if not isinstance(value, (
         ipaddress.IPv4Address,
         ipaddress.IPv6Address,
         ipaddress.IPv4Network,
         ipaddress.IPv6Network)):
            raise TypeError('value must be an instance of ipaddress.IPv4Address, ipaddress.IPv6Address, ipaddress.IPv4Network, or ipaddress.IPv6Network')
        self._value = value

    value = utils.read_only_property('_value')

    def __repr__(self):
        return '<IPAddress(value={})>'.format(self.value)

    def __eq__(self, other):
        if not isinstance(other, IPAddress):
            return NotImplemented
        return self.value == other.value

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.value)


@utils.register_interface(GeneralName)
class OtherName(object):

    def __init__(self, type_id, value):
        if not isinstance(type_id, ObjectIdentifier):
            raise TypeError('type_id must be an ObjectIdentifier')
        if not isinstance(value, bytes):
            raise TypeError('value must be a binary string')
        self._type_id = type_id
        self._value = value

    type_id = utils.read_only_property('_type_id')
    value = utils.read_only_property('_value')

    def __repr__(self):
        return '<OtherName(type_id={}, value={!r})>'.format(self.type_id, self.value)

    def __eq__(self, other):
        if not isinstance(other, OtherName):
            return NotImplemented
        return self.type_id == other.type_id and self.value == other.value

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.type_id, self.value))