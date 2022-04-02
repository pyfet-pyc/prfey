# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: jeepney\routing.py
from .low_level import MessageType, HeaderFields
from .wrappers import DBusErrorResponse

class Router:
    __doc__ = 'Routing for messages coming back to a client application.\n    \n    :param handle_factory: Constructor for an object like asyncio.Future,\n        with methods *set_result* and *set_exception*. Outgoing method call\n        messages will get a handle associated with them.\n    :param on_unhandled: Callback for messages not otherwise dispatched.\n    '

    def __init__(self, handle_factory, on_unhandled=None):
        self.handle_factory = handle_factory
        self.on_unhandled = on_unhandled
        self.outgoing_serial = 0
        self.awaiting_reply = {}
        self.signal_callbacks = {}

    def outgoing--- This code section failed: ---

 L.  22         0  LOAD_FAST                'self'
                2  DUP_TOP          
                4  LOAD_ATTR                outgoing_serial
                6  LOAD_CONST               1
                8  INPLACE_ADD      
               10  ROT_TWO          
               12  STORE_ATTR               outgoing_serial

 L.  23        14  LOAD_FAST                'self'
               16  LOAD_ATTR                outgoing_serial
               18  LOAD_FAST                'msg'
               20  LOAD_ATTR                header
               22  STORE_ATTR               serial

 L.  25        24  LOAD_FAST                'msg'
               26  LOAD_ATTR                header
               28  LOAD_ATTR                message_type
               30  LOAD_GLOBAL              MessageType
               32  LOAD_ATTR                method_call
               34  <117>                 0  ''
               36  POP_JUMP_IF_FALSE    64  'to 64'

 L.  26        38  LOAD_FAST                'self'
               40  LOAD_METHOD              handle_factory
               42  CALL_METHOD_0         0  ''
               44  DUP_TOP          
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                awaiting_reply
               50  LOAD_FAST                'msg'
               52  LOAD_ATTR                header
               54  LOAD_ATTR                serial
               56  STORE_SUBSCR     
               58  STORE_FAST               'handle'

 L.  27        60  LOAD_FAST                'handle'
               62  RETURN_VALUE     
             64_0  COME_FROM            36  '36'

Parse error at or near `<117>' instruction at offset 34

    def subscribe_signal(self, callback, path, interface, member):
        """Add a callback for a signal.
        """
        self.signal_callbacks[(path, interface, member)] = callback

    def incoming--- This code section failed: ---

 L.  37         0  LOAD_FAST                'msg'
                2  LOAD_ATTR                header
                4  STORE_FAST               'hdr'

 L.  40         6  LOAD_FAST                'hdr'
                8  LOAD_ATTR                message_type
               10  LOAD_GLOBAL              MessageType
               12  LOAD_ATTR                signal
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE   100  'to 100'

 L.  41        18  LOAD_FAST                'hdr'
               20  LOAD_ATTR                fields
               22  LOAD_METHOD              get
               24  LOAD_GLOBAL              HeaderFields
               26  LOAD_ATTR                path
               28  LOAD_CONST               None
               30  CALL_METHOD_2         2  ''

 L.  42        32  LOAD_FAST                'hdr'
               34  LOAD_ATTR                fields
               36  LOAD_METHOD              get
               38  LOAD_GLOBAL              HeaderFields
               40  LOAD_ATTR                interface
               42  LOAD_CONST               None
               44  CALL_METHOD_2         2  ''

 L.  43        46  LOAD_FAST                'hdr'
               48  LOAD_ATTR                fields
               50  LOAD_METHOD              get
               52  LOAD_GLOBAL              HeaderFields
               54  LOAD_ATTR                member
               56  LOAD_CONST               None
               58  CALL_METHOD_2         2  ''

 L.  41        60  BUILD_TUPLE_3         3 
               62  STORE_FAST               'key'

 L.  45        64  LOAD_FAST                'self'
               66  LOAD_ATTR                signal_callbacks
               68  LOAD_METHOD              get
               70  LOAD_FAST                'key'
               72  LOAD_CONST               None
               74  CALL_METHOD_2         2  ''
               76  STORE_FAST               'cb'

 L.  46        78  LOAD_FAST                'cb'
               80  LOAD_CONST               None
               82  <117>                 1  ''
               84  POP_JUMP_IF_FALSE   100  'to 100'

 L.  47        86  LOAD_FAST                'cb'
               88  LOAD_FAST                'msg'
               90  LOAD_ATTR                body
               92  CALL_FUNCTION_1       1  ''
               94  POP_TOP          

 L.  48        96  LOAD_CONST               None
               98  RETURN_VALUE     
            100_0  COME_FROM            84  '84'
            100_1  COME_FROM            16  '16'

 L.  51       100  LOAD_FAST                'hdr'
              102  LOAD_ATTR                fields
              104  LOAD_METHOD              get
              106  LOAD_GLOBAL              HeaderFields
              108  LOAD_ATTR                reply_serial
              110  LOAD_CONST               -1
              112  CALL_METHOD_2         2  ''
              114  STORE_FAST               'reply_serial'

 L.  52       116  LOAD_FAST                'self'
              118  LOAD_ATTR                awaiting_reply
              120  LOAD_METHOD              pop
              122  LOAD_FAST                'reply_serial'
              124  LOAD_CONST               None
              126  CALL_METHOD_2         2  ''
              128  STORE_FAST               'reply_handle'

 L.  53       130  LOAD_FAST                'reply_handle'
              132  LOAD_CONST               None
              134  <117>                 1  ''
              136  POP_JUMP_IF_FALSE   196  'to 196'

 L.  54       138  LOAD_FAST                'hdr'
              140  LOAD_ATTR                message_type
              142  LOAD_GLOBAL              MessageType
              144  LOAD_ATTR                method_return
              146  <117>                 0  ''
              148  POP_JUMP_IF_FALSE   166  'to 166'

 L.  55       150  LOAD_FAST                'reply_handle'
              152  LOAD_METHOD              set_result
              154  LOAD_FAST                'msg'
              156  LOAD_ATTR                body
              158  CALL_METHOD_1         1  ''
              160  POP_TOP          

 L.  56       162  LOAD_CONST               None
              164  RETURN_VALUE     
            166_0  COME_FROM           148  '148'

 L.  57       166  LOAD_FAST                'hdr'
              168  LOAD_ATTR                message_type
              170  LOAD_GLOBAL              MessageType
              172  LOAD_ATTR                error
              174  <117>                 0  ''
              176  POP_JUMP_IF_FALSE   196  'to 196'

 L.  58       178  LOAD_FAST                'reply_handle'
              180  LOAD_METHOD              set_exception
              182  LOAD_GLOBAL              DBusErrorResponse
              184  LOAD_FAST                'msg'
              186  CALL_FUNCTION_1       1  ''
              188  CALL_METHOD_1         1  ''
              190  POP_TOP          

 L.  59       192  LOAD_CONST               None
              194  RETURN_VALUE     
            196_0  COME_FROM           176  '176'
            196_1  COME_FROM           136  '136'

 L.  61       196  LOAD_FAST                'self'
              198  LOAD_ATTR                on_unhandled
              200  POP_JUMP_IF_FALSE   212  'to 212'

 L.  62       202  LOAD_FAST                'self'
              204  LOAD_METHOD              on_unhandled
              206  LOAD_FAST                'msg'
              208  CALL_METHOD_1         1  ''
              210  POP_TOP          
            212_0  COME_FROM           200  '200'

Parse error at or near `<117>' instruction at offset 14