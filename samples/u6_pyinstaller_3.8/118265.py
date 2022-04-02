# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pymongo\common.py
"""Functions and classes common to multiple pymongo modules."""
import datetime, warnings
from bson import SON
from bson.binary import STANDARD, PYTHON_LEGACY, JAVA_LEGACY, CSHARP_LEGACY
from bson.codec_options import CodecOptions, TypeRegistry
from bson.py3compat import abc, integer_types, iteritems, string_type
from bson.raw_bson import RawBSONDocument
from pymongo.auth import MECHANISMS
from pymongo.compression_support import validate_compressors, validate_zlib_compression_level
from pymongo.driver_info import DriverInfo
from pymongo.encryption_options import validate_auto_encryption_opts_or_none
from pymongo.errors import ConfigurationError
from pymongo.monitoring import _validate_event_listeners
from pymongo.read_concern import ReadConcern
from pymongo.read_preferences import _MONGOS_MODES, _ServerMode
from pymongo.ssl_support import validate_cert_reqs, validate_allow_invalid_certs
from pymongo.write_concern import DEFAULT_WRITE_CONCERN, WriteConcern
try:
    from collections import OrderedDict
    ORDERED_TYPES = (
     SON, OrderedDict)
except ImportError:
    ORDERED_TYPES = (
     SON,)
else:
    MAX_BSON_SIZE = 16777216
    MAX_MESSAGE_SIZE = 2 * MAX_BSON_SIZE
    MIN_WIRE_VERSION = 0
    MAX_WIRE_VERSION = 0
    MAX_WRITE_BATCH_SIZE = 1000
    MIN_SUPPORTED_SERVER_VERSION = '2.6'
    MIN_SUPPORTED_WIRE_VERSION = 2
    MAX_SUPPORTED_WIRE_VERSION = 8
    HEARTBEAT_FREQUENCY = 10
    KILL_CURSOR_FREQUENCY = 1
    EVENTS_QUEUE_FREQUENCY = 1
    SERVER_SELECTION_TIMEOUT = 30
    MIN_HEARTBEAT_INTERVAL = 0.5
    MIN_SRV_RESCAN_INTERVAL = 60
    CONNECT_TIMEOUT = 20.0
    MAX_POOL_SIZE = 100
    MIN_POOL_SIZE = 0
    MAX_IDLE_TIME_MS = None
    MAX_IDLE_TIME_SEC = None
    WAIT_QUEUE_TIMEOUT = None
    LOCAL_THRESHOLD_MS = 15
    RETRY_WRITES = True
    RETRY_READS = True
    COMMAND_NOT_FOUND_CODES = (59, )
    UNAUTHORIZED_CODES = (13, 16547, 16548)
    _MAX_END_SESSIONS = 10000

    def partition_node(node):
        """Split a host:port string into (host, int(port)) pair."""
        host = node
        port = 27017
        idx = node.rfind(':')
        if idx != -1:
            host, port = node[:idx], int(node[idx + 1:])
        if host.startswith('['):
            host = host[1:-1]
        return (
         host, port)


    def clean_node(node):
        """Split and normalize a node name from an ismaster response."""
        host, port = partition_node(node)
        return (
         host.lower(), port)


    def raise_config_error(key, dummy):
        """Raise ConfigurationError with the given key name."""
        raise ConfigurationError('Unknown option %s' % (key,))


    _UUID_REPRESENTATIONS = {'standard':STANDARD, 
     'pythonLegacy':PYTHON_LEGACY, 
     'javaLegacy':JAVA_LEGACY, 
     'csharpLegacy':CSHARP_LEGACY}

    def validate_boolean(option, value):
        """Validates that 'value' is True or False."""
        if isinstance(value, bool):
            return value
        raise TypeError('%s must be True or False' % (option,))


    def validate_boolean_or_string(option, value):
        """Validates that value is True, False, 'true', or 'false'."""
        if isinstance(value, string_type):
            if value not in ('true', 'false'):
                raise ValueError("The value of %s must be 'true' or 'false'" % (
                 option,))
            return value == 'true'
        return validate_boolean(option, value)


    def validate_integer--- This code section failed: ---

 L. 175         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'value'
                4  LOAD_GLOBAL              integer_types
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 176        10  LOAD_FAST                'value'
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 177        14  LOAD_GLOBAL              isinstance
               16  LOAD_FAST                'value'
               18  LOAD_GLOBAL              string_type
               20  CALL_FUNCTION_2       2  ''
               22  POP_JUMP_IF_FALSE    70  'to 70'

 L. 178        24  SETUP_FINALLY        36  'to 36'

 L. 179        26  LOAD_GLOBAL              int
               28  LOAD_FAST                'value'
               30  CALL_FUNCTION_1       1  ''
               32  POP_BLOCK        
               34  RETURN_VALUE     
             36_0  COME_FROM_FINALLY    24  '24'

 L. 180        36  DUP_TOP          
               38  LOAD_GLOBAL              ValueError
               40  COMPARE_OP               exception-match
               42  POP_JUMP_IF_FALSE    68  'to 68'
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L. 181        50  LOAD_GLOBAL              ValueError
               52  LOAD_STR                 'The value of %s must be an integer'

 L. 182        54  LOAD_FAST                'option'
               56  BUILD_TUPLE_1         1 

 L. 181        58  BINARY_MODULO    
               60  CALL_FUNCTION_1       1  ''
               62  RAISE_VARARGS_1       1  'exception instance'
               64  POP_EXCEPT       
               66  JUMP_FORWARD         70  'to 70'
             68_0  COME_FROM            42  '42'
               68  END_FINALLY      
             70_0  COME_FROM            66  '66'
             70_1  COME_FROM            22  '22'

 L. 183        70  LOAD_GLOBAL              TypeError
               72  LOAD_STR                 'Wrong type for %s, value must be an integer'
               74  LOAD_FAST                'option'
               76  BUILD_TUPLE_1         1 
               78  BINARY_MODULO    
               80  CALL_FUNCTION_1       1  ''
               82  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `POP_TOP' instruction at offset 46


    def validate_positive_integer(option, value):
        """Validate that 'value' is a positive integer, which does not include 0.
    """
        val = validate_integer(option, value)
        if val <= 0:
            raise ValueError('The value of %s must be a positive integer' % (
             option,))
        return val


    def validate_non_negative_integer(option, value):
        """Validate that 'value' is a positive integer or 0.
    """
        val = validate_integer(option, value)
        if val < 0:
            raise ValueError('The value of %s must be a non negative integer' % (
             option,))
        return val


    def validate_readable(option, value):
        """Validates that 'value' is file-like and readable.
    """
        if value is None:
            return value
        value = validate_string(option, value)
        open(value, 'r').close()
        return value


    def validate_positive_integer_or_none(option, value):
        """Validate that 'value' is a positive integer or None.
    """
        if value is None:
            return value
        return validate_positive_integer(option, value)


    def validate_non_negative_integer_or_none(option, value):
        """Validate that 'value' is a positive integer or 0 or None.
    """
        if value is None:
            return value
        return validate_non_negative_integer(option, value)


    def validate_string(option, value):
        """Validates that 'value' is an instance of `basestring` for Python 2
    or `str` for Python 3.
    """
        if isinstance(value, string_type):
            return value
        raise TypeError('Wrong type for %s, value must be an instance of %s' % (
         option, string_type.__name__))


    def validate_string_or_none(option, value):
        """Validates that 'value' is an instance of `basestring` or `None`.
    """
        if value is None:
            return value
        return validate_string(option, value)


    def validate_int_or_basestring--- This code section failed: ---

 L. 255         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'value'
                4  LOAD_GLOBAL              integer_types
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 256        10  LOAD_FAST                'value'
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 257        14  LOAD_GLOBAL              isinstance
               16  LOAD_FAST                'value'
               18  LOAD_GLOBAL              string_type
               20  CALL_FUNCTION_2       2  ''
               22  POP_JUMP_IF_FALSE    60  'to 60'

 L. 258        24  SETUP_FINALLY        36  'to 36'

 L. 259        26  LOAD_GLOBAL              int
               28  LOAD_FAST                'value'
               30  CALL_FUNCTION_1       1  ''
               32  POP_BLOCK        
               34  RETURN_VALUE     
             36_0  COME_FROM_FINALLY    24  '24'

 L. 260        36  DUP_TOP          
               38  LOAD_GLOBAL              ValueError
               40  COMPARE_OP               exception-match
               42  POP_JUMP_IF_FALSE    58  'to 58'
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L. 261        50  LOAD_FAST                'value'
               52  ROT_FOUR         
               54  POP_EXCEPT       
               56  RETURN_VALUE     
             58_0  COME_FROM            42  '42'
               58  END_FINALLY      
             60_0  COME_FROM            22  '22'

 L. 262        60  LOAD_GLOBAL              TypeError
               62  LOAD_STR                 'Wrong type for %s, value must be an integer or a string'

 L. 263        64  LOAD_FAST                'option'
               66  BUILD_TUPLE_1         1 

 L. 262        68  BINARY_MODULO    
               70  CALL_FUNCTION_1       1  ''
               72  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `POP_TOP' instruction at offset 46


    def validate_non_negative_int_or_basestring(option, value):
        """Validates that 'value' is an integer or string.
    """
        if isinstance(value, integer_types):
            return value
        if isinstance(value, string_type):
            try:
                val = int(value)
            except ValueError:
                return value
            else:
                return validate_non_negative_integer(option, val)
        raise TypeError('Wrong type for %s, value must be an non negative integer or a string' % (
         option,))


    def validate_positive_float(option, value):
        """Validates that 'value' is a float, or can be converted to one, and is
       positive.
    """
        errmsg = '%s must be an integer or float' % (option,)
        try:
            value = float(value)
        except ValueError:
            raise ValueError(errmsg)
        except TypeError:
            raise TypeError(errmsg)
        else:
            if not 0 < value < 1000000000.0:
                raise ValueError('%s must be greater than 0 and less than one billion' % (
                 option,))
            return value


    def validate_positive_float_or_zero(option, value):
        """Validates that 'value' is 0 or a positive float, or can be converted to
    0 or a positive float.
    """
        if value == 0 or value == '0':
            return 0
        return validate_positive_float(option, value)


    def validate_timeout_or_none(option, value):
        """Validates a timeout specified in milliseconds returning
    a value in floating point seconds.
    """
        if value is None:
            return value
        return validate_positive_float(option, value) / 1000.0


    def validate_timeout_or_zero(option, value):
        """Validates a timeout specified in milliseconds returning
    a value in floating point seconds for the case where None is an error
    and 0 is valid. Setting the timeout to nothing in the URI string is a
    config error.
    """
        if value is None:
            raise ConfigurationError('%s cannot be None' % (option,))
        if value == 0 or value == '0':
            return 0
        return validate_positive_float(option, value) / 1000.0


    def validate_max_staleness(option, value):
        """Validates maxStalenessSeconds according to the Max Staleness Spec."""
        if value == -1 or value == '-1':
            return -1
        return validate_positive_integer(option, value)


    def validate_read_preference(dummy, value):
        """Validate a read preference.
    """
        if not isinstance(value, _ServerMode):
            raise TypeError('%r is not a read preference.' % (value,))
        return value


    def validate_read_preference_mode(dummy, value):
        """Validate read preference mode for a MongoReplicaSetClient.

    .. versionchanged:: 3.5
       Returns the original ``value`` instead of the validated read preference
       mode.
    """
        if value not in _MONGOS_MODES:
            raise ValueError('%s is not a valid read preference' % (value,))
        return value


    def validate_auth_mechanism(option, value):
        """Validate the authMechanism URI option.
    """
        if value not in MECHANISMS:
            if value != 'CRAM-MD5':
                raise ValueError('%s must be in %s' % (option, tuple(MECHANISMS)))
        return value


    def validate_uuid_representation--- This code section failed: ---

 L. 374         0  SETUP_FINALLY        12  'to 12'

 L. 375         2  LOAD_GLOBAL              _UUID_REPRESENTATIONS
                4  LOAD_FAST                'value'
                6  BINARY_SUBSCR    
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L. 376        12  DUP_TOP          
               14  LOAD_GLOBAL              KeyError
               16  COMPARE_OP               exception-match
               18  POP_JUMP_IF_FALSE    50  'to 50'
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L. 377        26  LOAD_GLOBAL              ValueError
               28  LOAD_STR                 '%s is an invalid UUID representation. Must be one of %s'

 L. 379        30  LOAD_FAST                'value'
               32  LOAD_GLOBAL              tuple
               34  LOAD_GLOBAL              _UUID_REPRESENTATIONS
               36  CALL_FUNCTION_1       1  ''
               38  BUILD_TUPLE_2         2 

 L. 377        40  BINARY_MODULO    
               42  CALL_FUNCTION_1       1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
               46  POP_EXCEPT       
               48  JUMP_FORWARD         52  'to 52'
             50_0  COME_FROM            18  '18'
               50  END_FINALLY      
             52_0  COME_FROM            48  '48'

Parse error at or near `POP_TOP' instruction at offset 22


    def validate_read_preference_tags(name, value):
        """Parse readPreferenceTags if passed as a client kwarg.
    """
        if not isinstance(value, list):
            value = [
             value]
        tag_sets = []
        for tag_set in value:
            if tag_set == '':
                tag_sets.append({})
            else:
                try:
                    tag_sets.append(dict([tag.split(':') for tag in tag_set.split(',')]))
                except Exception:
                    raise ValueError('%r not a valid value for %s' % (
                     tag_set, name))

        else:
            return tag_sets


    _MECHANISM_PROPS = frozenset(['SERVICE_NAME',
     'CANONICALIZE_HOST_NAME',
     'SERVICE_REALM'])

    def validate_auth_mechanism_properties(option, value):
        """Validate authMechanismProperties."""
        value = validate_string(option, value)
        props = {}
        for opt in value.split(','):
            try:
                key, val = opt.split(':')
            except ValueError:
                raise ValueError('auth mechanism properties must be key:value pairs like SERVICE_NAME:mongodb, not %s.' % (
                 opt,))
            else:
                if key not in _MECHANISM_PROPS:
                    raise ValueError('%s is not a supported auth mechanism property. Must be one of %s.' % (
                     key, tuple(_MECHANISM_PROPS)))
                if key == 'CANONICALIZE_HOST_NAME':
                    props[key] = validate_boolean_or_string(key, val)
                else:
                    props[key] = val
        else:
            return props


    def validate_document_class(option, value):
        """Validate the document_class option."""
        if not issubclass(value, (abc.MutableMapping, RawBSONDocument)):
            raise TypeError('%s must be dict, bson.son.SON, bson.raw_bson.RawBSONDocument, or a sublass of collections.MutableMapping' % (
             option,))
        return value


    def validate_type_registry(option, value):
        """Validate the type_registry option."""
        if value is not None:
            if not isinstance(value, TypeRegistry):
                raise TypeError('%s must be an instance of %s' % (
                 option, TypeRegistry))
        return value


    def validate_list(option, value):
        """Validates that 'value' is a list."""
        if not isinstance(value, list):
            raise TypeError('%s must be a list' % (option,))
        return value


    def validate_list_or_none(option, value):
        """Validates that 'value' is a list or None."""
        if value is None:
            return value
        return validate_list(option, value)


    def validate_list_or_mapping(option, value):
        """Validates that 'value' is a list or a document."""
        if not isinstance(value, (abc.Mapping, list)):
            raise TypeError('%s must either be a list or an instance of dict, bson.son.SON, or any other type that inherits from collections.Mapping' % (
             option,))


    def validate_is_mapping(option, value):
        """Validate the type of method arguments that expect a document."""
        if not isinstance(value, abc.Mapping):
            raise TypeError('%s must be an instance of dict, bson.son.SON, or any other type that inherits from collections.Mapping' % (
             option,))


    def validate_is_document_type(option, value):
        """Validate the type of method arguments that expect a MongoDB document."""
        if not isinstance(value, (abc.MutableMapping, RawBSONDocument)):
            raise TypeError('%s must be an instance of dict, bson.son.SON, bson.raw_bson.RawBSONDocument, or a type that inherits from collections.MutableMapping' % (
             option,))


    def validate_appname_or_none(option, value):
        """Validate the appname option."""
        if value is None:
            return value
        validate_string(option, value)
        if len(value.encode('utf-8')) > 128:
            raise ValueError('%s must be <= 128 bytes' % (option,))
        return value


    def validate_driver_or_none(option, value):
        """Validate the driver keyword arg."""
        if value is None:
            return value
        if not isinstance(value, DriverInfo):
            raise TypeError('%s must be an instance of DriverInfo' % (option,))
        return value


    def validate_is_callable_or_none(option, value):
        """Validates that 'value' is a callable."""
        if value is None:
            return value
        if not callable(value):
            raise ValueError('%s must be a callable' % (option,))
        return value


    def validate_ok_for_replace(replacement):
        """Validate a replacement document."""
        validate_is_mapping('replacement', replacement)
        if replacement:
            if not isinstance(replacement, RawBSONDocument):
                first = next(iter(replacement))
                if first.startswith('$'):
                    raise ValueError('replacement can not include $ operators')


    def validate_ok_for_update(update):
        """Validate an update document."""
        validate_list_or_mapping('update', update)
        if not update:
            raise ValueError('update cannot be empty')
        is_document = not isinstance(update, list)
        first = next(iter(update))
        if is_document:
            if not first.startswith('$'):
                raise ValueError('update only works with $ operators')


    _UNICODE_DECODE_ERROR_HANDLERS = frozenset(['strict', 'replace', 'ignore'])

    def validate_unicode_decode_error_handler(dummy, value):
        """Validate the Unicode decode error handler option of CodecOptions.
    """
        if value not in _UNICODE_DECODE_ERROR_HANDLERS:
            raise ValueError('%s is an invalid Unicode decode error handler. Must be one of %s' % (
             value, tuple(_UNICODE_DECODE_ERROR_HANDLERS)))
        return value


    def validate_tzinfo(dummy, value):
        """Validate the tzinfo option
    """
        if value is not None:
            if not isinstance(value, datetime.tzinfo):
                raise TypeError('%s must be an instance of datetime.tzinfo' % value)
        return value


    URI_OPTIONS_ALIAS_MAP = {'journal':[
      'j'], 
     'wtimeoutms':[
      'wtimeout'], 
     'tls':[
      'ssl'], 
     'tlsallowinvalidcertificates':[
      'ssl_cert_reqs'], 
     'tlsallowinvalidhostnames':[
      'ssl_match_hostname'], 
     'tlscrlfile':[
      'ssl_crlfile'], 
     'tlscafile':[
      'ssl_ca_certs'], 
     'tlscertificatekeyfile':[
      'ssl_certfile'], 
     'tlscertificatekeyfilepassword':[
      'ssl_pem_passphrase']}
    URI_OPTIONS_VALIDATOR_MAP = {'appname':validate_appname_or_none, 
     'authmechanism':validate_auth_mechanism, 
     'authmechanismproperties':validate_auth_mechanism_properties, 
     'authsource':validate_string, 
     'compressors':validate_compressors, 
     'connecttimeoutms':validate_timeout_or_none, 
     'heartbeatfrequencyms':validate_timeout_or_none, 
     'journal':validate_boolean_or_string, 
     'localthresholdms':validate_positive_float_or_zero, 
     'maxidletimems':validate_timeout_or_none, 
     'maxpoolsize':validate_positive_integer_or_none, 
     'maxstalenessseconds':validate_max_staleness, 
     'readconcernlevel':validate_string_or_none, 
     'readpreference':validate_read_preference_mode, 
     'readpreferencetags':validate_read_preference_tags, 
     'replicaset':validate_string_or_none, 
     'retryreads':validate_boolean_or_string, 
     'retrywrites':validate_boolean_or_string, 
     'serverselectiontimeoutms':validate_timeout_or_zero, 
     'sockettimeoutms':validate_timeout_or_none, 
     'ssl_keyfile':validate_readable, 
     'tls':validate_boolean_or_string, 
     'tlsallowinvalidcertificates':validate_allow_invalid_certs, 
     'ssl_cert_reqs':validate_cert_reqs, 
     'tlsallowinvalidhostnames':lambda *x: not validate_boolean_or_string(*x), 
     'ssl_match_hostname':validate_boolean_or_string, 
     'tlscafile':validate_readable, 
     'tlscertificatekeyfile':validate_readable, 
     'tlscertificatekeyfilepassword':validate_string_or_none, 
     'tlsinsecure':validate_boolean_or_string, 
     'w':validate_non_negative_int_or_basestring, 
     'wtimeoutms':validate_non_negative_integer, 
     'zlibcompressionlevel':validate_zlib_compression_level}
    NONSPEC_OPTIONS_VALIDATOR_MAP = {'connect':validate_boolean_or_string, 
     'driver':validate_driver_or_none, 
     'fsync':validate_boolean_or_string, 
     'minpoolsize':validate_non_negative_integer, 
     'socketkeepalive':validate_boolean_or_string, 
     'tlscrlfile':validate_readable, 
     'tz_aware':validate_boolean_or_string, 
     'unicode_decode_error_handler':validate_unicode_decode_error_handler, 
     'uuidrepresentation':validate_uuid_representation, 
     'waitqueuemultiple':validate_non_negative_integer_or_none, 
     'waitqueuetimeoutms':validate_timeout_or_none}
    KW_VALIDATORS = {'document_class':validate_document_class, 
     'type_registry':validate_type_registry, 
     'read_preference':validate_read_preference, 
     'event_listeners':_validate_event_listeners, 
     'tzinfo':validate_tzinfo, 
     'username':validate_string_or_none, 
     'password':validate_string_or_none, 
     'server_selector':validate_is_callable_or_none, 
     'auto_encryption_opts':validate_auto_encryption_opts_or_none}
    INTERNAL_URI_OPTION_NAME_MAP = {'j':'journal', 
     'wtimeout':'wtimeoutms', 
     'tls':'ssl', 
     'tlsallowinvalidcertificates':'ssl_cert_reqs', 
     'tlsallowinvalidhostnames':'ssl_match_hostname', 
     'tlscrlfile':'ssl_crlfile', 
     'tlscafile':'ssl_ca_certs', 
     'tlscertificatekeyfile':'ssl_certfile', 
     'tlscertificatekeyfilepassword':'ssl_pem_passphrase'}
    URI_OPTIONS_DEPRECATION_MAP = {'j':('renamed', 'journal'), 
     'wtimeout':('renamed', 'wTimeoutMS'), 
     'ssl_cert_reqs':('renamed', 'tlsAllowInvalidCertificates'), 
     'ssl_match_hostname':('renamed', 'tlsAllowInvalidHostnames'), 
     'ssl_crlfile':('renamed', 'tlsCRLFile'), 
     'ssl_ca_certs':('renamed', 'tlsCAFile'), 
     'ssl_pem_passphrase':('renamed', 'tlsCertificateKeyFilePassword'), 
     'waitqueuemultiple':('removed', 'Instead of using waitQueueMultiple to bound queuing, limit the size of the thread pool in your application server')}
    URI_OPTIONS_VALIDATOR_MAP.update(NONSPEC_OPTIONS_VALIDATOR_MAP)
    for optname, aliases in iteritems(URI_OPTIONS_ALIAS_MAP):
        for alias in aliases:
            if alias not in URI_OPTIONS_VALIDATOR_MAP:
                URI_OPTIONS_VALIDATOR_MAP[alias] = URI_OPTIONS_VALIDATOR_MAP[optname]
        else:
            VALIDATORS = URI_OPTIONS_VALIDATOR_MAP.copy()
            VALIDATORS.update(KW_VALIDATORS)
            TIMEOUT_OPTIONS = [
             'connecttimeoutms',
             'heartbeatfrequencyms',
             'maxidletimems',
             'maxstalenessseconds',
             'serverselectiontimeoutms',
             'sockettimeoutms',
             'waitqueuetimeoutms']
            _AUTH_OPTIONS = frozenset(['authmechanismproperties'])

            def validate_auth_option(option, value):
                """Validate optional authentication parameters.
    """
                lower, value = validate(option, value)
                if lower not in _AUTH_OPTIONS:
                    raise ConfigurationError('Unknown authentication option: %s' % (
                     option,))
                return (
                 lower, value)


            def validate(option, value):
                """Generic validation function.
    """
                lower = option.lower()
                validator = VALIDATORS.get(lower, raise_config_error)
                value = validator(option, value)
                return (lower, value)


            def get_validated_options(options, warn=True):
                """Validate each entry in options and raise a warning if it is not valid.
    Returns a copy of options with invalid entries removed.

    :Parameters:
        - `opts`: A dict containing MongoDB URI options.
        - `warn` (optional): If ``True`` then warnings will be logged and
          invalid options will be ignored. Otherwise, invalid options will
          cause errors.
    """
                if isinstance(options, _CaseInsensitiveDictionary):
                    validated_options = _CaseInsensitiveDictionary()
                    get_normed_key = lambda x: x
                    get_setter_key = lambda x: options.cased_key(x)
                else:
                    validated_options = {}
                    get_normed_key = lambda x: x.lower()
                    get_setter_key = lambda x: x
                for opt, value in iteritems(options):
                    normed_key = get_normed_key(opt)
                    try:
                        validator = URI_OPTIONS_VALIDATOR_MAP.get(normed_key, raise_config_error)
                        value = validator(opt, value)
                    except (ValueError, TypeError, ConfigurationError) as exc:
                        try:
                            if warn:
                                warnings.warn(str(exc))
                            else:
                                raise
                        finally:
                            exc = None
                            del exc

                    else:
                        validated_options[get_setter_key(normed_key)] = value
                else:
                    return validated_options


            WRITE_CONCERN_OPTIONS = frozenset([
             'w',
             'wtimeout',
             'wtimeoutms',
             'fsync',
             'j',
             'journal'])

            class BaseObject(object):
                __doc__ = 'A base class that provides attributes and methods common\n    to multiple pymongo classes.\n\n    SHOULD NOT BE USED BY DEVELOPERS EXTERNAL TO MONGODB.\n    '

                def __init__(self, codec_options, read_preference, write_concern, read_concern):
                    if not isinstance(codec_options, CodecOptions):
                        raise TypeError('codec_options must be an instance of bson.codec_options.CodecOptions')
                    else:
                        self._BaseObject__codec_options = codec_options
                        if not isinstance(read_preference, _ServerMode):
                            raise TypeError('%r is not valid for read_preference. See pymongo.read_preferences for valid options.' % (
                             read_preference,))
                        self._BaseObject__read_preference = read_preference
                        if not isinstance(write_concern, WriteConcern):
                            raise TypeError('write_concern must be an instance of pymongo.write_concern.WriteConcern')
                        self._BaseObject__write_concern = write_concern
                        assert isinstance(read_concern, ReadConcern), 'read_concern must be an instance of pymongo.read_concern.ReadConcern'
                    self._BaseObject__read_concern = read_concern

                @property
                def codec_options(self):
                    """Read only access to the :class:`~bson.codec_options.CodecOptions`
        of this instance.
        """
                    return self._BaseObject__codec_options

                @property
                def write_concern(self):
                    """Read only access to the :class:`~pymongo.write_concern.WriteConcern`
        of this instance.

        .. versionchanged:: 3.0
          The :attr:`write_concern` attribute is now read only.
        """
                    return self._BaseObject__write_concern

                def _write_concern_for(self, session):
                    """Read only access to the write concern of this instance or session.
        """
                    if session:
                        if session.in_transaction:
                            return DEFAULT_WRITE_CONCERN
                    return self.write_concern

                @property
                def read_preference(self):
                    """Read only access to the read preference of this instance.

        .. versionchanged:: 3.0
          The :attr:`read_preference` attribute is now read only.
        """
                    return self._BaseObject__read_preference

                def _read_preference_for(self, session):
                    """Read only access to the read preference of this instance or session.
        """
                    if session:
                        return session._txn_read_preference() or self._BaseObject__read_preference
                    return self._BaseObject__read_preference

                @property
                def read_concern(self):
                    """Read only access to the :class:`~pymongo.read_concern.ReadConcern`
        of this instance.

        .. versionadded:: 3.2
        """
                    return self._BaseObject__read_concern


            class _CaseInsensitiveDictionary(abc.MutableMapping):

                def __init__(self, *args, **kwargs):
                    self._CaseInsensitiveDictionary__casedkeys = {}
                    self._CaseInsensitiveDictionary__data = {}
                    self.update(dict(*args, **kwargs))

                def __contains__(self, key):
                    return key.lower() in self._CaseInsensitiveDictionary__data

                def __len__(self):
                    return len(self._CaseInsensitiveDictionary__data)

                def __iter__(self):
                    return (key for key in self._CaseInsensitiveDictionary__casedkeys)

                def __repr__--- This code section failed: ---

 L. 874         0  LOAD_GLOBAL              str
                2  LOAD_CLOSURE             'self'
                4  BUILD_TUPLE_1         1 
                6  LOAD_DICTCOMP            '<code_object <dictcomp>>'
                8  LOAD_STR                 '_CaseInsensitiveDictionary.__repr__.<locals>.<dictcomp>'
               10  MAKE_FUNCTION_8          'closure'
               12  LOAD_DEREF               'self'
               14  GET_ITER         
               16  CALL_FUNCTION_1       1  ''
               18  CALL_FUNCTION_1       1  ''
               20  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

                def __setitem__(self, key, value):
                    lc_key = key.lower()
                    self._CaseInsensitiveDictionary__casedkeys[lc_key] = key
                    self._CaseInsensitiveDictionary__data[lc_key] = value

                def __getitem__(self, key):
                    return self._CaseInsensitiveDictionary__data[key.lower()]

                def __delitem__(self, key):
                    lc_key = key.lower()
                    del self._CaseInsensitiveDictionary__casedkeys[lc_key]
                    del self._CaseInsensitiveDictionary__data[lc_key]

                def __eq__(self, other):
                    if not isinstance(other, abc.Mapping):
                        return NotImplemented
                    if len(self) != len(other):
                        return False
                    for key in other:
                        if self[key] != other[key]:
                            return False
                        return True

                def get(self, key, default=None):
                    return self._CaseInsensitiveDictionary__data.get(key.lower(), default)

                def pop(self, key, *args, **kwargs):
                    lc_key = key.lower()
                    self._CaseInsensitiveDictionary__casedkeys.pop(lc_key, None)
                    return (self._CaseInsensitiveDictionary__data.pop)(lc_key, *args, **kwargs)

                def popitem(self):
                    lc_key, cased_key = self._CaseInsensitiveDictionary__casedkeys.popitem()
                    value = self._CaseInsensitiveDictionary__data.pop(lc_key)
                    return (cased_key, value)

                def clear(self):
                    self._CaseInsensitiveDictionary__casedkeys.clear()
                    self._CaseInsensitiveDictionary__data.clear()

                def setdefault(self, key, default=None):
                    lc_key = key.lower()
                    if key in self:
                        return self._CaseInsensitiveDictionary__data[lc_key]
                    self._CaseInsensitiveDictionary__casedkeys[lc_key] = key
                    self._CaseInsensitiveDictionary__data[lc_key] = default
                    return default

                def update(self, other):
                    if isinstance(other, _CaseInsensitiveDictionary):
                        for key in other:
                            self[other.cased_key(key)] = other[key]

                    else:
                        for key in other:
                            self[key] = other[key]

                def cased_key(self, key):
                    return self._CaseInsensitiveDictionary__casedkeys[key.lower()]