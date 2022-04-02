# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\openpyxl\reader\drawings.py
from __future__ import absolute_import
from io import BytesIO
from warnings import warn
from openpyxl.xml.functions import fromstring
from openpyxl.xml.constants import IMAGE_NS
from openpyxl.packaging.relationship import get_rel, get_rels_path, get_dependents
from openpyxl.drawing.spreadsheet_drawing import SpreadsheetDrawing
from openpyxl.drawing.image import Image, PILImage
from openpyxl.chart.chartspace import ChartSpace
from openpyxl.chart.reader import read_chart

def find_images--- This code section failed: ---

 L.  24         0  LOAD_FAST                'archive'
                2  LOAD_METHOD              read
                4  LOAD_FAST                'path'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'src'

 L.  25        10  LOAD_GLOBAL              fromstring
               12  LOAD_FAST                'src'
               14  CALL_FUNCTION_1       1  ''
               16  STORE_FAST               'tree'

 L.  26        18  SETUP_FINALLY        34  'to 34'

 L.  27        20  LOAD_GLOBAL              SpreadsheetDrawing
               22  LOAD_METHOD              from_tree
               24  LOAD_FAST                'tree'
               26  CALL_METHOD_1         1  ''
               28  STORE_FAST               'drawing'
               30  POP_BLOCK        
               32  JUMP_FORWARD         70  'to 70'
             34_0  COME_FROM_FINALLY    18  '18'

 L.  28        34  DUP_TOP          
               36  LOAD_GLOBAL              TypeError
               38  COMPARE_OP               exception-match
               40  POP_JUMP_IF_FALSE    68  'to 68'
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L.  29        48  LOAD_GLOBAL              warn
               50  LOAD_STR                 'DrawingML support is incomplete and limited to charts and images only. Shapes and drawings will be lost.'
               52  CALL_FUNCTION_1       1  ''
               54  POP_TOP          

 L.  30        56  BUILD_LIST_0          0 
               58  BUILD_LIST_0          0 
               60  BUILD_TUPLE_2         2 
               62  ROT_FOUR         
               64  POP_EXCEPT       
               66  RETURN_VALUE     
             68_0  COME_FROM            40  '40'
               68  END_FINALLY      
             70_0  COME_FROM            32  '32'

 L.  32        70  LOAD_GLOBAL              get_rels_path
               72  LOAD_FAST                'path'
               74  CALL_FUNCTION_1       1  ''
               76  STORE_FAST               'rels_path'

 L.  33        78  BUILD_LIST_0          0 
               80  STORE_FAST               'deps'

 L.  34        82  LOAD_FAST                'rels_path'
               84  LOAD_FAST                'archive'
               86  LOAD_METHOD              namelist
               88  CALL_METHOD_0         0  ''
               90  COMPARE_OP               in
               92  POP_JUMP_IF_FALSE   104  'to 104'

 L.  35        94  LOAD_GLOBAL              get_dependents
               96  LOAD_FAST                'archive'
               98  LOAD_FAST                'rels_path'
              100  CALL_FUNCTION_2       2  ''
              102  STORE_FAST               'deps'
            104_0  COME_FROM            92  '92'

 L.  37       104  BUILD_LIST_0          0 
              106  STORE_FAST               'charts'

 L.  38       108  LOAD_FAST                'drawing'
              110  LOAD_ATTR                _chart_rels
              112  GET_ITER         
              114  FOR_ITER            162  'to 162'
              116  STORE_FAST               'rel'

 L.  39       118  LOAD_GLOBAL              get_rel
              120  LOAD_FAST                'archive'
              122  LOAD_FAST                'deps'
              124  LOAD_FAST                'rel'
              126  LOAD_ATTR                id
              128  LOAD_GLOBAL              ChartSpace
              130  CALL_FUNCTION_4       4  ''
              132  STORE_FAST               'cs'

 L.  40       134  LOAD_GLOBAL              read_chart
              136  LOAD_FAST                'cs'
              138  CALL_FUNCTION_1       1  ''
              140  STORE_FAST               'chart'

 L.  41       142  LOAD_FAST                'rel'
              144  LOAD_ATTR                anchor
              146  LOAD_FAST                'chart'
              148  STORE_ATTR               anchor

 L.  42       150  LOAD_FAST                'charts'
              152  LOAD_METHOD              append
              154  LOAD_FAST                'chart'
              156  CALL_METHOD_1         1  ''
              158  POP_TOP          
              160  JUMP_BACK           114  'to 114'

 L.  44       162  BUILD_LIST_0          0 
              164  STORE_FAST               'images'

 L.  45       166  LOAD_GLOBAL              PILImage
              168  POP_JUMP_IF_TRUE    178  'to 178'

 L.  46       170  LOAD_FAST                'charts'
              172  LOAD_FAST                'images'
              174  BUILD_TUPLE_2         2 
              176  RETURN_VALUE     
            178_0  COME_FROM           168  '168'

 L.  48       178  LOAD_FAST                'drawing'
              180  LOAD_ATTR                _blip_rels
              182  GET_ITER         
            184_0  COME_FROM           206  '206'
              184  FOR_ITER            338  'to 338'
              186  STORE_FAST               'rel'

 L.  49       188  LOAD_FAST                'deps'
              190  LOAD_FAST                'rel'
              192  LOAD_ATTR                embed
              194  BINARY_SUBSCR    
              196  STORE_FAST               'dep'

 L.  50       198  LOAD_FAST                'dep'
              200  LOAD_ATTR                Type
              202  LOAD_GLOBAL              IMAGE_NS
              204  COMPARE_OP               ==
              206  POP_JUMP_IF_FALSE   184  'to 184'

 L.  51       208  SETUP_FINALLY       234  'to 234'

 L.  52       210  LOAD_GLOBAL              Image
              212  LOAD_GLOBAL              BytesIO
              214  LOAD_FAST                'archive'
              216  LOAD_METHOD              read
              218  LOAD_FAST                'dep'
              220  LOAD_ATTR                target
              222  CALL_METHOD_1         1  ''
              224  CALL_FUNCTION_1       1  ''
              226  CALL_FUNCTION_1       1  ''
              228  STORE_FAST               'image'
              230  POP_BLOCK        
              232  JUMP_FORWARD        280  'to 280'
            234_0  COME_FROM_FINALLY   208  '208'

 L.  53       234  DUP_TOP          
              236  LOAD_GLOBAL              OSError
              238  COMPARE_OP               exception-match
          240_242  POP_JUMP_IF_FALSE   278  'to 278'
              244  POP_TOP          
              246  POP_TOP          
              248  POP_TOP          

 L.  54       250  LOAD_STR                 'The image {0} will be removed because it cannot be read'
              252  LOAD_METHOD              format
              254  LOAD_FAST                'dep'
              256  LOAD_ATTR                target
              258  CALL_METHOD_1         1  ''
              260  STORE_FAST               'msg'

 L.  55       262  LOAD_GLOBAL              warn
              264  LOAD_FAST                'msg'
              266  CALL_FUNCTION_1       1  ''
              268  POP_TOP          

 L.  56       270  POP_EXCEPT       
              272  JUMP_BACK           184  'to 184'
              274  POP_EXCEPT       
              276  JUMP_FORWARD        280  'to 280'
            278_0  COME_FROM           240  '240'
              278  END_FINALLY      
            280_0  COME_FROM           276  '276'
            280_1  COME_FROM           232  '232'

 L.  57       280  LOAD_FAST                'image'
              282  LOAD_ATTR                format
              284  LOAD_METHOD              upper
              286  CALL_METHOD_0         0  ''
              288  LOAD_STR                 'WMF'
              290  COMPARE_OP               ==
          292_294  POP_JUMP_IF_FALSE   318  'to 318'

 L.  58       296  LOAD_STR                 '{0} image format is not supported so the image is being dropped'
              298  LOAD_METHOD              format
              300  LOAD_FAST                'image'
              302  LOAD_ATTR                format
              304  CALL_METHOD_1         1  ''
              306  STORE_FAST               'msg'

 L.  59       308  LOAD_GLOBAL              warn
              310  LOAD_FAST                'msg'
              312  CALL_FUNCTION_1       1  ''
              314  POP_TOP          

 L.  60       316  JUMP_BACK           184  'to 184'
            318_0  COME_FROM           292  '292'

 L.  61       318  LOAD_FAST                'rel'
              320  LOAD_ATTR                anchor
              322  LOAD_FAST                'image'
              324  STORE_ATTR               anchor

 L.  62       326  LOAD_FAST                'images'
              328  LOAD_METHOD              append
              330  LOAD_FAST                'image'
              332  CALL_METHOD_1         1  ''
              334  POP_TOP          
              336  JUMP_BACK           184  'to 184'

 L.  63       338  LOAD_FAST                'charts'
              340  LOAD_FAST                'images'
              342  BUILD_TUPLE_2         2 
              344  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 274