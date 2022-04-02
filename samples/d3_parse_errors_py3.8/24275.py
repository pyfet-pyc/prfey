# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: pynput\_util\__init__.py
"""
General utility functions and classes.
"""
import contextlib, functools, importlib, os, sys, threading, six
from six.moves import queue
RESOLUTIONS = {'darwin':'Please make sure that you have Python bindings for the system frameworks installed', 
 'uinput':'Please make sure that you are running as root, and that the utility dumpkeys is installed', 
 'xorg':'Please make sure that you have an X server running, and that the DISPLAY environment variable is set correctly'}

def backend--- This code section failed: ---

 L.  54         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                environ
                4  LOAD_METHOD              get

 L.  55         6  LOAD_STR                 'PYNPUT_BACKEND_{}'
                8  LOAD_METHOD              format
               10  LOAD_FAST                'package'
               12  LOAD_METHOD              rsplit
               14  LOAD_STR                 '.'
               16  CALL_METHOD_1         1  ''
               18  LOAD_CONST               -1
               20  BINARY_SUBSCR    
               22  LOAD_METHOD              upper
               24  CALL_METHOD_0         0  ''
               26  CALL_METHOD_1         1  ''

 L.  56        28  LOAD_GLOBAL              os
               30  LOAD_ATTR                environ
               32  LOAD_METHOD              get
               34  LOAD_STR                 'PYNPUT_BACKEND'
               36  LOAD_CONST               None
               38  CALL_METHOD_2         2  ''

 L.  54        40  CALL_METHOD_2         2  ''
               42  STORE_FAST               'backend_name'

 L.  57        44  LOAD_FAST                'backend_name'
               46  POP_JUMP_IF_FALSE    56  'to 56'

 L.  58        48  LOAD_FAST                'backend_name'
               50  BUILD_LIST_1          1 
               52  STORE_FAST               'modules'
               54  JUMP_FORWARD         98  'to 98'
             56_0  COME_FROM            46  '46'

 L.  59        56  LOAD_GLOBAL              sys
               58  LOAD_ATTR                platform
               60  LOAD_STR                 'darwin'
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_FALSE    74  'to 74'

 L.  60        66  LOAD_STR                 'darwin'
               68  BUILD_LIST_1          1 
               70  STORE_FAST               'modules'
               72  JUMP_FORWARD         98  'to 98'
             74_0  COME_FROM            64  '64'

 L.  61        74  LOAD_GLOBAL              sys
               76  LOAD_ATTR                platform
               78  LOAD_STR                 'win32'
               80  COMPARE_OP               ==
               82  POP_JUMP_IF_FALSE    92  'to 92'

 L.  62        84  LOAD_STR                 'win32'
               86  BUILD_LIST_1          1 
               88  STORE_FAST               'modules'
               90  JUMP_FORWARD         98  'to 98'
             92_0  COME_FROM            82  '82'

 L.  64        92  LOAD_STR                 'xorg'
               94  BUILD_LIST_1          1 
               96  STORE_FAST               'modules'
             98_0  COME_FROM            90  '90'
             98_1  COME_FROM            72  '72'
             98_2  COME_FROM            54  '54'

 L.  66        98  BUILD_LIST_0          0 
              100  STORE_FAST               'errors'

 L.  67       102  BUILD_LIST_0          0 
              104  STORE_FAST               'resolutions'

 L.  68       106  LOAD_FAST                'modules'
              108  GET_ITER         
            110_0  COME_FROM           204  '204'
            110_1  COME_FROM           200  '200'
              110  FOR_ITER            206  'to 206'
              112  STORE_FAST               'module'

 L.  69       114  SETUP_FINALLY       138  'to 138'

 L.  70       116  LOAD_GLOBAL              importlib
              118  LOAD_METHOD              import_module
              120  LOAD_STR                 '._'
              122  LOAD_FAST                'module'
              124  BINARY_ADD       
              126  LOAD_FAST                'package'
              128  CALL_METHOD_2         2  ''
              130  POP_BLOCK        
              132  ROT_TWO          
              134  POP_TOP          
              136  RETURN_VALUE     
            138_0  COME_FROM_FINALLY   114  '114'

 L.  71       138  DUP_TOP          
              140  LOAD_GLOBAL              ImportError
              142  COMPARE_OP               exception-match
              144  POP_JUMP_IF_FALSE   202  'to 202'
              146  POP_TOP          
              148  STORE_FAST               'e'
              150  POP_TOP          
              152  SETUP_FINALLY       190  'to 190'

 L.  72       154  LOAD_FAST                'errors'
              156  LOAD_METHOD              append
              158  LOAD_FAST                'e'
              160  CALL_METHOD_1         1  ''
              162  POP_TOP          

 L.  73       164  LOAD_FAST                'module'
              166  LOAD_GLOBAL              RESOLUTIONS
              168  COMPARE_OP               in
              170  POP_JUMP_IF_FALSE   186  'to 186'

 L.  74       172  LOAD_FAST                'resolutions'
              174  LOAD_METHOD              append
              176  LOAD_GLOBAL              RESOLUTIONS
              178  LOAD_FAST                'module'
              180  BINARY_SUBSCR    
              182  CALL_METHOD_1         1  ''
              184  POP_TOP          
            186_0  COME_FROM           170  '170'
              186  POP_BLOCK        
              188  BEGIN_FINALLY    
            190_0  COME_FROM_FINALLY   152  '152'
              190  LOAD_CONST               None
              192  STORE_FAST               'e'
              194  DELETE_FAST              'e'
              196  END_FINALLY      
              198  POP_EXCEPT       
              200  JUMP_BACK           110  'to 110'
            202_0  COME_FROM           144  '144'
              202  END_FINALLY      
              204  JUMP_BACK           110  'to 110'
            206_0  COME_FROM           110  '110'

 L.  76       206  LOAD_GLOBAL              ImportError

 L.  82       208  LOAD_FAST                'resolutions'

 L.  76   210_212  POP_JUMP_IF_FALSE   264  'to 264'
              214  LOAD_STR                 'this platform is not supported: {}'
              216  LOAD_METHOD              format

 L.  77       218  LOAD_STR                 '; '
              220  LOAD_METHOD              join
              222  LOAD_GENEXPR             '<code_object <genexpr>>'
              224  LOAD_STR                 'backend.<locals>.<genexpr>'
              226  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              228  LOAD_FAST                'errors'
              230  GET_ITER         
              232  CALL_FUNCTION_1       1  ''
              234  CALL_METHOD_1         1  ''

 L.  76       236  CALL_METHOD_1         1  ''

 L.  77       238  LOAD_STR                 '\n\nTry one of the following resolutions:\n\n'

 L.  79       240  LOAD_STR                 '\n\n'
              242  LOAD_METHOD              join
              244  LOAD_GENEXPR             '<code_object <genexpr>>'
              246  LOAD_STR                 'backend.<locals>.<genexpr>'
              248  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.  81       250  LOAD_FAST                'resolutions'

 L.  79       252  GET_ITER         
              254  CALL_FUNCTION_1       1  ''
              256  CALL_METHOD_1         1  ''

 L.  77       258  BINARY_ADD       

 L.  76       260  BINARY_ADD       
              262  JUMP_FORWARD        266  'to 266'
            264_0  COME_FROM           210  '210'

 L.  82       264  LOAD_STR                 ''
            266_0  COME_FROM           262  '262'

 L.  76       266  CALL_FUNCTION_1       1  ''
              268  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `ROT_TWO' instruction at offset 132


class AbstractListener(threading.Thread):
    __doc__ = 'A class implementing the basic behaviour for event listeners.\n\n    Instances of this class can be used as context managers. This is equivalent\n    to the following code::\n\n        listener.start()\n        listener.wait()\n        try:\n            with_statements()\n        finally:\n            listener.stop()\n\n    Actual implementations of this class must set the attribute ``_log``, which\n    must be an instance of :class:`logging.Logger`.\n\n    :param bool suppress: Whether to suppress events. Setting this to ``True``\n        will prevent the input events from being passed to the rest of the\n        system.\n\n    :param kwargs: A mapping from callback attribute to callback handler. All\n        handlers will be wrapped in a function reading the return value of the\n        callback, and if it ``is False``, raising :class:`StopException`.\n\n        Any callback that is falsy will be ignored.\n    '

    class StopException(Exception):
        __doc__ = 'If an event listener callback raises this exception, the current\n        listener is stopped.\n        '

    _HANDLED_EXCEPTIONS = tuple()

    def __init__(self, suppress=False, **kwargs):
        super(AbstractListener, self).__init__

        def wrapper(f):

            def inner(*args):
                if f(*args) is False:
                    raise self.StopException

            return inner

        self._suppress = suppress
        self._running = False
        self._thread = threading.current_thread
        self._condition = threading.Condition
        self._ready = False
        self._queue = queue.Queue10
        self.daemon = True
        for name, callback in kwargs.items:
            setattr(self, name, wrapper(callback or (lambda *a: None)))

    @property
    def suppress(self):
        """Whether to suppress events.
        """
        return self._suppress

    @property
    def running(self):
        """Whether the listener is currently running.
        """
        return self._running

    def stop(self):
        """Stops listening for events.

        When this method returns, no more events will be delivered. Once this
        method has been called, the listener instance cannot be used any more,
        since a listener is a :class:`threading.Thread`, and once stopped it
        cannot be restarted.

        To resume listening for event, a new listener must be created.
        """
        if self._running:
            self._running = False
            self._queue.putNone
            self._stop_platform

    def __enter__(self):
        self.start
        self.wait
        return self

    def __exit__(self, exc_type, value, traceback):
        self.stop

    def wait(self):
        """Waits for this listener to become ready.
        """
        self._condition.acquire
        while True:
            self._ready or self._condition.wait

        self._condition.release

    def run(self):
        """The thread runner method.
        """
        self._running = True
        self._thread = threading.current_thread
        self._run
        self._queue.putNone

    @classmethod
    def _emitter(cls, f):
        """A decorator to mark a method as the one emitting the callbacks.

        This decorator will wrap the method and catch exception. If a
        :class:`StopException` is caught, the listener will be stopped
        gracefully. If any other exception is caught, it will be propagated to
        the thread calling :meth:`join` and reraised there.
        """

        @functools.wrapsf
        def inner(self, *args, **kwargs):
            try:
                return f(self, *args, **kwargs)
                    except Exception as e:
                try:
                    if not isinstance(e, self._HANDLED_EXCEPTIONS):
                        if not isinstance(e, AbstractListener.StopException):
                            self._log.exception'Unhandled exception in listener callback'
                        self._queue.put(None if isinstance(e, cls.StopException) else sys.exc_info)
                        self.stop
                    raise
                finally:
                    e = None
                    del e

        return inner

    def _mark_ready(self):
        """Marks this listener as ready to receive events.

        This method must be called from :meth:`_run`. :meth:`wait` will block
        until this method is called.
        """
        self._condition.acquire
        self._ready = True
        self._condition.notify
        self._condition.release

    def _run(self):
        """The implementation of the :meth:`run` method.

        This is a platform dependent implementation.
        """
        raise NotImplementedError()

    def _stop_platform(self):
        """The implementation of the :meth:`stop` method.

        This is a platform dependent implementation.
        """
        raise NotImplementedError()

    def join(self, *args):
        (super(AbstractListener, self).join)(*args)
        try:
            exc_type, exc_value, exc_traceback = self._queue.get
        except TypeError:
            return
        else:
            six.reraise(exc_type, exc_value, exc_traceback)


class Events(object):
    __doc__ = 'A base class to enable iterating over events.\n    '
    _Listener = None

    class Event(object):

        def __str__(self):
            return '{}({})'.formatself.__class__.__name__', '.join('{}={}'.formatkv for k, v in vars(self).items)

        def __eq__(self, other):
            return self.__class__ == other.__class__ and dir(self) == dir(other) and all((getattr(self, k) == getattr(other, k) for k in dir(self)))

    def __init__(self, *args, **kwargs):
        super(Events, self).__init__
        self._event_queue = queue.Queue
        self._sentinel = object()
        self._listener = (self._Listener)(*args, **)
        self.start = self._listener.start

    def __enter__(self):
        self._listener.__enter__
        return self

    def __exit__(self, *args):
        (self._listener.__exit__)(*args)
        while True:
            try:
                self._event_queue.get_nowait
            except queue.Empty:
                break

        self._event_queue.putself._sentinel

    def __iter__(self):
        return self

    def __next__(self):
        event = self.get
        if event is not None:
            return event
        raise StopIteration()

    def get--- This code section failed: ---

 L. 327         0  SETUP_FINALLY        36  'to 36'

 L. 328         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _event_queue
                6  LOAD_ATTR                get
                8  LOAD_FAST                'timeout'
               10  LOAD_CONST               ('timeout',)
               12  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               14  STORE_FAST               'event'

 L. 329        16  LOAD_FAST                'event'
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                _sentinel
               22  COMPARE_OP               is-not
               24  POP_JUMP_IF_FALSE    30  'to 30'
               26  LOAD_FAST                'event'
               28  JUMP_FORWARD         32  'to 32'
             30_0  COME_FROM            24  '24'
               30  LOAD_CONST               None
             32_0  COME_FROM            28  '28'
               32  POP_BLOCK        
               34  RETURN_VALUE     
             36_0  COME_FROM_FINALLY     0  '0'

 L. 330        36  DUP_TOP          
               38  LOAD_GLOBAL              queue
               40  LOAD_ATTR                Empty
               42  COMPARE_OP               exception-match
               44  POP_JUMP_IF_FALSE    58  'to 58'
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L. 331        52  POP_EXCEPT       
               54  LOAD_CONST               None
               56  RETURN_VALUE     
             58_0  COME_FROM            44  '44'
               58  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 54

    def _event_mapper(self, event):
        """Generates an event callback to transforms the callback arguments to
        an event and then publishes it.

        :param callback event: A function generating an event object.

        :return: a callback
        """

        @functools.wrapsevent
        def inner(*args):
            try:
                self._event_queue.put(event(*args), block=False)
            except queue.Full:
                pass

        return inner


class NotifierMixin(object):
    __doc__ = 'A mixin for notifiers of fake events.\n\n    This mixin can be used for controllers on platforms where sending fake\n    events does not cause a listener to receive a notification.\n    '

    def _emit(self, action, *args):
        """Sends a notification to all registered listeners.

        This method will ensure that listeners that raise
        :class:`StopException` are stopped.

        :param str action: The name of the notification.

        :param args: The arguments to pass.
        """
        stopped = []
        for listener in self._listeners:
            try:
                (getattr(listener, action))(*args)
            except listener.StopException:
                stopped.appendlistener

        else:
            for listener in stopped:
                listener.stop

    @classmethod
    def _receiver(cls, listener_class):
        """A decorator to make a class able to receive fake events from a
        controller.

        This decorator will add the method ``_receive`` to the decorated class.

        This method is a context manager which ensures that all calls to
        :meth:`_emit` will invoke the named method in the listener instance
        while the block is active.
        """

        @contextlib.contextmanager
        def receive(self):
            """Executes a code block with this listener instance registered as
            a receiver of fake input events.
            """
            self._controller_class._add_listenerself
            try:
                yield
            finally:
                self._controller_class._remove_listenerself

        listener_class._receive = receive
        listener_class._controller_class = cls
        if not hasattr(cls, '_listener_cache'):
            cls._listener_cache = set()
            cls._listener_lock = threading.Lock
        return listener_class

    @classmethod
    def _listeners(cls):
        """Iterates over the set of running listeners.

        This method will quit without acquiring the lock if the set is empty,
        so there is potential for race conditions. This is an optimisation,
        since :class:`Controller` will need to call this method for every
        control event.
        """
        if not cls._listener_cache:
            return
        with cls._listener_lock:
            for listener in cls._listener_cache:
                yield listener

    @classmethod
    def _add_listener(cls, listener):
        """Adds a listener to the set of running listeners.

        :param listener: The listener for fake events.
        """
        with cls._listener_lock:
            cls._listener_cache.addlistener

    @classmethod
    def _remove_listener(cls, listener):
        """Removes this listener from the set of running listeners.

        :param listener: The listener for fake events.
        """
        with cls._listener_lock:
            cls._listener_cache.removelistener