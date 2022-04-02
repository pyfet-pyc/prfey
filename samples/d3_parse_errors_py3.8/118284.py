# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pymongo\network.py
"""Internal network layer helper methods."""
import datetime, errno, select, struct, threading
_HAS_POLL = True
_EVENT_MASK = 0
try:
    from select import poll
    _EVENT_MASK = select.POLLIN | select.POLLPRI | select.POLLERR | select.POLLHUP
except ImportError:
    _HAS_POLL = False
else:
    try:
        from select import error as _SELECT_ERROR
    except ImportError:
        _SELECT_ERROR = OSError
    else:
        from bson import _decode_all_selective
        from bson.py3compat import PY3
        from pymongo import helpers, message
        from pymongo.common import MAX_MESSAGE_SIZE
        from pymongo.compression_support import decompress, _NO_COMPRESSION
        from pymongo.errors import AutoReconnect, NotMasterError, OperationFailure, ProtocolError
        from pymongo.message import _UNPACK_REPLY
        _UNPACK_HEADER = struct.Struct('<iiii').unpack

        def command(sock, dbname, spec, slave_ok, is_mongos, read_preference, codec_options, session, client, check=True, allowable_errors=None, address=None, check_keys=False, listeners=None, max_bson_size=None, read_concern=None, parse_write_concern_error=False, collation=None, compression_ctx=None, use_op_msg=False, unacknowledged=False, user_fields=None):
            """Execute a command over the socket, or raise socket.error.

    :Parameters:
      - `sock`: a raw socket instance
      - `dbname`: name of the database on which to run the command
      - `spec`: a command document as an ordered dict type, eg SON.
      - `slave_ok`: whether to set the SlaveOkay wire protocol bit
      - `is_mongos`: are we connected to a mongos?
      - `read_preference`: a read preference
      - `codec_options`: a CodecOptions instance
      - `session`: optional ClientSession instance.
      - `client`: optional MongoClient instance for updating $clusterTime.
      - `check`: raise OperationFailure if there are errors
      - `allowable_errors`: errors to ignore if `check` is True
      - `address`: the (host, port) of `sock`
      - `check_keys`: if True, check `spec` for invalid keys
      - `listeners`: An instance of :class:`~pymongo.monitoring.EventListeners`
      - `max_bson_size`: The maximum encoded bson size for this server
      - `read_concern`: The read concern for this command.
      - `parse_write_concern_error`: Whether to parse the ``writeConcernError``
        field in the command response.
      - `collation`: The collation for this command.
      - `compression_ctx`: optional compression Context.
      - `use_op_msg`: True if we should use OP_MSG.
      - `unacknowledged`: True if this is an unacknowledged command.
      - `user_fields` (optional): Response fields that should be decoded
        using the TypeDecoders from codec_options, passed to
        bson._decode_all_selective.
    """
            name = next(iter(spec))
            ns = dbname + '.$cmd'
            flags = 4 if slave_ok else 0
            orig = spec
            if is_mongos:
                if not use_op_msg:
                    spec = message._maybe_add_read_preference(spec, read_preference)
                if read_concern:
                    if session and not session.in_transaction:
                        if read_concern.level:
                            spec['readConcern'] = read_concern.document
                        if session:
                            if session.options.causal_consistency:
                                if session.operation_time is not None:
                                    spec.setdefault('readConcern', {})['afterClusterTime'] = session.operation_time
                    if collation is not None:
                        spec['collation'] = collation
                    publish = listeners is not None and listeners.enabled_for_commands
                    if publish:
                        start = datetime.datetime.now()
                    if compression_ctx:
                        if name.lower() in _NO_COMPRESSION:
                            compression_ctx = None
                if not client or client._encrypter:
                    if not client._encrypter._bypass_auto_encryption:
                        spec = orig = client._encrypter.encrypt(dbname, spec, check_keys, codec_options)
                        check_keys = False
                    if use_op_msg:
                        flags = 2 if unacknowledged else 0
                        request_id, msg, size, max_doc_size = message._op_msg(flags,
                          spec, dbname, read_preference, slave_ok, check_keys, codec_options,
                          ctx=compression_ctx)
                        if unacknowledged:
                            if not max_bson_size is not None or max_doc_size > max_bson_size:
                                message._raise_document_too_large(name, size, max_bson_size)
                    else:
                        request_id, msg, size = message.query(flags, ns, 0, -1, spec, None, codec_options, check_keys, compression_ctx)
                    if max_bson_size is not None:
                        if size > max_bson_size + message._COMMAND_OVERHEAD:
                            message._raise_document_too_large(name, size, max_bson_size + message._COMMAND_OVERHEAD)
                    if publish:
                        encoding_duration = datetime.datetime.now() - start
                        listeners.publish_command_start(orig, dbname, request_id, address)
                        start = datetime.datetime.now()
            try:
                sock.sendall(msg)
                if use_op_msg and unacknowledged:
                    reply = None
                    response_doc = {'ok': 1}
                else:
                    reply = receive_message(sock, request_id)
                    unpacked_docs = reply.unpack_response(codec_options=codec_options,
                      user_fields=user_fields)
                    response_doc = unpacked_docs[0]
                    if client:
                        client._process_response(response_doc, session)
                    if check:
                        helpers._check_command_response(response_doc,
                          None, allowable_errors, parse_write_concern_error=parse_write_concern_error)
            except Exception as exc:
                try:
                    if publish:
                        duration = datetime.datetime.now() - start + encoding_duration
                        if isinstance(exc, (NotMasterError, OperationFailure)):
                            failure = exc.details
                        else:
                            failure = message._convert_exception(exc)
                        listeners.publish_command_failure(duration, failure, name, request_id, address)
                    raise
                finally:
                    exc = None
                    del exc

            else:
                if publish:
                    duration = datetime.datetime.now() - start + encoding_duration
                    listeners.publish_command_success(duration, response_doc, name, request_id, address)
                else:
                    if client:
                        if client._encrypter:
                            if reply:
                                decrypted = client._encrypter.decrypt(reply.raw_command_response())
                                response_doc = _decode_all_selective(decrypted, codec_options, user_fields)[0]
                    return response_doc


        _UNPACK_COMPRESSION_HEADER = struct.Struct('<iiB').unpack

        def receive_message(sock, request_id, max_message_size=MAX_MESSAGE_SIZE):
            """Receive a raw BSON message or raise socket.error."""
            length, _, response_to, op_code = _UNPACK_HEADER(_receive_data_on_socket(sock, 16))
            if request_id is not None:
                if request_id != response_to:
                    raise ProtocolError('Got response id %r but expected %r' % (
                     response_to, request_id))
            if length <= 16:
                raise ProtocolError('Message length (%r) not longer than standard message header size (16)' % (
                 length,))
            if length > max_message_size:
                raise ProtocolError('Message length (%r) is larger than server max message size (%r)' % (
                 length, max_message_size))
            if op_code == 2012:
                op_code, _, compressor_id = _UNPACK_COMPRESSION_HEADER(_receive_data_on_socket(sock, 9))
                data = decompress(_receive_data_on_socket(sock, length - 25), compressor_id)
            else:
                data = _receive_data_on_socket(sock, length - 16)
            try:
                unpack_reply = _UNPACK_REPLY[op_code]
            except KeyError:
                raise ProtocolError('Got opcode %r but expected %r' % (
                 op_code, _UNPACK_REPLY.keys()))
            else:
                return unpack_reply(data)


        if not PY3:

            def _receive_data_on_socket--- This code section failed: ---

 L. 231         0  LOAD_GLOBAL              bytearray
                2  LOAD_FAST                'length'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'buf'

 L. 232         8  LOAD_CONST               0
               10  STORE_FAST               'i'
             12_0  COME_FROM           154  '154'
             12_1  COME_FROM            72  '72'

 L. 233        12  LOAD_FAST                'length'
               14  POP_JUMP_IF_FALSE   156  'to 156'

 L. 234        16  SETUP_FINALLY        32  'to 32'

 L. 235        18  LOAD_FAST                'sock'
               20  LOAD_METHOD              recv
               22  LOAD_FAST                'length'
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'chunk'
               28  POP_BLOCK        
               30  JUMP_FORWARD         94  'to 94'
             32_0  COME_FROM_FINALLY    16  '16'

 L. 236        32  DUP_TOP          
               34  LOAD_GLOBAL              IOError
               36  LOAD_GLOBAL              OSError
               38  BUILD_TUPLE_2         2 
               40  COMPARE_OP               exception-match
               42  POP_JUMP_IF_FALSE    92  'to 92'
               44  POP_TOP          
               46  STORE_FAST               'exc'
               48  POP_TOP          
               50  SETUP_FINALLY        80  'to 80'

 L. 237        52  LOAD_GLOBAL              _errno_from_exception
               54  LOAD_FAST                'exc'
               56  CALL_FUNCTION_1       1  ''
               58  LOAD_GLOBAL              errno
               60  LOAD_ATTR                EINTR
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_FALSE    74  'to 74'

 L. 238        66  POP_BLOCK        
               68  POP_EXCEPT       
               70  CALL_FINALLY         80  'to 80'
               72  JUMP_BACK            12  'to 12'
             74_0  COME_FROM            64  '64'

 L. 239        74  RAISE_VARARGS_0       0  'reraise'
               76  POP_BLOCK        
               78  BEGIN_FINALLY    
             80_0  COME_FROM            70  '70'
             80_1  COME_FROM_FINALLY    50  '50'
               80  LOAD_CONST               None
               82  STORE_FAST               'exc'
               84  DELETE_FAST              'exc'
               86  END_FINALLY      
               88  POP_EXCEPT       
               90  JUMP_FORWARD         94  'to 94'
             92_0  COME_FROM            42  '42'
               92  END_FINALLY      
             94_0  COME_FROM            90  '90'
             94_1  COME_FROM            30  '30'

 L. 240        94  LOAD_FAST                'chunk'
               96  LOAD_CONST               b''
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_FALSE   110  'to 110'

 L. 241       102  LOAD_GLOBAL              AutoReconnect
              104  LOAD_STR                 'connection closed'
              106  CALL_FUNCTION_1       1  ''
              108  RAISE_VARARGS_1       1  'exception instance'
            110_0  COME_FROM           100  '100'

 L. 243       110  LOAD_FAST                'chunk'
              112  LOAD_FAST                'buf'
              114  LOAD_FAST                'i'
              116  LOAD_FAST                'i'
              118  LOAD_GLOBAL              len
              120  LOAD_FAST                'chunk'
              122  CALL_FUNCTION_1       1  ''
              124  BINARY_ADD       
              126  BUILD_SLICE_2         2 
              128  STORE_SUBSCR     

 L. 244       130  LOAD_FAST                'i'
              132  LOAD_GLOBAL              len
              134  LOAD_FAST                'chunk'
              136  CALL_FUNCTION_1       1  ''
              138  INPLACE_ADD      
              140  STORE_FAST               'i'

 L. 245       142  LOAD_FAST                'length'
              144  LOAD_GLOBAL              len
              146  LOAD_FAST                'chunk'
              148  CALL_FUNCTION_1       1  ''
              150  INPLACE_SUBTRACT 
              152  STORE_FAST               'length'
              154  JUMP_BACK            12  'to 12'
            156_0  COME_FROM            14  '14'

 L. 247       156  LOAD_GLOBAL              bytes
              158  LOAD_FAST                'buf'
              160  CALL_FUNCTION_1       1  ''
              162  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 68


        else:

            def _receive_data_on_socket--- This code section failed: ---

 L. 250         0  LOAD_GLOBAL              bytearray
                2  LOAD_FAST                'length'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'buf'

 L. 251         8  LOAD_GLOBAL              memoryview
               10  LOAD_FAST                'buf'
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'mv'

 L. 252        16  LOAD_CONST               0
               18  STORE_FAST               'bytes_read'
             20_0  COME_FROM           138  '138'
             20_1  COME_FROM            92  '92'

 L. 253        20  LOAD_FAST                'bytes_read'
               22  LOAD_FAST                'length'
               24  COMPARE_OP               <
               26  POP_JUMP_IF_FALSE   140  'to 140'

 L. 254        28  SETUP_FINALLY        52  'to 52'

 L. 255        30  LOAD_FAST                'sock'
               32  LOAD_METHOD              recv_into
               34  LOAD_FAST                'mv'
               36  LOAD_FAST                'bytes_read'
               38  LOAD_CONST               None
               40  BUILD_SLICE_2         2 
               42  BINARY_SUBSCR    
               44  CALL_METHOD_1         1  ''
               46  STORE_FAST               'chunk_length'
               48  POP_BLOCK        
               50  JUMP_FORWARD        114  'to 114'
             52_0  COME_FROM_FINALLY    28  '28'

 L. 256        52  DUP_TOP          
               54  LOAD_GLOBAL              IOError
               56  LOAD_GLOBAL              OSError
               58  BUILD_TUPLE_2         2 
               60  COMPARE_OP               exception-match
               62  POP_JUMP_IF_FALSE   112  'to 112'
               64  POP_TOP          
               66  STORE_FAST               'exc'
               68  POP_TOP          
               70  SETUP_FINALLY       100  'to 100'

 L. 257        72  LOAD_GLOBAL              _errno_from_exception
               74  LOAD_FAST                'exc'
               76  CALL_FUNCTION_1       1  ''
               78  LOAD_GLOBAL              errno
               80  LOAD_ATTR                EINTR
               82  COMPARE_OP               ==
               84  POP_JUMP_IF_FALSE    94  'to 94'

 L. 258        86  POP_BLOCK        
               88  POP_EXCEPT       
               90  CALL_FINALLY        100  'to 100'
               92  JUMP_BACK            20  'to 20'
             94_0  COME_FROM            84  '84'

 L. 259        94  RAISE_VARARGS_0       0  'reraise'
               96  POP_BLOCK        
               98  BEGIN_FINALLY    
            100_0  COME_FROM            90  '90'
            100_1  COME_FROM_FINALLY    70  '70'
              100  LOAD_CONST               None
              102  STORE_FAST               'exc'
              104  DELETE_FAST              'exc'
              106  END_FINALLY      
              108  POP_EXCEPT       
              110  JUMP_FORWARD        114  'to 114'
            112_0  COME_FROM            62  '62'
              112  END_FINALLY      
            114_0  COME_FROM           110  '110'
            114_1  COME_FROM            50  '50'

 L. 260       114  LOAD_FAST                'chunk_length'
              116  LOAD_CONST               0
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_FALSE   130  'to 130'

 L. 261       122  LOAD_GLOBAL              AutoReconnect
              124  LOAD_STR                 'connection closed'
              126  CALL_FUNCTION_1       1  ''
              128  RAISE_VARARGS_1       1  'exception instance'
            130_0  COME_FROM           120  '120'

 L. 263       130  LOAD_FAST                'bytes_read'
              132  LOAD_FAST                'chunk_length'
              134  INPLACE_ADD      
              136  STORE_FAST               'bytes_read'
              138  JUMP_BACK            20  'to 20'
            140_0  COME_FROM            26  '26'

 L. 265       140  LOAD_FAST                'mv'
              142  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 88


        def _errno_from_exception(exc):
            if hasattr(exc, 'errno'):
                return exc.errno
            if exc.args:
                return exc.args[0]
            return


        class SocketChecker(object):

            def __init__(self):
                if _HAS_POLL:
                    self._lock = threading.Lock()
                    self._poller = poll()
                else:
                    self._lock = None
                    self._poller = None

            def socket_closed--- This code section failed: ---
              0_0  COME_FROM           192  '192'

 L. 291         0  SETUP_FINALLY       102  'to 102'

 L. 292         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _poller
                6  POP_JUMP_IF_FALSE    74  'to 74'

 L. 293         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _lock
               12  SETUP_WITH           66  'to 66'
               14  POP_TOP          

 L. 294        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _poller
               20  LOAD_METHOD              register
               22  LOAD_FAST                'sock'
               24  LOAD_GLOBAL              _EVENT_MASK
               26  CALL_METHOD_2         2  ''
               28  POP_TOP          

 L. 295        30  SETUP_FINALLY        48  'to 48'

 L. 296        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _poller
               36  LOAD_METHOD              poll
               38  LOAD_CONST               0
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'rd'
               44  POP_BLOCK        
               46  BEGIN_FINALLY    
             48_0  COME_FROM_FINALLY    30  '30'

 L. 298        48  LOAD_FAST                'self'
               50  LOAD_ATTR                _poller
               52  LOAD_METHOD              unregister
               54  LOAD_FAST                'sock'
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          
               60  END_FINALLY      
               62  POP_BLOCK        
               64  BEGIN_FINALLY    
             66_0  COME_FROM_WITH       12  '12'
               66  WITH_CLEANUP_START
               68  WITH_CLEANUP_FINISH
               70  END_FINALLY      
               72  JUMP_FORWARD         98  'to 98'
             74_0  COME_FROM             6  '6'

 L. 300        74  LOAD_GLOBAL              select
               76  LOAD_METHOD              select
               78  LOAD_FAST                'sock'
               80  BUILD_LIST_1          1 
               82  BUILD_LIST_0          0 
               84  BUILD_LIST_0          0 
               86  LOAD_CONST               0
               88  CALL_METHOD_4         4  ''
               90  UNPACK_SEQUENCE_3     3 
               92  STORE_FAST               'rd'
               94  STORE_FAST               '_'
               96  STORE_FAST               '_'
             98_0  COME_FROM            72  '72'
               98  POP_BLOCK        
              100  JUMP_FORWARD        238  'to 238'
            102_0  COME_FROM_FINALLY     0  '0'

 L. 301       102  DUP_TOP          
              104  LOAD_GLOBAL              RuntimeError
              106  LOAD_GLOBAL              KeyError
              108  BUILD_TUPLE_2         2 
              110  COMPARE_OP               exception-match
              112  POP_JUMP_IF_FALSE   126  'to 126'
              114  POP_TOP          
              116  POP_TOP          
              118  POP_TOP          

 L. 306       120  RAISE_VARARGS_0       0  'reraise'
              122  POP_EXCEPT       
              124  JUMP_FORWARD        238  'to 238'
            126_0  COME_FROM           112  '112'

 L. 307       126  DUP_TOP          
              128  LOAD_GLOBAL              ValueError
              130  COMPARE_OP               exception-match
              132  POP_JUMP_IF_FALSE   146  'to 146'
              134  POP_TOP          
              136  POP_TOP          
              138  POP_TOP          

 L. 311       140  POP_EXCEPT       
              142  LOAD_CONST               True
              144  RETURN_VALUE     
            146_0  COME_FROM           132  '132'

 L. 312       146  DUP_TOP          
              148  LOAD_GLOBAL              _SELECT_ERROR
              150  LOAD_GLOBAL              IOError
              152  BUILD_TUPLE_2         2 
              154  COMPARE_OP               exception-match
              156  POP_JUMP_IF_FALSE   216  'to 216'
              158  POP_TOP          
              160  STORE_FAST               'exc'
              162  POP_TOP          
              164  SETUP_FINALLY       204  'to 204'

 L. 313       166  LOAD_GLOBAL              _errno_from_exception
              168  LOAD_FAST                'exc'
              170  CALL_FUNCTION_1       1  ''
              172  LOAD_GLOBAL              errno
              174  LOAD_ATTR                EINTR
              176  LOAD_GLOBAL              errno
              178  LOAD_ATTR                EAGAIN
              180  BUILD_TUPLE_2         2 
              182  COMPARE_OP               in
              184  POP_JUMP_IF_FALSE   194  'to 194'

 L. 314       186  POP_BLOCK        
              188  POP_EXCEPT       
              190  CALL_FINALLY        204  'to 204'
              192  JUMP_BACK             0  'to 0'
            194_0  COME_FROM           184  '184'

 L. 315       194  POP_BLOCK        
              196  POP_EXCEPT       
              198  CALL_FINALLY        204  'to 204'
              200  LOAD_CONST               True
              202  RETURN_VALUE     
            204_0  COME_FROM           198  '198'
            204_1  COME_FROM           190  '190'
            204_2  COME_FROM_FINALLY   164  '164'
              204  LOAD_CONST               None
              206  STORE_FAST               'exc'
              208  DELETE_FAST              'exc'
              210  END_FINALLY      
              212  POP_EXCEPT       
              214  JUMP_FORWARD        238  'to 238'
            216_0  COME_FROM           156  '156'

 L. 316       216  DUP_TOP          
              218  LOAD_GLOBAL              Exception
              220  COMPARE_OP               exception-match
              222  POP_JUMP_IF_FALSE   236  'to 236'
              224  POP_TOP          
              226  POP_TOP          
              228  POP_TOP          

 L. 319       230  POP_EXCEPT       
              232  LOAD_CONST               True
              234  RETURN_VALUE     
            236_0  COME_FROM           222  '222'
              236  END_FINALLY      
            238_0  COME_FROM           214  '214'
            238_1  COME_FROM           124  '124'
            238_2  COME_FROM           100  '100'

 L. 320       238  LOAD_GLOBAL              len
              240  LOAD_FAST                'rd'
              242  CALL_FUNCTION_1       1  ''
              244  LOAD_CONST               0
              246  COMPARE_OP               >
              248  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 188