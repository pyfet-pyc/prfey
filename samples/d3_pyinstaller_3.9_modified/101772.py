# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: pyttsx3\engine.py
from . import driver
import traceback, weakref

class Engine(object):
    __doc__ = '\n    @ivar proxy: Proxy to a driver implementation\n    @type proxy: L{DriverProxy}\n    @ivar _connects: Array of subscriptions\n    @type _connects: list\n    @ivar _inLoop: Running an event loop or not\n    @type _inLoop: bool\n    @ivar _driverLoop: Using a driver event loop or not\n    @type _driverLoop: bool\n    @ivar _debug: Print exceptions or not\n    @type _debug: bool\n    '

    def __init__(self, driverName=None, debug=False):
        """
        Constructs a new TTS engine instance.

        @param driverName: Name of the platform specific driver to use. If
            None, selects the default driver for the operating system.
        @type: str
        @param debug: Debugging output enabled or not
        @type debug: bool
        """
        self.proxy = driver.DriverProxy(weakref.proxy(self), driverName, debug)
        self._connects = {}
        self._inLoop = False
        self._driverLoop = True
        self._debug = debug

    def _notify--- This code section failed: ---

 L.  46         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _connects
                4  LOAD_METHOD              get
                6  LOAD_FAST                'topic'
                8  BUILD_LIST_0          0 
               10  CALL_METHOD_2         2  ''
               12  GET_ITER         
             14_0  COME_FROM            70  '70'
             14_1  COME_FROM            66  '66'
             14_2  COME_FROM            36  '36'
               14  FOR_ITER             72  'to 72'
               16  STORE_FAST               'cb'

 L.  47        18  SETUP_FINALLY        38  'to 38'

 L.  48        20  LOAD_FAST                'cb'
               22  BUILD_TUPLE_0         0 
               24  BUILD_MAP_0           0 
               26  LOAD_FAST                'kwargs'
               28  <164>                 1  ''
               30  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               32  POP_TOP          
               34  POP_BLOCK        
               36  JUMP_BACK            14  'to 14'
             38_0  COME_FROM_FINALLY    18  '18'

 L.  49        38  DUP_TOP          
               40  LOAD_GLOBAL              Exception
               42  <121>                68  ''
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L.  50        50  LOAD_FAST                'self'
               52  LOAD_ATTR                _debug
               54  POP_JUMP_IF_FALSE    64  'to 64'

 L.  51        56  LOAD_GLOBAL              traceback
               58  LOAD_METHOD              print_exc
               60  CALL_METHOD_0         0  ''
               62  POP_TOP          
             64_0  COME_FROM            54  '54'
               64  POP_EXCEPT       
               66  JUMP_BACK            14  'to 14'
               68  <48>             
               70  JUMP_BACK            14  'to 14'
             72_0  COME_FROM            14  '14'

Parse error at or near `<164>' instruction at offset 28

    def connect(self, topic, cb):
        """
        Registers a callback for an event topic. Valid topics and their
        associated values:

        started-utterance: name=<str>
        started-word: name=<str>, location=<int>, length=<int>
        finished-utterance: name=<str>, completed=<bool>
        error: name=<str>, exception=<exception>

        @param topic: Event topic name
        @type topic: str
        @param cb: Callback function
        @type cb: callable
        @return: Token to use to unregister
        @rtype: dict
        """
        arr = self._connects.setdefaulttopic[]
        arr.append(cb)
        return {'topic':topic, 
         'cb':cb}

    def disconnect--- This code section failed: ---

 L.  81         0  LOAD_FAST                'token'
                2  LOAD_STR                 'topic'
                4  BINARY_SUBSCR    
                6  STORE_FAST               'topic'

 L.  82         8  SETUP_FINALLY        24  'to 24'

 L.  83        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _connects
               14  LOAD_FAST                'topic'
               16  BINARY_SUBSCR    
               18  STORE_FAST               'arr'
               20  POP_BLOCK        
               22  JUMP_FORWARD         44  'to 44'
             24_0  COME_FROM_FINALLY     8  '8'

 L.  84        24  DUP_TOP          
               26  LOAD_GLOBAL              KeyError
               28  <121>                42  ''
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L.  85        36  POP_EXCEPT       
               38  LOAD_CONST               None
               40  RETURN_VALUE     
               42  <48>             
             44_0  COME_FROM            22  '22'

 L.  86        44  LOAD_FAST                'arr'
               46  LOAD_METHOD              remove
               48  LOAD_FAST                'token'
               50  LOAD_STR                 'cb'
               52  BINARY_SUBSCR    
               54  CALL_METHOD_1         1  ''
               56  POP_TOP          

 L.  87        58  LOAD_GLOBAL              len
               60  LOAD_FAST                'arr'
               62  CALL_FUNCTION_1       1  ''
               64  LOAD_CONST               0
               66  COMPARE_OP               ==
               68  POP_JUMP_IF_FALSE    78  'to 78'

 L.  88        70  LOAD_FAST                'self'
               72  LOAD_ATTR                _connects
               74  LOAD_FAST                'topic'
               76  DELETE_SUBSCR    
             78_0  COME_FROM            68  '68'

Parse error at or near `<121>' instruction at offset 28

    def say(self, text, name=None):
        """
        Adds an utterance to speak to the event queue.

        @param text: Text to sepak
        @type text: unicode
        @param name: Name to associate with this utterance. Included in
            notifications about this utterance.
        @type name: str
        """
        self.proxy.saytextname

    def stop(self):
        """
        Stops the current utterance and clears the event queue.
        """
        self.proxy.stop

    def save_to_file(self, text, filename, name=None):
        """
        Adds an utterance to speak to the event queue.

        @param text: Text to sepak
        @type text: unicode
        @param filename: the name of file to save.
        @param name: Name to associate with this utterance. Included in
            notifications about this utterance.
        @type name: str
        """
        self.proxy.save_to_file(text, filename, name)

    def isBusy(self):
        """
        @return: True if an utterance is currently being spoken, false if not
        @rtype: bool
        """
        return self.proxy.isBusy

    def getProperty(self, name):
        """
        Gets the current value of a property. Valid names and values include:

        voices: List of L{voice.Voice} objects supported by the driver
        voice: String ID of the current voice
        rate: Integer speech rate in words per minute
        volume: Floating point volume of speech in the range [0.0, 1.0]

        Numeric values outside the valid range supported by the driver are
        clipped.

        @param name: Name of the property to fetch
        @type name: str
        @return: Value associated with the property
        @rtype: object
        @raise KeyError: When the property name is unknown
        """
        return self.proxy.getProperty(name)

    def setProperty(self, name, value):
        """
        Adds a property value to set to the event queue. Valid names and values
        include:

        voice: String ID of the voice
        rate: Integer speech rate in words per minute
        volume: Floating point volume of speech in the range [0.0, 1.0]

        Numeric values outside the valid range supported by the driver are
        clipped.

        @param name: Name of the property to fetch
        @type name: str
        @param: Value to set for the property
        @rtype: object
        @raise KeyError: When the property name is unknown
        """
        self.proxy.setPropertynamevalue

    def runAndWait(self):
        """
        Runs an event loop until all commands queued up until this method call
        complete. Blocks during the event loop and returns when the queue is
        cleared.

        @raise RuntimeError: When the loop is already running
        """
        if self._inLoop:
            raise RuntimeError('run loop already started')
        self._inLoop = True
        self._driverLoop = True
        self.proxy.runAndWait

    def startLoop(self, useDriverLoop=True):
        """
        Starts an event loop to process queued commands and callbacks.

        @param useDriverLoop: If True, uses the run loop provided by the driver
            (the default). If False, assumes the caller will enter its own
            run loop which will pump any events for the TTS engine properly.
        @type useDriverLoop: bool
        @raise RuntimeError: When the loop is already running
        """
        if self._inLoop:
            raise RuntimeError('run loop already started')
        self._inLoop = True
        self._driverLoop = useDriverLoop
        self.proxy.startLoop(self._driverLoop)

    def endLoop(self):
        """
        Stops a running event loop.

        @raise RuntimeError: When the loop is not running
        """
        if not self._inLoop:
            raise RuntimeError('run loop not started')
        self.proxy.endLoop(self._driverLoop)
        self._inLoop = False

    def iterate(self):
        """
        Must be called regularly when using an external event loop.
        """
        if not self._inLoop:
            raise RuntimeError('run loop not started')
        elif self._driverLoop:
            raise RuntimeError('iterate not valid in driver run loop')
        self.proxy.iterate