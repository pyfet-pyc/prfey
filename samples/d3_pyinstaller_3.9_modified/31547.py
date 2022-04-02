# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\primitives\padding.py
from __future__ import absolute_import, division, print_function
import abc, six
from cryptography import utils
from cryptography.exceptions import AlreadyFinalized
from cryptography.hazmat.bindings._padding import lib

@six.add_metaclass(abc.ABCMeta)
class PaddingContext(object):

    @abc.abstractmethod
    def update(self, data):
        """
        Pads the provided bytes and returns any available data as bytes.
        """
        pass

    @abc.abstractmethod
    def finalize(self):
        """
        Finalize the padding, returns bytes.
        """
        pass


def _byte_padding_check(block_size):
    if not 0 <= block_size <= 2040:
        raise ValueError('block_size must be in range(0, 2041).')
    if block_size % 8 != 0:
        raise ValueError('block_size must be a multiple of 8.')


def _byte_padding_update--- This code section failed: ---

 L.  40         0  LOAD_FAST                'buffer_'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L.  41         8  LOAD_GLOBAL              AlreadyFinalized
               10  LOAD_STR                 'Context was already finalized.'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L.  43        16  LOAD_GLOBAL              utils
               18  LOAD_METHOD              _check_byteslike
               20  LOAD_STR                 'data'
               22  LOAD_FAST                'data'
               24  CALL_METHOD_2         2  ''
               26  POP_TOP          

 L.  48        28  LOAD_FAST                'buffer_'
               30  LOAD_GLOBAL              isinstance
               32  LOAD_FAST                'data'
               34  LOAD_GLOBAL              bytes
               36  CALL_FUNCTION_2       2  ''
               38  POP_JUMP_IF_FALSE    44  'to 44'
               40  LOAD_FAST                'data'
               42  JUMP_FORWARD         50  'to 50'
             44_0  COME_FROM            38  '38'
               44  LOAD_GLOBAL              bytes
               46  LOAD_FAST                'data'
               48  CALL_FUNCTION_1       1  ''
             50_0  COME_FROM            42  '42'
               50  INPLACE_ADD      
               52  STORE_FAST               'buffer_'

 L.  50        54  LOAD_GLOBAL              len
               56  LOAD_FAST                'buffer_'
               58  CALL_FUNCTION_1       1  ''
               60  LOAD_FAST                'block_size'
               62  LOAD_CONST               8
               64  BINARY_FLOOR_DIVIDE
               66  BINARY_FLOOR_DIVIDE
               68  STORE_FAST               'finished_blocks'

 L.  52        70  LOAD_FAST                'buffer_'
               72  LOAD_CONST               None
               74  LOAD_FAST                'finished_blocks'
               76  LOAD_FAST                'block_size'
               78  LOAD_CONST               8
               80  BINARY_FLOOR_DIVIDE
               82  BINARY_MULTIPLY  
               84  BUILD_SLICE_2         2 
               86  BINARY_SUBSCR    
               88  STORE_FAST               'result'

 L.  53        90  LOAD_FAST                'buffer_'
               92  LOAD_FAST                'finished_blocks'
               94  LOAD_FAST                'block_size'
               96  LOAD_CONST               8
               98  BINARY_FLOOR_DIVIDE
              100  BINARY_MULTIPLY  
              102  LOAD_CONST               None
              104  BUILD_SLICE_2         2 
              106  BINARY_SUBSCR    
              108  STORE_FAST               'buffer_'

 L.  55       110  LOAD_FAST                'buffer_'
              112  LOAD_FAST                'result'
              114  BUILD_TUPLE_2         2 
              116  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def _byte_padding_pad--- This code section failed: ---

 L.  59         0  LOAD_FAST                'buffer_'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L.  60         8  LOAD_GLOBAL              AlreadyFinalized
               10  LOAD_STR                 'Context was already finalized.'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L.  62        16  LOAD_FAST                'block_size'
               18  LOAD_CONST               8
               20  BINARY_FLOOR_DIVIDE
               22  LOAD_GLOBAL              len
               24  LOAD_FAST                'buffer_'
               26  CALL_FUNCTION_1       1  ''
               28  BINARY_SUBTRACT  
               30  STORE_FAST               'pad_size'

 L.  63        32  LOAD_FAST                'buffer_'
               34  LOAD_FAST                'paddingfn'
               36  LOAD_FAST                'pad_size'
               38  CALL_FUNCTION_1       1  ''
               40  BINARY_ADD       
               42  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def _byte_unpadding_update--- This code section failed: ---

 L.  67         0  LOAD_FAST                'buffer_'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L.  68         8  LOAD_GLOBAL              AlreadyFinalized
               10  LOAD_STR                 'Context was already finalized.'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L.  70        16  LOAD_GLOBAL              utils
               18  LOAD_METHOD              _check_byteslike
               20  LOAD_STR                 'data'
               22  LOAD_FAST                'data'
               24  CALL_METHOD_2         2  ''
               26  POP_TOP          

 L.  75        28  LOAD_FAST                'buffer_'
               30  LOAD_GLOBAL              isinstance
               32  LOAD_FAST                'data'
               34  LOAD_GLOBAL              bytes
               36  CALL_FUNCTION_2       2  ''
               38  POP_JUMP_IF_FALSE    44  'to 44'
               40  LOAD_FAST                'data'
               42  JUMP_FORWARD         50  'to 50'
             44_0  COME_FROM            38  '38'
               44  LOAD_GLOBAL              bytes
               46  LOAD_FAST                'data'
               48  CALL_FUNCTION_1       1  ''
             50_0  COME_FROM            42  '42'
               50  INPLACE_ADD      
               52  STORE_FAST               'buffer_'

 L.  77        54  LOAD_GLOBAL              max
               56  LOAD_GLOBAL              len
               58  LOAD_FAST                'buffer_'
               60  CALL_FUNCTION_1       1  ''
               62  LOAD_FAST                'block_size'
               64  LOAD_CONST               8
               66  BINARY_FLOOR_DIVIDE
               68  BINARY_FLOOR_DIVIDE
               70  LOAD_CONST               1
               72  BINARY_SUBTRACT  
               74  LOAD_CONST               0
               76  CALL_FUNCTION_2       2  ''
               78  STORE_FAST               'finished_blocks'

 L.  79        80  LOAD_FAST                'buffer_'
               82  LOAD_CONST               None
               84  LOAD_FAST                'finished_blocks'
               86  LOAD_FAST                'block_size'
               88  LOAD_CONST               8
               90  BINARY_FLOOR_DIVIDE
               92  BINARY_MULTIPLY  
               94  BUILD_SLICE_2         2 
               96  BINARY_SUBSCR    
               98  STORE_FAST               'result'

 L.  80       100  LOAD_FAST                'buffer_'
              102  LOAD_FAST                'finished_blocks'
              104  LOAD_FAST                'block_size'
              106  LOAD_CONST               8
              108  BINARY_FLOOR_DIVIDE
              110  BINARY_MULTIPLY  
              112  LOAD_CONST               None
              114  BUILD_SLICE_2         2 
              116  BINARY_SUBSCR    
              118  STORE_FAST               'buffer_'

 L.  82       120  LOAD_FAST                'buffer_'
              122  LOAD_FAST                'result'
              124  BUILD_TUPLE_2         2 
              126  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def _byte_unpadding_check--- This code section failed: ---

 L.  86         0  LOAD_FAST                'buffer_'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L.  87         8  LOAD_GLOBAL              AlreadyFinalized
               10  LOAD_STR                 'Context was already finalized.'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L.  89        16  LOAD_GLOBAL              len
               18  LOAD_FAST                'buffer_'
               20  CALL_FUNCTION_1       1  ''
               22  LOAD_FAST                'block_size'
               24  LOAD_CONST               8
               26  BINARY_FLOOR_DIVIDE
               28  COMPARE_OP               !=
               30  POP_JUMP_IF_FALSE    40  'to 40'

 L.  90        32  LOAD_GLOBAL              ValueError
               34  LOAD_STR                 'Invalid padding bytes.'
               36  CALL_FUNCTION_1       1  ''
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            30  '30'

 L.  92        40  LOAD_FAST                'checkfn'
               42  LOAD_FAST                'buffer_'
               44  LOAD_FAST                'block_size'
               46  LOAD_CONST               8
               48  BINARY_FLOOR_DIVIDE
               50  CALL_FUNCTION_2       2  ''
               52  STORE_FAST               'valid'

 L.  94        54  LOAD_FAST                'valid'
               56  POP_JUMP_IF_TRUE     66  'to 66'

 L.  95        58  LOAD_GLOBAL              ValueError
               60  LOAD_STR                 'Invalid padding bytes.'
               62  CALL_FUNCTION_1       1  ''
               64  RAISE_VARARGS_1       1  'exception instance'
             66_0  COME_FROM            56  '56'

 L.  97        66  LOAD_GLOBAL              six
               68  LOAD_METHOD              indexbytes
               70  LOAD_FAST                'buffer_'
               72  LOAD_CONST               -1
               74  CALL_METHOD_2         2  ''
               76  STORE_FAST               'pad_size'

 L.  98        78  LOAD_FAST                'buffer_'
               80  LOAD_CONST               None
               82  LOAD_FAST                'pad_size'
               84  UNARY_NEGATIVE   
               86  BUILD_SLICE_2         2 
               88  BINARY_SUBSCR    
               90  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class PKCS7(object):

    def __init__(self, block_size):
        _byte_padding_check(block_size)
        self.block_size = block_size

    def padder(self):
        return _PKCS7PaddingContext(self.block_size)

    def unpadder(self):
        return _PKCS7UnpaddingContext(self.block_size)


@utils.register_interface(PaddingContext)
class _PKCS7PaddingContext(object):

    def __init__(self, block_size):
        self.block_size = block_size
        self._buffer = b''

    def update(self, data):
        self._buffer, result = _byte_padding_update(self._buffer, data, self.block_size)
        return result

    def _padding(self, size):
        return six.int2byte(size) * size

    def finalize(self):
        result = _byte_padding_pad(self._buffer, self.block_size, self._padding)
        self._buffer = None
        return result


@utils.register_interface(PaddingContext)
class _PKCS7UnpaddingContext(object):

    def __init__(self, block_size):
        self.block_size = block_size
        self._buffer = b''

    def update(self, data):
        self._buffer, result = _byte_unpadding_update(self._buffer, data, self.block_size)
        return result

    def finalize(self):
        result = _byte_unpadding_check(self._buffer, self.block_size, lib.Cryptography_check_pkcs7_padding)
        self._buffer = None
        return result


class ANSIX923(object):

    def __init__(self, block_size):
        _byte_padding_check(block_size)
        self.block_size = block_size

    def padder(self):
        return _ANSIX923PaddingContext(self.block_size)

    def unpadder(self):
        return _ANSIX923UnpaddingContext(self.block_size)


@utils.register_interface(PaddingContext)
class _ANSIX923PaddingContext(object):

    def __init__(self, block_size):
        self.block_size = block_size
        self._buffer = b''

    def update(self, data):
        self._buffer, result = _byte_padding_update(self._buffer, data, self.block_size)
        return result

    def _padding(self, size):
        return six.int2byte(0) * (size - 1) + six.int2byte(size)

    def finalize(self):
        result = _byte_padding_pad(self._buffer, self.block_size, self._padding)
        self._buffer = None
        return result


@utils.register_interface(PaddingContext)
class _ANSIX923UnpaddingContext(object):

    def __init__(self, block_size):
        self.block_size = block_size
        self._buffer = b''

    def update(self, data):
        self._buffer, result = _byte_unpadding_update(self._buffer, data, self.block_size)
        return result

    def finalize(self):
        result = _byte_unpadding_check(self._buffer, self.block_size, lib.Cryptography_check_ansix923_padding)
        self._buffer = None
        return result