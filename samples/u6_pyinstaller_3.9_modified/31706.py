# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: pyasn1\error.py


class PyAsn1Error(Exception):
    __doc__ = 'Base pyasn1 exception\n\n    `PyAsn1Error` is the base exception class (based on\n    :class:`Exception`) that represents all possible ASN.1 related\n    errors.\n    '


class ValueConstraintError(PyAsn1Error):
    __doc__ = 'ASN.1 type constraints violation exception\n\n    The `ValueConstraintError` exception indicates an ASN.1 value\n    constraint violation.\n\n    It might happen on value object instantiation (for scalar types) or on\n    serialization (for constructed types).\n    '


class SubstrateUnderrunError(PyAsn1Error):
    __doc__ = 'ASN.1 data structure deserialization error\n\n    The `SubstrateUnderrunError` exception indicates insufficient serialised\n    data on input of a de-serialization codec.\n    '


class PyAsn1UnicodeError(PyAsn1Error, UnicodeError):
    __doc__ = 'Unicode text processing error\n\n    The `PyAsn1UnicodeError` exception is a base class for errors relating to\n    unicode text de/serialization.\n\n    Apart from inheriting from :class:`PyAsn1Error`, it also inherits from\n    :class:`UnicodeError` to help the caller catching unicode-related errors.\n    '

    def __init__--- This code section failed: ---

 L.  47         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'unicode_error'
                4  LOAD_GLOBAL              UnicodeError
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    30  'to 30'

 L.  48        10  LOAD_GLOBAL              UnicodeError
               12  LOAD_ATTR                __init__
               14  LOAD_FAST                'self'
               16  BUILD_LIST_1          1 
               18  LOAD_FAST                'unicode_error'
               20  LOAD_ATTR                args
               22  CALL_FINALLY         25  'to 25'
               24  WITH_CLEANUP_FINISH
               26  CALL_FUNCTION_EX      0  'positional arguments only'
               28  POP_TOP          
             30_0  COME_FROM             8  '8'

 L.  49        30  LOAD_GLOBAL              PyAsn1Error
               32  LOAD_METHOD              __init__
               34  LOAD_FAST                'self'
               36  LOAD_FAST                'message'
               38  CALL_METHOD_2         2  ''
               40  POP_TOP          

Parse error at or near `CALL_FINALLY' instruction at offset 22


class PyAsn1UnicodeDecodeError(PyAsn1UnicodeError, UnicodeDecodeError):
    __doc__ = 'Unicode text decoding error\n\n    The `PyAsn1UnicodeDecodeError` exception represents a failure to\n    deserialize unicode text.\n\n    Apart from inheriting from :class:`PyAsn1UnicodeError`, it also inherits\n    from :class:`UnicodeDecodeError` to help the caller catching unicode-related\n    errors.\n    '


class PyAsn1UnicodeEncodeError(PyAsn1UnicodeError, UnicodeEncodeError):
    __doc__ = 'Unicode text encoding error\n\n    The `PyAsn1UnicodeEncodeError` exception represents a failure to\n    serialize unicode text.\n\n    Apart from inheriting from :class:`PyAsn1UnicodeError`, it also inherits\n    from :class:`UnicodeEncodeError` to help the caller catching\n    unicode-related errors.\n    '