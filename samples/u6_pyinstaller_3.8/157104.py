# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\keyboard\_generic.py
from threading import Thread, Lock
import traceback, functools
try:
    from queue import Queue
except ImportError:
    from Queue import Queue
else:

    class GenericListener(object):
        lock = Lock()

        def __init__(self):
            self.handlers = []
            self.listening = False
            self.queue = Queue()

        def invoke_handlers--- This code section failed: ---

 L.  20         0  LOAD_FAST                'self'
                2  LOAD_ATTR                handlers
                4  GET_ITER         
                6  FOR_ITER             76  'to 76'
                8  STORE_FAST               'handler'

 L.  21        10  SETUP_FINALLY        32  'to 32'

 L.  22        12  LOAD_FAST                'handler'
               14  LOAD_FAST                'event'
               16  CALL_FUNCTION_1       1  ''
               18  POP_JUMP_IF_FALSE    28  'to 28'

 L.  24        20  POP_BLOCK        
               22  POP_TOP          
               24  LOAD_CONST               1
               26  RETURN_VALUE     
             28_0  COME_FROM            18  '18'
               28  POP_BLOCK        
               30  JUMP_BACK             6  'to 6'
             32_0  COME_FROM_FINALLY    10  '10'

 L.  25        32  DUP_TOP          
               34  LOAD_GLOBAL              Exception
               36  COMPARE_OP               exception-match
               38  POP_JUMP_IF_FALSE    72  'to 72'
               40  POP_TOP          
               42  STORE_FAST               'e'
               44  POP_TOP          
               46  SETUP_FINALLY        60  'to 60'

 L.  26        48  LOAD_GLOBAL              traceback
               50  LOAD_METHOD              print_exc
               52  CALL_METHOD_0         0  ''
               54  POP_TOP          
               56  POP_BLOCK        
               58  BEGIN_FINALLY    
             60_0  COME_FROM_FINALLY    46  '46'
               60  LOAD_CONST               None
               62  STORE_FAST               'e'
               64  DELETE_FAST              'e'
               66  END_FINALLY      
               68  POP_EXCEPT       
               70  JUMP_BACK             6  'to 6'
             72_0  COME_FROM            38  '38'
               72  END_FINALLY      
               74  JUMP_BACK             6  'to 6'

Parse error at or near `LOAD_CONST' instruction at offset 24

        def start_if_necessary(self):
            """
        Starts the listening thread if it wasn't already.
        """
            self.lock.acquire
            try:
                if not self.listening:
                    self.init
                    self.listening = True
                    self.listening_thread = Thread(target=(self.listen))
                    self.listening_thread.daemon = True
                    self.listening_thread.start
                    self.processing_thread = Thread(target=(self.process))
                    self.processing_thread.daemon = True
                    self.processing_thread.start
            finally:
                self.lock.release

        def pre_process_event(self, event):
            raise NotImplementedError('This method should be implemented in the child class.')

        def process(self):
            """
        Loops over the underlying queue of events and processes them in order.
        """
            assert self.queue is not None
            while True:
                event = self.queue.get
                if self.pre_process_event(event):
                    self.invoke_handlers(event)
                self.queue.task_done

        def add_handler(self, handler):
            """
        Adds a function to receive each event captured, starting the capturing
        process if necessary.
        """
            self.start_if_necessary
            self.handlers.append(handler)

        def remove_handler(self, handler):
            """ Removes a previously added event handler. """
            while handler in self.handlers:
                self.handlers.remove(handler)