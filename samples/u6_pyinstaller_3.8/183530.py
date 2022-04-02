# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\cryptography\x509\general_name.py
from __future__ import absolute_import, division, print_function
import abc, ipaddress, warnings
from email.utils import parseaddr
import six
from six.moves import urllib_parse
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

def _lazy_import_idna--- This code section failed: ---

 L.  36         0  SETUP_FINALLY        16  'to 16'

 L.  37         2  LOAD_CONST               0
                4  LOAD_CONST               None
                6  IMPORT_NAME              idna
                8  STORE_FAST               'idna'

 L.  38        10  LOAD_FAST                'idna'
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L.  39        16  DUP_TOP          
               18  LOAD_GLOBAL              ImportError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    42  'to 42'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L.  40        30  LOAD_GLOBAL              ImportError

 L.  41        32  LOAD_STR                 'idna is not installed, but a deprecated feature that requires it was used. See: https://cryptography.io/en/latest/faq/#importerror-idna-is-not-installed'

 L.  40        34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
               38  POP_EXCEPT       
               40  JUMP_FORWARD         44  'to 44'
             42_0  COME_FROM            22  '22'
               42  END_FINALLY      
             44_0  COME_FROM            40  '40'

Parse error at or near `POP_TOP' instruction at offset 26


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

    def __init__(self, value):
        if isinstance(value, six.text_type):
            try:
                value.encode('ascii')
            except UnicodeEncodeError:
                value = self._idna_encode(value)
                warnings.warn('RFC822Name values should be passed as an A-label string. This means unicode characters should be encoded via idna. Support for passing unicode strings (aka U-label) will be removed in a future version.',
                  (utils.PersistentlyDeprecated2017),
                  stacklevel=2)

        else:
            raise TypeError('value must be string')
        name, address = parseaddr(value)
        if not (name or address):
            raise ValueError('Invalid rfc822name value')
        self._value = value

    value = utils.read_only_property('_value')

    @classmethod
    def _init_without_validation(cls, value):
        instance = cls.__new__(cls)
        instance._value = value
        return instance

    def _idna_encode(self, value):
        idna = _lazy_import_idna()
        _, address = parseaddr(value)
        parts = address.split('@')
        return parts[0] + '@' + idna.encode(parts[1]).decode('ascii')

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


def _idna_encode(value):
    idna = _lazy_import_idna()
    for prefix in ('*.', '.'):
        if value.startswith(prefix):
            value = value[len(prefix):]
            return prefix + idna.encode(value).decode('ascii')
        return idna.encode(value).decode('ascii')


@utils.register_interface(GeneralName)
class DNSName(object):

    def __init__(self, value):
        if isinstance(value, six.text_type):
            try:
                value.encode('ascii')
            except UnicodeEncodeError:
                value = _idna_encode(value)
                warnings.warn('DNSName values should be passed as an A-label string. This means unicode characters should be encoded via idna. Support for passing unicode strings (aka U-label) will be removed in a future version.',
                  (utils.PersistentlyDeprecated2017),
                  stacklevel=2)

        else:
            raise TypeError('value must be string')
        self._value = value

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

    def __init__(self, value):
        if isinstance(value, six.text_type):
            try:
                value.encode('ascii')
            except UnicodeEncodeError:
                value = self._idna_encode(value)
                warnings.warn('URI values should be passed as an A-label string. This means unicode characters should be encoded via idna. Support for passing unicode strings (aka U-label)  will be removed in a future version.',
                  (utils.PersistentlyDeprecated2017),
                  stacklevel=2)

        else:
            raise TypeError('value must be string')
        self._value = value

    value = utils.read_only_property('_value')

    @classmethod
    def _init_without_validation(cls, value):
        instance = cls.__new__(cls)
        instance._value = value
        return instance

    def _idna_encode(self, value):
        idna = _lazy_import_idna()
        parsed = urllib_parse.urlparse(value)
        if parsed.port:
            netloc = (idna.encode(parsed.hostname) + ':{}'.format(parsed.port).encode('ascii')).decode('ascii')
        else:
            netloc = idna.encode(parsed.hostname).decode('ascii')
        return urllib_parse.urlunparse((
         parsed.scheme,
         netloc,
         parsed.path,
         parsed.params,
         parsed.query,
         parsed.fragment))

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