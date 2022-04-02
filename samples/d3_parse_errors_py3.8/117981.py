# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\discord\player.py
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
import threading, traceback, subprocess, audioop, asyncio, logging, shlex, time, json, sys, re
from .errors import ClientException
from .opus import Encoder as OpusEncoder
from .oggparse import OggStream
log = logging.getLogger(__name__)
__all__ = ('AudioSource', 'PCMAudio', 'FFmpegAudio', 'FFmpegPCMAudio', 'FFmpegOpusAudio',
           'PCMVolumeTransformer')

class AudioSource:
    __doc__ = 'Represents an audio stream.\n\n    The audio stream can be Opus encoded or not, however if the audio stream\n    is not Opus encoded then the audio format must be 16-bit 48KHz stereo PCM.\n\n    .. warning::\n\n        The audio source reads are done in a separate thread.\n    '

    def read(self):
        """Reads 20ms worth of audio.

        Subclasses must implement this.

        If the audio is complete, then returning an empty
        :term:`py:bytes-like object` to signal this is the way to do so.

        If :meth:`is_opus` method returns ``True``, then it must return
        20ms worth of Opus encoded audio. Otherwise, it must be 20ms
        worth of 16-bit 48KHz stereo PCM, which is about 3,840 bytes
        per frame (20ms worth of audio).

        Returns
        --------
        :class:`bytes`
            A bytes like object that represents the PCM or Opus data.
        """
        raise NotImplementedError

    def is_opus(self):
        """Checks if the audio source is already encoded in Opus."""
        return False

    def cleanup(self):
        """Called when clean-up is needed to be done.

        Useful for clearing buffer data or processes after
        it is done playing audio.
        """
        pass

    def __del__(self):
        self.cleanup()


class PCMAudio(AudioSource):
    __doc__ = 'Represents raw 16-bit 48KHz stereo PCM audio source.\n\n    Attributes\n    -----------\n    stream: :term:`py:file object`\n        A file-like object that reads byte data representing raw PCM.\n    '

    def __init__(self, stream):
        self.stream = stream

    def read(self):
        ret = self.stream.read(OpusEncoder.FRAME_SIZE)
        if len(ret) != OpusEncoder.FRAME_SIZE:
            return b''
        return ret


class FFmpegAudio(AudioSource):
    __doc__ = 'Represents an FFmpeg (or AVConv) based AudioSource.\n\n    User created AudioSources using FFmpeg differently from how :class:`FFmpegPCMAudio` and\n    :class:`FFmpegOpusAudio` work should subclass this.\n\n    .. versionadded:: 1.3\n    '

    def __init__(self, source, *, executable='ffmpeg', args, **subprocess_kwargs):
        self._process = self._stdout = None
        args = [
         
          executable, *args]
        kwargs = {'stdout': subprocess.PIPE}
        kwargs.update(subprocess_kwargs)
        self._process = (self._spawn_process)(args, **kwargs)
        self._stdout = self._process.stdout

    def _spawn_process(self, args, **subprocess_kwargs):
        process = None
        try:
            process = (subprocess.Popen)(args, **subprocess_kwargs)
        except FileNotFoundError:
            executable = args.partition(' ')[0] if isinstance(args, str) else args[0]
            raise ClientException(executable + ' was not found.') from None
        except subprocess.SubprocessError as exc:
            try:
                raise ClientException('Popen failed: {0.__class__.__name__}: {0}'.format(exc)) from exc
            finally:
                exc = None
                del exc

        else:
            return process

    def cleanup(self):
        proc = self._process
        if proc is None:
            return
        log.info('Preparing to terminate ffmpeg process %s.', proc.pid)
        try:
            proc.kill()
        except Exception:
            log.exception('Ignoring error attempting to kill ffmpeg process %s', proc.pid)
        else:
            if proc.poll() is None:
                log.info('ffmpeg process %s has not terminated. Waiting to terminate...', proc.pid)
                proc.communicate()
                log.info('ffmpeg process %s should have terminated with a return code of %s.', proc.pid, proc.returncode)
            else:
                log.info('ffmpeg process %s successfully terminated with return code of %s.', proc.pid, proc.returncode)
            self._process = self._stdout = None


class FFmpegPCMAudio(FFmpegAudio):
    __doc__ = 'An audio source from FFmpeg (or AVConv).\n\n    This launches a sub-process to a specific input file given.\n\n    .. warning::\n\n        You must have the ffmpeg or avconv executable in your path environment\n        variable in order for this to work.\n\n    Parameters\n    ------------\n    source: Union[:class:`str`, :class:`io.BufferedIOBase`]\n        The input that ffmpeg will take and convert to PCM bytes.\n        If ``pipe`` is True then this is a file-like object that is\n        passed to the stdin of ffmpeg.\n    executable: :class:`str`\n        The executable name (and path) to use. Defaults to ``ffmpeg``.\n    pipe: :class:`bool`\n        If ``True``, denotes that ``source`` parameter will be passed\n        to the stdin of ffmpeg. Defaults to ``False``.\n    stderr: Optional[:term:`py:file object`]\n        A file-like object to pass to the Popen constructor.\n        Could also be an instance of ``subprocess.PIPE``.\n    before_options: Optional[:class:`str`]\n        Extra command line arguments to pass to ffmpeg before the ``-i`` flag.\n    options: Optional[:class:`str`]\n        Extra command line arguments to pass to ffmpeg after the ``-i`` flag.\n\n    Raises\n    --------\n    ClientException\n        The subprocess failed to be created.\n    '

    def __init__(self, source, *, executable='ffmpeg', pipe=False, stderr=None, before_options=None, options=None):
        args = []
        subprocess_kwargs = {'stdin':source if pipe else None,  'stderr':stderr}
        if isinstance(before_options, str):
            args.extend(shlex.split(before_options))
        args.append('-i')
        args.append('-' if pipe else source)
        args.extend(('-f', 's16le', '-ar', '48000', '-ac', '2', '-loglevel', 'warning'))
        if isinstance(options, str):
            args.extend(shlex.split(options))
        args.append('pipe:1')
        (super().__init__)(source, executable=executable, args=args, **subprocess_kwargs)

    def read(self):
        ret = self._stdout.read(OpusEncoder.FRAME_SIZE)
        if len(ret) != OpusEncoder.FRAME_SIZE:
            return b''
        return ret

    def is_opus(self):
        return False


class FFmpegOpusAudio(FFmpegAudio):
    __doc__ = 'An audio source from FFmpeg (or AVConv).\n\n    This launches a sub-process to a specific input file given.  However, rather than\n    producing PCM packets like :class:`FFmpegPCMAudio` does that need to be encoded to\n    opus, this class produces opus packets, skipping the encoding step done by the library.\n\n    Alternatively, instead of instantiating this class directly, you can use\n    :meth:`FFmpegOpusAudio.from_probe` to probe for bitrate and codec information.  This\n    can be used to opportunistically skip pointless re-encoding of existing opus audio data\n    for a boost in performance at the cost of a short initial delay to gather the information.\n    The same can be achieved by passing ``copy`` to the ``codec`` parameter, but only if you\n    know that the input source is opus encoded beforehand.\n\n    .. versionadded:: 1.3\n\n    .. warning::\n\n        You must have the ffmpeg or avconv executable in your path environment\n        variable in order for this to work.\n\n    Parameters\n    ------------\n    source: Union[:class:`str`, :class:`io.BufferedIOBase`]\n        The input that ffmpeg will take and convert to PCM bytes.\n        If ``pipe`` is True then this is a file-like object that is\n        passed to the stdin of ffmpeg.\n    bitrate: :class:`int`\n        The bitrate in kbps to encode the output to.  Defaults to ``128``.\n    codec: Optional[:class:`str`]\n        The codec to use to encode the audio data.  Normally this would be\n        just ``libopus``, but is used by :meth:`FFmpegOpusAudio.from_probe` to\n        opportunistically skip pointlessly re-encoding opus audio data by passing\n        ``copy`` as the codec value.  Any values other than ``copy``, ``opus``, or\n        ``libopus`` will be considered ``libopus``.  Defaults to ``libopus``.\n\n        .. warning::\n\n            Do not provide this parameter unless you are certain that the audio input is\n            already opus encoded.  For typical use :meth:`FFmpegOpusAudio.from_probe`\n            should be used to determine the proper value for this parameter.\n\n    executable: :class:`str`\n        The executable name (and path) to use. Defaults to ``ffmpeg``.\n    pipe: :class:`bool`\n        If ``True``, denotes that ``source`` parameter will be passed\n        to the stdin of ffmpeg. Defaults to ``False``.\n    stderr: Optional[:term:`py:file object`]\n        A file-like object to pass to the Popen constructor.\n        Could also be an instance of ``subprocess.PIPE``.\n    before_options: Optional[:class:`str`]\n        Extra command line arguments to pass to ffmpeg before the ``-i`` flag.\n    options: Optional[:class:`str`]\n        Extra command line arguments to pass to ffmpeg after the ``-i`` flag.\n\n    Raises\n    --------\n    ClientException\n        The subprocess failed to be created.\n    '

    def __init__(self, source, *, bitrate=128, codec=None, executable='ffmpeg', pipe=False, stderr=None, before_options=None, options=None):
        args = []
        subprocess_kwargs = {'stdin':source if pipe else None, 
         'stderr':stderr}
        if isinstance(before_options, str):
            args.extend(shlex.split(before_options))
        args.append('-i')
        args.append('-' if pipe else source)
        codec = 'copy' if codec in ('opus', 'libopus') else 'libopus'
        args.extend(('-map_metadata', '-1',
         '-f', 'opus',
         '-c:a', codec,
         '-ar', '48000',
         '-ac', '2',
         '-b:a', '%sk' % bitrate,
         '-loglevel', 'warning'))
        if isinstance(options, str):
            args.extend(shlex.split(options))
        args.append('pipe:1')
        (super().__init__)(source, executable=executable, args=args, **subprocess_kwargs)
        self._packet_iter = OggStream(self._stdout).iter_packets()

    @classmethod
    async def from_probe(cls, source, *, method=None, **kwargs):
        """|coro|

        A factory method that creates a :class:`FFmpegOpusAudio` after probing
        the input source for audio codec and bitrate information.

        Examples
        ----------

        Use this function to create an :class:`FFmpegOpusAudio` instance instead of the constructor: ::

            source = await discord.FFmpegOpusAudio.from_probe("song.webm")
            voice_client.play(source)

        If you are on Windows and don't have ffprobe installed, use the ``fallback`` method
        to probe using ffmpeg instead: ::

            source = await discord.FFmpegOpusAudio.from_probe("song.webm", method='fallback')
            voice_client.play(source)

        Using a custom method of determining codec and bitrate: ::

            def custom_probe(source, executable):
                # some analysis code here

                return codec, bitrate

            source = await discord.FFmpegOpusAudio.from_probe("song.webm", method=custom_probe)
            voice_client.play(source)

        Parameters
        ------------
        source
            Identical to the ``source`` parameter for the constructor.
        method: Optional[Union[:class:`str`, Callable[:class:`str`, :class:`str`]]]
            The probing method used to determine bitrate and codec information. As a string, valid
            values are ``native`` to use ffprobe (or avprobe) and ``fallback`` to use ffmpeg
            (or avconv).  As a callable, it must take two string arguments, ``source`` and
            ``executable``.  Both parameters are the same values passed to this factory function.
            ``executable`` will default to ``ffmpeg`` if not provided as a keyword argument.
        kwargs
            The remaining parameters to be passed to the :class:`FFmpegOpusAudio` constructor,
            excluding ``bitrate`` and ``codec``.

        Raises
        --------
        AttributeError
            Invalid probe method, must be ``'native'`` or ``'fallback'``.
        TypeError
            Invalid value for ``probe`` parameter, must be :class:`str` or a callable.

        Returns
        --------
        :class:`FFmpegOpusAudio`
            An instance of this class.
        """
        executable = kwargs.get('executable')
        codec, bitrate = await cls.probe(source, method=method, executable=executable)
        return cls(source, bitrate=bitrate, codec=codec, **kwargs)

    @classmethod
    async def probe--- This code section failed: ---

 L. 412         0  LOAD_FAST                'method'
                2  JUMP_IF_TRUE_OR_POP     6  'to 6'
                4  LOAD_STR                 'native'
              6_0  COME_FROM             2  '2'
                6  STORE_FAST               'method'

 L. 413         8  LOAD_DEREF               'executable'
               10  JUMP_IF_TRUE_OR_POP    14  'to 14'
               12  LOAD_STR                 'ffmpeg'
             14_0  COME_FROM            10  '10'
               14  STORE_DEREF              'executable'

 L. 414        16  LOAD_CONST               None
               18  DUP_TOP          
               20  STORE_DEREF              'probefunc'
               22  STORE_DEREF              'fallback'

 L. 416        24  LOAD_GLOBAL              isinstance
               26  LOAD_FAST                'method'
               28  LOAD_GLOBAL              str
               30  CALL_FUNCTION_2       2  ''
               32  POP_JUMP_IF_FALSE    88  'to 88'

 L. 417        34  LOAD_GLOBAL              getattr
               36  LOAD_FAST                'cls'
               38  LOAD_STR                 '_probe_codec_'
               40  LOAD_FAST                'method'
               42  BINARY_ADD       
               44  LOAD_CONST               None
               46  CALL_FUNCTION_3       3  ''
               48  STORE_DEREF              'probefunc'

 L. 418        50  LOAD_DEREF               'probefunc'
               52  LOAD_CONST               None
               54  COMPARE_OP               is
               56  POP_JUMP_IF_FALSE    70  'to 70'

 L. 419        58  LOAD_GLOBAL              AttributeError
               60  LOAD_STR                 "Invalid probe method '%s'"
               62  LOAD_FAST                'method'
               64  BINARY_MODULO    
               66  CALL_FUNCTION_1       1  ''
               68  RAISE_VARARGS_1       1  'exception instance'
             70_0  COME_FROM            56  '56'

 L. 421        70  LOAD_DEREF               'probefunc'
               72  LOAD_FAST                'cls'
               74  LOAD_ATTR                _probe_codec_native
               76  COMPARE_OP               is
               78  POP_JUMP_IF_FALSE   122  'to 122'

 L. 422        80  LOAD_FAST                'cls'
               82  LOAD_ATTR                _probe_codec_fallback
               84  STORE_DEREF              'fallback'
               86  JUMP_FORWARD        122  'to 122'
             88_0  COME_FROM            32  '32'

 L. 424        88  LOAD_GLOBAL              callable
               90  LOAD_FAST                'method'
               92  CALL_FUNCTION_1       1  ''
               94  POP_JUMP_IF_FALSE   108  'to 108'

 L. 425        96  LOAD_FAST                'method'
               98  STORE_DEREF              'probefunc'

 L. 426       100  LOAD_FAST                'cls'
              102  LOAD_ATTR                _probe_codec_fallback
              104  STORE_DEREF              'fallback'
              106  JUMP_FORWARD        122  'to 122'
            108_0  COME_FROM            94  '94'

 L. 428       108  LOAD_GLOBAL              TypeError
              110  LOAD_STR                 "Expected str or callable for parameter 'probe', not '{0.__class__.__name__}'"
              112  LOAD_METHOD              format

 L. 429       114  LOAD_FAST                'method'

 L. 428       116  CALL_METHOD_1         1  ''
              118  CALL_FUNCTION_1       1  ''
              120  RAISE_VARARGS_1       1  'exception instance'
            122_0  COME_FROM           106  '106'
            122_1  COME_FROM            86  '86'
            122_2  COME_FROM            78  '78'

 L. 431       122  LOAD_CONST               None
              124  DUP_TOP          
              126  STORE_FAST               'codec'
              128  STORE_FAST               'bitrate'

 L. 432       130  LOAD_GLOBAL              asyncio
              132  LOAD_METHOD              get_event_loop
              134  CALL_METHOD_0         0  ''
              136  STORE_FAST               'loop'

 L. 433       138  LOAD_CONST               None
              140  SETUP_FINALLY       354  'to 354'
              142  SETUP_FINALLY       182  'to 182'

 L. 434       144  LOAD_FAST                'loop'
              146  LOAD_METHOD              run_in_executor
              148  LOAD_CONST               None
              150  LOAD_CLOSURE             'executable'
              152  LOAD_CLOSURE             'probefunc'
              154  LOAD_CLOSURE             'source'
              156  BUILD_TUPLE_3         3 
              158  LOAD_LAMBDA              '<code_object <lambda>>'
              160  LOAD_STR                 'FFmpegOpusAudio.probe.<locals>.<lambda>'
              162  MAKE_FUNCTION_8          'closure'
              164  CALL_METHOD_2         2  ''
              166  GET_AWAITABLE    
              168  LOAD_CONST               None
              170  YIELD_FROM       
              172  UNPACK_SEQUENCE_2     2 
              174  STORE_FAST               'codec'
              176  STORE_FAST               'bitrate'
              178  POP_BLOCK        
              180  JUMP_FORWARD        336  'to 336'
            182_0  COME_FROM_FINALLY   142  '142'

 L. 435       182  DUP_TOP          
              184  LOAD_GLOBAL              Exception
              186  COMPARE_OP               exception-match
          188_190  POP_JUMP_IF_FALSE   334  'to 334'
              192  POP_TOP          
              194  POP_TOP          
              196  POP_TOP          

 L. 436       198  LOAD_DEREF               'fallback'
              200  POP_JUMP_IF_TRUE    228  'to 228'

 L. 437       202  LOAD_GLOBAL              log
              204  LOAD_METHOD              exception
              206  LOAD_STR                 "Probe '%s' using '%s' failed"
              208  LOAD_FAST                'method'
              210  LOAD_DEREF               'executable'
              212  CALL_METHOD_3         3  ''
              214  POP_TOP          

 L. 438       216  POP_EXCEPT       
              218  POP_BLOCK        
              220  CALL_FINALLY        354  'to 354'
              222  POP_TOP          
              224  LOAD_CONST               None
              226  RETURN_VALUE     
            228_0  COME_FROM           200  '200'

 L. 440       228  LOAD_GLOBAL              log
              230  LOAD_METHOD              exception
              232  LOAD_STR                 "Probe '%s' using '%s' failed, trying fallback"
              234  LOAD_FAST                'method'
              236  LOAD_DEREF               'executable'
              238  CALL_METHOD_3         3  ''
              240  POP_TOP          

 L. 441       242  SETUP_FINALLY       282  'to 282'

 L. 442       244  LOAD_FAST                'loop'
              246  LOAD_METHOD              run_in_executor
              248  LOAD_CONST               None
              250  LOAD_CLOSURE             'executable'
              252  LOAD_CLOSURE             'fallback'
              254  LOAD_CLOSURE             'source'
              256  BUILD_TUPLE_3         3 
              258  LOAD_LAMBDA              '<code_object <lambda>>'
              260  LOAD_STR                 'FFmpegOpusAudio.probe.<locals>.<lambda>'
              262  MAKE_FUNCTION_8          'closure'
              264  CALL_METHOD_2         2  ''
              266  GET_AWAITABLE    
              268  LOAD_CONST               None
              270  YIELD_FROM       
              272  UNPACK_SEQUENCE_2     2 
              274  STORE_FAST               'codec'
              276  STORE_FAST               'bitrate'
              278  POP_BLOCK        
              280  JUMP_FORWARD        316  'to 316'
            282_0  COME_FROM_FINALLY   242  '242'

 L. 443       282  DUP_TOP          
              284  LOAD_GLOBAL              Exception
              286  COMPARE_OP               exception-match
          288_290  POP_JUMP_IF_FALSE   314  'to 314'
              292  POP_TOP          
              294  POP_TOP          
              296  POP_TOP          

 L. 444       298  LOAD_GLOBAL              log
              300  LOAD_METHOD              exception
              302  LOAD_STR                 "Fallback probe using '%s' failed"
              304  LOAD_DEREF               'executable'
              306  CALL_METHOD_2         2  ''
              308  POP_TOP          
              310  POP_EXCEPT       
              312  JUMP_FORWARD        330  'to 330'
            314_0  COME_FROM           288  '288'
              314  END_FINALLY      
            316_0  COME_FROM           280  '280'

 L. 446       316  LOAD_GLOBAL              log
              318  LOAD_METHOD              info
              320  LOAD_STR                 'Fallback probe found codec=%s, bitrate=%s'
              322  LOAD_FAST                'codec'
              324  LOAD_FAST                'bitrate'
              326  CALL_METHOD_3         3  ''
              328  POP_TOP          
            330_0  COME_FROM           312  '312'
              330  POP_EXCEPT       
              332  JUMP_FORWARD        350  'to 350'
            334_0  COME_FROM           188  '188'
              334  END_FINALLY      
            336_0  COME_FROM           180  '180'

 L. 448       336  LOAD_GLOBAL              log
              338  LOAD_METHOD              info
              340  LOAD_STR                 'Probe found codec=%s, bitrate=%s'
              342  LOAD_FAST                'codec'
              344  LOAD_FAST                'bitrate'
              346  CALL_METHOD_3         3  ''
              348  POP_TOP          
            350_0  COME_FROM           332  '332'
              350  POP_BLOCK        
              352  BEGIN_FINALLY    
            354_0  COME_FROM           220  '220'
            354_1  COME_FROM_FINALLY   140  '140'

 L. 450       354  LOAD_FAST                'codec'
              356  LOAD_FAST                'bitrate'
              358  BUILD_TUPLE_2         2 
              360  POP_FINALLY           1  ''
              362  ROT_TWO          
              364  POP_TOP          
              366  RETURN_VALUE     
              368  END_FINALLY      
              370  POP_TOP          

Parse error at or near `POP_BLOCK' instruction at offset 218

    @staticmethod
    def _probe_codec_native(source, executable='ffmpeg'):
        exe = executable[:2] + 'probe' if executable in ('ffmpeg', 'avconv') else executable
        args = [exe, '-v', 'quiet', '-print_format', 'json', '-show_streams', '-select_streams', 'a:0', source]
        output = subprocess.check_output(args, timeout=20)
        codec = bitrate = None
        if output:
            data = json.loads(output)
            streamdata = data['streams'][0]
            codec = streamdata.get('codec_name')
            bitrate = int(streamdata.get('bit_rate', 0))
            bitrate = max(round(bitrate / 1000, 0), 512)
        return (
         codec, bitrate)

    @staticmethod
    def _probe_codec_fallback(source, executable='ffmpeg'):
        args = [executable, '-hide_banner', '-i', source]
        proc = subprocess.Popen(args, stdout=(subprocess.PIPE), stderr=(subprocess.STDOUT))
        out, _ = proc.communicate(timeout=20)
        output = out.decode('utf8')
        codec = bitrate = None
        codec_match = re.search('Stream #0.*?Audio: (\\w+)', output)
        if codec_match:
            codec = codec_match.group(1)
        br_match = re.search('(\\d+) [kK]b/s', output)
        if br_match:
            bitrate = max(int(br_match.group(1)), 512)
        return (
         codec, bitrate)

    def read(self):
        return next(self._packet_iter, b'')

    def is_opus(self):
        return True


class PCMVolumeTransformer(AudioSource):
    __doc__ = 'Transforms a previous :class:`AudioSource` to have volume controls.\n\n    This does not work on audio sources that have :meth:`AudioSource.is_opus`\n    set to ``True``.\n\n    Parameters\n    ------------\n    original: :class:`AudioSource`\n        The original AudioSource to transform.\n    volume: :class:`float`\n        The initial volume to set it to.\n        See :attr:`volume` for more info.\n\n    Raises\n    -------\n    TypeError\n        Not an audio source.\n    ClientException\n        The audio source is opus encoded.\n    '

    def __init__(self, original, volume=1.0):
        if not isinstance(original, AudioSource):
            raise TypeError('expected AudioSource not {0.__class__.__name__}.'.format(original))
        if original.is_opus():
            raise ClientException('AudioSource must not be Opus encoded.')
        self.original = original
        self.volume = volume

    @property
    def volume(self):
        """Retrieves or sets the volume as a floating point percentage (e.g. 1.0 for 100%)."""
        return self._volume

    @volume.setter
    def volume(self, value):
        self._volume = max(value, 0.0)

    def cleanup(self):
        self.original.cleanup()

    def read(self):
        ret = self.original.read()
        return audioop.mul(ret, 2, min(self._volume, 2.0))


class AudioPlayer(threading.Thread):
    DELAY = OpusEncoder.FRAME_LENGTH / 1000.0

    def __init__(self, source, client, *, after=None):
        threading.Thread.__init__(self)
        self.daemon = True
        self.source = source
        self.client = client
        self.after = after
        self._end = threading.Event()
        self._resumed = threading.Event()
        self._resumed.set()
        self._current_error = None
        self._connected = client._connected
        self._lock = threading.Lock()
        if after is not None:
            if not callable(after):
                raise TypeError('Expected a callable for the "after" parameter.')

    def _do_run(self):
        self.loops = 0
        self._start = time.perf_counter()
        play_audio = self.client.send_audio_packet
        self._speak(True)
        while True:
            if not self._end.is_set():
                if not self._resumed.is_set():
                    self._resumed.wait()
                else:
                    if not self._connected.is_set():
                        self._connected.wait()
                        self.loops = 0
                        self._start = time.perf_counter()
                    self.loops += 1
                    data = self.source.read()
                    if not data:
                        self.stop()
                    else:
                        play_audio(data, encode=(not self.source.is_opus()))
                        next_time = self._start + self.DELAY * self.loops
                        delay = max(0, self.DELAY + (next_time - time.perf_counter()))
                        time.sleep(delay)

    def run(self):
        try:
            try:
                self._do_run()
            except Exception as exc:
                try:
                    self._current_error = exc
                    self.stop()
                finally:
                    exc = None
                    del exc

        finally:
            self.source.cleanup()
            self._call_after()

    def _call_after(self):
        error = self._current_error
        if self.after is not None:
            try:
                self.after(error)
            except Exception as exc:
                try:
                    log.exception('Calling the after function failed.')
                    exc.__context__ = error
                    traceback.print_exception(type(exc), exc, exc.__traceback__)
                finally:
                    exc = None
                    del exc

        elif error:
            msg = 'Exception in voice thread {}'.format(self.name)
            log.exception(msg, exc_info=error)
            print(msg, file=(sys.stderr))
            traceback.print_exception(type(error), error, error.__traceback__)

    def stop(self):
        self._end.set()
        self._resumed.set()
        self._speak(False)

    def pause(self, *, update_speaking=True):
        self._resumed.clear()
        if update_speaking:
            self._speak(False)

    def resume(self, *, update_speaking=True):
        self.loops = 0
        self._start = time.perf_counter()
        self._resumed.set()
        if update_speaking:
            self._speak(True)

    def is_playing(self):
        return self._resumed.is_set() and not self._end.is_set()

    def is_paused(self):
        return not self._end.is_set() and not self._resumed.is_set()

    def _set_source(self, source):
        with self._lock:
            self.pause(update_speaking=False)
            self.source = source
            self.resume(update_speaking=False)

    def _speak(self, speaking):
        try:
            asyncio.run_coroutine_threadsafe(self.client.ws.speak(speaking), self.client.loop)
        except Exception as e:
            try:
                log.info('Speaking call in player failed: %s', e)
            finally:
                e = None
                del e