# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
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
    else:
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
    else:
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
    while not done:
        if expiration is None:
            timeout = None
        else:
            timeout = expiration - time.time()
            if timeout <= 0.0:
                raise dns.exception.Timeout
            else:
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
        else:
            if af == dns.inet.AF_INET:
                destination = (
                 where, port)
                if source is not None or source_port != 0:
                    if source is None:
                        source = '0.0.0.0'
                    source = (
                     source, source_port)
    else:
        if af == dns.inet.AF_INET6:
            destination = (
             where, port, 0, 0)
            if source is not None or source_port != 0:
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
    return (n, sent_time)


def receive_udp--- This code section failed: ---

 L. 256         0  LOAD_CONST               b''
                2  STORE_FAST               'wire'
              4_0  COME_FROM            86  '86'

 L. 258         4  LOAD_GLOBAL              _wait_for_readable
                6  LOAD_FAST                'sock'
                8  LOAD_FAST                'expiration'
               10  CALL_FUNCTION_2       2  ''
               12  POP_TOP          

 L. 259        14  LOAD_FAST                'sock'
               16  LOAD_METHOD              recvfrom
               18  LOAD_CONST               65535
               20  CALL_METHOD_1         1  ''
               22  UNPACK_SEQUENCE_2     2 
               24  STORE_FAST               'wire'
               26  STORE_FAST               'from_address'

 L. 260        28  LOAD_GLOBAL              _addresses_equal
               30  LOAD_FAST                'sock'
               32  LOAD_ATTR                family
               34  LOAD_FAST                'from_address'
               36  LOAD_FAST                'destination'
               38  CALL_FUNCTION_3       3  ''
               40  POP_JUMP_IF_TRUE    106  'to 106'

 L. 261        42  LOAD_GLOBAL              dns
               44  LOAD_ATTR                inet
               46  LOAD_METHOD              is_multicast
               48  LOAD_FAST                'destination'
               50  LOAD_CONST               0
               52  BINARY_SUBSCR    
               54  CALL_METHOD_1         1  ''

 L. 260        56  POP_JUMP_IF_FALSE    84  'to 84'

 L. 262        58  LOAD_FAST                'from_address'
               60  LOAD_CONST               1
               62  LOAD_CONST               None
               64  BUILD_SLICE_2         2 
               66  BINARY_SUBSCR    
               68  LOAD_FAST                'destination'
               70  LOAD_CONST               1
               72  LOAD_CONST               None
               74  BUILD_SLICE_2         2 
               76  BINARY_SUBSCR    
               78  COMPARE_OP               ==

 L. 260        80  POP_JUMP_IF_FALSE    84  'to 84'

 L. 263        82  BREAK_LOOP          106  'to 106'
             84_0  COME_FROM            80  '80'
             84_1  COME_FROM            56  '56'

 L. 264        84  LOAD_FAST                'ignore_unexpected'
               86  POP_JUMP_IF_TRUE      4  'to 4'

 L. 265        88  LOAD_GLOBAL              UnexpectedSource
               90  LOAD_STR                 'got a response from %s instead of %s'

 L. 266        92  LOAD_FAST                'from_address'

 L. 267        94  LOAD_FAST                'destination'

 L. 266        96  BUILD_TUPLE_2         2 

 L. 265        98  BINARY_MODULO    
              100  CALL_FUNCTION_1       1  ''
              102  RAISE_VARARGS_1       1  'exception instance'
              104  JUMP_BACK             4  'to 4'
            106_0  COME_FROM            40  '40'

 L. 268       106  LOAD_GLOBAL              time
              108  LOAD_METHOD              time
              110  CALL_METHOD_0         0  ''
              112  STORE_FAST               'received_time'

 L. 269       114  LOAD_GLOBAL              dns
              116  LOAD_ATTR                message
              118  LOAD_ATTR                from_wire
              120  LOAD_FAST                'wire'
              122  LOAD_FAST                'keyring'
              124  LOAD_FAST                'request_mac'

 L. 270       126  LOAD_FAST                'one_rr_per_rrset'

 L. 271       128  LOAD_FAST                'ignore_trailing'

 L. 269       130  LOAD_CONST               ('keyring', 'request_mac', 'one_rr_per_rrset', 'ignore_trailing')
              132  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              134  STORE_FAST               'r'

 L. 272       136  LOAD_FAST                'r'
              138  LOAD_FAST                'received_time'
              140  BUILD_TUPLE_2         2 
              142  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 142


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
    while count > 0:
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
    while current < l:
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
    return (len(tcpmsg), sent_time)


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
    return (r, received_time)


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


def xfr(where, zone, rdtype=dns.rdatatype.AXFR, rdclass=dns.rdataclass.IN, timeout=None, port=53, keyring=None, keyname=None, relativize=True, af=None, lifetime=None, source=None, source_port=0, serial=0, use_udp=False, keyalgorithm=dns.tsig.default_algorithm):
    """Return a generator for the responses to a zone transfer.

    *where*.  If the inference attempt fails, AF_INET is used.  This
    parameter is historical; you need never set it.

    *zone*, a ``dns.name.Name`` or ``text``, the name of the zone to transfer.

    *rdtype*, an ``int`` or ``text``, the type of zone transfer.  The
    default is ``dns.rdatatype.AXFR``.  ``dns.rdatatype.IXFR`` can be
    used to do an incremental transfer instead.

    *rdclass*, an ``int`` or ``text``, the class of the zone transfer.
    The default is ``dns.rdataclass.IN``.

    *timeout*, a ``float``, the number of seconds to wait for each
    response message.  If None, the default, wait forever.

    *port*, an ``int``, the port send the message to.  The default is 53.

    *keyring*, a ``dict``, the keyring to use for TSIG.

    *keyname*, a ``dns.name.Name`` or ``text``, the name of the TSIG
    key to use.

    *relativize*, a ``bool``.  If ``True``, all names in the zone will be
    relativized to the zone origin.  It is essential that the
    relativize setting matches the one specified to
    ``dns.zone.from_xfr()`` if using this generator to make a zone.

    *af*, an ``int``, the address family to use.  The default is ``None``,
    which causes the address family to use to be inferred from the form of
    *where*.  If the inference attempt fails, AF_INET is used.  This
    parameter is historical; you need never set it.

    *lifetime*, a ``float``, the total number of seconds to spend
    doing the transfer.  If ``None``, the default, then there is no
    limit on the time the transfer may take.

    *source*, a ``text`` containing an IPv4 or IPv6 address, specifying
    the source address.  The default is the wildcard address.

    *source_port*, an ``int``, the port from which to send the message.
    The default is 0.

    *serial*, an ``int``, the SOA serial number to use as the base for
    an IXFR diff sequence (only meaningful if *rdtype* is
    ``dns.rdatatype.IXFR``).

    *use_udp*, a ``bool``.  If ``True``, use UDP (only meaningful for IXFR).

    *keyalgorithm*, a ``dns.name.Name`` or ``text``, the TSIG algorithm to use.

    Raises on errors, and so does the generator.

    Returns a generator of ``dns.message.Message`` objects.
    """
    if isinstance(zone, string_types):
        zone = dns.name.from_text(zone)
    else:
        if isinstance(rdtype, string_types):
            rdtype = dns.rdatatype.from_text(rdtype)
        else:
            q = dns.message.make_query(zone, rdtype, rdclass)
            if rdtype == dns.rdatatype.IXFR:
                rrset = dns.rrset.from_text(zone, 0, 'IN', 'SOA', '. . %u 0 0 0 0' % serial)
                q.authority.append(rrset)
            else:
                if keyring is not None:
                    q.use_tsig(keyring, keyname, algorithm=keyalgorithm)
                else:
                    wire = q.to_wire()
                    af, destination, source = _destination_and_source(af, where, port, source, source_port)
                    if use_udp:
                        if rdtype != dns.rdatatype.IXFR:
                            raise ValueError('cannot do a UDP AXFR')
                        s = socket_factory(af, socket.SOCK_DGRAM, 0)
                    else:
                        s = socket_factory(af, socket.SOCK_STREAM, 0)
                s.setblocking(0)
                if source is not None:
                    s.bind(source)
                expiration = _compute_expiration(lifetime)
                _connect(s, destination)
                l = len(wire)
                if use_udp:
                    _wait_for_writable(s, expiration)
                    s.send(wire)
                else:
                    tcpmsg = struct.pack('!H', l) + wire
                _net_write(s, tcpmsg, expiration)
            done = False
            delete_mode = True
            expecting_SOA = False
            soa_rrset = None
            if relativize:
                origin = zone
                oname = dns.name.empty
            else:
                origin = None
            oname = zone
        tsig_ctx = None
        first = True
        while True:
            mexpiration = done or _compute_expiration(timeout)
            if not mexpiration is None:
                if mexpiration > expiration:
                    mexpiration = expiration
                if use_udp:
                    _wait_for_readable(s, expiration)
                    wire, from_address = s.recvfrom(65535)
                else:
                    ldata = _net_read(s, 2, mexpiration)
                    l, = struct.unpack('!H', ldata)
                    wire = _net_read(s, l, mexpiration)
                is_ixfr = rdtype == dns.rdatatype.IXFR
                r = dns.message.from_wire(wire, keyring=(q.keyring), request_mac=(q.mac), xfr=True,
                  origin=origin,
                  tsig_ctx=tsig_ctx,
                  multi=True,
                  first=first,
                  one_rr_per_rrset=is_ixfr)
                rcode = r.rcode()
                if rcode != dns.rcode.NOERROR:
                    raise TransferError(rcode)
                tsig_ctx = r.tsig_ctx
                first = False
                answer_index = 0
                if soa_rrset is None:
                    if r.answer:
                        if r.answer[0].name != oname:
                            raise dns.exception.FormError('No answer or RRset not for qname')
                        rrset = r.answer[0]
                        if rrset.rdtype != dns.rdatatype.SOA:
                            raise dns.exception.FormError('first RRset is not an SOA')
                        answer_index = 1
                        soa_rrset = rrset.copy()
                        if rdtype == dns.rdatatype.IXFR:
                            if soa_rrset[0].serial <= serial:
                                done = True
                    else:
                        expecting_SOA = True
                for rrset in r.answer[answer_index:]:
                    if done:
                        raise dns.exception.FormError('answers after final SOA')
                    if rrset.rdtype == dns.rdatatype.SOA and rrset.name == oname:
                        if expecting_SOA:
                            if rrset[0].serial != serial:
                                raise dns.exception.FormError('IXFR base serial mismatch')
                            expecting_SOA = False
                        else:
                            if rdtype == dns.rdatatype.IXFR:
                                delete_mode = not delete_mode
                        if rrset == soa_rrset and not rdtype == dns.rdatatype.AXFR:
                            if not rdtype == dns.rdatatype.IXFR or delete_mode:
                                done = True
                    elif expecting_SOA:
                        rdtype = dns.rdatatype.AXFR
                        expecting_SOA = False

            else:
                if done:
                    if q.keyring:
                        if not r.had_tsig:
                            raise dns.exception.FormError('missing TSIG')
                (yield r)

    s.close()