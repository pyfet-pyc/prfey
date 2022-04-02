# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\paramiko\sftp_file.py
"""
SFTP file object
"""
from __future__ import with_statement
from binascii import hexlify
from collections import deque
import socket, threading, time
from paramiko.common import DEBUG
from paramiko.file import BufferedFile
from paramiko.py3compat import u, long
from paramiko.sftp import CMD_CLOSE, CMD_READ, CMD_DATA, SFTPError, CMD_WRITE, CMD_STATUS, CMD_FSTAT, CMD_ATTRS, CMD_FSETSTAT, CMD_EXTENDED
from paramiko.sftp_attr import SFTPAttributes

class SFTPFile(BufferedFile):
    __doc__ = '\n    Proxy object for a file on the remote server, in client mode SFTP.\n\n    Instances of this class may be used as context managers in the same way\n    that built-in Python file objects are.\n    '
    MAX_REQUEST_SIZE = 32768

    def __init__(self, sftp, handle, mode='r', bufsize=-1):
        BufferedFile.__init__(self)
        self.sftp = sftp
        self.handle = handle
        BufferedFile._set_mode(self, mode, bufsize)
        self.pipelined = False
        self._prefetching = False
        self._prefetch_done = False
        self._prefetch_data = {}
        self._prefetch_extents = {}
        self._prefetch_lock = threading.Lock()
        self._saved_exception = None
        self._reqs = deque()

    def __del__(self):
        self._close(async_=True)

    def close(self):
        """
        Close the file.
        """
        self._close(async_=False)

    def _close(self, async_=False):
        if self._closed:
            return
            self.sftp._log(DEBUG, 'close({})'.format(u(hexlify(self.handle))))
            if self.pipelined:
                self.sftp._finish_responses(self)
        else:
            BufferedFile.close(self)
            try:
                if async_:
                    self.sftp._async_request(type(None), CMD_CLOSE, self.handle)
                else:
                    self.sftp._request(CMD_CLOSE, self.handle)
            except EOFError:
                pass
            except (IOError, socket.error):
                pass

    def _data_in_prefetch_requests(self, offset, size):
        k = [x for x in list(self._prefetch_extents.values()) if x[0] <= offset]
        if len(k) == 0:
            return False
        k.sort(key=(lambda x: x[0]))
        buf_offset, buf_size = k[(-1)]
        if buf_offset + buf_size <= offset:
            return False
        if buf_offset + buf_size >= offset + size:
            return True
        return self._data_in_prefetch_requests(buf_offset + buf_size, offset + size - buf_offset - buf_size)

    def _data_in_prefetch_buffers(self, offset):
        """
        if a block of data is present in the prefetch buffers, at the given
        offset, return the offset of the relevant prefetch buffer.  otherwise,
        return None.  this guarantees nothing about the number of bytes
        collected in the prefetch buffer so far.
        """
        k = [i for i in self._prefetch_data.keys() if i <= offset]
        if len(k) == 0:
            return
        index = max(k)
        buf_offset = offset - index
        if buf_offset >= len(self._prefetch_data[index]):
            return
        return index

    def _read_prefetch(self, size):
        """
        read data out of the prefetch buffer, if possible.  if the data isn't
        in the buffer, return None.  otherwise, behaves like a normal read.
        """
        while 1:
            offset = self._data_in_prefetch_buffers(self._realpos)
            if offset is not None:
                break
            if not self._prefetch_done:
                if self._closed:
                    break
                self.sftp._read_response()
                self._check_exception()

        if offset is None:
            self._prefetching = False
            return
        prefetch = self._prefetch_data[offset]
        del self._prefetch_data[offset]
        buf_offset = self._realpos - offset
        if buf_offset > 0:
            self._prefetch_data[offset] = prefetch[:buf_offset]
            prefetch = prefetch[buf_offset:]
        if size < len(prefetch):
            self._prefetch_data[self._realpos + size] = prefetch[size:]
            prefetch = prefetch[:size]
        return prefetch

    def _read(self, size):
        size = min(size, self.MAX_REQUEST_SIZE)
        if self._prefetching:
            data = self._read_prefetch(size)
            if data is not None:
                return data
        t, msg = self.sftp._request(CMD_READ, self.handle, long(self._realpos), int(size))
        if t != CMD_DATA:
            raise SFTPError('Expected data')
        return msg.get_string()

    def _write--- This code section failed: ---

 L. 194         0  LOAD_GLOBAL              min
                2  LOAD_GLOBAL              len
                4  LOAD_FAST                'data'
                6  CALL_FUNCTION_1       1  '1 positional argument'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                MAX_REQUEST_SIZE
               12  CALL_FUNCTION_2       2  '2 positional arguments'
               14  STORE_FAST               'chunk'

 L. 195        16  LOAD_FAST                'self'
               18  LOAD_ATTR                sftp
               20  LOAD_METHOD              _async_request

 L. 196        22  LOAD_GLOBAL              type
               24  LOAD_CONST               None
               26  CALL_FUNCTION_1       1  '1 positional argument'

 L. 197        28  LOAD_GLOBAL              CMD_WRITE

 L. 198        30  LOAD_FAST                'self'
               32  LOAD_ATTR                handle

 L. 199        34  LOAD_GLOBAL              long
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                _realpos
               40  CALL_FUNCTION_1       1  '1 positional argument'

 L. 200        42  LOAD_FAST                'data'
               44  LOAD_CONST               None
               46  LOAD_FAST                'chunk'
               48  BUILD_SLICE_2         2 
               50  BINARY_SUBSCR    
               52  CALL_METHOD_5         5  '5 positional arguments'
               54  STORE_FAST               'sftp_async_request'

 L. 202        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _reqs
               60  LOAD_METHOD              append
               62  LOAD_FAST                'sftp_async_request'
               64  CALL_METHOD_1         1  '1 positional argument'
               66  POP_TOP          

 L. 203        68  LOAD_FAST                'self'
               70  LOAD_ATTR                pipelined
               72  POP_JUMP_IF_FALSE   100  'to 100'

 L. 204        74  LOAD_GLOBAL              len
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                _reqs
               80  CALL_FUNCTION_1       1  '1 positional argument'
               82  LOAD_CONST               100
               84  COMPARE_OP               >
               86  POP_JUMP_IF_FALSE   158  'to 158'
               88  LOAD_FAST                'self'
               90  LOAD_ATTR                sftp
               92  LOAD_ATTR                sock
               94  LOAD_METHOD              recv_ready
               96  CALL_METHOD_0         0  '0 positional arguments'
               98  POP_JUMP_IF_FALSE   158  'to 158'
            100_0  COME_FROM            72  '72'

 L. 206       100  SETUP_LOOP          158  'to 158'
            102_0  COME_FROM           144  '144'
              102  LOAD_GLOBAL              len
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                _reqs
              108  CALL_FUNCTION_1       1  '1 positional argument'
              110  POP_JUMP_IF_FALSE   156  'to 156'

 L. 207       112  LOAD_FAST                'self'
              114  LOAD_ATTR                _reqs
              116  LOAD_METHOD              popleft
              118  CALL_METHOD_0         0  '0 positional arguments'
              120  STORE_FAST               'req'

 L. 208       122  LOAD_FAST                'self'
              124  LOAD_ATTR                sftp
              126  LOAD_METHOD              _read_response
              128  LOAD_FAST                'req'
              130  CALL_METHOD_1         1  '1 positional argument'
              132  UNPACK_SEQUENCE_2     2 
              134  STORE_FAST               't'
              136  STORE_FAST               'msg'

 L. 209       138  LOAD_FAST                't'
              140  LOAD_GLOBAL              CMD_STATUS
              142  COMPARE_OP               !=
              144  POP_JUMP_IF_FALSE   102  'to 102'

 L. 210       146  LOAD_GLOBAL              SFTPError
              148  LOAD_STR                 'Expected status'
              150  CALL_FUNCTION_1       1  '1 positional argument'
              152  RAISE_VARARGS_1       1  'exception instance'
              154  JUMP_BACK           102  'to 102'
            156_0  COME_FROM           110  '110'
              156  POP_BLOCK        
            158_0  COME_FROM_LOOP      100  '100'
            158_1  COME_FROM            98  '98'
            158_2  COME_FROM            86  '86'

 L. 212       158  LOAD_FAST                'chunk'
              160  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 160

    def settimeout(self, timeout):
        """
        Set a timeout on read/write operations on the underlying socket or
        ssh `.Channel`.

        :param float timeout:
            seconds to wait for a pending read/write operation before raising
            ``socket.timeout``, or ``None`` for no timeout

        .. seealso:: `.Channel.settimeout`
        """
        self.sftp.sock.settimeout(timeout)

    def gettimeout(self):
        """
        Returns the timeout in seconds (as a `float`) associated with the
        socket or ssh `.Channel` used for this file.

        .. seealso:: `.Channel.gettimeout`
        """
        return self.sftp.sock.gettimeout()

    def setblocking(self, blocking):
        """
        Set blocking or non-blocking mode on the underiying socket or ssh
        `.Channel`.

        :param int blocking:
            0 to set non-blocking mode; non-0 to set blocking mode.

        .. seealso:: `.Channel.setblocking`
        """
        self.sftp.sock.setblocking(blocking)

    def seekable(self):
        """
        Check if the file supports random access.

        :return:
            `True` if the file supports random access. If `False`,
            :meth:`seek` will raise an exception
        """
        return True

    def seek(self, offset, whence=0):
        """
        Set the file's current position.

        See `file.seek` for details.
        """
        self.flush()
        if whence == self.SEEK_SET:
            self._realpos = self._pos = offset
        else:
            if whence == self.SEEK_CUR:
                self._pos += offset
                self._realpos = self._pos
            else:
                self._realpos = self._pos = self._get_size() + offset
        self._rbuffer = bytes()

    def stat(self):
        """
        Retrieve information about this file from the remote system.  This is
        exactly like `.SFTPClient.stat`, except that it operates on an
        already-open file.

        :returns:
            an `.SFTPAttributes` object containing attributes about this file.
        """
        t, msg = self.sftp._request(CMD_FSTAT, self.handle)
        if t != CMD_ATTRS:
            raise SFTPError('Expected attributes')
        return SFTPAttributes._from_msg(msg)

    def chmod(self, mode):
        """
        Change the mode (permissions) of this file.  The permissions are
        unix-style and identical to those used by Python's `os.chmod`
        function.

        :param int mode: new permissions
        """
        self.sftp._log(DEBUG, 'chmod({}, {!r})'.format(hexlify(self.handle), mode))
        attr = SFTPAttributes()
        attr.st_mode = mode
        self.sftp._request(CMD_FSETSTAT, self.handle, attr)

    def chown(self, uid, gid):
        """
        Change the owner (``uid``) and group (``gid``) of this file.  As with
        Python's `os.chown` function, you must pass both arguments, so if you
        only want to change one, use `stat` first to retrieve the current
        owner and group.

        :param int uid: new owner's uid
        :param int gid: new group id
        """
        self.sftp._log(DEBUG, 'chown({}, {!r}, {!r})'.format(hexlify(self.handle), uid, gid))
        attr = SFTPAttributes()
        attr.st_uid, attr.st_gid = uid, gid
        self.sftp._request(CMD_FSETSTAT, self.handle, attr)

    def utime(self, times):
        """
        Set the access and modified times of this file.  If
        ``times`` is ``None``, then the file's access and modified times are
        set to the current time.  Otherwise, ``times`` must be a 2-tuple of
        numbers, of the form ``(atime, mtime)``, which is used to set the
        access and modified times, respectively.  This bizarre API is mimicked
        from Python for the sake of consistency -- I apologize.

        :param tuple times:
            ``None`` or a tuple of (access time, modified time) in standard
            internet epoch time (seconds since 01 January 1970 GMT)
        """
        if times is None:
            times = (
             time.time(), time.time())
        self.sftp._log(DEBUG, 'utime({}, {!r})'.format(hexlify(self.handle), times))
        attr = SFTPAttributes()
        attr.st_atime, attr.st_mtime = times
        self.sftp._request(CMD_FSETSTAT, self.handle, attr)

    def truncate(self, size):
        """
        Change the size of this file.  This usually extends
        or shrinks the size of the file, just like the ``truncate()`` method on
        Python file objects.

        :param size: the new size of the file
        """
        self.sftp._log(DEBUG, 'truncate({}, {!r})'.format(hexlify(self.handle), size))
        attr = SFTPAttributes()
        attr.st_size = size
        self.sftp._request(CMD_FSETSTAT, self.handle, attr)

    def check(self, hash_algorithm, offset=0, length=0, block_size=0):
        """
        Ask the server for a hash of a section of this file.  This can be used
        to verify a successful upload or download, or for various rsync-like
        operations.

        The file is hashed from ``offset``, for ``length`` bytes.
        If ``length`` is 0, the remainder of the file is hashed.  Thus, if both
        ``offset`` and ``length`` are zero, the entire file is hashed.

        Normally, ``block_size`` will be 0 (the default), and this method will
        return a byte string representing the requested hash (for example, a
        string of length 16 for MD5, or 20 for SHA-1).  If a non-zero
        ``block_size`` is given, each chunk of the file (from ``offset`` to
        ``offset + length``) of ``block_size`` bytes is computed as a separate
        hash.  The hash results are all concatenated and returned as a single
        string.

        For example, ``check('sha1', 0, 1024, 512)`` will return a string of
        length 40.  The first 20 bytes will be the SHA-1 of the first 512 bytes
        of the file, and the last 20 bytes will be the SHA-1 of the next 512
        bytes.

        :param str hash_algorithm:
            the name of the hash algorithm to use (normally ``"sha1"`` or
            ``"md5"``)
        :param offset:
            offset into the file to begin hashing (0 means to start from the
            beginning)
        :param length:
            number of bytes to hash (0 means continue to the end of the file)
        :param int block_size:
            number of bytes to hash per result (must not be less than 256; 0
            means to compute only one hash of the entire segment)
        :return:
            `str` of bytes representing the hash of each block, concatenated
            together

        :raises:
            ``IOError`` -- if the server doesn't support the "check-file"
            extension, or possibly doesn't support the hash algorithm requested

        .. note:: Many (most?) servers don't support this extension yet.

        .. versionadded:: 1.4
        """
        t, msg = self.sftp._request(CMD_EXTENDED, 'check-file', self.handle, hash_algorithm, long(offset), long(length), block_size)
        msg.get_text()
        msg.get_text()
        data = msg.get_remainder()
        return data

    def set_pipelined(self, pipelined=True):
        """
        Turn on/off the pipelining of write operations to this file.  When
        pipelining is on, paramiko won't wait for the server response after
        each write operation.  Instead, they're collected as they come in. At
        the first non-write operation (including `.close`), all remaining
        server responses are collected.  This means that if there was an error
        with one of your later writes, an exception might be thrown from within
        `.close` instead of `.write`.

        By default, files are not pipelined.

        :param bool pipelined:
            ``True`` if pipelining should be turned on for this file; ``False``
            otherwise

        .. versionadded:: 1.5
        """
        self.pipelined = pipelined

    def prefetch(self, file_size=None):
        """
        Pre-fetch the remaining contents of this file in anticipation of future
        `.read` calls.  If reading the entire file, pre-fetching can
        dramatically improve the download speed by avoiding roundtrip latency.
        The file's contents are incrementally buffered in a background thread.

        The prefetched data is stored in a buffer until read via the `.read`
        method.  Once data has been read, it's removed from the buffer.  The
        data may be read in a random order (using `.seek`); chunks of the
        buffer that haven't been read will continue to be buffered.

        :param int file_size:
            When this is ``None`` (the default), this method calls `stat` to
            determine the remote file size. In some situations, doing so can
            cause exceptions or hangs (see `#562
            <https://github.com/paramiko/paramiko/pull/562>`_); as a
            workaround, one may call `stat` explicitly and pass its value in
            via this parameter.

        .. versionadded:: 1.5.1
        .. versionchanged:: 1.16.0
            The ``file_size`` parameter was added (with no default value).
        .. versionchanged:: 1.16.1
            The ``file_size`` parameter was made optional for backwards
            compatibility.
        """
        if file_size is None:
            file_size = self.stat().st_size
        chunks = []
        n = self._realpos
        while n < file_size:
            chunk = min(self.MAX_REQUEST_SIZE, file_size - n)
            chunks.append((n, chunk))
            n += chunk

        if len(chunks) > 0:
            self._start_prefetch(chunks)

    def readv(self, chunks):
        """
        Read a set of blocks from the file by (offset, length).  This is more
        efficient than doing a series of `.seek` and `.read` calls, since the
        prefetch machinery is used to retrieve all the requested blocks at
        once.

        :param chunks:
            a list of ``(offset, length)`` tuples indicating which sections of
            the file to read
        :return: a list of blocks read, in the same order as in ``chunks``

        .. versionadded:: 1.5.4
        """
        self.sftp._log(DEBUG, 'readv({}, {!r})'.format(hexlify(self.handle), chunks))
        read_chunks = []
        for offset, size in chunks:
            if not self._data_in_prefetch_buffers(offset):
                if self._data_in_prefetch_requests(offset, size):
                    continue
                while size > 0:
                    chunk_size = min(size, self.MAX_REQUEST_SIZE)
                    read_chunks.append((offset, chunk_size))
                    offset += chunk_size
                    size -= chunk_size

        self._start_prefetch(read_chunks)
        for x in chunks:
            self.seek(x[0])
            yield self.read(x[1])

    def _get_size(self):
        try:
            return self.stat().st_size
        except:
            return 0

    def _start_prefetch(self, chunks):
        self._prefetching = True
        self._prefetch_done = False
        t = threading.Thread(target=(self._prefetch_thread), args=(chunks,))
        t.setDaemon(True)
        t.start()

    def _prefetch_thread(self, chunks):
        for offset, length in chunks:
            num = self.sftp._async_requestselfCMD_READself.handlelong(offset)int(length)
            with self._prefetch_lock:
                self._prefetch_extents[num] = (
                 offset, length)

    def _async_response(self, t, msg, num):
        if t == CMD_STATUS:
            try:
                self.sftp._convert_status(msg)
            except Exception as e:
                try:
                    self._saved_exception = e
                finally:
                    e = None
                    del e

            return
        if t != CMD_DATA:
            raise SFTPError('Expected data')
        data = msg.get_string()
        while True:
            with self._prefetch_lock:
                if num in self._prefetch_extents:
                    offset, length = self._prefetch_extents[num]
                    self._prefetch_data[offset] = data
                    del self._prefetch_extents[num]
                    if len(self._prefetch_extents) == 0:
                        self._prefetch_done = True
                    break

    def _check_exception(self):
        """if there's a saved exception, raise & clear it"""
        if self._saved_exception is not None:
            x = self._saved_exception
            self._saved_exception = None
            raise x