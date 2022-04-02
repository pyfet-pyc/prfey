# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\PdfParser.py
import calendar, codecs, collections, mmap, os, re, time, zlib

def encode_text(s):
    return codecs.BOM_UTF16_BE + s.encode('utf_16_be')


PDFDocEncoding = {22:'\x17', 
 24:'˘', 
 25:'ˇ', 
 26:'ˆ', 
 27:'˙', 
 28:'˝', 
 29:'˛', 
 30:'˚', 
 31:'˜', 
 128:'•', 
 129:'†', 
 130:'‡', 
 131:'…', 
 132:'—', 
 133:'–', 
 134:'ƒ', 
 135:'⁄', 
 136:'‹', 
 137:'›', 
 138:'−', 
 139:'‰', 
 140:'„', 
 141:'“', 
 142:'”', 
 143:'‘', 
 144:'’', 
 145:'‚', 
 146:'™', 
 147:'ﬁ', 
 148:'ﬂ', 
 149:'Ł', 
 150:'Œ', 
 151:'Š', 
 152:'Ÿ', 
 153:'Ž', 
 154:'ı', 
 155:'ł', 
 156:'œ', 
 157:'š', 
 158:'ž', 
 160:'€'}

def decode_text(b):
    if b[:len(codecs.BOM_UTF16_BE)] == codecs.BOM_UTF16_BE:
        return b[len(codecs.BOM_UTF16_BE):].decode('utf_16_be')
    return ''.join((PDFDocEncoding.get(byte, chr(byte)) for byte in b))


class PdfFormatError(RuntimeError):
    __doc__ = 'An error that probably indicates a syntactic or semantic error in the\n    PDF file structure'


def check_format_condition(condition, error_message):
    if not condition:
        raise PdfFormatError(error_message)


class IndirectReference(collections.namedtuple('IndirectReferenceTuple', ['object_id', 'generation'])):

    def __str__(self):
        return '%s %s R' % self

    def __bytes__(self):
        return self.__str__().encode('us-ascii')

    def __eq__--- This code section failed: ---

 L.  92         0  LOAD_FAST                'other'
                2  LOAD_ATTR                __class__
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                __class__
                8  <117>                 0  ''
               10  JUMP_IF_FALSE_OR_POP    34  'to 34'

 L.  93        12  LOAD_FAST                'other'
               14  LOAD_ATTR                object_id
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                object_id
               20  COMPARE_OP               ==

 L.  92        22  JUMP_IF_FALSE_OR_POP    34  'to 34'

 L.  94        24  LOAD_FAST                'other'
               26  LOAD_ATTR                generation
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                generation
               32  COMPARE_OP               ==
             34_0  COME_FROM            22  '22'
             34_1  COME_FROM            10  '10'

 L.  91        34  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.object_id, self.generation))


class IndirectObjectDef(IndirectReference):

    def __str__(self):
        return '%s %s obj' % self


class XrefTable:

    def __init__(self):
        self.existing_entries = {}
        self.new_entries = {}
        self.deleted_entries = {0: 65536}
        self.reading_finished = False

    def __setitem__--- This code section failed: ---

 L. 117         0  LOAD_FAST                'self'
                2  LOAD_ATTR                reading_finished
                4  POP_JUMP_IF_FALSE    18  'to 18'

 L. 118         6  LOAD_FAST                'value'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                new_entries
               12  LOAD_FAST                'key'
               14  STORE_SUBSCR     
               16  JUMP_FORWARD         28  'to 28'
             18_0  COME_FROM             4  '4'

 L. 120        18  LOAD_FAST                'value'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                existing_entries
               24  LOAD_FAST                'key'
               26  STORE_SUBSCR     
             28_0  COME_FROM            16  '16'

 L. 121        28  LOAD_FAST                'key'
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                deleted_entries
               34  <118>                 0  ''
               36  POP_JUMP_IF_FALSE    46  'to 46'

 L. 122        38  LOAD_FAST                'self'
               40  LOAD_ATTR                deleted_entries
               42  LOAD_FAST                'key'
               44  DELETE_SUBSCR    
             46_0  COME_FROM            36  '36'

Parse error at or near `<118>' instruction at offset 34

    def __getitem__--- This code section failed: ---

 L. 125         0  SETUP_FINALLY        14  'to 14'

 L. 126         2  LOAD_FAST                'self'
                4  LOAD_ATTR                new_entries
                6  LOAD_FAST                'key'
                8  BINARY_SUBSCR    
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 127        14  DUP_TOP          
               16  LOAD_GLOBAL              KeyError
               18  <121>                40  ''
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L. 128        26  LOAD_FAST                'self'
               28  LOAD_ATTR                existing_entries
               30  LOAD_FAST                'key'
               32  BINARY_SUBSCR    
               34  ROT_FOUR         
               36  POP_EXCEPT       
               38  RETURN_VALUE     
               40  <48>             

Parse error at or near `<121>' instruction at offset 18

    def __delitem__--- This code section failed: ---

 L. 131         0  LOAD_FAST                'key'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                new_entries
                6  <118>                 0  ''
                8  POP_JUMP_IF_FALSE    48  'to 48'

 L. 132        10  LOAD_FAST                'self'
               12  LOAD_ATTR                new_entries
               14  LOAD_FAST                'key'
               16  BINARY_SUBSCR    
               18  LOAD_CONST               1
               20  BINARY_SUBSCR    
               22  LOAD_CONST               1
               24  BINARY_ADD       
               26  STORE_FAST               'generation'

 L. 133        28  LOAD_FAST                'self'
               30  LOAD_ATTR                new_entries
               32  LOAD_FAST                'key'
               34  DELETE_SUBSCR    

 L. 134        36  LOAD_FAST                'generation'
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                deleted_entries
               42  LOAD_FAST                'key'
               44  STORE_SUBSCR     
               46  JUMP_FORWARD        130  'to 130'
             48_0  COME_FROM             8  '8'

 L. 135        48  LOAD_FAST                'key'
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                existing_entries
               54  <118>                 0  ''
               56  POP_JUMP_IF_FALSE    88  'to 88'

 L. 136        58  LOAD_FAST                'self'
               60  LOAD_ATTR                existing_entries
               62  LOAD_FAST                'key'
               64  BINARY_SUBSCR    
               66  LOAD_CONST               1
               68  BINARY_SUBSCR    
               70  LOAD_CONST               1
               72  BINARY_ADD       
               74  STORE_FAST               'generation'

 L. 137        76  LOAD_FAST                'generation'
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                deleted_entries
               82  LOAD_FAST                'key'
               84  STORE_SUBSCR     
               86  JUMP_FORWARD        130  'to 130'
             88_0  COME_FROM            56  '56'

 L. 138        88  LOAD_FAST                'key'
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                deleted_entries
               94  <118>                 0  ''
               96  POP_JUMP_IF_FALSE   110  'to 110'

 L. 139        98  LOAD_FAST                'self'
              100  LOAD_ATTR                deleted_entries
              102  LOAD_FAST                'key'
              104  BINARY_SUBSCR    
              106  STORE_FAST               'generation'
              108  JUMP_FORWARD        130  'to 130'
            110_0  COME_FROM            96  '96'

 L. 141       110  LOAD_GLOBAL              IndexError

 L. 142       112  LOAD_STR                 'object ID '
              114  LOAD_GLOBAL              str
              116  LOAD_FAST                'key'
              118  CALL_FUNCTION_1       1  ''
              120  BINARY_ADD       
              122  LOAD_STR                 " cannot be deleted because it doesn't exist"
              124  BINARY_ADD       

 L. 141       126  CALL_FUNCTION_1       1  ''
              128  RAISE_VARARGS_1       1  'exception instance'
            130_0  COME_FROM           108  '108'
            130_1  COME_FROM            86  '86'
            130_2  COME_FROM            46  '46'

Parse error at or near `None' instruction at offset -1

    def __contains__--- This code section failed: ---

 L. 146         0  LOAD_FAST                'key'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                existing_entries
                6  <118>                 0  ''
                8  JUMP_IF_TRUE_OR_POP    18  'to 18'
               10  LOAD_FAST                'key'
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                new_entries
               16  <118>                 0  ''
             18_0  COME_FROM             8  '8'
               18  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def __len__(self):
        return len(set(self.existing_entries.keys()) | set(self.new_entries.keys()) | set(self.deleted_entries.keys()))

    def keys(self):
        return set(self.existing_entries.keys()) - set(self.deleted_entries.keys()) | set(self.new_entries.keys())

    def write--- This code section failed: ---

 L. 161         0  LOAD_GLOBAL              sorted
                2  LOAD_GLOBAL              set
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                new_entries
                8  LOAD_METHOD              keys
               10  CALL_METHOD_0         0  ''
               12  CALL_FUNCTION_1       1  ''
               14  LOAD_GLOBAL              set
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                deleted_entries
               20  LOAD_METHOD              keys
               22  CALL_METHOD_0         0  ''
               24  CALL_FUNCTION_1       1  ''
               26  BINARY_OR        
               28  CALL_FUNCTION_1       1  ''
               30  STORE_FAST               'keys'

 L. 162        32  LOAD_GLOBAL              sorted
               34  LOAD_GLOBAL              set
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                deleted_entries
               40  LOAD_METHOD              keys
               42  CALL_METHOD_0         0  ''
               44  CALL_FUNCTION_1       1  ''
               46  CALL_FUNCTION_1       1  ''
               48  STORE_FAST               'deleted_keys'

 L. 163        50  LOAD_FAST                'f'
               52  LOAD_METHOD              tell
               54  CALL_METHOD_0         0  ''
               56  STORE_FAST               'startxref'

 L. 164        58  LOAD_FAST                'f'
               60  LOAD_METHOD              write
               62  LOAD_CONST               b'xref\n'
               64  CALL_METHOD_1         1  ''
               66  POP_TOP          

 L. 165        68  LOAD_FAST                'keys'
            70_72  POP_JUMP_IF_FALSE   326  'to 326'

 L. 167        74  LOAD_CONST               None
               76  STORE_FAST               'prev'

 L. 168        78  LOAD_GLOBAL              enumerate
               80  LOAD_FAST                'keys'
               82  CALL_FUNCTION_1       1  ''
               84  GET_ITER         
               86  FOR_ITER            150  'to 150'
               88  UNPACK_SEQUENCE_2     2 
               90  STORE_FAST               'index'
               92  STORE_FAST               'key'

 L. 169        94  LOAD_FAST                'prev'
               96  LOAD_CONST               None
               98  <117>                 0  ''
              100  POP_JUMP_IF_TRUE    114  'to 114'
              102  LOAD_FAST                'prev'
              104  LOAD_CONST               1
              106  BINARY_ADD       
              108  LOAD_FAST                'key'
              110  COMPARE_OP               ==
              112  POP_JUMP_IF_FALSE   120  'to 120'
            114_0  COME_FROM           100  '100'

 L. 170       114  LOAD_FAST                'key'
              116  STORE_FAST               'prev'
              118  JUMP_BACK            86  'to 86'
            120_0  COME_FROM           112  '112'

 L. 172       120  LOAD_FAST                'keys'
              122  LOAD_CONST               None
              124  LOAD_FAST                'index'
              126  BUILD_SLICE_2         2 
              128  BINARY_SUBSCR    
              130  STORE_FAST               'contiguous_keys'

 L. 173       132  LOAD_FAST                'keys'
              134  LOAD_FAST                'index'
              136  LOAD_CONST               None
              138  BUILD_SLICE_2         2 
              140  BINARY_SUBSCR    
              142  STORE_FAST               'keys'

 L. 174       144  POP_TOP          
              146  BREAK_LOOP          158  'to 158'
              148  JUMP_BACK            86  'to 86'

 L. 176       150  LOAD_FAST                'keys'
              152  STORE_FAST               'contiguous_keys'

 L. 177       154  LOAD_CONST               None
              156  STORE_FAST               'keys'

 L. 178       158  LOAD_FAST                'f'
              160  LOAD_METHOD              write
              162  LOAD_CONST               b'%d %d\n'
              164  LOAD_FAST                'contiguous_keys'
              166  LOAD_CONST               0
              168  BINARY_SUBSCR    
              170  LOAD_GLOBAL              len
              172  LOAD_FAST                'contiguous_keys'
              174  CALL_FUNCTION_1       1  ''
              176  BUILD_TUPLE_2         2 
              178  BINARY_MODULO    
              180  CALL_METHOD_1         1  ''
              182  POP_TOP          

 L. 179       184  LOAD_FAST                'contiguous_keys'
              186  GET_ITER         
              188  FOR_ITER            324  'to 324'
              190  STORE_FAST               'object_id'

 L. 180       192  LOAD_FAST                'object_id'
              194  LOAD_FAST                'self'
              196  LOAD_ATTR                new_entries
              198  <118>                 0  ''
              200  POP_JUMP_IF_FALSE   224  'to 224'

 L. 181       202  LOAD_FAST                'f'
              204  LOAD_METHOD              write
              206  LOAD_CONST               b'%010d %05d n \n'
              208  LOAD_FAST                'self'
              210  LOAD_ATTR                new_entries
              212  LOAD_FAST                'object_id'
              214  BINARY_SUBSCR    
              216  BINARY_MODULO    
              218  CALL_METHOD_1         1  ''
              220  POP_TOP          
              222  JUMP_BACK           188  'to 188'
            224_0  COME_FROM           200  '200'

 L. 183       224  LOAD_FAST                'deleted_keys'
              226  LOAD_METHOD              pop
              228  LOAD_CONST               0
              230  CALL_METHOD_1         1  ''
              232  STORE_FAST               'this_deleted_object_id'

 L. 184       234  LOAD_GLOBAL              check_format_condition

 L. 185       236  LOAD_FAST                'object_id'
              238  LOAD_FAST                'this_deleted_object_id'
              240  COMPARE_OP               ==

 L. 186       242  LOAD_STR                 'expected the next deleted object ID to be '
              244  LOAD_FAST                'object_id'
              246  FORMAT_VALUE          0  ''
              248  LOAD_STR                 ', instead found '

 L. 187       250  LOAD_FAST                'this_deleted_object_id'

 L. 186       252  FORMAT_VALUE          0  ''
              254  BUILD_STRING_4        4 

 L. 184       256  CALL_FUNCTION_2       2  ''
              258  POP_TOP          

 L. 189       260  SETUP_FINALLY       274  'to 274'

 L. 190       262  LOAD_FAST                'deleted_keys'
              264  LOAD_CONST               0
              266  BINARY_SUBSCR    
              268  STORE_FAST               'next_in_linked_list'
              270  POP_BLOCK        
              272  JUMP_FORWARD        298  'to 298'
            274_0  COME_FROM_FINALLY   260  '260'

 L. 191       274  DUP_TOP          
              276  LOAD_GLOBAL              IndexError
          278_280  <121>               296  ''
              282  POP_TOP          
              284  POP_TOP          
              286  POP_TOP          

 L. 192       288  LOAD_CONST               0
              290  STORE_FAST               'next_in_linked_list'
              292  POP_EXCEPT       
              294  JUMP_FORWARD        298  'to 298'
              296  <48>             
            298_0  COME_FROM           294  '294'
            298_1  COME_FROM           272  '272'

 L. 193       298  LOAD_FAST                'f'
              300  LOAD_METHOD              write

 L. 194       302  LOAD_CONST               b'%010d %05d f \n'

 L. 195       304  LOAD_FAST                'next_in_linked_list'
              306  LOAD_FAST                'self'
              308  LOAD_ATTR                deleted_entries
              310  LOAD_FAST                'object_id'
              312  BINARY_SUBSCR    
              314  BUILD_TUPLE_2         2 

 L. 194       316  BINARY_MODULO    

 L. 193       318  CALL_METHOD_1         1  ''
              320  POP_TOP          
              322  JUMP_BACK           188  'to 188'
              324  JUMP_BACK            68  'to 68'
            326_0  COME_FROM            70  '70'

 L. 197       326  LOAD_FAST                'startxref'
              328  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 98


class PdfName:

    def __init__(self, name):
        if isinstance(name, PdfName):
            self.name = name.name
        else:
            if isinstance(name, bytes):
                self.name = name
            else:
                self.name = name.encode('us-ascii')

    def name_as_str(self):
        return self.name.decode('us-ascii')

    def __eq__(self, other):
        return isinstance(other, PdfName) and other.name == self.name or other == self.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"PdfName({repr(self.name)})"

    @classmethod
    def from_pdf_stream(cls, data):
        return cls(PdfParser.interpret_name(data))

    allowed_chars = set(range(33, 127)) - {ord(c) for c in '#%/()<>[]{}'}

    def __bytes__--- This code section failed: ---

 L. 230         0  LOAD_GLOBAL              bytearray
                2  LOAD_CONST               b'/'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'result'

 L. 231         8  LOAD_FAST                'self'
               10  LOAD_ATTR                name
               12  GET_ITER         
               14  FOR_ITER             56  'to 56'
               16  STORE_FAST               'b'

 L. 232        18  LOAD_FAST                'b'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                allowed_chars
               24  <118>                 0  ''
               26  POP_JUMP_IF_FALSE    40  'to 40'

 L. 233        28  LOAD_FAST                'result'
               30  LOAD_METHOD              append
               32  LOAD_FAST                'b'
               34  CALL_METHOD_1         1  ''
               36  POP_TOP          
               38  JUMP_BACK            14  'to 14'
             40_0  COME_FROM            26  '26'

 L. 235        40  LOAD_FAST                'result'
               42  LOAD_METHOD              extend
               44  LOAD_CONST               b'#%02X'
               46  LOAD_FAST                'b'
               48  BINARY_MODULO    
               50  CALL_METHOD_1         1  ''
               52  POP_TOP          
               54  JUMP_BACK            14  'to 14'

 L. 236        56  LOAD_GLOBAL              bytes
               58  LOAD_FAST                'result'
               60  CALL_FUNCTION_1       1  ''
               62  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 24


class PdfArray(list):

    def __bytes__(self):
        return b'[ ' + (b' ').join((pdf_repr(x) for x in self)) + b' ]'


class PdfDict(collections.UserDict):

    def __setattr__(self, key, value):
        if key == 'data':
            collections.UserDict.__setattr__(self, key, value)
        else:
            self[key.encode('us-ascii')] = value

    def __getattr__--- This code section failed: ---

 L. 252         0  SETUP_FINALLY        20  'to 20'

 L. 253         2  LOAD_FAST                'self'
                4  LOAD_FAST                'key'
                6  LOAD_METHOD              encode
                8  LOAD_STR                 'us-ascii'
               10  CALL_METHOD_1         1  ''
               12  BINARY_SUBSCR    
               14  STORE_FAST               'value'
               16  POP_BLOCK        
               18  JUMP_FORWARD         66  'to 66'
             20_0  COME_FROM_FINALLY     0  '0'

 L. 254        20  DUP_TOP          
               22  LOAD_GLOBAL              KeyError
               24  <121>                64  ''
               26  POP_TOP          
               28  STORE_FAST               'e'
               30  POP_TOP          
               32  SETUP_FINALLY        56  'to 56'

 L. 255        34  LOAD_GLOBAL              AttributeError
               36  LOAD_FAST                'key'
               38  CALL_FUNCTION_1       1  ''
               40  LOAD_FAST                'e'
               42  RAISE_VARARGS_2       2  'exception instance with __cause__'
               44  POP_BLOCK        
               46  POP_EXCEPT       
               48  LOAD_CONST               None
               50  STORE_FAST               'e'
               52  DELETE_FAST              'e'
               54  JUMP_FORWARD         66  'to 66'
             56_0  COME_FROM_FINALLY    32  '32'
               56  LOAD_CONST               None
               58  STORE_FAST               'e'
               60  DELETE_FAST              'e'
               62  <48>             
               64  <48>             
             66_0  COME_FROM            54  '54'
             66_1  COME_FROM            18  '18'

 L. 256        66  LOAD_GLOBAL              isinstance
               68  LOAD_FAST                'value'
               70  LOAD_GLOBAL              bytes
               72  CALL_FUNCTION_2       2  ''
               74  POP_JUMP_IF_FALSE    84  'to 84'

 L. 257        76  LOAD_GLOBAL              decode_text
               78  LOAD_FAST                'value'
               80  CALL_FUNCTION_1       1  ''
               82  STORE_FAST               'value'
             84_0  COME_FROM            74  '74'

 L. 258        84  LOAD_FAST                'key'
               86  LOAD_METHOD              endswith
               88  LOAD_STR                 'Date'
               90  CALL_METHOD_1         1  ''
            92_94  POP_JUMP_IF_FALSE   298  'to 298'

 L. 259        96  LOAD_FAST                'value'
               98  LOAD_METHOD              startswith
              100  LOAD_STR                 'D:'
              102  CALL_METHOD_1         1  ''
              104  POP_JUMP_IF_FALSE   118  'to 118'

 L. 260       106  LOAD_FAST                'value'
              108  LOAD_CONST               2
              110  LOAD_CONST               None
              112  BUILD_SLICE_2         2 
              114  BINARY_SUBSCR    
              116  STORE_FAST               'value'
            118_0  COME_FROM           104  '104'

 L. 262       118  LOAD_STR                 'Z'
              120  STORE_FAST               'relationship'

 L. 263       122  LOAD_GLOBAL              len
              124  LOAD_FAST                'value'
              126  CALL_FUNCTION_1       1  ''
              128  LOAD_CONST               17
              130  COMPARE_OP               >
              132  POP_JUMP_IF_FALSE   194  'to 194'

 L. 264       134  LOAD_FAST                'value'
              136  LOAD_CONST               14
              138  BINARY_SUBSCR    
              140  STORE_FAST               'relationship'

 L. 265       142  LOAD_GLOBAL              int
              144  LOAD_FAST                'value'
              146  LOAD_CONST               15
              148  LOAD_CONST               17
              150  BUILD_SLICE_2         2 
              152  BINARY_SUBSCR    
              154  CALL_FUNCTION_1       1  ''
              156  LOAD_CONST               60
              158  BINARY_MULTIPLY  
              160  STORE_FAST               'offset'

 L. 266       162  LOAD_GLOBAL              len
              164  LOAD_FAST                'value'
              166  CALL_FUNCTION_1       1  ''
              168  LOAD_CONST               20
              170  COMPARE_OP               >
              172  POP_JUMP_IF_FALSE   194  'to 194'

 L. 267       174  LOAD_FAST                'offset'
              176  LOAD_GLOBAL              int
              178  LOAD_FAST                'value'
              180  LOAD_CONST               18
              182  LOAD_CONST               20
              184  BUILD_SLICE_2         2 
              186  BINARY_SUBSCR    
              188  CALL_FUNCTION_1       1  ''
              190  INPLACE_ADD      
              192  STORE_FAST               'offset'
            194_0  COME_FROM           172  '172'
            194_1  COME_FROM           132  '132'

 L. 269       194  LOAD_STR                 '%Y%m%d%H%M%S'
              196  LOAD_CONST               None
              198  LOAD_GLOBAL              len
              200  LOAD_FAST                'value'
              202  CALL_FUNCTION_1       1  ''
              204  LOAD_CONST               2
              206  BINARY_SUBTRACT  
              208  BUILD_SLICE_2         2 
              210  BINARY_SUBSCR    
              212  STORE_FAST               'format'

 L. 270       214  LOAD_GLOBAL              time
              216  LOAD_METHOD              strptime
              218  LOAD_FAST                'value'
              220  LOAD_CONST               None
              222  LOAD_GLOBAL              len
              224  LOAD_FAST                'format'
              226  CALL_FUNCTION_1       1  ''
              228  LOAD_CONST               2
              230  BINARY_ADD       
              232  BUILD_SLICE_2         2 
              234  BINARY_SUBSCR    
              236  LOAD_FAST                'format'
              238  CALL_METHOD_2         2  ''
              240  STORE_FAST               'value'

 L. 271       242  LOAD_FAST                'relationship'
              244  LOAD_CONST               ('+', '-')
              246  <118>                 0  ''
          248_250  POP_JUMP_IF_FALSE   298  'to 298'

 L. 272       252  LOAD_FAST                'offset'
              254  LOAD_CONST               60
              256  INPLACE_MULTIPLY 
              258  STORE_FAST               'offset'

 L. 273       260  LOAD_FAST                'relationship'
              262  LOAD_STR                 '+'
              264  COMPARE_OP               ==
          266_268  POP_JUMP_IF_FALSE   278  'to 278'

 L. 274       270  LOAD_FAST                'offset'
              272  LOAD_CONST               -1
              274  INPLACE_MULTIPLY 
              276  STORE_FAST               'offset'
            278_0  COME_FROM           266  '266'

 L. 275       278  LOAD_GLOBAL              time
              280  LOAD_METHOD              gmtime
              282  LOAD_GLOBAL              calendar
              284  LOAD_METHOD              timegm
              286  LOAD_FAST                'value'
              288  CALL_METHOD_1         1  ''
              290  LOAD_FAST                'offset'
              292  BINARY_ADD       
              294  CALL_METHOD_1         1  ''
              296  STORE_FAST               'value'
            298_0  COME_FROM           248  '248'
            298_1  COME_FROM            92  '92'

 L. 276       298  LOAD_FAST                'value'
              300  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 24

    def __bytes__--- This code section failed: ---

 L. 279         0  LOAD_GLOBAL              bytearray
                2  LOAD_CONST               b'<<'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'out'

 L. 280         8  LOAD_FAST                'self'
               10  LOAD_METHOD              items
               12  CALL_METHOD_0         0  ''
               14  GET_ITER         
               16  FOR_ITER             92  'to 92'
               18  UNPACK_SEQUENCE_2     2 
               20  STORE_FAST               'key'
               22  STORE_FAST               'value'

 L. 281        24  LOAD_FAST                'value'
               26  LOAD_CONST               None
               28  <117>                 0  ''
               30  POP_JUMP_IF_FALSE    34  'to 34'

 L. 282        32  JUMP_BACK            16  'to 16'
             34_0  COME_FROM            30  '30'

 L. 283        34  LOAD_GLOBAL              pdf_repr
               36  LOAD_FAST                'value'
               38  CALL_FUNCTION_1       1  ''
               40  STORE_FAST               'value'

 L. 284        42  LOAD_FAST                'out'
               44  LOAD_METHOD              extend
               46  LOAD_CONST               b'\n'
               48  CALL_METHOD_1         1  ''
               50  POP_TOP          

 L. 285        52  LOAD_FAST                'out'
               54  LOAD_METHOD              extend
               56  LOAD_GLOBAL              bytes
               58  LOAD_GLOBAL              PdfName
               60  LOAD_FAST                'key'
               62  CALL_FUNCTION_1       1  ''
               64  CALL_FUNCTION_1       1  ''
               66  CALL_METHOD_1         1  ''
               68  POP_TOP          

 L. 286        70  LOAD_FAST                'out'
               72  LOAD_METHOD              extend
               74  LOAD_CONST               b' '
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          

 L. 287        80  LOAD_FAST                'out'
               82  LOAD_METHOD              extend
               84  LOAD_FAST                'value'
               86  CALL_METHOD_1         1  ''
               88  POP_TOP          
               90  JUMP_BACK            16  'to 16'

 L. 288        92  LOAD_FAST                'out'
               94  LOAD_METHOD              extend
               96  LOAD_CONST               b'\n>>'
               98  CALL_METHOD_1         1  ''
              100  POP_TOP          

 L. 289       102  LOAD_GLOBAL              bytes
              104  LOAD_FAST                'out'
              106  CALL_FUNCTION_1       1  ''
              108  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 28


class PdfBinary:

    def __init__(self, data):
        self.data = data

    def __bytes__(self):
        return b'<%s>' % (b'').join((b'%02X' % b for b in self.data))


class PdfStream:

    def __init__(self, dictionary, buf):
        self.dictionary = dictionary
        self.buf = buf

    def decode--- This code section failed: ---

 L. 306         0  SETUP_FINALLY        14  'to 14'

 L. 307         2  LOAD_FAST                'self'
                4  LOAD_ATTR                dictionary
                6  LOAD_ATTR                Filter
                8  STORE_FAST               'filter'
               10  POP_BLOCK        
               12  JUMP_FORWARD         38  'to 38'
             14_0  COME_FROM_FINALLY     0  '0'

 L. 308        14  DUP_TOP          
               16  LOAD_GLOBAL              AttributeError
               18  <121>                36  ''
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L. 309        26  LOAD_FAST                'self'
               28  LOAD_ATTR                buf
               30  ROT_FOUR         
               32  POP_EXCEPT       
               34  RETURN_VALUE     
               36  <48>             
             38_0  COME_FROM            12  '12'

 L. 310        38  LOAD_FAST                'filter'
               40  LOAD_CONST               b'FlateDecode'
               42  COMPARE_OP               ==
               44  POP_JUMP_IF_FALSE   106  'to 106'

 L. 311        46  SETUP_FINALLY        60  'to 60'

 L. 312        48  LOAD_FAST                'self'
               50  LOAD_ATTR                dictionary
               52  LOAD_ATTR                DL
               54  STORE_FAST               'expected_length'
               56  POP_BLOCK        
               58  JUMP_FORWARD         86  'to 86'
             60_0  COME_FROM_FINALLY    46  '46'

 L. 313        60  DUP_TOP          
               62  LOAD_GLOBAL              AttributeError
               64  <121>                84  ''
               66  POP_TOP          
               68  POP_TOP          
               70  POP_TOP          

 L. 314        72  LOAD_FAST                'self'
               74  LOAD_ATTR                dictionary
               76  LOAD_ATTR                Length
               78  STORE_FAST               'expected_length'
               80  POP_EXCEPT       
               82  JUMP_FORWARD         86  'to 86'
               84  <48>             
             86_0  COME_FROM            82  '82'
             86_1  COME_FROM            58  '58'

 L. 315        86  LOAD_GLOBAL              zlib
               88  LOAD_ATTR                decompress
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                buf
               94  LOAD_GLOBAL              int
               96  LOAD_FAST                'expected_length'
               98  CALL_FUNCTION_1       1  ''
              100  LOAD_CONST               ('bufsize',)
              102  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              104  RETURN_VALUE     
            106_0  COME_FROM            44  '44'

 L. 317       106  LOAD_GLOBAL              NotImplementedError

 L. 318       108  LOAD_STR                 'stream filter '
              110  LOAD_GLOBAL              repr
              112  LOAD_FAST                'self'
              114  LOAD_ATTR                dictionary
              116  LOAD_ATTR                Filter
              118  CALL_FUNCTION_1       1  ''
              120  FORMAT_VALUE          0  ''
              122  LOAD_STR                 ' unknown/unsupported'
              124  BUILD_STRING_3        3 

 L. 317       126  CALL_FUNCTION_1       1  ''
              128  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<121>' instruction at offset 18


def pdf_repr--- This code section failed: ---

 L. 323         0  LOAD_FAST                'x'
                2  LOAD_CONST               True
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 324         8  LOAD_CONST               b'true'
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L. 325        12  LOAD_FAST                'x'
               14  LOAD_CONST               False
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    24  'to 24'

 L. 326        20  LOAD_CONST               b'false'
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L. 327        24  LOAD_FAST                'x'
               26  LOAD_CONST               None
               28  <117>                 0  ''
               30  POP_JUMP_IF_FALSE    36  'to 36'

 L. 328        32  LOAD_CONST               b'null'
               34  RETURN_VALUE     
             36_0  COME_FROM            30  '30'

 L. 329        36  LOAD_GLOBAL              isinstance
               38  LOAD_FAST                'x'
               40  LOAD_GLOBAL              PdfName
               42  LOAD_GLOBAL              PdfDict
               44  LOAD_GLOBAL              PdfArray
               46  LOAD_GLOBAL              PdfBinary
               48  BUILD_TUPLE_4         4 
               50  CALL_FUNCTION_2       2  ''
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L. 330        54  LOAD_GLOBAL              bytes
               56  LOAD_FAST                'x'
               58  CALL_FUNCTION_1       1  ''
               60  RETURN_VALUE     
             62_0  COME_FROM            52  '52'

 L. 331        62  LOAD_GLOBAL              isinstance
               64  LOAD_FAST                'x'
               66  LOAD_GLOBAL              int
               68  CALL_FUNCTION_2       2  ''
               70  POP_JUMP_IF_FALSE    86  'to 86'

 L. 332        72  LOAD_GLOBAL              str
               74  LOAD_FAST                'x'
               76  CALL_FUNCTION_1       1  ''
               78  LOAD_METHOD              encode
               80  LOAD_STR                 'us-ascii'
               82  CALL_METHOD_1         1  ''
               84  RETURN_VALUE     
             86_0  COME_FROM            70  '70'

 L. 333        86  LOAD_GLOBAL              isinstance
               88  LOAD_FAST                'x'
               90  LOAD_GLOBAL              time
               92  LOAD_ATTR                struct_time
               94  CALL_FUNCTION_2       2  ''
               96  POP_JUMP_IF_FALSE   124  'to 124'

 L. 334        98  LOAD_CONST               b'(D:'
              100  LOAD_GLOBAL              time
              102  LOAD_METHOD              strftime
              104  LOAD_STR                 '%Y%m%d%H%M%SZ'
              106  LOAD_FAST                'x'
              108  CALL_METHOD_2         2  ''
              110  LOAD_METHOD              encode
              112  LOAD_STR                 'us-ascii'
              114  CALL_METHOD_1         1  ''
              116  BINARY_ADD       
              118  LOAD_CONST               b')'
              120  BINARY_ADD       
              122  RETURN_VALUE     
            124_0  COME_FROM            96  '96'

 L. 335       124  LOAD_GLOBAL              isinstance
              126  LOAD_FAST                'x'
              128  LOAD_GLOBAL              dict
              130  CALL_FUNCTION_2       2  ''
              132  POP_JUMP_IF_FALSE   146  'to 146'

 L. 336       134  LOAD_GLOBAL              bytes
              136  LOAD_GLOBAL              PdfDict
              138  LOAD_FAST                'x'
              140  CALL_FUNCTION_1       1  ''
              142  CALL_FUNCTION_1       1  ''
              144  RETURN_VALUE     
            146_0  COME_FROM           132  '132'

 L. 337       146  LOAD_GLOBAL              isinstance
              148  LOAD_FAST                'x'
              150  LOAD_GLOBAL              list
              152  CALL_FUNCTION_2       2  ''
              154  POP_JUMP_IF_FALSE   168  'to 168'

 L. 338       156  LOAD_GLOBAL              bytes
              158  LOAD_GLOBAL              PdfArray
              160  LOAD_FAST                'x'
              162  CALL_FUNCTION_1       1  ''
              164  CALL_FUNCTION_1       1  ''
              166  RETURN_VALUE     
            168_0  COME_FROM           154  '154'

 L. 339       168  LOAD_GLOBAL              isinstance
              170  LOAD_FAST                'x'
              172  LOAD_GLOBAL              str
              174  CALL_FUNCTION_2       2  ''
              176  POP_JUMP_IF_FALSE   190  'to 190'

 L. 340       178  LOAD_GLOBAL              pdf_repr
              180  LOAD_GLOBAL              encode_text
              182  LOAD_FAST                'x'
              184  CALL_FUNCTION_1       1  ''
              186  CALL_FUNCTION_1       1  ''
              188  RETURN_VALUE     
            190_0  COME_FROM           176  '176'

 L. 341       190  LOAD_GLOBAL              isinstance
              192  LOAD_FAST                'x'
              194  LOAD_GLOBAL              bytes
              196  CALL_FUNCTION_2       2  ''
          198_200  POP_JUMP_IF_FALSE   250  'to 250'

 L. 343       202  LOAD_FAST                'x'
              204  LOAD_METHOD              replace
              206  LOAD_CONST               b'\\'
              208  LOAD_CONST               b'\\\\'
              210  CALL_METHOD_2         2  ''
              212  STORE_FAST               'x'

 L. 344       214  LOAD_FAST                'x'
              216  LOAD_METHOD              replace
              218  LOAD_CONST               b'('
              220  LOAD_CONST               b'\\('
              222  CALL_METHOD_2         2  ''
              224  STORE_FAST               'x'

 L. 345       226  LOAD_FAST                'x'
              228  LOAD_METHOD              replace
              230  LOAD_CONST               b')'
              232  LOAD_CONST               b'\\)'
              234  CALL_METHOD_2         2  ''
              236  STORE_FAST               'x'

 L. 346       238  LOAD_CONST               b'('
              240  LOAD_FAST                'x'
              242  BINARY_ADD       
              244  LOAD_CONST               b')'
              246  BINARY_ADD       
              248  RETURN_VALUE     
            250_0  COME_FROM           198  '198'

 L. 348       250  LOAD_GLOBAL              bytes
              252  LOAD_FAST                'x'
              254  CALL_FUNCTION_1       1  ''
              256  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1


class PdfParser:
    __doc__ = 'Based on\n    https://www.adobe.com/content/dam/acom/en/devnet/acrobat/pdfs/PDF32000_2008.pdf\n    Supports PDF up to 1.4\n    '

    def __init__--- This code section failed: ---

 L. 358         0  LOAD_FAST                'buf'
                2  POP_JUMP_IF_FALSE    16  'to 16'
                4  LOAD_FAST                'f'
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 359         8  LOAD_GLOBAL              RuntimeError
               10  LOAD_STR                 'specify buf or f or filename, but not both buf and f'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'
             16_1  COME_FROM             2  '2'

 L. 360        16  LOAD_FAST                'filename'
               18  LOAD_FAST                'self'
               20  STORE_ATTR               filename

 L. 361        22  LOAD_FAST                'buf'
               24  LOAD_FAST                'self'
               26  STORE_ATTR               buf

 L. 362        28  LOAD_FAST                'f'
               30  LOAD_FAST                'self'
               32  STORE_ATTR               f

 L. 363        34  LOAD_FAST                'start_offset'
               36  LOAD_FAST                'self'
               38  STORE_ATTR               start_offset

 L. 364        40  LOAD_CONST               False
               42  LOAD_FAST                'self'
               44  STORE_ATTR               should_close_buf

 L. 365        46  LOAD_CONST               False
               48  LOAD_FAST                'self'
               50  STORE_ATTR               should_close_file

 L. 366        52  LOAD_FAST                'filename'
               54  LOAD_CONST               None
               56  <117>                 1  ''
               58  POP_JUMP_IF_FALSE    90  'to 90'
               60  LOAD_FAST                'f'
               62  LOAD_CONST               None
               64  <117>                 0  ''
               66  POP_JUMP_IF_FALSE    90  'to 90'

 L. 367        68  LOAD_GLOBAL              open
               70  LOAD_FAST                'filename'
               72  LOAD_FAST                'mode'
               74  CALL_FUNCTION_2       2  ''
               76  DUP_TOP          
               78  LOAD_FAST                'self'
               80  STORE_ATTR               f
               82  STORE_FAST               'f'

 L. 368        84  LOAD_CONST               True
               86  LOAD_FAST                'self'
               88  STORE_ATTR               should_close_file
             90_0  COME_FROM            66  '66'
             90_1  COME_FROM            58  '58'

 L. 369        90  LOAD_FAST                'f'
               92  LOAD_CONST               None
               94  <117>                 1  ''
               96  POP_JUMP_IF_FALSE   142  'to 142'

 L. 370        98  LOAD_FAST                'self'
              100  LOAD_METHOD              get_buf_from_file
              102  LOAD_FAST                'f'
              104  CALL_METHOD_1         1  ''
              106  DUP_TOP          
              108  LOAD_FAST                'self'
              110  STORE_ATTR               buf
              112  STORE_FAST               'buf'

 L. 371       114  LOAD_CONST               True
              116  LOAD_FAST                'self'
              118  STORE_ATTR               should_close_buf

 L. 372       120  LOAD_FAST                'filename'
              122  POP_JUMP_IF_TRUE    142  'to 142'
              124  LOAD_GLOBAL              hasattr
              126  LOAD_FAST                'f'
              128  LOAD_STR                 'name'
              130  CALL_FUNCTION_2       2  ''
              132  POP_JUMP_IF_FALSE   142  'to 142'

 L. 373       134  LOAD_FAST                'f'
              136  LOAD_ATTR                name
              138  LOAD_FAST                'self'
              140  STORE_ATTR               filename
            142_0  COME_FROM           132  '132'
            142_1  COME_FROM           122  '122'
            142_2  COME_FROM            96  '96'

 L. 374       142  BUILD_MAP_0           0 
              144  LOAD_FAST                'self'
              146  STORE_ATTR               cached_objects

 L. 375       148  LOAD_FAST                'buf'
              150  POP_JUMP_IF_FALSE   162  'to 162'

 L. 376       152  LOAD_FAST                'self'
              154  LOAD_METHOD              read_pdf_info
              156  CALL_METHOD_0         0  ''
              158  POP_TOP          
              160  JUMP_FORWARD        246  'to 246'
            162_0  COME_FROM           150  '150'

 L. 378       162  LOAD_CONST               0
              164  DUP_TOP          
              166  LOAD_FAST                'self'
              168  STORE_ATTR               file_size_total
              170  LOAD_FAST                'self'
              172  STORE_ATTR               file_size_this

 L. 379       174  LOAD_GLOBAL              PdfDict
              176  CALL_FUNCTION_0       0  ''
              178  LOAD_FAST                'self'
              180  STORE_ATTR               root

 L. 380       182  LOAD_CONST               None
              184  LOAD_FAST                'self'
              186  STORE_ATTR               root_ref

 L. 381       188  LOAD_GLOBAL              PdfDict
              190  CALL_FUNCTION_0       0  ''
              192  LOAD_FAST                'self'
              194  STORE_ATTR               info

 L. 382       196  LOAD_CONST               None
              198  LOAD_FAST                'self'
              200  STORE_ATTR               info_ref

 L. 383       202  BUILD_MAP_0           0 
              204  LOAD_FAST                'self'
              206  STORE_ATTR               page_tree_root

 L. 384       208  BUILD_LIST_0          0 
              210  LOAD_FAST                'self'
              212  STORE_ATTR               pages

 L. 385       214  BUILD_LIST_0          0 
              216  LOAD_FAST                'self'
              218  STORE_ATTR               orig_pages

 L. 386       220  LOAD_CONST               None
              222  LOAD_FAST                'self'
              224  STORE_ATTR               pages_ref

 L. 387       226  LOAD_CONST               None
              228  LOAD_FAST                'self'
              230  STORE_ATTR               last_xref_section_offset

 L. 388       232  BUILD_MAP_0           0 
              234  LOAD_FAST                'self'
              236  STORE_ATTR               trailer_dict

 L. 389       238  LOAD_GLOBAL              XrefTable
              240  CALL_FUNCTION_0       0  ''
              242  LOAD_FAST                'self'
              244  STORE_ATTR               xref_table
            246_0  COME_FROM           160  '160'

 L. 390       246  LOAD_CONST               True
              248  LOAD_FAST                'self'
              250  LOAD_ATTR                xref_table
              252  STORE_ATTR               reading_finished

 L. 391       254  LOAD_FAST                'f'
          256_258  POP_JUMP_IF_FALSE   268  'to 268'

 L. 392       260  LOAD_FAST                'self'
              262  LOAD_METHOD              seek_end
              264  CALL_METHOD_0         0  ''
              266  POP_TOP          
            268_0  COME_FROM           256  '256'

Parse error at or near `<117>' instruction at offset 56

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return False

    def start_writing(self):
        self.close_buf()
        self.seek_end()

    def close_buf--- This code section failed: ---

 L. 406         0  SETUP_FINALLY        16  'to 16'

 L. 407         2  LOAD_FAST                'self'
                4  LOAD_ATTR                buf
                6  LOAD_METHOD              close
                8  CALL_METHOD_0         0  ''
               10  POP_TOP          
               12  POP_BLOCK        
               14  JUMP_FORWARD         34  'to 34'
             16_0  COME_FROM_FINALLY     0  '0'

 L. 408        16  DUP_TOP          
               18  LOAD_GLOBAL              AttributeError
               20  <121>                32  ''
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L. 409        28  POP_EXCEPT       
               30  JUMP_FORWARD         34  'to 34'
               32  <48>             
             34_0  COME_FROM            30  '30'
             34_1  COME_FROM            14  '14'

 L. 410        34  LOAD_CONST               None
               36  LOAD_FAST                'self'
               38  STORE_ATTR               buf

Parse error at or near `<121>' instruction at offset 20

    def close--- This code section failed: ---

 L. 413         0  LOAD_FAST                'self'
                2  LOAD_ATTR                should_close_buf
                4  POP_JUMP_IF_FALSE    14  'to 14'

 L. 414         6  LOAD_FAST                'self'
                8  LOAD_METHOD              close_buf
               10  CALL_METHOD_0         0  ''
               12  POP_TOP          
             14_0  COME_FROM             4  '4'

 L. 415        14  LOAD_FAST                'self'
               16  LOAD_ATTR                f
               18  LOAD_CONST               None
               20  <117>                 1  ''
               22  POP_JUMP_IF_FALSE    46  'to 46'
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                should_close_file
               28  POP_JUMP_IF_FALSE    46  'to 46'

 L. 416        30  LOAD_FAST                'self'
               32  LOAD_ATTR                f
               34  LOAD_METHOD              close
               36  CALL_METHOD_0         0  ''
               38  POP_TOP          

 L. 417        40  LOAD_CONST               None
               42  LOAD_FAST                'self'
               44  STORE_ATTR               f
             46_0  COME_FROM            28  '28'
             46_1  COME_FROM            22  '22'

Parse error at or near `<117>' instruction at offset 20

    def seek_end(self):
        self.f.seek(0, os.SEEK_END)

    def write_header(self):
        self.f.write(b'%PDF-1.4\n')

    def write_comment(self, s):
        self.f.write(f"% {s}\n".encode('utf-8'))

    def write_catalog(self):
        self.del_root()
        self.root_ref = self.next_object_id(self.f.tell())
        self.pages_ref = self.next_object_id(0)
        self.rewrite_pages()
        self.write_obj((self.root_ref), Type=(PdfName(b'Catalog')), Pages=(self.pages_ref))
        self.write_obj((self.pages_ref),
          Type=(PdfName(b'Pages')),
          Count=(len(self.pages)),
          Kids=(self.pages))
        return self.root_ref

    def rewrite_pages--- This code section failed: ---

 L. 443         0  BUILD_LIST_0          0 
                2  STORE_FAST               'pages_tree_nodes_to_delete'

 L. 444         4  LOAD_GLOBAL              enumerate
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                orig_pages
               10  CALL_FUNCTION_1       1  ''
               12  GET_ITER         
               14  FOR_ITER            172  'to 172'
               16  UNPACK_SEQUENCE_2     2 
               18  STORE_FAST               'i'
               20  STORE_FAST               'page_ref'

 L. 445        22  LOAD_FAST                'self'
               24  LOAD_ATTR                cached_objects
               26  LOAD_FAST                'page_ref'
               28  BINARY_SUBSCR    
               30  STORE_FAST               'page_info'

 L. 446        32  LOAD_FAST                'self'
               34  LOAD_ATTR                xref_table
               36  LOAD_FAST                'page_ref'
               38  LOAD_ATTR                object_id
               40  DELETE_SUBSCR    

 L. 447        42  LOAD_FAST                'pages_tree_nodes_to_delete'
               44  LOAD_METHOD              append
               46  LOAD_FAST                'page_info'
               48  LOAD_GLOBAL              PdfName
               50  LOAD_CONST               b'Parent'
               52  CALL_FUNCTION_1       1  ''
               54  BINARY_SUBSCR    
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          

 L. 448        60  LOAD_FAST                'page_ref'
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                pages
               66  <118>                 1  ''
               68  POP_JUMP_IF_FALSE    72  'to 72'

 L. 450        70  JUMP_BACK            14  'to 14'
             72_0  COME_FROM            68  '68'

 L. 452        72  BUILD_MAP_0           0 
               74  STORE_FAST               'stringified_page_info'

 L. 453        76  LOAD_FAST                'page_info'
               78  LOAD_METHOD              items
               80  CALL_METHOD_0         0  ''
               82  GET_ITER         
               84  FOR_ITER            106  'to 106'
               86  UNPACK_SEQUENCE_2     2 
               88  STORE_FAST               'key'
               90  STORE_FAST               'value'

 L. 455        92  LOAD_FAST                'value'
               94  LOAD_FAST                'stringified_page_info'
               96  LOAD_FAST                'key'
               98  LOAD_METHOD              name_as_str
              100  CALL_METHOD_0         0  ''
              102  STORE_SUBSCR     
              104  JUMP_BACK            84  'to 84'

 L. 456       106  LOAD_FAST                'self'
              108  LOAD_ATTR                pages_ref
              110  LOAD_FAST                'stringified_page_info'
              112  LOAD_STR                 'Parent'
              114  STORE_SUBSCR     

 L. 457       116  LOAD_FAST                'self'
              118  LOAD_ATTR                write_page
              120  LOAD_CONST               (None,)
              122  BUILD_MAP_0           0 
              124  LOAD_FAST                'stringified_page_info'
              126  <164>                 1  ''
              128  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              130  STORE_FAST               'new_page_ref'

 L. 458       132  LOAD_GLOBAL              enumerate
              134  LOAD_FAST                'self'
              136  LOAD_ATTR                pages
              138  CALL_FUNCTION_1       1  ''
              140  GET_ITER         
            142_0  COME_FROM           156  '156'
              142  FOR_ITER            170  'to 170'
              144  UNPACK_SEQUENCE_2     2 
              146  STORE_FAST               'j'
              148  STORE_FAST               'cur_page_ref'

 L. 459       150  LOAD_FAST                'cur_page_ref'
              152  LOAD_FAST                'page_ref'
              154  COMPARE_OP               ==
              156  POP_JUMP_IF_FALSE   142  'to 142'

 L. 461       158  LOAD_FAST                'new_page_ref'
              160  LOAD_FAST                'self'
              162  LOAD_ATTR                pages
              164  LOAD_FAST                'j'
              166  STORE_SUBSCR     
              168  JUMP_BACK           142  'to 142'
              170  JUMP_BACK            14  'to 14'

 L. 463       172  LOAD_FAST                'pages_tree_nodes_to_delete'
              174  GET_ITER         
            176_0  COME_FROM           182  '182'
              176  FOR_ITER            232  'to 232'
              178  STORE_FAST               'pages_tree_node_ref'

 L. 464       180  LOAD_FAST                'pages_tree_node_ref'
              182  POP_JUMP_IF_FALSE   176  'to 176'

 L. 465       184  LOAD_FAST                'self'
              186  LOAD_ATTR                cached_objects
              188  LOAD_FAST                'pages_tree_node_ref'
              190  BINARY_SUBSCR    
              192  STORE_FAST               'pages_tree_node'

 L. 466       194  LOAD_FAST                'pages_tree_node_ref'
              196  LOAD_ATTR                object_id
              198  LOAD_FAST                'self'
              200  LOAD_ATTR                xref_table
              202  <118>                 0  ''
              204  POP_JUMP_IF_FALSE   216  'to 216'

 L. 467       206  LOAD_FAST                'self'
              208  LOAD_ATTR                xref_table
              210  LOAD_FAST                'pages_tree_node_ref'
              212  LOAD_ATTR                object_id
              214  DELETE_SUBSCR    
            216_0  COME_FROM           204  '204'

 L. 468       216  LOAD_FAST                'pages_tree_node'
              218  LOAD_METHOD              get
              220  LOAD_CONST               b'Parent'
              222  LOAD_CONST               None
              224  CALL_METHOD_2         2  ''
              226  STORE_FAST               'pages_tree_node_ref'
              228  JUMP_BACK           180  'to 180'
              230  JUMP_BACK           176  'to 176'

 L. 469       232  BUILD_LIST_0          0 
              234  LOAD_FAST                'self'
              236  STORE_ATTR               orig_pages

Parse error at or near `<118>' instruction at offset 66

    def write_xref_and_trailer--- This code section failed: ---

 L. 472         0  LOAD_FAST                'new_root_ref'
                2  POP_JUMP_IF_FALSE    18  'to 18'

 L. 473         4  LOAD_FAST                'self'
                6  LOAD_METHOD              del_root
                8  CALL_METHOD_0         0  ''
               10  POP_TOP          

 L. 474        12  LOAD_FAST                'new_root_ref'
               14  LOAD_FAST                'self'
               16  STORE_ATTR               root_ref
             18_0  COME_FROM             2  '2'

 L. 475        18  LOAD_FAST                'self'
               20  LOAD_ATTR                info
               22  POP_JUMP_IF_FALSE    40  'to 40'

 L. 476        24  LOAD_FAST                'self'
               26  LOAD_METHOD              write_obj
               28  LOAD_CONST               None
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                info
               34  CALL_METHOD_2         2  ''
               36  LOAD_FAST                'self'
               38  STORE_ATTR               info_ref
             40_0  COME_FROM            22  '22'

 L. 477        40  LOAD_FAST                'self'
               42  LOAD_ATTR                xref_table
               44  LOAD_METHOD              write
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                f
               50  CALL_METHOD_1         1  ''
               52  STORE_FAST               'start_xref'

 L. 478        54  LOAD_GLOBAL              len
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                xref_table
               60  CALL_FUNCTION_1       1  ''
               62  STORE_FAST               'num_entries'

 L. 479        64  LOAD_FAST                'self'
               66  LOAD_ATTR                root_ref
               68  LOAD_FAST                'num_entries'
               70  LOAD_CONST               (b'Root', b'Size')
               72  BUILD_CONST_KEY_MAP_2     2 
               74  STORE_FAST               'trailer_dict'

 L. 480        76  LOAD_FAST                'self'
               78  LOAD_ATTR                last_xref_section_offset
               80  LOAD_CONST               None
               82  <117>                 1  ''
               84  POP_JUMP_IF_FALSE    96  'to 96'

 L. 481        86  LOAD_FAST                'self'
               88  LOAD_ATTR                last_xref_section_offset
               90  LOAD_FAST                'trailer_dict'
               92  LOAD_CONST               b'Prev'
               94  STORE_SUBSCR     
             96_0  COME_FROM            84  '84'

 L. 482        96  LOAD_FAST                'self'
               98  LOAD_ATTR                info
              100  POP_JUMP_IF_FALSE   112  'to 112'

 L. 483       102  LOAD_FAST                'self'
              104  LOAD_ATTR                info_ref
              106  LOAD_FAST                'trailer_dict'
              108  LOAD_CONST               b'Info'
              110  STORE_SUBSCR     
            112_0  COME_FROM           100  '100'

 L. 484       112  LOAD_FAST                'start_xref'
              114  LOAD_FAST                'self'
              116  STORE_ATTR               last_xref_section_offset

 L. 485       118  LOAD_FAST                'self'
              120  LOAD_ATTR                f
              122  LOAD_METHOD              write

 L. 486       124  LOAD_CONST               b'trailer\n'

 L. 487       126  LOAD_GLOBAL              bytes
              128  LOAD_GLOBAL              PdfDict
              130  LOAD_FAST                'trailer_dict'
              132  CALL_FUNCTION_1       1  ''
              134  CALL_FUNCTION_1       1  ''

 L. 486       136  BINARY_ADD       

 L. 488       138  LOAD_CONST               b'\nstartxref\n%d\n%%%%EOF'
              140  LOAD_FAST                'start_xref'
              142  BINARY_MODULO    

 L. 486       144  BINARY_ADD       

 L. 485       146  CALL_METHOD_1         1  ''
              148  POP_TOP          

Parse error at or near `<117>' instruction at offset 82

    def write_page--- This code section failed: ---

 L. 492         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'ref'
                4  LOAD_GLOBAL              int
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    20  'to 20'

 L. 493        10  LOAD_FAST                'self'
               12  LOAD_ATTR                pages
               14  LOAD_FAST                'ref'
               16  BINARY_SUBSCR    
               18  STORE_FAST               'ref'
             20_0  COME_FROM             8  '8'

 L. 494        20  LOAD_STR                 'Type'
               22  LOAD_FAST                'dict_obj'
               24  <118>                 1  ''
               26  POP_JUMP_IF_FALSE    40  'to 40'

 L. 495        28  LOAD_GLOBAL              PdfName
               30  LOAD_CONST               b'Page'
               32  CALL_FUNCTION_1       1  ''
               34  LOAD_FAST                'dict_obj'
               36  LOAD_STR                 'Type'
               38  STORE_SUBSCR     
             40_0  COME_FROM            26  '26'

 L. 496        40  LOAD_STR                 'Parent'
               42  LOAD_FAST                'dict_obj'
               44  <118>                 1  ''
               46  POP_JUMP_IF_FALSE    58  'to 58'

 L. 497        48  LOAD_FAST                'self'
               50  LOAD_ATTR                pages_ref
               52  LOAD_FAST                'dict_obj'
               54  LOAD_STR                 'Parent'
               56  STORE_SUBSCR     
             58_0  COME_FROM            46  '46'

 L. 498        58  LOAD_FAST                'self'
               60  LOAD_ATTR                write_obj
               62  LOAD_FAST                'ref'
               64  BUILD_LIST_1          1 
               66  LOAD_FAST                'objs'
               68  CALL_FINALLY         71  'to 71'
               70  WITH_CLEANUP_FINISH
               72  BUILD_MAP_0           0 
               74  LOAD_FAST                'dict_obj'
               76  <164>                 1  ''
               78  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               80  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 24

    def write_obj--- This code section failed: ---

 L. 501         0  LOAD_FAST                'self'
                2  LOAD_ATTR                f
                4  STORE_FAST               'f'

 L. 502         6  LOAD_FAST                'ref'
                8  LOAD_CONST               None
               10  <117>                 0  ''
               12  POP_JUMP_IF_FALSE    30  'to 30'

 L. 503        14  LOAD_FAST                'self'
               16  LOAD_METHOD              next_object_id
               18  LOAD_FAST                'f'
               20  LOAD_METHOD              tell
               22  CALL_METHOD_0         0  ''
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'ref'
               28  JUMP_FORWARD         52  'to 52'
             30_0  COME_FROM            12  '12'

 L. 505        30  LOAD_FAST                'f'
               32  LOAD_METHOD              tell
               34  CALL_METHOD_0         0  ''
               36  LOAD_FAST                'ref'
               38  LOAD_ATTR                generation
               40  BUILD_TUPLE_2         2 
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                xref_table
               46  LOAD_FAST                'ref'
               48  LOAD_ATTR                object_id
               50  STORE_SUBSCR     
             52_0  COME_FROM            28  '28'

 L. 506        52  LOAD_FAST                'f'
               54  LOAD_METHOD              write
               56  LOAD_GLOBAL              bytes
               58  LOAD_GLOBAL              IndirectObjectDef
               60  LOAD_FAST                'ref'
               62  CALL_FUNCTION_EX      0  'positional arguments only'
               64  CALL_FUNCTION_1       1  ''
               66  CALL_METHOD_1         1  ''
               68  POP_TOP          

 L. 507        70  LOAD_FAST                'dict_obj'
               72  LOAD_METHOD              pop
               74  LOAD_STR                 'stream'
               76  LOAD_CONST               None
               78  CALL_METHOD_2         2  ''
               80  STORE_FAST               'stream'

 L. 508        82  LOAD_FAST                'stream'
               84  LOAD_CONST               None
               86  <117>                 1  ''
               88  POP_JUMP_IF_FALSE   102  'to 102'

 L. 509        90  LOAD_GLOBAL              len
               92  LOAD_FAST                'stream'
               94  CALL_FUNCTION_1       1  ''
               96  LOAD_FAST                'dict_obj'
               98  LOAD_STR                 'Length'
              100  STORE_SUBSCR     
            102_0  COME_FROM            88  '88'

 L. 510       102  LOAD_FAST                'dict_obj'
              104  POP_JUMP_IF_FALSE   120  'to 120'

 L. 511       106  LOAD_FAST                'f'
              108  LOAD_METHOD              write
              110  LOAD_GLOBAL              pdf_repr
              112  LOAD_FAST                'dict_obj'
              114  CALL_FUNCTION_1       1  ''
              116  CALL_METHOD_1         1  ''
              118  POP_TOP          
            120_0  COME_FROM           104  '104'

 L. 512       120  LOAD_FAST                'objs'
              122  GET_ITER         
              124  FOR_ITER            144  'to 144'
              126  STORE_FAST               'obj'

 L. 513       128  LOAD_FAST                'f'
              130  LOAD_METHOD              write
              132  LOAD_GLOBAL              pdf_repr
              134  LOAD_FAST                'obj'
              136  CALL_FUNCTION_1       1  ''
              138  CALL_METHOD_1         1  ''
              140  POP_TOP          
              142  JUMP_BACK           124  'to 124'

 L. 514       144  LOAD_FAST                'stream'
              146  LOAD_CONST               None
              148  <117>                 1  ''
              150  POP_JUMP_IF_FALSE   182  'to 182'

 L. 515       152  LOAD_FAST                'f'
              154  LOAD_METHOD              write
              156  LOAD_CONST               b'stream\n'
              158  CALL_METHOD_1         1  ''
              160  POP_TOP          

 L. 516       162  LOAD_FAST                'f'
              164  LOAD_METHOD              write
              166  LOAD_FAST                'stream'
              168  CALL_METHOD_1         1  ''
              170  POP_TOP          

 L. 517       172  LOAD_FAST                'f'
              174  LOAD_METHOD              write
              176  LOAD_CONST               b'\nendstream\n'
              178  CALL_METHOD_1         1  ''
              180  POP_TOP          
            182_0  COME_FROM           150  '150'

 L. 518       182  LOAD_FAST                'f'
              184  LOAD_METHOD              write
              186  LOAD_CONST               b'endobj\n'
              188  CALL_METHOD_1         1  ''
              190  POP_TOP          

 L. 519       192  LOAD_FAST                'ref'
              194  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10

    def del_root--- This code section failed: ---

 L. 522         0  LOAD_FAST                'self'
                2  LOAD_ATTR                root_ref
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L. 523        10  LOAD_CONST               None
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L. 524        14  LOAD_FAST                'self'
               16  LOAD_ATTR                xref_table
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                root_ref
               22  LOAD_ATTR                object_id
               24  DELETE_SUBSCR    

 L. 525        26  LOAD_FAST                'self'
               28  LOAD_ATTR                xref_table
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                root
               34  LOAD_CONST               b'Pages'
               36  BINARY_SUBSCR    
               38  LOAD_ATTR                object_id
               40  DELETE_SUBSCR    

Parse error at or near `None' instruction at offset -1

    @staticmethod
    def get_buf_from_file--- This code section failed: ---

 L. 529         0  LOAD_GLOBAL              hasattr
                2  LOAD_FAST                'f'
                4  LOAD_STR                 'getbuffer'
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 530        10  LOAD_FAST                'f'
               12  LOAD_METHOD              getbuffer
               14  CALL_METHOD_0         0  ''
               16  RETURN_VALUE     
             18_0  COME_FROM             8  '8'

 L. 531        18  LOAD_GLOBAL              hasattr
               20  LOAD_FAST                'f'
               22  LOAD_STR                 'getvalue'
               24  CALL_FUNCTION_2       2  ''
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 532        28  LOAD_FAST                'f'
               30  LOAD_METHOD              getvalue
               32  CALL_METHOD_0         0  ''
               34  RETURN_VALUE     
             36_0  COME_FROM            26  '26'

 L. 534        36  SETUP_FINALLY        62  'to 62'

 L. 535        38  LOAD_GLOBAL              mmap
               40  LOAD_ATTR                mmap
               42  LOAD_FAST                'f'
               44  LOAD_METHOD              fileno
               46  CALL_METHOD_0         0  ''
               48  LOAD_CONST               0
               50  LOAD_GLOBAL              mmap
               52  LOAD_ATTR                ACCESS_READ
               54  LOAD_CONST               ('access',)
               56  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               58  POP_BLOCK        
               60  RETURN_VALUE     
             62_0  COME_FROM_FINALLY    36  '36'

 L. 536        62  DUP_TOP          
               64  LOAD_GLOBAL              ValueError
               66  <121>                80  ''
               68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          

 L. 537        74  POP_EXCEPT       
               76  LOAD_CONST               b''
               78  RETURN_VALUE     
               80  <48>             

Parse error at or near `<121>' instruction at offset 66

    def read_pdf_info--- This code section failed: ---

 L. 540         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                buf
                6  CALL_FUNCTION_1       1  ''
                8  LOAD_FAST                'self'
               10  STORE_ATTR               file_size_total

 L. 541        12  LOAD_FAST                'self'
               14  LOAD_ATTR                file_size_total
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                start_offset
               20  BINARY_SUBTRACT  
               22  LOAD_FAST                'self'
               24  STORE_ATTR               file_size_this

 L. 542        26  LOAD_FAST                'self'
               28  LOAD_METHOD              read_trailer
               30  CALL_METHOD_0         0  ''
               32  POP_TOP          

 L. 543        34  LOAD_FAST                'self'
               36  LOAD_ATTR                trailer_dict
               38  LOAD_CONST               b'Root'
               40  BINARY_SUBSCR    
               42  LOAD_FAST                'self'
               44  STORE_ATTR               root_ref

 L. 544        46  LOAD_FAST                'self'
               48  LOAD_ATTR                trailer_dict
               50  LOAD_METHOD              get
               52  LOAD_CONST               b'Info'
               54  LOAD_CONST               None
               56  CALL_METHOD_2         2  ''
               58  LOAD_FAST                'self'
               60  STORE_ATTR               info_ref

 L. 545        62  LOAD_GLOBAL              PdfDict
               64  LOAD_FAST                'self'
               66  LOAD_METHOD              read_indirect
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                root_ref
               72  CALL_METHOD_1         1  ''
               74  CALL_FUNCTION_1       1  ''
               76  LOAD_FAST                'self'
               78  STORE_ATTR               root

 L. 546        80  LOAD_FAST                'self'
               82  LOAD_ATTR                info_ref
               84  LOAD_CONST               None
               86  <117>                 0  ''
               88  POP_JUMP_IF_FALSE   100  'to 100'

 L. 547        90  LOAD_GLOBAL              PdfDict
               92  CALL_FUNCTION_0       0  ''
               94  LOAD_FAST                'self'
               96  STORE_ATTR               info
               98  JUMP_FORWARD        118  'to 118'
            100_0  COME_FROM            88  '88'

 L. 549       100  LOAD_GLOBAL              PdfDict
              102  LOAD_FAST                'self'
              104  LOAD_METHOD              read_indirect
              106  LOAD_FAST                'self'
              108  LOAD_ATTR                info_ref
              110  CALL_METHOD_1         1  ''
              112  CALL_FUNCTION_1       1  ''
              114  LOAD_FAST                'self'
              116  STORE_ATTR               info
            118_0  COME_FROM            98  '98'

 L. 550       118  LOAD_GLOBAL              check_format_condition
              120  LOAD_CONST               b'Type'
              122  LOAD_FAST                'self'
              124  LOAD_ATTR                root
              126  <118>                 0  ''
              128  LOAD_STR                 '/Type missing in Root'
              130  CALL_FUNCTION_2       2  ''
              132  POP_TOP          

 L. 551       134  LOAD_GLOBAL              check_format_condition

 L. 552       136  LOAD_FAST                'self'
              138  LOAD_ATTR                root
              140  LOAD_CONST               b'Type'
              142  BINARY_SUBSCR    
              144  LOAD_CONST               b'Catalog'
              146  COMPARE_OP               ==
              148  LOAD_STR                 '/Type in Root is not /Catalog'

 L. 551       150  CALL_FUNCTION_2       2  ''
              152  POP_TOP          

 L. 554       154  LOAD_GLOBAL              check_format_condition
              156  LOAD_CONST               b'Pages'
              158  LOAD_FAST                'self'
              160  LOAD_ATTR                root
              162  <118>                 0  ''
              164  LOAD_STR                 '/Pages missing in Root'
              166  CALL_FUNCTION_2       2  ''
              168  POP_TOP          

 L. 555       170  LOAD_GLOBAL              check_format_condition

 L. 556       172  LOAD_GLOBAL              isinstance
              174  LOAD_FAST                'self'
              176  LOAD_ATTR                root
              178  LOAD_CONST               b'Pages'
              180  BINARY_SUBSCR    
              182  LOAD_GLOBAL              IndirectReference
              184  CALL_FUNCTION_2       2  ''

 L. 557       186  LOAD_STR                 '/Pages in Root is not an indirect reference'

 L. 555       188  CALL_FUNCTION_2       2  ''
              190  POP_TOP          

 L. 559       192  LOAD_FAST                'self'
              194  LOAD_ATTR                root
              196  LOAD_CONST               b'Pages'
              198  BINARY_SUBSCR    
              200  LOAD_FAST                'self'
              202  STORE_ATTR               pages_ref

 L. 560       204  LOAD_FAST                'self'
              206  LOAD_METHOD              read_indirect
              208  LOAD_FAST                'self'
              210  LOAD_ATTR                pages_ref
              212  CALL_METHOD_1         1  ''
              214  LOAD_FAST                'self'
              216  STORE_ATTR               page_tree_root

 L. 561       218  LOAD_FAST                'self'
              220  LOAD_METHOD              linearize_page_tree
              222  LOAD_FAST                'self'
              224  LOAD_ATTR                page_tree_root
              226  CALL_METHOD_1         1  ''
              228  LOAD_FAST                'self'
              230  STORE_ATTR               pages

 L. 565       232  LOAD_FAST                'self'
              234  LOAD_ATTR                pages
              236  LOAD_CONST               None
              238  LOAD_CONST               None
              240  BUILD_SLICE_2         2 
              242  BINARY_SUBSCR    
              244  LOAD_FAST                'self'
              246  STORE_ATTR               orig_pages

Parse error at or near `<117>' instruction at offset 86

    def next_object_id--- This code section failed: ---

 L. 568         0  SETUP_FINALLY        30  'to 30'

 L. 570         2  LOAD_GLOBAL              IndirectReference
                4  LOAD_GLOBAL              max
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                xref_table
               10  LOAD_METHOD              keys
               12  CALL_METHOD_0         0  ''
               14  CALL_FUNCTION_1       1  ''
               16  LOAD_CONST               1
               18  BINARY_ADD       
               20  LOAD_CONST               0
               22  CALL_FUNCTION_2       2  ''
               24  STORE_FAST               'reference'
               26  POP_BLOCK        
               28  JUMP_FORWARD         58  'to 58'
             30_0  COME_FROM_FINALLY     0  '0'

 L. 571        30  DUP_TOP          
               32  LOAD_GLOBAL              ValueError
               34  <121>                56  ''
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 572        42  LOAD_GLOBAL              IndirectReference
               44  LOAD_CONST               1
               46  LOAD_CONST               0
               48  CALL_FUNCTION_2       2  ''
               50  STORE_FAST               'reference'
               52  POP_EXCEPT       
               54  JUMP_FORWARD         58  'to 58'
               56  <48>             
             58_0  COME_FROM            54  '54'
             58_1  COME_FROM            28  '28'

 L. 573        58  LOAD_FAST                'offset'
               60  LOAD_CONST               None
               62  <117>                 1  ''
               64  POP_JUMP_IF_FALSE    82  'to 82'

 L. 574        66  LOAD_FAST                'offset'
               68  LOAD_CONST               0
               70  BUILD_TUPLE_2         2 
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                xref_table
               76  LOAD_FAST                'reference'
               78  LOAD_ATTR                object_id
               80  STORE_SUBSCR     
             82_0  COME_FROM            64  '64'

 L. 575        82  LOAD_FAST                'reference'
               84  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 34

    delimiter = b'[][()<>{}/%]'
    delimiter_or_ws = b'[][()<>{}/%\\000\\011\\012\\014\\015\\040]'
    whitespace = b'[\\000\\011\\012\\014\\015\\040]'
    whitespace_or_hex = b'[\\000\\011\\012\\014\\015\\0400-9a-fA-F]'
    whitespace_optional = whitespace + b'*'
    whitespace_mandatory = whitespace + b'+'
    newline_only = b'[\\r\\n]+'
    newline = whitespace_optional + newline_only + whitespace_optional
    re_trailer_end = re.compile(whitespace_mandatory + b'trailer' + whitespace_optional + b'\\<\\<(.*\\>\\>)' + newline + b'startxref' + newline + b'([0-9]+)' + newline + b'%%EOF' + whitespace_optional + b'$', re.DOTALL)
    re_trailer_prev = re.compile(whitespace_optional + b'trailer' + whitespace_optional + b'\\<\\<(.*?\\>\\>)' + newline + b'startxref' + newline + b'([0-9]+)' + newline + b'%%EOF' + whitespace_optional, re.DOTALL)

    def read_trailer--- This code section failed: ---

 L. 616         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                buf
                6  CALL_FUNCTION_1       1  ''
                8  LOAD_CONST               16384
               10  BINARY_SUBTRACT  
               12  STORE_FAST               'search_start_offset'

 L. 617        14  LOAD_FAST                'search_start_offset'
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                start_offset
               20  COMPARE_OP               <
               22  POP_JUMP_IF_FALSE    30  'to 30'

 L. 618        24  LOAD_FAST                'self'
               26  LOAD_ATTR                start_offset
               28  STORE_FAST               'search_start_offset'
             30_0  COME_FROM            22  '22'

 L. 619        30  LOAD_FAST                'self'
               32  LOAD_ATTR                re_trailer_end
               34  LOAD_METHOD              search
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                buf
               40  LOAD_FAST                'search_start_offset'
               42  CALL_METHOD_2         2  ''
               44  STORE_FAST               'm'

 L. 620        46  LOAD_GLOBAL              check_format_condition
               48  LOAD_FAST                'm'
               50  LOAD_STR                 'trailer end not found'
               52  CALL_FUNCTION_2       2  ''
               54  POP_TOP          

 L. 622        56  LOAD_FAST                'm'
               58  STORE_FAST               'last_match'

 L. 623        60  LOAD_FAST                'm'
               62  POP_JUMP_IF_FALSE    94  'to 94'

 L. 624        64  LOAD_FAST                'm'
               66  STORE_FAST               'last_match'

 L. 625        68  LOAD_FAST                'self'
               70  LOAD_ATTR                re_trailer_end
               72  LOAD_METHOD              search
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                buf
               78  LOAD_FAST                'm'
               80  LOAD_METHOD              start
               82  CALL_METHOD_0         0  ''
               84  LOAD_CONST               16
               86  BINARY_ADD       
               88  CALL_METHOD_2         2  ''
               90  STORE_FAST               'm'
               92  JUMP_BACK            60  'to 60'
             94_0  COME_FROM            62  '62'

 L. 626        94  LOAD_FAST                'm'
               96  POP_JUMP_IF_TRUE    102  'to 102'

 L. 627        98  LOAD_FAST                'last_match'
              100  STORE_FAST               'm'
            102_0  COME_FROM            96  '96'

 L. 628       102  LOAD_FAST                'm'
              104  LOAD_METHOD              group
              106  LOAD_CONST               1
              108  CALL_METHOD_1         1  ''
              110  STORE_FAST               'trailer_data'

 L. 629       112  LOAD_GLOBAL              int
              114  LOAD_FAST                'm'
              116  LOAD_METHOD              group
              118  LOAD_CONST               2
              120  CALL_METHOD_1         1  ''
              122  CALL_FUNCTION_1       1  ''
              124  LOAD_FAST                'self'
              126  STORE_ATTR               last_xref_section_offset

 L. 630       128  LOAD_FAST                'self'
              130  LOAD_METHOD              interpret_trailer
              132  LOAD_FAST                'trailer_data'
              134  CALL_METHOD_1         1  ''
              136  LOAD_FAST                'self'
              138  STORE_ATTR               trailer_dict

 L. 631       140  LOAD_GLOBAL              XrefTable
              142  CALL_FUNCTION_0       0  ''
              144  LOAD_FAST                'self'
              146  STORE_ATTR               xref_table

 L. 632       148  LOAD_FAST                'self'
              150  LOAD_ATTR                read_xref_table
              152  LOAD_FAST                'self'
              154  LOAD_ATTR                last_xref_section_offset
              156  LOAD_CONST               ('xref_section_offset',)
              158  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              160  POP_TOP          

 L. 633       162  LOAD_CONST               b'Prev'
              164  LOAD_FAST                'self'
              166  LOAD_ATTR                trailer_dict
              168  <118>                 0  ''
              170  POP_JUMP_IF_FALSE   188  'to 188'

 L. 634       172  LOAD_FAST                'self'
              174  LOAD_METHOD              read_prev_trailer
              176  LOAD_FAST                'self'
              178  LOAD_ATTR                trailer_dict
              180  LOAD_CONST               b'Prev'
              182  BINARY_SUBSCR    
              184  CALL_METHOD_1         1  ''
              186  POP_TOP          
            188_0  COME_FROM           170  '170'

Parse error at or near `<118>' instruction at offset 168

    def read_prev_trailer--- This code section failed: ---

 L. 637         0  LOAD_FAST                'self'
                2  LOAD_ATTR                read_xref_table
                4  LOAD_FAST                'xref_section_offset'
                6  LOAD_CONST               ('xref_section_offset',)
                8  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               10  STORE_FAST               'trailer_offset'

 L. 638        12  LOAD_FAST                'self'
               14  LOAD_ATTR                re_trailer_prev
               16  LOAD_METHOD              search

 L. 639        18  LOAD_FAST                'self'
               20  LOAD_ATTR                buf
               22  LOAD_FAST                'trailer_offset'
               24  LOAD_FAST                'trailer_offset'
               26  LOAD_CONST               16384
               28  BINARY_ADD       
               30  BUILD_SLICE_2         2 
               32  BINARY_SUBSCR    

 L. 638        34  CALL_METHOD_1         1  ''
               36  STORE_FAST               'm'

 L. 641        38  LOAD_GLOBAL              check_format_condition
               40  LOAD_FAST                'm'
               42  LOAD_STR                 'previous trailer not found'
               44  CALL_FUNCTION_2       2  ''
               46  POP_TOP          

 L. 642        48  LOAD_FAST                'm'
               50  LOAD_METHOD              group
               52  LOAD_CONST               1
               54  CALL_METHOD_1         1  ''
               56  STORE_FAST               'trailer_data'

 L. 643        58  LOAD_GLOBAL              check_format_condition

 L. 644        60  LOAD_GLOBAL              int
               62  LOAD_FAST                'm'
               64  LOAD_METHOD              group
               66  LOAD_CONST               2
               68  CALL_METHOD_1         1  ''
               70  CALL_FUNCTION_1       1  ''
               72  LOAD_FAST                'xref_section_offset'
               74  COMPARE_OP               ==

 L. 645        76  LOAD_STR                 "xref section offset in previous trailer doesn't match what was expected"

 L. 643        78  CALL_FUNCTION_2       2  ''
               80  POP_TOP          

 L. 647        82  LOAD_FAST                'self'
               84  LOAD_METHOD              interpret_trailer
               86  LOAD_FAST                'trailer_data'
               88  CALL_METHOD_1         1  ''
               90  STORE_FAST               'trailer_dict'

 L. 648        92  LOAD_CONST               b'Prev'
               94  LOAD_FAST                'trailer_dict'
               96  <118>                 0  ''
               98  POP_JUMP_IF_FALSE   114  'to 114'

 L. 649       100  LOAD_FAST                'self'
              102  LOAD_METHOD              read_prev_trailer
              104  LOAD_FAST                'trailer_dict'
              106  LOAD_CONST               b'Prev'
              108  BINARY_SUBSCR    
              110  CALL_METHOD_1         1  ''
              112  POP_TOP          
            114_0  COME_FROM            98  '98'

Parse error at or near `<118>' instruction at offset 96

    re_whitespace_optional = re.compile(whitespace_optional)
    re_name = re.compile(whitespace_optional + b"/([!-$&'*-.0-;=?-Z\\\\^-z|~]+)(?=" + delimiter_or_ws + b')')
    re_dict_start = re.compile(whitespace_optional + b'\\<\\<')
    re_dict_end = re.compile(whitespace_optional + b'\\>\\>' + whitespace_optional)

    @classmethod
    def interpret_trailer--- This code section failed: ---

 L. 663         0  BUILD_MAP_0           0 
                2  STORE_FAST               'trailer'

 L. 664         4  LOAD_CONST               0
                6  STORE_FAST               'offset'

 L. 666         8  LOAD_FAST                'cls'
               10  LOAD_ATTR                re_name
               12  LOAD_METHOD              match
               14  LOAD_FAST                'trailer_data'
               16  LOAD_FAST                'offset'
               18  CALL_METHOD_2         2  ''
               20  STORE_FAST               'm'

 L. 667        22  LOAD_FAST                'm'
               24  POP_JUMP_IF_TRUE     84  'to 84'

 L. 668        26  LOAD_FAST                'cls'
               28  LOAD_ATTR                re_dict_end
               30  LOAD_METHOD              match
               32  LOAD_FAST                'trailer_data'
               34  LOAD_FAST                'offset'
               36  CALL_METHOD_2         2  ''
               38  STORE_FAST               'm'

 L. 669        40  LOAD_GLOBAL              check_format_condition

 L. 670        42  LOAD_FAST                'm'
               44  JUMP_IF_FALSE_OR_POP    60  'to 60'
               46  LOAD_FAST                'm'
               48  LOAD_METHOD              end
               50  CALL_METHOD_0         0  ''
               52  LOAD_GLOBAL              len
               54  LOAD_FAST                'trailer_data'
               56  CALL_FUNCTION_1       1  ''
               58  COMPARE_OP               ==
             60_0  COME_FROM            44  '44'

 L. 671        60  LOAD_STR                 'name not found in trailer, remaining data: '

 L. 672        62  LOAD_GLOBAL              repr
               64  LOAD_FAST                'trailer_data'
               66  LOAD_FAST                'offset'
               68  LOAD_CONST               None
               70  BUILD_SLICE_2         2 
               72  BINARY_SUBSCR    
               74  CALL_FUNCTION_1       1  ''

 L. 671        76  BINARY_ADD       

 L. 669        78  CALL_FUNCTION_2       2  ''
               80  POP_TOP          

 L. 674        82  BREAK_LOOP          130  'to 130'
             84_0  COME_FROM            24  '24'

 L. 675        84  LOAD_FAST                'cls'
               86  LOAD_METHOD              interpret_name
               88  LOAD_FAST                'm'
               90  LOAD_METHOD              group
               92  LOAD_CONST               1
               94  CALL_METHOD_1         1  ''
               96  CALL_METHOD_1         1  ''
               98  STORE_FAST               'key'

 L. 676       100  LOAD_FAST                'cls'
              102  LOAD_METHOD              get_value
              104  LOAD_FAST                'trailer_data'
              106  LOAD_FAST                'm'
              108  LOAD_METHOD              end
              110  CALL_METHOD_0         0  ''
              112  CALL_METHOD_2         2  ''
              114  UNPACK_SEQUENCE_2     2 
              116  STORE_FAST               'value'
              118  STORE_FAST               'offset'

 L. 677       120  LOAD_FAST                'value'
              122  LOAD_FAST                'trailer'
              124  LOAD_FAST                'key'
              126  STORE_SUBSCR     
              128  JUMP_BACK             8  'to 8'

 L. 678       130  LOAD_GLOBAL              check_format_condition

 L. 679       132  LOAD_CONST               b'Size'
              134  LOAD_FAST                'trailer'
              136  <118>                 0  ''
              138  JUMP_IF_FALSE_OR_POP   152  'to 152'
              140  LOAD_GLOBAL              isinstance
              142  LOAD_FAST                'trailer'
              144  LOAD_CONST               b'Size'
              146  BINARY_SUBSCR    
              148  LOAD_GLOBAL              int
              150  CALL_FUNCTION_2       2  ''
            152_0  COME_FROM           138  '138'

 L. 680       152  LOAD_STR                 '/Size not in trailer or not an integer'

 L. 678       154  CALL_FUNCTION_2       2  ''
              156  POP_TOP          

 L. 682       158  LOAD_GLOBAL              check_format_condition

 L. 683       160  LOAD_CONST               b'Root'
              162  LOAD_FAST                'trailer'
              164  <118>                 0  ''
              166  JUMP_IF_FALSE_OR_POP   180  'to 180'
              168  LOAD_GLOBAL              isinstance
              170  LOAD_FAST                'trailer'
              172  LOAD_CONST               b'Root'
              174  BINARY_SUBSCR    
              176  LOAD_GLOBAL              IndirectReference
              178  CALL_FUNCTION_2       2  ''
            180_0  COME_FROM           166  '166'

 L. 684       180  LOAD_STR                 '/Root not in trailer or not an indirect reference'

 L. 682       182  CALL_FUNCTION_2       2  ''
              184  POP_TOP          

 L. 686       186  LOAD_FAST                'trailer'
              188  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 136

    re_hashes_in_name = re.compile(b'([^#]*)(#([0-9a-fA-F]{2}))?')

    @classmethod
    def interpret_name(cls, raw, as_text=False):
        name = b''
        for m in cls.re_hashes_in_name.finditer(raw):
            if m.group(3):
                name += m.group(1) + bytearray.fromhex(m.group(3).decode('us-ascii'))
            else:
                name += m.group(1)
        else:
            if as_text:
                return name.decode('utf-8')
            return bytes(name)

    re_null = re.compile(whitespace_optional + b'null(?=' + delimiter_or_ws + b')')
    re_true = re.compile(whitespace_optional + b'true(?=' + delimiter_or_ws + b')')
    re_false = re.compile(whitespace_optional + b'false(?=' + delimiter_or_ws + b')')
    re_int = re.compile(whitespace_optional + b'([-+]?[0-9]+)(?=' + delimiter_or_ws + b')')
    re_real = re.compile(whitespace_optional + b'([-+]?([0-9]+\\.[0-9]*|[0-9]*\\.[0-9]+))(?=' + delimiter_or_ws + b')')
    re_array_start = re.compile(whitespace_optional + b'\\[')
    re_array_end = re.compile(whitespace_optional + b']')
    re_string_hex = re.compile(whitespace_optional + b'\\<(' + whitespace_or_hex + b'*)\\>')
    re_string_lit = re.compile(whitespace_optional + b'\\(')
    re_indirect_reference = re.compile(whitespace_optional + b'([-+]?[0-9]+)' + whitespace_mandatory + b'([-+]?[0-9]+)' + whitespace_mandatory + b'R(?=' + delimiter_or_ws + b')')
    re_indirect_def_start = re.compile(whitespace_optional + b'([-+]?[0-9]+)' + whitespace_mandatory + b'([-+]?[0-9]+)' + whitespace_mandatory + b'obj(?=' + delimiter_or_ws + b')')
    re_indirect_def_end = re.compile(whitespace_optional + b'endobj(?=' + delimiter_or_ws + b')')
    re_comment = re.compile(b'(' + whitespace_optional + b'%[^\\r\\n]*' + newline + b')*')
    re_stream_start = re.compile(whitespace_optional + b'stream\\r?\\n')
    re_stream_end = re.compile(whitespace_optional + b'endstream(?=' + delimiter_or_ws + b')')

    @classmethod
    def get_value--- This code section failed: ---

 L. 754         0  LOAD_FAST                'max_nesting'
                2  LOAD_CONST               0
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 755         8  LOAD_CONST               (None, None)
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L. 756        12  LOAD_FAST                'cls'
               14  LOAD_ATTR                re_comment
               16  LOAD_METHOD              match
               18  LOAD_FAST                'data'
               20  LOAD_FAST                'offset'
               22  CALL_METHOD_2         2  ''
               24  STORE_FAST               'm'

 L. 757        26  LOAD_FAST                'm'
               28  POP_JUMP_IF_FALSE    38  'to 38'

 L. 758        30  LOAD_FAST                'm'
               32  LOAD_METHOD              end
               34  CALL_METHOD_0         0  ''
               36  STORE_FAST               'offset'
             38_0  COME_FROM            28  '28'

 L. 759        38  LOAD_FAST                'cls'
               40  LOAD_ATTR                re_indirect_def_start
               42  LOAD_METHOD              match
               44  LOAD_FAST                'data'
               46  LOAD_FAST                'offset'
               48  CALL_METHOD_2         2  ''
               50  STORE_FAST               'm'

 L. 760        52  LOAD_FAST                'm'
               54  POP_JUMP_IF_FALSE   232  'to 232'

 L. 761        56  LOAD_GLOBAL              check_format_condition

 L. 762        58  LOAD_GLOBAL              int
               60  LOAD_FAST                'm'
               62  LOAD_METHOD              group
               64  LOAD_CONST               1
               66  CALL_METHOD_1         1  ''
               68  CALL_FUNCTION_1       1  ''
               70  LOAD_CONST               0
               72  COMPARE_OP               >

 L. 763        74  LOAD_STR                 'indirect object definition: object ID must be greater than 0'

 L. 761        76  CALL_FUNCTION_2       2  ''
               78  POP_TOP          

 L. 765        80  LOAD_GLOBAL              check_format_condition

 L. 766        82  LOAD_GLOBAL              int
               84  LOAD_FAST                'm'
               86  LOAD_METHOD              group
               88  LOAD_CONST               2
               90  CALL_METHOD_1         1  ''
               92  CALL_FUNCTION_1       1  ''
               94  LOAD_CONST               0
               96  COMPARE_OP               >=

 L. 767        98  LOAD_STR                 'indirect object definition: generation must be non-negative'

 L. 765       100  CALL_FUNCTION_2       2  ''
              102  POP_TOP          

 L. 769       104  LOAD_GLOBAL              check_format_condition

 L. 770       106  LOAD_FAST                'expect_indirect'
              108  LOAD_CONST               None
              110  <117>                 0  ''
              112  JUMP_IF_TRUE_OR_POP   146  'to 146'

 L. 771       114  LOAD_FAST                'expect_indirect'

 L. 772       116  LOAD_GLOBAL              IndirectReference
              118  LOAD_GLOBAL              int
              120  LOAD_FAST                'm'
              122  LOAD_METHOD              group
              124  LOAD_CONST               1
              126  CALL_METHOD_1         1  ''
              128  CALL_FUNCTION_1       1  ''
              130  LOAD_GLOBAL              int
              132  LOAD_FAST                'm'
              134  LOAD_METHOD              group
              136  LOAD_CONST               2
              138  CALL_METHOD_1         1  ''
              140  CALL_FUNCTION_1       1  ''
              142  CALL_FUNCTION_2       2  ''

 L. 771       144  COMPARE_OP               ==
            146_0  COME_FROM           112  '112'

 L. 773       146  LOAD_STR                 'indirect object definition different than expected'

 L. 769       148  CALL_FUNCTION_2       2  ''
              150  POP_TOP          

 L. 775       152  LOAD_FAST                'cls'
              154  LOAD_ATTR                get_value
              156  LOAD_FAST                'data'
              158  LOAD_FAST                'm'
              160  LOAD_METHOD              end
              162  CALL_METHOD_0         0  ''
              164  LOAD_FAST                'max_nesting'
              166  LOAD_CONST               1
              168  BINARY_SUBTRACT  
              170  LOAD_CONST               ('max_nesting',)
              172  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              174  UNPACK_SEQUENCE_2     2 
              176  STORE_FAST               'object'
              178  STORE_FAST               'offset'

 L. 776       180  LOAD_FAST                'offset'
              182  LOAD_CONST               None
              184  <117>                 0  ''
              186  POP_JUMP_IF_FALSE   196  'to 196'

 L. 777       188  LOAD_FAST                'object'
              190  LOAD_CONST               None
              192  BUILD_TUPLE_2         2 
              194  RETURN_VALUE     
            196_0  COME_FROM           186  '186'

 L. 778       196  LOAD_FAST                'cls'
              198  LOAD_ATTR                re_indirect_def_end
              200  LOAD_METHOD              match
              202  LOAD_FAST                'data'
              204  LOAD_FAST                'offset'
              206  CALL_METHOD_2         2  ''
              208  STORE_FAST               'm'

 L. 779       210  LOAD_GLOBAL              check_format_condition
              212  LOAD_FAST                'm'
              214  LOAD_STR                 'indirect object definition end not found'
              216  CALL_FUNCTION_2       2  ''
              218  POP_TOP          

 L. 780       220  LOAD_FAST                'object'
              222  LOAD_FAST                'm'
              224  LOAD_METHOD              end
              226  CALL_METHOD_0         0  ''
              228  BUILD_TUPLE_2         2 
              230  RETURN_VALUE     
            232_0  COME_FROM            54  '54'

 L. 781       232  LOAD_GLOBAL              check_format_condition

 L. 782       234  LOAD_FAST                'expect_indirect'
              236  UNARY_NOT        
              238  LOAD_STR                 'indirect object definition not found'

 L. 781       240  CALL_FUNCTION_2       2  ''
              242  POP_TOP          

 L. 784       244  LOAD_FAST                'cls'
              246  LOAD_ATTR                re_indirect_reference
              248  LOAD_METHOD              match
              250  LOAD_FAST                'data'
              252  LOAD_FAST                'offset'
              254  CALL_METHOD_2         2  ''
              256  STORE_FAST               'm'

 L. 785       258  LOAD_FAST                'm'
          260_262  POP_JUMP_IF_FALSE   350  'to 350'

 L. 786       264  LOAD_GLOBAL              check_format_condition

 L. 787       266  LOAD_GLOBAL              int
              268  LOAD_FAST                'm'
              270  LOAD_METHOD              group
              272  LOAD_CONST               1
              274  CALL_METHOD_1         1  ''
              276  CALL_FUNCTION_1       1  ''
              278  LOAD_CONST               0
              280  COMPARE_OP               >

 L. 788       282  LOAD_STR                 'indirect object reference: object ID must be greater than 0'

 L. 786       284  CALL_FUNCTION_2       2  ''
              286  POP_TOP          

 L. 790       288  LOAD_GLOBAL              check_format_condition

 L. 791       290  LOAD_GLOBAL              int
              292  LOAD_FAST                'm'
              294  LOAD_METHOD              group
              296  LOAD_CONST               2
              298  CALL_METHOD_1         1  ''
              300  CALL_FUNCTION_1       1  ''
              302  LOAD_CONST               0
              304  COMPARE_OP               >=

 L. 792       306  LOAD_STR                 'indirect object reference: generation must be non-negative'

 L. 790       308  CALL_FUNCTION_2       2  ''
              310  POP_TOP          

 L. 794       312  LOAD_GLOBAL              IndirectReference
              314  LOAD_GLOBAL              int
              316  LOAD_FAST                'm'
              318  LOAD_METHOD              group
              320  LOAD_CONST               1
              322  CALL_METHOD_1         1  ''
              324  CALL_FUNCTION_1       1  ''
              326  LOAD_GLOBAL              int
              328  LOAD_FAST                'm'
              330  LOAD_METHOD              group
              332  LOAD_CONST               2
              334  CALL_METHOD_1         1  ''
              336  CALL_FUNCTION_1       1  ''
              338  CALL_FUNCTION_2       2  ''
              340  LOAD_FAST                'm'
              342  LOAD_METHOD              end
              344  CALL_METHOD_0         0  ''
              346  BUILD_TUPLE_2         2 
              348  RETURN_VALUE     
            350_0  COME_FROM           260  '260'

 L. 795       350  LOAD_FAST                'cls'
              352  LOAD_ATTR                re_dict_start
              354  LOAD_METHOD              match
              356  LOAD_FAST                'data'
              358  LOAD_FAST                'offset'
              360  CALL_METHOD_2         2  ''
              362  STORE_FAST               'm'

 L. 796       364  LOAD_FAST                'm'
          366_368  POP_JUMP_IF_FALSE   720  'to 720'

 L. 797       370  LOAD_FAST                'm'
              372  LOAD_METHOD              end
              374  CALL_METHOD_0         0  ''
              376  STORE_FAST               'offset'

 L. 798       378  BUILD_MAP_0           0 
              380  STORE_FAST               'result'

 L. 799       382  LOAD_FAST                'cls'
              384  LOAD_ATTR                re_dict_end
              386  LOAD_METHOD              match
              388  LOAD_FAST                'data'
              390  LOAD_FAST                'offset'
              392  CALL_METHOD_2         2  ''
              394  STORE_FAST               'm'

 L. 800       396  LOAD_FAST                'm'
          398_400  POP_JUMP_IF_TRUE    512  'to 512'

 L. 801       402  LOAD_FAST                'cls'
              404  LOAD_ATTR                get_value
              406  LOAD_FAST                'data'
              408  LOAD_FAST                'offset'
              410  LOAD_FAST                'max_nesting'
              412  LOAD_CONST               1
              414  BINARY_SUBTRACT  
              416  LOAD_CONST               ('max_nesting',)
              418  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              420  UNPACK_SEQUENCE_2     2 
              422  STORE_FAST               'key'
              424  STORE_FAST               'offset'

 L. 802       426  LOAD_FAST                'offset'
              428  LOAD_CONST               None
              430  <117>                 0  ''
          432_434  POP_JUMP_IF_FALSE   444  'to 444'

 L. 803       436  LOAD_FAST                'result'
              438  LOAD_CONST               None
              440  BUILD_TUPLE_2         2 
              442  RETURN_VALUE     
            444_0  COME_FROM           432  '432'

 L. 804       444  LOAD_FAST                'cls'
              446  LOAD_ATTR                get_value
              448  LOAD_FAST                'data'
              450  LOAD_FAST                'offset'
              452  LOAD_FAST                'max_nesting'
              454  LOAD_CONST               1
              456  BINARY_SUBTRACT  
              458  LOAD_CONST               ('max_nesting',)
              460  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              462  UNPACK_SEQUENCE_2     2 
              464  STORE_FAST               'value'
              466  STORE_FAST               'offset'

 L. 805       468  LOAD_FAST                'value'
              470  LOAD_FAST                'result'
              472  LOAD_FAST                'key'
              474  STORE_SUBSCR     

 L. 806       476  LOAD_FAST                'offset'
              478  LOAD_CONST               None
              480  <117>                 0  ''
          482_484  POP_JUMP_IF_FALSE   494  'to 494'

 L. 807       486  LOAD_FAST                'result'
              488  LOAD_CONST               None
              490  BUILD_TUPLE_2         2 
              492  RETURN_VALUE     
            494_0  COME_FROM           482  '482'

 L. 808       494  LOAD_FAST                'cls'
              496  LOAD_ATTR                re_dict_end
              498  LOAD_METHOD              match
              500  LOAD_FAST                'data'
              502  LOAD_FAST                'offset'
              504  CALL_METHOD_2         2  ''
              506  STORE_FAST               'm'
          508_510  JUMP_BACK           396  'to 396'
            512_0  COME_FROM           398  '398'

 L. 809       512  LOAD_FAST                'm'
              514  LOAD_METHOD              end
              516  CALL_METHOD_0         0  ''
              518  STORE_FAST               'offset'

 L. 810       520  LOAD_FAST                'cls'
              522  LOAD_ATTR                re_stream_start
              524  LOAD_METHOD              match
              526  LOAD_FAST                'data'
              528  LOAD_FAST                'offset'
              530  CALL_METHOD_2         2  ''
              532  STORE_FAST               'm'

 L. 811       534  LOAD_FAST                'm'
          536_538  POP_JUMP_IF_FALSE   704  'to 704'

 L. 812       540  SETUP_FINALLY       558  'to 558'

 L. 813       542  LOAD_GLOBAL              int
              544  LOAD_FAST                'result'
              546  LOAD_CONST               b'Length'
              548  BINARY_SUBSCR    
              550  CALL_FUNCTION_1       1  ''
              552  STORE_FAST               'stream_len'
              554  POP_BLOCK        
              556  JUMP_FORWARD        624  'to 624'
            558_0  COME_FROM_FINALLY   540  '540'

 L. 814       558  DUP_TOP          
              560  LOAD_GLOBAL              TypeError
              562  LOAD_GLOBAL              KeyError
              564  LOAD_GLOBAL              ValueError
              566  BUILD_TUPLE_3         3 
          568_570  <121>               622  ''
              572  POP_TOP          
              574  STORE_FAST               'e'
              576  POP_TOP          
              578  SETUP_FINALLY       614  'to 614'

 L. 815       580  LOAD_GLOBAL              PdfFormatError

 L. 816       582  LOAD_STR                 'bad or missing Length in stream dict (%r)'

 L. 817       584  LOAD_FAST                'result'
              586  LOAD_METHOD              get
              588  LOAD_CONST               b'Length'
              590  LOAD_CONST               None
              592  CALL_METHOD_2         2  ''

 L. 816       594  BINARY_MODULO    

 L. 815       596  CALL_FUNCTION_1       1  ''

 L. 818       598  LOAD_FAST                'e'

 L. 815       600  RAISE_VARARGS_2       2  'exception instance with __cause__'
              602  POP_BLOCK        
              604  POP_EXCEPT       
              606  LOAD_CONST               None
              608  STORE_FAST               'e'
              610  DELETE_FAST              'e'
              612  JUMP_FORWARD        624  'to 624'
            614_0  COME_FROM_FINALLY   578  '578'
              614  LOAD_CONST               None
              616  STORE_FAST               'e'
              618  DELETE_FAST              'e'
              620  <48>             
              622  <48>             
            624_0  COME_FROM           612  '612'
            624_1  COME_FROM           556  '556'

 L. 819       624  LOAD_FAST                'data'
              626  LOAD_FAST                'm'
              628  LOAD_METHOD              end
              630  CALL_METHOD_0         0  ''
              632  LOAD_FAST                'm'
              634  LOAD_METHOD              end
              636  CALL_METHOD_0         0  ''
              638  LOAD_FAST                'stream_len'
              640  BINARY_ADD       
              642  BUILD_SLICE_2         2 
              644  BINARY_SUBSCR    
              646  STORE_FAST               'stream_data'

 L. 820       648  LOAD_FAST                'cls'
              650  LOAD_ATTR                re_stream_end
              652  LOAD_METHOD              match
              654  LOAD_FAST                'data'
              656  LOAD_FAST                'm'
              658  LOAD_METHOD              end
              660  CALL_METHOD_0         0  ''
              662  LOAD_FAST                'stream_len'
              664  BINARY_ADD       
              666  CALL_METHOD_2         2  ''
              668  STORE_FAST               'm'

 L. 821       670  LOAD_GLOBAL              check_format_condition
              672  LOAD_FAST                'm'
              674  LOAD_STR                 'stream end not found'
              676  CALL_FUNCTION_2       2  ''
              678  POP_TOP          

 L. 822       680  LOAD_FAST                'm'
              682  LOAD_METHOD              end
              684  CALL_METHOD_0         0  ''
              686  STORE_FAST               'offset'

 L. 823       688  LOAD_GLOBAL              PdfStream
              690  LOAD_GLOBAL              PdfDict
              692  LOAD_FAST                'result'
              694  CALL_FUNCTION_1       1  ''
              696  LOAD_FAST                'stream_data'
              698  CALL_FUNCTION_2       2  ''
              700  STORE_FAST               'result'
              702  JUMP_FORWARD        712  'to 712'
            704_0  COME_FROM           536  '536'

 L. 825       704  LOAD_GLOBAL              PdfDict
              706  LOAD_FAST                'result'
              708  CALL_FUNCTION_1       1  ''
              710  STORE_FAST               'result'
            712_0  COME_FROM           702  '702'

 L. 826       712  LOAD_FAST                'result'
              714  LOAD_FAST                'offset'
              716  BUILD_TUPLE_2         2 
              718  RETURN_VALUE     
            720_0  COME_FROM           366  '366'

 L. 827       720  LOAD_FAST                'cls'
              722  LOAD_ATTR                re_array_start
              724  LOAD_METHOD              match
              726  LOAD_FAST                'data'
              728  LOAD_FAST                'offset'
              730  CALL_METHOD_2         2  ''
              732  STORE_FAST               'm'

 L. 828       734  LOAD_FAST                'm'
          736_738  POP_JUMP_IF_FALSE   854  'to 854'

 L. 829       740  LOAD_FAST                'm'
              742  LOAD_METHOD              end
              744  CALL_METHOD_0         0  ''
              746  STORE_FAST               'offset'

 L. 830       748  BUILD_LIST_0          0 
              750  STORE_FAST               'result'

 L. 831       752  LOAD_FAST                'cls'
              754  LOAD_ATTR                re_array_end
              756  LOAD_METHOD              match
              758  LOAD_FAST                'data'
              760  LOAD_FAST                'offset'
              762  CALL_METHOD_2         2  ''
              764  STORE_FAST               'm'

 L. 832       766  LOAD_FAST                'm'
          768_770  POP_JUMP_IF_TRUE    842  'to 842'

 L. 833       772  LOAD_FAST                'cls'
              774  LOAD_ATTR                get_value
              776  LOAD_FAST                'data'
              778  LOAD_FAST                'offset'
              780  LOAD_FAST                'max_nesting'
              782  LOAD_CONST               1
              784  BINARY_SUBTRACT  
              786  LOAD_CONST               ('max_nesting',)
              788  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              790  UNPACK_SEQUENCE_2     2 
              792  STORE_FAST               'value'
              794  STORE_FAST               'offset'

 L. 834       796  LOAD_FAST                'result'
              798  LOAD_METHOD              append
              800  LOAD_FAST                'value'
              802  CALL_METHOD_1         1  ''
              804  POP_TOP          

 L. 835       806  LOAD_FAST                'offset'
              808  LOAD_CONST               None
              810  <117>                 0  ''
          812_814  POP_JUMP_IF_FALSE   824  'to 824'

 L. 836       816  LOAD_FAST                'result'
              818  LOAD_CONST               None
              820  BUILD_TUPLE_2         2 
              822  RETURN_VALUE     
            824_0  COME_FROM           812  '812'

 L. 837       824  LOAD_FAST                'cls'
              826  LOAD_ATTR                re_array_end
              828  LOAD_METHOD              match
              830  LOAD_FAST                'data'
              832  LOAD_FAST                'offset'
              834  CALL_METHOD_2         2  ''
              836  STORE_FAST               'm'
          838_840  JUMP_BACK           766  'to 766'
            842_0  COME_FROM           768  '768'

 L. 838       842  LOAD_FAST                'result'
              844  LOAD_FAST                'm'
              846  LOAD_METHOD              end
              848  CALL_METHOD_0         0  ''
              850  BUILD_TUPLE_2         2 
              852  RETURN_VALUE     
            854_0  COME_FROM           736  '736'

 L. 839       854  LOAD_FAST                'cls'
              856  LOAD_ATTR                re_null
              858  LOAD_METHOD              match
              860  LOAD_FAST                'data'
              862  LOAD_FAST                'offset'
              864  CALL_METHOD_2         2  ''
              866  STORE_FAST               'm'

 L. 840       868  LOAD_FAST                'm'
          870_872  POP_JUMP_IF_FALSE   886  'to 886'

 L. 841       874  LOAD_CONST               None
              876  LOAD_FAST                'm'
              878  LOAD_METHOD              end
              880  CALL_METHOD_0         0  ''
              882  BUILD_TUPLE_2         2 
              884  RETURN_VALUE     
            886_0  COME_FROM           870  '870'

 L. 842       886  LOAD_FAST                'cls'
              888  LOAD_ATTR                re_true
              890  LOAD_METHOD              match
              892  LOAD_FAST                'data'
              894  LOAD_FAST                'offset'
              896  CALL_METHOD_2         2  ''
              898  STORE_FAST               'm'

 L. 843       900  LOAD_FAST                'm'
          902_904  POP_JUMP_IF_FALSE   918  'to 918'

 L. 844       906  LOAD_CONST               True
              908  LOAD_FAST                'm'
              910  LOAD_METHOD              end
              912  CALL_METHOD_0         0  ''
              914  BUILD_TUPLE_2         2 
              916  RETURN_VALUE     
            918_0  COME_FROM           902  '902'

 L. 845       918  LOAD_FAST                'cls'
              920  LOAD_ATTR                re_false
              922  LOAD_METHOD              match
              924  LOAD_FAST                'data'
              926  LOAD_FAST                'offset'
              928  CALL_METHOD_2         2  ''
              930  STORE_FAST               'm'

 L. 846       932  LOAD_FAST                'm'
          934_936  POP_JUMP_IF_FALSE   950  'to 950'

 L. 847       938  LOAD_CONST               False
              940  LOAD_FAST                'm'
              942  LOAD_METHOD              end
              944  CALL_METHOD_0         0  ''
              946  BUILD_TUPLE_2         2 
              948  RETURN_VALUE     
            950_0  COME_FROM           934  '934'

 L. 848       950  LOAD_FAST                'cls'
              952  LOAD_ATTR                re_name
              954  LOAD_METHOD              match
              956  LOAD_FAST                'data'
              958  LOAD_FAST                'offset'
              960  CALL_METHOD_2         2  ''
              962  STORE_FAST               'm'

 L. 849       964  LOAD_FAST                'm'
          966_968  POP_JUMP_IF_FALSE   998  'to 998'

 L. 850       970  LOAD_GLOBAL              PdfName
              972  LOAD_FAST                'cls'
              974  LOAD_METHOD              interpret_name
              976  LOAD_FAST                'm'
              978  LOAD_METHOD              group
              980  LOAD_CONST               1
              982  CALL_METHOD_1         1  ''
              984  CALL_METHOD_1         1  ''
              986  CALL_FUNCTION_1       1  ''
              988  LOAD_FAST                'm'
              990  LOAD_METHOD              end
              992  CALL_METHOD_0         0  ''
              994  BUILD_TUPLE_2         2 
              996  RETURN_VALUE     
            998_0  COME_FROM           966  '966'

 L. 851       998  LOAD_FAST                'cls'
             1000  LOAD_ATTR                re_int
             1002  LOAD_METHOD              match
             1004  LOAD_FAST                'data'
             1006  LOAD_FAST                'offset'
             1008  CALL_METHOD_2         2  ''
             1010  STORE_FAST               'm'

 L. 852      1012  LOAD_FAST                'm'
         1014_1016  POP_JUMP_IF_FALSE  1040  'to 1040'

 L. 853      1018  LOAD_GLOBAL              int
             1020  LOAD_FAST                'm'
             1022  LOAD_METHOD              group
             1024  LOAD_CONST               1
             1026  CALL_METHOD_1         1  ''
             1028  CALL_FUNCTION_1       1  ''
             1030  LOAD_FAST                'm'
             1032  LOAD_METHOD              end
             1034  CALL_METHOD_0         0  ''
             1036  BUILD_TUPLE_2         2 
             1038  RETURN_VALUE     
           1040_0  COME_FROM          1014  '1014'

 L. 854      1040  LOAD_FAST                'cls'
             1042  LOAD_ATTR                re_real
             1044  LOAD_METHOD              match
             1046  LOAD_FAST                'data'
             1048  LOAD_FAST                'offset'
             1050  CALL_METHOD_2         2  ''
             1052  STORE_FAST               'm'

 L. 855      1054  LOAD_FAST                'm'
         1056_1058  POP_JUMP_IF_FALSE  1082  'to 1082'

 L. 857      1060  LOAD_GLOBAL              float
             1062  LOAD_FAST                'm'
             1064  LOAD_METHOD              group
             1066  LOAD_CONST               1
             1068  CALL_METHOD_1         1  ''
             1070  CALL_FUNCTION_1       1  ''
             1072  LOAD_FAST                'm'
             1074  LOAD_METHOD              end
             1076  CALL_METHOD_0         0  ''
             1078  BUILD_TUPLE_2         2 
             1080  RETURN_VALUE     
           1082_0  COME_FROM          1056  '1056'

 L. 858      1082  LOAD_FAST                'cls'
             1084  LOAD_ATTR                re_string_hex
             1086  LOAD_METHOD              match
             1088  LOAD_FAST                'data'
             1090  LOAD_FAST                'offset'
             1092  CALL_METHOD_2         2  ''
             1094  STORE_FAST               'm'

 L. 859      1096  LOAD_FAST                'm'
         1098_1100  POP_JUMP_IF_FALSE  1182  'to 1182'

 L. 861      1102  LOAD_GLOBAL              bytearray

 L. 862      1104  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1106  LOAD_STR                 'PdfParser.get_value.<locals>.<listcomp>'
             1108  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             1110  LOAD_FAST                'm'
             1112  LOAD_METHOD              group
             1114  LOAD_CONST               1
             1116  CALL_METHOD_1         1  ''
             1118  GET_ITER         
             1120  CALL_FUNCTION_1       1  ''

 L. 861      1122  CALL_FUNCTION_1       1  ''
             1124  STORE_FAST               'hex_string'

 L. 864      1126  LOAD_GLOBAL              len
             1128  LOAD_FAST                'hex_string'
             1130  CALL_FUNCTION_1       1  ''
             1132  LOAD_CONST               2
             1134  BINARY_MODULO    
             1136  LOAD_CONST               1
             1138  COMPARE_OP               ==
         1140_1142  POP_JUMP_IF_FALSE  1158  'to 1158'

 L. 866      1144  LOAD_FAST                'hex_string'
             1146  LOAD_METHOD              append
             1148  LOAD_GLOBAL              ord
             1150  LOAD_CONST               b'0'
             1152  CALL_FUNCTION_1       1  ''
             1154  CALL_METHOD_1         1  ''
             1156  POP_TOP          
           1158_0  COME_FROM          1140  '1140'

 L. 867      1158  LOAD_GLOBAL              bytearray
             1160  LOAD_METHOD              fromhex
             1162  LOAD_FAST                'hex_string'
             1164  LOAD_METHOD              decode
             1166  LOAD_STR                 'us-ascii'
             1168  CALL_METHOD_1         1  ''
             1170  CALL_METHOD_1         1  ''
             1172  LOAD_FAST                'm'
             1174  LOAD_METHOD              end
             1176  CALL_METHOD_0         0  ''
             1178  BUILD_TUPLE_2         2 
             1180  RETURN_VALUE     
           1182_0  COME_FROM          1098  '1098'

 L. 868      1182  LOAD_FAST                'cls'
             1184  LOAD_ATTR                re_string_lit
             1186  LOAD_METHOD              match
             1188  LOAD_FAST                'data'
             1190  LOAD_FAST                'offset'
             1192  CALL_METHOD_2         2  ''
             1194  STORE_FAST               'm'

 L. 869      1196  LOAD_FAST                'm'
         1198_1200  POP_JUMP_IF_FALSE  1218  'to 1218'

 L. 870      1202  LOAD_FAST                'cls'
             1204  LOAD_METHOD              get_literal_string
             1206  LOAD_FAST                'data'
             1208  LOAD_FAST                'm'
             1210  LOAD_METHOD              end
             1212  CALL_METHOD_0         0  ''
             1214  CALL_METHOD_2         2  ''
             1216  RETURN_VALUE     
           1218_0  COME_FROM          1198  '1198'

 L. 872      1218  LOAD_GLOBAL              PdfFormatError
             1220  LOAD_STR                 'unrecognized object: '
             1222  LOAD_GLOBAL              repr
             1224  LOAD_FAST                'data'
             1226  LOAD_FAST                'offset'
             1228  LOAD_FAST                'offset'
             1230  LOAD_CONST               32
             1232  BINARY_ADD       
             1234  BUILD_SLICE_2         2 
             1236  BINARY_SUBSCR    
             1238  CALL_FUNCTION_1       1  ''
             1240  BINARY_ADD       
             1242  CALL_FUNCTION_1       1  ''
             1244  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<117>' instruction at offset 110

    re_lit_str_token = re.compile(b'(\\\\[nrtbf()\\\\])|(\\\\[0-9]{1,3})|(\\\\(\\r\\n|\\r|\\n))|(\\r\\n|\\r|\\n)|(\\()|(\\))')
    escaped_chars = {b'n': b'\n', 
     b'r': b'\r', 
     b't': b'\t', 
     b'b': b'\x08', 
     b'f': b'\x0c', 
     b'(': b'(', 
     b')': b')', 
     b'\\': b'\\', 
     ord(b'n'): b'\n', 
     ord(b'r'): b'\r', 
     ord(b't'): b'\t', 
     ord(b'b'): b'\x08', 
     ord(b'f'): b'\x0c', 
     ord(b'('): b'(', 
     ord(b')'): b')', 
     ord(b'\\'): b'\\'}

    @classmethod
    def get_literal_string(cls, data, offset):
        nesting_depth = 0
        result = bytearray
        for m in cls.re_lit_str_token.finditer(data, offset):
            result.extend(data[offset:m.start()])
            if m.group(1):
                result.extend(cls.escaped_chars[m.group(1)[1]])
            else:
                if m.group(2):
                    result.append(int(m.group(2)[1:], 8))
                else:
                    if m.group(3):
                        break
                    if m.group(5):
                        result.extend(b'\n')
                    else:
                        if m.group(6):
                            result.extend(b'(')
                            nesting_depth += 1
                        else:
                            if m.group(7):
                                if nesting_depth == 0:
                                    return (
                                     bytes(result), m.end())
                                result.extend(b')')
                                nesting_depth -= 1
            offset = m.end()
        else:
            raise PdfFormatError('unfinished literal string')

    re_xref_section_start = re.compile(whitespace_optional + b'xref' + newline)
    re_xref_subsection_start = re.compile(whitespace_optional + b'([0-9]+)' + whitespace_mandatory + b'([0-9]+)' + whitespace_optional + newline_only)
    re_xref_entry = re.compile(b'([0-9]{10}) ([0-9]{5}) ([fn])( \\r| \\n|\\r\\n)')

    def read_xref_table--- This code section failed: ---

 L. 933         0  LOAD_CONST               False
                2  STORE_FAST               'subsection_found'

 L. 934         4  LOAD_FAST                'self'
                6  LOAD_ATTR                re_xref_section_start
                8  LOAD_METHOD              match

 L. 935        10  LOAD_FAST                'self'
               12  LOAD_ATTR                buf
               14  LOAD_FAST                'xref_section_offset'
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                start_offset
               20  BINARY_ADD       

 L. 934        22  CALL_METHOD_2         2  ''
               24  STORE_FAST               'm'

 L. 937        26  LOAD_GLOBAL              check_format_condition
               28  LOAD_FAST                'm'
               30  LOAD_STR                 'xref section start not found'
               32  CALL_FUNCTION_2       2  ''
               34  POP_TOP          

 L. 938        36  LOAD_FAST                'm'
               38  LOAD_METHOD              end
               40  CALL_METHOD_0         0  ''
               42  STORE_FAST               'offset'

 L. 940        44  LOAD_FAST                'self'
               46  LOAD_ATTR                re_xref_subsection_start
               48  LOAD_METHOD              match
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                buf
               54  LOAD_FAST                'offset'
               56  CALL_METHOD_2         2  ''
               58  STORE_FAST               'm'

 L. 941        60  LOAD_FAST                'm'
               62  POP_JUMP_IF_TRUE     78  'to 78'

 L. 942        64  LOAD_GLOBAL              check_format_condition

 L. 943        66  LOAD_FAST                'subsection_found'
               68  LOAD_STR                 'xref subsection start not found'

 L. 942        70  CALL_FUNCTION_2       2  ''
               72  POP_TOP          

 L. 945     74_76  BREAK_LOOP          264  'to 264'
             78_0  COME_FROM            62  '62'

 L. 946        78  LOAD_CONST               True
               80  STORE_FAST               'subsection_found'

 L. 947        82  LOAD_FAST                'm'
               84  LOAD_METHOD              end
               86  CALL_METHOD_0         0  ''
               88  STORE_FAST               'offset'

 L. 948        90  LOAD_GLOBAL              int
               92  LOAD_FAST                'm'
               94  LOAD_METHOD              group
               96  LOAD_CONST               1
               98  CALL_METHOD_1         1  ''
              100  CALL_FUNCTION_1       1  ''
              102  STORE_FAST               'first_object'

 L. 949       104  LOAD_GLOBAL              int
              106  LOAD_FAST                'm'
              108  LOAD_METHOD              group
              110  LOAD_CONST               2
              112  CALL_METHOD_1         1  ''
              114  CALL_FUNCTION_1       1  ''
              116  STORE_FAST               'num_objects'

 L. 950       118  LOAD_GLOBAL              range
              120  LOAD_FAST                'first_object'
              122  LOAD_FAST                'first_object'
              124  LOAD_FAST                'num_objects'
              126  BINARY_ADD       
              128  CALL_FUNCTION_2       2  ''
              130  GET_ITER         
            132_0  COME_FROM           200  '200'
              132  FOR_ITER            262  'to 262'
              134  STORE_FAST               'i'

 L. 951       136  LOAD_FAST                'self'
              138  LOAD_ATTR                re_xref_entry
              140  LOAD_METHOD              match
              142  LOAD_FAST                'self'
              144  LOAD_ATTR                buf
              146  LOAD_FAST                'offset'
              148  CALL_METHOD_2         2  ''
              150  STORE_FAST               'm'

 L. 952       152  LOAD_GLOBAL              check_format_condition
              154  LOAD_FAST                'm'
              156  LOAD_STR                 'xref entry not found'
              158  CALL_FUNCTION_2       2  ''
              160  POP_TOP          

 L. 953       162  LOAD_FAST                'm'
              164  LOAD_METHOD              end
              166  CALL_METHOD_0         0  ''
              168  STORE_FAST               'offset'

 L. 954       170  LOAD_FAST                'm'
              172  LOAD_METHOD              group
              174  LOAD_CONST               3
              176  CALL_METHOD_1         1  ''
              178  LOAD_CONST               b'f'
              180  COMPARE_OP               ==
              182  STORE_FAST               'is_free'

 L. 955       184  LOAD_GLOBAL              int
              186  LOAD_FAST                'm'
              188  LOAD_METHOD              group
              190  LOAD_CONST               2
              192  CALL_METHOD_1         1  ''
              194  CALL_FUNCTION_1       1  ''
              196  STORE_FAST               'generation'

 L. 956       198  LOAD_FAST                'is_free'
              200  POP_JUMP_IF_TRUE    132  'to 132'

 L. 957       202  LOAD_GLOBAL              int
              204  LOAD_FAST                'm'
              206  LOAD_METHOD              group
              208  LOAD_CONST               1
              210  CALL_METHOD_1         1  ''
              212  CALL_FUNCTION_1       1  ''
              214  LOAD_FAST                'generation'
              216  BUILD_TUPLE_2         2 
              218  STORE_FAST               'new_entry'

 L. 958       220  LOAD_GLOBAL              check_format_condition

 L. 959       222  LOAD_FAST                'i'
              224  LOAD_FAST                'self'
              226  LOAD_ATTR                xref_table
              228  <118>                 1  ''
              230  JUMP_IF_TRUE_OR_POP   244  'to 244'
              232  LOAD_FAST                'self'
              234  LOAD_ATTR                xref_table
              236  LOAD_FAST                'i'
              238  BINARY_SUBSCR    
              240  LOAD_FAST                'new_entry'
              242  COMPARE_OP               ==
            244_0  COME_FROM           230  '230'

 L. 960       244  LOAD_STR                 'xref entry duplicated (and not identical)'

 L. 958       246  CALL_FUNCTION_2       2  ''
              248  POP_TOP          

 L. 962       250  LOAD_FAST                'new_entry'
              252  LOAD_FAST                'self'
              254  LOAD_ATTR                xref_table
              256  LOAD_FAST                'i'
              258  STORE_SUBSCR     
              260  JUMP_BACK           132  'to 132'
              262  JUMP_BACK            44  'to 44'

 L. 963       264  LOAD_FAST                'offset'
              266  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 228

    def read_indirect(self, ref, max_nesting=-1):
        offset, generation = self.xref_table[ref[0]]
        check_format_condition(generation == ref[1], f"expected to find generation {ref[1]} for object ID {ref[0]} in xref table, instead found generation {generation} at offset {offset}")
        value = self.get_value((self.buf),
          (offset + self.start_offset),
          expect_indirect=IndirectReference(*ref),
          max_nesting=max_nesting)[0]
        self.cached_objects[ref] = value
        return value

    def linearize_page_tree--- This code section failed: ---

 L. 982         0  LOAD_FAST                'node'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 983         8  LOAD_FAST                'self'
               10  LOAD_ATTR                page_tree_root
               12  STORE_FAST               'node'
             14_0  COME_FROM             6  '6'

 L. 984        14  LOAD_GLOBAL              check_format_condition

 L. 985        16  LOAD_FAST                'node'
               18  LOAD_CONST               b'Type'
               20  BINARY_SUBSCR    
               22  LOAD_CONST               b'Pages'
               24  COMPARE_OP               ==
               26  LOAD_STR                 '/Type of page tree node is not /Pages'

 L. 984        28  CALL_FUNCTION_2       2  ''
               30  POP_TOP          

 L. 987        32  BUILD_LIST_0          0 
               34  STORE_FAST               'pages'

 L. 988        36  LOAD_FAST                'node'
               38  LOAD_CONST               b'Kids'
               40  BINARY_SUBSCR    
               42  GET_ITER         
               44  FOR_ITER            102  'to 102'
               46  STORE_FAST               'kid'

 L. 989        48  LOAD_FAST                'self'
               50  LOAD_METHOD              read_indirect
               52  LOAD_FAST                'kid'
               54  CALL_METHOD_1         1  ''
               56  STORE_FAST               'kid_object'

 L. 990        58  LOAD_FAST                'kid_object'
               60  LOAD_CONST               b'Type'
               62  BINARY_SUBSCR    
               64  LOAD_CONST               b'Page'
               66  COMPARE_OP               ==
               68  POP_JUMP_IF_FALSE    82  'to 82'

 L. 991        70  LOAD_FAST                'pages'
               72  LOAD_METHOD              append
               74  LOAD_FAST                'kid'
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          
               80  JUMP_BACK            44  'to 44'
             82_0  COME_FROM            68  '68'

 L. 993        82  LOAD_FAST                'pages'
               84  LOAD_METHOD              extend
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                linearize_page_tree
               90  LOAD_FAST                'kid_object'
               92  LOAD_CONST               ('node',)
               94  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               96  CALL_METHOD_1         1  ''
               98  POP_TOP          
              100  JUMP_BACK            44  'to 44'

 L. 994       102  LOAD_FAST                'pages'
              104  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1