# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: uuid.py
r"""UUID objects (universally unique identifiers) according to RFC 4122.

This module provides immutable UUID objects (class UUID) and the functions
uuid1(), uuid3(), uuid4(), uuid5() for generating version 1, 3, 4, and 5
UUIDs as specified in RFC 4122.

If all you want is a unique ID, you should probably call uuid1() or uuid4().
Note that uuid1() may compromise privacy since it creates a UUID containing
the computer's network address.  uuid4() creates a random UUID.

Typical usage:

    >>> import uuid

    # make a UUID based on the host ID and current time
    >>> uuid.uuid1()    # doctest: +SKIP
    UUID('a8098c1a-f86e-11da-bd1a-00112444be1e')

    # make a UUID using an MD5 hash of a namespace UUID and a name
    >>> uuid.uuid3(uuid.NAMESPACE_DNS, 'python.org')
    UUID('6fa459ea-ee8a-3ca4-894e-db77e160355e')

    # make a random UUID
    >>> uuid.uuid4()    # doctest: +SKIP
    UUID('16fd2706-8baf-433b-82eb-8c7fada847da')

    # make a UUID using a SHA-1 hash of a namespace UUID and a name
    >>> uuid.uuid5(uuid.NAMESPACE_DNS, 'python.org')
    UUID('886313e1-3b8a-5372-9b90-0c9aee199e5d')

    # make a UUID from a string of hex digits (braces and hyphens ignored)
    >>> x = uuid.UUID('{00010203-0405-0607-0809-0a0b0c0d0e0f}')

    # convert a UUID to a string of hex digits in standard form
    >>> str(x)
    '00010203-0405-0607-0809-0a0b0c0d0e0f'

    # get the raw 16 bytes of the UUID
    >>> x.bytes
    b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'

    # make a UUID from a 16-byte string
    >>> uuid.UUID(bytes=x.bytes)
    UUID('00010203-0405-0607-0809-0a0b0c0d0e0f')
"""
import os, platform, sys
from enum import Enum
__author__ = 'Ka-Ping Yee <ping@zesty.ca>'
_AIX = platform.system() == 'AIX'
_DARWIN = platform.system() == 'Darwin'
_LINUX = platform.system() == 'Linux'
_WINDOWS = platform.system() == 'Windows'
RESERVED_NCS, RFC_4122, RESERVED_MICROSOFT, RESERVED_FUTURE = [
 'reserved for NCS compatibility', 'specified in RFC 4122',
 'reserved for Microsoft compatibility', 'reserved for future definition']
int_ = int
bytes_ = bytes

class SafeUUID(Enum):
    safe = 0
    unsafe = -1
    unknown = None


class UUID:
    __doc__ = "Instances of the UUID class represent UUIDs as specified in RFC 4122.\n    UUID objects are immutable, hashable, and usable as dictionary keys.\n    Converting a UUID to a string with str() yields something in the form\n    '12345678-1234-1234-1234-123456789abc'.  The UUID constructor accepts\n    five possible forms: a similar string of hexadecimal digits, or a tuple\n    of six integer fields (with 32-bit, 16-bit, 16-bit, 8-bit, 8-bit, and\n    48-bit values respectively) as an argument named 'fields', or a string\n    of 16 bytes (with all the integer fields in big-endian order) as an\n    argument named 'bytes', or a string of 16 bytes (with the first three\n    fields in little-endian order) as an argument named 'bytes_le', or a\n    single 128-bit integer as an argument named 'int'.\n\n    UUIDs have these read-only attributes:\n\n        bytes       the UUID as a 16-byte string (containing the six\n                    integer fields in big-endian byte order)\n\n        bytes_le    the UUID as a 16-byte string (with time_low, time_mid,\n                    and time_hi_version in little-endian byte order)\n\n        fields      a tuple of the six integer fields of the UUID,\n                    which are also available as six individual attributes\n                    and two derived attributes:\n\n            time_low                the first 32 bits of the UUID\n            time_mid                the next 16 bits of the UUID\n            time_hi_version         the next 16 bits of the UUID\n            clock_seq_hi_variant    the next 8 bits of the UUID\n            clock_seq_low           the next 8 bits of the UUID\n            node                    the last 48 bits of the UUID\n\n            time                    the 60-bit timestamp\n            clock_seq               the 14-bit sequence number\n\n        hex         the UUID as a 32-character hexadecimal string\n\n        int         the UUID as a 128-bit integer\n\n        urn         the UUID as a URN as specified in RFC 4122\n\n        variant     the UUID variant (one of the constants RESERVED_NCS,\n                    RFC_4122, RESERVED_MICROSOFT, or RESERVED_FUTURE)\n\n        version     the UUID version number (1 through 5, meaningful only\n                    when the variant is RFC_4122)\n\n        is_safe     An enum indicating whether the UUID has been generated in\n                    a way that is safe for multiprocessing applications, via\n                    uuid_generate_time_safe(3).\n    "
    __slots__ = ('int', 'is_safe', '__weakref__')

    def __init__(self, hex=None, bytes=None, bytes_le=None, fields=None, int=None, version=None, *, is_safe=SafeUUID.unknown):
        r"""Create a UUID from either a string of 32 hexadecimal digits,
        a string of 16 bytes as the 'bytes' argument, a string of 16 bytes
        in little-endian order as the 'bytes_le' argument, a tuple of six
        integers (32-bit time_low, 16-bit time_mid, 16-bit time_hi_version,
        8-bit clock_seq_hi_variant, 8-bit clock_seq_low, 48-bit node) as
        the 'fields' argument, or a single 128-bit integer as the 'int'
        argument.  When a string of hex digits is given, curly braces,
        hyphens, and a URN prefix are all optional.  For example, these
        expressions all yield the same UUID:

        UUID('{12345678-1234-5678-1234-567812345678}')
        UUID('12345678123456781234567812345678')
        UUID('urn:uuid:12345678-1234-5678-1234-567812345678')
        UUID(bytes='\x12\x34\x56\x78'*4)
        UUID(bytes_le='\x78\x56\x34\x12\x34\x12\x78\x56' +
                      '\x12\x34\x56\x78\x12\x34\x56\x78')
        UUID(fields=(0x12345678, 0x1234, 0x5678, 0x12, 0x34, 0x567812345678))
        UUID(int=0x12345678123456781234567812345678)

        Exactly one of 'hex', 'bytes', 'bytes_le', 'fields', or 'int' must
        be given.  The 'version' argument is optional; if given, the resulting
        UUID will have its variant and version set according to RFC 4122,
        overriding the given 'hex', 'bytes', 'bytes_le', 'fields', or 'int'.

        is_safe is an enum exposed as an attribute on the instance.  It
        indicates whether the UUID has been generated in a way that is safe
        for multiprocessing applications, via uuid_generate_time_safe(3).
        """
        if [
         hex, bytes, bytes_le, fields, int].count(None) != 4:
            raise TypeError('one of the hex, bytes, bytes_le, fields, or int arguments must be given')
        if hex is not None:
            hex = hex.replace('urn:', '').replace('uuid:', '')
            hex = hex.strip('{}').replace('-', '')
            if len(hex) != 32:
                raise ValueError('badly formed hexadecimal UUID string')
            int = int_(hex, 16)
        if bytes_le is not None:
            if len(bytes_le) != 16:
                raise ValueError('bytes_le is not a 16-char string')
            bytes = bytes_le[3::-1] + bytes_le[5:3:-1] + bytes_le[7:5:-1] + bytes_le[8:]
        if bytes is not None:
            if len(bytes) != 16:
                raise ValueError('bytes is not a 16-char string')
            assert isinstance(bytes, bytes_), repr(bytes)
            int = int_.from_bytes(bytes, byteorder='big')
        if fields is not None:
            if len(fields) != 6:
                raise ValueError('fields is not a 6-tuple')
            time_low, time_mid, time_hi_version, clock_seq_hi_variant, clock_seq_low, node = fields
            if not 0 <= time_low < 4294967296:
                raise ValueError('field 1 out of range (need a 32-bit value)')
            if not 0 <= time_mid < 65536:
                raise ValueError('field 2 out of range (need a 16-bit value)')
            if not 0 <= time_hi_version < 65536:
                raise ValueError('field 3 out of range (need a 16-bit value)')
            if not 0 <= clock_seq_hi_variant < 256:
                raise ValueError('field 4 out of range (need an 8-bit value)')
            if not 0 <= clock_seq_low < 256:
                raise ValueError('field 5 out of range (need an 8-bit value)')
            if not 0 <= node < 281474976710656:
                raise ValueError('field 6 out of range (need a 48-bit value)')
            clock_seq = clock_seq_hi_variant << 8 | clock_seq_low
            int = time_low << 96 | time_mid << 80 | time_hi_version << 64 | clock_seq << 48 | node
        if int is not None:
            if not 0 <= int < 1 << 128:
                raise ValueError('int is out of range (need a 128-bit value)')
        if version is not None:
            if not 1 <= version <= 5:
                raise ValueError('illegal version number')
            int &= -13835058055282163713
            int |= 9223372036854775808
            int &= -1133367955888714851287041
            int |= version << 76
        object.__setattr__(self, 'int', int)
        object.__setattr__(self, 'is_safe', is_safe)

    def __getstate__(self):
        d = {'int': self.int}
        if self.is_safe != SafeUUID.unknown:
            d['is_safe'] = self.is_safe.value
        return d

    def __setstate__(self, state):
        object.__setattr__(self, 'int', state['int'])
        object.__setattr__(self, 'is_safe', SafeUUID(state['is_safe']) if 'is_safe' in state else SafeUUID.unknown)

    def __eq__(self, other):
        if isinstance(other, UUID):
            return self.int == other.int
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, UUID):
            return self.int < other.int
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, UUID):
            return self.int > other.int
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, UUID):
            return self.int <= other.int
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, UUID):
            return self.int >= other.int
        return NotImplemented

    def __hash__(self):
        return hash(self.int)

    def __int__(self):
        return self.int

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, str(self))

    def __setattr__(self, name, value):
        raise TypeError('UUID objects are immutable')

    def __str__(self):
        hex = '%032x' % self.int
        return '%s-%s-%s-%s-%s' % (
         hex[:8], hex[8:12], hex[12:16], hex[16:20], hex[20:])

    @property
    def bytes(self):
        return self.int.to_bytes(16, 'big')

    @property
    def bytes_le(self):
        bytes = self.bytes
        return bytes[3::-1] + bytes[5:3:-1] + bytes[7:5:-1] + bytes[8:]

    @property
    def fields(self):
        return (
         self.time_low, self.time_mid, self.time_hi_version,
         self.clock_seq_hi_variant, self.clock_seq_low, self.node)

    @property
    def time_low(self):
        return self.int >> 96

    @property
    def time_mid(self):
        return self.int >> 80 & 65535

    @property
    def time_hi_version(self):
        return self.int >> 64 & 65535

    @property
    def clock_seq_hi_variant(self):
        return self.int >> 56 & 255

    @property
    def clock_seq_low(self):
        return self.int >> 48 & 255

    @property
    def time(self):
        return (self.time_hi_version & 4095) << 48 | self.time_mid << 32 | self.time_low

    @property
    def clock_seq(self):
        return (self.clock_seq_hi_variant & 63) << 8 | self.clock_seq_low

    @property
    def node(self):
        return self.int & 281474976710655

    @property
    def hex(self):
        return '%032x' % self.int

    @property
    def urn(self):
        return 'urn:uuid:' + str(self)

    @property
    def variant(self):
        if not self.int & 9223372036854775808:
            return RESERVED_NCS
        if not self.int & 4611686018427387904:
            return RFC_4122
        if not self.int & 2305843009213693952:
            return RESERVED_MICROSOFT
        return RESERVED_FUTURE

    @property
    def version(self):
        if self.variant == RFC_4122:
            return int(self.int >> 76 & 15)


def _popen(command, *args):
    import os, shutil, subprocess
    executable = shutil.which(command)
    if executable is None:
        path = os.pathsep.join(('/sbin', '/usr/sbin'))
        executable = shutil.which(command, path=path)
        if executable is None:
            return
    env = dict(os.environ)
    env['LC_ALL'] = 'C'
    proc = subprocess.Popen(((executable,) + args), stdout=(subprocess.PIPE),
      stderr=(subprocess.DEVNULL),
      env=env)
    return proc


def _is_universal(mac):
    return not mac & 2199023255552


def _find_mac--- This code section failed: ---

 L. 388         0  LOAD_CONST               None
                2  STORE_FAST               'first_local_mac'

 L. 389         4  SETUP_FINALLY       216  'to 216'

 L. 390         6  LOAD_GLOBAL              _popen
                8  LOAD_FAST                'command'
               10  BUILD_TUPLE_1         1 
               12  LOAD_FAST                'args'
               14  LOAD_METHOD              split
               16  CALL_METHOD_0         0  ''
               18  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
               20  CALL_FUNCTION_EX      0  'positional arguments only'
               22  STORE_FAST               'proc'

 L. 391        24  LOAD_FAST                'proc'
               26  POP_JUMP_IF_TRUE     34  'to 34'

 L. 392        28  POP_BLOCK        
               30  LOAD_CONST               None
               32  RETURN_VALUE     
             34_0  COME_FROM            26  '26'

 L. 393        34  LOAD_FAST                'proc'
               36  SETUP_WITH          206  'to 206'
               38  POP_TOP          

 L. 394        40  LOAD_FAST                'proc'
               42  LOAD_ATTR                stdout
               44  GET_ITER         
             46_0  COME_FROM           200  '200'
               46  FOR_ITER            202  'to 202'
               48  STORE_FAST               'line'

 L. 395        50  LOAD_FAST                'line'
               52  LOAD_METHOD              lower
               54  CALL_METHOD_0         0  ''
               56  LOAD_METHOD              rstrip
               58  CALL_METHOD_0         0  ''
               60  LOAD_METHOD              split
               62  CALL_METHOD_0         0  ''
               64  STORE_FAST               'words'

 L. 396        66  LOAD_GLOBAL              range
               68  LOAD_GLOBAL              len
               70  LOAD_FAST                'words'
               72  CALL_FUNCTION_1       1  ''
               74  CALL_FUNCTION_1       1  ''
               76  GET_ITER         
             78_0  COME_FROM           198  '198'
             78_1  COME_FROM           194  '194'
             78_2  COME_FROM           172  '172'
             78_3  COME_FROM            92  '92'
               78  FOR_ITER            200  'to 200'
               80  STORE_FAST               'i'

 L. 397        82  LOAD_FAST                'words'
               84  LOAD_FAST                'i'
               86  BINARY_SUBSCR    
               88  LOAD_FAST                'hw_identifiers'
               90  COMPARE_OP               in
               92  POP_JUMP_IF_FALSE_BACK    78  'to 78'

 L. 398        94  SETUP_FINALLY       174  'to 174'

 L. 399        96  LOAD_FAST                'words'
               98  LOAD_FAST                'get_index'
              100  LOAD_FAST                'i'
              102  CALL_FUNCTION_1       1  ''
              104  BINARY_SUBSCR    
              106  STORE_FAST               'word'

 L. 400       108  LOAD_GLOBAL              int
              110  LOAD_FAST                'word'
              112  LOAD_METHOD              replace
              114  LOAD_CONST               b':'
              116  LOAD_CONST               b''
              118  CALL_METHOD_2         2  ''
              120  LOAD_CONST               16
              122  CALL_FUNCTION_2       2  ''
              124  STORE_FAST               'mac'

 L. 401       126  LOAD_GLOBAL              _is_universal
              128  LOAD_FAST                'mac'
              130  CALL_FUNCTION_1       1  ''
              132  POP_JUMP_IF_FALSE   162  'to 162'

 L. 402       134  LOAD_FAST                'mac'
              136  POP_BLOCK        
              138  ROT_TWO          
              140  POP_TOP          
              142  ROT_TWO          
              144  POP_TOP          
              146  POP_BLOCK        
              148  ROT_TWO          
              150  BEGIN_FINALLY    
              152  WITH_CLEANUP_START
              154  WITH_CLEANUP_FINISH
              156  POP_FINALLY           0  ''
              158  POP_BLOCK        
              160  RETURN_VALUE     
            162_0  COME_FROM           132  '132'

 L. 403       162  LOAD_FAST                'first_local_mac'
              164  JUMP_IF_TRUE_OR_POP   168  'to 168'
              166  LOAD_FAST                'mac'
            168_0  COME_FROM           164  '164'
              168  STORE_FAST               'first_local_mac'
              170  POP_BLOCK        
              172  JUMP_BACK            78  'to 78'
            174_0  COME_FROM_FINALLY    94  '94'

 L. 404       174  DUP_TOP          
              176  LOAD_GLOBAL              ValueError
              178  LOAD_GLOBAL              IndexError
              180  BUILD_TUPLE_2         2 
              182  COMPARE_OP               exception-match
              184  POP_JUMP_IF_FALSE   196  'to 196'
              186  POP_TOP          
              188  POP_TOP          
              190  POP_TOP          

 L. 410       192  POP_EXCEPT       
              194  JUMP_BACK            78  'to 78'
            196_0  COME_FROM           184  '184'
              196  END_FINALLY      
              198  JUMP_BACK            78  'to 78'
            200_0  COME_FROM            78  '78'
              200  JUMP_BACK            46  'to 46'
            202_0  COME_FROM            46  '46'
              202  POP_BLOCK        
              204  BEGIN_FINALLY    
            206_0  COME_FROM_WITH       36  '36'
              206  WITH_CLEANUP_START
              208  WITH_CLEANUP_FINISH
              210  END_FINALLY      
              212  POP_BLOCK        
              214  JUMP_FORWARD        236  'to 236'
            216_0  COME_FROM_FINALLY     4  '4'

 L. 411       216  DUP_TOP          
              218  LOAD_GLOBAL              OSError
              220  COMPARE_OP               exception-match
              222  POP_JUMP_IF_FALSE   234  'to 234'
              224  POP_TOP          
              226  POP_TOP          
              228  POP_TOP          

 L. 412       230  POP_EXCEPT       
              232  JUMP_FORWARD        236  'to 236'
            234_0  COME_FROM           222  '222'
              234  END_FINALLY      
            236_0  COME_FROM           232  '232'
            236_1  COME_FROM           214  '214'

 L. 413       236  LOAD_FAST                'first_local_mac'
              238  JUMP_IF_TRUE_OR_POP   242  'to 242'
              240  LOAD_CONST               None
            242_0  COME_FROM           238  '238'
              242  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 30


def _ifconfig_getnode():
    """Get the hardware address on Unix by running ifconfig."""
    keywords = (b'hwaddr', b'ether', b'address:', b'lladdr')
    for args in ('', '-a', '-av'):
        mac = _find_mac('ifconfig', args, keywords, lambda i: i + 1)
        if mac:
            return mac
        else:
            return


def _ip_getnode():
    """Get the hardware address on Unix by running ip."""
    mac = _find_mac('ip', 'link', [b'link/ether'], lambda i: i + 1)
    if mac:
        return mac


def _arp_getnode():
    """Get the hardware address on Unix by running arp."""
    import os, socket
    try:
        ip_addr = socket.gethostbyname(socket.gethostname())
    except OSError:
        return
    else:
        mac = _find_mac('arp', '-an', [os.fsencode(ip_addr)], lambda i: -1)
        if mac:
            return mac
        mac = _find_mac('arp', '-an', [os.fsencode(ip_addr)], lambda i: i + 1)
        if mac:
            return mac
        mac = _find_mac('arp', '-an', [os.fsencode('(%s)' % ip_addr)], lambda i: i + 2)
        if mac:
            return mac


def _lanscan_getnode():
    """Get the hardware address on Unix by running lanscan."""
    return _find_mac('lanscan', '-ai', [b'lan0'], lambda i: 0)


def _netstat_getnode--- This code section failed: ---

 L. 467         0  LOAD_CONST               None
                2  STORE_FAST               'first_local_mac'

 L. 468       4_6  SETUP_FINALLY       262  'to 262'

 L. 469         8  LOAD_GLOBAL              _popen
               10  LOAD_STR                 'netstat'
               12  LOAD_STR                 '-ia'
               14  CALL_FUNCTION_2       2  ''
               16  STORE_FAST               'proc'

 L. 470        18  LOAD_FAST                'proc'
               20  POP_JUMP_IF_TRUE     28  'to 28'

 L. 471        22  POP_BLOCK        
               24  LOAD_CONST               None
               26  RETURN_VALUE     
             28_0  COME_FROM            20  '20'

 L. 472        28  LOAD_FAST                'proc'
               30  SETUP_WITH          252  'to 252'
               32  POP_TOP          

 L. 473        34  LOAD_FAST                'proc'
               36  LOAD_ATTR                stdout
               38  LOAD_METHOD              readline
               40  CALL_METHOD_0         0  ''
               42  LOAD_METHOD              rstrip
               44  CALL_METHOD_0         0  ''
               46  LOAD_METHOD              split
               48  CALL_METHOD_0         0  ''
               50  STORE_FAST               'words'

 L. 474        52  SETUP_FINALLY        68  'to 68'

 L. 475        54  LOAD_FAST                'words'
               56  LOAD_METHOD              index
               58  LOAD_CONST               b'Address'
               60  CALL_METHOD_1         1  ''
               62  STORE_FAST               'i'
               64  POP_BLOCK        
               66  JUMP_FORWARD        102  'to 102'
             68_0  COME_FROM_FINALLY    52  '52'

 L. 476        68  DUP_TOP          
               70  LOAD_GLOBAL              ValueError
               72  COMPARE_OP               exception-match
               74  POP_JUMP_IF_FALSE   100  'to 100'
               76  POP_TOP          
               78  POP_TOP          
               80  POP_TOP          

 L. 477        82  POP_EXCEPT       
               84  POP_BLOCK        
               86  BEGIN_FINALLY    
               88  WITH_CLEANUP_START
               90  WITH_CLEANUP_FINISH
               92  POP_FINALLY           0  ''
               94  POP_BLOCK        
               96  LOAD_CONST               None
               98  RETURN_VALUE     
            100_0  COME_FROM            74  '74'
              100  END_FINALLY      
            102_0  COME_FROM            66  '66'

 L. 478       102  LOAD_FAST                'proc'
              104  LOAD_ATTR                stdout
              106  GET_ITER         
            108_0  COME_FROM           246  '246'
            108_1  COME_FROM           242  '242'
            108_2  COME_FROM           220  '220'
              108  FOR_ITER            248  'to 248'
              110  STORE_FAST               'line'

 L. 479       112  SETUP_FINALLY       222  'to 222'

 L. 480       114  LOAD_FAST                'line'
              116  LOAD_METHOD              rstrip
              118  CALL_METHOD_0         0  ''
              120  LOAD_METHOD              split
              122  CALL_METHOD_0         0  ''
              124  STORE_FAST               'words'

 L. 481       126  LOAD_FAST                'words'
              128  LOAD_FAST                'i'
              130  BINARY_SUBSCR    
              132  STORE_FAST               'word'

 L. 482       134  LOAD_GLOBAL              len
              136  LOAD_FAST                'word'
              138  CALL_FUNCTION_1       1  ''
              140  LOAD_CONST               17
              142  COMPARE_OP               ==
              144  POP_JUMP_IF_FALSE   218  'to 218'
              146  LOAD_FAST                'word'
              148  LOAD_METHOD              count
              150  LOAD_CONST               b':'
              152  CALL_METHOD_1         1  ''
              154  LOAD_CONST               5
              156  COMPARE_OP               ==
              158  POP_JUMP_IF_FALSE   218  'to 218'

 L. 483       160  LOAD_GLOBAL              int
              162  LOAD_FAST                'word'
              164  LOAD_METHOD              replace
              166  LOAD_CONST               b':'
              168  LOAD_CONST               b''
              170  CALL_METHOD_2         2  ''
              172  LOAD_CONST               16
              174  CALL_FUNCTION_2       2  ''
              176  STORE_FAST               'mac'

 L. 484       178  LOAD_GLOBAL              _is_universal
              180  LOAD_FAST                'mac'
              182  CALL_FUNCTION_1       1  ''
              184  POP_JUMP_IF_FALSE   210  'to 210'

 L. 485       186  LOAD_FAST                'mac'
              188  POP_BLOCK        
              190  ROT_TWO          
              192  POP_TOP          
              194  POP_BLOCK        
              196  ROT_TWO          
              198  BEGIN_FINALLY    
              200  WITH_CLEANUP_START
              202  WITH_CLEANUP_FINISH
              204  POP_FINALLY           0  ''
              206  POP_BLOCK        
              208  RETURN_VALUE     
            210_0  COME_FROM           184  '184'

 L. 486       210  LOAD_FAST                'first_local_mac'
              212  JUMP_IF_TRUE_OR_POP   216  'to 216'
              214  LOAD_FAST                'mac'
            216_0  COME_FROM           212  '212'
              216  STORE_FAST               'first_local_mac'
            218_0  COME_FROM           158  '158'
            218_1  COME_FROM           144  '144'
              218  POP_BLOCK        
              220  JUMP_BACK           108  'to 108'
            222_0  COME_FROM_FINALLY   112  '112'

 L. 487       222  DUP_TOP          
              224  LOAD_GLOBAL              ValueError
              226  LOAD_GLOBAL              IndexError
              228  BUILD_TUPLE_2         2 
              230  COMPARE_OP               exception-match
              232  POP_JUMP_IF_FALSE   244  'to 244'
              234  POP_TOP          
              236  POP_TOP          
              238  POP_TOP          

 L. 488       240  POP_EXCEPT       
              242  JUMP_BACK           108  'to 108'
            244_0  COME_FROM           232  '232'
              244  END_FINALLY      
              246  JUMP_BACK           108  'to 108'
            248_0  COME_FROM           108  '108'
              248  POP_BLOCK        
              250  BEGIN_FINALLY    
            252_0  COME_FROM_WITH       30  '30'
              252  WITH_CLEANUP_START
              254  WITH_CLEANUP_FINISH
              256  END_FINALLY      
              258  POP_BLOCK        
              260  JUMP_FORWARD        284  'to 284'
            262_0  COME_FROM_FINALLY     4  '4'

 L. 489       262  DUP_TOP          
              264  LOAD_GLOBAL              OSError
              266  COMPARE_OP               exception-match
          268_270  POP_JUMP_IF_FALSE   282  'to 282'
              272  POP_TOP          
              274  POP_TOP          
              276  POP_TOP          

 L. 490       278  POP_EXCEPT       
              280  JUMP_FORWARD        284  'to 284'
            282_0  COME_FROM           268  '268'
              282  END_FINALLY      
            284_0  COME_FROM           280  '280'
            284_1  COME_FROM           260  '260'

 L. 491       284  LOAD_FAST                'first_local_mac'
          286_288  JUMP_IF_TRUE_OR_POP   292  'to 292'
              290  LOAD_CONST               None
            292_0  COME_FROM           286  '286'
              292  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 24


def _ipconfig_getnode--- This code section failed: ---

 L. 495         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              os
                6  STORE_FAST               'os'
                8  LOAD_CONST               0
               10  LOAD_CONST               None
               12  IMPORT_NAME              re
               14  STORE_FAST               're'
               16  LOAD_CONST               0
               18  LOAD_CONST               None
               20  IMPORT_NAME              subprocess
               22  STORE_FAST               'subprocess'

 L. 496        24  LOAD_CONST               None
               26  STORE_FAST               'first_local_mac'

 L. 497        28  LOAD_STR                 ''
               30  LOAD_STR                 'c:\\windows\\system32'
               32  LOAD_STR                 'c:\\winnt\\system32'
               34  BUILD_LIST_3          3 
               36  STORE_FAST               'dirs'

 L. 498        38  SETUP_FINALLY        98  'to 98'

 L. 499        40  LOAD_CONST               0
               42  LOAD_CONST               None
               44  IMPORT_NAME              ctypes
               46  STORE_FAST               'ctypes'

 L. 500        48  LOAD_FAST                'ctypes'
               50  LOAD_METHOD              create_string_buffer
               52  LOAD_CONST               300
               54  CALL_METHOD_1         1  ''
               56  STORE_FAST               'buffer'

 L. 501        58  LOAD_FAST                'ctypes'
               60  LOAD_ATTR                windll
               62  LOAD_ATTR                kernel32
               64  LOAD_METHOD              GetSystemDirectoryA
               66  LOAD_FAST                'buffer'
               68  LOAD_CONST               300
               70  CALL_METHOD_2         2  ''
               72  POP_TOP          

 L. 502        74  LOAD_FAST                'dirs'
               76  LOAD_METHOD              insert
               78  LOAD_CONST               0
               80  LOAD_FAST                'buffer'
               82  LOAD_ATTR                value
               84  LOAD_METHOD              decode
               86  LOAD_STR                 'mbcs'
               88  CALL_METHOD_1         1  ''
               90  CALL_METHOD_2         2  ''
               92  POP_TOP          
               94  POP_BLOCK        
               96  JUMP_FORWARD        110  'to 110'
             98_0  COME_FROM_FINALLY    38  '38'

 L. 503        98  POP_TOP          
              100  POP_TOP          
              102  POP_TOP          

 L. 504       104  POP_EXCEPT       
              106  JUMP_FORWARD        110  'to 110'
              108  END_FINALLY      
            110_0  COME_FROM           106  '106'
            110_1  COME_FROM            96  '96'

 L. 505       110  LOAD_FAST                'dirs'
              112  GET_ITER         
            114_0  COME_FROM           304  '304'
            114_1  COME_FROM           172  '172'
              114  FOR_ITER            306  'to 306'
              116  STORE_FAST               'dir'

 L. 506       118  SETUP_FINALLY       156  'to 156'

 L. 507       120  LOAD_FAST                'subprocess'
              122  LOAD_ATTR                Popen
              124  LOAD_FAST                'os'
              126  LOAD_ATTR                path
              128  LOAD_METHOD              join
              130  LOAD_FAST                'dir'
              132  LOAD_STR                 'ipconfig'
              134  CALL_METHOD_2         2  ''
              136  LOAD_STR                 '/all'
              138  BUILD_LIST_2          2 

 L. 508       140  LOAD_FAST                'subprocess'
              142  LOAD_ATTR                PIPE

 L. 509       144  LOAD_STR                 'oem'

 L. 507       146  LOAD_CONST               ('stdout', 'encoding')
              148  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              150  STORE_FAST               'proc'
              152  POP_BLOCK        
              154  JUMP_FORWARD        180  'to 180'
            156_0  COME_FROM_FINALLY   118  '118'

 L. 510       156  DUP_TOP          
              158  LOAD_GLOBAL              OSError
              160  COMPARE_OP               exception-match
              162  POP_JUMP_IF_FALSE   178  'to 178'
              164  POP_TOP          
              166  POP_TOP          
              168  POP_TOP          

 L. 511       170  POP_EXCEPT       
              172  JUMP_BACK           114  'to 114'
              174  POP_EXCEPT       
              176  JUMP_FORWARD        180  'to 180'
            178_0  COME_FROM           162  '162'
              178  END_FINALLY      
            180_0  COME_FROM           176  '176'
            180_1  COME_FROM           154  '154'

 L. 512       180  LOAD_FAST                'proc'
              182  SETUP_WITH          298  'to 298'
              184  POP_TOP          

 L. 513       186  LOAD_FAST                'proc'
              188  LOAD_ATTR                stdout
              190  GET_ITER         
            192_0  COME_FROM           292  '292'
            192_1  COME_FROM           228  '228'
              192  FOR_ITER            294  'to 294'
              194  STORE_FAST               'line'

 L. 514       196  LOAD_FAST                'line'
              198  LOAD_METHOD              split
              200  LOAD_STR                 ':'
              202  CALL_METHOD_1         1  ''
              204  LOAD_CONST               -1
              206  BINARY_SUBSCR    
              208  LOAD_METHOD              strip
              210  CALL_METHOD_0         0  ''
              212  LOAD_METHOD              lower
              214  CALL_METHOD_0         0  ''
              216  STORE_FAST               'value'

 L. 515       218  LOAD_FAST                're'
              220  LOAD_METHOD              fullmatch
              222  LOAD_STR                 '(?:[0-9a-f][0-9a-f]-){5}[0-9a-f][0-9a-f]'
              224  LOAD_FAST                'value'
              226  CALL_METHOD_2         2  ''
              228  POP_JUMP_IF_FALSE_BACK   192  'to 192'

 L. 516       230  LOAD_GLOBAL              int
              232  LOAD_FAST                'value'
              234  LOAD_METHOD              replace
              236  LOAD_STR                 '-'
              238  LOAD_STR                 ''
              240  CALL_METHOD_2         2  ''
              242  LOAD_CONST               16
              244  CALL_FUNCTION_2       2  ''
              246  STORE_FAST               'mac'

 L. 517       248  LOAD_GLOBAL              _is_universal
              250  LOAD_FAST                'mac'
              252  CALL_FUNCTION_1       1  ''
          254_256  POP_JUMP_IF_FALSE   282  'to 282'

 L. 518       258  LOAD_FAST                'mac'
              260  ROT_TWO          
              262  POP_TOP          
              264  POP_BLOCK        
              266  ROT_TWO          
              268  BEGIN_FINALLY    
              270  WITH_CLEANUP_START
              272  WITH_CLEANUP_FINISH
              274  POP_FINALLY           0  ''
              276  ROT_TWO          
              278  POP_TOP          
              280  RETURN_VALUE     
            282_0  COME_FROM           254  '254'

 L. 519       282  LOAD_FAST                'first_local_mac'
          284_286  JUMP_IF_TRUE_OR_POP   290  'to 290'
              288  LOAD_FAST                'mac'
            290_0  COME_FROM           284  '284'
              290  STORE_FAST               'first_local_mac'
              292  JUMP_BACK           192  'to 192'
            294_0  COME_FROM           192  '192'
              294  POP_BLOCK        
              296  BEGIN_FINALLY    
            298_0  COME_FROM_WITH      182  '182'
              298  WITH_CLEANUP_START
              300  WITH_CLEANUP_FINISH
              302  END_FINALLY      
              304  JUMP_BACK           114  'to 114'
            306_0  COME_FROM           114  '114'

 L. 520       306  LOAD_FAST                'first_local_mac'
          308_310  JUMP_IF_TRUE_OR_POP   314  'to 314'
              312  LOAD_CONST               None
            314_0  COME_FROM           308  '308'
              314  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 178_0


def _netbios_getnode():
    """Get the hardware address on Windows using NetBIOS calls.
    See http://support.microsoft.com/kb/118623 for details."""
    import win32wnet, netbios
    first_local_mac = None
    ncb = netbios.NCB()
    ncb.Command = netbios.NCBENUM
    ncb.Buffer = adapters = netbios.LANA_ENUM()
    adapters._pack()
    if win32wnet.Netbios(ncb) != 0:
        return
    adapters._unpack()
    for i in range(adapters.length):
        ncb.Reset()
        ncb.Command = netbios.NCBRESET
        ncb.Lana_num = ord(adapters.lana[i])
        if win32wnet.Netbios(ncb) != 0:
            pass
        else:
            ncb.Reset()
            ncb.Command = netbios.NCBASTAT
            ncb.Lana_num = ord(adapters.lana[i])
            ncb.Callname = '*'.ljust(16)
            ncb.Buffer = status = netbios.ADAPTER_STATUS()
            if win32wnet.Netbios(ncb) != 0:
                pass
            else:
                status._unpack()
                bytes = status.adapter_address[:6]
                if len(bytes) != 6:
                    pass
                else:
                    mac = int.from_bytes(bytes, 'big')
                    if _is_universal(mac):
                        return mac
                    first_local_mac = first_local_mac or mac
    else:
        return first_local_mac or None


_generate_time_safe = _UuidCreate = None
_has_uuid_generate_time_safe = None
try:
    import _uuid
except ImportError:
    _uuid = None
else:

    def _load_system_functions--- This code section failed: ---

 L. 574         0  LOAD_GLOBAL              _has_uuid_generate_time_safe
                2  LOAD_CONST               None
                4  COMPARE_OP               is-not
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 575         8  LOAD_CONST               None
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L. 577        12  LOAD_CONST               False
               14  STORE_GLOBAL             _has_uuid_generate_time_safe

 L. 579        16  LOAD_GLOBAL              sys
               18  LOAD_ATTR                platform
               20  LOAD_STR                 'darwin'
               22  COMPARE_OP               ==
               24  POP_JUMP_IF_FALSE    56  'to 56'
               26  LOAD_GLOBAL              int
               28  LOAD_GLOBAL              os
               30  LOAD_METHOD              uname
               32  CALL_METHOD_0         0  ''
               34  LOAD_ATTR                release
               36  LOAD_METHOD              split
               38  LOAD_STR                 '.'
               40  CALL_METHOD_1         1  ''
               42  LOAD_CONST               0
               44  BINARY_SUBSCR    
               46  CALL_FUNCTION_1       1  ''
               48  LOAD_CONST               9
               50  COMPARE_OP               <
               52  POP_JUMP_IF_FALSE    56  'to 56'

 L. 587        54  JUMP_FORWARD         80  'to 80'
             56_0  COME_FROM            52  '52'
             56_1  COME_FROM            24  '24'

 L. 588        56  LOAD_GLOBAL              _uuid
               58  LOAD_CONST               None
               60  COMPARE_OP               is-not
               62  POP_JUMP_IF_FALSE    80  'to 80'

 L. 589        64  LOAD_GLOBAL              _uuid
               66  LOAD_ATTR                generate_time_safe
               68  STORE_GLOBAL             _generate_time_safe

 L. 590        70  LOAD_GLOBAL              _uuid
               72  LOAD_ATTR                has_uuid_generate_time_safe
               74  STORE_GLOBAL             _has_uuid_generate_time_safe

 L. 591        76  LOAD_CONST               None
               78  RETURN_VALUE     
             80_0  COME_FROM            62  '62'
             80_1  COME_FROM            54  '54'

 L. 593        80  SETUP_FINALLY       322  'to 322'

 L. 597        82  LOAD_CONST               0
               84  LOAD_CONST               None
               86  IMPORT_NAME              ctypes
               88  STORE_DEREF              'ctypes'

 L. 598        90  LOAD_CONST               0
               92  LOAD_CONST               None
               94  IMPORT_NAME_ATTR         ctypes.util
               96  STORE_DEREF              'ctypes'

 L. 602        98  LOAD_STR                 'uuid'
              100  BUILD_LIST_1          1 
              102  STORE_FAST               '_libnames'

 L. 603       104  LOAD_GLOBAL              sys
              106  LOAD_ATTR                platform
              108  LOAD_METHOD              startswith
              110  LOAD_STR                 'win'
              112  CALL_METHOD_1         1  ''
              114  POP_JUMP_IF_TRUE    126  'to 126'

 L. 604       116  LOAD_FAST                '_libnames'
              118  LOAD_METHOD              append
              120  LOAD_STR                 'c'
              122  CALL_METHOD_1         1  ''
              124  POP_TOP          
            126_0  COME_FROM           114  '114'

 L. 605       126  LOAD_FAST                '_libnames'
              128  GET_ITER         
            130_0  COME_FROM           266  '266'
            130_1  COME_FROM           232  '232'
            130_2  COME_FROM           222  '222'
            130_3  COME_FROM           174  '174'
              130  FOR_ITER            268  'to 268'
              132  STORE_FAST               'libname'

 L. 606       134  SETUP_FINALLY       158  'to 158'

 L. 607       136  LOAD_DEREF               'ctypes'
              138  LOAD_METHOD              CDLL
              140  LOAD_DEREF               'ctypes'
              142  LOAD_ATTR                util
              144  LOAD_METHOD              find_library
              146  LOAD_FAST                'libname'
              148  CALL_METHOD_1         1  ''
              150  CALL_METHOD_1         1  ''
              152  STORE_FAST               'lib'
              154  POP_BLOCK        
              156  JUMP_FORWARD        182  'to 182'
            158_0  COME_FROM_FINALLY   134  '134'

 L. 608       158  DUP_TOP          
              160  LOAD_GLOBAL              Exception
              162  COMPARE_OP               exception-match
              164  POP_JUMP_IF_FALSE   180  'to 180'
              166  POP_TOP          
              168  POP_TOP          
              170  POP_TOP          

 L. 609       172  POP_EXCEPT       
              174  JUMP_BACK           130  'to 130'
              176  POP_EXCEPT       
              178  JUMP_FORWARD        182  'to 182'
            180_0  COME_FROM           164  '164'
              180  END_FINALLY      
            182_0  COME_FROM           178  '178'
            182_1  COME_FROM           156  '156'

 L. 611       182  LOAD_GLOBAL              hasattr
              184  LOAD_FAST                'lib'
              186  LOAD_STR                 'uuid_generate_time_safe'
              188  CALL_FUNCTION_2       2  ''
              190  POP_JUMP_IF_FALSE   224  'to 224'

 L. 612       192  LOAD_FAST                'lib'
              194  LOAD_ATTR                uuid_generate_time_safe
              196  STORE_DEREF              '_uuid_generate_time_safe'

 L. 614       198  LOAD_CLOSURE             '_uuid_generate_time_safe'
              200  LOAD_CLOSURE             'ctypes'
              202  BUILD_TUPLE_2         2 
              204  LOAD_CODE                <code_object _generate_time_safe>
              206  LOAD_STR                 '_generate_time_safe'
              208  MAKE_FUNCTION_8          'closure'
              210  STORE_GLOBAL             _generate_time_safe

 L. 618       212  LOAD_CONST               True
              214  STORE_GLOBAL             _has_uuid_generate_time_safe

 L. 619       216  POP_TOP          
          218_220  BREAK_LOOP          268  'to 268'
              222  JUMP_BACK           130  'to 130'
            224_0  COME_FROM           190  '190'

 L. 621       224  LOAD_GLOBAL              hasattr
              226  LOAD_FAST                'lib'
              228  LOAD_STR                 'uuid_generate_time'
              230  CALL_FUNCTION_2       2  ''
              232  POP_JUMP_IF_FALSE_BACK   130  'to 130'

 L. 622       234  LOAD_FAST                'lib'
              236  LOAD_ATTR                uuid_generate_time
              238  STORE_DEREF              '_uuid_generate_time'

 L. 624       240  LOAD_CONST               None
              242  LOAD_DEREF               '_uuid_generate_time'
              244  STORE_ATTR               restype

 L. 625       246  LOAD_CLOSURE             '_uuid_generate_time'
              248  LOAD_CLOSURE             'ctypes'
              250  BUILD_TUPLE_2         2 
              252  LOAD_CODE                <code_object _generate_time_safe>
              254  LOAD_STR                 '_generate_time_safe'
              256  MAKE_FUNCTION_8          'closure'
              258  STORE_GLOBAL             _generate_time_safe

 L. 629       260  POP_TOP          
          262_264  BREAK_LOOP          268  'to 268'
              266  JUMP_BACK           130  'to 130'
            268_0  COME_FROM           262  '262'
            268_1  COME_FROM           218  '218'
            268_2  COME_FROM           130  '130'

 L. 639       268  SETUP_FINALLY       282  'to 282'

 L. 640       270  LOAD_DEREF               'ctypes'
              272  LOAD_ATTR                windll
              274  LOAD_ATTR                rpcrt4
              276  STORE_FAST               'lib'
              278  POP_BLOCK        
              280  JUMP_FORWARD        298  'to 298'
            282_0  COME_FROM_FINALLY   268  '268'

 L. 641       282  POP_TOP          
              284  POP_TOP          
              286  POP_TOP          

 L. 642       288  LOAD_CONST               None
              290  STORE_FAST               'lib'
              292  POP_EXCEPT       
              294  JUMP_FORWARD        298  'to 298'
              296  END_FINALLY      
            298_0  COME_FROM           294  '294'
            298_1  COME_FROM           280  '280'

 L. 643       298  LOAD_GLOBAL              getattr
              300  LOAD_FAST                'lib'
              302  LOAD_STR                 'UuidCreateSequential'

 L. 644       304  LOAD_GLOBAL              getattr
              306  LOAD_FAST                'lib'
              308  LOAD_STR                 'UuidCreate'
              310  LOAD_CONST               None
              312  CALL_FUNCTION_3       3  ''

 L. 643       314  CALL_FUNCTION_3       3  ''
              316  STORE_GLOBAL             _UuidCreate
              318  POP_BLOCK        
              320  JUMP_FORWARD        384  'to 384'
            322_0  COME_FROM_FINALLY    80  '80'

 L. 646       322  DUP_TOP          
              324  LOAD_GLOBAL              Exception
              326  COMPARE_OP               exception-match
          328_330  POP_JUMP_IF_FALSE   382  'to 382'
              332  POP_TOP          
              334  STORE_FAST               'exc'
              336  POP_TOP          
              338  SETUP_FINALLY       370  'to 370'

 L. 647       340  LOAD_CONST               0
              342  LOAD_CONST               None
              344  IMPORT_NAME              warnings
              346  STORE_FAST               'warnings'

 L. 648       348  LOAD_FAST                'warnings'
              350  LOAD_METHOD              warn
              352  LOAD_STR                 'Could not find fallback ctypes uuid functions: '
              354  LOAD_FAST                'exc'
              356  FORMAT_VALUE          0  ''
              358  BUILD_STRING_2        2 

 L. 649       360  LOAD_GLOBAL              ImportWarning

 L. 648       362  CALL_METHOD_2         2  ''
              364  POP_TOP          
              366  POP_BLOCK        
              368  BEGIN_FINALLY    
            370_0  COME_FROM_FINALLY   338  '338'
              370  LOAD_CONST               None
              372  STORE_FAST               'exc'
              374  DELETE_FAST              'exc'
              376  END_FINALLY      
              378  POP_EXCEPT       
              380  JUMP_FORWARD        384  'to 384'
            382_0  COME_FROM           328  '328'
              382  END_FINALLY      
            384_0  COME_FROM           380  '380'
            384_1  COME_FROM           320  '320'

Parse error at or near `COME_FROM' instruction at offset 180_0


    def _unix_getnode():
        """Get the hardware address on Unix using the _uuid extension module
    or ctypes."""
        global _generate_time_safe
        _load_system_functions()
        uuid_time, _ = _generate_time_safe()
        return UUID(bytes=uuid_time).node


    def _windll_getnode():
        """Get the hardware address on Windows using ctypes."""
        global _UuidCreate
        import ctypes
        _load_system_functions()
        _buffer = ctypes.create_string_buffer(16)
        if _UuidCreate(_buffer) == 0:
            return UUID(bytes=(bytes_(_buffer.raw))).node


    def _random_getnode():
        """Get a random node ID."""
        import random
        return random.getrandbits(48) | 1099511627776


    if _LINUX:
        _OS_GETTERS = [
         _ip_getnode, _ifconfig_getnode]
    elif _DARWIN:
        _OS_GETTERS = [
         _ifconfig_getnode, _arp_getnode, _netstat_getnode]
    elif _WINDOWS:
        _OS_GETTERS = [
         _netbios_getnode, _ipconfig_getnode]
    elif _AIX:
        _OS_GETTERS = [
         _netstat_getnode]
    else:
        _OS_GETTERS = [
         _ifconfig_getnode, _ip_getnode, _arp_getnode,
         _netstat_getnode, _lanscan_getnode]
    if os.name == 'posix':
        _GETTERS = [
         _unix_getnode] + _OS_GETTERS
    elif os.name == 'nt':
        _GETTERS = [
         _windll_getnode] + _OS_GETTERS
    else:
        _GETTERS = _OS_GETTERS
    _node = None

    def getnode--- This code section failed: ---

 L. 718         0  LOAD_GLOBAL              _node
                2  LOAD_CONST               None
                4  COMPARE_OP               is-not
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 719         8  LOAD_GLOBAL              _node
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L. 721        12  LOAD_GLOBAL              _GETTERS
               14  LOAD_GLOBAL              _random_getnode
               16  BUILD_LIST_1          1 
               18  BINARY_ADD       
               20  GET_ITER         
             22_0  COME_FROM            94  '94'
             22_1  COME_FROM            84  '84'
             22_2  COME_FROM            78  '78'
             22_3  COME_FROM            60  '60'
             22_4  COME_FROM            46  '46'
               22  FOR_ITER             96  'to 96'
               24  STORE_FAST               'getter'

 L. 722        26  SETUP_FINALLY        38  'to 38'

 L. 723        28  LOAD_FAST                'getter'
               30  CALL_FUNCTION_0       0  ''
               32  STORE_GLOBAL             _node
               34  POP_BLOCK        
               36  JUMP_FORWARD         54  'to 54'
             38_0  COME_FROM_FINALLY    26  '26'

 L. 724        38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          

 L. 725        44  POP_EXCEPT       
               46  JUMP_BACK            22  'to 22'
               48  POP_EXCEPT       
               50  JUMP_FORWARD         54  'to 54'
               52  END_FINALLY      
             54_0  COME_FROM            50  '50'
             54_1  COME_FROM            36  '36'

 L. 726        54  LOAD_GLOBAL              _node
               56  LOAD_CONST               None
               58  COMPARE_OP               is-not
               60  POP_JUMP_IF_FALSE_BACK    22  'to 22'
               62  LOAD_CONST               0
               64  LOAD_GLOBAL              _node
               66  DUP_TOP          
               68  ROT_THREE        
               70  COMPARE_OP               <=
               72  POP_JUMP_IF_FALSE    82  'to 82'
               74  LOAD_CONST               281474976710656
               76  COMPARE_OP               <
               78  POP_JUMP_IF_FALSE_BACK    22  'to 22'
               80  JUMP_FORWARD         86  'to 86'
             82_0  COME_FROM            72  '72'
               82  POP_TOP          
               84  JUMP_BACK            22  'to 22'
             86_0  COME_FROM            80  '80'

 L. 727        86  LOAD_GLOBAL              _node
               88  ROT_TWO          
               90  POP_TOP          
               92  RETURN_VALUE     
               94  JUMP_BACK            22  'to 22'
             96_0  COME_FROM            22  '22'

 L. 728        96  LOAD_CONST               False
               98  POP_JUMP_IF_TRUE    114  'to 114'
              100  LOAD_ASSERT              AssertionError
              102  LOAD_STR                 '_random_getnode() returned invalid value: {}'
              104  LOAD_METHOD              format
              106  LOAD_GLOBAL              _node
              108  CALL_METHOD_1         1  ''
              110  CALL_FUNCTION_1       1  ''
              112  RAISE_VARARGS_1       1  'exception instance'
            114_0  COME_FROM            98  '98'

Parse error at or near `JUMP_BACK' instruction at offset 46


    _last_timestamp = None

    def uuid1(node=None, clock_seq=None):
        """Generate a UUID from a host ID, sequence number, and the current time.
    If 'node' is not given, getnode() is used to obtain the hardware
    address.  If 'clock_seq' is given, it is used as the sequence number;
    otherwise a random 14-bit sequence number is chosen."""
        global _last_timestamp
        _load_system_functions()
        if _generate_time_safe is not None:
            if node is clock_seq is None:
                uuid_time, safely_generated = _generate_time_safe()
                try:
                    is_safe = SafeUUID(safely_generated)
                except ValueError:
                    is_safe = SafeUUID.unknown
                else:
                    return UUID(bytes=uuid_time, is_safe=is_safe)
                import time
                nanoseconds = time.time_ns()
                timestamp = nanoseconds // 100 + 122192928000000000
                if _last_timestamp is not None:
                    if timestamp <= _last_timestamp:
                        timestamp = _last_timestamp + 1
                _last_timestamp = timestamp
                if clock_seq is None:
                    import random
                    clock_seq = random.getrandbits(14)
                time_low = timestamp & 4294967295
                time_mid = timestamp >> 32 & 65535
                time_hi_version = timestamp >> 48 & 4095
                clock_seq_low = clock_seq & 255
                clock_seq_hi_variant = clock_seq >> 8 & 63
                if node is None:
                    node = getnode()
            return UUID(fields=(time_low, time_mid, time_hi_version,
             clock_seq_hi_variant, clock_seq_low, node),
              version=1)


    def uuid3(namespace, name):
        """Generate a UUID from the MD5 hash of a namespace UUID and a name."""
        from hashlib import md5
        hash = md5(namespace.bytes + bytes(name, 'utf-8')).digest()
        return UUID(bytes=(hash[:16]), version=3)


    def uuid4():
        """Generate a random UUID."""
        return UUID(bytes=(os.urandom(16)), version=4)


    def uuid5(namespace, name):
        """Generate a UUID from the SHA-1 hash of a namespace UUID and a name."""
        from hashlib import sha1
        hash = sha1(namespace.bytes + bytes(name, 'utf-8')).digest()
        return UUID(bytes=(hash[:16]), version=5)


    NAMESPACE_DNS = UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')
    NAMESPACE_URL = UUID('6ba7b811-9dad-11d1-80b4-00c04fd430c8')
    NAMESPACE_OID = UUID('6ba7b812-9dad-11d1-80b4-00c04fd430c8')
    NAMESPACE_X500 = UUID('6ba7b814-9dad-11d1-80b4-00c04fd430c8')
# global _has_uuid_generate_time_safe ## Warning: Unused global
# global _node ## Warning: Unused global