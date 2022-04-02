# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\requests\packages\urllib3\util\connection.py
import socket
try:
    from select import poll, POLLIN
except ImportError:
    poll = False
    try:
        from select import select
    except ImportError:
        select = False

else:

    def is_connection_dropped--- This code section failed: ---

 L.  22         0  LOAD_GLOBAL              getattr
                2  LOAD_FAST                'conn'
                4  LOAD_STR                 'sock'
                6  LOAD_CONST               False
                8  CALL_FUNCTION_3       3  ''
               10  STORE_FAST               'sock'

 L.  23        12  LOAD_FAST                'sock'
               14  LOAD_CONST               False
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    24  'to 24'

 L.  24        20  LOAD_CONST               False
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L.  25        24  LOAD_FAST                'sock'
               26  LOAD_CONST               None
               28  COMPARE_OP               is
               30  POP_JUMP_IF_FALSE    36  'to 36'

 L.  26        32  LOAD_CONST               True
               34  RETURN_VALUE     
             36_0  COME_FROM            30  '30'

 L.  28        36  LOAD_GLOBAL              poll
               38  POP_JUMP_IF_TRUE     96  'to 96'

 L.  29        40  LOAD_GLOBAL              select
               42  POP_JUMP_IF_TRUE     48  'to 48'

 L.  30        44  LOAD_CONST               False
               46  RETURN_VALUE     
             48_0  COME_FROM            42  '42'

 L.  32        48  SETUP_FINALLY        72  'to 72'

 L.  33        50  LOAD_GLOBAL              select
               52  LOAD_FAST                'sock'
               54  BUILD_LIST_1          1 
               56  BUILD_LIST_0          0 
               58  BUILD_LIST_0          0 
               60  LOAD_CONST               0.0
               62  CALL_FUNCTION_4       4  ''
               64  LOAD_CONST               0
               66  BINARY_SUBSCR    
               68  POP_BLOCK        
               70  RETURN_VALUE     
             72_0  COME_FROM_FINALLY    48  '48'

 L.  34        72  DUP_TOP          
               74  LOAD_GLOBAL              socket
               76  LOAD_ATTR                error
               78  COMPARE_OP               exception-match
               80  POP_JUMP_IF_FALSE    94  'to 94'
               82  POP_TOP          
               84  POP_TOP          
               86  POP_TOP          

 L.  35        88  POP_EXCEPT       
               90  LOAD_CONST               True
               92  RETURN_VALUE     
             94_0  COME_FROM            80  '80'
               94  END_FINALLY      
             96_0  COME_FROM            38  '38'

 L.  38        96  LOAD_GLOBAL              poll
               98  CALL_FUNCTION_0       0  ''
              100  STORE_FAST               'p'

 L.  39       102  LOAD_FAST                'p'
              104  LOAD_METHOD              register
              106  LOAD_FAST                'sock'
              108  LOAD_GLOBAL              POLLIN
              110  CALL_METHOD_2         2  ''
              112  POP_TOP          

 L.  40       114  LOAD_FAST                'p'
              116  LOAD_METHOD              poll
              118  LOAD_CONST               0.0
              120  CALL_METHOD_1         1  ''
              122  GET_ITER         
            124_0  COME_FROM           142  '142'
              124  FOR_ITER            152  'to 152'
              126  UNPACK_SEQUENCE_2     2 
              128  STORE_FAST               'fno'
              130  STORE_FAST               'ev'

 L.  41       132  LOAD_FAST                'fno'
              134  LOAD_FAST                'sock'
              136  LOAD_METHOD              fileno
              138  CALL_METHOD_0         0  ''
              140  COMPARE_OP               ==
              142  POP_JUMP_IF_FALSE   124  'to 124'

 L.  43       144  POP_TOP          
              146  LOAD_CONST               True
              148  RETURN_VALUE     
              150  JUMP_BACK           124  'to 124'

Parse error at or near `POP_TOP' instruction at offset 84


    def create_connection--- This code section failed: ---

 L.  62         0  LOAD_FAST                'address'
                2  UNPACK_SEQUENCE_2     2 
                4  STORE_FAST               'host'
                6  STORE_FAST               'port'

 L.  63         8  LOAD_CONST               None
               10  STORE_FAST               'err'

 L.  64        12  LOAD_GLOBAL              socket
               14  LOAD_METHOD              getaddrinfo
               16  LOAD_FAST                'host'
               18  LOAD_FAST                'port'
               20  LOAD_CONST               0
               22  LOAD_GLOBAL              socket
               24  LOAD_ATTR                SOCK_STREAM
               26  CALL_METHOD_4         4  ''
               28  GET_ITER         
               30  FOR_ITER            194  'to 194'
               32  STORE_FAST               'res'

 L.  65        34  LOAD_FAST                'res'
               36  UNPACK_SEQUENCE_5     5 
               38  STORE_FAST               'af'
               40  STORE_FAST               'socktype'
               42  STORE_FAST               'proto'
               44  STORE_FAST               'canonname'
               46  STORE_FAST               'sa'

 L.  66        48  LOAD_CONST               None
               50  STORE_FAST               'sock'

 L.  67        52  SETUP_FINALLY       132  'to 132'

 L.  68        54  LOAD_GLOBAL              socket
               56  LOAD_METHOD              socket
               58  LOAD_FAST                'af'
               60  LOAD_FAST                'socktype'
               62  LOAD_FAST                'proto'
               64  CALL_METHOD_3         3  ''
               66  STORE_FAST               'sock'

 L.  72        68  LOAD_GLOBAL              _set_socket_options
               70  LOAD_FAST                'sock'
               72  LOAD_FAST                'socket_options'
               74  CALL_FUNCTION_2       2  ''
               76  POP_TOP          

 L.  74        78  LOAD_FAST                'timeout'
               80  LOAD_GLOBAL              socket
               82  LOAD_ATTR                _GLOBAL_DEFAULT_TIMEOUT
               84  COMPARE_OP               is-not
               86  POP_JUMP_IF_FALSE    98  'to 98'

 L.  75        88  LOAD_FAST                'sock'
               90  LOAD_METHOD              settimeout
               92  LOAD_FAST                'timeout'
               94  CALL_METHOD_1         1  ''
               96  POP_TOP          
             98_0  COME_FROM            86  '86'

 L.  76        98  LOAD_FAST                'source_address'
              100  POP_JUMP_IF_FALSE   112  'to 112'

 L.  77       102  LOAD_FAST                'sock'
              104  LOAD_METHOD              bind
              106  LOAD_FAST                'source_address'
              108  CALL_METHOD_1         1  ''
              110  POP_TOP          
            112_0  COME_FROM           100  '100'

 L.  78       112  LOAD_FAST                'sock'
              114  LOAD_METHOD              connect
              116  LOAD_FAST                'sa'
              118  CALL_METHOD_1         1  ''
              120  POP_TOP          

 L.  79       122  LOAD_FAST                'sock'
              124  POP_BLOCK        
              126  ROT_TWO          
              128  POP_TOP          
              130  RETURN_VALUE     
            132_0  COME_FROM_FINALLY    52  '52'

 L.  81       132  DUP_TOP          
              134  LOAD_GLOBAL              socket
              136  LOAD_ATTR                error
              138  COMPARE_OP               exception-match
              140  POP_JUMP_IF_FALSE   190  'to 190'
              142  POP_TOP          
              144  STORE_FAST               '_'
              146  POP_TOP          
              148  SETUP_FINALLY       178  'to 178'

 L.  82       150  LOAD_FAST                '_'
              152  STORE_FAST               'err'

 L.  83       154  LOAD_FAST                'sock'
              156  LOAD_CONST               None
              158  COMPARE_OP               is-not
              160  POP_JUMP_IF_FALSE   174  'to 174'

 L.  84       162  LOAD_FAST                'sock'
              164  LOAD_METHOD              close
              166  CALL_METHOD_0         0  ''
              168  POP_TOP          

 L.  85       170  LOAD_CONST               None
              172  STORE_FAST               'sock'
            174_0  COME_FROM           160  '160'
              174  POP_BLOCK        
              176  BEGIN_FINALLY    
            178_0  COME_FROM_FINALLY   148  '148'
              178  LOAD_CONST               None
              180  STORE_FAST               '_'
              182  DELETE_FAST              '_'
              184  END_FINALLY      
              186  POP_EXCEPT       
              188  JUMP_BACK            30  'to 30'
            190_0  COME_FROM           140  '140'
              190  END_FINALLY      
              192  JUMP_BACK            30  'to 30'

 L.  87       194  LOAD_FAST                'err'
              196  LOAD_CONST               None
              198  COMPARE_OP               is-not
              200  POP_JUMP_IF_FALSE   208  'to 208'

 L.  88       202  LOAD_FAST                'err'
              204  RAISE_VARARGS_1       1  'exception instance'
              206  JUMP_FORWARD        218  'to 218'
            208_0  COME_FROM           200  '200'

 L.  90       208  LOAD_GLOBAL              socket
              210  LOAD_METHOD              error
              212  LOAD_STR                 'getaddrinfo returns an empty list'
              214  CALL_METHOD_1         1  ''
              216  RAISE_VARARGS_1       1  'exception instance'
            218_0  COME_FROM           206  '206'

Parse error at or near `ROT_TWO' instruction at offset 126


    def _set_socket_options(sock, options):
        if options is None:
            return
        for opt in options:
            (sock.setsockopt)(*opt)