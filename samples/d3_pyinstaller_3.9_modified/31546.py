# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\primitives\hmac.py
from __future__ import absolute_import, division, print_function
from cryptography import utils
from cryptography.exceptions import AlreadyFinalized, UnsupportedAlgorithm, _Reasons
from cryptography.hazmat.backends import _get_backend
from cryptography.hazmat.backends.interfaces import HMACBackend
from cryptography.hazmat.primitives import hashes

@utils.register_interface(hashes.HashContext)
class HMAC(object):

    def __init__--- This code section failed: ---

 L.  21         0  LOAD_GLOBAL              _get_backend
                2  LOAD_FAST                'backend'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'backend'

 L.  22         8  LOAD_GLOBAL              isinstance
               10  LOAD_FAST                'backend'
               12  LOAD_GLOBAL              HMACBackend
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_TRUE     30  'to 30'

 L.  23        18  LOAD_GLOBAL              UnsupportedAlgorithm

 L.  24        20  LOAD_STR                 'Backend object does not implement HMACBackend.'

 L.  25        22  LOAD_GLOBAL              _Reasons
               24  LOAD_ATTR                BACKEND_MISSING_INTERFACE

 L.  23        26  CALL_FUNCTION_2       2  ''
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            16  '16'

 L.  28        30  LOAD_GLOBAL              isinstance
               32  LOAD_FAST                'algorithm'
               34  LOAD_GLOBAL              hashes
               36  LOAD_ATTR                HashAlgorithm
               38  CALL_FUNCTION_2       2  ''
               40  POP_JUMP_IF_TRUE     50  'to 50'

 L.  29        42  LOAD_GLOBAL              TypeError
               44  LOAD_STR                 'Expected instance of hashes.HashAlgorithm.'
               46  CALL_FUNCTION_1       1  ''
               48  RAISE_VARARGS_1       1  'exception instance'
             50_0  COME_FROM            40  '40'

 L.  30        50  LOAD_FAST                'algorithm'
               52  LOAD_FAST                'self'
               54  STORE_ATTR               _algorithm

 L.  32        56  LOAD_FAST                'backend'
               58  LOAD_FAST                'self'
               60  STORE_ATTR               _backend

 L.  33        62  LOAD_FAST                'key'
               64  LOAD_FAST                'self'
               66  STORE_ATTR               _key

 L.  34        68  LOAD_FAST                'ctx'
               70  LOAD_CONST               None
               72  <117>                 0  ''
               74  POP_JUMP_IF_FALSE    96  'to 96'

 L.  35        76  LOAD_FAST                'self'
               78  LOAD_ATTR                _backend
               80  LOAD_METHOD              create_hmac_ctx
               82  LOAD_FAST                'key'
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                algorithm
               88  CALL_METHOD_2         2  ''
               90  LOAD_FAST                'self'
               92  STORE_ATTR               _ctx
               94  JUMP_FORWARD        102  'to 102'
             96_0  COME_FROM            74  '74'

 L.  37        96  LOAD_FAST                'ctx'
               98  LOAD_FAST                'self'
              100  STORE_ATTR               _ctx
            102_0  COME_FROM            94  '94'

Parse error at or near `<117>' instruction at offset 72

    algorithm = utils.read_only_property('_algorithm')

    def update--- This code section failed: ---

 L.  42         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _ctx
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L.  43        10  LOAD_GLOBAL              AlreadyFinalized
               12  LOAD_STR                 'Context was already finalized.'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L.  44        18  LOAD_GLOBAL              utils
               20  LOAD_METHOD              _check_byteslike
               22  LOAD_STR                 'data'
               24  LOAD_FAST                'data'
               26  CALL_METHOD_2         2  ''
               28  POP_TOP          

 L.  45        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _ctx
               34  LOAD_METHOD              update
               36  LOAD_FAST                'data'
               38  CALL_METHOD_1         1  ''
               40  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def copy--- This code section failed: ---

 L.  48         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _ctx
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L.  49        10  LOAD_GLOBAL              AlreadyFinalized
               12  LOAD_STR                 'Context was already finalized.'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L.  50        18  LOAD_GLOBAL              HMAC

 L.  51        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _key

 L.  52        24  LOAD_FAST                'self'
               26  LOAD_ATTR                algorithm

 L.  53        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _backend

 L.  54        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _ctx
               36  LOAD_METHOD              copy
               38  CALL_METHOD_0         0  ''

 L.  50        40  LOAD_CONST               ('backend', 'ctx')
               42  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               44  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def finalize--- This code section failed: ---

 L.  58         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _ctx
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L.  59        10  LOAD_GLOBAL              AlreadyFinalized
               12  LOAD_STR                 'Context was already finalized.'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L.  60        18  LOAD_FAST                'self'
               20  LOAD_ATTR                _ctx
               22  LOAD_METHOD              finalize
               24  CALL_METHOD_0         0  ''
               26  STORE_FAST               'digest'

 L.  61        28  LOAD_CONST               None
               30  LOAD_FAST                'self'
               32  STORE_ATTR               _ctx

 L.  62        34  LOAD_FAST                'digest'
               36  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def verify--- This code section failed: ---

 L.  65         0  LOAD_GLOBAL              utils
                2  LOAD_METHOD              _check_bytes
                4  LOAD_STR                 'signature'
                6  LOAD_FAST                'signature'
                8  CALL_METHOD_2         2  ''
               10  POP_TOP          

 L.  66        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _ctx
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_FALSE    30  'to 30'

 L.  67        22  LOAD_GLOBAL              AlreadyFinalized
               24  LOAD_STR                 'Context was already finalized.'
               26  CALL_FUNCTION_1       1  ''
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            20  '20'

 L.  69        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _ctx
               34  LOAD_CONST               None
               36  ROT_TWO          
               38  STORE_FAST               'ctx'
               40  LOAD_FAST                'self'
               42  STORE_ATTR               _ctx

 L.  70        44  LOAD_FAST                'ctx'
               46  LOAD_METHOD              verify
               48  LOAD_FAST                'signature'
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          

Parse error at or near `<117>' instruction at offset 18