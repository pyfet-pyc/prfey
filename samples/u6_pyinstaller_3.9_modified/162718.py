# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: pyttsx3\drivers\dummy.py
from ..voice import Voice
import time

def buildDriver(proxy):
    """
    Builds a new instance of a driver and returns it for use by the driver
    proxy.

    @param proxy: Proxy creating the driver
    @type proxy: L{driver.DriverProxy}
    """
    return DummyDriver(proxy)


class DummyDriver(object):
    __doc__ = '\n    Dummy speech engine implementation. Documents the interface, notifications,\n    properties, and sequencing responsibilities of a driver implementation.\n\n    @ivar _proxy: Driver proxy that manages this instance\n    @type _proxy: L{driver.DriverProxy}\n    @ivar _config: Dummy configuration\n    @type _config: dict\n    @ivar _looping: True when in the dummy event loop, False when not\n    @ivar _looping: bool\n    '

    def __init__(self, proxy):
        """
        Constructs the driver.

        @param proxy: Proxy creating the driver
        @type proxy: L{driver.DriverProxy}
        """
        self._proxy = proxy
        self._looping = False
        voices = [
         Voice('dummy.voice1', 'John Doe', ['en-US', 'en-GB'], 'male', 'adult'),
         Voice('dummy.voice2', 'Jane Doe', ['en-US', 'en-GB'], 'female', 'adult'),
         Voice('dummy.voice3', 'Jimmy Doe', ['en-US', 'en-GB'], 'male', 10)]
        self._config = {'rate':200, 
         'volume':1.0, 
         'voice':voices[0], 
         'voices':voices}

    def destroy(self):
        """
        Optional method that will be called when the driver proxy is being
        destroyed. Can cleanup any resources to make sure the engine terminates
        properly.
        """
        pass

    def startLoop(self):
        """
        Starts a blocking run loop in which driver callbacks are properly
        invoked.

        @precondition: There was no previous successful call to L{startLoop}
            without an intervening call to L{stopLoop}.
        """
        first = True
        self._looping = True
        while self._looping:
            if first:
                self._proxy.setBusy(False)
                first = False
            time.sleep(0.5)

    def endLoop(self):
        """
        Stops a previously started run loop.

        @precondition: A previous call to L{startLoop} suceeded and there was
            no intervening call to L{endLoop}.
        """
        self._looping = False

    def iterate(self):
        """
        Iterates from within an external run loop.
        """
        self._proxy.setBusy(False)
        (yield)

    def say--- This code section failed: ---

 L. 114         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _proxy
                4  LOAD_METHOD              setBusy
                6  LOAD_CONST               True
                8  CALL_METHOD_1         1  ''
               10  POP_TOP          

 L. 115        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _proxy
               16  LOAD_METHOD              notify
               18  LOAD_STR                 'started-utterance'
               20  CALL_METHOD_1         1  ''
               22  POP_TOP          

 L. 116        24  LOAD_CONST               0
               26  STORE_FAST               'i'

 L. 117        28  LOAD_FAST                'text'
               30  LOAD_METHOD              split
               32  LOAD_STR                 ' '
               34  CALL_METHOD_1         1  ''
               36  GET_ITER         
               38  FOR_ITER            110  'to 110'
               40  STORE_FAST               'word'

 L. 118        42  LOAD_FAST                'self'
               44  LOAD_ATTR                _proxy
               46  LOAD_ATTR                notify
               48  LOAD_STR                 'started-word'
               50  LOAD_FAST                'i'
               52  LOAD_GLOBAL              len
               54  LOAD_FAST                'word'
               56  CALL_FUNCTION_1       1  ''
               58  LOAD_CONST               ('location', 'length')
               60  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               62  POP_TOP          

 L. 119        64  SETUP_FINALLY        90  'to 90'

 L. 120        66  LOAD_FAST                'text'
               68  LOAD_METHOD              index
               70  LOAD_STR                 ' '
               72  LOAD_FAST                'i'
               74  LOAD_CONST               1
               76  BINARY_ADD       
               78  CALL_METHOD_2         2  ''
               80  LOAD_CONST               1
               82  BINARY_ADD       
               84  STORE_FAST               'i'
               86  POP_BLOCK        
               88  JUMP_BACK            38  'to 38'
             90_0  COME_FROM_FINALLY    64  '64'

 L. 121        90  DUP_TOP          
               92  LOAD_GLOBAL              Exception
               94  <121>               106  ''
               96  POP_TOP          
               98  POP_TOP          
              100  POP_TOP          

 L. 122       102  POP_EXCEPT       
              104  JUMP_BACK            38  'to 38'
              106  <48>             
              108  JUMP_BACK            38  'to 38'

 L. 123       110  LOAD_FAST                'self'
              112  LOAD_ATTR                _proxy
              114  LOAD_ATTR                notify
              116  LOAD_STR                 'finished-utterance'
              118  LOAD_CONST               True
              120  LOAD_CONST               ('completed',)
              122  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              124  POP_TOP          

 L. 124       126  LOAD_FAST                'self'
              128  LOAD_ATTR                _proxy
              130  LOAD_METHOD              setBusy
              132  LOAD_CONST               False
              134  CALL_METHOD_1         1  ''
              136  POP_TOP          

Parse error at or near `<121>' instruction at offset 94

    def stop(self):
        """
        Stops any current output. If an utterance was being spoken, the driver
        is still responsible for sending the closing finished-utterance
        notification documented above and resetting the busy state of the
        proxy.
        """
        pass

    def getProperty--- This code section failed: ---

 L. 149         0  SETUP_FINALLY        14  'to 14'

 L. 150         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _config
                6  LOAD_FAST                'name'
                8  BINARY_SUBSCR    
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 151        14  DUP_TOP          
               16  LOAD_GLOBAL              KeyError
               18  <121>                42  ''
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L. 152        26  LOAD_GLOBAL              KeyError
               28  LOAD_STR                 'unknown property %s'
               30  LOAD_FAST                'name'
               32  BINARY_MODULO    
               34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
               38  POP_EXCEPT       
               40  JUMP_FORWARD         44  'to 44'
               42  <48>             
             44_0  COME_FROM            40  '40'

Parse error at or near `<121>' instruction at offset 18

    def setProperty(self, name, value):
        """
        Sets one of the supported property values of the speech engine listed
        above. If a value is invalid, attempts to clip it / coerce so it is
        valid before giving up and firing an exception.

        @param name: Property name
        @type name: str
        @param value: Property value
        @type value: object
        @raise KeyError: When the property name is unknown
        @raise ValueError: When the value cannot be coerced to fit the property
        """
        if name == 'voice':
            v = filter(lambda v: v.id == value, self._config['voices'])
            self._config['voice'] = v[0]
        else:
            if name == 'rate':
                self._config['rate'] = value
            else:
                if name == 'volume':
                    self._config['volume'] = value
                else:
                    raise KeyError('unknown property %s' % name)