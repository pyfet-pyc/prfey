# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\cryptography\hazmat\backends\openssl\decode_asn1.py
from __future__ import absolute_import, division, print_function
import datetime, ipaddress, six
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
        set_id = backend._lib.Cryptography_X509_NAME_ENTRY_set(entry)
        if set_id != prev_set_id:
            attributes.append(set([attribute]))
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

    def __init__(self, ext_count, get_ext, handlers):
        self.ext_count = ext_count
        self.get_ext = get_ext
        self.handlers = handlers

    def parse--- This code section failed: ---

 L. 188         0  BUILD_LIST_0          0 
                2  STORE_FAST               'extensions'

 L. 189         4  LOAD_GLOBAL              set
                6  CALL_FUNCTION_0       0  ''
                8  STORE_FAST               'seen_oids'

 L. 190        10  LOAD_GLOBAL              range
               12  LOAD_FAST                'self'
               14  LOAD_METHOD              ext_count
               16  LOAD_FAST                'backend'
               18  LOAD_FAST                'x509_obj'
               20  CALL_METHOD_2         2  ''
               22  CALL_FUNCTION_1       1  ''
               24  GET_ITER         
            26_28  FOR_ITER            574  'to 574'
               30  STORE_FAST               'i'

 L. 191        32  LOAD_FAST                'self'
               34  LOAD_METHOD              get_ext
               36  LOAD_FAST                'backend'
               38  LOAD_FAST                'x509_obj'
               40  LOAD_FAST                'i'
               42  CALL_METHOD_3         3  ''
               44  STORE_FAST               'ext'

 L. 192        46  LOAD_FAST                'backend'
               48  LOAD_METHOD              openssl_assert
               50  LOAD_FAST                'ext'
               52  LOAD_FAST                'backend'
               54  LOAD_ATTR                _ffi
               56  LOAD_ATTR                NULL
               58  COMPARE_OP               !=
               60  CALL_METHOD_1         1  ''
               62  POP_TOP          

 L. 193        64  LOAD_FAST                'backend'
               66  LOAD_ATTR                _lib
               68  LOAD_METHOD              X509_EXTENSION_get_critical
               70  LOAD_FAST                'ext'
               72  CALL_METHOD_1         1  ''
               74  STORE_FAST               'crit'

 L. 194        76  LOAD_FAST                'crit'
               78  LOAD_CONST               1
               80  COMPARE_OP               ==
               82  STORE_FAST               'critical'

 L. 195        84  LOAD_GLOBAL              x509
               86  LOAD_METHOD              ObjectIdentifier

 L. 196        88  LOAD_GLOBAL              _obj2txt
               90  LOAD_FAST                'backend'
               92  LOAD_FAST                'backend'
               94  LOAD_ATTR                _lib
               96  LOAD_METHOD              X509_EXTENSION_get_object
               98  LOAD_FAST                'ext'
              100  CALL_METHOD_1         1  ''
              102  CALL_FUNCTION_2       2  ''

 L. 195       104  CALL_METHOD_1         1  ''
              106  STORE_FAST               'oid'

 L. 198       108  LOAD_FAST                'oid'
              110  LOAD_FAST                'seen_oids'
              112  COMPARE_OP               in
              114  POP_JUMP_IF_FALSE   134  'to 134'

 L. 199       116  LOAD_GLOBAL              x509
              118  LOAD_METHOD              DuplicateExtension

 L. 200       120  LOAD_STR                 'Duplicate {} extension found'
              122  LOAD_METHOD              format
              124  LOAD_FAST                'oid'
              126  CALL_METHOD_1         1  ''

 L. 200       128  LOAD_FAST                'oid'

 L. 199       130  CALL_METHOD_2         2  ''
              132  RAISE_VARARGS_1       1  'exception instance'
            134_0  COME_FROM           114  '114'

 L. 206       134  LOAD_FAST                'oid'
              136  LOAD_GLOBAL              ExtensionOID
              138  LOAD_ATTR                TLS_FEATURE
              140  COMPARE_OP               ==
          142_144  POP_JUMP_IF_FALSE   270  'to 270'

 L. 208       146  LOAD_FAST                'backend'
              148  LOAD_ATTR                _lib
              150  LOAD_METHOD              X509_EXTENSION_get_data
              152  LOAD_FAST                'ext'
              154  CALL_METHOD_1         1  ''
              156  STORE_FAST               'data'

 L. 209       158  LOAD_GLOBAL              _asn1_string_to_bytes
              160  LOAD_FAST                'backend'
              162  LOAD_FAST                'data'
              164  CALL_FUNCTION_2       2  ''
              166  STORE_FAST               'data_bytes'

 L. 210       168  LOAD_GLOBAL              DERReader
              170  LOAD_FAST                'data_bytes'
              172  CALL_FUNCTION_1       1  ''
              174  LOAD_METHOD              read_single_element
              176  LOAD_GLOBAL              SEQUENCE
              178  CALL_METHOD_1         1  ''
              180  STORE_FAST               'features'

 L. 211       182  BUILD_LIST_0          0 
              184  STORE_FAST               'parsed'

 L. 212       186  LOAD_FAST                'features'
              188  LOAD_METHOD              is_empty
              190  CALL_METHOD_0         0  ''
              192  POP_JUMP_IF_TRUE    216  'to 216'

 L. 213       194  LOAD_FAST                'parsed'
              196  LOAD_METHOD              append
              198  LOAD_FAST                'features'
              200  LOAD_METHOD              read_element
              202  LOAD_GLOBAL              INTEGER
              204  CALL_METHOD_1         1  ''
              206  LOAD_METHOD              as_integer
              208  CALL_METHOD_0         0  ''
              210  CALL_METHOD_1         1  ''
              212  POP_TOP          
              214  JUMP_BACK           186  'to 186'
            216_0  COME_FROM           192  '192'

 L. 215       216  LOAD_GLOBAL              x509
              218  LOAD_METHOD              TLSFeature

 L. 216       220  LOAD_LISTCOMP            '<code_object <listcomp>>'
              222  LOAD_STR                 '_X509ExtensionParser.parse.<locals>.<listcomp>'
              224  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              226  LOAD_FAST                'parsed'
              228  GET_ITER         
              230  CALL_FUNCTION_1       1  ''

 L. 215       232  CALL_METHOD_1         1  ''
              234  STORE_FAST               'value'

 L. 218       236  LOAD_FAST                'extensions'
              238  LOAD_METHOD              append
              240  LOAD_GLOBAL              x509
              242  LOAD_METHOD              Extension
              244  LOAD_FAST                'oid'
              246  LOAD_FAST                'critical'
              248  LOAD_FAST                'value'
              250  CALL_METHOD_3         3  ''
              252  CALL_METHOD_1         1  ''
              254  POP_TOP          

 L. 219       256  LOAD_FAST                'seen_oids'
              258  LOAD_METHOD              add
              260  LOAD_FAST                'oid'
              262  CALL_METHOD_1         1  ''
              264  POP_TOP          

 L. 220       266  JUMP_BACK            26  'to 26'
              268  JUMP_FORWARD        358  'to 358'
            270_0  COME_FROM           142  '142'

 L. 221       270  LOAD_FAST                'oid'
              272  LOAD_GLOBAL              ExtensionOID
              274  LOAD_ATTR                PRECERT_POISON
              276  COMPARE_OP               ==
          278_280  POP_JUMP_IF_FALSE   358  'to 358'

 L. 222       282  LOAD_FAST                'backend'
              284  LOAD_ATTR                _lib
              286  LOAD_METHOD              X509_EXTENSION_get_data
              288  LOAD_FAST                'ext'
              290  CALL_METHOD_1         1  ''
              292  STORE_FAST               'data'

 L. 224       294  LOAD_GLOBAL              DERReader
              296  LOAD_GLOBAL              _asn1_string_to_bytes
              298  LOAD_FAST                'backend'
              300  LOAD_FAST                'data'
              302  CALL_FUNCTION_2       2  ''
              304  CALL_FUNCTION_1       1  ''
              306  STORE_FAST               'reader'

 L. 225       308  LOAD_FAST                'reader'
              310  LOAD_METHOD              read_single_element
              312  LOAD_GLOBAL              NULL
              314  CALL_METHOD_1         1  ''
              316  LOAD_METHOD              check_empty
              318  CALL_METHOD_0         0  ''
              320  POP_TOP          

 L. 226       322  LOAD_FAST                'extensions'
              324  LOAD_METHOD              append
              326  LOAD_GLOBAL              x509
              328  LOAD_METHOD              Extension

 L. 227       330  LOAD_FAST                'oid'

 L. 227       332  LOAD_FAST                'critical'

 L. 227       334  LOAD_GLOBAL              x509
              336  LOAD_METHOD              PrecertPoison
              338  CALL_METHOD_0         0  ''

 L. 226       340  CALL_METHOD_3         3  ''
              342  CALL_METHOD_1         1  ''
              344  POP_TOP          

 L. 229       346  LOAD_FAST                'seen_oids'
              348  LOAD_METHOD              add
              350  LOAD_FAST                'oid'
              352  CALL_METHOD_1         1  ''
              354  POP_TOP          

 L. 230       356  JUMP_BACK            26  'to 26'
            358_0  COME_FROM           278  '278'
            358_1  COME_FROM           268  '268'

 L. 232       358  SETUP_FINALLY       374  'to 374'

 L. 233       360  LOAD_FAST                'self'
              362  LOAD_ATTR                handlers
              364  LOAD_FAST                'oid'
              366  BINARY_SUBSCR    
              368  STORE_FAST               'handler'
              370  POP_BLOCK        
              372  JUMP_FORWARD        484  'to 484'
            374_0  COME_FROM_FINALLY   358  '358'

 L. 234       374  DUP_TOP          
              376  LOAD_GLOBAL              KeyError
              378  COMPARE_OP               exception-match
          380_382  POP_JUMP_IF_FALSE   482  'to 482'
              384  POP_TOP          
              386  POP_TOP          
              388  POP_TOP          

 L. 236       390  LOAD_FAST                'backend'
              392  LOAD_ATTR                _lib
              394  LOAD_METHOD              X509_EXTENSION_get_data
              396  LOAD_FAST                'ext'
              398  CALL_METHOD_1         1  ''
              400  STORE_FAST               'data'

 L. 237       402  LOAD_FAST                'backend'
              404  LOAD_METHOD              openssl_assert
              406  LOAD_FAST                'data'
              408  LOAD_FAST                'backend'
              410  LOAD_ATTR                _ffi
              412  LOAD_ATTR                NULL
              414  COMPARE_OP               !=
              416  CALL_METHOD_1         1  ''
              418  POP_TOP          

 L. 238       420  LOAD_FAST                'backend'
              422  LOAD_ATTR                _ffi
              424  LOAD_METHOD              buffer
              426  LOAD_FAST                'data'
              428  LOAD_ATTR                data
              430  LOAD_FAST                'data'
              432  LOAD_ATTR                length
              434  CALL_METHOD_2         2  ''
              436  LOAD_CONST               None
              438  LOAD_CONST               None
              440  BUILD_SLICE_2         2 
              442  BINARY_SUBSCR    
              444  STORE_FAST               'der'

 L. 239       446  LOAD_GLOBAL              x509
              448  LOAD_METHOD              UnrecognizedExtension
              450  LOAD_FAST                'oid'
              452  LOAD_FAST                'der'
              454  CALL_METHOD_2         2  ''
              456  STORE_FAST               'unrecognized'

 L. 240       458  LOAD_FAST                'extensions'
              460  LOAD_METHOD              append

 L. 241       462  LOAD_GLOBAL              x509
              464  LOAD_METHOD              Extension
              466  LOAD_FAST                'oid'
              468  LOAD_FAST                'critical'
              470  LOAD_FAST                'unrecognized'
              472  CALL_METHOD_3         3  ''

 L. 240       474  CALL_METHOD_1         1  ''
              476  POP_TOP          
              478  POP_EXCEPT       
              480  JUMP_FORWARD        562  'to 562'
            482_0  COME_FROM           380  '380'
              482  END_FINALLY      
            484_0  COME_FROM           372  '372'

 L. 244       484  LOAD_FAST                'backend'
              486  LOAD_ATTR                _lib
              488  LOAD_METHOD              X509V3_EXT_d2i
              490  LOAD_FAST                'ext'
              492  CALL_METHOD_1         1  ''
              494  STORE_FAST               'ext_data'

 L. 245       496  LOAD_FAST                'ext_data'
              498  LOAD_FAST                'backend'
              500  LOAD_ATTR                _ffi
              502  LOAD_ATTR                NULL
              504  COMPARE_OP               ==
          506_508  POP_JUMP_IF_FALSE   532  'to 532'

 L. 246       510  LOAD_FAST                'backend'
              512  LOAD_METHOD              _consume_errors
              514  CALL_METHOD_0         0  ''
              516  POP_TOP          

 L. 247       518  LOAD_GLOBAL              ValueError

 L. 248       520  LOAD_STR                 "The {} extension is invalid and can't be parsed"
              522  LOAD_METHOD              format

 L. 249       524  LOAD_FAST                'oid'

 L. 248       526  CALL_METHOD_1         1  ''

 L. 247       528  CALL_FUNCTION_1       1  ''
              530  RAISE_VARARGS_1       1  'exception instance'
            532_0  COME_FROM           506  '506'

 L. 252       532  LOAD_FAST                'handler'
              534  LOAD_FAST                'backend'
              536  LOAD_FAST                'ext_data'
              538  CALL_FUNCTION_2       2  ''
              540  STORE_FAST               'value'

 L. 253       542  LOAD_FAST                'extensions'
              544  LOAD_METHOD              append
              546  LOAD_GLOBAL              x509
              548  LOAD_METHOD              Extension
              550  LOAD_FAST                'oid'
              552  LOAD_FAST                'critical'
              554  LOAD_FAST                'value'
              556  CALL_METHOD_3         3  ''
              558  CALL_METHOD_1         1  ''
              560  POP_TOP          
            562_0  COME_FROM           480  '480'

 L. 255       562  LOAD_FAST                'seen_oids'
              564  LOAD_METHOD              add
              566  LOAD_FAST                'oid'
              568  CALL_METHOD_1         1  ''
              570  POP_TOP          
              572  JUMP_BACK            26  'to 26'

 L. 257       574  LOAD_GLOBAL              x509
              576  LOAD_METHOD              Extensions
              578  LOAD_FAST                'extensions'
              580  CALL_METHOD_1         1  ''
              582  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 268


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


def _decode_authority_information_access(backend, aia):
    aia = backend._ffi.cast('Cryptography_STACK_OF_ACCESS_DESCRIPTION *', aia)
    aia = backend._ffi.gc(aia, lambda x: backend._lib.sk_ACCESS_DESCRIPTION_pop_free(x, backend._ffi.addressof(backend._lib._original_lib, 'ACCESS_DESCRIPTION_free')))
    num = backend._lib.sk_ACCESS_DESCRIPTION_num(aia)
    access_descriptions = []
    for i in range(num):
        ad = backend._lib.sk_ACCESS_DESCRIPTION_value(aia, i)
        backend.openssl_assert(ad.method != backend._ffi.NULL)
        oid = x509.ObjectIdentifier(_obj2txt(backend, ad.method))
        backend.openssl_assert(ad.location != backend._ffi.NULL)
        gn = _decode_general_name(backend, ad.location)
        access_descriptions.append(x509.AccessDescription(oid, gn))
    else:
        return x509.AuthorityInformationAccess(access_descriptions)


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
    for bit_position, reason in six.iteritems(_REASON_BIT_MAPPING):
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


def _decode_precert_signed_certificate_timestamps(backend, asn1_scts):
    from cryptography.hazmat.backends.openssl.x509 import _SignedCertificateTimestamp
    asn1_scts = backend._ffi.cast('Cryptography_STACK_OF_SCT *', asn1_scts)
    asn1_scts = backend._ffi.gc(asn1_scts, backend._lib.SCT_LIST_free)
    scts = []
    for i in range(backend._lib.sk_SCT_num(asn1_scts)):
        sct = backend._lib.sk_SCT_value(asn1_scts, i)
        scts.append(_SignedCertificateTimestamp(backend, asn1_scts, sct))
    else:
        return x509.PrecertificateSignedCertificateTimestamps(scts)


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

 L. 701         0  LOAD_FAST                'backend'
                2  LOAD_ATTR                _ffi
                4  LOAD_METHOD              cast
                6  LOAD_STR                 'ASN1_ENUMERATED *'
                8  LOAD_FAST                'enum'
               10  CALL_METHOD_2         2  ''
               12  STORE_FAST               'enum'

 L. 702        14  LOAD_FAST                'backend'
               16  LOAD_ATTR                _ffi
               18  LOAD_METHOD              gc
               20  LOAD_FAST                'enum'
               22  LOAD_FAST                'backend'
               24  LOAD_ATTR                _lib
               26  LOAD_ATTR                ASN1_ENUMERATED_free
               28  CALL_METHOD_2         2  ''
               30  STORE_FAST               'enum'

 L. 703        32  LOAD_FAST                'backend'
               34  LOAD_ATTR                _lib
               36  LOAD_METHOD              ASN1_ENUMERATED_get
               38  LOAD_FAST                'enum'
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'code'

 L. 705        44  SETUP_FINALLY        62  'to 62'

 L. 706        46  LOAD_GLOBAL              x509
               48  LOAD_METHOD              CRLReason
               50  LOAD_GLOBAL              _CRL_ENTRY_REASON_CODE_TO_ENUM
               52  LOAD_FAST                'code'
               54  BINARY_SUBSCR    
               56  CALL_METHOD_1         1  ''
               58  POP_BLOCK        
               60  RETURN_VALUE     
             62_0  COME_FROM_FINALLY    44  '44'

 L. 707        62  DUP_TOP          
               64  LOAD_GLOBAL              KeyError
               66  COMPARE_OP               exception-match
               68  POP_JUMP_IF_FALSE    94  'to 94'
               70  POP_TOP          
               72  POP_TOP          
               74  POP_TOP          

 L. 708        76  LOAD_GLOBAL              ValueError
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


def _asn1_string_to_utf8(backend, asn1_string):
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


_EXTENSION_HANDLERS_NO_SCT = {ExtensionOID.BASIC_CONSTRAINTS: _decode_basic_constraints, 
 ExtensionOID.SUBJECT_KEY_IDENTIFIER: _decode_subject_key_identifier, 
 ExtensionOID.KEY_USAGE: _decode_key_usage, 
 ExtensionOID.SUBJECT_ALTERNATIVE_NAME: _decode_subject_alt_name, 
 ExtensionOID.EXTENDED_KEY_USAGE: _decode_extended_key_usage, 
 ExtensionOID.AUTHORITY_KEY_IDENTIFIER: _decode_authority_key_identifier, 
 ExtensionOID.AUTHORITY_INFORMATION_ACCESS: _decode_authority_information_access, 
 
 ExtensionOID.CERTIFICATE_POLICIES: _decode_certificate_policies, 
 ExtensionOID.CRL_DISTRIBUTION_POINTS: _decode_crl_distribution_points, 
 ExtensionOID.FRESHEST_CRL: _decode_freshest_crl, 
 ExtensionOID.OCSP_NO_CHECK: _decode_ocsp_no_check, 
 ExtensionOID.INHIBIT_ANY_POLICY: _decode_inhibit_any_policy, 
 ExtensionOID.ISSUER_ALTERNATIVE_NAME: _decode_issuer_alt_name, 
 ExtensionOID.NAME_CONSTRAINTS: _decode_name_constraints, 
 ExtensionOID.POLICY_CONSTRAINTS: _decode_policy_constraints}
_EXTENSION_HANDLERS = _EXTENSION_HANDLERS_NO_SCT.copy()
_EXTENSION_HANDLERS[ExtensionOID.PRECERT_SIGNED_CERTIFICATE_TIMESTAMPS] = _decode_precert_signed_certificate_timestamps
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
_CERTIFICATE_EXTENSION_PARSER_NO_SCT = _X509ExtensionParser(ext_count=(lambda backend, x: backend._lib.X509_get_ext_count(x)),
  get_ext=(lambda backend, x, i: backend._lib.X509_get_ext(x, i)),
  handlers=_EXTENSION_HANDLERS_NO_SCT)
_CERTIFICATE_EXTENSION_PARSER = _X509ExtensionParser(ext_count=(lambda backend, x: backend._lib.X509_get_ext_count(x)),
  get_ext=(lambda backend, x, i: backend._lib.X509_get_ext(x, i)),
  handlers=_EXTENSION_HANDLERS)
_CSR_EXTENSION_PARSER = _X509ExtensionParser(ext_count=(lambda backend, x: backend._lib.sk_X509_EXTENSION_num(x)),
  get_ext=(lambda backend, x, i: backend._lib.sk_X509_EXTENSION_value(x, i)),
  handlers=_EXTENSION_HANDLERS)
_REVOKED_CERTIFICATE_EXTENSION_PARSER = _X509ExtensionParser(ext_count=(lambda backend, x: backend._lib.X509_REVOKED_get_ext_count(x)),
  get_ext=(lambda backend, x, i: backend._lib.X509_REVOKED_get_ext(x, i)),
  handlers=_REVOKED_EXTENSION_HANDLERS)
_CRL_EXTENSION_PARSER = _X509ExtensionParser(ext_count=(lambda backend, x: backend._lib.X509_CRL_get_ext_count(x)),
  get_ext=(lambda backend, x, i: backend._lib.X509_CRL_get_ext(x, i)),
  handlers=_CRL_EXTENSION_HANDLERS)
_OCSP_REQ_EXT_PARSER = _X509ExtensionParser(ext_count=(lambda backend, x: backend._lib.OCSP_REQUEST_get_ext_count(x)),
  get_ext=(lambda backend, x, i: backend._lib.OCSP_REQUEST_get_ext(x, i)),
  handlers=_OCSP_REQ_EXTENSION_HANDLERS)
_OCSP_BASICRESP_EXT_PARSER = _X509ExtensionParser(ext_count=(lambda backend, x: backend._lib.OCSP_BASICRESP_get_ext_count(x)),
  get_ext=(lambda backend, x, i: backend._lib.OCSP_BASICRESP_get_ext(x, i)),
  handlers=_OCSP_BASICRESP_EXTENSION_HANDLERS)