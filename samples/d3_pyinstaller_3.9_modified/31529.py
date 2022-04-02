# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\backends\openssl\encode_asn1.py
from __future__ import absolute_import, division, print_function
import calendar, ipaddress, six
from cryptography import utils, x509
from cryptography.hazmat.backends.openssl.decode_asn1 import _CRL_ENTRY_REASON_ENUM_TO_CODE, _DISTPOINT_TYPE_FULLNAME, _DISTPOINT_TYPE_RELATIVENAME
from cryptography.x509.name import _ASN1Type
from cryptography.x509.oid import CRLEntryExtensionOID, ExtensionOID, OCSPExtensionOID

def _encode_asn1_int(backend, x):
    """
    Converts a python integer to an ASN1_INTEGER. The returned ASN1_INTEGER
    will not be garbage collected (to support adding them to structs that take
    ownership of the object). Be sure to register it for GC if it will be
    discarded after use.

    """
    i = backend._int_to_bn(x)
    i = backend._ffi.gc(i, backend._lib.BN_free)
    i = backend._lib.BN_to_ASN1_INTEGER(i, backend._ffi.NULL)
    backend.openssl_assert(i != backend._ffi.NULL)
    return i


def _encode_asn1_int_gc(backend, x):
    i = _encode_asn1_int(backend, x)
    i = backend._ffi.gc(i, backend._lib.ASN1_INTEGER_free)
    return i


def _encode_asn1_str(backend, data):
    """
    Create an ASN1_OCTET_STRING from a Python byte string.
    """
    s = backend._lib.ASN1_OCTET_STRING_new()
    res = backend._lib.ASN1_OCTET_STRING_set(s, data, len(data))
    backend.openssl_assert(res == 1)
    return s


def _encode_asn1_utf8_str(backend, string):
    """
    Create an ASN1_UTF8STRING from a Python unicode string.
    This object will be an ASN1_STRING with UTF8 type in OpenSSL and
    can be decoded with ASN1_STRING_to_UTF8.
    """
    s = backend._lib.ASN1_UTF8STRING_new()
    res = backend._lib.ASN1_STRING_set(s, string.encode('utf8'), len(string.encode('utf8')))
    backend.openssl_assert(res == 1)
    return s


def _encode_asn1_str_gc(backend, data):
    s = _encode_asn1_str(backend, data)
    s = backend._ffi.gc(s, backend._lib.ASN1_OCTET_STRING_free)
    return s


def _encode_inhibit_any_policy(backend, inhibit_any_policy):
    return _encode_asn1_int_gc(backend, inhibit_any_policy.skip_certs)


def _encode_name(backend, name):
    """
    The X509_NAME created will not be gc'd. Use _encode_name_gc if needed.
    """
    subject = backend._lib.X509_NAME_new()
    for rdn in name.rdns:
        set_flag = 0
        for attribute in rdn:
            name_entry = _encode_name_entry(backend, attribute)
            name_entry = backend._ffi.gc(name_entry, backend._lib.X509_NAME_ENTRY_free)
            res = backend._lib.X509_NAME_add_entry(subject, name_entry, -1, set_flag)
            backend.openssl_assert(res == 1)
            set_flag = -1

    else:
        return subject


def _encode_name_gc(backend, attributes):
    subject = _encode_name(backend, attributes)
    subject = backend._ffi.gc(subject, backend._lib.X509_NAME_free)
    return subject


def _encode_sk_name_entry(backend, attributes):
    """
    The sk_X509_NAME_ENTRY created will not be gc'd.
    """
    stack = backend._lib.sk_X509_NAME_ENTRY_new_null()
    for attribute in attributes:
        name_entry = _encode_name_entry(backend, attribute)
        res = backend._lib.sk_X509_NAME_ENTRY_push(stack, name_entry)
        backend.openssl_assert(res >= 1)
    else:
        return stack


def _encode_name_entry--- This code section failed: ---

 L. 126         0  LOAD_FAST                'attribute'
                2  LOAD_ATTR                _type
                4  LOAD_GLOBAL              _ASN1Type
                6  LOAD_ATTR                BMPString
                8  <117>                 0  ''
               10  POP_JUMP_IF_FALSE    26  'to 26'

 L. 127        12  LOAD_FAST                'attribute'
               14  LOAD_ATTR                value
               16  LOAD_METHOD              encode
               18  LOAD_STR                 'utf_16_be'
               20  CALL_METHOD_1         1  ''
               22  STORE_FAST               'value'
               24  JUMP_FORWARD         64  'to 64'
             26_0  COME_FROM            10  '10'

 L. 128        26  LOAD_FAST                'attribute'
               28  LOAD_ATTR                _type
               30  LOAD_GLOBAL              _ASN1Type
               32  LOAD_ATTR                UniversalString
               34  <117>                 0  ''
               36  POP_JUMP_IF_FALSE    52  'to 52'

 L. 129        38  LOAD_FAST                'attribute'
               40  LOAD_ATTR                value
               42  LOAD_METHOD              encode
               44  LOAD_STR                 'utf_32_be'
               46  CALL_METHOD_1         1  ''
               48  STORE_FAST               'value'
               50  JUMP_FORWARD         64  'to 64'
             52_0  COME_FROM            36  '36'

 L. 131        52  LOAD_FAST                'attribute'
               54  LOAD_ATTR                value
               56  LOAD_METHOD              encode
               58  LOAD_STR                 'utf8'
               60  CALL_METHOD_1         1  ''
               62  STORE_FAST               'value'
             64_0  COME_FROM            50  '50'
             64_1  COME_FROM            24  '24'

 L. 133        64  LOAD_GLOBAL              _txt2obj_gc
               66  LOAD_FAST                'backend'
               68  LOAD_FAST                'attribute'
               70  LOAD_ATTR                oid
               72  LOAD_ATTR                dotted_string
               74  CALL_FUNCTION_2       2  ''
               76  STORE_FAST               'obj'

 L. 135        78  LOAD_FAST                'backend'
               80  LOAD_ATTR                _lib
               82  LOAD_METHOD              X509_NAME_ENTRY_create_by_OBJ

 L. 136        84  LOAD_FAST                'backend'
               86  LOAD_ATTR                _ffi
               88  LOAD_ATTR                NULL
               90  LOAD_FAST                'obj'
               92  LOAD_FAST                'attribute'
               94  LOAD_ATTR                _type
               96  LOAD_ATTR                value
               98  LOAD_FAST                'value'
              100  LOAD_GLOBAL              len
              102  LOAD_FAST                'value'
              104  CALL_FUNCTION_1       1  ''

 L. 135       106  CALL_METHOD_5         5  ''
              108  STORE_FAST               'name_entry'

 L. 138       110  LOAD_FAST                'name_entry'
              112  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def _encode_crl_number_delta_crl_indicator(backend, ext):
    return _encode_asn1_int_gc(backend, ext.crl_number)


def _encode_issuing_dist_point(backend, ext):
    idp = backend._lib.ISSUING_DIST_POINT_new()
    backend.openssl_assert(idp != backend._ffi.NULL)
    idp = backend._ffi.gc(idp, backend._lib.ISSUING_DIST_POINT_free)
    idp.onlyuser = 255 if ext.only_contains_user_certs else 0
    idp.onlyCA = 255 if ext.only_contains_ca_certs else 0
    idp.indirectCRL = 255 if ext.indirect_crl else 0
    idp.onlyattr = 255 if ext.only_contains_attribute_certs else 0
    if ext.only_some_reasons:
        idp.onlysomereasons = _encode_reasonflags(backend, ext.only_some_reasons)
    if ext.full_name:
        idp.distpoint = _encode_full_name(backend, ext.full_name)
    if ext.relative_name:
        idp.distpoint = _encode_relative_name(backend, ext.relative_name)
    return idp


def _encode_crl_reason(backend, crl_reason):
    asn1enum = backend._lib.ASN1_ENUMERATED_new()
    backend.openssl_assert(asn1enum != backend._ffi.NULL)
    asn1enum = backend._ffi.gc(asn1enum, backend._lib.ASN1_ENUMERATED_free)
    res = backend._lib.ASN1_ENUMERATED_set(asn1enum, _CRL_ENTRY_REASON_ENUM_TO_CODE[crl_reason.reason])
    backend.openssl_assert(res == 1)
    return asn1enum


def _encode_invalidity_date(backend, invalidity_date):
    time = backend._lib.ASN1_GENERALIZEDTIME_set(backend._ffi.NULL, calendar.timegm(invalidity_date.invalidity_date.timetuple()))
    backend.openssl_assert(time != backend._ffi.NULL)
    time = backend._ffi.gc(time, backend._lib.ASN1_GENERALIZEDTIME_free)
    return time


def _encode_certificate_policies--- This code section failed: ---

 L. 191         0  LOAD_FAST                'backend'
                2  LOAD_ATTR                _lib
                4  LOAD_METHOD              sk_POLICYINFO_new_null
                6  CALL_METHOD_0         0  ''
                8  STORE_FAST               'cp'

 L. 192        10  LOAD_FAST                'backend'
               12  LOAD_METHOD              openssl_assert
               14  LOAD_FAST                'cp'
               16  LOAD_FAST                'backend'
               18  LOAD_ATTR                _ffi
               20  LOAD_ATTR                NULL
               22  COMPARE_OP               !=
               24  CALL_METHOD_1         1  ''
               26  POP_TOP          

 L. 193        28  LOAD_FAST                'backend'
               30  LOAD_ATTR                _ffi
               32  LOAD_METHOD              gc
               34  LOAD_FAST                'cp'
               36  LOAD_FAST                'backend'
               38  LOAD_ATTR                _lib
               40  LOAD_ATTR                sk_POLICYINFO_free
               42  CALL_METHOD_2         2  ''
               44  STORE_FAST               'cp'

 L. 194        46  LOAD_FAST                'certificate_policies'
               48  GET_ITER         
             50_0  COME_FROM           398  '398'
             50_1  COME_FROM           136  '136'
            50_52  FOR_ITER            400  'to 400'
               54  STORE_FAST               'policy_info'

 L. 195        56  LOAD_FAST                'backend'
               58  LOAD_ATTR                _lib
               60  LOAD_METHOD              POLICYINFO_new
               62  CALL_METHOD_0         0  ''
               64  STORE_FAST               'pi'

 L. 196        66  LOAD_FAST                'backend'
               68  LOAD_METHOD              openssl_assert
               70  LOAD_FAST                'pi'
               72  LOAD_FAST                'backend'
               74  LOAD_ATTR                _ffi
               76  LOAD_ATTR                NULL
               78  COMPARE_OP               !=
               80  CALL_METHOD_1         1  ''
               82  POP_TOP          

 L. 197        84  LOAD_FAST                'backend'
               86  LOAD_ATTR                _lib
               88  LOAD_METHOD              sk_POLICYINFO_push
               90  LOAD_FAST                'cp'
               92  LOAD_FAST                'pi'
               94  CALL_METHOD_2         2  ''
               96  STORE_FAST               'res'

 L. 198        98  LOAD_FAST                'backend'
              100  LOAD_METHOD              openssl_assert
              102  LOAD_FAST                'res'
              104  LOAD_CONST               1
              106  COMPARE_OP               >=
              108  CALL_METHOD_1         1  ''
              110  POP_TOP          

 L. 199       112  LOAD_GLOBAL              _txt2obj
              114  LOAD_FAST                'backend'
              116  LOAD_FAST                'policy_info'
              118  LOAD_ATTR                policy_identifier
              120  LOAD_ATTR                dotted_string
              122  CALL_FUNCTION_2       2  ''
              124  STORE_FAST               'oid'

 L. 200       126  LOAD_FAST                'oid'
              128  LOAD_FAST                'pi'
              130  STORE_ATTR               policyid

 L. 201       132  LOAD_FAST                'policy_info'
              134  LOAD_ATTR                policy_qualifiers
              136  POP_JUMP_IF_FALSE_BACK    50  'to 50'

 L. 202       138  LOAD_FAST                'backend'
              140  LOAD_ATTR                _lib
              142  LOAD_METHOD              sk_POLICYQUALINFO_new_null
              144  CALL_METHOD_0         0  ''
              146  STORE_FAST               'pqis'

 L. 203       148  LOAD_FAST                'backend'
              150  LOAD_METHOD              openssl_assert
              152  LOAD_FAST                'pqis'
              154  LOAD_FAST                'backend'
              156  LOAD_ATTR                _ffi
              158  LOAD_ATTR                NULL
              160  COMPARE_OP               !=
              162  CALL_METHOD_1         1  ''
              164  POP_TOP          

 L. 204       166  LOAD_FAST                'policy_info'
              168  LOAD_ATTR                policy_qualifiers
              170  GET_ITER         
            172_0  COME_FROM           390  '390'
            172_1  COME_FROM           282  '282'
              172  FOR_ITER            392  'to 392'
              174  STORE_FAST               'qualifier'

 L. 205       176  LOAD_FAST                'backend'
              178  LOAD_ATTR                _lib
              180  LOAD_METHOD              POLICYQUALINFO_new
              182  CALL_METHOD_0         0  ''
              184  STORE_FAST               'pqi'

 L. 206       186  LOAD_FAST                'backend'
              188  LOAD_METHOD              openssl_assert
              190  LOAD_FAST                'pqi'
              192  LOAD_FAST                'backend'
              194  LOAD_ATTR                _ffi
              196  LOAD_ATTR                NULL
              198  COMPARE_OP               !=
              200  CALL_METHOD_1         1  ''
              202  POP_TOP          

 L. 207       204  LOAD_FAST                'backend'
              206  LOAD_ATTR                _lib
              208  LOAD_METHOD              sk_POLICYQUALINFO_push
              210  LOAD_FAST                'pqis'
              212  LOAD_FAST                'pqi'
              214  CALL_METHOD_2         2  ''
              216  STORE_FAST               'res'

 L. 208       218  LOAD_FAST                'backend'
              220  LOAD_METHOD              openssl_assert
              222  LOAD_FAST                'res'
              224  LOAD_CONST               1
              226  COMPARE_OP               >=
              228  CALL_METHOD_1         1  ''
              230  POP_TOP          

 L. 209       232  LOAD_GLOBAL              isinstance
              234  LOAD_FAST                'qualifier'
              236  LOAD_GLOBAL              six
              238  LOAD_ATTR                text_type
              240  CALL_FUNCTION_2       2  ''
          242_244  POP_JUMP_IF_FALSE   284  'to 284'

 L. 210       246  LOAD_GLOBAL              _txt2obj

 L. 211       248  LOAD_FAST                'backend'
              250  LOAD_GLOBAL              x509
              252  LOAD_ATTR                OID_CPS_QUALIFIER
              254  LOAD_ATTR                dotted_string

 L. 210       256  CALL_FUNCTION_2       2  ''
              258  LOAD_FAST                'pqi'
              260  STORE_ATTR               pqualid

 L. 213       262  LOAD_GLOBAL              _encode_asn1_str

 L. 214       264  LOAD_FAST                'backend'

 L. 215       266  LOAD_FAST                'qualifier'
              268  LOAD_METHOD              encode
              270  LOAD_STR                 'ascii'
              272  CALL_METHOD_1         1  ''

 L. 213       274  CALL_FUNCTION_2       2  ''
              276  LOAD_FAST                'pqi'
              278  LOAD_ATTR                d
              280  STORE_ATTR               cpsuri
              282  JUMP_BACK           172  'to 172'
            284_0  COME_FROM           242  '242'

 L. 218       284  LOAD_GLOBAL              isinstance
              286  LOAD_FAST                'qualifier'
              288  LOAD_GLOBAL              x509
              290  LOAD_ATTR                UserNotice
              292  CALL_FUNCTION_2       2  ''
          294_296  POP_JUMP_IF_TRUE    302  'to 302'
              298  <74>             
              300  RAISE_VARARGS_1       1  'exception instance'
            302_0  COME_FROM           294  '294'

 L. 219       302  LOAD_GLOBAL              _txt2obj

 L. 220       304  LOAD_FAST                'backend'
              306  LOAD_GLOBAL              x509
              308  LOAD_ATTR                OID_CPS_USER_NOTICE
              310  LOAD_ATTR                dotted_string

 L. 219       312  CALL_FUNCTION_2       2  ''
              314  LOAD_FAST                'pqi'
              316  STORE_ATTR               pqualid

 L. 222       318  LOAD_FAST                'backend'
              320  LOAD_ATTR                _lib
              322  LOAD_METHOD              USERNOTICE_new
              324  CALL_METHOD_0         0  ''
              326  STORE_FAST               'un'

 L. 223       328  LOAD_FAST                'backend'
              330  LOAD_METHOD              openssl_assert
              332  LOAD_FAST                'un'
              334  LOAD_FAST                'backend'
              336  LOAD_ATTR                _ffi
              338  LOAD_ATTR                NULL
              340  COMPARE_OP               !=
              342  CALL_METHOD_1         1  ''
              344  POP_TOP          

 L. 224       346  LOAD_FAST                'un'
              348  LOAD_FAST                'pqi'
              350  LOAD_ATTR                d
              352  STORE_ATTR               usernotice

 L. 225       354  LOAD_FAST                'qualifier'
              356  LOAD_ATTR                explicit_text
          358_360  POP_JUMP_IF_FALSE   376  'to 376'

 L. 226       362  LOAD_GLOBAL              _encode_asn1_utf8_str

 L. 227       364  LOAD_FAST                'backend'
              366  LOAD_FAST                'qualifier'
              368  LOAD_ATTR                explicit_text

 L. 226       370  CALL_FUNCTION_2       2  ''
              372  LOAD_FAST                'un'
              374  STORE_ATTR               exptext
            376_0  COME_FROM           358  '358'

 L. 230       376  LOAD_GLOBAL              _encode_notice_reference

 L. 231       378  LOAD_FAST                'backend'
              380  LOAD_FAST                'qualifier'
              382  LOAD_ATTR                notice_reference

 L. 230       384  CALL_FUNCTION_2       2  ''
              386  LOAD_FAST                'un'
              388  STORE_ATTR               noticeref
              390  JUMP_BACK           172  'to 172'
            392_0  COME_FROM           172  '172'

 L. 234       392  LOAD_FAST                'pqis'
              394  LOAD_FAST                'pi'
              396  STORE_ATTR               qualifiers
              398  JUMP_BACK            50  'to 50'
            400_0  COME_FROM            50  '50'

 L. 236       400  LOAD_FAST                'cp'
              402  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 298


def _encode_notice_reference--- This code section failed: ---

 L. 240         0  LOAD_FAST                'notice'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 241         8  LOAD_FAST                'backend'
               10  LOAD_ATTR                _ffi
               12  LOAD_ATTR                NULL
               14  RETURN_VALUE     
             16_0  COME_FROM             6  '6'

 L. 243        16  LOAD_FAST                'backend'
               18  LOAD_ATTR                _lib
               20  LOAD_METHOD              NOTICEREF_new
               22  CALL_METHOD_0         0  ''
               24  STORE_FAST               'nr'

 L. 244        26  LOAD_FAST                'backend'
               28  LOAD_METHOD              openssl_assert
               30  LOAD_FAST                'nr'
               32  LOAD_FAST                'backend'
               34  LOAD_ATTR                _ffi
               36  LOAD_ATTR                NULL
               38  COMPARE_OP               !=
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          

 L. 246        44  LOAD_GLOBAL              _encode_asn1_utf8_str
               46  LOAD_FAST                'backend'
               48  LOAD_FAST                'notice'
               50  LOAD_ATTR                organization
               52  CALL_FUNCTION_2       2  ''
               54  LOAD_FAST                'nr'
               56  STORE_ATTR               organization

 L. 248        58  LOAD_FAST                'backend'
               60  LOAD_ATTR                _lib
               62  LOAD_METHOD              sk_ASN1_INTEGER_new_null
               64  CALL_METHOD_0         0  ''
               66  STORE_FAST               'notice_stack'

 L. 249        68  LOAD_FAST                'notice_stack'
               70  LOAD_FAST                'nr'
               72  STORE_ATTR               noticenos

 L. 250        74  LOAD_FAST                'notice'
               76  LOAD_ATTR                notice_numbers
               78  GET_ITER         
             80_0  COME_FROM           122  '122'
               80  FOR_ITER            124  'to 124'
               82  STORE_FAST               'number'

 L. 251        84  LOAD_GLOBAL              _encode_asn1_int
               86  LOAD_FAST                'backend'
               88  LOAD_FAST                'number'
               90  CALL_FUNCTION_2       2  ''
               92  STORE_FAST               'num'

 L. 252        94  LOAD_FAST                'backend'
               96  LOAD_ATTR                _lib
               98  LOAD_METHOD              sk_ASN1_INTEGER_push
              100  LOAD_FAST                'notice_stack'
              102  LOAD_FAST                'num'
              104  CALL_METHOD_2         2  ''
              106  STORE_FAST               'res'

 L. 253       108  LOAD_FAST                'backend'
              110  LOAD_METHOD              openssl_assert
              112  LOAD_FAST                'res'
              114  LOAD_CONST               1
              116  COMPARE_OP               >=
              118  CALL_METHOD_1         1  ''
              120  POP_TOP          
              122  JUMP_BACK            80  'to 80'
            124_0  COME_FROM            80  '80'

 L. 255       124  LOAD_FAST                'nr'
              126  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1


def _txt2obj(backend, name):
    """
    Converts a Python string with an ASN.1 object ID in dotted form to a
    ASN1_OBJECT.
    """
    name = name.encode('ascii')
    obj = backend._lib.OBJ_txt2obj(name, 1)
    backend.openssl_assert(obj != backend._ffi.NULL)
    return obj


def _txt2obj_gc(backend, name):
    obj = _txt2obj(backend, name)
    obj = backend._ffi.gc(obj, backend._lib.ASN1_OBJECT_free)
    return obj


def _encode_ocsp_nocheck(backend, ext):
    return backend._lib.ASN1_NULL_new()


def _encode_key_usage(backend, key_usage):
    set_bit = backend._lib.ASN1_BIT_STRING_set_bit
    ku = backend._lib.ASN1_BIT_STRING_new()
    ku = backend._ffi.gc(ku, backend._lib.ASN1_BIT_STRING_free)
    res = set_bit(ku, 0, key_usage.digital_signature)
    backend.openssl_assert(res == 1)
    res = set_bit(ku, 1, key_usage.content_commitment)
    backend.openssl_assert(res == 1)
    res = set_bit(ku, 2, key_usage.key_encipherment)
    backend.openssl_assert(res == 1)
    res = set_bit(ku, 3, key_usage.data_encipherment)
    backend.openssl_assert(res == 1)
    res = set_bit(ku, 4, key_usage.key_agreement)
    backend.openssl_assert(res == 1)
    res = set_bit(ku, 5, key_usage.key_cert_sign)
    backend.openssl_assert(res == 1)
    res = set_bit(ku, 6, key_usage.crl_sign)
    backend.openssl_assert(res == 1)
    if key_usage.key_agreement:
        res = set_bit(ku, 7, key_usage.encipher_only)
        backend.openssl_assert(res == 1)
        res = set_bit(ku, 8, key_usage.decipher_only)
        backend.openssl_assert(res == 1)
    else:
        res = set_bit(ku, 7, 0)
        backend.openssl_assert(res == 1)
        res = set_bit(ku, 8, 0)
        backend.openssl_assert(res == 1)
    return ku


def _encode_authority_key_identifier--- This code section failed: ---

 L. 313         0  LOAD_FAST                'backend'
                2  LOAD_ATTR                _lib
                4  LOAD_METHOD              AUTHORITY_KEYID_new
                6  CALL_METHOD_0         0  ''
                8  STORE_FAST               'akid'

 L. 314        10  LOAD_FAST                'backend'
               12  LOAD_METHOD              openssl_assert
               14  LOAD_FAST                'akid'
               16  LOAD_FAST                'backend'
               18  LOAD_ATTR                _ffi
               20  LOAD_ATTR                NULL
               22  COMPARE_OP               !=
               24  CALL_METHOD_1         1  ''
               26  POP_TOP          

 L. 315        28  LOAD_FAST                'backend'
               30  LOAD_ATTR                _ffi
               32  LOAD_METHOD              gc
               34  LOAD_FAST                'akid'
               36  LOAD_FAST                'backend'
               38  LOAD_ATTR                _lib
               40  LOAD_ATTR                AUTHORITY_KEYID_free
               42  CALL_METHOD_2         2  ''
               44  STORE_FAST               'akid'

 L. 316        46  LOAD_FAST                'authority_keyid'
               48  LOAD_ATTR                key_identifier
               50  LOAD_CONST               None
               52  <117>                 1  ''
               54  POP_JUMP_IF_FALSE    70  'to 70'

 L. 317        56  LOAD_GLOBAL              _encode_asn1_str

 L. 318        58  LOAD_FAST                'backend'

 L. 319        60  LOAD_FAST                'authority_keyid'
               62  LOAD_ATTR                key_identifier

 L. 317        64  CALL_FUNCTION_2       2  ''
               66  LOAD_FAST                'akid'
               68  STORE_ATTR               keyid
             70_0  COME_FROM            54  '54'

 L. 322        70  LOAD_FAST                'authority_keyid'
               72  LOAD_ATTR                authority_cert_issuer
               74  LOAD_CONST               None
               76  <117>                 1  ''
               78  POP_JUMP_IF_FALSE    94  'to 94'

 L. 323        80  LOAD_GLOBAL              _encode_general_names

 L. 324        82  LOAD_FAST                'backend'
               84  LOAD_FAST                'authority_keyid'
               86  LOAD_ATTR                authority_cert_issuer

 L. 323        88  CALL_FUNCTION_2       2  ''
               90  LOAD_FAST                'akid'
               92  STORE_ATTR               issuer
             94_0  COME_FROM            78  '78'

 L. 327        94  LOAD_FAST                'authority_keyid'
               96  LOAD_ATTR                authority_cert_serial_number
               98  LOAD_CONST               None
              100  <117>                 1  ''
              102  POP_JUMP_IF_FALSE   118  'to 118'

 L. 328       104  LOAD_GLOBAL              _encode_asn1_int

 L. 329       106  LOAD_FAST                'backend'
              108  LOAD_FAST                'authority_keyid'
              110  LOAD_ATTR                authority_cert_serial_number

 L. 328       112  CALL_FUNCTION_2       2  ''
              114  LOAD_FAST                'akid'
              116  STORE_ATTR               serial
            118_0  COME_FROM           102  '102'

 L. 332       118  LOAD_FAST                'akid'
              120  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 52


def _encode_basic_constraints--- This code section failed: ---

 L. 336         0  LOAD_FAST                'backend'
                2  LOAD_ATTR                _lib
                4  LOAD_METHOD              BASIC_CONSTRAINTS_new
                6  CALL_METHOD_0         0  ''
                8  STORE_FAST               'constraints'

 L. 337        10  LOAD_FAST                'backend'
               12  LOAD_ATTR                _ffi
               14  LOAD_METHOD              gc

 L. 338        16  LOAD_FAST                'constraints'
               18  LOAD_FAST                'backend'
               20  LOAD_ATTR                _lib
               22  LOAD_ATTR                BASIC_CONSTRAINTS_free

 L. 337        24  CALL_METHOD_2         2  ''
               26  STORE_FAST               'constraints'

 L. 340        28  LOAD_FAST                'basic_constraints'
               30  LOAD_ATTR                ca
               32  POP_JUMP_IF_FALSE    38  'to 38'
               34  LOAD_CONST               255
               36  JUMP_FORWARD         40  'to 40'
             38_0  COME_FROM            32  '32'
               38  LOAD_CONST               0
             40_0  COME_FROM            36  '36'
               40  LOAD_FAST                'constraints'
               42  STORE_ATTR               ca

 L. 341        44  LOAD_FAST                'basic_constraints'
               46  LOAD_ATTR                ca
               48  POP_JUMP_IF_FALSE    74  'to 74'
               50  LOAD_FAST                'basic_constraints'
               52  LOAD_ATTR                path_length
               54  LOAD_CONST               None
               56  <117>                 1  ''
               58  POP_JUMP_IF_FALSE    74  'to 74'

 L. 342        60  LOAD_GLOBAL              _encode_asn1_int

 L. 343        62  LOAD_FAST                'backend'
               64  LOAD_FAST                'basic_constraints'
               66  LOAD_ATTR                path_length

 L. 342        68  CALL_FUNCTION_2       2  ''
               70  LOAD_FAST                'constraints'
               72  STORE_ATTR               pathlen
             74_0  COME_FROM            58  '58'
             74_1  COME_FROM            48  '48'

 L. 346        74  LOAD_FAST                'constraints'
               76  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 56


def _encode_information_access(backend, info_access):
    aia = backend._lib.sk_ACCESS_DESCRIPTION_new_null()
    backend.openssl_assert(aia != backend._ffi.NULL)
    aia = backend._ffi.gc(aia, lambda x: backend._lib.sk_ACCESS_DESCRIPTION_pop_free(x, backend._ffi.addressof(backend._lib._original_lib, 'ACCESS_DESCRIPTION_free')))
    for access_description in info_access:
        ad = backend._lib.ACCESS_DESCRIPTION_new()
        method = _txt2obj(backend, access_description.access_method.dotted_string)
        _encode_general_name_preallocated(backend, access_description.access_location, ad.location)
        ad.method = method
        res = backend._lib.sk_ACCESS_DESCRIPTION_push(aia, ad)
        backend.openssl_assert(res >= 1)
    else:
        return aia


def _encode_general_names(backend, names):
    general_names = backend._lib.GENERAL_NAMES_new()
    backend.openssl_assert(general_names != backend._ffi.NULL)
    for name in names:
        gn = _encode_general_name(backend, name)
        res = backend._lib.sk_GENERAL_NAME_push(general_names, gn)
        backend.openssl_assert(res != 0)
    else:
        return general_names


def _encode_alt_name(backend, san):
    general_names = _encode_general_names(backend, san)
    general_names = backend._ffi.gc(general_names, backend._lib.GENERAL_NAMES_free)
    return general_names


def _encode_subject_key_identifier(backend, ski):
    return _encode_asn1_str_gc(backend, ski.digest)


def _encode_general_name(backend, name):
    gn = backend._lib.GENERAL_NAME_new()
    _encode_general_name_preallocated(backend, name, gn)
    return gn


def _encode_general_name_preallocated(backend, name, gn):
    if isinstance(name, x509.DNSName):
        backend.openssl_assert(gn != backend._ffi.NULL)
        gn.type = backend._lib.GEN_DNS
        ia5 = backend._lib.ASN1_IA5STRING_new()
        backend.openssl_assert(ia5 != backend._ffi.NULL)
        value = name.value.encode('utf8')
        res = backend._lib.ASN1_STRING_set(ia5, value, len(value))
        backend.openssl_assert(res == 1)
        gn.d.dNSName = ia5
    elif isinstance(name, x509.RegisteredID):
        backend.openssl_assert(gn != backend._ffi.NULL)
        gn.type = backend._lib.GEN_RID
        obj = backend._lib.OBJ_txt2obj(name.value.dotted_string.encode('ascii'), 1)
        backend.openssl_assert(obj != backend._ffi.NULL)
        gn.d.registeredID = obj
    elif isinstance(name, x509.DirectoryName):
        backend.openssl_assert(gn != backend._ffi.NULL)
        dir_name = _encode_name(backend, name.value)
        gn.type = backend._lib.GEN_DIRNAME
        gn.d.directoryName = dir_name
    elif isinstance(name, x509.IPAddress):
        backend.openssl_assert(gn != backend._ffi.NULL)
        if isinstance(name.value, ipaddress.IPv4Network):
            packed = name.value.network_address.packed + utils.int_to_bytes(4294967296 - name.value.num_addresses, 4)
        elif isinstance(name.value, ipaddress.IPv6Network):
            packed = name.value.network_address.packed + utils.int_to_bytes((1 << 128) - name.value.num_addresses, 16)
        else:
            packed = name.value.packed
        ipaddr = _encode_asn1_str(backend, packed)
        gn.type = backend._lib.GEN_IPADD
        gn.d.iPAddress = ipaddr
    elif isinstance(name, x509.OtherName):
        backend.openssl_assert(gn != backend._ffi.NULL)
        other_name = backend._lib.OTHERNAME_new()
        backend.openssl_assert(other_name != backend._ffi.NULL)
        type_id = backend._lib.OBJ_txt2obj(name.type_id.dotted_string.encode('ascii'), 1)
        backend.openssl_assert(type_id != backend._ffi.NULL)
        data = backend._ffi.new('unsigned char[]', name.value)
        data_ptr_ptr = backend._ffi.new('unsigned char **')
        data_ptr_ptr[0] = data
        value = backend._lib.d2i_ASN1_TYPE(backend._ffi.NULL, data_ptr_ptr, len(name.value))
        if value == backend._ffi.NULL:
            backend._consume_errors()
            raise ValueError('Invalid ASN.1 data')
        other_name.type_id = type_id
        other_name.value = value
        gn.type = backend._lib.GEN_OTHERNAME
        gn.d.otherName = other_name
    elif isinstance(name, x509.RFC822Name):
        backend.openssl_assert(gn != backend._ffi.NULL)
        data = name.value.encode('utf8')
        asn1_str = _encode_asn1_str(backend, data)
        gn.type = backend._lib.GEN_EMAIL
        gn.d.rfc822Name = asn1_str
    elif isinstance(name, x509.UniformResourceIdentifier):
        backend.openssl_assert(gn != backend._ffi.NULL)
        data = name.value.encode('utf8')
        asn1_str = _encode_asn1_str(backend, data)
        gn.type = backend._lib.GEN_URI
        gn.d.uniformResourceIdentifier = asn1_str
    else:
        raise ValueError('{} is an unknown GeneralName type'.format(name))


def _encode_extended_key_usage(backend, extended_key_usage):
    eku = backend._lib.sk_ASN1_OBJECT_new_null()
    eku = backend._ffi.gc(eku, backend._lib.sk_ASN1_OBJECT_free)
    for oid in extended_key_usage:
        obj = _txt2obj(backend, oid.dotted_string)
        res = backend._lib.sk_ASN1_OBJECT_push(eku, obj)
        backend.openssl_assert(res >= 1)
    else:
        return eku


_CRLREASONFLAGS = {x509.ReasonFlags.key_compromise: 1, 
 x509.ReasonFlags.ca_compromise: 2, 
 x509.ReasonFlags.affiliation_changed: 3, 
 x509.ReasonFlags.superseded: 4, 
 x509.ReasonFlags.cessation_of_operation: 5, 
 x509.ReasonFlags.certificate_hold: 6, 
 x509.ReasonFlags.privilege_withdrawn: 7, 
 x509.ReasonFlags.aa_compromise: 8}

def _encode_reasonflags(backend, reasons):
    bitmask = backend._lib.ASN1_BIT_STRING_new()
    backend.openssl_assert(bitmask != backend._ffi.NULL)
    for reason in reasons:
        res = backend._lib.ASN1_BIT_STRING_set_bit(bitmask, _CRLREASONFLAGS[reason], 1)
        backend.openssl_assert(res == 1)
    else:
        return bitmask


def _encode_full_name(backend, full_name):
    dpn = backend._lib.DIST_POINT_NAME_new()
    backend.openssl_assert(dpn != backend._ffi.NULL)
    dpn.type = _DISTPOINT_TYPE_FULLNAME
    dpn.name.fullname = _encode_general_names(backend, full_name)
    return dpn


def _encode_relative_name(backend, relative_name):
    dpn = backend._lib.DIST_POINT_NAME_new()
    backend.openssl_assert(dpn != backend._ffi.NULL)
    dpn.type = _DISTPOINT_TYPE_RELATIVENAME
    dpn.name.relativename = _encode_sk_name_entry(backend, relative_name)
    return dpn


def _encode_cdps_freshest_crl(backend, cdps):
    cdp = backend._lib.sk_DIST_POINT_new_null()
    cdp = backend._ffi.gc(cdp, backend._lib.sk_DIST_POINT_free)
    for point in cdps:
        dp = backend._lib.DIST_POINT_new()
        backend.openssl_assert(dp != backend._ffi.NULL)
        if point.reasons:
            dp.reasons = _encode_reasonflags(backend, point.reasons)
        else:
            if point.full_name:
                dp.distpoint = _encode_full_name(backend, point.full_name)
            if point.relative_name:
                dp.distpoint = _encode_relative_name(backend, point.relative_name)
            if point.crl_issuer:
                dp.CRLissuer = _encode_general_names(backend, point.crl_issuer)
            res = backend._lib.sk_DIST_POINT_push(cdp, dp)
            backend.openssl_assert(res >= 1)
    else:
        return cdp


def _encode_name_constraints(backend, name_constraints):
    nc = backend._lib.NAME_CONSTRAINTS_new()
    backend.openssl_assert(nc != backend._ffi.NULL)
    nc = backend._ffi.gc(nc, backend._lib.NAME_CONSTRAINTS_free)
    permitted = _encode_general_subtree(backend, name_constraints.permitted_subtrees)
    nc.permittedSubtrees = permitted
    excluded = _encode_general_subtree(backend, name_constraints.excluded_subtrees)
    nc.excludedSubtrees = excluded
    return nc


def _encode_policy_constraints--- This code section failed: ---

 L. 582         0  LOAD_FAST                'backend'
                2  LOAD_ATTR                _lib
                4  LOAD_METHOD              POLICY_CONSTRAINTS_new
                6  CALL_METHOD_0         0  ''
                8  STORE_FAST               'pc'

 L. 583        10  LOAD_FAST                'backend'
               12  LOAD_METHOD              openssl_assert
               14  LOAD_FAST                'pc'
               16  LOAD_FAST                'backend'
               18  LOAD_ATTR                _ffi
               20  LOAD_ATTR                NULL
               22  COMPARE_OP               !=
               24  CALL_METHOD_1         1  ''
               26  POP_TOP          

 L. 584        28  LOAD_FAST                'backend'
               30  LOAD_ATTR                _ffi
               32  LOAD_METHOD              gc
               34  LOAD_FAST                'pc'
               36  LOAD_FAST                'backend'
               38  LOAD_ATTR                _lib
               40  LOAD_ATTR                POLICY_CONSTRAINTS_free
               42  CALL_METHOD_2         2  ''
               44  STORE_FAST               'pc'

 L. 585        46  LOAD_FAST                'policy_constraints'
               48  LOAD_ATTR                require_explicit_policy
               50  LOAD_CONST               None
               52  <117>                 1  ''
               54  POP_JUMP_IF_FALSE    70  'to 70'

 L. 586        56  LOAD_GLOBAL              _encode_asn1_int

 L. 587        58  LOAD_FAST                'backend'
               60  LOAD_FAST                'policy_constraints'
               62  LOAD_ATTR                require_explicit_policy

 L. 586        64  CALL_FUNCTION_2       2  ''
               66  LOAD_FAST                'pc'
               68  STORE_ATTR               requireExplicitPolicy
             70_0  COME_FROM            54  '54'

 L. 590        70  LOAD_FAST                'policy_constraints'
               72  LOAD_ATTR                inhibit_policy_mapping
               74  LOAD_CONST               None
               76  <117>                 1  ''
               78  POP_JUMP_IF_FALSE    94  'to 94'

 L. 591        80  LOAD_GLOBAL              _encode_asn1_int

 L. 592        82  LOAD_FAST                'backend'
               84  LOAD_FAST                'policy_constraints'
               86  LOAD_ATTR                inhibit_policy_mapping

 L. 591        88  CALL_FUNCTION_2       2  ''
               90  LOAD_FAST                'pc'
               92  STORE_ATTR               inhibitPolicyMapping
             94_0  COME_FROM            78  '78'

 L. 595        94  LOAD_FAST                'pc'
               96  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 52


def _encode_general_subtree--- This code section failed: ---

 L. 599         0  LOAD_FAST                'subtrees'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 600         8  LOAD_FAST                'backend'
               10  LOAD_ATTR                _ffi
               12  LOAD_ATTR                NULL
               14  RETURN_VALUE     
             16_0  COME_FROM             6  '6'

 L. 602        16  LOAD_FAST                'backend'
               18  LOAD_ATTR                _lib
               20  LOAD_METHOD              sk_GENERAL_SUBTREE_new_null
               22  CALL_METHOD_0         0  ''
               24  STORE_FAST               'general_subtrees'

 L. 603        26  LOAD_FAST                'subtrees'
               28  GET_ITER         
             30_0  COME_FROM            84  '84'
               30  FOR_ITER             86  'to 86'
               32  STORE_FAST               'name'

 L. 604        34  LOAD_FAST                'backend'
               36  LOAD_ATTR                _lib
               38  LOAD_METHOD              GENERAL_SUBTREE_new
               40  CALL_METHOD_0         0  ''
               42  STORE_FAST               'gs'

 L. 605        44  LOAD_GLOBAL              _encode_general_name
               46  LOAD_FAST                'backend'
               48  LOAD_FAST                'name'
               50  CALL_FUNCTION_2       2  ''
               52  LOAD_FAST                'gs'
               54  STORE_ATTR               base

 L. 606        56  LOAD_FAST                'backend'
               58  LOAD_ATTR                _lib
               60  LOAD_METHOD              sk_GENERAL_SUBTREE_push
               62  LOAD_FAST                'general_subtrees'
               64  LOAD_FAST                'gs'
               66  CALL_METHOD_2         2  ''
               68  STORE_FAST               'res'

 L. 607        70  LOAD_FAST                'backend'
               72  LOAD_METHOD              openssl_assert
               74  LOAD_FAST                'res'
               76  LOAD_CONST               1
               78  COMPARE_OP               >=
               80  CALL_METHOD_1         1  ''
               82  POP_TOP          
               84  JUMP_BACK            30  'to 30'
             86_0  COME_FROM            30  '30'

 L. 609        86  LOAD_FAST                'general_subtrees'
               88  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1


def _encode_precert_signed_certificate_timestamps(backend, scts):
    sct_stack = backend._lib.sk_SCT_new_null()
    backend.openssl_assert(sct_stack != backend._ffi.NULL)
    sct_stack = backend._ffi.gc(sct_stack, backend._lib.sk_SCT_free)
    for sct in scts:
        res = backend._lib.sk_SCT_push(sct_stack, sct._sct)
        backend.openssl_assert(res >= 1)
    else:
        return sct_stack


def _encode_nonce(backend, nonce):
    return _encode_asn1_str_gc(backend, nonce.nonce)


_EXTENSION_ENCODE_HANDLERS = {ExtensionOID.BASIC_CONSTRAINTS: _encode_basic_constraints, 
 ExtensionOID.SUBJECT_KEY_IDENTIFIER: _encode_subject_key_identifier, 
 ExtensionOID.KEY_USAGE: _encode_key_usage, 
 ExtensionOID.SUBJECT_ALTERNATIVE_NAME: _encode_alt_name, 
 ExtensionOID.ISSUER_ALTERNATIVE_NAME: _encode_alt_name, 
 ExtensionOID.EXTENDED_KEY_USAGE: _encode_extended_key_usage, 
 ExtensionOID.AUTHORITY_KEY_IDENTIFIER: _encode_authority_key_identifier, 
 ExtensionOID.CERTIFICATE_POLICIES: _encode_certificate_policies, 
 ExtensionOID.AUTHORITY_INFORMATION_ACCESS: _encode_information_access, 
 ExtensionOID.SUBJECT_INFORMATION_ACCESS: _encode_information_access, 
 ExtensionOID.CRL_DISTRIBUTION_POINTS: _encode_cdps_freshest_crl, 
 ExtensionOID.FRESHEST_CRL: _encode_cdps_freshest_crl, 
 ExtensionOID.INHIBIT_ANY_POLICY: _encode_inhibit_any_policy, 
 ExtensionOID.OCSP_NO_CHECK: _encode_ocsp_nocheck, 
 ExtensionOID.NAME_CONSTRAINTS: _encode_name_constraints, 
 ExtensionOID.POLICY_CONSTRAINTS: _encode_policy_constraints, 
 ExtensionOID.PRECERT_SIGNED_CERTIFICATE_TIMESTAMPS: _encode_precert_signed_certificate_timestamps}
_CRL_EXTENSION_ENCODE_HANDLERS = {ExtensionOID.ISSUER_ALTERNATIVE_NAME: _encode_alt_name, 
 ExtensionOID.AUTHORITY_KEY_IDENTIFIER: _encode_authority_key_identifier, 
 ExtensionOID.AUTHORITY_INFORMATION_ACCESS: _encode_information_access, 
 ExtensionOID.CRL_NUMBER: _encode_crl_number_delta_crl_indicator, 
 ExtensionOID.DELTA_CRL_INDICATOR: _encode_crl_number_delta_crl_indicator, 
 ExtensionOID.ISSUING_DISTRIBUTION_POINT: _encode_issuing_dist_point, 
 ExtensionOID.FRESHEST_CRL: _encode_cdps_freshest_crl}
_CRL_ENTRY_EXTENSION_ENCODE_HANDLERS = {CRLEntryExtensionOID.CERTIFICATE_ISSUER: _encode_alt_name, 
 CRLEntryExtensionOID.CRL_REASON: _encode_crl_reason, 
 CRLEntryExtensionOID.INVALIDITY_DATE: _encode_invalidity_date}
_OCSP_REQUEST_EXTENSION_ENCODE_HANDLERS = {OCSPExtensionOID.NONCE: _encode_nonce}
_OCSP_BASICRESP_EXTENSION_ENCODE_HANDLERS = {OCSPExtensionOID.NONCE: _encode_nonce}