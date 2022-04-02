# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: jeepney\io\common.py
from contextlib import contextmanager
from itertools import count
from jeepney import HeaderFields, Message, MessageFlag, MessageType

class MessageFilters:

    def __init__(self):
        self.filters = {}
        self.filter_ids = count()

    def matches(self, message):
        for handle in self.filters.values():
            if handle.rule.matches(message):
                yield handle


class FilterHandle:

    def __init__(self, filters: MessageFilters, rule, queue):
        self._filters = filters
        self._filter_id = next(filters.filter_ids)
        self.rule = rule
        self.queue = queue
        self._filters.filters[self._filter_id] = self

    def close(self):
        del self._filters.filters[self._filter_id]

    def __enter__(self):
        return self.queue

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


class ReplyMatcher:

    def __init__(self):
        self._futures = {}

    @contextmanager
    def catch--- This code section failed: ---

 L.  44         0  LOAD_FAST                'future'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _futures
                6  LOAD_FAST                'serial'
                8  STORE_SUBSCR     

 L.  46        10  SETUP_FINALLY        30  'to 30'

 L.  47        12  LOAD_FAST                'future'
               14  YIELD_VALUE      
               16  POP_TOP          
               18  POP_BLOCK        

 L.  49        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _futures
               24  LOAD_FAST                'serial'
               26  DELETE_SUBSCR    
               28  JUMP_FORWARD         40  'to 40'
             30_0  COME_FROM_FINALLY    10  '10'
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                _futures
               34  LOAD_FAST                'serial'
               36  DELETE_SUBSCR    
               38  <48>             
             40_0  COME_FROM            28  '28'

Parse error at or near `DELETE_SUBSCR' instruction at offset 26

    def dispatch--- This code section failed: ---

 L.  56         0  LOAD_FAST                'msg'
                2  LOAD_ATTR                header
                4  LOAD_ATTR                fields
                6  LOAD_METHOD              get
                8  LOAD_GLOBAL              HeaderFields
               10  LOAD_ATTR                reply_serial
               12  LOAD_CONST               -1
               14  CALL_METHOD_2         2  ''
               16  STORE_FAST               'rep_serial'

 L.  57        18  LOAD_FAST                'rep_serial'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                _futures
               24  <118>                 0  ''
               26  POP_JUMP_IF_FALSE    48  'to 48'

 L.  58        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _futures
               32  LOAD_FAST                'rep_serial'
               34  BINARY_SUBSCR    
               36  LOAD_METHOD              set_result
               38  LOAD_FAST                'msg'
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          

 L.  59        44  LOAD_CONST               True
               46  RETURN_VALUE     
             48_0  COME_FROM            26  '26'

 L.  61        48  LOAD_CONST               False
               50  RETURN_VALUE     

Parse error at or near `<118>' instruction at offset 24

    def drop_all--- This code section failed: ---

 L.  65         0  LOAD_FAST                'exc'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L.  66         8  LOAD_GLOBAL              RouterClosed
               10  LOAD_STR                 'D-Bus router closed before reply arrived'
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'exc'
             16_0  COME_FROM             6  '6'

 L.  67        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _futures
               20  BUILD_MAP_0           0 
               22  ROT_TWO          
               24  STORE_FAST               'futures'
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _futures

 L.  68        30  LOAD_FAST                'futures'
               32  LOAD_METHOD              values
               34  CALL_METHOD_0         0  ''
               36  GET_ITER         
             38_0  COME_FROM            52  '52'
               38  FOR_ITER             54  'to 54'
               40  STORE_FAST               'fut'

 L.  69        42  LOAD_FAST                'fut'
               44  LOAD_METHOD              set_exception
               46  LOAD_FAST                'exc'
               48  CALL_METHOD_1         1  ''
               50  POP_TOP          
               52  JUMP_BACK            38  'to 38'
             54_0  COME_FROM            38  '38'

Parse error at or near `None' instruction at offset -1


class RouterClosed(Exception):
    __doc__ = 'Raised in tasks waiting for a reply when the router is closed\n\n    This will also be raised if the receiver task crashes, so tasks are not\n    stuck waiting for a reply that can never come. The router object will not\n    be usable after this is raised.\n    '


def check_replyable(msg: Message):
    """Raise an error if we wouldn't expect a reply for msg"""
    if msg.header.message_type != MessageType.method_call:
        raise TypeError(f"Only method call messages have replies (not {msg.header.message_type})")
    if MessageFlag.no_reply_expected & msg.header.flags:
        raise ValueError('This message has the no_reply_expected flag set')