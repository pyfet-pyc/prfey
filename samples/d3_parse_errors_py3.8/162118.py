# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\serial\serialjava.py
from serial.serialutil import *

def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    else:
        return mod


def detect_java_comm--- This code section failed: ---

 L.  23         0  LOAD_FAST                'names'
                2  GET_ITER         
              4_0  COME_FROM            58  '58'
              4_1  COME_FROM            54  '54'
                4  FOR_ITER             60  'to 60'
                6  STORE_FAST               'name'

 L.  24         8  SETUP_FINALLY        34  'to 34'

 L.  25        10  LOAD_GLOBAL              my_import
               12  LOAD_FAST                'name'
               14  CALL_FUNCTION_1       1  ''
               16  STORE_FAST               'mod'

 L.  26        18  LOAD_FAST                'mod'
               20  LOAD_ATTR                SerialPort
               22  POP_TOP          

 L.  27        24  LOAD_FAST                'mod'
               26  POP_BLOCK        
               28  ROT_TWO          
               30  POP_TOP          
               32  RETURN_VALUE     
             34_0  COME_FROM_FINALLY     8  '8'

 L.  28        34  DUP_TOP          
               36  LOAD_GLOBAL              ImportError
               38  LOAD_GLOBAL              AttributeError
               40  BUILD_TUPLE_2         2 
               42  COMPARE_OP               exception-match
               44  POP_JUMP_IF_FALSE    56  'to 56'
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L.  29        52  POP_EXCEPT       
               54  JUMP_BACK             4  'to 4'
             56_0  COME_FROM            44  '44'
               56  END_FINALLY      
               58  JUMP_BACK             4  'to 4'
             60_0  COME_FROM             4  '4'

 L.  30        60  LOAD_GLOBAL              ImportError
               62  LOAD_STR                 'No Java Communications API implementation found'
               64  CALL_FUNCTION_1       1  ''
               66  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `ROT_TWO' instruction at offset 28


comm = detect_java_comm([
 'javax.comm',
 'gnu.io'])

def device(portnumber):
    """Turn a port number into a device name"""
    enum = comm.CommPortIdentifier.getPortIdentifiers()
    ports = []
    while True:
        if enum.hasMoreElements():
            el = enum.nextElement()
            if el.getPortType() == comm.CommPortIdentifier.PORT_SERIAL:
                ports.append(el)

    return ports[portnumber].getName()


class Serial(SerialBase):
    __doc__ = '    Serial port class, implemented with Java Communications API and\n    thus usable with jython and the appropriate java extension.\n    '

    def open(self):
        """        Open port with current settings. This may throw a SerialException
        if the port cannot be opened.
        """
        if self._port is None:
            raise SerialException('Port must be configured before it can be used.')
        if self.is_open:
            raise SerialException('Port is already open.')
        if type(self._port) == type(''):
            portId = comm.CommPortIdentifier.getPortIdentifier(self._port)
        else:
            portId = comm.CommPortIdentifier.getPortIdentifier(device(self._port))
        try:
            self.sPort = portId.open('python serial module', 10)
        except Exception as msg:
            try:
                self.sPort = None
                raise SerialException('Could not open port: %s' % msg)
            finally:
                msg = None
                del msg

        else:
            self._reconfigurePort()
            self._instream = self.sPort.getInputStream()
            self._outstream = self.sPort.getOutputStream()
            self.is_open = True

    def _reconfigurePort(self):
        """Set communication parameters on opened port."""
        if not self.sPort:
            raise SerialException('Can only operate on a valid port handle')
        self.sPort.enableReceiveTimeout(30)
        if self._bytesize == FIVEBITS:
            jdatabits = comm.SerialPort.DATABITS_5
        elif self._bytesize == SIXBITS:
            jdatabits = comm.SerialPort.DATABITS_6
        elif self._bytesize == SEVENBITS:
            jdatabits = comm.SerialPort.DATABITS_7
        elif self._bytesize == EIGHTBITS:
            jdatabits = comm.SerialPort.DATABITS_8
        else:
            raise ValueError('unsupported bytesize: %r' % self._bytesize)
        if self._stopbits == STOPBITS_ONE:
            jstopbits = comm.SerialPort.STOPBITS_1
        elif self._stopbits == STOPBITS_ONE_POINT_FIVE:
            jstopbits = comm.SerialPort.STOPBITS_1_5
        elif self._stopbits == STOPBITS_TWO:
            jstopbits = comm.SerialPort.STOPBITS_2
        else:
            raise ValueError('unsupported number of stopbits: %r' % self._stopbits)
        if self._parity == PARITY_NONE:
            jparity = comm.SerialPort.PARITY_NONE
        elif self._parity == PARITY_EVEN:
            jparity = comm.SerialPort.PARITY_EVEN
        elif self._parity == PARITY_ODD:
            jparity = comm.SerialPort.PARITY_ODD
        elif self._parity == PARITY_MARK:
            jparity = comm.SerialPort.PARITY_MARK
        elif self._parity == PARITY_SPACE:
            jparity = comm.SerialPort.PARITY_SPACE
        else:
            raise ValueError('unsupported parity type: %r' % self._parity)
        jflowin = jflowout = 0
        if self._rtscts:
            jflowin |= comm.SerialPort.FLOWCONTROL_RTSCTS_IN
            jflowout |= comm.SerialPort.FLOWCONTROL_RTSCTS_OUT
        if self._xonxoff:
            jflowin |= comm.SerialPort.FLOWCONTROL_XONXOFF_IN
            jflowout |= comm.SerialPort.FLOWCONTROL_XONXOFF_OUT
        self.sPort.setSerialPortParams(self._baudrate, jdatabits, jstopbits, jparity)
        self.sPort.setFlowControlMode(jflowin | jflowout)
        if self._timeout >= 0:
            self.sPort.enableReceiveTimeout(int(self._timeout * 1000))
        else:
            self.sPort.disableReceiveTimeout()

    def close(self):
        """Close port"""
        if self.is_open:
            if self.sPort:
                self._instream.close()
                self._outstream.close()
                self.sPort.close()
                self.sPort = None
            self.is_open = False

    @property
    def in_waiting(self):
        """Return the number of characters currently in the input buffer."""
        if not self.sPort:
            raise portNotOpenError
        return self._instream.available()

    def read--- This code section failed: ---

 L. 162         0  LOAD_FAST                'self'
                2  LOAD_ATTR                sPort
                4  POP_JUMP_IF_TRUE     10  'to 10'

 L. 163         6  LOAD_GLOBAL              portNotOpenError
                8  RAISE_VARARGS_1       1  'exception instance'
             10_0  COME_FROM             4  '4'

 L. 164        10  LOAD_GLOBAL              bytearray
               12  CALL_FUNCTION_0       0  ''
               14  STORE_FAST               'read'

 L. 165        16  LOAD_FAST                'size'
               18  LOAD_CONST               0
               20  COMPARE_OP               >
               22  POP_JUMP_IF_FALSE    80  'to 80'
             24_0  COME_FROM            78  '78'
             24_1  COME_FROM            66  '66'

 L. 166        24  LOAD_GLOBAL              len
               26  LOAD_FAST                'read'
               28  CALL_FUNCTION_1       1  ''
               30  LOAD_FAST                'size'
               32  COMPARE_OP               <
               34  POP_JUMP_IF_FALSE    80  'to 80'

 L. 167        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _instream
               40  LOAD_METHOD              read
               42  CALL_METHOD_0         0  ''
               44  STORE_FAST               'x'

 L. 168        46  LOAD_FAST                'x'
               48  LOAD_CONST               -1
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    68  'to 68'

 L. 169        54  LOAD_FAST                'self'
               56  LOAD_ATTR                timeout
               58  LOAD_CONST               0
               60  COMPARE_OP               >=
               62  POP_JUMP_IF_FALSE    78  'to 78'

 L. 170        64  JUMP_FORWARD         80  'to 80'
               66  JUMP_BACK            24  'to 24'
             68_0  COME_FROM            52  '52'

 L. 172        68  LOAD_FAST                'read'
               70  LOAD_METHOD              append
               72  LOAD_FAST                'x'
               74  CALL_METHOD_1         1  ''
               76  POP_TOP          
             78_0  COME_FROM            62  '62'
               78  JUMP_BACK            24  'to 24'
             80_0  COME_FROM            64  '64'
             80_1  COME_FROM            34  '34'
             80_2  COME_FROM            22  '22'

 L. 173        80  LOAD_GLOBAL              bytes
               82  LOAD_FAST                'read'
               84  CALL_FUNCTION_1       1  ''
               86  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 86

    def write(self, data):
        """Output the given string over the serial port."""
        if not self.sPort:
            raise portNotOpenError
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError('expected %s or bytearray, got %s' % (bytes, type(data)))
        self._outstream.write(data)
        return len(data)

    def reset_input_buffer(self):
        """Clear input buffer, discarding all that is in the buffer."""
        if not self.sPort:
            raise portNotOpenError
        self._instream.skip(self._instream.available())

    def reset_output_buffer(self):
        """        Clear output buffer, aborting the current output and
        discarding all that is in the buffer.
        """
        if not self.sPort:
            raise portNotOpenError
        self._outstream.flush()

    def send_break(self, duration=0.25):
        """Send break condition. Timed, returns to idle state after given duration."""
        if not self.sPort:
            raise portNotOpenError
        self.sPort.sendBreak(duration * 1000.0)

    def _update_break_state(self):
        """Set break: Controls TXD. When active, to transmitting is possible."""
        if self.fd is None:
            raise portNotOpenError
        raise SerialException('The _update_break_state function is not implemented in java.')

    def _update_rts_state(self):
        """Set terminal status line: Request To Send"""
        if not self.sPort:
            raise portNotOpenError
        self.sPort.setRTS(self._rts_state)

    def _update_dtr_state(self):
        """Set terminal status line: Data Terminal Ready"""
        if not self.sPort:
            raise portNotOpenError
        self.sPort.setDTR(self._dtr_state)

    @property
    def cts(self):
        """Read terminal status line: Clear To Send"""
        if not self.sPort:
            raise portNotOpenError
        self.sPort.isCTS()

    @property
    def dsr(self):
        """Read terminal status line: Data Set Ready"""
        if not self.sPort:
            raise portNotOpenError
        self.sPort.isDSR()

    @property
    def ri(self):
        """Read terminal status line: Ring Indicator"""
        if not self.sPort:
            raise portNotOpenError
        self.sPort.isRI()

    @property
    def cd(self):
        """Read terminal status line: Carrier Detect"""
        if not self.sPort:
            raise portNotOpenError
        self.sPort.isCD()