# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\mss\base.py
"""
This is part of the MSS Python's module.
Source: https://github.com/BoboTiG/python-mss
"""
from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING
from threading import Lock
from .exception import ScreenShotError
from .screenshot import ScreenShot
from .tools import to_png
if TYPE_CHECKING:
    from typing import Any, Callable, Iterator, List, Optional, Type
    from .models import Monitor, Monitors
lock = Lock()

class MSSBase(metaclass=ABCMeta):
    __doc__ = ' This class will be overloaded by a system specific one. '
    __slots__ = {
     '_monitors', 'cls_image', 'compression_level'}

    def __init__(self):
        self.cls_image = ScreenShot
        self.compression_level = 6
        self._monitors = []

    def __enter__(self):
        """ For the cool call `with MSS() as mss:`. """
        return self

    def __exit__(self, *_):
        """ For the cool call `with MSS() as mss:`. """
        self.close()

    @abstractmethod
    def _grab_impl(self, monitor):
        """
        Retrieve all pixels from a monitor. Pixels have to be RGB.
        That method has to be run using a threading lock.
        """
        pass

    @abstractmethod
    def _monitors_impl(self):
        """
        Get positions of monitors (has to be run using a threading lock).
        It must populate self._monitors.
        """
        pass

    def close(self):
        """ Clean-up. """
        pass

    def grab--- This code section failed: ---

 L.  79         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'monitor'
                4  LOAD_GLOBAL              tuple
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    56  'to 56'

 L.  81        10  LOAD_FAST                'monitor'
               12  LOAD_CONST               0
               14  BINARY_SUBSCR    

 L.  82        16  LOAD_FAST                'monitor'
               18  LOAD_CONST               1
               20  BINARY_SUBSCR    

 L.  83        22  LOAD_FAST                'monitor'
               24  LOAD_CONST               2
               26  BINARY_SUBSCR    
               28  LOAD_FAST                'monitor'
               30  LOAD_CONST               0
               32  BINARY_SUBSCR    
               34  BINARY_SUBTRACT  

 L.  84        36  LOAD_FAST                'monitor'
               38  LOAD_CONST               3
               40  BINARY_SUBSCR    
               42  LOAD_FAST                'monitor'
               44  LOAD_CONST               1
               46  BINARY_SUBSCR    
               48  BINARY_SUBTRACT  

 L.  80        50  LOAD_CONST               ('left', 'top', 'width', 'height')
               52  BUILD_CONST_KEY_MAP_4     4 
               54  STORE_FAST               'monitor'
             56_0  COME_FROM             8  '8'

 L.  87        56  LOAD_GLOBAL              lock
               58  SETUP_WITH           84  'to 84'
               60  POP_TOP          

 L.  88        62  LOAD_FAST                'self'
               64  LOAD_METHOD              _grab_impl
               66  LOAD_FAST                'monitor'
               68  CALL_METHOD_1         1  ''
               70  POP_BLOCK        
               72  ROT_TWO          
               74  BEGIN_FINALLY    
               76  WITH_CLEANUP_START
               78  WITH_CLEANUP_FINISH
               80  POP_FINALLY           0  ''
               82  RETURN_VALUE     
             84_0  COME_FROM_WITH       58  '58'
               84  WITH_CLEANUP_START
               86  WITH_CLEANUP_FINISH
               88  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 72

    @property
    def monitors(self):
        """
        Get positions of all monitors.
        If the monitor has rotation, you have to deal with it
        inside this method.

        This method has to fill self._monitors with all information
        and use it as a cache:
            self._monitors[0] is a dict of all monitors together
            self._monitors[N] is a dict of the monitor N (with N > 0)

        Each monitor is a dict with:
        {
            'left':   the x-coordinate of the upper-left corner,
            'top':    the y-coordinate of the upper-left corner,
            'width':  the width,
            'height': the height
        }
        """
        if not self._monitors:
            with lock:
                self._monitors_impl()
        return self._monitors

    def save(self, mon=0, output='monitor-{mon}.png', callback=None):
        """
        Grab a screen shot and save it to a file.

        :param int mon: The monitor to screen shot (default=0).
                        -1: grab one screen shot of all monitors
                         0: grab one screen shot by monitor
                        N: grab the screen shot of the monitor N

        :param str output: The output filename.

            It can take several keywords to customize the filename:
            - `{mon}`: the monitor number
            - `{top}`: the screen shot y-coordinate of the upper-left corner
            - `{left}`: the screen shot x-coordinate of the upper-left corner
            - `{width}`: the screen shot's width
            - `{height}`: the screen shot's height
            - `{date}`: the current date using the default formatter

            As it is using the `format()` function, you can specify
            formatting options like `{date:%Y-%m-%s}`.

        :param callable callback: Callback called before saving the
            screen shot to a file.  Take the `output` argument as parameter.

        :return generator: Created file(s).
        """
        monitors = self.monitors
        if not monitors:
            raise ScreenShotError('No monitor found.')
        if mon == 0:
            for idx, monitor in enumeratemonitors[1:]1:
                fname = (output.format)(mon=idx, date=datetime.now(), **monitor)
                if callable(callback):
                    callback(fname)
                sct = self.grabmonitor
                to_png((sct.rgb), (sct.size), level=(self.compression_level), output=fname)
                (yield fname)

        else:
            mon = 0 if mon == -1 else mon
        try:
            monitor = monitors[mon]
        except IndexError:
            raise ScreenShotError('Monitor {!r} does not exist.'.formatmon)
        else:
            output = (output.format)(mon=mon, date=datetime.now(), **monitor)
            if callable(callback):
                callback(output)
            sct = self.grabmonitor
            to_png((sct.rgb), (sct.size), level=(self.compression_level), output=output)
            (yield output)

    def shot(self, **kwargs):
        """
        Helper to save the screen shot of the 1st monitor, by default.
        You can pass the same arguments as for ``save``.
        """
        kwargs['mon'] = kwargs.get('mon', 1)
        return next((self.save)(**kwargs))

    @staticmethod
    def _cfactory(attr, func, argtypes, restype, errcheck=None):
        """ Factory to create a ctypes function and automatically manage errors. """
        meth = getattrattrfunc
        meth.argtypes = argtypes
        meth.restype = restype
        if errcheck:
            meth.errcheck = errcheck