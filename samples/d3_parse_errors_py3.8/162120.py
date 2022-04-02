# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\serial\serialutil.py
import io, time
try:
    memoryview
except (NameError, AttributeError):

    class memoryview(object):
        pass


else:
    try:
        unicode
    except (NameError, AttributeError):
        unicode = str
    else:
        try:
            basestring
        except (NameError, AttributeError):
            basestring = (
             str,)
        else:

            def iterbytes--- This code section failed: ---

 L.  40         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'b'
                4  LOAD_GLOBAL              memoryview
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L.  41        10  LOAD_FAST                'b'
               12  LOAD_METHOD              tobytes
               14  CALL_METHOD_0         0  ''
               16  STORE_FAST               'b'
             18_0  COME_FROM             8  '8'

 L.  42        18  LOAD_CONST               0
               20  STORE_FAST               'i'
             22_0  COME_FROM            60  '60'
             22_1  COME_FROM            56  '56'

 L.  44        22  LOAD_FAST                'b'
               24  LOAD_FAST                'i'
               26  LOAD_FAST                'i'
               28  LOAD_CONST               1
               30  BINARY_ADD       
               32  BUILD_SLICE_2         2 
               34  BINARY_SUBSCR    
               36  STORE_FAST               'a'

 L.  45        38  LOAD_FAST                'i'
               40  LOAD_CONST               1
               42  INPLACE_ADD      
               44  STORE_FAST               'i'

 L.  46        46  LOAD_FAST                'a'
               48  POP_JUMP_IF_FALSE    62  'to 62'

 L.  47        50  LOAD_FAST                'a'
               52  YIELD_VALUE      
               54  POP_TOP          
               56  JUMP_BACK            22  'to 22'

 L.  49        58  JUMP_FORWARD         62  'to 62'
               60  JUMP_BACK            22  'to 22'
             62_0  COME_FROM            58  '58'
             62_1  COME_FROM            48  '48'

Parse error at or near `JUMP_FORWARD' instruction at offset 58


            def to_bytes(seq):
                """convert a sequence to a bytes type"""
                if isinstanceseqbytes:
                    return seq
                if isinstanceseqbytearray:
                    return bytes(seq)
                if isinstanceseqmemoryview:
                    return seq.tobytes
                if isinstancesequnicode:
                    raise TypeError('unicode strings are not supported, please encode to bytes: {!r}'.format(seq))
                else:
                    return bytes(bytearray(seq))


            XON = to_bytes([17])
            XOFF = to_bytes([19])
            CR = to_bytes([13])
            LF = to_bytes([10])
            PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE = ('N',
                                                                               'E',
                                                                               'O',
                                                                               'M',
                                                                               'S')
            STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO = (1, 1.5, 2)
            FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS = (5, 6, 7, 8)
            PARITY_NAMES = {PARITY_NONE: 'None', 
             PARITY_EVEN: 'Even', 
             PARITY_ODD: 'Odd', 
             PARITY_MARK: 'Mark', 
             PARITY_SPACE: 'Space'}

            class SerialException(IOError):
                __doc__ = 'Base class for serial port related exceptions.'


            class SerialTimeoutException(SerialException):
                __doc__ = 'Write timeouts give an exception'


            writeTimeoutError = SerialTimeoutException('Write timeout')
            portNotOpenError = SerialException('Attempting to use a port that is not open')

            class Timeout(object):
                __doc__ = '    Abstraction for timeout operations. Using time.monotonic() if available\n    or time.time() in all other cases.\n\n    The class can also be initialized with 0 or None, in order to support\n    non-blocking and fully blocking I/O operations. The attributes\n    is_non_blocking and is_infinite are set accordingly.\n    '
                if hasattrtime'monotonic':
                    TIME = time.monotonic
                else:
                    TIME = time.time

                def __init__(self, duration):
                    """Initialize a timeout with given duration"""
                    self.is_infinite = duration is None
                    self.is_non_blocking = duration == 0
                    self.duration = duration
                    if duration is not None:
                        self.target_time = self.TIME + duration
                    else:
                        self.target_time = None

                def expired(self):
                    """Return a boolean, telling if the timeout has expired"""
                    return self.target_time is not None and self.time_left <= 0

                def time_left(self):
                    """Return how many seconds are left until the timeout expires"""
                    if self.is_non_blocking:
                        return 0
                    if self.is_infinite:
                        return
                    delta = self.target_time - self.TIME
                    if delta > self.duration:
                        self.target_time = self.TIME + self.duration
                        return self.duration
                    return max0delta

                def restart(self, duration):
                    """        Restart a timeout, only supported if a timeout was already set up
        before.
        """
                    self.duration = duration
                    self.target_time = self.TIME + duration


            class SerialBase(io.RawIOBase):
                __doc__ = '    Serial port base class. Provides __init__ function and properties to\n    get/set port settings.\n    '
                BAUDRATES = (50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400,
                             4800, 9600, 19200, 38400, 57600, 115200, 230400, 460800,
                             500000, 576000, 921600, 1000000, 1152000, 1500000, 2000000,
                             2500000, 3000000, 3500000, 4000000)
                BYTESIZES = (
                 FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS)
                PARITIES = (PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE)
                STOPBITS = (STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO)

                def __init__(self, port=None, baudrate=9600, bytesize=EIGHTBITS, parity=PARITY_NONE, stopbits=STOPBITS_ONE, timeout=None, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=False, inter_byte_timeout=None, exclusive=None, **kwargs):
                    """        Initialize comm port object. If a "port" is given, then the port will be
        opened immediately. Otherwise a Serial port object in closed state
        is returned.
        """
                    self.is_open = False
                    self.portstr = None
                    self.name = None
                    self._port = None
                    self._baudrate = None
                    self._bytesize = None
                    self._parity = None
                    self._stopbits = None
                    self._timeout = None
                    self._write_timeout = None
                    self._xonxoff = None
                    self._rtscts = None
                    self._dsrdtr = None
                    self._inter_byte_timeout = None
                    self._rs485_mode = None
                    self._rts_state = True
                    self._dtr_state = True
                    self._break_state = False
                    self._exclusive = None
                    self.port = port
                    self.baudrate = baudrate
                    self.bytesize = bytesize
                    self.parity = parity
                    self.stopbits = stopbits
                    self.timeout = timeout
                    self.write_timeout = write_timeout
                    self.xonxoff = xonxoff
                    self.rtscts = rtscts
                    self.dsrdtr = dsrdtr
                    self.inter_byte_timeout = inter_byte_timeout
                    self.exclusive = exclusive
                    if 'writeTimeout' in kwargs:
                        self.write_timeout = kwargs.pop('writeTimeout')
                    if 'interCharTimeout' in kwargs:
                        self.inter_byte_timeout = kwargs.pop('interCharTimeout')
                    if kwargs:
                        raise ValueError('unexpected keyword arguments: {!r}'.format(kwargs))
                    if port is not None:
                        self.open

                @property
                def port(self):
                    """        Get the current port setting. The value that was passed on init or using
        setPort() is passed back.
        """
                    return self._port

                @port.setter
                def port(self, port):
                    """        Change the port.
        """
                    if port is not None:
                        if not isinstanceportbasestring:
                            raise ValueError('"port" must be None or a string, not {}'.format(type(port)))
                        was_open = self.is_open
                        if was_open:
                            self.close
                        self.portstr = port
                        self._port = port
                        self.name = self.portstr
                        if was_open:
                            self.open

                @property
                def baudrate(self):
                    """Get the current baud rate setting."""
                    return self._baudrate

                @baudrate.setter
                def baudrate(self, baudrate):
                    """        Change baud rate. It raises a ValueError if the port is open and the
        baud rate is not possible. If the port is closed, then the value is
        accepted and the exception is raised when the port is opened.
        """
                    try:
                        b = int(baudrate)
                    except TypeError:
                        raise ValueError('Not a valid baudrate: {!r}'.format(baudrate))
                    else:
                        if b < 0:
                            raise ValueError('Not a valid baudrate: {!r}'.format(baudrate))
                        self._baudrate = b
                        if self.is_open:
                            self._reconfigure_port

                @property
                def bytesize(self):
                    """Get the current byte size setting."""
                    return self._bytesize

                @bytesize.setter
                def bytesize(self, bytesize):
                    """Change byte size."""
                    if bytesize not in self.BYTESIZES:
                        raise ValueError('Not a valid byte size: {!r}'.format(bytesize))
                    self._bytesize = bytesize
                    if self.is_open:
                        self._reconfigure_port

                @property
                def exclusive(self):
                    """Get the current exclusive access setting."""
                    return self._exclusive

                @exclusive.setter
                def exclusive(self, exclusive):
                    """Change the exclusive access setting."""
                    self._exclusive = exclusive
                    if self.is_open:
                        self._reconfigure_port

                @property
                def parity(self):
                    """Get the current parity setting."""
                    return self._parity

                @parity.setter
                def parity(self, parity):
                    """Change parity setting."""
                    if parity not in self.PARITIES:
                        raise ValueError('Not a valid parity: {!r}'.format(parity))
                    self._parity = parity
                    if self.is_open:
                        self._reconfigure_port

                @property
                def stopbits(self):
                    """Get the current stop bits setting."""
                    return self._stopbits

                @stopbits.setter
                def stopbits(self, stopbits):
                    """Change stop bits size."""
                    if stopbits not in self.STOPBITS:
                        raise ValueError('Not a valid stop bit size: {!r}'.format(stopbits))
                    self._stopbits = stopbits
                    if self.is_open:
                        self._reconfigure_port

                @property
                def timeout(self):
                    """Get the current timeout setting."""
                    return self._timeout

                @timeout.setter
                def timeout(self, timeout):
                    """Change timeout setting."""
                    if timeout is not None:
                        try:
                            timeout + 1
                        except TypeError:
                            raise ValueError('Not a valid timeout: {!r}'.format(timeout))
                        else:
                            if timeout < 0:
                                raise ValueError('Not a valid timeout: {!r}'.format(timeout))
                        self._timeout = timeout
                        if self.is_open:
                            self._reconfigure_port

                @property
                def write_timeout(self):
                    """Get the current timeout setting."""
                    return self._write_timeout

                @write_timeout.setter
                def write_timeout(self, timeout):
                    """Change timeout setting."""
                    if timeout is not None:
                        if timeout < 0:
                            raise ValueError('Not a valid timeout: {!r}'.format(timeout))
                        try:
                            timeout + 1
                        except TypeError:
                            raise ValueError('Not a valid timeout: {!r}'.format(timeout))
                        else:
                            self._write_timeout = timeout
                            if self.is_open:
                                self._reconfigure_port

                @property
                def inter_byte_timeout(self):
                    """Get the current inter-character timeout setting."""
                    return self._inter_byte_timeout

                @inter_byte_timeout.setter
                def inter_byte_timeout(self, ic_timeout):
                    """Change inter-byte timeout setting."""
                    if ic_timeout is not None:
                        if ic_timeout < 0:
                            raise ValueError('Not a valid timeout: {!r}'.format(ic_timeout))
                        try:
                            ic_timeout + 1
                        except TypeError:
                            raise ValueError('Not a valid timeout: {!r}'.format(ic_timeout))
                        else:
                            self._inter_byte_timeout = ic_timeout
                            if self.is_open:
                                self._reconfigure_port

                @property
                def xonxoff(self):
                    """Get the current XON/XOFF setting."""
                    return self._xonxoff

                @xonxoff.setter
                def xonxoff(self, xonxoff):
                    """Change XON/XOFF setting."""
                    self._xonxoff = xonxoff
                    if self.is_open:
                        self._reconfigure_port

                @property
                def rtscts(self):
                    """Get the current RTS/CTS flow control setting."""
                    return self._rtscts

                @rtscts.setter
                def rtscts(self, rtscts):
                    """Change RTS/CTS flow control setting."""
                    self._rtscts = rtscts
                    if self.is_open:
                        self._reconfigure_port

                @property
                def dsrdtr(self):
                    """Get the current DSR/DTR flow control setting."""
                    return self._dsrdtr

                @dsrdtr.setter
                def dsrdtr(self, dsrdtr=None):
                    """Change DsrDtr flow control setting."""
                    if dsrdtr is None:
                        self._dsrdtr = self._rtscts
                    else:
                        self._dsrdtr = dsrdtr
                    if self.is_open:
                        self._reconfigure_port

                @property
                def rts(self):
                    return self._rts_state

                @rts.setter
                def rts(self, value):
                    self._rts_state = value
                    if self.is_open:
                        self._update_rts_state

                @property
                def dtr(self):
                    return self._dtr_state

                @dtr.setter
                def dtr(self, value):
                    self._dtr_state = value
                    if self.is_open:
                        self._update_dtr_state

                @property
                def break_condition(self):
                    return self._break_state

                @break_condition.setter
                def break_condition(self, value):
                    self._break_state = value
                    if self.is_open:
                        self._update_break_state

                @property
                def rs485_mode(self):
                    """        Enable RS485 mode and apply new settings, set to None to disable.
        See serial.rs485.RS485Settings for more info about the value.
        """
                    return self._rs485_mode

                @rs485_mode.setter
                def rs485_mode(self, rs485_settings):
                    self._rs485_mode = rs485_settings
                    if self.is_open:
                        self._reconfigure_port

                _SAVED_SETTINGS = ('baudrate', 'bytesize', 'parity', 'stopbits', 'xonxoff',
                                   'dsrdtr', 'rtscts', 'timeout', 'write_timeout',
                                   'inter_byte_timeout')

                def get_settings(self):
                    """        Get current port settings as a dictionary. For use with
        apply_settings().
        """
                    return dict([(key, getattrself('_' + key)) for key in self._SAVED_SETTINGS])

                def apply_settings(self, d):
                    """        Apply stored settings from a dictionary returned from
        get_settings(). It's allowed to delete keys from the dictionary. These
        values will simply left unchanged.
        """
                    for key in self._SAVED_SETTINGS:
                        if key in d:
                            if d[key] != getattrself('_' + key):
                                setattr(self, key, d[key])

                def __repr__(self):
                    """String representation of the current port settings and its state."""
                    return '{name}<id=0x{id:x}, open={p.is_open}>(port={p.portstr!r}, baudrate={p.baudrate!r}, bytesize={p.bytesize!r}, parity={p.parity!r}, stopbits={p.stopbits!r}, timeout={p.timeout!r}, xonxoff={p.xonxoff!r}, rtscts={p.rtscts!r}, dsrdtr={p.dsrdtr!r})'.format(name=(self.__class__.__name__),
                      id=(id(self)),
                      p=self)

                def readable(self):
                    return True

                def writable(self):
                    return True

                def seekable(self):
                    return False

                def readinto(self, b):
                    data = self.read(len(b))
                    n = len(data)
                    try:
                        b[:n] = data
                    except TypeError as err:
                        try:
                            import array
                            if not isinstancebarray.array:
                                raise err
                            b[:n] = array.array('b', data)
                        finally:
                            err = None
                            del err

                    else:
                        return n

                def __enter__(self):
                    if not self.is_open:
                        self.open
                    return self

                def __exit__(self, *args, **kwargs):
                    self.close

                def send_break(self, duration=0.25):
                    """        Send break condition. Timed, returns to idle state after given
        duration.
        """
                    if not self.is_open:
                        raise portNotOpenError
                    self.break_condition = True
                    time.sleep(duration)
                    self.break_condition = False

                def flushInput(self):
                    self.reset_input_buffer

                def flushOutput(self):
                    self.reset_output_buffer

                def inWaiting(self):
                    return self.in_waiting

                def sendBreak(self, duration=0.25):
                    self.send_break(duration)

                def setRTS(self, value=1):
                    self.rts = value

                def setDTR(self, value=1):
                    self.dtr = value

                def getCTS(self):
                    return self.cts

                def getDSR(self):
                    return self.dsr

                def getRI(self):
                    return self.ri

                def getCD(self):
                    return self.cd

                def setPort(self, port):
                    self.port = port

                @property
                def writeTimeout(self):
                    return self.write_timeout

                @writeTimeout.setter
                def writeTimeout(self, timeout):
                    self.write_timeout = timeout

                @property
                def interCharTimeout(self):
                    return self.inter_byte_timeout

                @interCharTimeout.setter
                def interCharTimeout(self, interCharTimeout):
                    self.inter_byte_timeout = interCharTimeout

                def getSettingsDict(self):
                    return self.get_settings

                def applySettingsDict(self, d):
                    self.apply_settings(d)

                def isOpen(self):
                    return self.is_open

                def read_all(self):
                    """        Read all bytes currently available in the buffer of the OS.
        """
                    return self.read(self.in_waiting)

                def read_until--- This code section failed: ---

 L. 655         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'terminator'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'lenterm'

 L. 656         8  LOAD_GLOBAL              bytearray
               10  CALL_FUNCTION_0       0  ''
               12  STORE_FAST               'line'

 L. 657        14  LOAD_GLOBAL              Timeout
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                _timeout
               20  CALL_FUNCTION_1       1  ''
               22  STORE_FAST               'timeout'
             24_0  COME_FROM           102  '102'
             24_1  COME_FROM            98  '98'

 L. 659        24  LOAD_FAST                'self'
               26  LOAD_METHOD              read
               28  LOAD_CONST               1
               30  CALL_METHOD_1         1  ''
               32  STORE_FAST               'c'

 L. 660        34  LOAD_FAST                'c'
               36  POP_JUMP_IF_FALSE   104  'to 104'

 L. 661        38  LOAD_FAST                'line'
               40  LOAD_FAST                'c'
               42  INPLACE_ADD      
               44  STORE_FAST               'line'

 L. 662        46  LOAD_FAST                'line'
               48  LOAD_FAST                'lenterm'
               50  UNARY_NEGATIVE   
               52  LOAD_CONST               None
               54  BUILD_SLICE_2         2 
               56  BINARY_SUBSCR    
               58  LOAD_FAST                'terminator'
               60  COMPARE_OP               ==
               62  POP_JUMP_IF_FALSE    66  'to 66'

 L. 663        64  JUMP_FORWARD        104  'to 104'
             66_0  COME_FROM            62  '62'

 L. 664        66  LOAD_FAST                'size'
               68  LOAD_CONST               None
               70  COMPARE_OP               is-not
               72  POP_JUMP_IF_FALSE    92  'to 92'
               74  LOAD_GLOBAL              len
               76  LOAD_FAST                'line'
               78  CALL_FUNCTION_1       1  ''
               80  LOAD_FAST                'size'
               82  COMPARE_OP               >=
               84  POP_JUMP_IF_FALSE    92  'to 92'

 L. 665        86  JUMP_FORWARD        104  'to 104'
               88  BREAK_LOOP           92  'to 92'

 L. 667        90  JUMP_FORWARD        104  'to 104'
             92_0  COME_FROM            88  '88'
             92_1  COME_FROM            84  '84'
             92_2  COME_FROM            72  '72'

 L. 668        92  LOAD_FAST                'timeout'
               94  LOAD_METHOD              expired
               96  CALL_METHOD_0         0  ''
               98  POP_JUMP_IF_FALSE_BACK    24  'to 24'

 L. 669       100  JUMP_FORWARD        104  'to 104'
              102  JUMP_BACK            24  'to 24'
            104_0  COME_FROM           100  '100'
            104_1  COME_FROM            90  '90'
            104_2  COME_FROM            86  '86'
            104_3  COME_FROM            64  '64'
            104_4  COME_FROM            36  '36'

 L. 670       104  LOAD_GLOBAL              bytes
              106  LOAD_FAST                'line'
              108  CALL_FUNCTION_1       1  ''
              110  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 102

                def iread_until(self, *args, **kwargs):
                    """        Read lines, implemented as generator. It will raise StopIteration on
        timeout (empty read).
        """
                    while True:
                        line = (self.read_until)(*args, **kwargs)
                        if not line:
                            pass
                        else:
                            yield line


            if __name__ == '__main__':
                import sys
                s = SerialBase()
                sys.stdout.write('port name:  {}\n'.format(s.name))
                sys.stdout.write('baud rates: {}\n'.format(s.BAUDRATES))
                sys.stdout.write('byte sizes: {}\n'.format(s.BYTESIZES))
                sys.stdout.write('parities:   {}\n'.format(s.PARITIES))
                sys.stdout.write('stop bits:  {}\n'.format(s.STOPBITS))
                sys.stdout.write('{}\n'.format(s))