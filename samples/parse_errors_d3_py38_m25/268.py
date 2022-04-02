# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: smtplib.py
"""SMTP/ESMTP client class.

This should follow RFC 821 (SMTP), RFC 1869 (ESMTP), RFC 2554 (SMTP
Authentication) and RFC 2487 (Secure SMTP over TLS).

Notes:

Please remember, when doing ESMTP, that the names of the SMTP service
extensions are NOT the same thing as the option keywords for the RCPT
and MAIL commands!

Example:

  >>> import smtplib
  >>> s=smtplib.SMTP("localhost")
  >>> print(s.help())
  This is Sendmail version 8.8.4
  Topics:
      HELO    EHLO    MAIL    RCPT    DATA
      RSET    NOOP    QUIT    HELP    VRFY
      EXPN    VERB    ETRN    DSN
  For more info use "HELP <topic>".
  To report bugs in the implementation send email to
      sendmail-bugs@sendmail.org.
  For local information send email to Postmaster at your site.
  End of HELP info
  >>> s.putcmd("vrfy","someone@here")
  >>> s.getreply()
  (250, "Somebody OverHere <somebody@here.my.org>")
  >>> s.quit()
"""
import socket, io, re, email.utils, email.message, email.generator, base64, hmac, copy, datetime, sys
import email.base64mime as encode_base64
__all__ = [
 'SMTPException', 'SMTPNotSupportedError', 'SMTPServerDisconnected', 'SMTPResponseException',
 'SMTPSenderRefused', 'SMTPRecipientsRefused', 'SMTPDataError',
 'SMTPConnectError', 'SMTPHeloError', 'SMTPAuthenticationError',
 'quoteaddr', 'quotedata', 'SMTP']
SMTP_PORT = 25
SMTP_SSL_PORT = 465
CRLF = '\r\n'
bCRLF = b'\r\n'
_MAXLINE = 8192
OLDSTYLE_AUTH = re.compile('auth=(.*)', re.I)

class SMTPException(OSError):
    __doc__ = 'Base class for all exceptions raised by this module.'


class SMTPNotSupportedError(SMTPException):
    __doc__ = 'The command or option is not supported by the SMTP server.\n\n    This exception is raised when an attempt is made to run a command or a\n    command with an option which is not supported by the server.\n    '


class SMTPServerDisconnected(SMTPException):
    __doc__ = 'Not connected to any SMTP server.\n\n    This exception is raised when the server unexpectedly disconnects,\n    or when an attempt is made to use the SMTP instance before\n    connecting it to a server.\n    '


class SMTPResponseException(SMTPException):
    __doc__ = "Base class for all exceptions that include an SMTP error code.\n\n    These exceptions are generated in some instances when the SMTP\n    server returns an error code.  The error code is stored in the\n    `smtp_code' attribute of the error, and the `smtp_error' attribute\n    is set to the error message.\n    "

    def __init__(self, code, msg):
        self.smtp_code = code
        self.smtp_error = msg
        self.args = (code, msg)


class SMTPSenderRefused(SMTPResponseException):
    __doc__ = "Sender address refused.\n\n    In addition to the attributes set by on all SMTPResponseException\n    exceptions, this sets `sender' to the string that the SMTP refused.\n    "

    def __init__(self, code, msg, sender):
        self.smtp_code = code
        self.smtp_error = msg
        self.sender = sender
        self.args = (code, msg, sender)


class SMTPRecipientsRefused(SMTPException):
    __doc__ = "All recipient addresses refused.\n\n    The errors for each recipient are accessible through the attribute\n    'recipients', which is a dictionary of exactly the same sort as\n    SMTP.sendmail() returns.\n    "

    def __init__(self, recipients):
        self.recipients = recipients
        self.args = (recipients,)


class SMTPDataError(SMTPResponseException):
    __doc__ = "The SMTP server didn't accept the data."


class SMTPConnectError(SMTPResponseException):
    __doc__ = 'Error during connection establishment.'


class SMTPHeloError(SMTPResponseException):
    __doc__ = 'The server refused our HELO reply.'


class SMTPAuthenticationError(SMTPResponseException):
    __doc__ = "Authentication error.\n\n    Most probably the server didn't accept the username/password\n    combination provided.\n    "


def quoteaddr(addrstring):
    """Quote a subset of the email addresses defined by RFC 821.

    Should be able to handle anything email.utils.parseaddr can handle.
    """
    displayname, addr = email.utils.parseaddr(addrstring)
    if (displayname, addr) == ('', ''):
        if addrstring.strip().startswith('<'):
            return addrstring
        return '<%s>' % addrstring
    return '<%s>' % addr


def _addr_only(addrstring):
    displayname, addr = email.utils.parseaddr(addrstring)
    if (displayname, addr) == ('', ''):
        return addrstring
    return addr


def quotedata(data):
    r"""Quote data for email.

    Double leading '.', and change Unix newline '\n', or Mac '\r' into
    Internet CRLF end-of-line.
    """
    return re.sub('(?m)^\\.', '..', re.sub('(?:\\r\\n|\\n|\\r(?!\\n))', CRLF, data))


def _quote_periods(bindata):
    return re.sub(b'(?m)^\\.', b'..', bindata)


def _fix_eols(data):
    return re.sub('(?:\\r\\n|\\n|\\r(?!\\n))', CRLF, data)


try:
    import ssl
except ImportError:
    _have_ssl = False
else:
    _have_ssl = True

class SMTP:
    __doc__ = "This class manages a connection to an SMTP or ESMTP server.\n    SMTP Objects:\n        SMTP objects have the following attributes:\n            helo_resp\n                This is the message given by the server in response to the\n                most recent HELO command.\n\n            ehlo_resp\n                This is the message given by the server in response to the\n                most recent EHLO command. This is usually multiline.\n\n            does_esmtp\n                This is a True value _after you do an EHLO command_, if the\n                server supports ESMTP.\n\n            esmtp_features\n                This is a dictionary, which, if the server supports ESMTP,\n                will _after you do an EHLO command_, contain the names of the\n                SMTP service extensions this server supports, and their\n                parameters (if any).\n\n                Note, all extension names are mapped to lower case in the\n                dictionary.\n\n        See each method's docstrings for details.  In general, there is a\n        method of the same name to perform each SMTP command.  There is also a\n        method called 'sendmail' that will do an entire mail transaction.\n        "
    debuglevel = 0
    sock = None
    file = None
    helo_resp = None
    ehlo_msg = 'ehlo'
    ehlo_resp = None
    does_esmtp = 0
    default_port = SMTP_PORT

    def __init__(self, host='', port=0, local_hostname=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, source_address=None):
        """Initialize a new instance.

        If specified, `host' is the name of the remote host to which to
        connect.  If specified, `port' specifies the port to which to connect.
        By default, smtplib.SMTP_PORT is used.  If a host is specified the
        connect method is called, and if it returns anything other than a
        success code an SMTPConnectError is raised.  If specified,
        `local_hostname` is used as the FQDN of the local host in the HELO/EHLO
        command.  Otherwise, the local hostname is found using
        socket.getfqdn(). The `source_address` parameter takes a 2-tuple (host,
        port) for the socket to bind to as its source address before
        connecting. If the host is '' and port is 0, the OS default behavior
        will be used.

        """
        self._host = host
        self.timeout = timeout
        self.esmtp_features = {}
        self.command_encoding = 'ascii'
        self.source_address = source_address
        if host:
            code, msg = self.connect(host, port)
            if code != 220:
                self.close()
                raise SMTPConnectError(code, msg)
        if local_hostname is not None:
            self.local_hostname = local_hostname
        else:
            fqdn = socket.getfqdn()
        if '.' in fqdn:
            self.local_hostname = fqdn
        else:
            addr = '127.0.0.1'
            try:
                addr = socket.gethostbyname(socket.gethostname())
            except socket.gaierror:
                pass
            else:
                self.local_hostname = '[%s]' % addr

    def __enter__(self):
        return self

    def __exit__(self, *args):
        try:
            try:
                code, message = self.docmd('QUIT')
                if code != 221:
                    raise SMTPResponseException(code, message)
            except SMTPServerDisconnected:
                pass

        finally:
            self.close()

    def set_debuglevel(self, debuglevel):
        """Set the debug output level.

        A non-false value results in debug messages for connection and for all
        messages sent to and received from the server.

        """
        self.debuglevel = debuglevel

    def _print_debug(self, *args):
        if self.debuglevel > 1:
            print(datetime.datetime.now().time(), *args, **{'file': sys.stderr})
        else:
            print(*args, **{'file': sys.stderr})

    def _get_socket(self, host, port, timeout):
        if self.debuglevel > 0:
            self._print_debug('connect: to', (host, port), self.source_address)
        return socket.create_connection((host, port), timeout, self.source_address)

    def connect(self, host='localhost', port=0, source_address=None):
        """Connect to a host on a given port.

        If the hostname ends with a colon (`:') followed by a number, and
        there is no port specified, that suffix will be stripped off and the
        number interpreted as the port number to use.

        Note: This method is automatically invoked by __init__, if a host is
        specified during instantiation.

        """
        if source_address:
            self.source_address = source_address
        if not port:
            if host.find(':') == host.rfind(':'):
                i = host.rfind(':')
                if i >= 0:
                    host, port = host[:i], host[i + 1:]
                    try:
                        port = int(port)
                    except ValueError:
                        raise OSError('nonnumeric port')
                    else:
                        if not port:
                            port = self.default_port
                        if self.debuglevel > 0:
                            self._print_debug('connect:', (host, port))
                sys.audit('smtplib.connect', self, host, port)
                self.sock = self._get_socket(host, port, self.timeout)
                self.file = None
                code, msg = self.getreply()
                if self.debuglevel > 0:
                    self._print_debug('connect:', repr(msg))
            return (
             code, msg)

    def send(self, s):
        """Send `s' to the server."""
        if self.debuglevel > 0:
            self._print_debug('send:', repr(s))
        if self.sock:
            if isinstance(s, str):
                s = s.encode(self.command_encoding)
            sys.audit('smtplib.send', self, s)
            try:
                self.sock.sendall(s)
            except OSError:
                self.close()
                raise SMTPServerDisconnected('Server not connected')

        else:
            raise SMTPServerDisconnected('please run connect() first')

    def putcmd(self, cmd, args=''):
        """Send a command to the server."""
        if args == '':
            str = '%s%s' % (cmd, CRLF)
        else:
            str = '%s %s%s' % (cmd, args, CRLF)
        self.send(str)

    def getreply--- This code section failed: ---

 L. 386         0  BUILD_LIST_0          0 
                2  STORE_FAST               'resp'

 L. 387         4  LOAD_FAST                'self'
                6  LOAD_ATTR                file
                8  LOAD_CONST               None
               10  COMPARE_OP               is
               12  POP_JUMP_IF_FALSE    28  'to 28'

 L. 388        14  LOAD_FAST                'self'
               16  LOAD_ATTR                sock
               18  LOAD_METHOD              makefile
               20  LOAD_STR                 'rb'
               22  CALL_METHOD_1         1  ''
               24  LOAD_FAST                'self'
               26  STORE_ATTR               file
             28_0  COME_FROM           286  '286'
             28_1  COME_FROM           280  '280'
             28_2  COME_FROM            12  '12'

 L. 390        28  SETUP_FINALLY        50  'to 50'

 L. 391        30  LOAD_FAST                'self'
               32  LOAD_ATTR                file
               34  LOAD_METHOD              readline
               36  LOAD_GLOBAL              _MAXLINE
               38  LOAD_CONST               1
               40  BINARY_ADD       
               42  CALL_METHOD_1         1  ''
               44  STORE_FAST               'line'
               46  POP_BLOCK        
               48  JUMP_FORWARD        108  'to 108'
             50_0  COME_FROM_FINALLY    28  '28'

 L. 392        50  DUP_TOP          
               52  LOAD_GLOBAL              OSError
               54  COMPARE_OP               exception-match
               56  POP_JUMP_IF_FALSE   106  'to 106'
               58  POP_TOP          
               60  STORE_FAST               'e'
               62  POP_TOP          
               64  SETUP_FINALLY        94  'to 94'

 L. 393        66  LOAD_FAST                'self'
               68  LOAD_METHOD              close
               70  CALL_METHOD_0         0  ''
               72  POP_TOP          

 L. 394        74  LOAD_GLOBAL              SMTPServerDisconnected
               76  LOAD_STR                 'Connection unexpectedly closed: '

 L. 395        78  LOAD_GLOBAL              str
               80  LOAD_FAST                'e'
               82  CALL_FUNCTION_1       1  ''

 L. 394        84  BINARY_ADD       
               86  CALL_FUNCTION_1       1  ''
               88  RAISE_VARARGS_1       1  'exception instance'
               90  POP_BLOCK        
               92  BEGIN_FINALLY    
             94_0  COME_FROM_FINALLY    64  '64'
               94  LOAD_CONST               None
               96  STORE_FAST               'e'
               98  DELETE_FAST              'e'
              100  END_FINALLY      
              102  POP_EXCEPT       
              104  JUMP_FORWARD        108  'to 108'
            106_0  COME_FROM            56  '56'
              106  END_FINALLY      
            108_0  COME_FROM           104  '104'
            108_1  COME_FROM            48  '48'

 L. 396       108  LOAD_FAST                'line'
              110  POP_JUMP_IF_TRUE    128  'to 128'

 L. 397       112  LOAD_FAST                'self'
              114  LOAD_METHOD              close
              116  CALL_METHOD_0         0  ''
              118  POP_TOP          

 L. 398       120  LOAD_GLOBAL              SMTPServerDisconnected
              122  LOAD_STR                 'Connection unexpectedly closed'
              124  CALL_FUNCTION_1       1  ''
              126  RAISE_VARARGS_1       1  'exception instance'
            128_0  COME_FROM           110  '110'

 L. 399       128  LOAD_FAST                'self'
              130  LOAD_ATTR                debuglevel
              132  LOAD_CONST               0
              134  COMPARE_OP               >
              136  POP_JUMP_IF_FALSE   154  'to 154'

 L. 400       138  LOAD_FAST                'self'
              140  LOAD_METHOD              _print_debug
              142  LOAD_STR                 'reply:'
              144  LOAD_GLOBAL              repr
              146  LOAD_FAST                'line'
              148  CALL_FUNCTION_1       1  ''
              150  CALL_METHOD_2         2  ''
              152  POP_TOP          
            154_0  COME_FROM           136  '136'

 L. 401       154  LOAD_GLOBAL              len
              156  LOAD_FAST                'line'
              158  CALL_FUNCTION_1       1  ''
              160  LOAD_GLOBAL              _MAXLINE
              162  COMPARE_OP               >
              164  POP_JUMP_IF_FALSE   184  'to 184'

 L. 402       166  LOAD_FAST                'self'
              168  LOAD_METHOD              close
              170  CALL_METHOD_0         0  ''
              172  POP_TOP          

 L. 403       174  LOAD_GLOBAL              SMTPResponseException
              176  LOAD_CONST               500
              178  LOAD_STR                 'Line too long.'
              180  CALL_FUNCTION_2       2  ''
              182  RAISE_VARARGS_1       1  'exception instance'
            184_0  COME_FROM           164  '164'

 L. 404       184  LOAD_FAST                'resp'
              186  LOAD_METHOD              append
              188  LOAD_FAST                'line'
              190  LOAD_CONST               4
              192  LOAD_CONST               None
              194  BUILD_SLICE_2         2 
              196  BINARY_SUBSCR    
              198  LOAD_METHOD              strip
              200  LOAD_CONST               b' \t\r\n'
              202  CALL_METHOD_1         1  ''
              204  CALL_METHOD_1         1  ''
              206  POP_TOP          

 L. 405       208  LOAD_FAST                'line'
              210  LOAD_CONST               None
              212  LOAD_CONST               3
              214  BUILD_SLICE_2         2 
              216  BINARY_SUBSCR    
              218  STORE_FAST               'code'

 L. 408       220  SETUP_FINALLY       234  'to 234'

 L. 409       222  LOAD_GLOBAL              int
              224  LOAD_FAST                'code'
              226  CALL_FUNCTION_1       1  ''
              228  STORE_FAST               'errcode'
              230  POP_BLOCK        
              232  JUMP_FORWARD        266  'to 266'
            234_0  COME_FROM_FINALLY   220  '220'

 L. 410       234  DUP_TOP          
              236  LOAD_GLOBAL              ValueError
              238  COMPARE_OP               exception-match
          240_242  POP_JUMP_IF_FALSE   264  'to 264'
              244  POP_TOP          
              246  POP_TOP          
              248  POP_TOP          

 L. 411       250  LOAD_CONST               -1
              252  STORE_FAST               'errcode'

 L. 412       254  POP_EXCEPT       
          256_258  BREAK_LOOP          288  'to 288'
              260  POP_EXCEPT       
              262  JUMP_FORWARD        266  'to 266'
            264_0  COME_FROM           240  '240'
              264  END_FINALLY      
            266_0  COME_FROM           262  '262'
            266_1  COME_FROM           232  '232'

 L. 414       266  LOAD_FAST                'line'
              268  LOAD_CONST               3
              270  LOAD_CONST               4
              272  BUILD_SLICE_2         2 
              274  BINARY_SUBSCR    
              276  LOAD_CONST               b'-'
              278  COMPARE_OP               !=
              280  POP_JUMP_IF_FALSE_BACK    28  'to 28'

 L. 415   282_284  JUMP_FORWARD        288  'to 288'
              286  JUMP_BACK            28  'to 28'
            288_0  COME_FROM           282  '282'
            288_1  COME_FROM           256  '256'

 L. 417       288  LOAD_CONST               b'\n'
              290  LOAD_METHOD              join
              292  LOAD_FAST                'resp'
              294  CALL_METHOD_1         1  ''
              296  STORE_FAST               'errmsg'

 L. 418       298  LOAD_FAST                'self'
              300  LOAD_ATTR                debuglevel
              302  LOAD_CONST               0
              304  COMPARE_OP               >
          306_308  POP_JUMP_IF_FALSE   328  'to 328'

 L. 419       310  LOAD_FAST                'self'
              312  LOAD_METHOD              _print_debug
              314  LOAD_STR                 'reply: retcode (%s); Msg: %a'
              316  LOAD_FAST                'errcode'
              318  LOAD_FAST                'errmsg'
              320  BUILD_TUPLE_2         2 
              322  BINARY_MODULO    
              324  CALL_METHOD_1         1  ''
              326  POP_TOP          
            328_0  COME_FROM           306  '306'

 L. 420       328  LOAD_FAST                'errcode'
              330  LOAD_FAST                'errmsg'
              332  BUILD_TUPLE_2         2 
              334  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 286

    def docmd(self, cmd, args=''):
        """Send a command, and return its response code."""
        self.putcmd(cmd, args)
        return self.getreply()

    def helo(self, name=''):
        """SMTP 'helo' command.
        Hostname to send for this command defaults to the FQDN of the local
        host.
        """
        self.putcmd('helo', name or self.local_hostname)
        code, msg = self.getreply()
        self.helo_resp = msg
        return (
         code, msg)

    def ehlo(self, name=''):
        """ SMTP 'ehlo' command.
        Hostname to send for this command defaults to the FQDN of the local
        host.
        """
        self.esmtp_features = {}
        self.putcmd(self.ehlo_msg, name or self.local_hostname)
        code, msg = self.getreply()
        if code == -1:
            if len(msg) == 0:
                self.close()
                raise SMTPServerDisconnected('Server not connected')
        self.ehlo_resp = msg
        if code != 250:
            return (code, msg)
        self.does_esmtp = 1
        assert isinstance(self.ehlo_resp, bytes), repr(self.ehlo_resp)
        resp = self.ehlo_resp.decode('latin-1').split('\n')
        del resp[0]
        for each in resp:
            auth_match = OLDSTYLE_AUTH.match(each)
            if auth_match:
                self.esmtp_features['auth'] = self.esmtp_features.get('auth', '') + ' ' + auth_match.groups(0)[0]
            else:
                m = re.match('(?P<feature>[A-Za-z0-9][A-Za-z0-9\\-]*) ?', each)
                if m:
                    feature = m.group('feature').lower()
                    params = m.string[m.end('feature'):].strip()
                    if feature == 'auth':
                        self.esmtp_features[feature] = self.esmtp_features.get(feature, '') + ' ' + params
                    else:
                        self.esmtp_features[feature] = params
        else:
            return (
             code, msg)

    def has_extn(self, opt):
        """Does the server support a given SMTP service extension?"""
        return opt.lower() in self.esmtp_features

    def help(self, args=''):
        """SMTP 'help' command.
        Returns help text from server."""
        self.putcmd('help', args)
        return self.getreply()[1]

    def rset(self):
        """SMTP 'rset' command -- resets session."""
        self.command_encoding = 'ascii'
        return self.docmd('rset')

    def _rset(self):
        """Internal 'rset' command which ignores any SMTPServerDisconnected error.

        Used internally in the library, since the server disconnected error
        should appear to the application when the *next* command is issued, if
        we are doing an internal "safety" reset.
        """
        try:
            self.rset()
        except SMTPServerDisconnected:
            pass

    def noop(self):
        """SMTP 'noop' command -- doesn't do anything :>"""
        return self.docmd('noop')

    def mail(self, sender, options=()):
        """SMTP 'mail' command -- begins mail xfer session.

        This method may raise the following exceptions:

         SMTPNotSupportedError  The options parameter includes 'SMTPUTF8'
                                but the SMTPUTF8 extension is not supported by
                                the server.
        """
        optionlist = ''
        if options:
            if self.does_esmtp:
                if any((x.lower() == 'smtputf8' for x in options)):
                    if self.has_extn('smtputf8'):
                        self.command_encoding = 'utf-8'
                    else:
                        raise SMTPNotSupportedError('SMTPUTF8 not supported by server')
                optionlist = ' ' + ' '.join(options)
        self.putcmd('mail', 'FROM:%s%s' % (quoteaddr(sender), optionlist))
        return self.getreply()

    def rcpt(self, recip, options=()):
        """SMTP 'rcpt' command -- indicates 1 recipient for this mail."""
        optionlist = ''
        if options:
            if self.does_esmtp:
                optionlist = ' ' + ' '.join(options)
        self.putcmd('rcpt', 'TO:%s%s' % (quoteaddr(recip), optionlist))
        return self.getreply()

    def data(self, msg):
        r"""SMTP 'DATA' command -- sends message data to server.

        Automatically quotes lines beginning with a period per rfc821.
        Raises SMTPDataError if there is an unexpected reply to the
        DATA command; the return value from this method is the final
        response code received when the all data is sent.  If msg
        is a string, lone '\r' and '\n' characters are converted to
        '\r\n' characters.  If msg is bytes, it is transmitted as is.
        """
        self.putcmd('data')
        code, repl = self.getreply()
        if self.debuglevel > 0:
            self._print_debug('data:', (code, repl))
        if code != 354:
            raise SMTPDataError(code, repl)
        else:
            if isinstance(msg, str):
                msg = _fix_eols(msg).encode('ascii')
            q = _quote_periods(msg)
            if q[-2:] != bCRLF:
                q = q + bCRLF
            q = q + b'.' + bCRLF
            self.send(q)
            code, msg = self.getreply()
            if self.debuglevel > 0:
                self._print_debug('data:', (code, msg))
            return (code, msg)

    def verify(self, address):
        """SMTP 'verify' command -- checks for address validity."""
        self.putcmd('vrfy', _addr_only(address))
        return self.getreply()

    vrfy = verify

    def expn(self, address):
        """SMTP 'expn' command -- expands a mailing list."""
        self.putcmd('expn', _addr_only(address))
        return self.getreply()

    def ehlo_or_helo_if_needed(self):
        """Call self.ehlo() and/or self.helo() if needed.

        If there has been no previous EHLO or HELO command this session, this
        method tries ESMTP EHLO first.

        This method may raise the following exceptions:

         SMTPHeloError            The server didn't reply properly to
                                  the helo greeting.
        """
        if self.helo_resp is None:
            if self.ehlo_resp is None:
                if not 200 <= self.ehlo()[0] <= 299:
                    code, resp = self.helo()
                    if not 200 <= code <= 299:
                        raise SMTPHeloError(code, resp)

    def auth(self, mechanism, authobject, *, initial_response_ok=True):
        """Authentication command - requires response processing.

        'mechanism' specifies which authentication mechanism is to
        be used - the valid values are those listed in the 'auth'
        element of 'esmtp_features'.

        'authobject' must be a callable object taking a single argument:

                data = authobject(challenge)

        It will be called to process the server's challenge response; the
        challenge argument it is passed will be a bytes.  It should return
        an ASCII string that will be base64 encoded and sent to the server.

        Keyword arguments:
            - initial_response_ok: Allow sending the RFC 4954 initial-response
              to the AUTH command, if the authentication methods supports it.
        """
        mechanism = mechanism.upper()
        initial_response = authobject() if initial_response_ok else None
        if initial_response is not None:
            response = encode_base64((initial_response.encode('ascii')), eol='')
            code, resp = self.docmd('AUTH', mechanism + ' ' + response)
        else:
            code, resp = self.docmd('AUTH', mechanism)
        if code == 334:
            challenge = base64.decodebytes(resp)
            response = encode_base64((authobject(challenge).encode('ascii')),
              eol='')
            code, resp = self.docmd(response)
        if code in (235, 503):
            return (code, resp)
        raise SMTPAuthenticationError(code, resp)

    def auth_cram_md5(self, challenge=None):
        """ Authobject to use with CRAM-MD5 authentication. Requires self.user
        and self.password to be set."""
        if challenge is None:
            return
        return self.user + ' ' + hmac.HMAC(self.password.encode('ascii'), challenge, 'md5').hexdigest()

    def auth_plain(self, challenge=None):
        """ Authobject to use with PLAIN authentication. Requires self.user and
        self.password to be set."""
        return '\x00%s\x00%s' % (self.user, self.password)

    def auth_login(self, challenge=None):
        """ Authobject to use with LOGIN authentication. Requires self.user and
        self.password to be set."""
        if challenge is None:
            return self.user
        return self.password

    def login--- This code section failed: ---

 L. 698         0  LOAD_FAST                'self'
                2  LOAD_METHOD              ehlo_or_helo_if_needed
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 699         8  LOAD_FAST                'self'
               10  LOAD_METHOD              has_extn
               12  LOAD_STR                 'auth'
               14  CALL_METHOD_1         1  ''
               16  POP_JUMP_IF_TRUE     26  'to 26'

 L. 700        18  LOAD_GLOBAL              SMTPNotSupportedError

 L. 701        20  LOAD_STR                 'SMTP AUTH extension not supported by server.'

 L. 700        22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            16  '16'

 L. 704        26  LOAD_FAST                'self'
               28  LOAD_ATTR                esmtp_features
               30  LOAD_STR                 'auth'
               32  BINARY_SUBSCR    
               34  LOAD_METHOD              split
               36  CALL_METHOD_0         0  ''
               38  STORE_DEREF              'advertised_authlist'

 L. 707        40  LOAD_STR                 'CRAM-MD5'
               42  LOAD_STR                 'PLAIN'
               44  LOAD_STR                 'LOGIN'
               46  BUILD_LIST_3          3 
               48  STORE_FAST               'preferred_auths'

 L. 711        50  LOAD_CLOSURE             'advertised_authlist'
               52  BUILD_TUPLE_1         1 
               54  LOAD_LISTCOMP            '<code_object <listcomp>>'
               56  LOAD_STR                 'SMTP.login.<locals>.<listcomp>'
               58  MAKE_FUNCTION_8          'closure'
               60  LOAD_FAST                'preferred_auths'
               62  GET_ITER         
               64  CALL_FUNCTION_1       1  ''
               66  STORE_FAST               'authlist'

 L. 713        68  LOAD_FAST                'authlist'
               70  POP_JUMP_IF_TRUE     80  'to 80'

 L. 714        72  LOAD_GLOBAL              SMTPException
               74  LOAD_STR                 'No suitable authentication method found.'
               76  CALL_FUNCTION_1       1  ''
               78  RAISE_VARARGS_1       1  'exception instance'
             80_0  COME_FROM            70  '70'

 L. 719        80  LOAD_FAST                'user'
               82  LOAD_FAST                'password'
               84  ROT_TWO          
               86  LOAD_FAST                'self'
               88  STORE_ATTR               user
               90  LOAD_FAST                'self'
               92  STORE_ATTR               password

 L. 720        94  LOAD_FAST                'authlist'
               96  GET_ITER         
             98_0  COME_FROM           214  '214'
             98_1  COME_FROM           210  '210'
             98_2  COME_FROM           174  '174'
               98  FOR_ITER            216  'to 216'
              100  STORE_FAST               'authmethod'

 L. 721       102  LOAD_STR                 'auth_'
              104  LOAD_FAST                'authmethod'
              106  LOAD_METHOD              lower
              108  CALL_METHOD_0         0  ''
              110  LOAD_METHOD              replace
              112  LOAD_STR                 '-'
              114  LOAD_STR                 '_'
              116  CALL_METHOD_2         2  ''
              118  BINARY_ADD       
              120  STORE_FAST               'method_name'

 L. 722       122  SETUP_FINALLY       176  'to 176'

 L. 723       124  LOAD_FAST                'self'
              126  LOAD_ATTR                auth

 L. 724       128  LOAD_FAST                'authmethod'

 L. 724       130  LOAD_GLOBAL              getattr
              132  LOAD_FAST                'self'
              134  LOAD_FAST                'method_name'
              136  CALL_FUNCTION_2       2  ''

 L. 725       138  LOAD_FAST                'initial_response_ok'

 L. 723       140  LOAD_CONST               ('initial_response_ok',)
              142  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              144  UNPACK_SEQUENCE_2     2 
              146  STORE_FAST               'code'
              148  STORE_FAST               'resp'

 L. 728       150  LOAD_FAST                'code'
              152  LOAD_CONST               (235, 503)
              154  COMPARE_OP               in
              156  POP_JUMP_IF_FALSE   172  'to 172'

 L. 729       158  LOAD_FAST                'code'
              160  LOAD_FAST                'resp'
              162  BUILD_TUPLE_2         2 
              164  POP_BLOCK        
              166  ROT_TWO          
              168  POP_TOP          
              170  RETURN_VALUE     
            172_0  COME_FROM           156  '156'
              172  POP_BLOCK        
              174  JUMP_BACK            98  'to 98'
            176_0  COME_FROM_FINALLY   122  '122'

 L. 730       176  DUP_TOP          
              178  LOAD_GLOBAL              SMTPAuthenticationError
              180  COMPARE_OP               exception-match
              182  POP_JUMP_IF_FALSE   212  'to 212'
              184  POP_TOP          
              186  STORE_FAST               'e'
              188  POP_TOP          
              190  SETUP_FINALLY       200  'to 200'

 L. 731       192  LOAD_FAST                'e'
              194  STORE_FAST               'last_exception'
              196  POP_BLOCK        
              198  BEGIN_FINALLY    
            200_0  COME_FROM_FINALLY   190  '190'
              200  LOAD_CONST               None
              202  STORE_FAST               'e'
              204  DELETE_FAST              'e'
              206  END_FINALLY      
              208  POP_EXCEPT       
              210  JUMP_BACK            98  'to 98'
            212_0  COME_FROM           182  '182'
              212  END_FINALLY      
              214  JUMP_BACK            98  'to 98'
            216_0  COME_FROM            98  '98'

 L. 734       216  LOAD_FAST                'last_exception'
              218  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `ROT_TWO' instruction at offset 166

    def starttls(self, keyfile=None, certfile=None, context=None):
        """Puts the connection to the SMTP server into TLS mode.

        If there has been no previous EHLO or HELO command this session, this
        method tries ESMTP EHLO first.

        If the server supports TLS, this will encrypt the rest of the SMTP
        session. If you provide the keyfile and certfile parameters,
        the identity of the SMTP server and client can be checked. This,
        however, depends on whether the socket module really checks the
        certificates.

        This method may raise the following exceptions:

         SMTPHeloError            The server didn't reply properly to
                                  the helo greeting.
        """
        self.ehlo_or_helo_if_needed()
        if not self.has_extn('starttls'):
            raise SMTPNotSupportedError('STARTTLS extension not supported by server.')
        resp, reply = self.docmd('STARTTLS')
        if resp == 220:
            if not _have_ssl:
                raise RuntimeError('No SSL support included in this Python')
            if context is not None:
                if keyfile is not None:
                    raise ValueError('context and keyfile arguments are mutually exclusive')
            if context is not None:
                if certfile is not None:
                    raise ValueError('context and certfile arguments are mutually exclusive')
            if keyfile is not None or (certfile is not None):
                import warnings
                warnings.warn('keyfile and certfile are deprecated, use a custom context instead', DeprecationWarning, 2)
            if context is None:
                context = ssl._create_stdlib_context(certfile=certfile, keyfile=keyfile)
            self.sock = context.wrap_socket((self.sock), server_hostname=(self._host))
            self.file = None
            self.helo_resp = None
            self.ehlo_resp = None
            self.esmtp_features = {}
            self.does_esmtp = 0
        else:
            raise SMTPResponseException(resp, reply)
        return (resp, reply)

    def sendmail(self, from_addr, to_addrs, msg, mail_options=(), rcpt_options=()):
        r"""This command performs an entire mail transaction.

        The arguments are:
            - from_addr    : The address sending this mail.
            - to_addrs     : A list of addresses to send this mail to.  A bare
                             string will be treated as a list with 1 address.
            - msg          : The message to send.
            - mail_options : List of ESMTP options (such as 8bitmime) for the
                             mail command.
            - rcpt_options : List of ESMTP options (such as DSN commands) for
                             all the rcpt commands.

        msg may be a string containing characters in the ASCII range, or a byte
        string.  A string is encoded to bytes using the ascii codec, and lone
        \r and \n characters are converted to \r\n characters.

        If there has been no previous EHLO or HELO command this session, this
        method tries ESMTP EHLO first.  If the server does ESMTP, message size
        and each of the specified options will be passed to it.  If EHLO
        fails, HELO will be tried and ESMTP options suppressed.

        This method will return normally if the mail is accepted for at least
        one recipient.  It returns a dictionary, with one entry for each
        recipient that was refused.  Each entry contains a tuple of the SMTP
        error code and the accompanying error message sent by the server.

        This method may raise the following exceptions:

         SMTPHeloError          The server didn't reply properly to
                                the helo greeting.
         SMTPRecipientsRefused  The server rejected ALL recipients
                                (no mail was sent).
         SMTPSenderRefused      The server didn't accept the from_addr.
         SMTPDataError          The server replied with an unexpected
                                error code (other than a refusal of
                                a recipient).
         SMTPNotSupportedError  The mail_options parameter includes 'SMTPUTF8'
                                but the SMTPUTF8 extension is not supported by
                                the server.

        Note: the connection will be open even after an exception is raised.

        Example:

         >>> import smtplib
         >>> s=smtplib.SMTP("localhost")
         >>> tolist=["one@one.org","two@two.org","three@three.org","four@four.org"]
         >>> msg = '''\
         ... From: Me@my.org
         ... Subject: testin'...
         ...
         ... This is a test '''
         >>> s.sendmail("me@my.org",tolist,msg)
         { "three@three.org" : ( 550 ,"User unknown" ) }
         >>> s.quit()

        In the above example, the message was accepted for delivery to three
        of the four addresses, and one was rejected, with the error code
        550.  If all addresses are accepted, then the method will return an
        empty dictionary.

        """
        self.ehlo_or_helo_if_needed()
        esmtp_opts = []
        if isinstance(msg, str):
            msg = _fix_eols(msg).encode('ascii')
        if self.does_esmtp:
            if self.has_extn('size'):
                esmtp_opts.append('size=%d' % len(msg))
            for option in mail_options:
                esmtp_opts.append(option)
            else:
                code, resp = self.mail(from_addr, esmtp_opts)
                if code != 250:
                    if code == 421:
                        self.close()
                    else:
                        self._rset()
                    raise SMTPSenderRefused(code, resp, from_addr)
                senderrs = {}
                if isinstance(to_addrs, str):
                    to_addrs = [
                     to_addrs]

        for each in to_addrs:
            code, resp = self.rcpt(each, rcpt_options)
            if code != 250:
                if code != 251:
                    senderrs[each] = (
                     code, resp)
            if code == 421:
                self.close()
                raise SMTPRecipientsRefused(senderrs)
        else:
            if len(senderrs) == len(to_addrs):
                self._rset()
                raise SMTPRecipientsRefused(senderrs)
            code, resp = self.data(msg)
            if code != 250:
                if code == 421:
                    self.close()
                else:
                    self._rset()
                raise SMTPDataError(code, resp)
            return senderrs

    def send_message(self, msg, from_addr=None, to_addrs=None, mail_options=(), rcpt_options=()):
        """Converts message to a bytestring and passes it to sendmail.

        The arguments are as for sendmail, except that msg is an
        email.message.Message object.  If from_addr is None or to_addrs is
        None, these arguments are taken from the headers of the Message as
        described in RFC 2822 (a ValueError is raised if there is more than
        one set of 'Resent-' headers).  Regardless of the values of from_addr and
        to_addr, any Bcc field (or Resent-Bcc field, when the Message is a
        resent) of the Message object won't be transmitted.  The Message
        object is then serialized using email.generator.BytesGenerator and
        sendmail is called to transmit the message.  If the sender or any of
        the recipient addresses contain non-ASCII and the server advertises the
        SMTPUTF8 capability, the policy is cloned with utf8 set to True for the
        serialization, and SMTPUTF8 and BODY=8BITMIME are asserted on the send.
        If the server does not support SMTPUTF8, an SMTPNotSupported error is
        raised.  Otherwise the generator is called without modifying the
        policy.

        """
        self.ehlo_or_helo_if_needed()
        resent = msg.get_all('Resent-Date')
        if resent is None:
            header_prefix = ''
        elif len(resent) == 1:
            header_prefix = 'Resent-'
        else:
            raise ValueError("message has more than one 'Resent-' header block")
        if from_addr is None:
            from_addr = msg[(header_prefix + 'Sender')] if header_prefix + 'Sender' in msg else msg[(header_prefix + 'From')]
            from_addr = email.utils.getaddresses([from_addr])[0][1]
        if to_addrs is None:
            addr_fields = [f for f in (msg[(header_prefix + 'To')],
             msg[(header_prefix + 'Bcc')],
             msg[(header_prefix + 'Cc')]) if f is not None]
            to_addrs = [a[1] for a in email.utils.getaddresses(addr_fields)]
        msg_copy = copy.copy(msg)
        del msg_copy['Bcc']
        del msg_copy['Resent-Bcc']
        international = False
        try:
            ''.join([from_addr, *to_addrs]).encode('ascii')
        except UnicodeEncodeError:
            if not self.has_extn('smtputf8'):
                raise SMTPNotSupportedError('One or more source or delivery addresses require internationalized email support, but the server does not advertise the required SMTPUTF8 capability')
            else:
                international = True
        else:
            with io.BytesIO() as bytesmsg:
                if international:
                    g = email.generator.BytesGenerator(bytesmsg,
                      policy=msg.policy.clone(utf8=True))
                    mail_options = (*mail_options, *('SMTPUTF8', 'BODY=8BITMIME'))
                else:
                    g = email.generator.BytesGenerator(bytesmsg)
                g.flatten(msg_copy, linesep='\r\n')
                flatmsg = bytesmsg.getvalue()
            return self.sendmail(from_addr, to_addrs, flatmsg, mail_options, rcpt_options)

    def close(self):
        """Close the connection to the SMTP server."""
        try:
            file = self.file
            self.file = None
            if file:
                file.close()
        finally:
            sock = self.sock
            self.sock = None
            if sock:
                sock.close()

    def quit(self):
        """Terminate the SMTP session."""
        res = self.docmd('quit')
        self.ehlo_resp = self.helo_resp = None
        self.esmtp_features = {}
        self.does_esmtp = False
        self.close()
        return res


if _have_ssl:

    class SMTP_SSL(SMTP):
        __doc__ = " This is a subclass derived from SMTP that connects over an SSL\n        encrypted socket (to use this class you need a socket module that was\n        compiled with SSL support). If host is not specified, '' (the local\n        host) is used. If port is omitted, the standard SMTP-over-SSL port\n        (465) is used.  local_hostname and source_address have the same meaning\n        as they do in the SMTP class.  keyfile and certfile are also optional -\n        they can contain a PEM formatted private key and certificate chain file\n        for the SSL connection. context also optional, can contain a\n        SSLContext, and is an alternative to keyfile and certfile; If it is\n        specified both keyfile and certfile must be None.\n\n        "
        default_port = SMTP_SSL_PORT

        def __init__(self, host='', port=0, local_hostname=None, keyfile=None, certfile=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, source_address=None, context=None):
            if context is not None:
                if keyfile is not None:
                    raise ValueError('context and keyfile arguments are mutually exclusive')
            if context is not None:
                if certfile is not None:
                    raise ValueError('context and certfile arguments are mutually exclusive')
            if keyfile is not None or (certfile is not None):
                import warnings
                warnings.warn('keyfile and certfile are deprecated, use a custom context instead', DeprecationWarning, 2)
            self.keyfile = keyfile
            self.certfile = certfile
            if context is None:
                context = ssl._create_stdlib_context(certfile=certfile, keyfile=keyfile)
            self.context = context
            SMTP.__init__(self, host, port, local_hostname, timeout, source_address)

        def _get_socket(self, host, port, timeout):
            if self.debuglevel > 0:
                self._print_debug('connect:', (host, port))
            new_socket = socket.create_connection((host, port), timeout, self.source_address)
            new_socket = self.context.wrap_socket(new_socket, server_hostname=(self._host))
            return new_socket


    __all__.append('SMTP_SSL')
LMTP_PORT = 2003

class LMTP(SMTP):
    __doc__ = "LMTP - Local Mail Transfer Protocol\n\n    The LMTP protocol, which is very similar to ESMTP, is heavily based\n    on the standard SMTP client. It's common to use Unix sockets for\n    LMTP, so our connect() method must support that as well as a regular\n    host:port server.  local_hostname and source_address have the same\n    meaning as they do in the SMTP class.  To specify a Unix socket,\n    you must use an absolute path as the host, starting with a '/'.\n\n    Authentication is supported, using the regular SMTP mechanism. When\n    using a Unix socket, LMTP generally don't support or require any\n    authentication, but your mileage might vary."
    ehlo_msg = 'lhlo'

    def __init__(self, host='', port=LMTP_PORT, local_hostname=None, source_address=None):
        """Initialize a new instance."""
        SMTP.__init__(self, host, port, local_hostname=local_hostname, source_address=source_address)

    def connect(self, host='localhost', port=0, source_address=None):
        """Connect to the LMTP daemon, on either a Unix or a TCP socket."""
        if host[0] != '/':
            return SMTP.connect(self, host, port, source_address=source_address)
        try:
            self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.file = None
            self.sock.connect(host)
        except OSError:
            if self.debuglevel > 0:
                self._print_debug('connect fail:', host)
            else:
                if self.sock:
                    self.sock.close()
                self.sock = None
                raise
        else:
            code, msg = self.getreply()
            if self.debuglevel > 0:
                self._print_debug('connect:', msg)
            else:
                return (
                 code, msg)


if __name__ == '__main__':

    def prompt(prompt):
        sys.stdout.write(prompt + ': ')
        sys.stdout.flush()
        return sys.stdin.readline().strip()


    fromaddr = prompt('From')
    toaddrs = prompt('To').split(',')
    print('Enter message, end with ^D:')
    msg = ''
    while True:
        line = sys.stdin.readline()
        if not line:
            pass
        else:
            msg = msg + line

    print('Message length is %d' % len(msg))
    server = SMTP('localhost')
    server.set_debuglevel(1)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()