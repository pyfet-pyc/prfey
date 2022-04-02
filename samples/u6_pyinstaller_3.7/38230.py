# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\paramiko\kex_gss.py
"""
This module provides GSS-API / SSPI Key Exchange as defined in :rfc:`4462`.

.. note:: Credential delegation is not supported in server mode.

.. note::
    `RFC 4462 Section 2.2
    <https://tools.ietf.org/html/rfc4462.html#section-2.2>`_ says we are not
    required to implement GSS-API error messages. Thus, in many methods within
    this module, if an error occurs an exception will be thrown and the
    connection will be terminated.

.. seealso:: :doc:`/api/ssh_gss`

.. versionadded:: 1.15
"""
import os
from hashlib import sha1
from paramiko.common import DEBUG, max_byte, zero_byte
from paramiko import util
from paramiko.message import Message
from paramiko.py3compat import byte_chr, byte_mask, byte_ord
from paramiko.ssh_exception import SSHException
MSG_KEXGSS_INIT, MSG_KEXGSS_CONTINUE, MSG_KEXGSS_COMPLETE, MSG_KEXGSS_HOSTKEY, MSG_KEXGSS_ERROR = range(30, 35)
MSG_KEXGSS_GROUPREQ, MSG_KEXGSS_GROUP = range(40, 42)
c_MSG_KEXGSS_INIT, c_MSG_KEXGSS_CONTINUE, c_MSG_KEXGSS_COMPLETE, c_MSG_KEXGSS_HOSTKEY, c_MSG_KEXGSS_ERROR = [byte_chr(c) for c in range(30, 35)]
c_MSG_KEXGSS_GROUPREQ, c_MSG_KEXGSS_GROUP = [byte_chr(c) for c in range(40, 42)]

class KexGSSGroup1(object):
    __doc__ = '\n    GSS-API / SSPI Authenticated Diffie-Hellman Key Exchange as defined in `RFC\n    4462 Section 2 <https://tools.ietf.org/html/rfc4462.html#section-2>`_\n    '
    P = 179769313486231590770839156793787453197860296048756011706444423684197180216158519368947833795864925541502180565485980503646440548199239100050792877003355816639229553136239076508735759914822574862575007425302077447712589550957937778424442426617334727629299387668709205606050270810842907692932019128194467627007
    G = 2
    b7fffffffffffffff = byte_chr(127) + max_byte * 7
    b0000000000000000 = zero_byte * 8
    NAME = 'gss-group1-sha1-toWM5Slw5Ew8Mqkay+al2g=='

    def __init__(self, transport):
        self.transport = transport
        self.kexgss = self.transport.kexgss_ctxt
        self.gss_host = None
        self.x = 0
        self.e = 0
        self.f = 0

    def start_kex(self):
        """
        Start the GSS-API / SSPI Authenticated Diffie-Hellman Key Exchange.
        """
        self._generate_x()
        if self.transport.server_mode:
            self.f = pow(self.G, self.x, self.P)
            self.transport._expect_packet(MSG_KEXGSS_INIT)
            return
        self.e = pow(self.G, self.x, self.P)
        self.gss_host = self.transport.gss_host
        m = Message()
        m.add_byte(c_MSG_KEXGSS_INIT)
        m.add_string(self.kexgss.ssh_init_sec_context(target=(self.gss_host)))
        m.add_mpint(self.e)
        self.transport._send_message(m)
        self.transport._expect_packet(MSG_KEXGSS_HOSTKEY, MSG_KEXGSS_CONTINUE, MSG_KEXGSS_COMPLETE, MSG_KEXGSS_ERROR)

    def parse_next(self, ptype, m):
        """
        Parse the next packet.

        :param ptype: The (string) type of the incoming packet
        :param `.Message` m: The paket content
        """
        if self.transport.server_mode:
            if ptype == MSG_KEXGSS_INIT:
                return self._parse_kexgss_init(m)
        else:
            if not self.transport.server_mode:
                if ptype == MSG_KEXGSS_HOSTKEY:
                    return self._parse_kexgss_hostkey(m)
            if self.transport.server_mode:
                if ptype == MSG_KEXGSS_CONTINUE:
                    return self._parse_kexgss_continue(m)
            if not self.transport.server_mode:
                if ptype == MSG_KEXGSS_COMPLETE:
                    return self._parse_kexgss_complete(m)
        if ptype == MSG_KEXGSS_ERROR:
            return self._parse_kexgss_error(m)
        msg = 'GSS KexGroup1 asked to handle packet type {:d}'
        raise SSHException(msg.format(ptype))

    def _generate_x(self):
        """
        generate an "x" (1 < x < q), where q is (p-1)/2.
        p is a 128-byte (1024-bit) number, where the first 64 bits are 1.
        therefore q can be approximated as a 2^1023.  we drop the subset of
        potential x where the first 63 bits are 1, because some of those will
        be larger than q (but this is a tiny tiny subset of potential x).
        """
        while 1:
            x_bytes = os.urandom(128)
            x_bytes = byte_mask(x_bytes[0], 127) + x_bytes[1:]
            first = x_bytes[:8]
            if first not in (self.b7fffffffffffffff, self.b0000000000000000):
                break

        self.x = util.inflate_long(x_bytes)

    def _parse_kexgss_hostkey(self, m):
        """
        Parse the SSH2_MSG_KEXGSS_HOSTKEY message (client mode).

        :param `.Message` m: The content of the SSH2_MSG_KEXGSS_HOSTKEY message
        """
        host_key = m.get_string()
        self.transport.host_key = host_key
        sig = m.get_string()
        self.transport._verify_key(host_key, sig)
        self.transport._expect_packet(MSG_KEXGSS_CONTINUE, MSG_KEXGSS_COMPLETE)

    def _parse_kexgss_continue--- This code section failed: ---

 L. 175         0  LOAD_FAST                'self'
                2  LOAD_ATTR                transport
                4  LOAD_ATTR                server_mode
                6  POP_JUMP_IF_TRUE     86  'to 86'

 L. 176         8  LOAD_FAST                'm'
               10  LOAD_METHOD              get_string
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  STORE_FAST               'srv_token'

 L. 177        16  LOAD_GLOBAL              Message
               18  CALL_FUNCTION_0       0  '0 positional arguments'
               20  STORE_FAST               'm'

 L. 178        22  LOAD_FAST                'm'
               24  LOAD_METHOD              add_byte
               26  LOAD_GLOBAL              c_MSG_KEXGSS_CONTINUE
               28  CALL_METHOD_1         1  '1 positional argument'
               30  POP_TOP          

 L. 179        32  LOAD_FAST                'm'
               34  LOAD_METHOD              add_string

 L. 180        36  LOAD_FAST                'self'
               38  LOAD_ATTR                kexgss
               40  LOAD_ATTR                ssh_init_sec_context

 L. 181        42  LOAD_FAST                'self'
               44  LOAD_ATTR                gss_host
               46  LOAD_FAST                'srv_token'
               48  LOAD_CONST               ('target', 'recv_token')
               50  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               52  CALL_METHOD_1         1  '1 positional argument'
               54  POP_TOP          

 L. 184        56  LOAD_FAST                'self'
               58  LOAD_ATTR                transport
               60  LOAD_METHOD              send_message
               62  LOAD_FAST                'm'
               64  CALL_METHOD_1         1  '1 positional argument'
               66  POP_TOP          

 L. 185        68  LOAD_FAST                'self'
               70  LOAD_ATTR                transport
               72  LOAD_METHOD              _expect_packet

 L. 186        74  LOAD_GLOBAL              MSG_KEXGSS_CONTINUE
               76  LOAD_GLOBAL              MSG_KEXGSS_COMPLETE
               78  LOAD_GLOBAL              MSG_KEXGSS_ERROR
               80  CALL_METHOD_3         3  '3 positional arguments'
               82  POP_TOP          
               84  JUMP_FORWARD         86  'to 86'
             86_0  COME_FROM            84  '84'
             86_1  COME_FROM             6  '6'

Parse error at or near `COME_FROM' instruction at offset 86_0

    def _parse_kexgss_complete(self, m):
        """
        Parse the SSH2_MSG_KEXGSS_COMPLETE message (client mode).

        :param `.Message` m: The content of the
            SSH2_MSG_KEXGSS_COMPLETE message
        """
        if self.transport.host_key is None:
            self.transport.host_key = NullHostKey()
        else:
            self.f = m.get_mpint()
            if not self.f < 1:
                if self.f > self.P - 1:
                    raise SSHException('Server kex "f" is out of range')
                mic_token = m.get_string()
                bool = m.get_boolean()
                srv_token = None
                if bool:
                    srv_token = m.get_string()
                K = pow(self.f, self.x, self.P)
                hm = Message()
                hm.add(self.transport.local_version, self.transport.remote_version, self.transport.local_kex_init, self.transport.remote_kex_init)
                hm.add_string(self.transport.host_key.__str__())
                hm.add_mpint(self.e)
                hm.add_mpint(self.f)
                hm.add_mpint(K)
                H = sha1(str(hm)).digest()
                self.transport._set_K_H(K, H)
                if srv_token is not None:
                    self.kexgss.ssh_init_sec_context(target=(self.gss_host),
                      recv_token=srv_token)
                    self.kexgss.ssh_check_mic(mic_token, H)
            else:
                self.kexgss.ssh_check_mic(mic_token, H)
        self.transport.gss_kex_used = True
        self.transport._activate_outbound()

    def _parse_kexgss_init(self, m):
        """
        Parse the SSH2_MSG_KEXGSS_INIT message (server mode).

        :param `.Message` m: The content of the SSH2_MSG_KEXGSS_INIT message
        """
        client_token = m.get_string()
        self.e = m.get_mpint()
        if self.e < 1 or self.e > self.P - 1:
            raise SSHException('Client kex "e" is out of range')
        K = pow(self.e, self.x, self.P)
        self.transport.host_key = NullHostKey()
        key = self.transport.host_key.__str__()
        hm = Message()
        hm.add(self.transport.remote_version, self.transport.local_version, self.transport.remote_kex_init, self.transport.local_kex_init)
        hm.add_string(key)
        hm.add_mpint(self.e)
        hm.add_mpint(self.f)
        hm.add_mpint(K)
        H = sha1(hm.asbytes()).digest()
        self.transport._set_K_H(K, H)
        srv_token = self.kexgss.ssh_accept_sec_context(self.gss_host, client_token)
        m = Message()
        if self.kexgss._gss_srv_ctxt_status:
            mic_token = self.kexgss.ssh_get_mic((self.transport.session_id),
              gss_kex=True)
            m.add_byte(c_MSG_KEXGSS_COMPLETE)
            m.add_mpint(self.f)
            m.add_string(mic_token)
            if srv_token is not None:
                m.add_boolean(True)
                m.add_string(srv_token)
            else:
                m.add_boolean(False)
            self.transport._send_message(m)
            self.transport.gss_kex_used = True
            self.transport._activate_outbound()
        else:
            m.add_byte(c_MSG_KEXGSS_CONTINUE)
            m.add_string(srv_token)
            self.transport._send_message(m)
            self.transport._expect_packetMSG_KEXGSS_CONTINUEMSG_KEXGSS_COMPLETEMSG_KEXGSS_ERROR

    def _parse_kexgss_error(self, m):
        """
        Parse the SSH2_MSG_KEXGSS_ERROR message (client mode).
        The server may send a GSS-API error message. if it does, we display
        the error by throwing an exception (client mode).

        :param `.Message` m: The content of the SSH2_MSG_KEXGSS_ERROR message
        :raise SSHException: Contains GSS-API major and minor status as well as
                             the error message and the language tag of the
                             message
        """
        maj_status = m.get_int()
        min_status = m.get_int()
        err_msg = m.get_string()
        m.get_string()
        raise SSHException('GSS-API Error:\nMajor Status: {}\nMinor Status: {}\nError Message: {}\n'.formatmaj_statusmin_statuserr_msg)


class KexGSSGroup14(KexGSSGroup1):
    __doc__ = '\n    GSS-API / SSPI Authenticated Diffie-Hellman Group14 Key Exchange as defined\n    in `RFC 4462 Section 2\n    <https://tools.ietf.org/html/rfc4462.html#section-2>`_\n    '
    P = 32317006071311007300338913926423828248817941241140239112842009751400741706634354222619689417363569347117901737909704191754605873209195028853758986185622153212175412514901774520270235796078236248884246189477587641105928646099411723245426622522193230540919037680524235519125679715870117001058055877651038861847280257976054903569732561526167081339361799541336476559160368317896729073178384589680639671900977202194168647225871031411336429319536193471636533209717077448227988588565369208645296636077250268955505928362751121174096972998068410554359584866583291642136218231078990999448652468262416972035911852507045361090559
    G = 2
    NAME = 'gss-group14-sha1-toWM5Slw5Ew8Mqkay+al2g=='


class KexGSSGex(object):
    __doc__ = '\n    GSS-API / SSPI Authenticated Diffie-Hellman Group Exchange as defined in\n    `RFC 4462 Section 2 <https://tools.ietf.org/html/rfc4462.html#section-2>`_\n    '
    NAME = 'gss-gex-sha1-toWM5Slw5Ew8Mqkay+al2g=='
    min_bits = 1024
    max_bits = 8192
    preferred_bits = 2048

    def __init__(self, transport):
        self.transport = transport
        self.kexgss = self.transport.kexgss_ctxt
        self.gss_host = None
        self.p = None
        self.q = None
        self.g = None
        self.x = None
        self.e = None
        self.f = None
        self.old_style = False

    def start_kex(self):
        """
        Start the GSS-API / SSPI Authenticated Diffie-Hellman Group Exchange
        """
        if self.transport.server_mode:
            self.transport._expect_packet(MSG_KEXGSS_GROUPREQ)
            return
        self.gss_host = self.transport.gss_host
        m = Message()
        m.add_byte(c_MSG_KEXGSS_GROUPREQ)
        m.add_int(self.min_bits)
        m.add_int(self.preferred_bits)
        m.add_int(self.max_bits)
        self.transport._send_message(m)
        self.transport._expect_packet(MSG_KEXGSS_GROUP)

    def parse_next(self, ptype, m):
        """
        Parse the next packet.

        :param ptype: The (string) type of the incoming packet
        :param `.Message` m: The paket content
        """
        if ptype == MSG_KEXGSS_GROUPREQ:
            return self._parse_kexgss_groupreq(m)
        if ptype == MSG_KEXGSS_GROUP:
            return self._parse_kexgss_group(m)
        if ptype == MSG_KEXGSS_INIT:
            return self._parse_kexgss_gex_init(m)
        if ptype == MSG_KEXGSS_HOSTKEY:
            return self._parse_kexgss_hostkey(m)
        if ptype == MSG_KEXGSS_CONTINUE:
            return self._parse_kexgss_continue(m)
        if ptype == MSG_KEXGSS_COMPLETE:
            return self._parse_kexgss_complete(m)
        if ptype == MSG_KEXGSS_ERROR:
            return self._parse_kexgss_error(m)
        msg = 'KexGex asked to handle packet type {:d}'
        raise SSHException(msg.format(ptype))

    def _generate_x(self):
        q = (self.p - 1) // 2
        qnorm = util.deflate_long(q, 0)
        qhbyte = byte_ord(qnorm[0])
        byte_count = len(qnorm)
        qmask = 255
        while not qhbyte & 128:
            qhbyte <<= 1
            qmask >>= 1

        while 1:
            x_bytes = os.urandom(byte_count)
            x_bytes = byte_mask(x_bytes[0], qmask) + x_bytes[1:]
            x = util.inflate_long(x_bytes, 1)
            if x > 1 and x < q:
                break

        self.x = x

    def _parse_kexgss_groupreq(self, m):
        """
        Parse the SSH2_MSG_KEXGSS_GROUPREQ message (server mode).

        :param `.Message` m: The content of the
            SSH2_MSG_KEXGSS_GROUPREQ message
        """
        minbits = m.get_int()
        preferredbits = m.get_int()
        maxbits = m.get_int()
        if preferredbits > self.max_bits:
            preferredbits = self.max_bits
        if preferredbits < self.min_bits:
            preferredbits = self.min_bits
        if minbits > preferredbits:
            minbits = preferredbits
        if maxbits < preferredbits:
            maxbits = preferredbits
        self.min_bits = minbits
        self.preferred_bits = preferredbits
        self.max_bits = maxbits
        pack = self.transport._get_modulus_pack()
        if pack is None:
            raise SSHException("Can't do server-side gex with no modulus pack")
        self.transport._log(DEBUG, 'Picking p ({} <= {} <= {} bits)'.formatminbitspreferredbitsmaxbits)
        self.g, self.p = pack.get_modulusminbitspreferredbitsmaxbits
        m = Message()
        m.add_byte(c_MSG_KEXGSS_GROUP)
        m.add_mpint(self.p)
        m.add_mpint(self.g)
        self.transport._send_message(m)
        self.transport._expect_packet(MSG_KEXGSS_INIT)

    def _parse_kexgss_group(self, m):
        """
        Parse the SSH2_MSG_KEXGSS_GROUP message (client mode).

        :param `Message` m: The content of the SSH2_MSG_KEXGSS_GROUP message
        """
        self.p = m.get_mpint()
        self.g = m.get_mpint()
        bitlen = util.bit_length(self.p)
        if bitlen < 1024 or bitlen > 8192:
            raise SSHException("Server-generated gex p (don't ask) is out of range ({} bits)".format(bitlen))
        self.transport._log(DEBUG, 'Got server p ({} bits)'.format(bitlen))
        self._generate_x()
        self.e = pow(self.g, self.x, self.p)
        m = Message()
        m.add_byte(c_MSG_KEXGSS_INIT)
        m.add_string(self.kexgss.ssh_init_sec_context(target=(self.gss_host)))
        m.add_mpint(self.e)
        self.transport._send_message(m)
        self.transport._expect_packet(MSG_KEXGSS_HOSTKEY, MSG_KEXGSS_CONTINUE, MSG_KEXGSS_COMPLETE, MSG_KEXGSS_ERROR)

    def _parse_kexgss_gex_init(self, m):
        """
        Parse the SSH2_MSG_KEXGSS_INIT message (server mode).

        :param `Message` m: The content of the SSH2_MSG_KEXGSS_INIT message
        """
        client_token = m.get_string()
        self.e = m.get_mpint()
        if self.e < 1 or self.e > self.p - 1:
            raise SSHException('Client kex "e" is out of range')
        self._generate_x()
        self.f = pow(self.g, self.x, self.p)
        K = pow(self.e, self.x, self.p)
        self.transport.host_key = NullHostKey()
        key = self.transport.host_key.__str__()
        hm = Message()
        hm.add(self.transport.remote_version, self.transport.local_version, self.transport.remote_kex_init, self.transport.local_kex_init, key)
        hm.add_int(self.min_bits)
        hm.add_int(self.preferred_bits)
        hm.add_int(self.max_bits)
        hm.add_mpint(self.p)
        hm.add_mpint(self.g)
        hm.add_mpint(self.e)
        hm.add_mpint(self.f)
        hm.add_mpint(K)
        H = sha1(hm.asbytes()).digest()
        self.transport._set_K_H(K, H)
        srv_token = self.kexgss.ssh_accept_sec_context(self.gss_host, client_token)
        m = Message()
        if self.kexgss._gss_srv_ctxt_status:
            mic_token = self.kexgss.ssh_get_mic((self.transport.session_id),
              gss_kex=True)
            m.add_byte(c_MSG_KEXGSS_COMPLETE)
            m.add_mpint(self.f)
            m.add_string(mic_token)
            if srv_token is not None:
                m.add_boolean(True)
                m.add_string(srv_token)
            else:
                m.add_boolean(False)
            self.transport._send_message(m)
            self.transport.gss_kex_used = True
            self.transport._activate_outbound()
        else:
            m.add_byte(c_MSG_KEXGSS_CONTINUE)
            m.add_string(srv_token)
            self.transport._send_message(m)
            self.transport._expect_packetMSG_KEXGSS_CONTINUEMSG_KEXGSS_COMPLETEMSG_KEXGSS_ERROR

    def _parse_kexgss_hostkey(self, m):
        """
        Parse the SSH2_MSG_KEXGSS_HOSTKEY message (client mode).

        :param `Message` m: The content of the SSH2_MSG_KEXGSS_HOSTKEY message
        """
        host_key = m.get_string()
        self.transport.host_key = host_key
        sig = m.get_string()
        self.transport._verify_key(host_key, sig)
        self.transport._expect_packet(MSG_KEXGSS_CONTINUE, MSG_KEXGSS_COMPLETE)

    def _parse_kexgss_continue--- This code section failed: ---

 L. 574         0  LOAD_FAST                'self'
                2  LOAD_ATTR                transport
                4  LOAD_ATTR                server_mode
                6  POP_JUMP_IF_TRUE     86  'to 86'

 L. 575         8  LOAD_FAST                'm'
               10  LOAD_METHOD              get_string
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  STORE_FAST               'srv_token'

 L. 576        16  LOAD_GLOBAL              Message
               18  CALL_FUNCTION_0       0  '0 positional arguments'
               20  STORE_FAST               'm'

 L. 577        22  LOAD_FAST                'm'
               24  LOAD_METHOD              add_byte
               26  LOAD_GLOBAL              c_MSG_KEXGSS_CONTINUE
               28  CALL_METHOD_1         1  '1 positional argument'
               30  POP_TOP          

 L. 578        32  LOAD_FAST                'm'
               34  LOAD_METHOD              add_string

 L. 579        36  LOAD_FAST                'self'
               38  LOAD_ATTR                kexgss
               40  LOAD_ATTR                ssh_init_sec_context

 L. 580        42  LOAD_FAST                'self'
               44  LOAD_ATTR                gss_host
               46  LOAD_FAST                'srv_token'
               48  LOAD_CONST               ('target', 'recv_token')
               50  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               52  CALL_METHOD_1         1  '1 positional argument'
               54  POP_TOP          

 L. 583        56  LOAD_FAST                'self'
               58  LOAD_ATTR                transport
               60  LOAD_METHOD              send_message
               62  LOAD_FAST                'm'
               64  CALL_METHOD_1         1  '1 positional argument'
               66  POP_TOP          

 L. 584        68  LOAD_FAST                'self'
               70  LOAD_ATTR                transport
               72  LOAD_METHOD              _expect_packet

 L. 585        74  LOAD_GLOBAL              MSG_KEXGSS_CONTINUE
               76  LOAD_GLOBAL              MSG_KEXGSS_COMPLETE
               78  LOAD_GLOBAL              MSG_KEXGSS_ERROR
               80  CALL_METHOD_3         3  '3 positional arguments'
               82  POP_TOP          
               84  JUMP_FORWARD         86  'to 86'
             86_0  COME_FROM            84  '84'
             86_1  COME_FROM             6  '6'

Parse error at or near `COME_FROM' instruction at offset 86_0

    def _parse_kexgss_complete(self, m):
        """
        Parse the SSH2_MSG_KEXGSS_COMPLETE message (client mode).

        :param `Message` m: The content of the SSH2_MSG_KEXGSS_COMPLETE message
        """
        if self.transport.host_key is None:
            self.transport.host_key = NullHostKey()
        else:
            self.f = m.get_mpint()
            mic_token = m.get_string()
            bool = m.get_boolean()
            srv_token = None
            if bool:
                srv_token = m.get_string()
            if not self.f < 1:
                if self.f > self.p - 1:
                    raise SSHException('Server kex "f" is out of range')
                K = pow(self.f, self.x, self.p)
                hm = Message()
                hm.add(self.transport.local_version, self.transport.remote_version, self.transport.local_kex_init, self.transport.remote_kex_init, self.transport.host_key.__str__())
                if not self.old_style:
                    hm.add_int(self.min_bits)
                hm.add_int(self.preferred_bits)
                if not self.old_style:
                    hm.add_int(self.max_bits)
                hm.add_mpint(self.p)
                hm.add_mpint(self.g)
                hm.add_mpint(self.e)
                hm.add_mpint(self.f)
                hm.add_mpint(K)
                H = sha1(hm.asbytes()).digest()
                self.transport._set_K_H(K, H)
                if srv_token is not None:
                    self.kexgss.ssh_init_sec_context(target=(self.gss_host),
                      recv_token=srv_token)
                    self.kexgss.ssh_check_mic(mic_token, H)
            else:
                self.kexgss.ssh_check_mic(mic_token, H)
        self.transport.gss_kex_used = True
        self.transport._activate_outbound()

    def _parse_kexgss_error(self, m):
        """
        Parse the SSH2_MSG_KEXGSS_ERROR message (client mode).
        The server may send a GSS-API error message. if it does, we display
        the error by throwing an exception (client mode).

        :param `Message` m:  The content of the SSH2_MSG_KEXGSS_ERROR message
        :raise SSHException: Contains GSS-API major and minor status as well as
                             the error message and the language tag of the
                             message
        """
        maj_status = m.get_int()
        min_status = m.get_int()
        err_msg = m.get_string()
        m.get_string()
        raise SSHException('GSS-API Error:\nMajor Status: {}\nMinor Status: {}\nError Message: {}\n'.formatmaj_statusmin_statuserr_msg)


class NullHostKey(object):
    __doc__ = '\n    This class represents the Null Host Key for GSS-API Key Exchange as defined\n    in `RFC 4462 Section 5\n    <https://tools.ietf.org/html/rfc4462.html#section-5>`_\n    '

    def __init__(self):
        self.key = ''

    def __str__(self):
        return self.key

    def get_name(self):
        return self.key