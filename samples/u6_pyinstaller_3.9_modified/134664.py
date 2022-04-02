# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: jeepney\io\blocking.py
"""Synchronous IO wrappers around jeepney
"""
from collections import deque
from errno import ECONNRESET
import functools
from itertools import count
import os
from selectors import DefaultSelector, EVENT_READ
import socket, time
from typing import Optional
from jeepney import Parser, Message, MessageType, HeaderFields
from jeepney.auth import SASLParser, make_auth_external, BEGIN, AuthenticationError
from jeepney.bus import get_bus
from jeepney.wrappers import ProxyBase, unwrap_msg
from jeepney.routing import Router
from jeepney.bus_messages import message_bus
from .common import MessageFilters, FilterHandle, check_replyable

class _Future:

    def __init__(self):
        self._result = None

    def done(self):
        return bool(self._result)

    def set_exception(self, exception):
        self._result = (
         False, exception)

    def set_result(self, result):
        self._result = (
         True, result)

    def result(self):
        success, value = self._result
        if success:
            return value
        raise value


def timeout_to_deadline--- This code section failed: ---

 L.  43         0  LOAD_FAST                'timeout'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    20  'to 20'

 L.  44         8  LOAD_GLOBAL              time
               10  LOAD_METHOD              monotonic
               12  CALL_METHOD_0         0  ''
               14  LOAD_FAST                'timeout'
               16  BINARY_ADD       
               18  RETURN_VALUE     
             20_0  COME_FROM             6  '6'

Parse error at or near `None' instruction at offset -1


def deadline_to_timeout--- This code section failed: ---

 L.  48         0  LOAD_FAST                'deadline'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  POP_JUMP_IF_FALSE    20  'to 20'

 L.  49         8  LOAD_FAST                'deadline'
               10  LOAD_GLOBAL              time
               12  LOAD_METHOD              monotonic
               14  CALL_METHOD_0         0  ''
               16  BINARY_SUBTRACT  
               18  RETURN_VALUE     
             20_0  COME_FROM             6  '6'

Parse error at or near `None' instruction at offset -1


class DBusConnection:

    def __init__(self, sock):
        self.sock = sock
        self.parser = Parser()
        self.outgoing_serial = count(start=1)
        self.selector = DefaultSelector()
        self.select_key = self.selector.register(sock, EVENT_READ)
        self._unwrap_reply = False
        self.router = Router(_Future)
        self._filters = MessageFilters()
        self.bus_proxy = Proxy(message_bus, self)
        hello_reply = self.bus_proxy.Hello
        self.unique_name = hello_reply[0]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close
        return False

    def send--- This code section failed: ---

 L.  80         0  LOAD_FAST                'serial'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    18  'to 18'

 L.  81         8  LOAD_GLOBAL              next
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                outgoing_serial
               14  CALL_FUNCTION_1       1  ''
               16  STORE_FAST               'serial'
             18_0  COME_FROM             6  '6'

 L.  82        18  LOAD_FAST                'message'
               20  LOAD_ATTR                serialise
               22  LOAD_FAST                'serial'
               24  LOAD_CONST               ('serial',)
               26  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               28  STORE_FAST               'data'

 L.  83        30  LOAD_FAST                'self'
               32  LOAD_ATTR                sock
               34  LOAD_METHOD              sendall
               36  LOAD_FAST                'data'
               38  CALL_METHOD_1         1  ''
               40  POP_TOP          

Parse error at or near `None' instruction at offset -1

    send_message = send

    def receive--- This code section failed: ---

 L.  94         0  LOAD_GLOBAL              timeout_to_deadline
                2  LOAD_FAST                'timeout'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'deadline'

 L.  97         8  LOAD_FAST                'self'
               10  LOAD_ATTR                parser
               12  LOAD_METHOD              get_next_message
               14  CALL_METHOD_0         0  ''
               16  STORE_FAST               'msg'

 L.  98        18  LOAD_FAST                'msg'
               20  LOAD_CONST               None
               22  <117>                 1  ''
               24  POP_JUMP_IF_FALSE    30  'to 30'

 L.  99        26  LOAD_FAST                'msg'
               28  RETURN_VALUE     
             30_0  COME_FROM            24  '24'

 L. 101        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _read_some_data
               34  LOAD_GLOBAL              deadline_to_timeout
               36  LOAD_FAST                'deadline'
               38  CALL_FUNCTION_1       1  ''
               40  LOAD_CONST               ('timeout',)
               42  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               44  STORE_FAST               'b'

 L. 102        46  LOAD_FAST                'self'
               48  LOAD_ATTR                parser
               50  LOAD_METHOD              add_data
               52  LOAD_FAST                'b'
               54  CALL_METHOD_1         1  ''
               56  POP_TOP          
               58  JUMP_BACK             8  'to 8'

Parse error at or near `<117>' instruction at offset 22

    def _read_some_data(self, timeout=None):
        for key, ev in self.selector.selecttimeout:
            if key == self.select_key:
                return unwrap_read(self.sock.recv4096)
        else:
            raise TimeoutError

    def recv_messages(self, *, timeout=None):
        """Receive one message and apply filters

        See :meth:`filter`. Returns nothing.
        """
        msg = self.receive(timeout=timeout)
        self.router.incomingmsg
        for filter in self._filters.matchesmsg:
            filter.queue.appendmsg

    def send_and_get_reply--- This code section failed: ---

 L. 127         0  LOAD_GLOBAL              check_replyable
                2  LOAD_FAST                'message'
                4  CALL_FUNCTION_1       1  ''
                6  POP_TOP          

 L. 128         8  LOAD_GLOBAL              timeout_to_deadline
               10  LOAD_FAST                'timeout'
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'deadline'

 L. 130        16  LOAD_FAST                'unwrap'
               18  LOAD_CONST               None
               20  <117>                 0  ''
               22  POP_JUMP_IF_FALSE    30  'to 30'

 L. 131        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _unwrap_reply
               28  STORE_FAST               'unwrap'
             30_0  COME_FROM            22  '22'

 L. 133        30  LOAD_GLOBAL              next
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                outgoing_serial
               36  CALL_FUNCTION_1       1  ''
               38  STORE_FAST               'serial'

 L. 134        40  LOAD_FAST                'self'
               42  LOAD_ATTR                send_message
               44  LOAD_FAST                'message'
               46  LOAD_FAST                'serial'
               48  LOAD_CONST               ('serial',)
               50  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               52  POP_TOP          

 L. 136        54  LOAD_FAST                'self'
               56  LOAD_ATTR                receive
               58  LOAD_GLOBAL              deadline_to_timeout
               60  LOAD_FAST                'deadline'
               62  CALL_FUNCTION_1       1  ''
               64  LOAD_CONST               ('timeout',)
               66  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               68  STORE_FAST               'msg_in'

 L. 137        70  LOAD_FAST                'msg_in'
               72  LOAD_ATTR                header
               74  LOAD_ATTR                fields
               76  LOAD_METHOD              get
               78  LOAD_GLOBAL              HeaderFields
               80  LOAD_ATTR                reply_serial
               82  LOAD_CONST               -1
               84  CALL_METHOD_2         2  ''
               86  STORE_FAST               'reply_to'

 L. 138        88  LOAD_FAST                'reply_to'
               90  LOAD_FAST                'serial'
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE   112  'to 112'

 L. 139        96  LOAD_FAST                'unwrap'
               98  POP_JUMP_IF_FALSE   108  'to 108'

 L. 140       100  LOAD_GLOBAL              unwrap_msg
              102  LOAD_FAST                'msg_in'
              104  CALL_FUNCTION_1       1  ''
              106  RETURN_VALUE     
            108_0  COME_FROM            98  '98'

 L. 141       108  LOAD_FAST                'msg_in'
              110  RETURN_VALUE     
            112_0  COME_FROM            94  '94'

 L. 144       112  LOAD_FAST                'self'
              114  LOAD_ATTR                router
              116  LOAD_METHOD              incoming
              118  LOAD_FAST                'msg_in'
              120  CALL_METHOD_1         1  ''
              122  POP_TOP          

 L. 145       124  LOAD_FAST                'self'
              126  LOAD_ATTR                _filters
              128  LOAD_METHOD              matches
              130  LOAD_FAST                'msg_in'
              132  CALL_METHOD_1         1  ''
              134  GET_ITER         
              136  FOR_ITER            154  'to 154'
              138  STORE_FAST               'filter'

 L. 146       140  LOAD_FAST                'filter'
              142  LOAD_ATTR                queue
              144  LOAD_METHOD              append
              146  LOAD_FAST                'msg_in'
              148  CALL_METHOD_1         1  ''
              150  POP_TOP          
              152  JUMP_BACK           136  'to 136'
              154  JUMP_BACK            54  'to 54'

Parse error at or near `<117>' instruction at offset 20

    def filter(self, rule, *, queue: Optional[deque]=None, bufsize=1):
        """Create a filter for incoming messages

        Usage::

            with conn.filter(rule) as matches:
                # matches is a deque containing matched messages
                matching_msg = conn.recv_until_filtered(matches)

        :param jeepney.MatchRule rule: Catch messages matching this rule
        :param collections.deque queue: Matched messages will be added to this
        :param int bufsize: If no deque is passed in, create one with this size
        """
        return FilterHandle(self._filters, rule, queue or deque(maxlen=bufsize))

    def recv_until_filtered(self, queue, *, timeout=None) -> Message:
        """Process incoming messages until one is filtered into queue

        Pops the message from queue and returns it, or raises TimeoutError if
        the optional timeout expires. Without a timeout, this is equivalent to::

            while len(queue) == 0:
                conn.recv_messages()
            return queue.popleft()

        In the other I/O modules, there is no need for this, because messages
        are placed in queues by a separate task.

        :param collections.deque queue: A deque connected by :meth:`filter`
        :param float timeout: Maximum time to wait in seconds
        """
        deadline = timeout_to_deadline(timeout)
        while len(queue) == 0:
            self.recv_messages(timeout=(deadline_to_timeout(deadline)))

        return queue.popleft

    def close(self):
        """Close this connection"""
        self.selector.close
        self.sock.close


class Proxy(ProxyBase):
    __doc__ = 'A blocking proxy for calling D-Bus methods\n\n    You can call methods on the proxy object, such as ``bus_proxy.Hello()``\n    to make a method call over D-Bus and wait for a reply. It will either\n    return a tuple of returned data, or raise :exc:`.DBusErrorResponse`.\n    The methods available are defined by the message generator you wrap.\n\n    You can set a time limit on a call by passing ``_timeout=`` in the method\n    call, or set a default when creating the proxy. The ``_timeout`` argument\n    is not passed to the message generator.\n    All timeouts are in seconds, and :exc:`TimeoutErrror` is raised if it\n    expires before a reply arrives.\n\n    :param msggen: A message generator object\n    :param ~blocking.DBusConnection connection: Connection to send and receive messages\n    :param float timeout: Default seconds to wait for a reply, or None for no limit\n    '

    def __init__(self, msggen, connection, *, timeout=None):
        super().__init__msggen
        self._connection = connection
        self._timeout = timeout

    def __repr__--- This code section failed: ---

 L. 214         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _timeout
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'
               10  LOAD_STR                 ''
               12  JUMP_FORWARD         24  'to 24'
             14_0  COME_FROM             8  '8'
               14  LOAD_STR                 ', timeout='
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _timeout
               20  FORMAT_VALUE          0  ''
               22  BUILD_STRING_2        2 
             24_0  COME_FROM            12  '12'
               24  STORE_FAST               'extra'

 L. 215        26  LOAD_STR                 'Proxy('
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                _msggen
               32  FORMAT_VALUE          0  ''
               34  LOAD_STR                 ', '
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                _connection
               40  FORMAT_VALUE          0  ''
               42  LOAD_FAST                'extra'
               44  FORMAT_VALUE          0  ''
               46  LOAD_STR                 ')'
               48  BUILD_STRING_6        6 
               50  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _method_call(self, make_msg):

        @functools.wrapsmake_msg
        def inner--- This code section failed: ---

 L. 220         0  LOAD_FAST                'kwargs'
                2  LOAD_METHOD              pop
                4  LOAD_STR                 '_timeout'
                6  LOAD_DEREF               'self'
                8  LOAD_ATTR                _timeout
               10  CALL_METHOD_2         2  ''
               12  STORE_FAST               'timeout'

 L. 221        14  LOAD_DEREF               'make_msg'
               16  LOAD_FAST                'args'
               18  BUILD_MAP_0           0 
               20  LOAD_FAST                'kwargs'
               22  <164>                 1  ''
               24  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               26  STORE_FAST               'msg'

 L. 222        28  LOAD_FAST                'msg'
               30  LOAD_ATTR                header
               32  LOAD_ATTR                message_type
               34  LOAD_GLOBAL              MessageType
               36  LOAD_ATTR                method_call
               38  <117>                 0  ''
               40  POP_JUMP_IF_TRUE     46  'to 46'
               42  <74>             
               44  RAISE_VARARGS_1       1  'exception instance'
             46_0  COME_FROM            40  '40'

 L. 223        46  LOAD_DEREF               'self'
               48  LOAD_ATTR                _connection
               50  LOAD_ATTR                send_and_get_reply

 L. 224        52  LOAD_FAST                'msg'
               54  LOAD_FAST                'timeout'
               56  LOAD_CONST               True

 L. 223        58  LOAD_CONST               ('timeout', 'unwrap')
               60  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               62  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<164>' instruction at offset 22

        return inner


def unwrap_read(b):
    """Raise ConnectionResetError from an empty read.

    Sometimes the socket raises an error itself, sometimes it gives no data.
    I haven't worked out when it behaves each way.
    """
    if not b:
        raise ConnectionResetError(ECONNRESET, os.strerrorECONNRESET)
    return b


def open_dbus_connection(bus='SESSION') -> DBusConnection:
    """Connect to a D-Bus message bus"""
    bus_addr = get_bus(bus)
    sock = socket.socket(family=(socket.AF_UNIX))
    sock.connectbus_addr
    sock.sendall(b'\x00' + make_auth_external())
    auth_parser = SASLParser()
    while not auth_parser.authenticated:
        auth_parser.feedunwrap_read(sock.recv1024)
        if auth_parser.error:
            raise AuthenticationError(auth_parser.error)

    sock.sendallBEGIN
    conn = DBusConnection(sock)
    conn.parser.add_dataauth_parser.buffer
    return conn


if __name__ == '__main__':
    conn = open_dbus_connection()
    print('Unique name:', conn.unique_name)