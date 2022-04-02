# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\bindings\openssl\_conditional.py


def cryptography_has_ec2m--- This code section failed: ---

 L.   7         0  BUILD_LIST_0          0 
                2  LOAD_CONST               ('EC_POINT_set_affine_coordinates_GF2m', 'EC_POINT_get_affine_coordinates_GF2m', 'EC_POINT_set_compressed_coordinates_GF2m')
                4  CALL_FINALLY          7  'to 7'
                6  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def cryptography_has_rsa_oaep_md():
    return [
     'EVP_PKEY_CTX_set_rsa_oaep_md']


def cryptography_has_rsa_oaep_label():
    return [
     'EVP_PKEY_CTX_set0_rsa_oaep_label']


def cryptography_has_ssl3_method--- This code section failed: ---

 L.  27         0  BUILD_LIST_0          0 
                2  LOAD_CONST               ('SSLv3_method', 'SSLv3_client_method', 'SSLv3_server_method')
                4  CALL_FINALLY          7  'to 7'
                6  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def cryptography_has_102_verification--- This code section failed: ---

 L.  35         0  BUILD_LIST_0          0 
                2  LOAD_CONST               ('X509_V_ERR_SUITE_B_INVALID_VERSION', 'X509_V_ERR_SUITE_B_INVALID_ALGORITHM', 'X509_V_ERR_SUITE_B_INVALID_CURVE', 'X509_V_ERR_SUITE_B_INVALID_SIGNATURE_ALGORITHM', 'X509_V_ERR_SUITE_B_LOS_NOT_ALLOWED', 'X509_V_ERR_SUITE_B_CANNOT_SIGN_P_384_WITH_P_256', 'X509_V_FLAG_SUITEB_128_LOS_ONLY', 'X509_V_FLAG_SUITEB_192_LOS', 'X509_V_FLAG_SUITEB_128_LOS')
                4  CALL_FINALLY          7  'to 7'
                6  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def cryptography_has_110_verification_params():
    return [
     'X509_CHECK_FLAG_NEVER_CHECK_SUBJECT']


def cryptography_has_set_cert_cb():
    return [
     'SSL_CTX_set_cert_cb',
     'SSL_set_cert_cb']


def cryptography_has_ssl_st--- This code section failed: ---

 L.  60         0  BUILD_LIST_0          0 
                2  LOAD_CONST               ('SSL_ST_BEFORE', 'SSL_ST_OK', 'SSL_ST_INIT', 'SSL_ST_RENEGOTIATE')
                4  CALL_FINALLY          7  'to 7'
                6  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def cryptography_has_tls_st():
    return [
     'TLS_ST_BEFORE',
     'TLS_ST_OK']


def cryptography_has_scrypt():
    return [
     'EVP_PBE_scrypt']


def cryptography_has_evp_pkey_dhx():
    return [
     'EVP_PKEY_DHX']


def cryptography_has_mem_functions():
    return [
     'Cryptography_CRYPTO_set_mem_functions']


def cryptography_has_sct--- This code section failed: ---

 L.  94         0  BUILD_LIST_0          0 
                2  LOAD_CONST               ('SCT_get_version', 'SCT_get_log_entry_type', 'SCT_get0_log_id', 'SCT_get0_signature', 'SCT_get_timestamp', 'SCT_set_source', 'sk_SCT_new_null', 'sk_SCT_free', 'sk_SCT_num', 'sk_SCT_value', 'sk_SCT_push', 'SCT_LIST_free', 'SCT_new', 'SCT_set1_log_id', 'SCT_set_timestamp', 'SCT_set_version', 'SCT_set_log_entry_type')
                4  CALL_FINALLY          7  'to 7'
                6  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def cryptography_has_x509_store_ctx_get_issuer():
    return [
     'X509_STORE_get_get_issuer',
     'X509_STORE_set_get_issuer']


def cryptography_has_ed448():
    return [
     'EVP_PKEY_ED448',
     'NID_ED448']


def cryptography_has_ed25519():
    return [
     'NID_ED25519',
     'EVP_PKEY_ED25519']


def cryptography_has_poly1305():
    return [
     'NID_poly1305',
     'EVP_PKEY_POLY1305']


def cryptography_has_oneshot_evp_digest_sign_verify():
    return [
     'EVP_DigestSign',
     'EVP_DigestVerify']


def cryptography_has_evp_digestfinal_xof():
    return [
     'EVP_DigestFinalXOF']


def cryptography_has_evp_pkey_get_set_tls_encodedpoint():
    return [
     'EVP_PKEY_get1_tls_encodedpoint',
     'EVP_PKEY_set1_tls_encodedpoint']


def cryptography_has_fips():
    return [
     'FIPS_mode_set',
     'FIPS_mode']


def cryptography_has_ssl_sigalgs():
    return [
     'SSL_CTX_set1_sigalgs_list',
     'SSL_get_sigalgs']


def cryptography_has_psk--- This code section failed: ---

 L. 178         0  BUILD_LIST_0          0 
                2  LOAD_CONST               ('SSL_CTX_use_psk_identity_hint', 'SSL_CTX_set_psk_server_callback', 'SSL_CTX_set_psk_client_callback')
                4  CALL_FINALLY          7  'to 7'
                6  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def cryptography_has_custom_ext--- This code section failed: ---

 L. 186         0  BUILD_LIST_0          0 
                2  LOAD_CONST               ('SSL_CTX_add_client_custom_ext', 'SSL_CTX_add_server_custom_ext', 'SSL_extension_supported')
                4  CALL_FINALLY          7  'to 7'
                6  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def cryptography_has_openssl_cleanup():
    return [
     'OPENSSL_cleanup']


def cryptography_has_tlsv13--- This code section failed: ---

 L. 200         0  BUILD_LIST_0          0 
                2  LOAD_CONST               ('TLS1_3_VERSION', 'SSL_OP_NO_TLSv1_3', 'SSL_VERIFY_POST_HANDSHAKE', 'SSL_CTX_set_ciphersuites', 'SSL_verify_client_post_handshake', 'SSL_CTX_set_post_handshake_auth', 'SSL_set_post_handshake_auth', 'SSL_SESSION_get_max_early_data', 'SSL_write_early_data', 'SSL_read_early_data', 'SSL_CTX_set_max_early_data')
                4  CALL_FINALLY          7  'to 7'
                6  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def cryptography_has_keylog():
    return [
     'SSL_CTX_set_keylog_callback',
     'SSL_CTX_get_keylog_callback']


def cryptography_has_raw_key--- This code section failed: ---

 L. 223         0  BUILD_LIST_0          0 
                2  LOAD_CONST               ('EVP_PKEY_new_raw_private_key', 'EVP_PKEY_new_raw_public_key', 'EVP_PKEY_get_raw_private_key', 'EVP_PKEY_get_raw_public_key')
                4  CALL_FINALLY          7  'to 7'
                6  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def cryptography_has_engine--- This code section failed: ---

 L. 232         0  BUILD_LIST_0          0 
                2  LOAD_CONST               ('ENGINE_by_id', 'ENGINE_init', 'ENGINE_finish', 'ENGINE_get_default_RAND', 'ENGINE_set_default_RAND', 'ENGINE_unregister_RAND', 'ENGINE_ctrl_cmd', 'ENGINE_free', 'ENGINE_get_name', 'Cryptography_add_osrandom_engine', 'ENGINE_ctrl_cmd_string', 'ENGINE_load_builtin_engines', 'ENGINE_load_private_key', 'ENGINE_load_public_key')
                4  CALL_FINALLY          7  'to 7'
                6  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def cryptography_has_verified_chain():
    return [
     'SSL_get0_verified_chain']


def cryptography_has_srtp--- This code section failed: ---

 L. 257         0  BUILD_LIST_0          0 
                2  LOAD_CONST               ('SSL_CTX_set_tlsext_use_srtp', 'SSL_set_tlsext_use_srtp', 'SSL_get_selected_srtp_profile')
                4  CALL_FINALLY          7  'to 7'
                6  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def cryptography_has_get_proto_version--- This code section failed: ---

 L. 265         0  BUILD_LIST_0          0 
                2  LOAD_CONST               ('SSL_CTX_get_min_proto_version', 'SSL_CTX_get_max_proto_version', 'SSL_get_min_proto_version', 'SSL_get_max_proto_version')
                4  CALL_FINALLY          7  'to 7'
                6  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


CONDITIONAL_NAMES = {'Cryptography_HAS_EC2M':cryptography_has_ec2m, 
 'Cryptography_HAS_RSA_OAEP_MD':cryptography_has_rsa_oaep_md, 
 'Cryptography_HAS_RSA_OAEP_LABEL':cryptography_has_rsa_oaep_label, 
 'Cryptography_HAS_SSL3_METHOD':cryptography_has_ssl3_method, 
 'Cryptography_HAS_102_VERIFICATION':cryptography_has_102_verification, 
 'Cryptography_HAS_110_VERIFICATION_PARAMS':cryptography_has_110_verification_params, 
 'Cryptography_HAS_SET_CERT_CB':cryptography_has_set_cert_cb, 
 'Cryptography_HAS_SSL_ST':cryptography_has_ssl_st, 
 'Cryptography_HAS_TLS_ST':cryptography_has_tls_st, 
 'Cryptography_HAS_SCRYPT':cryptography_has_scrypt, 
 'Cryptography_HAS_EVP_PKEY_DHX':cryptography_has_evp_pkey_dhx, 
 'Cryptography_HAS_MEM_FUNCTIONS':cryptography_has_mem_functions, 
 'Cryptography_HAS_SCT':cryptography_has_sct, 
 'Cryptography_HAS_X509_STORE_CTX_GET_ISSUER':cryptography_has_x509_store_ctx_get_issuer, 
 'Cryptography_HAS_ED448':cryptography_has_ed448, 
 'Cryptography_HAS_ED25519':cryptography_has_ed25519, 
 'Cryptography_HAS_POLY1305':cryptography_has_poly1305, 
 'Cryptography_HAS_ONESHOT_EVP_DIGEST_SIGN_VERIFY':cryptography_has_oneshot_evp_digest_sign_verify, 
 'Cryptography_HAS_EVP_PKEY_get_set_tls_encodedpoint':cryptography_has_evp_pkey_get_set_tls_encodedpoint, 
 'Cryptography_HAS_FIPS':cryptography_has_fips, 
 'Cryptography_HAS_SIGALGS':cryptography_has_ssl_sigalgs, 
 'Cryptography_HAS_PSK':cryptography_has_psk, 
 'Cryptography_HAS_CUSTOM_EXT':cryptography_has_custom_ext, 
 'Cryptography_HAS_OPENSSL_CLEANUP':cryptography_has_openssl_cleanup, 
 'Cryptography_HAS_TLSv1_3':cryptography_has_tlsv13, 
 'Cryptography_HAS_KEYLOG':cryptography_has_keylog, 
 'Cryptography_HAS_RAW_KEY':cryptography_has_raw_key, 
 'Cryptography_HAS_EVP_DIGESTFINAL_XOF':cryptography_has_evp_digestfinal_xof, 
 'Cryptography_HAS_ENGINE':cryptography_has_engine, 
 'Cryptography_HAS_VERIFIED_CHAIN':cryptography_has_verified_chain, 
 'Cryptography_HAS_SRTP':cryptography_has_srtp, 
 'Cryptography_HAS_GET_PROTO_VERSION':cryptography_has_get_proto_version}