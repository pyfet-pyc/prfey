# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: aiohttp\formdata.py
import io
from typing import Any, Iterable, List, Optional
from urllib.parse import urlencode
from multidict import MultiDict, MultiDictProxy
from . import hdrs, multipart, payload
from .helpers import guess_filename
from .payload import Payload
__all__ = ('FormData', )

class FormData:
    __doc__ = 'Helper class for multipart/form-data and\n    application/x-www-form-urlencoded body generation.'

    def __init__(self, fields: Iterable[Any]=(), quote_fields: bool=True, charset: Optional[str]=None) -> None:
        self._writer = multipart.MultipartWriter('form-data')
        self._fields = []
        self._is_multipart = False
        self._is_processed = False
        self._quote_fields = quote_fields
        self._charset = charset
        if isinstance(fields, dict):
            fields = list(fields.items())
        elif not isinstance(fields, (list, tuple)):
            fields = (
             fields,)
        (self.add_fields)(*fields)

    @property
    def is_multipart(self) -> bool:
        return self._is_multipart

    def add_field--- This code section failed: ---

 L.  51         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'value'
                4  LOAD_GLOBAL              io
                6  LOAD_ATTR                IOBase
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L.  52        12  LOAD_CONST               True
               14  LOAD_FAST                'self'
               16  STORE_ATTR               _is_multipart
               18  JUMP_FORWARD         56  'to 56'
             20_0  COME_FROM            10  '10'

 L.  53        20  LOAD_GLOBAL              isinstance
               22  LOAD_FAST                'value'
               24  LOAD_GLOBAL              bytes
               26  LOAD_GLOBAL              bytearray
               28  LOAD_GLOBAL              memoryview
               30  BUILD_TUPLE_3         3 
               32  CALL_FUNCTION_2       2  ''
               34  POP_JUMP_IF_FALSE    56  'to 56'

 L.  54        36  LOAD_FAST                'filename'
               38  LOAD_CONST               None
               40  <117>                 0  ''
               42  POP_JUMP_IF_FALSE    56  'to 56'
               44  LOAD_FAST                'content_transfer_encoding'
               46  LOAD_CONST               None
               48  <117>                 0  ''
               50  POP_JUMP_IF_FALSE    56  'to 56'

 L.  55        52  LOAD_FAST                'name'
               54  STORE_FAST               'filename'
             56_0  COME_FROM            50  '50'
             56_1  COME_FROM            42  '42'
             56_2  COME_FROM            34  '34'
             56_3  COME_FROM            18  '18'

 L.  57        56  LOAD_GLOBAL              MultiDict
               58  LOAD_STR                 'name'
               60  LOAD_FAST                'name'
               62  BUILD_MAP_1           1 
               64  CALL_FUNCTION_1       1  ''
               66  STORE_FAST               'type_options'

 L.  58        68  LOAD_FAST                'filename'
               70  LOAD_CONST               None
               72  <117>                 1  ''
               74  POP_JUMP_IF_FALSE    98  'to 98'
               76  LOAD_GLOBAL              isinstance
               78  LOAD_FAST                'filename'
               80  LOAD_GLOBAL              str
               82  CALL_FUNCTION_2       2  ''
               84  POP_JUMP_IF_TRUE     98  'to 98'

 L.  59        86  LOAD_GLOBAL              TypeError

 L.  60        88  LOAD_STR                 'filename must be an instance of str. Got: %s'
               90  LOAD_FAST                'filename'
               92  BINARY_MODULO    

 L.  59        94  CALL_FUNCTION_1       1  ''
               96  RAISE_VARARGS_1       1  'exception instance'
             98_0  COME_FROM            84  '84'
             98_1  COME_FROM            74  '74'

 L.  62        98  LOAD_FAST                'filename'
              100  LOAD_CONST               None
              102  <117>                 0  ''
              104  POP_JUMP_IF_FALSE   128  'to 128'
              106  LOAD_GLOBAL              isinstance
              108  LOAD_FAST                'value'
              110  LOAD_GLOBAL              io
              112  LOAD_ATTR                IOBase
              114  CALL_FUNCTION_2       2  ''
              116  POP_JUMP_IF_FALSE   128  'to 128'

 L.  63       118  LOAD_GLOBAL              guess_filename
              120  LOAD_FAST                'value'
              122  LOAD_FAST                'name'
              124  CALL_FUNCTION_2       2  ''
              126  STORE_FAST               'filename'
            128_0  COME_FROM           116  '116'
            128_1  COME_FROM           104  '104'

 L.  64       128  LOAD_FAST                'filename'
              130  LOAD_CONST               None
              132  <117>                 1  ''
              134  POP_JUMP_IF_FALSE   150  'to 150'

 L.  65       136  LOAD_FAST                'filename'
              138  LOAD_FAST                'type_options'
              140  LOAD_STR                 'filename'
              142  STORE_SUBSCR     

 L.  66       144  LOAD_CONST               True
              146  LOAD_FAST                'self'
              148  STORE_ATTR               _is_multipart
            150_0  COME_FROM           134  '134'

 L.  68       150  BUILD_MAP_0           0 
              152  STORE_FAST               'headers'

 L.  69       154  LOAD_FAST                'content_type'
              156  LOAD_CONST               None
              158  <117>                 1  ''
              160  POP_JUMP_IF_FALSE   200  'to 200'

 L.  70       162  LOAD_GLOBAL              isinstance
              164  LOAD_FAST                'content_type'
              166  LOAD_GLOBAL              str
              168  CALL_FUNCTION_2       2  ''
              170  POP_JUMP_IF_TRUE    184  'to 184'

 L.  71       172  LOAD_GLOBAL              TypeError

 L.  72       174  LOAD_STR                 'content_type must be an instance of str. Got: %s'
              176  LOAD_FAST                'content_type'
              178  BINARY_MODULO    

 L.  71       180  CALL_FUNCTION_1       1  ''
              182  RAISE_VARARGS_1       1  'exception instance'
            184_0  COME_FROM           170  '170'

 L.  74       184  LOAD_FAST                'content_type'
              186  LOAD_FAST                'headers'
              188  LOAD_GLOBAL              hdrs
              190  LOAD_ATTR                CONTENT_TYPE
              192  STORE_SUBSCR     

 L.  75       194  LOAD_CONST               True
              196  LOAD_FAST                'self'
              198  STORE_ATTR               _is_multipart
            200_0  COME_FROM           160  '160'

 L.  76       200  LOAD_FAST                'content_transfer_encoding'
              202  LOAD_CONST               None
              204  <117>                 1  ''
              206  POP_JUMP_IF_FALSE   246  'to 246'

 L.  77       208  LOAD_GLOBAL              isinstance
              210  LOAD_FAST                'content_transfer_encoding'
              212  LOAD_GLOBAL              str
              214  CALL_FUNCTION_2       2  ''
              216  POP_JUMP_IF_TRUE    230  'to 230'

 L.  78       218  LOAD_GLOBAL              TypeError

 L.  79       220  LOAD_STR                 'content_transfer_encoding must be an instance of str. Got: %s'

 L.  80       222  LOAD_FAST                'content_transfer_encoding'

 L.  79       224  BINARY_MODULO    

 L.  78       226  CALL_FUNCTION_1       1  ''
              228  RAISE_VARARGS_1       1  'exception instance'
            230_0  COME_FROM           216  '216'

 L.  82       230  LOAD_FAST                'content_transfer_encoding'
              232  LOAD_FAST                'headers'
              234  LOAD_GLOBAL              hdrs
              236  LOAD_ATTR                CONTENT_TRANSFER_ENCODING
              238  STORE_SUBSCR     

 L.  83       240  LOAD_CONST               True
              242  LOAD_FAST                'self'
              244  STORE_ATTR               _is_multipart
            246_0  COME_FROM           206  '206'

 L.  85       246  LOAD_FAST                'self'
              248  LOAD_ATTR                _fields
              250  LOAD_METHOD              append
              252  LOAD_FAST                'type_options'
              254  LOAD_FAST                'headers'
              256  LOAD_FAST                'value'
              258  BUILD_TUPLE_3         3 
              260  CALL_METHOD_1         1  ''
              262  POP_TOP          

Parse error at or near `<117>' instruction at offset 40

    def add_fields(self, *fields: Any) -> None:
        to_add = list(fields)
        while True:
            if to_add:
                rec = to_add.pop(0)
                if isinstance(rec, io.IOBase):
                    k = guess_filename(rec, 'unknown')
                    self.add_field(k, rec)
                else:
                    if isinstance(rec, (MultiDictProxy, MultiDict)):
                        to_add.extend(rec.items())
                    else:
                        if isinstance(rec, (list, tuple)) and len(rec) == 2:
                            k, fp = rec
                            self.add_field(k, fp)
                        else:
                            raise TypeError('Only io.IOBase, multidict and (name, file) pairs allowed, use .add_field() for passing more complex parameters, got {!r}'.format(rec))

    def _gen_form_urlencoded--- This code section failed: ---

 L. 113         0  BUILD_LIST_0          0 
                2  STORE_FAST               'data'

 L. 114         4  LOAD_FAST                'self'
                6  LOAD_ATTR                _fields
                8  GET_ITER         
             10_0  COME_FROM            38  '38'
               10  FOR_ITER             40  'to 40'
               12  UNPACK_SEQUENCE_3     3 
               14  STORE_FAST               'type_options'
               16  STORE_FAST               '_'
               18  STORE_FAST               'value'

 L. 115        20  LOAD_FAST                'data'
               22  LOAD_METHOD              append
               24  LOAD_FAST                'type_options'
               26  LOAD_STR                 'name'
               28  BINARY_SUBSCR    
               30  LOAD_FAST                'value'
               32  BUILD_TUPLE_2         2 
               34  CALL_METHOD_1         1  ''
               36  POP_TOP          
               38  JUMP_BACK            10  'to 10'
             40_0  COME_FROM            10  '10'

 L. 117        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _charset
               44  LOAD_CONST               None
               46  <117>                 1  ''
               48  POP_JUMP_IF_FALSE    56  'to 56'
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                _charset
               54  JUMP_FORWARD         58  'to 58'
             56_0  COME_FROM            48  '48'
               56  LOAD_STR                 'utf-8'
             58_0  COME_FROM            54  '54'
               58  STORE_FAST               'charset'

 L. 119        60  LOAD_FAST                'charset'
               62  LOAD_STR                 'utf-8'
               64  COMPARE_OP               ==
               66  POP_JUMP_IF_FALSE    74  'to 74'

 L. 120        68  LOAD_STR                 'application/x-www-form-urlencoded'
               70  STORE_FAST               'content_type'
               72  JUMP_FORWARD         82  'to 82'
             74_0  COME_FROM            66  '66'

 L. 122        74  LOAD_STR                 'application/x-www-form-urlencoded; charset=%s'
               76  LOAD_FAST                'charset'
               78  BINARY_MODULO    
               80  STORE_FAST               'content_type'
             82_0  COME_FROM            72  '72'

 L. 124        82  LOAD_GLOBAL              payload
               84  LOAD_ATTR                BytesPayload

 L. 125        86  LOAD_GLOBAL              urlencode
               88  LOAD_FAST                'data'
               90  LOAD_CONST               True
               92  LOAD_FAST                'charset'
               94  LOAD_CONST               ('doseq', 'encoding')
               96  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               98  LOAD_METHOD              encode
              100  CALL_METHOD_0         0  ''

 L. 126       102  LOAD_FAST                'content_type'

 L. 124       104  LOAD_CONST               ('content_type',)
              106  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              108  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 46

    def _gen_form_data--- This code section failed: ---

 L. 131         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _is_processed
                4  POP_JUMP_IF_FALSE    14  'to 14'

 L. 132         6  LOAD_GLOBAL              RuntimeError
                8  LOAD_STR                 'Form data has been processed already'
               10  CALL_FUNCTION_1       1  ''
               12  RAISE_VARARGS_1       1  'exception instance'
             14_0  COME_FROM             4  '4'

 L. 133        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _fields
               18  GET_ITER         
             20_0  COME_FROM           220  '220'
               20  FOR_ITER            222  'to 222'
               22  UNPACK_SEQUENCE_3     3 
               24  STORE_FAST               'dispparams'
               26  STORE_FAST               'headers'
               28  STORE_FAST               'value'

 L. 134        30  SETUP_FINALLY        92  'to 92'

 L. 135        32  LOAD_GLOBAL              hdrs
               34  LOAD_ATTR                CONTENT_TYPE
               36  LOAD_FAST                'headers'
               38  <118>                 0  ''
               40  POP_JUMP_IF_FALSE    70  'to 70'

 L. 136        42  LOAD_GLOBAL              payload
               44  LOAD_ATTR                get_payload

 L. 137        46  LOAD_FAST                'value'

 L. 138        48  LOAD_FAST                'headers'
               50  LOAD_GLOBAL              hdrs
               52  LOAD_ATTR                CONTENT_TYPE
               54  BINARY_SUBSCR    

 L. 139        56  LOAD_FAST                'headers'

 L. 140        58  LOAD_FAST                'self'
               60  LOAD_ATTR                _charset

 L. 136        62  LOAD_CONST               ('content_type', 'headers', 'encoding')
               64  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               66  STORE_FAST               'part'
               68  JUMP_FORWARD         88  'to 88'
             70_0  COME_FROM            40  '40'

 L. 143        70  LOAD_GLOBAL              payload
               72  LOAD_ATTR                get_payload

 L. 144        74  LOAD_FAST                'value'
               76  LOAD_FAST                'headers'
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                _charset

 L. 143        82  LOAD_CONST               ('headers', 'encoding')
               84  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               86  STORE_FAST               'part'
             88_0  COME_FROM            68  '68'
               88  POP_BLOCK        
               90  JUMP_FORWARD        152  'to 152'
             92_0  COME_FROM_FINALLY    30  '30'

 L. 146        92  DUP_TOP          
               94  LOAD_GLOBAL              Exception
               96  <121>               150  ''
               98  POP_TOP          
              100  STORE_FAST               'exc'
              102  POP_TOP          
              104  SETUP_FINALLY       142  'to 142'

 L. 147       106  LOAD_GLOBAL              TypeError

 L. 148       108  LOAD_STR                 'Can not serialize value type: %r\n headers: %r\n value: %r'

 L. 149       110  LOAD_GLOBAL              type
              112  LOAD_FAST                'value'
              114  CALL_FUNCTION_1       1  ''
              116  LOAD_FAST                'headers'
              118  LOAD_FAST                'value'
              120  BUILD_TUPLE_3         3 

 L. 148       122  BINARY_MODULO    

 L. 147       124  CALL_FUNCTION_1       1  ''

 L. 150       126  LOAD_FAST                'exc'

 L. 147       128  RAISE_VARARGS_2       2  'exception instance with __cause__'
              130  POP_BLOCK        
              132  POP_EXCEPT       
              134  LOAD_CONST               None
              136  STORE_FAST               'exc'
              138  DELETE_FAST              'exc'
              140  JUMP_FORWARD        152  'to 152'
            142_0  COME_FROM_FINALLY   104  '104'
              142  LOAD_CONST               None
              144  STORE_FAST               'exc'
              146  DELETE_FAST              'exc'
              148  <48>             
              150  <48>             
            152_0  COME_FROM           140  '140'
            152_1  COME_FROM            90  '90'

 L. 152       152  LOAD_FAST                'dispparams'
              154  POP_JUMP_IF_FALSE   208  'to 208'

 L. 153       156  LOAD_FAST                'part'
              158  LOAD_ATTR                set_content_disposition

 L. 153       160  LOAD_CONST               ('form-data',)
              162  LOAD_STR                 'quote_fields'

 L. 154       164  LOAD_FAST                'self'
              166  LOAD_ATTR                _quote_fields

 L. 153       168  BUILD_MAP_1           1 

 L. 154       170  LOAD_FAST                'dispparams'

 L. 153       172  <164>                 1  ''
              174  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              176  POP_TOP          

 L. 158       178  LOAD_FAST                'part'
              180  LOAD_ATTR                headers
              182  LOAD_CONST               None
              184  <117>                 1  ''
              186  POP_JUMP_IF_TRUE    192  'to 192'
              188  <74>             
              190  RAISE_VARARGS_1       1  'exception instance'
            192_0  COME_FROM           186  '186'

 L. 159       192  LOAD_FAST                'part'
              194  LOAD_ATTR                headers
              196  LOAD_METHOD              popall
              198  LOAD_GLOBAL              hdrs
              200  LOAD_ATTR                CONTENT_LENGTH
              202  LOAD_CONST               None
              204  CALL_METHOD_2         2  ''
              206  POP_TOP          
            208_0  COME_FROM           154  '154'

 L. 161       208  LOAD_FAST                'self'
              210  LOAD_ATTR                _writer
              212  LOAD_METHOD              append_payload
              214  LOAD_FAST                'part'
              216  CALL_METHOD_1         1  ''
              218  POP_TOP          
              220  JUMP_BACK            20  'to 20'
            222_0  COME_FROM            20  '20'

 L. 163       222  LOAD_CONST               True
              224  LOAD_FAST                'self'
              226  STORE_ATTR               _is_processed

 L. 164       228  LOAD_FAST                'self'
              230  LOAD_ATTR                _writer
              232  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 38

    def __call__(self) -> Payload:
        if self._is_multipart:
            return self._gen_form_data()
        return self._gen_form_urlencoded()