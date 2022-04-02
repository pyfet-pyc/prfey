# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\yaml\reader.py
__all__ = [
 'Reader', 'ReaderError']
from .error import YAMLError, Mark
import codecs, re

class ReaderError(YAMLError):

    def __init__(self, name, position, character, encoding, reason):
        self.name = name
        self.character = character
        self.position = position
        self.encoding = encoding
        self.reason = reason

    def __str__(self):
        if isinstance(self.character, bytes):
            return '\'%s\' codec can\'t decode byte #x%02x: %s\n  in "%s", position %d' % (
             self.encoding, ord(self.character), self.reason,
             self.name, self.position)
        return 'unacceptable character #x%04x: %s\n  in "%s", position %d' % (
         self.character, self.reason,
         self.name, self.position)


class Reader(object):

    def __init__(self, stream):
        self.name = None
        self.stream = None
        self.stream_pointer = 0
        self.eof = True
        self.buffer = ''
        self.pointer = 0
        self.raw_buffer = None
        self.raw_decode = None
        self.encoding = None
        self.index = 0
        self.line = 0
        self.column = 0
        if isinstance(stream, str):
            self.name = '<unicode string>'
            self.check_printable(stream)
            self.buffer = stream + '\x00'
        elif isinstance(stream, bytes):
            self.name = '<byte string>'
            self.raw_buffer = stream
            self.determine_encoding()
        else:
            self.stream = stream
            self.name = getattr(stream, 'name', '<file>')
            self.eof = False
            self.raw_buffer = None
            self.determine_encoding()

    def peek(self, index=0):
        try:
            return self.buffer[(self.pointer + index)]
        except IndexError:
            self.update(index + 1)
            return self.buffer[(self.pointer + index)]

    def prefix(self, length=1):
        if self.pointer + length >= len(self.buffer):
            self.update(length)
        return self.buffer[self.pointer:self.pointer + length]

    def forward(self, length=1):
        if self.pointer + length + 1 >= len(self.buffer):
            self.update(length + 1)
            while True:
                if length:
                    ch = self.buffer[self.pointer]
                    self.pointer += 1
                    self.index += 1
                    if not (ch in '\n\x85\u2028\u2029' or ch) == '\r' or self.buffer[self.pointer] != '\n':
                        self.line += 1
                        self.column = 0
                    elif ch != '\ufeff':
                        self.column += 1
                    length -= 1

    def get_mark(self):
        if self.stream is None:
            return Mark(self.name, self.index, self.line, self.column, self.buffer, self.pointer)
        return Mark(self.name, self.index, self.line, self.column, None, None)

    def determine_encoding(self):
        while not self.eof:
            if self.raw_buffer is None or len(self.raw_buffer) < 2:
                self.update_raw()

        if isinstance(self.raw_buffer, bytes):
            if self.raw_buffer.startswith(codecs.BOM_UTF16_LE):
                self.raw_decode = codecs.utf_16_le_decode
                self.encoding = 'utf-16-le'
            elif self.raw_buffer.startswith(codecs.BOM_UTF16_BE):
                self.raw_decode = codecs.utf_16_be_decode
                self.encoding = 'utf-16-be'
            else:
                self.raw_decode = codecs.utf_8_decode
                self.encoding = 'utf-8'
        self.update(1)

    NON_PRINTABLE = re.compile('[^\t\n\r -~\x85\xa0-\ud7ff\ue000-�𐀀-\U0010ffff]')

    def check_printable(self, data):
        match = self.NON_PRINTABLE.search(data)
        if match:
            character = match.group()
            position = self.index + (len(self.buffer) - self.pointer) + match.start()
            raise ReaderError(self.name, position, ord(character), 'unicode', 'special characters are not allowed')

    def update--- This code section failed: ---

 L. 147         0  LOAD_FAST                'self'
                2  LOAD_ATTR                raw_buffer
                4  LOAD_CONST               None
                6  COMPARE_OP               is
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 148        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 149        14  LOAD_FAST                'self'
               16  LOAD_ATTR                buffer
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                pointer
               22  LOAD_CONST               None
               24  BUILD_SLICE_2         2 
               26  BINARY_SUBSCR    
               28  LOAD_FAST                'self'
               30  STORE_ATTR               buffer

 L. 150        32  LOAD_CONST               0
               34  LOAD_FAST                'self'
               36  STORE_ATTR               pointer
             38_0  COME_FROM           300  '300'
             38_1  COME_FROM           274  '274'

 L. 151        38  LOAD_GLOBAL              len
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                buffer
               44  CALL_FUNCTION_1       1  ''
               46  LOAD_FAST                'length'
               48  COMPARE_OP               <
            50_52  POP_JUMP_IF_FALSE   302  'to 302'

 L. 152        54  LOAD_FAST                'self'
               56  LOAD_ATTR                eof
               58  POP_JUMP_IF_TRUE     68  'to 68'

 L. 153        60  LOAD_FAST                'self'
               62  LOAD_METHOD              update_raw
               64  CALL_METHOD_0         0  ''
               66  POP_TOP          
             68_0  COME_FROM            58  '58'

 L. 154        68  LOAD_FAST                'self'
               70  LOAD_ATTR                raw_decode
               72  LOAD_CONST               None
               74  COMPARE_OP               is-not
               76  POP_JUMP_IF_FALSE   216  'to 216'

 L. 155        78  SETUP_FINALLY       106  'to 106'

 L. 156        80  LOAD_FAST                'self'
               82  LOAD_METHOD              raw_decode
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                raw_buffer

 L. 157        88  LOAD_STR                 'strict'

 L. 157        90  LOAD_FAST                'self'
               92  LOAD_ATTR                eof

 L. 156        94  CALL_METHOD_3         3  ''
               96  UNPACK_SEQUENCE_2     2 
               98  STORE_FAST               'data'
              100  STORE_FAST               'converted'
              102  POP_BLOCK        
              104  JUMP_FORWARD        230  'to 230'
            106_0  COME_FROM_FINALLY    78  '78'

 L. 158       106  DUP_TOP          
              108  LOAD_GLOBAL              UnicodeDecodeError
              110  COMPARE_OP               exception-match
              112  POP_JUMP_IF_FALSE   212  'to 212'
              114  POP_TOP          
              116  STORE_FAST               'exc'
              118  POP_TOP          
              120  SETUP_FINALLY       200  'to 200'

 L. 159       122  LOAD_FAST                'self'
              124  LOAD_ATTR                raw_buffer
              126  LOAD_FAST                'exc'
              128  LOAD_ATTR                start
              130  BINARY_SUBSCR    
              132  STORE_FAST               'character'

 L. 160       134  LOAD_FAST                'self'
              136  LOAD_ATTR                stream
              138  LOAD_CONST               None
              140  COMPARE_OP               is-not
              142  POP_JUMP_IF_FALSE   168  'to 168'

 L. 161       144  LOAD_FAST                'self'
              146  LOAD_ATTR                stream_pointer
              148  LOAD_GLOBAL              len
              150  LOAD_FAST                'self'
              152  LOAD_ATTR                raw_buffer
              154  CALL_FUNCTION_1       1  ''
              156  BINARY_SUBTRACT  
              158  LOAD_FAST                'exc'
              160  LOAD_ATTR                start
              162  BINARY_ADD       
              164  STORE_FAST               'position'
              166  JUMP_FORWARD        174  'to 174'
            168_0  COME_FROM           142  '142'

 L. 163       168  LOAD_FAST                'exc'
              170  LOAD_ATTR                start
              172  STORE_FAST               'position'
            174_0  COME_FROM           166  '166'

 L. 164       174  LOAD_GLOBAL              ReaderError
              176  LOAD_FAST                'self'
              178  LOAD_ATTR                name
              180  LOAD_FAST                'position'
              182  LOAD_FAST                'character'

 L. 165       184  LOAD_FAST                'exc'
              186  LOAD_ATTR                encoding

 L. 165       188  LOAD_FAST                'exc'
              190  LOAD_ATTR                reason

 L. 164       192  CALL_FUNCTION_5       5  ''
              194  RAISE_VARARGS_1       1  'exception instance'
              196  POP_BLOCK        
              198  BEGIN_FINALLY    
            200_0  COME_FROM_FINALLY   120  '120'
              200  LOAD_CONST               None
              202  STORE_FAST               'exc'
              204  DELETE_FAST              'exc'
              206  END_FINALLY      
              208  POP_EXCEPT       
              210  JUMP_FORWARD        230  'to 230'
            212_0  COME_FROM           112  '112'
              212  END_FINALLY      
              214  JUMP_FORWARD        230  'to 230'
            216_0  COME_FROM            76  '76'

 L. 167       216  LOAD_FAST                'self'
              218  LOAD_ATTR                raw_buffer
              220  STORE_FAST               'data'

 L. 168       222  LOAD_GLOBAL              len
              224  LOAD_FAST                'data'
              226  CALL_FUNCTION_1       1  ''
              228  STORE_FAST               'converted'
            230_0  COME_FROM           214  '214'
            230_1  COME_FROM           210  '210'
            230_2  COME_FROM           104  '104'

 L. 169       230  LOAD_FAST                'self'
              232  LOAD_METHOD              check_printable
              234  LOAD_FAST                'data'
              236  CALL_METHOD_1         1  ''
              238  POP_TOP          

 L. 170       240  LOAD_FAST                'self'
              242  DUP_TOP          
              244  LOAD_ATTR                buffer
              246  LOAD_FAST                'data'
              248  INPLACE_ADD      
              250  ROT_TWO          
              252  STORE_ATTR               buffer

 L. 171       254  LOAD_FAST                'self'
              256  LOAD_ATTR                raw_buffer
              258  LOAD_FAST                'converted'
              260  LOAD_CONST               None
              262  BUILD_SLICE_2         2 
              264  BINARY_SUBSCR    
              266  LOAD_FAST                'self'
              268  STORE_ATTR               raw_buffer

 L. 172       270  LOAD_FAST                'self'
              272  LOAD_ATTR                eof
              274  POP_JUMP_IF_FALSE_BACK    38  'to 38'

 L. 173       276  LOAD_FAST                'self'
              278  DUP_TOP          
              280  LOAD_ATTR                buffer
              282  LOAD_STR                 '\x00'
              284  INPLACE_ADD      
              286  ROT_TWO          
              288  STORE_ATTR               buffer

 L. 174       290  LOAD_CONST               None
              292  LOAD_FAST                'self'
              294  STORE_ATTR               raw_buffer

 L. 175   296_298  JUMP_FORWARD        302  'to 302'
              300  JUMP_BACK            38  'to 38'
            302_0  COME_FROM           296  '296'
            302_1  COME_FROM            50  '50'

Parse error at or near `JUMP_BACK' instruction at offset 300

    def update_raw(self, size=4096):
        data = self.stream.read(size)
        if self.raw_buffer is None:
            self.raw_buffer = data
        else:
            self.raw_buffer += data
        self.stream_pointer += len(data)
        if not data:
            self.eof = True