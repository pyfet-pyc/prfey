# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: jeepney\bus.py
import os, re
_escape_pat = re.compile('%([0-9A-Fa-f]{2})')

def unescape(v):

    def repl(match):
        n = int((match.group(1)), base=16)
        return chr(n)

    return _escape_pat.sub(repl, v)


def parse_addresses(s):
    for addr in s.split(';'):
        transport, info = addr.split(':', 1)
        kv = {}
        for x in info.split(','):
            k, v = x.split('=', 1)
            kv[k] = unescape(v)
        else:
            yield (
             transport, kv)


SUPPORTED_TRANSPORTS = ('unix', )

def get_connectable_addresses--- This code section failed: ---

 L.  23         0  LOAD_GLOBAL              set
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'unsupported_transports'

 L.  24         6  LOAD_CONST               False
                8  STORE_FAST               'found'

 L.  25        10  LOAD_GLOBAL              parse_addresses
               12  LOAD_FAST                'addr'
               14  CALL_FUNCTION_1       1  ''
               16  GET_ITER         
             18_0  COME_FROM           104  '104'
             18_1  COME_FROM            88  '88'
             18_2  COME_FROM            80  '80'
             18_3  COME_FROM            52  '52'
             18_4  COME_FROM            44  '44'
               18  FOR_ITER            106  'to 106'
               20  UNPACK_SEQUENCE_2     2 
               22  STORE_FAST               'transport'
               24  STORE_FAST               'kv'

 L.  26        26  LOAD_FAST                'transport'
               28  LOAD_GLOBAL              SUPPORTED_TRANSPORTS
               30  <118>                 1  ''
               32  POP_JUMP_IF_FALSE    46  'to 46'

 L.  27        34  LOAD_FAST                'unsupported_transports'
               36  LOAD_METHOD              add
               38  LOAD_FAST                'transport'
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          
               44  JUMP_BACK            18  'to 18'
             46_0  COME_FROM            32  '32'

 L.  29        46  LOAD_FAST                'transport'
               48  LOAD_STR                 'unix'
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE_BACK    18  'to 18'

 L.  30        54  LOAD_STR                 'abstract'
               56  LOAD_FAST                'kv'
               58  <118>                 0  ''
               60  POP_JUMP_IF_FALSE    82  'to 82'

 L.  31        62  LOAD_STR                 '\x00'
               64  LOAD_FAST                'kv'
               66  LOAD_STR                 'abstract'
               68  BINARY_SUBSCR    
               70  BINARY_ADD       
               72  YIELD_VALUE      
               74  POP_TOP          

 L.  32        76  LOAD_CONST               True
               78  STORE_FAST               'found'
               80  JUMP_BACK            18  'to 18'
             82_0  COME_FROM            60  '60'

 L.  33        82  LOAD_STR                 'path'
               84  LOAD_FAST                'kv'
               86  <118>                 0  ''
               88  POP_JUMP_IF_FALSE_BACK    18  'to 18'

 L.  34        90  LOAD_FAST                'kv'
               92  LOAD_STR                 'path'
               94  BINARY_SUBSCR    
               96  YIELD_VALUE      
               98  POP_TOP          

 L.  35       100  LOAD_CONST               True
              102  STORE_FAST               'found'
              104  JUMP_BACK            18  'to 18'
            106_0  COME_FROM            18  '18'

 L.  37       106  LOAD_FAST                'found'
              108  POP_JUMP_IF_TRUE    126  'to 126'

 L.  38       110  LOAD_GLOBAL              RuntimeError
              112  LOAD_STR                 'DBus transports ({}) not supported. Supported: {}'
              114  LOAD_METHOD              format

 L.  39       116  LOAD_FAST                'unsupported_transports'
              118  LOAD_GLOBAL              SUPPORTED_TRANSPORTS

 L.  38       120  CALL_METHOD_2         2  ''
              122  CALL_FUNCTION_1       1  ''
              124  RAISE_VARARGS_1       1  'exception instance'
            126_0  COME_FROM           108  '108'

Parse error at or near `<118>' instruction at offset 30


def find_session_bus():
    addr = os.environ['DBUS_SESSION_BUS_ADDRESS']
    return next(get_connectable_addresses(addr))


def find_system_bus():
    addr = os.environ.get('DBUS_SYSTEM_BUS_ADDRESS', '') or 'unix:path=/var/run/dbus/system_bus_socket'
    return next(get_connectable_addresses(addr))


def get_bus(addr):
    if addr == 'SESSION':
        return find_session_bus()
    if addr == 'SYSTEM':
        return find_system_bus()
    return next(get_connectable_addresses(addr))


if __name__ == '__main__':
    print('System bus at:', find_system_bus())
    print('Session bus at:', find_session_bus())