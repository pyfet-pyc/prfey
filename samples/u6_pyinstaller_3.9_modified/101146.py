# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: asyncio\transports.py
"""Abstract Transport class."""
__all__ = ('BaseTransport', 'ReadTransport', 'WriteTransport', 'Transport', 'DatagramTransport',
           'SubprocessTransport')

class BaseTransport:
    __doc__ = 'Base class for transports.'
    __slots__ = ('_extra', )

    def __init__--- This code section failed: ---

 L.  15         0  LOAD_FAST                'extra'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L.  16         8  BUILD_MAP_0           0 
               10  STORE_FAST               'extra'
             12_0  COME_FROM             6  '6'

 L.  17        12  LOAD_FAST                'extra'
               14  LOAD_FAST                'self'
               16  STORE_ATTR               _extra

Parse error at or near `None' instruction at offset -1

    def get_extra_info(self, name, default=None):
        """Get optional transport information."""
        return self._extra.get(name, default)

    def is_closing(self):
        """Return True if the transport is closing or closed."""
        raise NotImplementedError

    def close(self):
        """Close the transport.

        Buffered data will be flushed asynchronously.  No more data
        will be received.  After all buffered data is flushed, the
        protocol's connection_lost() method will (eventually) be
        called with None as its argument.
        """
        raise NotImplementedError

    def set_protocol(self, protocol):
        """Set a new protocol."""
        raise NotImplementedError

    def get_protocol(self):
        """Return the current protocol."""
        raise NotImplementedError


class ReadTransport(BaseTransport):
    __doc__ = 'Interface for read-only transports.'
    __slots__ = ()

    def is_reading(self):
        """Return True if the transport is receiving."""
        raise NotImplementedError

    def pause_reading(self):
        """Pause the receiving end.

        No data will be passed to the protocol's data_received()
        method until resume_reading() is called.
        """
        raise NotImplementedError

    def resume_reading(self):
        """Resume the receiving end.

        Data received will once again be passed to the protocol's
        data_received() method.
        """
        raise NotImplementedError


class WriteTransport(BaseTransport):
    __doc__ = 'Interface for write-only transports.'
    __slots__ = ()

    def set_write_buffer_limits(self, high=None, low=None):
        """Set the high- and low-water limits for write flow control.

        These two values control when to call the protocol's
        pause_writing() and resume_writing() methods.  If specified,
        the low-water limit must be less than or equal to the
        high-water limit.  Neither value can be negative.

        The defaults are implementation-specific.  If only the
        high-water limit is given, the low-water limit defaults to an
        implementation-specific value less than or equal to the
        high-water limit.  Setting high to zero forces low to zero as
        well, and causes pause_writing() to be called whenever the
        buffer becomes non-empty.  Setting low to zero causes
        resume_writing() to be called only once the buffer is empty.
        Use of zero for either limit is generally sub-optimal as it
        reduces opportunities for doing I/O and computation
        concurrently.
        """
        raise NotImplementedError

    def get_write_buffer_size(self):
        """Return the current size of the write buffer."""
        raise NotImplementedError

    def write(self, data):
        """Write some data bytes to the transport.

        This does not block; it buffers the data and arranges for it
        to be sent out asynchronously.
        """
        raise NotImplementedError

    def writelines(self, list_of_data):
        """Write a list (or any iterable) of data bytes to the transport.

        The default implementation concatenates the arguments and
        calls write() on the result.
        """
        data = (b'').join(list_of_data)
        self.write(data)

    def write_eof(self):
        """Close the write end after flushing buffered data.

        (This is like typing ^D into a UNIX program reading from stdin.)

        Data may still be received.
        """
        raise NotImplementedError

    def can_write_eof(self):
        """Return True if this transport supports write_eof(), False if not."""
        raise NotImplementedError

    def abort(self):
        """Close the transport immediately.

        Buffered data will be lost.  No more data will be received.
        The protocol's connection_lost() method will (eventually) be
        called with None as its argument.
        """
        raise NotImplementedError


class Transport(ReadTransport, WriteTransport):
    __doc__ = "Interface representing a bidirectional transport.\n\n    There may be several implementations, but typically, the user does\n    not implement new transports; rather, the platform provides some\n    useful transports that are implemented using the platform's best\n    practices.\n\n    The user never instantiates a transport directly; they call a\n    utility function, passing it a protocol factory and other\n    information necessary to create the transport and protocol.  (E.g.\n    EventLoop.create_connection() or EventLoop.create_server().)\n\n    The utility function will asynchronously create a transport and a\n    protocol and hook them up by calling the protocol's\n    connection_made() method, passing it the transport.\n\n    The implementation here raises NotImplemented for every method\n    except writelines(), which calls write() in a loop.\n    "
    __slots__ = ()


class DatagramTransport(BaseTransport):
    __doc__ = 'Interface for datagram (UDP) transports.'
    __slots__ = ()

    def sendto(self, data, addr=None):
        """Send data to the transport.

        This does not block; it buffers the data and arranges for it
        to be sent out asynchronously.
        addr is target socket address.
        If addr is None use target address pointed on transport creation.
        """
        raise NotImplementedError

    def abort(self):
        """Close the transport immediately.

        Buffered data will be lost.  No more data will be received.
        The protocol's connection_lost() method will (eventually) be
        called with None as its argument.
        """
        raise NotImplementedError


class SubprocessTransport(BaseTransport):
    __slots__ = ()

    def get_pid(self):
        """Get subprocess id."""
        raise NotImplementedError

    def get_returncode(self):
        """Get subprocess returncode.

        See also
        http://docs.python.org/3/library/subprocess#subprocess.Popen.returncode
        """
        raise NotImplementedError

    def get_pipe_transport(self, fd):
        """Get transport for pipe with number fd."""
        raise NotImplementedError

    def send_signal(self, signal):
        """Send signal to subprocess.

        See also:
        docs.python.org/3/library/subprocess#subprocess.Popen.send_signal
        """
        raise NotImplementedError

    def terminate(self):
        """Stop the subprocess.

        Alias for close() method.

        On Posix OSs the method sends SIGTERM to the subprocess.
        On Windows the Win32 API function TerminateProcess()
         is called to stop the subprocess.

        See also:
        http://docs.python.org/3/library/subprocess#subprocess.Popen.terminate
        """
        raise NotImplementedError

    def kill(self):
        """Kill the subprocess.

        On Posix OSs the function sends SIGKILL to the subprocess.
        On Windows kill() is an alias for terminate().

        See also:
        http://docs.python.org/3/library/subprocess#subprocess.Popen.kill
        """
        raise NotImplementedError


class _FlowControlMixin(Transport):
    __doc__ = "All the logic for (write) flow control in a mix-in base class.\n\n    The subclass must implement get_write_buffer_size().  It must call\n    _maybe_pause_protocol() whenever the write buffer size increases,\n    and _maybe_resume_protocol() whenever it decreases.  It may also\n    override set_write_buffer_limits() (e.g. to specify different\n    defaults).\n\n    The subclass constructor must call super().__init__(extra).  This\n    will call set_write_buffer_limits().\n\n    The user may call set_write_buffer_limits() and\n    get_write_buffer_size(), and their protocol's pause_writing() and\n    resume_writing() may be called.\n    "
    __slots__ = ('_loop', '_protocol_paused', '_high_water', '_low_water')

    def __init__--- This code section failed: ---

 L. 265         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_METHOD              __init__
                6  LOAD_FAST                'extra'
                8  CALL_METHOD_1         1  ''
               10  POP_TOP          

 L. 266        12  LOAD_FAST                'loop'
               14  LOAD_CONST               None
               16  <117>                 1  ''
               18  POP_JUMP_IF_TRUE     24  'to 24'
               20  <74>             
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            18  '18'

 L. 267        24  LOAD_FAST                'loop'
               26  LOAD_FAST                'self'
               28  STORE_ATTR               _loop

 L. 268        30  LOAD_CONST               False
               32  LOAD_FAST                'self'
               34  STORE_ATTR               _protocol_paused

 L. 269        36  LOAD_FAST                'self'
               38  LOAD_METHOD              _set_write_buffer_limits
               40  CALL_METHOD_0         0  ''
               42  POP_TOP          

Parse error at or near `<117>' instruction at offset 16

    def _maybe_pause_protocol--- This code section failed: ---

 L. 272         0  LOAD_FAST                'self'
                2  LOAD_METHOD              get_write_buffer_size
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'size'

 L. 273         8  LOAD_FAST                'size'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _high_water
               14  COMPARE_OP               <=
               16  POP_JUMP_IF_FALSE    22  'to 22'

 L. 274        18  LOAD_CONST               None
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L. 275        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _protocol_paused
               26  POP_JUMP_IF_TRUE    132  'to 132'

 L. 276        28  LOAD_CONST               True
               30  LOAD_FAST                'self'
               32  STORE_ATTR               _protocol_paused

 L. 277        34  SETUP_FINALLY        50  'to 50'

 L. 278        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _protocol
               40  LOAD_METHOD              pause_writing
               42  CALL_METHOD_0         0  ''
               44  POP_TOP          
               46  POP_BLOCK        
               48  JUMP_FORWARD        132  'to 132'
             50_0  COME_FROM_FINALLY    34  '34'

 L. 279        50  DUP_TOP          
               52  LOAD_GLOBAL              SystemExit
               54  LOAD_GLOBAL              KeyboardInterrupt
               56  BUILD_TUPLE_2         2 
               58  <121>                72  ''
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L. 280        66  RAISE_VARARGS_0       0  'reraise'
               68  POP_EXCEPT       
               70  JUMP_FORWARD        132  'to 132'

 L. 281        72  DUP_TOP          
               74  LOAD_GLOBAL              BaseException
               76  <121>               130  ''
               78  POP_TOP          
               80  STORE_FAST               'exc'
               82  POP_TOP          
               84  SETUP_FINALLY       122  'to 122'

 L. 282        86  LOAD_FAST                'self'
               88  LOAD_ATTR                _loop
               90  LOAD_METHOD              call_exception_handler

 L. 283        92  LOAD_STR                 'protocol.pause_writing() failed'

 L. 284        94  LOAD_FAST                'exc'

 L. 285        96  LOAD_FAST                'self'

 L. 286        98  LOAD_FAST                'self'
              100  LOAD_ATTR                _protocol

 L. 282       102  LOAD_CONST               ('message', 'exception', 'transport', 'protocol')
              104  BUILD_CONST_KEY_MAP_4     4 
              106  CALL_METHOD_1         1  ''
              108  POP_TOP          
              110  POP_BLOCK        
              112  POP_EXCEPT       
              114  LOAD_CONST               None
              116  STORE_FAST               'exc'
              118  DELETE_FAST              'exc'
              120  JUMP_FORWARD        132  'to 132'
            122_0  COME_FROM_FINALLY    84  '84'
              122  LOAD_CONST               None
              124  STORE_FAST               'exc'
              126  DELETE_FAST              'exc'
              128  <48>             
              130  <48>             
            132_0  COME_FROM           120  '120'
            132_1  COME_FROM            70  '70'
            132_2  COME_FROM            48  '48'
            132_3  COME_FROM            26  '26'

Parse error at or near `<121>' instruction at offset 58

    def _maybe_resume_protocol--- This code section failed: ---

 L. 290         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _protocol_paused
                4  POP_JUMP_IF_FALSE   124  'to 124'

 L. 291         6  LOAD_FAST                'self'
                8  LOAD_METHOD              get_write_buffer_size
               10  CALL_METHOD_0         0  ''
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                _low_water
               16  COMPARE_OP               <=

 L. 290        18  POP_JUMP_IF_FALSE   124  'to 124'

 L. 292        20  LOAD_CONST               False
               22  LOAD_FAST                'self'
               24  STORE_ATTR               _protocol_paused

 L. 293        26  SETUP_FINALLY        42  'to 42'

 L. 294        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _protocol
               32  LOAD_METHOD              resume_writing
               34  CALL_METHOD_0         0  ''
               36  POP_TOP          
               38  POP_BLOCK        
               40  JUMP_FORWARD        124  'to 124'
             42_0  COME_FROM_FINALLY    26  '26'

 L. 295        42  DUP_TOP          
               44  LOAD_GLOBAL              SystemExit
               46  LOAD_GLOBAL              KeyboardInterrupt
               48  BUILD_TUPLE_2         2 
               50  <121>                64  ''
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          

 L. 296        58  RAISE_VARARGS_0       0  'reraise'
               60  POP_EXCEPT       
               62  JUMP_FORWARD        124  'to 124'

 L. 297        64  DUP_TOP          
               66  LOAD_GLOBAL              BaseException
               68  <121>               122  ''
               70  POP_TOP          
               72  STORE_FAST               'exc'
               74  POP_TOP          
               76  SETUP_FINALLY       114  'to 114'

 L. 298        78  LOAD_FAST                'self'
               80  LOAD_ATTR                _loop
               82  LOAD_METHOD              call_exception_handler

 L. 299        84  LOAD_STR                 'protocol.resume_writing() failed'

 L. 300        86  LOAD_FAST                'exc'

 L. 301        88  LOAD_FAST                'self'

 L. 302        90  LOAD_FAST                'self'
               92  LOAD_ATTR                _protocol

 L. 298        94  LOAD_CONST               ('message', 'exception', 'transport', 'protocol')
               96  BUILD_CONST_KEY_MAP_4     4 
               98  CALL_METHOD_1         1  ''
              100  POP_TOP          
              102  POP_BLOCK        
              104  POP_EXCEPT       
              106  LOAD_CONST               None
              108  STORE_FAST               'exc'
              110  DELETE_FAST              'exc'
              112  JUMP_FORWARD        124  'to 124'
            114_0  COME_FROM_FINALLY    76  '76'
              114  LOAD_CONST               None
              116  STORE_FAST               'exc'
              118  DELETE_FAST              'exc'
              120  <48>             
              122  <48>             
            124_0  COME_FROM           112  '112'
            124_1  COME_FROM            62  '62'
            124_2  COME_FROM            40  '40'
            124_3  COME_FROM            18  '18'
            124_4  COME_FROM             4  '4'

Parse error at or near `<121>' instruction at offset 50

    def get_write_buffer_limits(self):
        return (
         self._low_water, self._high_water)

    def _set_write_buffer_limits--- This code section failed: ---

 L. 309         0  LOAD_FAST                'high'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    30  'to 30'

 L. 310         8  LOAD_FAST                'low'
               10  LOAD_CONST               None
               12  <117>                 0  ''
               14  POP_JUMP_IF_FALSE    22  'to 22'

 L. 311        16  LOAD_CONST               65536
               18  STORE_FAST               'high'
               20  JUMP_FORWARD         30  'to 30'
             22_0  COME_FROM            14  '14'

 L. 313        22  LOAD_CONST               4
               24  LOAD_FAST                'low'
               26  BINARY_MULTIPLY  
               28  STORE_FAST               'high'
             30_0  COME_FROM            20  '20'
             30_1  COME_FROM             6  '6'

 L. 314        30  LOAD_FAST                'low'
               32  LOAD_CONST               None
               34  <117>                 0  ''
               36  POP_JUMP_IF_FALSE    46  'to 46'

 L. 315        38  LOAD_FAST                'high'
               40  LOAD_CONST               4
               42  BINARY_FLOOR_DIVIDE
               44  STORE_FAST               'low'
             46_0  COME_FROM            36  '36'

 L. 317        46  LOAD_FAST                'high'
               48  LOAD_FAST                'low'
               50  DUP_TOP          
               52  ROT_THREE        
               54  COMPARE_OP               >=
               56  POP_JUMP_IF_FALSE    66  'to 66'
               58  LOAD_CONST               0
               60  COMPARE_OP               >=
               62  POP_JUMP_IF_TRUE     90  'to 90'
               64  JUMP_FORWARD         68  'to 68'
             66_0  COME_FROM            56  '56'
               66  POP_TOP          
             68_0  COME_FROM            64  '64'

 L. 318        68  LOAD_GLOBAL              ValueError

 L. 319        70  LOAD_STR                 'high ('
               72  LOAD_FAST                'high'
               74  FORMAT_VALUE          2  '!r'
               76  LOAD_STR                 ') must be >= low ('
               78  LOAD_FAST                'low'
               80  FORMAT_VALUE          2  '!r'
               82  LOAD_STR                 ') must be >= 0'
               84  BUILD_STRING_5        5 

 L. 318        86  CALL_FUNCTION_1       1  ''
               88  RAISE_VARARGS_1       1  'exception instance'
             90_0  COME_FROM            62  '62'

 L. 321        90  LOAD_FAST                'high'
               92  LOAD_FAST                'self'
               94  STORE_ATTR               _high_water

 L. 322        96  LOAD_FAST                'low'
               98  LOAD_FAST                'self'
              100  STORE_ATTR               _low_water

Parse error at or near `None' instruction at offset -1

    def set_write_buffer_limits(self, high=None, low=None):
        self._set_write_buffer_limits(high=high, low=low)
        self._maybe_pause_protocol

    def get_write_buffer_size(self):
        raise NotImplementedError