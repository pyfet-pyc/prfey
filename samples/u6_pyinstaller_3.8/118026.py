# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\dns\inet.py
"""Generic Internet address helper functions."""
import socket, dns.ipv4, dns.ipv6
from ._compat import maybe_ord
AF_INET = socket.AF_INET
try:
    AF_INET6 = socket.AF_INET6
except AttributeError:
    AF_INET6 = 9999
else:

    def inet_pton(family, text):
        """Convert the textual form of a network address into its binary form.

    *family* is an ``int``, the address family.

    *text* is a ``text``, the textual address.

    Raises ``NotImplementedError`` if the address family specified is not
    implemented.

    Returns a ``binary``.
    """
        if family == AF_INET:
            return dns.ipv4.inet_aton(text)
        if family == AF_INET6:
            return dns.ipv6.inet_aton(text)
        raise NotImplementedError


    def inet_ntop(family, address):
        """Convert the binary form of a network address into its textual form.

    *family* is an ``int``, the address family.

    *address* is a ``binary``, the network address in binary form.

    Raises ``NotImplementedError`` if the address family specified is not
    implemented.

    Returns a ``text``.
    """
        if family == AF_INET:
            return dns.ipv4.inet_ntoa(address)
        if family == AF_INET6:
            return dns.ipv6.inet_ntoa(address)
        raise NotImplementedError


    def af_for_address--- This code section failed: ---

 L.  94         0  SETUP_FINALLY        20  'to 20'

 L.  95         2  LOAD_GLOBAL              dns
                4  LOAD_ATTR                ipv4
                6  LOAD_METHOD              inet_aton
                8  LOAD_FAST                'text'
               10  CALL_METHOD_1         1  ''
               12  POP_TOP          

 L.  96        14  LOAD_GLOBAL              AF_INET
               16  POP_BLOCK        
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     0  '0'

 L.  97        20  DUP_TOP          
               22  LOAD_GLOBAL              Exception
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    78  'to 78'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L.  98        34  SETUP_FINALLY        58  'to 58'

 L.  99        36  LOAD_GLOBAL              dns
               38  LOAD_ATTR                ipv6
               40  LOAD_METHOD              inet_aton
               42  LOAD_FAST                'text'
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          

 L. 100        48  LOAD_GLOBAL              AF_INET6
               50  POP_BLOCK        
               52  ROT_FOUR         
               54  POP_EXCEPT       
               56  RETURN_VALUE     
             58_0  COME_FROM_FINALLY    34  '34'

 L. 101        58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          

 L. 102        64  LOAD_GLOBAL              ValueError
               66  RAISE_VARARGS_1       1  'exception instance'
               68  POP_EXCEPT       
               70  JUMP_FORWARD         74  'to 74'
               72  END_FINALLY      
             74_0  COME_FROM            70  '70'
               74  POP_EXCEPT       
               76  JUMP_FORWARD         80  'to 80'
             78_0  COME_FROM            26  '26'
               78  END_FINALLY      
             80_0  COME_FROM            76  '76'

Parse error at or near `POP_TOP' instruction at offset 30


    def is_multicast--- This code section failed: ---

 L. 116         0  SETUP_FINALLY        40  'to 40'

 L. 117         2  LOAD_GLOBAL              maybe_ord
                4  LOAD_GLOBAL              dns
                6  LOAD_ATTR                ipv4
                8  LOAD_METHOD              inet_aton
               10  LOAD_FAST                'text'
               12  CALL_METHOD_1         1  ''
               14  LOAD_CONST               0
               16  BINARY_SUBSCR    
               18  CALL_FUNCTION_1       1  ''
               20  STORE_FAST               'first'

 L. 118        22  LOAD_FAST                'first'
               24  LOAD_CONST               224
               26  COMPARE_OP               >=
               28  JUMP_IF_FALSE_OR_POP    36  'to 36'
               30  LOAD_FAST                'first'
               32  LOAD_CONST               239
               34  COMPARE_OP               <=
             36_0  COME_FROM            28  '28'
               36  POP_BLOCK        
               38  RETURN_VALUE     
             40_0  COME_FROM_FINALLY     0  '0'

 L. 119        40  DUP_TOP          
               42  LOAD_GLOBAL              Exception
               44  COMPARE_OP               exception-match
               46  POP_JUMP_IF_FALSE   118  'to 118'
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L. 120        54  SETUP_FINALLY        90  'to 90'

 L. 121        56  LOAD_GLOBAL              maybe_ord
               58  LOAD_GLOBAL              dns
               60  LOAD_ATTR                ipv6
               62  LOAD_METHOD              inet_aton
               64  LOAD_FAST                'text'
               66  CALL_METHOD_1         1  ''
               68  LOAD_CONST               0
               70  BINARY_SUBSCR    
               72  CALL_FUNCTION_1       1  ''
               74  STORE_FAST               'first'

 L. 122        76  LOAD_FAST                'first'
               78  LOAD_CONST               255
               80  COMPARE_OP               ==
               82  POP_BLOCK        
               84  ROT_FOUR         
               86  POP_EXCEPT       
               88  RETURN_VALUE     
             90_0  COME_FROM_FINALLY    54  '54'

 L. 123        90  DUP_TOP          
               92  LOAD_GLOBAL              Exception
               94  COMPARE_OP               exception-match
               96  POP_JUMP_IF_FALSE   112  'to 112'
               98  POP_TOP          
              100  POP_TOP          
              102  POP_TOP          

 L. 124       104  LOAD_GLOBAL              ValueError
              106  RAISE_VARARGS_1       1  'exception instance'
              108  POP_EXCEPT       
              110  JUMP_FORWARD        114  'to 114'
            112_0  COME_FROM            96  '96'
              112  END_FINALLY      
            114_0  COME_FROM           110  '110'
              114  POP_EXCEPT       
              116  JUMP_FORWARD        120  'to 120'
            118_0  COME_FROM            46  '46'
              118  END_FINALLY      
            120_0  COME_FROM           116  '116'

Parse error at or near `POP_TOP' instruction at offset 50