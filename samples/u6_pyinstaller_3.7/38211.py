# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\paramiko\auth_handler.py
"""
`.AuthHandler`
"""
import weakref, time
from paramiko.common import cMSG_SERVICE_REQUEST, cMSG_DISCONNECT, DISCONNECT_SERVICE_NOT_AVAILABLE, DISCONNECT_NO_MORE_AUTH_METHODS_AVAILABLE, cMSG_USERAUTH_REQUEST, cMSG_SERVICE_ACCEPT, DEBUG, AUTH_SUCCESSFUL, INFO, cMSG_USERAUTH_SUCCESS, cMSG_USERAUTH_FAILURE, AUTH_PARTIALLY_SUCCESSFUL, cMSG_USERAUTH_INFO_REQUEST, WARNING, AUTH_FAILED, cMSG_USERAUTH_PK_OK, cMSG_USERAUTH_INFO_RESPONSE, MSG_SERVICE_REQUEST, MSG_SERVICE_ACCEPT, MSG_USERAUTH_REQUEST, MSG_USERAUTH_SUCCESS, MSG_USERAUTH_FAILURE, MSG_USERAUTH_BANNER, MSG_USERAUTH_INFO_REQUEST, MSG_USERAUTH_INFO_RESPONSE, cMSG_USERAUTH_GSSAPI_RESPONSE, cMSG_USERAUTH_GSSAPI_TOKEN, cMSG_USERAUTH_GSSAPI_MIC, MSG_USERAUTH_GSSAPI_RESPONSE, MSG_USERAUTH_GSSAPI_TOKEN, MSG_USERAUTH_GSSAPI_ERROR, MSG_USERAUTH_GSSAPI_ERRTOK, MSG_USERAUTH_GSSAPI_MIC, MSG_NAMES, cMSG_USERAUTH_BANNER
from paramiko.message import Message
from paramiko.py3compat import b
from paramiko.ssh_exception import SSHException, AuthenticationException, BadAuthenticationType, PartialAuthentication
from paramiko.server import InteractiveQuery
from paramiko.ssh_gss import GSSAuth, GSS_EXCEPTIONS

class AuthHandler(object):
    __doc__ = '\n    Internal class to handle the mechanics of authentication.\n    '

    def __init__(self, transport):
        self.transport = weakref.proxy(transport)
        self.username = None
        self.authenticated = False
        self.auth_event = None
        self.auth_method = ''
        self.banner = None
        self.password = None
        self.private_key = None
        self.interactive_handler = None
        self.submethods = None
        self.auth_username = None
        self.auth_fail_count = 0
        self.gss_host = None
        self.gss_deleg_creds = True

    def _log(self, *args):
        return (self.transport._log)(*args)

    def is_authenticated(self):
        return self.authenticated

    def get_username(self):
        if self.transport.server_mode:
            return self.auth_username
        return self.username

    def auth_none(self, username, event):
        self.transport.lock.acquire()
        try:
            self.auth_event = event
            self.auth_method = 'none'
            self.username = username
            self._request_auth()
        finally:
            self.transport.lock.release()

    def auth_publickey(self, username, key, event):
        self.transport.lock.acquire()
        try:
            self.auth_event = event
            self.auth_method = 'publickey'
            self.username = username
            self.private_key = key
            self._request_auth()
        finally:
            self.transport.lock.release()

    def auth_password(self, username, password, event):
        self.transport.lock.acquire()
        try:
            self.auth_event = event
            self.auth_method = 'password'
            self.username = username
            self.password = password
            self._request_auth()
        finally:
            self.transport.lock.release()

    def auth_interactive(self, username, handler, event, submethods=''):
        """
        response_list = handler(title, instructions, prompt_list)
        """
        self.transport.lock.acquire()
        try:
            self.auth_event = event
            self.auth_method = 'keyboard-interactive'
            self.username = username
            self.interactive_handler = handler
            self.submethods = submethods
            self._request_auth()
        finally:
            self.transport.lock.release()

    def auth_gssapi_with_mic(self, username, gss_host, gss_deleg_creds, event):
        self.transport.lock.acquire()
        try:
            self.auth_event = event
            self.auth_method = 'gssapi-with-mic'
            self.username = username
            self.gss_host = gss_host
            self.gss_deleg_creds = gss_deleg_creds
            self._request_auth()
        finally:
            self.transport.lock.release()

    def auth_gssapi_keyex(self, username, event):
        self.transport.lock.acquire()
        try:
            self.auth_event = event
            self.auth_method = 'gssapi-keyex'
            self.username = username
            self._request_auth()
        finally:
            self.transport.lock.release()

    def abort(self):
        if self.auth_event is not None:
            self.auth_event.set()

    def _request_auth(self):
        m = Message()
        m.add_byte(cMSG_SERVICE_REQUEST)
        m.add_string('ssh-userauth')
        self.transport._send_message(m)

    def _disconnect_service_not_available(self):
        m = Message()
        m.add_byte(cMSG_DISCONNECT)
        m.add_int(DISCONNECT_SERVICE_NOT_AVAILABLE)
        m.add_string('Service not available')
        m.add_string('en')
        self.transport._send_message(m)
        self.transport.close()

    def _disconnect_no_more_auth(self):
        m = Message()
        m.add_byte(cMSG_DISCONNECT)
        m.add_int(DISCONNECT_NO_MORE_AUTH_METHODS_AVAILABLE)
        m.add_string('No more auth methods available')
        m.add_string('en')
        self.transport._send_message(m)
        self.transport.close()

    def _get_session_blob(self, key, service, username):
        m = Message()
        m.add_string(self.transport.session_id)
        m.add_byte(cMSG_USERAUTH_REQUEST)
        m.add_string(username)
        m.add_string(service)
        m.add_string('publickey')
        m.add_boolean(True)
        if key.public_blob:
            m.add_string(key.public_blob.key_type)
            m.add_string(key.public_blob.key_blob)
        else:
            m.add_string(key.get_name())
            m.add_string(key)
        return m.asbytes()

    def wait_for_response(self, event):
        max_ts = None
        if self.transport.auth_timeout is not None:
            max_ts = time.time() + self.transport.auth_timeout
        while 1:
            event.wait(0.1)
            if not self.transport.is_active():
                e = self.transport.get_exception()
                if e is None or issubclass(e.__class__, EOFError):
                    e = AuthenticationException('Authentication failed.')
                raise e
            if event.is_set():
                break
            if max_ts is not None and max_ts <= time.time():
                raise AuthenticationException('Authentication timeout.')

        if not self.is_authenticated():
            e = self.transport.get_exception()
            if e is None:
                e = AuthenticationException('Authentication failed.')
            if issubclass(e.__class__, PartialAuthentication):
                return e.allowed_types
            raise e
        return []

    def _parse_service_request(self, m):
        service = m.get_text()
        if self.transport.server_mode:
            if service == 'ssh-userauth':
                m = Message()
                m.add_byte(cMSG_SERVICE_ACCEPT)
                m.add_string(service)
                self.transport._send_message(m)
                banner, language = self.transport.server_object.get_banner()
                if banner:
                    m = Message()
                    m.add_byte(cMSG_USERAUTH_BANNER)
                    m.add_string(banner)
                    m.add_string(language)
                    self.transport._send_message(m)
                return
        self._disconnect_service_not_available()

    def _parse_service_accept(self, m):
        service = m.get_text()
        if service == 'ssh-userauth':
            self._log(DEBUG, 'userauth is OK')
            m = Message()
            m.add_byte(cMSG_USERAUTH_REQUEST)
            m.add_string(self.username)
            m.add_string('ssh-connection')
            m.add_string(self.auth_method)
            if self.auth_method == 'password':
                m.add_boolean(False)
                password = b(self.password)
                m.add_string(password)
            else:
                if self.auth_method == 'publickey':
                    m.add_boolean(True)
                    if self.private_key.public_blob:
                        m.add_string(self.private_key.public_blob.key_type)
                        m.add_string(self.private_key.public_blob.key_blob)
                    else:
                        m.add_string(self.private_key.get_name())
                        m.add_string(self.private_key)
                    blob = self._get_session_blob(self.private_key, 'ssh-connection', self.username)
                    sig = self.private_key.sign_ssh_data(blob)
                    m.add_string(sig)
                else:
                    if self.auth_method == 'keyboard-interactive':
                        m.add_string('')
                        m.add_string(self.submethods)
                    else:
                        if self.auth_method == 'gssapi-with-mic':
                            sshgss = GSSAuth(self.auth_method, self.gss_deleg_creds)
                            m.add_bytes(sshgss.ssh_gss_oids())
                            self.transport._send_message(m)
                            ptype, m = self.transport.packetizer.read_message()
                            if ptype == MSG_USERAUTH_BANNER:
                                self._parse_userauth_banner(m)
                                ptype, m = self.transport.packetizer.read_message()
                            if ptype == MSG_USERAUTH_GSSAPI_RESPONSE:
                                mech = m.get_string()
                                m = Message()
                                m.add_byte(cMSG_USERAUTH_GSSAPI_TOKEN)
                                try:
                                    m.add_string(sshgss.ssh_init_sec_context(self.gss_host, mech, self.username))
                                except GSS_EXCEPTIONS as e:
                                    try:
                                        return self._handle_local_gss_failure(e)
                                    finally:
                                        e = None
                                        del e

                                self.transport._send_message(m)
                                while 1:
                                    ptype, m = self.transport.packetizer.read_message()
                                    if ptype == MSG_USERAUTH_GSSAPI_TOKEN:
                                        srv_token = m.get_string()
                                        try:
                                            next_token = sshgss.ssh_init_sec_context(self.gss_host, mech, self.username, srv_token)
                                        except GSS_EXCEPTIONS as e:
                                            try:
                                                return self._handle_local_gss_failure(e)
                                            finally:
                                                e = None
                                                del e

                                        if next_token is None:
                                            break
                                        else:
                                            m = Message()
                                            m.add_byte(cMSG_USERAUTH_GSSAPI_TOKEN)
                                            m.add_string(next_token)
                                            self.transport.send_message(m)
                                else:
                                    raise SSHException('Received Package: {}'.format(MSG_NAMES[ptype]))

                                m = Message()
                                m.add_byte(cMSG_USERAUTH_GSSAPI_MIC)
                                m.add_string(sshgss.ssh_get_mic(self.transport.session_id))
                        elif ptype == MSG_USERAUTH_GSSAPI_ERRTOK:
                            raise SSHException('Server returned an error token')
                        else:
                            if ptype == MSG_USERAUTH_GSSAPI_ERROR:
                                maj_status = m.get_int()
                                min_status = m.get_int()
                                err_msg = m.get_string()
                                m.get_string()
                                raise SSHException('GSS-API Error:\nMajor Status: {}\nMinor Status: {}\nError Message: {}\n'.format(maj_status, min_status, err_msg))
                            else:
                                if ptype == MSG_USERAUTH_FAILURE:
                                    self._parse_userauth_failure(m)
                                    return
                                raise SSHException('Received Package: {}'.format(MSG_NAMES[ptype]))
        else:
            if self.auth_method == 'gssapi-keyex':
                if self.transport.gss_kex_used:
                    kexgss = self.transport.kexgss_ctxt
                    kexgss.set_username(self.username)
                    mic_token = kexgss.ssh_get_mic(self.transport.session_id)
                    m.add_string(mic_token)
                else:
                    if self.auth_method == 'none':
                        pass
                    else:
                        raise SSHException('Unknown auth method "{}"'.format(self.auth_method))
                    self.transport._send_message(m)
            else:
                self._log(DEBUG, 'Service request "{}" accepted (?)'.format(service))

    def _send_auth_result(self, username, method, result):
        m = Message()
        if result == AUTH_SUCCESSFUL:
            self._log(INFO, 'Auth granted ({}).'.format(method))
            m.add_byte(cMSG_USERAUTH_SUCCESS)
            self.authenticated = True
        else:
            self._log(INFO, 'Auth rejected ({}).'.format(method))
            m.add_byte(cMSG_USERAUTH_FAILURE)
            m.add_string(self.transport.server_object.get_allowed_auths(username))
            if result == AUTH_PARTIALLY_SUCCESSFUL:
                m.add_boolean(True)
            else:
                m.add_boolean(False)
                self.auth_fail_count += 1
        self.transport._send_message(m)
        if self.auth_fail_count >= 10:
            self._disconnect_no_more_auth()
        if result == AUTH_SUCCESSFUL:
            self.transport._auth_trigger()

    def _interactive_query(self, q):
        m = Message()
        m.add_byte(cMSG_USERAUTH_INFO_REQUEST)
        m.add_string(q.name)
        m.add_string(q.instructions)
        m.add_string(bytes())
        m.add_int(len(q.prompts))
        for p in q.prompts:
            m.add_string(p[0])
            m.add_boolean(p[1])

        self.transport._send_message(m)

    def _parse_userauth_request--- This code section failed: ---

 L. 444         0  LOAD_FAST                'self'
                2  LOAD_ATTR                transport
                4  LOAD_ATTR                server_mode
                6  POP_JUMP_IF_TRUE     60  'to 60'

 L. 446         8  LOAD_GLOBAL              Message
               10  CALL_FUNCTION_0       0  '0 positional arguments'
               12  STORE_FAST               'm'

 L. 447        14  LOAD_FAST                'm'
               16  LOAD_METHOD              add_byte
               18  LOAD_GLOBAL              cMSG_USERAUTH_FAILURE
               20  CALL_METHOD_1         1  '1 positional argument'
               22  POP_TOP          

 L. 448        24  LOAD_FAST                'm'
               26  LOAD_METHOD              add_string
               28  LOAD_STR                 'none'
               30  CALL_METHOD_1         1  '1 positional argument'
               32  POP_TOP          

 L. 449        34  LOAD_FAST                'm'
               36  LOAD_METHOD              add_boolean
               38  LOAD_CONST               False
               40  CALL_METHOD_1         1  '1 positional argument'
               42  POP_TOP          

 L. 450        44  LOAD_FAST                'self'
               46  LOAD_ATTR                transport
               48  LOAD_METHOD              _send_message
               50  LOAD_FAST                'm'
               52  CALL_METHOD_1         1  '1 positional argument'
               54  POP_TOP          

 L. 451        56  LOAD_CONST               None
               58  RETURN_VALUE     
             60_0  COME_FROM             6  '6'

 L. 452        60  LOAD_FAST                'self'
               62  LOAD_ATTR                authenticated
               64  POP_JUMP_IF_FALSE    70  'to 70'

 L. 454        66  LOAD_CONST               None
               68  RETURN_VALUE     
             70_0  COME_FROM            64  '64'

 L. 455        70  LOAD_FAST                'm'
               72  LOAD_METHOD              get_text
               74  CALL_METHOD_0         0  '0 positional arguments'
               76  STORE_FAST               'username'

 L. 456        78  LOAD_FAST                'm'
               80  LOAD_METHOD              get_text
               82  CALL_METHOD_0         0  '0 positional arguments'
               84  STORE_FAST               'service'

 L. 457        86  LOAD_FAST                'm'
               88  LOAD_METHOD              get_text
               90  CALL_METHOD_0         0  '0 positional arguments'
               92  STORE_FAST               'method'

 L. 458        94  LOAD_FAST                'self'
               96  LOAD_METHOD              _log

 L. 459        98  LOAD_GLOBAL              DEBUG

 L. 460       100  LOAD_STR                 'Auth request (type={}) service={}, username={}'
              102  LOAD_METHOD              format

 L. 461       104  LOAD_FAST                'method'
              106  LOAD_FAST                'service'
              108  LOAD_FAST                'username'
              110  CALL_METHOD_3         3  '3 positional arguments'
              112  CALL_METHOD_2         2  '2 positional arguments'
              114  POP_TOP          

 L. 464       116  LOAD_FAST                'service'
              118  LOAD_STR                 'ssh-connection'
              120  COMPARE_OP               !=
              122  POP_JUMP_IF_FALSE   136  'to 136'

 L. 465       124  LOAD_FAST                'self'
              126  LOAD_METHOD              _disconnect_service_not_available
              128  CALL_METHOD_0         0  '0 positional arguments'
              130  POP_TOP          

 L. 466       132  LOAD_CONST               None
              134  RETURN_VALUE     
            136_0  COME_FROM           122  '122'

 L. 467       136  LOAD_FAST                'self'
              138  LOAD_ATTR                auth_username
              140  LOAD_CONST               None
              142  COMPARE_OP               is-not
              144  POP_JUMP_IF_FALSE   180  'to 180'

 L. 468       146  LOAD_FAST                'self'
              148  LOAD_ATTR                auth_username
              150  LOAD_FAST                'username'
              152  COMPARE_OP               !=
              154  POP_JUMP_IF_FALSE   180  'to 180'

 L. 470       156  LOAD_FAST                'self'
              158  LOAD_METHOD              _log

 L. 471       160  LOAD_GLOBAL              WARNING

 L. 472       162  LOAD_STR                 'Auth rejected because the client attempted to change username in mid-flight'
              164  CALL_METHOD_2         2  '2 positional arguments'
              166  POP_TOP          

 L. 474       168  LOAD_FAST                'self'
              170  LOAD_METHOD              _disconnect_no_more_auth
              172  CALL_METHOD_0         0  '0 positional arguments'
              174  POP_TOP          

 L. 475       176  LOAD_CONST               None
              178  RETURN_VALUE     
            180_0  COME_FROM           154  '154'
            180_1  COME_FROM           144  '144'

 L. 476       180  LOAD_FAST                'username'
              182  LOAD_FAST                'self'
              184  STORE_ATTR               auth_username

 L. 478       186  LOAD_FAST                'self'
              188  LOAD_ATTR                transport
              190  LOAD_ATTR                server_object
              192  LOAD_METHOD              enable_auth_gssapi
              194  CALL_METHOD_0         0  '0 positional arguments'
              196  STORE_FAST               'gss_auth'

 L. 480       198  LOAD_FAST                'method'
              200  LOAD_STR                 'none'
              202  COMPARE_OP               ==
              204  POP_JUMP_IF_FALSE   224  'to 224'

 L. 481       206  LOAD_FAST                'self'
              208  LOAD_ATTR                transport
              210  LOAD_ATTR                server_object
              212  LOAD_METHOD              check_auth_none
              214  LOAD_FAST                'username'
              216  CALL_METHOD_1         1  '1 positional argument'
              218  STORE_FAST               'result'
          220_222  JUMP_FORWARD       1148  'to 1148'
            224_0  COME_FROM           204  '204'

 L. 482       224  LOAD_FAST                'method'
              226  LOAD_STR                 'password'
              228  COMPARE_OP               ==
          230_232  POP_JUMP_IF_FALSE   380  'to 380'

 L. 483       234  LOAD_FAST                'm'
              236  LOAD_METHOD              get_boolean
              238  CALL_METHOD_0         0  '0 positional arguments'
              240  STORE_FAST               'changereq'

 L. 484       242  LOAD_FAST                'm'
              244  LOAD_METHOD              get_binary
              246  CALL_METHOD_0         0  '0 positional arguments'
              248  STORE_FAST               'password'

 L. 485       250  SETUP_EXCEPT        266  'to 266'

 L. 486       252  LOAD_FAST                'password'
              254  LOAD_METHOD              decode
              256  LOAD_STR                 'UTF-8'
              258  CALL_METHOD_1         1  '1 positional argument'
              260  STORE_FAST               'password'
              262  POP_BLOCK        
              264  JUMP_FORWARD        288  'to 288'
            266_0  COME_FROM_EXCEPT    250  '250'

 L. 487       266  DUP_TOP          
              268  LOAD_GLOBAL              UnicodeError
              270  COMPARE_OP               exception-match
          272_274  POP_JUMP_IF_FALSE   286  'to 286'
              276  POP_TOP          
              278  POP_TOP          
              280  POP_TOP          

 L. 490       282  POP_EXCEPT       
              284  JUMP_FORWARD        288  'to 288'
            286_0  COME_FROM           272  '272'
              286  END_FINALLY      
            288_0  COME_FROM           284  '284'
            288_1  COME_FROM           264  '264'

 L. 491       288  LOAD_FAST                'changereq'
          290_292  POP_JUMP_IF_FALSE   360  'to 360'

 L. 495       294  LOAD_FAST                'self'
              296  LOAD_METHOD              _log
              298  LOAD_GLOBAL              DEBUG
              300  LOAD_STR                 'Auth request to change passwords (rejected)'
              302  CALL_METHOD_2         2  '2 positional arguments'
              304  POP_TOP          

 L. 496       306  LOAD_FAST                'm'
              308  LOAD_METHOD              get_binary
              310  CALL_METHOD_0         0  '0 positional arguments'
              312  STORE_FAST               'newpassword'

 L. 497       314  SETUP_EXCEPT        332  'to 332'

 L. 498       316  LOAD_FAST                'newpassword'
              318  LOAD_METHOD              decode
              320  LOAD_STR                 'UTF-8'
              322  LOAD_STR                 'replace'
              324  CALL_METHOD_2         2  '2 positional arguments'
              326  STORE_FAST               'newpassword'
              328  POP_BLOCK        
              330  JUMP_FORWARD        354  'to 354'
            332_0  COME_FROM_EXCEPT    314  '314'

 L. 499       332  DUP_TOP          
              334  LOAD_GLOBAL              UnicodeError
              336  COMPARE_OP               exception-match
          338_340  POP_JUMP_IF_FALSE   352  'to 352'
              342  POP_TOP          
              344  POP_TOP          
              346  POP_TOP          

 L. 500       348  POP_EXCEPT       
              350  JUMP_FORWARD        354  'to 354'
            352_0  COME_FROM           338  '338'
              352  END_FINALLY      
            354_0  COME_FROM           350  '350'
            354_1  COME_FROM           330  '330'

 L. 501       354  LOAD_GLOBAL              AUTH_FAILED
              356  STORE_FAST               'result'
              358  JUMP_FORWARD       1148  'to 1148'
            360_0  COME_FROM           290  '290'

 L. 503       360  LOAD_FAST                'self'
              362  LOAD_ATTR                transport
              364  LOAD_ATTR                server_object
              366  LOAD_METHOD              check_auth_password

 L. 504       368  LOAD_FAST                'username'
              370  LOAD_FAST                'password'
              372  CALL_METHOD_2         2  '2 positional arguments'
              374  STORE_FAST               'result'
          376_378  JUMP_FORWARD       1148  'to 1148'
            380_0  COME_FROM           230  '230'

 L. 506       380  LOAD_FAST                'method'
              382  LOAD_STR                 'publickey'
              384  COMPARE_OP               ==
          386_388  POP_JUMP_IF_FALSE   734  'to 734'

 L. 507       390  LOAD_FAST                'm'
              392  LOAD_METHOD              get_boolean
              394  CALL_METHOD_0         0  '0 positional arguments'
              396  STORE_FAST               'sig_attached'

 L. 508       398  LOAD_FAST                'm'
              400  LOAD_METHOD              get_text
              402  CALL_METHOD_0         0  '0 positional arguments'
              404  STORE_FAST               'keytype'

 L. 509       406  LOAD_FAST                'm'
              408  LOAD_METHOD              get_binary
              410  CALL_METHOD_0         0  '0 positional arguments'
              412  STORE_FAST               'keyblob'

 L. 510       414  SETUP_EXCEPT        440  'to 440'

 L. 511       416  LOAD_FAST                'self'
              418  LOAD_ATTR                transport
              420  LOAD_ATTR                _key_info
              422  LOAD_FAST                'keytype'
              424  BINARY_SUBSCR    
              426  LOAD_GLOBAL              Message
              428  LOAD_FAST                'keyblob'
              430  CALL_FUNCTION_1       1  '1 positional argument'
              432  CALL_FUNCTION_1       1  '1 positional argument'
              434  STORE_FAST               'key'
              436  POP_BLOCK        
              438  JUMP_FORWARD        568  'to 568'
            440_0  COME_FROM_EXCEPT    414  '414'

 L. 512       440  DUP_TOP          
              442  LOAD_GLOBAL              SSHException
              444  COMPARE_OP               exception-match
          446_448  POP_JUMP_IF_FALSE   500  'to 500'
              450  POP_TOP          
              452  STORE_FAST               'e'
              454  POP_TOP          
              456  SETUP_FINALLY       488  'to 488'

 L. 513       458  LOAD_FAST                'self'
              460  LOAD_METHOD              _log
              462  LOAD_GLOBAL              INFO
              464  LOAD_STR                 'Auth rejected: public key: {}'
              466  LOAD_METHOD              format
              468  LOAD_GLOBAL              str
              470  LOAD_FAST                'e'
              472  CALL_FUNCTION_1       1  '1 positional argument'
              474  CALL_METHOD_1         1  '1 positional argument'
              476  CALL_METHOD_2         2  '2 positional arguments'
              478  POP_TOP          

 L. 514       480  LOAD_CONST               None
              482  STORE_FAST               'key'
              484  POP_BLOCK        
              486  LOAD_CONST               None
            488_0  COME_FROM_FINALLY   456  '456'
              488  LOAD_CONST               None
              490  STORE_FAST               'e'
              492  DELETE_FAST              'e'
              494  END_FINALLY      
              496  POP_EXCEPT       
              498  JUMP_FORWARD        568  'to 568'
            500_0  COME_FROM           446  '446'

 L. 515       500  DUP_TOP          
              502  LOAD_GLOBAL              Exception
              504  COMPARE_OP               exception-match
          506_508  POP_JUMP_IF_FALSE   566  'to 566'
              510  POP_TOP          
              512  STORE_FAST               'e'
              514  POP_TOP          
              516  SETUP_FINALLY       554  'to 554'

 L. 517       518  LOAD_STR                 'Auth rejected: unsupported or mangled public key ({}: {})'
              520  STORE_FAST               'msg'

 L. 519       522  LOAD_FAST                'self'
              524  LOAD_METHOD              _log
              526  LOAD_GLOBAL              INFO
              528  LOAD_FAST                'msg'
              530  LOAD_METHOD              format
              532  LOAD_FAST                'e'
              534  LOAD_ATTR                __class__
              536  LOAD_ATTR                __name__
              538  LOAD_FAST                'e'
              540  CALL_METHOD_2         2  '2 positional arguments'
              542  CALL_METHOD_2         2  '2 positional arguments'
              544  POP_TOP          

 L. 520       546  LOAD_CONST               None
              548  STORE_FAST               'key'
              550  POP_BLOCK        
              552  LOAD_CONST               None
            554_0  COME_FROM_FINALLY   516  '516'
              554  LOAD_CONST               None
              556  STORE_FAST               'e'
              558  DELETE_FAST              'e'
              560  END_FINALLY      
              562  POP_EXCEPT       
              564  JUMP_FORWARD        568  'to 568'
            566_0  COME_FROM           506  '506'
              566  END_FINALLY      
            568_0  COME_FROM           564  '564'
            568_1  COME_FROM           498  '498'
            568_2  COME_FROM           438  '438'

 L. 521       568  LOAD_FAST                'key'
              570  LOAD_CONST               None
              572  COMPARE_OP               is
          574_576  POP_JUMP_IF_FALSE   590  'to 590'

 L. 522       578  LOAD_FAST                'self'
              580  LOAD_METHOD              _disconnect_no_more_auth
              582  CALL_METHOD_0         0  '0 positional arguments'
              584  POP_TOP          

 L. 523       586  LOAD_CONST               None
              588  RETURN_VALUE     
            590_0  COME_FROM           574  '574'

 L. 525       590  LOAD_FAST                'self'
              592  LOAD_ATTR                transport
              594  LOAD_ATTR                server_object
              596  LOAD_METHOD              check_auth_publickey

 L. 526       598  LOAD_FAST                'username'
              600  LOAD_FAST                'key'
              602  CALL_METHOD_2         2  '2 positional arguments'
              604  STORE_FAST               'result'

 L. 528       606  LOAD_FAST                'result'
              608  LOAD_GLOBAL              AUTH_FAILED
              610  COMPARE_OP               !=
          612_614  POP_JUMP_IF_FALSE  1148  'to 1148'

 L. 530       616  LOAD_FAST                'sig_attached'
          618_620  POP_JUMP_IF_TRUE    674  'to 674'

 L. 533       622  LOAD_GLOBAL              Message
              624  CALL_FUNCTION_0       0  '0 positional arguments'
              626  STORE_FAST               'm'

 L. 534       628  LOAD_FAST                'm'
              630  LOAD_METHOD              add_byte
              632  LOAD_GLOBAL              cMSG_USERAUTH_PK_OK
              634  CALL_METHOD_1         1  '1 positional argument'
              636  POP_TOP          

 L. 535       638  LOAD_FAST                'm'
              640  LOAD_METHOD              add_string
              642  LOAD_FAST                'keytype'
              644  CALL_METHOD_1         1  '1 positional argument'
              646  POP_TOP          

 L. 536       648  LOAD_FAST                'm'
              650  LOAD_METHOD              add_string
              652  LOAD_FAST                'keyblob'
              654  CALL_METHOD_1         1  '1 positional argument'
              656  POP_TOP          

 L. 537       658  LOAD_FAST                'self'
              660  LOAD_ATTR                transport
              662  LOAD_METHOD              _send_message
              664  LOAD_FAST                'm'
              666  CALL_METHOD_1         1  '1 positional argument'
              668  POP_TOP          

 L. 538       670  LOAD_CONST               None
              672  RETURN_VALUE     
            674_0  COME_FROM           618  '618'

 L. 539       674  LOAD_GLOBAL              Message
              676  LOAD_FAST                'm'
              678  LOAD_METHOD              get_binary
              680  CALL_METHOD_0         0  '0 positional arguments'
              682  CALL_FUNCTION_1       1  '1 positional argument'
              684  STORE_FAST               'sig'

 L. 540       686  LOAD_FAST                'self'
              688  LOAD_METHOD              _get_session_blob
              690  LOAD_FAST                'key'
              692  LOAD_FAST                'service'
              694  LOAD_FAST                'username'
              696  CALL_METHOD_3         3  '3 positional arguments'
              698  STORE_FAST               'blob'

 L. 541       700  LOAD_FAST                'key'
              702  LOAD_METHOD              verify_ssh_sig
              704  LOAD_FAST                'blob'
              706  LOAD_FAST                'sig'
              708  CALL_METHOD_2         2  '2 positional arguments'
          710_712  POP_JUMP_IF_TRUE   1148  'to 1148'

 L. 542       714  LOAD_FAST                'self'
              716  LOAD_METHOD              _log
              718  LOAD_GLOBAL              INFO
              720  LOAD_STR                 'Auth rejected: invalid signature'
              722  CALL_METHOD_2         2  '2 positional arguments'
              724  POP_TOP          

 L. 543       726  LOAD_GLOBAL              AUTH_FAILED
              728  STORE_FAST               'result'
          730_732  JUMP_FORWARD       1148  'to 1148'
            734_0  COME_FROM           386  '386'

 L. 544       734  LOAD_FAST                'method'
              736  LOAD_STR                 'keyboard-interactive'
              738  COMPARE_OP               ==
          740_742  POP_JUMP_IF_FALSE   798  'to 798'

 L. 545       744  LOAD_FAST                'm'
              746  LOAD_METHOD              get_string
              748  CALL_METHOD_0         0  '0 positional arguments'
              750  STORE_FAST               'submethods'

 L. 546       752  LOAD_FAST                'self'
              754  LOAD_ATTR                transport
              756  LOAD_ATTR                server_object
              758  LOAD_METHOD              check_auth_interactive

 L. 547       760  LOAD_FAST                'username'
              762  LOAD_FAST                'submethods'
              764  CALL_METHOD_2         2  '2 positional arguments'
              766  STORE_FAST               'result'

 L. 549       768  LOAD_GLOBAL              isinstance
              770  LOAD_FAST                'result'
              772  LOAD_GLOBAL              InteractiveQuery
              774  CALL_FUNCTION_2       2  '2 positional arguments'
          776_778  POP_JUMP_IF_FALSE  1148  'to 1148'

 L. 551       780  LOAD_FAST                'self'
              782  LOAD_METHOD              _interactive_query
              784  LOAD_FAST                'result'
              786  CALL_METHOD_1         1  '1 positional argument'
              788  POP_TOP          

 L. 552       790  LOAD_CONST               None
              792  RETURN_VALUE     
          794_796  JUMP_FORWARD       1148  'to 1148'
            798_0  COME_FROM           740  '740'

 L. 553       798  LOAD_FAST                'method'
              800  LOAD_STR                 'gssapi-with-mic'
              802  COMPARE_OP               ==
          804_806  POP_JUMP_IF_FALSE   984  'to 984'
              808  LOAD_FAST                'gss_auth'
          810_812  POP_JUMP_IF_FALSE   984  'to 984'

 L. 554       814  LOAD_GLOBAL              GSSAuth
              816  LOAD_FAST                'method'
              818  CALL_FUNCTION_1       1  '1 positional argument'
              820  STORE_FAST               'sshgss'

 L. 558       822  LOAD_FAST                'm'
              824  LOAD_METHOD              get_int
              826  CALL_METHOD_0         0  '0 positional arguments'
              828  STORE_FAST               'mechs'

 L. 561       830  LOAD_FAST                'mechs'
              832  LOAD_CONST               1
              834  COMPARE_OP               >
          836_838  POP_JUMP_IF_FALSE   860  'to 860'

 L. 562       840  LOAD_FAST                'self'
              842  LOAD_METHOD              _log

 L. 563       844  LOAD_GLOBAL              INFO

 L. 564       846  LOAD_STR                 'Disconnect: Received more than one GSS-API OID mechanism'
              848  CALL_METHOD_2         2  '2 positional arguments'
              850  POP_TOP          

 L. 566       852  LOAD_FAST                'self'
              854  LOAD_METHOD              _disconnect_no_more_auth
              856  CALL_METHOD_0         0  '0 positional arguments'
              858  POP_TOP          
            860_0  COME_FROM           836  '836'

 L. 567       860  LOAD_FAST                'm'
              862  LOAD_METHOD              get_string
              864  CALL_METHOD_0         0  '0 positional arguments'
              866  STORE_FAST               'desired_mech'

 L. 568       868  LOAD_FAST                'sshgss'
              870  LOAD_METHOD              ssh_check_mech
              872  LOAD_FAST                'desired_mech'
              874  CALL_METHOD_1         1  '1 positional argument'
              876  STORE_FAST               'mech_ok'

 L. 570       878  LOAD_FAST                'mech_ok'
          880_882  POP_JUMP_IF_TRUE    904  'to 904'

 L. 571       884  LOAD_FAST                'self'
              886  LOAD_METHOD              _log

 L. 572       888  LOAD_GLOBAL              INFO

 L. 573       890  LOAD_STR                 'Disconnect: Received an invalid GSS-API OID mechanism'
              892  CALL_METHOD_2         2  '2 positional arguments'
              894  POP_TOP          

 L. 575       896  LOAD_FAST                'self'
              898  LOAD_METHOD              _disconnect_no_more_auth
              900  CALL_METHOD_0         0  '0 positional arguments'
              902  POP_TOP          
            904_0  COME_FROM           880  '880'

 L. 577       904  LOAD_FAST                'sshgss'
              906  LOAD_METHOD              ssh_gss_oids
              908  LOAD_STR                 'server'
              910  CALL_METHOD_1         1  '1 positional argument'
              912  STORE_FAST               'supported_mech'

 L. 580       914  LOAD_GLOBAL              Message
              916  CALL_FUNCTION_0       0  '0 positional arguments'
              918  STORE_FAST               'm'

 L. 581       920  LOAD_FAST                'm'
              922  LOAD_METHOD              add_byte
              924  LOAD_GLOBAL              cMSG_USERAUTH_GSSAPI_RESPONSE
              926  CALL_METHOD_1         1  '1 positional argument'
              928  POP_TOP          

 L. 582       930  LOAD_FAST                'm'
              932  LOAD_METHOD              add_bytes
              934  LOAD_FAST                'supported_mech'
              936  CALL_METHOD_1         1  '1 positional argument'
              938  POP_TOP          

 L. 583       940  LOAD_GLOBAL              GssapiWithMicAuthHandler

 L. 584       942  LOAD_FAST                'self'
              944  LOAD_FAST                'sshgss'
              946  CALL_FUNCTION_2       2  '2 positional arguments'
              948  LOAD_FAST                'self'
              950  LOAD_ATTR                transport
              952  STORE_ATTR               auth_handler

 L. 587       954  LOAD_GLOBAL              MSG_USERAUTH_GSSAPI_TOKEN

 L. 588       956  LOAD_GLOBAL              MSG_USERAUTH_REQUEST

 L. 589       958  LOAD_GLOBAL              MSG_SERVICE_REQUEST
              960  BUILD_TUPLE_3         3 
              962  LOAD_FAST                'self'
              964  LOAD_ATTR                transport
              966  STORE_ATTR               _expected_packet

 L. 591       968  LOAD_FAST                'self'
              970  LOAD_ATTR                transport
              972  LOAD_METHOD              _send_message
              974  LOAD_FAST                'm'
              976  CALL_METHOD_1         1  '1 positional argument'
              978  POP_TOP          

 L. 592       980  LOAD_CONST               None
              982  RETURN_VALUE     
            984_0  COME_FROM           810  '810'
            984_1  COME_FROM           804  '804'

 L. 593       984  LOAD_FAST                'method'
              986  LOAD_STR                 'gssapi-keyex'
              988  COMPARE_OP               ==
          990_992  POP_JUMP_IF_FALSE  1134  'to 1134'
              994  LOAD_FAST                'gss_auth'
          996_998  POP_JUMP_IF_FALSE  1134  'to 1134'

 L. 594      1000  LOAD_FAST                'm'
             1002  LOAD_METHOD              get_string
             1004  CALL_METHOD_0         0  '0 positional arguments'
             1006  STORE_FAST               'mic_token'

 L. 595      1008  LOAD_FAST                'self'
             1010  LOAD_ATTR                transport
             1012  LOAD_ATTR                kexgss_ctxt
             1014  STORE_FAST               'sshgss'

 L. 596      1016  LOAD_FAST                'sshgss'
             1018  LOAD_CONST               None
             1020  COMPARE_OP               is
         1022_1024  POP_JUMP_IF_FALSE  1044  'to 1044'

 L. 598      1026  LOAD_GLOBAL              AUTH_FAILED
             1028  STORE_FAST               'result'

 L. 599      1030  LOAD_FAST                'self'
             1032  LOAD_METHOD              _send_auth_result
             1034  LOAD_FAST                'username'
             1036  LOAD_FAST                'method'
             1038  LOAD_FAST                'result'
             1040  CALL_METHOD_3         3  '3 positional arguments'
             1042  POP_TOP          
           1044_0  COME_FROM          1022  '1022'

 L. 600      1044  SETUP_EXCEPT       1070  'to 1070'

 L. 601      1046  LOAD_FAST                'sshgss'
             1048  LOAD_METHOD              ssh_check_mic

 L. 602      1050  LOAD_FAST                'mic_token'
             1052  LOAD_FAST                'self'
             1054  LOAD_ATTR                transport
             1056  LOAD_ATTR                session_id
             1058  LOAD_FAST                'self'
             1060  LOAD_ATTR                auth_username
             1062  CALL_METHOD_3         3  '3 positional arguments'
             1064  POP_TOP          
             1066  POP_BLOCK        
             1068  JUMP_FORWARD       1112  'to 1112'
           1070_0  COME_FROM_EXCEPT   1044  '1044'

 L. 604      1070  DUP_TOP          
             1072  LOAD_GLOBAL              Exception
             1074  COMPARE_OP               exception-match
         1076_1078  POP_JUMP_IF_FALSE  1110  'to 1110'
             1080  POP_TOP          
             1082  POP_TOP          
             1084  POP_TOP          

 L. 605      1086  LOAD_GLOBAL              AUTH_FAILED
             1088  STORE_FAST               'result'

 L. 606      1090  LOAD_FAST                'self'
             1092  LOAD_METHOD              _send_auth_result
             1094  LOAD_FAST                'username'
             1096  LOAD_FAST                'method'
             1098  LOAD_FAST                'result'
             1100  CALL_METHOD_3         3  '3 positional arguments'
             1102  POP_TOP          

 L. 607      1104  RAISE_VARARGS_0       0  'reraise'
             1106  POP_EXCEPT       
             1108  JUMP_FORWARD       1112  'to 1112'
           1110_0  COME_FROM          1076  '1076'
             1110  END_FINALLY      
           1112_0  COME_FROM          1108  '1108'
           1112_1  COME_FROM          1068  '1068'

 L. 608      1112  LOAD_GLOBAL              AUTH_SUCCESSFUL
             1114  STORE_FAST               'result'

 L. 609      1116  LOAD_FAST                'self'
             1118  LOAD_ATTR                transport
             1120  LOAD_ATTR                server_object
             1122  LOAD_METHOD              check_auth_gssapi_keyex

 L. 610      1124  LOAD_FAST                'username'
             1126  LOAD_FAST                'result'
           1128_0  COME_FROM           358  '358'
             1128  CALL_METHOD_2         2  '2 positional arguments'
             1130  POP_TOP          
             1132  JUMP_FORWARD       1148  'to 1148'
           1134_0  COME_FROM           996  '996'
           1134_1  COME_FROM           990  '990'

 L. 613      1134  LOAD_FAST                'self'
             1136  LOAD_ATTR                transport
             1138  LOAD_ATTR                server_object
             1140  LOAD_METHOD              check_auth_none
             1142  LOAD_FAST                'username'
             1144  CALL_METHOD_1         1  '1 positional argument'
             1146  STORE_FAST               'result'
           1148_0  COME_FROM          1132  '1132'
           1148_1  COME_FROM           794  '794'
           1148_2  COME_FROM           776  '776'
           1148_3  COME_FROM           730  '730'
           1148_4  COME_FROM           710  '710'
           1148_5  COME_FROM           612  '612'
           1148_6  COME_FROM           376  '376'
           1148_7  COME_FROM           220  '220'

 L. 615      1148  LOAD_FAST                'self'
             1150  LOAD_METHOD              _send_auth_result
             1152  LOAD_FAST                'username'
             1154  LOAD_FAST                'method'
             1156  LOAD_FAST                'result'
             1158  CALL_METHOD_3         3  '3 positional arguments'
             1160  POP_TOP          

Parse error at or near `COME_FROM' instruction at offset 1128_0

    def _parse_userauth_success(self, m):
        self._log(INFO, 'Authentication ({}) successful!'.format(self.auth_method))
        self.authenticated = True
        self.transport._auth_trigger()
        if self.auth_event is not None:
            self.auth_event.set()

    def _parse_userauth_failure(self, m):
        authlist = m.get_list()
        partial = m.get_boolean()
        if partial:
            self._log(INFO, 'Authentication continues...')
            self._log(DEBUG, 'Methods: ' + str(authlist))
            self.transport.saved_exception = PartialAuthentication(authlist)
        else:
            if self.auth_method not in authlist:
                for msg in (
                 'Authentication type ({}) not permitted.'.format(self.auth_method),
                 'Allowed methods: {}'.format(authlist)):
                    self._log(DEBUG, msg)

                self.transport.saved_exception = BadAuthenticationType('Bad authentication type', authlist)
            else:
                self._log(INFO, 'Authentication ({}) failed.'.format(self.auth_method))
        self.authenticated = False
        self.username = None
        if self.auth_event is not None:
            self.auth_event.set()

    def _parse_userauth_banner(self, m):
        banner = m.get_string()
        self.banner = banner
        self._log(INFO, 'Auth banner: {}'.format(banner))

    def _parse_userauth_info_request(self, m):
        if self.auth_method != 'keyboard-interactive':
            raise SSHException('Illegal info request from server')
        title = m.get_text()
        instructions = m.get_text()
        m.get_binary()
        prompts = m.get_int()
        prompt_list = []
        for i in range(prompts):
            prompt_list.append((m.get_text(), m.get_boolean()))

        response_list = self.interactive_handler(title, instructions, prompt_list)
        m = Message()
        m.add_byte(cMSG_USERAUTH_INFO_RESPONSE)
        m.add_int(len(response_list))
        for r in response_list:
            m.add_string(r)

        self.transport._send_message(m)

    def _parse_userauth_info_response(self, m):
        if not self.transport.server_mode:
            raise SSHException('Illegal info response from server')
        n = m.get_int()
        responses = []
        for i in range(n):
            responses.append(m.get_text())

        result = self.transport.server_object.check_auth_interactive_response(responses)
        if isinstance(result, InteractiveQuery):
            self._interactive_query(result)
            return
        self._send_auth_result(self.auth_username, 'keyboard-interactive', result)

    def _handle_local_gss_failure(self, e):
        self.transport.saved_exception = e
        self._log(DEBUG, 'GSSAPI failure: {}'.format(e))
        self._log(INFO, 'Authentication ({}) failed.'.format(self.auth_method))
        self.authenticated = False
        self.username = None
        if self.auth_event is not None:
            self.auth_event.set()

    _server_handler_table = {MSG_SERVICE_REQUEST: _parse_service_request, 
     MSG_USERAUTH_REQUEST: _parse_userauth_request, 
     MSG_USERAUTH_INFO_RESPONSE: _parse_userauth_info_response}
    _client_handler_table = {MSG_SERVICE_ACCEPT: _parse_service_accept, 
     MSG_USERAUTH_SUCCESS: _parse_userauth_success, 
     MSG_USERAUTH_FAILURE: _parse_userauth_failure, 
     MSG_USERAUTH_BANNER: _parse_userauth_banner, 
     MSG_USERAUTH_INFO_REQUEST: _parse_userauth_info_request}

    @property
    def _handler_table(self):
        if self.transport.server_mode:
            return self._server_handler_table
        return self._client_handler_table


class GssapiWithMicAuthHandler(object):
    __doc__ = 'A specialized Auth handler for gssapi-with-mic\n\n    During the GSSAPI token exchange we need a modified dispatch table,\n    because the packet type numbers are not unique.\n    '
    method = 'gssapi-with-mic'

    def __init__(self, delegate, sshgss):
        self._delegate = delegate
        self.sshgss = sshgss

    def abort(self):
        self._restore_delegate_auth_handler()
        return self._delegate.abort()

    @property
    def transport(self):
        return self._delegate.transport

    @property
    def _send_auth_result(self):
        return self._delegate._send_auth_result

    @property
    def auth_username(self):
        return self._delegate.auth_username

    @property
    def gss_host(self):
        return self._delegate.gss_host

    def _restore_delegate_auth_handler(self):
        self.transport.auth_handler = self._delegate

    def _parse_userauth_gssapi_token(self, m):
        client_token = m.get_string()
        sshgss = self.sshgss
        try:
            token = sshgss.ssh_accept_sec_context(self.gss_host, client_token, self.auth_username)
        except Exception as e:
            try:
                self.transport.saved_exception = e
                result = AUTH_FAILED
                self._restore_delegate_auth_handler()
                self._send_auth_result(self.auth_username, self.method, result)
                raise
            finally:
                e = None
                del e

        if token is not None:
            m = Message()
            m.add_byte(cMSG_USERAUTH_GSSAPI_TOKEN)
            m.add_string(token)
            self.transport._expected_packet = (
             MSG_USERAUTH_GSSAPI_TOKEN,
             MSG_USERAUTH_GSSAPI_MIC,
             MSG_USERAUTH_REQUEST)
            self.transport._send_message(m)

    def _parse_userauth_gssapi_mic(self, m):
        mic_token = m.get_string()
        sshgss = self.sshgss
        username = self.auth_username
        self._restore_delegate_auth_handler()
        try:
            sshgss.ssh_check_mic(mic_token, self.transport.session_id, username)
        except Exception as e:
            try:
                self.transport.saved_exception = e
                result = AUTH_FAILED
                self._send_auth_result(username, self.method, result)
                raise
            finally:
                e = None
                del e

        result = AUTH_SUCCESSFUL
        self.transport.server_object.check_auth_gssapi_with_mic(username, result)
        self._send_auth_result(username, self.method, result)

    def _parse_service_request(self, m):
        self._restore_delegate_auth_handler()
        return self._delegate._parse_service_request(m)

    def _parse_userauth_request(self, m):
        self._restore_delegate_auth_handler()
        return self._delegate._parse_userauth_request(m)

    _GssapiWithMicAuthHandler__handler_table = {MSG_SERVICE_REQUEST: _parse_service_request, 
     MSG_USERAUTH_REQUEST: _parse_userauth_request, 
     MSG_USERAUTH_GSSAPI_TOKEN: _parse_userauth_gssapi_token, 
     MSG_USERAUTH_GSSAPI_MIC: _parse_userauth_gssapi_mic}

    @property
    def _handler_table(self):
        return self._GssapiWithMicAuthHandler__handler_table