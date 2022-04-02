# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: jeepney\low_level.py
from collections import deque
from enum import Enum, IntEnum, IntFlag
import struct
from typing import Optional

class SizeLimitError(ValueError):
    __doc__ = "Raised when trying to (de-)serialise data exceeding D-Bus' size limit.\n\n    This is currently only implemented for arrays, where the maximum size is\n    64 MiB.\n    "


class Endianness(Enum):
    little = 1
    big = 2

    def struct_code--- This code section failed: ---

 L.  19         0  LOAD_FAST                'self'
                2  LOAD_GLOBAL              Endianness
                4  LOAD_ATTR                little
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'
               10  LOAD_STR                 '<'
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'
               14  LOAD_STR                 '>'
               16  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def dbus_code--- This code section failed: ---

 L.  22         0  LOAD_FAST                'self'
                2  LOAD_GLOBAL              Endianness
                4  LOAD_ATTR                little
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'
               10  LOAD_CONST               b'l'
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'
               14  LOAD_CONST               b'B'
               16  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


endian_map = {b'l':Endianness.little, 
 b'B':Endianness.big}

class MessageType(Enum):
    method_call = 1
    method_return = 2
    error = 3
    signal = 4


class MessageFlag(IntFlag):
    no_reply_expected = 1
    no_auto_start = 2
    allow_interactive_authorization = 4


class HeaderFields(IntEnum):
    path = 1
    interface = 2
    member = 3
    error_name = 4
    reply_serial = 5
    destination = 6
    sender = 7
    signature = 8
    unix_fds = 9


def padding(pos, step):
    pad = step - pos % step
    if pad == step:
        return 0
    return pad


class FixedType:

    def __init__(self, size, struct_code):
        self.size = self.alignment = size
        self.struct_code = struct_code

    def parse_data(self, buf, pos, endianness):
        pos += padding(pos, self.alignment)
        code = endianness.struct_code() + self.struct_code
        val = struct.unpack(code, buf[pos:pos + self.size])[0]
        return (
         val, pos + self.size)

    def serialise(self, data, pos, endianness):
        pad = b'\x00' * padding(pos, self.alignment)
        code = endianness.struct_code() + self.struct_code
        return pad + struct.pack(code, data)

    def __repr__(self):
        return 'FixedType({!r}, {!r})'.format(self.size, self.struct_code)

    def __eq__--- This code section failed: ---

 L.  80         0  LOAD_GLOBAL              type
                2  LOAD_FAST                'other'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_GLOBAL              FixedType
                8  <117>                 0  ''
               10  JUMP_IF_FALSE_OR_POP    34  'to 34'
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                size
               16  LOAD_FAST                'other'
               18  LOAD_ATTR                size
               20  COMPARE_OP               ==
               22  JUMP_IF_FALSE_OR_POP    34  'to 34'

 L.  81        24  LOAD_FAST                'self'
               26  LOAD_ATTR                struct_code
               28  LOAD_FAST                'other'
               30  LOAD_ATTR                struct_code
               32  COMPARE_OP               ==
             34_0  COME_FROM            22  '22'
             34_1  COME_FROM            10  '10'

 L.  80        34  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class Boolean(FixedType):

    def __init__(self):
        super().__init__(4, 'I')

    def parse_data(self, buf, pos, endianness):
        val, new_pos = super().parse_data(buf, pos, endianness)
        return (
         bool(val), new_pos)

    def __repr__(self):
        return 'Boolean()'

    def __eq__--- This code section failed: ---

 L.  96         0  LOAD_GLOBAL              type
                2  LOAD_FAST                'other'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_GLOBAL              Boolean
                8  <117>                 0  ''
               10  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


simple_types = {'y':FixedType(1, 'B'), 
 'n':FixedType(2, 'h'), 
 'q':FixedType(2, 'H'), 
 'b':Boolean(), 
 'i':FixedType(4, 'i'), 
 'u':FixedType(4, 'I'), 
 'x':FixedType(8, 'q'), 
 't':FixedType(8, 'Q'), 
 'd':FixedType(8, 'd'), 
 'h':FixedType(8, 'I')}

class StringType:

    def __init__(self, length_type):
        self.length_type = length_type

    @property
    def alignment(self):
        return self.length_type.size

    def parse_data--- This code section failed: ---

 L. 122         0  LOAD_FAST                'self'
                2  LOAD_ATTR                length_type
                4  LOAD_METHOD              parse_data
                6  LOAD_FAST                'buf'
                8  LOAD_FAST                'pos'
               10  LOAD_FAST                'endianness'
               12  CALL_METHOD_3         3  ''
               14  UNPACK_SEQUENCE_2     2 
               16  STORE_FAST               'length'
               18  STORE_FAST               'pos'

 L. 123        20  LOAD_FAST                'pos'
               22  LOAD_FAST                'length'
               24  BINARY_ADD       
               26  STORE_FAST               'end'

 L. 124        28  LOAD_FAST                'buf'
               30  LOAD_FAST                'pos'
               32  LOAD_FAST                'end'
               34  BUILD_SLICE_2         2 
               36  BINARY_SUBSCR    
               38  LOAD_METHOD              decode
               40  LOAD_STR                 'utf-8'
               42  CALL_METHOD_1         1  ''
               44  STORE_FAST               'val'

 L. 125        46  LOAD_FAST                'buf'
               48  LOAD_FAST                'end'
               50  LOAD_FAST                'end'
               52  LOAD_CONST               1
               54  BINARY_ADD       
               56  BUILD_SLICE_2         2 
               58  BINARY_SUBSCR    
               60  LOAD_CONST               b'\x00'
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_TRUE     70  'to 70'
               66  <74>             
               68  RAISE_VARARGS_1       1  'exception instance'
             70_0  COME_FROM            64  '64'

 L. 126        70  LOAD_FAST                'val'
               72  LOAD_FAST                'end'
               74  LOAD_CONST               1
               76  BINARY_ADD       
               78  BUILD_TUPLE_2         2 
               80  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 66

    def serialise(self, data, pos, endianness):
        if not isinstance(data, str):
            raise TypeError('Expected str, not {!r}'.format(data))
        encoded = data.encode('utf-8')
        len_data = self.length_type.serialise(len(encoded), pos, endianness)
        return len_data + encoded + b'\x00'

    def __repr__(self):
        return 'StringType({!r})'.format(self.length_type)

    def __eq__--- This code section failed: ---

 L. 139         0  LOAD_GLOBAL              type
                2  LOAD_FAST                'other'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_GLOBAL              StringType
                8  <117>                 0  ''
               10  JUMP_IF_FALSE_OR_POP    22  'to 22'

 L. 140        12  LOAD_FAST                'self'
               14  LOAD_ATTR                length_type
               16  LOAD_FAST                'other'
               18  LOAD_ATTR                length_type
               20  COMPARE_OP               ==
             22_0  COME_FROM            10  '10'

 L. 139        22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


simple_types.update({'s':StringType(simple_types['u']), 
 'o':StringType(simple_types['u']), 
 'g':StringType(simple_types['y'])})

class Struct:
    alignment = 8

    def __init__(self, fields):
        if any((isinstance(f, DictEntry) for f in fields)):
            raise TypeError('Found dict entry outside array')
        self.fields = fields

    def parse_data(self, buf, pos, endianness):
        pos += padding(pos, 8)
        res = []
        for field in self.fields:
            v, pos = field.parse_data(buf, pos, endianness)
            res.append(v)
        else:
            return (
             tuple(res), pos)

    def serialise(self, data, pos, endianness):
        if not isinstance(data, tuple):
            raise TypeError('Expected tuple, not {!r}'.format(data))
        if len(data) != len(self.fields):
            raise ValueError('{} entries for {} fields'.format(len(data), len(self.fields)))
        pad = b'\x00' * padding(pos, self.alignment)
        pos += len(pad)
        res_pieces = []
        for item, field in zip(data, self.fields):
            res_pieces.append(field.serialise(item, pos, endianness))
            pos += len(res_pieces[(-1)])
        else:
            return pad + (b'').join(res_pieces)

    def __repr__(self):
        return '{}({!r})'.format(type(self).__name__, self.fields)

    def __eq__--- This code section failed: ---

 L. 185         0  LOAD_GLOBAL              type
                2  LOAD_FAST                'other'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_GLOBAL              type
                8  LOAD_FAST                'self'
               10  CALL_FUNCTION_1       1  ''
               12  <117>                 0  ''
               14  JUMP_IF_FALSE_OR_POP    26  'to 26'
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                fields
               20  LOAD_FAST                'other'
               22  LOAD_ATTR                fields
               24  COMPARE_OP               ==
             26_0  COME_FROM            14  '14'
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class DictEntry(Struct):

    def __init__(self, fields):
        if len(fields) != 2:
            raise TypeError('Dict entry must have 2 fields, not %d' % len(fields))
        if not isinstance(fields[0], (FixedType, StringType)):
            raise TypeError('First field in dict entry must be simple type, not {}'.format(type(fields[0])))
        super().__init__(fields)


class Array:
    alignment = 4
    length_type = FixedType(4, 'I')

    def __init__(self, elt_type):
        self.elt_type = elt_type

    def parse_data(self, buf, pos, endianness):
        length, pos = self.length_type.parse_data(buf, pos, endianness)
        pos += padding(pos, self.elt_type.alignment)
        end = pos + length
        res = []
        while True:
            if pos < end:
                v, pos = self.elt_type.parse_data(buf, pos, endianness)
                res.append(v)

        if isinstance(self.elt_type, DictEntry):
            res = dict(res)
        return (res, pos)

    def serialise(self, data, pos, endianness):
        if isinstance(self.elt_type, DictEntry) and isinstance(data, dict):
            data = data.items()
        else:
            pass
        if self.elt_type == simple_types['y'] and isinstance(data, bytes):
            pass
        else:
            if not isinstance(data, list):
                raise TypeError('Not suitable for array: {!r}'.format(data))
            if isinstance(self.elt_type, FixedType):
                if self.elt_type.size * len(data) > 67108864:
                    raise SizeLimitError('Array size exceeds 64 MiB limit')
            pad1 = padding(pos, self.alignment)
            pos_after_length = pos + pad1 + 4
            pad2 = padding(pos_after_length, self.elt_type.alignment)
            data_pos = pos_after_length + pad2
            limit_pos = data_pos + 67108864
            chunks = []
            for item in data:
                chunks.append(self.elt_type.serialise(item, data_pos, endianness))
                data_pos += len(chunks[(-1)])
                if data_pos > limit_pos:
                    raise SizeLimitError('Array size exceeds 64 MiB limit')
            else:
                buf = (b'').join(chunks)
                len_data = self.length_type.serialise(len(buf), pos + pad1, endianness)
                pos += len(len_data)
                return b'\x00' * pad1 + len_data + b'\x00' * pad2 + buf

    def __repr__(self):
        return 'Array({!r})'.format(self.elt_type)

    def __eq__--- This code section failed: ---

 L. 256         0  LOAD_GLOBAL              type
                2  LOAD_FAST                'other'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_GLOBAL              Array
                8  <117>                 0  ''
               10  JUMP_IF_FALSE_OR_POP    22  'to 22'
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                elt_type
               16  LOAD_FAST                'other'
               18  LOAD_ATTR                elt_type
               20  COMPARE_OP               ==
             22_0  COME_FROM            10  '10'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class Variant:
    alignment = 1

    def parse_data(self, buf, pos, endianness):
        sig, pos = simple_types['g'].parse_data(buf, pos, endianness)
        valtype = parse_signature(list(sig))
        val, pos = valtype.parse_data(buf, pos, endianness)
        return (
         (
          sig, val), pos)

    def serialise(self, data, pos, endianness):
        sig, data = data
        valtype = parse_signature(list(sig))
        sig_buf = simple_types['g'].serialise(sig, pos, endianness)
        return sig_buf + valtype.serialise(data, pos + len(sig_buf), endianness)

    def __repr__(self):
        return 'Variant()'

    def __eq__--- This code section failed: ---

 L. 281         0  LOAD_GLOBAL              type
                2  LOAD_FAST                'other'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_GLOBAL              Variant
                8  <117>                 0  ''
               10  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def parse_signature--- This code section failed: ---

 L. 287         0  LOAD_FAST                'sig'
                2  LOAD_METHOD              pop
                4  LOAD_CONST               0
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'token'

 L. 288        10  LOAD_FAST                'token'
               12  LOAD_STR                 'a'
               14  COMPARE_OP               ==
               16  POP_JUMP_IF_FALSE    30  'to 30'

 L. 289        18  LOAD_GLOBAL              Array
               20  LOAD_GLOBAL              parse_signature
               22  LOAD_FAST                'sig'
               24  CALL_FUNCTION_1       1  ''
               26  CALL_FUNCTION_1       1  ''
               28  RETURN_VALUE     
             30_0  COME_FROM            16  '16'

 L. 290        30  LOAD_FAST                'token'
               32  LOAD_STR                 'v'
               34  COMPARE_OP               ==
               36  POP_JUMP_IF_FALSE    44  'to 44'

 L. 291        38  LOAD_GLOBAL              Variant
               40  CALL_FUNCTION_0       0  ''
               42  RETURN_VALUE     
             44_0  COME_FROM            36  '36'

 L. 292        44  LOAD_FAST                'token'
               46  LOAD_STR                 '('
               48  COMPARE_OP               ==
               50  POP_JUMP_IF_FALSE   102  'to 102'

 L. 293        52  BUILD_LIST_0          0 
               54  STORE_FAST               'fields'
             56_0  COME_FROM            82  '82'

 L. 294        56  LOAD_FAST                'sig'
               58  LOAD_CONST               0
               60  BINARY_SUBSCR    
               62  LOAD_STR                 ')'
               64  COMPARE_OP               !=
               66  POP_JUMP_IF_FALSE    84  'to 84'

 L. 295        68  LOAD_FAST                'fields'
               70  LOAD_METHOD              append
               72  LOAD_GLOBAL              parse_signature
               74  LOAD_FAST                'sig'
               76  CALL_FUNCTION_1       1  ''
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          
               82  JUMP_BACK            56  'to 56'
             84_0  COME_FROM            66  '66'

 L. 296        84  LOAD_FAST                'sig'
               86  LOAD_METHOD              pop
               88  LOAD_CONST               0
               90  CALL_METHOD_1         1  ''
               92  POP_TOP          

 L. 297        94  LOAD_GLOBAL              Struct
               96  LOAD_FAST                'fields'
               98  CALL_FUNCTION_1       1  ''
              100  RETURN_VALUE     
            102_0  COME_FROM            50  '50'

 L. 298       102  LOAD_FAST                'token'
              104  LOAD_STR                 '{'
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_FALSE   160  'to 160'

 L. 299       110  BUILD_LIST_0          0 
              112  STORE_FAST               'de'
            114_0  COME_FROM           140  '140'

 L. 300       114  LOAD_FAST                'sig'
              116  LOAD_CONST               0
              118  BINARY_SUBSCR    
              120  LOAD_STR                 '}'
              122  COMPARE_OP               !=
              124  POP_JUMP_IF_FALSE   142  'to 142'

 L. 301       126  LOAD_FAST                'de'
              128  LOAD_METHOD              append
              130  LOAD_GLOBAL              parse_signature
              132  LOAD_FAST                'sig'
              134  CALL_FUNCTION_1       1  ''
              136  CALL_METHOD_1         1  ''
              138  POP_TOP          
              140  JUMP_BACK           114  'to 114'
            142_0  COME_FROM           124  '124'

 L. 302       142  LOAD_FAST                'sig'
              144  LOAD_METHOD              pop
              146  LOAD_CONST               0
              148  CALL_METHOD_1         1  ''
              150  POP_TOP          

 L. 303       152  LOAD_GLOBAL              DictEntry
              154  LOAD_FAST                'de'
              156  CALL_FUNCTION_1       1  ''
              158  RETURN_VALUE     
            160_0  COME_FROM           108  '108'

 L. 304       160  LOAD_FAST                'token'
              162  LOAD_STR                 ')}'
              164  <118>                 0  ''
              166  POP_JUMP_IF_FALSE   178  'to 178'

 L. 305       168  LOAD_GLOBAL              ValueError
              170  LOAD_STR                 'Unexpected end of struct'
              172  CALL_FUNCTION_1       1  ''
              174  RAISE_VARARGS_1       1  'exception instance'
              176  JUMP_FORWARD        186  'to 186'
            178_0  COME_FROM           166  '166'

 L. 307       178  LOAD_GLOBAL              simple_types
              180  LOAD_FAST                'token'
              182  BINARY_SUBSCR    
              184  RETURN_VALUE     
            186_0  COME_FROM           176  '176'

Parse error at or near `<118>' instruction at offset 164


def calc_msg_size(buf):
    endian, = struct.unpack('c', buf[:1])
    endian = endian_map[endian]
    body_length, = struct.unpack(endian.struct_code() + 'I', buf[4:8])
    fields_array_len, = struct.unpack(endian.struct_code() + 'I', buf[12:16])
    header_len = 16 + fields_array_len
    return header_len + padding(header_len, 8) + body_length


_header_fields_type = Array(Struct([simple_types['y'], Variant()]))

def parse_header_fields(buf, endianness):
    l, pos = _header_fields_type.parse_data(buf, 12, endianness)
    return ({v[1]:HeaderFields(k) for k, v in l}, pos)


header_field_codes = {1:'o', 
 2:'s', 
 3:'s', 
 4:'s', 
 5:'u', 
 6:'s', 
 7:'s', 
 8:'g', 
 9:'u'}

def serialise_header_fields(d, endianness):
    l = [(i.value, (header_field_codes[i], v)) for i, v in sorted(d.items())]
    return _header_fields_type.serialise(l, 12, endianness)


class Header:

    def __init__(self, endianness, message_type, flags, protocol_version, body_length, serial, fields):
        """A D-Bus message header

        It's not normally necessary to construct this directly: use higher level
        functions and methods instead.
        """
        self.endianness = endianness
        self.message_type = MessageType(message_type)
        self.flags = MessageFlag(flags)
        self.protocol_version = protocol_version
        self.body_length = body_length
        self.serial = serial
        self.fields = fields

    def __repr__(self):
        return 'Header({!r}, {!r}, {!r}, {!r}, {!r}, {!r}, fields={!r})'.format(self.endianness, self.message_type, self.flags, self.protocol_version, self.body_length, self.serial, self.fields)

    def serialise--- This code section failed: ---

 L. 367         0  LOAD_FAST                'self'
                2  LOAD_ATTR                endianness
                4  LOAD_METHOD              struct_code
                6  CALL_METHOD_0         0  ''
                8  LOAD_STR                 'cBBBII'
               10  BINARY_ADD       
               12  STORE_FAST               's'

 L. 368        14  LOAD_FAST                'serial'
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_FALSE    28  'to 28'

 L. 369        22  LOAD_FAST                'self'
               24  LOAD_ATTR                serial
               26  STORE_FAST               'serial'
             28_0  COME_FROM            20  '20'

 L. 370        28  LOAD_GLOBAL              struct
               30  LOAD_METHOD              pack
               32  LOAD_FAST                's'
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                endianness
               38  LOAD_METHOD              dbus_code
               40  CALL_METHOD_0         0  ''

 L. 371        42  LOAD_FAST                'self'
               44  LOAD_ATTR                message_type
               46  LOAD_ATTR                value
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                flags

 L. 372        52  LOAD_FAST                'self'
               54  LOAD_ATTR                protocol_version

 L. 373        56  LOAD_FAST                'self'
               58  LOAD_ATTR                body_length
               60  LOAD_FAST                'serial'

 L. 370        62  CALL_METHOD_7         7  ''

 L. 374        64  LOAD_GLOBAL              serialise_header_fields
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                fields
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                endianness
               74  CALL_FUNCTION_2       2  ''

 L. 370        76  BINARY_ADD       
               78  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 18

    @classmethod
    def from_buffer(cls, buf):
        endian, msgtype, flags, pv = struct.unpack('cBBB', buf[:4])
        endian = endian_map[endian]
        bodylen, serial = struct.unpack(endian.struct_code() + 'II', buf[4:12])
        fields, pos = parse_header_fields(buf, endian)
        return (
         cls(endian, msgtype, flags, pv, bodylen, serial, fields), pos)


class Message:
    __doc__ = "Object representing a DBus message.\n\n    It's not normally necessary to construct this directly: use higher level\n    functions and methods instead.\n    "

    def __init__(self, header, body):
        self.header = header
        self.body = body

    def __repr__(self):
        return '{}({!r}, {!r})'.format(type(self).__name__, self.header, self.body)

    @classmethod
    def from_buffer--- This code section failed: ---

 L. 400         0  LOAD_GLOBAL              Header
                2  LOAD_METHOD              from_buffer
                4  LOAD_FAST                'buf'
                6  CALL_METHOD_1         1  ''
                8  UNPACK_SEQUENCE_2     2 
               10  STORE_FAST               'header'
               12  STORE_FAST               'pos'

 L. 401        14  LOAD_CONST               ()
               16  STORE_FAST               'body'

 L. 402        18  LOAD_GLOBAL              HeaderFields
               20  LOAD_ATTR                signature
               22  LOAD_FAST                'header'
               24  LOAD_ATTR                fields
               26  <118>                 0  ''
               28  POP_JUMP_IF_FALSE    78  'to 78'

 L. 403        30  LOAD_FAST                'header'
               32  LOAD_ATTR                fields
               34  LOAD_GLOBAL              HeaderFields
               36  LOAD_ATTR                signature
               38  BINARY_SUBSCR    
               40  STORE_FAST               'sig'

 L. 404        42  LOAD_GLOBAL              parse_signature
               44  LOAD_GLOBAL              list
               46  LOAD_STR                 '(%s)'
               48  LOAD_FAST                'sig'
               50  BINARY_MODULO    
               52  CALL_FUNCTION_1       1  ''
               54  CALL_FUNCTION_1       1  ''
               56  STORE_FAST               'body_type'

 L. 405        58  LOAD_FAST                'body_type'
               60  LOAD_METHOD              parse_data
               62  LOAD_FAST                'buf'
               64  LOAD_FAST                'pos'
               66  LOAD_FAST                'header'
               68  LOAD_ATTR                endianness
               70  CALL_METHOD_3         3  ''
               72  LOAD_CONST               0
               74  BINARY_SUBSCR    
               76  STORE_FAST               'body'
             78_0  COME_FROM            28  '28'

 L. 406        78  LOAD_FAST                'cls'
               80  LOAD_FAST                'header'
               82  LOAD_FAST                'body'
               84  CALL_FUNCTION_2       2  ''
               86  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 26

    def serialise--- This code section failed: ---

 L. 414         0  LOAD_FAST                'self'
                2  LOAD_ATTR                header
                4  LOAD_ATTR                endianness
                6  STORE_FAST               'endian'

 L. 416         8  LOAD_GLOBAL              HeaderFields
               10  LOAD_ATTR                signature
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                header
               16  LOAD_ATTR                fields
               18  <118>                 0  ''
               20  POP_JUMP_IF_FALSE    70  'to 70'

 L. 417        22  LOAD_FAST                'self'
               24  LOAD_ATTR                header
               26  LOAD_ATTR                fields
               28  LOAD_GLOBAL              HeaderFields
               30  LOAD_ATTR                signature
               32  BINARY_SUBSCR    
               34  STORE_FAST               'sig'

 L. 418        36  LOAD_GLOBAL              parse_signature
               38  LOAD_GLOBAL              list
               40  LOAD_STR                 '(%s)'
               42  LOAD_FAST                'sig'
               44  BINARY_MODULO    
               46  CALL_FUNCTION_1       1  ''
               48  CALL_FUNCTION_1       1  ''
               50  STORE_FAST               'body_type'

 L. 419        52  LOAD_FAST                'body_type'
               54  LOAD_METHOD              serialise
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                body
               60  LOAD_CONST               0
               62  LOAD_FAST                'endian'
               64  CALL_METHOD_3         3  ''
               66  STORE_FAST               'body_buf'
               68  JUMP_FORWARD         74  'to 74'
             70_0  COME_FROM            20  '20'

 L. 421        70  LOAD_CONST               b''
               72  STORE_FAST               'body_buf'
             74_0  COME_FROM            68  '68'

 L. 423        74  LOAD_GLOBAL              len
               76  LOAD_FAST                'body_buf'
               78  CALL_FUNCTION_1       1  ''
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                header
               84  STORE_ATTR               body_length

 L. 425        86  LOAD_FAST                'self'
               88  LOAD_ATTR                header
               90  LOAD_ATTR                serialise
               92  LOAD_FAST                'serial'
               94  LOAD_CONST               ('serial',)
               96  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               98  STORE_FAST               'header_buf'

 L. 426       100  LOAD_CONST               b'\x00'
              102  LOAD_GLOBAL              padding
              104  LOAD_GLOBAL              len
              106  LOAD_FAST                'header_buf'
              108  CALL_FUNCTION_1       1  ''
              110  LOAD_CONST               8
              112  CALL_FUNCTION_2       2  ''
              114  BINARY_MULTIPLY  
              116  STORE_FAST               'pad'

 L. 427       118  LOAD_FAST                'header_buf'
              120  LOAD_FAST                'pad'
              122  BINARY_ADD       
              124  LOAD_FAST                'body_buf'
              126  BINARY_ADD       
              128  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 18


class Parser:
    __doc__ = 'Parse DBus messages from a stream of incoming data.\n    '

    def __init__(self):
        self.buf = BufferPipe()
        self.next_msg_size = None

    def add_data(self, data: bytes):
        """Provide newly received data to the parser"""
        self.buf.write(data)

    def feed(self, data):
        """Feed the parser newly read data.

        Returns a list of messages completed by the new data.
        """
        self.add_data(data)
        return list(iter(self.get_next_message, None))

    def get_next_message--- This code section failed: ---

 L. 454         0  LOAD_FAST                'self'
                2  LOAD_ATTR                next_msg_size
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    40  'to 40'

 L. 455        10  LOAD_FAST                'self'
               12  LOAD_ATTR                buf
               14  LOAD_ATTR                bytes_buffered
               16  LOAD_CONST               16
               18  COMPARE_OP               >=
               20  POP_JUMP_IF_FALSE    40  'to 40'

 L. 456        22  LOAD_GLOBAL              calc_msg_size
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                buf
               28  LOAD_METHOD              peek
               30  LOAD_CONST               16
               32  CALL_METHOD_1         1  ''
               34  CALL_FUNCTION_1       1  ''
               36  LOAD_FAST                'self'
               38  STORE_ATTR               next_msg_size
             40_0  COME_FROM            20  '20'
             40_1  COME_FROM             8  '8'

 L. 457        40  LOAD_FAST                'self'
               42  LOAD_ATTR                next_msg_size
               44  STORE_FAST               'nms'

 L. 458        46  LOAD_FAST                'nms'
               48  LOAD_CONST               None
               50  <117>                 1  ''
               52  POP_JUMP_IF_FALSE    98  'to 98'
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                buf
               58  LOAD_ATTR                bytes_buffered
               60  LOAD_FAST                'nms'
               62  COMPARE_OP               >=
               64  POP_JUMP_IF_FALSE    98  'to 98'

 L. 459        66  LOAD_FAST                'self'
               68  LOAD_ATTR                buf
               70  LOAD_METHOD              read
               72  LOAD_FAST                'nms'
               74  CALL_METHOD_1         1  ''
               76  STORE_FAST               'raw_msg'

 L. 460        78  LOAD_GLOBAL              Message
               80  LOAD_METHOD              from_buffer
               82  LOAD_FAST                'raw_msg'
               84  CALL_METHOD_1         1  ''
               86  STORE_FAST               'msg'

 L. 461        88  LOAD_CONST               None
               90  LOAD_FAST                'self'
               92  STORE_ATTR               next_msg_size

 L. 462        94  LOAD_FAST                'msg'
               96  RETURN_VALUE     
             98_0  COME_FROM            64  '64'
             98_1  COME_FROM            52  '52'

Parse error at or near `None' instruction at offset -1


class BufferPipe:
    __doc__ = 'A place to store received data until we can parse a complete message\n\n    The main difference from io.BytesIO is that read & write operate at\n    opposite ends, like a pipe.\n    '

    def __init__(self):
        self.chunks = deque()
        self.bytes_buffered = 0

    def write(self, b: bytes):
        self.chunks.append(b)
        self.bytes_buffered += len(b)

    def _peek_iter--- This code section failed: ---

 L. 480         0  LOAD_FAST                'nbytes'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                bytes_buffered
                6  COMPARE_OP               <=
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  <74>             
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             8  '8'

 L. 481        14  LOAD_FAST                'self'
               16  LOAD_ATTR                chunks
               18  GET_ITER         
             20_0  COME_FROM            66  '66'
             20_1  COME_FROM            60  '60'
               20  FOR_ITER             68  'to 68'
               22  STORE_FAST               'chunk'

 L. 482        24  LOAD_FAST                'chunk'
               26  LOAD_CONST               None
               28  LOAD_FAST                'nbytes'
               30  BUILD_SLICE_2         2 
               32  BINARY_SUBSCR    
               34  STORE_FAST               'chunk'

 L. 483        36  LOAD_FAST                'nbytes'
               38  LOAD_GLOBAL              len
               40  LOAD_FAST                'chunk'
               42  CALL_FUNCTION_1       1  ''
               44  INPLACE_SUBTRACT 
               46  STORE_FAST               'nbytes'

 L. 484        48  LOAD_FAST                'chunk'
               50  YIELD_VALUE      
               52  POP_TOP          

 L. 485        54  LOAD_FAST                'nbytes'
               56  LOAD_CONST               0
               58  COMPARE_OP               <=
               60  POP_JUMP_IF_FALSE_BACK    20  'to 20'

 L. 486        62  POP_TOP          
               64  BREAK_LOOP           68  'to 68'
               66  JUMP_BACK            20  'to 20'
             68_0  COME_FROM            64  '64'
             68_1  COME_FROM            20  '20'

Parse error at or near `None' instruction at offset -1

    def peek(self, nbytes: int) -> bytes:
        """Get exactly nbytes bytes from the front without removing them"""
        return (b'').join(self._peek_iter(nbytes))

    def _read_iter--- This code section failed: ---

 L. 493         0  LOAD_FAST                'nbytes'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                bytes_buffered
                6  COMPARE_OP               <=
                8  POP_JUMP_IF_TRUE     14  'to 14'
               10  <74>             
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM            74  '74'
             14_1  COME_FROM             8  '8'

 L. 495        14  LOAD_FAST                'self'
               16  LOAD_ATTR                chunks
               18  LOAD_METHOD              popleft
               20  CALL_METHOD_0         0  ''
               22  STORE_FAST               'chunk'

 L. 496        24  LOAD_FAST                'self'
               26  DUP_TOP          
               28  LOAD_ATTR                bytes_buffered
               30  LOAD_GLOBAL              len
               32  LOAD_FAST                'chunk'
               34  CALL_FUNCTION_1       1  ''
               36  INPLACE_SUBTRACT 
               38  ROT_TWO          
               40  STORE_ATTR               bytes_buffered

 L. 497        42  LOAD_FAST                'nbytes'
               44  LOAD_GLOBAL              len
               46  LOAD_FAST                'chunk'
               48  CALL_FUNCTION_1       1  ''
               50  COMPARE_OP               <=
               52  POP_JUMP_IF_FALSE    56  'to 56'

 L. 498        54  JUMP_FORWARD         76  'to 76'
             56_0  COME_FROM            52  '52'

 L. 499        56  LOAD_FAST                'nbytes'
               58  LOAD_GLOBAL              len
               60  LOAD_FAST                'chunk'
               62  CALL_FUNCTION_1       1  ''
               64  INPLACE_SUBTRACT 
               66  STORE_FAST               'nbytes'

 L. 500        68  LOAD_FAST                'chunk'
               70  YIELD_VALUE      
               72  POP_TOP          
               74  JUMP_BACK            14  'to 14'
             76_0  COME_FROM            54  '54'

 L. 503        76  LOAD_FAST                'chunk'
               78  LOAD_CONST               None
               80  LOAD_FAST                'nbytes'
               82  BUILD_SLICE_2         2 
               84  BINARY_SUBSCR    
               86  LOAD_FAST                'chunk'
               88  LOAD_FAST                'nbytes'
               90  LOAD_CONST               None
               92  BUILD_SLICE_2         2 
               94  BINARY_SUBSCR    
               96  ROT_TWO          
               98  STORE_FAST               'chunk'
              100  STORE_FAST               'rem'

 L. 504       102  LOAD_FAST                'rem'
              104  POP_JUMP_IF_FALSE   136  'to 136'

 L. 505       106  LOAD_FAST                'self'
              108  LOAD_ATTR                chunks
              110  LOAD_METHOD              appendleft
              112  LOAD_FAST                'rem'
              114  CALL_METHOD_1         1  ''
              116  POP_TOP          

 L. 506       118  LOAD_FAST                'self'
              120  DUP_TOP          
              122  LOAD_ATTR                bytes_buffered
              124  LOAD_GLOBAL              len
              126  LOAD_FAST                'rem'
              128  CALL_FUNCTION_1       1  ''
              130  INPLACE_ADD      
              132  ROT_TWO          
              134  STORE_ATTR               bytes_buffered
            136_0  COME_FROM           104  '104'

 L. 507       136  LOAD_FAST                'chunk'
              138  YIELD_VALUE      
              140  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def read(self, nbytes: int) -> bytes:
        """Take & return exactly nbytes bytes from the front"""
        return (b'').join(self._read_iter(nbytes))