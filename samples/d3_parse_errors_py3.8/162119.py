# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\serial\serialposix.py
import errno, fcntl, os, select, struct, sys, termios, serial
from serial.serialutil import SerialBase, SerialException, to_bytes, portNotOpenError, writeTimeoutError, Timeout

class PlatformSpecificBase(object):
    BAUDRATE_CONSTANTS = {}

    def _set_special_baudrate(self, baudrate):
        raise NotImplementedError('non-standard baudrates are not supported on this platform')

    def _set_rs485_mode(self, rs485_settings):
        raise NotImplementedError('RS485 not supported on this platform')


CMSPAR = 0
plat = sys.platform.lower()
if plat[:5] == 'linux':
    import array
    CMSPAR = 1073741824
    TCGETS2 = 2150388778
    TCSETS2 = 1076646955
    BOTHER = 4096
    TIOCGRS485 = 21550
    TIOCSRS485 = 21551
    SER_RS485_ENABLED = 1
    SER_RS485_RTS_ON_SEND = 2
    SER_RS485_RTS_AFTER_SEND = 4
    SER_RS485_RX_DURING_TX = 16

    class PlatformSpecific(PlatformSpecificBase):
        BAUDRATE_CONSTANTS = {0:0, 
         50:1, 
         75:2, 
         110:3, 
         134:4, 
         150:5, 
         200:6, 
         300:7, 
         600:8, 
         1200:9, 
         1800:10, 
         2400:11, 
         4800:12, 
         9600:13, 
         19200:14, 
         38400:15, 
         57600:4097, 
         115200:4098, 
         230400:4099, 
         460800:4100, 
         500000:4101, 
         576000:4102, 
         921600:4103, 
         1000000:4104, 
         1152000:4105, 
         1500000:4106, 
         2000000:4107, 
         2500000:4108, 
         3000000:4109, 
         3500000:4110, 
         4000000:4111}

        def _set_special_baudrate(self, baudrate):
            buf = array.array('i', [0] * 64)
            try:
                fcntl.ioctl(self.fd, TCGETS2, buf)
                buf[2] &= ~termios.CBAUD
                buf[2] |= BOTHER
                buf[9] = buf[10] = baudrate
                fcntl.ioctl(self.fd, TCSETS2, buf)
            except IOError as e:
                try:
                    raise ValueError('Failed to set custom baud rate ({}): {}'.format(baudrate, e))
                finally:
                    e = None
                    del e

        def _set_rs485_mode(self, rs485_settings):
            buf = array.array('i', [0] * 8)
            try:
                fcntl.ioctl(self.fd, TIOCGRS485, buf)
                buf[0] |= SER_RS485_ENABLED
                if rs485_settings is not None:
                    if rs485_settings.loopback:
                        buf[0] |= SER_RS485_RX_DURING_TX
                    else:
                        buf[0] &= ~SER_RS485_RX_DURING_TX
                    if rs485_settings.rts_level_for_tx:
                        buf[0] |= SER_RS485_RTS_ON_SEND
                    else:
                        buf[0] &= ~SER_RS485_RTS_ON_SEND
                    if rs485_settings.rts_level_for_rx:
                        buf[0] |= SER_RS485_RTS_AFTER_SEND
                    else:
                        buf[0] &= ~SER_RS485_RTS_AFTER_SEND
                    if rs485_settings.delay_before_tx is not None:
                        buf[1] = int(rs485_settings.delay_before_tx * 1000)
                    if rs485_settings.delay_before_rx is not None:
                        buf[2] = int(rs485_settings.delay_before_rx * 1000)
                else:
                    buf[0] = 0
                fcntl.ioctl(self.fd, TIOCSRS485, buf)
            except IOError as e:
                try:
                    raise ValueError('Failed to set RS485 mode: {}'.format(e))
                finally:
                    e = None
                    del e


elif plat == 'cygwin':

    class PlatformSpecific(PlatformSpecificBase):
        BAUDRATE_CONSTANTS = {128000:4099, 
         256000:4101, 
         500000:4103, 
         576000:4104, 
         921600:4105, 
         1000000:4106, 
         1152000:4107, 
         1500000:4108, 
         2000000:4109, 
         2500000:4110, 
         3000000:4111}


elif plat[:6] == 'darwin':
    import array
    IOSSIOSPEED = 2147767298

    class PlatformSpecific(PlatformSpecificBase):
        osx_version = os.uname()[2].split('.')
        if int(osx_version[0]) >= 8:

            def _set_special_baudrate(self, baudrate):
                buf = array.array('i', [baudrate])
                fcntl.ioctl(self.fd, IOSSIOSPEED, buf, 1)


elif plat[:3] == 'bsd' or plat[:7] == 'freebsd' or plat[:6] == 'netbsd' or plat[:7] == 'openbsd':

    class ReturnBaudrate(object):

        def __getitem__(self, key):
            return key


    class PlatformSpecific(PlatformSpecificBase):
        BAUDRATE_CONSTANTS = ReturnBaudrate()


else:

    class PlatformSpecific(PlatformSpecificBase):
        pass


TIOCMGET = getattr(termios, 'TIOCMGET', 21525)
TIOCMBIS = getattr(termios, 'TIOCMBIS', 21526)
TIOCMBIC = getattr(termios, 'TIOCMBIC', 21527)
TIOCMSET = getattr(termios, 'TIOCMSET', 21528)
TIOCM_DTR = getattr(termios, 'TIOCM_DTR', 2)
TIOCM_RTS = getattr(termios, 'TIOCM_RTS', 4)
TIOCM_CTS = getattr(termios, 'TIOCM_CTS', 32)
TIOCM_CAR = getattr(termios, 'TIOCM_CAR', 64)
TIOCM_RNG = getattr(termios, 'TIOCM_RNG', 128)
TIOCM_DSR = getattr(termios, 'TIOCM_DSR', 256)
TIOCM_CD = getattr(termios, 'TIOCM_CD', TIOCM_CAR)
TIOCM_RI = getattr(termios, 'TIOCM_RI', TIOCM_RNG)
if hasattr(termios, 'TIOCINQ'):
    TIOCINQ = termios.TIOCINQ
else:
    TIOCINQ = getattr(termios, 'FIONREAD', 21531)
TIOCOUTQ = getattr(termios, 'TIOCOUTQ', 21521)
TIOCM_zero_str = struct.pack('I', 0)
TIOCM_RTS_str = struct.pack('I', TIOCM_RTS)
TIOCM_DTR_str = struct.pack('I', TIOCM_DTR)
TIOCSBRK = getattr(termios, 'TIOCSBRK', 21543)
TIOCCBRK = getattr(termios, 'TIOCCBRK', 21544)

class Serial(SerialBase, PlatformSpecific):
    __doc__ = '    Serial port class POSIX implementation. Serial port configuration is\n    done with termios and fcntl. Runs on Linux and many other Un*x like\n    systems.\n    '

    def open(self):
        """        Open port with current settings. This may throw a SerialException
        if the port cannot be opened."""
        if self._port is None:
            raise SerialException('Port must be configured before it can be used.')
        if self.is_open:
            raise SerialException('Port is already open.')
        self.fd = None
        try:
            self.fd = os.open(self.portstr, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)
        except OSError as msg:
            try:
                self.fd = None
                raise SerialException(msg.errno, 'could not open port {}: {}'.format(self._port, msg))
            finally:
                msg = None
                del msg

        else:
            try:
                self._reconfigure_port(force_update=True)
            except:
                try:
                    os.close(self.fd)
                except:
                    pass
                else:
                    self.fd = None
                    raise
            else:
                self.is_open = True
            try:
                if not self._dsrdtr:
                    self._update_dtr_state()
                if not self._rtscts:
                    self._update_rts_state()
            except IOError as e:
                try:
                    if e.errno in (errno.EINVAL, errno.ENOTTY):
                        pass
                    else:
                        raise
                finally:
                    e = None
                    del e

            else:
                self.reset_input_buffer()
                self.pipe_abort_read_r, self.pipe_abort_read_w = os.pipe()
                self.pipe_abort_write_r, self.pipe_abort_write_w = os.pipe()
                fcntl.fcntl(self.pipe_abort_read_r, fcntl.F_SETFL, os.O_NONBLOCK)
                fcntl.fcntl(self.pipe_abort_write_r, fcntl.F_SETFL, os.O_NONBLOCK)

    def _reconfigure_port(self, force_update=False):
        """Set communication parameters on opened port."""
        if self.fd is None:
            raise SerialException('Can only operate on a valid file descriptor')
        if self._exclusive is not None:
            if self._exclusive:
                try:
                    fcntl.flock(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except IOError as msg:
                    try:
                        raise SerialException(msg.errno, 'Could not exclusively lock port {}: {}'.format(self._port, msg))
                    finally:
                        msg = None
                        del msg

            else:
                fcntl.flock(self.fd, fcntl.LOCK_UN)
        custom_baud = None
        vmin = vtime = 0
        if self._inter_byte_timeout is not None:
            vmin = 1
            vtime = int(self._inter_byte_timeout * 10)
        try:
            orig_attr = termios.tcgetattr(self.fd)
            iflag, oflag, cflag, lflag, ispeed, ospeed, cc = orig_attr
        except termios.error as msg:
            try:
                raise SerialException('Could not configure port: {}'.format(msg))
            finally:
                msg = None
                del msg

        else:
            cflag |= termios.CLOCAL | termios.CREAD
            lflag &= ~(termios.ICANON | termios.ECHO | termios.ECHOE | termios.ECHOK | termios.ECHONL | termios.ISIG | termios.IEXTEN)
        for flag in ('ECHOCTL', 'ECHOKE'):
            if hasattr(termios, flag):
                lflag &= ~getattr(termios, flag)
        else:
            oflag &= ~(termios.OPOST | termios.ONLCR | termios.OCRNL)
            iflag &= ~(termios.INLCR | termios.IGNCR | termios.ICRNL | termios.IGNBRK)
            if hasattr(termios, 'IUCLC'):
                iflag &= ~termios.IUCLC
            if hasattr(termios, 'PARMRK'):
                iflag &= ~termios.PARMRK
            try:
                ispeed = ospeed = getattr(termios, 'B{}'.format(self._baudrate))
            except AttributeError:
                try:
                    ispeed = ospeed = self.BAUDRATE_CONSTANTS[self._baudrate]
                except KeyError:
                    ispeed = ospeed = getattr(termios, 'B38400')
                    try:
                        custom_baud = int(self._baudrate)
                    except ValueError:
                        raise ValueError('Invalid baud rate: {!r}'.format(self._baudrate))
                    else:
                        if custom_baud < 0:
                            raise ValueError('Invalid baud rate: {!r}'.format(self._baudrate))

            else:
                cflag &= ~termios.CSIZE
                if self._bytesize == 8:
                    cflag |= termios.CS8
                elif self._bytesize == 7:
                    cflag |= termios.CS7
                elif self._bytesize == 6:
                    cflag |= termios.CS6
                elif self._bytesize == 5:
                    cflag |= termios.CS5
                else:
                    raise ValueError('Invalid char len: {!r}'.format(self._bytesize))
                if self._stopbits == serial.STOPBITS_ONE:
                    cflag &= ~termios.CSTOPB
                elif self._stopbits == serial.STOPBITS_ONE_POINT_FIVE:
                    cflag |= termios.CSTOPB
                elif self._stopbits == serial.STOPBITS_TWO:
                    cflag |= termios.CSTOPB
                else:
                    raise ValueError('Invalid stop bit specification: {!r}'.format(self._stopbits))
                iflag &= ~(termios.INPCK | termios.ISTRIP)
                if self._parity == serial.PARITY_NONE:
                    cflag &= ~(termios.PARENB | termios.PARODD | CMSPAR)
                elif self._parity == serial.PARITY_EVEN:
                    cflag &= ~(termios.PARODD | CMSPAR)
                    cflag |= termios.PARENB
                elif self._parity == serial.PARITY_ODD:
                    cflag &= ~CMSPAR
                    cflag |= termios.PARENB | termios.PARODD
                elif self._parity == serial.PARITY_MARK and CMSPAR:
                    cflag |= termios.PARENB | CMSPAR | termios.PARODD
                elif self._parity == serial.PARITY_SPACE and CMSPAR:
                    cflag |= termios.PARENB | CMSPAR
                    cflag &= ~termios.PARODD
                else:
                    raise ValueError('Invalid parity: {!r}'.format(self._parity))
                if hasattr(termios, 'IXANY'):
                    if self._xonxoff:
                        iflag |= termios.IXON | termios.IXOFF
                    else:
                        iflag &= ~(termios.IXON | termios.IXOFF | termios.IXANY)
                elif self._xonxoff:
                    iflag |= termios.IXON | termios.IXOFF
                else:
                    iflag &= ~(termios.IXON | termios.IXOFF)
                if hasattr(termios, 'CRTSCTS'):
                    if self._rtscts:
                        cflag |= termios.CRTSCTS
                    else:
                        cflag &= ~termios.CRTSCTS
                elif hasattr(termios, 'CNEW_RTSCTS'):
                    if self._rtscts:
                        cflag |= termios.CNEW_RTSCTS
                    else:
                        cflag &= ~termios.CNEW_RTSCTS
                if vmin < 0 or (vmin > 255):
                    raise ValueError('Invalid vmin: {!r}'.format(vmin))
                cc[termios.VMIN] = vmin
                if vtime < 0 or (vtime > 255):
                    raise ValueError('Invalid vtime: {!r}'.format(vtime))
                cc[termios.VTIME] = vtime
                if force_update or ([iflag, oflag, cflag, lflag, ispeed, ospeed, cc] != orig_attr):
                    termios.tcsetattr(self.fd, termios.TCSANOW, [
                     iflag, oflag, cflag, lflag, ispeed, ospeed, cc])
                if custom_baud is not None:
                    self._set_special_baudrate(custom_baud)
                if self._rs485_mode is not None:
                    self._set_rs485_mode(self._rs485_mode)

    def close(self):
        """Close port"""
        if self.is_open:
            if self.fd is not None:
                os.close(self.fd)
                self.fd = None
                os.close(self.pipe_abort_read_w)
                os.close(self.pipe_abort_read_r)
                os.close(self.pipe_abort_write_w)
                os.close(self.pipe_abort_write_r)
                self.pipe_abort_read_r, self.pipe_abort_read_w = (None, None)
                self.pipe_abort_write_r, self.pipe_abort_write_w = (None, None)
            self.is_open = False

    @property
    def in_waiting(self):
        """Return the number of bytes currently in the input buffer."""
        s = fcntl.ioctl(self.fd, TIOCINQ, TIOCM_zero_str)
        return struct.unpack('I', s)[0]

    def read--- This code section failed: ---

 L. 477         0  LOAD_FAST                'self'
                2  LOAD_ATTR                is_open
                4  POP_JUMP_IF_TRUE     10  'to 10'

 L. 478         6  LOAD_GLOBAL              portNotOpenError
                8  RAISE_VARARGS_1       1  'exception instance'
             10_0  COME_FROM             4  '4'

 L. 479        10  LOAD_GLOBAL              bytearray
               12  CALL_FUNCTION_0       0  ''
               14  STORE_FAST               'read'

 L. 480        16  LOAD_GLOBAL              Timeout
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                _timeout
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'timeout'
             26_0  COME_FROM           338  '338'
             26_1  COME_FROM           332  '332'

 L. 481        26  LOAD_GLOBAL              len
               28  LOAD_FAST                'read'
               30  CALL_FUNCTION_1       1  ''
               32  LOAD_FAST                'size'
               34  COMPARE_OP               <
            36_38  POP_JUMP_IF_FALSE   340  'to 340'

 L. 482        40  SETUP_FINALLY       164  'to 164'

 L. 483        42  LOAD_GLOBAL              select
               44  LOAD_METHOD              select
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                fd
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                pipe_abort_read_r
               54  BUILD_LIST_2          2 
               56  BUILD_LIST_0          0 
               58  BUILD_LIST_0          0 
               60  LOAD_FAST                'timeout'
               62  LOAD_METHOD              time_left
               64  CALL_METHOD_0         0  ''
               66  CALL_METHOD_4         4  ''
               68  UNPACK_SEQUENCE_3     3 
               70  STORE_FAST               'ready'
               72  STORE_FAST               '_'
               74  STORE_FAST               '_'

 L. 484        76  LOAD_FAST                'self'
               78  LOAD_ATTR                pipe_abort_read_r
               80  LOAD_FAST                'ready'
               82  COMPARE_OP               in
               84  POP_JUMP_IF_FALSE   106  'to 106'

 L. 485        86  LOAD_GLOBAL              os
               88  LOAD_METHOD              read
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                pipe_abort_read_r
               94  LOAD_CONST               1000
               96  CALL_METHOD_2         2  ''
               98  POP_TOP          

 L. 486       100  POP_BLOCK        
          102_104  BREAK_LOOP          340  'to 340'
            106_0  COME_FROM            84  '84'

 L. 491       106  LOAD_FAST                'ready'
              108  POP_JUMP_IF_TRUE    116  'to 116'

 L. 492       110  POP_BLOCK        
          112_114  BREAK_LOOP          340  'to 340'
            116_0  COME_FROM           108  '108'

 L. 493       116  LOAD_GLOBAL              os
              118  LOAD_METHOD              read
              120  LOAD_FAST                'self'
              122  LOAD_ATTR                fd
              124  LOAD_FAST                'size'
              126  LOAD_GLOBAL              len
              128  LOAD_FAST                'read'
              130  CALL_FUNCTION_1       1  ''
              132  BINARY_SUBTRACT  
              134  CALL_METHOD_2         2  ''
              136  STORE_FAST               'buf'

 L. 496       138  LOAD_FAST                'buf'
              140  POP_JUMP_IF_TRUE    150  'to 150'

 L. 500       142  LOAD_GLOBAL              SerialException

 L. 501       144  LOAD_STR                 'device reports readiness to read but returned no data (device disconnected or multiple access on port?)'

 L. 500       146  CALL_FUNCTION_1       1  ''
              148  RAISE_VARARGS_1       1  'exception instance'
            150_0  COME_FROM           140  '140'

 L. 503       150  LOAD_FAST                'read'
              152  LOAD_METHOD              extend
              154  LOAD_FAST                'buf'
              156  CALL_METHOD_1         1  ''
              158  POP_TOP          
              160  POP_BLOCK        
              162  JUMP_FORWARD        326  'to 326'
            164_0  COME_FROM_FINALLY    40  '40'

 L. 504       164  DUP_TOP          
              166  LOAD_GLOBAL              OSError
              168  COMPARE_OP               exception-match
              170  POP_JUMP_IF_FALSE   240  'to 240'
              172  POP_TOP          
              174  STORE_FAST               'e'
              176  POP_TOP          
              178  SETUP_FINALLY       228  'to 228'

 L. 508       180  LOAD_FAST                'e'
              182  LOAD_ATTR                errno
              184  LOAD_GLOBAL              errno
              186  LOAD_ATTR                EAGAIN
              188  LOAD_GLOBAL              errno
              190  LOAD_ATTR                EALREADY
              192  LOAD_GLOBAL              errno
              194  LOAD_ATTR                EWOULDBLOCK
              196  LOAD_GLOBAL              errno
              198  LOAD_ATTR                EINPROGRESS
              200  LOAD_GLOBAL              errno
              202  LOAD_ATTR                EINTR
              204  BUILD_TUPLE_5         5 
              206  COMPARE_OP               not-in
              208  POP_JUMP_IF_FALSE   224  'to 224'

 L. 509       210  LOAD_GLOBAL              SerialException
              212  LOAD_STR                 'read failed: {}'
              214  LOAD_METHOD              format
              216  LOAD_FAST                'e'
              218  CALL_METHOD_1         1  ''
              220  CALL_FUNCTION_1       1  ''
              222  RAISE_VARARGS_1       1  'exception instance'
            224_0  COME_FROM           208  '208'
              224  POP_BLOCK        
              226  BEGIN_FINALLY    
            228_0  COME_FROM_FINALLY   178  '178'
              228  LOAD_CONST               None
              230  STORE_FAST               'e'
              232  DELETE_FAST              'e'
              234  END_FINALLY      
              236  POP_EXCEPT       
              238  JUMP_FORWARD        326  'to 326'
            240_0  COME_FROM           170  '170'

 L. 510       240  DUP_TOP          
              242  LOAD_GLOBAL              select
              244  LOAD_ATTR                error
              246  COMPARE_OP               exception-match
          248_250  POP_JUMP_IF_FALSE   324  'to 324'
              252  POP_TOP          
              254  STORE_FAST               'e'
              256  POP_TOP          
              258  SETUP_FINALLY       312  'to 312'

 L. 514       260  LOAD_FAST                'e'
              262  LOAD_CONST               0
              264  BINARY_SUBSCR    
              266  LOAD_GLOBAL              errno
              268  LOAD_ATTR                EAGAIN
              270  LOAD_GLOBAL              errno
              272  LOAD_ATTR                EALREADY
              274  LOAD_GLOBAL              errno
              276  LOAD_ATTR                EWOULDBLOCK
              278  LOAD_GLOBAL              errno
              280  LOAD_ATTR                EINPROGRESS
              282  LOAD_GLOBAL              errno
              284  LOAD_ATTR                EINTR
              286  BUILD_TUPLE_5         5 
              288  COMPARE_OP               not-in
          290_292  POP_JUMP_IF_FALSE   308  'to 308'

 L. 515       294  LOAD_GLOBAL              SerialException
              296  LOAD_STR                 'read failed: {}'
              298  LOAD_METHOD              format
              300  LOAD_FAST                'e'
              302  CALL_METHOD_1         1  ''
              304  CALL_FUNCTION_1       1  ''
              306  RAISE_VARARGS_1       1  'exception instance'
            308_0  COME_FROM           290  '290'
              308  POP_BLOCK        
              310  BEGIN_FINALLY    
            312_0  COME_FROM_FINALLY   258  '258'
              312  LOAD_CONST               None
              314  STORE_FAST               'e'
              316  DELETE_FAST              'e'
              318  END_FINALLY      
              320  POP_EXCEPT       
              322  JUMP_FORWARD        326  'to 326'
            324_0  COME_FROM           248  '248'
              324  END_FINALLY      
            326_0  COME_FROM           322  '322'
            326_1  COME_FROM           238  '238'
            326_2  COME_FROM           162  '162'

 L. 516       326  LOAD_FAST                'timeout'
              328  LOAD_METHOD              expired
              330  CALL_METHOD_0         0  ''
              332  POP_JUMP_IF_FALSE_BACK    26  'to 26'

 L. 517   334_336  JUMP_FORWARD        340  'to 340'
              338  JUMP_BACK            26  'to 26'
            340_0  COME_FROM           334  '334'
            340_1  COME_FROM           112  '112'
            340_2  COME_FROM           102  '102'
            340_3  COME_FROM            36  '36'

 L. 518       340  LOAD_GLOBAL              bytes
              342  LOAD_FAST                'read'
              344  CALL_FUNCTION_1       1  ''
              346  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 338

    def cancel_read(self):
        if self.is_open:
            os.write(self.pipe_abort_read_w, b'x')

    def cancel_write(self):
        if self.is_open:
            os.write(self.pipe_abort_write_w, b'x')

    def write(self, data):
        """Output the given byte string over the serial port."""
        if not self.is_open:
            raise portNotOpenError
        d = to_bytes(data)
        tx_len = length = len(d)
        timeout = Timeout(self._write_timeout)
        while True:
            if tx_len > 0:
                try:
                    n = os.write(self.fd, d)
                    if timeout.is_non_blocking:
                        return n
                    if not timeout.is_infinite:
                        if timeout.expired():
                            raise writeTimeoutError
                        abort, ready, _ = select.select([self.pipe_abort_write_r], [self.fd], [], timeout.time_left())
                        if abort:
                            os.read(self.pipe_abort_write_r, 1000)
                            break
                        assert ready
                    else:
                        assert timeout.time_left() is None
                        abort, ready, _ = select.select([self.pipe_abort_write_r], [self.fd], [], None)
                        if abort:
                            os.read(self.pipe_abort_write_r, 1)
                            break
                        if not ready:
                            raise SerialException('write failed (select)')
                    d = d[n:]
                    tx_len -= n
                except SerialException:
                    raise
                except OSError as e:
                    try:
                        if e.errno not in (errno.EAGAIN, errno.EALREADY, errno.EWOULDBLOCK, errno.EINPROGRESS, errno.EINTR):
                            raise SerialException('write failed: {}'.format(e))
                    finally:
                        e = None
                        del e

                except select.error as e:
                    try:
                        if e[0] not in (errno.EAGAIN, errno.EALREADY, errno.EWOULDBLOCK, errno.EINPROGRESS, errno.EINTR):
                            raise SerialException('write failed: {}'.format(e))
                    finally:
                        e = None
                        del e

                else:
                    if not timeout.is_non_blocking:
                        if timeout.expired():
                            raise writeTimeoutError

        return length - len(d)

    def flush(self):
        """        Flush of file like objects. In this case, wait until all data
        is written.
        """
        if not self.is_open:
            raise portNotOpenError
        termios.tcdrain(self.fd)

    def reset_input_buffer(self):
        """Clear input buffer, discarding all that is in the buffer."""
        if not self.is_open:
            raise portNotOpenError
        termios.tcflush(self.fd, termios.TCIFLUSH)

    def reset_output_buffer(self):
        """        Clear output buffer, aborting the current output and discarding all
        that is in the buffer.
        """
        if not self.is_open:
            raise portNotOpenError
        termios.tcflush(self.fd, termios.TCOFLUSH)

    def send_break(self, duration=0.25):
        """        Send break condition. Timed, returns to idle state after given
        duration.
        """
        if not self.is_open:
            raise portNotOpenError
        termios.tcsendbreak(self.fd, int(duration / 0.25))

    def _update_break_state(self):
        """        Set break: Controls TXD. When active, no transmitting is possible.
        """
        if self._break_state:
            fcntl.ioctl(self.fd, TIOCSBRK)
        else:
            fcntl.ioctl(self.fd, TIOCCBRK)

    def _update_rts_state(self):
        """Set terminal status line: Request To Send"""
        if self._rts_state:
            fcntl.ioctl(self.fd, TIOCMBIS, TIOCM_RTS_str)
        else:
            fcntl.ioctl(self.fd, TIOCMBIC, TIOCM_RTS_str)

    def _update_dtr_state(self):
        """Set terminal status line: Data Terminal Ready"""
        if self._dtr_state:
            fcntl.ioctl(self.fd, TIOCMBIS, TIOCM_DTR_str)
        else:
            fcntl.ioctl(self.fd, TIOCMBIC, TIOCM_DTR_str)

    @property
    def cts(self):
        """Read terminal status line: Clear To Send"""
        if not self.is_open:
            raise portNotOpenError
        s = fcntl.ioctl(self.fd, TIOCMGET, TIOCM_zero_str)
        return struct.unpack('I', s)[0] & TIOCM_CTS != 0

    @property
    def dsr(self):
        """Read terminal status line: Data Set Ready"""
        if not self.is_open:
            raise portNotOpenError
        s = fcntl.ioctl(self.fd, TIOCMGET, TIOCM_zero_str)
        return struct.unpack('I', s)[0] & TIOCM_DSR != 0

    @property
    def ri(self):
        """Read terminal status line: Ring Indicator"""
        if not self.is_open:
            raise portNotOpenError
        s = fcntl.ioctl(self.fd, TIOCMGET, TIOCM_zero_str)
        return struct.unpack('I', s)[0] & TIOCM_RI != 0

    @property
    def cd(self):
        """Read terminal status line: Carrier Detect"""
        if not self.is_open:
            raise portNotOpenError
        s = fcntl.ioctl(self.fd, TIOCMGET, TIOCM_zero_str)
        return struct.unpack('I', s)[0] & TIOCM_CD != 0

    @property
    def out_waiting(self):
        """Return the number of bytes currently in the output buffer."""
        s = fcntl.ioctl(self.fd, TIOCOUTQ, TIOCM_zero_str)
        return struct.unpack('I', s)[0]

    def fileno(self):
        """        For easier use of the serial port instance with select.
        WARNING: this function is not portable to different platforms!
        """
        if not self.is_open:
            raise portNotOpenError
        return self.fd

    def set_input_flow_control(self, enable=True):
        """        Manually control flow - when software flow control is enabled.
        This will send XON (true) or XOFF (false) to the other device.
        WARNING: this function is not portable to different platforms!
        """
        if not self.is_open:
            raise portNotOpenError
        if enable:
            termios.tcflow(self.fd, termios.TCION)
        else:
            termios.tcflow(self.fd, termios.TCIOFF)

    def set_output_flow_control(self, enable=True):
        """        Manually control flow of outgoing data - when hardware or software flow
        control is enabled.
        WARNING: this function is not portable to different platforms!
        """
        if not self.is_open:
            raise portNotOpenError
        if enable:
            termios.tcflow(self.fd, termios.TCOON)
        else:
            termios.tcflow(self.fd, termios.TCOOFF)

    def nonblocking(self):
        """DEPRECATED - has no use"""
        import warnings
        warnings.warn('nonblocking() has no effect, already nonblocking', DeprecationWarning)


class PosixPollSerial(Serial):
    __doc__ = "    Poll based read implementation. Not all systems support poll properly.\n    However this one has better handling of errors, such as a device\n    disconnecting while it's in use (e.g. USB-serial unplugged).\n    "

    def read(self, size=1):
        """        Read size bytes from the serial port. If a timeout is set it may
        return less characters as requested. With no timeout it will block
        until the requested number of bytes is read.
        """
        if not self.is_open:
            raise portNotOpenError
        read = bytearray()
        poll = select.poll()
        poll.register(self.fd, select.POLLIN | select.POLLERR | select.POLLHUP | select.POLLNVAL)
        if size > 0:
            while True:
                if len(read) < size:
                    for fd, event in poll.poll(self._timeout * 1000):
                        if event & (select.POLLERR | select.POLLHUP | select.POLLNVAL):
                            raise SerialException('device reports error (poll)')
                    else:
                        buf = os.read(self.fd, size - len(read))
                        read.extend(buf)
                        if not (self._timeout is not None and self._timeout >= 0):
                            if self._inter_byte_timeout is not None:
                                if self._inter_byte_timeout > 0:
                                    pass
                                if not buf:
                                    break

            return bytes(read)


class VTIMESerial(Serial):
    __doc__ = '    Implement timeout using vtime of tty device instead of using select.\n    This means that no inter character timeout can be specified and that\n    the error handling is degraded.\n\n    Overall timeout is disabled when inter-character timeout is used.\n    '

    def _reconfigure_port(self, force_update=True):
        """Set communication parameters on opened port."""
        super(VTIMESerial, self)._reconfigure_port()
        fcntl.fcntl(self.fd, fcntl.F_SETFL, 0)
        if self._inter_byte_timeout is not None:
            vmin = 1
            vtime = int(self._inter_byte_timeout * 10)
        elif self._timeout is None:
            vmin = 1
            vtime = 0
        else:
            vmin = 0
            vtime = int(self._timeout * 10)
        try:
            orig_attr = termios.tcgetattr(self.fd)
            iflag, oflag, cflag, lflag, ispeed, ospeed, cc = orig_attr
        except termios.error as msg:
            try:
                raise serial.SerialException('Could not configure port: {}'.format(msg))
            finally:
                msg = None
                del msg

        else:
            if vtime < 0 or (vtime > 255):
                raise ValueError('Invalid vtime: {!r}'.format(vtime))
            cc[termios.VTIME] = vtime
            cc[termios.VMIN] = vmin
            termios.tcsetattr(self.fd, termios.TCSANOW, [
             iflag, oflag, cflag, lflag, ispeed, ospeed, cc])

    def read(self, size=1):
        """        Read size bytes from the serial port. If a timeout is set it may
        return less characters as requested. With no timeout it will block
        until the requested number of bytes is read.
        """
        if not self.is_open:
            raise portNotOpenError
        read = bytearray()
        while True:
            if len(read) < size:
                buf = os.read(self.fd, size - len(read))
                if not buf:
                    pass
                else:
                    read.extend(buf)

        return bytes(read)

    cancel_read = property()