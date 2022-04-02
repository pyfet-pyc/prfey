# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pynput\_util\__init__.py
"""
General utility functions and classes.
"""
import contextlib, functools, sys, threading, six
from six.moves import queue

class AbstractListener(threading.Thread):
    __doc__ = 'A class implementing the basic behaviour for event listeners.\n\n    Instances of this class can be used as context managers. This is equivalent\n    to the following code::\n\n        listener.start()\n        listener.wait()\n        try:\n            with_statements()\n        finally:\n            listener.stop()\n\n    Actual implementations of this class must set the attribute ``_log``, which\n    must be an instance of :class:`logging.Logger`.\n\n    :param bool suppress: Whether to suppress events. Setting this to ``True``\n        will prevent the input events from being passed to the rest of the\n        system.\n\n    :param kwargs: A mapping from callback attribute to callback handler. All\n        handlers will be wrapped in a function reading the return value of the\n        callback, and if it ``is False``, raising :class:`StopException`.\n\n        Any callback that is falsy will be ignored.\n    '

    class StopException(Exception):
        __doc__ = 'If an event listener callback raises this exception, the current\n        listener is stopped.\n        '

    _HANDLED_EXCEPTIONS = tuple()

    def __init__(self, suppress=False, **kwargs):
        super(AbstractListener, self).__init__()

        def wrapper(f):

            def inner(*args):
                if f(*args) is False:
                    raise self.StopException()

            return inner

        self._suppress = suppress
        self._running = False
        self._thread = threading.current_thread()
        self._condition = threading.Condition()
        self._ready = False
        self._queue = queue.Queue(10)
        self.daemon = True
        for name, callback in kwargs.items():
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
            self._queue.put(None)
            self._stop_platform()

    def __enter__(self):
        self.start()
        self.wait()
        return self

    def __exit__(self, exc_type, value, traceback):
        self.stop()

    def wait(self):
        """Waits for this listener to become ready.
        """
        self._condition.acquire()
        while not self._ready:
            self._condition.wait()

        self._condition.release()

    def run(self):
        """The thread runner method.
        """
        self._running = True
        self._thread = threading.current_thread()
        self._run()
        self._queue.put(None)

    @classmethod
    def _emitter(cls, f):
        """A decorator to mark a method as the one emitting the callbacks.

        This decorator will wrap the method and catch exception. If a
        :class:`StopException` is caught, the listener will be stopped
        gracefully. If any other exception is caught, it will be propagated to
        the thread calling :meth:`join` and reraised there.
        """

        @functools.wraps(f)
        def inner(self, *args, **kwargs):
            try:
                return f(self, *args, **kwargs)
                    except Exception as e:
                try:
                    if not isinstance(e, self._HANDLED_EXCEPTIONS):
                        if not isinstance(e, AbstractListener.StopException):
                            self._log.exception('Unhandled exception in listener callback')
                        self._queue.put(None if isinstance(e, cls.StopException) else sys.exc_info())
                        self.stop()
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
        self._condition.acquire()
        self._ready = True
        self._condition.notify()
        self._condition.release()

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
            exc_type, exc_value, exc_traceback = self._queue.get()
        except TypeError:
            return
        else:
            six.reraise(exc_type, exc_value, exc_traceback)


class Events(object):
    __doc__ = 'A base class to enable iterating over events.\n    '
    _Listener = None

    class Event(object):

        def __str__(self):
            return '{}({})'.format(self.__class__.__name__, ', '.join(('{}={}'.format(k, v) for k, v in vars(self))))

        def __eq__(self, other):
            return self.__class__ == other.__class__ and dir(self) == dir(other) and all((getattr(self, k) == getattr(other, k) for k in dir(self)))

    def __init__--- This code section failed: ---

 L. 235         0  LOAD_GLOBAL              super
                2  LOAD_GLOBAL              Events
                4  LOAD_DEREF               'self'
                6  CALL_FUNCTION_2       2  ''
                8  LOAD_METHOD              __init__
               10  CALL_METHOD_0         0  ''
               12  POP_TOP          

 L. 236        14  LOAD_GLOBAL              queue
               16  LOAD_METHOD              Queue
               18  CALL_METHOD_0         0  ''
               20  LOAD_DEREF               'self'
               22  STORE_ATTR               _event_queue

 L. 237        24  LOAD_GLOBAL              object
               26  CALL_FUNCTION_0       0  ''
               28  LOAD_DEREF               'self'
               30  STORE_ATTR               _sentinel

 L. 238        32  LOAD_DEREF               'self'
               34  LOAD_ATTR                _Listener
               36  LOAD_FAST                'args'
               38  LOAD_CLOSURE             'self'
               40  BUILD_TUPLE_1         1 
               42  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               44  LOAD_STR                 'Events.__init__.<locals>.<dictcomp>'
               46  MAKE_FUNCTION_8          'closure'

 L. 240        48  LOAD_FAST                'kwargs'
               50  LOAD_METHOD              items
               52  CALL_METHOD_0         0  ''

 L. 238        54  GET_ITER         
               56  CALL_FUNCTION_1       1  ''
               58  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               60  LOAD_DEREF               'self'
               62  STORE_ATTR               _listener

 L. 241        64  LOAD_DEREF               'self'
               66  LOAD_ATTR                _listener
               68  LOAD_ATTR                start
               70  LOAD_DEREF               'self'
               72  STORE_ATTR               start

Parse error at or near `LOAD_DICTCOMP' instruction at offset 42

    def __enter__(self):
        self._listener.__enter__()
        return self

    def __exit__(self, *args):
        (self._listener.__exit__)(*args)
        while True:
            try:
                self._event_queue.get_nowait()
            except queue.Empty:
                break

        self._event_queue.put(self._sentinel)

    def __iter__(self):
        return self

    def __next__(self):
        event = self.get()
        if event is not None:
            return event
        raise StopIteration()

    def get(self, timeout=None):
        """Attempts to read the next event.

        :param int timeout: An optional timeout. If this is not provided, this
            method may block infinitely.

        :return: The next event, or ``None`` if the source has been stopped
        """
        event = self._event_queue.get(timeout=timeout)
        if event is not self._sentinel:
            return event

    def _event_mapper(self, event):
        """Generates an event callback to transforms the callback arguments to
        an event and then publishes it.

        :param callback event: A function generating an event object.

        :return: a callback
        """

        @functools.wraps(event)
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
        for listener in self._listeners():
            try:
                (getattr(listener, action))(*args)
            except listener.StopException:
                stopped.append(listener)

        else:
            for listener in stopped:
                listener.stop()

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
            self._controller_class._add_listener(self)
            try:
                (yield)
            finally:
                self._controller_class._remove_listener(self)

        listener_class._receive = receive
        listener_class._controller_class = cls
        if not hasattr(cls, '_listener_cache'):
            cls._listener_cache = set()
            cls._listener_lock = threading.Lock()
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
                (yield listener)

    @classmethod
    def _add_listener(cls, listener):
        """Adds a listener to the set of running listeners.

        :param listener: The listener for fake events.
        """
        with cls._listener_lock:
            cls._listener_cache.add(listener)

    @classmethod
    def _remove_listener(cls, listener):
        """Removes this listener from the set of running listeners.

        :param listener: The listener for fake events.
        """
        with cls._listener_lock:
            cls._listener_cache.remove(listener)