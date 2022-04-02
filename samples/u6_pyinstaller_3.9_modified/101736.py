# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: mss\darwin.py
"""
This is part of the MSS Python's module.
Source: https://github.com/BoboTiG/python-mss
"""
import ctypes, ctypes.util, sys
from ctypes import POINTER, Structure, c_double, c_float, c_int32, c_uint64, c_ubyte, c_uint32, c_void_p
from platform import mac_ver
from typing import TYPE_CHECKING
from .base import MSSBase
from .exception import ScreenShotError
from .screenshot import Size
if TYPE_CHECKING:
    from typing import Any, List, Type, Union
    from .models import Monitor, Monitors
    from .screenshot import ScreenShot
__all__ = ('MSS', )

def cgfloat():
    """ Get the appropriate value for a float. """
    if sys.maxsize > 4294967296:
        return c_double
    return c_float


class CGPoint(Structure):
    __doc__ = ' Structure that contains coordinates of a rectangle. '
    _fields_ = [
     (
      'x', cgfloat()), ('y', cgfloat())]

    def __repr__(self):
        return '{}(left={} top={})'.format(type(self).__name__, self.x, self.y)


class CGSize(Structure):
    __doc__ = ' Structure that contains dimensions of an rectangle. '
    _fields_ = [
     (
      'width', cgfloat()), ('height', cgfloat())]

    def __repr__(self):
        return '{}(width={} height={})'.format(type(self).__name__, self.width, self.height)


class CGRect(Structure):
    __doc__ = ' Structure that contains information about a rectangle. '
    _fields_ = [
     (
      'origin', CGPoint), ('size', CGSize)]

    def __repr__(self):
        return '{}<{} {}>'.format(type(self).__name__, self.origin, self.size)


CFUNCTIONS = {'CGDataProviderCopyData':(
  'core', [c_void_p], c_void_p), 
 'CGDisplayBounds':(
  'core', [c_uint32], CGRect), 
 'CGDisplayRotation':(
  'core', [c_uint32], c_float), 
 'CFDataGetBytePtr':(
  'core', [c_void_p], c_void_p), 
 'CFDataGetLength':(
  'core', [c_void_p], c_uint64), 
 'CFRelease':(
  'core', [c_void_p], c_void_p), 
 'CGDataProviderRelease':(
  'core', [c_void_p], c_void_p), 
 'CGGetActiveDisplayList':(
  'core',
  [
   c_uint32, POINTER(c_uint32), POINTER(c_uint32)],
  c_int32), 
 'CGImageGetBitsPerPixel':(
  'core', [c_void_p], int), 
 'CGImageGetBytesPerRow':(
  'core', [c_void_p], int), 
 'CGImageGetDataProvider':(
  'core', [c_void_p], c_void_p), 
 'CGImageGetHeight':(
  'core', [c_void_p], int), 
 'CGImageGetWidth':(
  'core', [c_void_p], int), 
 'CGRectStandardize':(
  'core', [CGRect], CGRect), 
 'CGRectUnion':(
  'core', [CGRect, CGRect], CGRect), 
 'CGWindowListCreateImage':(
  'core',
  [
   CGRect, c_uint32, c_uint32, c_uint32],
  c_void_p)}

class MSS(MSSBase):
    __doc__ = '\n    Multiple ScreenShots implementation for macOS.\n    It uses intensively the CoreGraphics library.\n    '
    __slots__ = {
     'core', 'max_displays'}

    def __init__(self, **_):
        super().__init__()
        self.max_displays = 32
        self._init_library()
        self._set_cfunctions()

    def _init_library(self):
        """ Load the CoreGraphics library. """
        version = float('.'.join(mac_ver()[0].split('.')[:2]))
        if version < 10.16:
            coregraphics = ctypes.util.find_library('CoreGraphics')
        else:
            coregraphics = '/System/Library/Frameworks/CoreGraphics.framework/Versions/Current/CoreGraphics'
        if not coregraphics:
            raise ScreenShotError('No CoreGraphics library found.')
        self.core = ctypes.cdll.LoadLibrary(coregraphics)

    def _set_cfunctions(self):
        """ Set all ctypes functions and attach them to attributes. """
        cfactory = self._cfactory
        attrs = {'core': self.core}
        for func, (attr, argtypes, restype) in CFUNCTIONS.items():
            cfactory(attr=(attrs[attr]),
              func=func,
              argtypes=argtypes,
              restype=restype)

    def _monitors_impl--- This code section failed: ---

 L. 158         0  LOAD_GLOBAL              int
                2  STORE_FAST               'int_'

 L. 159         4  LOAD_FAST                'self'
                6  LOAD_ATTR                core
                8  STORE_FAST               'core'

 L. 164        10  LOAD_GLOBAL              CGRect
               12  CALL_FUNCTION_0       0  ''
               14  STORE_FAST               'all_monitors'

 L. 165        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _monitors
               20  LOAD_METHOD              append
               22  BUILD_MAP_0           0 
               24  CALL_METHOD_1         1  ''
               26  POP_TOP          

 L. 168        28  LOAD_GLOBAL              c_uint32
               30  LOAD_CONST               0
               32  CALL_FUNCTION_1       1  ''
               34  STORE_FAST               'display_count'

 L. 169        36  LOAD_GLOBAL              c_uint32
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                max_displays
               42  BINARY_MULTIPLY  
               44  CALL_FUNCTION_0       0  ''
               46  STORE_FAST               'active_displays'

 L. 170        48  LOAD_FAST                'core'
               50  LOAD_METHOD              CGGetActiveDisplayList

 L. 171        52  LOAD_FAST                'self'
               54  LOAD_ATTR                max_displays
               56  LOAD_FAST                'active_displays'
               58  LOAD_GLOBAL              ctypes
               60  LOAD_METHOD              byref
               62  LOAD_FAST                'display_count'
               64  CALL_METHOD_1         1  ''

 L. 170        66  CALL_METHOD_3         3  ''
               68  POP_TOP          

 L. 173        70  LOAD_STR                 'normal'
               72  LOAD_STR                 'right'
               74  LOAD_STR                 'left'
               76  LOAD_CONST               (0.0, 90.0, -90.0)
               78  BUILD_CONST_KEY_MAP_3     3 
               80  STORE_FAST               'rotations'

 L. 174        82  LOAD_GLOBAL              range
               84  LOAD_FAST                'display_count'
               86  LOAD_ATTR                value
               88  CALL_FUNCTION_1       1  ''
               90  GET_ITER         
               92  FOR_ITER            234  'to 234'
               94  STORE_FAST               'idx'

 L. 175        96  LOAD_FAST                'active_displays'
               98  LOAD_FAST                'idx'
              100  BINARY_SUBSCR    
              102  STORE_FAST               'display'

 L. 176       104  LOAD_FAST                'core'
              106  LOAD_METHOD              CGDisplayBounds
              108  LOAD_FAST                'display'
              110  CALL_METHOD_1         1  ''
              112  STORE_FAST               'rect'

 L. 177       114  LOAD_FAST                'core'
              116  LOAD_METHOD              CGRectStandardize
              118  LOAD_FAST                'rect'
              120  CALL_METHOD_1         1  ''
              122  STORE_FAST               'rect'

 L. 178       124  LOAD_FAST                'rect'
              126  LOAD_ATTR                size
              128  LOAD_ATTR                width
              130  LOAD_FAST                'rect'
              132  LOAD_ATTR                size
              134  LOAD_ATTR                height
              136  ROT_TWO          
              138  STORE_FAST               'width'
              140  STORE_FAST               'height'

 L. 179       142  LOAD_FAST                'core'
              144  LOAD_METHOD              CGDisplayRotation
              146  LOAD_FAST                'display'
              148  CALL_METHOD_1         1  ''
              150  STORE_FAST               'rot'

 L. 180       152  LOAD_FAST                'rotations'
              154  LOAD_FAST                'rot'
              156  BINARY_SUBSCR    
              158  LOAD_CONST               ('left', 'right')
              160  <118>                 0  ''
              162  POP_JUMP_IF_FALSE   174  'to 174'

 L. 181       164  LOAD_FAST                'height'
              166  LOAD_FAST                'width'
              168  ROT_TWO          
              170  STORE_FAST               'width'
              172  STORE_FAST               'height'
            174_0  COME_FROM           162  '162'

 L. 182       174  LOAD_FAST                'self'
              176  LOAD_ATTR                _monitors
              178  LOAD_METHOD              append

 L. 184       180  LOAD_FAST                'int_'
              182  LOAD_FAST                'rect'
              184  LOAD_ATTR                origin
              186  LOAD_ATTR                x
              188  CALL_FUNCTION_1       1  ''

 L. 185       190  LOAD_FAST                'int_'
              192  LOAD_FAST                'rect'
              194  LOAD_ATTR                origin
              196  LOAD_ATTR                y
              198  CALL_FUNCTION_1       1  ''

 L. 186       200  LOAD_FAST                'int_'
              202  LOAD_FAST                'width'
              204  CALL_FUNCTION_1       1  ''

 L. 187       206  LOAD_FAST                'int_'
              208  LOAD_FAST                'height'
              210  CALL_FUNCTION_1       1  ''

 L. 183       212  LOAD_CONST               ('left', 'top', 'width', 'height')
              214  BUILD_CONST_KEY_MAP_4     4 

 L. 182       216  CALL_METHOD_1         1  ''
              218  POP_TOP          

 L. 192       220  LOAD_FAST                'core'
              222  LOAD_METHOD              CGRectUnion
              224  LOAD_FAST                'all_monitors'
              226  LOAD_FAST                'rect'
              228  CALL_METHOD_2         2  ''
              230  STORE_FAST               'all_monitors'
              232  JUMP_BACK            92  'to 92'

 L. 196       234  LOAD_FAST                'int_'
              236  LOAD_FAST                'all_monitors'
              238  LOAD_ATTR                origin
              240  LOAD_ATTR                x
              242  CALL_FUNCTION_1       1  ''

 L. 197       244  LOAD_FAST                'int_'
              246  LOAD_FAST                'all_monitors'
              248  LOAD_ATTR                origin
              250  LOAD_ATTR                y
              252  CALL_FUNCTION_1       1  ''

 L. 198       254  LOAD_FAST                'int_'
              256  LOAD_FAST                'all_monitors'
              258  LOAD_ATTR                size
              260  LOAD_ATTR                width
              262  CALL_FUNCTION_1       1  ''

 L. 199       264  LOAD_FAST                'int_'
              266  LOAD_FAST                'all_monitors'
              268  LOAD_ATTR                size
              270  LOAD_ATTR                height
              272  CALL_FUNCTION_1       1  ''

 L. 195       274  LOAD_CONST               ('left', 'top', 'width', 'height')
              276  BUILD_CONST_KEY_MAP_4     4 
              278  LOAD_FAST                'self'
              280  LOAD_ATTR                _monitors
              282  LOAD_CONST               0
              284  STORE_SUBSCR     

Parse error at or near `<118>' instruction at offset 160

    def _grab_impl--- This code section failed: ---

 L. 208         0  LOAD_FAST                'self'
                2  LOAD_ATTR                core
                4  STORE_FAST               'core'

 L. 209         6  LOAD_GLOBAL              CGRect

 L. 210         8  LOAD_FAST                'monitor'
               10  LOAD_STR                 'left'
               12  BINARY_SUBSCR    
               14  LOAD_FAST                'monitor'
               16  LOAD_STR                 'top'
               18  BINARY_SUBSCR    
               20  BUILD_TUPLE_2         2 
               22  LOAD_FAST                'monitor'
               24  LOAD_STR                 'width'
               26  BINARY_SUBSCR    
               28  LOAD_FAST                'monitor'
               30  LOAD_STR                 'height'
               32  BINARY_SUBSCR    
               34  BUILD_TUPLE_2         2 

 L. 209        36  CALL_FUNCTION_2       2  ''
               38  STORE_FAST               'rect'

 L. 213        40  LOAD_FAST                'core'
               42  LOAD_METHOD              CGWindowListCreateImage
               44  LOAD_FAST                'rect'
               46  LOAD_CONST               1
               48  LOAD_CONST               0
               50  LOAD_CONST               0
               52  CALL_METHOD_4         4  ''
               54  STORE_FAST               'image_ref'

 L. 214        56  LOAD_FAST                'image_ref'
               58  POP_JUMP_IF_TRUE     68  'to 68'

 L. 215        60  LOAD_GLOBAL              ScreenShotError
               62  LOAD_STR                 'CoreGraphics.CGWindowListCreateImage() failed.'
               64  CALL_FUNCTION_1       1  ''
               66  RAISE_VARARGS_1       1  'exception instance'
             68_0  COME_FROM            58  '58'

 L. 217        68  LOAD_FAST                'core'
               70  LOAD_METHOD              CGImageGetWidth
               72  LOAD_FAST                'image_ref'
               74  CALL_METHOD_1         1  ''
               76  STORE_FAST               'width'

 L. 218        78  LOAD_FAST                'core'
               80  LOAD_METHOD              CGImageGetHeight
               82  LOAD_FAST                'image_ref'
               84  CALL_METHOD_1         1  ''
               86  STORE_FAST               'height'

 L. 219        88  LOAD_CONST               None
               90  DUP_TOP          
               92  STORE_FAST               'prov'
               94  STORE_FAST               'copy_data'

 L. 220        96  SETUP_FINALLY       312  'to 312'

 L. 221        98  LOAD_FAST                'core'
              100  LOAD_METHOD              CGImageGetDataProvider
              102  LOAD_FAST                'image_ref'
              104  CALL_METHOD_1         1  ''
              106  STORE_FAST               'prov'

 L. 222       108  LOAD_FAST                'core'
              110  LOAD_METHOD              CGDataProviderCopyData
              112  LOAD_FAST                'prov'
              114  CALL_METHOD_1         1  ''
              116  STORE_FAST               'copy_data'

 L. 223       118  LOAD_FAST                'core'
              120  LOAD_METHOD              CFDataGetBytePtr
              122  LOAD_FAST                'copy_data'
              124  CALL_METHOD_1         1  ''
              126  STORE_FAST               'data_ref'

 L. 224       128  LOAD_FAST                'core'
              130  LOAD_METHOD              CFDataGetLength
              132  LOAD_FAST                'copy_data'
              134  CALL_METHOD_1         1  ''
              136  STORE_FAST               'buf_len'

 L. 225       138  LOAD_GLOBAL              ctypes
              140  LOAD_METHOD              cast
              142  LOAD_FAST                'data_ref'
              144  LOAD_GLOBAL              POINTER
              146  LOAD_GLOBAL              c_ubyte
              148  LOAD_FAST                'buf_len'
              150  BINARY_MULTIPLY  
              152  CALL_FUNCTION_1       1  ''
              154  CALL_METHOD_2         2  ''
              156  STORE_FAST               'raw'

 L. 226       158  LOAD_GLOBAL              bytearray
              160  LOAD_FAST                'raw'
              162  LOAD_ATTR                contents
              164  CALL_FUNCTION_1       1  ''
              166  STORE_FAST               'data'

 L. 229       168  LOAD_FAST                'core'
              170  LOAD_METHOD              CGImageGetBytesPerRow
              172  LOAD_FAST                'image_ref'
              174  CALL_METHOD_1         1  ''
              176  STORE_FAST               'bytes_per_row'

 L. 230       178  LOAD_FAST                'core'
              180  LOAD_METHOD              CGImageGetBitsPerPixel
              182  LOAD_FAST                'image_ref'
              184  CALL_METHOD_1         1  ''
              186  STORE_FAST               'bytes_per_pixel'

 L. 231       188  LOAD_FAST                'bytes_per_pixel'
              190  LOAD_CONST               7
              192  BINARY_ADD       
              194  LOAD_CONST               8
              196  BINARY_FLOOR_DIVIDE
              198  STORE_FAST               'bytes_per_pixel'

 L. 233       200  LOAD_FAST                'bytes_per_pixel'
              202  LOAD_FAST                'width'
              204  BINARY_MULTIPLY  
              206  LOAD_FAST                'bytes_per_row'
              208  COMPARE_OP               !=
          210_212  POP_JUMP_IF_FALSE   276  'to 276'

 L. 234       214  LOAD_GLOBAL              bytearray
              216  CALL_FUNCTION_0       0  ''
              218  STORE_FAST               'cropped'

 L. 235       220  LOAD_GLOBAL              range
              222  LOAD_FAST                'height'
              224  CALL_FUNCTION_1       1  ''
              226  GET_ITER         
              228  FOR_ITER            272  'to 272'
              230  STORE_FAST               'row'

 L. 236       232  LOAD_FAST                'row'
              234  LOAD_FAST                'bytes_per_row'
              236  BINARY_MULTIPLY  
              238  STORE_FAST               'start'

 L. 237       240  LOAD_FAST                'start'
              242  LOAD_FAST                'width'
              244  LOAD_FAST                'bytes_per_pixel'
              246  BINARY_MULTIPLY  
              248  BINARY_ADD       
              250  STORE_FAST               'end'

 L. 238       252  LOAD_FAST                'cropped'
              254  LOAD_METHOD              extend
              256  LOAD_FAST                'data'
              258  LOAD_FAST                'start'
              260  LOAD_FAST                'end'
              262  BUILD_SLICE_2         2 
              264  BINARY_SUBSCR    
              266  CALL_METHOD_1         1  ''
              268  POP_TOP          
              270  JUMP_BACK           228  'to 228'

 L. 239       272  LOAD_FAST                'cropped'
              274  STORE_FAST               'data'
            276_0  COME_FROM           210  '210'
              276  POP_BLOCK        

 L. 241       278  LOAD_FAST                'prov'
          280_282  POP_JUMP_IF_FALSE   294  'to 294'

 L. 242       284  LOAD_FAST                'core'
              286  LOAD_METHOD              CGDataProviderRelease
              288  LOAD_FAST                'prov'
              290  CALL_METHOD_1         1  ''
              292  POP_TOP          
            294_0  COME_FROM           280  '280'

 L. 243       294  LOAD_FAST                'copy_data'
          296_298  POP_JUMP_IF_FALSE   346  'to 346'

 L. 244       300  LOAD_FAST                'core'
              302  LOAD_METHOD              CFRelease
              304  LOAD_FAST                'copy_data'
              306  CALL_METHOD_1         1  ''
              308  POP_TOP          
              310  JUMP_FORWARD        346  'to 346'
            312_0  COME_FROM_FINALLY    96  '96'

 L. 241       312  LOAD_FAST                'prov'
          314_316  POP_JUMP_IF_FALSE   328  'to 328'

 L. 242       318  LOAD_FAST                'core'
              320  LOAD_METHOD              CGDataProviderRelease
              322  LOAD_FAST                'prov'
              324  CALL_METHOD_1         1  ''
              326  POP_TOP          
            328_0  COME_FROM           314  '314'

 L. 243       328  LOAD_FAST                'copy_data'
          330_332  POP_JUMP_IF_FALSE   344  'to 344'

 L. 244       334  LOAD_FAST                'core'
              336  LOAD_METHOD              CFRelease
              338  LOAD_FAST                'copy_data'
              340  CALL_METHOD_1         1  ''
              342  POP_TOP          
            344_0  COME_FROM           330  '330'
              344  <48>             
            346_0  COME_FROM           310  '310'
            346_1  COME_FROM           296  '296'

 L. 246       346  LOAD_FAST                'self'
              348  LOAD_ATTR                cls_image
              350  LOAD_FAST                'data'
              352  LOAD_FAST                'monitor'
              354  LOAD_GLOBAL              Size
              356  LOAD_FAST                'width'
              358  LOAD_FAST                'height'
              360  CALL_FUNCTION_2       2  ''
              362  LOAD_CONST               ('size',)
              364  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              366  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 278