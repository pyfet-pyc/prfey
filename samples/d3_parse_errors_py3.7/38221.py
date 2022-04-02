# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\paramiko\ed25519key.py
import bcrypt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher
import nacl.signing, six
from paramiko.message import Message
from paramiko.pkey import PKey
from paramiko.py3compat import b
from paramiko.ssh_exception import SSHException, PasswordRequiredException
OPENSSH_AUTH_MAGIC = 'openssh-key-v1\x00'

def unpad(data):
    padding_length = six.indexbytes(data, -1)
    if 32 <= padding_length < 127:
        return data
    if padding_length > 15:
        raise SSHException('Invalid key')
    for i in range(padding_length):
        if six.indexbytes(data, i - padding_length) != i + 1:
            raise SSHException('Invalid key')

    return data[:-padding_length]


class Ed25519Key(PKey):
    __doc__ = '\n    Representation of an `Ed25519 <https://ed25519.cr.yp.to/>`_ key.\n\n    .. note::\n        Ed25519 key support was added to OpenSSH in version 6.5.\n\n    .. versionadded:: 2.2\n    .. versionchanged:: 2.3\n        Added a ``file_obj`` parameter to match other key classes.\n    '

    def __init__(self, msg=None, data=None, filename=None, password=None, file_obj=None):
        self.public_blob = None
        verifying_key = signing_key = None
        if msg is None:
            if data is not None:
                msg = Message(data)
        if msg is not None:
            self._check_type_and_load_cert(msg=msg,
              key_type='ssh-ed25519',
              cert_type='ssh-ed25519-cert-v01@openssh.com')
            verifying_key = nacl.signing.VerifyKey(msg.get_binary())
        elif filename is not None:
            with open(filename, 'r') as f:
                pkformat, data = self._read_private_key('OPENSSH', f)
        elif file_obj is not None:
            pkformat, data = self._read_private_key('OPENSSH', file_obj)
        if filename or (file_obj):
            signing_key = self._parse_signing_key_data(data, password)
        if signing_key is None:
            if verifying_key is None:
                raise ValueError('need a key')
        self._signing_key = signing_key
        self._verifying_key = verifying_key

    def _parse_signing_key_data--- This code section failed: ---

 L.  92         0  LOAD_CONST               0
                2  LOAD_CONST               ('Transport',)
                4  IMPORT_NAME_ATTR         paramiko.transport
                6  IMPORT_FROM              Transport
                8  STORE_FAST               'Transport'
               10  POP_TOP          

 L. 100        12  LOAD_GLOBAL              Message
               14  LOAD_FAST                'data'
               16  CALL_FUNCTION_1       1  '1 positional argument'
               18  STORE_FAST               'message'

 L. 101        20  LOAD_FAST                'message'
               22  LOAD_METHOD              get_bytes
               24  LOAD_GLOBAL              len
               26  LOAD_GLOBAL              OPENSSH_AUTH_MAGIC
               28  CALL_FUNCTION_1       1  '1 positional argument'
               30  CALL_METHOD_1         1  '1 positional argument'
               32  LOAD_GLOBAL              OPENSSH_AUTH_MAGIC
               34  COMPARE_OP               !=
               36  POP_JUMP_IF_FALSE    46  'to 46'

 L. 102        38  LOAD_GLOBAL              SSHException
               40  LOAD_STR                 'Invalid key'
               42  CALL_FUNCTION_1       1  '1 positional argument'
               44  RAISE_VARARGS_1       1  'exception instance'
             46_0  COME_FROM            36  '36'

 L. 104        46  LOAD_FAST                'message'
               48  LOAD_METHOD              get_text
               50  CALL_METHOD_0         0  '0 positional arguments'
               52  STORE_FAST               'ciphername'

 L. 105        54  LOAD_FAST                'message'
               56  LOAD_METHOD              get_text
               58  CALL_METHOD_0         0  '0 positional arguments'
               60  STORE_FAST               'kdfname'

 L. 106        62  LOAD_FAST                'message'
               64  LOAD_METHOD              get_binary
               66  CALL_METHOD_0         0  '0 positional arguments'
               68  STORE_FAST               'kdfoptions'

 L. 107        70  LOAD_FAST                'message'
               72  LOAD_METHOD              get_int
               74  CALL_METHOD_0         0  '0 positional arguments'
               76  STORE_FAST               'num_keys'

 L. 109        78  LOAD_FAST                'kdfname'
               80  LOAD_STR                 'none'
               82  COMPARE_OP               ==
               84  POP_JUMP_IF_FALSE   108  'to 108'

 L. 112        86  LOAD_FAST                'kdfoptions'
               88  POP_JUMP_IF_TRUE     98  'to 98'
               90  LOAD_FAST                'ciphername'
               92  LOAD_STR                 'none'
               94  COMPARE_OP               !=
               96  POP_JUMP_IF_FALSE   162  'to 162'
             98_0  COME_FROM            88  '88'

 L. 113        98  LOAD_GLOBAL              SSHException
              100  LOAD_STR                 'Invalid key'
              102  CALL_FUNCTION_1       1  '1 positional argument'
              104  RAISE_VARARGS_1       1  'exception instance'
              106  JUMP_FORWARD        162  'to 162'
            108_0  COME_FROM            84  '84'

 L. 114       108  LOAD_FAST                'kdfname'
              110  LOAD_STR                 'bcrypt'
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   154  'to 154'

 L. 115       116  LOAD_FAST                'password'
              118  POP_JUMP_IF_TRUE    128  'to 128'

 L. 116       120  LOAD_GLOBAL              PasswordRequiredException

 L. 117       122  LOAD_STR                 'Private key file is encrypted'
              124  CALL_FUNCTION_1       1  '1 positional argument'
              126  RAISE_VARARGS_1       1  'exception instance'
            128_0  COME_FROM           118  '118'

 L. 119       128  LOAD_GLOBAL              Message
              130  LOAD_FAST                'kdfoptions'
              132  CALL_FUNCTION_1       1  '1 positional argument'
              134  STORE_FAST               'kdf'

 L. 120       136  LOAD_FAST                'kdf'
              138  LOAD_METHOD              get_binary
              140  CALL_METHOD_0         0  '0 positional arguments'
              142  STORE_FAST               'bcrypt_salt'

 L. 121       144  LOAD_FAST                'kdf'
              146  LOAD_METHOD              get_int
              148  CALL_METHOD_0         0  '0 positional arguments'
              150  STORE_FAST               'bcrypt_rounds'
              152  JUMP_FORWARD        162  'to 162'
            154_0  COME_FROM           114  '114'

 L. 123       154  LOAD_GLOBAL              SSHException
              156  LOAD_STR                 'Invalid key'
              158  CALL_FUNCTION_1       1  '1 positional argument'
              160  RAISE_VARARGS_1       1  'exception instance'
            162_0  COME_FROM           152  '152'
            162_1  COME_FROM           106  '106'
            162_2  COME_FROM            96  '96'

 L. 125       162  LOAD_FAST                'ciphername'
              164  LOAD_STR                 'none'
              166  COMPARE_OP               !=
              168  POP_JUMP_IF_FALSE   188  'to 188'
              170  LOAD_FAST                'ciphername'
              172  LOAD_FAST                'Transport'
              174  LOAD_ATTR                _cipher_info
              176  COMPARE_OP               not-in
              178  POP_JUMP_IF_FALSE   188  'to 188'

 L. 126       180  LOAD_GLOBAL              SSHException
              182  LOAD_STR                 'Invalid key'
              184  CALL_FUNCTION_1       1  '1 positional argument'
              186  RAISE_VARARGS_1       1  'exception instance'
            188_0  COME_FROM           178  '178'
            188_1  COME_FROM           168  '168'

 L. 128       188  BUILD_LIST_0          0 
              190  STORE_FAST               'public_keys'

 L. 129       192  SETUP_LOOP          256  'to 256'
              194  LOAD_GLOBAL              range
              196  LOAD_FAST                'num_keys'
              198  CALL_FUNCTION_1       1  '1 positional argument'
              200  GET_ITER         
            202_0  COME_FROM           252  '252'
              202  FOR_ITER            254  'to 254'
              204  STORE_FAST               '_'

 L. 130       206  LOAD_GLOBAL              Message
              208  LOAD_FAST                'message'
              210  LOAD_METHOD              get_binary
              212  CALL_METHOD_0         0  '0 positional arguments'
              214  CALL_FUNCTION_1       1  '1 positional argument'
              216  STORE_FAST               'pubkey'

 L. 131       218  LOAD_FAST                'pubkey'
              220  LOAD_METHOD              get_text
              222  CALL_METHOD_0         0  '0 positional arguments'
              224  LOAD_STR                 'ssh-ed25519'
              226  COMPARE_OP               !=
              228  POP_JUMP_IF_FALSE   238  'to 238'

 L. 132       230  LOAD_GLOBAL              SSHException
              232  LOAD_STR                 'Invalid key'
              234  CALL_FUNCTION_1       1  '1 positional argument'
              236  RAISE_VARARGS_1       1  'exception instance'
            238_0  COME_FROM           228  '228'

 L. 133       238  LOAD_FAST                'public_keys'
              240  LOAD_METHOD              append
              242  LOAD_FAST                'pubkey'
              244  LOAD_METHOD              get_binary
              246  CALL_METHOD_0         0  '0 positional arguments'
              248  CALL_METHOD_1         1  '1 positional argument'
              250  POP_TOP          
              252  JUMP_BACK           202  'to 202'
              254  POP_BLOCK        
            256_0  COME_FROM_LOOP      192  '192'

 L. 135       256  LOAD_FAST                'message'
              258  LOAD_METHOD              get_binary
              260  CALL_METHOD_0         0  '0 positional arguments'
              262  STORE_FAST               'private_ciphertext'

 L. 136       264  LOAD_FAST                'ciphername'
              266  LOAD_STR                 'none'
              268  COMPARE_OP               ==
          270_272  POP_JUMP_IF_FALSE   280  'to 280'

 L. 137       274  LOAD_FAST                'private_ciphertext'
              276  STORE_FAST               'private_data'
              278  JUMP_FORWARD        404  'to 404'
            280_0  COME_FROM           270  '270'

 L. 139       280  LOAD_FAST                'Transport'
              282  LOAD_ATTR                _cipher_info
              284  LOAD_FAST                'ciphername'
              286  BINARY_SUBSCR    
              288  STORE_FAST               'cipher'

 L. 140       290  LOAD_GLOBAL              bcrypt
              292  LOAD_ATTR                kdf

 L. 141       294  LOAD_GLOBAL              b
              296  LOAD_FAST                'password'
              298  CALL_FUNCTION_1       1  '1 positional argument'

 L. 142       300  LOAD_FAST                'bcrypt_salt'

 L. 143       302  LOAD_FAST                'cipher'
              304  LOAD_STR                 'key-size'
              306  BINARY_SUBSCR    
              308  LOAD_FAST                'cipher'
              310  LOAD_STR                 'block-size'
              312  BINARY_SUBSCR    
              314  BINARY_ADD       

 L. 144       316  LOAD_FAST                'bcrypt_rounds'

 L. 147       318  LOAD_CONST               True
              320  LOAD_CONST               ('password', 'salt', 'desired_key_bytes', 'rounds', 'ignore_few_rounds')
              322  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              324  STORE_FAST               'key'

 L. 149       326  LOAD_GLOBAL              Cipher

 L. 150       328  LOAD_FAST                'cipher'
              330  LOAD_STR                 'class'
              332  BINARY_SUBSCR    
              334  LOAD_FAST                'key'
              336  LOAD_CONST               None
              338  LOAD_FAST                'cipher'
              340  LOAD_STR                 'key-size'
              342  BINARY_SUBSCR    
              344  BUILD_SLICE_2         2 
              346  BINARY_SUBSCR    
              348  CALL_FUNCTION_1       1  '1 positional argument'

 L. 151       350  LOAD_FAST                'cipher'
              352  LOAD_STR                 'mode'
              354  BINARY_SUBSCR    
              356  LOAD_FAST                'key'
              358  LOAD_FAST                'cipher'
              360  LOAD_STR                 'key-size'
              362  BINARY_SUBSCR    
              364  LOAD_CONST               None
              366  BUILD_SLICE_2         2 
              368  BINARY_SUBSCR    
              370  CALL_FUNCTION_1       1  '1 positional argument'

 L. 152       372  LOAD_GLOBAL              default_backend
              374  CALL_FUNCTION_0       0  '0 positional arguments'
              376  LOAD_CONST               ('backend',)
              378  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              380  LOAD_METHOD              decryptor
              382  CALL_METHOD_0         0  '0 positional arguments'
              384  STORE_FAST               'decryptor'

 L. 155       386  LOAD_FAST                'decryptor'
              388  LOAD_METHOD              update
              390  LOAD_FAST                'private_ciphertext'
              392  CALL_METHOD_1         1  '1 positional argument'
              394  LOAD_FAST                'decryptor'
              396  LOAD_METHOD              finalize
              398  CALL_METHOD_0         0  '0 positional arguments'
              400  BINARY_ADD       
              402  STORE_FAST               'private_data'
            404_0  COME_FROM           278  '278'

 L. 158       404  LOAD_GLOBAL              Message
              406  LOAD_GLOBAL              unpad
              408  LOAD_FAST                'private_data'
              410  CALL_FUNCTION_1       1  '1 positional argument'
              412  CALL_FUNCTION_1       1  '1 positional argument'
              414  STORE_FAST               'message'

 L. 159       416  LOAD_FAST                'message'
              418  LOAD_METHOD              get_int
              420  CALL_METHOD_0         0  '0 positional arguments'
              422  LOAD_FAST                'message'
              424  LOAD_METHOD              get_int
              426  CALL_METHOD_0         0  '0 positional arguments'
              428  COMPARE_OP               !=
          430_432  POP_JUMP_IF_FALSE   442  'to 442'

 L. 160       434  LOAD_GLOBAL              SSHException
              436  LOAD_STR                 'Invalid key'
              438  CALL_FUNCTION_1       1  '1 positional argument'
              440  RAISE_VARARGS_1       1  'exception instance'
            442_0  COME_FROM           430  '430'

 L. 162       442  BUILD_LIST_0          0 
              444  STORE_FAST               'signing_keys'

 L. 163       446  SETUP_LOOP          602  'to 602'
              448  LOAD_GLOBAL              range
              450  LOAD_FAST                'num_keys'
              452  CALL_FUNCTION_1       1  '1 positional argument'
              454  GET_ITER         
            456_0  COME_FROM           596  '596'
              456  FOR_ITER            600  'to 600'
              458  STORE_FAST               'i'

 L. 164       460  LOAD_FAST                'message'
              462  LOAD_METHOD              get_text
              464  CALL_METHOD_0         0  '0 positional arguments'
              466  LOAD_STR                 'ssh-ed25519'
              468  COMPARE_OP               !=
          470_472  POP_JUMP_IF_FALSE   482  'to 482'

 L. 165       474  LOAD_GLOBAL              SSHException
              476  LOAD_STR                 'Invalid key'
              478  CALL_FUNCTION_1       1  '1 positional argument'
              480  RAISE_VARARGS_1       1  'exception instance'
            482_0  COME_FROM           470  '470'

 L. 167       482  LOAD_FAST                'message'
              484  LOAD_METHOD              get_binary
              486  CALL_METHOD_0         0  '0 positional arguments'
              488  STORE_FAST               'public'

 L. 168       490  LOAD_FAST                'message'
              492  LOAD_METHOD              get_binary
              494  CALL_METHOD_0         0  '0 positional arguments'
              496  STORE_FAST               'key_data'

 L. 171       498  LOAD_GLOBAL              nacl
              500  LOAD_ATTR                signing
              502  LOAD_METHOD              SigningKey
              504  LOAD_FAST                'key_data'
              506  LOAD_CONST               None
              508  LOAD_CONST               32
              510  BUILD_SLICE_2         2 
              512  BINARY_SUBSCR    
              514  CALL_METHOD_1         1  '1 positional argument'
              516  STORE_FAST               'signing_key'

 L. 174       518  LOAD_FAST                'signing_key'
              520  LOAD_ATTR                verify_key
              522  LOAD_METHOD              encode
              524  CALL_METHOD_0         0  '0 positional arguments'

 L. 175       526  LOAD_FAST                'public'
              528  DUP_TOP          
              530  ROT_THREE        
              532  COMPARE_OP               ==
          534_536  POP_JUMP_IF_FALSE   572  'to 572'

 L. 176       538  LOAD_FAST                'public_keys'
              540  LOAD_FAST                'i'
              542  BINARY_SUBSCR    
              544  DUP_TOP          
              546  ROT_THREE        
              548  COMPARE_OP               ==
          550_552  POP_JUMP_IF_FALSE   572  'to 572'

 L. 177       554  LOAD_FAST                'key_data'
              556  LOAD_CONST               32
              558  LOAD_CONST               None
              560  BUILD_SLICE_2         2 
              562  BINARY_SUBSCR    
              564  COMPARE_OP               ==
          566_568  POP_JUMP_IF_TRUE    578  'to 578'
              570  JUMP_FORWARD        574  'to 574'
            572_0  COME_FROM           550  '550'
            572_1  COME_FROM           534  '534'
              572  POP_TOP          
            574_0  COME_FROM           570  '570'
              574  LOAD_GLOBAL              AssertionError
              576  RAISE_VARARGS_1       1  'exception instance'
            578_0  COME_FROM           566  '566'

 L. 179       578  LOAD_FAST                'signing_keys'
              580  LOAD_METHOD              append
              582  LOAD_FAST                'signing_key'
              584  CALL_METHOD_1         1  '1 positional argument'
              586  POP_TOP          

 L. 181       588  LOAD_FAST                'message'
              590  LOAD_METHOD              get_binary
              592  CALL_METHOD_0         0  '0 positional arguments'
              594  POP_TOP          
          596_598  JUMP_BACK           456  'to 456'
              600  POP_BLOCK        
            602_0  COME_FROM_LOOP      446  '446'

 L. 183       602  LOAD_GLOBAL              len
              604  LOAD_FAST                'signing_keys'
              606  CALL_FUNCTION_1       1  '1 positional argument'
              608  LOAD_CONST               1
              610  COMPARE_OP               !=
          612_614  POP_JUMP_IF_FALSE   624  'to 624'

 L. 184       616  LOAD_GLOBAL              SSHException
              618  LOAD_STR                 'Invalid key'
              620  CALL_FUNCTION_1       1  '1 positional argument'
              622  RAISE_VARARGS_1       1  'exception instance'
            624_0  COME_FROM           612  '612'

 L. 185       624  LOAD_FAST                'signing_keys'
              626  LOAD_CONST               0
              628  BINARY_SUBSCR    
              630  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 572

    def asbytes(self):
        if self.can_sign():
            v = self._signing_key.verify_key
        else:
            v = self._verifying_key
        m = Message
        m.add_string('ssh-ed25519')
        m.add_string(v.encode())
        return m.asbytes()

    def __hash__(self):
        if self.can_sign():
            v = self._signing_key.verify_key
        else:
            v = self._verifying_key
        return hash((self.get_name(), v))

    def get_name(self):
        return 'ssh-ed25519'

    def get_bits(self):
        return 256

    def can_sign(self):
        return self._signing_key is not None

    def sign_ssh_data(self, data):
        m = Message
        m.add_string('ssh-ed25519')
        m.add_string(self._signing_key.sign(data).signature)
        return m

    def verify_ssh_sig(self, data, msg):
        if msg.get_text() != 'ssh-ed25519':
            return False
        try:
            self._verifying_key.verify(data, msg.get_binary())
        except nacl.exceptions.BadSignatureError:
            return False
        else:
            return True