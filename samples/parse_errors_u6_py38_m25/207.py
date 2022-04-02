# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: multiprocessing\managers.py
__all__ = [
 'BaseManager', 'SyncManager', 'BaseProxy', 'Token',
 'SharedMemoryManager']
import sys, threading, signal, array, queue, time, os
from os import getpid
from traceback import format_exc
from . import connection
from .context import reduction, get_spawning_popen, ProcessError
from . import pool
from . import process
from . import util
from . import get_context
try:
    from . import shared_memory
    HAS_SHMEM = True
except ImportError:
    HAS_SHMEM = False
else:

    def reduce_array(a):
        return (
         array.array, (a.typecode, a.tobytes()))


    reduction.register(array.array, reduce_array)
    view_types = [type(getattr({}, name)()) for name in ('items', 'keys', 'values')]
    if view_types[0] is not list:

        def rebuild_as_list(obj):
            return (
             list, (list(obj),))


        for view_type in view_types:
            reduction.register(view_type, rebuild_as_list)

    else:

        class Token(object):
            __doc__ = '\n    Type to uniquely identify a shared object\n    '
            __slots__ = ('typeid', 'address', 'id')

            def __init__(self, typeid, address, id):
                self.typeid, self.address, self.id = typeid, address, id

            def __getstate__(self):
                return (
                 self.typeid, self.address, self.id)

            def __setstate__(self, state):
                self.typeid, self.address, self.id = state

            def __repr__(self):
                return '%s(typeid=%r, address=%r, id=%r)' % (
                 self.__class__.__name__, self.typeid, self.address, self.id)


        def dispatch(c, id, methodname, args=(), kwds={}):
            """
    Send a message to manager using connection `c` and return response
    """
            c.send((id, methodname, args, kwds))
            kind, result = c.recv()
            if kind == '#RETURN':
                return result
            raise convert_to_error(kind, result)


        def convert_to_error(kind, result):
            if kind == '#ERROR':
                return result
                if kind in ('#TRACEBACK', '#UNSERIALIZABLE'):
                    if not isinstance(result, str):
                        raise TypeError("Result {0!r} (kind '{1}') type is {2}, not str".format(result, kind, type(result)))
                    if kind == '#UNSERIALIZABLE':
                        return RemoteError('Unserializable message: %s\n' % result)
                    return RemoteError(result)
            else:
                return ValueError('Unrecognized message type {!r}'.format(kind))


        class RemoteError(Exception):

            def __str__(self):
                return '\n---------------------------------------------------------------------------\n' + str(self.args[0]) + '---------------------------------------------------------------------------'


        def all_methods(obj):
            """
    Return a list of names of methods of `obj`
    """
            temp = []
            for name in dir(obj):
                func = getattr(obj, name)
                if callable(func):
                    temp.append(name)
                return temp


        def public_methods(obj):
            """
    Return a list of names of methods of `obj` which do not start with '_'
    """
            return [name for name in all_methods(obj) if name[0] != '_']


        class Server(object):
            __doc__ = '\n    Server class which runs in a process controlled by a manager object\n    '
            public = [
             'shutdown', 'create', 'accept_connection', 'get_methods',
             'debug_info', 'number_of_objects', 'dummy', 'incref', 'decref']

            def __init__(self, registry, address, authkey, serializer):
                if not isinstance(authkey, bytes):
                    raise TypeError('Authkey {0!r} is type {1!s}, not bytes'.format(authkey, type(authkey)))
                self.registry = registry
                self.authkey = process.AuthenticationString(authkey)
                Listener, Client = listener_client[serializer]
                self.listener = Listener(address=address, backlog=16)
                self.address = self.listener.address
                self.id_to_obj = {'0': (None, ())}
                self.id_to_refcount = {}
                self.id_to_local_proxy_obj = {}
                self.mutex = threading.Lock()

            def serve_forever(self):
                """
        Run the server forever
        """
                self.stop_event = threading.Event()
                process.current_process()._manager_server = self
                try:
                    accepter = threading.Thread(target=(self.accepter))
                    accepter.daemon = True
                    accepter.start()
                    try:
                        while not self.stop_event.is_set():
                            self.stop_event.wait(1)

                    except (KeyboardInterrupt, SystemExit):
                        pass

                finally:
                    if sys.stdout != sys.__stdout__:
                        util.debug('resetting stdout, stderr')
                        sys.stdout = sys.__stdout__
                        sys.stderr = sys.__stderr__
                    sys.exit(0)

            def accepter--- This code section failed: ---

 L. 186         0  SETUP_FINALLY        16  'to 16'

 L. 187         2  LOAD_FAST                'self'
                4  LOAD_ATTR                listener
                6  LOAD_METHOD              accept
                8  CALL_METHOD_0         0  ''
               10  STORE_FAST               'c'
               12  POP_BLOCK        
               14  JUMP_FORWARD         40  'to 40'
             16_0  COME_FROM_FINALLY     0  '0'

 L. 188        16  DUP_TOP          
               18  LOAD_GLOBAL              OSError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    38  'to 38'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 189        30  POP_EXCEPT       
               32  JUMP_BACK             0  'to 0'
               34  POP_EXCEPT       
               36  JUMP_FORWARD         40  'to 40'
             38_0  COME_FROM            22  '22'
               38  END_FINALLY      
             40_0  COME_FROM            36  '36'
             40_1  COME_FROM            14  '14'

 L. 190        40  LOAD_GLOBAL              threading
               42  LOAD_ATTR                Thread
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                handle_request
               48  LOAD_FAST                'c'
               50  BUILD_TUPLE_1         1 
               52  LOAD_CONST               ('target', 'args')
               54  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               56  STORE_FAST               't'

 L. 191        58  LOAD_CONST               True
               60  LOAD_FAST                't'
               62  STORE_ATTR               daemon

 L. 192        64  LOAD_FAST                't'
               66  LOAD_METHOD              start
               68  CALL_METHOD_0         0  ''
               70  POP_TOP          
               72  JUMP_BACK             0  'to 0'

Parse error at or near `POP_EXCEPT' instruction at offset 34

            def handle_request(self, c):
                """
        Handle a new connection
        """
                funcname = result = request = None
                try:
                    connection.deliver_challenge(c, self.authkey)
                    connection.answer_challenge(c, self.authkey)
                    request = c.recv()
                    ignore, funcname, args, kwds = request
                    assert funcname in self.public, '%r unrecognized' % funcname
                    func = getattr(self, funcname)
                except Exception:
                    msg = (
                     '#TRACEBACK', format_exc())
                else:
                    try:
                        result = func(c, *args, **kwds)
                    except Exception:
                        msg = (
                         '#TRACEBACK', format_exc())
                    else:
                        msg = (
                         '#RETURN', result)
                    try:
                        c.send(msg)
                    except Exception as e:
                        try:
                            try:
                                c.send(('#TRACEBACK', format_exc()))
                            except Exception:
                                pass
                            else:
                                util.info('Failure to send message: %r', msg)
                                util.info(' ... request was %r', request)
                                util.info(' ... exception was %r', e)
                        finally:
                            e = None
                            del e

                    else:
                        c.close()

            def serve_client(self, conn):
                """
        Handle requests from the proxies in a particular process/thread
        """
                util.debug('starting server thread to service %r', threading.current_thread().name)
                recv = conn.recv
                send = conn.send
                id_to_obj = self.id_to_obj
                while not self.stop_event.is_set():
                    try:
                        methodname = obj = None
                        request = recv()
                        ident, methodname, args, kwds = request
                        try:
                            obj, exposed, gettypeid = id_to_obj[ident]
                        except KeyError as ke:
                            try:
                                try:
                                    obj, exposed, gettypeid = self.id_to_local_proxy_obj[ident]
                                except KeyError as second_ke:
                                    try:
                                        raise ke
                                    finally:
                                        second_ke = None
                                        del second_ke

                            finally:
                                ke = None
                                del ke

                        else:
                            if methodname not in exposed:
                                raise AttributeError('method %r of %r object is not in exposed=%r' % (
                                 methodname, type(obj), exposed))
                            function = getattr(obj, methodname)
                            try:
                                res = function(*args, **kwds)
                            except Exception as e:
                                try:
                                    msg = (
                                     '#ERROR', e)
                                finally:
                                    e = None
                                    del e

                            else:
                                typeid = gettypeid and gettypeid.get(methodname, None)
                                if typeid:
                                    rident, rexposed = self.create(conn, typeid, res)
                                    token = Token(typeid, self.address, rident)
                                    msg = ('#PROXY', (rexposed, token))
                                else:
                                    msg = (
                                     '#RETURN', res)
                    except AttributeError:
                        if methodname is None:
                            msg = (
                             '#TRACEBACK', format_exc())
                        else:
                            try:
                                fallback_func = self.fallback_mapping[methodname]
                                result = fallback_func(
 self, conn, ident, obj, *args, **kwds)
                                msg = (
                                 '#RETURN', result)
                            except Exception:
                                msg = (
                                 '#TRACEBACK', format_exc())

                    except EOFError:
                        util.debug('got EOF -- exiting thread serving %r', threading.current_thread().name)
                        sys.exit(0)
                    except Exception:
                        msg = (
                         '#TRACEBACK', format_exc())
                    else:
                        try:
                            try:
                                send(msg)
                            except Exception as e:
                                try:
                                    send(('#UNSERIALIZABLE', format_exc()))
                                finally:
                                    e = None
                                    del e

                        except Exception as e:
                            try:
                                util.info('exception in thread serving %r', threading.current_thread().name)
                                util.info(' ... message was %r', msg)
                                util.info(' ... exception was %r', e)
                                conn.close()
                                sys.exit(1)
                            finally:
                                e = None
                                del e

            def fallback_getvalue(self, conn, ident, obj):
                return obj

            def fallback_str(self, conn, ident, obj):
                return str(obj)

            def fallback_repr(self, conn, ident, obj):
                return repr(obj)

            fallback_mapping = {'__str__':fallback_str, 
             '__repr__':fallback_repr, 
             '#GETVALUE':fallback_getvalue}

            def dummy(self, c):
                pass

            def debug_info--- This code section failed: ---

 L. 332         0  LOAD_FAST                'self'
                2  LOAD_ATTR                mutex
                4  SETUP_WITH          122  'to 122'
                6  POP_TOP          

 L. 333         8  BUILD_LIST_0          0 
               10  STORE_FAST               'result'

 L. 334        12  LOAD_GLOBAL              list
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                id_to_refcount
               18  LOAD_METHOD              keys
               20  CALL_METHOD_0         0  ''
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'keys'

 L. 335        26  LOAD_FAST                'keys'
               28  LOAD_METHOD              sort
               30  CALL_METHOD_0         0  ''
               32  POP_TOP          

 L. 336        34  LOAD_FAST                'keys'
               36  GET_ITER         
             38_0  COME_FROM            48  '48'
               38  FOR_ITER            100  'to 100'
               40  STORE_FAST               'ident'

 L. 337        42  LOAD_FAST                'ident'
               44  LOAD_STR                 '0'
               46  COMPARE_OP               !=
               48  POP_JUMP_IF_FALSE    38  'to 38'

 L. 338        50  LOAD_FAST                'result'
               52  LOAD_METHOD              append
               54  LOAD_STR                 '  %s:       refcount=%s\n    %s'

 L. 339        56  LOAD_FAST                'ident'
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                id_to_refcount
               62  LOAD_FAST                'ident'
               64  BINARY_SUBSCR    

 L. 340        66  LOAD_GLOBAL              str
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                id_to_obj
               72  LOAD_FAST                'ident'
               74  BINARY_SUBSCR    
               76  LOAD_CONST               0
               78  BINARY_SUBSCR    
               80  CALL_FUNCTION_1       1  ''
               82  LOAD_CONST               None
               84  LOAD_CONST               75
               86  BUILD_SLICE_2         2 
               88  BINARY_SUBSCR    

 L. 339        90  BUILD_TUPLE_3         3 

 L. 338        92  BINARY_MODULO    
               94  CALL_METHOD_1         1  ''
               96  POP_TOP          
               98  JUMP_BACK            38  'to 38'

 L. 341       100  LOAD_STR                 '\n'
              102  LOAD_METHOD              join
              104  LOAD_FAST                'result'
              106  CALL_METHOD_1         1  ''
              108  POP_BLOCK        
              110  ROT_TWO          
              112  BEGIN_FINALLY    
              114  WITH_CLEANUP_START
              116  WITH_CLEANUP_FINISH
              118  POP_FINALLY           0  ''
              120  RETURN_VALUE     
            122_0  COME_FROM_WITH        4  '4'
              122  WITH_CLEANUP_START
              124  WITH_CLEANUP_FINISH
              126  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 110

            def number_of_objects(self, c):
                """
        Number of shared objects
        """
                return len(self.id_to_refcount)

            def shutdown(self, c):
                """
        Shutdown this process
        """
                try:
                    try:
                        util.debug('manager received shutdown message')
                        c.send(('#RETURN', None))
                    except:
                        import traceback
                        traceback.print_exc()

                finally:
                    self.stop_event.set()

            def create(*args, **kwds):
                """
        Create a new shared object and return its id
        """
                if len(args) >= 3:
                    self, c, typeid, *args = args
                else:
                    if not args:
                        raise TypeError("descriptor 'create' of 'Server' object needs an argument")
                    else:
                        if 'typeid' not in kwds:
                            raise TypeError('create expected at least 2 positional arguments, got %d' % (len(args) - 1))
                        else:
                            typeid = kwds.pop('typeid')
                            if len(args) >= 2:
                                self, c, *args = args
                                import warnings
                                warnings.warn("Passing 'typeid' as keyword argument is deprecated", DeprecationWarning,
                                  stacklevel=2)
                            else:
                                if 'c' not in kwds:
                                    raise TypeError('create expected at least 2 positional arguments, got %d' % (len(args) - 1))
                            c = kwds.pop('c')
                            self, *args = args
                            import warnings
                            warnings.warn("Passing 'c' as keyword argument is deprecated", DeprecationWarning,
                              stacklevel=2)
                args = tuple(args)
                with self.mutex:
                    callable, exposed, method_to_typeid, proxytype = self.registry[typeid]
                    if callable is None and not kwds:
                        if len(args) != 1:
                            raise ValueError('Without callable, must have one non-keyword argument')
                        obj = args[0]
                    else:
                        obj = callable(*args, **kwds)
                    if exposed is None:
                        exposed = public_methods(obj)
                    if method_to_typeid is not None:
                        if not isinstance(method_to_typeid, dict):
                            raise TypeError('Method_to_typeid {0!r}: type {1!s}, not dict'.format(method_to_typeid, type(method_to_typeid)))
                        exposed = list(exposed) + list(method_to_typeid)
                    ident = '%x' % id(obj)
                    util.debug('%r callable returned object with id %r', typeid, ident)
                    self.id_to_obj[ident] = (
                     obj, set(exposed), method_to_typeid)
                    if ident not in self.id_to_refcount:
                        self.id_to_refcount[ident] = 0
                self.incref(c, ident)
                return (ident, tuple(exposed))

            create.__text_signature__ = '($self, c, typeid, /, *args, **kwds)'

            def get_methods(self, c, token):
                """
        Return the methods of the shared object indicated by token
        """
                return tuple(self.id_to_obj[token.id][1])

            def accept_connection(self, c, name):
                """
        Spawn a new thread to serve this connection
        """
                threading.current_thread().name = name
                c.send(('#RETURN', None))
                self.serve_client(c)

            def incref(self, c, ident):
                with self.mutex:
                    try:
                        self.id_to_refcount[ident] += 1
                    except KeyError as ke:
                        try:
                            if ident in self.id_to_local_proxy_obj:
                                self.id_to_refcount[ident] = 1
                                self.id_to_obj[ident] = self.id_to_local_proxy_obj[ident]
                                obj, exposed, gettypeid = self.id_to_obj[ident]
                                util.debug('Server re-enabled tracking & INCREF %r', ident)
                            else:
                                raise ke
                        finally:
                            ke = None
                            del ke

            def decref(self, c, ident):
                if ident not in self.id_to_refcount:
                    if ident in self.id_to_local_proxy_obj:
                        util.debug('Server DECREF skipping %r', ident)
                        return None
                with self.mutex:
                    if self.id_to_refcount[ident] <= 0:
                        raise AssertionError('Id {0!s} ({1!r}) has refcount {2:n}, not 1+'.format(ident, self.id_to_obj[ident], self.id_to_refcount[ident]))
                    self.id_to_refcount[ident] -= 1
                    if self.id_to_refcount[ident] == 0:
                        del self.id_to_refcount[ident]
                if ident not in self.id_to_refcount:
                    self.id_to_obj[ident] = (None, (), None)
                    util.debug('disposing of obj with id %r', ident)
                    with self.mutex:
                        del self.id_to_obj[ident]


        class State(object):
            __slots__ = [
             'value']
            INITIAL = 0
            STARTED = 1
            SHUTDOWN = 2


        listener_client = {'pickle':(
          connection.Listener, connection.Client), 
         'xmlrpclib':(
          connection.XmlListener, connection.XmlClient)}

        class BaseManager(object):
            __doc__ = '\n    Base class for managers\n    '
            _registry = {}
            _Server = Server

            def __init__(self, address=None, authkey=None, serializer='pickle', ctx=None):
                if authkey is None:
                    authkey = process.current_process().authkey
                self._address = address
                self._authkey = process.AuthenticationString(authkey)
                self._state = State()
                self._state.value = State.INITIAL
                self._serializer = serializer
                self._Listener, self._Client = listener_client[serializer]
                self._ctx = ctx or get_context()

            def get_server(self):
                """
        Return server object with serve_forever() method and address attribute
        """
                if self._state.value != State.INITIAL:
                    if self._state.value == State.STARTED:
                        raise ProcessError('Already started server')
                    else:
                        if self._state.value == State.SHUTDOWN:
                            raise ProcessError('Manager has shut down')
                        else:
                            raise ProcessError('Unknown state {!r}'.format(self._state.value))
                return Server(self._registry, self._address, self._authkey, self._serializer)

            def connect(self):
                """
        Connect manager object to the server process
        """
                Listener, Client = listener_client[self._serializer]
                conn = Client((self._address), authkey=(self._authkey))
                dispatch(conn, None, 'dummy')
                self._state.value = State.STARTED

            def start(self, initializer=None, initargs=()):
                """
        Spawn a server process for this manager object
        """
                if self._state.value != State.INITIAL:
                    if self._state.value == State.STARTED:
                        raise ProcessError('Already started server')
                    else:
                        if self._state.value == State.SHUTDOWN:
                            raise ProcessError('Manager has shut down')
                        else:
                            raise ProcessError('Unknown state {!r}'.format(self._state.value))
                if initializer is not None:
                    if not callable(initializer):
                        raise TypeError('initializer must be a callable')
                reader, writer = connection.Pipe(duplex=False)
                self._process = self._ctx.Process(target=(type(self)._run_server),
                  args=(
                 self._registry, self._address, self._authkey,
                 self._serializer, writer, initializer, initargs))
                ident = ':'.join((str(i) for i in self._process._identity))
                self._process.name = type(self).__name__ + '-' + ident
                self._process.start()
                writer.close()
                self._address = reader.recv()
                reader.close()
                self._state.value = State.STARTED
                self.shutdown = util.Finalize(self,
                  (type(self)._finalize_manager), args=(
                 self._process, self._address, self._authkey,
                 self._state, self._Client),
                  exitpriority=0)

            @classmethod
            def _run_server(cls, registry, address, authkey, serializer, writer, initializer=None, initargs=()):
                """
        Create a server, report its address and run it
        """
                signal.signal(signal.SIGINT, signal.SIG_IGN)
                if initializer is not None:
                    initializer(*initargs)
                server = cls._Server(registry, address, authkey, serializer)
                writer.send(server.address)
                writer.close()
                util.info('manager serving at %r', server.address)
                server.serve_forever()

            def _create(self, typeid, *args, **kwds):
                """
        Create a new shared object; return the token and exposed tuple
        """
                assert self._state.value == State.STARTED, 'server not yet started'
                conn = self._Client((self._address), authkey=(self._authkey))
                try:
                    id, exposed = dispatch(conn, None, 'create', (typeid,) + args, kwds)
                finally:
                    conn.close()

                return (
                 Token(typeid, self._address, id), exposed)

            def join(self, timeout=None):
                """
        Join the manager process (if it has been spawned)
        """
                if self._process is not None:
                    self._process.join(timeout)
                    if not self._process.is_alive():
                        self._process = None

            def _debug_info(self):
                """
        Return some info about the servers shared objects and connections
        """
                conn = self._Client((self._address), authkey=(self._authkey))
                try:
                    return dispatch(conn, None, 'debug_info')
                finally:
                    conn.close()

            def _number_of_objects(self):
                """
        Return the number of shared objects
        """
                conn = self._Client((self._address), authkey=(self._authkey))
                try:
                    return dispatch(conn, None, 'number_of_objects')
                finally:
                    conn.close()

            def __enter__(self):
                if self._state.value == State.INITIAL:
                    self.start()
                elif self._state.value != State.STARTED:
                    if self._state.value == State.INITIAL:
                        raise ProcessError('Unable to start server')
                    else:
                        if self._state.value == State.SHUTDOWN:
                            raise ProcessError('Manager has shut down')
                        else:
                            raise ProcessError('Unknown state {!r}'.format(self._state.value))
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.shutdown()

            @staticmethod
            def _finalize_manager(process, address, authkey, state, _Client):
                """
        Shutdown the manager process; will be registered as a finalizer
        """
                if process.is_alive():
                    util.info('sending shutdown message to manager')
                    try:
                        conn = _Client(address, authkey=authkey)
                        try:
                            dispatch(conn, None, 'shutdown')
                        finally:
                            conn.close()

                    except Exception:
                        pass
                    else:
                        process.join(timeout=1.0)
                        if process.is_alive():
                            util.info('manager still alive')
                            if hasattr(process, 'terminate'):
                                util.info('trying to `terminate()` manager process')
                                process.terminate()
                                process.join(timeout=0.1)
                                if process.is_alive():
                                    util.info('manager still alive after terminate')
                state.value = State.SHUTDOWN
                try:
                    del BaseProxy._address_to_local[address]
                except KeyError:
                    pass

            @property
            def address(self):
                return self._address

            @classmethod
            def register(cls, typeid, callable=None, proxytype=None, exposed=None, method_to_typeid=None, create_method=True):
                """
        Register a typeid with the manager type
        """
                if '_registry' not in cls.__dict__:
                    cls._registry = cls._registry.copy()
                else:
                    if proxytype is None:
                        proxytype = AutoProxy
                    exposed = exposed or getattr(proxytype, '_exposed_', None)
                    method_to_typeid = method_to_typeid or getattr(proxytype, '_method_to_typeid_', None)
                    if method_to_typeid:
                        for key, value in list(method_to_typeid.items()):
                            assert type(key) is str, '%r is not a string' % key

                        if not type(value) is str:
                            raise AssertionError('%r is not a string' % value)
                cls._registry[typeid] = (
                 callable, exposed, method_to_typeid, proxytype)
                if create_method:

                    def temp(self, *args, **kwds):
                        util.debug('requesting creation of a shared %r object', typeid)
                        token, exp = (self._create)(typeid, *args, **kwds)
                        proxy = proxytype(token,
                          (self._serializer), manager=self, authkey=(self._authkey),
                          exposed=exp)
                        conn = self._Client((token.address), authkey=(self._authkey))
                        dispatch(conn, None, 'decref', (token.id,))
                        return proxy

                    temp.__name__ = typeid
                    setattr(cls, typeid, temp)


        class ProcessLocalSet(set):

            def __init__(self):
                util.register_after_fork(self, lambda obj: obj.clear())

            def __reduce__(self):
                return (type(self), ())


        class BaseProxy(object):
            __doc__ = '\n    A base for proxies of shared objects\n    '
            _address_to_local = {}
            _mutex = util.ForkAwareThreadLock()

            def __init__(self, token, serializer, manager=None, authkey=None, exposed=None, incref=True, manager_owned=False):
                with BaseProxy._mutex:
                    tls_idset = BaseProxy._address_to_local.get(token.address, None)
                    if tls_idset is None:
                        tls_idset = (
                         util.ForkAwareLocal(), ProcessLocalSet())
                        BaseProxy._address_to_local[token.address] = tls_idset
                self._tls = tls_idset[0]
                self._idset = tls_idset[1]
                self._token = token
                self._id = self._token.id
                self._manager = manager
                self._serializer = serializer
                self._Client = listener_client[serializer][1]
                self._owned_by_manager = manager_owned
                if authkey is not None:
                    self._authkey = process.AuthenticationString(authkey)
                else:
                    if self._manager is not None:
                        self._authkey = self._manager._authkey
                    else:
                        self._authkey = process.current_process().authkey
                if incref:
                    self._incref()
                util.register_after_fork(self, BaseProxy._after_fork)

            def _connect(self):
                util.debug('making connection to manager')
                name = process.current_process().name
                if threading.current_thread().name != 'MainThread':
                    name += '|' + threading.current_thread().name
                conn = self._Client((self._token.address), authkey=(self._authkey))
                dispatch(conn, None, 'accept_connection', (name,))
                self._tls.connection = conn

            def _callmethod(self, methodname, args=(), kwds={}):
                """
        Try to call a method of the referent and return a copy of the result
        """
                try:
                    conn = self._tls.connection
                except AttributeError:
                    util.debug('thread %r does not own a connection', threading.current_thread().name)
                    self._connect()
                    conn = self._tls.connection
                else:
                    conn.send((self._id, methodname, args, kwds))
                    kind, result = conn.recv()
                    if kind == '#RETURN':
                        return result
                    if kind == '#PROXY':
                        exposed, token = result
                        proxytype = self._manager._registry[token.typeid][(-1)]
                        token.address = self._token.address
                        proxy = proxytype(token,
                          (self._serializer), manager=(self._manager), authkey=(self._authkey),
                          exposed=exposed)
                        conn = self._Client((token.address), authkey=(self._authkey))
                        dispatch(conn, None, 'decref', (token.id,))
                        return proxy
                    raise convert_to_error(kind, result)

            def _getvalue(self):
                """
        Get a copy of the value of the referent
        """
                return self._callmethod('#GETVALUE')

            def _incref(self):
                if self._owned_by_manager:
                    util.debug('owned_by_manager skipped INCREF of %r', self._token.id)
                    return None
                conn = self._Client((self._token.address), authkey=(self._authkey))
                dispatch(conn, None, 'incref', (self._id,))
                util.debug('INCREF %r', self._token.id)
                self._idset.add(self._id)
                state = self._manager and self._manager._state
                self._close = util.Finalize(self,
                  (BaseProxy._decref), args=(
                 self._token, self._authkey, state,
                 self._tls, self._idset, self._Client),
                  exitpriority=10)

            @staticmethod
            def _decref(token, authkey, state, tls, idset, _Client):
                idset.discard(token.id)
                if state is None or state.value == State.STARTED:
                    try:
                        util.debug('DECREF %r', token.id)
                        conn = _Client((token.address), authkey=authkey)
                        dispatch(conn, None, 'decref', (token.id,))
                    except Exception as e:
                        try:
                            util.debug('... decref failed %s', e)
                        finally:
                            e = None
                            del e

                else:
                    util.debug('DECREF %r -- manager already shutdown', token.id)
                if not idset:
                    if hasattr(tls, 'connection'):
                        util.debug('thread %r has no more proxies so closing conn', threading.current_thread().name)
                        tls.connection.close()
                        del tls.connection

            def _after_fork(self):
                self._manager = None
                try:
                    self._incref()
                except Exception as e:
                    try:
                        util.info('incref failed: %s' % e)
                    finally:
                        e = None
                        del e

            def __reduce__(self):
                kwds = {}
                if get_spawning_popen() is not None:
                    kwds['authkey'] = self._authkey
                if getattr(self, '_isauto', False):
                    kwds['exposed'] = self._exposed_
                    return (RebuildProxy,
                     (
                      AutoProxy, self._token, self._serializer, kwds))
                return (RebuildProxy,
                 (
                  type(self), self._token, self._serializer, kwds))

            def __deepcopy__(self, memo):
                return self._getvalue()

            def __repr__(self):
                return '<%s object, typeid %r at %#x>' % (
                 type(self).__name__, self._token.typeid, id(self))

            def __str__--- This code section failed: ---

 L. 935         0  SETUP_FINALLY        14  'to 14'

 L. 936         2  LOAD_FAST                'self'
                4  LOAD_METHOD              _callmethod
                6  LOAD_STR                 '__repr__'
                8  CALL_METHOD_1         1  ''
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 937        14  DUP_TOP          
               16  LOAD_GLOBAL              Exception
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    52  'to 52'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 938        28  LOAD_GLOBAL              repr
               30  LOAD_FAST                'self'
               32  CALL_FUNCTION_1       1  ''
               34  LOAD_CONST               None
               36  LOAD_CONST               -1
               38  BUILD_SLICE_2         2 
               40  BINARY_SUBSCR    
               42  LOAD_STR                 "; '__str__()' failed>"
               44  BINARY_ADD       
               46  ROT_FOUR         
               48  POP_EXCEPT       
               50  RETURN_VALUE     
             52_0  COME_FROM            20  '20'
               52  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 24


        def RebuildProxy(func, token, serializer, kwds):
            """
    Function used for unpickling proxy objects.
    """
            server = getattr(process.current_process(), '_manager_server', None)
            if server:
                if server.address == token.address:
                    util.debug('Rebuild a proxy owned by manager, token=%r', token)
                    kwds['manager_owned'] = True
                    if token.id not in server.id_to_local_proxy_obj:
                        server.id_to_local_proxy_obj[token.id] = server.id_to_obj[token.id]
            incref = kwds.pop('incref', True) and not getattr(process.current_process(), '_inheriting', False)
            return func(token, serializer, incref=incref, **kwds)


        def MakeProxyType--- This code section failed: ---

 L. 969         0  LOAD_GLOBAL              tuple
                2  LOAD_FAST                'exposed'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'exposed'

 L. 970         8  SETUP_FINALLY        24  'to 24'

 L. 971        10  LOAD_FAST                '_cache'
               12  LOAD_FAST                'name'
               14  LOAD_FAST                'exposed'
               16  BUILD_TUPLE_2         2 
               18  BINARY_SUBSCR    
               20  POP_BLOCK        
               22  RETURN_VALUE     
             24_0  COME_FROM_FINALLY     8  '8'

 L. 972        24  DUP_TOP          
               26  LOAD_GLOBAL              KeyError
               28  COMPARE_OP               exception-match
               30  POP_JUMP_IF_FALSE    42  'to 42'
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L. 973        38  POP_EXCEPT       
               40  JUMP_FORWARD         44  'to 44'
             42_0  COME_FROM            30  '30'
               42  END_FINALLY      
             44_0  COME_FROM            40  '40'

 L. 975        44  BUILD_MAP_0           0 
               46  STORE_FAST               'dic'

 L. 977        48  LOAD_FAST                'exposed'
               50  GET_ITER         
               52  FOR_ITER             76  'to 76'
               54  STORE_FAST               'meth'

 L. 978        56  LOAD_GLOBAL              exec
               58  LOAD_STR                 'def %s(self, /, *args, **kwds):\n        return self._callmethod(%r, args, kwds)'

 L. 979        60  LOAD_FAST                'meth'
               62  LOAD_FAST                'meth'
               64  BUILD_TUPLE_2         2 

 L. 978        66  BINARY_MODULO    

 L. 979        68  LOAD_FAST                'dic'

 L. 978        70  CALL_FUNCTION_2       2  ''
               72  POP_TOP          
               74  JUMP_BACK            52  'to 52'

 L. 981        76  LOAD_GLOBAL              type
               78  LOAD_FAST                'name'
               80  LOAD_GLOBAL              BaseProxy
               82  BUILD_TUPLE_1         1 
               84  LOAD_FAST                'dic'
               86  CALL_FUNCTION_3       3  ''
               88  STORE_FAST               'ProxyType'

 L. 982        90  LOAD_FAST                'exposed'
               92  LOAD_FAST                'ProxyType'
               94  STORE_ATTR               _exposed_

 L. 983        96  LOAD_FAST                'ProxyType'
               98  LOAD_FAST                '_cache'
              100  LOAD_FAST                'name'
              102  LOAD_FAST                'exposed'
              104  BUILD_TUPLE_2         2 
              106  STORE_SUBSCR     

 L. 984       108  LOAD_FAST                'ProxyType'
              110  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 34


        def AutoProxy(token, serializer, manager=None, authkey=None, exposed=None, incref=True):
            """
    Return an auto-proxy for `token`
    """
            _Client = listener_client[serializer][1]
            if exposed is None:
                conn = _Client((token.address), authkey=authkey)
                try:
                    exposed = dispatch(conn, None, 'get_methods', (token,))
                finally:
                    conn.close()

            if authkey is None:
                if manager is not None:
                    authkey = manager._authkey
            if authkey is None:
                authkey = process.current_process().authkey
            ProxyType = MakeProxyType('AutoProxy[%s]' % token.typeid, exposed)
            proxy = ProxyType(token, serializer, manager=manager, authkey=authkey, incref=incref)
            proxy._isauto = True
            return proxy


        class Namespace(object):

            def __init__(self, **kwds):
                self.__dict__.update(kwds)

            def __repr__(self):
                items = list(self.__dict__.items())
                temp = []
                for name, value in items:
                    if not name.startswith('_'):
                        temp.append('%s=%r' % (name, value))
                    temp.sort()
                    return '%s(%s)' % (self.__class__.__name__, ', '.join(temp))


        class Value(object):

            def __init__(self, typecode, value, lock=True):
                self._typecode = typecode
                self._value = value

            def get(self):
                return self._value

            def set(self, value):
                self._value = value

            def __repr__(self):
                return '%s(%r, %r)' % (type(self).__name__, self._typecode, self._value)

            value = property(get, set)


        def Array(typecode, sequence, lock=True):
            return array.array(typecode, sequence)


        class IteratorProxy(BaseProxy):
            _exposed_ = ('__next__', 'send', 'throw', 'close')

            def __iter__(self):
                return self

            def __next__(self, *args):
                return self._callmethod('__next__', args)

            def send(self, *args):
                return self._callmethod('send', args)

            def throw(self, *args):
                return self._callmethod('throw', args)

            def close(self, *args):
                return self._callmethod('close', args)


        class AcquirerProxy(BaseProxy):
            _exposed_ = ('acquire', 'release')

            def acquire(self, blocking=True, timeout=None):
                args = (blocking,) if timeout is None else (blocking, timeout)
                return self._callmethod('acquire', args)

            def release(self):
                return self._callmethod('release')

            def __enter__(self):
                return self._callmethod('acquire')

            def __exit__(self, exc_type, exc_val, exc_tb):
                return self._callmethod('release')


        class ConditionProxy(AcquirerProxy):
            _exposed_ = ('acquire', 'release', 'wait', 'notify', 'notify_all')

            def wait(self, timeout=None):
                return self._callmethod('wait', (timeout,))

            def notify(self, n=1):
                return self._callmethod('notify', (n,))

            def notify_all(self):
                return self._callmethod('notify_all')

            def wait_for(self, predicate, timeout=None):
                result = predicate()
                if result:
                    return result
                if timeout is not None:
                    endtime = time.monotonic() + timeout
                else:
                    endtime = None
                    waittime = None
                    while not result:
                        if endtime is not None:
                            waittime = endtime - time.monotonic()
                            if waittime <= 0:
                                break
                        self.wait(waittime)
                        result = predicate()

                    return result


        class EventProxy(BaseProxy):
            _exposed_ = ('is_set', 'set', 'clear', 'wait')

            def is_set(self):
                return self._callmethod('is_set')

            def set(self):
                return self._callmethod('set')

            def clear(self):
                return self._callmethod('clear')

            def wait(self, timeout=None):
                return self._callmethod('wait', (timeout,))


        class BarrierProxy(BaseProxy):
            _exposed_ = ('__getattribute__', 'wait', 'abort', 'reset')

            def wait(self, timeout=None):
                return self._callmethod('wait', (timeout,))

            def abort(self):
                return self._callmethod('abort')

            def reset(self):
                return self._callmethod('reset')

            @property
            def parties(self):
                return self._callmethod('__getattribute__', ('parties', ))

            @property
            def n_waiting(self):
                return self._callmethod('__getattribute__', ('n_waiting', ))

            @property
            def broken(self):
                return self._callmethod('__getattribute__', ('broken', ))


        class NamespaceProxy(BaseProxy):
            _exposed_ = ('__getattribute__', '__setattr__', '__delattr__')

            def __getattr__(self, key):
                if key[0] == '_':
                    return object.__getattribute__(self, key)
                callmethod = object.__getattribute__(self, '_callmethod')
                return callmethod('__getattribute__', (key,))

            def __setattr__(self, key, value):
                if key[0] == '_':
                    return object.__setattr__(self, key, value)
                callmethod = object.__getattribute__(self, '_callmethod')
                return callmethod('__setattr__', (key, value))

            def __delattr__(self, key):
                if key[0] == '_':
                    return object.__delattr__(self, key)
                callmethod = object.__getattribute__(self, '_callmethod')
                return callmethod('__delattr__', (key,))


        class ValueProxy(BaseProxy):
            _exposed_ = ('get', 'set')

            def get(self):
                return self._callmethod('get')

            def set(self, value):
                return self._callmethod('set', (value,))

            value = property(get, set)


        BaseListProxy = MakeProxyType('BaseListProxy', ('__add__', '__contains__',
                                                        '__delitem__', '__getitem__',
                                                        '__len__', '__mul__', '__reversed__',
                                                        '__rmul__', '__setitem__',
                                                        'append', 'count', 'extend',
                                                        'index', 'insert', 'pop',
                                                        'remove', 'reverse', 'sort',
                                                        '__imul__'))

        class ListProxy(BaseListProxy):

            def __iadd__(self, value):
                self._callmethod('extend', (value,))
                return self

            def __imul__(self, value):
                self._callmethod('__imul__', (value,))
                return self


        DictProxy = MakeProxyType('DictProxy', ('__contains__', '__delitem__', '__getitem__',
                                                '__iter__', '__len__', '__setitem__',
                                                'clear', 'copy', 'get', 'items',
                                                'keys', 'pop', 'popitem', 'setdefault',
                                                'update', 'values'))
        DictProxy._method_to_typeid_ = {'__iter__': 'Iterator'}
        ArrayProxy = MakeProxyType('ArrayProxy', ('__len__', '__getitem__', '__setitem__'))
        BasePoolProxy = MakeProxyType('PoolProxy', ('apply', 'apply_async', 'close',
                                                    'imap', 'imap_unordered', 'join',
                                                    'map', 'map_async', 'starmap',
                                                    'starmap_async', 'terminate'))
        BasePoolProxy._method_to_typeid_ = {'apply_async':'AsyncResult', 
         'map_async':'AsyncResult', 
         'starmap_async':'AsyncResult', 
         'imap':'Iterator', 
         'imap_unordered':'Iterator'}

        class PoolProxy(BasePoolProxy):

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.terminate()


        class SyncManager(BaseManager):
            __doc__ = '\n    Subclass of `BaseManager` which supports a number of shared object types.\n\n    The types registered are those intended for the synchronization\n    of threads, plus `dict`, `list` and `Namespace`.\n\n    The `multiprocessing.Manager()` function creates started instances of\n    this class.\n    '


        SyncManager.register('Queue', queue.Queue)
        SyncManager.register('JoinableQueue', queue.Queue)
        SyncManager.register('Event', threading.Event, EventProxy)
        SyncManager.register('Lock', threading.Lock, AcquirerProxy)
        SyncManager.register('RLock', threading.RLock, AcquirerProxy)
        SyncManager.register('Semaphore', threading.Semaphore, AcquirerProxy)
        SyncManager.register('BoundedSemaphore', threading.BoundedSemaphore, AcquirerProxy)
        SyncManager.register('Condition', threading.Condition, ConditionProxy)
        SyncManager.register('Barrier', threading.Barrier, BarrierProxy)
        SyncManager.register('Pool', pool.Pool, PoolProxy)
        SyncManager.register('list', list, ListProxy)
        SyncManager.register('dict', dict, DictProxy)
        SyncManager.register('Value', Value, ValueProxy)
        SyncManager.register('Array', Array, ArrayProxy)
        SyncManager.register('Namespace', Namespace, NamespaceProxy)
        SyncManager.register('Iterator', proxytype=IteratorProxy, create_method=False)
        SyncManager.register('AsyncResult', create_method=False)
        if HAS_SHMEM:

            class _SharedMemoryTracker:
                __doc__ = 'Manages one or more shared memory segments.'

                def __init__(self, name, segment_names=[]):
                    self.shared_memory_context_name = name
                    self.segment_names = segment_names

                def register_segment(self, segment_name):
                    """Adds the supplied shared memory block name to tracker."""
                    util.debug(f"Register segment {segment_name!r} in pid {getpid()}")
                    self.segment_names.append(segment_name)

                def destroy_segment(self, segment_name):
                    """Calls unlink() on the shared memory block with the supplied name
            and removes it from the list of blocks being tracked."""
                    util.debug(f"Destroy segment {segment_name!r} in pid {getpid()}")
                    self.segment_names.remove(segment_name)
                    segment = shared_memory.SharedMemory(segment_name)
                    segment.close()
                    segment.unlink()

                def unlink(self):
                    """Calls destroy_segment() on all tracked shared memory blocks."""
                    for segment_name in self.segment_names[:]:
                        self.destroy_segment(segment_name)

                def __del__(self):
                    util.debug(f"Call {self.__class__.__name__}.__del__ in {getpid()}")
                    self.unlink()

                def __getstate__(self):
                    return (
                     self.shared_memory_context_name, self.segment_names)

                def __setstate__(self, state):
                    (self.__init__)(*state)


            class SharedMemoryServer(Server):
                public = Server.public + [
                 'track_segment', 'release_segment', 'list_segments']

                def __init__(self, *args, **kwargs):
                    (Server.__init__)(self, *args, **kwargs)
                    address = self.address
                    if isinstance(address, bytes):
                        address = os.fsdecode(address)
                    self.shared_memory_context = _SharedMemoryTracker(f"shm_{address}_{getpid()}")
                    util.debug(f"SharedMemoryServer started by pid {getpid()}")

                def create(*args, **kwargs):
                    """Create a new distributed-shared object (not backed by a shared
            memory block) and return its id to be used in a Proxy Object."""
                    if len(args) >= 3:
                        typeod = args[2]
                    else:
                        if 'typeid' in kwargs:
                            typeid = kwargs['typeid']
                        else:
                            if not args:
                                raise TypeError("descriptor 'create' of 'SharedMemoryServer' object needs an argument")
                            else:
                                raise TypeError('create expected at least 2 positional arguments, got %d' % (len(args) - 1))
                    if hasattr(self.registry[typeid][(-1)], '_shared_memory_proxy'):
                        kwargs['shared_memory_context'] = self.shared_memory_context
                    return (Server.create)(*args, **kwargs)

                create.__text_signature__ = '($self, c, typeid, /, *args, **kwargs)'

                def shutdown(self, c):
                    """Call unlink() on all tracked shared memory, terminate the Server."""
                    self.shared_memory_context.unlink()
                    return Server.shutdown(self, c)

                def track_segment(self, c, segment_name):
                    """Adds the supplied shared memory block name to Server's tracker."""
                    self.shared_memory_context.register_segment(segment_name)

                def release_segment(self, c, segment_name):
                    """Calls unlink() on the shared memory block with the supplied name
            and removes it from the tracker instance inside the Server."""
                    self.shared_memory_context.destroy_segment(segment_name)

                def list_segments(self, c):
                    """Returns a list of names of shared memory blocks that the Server
            is currently tracking."""
                    return self.shared_memory_context.segment_names


            class SharedMemoryManager(BaseManager):
                __doc__ = 'Like SyncManager but uses SharedMemoryServer instead of Server.\n\n        It provides methods for creating and returning SharedMemory instances\n        and for creating a list-like object (ShareableList) backed by shared\n        memory.  It also provides methods that create and return Proxy Objects\n        that support synchronization across processes (i.e. multi-process-safe\n        locks and semaphores).\n        '
                _Server = SharedMemoryServer

                def __init__(self, *args, **kwargs):
                    if os.name == 'posix':
                        from . import resource_tracker
                        resource_tracker.ensure_running()
                    (BaseManager.__init__)(self, *args, **kwargs)
                    util.debug(f"{self.__class__.__name__} created by pid {getpid()}")

                def __del__(self):
                    util.debug(f"{self.__class__.__name__}.__del__ by pid {getpid()}")

                def get_server(self):
                    """Better than monkeypatching for now; merge into Server ultimately"""
                    if self._state.value != State.INITIAL:
                        if self._state.value == State.STARTED:
                            raise ProcessError('Already started SharedMemoryServer')
                        else:
                            if self._state.value == State.SHUTDOWN:
                                raise ProcessError('SharedMemoryManager has shut down')
                            else:
                                raise ProcessError('Unknown state {!r}'.format(self._state.value))
                    return self._Server(self._registry, self._address, self._authkey, self._serializer)

                def SharedMemory(self, size):
                    """Returns a new SharedMemory instance with the specified size in
            bytes, to be tracked by the manager."""
                    with self._Client((self._address), authkey=(self._authkey)) as (conn):
                        sms = shared_memory.SharedMemory(None, create=True, size=size)
                        try:
                            dispatch(conn, None, 'track_segment', (sms.name,))
                        except BaseException as e:
                            try:
                                sms.unlink()
                                raise e
                            finally:
                                e = None
                                del e

                    return sms

                def ShareableList(self, sequence):
                    """Returns a new ShareableList instance populated with the values
            from the input sequence, to be tracked by the manager."""
                    with self._Client((self._address), authkey=(self._authkey)) as (conn):
                        sl = shared_memory.ShareableList(sequence)
                        try:
                            dispatch(conn, None, 'track_segment', (sl.shm.name,))
                        except BaseException as e:
                            try:
                                sl.shm.unlink()
                                raise e
                            finally:
                                e = None
                                del e

                    return sl