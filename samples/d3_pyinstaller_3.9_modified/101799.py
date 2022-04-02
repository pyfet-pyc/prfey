# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: telebot\handler_backends.py
import os, pickle, threading
from telebot import apihelper

class HandlerBackend(object):
    __doc__ = '\n    Class for saving (next step|reply) handlers\n    '

    def __init__--- This code section failed: ---

 L.  13         0  LOAD_FAST                'handlers'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L.  14         8  BUILD_MAP_0           0 
               10  STORE_FAST               'handlers'
             12_0  COME_FROM             6  '6'

 L.  15        12  LOAD_FAST                'handlers'
               14  LOAD_FAST                'self'
               16  STORE_ATTR               handlers

Parse error at or near `None' instruction at offset -1

    def register_handler(self, handler_group_id, handler):
        raise NotImplementedError()

    def clear_handlers(self, handler_group_id):
        raise NotImplementedError()

    def get_handlers(self, handler_group_id):
        raise NotImplementedError()


class MemoryHandlerBackend(HandlerBackend):

    def register_handler--- This code section failed: ---

 L.  29         0  LOAD_FAST                'handler_group_id'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                handlers
                6  <118>                 0  ''
                8  POP_JUMP_IF_FALSE    28  'to 28'

 L.  30        10  LOAD_FAST                'self'
               12  LOAD_ATTR                handlers
               14  LOAD_FAST                'handler_group_id'
               16  BINARY_SUBSCR    
               18  LOAD_METHOD              append
               20  LOAD_FAST                'handler'
               22  CALL_METHOD_1         1  ''
               24  POP_TOP          
               26  JUMP_FORWARD         40  'to 40'
             28_0  COME_FROM             8  '8'

 L.  32        28  LOAD_FAST                'handler'
               30  BUILD_LIST_1          1 
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                handlers
               36  LOAD_FAST                'handler_group_id'
               38  STORE_SUBSCR     
             40_0  COME_FROM            26  '26'

Parse error at or near `None' instruction at offset -1

    def clear_handlers(self, handler_group_id):
        self.handlers.pop(handler_group_id, None)

    def get_handlers(self, handler_group_id):
        return self.handlers.pop(handler_group_id, None)

    def load_handlers(self, filename, del_file_after_loading):
        raise NotImplementedError()


class FileHandlerBackend(HandlerBackend):

    def __init__(self, handlers=None, filename='./.handler-saves/handlers.save', delay=120):
        super(FileHandlerBackend, self).__init__handlers
        self.filename = filename
        self.delay = delay
        self.timer = threading.Timer(delay, self.save_handlers)

    def register_handler--- This code section failed: ---

 L.  52         0  LOAD_FAST                'handler_group_id'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                handlers
                6  <118>                 0  ''
                8  POP_JUMP_IF_FALSE    28  'to 28'

 L.  53        10  LOAD_FAST                'self'
               12  LOAD_ATTR                handlers
               14  LOAD_FAST                'handler_group_id'
               16  BINARY_SUBSCR    
               18  LOAD_METHOD              append
               20  LOAD_FAST                'handler'
               22  CALL_METHOD_1         1  ''
               24  POP_TOP          
               26  JUMP_FORWARD         40  'to 40'
             28_0  COME_FROM             8  '8'

 L.  55        28  LOAD_FAST                'handler'
               30  BUILD_LIST_1          1 
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                handlers
               36  LOAD_FAST                'handler_group_id'
               38  STORE_SUBSCR     
             40_0  COME_FROM            26  '26'

 L.  56        40  LOAD_FAST                'self'
               42  LOAD_METHOD              start_save_timer
               44  CALL_METHOD_0         0  ''
               46  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def clear_handlers(self, handler_group_id):
        self.handlers.pop(handler_group_id, None)
        self.start_save_timer

    def get_handlers(self, handler_group_id):
        handlers = self.handlers.pop(handler_group_id, None)
        self.start_save_timer
        return handlers

    def start_save_timer(self):
        if not self.timer.is_alive:
            if self.delay <= 0:
                self.save_handlers
            else:
                self.timer = threading.Timer(self.delay, self.save_handlers)
                self.timer.start

    def save_handlers(self):
        self.dump_handlers(self.handlers, self.filename)

    def load_handlers--- This code section failed: ---

 L.  79         0  LOAD_FAST                'filename'
                2  POP_JUMP_IF_TRUE     10  'to 10'

 L.  80         4  LOAD_FAST                'self'
                6  LOAD_ATTR                filename
                8  STORE_FAST               'filename'
             10_0  COME_FROM             2  '2'

 L.  81        10  LOAD_FAST                'self'
               12  LOAD_ATTR                return_load_handlers
               14  LOAD_FAST                'filename'
               16  LOAD_FAST                'del_file_after_loading'
               18  LOAD_CONST               ('del_file_after_loading',)
               20  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               22  STORE_FAST               'tmp'

 L.  82        24  LOAD_FAST                'tmp'
               26  LOAD_CONST               None
               28  <117>                 1  ''
               30  POP_JUMP_IF_FALSE    44  'to 44'

 L.  83        32  LOAD_FAST                'self'
               34  LOAD_ATTR                handlers
               36  LOAD_METHOD              update
               38  LOAD_FAST                'tmp'
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          
             44_0  COME_FROM            30  '30'

Parse error at or near `<117>' instruction at offset 28

    @staticmethod
    def dump_handlers--- This code section failed: ---

 L.  87         0  LOAD_FAST                'filename'
                2  LOAD_ATTR                rsplit
                4  LOAD_STR                 '/'
                6  LOAD_CONST               1
                8  LOAD_CONST               ('maxsplit',)
               10  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               12  LOAD_CONST               0
               14  BINARY_SUBSCR    
               16  STORE_FAST               'dirs'

 L.  88        18  LOAD_GLOBAL              os
               20  LOAD_ATTR                makedirs
               22  LOAD_FAST                'dirs'
               24  LOAD_CONST               True
               26  LOAD_CONST               ('exist_ok',)
               28  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               30  POP_TOP          

 L.  90        32  LOAD_GLOBAL              open
               34  LOAD_FAST                'filename'
               36  LOAD_STR                 '.tmp'
               38  BINARY_ADD       
               40  LOAD_FAST                'file_mode'
               42  CALL_FUNCTION_2       2  ''
               44  SETUP_WITH          100  'to 100'
               46  STORE_FAST               'file'

 L.  91        48  LOAD_GLOBAL              apihelper
               50  LOAD_ATTR                CUSTOM_SERIALIZER
               52  LOAD_CONST               None
               54  <117>                 0  ''
               56  POP_JUMP_IF_FALSE    72  'to 72'

 L.  92        58  LOAD_GLOBAL              pickle
               60  LOAD_METHOD              dump
               62  LOAD_FAST                'handlers'
               64  LOAD_FAST                'file'
               66  CALL_METHOD_2         2  ''
               68  POP_TOP          
               70  JUMP_FORWARD         86  'to 86'
             72_0  COME_FROM            56  '56'

 L.  94        72  LOAD_GLOBAL              apihelper
               74  LOAD_ATTR                CUSTOM_SERIALIZER
               76  LOAD_METHOD              dump
               78  LOAD_FAST                'handlers'
               80  LOAD_FAST                'file'
               82  CALL_METHOD_2         2  ''
               84  POP_TOP          
             86_0  COME_FROM            70  '70'
               86  POP_BLOCK        
               88  LOAD_CONST               None
               90  DUP_TOP          
               92  DUP_TOP          
               94  CALL_FUNCTION_3       3  ''
               96  POP_TOP          
               98  JUMP_FORWARD        116  'to 116'
            100_0  COME_FROM_WITH       44  '44'
              100  <49>             
              102  POP_JUMP_IF_TRUE    106  'to 106'
              104  <48>             
            106_0  COME_FROM           102  '102'
              106  POP_TOP          
              108  POP_TOP          
              110  POP_TOP          
              112  POP_EXCEPT       
              114  POP_TOP          
            116_0  COME_FROM            98  '98'

 L.  96       116  LOAD_GLOBAL              os
              118  LOAD_ATTR                path
              120  LOAD_METHOD              isfile
              122  LOAD_FAST                'filename'
              124  CALL_METHOD_1         1  ''
              126  POP_JUMP_IF_FALSE   138  'to 138'

 L.  97       128  LOAD_GLOBAL              os
              130  LOAD_METHOD              remove
              132  LOAD_FAST                'filename'
              134  CALL_METHOD_1         1  ''
              136  POP_TOP          
            138_0  COME_FROM           126  '126'

 L.  99       138  LOAD_GLOBAL              os
              140  LOAD_METHOD              rename
              142  LOAD_FAST                'filename'
              144  LOAD_STR                 '.tmp'
              146  BINARY_ADD       
              148  LOAD_FAST                'filename'
              150  CALL_METHOD_2         2  ''
              152  POP_TOP          

Parse error at or near `<117>' instruction at offset 54

    @staticmethod
    def return_load_handlers--- This code section failed: ---

 L. 103         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              isfile
                6  LOAD_FAST                'filename'
                8  CALL_METHOD_1         1  ''
               10  POP_JUMP_IF_FALSE   122  'to 122'
               12  LOAD_GLOBAL              os
               14  LOAD_ATTR                path
               16  LOAD_METHOD              getsize
               18  LOAD_FAST                'filename'
               20  CALL_METHOD_1         1  ''
               22  LOAD_CONST               0
               24  COMPARE_OP               >
               26  POP_JUMP_IF_FALSE   122  'to 122'

 L. 104        28  LOAD_GLOBAL              open
               30  LOAD_FAST                'filename'
               32  LOAD_STR                 'rb'
               34  CALL_FUNCTION_2       2  ''
               36  SETUP_WITH           88  'to 88'
               38  STORE_FAST               'file'

 L. 105        40  LOAD_GLOBAL              apihelper
               42  LOAD_ATTR                CUSTOM_SERIALIZER
               44  LOAD_CONST               None
               46  <117>                 0  ''
               48  POP_JUMP_IF_FALSE    62  'to 62'

 L. 106        50  LOAD_GLOBAL              pickle
               52  LOAD_METHOD              load
               54  LOAD_FAST                'file'
               56  CALL_METHOD_1         1  ''
               58  STORE_FAST               'handlers'
               60  JUMP_FORWARD         74  'to 74'
             62_0  COME_FROM            48  '48'

 L. 108        62  LOAD_GLOBAL              apihelper
               64  LOAD_ATTR                CUSTOM_SERIALIZER
               66  LOAD_METHOD              load
               68  LOAD_FAST                'file'
               70  CALL_METHOD_1         1  ''
               72  STORE_FAST               'handlers'
             74_0  COME_FROM            60  '60'
               74  POP_BLOCK        
               76  LOAD_CONST               None
               78  DUP_TOP          
               80  DUP_TOP          
               82  CALL_FUNCTION_3       3  ''
               84  POP_TOP          
               86  JUMP_FORWARD        104  'to 104'
             88_0  COME_FROM_WITH       36  '36'
               88  <49>             
               90  POP_JUMP_IF_TRUE     94  'to 94'
               92  <48>             
             94_0  COME_FROM            90  '90'
               94  POP_TOP          
               96  POP_TOP          
               98  POP_TOP          
              100  POP_EXCEPT       
              102  POP_TOP          
            104_0  COME_FROM            86  '86'

 L. 110       104  LOAD_FAST                'del_file_after_loading'
              106  POP_JUMP_IF_FALSE   118  'to 118'

 L. 111       108  LOAD_GLOBAL              os
              110  LOAD_METHOD              remove
              112  LOAD_FAST                'filename'
              114  CALL_METHOD_1         1  ''
              116  POP_TOP          
            118_0  COME_FROM           106  '106'

 L. 113       118  LOAD_FAST                'handlers'
              120  RETURN_VALUE     
            122_0  COME_FROM            26  '26'
            122_1  COME_FROM            10  '10'

Parse error at or near `<117>' instruction at offset 46


class RedisHandlerBackend(HandlerBackend):

    def __init__(self, handlers=None, host='localhost', port=6379, db=0, prefix='telebot', password=None):
        super(RedisHandlerBackend, self).__init__handlers
        from redis import Redis
        self.prefix = prefix
        self.redis = Redis(host, port, db, password)

    def _key(self, handle_group_id):
        return ':'.join(self.prefix, str(handle_group_id))

    def register_handler(self, handler_group_id, handler):
        handlers = []
        value = self.redis.getself._keyhandler_group_id
        if value:
            handlers = pickle.loadsvalue
        handlers.appendhandler
        self.redis.set(self._keyhandler_group_id, pickle.dumpshandlers)

    def clear_handlers(self, handler_group_id):
        self.redis.deleteself._keyhandler_group_id

    def get_handlers(self, handler_group_id):
        handlers = None
        value = self.redis.getself._keyhandler_group_id
        if value:
            handlers = pickle.loadsvalue
            self.clear_handlershandler_group_id
        return handlers