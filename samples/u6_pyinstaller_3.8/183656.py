# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\mss\screenshot.py
"""
This is part of the MSS Python's module.
Source: https://github.com/BoboTiG/python-mss
"""
from typing import TYPE_CHECKING
from .models import Size, Pos
from .exception import ScreenShotError
if TYPE_CHECKING:
    from typing import Any, Dict, Iterator, Optional
    from .models import Monitor, Pixel, Pixels

class ScreenShot:
    __doc__ = '\n    Screen shot object.\n\n    .. note::\n\n        A better name would have  been *Image*, but to prevent collisions\n        with PIL.Image, it has been decided to use *ScreenShot*.\n    '
    __slots__ = {
     '__pixels', '__rgb', 'pos', 'raw', 'size'}

    def __init__(self, data, monitor, size=None):
        self._ScreenShot__pixels = None
        self._ScreenShot__rgb = None
        self.raw = data
        self.pos = Pos(monitor['left'], monitor['top'])
        if size is not None:
            self.size = size
        else:
            self.size = Size(monitor['width'], monitor['height'])

    def __repr__(self):
        return '<{!s} pos={cls.left},{cls.top} size={cls.width}x{cls.height}>'.format((type(self).__name__),
          cls=self)

    @property
    def __array_interface__(self):
        """
        Numpy array interface support.
        It uses raw data in BGRA form.

        See https://docs.scipy.org/doc/numpy/reference/arrays.interface.html
        """
        return {'version':3, 
         'shape':(
          self.height, self.width, 4), 
         'typestr':'|u1', 
         'data':self.raw}

    @classmethod
    def from_size(cls, data, width, height):
        """ Instantiate a new class given only screen shot's data and size. """
        monitor = {'left':0, 
         'top':0,  'width':width,  'height':height}
        return cls(data, monitor)

    @property
    def bgra(self):
        """ BGRA values from the BGRA raw pixels. """
        return bytes(self.raw)

    @property
    def height(self):
        """ Convenient accessor to the height size. """
        return self.size.height

    @property
    def left(self):
        """ Convenient accessor to the left position. """
        return self.pos.left

    @property
    def pixels(self):
        """
        :return list: RGB tuples.
        """
        if not self._ScreenShot__pixels:
            rgb_tuples = zip(self.raw[2::4], self.raw[1::4], self.raw[0::4])
            self._ScreenShot__pixels = list(zip(*[iter(rgb_tuples)] * self.width))
        return self._ScreenShot__pixels

    @property
    def rgb(self):
        """
        Compute RGB values from the BGRA raw pixels.

        :return bytes: RGB pixels.
        """
        if not self._ScreenShot__rgb:
            rgb = bytearray(self.height * self.width * 3)
            raw = self.raw
            rgb[0::3] = raw[2::4]
            rgb[1::3] = raw[1::4]
            rgb[2::3] = raw[0::4]
            self._ScreenShot__rgb = bytes(rgb)
        return self._ScreenShot__rgb

    @property
    def top(self):
        """ Convenient accessor to the top position. """
        return self.pos.top

    @property
    def width(self):
        """ Convenient accessor to the width size. """
        return self.size.width

    def pixel--- This code section failed: ---

 L. 152         0  SETUP_FINALLY        18  'to 18'

 L. 153         2  LOAD_FAST                'self'
                4  LOAD_ATTR                pixels
                6  LOAD_FAST                'coord_y'
                8  BINARY_SUBSCR    
               10  LOAD_FAST                'coord_x'
               12  BINARY_SUBSCR    
               14  POP_BLOCK        
               16  RETURN_VALUE     
             18_0  COME_FROM_FINALLY     0  '0'

 L. 154        18  DUP_TOP          
               20  LOAD_GLOBAL              IndexError
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    52  'to 52'
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 155        32  LOAD_GLOBAL              ScreenShotError

 L. 156        34  LOAD_STR                 'Pixel location ({}, {}) is out of range.'
               36  LOAD_METHOD              format
               38  LOAD_FAST                'coord_x'
               40  LOAD_FAST                'coord_y'
               42  CALL_METHOD_2         2  ''

 L. 155        44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  'exception instance'
               48  POP_EXCEPT       
               50  JUMP_FORWARD         54  'to 54'
             52_0  COME_FROM            24  '24'
               52  END_FINALLY      
             54_0  COME_FROM            50  '50'

Parse error at or near `POP_TOP' instruction at offset 28