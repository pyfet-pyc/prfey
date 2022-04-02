# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\x509\extensions.py
from __future__ import absolute_import, division, print_function
import abc, datetime, hashlib, ipaddress
from enum import Enum
import six
from cryptography import utils
from cryptography.hazmat._der import BIT_STRING, DERReader, OBJECT_IDENTIFIER, SEQUENCE
from cryptography.hazmat.primitives import constant_time, serialization
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.x509.certificate_transparency import SignedCertificateTimestamp
from cryptography.x509.general_name import GeneralName, IPAddress, OtherName
from cryptography.x509.name import RelativeDistinguishedName
from cryptography.x509.oid import CRLEntryExtensionOID, ExtensionOID, OCSPExtensionOID, ObjectIdentifier

def _key_identifier_from_public_key--- This code section failed: ---

 L.  39         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'public_key'
                4  LOAD_GLOBAL              RSAPublicKey
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    32  'to 32'

 L.  40        10  LOAD_FAST                'public_key'
               12  LOAD_METHOD              public_bytes

 L.  41        14  LOAD_GLOBAL              serialization
               16  LOAD_ATTR                Encoding
               18  LOAD_ATTR                DER

 L.  42        20  LOAD_GLOBAL              serialization
               22  LOAD_ATTR                PublicFormat
               24  LOAD_ATTR                PKCS1

 L.  40        26  CALL_METHOD_2         2  ''
               28  STORE_FAST               'data'
               30  JUMP_FORWARD        242  'to 242'
             32_0  COME_FROM             8  '8'

 L.  44        32  LOAD_GLOBAL              isinstance
               34  LOAD_FAST                'public_key'
               36  LOAD_GLOBAL              EllipticCurvePublicKey
               38  CALL_FUNCTION_2       2  ''
               40  POP_JUMP_IF_FALSE    64  'to 64'

 L.  45        42  LOAD_FAST                'public_key'
               44  LOAD_METHOD              public_bytes

 L.  46        46  LOAD_GLOBAL              serialization
               48  LOAD_ATTR                Encoding
               50  LOAD_ATTR                X962

 L.  47        52  LOAD_GLOBAL              serialization
               54  LOAD_ATTR                PublicFormat
               56  LOAD_ATTR                UncompressedPoint

 L.  45        58  CALL_METHOD_2         2  ''
               60  STORE_FAST               'data'
               62  JUMP_FORWARD        242  'to 242'
             64_0  COME_FROM            40  '40'

 L.  51        64  LOAD_FAST                'public_key'
               66  LOAD_METHOD              public_bytes

 L.  52        68  LOAD_GLOBAL              serialization
               70  LOAD_ATTR                Encoding
               72  LOAD_ATTR                DER

 L.  53        74  LOAD_GLOBAL              serialization
               76  LOAD_ATTR                PublicFormat
               78  LOAD_ATTR                SubjectPublicKeyInfo

 L.  51        80  CALL_METHOD_2         2  ''
               82  STORE_FAST               'serialized'

 L.  56        84  LOAD_GLOBAL              DERReader
               86  LOAD_FAST                'serialized'
               88  CALL_FUNCTION_1       1  ''
               90  STORE_FAST               'reader'

 L.  57        92  LOAD_FAST                'reader'
               94  LOAD_METHOD              read_single_element
               96  LOAD_GLOBAL              SEQUENCE
               98  CALL_METHOD_1         1  ''
              100  SETUP_WITH          138  'to 138'
              102  STORE_FAST               'public_key_info'

 L.  58       104  LOAD_FAST                'public_key_info'
              106  LOAD_METHOD              read_element
              108  LOAD_GLOBAL              SEQUENCE
              110  CALL_METHOD_1         1  ''
              112  STORE_FAST               'algorithm'

 L.  59       114  LOAD_FAST                'public_key_info'
              116  LOAD_METHOD              read_element
              118  LOAD_GLOBAL              BIT_STRING
              120  CALL_METHOD_1         1  ''
              122  STORE_FAST               'public_key'
              124  POP_BLOCK        
              126  LOAD_CONST               None
              128  DUP_TOP          
              130  DUP_TOP          
              132  CALL_FUNCTION_3       3  ''
              134  POP_TOP          
              136  JUMP_FORWARD        154  'to 154'
            138_0  COME_FROM_WITH      100  '100'
              138  <49>             
              140  POP_JUMP_IF_TRUE    144  'to 144'
              142  <48>             
            144_0  COME_FROM           140  '140'
              144  POP_TOP          
              146  POP_TOP          
              148  POP_TOP          
              150  POP_EXCEPT       
              152  POP_TOP          
            154_0  COME_FROM           136  '136'

 L.  62       154  LOAD_FAST                'algorithm'
              156  SETUP_WITH          200  'to 200'
              158  POP_TOP          

 L.  63       160  LOAD_FAST                'algorithm'
              162  LOAD_METHOD              read_element
              164  LOAD_GLOBAL              OBJECT_IDENTIFIER
              166  CALL_METHOD_1         1  ''
              168  POP_TOP          

 L.  64       170  LOAD_FAST                'algorithm'
              172  LOAD_METHOD              is_empty
              174  CALL_METHOD_0         0  ''
              176  POP_JUMP_IF_TRUE    186  'to 186'

 L.  66       178  LOAD_FAST                'algorithm'
              180  LOAD_METHOD              read_any_element
              182  CALL_METHOD_0         0  ''
              184  POP_TOP          
            186_0  COME_FROM           176  '176'
              186  POP_BLOCK        
              188  LOAD_CONST               None
              190  DUP_TOP          
              192  DUP_TOP          
              194  CALL_FUNCTION_3       3  ''
              196  POP_TOP          
              198  JUMP_FORWARD        216  'to 216'
            200_0  COME_FROM_WITH      156  '156'
              200  <49>             
              202  POP_JUMP_IF_TRUE    206  'to 206'
              204  <48>             
            206_0  COME_FROM           202  '202'
              206  POP_TOP          
              208  POP_TOP          
              210  POP_TOP          
              212  POP_EXCEPT       
              214  POP_TOP          
            216_0  COME_FROM           198  '198'

 L.  70       216  LOAD_FAST                'public_key'
              218  LOAD_METHOD              read_byte
              220  CALL_METHOD_0         0  ''
              222  LOAD_CONST               0
              224  COMPARE_OP               !=
              226  POP_JUMP_IF_FALSE   236  'to 236'

 L.  71       228  LOAD_GLOBAL              ValueError
              230  LOAD_STR                 'Invalid public key encoding'
              232  CALL_FUNCTION_1       1  ''
              234  RAISE_VARARGS_1       1  'exception instance'
            236_0  COME_FROM           226  '226'

 L.  73       236  LOAD_FAST                'public_key'
              238  LOAD_ATTR                data
              240  STORE_FAST               'data'
            242_0  COME_FROM            62  '62'
            242_1  COME_FROM            30  '30'

 L.  75       242  LOAD_GLOBAL              hashlib
              244  LOAD_METHOD              sha1
              246  LOAD_FAST                'data'
              248  CALL_METHOD_1         1  ''
              250  LOAD_METHOD              digest
              252  CALL_METHOD_0         0  ''
              254  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 128


def _make_sequence_methods(field_name):

    def len_method(self):
        return len(getattrselffield_name)

    def iter_method(self):
        return iter(getattrselffield_name)

    def getitem_method(self, idx):
        return getattrselffield_name[idx]

    return (
     len_method, iter_method, getitem_method)


class DuplicateExtension(Exception):

    def __init__(self, msg, oid):
        superDuplicateExtensionself.__init__(msg)
        self.oid = oid


class ExtensionNotFound(Exception):

    def __init__(self, msg, oid):
        superExtensionNotFoundself.__init__(msg)
        self.oid = oid


@six.add_metaclass(abc.ABCMeta)
class ExtensionType(object):

    @abc.abstractproperty
    def oid(self):
        """
        Returns the oid associated with the given extension type.
        """
        pass


class Extensions(object):

    def __init__(self, extensions):
        self._extensions = extensions

    def get_extension_for_oid(self, oid):
        for ext in self:
            if ext.oid == oid:
                return ext
        else:
            raise ExtensionNotFound'No {} extension was found'.format(oid)oid

    def get_extension_for_class--- This code section failed: ---

 L. 124         0  LOAD_FAST                'extclass'
                2  LOAD_GLOBAL              UnrecognizedExtension
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 125         8  LOAD_GLOBAL              TypeError

 L. 126        10  LOAD_STR                 "UnrecognizedExtension can't be used with get_extension_for_class because more than one instance of the class may be present."

 L. 125        12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 131        16  LOAD_FAST                'self'
               18  GET_ITER         
             20_0  COME_FROM            34  '34'
               20  FOR_ITER             46  'to 46'
               22  STORE_FAST               'ext'

 L. 132        24  LOAD_GLOBAL              isinstance
               26  LOAD_FAST                'ext'
               28  LOAD_ATTR                value
               30  LOAD_FAST                'extclass'
               32  CALL_FUNCTION_2       2  ''
               34  POP_JUMP_IF_FALSE    20  'to 20'

 L. 133        36  LOAD_FAST                'ext'
               38  ROT_TWO          
               40  POP_TOP          
               42  RETURN_VALUE     
               44  JUMP_BACK            20  'to 20'

 L. 135        46  LOAD_GLOBAL              ExtensionNotFound

 L. 136        48  LOAD_STR                 'No {} extension was found'
               50  LOAD_METHOD              format
               52  LOAD_FAST                'extclass'
               54  CALL_METHOD_1         1  ''
               56  LOAD_FAST                'extclass'
               58  LOAD_ATTR                oid

 L. 135        60  CALL_FUNCTION_2       2  ''
               62  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `None' instruction at offset -1

    __len__, __iter__, __getitem__ = _make_sequence_methods('_extensions')

    def __repr__(self):
        return '<Extensions({})>'.format(self._extensions)


@utils.register_interface(ExtensionType)
class CRLNumber(object):
    oid = ExtensionOID.CRL_NUMBER

    def __init__(self, crl_number):
        if not isinstancecrl_numbersix.integer_types:
            raise TypeError('crl_number must be an integer')
        self._crl_number = crl_number

    def __eq__(self, other):
        if not isinstanceotherCRLNumber:
            return NotImplemented
        return self.crl_number == other.crl_number

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.crl_number)

    def __repr__(self):
        return '<CRLNumber({})>'.format(self.crl_number)

    crl_number = utils.read_only_property('_crl_number')


@utils.register_interface(ExtensionType)
class AuthorityKeyIdentifier(object):
    oid = ExtensionOID.AUTHORITY_KEY_IDENTIFIER

    def __init__--- This code section failed: ---

 L. 183         0  LOAD_FAST                'authority_cert_issuer'
                2  LOAD_CONST               None
                4  <117>                 0  ''

 L. 184         6  LOAD_FAST                'authority_cert_serial_number'
                8  LOAD_CONST               None
               10  <117>                 0  ''

 L. 183        12  COMPARE_OP               !=
               14  POP_JUMP_IF_FALSE    24  'to 24'

 L. 186        16  LOAD_GLOBAL              ValueError

 L. 187        18  LOAD_STR                 'authority_cert_issuer and authority_cert_serial_number must both be present or both None'

 L. 186        20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            14  '14'

 L. 191        24  LOAD_FAST                'authority_cert_issuer'
               26  LOAD_CONST               None
               28  <117>                 1  ''
               30  POP_JUMP_IF_FALSE    66  'to 66'

 L. 192        32  LOAD_GLOBAL              list
               34  LOAD_FAST                'authority_cert_issuer'
               36  CALL_FUNCTION_1       1  ''
               38  STORE_FAST               'authority_cert_issuer'

 L. 193        40  LOAD_GLOBAL              all
               42  LOAD_GENEXPR             '<code_object <genexpr>>'
               44  LOAD_STR                 'AuthorityKeyIdentifier.__init__.<locals>.<genexpr>'
               46  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 194        48  LOAD_FAST                'authority_cert_issuer'

 L. 193        50  GET_ITER         
               52  CALL_FUNCTION_1       1  ''
               54  CALL_FUNCTION_1       1  ''
               56  POP_JUMP_IF_TRUE     66  'to 66'

 L. 196        58  LOAD_GLOBAL              TypeError

 L. 197        60  LOAD_STR                 'authority_cert_issuer must be a list of GeneralName objects'

 L. 196        62  CALL_FUNCTION_1       1  ''
               64  RAISE_VARARGS_1       1  'exception instance'
             66_0  COME_FROM            56  '56'
             66_1  COME_FROM            30  '30'

 L. 201        66  LOAD_FAST                'authority_cert_serial_number'
               68  LOAD_CONST               None
               70  <117>                 1  ''
               72  POP_JUMP_IF_FALSE    94  'to 94'
               74  LOAD_GLOBAL              isinstance

 L. 202        76  LOAD_FAST                'authority_cert_serial_number'
               78  LOAD_GLOBAL              six
               80  LOAD_ATTR                integer_types

 L. 201        82  CALL_FUNCTION_2       2  ''
               84  POP_JUMP_IF_TRUE     94  'to 94'

 L. 204        86  LOAD_GLOBAL              TypeError
               88  LOAD_STR                 'authority_cert_serial_number must be an integer'
               90  CALL_FUNCTION_1       1  ''
               92  RAISE_VARARGS_1       1  'exception instance'
             94_0  COME_FROM            84  '84'
             94_1  COME_FROM            72  '72'

 L. 206        94  LOAD_FAST                'key_identifier'
               96  LOAD_FAST                'self'
               98  STORE_ATTR               _key_identifier

 L. 207       100  LOAD_FAST                'authority_cert_issuer'
              102  LOAD_FAST                'self'
              104  STORE_ATTR               _authority_cert_issuer

 L. 208       106  LOAD_FAST                'authority_cert_serial_number'
              108  LOAD_FAST                'self'
              110  STORE_ATTR               _authority_cert_serial_number

Parse error at or near `None' instruction at offset -1

    @classmethod
    def from_issuer_public_key(cls, public_key):
        digest = _key_identifier_from_public_key(public_key)
        return cls(key_identifier=digest,
          authority_cert_issuer=None,
          authority_cert_serial_number=None)

    @classmethod
    def from_issuer_subject_key_identifier(cls, ski):
        return cls(key_identifier=(ski.digest),
          authority_cert_issuer=None,
          authority_cert_serial_number=None)

    def __repr__(self):
        return '<AuthorityKeyIdentifier(key_identifier={0.key_identifier!r}, authority_cert_issuer={0.authority_cert_issuer}, authority_cert_serial_number={0.authority_cert_serial_number})>'.format(self)

    def __eq__(self, other):
        if not isinstanceotherAuthorityKeyIdentifier:
            return NotImplemented
        return self.key_identifier == other.key_identifier and self.authority_cert_issuer == other.authority_cert_issuer and self.authority_cert_serial_number == other.authority_cert_serial_number

    def __ne__(self, other):
        return not self == other

    def __hash__--- This code section failed: ---

 L. 250         0  LOAD_FAST                'self'
                2  LOAD_ATTR                authority_cert_issuer
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    16  'to 16'

 L. 251        10  LOAD_CONST               None
               12  STORE_FAST               'aci'
               14  JUMP_FORWARD         26  'to 26'
             16_0  COME_FROM             8  '8'

 L. 253        16  LOAD_GLOBAL              tuple
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                authority_cert_issuer
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'aci'
             26_0  COME_FROM            14  '14'

 L. 254        26  LOAD_GLOBAL              hash

 L. 255        28  LOAD_FAST                'self'
               30  LOAD_ATTR                key_identifier
               32  LOAD_FAST                'aci'
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                authority_cert_serial_number
               38  BUILD_TUPLE_3         3 

 L. 254        40  CALL_FUNCTION_1       1  ''
               42  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    key_identifier = utils.read_only_property('_key_identifier')
    authority_cert_issuer = utils.read_only_property('_authority_cert_issuer')
    authority_cert_serial_number = utils.read_only_property('_authority_cert_serial_number')


@utils.register_interface(ExtensionType)
class SubjectKeyIdentifier(object):
    oid = ExtensionOID.SUBJECT_KEY_IDENTIFIER

    def __init__(self, digest):
        self._digest = digest

    @classmethod
    def from_public_key(cls, public_key):
        return cls(_key_identifier_from_public_key(public_key))

    digest = utils.read_only_property('_digest')

    def __repr__(self):
        return '<SubjectKeyIdentifier(digest={0!r})>'.format(self.digest)

    def __eq__(self, other):
        if not isinstanceotherSubjectKeyIdentifier:
            return NotImplemented
        return constant_time.bytes_eqself.digestother.digest

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.digest)


@utils.register_interface(ExtensionType)
class AuthorityInformationAccess(object):
    oid = ExtensionOID.AUTHORITY_INFORMATION_ACCESS

    def __init__(self, descriptions):
        descriptions = list(descriptions)
        if not all((isinstancexAccessDescription for x in descriptions)):
            raise TypeError('Every item in the descriptions list must be an AccessDescription')
        self._descriptions = descriptions

    __len__, __iter__, __getitem__ = _make_sequence_methods('_descriptions')

    def __repr__(self):
        return '<AuthorityInformationAccess({})>'.format(self._descriptions)

    def __eq__(self, other):
        if not isinstanceotherAuthorityInformationAccess:
            return NotImplemented
        return self._descriptions == other._descriptions

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(tuple(self._descriptions))


@utils.register_interface(ExtensionType)
class SubjectInformationAccess(object):
    oid = ExtensionOID.SUBJECT_INFORMATION_ACCESS

    def __init__(self, descriptions):
        descriptions = list(descriptions)
        if not all((isinstancexAccessDescription for x in descriptions)):
            raise TypeError('Every item in the descriptions list must be an AccessDescription')
        self._descriptions = descriptions

    __len__, __iter__, __getitem__ = _make_sequence_methods('_descriptions')

    def __repr__(self):
        return '<SubjectInformationAccess({})>'.format(self._descriptions)

    def __eq__(self, other):
        if not isinstanceotherSubjectInformationAccess:
            return NotImplemented
        return self._descriptions == other._descriptions

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(tuple(self._descriptions))


class AccessDescription(object):

    def __init__(self, access_method, access_location):
        if not isinstanceaccess_methodObjectIdentifier:
            raise TypeError('access_method must be an ObjectIdentifier')
        if not isinstanceaccess_locationGeneralName:
            raise TypeError('access_location must be a GeneralName')
        self._access_method = access_method
        self._access_location = access_location

    def __repr__(self):
        return '<AccessDescription(access_method={0.access_method}, access_location={0.access_location})>'.format(self)

    def __eq__(self, other):
        if not isinstanceotherAccessDescription:
            return NotImplemented
        return self.access_method == other.access_method and self.access_location == other.access_location

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.access_method, self.access_location))

    access_method = utils.read_only_property('_access_method')
    access_location = utils.read_only_property('_access_location')


@utils.register_interface(ExtensionType)
class BasicConstraints(object):
    oid = ExtensionOID.BASIC_CONSTRAINTS

    def __init__--- This code section failed: ---

 L. 399         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'ca'
                4  LOAD_GLOBAL              bool
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     18  'to 18'

 L. 400        10  LOAD_GLOBAL              TypeError
               12  LOAD_STR                 'ca must be a boolean value'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 402        18  LOAD_FAST                'path_length'
               20  LOAD_CONST               None
               22  <117>                 1  ''
               24  POP_JUMP_IF_FALSE    38  'to 38'
               26  LOAD_FAST                'ca'
               28  POP_JUMP_IF_TRUE     38  'to 38'

 L. 403        30  LOAD_GLOBAL              ValueError
               32  LOAD_STR                 'path_length must be None when ca is False'
               34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            28  '28'
             38_1  COME_FROM            24  '24'

 L. 405        38  LOAD_FAST                'path_length'
               40  LOAD_CONST               None
               42  <117>                 1  ''
               44  POP_JUMP_IF_FALSE    74  'to 74'

 L. 406        46  LOAD_GLOBAL              isinstance
               48  LOAD_FAST                'path_length'
               50  LOAD_GLOBAL              six
               52  LOAD_ATTR                integer_types
               54  CALL_FUNCTION_2       2  ''

 L. 405        56  POP_JUMP_IF_FALSE    66  'to 66'

 L. 406        58  LOAD_FAST                'path_length'
               60  LOAD_CONST               0
               62  COMPARE_OP               <

 L. 405        64  POP_JUMP_IF_FALSE    74  'to 74'
             66_0  COME_FROM            56  '56'

 L. 408        66  LOAD_GLOBAL              TypeError

 L. 409        68  LOAD_STR                 'path_length must be a non-negative integer or None'

 L. 408        70  CALL_FUNCTION_1       1  ''
               72  RAISE_VARARGS_1       1  'exception instance'
             74_0  COME_FROM            64  '64'
             74_1  COME_FROM            44  '44'

 L. 412        74  LOAD_FAST                'ca'
               76  LOAD_FAST                'self'
               78  STORE_ATTR               _ca

 L. 413        80  LOAD_FAST                'path_length'
               82  LOAD_FAST                'self'
               84  STORE_ATTR               _path_length

Parse error at or near `<117>' instruction at offset 22

    ca = utils.read_only_property('_ca')
    path_length = utils.read_only_property('_path_length')

    def __repr__(self):
        return '<BasicConstraints(ca={0.ca}, path_length={0.path_length})>'.format(self)

    def __eq__(self, other):
        if not isinstanceotherBasicConstraints:
            return NotImplemented
        return self.ca == other.ca and self.path_length == other.path_length

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.ca, self.path_length))


@utils.register_interface(ExtensionType)
class DeltaCRLIndicator(object):
    oid = ExtensionOID.DELTA_CRL_INDICATOR

    def __init__(self, crl_number):
        if not isinstancecrl_numbersix.integer_types:
            raise TypeError('crl_number must be an integer')
        self._crl_number = crl_number

    crl_number = utils.read_only_property('_crl_number')

    def __eq__(self, other):
        if not isinstanceotherDeltaCRLIndicator:
            return NotImplemented
        return self.crl_number == other.crl_number

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.crl_number)

    def __repr__(self):
        return '<DeltaCRLIndicator(crl_number={0.crl_number})>'.format(self)


@utils.register_interface(ExtensionType)
class CRLDistributionPoints(object):
    oid = ExtensionOID.CRL_DISTRIBUTION_POINTS

    def __init__(self, distribution_points):
        distribution_points = list(distribution_points)
        if not all((isinstancexDistributionPoint for x in distribution_points)):
            raise TypeError('distribution_points must be a list of DistributionPoint objects')
        self._distribution_points = distribution_points

    __len__, __iter__, __getitem__ = _make_sequence_methods('_distribution_points')

    def __repr__(self):
        return '<CRLDistributionPoints({})>'.format(self._distribution_points)

    def __eq__(self, other):
        if not isinstanceotherCRLDistributionPoints:
            return NotImplemented
        return self._distribution_points == other._distribution_points

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(tuple(self._distribution_points))


@utils.register_interface(ExtensionType)
class FreshestCRL(object):
    oid = ExtensionOID.FRESHEST_CRL

    def __init__(self, distribution_points):
        distribution_points = list(distribution_points)
        if not all((isinstancexDistributionPoint for x in distribution_points)):
            raise TypeError('distribution_points must be a list of DistributionPoint objects')
        self._distribution_points = distribution_points

    __len__, __iter__, __getitem__ = _make_sequence_methods('_distribution_points')

    def __repr__(self):
        return '<FreshestCRL({})>'.format(self._distribution_points)

    def __eq__(self, other):
        if not isinstanceotherFreshestCRL:
            return NotImplemented
        return self._distribution_points == other._distribution_points

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(tuple(self._distribution_points))


class DistributionPoint(object):

    def __init__--- This code section failed: ---

 L. 538         0  LOAD_FAST                'full_name'
                2  POP_JUMP_IF_FALSE    16  'to 16'
                4  LOAD_FAST                'relative_name'
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 539         8  LOAD_GLOBAL              ValueError

 L. 540        10  LOAD_STR                 'You cannot provide both full_name and relative_name, at least one must be None.'

 L. 539        12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'
             16_1  COME_FROM             2  '2'

 L. 544        16  LOAD_FAST                'full_name'
               18  POP_JUMP_IF_FALSE    54  'to 54'

 L. 545        20  LOAD_GLOBAL              list
               22  LOAD_FAST                'full_name'
               24  CALL_FUNCTION_1       1  ''
               26  STORE_FAST               'full_name'

 L. 546        28  LOAD_GLOBAL              all
               30  LOAD_GENEXPR             '<code_object <genexpr>>'
               32  LOAD_STR                 'DistributionPoint.__init__.<locals>.<genexpr>'
               34  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               36  LOAD_FAST                'full_name'
               38  GET_ITER         
               40  CALL_FUNCTION_1       1  ''
               42  CALL_FUNCTION_1       1  ''
               44  POP_JUMP_IF_TRUE     54  'to 54'

 L. 547        46  LOAD_GLOBAL              TypeError

 L. 548        48  LOAD_STR                 'full_name must be a list of GeneralName objects'

 L. 547        50  CALL_FUNCTION_1       1  ''
               52  RAISE_VARARGS_1       1  'exception instance'
             54_0  COME_FROM            44  '44'
             54_1  COME_FROM            18  '18'

 L. 551        54  LOAD_FAST                'relative_name'
               56  POP_JUMP_IF_FALSE    76  'to 76'

 L. 552        58  LOAD_GLOBAL              isinstance
               60  LOAD_FAST                'relative_name'
               62  LOAD_GLOBAL              RelativeDistinguishedName
               64  CALL_FUNCTION_2       2  ''
               66  POP_JUMP_IF_TRUE     76  'to 76'

 L. 553        68  LOAD_GLOBAL              TypeError

 L. 554        70  LOAD_STR                 'relative_name must be a RelativeDistinguishedName'

 L. 553        72  CALL_FUNCTION_1       1  ''
               74  RAISE_VARARGS_1       1  'exception instance'
             76_0  COME_FROM            66  '66'
             76_1  COME_FROM            56  '56'

 L. 557        76  LOAD_FAST                'crl_issuer'
               78  POP_JUMP_IF_FALSE   114  'to 114'

 L. 558        80  LOAD_GLOBAL              list
               82  LOAD_FAST                'crl_issuer'
               84  CALL_FUNCTION_1       1  ''
               86  STORE_FAST               'crl_issuer'

 L. 559        88  LOAD_GLOBAL              all
               90  LOAD_GENEXPR             '<code_object <genexpr>>'
               92  LOAD_STR                 'DistributionPoint.__init__.<locals>.<genexpr>'
               94  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               96  LOAD_FAST                'crl_issuer'
               98  GET_ITER         
              100  CALL_FUNCTION_1       1  ''
              102  CALL_FUNCTION_1       1  ''
              104  POP_JUMP_IF_TRUE    114  'to 114'

 L. 560       106  LOAD_GLOBAL              TypeError

 L. 561       108  LOAD_STR                 'crl_issuer must be None or a list of general names'

 L. 560       110  CALL_FUNCTION_1       1  ''
              112  RAISE_VARARGS_1       1  'exception instance'
            114_0  COME_FROM           104  '104'
            114_1  COME_FROM            78  '78'

 L. 564       114  LOAD_FAST                'reasons'
              116  POP_JUMP_IF_FALSE   154  'to 154'

 L. 565       118  LOAD_GLOBAL              isinstance
              120  LOAD_FAST                'reasons'
              122  LOAD_GLOBAL              frozenset
              124  CALL_FUNCTION_2       2  ''

 L. 564       126  POP_JUMP_IF_FALSE   146  'to 146'

 L. 566       128  LOAD_GLOBAL              all
              130  LOAD_GENEXPR             '<code_object <genexpr>>'
              132  LOAD_STR                 'DistributionPoint.__init__.<locals>.<genexpr>'
              134  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              136  LOAD_FAST                'reasons'
              138  GET_ITER         
              140  CALL_FUNCTION_1       1  ''
              142  CALL_FUNCTION_1       1  ''

 L. 564       144  POP_JUMP_IF_TRUE    154  'to 154'
            146_0  COME_FROM           126  '126'

 L. 568       146  LOAD_GLOBAL              TypeError
              148  LOAD_STR                 'reasons must be None or frozenset of ReasonFlags'
              150  CALL_FUNCTION_1       1  ''
              152  RAISE_VARARGS_1       1  'exception instance'
            154_0  COME_FROM           144  '144'
            154_1  COME_FROM           116  '116'

 L. 570       154  LOAD_FAST                'reasons'
              156  POP_JUMP_IF_FALSE   186  'to 186'

 L. 571       158  LOAD_GLOBAL              ReasonFlags
              160  LOAD_ATTR                unspecified
              162  LOAD_FAST                'reasons'
              164  <118>                 0  ''

 L. 570       166  POP_JUMP_IF_TRUE    178  'to 178'

 L. 572       168  LOAD_GLOBAL              ReasonFlags
              170  LOAD_ATTR                remove_from_crl
              172  LOAD_FAST                'reasons'
              174  <118>                 0  ''

 L. 570       176  POP_JUMP_IF_FALSE   186  'to 186'
            178_0  COME_FROM           166  '166'

 L. 574       178  LOAD_GLOBAL              ValueError

 L. 575       180  LOAD_STR                 'unspecified and remove_from_crl are not valid reasons in a DistributionPoint'

 L. 574       182  CALL_FUNCTION_1       1  ''
              184  RAISE_VARARGS_1       1  'exception instance'
            186_0  COME_FROM           176  '176'
            186_1  COME_FROM           156  '156'

 L. 579       186  LOAD_FAST                'reasons'
              188  POP_JUMP_IF_FALSE   210  'to 210'
              190  LOAD_FAST                'crl_issuer'
              192  POP_JUMP_IF_TRUE    210  'to 210'
              194  LOAD_FAST                'full_name'
              196  POP_JUMP_IF_TRUE    210  'to 210'
              198  LOAD_FAST                'relative_name'
              200  POP_JUMP_IF_TRUE    210  'to 210'

 L. 580       202  LOAD_GLOBAL              ValueError

 L. 581       204  LOAD_STR                 'You must supply crl_issuer, full_name, or relative_name when reasons is not None'

 L. 580       206  CALL_FUNCTION_1       1  ''
              208  RAISE_VARARGS_1       1  'exception instance'
            210_0  COME_FROM           200  '200'
            210_1  COME_FROM           196  '196'
            210_2  COME_FROM           192  '192'
            210_3  COME_FROM           188  '188'

 L. 585       210  LOAD_FAST                'full_name'
              212  LOAD_FAST                'self'
              214  STORE_ATTR               _full_name

 L. 586       216  LOAD_FAST                'relative_name'
              218  LOAD_FAST                'self'
              220  STORE_ATTR               _relative_name

 L. 587       222  LOAD_FAST                'reasons'
              224  LOAD_FAST                'self'
              226  STORE_ATTR               _reasons

 L. 588       228  LOAD_FAST                'crl_issuer'
              230  LOAD_FAST                'self'
              232  STORE_ATTR               _crl_issuer

Parse error at or near `<118>' instruction at offset 164

    def __repr__(self):
        return '<DistributionPoint(full_name={0.full_name}, relative_name={0.relative_name}, reasons={0.reasons}, crl_issuer={0.crl_issuer})>'.format(self)

    def __eq__(self, other):
        if not isinstanceotherDistributionPoint:
            return NotImplemented
        return self.full_name == other.full_name and self.relative_name == other.relative_name and self.reasons == other.reasons and self.crl_issuer == other.crl_issuer

    def __ne__(self, other):
        return not self == other

    def __hash__--- This code section failed: ---

 L. 612         0  LOAD_FAST                'self'
                2  LOAD_ATTR                full_name
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    22  'to 22'

 L. 613        10  LOAD_GLOBAL              tuple
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                full_name
               16  CALL_FUNCTION_1       1  ''
               18  STORE_FAST               'fn'
               20  JUMP_FORWARD         26  'to 26'
             22_0  COME_FROM             8  '8'

 L. 615        22  LOAD_CONST               None
               24  STORE_FAST               'fn'
             26_0  COME_FROM            20  '20'

 L. 617        26  LOAD_FAST                'self'
               28  LOAD_ATTR                crl_issuer
               30  LOAD_CONST               None
               32  <117>                 1  ''
               34  POP_JUMP_IF_FALSE    48  'to 48'

 L. 618        36  LOAD_GLOBAL              tuple
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                crl_issuer
               42  CALL_FUNCTION_1       1  ''
               44  STORE_FAST               'crl_issuer'
               46  JUMP_FORWARD         52  'to 52'
             48_0  COME_FROM            34  '34'

 L. 620        48  LOAD_CONST               None
               50  STORE_FAST               'crl_issuer'
             52_0  COME_FROM            46  '46'

 L. 622        52  LOAD_GLOBAL              hash
               54  LOAD_FAST                'fn'
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                relative_name
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                reasons
               64  LOAD_FAST                'crl_issuer'
               66  BUILD_TUPLE_4         4 
               68  CALL_FUNCTION_1       1  ''
               70  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    full_name = utils.read_only_property('_full_name')
    relative_name = utils.read_only_property('_relative_name')
    reasons = utils.read_only_property('_reasons')
    crl_issuer = utils.read_only_property('_crl_issuer')


class ReasonFlags(Enum):
    unspecified = 'unspecified'
    key_compromise = 'keyCompromise'
    ca_compromise = 'cACompromise'
    affiliation_changed = 'affiliationChanged'
    superseded = 'superseded'
    cessation_of_operation = 'cessationOfOperation'
    certificate_hold = 'certificateHold'
    privilege_withdrawn = 'privilegeWithdrawn'
    aa_compromise = 'aACompromise'
    remove_from_crl = 'removeFromCRL'


@utils.register_interface(ExtensionType)
class PolicyConstraints(object):
    oid = ExtensionOID.POLICY_CONSTRAINTS

    def __init__--- This code section failed: ---

 L. 648         0  LOAD_FAST                'require_explicit_policy'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    28  'to 28'
                8  LOAD_GLOBAL              isinstance

 L. 649        10  LOAD_FAST                'require_explicit_policy'
               12  LOAD_GLOBAL              six
               14  LOAD_ATTR                integer_types

 L. 648        16  CALL_FUNCTION_2       2  ''
               18  POP_JUMP_IF_TRUE     28  'to 28'

 L. 651        20  LOAD_GLOBAL              TypeError

 L. 652        22  LOAD_STR                 'require_explicit_policy must be a non-negative integer or None'

 L. 651        24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            18  '18'
             28_1  COME_FROM             6  '6'

 L. 656        28  LOAD_FAST                'inhibit_policy_mapping'
               30  LOAD_CONST               None
               32  <117>                 1  ''
               34  POP_JUMP_IF_FALSE    56  'to 56'
               36  LOAD_GLOBAL              isinstance

 L. 657        38  LOAD_FAST                'inhibit_policy_mapping'
               40  LOAD_GLOBAL              six
               42  LOAD_ATTR                integer_types

 L. 656        44  CALL_FUNCTION_2       2  ''
               46  POP_JUMP_IF_TRUE     56  'to 56'

 L. 659        48  LOAD_GLOBAL              TypeError

 L. 660        50  LOAD_STR                 'inhibit_policy_mapping must be a non-negative integer or None'

 L. 659        52  CALL_FUNCTION_1       1  ''
               54  RAISE_VARARGS_1       1  'exception instance'
             56_0  COME_FROM            46  '46'
             56_1  COME_FROM            34  '34'

 L. 663        56  LOAD_FAST                'inhibit_policy_mapping'
               58  LOAD_CONST               None
               60  <117>                 0  ''
               62  POP_JUMP_IF_FALSE    80  'to 80'
               64  LOAD_FAST                'require_explicit_policy'
               66  LOAD_CONST               None
               68  <117>                 0  ''
               70  POP_JUMP_IF_FALSE    80  'to 80'

 L. 664        72  LOAD_GLOBAL              ValueError

 L. 665        74  LOAD_STR                 'At least one of require_explicit_policy and inhibit_policy_mapping must not be None'

 L. 664        76  CALL_FUNCTION_1       1  ''
               78  RAISE_VARARGS_1       1  'exception instance'
             80_0  COME_FROM            70  '70'
             80_1  COME_FROM            62  '62'

 L. 669        80  LOAD_FAST                'require_explicit_policy'
               82  LOAD_FAST                'self'
               84  STORE_ATTR               _require_explicit_policy

 L. 670        86  LOAD_FAST                'inhibit_policy_mapping'
               88  LOAD_FAST                'self'
               90  STORE_ATTR               _inhibit_policy_mapping

Parse error at or near `None' instruction at offset -1

    def __repr__(self):
        return '<PolicyConstraints(require_explicit_policy={0.require_explicit_policy}, inhibit_policy_mapping={0.inhibit_policy_mapping})>'.format(self)

    def __eq__(self, other):
        if not isinstanceotherPolicyConstraints:
            return NotImplemented
        return self.require_explicit_policy == other.require_explicit_policy and self.inhibit_policy_mapping == other.inhibit_policy_mapping

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((
         self.require_explicit_policy, self.inhibit_policy_mapping))

    require_explicit_policy = utils.read_only_property('_require_explicit_policy')
    inhibit_policy_mapping = utils.read_only_property('_inhibit_policy_mapping')


@utils.register_interface(ExtensionType)
class CertificatePolicies(object):
    oid = ExtensionOID.CERTIFICATE_POLICIES

    def __init__(self, policies):
        policies = list(policies)
        if not all((isinstancexPolicyInformation for x in policies)):
            raise TypeError('Every item in the policies list must be a PolicyInformation')
        self._policies = policies

    __len__, __iter__, __getitem__ = _make_sequence_methods('_policies')

    def __repr__(self):
        return '<CertificatePolicies({})>'.format(self._policies)

    def __eq__(self, other):
        if not isinstanceotherCertificatePolicies:
            return NotImplemented
        return self._policies == other._policies

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(tuple(self._policies))


class PolicyInformation(object):

    def __init__(self, policy_identifier, policy_qualifiers):
        if not isinstancepolicy_identifierObjectIdentifier:
            raise TypeError('policy_identifier must be an ObjectIdentifier')
        self._policy_identifier = policy_identifier
        if policy_qualifiers:
            policy_qualifiers = list(policy_qualifiers)
            if not all((isinstancex(six.text_type, UserNotice) for x in policy_qualifiers)):
                raise TypeError('policy_qualifiers must be a list of strings and/or UserNotice objects or None')
        self._policy_qualifiers = policy_qualifiers

    def __repr__(self):
        return '<PolicyInformation(policy_identifier={0.policy_identifier}, policy_qualifiers={0.policy_qualifiers})>'.format(self)

    def __eq__(self, other):
        if not isinstanceotherPolicyInformation:
            return NotImplemented
        return self.policy_identifier == other.policy_identifier and self.policy_qualifiers == other.policy_qualifiers

    def __ne__(self, other):
        return not self == other

    def __hash__--- This code section failed: ---

 L. 775         0  LOAD_FAST                'self'
                2  LOAD_ATTR                policy_qualifiers
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    22  'to 22'

 L. 776        10  LOAD_GLOBAL              tuple
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                policy_qualifiers
               16  CALL_FUNCTION_1       1  ''
               18  STORE_FAST               'pq'
               20  JUMP_FORWARD         26  'to 26'
             22_0  COME_FROM             8  '8'

 L. 778        22  LOAD_CONST               None
               24  STORE_FAST               'pq'
             26_0  COME_FROM            20  '20'

 L. 780        26  LOAD_GLOBAL              hash
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                policy_identifier
               32  LOAD_FAST                'pq'
               34  BUILD_TUPLE_2         2 
               36  CALL_FUNCTION_1       1  ''
               38  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    policy_identifier = utils.read_only_property('_policy_identifier')
    policy_qualifiers = utils.read_only_property('_policy_qualifiers')


class UserNotice(object):

    def __init__(self, notice_reference, explicit_text):
        if notice_reference:
            if not isinstancenotice_referenceNoticeReference:
                raise TypeError('notice_reference must be None or a NoticeReference')
        self._notice_reference = notice_reference
        self._explicit_text = explicit_text

    def __repr__(self):
        return '<UserNotice(notice_reference={0.notice_reference}, explicit_text={0.explicit_text!r})>'.format(self)

    def __eq__(self, other):
        if not isinstanceotherUserNotice:
            return NotImplemented
        return self.notice_reference == other.notice_reference and self.explicit_text == other.explicit_text

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.notice_reference, self.explicit_text))

    notice_reference = utils.read_only_property('_notice_reference')
    explicit_text = utils.read_only_property('_explicit_text')


class NoticeReference(object):

    def __init__(self, organization, notice_numbers):
        self._organization = organization
        notice_numbers = list(notice_numbers)
        if not all((isinstancexint for x in notice_numbers)):
            raise TypeError('notice_numbers must be a list of integers')
        self._notice_numbers = notice_numbers

    def __repr__(self):
        return '<NoticeReference(organization={0.organization!r}, notice_numbers={0.notice_numbers})>'.format(self)

    def __eq__(self, other):
        if not isinstanceotherNoticeReference:
            return NotImplemented
        return self.organization == other.organization and self.notice_numbers == other.notice_numbers

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.organization, tuple(self.notice_numbers)))

    organization = utils.read_only_property('_organization')
    notice_numbers = utils.read_only_property('_notice_numbers')


@utils.register_interface(ExtensionType)
class ExtendedKeyUsage(object):
    oid = ExtensionOID.EXTENDED_KEY_USAGE

    def __init__(self, usages):
        usages = list(usages)
        if not all((isinstancexObjectIdentifier for x in usages)):
            raise TypeError('Every item in the usages list must be an ObjectIdentifier')
        self._usages = usages

    __len__, __iter__, __getitem__ = _make_sequence_methods('_usages')

    def __repr__(self):
        return '<ExtendedKeyUsage({})>'.format(self._usages)

    def __eq__(self, other):
        if not isinstanceotherExtendedKeyUsage:
            return NotImplemented
        return self._usages == other._usages

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(tuple(self._usages))


@utils.register_interface(ExtensionType)
class OCSPNoCheck(object):
    oid = ExtensionOID.OCSP_NO_CHECK

    def __eq__(self, other):
        if not isinstanceotherOCSPNoCheck:
            return NotImplemented
        return True

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(OCSPNoCheck)

    def __repr__(self):
        return '<OCSPNoCheck()>'


@utils.register_interface(ExtensionType)
class PrecertPoison(object):
    oid = ExtensionOID.PRECERT_POISON

    def __eq__(self, other):
        if not isinstanceotherPrecertPoison:
            return NotImplemented
        return True

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(PrecertPoison)

    def __repr__(self):
        return '<PrecertPoison()>'


@utils.register_interface(ExtensionType)
class TLSFeature(object):
    oid = ExtensionOID.TLS_FEATURE

    def __init__(self, features):
        features = list(features)
        if not all((isinstancexTLSFeatureType for x in features)) or len(features) == 0:
            raise TypeError('features must be a list of elements from the TLSFeatureType enum')
        self._features = features

    __len__, __iter__, __getitem__ = _make_sequence_methods('_features')

    def __repr__(self):
        return '<TLSFeature(features={0._features})>'.format(self)

    def __eq__(self, other):
        if not isinstanceotherTLSFeature:
            return NotImplemented
        return self._features == other._features

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(tuple(self._features))


class TLSFeatureType(Enum):
    status_request = 5
    status_request_v2 = 17


_TLS_FEATURE_TYPE_TO_ENUM = {x:x.value for x in TLSFeatureType}

@utils.register_interface(ExtensionType)
class InhibitAnyPolicy(object):
    oid = ExtensionOID.INHIBIT_ANY_POLICY

    def __init__(self, skip_certs):
        if not isinstanceskip_certssix.integer_types:
            raise TypeError('skip_certs must be an integer')
        if skip_certs < 0:
            raise ValueError('skip_certs must be a non-negative integer')
        self._skip_certs = skip_certs

    def __repr__(self):
        return '<InhibitAnyPolicy(skip_certs={0.skip_certs})>'.format(self)

    def __eq__(self, other):
        if not isinstanceotherInhibitAnyPolicy:
            return NotImplemented
        return self.skip_certs == other.skip_certs

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.skip_certs)

    skip_certs = utils.read_only_property('_skip_certs')


@utils.register_interface(ExtensionType)
class KeyUsage(object):
    oid = ExtensionOID.KEY_USAGE

    def __init__(self, digital_signature, content_commitment, key_encipherment, data_encipherment, key_agreement, key_cert_sign, crl_sign, encipher_only, decipher_only):
        if not key_agreement:
            if encipher_only or decipher_only:
                raise ValueError('encipher_only and decipher_only can only be true when key_agreement is true')
        self._digital_signature = digital_signature
        self._content_commitment = content_commitment
        self._key_encipherment = key_encipherment
        self._data_encipherment = data_encipherment
        self._key_agreement = key_agreement
        self._key_cert_sign = key_cert_sign
        self._crl_sign = crl_sign
        self._encipher_only = encipher_only
        self._decipher_only = decipher_only

    digital_signature = utils.read_only_property('_digital_signature')
    content_commitment = utils.read_only_property('_content_commitment')
    key_encipherment = utils.read_only_property('_key_encipherment')
    data_encipherment = utils.read_only_property('_data_encipherment')
    key_agreement = utils.read_only_property('_key_agreement')
    key_cert_sign = utils.read_only_property('_key_cert_sign')
    crl_sign = utils.read_only_property('_crl_sign')

    @property
    def encipher_only(self):
        if not self.key_agreement:
            raise ValueError('encipher_only is undefined unless key_agreement is true')
        else:
            return self._encipher_only

    @property
    def decipher_only(self):
        if not self.key_agreement:
            raise ValueError('decipher_only is undefined unless key_agreement is true')
        else:
            return self._decipher_only

    def __repr__--- This code section failed: ---

 L.1067         0  SETUP_FINALLY        18  'to 18'

 L.1068         2  LOAD_FAST                'self'
                4  LOAD_ATTR                encipher_only
                6  STORE_FAST               'encipher_only'

 L.1069         8  LOAD_FAST                'self'
               10  LOAD_ATTR                decipher_only
               12  STORE_FAST               'decipher_only'
               14  POP_BLOCK        
               16  JUMP_FORWARD         44  'to 44'
             18_0  COME_FROM_FINALLY     0  '0'

 L.1070        18  DUP_TOP          
               20  LOAD_GLOBAL              ValueError
               22  <121>                42  ''
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L.1074        30  LOAD_CONST               False
               32  STORE_FAST               'encipher_only'

 L.1075        34  LOAD_CONST               False
               36  STORE_FAST               'decipher_only'
               38  POP_EXCEPT       
               40  JUMP_FORWARD         44  'to 44'
               42  <48>             
             44_0  COME_FROM            40  '40'
             44_1  COME_FROM            16  '16'

 L.1078        44  LOAD_STR                 '<KeyUsage(digital_signature={0.digital_signature}, content_commitment={0.content_commitment}, key_encipherment={0.key_encipherment}, data_encipherment={0.data_encipherment}, key_agreement={0.key_agreement}, key_cert_sign={0.key_cert_sign}, crl_sign={0.crl_sign}, encipher_only={1}, decipher_only={2})>'

 L.1077        46  LOAD_METHOD              format

 L.1085        48  LOAD_FAST                'self'
               50  LOAD_FAST                'encipher_only'
               52  LOAD_FAST                'decipher_only'

 L.1077        54  CALL_METHOD_3         3  ''
               56  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 22

    def __eq__(self, other):
        if not isinstanceotherKeyUsage:
            return NotImplemented
        return self.digital_signature == other.digital_signature and self.content_commitment == other.content_commitment and self.key_encipherment == other.key_encipherment and self.data_encipherment == other.data_encipherment and self.key_agreement == other.key_agreement and self.key_cert_sign == other.key_cert_sign and self.crl_sign == other.crl_sign and self._encipher_only == other._encipher_only and self._decipher_only == other._decipher_only

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((
         self.digital_signature,
         self.content_commitment,
         self.key_encipherment,
         self.data_encipherment,
         self.key_agreement,
         self.key_cert_sign,
         self.crl_sign,
         self._encipher_only,
         self._decipher_only))


@utils.register_interface(ExtensionType)
class NameConstraints(object):
    oid = ExtensionOID.NAME_CONSTRAINTS

    def __init__--- This code section failed: ---

 L.1127         0  LOAD_FAST                'permitted_subtrees'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    52  'to 52'

 L.1128         8  LOAD_GLOBAL              list
               10  LOAD_FAST                'permitted_subtrees'
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'permitted_subtrees'

 L.1129        16  LOAD_GLOBAL              all
               18  LOAD_GENEXPR             '<code_object <genexpr>>'
               20  LOAD_STR                 'NameConstraints.__init__.<locals>.<genexpr>'
               22  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               24  LOAD_FAST                'permitted_subtrees'
               26  GET_ITER         
               28  CALL_FUNCTION_1       1  ''
               30  CALL_FUNCTION_1       1  ''
               32  POP_JUMP_IF_TRUE     42  'to 42'

 L.1130        34  LOAD_GLOBAL              TypeError

 L.1131        36  LOAD_STR                 'permitted_subtrees must be a list of GeneralName objects or None'

 L.1130        38  CALL_FUNCTION_1       1  ''
               40  RAISE_VARARGS_1       1  'exception instance'
             42_0  COME_FROM            32  '32'

 L.1135        42  LOAD_FAST                'self'
               44  LOAD_METHOD              _validate_ip_name
               46  LOAD_FAST                'permitted_subtrees'
               48  CALL_METHOD_1         1  ''
               50  POP_TOP          
             52_0  COME_FROM             6  '6'

 L.1137        52  LOAD_FAST                'excluded_subtrees'
               54  LOAD_CONST               None
               56  <117>                 1  ''
               58  POP_JUMP_IF_FALSE   104  'to 104'

 L.1138        60  LOAD_GLOBAL              list
               62  LOAD_FAST                'excluded_subtrees'
               64  CALL_FUNCTION_1       1  ''
               66  STORE_FAST               'excluded_subtrees'

 L.1139        68  LOAD_GLOBAL              all
               70  LOAD_GENEXPR             '<code_object <genexpr>>'
               72  LOAD_STR                 'NameConstraints.__init__.<locals>.<genexpr>'
               74  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               76  LOAD_FAST                'excluded_subtrees'
               78  GET_ITER         
               80  CALL_FUNCTION_1       1  ''
               82  CALL_FUNCTION_1       1  ''
               84  POP_JUMP_IF_TRUE     94  'to 94'

 L.1140        86  LOAD_GLOBAL              TypeError

 L.1141        88  LOAD_STR                 'excluded_subtrees must be a list of GeneralName objects or None'

 L.1140        90  CALL_FUNCTION_1       1  ''
               92  RAISE_VARARGS_1       1  'exception instance'
             94_0  COME_FROM            84  '84'

 L.1145        94  LOAD_FAST                'self'
               96  LOAD_METHOD              _validate_ip_name
               98  LOAD_FAST                'excluded_subtrees'
              100  CALL_METHOD_1         1  ''
              102  POP_TOP          
            104_0  COME_FROM            58  '58'

 L.1147       104  LOAD_FAST                'permitted_subtrees'
              106  LOAD_CONST               None
              108  <117>                 0  ''
              110  POP_JUMP_IF_FALSE   128  'to 128'
              112  LOAD_FAST                'excluded_subtrees'
              114  LOAD_CONST               None
              116  <117>                 0  ''
              118  POP_JUMP_IF_FALSE   128  'to 128'

 L.1148       120  LOAD_GLOBAL              ValueError

 L.1149       122  LOAD_STR                 'At least one of permitted_subtrees and excluded_subtrees must not be None'

 L.1148       124  CALL_FUNCTION_1       1  ''
              126  RAISE_VARARGS_1       1  'exception instance'
            128_0  COME_FROM           118  '118'
            128_1  COME_FROM           110  '110'

 L.1153       128  LOAD_FAST                'permitted_subtrees'
              130  LOAD_FAST                'self'
              132  STORE_ATTR               _permitted_subtrees

 L.1154       134  LOAD_FAST                'excluded_subtrees'
              136  LOAD_FAST                'self'
              138  STORE_ATTR               _excluded_subtrees

Parse error at or near `None' instruction at offset -1

    def __eq__(self, other):
        if not isinstanceotherNameConstraints:
            return NotImplemented
        return self.excluded_subtrees == other.excluded_subtrees and self.permitted_subtrees == other.permitted_subtrees

    def __ne__(self, other):
        return not self == other

    def _validate_ip_name(self, tree):
        if any((isinstancenameIPAddress and not isinstancename.value(ipaddress.IPv4Network, ipaddress.IPv6Network) for name in tree)):
            raise TypeError('IPAddress name constraints must be an IPv4Network or IPv6Network object')

    def __repr__(self):
        return '<NameConstraints(permitted_subtrees={0.permitted_subtrees}, excluded_subtrees={0.excluded_subtrees})>'.format(self)

    def __hash__--- This code section failed: ---

 L.1188         0  LOAD_FAST                'self'
                2  LOAD_ATTR                permitted_subtrees
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    22  'to 22'

 L.1189        10  LOAD_GLOBAL              tuple
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                permitted_subtrees
               16  CALL_FUNCTION_1       1  ''
               18  STORE_FAST               'ps'
               20  JUMP_FORWARD         26  'to 26'
             22_0  COME_FROM             8  '8'

 L.1191        22  LOAD_CONST               None
               24  STORE_FAST               'ps'
             26_0  COME_FROM            20  '20'

 L.1193        26  LOAD_FAST                'self'
               28  LOAD_ATTR                excluded_subtrees
               30  LOAD_CONST               None
               32  <117>                 1  ''
               34  POP_JUMP_IF_FALSE    48  'to 48'

 L.1194        36  LOAD_GLOBAL              tuple
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                excluded_subtrees
               42  CALL_FUNCTION_1       1  ''
               44  STORE_FAST               'es'
               46  JUMP_FORWARD         52  'to 52'
             48_0  COME_FROM            34  '34'

 L.1196        48  LOAD_CONST               None
               50  STORE_FAST               'es'
             52_0  COME_FROM            46  '46'

 L.1198        52  LOAD_GLOBAL              hash
               54  LOAD_FAST                'ps'
               56  LOAD_FAST                'es'
               58  BUILD_TUPLE_2         2 
               60  CALL_FUNCTION_1       1  ''
               62  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    permitted_subtrees = utils.read_only_property('_permitted_subtrees')
    excluded_subtrees = utils.read_only_property('_excluded_subtrees')


class Extension(object):

    def __init__(self, oid, critical, value):
        if not isinstanceoidObjectIdentifier:
            raise TypeError('oid argument must be an ObjectIdentifier instance.')
        if not isinstancecriticalbool:
            raise TypeError('critical must be a boolean value')
        self._oid = oid
        self._critical = critical
        self._value = value

    oid = utils.read_only_property('_oid')
    critical = utils.read_only_property('_critical')
    value = utils.read_only_property('_value')

    def __repr__(self):
        return '<Extension(oid={0.oid}, critical={0.critical}, value={0.value})>'.format(self)

    def __eq__(self, other):
        if not isinstanceotherExtension:
            return NotImplemented
        return self.oid == other.oid and self.critical == other.critical and self.value == other.value

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.oid, self.critical, self.value))


class GeneralNames(object):

    def __init__(self, general_names):
        general_names = list(general_names)
        if not all((isinstancexGeneralName for x in general_names)):
            raise TypeError('Every item in the general_names list must be an object conforming to the GeneralName interface')
        self._general_names = general_names

    __len__, __iter__, __getitem__ = _make_sequence_methods('_general_names')

    def get_values_for_type(self, type):
        objs = (i for i in self if isinstanceitype)
        if type != OtherName:
            objs = (i.value for i in objs)
        return list(objs)

    def __repr__(self):
        return '<GeneralNames({})>'.format(self._general_names)

    def __eq__(self, other):
        if not isinstanceotherGeneralNames:
            return NotImplemented
        return self._general_names == other._general_names

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(tuple(self._general_names))


@utils.register_interface(ExtensionType)
class SubjectAlternativeName(object):
    oid = ExtensionOID.SUBJECT_ALTERNATIVE_NAME

    def __init__(self, general_names):
        self._general_names = GeneralNames(general_names)

    __len__, __iter__, __getitem__ = _make_sequence_methods('_general_names')

    def get_values_for_type(self, type):
        return self._general_names.get_values_for_type(type)

    def __repr__(self):
        return '<SubjectAlternativeName({})>'.format(self._general_names)

    def __eq__(self, other):
        if not isinstanceotherSubjectAlternativeName:
            return NotImplemented
        return self._general_names == other._general_names

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self._general_names)


@utils.register_interface(ExtensionType)
class IssuerAlternativeName(object):
    oid = ExtensionOID.ISSUER_ALTERNATIVE_NAME

    def __init__(self, general_names):
        self._general_names = GeneralNames(general_names)

    __len__, __iter__, __getitem__ = _make_sequence_methods('_general_names')

    def get_values_for_type(self, type):
        return self._general_names.get_values_for_type(type)

    def __repr__(self):
        return '<IssuerAlternativeName({})>'.format(self._general_names)

    def __eq__(self, other):
        if not isinstanceotherIssuerAlternativeName:
            return NotImplemented
        return self._general_names == other._general_names

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self._general_names)


@utils.register_interface(ExtensionType)
class CertificateIssuer(object):
    oid = CRLEntryExtensionOID.CERTIFICATE_ISSUER

    def __init__(self, general_names):
        self._general_names = GeneralNames(general_names)

    __len__, __iter__, __getitem__ = _make_sequence_methods('_general_names')

    def get_values_for_type(self, type):
        return self._general_names.get_values_for_type(type)

    def __repr__(self):
        return '<CertificateIssuer({})>'.format(self._general_names)

    def __eq__(self, other):
        if not isinstanceotherCertificateIssuer:
            return NotImplemented
        return self._general_names == other._general_names

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self._general_names)


@utils.register_interface(ExtensionType)
class CRLReason(object):
    oid = CRLEntryExtensionOID.CRL_REASON

    def __init__(self, reason):
        if not isinstancereasonReasonFlags:
            raise TypeError('reason must be an element from ReasonFlags')
        self._reason = reason

    def __repr__(self):
        return '<CRLReason(reason={})>'.format(self._reason)

    def __eq__(self, other):
        if not isinstanceotherCRLReason:
            return NotImplemented
        return self.reason == other.reason

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.reason)

    reason = utils.read_only_property('_reason')


@utils.register_interface(ExtensionType)
class InvalidityDate(object):
    oid = CRLEntryExtensionOID.INVALIDITY_DATE

    def __init__(self, invalidity_date):
        if not isinstanceinvalidity_datedatetime.datetime:
            raise TypeError('invalidity_date must be a datetime.datetime')
        self._invalidity_date = invalidity_date

    def __repr__(self):
        return '<InvalidityDate(invalidity_date={})>'.format(self._invalidity_date)

    def __eq__(self, other):
        if not isinstanceotherInvalidityDate:
            return NotImplemented
        return self.invalidity_date == other.invalidity_date

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.invalidity_date)

    invalidity_date = utils.read_only_property('_invalidity_date')


@utils.register_interface(ExtensionType)
class PrecertificateSignedCertificateTimestamps(object):
    oid = ExtensionOID.PRECERT_SIGNED_CERTIFICATE_TIMESTAMPS

    def __init__(self, signed_certificate_timestamps):
        signed_certificate_timestamps = list(signed_certificate_timestamps)
        if not all((isinstancesctSignedCertificateTimestamp for sct in signed_certificate_timestamps)):
            raise TypeError('Every item in the signed_certificate_timestamps list must be a SignedCertificateTimestamp')
        self._signed_certificate_timestamps = signed_certificate_timestamps

    __len__, __iter__, __getitem__ = _make_sequence_methods('_signed_certificate_timestamps')

    def __repr__(self):
        return '<PrecertificateSignedCertificateTimestamps({})>'.format(list(self))

    def __hash__(self):
        return hash(tuple(self._signed_certificate_timestamps))

    def __eq__(self, other):
        if not isinstanceotherPrecertificateSignedCertificateTimestamps:
            return NotImplemented
        return self._signed_certificate_timestamps == other._signed_certificate_timestamps

    def __ne__(self, other):
        return not self == other


@utils.register_interface(ExtensionType)
class SignedCertificateTimestamps(object):
    oid = ExtensionOID.SIGNED_CERTIFICATE_TIMESTAMPS

    def __init__(self, signed_certificate_timestamps):
        signed_certificate_timestamps = list(signed_certificate_timestamps)
        if not all((isinstancesctSignedCertificateTimestamp for sct in signed_certificate_timestamps)):
            raise TypeError('Every item in the signed_certificate_timestamps list must be a SignedCertificateTimestamp')
        self._signed_certificate_timestamps = signed_certificate_timestamps

    __len__, __iter__, __getitem__ = _make_sequence_methods('_signed_certificate_timestamps')

    def __repr__(self):
        return '<SignedCertificateTimestamps({})>'.format(list(self))

    def __hash__(self):
        return hash(tuple(self._signed_certificate_timestamps))

    def __eq__(self, other):
        if not isinstanceotherSignedCertificateTimestamps:
            return NotImplemented
        return self._signed_certificate_timestamps == other._signed_certificate_timestamps

    def __ne__(self, other):
        return not self == other


@utils.register_interface(ExtensionType)
class OCSPNonce(object):
    oid = OCSPExtensionOID.NONCE

    def __init__(self, nonce):
        if not isinstancenoncebytes:
            raise TypeError('nonce must be bytes')
        self._nonce = nonce

    def __eq__(self, other):
        if not isinstanceotherOCSPNonce:
            return NotImplemented
        return self.nonce == other.nonce

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.nonce)

    def __repr__(self):
        return '<OCSPNonce(nonce={0.nonce!r})>'.format(self)

    nonce = utils.read_only_property('_nonce')


@utils.register_interface(ExtensionType)
class IssuingDistributionPoint(object):
    oid = ExtensionOID.ISSUING_DISTRIBUTION_POINT

    def __init__--- This code section failed: ---

 L.1547         0  LOAD_FAST                'only_some_reasons'
                2  POP_JUMP_IF_FALSE    40  'to 40'

 L.1548         4  LOAD_GLOBAL              isinstance
                6  LOAD_FAST                'only_some_reasons'
                8  LOAD_GLOBAL              frozenset
               10  CALL_FUNCTION_2       2  ''

 L.1547        12  POP_JUMP_IF_FALSE    32  'to 32'

 L.1549        14  LOAD_GLOBAL              all
               16  LOAD_GENEXPR             '<code_object <genexpr>>'
               18  LOAD_STR                 'IssuingDistributionPoint.__init__.<locals>.<genexpr>'
               20  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               22  LOAD_FAST                'only_some_reasons'
               24  GET_ITER         
               26  CALL_FUNCTION_1       1  ''
               28  CALL_FUNCTION_1       1  ''

 L.1547        30  POP_JUMP_IF_TRUE     40  'to 40'
             32_0  COME_FROM            12  '12'

 L.1551        32  LOAD_GLOBAL              TypeError

 L.1552        34  LOAD_STR                 'only_some_reasons must be None or frozenset of ReasonFlags'

 L.1551        36  CALL_FUNCTION_1       1  ''
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            30  '30'
             40_1  COME_FROM             2  '2'

 L.1555        40  LOAD_FAST                'only_some_reasons'
               42  POP_JUMP_IF_FALSE    72  'to 72'

 L.1556        44  LOAD_GLOBAL              ReasonFlags
               46  LOAD_ATTR                unspecified
               48  LOAD_FAST                'only_some_reasons'
               50  <118>                 0  ''

 L.1555        52  POP_JUMP_IF_TRUE     64  'to 64'

 L.1557        54  LOAD_GLOBAL              ReasonFlags
               56  LOAD_ATTR                remove_from_crl
               58  LOAD_FAST                'only_some_reasons'
               60  <118>                 0  ''

 L.1555        62  POP_JUMP_IF_FALSE    72  'to 72'
             64_0  COME_FROM            52  '52'

 L.1559        64  LOAD_GLOBAL              ValueError

 L.1560        66  LOAD_STR                 'unspecified and remove_from_crl are not valid reasons in an IssuingDistributionPoint'

 L.1559        68  CALL_FUNCTION_1       1  ''
               70  RAISE_VARARGS_1       1  'exception instance'
             72_0  COME_FROM            62  '62'
             72_1  COME_FROM            42  '42'

 L.1565        72  LOAD_GLOBAL              isinstance
               74  LOAD_FAST                'only_contains_user_certs'
               76  LOAD_GLOBAL              bool
               78  CALL_FUNCTION_2       2  ''

 L.1564        80  POP_JUMP_IF_FALSE   112  'to 112'

 L.1566        82  LOAD_GLOBAL              isinstance
               84  LOAD_FAST                'only_contains_ca_certs'
               86  LOAD_GLOBAL              bool
               88  CALL_FUNCTION_2       2  ''

 L.1564        90  POP_JUMP_IF_FALSE   112  'to 112'

 L.1567        92  LOAD_GLOBAL              isinstance
               94  LOAD_FAST                'indirect_crl'
               96  LOAD_GLOBAL              bool
               98  CALL_FUNCTION_2       2  ''

 L.1564       100  POP_JUMP_IF_FALSE   112  'to 112'

 L.1568       102  LOAD_GLOBAL              isinstance
              104  LOAD_FAST                'only_contains_attribute_certs'
              106  LOAD_GLOBAL              bool
              108  CALL_FUNCTION_2       2  ''

 L.1564       110  POP_JUMP_IF_TRUE    120  'to 120'
            112_0  COME_FROM           100  '100'
            112_1  COME_FROM            90  '90'
            112_2  COME_FROM            80  '80'

 L.1570       112  LOAD_GLOBAL              TypeError

 L.1571       114  LOAD_STR                 'only_contains_user_certs, only_contains_ca_certs, indirect_crl and only_contains_attribute_certs must all be boolean.'

 L.1570       116  CALL_FUNCTION_1       1  ''
              118  RAISE_VARARGS_1       1  'exception instance'
            120_0  COME_FROM           110  '110'

 L.1577       120  LOAD_FAST                'only_contains_user_certs'

 L.1578       122  LOAD_FAST                'only_contains_ca_certs'

 L.1579       124  LOAD_FAST                'indirect_crl'

 L.1580       126  LOAD_FAST                'only_contains_attribute_certs'

 L.1576       128  BUILD_LIST_4          4 
              130  STORE_FAST               'crl_constraints'

 L.1583       132  LOAD_GLOBAL              len
              134  LOAD_LISTCOMP            '<code_object <listcomp>>'
              136  LOAD_STR                 'IssuingDistributionPoint.__init__.<locals>.<listcomp>'
              138  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              140  LOAD_FAST                'crl_constraints'
              142  GET_ITER         
              144  CALL_FUNCTION_1       1  ''
              146  CALL_FUNCTION_1       1  ''
              148  LOAD_CONST               1
              150  COMPARE_OP               >
              152  POP_JUMP_IF_FALSE   162  'to 162'

 L.1584       154  LOAD_GLOBAL              ValueError

 L.1585       156  LOAD_STR                 'Only one of the following can be set to True: only_contains_user_certs, only_contains_ca_certs, indirect_crl, only_contains_attribute_certs'

 L.1584       158  CALL_FUNCTION_1       1  ''
              160  RAISE_VARARGS_1       1  'exception instance'
            162_0  COME_FROM           152  '152'

 L.1590       162  LOAD_GLOBAL              any

 L.1592       164  LOAD_FAST                'only_contains_user_certs'

 L.1593       166  LOAD_FAST                'only_contains_ca_certs'

 L.1594       168  LOAD_FAST                'indirect_crl'

 L.1595       170  LOAD_FAST                'only_contains_attribute_certs'

 L.1596       172  LOAD_FAST                'full_name'

 L.1597       174  LOAD_FAST                'relative_name'

 L.1598       176  LOAD_FAST                'only_some_reasons'

 L.1591       178  BUILD_LIST_7          7 

 L.1590       180  CALL_FUNCTION_1       1  ''
              182  POP_JUMP_IF_TRUE    192  'to 192'

 L.1601       184  LOAD_GLOBAL              ValueError

 L.1602       186  LOAD_STR                 'Cannot create empty extension: if only_contains_user_certs, only_contains_ca_certs, indirect_crl, and only_contains_attribute_certs are all False, then either full_name, relative_name, or only_some_reasons must have a value.'

 L.1601       188  CALL_FUNCTION_1       1  ''
              190  RAISE_VARARGS_1       1  'exception instance'
            192_0  COME_FROM           182  '182'

 L.1609       192  LOAD_FAST                'only_contains_user_certs'
              194  LOAD_FAST                'self'
              196  STORE_ATTR               _only_contains_user_certs

 L.1610       198  LOAD_FAST                'only_contains_ca_certs'
              200  LOAD_FAST                'self'
              202  STORE_ATTR               _only_contains_ca_certs

 L.1611       204  LOAD_FAST                'indirect_crl'
              206  LOAD_FAST                'self'
              208  STORE_ATTR               _indirect_crl

 L.1612       210  LOAD_FAST                'only_contains_attribute_certs'
              212  LOAD_FAST                'self'
              214  STORE_ATTR               _only_contains_attribute_certs

 L.1613       216  LOAD_FAST                'only_some_reasons'
              218  LOAD_FAST                'self'
              220  STORE_ATTR               _only_some_reasons

 L.1614       222  LOAD_FAST                'full_name'
              224  LOAD_FAST                'self'
              226  STORE_ATTR               _full_name

 L.1615       228  LOAD_FAST                'relative_name'
              230  LOAD_FAST                'self'
              232  STORE_ATTR               _relative_name

Parse error at or near `<118>' instruction at offset 50

    def __repr__(self):
        return '<IssuingDistributionPoint(full_name={0.full_name}, relative_name={0.relative_name}, only_contains_user_certs={0.only_contains_user_certs}, only_contains_ca_certs={0.only_contains_ca_certs}, only_some_reasons={0.only_some_reasons}, indirect_crl={0.indirect_crl}, only_contains_attribute_certs={0.only_contains_attribute_certs})>'.format(self)

    def __eq__(self, other):
        if not isinstanceotherIssuingDistributionPoint:
            return NotImplemented
        return self.full_name == other.full_name and self.relative_name == other.relative_name and self.only_contains_user_certs == other.only_contains_user_certs and self.only_contains_ca_certs == other.only_contains_ca_certs and self.only_some_reasons == other.only_some_reasons and self.indirect_crl == other.indirect_crl and self.only_contains_attribute_certs == other.only_contains_attribute_certs

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((
         self.full_name,
         self.relative_name,
         self.only_contains_user_certs,
         self.only_contains_ca_certs,
         self.only_some_reasons,
         self.indirect_crl,
         self.only_contains_attribute_certs))

    full_name = utils.read_only_property('_full_name')
    relative_name = utils.read_only_property('_relative_name')
    only_contains_user_certs = utils.read_only_property('_only_contains_user_certs')
    only_contains_ca_certs = utils.read_only_property('_only_contains_ca_certs')
    only_some_reasons = utils.read_only_property('_only_some_reasons')
    indirect_crl = utils.read_only_property('_indirect_crl')
    only_contains_attribute_certs = utils.read_only_property('_only_contains_attribute_certs')


@utils.register_interface(ExtensionType)
class UnrecognizedExtension(object):

    def __init__(self, oid, value):
        if not isinstanceoidObjectIdentifier:
            raise TypeError('oid must be an ObjectIdentifier')
        self._oid = oid
        self._value = value

    oid = utils.read_only_property('_oid')
    value = utils.read_only_property('_value')

    def __repr__(self):
        return '<UnrecognizedExtension(oid={0.oid}, value={0.value!r})>'.format(self)

    def __eq__(self, other):
        if not isinstanceotherUnrecognizedExtension:
            return NotImplemented
        return self.oid == other.oid and self.value == other.value

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.oid, self.value))