# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\dns\query.py
"""Talk to a DNS server."""
from __future__ import generators
import errno, select, socket, struct, sys, time, dns.exception, dns.inet, dns.name, dns.message, dns.rcode, dns.rdataclass, dns.rdatatype
from ._compat import long, string_types, PY3
if PY3:
    select_error = OSError
else:
    select_error = select.error
socket_factory = socket.socket

class UnexpectedSource(dns.exception.DNSException):
    __doc__ = 'A DNS query response came from an unexpected address or port.'


class BadResponse(dns.exception.FormError):
    __doc__ = 'A DNS query response does not respond to the question asked.'


class TransferError(dns.exception.DNSException):
    __doc__ = 'A zone transfer response got a non-zero rcode.'

    def __init__(self, rcode):
        message = 'Zone transfer error: %s' % dns.rcode.to_text(rcode)
        super(TransferError, self).__init__(message)
        self.rcode = rcode


def _compute_expiration(timeout):
    if timeout is None:
        return
    return time.time() + timeout


def _poll_for(fd, readable, writable, error, timeout):
    """Poll polling backend."""
    event_mask = 0
    if readable:
        event_mask |= select.POLLIN
    if writable:
        event_mask |= select.POLLOUT
    if error:
        event_mask |= select.POLLERR
    pollable = select.poll()
    pollable.register(fd, event_mask)
    if timeout:
        event_list = pollable.poll(long(timeout * 1000))
    else:
        event_list = pollable.poll()
    return bool(event_list)


def _select_for(fd, readable, writable, error, timeout):
    """Select polling backend."""
    rset, wset, xset = [], [], []
    if readable:
        rset = [
         fd]
    if writable:
        wset = [
         fd]
    if error:
        xset = [
         fd]
    if timeout is None:
        rcount, wcount, xcount = select.select(rset, wset, xset)
    else:
        rcount, wcount, xcount = select.select(rset, wset, xset, timeout)
    return bool(rcount or wcount or xcount)


def _wait_for(fd, readable, writable, error, expiration):
    global _polling_backend
    done = False
    while True:
        if not done:
            if expiration is None:
                timeout = None
            else:
                timeout = expiration - time.time()
                if timeout <= 0.0:
                    raise dns.exception.Timeout
            try:
                if not _polling_backend(fd, readable, writable, error, timeout):
                    raise dns.exception.Timeout
            except select_error as e:
                try:
                    if e.args[0] != errno.EINTR:
                        raise e
                finally:
                    e = None
                    del e

            else:
                done = True


def _set_polling_backend(fn):
    global _polling_backend
    _polling_backend = fn


if hasattr(select, 'poll'):
    _polling_backend = _poll_for
else:
    _polling_backend = _select_for

def _wait_for_readable(s, expiration):
    _wait_for(s, True, False, True, expiration)


def _wait_for_writable(s, expiration):
    _wait_for(s, False, True, True, expiration)


def _addresses_equal(af, a1, a2):
    try:
        n1 = dns.inet.inet_pton(af, a1[0])
        n2 = dns.inet.inet_pton(af, a2[0])
    except dns.exception.SyntaxError:
        return False
    else:
        return n1 == n2 and a1[1:] == a2[1:]


def _destination_and_source(af, where, port, source, source_port):
    if af is None:
        try:
            af = dns.inet.af_for_address(where)
        except Exception:
            af = dns.inet.AF_INET

        if af == dns.inet.AF_INET:
            destination = (
             where, port)
            if source is not None or source_port != 0:
                if source is None:
                    source = '0.0.0.0'
                source = (
                 source, source_port)
        elif af == dns.inet.AF_INET6:
            destination = (
             where, port, 0, 0)
            if source is not None or (source_port != 0):
                if source is None:
                    source = '::'
                source = (
                 source, source_port, 0, 0)
        return (
         af, destination, source)


def send_udp(sock, what, destination, expiration=None):
    """Send a DNS message to the specified UDP socket.

    *sock*, a ``socket``.

    *what*, a ``binary`` or ``dns.message.Message``, the message to send.

    *destination*, a destination tuple appropriate for the address family
    of the socket, specifying where to send the query.

    *expiration*, a ``float`` or ``None``, the absolute time at which
    a timeout exception should be raised.  If ``None``, no timeout will
    occur.

    Returns an ``(int, float)`` tuple of bytes sent and the sent time.
    """
    if isinstance(what, dns.message.Message):
        what = what.to_wire()
    _wait_for_writable(sock, expiration)
    sent_time = time.time()
    n = sock.sendto(what, destination)
    return (
     n, sent_time)


def receive_udp(sock, destination, expiration=None, ignore_unexpected=False, one_rr_per_rrset=False, keyring=None, request_mac=b'', ignore_trailing=False):
    """Read a DNS message from a UDP socket.

    *sock*, a ``socket``.

    *destination*, a destination tuple appropriate for the address family
    of the socket, specifying where the associated query was sent.

    *expiration*, a ``float`` or ``None``, the absolute time at which
    a timeout exception should be raised.  If ``None``, no timeout will
    occur.

    *ignore_unexpected*, a ``bool``.  If ``True``, ignore responses from
    unexpected sources.

    *one_rr_per_rrset*, a ``bool``.  If ``True``, put each RR into its own
    RRset.

    *keyring*, a ``dict``, the keyring to use for TSIG.

    *request_mac*, a ``binary``, the MAC of the request (for TSIG).

    *ignore_trailing*, a ``bool``.  If ``True``, ignore trailing
    junk at end of the received message.

    Raises if the message is malformed, if network errors occur, of if
    there is a timeout.

    Returns a ``dns.message.Message`` object.
    """
    wire = b''
    while True:
        _wait_for_readable(sock, expiration)
        wire, from_address = sock.recvfrom(65535)
        if not _addresses_equal(sock.family, from_address, destination):
            if dns.inet.is_multicast(destination[0]):
                if from_address[1:] == destination[1:]:
                    break
            if not ignore_unexpected:
                raise UnexpectedSource('got a response from %s instead of %s' % (
                 from_address,
                 destination))

    received_time = time.time()
    r = dns.message.from_wire(wire, keyring=keyring, request_mac=request_mac, one_rr_per_rrset=one_rr_per_rrset,
      ignore_trailing=ignore_trailing)
    return (
     r, received_time)


def udp(q, where, timeout=None, port=53, af=None, source=None, source_port=0, ignore_unexpected=False, one_rr_per_rrset=False, ignore_trailing=False):
    """Return the response obtained after sending a query via UDP.

    *q*, a ``dns.message.Message``, the query to send

    *where*, a ``text`` containing an IPv4 or IPv6 address,  where
    to send the message.

    *timeout*, a ``float`` or ``None``, the number of seconds to wait before the
    query times out.  If ``None``, the default, wait forever.

    *port*, an ``int``, the port send the message to.  The default is 53.

    *af*, an ``int``, the address family to use.  The default is ``None``,
    which causes the address family to use to be inferred from the form of
    *where*.  If the inference attempt fails, AF_INET is used.  This
    parameter is historical; you need never set it.

    *source*, a ``text`` containing an IPv4 or IPv6 address, specifying
    the source address.  The default is the wildcard address.

    *source_port*, an ``int``, the port from which to send the message.
    The default is 0.

    *ignore_unexpected*, a ``bool``.  If ``True``, ignore responses from
    unexpected sources.

    *one_rr_per_rrset*, a ``bool``.  If ``True``, put each RR into its own
    RRset.

    *ignore_trailing*, a ``bool``.  If ``True``, ignore trailing
    junk at end of the received message.

    Returns a ``dns.message.Message``.
    """
    wire = q.to_wire()
    af, destination, source = _destination_and_source(af, where, port, source, source_port)
    s = socket_factory(af, socket.SOCK_DGRAM, 0)
    received_time = None
    sent_time = None
    try:
        expiration = _compute_expiration(timeout)
        s.setblocking(0)
        if source is not None:
            s.bind(source)
        _, sent_time = send_udp(s, wire, destination, expiration)
        r, received_time = receive_udp(s, destination, expiration, ignore_unexpected, one_rr_per_rrset, q.keyring, q.mac, ignore_trailing)
    finally:
        if sent_time is None or received_time is None:
            response_time = 0
        else:
            response_time = received_time - sent_time
        s.close()

    r.time = response_time
    if not q.is_response(r):
        raise BadResponse
    return r


def _net_read(sock, count, expiration):
    """Read the specified number of bytes from sock.  Keep trying until we
    either get the desired amount, or we hit EOF.
    A Timeout exception will be raised if the operation is not completed
    by the expiration time.
    """
    s = b''
    while True:
        if count > 0:
            _wait_for_readable(sock, expiration)
            n = sock.recv(count)
            if n == b'':
                raise EOFError
            count = count - len(n)
            s = s + n

    return s


def _net_write(sock, data, expiration):
    """Write the specified data to the socket.
    A Timeout exception will be raised if the operation is not completed
    by the expiration time.
    """
    current = 0
    l = len(data)
    while True:
        if current < l:
            _wait_for_writable(sock, expiration)
            current += sock.send(data[current:])


def send_tcp(sock, what, expiration=None):
    """Send a DNS message to the specified TCP socket.

    *sock*, a ``socket``.

    *what*, a ``binary`` or ``dns.message.Message``, the message to send.

    *expiration*, a ``float`` or ``None``, the absolute time at which
    a timeout exception should be raised.  If ``None``, no timeout will
    occur.

    Returns an ``(int, float)`` tuple of bytes sent and the sent time.
    """
    if isinstance(what, dns.message.Message):
        what = what.to_wire()
    l = len(what)
    tcpmsg = struct.pack('!H', l) + what
    _wait_for_writable(sock, expiration)
    sent_time = time.time()
    _net_write(sock, tcpmsg, expiration)
    return (
     len(tcpmsg), sent_time)


def receive_tcp(sock, expiration=None, one_rr_per_rrset=False, keyring=None, request_mac=b'', ignore_trailing=False):
    """Read a DNS message from a TCP socket.

    *sock*, a ``socket``.

    *expiration*, a ``float`` or ``None``, the absolute time at which
    a timeout exception should be raised.  If ``None``, no timeout will
    occur.

    *one_rr_per_rrset*, a ``bool``.  If ``True``, put each RR into its own
    RRset.

    *keyring*, a ``dict``, the keyring to use for TSIG.

    *request_mac*, a ``binary``, the MAC of the request (for TSIG).

    *ignore_trailing*, a ``bool``.  If ``True``, ignore trailing
    junk at end of the received message.

    Raises if the message is malformed, if network errors occur, of if
    there is a timeout.

    Returns a ``dns.message.Message`` object.
    """
    ldata = _net_read(sock, 2, expiration)
    l, = struct.unpack('!H', ldata)
    wire = _net_read(sock, l, expiration)
    received_time = time.time()
    r = dns.message.from_wire(wire, keyring=keyring, request_mac=request_mac, one_rr_per_rrset=one_rr_per_rrset,
      ignore_trailing=ignore_trailing)
    return (
     r, received_time)


def _connect(s, address):
    try:
        s.connect(address)
    except socket.error:
        ty, v = sys.exc_info()[:2]
        if hasattr(v, 'errno'):
            v_err = v.errno
        else:
            v_err = v[0]
        if v_err not in (errno.EINPROGRESS, errno.EWOULDBLOCK, errno.EALREADY):
            raise v


def tcp(q, where, timeout=None, port=53, af=None, source=None, source_port=0, one_rr_per_rrset=False, ignore_trailing=False):
    """Return the response obtained after sending a query via TCP.

    *q*, a ``dns.message.Message``, the query to send

    *where*, a ``text`` containing an IPv4 or IPv6 address,  where
    to send the message.

    *timeout*, a ``float`` or ``None``, the number of seconds to wait before the
    query times out.  If ``None``, the default, wait forever.

    *port*, an ``int``, the port send the message to.  The default is 53.

    *af*, an ``int``, the address family to use.  The default is ``None``,
    which causes the address family to use to be inferred from the form of
    *where*.  If the inference attempt fails, AF_INET is used.  This
    parameter is historical; you need never set it.

    *source*, a ``text`` containing an IPv4 or IPv6 address, specifying
    the source address.  The default is the wildcard address.

    *source_port*, an ``int``, the port from which to send the message.
    The default is 0.

    *one_rr_per_rrset*, a ``bool``.  If ``True``, put each RR into its own
    RRset.

    *ignore_trailing*, a ``bool``.  If ``True``, ignore trailing
    junk at end of the received message.

    Returns a ``dns.message.Message``.
    """
    wire = q.to_wire()
    af, destination, source = _destination_and_source(af, where, port, source, source_port)
    s = socket_factory(af, socket.SOCK_STREAM, 0)
    begin_time = None
    received_time = None
    try:
        expiration = _compute_expiration(timeout)
        s.setblocking(0)
        begin_time = time.time()
        if source is not None:
            s.bind(source)
        _connect(s, destination)
        send_tcp(s, wire, expiration)
        r, received_time = receive_tcp(s, expiration, one_rr_per_rrset, q.keyring, q.mac, ignore_trailing)
    finally:
        if begin_time is None or received_time is None:
            response_time = 0
        else:
            response_time = received_time - begin_time
        s.close()

    r.time = response_time
    if not q.is_response(r):
        raise BadResponse
    return r


def xfr--- This code section failed: ---

 L. 565         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'zone'
                4  LOAD_GLOBAL              string_types
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    22  'to 22'

 L. 566        10  LOAD_GLOBAL              dns
               12  LOAD_ATTR                name
               14  LOAD_METHOD              from_text
               16  LOAD_FAST                'zone'
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'zone'
             22_0  COME_FROM             8  '8'

 L. 567        22  LOAD_GLOBAL              isinstance
               24  LOAD_FAST                'rdtype'
               26  LOAD_GLOBAL              string_types
               28  CALL_FUNCTION_2       2  ''
               30  POP_JUMP_IF_FALSE    44  'to 44'

 L. 568        32  LOAD_GLOBAL              dns
               34  LOAD_ATTR                rdatatype
               36  LOAD_METHOD              from_text
               38  LOAD_FAST                'rdtype'
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'rdtype'
             44_0  COME_FROM            30  '30'

 L. 569        44  LOAD_GLOBAL              dns
               46  LOAD_ATTR                message
               48  LOAD_METHOD              make_query
               50  LOAD_FAST                'zone'
               52  LOAD_FAST                'rdtype'
               54  LOAD_FAST                'rdclass'
               56  CALL_METHOD_3         3  ''
               58  STORE_FAST               'q'

 L. 570        60  LOAD_FAST                'rdtype'
               62  LOAD_GLOBAL              dns
               64  LOAD_ATTR                rdatatype
               66  LOAD_ATTR                IXFR
               68  COMPARE_OP               ==
               70  POP_JUMP_IF_FALSE   108  'to 108'

 L. 571        72  LOAD_GLOBAL              dns
               74  LOAD_ATTR                rrset
               76  LOAD_METHOD              from_text
               78  LOAD_FAST                'zone'
               80  LOAD_CONST               0
               82  LOAD_STR                 'IN'
               84  LOAD_STR                 'SOA'

 L. 572        86  LOAD_STR                 '. . %u 0 0 0 0'
               88  LOAD_FAST                'serial'
               90  BINARY_MODULO    

 L. 571        92  CALL_METHOD_5         5  ''
               94  STORE_FAST               'rrset'

 L. 573        96  LOAD_FAST                'q'
               98  LOAD_ATTR                authority
              100  LOAD_METHOD              append
              102  LOAD_FAST                'rrset'
              104  CALL_METHOD_1         1  ''
              106  POP_TOP          
            108_0  COME_FROM            70  '70'

 L. 574       108  LOAD_FAST                'keyring'
              110  LOAD_CONST               None
              112  COMPARE_OP               is-not
              114  POP_JUMP_IF_FALSE   132  'to 132'

 L. 575       116  LOAD_FAST                'q'
              118  LOAD_ATTR                use_tsig
              120  LOAD_FAST                'keyring'
              122  LOAD_FAST                'keyname'
              124  LOAD_FAST                'keyalgorithm'
              126  LOAD_CONST               ('algorithm',)
              128  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              130  POP_TOP          
            132_0  COME_FROM           114  '114'

 L. 576       132  LOAD_FAST                'q'
              134  LOAD_METHOD              to_wire
              136  CALL_METHOD_0         0  ''
              138  STORE_FAST               'wire'

 L. 577       140  LOAD_GLOBAL              _destination_and_source
              142  LOAD_FAST                'af'
              144  LOAD_FAST                'where'
              146  LOAD_FAST                'port'

 L. 578       148  LOAD_FAST                'source'

 L. 578       150  LOAD_FAST                'source_port'

 L. 577       152  CALL_FUNCTION_5       5  ''
              154  UNPACK_SEQUENCE_3     3 
              156  STORE_FAST               'af'
              158  STORE_FAST               'destination'
              160  STORE_FAST               'source'

 L. 579       162  LOAD_FAST                'use_udp'
              164  POP_JUMP_IF_FALSE   202  'to 202'

 L. 580       166  LOAD_FAST                'rdtype'
              168  LOAD_GLOBAL              dns
              170  LOAD_ATTR                rdatatype
              172  LOAD_ATTR                IXFR
              174  COMPARE_OP               !=
              176  POP_JUMP_IF_FALSE   186  'to 186'

 L. 581       178  LOAD_GLOBAL              ValueError
              180  LOAD_STR                 'cannot do a UDP AXFR'
              182  CALL_FUNCTION_1       1  ''
              184  RAISE_VARARGS_1       1  'exception instance'
            186_0  COME_FROM           176  '176'

 L. 582       186  LOAD_GLOBAL              socket_factory
              188  LOAD_FAST                'af'
              190  LOAD_GLOBAL              socket
              192  LOAD_ATTR                SOCK_DGRAM
              194  LOAD_CONST               0
              196  CALL_FUNCTION_3       3  ''
              198  STORE_FAST               's'
              200  JUMP_FORWARD        216  'to 216'
            202_0  COME_FROM           164  '164'

 L. 584       202  LOAD_GLOBAL              socket_factory
              204  LOAD_FAST                'af'
              206  LOAD_GLOBAL              socket
              208  LOAD_ATTR                SOCK_STREAM
              210  LOAD_CONST               0
              212  CALL_FUNCTION_3       3  ''
              214  STORE_FAST               's'
            216_0  COME_FROM           200  '200'

 L. 585       216  LOAD_FAST                's'
              218  LOAD_METHOD              setblocking
              220  LOAD_CONST               0
              222  CALL_METHOD_1         1  ''
              224  POP_TOP          

 L. 586       226  LOAD_FAST                'source'
              228  LOAD_CONST               None
              230  COMPARE_OP               is-not
              232  POP_JUMP_IF_FALSE   244  'to 244'

 L. 587       234  LOAD_FAST                's'
              236  LOAD_METHOD              bind
              238  LOAD_FAST                'source'
              240  CALL_METHOD_1         1  ''
              242  POP_TOP          
            244_0  COME_FROM           232  '232'

 L. 588       244  LOAD_GLOBAL              _compute_expiration
              246  LOAD_FAST                'lifetime'
              248  CALL_FUNCTION_1       1  ''
              250  STORE_FAST               'expiration'

 L. 589       252  LOAD_GLOBAL              _connect
              254  LOAD_FAST                's'
              256  LOAD_FAST                'destination'
              258  CALL_FUNCTION_2       2  ''
              260  POP_TOP          

 L. 590       262  LOAD_GLOBAL              len
              264  LOAD_FAST                'wire'
              266  CALL_FUNCTION_1       1  ''
              268  STORE_FAST               'l'

 L. 591       270  LOAD_FAST                'use_udp'
          272_274  POP_JUMP_IF_FALSE   298  'to 298'

 L. 592       276  LOAD_GLOBAL              _wait_for_writable
              278  LOAD_FAST                's'
              280  LOAD_FAST                'expiration'
              282  CALL_FUNCTION_2       2  ''
              284  POP_TOP          

 L. 593       286  LOAD_FAST                's'
              288  LOAD_METHOD              send
              290  LOAD_FAST                'wire'
              292  CALL_METHOD_1         1  ''
              294  POP_TOP          
              296  JUMP_FORWARD        326  'to 326'
            298_0  COME_FROM           272  '272'

 L. 595       298  LOAD_GLOBAL              struct
              300  LOAD_METHOD              pack
              302  LOAD_STR                 '!H'
              304  LOAD_FAST                'l'
              306  CALL_METHOD_2         2  ''
              308  LOAD_FAST                'wire'
              310  BINARY_ADD       
              312  STORE_FAST               'tcpmsg'

 L. 596       314  LOAD_GLOBAL              _net_write
              316  LOAD_FAST                's'
              318  LOAD_FAST                'tcpmsg'
              320  LOAD_FAST                'expiration'
              322  CALL_FUNCTION_3       3  ''
              324  POP_TOP          
            326_0  COME_FROM           296  '296'

 L. 597       326  LOAD_CONST               False
              328  STORE_FAST               'done'

 L. 598       330  LOAD_CONST               True
              332  STORE_FAST               'delete_mode'

 L. 599       334  LOAD_CONST               False
              336  STORE_FAST               'expecting_SOA'

 L. 600       338  LOAD_CONST               None
              340  STORE_FAST               'soa_rrset'

 L. 601       342  LOAD_FAST                'relativize'
          344_346  POP_JUMP_IF_FALSE   362  'to 362'

 L. 602       348  LOAD_FAST                'zone'
              350  STORE_FAST               'origin'

 L. 603       352  LOAD_GLOBAL              dns
              354  LOAD_ATTR                name
              356  LOAD_ATTR                empty
              358  STORE_FAST               'oname'
              360  JUMP_FORWARD        370  'to 370'
            362_0  COME_FROM           344  '344'

 L. 605       362  LOAD_CONST               None
              364  STORE_FAST               'origin'

 L. 606       366  LOAD_FAST                'zone'
              368  STORE_FAST               'oname'
            370_0  COME_FROM           360  '360'

 L. 607       370  LOAD_CONST               None
              372  STORE_FAST               'tsig_ctx'

 L. 608       374  LOAD_CONST               True
              376  STORE_FAST               'first'
            378_0  COME_FROM           950  '950'

 L. 609       378  LOAD_FAST                'done'
          380_382  POP_JUMP_IF_TRUE    954  'to 954'

 L. 610       384  LOAD_GLOBAL              _compute_expiration
              386  LOAD_FAST                'timeout'
              388  CALL_FUNCTION_1       1  ''
              390  STORE_FAST               'mexpiration'

 L. 611       392  LOAD_FAST                'mexpiration'
              394  LOAD_CONST               None
              396  COMPARE_OP               is
          398_400  POP_JUMP_IF_TRUE    412  'to 412'
              402  LOAD_FAST                'mexpiration'
              404  LOAD_FAST                'expiration'
              406  COMPARE_OP               >
          408_410  POP_JUMP_IF_FALSE   416  'to 416'
            412_0  COME_FROM           398  '398'

 L. 612       412  LOAD_FAST                'expiration'
              414  STORE_FAST               'mexpiration'
            416_0  COME_FROM           408  '408'

 L. 613       416  LOAD_FAST                'use_udp'
          418_420  POP_JUMP_IF_FALSE   448  'to 448'

 L. 614       422  LOAD_GLOBAL              _wait_for_readable
              424  LOAD_FAST                's'
              426  LOAD_FAST                'expiration'
              428  CALL_FUNCTION_2       2  ''
              430  POP_TOP          

 L. 615       432  LOAD_FAST                's'
              434  LOAD_METHOD              recvfrom
              436  LOAD_CONST               65535
              438  CALL_METHOD_1         1  ''
              440  UNPACK_SEQUENCE_2     2 
              442  STORE_FAST               'wire'
              444  STORE_FAST               'from_address'
              446  JUMP_FORWARD        486  'to 486'
            448_0  COME_FROM           418  '418'

 L. 617       448  LOAD_GLOBAL              _net_read
              450  LOAD_FAST                's'
              452  LOAD_CONST               2
              454  LOAD_FAST                'mexpiration'
              456  CALL_FUNCTION_3       3  ''
              458  STORE_FAST               'ldata'

 L. 618       460  LOAD_GLOBAL              struct
              462  LOAD_METHOD              unpack
              464  LOAD_STR                 '!H'
              466  LOAD_FAST                'ldata'
              468  CALL_METHOD_2         2  ''
              470  UNPACK_SEQUENCE_1     1 
              472  STORE_FAST               'l'

 L. 619       474  LOAD_GLOBAL              _net_read
              476  LOAD_FAST                's'
              478  LOAD_FAST                'l'
              480  LOAD_FAST                'mexpiration'
              482  CALL_FUNCTION_3       3  ''
              484  STORE_FAST               'wire'
            486_0  COME_FROM           446  '446'

 L. 620       486  LOAD_FAST                'rdtype'
              488  LOAD_GLOBAL              dns
              490  LOAD_ATTR                rdatatype
              492  LOAD_ATTR                IXFR
              494  COMPARE_OP               ==
              496  STORE_FAST               'is_ixfr'

 L. 621       498  LOAD_GLOBAL              dns
              500  LOAD_ATTR                message
              502  LOAD_ATTR                from_wire
              504  LOAD_FAST                'wire'
              506  LOAD_FAST                'q'
              508  LOAD_ATTR                keyring
              510  LOAD_FAST                'q'
              512  LOAD_ATTR                mac

 L. 622       514  LOAD_CONST               True

 L. 622       516  LOAD_FAST                'origin'

 L. 622       518  LOAD_FAST                'tsig_ctx'

 L. 623       520  LOAD_CONST               True

 L. 623       522  LOAD_FAST                'first'

 L. 624       524  LOAD_FAST                'is_ixfr'

 L. 621       526  LOAD_CONST               ('keyring', 'request_mac', 'xfr', 'origin', 'tsig_ctx', 'multi', 'first', 'one_rr_per_rrset')
              528  CALL_FUNCTION_KW_9     9  '9 total positional and keyword args'
              530  STORE_FAST               'r'

 L. 625       532  LOAD_FAST                'r'
              534  LOAD_METHOD              rcode
              536  CALL_METHOD_0         0  ''
              538  STORE_FAST               'rcode'

 L. 626       540  LOAD_FAST                'rcode'
              542  LOAD_GLOBAL              dns
              544  LOAD_ATTR                rcode
              546  LOAD_ATTR                NOERROR
              548  COMPARE_OP               !=
          550_552  POP_JUMP_IF_FALSE   562  'to 562'

 L. 627       554  LOAD_GLOBAL              TransferError
              556  LOAD_FAST                'rcode'
              558  CALL_FUNCTION_1       1  ''
              560  RAISE_VARARGS_1       1  'exception instance'
            562_0  COME_FROM           550  '550'

 L. 628       562  LOAD_FAST                'r'
              564  LOAD_ATTR                tsig_ctx
              566  STORE_FAST               'tsig_ctx'

 L. 629       568  LOAD_CONST               False
              570  STORE_FAST               'first'

 L. 630       572  LOAD_CONST               0
              574  STORE_FAST               'answer_index'

 L. 631       576  LOAD_FAST                'soa_rrset'
              578  LOAD_CONST               None
              580  COMPARE_OP               is
          582_584  POP_JUMP_IF_FALSE   714  'to 714'

 L. 632       586  LOAD_FAST                'r'
              588  LOAD_ATTR                answer
          590_592  POP_JUMP_IF_FALSE   612  'to 612'
              594  LOAD_FAST                'r'
              596  LOAD_ATTR                answer
              598  LOAD_CONST               0
              600  BINARY_SUBSCR    
              602  LOAD_ATTR                name
              604  LOAD_FAST                'oname'
              606  COMPARE_OP               !=
          608_610  POP_JUMP_IF_FALSE   624  'to 624'
            612_0  COME_FROM           590  '590'

 L. 633       612  LOAD_GLOBAL              dns
              614  LOAD_ATTR                exception
              616  LOAD_METHOD              FormError

 L. 634       618  LOAD_STR                 'No answer or RRset not for qname'

 L. 633       620  CALL_METHOD_1         1  ''
              622  RAISE_VARARGS_1       1  'exception instance'
            624_0  COME_FROM           608  '608'

 L. 635       624  LOAD_FAST                'r'
              626  LOAD_ATTR                answer
              628  LOAD_CONST               0
              630  BINARY_SUBSCR    
              632  STORE_FAST               'rrset'

 L. 636       634  LOAD_FAST                'rrset'
              636  LOAD_ATTR                rdtype
              638  LOAD_GLOBAL              dns
              640  LOAD_ATTR                rdatatype
              642  LOAD_ATTR                SOA
              644  COMPARE_OP               !=
          646_648  POP_JUMP_IF_FALSE   662  'to 662'

 L. 637       650  LOAD_GLOBAL              dns
              652  LOAD_ATTR                exception
              654  LOAD_METHOD              FormError
              656  LOAD_STR                 'first RRset is not an SOA'
              658  CALL_METHOD_1         1  ''
              660  RAISE_VARARGS_1       1  'exception instance'
            662_0  COME_FROM           646  '646'

 L. 638       662  LOAD_CONST               1
              664  STORE_FAST               'answer_index'

 L. 639       666  LOAD_FAST                'rrset'
              668  LOAD_METHOD              copy
              670  CALL_METHOD_0         0  ''
              672  STORE_FAST               'soa_rrset'

 L. 640       674  LOAD_FAST                'rdtype'
              676  LOAD_GLOBAL              dns
              678  LOAD_ATTR                rdatatype
              680  LOAD_ATTR                IXFR
              682  COMPARE_OP               ==
          684_686  POP_JUMP_IF_FALSE   714  'to 714'

 L. 641       688  LOAD_FAST                'soa_rrset'
              690  LOAD_CONST               0
              692  BINARY_SUBSCR    
              694  LOAD_ATTR                serial
              696  LOAD_FAST                'serial'
              698  COMPARE_OP               <=
          700_702  POP_JUMP_IF_FALSE   710  'to 710'

 L. 645       704  LOAD_CONST               True
              706  STORE_FAST               'done'
              708  JUMP_FORWARD        714  'to 714'
            710_0  COME_FROM           700  '700'

 L. 647       710  LOAD_CONST               True
              712  STORE_FAST               'expecting_SOA'
            714_0  COME_FROM           708  '708'
            714_1  COME_FROM           684  '684'
            714_2  COME_FROM           582  '582'

 L. 652       714  LOAD_FAST                'r'
              716  LOAD_ATTR                answer
              718  LOAD_FAST                'answer_index'
              720  LOAD_CONST               None
              722  BUILD_SLICE_2         2 
              724  BINARY_SUBSCR    
              726  GET_ITER         
            728_0  COME_FROM           906  '906'
            728_1  COME_FROM           890  '890'
            728_2  COME_FROM           886  '886'
              728  FOR_ITER            910  'to 910'
              730  STORE_FAST               'rrset'

 L. 653       732  LOAD_FAST                'done'
          734_736  POP_JUMP_IF_FALSE   750  'to 750'

 L. 654       738  LOAD_GLOBAL              dns
              740  LOAD_ATTR                exception
              742  LOAD_METHOD              FormError
              744  LOAD_STR                 'answers after final SOA'
              746  CALL_METHOD_1         1  ''
              748  RAISE_VARARGS_1       1  'exception instance'
            750_0  COME_FROM           734  '734'

 L. 655       750  LOAD_FAST                'rrset'
              752  LOAD_ATTR                rdtype
              754  LOAD_GLOBAL              dns
              756  LOAD_ATTR                rdatatype
              758  LOAD_ATTR                SOA
              760  COMPARE_OP               ==
          762_764  POP_JUMP_IF_FALSE   888  'to 888'
              766  LOAD_FAST                'rrset'
              768  LOAD_ATTR                name
              770  LOAD_FAST                'oname'
              772  COMPARE_OP               ==
          774_776  POP_JUMP_IF_FALSE   888  'to 888'

 L. 656       778  LOAD_FAST                'expecting_SOA'
          780_782  POP_JUMP_IF_FALSE   818  'to 818'

 L. 657       784  LOAD_FAST                'rrset'
              786  LOAD_CONST               0
              788  BINARY_SUBSCR    
              790  LOAD_ATTR                serial
              792  LOAD_FAST                'serial'
              794  COMPARE_OP               !=
          796_798  POP_JUMP_IF_FALSE   812  'to 812'

 L. 658       800  LOAD_GLOBAL              dns
              802  LOAD_ATTR                exception
              804  LOAD_METHOD              FormError

 L. 659       806  LOAD_STR                 'IXFR base serial mismatch'

 L. 658       808  CALL_METHOD_1         1  ''
              810  RAISE_VARARGS_1       1  'exception instance'
            812_0  COME_FROM           796  '796'

 L. 660       812  LOAD_CONST               False
              814  STORE_FAST               'expecting_SOA'
              816  JUMP_FORWARD        838  'to 838'
            818_0  COME_FROM           780  '780'

 L. 661       818  LOAD_FAST                'rdtype'
              820  LOAD_GLOBAL              dns
              822  LOAD_ATTR                rdatatype
              824  LOAD_ATTR                IXFR
              826  COMPARE_OP               ==
          828_830  POP_JUMP_IF_FALSE   838  'to 838'

 L. 662       832  LOAD_FAST                'delete_mode'
              834  UNARY_NOT        
              836  STORE_FAST               'delete_mode'
            838_0  COME_FROM           828  '828'
            838_1  COME_FROM           816  '816'

 L. 668       838  LOAD_FAST                'rrset'
              840  LOAD_FAST                'soa_rrset'
              842  COMPARE_OP               ==
          844_846  POP_JUMP_IF_FALSE   906  'to 906'

 L. 669       848  LOAD_FAST                'rdtype'
              850  LOAD_GLOBAL              dns
              852  LOAD_ATTR                rdatatype
              854  LOAD_ATTR                AXFR
              856  COMPARE_OP               ==

 L. 668   858_860  POP_JUMP_IF_TRUE    882  'to 882'

 L. 670       862  LOAD_FAST                'rdtype'
              864  LOAD_GLOBAL              dns
              866  LOAD_ATTR                rdatatype
              868  LOAD_ATTR                IXFR
              870  COMPARE_OP               ==

 L. 668   872_874  POP_JUMP_IF_FALSE   906  'to 906'

 L. 670       876  LOAD_FAST                'delete_mode'

 L. 668   878_880  POP_JUMP_IF_FALSE   906  'to 906'
            882_0  COME_FROM           858  '858'

 L. 671       882  LOAD_CONST               True
              884  STORE_FAST               'done'
              886  JUMP_BACK           728  'to 728'
            888_0  COME_FROM           774  '774'
            888_1  COME_FROM           762  '762'

 L. 672       888  LOAD_FAST                'expecting_SOA'
          890_892  POP_JUMP_IF_FALSE_BACK   728  'to 728'

 L. 678       894  LOAD_GLOBAL              dns
              896  LOAD_ATTR                rdatatype
              898  LOAD_ATTR                AXFR
              900  STORE_FAST               'rdtype'

 L. 679       902  LOAD_CONST               False
              904  STORE_FAST               'expecting_SOA'
            906_0  COME_FROM           878  '878'
            906_1  COME_FROM           872  '872'
            906_2  COME_FROM           844  '844'
          906_908  JUMP_BACK           728  'to 728'
            910_0  COME_FROM           728  '728'

 L. 680       910  LOAD_FAST                'done'
          912_914  POP_JUMP_IF_FALSE   944  'to 944'
              916  LOAD_FAST                'q'
              918  LOAD_ATTR                keyring
          920_922  POP_JUMP_IF_FALSE   944  'to 944'
              924  LOAD_FAST                'r'
              926  LOAD_ATTR                had_tsig
          928_930  POP_JUMP_IF_TRUE    944  'to 944'

 L. 681       932  LOAD_GLOBAL              dns
              934  LOAD_ATTR                exception
              936  LOAD_METHOD              FormError
              938  LOAD_STR                 'missing TSIG'
              940  CALL_METHOD_1         1  ''
              942  RAISE_VARARGS_1       1  'exception instance'
            944_0  COME_FROM           928  '928'
            944_1  COME_FROM           920  '920'
            944_2  COME_FROM           912  '912'

 L. 682       944  LOAD_FAST                'r'
              946  YIELD_VALUE      
              948  POP_TOP          
          950_952  JUMP_BACK           378  'to 378'
            954_0  COME_FROM           380  '380'

 L. 683       954  LOAD_FAST                's'
              956  LOAD_METHOD              close
              958  CALL_METHOD_0         0  ''
              960  POP_TOP          

Parse error at or near `JUMP_BACK' instruction at offset 906_908