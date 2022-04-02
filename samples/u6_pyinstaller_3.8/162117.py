# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\serial\serialcli.py
import System, System.IO.Ports
from serial.serialutil import *
sab = System.Array[System.Byte]

def as_byte_array(string):
    return sab([ord(x) for x in string])


class Serial(SerialBase):
    __doc__ = 'Serial port implementation for .NET/Mono.'
    BAUDRATES = (50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600,
                 19200, 38400, 57600, 115200)

    def open(self):
        """        Open port with current settings. This may throw a SerialException
        if the port cannot be opened.
        """
        if self._port is None:
            raise SerialException('Port must be configured before it can be used.')
        if self.is_open:
            raise SerialException('Port is already open.')
        try:
            self._port_handle = System.IO.Ports.SerialPort(self.portstr)
        except Exception as msg:
            try:
                self._port_handle = None
                raise SerialException('could not open port %s: %s' % (self.portstr, msg))
            finally:
                msg = None
                del msg

        else:
            if self._rts_state is None:
                self._rts_state = True
            else:
                if self._dtr_state is None:
                    self._dtr_state = True
                self._reconfigure_port()
                self._port_handle.Open()
                self.is_open = True
                if not self._dsrdtr:
                    self._update_dtr_state()
                self._rtscts or self._update_rts_state()
            self.reset_input_buffer()

    def _reconfigure_port(self):
        """Set communication parameters on opened port."""
        if not self._port_handle:
            raise SerialException('Can only operate on a valid port handle')
        else:
            if self._timeout is None:
                self._port_handle.ReadTimeout = System.IO.Ports.SerialPort.InfiniteTimeout
            else:
                self._port_handle.ReadTimeout = int(self._timeout * 1000)
            if self._write_timeout is None:
                self._port_handle.WriteTimeout = System.IO.Ports.SerialPort.InfiniteTimeout
            else:
                self._port_handle.WriteTimeout = int(self._write_timeout * 1000)
        try:
            self._port_handle.BaudRate = self._baudrate
        except IOError as e:
            try:
                raise ValueError(str(e))
            finally:
                e = None
                del e

        else:
            if self._bytesize == FIVEBITS:
                self._port_handle.DataBits = 5
            else:
                if self._bytesize == SIXBITS:
                    self._port_handle.DataBits = 6
                else:
                    if self._bytesize == SEVENBITS:
                        self._port_handle.DataBits = 7
                    else:
                        if self._bytesize == EIGHTBITS:
                            self._port_handle.DataBits = 8
                        else:
                            raise ValueError('Unsupported number of data bits: %r' % self._bytesize)
            if self._parity == PARITY_NONE:
                self._port_handle.Parity = getattr(System.IO.Ports.Parity, 'None')
            else:
                if self._parity == PARITY_EVEN:
                    self._port_handle.Parity = System.IO.Ports.Parity.Even
                else:
                    if self._parity == PARITY_ODD:
                        self._port_handle.Parity = System.IO.Ports.Parity.Odd
                    else:
                        if self._parity == PARITY_MARK:
                            self._port_handle.Parity = System.IO.Ports.Parity.Mark
                        else:
                            if self._parity == PARITY_SPACE:
                                self._port_handle.Parity = System.IO.Ports.Parity.Space
                            else:
                                raise ValueError('Unsupported parity mode: %r' % self._parity)
            if self._stopbits == STOPBITS_ONE:
                self._port_handle.StopBits = System.IO.Ports.StopBits.One
            else:
                if self._stopbits == STOPBITS_ONE_POINT_FIVE:
                    self._port_handle.StopBits = System.IO.Ports.StopBits.OnePointFive
                else:
                    if self._stopbits == STOPBITS_TWO:
                        self._port_handle.StopBits = System.IO.Ports.StopBits.Two
                    else:
                        raise ValueError('Unsupported number of stop bits: %r' % self._stopbits)
            if self._rtscts and self._xonxoff:
                self._port_handle.Handshake = System.IO.Ports.Handshake.RequestToSendXOnXOff
            else:
                if self._rtscts:
                    self._port_handle.Handshake = System.IO.Ports.Handshake.RequestToSend
                else:
                    if self._xonxoff:
                        self._port_handle.Handshake = System.IO.Ports.Handshake.XOnXOff
                    else:
                        self._port_handle.Handshake = getattr(System.IO.Ports.Handshake, 'None')

    def close(self):
        """Close port"""
        if self.is_open:
            if self._port_handle:
                try:
                    self._port_handle.Close()
                except System.IO.Ports.InvalidOperationException:
                    pass
                else:
                    self._port_handle = None
            self.is_open = False

    @property
    def in_waiting(self):
        """Return the number of characters currently in the input buffer."""
        if not self.is_open:
            raise portNotOpenError
        return self._port_handle.BytesToRead

    def read--- This code section failed: ---

 L. 158         0  LOAD_FAST                'self'
                2  LOAD_ATTR                is_open
                4  POP_JUMP_IF_TRUE     10  'to 10'

 L. 159         6  LOAD_GLOBAL              portNotOpenError
                8  RAISE_VARARGS_1       1  'exception instance'
             10_0  COME_FROM             4  '4'

 L. 162        10  LOAD_GLOBAL              bytearray
               12  CALL_FUNCTION_0       0  ''
               14  STORE_FAST               'data'

 L. 163        16  LOAD_FAST                'size'
               18  POP_JUMP_IF_FALSE    78  'to 78'

 L. 164        20  SETUP_FINALLY        42  'to 42'

 L. 165        22  LOAD_FAST                'data'
               24  LOAD_METHOD              append
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                _port_handle
               30  LOAD_METHOD              ReadByte
               32  CALL_METHOD_0         0  ''
               34  CALL_METHOD_1         1  ''
               36  POP_TOP          
               38  POP_BLOCK        
               40  JUMP_FORWARD         68  'to 68'
             42_0  COME_FROM_FINALLY    20  '20'

 L. 166        42  DUP_TOP          
               44  LOAD_GLOBAL              System
               46  LOAD_ATTR                TimeoutException
               48  COMPARE_OP               exception-match
               50  POP_JUMP_IF_FALSE    66  'to 66'
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          

 L. 167        58  POP_EXCEPT       
               60  BREAK_LOOP           78  'to 78'
               62  POP_EXCEPT       
               64  JUMP_BACK            16  'to 16'
             66_0  COME_FROM            50  '50'
               66  END_FINALLY      
             68_0  COME_FROM            40  '40'

 L. 169        68  LOAD_FAST                'size'
               70  LOAD_CONST               1
               72  INPLACE_SUBTRACT 
               74  STORE_FAST               'size'
               76  JUMP_BACK            16  'to 16'
             78_0  COME_FROM_EXCEPT_CLAUSE    60  '60'
             78_1  COME_FROM_EXCEPT_CLAUSE    18  '18'

 L. 170        78  LOAD_GLOBAL              bytes
               80  LOAD_FAST                'data'
               82  CALL_FUNCTION_1       1  ''
               84  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_EXCEPT_CLAUSE' instruction at offset 78_1

    def write(self, data):
        """Output the given string over the serial port."""
        if not self.is_open:
            raise portNotOpenError
        try:
            self._port_handle.Write(as_byte_array(data), 0, len(data))
        except System.TimeoutException:
            raise writeTimeoutError
        else:
            return len(data)

    def reset_input_buffer(self):
        """Clear input buffer, discarding all that is in the buffer."""
        if not self.is_open:
            raise portNotOpenError
        self._port_handle.DiscardInBuffer()

    def reset_output_buffer(self):
        """        Clear output buffer, aborting the current output and
        discarding all that is in the buffer.
        """
        if not self.is_open:
            raise portNotOpenError
        self._port_handle.DiscardOutBuffer()

    def _update_break_state(self):
        """
        Set break: Controls TXD. When active, to transmitting is possible.
        """
        if not self.is_open:
            raise portNotOpenError
        self._port_handle.BreakState = bool(self._break_state)

    def _update_rts_state(self):
        """Set terminal status line: Request To Send"""
        if not self.is_open:
            raise portNotOpenError
        self._port_handle.RtsEnable = bool(self._rts_state)

    def _update_dtr_state(self):
        """Set terminal status line: Data Terminal Ready"""
        if not self.is_open:
            raise portNotOpenError
        self._port_handle.DtrEnable = bool(self._dtr_state)

    @property
    def cts(self):
        """Read terminal status line: Clear To Send"""
        if not self.is_open:
            raise portNotOpenError
        return self._port_handle.CtsHolding

    @property
    def dsr(self):
        """Read terminal status line: Data Set Ready"""
        if not self.is_open:
            raise portNotOpenError
        return self._port_handle.DsrHolding

    @property
    def ri(self):
        """Read terminal status line: Ring Indicator"""
        if not self.is_open:
            raise portNotOpenError
        return False

    @property
    def cd(self):
        """Read terminal status line: Carrier Detect"""
        if not self.is_open:
            raise portNotOpenError
        return self._port_handle.CDHolding