# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\backends\openssl\rsa.py
import typing
from cryptography import utils
from cryptography.exceptions import InvalidSignature, UnsupportedAlgorithm, _Reasons
from cryptography.hazmat.backends.openssl.utils import _calculate_digest_and_algorithm, _check_not_prehashed, _warn_sign_verify_deprecated
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import AsymmetricSignatureContext, AsymmetricVerificationContext, utils as asym_utils
from cryptography.hazmat.primitives.asymmetric.padding import AsymmetricPadding, MGF1, OAEP, PKCS1v15, PSS, calculate_max_pss_salt_length
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPrivateNumbers, RSAPublicKey, RSAPublicNumbers

def _get_rsa_pss_salt_length--- This code section failed: ---

 L.  46         0  LOAD_FAST                'pss'
                2  LOAD_ATTR                _salt_length
                4  STORE_FAST               'salt'

 L.  48         6  LOAD_FAST                'salt'
                8  LOAD_GLOBAL              MGF1
               10  LOAD_ATTR                MAX_LENGTH
               12  <117>                 0  ''
               14  POP_JUMP_IF_TRUE     26  'to 26'
               16  LOAD_FAST                'salt'
               18  LOAD_GLOBAL              PSS
               20  LOAD_ATTR                MAX_LENGTH
               22  <117>                 0  ''
               24  POP_JUMP_IF_FALSE    36  'to 36'
             26_0  COME_FROM            14  '14'

 L.  49        26  LOAD_GLOBAL              calculate_max_pss_salt_length
               28  LOAD_FAST                'key'
               30  LOAD_FAST                'hash_algorithm'
               32  CALL_FUNCTION_2       2  ''
               34  RETURN_VALUE     
             36_0  COME_FROM            24  '24'

 L.  51        36  LOAD_FAST                'salt'
               38  RETURN_VALUE     

Parse error at or near `<117>' instruction at offset 12


def _enc_dec_rsa(backend, key: typing.Union[('_RSAPrivateKey', '_RSAPublicKey')], data: bytes, padding: AsymmetricPadding) -> bytes:
    if not isinstancepaddingAsymmetricPadding:
        raise TypeError('Padding must be an instance of AsymmetricPadding.')
    if isinstancepaddingPKCS1v15:
        padding_enum = backend._lib.RSA_PKCS1_PADDING
    elif isinstancepaddingOAEP:
        padding_enum = backend._lib.RSA_PKCS1_OAEP_PADDING
        if not isinstancepadding._mgfMGF1:
            raise UnsupportedAlgorithm'Only MGF1 is supported by this backend.'_Reasons.UNSUPPORTED_MGF
        raise (backend.rsa_padding_supported(padding) or UnsupportedAlgorithm)'This combination of padding and hash algorithm is not supported by this backend.'_Reasons.UNSUPPORTED_PADDING
    else:
        raise UnsupportedAlgorithm'{} is not supported by this backend.'.format(padding.name)_Reasons.UNSUPPORTED_PADDING
    return _enc_dec_rsa_pkey_ctx(backend, key, data, padding_enum, padding)


def _enc_dec_rsa_pkey_ctx--- This code section failed: ---

 L.  97         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'key'
                4  LOAD_GLOBAL              _RSAPublicKey
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    28  'to 28'

 L.  98        10  LOAD_FAST                'backend'
               12  LOAD_ATTR                _lib
               14  LOAD_ATTR                EVP_PKEY_encrypt_init
               16  STORE_FAST               'init'

 L.  99        18  LOAD_FAST                'backend'
               20  LOAD_ATTR                _lib
               22  LOAD_ATTR                EVP_PKEY_encrypt
               24  STORE_FAST               'crypt'
               26  JUMP_FORWARD         44  'to 44'
             28_0  COME_FROM             8  '8'

 L. 101        28  LOAD_FAST                'backend'
               30  LOAD_ATTR                _lib
               32  LOAD_ATTR                EVP_PKEY_decrypt_init
               34  STORE_FAST               'init'

 L. 102        36  LOAD_FAST                'backend'
               38  LOAD_ATTR                _lib
               40  LOAD_ATTR                EVP_PKEY_decrypt
               42  STORE_FAST               'crypt'
             44_0  COME_FROM            26  '26'

 L. 104        44  LOAD_FAST                'backend'
               46  LOAD_ATTR                _lib
               48  LOAD_METHOD              EVP_PKEY_CTX_new
               50  LOAD_FAST                'key'
               52  LOAD_ATTR                _evp_pkey
               54  LOAD_FAST                'backend'
               56  LOAD_ATTR                _ffi
               58  LOAD_ATTR                NULL
               60  CALL_METHOD_2         2  ''
               62  STORE_FAST               'pkey_ctx'

 L. 105        64  LOAD_FAST                'backend'
               66  LOAD_METHOD              openssl_assert
               68  LOAD_FAST                'pkey_ctx'
               70  LOAD_FAST                'backend'
               72  LOAD_ATTR                _ffi
               74  LOAD_ATTR                NULL
               76  COMPARE_OP               !=
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          

 L. 106        82  LOAD_FAST                'backend'
               84  LOAD_ATTR                _ffi
               86  LOAD_METHOD              gc
               88  LOAD_FAST                'pkey_ctx'
               90  LOAD_FAST                'backend'
               92  LOAD_ATTR                _lib
               94  LOAD_ATTR                EVP_PKEY_CTX_free
               96  CALL_METHOD_2         2  ''
               98  STORE_FAST               'pkey_ctx'

 L. 107       100  LOAD_FAST                'init'
              102  LOAD_FAST                'pkey_ctx'
              104  CALL_FUNCTION_1       1  ''
              106  STORE_FAST               'res'

 L. 108       108  LOAD_FAST                'backend'
              110  LOAD_METHOD              openssl_assert
              112  LOAD_FAST                'res'
              114  LOAD_CONST               1
              116  COMPARE_OP               ==
              118  CALL_METHOD_1         1  ''
              120  POP_TOP          

 L. 109       122  LOAD_FAST                'backend'
              124  LOAD_ATTR                _lib
              126  LOAD_METHOD              EVP_PKEY_CTX_set_rsa_padding
              128  LOAD_FAST                'pkey_ctx'
              130  LOAD_FAST                'padding_enum'
              132  CALL_METHOD_2         2  ''
              134  STORE_FAST               'res'

 L. 110       136  LOAD_FAST                'backend'
              138  LOAD_METHOD              openssl_assert
              140  LOAD_FAST                'res'
              142  LOAD_CONST               0
              144  COMPARE_OP               >
              146  CALL_METHOD_1         1  ''
              148  POP_TOP          

 L. 111       150  LOAD_FAST                'backend'
              152  LOAD_ATTR                _lib
              154  LOAD_METHOD              EVP_PKEY_size
              156  LOAD_FAST                'key'
              158  LOAD_ATTR                _evp_pkey
              160  CALL_METHOD_1         1  ''
              162  STORE_FAST               'buf_size'

 L. 112       164  LOAD_FAST                'backend'
              166  LOAD_METHOD              openssl_assert
              168  LOAD_FAST                'buf_size'
              170  LOAD_CONST               0
              172  COMPARE_OP               >
              174  CALL_METHOD_1         1  ''
              176  POP_TOP          

 L. 113       178  LOAD_GLOBAL              isinstance
              180  LOAD_FAST                'padding'
              182  LOAD_GLOBAL              OAEP
              184  CALL_FUNCTION_2       2  ''
          186_188  POP_JUMP_IF_FALSE   282  'to 282'
              190  LOAD_FAST                'backend'
              192  LOAD_ATTR                _lib
              194  LOAD_ATTR                Cryptography_HAS_RSA_OAEP_MD
          196_198  POP_JUMP_IF_FALSE   282  'to 282'

 L. 114       200  LOAD_FAST                'backend'
              202  LOAD_METHOD              _evp_md_non_null_from_algorithm

 L. 115       204  LOAD_FAST                'padding'
              206  LOAD_ATTR                _mgf
              208  LOAD_ATTR                _algorithm

 L. 114       210  CALL_METHOD_1         1  ''
              212  STORE_FAST               'mgf1_md'

 L. 117       214  LOAD_FAST                'backend'
              216  LOAD_ATTR                _lib
              218  LOAD_METHOD              EVP_PKEY_CTX_set_rsa_mgf1_md
              220  LOAD_FAST                'pkey_ctx'
              222  LOAD_FAST                'mgf1_md'
              224  CALL_METHOD_2         2  ''
              226  STORE_FAST               'res'

 L. 118       228  LOAD_FAST                'backend'
              230  LOAD_METHOD              openssl_assert
              232  LOAD_FAST                'res'
              234  LOAD_CONST               0
              236  COMPARE_OP               >
              238  CALL_METHOD_1         1  ''
              240  POP_TOP          

 L. 119       242  LOAD_FAST                'backend'
              244  LOAD_METHOD              _evp_md_non_null_from_algorithm
              246  LOAD_FAST                'padding'
              248  LOAD_ATTR                _algorithm
              250  CALL_METHOD_1         1  ''
              252  STORE_FAST               'oaep_md'

 L. 120       254  LOAD_FAST                'backend'
              256  LOAD_ATTR                _lib
              258  LOAD_METHOD              EVP_PKEY_CTX_set_rsa_oaep_md
              260  LOAD_FAST                'pkey_ctx'
              262  LOAD_FAST                'oaep_md'
              264  CALL_METHOD_2         2  ''
              266  STORE_FAST               'res'

 L. 121       268  LOAD_FAST                'backend'
              270  LOAD_METHOD              openssl_assert
              272  LOAD_FAST                'res'
              274  LOAD_CONST               0
              276  COMPARE_OP               >
              278  CALL_METHOD_1         1  ''
              280  POP_TOP          
            282_0  COME_FROM           196  '196'
            282_1  COME_FROM           186  '186'

 L. 124       282  LOAD_GLOBAL              isinstance
              284  LOAD_FAST                'padding'
              286  LOAD_GLOBAL              OAEP
              288  CALL_FUNCTION_2       2  ''

 L. 123   290_292  POP_JUMP_IF_FALSE   418  'to 418'

 L. 125       294  LOAD_FAST                'padding'
              296  LOAD_ATTR                _label
              298  LOAD_CONST               None
              300  <117>                 1  ''

 L. 123   302_304  POP_JUMP_IF_FALSE   418  'to 418'

 L. 126       306  LOAD_GLOBAL              len
              308  LOAD_FAST                'padding'
              310  LOAD_ATTR                _label
              312  CALL_FUNCTION_1       1  ''
              314  LOAD_CONST               0
              316  COMPARE_OP               >

 L. 123   318_320  POP_JUMP_IF_FALSE   418  'to 418'

 L. 130       322  LOAD_FAST                'backend'
              324  LOAD_ATTR                _lib
              326  LOAD_METHOD              OPENSSL_malloc
              328  LOAD_GLOBAL              len
              330  LOAD_FAST                'padding'
              332  LOAD_ATTR                _label
              334  CALL_FUNCTION_1       1  ''
              336  CALL_METHOD_1         1  ''
              338  STORE_FAST               'labelptr'

 L. 131       340  LOAD_FAST                'backend'
              342  LOAD_METHOD              openssl_assert
              344  LOAD_FAST                'labelptr'
              346  LOAD_FAST                'backend'
              348  LOAD_ATTR                _ffi
              350  LOAD_ATTR                NULL
              352  COMPARE_OP               !=
              354  CALL_METHOD_1         1  ''
              356  POP_TOP          

 L. 132       358  LOAD_FAST                'backend'
              360  LOAD_ATTR                _ffi
              362  LOAD_METHOD              memmove
              364  LOAD_FAST                'labelptr'
              366  LOAD_FAST                'padding'
              368  LOAD_ATTR                _label
              370  LOAD_GLOBAL              len
              372  LOAD_FAST                'padding'
              374  LOAD_ATTR                _label
              376  CALL_FUNCTION_1       1  ''
              378  CALL_METHOD_3         3  ''
              380  POP_TOP          

 L. 133       382  LOAD_FAST                'backend'
              384  LOAD_ATTR                _lib
              386  LOAD_METHOD              EVP_PKEY_CTX_set0_rsa_oaep_label

 L. 134       388  LOAD_FAST                'pkey_ctx'
              390  LOAD_FAST                'labelptr'
              392  LOAD_GLOBAL              len
              394  LOAD_FAST                'padding'
              396  LOAD_ATTR                _label
              398  CALL_FUNCTION_1       1  ''

 L. 133       400  CALL_METHOD_3         3  ''
              402  STORE_FAST               'res'

 L. 136       404  LOAD_FAST                'backend'
              406  LOAD_METHOD              openssl_assert
              408  LOAD_FAST                'res'
              410  LOAD_CONST               1
              412  COMPARE_OP               ==
              414  CALL_METHOD_1         1  ''
              416  POP_TOP          
            418_0  COME_FROM           318  '318'
            418_1  COME_FROM           302  '302'
            418_2  COME_FROM           290  '290'

 L. 138       418  LOAD_FAST                'backend'
              420  LOAD_ATTR                _ffi
              422  LOAD_METHOD              new
              424  LOAD_STR                 'size_t *'
              426  LOAD_FAST                'buf_size'
              428  CALL_METHOD_2         2  ''
              430  STORE_FAST               'outlen'

 L. 139       432  LOAD_FAST                'backend'
              434  LOAD_ATTR                _ffi
              436  LOAD_METHOD              new
              438  LOAD_STR                 'unsigned char[]'
              440  LOAD_FAST                'buf_size'
              442  CALL_METHOD_2         2  ''
              444  STORE_FAST               'buf'

 L. 147       446  LOAD_FAST                'crypt'
              448  LOAD_FAST                'pkey_ctx'
              450  LOAD_FAST                'buf'
              452  LOAD_FAST                'outlen'
              454  LOAD_FAST                'data'
              456  LOAD_GLOBAL              len
              458  LOAD_FAST                'data'
              460  CALL_FUNCTION_1       1  ''
              462  CALL_FUNCTION_5       5  ''
              464  STORE_FAST               'res'

 L. 148       466  LOAD_FAST                'backend'
              468  LOAD_ATTR                _ffi
              470  LOAD_METHOD              buffer
              472  LOAD_FAST                'buf'
              474  CALL_METHOD_1         1  ''
              476  LOAD_CONST               None
              478  LOAD_FAST                'outlen'
              480  LOAD_CONST               0
              482  BINARY_SUBSCR    
              484  BUILD_SLICE_2         2 
              486  BINARY_SUBSCR    
              488  STORE_FAST               'resbuf'

 L. 149       490  LOAD_FAST                'backend'
              492  LOAD_ATTR                _lib
              494  LOAD_METHOD              ERR_clear_error
              496  CALL_METHOD_0         0  ''
              498  POP_TOP          

 L. 150       500  LOAD_FAST                'res'
              502  LOAD_CONST               0
              504  COMPARE_OP               <=
          506_508  POP_JUMP_IF_FALSE   518  'to 518'

 L. 151       510  LOAD_GLOBAL              ValueError
              512  LOAD_STR                 'Encryption/decryption failed.'
              514  CALL_FUNCTION_1       1  ''
              516  RAISE_VARARGS_1       1  'exception instance'
            518_0  COME_FROM           506  '506'

 L. 152       518  LOAD_FAST                'resbuf'
              520  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 300


def _rsa_sig_determine_padding(backend, key, padding, algorithm):
    if not isinstancepaddingAsymmetricPadding:
        raise TypeError('Expected provider of AsymmetricPadding.')
    pkey_size = backend._lib.EVP_PKEY_size(key._evp_pkey)
    backend.openssl_assert(pkey_size > 0)
    if isinstancepaddingPKCS1v15:
        padding_enum = backend._lib.RSA_PKCS1_PADDING
    elif isinstancepaddingPSS:
        if not isinstancepadding._mgfMGF1:
            raise UnsupportedAlgorithm'Only MGF1 is supported by this backend.'_Reasons.UNSUPPORTED_MGF
        if not isinstancealgorithmhashes.HashAlgorithm:
            raise TypeError('Expected instance of hashes.HashAlgorithm.')
        if pkey_size - algorithm.digest_size - 2 < 0:
            raise ValueError('Digest too large for key size. Use a larger key or different digest.')
        padding_enum = backend._lib.RSA_PKCS1_PSS_PADDING
    else:
        raise UnsupportedAlgorithm'{} is not supported by this backend.'.format(padding.name)_Reasons.UNSUPPORTED_PADDING
    return padding_enum


def _rsa_sig_setup--- This code section failed: ---

 L. 199         0  LOAD_GLOBAL              _rsa_sig_determine_padding
                2  LOAD_FAST                'backend'
                4  LOAD_FAST                'key'
                6  LOAD_FAST                'padding'
                8  LOAD_FAST                'algorithm'
               10  CALL_FUNCTION_4       4  ''
               12  STORE_FAST               'padding_enum'

 L. 200        14  LOAD_FAST                'backend'
               16  LOAD_ATTR                _lib
               18  LOAD_METHOD              EVP_PKEY_CTX_new
               20  LOAD_FAST                'key'
               22  LOAD_ATTR                _evp_pkey
               24  LOAD_FAST                'backend'
               26  LOAD_ATTR                _ffi
               28  LOAD_ATTR                NULL
               30  CALL_METHOD_2         2  ''
               32  STORE_FAST               'pkey_ctx'

 L. 201        34  LOAD_FAST                'backend'
               36  LOAD_METHOD              openssl_assert
               38  LOAD_FAST                'pkey_ctx'
               40  LOAD_FAST                'backend'
               42  LOAD_ATTR                _ffi
               44  LOAD_ATTR                NULL
               46  COMPARE_OP               !=
               48  CALL_METHOD_1         1  ''
               50  POP_TOP          

 L. 202        52  LOAD_FAST                'backend'
               54  LOAD_ATTR                _ffi
               56  LOAD_METHOD              gc
               58  LOAD_FAST                'pkey_ctx'
               60  LOAD_FAST                'backend'
               62  LOAD_ATTR                _lib
               64  LOAD_ATTR                EVP_PKEY_CTX_free
               66  CALL_METHOD_2         2  ''
               68  STORE_FAST               'pkey_ctx'

 L. 203        70  LOAD_FAST                'init_func'
               72  LOAD_FAST                'pkey_ctx'
               74  CALL_FUNCTION_1       1  ''
               76  STORE_FAST               'res'

 L. 204        78  LOAD_FAST                'backend'
               80  LOAD_METHOD              openssl_assert
               82  LOAD_FAST                'res'
               84  LOAD_CONST               1
               86  COMPARE_OP               ==
               88  CALL_METHOD_1         1  ''
               90  POP_TOP          

 L. 205        92  LOAD_FAST                'algorithm'
               94  LOAD_CONST               None
               96  <117>                 1  ''
               98  POP_JUMP_IF_FALSE   160  'to 160'

 L. 206       100  LOAD_FAST                'backend'
              102  LOAD_METHOD              _evp_md_non_null_from_algorithm
              104  LOAD_FAST                'algorithm'
              106  CALL_METHOD_1         1  ''
              108  STORE_FAST               'evp_md'

 L. 207       110  LOAD_FAST                'backend'
              112  LOAD_ATTR                _lib
              114  LOAD_METHOD              EVP_PKEY_CTX_set_signature_md
              116  LOAD_FAST                'pkey_ctx'
              118  LOAD_FAST                'evp_md'
              120  CALL_METHOD_2         2  ''
              122  STORE_FAST               'res'

 L. 208       124  LOAD_FAST                'res'
              126  LOAD_CONST               0
              128  COMPARE_OP               ==
              130  POP_JUMP_IF_FALSE   160  'to 160'

 L. 209       132  LOAD_FAST                'backend'
              134  LOAD_METHOD              _consume_errors
              136  CALL_METHOD_0         0  ''
              138  POP_TOP          

 L. 210       140  LOAD_GLOBAL              UnsupportedAlgorithm

 L. 211       142  LOAD_STR                 '{} is not supported by this backend for RSA signing.'
              144  LOAD_METHOD              format

 L. 212       146  LOAD_FAST                'algorithm'
              148  LOAD_ATTR                name

 L. 211       150  CALL_METHOD_1         1  ''

 L. 214       152  LOAD_GLOBAL              _Reasons
              154  LOAD_ATTR                UNSUPPORTED_HASH

 L. 210       156  CALL_FUNCTION_2       2  ''
              158  RAISE_VARARGS_1       1  'exception instance'
            160_0  COME_FROM           130  '130'
            160_1  COME_FROM            98  '98'

 L. 216       160  LOAD_FAST                'backend'
              162  LOAD_ATTR                _lib
              164  LOAD_METHOD              EVP_PKEY_CTX_set_rsa_padding
              166  LOAD_FAST                'pkey_ctx'
              168  LOAD_FAST                'padding_enum'
              170  CALL_METHOD_2         2  ''
              172  STORE_FAST               'res'

 L. 217       174  LOAD_FAST                'res'
              176  LOAD_CONST               0
              178  COMPARE_OP               <=
              180  POP_JUMP_IF_FALSE   210  'to 210'

 L. 218       182  LOAD_FAST                'backend'
              184  LOAD_METHOD              _consume_errors
              186  CALL_METHOD_0         0  ''
              188  POP_TOP          

 L. 219       190  LOAD_GLOBAL              UnsupportedAlgorithm

 L. 220       192  LOAD_STR                 '{} is not supported for the RSA signature operation.'
              194  LOAD_METHOD              format

 L. 221       196  LOAD_FAST                'padding'
              198  LOAD_ATTR                name

 L. 220       200  CALL_METHOD_1         1  ''

 L. 223       202  LOAD_GLOBAL              _Reasons
              204  LOAD_ATTR                UNSUPPORTED_PADDING

 L. 219       206  CALL_FUNCTION_2       2  ''
              208  RAISE_VARARGS_1       1  'exception instance'
            210_0  COME_FROM           180  '180'

 L. 225       210  LOAD_GLOBAL              isinstance
              212  LOAD_FAST                'padding'
              214  LOAD_GLOBAL              PSS
              216  CALL_FUNCTION_2       2  ''
          218_220  POP_JUMP_IF_FALSE   300  'to 300'

 L. 226       222  LOAD_FAST                'backend'
              224  LOAD_ATTR                _lib
              226  LOAD_METHOD              EVP_PKEY_CTX_set_rsa_pss_saltlen

 L. 227       228  LOAD_FAST                'pkey_ctx'
              230  LOAD_GLOBAL              _get_rsa_pss_salt_length
              232  LOAD_FAST                'padding'
              234  LOAD_FAST                'key'
              236  LOAD_FAST                'algorithm'
              238  CALL_FUNCTION_3       3  ''

 L. 226       240  CALL_METHOD_2         2  ''
              242  STORE_FAST               'res'

 L. 229       244  LOAD_FAST                'backend'
              246  LOAD_METHOD              openssl_assert
              248  LOAD_FAST                'res'
              250  LOAD_CONST               0
              252  COMPARE_OP               >
              254  CALL_METHOD_1         1  ''
              256  POP_TOP          

 L. 231       258  LOAD_FAST                'backend'
              260  LOAD_METHOD              _evp_md_non_null_from_algorithm

 L. 232       262  LOAD_FAST                'padding'
              264  LOAD_ATTR                _mgf
              266  LOAD_ATTR                _algorithm

 L. 231       268  CALL_METHOD_1         1  ''
              270  STORE_FAST               'mgf1_md'

 L. 234       272  LOAD_FAST                'backend'
              274  LOAD_ATTR                _lib
              276  LOAD_METHOD              EVP_PKEY_CTX_set_rsa_mgf1_md
              278  LOAD_FAST                'pkey_ctx'
              280  LOAD_FAST                'mgf1_md'
              282  CALL_METHOD_2         2  ''
              284  STORE_FAST               'res'

 L. 235       286  LOAD_FAST                'backend'
              288  LOAD_METHOD              openssl_assert
              290  LOAD_FAST                'res'
              292  LOAD_CONST               0
              294  COMPARE_OP               >
              296  CALL_METHOD_1         1  ''
              298  POP_TOP          
            300_0  COME_FROM           218  '218'

 L. 237       300  LOAD_FAST                'pkey_ctx'
              302  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 96


def _rsa_sig_sign(backend, padding, algorithm, private_key, data):
    pkey_ctx = _rsa_sig_setup(backend, padding, algorithm, private_key, backend._lib.EVP_PKEY_sign_init)
    buflen = backend._ffi.new('size_t *')
    res = backend._lib.EVP_PKEY_sign(pkey_ctx, backend._ffi.NULL, buflen, data, len(data))
    backend.openssl_assert(res == 1)
    buf = backend._ffi.new'unsigned char[]'buflen[0]
    res = backend._lib.EVP_PKEY_sign(pkey_ctx, buf, buflen, data, len(data))
    if res != 1:
        errors = backend._consume_errors_with_text
        raise ValueError'Digest or salt length too long for key size. Use a larger key or shorter salt length if you are specifying a PSS salt'errors
    return backend._ffi.buffer(buf)[:]


def _rsa_sig_verify(backend, padding, algorithm, public_key, signature, data):
    pkey_ctx = _rsa_sig_setup(backend, padding, algorithm, public_key, backend._lib.EVP_PKEY_verify_init)
    res = backend._lib.EVP_PKEY_verify(pkey_ctx, signature, len(signature), data, len(data))
    backend.openssl_assert(res >= 0)
    if res == 0:
        backend._consume_errors
        raise InvalidSignature


def _rsa_sig_recover(backend, padding, algorithm, public_key, signature):
    pkey_ctx = _rsa_sig_setup(backend, padding, algorithm, public_key, backend._lib.EVP_PKEY_verify_recover_init)
    maxlen = backend._lib.EVP_PKEY_size(public_key._evp_pkey)
    backend.openssl_assert(maxlen > 0)
    buf = backend._ffi.new'unsigned char[]'maxlen
    buflen = backend._ffi.new'size_t *'maxlen
    res = backend._lib.EVP_PKEY_verify_recover(pkey_ctx, buf, buflen, signature, len(signature))
    resbuf = backend._ffi.buffer(buf)[:buflen[0]]
    backend._lib.ERR_clear_error
    if res != 1:
        raise InvalidSignature
    return resbuf


class _RSASignatureContext(AsymmetricSignatureContext):

    def __init__(self, backend, private_key: RSAPrivateKey, padding: AsymmetricPadding, algorithm: hashes.HashAlgorithm):
        self._backend = backend
        self._private_key = private_key
        _rsa_sig_determine_paddingbackendprivate_keypaddingalgorithm
        self._padding = padding
        self._algorithm = algorithm
        self._hash_ctx = hashes.Hashself._algorithmself._backend

    def update(self, data: bytes) -> None:
        self._hash_ctx.update(data)

    def finalize(self) -> bytes:
        return _rsa_sig_sign(self._backend, self._padding, self._algorithm, self._private_key, self._hash_ctx.finalize)


class _RSAVerificationContext(AsymmetricVerificationContext):

    def __init__(self, backend, public_key: RSAPublicKey, signature: bytes, padding: AsymmetricPadding, algorithm: hashes.HashAlgorithm):
        self._backend = backend
        self._public_key = public_key
        self._signature = signature
        self._padding = padding
        _rsa_sig_determine_paddingbackendpublic_keypaddingalgorithm
        padding = padding
        self._algorithm = algorithm
        self._hash_ctx = hashes.Hashself._algorithmself._backend

    def update(self, data: bytes) -> None:
        self._hash_ctx.update(data)

    def verify(self) -> None:
        return _rsa_sig_verify(self._backend, self._padding, self._algorithm, self._public_key, self._signature, self._hash_ctx.finalize)


class _RSAPrivateKey(RSAPrivateKey):

    def __init__(self, backend, rsa_cdata, evp_pkey):
        res = backend._lib.RSA_check_key(rsa_cdata)
        if res != 1:
            errors = backend._consume_errors_with_text
            raise ValueError'Invalid private key'errors
        res = backend._lib.RSA_blinding_onrsa_cdatabackend._ffi.NULL
        backend.openssl_assert(res == 1)
        self._backend = backend
        self._rsa_cdata = rsa_cdata
        self._evp_pkey = evp_pkey
        n = self._backend._ffi.new('BIGNUM **')
        self._backend._lib.RSA_get0_key(self._rsa_cdata, n, self._backend._ffi.NULL, self._backend._ffi.NULL)
        self._backend.openssl_assert(n[0] != self._backend._ffi.NULL)
        self._key_size = self._backend._lib.BN_num_bits(n[0])

    key_size = utils.read_only_property('_key_size')

    def signer(self, padding: AsymmetricPadding, algorithm: hashes.HashAlgorithm) -> AsymmetricSignatureContext:
        _warn_sign_verify_deprecated()
        _check_not_prehashed(algorithm)
        return _RSASignatureContextself._backendselfpaddingalgorithm

    def decrypt(self, ciphertext: bytes, padding: AsymmetricPadding) -> bytes:
        key_size_bytes = (self.key_size + 7) // 8
        if key_size_bytes != len(ciphertext):
            raise ValueError('Ciphertext length must be equal to key size.')
        return _enc_dec_rsaself._backendselfciphertextpadding

    def public_key(self) -> RSAPublicKey:
        ctx = self._backend._lib.RSAPublicKey_dup(self._rsa_cdata)
        self._backend.openssl_assert(ctx != self._backend._ffi.NULL)
        ctx = self._backend._ffi.gcctxself._backend._lib.RSA_free
        evp_pkey = self._backend._rsa_cdata_to_evp_pkey(ctx)
        return _RSAPublicKey(self._backend, ctx, evp_pkey)

    def private_numbers(self) -> RSAPrivateNumbers:
        n = self._backend._ffi.new('BIGNUM **')
        e = self._backend._ffi.new('BIGNUM **')
        d = self._backend._ffi.new('BIGNUM **')
        p = self._backend._ffi.new('BIGNUM **')
        q = self._backend._ffi.new('BIGNUM **')
        dmp1 = self._backend._ffi.new('BIGNUM **')
        dmq1 = self._backend._ffi.new('BIGNUM **')
        iqmp = self._backend._ffi.new('BIGNUM **')
        self._backend._lib.RSA_get0_key(self._rsa_cdata, n, e, d)
        self._backend.openssl_assert(n[0] != self._backend._ffi.NULL)
        self._backend.openssl_assert(e[0] != self._backend._ffi.NULL)
        self._backend.openssl_assert(d[0] != self._backend._ffi.NULL)
        self._backend._lib.RSA_get0_factorsself._rsa_cdatapq
        self._backend.openssl_assert(p[0] != self._backend._ffi.NULL)
        self._backend.openssl_assert(q[0] != self._backend._ffi.NULL)
        self._backend._lib.RSA_get0_crt_params(self._rsa_cdata, dmp1, dmq1, iqmp)
        self._backend.openssl_assert(dmp1[0] != self._backend._ffi.NULL)
        self._backend.openssl_assert(dmq1[0] != self._backend._ffi.NULL)
        self._backend.openssl_assert(iqmp[0] != self._backend._ffi.NULL)
        return RSAPrivateNumbers(p=(self._backend._bn_to_int(p[0])),
          q=(self._backend._bn_to_int(q[0])),
          d=(self._backend._bn_to_int(d[0])),
          dmp1=(self._backend._bn_to_int(dmp1[0])),
          dmq1=(self._backend._bn_to_int(dmq1[0])),
          iqmp=(self._backend._bn_to_int(iqmp[0])),
          public_numbers=RSAPublicNumbers(e=(self._backend._bn_to_int(e[0])),
          n=(self._backend._bn_to_int(n[0]))))

    def private_bytes(self, encoding: serialization.Encoding, format: serialization.PrivateFormat, encryption_algorithm: serialization.KeySerializationEncryption) -> bytes:
        return self._backend._private_key_bytes(encoding, format, encryption_algorithm, self, self._evp_pkey, self._rsa_cdata)

    def sign(self, data: bytes, padding: AsymmetricPadding, algorithm: typing.Union[(asym_utils.Prehashed, hashes.HashAlgorithm)]) -> bytes:
        data, algorithm = _calculate_digest_and_algorithm(self._backend, data, algorithm)
        return _rsa_sig_sign(self._backend, padding, algorithm, self, data)


class _RSAPublicKey(RSAPublicKey):

    def __init__(self, backend, rsa_cdata, evp_pkey):
        self._backend = backend
        self._rsa_cdata = rsa_cdata
        self._evp_pkey = evp_pkey
        n = self._backend._ffi.new('BIGNUM **')
        self._backend._lib.RSA_get0_key(self._rsa_cdata, n, self._backend._ffi.NULL, self._backend._ffi.NULL)
        self._backend.openssl_assert(n[0] != self._backend._ffi.NULL)
        self._key_size = self._backend._lib.BN_num_bits(n[0])

    key_size = utils.read_only_property('_key_size')

    def verifier(self, signature: bytes, padding: AsymmetricPadding, algorithm: hashes.HashAlgorithm) -> AsymmetricVerificationContext:
        _warn_sign_verify_deprecated()
        utils._check_bytes'signature'signature
        _check_not_prehashed(algorithm)
        return _RSAVerificationContext(self._backend, self, signature, padding, algorithm)

    def encrypt(self, plaintext: bytes, padding: AsymmetricPadding) -> bytes:
        return _enc_dec_rsaself._backendselfplaintextpadding

    def public_numbers(self) -> RSAPublicNumbers:
        n = self._backend._ffi.new('BIGNUM **')
        e = self._backend._ffi.new('BIGNUM **')
        self._backend._lib.RSA_get0_key(self._rsa_cdata, n, e, self._backend._ffi.NULL)
        self._backend.openssl_assert(n[0] != self._backend._ffi.NULL)
        self._backend.openssl_assert(e[0] != self._backend._ffi.NULL)
        return RSAPublicNumbers(e=(self._backend._bn_to_int(e[0])),
          n=(self._backend._bn_to_int(n[0])))

    def public_bytes(self, encoding: serialization.Encoding, format: serialization.PublicFormat) -> bytes:
        return self._backend._public_key_bytes(encoding, format, self, self._evp_pkey, self._rsa_cdata)

    def verify(self, signature: bytes, data: bytes, padding: AsymmetricPadding, algorithm: typing.Union[(asym_utils.Prehashed, hashes.HashAlgorithm)]) -> None:
        data, algorithm = _calculate_digest_and_algorithm(self._backend, data, algorithm)
        return _rsa_sig_verify(self._backend, padding, algorithm, self, signature, data)

    def recover_data_from_signature(self, signature: bytes, padding: AsymmetricPadding, algorithm: typing.Optional[hashes.HashAlgorithm]) -> bytes:
        _check_not_prehashed(algorithm)
        return _rsa_sig_recover(self._backend, padding, algorithm, self, signature)