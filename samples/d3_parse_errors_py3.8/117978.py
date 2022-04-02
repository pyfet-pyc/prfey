# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\discord\opus.py
"""
The MIT License (MIT)

Copyright (c) 2015-2020 Rapptz

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
import array, ctypes, ctypes.util, logging, os.path, sys
from .errors import DiscordException
log = logging.getLogger(__name__)
c_int_ptr = ctypes.POINTER(ctypes.c_int)
c_int16_ptr = ctypes.POINTER(ctypes.c_int16)
c_float_ptr = ctypes.POINTER(ctypes.c_float)
_lib = None

class EncoderStruct(ctypes.Structure):
    pass


EncoderStructPtr = ctypes.POINTER(EncoderStruct)

def _err_lt(result, func, args):
    if result < 0:
        log.info('error has happened in %s', func.__name__)
        raise OpusError(result)
    return result


def _err_ne(result, func, args):
    ret = args[(-1)]._obj
    if ret.value != 0:
        log.info('error has happened in %s', func.__name__)
        raise OpusError(ret.value)
    return result


exported_functions = [
 (
  'opus_strerror',
  [
   ctypes.c_int], ctypes.c_char_p, None),
 (
  'opus_encoder_get_size',
  [
   ctypes.c_int], ctypes.c_int, None),
 (
  'opus_encoder_create',
  [
   ctypes.c_int, ctypes.c_int, ctypes.c_int, c_int_ptr], EncoderStructPtr, _err_ne),
 (
  'opus_encode',
  [
   EncoderStructPtr, c_int16_ptr, ctypes.c_int, ctypes.c_char_p, ctypes.c_int32], ctypes.c_int32, _err_lt),
 (
  'opus_encoder_ctl',
  None, ctypes.c_int32, _err_lt),
 (
  'opus_encoder_destroy',
  [
   EncoderStructPtr], None, None)]

def libopus_loader--- This code section failed: ---

 L.  83         0  LOAD_GLOBAL              ctypes
                2  LOAD_ATTR                cdll
                4  LOAD_METHOD              LoadLibrary
                6  LOAD_FAST                'name'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'lib'

 L.  86        12  LOAD_GLOBAL              exported_functions
               14  GET_ITER         
             16_0  COME_FROM           144  '144'
             16_1  COME_FROM           140  '140'
             16_2  COME_FROM           110  '110'
               16  FOR_ITER            146  'to 146'
               18  STORE_FAST               'item'

 L.  87        20  LOAD_GLOBAL              getattr
               22  LOAD_FAST                'lib'
               24  LOAD_FAST                'item'
               26  LOAD_CONST               0
               28  BINARY_SUBSCR    
               30  CALL_FUNCTION_2       2  ''
               32  STORE_FAST               'func'

 L.  89        34  SETUP_FINALLY        68  'to 68'

 L.  90        36  LOAD_FAST                'item'
               38  LOAD_CONST               1
               40  BINARY_SUBSCR    
               42  POP_JUMP_IF_FALSE    54  'to 54'

 L.  91        44  LOAD_FAST                'item'
               46  LOAD_CONST               1
               48  BINARY_SUBSCR    
               50  LOAD_FAST                'func'
               52  STORE_ATTR               argtypes
             54_0  COME_FROM            42  '42'

 L.  93        54  LOAD_FAST                'item'
               56  LOAD_CONST               2
               58  BINARY_SUBSCR    
               60  LOAD_FAST                'func'
               62  STORE_ATTR               restype
               64  POP_BLOCK        
               66  JUMP_FORWARD         88  'to 88'
             68_0  COME_FROM_FINALLY    34  '34'

 L.  94        68  DUP_TOP          
               70  LOAD_GLOBAL              KeyError
               72  COMPARE_OP               exception-match
               74  POP_JUMP_IF_FALSE    86  'to 86'
               76  POP_TOP          
               78  POP_TOP          
               80  POP_TOP          

 L.  95        82  POP_EXCEPT       
               84  BREAK_LOOP           88  'to 88'
             86_0  COME_FROM            74  '74'
               86  END_FINALLY      
             88_0  COME_FROM            84  '84'
             88_1  COME_FROM            66  '66'

 L.  97        88  SETUP_FINALLY       112  'to 112'

 L.  98        90  LOAD_FAST                'item'
               92  LOAD_CONST               3
               94  BINARY_SUBSCR    
               96  POP_JUMP_IF_FALSE   108  'to 108'

 L.  99        98  LOAD_FAST                'item'
              100  LOAD_CONST               3
              102  BINARY_SUBSCR    
              104  LOAD_FAST                'func'
              106  STORE_ATTR               errcheck
            108_0  COME_FROM            96  '96'
              108  POP_BLOCK        
              110  JUMP_BACK            16  'to 16'
            112_0  COME_FROM_FINALLY    88  '88'

 L. 100       112  DUP_TOP          
              114  LOAD_GLOBAL              KeyError
              116  COMPARE_OP               exception-match
              118  POP_JUMP_IF_FALSE   142  'to 142'
              120  POP_TOP          
              122  POP_TOP          
              124  POP_TOP          

 L. 101       126  LOAD_GLOBAL              log
              128  LOAD_METHOD              exception
              130  LOAD_STR                 'Error assigning check function to %s'
              132  LOAD_FAST                'func'
              134  CALL_METHOD_2         2  ''
              136  POP_TOP          
              138  POP_EXCEPT       
              140  JUMP_BACK            16  'to 16'
            142_0  COME_FROM           118  '118'
              142  END_FINALLY      
              144  JUMP_BACK            16  'to 16'
            146_0  COME_FROM            16  '16'

 L. 103       146  LOAD_FAST                'lib'
              148  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `END_FINALLY' instruction at offset 86


def _load_default():
    global _lib
    try:
        if sys.platform == 'win32':
            _basedir = os.path.dirname(os.path.abspath(__file__))
            _bitness = 'x64' if sys.maxsize > 4294967296 else 'x86'
            _filename = os.path.join(_basedir, 'bin', 'libopus-0.{}.dll'.format(_bitness))
            _lib = libopus_loader(_filename)
        else:
            _lib = libopus_loader(ctypes.util.find_library('opus'))
    except Exception:
        _lib = None
    else:
        return _lib is not None


def load_opus(name):
    """Loads the libopus shared library for use with voice.

    If this function is not called then the library uses the function
    :func:`ctypes.util.find_library` and then loads that one if available.

    Not loading a library and attempting to use PCM based AudioSources will
    lead to voice not working.

    This function propagates the exceptions thrown.

    .. warning::

        The bitness of the library must match the bitness of your python
        interpreter. If the library is 64-bit then your python interpreter
        must be 64-bit as well. Usually if there's a mismatch in bitness then
        the load will throw an exception.

    .. note::

        On Windows, this function should not need to be called as the binaries
        are automatically loaded.

    .. note::

        On Windows, the .dll extension is not necessary. However, on Linux
        the full extension is required to load the library, e.g. ``libopus.so.1``.
        On Linux however, :func:`ctypes.util.find_library` will usually find the library automatically
        without you having to call this.

    Parameters
    ----------
    name: :class:`str`
        The filename of the shared library.
    """
    global _lib
    _lib = libopus_loader(name)


def is_loaded():
    """Function to check if opus lib is successfully loaded either
    via the :func:`ctypes.util.find_library` call of :func:`load_opus`.

    This must return ``True`` for voice to work.

    Returns
    -------
    :class:`bool`
        Indicates if the opus library has been loaded.
    """
    return _lib is not None


class OpusError(DiscordException):
    __doc__ = 'An exception that is thrown for libopus related errors.\n\n    Attributes\n    ----------\n    code: :class:`int`\n        The error code returned.\n    '

    def __init__(self, code):
        self.code = code
        msg = _lib.opus_strerror(self.code).decode('utf-8')
        log.info('"%s" has happened', msg)
        super().__init__(msg)


class OpusNotLoaded(DiscordException):
    __doc__ = 'An exception that is thrown for when libopus is not loaded.'


OK = 0
APPLICATION_AUDIO = 2049
APPLICATION_VOIP = 2048
APPLICATION_LOWDELAY = 2051
CTL_SET_BITRATE = 4002
CTL_SET_BANDWIDTH = 4008
CTL_SET_FEC = 4012
CTL_SET_PLP = 4014
CTL_SET_SIGNAL = 4024
band_ctl = {'narrow':1101, 
 'medium':1102, 
 'wide':1103, 
 'superwide':1104, 
 'full':1105}
signal_ctl = {'auto':-1000, 
 'voice':3001, 
 'music':3002}

class Encoder:
    SAMPLING_RATE = 48000
    CHANNELS = 2
    FRAME_LENGTH = 20
    SAMPLE_SIZE = 4
    SAMPLES_PER_FRAME = int(SAMPLING_RATE / 1000 * FRAME_LENGTH)
    FRAME_SIZE = SAMPLES_PER_FRAME * SAMPLE_SIZE

    def __init__(self, application=APPLICATION_AUDIO):
        self.application = application
        if not is_loaded():
            if not _load_default():
                raise OpusNotLoaded()
        self._state = self._create_state()
        self.set_bitrate(128)
        self.set_fec(True)
        self.set_expected_packet_loss_percent(0.15)
        self.set_bandwidth('full')
        self.set_signal_type('auto')

    def __del__(self):
        if hasattr(self, '_state'):
            _lib.opus_encoder_destroy(self._state)
            self._state = None

    def _create_state(self):
        ret = ctypes.c_int()
        return _lib.opus_encoder_create(self.SAMPLING_RATE, self.CHANNELS, self.application, ctypes.byref(ret))

    def set_bitrate(self, kbps):
        kbps = min(512, max(16, int(kbps)))
        _lib.opus_encoder_ctl(self._state, CTL_SET_BITRATE, kbps * 1024)
        return kbps

    def set_bandwidth(self, req):
        if req not in band_ctl:
            raise KeyError('%r is not a valid bandwidth setting. Try one of: %s' % (req, ','.join(band_ctl)))
        k = band_ctl[req]
        _lib.opus_encoder_ctl(self._state, CTL_SET_BANDWIDTH, k)

    def set_signal_type(self, req):
        if req not in signal_ctl:
            raise KeyError('%r is not a valid signal setting. Try one of: %s' % (req, ','.join(signal_ctl)))
        k = signal_ctl[req]
        _lib.opus_encoder_ctl(self._state, CTL_SET_SIGNAL, k)

    def set_fec(self, enabled=True):
        _lib.opus_encoder_ctl(self._state, CTL_SET_FEC, 1 if enabled else 0)

    def set_expected_packet_loss_percent(self, percentage):
        _lib.opus_encoder_ctl(self._state, CTL_SET_PLP, min(100, max(0, int(percentage * 100))))

    def encode(self, pcm, frame_size):
        max_data_bytes = len(pcm)
        pcm = ctypes.cast(pcm, c_int16_ptr)
        data = (ctypes.c_char * max_data_bytes)()
        ret = _lib.opus_encode(self._state, pcm, frame_size, data, max_data_bytes)
        return array.array('b', data[:ret]).tobytes()