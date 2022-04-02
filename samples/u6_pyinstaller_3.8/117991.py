# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\discord\voice_client.py
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
import asyncio, socket, logging, struct, threading
from . import opus
from .backoff import ExponentialBackoff
from .gateway import *
from .errors import ClientException, ConnectionClosed
from .player import AudioPlayer, AudioSource
try:
    import nacl.secret
    has_nacl = True
except ImportError:
    has_nacl = False
else:
    log = logging.getLogger(__name__)

    class VoiceClient:
        __doc__ = 'Represents a Discord voice connection.\n\n    You do not create these, you typically get them from\n    e.g. :meth:`VoiceChannel.connect`.\n\n    Warning\n    --------\n    In order to use PCM based AudioSources, you must have the opus library\n    installed on your system and loaded through :func:`opus.load_opus`.\n    Otherwise, your AudioSources must be opus encoded (e.g. using :class:`FFmpegOpusAudio`)\n    or the library will not be able to transmit audio.\n\n    Attributes\n    -----------\n    session_id: :class:`str`\n        The voice connection session ID.\n    token: :class:`str`\n        The voice connection token.\n    endpoint: :class:`str`\n        The endpoint we are connecting to.\n    channel: :class:`abc.Connectable`\n        The voice channel connected to.\n    loop: :class:`asyncio.AbstractEventLoop`\n        The event loop that the voice client is running on.\n    '

        def __init__(self, state, timeout, channel):
            if not has_nacl:
                raise RuntimeError('PyNaCl library needed in order to use voice')
            self.channel = channel
            self.main_ws = None
            self.timeout = timeout
            self.ws = None
            self.socket = None
            self.loop = state.loop
            self._state = state
            self._connected = threading.Event()
            self._handshaking = False
            self._handshake_check = asyncio.Lock()
            self._handshake_complete = asyncio.Event()
            self.mode = None
            self._connections = 0
            self.sequence = 0
            self.timestamp = 0
            self._runner = None
            self._player = None
            self.encoder = None
            self._lite_nonce = 0

        warn_nacl = not has_nacl
        supported_modes = ('xsalsa20_poly1305_lite', 'xsalsa20_poly1305_suffix', 'xsalsa20_poly1305')

        @property
        def guild(self):
            """Optional[:class:`Guild`]: The guild we're connected to, if applicable."""
            return getattr(self.channel, 'guild', None)

        @property
        def user(self):
            """:class:`ClientUser`: The user connected to voice (i.e. ourselves)."""
            return self._state.user

        def checked_add(self, attr, value, limit):
            val = getattr(self, attr)
            if val + value > limit:
                setattr(self, attr, 0)
            else:
                setattr(self, attr, val + value)

        async def start_handshake(self):
            log.info('Starting voice handshake...')
            guild_id, channel_id = self.channel._get_voice_state_pair()
            state = self._state
            self.main_ws = ws = state._get_websocket(guild_id)
            self._connections += 1
            await ws.voice_state(guild_id, channel_id)
            try:
                await asyncio.wait_for((self._handshake_complete.wait()), timeout=(self.timeout))
            except asyncio.TimeoutError:
                await self.terminate_handshake(remove=True)
                raise
            else:
                log.info('Voice handshake complete. Endpoint found %s (IP: %s)', self.endpoint, self.endpoint_ip)

        async def terminate_handshake(self, *, remove=False):
            guild_id, channel_id = self.channel._get_voice_state_pair()
            self._handshake_complete.clear()
            await self.main_ws.voice_state(guild_id, None, self_mute=True)
            log.info('The voice handshake is being terminated for Channel ID %s (Guild ID %s)', channel_id, guild_id)
            if remove:
                log.info('The voice client has been removed for Channel ID %s (Guild ID %s)', channel_id, guild_id)
                key_id, _ = self.channel._get_voice_client_key()
                self._state._remove_voice_client(key_id)

        async def _create_socket--- This code section failed: ---

 L. 173         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _handshake_check
                4  BEFORE_ASYNC_WITH
                6  GET_AWAITABLE    
                8  LOAD_CONST               None
               10  YIELD_FROM       
               12  SETUP_ASYNC_WITH     62  'to 62'
               14  POP_TOP          

 L. 174        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _handshaking
               20  POP_JUMP_IF_FALSE    52  'to 52'

 L. 175        22  LOAD_GLOBAL              log
               24  LOAD_METHOD              info
               26  LOAD_STR                 'Ignoring voice server update while handshake is in progress'
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L. 176        32  POP_BLOCK        
               34  BEGIN_FINALLY    
               36  WITH_CLEANUP_START
               38  GET_AWAITABLE    
               40  LOAD_CONST               None
               42  YIELD_FROM       
               44  WITH_CLEANUP_FINISH
               46  POP_FINALLY           0  ''
               48  LOAD_CONST               None
               50  RETURN_VALUE     
             52_0  COME_FROM            20  '20'

 L. 177        52  LOAD_CONST               True
               54  LOAD_FAST                'self'
               56  STORE_ATTR               _handshaking
               58  POP_BLOCK        
               60  BEGIN_FINALLY    
             62_0  COME_FROM_ASYNC_WITH    12  '12'
               62  WITH_CLEANUP_START
               64  GET_AWAITABLE    
               66  LOAD_CONST               None
               68  YIELD_FROM       
               70  WITH_CLEANUP_FINISH
               72  END_FINALLY      

 L. 179        74  LOAD_FAST                'self'
               76  LOAD_ATTR                _connected
               78  LOAD_METHOD              clear
               80  CALL_METHOD_0         0  ''
               82  POP_TOP          

 L. 180        84  LOAD_FAST                'self'
               86  LOAD_ATTR                main_ws
               88  LOAD_ATTR                session_id
               90  LOAD_FAST                'self'
               92  STORE_ATTR               session_id

 L. 181        94  LOAD_FAST                'server_id'
               96  LOAD_FAST                'self'
               98  STORE_ATTR               server_id

 L. 182       100  LOAD_FAST                'data'
              102  LOAD_METHOD              get
              104  LOAD_STR                 'token'
              106  CALL_METHOD_1         1  ''
              108  LOAD_FAST                'self'
              110  STORE_ATTR               token

 L. 183       112  LOAD_FAST                'data'
              114  LOAD_METHOD              get
              116  LOAD_STR                 'endpoint'
              118  CALL_METHOD_1         1  ''
              120  STORE_FAST               'endpoint'

 L. 185       122  LOAD_FAST                'endpoint'
              124  LOAD_CONST               None
              126  COMPARE_OP               is
              128  POP_JUMP_IF_TRUE    140  'to 140'
              130  LOAD_FAST                'self'
              132  LOAD_ATTR                token
              134  LOAD_CONST               None
              136  COMPARE_OP               is
              138  POP_JUMP_IF_FALSE   154  'to 154'
            140_0  COME_FROM           128  '128'

 L. 186       140  LOAD_GLOBAL              log
              142  LOAD_METHOD              warning
              144  LOAD_STR                 'Awaiting endpoint... This requires waiting. If timeout occurred considering raising the timeout and reconnecting.'
              146  CALL_METHOD_1         1  ''
              148  POP_TOP          

 L. 188       150  LOAD_CONST               None
              152  RETURN_VALUE     
            154_0  COME_FROM           138  '138'

 L. 190       154  LOAD_FAST                'endpoint'
              156  LOAD_METHOD              replace
              158  LOAD_STR                 ':80'
              160  LOAD_STR                 ''
              162  CALL_METHOD_2         2  ''
              164  LOAD_FAST                'self'
              166  STORE_ATTR               endpoint

 L. 191       168  LOAD_GLOBAL              socket
              170  LOAD_METHOD              gethostbyname
              172  LOAD_FAST                'self'
              174  LOAD_ATTR                endpoint
              176  CALL_METHOD_1         1  ''
              178  LOAD_FAST                'self'
              180  STORE_ATTR               endpoint_ip

 L. 193       182  LOAD_FAST                'self'
              184  LOAD_ATTR                socket
              186  POP_JUMP_IF_FALSE   224  'to 224'

 L. 194       188  SETUP_FINALLY       204  'to 204'

 L. 195       190  LOAD_FAST                'self'
              192  LOAD_ATTR                socket
              194  LOAD_METHOD              close
              196  CALL_METHOD_0         0  ''
              198  POP_TOP          
              200  POP_BLOCK        
              202  JUMP_FORWARD        224  'to 224'
            204_0  COME_FROM_FINALLY   188  '188'

 L. 196       204  DUP_TOP          
              206  LOAD_GLOBAL              Exception
              208  COMPARE_OP               exception-match
              210  POP_JUMP_IF_FALSE   222  'to 222'
              212  POP_TOP          
              214  POP_TOP          
              216  POP_TOP          

 L. 197       218  POP_EXCEPT       
              220  JUMP_FORWARD        224  'to 224'
            222_0  COME_FROM           210  '210'
              222  END_FINALLY      
            224_0  COME_FROM           220  '220'
            224_1  COME_FROM           202  '202'
            224_2  COME_FROM           186  '186'

 L. 199       224  LOAD_GLOBAL              socket
              226  LOAD_METHOD              socket
              228  LOAD_GLOBAL              socket
              230  LOAD_ATTR                AF_INET
              232  LOAD_GLOBAL              socket
              234  LOAD_ATTR                SOCK_DGRAM
              236  CALL_METHOD_2         2  ''
              238  LOAD_FAST                'self'
              240  STORE_ATTR               socket

 L. 200       242  LOAD_FAST                'self'
              244  LOAD_ATTR                socket
              246  LOAD_METHOD              setblocking
              248  LOAD_CONST               False
              250  CALL_METHOD_1         1  ''
              252  POP_TOP          

 L. 202       254  LOAD_FAST                'self'
              256  LOAD_ATTR                _handshake_complete
              258  LOAD_METHOD              is_set
              260  CALL_METHOD_0         0  ''
          262_264  POP_JUMP_IF_FALSE   298  'to 298'

 L. 204       266  LOAD_FAST                'self'
              268  LOAD_ATTR                _handshake_complete
              270  LOAD_METHOD              clear
              272  CALL_METHOD_0         0  ''
              274  POP_TOP          

 L. 205       276  LOAD_FAST                'self'
              278  LOAD_ATTR                ws
              280  LOAD_METHOD              close
              282  LOAD_CONST               4000
              284  CALL_METHOD_1         1  ''
              286  GET_AWAITABLE    
              288  LOAD_CONST               None
              290  YIELD_FROM       
              292  POP_TOP          

 L. 206       294  LOAD_CONST               None
              296  RETURN_VALUE     
            298_0  COME_FROM           262  '262'

 L. 208       298  LOAD_FAST                'self'
              300  LOAD_ATTR                _handshake_complete
              302  LOAD_METHOD              set
              304  CALL_METHOD_0         0  ''
              306  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 34

        async def connect(self, *, reconnect=True, _tries=0, do_handshake=True):
            log.info('Connecting to voice...')
            try:
                del self.secret_key
            except AttributeError:
                pass
            else:
                if do_handshake:
                    await self.start_handshake()
                try:
                    self.ws = await DiscordVoiceWebSocket.from_client(self)
                    self._handshaking = False
                    self._connected.clear()
                    while not hasattr(self, 'secret_key'):
                        await self.ws.poll_event()

                    self._connected.set()
                except (ConnectionClosed, asyncio.TimeoutError):
                    if reconnect and _tries < 5:
                        log.exception('Failed to connect to voice... Retrying...')
                        await asyncio.sleep(1 + _tries * 2.0)
                        await self.terminate_handshake()
                        await self.connect(reconnect=reconnect, _tries=(_tries + 1))
                    else:
                        raise
                else:
                    if self._runner is None:
                        self._runner = self.loop.create_task(self.poll_voice_ws(reconnect))

        async def poll_voice_ws--- This code section failed: ---

 L. 240         0  LOAD_GLOBAL              ExponentialBackoff
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'backoff'

 L. 242         6  SETUP_FINALLY        28  'to 28'

 L. 243         8  LOAD_FAST                'self'
               10  LOAD_ATTR                ws
               12  LOAD_METHOD              poll_event
               14  CALL_METHOD_0         0  ''
               16  GET_AWAITABLE    
               18  LOAD_CONST               None
               20  YIELD_FROM       
               22  POP_TOP          
               24  POP_BLOCK        
               26  JUMP_BACK             6  'to 6'
             28_0  COME_FROM_FINALLY     6  '6'

 L. 244        28  DUP_TOP          
               30  LOAD_GLOBAL              ConnectionClosed
               32  LOAD_GLOBAL              asyncio
               34  LOAD_ATTR                TimeoutError
               36  BUILD_TUPLE_2         2 
               38  COMPARE_OP               exception-match
            40_42  POP_JUMP_IF_FALSE   272  'to 272'
               44  POP_TOP          
               46  STORE_FAST               'exc'
               48  POP_TOP          
               50  SETUP_FINALLY       260  'to 260'

 L. 245        52  LOAD_GLOBAL              isinstance
               54  LOAD_FAST                'exc'
               56  LOAD_GLOBAL              ConnectionClosed
               58  CALL_FUNCTION_2       2  ''
               60  POP_JUMP_IF_FALSE   110  'to 110'

 L. 250        62  LOAD_FAST                'exc'
               64  LOAD_ATTR                code
               66  LOAD_CONST               (1000, 4014, 4015)
               68  COMPARE_OP               in
               70  POP_JUMP_IF_FALSE   110  'to 110'

 L. 251        72  LOAD_GLOBAL              log
               74  LOAD_METHOD              info
               76  LOAD_STR                 'Disconnecting from voice normally, close code %d.'
               78  LOAD_FAST                'exc'
               80  LOAD_ATTR                code
               82  CALL_METHOD_2         2  ''
               84  POP_TOP          

 L. 252        86  LOAD_FAST                'self'
               88  LOAD_METHOD              disconnect
               90  CALL_METHOD_0         0  ''
               92  GET_AWAITABLE    
               94  LOAD_CONST               None
               96  YIELD_FROM       
               98  POP_TOP          

 L. 253       100  POP_BLOCK        
              102  POP_EXCEPT       
              104  CALL_FINALLY        260  'to 260'
          106_108  BREAK_LOOP          276  'to 276'
            110_0  COME_FROM            70  '70'
            110_1  COME_FROM            60  '60'

 L. 255       110  LOAD_FAST                'reconnect'
              112  POP_JUMP_IF_TRUE    130  'to 130'

 L. 256       114  LOAD_FAST                'self'
              116  LOAD_METHOD              disconnect
              118  CALL_METHOD_0         0  ''
              120  GET_AWAITABLE    
              122  LOAD_CONST               None
              124  YIELD_FROM       
              126  POP_TOP          

 L. 257       128  RAISE_VARARGS_0       0  'reraise'
            130_0  COME_FROM           112  '112'

 L. 259       130  LOAD_FAST                'backoff'
              132  LOAD_METHOD              delay
              134  CALL_METHOD_0         0  ''
              136  STORE_FAST               'retry'

 L. 260       138  LOAD_GLOBAL              log
              140  LOAD_METHOD              exception
              142  LOAD_STR                 'Disconnected from voice... Reconnecting in %.2fs.'
              144  LOAD_FAST                'retry'
              146  CALL_METHOD_2         2  ''
              148  POP_TOP          

 L. 261       150  LOAD_FAST                'self'
              152  LOAD_ATTR                _connected
              154  LOAD_METHOD              clear
              156  CALL_METHOD_0         0  ''
              158  POP_TOP          

 L. 262       160  LOAD_GLOBAL              asyncio
              162  LOAD_METHOD              sleep
              164  LOAD_FAST                'retry'
              166  CALL_METHOD_1         1  ''
              168  GET_AWAITABLE    
              170  LOAD_CONST               None
              172  YIELD_FROM       
              174  POP_TOP          

 L. 263       176  LOAD_FAST                'self'
              178  LOAD_METHOD              terminate_handshake
              180  CALL_METHOD_0         0  ''
              182  GET_AWAITABLE    
              184  LOAD_CONST               None
              186  YIELD_FROM       
              188  POP_TOP          

 L. 264       190  SETUP_FINALLY       214  'to 214'

 L. 265       192  LOAD_FAST                'self'
              194  LOAD_ATTR                connect
              196  LOAD_CONST               True
              198  LOAD_CONST               ('reconnect',)
              200  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              202  GET_AWAITABLE    
              204  LOAD_CONST               None
              206  YIELD_FROM       
              208  POP_TOP          
              210  POP_BLOCK        
              212  JUMP_FORWARD        256  'to 256'
            214_0  COME_FROM_FINALLY   190  '190'

 L. 266       214  DUP_TOP          
              216  LOAD_GLOBAL              asyncio
              218  LOAD_ATTR                TimeoutError
              220  COMPARE_OP               exception-match
              222  POP_JUMP_IF_FALSE   254  'to 254'
              224  POP_TOP          
              226  POP_TOP          
              228  POP_TOP          

 L. 268       230  LOAD_GLOBAL              log
              232  LOAD_METHOD              warning
              234  LOAD_STR                 'Could not connect to voice... Retrying...'
              236  CALL_METHOD_1         1  ''
              238  POP_TOP          

 L. 269       240  POP_EXCEPT       
              242  POP_BLOCK        
              244  POP_EXCEPT       
              246  CALL_FINALLY        260  'to 260'
              248  JUMP_BACK             6  'to 6'
              250  POP_EXCEPT       
              252  JUMP_FORWARD        256  'to 256'
            254_0  COME_FROM           222  '222'
              254  END_FINALLY      
            256_0  COME_FROM           252  '252'
            256_1  COME_FROM           212  '212'
              256  POP_BLOCK        
              258  BEGIN_FINALLY    
            260_0  COME_FROM           246  '246'
            260_1  COME_FROM           104  '104'
            260_2  COME_FROM_FINALLY    50  '50'
              260  LOAD_CONST               None
              262  STORE_FAST               'exc'
              264  DELETE_FAST              'exc'
              266  END_FINALLY      
              268  POP_EXCEPT       
              270  JUMP_BACK             6  'to 6'
            272_0  COME_FROM            40  '40'
              272  END_FINALLY      
              274  JUMP_BACK             6  'to 6'

Parse error at or near `POP_EXCEPT' instruction at offset 102

        async def disconnect(self, *, force=False):
            """|coro|

        Disconnects this voice client from voice.
        """
            if not force:
                if not self.is_connected():
                    return
            self.stop()
            self._connected.clear()
            try:
                if self.ws:
                    await self.ws.close()
                await self.terminate_handshake(remove=True)
            finally:
                if self.socket:
                    self.socket.close()

        async def move_to(self, channel):
            """|coro|

        Moves you to a different voice channel.

        Parameters
        -----------
        channel: :class:`abc.Snowflake`
            The channel to move to. Must be a voice channel.
        """
            guild_id, _ = self.channel._get_voice_state_pair()
            await self.main_ws.voice_state(guild_id, channel.id)

        def is_connected(self):
            """Indicates if the voice client is connected to voice."""
            return self._connected.is_set()

        def _get_voice_packet(self, data):
            header = bytearray(12)
            header[0] = 128
            header[1] = 120
            struct.pack_into('>H', header, 2, self.sequence)
            struct.pack_into('>I', header, 4, self.timestamp)
            struct.pack_into('>I', header, 8, self.ssrc)
            encrypt_packet = getattr(self, '_encrypt_' + self.mode)
            return encrypt_packet(header, data)

        def _encrypt_xsalsa20_poly1305(self, header, data):
            box = nacl.secret.SecretBox(bytes(self.secret_key))
            nonce = bytearray(24)
            nonce[:12] = header
            return header + box.encrypt(bytes(data), bytes(nonce)).ciphertext

        def _encrypt_xsalsa20_poly1305_suffix(self, header, data):
            box = nacl.secret.SecretBox(bytes(self.secret_key))
            nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
            return header + box.encrypt(bytes(data), nonce).ciphertext + nonce

        def _encrypt_xsalsa20_poly1305_lite(self, header, data):
            box = nacl.secret.SecretBox(bytes(self.secret_key))
            nonce = bytearray(24)
            nonce[:4] = struct.pack('>I', self._lite_nonce)
            self.checked_add('_lite_nonce', 1, 4294967295)
            return header + box.encrypt(bytes(data), bytes(nonce)).ciphertext + nonce[:4]

        def play(self, source, *, after=None):
            """Plays an :class:`AudioSource`.

        The finalizer, ``after`` is called after the source has been exhausted
        or an error occurred.

        If an error happens while the audio player is running, the exception is
        caught and the audio player is then stopped.  If no after callback is
        passed, any caught exception will be displayed as if it were raised.

        Parameters
        -----------
        source: :class:`AudioSource`
            The audio source we're reading from.
        after: Callable[[:class:`Exception`], Any]
            The finalizer that is called after the stream is exhausted.
            This function must have a single parameter, ``error``, that
            denotes an optional exception that was raised during playing.

        Raises
        -------
        ClientException
            Already playing audio or not connected.
        TypeError
            Source is not a :class:`AudioSource` or after is not a callable.
        OpusNotLoaded
            Source is not opus encoded and opus is not loaded.
        """
            if not self.is_connected():
                raise ClientException('Not connected to voice.')
            elif self.is_playing():
                raise ClientException('Already playing audio.')
            else:
                if not isinstance(source, AudioSource):
                    raise TypeError('source must an AudioSource not {0.__class__.__name__}'.format(source))
                self.encoder = self.encoder or source.is_opus() or opus.Encoder()
            self._player = AudioPlayer(source, self, after=after)
            self._player.start()

        def is_playing(self):
            """Indicates if we're currently playing audio."""
            return self._player is not None and self._player.is_playing()

        def is_paused(self):
            """Indicates if we're playing audio, but if we're paused."""
            return self._player is not None and self._player.is_paused()

        def stop(self):
            """Stops playing audio."""
            if self._player:
                self._player.stop()
                self._player = None

        def pause(self):
            """Pauses the audio playing."""
            if self._player:
                self._player.pause()

        def resume(self):
            """Resumes the audio playing."""
            if self._player:
                self._player.resume()

        @property
        def source(self):
            """Optional[:class:`AudioSource`]: The audio source being played, if playing.

        This property can also be used to change the audio source currently being played.
        """
            if self._player:
                return self._player.source

        @source.setter
        def source(self, value):
            if not isinstance(value, AudioSource):
                raise TypeError('expected AudioSource not {0.__class__.__name__}.'.format(value))
            if self._player is None:
                raise ValueError('Not playing anything.')
            self._player._set_source(value)

        def send_audio_packet(self, data, *, encode=True):
            """Sends an audio packet composed of the data.

        You must be connected to play audio.

        Parameters
        ----------
        data: :class:`bytes`
            The :term:`py:bytes-like object` denoting PCM or Opus voice data.
        encode: :class:`bool`
            Indicates if ``data`` should be encoded into Opus.

        Raises
        -------
        ClientException
            You are not connected.
        opus.OpusError
            Encoding the data failed.
        """
            self.checked_add('sequence', 1, 65535)
            if encode:
                encoded_data = self.encoder.encode(data, self.encoder.SAMPLES_PER_FRAME)
            else:
                encoded_data = data
            packet = self._get_voice_packet(encoded_data)
            try:
                self.socket.sendto(packet, (self.endpoint_ip, self.voice_port))
            except BlockingIOError:
                log.warning('A packet has been dropped (seq: %s, timestamp: %s)', self.sequence, self.timestamp)
            else:
                self.checked_add('timestamp', opus.Encoder.SAMPLES_PER_FRAME, 4294967295)