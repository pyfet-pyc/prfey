# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
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


def _decode_general_name(backend, gn):
    if gn.type == backend._lib.GEN_DNS:
        data = _asn1_string_to_bytes(backend, gn.d.dNSName).decode('utf8')
        return x509.DNSName._init_without_validation(data)
    else:
        if gn.type == backend._lib.GEN_URI:
            data = _asn1_string_to_bytes(backend, gn.d.uniformResourceIdentifier).decode('utf8')
            return x509.UniformResourceIdentifier._init_without_validation(data)
        elif gn.type == backend._lib.GEN_RID:
            oid = _obj2txt(backend, gn.d.registeredID)
            return x509.RegisteredID(x509.ObjectIdentifier(oid))
            if gn.type == backend._lib.GEN_IPADD:
                data = _asn1_string_to_bytes(backend, gn.d.iPAddress)
                data_len = len(data)
                if data_len == 8 or data_len == 32:
                    base = ipaddress.ip_address(data[:data_len // 2])
                    netmask = ipaddress.ip_address(data[data_len // 2:])
                    bits = bin(int(netmask))[2:]
                    prefix = bits.find('0')
                    if prefix == -1:
                        prefix = len(bits)
                    if '1' in bits[prefix:]:
                        raise ValueError('Invalid netmask')
                    ip = ipaddress.ip_network(base.exploded + '/{}'.format(prefix))
        else:
            ip = ipaddress.ip_address(data)
        return x509.IPAddress(ip)
    if gn.type == backend._lib.GEN_DIRNAME:
        return x509.DirectoryName(_decode_x509_name(backend, gn.d.directoryName))
    if gn.type == backend._lib.GEN_EMAIL:
        data = _asn1_string_to_bytes(backend, gn.d.rfc822Name).decode('utf8')
        return x509.RFC822Name._init_without_validation(data)
    if gn.type == backend._lib.GEN_OTHERNAME:
        type_id = _obj2txt(backend, gn.d.otherName.type_id)
        value = _asn1_to_der(backend, gn.d.otherName.value)
        return x509.OtherName(x509.ObjectIdentifier(type_id), value)
    raise x509.UnsupportedGeneralNameType('{} is not a supported type'.format(x509._GENERAL_NAMES.get(gn.type, gn.type)), gn.type)


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
            24_26  FOR_ITER            604  'to 604'
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
              118  COMPARE_OP               in
              120  POP_JUMP_IF_FALSE   140  'to 140'

 L. 202       122  LOAD_GLOBAL              x509
              124  LOAD_METHOD              DuplicateExtension

 L. 203       126  LOAD_STR                 'Duplicate {} extension found'
              128  LOAD_METHOD              format
              130  LOAD_FAST                'oid'
              132  CALL_METHOD_1         1  ''

 L. 203       134  LOAD_FAST                'oid'

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
              386  JUMP_FORWARD        506  'to 506'
            388_0  COME_FROM_FINALLY   372  '372'

 L. 237       388  DUP_TOP          
              390  LOAD_GLOBAL              KeyError
              392  COMPARE_OP               exception-match
          394_396  POP_JUMP_IF_FALSE   504  'to 504'
              398  POP_TOP          
              400  POP_TOP          
              402  POP_TOP          

 L. 239       404  LOAD_FAST                'self'
              406  LOAD_ATTR                _backend
              408  LOAD_ATTR                _lib
              410  LOAD_METHOD              X509_EXTENSION_get_data
              412  LOAD_FAST                'ext'
              414  CALL_METHOD_1         1  ''
              416  STORE_FAST               'data'

 L. 240       418  LOAD_FAST                'self'
              420  LOAD_ATTR                _backend
              422  LOAD_METHOD              openssl_assert
              424  LOAD_FAST                'data'
              426  LOAD_FAST                'self'
              428  LOAD_ATTR                _backend
              430  LOAD_ATTR                _ffi
              432  LOAD_ATTR                NULL
              434  COMPARE_OP               !=
              436  CALL_METHOD_1         1  ''
              438  POP_TOP          

 L. 241       440  LOAD_FAST                'self'
              442  LOAD_ATTR                _backend
              444  LOAD_ATTR                _ffi
              446  LOAD_METHOD              buffer
              448  LOAD_FAST                'data'
              450  LOAD_ATTR                data
              452  LOAD_FAST                'data'
              454  LOAD_ATTR                length
              456  CALL_METHOD_2         2  ''
              458  LOAD_CONST               None
              460  LOAD_CONST               None
              462  BUILD_SLICE_2         2 
              464  BINARY_SUBSCR    
              466  STORE_FAST               'der'

 L. 242       468  LOAD_GLOBAL              x509
              470  LOAD_METHOD              UnrecognizedExtension
              472  LOAD_FAST                'oid'
              474  LOAD_FAST                'der'
              476  CALL_METHOD_2         2  ''
              478  STORE_FAST               'unrecognized'

 L. 243       480  LOAD_FAST                'extensions'
              482  LOAD_METHOD              append
              484  LOAD_GLOBAL              x509
              486  LOAD_METHOD              Extension
              488  LOAD_FAST                'oid'
              490  LOAD_FAST                'critical'
              492  LOAD_FAST                'unrecognized'
              494  CALL_METHOD_3         3  ''
              496  CALL_METHOD_1         1  ''
              498  POP_TOP          
              500  POP_EXCEPT       
              502  JUMP_FORWARD        592  'to 592'
            504_0  COME_FROM           394  '394'
              504  END_FINALLY      
            506_0  COME_FROM           386  '386'

 L. 245       506  LOAD_FAST                'self'
              508  LOAD_ATTR                _backend
              510  LOAD_ATTR                _lib
              512  LOAD_METHOD              X509V3_EXT_d2i
              514  LOAD_FAST                'ext'
              516  CALL_METHOD_1         1  ''
              518  STORE_FAST               'ext_data'

 L. 246       520  LOAD_FAST                'ext_data'
              522  LOAD_FAST                'self'
              524  LOAD_ATTR                _backend
              526  LOAD_ATTR                _ffi
              528  LOAD_ATTR                NULL
              530  COMPARE_OP               ==
          532_534  POP_JUMP_IF_FALSE   560  'to 560'

 L. 247       536  LOAD_FAST                'self'
              538  LOAD_ATTR                _backend
              540  LOAD_METHOD              _consume_errors
              542  CALL_METHOD_0         0  ''
              544  POP_TOP          

 L. 248       546  LOAD_GLOBAL              ValueError

 L. 249       548  LOAD_STR                 "The {} extension is invalid and can't be parsed"
              550  LOAD_METHOD              format

 L. 250       552  LOAD_FAST                'oid'

 L. 249       554  CALL_METHOD_1         1  ''

 L. 248       556  CALL_FUNCTION_1       1  ''
              558  RAISE_VARARGS_1       1  'exception instance'
            560_0  COME_FROM           532  '532'

 L. 253       560  LOAD_FAST                'handler'
              562  LOAD_FAST                'self'
              564  LOAD_ATTR                _backend
              566  LOAD_FAST                'ext_data'
              568  CALL_FUNCTION_2       2  ''
              570  STORE_FAST               'value'

 L. 254       572  LOAD_FAST                'extensions'
              574  LOAD_METHOD              append
              576  LOAD_GLOBAL              x509
              578  LOAD_METHOD              Extension
              580  LOAD_FAST                'oid'
              582  LOAD_FAST                'critical'
              584  LOAD_FAST                'value'
              586  CALL_METHOD_3         3  ''
              588  CALL_METHOD_1         1  ''
              590  POP_TOP          
            592_0  COME_FROM           502  '502'

 L. 256       592  LOAD_FAST                'seen_oids'
              594  LOAD_METHOD              add
              596  LOAD_FAST                'oid'
              598  CALL_METHOD_1         1  ''
              600  POP_TOP          
              602  JUMP_BACK            24  'to 24'

 L. 258       604  LOAD_GLOBAL              x509
              606  LOAD_METHOD              Extensions
              608  LOAD_FAST                'extensions'
              610  CALL_METHOD_1         1  ''
              612  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 278


def _decode_certificate_policies(backend, cp):
    cp = backend._ffi.cast('Cryptography_STACK_OF_POLICYINFO *', cp)
    cp = backend._ffi.gc(cp, backend._lib.CERTIFICATEPOLICIES_free)
    num = backend._lib.sk_POLICYINFO_num(cp)
    certificate_policies = []
    for i in range(num):
        qualifiers = None
        pi = backend._lib.sk_POLICYINFO_value(cp, i)
        oid = x509.ObjectIdentifier(_obj2txt(backend, pi.policyid))
        if pi.qualifiers != backend._ffi.NULL:
            qnum = backend._lib.sk_POLICYQUALINFO_num(pi.qualifiers)
            qualifiers = []
            for j in range(qnum):
                pqi = backend._lib.sk_POLICYQUALINFO_value(pi.qualifiers, j)
                pqualid = x509.ObjectIdentifier(_obj2txt(backend, pqi.pqualid))

            if pqualid == CertificatePoliciesOID.CPS_QUALIFIER:
                cpsuri = backend._ffi.buffer(pqi.d.cpsuri.data, pqi.d.cpsuri.length)[:].decode('ascii')
                qualifiers.append(cpsuri)
            else:
                assert pqualid == CertificatePoliciesOID.CPS_USER_NOTICE
                user_notice = _decode_user_notice(backend, pqi.d.usernotice)
                qualifiers.append(user_notice)
        else:
            certificate_policies.append(x509.PolicyInformation(oid, qualifiers))
    else:
        return x509.CertificatePolicies(certificate_policies)


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
        return frozenset(enum_reasons)


def _decode_distpoint(backend, distpoint):
    if distpoint.type == _DISTPOINT_TYPE_FULLNAME:
        full_name = _decode_general_names(backend, distpoint.name.fullname)
        return (full_name, None)
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
               66  COMPARE_OP               exception-match
               68  POP_JUMP_IF_FALSE    94  'to 94'
               70  POP_TOP          
               72  POP_TOP          
               74  POP_TOP          

 L. 718        76  LOAD_GLOBAL              ValueError
               78  LOAD_STR                 'Unsupported reason code: {}'
               80  LOAD_METHOD              format
               82  LOAD_FAST                'code'
               84  CALL_METHOD_1         1  ''
               86  CALL_FUNCTION_1       1  ''
               88  RAISE_VARARGS_1       1  'exception instance'
               90  POP_EXCEPT       
               92  JUMP_FORWARD         96  'to 96'
             94_0  COME_FROM            68  '68'
               94  END_FINALLY      
             96_0  COME_FROM            92  '92'

Parse error at or near `POP_TOP' instruction at offset 72


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