# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\backends\openssl\ciphers.py
from cryptography import utils
from cryptography.exceptions import InvalidTag, UnsupportedAlgorithm, _Reasons
from cryptography.hazmat.primitives import ciphers
from cryptography.hazmat.primitives.ciphers import modes

@utils.register_interface(ciphers.CipherContext)
@utils.register_interface(ciphers.AEADCipherContext)
@utils.register_interface(ciphers.AEADEncryptionContext)
@utils.register_interface(ciphers.AEADDecryptionContext)
class _CipherContext(object):
    _ENCRYPT = 1
    _DECRYPT = 0
    _MAX_CHUNK_SIZE = 1073741823

    def __init__--- This code section failed: ---

 L.  22         0  LOAD_FAST                'backend'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _backend

 L.  23         6  LOAD_FAST                'cipher'
                8  LOAD_FAST                'self'
               10  STORE_ATTR               _cipher

 L.  24        12  LOAD_FAST                'mode'
               14  LOAD_FAST                'self'
               16  STORE_ATTR               _mode

 L.  25        18  LOAD_FAST                'operation'
               20  LOAD_FAST                'self'
               22  STORE_ATTR               _operation

 L.  26        24  LOAD_CONST               None
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _tag

 L.  28        30  LOAD_GLOBAL              isinstance
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                _cipher
               36  LOAD_GLOBAL              ciphers
               38  LOAD_ATTR                BlockCipherAlgorithm
               40  CALL_FUNCTION_2       2  ''
               42  POP_JUMP_IF_FALSE    60  'to 60'

 L.  29        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _cipher
               48  LOAD_ATTR                block_size
               50  LOAD_CONST               8
               52  BINARY_FLOOR_DIVIDE
               54  LOAD_FAST                'self'
               56  STORE_ATTR               _block_size_bytes
               58  JUMP_FORWARD         66  'to 66'
             60_0  COME_FROM            42  '42'

 L.  31        60  LOAD_CONST               1
               62  LOAD_FAST                'self'
               64  STORE_ATTR               _block_size_bytes
             66_0  COME_FROM            58  '58'

 L.  33        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _backend
               70  LOAD_ATTR                _lib
               72  LOAD_METHOD              EVP_CIPHER_CTX_new
               74  CALL_METHOD_0         0  ''
               76  STORE_FAST               'ctx'

 L.  34        78  LOAD_FAST                'self'
               80  LOAD_ATTR                _backend
               82  LOAD_ATTR                _ffi
               84  LOAD_METHOD              gc

 L.  35        86  LOAD_FAST                'ctx'
               88  LOAD_FAST                'self'
               90  LOAD_ATTR                _backend
               92  LOAD_ATTR                _lib
               94  LOAD_ATTR                EVP_CIPHER_CTX_free

 L.  34        96  CALL_METHOD_2         2  ''
               98  STORE_FAST               'ctx'

 L.  38       100  LOAD_FAST                'self'
              102  LOAD_ATTR                _backend
              104  LOAD_ATTR                _cipher_registry
              106  STORE_FAST               'registry'

 L.  39       108  SETUP_FINALLY       134  'to 134'

 L.  40       110  LOAD_FAST                'registry'
              112  LOAD_GLOBAL              type
              114  LOAD_FAST                'cipher'
              116  CALL_FUNCTION_1       1  ''
              118  LOAD_GLOBAL              type
              120  LOAD_FAST                'mode'
              122  CALL_FUNCTION_1       1  ''
              124  BUILD_TUPLE_2         2 
              126  BINARY_SUBSCR    
              128  STORE_FAST               'adapter'
              130  POP_BLOCK        
              132  JUMP_FORWARD        184  'to 184'
            134_0  COME_FROM_FINALLY   108  '108'

 L.  41       134  DUP_TOP          
              136  LOAD_GLOBAL              KeyError
              138  <121>               182  ''
              140  POP_TOP          
              142  POP_TOP          
              144  POP_TOP          

 L.  42       146  LOAD_GLOBAL              UnsupportedAlgorithm

 L.  43       148  LOAD_STR                 'cipher {} in {} mode is not supported by this backend.'
              150  LOAD_METHOD              format

 L.  45       152  LOAD_FAST                'cipher'
              154  LOAD_ATTR                name
              156  LOAD_FAST                'mode'
              158  POP_JUMP_IF_FALSE   166  'to 166'
              160  LOAD_FAST                'mode'
              162  LOAD_ATTR                name
              164  JUMP_FORWARD        168  'to 168'
            166_0  COME_FROM           158  '158'
              166  LOAD_FAST                'mode'
            168_0  COME_FROM           164  '164'

 L.  43       168  CALL_METHOD_2         2  ''

 L.  47       170  LOAD_GLOBAL              _Reasons
              172  LOAD_ATTR                UNSUPPORTED_CIPHER

 L.  42       174  CALL_FUNCTION_2       2  ''
              176  RAISE_VARARGS_1       1  'exception instance'
              178  POP_EXCEPT       
              180  JUMP_FORWARD        184  'to 184'
              182  <48>             
            184_0  COME_FROM           180  '180'
            184_1  COME_FROM           132  '132'

 L.  50       184  LOAD_FAST                'adapter'
              186  LOAD_FAST                'self'
              188  LOAD_ATTR                _backend
              190  LOAD_FAST                'cipher'
              192  LOAD_FAST                'mode'
              194  CALL_FUNCTION_3       3  ''
              196  STORE_FAST               'evp_cipher'

 L.  51       198  LOAD_FAST                'evp_cipher'
              200  LOAD_FAST                'self'
              202  LOAD_ATTR                _backend
              204  LOAD_ATTR                _ffi
              206  LOAD_ATTR                NULL
              208  COMPARE_OP               ==
          210_212  POP_JUMP_IF_FALSE   278  'to 278'

 L.  52       214  LOAD_STR                 'cipher {0.name} '
              216  LOAD_METHOD              format
              218  LOAD_FAST                'cipher'
              220  CALL_METHOD_1         1  ''
              222  STORE_FAST               'msg'

 L.  53       224  LOAD_FAST                'mode'
              226  LOAD_CONST               None
              228  <117>                 1  ''
              230  POP_JUMP_IF_FALSE   246  'to 246'

 L.  54       232  LOAD_FAST                'msg'
              234  LOAD_STR                 'in {0.name} mode '
              236  LOAD_METHOD              format
              238  LOAD_FAST                'mode'
              240  CALL_METHOD_1         1  ''
              242  INPLACE_ADD      
              244  STORE_FAST               'msg'
            246_0  COME_FROM           230  '230'

 L.  55       246  LOAD_FAST                'msg'

 L.  56       248  LOAD_STR                 'is not supported by this backend (Your version of OpenSSL may be too old. Current version: {}.)'

 L.  55       250  LOAD_METHOD              format

 L.  58       252  LOAD_FAST                'self'
              254  LOAD_ATTR                _backend
              256  LOAD_METHOD              openssl_version_text
              258  CALL_METHOD_0         0  ''

 L.  55       260  CALL_METHOD_1         1  ''
              262  INPLACE_ADD      
              264  STORE_FAST               'msg'

 L.  59       266  LOAD_GLOBAL              UnsupportedAlgorithm
              268  LOAD_FAST                'msg'
              270  LOAD_GLOBAL              _Reasons
              272  LOAD_ATTR                UNSUPPORTED_CIPHER
              274  CALL_FUNCTION_2       2  ''
              276  RAISE_VARARGS_1       1  'exception instance'
            278_0  COME_FROM           210  '210'

 L.  61       278  LOAD_GLOBAL              isinstance
              280  LOAD_FAST                'mode'
              282  LOAD_GLOBAL              modes
              284  LOAD_ATTR                ModeWithInitializationVector
              286  CALL_FUNCTION_2       2  ''
          288_290  POP_JUMP_IF_FALSE   310  'to 310'

 L.  62       292  LOAD_FAST                'self'
              294  LOAD_ATTR                _backend
              296  LOAD_ATTR                _ffi
              298  LOAD_METHOD              from_buffer

 L.  63       300  LOAD_FAST                'mode'
              302  LOAD_ATTR                initialization_vector

 L.  62       304  CALL_METHOD_1         1  ''
              306  STORE_FAST               'iv_nonce'
              308  JUMP_FORWARD        416  'to 416'
            310_0  COME_FROM           288  '288'

 L.  65       310  LOAD_GLOBAL              isinstance
              312  LOAD_FAST                'mode'
              314  LOAD_GLOBAL              modes
              316  LOAD_ATTR                ModeWithTweak
              318  CALL_FUNCTION_2       2  ''
          320_322  POP_JUMP_IF_FALSE   342  'to 342'

 L.  66       324  LOAD_FAST                'self'
              326  LOAD_ATTR                _backend
              328  LOAD_ATTR                _ffi
              330  LOAD_METHOD              from_buffer
              332  LOAD_FAST                'mode'
              334  LOAD_ATTR                tweak
              336  CALL_METHOD_1         1  ''
              338  STORE_FAST               'iv_nonce'
              340  JUMP_FORWARD        416  'to 416'
            342_0  COME_FROM           320  '320'

 L.  67       342  LOAD_GLOBAL              isinstance
              344  LOAD_FAST                'mode'
              346  LOAD_GLOBAL              modes
              348  LOAD_ATTR                ModeWithNonce
              350  CALL_FUNCTION_2       2  ''
          352_354  POP_JUMP_IF_FALSE   374  'to 374'

 L.  68       356  LOAD_FAST                'self'
              358  LOAD_ATTR                _backend
              360  LOAD_ATTR                _ffi
              362  LOAD_METHOD              from_buffer
              364  LOAD_FAST                'mode'
              366  LOAD_ATTR                nonce
              368  CALL_METHOD_1         1  ''
              370  STORE_FAST               'iv_nonce'
              372  JUMP_FORWARD        416  'to 416'
            374_0  COME_FROM           352  '352'

 L.  69       374  LOAD_GLOBAL              isinstance
              376  LOAD_FAST                'cipher'
              378  LOAD_GLOBAL              modes
              380  LOAD_ATTR                ModeWithNonce
              382  CALL_FUNCTION_2       2  ''
          384_386  POP_JUMP_IF_FALSE   406  'to 406'

 L.  70       388  LOAD_FAST                'self'
              390  LOAD_ATTR                _backend
              392  LOAD_ATTR                _ffi
              394  LOAD_METHOD              from_buffer
              396  LOAD_FAST                'cipher'
              398  LOAD_ATTR                nonce
              400  CALL_METHOD_1         1  ''
              402  STORE_FAST               'iv_nonce'
              404  JUMP_FORWARD        416  'to 416'
            406_0  COME_FROM           384  '384'

 L.  72       406  LOAD_FAST                'self'
              408  LOAD_ATTR                _backend
              410  LOAD_ATTR                _ffi
              412  LOAD_ATTR                NULL
              414  STORE_FAST               'iv_nonce'
            416_0  COME_FROM           404  '404'
            416_1  COME_FROM           372  '372'
            416_2  COME_FROM           340  '340'
            416_3  COME_FROM           308  '308'

 L.  74       416  LOAD_FAST                'self'
              418  LOAD_ATTR                _backend
              420  LOAD_ATTR                _lib
              422  LOAD_METHOD              EVP_CipherInit_ex

 L.  75       424  LOAD_FAST                'ctx'

 L.  76       426  LOAD_FAST                'evp_cipher'

 L.  77       428  LOAD_FAST                'self'
              430  LOAD_ATTR                _backend
              432  LOAD_ATTR                _ffi
              434  LOAD_ATTR                NULL

 L.  78       436  LOAD_FAST                'self'
              438  LOAD_ATTR                _backend
              440  LOAD_ATTR                _ffi
              442  LOAD_ATTR                NULL

 L.  79       444  LOAD_FAST                'self'
              446  LOAD_ATTR                _backend
              448  LOAD_ATTR                _ffi
              450  LOAD_ATTR                NULL

 L.  80       452  LOAD_FAST                'operation'

 L.  74       454  CALL_METHOD_6         6  ''
              456  STORE_FAST               'res'

 L.  82       458  LOAD_FAST                'self'
              460  LOAD_ATTR                _backend
              462  LOAD_METHOD              openssl_assert
              464  LOAD_FAST                'res'
              466  LOAD_CONST               0
              468  COMPARE_OP               !=
              470  CALL_METHOD_1         1  ''
              472  POP_TOP          

 L.  84       474  LOAD_FAST                'self'
              476  LOAD_ATTR                _backend
              478  LOAD_ATTR                _lib
              480  LOAD_METHOD              EVP_CIPHER_CTX_set_key_length

 L.  85       482  LOAD_FAST                'ctx'
              484  LOAD_GLOBAL              len
              486  LOAD_FAST                'cipher'
              488  LOAD_ATTR                key
              490  CALL_FUNCTION_1       1  ''

 L.  84       492  CALL_METHOD_2         2  ''
              494  STORE_FAST               'res'

 L.  87       496  LOAD_FAST                'self'
              498  LOAD_ATTR                _backend
              500  LOAD_METHOD              openssl_assert
              502  LOAD_FAST                'res'
              504  LOAD_CONST               0
              506  COMPARE_OP               !=
              508  CALL_METHOD_1         1  ''
              510  POP_TOP          

 L.  88       512  LOAD_GLOBAL              isinstance
              514  LOAD_FAST                'mode'
              516  LOAD_GLOBAL              modes
              518  LOAD_ATTR                GCM
              520  CALL_FUNCTION_2       2  ''
          522_524  POP_JUMP_IF_FALSE   648  'to 648'

 L.  89       526  LOAD_FAST                'self'
              528  LOAD_ATTR                _backend
              530  LOAD_ATTR                _lib
              532  LOAD_METHOD              EVP_CIPHER_CTX_ctrl

 L.  90       534  LOAD_FAST                'ctx'

 L.  91       536  LOAD_FAST                'self'
              538  LOAD_ATTR                _backend
              540  LOAD_ATTR                _lib
              542  LOAD_ATTR                EVP_CTRL_AEAD_SET_IVLEN

 L.  92       544  LOAD_GLOBAL              len
              546  LOAD_FAST                'iv_nonce'
              548  CALL_FUNCTION_1       1  ''

 L.  93       550  LOAD_FAST                'self'
              552  LOAD_ATTR                _backend
              554  LOAD_ATTR                _ffi
              556  LOAD_ATTR                NULL

 L.  89       558  CALL_METHOD_4         4  ''
              560  STORE_FAST               'res'

 L.  95       562  LOAD_FAST                'self'
              564  LOAD_ATTR                _backend
              566  LOAD_METHOD              openssl_assert
              568  LOAD_FAST                'res'
              570  LOAD_CONST               0
              572  COMPARE_OP               !=
              574  CALL_METHOD_1         1  ''
              576  POP_TOP          

 L.  96       578  LOAD_FAST                'mode'
              580  LOAD_ATTR                tag
              582  LOAD_CONST               None
              584  <117>                 1  ''
          586_588  POP_JUMP_IF_FALSE   648  'to 648'

 L.  97       590  LOAD_FAST                'self'
              592  LOAD_ATTR                _backend
              594  LOAD_ATTR                _lib
              596  LOAD_METHOD              EVP_CIPHER_CTX_ctrl

 L.  98       598  LOAD_FAST                'ctx'

 L.  99       600  LOAD_FAST                'self'
              602  LOAD_ATTR                _backend
              604  LOAD_ATTR                _lib
              606  LOAD_ATTR                EVP_CTRL_AEAD_SET_TAG

 L. 100       608  LOAD_GLOBAL              len
              610  LOAD_FAST                'mode'
              612  LOAD_ATTR                tag
              614  CALL_FUNCTION_1       1  ''

 L. 101       616  LOAD_FAST                'mode'
              618  LOAD_ATTR                tag

 L.  97       620  CALL_METHOD_4         4  ''
              622  STORE_FAST               'res'

 L. 103       624  LOAD_FAST                'self'
              626  LOAD_ATTR                _backend
              628  LOAD_METHOD              openssl_assert
              630  LOAD_FAST                'res'
              632  LOAD_CONST               0
              634  COMPARE_OP               !=
              636  CALL_METHOD_1         1  ''
              638  POP_TOP          

 L. 104       640  LOAD_FAST                'mode'
              642  LOAD_ATTR                tag
              644  LOAD_FAST                'self'
              646  STORE_ATTR               _tag
            648_0  COME_FROM           586  '586'
            648_1  COME_FROM           522  '522'

 L. 107       648  LOAD_FAST                'self'
              650  LOAD_ATTR                _backend
              652  LOAD_ATTR                _lib
              654  LOAD_METHOD              EVP_CipherInit_ex

 L. 108       656  LOAD_FAST                'ctx'

 L. 109       658  LOAD_FAST                'self'
              660  LOAD_ATTR                _backend
              662  LOAD_ATTR                _ffi
              664  LOAD_ATTR                NULL

 L. 110       666  LOAD_FAST                'self'
              668  LOAD_ATTR                _backend
              670  LOAD_ATTR                _ffi
              672  LOAD_ATTR                NULL

 L. 111       674  LOAD_FAST                'self'
              676  LOAD_ATTR                _backend
              678  LOAD_ATTR                _ffi
              680  LOAD_METHOD              from_buffer
              682  LOAD_FAST                'cipher'
              684  LOAD_ATTR                key
              686  CALL_METHOD_1         1  ''

 L. 112       688  LOAD_FAST                'iv_nonce'

 L. 113       690  LOAD_FAST                'operation'

 L. 107       692  CALL_METHOD_6         6  ''
              694  STORE_FAST               'res'

 L. 115       696  LOAD_FAST                'self'
              698  LOAD_ATTR                _backend
              700  LOAD_METHOD              openssl_assert
              702  LOAD_FAST                'res'
              704  LOAD_CONST               0
              706  COMPARE_OP               !=
              708  CALL_METHOD_1         1  ''
              710  POP_TOP          

 L. 118       712  LOAD_FAST                'self'
              714  LOAD_ATTR                _backend
              716  LOAD_ATTR                _lib
              718  LOAD_METHOD              EVP_CIPHER_CTX_set_padding
              720  LOAD_FAST                'ctx'
              722  LOAD_CONST               0
              724  CALL_METHOD_2         2  ''
              726  POP_TOP          

 L. 119       728  LOAD_FAST                'ctx'
              730  LOAD_FAST                'self'
              732  STORE_ATTR               _ctx

Parse error at or near `<121>' instruction at offset 138

    def update(self, data: bytes) -> bytes:
        buf = bytearray(len(data) + self._block_size_bytes - 1)
        n = self.update_intodatabuf
        return bytes(buf[:n])

    def update_into(self, data: bytes, buf) -> int:
        total_data_len = len(data)
        if len(buf) < total_data_len + self._block_size_bytes - 1:
            raise ValueError('buffer must be at least {} bytes for this payload'.format(len(data) + self._block_size_bytes - 1))
        else:
            data_processed = 0
            total_out = 0
            outlen = self._backend._ffi.new('int *')
            baseoutbuf = self._backend._ffi.from_buffer(buf)
            baseinbuf = self._backend._ffi.from_buffer(data)
            while True:
                if data_processed != total_data_len:
                    outbuf = baseoutbuf + total_out
                    inbuf = baseinbuf + data_processed
                    inlen = minself._MAX_CHUNK_SIZE(total_data_len - data_processed)
                    res = self._backend._lib.EVP_CipherUpdate(self._ctx, outbuf, outlen, inbuf, inlen)
                    self._backend.openssl_assert(res != 0)
                    data_processed += inlen
                    total_out += outlen[0]

        return total_out

    def finalize--- This code section failed: ---

 L. 156         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _operation
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _DECRYPT
                8  COMPARE_OP               ==

 L. 155        10  POP_JUMP_IF_FALSE    44  'to 44'

 L. 157        12  LOAD_GLOBAL              isinstance
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                _mode
               18  LOAD_GLOBAL              modes
               20  LOAD_ATTR                ModeWithAuthenticationTag
               22  CALL_FUNCTION_2       2  ''

 L. 155        24  POP_JUMP_IF_FALSE    44  'to 44'

 L. 158        26  LOAD_FAST                'self'
               28  LOAD_ATTR                tag
               30  LOAD_CONST               None
               32  <117>                 0  ''

 L. 155        34  POP_JUMP_IF_FALSE    44  'to 44'

 L. 160        36  LOAD_GLOBAL              ValueError

 L. 161        38  LOAD_STR                 'Authentication tag must be provided when decrypting.'

 L. 160        40  CALL_FUNCTION_1       1  ''
               42  RAISE_VARARGS_1       1  'exception instance'
             44_0  COME_FROM            34  '34'
             44_1  COME_FROM            24  '24'
             44_2  COME_FROM            10  '10'

 L. 164        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _backend
               48  LOAD_ATTR                _ffi
               50  LOAD_METHOD              new
               52  LOAD_STR                 'unsigned char[]'
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                _block_size_bytes
               58  CALL_METHOD_2         2  ''
               60  STORE_FAST               'buf'

 L. 165        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _backend
               66  LOAD_ATTR                _ffi
               68  LOAD_METHOD              new
               70  LOAD_STR                 'int *'
               72  CALL_METHOD_1         1  ''
               74  STORE_FAST               'outlen'

 L. 166        76  LOAD_FAST                'self'
               78  LOAD_ATTR                _backend
               80  LOAD_ATTR                _lib
               82  LOAD_METHOD              EVP_CipherFinal_ex
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                _ctx
               88  LOAD_FAST                'buf'
               90  LOAD_FAST                'outlen'
               92  CALL_METHOD_3         3  ''
               94  STORE_FAST               'res'

 L. 167        96  LOAD_FAST                'res'
               98  LOAD_CONST               0
              100  COMPARE_OP               ==
              102  POP_JUMP_IF_FALSE   184  'to 184'

 L. 168       104  LOAD_FAST                'self'
              106  LOAD_ATTR                _backend
              108  LOAD_METHOD              _consume_errors
              110  CALL_METHOD_0         0  ''
              112  STORE_FAST               'errors'

 L. 170       114  LOAD_FAST                'errors'
              116  POP_JUMP_IF_TRUE    136  'to 136'
              118  LOAD_GLOBAL              isinstance
              120  LOAD_FAST                'self'
              122  LOAD_ATTR                _mode
              124  LOAD_GLOBAL              modes
              126  LOAD_ATTR                GCM
              128  CALL_FUNCTION_2       2  ''
              130  POP_JUMP_IF_FALSE   136  'to 136'

 L. 171       132  LOAD_GLOBAL              InvalidTag
              134  RAISE_VARARGS_1       1  'exception instance'
            136_0  COME_FROM           130  '130'
            136_1  COME_FROM           116  '116'

 L. 173       136  LOAD_FAST                'self'
              138  LOAD_ATTR                _backend
              140  LOAD_ATTR                openssl_assert

 L. 174       142  LOAD_FAST                'errors'
              144  LOAD_CONST               0
              146  BINARY_SUBSCR    
              148  LOAD_METHOD              _lib_reason_match

 L. 175       150  LOAD_FAST                'self'
              152  LOAD_ATTR                _backend
              154  LOAD_ATTR                _lib
              156  LOAD_ATTR                ERR_LIB_EVP

 L. 176       158  LOAD_FAST                'self'
              160  LOAD_ATTR                _backend
              162  LOAD_ATTR                _lib
              164  LOAD_ATTR                EVP_R_DATA_NOT_MULTIPLE_OF_BLOCK_LENGTH

 L. 174       166  CALL_METHOD_2         2  ''

 L. 178       168  LOAD_FAST                'errors'

 L. 173       170  LOAD_CONST               ('errors',)
              172  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              174  POP_TOP          

 L. 180       176  LOAD_GLOBAL              ValueError

 L. 181       178  LOAD_STR                 'The length of the provided data is not a multiple of the block length.'

 L. 180       180  CALL_FUNCTION_1       1  ''
              182  RAISE_VARARGS_1       1  'exception instance'
            184_0  COME_FROM           102  '102'

 L. 186       184  LOAD_GLOBAL              isinstance
              186  LOAD_FAST                'self'
              188  LOAD_ATTR                _mode
              190  LOAD_GLOBAL              modes
              192  LOAD_ATTR                GCM
              194  CALL_FUNCTION_2       2  ''

 L. 185   196_198  POP_JUMP_IF_FALSE   302  'to 302'

 L. 187       200  LOAD_FAST                'self'
              202  LOAD_ATTR                _operation
              204  LOAD_FAST                'self'
              206  LOAD_ATTR                _ENCRYPT
              208  COMPARE_OP               ==

 L. 185   210_212  POP_JUMP_IF_FALSE   302  'to 302'

 L. 189       214  LOAD_FAST                'self'
              216  LOAD_ATTR                _backend
              218  LOAD_ATTR                _ffi
              220  LOAD_METHOD              new

 L. 190       222  LOAD_STR                 'unsigned char[]'
              224  LOAD_FAST                'self'
              226  LOAD_ATTR                _block_size_bytes

 L. 189       228  CALL_METHOD_2         2  ''
              230  STORE_FAST               'tag_buf'

 L. 192       232  LOAD_FAST                'self'
              234  LOAD_ATTR                _backend
              236  LOAD_ATTR                _lib
              238  LOAD_METHOD              EVP_CIPHER_CTX_ctrl

 L. 193       240  LOAD_FAST                'self'
              242  LOAD_ATTR                _ctx

 L. 194       244  LOAD_FAST                'self'
              246  LOAD_ATTR                _backend
              248  LOAD_ATTR                _lib
              250  LOAD_ATTR                EVP_CTRL_AEAD_GET_TAG

 L. 195       252  LOAD_FAST                'self'
              254  LOAD_ATTR                _block_size_bytes

 L. 196       256  LOAD_FAST                'tag_buf'

 L. 192       258  CALL_METHOD_4         4  ''
              260  STORE_FAST               'res'

 L. 198       262  LOAD_FAST                'self'
              264  LOAD_ATTR                _backend
              266  LOAD_METHOD              openssl_assert
              268  LOAD_FAST                'res'
              270  LOAD_CONST               0
              272  COMPARE_OP               !=
              274  CALL_METHOD_1         1  ''
              276  POP_TOP          

 L. 199       278  LOAD_FAST                'self'
              280  LOAD_ATTR                _backend
              282  LOAD_ATTR                _ffi
              284  LOAD_METHOD              buffer
              286  LOAD_FAST                'tag_buf'
              288  CALL_METHOD_1         1  ''
              290  LOAD_CONST               None
              292  LOAD_CONST               None
              294  BUILD_SLICE_2         2 
              296  BINARY_SUBSCR    
              298  LOAD_FAST                'self'
              300  STORE_ATTR               _tag
            302_0  COME_FROM           210  '210'
            302_1  COME_FROM           196  '196'

 L. 201       302  LOAD_FAST                'self'
              304  LOAD_ATTR                _backend
              306  LOAD_ATTR                _lib
              308  LOAD_METHOD              EVP_CIPHER_CTX_reset
              310  LOAD_FAST                'self'
              312  LOAD_ATTR                _ctx
              314  CALL_METHOD_1         1  ''
              316  STORE_FAST               'res'

 L. 202       318  LOAD_FAST                'self'
              320  LOAD_ATTR                _backend
              322  LOAD_METHOD              openssl_assert
              324  LOAD_FAST                'res'
              326  LOAD_CONST               1
              328  COMPARE_OP               ==
              330  CALL_METHOD_1         1  ''
              332  POP_TOP          

 L. 203       334  LOAD_FAST                'self'
              336  LOAD_ATTR                _backend
              338  LOAD_ATTR                _ffi
              340  LOAD_METHOD              buffer
              342  LOAD_FAST                'buf'
              344  CALL_METHOD_1         1  ''
              346  LOAD_CONST               None
              348  LOAD_FAST                'outlen'
              350  LOAD_CONST               0
              352  BINARY_SUBSCR    
              354  BUILD_SLICE_2         2 
              356  BINARY_SUBSCR    
              358  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 32

    def finalize_with_tag(self, tag: bytes) -> bytes:
        if len(tag) < self._mode._min_tag_length:
            raise ValueError('Authentication tag must be {} bytes or longer.'.format(self._mode._min_tag_length))
        res = self._backend._lib.EVP_CIPHER_CTX_ctrlself._ctxself._backend._lib.EVP_CTRL_AEAD_SET_TAGlen(tag)tag
        self._backend.openssl_assert(res != 0)
        self._tag = tag
        return self.finalize

    def authenticate_additional_data(self, data: bytes) -> None:
        outlen = self._backend._ffi.new('int *')
        res = self._backend._lib.EVP_CipherUpdate(self._ctx, self._backend._ffi.NULL, outlen, self._backend._ffi.from_buffer(data), len(data))
        self._backend.openssl_assert(res != 0)

    tag = utils.read_only_property('_tag')