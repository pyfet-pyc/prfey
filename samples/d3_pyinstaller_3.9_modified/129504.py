# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\x509\name.py
import typing
from enum import Enum
from cryptography import utils
from cryptography.hazmat.backends import _get_backend
from cryptography.x509.oid import NameOID, ObjectIdentifier

class _ASN1Type(Enum):
    UTF8String = 12
    NumericString = 18
    PrintableString = 19
    T61String = 20
    IA5String = 22
    UTCTime = 23
    GeneralizedTime = 24
    VisibleString = 26
    UniversalString = 28
    BMPString = 30


_ASN1_TYPE_TO_ENUM = {i:i.value for i in _ASN1Type}
_SENTINEL = object()
_NAMEOID_DEFAULT_TYPE = {NameOID.COUNTRY_NAME: _ASN1Type.PrintableString, 
 NameOID.JURISDICTION_COUNTRY_NAME: _ASN1Type.PrintableString, 
 NameOID.SERIAL_NUMBER: _ASN1Type.PrintableString, 
 NameOID.DN_QUALIFIER: _ASN1Type.PrintableString, 
 NameOID.EMAIL_ADDRESS: _ASN1Type.IA5String, 
 NameOID.DOMAIN_COMPONENT: _ASN1Type.IA5String}
_NAMEOID_TO_NAME = {NameOID.COMMON_NAME: 'CN', 
 NameOID.LOCALITY_NAME: 'L', 
 NameOID.STATE_OR_PROVINCE_NAME: 'ST', 
 NameOID.ORGANIZATION_NAME: 'O', 
 NameOID.ORGANIZATIONAL_UNIT_NAME: 'OU', 
 NameOID.COUNTRY_NAME: 'C', 
 NameOID.STREET_ADDRESS: 'STREET', 
 NameOID.DOMAIN_COMPONENT: 'DC', 
 NameOID.USER_ID: 'UID'}

def _escape_dn_value--- This code section failed: ---

 L.  55         0  LOAD_FAST                'val'
                2  POP_JUMP_IF_TRUE      8  'to 8'

 L.  56         4  LOAD_STR                 ''
                6  RETURN_VALUE     
              8_0  COME_FROM             2  '2'

 L.  59         8  LOAD_FAST                'val'
               10  LOAD_METHOD              replace
               12  LOAD_STR                 '\\'
               14  LOAD_STR                 '\\\\'
               16  CALL_METHOD_2         2  ''
               18  STORE_FAST               'val'

 L.  60        20  LOAD_FAST                'val'
               22  LOAD_METHOD              replace
               24  LOAD_STR                 '"'
               26  LOAD_STR                 '\\"'
               28  CALL_METHOD_2         2  ''
               30  STORE_FAST               'val'

 L.  61        32  LOAD_FAST                'val'
               34  LOAD_METHOD              replace
               36  LOAD_STR                 '+'
               38  LOAD_STR                 '\\+'
               40  CALL_METHOD_2         2  ''
               42  STORE_FAST               'val'

 L.  62        44  LOAD_FAST                'val'
               46  LOAD_METHOD              replace
               48  LOAD_STR                 ','
               50  LOAD_STR                 '\\,'
               52  CALL_METHOD_2         2  ''
               54  STORE_FAST               'val'

 L.  63        56  LOAD_FAST                'val'
               58  LOAD_METHOD              replace
               60  LOAD_STR                 ';'
               62  LOAD_STR                 '\\;'
               64  CALL_METHOD_2         2  ''
               66  STORE_FAST               'val'

 L.  64        68  LOAD_FAST                'val'
               70  LOAD_METHOD              replace
               72  LOAD_STR                 '<'
               74  LOAD_STR                 '\\<'
               76  CALL_METHOD_2         2  ''
               78  STORE_FAST               'val'

 L.  65        80  LOAD_FAST                'val'
               82  LOAD_METHOD              replace
               84  LOAD_STR                 '>'
               86  LOAD_STR                 '\\>'
               88  CALL_METHOD_2         2  ''
               90  STORE_FAST               'val'

 L.  66        92  LOAD_FAST                'val'
               94  LOAD_METHOD              replace
               96  LOAD_STR                 '\x00'
               98  LOAD_STR                 '\\00'
              100  CALL_METHOD_2         2  ''
              102  STORE_FAST               'val'

 L.  68       104  LOAD_FAST                'val'
              106  LOAD_CONST               0
              108  BINARY_SUBSCR    
              110  LOAD_CONST               ('#', ' ')
              112  <118>                 0  ''
              114  POP_JUMP_IF_FALSE   124  'to 124'

 L.  69       116  LOAD_STR                 '\\'
              118  LOAD_FAST                'val'
              120  BINARY_ADD       
              122  STORE_FAST               'val'
            124_0  COME_FROM           114  '114'

 L.  70       124  LOAD_FAST                'val'
              126  LOAD_CONST               -1
              128  BINARY_SUBSCR    
              130  LOAD_STR                 ' '
              132  COMPARE_OP               ==
              134  POP_JUMP_IF_FALSE   152  'to 152'

 L.  71       136  LOAD_FAST                'val'
              138  LOAD_CONST               None
              140  LOAD_CONST               -1
              142  BUILD_SLICE_2         2 
              144  BINARY_SUBSCR    
              146  LOAD_STR                 '\\ '
              148  BINARY_ADD       
              150  STORE_FAST               'val'
            152_0  COME_FROM           134  '134'

 L.  73       152  LOAD_FAST                'val'
              154  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 112


class NameAttribute(object):

    def __init__(self, oid: ObjectIdentifier, value: str, _type=_SENTINEL):
        if not isinstance(oid, ObjectIdentifier):
            raise TypeError('oid argument must be an ObjectIdentifier instance.')
        if not isinstance(value, str):
            raise TypeError('value argument must be a text type.')
        if oid == NameOID.COUNTRY_NAME or (oid == NameOID.JURISDICTION_COUNTRY_NAME):
            if len(value.encode('utf8')) != 2:
                raise ValueError('Country name must be a 2 character country code')
        if _type == _SENTINEL:
            _type = _NAMEOID_DEFAULT_TYPE.getoid_ASN1Type.UTF8String
        if not isinstance(_type, _ASN1Type):
            raise TypeError('_type must be from the _ASN1Type enum')
        self._oid = oid
        self._value = value
        self._type = _type

    oid = utils.read_only_property('_oid')
    value = utils.read_only_property('_value')

    def rfc4514_string(self) -> str:
        """
        Format as RFC4514 Distinguished Name string.

        Use short attribute name if available, otherwise fall back to OID
        dotted string.
        """
        key = _NAMEOID_TO_NAME.getself.oidself.oid.dotted_string
        return '%s=%s' % (key, _escape_dn_value(self.value))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, NameAttribute):
            return NotImplemented
        return self.oid == other.oid and self.value == other.value

    def __ne__(self, other: object) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash((self.oid, self.value))

    def __repr__(self) -> str:
        return '<NameAttribute(oid={0.oid}, value={0.value!r})>'.format(self)


class RelativeDistinguishedName(object):

    def __init__(self, attributes: typing.Iterable[NameAttribute]):
        attributes = list(attributes)
        if not attributes:
            raise ValueError('a relative distinguished name cannot be empty')
        if not all((isinstance(x, NameAttribute) for x in attributes)):
            raise TypeError('attributes must be an iterable of NameAttribute')
        self._attributes = attributes
        self._attribute_set = frozenset(attributes)
        if len(self._attribute_set) != len(attributes):
            raise ValueError('duplicate attributes are not allowed')

    def get_attributes_for_oid(self, oid) -> typing.List[NameAttribute]:
        return [i for i in self if i.oid == oid]

    def rfc4514_string(self) -> str:
        """
        Format as RFC4514 Distinguished Name string.

        Within each RDN, attributes are joined by '+', although that is rarely
        used in certificates.
        """
        return '+'.join((attr.rfc4514_string() for attr in self._attributes))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RelativeDistinguishedName):
            return NotImplemented
        return self._attribute_set == other._attribute_set

    def __ne__(self, other: object) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash(self._attribute_set)

    def __iter__(self) -> typing.Iterator[NameAttribute]:
        return iter(self._attributes)

    def __len__(self) -> int:
        return len(self._attributes)

    def __repr__(self) -> str:
        return '<RelativeDistinguishedName({})>'.format(self.rfc4514_string())


class Name(object):

    def __init__(self, attributes):
        attributes = list(attributes)
        if all((isinstance(x, NameAttribute) for x in attributes)):
            self._attributes = [RelativeDistinguishedName([x]) for x in attributes]
        elif all((isinstance(x, RelativeDistinguishedName) for x in attributes)):
            self._attributes = attributes
        else:
            raise TypeError('attributes must be a list of NameAttribute or a list RelativeDistinguishedName')

    def rfc4514_string(self) -> str:
        """
        Format as RFC4514 Distinguished Name string.
        For example 'CN=foobar.com,O=Foo Corp,C=US'

        An X.509 name is a two-level structure: a list of sets of attributes.
        Each list element is separated by ',' and within each list element, set
        elements are separated by '+'. The latter is almost never used in
        real world certificates. According to RFC4514 section 2.1 the
        RDNSequence must be reversed when converting to string representation.
        """
        return ','.join((attr.rfc4514_string() for attr in reversed(self._attributes)))

    def get_attributes_for_oid(self, oid) -> typing.List[NameAttribute]:
        return [i for i in self if i.oid == oid]

    @property
    def rdns(self) -> typing.Iterable[RelativeDistinguishedName]:
        return self._attributes

    def public_bytes(self, backend=None) -> bytes:
        backend = _get_backend(backend)
        return backend.x509_name_bytes(self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Name):
            return NotImplemented
        return self._attributes == other._attributes

    def __ne__(self, other: object) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash(tuple(self._attributes))

    def __iter__(self) -> typing.Iterator[NameAttribute]:
        for rdn in self._attributes:
            for ava in rdn:
                yield ava

    def __len__(self) -> int:
        return sum((len(rdn) for rdn in self._attributes))

    def __repr__(self) -> str:
        rdns = ','.join((attr.rfc4514_string() for attr in self._attributes))
        return '<Name({})>'.format(rdns)