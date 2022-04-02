# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: selectors.py
"""Selectors module.

This module allows high-level and efficient I/O multiplexing, built upon the
`select` module primitives.
"""
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from collections.abc import Mapping
import math, select, sys
EVENT_READ = 1
EVENT_WRITE = 2

def _fileobj_to_fd(fileobj):
    """Return a file descriptor from a file object.

    Parameters:
    fileobj -- file object or file descriptor

    Returns:
    corresponding file descriptor

    Raises:
    ValueError if the object is invalid
    """
    if isinstance(fileobj, int):
        fd = fileobj
    else:
        try:
            fd = int(fileobj.fileno())
        except (AttributeError, TypeError, ValueError):
            raise ValueError('Invalid file object: {!r}'.format(fileobj)) from None
        else:
            if fd < 0:
                raise ValueError('Invalid file descriptor: {}'.format(fd))
            return fd


SelectorKey = namedtuple('SelectorKey', ['fileobj', 'fd', 'events', 'data'])
SelectorKey.__doc__ = 'SelectorKey(fileobj, fd, events, data)\n\n    Object used to associate a file object to its backing\n    file descriptor, selected event mask, and attached data.\n'
if sys.version_info >= (3, 5):
    SelectorKey.fileobj.__doc__ = 'File object registered.'
    SelectorKey.fd.__doc__ = 'Underlying file descriptor.'
    SelectorKey.events.__doc__ = 'Events that must be waited for on this file object.'
    SelectorKey.data.__doc__ = 'Optional opaque data associated to this file object.\n    For example, this could be used to store a per-client session ID.'
else:

    class _SelectorMapping(Mapping):
        __doc__ = 'Mapping of file objects to selector keys.'

        def __init__(self, selector):
            self._selector = selector

        def __len__(self):
            return len(self._selector._fd_to_key)

        def __getitem__--- This code section failed: ---

 L.  70         0  SETUP_FINALLY        28  'to 28'

 L.  71         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _selector
                6  LOAD_METHOD              _fileobj_lookup
                8  LOAD_FAST                'fileobj'
               10  CALL_METHOD_1         1  ''
               12  STORE_FAST               'fd'

 L.  72        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _selector
               18  LOAD_ATTR                _fd_to_key
               20  LOAD_FAST                'fd'
               22  BINARY_SUBSCR    
               24  POP_BLOCK        
               26  RETURN_VALUE     
             28_0  COME_FROM_FINALLY     0  '0'

 L.  73        28  DUP_TOP          
               30  LOAD_GLOBAL              KeyError
               32  COMPARE_OP               exception-match
               34  POP_JUMP_IF_FALSE    62  'to 62'
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L.  74        42  LOAD_GLOBAL              KeyError
               44  LOAD_STR                 '{!r} is not registered'
               46  LOAD_METHOD              format
               48  LOAD_FAST                'fileobj'
               50  CALL_METHOD_1         1  ''
               52  CALL_FUNCTION_1       1  ''
               54  LOAD_CONST               None
               56  RAISE_VARARGS_2       2  'exception instance with __cause__'
               58  POP_EXCEPT       
               60  JUMP_FORWARD         64  'to 64'
             62_0  COME_FROM            34  '34'
               62  END_FINALLY      
             64_0  COME_FROM            60  '60'

Parse error at or near `POP_TOP' instruction at offset 38

        def __iter__(self):
            return iter(self._selector._fd_to_key)


    class BaseSelector(metaclass=ABCMeta):
        __doc__ = 'Selector abstract base class.\n\n    A selector supports registering file objects to be monitored for specific\n    I/O events.\n\n    A file object is a file descriptor or any object with a `fileno()` method.\n    An arbitrary object can be attached to the file object, which can be used\n    for example to store context information, a callback, etc.\n\n    A selector can use various implementations (select(), poll(), epoll()...)\n    depending on the platform. The default `Selector` class uses the most\n    efficient implementation on the current platform.\n    '

        @abstractmethod
        def register(self, fileobj, events, data=None):
            """Register a file object.

        Parameters:
        fileobj -- file object or file descriptor
        events  -- events to monitor (bitwise mask of EVENT_READ|EVENT_WRITE)
        data    -- attached data

        Returns:
        SelectorKey instance

        Raises:
        ValueError if events is invalid
        KeyError if fileobj is already registered
        OSError if fileobj is closed or otherwise is unacceptable to
                the underlying system call (if a system call is made)

        Note:
        OSError may or may not be raised
        """
            raise NotImplementedError

        @abstractmethod
        def unregister(self, fileobj):
            """Unregister a file object.

        Parameters:
        fileobj -- file object or file descriptor

        Returns:
        SelectorKey instance

        Raises:
        KeyError if fileobj is not registered

        Note:
        If fileobj is registered but has since been closed this does
        *not* raise OSError (even if the wrapped syscall does)
        """
            raise NotImplementedError

        def modify(self, fileobj, events, data=None):
            """Change a registered file object monitored events or attached data.

        Parameters:
        fileobj -- file object or file descriptor
        events  -- events to monitor (bitwise mask of EVENT_READ|EVENT_WRITE)
        data    -- attached data

        Returns:
        SelectorKey instance

        Raises:
        Anything that unregister() or register() raises
        """
            self.unregister(fileobj)
            return self.register(fileobj, events, data)

        @abstractmethod
        def select(self, timeout=None):
            """Perform the actual selection, until some monitored file objects are
        ready or a timeout expires.

        Parameters:
        timeout -- if timeout > 0, this specifies the maximum wait time, in
                   seconds
                   if timeout <= 0, the select() call won't block, and will
                   report the currently ready file objects
                   if timeout is None, select() will block until a monitored
                   file object becomes ready

        Returns:
        list of (key, events) for ready file objects
        `events` is a bitwise mask of EVENT_READ|EVENT_WRITE
        """
            raise NotImplementedError

        def close(self):
            """Close the selector.

        This must be called to make sure that any underlying resource is freed.
        """
            pass

        def get_key--- This code section failed: ---

 L. 186         0  LOAD_FAST                'self'
                2  LOAD_METHOD              get_map
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'mapping'

 L. 187         8  LOAD_FAST                'mapping'
               10  LOAD_CONST               None
               12  COMPARE_OP               is
               14  POP_JUMP_IF_FALSE    24  'to 24'

 L. 188        16  LOAD_GLOBAL              RuntimeError
               18  LOAD_STR                 'Selector is closed'
               20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            14  '14'

 L. 189        24  SETUP_FINALLY        36  'to 36'

 L. 190        26  LOAD_FAST                'mapping'
               28  LOAD_FAST                'fileobj'
               30  BINARY_SUBSCR    
               32  POP_BLOCK        
               34  RETURN_VALUE     
             36_0  COME_FROM_FINALLY    24  '24'

 L. 191        36  DUP_TOP          
               38  LOAD_GLOBAL              KeyError
               40  COMPARE_OP               exception-match
               42  POP_JUMP_IF_FALSE    70  'to 70'
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L. 192        50  LOAD_GLOBAL              KeyError
               52  LOAD_STR                 '{!r} is not registered'
               54  LOAD_METHOD              format
               56  LOAD_FAST                'fileobj'
               58  CALL_METHOD_1         1  ''
               60  CALL_FUNCTION_1       1  ''
               62  LOAD_CONST               None
               64  RAISE_VARARGS_2       2  'exception instance with __cause__'
               66  POP_EXCEPT       
               68  JUMP_FORWARD         72  'to 72'
             70_0  COME_FROM            42  '42'
               70  END_FINALLY      
             72_0  COME_FROM            68  '68'

Parse error at or near `POP_TOP' instruction at offset 46

        @abstractmethod
        def get_map(self):
            """Return a mapping of file objects to selector keys."""
            raise NotImplementedError

        def __enter__(self):
            return self

        def __exit__(self, *args):
            self.close()


    class _BaseSelectorImpl(BaseSelector):
        __doc__ = 'Base selector implementation.'

        def __init__(self):
            self._fd_to_key = {}
            self._map = _SelectorMapping(self)

        def _fileobj_lookup--- This code section failed: ---

 L. 224         0  SETUP_FINALLY        12  'to 12'

 L. 225         2  LOAD_GLOBAL              _fileobj_to_fd
                4  LOAD_FAST                'fileobj'
                6  CALL_FUNCTION_1       1  ''
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L. 226        12  DUP_TOP          
               14  LOAD_GLOBAL              ValueError
               16  COMPARE_OP               exception-match
               18  POP_JUMP_IF_FALSE    72  'to 72'
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L. 228        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _fd_to_key
               30  LOAD_METHOD              values
               32  CALL_METHOD_0         0  ''
               34  GET_ITER         
             36_0  COME_FROM            48  '48'
               36  FOR_ITER             66  'to 66'
               38  STORE_FAST               'key'

 L. 229        40  LOAD_FAST                'key'
               42  LOAD_ATTR                fileobj
               44  LOAD_FAST                'fileobj'
               46  COMPARE_OP               is
               48  POP_JUMP_IF_FALSE    36  'to 36'

 L. 230        50  LOAD_FAST                'key'
               52  LOAD_ATTR                fd
               54  ROT_TWO          
               56  POP_TOP          
               58  ROT_FOUR         
               60  POP_EXCEPT       
               62  RETURN_VALUE     
               64  JUMP_BACK            36  'to 36'

 L. 232        66  RAISE_VARARGS_0       0  'reraise'
               68  POP_EXCEPT       
               70  JUMP_FORWARD         74  'to 74'
             72_0  COME_FROM            18  '18'
               72  END_FINALLY      
             74_0  COME_FROM            70  '70'

Parse error at or near `POP_TOP' instruction at offset 22

        def register(self, fileobj, events, data=None):
            if not events or events & ~(EVENT_READ | EVENT_WRITE):
                raise ValueError('Invalid events: {!r}'.format(events))
            key = SelectorKey(fileobj, self._fileobj_lookup(fileobj), events, data)
            if key.fd in self._fd_to_key:
                raise KeyError('{!r} (FD {}) is already registered'.format(fileobj, key.fd))
            self._fd_to_key[key.fd] = key
            return key

        def unregister(self, fileobj):
            try:
                key = self._fd_to_key.pop(self._fileobj_lookup(fileobj))
            except KeyError:
                raise KeyError('{!r} is not registered'.format(fileobj)) from None
            else:
                return key

        def modify(self, fileobj, events, data=None):
            try:
                key = self._fd_to_key[self._fileobj_lookup(fileobj)]
            except KeyError:
                raise KeyError('{!r} is not registered'.format(fileobj)) from None
            else:
                if events != key.events:
                    self.unregister(fileobj)
                    key = self.register(fileobj, events, data)
                else:
                    if data != key.data:
                        key = key._replace(data=data)
                        self._fd_to_key[key.fd] = key
                return key

        def close(self):
            self._fd_to_key.clear()
            self._map = None

        def get_map(self):
            return self._map

        def _key_from_fd--- This code section failed: ---

 L. 284         0  SETUP_FINALLY        14  'to 14'

 L. 285         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _fd_to_key
                6  LOAD_FAST                'fd'
                8  BINARY_SUBSCR    
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 286        14  DUP_TOP          
               16  LOAD_GLOBAL              KeyError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    34  'to 34'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 287        28  POP_EXCEPT       
               30  LOAD_CONST               None
               32  RETURN_VALUE     
             34_0  COME_FROM            20  '20'
               34  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 24


    class SelectSelector(_BaseSelectorImpl):
        __doc__ = 'Select-based selector.'

        def __init__(self):
            super().__init__()
            self._readers = set()
            self._writers = set()

        def register(self, fileobj, events, data=None):
            key = super().register(fileobj, events, data)
            if events & EVENT_READ:
                self._readers.add(key.fd)
            if events & EVENT_WRITE:
                self._writers.add(key.fd)
            return key

        def unregister(self, fileobj):
            key = super().unregister(fileobj)
            self._readers.discard(key.fd)
            self._writers.discard(key.fd)
            return key

        if sys.platform == 'win32':

            def _select(self, r, w, _, timeout=None):
                r, w, x = select.select(r, w, w, timeout)
                return (r, w + x, [])

        else:
            _select = select.select

        def select(self, timeout=None):
            timeout = None if timeout is None else max(timeout, 0)
            ready = []
            try:
                r, w, _ = self._select(self._readers, self._writers, [], timeout)
            except InterruptedError:
                return ready
            else:
                r = set(r)
                w = set(w)
                for fd in r | w:
                    events = 0
                    if fd in r:
                        events |= EVENT_READ
                    if fd in w:
                        events |= EVENT_WRITE
                    key = self._key_from_fd(fd)
                    if key:
                        ready.append((key, events & key.events))
                    return ready


    class _PollLikeSelector(_BaseSelectorImpl):
        __doc__ = 'Base class shared between poll, epoll and devpoll selectors.'
        _selector_cls = None
        _EVENT_READ = None
        _EVENT_WRITE = None

        def __init__(self):
            super().__init__()
            self._selector = self._selector_cls()

        def register(self, fileobj, events, data=None):
            key = super().register(fileobj, events, data)
            poller_events = 0
            if events & EVENT_READ:
                poller_events |= self._EVENT_READ
            if events & EVENT_WRITE:
                poller_events |= self._EVENT_WRITE
            try:
                self._selector.register(key.fd, poller_events)
            except:
                super().unregister(fileobj)
                raise
            else:
                return key

        def unregister(self, fileobj):
            key = super().unregister(fileobj)
            try:
                self._selector.unregister(key.fd)
            except OSError:
                pass
            else:
                return key

        def modify(self, fileobj, events, data=None):
            try:
                key = self._fd_to_key[self._fileobj_lookup(fileobj)]
            except KeyError:
                raise KeyError(f"{fileobj!r} is not registered") from None
            else:
                changed = False
                if events != key.events:
                    selector_events = 0
                    if events & EVENT_READ:
                        selector_events |= self._EVENT_READ
                    if events & EVENT_WRITE:
                        selector_events |= self._EVENT_WRITE
                    try:
                        self._selector.modify(key.fd, selector_events)
                    except:
                        super().unregister(fileobj)
                        raise
                    else:
                        changed = True
                if data != key.data:
                    changed = True
                if changed:
                    key = key._replace(events=events, data=data)
                    self._fd_to_key[key.fd] = key
                return key

        def select(self, timeout=None):
            if timeout is None:
                timeout = None
            else:
                if timeout <= 0:
                    timeout = 0
                else:
                    timeout = math.ceil(timeout * 1000.0)
            ready = []
            try:
                fd_event_list = self._selector.poll(timeout)
            except InterruptedError:
                return ready
            else:
                for fd, event in fd_event_list:
                    events = 0
                    if event & ~self._EVENT_READ:
                        events |= EVENT_WRITE
                    if event & ~self._EVENT_WRITE:
                        events |= EVENT_READ
                    key = self._key_from_fd(fd)
                    if key:
                        ready.append((key, events & key.events))
                    return ready


    if hasattr(select, 'poll'):

        class PollSelector(_PollLikeSelector):
            __doc__ = 'Poll-based selector.'
            _selector_cls = select.poll
            _EVENT_READ = select.POLLIN
            _EVENT_WRITE = select.POLLOUT


    elif hasattr(select, 'epoll'):

        class EpollSelector(_PollLikeSelector):
            __doc__ = 'Epoll-based selector.'
            _selector_cls = select.epoll
            _EVENT_READ = select.EPOLLIN
            _EVENT_WRITE = select.EPOLLOUT

            def fileno(self):
                return self._selector.fileno()

            def select(self, timeout=None):
                if timeout is None:
                    timeout = -1
                else:
                    if timeout <= 0:
                        timeout = 0
                    else:
                        timeout = math.ceil(timeout * 1000.0) * 0.001
                max_ev = max(len(self._fd_to_key), 1)
                ready = []
                try:
                    fd_event_list = self._selector.poll(timeout, max_ev)
                except InterruptedError:
                    return ready
                else:
                    for fd, event in fd_event_list:
                        events = 0
                        if event & ~select.EPOLLIN:
                            events |= EVENT_WRITE
                        if event & ~select.EPOLLOUT:
                            events |= EVENT_READ
                        key = self._key_from_fd(fd)
                        if key:
                            ready.append((key, events & key.events))
                        return ready

            def close(self):
                self._selector.close()
                super().close()


    elif hasattr(select, 'devpoll'):

        class DevpollSelector(_PollLikeSelector):
            __doc__ = 'Solaris /dev/poll selector.'
            _selector_cls = select.devpoll
            _EVENT_READ = select.POLLIN
            _EVENT_WRITE = select.POLLOUT

            def fileno(self):
                return self._selector.fileno()

            def close(self):
                self._selector.close()
                super().close()


    else:
        if hasattr(select, 'kqueue'):

            class KqueueSelector(_BaseSelectorImpl):
                __doc__ = 'Kqueue-based selector.'

                def __init__(self):
                    super().__init__()
                    self._selector = select.kqueue()

                def fileno(self):
                    return self._selector.fileno()

                def register(self, fileobj, events, data=None):
                    key = super().register(fileobj, events, data)
                    try:
                        if events & EVENT_READ:
                            kev = select.kevent(key.fd, select.KQ_FILTER_READ, select.KQ_EV_ADD)
                            self._selector.control([kev], 0, 0)
                        if events & EVENT_WRITE:
                            kev = select.kevent(key.fd, select.KQ_FILTER_WRITE, select.KQ_EV_ADD)
                            self._selector.control([kev], 0, 0)
                    except:
                        super().unregister(fileobj)
                        raise
                    else:
                        return key

                def unregister(self, fileobj):
                    key = super().unregister(fileobj)
                    if key.events & EVENT_READ:
                        kev = select.kevent(key.fd, select.KQ_FILTER_READ, select.KQ_EV_DELETE)
                        try:
                            self._selector.control([kev], 0, 0)
                        except OSError:
                            pass

                    if key.events & EVENT_WRITE:
                        kev = select.kevent(key.fd, select.KQ_FILTER_WRITE, select.KQ_EV_DELETE)
                        try:
                            self._selector.control([kev], 0, 0)
                        except OSError:
                            pass

                    return key

                def select(self, timeout=None):
                    timeout = None if timeout is None else max(timeout, 0)
                    max_ev = len(self._fd_to_key)
                    ready = []
                    try:
                        kev_list = self._selector.control(None, max_ev, timeout)
                    except InterruptedError:
                        return ready
                    else:
                        for kev in kev_list:
                            fd = kev.ident
                            flag = kev.filter
                            events = 0
                            if flag == select.KQ_FILTER_READ:
                                events |= EVENT_READ
                            if flag == select.KQ_FILTER_WRITE:
                                events |= EVENT_WRITE
                            key = self._key_from_fd(fd)
                            if key:
                                ready.append((key, events & key.events))
                            return ready

                def close(self):
                    self._selector.close()
                    super().close()


        if 'KqueueSelector' in globals():
            DefaultSelector = KqueueSelector
        else:
            if 'EpollSelector' in globals():
                DefaultSelector = EpollSelector
            else:
                if 'DevpollSelector' in globals():
                    DefaultSelector = DevpollSelector
                else:
                    if 'PollSelector' in globals():
                        DefaultSelector = PollSelector
                    else:
                        DefaultSelector = SelectSelector