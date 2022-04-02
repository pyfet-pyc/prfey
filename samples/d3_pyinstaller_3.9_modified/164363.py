# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\backends\openssl\decode_asn1.py
import datetime, ipaddress
from cryptography import x509
from cryptography.hazmat._der import DERReader, INTEGER, NULL, SEQUENCE
from cryptography.x509.extensions import _TLS_FEATURE_TYPE_TO_ENUM
from cryptography.x509.name import _ASN1_TYPE_TO_ENUM
from cryptography.x509.oid import CRLEntryExtensionOID, CertificatePoliciesOID, ExtensionOID, OCSPExtensionOID

def _obj2txt(backend, obj):
    buf_len = 80
    buf = backend._ffi.new('char[]', buf_len)
    res = backend._lib.OBJ_obj2txt(buf, buf_len, obj, 1)
    if res > buf_len - 1:
        buf_len = res + 1
        buf = backend._ffi.new('char[]', buf_len)
        res = backend._lib.OBJ_obj2txt(buf, buf_len, obj, 1)
    backend.openssl_assert(res > 0)
    return backend._ffi.buffer(buf, res)[:].decode()


def _decode_x509_name_entry(backend, x509_name_entry):
    obj = backend._lib.X509_NAME_ENTRY_get_object(x509_name_entry)
    backend.openssl_assert(obj != backend._ffi.NULL)
    data = backend._lib.X509_NAME_ENTRY_get_data(x509_name_entry)
    backend.openssl_assert(data != backend._ffi.NULL)
    value = _asn1_string_to_utf8(backend, data)
    oid = _obj2txt(backend, obj)
    type = _ASN1_TYPE_TO_ENUM[data.type]
    return x509.NameAttribute(x509.ObjectIdentifier(oid), value, type)


def _decode_x509_name(backend, x509_name):
    count = backend._lib.X509_NAME_entry_count(x509_name)
    attributes = []
    prev_set_id = -1
    for x in range(count):
        entry = backend._lib.X509_NAME_get_entry(x509_name, x)
        attribute = _decode_x509_name_entry(backend, entry)
        set_id = backend._lib.X509_NAME_ENTRY_set(entry)
        if set_id != prev_set_id:
            attributes.append({attribute})
        else:
            attributes[(-1)].add(attribute)
        prev_set_id = set_id
    else:
        return x509.Name((x509.RelativeDistinguishedName(rdn) for rdn in attributes))


def _decode_general_names(backend, gns):
    num = backend._lib.sk_GENERAL_NAME_num(gns)
    names = []
    for i in range(num):
        gn = backend._lib.sk_GENERAL_NAME_value(gns, i)
        backend.openssl_assert(gn != backend._ffi.NULL)
        names.append(_decode_general_name(backend, gn))
    else:
        return names


def _decode_general_name--- This code section failed: ---

 L.  87         0  LOAD_FAST                'gn'
                2  LOAD_ATTR                type
                4  LOAD_FAST                'backend'
                6  LOAD_ATTR                _lib
                8  LOAD_ATTR                GEN_DNS
               10  COMPARE_OP               ==
               12  POP_JUMP_IF_FALSE    46  'to 46'

 L.  91        14  LOAD_GLOBAL              _asn1_string_to_bytes
               16  LOAD_FAST                'backend'
               18  LOAD_FAST                'gn'
               20  LOAD_ATTR                d
               22  LOAD_ATTR                dNSName
               24  CALL_FUNCTION_2       2  ''
               26  LOAD_METHOD              decode
               28  LOAD_STR                 'utf8'
               30  CALL_METHOD_1         1  ''
               32  STORE_FAST               'data'

 L.  95        34  LOAD_GLOBAL              x509
               36  LOAD_ATTR                DNSName
               38  LOAD_METHOD              _init_without_validation
               40  LOAD_FAST                'data'
               42  CALL_METHOD_1         1  ''
               44  RETURN_VALUE     
             46_0  COME_FROM            12  '12'

 L.  96        46  LOAD_FAST                'gn'
               48  LOAD_ATTR                type
               50  LOAD_FAST                'backend'
               52  LOAD_ATTR                _lib
               54  LOAD_ATTR                GEN_URI
               56  COMPARE_OP               ==
               58  POP_JUMP_IF_FALSE    92  'to 92'

 L. 100        60  LOAD_GLOBAL              _asn1_string_to_bytes

 L. 101        62  LOAD_FAST                'backend'
               64  LOAD_FAST                'gn'
               66  LOAD_ATTR                d
               68  LOAD_ATTR                uniformResourceIdentifier

 L. 100        70  CALL_FUNCTION_2       2  ''
               72  LOAD_METHOD              decode

 L. 102        74  LOAD_STR                 'utf8'

 L. 100        76  CALL_METHOD_1         1  ''
               78  STORE_FAST               'data'

 L. 106        80  LOAD_GLOBAL              x509
               82  LOAD_ATTR                UniformResourceIdentifier
               84  LOAD_METHOD              _init_without_validation
               86  LOAD_FAST                'data'
               88  CALL_METHOD_1         1  ''
               90  RETURN_VALUE     
             92_0  COME_FROM            58  '58'

 L. 107        92  LOAD_FAST                'gn'
               94  LOAD_ATTR                type
               96  LOAD_FAST                'backend'
               98  LOAD_ATTR                _lib
              100  LOAD_ATTR                GEN_RID
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_FALSE   136  'to 136'

 L. 108       106  LOAD_GLOBAL              _obj2txt
              108  LOAD_FAST                'backend'
              110  LOAD_FAST                'gn'
              112  LOAD_ATTR                d
              114  LOAD_ATTR                registeredID
              116  CALL_FUNCTION_2       2  ''
              118  STORE_FAST               'oid'

 L. 109       120  LOAD_GLOBAL              x509
              122  LOAD_METHOD              RegisteredID
              124  LOAD_GLOBAL              x509
              126  LOAD_METHOD              ObjectIdentifier
              128  LOAD_FAST                'oid'
              130  CALL_METHOD_1         1  ''
              132  CALL_METHOD_1         1  ''
              134  RETURN_VALUE     
            136_0  COME_FROM           104  '104'

 L. 110       136  LOAD_FAST                'gn'
              138  LOAD_ATTR                type
              140  LOAD_FAST                'backend'
              142  LOAD_ATTR                _lib
              144  LOAD_ATTR                GEN_IPADD
              146  COMPARE_OP               ==
          148_150  POP_JUMP_IF_FALSE   354  'to 354'

 L. 111       152  LOAD_GLOBAL              _asn1_string_to_bytes
              154  LOAD_FAST                'backend'
              156  LOAD_FAST                'gn'
              158  LOAD_ATTR                d
              160  LOAD_ATTR                iPAddress
              162  CALL_FUNCTION_2       2  ''
              164  STORE_FAST               'data'

 L. 112       166  LOAD_GLOBAL              len
              168  LOAD_FAST                'data'
              170  CALL_FUNCTION_1       1  ''
              172  STORE_FAST               'data_len'

 L. 113       174  LOAD_FAST                'data_len'
              176  LOAD_CONST               8
              178  COMPARE_OP               ==
              180  POP_JUMP_IF_TRUE    192  'to 192'
              182  LOAD_FAST                'data_len'
              184  LOAD_CONST               32
              186  COMPARE_OP               ==
          188_190  POP_JUMP_IF_FALSE   334  'to 334'
            192_0  COME_FROM           180  '180'

 L. 121       192  LOAD_GLOBAL              ipaddress
              194  LOAD_METHOD              ip_address
              196  LOAD_FAST                'data'
              198  LOAD_CONST               None
              200  LOAD_FAST                'data_len'
              202  LOAD_CONST               2
              204  BINARY_FLOOR_DIVIDE
              206  BUILD_SLICE_2         2 
              208  BINARY_SUBSCR    
              210  CALL_METHOD_1         1  ''
              212  STORE_FAST               'base'

 L. 122       214  LOAD_GLOBAL              ipaddress
              216  LOAD_METHOD              ip_address
              218  LOAD_FAST                'data'
              220  LOAD_FAST                'data_len'
              222  LOAD_CONST               2
              224  BINARY_FLOOR_DIVIDE
              226  LOAD_CONST               None
              228  BUILD_SLICE_2         2 
              230  BINARY_SUBSCR    
              232  CALL_METHOD_1         1  ''
              234  STORE_FAST               'netmask'

 L. 123       236  LOAD_GLOBAL              bin
              238  LOAD_GLOBAL              int
              240  LOAD_FAST                'netmask'
              242  CALL_FUNCTION_1       1  ''
              244  CALL_FUNCTION_1       1  ''
              246  LOAD_CONST               2
              248  LOAD_CONST               None
              250  BUILD_SLICE_2         2 
              252  BINARY_SUBSCR    
              254  STORE_FAST               'bits'

 L. 124       256  LOAD_FAST                'bits'
              258  LOAD_METHOD              find
              260  LOAD_STR                 '0'
              262  CALL_METHOD_1         1  ''
              264  STORE_FAST               'prefix'

 L. 126       266  LOAD_FAST                'prefix'
              268  LOAD_CONST               -1
              270  COMPARE_OP               ==
          272_274  POP_JUMP_IF_FALSE   284  'to 284'

 L. 127       276  LOAD_GLOBAL              len
              278  LOAD_FAST                'bits'
              280  CALL_FUNCTION_1       1  ''
              282  STORE_FAST               'prefix'
            284_0  COME_FROM           272  '272'

 L. 129       284  LOAD_STR                 '1'
              286  LOAD_FAST                'bits'
              288  LOAD_FAST                'prefix'
              290  LOAD_CONST               None
              292  BUILD_SLICE_2         2 
              294  BINARY_SUBSCR    
              296  <118>                 0  ''
          298_300  POP_JUMP_IF_FALSE   310  'to 310'

 L. 130       302  LOAD_GLOBAL              ValueError
              304  LOAD_STR                 'Invalid netmask'
              306  CALL_FUNCTION_1       1  ''
              308  RAISE_VARARGS_1       1  'exception instance'
            310_0  COME_FROM           298  '298'

 L. 132       310  LOAD_GLOBAL              ipaddress
              312  LOAD_METHOD              ip_network
              314  LOAD_FAST                'base'
              316  LOAD_ATTR                exploded
              318  LOAD_STR                 '/{}'
              320  LOAD_METHOD              format
              322  LOAD_FAST                'prefix'
              324  CALL_METHOD_1         1  ''
              326  BINARY_ADD       
              328  CALL_METHOD_1         1  ''
              330  STORE_FAST               'ip'
              332  JUMP_FORWARD        344  'to 344'
            334_0  COME_FROM           188  '188'

 L. 134       334  LOAD_GLOBAL              ipaddress
              336  LOAD_METHOD              ip_address
              338  LOAD_FAST                'data'
              340  CALL_METHOD_1         1  ''
              342  STORE_FAST               'ip'
            344_0  COME_FROM           332  '332'

 L. 136       344  LOAD_GLOBAL              x509
              346  LOAD_METHOD              IPAddress
              348  LOAD_FAST                'ip'
              350  CALL_METHOD_1         1  ''
              352  RETURN_VALUE     
            354_0  COME_FROM           148  '148'

 L. 137       354  LOAD_FAST                'gn'
              356  LOAD_ATTR                type
              358  LOAD_FAST                'backend'
              360  LOAD_ATTR                _lib
              362  LOAD_ATTR                GEN_DIRNAME
              364  COMPARE_OP               ==
          366_368  POP_JUMP_IF_FALSE   390  'to 390'

 L. 138       370  LOAD_GLOBAL              x509
              372  LOAD_METHOD              DirectoryName

 L. 139       374  LOAD_GLOBAL              _decode_x509_name
              376  LOAD_FAST                'backend'
              378  LOAD_FAST                'gn'
              380  LOAD_ATTR                d
              382  LOAD_ATTR                directoryName
              384  CALL_FUNCTION_2       2  ''

 L. 138       386  CALL_METHOD_1         1  ''
              388  RETURN_VALUE     
            390_0  COME_FROM           366  '366'

 L. 141       390  LOAD_FAST                'gn'
              392  LOAD_ATTR                type
              394  LOAD_FAST                'backend'
              396  LOAD_ATTR                _lib
              398  LOAD_ATTR                GEN_EMAIL
              400  COMPARE_OP               ==
          402_404  POP_JUMP_IF_FALSE   438  'to 438'

 L. 145       406  LOAD_GLOBAL              _asn1_string_to_bytes
              408  LOAD_FAST                'backend'
              410  LOAD_FAST                'gn'
              412  LOAD_ATTR                d
              414  LOAD_ATTR                rfc822Name
              416  CALL_FUNCTION_2       2  ''
              418  LOAD_METHOD              decode
              420  LOAD_STR                 'utf8'
              422  CALL_METHOD_1         1  ''
              424  STORE_FAST               'data'

 L. 149       426  LOAD_GLOBAL              x509
              428  LOAD_ATTR                RFC822Name
              430  LOAD_METHOD              _init_without_validation
              432  LOAD_FAST                'data'
              434  CALL_METHOD_1         1  ''
              436  RETURN_VALUE     
            438_0  COME_FROM           402  '402'

 L. 150       438  LOAD_FAST                'gn'
              440  LOAD_ATTR                type
              442  LOAD_FAST                'backend'
              444  LOAD_ATTR                _lib
              446  LOAD_ATTR                GEN_OTHERNAME
              448  COMPARE_OP               ==
          450_452  POP_JUMP_IF_FALSE   504  'to 504'

 L. 151       454  LOAD_GLOBAL              _obj2txt
              456  LOAD_FAST                'backend'
              458  LOAD_FAST                'gn'
              460  LOAD_ATTR                d
              462  LOAD_ATTR                otherName
              464  LOAD_ATTR                type_id
              466  CALL_FUNCTION_2       2  ''
              468  STORE_FAST               'type_id'

 L. 152       470  LOAD_GLOBAL              _asn1_to_der
              472  LOAD_FAST                'backend'
              474  LOAD_FAST                'gn'
              476  LOAD_ATTR                d
              478  LOAD_ATTR                otherName
              480  LOAD_ATTR                value
              482  CALL_FUNCTION_2       2  ''
              484  STORE_FAST               'value'

 L. 153       486  LOAD_GLOBAL              x509
              488  LOAD_METHOD              OtherName
              490  LOAD_GLOBAL              x509
              492  LOAD_METHOD              ObjectIdentifier
              494  LOAD_FAST                'type_id'
              496  CALL_METHOD_1         1  ''
              498  LOAD_FAST                'value'
              500  CALL_METHOD_2         2  ''
              502  RETURN_VALUE     
            504_0  COME_FROM           450  '450'

 L. 156       504  LOAD_GLOBAL              x509
              506  LOAD_METHOD              UnsupportedGeneralNameType

 L. 157       508  LOAD_STR                 '{} is not a supported type'
              510  LOAD_METHOD              format

 L. 158       512  LOAD_GLOBAL              x509
              514  LOAD_ATTR                _GENERAL_NAMES
              516  LOAD_METHOD              get
              518  LOAD_FAST                'gn'
              520  LOAD_ATTR                type
              522  LOAD_FAST                'gn'
              524  LOAD_ATTR                type
              526  CALL_METHOD_2         2  ''

 L. 157       528  CALL_METHOD_1         1  ''

 L. 160       530  LOAD_FAST                'gn'
              532  LOAD_ATTR                type

 L. 156       534  CALL_METHOD_2         2  ''
              536  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<118>' instruction at offset 296


def _decode_ocsp_no_check(backend, ext):
    return x509.OCSPNoCheck()


def _decode_crl_number(backend, ext):
    asn1_int = backend._ffi.cast('ASN1_INTEGER *', ext)
    asn1_int = backend._ffi.gc(asn1_int, backend._lib.ASN1_INTEGER_free)
    return x509.CRLNumber(_asn1_integer_to_int(backend, asn1_int))


def _decode_delta_crl_indicator(backend, ext):
    asn1_int = backend._ffi.cast('ASN1_INTEGER *', ext)
    asn1_int = backend._ffi.gc(asn1_int, backend._lib.ASN1_INTEGER_free)
    return x509.DeltaCRLIndicator(_asn1_integer_to_int(backend, asn1_int))


class _X509ExtensionParser(object):

    def __init__(self, backend, ext_count, get_ext, handlers):
        self.ext_count = ext_count
        self.get_ext = get_ext
        self.handlers = handlers
        self._backend = backend

    def parse--- This code section failed: ---

 L. 188         0  BUILD_LIST_0          0 
                2  STORE_FAST               'extensions'

 L. 189         4  LOAD_GLOBAL              set
                6  CALL_FUNCTION_0       0  ''
                8  STORE_FAST               'seen_oids'

 L. 190        10  LOAD_GLOBAL              range
               12  LOAD_FAST                'self'
               14  LOAD_METHOD              ext_count
               16  LOAD_FAST                'x509_obj'
               18  CALL_METHOD_1         1  ''
               20  CALL_FUNCTION_1       1  ''
               22  GET_ITER         
             24_0  COME_FROM           600  '600'
             24_1  COME_FROM           370  '370'
             24_2  COME_FROM           276  '276'
            24_26  FOR_ITER            602  'to 602'
               28  STORE_FAST               'i'

 L. 191        30  LOAD_FAST                'self'
               32  LOAD_METHOD              get_ext
               34  LOAD_FAST                'x509_obj'
               36  LOAD_FAST                'i'
               38  CALL_METHOD_2         2  ''
               40  STORE_FAST               'ext'

 L. 192        42  LOAD_FAST                'self'
               44  LOAD_ATTR                _backend
               46  LOAD_METHOD              openssl_assert
               48  LOAD_FAST                'ext'
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                _backend
               54  LOAD_ATTR                _ffi
               56  LOAD_ATTR                NULL
               58  COMPARE_OP               !=
               60  CALL_METHOD_1         1  ''
               62  POP_TOP          

 L. 193        64  LOAD_FAST                'self'
               66  LOAD_ATTR                _backend
               68  LOAD_ATTR                _lib
               70  LOAD_METHOD              X509_EXTENSION_get_critical
               72  LOAD_FAST                'ext'
               74  CALL_METHOD_1         1  ''
               76  STORE_FAST               'crit'

 L. 194        78  LOAD_FAST                'crit'
               80  LOAD_CONST               1
               82  COMPARE_OP               ==
               84  STORE_FAST               'critical'

 L. 195        86  LOAD_GLOBAL              x509
               88  LOAD_METHOD              ObjectIdentifier

 L. 196        90  LOAD_GLOBAL              _obj2txt

 L. 197        92  LOAD_FAST                'self'
               94  LOAD_ATTR                _backend

 L. 198        96  LOAD_FAST                'self'
               98  LOAD_ATTR                _backend
              100  LOAD_ATTR                _lib
              102  LOAD_METHOD              X509_EXTENSION_get_object
              104  LOAD_FAST                'ext'
              106  CALL_METHOD_1         1  ''

 L. 196       108  CALL_FUNCTION_2       2  ''

 L. 195       110  CALL_METHOD_1         1  ''
              112  STORE_FAST               'oid'

 L. 201       114  LOAD_FAST                'oid'
              116  LOAD_FAST                'seen_oids'
              118  <118>                 0  ''
              120  POP_JUMP_IF_FALSE   140  'to 140'

 L. 202       122  LOAD_GLOBAL              x509
              124  LOAD_METHOD              DuplicateExtension

 L. 203       126  LOAD_STR                 'Duplicate {} extension found'
              128  LOAD_METHOD              format
              130  LOAD_FAST                'oid'
              132  CALL_METHOD_1         1  ''
              134  LOAD_FAST                'oid'

 L. 202       136  CALL_METHOD_2         2  ''
              138  RAISE_VARARGS_1       1  'exception instance'
            140_0  COME_FROM           120  '120'

 L. 209       140  LOAD_FAST                'oid'
              142  LOAD_GLOBAL              ExtensionOID
              144  LOAD_ATTR                TLS_FEATURE
              146  COMPARE_OP               ==
          148_150  POP_JUMP_IF_FALSE   280  'to 280'

 L. 211       152  LOAD_FAST                'self'
              154  LOAD_ATTR                _backend
              156  LOAD_ATTR                _lib
              158  LOAD_METHOD              X509_EXTENSION_get_data
              160  LOAD_FAST                'ext'
              162  CALL_METHOD_1         1  ''
              164  STORE_FAST               'data'

 L. 212       166  LOAD_GLOBAL              _asn1_string_to_bytes
              168  LOAD_FAST                'self'
              170  LOAD_ATTR                _backend
              172  LOAD_FAST                'data'
              174  CALL_FUNCTION_2       2  ''
              176  STORE_FAST               'data_bytes'

 L. 213       178  LOAD_GLOBAL              DERReader
              180  LOAD_FAST                'data_bytes'
              182  CALL_FUNCTION_1       1  ''
              184  LOAD_METHOD              read_single_element
              186  LOAD_GLOBAL              SEQUENCE
              188  CALL_METHOD_1         1  ''
              190  STORE_FAST               'features'

 L. 214       192  BUILD_LIST_0          0 
              194  STORE_FAST               'parsed'
            196_0  COME_FROM           224  '224'

 L. 215       196  LOAD_FAST                'features'
              198  LOAD_METHOD              is_empty
              200  CALL_METHOD_0         0  ''
              202  POP_JUMP_IF_TRUE    226  'to 226'

 L. 216       204  LOAD_FAST                'parsed'
              206  LOAD_METHOD              append
              208  LOAD_FAST                'features'
              210  LOAD_METHOD              read_element
              212  LOAD_GLOBAL              INTEGER
              214  CALL_METHOD_1         1  ''
              216  LOAD_METHOD              as_integer
              218  CALL_METHOD_0         0  ''
              220  CALL_METHOD_1         1  ''
              222  POP_TOP          
              224  JUMP_BACK           196  'to 196'
            226_0  COME_FROM           202  '202'

 L. 218       226  LOAD_GLOBAL              x509
              228  LOAD_METHOD              TLSFeature

 L. 219       230  LOAD_LISTCOMP            '<code_object <listcomp>>'
              232  LOAD_STR                 '_X509ExtensionParser.parse.<locals>.<listcomp>'
              234  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              236  LOAD_FAST                'parsed'
              238  GET_ITER         
              240  CALL_FUNCTION_1       1  ''

 L. 218       242  CALL_METHOD_1         1  ''
              244  STORE_FAST               'value'

 L. 221       246  LOAD_FAST                'extensions'
              248  LOAD_METHOD              append
              250  LOAD_GLOBAL              x509
              252  LOAD_METHOD              Extension
              254  LOAD_FAST                'oid'
              256  LOAD_FAST                'critical'
              258  LOAD_FAST                'value'
              260  CALL_METHOD_3         3  ''
              262  CALL_METHOD_1         1  ''
              264  POP_TOP          

 L. 222       266  LOAD_FAST                'seen_oids'
              268  LOAD_METHOD              add
              270  LOAD_FAST                'oid'
              272  CALL_METHOD_1         1  ''
              274  POP_TOP          

 L. 223       276  JUMP_BACK            24  'to 24'
              278  JUMP_FORWARD        372  'to 372'
            280_0  COME_FROM           148  '148'

 L. 224       280  LOAD_FAST                'oid'
              282  LOAD_GLOBAL              ExtensionOID
              284  LOAD_ATTR                PRECERT_POISON
              286  COMPARE_OP               ==
          288_290  POP_JUMP_IF_FALSE   372  'to 372'

 L. 225       292  LOAD_FAST                'self'
              294  LOAD_ATTR                _backend
              296  LOAD_ATTR                _lib
              298  LOAD_METHOD              X509_EXTENSION_get_data
              300  LOAD_FAST                'ext'
              302  CALL_METHOD_1         1  ''
              304  STORE_FAST               'data'

 L. 227       306  LOAD_GLOBAL              DERReader
              308  LOAD_GLOBAL              _asn1_string_to_bytes
              310  LOAD_FAST                'self'
              312  LOAD_ATTR                _backend
              314  LOAD_FAST                'data'
              316  CALL_FUNCTION_2       2  ''
              318  CALL_FUNCTION_1       1  ''
              320  STORE_FAST               'reader'

 L. 228       322  LOAD_FAST                'reader'
              324  LOAD_METHOD              read_single_element
              326  LOAD_GLOBAL              NULL
              328  CALL_METHOD_1         1  ''
              330  LOAD_METHOD              check_empty
              332  CALL_METHOD_0         0  ''
              334  POP_TOP          

 L. 229       336  LOAD_FAST                'extensions'
              338  LOAD_METHOD              append

 L. 230       340  LOAD_GLOBAL              x509
              342  LOAD_METHOD              Extension
              344  LOAD_FAST                'oid'
              346  LOAD_FAST                'critical'
              348  LOAD_GLOBAL              x509
              350  LOAD_METHOD              PrecertPoison
              352  CALL_METHOD_0         0  ''
              354  CALL_METHOD_3         3  ''

 L. 229       356  CALL_METHOD_1         1  ''
              358  POP_TOP          

 L. 232       360  LOAD_FAST                'seen_oids'
              362  LOAD_METHOD              add
              364  LOAD_FAST                'oid'
              366  CALL_METHOD_1         1  ''
              368  POP_TOP          

 L. 233       370  JUMP_BACK            24  'to 24'
            372_0  COME_FROM           288  '288'
            372_1  COME_FROM           278  '278'

 L. 235       372  SETUP_FINALLY       388  'to 388'

 L. 236       374  LOAD_FAST                'self'
              376  LOAD_ATTR                handlers
              378  LOAD_FAST                'oid'
              380  BINARY_SUBSCR    
              382  STORE_FAST               'handler'
              384  POP_BLOCK        
              386  JUMP_FORWARD        504  'to 504'
            388_0  COME_FROM_FINALLY   372  '372'

 L. 237       388  DUP_TOP          
              390  LOAD_GLOBAL              KeyError
          392_394  <121>               502  ''
              396  POP_TOP          
              398  POP_TOP          
              400  POP_TOP          

 L. 239       402  LOAD_FAST                'self'
              404  LOAD_ATTR                _backend
              406  LOAD_ATTR                _lib
              408  LOAD_METHOD              X509_EXTENSION_get_data
              410  LOAD_FAST                'ext'
              412  CALL_METHOD_1         1  ''
              414  STORE_FAST               'data'

 L. 240       416  LOAD_FAST                'self'
              418  LOAD_ATTR                _backend
              420  LOAD_METHOD              openssl_assert
              422  LOAD_FAST                'data'
              424  LOAD_FAST                'self'
              426  LOAD_ATTR                _backend
              428  LOAD_ATTR                _ffi
              430  LOAD_ATTR                NULL
              432  COMPARE_OP               !=
              434  CALL_METHOD_1         1  ''
              436  POP_TOP          

 L. 241       438  LOAD_FAST                'self'
              440  LOAD_ATTR                _backend
              442  LOAD_ATTR                _ffi
              444  LOAD_METHOD              buffer
              446  LOAD_FAST                'data'
              448  LOAD_ATTR                data
              450  LOAD_FAST                'data'
              452  LOAD_ATTR                length
              454  CALL_METHOD_2         2  ''
              456  LOAD_CONST               None
              458  LOAD_CONST               None
              460  BUILD_SLICE_2         2 
              462  BINARY_SUBSCR    
              464  STORE_FAST               'der'

 L. 242       466  LOAD_GLOBAL              x509
              468  LOAD_METHOD              UnrecognizedExtension
              470  LOAD_FAST                'oid'
              472  LOAD_FAST                'der'
              474  CALL_METHOD_2         2  ''
              476  STORE_FAST               'unrecognized'

 L. 243       478  LOAD_FAST                'extensions'
              480  LOAD_METHOD              append
              482  LOAD_GLOBAL              x509
              484  LOAD_METHOD              Extension
              486  LOAD_FAST                'oid'
              488  LOAD_FAST                'critical'
              490  LOAD_FAST                'unrecognized'
              492  CALL_METHOD_3         3  ''
              494  CALL_METHOD_1         1  ''
              496  POP_TOP          
              498  POP_EXCEPT       
              500  JUMP_FORWARD        590  'to 590'
              502  <48>             
            504_0  COME_FROM           386  '386'

 L. 245       504  LOAD_FAST                'self'
              506  LOAD_ATTR                _backend
              508  LOAD_ATTR                _lib
              510  LOAD_METHOD              X509V3_EXT_d2i
              512  LOAD_FAST                'ext'
              514  CALL_METHOD_1         1  ''
              516  STORE_FAST               'ext_data'

 L. 246       518  LOAD_FAST                'ext_data'
              520  LOAD_FAST                'self'
              522  LOAD_ATTR                _backend
              524  LOAD_ATTR                _ffi
              526  LOAD_ATTR                NULL
              528  COMPARE_OP               ==
          530_532  POP_JUMP_IF_FALSE   558  'to 558'

 L. 247       534  LOAD_FAST                'self'
              536  LOAD_ATTR                _backend
              538  LOAD_METHOD              _consume_errors
              540  CALL_METHOD_0         0  ''
              542  POP_TOP          

 L. 248       544  LOAD_GLOBAL              ValueError

 L. 249       546  LOAD_STR                 "The {} extension is invalid and can't be parsed"
              548  LOAD_METHOD              format

 L. 250       550  LOAD_FAST                'oid'

 L. 249       552  CALL_METHOD_1         1  ''

 L. 248       554  CALL_FUNCTION_1       1  ''
              556  RAISE_VARARGS_1       1  'exception instance'
            558_0  COME_FROM           530  '530'

 L. 253       558  LOAD_FAST                'handler'
              560  LOAD_FAST                'self'
              562  LOAD_ATTR                _backend
              564  LOAD_FAST                'ext_data'
              566  CALL_FUNCTION_2       2  ''
              568  STORE_FAST               'value'

 L. 254       570  LOAD_FAST                'extensions'
              572  LOAD_METHOD              append
              574  LOAD_GLOBAL              x509
              576  LOAD_METHOD              Extension
              578  LOAD_FAST                'oid'
              580  LOAD_FAST                'critical'
              582  LOAD_FAST                'value'
              584  CALL_METHOD_3         3  ''
              586  CALL_METHOD_1         1  ''
              588  POP_TOP          
            590_0  COME_FROM           500  '500'

 L. 256       590  LOAD_FAST                'seen_oids'
              592  LOAD_METHOD              add
              594  LOAD_FAST                'oid'
              596  CALL_METHOD_1         1  ''
              598  POP_TOP          
              600  JUMP_BACK            24  'to 24'
            602_0  COME_FROM            24  '24'

 L. 258       602  LOAD_GLOBAL              x509
              604  LOAD_METHOD              Extensions
              606  LOAD_FAST                'extensions'
              608  CALL_METHOD_1         1  ''
              610  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 118


def _decode_certificate_policies--- This code section failed: ---

 L. 262         0  LOAD_FAST                'backend'
                2  LOAD_ATTR                _ffi
                4  LOAD_METHOD              cast
                6  LOAD_STR                 'Cryptography_STACK_OF_POLICYINFO *'
                8  LOAD_FAST                'cp'
               10  CALL_METHOD_2         2  ''
               12  STORE_FAST               'cp'

 L. 263        14  LOAD_FAST                'backend'
               16  LOAD_ATTR                _ffi
               18  LOAD_METHOD              gc
               20  LOAD_FAST                'cp'
               22  LOAD_FAST                'backend'
               24  LOAD_ATTR                _lib
               26  LOAD_ATTR                CERTIFICATEPOLICIES_free
               28  CALL_METHOD_2         2  ''
               30  STORE_FAST               'cp'

 L. 265        32  LOAD_FAST                'backend'
               34  LOAD_ATTR                _lib
               36  LOAD_METHOD              sk_POLICYINFO_num
               38  LOAD_FAST                'cp'
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'num'

 L. 266        44  BUILD_LIST_0          0 
               46  STORE_FAST               'certificate_policies'

 L. 267        48  LOAD_GLOBAL              range
               50  LOAD_FAST                'num'
               52  CALL_FUNCTION_1       1  ''
               54  GET_ITER         
             56_0  COME_FROM           296  '296'
               56  FOR_ITER            298  'to 298'
               58  STORE_FAST               'i'

 L. 268        60  LOAD_CONST               None
               62  STORE_FAST               'qualifiers'

 L. 269        64  LOAD_FAST                'backend'
               66  LOAD_ATTR                _lib
               68  LOAD_METHOD              sk_POLICYINFO_value
               70  LOAD_FAST                'cp'
               72  LOAD_FAST                'i'
               74  CALL_METHOD_2         2  ''
               76  STORE_FAST               'pi'

 L. 270        78  LOAD_GLOBAL              x509
               80  LOAD_METHOD              ObjectIdentifier
               82  LOAD_GLOBAL              _obj2txt
               84  LOAD_FAST                'backend'
               86  LOAD_FAST                'pi'
               88  LOAD_ATTR                policyid
               90  CALL_FUNCTION_2       2  ''
               92  CALL_METHOD_1         1  ''
               94  STORE_FAST               'oid'

 L. 271        96  LOAD_FAST                'pi'
               98  LOAD_ATTR                qualifiers
              100  LOAD_FAST                'backend'
              102  LOAD_ATTR                _ffi
              104  LOAD_ATTR                NULL
              106  COMPARE_OP               !=
          108_110  POP_JUMP_IF_FALSE   278  'to 278'

 L. 272       112  LOAD_FAST                'backend'
              114  LOAD_ATTR                _lib
              116  LOAD_METHOD              sk_POLICYQUALINFO_num
              118  LOAD_FAST                'pi'
              120  LOAD_ATTR                qualifiers
              122  CALL_METHOD_1         1  ''
              124  STORE_FAST               'qnum'

 L. 273       126  BUILD_LIST_0          0 
              128  STORE_FAST               'qualifiers'

 L. 274       130  LOAD_GLOBAL              range
              132  LOAD_FAST                'qnum'
              134  CALL_FUNCTION_1       1  ''
              136  GET_ITER         
            138_0  COME_FROM           276  '276'
            138_1  COME_FROM           236  '236'
              138  FOR_ITER            278  'to 278'
              140  STORE_FAST               'j'

 L. 275       142  LOAD_FAST                'backend'
              144  LOAD_ATTR                _lib
              146  LOAD_METHOD              sk_POLICYQUALINFO_value
              148  LOAD_FAST                'pi'
              150  LOAD_ATTR                qualifiers
              152  LOAD_FAST                'j'
              154  CALL_METHOD_2         2  ''
              156  STORE_FAST               'pqi'

 L. 276       158  LOAD_GLOBAL              x509
              160  LOAD_METHOD              ObjectIdentifier
              162  LOAD_GLOBAL              _obj2txt
              164  LOAD_FAST                'backend'
              166  LOAD_FAST                'pqi'
              168  LOAD_ATTR                pqualid
              170  CALL_FUNCTION_2       2  ''
              172  CALL_METHOD_1         1  ''
              174  STORE_FAST               'pqualid'

 L. 277       176  LOAD_FAST                'pqualid'
              178  LOAD_GLOBAL              CertificatePoliciesOID
              180  LOAD_ATTR                CPS_QUALIFIER
              182  COMPARE_OP               ==
              184  POP_JUMP_IF_FALSE   238  'to 238'

 L. 278       186  LOAD_FAST                'backend'
              188  LOAD_ATTR                _ffi
              190  LOAD_METHOD              buffer

 L. 279       192  LOAD_FAST                'pqi'
              194  LOAD_ATTR                d
              196  LOAD_ATTR                cpsuri
              198  LOAD_ATTR                data
              200  LOAD_FAST                'pqi'
              202  LOAD_ATTR                d
              204  LOAD_ATTR                cpsuri
              206  LOAD_ATTR                length

 L. 278       208  CALL_METHOD_2         2  ''

 L. 280       210  LOAD_CONST               None
              212  LOAD_CONST               None
              214  BUILD_SLICE_2         2 

 L. 278       216  BINARY_SUBSCR    
              218  LOAD_METHOD              decode

 L. 280       220  LOAD_STR                 'ascii'

 L. 278       222  CALL_METHOD_1         1  ''
              224  STORE_FAST               'cpsuri'

 L. 281       226  LOAD_FAST                'qualifiers'
              228  LOAD_METHOD              append
              230  LOAD_FAST                'cpsuri'
              232  CALL_METHOD_1         1  ''
              234  POP_TOP          
              236  JUMP_BACK           138  'to 138'
            238_0  COME_FROM           184  '184'

 L. 283       238  LOAD_FAST                'pqualid'
              240  LOAD_GLOBAL              CertificatePoliciesOID
              242  LOAD_ATTR                CPS_USER_NOTICE
              244  COMPARE_OP               ==
              246  POP_JUMP_IF_TRUE    252  'to 252'
              248  <74>             
              250  RAISE_VARARGS_1       1  'exception instance'
            252_0  COME_FROM           246  '246'

 L. 284       252  LOAD_GLOBAL              _decode_user_notice

 L. 285       254  LOAD_FAST                'backend'
              256  LOAD_FAST                'pqi'
              258  LOAD_ATTR                d
              260  LOAD_ATTR                usernotice

 L. 284       262  CALL_FUNCTION_2       2  ''
              264  STORE_FAST               'user_notice'

 L. 287       266  LOAD_FAST                'qualifiers'
              268  LOAD_METHOD              append
              270  LOAD_FAST                'user_notice'
              272  CALL_METHOD_1         1  ''
              274  POP_TOP          
              276  JUMP_BACK           138  'to 138'
            278_0  COME_FROM           138  '138'
            278_1  COME_FROM           108  '108'

 L. 289       278  LOAD_FAST                'certificate_policies'
              280  LOAD_METHOD              append
              282  LOAD_GLOBAL              x509
              284  LOAD_METHOD              PolicyInformation
              286  LOAD_FAST                'oid'
              288  LOAD_FAST                'qualifiers'
              290  CALL_METHOD_2         2  ''
              292  CALL_METHOD_1         1  ''
              294  POP_TOP          
              296  JUMP_BACK            56  'to 56'
            298_0  COME_FROM            56  '56'

 L. 291       298  LOAD_GLOBAL              x509
              300  LOAD_METHOD              CertificatePolicies
              302  LOAD_FAST                'certificate_policies'
              304  CALL_METHOD_1         1  ''
              306  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 248


def _decode_user_notice(backend, un):
    explicit_text = None
    notice_reference = None
    if un.exptext != backend._ffi.NULL:
        explicit_text = _asn1_string_to_utf8(backend, un.exptext)
    if un.noticeref != backend._ffi.NULL:
        organization = _asn1_string_to_utf8(backend, un.noticeref.organization)
        num = backend._lib.sk_ASN1_INTEGER_num(un.noticeref.noticenos)
        notice_numbers = []
        for i in range(num):
            asn1_int = backend._lib.sk_ASN1_INTEGER_value(un.noticeref.noticenos, i)
            notice_num = _asn1_integer_to_int(backend, asn1_int)
            notice_numbers.append(notice_num)
        else:
            notice_reference = x509.NoticeReference(organization, notice_numbers)

    return x509.UserNotice(notice_reference, explicit_text)


def _decode_basic_constraints(backend, bc_st):
    basic_constraints = backend._ffi.cast('BASIC_CONSTRAINTS *', bc_st)
    basic_constraints = backend._ffi.gc(basic_constraints, backend._lib.BASIC_CONSTRAINTS_free)
    ca = basic_constraints.ca == 255
    path_length = _asn1_integer_to_int_or_none(backend, basic_constraints.pathlen)
    return x509.BasicConstraints(ca, path_length)


def _decode_subject_key_identifier(backend, asn1_string):
    asn1_string = backend._ffi.cast('ASN1_OCTET_STRING *', asn1_string)
    asn1_string = backend._ffi.gc(asn1_string, backend._lib.ASN1_OCTET_STRING_free)
    return x509.SubjectKeyIdentifier(backend._ffi.buffer(asn1_string.data, asn1_string.length)[:])


def _decode_authority_key_identifier(backend, akid):
    akid = backend._ffi.cast('AUTHORITY_KEYID *', akid)
    akid = backend._ffi.gc(akid, backend._lib.AUTHORITY_KEYID_free)
    key_identifier = None
    authority_cert_issuer = None
    if akid.keyid != backend._ffi.NULL:
        key_identifier = backend._ffi.buffer(akid.keyid.data, akid.keyid.length)[:]
    if akid.issuer != backend._ffi.NULL:
        authority_cert_issuer = _decode_general_names(backend, akid.issuer)
    authority_cert_serial_number = _asn1_integer_to_int_or_none(backend, akid.serial)
    return x509.AuthorityKeyIdentifier(key_identifier, authority_cert_issuer, authority_cert_serial_number)


def _decode_information_access(backend, ia):
    ia = backend._ffi.cast('Cryptography_STACK_OF_ACCESS_DESCRIPTION *', ia)
    ia = backend._ffi.gc(ia, lambda x: backend._lib.sk_ACCESS_DESCRIPTION_pop_free(x, backend._ffi.addressof(backend._lib._original_lib, 'ACCESS_DESCRIPTION_free')))
    num = backend._lib.sk_ACCESS_DESCRIPTION_num(ia)
    access_descriptions = []
    for i in range(num):
        ad = backend._lib.sk_ACCESS_DESCRIPTION_value(ia, i)
        backend.openssl_assert(ad.method != backend._ffi.NULL)
        oid = x509.ObjectIdentifier(_obj2txt(backend, ad.method))
        backend.openssl_assert(ad.location != backend._ffi.NULL)
        gn = _decode_general_name(backend, ad.location)
        access_descriptions.append(x509.AccessDescription(oid, gn))
    else:
        return access_descriptions


def _decode_authority_information_access(backend, aia):
    access_descriptions = _decode_information_access(backend, aia)
    return x509.AuthorityInformationAccess(access_descriptions)


def _decode_subject_information_access(backend, aia):
    access_descriptions = _decode_information_access(backend, aia)
    return x509.SubjectInformationAccess(access_descriptions)


def _decode_key_usage(backend, bit_string):
    bit_string = backend._ffi.cast('ASN1_BIT_STRING *', bit_string)
    bit_string = backend._ffi.gc(bit_string, backend._lib.ASN1_BIT_STRING_free)
    get_bit = backend._lib.ASN1_BIT_STRING_get_bit
    digital_signature = get_bit(bit_string, 0) == 1
    content_commitment = get_bit(bit_string, 1) == 1
    key_encipherment = get_bit(bit_string, 2) == 1
    data_encipherment = get_bit(bit_string, 3) == 1
    key_agreement = get_bit(bit_string, 4) == 1
    key_cert_sign = get_bit(bit_string, 5) == 1
    crl_sign = get_bit(bit_string, 6) == 1
    encipher_only = get_bit(bit_string, 7) == 1
    decipher_only = get_bit(bit_string, 8) == 1
    return x509.KeyUsage(digital_signature, content_commitment, key_encipherment, data_encipherment, key_agreement, key_cert_sign, crl_sign, encipher_only, decipher_only)


def _decode_general_names_extension(backend, gns):
    gns = backend._ffi.cast('GENERAL_NAMES *', gns)
    gns = backend._ffi.gc(gns, backend._lib.GENERAL_NAMES_free)
    general_names = _decode_general_names(backend, gns)
    return general_names


def _decode_subject_alt_name(backend, ext):
    return x509.SubjectAlternativeName(_decode_general_names_extension(backend, ext))


def _decode_issuer_alt_name(backend, ext):
    return x509.IssuerAlternativeName(_decode_general_names_extension(backend, ext))


def _decode_name_constraints(backend, nc):
    nc = backend._ffi.cast('NAME_CONSTRAINTS *', nc)
    nc = backend._ffi.gc(nc, backend._lib.NAME_CONSTRAINTS_free)
    permitted = _decode_general_subtrees(backend, nc.permittedSubtrees)
    excluded = _decode_general_subtrees(backend, nc.excludedSubtrees)
    return x509.NameConstraints(permitted_subtrees=permitted,
      excluded_subtrees=excluded)


def _decode_general_subtrees(backend, stack_subtrees):
    if stack_subtrees == backend._ffi.NULL:
        return
    num = backend._lib.sk_GENERAL_SUBTREE_num(stack_subtrees)
    subtrees = []
    for i in range(num):
        obj = backend._lib.sk_GENERAL_SUBTREE_value(stack_subtrees, i)
        backend.openssl_assert(obj != backend._ffi.NULL)
        name = _decode_general_name(backend, obj.base)
        subtrees.append(name)
    else:
        return subtrees


def _decode_issuing_dist_point(backend, idp):
    idp = backend._ffi.cast('ISSUING_DIST_POINT *', idp)
    idp = backend._ffi.gc(idp, backend._lib.ISSUING_DIST_POINT_free)
    if idp.distpoint != backend._ffi.NULL:
        full_name, relative_name = _decode_distpoint(backend, idp.distpoint)
    else:
        full_name = None
        relative_name = None
    only_user = idp.onlyuser == 255
    only_ca = idp.onlyCA == 255
    indirect_crl = idp.indirectCRL == 255
    only_attr = idp.onlyattr == 255
    if idp.onlysomereasons != backend._ffi.NULL:
        only_some_reasons = _decode_reasons(backend, idp.onlysomereasons)
    else:
        only_some_reasons = None
    return x509.IssuingDistributionPoint(full_name, relative_name, only_user, only_ca, only_some_reasons, indirect_crl, only_attr)


def _decode_policy_constraints(backend, pc):
    pc = backend._ffi.cast('POLICY_CONSTRAINTS *', pc)
    pc = backend._ffi.gc(pc, backend._lib.POLICY_CONSTRAINTS_free)
    require_explicit_policy = _asn1_integer_to_int_or_none(backend, pc.requireExplicitPolicy)
    inhibit_policy_mapping = _asn1_integer_to_int_or_none(backend, pc.inhibitPolicyMapping)
    return x509.PolicyConstraints(require_explicit_policy, inhibit_policy_mapping)


def _decode_extended_key_usage(backend, sk):
    sk = backend._ffi.cast('Cryptography_STACK_OF_ASN1_OBJECT *', sk)
    sk = backend._ffi.gc(sk, backend._lib.sk_ASN1_OBJECT_free)
    num = backend._lib.sk_ASN1_OBJECT_num(sk)
    ekus = []
    for i in range(num):
        obj = backend._lib.sk_ASN1_OBJECT_value(sk, i)
        backend.openssl_assert(obj != backend._ffi.NULL)
        oid = x509.ObjectIdentifier(_obj2txt(backend, obj))
        ekus.append(oid)
    else:
        return x509.ExtendedKeyUsage(ekus)


_DISTPOINT_TYPE_FULLNAME = 0
_DISTPOINT_TYPE_RELATIVENAME = 1

def _decode_dist_points(backend, cdps):
    cdps = backend._ffi.cast('Cryptography_STACK_OF_DIST_POINT *', cdps)
    cdps = backend._ffi.gc(cdps, backend._lib.CRL_DIST_POINTS_free)
    num = backend._lib.sk_DIST_POINT_num(cdps)
    dist_points = []
    for i in range(num):
        full_name = None
        relative_name = None
        crl_issuer = None
        reasons = None
        cdp = backend._lib.sk_DIST_POINT_value(cdps, i)
        if cdp.reasons != backend._ffi.NULL:
            reasons = _decode_reasons(backend, cdp.reasons)
        else:
            if cdp.CRLissuer != backend._ffi.NULL:
                crl_issuer = _decode_general_names(backend, cdp.CRLissuer)
            if cdp.distpoint != backend._ffi.NULL:
                full_name, relative_name = _decode_distpoint(backend, cdp.distpoint)
            dist_points.append(x509.DistributionPoint(full_name, relative_name, reasons, crl_issuer))
    else:
        return dist_points


_REASON_BIT_MAPPING = {1:x509.ReasonFlags.key_compromise, 
 2:x509.ReasonFlags.ca_compromise, 
 3:x509.ReasonFlags.affiliation_changed, 
 4:x509.ReasonFlags.superseded, 
 5:x509.ReasonFlags.cessation_of_operation, 
 6:x509.ReasonFlags.certificate_hold, 
 7:x509.ReasonFlags.privilege_withdrawn, 
 8:x509.ReasonFlags.aa_compromise}

def _decode_reasons(backend, reasons):
    enum_reasons = []
    for bit_position, reason in _REASON_BIT_MAPPING.items():
        if backend._lib.ASN1_BIT_STRING_get_bit(reasons, bit_position):
            enum_reasons.append(reason)
    else:
        return frozenset(enum_reasons)


def _decode_distpoint(backend, distpoint):
    if distpoint.type == _DISTPOINT_TYPE_FULLNAME:
        full_name = _decode_general_names(backend, distpoint.name.fullname)
        return (
         full_name, None)
    rns = distpoint.name.relativename
    rnum = backend._lib.sk_X509_NAME_ENTRY_num(rns)
    attributes = set
    for i in range(rnum):
        rn = backend._lib.sk_X509_NAME_ENTRY_value(rns, i)
        backend.openssl_assert(rn != backend._ffi.NULL)
        attributes.add(_decode_x509_name_entry(backend, rn))
    else:
        relative_name = x509.RelativeDistinguishedName(attributes)
        return (
         None, relative_name)


def _decode_crl_distribution_points(backend, cdps):
    dist_points = _decode_dist_points(backend, cdps)
    return x509.CRLDistributionPoints(dist_points)


def _decode_freshest_crl(backend, cdps):
    dist_points = _decode_dist_points(backend, cdps)
    return x509.FreshestCRL(dist_points)


def _decode_inhibit_any_policy(backend, asn1_int):
    asn1_int = backend._ffi.cast('ASN1_INTEGER *', asn1_int)
    asn1_int = backend._ffi.gc(asn1_int, backend._lib.ASN1_INTEGER_free)
    skip_certs = _asn1_integer_to_int(backend, asn1_int)
    return x509.InhibitAnyPolicy(skip_certs)


def _decode_scts(backend, asn1_scts):
    from cryptography.hazmat.backends.openssl.x509 import _SignedCertificateTimestamp
    asn1_scts = backend._ffi.cast('Cryptography_STACK_OF_SCT *', asn1_scts)
    asn1_scts = backend._ffi.gc(asn1_scts, backend._lib.SCT_LIST_free)
    scts = []
    for i in range(backend._lib.sk_SCT_num(asn1_scts)):
        sct = backend._lib.sk_SCT_value(asn1_scts, i)
        scts.append(_SignedCertificateTimestamp(backend, asn1_scts, sct))
    else:
        return scts


def _decode_precert_signed_certificate_timestamps(backend, asn1_scts):
    return x509.PrecertificateSignedCertificateTimestamps(_decode_scts(backend, asn1_scts))


def _decode_signed_certificate_timestamps(backend, asn1_scts):
    return x509.SignedCertificateTimestamps(_decode_scts(backend, asn1_scts))


_CRL_ENTRY_REASON_CODE_TO_ENUM = {0:x509.ReasonFlags.unspecified, 
 1:x509.ReasonFlags.key_compromise, 
 2:x509.ReasonFlags.ca_compromise, 
 3:x509.ReasonFlags.affiliation_changed, 
 4:x509.ReasonFlags.superseded, 
 5:x509.ReasonFlags.cessation_of_operation, 
 6:x509.ReasonFlags.certificate_hold, 
 8:x509.ReasonFlags.remove_from_crl, 
 9:x509.ReasonFlags.privilege_withdrawn, 
 10:x509.ReasonFlags.aa_compromise}
_CRL_ENTRY_REASON_ENUM_TO_CODE = {x509.ReasonFlags.unspecified: 0, 
 x509.ReasonFlags.key_compromise: 1, 
 x509.ReasonFlags.ca_compromise: 2, 
 x509.ReasonFlags.affiliation_changed: 3, 
 x509.ReasonFlags.superseded: 4, 
 x509.ReasonFlags.cessation_of_operation: 5, 
 x509.ReasonFlags.certificate_hold: 6, 
 x509.ReasonFlags.remove_from_crl: 8, 
 x509.ReasonFlags.privilege_withdrawn: 9, 
 x509.ReasonFlags.aa_compromise: 10}

def _decode_crl_reason--- This code section failed: ---

 L. 711         0  LOAD_FAST                'backend'
                2  LOAD_ATTR                _ffi
                4  LOAD_METHOD              cast
                6  LOAD_STR                 'ASN1_ENUMERATED *'
                8  LOAD_FAST                'enum'
               10  CALL_METHOD_2         2  ''
               12  STORE_FAST               'enum'

 L. 712        14  LOAD_FAST                'backend'
               16  LOAD_ATTR                _ffi
               18  LOAD_METHOD              gc
               20  LOAD_FAST                'enum'
               22  LOAD_FAST                'backend'
               24  LOAD_ATTR                _lib
               26  LOAD_ATTR                ASN1_ENUMERATED_free
               28  CALL_METHOD_2         2  ''
               30  STORE_FAST               'enum'

 L. 713        32  LOAD_FAST                'backend'
               34  LOAD_ATTR                _lib
               36  LOAD_METHOD              ASN1_ENUMERATED_get
               38  LOAD_FAST                'enum'
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'code'

 L. 715        44  SETUP_FINALLY        62  'to 62'

 L. 716        46  LOAD_GLOBAL              x509
               48  LOAD_METHOD              CRLReason
               50  LOAD_GLOBAL              _CRL_ENTRY_REASON_CODE_TO_ENUM
               52  LOAD_FAST                'code'
               54  BINARY_SUBSCR    
               56  CALL_METHOD_1         1  ''
               58  POP_BLOCK        
               60  RETURN_VALUE     
             62_0  COME_FROM_FINALLY    44  '44'

 L. 717        62  DUP_TOP          
               64  LOAD_GLOBAL              KeyError
               66  <121>                92  ''
               68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          

 L. 718        74  LOAD_GLOBAL              ValueError
               76  LOAD_STR                 'Unsupported reason code: {}'
               78  LOAD_METHOD              format
               80  LOAD_FAST                'code'
               82  CALL_METHOD_1         1  ''
               84  CALL_FUNCTION_1       1  ''
               86  RAISE_VARARGS_1       1  'exception instance'
               88  POP_EXCEPT       
               90  JUMP_FORWARD         94  'to 94'
               92  <48>             
             94_0  COME_FROM            90  '90'

Parse error at or near `<121>' instruction at offset 66


def _decode_invalidity_date(backend, inv_date):
    generalized_time = backend._ffi.cast('ASN1_GENERALIZEDTIME *', inv_date)
    generalized_time = backend._ffi.gc(generalized_time, backend._lib.ASN1_GENERALIZEDTIME_free)
    return x509.InvalidityDate(_parse_asn1_generalized_time(backend, generalized_time))


def _decode_cert_issuer(backend, gns):
    gns = backend._ffi.cast('GENERAL_NAMES *', gns)
    gns = backend._ffi.gc(gns, backend._lib.GENERAL_NAMES_free)
    general_names = _decode_general_names(backend, gns)
    return x509.CertificateIssuer(general_names)


def _asn1_to_der(backend, asn1_type):
    buf = backend._ffi.new('unsigned char **')
    res = backend._lib.i2d_ASN1_TYPE(asn1_type, buf)
    backend.openssl_assert(res >= 0)
    backend.openssl_assert(buf[0] != backend._ffi.NULL)
    buf = backend._ffi.gc(buf, lambda buffer: backend._lib.OPENSSL_free(buffer[0]))
    return backend._ffi.buffer(buf[0], res)[:]


def _asn1_integer_to_int(backend, asn1_int):
    bn = backend._lib.ASN1_INTEGER_to_BN(asn1_int, backend._ffi.NULL)
    backend.openssl_assert(bn != backend._ffi.NULL)
    bn = backend._ffi.gc(bn, backend._lib.BN_free)
    return backend._bn_to_int(bn)


def _asn1_integer_to_int_or_none(backend, asn1_int):
    if asn1_int == backend._ffi.NULL:
        return
    return _asn1_integer_to_int(backend, asn1_int)


def _asn1_string_to_bytes(backend, asn1_string):
    return backend._ffi.buffer(asn1_string.data, asn1_string.length)[:]


def _asn1_string_to_ascii(backend, asn1_string):
    return _asn1_string_to_bytes(backend, asn1_string).decode('ascii')


def _asn1_string_to_utf8(backend, asn1_string) -> str:
    buf = backend._ffi.new('unsigned char **')
    res = backend._lib.ASN1_STRING_to_UTF8(buf, asn1_string)
    if res == -1:
        raise ValueError('Unsupported ASN1 string type. Type: {}'.format(asn1_string.type))
    backend.openssl_assert(buf[0] != backend._ffi.NULL)
    buf = backend._ffi.gc(buf, lambda buffer: backend._lib.OPENSSL_free(buffer[0]))
    return backend._ffi.buffer(buf[0], res)[:].decode('utf8')


def _parse_asn1_time(backend, asn1_time):
    backend.openssl_assert(asn1_time != backend._ffi.NULL)
    generalized_time = backend._lib.ASN1_TIME_to_generalizedtime(asn1_time, backend._ffi.NULL)
    if generalized_time == backend._ffi.NULL:
        raise ValueError("Couldn't parse ASN.1 time as generalizedtime {!r}".format(_asn1_string_to_bytes(backend, asn1_time)))
    generalized_time = backend._ffi.gc(generalized_time, backend._lib.ASN1_GENERALIZEDTIME_free)
    return _parse_asn1_generalized_time(backend, generalized_time)


def _parse_asn1_generalized_time(backend, generalized_time):
    time = _asn1_string_to_ascii(backend, backend._ffi.cast('ASN1_STRING *', generalized_time))
    return datetime.datetime.strptime(time, '%Y%m%d%H%M%SZ')


def _decode_nonce(backend, nonce):
    nonce = backend._ffi.cast('ASN1_OCTET_STRING *', nonce)
    nonce = backend._ffi.gc(nonce, backend._lib.ASN1_OCTET_STRING_free)
    return x509.OCSPNonce(_asn1_string_to_bytes(backend, nonce))


_EXTENSION_HANDLERS_BASE = {ExtensionOID.BASIC_CONSTRAINTS: _decode_basic_constraints, 
 ExtensionOID.SUBJECT_KEY_IDENTIFIER: _decode_subject_key_identifier, 
 ExtensionOID.KEY_USAGE: _decode_key_usage, 
 ExtensionOID.SUBJECT_ALTERNATIVE_NAME: _decode_subject_alt_name, 
 ExtensionOID.EXTENDED_KEY_USAGE: _decode_extended_key_usage, 
 ExtensionOID.AUTHORITY_KEY_IDENTIFIER: _decode_authority_key_identifier, 
 ExtensionOID.AUTHORITY_INFORMATION_ACCESS: _decode_authority_information_access, 
 
 ExtensionOID.SUBJECT_INFORMATION_ACCESS: _decode_subject_information_access, 
 
 ExtensionOID.CERTIFICATE_POLICIES: _decode_certificate_policies, 
 ExtensionOID.CRL_DISTRIBUTION_POINTS: _decode_crl_distribution_points, 
 ExtensionOID.FRESHEST_CRL: _decode_freshest_crl, 
 ExtensionOID.OCSP_NO_CHECK: _decode_ocsp_no_check, 
 ExtensionOID.INHIBIT_ANY_POLICY: _decode_inhibit_any_policy, 
 ExtensionOID.ISSUER_ALTERNATIVE_NAME: _decode_issuer_alt_name, 
 ExtensionOID.NAME_CONSTRAINTS: _decode_name_constraints, 
 ExtensionOID.POLICY_CONSTRAINTS: _decode_policy_constraints}
_EXTENSION_HANDLERS_SCT = {ExtensionOID.PRECERT_SIGNED_CERTIFICATE_TIMESTAMPS: _decode_precert_signed_certificate_timestamps}
_REVOKED_EXTENSION_HANDLERS = {CRLEntryExtensionOID.CRL_REASON: _decode_crl_reason, 
 CRLEntryExtensionOID.INVALIDITY_DATE: _decode_invalidity_date, 
 CRLEntryExtensionOID.CERTIFICATE_ISSUER: _decode_cert_issuer}
_CRL_EXTENSION_HANDLERS = {ExtensionOID.CRL_NUMBER: _decode_crl_number, 
 ExtensionOID.DELTA_CRL_INDICATOR: _decode_delta_crl_indicator, 
 ExtensionOID.AUTHORITY_KEY_IDENTIFIER: _decode_authority_key_identifier, 
 ExtensionOID.ISSUER_ALTERNATIVE_NAME: _decode_issuer_alt_name, 
 ExtensionOID.AUTHORITY_INFORMATION_ACCESS: _decode_authority_information_access, 
 
 ExtensionOID.ISSUING_DISTRIBUTION_POINT: _decode_issuing_dist_point, 
 ExtensionOID.FRESHEST_CRL: _decode_freshest_crl}
_OCSP_REQ_EXTENSION_HANDLERS = {OCSPExtensionOID.NONCE: _decode_nonce}
_OCSP_BASICRESP_EXTENSION_HANDLERS = {OCSPExtensionOID.NONCE: _decode_nonce}
_OCSP_SINGLERESP_EXTENSION_HANDLERS_SCT = {ExtensionOID.SIGNED_CERTIFICATE_TIMESTAMPS: _decode_signed_certificate_timestamps}