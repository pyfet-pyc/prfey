# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pymongo\encryption.py
"""Support for explicit client-side field level encryption."""
import contextlib, os, subprocess, uuid, weakref
try:
    from pymongocrypt.auto_encrypter import AutoEncrypter
    from pymongocrypt.errors import MongoCryptError
    from pymongocrypt.explicit_encrypter import ExplicitEncrypter
    from pymongocrypt.mongocrypt import MongoCryptOptions
    from pymongocrypt.state_machine import MongoCryptCallback
    _HAVE_PYMONGOCRYPT = True
except ImportError:
    _HAVE_PYMONGOCRYPT = False
    MongoCryptCallback = object
else:
    from bson import _dict_to_bson, decode, encode
    from bson.codec_options import CodecOptions
    from bson.binary import Binary, STANDARD, UUID_SUBTYPE
    from bson.errors import BSONError
    from bson.raw_bson import DEFAULT_RAW_BSON_OPTIONS, RawBSONDocument, _inflate_bson
    from bson.son import SON
    from pymongo.errors import ConfigurationError, EncryptionError, InvalidOperation, ServerSelectionTimeoutError
    from pymongo.mongo_client import MongoClient
    from pymongo.pool import _configured_socket, PoolOptions
    from pymongo.read_concern import ReadConcern
    from pymongo.ssl_support import get_ssl_context
    from pymongo.uri_parser import parse_host
    from pymongo.write_concern import WriteConcern
    from pymongo.daemon import _spawn_daemon
    _HTTPS_PORT = 443
    _KMS_CONNECT_TIMEOUT = 10
    _MONGOCRYPTD_TIMEOUT_MS = 1000
    _DATA_KEY_OPTS = CodecOptions(document_class=SON, uuid_representation=STANDARD)
    _KEY_VAULT_OPTS = CodecOptions(document_class=RawBSONDocument, uuid_representation=STANDARD)

    @contextlib.contextmanager
    def _wrap_encryption_errors():
        """Context manager to wrap encryption related errors."""
        try:
            yield
        except BSONError:
            raise
        except Exception as exc:
            try:
                raise EncryptionError(exc)
            finally:
                exc = None
                del exc


    class _EncryptionIO(MongoCryptCallback):

        def __init__(self, client, key_vault_coll, mongocryptd_client, opts):
            """Internal class to perform I/O on behalf of pymongocrypt."""
            if client is not None:
                self.client_ref = weakref.ref(client)
            else:
                self.client_ref = None
            self.key_vault_coll = key_vault_coll.with_options(codec_options=_KEY_VAULT_OPTS,
              read_concern=ReadConcern(level='majority'),
              write_concern=WriteConcern(w='majority'))
            self.mongocryptd_client = mongocryptd_client
            self.opts = opts
            self._spawned = False

        def kms_request(self, kms_context):
            """Complete a KMS request.

        :Parameters:
          - `kms_context`: A :class:`MongoCryptKmsContext`.

        :Returns:
          None
        """
            endpoint = kms_context.endpoint
            message = kms_context.message
            host, port = parse_host(endpoint, _HTTPS_PORT)
            ctx = get_ssl_context(None, None, None, None, None, None, True)
            opts = PoolOptions(connect_timeout=_KMS_CONNECT_TIMEOUT, socket_timeout=_KMS_CONNECT_TIMEOUT,
              ssl_context=ctx)
            conn = _configured_socket((host, port), opts)
            try:
                conn.sendall(message)
                while kms_context.bytes_needed > 0:
                    data = conn.recv(kms_context.bytes_needed)
                    kms_context.feed(data)

            finally:
                conn.close()

        def collection_info--- This code section failed: ---

 L. 136         0  LOAD_FAST                'self'
                2  LOAD_METHOD              client_ref
                4  CALL_METHOD_0         0  ''
                6  LOAD_FAST                'database'
                8  BINARY_SUBSCR    
               10  LOAD_ATTR                list_collections

 L. 137        12  LOAD_GLOBAL              RawBSONDocument
               14  LOAD_FAST                'filter'
               16  CALL_FUNCTION_1       1  ''

 L. 136        18  LOAD_CONST               ('filter',)
               20  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               22  SETUP_WITH           66  'to 66'

 L. 137        24  STORE_FAST               'cursor'

 L. 138        26  LOAD_FAST                'cursor'
               28  GET_ITER         
               30  FOR_ITER             62  'to 62'
               32  STORE_FAST               'doc'

 L. 139        34  LOAD_GLOBAL              _dict_to_bson
               36  LOAD_FAST                'doc'
               38  LOAD_CONST               False
               40  LOAD_GLOBAL              _DATA_KEY_OPTS
               42  CALL_FUNCTION_3       3  ''
               44  ROT_TWO          
               46  POP_TOP          
               48  POP_BLOCK        
               50  ROT_TWO          
               52  BEGIN_FINALLY    
               54  WITH_CLEANUP_START
               56  WITH_CLEANUP_FINISH
               58  POP_FINALLY           0  ''
               60  RETURN_VALUE     
               62  POP_BLOCK        
               64  BEGIN_FINALLY    
             66_0  COME_FROM_WITH       22  '22'
               66  WITH_CLEANUP_START
               68  WITH_CLEANUP_FINISH
               70  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 48

        def spawn(self):
            """Spawn mongocryptd.

        Note this method is thread safe; at most one mongocryptd will start
        successfully.
        """
            self._spawned = True
            args = [self.opts._mongocryptd_spawn_path or 'mongocryptd']
            args.extend(self.opts._mongocryptd_spawn_args)
            _spawn_daemon(args)

        def mark_command(self, database, cmd):
            """Mark a command for encryption.

        :Parameters:
          - `database`: The database on which to run this command.
          - `cmd`: The BSON command to run.

        :Returns:
          The marked command response from mongocryptd.
        """
            if not self._spawned:
                if not self.opts._mongocryptd_bypass_spawn:
                    self.spawn()
            inflated_cmd = _inflate_bson(cmd, DEFAULT_RAW_BSON_OPTIONS)
            try:
                res = self.mongocryptd_client[database].command(inflated_cmd,
                  codec_options=DEFAULT_RAW_BSON_OPTIONS)
            except ServerSelectionTimeoutError:
                if self.opts._mongocryptd_bypass_spawn:
                    raise
                self.spawn()
                res = self.mongocryptd_client[database].command(inflated_cmd,
                  codec_options=DEFAULT_RAW_BSON_OPTIONS)
            else:
                return res.raw

        def fetch_keys(self, filter):
            """Yields one or more keys from the key vault.

        :Parameters:
          - `filter`: The filter to pass to find.

        :Returns:
          A generator which yields the requested keys from the key vault.
        """
            with self.key_vault_coll.find(RawBSONDocument(filter)) as (cursor):
                for key in cursor:
                    (yield key.raw)

        def insert_data_key(self, data_key):
            """Insert a data key into the key vault.

        :Parameters:
          - `data_key`: The data key document to insert.

        :Returns:
          The _id of the inserted data key document.
        """
            raw_doc = RawBSONDocument(data_key)
            data_key_id = raw_doc.get('_id')
            if not isinstance(data_key_id, uuid.UUID):
                raise TypeError('data_key _id must be a UUID')
            self.key_vault_coll.insert_one(raw_doc)
            return Binary((data_key_id.bytes), subtype=UUID_SUBTYPE)

        def bson_encode(self, doc):
            """Encode a document to BSON.

        A document can be any mapping type (like :class:`dict`).

        :Parameters:
          - `doc`: mapping type representing a document

        :Returns:
          The encoded BSON bytes.
        """
            return encode(doc)

        def close(self):
            """Release resources.

        Note it is not safe to call this method from __del__ or any GC hooks.
        """
            self.client_ref = None
            self.key_vault_coll = None
            if self.mongocryptd_client:
                self.mongocryptd_client.close()
                self.mongocryptd_client = None


    class _Encrypter(object):

        def __init__(self, io_callbacks, opts):
            """Encrypts and decrypts MongoDB commands.

        This class is used to support automatic encryption and decryption of
        MongoDB commands.

        :Parameters:
          - `io_callbacks`: A :class:`MongoCryptCallback`.
          - `opts`: The encrypted client's :class:`AutoEncryptionOpts`.
        """
            if opts._schema_map is None:
                schema_map = None
            else:
                schema_map = _dict_to_bson(opts._schema_map, False, _DATA_KEY_OPTS)
            self._auto_encrypter = AutoEncrypter(io_callbacks, MongoCryptOptions(opts._kms_providers, schema_map))
            self._bypass_auto_encryption = opts._bypass_auto_encryption
            self._closed = False

        def encrypt--- This code section failed: ---

 L. 267         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _check_closed
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 270         8  LOAD_FAST                'check_keys'
               10  JUMP_IF_FALSE_OR_POP    22  'to 22'
               12  LOAD_FAST                'cmd'
               14  LOAD_METHOD              pop
               16  LOAD_STR                 '$clusterTime'
               18  LOAD_CONST               None
               20  CALL_METHOD_2         2  ''
             22_0  COME_FROM            10  '10'
               22  STORE_FAST               'cluster_time'

 L. 271        24  LOAD_GLOBAL              _dict_to_bson
               26  LOAD_FAST                'cmd'
               28  LOAD_FAST                'check_keys'
               30  LOAD_FAST                'codec_options'
               32  CALL_FUNCTION_3       3  ''
               34  STORE_FAST               'encoded_cmd'

 L. 272        36  LOAD_GLOBAL              _wrap_encryption_errors
               38  CALL_FUNCTION_0       0  ''
               40  SETUP_WITH           96  'to 96'
               42  POP_TOP          

 L. 273        44  LOAD_FAST                'self'
               46  LOAD_ATTR                _auto_encrypter
               48  LOAD_METHOD              encrypt
               50  LOAD_FAST                'database'
               52  LOAD_FAST                'encoded_cmd'
               54  CALL_METHOD_2         2  ''
               56  STORE_FAST               'encrypted_cmd'

 L. 275        58  LOAD_GLOBAL              _inflate_bson

 L. 276        60  LOAD_FAST                'encrypted_cmd'

 L. 276        62  LOAD_GLOBAL              DEFAULT_RAW_BSON_OPTIONS

 L. 275        64  CALL_FUNCTION_2       2  ''
               66  STORE_FAST               'encrypt_cmd'

 L. 277        68  LOAD_FAST                'cluster_time'
               70  POP_JUMP_IF_FALSE    80  'to 80'

 L. 278        72  LOAD_FAST                'cluster_time'
               74  LOAD_FAST                'encrypt_cmd'
               76  LOAD_STR                 '$clusterTime'
               78  STORE_SUBSCR     
             80_0  COME_FROM            70  '70'

 L. 279        80  LOAD_FAST                'encrypt_cmd'
               82  POP_BLOCK        
               84  ROT_TWO          
               86  BEGIN_FINALLY    
               88  WITH_CLEANUP_START
               90  WITH_CLEANUP_FINISH
               92  POP_FINALLY           0  ''
               94  RETURN_VALUE     
             96_0  COME_FROM_WITH       40  '40'
               96  WITH_CLEANUP_START
               98  WITH_CLEANUP_FINISH
              100  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 84

        def decrypt--- This code section failed: ---

 L. 290         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _check_closed
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 291         8  LOAD_GLOBAL              _wrap_encryption_errors
               10  CALL_FUNCTION_0       0  ''
               12  SETUP_WITH           40  'to 40'
               14  POP_TOP          

 L. 292        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _auto_encrypter
               20  LOAD_METHOD              decrypt
               22  LOAD_FAST                'response'
               24  CALL_METHOD_1         1  ''
               26  POP_BLOCK        
               28  ROT_TWO          
               30  BEGIN_FINALLY    
               32  WITH_CLEANUP_START
               34  WITH_CLEANUP_FINISH
               36  POP_FINALLY           0  ''
               38  RETURN_VALUE     
             40_0  COME_FROM_WITH       12  '12'
               40  WITH_CLEANUP_START
               42  WITH_CLEANUP_FINISH
               44  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 28

        def _check_closed(self):
            if self._closed:
                raise InvalidOperation('Cannot use MongoClient after close')

        def close(self):
            """Cleanup resources."""
            self._closed = True
            self._auto_encrypter.close()

        @staticmethod
        def create(client, opts):
            """Create a _CommandEncyptor for a client.

        :Parameters:
          - `client`: The encrypted MongoClient.
          - `opts`: The encrypted client's :class:`AutoEncryptionOpts`.

        :Returns:
          A :class:`_CommandEncrypter` for this client.
        """
            key_vault_client = opts._key_vault_client or client
            db, coll = opts._key_vault_namespace.split'.'1
            key_vault_coll = key_vault_client[db][coll]
            mongocryptd_client = MongoClient((opts._mongocryptd_uri),
              connect=False, serverSelectionTimeoutMS=_MONGOCRYPTD_TIMEOUT_MS)
            io_callbacks = _EncryptionIO(client, key_vault_coll, mongocryptd_client, opts)
            return _Encrypter(io_callbacks, opts)


    class Algorithm(object):
        __doc__ = 'An enum that defines the supported encryption algorithms.'
        AEAD_AES_256_CBC_HMAC_SHA_512_Deterministic = 'AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic'
        AEAD_AES_256_CBC_HMAC_SHA_512_Random = 'AEAD_AES_256_CBC_HMAC_SHA_512-Random'


    class ClientEncryption(object):
        __doc__ = 'Explicit client-side field level encryption.'

        def __init__(self, kms_providers, key_vault_namespace, key_vault_client, codec_options):
            """Explicit client-side field level encryption.

        The ClientEncryption class encapsulates explicit operations on a key
        vault collection that cannot be done directly on a MongoClient. Similar
        to configuring auto encryption on a MongoClient, it is constructed with
        a MongoClient (to a MongoDB cluster containing the key vault
        collection), KMS provider configuration, and keyVaultNamespace. It
        provides an API for explicitly encrypting and decrypting values, and
        creating data keys. It does not provide an API to query keys from the
        key vault collection, as this can be done directly on the MongoClient.

        See :ref:`explicit-client-side-encryption` for an example.

        :Parameters:
          - `kms_providers`: Map of KMS provider options. Two KMS providers
            are supported: "aws" and "local". The kmsProviders map values
            differ by provider:

              - `aws`: Map with "accessKeyId" and "secretAccessKey" as strings.
                These are the AWS access key ID and AWS secret access key used
                to generate KMS messages.
              - `local`: Map with "key" as a 96-byte array or string. "key"
                is the master key used to encrypt/decrypt data keys. This key
                should be generated and stored as securely as possible.

          - `key_vault_namespace`: The namespace for the key vault collection.
            The key vault collection contains all data keys used for encryption
            and decryption. Data keys are stored as documents in this MongoDB
            collection. Data keys are protected with encryption by a KMS
            provider.
          - `key_vault_client`: A MongoClient connected to a MongoDB cluster
            containing the `key_vault_namespace` collection.
          - `codec_options`: An instance of
            :class:`~bson.codec_options.CodecOptions` to use when encoding a
            value for encryption and decoding the decrypted BSON value. This
            should be the same CodecOptions instance configured on the
            MongoClient, Database, or Collection used to access application
            data.

        .. versionadded:: 3.9
        """
            if not _HAVE_PYMONGOCRYPT:
                raise ConfigurationError("client-side field level encryption requires the pymongocrypt library: install a compatible version with: python -m pip install 'pymongo[encryption]'")
            if not isinstance(codec_options, CodecOptions):
                raise TypeError('codec_options must be an instance of bson.codec_options.CodecOptions')
            self._kms_providers = kms_providers
            self._key_vault_namespace = key_vault_namespace
            self._key_vault_client = key_vault_client
            self._codec_options = codec_options
            db, coll = key_vault_namespace.split'.'1
            key_vault_coll = key_vault_client[db][coll]
            self._io_callbacks = _EncryptionIO(None, key_vault_coll, None, None)
            self._encryption = ExplicitEncrypter(self._io_callbacks, MongoCryptOptions(kms_providers, None))

        def create_data_key--- This code section failed: ---

 L. 438         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _check_closed
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 439         8  LOAD_GLOBAL              _wrap_encryption_errors
               10  CALL_FUNCTION_0       0  ''
               12  SETUP_WITH           46  'to 46'
               14  POP_TOP          

 L. 440        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _encryption
               20  LOAD_ATTR                create_data_key

 L. 441        22  LOAD_FAST                'kms_provider'

 L. 441        24  LOAD_FAST                'master_key'

 L. 442        26  LOAD_FAST                'key_alt_names'

 L. 440        28  LOAD_CONST               ('master_key', 'key_alt_names')
               30  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               32  POP_BLOCK        
               34  ROT_TWO          
               36  BEGIN_FINALLY    
               38  WITH_CLEANUP_START
               40  WITH_CLEANUP_FINISH
               42  POP_FINALLY           0  ''
               44  RETURN_VALUE     
             46_0  COME_FROM_WITH       12  '12'
               46  WITH_CLEANUP_START
               48  WITH_CLEANUP_FINISH
               50  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 34

        def encrypt--- This code section failed: ---

 L. 462         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _check_closed
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 463         8  LOAD_FAST                'key_id'
               10  LOAD_CONST               None
               12  COMPARE_OP               is-not
               14  POP_JUMP_IF_FALSE    44  'to 44'

 L. 464        16  LOAD_GLOBAL              isinstance
               18  LOAD_FAST                'key_id'
               20  LOAD_GLOBAL              Binary
               22  CALL_FUNCTION_2       2  ''

 L. 463        24  POP_JUMP_IF_FALSE    36  'to 36'

 L. 465        26  LOAD_FAST                'key_id'
               28  LOAD_ATTR                subtype
               30  LOAD_GLOBAL              UUID_SUBTYPE
               32  COMPARE_OP               ==

 L. 463        34  POP_JUMP_IF_TRUE     44  'to 44'
             36_0  COME_FROM            24  '24'

 L. 466        36  LOAD_GLOBAL              TypeError

 L. 467        38  LOAD_STR                 'key_id must be a bson.binary.Binary with subtype 4'

 L. 466        40  CALL_FUNCTION_1       1  ''
               42  RAISE_VARARGS_1       1  'exception instance'
             44_0  COME_FROM            34  '34'
             44_1  COME_FROM            14  '14'

 L. 469        44  LOAD_GLOBAL              encode
               46  LOAD_STR                 'v'
               48  LOAD_FAST                'value'
               50  BUILD_MAP_1           1 
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                _codec_options
               56  LOAD_CONST               ('codec_options',)
               58  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               60  STORE_FAST               'doc'

 L. 470        62  LOAD_GLOBAL              _wrap_encryption_errors
               64  CALL_FUNCTION_0       0  ''
               66  SETUP_WITH          114  'to 114'
               68  POP_TOP          

 L. 471        70  LOAD_FAST                'self'
               72  LOAD_ATTR                _encryption
               74  LOAD_ATTR                encrypt

 L. 472        76  LOAD_FAST                'doc'

 L. 472        78  LOAD_FAST                'algorithm'

 L. 472        80  LOAD_FAST                'key_id'

 L. 472        82  LOAD_FAST                'key_alt_name'

 L. 471        84  LOAD_CONST               ('key_id', 'key_alt_name')
               86  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               88  STORE_FAST               'encrypted_doc'

 L. 473        90  LOAD_GLOBAL              decode
               92  LOAD_FAST                'encrypted_doc'
               94  CALL_FUNCTION_1       1  ''
               96  LOAD_STR                 'v'
               98  BINARY_SUBSCR    
              100  POP_BLOCK        
              102  ROT_TWO          
              104  BEGIN_FINALLY    
              106  WITH_CLEANUP_START
              108  WITH_CLEANUP_FINISH
              110  POP_FINALLY           0  ''
              112  RETURN_VALUE     
            114_0  COME_FROM_WITH       66  '66'
              114  WITH_CLEANUP_START
              116  WITH_CLEANUP_FINISH
              118  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 102

        def decrypt--- This code section failed: ---

 L. 485         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _check_closed
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 486         8  LOAD_GLOBAL              isinstance
               10  LOAD_FAST                'value'
               12  LOAD_GLOBAL              Binary
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_FALSE    28  'to 28'
               18  LOAD_FAST                'value'
               20  LOAD_ATTR                subtype
               22  LOAD_CONST               6
               24  COMPARE_OP               ==
               26  POP_JUMP_IF_TRUE     36  'to 36'
             28_0  COME_FROM            16  '16'

 L. 487        28  LOAD_GLOBAL              TypeError

 L. 488        30  LOAD_STR                 'value to decrypt must be a bson.binary.Binary with subtype 6'

 L. 487        32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            26  '26'

 L. 490        36  LOAD_GLOBAL              _wrap_encryption_errors
               38  CALL_FUNCTION_0       0  ''
               40  SETUP_WITH           98  'to 98'
               42  POP_TOP          

 L. 491        44  LOAD_GLOBAL              encode
               46  LOAD_STR                 'v'
               48  LOAD_FAST                'value'
               50  BUILD_MAP_1           1 
               52  CALL_FUNCTION_1       1  ''
               54  STORE_FAST               'doc'

 L. 492        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _encryption
               60  LOAD_METHOD              decrypt
               62  LOAD_FAST                'doc'
               64  CALL_METHOD_1         1  ''
               66  STORE_FAST               'decrypted_doc'

 L. 493        68  LOAD_GLOBAL              decode
               70  LOAD_FAST                'decrypted_doc'

 L. 494        72  LOAD_FAST                'self'
               74  LOAD_ATTR                _codec_options

 L. 493        76  LOAD_CONST               ('codec_options',)
               78  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 494        80  LOAD_STR                 'v'

 L. 493        82  BINARY_SUBSCR    
               84  POP_BLOCK        
               86  ROT_TWO          
               88  BEGIN_FINALLY    
               90  WITH_CLEANUP_START
               92  WITH_CLEANUP_FINISH
               94  POP_FINALLY           0  ''
               96  RETURN_VALUE     
             98_0  COME_FROM_WITH       40  '40'
               98  WITH_CLEANUP_START
              100  WITH_CLEANUP_FINISH
              102  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 86

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.close()

        def _check_closed(self):
            if self._encryption is None:
                raise InvalidOperation('Cannot use closed ClientEncryption')

        def close(self):
            """Release resources.

        Note that using this class in a with-statement will automatically call
        :meth:`close`::

            with ClientEncryption(...) as client_encryption:
                encrypted = client_encryption.encrypt(value, ...)
                decrypted = client_encryption.decrypt(encrypted)

        """
            if self._io_callbacks:
                self._io_callbacks.close()
                self._encryption.close()
                self._io_callbacks = None
                self._encryption = None