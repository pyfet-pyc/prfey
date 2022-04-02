# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\paramiko\channel.py
"""
Abstraction for an SSH2 channel.
"""
import binascii, os, socket, time, threading
from functools import wraps
from paramiko import util
from paramiko.common import cMSG_CHANNEL_REQUEST, cMSG_CHANNEL_WINDOW_ADJUST, cMSG_CHANNEL_DATA, cMSG_CHANNEL_EXTENDED_DATA, DEBUG, ERROR, cMSG_CHANNEL_SUCCESS, cMSG_CHANNEL_FAILURE, cMSG_CHANNEL_EOF, cMSG_CHANNEL_CLOSE
from paramiko.message import Message
from paramiko.py3compat import bytes_types
from paramiko.ssh_exception import SSHException
from paramiko.file import BufferedFile
from paramiko.buffered_pipe import BufferedPipe, PipeTimeout
from paramiko import pipe
from paramiko.util import ClosingContextManager

def open_only(func):
    """
    Decorator for `.Channel` methods which performs an openness check.

    :raises:
        `.SSHException` -- If the wrapped method is called on an unopened
        `.Channel`.
    """

    @wraps(func)
    def _check--- This code section failed: ---

 L.  66         0  LOAD_FAST                'self'
                2  LOAD_ATTR                closed
                4  POP_JUMP_IF_TRUE     24  'to 24'

 L.  67         6  LOAD_FAST                'self'
                8  LOAD_ATTR                eof_received
               10  POP_JUMP_IF_TRUE     24  'to 24'

 L.  68        12  LOAD_FAST                'self'
               14  LOAD_ATTR                eof_sent
               16  POP_JUMP_IF_TRUE     24  'to 24'

 L.  69        18  LOAD_FAST                'self'
               20  LOAD_ATTR                active
               22  POP_JUMP_IF_TRUE     32  'to 32'
             24_0  COME_FROM            16  '16'
             24_1  COME_FROM            10  '10'
             24_2  COME_FROM             4  '4'

 L.  71        24  LOAD_GLOBAL              SSHException
               26  LOAD_STR                 'Channel is not open'
               28  CALL_FUNCTION_1       1  '1 positional argument'
               30  RAISE_VARARGS_1       1  'exception instance'
             32_0  COME_FROM            22  '22'

 L.  72        32  LOAD_DEREF               'func'
               34  LOAD_FAST                'self'
               36  BUILD_TUPLE_1         1 
               38  LOAD_FAST                'args'
               40  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
               42  LOAD_FAST                'kwds'
               44  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               46  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 32_0

    return _check


class Channel(ClosingContextManager):
    __doc__ = "\n    A secure tunnel across an SSH `.Transport`.  A Channel is meant to behave\n    like a socket, and has an API that should be indistinguishable from the\n    Python socket API.\n\n    Because SSH2 has a windowing kind of flow control, if you stop reading data\n    from a Channel and its buffer fills up, the server will be unable to send\n    you any more data until you read some of it.  (This won't affect other\n    channels on the same transport -- all channels on a single transport are\n    flow-controlled independently.)  Similarly, if the server isn't reading\n    data you send, calls to `send` may block, unless you set a timeout.  This\n    is exactly like a normal network socket, so it shouldn't be too surprising.\n\n    Instances of this class may be used as context managers.\n    "

    def __init__(self, chanid):
        """
        Create a new channel.  The channel is not associated with any
        particular session or `.Transport` until the Transport attaches it.
        Normally you would only call this method from the constructor of a
        subclass of `.Channel`.

        :param int chanid:
            the ID of this channel, as passed by an existing `.Transport`.
        """
        self.chanid = chanid
        self.remote_chanid = 0
        self.transport = None
        self.active = False
        self.eof_received = 0
        self.eof_sent = 0
        self.in_buffer = BufferedPipe()
        self.in_stderr_buffer = BufferedPipe()
        self.timeout = None
        self.closed = False
        self.ultra_debug = False
        self.lock = threading.Lock()
        self.out_buffer_cv = threading.Condition(self.lock)
        self.in_window_size = 0
        self.out_window_size = 0
        self.in_max_packet_size = 0
        self.out_max_packet_size = 0
        self.in_window_threshold = 0
        self.in_window_sofar = 0
        self.status_event = threading.Event()
        self._name = str(chanid)
        self.logger = util.get_logger('paramiko.transport')
        self._pipe = None
        self.event = threading.Event()
        self.event_ready = False
        self.combine_stderr = False
        self.exit_status = -1
        self.origin_addr = None

    def __del__(self):
        try:
            self.close()
        except:
            pass

    def __repr__(self):
        """
        Return a string representation of this object, for debugging.
        """
        out = '<paramiko.Channel {}'.format(self.chanid)
        if self.closed:
            out += ' (closed)'
        else:
            if self.active:
                if self.eof_received:
                    out += ' (EOF received)'
                if self.eof_sent:
                    out += ' (EOF sent)'
                out += ' (open) window={}'.format(self.out_window_size)
                if len(self.in_buffer) > 0:
                    out += ' in-buffer={}'.format(len(self.in_buffer))
        out += ' -> ' + repr(self.transport)
        out += '>'
        return out

    @open_only
    def get_pty(self, term='vt100', width=80, height=24, width_pixels=0, height_pixels=0):
        """
        Request a pseudo-terminal from the server.  This is usually used right
        after creating a client channel, to ask the server to provide some
        basic terminal semantics for a shell invoked with `invoke_shell`.
        It isn't necessary (or desirable) to call this method if you're going
        to execute a single command with `exec_command`.

        :param str term: the terminal type to emulate
            (for example, ``'vt100'``)
        :param int width: width (in characters) of the terminal screen
        :param int height: height (in characters) of the terminal screen
        :param int width_pixels: width (in pixels) of the terminal screen
        :param int height_pixels: height (in pixels) of the terminal screen

        :raises:
            `.SSHException` -- if the request was rejected or the channel was
            closed
        """
        m = Message()
        m.add_byte(cMSG_CHANNEL_REQUEST)
        m.add_int(self.remote_chanid)
        m.add_string('pty-req')
        m.add_boolean(True)
        m.add_string(term)
        m.add_int(width)
        m.add_int(height)
        m.add_int(width_pixels)
        m.add_int(height_pixels)
        m.add_string(bytes())
        self._event_pending()
        self.transport._send_user_message(m)
        self._wait_for_event()

    @open_only
    def invoke_shell(self):
        """
        Request an interactive shell session on this channel.  If the server
        allows it, the channel will then be directly connected to the stdin,
        stdout, and stderr of the shell.

        Normally you would call `get_pty` before this, in which case the
        shell will operate through the pty, and the channel will be connected
        to the stdin and stdout of the pty.

        When the shell exits, the channel will be closed and can't be reused.
        You must open a new channel if you wish to open another shell.

        :raises:
            `.SSHException` -- if the request was rejected or the channel was
            closed
        """
        m = Message()
        m.add_byte(cMSG_CHANNEL_REQUEST)
        m.add_int(self.remote_chanid)
        m.add_string('shell')
        m.add_boolean(True)
        self._event_pending()
        self.transport._send_user_message(m)
        self._wait_for_event()

    @open_only
    def exec_command(self, command):
        """
        Execute a command on the server.  If the server allows it, the channel
        will then be directly connected to the stdin, stdout, and stderr of
        the command being executed.

        When the command finishes executing, the channel will be closed and
        can't be reused.  You must open a new channel if you wish to execute
        another command.

        :param str command: a shell command to execute.

        :raises:
            `.SSHException` -- if the request was rejected or the channel was
            closed
        """
        m = Message()
        m.add_byte(cMSG_CHANNEL_REQUEST)
        m.add_int(self.remote_chanid)
        m.add_string('exec')
        m.add_boolean(True)
        m.add_string(command)
        self._event_pending()
        self.transport._send_user_message(m)
        self._wait_for_event()

    @open_only
    def invoke_subsystem(self, subsystem):
        """
        Request a subsystem on the server (for example, ``sftp``).  If the
        server allows it, the channel will then be directly connected to the
        requested subsystem.

        When the subsystem finishes, the channel will be closed and can't be
        reused.

        :param str subsystem: name of the subsystem being requested.

        :raises:
            `.SSHException` -- if the request was rejected or the channel was
            closed
        """
        m = Message()
        m.add_byte(cMSG_CHANNEL_REQUEST)
        m.add_int(self.remote_chanid)
        m.add_string('subsystem')
        m.add_boolean(True)
        m.add_string(subsystem)
        self._event_pending()
        self.transport._send_user_message(m)
        self._wait_for_event()

    @open_only
    def resize_pty(self, width=80, height=24, width_pixels=0, height_pixels=0):
        """
        Resize the pseudo-terminal.  This can be used to change the width and
        height of the terminal emulation created in a previous `get_pty` call.

        :param int width: new width (in characters) of the terminal screen
        :param int height: new height (in characters) of the terminal screen
        :param int width_pixels: new width (in pixels) of the terminal screen
        :param int height_pixels: new height (in pixels) of the terminal screen

        :raises:
            `.SSHException` -- if the request was rejected or the channel was
            closed
        """
        m = Message()
        m.add_byte(cMSG_CHANNEL_REQUEST)
        m.add_int(self.remote_chanid)
        m.add_string('window-change')
        m.add_boolean(False)
        m.add_int(width)
        m.add_int(height)
        m.add_int(width_pixels)
        m.add_int(height_pixels)
        self.transport._send_user_message(m)

    @open_only
    def update_environment(self, environment):
        """
        Updates this channel's remote shell environment.

        .. note::
            This operation is additive - i.e. the current environment is not
            reset before the given environment variables are set.

        .. warning::
            Servers may silently reject some environment variables; see the
            warning in `set_environment_variable` for details.

        :param dict environment:
            a dictionary containing the name and respective values to set
        :raises:
            `.SSHException` -- if any of the environment variables was rejected
            by the server or the channel was closed
        """
        for name, value in environment.items():
            try:
                self.set_environment_variable(name, value)
            except SSHException as e:
                try:
                    err = 'Failed to set environment variable "{}".'
                    raise SSHException(err.format(name), e)
                finally:
                    e = None
                    del e

    @open_only
    def set_environment_variable(self, name, value):
        """
        Set the value of an environment variable.

        .. warning::
            The server may reject this request depending on its ``AcceptEnv``
            setting; such rejections will fail silently (which is common client
            practice for this particular request type). Make sure you
            understand your server's configuration before using!

        :param str name: name of the environment variable
        :param str value: value of the environment variable

        :raises:
            `.SSHException` -- if the request was rejected or the channel was
            closed
        """
        m = Message()
        m.add_byte(cMSG_CHANNEL_REQUEST)
        m.add_int(self.remote_chanid)
        m.add_string('env')
        m.add_boolean(False)
        m.add_string(name)
        m.add_string(value)
        self.transport._send_user_message(m)

    def exit_status_ready(self):
        """
        Return true if the remote process has exited and returned an exit
        status. You may use this to poll the process status if you don't
        want to block in `recv_exit_status`. Note that the server may not
        return an exit status in some cases (like bad servers).

        :return:
            ``True`` if `recv_exit_status` will return immediately, else
            ``False``.

        .. versionadded:: 1.7.3
        """
        return self.closed or self.status_event.is_set()

    def recv_exit_status(self):
        """
        Return the exit status from the process on the server.  This is
        mostly useful for retrieving the results of an `exec_command`.
        If the command hasn't finished yet, this method will wait until
        it does, or until the channel is closed.  If no exit status is
        provided by the server, -1 is returned.

        .. warning::
            In some situations, receiving remote output larger than the current
            `.Transport` or session's ``window_size`` (e.g. that set by the
            ``default_window_size`` kwarg for `.Transport.__init__`) will cause
            `.recv_exit_status` to hang indefinitely if it is called prior to a
            sufficiently large `.Channel.recv` (or if there are no threads
            calling `.Channel.recv` in the background).

            In these cases, ensuring that `.recv_exit_status` is called *after*
            `.Channel.recv` (or, again, using threads) can avoid the hang.

        :return: the exit code (as an `int`) of the process on the server.

        .. versionadded:: 1.2
        """
        self.status_event.wait()
        assert self.status_event.is_set()
        return self.exit_status

    def send_exit_status(self, status):
        """
        Send the exit status of an executed command to the client.  (This
        really only makes sense in server mode.)  Many clients expect to
        get some sort of status code back from an executed command after
        it completes.

        :param int status: the exit code of the process

        .. versionadded:: 1.2
        """
        m = Message()
        m.add_byte(cMSG_CHANNEL_REQUEST)
        m.add_int(self.remote_chanid)
        m.add_string('exit-status')
        m.add_boolean(False)
        m.add_int(status)
        self.transport._send_user_message(m)

    @open_only
    def request_x11(self, screen_number=0, auth_protocol=None, auth_cookie=None, single_connection=False, handler=None):
        """
        Request an x11 session on this channel.  If the server allows it,
        further x11 requests can be made from the server to the client,
        when an x11 application is run in a shell session.

        From :rfc:`4254`::

            It is RECOMMENDED that the 'x11 authentication cookie' that is
            sent be a fake, random cookie, and that the cookie be checked and
            replaced by the real cookie when a connection request is received.

        If you omit the auth_cookie, a new secure random 128-bit value will be
        generated, used, and returned.  You will need to use this value to
        verify incoming x11 requests and replace them with the actual local
        x11 cookie (which requires some knowledge of the x11 protocol).

        If a handler is passed in, the handler is called from another thread
        whenever a new x11 connection arrives.  The default handler queues up
        incoming x11 connections, which may be retrieved using
        `.Transport.accept`.  The handler's calling signature is::

            handler(channel: Channel, (address: str, port: int))

        :param int screen_number: the x11 screen number (0, 10, etc.)
        :param str auth_protocol:
            the name of the X11 authentication method used; if none is given,
            ``"MIT-MAGIC-COOKIE-1"`` is used
        :param str auth_cookie:
            hexadecimal string containing the x11 auth cookie; if none is
            given, a secure random 128-bit value is generated
        :param bool single_connection:
            if True, only a single x11 connection will be forwarded (by
            default, any number of x11 connections can arrive over this
            session)
        :param handler:
            an optional callable handler to use for incoming X11 connections
        :return: the auth_cookie used
        """
        if auth_protocol is None:
            auth_protocol = 'MIT-MAGIC-COOKIE-1'
        if auth_cookie is None:
            auth_cookie = binascii.hexlify(os.urandom(16))
        m = Message()
        m.add_byte(cMSG_CHANNEL_REQUEST)
        m.add_int(self.remote_chanid)
        m.add_string('x11-req')
        m.add_boolean(True)
        m.add_boolean(single_connection)
        m.add_string(auth_protocol)
        m.add_string(auth_cookie)
        m.add_int(screen_number)
        self._event_pending()
        self.transport._send_user_message(m)
        self._wait_for_event()
        self.transport._set_x11_handler(handler)
        return auth_cookie

    @open_only
    def request_forward_agent(self, handler):
        """
        Request for a forward SSH Agent on this channel.
        This is only valid for an ssh-agent from OpenSSH !!!

        :param handler:
            a required callable handler to use for incoming SSH Agent
            connections

        :return: True if we are ok, else False
            (at that time we always return ok)

        :raises: SSHException in case of channel problem.
        """
        m = Message()
        m.add_byte(cMSG_CHANNEL_REQUEST)
        m.add_int(self.remote_chanid)
        m.add_string('auth-agent-req@openssh.com')
        m.add_boolean(False)
        self.transport._send_user_message(m)
        self.transport._set_forward_agent_handler(handler)
        return True

    def get_transport(self):
        """
        Return the `.Transport` associated with this channel.
        """
        return self.transport

    def set_name(self, name):
        """
        Set a name for this channel.  Currently it's only used to set the name
        of the channel in logfile entries.  The name can be fetched with the
        `get_name` method.

        :param str name: new channel name
        """
        self._name = name

    def get_name(self):
        """
        Get the name of this channel that was previously set by `set_name`.
        """
        return self._name

    def get_id(self):
        """
        Return the `int` ID # for this channel.

        The channel ID is unique across a `.Transport` and usually a small
        number.  It's also the number passed to
        `.ServerInterface.check_channel_request` when determining whether to
        accept a channel request in server mode.
        """
        return self.chanid

    def set_combine_stderr(self, combine):
        """
        Set whether stderr should be combined into stdout on this channel.
        The default is ``False``, but in some cases it may be convenient to
        have both streams combined.

        If this is ``False``, and `exec_command` is called (or ``invoke_shell``
        with no pty), output to stderr will not show up through the `recv`
        and `recv_ready` calls.  You will have to use `recv_stderr` and
        `recv_stderr_ready` to get stderr output.

        If this is ``True``, data will never show up via `recv_stderr` or
        `recv_stderr_ready`.

        :param bool combine:
            ``True`` if stderr output should be combined into stdout on this
            channel.
        :return: the previous setting (a `bool`).

        .. versionadded:: 1.1
        """
        data = bytes()
        self.lock.acquire()
        try:
            old = self.combine_stderr
            self.combine_stderr = combine
            if combine:
                if not old:
                    data = self.in_stderr_buffer.empty()
        finally:
            self.lock.release()

        if len(data) > 0:
            self._feed(data)
        return old

    def settimeout(self, timeout):
        """
        Set a timeout on blocking read/write operations.  The ``timeout``
        argument can be a nonnegative float expressing seconds, or ``None``.
        If a float is given, subsequent channel read/write operations will
        raise a timeout exception if the timeout period value has elapsed
        before the operation has completed.  Setting a timeout of ``None``
        disables timeouts on socket operations.

        ``chan.settimeout(0.0)`` is equivalent to ``chan.setblocking(0)``;
        ``chan.settimeout(None)`` is equivalent to ``chan.setblocking(1)``.

        :param float timeout:
            seconds to wait for a pending read/write operation before raising
            ``socket.timeout``, or ``None`` for no timeout.
        """
        self.timeout = timeout

    def gettimeout(self):
        """
        Returns the timeout in seconds (as a float) associated with socket
        operations, or ``None`` if no timeout is set.  This reflects the last
        call to `setblocking` or `settimeout`.
        """
        return self.timeout

    def setblocking(self, blocking):
        """
        Set blocking or non-blocking mode of the channel: if ``blocking`` is 0,
        the channel is set to non-blocking mode; otherwise it's set to blocking
        mode. Initially all channels are in blocking mode.

        In non-blocking mode, if a `recv` call doesn't find any data, or if a
        `send` call can't immediately dispose of the data, an error exception
        is raised. In blocking mode, the calls block until they can proceed. An
        EOF condition is considered "immediate data" for `recv`, so if the
        channel is closed in the read direction, it will never block.

        ``chan.setblocking(0)`` is equivalent to ``chan.settimeout(0)``;
        ``chan.setblocking(1)`` is equivalent to ``chan.settimeout(None)``.

        :param int blocking:
            0 to set non-blocking mode; non-0 to set blocking mode.
        """
        if blocking:
            self.settimeout(None)
        else:
            self.settimeout(0.0)

    def getpeername(self):
        """
        Return the address of the remote side of this Channel, if possible.

        This simply wraps `.Transport.getpeername`, used to provide enough of a
        socket-like interface to allow asyncore to work. (asyncore likes to
        call ``'getpeername'``.)
        """
        return self.transport.getpeername()

    def close(self):
        """
        Close the channel.  All future read/write operations on the channel
        will fail.  The remote end will receive no more data (after queued data
        is flushed).  Channels are automatically closed when their `.Transport`
        is closed or when they are garbage collected.
        """
        self.lock.acquire()
        try:
            if self._pipe is not None:
                self._pipe.close()
                self._pipe = None
            if not self.active or self.closed:
                return
            msgs = self._close_internal()
        finally:
            self.lock.release()

        for m in msgs:
            if m is not None:
                self.transport._send_user_message(m)

    def recv_ready(self):
        """
        Returns true if data is buffered and ready to be read from this
        channel.  A ``False`` result does not mean that the channel has closed;
        it means you may need to wait before more data arrives.

        :return:
            ``True`` if a `recv` call on this channel would immediately return
            at least one byte; ``False`` otherwise.
        """
        return self.in_buffer.read_ready()

    def recv(self, nbytes):
        """
        Receive data from the channel.  The return value is a string
        representing the data received.  The maximum amount of data to be
        received at once is specified by ``nbytes``.  If a string of
        length zero is returned, the channel stream has closed.

        :param int nbytes: maximum number of bytes to read.
        :return: received data, as a ``str``/``bytes``.

        :raises socket.timeout:
            if no data is ready before the timeout set by `settimeout`.
        """
        try:
            out = self.in_buffer.read(nbytes, self.timeout)
        except PipeTimeout:
            raise socket.timeout()

        ack = self._check_add_window(len(out))
        if ack > 0:
            m = Message()
            m.add_byte(cMSG_CHANNEL_WINDOW_ADJUST)
            m.add_int(self.remote_chanid)
            m.add_int(ack)
            self.transport._send_user_message(m)
        return out

    def recv_stderr_ready(self):
        """
        Returns true if data is buffered and ready to be read from this
        channel's stderr stream.  Only channels using `exec_command` or
        `invoke_shell` without a pty will ever have data on the stderr
        stream.

        :return:
            ``True`` if a `recv_stderr` call on this channel would immediately
            return at least one byte; ``False`` otherwise.

        .. versionadded:: 1.1
        """
        return self.in_stderr_buffer.read_ready()

    def recv_stderr(self, nbytes):
        """
        Receive data from the channel's stderr stream.  Only channels using
        `exec_command` or `invoke_shell` without a pty will ever have data
        on the stderr stream.  The return value is a string representing the
        data received.  The maximum amount of data to be received at once is
        specified by ``nbytes``.  If a string of length zero is returned, the
        channel stream has closed.

        :param int nbytes: maximum number of bytes to read.
        :return: received data as a `str`

        :raises socket.timeout: if no data is ready before the timeout set by
            `settimeout`.

        .. versionadded:: 1.1
        """
        try:
            out = self.in_stderr_buffer.read(nbytes, self.timeout)
        except PipeTimeout:
            raise socket.timeout()

        ack = self._check_add_window(len(out))
        if ack > 0:
            m = Message()
            m.add_byte(cMSG_CHANNEL_WINDOW_ADJUST)
            m.add_int(self.remote_chanid)
            m.add_int(ack)
            self.transport._send_user_message(m)
        return out

    def send_ready(self):
        """
        Returns true if data can be written to this channel without blocking.
        This means the channel is either closed (so any write attempt would
        return immediately) or there is at least one byte of space in the
        outbound buffer. If there is at least one byte of space in the
        outbound buffer, a `send` call will succeed immediately and return
        the number of bytes actually written.

        :return:
            ``True`` if a `send` call on this channel would immediately succeed
            or fail
        """
        self.lock.acquire()
        try:
            if self.closed or self.eof_sent:
                return True
            return self.out_window_size > 0
        finally:
            self.lock.release()

    def send(self, s):
        """
        Send data to the channel.  Returns the number of bytes sent, or 0 if
        the channel stream is closed.  Applications are responsible for
        checking that all data has been sent: if only some of the data was
        transmitted, the application needs to attempt delivery of the remaining
        data.

        :param str s: data to send
        :return: number of bytes actually sent, as an `int`

        :raises socket.timeout: if no data could be sent before the timeout set
            by `settimeout`.
        """
        m = Message()
        m.add_byte(cMSG_CHANNEL_DATA)
        m.add_int(self.remote_chanid)
        return self._send(s, m)

    def send_stderr(self, s):
        """
        Send data to the channel on the "stderr" stream.  This is normally
        only used by servers to send output from shell commands -- clients
        won't use this.  Returns the number of bytes sent, or 0 if the channel
        stream is closed.  Applications are responsible for checking that all
        data has been sent: if only some of the data was transmitted, the
        application needs to attempt delivery of the remaining data.

        :param str s: data to send.
        :return: number of bytes actually sent, as an `int`.

        :raises socket.timeout:
            if no data could be sent before the timeout set by `settimeout`.

        .. versionadded:: 1.1
        """
        m = Message()
        m.add_byte(cMSG_CHANNEL_EXTENDED_DATA)
        m.add_int(self.remote_chanid)
        m.add_int(1)
        return self._send(s, m)

    def sendall(self, s):
        """
        Send data to the channel, without allowing partial results.  Unlike
        `send`, this method continues to send data from the given string until
        either all data has been sent or an error occurs.  Nothing is returned.

        :param str s: data to send.

        :raises socket.timeout:
            if sending stalled for longer than the timeout set by `settimeout`.
        :raises socket.error:
            if an error occurred before the entire string was sent.

        .. note::
            If the channel is closed while only part of the data has been
            sent, there is no way to determine how much data (if any) was sent.
            This is irritating, but identically follows Python's API.
        """
        while s:
            sent = self.send(s)
            s = s[sent:]

    def sendall_stderr(self, s):
        """
        Send data to the channel's "stderr" stream, without allowing partial
        results.  Unlike `send_stderr`, this method continues to send data
        from the given string until all data has been sent or an error occurs.
        Nothing is returned.

        :param str s: data to send to the client as "stderr" output.

        :raises socket.timeout:
            if sending stalled for longer than the timeout set by `settimeout`.
        :raises socket.error:
            if an error occurred before the entire string was sent.

        .. versionadded:: 1.1
        """
        while s:
            sent = self.send_stderr(s)
            s = s[sent:]

    def makefile(self, *params):
        """
        Return a file-like object associated with this channel.  The optional
        ``mode`` and ``bufsize`` arguments are interpreted the same way as by
        the built-in ``file()`` function in Python.

        :return: `.ChannelFile` object which can be used for Python file I/O.
        """
        return ChannelFile(*[self] + list(params))

    def makefile_stderr(self, *params):
        """
        Return a file-like object associated with this channel's stderr
        stream.   Only channels using `exec_command` or `invoke_shell`
        without a pty will ever have data on the stderr stream.

        The optional ``mode`` and ``bufsize`` arguments are interpreted the
        same way as by the built-in ``file()`` function in Python.  For a
        client, it only makes sense to open this file for reading.  For a
        server, it only makes sense to open this file for writing.

        :returns:
            `.ChannelStderrFile` object which can be used for Python file I/O.

        .. versionadded:: 1.1
        """
        return ChannelStderrFile(*[self] + list(params))

    def makefile_stdin(self, *params):
        """
        Return a file-like object associated with this channel's stdin
        stream.

        The optional ``mode`` and ``bufsize`` arguments are interpreted the
        same way as by the built-in ``file()`` function in Python.  For a
        client, it only makes sense to open this file for writing.  For a
        server, it only makes sense to open this file for reading.

        :returns:
            `.ChannelStdinFile` object which can be used for Python file I/O.

        .. versionadded:: 2.6
        """
        return ChannelStdinFile(*[self] + list(params))

    def fileno(self):
        """
        Returns an OS-level file descriptor which can be used for polling, but
        but not for reading or writing.  This is primarily to allow Python's
        ``select`` module to work.

        The first time ``fileno`` is called on a channel, a pipe is created to
        simulate real OS-level file descriptor (FD) behavior.  Because of this,
        two OS-level FDs are created, which will use up FDs faster than normal.
        (You won't notice this effect unless you have hundreds of channels
        open at the same time.)

        :return: an OS-level file descriptor (`int`)

        .. warning::
            This method causes channel reads to be slightly less efficient.
        """
        self.lock.acquire()
        try:
            if self._pipe is not None:
                return self._pipe.fileno()
            self._pipe = pipe.make_pipe()
            p1, p2 = pipe.make_or_pipe(self._pipe)
            self.in_buffer.set_event(p1)
            self.in_stderr_buffer.set_event(p2)
            return self._pipe.fileno()
        finally:
            self.lock.release()

    def shutdown(self, how):
        """
        Shut down one or both halves of the connection.  If ``how`` is 0,
        further receives are disallowed.  If ``how`` is 1, further sends
        are disallowed.  If ``how`` is 2, further sends and receives are
        disallowed.  This closes the stream in one or both directions.

        :param int how:
            0 (stop receiving), 1 (stop sending), or 2 (stop receiving and
              sending).
        """
        if how == 0 or how == 2:
            self.eof_received = 1
        if how == 1 or how == 2:
            self.lock.acquire()
            try:
                m = self._send_eof()
            finally:
                self.lock.release()

            if m is not None:
                self.transport._send_user_message(m)

    def shutdown_read(self):
        """
        Shutdown the receiving side of this socket, closing the stream in
        the incoming direction.  After this call, future reads on this
        channel will fail instantly.  This is a convenience method, equivalent
        to ``shutdown(0)``, for people who don't make it a habit to
        memorize unix constants from the 1970s.

        .. versionadded:: 1.2
        """
        self.shutdown(0)

    def shutdown_write(self):
        """
        Shutdown the sending side of this socket, closing the stream in
        the outgoing direction.  After this call, future writes on this
        channel will fail instantly.  This is a convenience method, equivalent
        to ``shutdown(1)``, for people who don't make it a habit to
        memorize unix constants from the 1970s.

        .. versionadded:: 1.2
        """
        self.shutdown(1)

    @property
    def _closed(self):
        return self.closed

    def _set_transport(self, transport):
        self.transport = transport
        self.logger = util.get_logger(self.transport.get_log_channel())

    def _set_window(self, window_size, max_packet_size):
        self.in_window_size = window_size
        self.in_max_packet_size = max_packet_size
        self.in_window_threshold = window_size // 10
        self.in_window_sofar = 0
        self._log(DEBUG, 'Max packet in: {} bytes'.format(max_packet_size))

    def _set_remote_channel(self, chanid, window_size, max_packet_size):
        self.remote_chanid = chanid
        self.out_window_size = window_size
        self.out_max_packet_size = self.transport._sanitize_packet_size(max_packet_size)
        self.active = 1
        self._log(DEBUG, 'Max packet out: {} bytes'.format(self.out_max_packet_size))

    def _request_success(self, m):
        self._log(DEBUG, 'Sesch channel {} request ok'.format(self.chanid))
        self.event_ready = True
        self.event.set()

    def _request_failed(self, m):
        self.lock.acquire()
        try:
            msgs = self._close_internal()
        finally:
            self.lock.release()

        for m in msgs:
            if m is not None:
                self.transport._send_user_message(m)

    def _feed(self, m):
        if isinstance(m, bytes_types):
            s = m
        else:
            s = m.get_binary()
        self.in_buffer.feed(s)

    def _feed_extended(self, m):
        code = m.get_int()
        s = m.get_binary()
        if code != 1:
            self._log(ERROR, 'unknown extended_data type {}; discarding'.format(code))
            return
        elif self.combine_stderr:
            self._feed(s)
        else:
            self.in_stderr_buffer.feed(s)

    def _window_adjust(self, m):
        nbytes = m.get_int()
        self.lock.acquire()
        try:
            if self.ultra_debug:
                self._log(DEBUG, 'window up {}'.format(nbytes))
            self.out_window_size += nbytes
            self.out_buffer_cv.notifyAll()
        finally:
            self.lock.release()

    def _handle_request--- This code section failed: ---

 L.1074         0  LOAD_FAST                'm'
                2  LOAD_METHOD              get_text
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  STORE_FAST               'key'

 L.1075         8  LOAD_FAST                'm'
               10  LOAD_METHOD              get_boolean
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  STORE_FAST               'want_reply'

 L.1076        16  LOAD_FAST                'self'
               18  LOAD_ATTR                transport
               20  LOAD_ATTR                server_object
               22  STORE_FAST               'server'

 L.1077        24  LOAD_CONST               False
               26  STORE_FAST               'ok'

 L.1078        28  LOAD_FAST                'key'
               30  LOAD_STR                 'exit-status'
               32  COMPARE_OP               ==
               34  POP_JUMP_IF_FALSE    64  'to 64'

 L.1079        36  LOAD_FAST                'm'
               38  LOAD_METHOD              get_int
               40  CALL_METHOD_0         0  '0 positional arguments'
               42  LOAD_FAST                'self'
               44  STORE_ATTR               exit_status

 L.1080        46  LOAD_FAST                'self'
               48  LOAD_ATTR                status_event
               50  LOAD_METHOD              set
               52  CALL_METHOD_0         0  '0 positional arguments'
               54  POP_TOP          

 L.1081        56  LOAD_CONST               True
               58  STORE_FAST               'ok'
            60_62  JUMP_FORWARD        584  'to 584'
             64_0  COME_FROM            34  '34'

 L.1082        64  LOAD_FAST                'key'
               66  LOAD_STR                 'xon-xoff'
               68  COMPARE_OP               ==
               70  POP_JUMP_IF_FALSE    80  'to 80'

 L.1084        72  LOAD_CONST               True
               74  STORE_FAST               'ok'
            76_78  JUMP_FORWARD        584  'to 584'
             80_0  COME_FROM            70  '70'

 L.1085        80  LOAD_FAST                'key'
               82  LOAD_STR                 'pty-req'
               84  COMPARE_OP               ==
               86  POP_JUMP_IF_FALSE   176  'to 176'

 L.1086        88  LOAD_FAST                'm'
               90  LOAD_METHOD              get_string
               92  CALL_METHOD_0         0  '0 positional arguments'
               94  STORE_FAST               'term'

 L.1087        96  LOAD_FAST                'm'
               98  LOAD_METHOD              get_int
              100  CALL_METHOD_0         0  '0 positional arguments'
              102  STORE_FAST               'width'

 L.1088       104  LOAD_FAST                'm'
              106  LOAD_METHOD              get_int
              108  CALL_METHOD_0         0  '0 positional arguments'
              110  STORE_FAST               'height'

 L.1089       112  LOAD_FAST                'm'
              114  LOAD_METHOD              get_int
              116  CALL_METHOD_0         0  '0 positional arguments'
              118  STORE_FAST               'pixelwidth'

 L.1090       120  LOAD_FAST                'm'
              122  LOAD_METHOD              get_int
              124  CALL_METHOD_0         0  '0 positional arguments'
              126  STORE_FAST               'pixelheight'

 L.1091       128  LOAD_FAST                'm'
              130  LOAD_METHOD              get_string
              132  CALL_METHOD_0         0  '0 positional arguments'
              134  STORE_FAST               'modes'

 L.1092       136  LOAD_FAST                'server'
              138  LOAD_CONST               None
              140  COMPARE_OP               is
              142  POP_JUMP_IF_FALSE   150  'to 150'

 L.1093       144  LOAD_CONST               False
              146  STORE_FAST               'ok'
              148  JUMP_FORWARD        584  'to 584'
            150_0  COME_FROM           142  '142'

 L.1095       150  LOAD_FAST                'server'
              152  LOAD_METHOD              check_channel_pty_request

 L.1096       154  LOAD_FAST                'self'
              156  LOAD_FAST                'term'
              158  LOAD_FAST                'width'
              160  LOAD_FAST                'height'
              162  LOAD_FAST                'pixelwidth'
              164  LOAD_FAST                'pixelheight'
              166  LOAD_FAST                'modes'
              168  CALL_METHOD_7         7  '7 positional arguments'
              170  STORE_FAST               'ok'
          172_174  JUMP_FORWARD        584  'to 584'
            176_0  COME_FROM            86  '86'

 L.1098       176  LOAD_FAST                'key'
              178  LOAD_STR                 'shell'
              180  COMPARE_OP               ==
              182  POP_JUMP_IF_FALSE   212  'to 212'

 L.1099       184  LOAD_FAST                'server'
              186  LOAD_CONST               None
              188  COMPARE_OP               is
              190  POP_JUMP_IF_FALSE   198  'to 198'

 L.1100       192  LOAD_CONST               False
              194  STORE_FAST               'ok'
              196  JUMP_FORWARD        584  'to 584'
            198_0  COME_FROM           190  '190'

 L.1102       198  LOAD_FAST                'server'
              200  LOAD_METHOD              check_channel_shell_request
              202  LOAD_FAST                'self'
              204  CALL_METHOD_1         1  '1 positional argument'
              206  STORE_FAST               'ok'
          208_210  JUMP_FORWARD        584  'to 584'
            212_0  COME_FROM           182  '182'

 L.1103       212  LOAD_FAST                'key'
              214  LOAD_STR                 'env'
              216  COMPARE_OP               ==
          218_220  POP_JUMP_IF_FALSE   270  'to 270'

 L.1104       222  LOAD_FAST                'm'
              224  LOAD_METHOD              get_string
              226  CALL_METHOD_0         0  '0 positional arguments'
              228  STORE_FAST               'name'

 L.1105       230  LOAD_FAST                'm'
              232  LOAD_METHOD              get_string
              234  CALL_METHOD_0         0  '0 positional arguments'
              236  STORE_FAST               'value'

 L.1106       238  LOAD_FAST                'server'
              240  LOAD_CONST               None
              242  COMPARE_OP               is
              244  POP_JUMP_IF_FALSE   252  'to 252'

 L.1107       246  LOAD_CONST               False
              248  STORE_FAST               'ok'
              250  JUMP_FORWARD        584  'to 584'
            252_0  COME_FROM           244  '244'

 L.1109       252  LOAD_FAST                'server'
              254  LOAD_METHOD              check_channel_env_request
              256  LOAD_FAST                'self'
              258  LOAD_FAST                'name'
              260  LOAD_FAST                'value'
              262  CALL_METHOD_3         3  '3 positional arguments'
              264  STORE_FAST               'ok'
          266_268  JUMP_FORWARD        584  'to 584'
            270_0  COME_FROM           218  '218'

 L.1110       270  LOAD_FAST                'key'
              272  LOAD_STR                 'exec'
              274  COMPARE_OP               ==
          276_278  POP_JUMP_IF_FALSE   320  'to 320'

 L.1111       280  LOAD_FAST                'm'
              282  LOAD_METHOD              get_string
              284  CALL_METHOD_0         0  '0 positional arguments'
              286  STORE_FAST               'cmd'

 L.1112       288  LOAD_FAST                'server'
              290  LOAD_CONST               None
              292  COMPARE_OP               is
          294_296  POP_JUMP_IF_FALSE   304  'to 304'

 L.1113       298  LOAD_CONST               False
              300  STORE_FAST               'ok'
              302  JUMP_FORWARD        584  'to 584'
            304_0  COME_FROM           294  '294'

 L.1115       304  LOAD_FAST                'server'
              306  LOAD_METHOD              check_channel_exec_request
              308  LOAD_FAST                'self'
              310  LOAD_FAST                'cmd'
              312  CALL_METHOD_2         2  '2 positional arguments'
              314  STORE_FAST               'ok'
          316_318  JUMP_FORWARD        584  'to 584'
            320_0  COME_FROM           276  '276'

 L.1116       320  LOAD_FAST                'key'
              322  LOAD_STR                 'subsystem'
              324  COMPARE_OP               ==
          326_328  POP_JUMP_IF_FALSE   368  'to 368'

 L.1117       330  LOAD_FAST                'm'
              332  LOAD_METHOD              get_text
              334  CALL_METHOD_0         0  '0 positional arguments'
              336  STORE_FAST               'name'

 L.1118       338  LOAD_FAST                'server'
              340  LOAD_CONST               None
              342  COMPARE_OP               is
          344_346  POP_JUMP_IF_FALSE   354  'to 354'

 L.1119       348  LOAD_CONST               False
              350  STORE_FAST               'ok'
              352  JUMP_FORWARD        366  'to 366'
            354_0  COME_FROM           344  '344'

 L.1121       354  LOAD_FAST                'server'
              356  LOAD_METHOD              check_channel_subsystem_request
              358  LOAD_FAST                'self'
              360  LOAD_FAST                'name'
              362  CALL_METHOD_2         2  '2 positional arguments'
              364  STORE_FAST               'ok'
            366_0  COME_FROM           352  '352'
              366  JUMP_FORWARD        584  'to 584'
            368_0  COME_FROM           326  '326'

 L.1122       368  LOAD_FAST                'key'
              370  LOAD_STR                 'window-change'
              372  COMPARE_OP               ==
          374_376  POP_JUMP_IF_FALSE   446  'to 446'

 L.1123       378  LOAD_FAST                'm'
              380  LOAD_METHOD              get_int
              382  CALL_METHOD_0         0  '0 positional arguments'
              384  STORE_FAST               'width'

 L.1124       386  LOAD_FAST                'm'
              388  LOAD_METHOD              get_int
              390  CALL_METHOD_0         0  '0 positional arguments'
              392  STORE_FAST               'height'

 L.1125       394  LOAD_FAST                'm'
              396  LOAD_METHOD              get_int
              398  CALL_METHOD_0         0  '0 positional arguments'
              400  STORE_FAST               'pixelwidth'

 L.1126       402  LOAD_FAST                'm'
              404  LOAD_METHOD              get_int
              406  CALL_METHOD_0         0  '0 positional arguments'
              408  STORE_FAST               'pixelheight'

 L.1127       410  LOAD_FAST                'server'
              412  LOAD_CONST               None
              414  COMPARE_OP               is
          416_418  POP_JUMP_IF_FALSE   426  'to 426'

 L.1128       420  LOAD_CONST               False
              422  STORE_FAST               'ok'
              424  JUMP_FORWARD        444  'to 444'
            426_0  COME_FROM           416  '416'

 L.1130       426  LOAD_FAST                'server'
              428  LOAD_METHOD              check_channel_window_change_request

 L.1131       430  LOAD_FAST                'self'
              432  LOAD_FAST                'width'
              434  LOAD_FAST                'height'
              436  LOAD_FAST                'pixelwidth'
              438  LOAD_FAST                'pixelheight'
              440  CALL_METHOD_5         5  '5 positional arguments'
              442  STORE_FAST               'ok'
            444_0  COME_FROM           424  '424'
              444  JUMP_FORWARD        584  'to 584'
            446_0  COME_FROM           374  '374'

 L.1133       446  LOAD_FAST                'key'
              448  LOAD_STR                 'x11-req'
              450  COMPARE_OP               ==
          452_454  POP_JUMP_IF_FALSE   524  'to 524'

 L.1134       456  LOAD_FAST                'm'
              458  LOAD_METHOD              get_boolean
              460  CALL_METHOD_0         0  '0 positional arguments'
              462  STORE_FAST               'single_connection'

 L.1135       464  LOAD_FAST                'm'
              466  LOAD_METHOD              get_text
              468  CALL_METHOD_0         0  '0 positional arguments'
              470  STORE_FAST               'auth_proto'

 L.1136       472  LOAD_FAST                'm'
              474  LOAD_METHOD              get_binary
              476  CALL_METHOD_0         0  '0 positional arguments'
              478  STORE_FAST               'auth_cookie'

 L.1137       480  LOAD_FAST                'm'
              482  LOAD_METHOD              get_int
              484  CALL_METHOD_0         0  '0 positional arguments'
              486  STORE_FAST               'screen_number'

 L.1138       488  LOAD_FAST                'server'
              490  LOAD_CONST               None
              492  COMPARE_OP               is
          494_496  POP_JUMP_IF_FALSE   504  'to 504'

 L.1139       498  LOAD_CONST               False
              500  STORE_FAST               'ok'
              502  JUMP_FORWARD        522  'to 522'
            504_0  COME_FROM           494  '494'

 L.1141       504  LOAD_FAST                'server'
              506  LOAD_METHOD              check_channel_x11_request

 L.1142       508  LOAD_FAST                'self'

 L.1143       510  LOAD_FAST                'single_connection'

 L.1144       512  LOAD_FAST                'auth_proto'

 L.1145       514  LOAD_FAST                'auth_cookie'

 L.1146       516  LOAD_FAST                'screen_number'
              518  CALL_METHOD_5         5  '5 positional arguments'
              520  STORE_FAST               'ok'
            522_0  COME_FROM           502  '502'
              522  JUMP_FORWARD        584  'to 584'
            524_0  COME_FROM           452  '452'

 L.1148       524  LOAD_FAST                'key'
              526  LOAD_STR                 'auth-agent-req@openssh.com'
              528  COMPARE_OP               ==
          530_532  POP_JUMP_IF_FALSE   562  'to 562'

 L.1149       534  LOAD_FAST                'server'
              536  LOAD_CONST               None
              538  COMPARE_OP               is
          540_542  POP_JUMP_IF_FALSE   550  'to 550'

 L.1150       544  LOAD_CONST               False
              546  STORE_FAST               'ok'
              548  JUMP_FORWARD        560  'to 560'
            550_0  COME_FROM           540  '540'

 L.1152       550  LOAD_FAST                'server'
              552  LOAD_METHOD              check_channel_forward_agent_request
              554  LOAD_FAST                'self'
              556  CALL_METHOD_1         1  '1 positional argument'
            558_0  COME_FROM           148  '148'
              558  STORE_FAST               'ok'
            560_0  COME_FROM           548  '548'
              560  JUMP_FORWARD        584  'to 584'
            562_0  COME_FROM           530  '530'

 L.1154       562  LOAD_FAST                'self'
              564  LOAD_METHOD              _log
            566_0  COME_FROM           250  '250'
              566  LOAD_GLOBAL              DEBUG
            568_0  COME_FROM           302  '302'
              568  LOAD_STR                 'Unhandled channel request "{}"'
            570_0  COME_FROM           196  '196'
              570  LOAD_METHOD              format
              572  LOAD_FAST                'key'
              574  CALL_METHOD_1         1  '1 positional argument'
              576  CALL_METHOD_2         2  '2 positional arguments'
              578  POP_TOP          

 L.1155       580  LOAD_CONST               False
              582  STORE_FAST               'ok'
            584_0  COME_FROM           560  '560'
            584_1  COME_FROM           522  '522'
            584_2  COME_FROM           444  '444'
            584_3  COME_FROM           366  '366'
            584_4  COME_FROM           316  '316'
            584_5  COME_FROM           266  '266'
            584_6  COME_FROM           208  '208'
            584_7  COME_FROM           172  '172'
            584_8  COME_FROM            76  '76'
            584_9  COME_FROM            60  '60'

 L.1156       584  LOAD_FAST                'want_reply'
          586_588  POP_JUMP_IF_FALSE   648  'to 648'

 L.1157       590  LOAD_GLOBAL              Message
              592  CALL_FUNCTION_0       0  '0 positional arguments'
              594  STORE_FAST               'm'

 L.1158       596  LOAD_FAST                'ok'
          598_600  POP_JUMP_IF_FALSE   614  'to 614'

 L.1159       602  LOAD_FAST                'm'
              604  LOAD_METHOD              add_byte
              606  LOAD_GLOBAL              cMSG_CHANNEL_SUCCESS
              608  CALL_METHOD_1         1  '1 positional argument'
              610  POP_TOP          
              612  JUMP_FORWARD        624  'to 624'
            614_0  COME_FROM           598  '598'

 L.1161       614  LOAD_FAST                'm'
              616  LOAD_METHOD              add_byte
              618  LOAD_GLOBAL              cMSG_CHANNEL_FAILURE
              620  CALL_METHOD_1         1  '1 positional argument'
              622  POP_TOP          
            624_0  COME_FROM           612  '612'

 L.1162       624  LOAD_FAST                'm'
              626  LOAD_METHOD              add_int
              628  LOAD_FAST                'self'
              630  LOAD_ATTR                remote_chanid
              632  CALL_METHOD_1         1  '1 positional argument'
              634  POP_TOP          

 L.1163       636  LOAD_FAST                'self'
              638  LOAD_ATTR                transport
              640  LOAD_METHOD              _send_user_message
              642  LOAD_FAST                'm'
              644  CALL_METHOD_1         1  '1 positional argument'
              646  POP_TOP          
            648_0  COME_FROM           586  '586'

Parse error at or near `COME_FROM' instruction at offset 558_0

    def _handle_eof(self, m):
        self.lock.acquire()
        try:
            if not self.eof_received:
                self.eof_received = True
                self.in_buffer.close()
                self.in_stderr_buffer.close()
                if self._pipe is not None:
                    self._pipe.set_forever()
        finally:
            self.lock.release()

        self._log(DEBUG, 'EOF received ({})'.format(self._name))

    def _handle_close(self, m):
        self.lock.acquire()
        try:
            msgs = self._close_internal()
            self.transport._unlink_channel(self.chanid)
        finally:
            self.lock.release()

        for m in msgs:
            if m is not None:
                self.transport._send_user_message(m)

    def _send(self, s, m):
        size = len(s)
        self.lock.acquire()
        try:
            if self.closed:
                raise socket.error('Socket is closed')
            size = self._wait_for_send_window(size)
            if size == 0:
                return 0
            m.add_string(s[:size])
        finally:
            self.lock.release()

        self.transport._send_user_message(m)
        return size

    def _log(self, level, msg, *args):
        (self.logger.log)(level, '[chan ' + self._name + '] ' + msg, *args)

    def _event_pending(self):
        self.event.clear()
        self.event_ready = False

    def _wait_for_event(self):
        self.event.wait()
        assert self.event.is_set()
        if self.event_ready:
            return
        e = self.transport.get_exception()
        if e is None:
            e = SSHException('Channel closed.')
        raise e

    def _set_closed(self):
        self.closed = True
        self.in_buffer.close()
        self.in_stderr_buffer.close()
        self.out_buffer_cv.notifyAll()
        self.event.set()
        self.status_event.set()
        if self._pipe is not None:
            self._pipe.set_forever()

    def _send_eof(self):
        if self.eof_sent:
            return
        m = Message()
        m.add_byte(cMSG_CHANNEL_EOF)
        m.add_int(self.remote_chanid)
        self.eof_sent = True
        self._log(DEBUG, 'EOF sent ({})'.format(self._name))
        return m

    def _close_internal(self):
        if not self.active or self.closed:
            return (None, None)
        m1 = self._send_eof()
        m2 = Message()
        m2.add_byte(cMSG_CHANNEL_CLOSE)
        m2.add_int(self.remote_chanid)
        self._set_closed()
        return (
         m1, m2)

    def _unlink(self):
        if self.closed:
            return
        self.lock.acquire()
        try:
            self._set_closed()
            self.transport._unlink_channel(self.chanid)
        finally:
            self.lock.release()

    def _check_add_window--- This code section failed: ---

 L.1277         0  LOAD_FAST                'self'
                2  LOAD_ATTR                lock
                4  LOAD_METHOD              acquire
                6  CALL_METHOD_0         0  '0 positional arguments'
                8  POP_TOP          

 L.1278        10  SETUP_FINALLY       130  'to 130'

 L.1279        12  LOAD_FAST                'self'
               14  LOAD_ATTR                closed
               16  POP_JUMP_IF_TRUE     30  'to 30'
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                eof_received
               22  POP_JUMP_IF_TRUE     30  'to 30'
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                active
               28  POP_JUMP_IF_TRUE     34  'to 34'
             30_0  COME_FROM            22  '22'
             30_1  COME_FROM            16  '16'

 L.1280        30  LOAD_CONST               0
               32  RETURN_VALUE     
             34_0  COME_FROM            28  '28'

 L.1281        34  LOAD_FAST                'self'
               36  LOAD_ATTR                ultra_debug
               38  POP_JUMP_IF_FALSE    58  'to 58'

 L.1282        40  LOAD_FAST                'self'
               42  LOAD_METHOD              _log
               44  LOAD_GLOBAL              DEBUG
               46  LOAD_STR                 'addwindow {}'
               48  LOAD_METHOD              format
               50  LOAD_FAST                'n'
               52  CALL_METHOD_1         1  '1 positional argument'
               54  CALL_METHOD_2         2  '2 positional arguments'
               56  POP_TOP          
             58_0  COME_FROM            38  '38'

 L.1283        58  LOAD_FAST                'self'
               60  DUP_TOP          
               62  LOAD_ATTR                in_window_sofar
               64  LOAD_FAST                'n'
               66  INPLACE_ADD      
               68  ROT_TWO          
               70  STORE_ATTR               in_window_sofar

 L.1284        72  LOAD_FAST                'self'
               74  LOAD_ATTR                in_window_sofar
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                in_window_threshold
               80  COMPARE_OP               <=
               82  POP_JUMP_IF_FALSE    88  'to 88'

 L.1285        84  LOAD_CONST               0
               86  RETURN_VALUE     
             88_0  COME_FROM            82  '82'

 L.1286        88  LOAD_FAST                'self'
               90  LOAD_ATTR                ultra_debug
               92  POP_JUMP_IF_FALSE   114  'to 114'

 L.1287        94  LOAD_FAST                'self'
               96  LOAD_METHOD              _log

 L.1288        98  LOAD_GLOBAL              DEBUG
              100  LOAD_STR                 'addwindow send {}'
              102  LOAD_METHOD              format
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                in_window_sofar
              108  CALL_METHOD_1         1  '1 positional argument'
              110  CALL_METHOD_2         2  '2 positional arguments'
              112  POP_TOP          
            114_0  COME_FROM            92  '92'

 L.1290       114  LOAD_FAST                'self'
              116  LOAD_ATTR                in_window_sofar
              118  STORE_FAST               'out'

 L.1291       120  LOAD_CONST               0
              122  LOAD_FAST                'self'
              124  STORE_ATTR               in_window_sofar

 L.1292       126  LOAD_FAST                'out'
              128  RETURN_VALUE     
            130_0  COME_FROM_FINALLY    10  '10'

 L.1294       130  LOAD_FAST                'self'
              132  LOAD_ATTR                lock
              134  LOAD_METHOD              release
              136  CALL_METHOD_0         0  '0 positional arguments'
              138  POP_TOP          
              140  END_FINALLY      

Parse error at or near `COME_FROM_FINALLY' instruction at offset 130_0

    def _wait_for_send_window(self, size):
        """
        (You are already holding the lock.)
        Wait for the send window to open up, and allocate up to ``size`` bytes
        for transmission.  If no space opens up before the timeout, a timeout
        exception is raised.  Returns the number of bytes available to send
        (may be less than requested).
        """
        if self.closed or self.eof_sent:
            return 0
        if self.out_window_size == 0:
            if self.timeout == 0.0:
                raise socket.timeout()
            timeout = self.timeout
            while self.out_window_size == 0 and not self.closed:
                if self.eof_sent:
                    return 0
                then = time.time()
                self.out_buffer_cv.wait(timeout)
                if timeout is not None:
                    timeout -= time.time() - then
                    if timeout <= 0.0:
                        raise socket.timeout()

        if self.closed or self.eof_sent:
            return 0
        if self.out_window_size < size:
            size = self.out_window_size
        if self.out_max_packet_size - 64 < size:
            size = self.out_max_packet_size - 64
        self.out_window_size -= size
        if self.ultra_debug:
            self._log(DEBUG, 'window down to {}'.format(self.out_window_size))
        return size


class ChannelFile(BufferedFile):
    __doc__ = "\n    A file-like wrapper around `.Channel`.  A ChannelFile is created by calling\n    `Channel.makefile`.\n\n    .. warning::\n        To correctly emulate the file object created from a socket's `makefile\n        <python:socket.socket.makefile>` method, a `.Channel` and its\n        `.ChannelFile` should be able to be closed or garbage-collected\n        independently. Currently, closing the `ChannelFile` does nothing but\n        flush the buffer.\n    "

    def __init__(self, channel, mode='r', bufsize=-1):
        self.channel = channel
        BufferedFile.__init__(self)
        self._set_mode(mode, bufsize)

    def __repr__(self):
        """
        Returns a string representation of this object, for debugging.
        """
        return '<paramiko.ChannelFile from ' + repr(self.channel) + '>'

    def _read(self, size):
        return self.channel.recv(size)

    def _write(self, data):
        self.channel.sendall(data)
        return len(data)


class ChannelStderrFile(ChannelFile):
    __doc__ = '\n    A file-like wrapper around `.Channel` stderr.\n\n    See `Channel.makefile_stderr` for details.\n    '

    def _read(self, size):
        return self.channel.recv_stderr(size)

    def _write(self, data):
        self.channel.sendall_stderr(data)
        return len(data)


class ChannelStdinFile(ChannelFile):
    __doc__ = '\n    A file-like wrapper around `.Channel` stdin.\n\n    See `Channel.makefile_stdin` for details.\n    '

    def close(self):
        super(ChannelStdinFile, self).close()
        self.channel.shutdown_write()