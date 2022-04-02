# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\selenium\webdriver\common\utils.py
"""
The Utils methods.
"""
import socket
from selenium.webdriver.common.keys import Keys
try:
    basestring
except NameError:
    basestring = str
else:

    def free_port():
        """
    Determines a free port using sockets.
    """
        free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        free_socket.bind(('0.0.0.0', 0))
        free_socket.listen(5)
        port = free_socket.getsockname()[1]
        free_socket.close()
        return port


    def find_connectable_ip(host, port=None):
        """Resolve a hostname to an IP, preferring IPv4 addresses.

    We prefer IPv4 so that we don't change behavior from previous IPv4-only
    implementations, and because some drivers (e.g., FirefoxDriver) do not
    support IPv6 connections.

    If the optional port number is provided, only IPs that listen on the given
    port are considered.

    :Args:
        - host - A hostname.
        - port - Optional port number.

    :Returns:
        A single IP address, as a string. If any IPv4 address is found, one is
        returned. Otherwise, if any IPv6 address is found, one is returned. If
        neither, then None is returned.

    """
        try:
            addrinfos = socket.getaddrinfo(host, None)
        except socket.gaierror:
            return
        else:
            ip = None
            for family, _, _, _, sockaddr in addrinfos:
                connectable = True
                if port:
                    connectable = is_connectable(port, sockaddr[0])
                if connectable:
                    if family == socket.AF_INET:
                        return sockaddr[0]
                if connectable:
                    if not ip:
                        if family == socket.AF_INET6:
                            ip = sockaddr[0]
            else:
                return ip


    def join_host_port(host, port):
        """Joins a hostname and port together.

    This is a minimal implementation intended to cope with IPv6 literals. For
    example, _join_host_port('::1', 80) == '[::1]:80'.

    :Args:
        - host - A hostname.
        - port - An integer port.

    """
        if ':' in host:
            if not host.startswith('['):
                return '[%s]:%d' % (host, port)
            return '%s:%d' % (host, port)


    def is_connectable(port, host='localhost'):
        """
    Tries to connect to the server at port to see if it is running.

    :Args:
     - port - The port to connect.
    """
        socket_ = None
        try:
            try:
                socket_ = socket.create_connection((host, port), 1)
                result = True
            except socket.error:
                result = False

        finally:
            if socket_:
                socket_.close()

        return result


    def is_url_connectable--- This code section failed: ---

 L. 124         0  SETUP_FINALLY        18  'to 18'

 L. 125         2  LOAD_CONST               0
                4  LOAD_CONST               ('request',)
                6  IMPORT_NAME              urllib
                8  IMPORT_FROM              request
               10  STORE_FAST               'url_request'
               12  POP_TOP          
               14  POP_BLOCK        
               16  JUMP_FORWARD         46  'to 46'
             18_0  COME_FROM_FINALLY     0  '0'

 L. 126        18  DUP_TOP          
               20  LOAD_GLOBAL              ImportError
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    44  'to 44'
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 127        32  LOAD_CONST               0
               34  LOAD_CONST               None
               36  IMPORT_NAME              urllib2
               38  STORE_FAST               'url_request'
               40  POP_EXCEPT       
               42  JUMP_FORWARD         46  'to 46'
             44_0  COME_FROM            24  '24'
               44  END_FINALLY      
             46_0  COME_FROM            42  '42'
             46_1  COME_FROM            16  '16'

 L. 129        46  SETUP_FINALLY        90  'to 90'

 L. 130        48  LOAD_FAST                'url_request'
               50  LOAD_METHOD              urlopen
               52  LOAD_STR                 'http://127.0.0.1:%s/status'
               54  LOAD_FAST                'port'
               56  BINARY_MODULO    
               58  CALL_METHOD_1         1  ''
               60  STORE_FAST               'res'

 L. 131        62  LOAD_FAST                'res'
               64  LOAD_METHOD              getcode
               66  CALL_METHOD_0         0  ''
               68  LOAD_CONST               200
               70  COMPARE_OP               ==
               72  POP_JUMP_IF_FALSE    80  'to 80'

 L. 132        74  POP_BLOCK        
               76  LOAD_CONST               True
               78  RETURN_VALUE     
             80_0  COME_FROM            72  '72'

 L. 134        80  POP_BLOCK        
               82  LOAD_CONST               False
               84  RETURN_VALUE     
               86  POP_BLOCK        
               88  JUMP_FORWARD        112  'to 112'
             90_0  COME_FROM_FINALLY    46  '46'

 L. 135        90  DUP_TOP          
               92  LOAD_GLOBAL              Exception
               94  COMPARE_OP               exception-match
               96  POP_JUMP_IF_FALSE   110  'to 110'
               98  POP_TOP          
              100  POP_TOP          
              102  POP_TOP          

 L. 136       104  POP_EXCEPT       
              106  LOAD_CONST               False
              108  RETURN_VALUE     
            110_0  COME_FROM            96  '96'
              110  END_FINALLY      
            112_0  COME_FROM            88  '88'

Parse error at or near `LOAD_CONST' instruction at offset 76


    def keys_to_typing(value):
        """Processes the values that will be typed in the element."""
        typing = []
        for val in value:
            if isinstance(val, Keys):
                typing.append(val)
            else:
                if isinstance(val, int):
                    val = str(val)
                    for i in range(len(val)):
                        typing.append(val[i])

                for i in range(len(val)):
                    typing.append(val[i])

        else:
            return typing