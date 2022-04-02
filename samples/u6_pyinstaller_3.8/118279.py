# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pymongo\mongo_client.py
"""Tools for connecting to MongoDB.

.. seealso:: :doc:`/examples/high_availability` for examples of connecting
   to replica sets or sets of mongos servers.

To get a :class:`~pymongo.database.Database` instance from a
:class:`MongoClient` use either dictionary-style or attribute-style
access:

.. doctest::

  >>> from pymongo import MongoClient
  >>> c = MongoClient()
  >>> c.test_database
  Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True), u'test_database')
  >>> c['test-database']
  Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True), u'test-database')
"""
import contextlib, datetime, threading, warnings, weakref
from collections import defaultdict
from bson.codec_options import DEFAULT_CODEC_OPTIONS
from bson.py3compat import integer_types, string_type
from bson.son import SON
from pymongo import common, database, helpers, message, periodic_executor, uri_parser, client_session
from pymongo.change_stream import ClusterChangeStream
from pymongo.client_options import ClientOptions
from pymongo.command_cursor import CommandCursor
from pymongo.cursor_manager import CursorManager
from pymongo.errors import AutoReconnect, BulkWriteError, ConfigurationError, ConnectionFailure, InvalidOperation, NetworkTimeout, NotMasterError, OperationFailure, PyMongoError, ServerSelectionTimeoutError
from pymongo.read_preferences import ReadPreference
from pymongo.server_selectors import writable_preferred_server_selector, writable_server_selector
from pymongo.server_type import SERVER_TYPE
from pymongo.topology import Topology
from pymongo.topology_description import TOPOLOGY_TYPE
from pymongo.settings import TopologySettings
from pymongo.uri_parser import _handle_option_deprecations, _handle_security_options, _normalize_options
from pymongo.write_concern import DEFAULT_WRITE_CONCERN

class MongoClient(common.BaseObject):
    __doc__ = '\n    A client-side representation of a MongoDB cluster.\n\n    Instances can represent either a standalone MongoDB server, a replica\n    set, or a sharded cluster. Instances of this class are responsible for\n    maintaining up-to-date state of the cluster, and possibly cache\n    resources related to this, including background threads for monitoring,\n    and connection pools.\n    '
    HOST = 'localhost'
    PORT = 27017
    _constructor_args = ('document_class', 'tz_aware', 'connect')

    def __init__(self, host=None, port=None, document_class=dict, tz_aware=None, connect=None, type_registry=None, **kwargs):
        """Client for a MongoDB instance, a replica set, or a set of mongoses.

        The client object is thread-safe and has connection-pooling built in.
        If an operation fails because of a network error,
        :class:`~pymongo.errors.ConnectionFailure` is raised and the client
        reconnects in the background. Application code should handle this
        exception (recognizing that the operation failed) and then continue to
        execute.

        The `host` parameter can be a full `mongodb URI
        <http://dochub.mongodb.org/core/connections>`_, in addition to
        a simple hostname. It can also be a list of hostnames or
        URIs. Any port specified in the host string(s) will override
        the `port` parameter. If multiple mongodb URIs containing
        database or auth information are passed, the last database,
        username, and password present will be used.  For username and
        passwords reserved characters like ':', '/', '+' and '@' must be
        percent encoded following RFC 2396::

            try:
                # Python 3.x
                from urllib.parse import quote_plus
            except ImportError:
                # Python 2.x
                from urllib import quote_plus

            uri = "mongodb://%s:%s@%s" % (
                quote_plus(user), quote_plus(password), host)
            client = MongoClient(uri)

        Unix domain sockets are also supported. The socket path must be percent
        encoded in the URI::

            uri = "mongodb://%s:%s@%s" % (
                quote_plus(user), quote_plus(password), quote_plus(socket_path))
            client = MongoClient(uri)

        But not when passed as a simple hostname::

            client = MongoClient('/tmp/mongodb-27017.sock')

        Starting with version 3.6, PyMongo supports mongodb+srv:// URIs. The
        URI must include one, and only one, hostname. The hostname will be
        resolved to one or more DNS `SRV records
        <https://en.wikipedia.org/wiki/SRV_record>`_ which will be used
        as the seed list for connecting to the MongoDB deployment. When using
        SRV URIs, the `authSource` and `replicaSet` configuration options can
        be specified using `TXT records
        <https://en.wikipedia.org/wiki/TXT_record>`_. See the
        `Initial DNS Seedlist Discovery spec
        <https://github.com/mongodb/specifications/blob/master/source/
        initial-dns-seedlist-discovery/initial-dns-seedlist-discovery.rst>`_
        for more details. Note that the use of SRV URIs implicitly enables
        TLS support. Pass tls=false in the URI to override.

        .. note:: MongoClient creation will block waiting for answers from
          DNS when mongodb+srv:// URIs are used.

        .. note:: Starting with version 3.0 the :class:`MongoClient`
          constructor no longer blocks while connecting to the server or
          servers, and it no longer raises
          :class:`~pymongo.errors.ConnectionFailure` if they are
          unavailable, nor :class:`~pymongo.errors.ConfigurationError`
          if the user's credentials are wrong. Instead, the constructor
          returns immediately and launches the connection process on
          background threads. You can check if the server is available
          like this::

            from pymongo.errors import ConnectionFailure
            client = MongoClient()
            try:
                # The ismaster command is cheap and does not require auth.
                client.admin.command('ismaster')
            except ConnectionFailure:
                print("Server not available")

        .. warning:: When using PyMongo in a multiprocessing context, please
          read :ref:`multiprocessing` first.

        .. note:: Many of the following options can be passed using a MongoDB
          URI or keyword parameters. If the same option is passed in a URI and
          as a keyword parameter the keyword parameter takes precedence.

        :Parameters:
          - `host` (optional): hostname or IP address or Unix domain socket
            path of a single mongod or mongos instance to connect to, or a
            mongodb URI, or a list of hostnames / mongodb URIs. If `host` is
            an IPv6 literal it must be enclosed in '[' and ']' characters
            following the RFC2732 URL syntax (e.g. '[::1]' for localhost).
            Multihomed and round robin DNS addresses are **not** supported.
          - `port` (optional): port number on which to connect
          - `document_class` (optional): default class to use for
            documents returned from queries on this client
          - `type_registry` (optional): instance of
            :class:`~bson.codec_options.TypeRegistry` to enable encoding
            and decoding of custom types.
          - `tz_aware` (optional): if ``True``,
            :class:`~datetime.datetime` instances returned as values
            in a document by this :class:`MongoClient` will be timezone
            aware (otherwise they will be naive)
          - `connect` (optional): if ``True`` (the default), immediately
            begin connecting to MongoDB in the background. Otherwise connect
            on the first operation.

          | **Other optional parameters can be passed as keyword arguments:**

          - `maxPoolSize` (optional): The maximum allowable number of
            concurrent connections to each connected server. Requests to a
            server will block if there are `maxPoolSize` outstanding
            connections to the requested server. Defaults to 100. Cannot be 0.
          - `minPoolSize` (optional): The minimum required number of concurrent
            connections that the pool will maintain to each connected server.
            Default is 0.
          - `maxIdleTimeMS` (optional): The maximum number of milliseconds that
            a connection can remain idle in the pool before being removed and
            replaced. Defaults to `None` (no limit).
          - `socketTimeoutMS`: (integer or None) Controls how long (in
            milliseconds) the driver will wait for a response after sending an
            ordinary (non-monitoring) database operation before concluding that
            a network error has occurred. Defaults to ``None`` (no timeout).
          - `connectTimeoutMS`: (integer or None) Controls how long (in
            milliseconds) the driver will wait during server monitoring when
            connecting a new socket to a server before concluding the server
            is unavailable. Defaults to ``20000`` (20 seconds).
          - `server_selector`: (callable or None) Optional, user-provided
            function that augments server selection rules. The function should
            accept as an argument a list of
            :class:`~pymongo.server_description.ServerDescription` objects and
            return a list of server descriptions that should be considered
            suitable for the desired operation.
          - `serverSelectionTimeoutMS`: (integer) Controls how long (in
            milliseconds) the driver will wait to find an available,
            appropriate server to carry out a database operation; while it is
            waiting, multiple server monitoring operations may be carried out,
            each controlled by `connectTimeoutMS`. Defaults to ``30000`` (30
            seconds).
          - `waitQueueTimeoutMS`: (integer or None) How long (in milliseconds)
            a thread will wait for a socket from the pool if the pool has no
            free sockets. Defaults to ``None`` (no timeout).
          - `waitQueueMultiple`: (integer or None) Multiplied by maxPoolSize
            to give the number of threads allowed to wait for a socket at one
            time. Defaults to ``None`` (no limit).
          - `heartbeatFrequencyMS`: (optional) The number of milliseconds
            between periodic server checks, or None to accept the default
            frequency of 10 seconds.
          - `appname`: (string or None) The name of the application that
            created this MongoClient instance. MongoDB 3.4 and newer will
            print this value in the server log upon establishing each
            connection. It is also recorded in the slow query log and
            profile collections.
          - `driver`: (pair or None) A driver implemented on top of PyMongo can
            pass a :class:`~pymongo.driver_info.DriverInfo` to add its name,
            version, and platform to the message printed in the server log when
            establishing a connection.
          - `event_listeners`: a list or tuple of event listeners. See
            :mod:`~pymongo.monitoring` for details.
          - `retryWrites`: (boolean) Whether supported write operations
            executed within this MongoClient will be retried once after a
            network error on MongoDB 3.6+. Defaults to ``True``.
            The supported write operations are:

              - :meth:`~pymongo.collection.Collection.bulk_write`, as long as
                :class:`~pymongo.operations.UpdateMany` or
                :class:`~pymongo.operations.DeleteMany` are not included.
              - :meth:`~pymongo.collection.Collection.delete_one`
              - :meth:`~pymongo.collection.Collection.insert_one`
              - :meth:`~pymongo.collection.Collection.insert_many`
              - :meth:`~pymongo.collection.Collection.replace_one`
              - :meth:`~pymongo.collection.Collection.update_one`
              - :meth:`~pymongo.collection.Collection.find_one_and_delete`
              - :meth:`~pymongo.collection.Collection.find_one_and_replace`
              - :meth:`~pymongo.collection.Collection.find_one_and_update`

            Unsupported write operations include, but are not limited to,
            :meth:`~pymongo.collection.Collection.aggregate` using the ``$out``
            pipeline operator and any operation with an unacknowledged write
            concern (e.g. {w: 0})). See
            https://github.com/mongodb/specifications/blob/master/source/retryable-writes/retryable-writes.rst
          - `retryReads`: (boolean) Whether supported read operations
            executed within this MongoClient will be retried once after a
            network error on MongoDB 3.6+. Defaults to ``True``.
            The supported read operations are:
            :meth:`~pymongo.collection.Collection.find`,
            :meth:`~pymongo.collection.Collection.find_one`,
            :meth:`~pymongo.collection.Collection.aggregate` without ``$out``,
            :meth:`~pymongo.collection.Collection.distinct`,
            :meth:`~pymongo.collection.Collection.count`,
            :meth:`~pymongo.collection.Collection.estimated_document_count`,
            :meth:`~pymongo.collection.Collection.count_documents`,
            :meth:`pymongo.collection.Collection.watch`,
            :meth:`~pymongo.collection.Collection.list_indexes`,
            :meth:`pymongo.database.Database.watch`,
            :meth:`~pymongo.database.Database.list_collections`,
            :meth:`pymongo.mongo_client.MongoClient.watch`,
            and :meth:`~pymongo.mongo_client.MongoClient.list_databases`.

            Unsupported read operations include, but are not limited to:
            :meth:`~pymongo.collection.Collection.map_reduce`,
            :meth:`~pymongo.collection.Collection.inline_map_reduce`,
            :meth:`~pymongo.database.Database.command`,
            and any getMore operation on a cursor.

            Enabling retryable reads makes applications more resilient to
            transient errors such as network failures, database upgrades, and
            replica set failovers. For an exact definition of which errors
            trigger a retry, see the `retryable reads specification
            <https://github.com/mongodb/specifications/blob/master/source/retryable-reads/retryable-reads.rst>`_.

          - `socketKeepAlive`: (boolean) **DEPRECATED** Whether to send
            periodic keep-alive packets on connected sockets. Defaults to
            ``True``. Disabling it is not recommended, see
            https://docs.mongodb.com/manual/faq/diagnostics/#does-tcp-keepalive-time-affect-mongodb-deployments",
          - `compressors`: Comma separated list of compressors for wire
            protocol compression. The list is used to negotiate a compressor
            with the server. Currently supported options are "snappy", "zlib"
            and "zstd". Support for snappy requires the
            `python-snappy <https://pypi.org/project/python-snappy/>`_ package.
            zlib support requires the Python standard library zlib module. zstd
            requires the `zstandard <https://pypi.org/project/zstandard/>`_
            package. By default no compression is used. Compression support
            must also be enabled on the server. MongoDB 3.4+ supports snappy
            compression. MongoDB 3.6 adds support for zlib. MongoDB 4.2 adds
            support for zstd.
          - `zlibCompressionLevel`: (int) The zlib compression level to use
            when zlib is used as the wire protocol compressor. Supported values
            are -1 through 9. -1 tells the zlib library to use its default
            compression level (usually 6). 0 means no compression. 1 is best
            speed. 9 is best compression. Defaults to -1.
          - `uuidRepresentation`: The BSON representation to use when encoding
            from and decoding to instances of :class:`~uuid.UUID`. Valid
            values are `pythonLegacy` (the default), `javaLegacy`,
            `csharpLegacy` and `standard`. New applications should consider
            setting this to `standard` for cross language compatibility.

          | **Write Concern options:**
          | (Only set if passed. No default values.)

          - `w`: (integer or string) If this is a replica set, write operations
            will block until they have been replicated to the specified number
            or tagged set of servers. `w=<int>` always includes the replica set
            primary (e.g. w=3 means write to the primary and wait until
            replicated to **two** secondaries). Passing w=0 **disables write
            acknowledgement** and all other write concern options.
          - `wTimeoutMS`: (integer) Used in conjunction with `w`. Specify a value
            in milliseconds to control how long to wait for write propagation
            to complete. If replication does not complete in the given
            timeframe, a timeout exception is raised. Passing wTimeoutMS=0
            will cause **write operations to wait indefinitely**.
          - `journal`: If ``True`` block until write operations have been
            committed to the journal. Cannot be used in combination with
            `fsync`. Prior to MongoDB 2.6 this option was ignored if the server
            was running without journaling. Starting with MongoDB 2.6 write
            operations will fail with an exception if this option is used when
            the server is running without journaling.
          - `fsync`: If ``True`` and the server is running without journaling,
            blocks until the server has synced all data files to disk. If the
            server is running with journaling, this acts the same as the `j`
            option, blocking until write operations have been committed to the
            journal. Cannot be used in combination with `j`.

          | **Replica set keyword arguments for connecting with a replica set
            - either directly or via a mongos:**

          - `replicaSet`: (string or None) The name of the replica set to
            connect to. The driver will verify that all servers it connects to
            match this name. Implies that the hosts specified are a seed list
            and the driver should attempt to find all members of the set.
            Defaults to ``None``.

          | **Read Preference:**

          - `readPreference`: The replica set read preference for this client.
            One of ``primary``, ``primaryPreferred``, ``secondary``,
            ``secondaryPreferred``, or ``nearest``. Defaults to ``primary``.
          - `readPreferenceTags`: Specifies a tag set as a comma-separated list
            of colon-separated key-value pairs. For example ``dc:ny,rack:1``.
            Defaults to ``None``.
          - `maxStalenessSeconds`: (integer) The maximum estimated
            length of time a replica set secondary can fall behind the primary
            in replication before it will no longer be selected for operations.
            Defaults to ``-1``, meaning no maximum. If maxStalenessSeconds
            is set, it must be a positive integer greater than or equal to
            90 seconds.

          .. seealso:: :doc:`/examples/server_selection`

          | **Authentication:**

          - `username`: A string.
          - `password`: A string.

            Although username and password must be percent-escaped in a MongoDB
            URI, they must not be percent-escaped when passed as parameters. In
            this example, both the space and slash special characters are passed
            as-is::

              MongoClient(username="user name", password="pass/word")

          - `authSource`: The database to authenticate on. Defaults to the
            database specified in the URI, if provided, or to "admin".
          - `authMechanism`: See :data:`~pymongo.auth.MECHANISMS` for options.
            If no mechanism is specified, PyMongo automatically uses MONGODB-CR
            when connected to a pre-3.0 version of MongoDB, SCRAM-SHA-1 when
            connected to MongoDB 3.0 through 3.6, and negotiates the mechanism
            to use (SCRAM-SHA-1 or SCRAM-SHA-256) when connected to MongoDB
            4.0+.
          - `authMechanismProperties`: Used to specify authentication mechanism
            specific options. To specify the service name for GSSAPI
            authentication pass authMechanismProperties='SERVICE_NAME:<service
            name>'

          .. seealso:: :doc:`/examples/authentication`

          | **TLS/SSL configuration:**

          - `tls`: (boolean) If ``True``, create the connection to the server
            using transport layer security. Defaults to ``False``.
          - `tlsInsecure`: (boolean) Specify whether TLS constraints should be
            relaxed as much as possible. Setting ``tlsInsecure=True`` implies
            ``tlsAllowInvalidCertificates=True`` and
            ``tlsAllowInvalidHostnames=True``. Defaults to ``False``. Think
            very carefully before setting this to ``True`` as it dramatically
            reduces the security of TLS.
          - `tlsAllowInvalidCertificates`: (boolean) If ``True``, continues
            the TLS handshake regardless of the outcome of the certificate
            verification process. If this is ``False``, and a value is not
            provided for ``tlsCAFile``, PyMongo will attempt to load system
            provided CA certificates. If the python version in use does not
            support loading system CA certificates then the ``tlsCAFile``
            parameter must point to a file of CA certificates.
            ``tlsAllowInvalidCertificates=False`` implies ``tls=True``.
            Defaults to ``False``. Think very carefully before setting this
            to ``True`` as that could make your application vulnerable to
            man-in-the-middle attacks.
          - `tlsAllowInvalidHostnames`: (boolean) If ``True``, disables TLS
            hostname verification. ``tlsAllowInvalidHostnames=False`` implies
            ``tls=True``. Defaults to ``False``. Think very carefully before
            setting this to ``True`` as that could make your application
            vulnerable to man-in-the-middle attacks.
          - `tlsCAFile`: A file containing a single or a bundle of
            "certification authority" certificates, which are used to validate
            certificates passed from the other end of the connection.
            Implies ``tls=True``. Defaults to ``None``.
          - `tlsCertificateKeyFile`: A file containing the client certificate
            and private key. If you want to pass the certificate and private
            key as separate files, use the ``ssl_certfile`` and ``ssl_keyfile``
            options instead. Implies ``tls=True``. Defaults to ``None``.
          - `tlsCRLFile`: A file containing a PEM or DER formatted
            certificate revocation list. Only supported by python 2.7.9+
            (pypy 2.5.1+). Implies ``tls=True``. Defaults to ``None``.
          - `tlsCertificateKeyFilePassword`: The password or passphrase for
            decrypting the private key in ``tlsCertificateKeyFile`` or
            ``ssl_keyfile``. Only necessary if the private key is encrypted.
            Only supported by python 2.7.9+ (pypy 2.5.1+) and 3.3+. Defaults
            to ``None``.
          - `ssl`: (boolean) Alias for ``tls``.
          - `ssl_certfile`: The certificate file used to identify the local
            connection against mongod. Implies ``tls=True``. Defaults to
            ``None``.
          - `ssl_keyfile`: The private keyfile used to identify the local
            connection against mongod. Can be omitted if the keyfile is
            included with the ``tlsCertificateKeyFile``. Implies ``tls=True``.
            Defaults to ``None``.

          | **Read Concern options:**
          | (If not set explicitly, this will use the server default)

          - `readConcernLevel`: (string) The read concern level specifies the
            level of isolation for read operations.  For example, a read
            operation using a read concern level of ``majority`` will only
            return data that has been written to a majority of nodes. If the
            level is left unspecified, the server default will be used.

          | **Client side encryption options:**
          | (If not set explicitly, client side encryption will not be enabled.)

          - `auto_encryption_opts`: A
            :class:`~pymongo.encryption_options.AutoEncryptionOpts` which
            configures this client to automatically encrypt collection commands
            and automatically decrypt results. See
            :ref:`automatic-client-side-encryption` for an example.

        .. mongodoc:: connections

        .. versionchanged:: 3.9
           Added the ``retryReads`` keyword argument and URI option.
           Added the ``tlsInsecure`` keyword argument and URI option.
           The following keyword arguments and URI options were deprecated:

             - ``wTimeout`` was deprecated in favor of ``wTimeoutMS``.
             - ``j`` was deprecated in favor of ``journal``.
             - ``ssl_cert_reqs`` was deprecated in favor of
               ``tlsAllowInvalidCertificates``.
             - ``ssl_match_hostname`` was deprecated in favor of
               ``tlsAllowInvalidHostnames``.
             - ``ssl_ca_certs`` was deprecated in favor of ``tlsCAFile``.
             - ``ssl_certfile`` was deprecated in favor of
               ``tlsCertificateKeyFile``.
             - ``ssl_crlfile`` was deprecated in favor of ``tlsCRLFile``.
             - ``ssl_pem_passphrase`` was deprecated in favor of
               ``tlsCertificateKeyFilePassword``.

        .. versionchanged:: 3.9
           ``retryWrites`` now defaults to ``True``.

        .. versionchanged:: 3.8
           Added the ``server_selector`` keyword argument.
           Added the ``type_registry`` keyword argument.

        .. versionchanged:: 3.7
           Added the ``driver`` keyword argument.

        .. versionchanged:: 3.6
           Added support for mongodb+srv:// URIs.
           Added the ``retryWrites`` keyword argument and URI option.

        .. versionchanged:: 3.5
           Add ``username`` and ``password`` options. Document the
           ``authSource``, ``authMechanism``, and ``authMechanismProperties ``
           options.
           Deprecated the ``socketKeepAlive`` keyword argument and URI option.
           ``socketKeepAlive`` now defaults to ``True``.

        .. versionchanged:: 3.0
           :class:`~pymongo.mongo_client.MongoClient` is now the one and only
           client class for a standalone server, mongos, or replica set.
           It includes the functionality that had been split into
           :class:`~pymongo.mongo_client.MongoReplicaSetClient`: it can connect
           to a replica set, discover all its members, and monitor the set for
           stepdowns, elections, and reconfigs.

           The :class:`~pymongo.mongo_client.MongoClient` constructor no
           longer blocks while connecting to the server or servers, and it no
           longer raises :class:`~pymongo.errors.ConnectionFailure` if they
           are unavailable, nor :class:`~pymongo.errors.ConfigurationError`
           if the user's credentials are wrong. Instead, the constructor
           returns immediately and launches the connection process on
           background threads.

           Therefore the ``alive`` method is removed since it no longer
           provides meaningful information; even if the client is disconnected,
           it may discover a server in time to fulfill the next operation.

           In PyMongo 2.x, :class:`~pymongo.MongoClient` accepted a list of
           standalone MongoDB servers and used the first it could connect to::

               MongoClient(['host1.com:27017', 'host2.com:27017'])

           A list of multiple standalones is no longer supported; if multiple
           servers are listed they must be members of the same replica set, or
           mongoses in the same sharded cluster.

           The behavior for a list of mongoses is changed from "high
           availability" to "load balancing". Before, the client connected to
           the lowest-latency mongos in the list, and used it until a network
           error prompted it to re-evaluate all mongoses' latencies and
           reconnect to one of them. In PyMongo 3, the client monitors its
           network latency to all the mongoses continuously, and distributes
           operations evenly among those with the lowest latency. See
           :ref:`mongos-load-balancing` for more information.

           The ``connect`` option is added.

           The ``start_request``, ``in_request``, and ``end_request`` methods
           are removed, as well as the ``auto_start_request`` option.

           The ``copy_database`` method is removed, see the
           :doc:`copy_database examples </examples/copydb>` for alternatives.

           The :meth:`MongoClient.disconnect` method is removed; it was a
           synonym for :meth:`~pymongo.MongoClient.close`.

           :class:`~pymongo.mongo_client.MongoClient` no longer returns an
           instance of :class:`~pymongo.database.Database` for attribute names
           with leading underscores. You must use dict-style lookups instead::

               client['__my_database__']

           Not::

               client.__my_database__
        """
        if host is None:
            host = self.HOST
        else:
            if isinstance(host, string_type):
                host = [
                 host]
            if port is None:
                port = self.PORT
            assert isinstance(port, int), 'port must be an instance of int'
        pool_class = kwargs.pop('_pool_class', None)
        monitor_class = kwargs.pop('_monitor_class', None)
        condition_class = kwargs.pop('_condition_class', None)
        keyword_opts = common._CaseInsensitiveDictionary(kwargs)
        keyword_opts['document_class'] = document_class
        seeds = set()
        username = None
        password = None
        dbase = None
        opts = {}
        fqdn = None
        for entity in host:
            if '://' in entity:
                timeout = keyword_opts.get('connecttimeoutms')
                if timeout is not None:
                    timeout = common.validate_timeout_or_none(keyword_opts.cased_key('connecttimeoutms'), timeout)
                res = uri_parser.parse_uri(entity,
                  port, validate=True, warn=True, normalize=False, connect_timeout=timeout)
                seeds.update(res['nodelist'])
                username = res['username'] or username
                password = res['password'] or password
                dbase = res['database'] or dbase
                opts = res['options']
                fqdn = res['fqdn']
            else:
                seeds.update(uri_parser.split_hosts(entity, port))
        else:
            if not seeds:
                raise ConfigurationError('need to specify at least one host')
            if type_registry is not None:
                keyword_opts['type_registry'] = type_registry
            if tz_aware is None:
                tz_aware = opts.get('tz_aware', False)
            if connect is None:
                connect = opts.get('connect', True)
            keyword_opts['tz_aware'] = tz_aware
            keyword_opts['connect'] = connect
            keyword_opts = _handle_option_deprecations(keyword_opts)
            keyword_opts = common._CaseInsensitiveDictionary(dict((common.validate(k, v) for k, v in keyword_opts.items())))
            opts.update(keyword_opts)
            opts = _handle_security_options(opts)
            opts = _normalize_options(opts)
            username = opts.get('username', username)
            password = opts.get('password', password)
            if 'socketkeepalive' in opts:
                warnings.warn('The socketKeepAlive option is deprecated. It nowdefaults to true and disabling it is not recommended, see https://docs.mongodb.com/manual/faq/diagnostics/#does-tcp-keepalive-time-affect-mongodb-deployments',
                  DeprecationWarning,
                  stacklevel=2)
            self._MongoClient__options = options = ClientOptions(username, password, dbase, opts)
            self._MongoClient__default_database_name = dbase
            self._MongoClient__lock = threading.Lock()
            self._MongoClient__cursor_manager = None
            self._MongoClient__kill_cursors_queue = []
            self._event_listeners = options.pool_options.event_listeners
            self._MongoClient__index_cache = {}
            self._MongoClient__index_cache_lock = threading.Lock()
            super(MongoClient, self).__init__(options.codec_options, options.read_preference, options.write_concern, options.read_concern)
            self._MongoClient__all_credentials = {}
            creds = options.credentials
            if creds:
                self._cache_credentials(creds.source, creds)
            self._topology_settings = TopologySettings(seeds=seeds,
              replica_set_name=(options.replica_set_name),
              pool_class=pool_class,
              pool_options=(options.pool_options),
              monitor_class=monitor_class,
              condition_class=condition_class,
              local_threshold_ms=(options.local_threshold_ms),
              server_selection_timeout=(options.server_selection_timeout),
              server_selector=(options.server_selector),
              heartbeat_frequency=(options.heartbeat_frequency),
              fqdn=fqdn)
            self._topology = Topology(self._topology_settings)
            if connect:
                self._topology.open()

            def target():
                client = self_ref()
                if client is None:
                    return False
                MongoClient._process_periodic_tasks(client)
                return True

            executor = periodic_executor.PeriodicExecutor(interval=(common.KILL_CURSOR_FREQUENCY),
              min_interval=0.5,
              target=target,
              name='pymongo_kill_cursors_thread')
            self_ref = weakref.ref(self, executor.close)
            self._kill_cursors_executor = executor
            executor.open()
            self._encrypter = None
            if self._MongoClient__options.auto_encryption_opts:
                from pymongo.encryption import _Encrypter
                self._encrypter = _Encrypter.create(self, self._MongoClient__options.auto_encryption_opts)

    def _cache_credentials(self, source, credentials, connect=False):
        """Save a set of authentication credentials.

        The credentials are used to login a socket whenever one is created.
        If `connect` is True, verify the credentials on the server first.
        """
        all_credentials = self._MongoClient__all_credentials.copy()
        if source in all_credentials:
            if credentials == all_credentials[source]:
                return
            raise OperationFailure('Another user is already authenticated to this database. You must logout first.')
        if connect:
            server = self._get_topology().select_server(writable_preferred_server_selector)
            with server.get_socket(all_credentials) as (sock_info):
                sock_info.authenticate(credentials)
        self._MongoClient__all_credentials[source] = credentials

    def _purge_credentials(self, source):
        """Purge credentials from the authentication cache."""
        self._MongoClient__all_credentials.pop(source, None)

    def _cached--- This code section failed: ---

 L. 766         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _MongoClient__index_cache
                4  STORE_FAST               'cache'

 L. 767         6  LOAD_GLOBAL              datetime
                8  LOAD_ATTR                datetime
               10  LOAD_METHOD              utcnow
               12  CALL_METHOD_0         0  ''
               14  STORE_FAST               'now'

 L. 768        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _MongoClient__index_cache_lock
               20  SETUP_WITH           92  'to 92'
               22  POP_TOP          

 L. 769        24  LOAD_FAST                'dbname'
               26  LOAD_FAST                'cache'
               28  COMPARE_OP               in
               30  JUMP_IF_FALSE_OR_POP    78  'to 78'

 L. 770        32  LOAD_FAST                'coll'
               34  LOAD_FAST                'cache'
               36  LOAD_FAST                'dbname'
               38  BINARY_SUBSCR    
               40  COMPARE_OP               in

 L. 769        42  JUMP_IF_FALSE_OR_POP    78  'to 78'

 L. 771        44  LOAD_FAST                'index'
               46  LOAD_FAST                'cache'
               48  LOAD_FAST                'dbname'
               50  BINARY_SUBSCR    
               52  LOAD_FAST                'coll'
               54  BINARY_SUBSCR    
               56  COMPARE_OP               in

 L. 769        58  JUMP_IF_FALSE_OR_POP    78  'to 78'

 L. 772        60  LOAD_FAST                'now'
               62  LOAD_FAST                'cache'
               64  LOAD_FAST                'dbname'
               66  BINARY_SUBSCR    
               68  LOAD_FAST                'coll'
               70  BINARY_SUBSCR    
               72  LOAD_FAST                'index'
               74  BINARY_SUBSCR    
               76  COMPARE_OP               <
             78_0  COME_FROM            58  '58'
             78_1  COME_FROM            42  '42'
             78_2  COME_FROM            30  '30'

 L. 769        78  POP_BLOCK        
               80  ROT_TWO          
               82  BEGIN_FINALLY    
               84  WITH_CLEANUP_START
               86  WITH_CLEANUP_FINISH
               88  POP_FINALLY           0  ''
               90  RETURN_VALUE     
             92_0  COME_FROM_WITH       20  '20'
               92  WITH_CLEANUP_START
               94  WITH_CLEANUP_FINISH
               96  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 80

    def _cache_index(self, dbname, collection, index, cache_for):
        """Add an index to the index cache for ensure_index operations."""
        now = datetime.datetime.utcnow()
        expire = datetime.timedelta(seconds=cache_for) + now
        with self._MongoClient__index_cache_lock:
            if dbname not in self._MongoClient__index_cache:
                self._MongoClient__index_cache[dbname] = {}
                self._MongoClient__index_cache[dbname][collection] = {}
                self._MongoClient__index_cache[dbname][collection][index] = expire
            else:
                if collection not in self._MongoClient__index_cache[dbname]:
                    self._MongoClient__index_cache[dbname][collection] = {}
                    self._MongoClient__index_cache[dbname][collection][index] = expire
                else:
                    self._MongoClient__index_cache[dbname][collection][index] = expire

    def _purge_index--- This code section failed: ---

 L. 800         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _MongoClient__index_cache_lock
                4  SETUP_WITH          162  'to 162'
                6  POP_TOP          

 L. 801         8  LOAD_FAST                'database_name'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _MongoClient__index_cache
               14  COMPARE_OP               not-in
               16  POP_JUMP_IF_FALSE    32  'to 32'

 L. 802        18  POP_BLOCK        
               20  BEGIN_FINALLY    
               22  WITH_CLEANUP_START
               24  WITH_CLEANUP_FINISH
               26  POP_FINALLY           0  ''
               28  LOAD_CONST               None
               30  RETURN_VALUE     
             32_0  COME_FROM            16  '16'

 L. 804        32  LOAD_FAST                'collection_name'
               34  LOAD_CONST               None
               36  COMPARE_OP               is
               38  POP_JUMP_IF_FALSE    62  'to 62'

 L. 805        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _MongoClient__index_cache
               44  LOAD_FAST                'database_name'
               46  DELETE_SUBSCR    

 L. 806        48  POP_BLOCK        
               50  BEGIN_FINALLY    
               52  WITH_CLEANUP_START
               54  WITH_CLEANUP_FINISH
               56  POP_FINALLY           0  ''
               58  LOAD_CONST               None
               60  RETURN_VALUE     
             62_0  COME_FROM            38  '38'

 L. 808        62  LOAD_FAST                'collection_name'
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                _MongoClient__index_cache
               68  LOAD_FAST                'database_name'
               70  BINARY_SUBSCR    
               72  COMPARE_OP               not-in
               74  POP_JUMP_IF_FALSE    90  'to 90'

 L. 809        76  POP_BLOCK        
               78  BEGIN_FINALLY    
               80  WITH_CLEANUP_START
               82  WITH_CLEANUP_FINISH
               84  POP_FINALLY           0  ''
               86  LOAD_CONST               None
               88  RETURN_VALUE     
             90_0  COME_FROM            74  '74'

 L. 811        90  LOAD_FAST                'index_name'
               92  LOAD_CONST               None
               94  COMPARE_OP               is
               96  POP_JUMP_IF_FALSE   124  'to 124'

 L. 812        98  LOAD_FAST                'self'
              100  LOAD_ATTR                _MongoClient__index_cache
              102  LOAD_FAST                'database_name'
              104  BINARY_SUBSCR    
              106  LOAD_FAST                'collection_name'
              108  DELETE_SUBSCR    

 L. 813       110  POP_BLOCK        
              112  BEGIN_FINALLY    
              114  WITH_CLEANUP_START
              116  WITH_CLEANUP_FINISH
              118  POP_FINALLY           0  ''
              120  LOAD_CONST               None
              122  RETURN_VALUE     
            124_0  COME_FROM            96  '96'

 L. 815       124  LOAD_FAST                'index_name'
              126  LOAD_FAST                'self'
              128  LOAD_ATTR                _MongoClient__index_cache
              130  LOAD_FAST                'database_name'
              132  BINARY_SUBSCR    
              134  LOAD_FAST                'collection_name'
              136  BINARY_SUBSCR    
              138  COMPARE_OP               in
              140  POP_JUMP_IF_FALSE   158  'to 158'

 L. 816       142  LOAD_FAST                'self'
              144  LOAD_ATTR                _MongoClient__index_cache
              146  LOAD_FAST                'database_name'
              148  BINARY_SUBSCR    
              150  LOAD_FAST                'collection_name'
              152  BINARY_SUBSCR    
              154  LOAD_FAST                'index_name'
              156  DELETE_SUBSCR    
            158_0  COME_FROM           140  '140'
              158  POP_BLOCK        
              160  BEGIN_FINALLY    
            162_0  COME_FROM_WITH        4  '4'
              162  WITH_CLEANUP_START
              164  WITH_CLEANUP_FINISH
              166  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 20

    def _server_property(self, attr_name):
        """An attribute of the current server's description.

        If the client is not connected, this will block until a connection is
        established or raise ServerSelectionTimeoutError if no server is
        available.

        Not threadsafe if used multiple times in a single method, since
        the server may change. In such cases, store a local reference to a
        ServerDescription first, then use its properties.
        """
        server = self._topology.select_server(writable_server_selector)
        return getattr(server.description, attr_name)

    def watch(self, pipeline=None, full_document=None, resume_after=None, max_await_time_ms=None, batch_size=None, collation=None, start_at_operation_time=None, session=None, start_after=None):
        """Watch changes on this cluster.

        Performs an aggregation with an implicit initial ``$changeStream``
        stage and returns a
        :class:`~pymongo.change_stream.ClusterChangeStream` cursor which
        iterates over changes on all databases on this cluster.

        Introduced in MongoDB 4.0.

        .. code-block:: python

           with client.watch() as stream:
               for change in stream:
                   print(change)

        The :class:`~pymongo.change_stream.ClusterChangeStream` iterable
        blocks until the next change document is returned or an error is
        raised. If the
        :meth:`~pymongo.change_stream.ClusterChangeStream.next` method
        encounters a network error when retrieving a batch from the server,
        it will automatically attempt to recreate the cursor such that no
        change events are missed. Any error encountered during the resume
        attempt indicates there may be an outage and will be raised.

        .. code-block:: python

            try:
                with client.watch(
                        [{'$match': {'operationType': 'insert'}}]) as stream:
                    for insert_change in stream:
                        print(insert_change)
            except pymongo.errors.PyMongoError:
                # The ChangeStream encountered an unrecoverable error or the
                # resume attempt failed to recreate the cursor.
                logging.error('...')

        For a precise description of the resume process see the
        `change streams specification`_.

        :Parameters:
          - `pipeline` (optional): A list of aggregation pipeline stages to
            append to an initial ``$changeStream`` stage. Not all
            pipeline stages are valid after a ``$changeStream`` stage, see the
            MongoDB documentation on change streams for the supported stages.
          - `full_document` (optional): The fullDocument to pass as an option
            to the ``$changeStream`` stage. Allowed values: 'updateLookup'.
            When set to 'updateLookup', the change notification for partial
            updates will include both a delta describing the changes to the
            document, as well as a copy of the entire document that was
            changed from some time after the change occurred.
          - `resume_after` (optional): A resume token. If provided, the
            change stream will start returning changes that occur directly
            after the operation specified in the resume token. A resume token
            is the _id value of a change document.
          - `max_await_time_ms` (optional): The maximum time in milliseconds
            for the server to wait for changes before responding to a getMore
            operation.
          - `batch_size` (optional): The maximum number of documents to return
            per batch.
          - `collation` (optional): The :class:`~pymongo.collation.Collation`
            to use for the aggregation.
          - `start_at_operation_time` (optional): If provided, the resulting
            change stream will only return changes that occurred at or after
            the specified :class:`~bson.timestamp.Timestamp`. Requires
            MongoDB >= 4.0.
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.
          - `start_after` (optional): The same as `resume_after` except that
            `start_after` can resume notifications after an invalidate event.
            This option and `resume_after` are mutually exclusive.

        :Returns:
          A :class:`~pymongo.change_stream.ClusterChangeStream` cursor.

        .. versionchanged:: 3.9
           Added the ``start_after`` parameter.

        .. versionadded:: 3.7

        .. mongodoc:: changeStreams

        .. _change streams specification:
            https://github.com/mongodb/specifications/blob/master/source/change-streams/change-streams.rst
        """
        return ClusterChangeStream(self.admin, pipeline, full_document, resume_after, max_await_time_ms, batch_size, collation, start_at_operation_time, session, start_after)

    @property
    def event_listeners(self):
        """The event listeners registered for this client.

        See :mod:`~pymongo.monitoring` for details.
        """
        return self._event_listeners.event_listeners

    @property
    def address(self):
        """(host, port) of the current standalone, primary, or mongos, or None.

        Accessing :attr:`address` raises :exc:`~.errors.InvalidOperation` if
        the client is load-balancing among mongoses, since there is no single
        address. Use :attr:`nodes` instead.

        If the client is not connected, this will block until a connection is
        established or raise ServerSelectionTimeoutError if no server is
        available.

        .. versionadded:: 3.0
        """
        topology_type = self._topology._description.topology_type
        if topology_type == TOPOLOGY_TYPE.Sharded:
            raise InvalidOperation('Cannot use "address" property when load balancing among mongoses, use "nodes" instead.')
        if topology_type not in (TOPOLOGY_TYPE.ReplicaSetWithPrimary,
         TOPOLOGY_TYPE.Single):
            return
        return self._server_property('address')

    @property
    def primary(self):
        """The (host, port) of the current primary of the replica set.

        Returns ``None`` if this client is not connected to a replica set,
        there is no primary, or this client was created without the
        `replicaSet` option.

        .. versionadded:: 3.0
           MongoClient gained this property in version 3.0 when
           MongoReplicaSetClient's functionality was merged in.
        """
        return self._topology.get_primary()

    @property
    def secondaries(self):
        """The secondary members known to this client.

        A sequence of (host, port) pairs. Empty if this client is not
        connected to a replica set, there are no visible secondaries, or this
        client was created without the `replicaSet` option.

        .. versionadded:: 3.0
           MongoClient gained this property in version 3.0 when
           MongoReplicaSetClient's functionality was merged in.
        """
        return self._topology.get_secondaries()

    @property
    def arbiters(self):
        """Arbiters in the replica set.

        A sequence of (host, port) pairs. Empty if this client is not
        connected to a replica set, there are no arbiters, or this client was
        created without the `replicaSet` option.
        """
        return self._topology.get_arbiters()

    @property
    def is_primary(self):
        """If this client is connected to a server that can accept writes.

        True if the current server is a standalone, mongos, or the primary of
        a replica set. If the client is not connected, this will block until a
        connection is established or raise ServerSelectionTimeoutError if no
        server is available.
        """
        return self._server_property('is_writable')

    @property
    def is_mongos(self):
        """If this client is connected to mongos. If the client is not
        connected, this will block until a connection is established or raise
        ServerSelectionTimeoutError if no server is available..
        """
        return self._server_property('server_type') == SERVER_TYPE.Mongos

    @property
    def max_pool_size(self):
        """The maximum allowable number of concurrent connections to each
        connected server. Requests to a server will block if there are
        `maxPoolSize` outstanding connections to the requested server.
        Defaults to 100. Cannot be 0.

        When a server's pool has reached `max_pool_size`, operations for that
        server block waiting for a socket to be returned to the pool. If
        ``waitQueueTimeoutMS`` is set, a blocked operation will raise
        :exc:`~pymongo.errors.ConnectionFailure` after a timeout.
        By default ``waitQueueTimeoutMS`` is not set.
        """
        return self._MongoClient__options.pool_options.max_pool_size

    @property
    def min_pool_size(self):
        """The minimum required number of concurrent connections that the pool
        will maintain to each connected server. Default is 0.
        """
        return self._MongoClient__options.pool_options.min_pool_size

    @property
    def max_idle_time_ms(self):
        """The maximum number of milliseconds that a connection can remain
        idle in the pool before being removed and replaced. Defaults to
        `None` (no limit).
        """
        seconds = self._MongoClient__options.pool_options.max_idle_time_seconds
        if seconds is None:
            return
        return 1000 * seconds

    @property
    def nodes(self):
        """Set of all currently connected servers.

        .. warning:: When connected to a replica set the value of :attr:`nodes`
          can change over time as :class:`MongoClient`'s view of the replica
          set changes. :attr:`nodes` can also be an empty set when
          :class:`MongoClient` is first instantiated and hasn't yet connected
          to any servers, or a network partition causes it to lose connection
          to all servers.
        """
        description = self._topology.description
        return frozenset((s.address for s in description.known_servers))

    @property
    def max_bson_size(self):
        """The largest BSON object the connected server accepts in bytes.

        If the client is not connected, this will block until a connection is
        established or raise ServerSelectionTimeoutError if no server is
        available.
        """
        return self._server_property('max_bson_size')

    @property
    def max_message_size(self):
        """The largest message the connected server accepts in bytes.

        If the client is not connected, this will block until a connection is
        established or raise ServerSelectionTimeoutError if no server is
        available.
        """
        return self._server_property('max_message_size')

    @property
    def max_write_batch_size(self):
        """The maxWriteBatchSize reported by the server.

        If the client is not connected, this will block until a connection is
        established or raise ServerSelectionTimeoutError if no server is
        available.

        Returns a default value when connected to server versions prior to
        MongoDB 2.6.
        """
        return self._server_property('max_write_batch_size')

    @property
    def local_threshold_ms(self):
        """The local threshold for this instance."""
        return self._MongoClient__options.local_threshold_ms

    @property
    def server_selection_timeout(self):
        """The server selection timeout for this instance in seconds."""
        return self._MongoClient__options.server_selection_timeout

    @property
    def retry_writes(self):
        """If this instance should retry supported write operations."""
        return self._MongoClient__options.retry_writes

    @property
    def retry_reads(self):
        """If this instance should retry supported write operations."""
        return self._MongoClient__options.retry_reads

    def _is_writable--- This code section failed: ---

 L.1118         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _get_topology
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'topology'

 L.1119         8  SETUP_FINALLY        30  'to 30'

 L.1120        10  LOAD_FAST                'topology'
               12  LOAD_METHOD              select_server
               14  LOAD_GLOBAL              writable_server_selector
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'svr'

 L.1125        20  LOAD_FAST                'svr'
               22  LOAD_ATTR                description
               24  LOAD_ATTR                is_writable
               26  POP_BLOCK        
               28  RETURN_VALUE     
             30_0  COME_FROM_FINALLY     8  '8'

 L.1126        30  DUP_TOP          
               32  LOAD_GLOBAL              ConnectionFailure
               34  COMPARE_OP               exception-match
               36  POP_JUMP_IF_FALSE    50  'to 50'
               38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          

 L.1127        44  POP_EXCEPT       
               46  LOAD_CONST               False
               48  RETURN_VALUE     
             50_0  COME_FROM            36  '36'
               50  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 40

    def _end_sessions--- This code section failed: ---

 L.1131         0  SETUP_FINALLY       128  'to 128'

 L.1134         2  LOAD_FAST                'self'
                4  LOAD_METHOD              _socket_for_reads

 L.1135         6  LOAD_GLOBAL              ReadPreference
                8  LOAD_ATTR                PRIMARY_PREFERRED

 L.1136        10  LOAD_CONST               None

 L.1134        12  CALL_METHOD_2         2  ''
               14  SETUP_WITH          118  'to 118'

 L.1136        16  UNPACK_SEQUENCE_2     2 
               18  STORE_FAST               'sock_info'
               20  STORE_FAST               'slave_ok'

 L.1137        22  LOAD_FAST                'sock_info'
               24  LOAD_ATTR                supports_sessions
               26  POP_JUMP_IF_TRUE     44  'to 44'

 L.1138        28  POP_BLOCK        
               30  BEGIN_FINALLY    
               32  WITH_CLEANUP_START
               34  WITH_CLEANUP_FINISH
               36  POP_FINALLY           0  ''
               38  POP_BLOCK        
               40  LOAD_CONST               None
               42  RETURN_VALUE     
             44_0  COME_FROM            26  '26'

 L.1140        44  LOAD_GLOBAL              range
               46  LOAD_CONST               0
               48  LOAD_GLOBAL              len
               50  LOAD_FAST                'session_ids'
               52  CALL_FUNCTION_1       1  ''
               54  LOAD_GLOBAL              common
               56  LOAD_ATTR                _MAX_END_SESSIONS
               58  CALL_FUNCTION_3       3  ''
               60  GET_ITER         
               62  FOR_ITER            114  'to 114'
               64  STORE_FAST               'i'

 L.1141        66  LOAD_GLOBAL              SON
               68  LOAD_STR                 'endSessions'

 L.1142        70  LOAD_FAST                'session_ids'
               72  LOAD_FAST                'i'
               74  LOAD_FAST                'i'
               76  LOAD_GLOBAL              common
               78  LOAD_ATTR                _MAX_END_SESSIONS
               80  BINARY_ADD       
               82  BUILD_SLICE_2         2 
               84  BINARY_SUBSCR    

 L.1141        86  BUILD_TUPLE_2         2 
               88  BUILD_LIST_1          1 
               90  CALL_FUNCTION_1       1  ''
               92  STORE_FAST               'spec'

 L.1143        94  LOAD_FAST                'sock_info'
               96  LOAD_ATTR                command

 L.1144        98  LOAD_STR                 'admin'

 L.1144       100  LOAD_FAST                'spec'

 L.1144       102  LOAD_FAST                'slave_ok'

 L.1144       104  LOAD_FAST                'self'

 L.1143       106  LOAD_CONST               ('slave_ok', 'client')
              108  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              110  POP_TOP          
              112  JUMP_BACK            62  'to 62'
              114  POP_BLOCK        
              116  BEGIN_FINALLY    
            118_0  COME_FROM_WITH       14  '14'
              118  WITH_CLEANUP_START
              120  WITH_CLEANUP_FINISH
              122  END_FINALLY      
              124  POP_BLOCK        
              126  JUMP_FORWARD        148  'to 148'
            128_0  COME_FROM_FINALLY     0  '0'

 L.1145       128  DUP_TOP          
              130  LOAD_GLOBAL              PyMongoError
              132  COMPARE_OP               exception-match
              134  POP_JUMP_IF_FALSE   146  'to 146'
              136  POP_TOP          
              138  POP_TOP          
              140  POP_TOP          

 L.1148       142  POP_EXCEPT       
              144  JUMP_FORWARD        148  'to 148'
            146_0  COME_FROM           134  '134'
              146  END_FINALLY      
            148_0  COME_FROM           144  '144'
            148_1  COME_FROM           126  '126'

Parse error at or near `BEGIN_FINALLY' instruction at offset 30

    def close(self):
        """Cleanup client resources and disconnect from MongoDB.

        On MongoDB >= 3.6, end all server sessions created by this client by
        sending one or more endSessions commands.

        Close all sockets in the connection pools and stop the monitor threads.
        If this instance is used again it will be automatically re-opened and
        the threads restarted unless auto encryption is enabled. A client
        enabled with auto encryption cannot be used again after being closed;
        any attempt will raise :exc:`~.errors.InvalidOperation`.

        .. versionchanged:: 3.6
           End all server sessions created by this client.
        """
        session_ids = self._topology.pop_all_sessions()
        if session_ids:
            self._end_sessions(session_ids)
        self._kill_cursors_executor.close()
        self._process_kill_cursors()
        self._topology.close()
        if self._encrypter:
            self._encrypter.close()

    def set_cursor_manager(self, manager_class):
        """DEPRECATED - Set this client's cursor manager.

        Raises :class:`TypeError` if `manager_class` is not a subclass of
        :class:`~pymongo.cursor_manager.CursorManager`. A cursor manager
        handles closing cursors. Different managers can implement different
        policies in terms of when to actually kill a cursor that has
        been closed.

        :Parameters:
          - `manager_class`: cursor manager to use

        .. versionchanged:: 3.3
           Deprecated, for real this time.

        .. versionchanged:: 3.0
           Undeprecated.
        """
        warnings.warn('set_cursor_manager is Deprecated',
          DeprecationWarning,
          stacklevel=2)
        manager = manager_class(self)
        if not isinstance(manager, CursorManager):
            raise TypeError('manager_class must be a subclass of CursorManager')
        self._MongoClient__cursor_manager = manager

    def _get_topology(self):
        """Get the internal :class:`~pymongo.topology.Topology` object.

        If this client was created with "connect=False", calling _get_topology
        launches the connection process in the background.
        """
        self._topology.open()
        with self._MongoClient__lock:
            self._kill_cursors_executor.open()
        return self._topology

    @contextlib.contextmanager
    def _get_socket(self, server, session, exhaust=False):
        with _MongoClientErrorHandler(self, server.description.address, session) as (err_handler):
            with server.get_socket((self._MongoClient__all_credentials),
              checkout=exhaust) as (sock_info):
                err_handler.contribute_socket(sock_info)
                if self._encrypter:
                    if not self._encrypter._bypass_auto_encryption:
                        if sock_info.max_wire_version < 8:
                            raise ConfigurationError('Auto-encryption requires a minimum MongoDB version of 4.2')
                (yield sock_info)

    def _select_server(self, server_selector, session, address=None):
        """Select a server to run an operation on this client.

        :Parameters:
          - `server_selector`: The server selector to use if the session is
            not pinned and no address is given.
          - `session`: The ClientSession for the next operation, or None. May
            be pinned to a mongos server address.
          - `address` (optional): Address when sending a message
            to a specific server, used for getMore.
        """
        try:
            topology = self._get_topology()
            address = address or session and session._pinned_address
            if address:
                server = topology.select_server_by_address(address)
                assert server, 'server %s:%d no longer available' % address
            else:
                server = topology.select_server(server_selector)
                if server.description.mongos and session and session.in_transaction:
                    session._pin_mongos(server)
            return server
            except PyMongoError as exc:
            try:
                if session:
                    if exc.has_error_label('TransientTransactionError'):
                        session._unpin_mongos()
                raise
            finally:
                exc = None
                del exc

    def _socket_for_writes(self, session):
        server = self._select_server(writable_server_selector, session)
        return self._get_socket(server, session)

    @contextlib.contextmanager
    def _slaveok_for_server(self, read_preference, server, session, exhaust=False):
        assert read_preference is not None, 'read_preference must not be None'
        topology = self._get_topology()
        single = topology.description.topology_type == TOPOLOGY_TYPE.Single
        with self._get_socket(server, session, exhaust=exhaust) as (sock_info):
            slave_ok = single and not sock_info.is_mongos or read_preference != ReadPreference.PRIMARY
            (yield (sock_info, slave_ok))

    @contextlib.contextmanager
    def _socket_for_reads(self, read_preference, session):
        assert read_preference is not None, 'read_preference must not be None'
        topology = self._get_topology()
        single = topology.description.topology_type == TOPOLOGY_TYPE.Single
        server = self._select_server(read_preference, session)
        with self._get_socket(server, session) as (sock_info):
            slave_ok = single and not sock_info.is_mongos or read_preference != ReadPreference.PRIMARY
            (yield (sock_info, slave_ok))

    def _run_operation_with_response--- This code section failed: ---

 L.1317         0  LOAD_DEREF               'operation'
                2  LOAD_ATTR                exhaust_mgr
                4  POP_JUMP_IF_FALSE   104  'to 104'

 L.1318         6  LOAD_DEREF               'self'
                8  LOAD_ATTR                _select_server

 L.1319        10  LOAD_DEREF               'operation'
               12  LOAD_ATTR                read_preference

 L.1319        14  LOAD_DEREF               'operation'
               16  LOAD_ATTR                session

 L.1319        18  LOAD_FAST                'address'

 L.1318        20  LOAD_CONST               ('address',)
               22  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               24  STORE_FAST               'server'

 L.1321        26  LOAD_GLOBAL              _MongoClientErrorHandler

 L.1322        28  LOAD_DEREF               'self'

 L.1322        30  LOAD_FAST                'server'
               32  LOAD_ATTR                description
               34  LOAD_ATTR                address

 L.1323        36  LOAD_DEREF               'operation'
               38  LOAD_ATTR                session

 L.1321        40  CALL_FUNCTION_3       3  ''
               42  SETUP_WITH           98  'to 98'

 L.1323        44  STORE_FAST               'err_handler'

 L.1324        46  LOAD_FAST                'err_handler'
               48  LOAD_METHOD              contribute_socket
               50  LOAD_DEREF               'operation'
               52  LOAD_ATTR                exhaust_mgr
               54  LOAD_ATTR                sock
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          

 L.1325        60  LOAD_FAST                'server'
               62  LOAD_METHOD              run_operation_with_response

 L.1326        64  LOAD_DEREF               'operation'
               66  LOAD_ATTR                exhaust_mgr
               68  LOAD_ATTR                sock

 L.1327        70  LOAD_DEREF               'operation'

 L.1328        72  LOAD_CONST               True

 L.1329        74  LOAD_DEREF               'self'
               76  LOAD_ATTR                _event_listeners

 L.1330        78  LOAD_DEREF               'exhaust'

 L.1331        80  LOAD_DEREF               'unpack_res'

 L.1325        82  CALL_METHOD_6         6  ''
               84  POP_BLOCK        
               86  ROT_TWO          
               88  BEGIN_FINALLY    
               90  WITH_CLEANUP_START
               92  WITH_CLEANUP_FINISH
               94  POP_FINALLY           0  ''
               96  RETURN_VALUE     
             98_0  COME_FROM_WITH       42  '42'
               98  WITH_CLEANUP_START
              100  WITH_CLEANUP_FINISH
              102  END_FINALLY      
            104_0  COME_FROM             4  '4'

 L.1333       104  LOAD_CLOSURE             'exhaust'
              106  LOAD_CLOSURE             'operation'
              108  LOAD_CLOSURE             'self'
              110  LOAD_CLOSURE             'unpack_res'
              112  BUILD_TUPLE_4         4 
              114  LOAD_CODE                <code_object _cmd>
              116  LOAD_STR                 'MongoClient._run_operation_with_response.<locals>._cmd'
              118  MAKE_FUNCTION_8          'closure'
              120  STORE_FAST               '_cmd'

 L.1342       122  LOAD_DEREF               'self'
              124  LOAD_ATTR                _retryable_read

 L.1343       126  LOAD_FAST                '_cmd'

 L.1343       128  LOAD_DEREF               'operation'
              130  LOAD_ATTR                read_preference

 L.1343       132  LOAD_DEREF               'operation'
              134  LOAD_ATTR                session

 L.1344       136  LOAD_FAST                'address'

 L.1345       138  LOAD_GLOBAL              isinstance
              140  LOAD_DEREF               'operation'
              142  LOAD_GLOBAL              message
              144  LOAD_ATTR                _Query
              146  CALL_FUNCTION_2       2  ''

 L.1346       148  LOAD_DEREF               'exhaust'

 L.1342       150  LOAD_CONST               ('address', 'retryable', 'exhaust')
              152  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              154  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ROT_TWO' instruction at offset 86

    def _retry_with_session--- This code section failed: ---

 L.1356         0  LOAD_FAST                'retryable'
                2  JUMP_IF_FALSE_OR_POP    20  'to 20'
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                retry_writes
                8  JUMP_IF_FALSE_OR_POP    20  'to 20'

 L.1357        10  LOAD_FAST                'session'

 L.1356        12  JUMP_IF_FALSE_OR_POP    20  'to 20'

 L.1357        14  LOAD_FAST                'session'
               16  LOAD_ATTR                in_transaction
               18  UNARY_NOT        
             20_0  COME_FROM            12  '12'
             20_1  COME_FROM             8  '8'
             20_2  COME_FROM             2  '2'

 L.1356        20  STORE_FAST               'retryable'

 L.1358        22  LOAD_CONST               None
               24  STORE_FAST               'last_error'

 L.1359        26  LOAD_CONST               False
               28  STORE_DEREF              'retrying'

 L.1361        30  LOAD_CLOSURE             'bulk'
               32  LOAD_CLOSURE             'retrying'
               34  BUILD_TUPLE_2         2 
               36  LOAD_CODE                <code_object is_retrying>
               38  LOAD_STR                 'MongoClient._retry_with_session.<locals>.is_retrying'
               40  MAKE_FUNCTION_8          'closure'
               42  STORE_FAST               'is_retrying'

 L.1366        44  LOAD_FAST                'retryable'
               46  POP_JUMP_IF_FALSE    66  'to 66'

 L.1367        48  LOAD_FAST                'session'
               50  LOAD_METHOD              _start_retryable_write
               52  CALL_METHOD_0         0  ''
               54  POP_TOP          

 L.1368        56  LOAD_DEREF               'bulk'
               58  POP_JUMP_IF_FALSE    66  'to 66'

 L.1369        60  LOAD_CONST               True
               62  LOAD_DEREF               'bulk'
               64  STORE_ATTR               started_retryable_write
             66_0  COME_FROM            58  '58'
             66_1  COME_FROM            46  '46'

 L.1372        66  SETUP_FINALLY       168  'to 168'

 L.1373        68  LOAD_FAST                'self'
               70  LOAD_METHOD              _select_server
               72  LOAD_GLOBAL              writable_server_selector
               74  LOAD_FAST                'session'
               76  CALL_METHOD_2         2  ''
               78  STORE_FAST               'server'

 L.1375        80  LOAD_FAST                'session'
               82  LOAD_CONST               None
               84  COMPARE_OP               is-not
               86  JUMP_IF_FALSE_OR_POP    94  'to 94'

 L.1376        88  LOAD_FAST                'server'
               90  LOAD_ATTR                description
               92  LOAD_ATTR                retryable_writes_supported
             94_0  COME_FROM            86  '86'

 L.1374        94  STORE_FAST               'supports_session'

 L.1377        96  LOAD_FAST                'self'
               98  LOAD_METHOD              _get_socket
              100  LOAD_FAST                'server'
              102  LOAD_FAST                'session'
              104  CALL_METHOD_2         2  ''
              106  SETUP_WITH          158  'to 158'
              108  STORE_FAST               'sock_info'

 L.1378       110  LOAD_FAST                'retryable'
              112  POP_JUMP_IF_FALSE   132  'to 132'
              114  LOAD_FAST                'supports_session'
              116  POP_JUMP_IF_TRUE    132  'to 132'

 L.1379       118  LOAD_FAST                'is_retrying'
              120  CALL_FUNCTION_0       0  ''
              122  POP_JUMP_IF_FALSE   128  'to 128'

 L.1382       124  LOAD_FAST                'last_error'
              126  RAISE_VARARGS_1       1  'exception instance'
            128_0  COME_FROM           122  '122'

 L.1383       128  LOAD_CONST               False
              130  STORE_FAST               'retryable'
            132_0  COME_FROM           116  '116'
            132_1  COME_FROM           112  '112'

 L.1384       132  LOAD_FAST                'func'
              134  LOAD_FAST                'session'
              136  LOAD_FAST                'sock_info'
              138  LOAD_FAST                'retryable'
              140  CALL_FUNCTION_3       3  ''
              142  POP_BLOCK        
              144  ROT_TWO          
              146  BEGIN_FINALLY    
              148  WITH_CLEANUP_START
              150  WITH_CLEANUP_FINISH
              152  POP_FINALLY           0  ''
              154  POP_BLOCK        
              156  RETURN_VALUE     
            158_0  COME_FROM_WITH      106  '106'
              158  WITH_CLEANUP_START
              160  WITH_CLEANUP_FINISH
              162  END_FINALLY      
              164  POP_BLOCK        
              166  JUMP_BACK            66  'to 66'
            168_0  COME_FROM_FINALLY    66  '66'

 L.1385       168  DUP_TOP          
              170  LOAD_GLOBAL              ServerSelectionTimeoutError
              172  COMPARE_OP               exception-match
              174  POP_JUMP_IF_FALSE   198  'to 198'
              176  POP_TOP          
              178  POP_TOP          
              180  POP_TOP          

 L.1386       182  LOAD_FAST                'is_retrying'
              184  CALL_FUNCTION_0       0  ''
              186  POP_JUMP_IF_FALSE   192  'to 192'

 L.1390       188  LOAD_FAST                'last_error'
              190  RAISE_VARARGS_1       1  'exception instance'
            192_0  COME_FROM           186  '186'

 L.1394       192  RAISE_VARARGS_0       0  'reraise'
              194  POP_EXCEPT       
              196  JUMP_BACK            66  'to 66'
            198_0  COME_FROM           174  '174'

 L.1395       198  DUP_TOP          
              200  LOAD_GLOBAL              ConnectionFailure
              202  COMPARE_OP               exception-match
          204_206  POP_JUMP_IF_FALSE   264  'to 264'
              208  POP_TOP          
              210  STORE_FAST               'exc'
              212  POP_TOP          
              214  SETUP_FINALLY       252  'to 252'

 L.1396       216  LOAD_FAST                'retryable'
              218  POP_JUMP_IF_FALSE   226  'to 226'
              220  LOAD_FAST                'is_retrying'
              222  CALL_FUNCTION_0       0  ''
              224  POP_JUMP_IF_FALSE   228  'to 228'
            226_0  COME_FROM           218  '218'

 L.1397       226  RAISE_VARARGS_0       0  'reraise'
            228_0  COME_FROM           224  '224'

 L.1398       228  LOAD_DEREF               'bulk'
              230  POP_JUMP_IF_FALSE   240  'to 240'

 L.1399       232  LOAD_CONST               True
              234  LOAD_DEREF               'bulk'
              236  STORE_ATTR               retrying
              238  JUMP_FORWARD        244  'to 244'
            240_0  COME_FROM           230  '230'

 L.1401       240  LOAD_CONST               True
              242  STORE_DEREF              'retrying'
            244_0  COME_FROM           238  '238'

 L.1402       244  LOAD_FAST                'exc'
              246  STORE_FAST               'last_error'
              248  POP_BLOCK        
              250  BEGIN_FINALLY    
            252_0  COME_FROM_FINALLY   214  '214'
              252  LOAD_CONST               None
              254  STORE_FAST               'exc'
              256  DELETE_FAST              'exc'
              258  END_FINALLY      
              260  POP_EXCEPT       
              262  JUMP_BACK            66  'to 66'
            264_0  COME_FROM           204  '204'

 L.1403       264  DUP_TOP          
              266  LOAD_GLOBAL              BulkWriteError
              268  COMPARE_OP               exception-match
          270_272  POP_JUMP_IF_FALSE   386  'to 386'
              274  POP_TOP          
              276  STORE_FAST               'exc'
              278  POP_TOP          
              280  SETUP_FINALLY       374  'to 374'

 L.1404       282  LOAD_FAST                'retryable'
          284_286  POP_JUMP_IF_FALSE   296  'to 296'
              288  LOAD_FAST                'is_retrying'
              290  CALL_FUNCTION_0       0  ''
          292_294  POP_JUMP_IF_FALSE   298  'to 298'
            296_0  COME_FROM           284  '284'

 L.1405       296  RAISE_VARARGS_0       0  'reraise'
            298_0  COME_FROM           292  '292'

 L.1408       298  LOAD_FAST                'exc'
              300  LOAD_ATTR                details
              302  LOAD_STR                 'writeConcernErrors'
              304  BINARY_SUBSCR    
              306  STORE_FAST               'wces'

 L.1409       308  LOAD_FAST                'wces'
          310_312  POP_JUMP_IF_FALSE   322  'to 322'
              314  LOAD_FAST                'wces'
              316  LOAD_CONST               -1
              318  BINARY_SUBSCR    
              320  JUMP_FORWARD        324  'to 324'
            322_0  COME_FROM           310  '310'
              322  BUILD_MAP_0           0 
            324_0  COME_FROM           320  '320'
              324  STORE_FAST               'wce'

 L.1410       326  LOAD_FAST                'wce'
              328  LOAD_METHOD              get
              330  LOAD_STR                 'code'
              332  LOAD_CONST               0
              334  CALL_METHOD_2         2  ''
              336  LOAD_GLOBAL              helpers
              338  LOAD_ATTR                _RETRYABLE_ERROR_CODES
              340  COMPARE_OP               not-in
          342_344  POP_JUMP_IF_FALSE   348  'to 348'

 L.1411       346  RAISE_VARARGS_0       0  'reraise'
            348_0  COME_FROM           342  '342'

 L.1412       348  LOAD_DEREF               'bulk'
          350_352  POP_JUMP_IF_FALSE   362  'to 362'

 L.1413       354  LOAD_CONST               True
              356  LOAD_DEREF               'bulk'
              358  STORE_ATTR               retrying
              360  JUMP_FORWARD        366  'to 366'
            362_0  COME_FROM           350  '350'

 L.1415       362  LOAD_CONST               True
              364  STORE_DEREF              'retrying'
            366_0  COME_FROM           360  '360'

 L.1416       366  LOAD_FAST                'exc'
              368  STORE_FAST               'last_error'
              370  POP_BLOCK        
              372  BEGIN_FINALLY    
            374_0  COME_FROM_FINALLY   280  '280'
              374  LOAD_CONST               None
              376  STORE_FAST               'exc'
              378  DELETE_FAST              'exc'
              380  END_FINALLY      
              382  POP_EXCEPT       
              384  JUMP_BACK            66  'to 66'
            386_0  COME_FROM           270  '270'

 L.1417       386  DUP_TOP          
              388  LOAD_GLOBAL              OperationFailure
              390  COMPARE_OP               exception-match
          392_394  POP_JUMP_IF_FALSE   522  'to 522'
              396  POP_TOP          
              398  STORE_FAST               'exc'
              400  POP_TOP          
              402  SETUP_FINALLY       510  'to 510'

 L.1419       404  LOAD_FAST                'exc'
              406  LOAD_ATTR                code
              408  LOAD_CONST               20
              410  COMPARE_OP               ==
          412_414  POP_JUMP_IF_FALSE   452  'to 452'

 L.1420       416  LOAD_GLOBAL              str
              418  LOAD_FAST                'exc'
              420  CALL_FUNCTION_1       1  ''
              422  LOAD_METHOD              startswith
              424  LOAD_STR                 'Transaction numbers'
              426  CALL_METHOD_1         1  ''

 L.1419   428_430  POP_JUMP_IF_FALSE   452  'to 452'

 L.1422       432  LOAD_STR                 'This MongoDB deployment does not support retryable writes. Please add retryWrites=false to your connection string.'

 L.1421       434  STORE_FAST               'errmsg'

 L.1425       436  LOAD_GLOBAL              OperationFailure
              438  LOAD_FAST                'errmsg'
              440  LOAD_FAST                'exc'
              442  LOAD_ATTR                code
              444  LOAD_FAST                'exc'
              446  LOAD_ATTR                details
              448  CALL_FUNCTION_3       3  ''
              450  RAISE_VARARGS_1       1  'exception instance'
            452_0  COME_FROM           428  '428'
            452_1  COME_FROM           412  '412'

 L.1426       452  LOAD_FAST                'retryable'
          454_456  POP_JUMP_IF_FALSE   466  'to 466'
              458  LOAD_FAST                'is_retrying'
              460  CALL_FUNCTION_0       0  ''
          462_464  POP_JUMP_IF_FALSE   468  'to 468'
            466_0  COME_FROM           454  '454'

 L.1427       466  RAISE_VARARGS_0       0  'reraise'
            468_0  COME_FROM           462  '462'

 L.1428       468  LOAD_FAST                'exc'
              470  LOAD_ATTR                code
              472  LOAD_GLOBAL              helpers
              474  LOAD_ATTR                _RETRYABLE_ERROR_CODES
              476  COMPARE_OP               not-in
          478_480  POP_JUMP_IF_FALSE   484  'to 484'

 L.1429       482  RAISE_VARARGS_0       0  'reraise'
            484_0  COME_FROM           478  '478'

 L.1430       484  LOAD_DEREF               'bulk'
          486_488  POP_JUMP_IF_FALSE   498  'to 498'

 L.1431       490  LOAD_CONST               True
              492  LOAD_DEREF               'bulk'
              494  STORE_ATTR               retrying
              496  JUMP_FORWARD        502  'to 502'
            498_0  COME_FROM           486  '486'

 L.1433       498  LOAD_CONST               True
              500  STORE_DEREF              'retrying'
            502_0  COME_FROM           496  '496'

 L.1434       502  LOAD_FAST                'exc'
              504  STORE_FAST               'last_error'
              506  POP_BLOCK        
              508  BEGIN_FINALLY    
            510_0  COME_FROM_FINALLY   402  '402'
              510  LOAD_CONST               None
              512  STORE_FAST               'exc'
              514  DELETE_FAST              'exc'
              516  END_FINALLY      
              518  POP_EXCEPT       
              520  JUMP_BACK            66  'to 66'
            522_0  COME_FROM           392  '392'
              522  END_FINALLY      
              524  JUMP_BACK            66  'to 66'

Parse error at or near `ROT_TWO' instruction at offset 144

    def _retryable_read--- This code section failed: ---

 L.1445         0  LOAD_FAST                'retryable'
                2  JUMP_IF_FALSE_OR_POP    20  'to 20'

 L.1446         4  LOAD_FAST                'self'
                6  LOAD_ATTR                retry_reads

 L.1445         8  JUMP_IF_FALSE_OR_POP    20  'to 20'

 L.1447        10  LOAD_FAST                'session'
               12  JUMP_IF_FALSE_OR_POP    18  'to 18'
               14  LOAD_FAST                'session'
               16  LOAD_ATTR                in_transaction
             18_0  COME_FROM            12  '12'
               18  UNARY_NOT        
             20_0  COME_FROM             8  '8'
             20_1  COME_FROM             2  '2'

 L.1445        20  STORE_FAST               'retryable'

 L.1448        22  LOAD_CONST               None
               24  STORE_FAST               'last_error'

 L.1449        26  LOAD_CONST               False
               28  STORE_FAST               'retrying'

 L.1452        30  SETUP_FINALLY       134  'to 134'

 L.1453        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _select_server

 L.1454        36  LOAD_FAST                'read_pref'

 L.1454        38  LOAD_FAST                'session'

 L.1454        40  LOAD_FAST                'address'

 L.1453        42  LOAD_CONST               ('address',)
               44  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               46  STORE_FAST               'server'

 L.1455        48  LOAD_FAST                'server'
               50  LOAD_ATTR                description
               52  LOAD_ATTR                retryable_reads_supported
               54  POP_JUMP_IF_TRUE     60  'to 60'

 L.1456        56  LOAD_CONST               False
               58  STORE_FAST               'retryable'
             60_0  COME_FROM            54  '54'

 L.1457        60  LOAD_FAST                'self'
               62  LOAD_ATTR                _slaveok_for_server
               64  LOAD_FAST                'read_pref'
               66  LOAD_FAST                'server'
               68  LOAD_FAST                'session'

 L.1458        70  LOAD_FAST                'exhaust'

 L.1457        72  LOAD_CONST               ('exhaust',)
               74  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               76  SETUP_WITH          124  'to 124'

 L.1458        78  UNPACK_SEQUENCE_2     2 
               80  STORE_FAST               'sock_info'

 L.1459        82  STORE_FAST               'slave_ok'

 L.1460        84  LOAD_FAST                'retrying'
               86  POP_JUMP_IF_FALSE    96  'to 96'
               88  LOAD_FAST                'retryable'
               90  POP_JUMP_IF_TRUE     96  'to 96'

 L.1463        92  LOAD_FAST                'last_error'
               94  RAISE_VARARGS_1       1  'exception instance'
             96_0  COME_FROM            90  '90'
             96_1  COME_FROM            86  '86'

 L.1464        96  LOAD_FAST                'func'
               98  LOAD_FAST                'session'
              100  LOAD_FAST                'server'
              102  LOAD_FAST                'sock_info'
              104  LOAD_FAST                'slave_ok'
              106  CALL_FUNCTION_4       4  ''
              108  POP_BLOCK        
              110  ROT_TWO          
              112  BEGIN_FINALLY    
              114  WITH_CLEANUP_START
              116  WITH_CLEANUP_FINISH
              118  POP_FINALLY           0  ''
              120  POP_BLOCK        
              122  RETURN_VALUE     
            124_0  COME_FROM_WITH       76  '76'
              124  WITH_CLEANUP_START
              126  WITH_CLEANUP_FINISH
              128  END_FINALLY      
              130  POP_BLOCK        
              132  JUMP_BACK            30  'to 30'
            134_0  COME_FROM_FINALLY    30  '30'

 L.1465       134  DUP_TOP          
              136  LOAD_GLOBAL              ServerSelectionTimeoutError
              138  COMPARE_OP               exception-match
              140  POP_JUMP_IF_FALSE   162  'to 162'
              142  POP_TOP          
              144  POP_TOP          
              146  POP_TOP          

 L.1466       148  LOAD_FAST                'retrying'
              150  POP_JUMP_IF_FALSE   156  'to 156'

 L.1470       152  LOAD_FAST                'last_error'
              154  RAISE_VARARGS_1       1  'exception instance'
            156_0  COME_FROM           150  '150'

 L.1474       156  RAISE_VARARGS_0       0  'reraise'
              158  POP_EXCEPT       
              160  JUMP_BACK            30  'to 30'
            162_0  COME_FROM           140  '140'

 L.1475       162  DUP_TOP          
              164  LOAD_GLOBAL              ConnectionFailure
              166  COMPARE_OP               exception-match
              168  POP_JUMP_IF_FALSE   212  'to 212'
              170  POP_TOP          
              172  STORE_FAST               'exc'
              174  POP_TOP          
              176  SETUP_FINALLY       200  'to 200'

 L.1476       178  LOAD_FAST                'retryable'
              180  POP_JUMP_IF_FALSE   186  'to 186'
              182  LOAD_FAST                'retrying'
              184  POP_JUMP_IF_FALSE   188  'to 188'
            186_0  COME_FROM           180  '180'

 L.1477       186  RAISE_VARARGS_0       0  'reraise'
            188_0  COME_FROM           184  '184'

 L.1478       188  LOAD_CONST               True
              190  STORE_FAST               'retrying'

 L.1479       192  LOAD_FAST                'exc'
              194  STORE_FAST               'last_error'
              196  POP_BLOCK        
              198  BEGIN_FINALLY    
            200_0  COME_FROM_FINALLY   176  '176'
              200  LOAD_CONST               None
              202  STORE_FAST               'exc'
              204  DELETE_FAST              'exc'
              206  END_FINALLY      
              208  POP_EXCEPT       
              210  JUMP_BACK            30  'to 30'
            212_0  COME_FROM           168  '168'

 L.1480       212  DUP_TOP          
              214  LOAD_GLOBAL              OperationFailure
              216  COMPARE_OP               exception-match
          218_220  POP_JUMP_IF_FALSE   280  'to 280'
              222  POP_TOP          
              224  STORE_FAST               'exc'
              226  POP_TOP          
              228  SETUP_FINALLY       268  'to 268'

 L.1481       230  LOAD_FAST                'retryable'
              232  POP_JUMP_IF_FALSE   238  'to 238'
              234  LOAD_FAST                'retrying'
              236  POP_JUMP_IF_FALSE   240  'to 240'
            238_0  COME_FROM           232  '232'

 L.1482       238  RAISE_VARARGS_0       0  'reraise'
            240_0  COME_FROM           236  '236'

 L.1483       240  LOAD_FAST                'exc'
              242  LOAD_ATTR                code
              244  LOAD_GLOBAL              helpers
              246  LOAD_ATTR                _RETRYABLE_ERROR_CODES
              248  COMPARE_OP               not-in
          250_252  POP_JUMP_IF_FALSE   256  'to 256'

 L.1484       254  RAISE_VARARGS_0       0  'reraise'
            256_0  COME_FROM           250  '250'

 L.1485       256  LOAD_CONST               True
              258  STORE_FAST               'retrying'

 L.1486       260  LOAD_FAST                'exc'
              262  STORE_FAST               'last_error'
              264  POP_BLOCK        
              266  BEGIN_FINALLY    
            268_0  COME_FROM_FINALLY   228  '228'
              268  LOAD_CONST               None
              270  STORE_FAST               'exc'
              272  DELETE_FAST              'exc'
              274  END_FINALLY      
              276  POP_EXCEPT       
              278  JUMP_BACK            30  'to 30'
            280_0  COME_FROM           218  '218'
              280  END_FINALLY      
              282  JUMP_BACK            30  'to 30'

Parse error at or near `ROT_TWO' instruction at offset 110

    def _retryable_write--- This code section failed: ---

 L.1490         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _tmp_session
                4  LOAD_FAST                'session'
                6  CALL_METHOD_1         1  ''
                8  SETUP_WITH           40  'to 40'
               10  STORE_FAST               's'

 L.1491        12  LOAD_FAST                'self'
               14  LOAD_METHOD              _retry_with_session
               16  LOAD_FAST                'retryable'
               18  LOAD_FAST                'func'
               20  LOAD_FAST                's'
               22  LOAD_CONST               None
               24  CALL_METHOD_4         4  ''
               26  POP_BLOCK        
               28  ROT_TWO          
               30  BEGIN_FINALLY    
               32  WITH_CLEANUP_START
               34  WITH_CLEANUP_FINISH
               36  POP_FINALLY           0  ''
               38  RETURN_VALUE     
             40_0  COME_FROM_WITH        8  '8'
               40  WITH_CLEANUP_START
               42  WITH_CLEANUP_FINISH
               44  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 28

    def _reset_server(self, address):
        """Clear our connection pool for a server and mark it Unknown."""
        self._topology.reset_server(address)

    def _reset_server_and_request_check(self, address):
        """Clear our pool for a server, mark it Unknown, and check it soon."""
        self._topology.reset_server_and_request_check(address)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.address == other.address
        return NotImplemented

    def __ne__(self, other):
        return not self == other

    def _repr_helper(self):

        def option_repr(option, value):
            """Fix options whose __repr__ isn't usable in a constructor."""
            if option == 'document_class':
                if value is dict:
                    return 'document_class=dict'
                return 'document_class=%s.%s' % (value.__module__,
                 value.__name__)
            if option in common.TIMEOUT_OPTIONS:
                if value is not None:
                    return '%s=%s' % (option, int(value * 1000))
            return '%s=%r' % (option, value)

        options = [
         'host=%r' % ['%s:%d' % (host, port) if port is not None else host for host, port in self._topology_settings.seeds]]
        options.extend((option_repr(key, self._MongoClient__options._options[key]) for key in self._constructor_args))
        options.extend((option_repr(key, self._MongoClient__options._options[key]) for key in self._MongoClient__options._options if key not in set(self._constructor_args) if key != 'username' if key != 'password'))
        return ', '.join(options)

    def __repr__(self):
        return 'MongoClient(%s)' % (self._repr_helper(),)

    def __getattr__(self, name):
        """Get a database by name.

        Raises :class:`~pymongo.errors.InvalidName` if an invalid
        database name is used.

        :Parameters:
          - `name`: the name of the database to get
        """
        if name.startswith('_'):
            raise AttributeError('MongoClient has no attribute %r. To access the %s database, use client[%r].' % (
             name, name, name))
        return self.__getitem__(name)

    def __getitem__(self, name):
        """Get a database by name.

        Raises :class:`~pymongo.errors.InvalidName` if an invalid
        database name is used.

        :Parameters:
          - `name`: the name of the database to get
        """
        return database.Database(self, name)

    def close_cursor(self, cursor_id, address=None):
        """DEPRECATED - Send a kill cursors message soon with the given id.

        Raises :class:`TypeError` if `cursor_id` is not an instance of
        ``(int, long)``. What closing the cursor actually means
        depends on this client's cursor manager.

        This method may be called from a :class:`~pymongo.cursor.Cursor`
        destructor during garbage collection, so it isn't safe to take a
        lock or do network I/O. Instead, we schedule the cursor to be closed
        soon on a background thread.

        :Parameters:
          - `cursor_id`: id of cursor to close
          - `address` (optional): (host, port) pair of the cursor's server.
            If it is not provided, the client attempts to close the cursor on
            the primary or standalone, or a mongos server.

        .. versionchanged:: 3.7
           Deprecated.

        .. versionchanged:: 3.0
           Added ``address`` parameter.
        """
        warnings.warn('close_cursor is deprecated.',
          DeprecationWarning,
          stacklevel=2)
        if not isinstance(cursor_id, integer_types):
            raise TypeError('cursor_id must be an instance of (int, long)')
        self._close_cursor(cursor_id, address)

    def _close_cursor(self, cursor_id, address):
        """Send a kill cursors message with the given id.

        What closing the cursor actually means depends on this client's
        cursor manager. If there is none, the cursor is closed asynchronously
        on a background thread.
        """
        if self._MongoClient__cursor_manager is not None:
            self._MongoClient__cursor_manager.close(cursor_id, address)
        else:
            self._MongoClient__kill_cursors_queue.append((address, [cursor_id]))

    def _close_cursor_now(self, cursor_id, address=None, session=None):
        """Send a kill cursors message with the given id.

        What closing the cursor actually means depends on this client's
        cursor manager. If there is none, the cursor is closed synchronously
        on the current thread.
        """
        if not isinstance(cursor_id, integer_types):
            raise TypeError('cursor_id must be an instance of (int, long)')
        elif self._MongoClient__cursor_manager is not None:
            self._MongoClient__cursor_manager.close(cursor_id, address)
        else:
            try:
                self._kill_cursors([
                 cursor_id], address, self._get_topology(), session)
            except PyMongoError:
                self._MongoClient__kill_cursors_queue.append((address, [cursor_id]))

    def kill_cursors(self, cursor_ids, address=None):
        """DEPRECATED - Send a kill cursors message soon with the given ids.

        Raises :class:`TypeError` if `cursor_ids` is not an instance of
        ``list``.

        :Parameters:
          - `cursor_ids`: list of cursor ids to kill
          - `address` (optional): (host, port) pair of the cursor's server.
            If it is not provided, the client attempts to close the cursor on
            the primary or standalone, or a mongos server.

        .. versionchanged:: 3.3
           Deprecated.

        .. versionchanged:: 3.0
           Now accepts an `address` argument. Schedules the cursors to be
           closed on a background thread instead of sending the message
           immediately.
        """
        warnings.warn('kill_cursors is deprecated.',
          DeprecationWarning,
          stacklevel=2)
        if not isinstance(cursor_ids, list):
            raise TypeError('cursor_ids must be a list')
        self._MongoClient__kill_cursors_queue.append((address, cursor_ids))

    def _kill_cursors(self, cursor_ids, address, topology, session):
        """Send a kill cursors message with the given ids."""
        listeners = self._event_listeners
        publish = listeners.enabled_for_commands
        if address:
            server = topology.select_server_by_address(tuple(address))
        else:
            server = topology.select_server(writable_server_selector)
        try:
            namespace = address.namespace
            db, coll = namespace.split('.', 1)
        except AttributeError:
            namespace = None
            db = coll = 'OP_KILL_CURSORS'
        else:
            spec = SON([('killCursors', coll), ('cursors', cursor_ids)])
            with server.get_socket(self._MongoClient__all_credentials) as (sock_info):
                if sock_info.max_wire_version >= 4 and namespace is not None:
                    sock_info.command(db, spec, session=session, client=self)
                else:
                    if publish:
                        start = datetime.datetime.now()
                    request_id, msg = message.kill_cursors(cursor_ids)
                    if publish:
                        duration = datetime.datetime.now() - start
                        listeners.publish_command_start(spec, db, request_id, tuple(address))
                        start = datetime.datetime.now()
                try:
                    sock_info.send_message(msg, 0)
                except Exception as exc:
                    try:
                        if publish:
                            dur = datetime.datetime.now() - start + duration
                            listeners.publish_command_failure(dur, message._convert_exception(exc), 'killCursors', request_id, tuple(address))
                        raise
                    finally:
                        exc = None
                        del exc

                else:
                    if publish:
                        duration = datetime.datetime.now() - start + duration
                        reply = {'cursorsUnknown':cursor_ids, 
                         'ok':1}
                        listeners.publish_command_success(duration, reply, 'killCursors', request_id, tuple(address))

    def _process_kill_cursors(self):
        """Process any pending kill cursors requests."""
        address_to_cursor_ids = defaultdict(list)
        while True:
            try:
                address, cursor_ids = self._MongoClient__kill_cursors_queue.pop()
            except IndexError:
                break
            else:
                address_to_cursor_ids[address].extend(cursor_ids)

        if address_to_cursor_ids:
            topology = self._get_topology()
            for address, cursor_ids in address_to_cursor_ids.items():
                try:
                    self._kill_cursors(cursor_ids,
                      address, topology, session=None)
                except Exception:
                    helpers._handle_exception()

    def _process_periodic_tasks(self):
        """Process any pending kill cursors requests and
        maintain connection pool parameters."""
        self._process_kill_cursors()
        try:
            self._topology.update_pool()
        except Exception:
            helpers._handle_exception()

    def __start_session(self, implicit, **kwargs):
        authset = set(self._MongoClient__all_credentials.values())
        if len(authset) > 1:
            raise InvalidOperation('Cannot call start_session when multiple users are authenticated')
        server_session = self._get_server_session()
        opts = (client_session.SessionOptions)(**kwargs)
        return client_session.ClientSession(self, server_session, opts, authset, implicit)

    def start_session(self, causal_consistency=True, default_transaction_options=None):
        """Start a logical session.

        This method takes the same parameters as
        :class:`~pymongo.client_session.SessionOptions`. See the
        :mod:`~pymongo.client_session` module for details and examples.

        Requires MongoDB 3.6. It is an error to call :meth:`start_session`
        if this client has been authenticated to multiple databases using the
        deprecated method :meth:`~pymongo.database.Database.authenticate`.

        A :class:`~pymongo.client_session.ClientSession` may only be used with
        the MongoClient that started it.

        :Returns:
          An instance of :class:`~pymongo.client_session.ClientSession`.

        .. versionadded:: 3.6
        """
        return self._MongoClient__start_session(False,
          causal_consistency=causal_consistency,
          default_transaction_options=default_transaction_options)

    def _get_server_session(self):
        """Internal: start or resume a _ServerSession."""
        return self._topology.get_server_session()

    def _return_server_session(self, server_session, lock):
        """Internal: return a _ServerSession to the pool."""
        return self._topology.return_server_session(server_session, lock)

    def _ensure_session--- This code section failed: ---

 L.1804         0  LOAD_FAST                'session'
                2  POP_JUMP_IF_FALSE     8  'to 8'

 L.1805         4  LOAD_FAST                'session'
                6  RETURN_VALUE     
              8_0  COME_FROM             2  '2'

 L.1807         8  SETUP_FINALLY        26  'to 26'

 L.1810        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _MongoClient__start_session
               14  LOAD_CONST               True
               16  LOAD_CONST               False
               18  LOAD_CONST               ('causal_consistency',)
               20  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               22  POP_BLOCK        
               24  RETURN_VALUE     
             26_0  COME_FROM_FINALLY     8  '8'

 L.1811        26  DUP_TOP          
               28  LOAD_GLOBAL              ConfigurationError
               30  LOAD_GLOBAL              InvalidOperation
               32  BUILD_TUPLE_2         2 
               34  COMPARE_OP               exception-match
               36  POP_JUMP_IF_FALSE    50  'to 50'
               38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          

 L.1813        44  POP_EXCEPT       
               46  LOAD_CONST               None
               48  RETURN_VALUE     
             50_0  COME_FROM            36  '36'
               50  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 40

    @contextlib.contextmanager
    def _tmp_session(self, session, close=True):
        """If provided session is None, lend a temporary session."""
        if session:
            (yield session)
            return
        s = self._ensure_session(session)
        if s and close:
            with s:
                (yield s)
        else:
            if s:
                try:
                    (yield s)
                except Exception:
                    s.end_session()
                    raise

            else:
                (yield)

    def _send_cluster_time(self, command, session):
        topology_time = self._topology.max_cluster_time()
        session_time = session.cluster_time if session else None
        if topology_time:
            if session_time:
                if topology_time['clusterTime'] > session_time['clusterTime']:
                    cluster_time = topology_time
            else:
                cluster_time = session_time
        else:
            cluster_time = topology_time or session_time
        if cluster_time:
            command['$clusterTime'] = cluster_time

    def _process_response(self, reply, session):
        self._topology.receive_cluster_time(reply.get('$clusterTime'))
        if session is not None:
            session._process_response(reply)

    def server_info(self, session=None):
        """Get information about the MongoDB server we're connected to.

        :Parameters:
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.

        .. versionchanged:: 3.6
           Added ``session`` parameter.
        """
        return self.admin.command('buildinfo', read_preference=(ReadPreference.PRIMARY),
          session=session)

    def list_databases(self, session=None, **kwargs):
        """Get a cursor over the databases of the connected server.

        :Parameters:
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.
          - `**kwargs` (optional): Optional parameters of the
            `listDatabases command
            <https://docs.mongodb.com/manual/reference/command/listDatabases/>`_
            can be passed as keyword arguments to this method. The supported
            options differ by server version.

        :Returns:
          An instance of :class:`~pymongo.command_cursor.CommandCursor`.

        .. versionadded:: 3.6
        """
        cmd = SON([('listDatabases', 1)])
        cmd.update(kwargs)
        admin = self._database_default_options('admin')
        res = admin._retryable_read_command(cmd, session=session)
        cursor = {'id':0, 
         'firstBatch':res['databases'], 
         'ns':'admin.$cmd'}
        return CommandCursor(admin['$cmd'], cursor, None)

    def list_database_names(self, session=None):
        """Get a list of the names of all databases on the connected server.

        :Parameters:
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.

        .. versionadded:: 3.6
        """
        return [doc['name'] for doc in self.list_databases(session, nameOnly=True)]

    def database_names(self, session=None):
        """**DEPRECATED**: Get a list of the names of all databases on the
        connected server.

        :Parameters:
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.

        .. versionchanged:: 3.7
           Deprecated. Use :meth:`list_database_names` instead.

        .. versionchanged:: 3.6
           Added ``session`` parameter.
        """
        warnings.warn('database_names is deprecated. Use list_database_names instead.', DeprecationWarning,
          stacklevel=2)
        return self.list_database_names(session)

    def drop_database(self, name_or_database, session=None):
        """Drop a database.

        Raises :class:`TypeError` if `name_or_database` is not an instance of
        :class:`basestring` (:class:`str` in python 3) or
        :class:`~pymongo.database.Database`.

        :Parameters:
          - `name_or_database`: the name of a database to drop, or a
            :class:`~pymongo.database.Database` instance representing the
            database to drop
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.

        .. versionchanged:: 3.6
           Added ``session`` parameter.

        .. note:: The :attr:`~pymongo.mongo_client.MongoClient.write_concern` of
           this client is automatically applied to this operation when using
           MongoDB >= 3.4.

        .. versionchanged:: 3.4
           Apply this client's write concern automatically to this operation
           when connected to MongoDB >= 3.4.

        """
        name = name_or_database
        if isinstance(name, database.Database):
            name = name.name
        if not isinstance(name, string_type):
            raise TypeError('name_or_database must be an instance of %s or a Database' % (
             string_type.__name__,))
        self._purge_index(name)
        with self._socket_for_writes(session) as (sock_info):
            self[name]._command(sock_info,
              'dropDatabase',
              read_preference=(ReadPreference.PRIMARY),
              write_concern=(self._write_concern_for(session)),
              parse_write_concern_error=True,
              session=session)

    def get_default_database(self, default=None, codec_options=None, read_preference=None, write_concern=None, read_concern=None):
        """Get the database named in the MongoDB connection URI.

        >>> uri = 'mongodb://host/my_database'
        >>> client = MongoClient(uri)
        >>> db = client.get_default_database()
        >>> assert db.name == 'my_database'
        >>> db = client.get_database()
        >>> assert db.name == 'my_database'

        Useful in scripts where you want to choose which database to use
        based only on the URI in a configuration file.

        :Parameters:
          - `default` (optional): the database name to use if no database name
            was provided in the URI.
          - `codec_options` (optional): An instance of
            :class:`~bson.codec_options.CodecOptions`. If ``None`` (the
            default) the :attr:`codec_options` of this :class:`MongoClient` is
            used.
          - `read_preference` (optional): The read preference to use. If
            ``None`` (the default) the :attr:`read_preference` of this
            :class:`MongoClient` is used. See :mod:`~pymongo.read_preferences`
            for options.
          - `write_concern` (optional): An instance of
            :class:`~pymongo.write_concern.WriteConcern`. If ``None`` (the
            default) the :attr:`write_concern` of this :class:`MongoClient` is
            used.
          - `read_concern` (optional): An instance of
            :class:`~pymongo.read_concern.ReadConcern`. If ``None`` (the
            default) the :attr:`read_concern` of this :class:`MongoClient` is
            used.

        .. versionchanged:: 3.8
           Undeprecated. Added the ``default``, ``codec_options``,
           ``read_preference``, ``write_concern`` and ``read_concern``
           parameters.

        .. versionchanged:: 3.5
           Deprecated, use :meth:`get_database` instead.
        """
        if self._MongoClient__default_database_name is None:
            if default is None:
                raise ConfigurationError('No default database name defined or provided.')
        return database.Databaseself(self._MongoClient__default_database_name or default)codec_optionsread_preferencewrite_concernread_concern

    def get_database(self, name=None, codec_options=None, read_preference=None, write_concern=None, read_concern=None):
        """Get a :class:`~pymongo.database.Database` with the given name and
        options.

        Useful for creating a :class:`~pymongo.database.Database` with
        different codec options, read preference, and/or write concern from
        this :class:`MongoClient`.

          >>> client.read_preference
          Primary()
          >>> db1 = client.test
          >>> db1.read_preference
          Primary()
          >>> from pymongo import ReadPreference
          >>> db2 = client.get_database(
          ...     'test', read_preference=ReadPreference.SECONDARY)
          >>> db2.read_preference
          Secondary(tag_sets=None)

        :Parameters:
          - `name` (optional): The name of the database - a string. If ``None``
            (the default) the database named in the MongoDB connection URI is
            returned.
          - `codec_options` (optional): An instance of
            :class:`~bson.codec_options.CodecOptions`. If ``None`` (the
            default) the :attr:`codec_options` of this :class:`MongoClient` is
            used.
          - `read_preference` (optional): The read preference to use. If
            ``None`` (the default) the :attr:`read_preference` of this
            :class:`MongoClient` is used. See :mod:`~pymongo.read_preferences`
            for options.
          - `write_concern` (optional): An instance of
            :class:`~pymongo.write_concern.WriteConcern`. If ``None`` (the
            default) the :attr:`write_concern` of this :class:`MongoClient` is
            used.
          - `read_concern` (optional): An instance of
            :class:`~pymongo.read_concern.ReadConcern`. If ``None`` (the
            default) the :attr:`read_concern` of this :class:`MongoClient` is
            used.

        .. versionchanged:: 3.5
           The `name` parameter is now optional, defaulting to the database
           named in the MongoDB connection URI.
        """
        if name is None:
            if self._MongoClient__default_database_name is None:
                raise ConfigurationError('No default database defined')
            name = self._MongoClient__default_database_name
        return database.Databaseselfnamecodec_optionsread_preferencewrite_concernread_concern

    def _database_default_options(self, name):
        """Get a Database instance with the default settings."""
        return self.get_database(name,
          codec_options=DEFAULT_CODEC_OPTIONS, read_preference=(ReadPreference.PRIMARY),
          write_concern=DEFAULT_WRITE_CONCERN)

    @property
    def is_locked(self):
        """Is this server locked? While locked, all write operations
        are blocked, although read operations may still be allowed.
        Use :meth:`unlock` to unlock.
        """
        ops = self._database_default_options('admin')._current_op()
        return bool(ops.get('fsyncLock', 0))

    def fsync(self, **kwargs):
        """Flush all pending writes to datafiles.

        Optional parameters can be passed as keyword arguments:
          - `lock`: If True lock the server to disallow writes.
          - `async`: If True don't block while synchronizing.
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.

        .. note:: Starting with Python 3.7 `async` is a reserved keyword.
          The async option to the fsync command can be passed using a
          dictionary instead::

            options = {'async': True}
            client.fsync(**options)

        .. versionchanged:: 3.6
           Added ``session`` parameter.

        .. warning:: `async` and `lock` can not be used together.

        .. warning:: MongoDB does not support the `async` option
                     on Windows and will raise an exception on that
                     platform.
        """
        (self.admin.command)('fsync', read_preference=ReadPreference.PRIMARY, **kwargs)

    def unlock(self, session=None):
        """Unlock a previously locked server.

        :Parameters:
          - `session` (optional): a
            :class:`~pymongo.client_session.ClientSession`.

        .. versionchanged:: 3.6
           Added ``session`` parameter.
        """
        cmd = SON([('fsyncUnlock', 1)])
        with self._socket_for_writes(session) as (sock_info):
            if sock_info.max_wire_version >= 4:
                try:
                    with self._tmp_session(session) as (s):
                        sock_info.command('admin',
                          cmd, session=s, client=self)
                except OperationFailure as exc:
                    try:
                        if exc.code != 125:
                            raise
                    finally:
                        exc = None
                        del exc

            else:
                message._first_batch(sock_info, 'admin', '$cmd.sys.unlock', {}, -1, True, self.codec_options, ReadPreference.PRIMARY, cmd, self._event_listeners)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __iter__(self):
        return self

    def __next__(self):
        raise TypeError("'MongoClient' object is not iterable")

    next = __next__


class _MongoClientErrorHandler(object):
    __doc__ = 'Error handler for MongoClient.'
    __slots__ = ('_client', '_server_address', '_session', '_max_wire_version')

    def __init__(self, client, server_address, session):
        self._client = client
        self._server_address = server_address
        self._session = session
        self._max_wire_version = None

    def contribute_socket(self, sock_info):
        """Provide socket information to the error handler."""
        self._max_wire_version = sock_info.max_wire_version

    def __enter__(self):
        return self

    def __exit__--- This code section failed: ---

 L.2182         0  LOAD_FAST                'exc_type'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L.2183         8  LOAD_CONST               None
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L.2185        12  LOAD_GLOBAL              issubclass
               14  LOAD_FAST                'exc_type'
               16  LOAD_GLOBAL              PyMongoError
               18  CALL_FUNCTION_2       2  ''
               20  POP_JUMP_IF_FALSE    48  'to 48'

 L.2186        22  LOAD_FAST                'self'
               24  LOAD_ATTR                _session
               26  POP_JUMP_IF_FALSE    48  'to 48'
               28  LOAD_FAST                'exc_val'
               30  LOAD_METHOD              has_error_label

 L.2187        32  LOAD_STR                 'TransientTransactionError'

 L.2186        34  CALL_METHOD_1         1  ''
               36  POP_JUMP_IF_FALSE    48  'to 48'

 L.2188        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _session
               42  LOAD_METHOD              _unpin_mongos
               44  CALL_METHOD_0         0  ''
               46  POP_TOP          
             48_0  COME_FROM            36  '36'
             48_1  COME_FROM            26  '26'
             48_2  COME_FROM            20  '20'

 L.2190        48  LOAD_GLOBAL              issubclass
               50  LOAD_FAST                'exc_type'
               52  LOAD_GLOBAL              NetworkTimeout
               54  CALL_FUNCTION_2       2  ''
               56  POP_JUMP_IF_FALSE    78  'to 78'

 L.2195        58  LOAD_FAST                'self'
               60  LOAD_ATTR                _session
               62  POP_JUMP_IF_FALSE   250  'to 250'

 L.2196        64  LOAD_FAST                'self'
               66  LOAD_ATTR                _session
               68  LOAD_ATTR                _server_session
               70  LOAD_METHOD              mark_dirty
               72  CALL_METHOD_0         0  ''
               74  POP_TOP          
               76  JUMP_FORWARD        250  'to 250'
             78_0  COME_FROM            56  '56'

 L.2197        78  LOAD_GLOBAL              issubclass
               80  LOAD_FAST                'exc_type'
               82  LOAD_GLOBAL              NotMasterError
               84  CALL_FUNCTION_2       2  ''
               86  POP_JUMP_IF_FALSE   170  'to 170'

 L.2206        88  LOAD_FAST                'exc_val'
               90  LOAD_ATTR                details
               92  LOAD_METHOD              get
               94  LOAD_STR                 'code'
               96  LOAD_CONST               -1
               98  CALL_METHOD_2         2  ''
              100  STORE_FAST               'err_code'

 L.2207       102  LOAD_FAST                'err_code'
              104  LOAD_GLOBAL              helpers
              106  LOAD_ATTR                _SHUTDOWN_CODES
              108  COMPARE_OP               in
              110  STORE_FAST               'is_shutting_down'

 L.2208       112  LOAD_FAST                'is_shutting_down'
              114  POP_JUMP_IF_TRUE    136  'to 136'
              116  LOAD_FAST                'self'
              118  LOAD_ATTR                _max_wire_version
              120  LOAD_CONST               None
              122  COMPARE_OP               is
              124  POP_JUMP_IF_TRUE    136  'to 136'

 L.2209       126  LOAD_FAST                'self'
              128  LOAD_ATTR                _max_wire_version
              130  LOAD_CONST               7
              132  COMPARE_OP               <=

 L.2208       134  POP_JUMP_IF_FALSE   152  'to 152'
            136_0  COME_FROM           124  '124'
            136_1  COME_FROM           114  '114'

 L.2211       136  LOAD_FAST                'self'
              138  LOAD_ATTR                _client
              140  LOAD_METHOD              _reset_server_and_request_check

 L.2212       142  LOAD_FAST                'self'
              144  LOAD_ATTR                _server_address

 L.2211       146  CALL_METHOD_1         1  ''
              148  POP_TOP          
              150  JUMP_ABSOLUTE       250  'to 250'
            152_0  COME_FROM           134  '134'

 L.2214       152  LOAD_FAST                'self'
              154  LOAD_ATTR                _client
              156  LOAD_ATTR                _topology
              158  LOAD_METHOD              mark_server_unknown_and_request_check

 L.2215       160  LOAD_FAST                'self'
              162  LOAD_ATTR                _server_address

 L.2214       164  CALL_METHOD_1         1  ''
              166  POP_TOP          
              168  JUMP_FORWARD        250  'to 250'
            170_0  COME_FROM            86  '86'

 L.2216       170  LOAD_GLOBAL              issubclass
              172  LOAD_FAST                'exc_type'
              174  LOAD_GLOBAL              ConnectionFailure
              176  CALL_FUNCTION_2       2  ''
              178  POP_JUMP_IF_FALSE   214  'to 214'

 L.2219       180  LOAD_FAST                'self'
              182  LOAD_ATTR                _client
              184  LOAD_METHOD              _reset_server
              186  LOAD_FAST                'self'
              188  LOAD_ATTR                _server_address
              190  CALL_METHOD_1         1  ''
              192  POP_TOP          

 L.2220       194  LOAD_FAST                'self'
              196  LOAD_ATTR                _session
              198  POP_JUMP_IF_FALSE   250  'to 250'

 L.2221       200  LOAD_FAST                'self'
              202  LOAD_ATTR                _session
              204  LOAD_ATTR                _server_session
              206  LOAD_METHOD              mark_dirty
              208  CALL_METHOD_0         0  ''
              210  POP_TOP          
              212  JUMP_FORWARD        250  'to 250'
            214_0  COME_FROM           178  '178'

 L.2222       214  LOAD_GLOBAL              issubclass
              216  LOAD_FAST                'exc_type'
              218  LOAD_GLOBAL              OperationFailure
              220  CALL_FUNCTION_2       2  ''
              222  POP_JUMP_IF_FALSE   250  'to 250'

 L.2225       224  LOAD_FAST                'exc_val'
              226  LOAD_ATTR                code
              228  LOAD_GLOBAL              helpers
              230  LOAD_ATTR                _RETRYABLE_ERROR_CODES
              232  COMPARE_OP               in
              234  POP_JUMP_IF_FALSE   250  'to 250'

 L.2226       236  LOAD_FAST                'self'
              238  LOAD_ATTR                _client
              240  LOAD_METHOD              _reset_server
              242  LOAD_FAST                'self'
              244  LOAD_ATTR                _server_address
              246  CALL_METHOD_1         1  ''
              248  POP_TOP          
            250_0  COME_FROM           234  '234'
            250_1  COME_FROM           222  '222'
            250_2  COME_FROM           212  '212'
            250_3  COME_FROM           198  '198'
            250_4  COME_FROM           168  '168'
            250_5  COME_FROM            76  '76'
            250_6  COME_FROM            62  '62'

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 150