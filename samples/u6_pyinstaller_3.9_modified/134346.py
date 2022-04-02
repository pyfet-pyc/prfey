# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: aiohttp\web_fileresponse.py
import asyncio, mimetypes, os, pathlib, sys
from typing import IO, TYPE_CHECKING, Any, Awaitable, Callable, List, Optional, Union, cast
from . import hdrs
from .abc import AbstractStreamWriter
from .typedefs import LooseHeaders
from .web_exceptions import HTTPNotModified, HTTPPartialContent, HTTPPreconditionFailed, HTTPRequestRangeNotSatisfiable
from .web_response import StreamResponse
__all__ = ('FileResponse', )
if TYPE_CHECKING:
    from .web_request import BaseRequest
_T_OnChunkSent = Optional[Callable[([bytes], Awaitable[None])]]
NOSENDFILE = bool(os.environ.get('AIOHTTP_NOSENDFILE'))

class FileResponse(StreamResponse):
    __doc__ = 'A response object can be used to send files.'

    def __init__(self, path, chunk_size=262144, status=200, reason=None, headers=None):
        super().__init__(status=status, reason=reason, headers=headers)
        if isinstance(path, str):
            path = pathlib.Path(path)
        self._path = path
        self._chunk_size = chunk_size

    async def _sendfile_fallback(self, writer: AbstractStreamWriter, fobj: IO[Any], offset: int, count: int) -> AbstractStreamWriter:
        chunk_size = self._chunk_size
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, fobj.seek, offset)
        chunk = await loop.run_in_executor(None, fobj.read, chunk_size)
        while chunk:
            await writer.write(chunk)
            count = count - chunk_size
            if count <= 0:
                break
            chunk = await loop.run_in_executor(None, fobj.read, min(chunk_size, count))

        await writer.drain()
        return writer

    async def _sendfile--- This code section failed: ---

 L.  85         0  LOAD_GLOBAL              super
                2  CALL_FUNCTION_0       0  ''
                4  LOAD_METHOD              prepare
                6  LOAD_FAST                'request'
                8  CALL_METHOD_1         1  ''
               10  GET_AWAITABLE    
               12  LOAD_CONST               None
               14  YIELD_FROM       
               16  STORE_FAST               'writer'

 L.  86        18  LOAD_FAST                'writer'
               20  LOAD_CONST               None
               22  <117>                 1  ''
               24  POP_JUMP_IF_TRUE     30  'to 30'
               26  <74>             
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            24  '24'

 L.  88        30  LOAD_GLOBAL              NOSENDFILE
               32  POP_JUMP_IF_TRUE     50  'to 50'
               34  LOAD_GLOBAL              sys
               36  LOAD_ATTR                version_info
               38  LOAD_CONST               (3, 7)
               40  COMPARE_OP               <
               42  POP_JUMP_IF_TRUE     50  'to 50'
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                compression
               48  POP_JUMP_IF_FALSE    72  'to 72'
             50_0  COME_FROM            42  '42'
             50_1  COME_FROM            32  '32'

 L.  89        50  LOAD_FAST                'self'
               52  LOAD_METHOD              _sendfile_fallback
               54  LOAD_FAST                'writer'
               56  LOAD_FAST                'fobj'
               58  LOAD_FAST                'offset'
               60  LOAD_FAST                'count'
               62  CALL_METHOD_4         4  ''
               64  GET_AWAITABLE    
               66  LOAD_CONST               None
               68  YIELD_FROM       
               70  RETURN_VALUE     
             72_0  COME_FROM            48  '48'

 L.  91        72  LOAD_FAST                'request'
               74  LOAD_ATTR                _loop
               76  STORE_FAST               'loop'

 L.  92        78  LOAD_FAST                'request'
               80  LOAD_ATTR                transport
               82  STORE_FAST               'transport'

 L.  93        84  LOAD_FAST                'transport'
               86  LOAD_CONST               None
               88  <117>                 1  ''
               90  POP_JUMP_IF_TRUE     96  'to 96'
               92  <74>             
               94  RAISE_VARARGS_1       1  'exception instance'
             96_0  COME_FROM            90  '90'

 L.  95        96  SETUP_FINALLY       124  'to 124'

 L.  96        98  LOAD_FAST                'loop'
              100  LOAD_METHOD              sendfile
              102  LOAD_FAST                'transport'
              104  LOAD_FAST                'fobj'
              106  LOAD_FAST                'offset'
              108  LOAD_FAST                'count'
              110  CALL_METHOD_4         4  ''
              112  GET_AWAITABLE    
              114  LOAD_CONST               None
              116  YIELD_FROM       
              118  POP_TOP          
              120  POP_BLOCK        
              122  JUMP_FORWARD        164  'to 164'
            124_0  COME_FROM_FINALLY    96  '96'

 L.  97       124  DUP_TOP          
              126  LOAD_GLOBAL              NotImplementedError
              128  <121>               162  ''
              130  POP_TOP          
              132  POP_TOP          
              134  POP_TOP          

 L.  98       136  LOAD_FAST                'self'
              138  LOAD_METHOD              _sendfile_fallback
              140  LOAD_FAST                'writer'
              142  LOAD_FAST                'fobj'
              144  LOAD_FAST                'offset'
              146  LOAD_FAST                'count'
              148  CALL_METHOD_4         4  ''
              150  GET_AWAITABLE    
              152  LOAD_CONST               None
              154  YIELD_FROM       
              156  ROT_FOUR         
              158  POP_EXCEPT       
              160  RETURN_VALUE     
              162  <48>             
            164_0  COME_FROM           122  '122'

 L. 100       164  LOAD_GLOBAL              super
              166  CALL_FUNCTION_0       0  ''
              168  LOAD_METHOD              write_eof
              170  CALL_METHOD_0         0  ''
              172  GET_AWAITABLE    
              174  LOAD_CONST               None
              176  YIELD_FROM       
              178  POP_TOP          

 L. 101       180  LOAD_FAST                'writer'
              182  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 22

    async def prepare--- This code section failed: ---

 L. 104         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _path
                4  STORE_FAST               'filepath'

 L. 106         6  LOAD_CONST               False
                8  STORE_FAST               'gzip'

 L. 107        10  LOAD_STR                 'gzip'
               12  LOAD_FAST                'request'
               14  LOAD_ATTR                headers
               16  LOAD_METHOD              get
               18  LOAD_GLOBAL              hdrs
               20  LOAD_ATTR                ACCEPT_ENCODING
               22  LOAD_STR                 ''
               24  CALL_METHOD_2         2  ''
               26  <118>                 0  ''
               28  POP_JUMP_IF_FALSE    62  'to 62'

 L. 108        30  LOAD_FAST                'filepath'
               32  LOAD_METHOD              with_name
               34  LOAD_FAST                'filepath'
               36  LOAD_ATTR                name
               38  LOAD_STR                 '.gz'
               40  BINARY_ADD       
               42  CALL_METHOD_1         1  ''
               44  STORE_FAST               'gzip_path'

 L. 110        46  LOAD_FAST                'gzip_path'
               48  LOAD_METHOD              is_file
               50  CALL_METHOD_0         0  ''
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L. 111        54  LOAD_FAST                'gzip_path'
               56  STORE_FAST               'filepath'

 L. 112        58  LOAD_CONST               True
               60  STORE_FAST               'gzip'
             62_0  COME_FROM            52  '52'
             62_1  COME_FROM            28  '28'

 L. 114        62  LOAD_GLOBAL              asyncio
               64  LOAD_METHOD              get_event_loop
               66  CALL_METHOD_0         0  ''
               68  STORE_FAST               'loop'

 L. 115        70  LOAD_FAST                'loop'
               72  LOAD_METHOD              run_in_executor
               74  LOAD_CONST               None
               76  LOAD_FAST                'filepath'
               78  LOAD_ATTR                stat
               80  CALL_METHOD_2         2  ''
               82  GET_AWAITABLE    
               84  LOAD_CONST               None
               86  YIELD_FROM       
               88  STORE_FAST               'st'

 L. 117        90  LOAD_FAST                'request'
               92  LOAD_ATTR                if_modified_since
               94  STORE_FAST               'modsince'

 L. 118        96  LOAD_FAST                'modsince'
               98  LOAD_CONST               None
              100  <117>                 1  ''
              102  POP_JUMP_IF_FALSE   154  'to 154'
              104  LOAD_FAST                'st'
              106  LOAD_ATTR                st_mtime
              108  LOAD_FAST                'modsince'
              110  LOAD_METHOD              timestamp
              112  CALL_METHOD_0         0  ''
              114  COMPARE_OP               <=
              116  POP_JUMP_IF_FALSE   154  'to 154'

 L. 119       118  LOAD_FAST                'self'
              120  LOAD_METHOD              set_status
              122  LOAD_GLOBAL              HTTPNotModified
              124  LOAD_ATTR                status_code
              126  CALL_METHOD_1         1  ''
              128  POP_TOP          

 L. 120       130  LOAD_CONST               False
              132  LOAD_FAST                'self'
              134  STORE_ATTR               _length_check

 L. 123       136  LOAD_GLOBAL              super
              138  CALL_FUNCTION_0       0  ''
              140  LOAD_METHOD              prepare
              142  LOAD_FAST                'request'
              144  CALL_METHOD_1         1  ''
              146  GET_AWAITABLE    
              148  LOAD_CONST               None
              150  YIELD_FROM       
              152  RETURN_VALUE     
            154_0  COME_FROM           116  '116'
            154_1  COME_FROM           102  '102'

 L. 125       154  LOAD_FAST                'request'
              156  LOAD_ATTR                if_unmodified_since
              158  STORE_FAST               'unmodsince'

 L. 126       160  LOAD_FAST                'unmodsince'
              162  LOAD_CONST               None
              164  <117>                 1  ''
              166  POP_JUMP_IF_FALSE   212  'to 212'
              168  LOAD_FAST                'st'
              170  LOAD_ATTR                st_mtime
              172  LOAD_FAST                'unmodsince'
              174  LOAD_METHOD              timestamp
              176  CALL_METHOD_0         0  ''
              178  COMPARE_OP               >
              180  POP_JUMP_IF_FALSE   212  'to 212'

 L. 127       182  LOAD_FAST                'self'
              184  LOAD_METHOD              set_status
              186  LOAD_GLOBAL              HTTPPreconditionFailed
              188  LOAD_ATTR                status_code
              190  CALL_METHOD_1         1  ''
              192  POP_TOP          

 L. 128       194  LOAD_GLOBAL              super
              196  CALL_FUNCTION_0       0  ''
              198  LOAD_METHOD              prepare
              200  LOAD_FAST                'request'
              202  CALL_METHOD_1         1  ''
              204  GET_AWAITABLE    
              206  LOAD_CONST               None
              208  YIELD_FROM       
              210  RETURN_VALUE     
            212_0  COME_FROM           180  '180'
            212_1  COME_FROM           166  '166'

 L. 130       212  LOAD_GLOBAL              hdrs
              214  LOAD_ATTR                CONTENT_TYPE
              216  LOAD_FAST                'self'
              218  LOAD_ATTR                headers
              220  <118>                 1  ''
          222_224  POP_JUMP_IF_FALSE   258  'to 258'

 L. 131       226  LOAD_GLOBAL              mimetypes
              228  LOAD_METHOD              guess_type
              230  LOAD_GLOBAL              str
              232  LOAD_FAST                'filepath'
              234  CALL_FUNCTION_1       1  ''
              236  CALL_METHOD_1         1  ''
              238  UNPACK_SEQUENCE_2     2 
              240  STORE_FAST               'ct'
              242  STORE_FAST               'encoding'

 L. 132       244  LOAD_FAST                'ct'
              246  POP_JUMP_IF_TRUE    252  'to 252'

 L. 133       248  LOAD_STR                 'application/octet-stream'
              250  STORE_FAST               'ct'
            252_0  COME_FROM           246  '246'

 L. 134       252  LOAD_CONST               True
              254  STORE_FAST               'should_set_ct'
              256  JUMP_FORWARD        276  'to 276'
            258_0  COME_FROM           222  '222'

 L. 136       258  LOAD_FAST                'gzip'
          260_262  POP_JUMP_IF_FALSE   268  'to 268'
              264  LOAD_STR                 'gzip'
              266  JUMP_FORWARD        270  'to 270'
            268_0  COME_FROM           260  '260'
              268  LOAD_CONST               None
            270_0  COME_FROM           266  '266'
              270  STORE_FAST               'encoding'

 L. 137       272  LOAD_CONST               False
              274  STORE_FAST               'should_set_ct'
            276_0  COME_FROM           256  '256'

 L. 139       276  LOAD_FAST                'self'
              278  LOAD_ATTR                _status
              280  STORE_FAST               'status'

 L. 140       282  LOAD_FAST                'st'
              284  LOAD_ATTR                st_size
              286  STORE_FAST               'file_size'

 L. 141       288  LOAD_FAST                'file_size'
              290  STORE_FAST               'count'

 L. 143       292  LOAD_CONST               None
              294  STORE_FAST               'start'

 L. 145       296  LOAD_FAST                'request'
              298  LOAD_ATTR                if_range
              300  STORE_FAST               'ifrange'

 L. 146       302  LOAD_FAST                'ifrange'
              304  LOAD_CONST               None
              306  <117>                 0  ''
          308_310  POP_JUMP_IF_TRUE    328  'to 328'
              312  LOAD_FAST                'st'
              314  LOAD_ATTR                st_mtime
              316  LOAD_FAST                'ifrange'
              318  LOAD_METHOD              timestamp
              320  CALL_METHOD_0         0  ''
              322  COMPARE_OP               <=
          324_326  POP_JUMP_IF_FALSE   594  'to 594'
            328_0  COME_FROM           308  '308'

 L. 154       328  SETUP_FINALLY       352  'to 352'

 L. 155       330  LOAD_FAST                'request'
              332  LOAD_ATTR                http_range
              334  STORE_FAST               'rng'

 L. 156       336  LOAD_FAST                'rng'
              338  LOAD_ATTR                start
              340  STORE_FAST               'start'

 L. 157       342  LOAD_FAST                'rng'
              344  LOAD_ATTR                stop
              346  STORE_FAST               'end'
              348  POP_BLOCK        
              350  JUMP_FORWARD        420  'to 420'
            352_0  COME_FROM_FINALLY   328  '328'

 L. 158       352  DUP_TOP          
              354  LOAD_GLOBAL              ValueError
          356_358  <121>               418  ''
              360  POP_TOP          
              362  POP_TOP          
              364  POP_TOP          

 L. 168       366  LOAD_STR                 'bytes */'
              368  LOAD_FAST                'file_size'
              370  FORMAT_VALUE          0  ''
              372  BUILD_STRING_2        2 
              374  LOAD_FAST                'self'
              376  LOAD_ATTR                headers
              378  LOAD_GLOBAL              hdrs
              380  LOAD_ATTR                CONTENT_RANGE
              382  STORE_SUBSCR     

 L. 169       384  LOAD_FAST                'self'
              386  LOAD_METHOD              set_status
              388  LOAD_GLOBAL              HTTPRequestRangeNotSatisfiable
              390  LOAD_ATTR                status_code
              392  CALL_METHOD_1         1  ''
              394  POP_TOP          

 L. 170       396  LOAD_GLOBAL              super
              398  CALL_FUNCTION_0       0  ''
              400  LOAD_METHOD              prepare
              402  LOAD_FAST                'request'
              404  CALL_METHOD_1         1  ''
              406  GET_AWAITABLE    
              408  LOAD_CONST               None
              410  YIELD_FROM       
              412  ROT_FOUR         
              414  POP_EXCEPT       
              416  RETURN_VALUE     
              418  <48>             
            420_0  COME_FROM           350  '350'

 L. 174       420  LOAD_FAST                'start'
              422  LOAD_CONST               None
              424  <117>                 1  ''
          426_428  POP_JUMP_IF_TRUE    440  'to 440'
              430  LOAD_FAST                'end'
              432  LOAD_CONST               None
              434  <117>                 1  ''
          436_438  POP_JUMP_IF_FALSE   594  'to 594'
            440_0  COME_FROM           426  '426'

 L. 175       440  LOAD_FAST                'start'
              442  LOAD_CONST               0
              444  COMPARE_OP               <
          446_448  POP_JUMP_IF_FALSE   492  'to 492'
              450  LOAD_FAST                'end'
              452  LOAD_CONST               None
              454  <117>                 0  ''
          456_458  POP_JUMP_IF_FALSE   492  'to 492'

 L. 176       460  LOAD_FAST                'start'
              462  LOAD_FAST                'file_size'
              464  INPLACE_ADD      
              466  STORE_FAST               'start'

 L. 177       468  LOAD_FAST                'start'
              470  LOAD_CONST               0
              472  COMPARE_OP               <
          474_476  POP_JUMP_IF_FALSE   482  'to 482'

 L. 180       478  LOAD_CONST               0
              480  STORE_FAST               'start'
            482_0  COME_FROM           474  '474'

 L. 181       482  LOAD_FAST                'file_size'
              484  LOAD_FAST                'start'
              486  BINARY_SUBTRACT  
              488  STORE_FAST               'count'
              490  JUMP_FORWARD        520  'to 520'
            492_0  COME_FROM           456  '456'
            492_1  COME_FROM           446  '446'

 L. 191       492  LOAD_GLOBAL              min
              494  LOAD_FAST                'end'
              496  LOAD_CONST               None
              498  <117>                 1  ''
          500_502  POP_JUMP_IF_FALSE   508  'to 508'
              504  LOAD_FAST                'end'
              506  JUMP_FORWARD        510  'to 510'
            508_0  COME_FROM           500  '500'
              508  LOAD_FAST                'file_size'
            510_0  COME_FROM           506  '506'
              510  LOAD_FAST                'file_size'
              512  CALL_FUNCTION_2       2  ''
              514  LOAD_FAST                'start'
              516  BINARY_SUBTRACT  

 L. 190       518  STORE_FAST               'count'
            520_0  COME_FROM           490  '490'

 L. 194       520  LOAD_FAST                'start'
              522  LOAD_FAST                'file_size'
              524  COMPARE_OP               >=
          526_528  POP_JUMP_IF_FALSE   578  'to 578'

 L. 204       530  LOAD_STR                 'bytes */'
              532  LOAD_FAST                'file_size'
              534  FORMAT_VALUE          0  ''
              536  BUILD_STRING_2        2 
              538  LOAD_FAST                'self'
              540  LOAD_ATTR                headers
              542  LOAD_GLOBAL              hdrs
              544  LOAD_ATTR                CONTENT_RANGE
              546  STORE_SUBSCR     

 L. 205       548  LOAD_FAST                'self'
              550  LOAD_METHOD              set_status
              552  LOAD_GLOBAL              HTTPRequestRangeNotSatisfiable
              554  LOAD_ATTR                status_code
              556  CALL_METHOD_1         1  ''
              558  POP_TOP          

 L. 206       560  LOAD_GLOBAL              super
              562  CALL_FUNCTION_0       0  ''
              564  LOAD_METHOD              prepare
              566  LOAD_FAST                'request'
              568  CALL_METHOD_1         1  ''
              570  GET_AWAITABLE    
              572  LOAD_CONST               None
              574  YIELD_FROM       
              576  RETURN_VALUE     
            578_0  COME_FROM           526  '526'

 L. 208       578  LOAD_GLOBAL              HTTPPartialContent
              580  LOAD_ATTR                status_code
              582  STORE_FAST               'status'

 L. 211       584  LOAD_FAST                'self'
              586  LOAD_METHOD              set_status
              588  LOAD_FAST                'status'
              590  CALL_METHOD_1         1  ''
              592  POP_TOP          
            594_0  COME_FROM           436  '436'
            594_1  COME_FROM           324  '324'

 L. 213       594  LOAD_FAST                'should_set_ct'
          596_598  POP_JUMP_IF_FALSE   606  'to 606'

 L. 214       600  LOAD_FAST                'ct'
              602  LOAD_FAST                'self'
              604  STORE_ATTR               content_type
            606_0  COME_FROM           596  '596'

 L. 215       606  LOAD_FAST                'encoding'
          608_610  POP_JUMP_IF_FALSE   624  'to 624'

 L. 216       612  LOAD_FAST                'encoding'
              614  LOAD_FAST                'self'
              616  LOAD_ATTR                headers
              618  LOAD_GLOBAL              hdrs
              620  LOAD_ATTR                CONTENT_ENCODING
              622  STORE_SUBSCR     
            624_0  COME_FROM           608  '608'

 L. 217       624  LOAD_FAST                'gzip'
          626_628  POP_JUMP_IF_FALSE   644  'to 644'

 L. 218       630  LOAD_GLOBAL              hdrs
              632  LOAD_ATTR                ACCEPT_ENCODING
              634  LOAD_FAST                'self'
              636  LOAD_ATTR                headers
              638  LOAD_GLOBAL              hdrs
              640  LOAD_ATTR                VARY
              642  STORE_SUBSCR     
            644_0  COME_FROM           626  '626'

 L. 219       644  LOAD_FAST                'st'
              646  LOAD_ATTR                st_mtime
              648  LOAD_FAST                'self'
              650  STORE_ATTR               last_modified

 L. 220       652  LOAD_FAST                'count'
              654  LOAD_FAST                'self'
              656  STORE_ATTR               content_length

 L. 222       658  LOAD_STR                 'bytes'
              660  LOAD_FAST                'self'
              662  LOAD_ATTR                headers
              664  LOAD_GLOBAL              hdrs
              666  LOAD_ATTR                ACCEPT_RANGES
              668  STORE_SUBSCR     

 L. 224       670  LOAD_GLOBAL              cast
              672  LOAD_GLOBAL              int
              674  LOAD_FAST                'start'
              676  CALL_FUNCTION_2       2  ''
              678  STORE_FAST               'real_start'

 L. 226       680  LOAD_FAST                'status'
              682  LOAD_GLOBAL              HTTPPartialContent
              684  LOAD_ATTR                status_code
              686  COMPARE_OP               ==
          688_690  POP_JUMP_IF_FALSE   722  'to 722'

 L. 227       692  LOAD_STR                 'bytes {}-{}/{}'
              694  LOAD_METHOD              format

 L. 228       696  LOAD_FAST                'real_start'
              698  LOAD_FAST                'real_start'
              700  LOAD_FAST                'count'
              702  BINARY_ADD       
              704  LOAD_CONST               1
              706  BINARY_SUBTRACT  
              708  LOAD_FAST                'file_size'

 L. 227       710  CALL_METHOD_3         3  ''
              712  LOAD_FAST                'self'
              714  LOAD_ATTR                headers
              716  LOAD_GLOBAL              hdrs
              718  LOAD_ATTR                CONTENT_RANGE
              720  STORE_SUBSCR     
            722_0  COME_FROM           688  '688'

 L. 231       722  LOAD_FAST                'request'
              724  LOAD_ATTR                method
              726  LOAD_GLOBAL              hdrs
              728  LOAD_ATTR                METH_HEAD
              730  COMPARE_OP               ==
          732_734  POP_JUMP_IF_TRUE    748  'to 748'
              736  LOAD_FAST                'self'
              738  LOAD_ATTR                status
              740  LOAD_CONST               (204, 304)
              742  <118>                 0  ''
          744_746  POP_JUMP_IF_FALSE   766  'to 766'
            748_0  COME_FROM           732  '732'

 L. 232       748  LOAD_GLOBAL              super
              750  CALL_FUNCTION_0       0  ''
              752  LOAD_METHOD              prepare
              754  LOAD_FAST                'request'
              756  CALL_METHOD_1         1  ''
              758  GET_AWAITABLE    
              760  LOAD_CONST               None
              762  YIELD_FROM       
              764  RETURN_VALUE     
            766_0  COME_FROM           744  '744'

 L. 234       766  LOAD_FAST                'loop'
              768  LOAD_METHOD              run_in_executor
              770  LOAD_CONST               None
              772  LOAD_FAST                'filepath'
              774  LOAD_ATTR                open
              776  LOAD_STR                 'rb'
              778  CALL_METHOD_3         3  ''
              780  GET_AWAITABLE    
              782  LOAD_CONST               None
              784  YIELD_FROM       
              786  STORE_FAST               'fobj'

 L. 235       788  LOAD_FAST                'start'
          790_792  POP_JUMP_IF_FALSE   800  'to 800'

 L. 236       794  LOAD_FAST                'start'
              796  STORE_FAST               'offset'
              798  JUMP_FORWARD        804  'to 804'
            800_0  COME_FROM           790  '790'

 L. 238       800  LOAD_CONST               0
              802  STORE_FAST               'offset'
            804_0  COME_FROM           798  '798'

 L. 240       804  SETUP_FINALLY       850  'to 850'

 L. 241       806  LOAD_FAST                'self'
              808  LOAD_METHOD              _sendfile
              810  LOAD_FAST                'request'
              812  LOAD_FAST                'fobj'
              814  LOAD_FAST                'offset'
              816  LOAD_FAST                'count'
              818  CALL_METHOD_4         4  ''
              820  GET_AWAITABLE    
              822  LOAD_CONST               None
              824  YIELD_FROM       
              826  POP_BLOCK        

 L. 243       828  LOAD_FAST                'loop'
              830  LOAD_METHOD              run_in_executor
              832  LOAD_CONST               None
              834  LOAD_FAST                'fobj'
              836  LOAD_ATTR                close
              838  CALL_METHOD_2         2  ''
              840  GET_AWAITABLE    
              842  LOAD_CONST               None
              844  YIELD_FROM       
              846  POP_TOP          

 L. 241       848  RETURN_VALUE     
            850_0  COME_FROM_FINALLY   804  '804'

 L. 243       850  LOAD_FAST                'loop'
              852  LOAD_METHOD              run_in_executor
              854  LOAD_CONST               None
              856  LOAD_FAST                'fobj'
              858  LOAD_ATTR                close
              860  CALL_METHOD_2         2  ''
              862  GET_AWAITABLE    
              864  LOAD_CONST               None
              866  YIELD_FROM       
              868  POP_TOP          
              870  <48>             

Parse error at or near `<118>' instruction at offset 26