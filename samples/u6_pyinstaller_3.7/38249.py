# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\paramiko\transport.py
"""
Core protocol implementation
"""
from __future__ import print_function
import os, socket, sys, threading, time, weakref
from hashlib import md5, sha1, sha256, sha512
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import algorithms, Cipher, modes
import paramiko
from paramiko import util
from paramiko.auth_handler import AuthHandler
from paramiko.ssh_gss import GSSAuth
from paramiko.channel import Channel
from paramiko.common import xffffffff, cMSG_CHANNEL_OPEN, cMSG_IGNORE, cMSG_GLOBAL_REQUEST, DEBUG, MSG_KEXINIT, MSG_IGNORE, MSG_DISCONNECT, MSG_DEBUG, ERROR, WARNING, cMSG_UNIMPLEMENTED, INFO, cMSG_KEXINIT, cMSG_NEWKEYS, MSG_NEWKEYS, cMSG_REQUEST_SUCCESS, cMSG_REQUEST_FAILURE, CONNECTION_FAILED_CODE, OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED, OPEN_SUCCEEDED, cMSG_CHANNEL_OPEN_FAILURE, cMSG_CHANNEL_OPEN_SUCCESS, MSG_GLOBAL_REQUEST, MSG_REQUEST_SUCCESS, MSG_REQUEST_FAILURE, MSG_CHANNEL_OPEN_SUCCESS, MSG_CHANNEL_OPEN_FAILURE, MSG_CHANNEL_OPEN, MSG_CHANNEL_SUCCESS, MSG_CHANNEL_FAILURE, MSG_CHANNEL_DATA, MSG_CHANNEL_EXTENDED_DATA, MSG_CHANNEL_WINDOW_ADJUST, MSG_CHANNEL_REQUEST, MSG_CHANNEL_EOF, MSG_CHANNEL_CLOSE, MIN_WINDOW_SIZE, MIN_PACKET_SIZE, MAX_WINDOW_SIZE, DEFAULT_WINDOW_SIZE, DEFAULT_MAX_PACKET_SIZE, HIGHEST_USERAUTH_MESSAGE_ID, MSG_UNIMPLEMENTED, MSG_NAMES
from paramiko.compress import ZlibCompressor, ZlibDecompressor
from paramiko.dsskey import DSSKey
from paramiko.ed25519key import Ed25519Key
from paramiko.kex_curve25519 import KexCurve25519
from paramiko.kex_gex import KexGex, KexGexSHA256
from paramiko.kex_group1 import KexGroup1
from paramiko.kex_group14 import KexGroup14, KexGroup14SHA256
from paramiko.kex_group16 import KexGroup16SHA512
from paramiko.kex_ecdh_nist import KexNistp256, KexNistp384, KexNistp521
from paramiko.kex_gss import KexGSSGex, KexGSSGroup1, KexGSSGroup14
from paramiko.message import Message
from paramiko.packet import Packetizer, NeedRekeyException
from paramiko.primes import ModulusPack
from paramiko.py3compat import string_types, long, byte_ord, b, input, PY2
from paramiko.rsakey import RSAKey
from paramiko.ecdsakey import ECDSAKey
from paramiko.server import ServerInterface
from paramiko.sftp_client import SFTPClient
from paramiko.ssh_exception import SSHException, BadAuthenticationType, ChannelException, ProxyCommandFailure
from paramiko.util import retry_on_signal, ClosingContextManager, clamp_value
_active_threads = []

def _join_lingering_threads():
    for thr in _active_threads:
        thr.stop_thread()


import atexit
atexit.register(_join_lingering_threads)

class Transport(threading.Thread, ClosingContextManager):
    __doc__ = '\n    An SSH Transport attaches to a stream (usually a socket), negotiates an\n    encrypted session, authenticates, and then creates stream tunnels, called\n    `channels <.Channel>`, across the session.  Multiple channels can be\n    multiplexed across a single session (and often are, in the case of port\n    forwardings).\n\n    Instances of this class may be used as context managers.\n    '
    _ENCRYPT = object()
    _DECRYPT = object()
    _PROTO_ID = '2.0'
    _CLIENT_ID = 'paramiko_{}'.format(paramiko.__version__)
    _preferred_ciphers = ('aes128-ctr', 'aes192-ctr', 'aes256-ctr', 'aes128-cbc', 'aes192-cbc',
                          'aes256-cbc', 'blowfish-cbc', '3des-cbc')
    _preferred_macs = ('hmac-sha2-256', 'hmac-sha2-512', 'hmac-sha2-256-etm@openssh.com',
                       'hmac-sha2-512-etm@openssh.com', 'hmac-sha1', 'hmac-md5',
                       'hmac-sha1-96', 'hmac-md5-96')
    _preferred_keys = ('ssh-ed25519', 'ecdsa-sha2-nistp256', 'ecdsa-sha2-nistp384',
                       'ecdsa-sha2-nistp521', 'ssh-rsa', 'ssh-dss')
    _preferred_kex = ('ecdh-sha2-nistp256', 'ecdh-sha2-nistp384', 'ecdh-sha2-nistp521',
                      'diffie-hellman-group16-sha512', 'diffie-hellman-group-exchange-sha256',
                      'diffie-hellman-group14-sha256', 'diffie-hellman-group-exchange-sha1',
                      'diffie-hellman-group14-sha1', 'diffie-hellman-group1-sha1')
    if KexCurve25519.is_available():
        _preferred_kex = ('curve25519-sha256@libssh.org', ) + _preferred_kex
    _preferred_gsskex = ('gss-gex-sha1-toWM5Slw5Ew8Mqkay+al2g==', 'gss-group14-sha1-toWM5Slw5Ew8Mqkay+al2g==',
                         'gss-group1-sha1-toWM5Slw5Ew8Mqkay+al2g==')
    _preferred_compression = ('none', )
    _cipher_info = {'aes128-ctr':{'class':algorithms.AES, 
      'mode':modes.CTR, 
      'block-size':16, 
      'key-size':16}, 
     'aes192-ctr':{'class':algorithms.AES, 
      'mode':modes.CTR, 
      'block-size':16, 
      'key-size':24}, 
     'aes256-ctr':{'class':algorithms.AES, 
      'mode':modes.CTR, 
      'block-size':16, 
      'key-size':32}, 
     'blowfish-cbc':{'class':algorithms.Blowfish, 
      'mode':modes.CBC, 
      'block-size':8, 
      'key-size':16}, 
     'aes128-cbc':{'class':algorithms.AES, 
      'mode':modes.CBC, 
      'block-size':16, 
      'key-size':16}, 
     'aes192-cbc':{'class':algorithms.AES, 
      'mode':modes.CBC, 
      'block-size':16, 
      'key-size':24}, 
     'aes256-cbc':{'class':algorithms.AES, 
      'mode':modes.CBC, 
      'block-size':16, 
      'key-size':32}, 
     '3des-cbc':{'class':algorithms.TripleDES, 
      'mode':modes.CBC, 
      'block-size':8, 
      'key-size':24}}
    _mac_info = {'hmac-sha1':{'class':sha1, 
      'size':20}, 
     'hmac-sha1-96':{'class':sha1, 
      'size':12}, 
     'hmac-sha2-256':{'class':sha256, 
      'size':32}, 
     'hmac-sha2-256-etm@openssh.com':{'class':sha256, 
      'size':32}, 
     'hmac-sha2-512':{'class':sha512, 
      'size':64}, 
     'hmac-sha2-512-etm@openssh.com':{'class':sha512, 
      'size':64}, 
     'hmac-md5':{'class':md5, 
      'size':16}, 
     'hmac-md5-96':{'class':md5, 
      'size':12}}
    _key_info = {'ssh-rsa':RSAKey, 
     'ssh-rsa-cert-v01@openssh.com':RSAKey, 
     'ssh-dss':DSSKey, 
     'ssh-dss-cert-v01@openssh.com':DSSKey, 
     'ecdsa-sha2-nistp256':ECDSAKey, 
     'ecdsa-sha2-nistp256-cert-v01@openssh.com':ECDSAKey, 
     'ecdsa-sha2-nistp384':ECDSAKey, 
     'ecdsa-sha2-nistp384-cert-v01@openssh.com':ECDSAKey, 
     'ecdsa-sha2-nistp521':ECDSAKey, 
     'ecdsa-sha2-nistp521-cert-v01@openssh.com':ECDSAKey, 
     'ssh-ed25519':Ed25519Key, 
     'ssh-ed25519-cert-v01@openssh.com':Ed25519Key}
    _kex_info = {'diffie-hellman-group1-sha1':KexGroup1, 
     'diffie-hellman-group14-sha1':KexGroup14, 
     'diffie-hellman-group-exchange-sha1':KexGex, 
     'diffie-hellman-group-exchange-sha256':KexGexSHA256, 
     'diffie-hellman-group14-sha256':KexGroup14SHA256, 
     'diffie-hellman-group16-sha512':KexGroup16SHA512, 
     'gss-group1-sha1-toWM5Slw5Ew8Mqkay+al2g==':KexGSSGroup1, 
     'gss-group14-sha1-toWM5Slw5Ew8Mqkay+al2g==':KexGSSGroup14, 
     'gss-gex-sha1-toWM5Slw5Ew8Mqkay+al2g==':KexGSSGex, 
     'ecdh-sha2-nistp256':KexNistp256, 
     'ecdh-sha2-nistp384':KexNistp384, 
     'ecdh-sha2-nistp521':KexNistp521}
    if KexCurve25519.is_available():
        _kex_info['curve25519-sha256@libssh.org'] = KexCurve25519
    _compression_info = {'zlib@openssh.com':(
      ZlibCompressor, ZlibDecompressor), 
     'zlib':(
      ZlibCompressor, ZlibDecompressor), 
     'none':(None, None)}
    _modulus_pack = None
    _active_check_timeout = 0.1

    def __init__(self, sock, default_window_size=DEFAULT_WINDOW_SIZE, default_max_packet_size=DEFAULT_MAX_PACKET_SIZE, gss_kex=False, gss_deleg_creds=True, disabled_algorithms=None):
        """
        Create a new SSH session over an existing socket, or socket-like
        object.  This only creates the `.Transport` object; it doesn't begin
        the SSH session yet.  Use `connect` or `start_client` to begin a client
        session, or `start_server` to begin a server session.

        If the object is not actually a socket, it must have the following
        methods:

        - ``send(str)``: Writes from 1 to ``len(str)`` bytes, and returns an
          int representing the number of bytes written.  Returns
          0 or raises ``EOFError`` if the stream has been closed.
        - ``recv(int)``: Reads from 1 to ``int`` bytes and returns them as a
          string.  Returns 0 or raises ``EOFError`` if the stream has been
          closed.
        - ``close()``: Closes the socket.
        - ``settimeout(n)``: Sets a (float) timeout on I/O operations.

        For ease of use, you may also pass in an address (as a tuple) or a host
        string as the ``sock`` argument.  (A host string is a hostname with an
        optional port (separated by ``":"``) which will be converted into a
        tuple of ``(hostname, port)``.)  A socket will be connected to this
        address and used for communication.  Exceptions from the ``socket``
        call may be thrown in this case.

        .. note::
            Modifying the the window and packet sizes might have adverse
            effects on your channels created from this transport. The default
            values are the same as in the OpenSSH code base and have been
            battle tested.

        :param socket sock:
            a socket or socket-like object to create the session over.
        :param int default_window_size:
            sets the default window size on the transport. (defaults to
            2097152)
        :param int default_max_packet_size:
            sets the default max packet size on the transport. (defaults to
            32768)
        :param bool gss_kex:
            Whether to enable GSSAPI key exchange when GSSAPI is in play.
            Default: ``False``.
        :param bool gss_deleg_creds:
            Whether to enable GSSAPI credential delegation when GSSAPI is in
            play. Default: ``True``.
        :param dict disabled_algorithms:
            If given, must be a dictionary mapping algorithm type to an
            iterable of algorithm identifiers, which will be disabled for the
            lifetime of the transport.

            Keys should match the last word in the class' builtin algorithm
            tuple attributes, such as ``"ciphers"`` to disable names within
            ``_preferred_ciphers``; or ``"kex"`` to disable something defined
            inside ``_preferred_kex``. Values should exactly match members of
            the matching attribute.

            For example, if you need to disable
            ``diffie-hellman-group16-sha512`` key exchange (perhaps because
            your code talks to a server which implements it differently from
            Paramiko), specify ``disabled_algorithms={"kex":
            ["diffie-hellman-group16-sha512"]}``.

        .. versionchanged:: 1.15
            Added the ``default_window_size`` and ``default_max_packet_size``
            arguments.
        .. versionchanged:: 1.15
            Added the ``gss_kex`` and ``gss_deleg_creds`` kwargs.
        .. versionchanged:: 2.6
            Added the ``disabled_algorithms`` kwarg.
        """
        self.active = False
        self.hostname = None
        if isinstance(sock, string_types):
            hl = sock.split(':', 1)
            self.hostname = hl[0]
            if len(hl) == 1:
                sock = (
                 hl[0], 22)
            else:
                sock = (
                 hl[0], int(hl[1]))
        if type(sock) is tuple:
            hostname, port = sock
            self.hostname = hostname
            reason = 'No suitable address family'
            addrinfos = socket.getaddrinfo(hostname, port, socket.AF_UNSPEC, socket.SOCK_STREAM)
            for family, socktype, proto, canonname, sockaddr in addrinfos:
                if socktype == socket.SOCK_STREAM:
                    af = family
                    sock = socket.socket(af, socket.SOCK_STREAM)
                    try:
                        retry_on_signal(lambda : sock.connect((hostname, port)))
                    except socket.error as e:
                        try:
                            reason = str(e)
                        finally:
                            e = None
                            del e

                    break
            else:
                raise SSHException('Unable to connect to {}: {}'.format(hostname, reason))

        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.sock = sock
        self.sock.settimeout(self._active_check_timeout)
        self.packetizer = Packetizer(sock)
        self.local_version = 'SSH-' + self._PROTO_ID + '-' + self._CLIENT_ID
        self.remote_version = ''
        self.local_cipher = self.remote_cipher = ''
        self.local_kex_init = self.remote_kex_init = None
        self.local_mac = self.remote_mac = None
        self.local_compression = self.remote_compression = None
        self.session_id = None
        self.host_key_type = None
        self.host_key = None
        self.use_gss_kex = gss_kex
        self.gss_kex_used = False
        self.kexgss_ctxt = None
        self.gss_host = None
        if self.use_gss_kex:
            self.kexgss_ctxt = GSSAuth('gssapi-keyex', gss_deleg_creds)
            self._preferred_kex = self._preferred_gsskex + self._preferred_kex
        self.kex_engine = None
        self.H = None
        self.K = None
        self.initial_kex_done = False
        self.in_kex = False
        self.authenticated = False
        self._expected_packet = tuple()
        self.lock = threading.Lock()
        self._channels = ChannelMap()
        self.channel_events = {}
        self.channels_seen = {}
        self._channel_counter = 0
        self.default_max_packet_size = default_max_packet_size
        self.default_window_size = default_window_size
        self._forward_agent_handler = None
        self._x11_handler = None
        self._tcp_handler = None
        self.saved_exception = None
        self.clear_to_send = threading.Event()
        self.clear_to_send_lock = threading.Lock()
        self.clear_to_send_timeout = 30.0
        self.log_name = 'paramiko.transport'
        self.logger = util.get_logger(self.log_name)
        self.packetizer.set_log(self.logger)
        self.auth_handler = None
        self.global_response = None
        self.completion_event = None
        self.banner_timeout = 15
        self.handshake_timeout = 15
        self.auth_timeout = 30
        self.disabled_algorithms = disabled_algorithms or {}
        self.server_mode = False
        self.server_object = None
        self.server_key_dict = {}
        self.server_accepts = []
        self.server_accept_cv = threading.Condition(self.lock)
        self.subsystem_table = {}

    def _filter_algorithm(self, type_):
        default = getattr(self, '_preferred_{}'.format(type_))
        return tuple((x for x in default if x not in self.disabled_algorithms.get(type_, [])))

    @property
    def preferred_ciphers(self):
        return self._filter_algorithm('ciphers')

    @property
    def preferred_macs(self):
        return self._filter_algorithm('macs')

    @property
    def preferred_keys(self):
        return self._filter_algorithm('keys')

    @property
    def preferred_kex(self):
        return self._filter_algorithm('kex')

    @property
    def preferred_compression(self):
        return self._filter_algorithm('compression')

    def __repr__(self):
        """
        Returns a string representation of this object, for debugging.
        """
        id_ = hex(long(id(self)) & xffffffff)
        out = '<paramiko.Transport at {}'.format(id_)
        if not self.active:
            out += ' (unconnected)'
        else:
            if self.local_cipher != '':
                out += ' (cipher {}, {:d} bits)'.format(self.local_cipher, self._cipher_info[self.local_cipher]['key-size'] * 8)
            elif self.is_authenticated():
                out += ' (active; {} open channel(s))'.format(len(self._channels))
            else:
                if self.initial_kex_done:
                    out += ' (connected; awaiting auth)'
                else:
                    out += ' (connecting)'
        out += '>'
        return out

    def atfork(self):
        """
        Terminate this Transport without closing the session.  On posix
        systems, if a Transport is open during process forking, both parent
        and child will share the underlying socket, but only one process can
        use the connection (without corrupting the session).  Use this method
        to clean up a Transport object without disrupting the other process.

        .. versionadded:: 1.5.3
        """
        self.sock.close()
        self.close()

    def get_security_options(self):
        """
        Return a `.SecurityOptions` object which can be used to tweak the
        encryption algorithms this transport will permit (for encryption,
        digest/hash operations, public keys, and key exchanges) and the order
        of preference for them.
        """
        return SecurityOptions(self)

    def set_gss_host(self, gss_host, trust_dns=True, gssapi_requested=True):
        """
        Normalize/canonicalize ``self.gss_host`` depending on various factors.

        :param str gss_host:
            The explicitly requested GSS-oriented hostname to connect to (i.e.
            what the host's name is in the Kerberos database.) Defaults to
            ``self.hostname`` (which will be the 'real' target hostname and/or
            host portion of given socket object.)
        :param bool trust_dns:
            Indicates whether or not DNS is trusted; if true, DNS will be used
            to canonicalize the GSS hostname (which again will either be
            ``gss_host`` or the transport's default hostname.)
            (Defaults to True due to backwards compatibility.)
        :param bool gssapi_requested:
            Whether GSSAPI key exchange or authentication was even requested.
            If not, this is a no-op and nothing happens
            (and ``self.gss_host`` is not set.)
            (Defaults to True due to backwards compatibility.)
        :returns: ``None``.
        """
        if not gssapi_requested:
            return
        else:
            if gss_host is None:
                gss_host = self.hostname
            if trust_dns and gss_host is not None:
                gss_host = socket.getfqdn(gss_host)
        self.gss_host = gss_host

    def start_client(self, event=None, timeout=None):
        """
        Negotiate a new SSH2 session as a client.  This is the first step after
        creating a new `.Transport`.  A separate thread is created for protocol
        negotiation.

        If an event is passed in, this method returns immediately.  When
        negotiation is done (successful or not), the given ``Event`` will
        be triggered.  On failure, `is_active` will return ``False``.

        (Since 1.4) If ``event`` is ``None``, this method will not return until
        negotiation is done.  On success, the method returns normally.
        Otherwise an SSHException is raised.

        After a successful negotiation, you will usually want to authenticate,
        calling `auth_password <Transport.auth_password>` or
        `auth_publickey <Transport.auth_publickey>`.

        .. note:: `connect` is a simpler method for connecting as a client.

        .. note::
            After calling this method (or `start_server` or `connect`), you
            should no longer directly read from or write to the original socket
            object.

        :param .threading.Event event:
            an event to trigger when negotiation is complete (optional)

        :param float timeout:
            a timeout, in seconds, for SSH2 session negotiation (optional)

        :raises:
            `.SSHException` -- if negotiation fails (and no ``event`` was
            passed in)
        """
        self.active = True
        if event is not None:
            self.completion_event = event
            self.start()
            return
        self.completion_event = event = threading.Event()
        self.start()
        max_time = time.time() + timeout if timeout is not None else None
        while 1:
            event.wait(0.1)
            if not self.active:
                e = self.get_exception()
                if e is not None:
                    raise e
                raise SSHException('Negotiation failed.')
            if not event.is_set():
                if not timeout is not None or time.time() >= max_time:
                    break

    def start_server(self, event=None, server=None):
        """
        Negotiate a new SSH2 session as a server.  This is the first step after
        creating a new `.Transport` and setting up your server host key(s).  A
        separate thread is created for protocol negotiation.

        If an event is passed in, this method returns immediately.  When
        negotiation is done (successful or not), the given ``Event`` will
        be triggered.  On failure, `is_active` will return ``False``.

        (Since 1.4) If ``event`` is ``None``, this method will not return until
        negotiation is done.  On success, the method returns normally.
        Otherwise an SSHException is raised.

        After a successful negotiation, the client will need to authenticate.
        Override the methods `get_allowed_auths
        <.ServerInterface.get_allowed_auths>`, `check_auth_none
        <.ServerInterface.check_auth_none>`, `check_auth_password
        <.ServerInterface.check_auth_password>`, and `check_auth_publickey
        <.ServerInterface.check_auth_publickey>` in the given ``server`` object
        to control the authentication process.

        After a successful authentication, the client should request to open a
        channel.  Override `check_channel_request
        <.ServerInterface.check_channel_request>` in the given ``server``
        object to allow channels to be opened.

        .. note::
            After calling this method (or `start_client` or `connect`), you
            should no longer directly read from or write to the original socket
            object.

        :param .threading.Event event:
            an event to trigger when negotiation is complete.
        :param .ServerInterface server:
            an object used to perform authentication and create `channels
            <.Channel>`

        :raises:
            `.SSHException` -- if negotiation fails (and no ``event`` was
            passed in)
        """
        if server is None:
            server = ServerInterface()
        self.server_mode = True
        self.server_object = server
        self.active = True
        if event is not None:
            self.completion_event = event
            self.start()
            return
        self.completion_event = event = threading.Event()
        self.start()
        while 1:
            event.wait(0.1)
            if not self.active:
                e = self.get_exception()
                if e is not None:
                    raise e
                raise SSHException('Negotiation failed.')
            if event.is_set():
                break

    def add_server_key(self, key):
        """
        Add a host key to the list of keys used for server mode.  When behaving
        as a server, the host key is used to sign certain packets during the
        SSH2 negotiation, so that the client can trust that we are who we say
        we are.  Because this is used for signing, the key must contain private
        key info, not just the public half.  Only one key of each type (RSA or
        DSS) is kept.

        :param .PKey key:
            the host key to add, usually an `.RSAKey` or `.DSSKey`.
        """
        self.server_key_dict[key.get_name()] = key

    def get_server_key(self):
        """
        Return the active host key, in server mode.  After negotiating with the
        client, this method will return the negotiated host key.  If only one
        type of host key was set with `add_server_key`, that's the only key
        that will ever be returned.  But in cases where you have set more than
        one type of host key (for example, an RSA key and a DSS key), the key
        type will be negotiated by the client, and this method will return the
        key of the type agreed on.  If the host key has not been negotiated
        yet, ``None`` is returned.  In client mode, the behavior is undefined.

        :return:
            host key (`.PKey`) of the type negotiated by the client, or
            ``None``.
        """
        try:
            return self.server_key_dict[self.host_key_type]
        except KeyError:
            pass

    @staticmethod
    def load_server_moduli(filename=None):
        """
        (optional)
        Load a file of prime moduli for use in doing group-exchange key
        negotiation in server mode.  It's a rather obscure option and can be
        safely ignored.

        In server mode, the remote client may request "group-exchange" key
        negotiation, which asks the server to send a random prime number that
        fits certain criteria.  These primes are pretty difficult to compute,
        so they can't be generated on demand.  But many systems contain a file
        of suitable primes (usually named something like ``/etc/ssh/moduli``).
        If you call `load_server_moduli` and it returns ``True``, then this
        file of primes has been loaded and we will support "group-exchange" in
        server mode.  Otherwise server mode will just claim that it doesn't
        support that method of key negotiation.

        :param str filename:
            optional path to the moduli file, if you happen to know that it's
            not in a standard location.
        :return:
            True if a moduli file was successfully loaded; False otherwise.

        .. note:: This has no effect when used in client mode.
        """
        Transport._modulus_pack = ModulusPack()
        file_list = [
         '/etc/ssh/moduli', '/usr/local/etc/moduli']
        if filename is not None:
            file_list.insert(0, filename)
        for fn in file_list:
            try:
                Transport._modulus_pack.read_file(fn)
                return True
            except IOError:
                pass

        Transport._modulus_pack = None
        return False

    def close(self):
        """
        Close this session, and any open channels that are tied to it.
        """
        if not self.active:
            return
        self.stop_thread()
        for chan in list(self._channels.values()):
            chan._unlink()

        self.sock.close()

    def get_remote_server_key(self):
        """
        Return the host key of the server (in client mode).

        .. note::
            Previously this call returned a tuple of ``(key type, key
            string)``. You can get the same effect by calling `.PKey.get_name`
            for the key type, and ``str(key)`` for the key string.

        :raises: `.SSHException` -- if no session is currently active.

        :return: public key (`.PKey`) of the remote server
        """
        if not (self.active and self.initial_kex_done):
            raise SSHException('No existing session')
        return self.host_key

    def is_active(self):
        """
        Return true if this session is active (open).

        :return:
            True if the session is still active (open); False if the session is
            closed
        """
        return self.active

    def open_session(self, window_size=None, max_packet_size=None, timeout=None):
        """
        Request a new channel to the server, of type ``"session"``.  This is
        just an alias for calling `open_channel` with an argument of
        ``"session"``.

        .. note:: Modifying the the window and packet sizes might have adverse
            effects on the session created. The default values are the same
            as in the OpenSSH code base and have been battle tested.

        :param int window_size:
            optional window size for this session.
        :param int max_packet_size:
            optional max packet size for this session.

        :return: a new `.Channel`

        :raises:
            `.SSHException` -- if the request is rejected or the session ends
            prematurely

        .. versionchanged:: 1.13.4/1.14.3/1.15.3
            Added the ``timeout`` argument.
        .. versionchanged:: 1.15
            Added the ``window_size`` and ``max_packet_size`` arguments.
        """
        return self.open_channel('session',
          window_size=window_size,
          max_packet_size=max_packet_size,
          timeout=timeout)

    def open_x11_channel(self, src_addr=None):
        """
        Request a new channel to the client, of type ``"x11"``.  This
        is just an alias for ``open_channel('x11', src_addr=src_addr)``.

        :param tuple src_addr:
            the source address (``(str, int)``) of the x11 server (port is the
            x11 port, ie. 6010)
        :return: a new `.Channel`

        :raises:
            `.SSHException` -- if the request is rejected or the session ends
            prematurely
        """
        return self.open_channel('x11', src_addr=src_addr)

    def open_forward_agent_channel(self):
        """
        Request a new channel to the client, of type
        ``"auth-agent@openssh.com"``.

        This is just an alias for ``open_channel('auth-agent@openssh.com')``.

        :return: a new `.Channel`

        :raises: `.SSHException` --
            if the request is rejected or the session ends prematurely
        """
        return self.open_channel('auth-agent@openssh.com')

    def open_forwarded_tcpip_channel(self, src_addr, dest_addr):
        """
        Request a new channel back to the client, of type ``forwarded-tcpip``.

        This is used after a client has requested port forwarding, for sending
        incoming connections back to the client.

        :param src_addr: originator's address
        :param dest_addr: local (server) connected address
        """
        return self.open_channel('forwarded-tcpip', dest_addr, src_addr)

    def open_channel(self, kind, dest_addr=None, src_addr=None, window_size=None, max_packet_size=None, timeout=None):
        """
        Request a new channel to the server. `Channels <.Channel>` are
        socket-like objects used for the actual transfer of data across the
        session. You may only request a channel after negotiating encryption
        (using `connect` or `start_client`) and authenticating.

        .. note:: Modifying the the window and packet sizes might have adverse
            effects on the channel created. The default values are the same
            as in the OpenSSH code base and have been battle tested.

        :param str kind:
            the kind of channel requested (usually ``"session"``,
            ``"forwarded-tcpip"``, ``"direct-tcpip"``, or ``"x11"``)
        :param tuple dest_addr:
            the destination address (address + port tuple) of this port
            forwarding, if ``kind`` is ``"forwarded-tcpip"`` or
            ``"direct-tcpip"`` (ignored for other channel types)
        :param src_addr: the source address of this port forwarding, if
            ``kind`` is ``"forwarded-tcpip"``, ``"direct-tcpip"``, or ``"x11"``
        :param int window_size:
            optional window size for this session.
        :param int max_packet_size:
            optional max packet size for this session.
        :param float timeout:
            optional timeout opening a channel, default 3600s (1h)

        :return: a new `.Channel` on success

        :raises:
            `.SSHException` -- if the request is rejected, the session ends
            prematurely or there is a timeout openning a channel

        .. versionchanged:: 1.15
            Added the ``window_size`` and ``max_packet_size`` arguments.
        """
        if not self.active:
            raise SSHException('SSH session not active')
        timeout = 3600 if timeout is None else timeout
        self.lock.acquire()
        try:
            window_size = self._sanitize_window_size(window_size)
            max_packet_size = self._sanitize_packet_size(max_packet_size)
            chanid = self._next_channel()
            m = Message()
            m.add_byte(cMSG_CHANNEL_OPEN)
            m.add_string(kind)
            m.add_int(chanid)
            m.add_int(window_size)
            m.add_int(max_packet_size)
            if kind == 'forwarded-tcpip' or kind == 'direct-tcpip':
                m.add_string(dest_addr[0])
                m.add_int(dest_addr[1])
                m.add_string(src_addr[0])
                m.add_int(src_addr[1])
            else:
                if kind == 'x11':
                    m.add_string(src_addr[0])
                    m.add_int(src_addr[1])
            chan = Channel(chanid)
            self._channels.put(chanid, chan)
            self.channel_events[chanid] = event = threading.Event()
            self.channels_seen[chanid] = True
            chan._set_transport(self)
            chan._set_window(window_size, max_packet_size)
        finally:
            self.lock.release()

        self._send_user_message(m)
        start_ts = time.time()
        while 1:
            event.wait(0.1)
            if not self.active:
                e = self.get_exception()
                if e is None:
                    e = SSHException('Unable to open channel.')
                raise e
            if event.is_set():
                break
            elif start_ts + timeout < time.time():
                raise SSHException('Timeout opening channel.')

        chan = self._channels.get(chanid)
        if chan is not None:
            return chan
        e = self.get_exception()
        if e is None:
            e = SSHException('Unable to open channel.')
        raise e

    def request_port_forward(self, address, port, handler=None):
        """
        Ask the server to forward TCP connections from a listening port on
        the server, across this SSH session.

        If a handler is given, that handler is called from a different thread
        whenever a forwarded connection arrives.  The handler parameters are::

            handler(
                channel,
                (origin_addr, origin_port),
                (server_addr, server_port),
            )

        where ``server_addr`` and ``server_port`` are the address and port that
        the server was listening on.

        If no handler is set, the default behavior is to send new incoming
        forwarded connections into the accept queue, to be picked up via
        `accept`.

        :param str address: the address to bind when forwarding
        :param int port:
            the port to forward, or 0 to ask the server to allocate any port
        :param callable handler:
            optional handler for incoming forwarded connections, of the form
            ``func(Channel, (str, int), (str, int))``.

        :return: the port number (`int`) allocated by the server

        :raises:
            `.SSHException` -- if the server refused the TCP forward request
        """
        if not self.active:
            raise SSHException('SSH session not active')
        port = int(port)
        response = self.global_request('tcpip-forward',
          (address, port), wait=True)
        if response is None:
            raise SSHException('TCP forwarding request denied')
        if port == 0:
            port = response.get_int()
        if handler is None:

            def default_handler(channel, src_addr, dest_addr_port):
                self._queue_incoming_channel(channel)

            handler = default_handler
        self._tcp_handler = handler
        return port

    def cancel_port_forward(self, address, port):
        """
        Ask the server to cancel a previous port-forwarding request.  No more
        connections to the given address & port will be forwarded across this
        ssh connection.

        :param str address: the address to stop forwarding
        :param int port: the port to stop forwarding
        """
        if not self.active:
            return
        self._tcp_handler = None
        self.global_request('cancel-tcpip-forward', (address, port), wait=True)

    def open_sftp_client(self):
        """
        Create an SFTP client channel from an open transport.  On success, an
        SFTP session will be opened with the remote host, and a new
        `.SFTPClient` object will be returned.

        :return:
            a new `.SFTPClient` referring to an sftp session (channel) across
            this transport
        """
        return SFTPClient.from_transport(self)

    def send_ignore(self, byte_count=None):
        """
        Send a junk packet across the encrypted link.  This is sometimes used
        to add "noise" to a connection to confuse would-be attackers.  It can
        also be used as a keep-alive for long lived connections traversing
        firewalls.

        :param int byte_count:
            the number of random bytes to send in the payload of the ignored
            packet -- defaults to a random number from 10 to 41.
        """
        m = Message()
        m.add_byte(cMSG_IGNORE)
        if byte_count is None:
            byte_count = byte_ord(os.urandom(1)) % 32 + 10
        m.add_bytes(os.urandom(byte_count))
        self._send_user_message(m)

    def renegotiate_keys(self):
        """
        Force this session to switch to new keys.  Normally this is done
        automatically after the session hits a certain number of packets or
        bytes sent or received, but this method gives you the option of forcing
        new keys whenever you want.  Negotiating new keys causes a pause in
        traffic both ways as the two sides swap keys and do computations.  This
        method returns when the session has switched to new keys.

        :raises:
            `.SSHException` -- if the key renegotiation failed (which causes
            the session to end)
        """
        self.completion_event = threading.Event()
        self._send_kex_init()
        while 1:
            self.completion_event.wait(0.1)
            if not self.active:
                e = self.get_exception()
                if e is not None:
                    raise e
                raise SSHException('Negotiation failed.')
            if self.completion_event.is_set():
                break

    def set_keepalive(self, interval):
        """
        Turn on/off keepalive packets (default is off).  If this is set, after
        ``interval`` seconds without sending any data over the connection, a
        "keepalive" packet will be sent (and ignored by the remote host).  This
        can be useful to keep connections alive over a NAT, for example.

        :param int interval:
            seconds to wait before sending a keepalive packet (or
            0 to disable keepalives).
        """

        def _request(x=weakref.proxy(self)):
            return x.global_request('keepalive@lag.net', wait=False)

        self.packetizer.set_keepalive(interval, _request)

    def global_request(self, kind, data=None, wait=True):
        """
        Make a global request to the remote host.  These are normally
        extensions to the SSH2 protocol.

        :param str kind: name of the request.
        :param tuple data:
            an optional tuple containing additional data to attach to the
            request.
        :param bool wait:
            ``True`` if this method should not return until a response is
            received; ``False`` otherwise.
        :return:
            a `.Message` containing possible additional data if the request was
            successful (or an empty `.Message` if ``wait`` was ``False``);
            ``None`` if the request was denied.
        """
        if wait:
            self.completion_event = threading.Event()
        else:
            m = Message()
            m.add_byte(cMSG_GLOBAL_REQUEST)
            m.add_string(kind)
            m.add_boolean(wait)
            if data is not None:
                (m.add)(*data)
            self._log(DEBUG, 'Sending global request "{}"'.format(kind))
            self._send_user_message(m)
            return wait or None
        while 1:
            self.completion_event.wait(0.1)
            if not self.active:
                return
                if self.completion_event.is_set():
                    break

        return self.global_response

    def accept(self, timeout=None):
        """
        Return the next channel opened by the client over this transport, in
        server mode.  If no channel is opened before the given timeout,
        ``None`` is returned.

        :param int timeout:
            seconds to wait for a channel, or ``None`` to wait forever
        :return: a new `.Channel` opened by the client
        """
        self.lock.acquire()
        try:
            if len(self.server_accepts) > 0:
                chan = self.server_accepts.pop(0)
            else:
                self.server_accept_cv.wait(timeout)
                if len(self.server_accepts) > 0:
                    chan = self.server_accepts.pop(0)
                else:
                    chan = None
        finally:
            self.lock.release()

        return chan

    def connect--- This code section failed: ---

 L.1282         0  LOAD_FAST                'hostkey'
                2  LOAD_CONST               None
                4  COMPARE_OP               is-not
                6  POP_JUMP_IF_FALSE    20  'to 20'

 L.1283         8  LOAD_FAST                'hostkey'
               10  LOAD_METHOD              get_name
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  BUILD_LIST_1          1 
               16  LOAD_FAST                'self'
               18  STORE_ATTR               _preferred_keys
             20_0  COME_FROM             6  '6'

 L.1285        20  LOAD_FAST                'self'
               22  LOAD_ATTR                set_gss_host

 L.1286        24  LOAD_FAST                'gss_host'

 L.1287        26  LOAD_FAST                'gss_trust_dns'

 L.1288        28  LOAD_FAST                'gss_kex'
               30  JUMP_IF_TRUE_OR_POP    34  'to 34'
               32  LOAD_FAST                'gss_auth'
             34_0  COME_FROM            30  '30'
               34  LOAD_CONST               ('gss_host', 'trust_dns', 'gssapi_requested')
               36  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               38  POP_TOP          

 L.1291        40  LOAD_FAST                'self'
               42  LOAD_METHOD              start_client
               44  CALL_METHOD_0         0  '0 positional arguments'
               46  POP_TOP          

 L.1296        48  LOAD_FAST                'hostkey'
               50  LOAD_CONST               None
               52  COMPARE_OP               is-not
               54  POP_JUMP_IF_FALSE   206  'to 206'
               56  LOAD_FAST                'gss_kex'
               58  POP_JUMP_IF_TRUE    206  'to 206'

 L.1297        60  LOAD_FAST                'self'
               62  LOAD_METHOD              get_remote_server_key
               64  CALL_METHOD_0         0  '0 positional arguments'
               66  STORE_FAST               'key'

 L.1299        68  LOAD_FAST                'key'
               70  LOAD_METHOD              get_name
               72  CALL_METHOD_0         0  '0 positional arguments'
               74  LOAD_FAST                'hostkey'
               76  LOAD_METHOD              get_name
               78  CALL_METHOD_0         0  '0 positional arguments'
               80  COMPARE_OP               !=
               82  POP_JUMP_IF_TRUE    100  'to 100'

 L.1300        84  LOAD_FAST                'key'
               86  LOAD_METHOD              asbytes
               88  CALL_METHOD_0         0  '0 positional arguments'
               90  LOAD_FAST                'hostkey'
               92  LOAD_METHOD              asbytes
               94  CALL_METHOD_0         0  '0 positional arguments'
               96  COMPARE_OP               !=
               98  POP_JUMP_IF_FALSE   184  'to 184'
            100_0  COME_FROM            82  '82'

 L.1302       100  LOAD_FAST                'self'
              102  LOAD_METHOD              _log
              104  LOAD_GLOBAL              DEBUG
              106  LOAD_STR                 'Bad host key from server'
              108  CALL_METHOD_2         2  '2 positional arguments'
              110  POP_TOP          

 L.1303       112  LOAD_FAST                'self'
              114  LOAD_METHOD              _log

 L.1304       116  LOAD_GLOBAL              DEBUG

 L.1305       118  LOAD_STR                 'Expected: {}: {}'
              120  LOAD_METHOD              format

 L.1306       122  LOAD_FAST                'hostkey'
              124  LOAD_METHOD              get_name
              126  CALL_METHOD_0         0  '0 positional arguments'
              128  LOAD_GLOBAL              repr
              130  LOAD_FAST                'hostkey'
              132  LOAD_METHOD              asbytes
              134  CALL_METHOD_0         0  '0 positional arguments'
              136  CALL_FUNCTION_1       1  '1 positional argument'
              138  CALL_METHOD_2         2  '2 positional arguments'
              140  CALL_METHOD_2         2  '2 positional arguments'
              142  POP_TOP          

 L.1309       144  LOAD_FAST                'self'
              146  LOAD_METHOD              _log

 L.1310       148  LOAD_GLOBAL              DEBUG

 L.1311       150  LOAD_STR                 'Got     : {}: {}'
              152  LOAD_METHOD              format

 L.1312       154  LOAD_FAST                'key'
              156  LOAD_METHOD              get_name
              158  CALL_METHOD_0         0  '0 positional arguments'
              160  LOAD_GLOBAL              repr
              162  LOAD_FAST                'key'
              164  LOAD_METHOD              asbytes
              166  CALL_METHOD_0         0  '0 positional arguments'
              168  CALL_FUNCTION_1       1  '1 positional argument'
              170  CALL_METHOD_2         2  '2 positional arguments'
              172  CALL_METHOD_2         2  '2 positional arguments'
              174  POP_TOP          

 L.1315       176  LOAD_GLOBAL              SSHException
              178  LOAD_STR                 'Bad host key from server'
              180  CALL_FUNCTION_1       1  '1 positional argument'
              182  RAISE_VARARGS_1       1  'exception instance'
            184_0  COME_FROM            98  '98'

 L.1316       184  LOAD_FAST                'self'
              186  LOAD_METHOD              _log

 L.1317       188  LOAD_GLOBAL              DEBUG
              190  LOAD_STR                 'Host key verified ({})'
              192  LOAD_METHOD              format
              194  LOAD_FAST                'hostkey'
              196  LOAD_METHOD              get_name
              198  CALL_METHOD_0         0  '0 positional arguments'
              200  CALL_METHOD_1         1  '1 positional argument'
              202  CALL_METHOD_2         2  '2 positional arguments'
              204  POP_TOP          
            206_0  COME_FROM            58  '58'
            206_1  COME_FROM            54  '54'

 L.1320       206  LOAD_FAST                'pkey'
              208  LOAD_CONST               None
              210  COMPARE_OP               is-not
              212  POP_JUMP_IF_TRUE    232  'to 232'
              214  LOAD_FAST                'password'
              216  LOAD_CONST               None
              218  COMPARE_OP               is-not
              220  POP_JUMP_IF_TRUE    232  'to 232'
              222  LOAD_FAST                'gss_auth'
              224  POP_JUMP_IF_TRUE    232  'to 232'
              226  LOAD_FAST                'gss_kex'
          228_230  POP_JUMP_IF_FALSE   358  'to 358'
            232_0  COME_FROM           224  '224'
            232_1  COME_FROM           220  '220'
            232_2  COME_FROM           212  '212'

 L.1321       232  LOAD_FAST                'gss_auth'
          234_236  POP_JUMP_IF_FALSE   268  'to 268'

 L.1322       238  LOAD_FAST                'self'
              240  LOAD_METHOD              _log

 L.1323       242  LOAD_GLOBAL              DEBUG
              244  LOAD_STR                 'Attempting GSS-API auth... (gssapi-with-mic)'
              246  CALL_METHOD_2         2  '2 positional arguments'
              248  POP_TOP          

 L.1325       250  LOAD_FAST                'self'
              252  LOAD_METHOD              auth_gssapi_with_mic

 L.1326       254  LOAD_FAST                'username'
              256  LOAD_FAST                'self'
              258  LOAD_ATTR                gss_host
              260  LOAD_FAST                'gss_deleg_creds'
              262  CALL_METHOD_3         3  '3 positional arguments'
              264  POP_TOP          
              266  JUMP_FORWARD        358  'to 358'
            268_0  COME_FROM           234  '234'

 L.1328       268  LOAD_FAST                'gss_kex'
          270_272  POP_JUMP_IF_FALSE   298  'to 298'

 L.1329       274  LOAD_FAST                'self'
              276  LOAD_METHOD              _log
              278  LOAD_GLOBAL              DEBUG
              280  LOAD_STR                 'Attempting GSS-API auth... (gssapi-keyex)'
              282  CALL_METHOD_2         2  '2 positional arguments'
              284  POP_TOP          

 L.1330       286  LOAD_FAST                'self'
              288  LOAD_METHOD              auth_gssapi_keyex
              290  LOAD_FAST                'username'
              292  CALL_METHOD_1         1  '1 positional argument'
              294  POP_TOP          
              296  JUMP_FORWARD        358  'to 358'
            298_0  COME_FROM           270  '270'

 L.1331       298  LOAD_FAST                'pkey'
              300  LOAD_CONST               None
              302  COMPARE_OP               is-not
          304_306  POP_JUMP_IF_FALSE   334  'to 334'

 L.1332       308  LOAD_FAST                'self'
              310  LOAD_METHOD              _log
              312  LOAD_GLOBAL              DEBUG
              314  LOAD_STR                 'Attempting public-key auth...'
              316  CALL_METHOD_2         2  '2 positional arguments'
              318  POP_TOP          

 L.1333       320  LOAD_FAST                'self'
              322  LOAD_METHOD              auth_publickey
              324  LOAD_FAST                'username'
              326  LOAD_FAST                'pkey'
              328  CALL_METHOD_2         2  '2 positional arguments'
              330  POP_TOP          
              332  JUMP_FORWARD        358  'to 358'
            334_0  COME_FROM           304  '304'

 L.1335       334  LOAD_FAST                'self'
              336  LOAD_METHOD              _log
              338  LOAD_GLOBAL              DEBUG
              340  LOAD_STR                 'Attempting password auth...'
              342  CALL_METHOD_2         2  '2 positional arguments'
              344  POP_TOP          

 L.1336       346  LOAD_FAST                'self'
              348  LOAD_METHOD              auth_password
              350  LOAD_FAST                'username'
              352  LOAD_FAST                'password'
              354  CALL_METHOD_2         2  '2 positional arguments'
              356  POP_TOP          
            358_0  COME_FROM           332  '332'
            358_1  COME_FROM           296  '296'
            358_2  COME_FROM           266  '266'
            358_3  COME_FROM           228  '228'

Parse error at or near `COME_FROM' instruction at offset 358_2

    def get_exception(self):
        """
        Return any exception that happened during the last server request.
        This can be used to fetch more specific error information after using
        calls like `start_client`.  The exception (if any) is cleared after
        this call.

        :return:
            an exception, or ``None`` if there is no stored exception.

        .. versionadded:: 1.1
        """
        self.lock.acquire()
        try:
            e = self.saved_exception
            self.saved_exception = None
            return e
        finally:
            self.lock.release()

    def set_subsystem_handler(self, name, handler, *larg, **kwarg):
        """
        Set the handler class for a subsystem in server mode.  If a request
        for this subsystem is made on an open ssh channel later, this handler
        will be constructed and called -- see `.SubsystemHandler` for more
        detailed documentation.

        Any extra parameters (including keyword arguments) are saved and
        passed to the `.SubsystemHandler` constructor later.

        :param str name: name of the subsystem.
        :param handler:
            subclass of `.SubsystemHandler` that handles this subsystem.
        """
        try:
            self.lock.acquire()
            self.subsystem_table[name] = (handler, larg, kwarg)
        finally:
            self.lock.release()

    def is_authenticated(self):
        """
        Return true if this session is active and authenticated.

        :return:
            True if the session is still open and has been authenticated
            successfully; False if authentication failed and/or the session is
            closed.
        """
        return self.active and self.auth_handler is not None and self.auth_handler.is_authenticated()

    def get_username(self):
        """
        Return the username this connection is authenticated for.  If the
        session is not authenticated (or authentication failed), this method
        returns ``None``.

        :return: username that was authenticated (a `str`), or ``None``.
        """
        if not self.active or self.auth_handler is None:
            return
        return self.auth_handler.get_username()

    def get_banner(self):
        """
        Return the banner supplied by the server upon connect. If no banner is
        supplied, this method returns ``None``.

        :returns: server supplied banner (`str`), or ``None``.

        .. versionadded:: 1.13
        """
        if not self.active or self.auth_handler is None:
            return
        return self.auth_handler.banner

    def auth_none(self, username):
        """
        Try to authenticate to the server using no authentication at all.
        This will almost always fail.  It may be useful for determining the
        list of authentication types supported by the server, by catching the
        `.BadAuthenticationType` exception raised.

        :param str username: the username to authenticate as
        :return:
            list of auth types permissible for the next stage of
            authentication (normally empty)

        :raises:
            `.BadAuthenticationType` -- if "none" authentication isn't allowed
            by the server for this user
        :raises:
            `.SSHException` -- if the authentication failed due to a network
            error

        .. versionadded:: 1.5
        """
        if not (self.active and self.initial_kex_done):
            raise SSHException('No existing session')
        my_event = threading.Event()
        self.auth_handler = AuthHandler(self)
        self.auth_handler.auth_none(username, my_event)
        return self.auth_handler.wait_for_response(my_event)

    def auth_password(self, username, password, event=None, fallback=True):
        """
        Authenticate to the server using a password.  The username and password
        are sent over an encrypted link.

        If an ``event`` is passed in, this method will return immediately, and
        the event will be triggered once authentication succeeds or fails.  On
        success, `is_authenticated` will return ``True``.  On failure, you may
        use `get_exception` to get more detailed error information.

        Since 1.1, if no event is passed, this method will block until the
        authentication succeeds or fails.  On failure, an exception is raised.
        Otherwise, the method simply returns.

        Since 1.5, if no event is passed and ``fallback`` is ``True`` (the
        default), if the server doesn't support plain password authentication
        but does support so-called "keyboard-interactive" mode, an attempt
        will be made to authenticate using this interactive mode.  If it fails,
        the normal exception will be thrown as if the attempt had never been
        made.  This is useful for some recent Gentoo and Debian distributions,
        which turn off plain password authentication in a misguided belief
        that interactive authentication is "more secure".  (It's not.)

        If the server requires multi-step authentication (which is very rare),
        this method will return a list of auth types permissible for the next
        step.  Otherwise, in the normal case, an empty list is returned.

        :param str username: the username to authenticate as
        :param basestring password: the password to authenticate with
        :param .threading.Event event:
            an event to trigger when the authentication attempt is complete
            (whether it was successful or not)
        :param bool fallback:
            ``True`` if an attempt at an automated "interactive" password auth
            should be made if the server doesn't support normal password auth
        :return:
            list of auth types permissible for the next stage of
            authentication (normally empty)

        :raises:
            `.BadAuthenticationType` -- if password authentication isn't
            allowed by the server for this user (and no event was passed in)
        :raises:
            `.AuthenticationException` -- if the authentication failed (and no
            event was passed in)
        :raises: `.SSHException` -- if there was a network error
        """
        if self.active:
            raise self.initial_kex_done or SSHException('No existing session')
        else:
            if event is None:
                my_event = threading.Event()
            else:
                my_event = event
            self.auth_handler = AuthHandler(self)
            self.auth_handler.auth_password(username, password, my_event)
            if event is not None:
                return []
            try:
                return self.auth_handler.wait_for_response(my_event)
            except BadAuthenticationType as e:
                try:
                    if not fallback or 'keyboard-interactive' not in e.allowed_types:
                        raise
                    try:

                        def handler(title, instructions, fields):
                            if len(fields) > 1:
                                raise SSHException('Fallback authentication failed.')
                            if len(fields) == 0:
                                return []
                            return [
                             password]

                        return self.auth_interactive(username, handler)
                    except SSHException:
                        raise e

                finally:
                    e = None
                    del e

    def auth_publickey(self, username, key, event=None):
        """
        Authenticate to the server using a private key.  The key is used to
        sign data from the server, so it must include the private part.

        If an ``event`` is passed in, this method will return immediately, and
        the event will be triggered once authentication succeeds or fails.  On
        success, `is_authenticated` will return ``True``.  On failure, you may
        use `get_exception` to get more detailed error information.

        Since 1.1, if no event is passed, this method will block until the
        authentication succeeds or fails.  On failure, an exception is raised.
        Otherwise, the method simply returns.

        If the server requires multi-step authentication (which is very rare),
        this method will return a list of auth types permissible for the next
        step.  Otherwise, in the normal case, an empty list is returned.

        :param str username: the username to authenticate as
        :param .PKey key: the private key to authenticate with
        :param .threading.Event event:
            an event to trigger when the authentication attempt is complete
            (whether it was successful or not)
        :return:
            list of auth types permissible for the next stage of
            authentication (normally empty)

        :raises:
            `.BadAuthenticationType` -- if public-key authentication isn't
            allowed by the server for this user (and no event was passed in)
        :raises:
            `.AuthenticationException` -- if the authentication failed (and no
            event was passed in)
        :raises: `.SSHException` -- if there was a network error
        """
        if self.active:
            raise self.initial_kex_done or SSHException('No existing session')
        elif event is None:
            my_event = threading.Event()
        else:
            my_event = event
        self.auth_handler = AuthHandler(self)
        self.auth_handler.auth_publickey(username, key, my_event)
        if event is not None:
            return []
        return self.auth_handler.wait_for_response(my_event)

    def auth_interactive(self, username, handler, submethods=''):
        """
        Authenticate to the server interactively.  A handler is used to answer
        arbitrary questions from the server.  On many servers, this is just a
        dumb wrapper around PAM.

        This method will block until the authentication succeeds or fails,
        peroidically calling the handler asynchronously to get answers to
        authentication questions.  The handler may be called more than once
        if the server continues to ask questions.

        The handler is expected to be a callable that will handle calls of the
        form: ``handler(title, instructions, prompt_list)``.  The ``title`` is
        meant to be a dialog-window title, and the ``instructions`` are user
        instructions (both are strings).  ``prompt_list`` will be a list of
        prompts, each prompt being a tuple of ``(str, bool)``.  The string is
        the prompt and the boolean indicates whether the user text should be
        echoed.

        A sample call would thus be:
        ``handler('title', 'instructions', [('Password:', False)])``.

        The handler should return a list or tuple of answers to the server's
        questions.

        If the server requires multi-step authentication (which is very rare),
        this method will return a list of auth types permissible for the next
        step.  Otherwise, in the normal case, an empty list is returned.

        :param str username: the username to authenticate as
        :param callable handler: a handler for responding to server questions
        :param str submethods: a string list of desired submethods (optional)
        :return:
            list of auth types permissible for the next stage of
            authentication (normally empty).

        :raises: `.BadAuthenticationType` -- if public-key authentication isn't
            allowed by the server for this user
        :raises: `.AuthenticationException` -- if the authentication failed
        :raises: `.SSHException` -- if there was a network error

        .. versionadded:: 1.5
        """
        if not (self.active and self.initial_kex_done):
            raise SSHException('No existing session')
        my_event = threading.Event()
        self.auth_handler = AuthHandler(self)
        self.auth_handler.auth_interactive(username, handler, my_event, submethods)
        return self.auth_handler.wait_for_response(my_event)

    def auth_interactive_dumb(self, username, handler=None, submethods=''):
        """
        Autenticate to the server interactively but dumber.
        Just print the prompt and / or instructions to stdout and send back
        the response. This is good for situations where partial auth is
        achieved by key and then the user has to enter a 2fac token.
        """
        if not handler:

            def handler(title, instructions, prompt_list):
                answers = []
                if title:
                    print(title.strip())
                if instructions:
                    print(instructions.strip())
                for prompt, show_input in prompt_list:
                    print((prompt.strip()), end=' ')
                    answers.append(input())

                return answers

        return self.auth_interactive(username, handler, submethods)

    def auth_gssapi_with_mic(self, username, gss_host, gss_deleg_creds):
        """
        Authenticate to the Server using GSS-API / SSPI.

        :param str username: The username to authenticate as
        :param str gss_host: The target host
        :param bool gss_deleg_creds: Delegate credentials or not
        :return: list of auth types permissible for the next stage of
                 authentication (normally empty)
        :raises: `.BadAuthenticationType` -- if gssapi-with-mic isn't
            allowed by the server (and no event was passed in)
        :raises:
            `.AuthenticationException` -- if the authentication failed (and no
            event was passed in)
        :raises: `.SSHException` -- if there was a network error
        """
        if not (self.active and self.initial_kex_done):
            raise SSHException('No existing session')
        my_event = threading.Event()
        self.auth_handler = AuthHandler(self)
        self.auth_handler.auth_gssapi_with_mic(username, gss_host, gss_deleg_creds, my_event)
        return self.auth_handler.wait_for_response(my_event)

    def auth_gssapi_keyex(self, username):
        """
        Authenticate to the server with GSS-API/SSPI if GSS-API kex is in use.

        :param str username: The username to authenticate as.
        :returns:
            a list of auth types permissible for the next stage of
            authentication (normally empty)
        :raises: `.BadAuthenticationType` --
            if GSS-API Key Exchange was not performed (and no event was passed
            in)
        :raises: `.AuthenticationException` --
            if the authentication failed (and no event was passed in)
        :raises: `.SSHException` -- if there was a network error
        """
        if not (self.active and self.initial_kex_done):
            raise SSHException('No existing session')
        my_event = threading.Event()
        self.auth_handler = AuthHandler(self)
        self.auth_handler.auth_gssapi_keyex(username, my_event)
        return self.auth_handler.wait_for_response(my_event)

    def set_log_channel(self, name):
        """
        Set the channel for this transport's logging.  The default is
        ``"paramiko.transport"`` but it can be set to anything you want. (See
        the `.logging` module for more info.)  SSH Channels will log to a
        sub-channel of the one specified.

        :param str name: new channel name for logging

        .. versionadded:: 1.1
        """
        self.log_name = name
        self.logger = util.get_logger(name)
        self.packetizer.set_log(self.logger)

    def get_log_channel(self):
        """
        Return the channel name used for this transport's logging.

        :return: channel name as a `str`

        .. versionadded:: 1.2
        """
        return self.log_name

    def set_hexdump(self, hexdump):
        """
        Turn on/off logging a hex dump of protocol traffic at DEBUG level in
        the logs.  Normally you would want this off (which is the default),
        but if you are debugging something, it may be useful.

        :param bool hexdump:
            ``True`` to log protocol traffix (in hex) to the log; ``False``
            otherwise.
        """
        self.packetizer.set_hexdump(hexdump)

    def get_hexdump(self):
        """
        Return ``True`` if the transport is currently logging hex dumps of
        protocol traffic.

        :return: ``True`` if hex dumps are being logged, else ``False``.

        .. versionadded:: 1.4
        """
        return self.packetizer.get_hexdump()

    def use_compression(self, compress=True):
        """
        Turn on/off compression.  This will only have an affect before starting
        the transport (ie before calling `connect`, etc).  By default,
        compression is off since it negatively affects interactive sessions.

        :param bool compress:
            ``True`` to ask the remote client/server to compress traffic;
            ``False`` to refuse compression

        .. versionadded:: 1.5.2
        """
        if compress:
            self._preferred_compression = ('zlib@openssh.com', 'zlib', 'none')
        else:
            self._preferred_compression = ('none', )

    def getpeername(self):
        """
        Return the address of the remote side of this Transport, if possible.

        This is effectively a wrapper around ``getpeername`` on the underlying
        socket.  If the socket-like object has no ``getpeername`` method, then
        ``("unknown", 0)`` is returned.

        :return:
            the address of the remote host, if known, as a ``(str, int)``
            tuple.
        """
        gp = getattr(self.sock, 'getpeername', None)
        if gp is None:
            return ('unknown', 0)
        return gp()

    def stop_thread(self):
        self.active = False
        self.packetizer.close()
        if PY2:
            while self.is_alive() and self is not threading.current_thread():
                self.join(10)

        else:
            while self.is_alive() and self is not threading.current_thread():
                self.sock._closed or self.packetizer.closed or self.join(0.1)

    def _log(self, level, msg, *args):
        if issubclass(type(msg), list):
            for m in msg:
                self.logger.log(level, m)

        else:
            (self.logger.log)(level, msg, *args)

    def _get_modulus_pack(self):
        """used by KexGex to find primes for group exchange"""
        return self._modulus_pack

    def _next_channel(self):
        """you are holding the lock"""
        chanid = self._channel_counter
        while self._channels.get(chanid) is not None:
            self._channel_counter = self._channel_counter + 1 & 16777215
            chanid = self._channel_counter

        self._channel_counter = self._channel_counter + 1 & 16777215
        return chanid

    def _unlink_channel(self, chanid):
        """used by a Channel to remove itself from the active channel list"""
        self._channels.delete(chanid)

    def _send_message(self, data):
        self.packetizer.send_message(data)

    def _send_user_message(self, data):
        """
        send a message, but block if we're in key negotiation.  this is used
        for user-initiated requests.
        """
        start = time.time()
        while 1:
            self.clear_to_send.wait(0.1)
            if not self.active:
                self._log(DEBUG, 'Dropping user packet because connection is dead.')
                return
                self.clear_to_send_lock.acquire()
                if self.clear_to_send.is_set():
                    break
                self.clear_to_send_lock.release()
                if time.time() > start + self.clear_to_send_timeout:
                    raise SSHException('Key-exchange timed out waiting for key negotiation')

        try:
            self._send_message(data)
        finally:
            self.clear_to_send_lock.release()

    def _set_K_H(self, k, h):
        """
        Used by a kex obj to set the K (root key) and H (exchange hash).
        """
        self.K = k
        self.H = h
        if self.session_id is None:
            self.session_id = h

    def _expect_packet(self, *ptypes):
        """
        Used by a kex obj to register the next packet type it expects to see.
        """
        self._expected_packet = tuple(ptypes)

    def _verify_key(self, host_key, sig):
        key = self._key_info[self.host_key_type](Message(host_key))
        if key is None:
            raise SSHException('Unknown host key type')
        if not key.verify_ssh_sig(self.H, Message(sig)):
            raise SSHException('Signature verification ({}) failed.'.format(self.host_key_type))
        self.host_key = key

    def _compute_key(self, id, nbytes):
        """id is 'A' - 'F' for the various keys used by ssh"""
        m = Message()
        m.add_mpint(self.K)
        m.add_bytes(self.H)
        m.add_byte(b(id))
        m.add_bytes(self.session_id)
        hash_algo = getattr(self.kex_engine, 'hash_algo', None)
        hash_select_msg = 'kex engine {} specified hash_algo {!r}'.format(self.kex_engine.__class__.__name__, hash_algo)
        if hash_algo is None:
            hash_algo = sha1
            hash_select_msg += ', falling back to sha1'
        if not hasattr(self, '_logged_hash_selection'):
            self._log(DEBUG, hash_select_msg)
            setattr(self, '_logged_hash_selection', True)
        out = sofar = hash_algo(m.asbytes()).digest()
        while len(out) < nbytes:
            m = Message()
            m.add_mpint(self.K)
            m.add_bytes(self.H)
            m.add_bytes(sofar)
            digest = hash_algo(m.asbytes()).digest()
            out += digest
            sofar += digest

        return out[:nbytes]

    def _get_cipher(self, name, key, iv, operation):
        if name not in self._cipher_info:
            raise SSHException('Unknown client cipher ' + name)
        else:
            cipher = Cipher((self._cipher_info[name]['class'](key)),
              (self._cipher_info[name]['mode'](iv)),
              backend=(default_backend()))
            if operation is self._ENCRYPT:
                return cipher.encryptor()
            return cipher.decryptor()

    def _set_forward_agent_handler(self, handler):
        if handler is None:

            def default_handler(channel):
                self._queue_incoming_channel(channel)

            self._forward_agent_handler = default_handler
        else:
            self._forward_agent_handler = handler

    def _set_x11_handler(self, handler):
        if handler is None:

            def default_handler(channel, src_addr_port):
                self._queue_incoming_channel(channel)

            self._x11_handler = default_handler
        else:
            self._x11_handler = handler

    def _queue_incoming_channel(self, channel):
        self.lock.acquire()
        try:
            self.server_accepts.append(channel)
            self.server_accept_cv.notify()
        finally:
            self.lock.release()

    def _sanitize_window_size(self, window_size):
        if window_size is None:
            window_size = self.default_window_size
        return clamp_value(MIN_WINDOW_SIZE, window_size, MAX_WINDOW_SIZE)

    def _sanitize_packet_size(self, max_packet_size):
        if max_packet_size is None:
            max_packet_size = self.default_max_packet_size
        return clamp_value(MIN_PACKET_SIZE, max_packet_size, MAX_WINDOW_SIZE)

    def _ensure_authed(self, ptype, message):
        """
        Checks message type against current auth state.

        If server mode, and auth has not succeeded, and the message is of a
        post-auth type (channel open or global request) an appropriate error
        response Message is crafted and returned to caller for sending.

        Otherwise (client mode, authed, or pre-auth message) returns None.
        """
        if self.server_mode:
            if ptype <= HIGHEST_USERAUTH_MESSAGE_ID or self.is_authenticated():
                return
            reply = Message()
            if ptype == MSG_GLOBAL_REQUEST:
                reply.add_byte(cMSG_REQUEST_FAILURE)
        elif ptype == MSG_CHANNEL_OPEN:
            kind = message.get_text()
            chanid = message.get_int()
            reply.add_byte(cMSG_CHANNEL_OPEN_FAILURE)
            reply.add_int(chanid)
            reply.add_int(OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED)
            reply.add_string('')
            reply.add_string('en')
        return reply

    def run--- This code section failed: ---

 L.2023         0  LOAD_GLOBAL              sys
                2  LOAD_FAST                'self'
                4  STORE_ATTR               sys

 L.2026         6  LOAD_GLOBAL              _active_threads
                8  LOAD_METHOD              append
               10  LOAD_FAST                'self'
               12  CALL_METHOD_1         1  '1 positional argument'
               14  POP_TOP          

 L.2027        16  LOAD_GLOBAL              hex
               18  LOAD_GLOBAL              long
               20  LOAD_GLOBAL              id
               22  LOAD_FAST                'self'
               24  CALL_FUNCTION_1       1  '1 positional argument'
               26  CALL_FUNCTION_1       1  '1 positional argument'
               28  LOAD_GLOBAL              xffffffff
               30  BINARY_AND       
               32  CALL_FUNCTION_1       1  '1 positional argument'
               34  STORE_FAST               'tid'

 L.2028        36  LOAD_FAST                'self'
               38  LOAD_ATTR                server_mode
               40  POP_JUMP_IF_FALSE    62  'to 62'

 L.2029        42  LOAD_FAST                'self'
               44  LOAD_METHOD              _log
               46  LOAD_GLOBAL              DEBUG
               48  LOAD_STR                 'starting thread (server mode): {}'
               50  LOAD_METHOD              format
               52  LOAD_FAST                'tid'
               54  CALL_METHOD_1         1  '1 positional argument'
               56  CALL_METHOD_2         2  '2 positional arguments'
               58  POP_TOP          
               60  JUMP_FORWARD         80  'to 80'
             62_0  COME_FROM            40  '40'

 L.2031        62  LOAD_FAST                'self'
               64  LOAD_METHOD              _log
               66  LOAD_GLOBAL              DEBUG
               68  LOAD_STR                 'starting thread (client mode): {}'
               70  LOAD_METHOD              format
               72  LOAD_FAST                'tid'
               74  CALL_METHOD_1         1  '1 positional argument'
               76  CALL_METHOD_2         2  '2 positional arguments'
               78  POP_TOP          
             80_0  COME_FROM            60  '60'

 L.2032     80_82  SETUP_EXCEPT       1280  'to 1280'

 L.2033     84_86  SETUP_EXCEPT        744  'to 744'

 L.2034        88  LOAD_FAST                'self'
               90  LOAD_ATTR                packetizer
               92  LOAD_METHOD              write_all
               94  LOAD_GLOBAL              b
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                local_version
              100  LOAD_STR                 '\r\n'
              102  BINARY_ADD       
              104  CALL_FUNCTION_1       1  '1 positional argument'
              106  CALL_METHOD_1         1  '1 positional argument'
              108  POP_TOP          

 L.2035       110  LOAD_FAST                'self'
              112  LOAD_METHOD              _log

 L.2036       114  LOAD_GLOBAL              DEBUG

 L.2037       116  LOAD_STR                 'Local version/idstring: {}'
              118  LOAD_METHOD              format
              120  LOAD_FAST                'self'
              122  LOAD_ATTR                local_version
              124  CALL_METHOD_1         1  '1 positional argument'
              126  CALL_METHOD_2         2  '2 positional arguments'
              128  POP_TOP          

 L.2039       130  LOAD_FAST                'self'
              132  LOAD_METHOD              _check_banner
              134  CALL_METHOD_0         0  '0 positional arguments'
              136  POP_TOP          

 L.2047       138  LOAD_FAST                'self'
              140  LOAD_ATTR                packetizer
              142  LOAD_METHOD              start_handshake
              144  LOAD_FAST                'self'
              146  LOAD_ATTR                handshake_timeout
              148  CALL_METHOD_1         1  '1 positional argument'
              150  POP_TOP          

 L.2048       152  LOAD_FAST                'self'
              154  LOAD_METHOD              _send_kex_init
              156  CALL_METHOD_0         0  '0 positional arguments'
              158  POP_TOP          

 L.2049       160  LOAD_FAST                'self'
              162  LOAD_METHOD              _expect_packet
              164  LOAD_GLOBAL              MSG_KEXINIT
              166  CALL_METHOD_1         1  '1 positional argument'
              168  POP_TOP          

 L.2051   170_172  SETUP_LOOP          738  'to 738'
              174  LOAD_FAST                'self'
              176  LOAD_ATTR                active
          178_180  POP_JUMP_IF_FALSE   736  'to 736'

 L.2052       182  LOAD_FAST                'self'
              184  LOAD_ATTR                packetizer
              186  LOAD_METHOD              need_rekey
              188  CALL_METHOD_0         0  '0 positional arguments'
              190  POP_JUMP_IF_FALSE   206  'to 206'
              192  LOAD_FAST                'self'
              194  LOAD_ATTR                in_kex
              196  POP_JUMP_IF_TRUE    206  'to 206'

 L.2053       198  LOAD_FAST                'self'
              200  LOAD_METHOD              _send_kex_init
              202  CALL_METHOD_0         0  '0 positional arguments'
              204  POP_TOP          
            206_0  COME_FROM           196  '196'
            206_1  COME_FROM           190  '190'

 L.2054       206  SETUP_EXCEPT        226  'to 226'

 L.2055       208  LOAD_FAST                'self'
              210  LOAD_ATTR                packetizer
              212  LOAD_METHOD              read_message
              214  CALL_METHOD_0         0  '0 positional arguments'
              216  UNPACK_SEQUENCE_2     2 
              218  STORE_FAST               'ptype'
              220  STORE_FAST               'm'
              222  POP_BLOCK        
              224  JUMP_FORWARD        248  'to 248'
            226_0  COME_FROM_EXCEPT    206  '206'

 L.2056       226  DUP_TOP          
              228  LOAD_GLOBAL              NeedRekeyException
              230  COMPARE_OP               exception-match
              232  POP_JUMP_IF_FALSE   246  'to 246'
              234  POP_TOP          
              236  POP_TOP          
              238  POP_TOP          

 L.2057       240  CONTINUE_LOOP       174  'to 174'
              242  POP_EXCEPT       
              244  JUMP_FORWARD        248  'to 248'
            246_0  COME_FROM           232  '232'
              246  END_FINALLY      
            248_0  COME_FROM           244  '244'
            248_1  COME_FROM           224  '224'

 L.2058       248  LOAD_FAST                'ptype'
              250  LOAD_GLOBAL              MSG_IGNORE
              252  COMPARE_OP               ==
          254_256  POP_JUMP_IF_FALSE   262  'to 262'

 L.2059       258  CONTINUE            174  'to 174'
              260  JUMP_FORWARD        308  'to 308'
            262_0  COME_FROM           254  '254'

 L.2060       262  LOAD_FAST                'ptype'
              264  LOAD_GLOBAL              MSG_DISCONNECT
              266  COMPARE_OP               ==
          268_270  POP_JUMP_IF_FALSE   286  'to 286'

 L.2061       272  LOAD_FAST                'self'
              274  LOAD_METHOD              _parse_disconnect
              276  LOAD_FAST                'm'
              278  CALL_METHOD_1         1  '1 positional argument'
              280  POP_TOP          

 L.2062       282  BREAK_LOOP       
              284  JUMP_FORWARD        308  'to 308'
            286_0  COME_FROM           268  '268'

 L.2063       286  LOAD_FAST                'ptype'
              288  LOAD_GLOBAL              MSG_DEBUG
              290  COMPARE_OP               ==
          292_294  POP_JUMP_IF_FALSE   308  'to 308'

 L.2064       296  LOAD_FAST                'self'
              298  LOAD_METHOD              _parse_debug
              300  LOAD_FAST                'm'
              302  CALL_METHOD_1         1  '1 positional argument'
              304  POP_TOP          

 L.2065       306  CONTINUE            174  'to 174'
            308_0  COME_FROM           292  '292'
            308_1  COME_FROM           284  '284'
            308_2  COME_FROM           260  '260'

 L.2066       308  LOAD_GLOBAL              len
              310  LOAD_FAST                'self'
              312  LOAD_ATTR                _expected_packet
              314  CALL_FUNCTION_1       1  '1 positional argument'
              316  LOAD_CONST               0
              318  COMPARE_OP               >
          320_322  POP_JUMP_IF_FALSE   398  'to 398'

 L.2067       324  LOAD_FAST                'ptype'
              326  LOAD_FAST                'self'
              328  LOAD_ATTR                _expected_packet
              330  COMPARE_OP               not-in
          332_334  POP_JUMP_IF_FALSE   354  'to 354'

 L.2068       336  LOAD_GLOBAL              SSHException

 L.2069       338  LOAD_STR                 'Expecting packet from {!r}, got {:d}'
              340  LOAD_METHOD              format

 L.2070       342  LOAD_FAST                'self'
              344  LOAD_ATTR                _expected_packet
              346  LOAD_FAST                'ptype'
              348  CALL_METHOD_2         2  '2 positional arguments'
              350  CALL_FUNCTION_1       1  '1 positional argument'
              352  RAISE_VARARGS_1       1  'exception instance'
            354_0  COME_FROM           332  '332'

 L.2073       354  LOAD_GLOBAL              tuple
              356  CALL_FUNCTION_0       0  '0 positional arguments'
              358  LOAD_FAST                'self'
              360  STORE_ATTR               _expected_packet

 L.2074       362  LOAD_FAST                'ptype'
              364  LOAD_CONST               30
              366  COMPARE_OP               >=
          368_370  POP_JUMP_IF_FALSE   398  'to 398'
              372  LOAD_FAST                'ptype'
              374  LOAD_CONST               41
              376  COMPARE_OP               <=
          378_380  POP_JUMP_IF_FALSE   398  'to 398'

 L.2075       382  LOAD_FAST                'self'
              384  LOAD_ATTR                kex_engine
              386  LOAD_METHOD              parse_next
              388  LOAD_FAST                'ptype'
              390  LOAD_FAST                'm'
              392  CALL_METHOD_2         2  '2 positional arguments'
              394  POP_TOP          

 L.2076       396  CONTINUE            174  'to 174'
            398_0  COME_FROM           378  '378'
            398_1  COME_FROM           368  '368'
            398_2  COME_FROM           320  '320'

 L.2078       398  LOAD_FAST                'ptype'
              400  LOAD_FAST                'self'
              402  LOAD_ATTR                _handler_table
              404  COMPARE_OP               in
          406_408  POP_JUMP_IF_FALSE   460  'to 460'

 L.2079       410  LOAD_FAST                'self'
              412  LOAD_METHOD              _ensure_authed
              414  LOAD_FAST                'ptype'
              416  LOAD_FAST                'm'
              418  CALL_METHOD_2         2  '2 positional arguments'
              420  STORE_FAST               'error_msg'

 L.2080       422  LOAD_FAST                'error_msg'
          424_426  POP_JUMP_IF_FALSE   440  'to 440'

 L.2081       428  LOAD_FAST                'self'
              430  LOAD_METHOD              _send_message
              432  LOAD_FAST                'error_msg'
              434  CALL_METHOD_1         1  '1 positional argument'
              436  POP_TOP          
              438  JUMP_FORWARD        724  'to 724'
            440_0  COME_FROM           424  '424'

 L.2083       440  LOAD_FAST                'self'
              442  LOAD_ATTR                _handler_table
              444  LOAD_FAST                'ptype'
              446  BINARY_SUBSCR    
              448  LOAD_FAST                'self'
              450  LOAD_FAST                'm'
              452  CALL_FUNCTION_2       2  '2 positional arguments'
              454  POP_TOP          
          456_458  JUMP_FORWARD        724  'to 724'
            460_0  COME_FROM           406  '406'

 L.2084       460  LOAD_FAST                'ptype'
              462  LOAD_FAST                'self'
              464  LOAD_ATTR                _channel_handler_table
              466  COMPARE_OP               in
          468_470  POP_JUMP_IF_FALSE   574  'to 574'

 L.2085       472  LOAD_FAST                'm'
              474  LOAD_METHOD              get_int
              476  CALL_METHOD_0         0  '0 positional arguments'
              478  STORE_FAST               'chanid'

 L.2086       480  LOAD_FAST                'self'
              482  LOAD_ATTR                _channels
              484  LOAD_METHOD              get
              486  LOAD_FAST                'chanid'
              488  CALL_METHOD_1         1  '1 positional argument'
              490  STORE_FAST               'chan'

 L.2087       492  LOAD_FAST                'chan'
              494  LOAD_CONST               None
              496  COMPARE_OP               is-not
          498_500  POP_JUMP_IF_FALSE   520  'to 520'

 L.2088       502  LOAD_FAST                'self'
              504  LOAD_ATTR                _channel_handler_table
              506  LOAD_FAST                'ptype'
              508  BINARY_SUBSCR    
              510  LOAD_FAST                'chan'
              512  LOAD_FAST                'm'
              514  CALL_FUNCTION_2       2  '2 positional arguments'
              516  POP_TOP          
              518  JUMP_FORWARD        572  'to 572'
            520_0  COME_FROM           498  '498'

 L.2089       520  LOAD_FAST                'chanid'
              522  LOAD_FAST                'self'
              524  LOAD_ATTR                channels_seen
              526  COMPARE_OP               in
          528_530  POP_JUMP_IF_FALSE   552  'to 552'

 L.2090       532  LOAD_FAST                'self'
              534  LOAD_METHOD              _log

 L.2091       536  LOAD_GLOBAL              DEBUG

 L.2092       538  LOAD_STR                 'Ignoring message for dead channel {:d}'
              540  LOAD_METHOD              format

 L.2093       542  LOAD_FAST                'chanid'
              544  CALL_METHOD_1         1  '1 positional argument'
              546  CALL_METHOD_2         2  '2 positional arguments'
              548  POP_TOP          
              550  JUMP_FORWARD        572  'to 572'
            552_0  COME_FROM           528  '528'

 L.2097       552  LOAD_FAST                'self'
              554  LOAD_METHOD              _log

 L.2098       556  LOAD_GLOBAL              ERROR

 L.2099       558  LOAD_STR                 'Channel request for unknown channel {:d}'
              560  LOAD_METHOD              format

 L.2100       562  LOAD_FAST                'chanid'
              564  CALL_METHOD_1         1  '1 positional argument'
              566  CALL_METHOD_2         2  '2 positional arguments'
              568  POP_TOP          

 L.2103       570  BREAK_LOOP       
            572_0  COME_FROM           550  '550'
            572_1  COME_FROM           518  '518'
              572  JUMP_FORWARD        724  'to 724'
            574_0  COME_FROM           468  '468'

 L.2105       574  LOAD_FAST                'self'
              576  LOAD_ATTR                auth_handler
              578  LOAD_CONST               None
              580  COMPARE_OP               is-not
          582_584  POP_JUMP_IF_FALSE   644  'to 644'

 L.2106       586  LOAD_FAST                'ptype'
              588  LOAD_FAST                'self'
              590  LOAD_ATTR                auth_handler
              592  LOAD_ATTR                _handler_table
              594  COMPARE_OP               in
          596_598  POP_JUMP_IF_FALSE   644  'to 644'

 L.2108       600  LOAD_FAST                'self'
              602  LOAD_ATTR                auth_handler
              604  LOAD_ATTR                _handler_table
              606  LOAD_FAST                'ptype'
              608  BINARY_SUBSCR    
              610  STORE_FAST               'handler'

 L.2109       612  LOAD_FAST                'handler'
              614  LOAD_FAST                'self'
              616  LOAD_ATTR                auth_handler
              618  LOAD_FAST                'm'
              620  CALL_FUNCTION_2       2  '2 positional arguments'
              622  POP_TOP          

 L.2110       624  LOAD_GLOBAL              len
              626  LOAD_FAST                'self'
              628  LOAD_ATTR                _expected_packet
              630  CALL_FUNCTION_1       1  '1 positional argument'
              632  LOAD_CONST               0
              634  COMPARE_OP               >
          636_638  POP_JUMP_IF_FALSE   724  'to 724'

 L.2111       640  CONTINUE            174  'to 174'
              642  JUMP_FORWARD        724  'to 724'
            644_0  COME_FROM           596  '596'
            644_1  COME_FROM           582  '582'

 L.2117       644  LOAD_GLOBAL              MSG_NAMES
              646  LOAD_FAST                'ptype'
              648  BINARY_SUBSCR    
              650  STORE_FAST               'name'

 L.2118       652  LOAD_STR                 'Oops, unhandled type {} ({!r})'
              654  LOAD_METHOD              format

 L.2119       656  LOAD_FAST                'ptype'
              658  LOAD_FAST                'name'
              660  CALL_METHOD_2         2  '2 positional arguments'
              662  STORE_FAST               'warning'

 L.2121       664  LOAD_FAST                'self'
              666  LOAD_METHOD              _log
              668  LOAD_GLOBAL              WARNING
              670  LOAD_FAST                'warning'
              672  CALL_METHOD_2         2  '2 positional arguments'
              674  POP_TOP          

 L.2122       676  LOAD_FAST                'ptype'
              678  LOAD_GLOBAL              MSG_UNIMPLEMENTED
              680  COMPARE_OP               !=
          682_684  POP_JUMP_IF_FALSE   724  'to 724'

 L.2123       686  LOAD_GLOBAL              Message
              688  CALL_FUNCTION_0       0  '0 positional arguments'
              690  STORE_FAST               'msg'

 L.2124       692  LOAD_FAST                'msg'
              694  LOAD_METHOD              add_byte
              696  LOAD_GLOBAL              cMSG_UNIMPLEMENTED
              698  CALL_METHOD_1         1  '1 positional argument'
              700  POP_TOP          

 L.2125       702  LOAD_FAST                'msg'
            704_0  COME_FROM           438  '438'
              704  LOAD_METHOD              add_int
              706  LOAD_FAST                'm'
              708  LOAD_ATTR                seqno
              710  CALL_METHOD_1         1  '1 positional argument'
              712  POP_TOP          

 L.2126       714  LOAD_FAST                'self'
              716  LOAD_METHOD              _send_message
              718  LOAD_FAST                'msg'
              720  CALL_METHOD_1         1  '1 positional argument'
              722  POP_TOP          
            724_0  COME_FROM           682  '682'
            724_1  COME_FROM           642  '642'
            724_2  COME_FROM           636  '636'
            724_3  COME_FROM           572  '572'
            724_4  COME_FROM           456  '456'

 L.2127       724  LOAD_FAST                'self'
              726  LOAD_ATTR                packetizer
              728  LOAD_METHOD              complete_handshake
              730  CALL_METHOD_0         0  '0 positional arguments'
              732  POP_TOP          
              734  JUMP_BACK           174  'to 174'
            736_0  COME_FROM           178  '178'
              736  POP_BLOCK        
            738_0  COME_FROM_LOOP      170  '170'
              738  POP_BLOCK        
          740_742  JUMP_FORWARD       1086  'to 1086'
            744_0  COME_FROM_EXCEPT     84  '84'

 L.2128       744  DUP_TOP          
              746  LOAD_GLOBAL              SSHException
              748  COMPARE_OP               exception-match
          750_752  POP_JUMP_IF_FALSE   822  'to 822'
              754  POP_TOP          
              756  STORE_FAST               'e'
              758  POP_TOP          
              760  SETUP_FINALLY       808  'to 808'

 L.2129       762  LOAD_FAST                'self'
              764  LOAD_METHOD              _log
              766  LOAD_GLOBAL              ERROR
              768  LOAD_STR                 'Exception: '
              770  LOAD_GLOBAL              str
              772  LOAD_FAST                'e'
              774  CALL_FUNCTION_1       1  '1 positional argument'
              776  BINARY_ADD       
              778  CALL_METHOD_2         2  '2 positional arguments'
              780  POP_TOP          

 L.2130       782  LOAD_FAST                'self'
              784  LOAD_METHOD              _log
              786  LOAD_GLOBAL              ERROR
              788  LOAD_GLOBAL              util
              790  LOAD_METHOD              tb_strings
              792  CALL_METHOD_0         0  '0 positional arguments'
              794  CALL_METHOD_2         2  '2 positional arguments'
              796  POP_TOP          

 L.2131       798  LOAD_FAST                'e'
              800  LOAD_FAST                'self'
              802  STORE_ATTR               saved_exception
              804  POP_BLOCK        
              806  LOAD_CONST               None
            808_0  COME_FROM_FINALLY   760  '760'
              808  LOAD_CONST               None
              810  STORE_FAST               'e'
              812  DELETE_FAST              'e'
              814  END_FINALLY      
              816  POP_EXCEPT       
          818_820  JUMP_FORWARD       1086  'to 1086'
            822_0  COME_FROM           750  '750'

 L.2132       822  DUP_TOP          
              824  LOAD_GLOBAL              EOFError
              826  COMPARE_OP               exception-match
          828_830  POP_JUMP_IF_FALSE   874  'to 874'
              832  POP_TOP          
              834  STORE_FAST               'e'
              836  POP_TOP          
              838  SETUP_FINALLY       862  'to 862'

 L.2133       840  LOAD_FAST                'self'
              842  LOAD_METHOD              _log
              844  LOAD_GLOBAL              DEBUG
              846  LOAD_STR                 'EOF in transport thread'
              848  CALL_METHOD_2         2  '2 positional arguments'
              850  POP_TOP          

 L.2134       852  LOAD_FAST                'e'
              854  LOAD_FAST                'self'
              856  STORE_ATTR               saved_exception
              858  POP_BLOCK        
              860  LOAD_CONST               None
            862_0  COME_FROM_FINALLY   838  '838'
              862  LOAD_CONST               None
              864  STORE_FAST               'e'
              866  DELETE_FAST              'e'
              868  END_FINALLY      
              870  POP_EXCEPT       
              872  JUMP_FORWARD       1086  'to 1086'
            874_0  COME_FROM           828  '828'

 L.2135       874  DUP_TOP          
              876  LOAD_GLOBAL              socket
              878  LOAD_ATTR                error
              880  COMPARE_OP               exception-match
          882_884  POP_JUMP_IF_FALSE  1008  'to 1008'
              886  POP_TOP          
              888  STORE_FAST               'e'
              890  POP_TOP          
              892  SETUP_FINALLY       996  'to 996'

 L.2136       894  LOAD_GLOBAL              type
              896  LOAD_FAST                'e'
              898  LOAD_ATTR                args
              900  CALL_FUNCTION_1       1  '1 positional argument'
              902  LOAD_GLOBAL              tuple
              904  COMPARE_OP               is
          906_908  POP_JUMP_IF_FALSE   964  'to 964'

 L.2137       910  LOAD_FAST                'e'
              912  LOAD_ATTR                args
          914_916  POP_JUMP_IF_FALSE   944  'to 944'

 L.2138       918  LOAD_STR                 '{} ({:d})'
              920  LOAD_METHOD              format
              922  LOAD_FAST                'e'
              924  LOAD_ATTR                args
              926  LOAD_CONST               1
              928  BINARY_SUBSCR    
              930  LOAD_FAST                'e'
              932  LOAD_ATTR                args
              934  LOAD_CONST               0
              936  BINARY_SUBSCR    
              938  CALL_METHOD_2         2  '2 positional arguments'
              940  STORE_FAST               'emsg'
              942  JUMP_FORWARD        962  'to 962'
            944_0  COME_FROM           914  '914'

 L.2140       944  LOAD_GLOBAL              str
              946  LOAD_FAST                'e'
              948  CALL_FUNCTION_1       1  '1 positional argument'
          950_952  JUMP_IF_TRUE_OR_POP   960  'to 960'
              954  LOAD_GLOBAL              repr
              956  LOAD_FAST                'e'
              958  CALL_FUNCTION_1       1  '1 positional argument'
            960_0  COME_FROM           950  '950'
              960  STORE_FAST               'emsg'
            962_0  COME_FROM           942  '942'
              962  JUMP_FORWARD        970  'to 970'
            964_0  COME_FROM           906  '906'

 L.2142       964  LOAD_FAST                'e'
              966  LOAD_ATTR                args
              968  STORE_FAST               'emsg'
            970_0  COME_FROM           962  '962'

 L.2143       970  LOAD_FAST                'self'
              972  LOAD_METHOD              _log
              974  LOAD_GLOBAL              ERROR
              976  LOAD_STR                 'Socket exception: '
              978  LOAD_FAST                'emsg'
              980  BINARY_ADD       
              982  CALL_METHOD_2         2  '2 positional arguments'
              984  POP_TOP          

 L.2144       986  LOAD_FAST                'e'
              988  LOAD_FAST                'self'
              990  STORE_ATTR               saved_exception
              992  POP_BLOCK        
              994  LOAD_CONST               None
            996_0  COME_FROM_FINALLY   892  '892'
              996  LOAD_CONST               None
              998  STORE_FAST               'e'
             1000  DELETE_FAST              'e'
             1002  END_FINALLY      
             1004  POP_EXCEPT       
             1006  JUMP_FORWARD       1086  'to 1086'
           1008_0  COME_FROM           882  '882'

 L.2145      1008  DUP_TOP          
             1010  LOAD_GLOBAL              Exception
             1012  COMPARE_OP               exception-match
         1014_1016  POP_JUMP_IF_FALSE  1084  'to 1084'
             1018  POP_TOP          
             1020  STORE_FAST               'e'
             1022  POP_TOP          
             1024  SETUP_FINALLY      1072  'to 1072'

 L.2146      1026  LOAD_FAST                'self'
             1028  LOAD_METHOD              _log
             1030  LOAD_GLOBAL              ERROR
             1032  LOAD_STR                 'Unknown exception: '
             1034  LOAD_GLOBAL              str
             1036  LOAD_FAST                'e'
             1038  CALL_FUNCTION_1       1  '1 positional argument'
             1040  BINARY_ADD       
             1042  CALL_METHOD_2         2  '2 positional arguments'
             1044  POP_TOP          

 L.2147      1046  LOAD_FAST                'self'
             1048  LOAD_METHOD              _log
             1050  LOAD_GLOBAL              ERROR
             1052  LOAD_GLOBAL              util
             1054  LOAD_METHOD              tb_strings
             1056  CALL_METHOD_0         0  '0 positional arguments'
             1058  CALL_METHOD_2         2  '2 positional arguments'
             1060  POP_TOP          

 L.2148      1062  LOAD_FAST                'e'
             1064  LOAD_FAST                'self'
             1066  STORE_ATTR               saved_exception
             1068  POP_BLOCK        
             1070  LOAD_CONST               None
           1072_0  COME_FROM_FINALLY  1024  '1024'
             1072  LOAD_CONST               None
             1074  STORE_FAST               'e'
             1076  DELETE_FAST              'e'
             1078  END_FINALLY      
             1080  POP_EXCEPT       
             1082  JUMP_FORWARD       1086  'to 1086'
           1084_0  COME_FROM          1014  '1014'
             1084  END_FINALLY      
           1086_0  COME_FROM          1082  '1082'
           1086_1  COME_FROM          1006  '1006'
           1086_2  COME_FROM           872  '872'
           1086_3  COME_FROM           818  '818'
           1086_4  COME_FROM           740  '740'

 L.2149      1086  LOAD_GLOBAL              _active_threads
             1088  LOAD_METHOD              remove
             1090  LOAD_FAST                'self'
             1092  CALL_METHOD_1         1  '1 positional argument'
             1094  POP_TOP          

 L.2150      1096  SETUP_LOOP         1130  'to 1130'
             1098  LOAD_GLOBAL              list
             1100  LOAD_FAST                'self'
             1102  LOAD_ATTR                _channels
             1104  LOAD_METHOD              values
             1106  CALL_METHOD_0         0  '0 positional arguments'
             1108  CALL_FUNCTION_1       1  '1 positional argument'
             1110  GET_ITER         
             1112  FOR_ITER           1128  'to 1128'
             1114  STORE_FAST               'chan'

 L.2151      1116  LOAD_FAST                'chan'
             1118  LOAD_METHOD              _unlink
             1120  CALL_METHOD_0         0  '0 positional arguments'
             1122  POP_TOP          
         1124_1126  JUMP_BACK          1112  'to 1112'
             1128  POP_BLOCK        
           1130_0  COME_FROM_LOOP     1096  '1096'

 L.2152      1130  LOAD_FAST                'self'
             1132  LOAD_ATTR                active
         1134_1136  POP_JUMP_IF_FALSE  1266  'to 1266'

 L.2153      1138  LOAD_CONST               False
             1140  LOAD_FAST                'self'
             1142  STORE_ATTR               active

 L.2154      1144  LOAD_FAST                'self'
             1146  LOAD_ATTR                packetizer
             1148  LOAD_METHOD              close
             1150  CALL_METHOD_0         0  '0 positional arguments'
             1152  POP_TOP          

 L.2155      1154  LOAD_FAST                'self'
             1156  LOAD_ATTR                completion_event
             1158  LOAD_CONST               None
             1160  COMPARE_OP               is-not
         1162_1164  POP_JUMP_IF_FALSE  1176  'to 1176'

 L.2156      1166  LOAD_FAST                'self'
             1168  LOAD_ATTR                completion_event
             1170  LOAD_METHOD              set
             1172  CALL_METHOD_0         0  '0 positional arguments'
             1174  POP_TOP          
           1176_0  COME_FROM          1162  '1162'

 L.2157      1176  LOAD_FAST                'self'
             1178  LOAD_ATTR                auth_handler
             1180  LOAD_CONST               None
             1182  COMPARE_OP               is-not
         1184_1186  POP_JUMP_IF_FALSE  1198  'to 1198'

 L.2158      1188  LOAD_FAST                'self'
             1190  LOAD_ATTR                auth_handler
             1192  LOAD_METHOD              abort
             1194  CALL_METHOD_0         0  '0 positional arguments'
             1196  POP_TOP          
           1198_0  COME_FROM          1184  '1184'

 L.2159      1198  SETUP_LOOP         1228  'to 1228'
             1200  LOAD_FAST                'self'
             1202  LOAD_ATTR                channel_events
             1204  LOAD_METHOD              values
             1206  CALL_METHOD_0         0  '0 positional arguments'
             1208  GET_ITER         
             1210  FOR_ITER           1226  'to 1226'
             1212  STORE_FAST               'event'

 L.2160      1214  LOAD_FAST                'event'
             1216  LOAD_METHOD              set
             1218  CALL_METHOD_0         0  '0 positional arguments'
             1220  POP_TOP          
         1222_1224  JUMP_BACK          1210  'to 1210'
             1226  POP_BLOCK        
           1228_0  COME_FROM_LOOP     1198  '1198'

 L.2161      1228  SETUP_FINALLY      1254  'to 1254'

 L.2162      1230  LOAD_FAST                'self'
             1232  LOAD_ATTR                lock
             1234  LOAD_METHOD              acquire
             1236  CALL_METHOD_0         0  '0 positional arguments'
             1238  POP_TOP          

 L.2163      1240  LOAD_FAST                'self'
             1242  LOAD_ATTR                server_accept_cv
             1244  LOAD_METHOD              notify
             1246  CALL_METHOD_0         0  '0 positional arguments'
             1248  POP_TOP          
             1250  POP_BLOCK        
             1252  LOAD_CONST               None
           1254_0  COME_FROM_FINALLY  1228  '1228'

 L.2165      1254  LOAD_FAST                'self'
             1256  LOAD_ATTR                lock
             1258  LOAD_METHOD              release
             1260  CALL_METHOD_0         0  '0 positional arguments'
             1262  POP_TOP          
             1264  END_FINALLY      
           1266_0  COME_FROM          1134  '1134'

 L.2166      1266  LOAD_FAST                'self'
             1268  LOAD_ATTR                sock
             1270  LOAD_METHOD              close
             1272  CALL_METHOD_0         0  '0 positional arguments'
             1274  POP_TOP          
             1276  POP_BLOCK        
             1278  JUMP_FORWARD       1308  'to 1308'
           1280_0  COME_FROM_EXCEPT     80  '80'

 L.2167      1280  POP_TOP          
             1282  POP_TOP          
             1284  POP_TOP          

 L.2172      1286  LOAD_FAST                'self'
             1288  LOAD_ATTR                sys
             1290  LOAD_ATTR                modules
             1292  LOAD_CONST               None
             1294  COMPARE_OP               is-not
         1296_1298  POP_JUMP_IF_FALSE  1302  'to 1302'

 L.2173      1300  RAISE_VARARGS_0       0  'reraise'
           1302_0  COME_FROM          1296  '1296'
             1302  POP_EXCEPT       
             1304  JUMP_FORWARD       1308  'to 1308'
             1306  END_FINALLY      
           1308_0  COME_FROM          1304  '1304'
           1308_1  COME_FROM          1278  '1278'

Parse error at or near `LOAD_METHOD' instruction at offset 704

    def _log_agreement(self, which, local, remote):
        msg = '{} agreed: '.format(which)
        if local == remote:
            msg += local
        else:
            msg += 'local={}, remote={}'.format(local, remote)
        self._log(DEBUG, msg)

    def _negotiate_keys(self, m):
        self.clear_to_send_lock.acquire()
        try:
            self.clear_to_send.clear()
        finally:
            self.clear_to_send_lock.release()

        if self.local_kex_init is None:
            self._send_kex_init()
        self._parse_kex_init(m)
        self.kex_engine.start_kex()

    def _check_banner(self):
        for i in range(100):
            if i == 0:
                timeout = self.banner_timeout
            else:
                timeout = 2
            try:
                buf = self.packetizer.readline(timeout)
            except ProxyCommandFailure:
                raise
            except Exception as e:
                try:
                    raise SSHException('Error reading SSH protocol banner' + str(e))
                finally:
                    e = None
                    del e

            if buf[:4] == 'SSH-':
                break
            self._log(DEBUG, 'Banner: ' + buf)

        if buf[:4] != 'SSH-':
            raise SSHException('Indecipherable protocol version "' + buf + '"')
        self.remote_version = buf
        self._log(DEBUG, 'Remote version/idstring: {}'.format(buf))
        i = buf.find(' ')
        if i >= 0:
            buf = buf[:i]
        segs = buf.split('-', 2)
        if len(segs) < 3:
            raise SSHException('Invalid SSH banner')
        version = segs[1]
        client = segs[2]
        if version != '1.99':
            if version != '2.0':
                msg = 'Incompatible version ({} instead of 2.0)'
                raise SSHException(msg.format(version))
        msg = 'Connected (version {}, client {})'.format(version, client)
        self._log(INFO, msg)

    def _send_kex_init(self):
        """
        announce to the other side that we'd like to negotiate keys, and what
        kind of key negotiation we support.
        """
        self.clear_to_send_lock.acquire()
        try:
            self.clear_to_send.clear()
        finally:
            self.clear_to_send_lock.release()

        self.gss_kex_used = False
        self.in_kex = True
        if self.server_mode:
            mp_required_prefix = 'diffie-hellman-group-exchange-sha'
            kex_mp = [k for k in self.preferred_kex if k.startswith(mp_required_prefix)]
            if self._modulus_pack is None:
                if len(kex_mp) > 0:
                    pkex = [k for k in self.get_security_options().kex if not k.startswith(mp_required_prefix)]
                    self.get_security_options().kex = pkex
            available_server_keys = list(filter(list(self.server_key_dict.keys()).__contains__, self.preferred_keys))
        else:
            available_server_keys = self.preferred_keys
        m = Message()
        m.add_byte(cMSG_KEXINIT)
        m.add_bytes(os.urandom(16))
        m.add_list(self.preferred_kex)
        m.add_list(available_server_keys)
        m.add_list(self.preferred_ciphers)
        m.add_list(self.preferred_ciphers)
        m.add_list(self.preferred_macs)
        m.add_list(self.preferred_macs)
        m.add_list(self.preferred_compression)
        m.add_list(self.preferred_compression)
        m.add_string(bytes())
        m.add_string(bytes())
        m.add_boolean(False)
        m.add_int(0)
        self.local_kex_init = m.asbytes()
        self._send_message(m)

    def _parse_kex_init(self, m):
        m.get_bytes(16)
        kex_algo_list = m.get_list()
        server_key_algo_list = m.get_list()
        client_encrypt_algo_list = m.get_list()
        server_encrypt_algo_list = m.get_list()
        client_mac_algo_list = m.get_list()
        server_mac_algo_list = m.get_list()
        client_compress_algo_list = m.get_list()
        server_compress_algo_list = m.get_list()
        client_lang_list = m.get_list()
        server_lang_list = m.get_list()
        kex_follows = m.get_boolean()
        m.get_int()
        self._log(DEBUG, 'kex algos:' + str(kex_algo_list) + ' server key:' + str(server_key_algo_list) + ' client encrypt:' + str(client_encrypt_algo_list) + ' server encrypt:' + str(server_encrypt_algo_list) + ' client mac:' + str(client_mac_algo_list) + ' server mac:' + str(server_mac_algo_list) + ' client compress:' + str(client_compress_algo_list) + ' server compress:' + str(server_compress_algo_list) + ' client lang:' + str(client_lang_list) + ' server lang:' + str(server_lang_list) + ' kex follows?' + str(kex_follows))
        if self.server_mode:
            agreed_kex = list(filter(self.preferred_kex.__contains__, kex_algo_list))
        else:
            agreed_kex = list(filter(kex_algo_list.__contains__, self.preferred_kex))
        if len(agreed_kex) == 0:
            raise SSHException('Incompatible ssh peer (no acceptable kex algorithm)')
        else:
            self.kex_engine = self._kex_info[agreed_kex[0]](self)
            self._log(DEBUG, 'Kex agreed: {}'.format(agreed_kex[0]))
            if self.server_mode:
                available_server_keys = list(filter(list(self.server_key_dict.keys()).__contains__, self.preferred_keys))
                agreed_keys = list(filter(available_server_keys.__contains__, server_key_algo_list))
            else:
                agreed_keys = list(filter(server_key_algo_list.__contains__, self.preferred_keys))
        if len(agreed_keys) == 0:
            raise SSHException('Incompatible ssh peer (no acceptable host key)')
        self.host_key_type = agreed_keys[0]
        if self.server_mode:
            if self.get_server_key() is None:
                raise SSHException("Incompatible ssh peer (can't match requested host key type)")
        self._log_agreement('HostKey', agreed_keys[0], agreed_keys[0])
        if self.server_mode:
            agreed_local_ciphers = list(filter(self.preferred_ciphers.__contains__, server_encrypt_algo_list))
            agreed_remote_ciphers = list(filter(self.preferred_ciphers.__contains__, client_encrypt_algo_list))
        else:
            agreed_local_ciphers = list(filter(client_encrypt_algo_list.__contains__, self.preferred_ciphers))
            agreed_remote_ciphers = list(filter(server_encrypt_algo_list.__contains__, self.preferred_ciphers))
        if len(agreed_local_ciphers) == 0 or len(agreed_remote_ciphers) == 0:
            raise SSHException('Incompatible ssh server (no acceptable ciphers)')
        self.local_cipher = agreed_local_ciphers[0]
        self.remote_cipher = agreed_remote_ciphers[0]
        self._log_agreement('Cipher',
          local=(self.local_cipher), remote=(self.remote_cipher))
        if self.server_mode:
            agreed_remote_macs = list(filter(self.preferred_macs.__contains__, client_mac_algo_list))
            agreed_local_macs = list(filter(self.preferred_macs.__contains__, server_mac_algo_list))
        else:
            agreed_local_macs = list(filter(client_mac_algo_list.__contains__, self.preferred_macs))
            agreed_remote_macs = list(filter(server_mac_algo_list.__contains__, self.preferred_macs))
        if len(agreed_local_macs) == 0 or len(agreed_remote_macs) == 0:
            raise SSHException('Incompatible ssh server (no acceptable macs)')
        self.local_mac = agreed_local_macs[0]
        self.remote_mac = agreed_remote_macs[0]
        self._log_agreement('MAC',
          local=(self.local_mac), remote=(self.remote_mac))
        if self.server_mode:
            agreed_remote_compression = list(filter(self.preferred_compression.__contains__, client_compress_algo_list))
            agreed_local_compression = list(filter(self.preferred_compression.__contains__, server_compress_algo_list))
        else:
            agreed_local_compression = list(filter(client_compress_algo_list.__contains__, self.preferred_compression))
            agreed_remote_compression = list(filter(server_compress_algo_list.__contains__, self.preferred_compression))
        if len(agreed_local_compression) == 0 or len(agreed_remote_compression) == 0:
            msg = 'Incompatible ssh server (no acceptable compression)'
            msg += ' {!r} {!r} {!r}'
            raise SSHException(msg.format(agreed_local_compression, agreed_remote_compression, self.preferred_compression))
        self.local_compression = agreed_local_compression[0]
        self.remote_compression = agreed_remote_compression[0]
        self._log_agreement('Compression',
          local=(self.local_compression),
          remote=(self.remote_compression))
        self.remote_kex_init = cMSG_KEXINIT + m.get_so_far()

    def _activate_inbound(self):
        """switch on newly negotiated encryption parameters for
         inbound traffic"""
        block_size = self._cipher_info[self.remote_cipher]['block-size']
        if self.server_mode:
            IV_in = self._compute_key('A', block_size)
            key_in = self._compute_key('C', self._cipher_info[self.remote_cipher]['key-size'])
        else:
            IV_in = self._compute_key('B', block_size)
            key_in = self._compute_key('D', self._cipher_info[self.remote_cipher]['key-size'])
        engine = self._get_cipher(self.remote_cipher, key_in, IV_in, self._DECRYPT)
        etm = 'etm@openssh.com' in self.remote_mac
        mac_size = self._mac_info[self.remote_mac]['size']
        mac_engine = self._mac_info[self.remote_mac]['class']
        if self.server_mode:
            mac_key = self._compute_key('E', mac_engine().digest_size)
        else:
            mac_key = self._compute_key('F', mac_engine().digest_size)
        self.packetizer.set_inbound_cipher(engine,
          block_size, mac_engine, mac_size, mac_key, etm=etm)
        compress_in = self._compression_info[self.remote_compression][1]
        if compress_in is not None and not self.remote_compression != 'zlib@openssh.com':
            if self.authenticated:
                self._log(DEBUG, 'Switching on inbound compression ...')
                self.packetizer.set_inbound_compressor(compress_in())

    def _activate_outbound(self):
        """switch on newly negotiated encryption parameters for
         outbound traffic"""
        m = Message()
        m.add_byte(cMSG_NEWKEYS)
        self._send_message(m)
        block_size = self._cipher_info[self.local_cipher]['block-size']
        if self.server_mode:
            IV_out = self._compute_key('B', block_size)
            key_out = self._compute_key('D', self._cipher_info[self.local_cipher]['key-size'])
        else:
            IV_out = self._compute_key('A', block_size)
            key_out = self._compute_key('C', self._cipher_info[self.local_cipher]['key-size'])
        engine = self._get_cipher(self.local_cipher, key_out, IV_out, self._ENCRYPT)
        etm = 'etm@openssh.com' in self.local_mac
        mac_size = self._mac_info[self.local_mac]['size']
        mac_engine = self._mac_info[self.local_mac]['class']
        if self.server_mode:
            mac_key = self._compute_key('F', mac_engine().digest_size)
        else:
            mac_key = self._compute_key('E', mac_engine().digest_size)
        sdctr = self.local_cipher.endswith('-ctr')
        self.packetizer.set_outbound_cipher(engine,
          block_size, mac_engine, mac_size, mac_key, sdctr, etm=etm)
        compress_out = self._compression_info[self.local_compression][0]
        if compress_out is not None and not self.local_compression != 'zlib@openssh.com':
            if self.authenticated:
                self._log(DEBUG, 'Switching on outbound compression ...')
                self.packetizer.set_outbound_compressor(compress_out())
        if not self.packetizer.need_rekey():
            self.in_kex = False
        self._expect_packet(MSG_NEWKEYS)

    def _auth_trigger(self):
        self.authenticated = True
        if self.local_compression == 'zlib@openssh.com':
            compress_out = self._compression_info[self.local_compression][0]
            self._log(DEBUG, 'Switching on outbound compression ...')
            self.packetizer.set_outbound_compressor(compress_out())
        if self.remote_compression == 'zlib@openssh.com':
            compress_in = self._compression_info[self.remote_compression][1]
            self._log(DEBUG, 'Switching on inbound compression ...')
            self.packetizer.set_inbound_compressor(compress_in())

    def _parse_newkeys(self, m):
        self._log(DEBUG, 'Switch to new keys ...')
        self._activate_inbound()
        self.local_kex_init = self.remote_kex_init = None
        self.K = None
        self.kex_engine = None
        if self.server_mode:
            if self.auth_handler is None:
                self.auth_handler = AuthHandler(self)
        if not self.initial_kex_done:
            self.initial_kex_done = True
        if self.completion_event is not None:
            self.completion_event.set()
        if not self.packetizer.need_rekey():
            self.in_kex = False
        self.clear_to_send_lock.acquire()
        try:
            self.clear_to_send.set()
        finally:
            self.clear_to_send_lock.release()

    def _parse_disconnect(self, m):
        code = m.get_int()
        desc = m.get_text()
        self._log(INFO, 'Disconnect (code {:d}): {}'.format(code, desc))

    def _parse_global_request(self, m):
        kind = m.get_text()
        self._log(DEBUG, 'Received global request "{}"'.format(kind))
        want_reply = m.get_boolean()
        if not self.server_mode:
            self._log(DEBUG, 'Rejecting "{}" global request from server.'.format(kind))
            ok = False
        else:
            if kind == 'tcpip-forward':
                address = m.get_text()
                port = m.get_int()
                ok = self.server_object.check_port_forward_request(address, port)
                if ok:
                    ok = (
                     ok,)
            elif kind == 'cancel-tcpip-forward':
                address = m.get_text()
                port = m.get_int()
                self.server_object.cancel_port_forward_request(address, port)
                ok = True
            else:
                ok = self.server_object.check_global_request(kind, m)
        extra = ()
        if type(ok) is tuple:
            extra = ok
            ok = True
        if want_reply:
            msg = Message()
            if ok:
                msg.add_byte(cMSG_REQUEST_SUCCESS)
                (msg.add)(*extra)
            else:
                msg.add_byte(cMSG_REQUEST_FAILURE)
            self._send_message(msg)

    def _parse_request_success(self, m):
        self._log(DEBUG, 'Global request successful.')
        self.global_response = m
        if self.completion_event is not None:
            self.completion_event.set()

    def _parse_request_failure(self, m):
        self._log(DEBUG, 'Global request denied.')
        self.global_response = None
        if self.completion_event is not None:
            self.completion_event.set()

    def _parse_channel_open_success(self, m):
        chanid = m.get_int()
        server_chanid = m.get_int()
        server_window_size = m.get_int()
        server_max_packet_size = m.get_int()
        chan = self._channels.get(chanid)
        if chan is None:
            self._log(WARNING, 'Success for unrequested channel! [??]')
            return
        self.lock.acquire()
        try:
            chan._set_remote_channel(server_chanid, server_window_size, server_max_packet_size)
            self._log(DEBUG, 'Secsh channel {:d} opened.'.format(chanid))
            if chanid in self.channel_events:
                self.channel_events[chanid].set()
                del self.channel_events[chanid]
        finally:
            self.lock.release()

    def _parse_channel_open_failure(self, m):
        chanid = m.get_int()
        reason = m.get_int()
        reason_str = m.get_text()
        m.get_text()
        reason_text = CONNECTION_FAILED_CODE.get(reason, '(unknown code)')
        self._log(ERROR, 'Secsh channel {:d} open FAILED: {}: {}'.format(chanid, reason_str, reason_text))
        self.lock.acquire()
        try:
            self.saved_exception = ChannelException(reason, reason_text)
            if chanid in self.channel_events:
                self._channels.delete(chanid)
                if chanid in self.channel_events:
                    self.channel_events[chanid].set()
                    del self.channel_events[chanid]
        finally:
            self.lock.release()

    def _parse_channel_open(self, m):
        kind = m.get_text()
        chanid = m.get_int()
        initial_window_size = m.get_int()
        max_packet_size = m.get_int()
        reject = False
        if kind == 'auth-agent@openssh.com' and self._forward_agent_handler is not None:
            self._log(DEBUG, 'Incoming forward agent connection')
            self.lock.acquire()
            try:
                my_chanid = self._next_channel()
            finally:
                self.lock.release()

        else:
            if kind == 'x11' and self._x11_handler is not None:
                origin_addr = m.get_text()
                origin_port = m.get_int()
                self._log(DEBUG, 'Incoming x11 connection from {}:{:d}'.format(origin_addr, origin_port))
                self.lock.acquire()
                try:
                    my_chanid = self._next_channel()
                finally:
                    self.lock.release()

            else:
                if kind == 'forwarded-tcpip' and self._tcp_handler is not None:
                    server_addr = m.get_text()
                    server_port = m.get_int()
                    origin_addr = m.get_text()
                    origin_port = m.get_int()
                    self._log(DEBUG, 'Incoming tcp forwarded connection from {}:{:d}'.format(origin_addr, origin_port))
                    self.lock.acquire()
                    try:
                        my_chanid = self._next_channel()
                    finally:
                        self.lock.release()

                else:
                    if not self.server_mode:
                        self._log(DEBUG, 'Rejecting "{}" channel request from server.'.format(kind))
                        reject = True
                        reason = OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
                    else:
                        self.lock.acquire()
                        try:
                            my_chanid = self._next_channel()
                        finally:
                            self.lock.release()

                        if kind == 'direct-tcpip':
                            dest_addr = m.get_text()
                            dest_port = m.get_int()
                            origin_addr = m.get_text()
                            origin_port = m.get_int()
                            reason = self.server_object.check_channel_direct_tcpip_request(my_chanid, (
                             origin_addr, origin_port), (
                             dest_addr, dest_port))
                        else:
                            reason = self.server_object.check_channel_request(kind, my_chanid)
        if reason != OPEN_SUCCEEDED:
            self._log(DEBUG, 'Rejecting "{}" channel request from client.'.format(kind))
            reject = True
        elif reject:
            msg = Message()
            msg.add_byte(cMSG_CHANNEL_OPEN_FAILURE)
            msg.add_int(chanid)
            msg.add_int(reason)
            msg.add_string('')
            msg.add_string('en')
            self._send_message(msg)
            return
            chan = Channel(my_chanid)
            self.lock.acquire()
            try:
                self._channels.put(my_chanid, chan)
                self.channels_seen[my_chanid] = True
                chan._set_transport(self)
                chan._set_window(self.default_window_size, self.default_max_packet_size)
                chan._set_remote_channel(chanid, initial_window_size, max_packet_size)
            finally:
                self.lock.release()

            m = Message()
            m.add_byte(cMSG_CHANNEL_OPEN_SUCCESS)
            m.add_int(chanid)
            m.add_int(my_chanid)
            m.add_int(self.default_window_size)
            m.add_int(self.default_max_packet_size)
            self._send_message(m)
            self._log(DEBUG, 'Secsh channel {:d} ({}) opened.'.format(my_chanid, kind))
            if kind == 'auth-agent@openssh.com':
                self._forward_agent_handler(chan)
        elif kind == 'x11':
            self._x11_handler(chan, (origin_addr, origin_port))
        else:
            if kind == 'forwarded-tcpip':
                chan.origin_addr = (
                 origin_addr, origin_port)
                self._tcp_handler(chan, (origin_addr, origin_port), (server_addr, server_port))
            else:
                self._queue_incoming_channel(chan)

    def _parse_debug(self, m):
        m.get_boolean()
        msg = m.get_string()
        m.get_string()
        self._log(DEBUG, 'Debug msg: {}'.format(util.safe_string(msg)))

    def _get_subsystem_handler(self, name):
        try:
            self.lock.acquire()
            if name not in self.subsystem_table:
                return (
                 None, [], {})
            return self.subsystem_table[name]
        finally:
            self.lock.release()

    _handler_table = {MSG_NEWKEYS: _parse_newkeys, 
     MSG_GLOBAL_REQUEST: _parse_global_request, 
     MSG_REQUEST_SUCCESS: _parse_request_success, 
     MSG_REQUEST_FAILURE: _parse_request_failure, 
     MSG_CHANNEL_OPEN_SUCCESS: _parse_channel_open_success, 
     MSG_CHANNEL_OPEN_FAILURE: _parse_channel_open_failure, 
     MSG_CHANNEL_OPEN: _parse_channel_open, 
     MSG_KEXINIT: _negotiate_keys}
    _channel_handler_table = {MSG_CHANNEL_SUCCESS: Channel._request_success, 
     MSG_CHANNEL_FAILURE: Channel._request_failed, 
     MSG_CHANNEL_DATA: Channel._feed, 
     MSG_CHANNEL_EXTENDED_DATA: Channel._feed_extended, 
     MSG_CHANNEL_WINDOW_ADJUST: Channel._window_adjust, 
     MSG_CHANNEL_REQUEST: Channel._handle_request, 
     MSG_CHANNEL_EOF: Channel._handle_eof, 
     MSG_CHANNEL_CLOSE: Channel._handle_close}


class SecurityOptions(object):
    __doc__ = "\n    Simple object containing the security preferences of an ssh transport.\n    These are tuples of acceptable ciphers, digests, key types, and key\n    exchange algorithms, listed in order of preference.\n\n    Changing the contents and/or order of these fields affects the underlying\n    `.Transport` (but only if you change them before starting the session).\n    If you try to add an algorithm that paramiko doesn't recognize,\n    ``ValueError`` will be raised.  If you try to assign something besides a\n    tuple to one of the fields, ``TypeError`` will be raised.\n    "
    __slots__ = '_transport'

    def __init__(self, transport):
        self._transport = transport

    def __repr__(self):
        """
        Returns a string representation of this object, for debugging.
        """
        return '<paramiko.SecurityOptions for {!r}>'.format(self._transport)

    def _set(self, name, orig, x):
        if type(x) is list:
            x = tuple(x)
        if type(x) is not tuple:
            raise TypeError('expected tuple or list')
        possible = list(getattr(self._transport, orig).keys())
        forbidden = [n for n in x if n not in possible]
        if len(forbidden) > 0:
            raise ValueError('unknown cipher')
        setattr(self._transport, name, x)

    @property
    def ciphers(self):
        """Symmetric encryption ciphers"""
        return self._transport._preferred_ciphers

    @ciphers.setter
    def ciphers(self, x):
        self._set('_preferred_ciphers', '_cipher_info', x)

    @property
    def digests(self):
        """Digest (one-way hash) algorithms"""
        return self._transport._preferred_macs

    @digests.setter
    def digests(self, x):
        self._set('_preferred_macs', '_mac_info', x)

    @property
    def key_types(self):
        """Public-key algorithms"""
        return self._transport._preferred_keys

    @key_types.setter
    def key_types(self, x):
        self._set('_preferred_keys', '_key_info', x)

    @property
    def kex(self):
        """Key exchange algorithms"""
        return self._transport._preferred_kex

    @kex.setter
    def kex(self, x):
        self._set('_preferred_kex', '_kex_info', x)

    @property
    def compression(self):
        """Compression algorithms"""
        return self._transport._preferred_compression

    @compression.setter
    def compression(self, x):
        self._set('_preferred_compression', '_compression_info', x)


class ChannelMap(object):

    def __init__(self):
        self._map = weakref.WeakValueDictionary()
        self._lock = threading.Lock()

    def put(self, chanid, chan):
        self._lock.acquire()
        try:
            self._map[chanid] = chan
        finally:
            self._lock.release()

    def get(self, chanid):
        self._lock.acquire()
        try:
            return self._map.get(chanid, None)
        finally:
            self._lock.release()

    def delete(self, chanid):
        self._lock.acquire()
        try:
            try:
                del self._map[chanid]
            except KeyError:
                pass

        finally:
            self._lock.release()

    def values(self):
        self._lock.acquire()
        try:
            return list(self._map.values())
        finally:
            self._lock.release()

    def __len__(self):
        self._lock.acquire()
        try:
            return len(self._map)
        finally:
            self._lock.release()