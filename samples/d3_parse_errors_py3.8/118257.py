# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pymongo\auth.py
"""Authentication helpers."""
import functools, hashlib, hmac, os, socket
try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote
else:
    HAVE_KERBEROS = True
    _USE_PRINCIPAL = False
    try:
        import winkerberos as kerberos
        if tuple(map(int, kerberos.__version__.split('.')[:2])) >= (0, 5):
            _USE_PRINCIPAL = True
    except ImportError:
        try:
            import kerberos
        except ImportError:
            HAVE_KERBEROS = False

    else:
        from base64 import standard_b64decode, standard_b64encode
        from collections import namedtuple
        from bson.binary import Binary
        from bson.py3compat import string_type, _unicode, PY3
        from bson.son import SON
        from pymongo.errors import ConfigurationError, OperationFailure
        import pymongo.saslprep as saslprep
        MECHANISMS = frozenset([
         'GSSAPI',
         'MONGODB-CR',
         'MONGODB-X509',
         'PLAIN',
         'SCRAM-SHA-1',
         'SCRAM-SHA-256',
         'DEFAULT'])

        class _Cache(object):
            __slots__ = ('data', )
            _hash_val = hash('_Cache')

            def __init__(self):
                self.data = None

            def __eq__(self, other):
                if isinstance(other, _Cache):
                    return True
                return NotImplemented

            def __ne__(self, other):
                if isinstance(other, _Cache):
                    return False
                return NotImplemented

            def __hash__(self):
                return self._hash_val


        MongoCredential = namedtuple('MongoCredential', [
         'mechanism',
         'source',
         'username',
         'password',
         'mechanism_properties',
         'cache'])
        GSSAPIProperties = namedtuple('GSSAPIProperties', [
         'service_name',
         'canonicalize_host_name',
         'service_realm'])

        def _build_credentials_tuple(mech, source, user, passwd, extra, database):
            """Build and return a mechanism specific credentials tuple.
    """
            if mech != 'MONGODB-X509':
                if user is None:
                    raise ConfigurationError('%s requires a username.' % (mech,))
            if mech == 'GSSAPI':
                if source is not None:
                    if source != '$external':
                        raise ValueError('authentication source must be $external or None for GSSAPI')
                properties = extra.get('authmechanismproperties', {})
                service_name = properties.get('SERVICE_NAME', 'mongodb')
                canonicalize = properties.get('CANONICALIZE_HOST_NAME', False)
                service_realm = properties.get('SERVICE_REALM')
                props = GSSAPIProperties(service_name=service_name, canonicalize_host_name=canonicalize,
                  service_realm=service_realm)
                return MongoCredential(mech, '$external', user, passwd, props, None)
            if mech == 'MONGODB-X509':
                if passwd is not None:
                    raise ConfigurationError('Passwords are not supported by MONGODB-X509')
                if source is not None:
                    if source != '$external':
                        raise ValueError('authentication source must be $external or None for MONGODB-X509')
                return MongoCredential(mech, '$external', user, None, None, None)
            if mech == 'PLAIN':
                source_database = source or database or '$external'
                return MongoCredential(mech, source_database, user, passwd, None, None)
            source_database = source or database or 'admin'
            if passwd is None:
                raise ConfigurationError('A password is required.')
            return MongoCredential(mech, source_database, user, passwd, None, _Cache())


        if PY3:

            def _xor(fir, sec):
                """XOR two byte strings together (python 3.x)."""
                return (b'').join([bytes([x ^ y]) for x, y in zip(fir, sec)])


            _from_bytes = int.from_bytes
            _to_bytes = int.to_bytes
        else:
            from binascii import hexlify as _hexlify, unhexlify as _unhexlify

            def _xor(fir, sec):
                """XOR two byte strings together (python 2.x)."""
                return (b'').join([chr(ord(x) ^ ord(y)) for x, y in zip(fir, sec)])


            def _from_bytes(value, dummy, _int=int, _hexlify=_hexlify):
                """An implementation of int.from_bytes for python 2.x."""
                return _int(_hexlify(value), 16)


            def _to_bytes(value, length, dummy, _unhexlify=_unhexlify):
                """An implementation of int.to_bytes for python 2.x."""
                fmt = '%%0%dx' % (2 * length,)
                return _unhexlify(fmt % value)


        try:
            import backports.pbkdf2 as _hi
        except ImportError:
            try:
                from hashlib import pbkdf2_hmac as _hi
            except ImportError:

                def _hi(hash_name, data, salt, iterations):
                    """A simple implementation of PBKDF2-HMAC."""
                    mac = hmac.HMAC(data, None, getattr(hashlib, hash_name))

                    def _digest(msg, mac=mac):
                        """Get a digest for msg."""
                        _mac = mac.copy()
                        _mac.update(msg)
                        return _mac.digest()

                    from_bytes = _from_bytes
                    to_bytes = _to_bytes
                    _u1 = _digest(salt + b'\x00\x00\x00\x01')
                    _ui = from_bytes(_u1, 'big')
                    for _ in range(iterations - 1):
                        _u1 = _digest(_u1)
                        _ui ^= from_bytes(_u1, 'big')
                    else:
                        return to_bytes(_ui, mac.digest_size, 'big')


        else:
            try:
                from hmac import compare_digest
            except ImportError:
                if PY3:

                    def _xor_bytes(a, b):
                        return a ^ b


                else:

                    def _xor_bytes(a, b, _ord=ord):
                        return _ord(a) ^ _ord(b)


                def compare_digest(a, b, _xor_bytes=_xor_bytes):
                    left = None
                    right = b
                    if len(a) == len(b):
                        left = a
                        result = 0
                    if len(a) != len(b):
                        left = b
                        result = 1
                    for x, y in zip(left, right):
                        result |= _xor_bytes(x, y)
                    else:
                        return result == 0


            else:

                def _parse_scram_response(response):
                    """Split a scram response into key, value pairs."""
                    return dict((item.split(b'=', 1) for item in response.split(b',')))


                def _authenticate_scram(credentials, sock_info, mechanism):
                    """Authenticate using SCRAM."""
                    username = credentials.username
                    if mechanism == 'SCRAM-SHA-256':
                        digest = 'sha256'
                        digestmod = hashlib.sha256
                        data = saslprep(credentials.password).encode('utf-8')
                    else:
                        digest = 'sha1'
                        digestmod = hashlib.sha1
                        data = _password_digest(username, credentials.password).encode('utf-8')
                    source = credentials.source
                    cache = credentials.cache
                    _hmac = hmac.HMAC
                    user = username.encode('utf-8').replace(b'=', b'=3D').replace(b',', b'=2C')
                    nonce = standard_b64encode(os.urandom(32))
                    first_bare = b'n=' + user + b',r=' + nonce
                    cmd = SON([('saslStart', 1),
                     (
                      'mechanism', mechanism),
                     (
                      'payload', Binary(b'n,,' + first_bare)),
                     ('autoAuthorize', 1)])
                    res = sock_info.command(source, cmd)
                    server_first = res['payload']
                    parsed = _parse_scram_response(server_first)
                    iterations = int(parsed[b'i'])
                    if iterations < 4096:
                        raise OperationFailure('Server returned an invalid iteration count.')
                    salt = parsed[b's']
                    rnonce = parsed[b'r']
                    if not rnonce.startswith(nonce):
                        raise OperationFailure('Server returned an invalid nonce.')
                    without_proof = b'c=biws,r=' + rnonce
                    if cache.data:
                        client_key, server_key, csalt, citerations = cache.data
                    else:
                        client_key, server_key, csalt, citerations = (None, None, None,
                                                                      None)
                    if client_key and salt != csalt or iterations != citerations:
                        salted_pass = _hi(digest, data, standard_b64decode(salt), iterations)
                        client_key = _hmac(salted_pass, b'Client Key', digestmod).digest()
                        server_key = _hmac(salted_pass, b'Server Key', digestmod).digest()
                        cache.data = (client_key, server_key, salt, iterations)
                    stored_key = digestmod(client_key).digest()
                    auth_msg = (b',').join((first_bare, server_first, without_proof))
                    client_sig = _hmac(stored_key, auth_msg, digestmod).digest()
                    client_proof = b'p=' + standard_b64encode(_xor(client_key, client_sig))
                    client_final = (b',').join((without_proof, client_proof))
                    server_sig = standard_b64encode(_hmac(server_key, auth_msg, digestmod).digest())
                    cmd = SON([('saslContinue', 1),
                     (
                      'conversationId', res['conversationId']),
                     (
                      'payload', Binary(client_final))])
                    res = sock_info.command(source, cmd)
                    parsed = _parse_scram_response(res['payload'])
                    if not compare_digest(parsed[b'v'], server_sig):
                        raise OperationFailure('Server returned an invalid signature.')
                    cmd = res['done'] or SON([('saslContinue', 1),
                     (
                      'conversationId', res['conversationId']),
                     (
                      'payload', Binary(b''))])
                    res = sock_info.command(source, cmd)
                    if not res['done']:
                        raise OperationFailure('SASL conversation failed to complete.')


                def _password_digest(username, password):
                    """Get a password digest to use for authentication.
    """
                    if not isinstance(password, string_type):
                        raise TypeError('password must be an instance of %s' % (
                         string_type.__name__,))
                    if len(password) == 0:
                        raise ValueError("password can't be empty")
                    if not isinstance(username, string_type):
                        raise TypeError('password must be an instance of  %s' % (
                         string_type.__name__,))
                    md5hash = hashlib.md5()
                    data = '%s:mongo:%s' % (username, password)
                    md5hash.update(data.encode('utf-8'))
                    return _unicode(md5hash.hexdigest())


                def _auth_key(nonce, username, password):
                    """Get an auth key to use for authentication.
    """
                    digest = _password_digest(username, password)
                    md5hash = hashlib.md5()
                    data = '%s%s%s' % (nonce, username, digest)
                    md5hash.update(data.encode('utf-8'))
                    return _unicode(md5hash.hexdigest())


                def _authenticate_gssapi--- This code section failed: ---

 L. 349         0  LOAD_GLOBAL              HAVE_KERBEROS
                2  POP_JUMP_IF_TRUE     12  'to 12'

 L. 350         4  LOAD_GLOBAL              ConfigurationError
                6  LOAD_STR                 'The "kerberos" module must be installed to use GSSAPI authentication.'
                8  CALL_FUNCTION_1       1  ''
               10  RAISE_VARARGS_1       1  'exception instance'
             12_0  COME_FROM             2  '2'

 L. 353     12_14  SETUP_FINALLY       602  'to 602'

 L. 354        16  LOAD_FAST                'credentials'
               18  LOAD_ATTR                username
               20  STORE_FAST               'username'

 L. 355        22  LOAD_FAST                'credentials'
               24  LOAD_ATTR                password
               26  STORE_FAST               'password'

 L. 356        28  LOAD_FAST                'credentials'
               30  LOAD_ATTR                mechanism_properties
               32  STORE_FAST               'props'

 L. 359        34  LOAD_FAST                'sock_info'
               36  LOAD_ATTR                address
               38  LOAD_CONST               0
               40  BINARY_SUBSCR    
               42  STORE_FAST               'host'

 L. 360        44  LOAD_FAST                'props'
               46  LOAD_ATTR                canonicalize_host_name
               48  POP_JUMP_IF_FALSE    60  'to 60'

 L. 361        50  LOAD_GLOBAL              socket
               52  LOAD_METHOD              getfqdn
               54  LOAD_FAST                'host'
               56  CALL_METHOD_1         1  ''
               58  STORE_FAST               'host'
             60_0  COME_FROM            48  '48'

 L. 362        60  LOAD_FAST                'props'
               62  LOAD_ATTR                service_name
               64  LOAD_STR                 '@'
               66  BINARY_ADD       
               68  LOAD_FAST                'host'
               70  BINARY_ADD       
               72  STORE_FAST               'service'

 L. 363        74  LOAD_FAST                'props'
               76  LOAD_ATTR                service_realm
               78  LOAD_CONST               None
               80  COMPARE_OP               is-not
               82  POP_JUMP_IF_FALSE    98  'to 98'

 L. 364        84  LOAD_FAST                'service'
               86  LOAD_STR                 '@'
               88  BINARY_ADD       
               90  LOAD_FAST                'props'
               92  LOAD_ATTR                service_realm
               94  BINARY_ADD       
               96  STORE_FAST               'service'
             98_0  COME_FROM            82  '82'

 L. 366        98  LOAD_FAST                'password'
              100  LOAD_CONST               None
              102  COMPARE_OP               is-not
              104  POP_JUMP_IF_FALSE   220  'to 220'

 L. 367       106  LOAD_GLOBAL              _USE_PRINCIPAL
              108  POP_JUMP_IF_FALSE   156  'to 156'

 L. 371       110  LOAD_STR                 ':'
              112  LOAD_METHOD              join
              114  LOAD_GLOBAL              quote
              116  LOAD_FAST                'username'
              118  CALL_FUNCTION_1       1  ''
              120  LOAD_GLOBAL              quote
              122  LOAD_FAST                'password'
              124  CALL_FUNCTION_1       1  ''
              126  BUILD_TUPLE_2         2 
              128  CALL_METHOD_1         1  ''
              130  STORE_FAST               'principal'

 L. 372       132  LOAD_GLOBAL              kerberos
              134  LOAD_ATTR                authGSSClientInit

 L. 373       136  LOAD_FAST                'service'

 L. 373       138  LOAD_FAST                'principal'

 L. 373       140  LOAD_GLOBAL              kerberos
              142  LOAD_ATTR                GSS_C_MUTUAL_FLAG

 L. 372       144  LOAD_CONST               ('gssflags',)
              146  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              148  UNPACK_SEQUENCE_2     2 
              150  STORE_FAST               'result'
              152  STORE_FAST               'ctx'
              154  JUMP_FORWARD        240  'to 240'
            156_0  COME_FROM           108  '108'

 L. 375       156  LOAD_STR                 '@'
              158  LOAD_FAST                'username'
              160  COMPARE_OP               in
              162  POP_JUMP_IF_FALSE   182  'to 182'

 L. 376       164  LOAD_FAST                'username'
              166  LOAD_METHOD              split
              168  LOAD_STR                 '@'
              170  LOAD_CONST               1
              172  CALL_METHOD_2         2  ''
              174  UNPACK_SEQUENCE_2     2 
              176  STORE_FAST               'user'
              178  STORE_FAST               'domain'
              180  JUMP_FORWARD        192  'to 192'
            182_0  COME_FROM           162  '162'

 L. 378       182  LOAD_FAST                'username'
              184  LOAD_CONST               None
              186  ROT_TWO          
              188  STORE_FAST               'user'
              190  STORE_FAST               'domain'
            192_0  COME_FROM           180  '180'

 L. 379       192  LOAD_GLOBAL              kerberos
              194  LOAD_ATTR                authGSSClientInit

 L. 380       196  LOAD_FAST                'service'

 L. 380       198  LOAD_GLOBAL              kerberos
              200  LOAD_ATTR                GSS_C_MUTUAL_FLAG

 L. 381       202  LOAD_FAST                'user'

 L. 381       204  LOAD_FAST                'domain'

 L. 381       206  LOAD_FAST                'password'

 L. 379       208  LOAD_CONST               ('gssflags', 'user', 'domain', 'password')
              210  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              212  UNPACK_SEQUENCE_2     2 
              214  STORE_FAST               'result'
              216  STORE_FAST               'ctx'
              218  JUMP_FORWARD        240  'to 240'
            220_0  COME_FROM           104  '104'

 L. 383       220  LOAD_GLOBAL              kerberos
              222  LOAD_ATTR                authGSSClientInit

 L. 384       224  LOAD_FAST                'service'

 L. 384       226  LOAD_GLOBAL              kerberos
              228  LOAD_ATTR                GSS_C_MUTUAL_FLAG

 L. 383       230  LOAD_CONST               ('gssflags',)
              232  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              234  UNPACK_SEQUENCE_2     2 
              236  STORE_FAST               'result'
              238  STORE_FAST               'ctx'
            240_0  COME_FROM           218  '218'
            240_1  COME_FROM           154  '154'

 L. 386       240  LOAD_FAST                'result'
              242  LOAD_GLOBAL              kerberos
              244  LOAD_ATTR                AUTH_GSS_COMPLETE
              246  COMPARE_OP               !=
          248_250  POP_JUMP_IF_FALSE   260  'to 260'

 L. 387       252  LOAD_GLOBAL              OperationFailure
              254  LOAD_STR                 'Kerberos context failed to initialize.'
              256  CALL_FUNCTION_1       1  ''
              258  RAISE_VARARGS_1       1  'exception instance'
            260_0  COME_FROM           248  '248'

 L. 389   260_262  SETUP_FINALLY       586  'to 586'

 L. 394       264  LOAD_GLOBAL              kerberos
              266  LOAD_METHOD              authGSSClientStep
              268  LOAD_FAST                'ctx'
              270  LOAD_STR                 ''
              272  CALL_METHOD_2         2  ''
              274  LOAD_CONST               0
              276  COMPARE_OP               !=
          278_280  POP_JUMP_IF_FALSE   290  'to 290'

 L. 395       282  LOAD_GLOBAL              OperationFailure
              284  LOAD_STR                 'Unknown kerberos failure in step function.'
              286  CALL_FUNCTION_1       1  ''
              288  RAISE_VARARGS_1       1  'exception instance'
            290_0  COME_FROM           278  '278'

 L. 402       290  LOAD_GLOBAL              kerberos
              292  LOAD_METHOD              authGSSClientResponse
              294  LOAD_FAST                'ctx'
              296  CALL_METHOD_1         1  ''
              298  STORE_FAST               'payload'

 L. 403       300  LOAD_GLOBAL              SON
              302  LOAD_CONST               ('saslStart', 1)

 L. 404       304  LOAD_CONST               ('mechanism', 'GSSAPI')

 L. 405       306  LOAD_STR                 'payload'
              308  LOAD_FAST                'payload'
              310  BUILD_TUPLE_2         2 

 L. 406       312  LOAD_CONST               ('autoAuthorize', 1)

 L. 403       314  BUILD_LIST_4          4 
              316  CALL_FUNCTION_1       1  ''
              318  STORE_FAST               'cmd'

 L. 407       320  LOAD_FAST                'sock_info'
              322  LOAD_METHOD              command
              324  LOAD_STR                 '$external'
              326  LOAD_FAST                'cmd'
              328  CALL_METHOD_2         2  ''
              330  STORE_FAST               'response'

 L. 410       332  LOAD_GLOBAL              range
              334  LOAD_CONST               10
              336  CALL_FUNCTION_1       1  ''
              338  GET_ITER         
            340_0  COME_FROM           454  '454'
            340_1  COME_FROM           444  '444'
              340  FOR_ITER            458  'to 458'
              342  STORE_FAST               '_'

 L. 411       344  LOAD_GLOBAL              kerberos
              346  LOAD_METHOD              authGSSClientStep
              348  LOAD_FAST                'ctx'

 L. 412       350  LOAD_GLOBAL              str
              352  LOAD_FAST                'response'
              354  LOAD_STR                 'payload'
              356  BINARY_SUBSCR    
              358  CALL_FUNCTION_1       1  ''

 L. 411       360  CALL_METHOD_2         2  ''
              362  STORE_FAST               'result'

 L. 413       364  LOAD_FAST                'result'
              366  LOAD_CONST               -1
              368  COMPARE_OP               ==
          370_372  POP_JUMP_IF_FALSE   382  'to 382'

 L. 414       374  LOAD_GLOBAL              OperationFailure
              376  LOAD_STR                 'Unknown kerberos failure in step function.'
              378  CALL_FUNCTION_1       1  ''
              380  RAISE_VARARGS_1       1  'exception instance'
            382_0  COME_FROM           370  '370'

 L. 417       382  LOAD_GLOBAL              kerberos
              384  LOAD_METHOD              authGSSClientResponse
              386  LOAD_FAST                'ctx'
              388  CALL_METHOD_1         1  ''
          390_392  JUMP_IF_TRUE_OR_POP   396  'to 396'
              394  LOAD_STR                 ''
            396_0  COME_FROM           390  '390'
              396  STORE_FAST               'payload'

 L. 419       398  LOAD_GLOBAL              SON
              400  LOAD_CONST               ('saslContinue', 1)

 L. 420       402  LOAD_STR                 'conversationId'
              404  LOAD_FAST                'response'
              406  LOAD_STR                 'conversationId'
              408  BINARY_SUBSCR    
              410  BUILD_TUPLE_2         2 

 L. 421       412  LOAD_STR                 'payload'
              414  LOAD_FAST                'payload'
              416  BUILD_TUPLE_2         2 

 L. 419       418  BUILD_LIST_3          3 
              420  CALL_FUNCTION_1       1  ''
              422  STORE_FAST               'cmd'

 L. 422       424  LOAD_FAST                'sock_info'
              426  LOAD_METHOD              command
              428  LOAD_STR                 '$external'
              430  LOAD_FAST                'cmd'
              432  CALL_METHOD_2         2  ''
              434  STORE_FAST               'response'

 L. 424       436  LOAD_FAST                'result'
              438  LOAD_GLOBAL              kerberos
              440  LOAD_ATTR                AUTH_GSS_COMPLETE
              442  COMPARE_OP               ==
          444_446  POP_JUMP_IF_FALSE_BACK   340  'to 340'

 L. 425       448  POP_TOP          
          450_452  BREAK_LOOP          466  'to 466'
          454_456  JUMP_BACK           340  'to 340'
            458_0  COME_FROM           340  '340'

 L. 427       458  LOAD_GLOBAL              OperationFailure
              460  LOAD_STR                 'Kerberos authentication failed to complete.'
              462  CALL_FUNCTION_1       1  ''
              464  RAISE_VARARGS_1       1  'exception instance'
            466_0  COME_FROM           450  '450'

 L. 432       466  LOAD_GLOBAL              kerberos
              468  LOAD_METHOD              authGSSClientUnwrap
              470  LOAD_FAST                'ctx'

 L. 433       472  LOAD_GLOBAL              str
              474  LOAD_FAST                'response'
              476  LOAD_STR                 'payload'
              478  BINARY_SUBSCR    
              480  CALL_FUNCTION_1       1  ''

 L. 432       482  CALL_METHOD_2         2  ''

 L. 433       484  LOAD_CONST               1

 L. 432       486  COMPARE_OP               !=
          488_490  POP_JUMP_IF_FALSE   500  'to 500'

 L. 434       492  LOAD_GLOBAL              OperationFailure
              494  LOAD_STR                 'Unknown kerberos failure during GSS_Unwrap step.'
              496  CALL_FUNCTION_1       1  ''
              498  RAISE_VARARGS_1       1  'exception instance'
            500_0  COME_FROM           488  '488'

 L. 437       500  LOAD_GLOBAL              kerberos
              502  LOAD_METHOD              authGSSClientWrap
              504  LOAD_FAST                'ctx'

 L. 438       506  LOAD_GLOBAL              kerberos
              508  LOAD_METHOD              authGSSClientResponse
              510  LOAD_FAST                'ctx'
              512  CALL_METHOD_1         1  ''

 L. 439       514  LOAD_FAST                'username'

 L. 437       516  CALL_METHOD_3         3  ''

 L. 439       518  LOAD_CONST               1

 L. 437       520  COMPARE_OP               !=
          522_524  POP_JUMP_IF_FALSE   534  'to 534'

 L. 440       526  LOAD_GLOBAL              OperationFailure
              528  LOAD_STR                 'Unknown kerberos failure during GSS_Wrap step.'
              530  CALL_FUNCTION_1       1  ''
              532  RAISE_VARARGS_1       1  'exception instance'
            534_0  COME_FROM           522  '522'

 L. 443       534  LOAD_GLOBAL              kerberos
              536  LOAD_METHOD              authGSSClientResponse
              538  LOAD_FAST                'ctx'
              540  CALL_METHOD_1         1  ''
              542  STORE_FAST               'payload'

 L. 444       544  LOAD_GLOBAL              SON
              546  LOAD_CONST               ('saslContinue', 1)

 L. 445       548  LOAD_STR                 'conversationId'
              550  LOAD_FAST                'response'
              552  LOAD_STR                 'conversationId'
              554  BINARY_SUBSCR    
              556  BUILD_TUPLE_2         2 

 L. 446       558  LOAD_STR                 'payload'
              560  LOAD_FAST                'payload'
              562  BUILD_TUPLE_2         2 

 L. 444       564  BUILD_LIST_3          3 
              566  CALL_FUNCTION_1       1  ''
              568  STORE_FAST               'cmd'

 L. 447       570  LOAD_FAST                'sock_info'
              572  LOAD_METHOD              command
              574  LOAD_STR                 '$external'
              576  LOAD_FAST                'cmd'
              578  CALL_METHOD_2         2  ''
              580  POP_TOP          
              582  POP_BLOCK        
              584  BEGIN_FINALLY    
            586_0  COME_FROM_FINALLY   260  '260'

 L. 450       586  LOAD_GLOBAL              kerberos
              588  LOAD_METHOD              authGSSClientClean
              590  LOAD_FAST                'ctx'
              592  CALL_METHOD_1         1  ''
              594  POP_TOP          
              596  END_FINALLY      
              598  POP_BLOCK        
              600  JUMP_FORWARD        652  'to 652'
            602_0  COME_FROM_FINALLY    12  '12'

 L. 452       602  DUP_TOP          
              604  LOAD_GLOBAL              kerberos
              606  LOAD_ATTR                KrbError
              608  COMPARE_OP               exception-match
          610_612  POP_JUMP_IF_FALSE   650  'to 650'
              614  POP_TOP          
              616  STORE_FAST               'exc'
              618  POP_TOP          
              620  SETUP_FINALLY       638  'to 638'

 L. 453       622  LOAD_GLOBAL              OperationFailure
              624  LOAD_GLOBAL              str
              626  LOAD_FAST                'exc'
              628  CALL_FUNCTION_1       1  ''
              630  CALL_FUNCTION_1       1  ''
              632  RAISE_VARARGS_1       1  'exception instance'
              634  POP_BLOCK        
              636  BEGIN_FINALLY    
            638_0  COME_FROM_FINALLY   620  '620'
              638  LOAD_CONST               None
              640  STORE_FAST               'exc'
              642  DELETE_FAST              'exc'
              644  END_FINALLY      
              646  POP_EXCEPT       
              648  JUMP_FORWARD        652  'to 652'
            650_0  COME_FROM           610  '610'
              650  END_FINALLY      
            652_0  COME_FROM           648  '648'
            652_1  COME_FROM           600  '600'

Parse error at or near `BEGIN_FINALLY' instruction at offset 584


                def _authenticate_plain(credentials, sock_info):
                    """Authenticate using SASL PLAIN (RFC 4616)
    """
                    source = credentials.source
                    username = credentials.username
                    password = credentials.password
                    payload = ('\x00%s\x00%s' % (username, password)).encode('utf-8')
                    cmd = SON([('saslStart', 1),
                     ('mechanism', 'PLAIN'),
                     (
                      'payload', Binary(payload)),
                     ('autoAuthorize', 1)])
                    sock_info.command(source, cmd)


                def _authenticate_cram_md5(credentials, sock_info):
                    """Authenticate using CRAM-MD5 (RFC 2195)
    """
                    source = credentials.source
                    username = credentials.username
                    password = credentials.password
                    passwd = _password_digest(username, password)
                    cmd = SON([('saslStart', 1),
                     ('mechanism', 'CRAM-MD5'),
                     (
                      'payload', Binary(b'')),
                     ('autoAuthorize', 1)])
                    response = sock_info.command(source, cmd)
                    mac = hmac.HMAC(key=(passwd.encode('utf-8')), digestmod=(hashlib.md5))
                    mac.update(response['payload'])
                    challenge = username.encode('utf-8') + b' ' + mac.hexdigest().encode('utf-8')
                    cmd = SON([('saslContinue', 1),
                     (
                      'conversationId', response['conversationId']),
                     (
                      'payload', Binary(challenge))])
                    sock_info.command(source, cmd)


                def _authenticate_x509(credentials, sock_info):
                    """Authenticate using MONGODB-X509.
    """
                    query = SON([('authenticate', 1),
                     ('mechanism', 'MONGODB-X509')])
                    if credentials.username is not None:
                        query['user'] = credentials.username
                    elif sock_info.max_wire_version < 5:
                        raise ConfigurationError('A username is required for MONGODB-X509 authentication when connected to MongoDB versions older than 3.4.')
                    sock_info.command('$external', query)


                def _authenticate_mongo_cr(credentials, sock_info):
                    """Authenticate using MONGODB-CR.
    """
                    source = credentials.source
                    username = credentials.username
                    password = credentials.password
                    response = sock_info.command(source, {'getnonce': 1})
                    nonce = response['nonce']
                    key = _auth_key(nonce, username, password)
                    query = SON([('authenticate', 1),
                     (
                      'user', username),
                     (
                      'nonce', nonce),
                     (
                      'key', key)])
                    sock_info.command(source, query)


                def _authenticate_default(credentials, sock_info):
                    if sock_info.max_wire_version >= 7:
                        source = credentials.source
                        cmd = SON([
                         ('ismaster', 1),
                         (
                          'saslSupportedMechs', source + '.' + credentials.username)])
                        mechs = sock_info.command(source,
                          cmd, publish_events=False).get('saslSupportedMechs', [])
                        if 'SCRAM-SHA-256' in mechs:
                            return _authenticate_scram(credentials, sock_info, 'SCRAM-SHA-256')
                        return _authenticate_scram(credentials, sock_info, 'SCRAM-SHA-1')
                    else:
                        if sock_info.max_wire_version >= 3:
                            return _authenticate_scram(credentials, sock_info, 'SCRAM-SHA-1')
                        return _authenticate_mongo_cr(credentials, sock_info)


                _AUTH_MAP = {'CRAM-MD5':_authenticate_cram_md5, 
                 'GSSAPI':_authenticate_gssapi, 
                 'MONGODB-CR':_authenticate_mongo_cr, 
                 'MONGODB-X509':_authenticate_x509, 
                 'PLAIN':_authenticate_plain, 
                 'SCRAM-SHA-1':functools.partial(_authenticate_scram,
                   mechanism='SCRAM-SHA-1'), 
                 'SCRAM-SHA-256':functools.partial(_authenticate_scram,
                   mechanism='SCRAM-SHA-256'), 
                 'DEFAULT':_authenticate_default}

                def authenticate(credentials, sock_info):
                    """Authenticate sock_info."""
                    mechanism = credentials.mechanism
                    auth_func = _AUTH_MAP.get(mechanism)
                    auth_func(credentials, sock_info)


                def logout(source, sock_info):
                    """Log out from a database."""
                    sock_info.command(source, {'logout': 1})