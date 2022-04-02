# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: gallery_dl\downloader\http.py
"""Downloader module for http:// and https:// URLs"""
import time, mimetypes
from requests.exceptions import RequestException, ConnectionError, Timeout
from .common import DownloaderBase
from .. import text, util
from ssl import SSLError
try:
    import OpenSSL.SSL as OpenSSLError
except ImportError:
    OpenSSLError = SSLError

class HttpDownloader(DownloaderBase):
    scheme = 'http'

    def __init__(self, job):
        DownloaderBase.__init__(self, job)
        extractor = job.extractor
        self.chunk_size = 16384
        self.downloading = False
        self.adjust_extension = self.config('adjust-extensions', True)
        self.minsize = self.config('filesize-min')
        self.maxsize = self.config('filesize-max')
        self.retries = self.config('retries', extractor._retries)
        self.timeout = self.config('timeout', extractor._timeout)
        self.verify = self.config('verify', extractor._verify)
        self.mtime = self.config('mtime', True)
        self.rate = self.config('rate')
        if self.retries < 0:
            self.retries = float('inf')
        else:
            if self.minsize:
                minsize = text.parse_bytes(self.minsize)
                if not minsize:
                    self.log.warning('Invalid minimum file size (%r)', self.minsize)
                self.minsize = minsize
            if self.maxsize:
                maxsize = text.parse_bytes(self.maxsize)
                if not maxsize:
                    self.log.warning('Invalid maximum file size (%r)', self.maxsize)
                self.maxsize = maxsize
            if self.rate:
                rate = text.parse_bytes(self.rate)
                if rate:
                    if rate < self.chunk_size:
                        self.chunk_size = rate
                    self.rate = rate
                    self.receive = self._receive_rate
                else:
                    self.log.warning('Invalid rate limit (%r)', self.rate)

    def download(self, url, pathfmt):
        try:
            try:
                return self._download_impl(url, pathfmt)
            except Exception:
                print()
                raise

        finally:
            if self.downloading:
                if not self.part:
                    util.remove_file(pathfmt.temppath)

    def _download_impl--- This code section failed: ---

 L.  78         0  LOAD_CONST               None
                2  STORE_FAST               'response'

 L.  79         4  LOAD_CONST               0
                6  STORE_FAST               'tries'

 L.  80         8  LOAD_STR                 ''
               10  STORE_FAST               'msg'

 L.  82        12  LOAD_FAST                'self'
               14  LOAD_ATTR                part
               16  POP_JUMP_IF_FALSE    30  'to 30'

 L.  83        18  LOAD_FAST                'pathfmt'
               20  LOAD_METHOD              part_enable
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                partdir
               26  CALL_METHOD_1         1  '1 positional argument'
               28  POP_TOP          
             30_0  COME_FROM            16  '16'

 L.  85     30_32  SETUP_LOOP         1062  'to 1062'
             34_0  COME_FROM           410  '410'

 L.  86        34  LOAD_FAST                'tries'
               36  POP_JUMP_IF_FALSE   102  'to 102'

 L.  87        38  LOAD_FAST                'response'
               40  POP_JUMP_IF_FALSE    54  'to 54'

 L.  88        42  LOAD_FAST                'response'
               44  LOAD_METHOD              close
               46  CALL_METHOD_0         0  '0 positional arguments'
               48  POP_TOP          

 L.  89        50  LOAD_CONST               None
               52  STORE_FAST               'response'
             54_0  COME_FROM            40  '40'

 L.  90        54  LOAD_FAST                'self'
               56  LOAD_ATTR                log
               58  LOAD_METHOD              warning
               60  LOAD_STR                 '%s (%s/%s)'
               62  LOAD_FAST                'msg'
               64  LOAD_FAST                'tries'
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                retries
               70  LOAD_CONST               1
               72  BINARY_ADD       
               74  CALL_METHOD_4         4  '4 positional arguments'
               76  POP_TOP          

 L.  91        78  LOAD_FAST                'tries'
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                retries
               84  COMPARE_OP               >
               86  POP_JUMP_IF_FALSE    92  'to 92'

 L.  92        88  LOAD_CONST               False
               90  RETURN_VALUE     
             92_0  COME_FROM            86  '86'

 L.  93        92  LOAD_GLOBAL              time
               94  LOAD_METHOD              sleep
               96  LOAD_FAST                'tries'
               98  CALL_METHOD_1         1  '1 positional argument'
              100  POP_TOP          
            102_0  COME_FROM            36  '36'

 L.  95       102  LOAD_FAST                'tries'
              104  LOAD_CONST               1
              106  INPLACE_ADD      
              108  STORE_FAST               'tries'

 L.  96       110  BUILD_MAP_0           0 
              112  STORE_FAST               'headers'

 L.  97       114  LOAD_CONST               None
              116  STORE_FAST               'file_header'

 L. 100       118  LOAD_FAST                'pathfmt'
              120  LOAD_METHOD              part_size
              122  CALL_METHOD_0         0  '0 positional arguments'
              124  STORE_FAST               'file_size'

 L. 101       126  LOAD_FAST                'file_size'
              128  POP_JUMP_IF_FALSE   144  'to 144'

 L. 102       130  LOAD_STR                 'bytes={}-'
              132  LOAD_METHOD              format
              134  LOAD_FAST                'file_size'
              136  CALL_METHOD_1         1  '1 positional argument'
              138  LOAD_FAST                'headers'
              140  LOAD_STR                 'Range'
              142  STORE_SUBSCR     
            144_0  COME_FROM           128  '128'

 L. 104       144  LOAD_FAST                'pathfmt'
              146  LOAD_ATTR                kwdict
              148  LOAD_METHOD              get
              150  LOAD_STR                 '_http_headers'
              152  CALL_METHOD_1         1  '1 positional argument'
              154  STORE_FAST               'extra'

 L. 105       156  LOAD_FAST                'extra'
              158  POP_JUMP_IF_FALSE   170  'to 170'

 L. 106       160  LOAD_FAST                'headers'
              162  LOAD_METHOD              update
              164  LOAD_FAST                'extra'
              166  CALL_METHOD_1         1  '1 positional argument'
              168  POP_TOP          
            170_0  COME_FROM           158  '158'

 L. 109       170  SETUP_EXCEPT        204  'to 204'

 L. 110       172  LOAD_FAST                'self'
              174  LOAD_ATTR                session
              176  LOAD_ATTR                request

 L. 111       178  LOAD_STR                 'GET'
              180  LOAD_FAST                'url'
              182  LOAD_CONST               True
              184  LOAD_FAST                'headers'

 L. 112       186  LOAD_FAST                'self'
              188  LOAD_ATTR                timeout
              190  LOAD_FAST                'self'
              192  LOAD_ATTR                verify
              194  LOAD_CONST               ('stream', 'headers', 'timeout', 'verify')
              196  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              198  STORE_FAST               'response'
              200  POP_BLOCK        
              202  JUMP_FORWARD        298  'to 298'
            204_0  COME_FROM_EXCEPT    170  '170'

 L. 113       204  DUP_TOP          
              206  LOAD_GLOBAL              ConnectionError
              208  LOAD_GLOBAL              Timeout
              210  BUILD_TUPLE_2         2 
              212  COMPARE_OP               exception-match
              214  POP_JUMP_IF_FALSE   250  'to 250'
              216  POP_TOP          
              218  STORE_FAST               'exc'
              220  POP_TOP          
              222  SETUP_FINALLY       238  'to 238'

 L. 114       224  LOAD_GLOBAL              str
              226  LOAD_FAST                'exc'
              228  CALL_FUNCTION_1       1  '1 positional argument'
              230  STORE_FAST               'msg'

 L. 115       232  CONTINUE_LOOP        34  'to 34'
              234  POP_BLOCK        
              236  LOAD_CONST               None
            238_0  COME_FROM_FINALLY   222  '222'
              238  LOAD_CONST               None
              240  STORE_FAST               'exc'
              242  DELETE_FAST              'exc'
              244  END_FINALLY      
              246  POP_EXCEPT       
              248  JUMP_FORWARD        298  'to 298'
            250_0  COME_FROM           214  '214'

 L. 116       250  DUP_TOP          
              252  LOAD_GLOBAL              Exception
              254  COMPARE_OP               exception-match
          256_258  POP_JUMP_IF_FALSE   296  'to 296'
              260  POP_TOP          
              262  STORE_FAST               'exc'
              264  POP_TOP          
              266  SETUP_FINALLY       284  'to 284'

 L. 117       268  LOAD_FAST                'self'
              270  LOAD_ATTR                log
              272  LOAD_METHOD              warning
              274  LOAD_FAST                'exc'
              276  CALL_METHOD_1         1  '1 positional argument'
              278  POP_TOP          

 L. 118       280  LOAD_CONST               False
              282  RETURN_VALUE     
            284_0  COME_FROM_FINALLY   266  '266'
              284  LOAD_CONST               None
              286  STORE_FAST               'exc'
              288  DELETE_FAST              'exc'
              290  END_FINALLY      
              292  POP_EXCEPT       
              294  JUMP_FORWARD        298  'to 298'
            296_0  COME_FROM           256  '256'
              296  END_FINALLY      
            298_0  COME_FROM           294  '294'
            298_1  COME_FROM           248  '248'
            298_2  COME_FROM           202  '202'

 L. 121       298  LOAD_FAST                'response'
              300  LOAD_ATTR                status_code
              302  STORE_FAST               'code'

 L. 122       304  LOAD_FAST                'code'
              306  LOAD_CONST               200
              308  COMPARE_OP               ==
          310_312  POP_JUMP_IF_FALSE   332  'to 332'

 L. 123       314  LOAD_CONST               0
              316  STORE_FAST               'offset'

 L. 124       318  LOAD_FAST                'response'
              320  LOAD_ATTR                headers
              322  LOAD_METHOD              get
              324  LOAD_STR                 'Content-Length'
              326  CALL_METHOD_1         1  '1 positional argument'
              328  STORE_FAST               'size'
              330  JUMP_FORWARD        458  'to 458'
            332_0  COME_FROM           310  '310'

 L. 125       332  LOAD_FAST                'code'
              334  LOAD_CONST               206
              336  COMPARE_OP               ==
          338_340  POP_JUMP_IF_FALSE   368  'to 368'

 L. 126       342  LOAD_FAST                'file_size'
              344  STORE_FAST               'offset'

 L. 127       346  LOAD_FAST                'response'
              348  LOAD_ATTR                headers
              350  LOAD_STR                 'Content-Range'
              352  BINARY_SUBSCR    
              354  LOAD_METHOD              rpartition
              356  LOAD_STR                 '/'
              358  CALL_METHOD_1         1  '1 positional argument'
              360  LOAD_CONST               2
              362  BINARY_SUBSCR    
              364  STORE_FAST               'size'
              366  JUMP_FORWARD        458  'to 458'
            368_0  COME_FROM           338  '338'

 L. 128       368  LOAD_FAST                'code'
              370  LOAD_CONST               416
              372  COMPARE_OP               ==
          374_376  POP_JUMP_IF_FALSE   388  'to 388'
              378  LOAD_FAST                'file_size'
          380_382  POP_JUMP_IF_FALSE   388  'to 388'

 L. 129       384  BREAK_LOOP       
              386  JUMP_FORWARD        458  'to 458'
            388_0  COME_FROM           380  '380'
            388_1  COME_FROM           374  '374'

 L. 131       388  LOAD_STR                 "'{} {}' for '{}'"
              390  LOAD_METHOD              format
              392  LOAD_FAST                'code'
              394  LOAD_FAST                'response'
              396  LOAD_ATTR                reason
              398  LOAD_FAST                'url'
              400  CALL_METHOD_3         3  '3 positional arguments'
              402  STORE_FAST               'msg'

 L. 132       404  LOAD_FAST                'code'
              406  LOAD_CONST               429
              408  COMPARE_OP               ==
              410  POP_JUMP_IF_TRUE     34  'to 34'
              412  LOAD_CONST               500
              414  LOAD_FAST                'code'
              416  DUP_TOP          
              418  ROT_THREE        
              420  COMPARE_OP               <=
          422_424  POP_JUMP_IF_FALSE   436  'to 436'
              426  LOAD_CONST               600
              428  COMPARE_OP               <
          430_432  POP_JUMP_IF_FALSE   442  'to 442'
              434  JUMP_BACK            34  'to 34'
            436_0  COME_FROM           422  '422'
              436  POP_TOP          
              438  JUMP_FORWARD        442  'to 442'

 L. 133       440  CONTINUE             34  'to 34'
            442_0  COME_FROM           438  '438'
            442_1  COME_FROM           430  '430'

 L. 134       442  LOAD_FAST                'self'
              444  LOAD_ATTR                log
              446  LOAD_METHOD              warning
              448  LOAD_FAST                'msg'
              450  CALL_METHOD_1         1  '1 positional argument'
              452  POP_TOP          

 L. 135       454  LOAD_CONST               False
              456  RETURN_VALUE     
            458_0  COME_FROM           386  '386'
            458_1  COME_FROM           366  '366'
            458_2  COME_FROM           330  '330'

 L. 138       458  LOAD_FAST                'pathfmt'
              460  LOAD_ATTR                extension
          462_464  POP_JUMP_IF_TRUE    502  'to 502'

 L. 139       466  LOAD_FAST                'pathfmt'
              468  LOAD_METHOD              set_extension
              470  LOAD_FAST                'self'
              472  LOAD_METHOD              _find_extension
              474  LOAD_FAST                'response'
              476  CALL_METHOD_1         1  '1 positional argument'
              478  CALL_METHOD_1         1  '1 positional argument'
              480  POP_TOP          

 L. 140       482  LOAD_FAST                'pathfmt'
              484  LOAD_METHOD              exists
              486  CALL_METHOD_0         0  '0 positional arguments'
          488_490  POP_JUMP_IF_FALSE   502  'to 502'

 L. 141       492  LOAD_STR                 ''
              494  LOAD_FAST                'pathfmt'
              496  STORE_ATTR               temppath

 L. 142       498  LOAD_CONST               True
              500  RETURN_VALUE     
            502_0  COME_FROM           488  '488'
            502_1  COME_FROM           462  '462'

 L. 145       502  LOAD_GLOBAL              text
              504  LOAD_METHOD              parse_int
              506  LOAD_FAST                'size'
              508  LOAD_CONST               None
              510  CALL_METHOD_2         2  '2 positional arguments'
              512  STORE_FAST               'size'

 L. 146       514  LOAD_FAST                'size'
              516  LOAD_CONST               None
              518  COMPARE_OP               is-not
          520_522  POP_JUMP_IF_FALSE   608  'to 608'

 L. 147       524  LOAD_FAST                'self'
              526  LOAD_ATTR                minsize
          528_530  POP_JUMP_IF_FALSE   566  'to 566'
              532  LOAD_FAST                'size'
              534  LOAD_FAST                'self'
              536  LOAD_ATTR                minsize
              538  COMPARE_OP               <
          540_542  POP_JUMP_IF_FALSE   566  'to 566'

 L. 148       544  LOAD_FAST                'self'
              546  LOAD_ATTR                log
              548  LOAD_METHOD              warning

 L. 149       550  LOAD_STR                 'File size smaller than allowed minimum (%s < %s)'

 L. 150       552  LOAD_FAST                'size'
              554  LOAD_FAST                'self'
              556  LOAD_ATTR                minsize
              558  CALL_METHOD_3         3  '3 positional arguments'
              560  POP_TOP          

 L. 151       562  LOAD_CONST               False
              564  RETURN_VALUE     
            566_0  COME_FROM           540  '540'
            566_1  COME_FROM           528  '528'

 L. 152       566  LOAD_FAST                'self'
              568  LOAD_ATTR                maxsize
          570_572  POP_JUMP_IF_FALSE   608  'to 608'
              574  LOAD_FAST                'size'
              576  LOAD_FAST                'self'
              578  LOAD_ATTR                maxsize
              580  COMPARE_OP               >
          582_584  POP_JUMP_IF_FALSE   608  'to 608'

 L. 153       586  LOAD_FAST                'self'
              588  LOAD_ATTR                log
              590  LOAD_METHOD              warning

 L. 154       592  LOAD_STR                 'File size larger than allowed maximum (%s > %s)'

 L. 155       594  LOAD_FAST                'size'
              596  LOAD_FAST                'self'
              598  LOAD_ATTR                maxsize
              600  CALL_METHOD_3         3  '3 positional arguments'
              602  POP_TOP          

 L. 156       604  LOAD_CONST               False
              606  RETURN_VALUE     
            608_0  COME_FROM           582  '582'
            608_1  COME_FROM           570  '570'
            608_2  COME_FROM           520  '520'

 L. 158       608  LOAD_FAST                'response'
              610  LOAD_METHOD              iter_content
              612  LOAD_FAST                'self'
              614  LOAD_ATTR                chunk_size
              616  CALL_METHOD_1         1  '1 positional argument'
              618  STORE_FAST               'content'

 L. 161       620  LOAD_FAST                'self'
              622  LOAD_ATTR                adjust_extension
          624_626  POP_JUMP_IF_FALSE   774  'to 774'
              628  LOAD_FAST                'offset'
          630_632  POP_JUMP_IF_TRUE    774  'to 774'

 L. 162       634  LOAD_FAST                'pathfmt'
              636  LOAD_ATTR                extension
              638  LOAD_GLOBAL              FILE_SIGNATURES
              640  COMPARE_OP               in
          642_644  POP_JUMP_IF_FALSE   774  'to 774'

 L. 163       646  SETUP_EXCEPT        682  'to 682'

 L. 164       648  LOAD_GLOBAL              next

 L. 165       650  LOAD_FAST                'response'
              652  LOAD_ATTR                raw
              654  LOAD_ATTR                chunked
          656_658  POP_JUMP_IF_FALSE   664  'to 664'
              660  LOAD_FAST                'content'
              662  JUMP_FORWARD        672  'to 672'
            664_0  COME_FROM           656  '656'

 L. 166       664  LOAD_FAST                'response'
              666  LOAD_METHOD              iter_content
              668  LOAD_CONST               16
              670  CALL_METHOD_1         1  '1 positional argument'
            672_0  COME_FROM           662  '662'
              672  LOAD_CONST               b''
              674  CALL_FUNCTION_2       2  '2 positional arguments'
              676  STORE_FAST               'file_header'
              678  POP_BLOCK        
              680  JUMP_FORWARD        740  'to 740'
            682_0  COME_FROM_EXCEPT    646  '646'

 L. 167       682  DUP_TOP          
              684  LOAD_GLOBAL              RequestException
              686  LOAD_GLOBAL              SSLError
              688  LOAD_GLOBAL              OpenSSLError
              690  BUILD_TUPLE_3         3 
              692  COMPARE_OP               exception-match
          694_696  POP_JUMP_IF_FALSE   738  'to 738'
              698  POP_TOP          
              700  STORE_FAST               'exc'
              702  POP_TOP          
              704  SETUP_FINALLY       726  'to 726'

 L. 168       706  LOAD_GLOBAL              str
              708  LOAD_FAST                'exc'
              710  CALL_FUNCTION_1       1  '1 positional argument'
              712  STORE_FAST               'msg'

 L. 169       714  LOAD_GLOBAL              print
              716  CALL_FUNCTION_0       0  '0 positional arguments'
              718  POP_TOP          

 L. 170       720  CONTINUE_LOOP        34  'to 34'
              722  POP_BLOCK        
              724  LOAD_CONST               None
            726_0  COME_FROM_FINALLY   704  '704'
              726  LOAD_CONST               None
              728  STORE_FAST               'exc'
              730  DELETE_FAST              'exc'
              732  END_FINALLY      
              734  POP_EXCEPT       
              736  JUMP_FORWARD        740  'to 740'
            738_0  COME_FROM           694  '694'
              738  END_FINALLY      
            740_0  COME_FROM           736  '736'
            740_1  COME_FROM           680  '680'

 L. 171       740  LOAD_FAST                'self'
              742  LOAD_METHOD              _adjust_extension
              744  LOAD_FAST                'pathfmt'
              746  LOAD_FAST                'file_header'
              748  CALL_METHOD_2         2  '2 positional arguments'
          750_752  POP_JUMP_IF_FALSE   774  'to 774'

 L. 172       754  LOAD_FAST                'pathfmt'
              756  LOAD_METHOD              exists
              758  CALL_METHOD_0         0  '0 positional arguments'
          760_762  POP_JUMP_IF_FALSE   774  'to 774'

 L. 173       764  LOAD_STR                 ''
              766  LOAD_FAST                'pathfmt'
              768  STORE_ATTR               temppath

 L. 174       770  LOAD_CONST               True
              772  RETURN_VALUE     
            774_0  COME_FROM           760  '760'
            774_1  COME_FROM           750  '750'
            774_2  COME_FROM           642  '642'
            774_3  COME_FROM           630  '630'
            774_4  COME_FROM           624  '624'

 L. 177       774  LOAD_FAST                'offset'
          776_778  POP_JUMP_IF_TRUE    804  'to 804'

 L. 178       780  LOAD_STR                 'w+b'
              782  STORE_FAST               'mode'

 L. 179       784  LOAD_FAST                'file_size'
          786_788  POP_JUMP_IF_FALSE   822  'to 822'

 L. 180       790  LOAD_FAST                'self'
              792  LOAD_ATTR                log
              794  LOAD_METHOD              debug
              796  LOAD_STR                 'Unable to resume partial download'
              798  CALL_METHOD_1         1  '1 positional argument'
              800  POP_TOP          
              802  JUMP_FORWARD        822  'to 822'
            804_0  COME_FROM           776  '776'

 L. 182       804  LOAD_STR                 'r+b'
              806  STORE_FAST               'mode'

 L. 183       808  LOAD_FAST                'self'
              810  LOAD_ATTR                log
              812  LOAD_METHOD              debug
              814  LOAD_STR                 'Resuming download at byte %d'
              816  LOAD_FAST                'offset'
              818  CALL_METHOD_2         2  '2 positional arguments'
              820  POP_TOP          
            822_0  COME_FROM           802  '802'
            822_1  COME_FROM           786  '786'

 L. 186       822  LOAD_CONST               True
              824  LOAD_FAST                'self'
              826  STORE_ATTR               downloading

 L. 187       828  LOAD_FAST                'pathfmt'
              830  LOAD_METHOD              open
              832  LOAD_FAST                'mode'
              834  CALL_METHOD_1         1  '1 positional argument'
              836  SETUP_WITH         1050  'to 1050'
              838  STORE_FAST               'fp'

 L. 188       840  LOAD_FAST                'file_header'
          842_844  POP_JUMP_IF_FALSE   858  'to 858'

 L. 189       846  LOAD_FAST                'fp'
              848  LOAD_METHOD              write
              850  LOAD_FAST                'file_header'
              852  CALL_METHOD_1         1  '1 positional argument'
              854  POP_TOP          
              856  JUMP_FORWARD        912  'to 912'
            858_0  COME_FROM           842  '842'

 L. 190       858  LOAD_FAST                'offset'
          860_862  POP_JUMP_IF_FALSE   912  'to 912'

 L. 191       864  LOAD_FAST                'self'
              866  LOAD_ATTR                adjust_extension
          868_870  POP_JUMP_IF_FALSE   902  'to 902'

 L. 192       872  LOAD_FAST                'pathfmt'
              874  LOAD_ATTR                extension
              876  LOAD_GLOBAL              FILE_SIGNATURES
              878  COMPARE_OP               in
          880_882  POP_JUMP_IF_FALSE   902  'to 902'

 L. 193       884  LOAD_FAST                'self'
              886  LOAD_METHOD              _adjust_extension
              888  LOAD_FAST                'pathfmt'
              890  LOAD_FAST                'fp'
              892  LOAD_METHOD              read
              894  LOAD_CONST               16
              896  CALL_METHOD_1         1  '1 positional argument'
              898  CALL_METHOD_2         2  '2 positional arguments'
              900  POP_TOP          
            902_0  COME_FROM           880  '880'
            902_1  COME_FROM           868  '868'

 L. 194       902  LOAD_FAST                'fp'
              904  LOAD_METHOD              seek
              906  LOAD_FAST                'offset'
              908  CALL_METHOD_1         1  '1 positional argument'
              910  POP_TOP          
            912_0  COME_FROM           860  '860'
            912_1  COME_FROM           856  '856'

 L. 196       912  LOAD_FAST                'self'
              914  LOAD_ATTR                out
              916  LOAD_METHOD              start
              918  LOAD_FAST                'pathfmt'
              920  LOAD_ATTR                path
              922  CALL_METHOD_1         1  '1 positional argument'
              924  POP_TOP          

 L. 197       926  SETUP_EXCEPT        944  'to 944'

 L. 198       928  LOAD_FAST                'self'
              930  LOAD_METHOD              receive
              932  LOAD_FAST                'fp'
              934  LOAD_FAST                'content'
              936  CALL_METHOD_2         2  '2 positional arguments'
              938  POP_TOP          
              940  POP_BLOCK        
              942  JUMP_FORWARD       1002  'to 1002'
            944_0  COME_FROM_EXCEPT    926  '926'

 L. 199       944  DUP_TOP          
              946  LOAD_GLOBAL              RequestException
              948  LOAD_GLOBAL              SSLError
              950  LOAD_GLOBAL              OpenSSLError
              952  BUILD_TUPLE_3         3 
              954  COMPARE_OP               exception-match
          956_958  POP_JUMP_IF_FALSE  1000  'to 1000'
              960  POP_TOP          
              962  STORE_FAST               'exc'
              964  POP_TOP          
              966  SETUP_FINALLY       988  'to 988'

 L. 200       968  LOAD_GLOBAL              str
              970  LOAD_FAST                'exc'
              972  CALL_FUNCTION_1       1  '1 positional argument'
              974  STORE_FAST               'msg'

 L. 201       976  LOAD_GLOBAL              print
              978  CALL_FUNCTION_0       0  '0 positional arguments'
              980  POP_TOP          

 L. 202       982  CONTINUE_LOOP        34  'to 34'
              984  POP_BLOCK        
              986  LOAD_CONST               None
            988_0  COME_FROM_FINALLY   966  '966'
              988  LOAD_CONST               None
              990  STORE_FAST               'exc'
              992  DELETE_FAST              'exc'
              994  END_FINALLY      
              996  POP_EXCEPT       
              998  JUMP_FORWARD       1002  'to 1002'
           1000_0  COME_FROM           956  '956'
             1000  END_FINALLY      
           1002_0  COME_FROM           998  '998'
           1002_1  COME_FROM           942  '942'

 L. 205      1002  LOAD_FAST                'size'
         1004_1006  POP_JUMP_IF_FALSE  1046  'to 1046'
             1008  LOAD_FAST                'fp'
             1010  LOAD_METHOD              tell
             1012  CALL_METHOD_0         0  '0 positional arguments'
             1014  LOAD_FAST                'size'
             1016  COMPARE_OP               <
         1018_1020  POP_JUMP_IF_FALSE  1046  'to 1046'

 L. 206      1022  LOAD_STR                 'file size mismatch ({} < {})'
             1024  LOAD_METHOD              format

 L. 207      1026  LOAD_FAST                'fp'
             1028  LOAD_METHOD              tell
             1030  CALL_METHOD_0         0  '0 positional arguments'
             1032  LOAD_FAST                'size'
             1034  CALL_METHOD_2         2  '2 positional arguments'
             1036  STORE_FAST               'msg'

 L. 208      1038  LOAD_GLOBAL              print
             1040  CALL_FUNCTION_0       0  '0 positional arguments'
             1042  POP_TOP          

 L. 209      1044  CONTINUE_LOOP        34  'to 34'
           1046_0  COME_FROM          1018  '1018'
           1046_1  COME_FROM          1004  '1004'
             1046  POP_BLOCK        
             1048  LOAD_CONST               None
           1050_0  COME_FROM_WITH      836  '836'
             1050  WITH_CLEANUP_START
             1052  WITH_CLEANUP_FINISH
             1054  END_FINALLY      

 L. 211      1056  BREAK_LOOP       
             1058  JUMP_BACK            34  'to 34'
             1060  POP_BLOCK        
           1062_0  COME_FROM_LOOP       30  '30'

 L. 213      1062  LOAD_CONST               False
             1064  LOAD_FAST                'self'
             1066  STORE_ATTR               downloading

 L. 214      1068  LOAD_FAST                'self'
             1070  LOAD_ATTR                mtime
         1072_1074  POP_JUMP_IF_FALSE  1100  'to 1100'

 L. 215      1076  LOAD_FAST                'pathfmt'
             1078  LOAD_ATTR                kwdict
             1080  LOAD_METHOD              setdefault

 L. 216      1082  LOAD_STR                 '_mtime'
             1084  LOAD_FAST                'response'
             1086  LOAD_ATTR                headers
             1088  LOAD_METHOD              get
             1090  LOAD_STR                 'Last-Modified'
             1092  CALL_METHOD_1         1  '1 positional argument'
             1094  CALL_METHOD_2         2  '2 positional arguments'
             1096  POP_TOP          
             1098  JUMP_FORWARD       1110  'to 1110'
           1100_0  COME_FROM          1072  '1072'

 L. 218      1100  LOAD_CONST               None
             1102  LOAD_FAST                'pathfmt'
             1104  LOAD_ATTR                kwdict
             1106  LOAD_STR                 '_mtime'
             1108  STORE_SUBSCR     
           1110_0  COME_FROM          1098  '1098'

 L. 220      1110  LOAD_CONST               True
             1112  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 436

    @staticmethod
    def receive(fp, content):
        write = fp.write
        for data in content:
            write(data)

    def _receive_rate(self, fp, content):
        rt = self.rate
        t1 = time.time
        for data in content:
            fp.write(data)
            t2 = time.time
            actual = t2 - t1
            expected = len(data) / rt
            if actual < expected:
                time.sleep(expected - actual)
                t1 = time.time
            else:
                t1 = t2

    def _find_extension(self, response):
        """Get filename extension from MIME type"""
        mtype = response.headers.get('Content-Type', 'image/jpeg')
        mtype = mtype.partition(';')[0]
        if '/' not in mtype:
            mtype = 'image/' + mtype
        if mtype in MIME_TYPES:
            return MIME_TYPES[mtype]
        ext = mimetypes.guess_extension(mtype, strict=False)
        if ext:
            return ext[1:]
        self.log.warning("Unknown MIME type '%s'", mtype)
        return 'bin'

    @staticmethod
    def _adjust_extension(pathfmt, file_header):
        """Check filename extension against file header"""
        sig = FILE_SIGNATURES[pathfmt.extension]
        if not file_header.startswith(sig):
            for ext, sig in FILE_SIGNATURES.items:
                if file_header.startswith(sig):
                    pathfmt.set_extension(ext)
                    return True

        return False


MIME_TYPES = {'image/jpeg':'jpg', 
 'image/jpg':'jpg', 
 'image/png':'png', 
 'image/gif':'gif', 
 'image/bmp':'bmp', 
 'image/x-bmp':'bmp', 
 'image/x-ms-bmp':'bmp', 
 'image/webp':'webp', 
 'image/svg+xml':'svg', 
 'image/ico':'ico', 
 'image/icon':'ico', 
 'image/x-icon':'ico', 
 'image/vnd.microsoft.icon':'ico', 
 'image/x-photoshop':'psd', 
 'application/x-photoshop':'psd', 
 'image/vnd.adobe.photoshop':'psd', 
 'video/webm':'webm', 
 'video/ogg':'ogg', 
 'video/mp4':'mp4', 
 'audio/wav':'wav', 
 'audio/x-wav':'wav', 
 'audio/webm':'webm', 
 'audio/ogg':'ogg', 
 'audio/mpeg':'mp3', 
 'application/zip':'zip', 
 'application/x-zip':'zip', 
 'application/x-zip-compressed':'zip', 
 'application/rar':'rar', 
 'application/x-rar':'rar', 
 'application/x-rar-compressed':'rar', 
 'application/x-7z-compressed':'7z', 
 'application/pdf':'pdf', 
 'application/x-pdf':'pdf', 
 'application/x-shockwave-flash':'swf', 
 'application/ogg':'ogg', 
 'application/octet-stream':'bin'}
FILE_SIGNATURES = {'jpg':b'\xff\xd8\xff', 
 'png':b'\x89PNG\r\n\x1a\n', 
 'gif':(b'GIF87a', b'GIF89a'), 
 'bmp':b'BM', 
 'webp':b'RIFF', 
 'svg':b'<?xml', 
 'ico':b'\x00\x00\x01\x00', 
 'cur':b'\x00\x00\x02\x00', 
 'psd':b'8BPS', 
 'webm':b'\x1aE\xdf\xa3', 
 'ogg':b'OggS', 
 'wav':b'RIFF', 
 'mp3':(b'\xff\xfb', b'\xff\xf3', b'\xff\xf2', b'ID3'), 
 'zip':(b'PK\x03\x04', b'PK\x05\x06', b'PK\x07\x08'), 
 'rar':b'Rar!\x1a\x07', 
 '7z':b"7z\xbc\xaf'\x1c", 
 'pdf':b'%PDF-', 
 'swf':(b'CWS', b'FWS'), 
 'bin':b'\x00\x00\x00\x00\x00\x00\x00\x00'}
__downloader__ = HttpDownloader