# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\_binary.py
"""Binary input/output support routines."""
from struct import pack, unpack_from

def i8--- This code section failed: ---

 L.  22         0  LOAD_FAST                'c'
                2  LOAD_ATTR                __class__
                4  LOAD_GLOBAL              int
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'
               10  LOAD_FAST                'c'
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'
               14  LOAD_FAST                'c'
               16  LOAD_CONST               0
               18  BINARY_SUBSCR    
               20  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def o8(i):
    return bytes((i & 255,))


def i16le(c, o=0):
    """
    Converts a 2-bytes (16 bits) string to an unsigned integer.

    :param c: string containing bytes to convert
    :param o: offset of bytes to convert in string
    """
    return unpack_from('<H', c, o)[0]


def si16le(c, o=0):
    """
    Converts a 2-bytes (16 bits) string to a signed integer.

    :param c: string containing bytes to convert
    :param o: offset of bytes to convert in string
    """
    return unpack_from('<h', c, o)[0]


def i32le(c, o=0):
    """
    Converts a 4-bytes (32 bits) string to an unsigned integer.

    :param c: string containing bytes to convert
    :param o: offset of bytes to convert in string
    """
    return unpack_from('<I', c, o)[0]


def si32le(c, o=0):
    """
    Converts a 4-bytes (32 bits) string to a signed integer.

    :param c: string containing bytes to convert
    :param o: offset of bytes to convert in string
    """
    return unpack_from('<i', c, o)[0]


def i16be(c, o=0):
    return unpack_from('>H', c, o)[0]


def i32be(c, o=0):
    return unpack_from('>I', c, o)[0]


def o16le(i):
    return pack('<H', i)


def o32le(i):
    return pack('<I', i)


def o16be(i):
    return pack('>H', i)


def o32be(i):
    return pack('>I', i)