# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\PIL\PdfParser.py
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

    def __eq__(self, other):
        return other.__class__ is self.__class__ and other.object_id == self.object_id and other.generation == self.generation

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

    def __setitem__(self, key, value):
        if self.reading_finished:
            self.new_entries[key] = value
        else:
            self.existing_entries[key] = value
        if key in self.deleted_entries:
            del self.deleted_entries[key]

    def __getitem__(self, key):
        try:
            return self.new_entries[key]
        except KeyError:
            return self.existing_entries[key]

    def __delitem__(self, key):
        if key in self.new_entries:
            generation = self.new_entries[key][1] + 1
            del self.new_entries[key]
            self.deleted_entries[key] = generation
        elif key in self.existing_entries:
            generation = self.existing_entries[key][1] + 1
            self.deleted_entries[key] = generation
        elif key in self.deleted_entries:
            generation = self.deleted_entries[key]
        else:
            raise IndexError('object ID ' + str(key) + " cannot be deleted because it doesn't exist")

    def __contains__(self, key):
        return key in self.existing_entries or key in self.new_entries

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
             68_0  COME_FROM           322  '322'

 L. 165        68  LOAD_FAST                'keys'
            70_72  POP_JUMP_IF_FALSE   324  'to 324'

 L. 167        74  LOAD_CONST               None
               76  STORE_FAST               'prev'

 L. 168        78  LOAD_GLOBAL              enumerate
               80  LOAD_FAST                'keys'
               82  CALL_FUNCTION_1       1  ''
               84  GET_ITER         
             86_0  COME_FROM           148  '148'
             86_1  COME_FROM           118  '118'
               86  FOR_ITER            150  'to 150'
               88  UNPACK_SEQUENCE_2     2 
               90  STORE_FAST               'index'
               92  STORE_FAST               'key'

 L. 169        94  LOAD_FAST                'prev'
               96  LOAD_CONST               None
               98  COMPARE_OP               is
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
            150_0  COME_FROM            86  '86'

 L. 176       150  LOAD_FAST                'keys'
              152  STORE_FAST               'contiguous_keys'

 L. 177       154  LOAD_CONST               None
              156  STORE_FAST               'keys'
            158_0  COME_FROM           146  '146'

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
            188_0  COME_FROM           320  '320'
            188_1  COME_FROM           222  '222'
              188  FOR_ITER            322  'to 322'
              190  STORE_FAST               'object_id'

 L. 180       192  LOAD_FAST                'object_id'
              194  LOAD_FAST                'self'
              196  LOAD_ATTR                new_entries
              198  COMPARE_OP               in
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

 L. 186       242  LOAD_STR                 'expected the next deleted object ID to be %s, instead found %s'

 L. 187       244  LOAD_FAST                'object_id'
              246  LOAD_FAST                'this_deleted_object_id'
              248  BUILD_TUPLE_2         2 

 L. 186       250  BINARY_MODULO    

 L. 184       252  CALL_FUNCTION_2       2  ''
              254  POP_TOP          

 L. 189       256  SETUP_FINALLY       270  'to 270'

 L. 190       258  LOAD_FAST                'deleted_keys'
              260  LOAD_CONST               0
              262  BINARY_SUBSCR    
              264  STORE_FAST               'next_in_linked_list'
              266  POP_BLOCK        
              268  JUMP_FORWARD        296  'to 296'
            270_0  COME_FROM_FINALLY   256  '256'

 L. 191       270  DUP_TOP          
              272  LOAD_GLOBAL              IndexError
              274  COMPARE_OP               exception-match
          276_278  POP_JUMP_IF_FALSE   294  'to 294'
              280  POP_TOP          
              282  POP_TOP          
              284  POP_TOP          

 L. 192       286  LOAD_CONST               0
              288  STORE_FAST               'next_in_linked_list'
              290  POP_EXCEPT       
              292  JUMP_FORWARD        296  'to 296'
            294_0  COME_FROM           276  '276'
              294  END_FINALLY      
            296_0  COME_FROM           292  '292'
            296_1  COME_FROM           268  '268'

 L. 193       296  LOAD_FAST                'f'
              298  LOAD_METHOD              write

 L. 194       300  LOAD_CONST               b'%010d %05d f \n'

 L. 195       302  LOAD_FAST                'next_in_linked_list'
              304  LOAD_FAST                'self'
              306  LOAD_ATTR                deleted_entries
              308  LOAD_FAST                'object_id'
              310  BINARY_SUBSCR    
              312  BUILD_TUPLE_2         2 

 L. 194       314  BINARY_MODULO    

 L. 193       316  CALL_METHOD_1         1  ''
              318  POP_TOP          
              320  JUMP_BACK           188  'to 188'
            322_0  COME_FROM           188  '188'
              322  JUMP_BACK            68  'to 68'
            324_0  COME_FROM            70  '70'

 L. 197       324  LOAD_FAST                'startxref'
              326  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 326


class PdfName:

    def __init__(self, name):
        if isinstance(name, PdfName):
            self.name = name.name
        elif isinstance(name, bytes):
            self.name = name
        else:
            self.name = name.encode('us-ascii')

    def name_as_str(self):
        return self.name.decode('us-ascii')

    def __eq__(self, other):
        return (isinstance(other, PdfName)) and (other.name == self.name) or (other == self.name)

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return 'PdfName(%s)' % repr(self.name)

    @classmethod
    def from_pdf_stream(cls, data):
        return cls(PdfParser.interpret_name(data))

    allowed_chars = set(range(33, 127)) - {ord(c) for c in '#%/()<>[]{}'}

    def __bytes__(self):
        result = bytearray(b'/')
        for b in self.name:
            if b in self.allowed_chars:
                result.append(b)
            else:
                result.extend(b'#%02X' % b)
        else:
            return bytes(result)


class PdfArray(list):

    def __bytes__(self):
        return b'[ ' + (b' ').join((pdf_repr(x) for x in self)) + b' ]'


class PdfDict(collections.UserDict):

    def __setattr__(self, key, value):
        if key == 'data':
            collections.UserDict.__setattr__(self, key, value)
        else:
            self[key.encode('us-ascii')] = value

    def __getattr__(self, key):
        try:
            value = self[key.encode('us-ascii')]
        except KeyError:
            raise AttributeError(key)
        else:
            if isinstance(value, bytes):
                value = decode_text(value)
            else:
                if key.endswith('Date'):
                    if value.startswith('D:'):
                        value = value[2:]
                    relationship = 'Z'
                    if len(value) > 17:
                        relationship = value[14]
                        offset = int(value[15:17]) * 60
                        if len(value) > 20:
                            offset += int(value[18:20])
                    format = '%Y%m%d%H%M%S'[:len(value) - 2]
                    value = time.strptime(value[:len(format) + 2], format)
                    if relationship in ('+', '-'):
                        offset *= 60
                        if relationship == '+':
                            offset *= -1
                        value = time.gmtime(calendar.timegm(value) + offset)
                return value

    def __bytes__(self):
        out = bytearray(b'<<')
        for key, value in self.items():
            if value is None:
                pass
            else:
                value = pdf_repr(value)
                out.extend(b'\n')
                out.extend(bytes(PdfName(key)))
                out.extend(b' ')
                out.extend(value)
        else:
            out.extend(b'\n>>')
            return bytes(out)


class PdfBinary:

    def __init__(self, data):
        self.data = data

    def __bytes__(self):
        return b'<%s>' % (b'').join((b'%02X' % b for b in self.data))


class PdfStream:

    def __init__(self, dictionary, buf):
        self.dictionary = dictionary
        self.buf = buf

    def decode(self):
        try:
            filter = self.dictionary.Filter
        except AttributeError:
            return self.buf
        else:
            if filter == b'FlateDecode':
                try:
                    expected_length = self.dictionary.DL
                except AttributeError:
                    expected_length = self.dictionary.Length
                else:
                    return zlib.decompress((self.buf), bufsize=(int(expected_length)))
            raise NotImplementedError('stream filter %s unknown/unsupported' % repr(self.dictionary.Filter))


def pdf_repr(x):
    if x is True:
        return b'true'
    if x is False:
        return b'false'
    if x is None:
        return b'null'
    if isinstance(x, (PdfName, PdfDict, PdfArray, PdfBinary)):
        return bytes(x)
    if isinstance(x, int):
        return str(x).encode('us-ascii')
    if isinstance(x, time.struct_time):
        return b'(D:' + time.strftime('%Y%m%d%H%M%SZ', x).encode('us-ascii') + b')'
    if isinstance(x, dict):
        return bytes(PdfDict(x))
    if isinstance(x, list):
        return bytes(PdfArray(x))
    if isinstance(x, str):
        return pdf_repr(encode_text(x))
    if isinstance(x, bytes):
        x = x.replace(b'\\', b'\\\\')
        x = x.replace(b'(', b'\\(')
        x = x.replace(b')', b'\\)')
        return b'(' + x + b')'
    return bytes(x)


class PdfParser:
    __doc__ = 'Based on\n    https://www.adobe.com/content/dam/acom/en/devnet/acrobat/pdfs/PDF32000_2008.pdf\n    Supports PDF up to 1.4\n    '

    def __init__(self, filename=None, f=None, buf=None, start_offset=0, mode='rb'):
        if buf:
            if f:
                raise RuntimeError('specify buf or f or filename, but not both buf and f')
        self.filename = filename
        self.buf = buf
        self.f = f
        self.start_offset = start_offset
        self.should_close_buf = False
        self.should_close_file = False
        if filename is not None:
            if f is None:
                self.f = f = open(filename, mode)
                self.should_close_file = True
        if f is not None:
            self.buf = buf = self.get_buf_from_file(f)
            self.should_close_buf = True
            if not filename:
                if hasattr(f, 'name'):
                    self.filename = f.name
            self.cached_objects = {}
            if buf:
                self.read_pdf_info()
            else:
                self.file_size_total = self.file_size_this = 0
                self.root = PdfDict()
                self.root_ref = None
                self.info = PdfDict()
                self.info_ref = None
                self.page_tree_root = {}
                self.pages = []
                self.orig_pages = []
                self.pages_ref = None
                self.last_xref_section_offset = None
                self.trailer_dict = {}
                self.xref_table = XrefTable()
            self.xref_table.reading_finished = True
            if f:
                self.seek_end()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return False

    def start_writing(self):
        self.close_buf()
        self.seek_end()

    def close_buf(self):
        try:
            self.buf.close()
        except AttributeError:
            pass
        else:
            self.buf = None

    def close(self):
        if self.should_close_buf:
            self.close_buf()
        if self.f is not None:
            if self.should_close_file:
                self.f.close()
                self.f = None

    def seek_end(self):
        self.f.seek(0, os.SEEK_END)

    def write_header(self):
        self.f.write(b'%PDF-1.4\n')

    def write_comment(self, s):
        self.f.write('% {}\n'.format(s).encode('utf-8'))

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

    def rewrite_pages(self):
        pages_tree_nodes_to_delete = []
        for i, page_ref in enumerate(self.orig_pages):
            page_info = self.cached_objects[page_ref]
            del self.xref_table[page_ref.object_id]
            pages_tree_nodes_to_delete.append(page_info[PdfName(b'Parent')])
            if page_ref not in self.pages:
                pass
            else:
                stringified_page_info = {}
                for key, value in page_info.items():
                    stringified_page_info[key.name_as_str()] = value

        else:
            stringified_page_info['Parent'] = self.pages_ref
            new_page_ref = (self.write_page)(*(None, ), **stringified_page_info)

        for j, cur_page_ref in enumerate(self.pages):
            if cur_page_ref == page_ref:
                self.pages[j] = new_page_ref
        else:
            for pages_tree_node_ref in pages_tree_nodes_to_delete:
                while True:
                    if pages_tree_node_ref:
                        pages_tree_node = self.cached_objects[pages_tree_node_ref]
                        if pages_tree_node_ref.object_id in self.xref_table:
                            del self.xref_table[pages_tree_node_ref.object_id]
                        else:
                            pages_tree_node_ref = pages_tree_node.get(b'Parent', None)

            else:
                self.orig_pages = []

    def write_xref_and_trailer(self, new_root_ref=None):
        if new_root_ref:
            self.del_root()
            self.root_ref = new_root_ref
        if self.info:
            self.info_ref = self.write_obj(None, self.info)
        start_xref = self.xref_table.write(self.f)
        num_entries = len(self.xref_table)
        trailer_dict = {b'Root':self.root_ref,  b'Size':num_entries}
        if self.last_xref_section_offset is not None:
            trailer_dict[b'Prev'] = self.last_xref_section_offset
        if self.info:
            trailer_dict[b'Info'] = self.info_ref
        self.last_xref_section_offset = start_xref
        self.f.write(b'trailer\n' + bytes(PdfDict(trailer_dict)) + b'\nstartxref\n%d\n%%%%EOF' % start_xref)

    def write_page(self, ref, *objs, **dict_obj):
        if isinstance(ref, int):
            ref = self.pages[ref]
        if 'Type' not in dict_obj:
            dict_obj['Type'] = PdfName(b'Page')
        if 'Parent' not in dict_obj:
            dict_obj['Parent'] = self.pages_ref
        return (self.write_obj)(ref, *objs, **dict_obj)

    def write_obj(self, ref, *objs, **dict_obj):
        f = self.f
        if ref is None:
            ref = self.next_object_id(f.tell())
        else:
            self.xref_table[ref.object_id] = (
             f.tell(), ref.generation)
        f.write(bytes(IndirectObjectDef(*ref)))
        stream = dict_obj.pop('stream', None)
        if stream is not None:
            dict_obj['Length'] = len(stream)
        if dict_obj:
            f.write(pdf_repr(dict_obj))
        for obj in objs:
            f.write(pdf_repr(obj))
        else:
            if stream is not None:
                f.write(b'stream\n')
                f.write(stream)
                f.write(b'\nendstream\n')
            f.write(b'endobj\n')
            return ref

    def del_root(self):
        if self.root_ref is None:
            return
        del self.xref_table[self.root_ref.object_id]
        del self.xref_table[self.root[b'Pages'].object_id]

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
               66  COMPARE_OP               exception-match
               68  POP_JUMP_IF_FALSE    82  'to 82'
               70  POP_TOP          
               72  POP_TOP          
               74  POP_TOP          

 L. 537        76  POP_EXCEPT       
               78  LOAD_CONST               b''
               80  RETURN_VALUE     
             82_0  COME_FROM            68  '68'
               82  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 78

    def read_pdf_info(self):
        self.file_size_total = len(self.buf)
        self.file_size_this = self.file_size_total - self.start_offset
        self.read_trailer()
        self.root_ref = self.trailer_dict[b'Root']
        self.info_ref = self.trailer_dict.get(b'Info', None)
        self.root = PdfDict(self.read_indirect(self.root_ref))
        if self.info_ref is None:
            self.info = PdfDict()
        else:
            self.info = PdfDict(self.read_indirect(self.info_ref))
        check_format_condition(b'Type' in self.root, '/Type missing in Root')
        check_format_condition(self.root[b'Type'] == b'Catalog', '/Type in Root is not /Catalog')
        check_format_condition(b'Pages' in self.root, '/Pages missing in Root')
        check_format_condition(isinstance(self.root[b'Pages'], IndirectReference), '/Pages in Root is not an indirect reference')
        self.pages_ref = self.root[b'Pages']
        self.page_tree_root = self.read_indirect(self.pages_ref)
        self.pages = self.linearize_page_tree(self.page_tree_root)
        self.orig_pages = self.pages[:]

    def next_object_id(self, offset=None):
        try:
            reference = IndirectReference(max(self.xref_table.keys()) + 1, 0)
        except ValueError:
            reference = IndirectReference(1, 0)
        else:
            if offset is not None:
                self.xref_table[reference.object_id] = (
                 offset, 0)
            else:
                return reference

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

    def read_trailer(self):
        search_start_offset = len(self.buf) - 16384
        if search_start_offset < self.start_offset:
            search_start_offset = self.start_offset
        m = self.re_trailer_end.search(self.buf, search_start_offset)
        check_format_condition(m, 'trailer end not found')
        last_match = m
        while True:
            if m:
                last_match = m
                m = self.re_trailer_end.search(self.buf, m.start() + 16)

        if not m:
            m = last_match
        trailer_data = m.group(1)
        self.last_xref_section_offset = int(m.group(2))
        self.trailer_dict = self.interpret_trailer(trailer_data)
        self.xref_table = XrefTable()
        self.read_xref_table(xref_section_offset=(self.last_xref_section_offset))
        if b'Prev' in self.trailer_dict:
            self.read_prev_trailer(self.trailer_dict[b'Prev'])

    def read_prev_trailer(self, xref_section_offset):
        trailer_offset = self.read_xref_table(xref_section_offset=xref_section_offset)
        m = self.re_trailer_prev.search(self.buf[trailer_offset:trailer_offset + 16384])
        check_format_condition(m, 'previous trailer not found')
        trailer_data = m.group(1)
        check_format_condition(int(m.group(2)) == xref_section_offset, "xref section offset in previous trailer doesn't match what was expected")
        trailer_dict = self.interpret_trailer(trailer_data)
        if b'Prev' in trailer_dict:
            self.read_prev_trailer(trailer_dict[b'Prev'])

    re_whitespace_optional = re.compile(whitespace_optional)
    re_name = re.compile(whitespace_optional + b"/([!-$&'*-.0-;=?-Z\\\\^-z|~]+)(?=" + delimiter_or_ws + b')')
    re_dict_start = re.compile(whitespace_optional + b'\\<\\<')
    re_dict_end = re.compile(whitespace_optional + b'\\>\\>' + whitespace_optional)

    @classmethod
    def interpret_trailer(cls, trailer_data):
        trailer = {}
        offset = 0
        while True:
            m = cls.re_name.match(trailer_data, offset)
            if not m:
                m = cls.re_dict_end.match(trailer_data, offset)
                check_format_condition(m and m.end() == len(trailer_data), 'name not found in trailer, remaining data: ' + repr(trailer_data[offset:]))
            else:
                key = cls.interpret_name(m.group(1))
                value, offset = cls.get_value(trailer_data, m.end())
                trailer[key] = value

        check_format_condition(b'Size' in trailer and isinstance(trailer[b'Size'], int), '/Size not in trailer or not an integer')
        check_format_condition(b'Root' in trailer and isinstance(trailer[b'Root'], IndirectReference), '/Root not in trailer or not an indirect reference')
        return trailer

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
    def get_value(cls, data, offset, expect_indirect=None, max_nesting=-1):
        if max_nesting == 0:
            return (None, None)
        m = cls.re_comment.match(data, offset)
        if m:
            offset = m.end()
        m = cls.re_indirect_def_start.match(data, offset)
        if m:
            check_format_condition(int(m.group(1)) > 0, 'indirect object definition: object ID must be greater than 0')
            check_format_condition(int(m.group(2)) >= 0, 'indirect object definition: generation must be non-negative')
            check_format_condition(expect_indirect is None or expect_indirect == IndirectReference(int(m.group(1)), int(m.group(2))), 'indirect object definition different than expected')
            object, offset = cls.get_value(data, (m.end()), max_nesting=(max_nesting - 1))
            if offset is None:
                return (object, None)
            m = cls.re_indirect_def_end.match(data, offset)
            check_format_condition(m, 'indirect object definition end not found')
            return (
             object, m.end())
        check_format_condition(not expect_indirect, 'indirect object definition not found')
        m = cls.re_indirect_reference.match(data, offset)
        if m:
            check_format_condition(int(m.group(1)) > 0, 'indirect object reference: object ID must be greater than 0')
            check_format_condition(int(m.group(2)) >= 0, 'indirect object reference: generation must be non-negative')
            return (
             IndirectReference(int(m.group(1)), int(m.group(2))), m.end())
        m = cls.re_dict_start.match(data, offset)
        if m:
            offset = m.end()
            result = {}
            m = cls.re_dict_end.match(data, offset)
            while True:
                key, offset = m or cls.get_value(data, offset, max_nesting=(max_nesting - 1))
                if offset is None:
                    return (result, None)
                else:
                    value, offset = cls.get_value(data, offset, max_nesting=(max_nesting - 1))
                    result[key] = value
                    if offset is None:
                        return (result, None)
                    m = cls.re_dict_end.match(data, offset)

            offset = m.end()
            m = cls.re_stream_start.match(data, offset)
            if m:
                try:
                    stream_len = int(result[b'Length'])
                except (TypeError, KeyError, ValueError):
                    raise PdfFormatError('bad or missing Length in stream dict (%r)' % result.get(b'Length', None))
                else:
                    stream_data = data[m.end():m.end() + stream_len]
                    m = cls.re_stream_end.match(data, m.end() + stream_len)
                    check_format_condition(m, 'stream end not found')
                    offset = m.end()
                    result = PdfStream(PdfDict(result), stream_data)
            else:
                result = PdfDict(result)
            return (result, offset)
        m = cls.re_array_start.match(data, offset)
        if m:
            offset = m.end()
            result = []
            m = cls.re_array_end.match(data, offset)
            while True:
                value, offset = m or cls.get_value(data, offset, max_nesting=(max_nesting - 1))
                result.append(value)
                if offset is None:
                    return (result, None)
                else:
                    m = cls.re_array_end.match(data, offset)

            return (
             result, m.end())
        m = cls.re_null.match(data, offset)
        if m:
            return (None, m.end())
        m = cls.re_true.match(data, offset)
        if m:
            return (True, m.end())
        m = cls.re_false.match(data, offset)
        if m:
            return (False, m.end())
        m = cls.re_name.match(data, offset)
        if m:
            return (PdfName(cls.interpret_name(m.group(1))), m.end())
        m = cls.re_int.match(data, offset)
        if m:
            return (int(m.group(1)), m.end())
        m = cls.re_real.match(data, offset)
        if m:
            return (
             float(m.group(1)), m.end())
        m = cls.re_string_hex.match(data, offset)
        if m:
            hex_string = bytearray([b for b in m.group(1) if b in b'0123456789abcdefABCDEF'])
            if len(hex_string) % 2 == 1:
                hex_string.append(ord(b'0'))
            return (bytearray.fromhex(hex_string.decode('us-ascii')), m.end())
        m = cls.re_string_lit.match(data, offset)
        if m:
            return cls.get_literal_string(data, m.end())
        raise PdfFormatError('unrecognized object: ' + repr(data[offset:offset + 32]))

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
        result = bytearray()
        for m in cls.re_lit_str_token.finditer(data, offset):
            result.extend(data[offset:m.start()])
            if m.group(1):
                result.extend(cls.escaped_chars[m.group(1)[1]])
            elif m.group(2):
                result.append(int(m.group(2)[1:], 8))
            elif m.group(3):
                pass
            elif m.group(5):
                result.extend(b'\n')
            elif m.group(6):
                result.extend(b'(')
                nesting_depth += 1
            elif m.group(7):
                if nesting_depth == 0:
                    return (bytes(result), m.end())
                result.extend(b')')
                nesting_depth -= 1
            offset = m.end()
        else:
            raise PdfFormatError('unfinished literal string')

    re_xref_section_start = re.compile(whitespace_optional + b'xref' + newline)
    re_xref_subsection_start = re.compile(whitespace_optional + b'([0-9]+)' + whitespace_mandatory + b'([0-9]+)' + whitespace_optional + newline_only)
    re_xref_entry = re.compile(b'([0-9]{10}) ([0-9]{5}) ([fn])( \\r| \\n|\\r\\n)')

    def read_xref_table(self, xref_section_offset):
        subsection_found = False
        m = self.re_xref_section_start.match(self.buf, xref_section_offset + self.start_offset)
        check_format_condition(m, 'xref section start not found')
        offset = m.end()
        while True:
            m = self.re_xref_subsection_start.match(self.buf, offset)
            if not m:
                check_format_condition(subsection_found, 'xref subsection start not found')
            else:
                subsection_found = True
                offset = m.end()
                first_object = int(m.group(1))
                num_objects = int(m.group(2))
                for i in range(first_object, first_object + num_objects):
                    m = self.re_xref_entry.match(self.buf, offset)
                    check_format_condition(m, 'xref entry not found')
                    offset = m.end()
                    is_free = m.group(3) == b'f'
                    generation = int(m.group(2))
                    if not is_free:
                        new_entry = (
                         int(m.group(1)), generation)
                        check_format_condition(i not in self.xref_table or self.xref_table[i] == new_entry, 'xref entry duplicated (and not identical)')
                        self.xref_table[i] = new_entry

        return offset

    def read_indirect(self, ref, max_nesting=-1):
        offset, generation = self.xref_table[ref[0]]
        check_format_condition(generation == ref[1], 'expected to find generation %s for object ID %s in xref table, instead found generation %s at offset %s' % (
         ref[1], ref[0], generation, offset))
        value = self.get_value((self.buf),
          (offset + self.start_offset),
          expect_indirect=IndirectReference(*ref),
          max_nesting=max_nesting)[0]
        self.cached_objects[ref] = value
        return value

    def linearize_page_tree(self, node=None):
        if node is None:
            node = self.page_tree_root
        check_format_condition(node[b'Type'] == b'Pages', '/Type of page tree node is not /Pages')
        pages = []
        for kid in node[b'Kids']:
            kid_object = self.read_indirect(kid)
            if kid_object[b'Type'] == b'Page':
                pages.append(kid)
            else:
                pages.extend(self.linearize_page_tree(node=kid_object))
        else:
            return pages