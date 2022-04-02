# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\html5lib\_inputstream.py
from __future__ import absolute_import, division, unicode_literals
from six import text_type, binary_type
from six.moves import http_client, urllib
import codecs, re, webencodings
from .constants import EOF, spaceCharacters, asciiLetters, asciiUppercase
from .constants import _ReparseException
from . import _utils
from io import StringIO
try:
    from io import BytesIO
except ImportError:
    BytesIO = StringIO
else:
    spaceCharactersBytes = frozenset([item.encode('ascii') for item in spaceCharacters])
    asciiLettersBytes = frozenset([item.encode('ascii') for item in asciiLetters])
    asciiUppercaseBytes = frozenset([item.encode('ascii') for item in asciiUppercase])
    spacesAngleBrackets = spaceCharactersBytes | frozenset([b'>', b'<'])
    invalid_unicode_no_surrogate = '[\x01-\x08\x0b\x0e-\x1f\x7f-\x9f\ufdd0-\ufdef\ufffe\uffff\U0001fffe\U0001ffff\U0002fffe\U0002ffff\U0003fffe\U0003ffff\U0004fffe\U0004ffff\U0005fffe\U0005ffff\U0006fffe\U0006ffff\U0007fffe\U0007ffff\U0008fffe\U0008ffff\U0009fffe\U0009ffff\U000afffe\U000affff\U000bfffe\U000bffff\U000cfffe\U000cffff\U000dfffe\U000dffff\U000efffe\U000effff\U000ffffe\U000fffff\U0010fffe\U0010ffff]'
    if _utils.supports_lone_surrogates:
        if not (invalid_unicode_no_surrogate[(-1)] == ']' and invalid_unicode_no_surrogate.count(']') == 1):
            raise AssertionError
        invalid_unicode_re = re.compile(invalid_unicode_no_surrogate[:-1] + eval('"\\uD800-\\uDFFF"') + ']')
    else:
        invalid_unicode_re = re.compile(invalid_unicode_no_surrogate)
    non_bmp_invalid_codepoints = set([131070, 131071, 196606, 196607, 262142,
     262143, 327678, 327679, 393214, 393215,
     458750, 458751, 524286, 524287, 589822,
     589823, 655358, 655359, 720894, 720895,
     786430, 786431, 851966, 851967, 917502,
     917503, 983038, 983039, 1048574, 1048575,
     1114110, 1114111])
    ascii_punctuation_re = re.compile('[\t-\r -/:-@\\[-`{-~]')
    charsUntilRegEx = {}

    class BufferedStream(object):
        __doc__ = 'Buffering for streams that do not have buffering of their own\n\n    The buffer is implemented as a list of chunks on the assumption that\n    joining many strings will be slow since it is O(n**2)\n    '

        def __init__(self, stream):
            self.stream = stream
            self.buffer = []
            self.position = [-1, 0]

        def tell(self):
            pos = 0
            for chunk in self.buffer[:self.position[0]]:
                pos += len(chunk)
            else:
                pos += self.position[1]
                return pos

        def seek(self, pos):
            assert pos <= self._bufferedBytes()
            offset = pos
            i = 0
            while True:
                if len(self.buffer[i]) < offset:
                    offset -= len(self.buffer[i])
                    i += 1

            self.position = [
             i, offset]

        def read(self, bytes):
            if not self.buffer:
                return self._readStream(bytes)
            if self.position[0] == len(self.buffer):
                if self.position[1] == len(self.buffer[(-1)]):
                    return self._readStream(bytes)
            return self._readFromBuffer(bytes)

        def _bufferedBytes(self):
            return sum([len(item) for item in self.buffer])

        def _readStream(self, bytes):
            data = self.stream.read(bytes)
            self.buffer.append(data)
            self.position[0] += 1
            self.position[1] = len(data)
            return data

        def _readFromBuffer(self, bytes):
            remainingBytes = bytes
            rv = []
            bufferIndex = self.position[0]
            bufferOffset = self.position[1]
            while bufferIndex < len(self.buffer):
                if remainingBytes != 0:
                    if not remainingBytes > 0:
                        raise AssertionError
                    else:
                        bufferedData = self.buffer[bufferIndex]
                        if remainingBytes <= len(bufferedData) - bufferOffset:
                            bytesToRead = remainingBytes
                            self.position = [bufferIndex, bufferOffset + bytesToRead]
                        else:
                            bytesToRead = len(bufferedData) - bufferOffset
                            self.position = [bufferIndex, len(bufferedData)]
                            bufferIndex += 1
                        rv.append(bufferedData[bufferOffset:bufferOffset + bytesToRead])
                        remainingBytes -= bytesToRead
                        bufferOffset = 0

            if remainingBytes:
                rv.append(self._readStream(remainingBytes))
            return (b'').join(rv)


    def HTMLInputStream(source, **kwargs):
        if not isinstance(source, http_client.HTTPResponse):
            if not isinstance(source, urllib.response.addbase) or isinstance(source.fp, http_client.HTTPResponse):
                isUnicode = False
            elif hasattr(source, 'read'):
                isUnicode = isinstance(source.read(0), text_type)
            else:
                isUnicode = isinstance(source, text_type)
            if isUnicode:
                encodings = [x for x in kwargs if x.endswith('_encoding')]
                if encodings:
                    raise TypeError('Cannot set an encoding with a unicode input, set %r' % encodings)
                return HTMLUnicodeInputStream(source, **kwargs)
            return HTMLBinaryInputStream(source, **kwargs)


    class HTMLUnicodeInputStream(object):
        __doc__ = 'Provides a unicode stream of characters to the HTMLTokenizer.\n\n    This class takes care of character encoding and removing or replacing\n    incorrect byte-sequences and also provides column and line tracking.\n\n    '
        _defaultChunkSize = 10240

        def __init__(self, source):
            """Initialises the HTMLInputStream.

        HTMLInputStream(source, [encoding]) -> Normalized stream from source
        for use by html5lib.

        source can be either a file-object, local filename or a string.

        The optional encoding parameter must be a string that indicates
        the encoding.  If specified, that encoding will be used,
        regardless of any BOM or later declaration (such as in a meta
        element)

        """
            if not _utils.supports_lone_surrogates:
                self.reportCharacterErrors = None
            elif len('\U0010ffff') == 1:
                self.reportCharacterErrors = self.characterErrorsUCS4
            else:
                self.reportCharacterErrors = self.characterErrorsUCS2
            self.newLines = [
             0]
            self.charEncoding = (
             lookupEncoding('utf-8'), 'certain')
            self.dataStream = self.openStream(source)
            self.reset()

        def reset(self):
            self.chunk = ''
            self.chunkSize = 0
            self.chunkOffset = 0
            self.errors = []
            self.prevNumLines = 0
            self.prevNumCols = 0
            self._bufferedCharacter = None

        def openStream(self, source):
            """Produces a file object from source.

        source can be either a file object, local filename or a string.

        """
            if hasattr(source, 'read'):
                stream = source
            else:
                stream = StringIO(source)
            return stream

        def _position(self, offset):
            chunk = self.chunk
            nLines = chunk.count('\n', 0, offset)
            positionLine = self.prevNumLines + nLines
            lastLinePos = chunk.rfind('\n', 0, offset)
            if lastLinePos == -1:
                positionColumn = self.prevNumCols + offset
            else:
                positionColumn = offset - (lastLinePos + 1)
            return (positionLine, positionColumn)

        def position(self):
            """Returns (line, col) of the current position in the stream."""
            line, col = self._position(self.chunkOffset)
            return (
             line + 1, col)

        def char(self):
            """ Read one character from the stream or queue if available. Return
            EOF when EOF is reached.
        """
            if self.chunkOffset >= self.chunkSize:
                if not self.readChunk():
                    return EOF
                chunkOffset = self.chunkOffset
                char = self.chunk[chunkOffset]
                self.chunkOffset = chunkOffset + 1
                return char

        def readChunk(self, chunkSize=None):
            if chunkSize is None:
                chunkSize = self._defaultChunkSize
            self.prevNumLines, self.prevNumCols = self._position(self.chunkSize)
            self.chunk = ''
            self.chunkSize = 0
            self.chunkOffset = 0
            data = self.dataStream.read(chunkSize)
            if self._bufferedCharacter:
                data = self._bufferedCharacter + data
                self._bufferedCharacter = None
            elif not data:
                return False
            if len(data) > 1:
                lastv = ord(data[(-1)])
                if not lastv == 13:
                    if 55296 <= lastv <= 56319:
                        self._bufferedCharacter = data[(-1)]
                        data = data[:-1]
            if self.reportCharacterErrors:
                self.reportCharacterErrors(data)
            data = data.replace('\r\n', '\n')
            data = data.replace('\r', '\n')
            self.chunk = data
            self.chunkSize = len(data)
            return True

        def characterErrorsUCS4(self, data):
            for _ in range(len(invalid_unicode_re.findall(data))):
                self.errors.append('invalid-codepoint')

        def characterErrorsUCS2(self, data):
            skip = False
            for match in invalid_unicode_re.finditer(data):
                if skip:
                    pass
                else:
                    codepoint = ord(match.group())
                    pos = match.start()
                    if _utils.isSurrogatePair(data[pos:pos + 2]):
                        char_val = _utils.surrogatePairToCodepoint(data[pos:pos + 2])
                        if char_val in non_bmp_invalid_codepoints:
                            self.errors.append('invalid-codepoint')
                        else:
                            skip = True
                    else:
                        if codepoint >= 55296:
                            if codepoint <= 57343 and pos == len(data) - 1:
                                self.errors.append('invalid-codepoint')
                            else:
                                skip = False
                                self.errors.append('invalid-codepoint')

        def charsUntil--- This code section failed: ---

 L. 328         0  SETUP_FINALLY        18  'to 18'

 L. 329         2  LOAD_GLOBAL              charsUntilRegEx
                4  LOAD_FAST                'characters'
                6  LOAD_FAST                'opposite'
                8  BUILD_TUPLE_2         2 
               10  BINARY_SUBSCR    
               12  STORE_FAST               'chars'
               14  POP_BLOCK        
               16  JUMP_FORWARD        122  'to 122'
             18_0  COME_FROM_FINALLY     0  '0'

 L. 330        18  DUP_TOP          
               20  LOAD_GLOBAL              KeyError
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE   120  'to 120'
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 332        32  LOAD_FAST                'characters'
               34  GET_ITER         
             36_0  COME_FROM            56  '56'
             36_1  COME_FROM            50  '50'
               36  FOR_ITER             58  'to 58'
               38  STORE_FAST               'c'

 L. 333        40  LOAD_GLOBAL              ord
               42  LOAD_FAST                'c'
               44  CALL_FUNCTION_1       1  ''
               46  LOAD_CONST               128
               48  COMPARE_OP               <
               50  POP_JUMP_IF_TRUE_BACK    36  'to 36'
               52  LOAD_GLOBAL              AssertionError
               54  RAISE_VARARGS_1       1  'exception instance'
               56  JUMP_BACK            36  'to 36'
             58_0  COME_FROM            36  '36'

 L. 334        58  LOAD_STR                 ''
               60  LOAD_METHOD              join
               62  LOAD_LISTCOMP            '<code_object <listcomp>>'
               64  LOAD_STR                 'HTMLUnicodeInputStream.charsUntil.<locals>.<listcomp>'
               66  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               68  LOAD_FAST                'characters'
               70  GET_ITER         
               72  CALL_FUNCTION_1       1  ''
               74  CALL_METHOD_1         1  ''
               76  STORE_FAST               'regex'

 L. 335        78  LOAD_FAST                'opposite'
               80  POP_JUMP_IF_TRUE     90  'to 90'

 L. 336        82  LOAD_STR                 '^%s'
               84  LOAD_FAST                'regex'
               86  BINARY_MODULO    
               88  STORE_FAST               'regex'
             90_0  COME_FROM            80  '80'

 L. 337        90  LOAD_GLOBAL              re
               92  LOAD_METHOD              compile
               94  LOAD_STR                 '[%s]+'
               96  LOAD_FAST                'regex'
               98  BINARY_MODULO    
              100  CALL_METHOD_1         1  ''
              102  DUP_TOP          
              104  STORE_FAST               'chars'
              106  LOAD_GLOBAL              charsUntilRegEx
              108  LOAD_FAST                'characters'
              110  LOAD_FAST                'opposite'
              112  BUILD_TUPLE_2         2 
              114  STORE_SUBSCR     
              116  POP_EXCEPT       
              118  JUMP_FORWARD        122  'to 122'
            120_0  COME_FROM            24  '24'
              120  END_FINALLY      
            122_0  COME_FROM           118  '118'
            122_1  COME_FROM            16  '16'

 L. 339       122  BUILD_LIST_0          0 
              124  STORE_FAST               'rv'
            126_0  COME_FROM           246  '246'
            126_1  COME_FROM           242  '242'

 L. 343       126  LOAD_FAST                'chars'
              128  LOAD_METHOD              match
              130  LOAD_FAST                'self'
              132  LOAD_ATTR                chunk
              134  LOAD_FAST                'self'
              136  LOAD_ATTR                chunkOffset
              138  CALL_METHOD_2         2  ''
              140  STORE_FAST               'm'

 L. 344       142  LOAD_FAST                'm'
              144  LOAD_CONST               None
              146  COMPARE_OP               is
              148  POP_JUMP_IF_FALSE   166  'to 166'

 L. 347       150  LOAD_FAST                'self'
              152  LOAD_ATTR                chunkOffset
              154  LOAD_FAST                'self'
              156  LOAD_ATTR                chunkSize
              158  COMPARE_OP               !=
              160  POP_JUMP_IF_FALSE   214  'to 214'

 L. 348       162  JUMP_FORWARD        248  'to 248'
              164  BREAK_LOOP          214  'to 214'
            166_0  COME_FROM           148  '148'

 L. 350       166  LOAD_FAST                'm'
              168  LOAD_METHOD              end
              170  CALL_METHOD_0         0  ''
              172  STORE_FAST               'end'

 L. 353       174  LOAD_FAST                'end'
              176  LOAD_FAST                'self'
              178  LOAD_ATTR                chunkSize
              180  COMPARE_OP               !=
              182  POP_JUMP_IF_FALSE   214  'to 214'

 L. 354       184  LOAD_FAST                'rv'
              186  LOAD_METHOD              append
              188  LOAD_FAST                'self'
              190  LOAD_ATTR                chunk
              192  LOAD_FAST                'self'
              194  LOAD_ATTR                chunkOffset
              196  LOAD_FAST                'end'
              198  BUILD_SLICE_2         2 
              200  BINARY_SUBSCR    
              202  CALL_METHOD_1         1  ''
              204  POP_TOP          

 L. 355       206  LOAD_FAST                'end'
              208  LOAD_FAST                'self'
              210  STORE_ATTR               chunkOffset

 L. 356       212  JUMP_FORWARD        248  'to 248'
            214_0  COME_FROM           182  '182'
            214_1  COME_FROM           164  '164'
            214_2  COME_FROM           160  '160'

 L. 359       214  LOAD_FAST                'rv'
              216  LOAD_METHOD              append
              218  LOAD_FAST                'self'
              220  LOAD_ATTR                chunk
              222  LOAD_FAST                'self'
              224  LOAD_ATTR                chunkOffset
              226  LOAD_CONST               None
              228  BUILD_SLICE_2         2 
              230  BINARY_SUBSCR    
              232  CALL_METHOD_1         1  ''
              234  POP_TOP          

 L. 360       236  LOAD_FAST                'self'
              238  LOAD_METHOD              readChunk
              240  CALL_METHOD_0         0  ''
              242  POP_JUMP_IF_TRUE_BACK   126  'to 126'

 L. 362       244  JUMP_FORWARD        248  'to 248'
              246  JUMP_BACK           126  'to 126'
            248_0  COME_FROM           244  '244'
            248_1  COME_FROM           212  '212'
            248_2  COME_FROM           162  '162'

 L. 364       248  LOAD_STR                 ''
              250  LOAD_METHOD              join
              252  LOAD_FAST                'rv'
              254  CALL_METHOD_1         1  ''
              256  STORE_FAST               'r'

 L. 365       258  LOAD_FAST                'r'
              260  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 246

        def unget(self, char):
            if char is not None:
                if self.chunkOffset == 0:
                    self.chunk = char + self.chunk
                    self.chunkSize += 1
                else:
                    self.chunkOffset -= 1
                    assert self.chunk[self.chunkOffset] == char


    class HTMLBinaryInputStream(HTMLUnicodeInputStream):
        __doc__ = 'Provides a unicode stream of characters to the HTMLTokenizer.\n\n    This class takes care of character encoding and removing or replacing\n    incorrect byte-sequences and also provides column and line tracking.\n\n    '

        def __init__(self, source, override_encoding=None, transport_encoding=None, same_origin_parent_encoding=None, likely_encoding=None, default_encoding='windows-1252', useChardet=True):
            """Initialises the HTMLInputStream.

        HTMLInputStream(source, [encoding]) -> Normalized stream from source
        for use by html5lib.

        source can be either a file-object, local filename or a string.

        The optional encoding parameter must be a string that indicates
        the encoding.  If specified, that encoding will be used,
        regardless of any BOM or later declaration (such as in a meta
        element)

        """
            self.rawStream = self.openStream(source)
            HTMLUnicodeInputStream.__init__(self, self.rawStream)
            self.numBytesMeta = 1024
            self.numBytesChardet = 100
            self.override_encoding = override_encoding
            self.transport_encoding = transport_encoding
            self.same_origin_parent_encoding = same_origin_parent_encoding
            self.likely_encoding = likely_encoding
            self.default_encoding = default_encoding
            self.charEncoding = self.determineEncoding(useChardet)
            assert self.charEncoding[0] is not None
            self.reset()

        def reset(self):
            self.dataStream = self.charEncoding[0].codec_info.streamreader(self.rawStream, 'replace')
            HTMLUnicodeInputStream.reset(self)

        def openStream(self, source):
            """Produces a file object from source.

        source can be either a file object, local filename or a string.

        """
            if hasattr(source, 'read'):
                stream = source
            else:
                stream = BytesIO(source)
            try:
                stream.seek(stream.tell())
            except:
                stream = BufferedStream(stream)
            else:
                return stream

        def determineEncoding(self, chardet=True):
            charEncoding = (
             self.detectBOM(), 'certain')
            if charEncoding[0] is not None:
                return charEncoding
            charEncoding = (
             lookupEncoding(self.override_encoding), 'certain')
            if charEncoding[0] is not None:
                return charEncoding
            charEncoding = (
             lookupEncoding(self.transport_encoding), 'certain')
            if charEncoding[0] is not None:
                return charEncoding
            charEncoding = (
             self.detectEncodingMeta(), 'tentative')
            if charEncoding[0] is not None:
                return charEncoding
            charEncoding = (
             lookupEncoding(self.same_origin_parent_encoding), 'tentative')
            if charEncoding[0] is not None:
                if not charEncoding[0].name.startswith('utf-16'):
                    return charEncoding
                charEncoding = (
                 lookupEncoding(self.likely_encoding), 'tentative')
                if charEncoding[0] is not None:
                    return charEncoding
            if chardet:
                try:
                    from chardet.universaldetector import UniversalDetector
                except ImportError:
                    pass
                else:
                    buffers = []
                    detector = UniversalDetector()
                    while True:
                        buffer = (detector.done or self.rawStream.read)(self.numBytesChardet)
                        if not isinstance(buffer, bytes):
                            raise AssertionError
                        elif not buffer:
                            pass
                        else:
                            buffers.append(buffer)
                            detector.feed(buffer)

                    detector.close()
                    encoding = lookupEncoding(detector.result['encoding'])
                    self.rawStream.seek(0)
                    if encoding is not None:
                        return (encoding, 'tentative')
                charEncoding = (lookupEncoding(self.default_encoding), 'tentative')
                if charEncoding[0] is not None:
                    return charEncoding
                return (
                 lookupEncoding('windows-1252'), 'tentative')

        def changeEncoding(self, newEncoding):
            assert self.charEncoding[1] != 'certain'
            newEncoding = lookupEncoding(newEncoding)
            if newEncoding is None:
                return
            if newEncoding.name in ('utf-16be', 'utf-16le'):
                newEncoding = lookupEncoding('utf-8')
                if not newEncoding is not None:
                    raise AssertionError
            elif newEncoding == self.charEncoding[0]:
                self.charEncoding = (
                 self.charEncoding[0], 'certain')
            else:
                self.rawStream.seek(0)
                self.charEncoding = (newEncoding, 'certain')
                self.reset()
                raise _ReparseException('Encoding changed from %s to %s' % (self.charEncoding[0], newEncoding))

        def detectBOM(self):
            """Attempts to detect at BOM at the start of the stream. If
        an encoding can be determined from the BOM return the name of the
        encoding otherwise return None"""
            bomDict = {codecs.BOM_UTF8: 'utf-8', 
             codecs.BOM_UTF16_LE: 'utf-16le', codecs.BOM_UTF16_BE: 'utf-16be', 
             codecs.BOM_UTF32_LE: 'utf-32le', codecs.BOM_UTF32_BE: 'utf-32be'}
            string = self.rawStream.read(4)
            assert isinstance(string, bytes)
            encoding = bomDict.get(string[:3])
            seek = 3
            if not encoding:
                encoding = bomDict.get(string)
                seek = 4
                if not encoding:
                    encoding = bomDict.get(string[:2])
                    seek = 2
                if encoding:
                    self.rawStream.seek(seek)
                    return lookupEncoding(encoding)
                self.rawStream.seek(0)
                return

        def detectEncodingMeta(self):
            """Report the encoding declared by the meta element
        """
            buffer = self.rawStream.read(self.numBytesMeta)
            assert isinstance(buffer, bytes)
            parser = EncodingParser(buffer)
            self.rawStream.seek(0)
            encoding = parser.getEncoding()
            if encoding is not None:
                if encoding.name in ('utf-16be', 'utf-16le'):
                    encoding = lookupEncoding('utf-8')
            return encoding


    class EncodingBytes(bytes):
        __doc__ = 'String-like object with an associated position and various extra methods\n    If the position is ever greater than the string length then an exception is\n    raised'

        def __new__(self, value):
            assert isinstance(value, bytes)
            return bytes.__new__(self, value.lower())

        def __init__(self, value):
            self._position = -1

        def __iter__(self):
            return self

        def __next__(self):
            p = self._position = self._position + 1
            if p >= len(self):
                raise StopIteration
            elif p < 0:
                raise TypeError
            return self[p:p + 1]

        def next(self):
            return self.__next__()

        def previous(self):
            p = self._position
            if p >= len(self):
                raise StopIteration
            elif p < 0:
                raise TypeError
            self._position = p = p - 1
            return self[p:p + 1]

        def setPosition(self, position):
            if self._position >= len(self):
                raise StopIteration
            self._position = position

        def getPosition(self):
            if self._position >= len(self):
                raise StopIteration
            if self._position >= 0:
                return self._position
            return

        position = property(getPosition, setPosition)

        def getCurrentByte(self):
            return self[self.position:self.position + 1]

        currentByte = property(getCurrentByte)

        def skip(self, chars=spaceCharactersBytes):
            """Skip past a list of characters"""
            p = self.position
            while True:
                if p < len(self):
                    c = self[p:p + 1]
                    if c not in chars:
                        self._position = p
                        return c
                    p += 1

            self._position = p

        def skipUntil(self, chars):
            p = self.position
            while True:
                if p < len(self):
                    c = self[p:p + 1]
                    if c in chars:
                        self._position = p
                        return c
                    p += 1

            self._position = p

        def matchBytes(self, bytes):
            """Look for a sequence of bytes at the start of a string. If the bytes
        are found return True and advance the position to the byte after the
        match. Otherwise return False and leave the position alone"""
            p = self.position
            data = self[p:p + len(bytes)]
            rv = data.startswith(bytes)
            if rv:
                self.position += len(bytes)
            return rv

        def jumpTo(self, bytes):
            """Look for the next sequence of bytes matching a given sequence. If
        a match is found advance the position to the last byte of the match"""
            newPosition = self[self.position:].find(bytes)
            if newPosition > -1:
                if self._position == -1:
                    self._position = 0
                self._position += newPosition + len(bytes) - 1
                return True
            raise StopIteration


    class EncodingParser(object):
        __doc__ = 'Mini parser for detecting character encoding from meta elements'

        def __init__(self, data):
            """string - the data to work on for encoding detection"""
            self.data = EncodingBytes(data)
            self.encoding = None

        def getEncoding--- This code section failed: ---

 L. 698         0  LOAD_CONST               b'<!--'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                handleComment
                6  BUILD_TUPLE_2         2 

 L. 699         8  LOAD_CONST               b'<meta'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                handleMeta
               14  BUILD_TUPLE_2         2 

 L. 700        16  LOAD_CONST               b'</'
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                handlePossibleEndTag
               22  BUILD_TUPLE_2         2 

 L. 701        24  LOAD_CONST               b'<!'
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                handleOther
               30  BUILD_TUPLE_2         2 

 L. 702        32  LOAD_CONST               b'<?'
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                handleOther
               38  BUILD_TUPLE_2         2 

 L. 703        40  LOAD_CONST               b'<'
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                handlePossibleStartTag
               46  BUILD_TUPLE_2         2 

 L. 697        48  BUILD_TUPLE_6         6 
               50  STORE_FAST               'methodDispatch'

 L. 704        52  LOAD_FAST                'self'
               54  LOAD_ATTR                data
               56  GET_ITER         
             58_0  COME_FROM           148  '148'
             58_1  COME_FROM           142  '142'
               58  FOR_ITER            150  'to 150'
               60  STORE_FAST               '_'

 L. 705        62  LOAD_CONST               True
               64  STORE_FAST               'keepParsing'

 L. 706        66  LOAD_FAST                'methodDispatch'
               68  GET_ITER         
             70_0  COME_FROM           138  '138'
             70_1  COME_FROM           134  '134'
             70_2  COME_FROM           106  '106'
             70_3  COME_FROM            88  '88'
               70  FOR_ITER            140  'to 140'
               72  UNPACK_SEQUENCE_2     2 
               74  STORE_FAST               'key'
               76  STORE_FAST               'method'

 L. 707        78  LOAD_FAST                'self'
               80  LOAD_ATTR                data
               82  LOAD_METHOD              matchBytes
               84  LOAD_FAST                'key'
               86  CALL_METHOD_1         1  ''
               88  POP_JUMP_IF_FALSE_BACK    70  'to 70'

 L. 708        90  SETUP_FINALLY       108  'to 108'

 L. 709        92  LOAD_FAST                'method'
               94  CALL_FUNCTION_0       0  ''
               96  STORE_FAST               'keepParsing'

 L. 710        98  POP_BLOCK        
              100  POP_TOP          
              102  JUMP_FORWARD        140  'to 140'
              104  POP_BLOCK        
              106  JUMP_BACK            70  'to 70'
            108_0  COME_FROM_FINALLY    90  '90'

 L. 711       108  DUP_TOP          
              110  LOAD_GLOBAL              StopIteration
              112  COMPARE_OP               exception-match
              114  POP_JUMP_IF_FALSE   136  'to 136'
              116  POP_TOP          
              118  POP_TOP          
              120  POP_TOP          

 L. 712       122  LOAD_CONST               False
              124  STORE_FAST               'keepParsing'

 L. 713       126  POP_EXCEPT       
              128  POP_TOP          
              130  JUMP_FORWARD        140  'to 140'
              132  POP_EXCEPT       
              134  JUMP_BACK            70  'to 70'
            136_0  COME_FROM           114  '114'
              136  END_FINALLY      
              138  JUMP_BACK            70  'to 70'
            140_0  COME_FROM           130  '130'
            140_1  COME_FROM           102  '102'
            140_2  COME_FROM            70  '70'

 L. 714       140  LOAD_FAST                'keepParsing'
              142  POP_JUMP_IF_TRUE_BACK    58  'to 58'

 L. 715       144  POP_TOP          
              146  BREAK_LOOP          150  'to 150'
              148  JUMP_BACK            58  'to 58'
            150_0  COME_FROM           146  '146'
            150_1  COME_FROM            58  '58'

 L. 717       150  LOAD_FAST                'self'
              152  LOAD_ATTR                encoding
              154  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 128

        def handleComment(self):
            """Skip over comments"""
            return self.data.jumpTo(b'-->')

        def handleMeta(self):
            if self.data.currentByte not in spaceCharactersBytes:
                return True
            hasPragma = False
            pendingEncoding = None
            while True:
                attr = self.getAttribute()
                if attr is None:
                    return True
                if attr[0] == b'http-equiv':
                    hasPragma = attr[1] == b'content-type'
                    if hasPragma and pendingEncoding is not None:
                        self.encoding = pendingEncoding
                        return False
                    else:
                        if attr[0] == b'charset':
                            tentativeEncoding = attr[1]
                            codec = lookupEncoding(tentativeEncoding)
                            if codec is not None:
                                self.encoding = codec
                                return False
                        else:
                            if attr[0] == b'content':
                                contentParser = ContentAttrParser(EncodingBytes(attr[1]))
                                tentativeEncoding = contentParser.parse()
                                if tentativeEncoding is not None:
                                    codec = lookupEncoding(tentativeEncoding)
                                    if codec is not None:
                                        if hasPragma:
                                            self.encoding = codec
                                            return False
                                        else:
                                            pendingEncoding = codec

        def handlePossibleStartTag(self):
            return self.handlePossibleTag(False)

        def handlePossibleEndTag(self):
            next(self.data)
            return self.handlePossibleTag(True)

        def handlePossibleTag(self, endTag):
            data = self.data
            if data.currentByte not in asciiLettersBytes:
                if endTag:
                    data.previous()
                    self.handleOther()
                return True
            c = data.skipUntil(spacesAngleBrackets)
            if c == b'<':
                data.previous()
            else:
                attr = self.getAttribute()
                while True:
                    if attr is not None:
                        attr = self.getAttribute()

            return True

        def handleOther(self):
            return self.data.jumpTo(b'>')

        def getAttribute--- This code section failed: ---

 L. 795         0  LOAD_FAST                'self'
                2  LOAD_ATTR                data
                4  STORE_FAST               'data'

 L. 797         6  LOAD_FAST                'data'
                8  LOAD_METHOD              skip
               10  LOAD_GLOBAL              spaceCharactersBytes
               12  LOAD_GLOBAL              frozenset
               14  LOAD_CONST               b'/'
               16  BUILD_LIST_1          1 
               18  CALL_FUNCTION_1       1  ''
               20  BINARY_OR        
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'c'

 L. 798        26  LOAD_FAST                'c'
               28  LOAD_CONST               None
               30  COMPARE_OP               is
               32  POP_JUMP_IF_TRUE     50  'to 50'
               34  LOAD_GLOBAL              len
               36  LOAD_FAST                'c'
               38  CALL_FUNCTION_1       1  ''
               40  LOAD_CONST               1
               42  COMPARE_OP               ==
               44  POP_JUMP_IF_TRUE     50  'to 50'
               46  LOAD_ASSERT              AssertionError
               48  RAISE_VARARGS_1       1  'exception instance'
             50_0  COME_FROM            44  '44'
             50_1  COME_FROM            32  '32'

 L. 800        50  LOAD_FAST                'c'
               52  LOAD_CONST               (b'>', None)
               54  COMPARE_OP               in
               56  POP_JUMP_IF_FALSE    62  'to 62'

 L. 801        58  LOAD_CONST               None
               60  RETURN_VALUE     
             62_0  COME_FROM            56  '56'

 L. 803        62  BUILD_LIST_0          0 
               64  STORE_FAST               'attrName'

 L. 804        66  BUILD_LIST_0          0 
               68  STORE_FAST               'attrValue'
             70_0  COME_FROM           182  '182'

 L. 807        70  LOAD_FAST                'c'
               72  LOAD_CONST               b'='
               74  COMPARE_OP               ==
               76  POP_JUMP_IF_FALSE    86  'to 86'
               78  LOAD_FAST                'attrName'
               80  POP_JUMP_IF_FALSE    86  'to 86'

 L. 808        82  JUMP_FORWARD        184  'to 184'
               84  BREAK_LOOP          174  'to 174'
             86_0  COME_FROM            80  '80'
             86_1  COME_FROM            76  '76'

 L. 809        86  LOAD_FAST                'c'
               88  LOAD_GLOBAL              spaceCharactersBytes
               90  COMPARE_OP               in
               92  POP_JUMP_IF_FALSE   106  'to 106'

 L. 811        94  LOAD_FAST                'data'
               96  LOAD_METHOD              skip
               98  CALL_METHOD_0         0  ''
              100  STORE_FAST               'c'

 L. 812       102  JUMP_FORWARD        184  'to 184'
              104  BREAK_LOOP          174  'to 174'
            106_0  COME_FROM            92  '92'

 L. 813       106  LOAD_FAST                'c'
              108  LOAD_CONST               (b'/', b'>')
              110  COMPARE_OP               in
              112  POP_JUMP_IF_FALSE   128  'to 128'

 L. 814       114  LOAD_CONST               b''
              116  LOAD_METHOD              join
              118  LOAD_FAST                'attrName'
              120  CALL_METHOD_1         1  ''
              122  LOAD_CONST               b''
              124  BUILD_TUPLE_2         2 
              126  RETURN_VALUE     
            128_0  COME_FROM           112  '112'

 L. 815       128  LOAD_FAST                'c'
              130  LOAD_GLOBAL              asciiUppercaseBytes
              132  COMPARE_OP               in
              134  POP_JUMP_IF_FALSE   152  'to 152'

 L. 816       136  LOAD_FAST                'attrName'
              138  LOAD_METHOD              append
              140  LOAD_FAST                'c'
              142  LOAD_METHOD              lower
              144  CALL_METHOD_0         0  ''
              146  CALL_METHOD_1         1  ''
              148  POP_TOP          
              150  JUMP_FORWARD        174  'to 174'
            152_0  COME_FROM           134  '134'

 L. 817       152  LOAD_FAST                'c'
              154  LOAD_CONST               None
              156  COMPARE_OP               is
              158  POP_JUMP_IF_FALSE   164  'to 164'

 L. 818       160  LOAD_CONST               None
              162  RETURN_VALUE     
            164_0  COME_FROM           158  '158'

 L. 820       164  LOAD_FAST                'attrName'
              166  LOAD_METHOD              append
              168  LOAD_FAST                'c'
              170  CALL_METHOD_1         1  ''
              172  POP_TOP          
            174_0  COME_FROM           150  '150'
            174_1  COME_FROM           104  '104'
            174_2  COME_FROM            84  '84'

 L. 822       174  LOAD_GLOBAL              next
              176  LOAD_FAST                'data'
              178  CALL_FUNCTION_1       1  ''
              180  STORE_FAST               'c'
              182  JUMP_BACK            70  'to 70'
            184_0  COME_FROM           102  '102'
            184_1  COME_FROM            82  '82'

 L. 824       184  LOAD_FAST                'c'
              186  LOAD_CONST               b'='
              188  COMPARE_OP               !=
              190  POP_JUMP_IF_FALSE   214  'to 214'

 L. 825       192  LOAD_FAST                'data'
              194  LOAD_METHOD              previous
              196  CALL_METHOD_0         0  ''
              198  POP_TOP          

 L. 826       200  LOAD_CONST               b''
              202  LOAD_METHOD              join
              204  LOAD_FAST                'attrName'
              206  CALL_METHOD_1         1  ''
              208  LOAD_CONST               b''
              210  BUILD_TUPLE_2         2 
              212  RETURN_VALUE     
            214_0  COME_FROM           190  '190'

 L. 828       214  LOAD_GLOBAL              next
              216  LOAD_FAST                'data'
              218  CALL_FUNCTION_1       1  ''
              220  POP_TOP          

 L. 830       222  LOAD_FAST                'data'
              224  LOAD_METHOD              skip
              226  CALL_METHOD_0         0  ''
              228  STORE_FAST               'c'

 L. 832       230  LOAD_FAST                'c'
              232  LOAD_CONST               (b"'", b'"')
              234  COMPARE_OP               in
          236_238  POP_JUMP_IF_FALSE   330  'to 330'

 L. 834       240  LOAD_FAST                'c'
              242  STORE_FAST               'quoteChar'
            244_0  COME_FROM           326  '326'
            244_1  COME_FROM           314  '314'

 L. 837       244  LOAD_GLOBAL              next
              246  LOAD_FAST                'data'
              248  CALL_FUNCTION_1       1  ''
              250  STORE_FAST               'c'

 L. 839       252  LOAD_FAST                'c'
              254  LOAD_FAST                'quoteChar'
              256  COMPARE_OP               ==
          258_260  POP_JUMP_IF_FALSE   290  'to 290'

 L. 840       262  LOAD_GLOBAL              next
              264  LOAD_FAST                'data'
              266  CALL_FUNCTION_1       1  ''
              268  POP_TOP          

 L. 841       270  LOAD_CONST               b''
              272  LOAD_METHOD              join
              274  LOAD_FAST                'attrName'
              276  CALL_METHOD_1         1  ''
              278  LOAD_CONST               b''
              280  LOAD_METHOD              join
              282  LOAD_FAST                'attrValue'
              284  CALL_METHOD_1         1  ''
              286  BUILD_TUPLE_2         2 
              288  RETURN_VALUE     
            290_0  COME_FROM           258  '258'

 L. 843       290  LOAD_FAST                'c'
              292  LOAD_GLOBAL              asciiUppercaseBytes
              294  COMPARE_OP               in
          296_298  POP_JUMP_IF_FALSE   316  'to 316'

 L. 844       300  LOAD_FAST                'attrValue'
              302  LOAD_METHOD              append
              304  LOAD_FAST                'c'
              306  LOAD_METHOD              lower
              308  CALL_METHOD_0         0  ''
              310  CALL_METHOD_1         1  ''
              312  POP_TOP          
              314  JUMP_BACK           244  'to 244'
            316_0  COME_FROM           296  '296'

 L. 847       316  LOAD_FAST                'attrValue'
              318  LOAD_METHOD              append
              320  LOAD_FAST                'c'
              322  CALL_METHOD_1         1  ''
              324  POP_TOP          
              326  JUMP_BACK           244  'to 244'
              328  JUMP_FORWARD        404  'to 404'
            330_0  COME_FROM           236  '236'

 L. 848       330  LOAD_FAST                'c'
              332  LOAD_CONST               b'>'
              334  COMPARE_OP               ==
          336_338  POP_JUMP_IF_FALSE   354  'to 354'

 L. 849       340  LOAD_CONST               b''
              342  LOAD_METHOD              join
              344  LOAD_FAST                'attrName'
              346  CALL_METHOD_1         1  ''
              348  LOAD_CONST               b''
              350  BUILD_TUPLE_2         2 
              352  RETURN_VALUE     
            354_0  COME_FROM           336  '336'

 L. 850       354  LOAD_FAST                'c'
              356  LOAD_GLOBAL              asciiUppercaseBytes
              358  COMPARE_OP               in
          360_362  POP_JUMP_IF_FALSE   380  'to 380'

 L. 851       364  LOAD_FAST                'attrValue'
              366  LOAD_METHOD              append
              368  LOAD_FAST                'c'
              370  LOAD_METHOD              lower
              372  CALL_METHOD_0         0  ''
              374  CALL_METHOD_1         1  ''
              376  POP_TOP          
              378  JUMP_FORWARD        404  'to 404'
            380_0  COME_FROM           360  '360'

 L. 852       380  LOAD_FAST                'c'
              382  LOAD_CONST               None
              384  COMPARE_OP               is
          386_388  POP_JUMP_IF_FALSE   394  'to 394'

 L. 853       390  LOAD_CONST               None
              392  RETURN_VALUE     
            394_0  COME_FROM           386  '386'

 L. 855       394  LOAD_FAST                'attrValue'
              396  LOAD_METHOD              append
              398  LOAD_FAST                'c'
              400  CALL_METHOD_1         1  ''
              402  POP_TOP          
            404_0  COME_FROM           492  '492'
            404_1  COME_FROM           466  '466'
            404_2  COME_FROM           378  '378'
            404_3  COME_FROM           328  '328'

 L. 858       404  LOAD_GLOBAL              next
              406  LOAD_FAST                'data'
              408  CALL_FUNCTION_1       1  ''
              410  STORE_FAST               'c'

 L. 859       412  LOAD_FAST                'c'
              414  LOAD_GLOBAL              spacesAngleBrackets
              416  COMPARE_OP               in
          418_420  POP_JUMP_IF_FALSE   442  'to 442'

 L. 860       422  LOAD_CONST               b''
              424  LOAD_METHOD              join
              426  LOAD_FAST                'attrName'
              428  CALL_METHOD_1         1  ''
              430  LOAD_CONST               b''
              432  LOAD_METHOD              join
              434  LOAD_FAST                'attrValue'
              436  CALL_METHOD_1         1  ''
              438  BUILD_TUPLE_2         2 
              440  RETURN_VALUE     
            442_0  COME_FROM           418  '418'

 L. 861       442  LOAD_FAST                'c'
              444  LOAD_GLOBAL              asciiUppercaseBytes
              446  COMPARE_OP               in
          448_450  POP_JUMP_IF_FALSE   468  'to 468'

 L. 862       452  LOAD_FAST                'attrValue'
              454  LOAD_METHOD              append
              456  LOAD_FAST                'c'
              458  LOAD_METHOD              lower
              460  CALL_METHOD_0         0  ''
              462  CALL_METHOD_1         1  ''
              464  POP_TOP          
              466  JUMP_BACK           404  'to 404'
            468_0  COME_FROM           448  '448'

 L. 863       468  LOAD_FAST                'c'
              470  LOAD_CONST               None
              472  COMPARE_OP               is
          474_476  POP_JUMP_IF_FALSE   482  'to 482'

 L. 864       478  LOAD_CONST               None
              480  RETURN_VALUE     
            482_0  COME_FROM           474  '474'

 L. 866       482  LOAD_FAST                'attrValue'
              484  LOAD_METHOD              append
              486  LOAD_FAST                'c'
              488  CALL_METHOD_1         1  ''
              490  POP_TOP          
          492_494  JUMP_BACK           404  'to 404'

Parse error at or near `LOAD_FAST' instruction at offset 184


    class ContentAttrParser(object):

        def __init__(self, data):
            assert isinstance(data, bytes)
            self.data = data

        def parse--- This code section failed: ---

 L. 875       0_2  SETUP_FINALLY       256  'to 256'

 L. 878         4  LOAD_FAST                'self'
                6  LOAD_ATTR                data
                8  LOAD_METHOD              jumpTo
               10  LOAD_CONST               b'charset'
               12  CALL_METHOD_1         1  ''
               14  POP_TOP          

 L. 879        16  LOAD_FAST                'self'
               18  LOAD_ATTR                data
               20  DUP_TOP          
               22  LOAD_ATTR                position
               24  LOAD_CONST               1
               26  INPLACE_ADD      
               28  ROT_TWO          
               30  STORE_ATTR               position

 L. 880        32  LOAD_FAST                'self'
               34  LOAD_ATTR                data
               36  LOAD_METHOD              skip
               38  CALL_METHOD_0         0  ''
               40  POP_TOP          

 L. 881        42  LOAD_FAST                'self'
               44  LOAD_ATTR                data
               46  LOAD_ATTR                currentByte
               48  LOAD_CONST               b'='
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_TRUE     60  'to 60'

 L. 883        54  POP_BLOCK        
               56  LOAD_CONST               None
               58  RETURN_VALUE     
             60_0  COME_FROM            52  '52'

 L. 884        60  LOAD_FAST                'self'
               62  LOAD_ATTR                data
               64  DUP_TOP          
               66  LOAD_ATTR                position
               68  LOAD_CONST               1
               70  INPLACE_ADD      
               72  ROT_TWO          
               74  STORE_ATTR               position

 L. 885        76  LOAD_FAST                'self'
               78  LOAD_ATTR                data
               80  LOAD_METHOD              skip
               82  CALL_METHOD_0         0  ''
               84  POP_TOP          

 L. 887        86  LOAD_FAST                'self'
               88  LOAD_ATTR                data
               90  LOAD_ATTR                currentByte
               92  LOAD_CONST               (b'"', b"'")
               94  COMPARE_OP               in
               96  POP_JUMP_IF_FALSE   170  'to 170'

 L. 888        98  LOAD_FAST                'self'
              100  LOAD_ATTR                data
              102  LOAD_ATTR                currentByte
              104  STORE_FAST               'quoteMark'

 L. 889       106  LOAD_FAST                'self'
              108  LOAD_ATTR                data
              110  DUP_TOP          
              112  LOAD_ATTR                position
              114  LOAD_CONST               1
              116  INPLACE_ADD      
              118  ROT_TWO          
              120  STORE_ATTR               position

 L. 890       122  LOAD_FAST                'self'
              124  LOAD_ATTR                data
              126  LOAD_ATTR                position
              128  STORE_FAST               'oldPosition'

 L. 891       130  LOAD_FAST                'self'
              132  LOAD_ATTR                data
              134  LOAD_METHOD              jumpTo
              136  LOAD_FAST                'quoteMark'
              138  CALL_METHOD_1         1  ''
              140  POP_JUMP_IF_FALSE   162  'to 162'

 L. 892       142  LOAD_FAST                'self'
              144  LOAD_ATTR                data
              146  LOAD_FAST                'oldPosition'
              148  LOAD_FAST                'self'
              150  LOAD_ATTR                data
              152  LOAD_ATTR                position
              154  BUILD_SLICE_2         2 
              156  BINARY_SUBSCR    
              158  POP_BLOCK        
              160  RETURN_VALUE     
            162_0  COME_FROM           140  '140'

 L. 894       162  POP_BLOCK        
              164  LOAD_CONST               None
              166  RETURN_VALUE     
              168  JUMP_FORWARD        252  'to 252'
            170_0  COME_FROM            96  '96'

 L. 897       170  LOAD_FAST                'self'
              172  LOAD_ATTR                data
              174  LOAD_ATTR                position
              176  STORE_FAST               'oldPosition'

 L. 898       178  SETUP_FINALLY       214  'to 214'

 L. 899       180  LOAD_FAST                'self'
              182  LOAD_ATTR                data
              184  LOAD_METHOD              skipUntil
              186  LOAD_GLOBAL              spaceCharactersBytes
              188  CALL_METHOD_1         1  ''
              190  POP_TOP          

 L. 900       192  LOAD_FAST                'self'
              194  LOAD_ATTR                data
              196  LOAD_FAST                'oldPosition'
              198  LOAD_FAST                'self'
              200  LOAD_ATTR                data
              202  LOAD_ATTR                position
              204  BUILD_SLICE_2         2 
              206  BINARY_SUBSCR    
              208  POP_BLOCK        
              210  POP_BLOCK        
              212  RETURN_VALUE     
            214_0  COME_FROM_FINALLY   178  '178'

 L. 901       214  DUP_TOP          
              216  LOAD_GLOBAL              StopIteration
              218  COMPARE_OP               exception-match
          220_222  POP_JUMP_IF_FALSE   250  'to 250'
              224  POP_TOP          
              226  POP_TOP          
              228  POP_TOP          

 L. 903       230  LOAD_FAST                'self'
              232  LOAD_ATTR                data
              234  LOAD_FAST                'oldPosition'
              236  LOAD_CONST               None
              238  BUILD_SLICE_2         2 
              240  BINARY_SUBSCR    
              242  ROT_FOUR         
              244  POP_EXCEPT       
              246  POP_BLOCK        
              248  RETURN_VALUE     
            250_0  COME_FROM           220  '220'
              250  END_FINALLY      
            252_0  COME_FROM           168  '168'
              252  POP_BLOCK        
              254  JUMP_FORWARD        280  'to 280'
            256_0  COME_FROM_FINALLY     0  '0'

 L. 904       256  DUP_TOP          
              258  LOAD_GLOBAL              StopIteration
              260  COMPARE_OP               exception-match
          262_264  POP_JUMP_IF_FALSE   278  'to 278'
              266  POP_TOP          
              268  POP_TOP          
              270  POP_TOP          

 L. 905       272  POP_EXCEPT       
              274  LOAD_CONST               None
              276  RETURN_VALUE     
            278_0  COME_FROM           262  '262'
              278  END_FINALLY      
            280_0  COME_FROM           254  '254'

Parse error at or near `LOAD_CONST' instruction at offset 56


    def lookupEncoding--- This code section failed: ---

 L. 911         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'encoding'
                4  LOAD_GLOBAL              binary_type
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    48  'to 48'

 L. 912        10  SETUP_FINALLY        26  'to 26'

 L. 913        12  LOAD_FAST                'encoding'
               14  LOAD_METHOD              decode
               16  LOAD_STR                 'ascii'
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'encoding'
               22  POP_BLOCK        
               24  JUMP_FORWARD         48  'to 48'
             26_0  COME_FROM_FINALLY    10  '10'

 L. 914        26  DUP_TOP          
               28  LOAD_GLOBAL              UnicodeDecodeError
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    46  'to 46'
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L. 915        40  POP_EXCEPT       
               42  LOAD_CONST               None
               44  RETURN_VALUE     
             46_0  COME_FROM            32  '32'
               46  END_FINALLY      
             48_0  COME_FROM            24  '24'
             48_1  COME_FROM             8  '8'

 L. 917        48  LOAD_FAST                'encoding'
               50  LOAD_CONST               None
               52  COMPARE_OP               is-not
               54  POP_JUMP_IF_FALSE    94  'to 94'

 L. 918        56  SETUP_FINALLY        70  'to 70'

 L. 919        58  LOAD_GLOBAL              webencodings
               60  LOAD_METHOD              lookup
               62  LOAD_FAST                'encoding'
               64  CALL_METHOD_1         1  ''
               66  POP_BLOCK        
               68  RETURN_VALUE     
             70_0  COME_FROM_FINALLY    56  '56'

 L. 920        70  DUP_TOP          
               72  LOAD_GLOBAL              AttributeError
               74  COMPARE_OP               exception-match
               76  POP_JUMP_IF_FALSE    90  'to 90'
               78  POP_TOP          
               80  POP_TOP          
               82  POP_TOP          

 L. 921        84  POP_EXCEPT       
               86  LOAD_CONST               None
               88  RETURN_VALUE     
             90_0  COME_FROM            76  '76'
               90  END_FINALLY      
               92  JUMP_FORWARD         98  'to 98'
             94_0  COME_FROM            54  '54'

 L. 923        94  LOAD_CONST               None
               96  RETURN_VALUE     
             98_0  COME_FROM            92  '92'

Parse error at or near `LOAD_CONST' instruction at offset 86