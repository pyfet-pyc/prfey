# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: jeepney\auth.py
from binascii import hexlify
import os

def make_auth_external() -> bytes:
    """Prepare an AUTH command line with the current effective user ID.

    This is the preferred authentication method for typical D-Bus connections
    over a Unix domain socket.
    """
    hex_uid = hexlify(str(os.geteuid()).encode('ascii'))
    return b'AUTH EXTERNAL %b\r\n' % hex_uid


def make_auth_anonymous() -> bytes:
    """Format an AUTH command line for the ANONYMOUS mechanism

    Jeepney's higher-level wrappers don't currently use this mechanism,
    but third-party code may choose to.

    See <https://tools.ietf.org/html/rfc4505> for details.
    """
    from . import __version__
    trace = hexlify(('Jeepney %s' % __version__).encode('ascii'))
    return b'AUTH ANONYMOUS %s\r\n' % trace


BEGIN = b'BEGIN\r\n'

class AuthenticationError(ValueError):
    __doc__ = 'Raised by integration code when DBus authentication fails'

    def __init__(self, data):
        self.data = data

    def __str__(self):
        return 'Authentication failed. Bus sent: %r' % self.data


class SASLParser:
    __doc__ = 'Parse authentication messages received'

    def __init__(self):
        self.buffer = b''
        self.authenticated = False
        self.error = None

    def process_line(self, line):
        if line.startswith(b'OK '):
            self.authenticated = True
        else:
            self.error = line

    def feed--- This code section failed: ---

 L.  50         0  LOAD_FAST                'self'
                2  DUP_TOP          
                4  LOAD_ATTR                buffer
                6  LOAD_FAST                'data'
                8  INPLACE_ADD      
               10  ROT_TWO          
               12  STORE_ATTR               buffer

 L.  51        14  LOAD_CONST               b'\r\n'
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                buffer
               20  <118>                 0  ''
               22  POP_JUMP_IF_FALSE    62  'to 62'
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                authenticated
               28  POP_JUMP_IF_TRUE     62  'to 62'

 L.  52        30  LOAD_FAST                'self'
               32  LOAD_ATTR                buffer
               34  LOAD_METHOD              split
               36  LOAD_CONST               b'\r\n'
               38  LOAD_CONST               1
               40  CALL_METHOD_2         2  ''
               42  UNPACK_SEQUENCE_2     2 
               44  STORE_FAST               'line'
               46  LOAD_FAST                'self'
               48  STORE_ATTR               buffer

 L.  53        50  LOAD_FAST                'self'
               52  LOAD_METHOD              process_line
               54  LOAD_FAST                'line'
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          
               60  JUMP_BACK            14  'to 14'
             62_0  COME_FROM            28  '28'
             62_1  COME_FROM            22  '22'

Parse error at or near `<118>' instruction at offset 20