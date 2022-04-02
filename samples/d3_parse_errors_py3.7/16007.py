# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\youtube_dl\extractor\cammodels.py
from __future__ import unicode_literals
from .common import InfoExtractor
from ..utils import ExtractorError, int_or_none, url_or_none

class CamModelsIE(InfoExtractor):
    _VALID_URL = 'https?://(?:www\\.)?cammodels\\.com/cam/(?P<id>[^/?#&]+)'
    _TESTS = [
     {'url':'https://www.cammodels.com/cam/AutumnKnight/', 
      'only_matching':True, 
      'age_limit':18}]

    def _real_extract--- This code section failed: ---

 L.  21         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _match_id
                4  LOAD_FAST                'url'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  STORE_FAST               'user_id'

 L.  23        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _download_webpage

 L.  24        14  LOAD_FAST                'url'
               16  LOAD_FAST                'user_id'
               18  LOAD_FAST                'self'
               20  LOAD_METHOD              geo_verification_headers
               22  CALL_METHOD_0         0  '0 positional arguments'
               24  LOAD_CONST               ('headers',)
               26  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               28  STORE_FAST               'webpage'

 L.  26        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _html_search_regex

 L.  27        34  LOAD_STR                 "manifestUrlRoot=([^&\\']+)"
               36  LOAD_FAST                'webpage'
               38  LOAD_STR                 'manifest'
               40  LOAD_CONST               None
               42  LOAD_CONST               ('default',)
               44  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               46  STORE_FAST               'manifest_root'

 L.  29        48  LOAD_FAST                'manifest_root'
               50  POP_JUMP_IF_TRUE    112  'to 112'

 L.  31        52  LOAD_CONST               (("I'm offline, but let's stay connected", 'This user is currently offline'), ('in a private show', 'This user is in a private show'), ('is currently performing LIVE', 'This model is currently performing live'))
               54  STORE_FAST               'ERRORS'

 L.  35        56  SETUP_LOOP          100  'to 100'
               58  LOAD_FAST                'ERRORS'
               60  GET_ITER         
             62_0  COME_FROM            88  '88'
             62_1  COME_FROM            76  '76'
               62  FOR_ITER             90  'to 90'
               64  UNPACK_SEQUENCE_2     2 
               66  STORE_FAST               'pattern'
               68  STORE_FAST               'message'

 L.  36        70  LOAD_FAST                'pattern'
               72  LOAD_FAST                'webpage'
               74  COMPARE_OP               in
               76  POP_JUMP_IF_FALSE_BACK    62  'to 62'

 L.  37        78  LOAD_FAST                'message'
               80  STORE_FAST               'error'

 L.  38        82  LOAD_CONST               True
               84  STORE_FAST               'expected'

 L.  39        86  BREAK_LOOP       
               88  JUMP_BACK            62  'to 62'
               90  POP_BLOCK        

 L.  41        92  LOAD_STR                 'Unable to find manifest URL root'
               94  STORE_FAST               'error'

 L.  42        96  LOAD_CONST               False
               98  STORE_FAST               'expected'
            100_0  COME_FROM_LOOP       56  '56'

 L.  43       100  LOAD_GLOBAL              ExtractorError
              102  LOAD_FAST                'error'
              104  LOAD_FAST                'expected'
              106  LOAD_CONST               ('expected',)
              108  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              110  RAISE_VARARGS_1       1  'exception instance'
            112_0  COME_FROM            50  '50'

 L.  45       112  LOAD_FAST                'self'
              114  LOAD_METHOD              _download_json

 L.  46       116  LOAD_STR                 '%s%s.json'
              118  LOAD_FAST                'manifest_root'
              120  LOAD_FAST                'user_id'
              122  BUILD_TUPLE_2         2 
              124  BINARY_MODULO    
              126  LOAD_FAST                'user_id'
              128  CALL_METHOD_2         2  '2 positional arguments'
              130  STORE_FAST               'manifest'

 L.  48       132  BUILD_LIST_0          0 
              134  STORE_FAST               'formats'

 L.  49   136_138  SETUP_LOOP          440  'to 440'
              140  LOAD_FAST                'manifest'
              142  LOAD_STR                 'formats'
              144  BINARY_SUBSCR    
              146  LOAD_METHOD              items
              148  CALL_METHOD_0         0  '0 positional arguments'
              150  GET_ITER         
            152_0  COME_FROM           436  '436'
            152_1  COME_FROM           194  '194'
            152_2  COME_FROM           172  '172'
          152_154  FOR_ITER            438  'to 438'
              156  UNPACK_SEQUENCE_2     2 
              158  STORE_FAST               'format_id'
              160  STORE_FAST               'format_dict'

 L.  50       162  LOAD_GLOBAL              isinstance
              164  LOAD_FAST                'format_dict'
              166  LOAD_GLOBAL              dict
              168  CALL_FUNCTION_2       2  '2 positional arguments'
              170  POP_JUMP_IF_TRUE    174  'to 174'

 L.  51       172  CONTINUE            152  'to 152'
            174_0  COME_FROM           170  '170'

 L.  52       174  LOAD_FAST                'format_dict'
              176  LOAD_METHOD              get
              178  LOAD_STR                 'encodings'
              180  CALL_METHOD_1         1  '1 positional argument'
              182  STORE_FAST               'encodings'

 L.  53       184  LOAD_GLOBAL              isinstance
              186  LOAD_FAST                'encodings'
              188  LOAD_GLOBAL              list
              190  CALL_FUNCTION_2       2  '2 positional arguments'
              192  POP_JUMP_IF_TRUE    196  'to 196'

 L.  54       194  CONTINUE            152  'to 152'
            196_0  COME_FROM           192  '192'

 L.  55       196  LOAD_FAST                'format_dict'
              198  LOAD_METHOD              get
              200  LOAD_STR                 'videoCodec'
              202  CALL_METHOD_1         1  '1 positional argument'
              204  STORE_FAST               'vcodec'

 L.  56       206  LOAD_FAST                'format_dict'
              208  LOAD_METHOD              get
              210  LOAD_STR                 'audioCodec'
              212  CALL_METHOD_1         1  '1 positional argument'
              214  STORE_FAST               'acodec'

 L.  57       216  SETUP_LOOP          436  'to 436'
              218  LOAD_FAST                'encodings'
              220  GET_ITER         
            222_0  COME_FROM           432  '432'
            222_1  COME_FROM           420  '420'
            222_2  COME_FROM           400  '400'
            222_3  COME_FROM           258  '258'
            222_4  COME_FROM           236  '236'
              222  FOR_ITER            434  'to 434'
              224  STORE_FAST               'media'

 L.  58       226  LOAD_GLOBAL              isinstance
              228  LOAD_FAST                'media'
              230  LOAD_GLOBAL              dict
              232  CALL_FUNCTION_2       2  '2 positional arguments'
              234  POP_JUMP_IF_TRUE    238  'to 238'

 L.  59       236  CONTINUE            222  'to 222'
            238_0  COME_FROM           234  '234'

 L.  60       238  LOAD_GLOBAL              url_or_none
              240  LOAD_FAST                'media'
              242  LOAD_METHOD              get
              244  LOAD_STR                 'location'
              246  CALL_METHOD_1         1  '1 positional argument'
              248  CALL_FUNCTION_1       1  '1 positional argument'
              250  STORE_FAST               'media_url'

 L.  61       252  LOAD_FAST                'media_url'
          254_256  POP_JUMP_IF_TRUE    260  'to 260'

 L.  62       258  CONTINUE            222  'to 222'
            260_0  COME_FROM           254  '254'

 L.  64       260  LOAD_FAST                'format_id'
              262  BUILD_LIST_1          1 
              264  STORE_FAST               'format_id_list'

 L.  65       266  LOAD_GLOBAL              int_or_none
              268  LOAD_FAST                'media'
              270  LOAD_METHOD              get
              272  LOAD_STR                 'videoHeight'
              274  CALL_METHOD_1         1  '1 positional argument'
              276  CALL_FUNCTION_1       1  '1 positional argument'
              278  STORE_FAST               'height'

 L.  66       280  LOAD_FAST                'height'
              282  LOAD_CONST               None
              284  COMPARE_OP               is-not
          286_288  POP_JUMP_IF_FALSE   304  'to 304'

 L.  67       290  LOAD_FAST                'format_id_list'
              292  LOAD_METHOD              append
              294  LOAD_STR                 '%dp'
              296  LOAD_FAST                'height'
              298  BINARY_MODULO    
              300  CALL_METHOD_1         1  '1 positional argument'
              302  POP_TOP          
            304_0  COME_FROM           286  '286'

 L.  69       304  LOAD_FAST                'media_url'

 L.  70       306  LOAD_STR                 '-'
              308  LOAD_METHOD              join
              310  LOAD_FAST                'format_id_list'
              312  CALL_METHOD_1         1  '1 positional argument'

 L.  71       314  LOAD_GLOBAL              int_or_none
              316  LOAD_FAST                'media'
              318  LOAD_METHOD              get
              320  LOAD_STR                 'videoWidth'
              322  CALL_METHOD_1         1  '1 positional argument'
              324  CALL_FUNCTION_1       1  '1 positional argument'

 L.  72       326  LOAD_FAST                'height'

 L.  73       328  LOAD_GLOBAL              int_or_none
              330  LOAD_FAST                'media'
              332  LOAD_METHOD              get
              334  LOAD_STR                 'videoKbps'
              336  CALL_METHOD_1         1  '1 positional argument'
              338  CALL_FUNCTION_1       1  '1 positional argument'

 L.  74       340  LOAD_GLOBAL              int_or_none
              342  LOAD_FAST                'media'
              344  LOAD_METHOD              get
              346  LOAD_STR                 'audioKbps'
              348  CALL_METHOD_1         1  '1 positional argument'
              350  CALL_FUNCTION_1       1  '1 positional argument'

 L.  75       352  LOAD_GLOBAL              int_or_none
              354  LOAD_FAST                'media'
              356  LOAD_METHOD              get
              358  LOAD_STR                 'fps'
              360  CALL_METHOD_1         1  '1 positional argument'
              362  CALL_FUNCTION_1       1  '1 positional argument'

 L.  76       364  LOAD_FAST                'vcodec'

 L.  77       366  LOAD_FAST                'acodec'
              368  LOAD_CONST               ('url', 'format_id', 'width', 'height', 'vbr', 'abr', 'fps', 'vcodec', 'acodec')
              370  BUILD_CONST_KEY_MAP_9     9 
              372  STORE_FAST               'f'

 L.  79       374  LOAD_STR                 'rtmp'
              376  LOAD_FAST                'format_id'
              378  COMPARE_OP               in
          380_382  POP_JUMP_IF_FALSE   394  'to 394'

 L.  80       384  LOAD_STR                 'flv'
              386  LOAD_FAST                'f'
              388  LOAD_STR                 'ext'
              390  STORE_SUBSCR     
              392  JUMP_FORWARD        422  'to 422'
            394_0  COME_FROM           380  '380'

 L.  81       394  LOAD_STR                 'hls'
              396  LOAD_FAST                'format_id'
              398  COMPARE_OP               in
              400  POP_JUMP_IF_FALSE_BACK   222  'to 222'

 L.  82       402  LOAD_FAST                'f'
              404  LOAD_METHOD              update

 L.  83       406  LOAD_STR                 'mp4'

 L.  85       408  LOAD_CONST               -1
              410  LOAD_CONST               ('ext', 'preference')
              412  BUILD_CONST_KEY_MAP_2     2 
              414  CALL_METHOD_1         1  '1 positional argument'
              416  POP_TOP          
              418  JUMP_FORWARD        422  'to 422'

 L.  88       420  CONTINUE            222  'to 222'
            422_0  COME_FROM           418  '418'
            422_1  COME_FROM           392  '392'

 L.  89       422  LOAD_FAST                'formats'
              424  LOAD_METHOD              append
              426  LOAD_FAST                'f'
              428  CALL_METHOD_1         1  '1 positional argument'
              430  POP_TOP          
              432  JUMP_BACK           222  'to 222'
              434  POP_BLOCK        
            436_0  COME_FROM_LOOP      216  '216'
              436  JUMP_BACK           152  'to 152'
              438  POP_BLOCK        
            440_0  COME_FROM_LOOP      136  '136'

 L.  90       440  LOAD_FAST                'self'
              442  LOAD_METHOD              _sort_formats
              444  LOAD_FAST                'formats'
              446  CALL_METHOD_1         1  '1 positional argument'
              448  POP_TOP          

 L.  93       450  LOAD_FAST                'user_id'

 L.  94       452  LOAD_FAST                'self'
              454  LOAD_METHOD              _live_title
              456  LOAD_FAST                'user_id'
              458  CALL_METHOD_1         1  '1 positional argument'

 L.  95       460  LOAD_CONST               True

 L.  96       462  LOAD_FAST                'formats'

 L.  97       464  LOAD_CONST               18
              466  LOAD_CONST               ('id', 'title', 'is_live', 'formats', 'age_limit')
              468  BUILD_CONST_KEY_MAP_5     5 
              470  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CONTINUE' instruction at offset 420