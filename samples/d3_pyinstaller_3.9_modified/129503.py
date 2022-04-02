# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\x509\general_name.py
import abc, ipaddress, typing
from email.utils import parseaddr
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


class GeneralName(metaclass=abc.ABCMeta):

    @abc.abstractproperty
    def value(self):
        """
        Return the value of the object
        """
        pass


class RFC822Name(GeneralName):

    def __init__--- This code section failed: ---

 L.  45         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'value'
                4  LOAD_GLOBAL              str
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    54  'to 54'

 L.  46        10  SETUP_FINALLY        26  'to 26'

 L.  47        12  LOAD_FAST                'value'
               14  LOAD_METHOD              encode
               16  LOAD_STR                 'ascii'
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          
               22  POP_BLOCK        
               24  JUMP_FORWARD         62  'to 62'
             26_0  COME_FROM_FINALLY    10  '10'

 L.  48        26  DUP_TOP          
               28  LOAD_GLOBAL              UnicodeEncodeError
               30  <121>                50  ''
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L.  49        38  LOAD_GLOBAL              ValueError

 L.  50        40  LOAD_STR                 'RFC822Name values should be passed as an A-label string. This means unicode characters should be encoded via a library like idna.'

 L.  49        42  CALL_FUNCTION_1       1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
               46  POP_EXCEPT       
               48  JUMP_FORWARD         62  'to 62'
               50  <48>             
               52  JUMP_FORWARD         62  'to 62'
             54_0  COME_FROM             8  '8'

 L.  55        54  LOAD_GLOBAL              TypeError
               56  LOAD_STR                 'value must be string'
               58  CALL_FUNCTION_1       1  ''
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            52  '52'
             62_1  COME_FROM            48  '48'
             62_2  COME_FROM            24  '24'

 L.  57        62  LOAD_GLOBAL              parseaddr
               64  LOAD_FAST                'value'
               66  CALL_FUNCTION_1       1  ''
               68  UNPACK_SEQUENCE_2     2 
               70  STORE_FAST               'name'
               72  STORE_FAST               'address'

 L.  58        74  LOAD_FAST                'name'
               76  POP_JUMP_IF_TRUE     82  'to 82'
               78  LOAD_FAST                'address'
               80  POP_JUMP_IF_TRUE     90  'to 90'
             82_0  COME_FROM            76  '76'

 L.  61        82  LOAD_GLOBAL              ValueError
               84  LOAD_STR                 'Invalid rfc822name value'
               86  CALL_FUNCTION_1       1  ''
               88  RAISE_VARARGS_1       1  'exception instance'
             90_0  COME_FROM            80  '80'

 L.  63        90  LOAD_FAST                'value'
               92  LOAD_FAST                'self'
               94  STORE_ATTR               _value

Parse error at or near `<121>' instruction at offset 30

    value = utils.read_only_property('_value')

    @classmethod
    def _init_without_validation(cls, value):
        instance = cls.__new__(cls)
        instance._value = value
        return instance

    def __repr__(self) -> str:
        return '<RFC822Name(value={0!r})>'.format(self.value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RFC822Name):
            return NotImplemented
        return self.value == other.value

    def __ne__(self, other: object) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash(self.value)


class DNSName(GeneralName):

    def __init__--- This code section failed: ---

 L.  91         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'value'
                4  LOAD_GLOBAL              str
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    54  'to 54'

 L.  92        10  SETUP_FINALLY        26  'to 26'

 L.  93        12  LOAD_FAST                'value'
               14  LOAD_METHOD              encode
               16  LOAD_STR                 'ascii'
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          
               22  POP_BLOCK        
               24  JUMP_FORWARD         62  'to 62'
             26_0  COME_FROM_FINALLY    10  '10'

 L.  94        26  DUP_TOP          
               28  LOAD_GLOBAL              UnicodeEncodeError
               30  <121>                50  ''
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L.  95        38  LOAD_GLOBAL              ValueError

 L.  96        40  LOAD_STR                 'DNSName values should be passed as an A-label string. This means unicode characters should be encoded via a library like idna.'

 L.  95        42  CALL_FUNCTION_1       1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
               46  POP_EXCEPT       
               48  JUMP_FORWARD         62  'to 62'
               50  <48>             
               52  JUMP_FORWARD         62  'to 62'
             54_0  COME_FROM             8  '8'

 L. 101        54  LOAD_GLOBAL              TypeError
               56  LOAD_STR                 'value must be string'
               58  CALL_FUNCTION_1       1  ''
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            52  '52'
             62_1  COME_FROM            48  '48'
             62_2  COME_FROM            24  '24'

 L. 103        62  LOAD_FAST                'value'
               64  LOAD_FAST                'self'
               66  STORE_ATTR               _value

Parse error at or near `<121>' instruction at offset 30

    value = utils.read_only_property('_value')

    @classmethod
    def _init_without_validation(cls, value):
        instance = cls.__new__(cls)
        instance._value = value
        return instance

    def __repr__(self):
        return '<DNSName(value={0!r})>'.format(self.value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DNSName):
            return NotImplemented
        return self.value == other.value

    def __ne__(self, other: object) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash(self.value)


class UniformResourceIdentifier(GeneralName):

    def __init__--- This code section failed: ---

 L. 131         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'value'
                4  LOAD_GLOBAL              str
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    54  'to 54'

 L. 132        10  SETUP_FINALLY        26  'to 26'

 L. 133        12  LOAD_FAST                'value'
               14  LOAD_METHOD              encode
               16  LOAD_STR                 'ascii'
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          
               22  POP_BLOCK        
               24  JUMP_FORWARD         62  'to 62'
             26_0  COME_FROM_FINALLY    10  '10'

 L. 134        26  DUP_TOP          
               28  LOAD_GLOBAL              UnicodeEncodeError
               30  <121>                50  ''
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L. 135        38  LOAD_GLOBAL              ValueError

 L. 136        40  LOAD_STR                 'URI values should be passed as an A-label string. This means unicode characters should be encoded via a library like idna.'

 L. 135        42  CALL_FUNCTION_1       1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
               46  POP_EXCEPT       
               48  JUMP_FORWARD         62  'to 62'
               50  <48>             
               52  JUMP_FORWARD         62  'to 62'
             54_0  COME_FROM             8  '8'

 L. 141        54  LOAD_GLOBAL              TypeError
               56  LOAD_STR                 'value must be string'
               58  CALL_FUNCTION_1       1  ''
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            52  '52'
             62_1  COME_FROM            48  '48'
             62_2  COME_FROM            24  '24'

 L. 143        62  LOAD_FAST                'value'
               64  LOAD_FAST                'self'
               66  STORE_ATTR               _value

Parse error at or near `<121>' instruction at offset 30

    value = utils.read_only_property('_value')

    @classmethod
    def _init_without_validation(cls, value):
        instance = cls.__new__(cls)
        instance._value = value
        return instance

    def __repr__(self) -> str:
        return '<UniformResourceIdentifier(value={0!r})>'.format(self.value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UniformResourceIdentifier):
            return NotImplemented
        return self.value == other.value

    def __ne__(self, other: object) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash(self.value)


class DirectoryName(GeneralName):

    def __init__(self, value: Name):
        if not isinstance(value, Name):
            raise TypeError('value must be a Name')
        self._value = value

    value = utils.read_only_property('_value')

    def __repr__(self) -> str:
        return '<DirectoryName(value={})>'.format(self.value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DirectoryName):
            return NotImplemented
        return self.value == other.value

    def __ne__(self, other: object) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash(self.value)


class RegisteredID(GeneralName):

    def __init__(self, value: ObjectIdentifier):
        if not isinstance(value, ObjectIdentifier):
            raise TypeError('value must be an ObjectIdentifier')
        self._value = value

    value = utils.read_only_property('_value')

    def __repr__(self) -> str:
        return '<RegisteredID(value={})>'.format(self.value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RegisteredID):
            return NotImplemented
        return self.value == other.value

    def __ne__(self, other: object) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash(self.value)


class IPAddress(GeneralName):

    def __init__(self, value: typing.Union[(
 ipaddress.IPv4Address,
 ipaddress.IPv6Address,
 ipaddress.IPv4Network,
 ipaddress.IPv6Network)]):
        if not isinstance(value, (
         ipaddress.IPv4Address,
         ipaddress.IPv6Address,
         ipaddress.IPv4Network,
         ipaddress.IPv6Network)):
            raise TypeError('value must be an instance of ipaddress.IPv4Address, ipaddress.IPv6Address, ipaddress.IPv4Network, or ipaddress.IPv6Network')
        self._value = value

    value = utils.read_only_property('_value')

    def __repr__(self) -> str:
        return '<IPAddress(value={})>'.format(self.value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, IPAddress):
            return NotImplemented
        return self.value == other.value

    def __ne__(self, other: object) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash(self.value)


class OtherName(GeneralName):

    def __init__(self, type_id: ObjectIdentifier, value: bytes):
        if not isinstance(type_id, ObjectIdentifier):
            raise TypeError('type_id must be an ObjectIdentifier')
        if not isinstance(value, bytes):
            raise TypeError('value must be a binary string')
        self._type_id = type_id
        self._value = value

    type_id = utils.read_only_property('_type_id')
    value = utils.read_only_property('_value')

    def __repr__(self) -> str:
        return '<OtherName(type_id={}, value={!r})>'.format(self.type_id, self.value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, OtherName):
            return NotImplemented
        return self.type_id == other.type_id and self.value == other.value

    def __ne__(self, other: object) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash((self.type_id, self.value))