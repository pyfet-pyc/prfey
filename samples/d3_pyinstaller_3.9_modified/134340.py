# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: aiohttp\tcp_helpers.py
"""Helper methods to tune a TCP connection"""
import asyncio, socket
from contextlib import suppress
from typing import Optional
__all__ = ('tcp_keepalive', 'tcp_nodelay')
if hasattr(socket, 'SO_KEEPALIVE'):

    def tcp_keepalive--- This code section failed: ---

 L.  14         0  LOAD_FAST                'transport'
                2  LOAD_METHOD              get_extra_info
                4  LOAD_STR                 'socket'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'sock'

 L.  15        10  LOAD_FAST                'sock'
               12  LOAD_CONST               None
               14  <117>                 1  ''
               16  POP_JUMP_IF_FALSE    36  'to 36'

 L.  16        18  LOAD_FAST                'sock'
               20  LOAD_METHOD              setsockopt
               22  LOAD_GLOBAL              socket
               24  LOAD_ATTR                SOL_SOCKET
               26  LOAD_GLOBAL              socket
               28  LOAD_ATTR                SO_KEEPALIVE
               30  LOAD_CONST               1
               32  CALL_METHOD_3         3  ''
               34  POP_TOP          
             36_0  COME_FROM            16  '16'

Parse error at or near `<117>' instruction at offset 14


else:

    def tcp_keepalive(transport: asyncio.Transport) -> None:
        pass


def tcp_nodelay--- This code section failed: ---

 L.  26         0  LOAD_FAST                'transport'
                2  LOAD_METHOD              get_extra_info
                4  LOAD_STR                 'socket'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'sock'

 L.  28        10  LOAD_FAST                'sock'
               12  LOAD_CONST               None
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    22  'to 22'

 L.  29        18  LOAD_CONST               None
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L.  31        22  LOAD_FAST                'sock'
               24  LOAD_ATTR                family
               26  LOAD_GLOBAL              socket
               28  LOAD_ATTR                AF_INET
               30  LOAD_GLOBAL              socket
               32  LOAD_ATTR                AF_INET6
               34  BUILD_TUPLE_2         2 
               36  <118>                 1  ''
               38  POP_JUMP_IF_FALSE    44  'to 44'

 L.  32        40  LOAD_CONST               None
               42  RETURN_VALUE     
             44_0  COME_FROM            38  '38'

 L.  34        44  LOAD_GLOBAL              bool
               46  LOAD_FAST                'value'
               48  CALL_FUNCTION_1       1  ''
               50  STORE_FAST               'value'

 L.  37        52  LOAD_GLOBAL              suppress
               54  LOAD_GLOBAL              OSError
               56  CALL_FUNCTION_1       1  ''
               58  SETUP_WITH           94  'to 94'
               60  POP_TOP          

 L.  38        62  LOAD_FAST                'sock'
               64  LOAD_METHOD              setsockopt
               66  LOAD_GLOBAL              socket
               68  LOAD_ATTR                IPPROTO_TCP
               70  LOAD_GLOBAL              socket
               72  LOAD_ATTR                TCP_NODELAY
               74  LOAD_FAST                'value'
               76  CALL_METHOD_3         3  ''
               78  POP_TOP          
               80  POP_BLOCK        
               82  LOAD_CONST               None
               84  DUP_TOP          
               86  DUP_TOP          
               88  CALL_FUNCTION_3       3  ''
               90  POP_TOP          
               92  JUMP_FORWARD        110  'to 110'
             94_0  COME_FROM_WITH       58  '58'
               94  <49>             
               96  POP_JUMP_IF_TRUE    100  'to 100'
               98  <48>             
            100_0  COME_FROM            96  '96'
              100  POP_TOP          
              102  POP_TOP          
              104  POP_TOP          
              106  POP_EXCEPT       
              108  POP_TOP          
            110_0  COME_FROM            92  '92'

Parse error at or near `<117>' instruction at offset 14