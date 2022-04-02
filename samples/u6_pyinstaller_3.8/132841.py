# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: cryptography\hazmat\_der.py
import typing
from cryptography.utils import int_to_bytes
CONSTRUCTED = 32
CONTEXT_SPECIFIC = 128
INTEGER = 2
BIT_STRING = 3
OCTET_STRING = 4
NULL = 5
OBJECT_IDENTIFIER = 6
SEQUENCE = 16 | CONSTRUCTED
SET = 17 | CONSTRUCTED
PRINTABLE_STRING = 19
UTC_TIME = 23
GENERALIZED_TIME = 24

class DERReader(object):

    def __init__(self, data):
        self.data = memoryview(data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_value is None:
            self.check_empty()

    def is_empty(self):
        return len(self.data) == 0

    def check_empty(self):
        if not self.is_empty():
            raise ValueError('Invalid DER input: trailing data')

    def read_byte(self) -> int:
        if len(self.data) < 1:
            raise ValueError('Invalid DER input: insufficient data')
        ret = self.data[0]
        self.data = self.data[1:]
        return ret

    def read_bytes(self, n) -> memoryview:
        if len(self.data) < n:
            raise ValueError('Invalid DER input: insufficient data')
        ret = self.data[:n]
        self.data = self.data[n:]
        return ret

    def read_any_element(self) -> typing.Tuple[(int, 'DERReader')]:
        tag = self.read_byte()
        if tag & 31 == 31:
            raise ValueError('Invalid DER input: unexpected high tag number')
        else:
            length_byte = self.read_byte()
            if length_byte & 128 == 0:
                length = length_byte
            else:
                length_byte &= 127
                if length_byte == 0:
                    raise ValueError('Invalid DER input: indefinite length form is not allowed in DER')
            length = 0
            for i in range(length_byte):
                length <<= 8
                length |= self.read_byte()
                if length == 0:
                    raise ValueError('Invalid DER input: length was not minimally-encoded')
            else:
                if length < 128:
                    raise ValueError('Invalid DER input: length was not minimally-encoded')

        body = self.read_bytes(length)
        return (tag, DERReader(body))

    def read_element(self, expected_tag: int) -> 'DERReader':
        tag, body = self.read_any_element()
        if tag != expected_tag:
            raise ValueError('Invalid DER input: unexpected tag')
        return body

    def read_single_element--- This code section failed: ---

 L. 108         0  LOAD_FAST                'self'
                2  SETUP_WITH           28  'to 28'
                4  POP_TOP          

 L. 109         6  LOAD_FAST                'self'
                8  LOAD_METHOD              read_element
               10  LOAD_FAST                'expected_tag'
               12  CALL_METHOD_1         1  ''
               14  POP_BLOCK        
               16  ROT_TWO          
               18  BEGIN_FINALLY    
               20  WITH_CLEANUP_START
               22  WITH_CLEANUP_FINISH
               24  POP_FINALLY           0  ''
               26  RETURN_VALUE     
             28_0  COME_FROM_WITH        2  '2'
               28  WITH_CLEANUP_START
               30  WITH_CLEANUP_FINISH
               32  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 16

    def read_optional_element(self, expected_tag: int) -> typing.Optional['DERReader']:
        if len(self.data) > 0:
            if self.data[0] == expected_tag:
                return self.read_element(expected_tag)

    def as_integer(self) -> int:
        if len(self.data) == 0:
            raise ValueError('Invalid DER input: empty integer contents')
        else:
            first = self.data[0]
            if first & 128 == 128:
                raise ValueError('Negative DER integers are not supported')
            if len(self.data) > 1:
                second = self.data[1]
                if first == 0:
                    if second & 128 == 0:
                        raise ValueError('Invalid DER input: integer not minimally-encoded')
        return int.from_bytes(self.data, 'big')


def encode_der_integer(x: int) -> bytes:
    if not isinstance(x, int):
        raise ValueError('Value must be an integer')
    if x < 0:
        raise ValueError('Negative integers are not supported')
    n = x.bit_length() // 8 + 1
    return int_to_bytes(x, n)


def encode_der(tag: int, *children: bytes) -> bytes:
    length = 0
    for child in children:
        length += len(child)
    else:
        chunks = [
         bytes([tag])]
        if length < 128:
            chunks.append(bytes([length]))
        else:
            length_bytes = int_to_bytes(length)
            chunks.append(bytes([128 | len(length_bytes)]))
            chunks.append(length_bytes)
        chunks.extend(children)
        return (b'').join(chunks)