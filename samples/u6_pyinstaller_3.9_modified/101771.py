# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: pyttsx3\driver.py
import sys, traceback, weakref, importlib

class DriverProxy(object):
    __doc__ = '\n    Proxy to a driver implementation.\n\n    @ivar _module: Module containing the driver implementation\n    @type _module: module\n    @ivar _engine: Reference to the engine that owns the driver\n    @type _engine: L{engine.Engine}\n    @ivar _queue: Queue of commands outstanding for the driver\n    @type _queue: list\n    @ivar _busy: True when the driver is busy processing a command, False when\n        not\n    @type _busy: bool\n    @ivar _name: Name associated with the current utterance\n    @type _name: str\n    @ivar _debug: Debugging output enabled or not\n    @type _debug: bool\n    @ivar _iterator: Driver iterator to invoke when in an external run loop\n    @type _iterator: iterator\n    '

    def __init__--- This code section failed: ---

 L.  40         0  LOAD_FAST                'driverName'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    44  'to 44'

 L.  42         8  LOAD_GLOBAL              sys
               10  LOAD_ATTR                platform
               12  LOAD_STR                 'darwin'
               14  COMPARE_OP               ==
               16  POP_JUMP_IF_FALSE    24  'to 24'

 L.  43        18  LOAD_STR                 'nsss'
               20  STORE_FAST               'driverName'
               22  JUMP_FORWARD         44  'to 44'
             24_0  COME_FROM            16  '16'

 L.  44        24  LOAD_GLOBAL              sys
               26  LOAD_ATTR                platform
               28  LOAD_STR                 'win32'
               30  COMPARE_OP               ==
               32  POP_JUMP_IF_FALSE    40  'to 40'

 L.  45        34  LOAD_STR                 'sapi5'
               36  STORE_FAST               'driverName'
               38  JUMP_FORWARD         44  'to 44'
             40_0  COME_FROM            32  '32'

 L.  47        40  LOAD_STR                 'espeak'
               42  STORE_FAST               'driverName'
             44_0  COME_FROM            38  '38'
             44_1  COME_FROM            22  '22'
             44_2  COME_FROM             6  '6'

 L.  49        44  LOAD_STR                 'pyttsx3.drivers.%s'
               46  LOAD_FAST                'driverName'
               48  BINARY_MODULO    
               50  STORE_FAST               'name'

 L.  50        52  LOAD_GLOBAL              importlib
               54  LOAD_METHOD              import_module
               56  LOAD_FAST                'name'
               58  CALL_METHOD_1         1  ''
               60  LOAD_FAST                'self'
               62  STORE_ATTR               _module

 L.  52        64  LOAD_FAST                'self'
               66  LOAD_ATTR                _module
               68  LOAD_METHOD              buildDriver
               70  LOAD_GLOBAL              weakref
               72  LOAD_METHOD              proxy
               74  LOAD_FAST                'self'
               76  CALL_METHOD_1         1  ''
               78  CALL_METHOD_1         1  ''
               80  LOAD_FAST                'self'
               82  STORE_ATTR               _driver

 L.  54        84  LOAD_FAST                'engine'
               86  LOAD_FAST                'self'
               88  STORE_ATTR               _engine

 L.  55        90  BUILD_LIST_0          0 
               92  LOAD_FAST                'self'
               94  STORE_ATTR               _queue

 L.  56        96  LOAD_CONST               True
               98  LOAD_FAST                'self'
              100  STORE_ATTR               _busy

 L.  57       102  LOAD_CONST               None
              104  LOAD_FAST                'self'
              106  STORE_ATTR               _name

 L.  58       108  LOAD_CONST               None
              110  LOAD_FAST                'self'
              112  STORE_ATTR               _iterator

 L.  59       114  LOAD_FAST                'debug'
              116  LOAD_FAST                'self'
              118  STORE_ATTR               _debug

Parse error at or near `None' instruction at offset -1

    def __del__--- This code section failed: ---

 L.  62         0  SETUP_FINALLY        16  'to 16'

 L.  63         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _driver
                6  LOAD_METHOD              destroy
                8  CALL_METHOD_0         0  ''
               10  POP_TOP          
               12  POP_BLOCK        
               14  JUMP_FORWARD         38  'to 38'
             16_0  COME_FROM_FINALLY     0  '0'

 L.  64        16  DUP_TOP          
               18  LOAD_GLOBAL              AttributeError
               20  LOAD_GLOBAL              TypeError
               22  BUILD_TUPLE_2         2 
               24  <121>                36  ''
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L.  65        32  POP_EXCEPT       
               34  JUMP_FORWARD         38  'to 38'
               36  <48>             
             38_0  COME_FROM            34  '34'
             38_1  COME_FROM            14  '14'

Parse error at or near `<121>' instruction at offset 24

    def _push(self, mtd, args, name=None):
        """
        Adds a command to the queue.

        @param mtd: Method to invoke to process the command
        @type mtd: method
        @param args: Arguments to apply when invoking the method
        @type args: tuple
        @param name: Name associated with the command
        @type name: str
        """
        self._queue.append(mtd, args, name)
        self._pump

    def _pump--- This code section failed: ---

 L.  86         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _busy
                4  POP_JUMP_IF_TRUE    126  'to 126'
                6  LOAD_GLOBAL              len
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                _queue
               12  CALL_FUNCTION_1       1  ''
               14  POP_JUMP_IF_FALSE   126  'to 126'

 L.  87        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _queue
               20  LOAD_METHOD              pop
               22  LOAD_CONST               0
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'cmd'

 L.  88        28  LOAD_FAST                'cmd'
               30  LOAD_CONST               2
               32  BINARY_SUBSCR    
               34  LOAD_FAST                'self'
               36  STORE_ATTR               _name

 L.  89        38  SETUP_FINALLY        60  'to 60'

 L.  90        40  LOAD_FAST                'cmd'
               42  LOAD_CONST               0
               44  BINARY_SUBSCR    
               46  LOAD_FAST                'cmd'
               48  LOAD_CONST               1
               50  BINARY_SUBSCR    
               52  CALL_FUNCTION_EX      0  'positional arguments only'
               54  POP_TOP          
               56  POP_BLOCK        
               58  JUMP_BACK             0  'to 0'
             60_0  COME_FROM_FINALLY    38  '38'

 L.  91        60  DUP_TOP          
               62  LOAD_GLOBAL              Exception
               64  <121>               122  ''
               66  POP_TOP          
               68  STORE_FAST               'e'
               70  POP_TOP          
               72  SETUP_FINALLY       114  'to 114'

 L.  92        74  LOAD_FAST                'self'
               76  LOAD_ATTR                notify
               78  LOAD_STR                 'error'
               80  LOAD_FAST                'e'
               82  LOAD_CONST               ('exception',)
               84  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               86  POP_TOP          

 L.  93        88  LOAD_FAST                'self'
               90  LOAD_ATTR                _debug
               92  POP_JUMP_IF_FALSE   102  'to 102'

 L.  94        94  LOAD_GLOBAL              traceback
               96  LOAD_METHOD              print_exc
               98  CALL_METHOD_0         0  ''
              100  POP_TOP          
            102_0  COME_FROM            92  '92'
              102  POP_BLOCK        
              104  POP_EXCEPT       
              106  LOAD_CONST               None
              108  STORE_FAST               'e'
              110  DELETE_FAST              'e'
              112  JUMP_BACK             0  'to 0'
            114_0  COME_FROM_FINALLY    72  '72'
              114  LOAD_CONST               None
              116  STORE_FAST               'e'
              118  DELETE_FAST              'e'
              120  <48>             
              122  <48>             
              124  JUMP_BACK             0  'to 0'
            126_0  COME_FROM            14  '14'
            126_1  COME_FROM             4  '4'

Parse error at or near `<121>' instruction at offset 64

    def notify--- This code section failed: ---

 L. 105         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _name
                4  LOAD_FAST                'kwargs'
                6  LOAD_STR                 'name'
                8  STORE_SUBSCR     

 L. 106        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _engine
               14  LOAD_ATTR                _notify
               16  LOAD_FAST                'topic'
               18  BUILD_TUPLE_1         1 
               20  BUILD_MAP_0           0 
               22  LOAD_FAST                'kwargs'
               24  <164>                 1  ''
               26  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               28  POP_TOP          

Parse error at or near `<164>' instruction at offset 24

    def setBusy(self, busy):
        """
        Called by the driver to indicate it is busy.

        @param busy: True when busy, false when idle
        @type busy: bool
        """
        self._busy = busy
        if not self._busy:
            self._pump

    def isBusy(self):
        """
        @return: True if the driver is busy, false if not
        @rtype: bool
        """
        return self._busy

    def say(self, text, name):
        """
        Called by the engine to push a say command onto the queue.

        @param text: Text to speak
        @type text: unicode
        @param name: Name to associate with the utterance
        @type name: str
        """
        self._push(self._driver.say, (text,), name)

    def stop--- This code section failed: ---

 L. 144         0  SETUP_FINALLY        22  'to 22'

 L. 145         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _queue
                6  LOAD_CONST               0
                8  BINARY_SUBSCR    
               10  UNPACK_SEQUENCE_3     3 
               12  STORE_FAST               'mtd'
               14  STORE_FAST               'args'
               16  STORE_FAST               'name'
               18  POP_BLOCK        
               20  JUMP_FORWARD         44  'to 44'
             22_0  COME_FROM_FINALLY     0  '0'

 L. 146        22  DUP_TOP          
               24  LOAD_GLOBAL              IndexError
               26  <121>                42  ''
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 147        34  POP_EXCEPT       
               36  BREAK_LOOP           72  'to 72'
               38  POP_EXCEPT       
               40  JUMP_FORWARD         44  'to 44'
               42  <48>             
             44_0  COME_FROM            40  '40'
             44_1  COME_FROM            20  '20'

 L. 148        44  LOAD_FAST                'mtd'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                _engine
               50  LOAD_ATTR                endLoop
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_FALSE    58  'to 58'

 L. 149        56  BREAK_LOOP           72  'to 72'
             58_0  COME_FROM            54  '54'

 L. 150        58  LOAD_FAST                'self'
               60  LOAD_ATTR                _queue
               62  LOAD_METHOD              pop
               64  LOAD_CONST               0
               66  CALL_METHOD_1         1  ''
               68  POP_TOP          
               70  JUMP_BACK             0  'to 0'
             72_0  COME_FROM_EXCEPT_CLAUSE    36  '36'

 L. 151        72  LOAD_FAST                'self'
               74  LOAD_ATTR                _driver
               76  LOAD_METHOD              stop
               78  CALL_METHOD_0         0  ''
               80  POP_TOP          

Parse error at or near `<121>' instruction at offset 26

    def save_to_file(self, text, filename, name):
        """
        Called by the engine to push a say command onto the queue.

        @param text: Text to speak
        @type text: unicode
        @param name: Name to associate with the utterance
        @type name: str
        """
        self._push(self._driver.save_to_file, (text, filename), name)

    def getProperty(self, name):
        """
        Called by the engine to get a driver property value.

        @param name: Name of the property
        @type name: str
        @return: Property value
        @rtype: object
        """
        return self._driver.getPropertyname

    def setProperty(self, name, value):
        """
        Called by the engine to set a driver property value.

        @param name: Name of the property
        @type name: str
        @param value: Property value
        @type value: object
        """
        self._push(self._driver.setProperty, (name, value))

    def runAndWait(self):
        """
        Called by the engine to start an event loop, process all commands in
        the queue at the start of the loop, and then exit the loop.
        """
        self._push(self._engine.endLoop, tuple())
        self._driver.startLoop

    def startLoop(self, useDriverLoop):
        """
        Called by the engine to start an event loop.
        """
        if useDriverLoop:
            self._driver.startLoop
        else:
            self._iterator = self._driver.iterate

    def endLoop(self, useDriverLoop):
        """
        Called by the engine to stop an event loop.
        """
        self._queue = []
        self._driver.stop
        if useDriverLoop:
            self._driver.endLoop
        else:
            self._iterator = None
        self.setBusyTrue

    def iterate--- This code section failed: ---

 L. 220         0  SETUP_FINALLY        16  'to 16'

 L. 221         2  LOAD_GLOBAL              next
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _iterator
                8  CALL_FUNCTION_1       1  ''
               10  POP_TOP          
               12  POP_BLOCK        
               14  JUMP_FORWARD         34  'to 34'
             16_0  COME_FROM_FINALLY     0  '0'

 L. 222        16  DUP_TOP          
               18  LOAD_GLOBAL              StopIteration
               20  <121>                32  ''
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 223        28  POP_EXCEPT       
               30  JUMP_FORWARD         34  'to 34'
               32  <48>             
             34_0  COME_FROM            30  '30'
             34_1  COME_FROM            14  '14'

Parse error at or near `<121>' instruction at offset 20