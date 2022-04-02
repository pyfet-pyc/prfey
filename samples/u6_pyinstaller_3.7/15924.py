# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\youtube_dl\downloader\http.py
from __future__ import unicode_literals
import errno, os, socket, time, random, re
from .common import FileDownloader
from ..compat import compat_str, compat_urllib_error
from ..utils import ContentTooShortError, encodeFilename, int_or_none, sanitize_open, sanitized_Request, write_xattr, XAttrMetadataError, XAttrUnavailableError

class HttpFD(FileDownloader):

    def real_download(self, filename, info_dict):
        url = info_dict['url']

        class DownloadContext(dict):
            __getattr__ = dict.get
            __setattr__ = dict.__setitem__
            __delattr__ = dict.__delitem__

        ctx = DownloadContext()
        ctx.filename = filename
        ctx.tmpfilename = self.temp_name(filename)
        ctx.stream = None
        headers = {'Youtubedl-no-compression': 'True'}
        add_headers = info_dict.get('http_headers')
        if add_headers:
            headers.update(add_headers)
        is_test = self.params.get('test', False)
        chunk_size = self._TEST_FILE_SIZE if is_test else info_dict.get('downloader_options', {}).get('http_chunk_size') or self.params.get('http_chunk_size') or 0
        ctx.open_mode = 'wb'
        ctx.resume_len = 0
        ctx.data_len = None
        ctx.block_size = self.params.get('buffersize', 1024)
        ctx.start_time = time.time()
        ctx.chunk_size = None
        if self.params.get('continuedl', True):
            if os.path.isfile(encodeFilename(ctx.tmpfilename)):
                ctx.resume_len = os.path.getsize(encodeFilename(ctx.tmpfilename))
        ctx.is_resume = ctx.resume_len > 0
        count = 0
        retries = self.params.get('retries', 0)

        class SucceedDownload(Exception):
            pass

        class RetryDownload(Exception):

            def __init__(self, source_error):
                self.source_error = source_error

        class NextFragment(Exception):
            pass

        def set_range(req, start, end):
            range_header = 'bytes=%d-' % start
            if end:
                range_header += compat_str(end)
            req.add_header('Range', range_header)

        def establish_connection--- This code section failed: ---

 L.  88         0  LOAD_DEREF               'is_test'
                2  POP_JUMP_IF_TRUE     28  'to 28'
                4  LOAD_DEREF               'chunk_size'
                6  POP_JUMP_IF_FALSE    28  'to 28'
                8  LOAD_GLOBAL              random
               10  LOAD_METHOD              randint
               12  LOAD_GLOBAL              int
               14  LOAD_DEREF               'chunk_size'
               16  LOAD_CONST               0.95
               18  BINARY_MULTIPLY  
               20  CALL_FUNCTION_1       1  '1 positional argument'
               22  LOAD_DEREF               'chunk_size'
               24  CALL_METHOD_2         2  '2 positional arguments'
               26  JUMP_FORWARD         30  'to 30'
             28_0  COME_FROM             6  '6'
             28_1  COME_FROM             2  '2'
               28  LOAD_DEREF               'chunk_size'
             30_0  COME_FROM            26  '26'
               30  LOAD_DEREF               'ctx'
               32  STORE_ATTR               chunk_size

 L.  89        34  LOAD_DEREF               'ctx'
               36  LOAD_ATTR                resume_len
               38  LOAD_CONST               0
               40  COMPARE_OP               >
               42  POP_JUMP_IF_FALSE    76  'to 76'

 L.  90        44  LOAD_DEREF               'ctx'
               46  LOAD_ATTR                resume_len
               48  STORE_FAST               'range_start'

 L.  91        50  LOAD_DEREF               'ctx'
               52  LOAD_ATTR                is_resume
               54  POP_JUMP_IF_FALSE    68  'to 68'

 L.  92        56  LOAD_DEREF               'self'
               58  LOAD_METHOD              report_resuming_byte
               60  LOAD_DEREF               'ctx'
               62  LOAD_ATTR                resume_len
               64  CALL_METHOD_1         1  '1 positional argument'
               66  POP_TOP          
             68_0  COME_FROM            54  '54'

 L.  93        68  LOAD_STR                 'ab'
               70  LOAD_DEREF               'ctx'
               72  STORE_ATTR               open_mode
               74  JUMP_FORWARD         96  'to 96'
             76_0  COME_FROM            42  '42'

 L.  94        76  LOAD_DEREF               'ctx'
               78  LOAD_ATTR                chunk_size
               80  LOAD_CONST               0
               82  COMPARE_OP               >
               84  POP_JUMP_IF_FALSE    92  'to 92'

 L.  95        86  LOAD_CONST               0
               88  STORE_FAST               'range_start'
               90  JUMP_FORWARD         96  'to 96'
             92_0  COME_FROM            84  '84'

 L.  97        92  LOAD_CONST               None
               94  STORE_FAST               'range_start'
             96_0  COME_FROM            90  '90'
             96_1  COME_FROM            74  '74'

 L.  98        96  LOAD_CONST               False
               98  LOAD_DEREF               'ctx'
              100  STORE_ATTR               is_resume

 L.  99       102  LOAD_DEREF               'ctx'
              104  LOAD_ATTR                chunk_size
              106  POP_JUMP_IF_FALSE   122  'to 122'
              108  LOAD_FAST                'range_start'
              110  LOAD_DEREF               'ctx'
              112  LOAD_ATTR                chunk_size
              114  BINARY_ADD       
              116  LOAD_CONST               1
              118  BINARY_SUBTRACT  
              120  JUMP_FORWARD        124  'to 124'
            122_0  COME_FROM           106  '106'
              122  LOAD_CONST               None
            124_0  COME_FROM           120  '120'
              124  STORE_FAST               'range_end'

 L. 100       126  LOAD_FAST                'range_end'
              128  POP_JUMP_IF_FALSE   160  'to 160'
              130  LOAD_DEREF               'ctx'
              132  LOAD_ATTR                data_len
              134  LOAD_CONST               None
              136  COMPARE_OP               is-not
              138  POP_JUMP_IF_FALSE   160  'to 160'
              140  LOAD_FAST                'range_end'
              142  LOAD_DEREF               'ctx'
              144  LOAD_ATTR                data_len
              146  COMPARE_OP               >=
              148  POP_JUMP_IF_FALSE   160  'to 160'

 L. 101       150  LOAD_DEREF               'ctx'
              152  LOAD_ATTR                data_len
              154  LOAD_CONST               1
              156  BINARY_SUBTRACT  
              158  STORE_FAST               'range_end'
            160_0  COME_FROM           148  '148'
            160_1  COME_FROM           138  '138'
            160_2  COME_FROM           128  '128'

 L. 102       160  LOAD_FAST                'range_start'
              162  LOAD_CONST               None
              164  COMPARE_OP               is-not
              166  STORE_FAST               'has_range'

 L. 103       168  LOAD_FAST                'has_range'
              170  LOAD_DEREF               'ctx'
              172  STORE_ATTR               has_range

 L. 104       174  LOAD_GLOBAL              sanitized_Request
              176  LOAD_DEREF               'url'
              178  LOAD_CONST               None
              180  LOAD_DEREF               'headers'
              182  CALL_FUNCTION_3       3  '3 positional arguments'
              184  STORE_FAST               'request'

 L. 105       186  LOAD_FAST                'has_range'
              188  POP_JUMP_IF_FALSE   202  'to 202'

 L. 106       190  LOAD_DEREF               'set_range'
              192  LOAD_FAST                'request'
              194  LOAD_FAST                'range_start'
              196  LOAD_FAST                'range_end'
              198  CALL_FUNCTION_3       3  '3 positional arguments'
              200  POP_TOP          
            202_0  COME_FROM           188  '188'

 L. 108   202_204  SETUP_EXCEPT        488  'to 488'

 L. 109       206  SETUP_EXCEPT        226  'to 226'

 L. 110       208  LOAD_DEREF               'self'
              210  LOAD_ATTR                ydl
              212  LOAD_METHOD              urlopen
              214  LOAD_FAST                'request'
              216  CALL_METHOD_1         1  '1 positional argument'
              218  LOAD_DEREF               'ctx'
              220  STORE_ATTR               data
              222  POP_BLOCK        
              224  JUMP_FORWARD        304  'to 304'
            226_0  COME_FROM_EXCEPT    206  '206'

 L. 111       226  DUP_TOP          
              228  LOAD_GLOBAL              compat_urllib_error
              230  LOAD_ATTR                URLError
              232  BUILD_TUPLE_1         1 
              234  COMPARE_OP               exception-match
          236_238  POP_JUMP_IF_FALSE   302  'to 302'
              240  POP_TOP          
              242  STORE_FAST               'err'
              244  POP_TOP          
              246  SETUP_FINALLY       290  'to 290'

 L. 113       248  LOAD_GLOBAL              getattr
              250  LOAD_FAST                'err'
              252  LOAD_STR                 'reason'
              254  LOAD_CONST               None
              256  CALL_FUNCTION_3       3  '3 positional arguments'
              258  STORE_FAST               'reason'

 L. 114       260  LOAD_GLOBAL              isinstance
              262  LOAD_FAST                'reason'
              264  LOAD_GLOBAL              socket
              266  LOAD_ATTR                timeout
              268  CALL_FUNCTION_2       2  '2 positional arguments'
          270_272  POP_JUMP_IF_FALSE   282  'to 282'

 L. 115       274  LOAD_DEREF               'RetryDownload'
              276  LOAD_FAST                'err'
              278  CALL_FUNCTION_1       1  '1 positional argument'
              280  RAISE_VARARGS_1       1  'exception instance'
            282_0  COME_FROM           270  '270'

 L. 116       282  LOAD_FAST                'err'
              284  RAISE_VARARGS_1       1  'exception instance'
              286  POP_BLOCK        
              288  LOAD_CONST               None
            290_0  COME_FROM_FINALLY   246  '246'
              290  LOAD_CONST               None
              292  STORE_FAST               'err'
              294  DELETE_FAST              'err'
              296  END_FINALLY      
              298  POP_EXCEPT       
              300  JUMP_FORWARD        304  'to 304'
            302_0  COME_FROM           236  '236'
              302  END_FINALLY      
            304_0  COME_FROM           300  '300'
            304_1  COME_FROM           224  '224'

 L. 122       304  LOAD_FAST                'has_range'
          306_308  POP_JUMP_IF_FALSE   460  'to 460'

 L. 123       310  LOAD_DEREF               'ctx'
              312  LOAD_ATTR                data
              314  LOAD_ATTR                headers
              316  LOAD_METHOD              get
              318  LOAD_STR                 'Content-Range'
              320  CALL_METHOD_1         1  '1 positional argument'
              322  STORE_FAST               'content_range'

 L. 124       324  LOAD_FAST                'content_range'
          326_328  POP_JUMP_IF_FALSE   440  'to 440'

 L. 125       330  LOAD_GLOBAL              re
              332  LOAD_METHOD              search
              334  LOAD_STR                 'bytes (\\d+)-(\\d+)?(?:/(\\d+))?'
              336  LOAD_FAST                'content_range'
              338  CALL_METHOD_2         2  '2 positional arguments'
              340  STORE_FAST               'content_range_m'

 L. 127       342  LOAD_FAST                'content_range_m'
          344_346  POP_JUMP_IF_FALSE   440  'to 440'

 L. 128       348  LOAD_FAST                'range_start'
              350  LOAD_GLOBAL              int
              352  LOAD_FAST                'content_range_m'
              354  LOAD_METHOD              group
              356  LOAD_CONST               1
              358  CALL_METHOD_1         1  '1 positional argument'
              360  CALL_FUNCTION_1       1  '1 positional argument'
              362  COMPARE_OP               ==
          364_366  POP_JUMP_IF_FALSE   440  'to 440'

 L. 129       368  LOAD_GLOBAL              int_or_none
              370  LOAD_FAST                'content_range_m'
              372  LOAD_METHOD              group
              374  LOAD_CONST               2
              376  CALL_METHOD_1         1  '1 positional argument'
              378  CALL_FUNCTION_1       1  '1 positional argument'
              380  STORE_FAST               'content_range_end'

 L. 130       382  LOAD_GLOBAL              int_or_none
              384  LOAD_FAST                'content_range_m'
              386  LOAD_METHOD              group
              388  LOAD_CONST               3
              390  CALL_METHOD_1         1  '1 positional argument'
              392  CALL_FUNCTION_1       1  '1 positional argument'
              394  STORE_FAST               'content_len'

 L. 133       396  LOAD_DEREF               'ctx'
              398  LOAD_ATTR                chunk_size
              400  UNARY_NOT        
          402_404  JUMP_IF_TRUE_OR_POP   422  'to 422'

 L. 136       406  LOAD_FAST                'content_range_end'
              408  LOAD_FAST                'range_end'
              410  COMPARE_OP               ==
          412_414  JUMP_IF_TRUE_OR_POP   422  'to 422'

 L. 137       416  LOAD_FAST                'content_len'
              418  LOAD_FAST                'range_end'
              420  COMPARE_OP               <
            422_0  COME_FROM           412  '412'
            422_1  COME_FROM           402  '402'
              422  STORE_FAST               'accept_content_len'

 L. 138       424  LOAD_FAST                'accept_content_len'
          426_428  POP_JUMP_IF_FALSE   440  'to 440'

 L. 139       430  LOAD_FAST                'content_len'
              432  LOAD_DEREF               'ctx'
              434  STORE_ATTR               data_len

 L. 140       436  LOAD_CONST               None
              438  RETURN_VALUE     
            440_0  COME_FROM           426  '426'
            440_1  COME_FROM           364  '364'
            440_2  COME_FROM           344  '344'
            440_3  COME_FROM           326  '326'

 L. 144       440  LOAD_DEREF               'self'
              442  LOAD_METHOD              report_unable_to_resume
              444  CALL_METHOD_0         0  '0 positional arguments'
              446  POP_TOP          

 L. 145       448  LOAD_CONST               0
              450  LOAD_DEREF               'ctx'
              452  STORE_ATTR               resume_len

 L. 146       454  LOAD_STR                 'wb'
              456  LOAD_DEREF               'ctx'
              458  STORE_ATTR               open_mode
            460_0  COME_FROM           306  '306'

 L. 147       460  LOAD_GLOBAL              int_or_none
              462  LOAD_DEREF               'ctx'
              464  LOAD_ATTR                data
              466  LOAD_METHOD              info
              468  CALL_METHOD_0         0  '0 positional arguments'
              470  LOAD_METHOD              get
              472  LOAD_STR                 'Content-length'
              474  LOAD_CONST               None
              476  CALL_METHOD_2         2  '2 positional arguments'
              478  CALL_FUNCTION_1       1  '1 positional argument'
              480  LOAD_DEREF               'ctx'
              482  STORE_ATTR               data_len

 L. 148       484  LOAD_CONST               None
              486  RETURN_VALUE     
            488_0  COME_FROM_EXCEPT    202  '202'

 L. 149       488  DUP_TOP          
              490  LOAD_GLOBAL              compat_urllib_error
              492  LOAD_ATTR                HTTPError
              494  BUILD_TUPLE_1         1 
              496  COMPARE_OP               exception-match
          498_500  POP_JUMP_IF_FALSE   824  'to 824'
              502  POP_TOP          
              504  STORE_FAST               'err'
              506  POP_TOP          
          508_510  SETUP_FINALLY       812  'to 812'

 L. 150       512  LOAD_FAST                'err'
              514  LOAD_ATTR                code
              516  LOAD_CONST               416
              518  COMPARE_OP               ==
          520_522  POP_JUMP_IF_FALSE   774  'to 774'

 L. 152       524  SETUP_EXCEPT        566  'to 566'

 L. 154       526  LOAD_DEREF               'self'
              528  LOAD_ATTR                ydl
              530  LOAD_METHOD              urlopen

 L. 155       532  LOAD_GLOBAL              sanitized_Request
              534  LOAD_DEREF               'url'
              536  LOAD_CONST               None
              538  LOAD_DEREF               'headers'
              540  CALL_FUNCTION_3       3  '3 positional arguments'
              542  CALL_METHOD_1         1  '1 positional argument'
              544  LOAD_DEREF               'ctx'
              546  STORE_ATTR               data

 L. 156       548  LOAD_DEREF               'ctx'
              550  LOAD_ATTR                data
              552  LOAD_METHOD              info
              554  CALL_METHOD_0         0  '0 positional arguments'
              556  LOAD_STR                 'Content-Length'
              558  BINARY_SUBSCR    
              560  STORE_FAST               'content_length'
              562  POP_BLOCK        
              564  JUMP_FORWARD        632  'to 632'
            566_0  COME_FROM_EXCEPT    524  '524'

 L. 157       566  DUP_TOP          
              568  LOAD_GLOBAL              compat_urllib_error
              570  LOAD_ATTR                HTTPError
              572  BUILD_TUPLE_1         1 
              574  COMPARE_OP               exception-match
          576_578  POP_JUMP_IF_FALSE   630  'to 630'
              580  POP_TOP          
              582  STORE_FAST               'err'
              584  POP_TOP          
              586  SETUP_FINALLY       618  'to 618'

 L. 158       588  LOAD_FAST                'err'
              590  LOAD_ATTR                code
              592  LOAD_CONST               500
              594  COMPARE_OP               <
          596_598  POP_JUMP_IF_TRUE    612  'to 612'
              600  LOAD_FAST                'err'
              602  LOAD_ATTR                code
              604  LOAD_CONST               600
              606  COMPARE_OP               >=
          608_610  POP_JUMP_IF_FALSE   614  'to 614'
            612_0  COME_FROM           596  '596'

 L. 159       612  RAISE_VARARGS_0       0  'reraise'
            614_0  COME_FROM           608  '608'
              614  POP_BLOCK        
              616  LOAD_CONST               None
            618_0  COME_FROM_FINALLY   586  '586'
              618  LOAD_CONST               None
              620  STORE_FAST               'err'
              622  DELETE_FAST              'err'
              624  END_FINALLY      
              626  POP_EXCEPT       
              628  JUMP_FORWARD        772  'to 772'
            630_0  COME_FROM           576  '576'
              630  END_FINALLY      
            632_0  COME_FROM           564  '564'

 L. 162       632  LOAD_FAST                'content_length'
              634  LOAD_CONST               None
              636  COMPARE_OP               is-not
          638_640  POP_JUMP_IF_FALSE   748  'to 748'

 L. 163       642  LOAD_DEREF               'ctx'
              644  LOAD_ATTR                resume_len
              646  LOAD_CONST               100
              648  BINARY_SUBTRACT  
              650  LOAD_GLOBAL              int
              652  LOAD_FAST                'content_length'
              654  CALL_FUNCTION_1       1  '1 positional argument'
              656  DUP_TOP          
              658  ROT_THREE        
              660  COMPARE_OP               <
          662_664  POP_JUMP_IF_FALSE   682  'to 682'
              666  LOAD_DEREF               'ctx'
              668  LOAD_ATTR                resume_len
              670  LOAD_CONST               100
              672  BINARY_ADD       
              674  COMPARE_OP               <
          676_678  POP_JUMP_IF_FALSE   748  'to 748'
              680  JUMP_FORWARD        686  'to 686'
            682_0  COME_FROM           662  '662'
              682  POP_TOP          
              684  JUMP_FORWARD        748  'to 748'
            686_0  COME_FROM           680  '680'

 L. 171       686  LOAD_DEREF               'self'
              688  LOAD_METHOD              report_file_already_downloaded
              690  LOAD_DEREF               'ctx'
              692  LOAD_ATTR                filename
              694  CALL_METHOD_1         1  '1 positional argument'
              696  POP_TOP          

 L. 172       698  LOAD_DEREF               'self'
              700  LOAD_METHOD              try_rename
              702  LOAD_DEREF               'ctx'
              704  LOAD_ATTR                tmpfilename
              706  LOAD_DEREF               'ctx'
              708  LOAD_ATTR                filename
              710  CALL_METHOD_2         2  '2 positional arguments'
              712  POP_TOP          

 L. 173       714  LOAD_DEREF               'self'
              716  LOAD_METHOD              _hook_progress

 L. 174       718  LOAD_DEREF               'ctx'
              720  LOAD_ATTR                filename

 L. 175       722  LOAD_STR                 'finished'

 L. 176       724  LOAD_DEREF               'ctx'
              726  LOAD_ATTR                resume_len

 L. 177       728  LOAD_DEREF               'ctx'
              730  LOAD_ATTR                resume_len
              732  LOAD_CONST               ('filename', 'status', 'downloaded_bytes', 'total_bytes')
              734  BUILD_CONST_KEY_MAP_4     4 
              736  CALL_METHOD_1         1  '1 positional argument'
              738  POP_TOP          

 L. 179       740  LOAD_DEREF               'SucceedDownload'
              742  CALL_FUNCTION_0       0  '0 positional arguments'
              744  RAISE_VARARGS_1       1  'exception instance'
              746  JUMP_FORWARD        772  'to 772'
            748_0  COME_FROM           684  '684'
            748_1  COME_FROM           676  '676'
            748_2  COME_FROM           638  '638'

 L. 182       748  LOAD_DEREF               'self'
              750  LOAD_METHOD              report_unable_to_resume
              752  CALL_METHOD_0         0  '0 positional arguments'
              754  POP_TOP          

 L. 183       756  LOAD_CONST               0
              758  LOAD_DEREF               'ctx'
              760  STORE_ATTR               resume_len

 L. 184       762  LOAD_STR                 'wb'
              764  LOAD_DEREF               'ctx'
              766  STORE_ATTR               open_mode

 L. 185       768  LOAD_CONST               None
              770  RETURN_VALUE     
            772_0  COME_FROM           746  '746'
            772_1  COME_FROM           628  '628'
              772  JUMP_FORWARD        800  'to 800'
            774_0  COME_FROM           520  '520'

 L. 186       774  LOAD_FAST                'err'
              776  LOAD_ATTR                code
              778  LOAD_CONST               500
              780  COMPARE_OP               <
          782_784  POP_JUMP_IF_TRUE    798  'to 798'
              786  LOAD_FAST                'err'
              788  LOAD_ATTR                code
              790  LOAD_CONST               600
              792  COMPARE_OP               >=
          794_796  POP_JUMP_IF_FALSE   800  'to 800'
            798_0  COME_FROM           782  '782'

 L. 188       798  RAISE_VARARGS_0       0  'reraise'
            800_0  COME_FROM           794  '794'
            800_1  COME_FROM           772  '772'

 L. 189       800  LOAD_DEREF               'RetryDownload'
              802  LOAD_FAST                'err'
              804  CALL_FUNCTION_1       1  '1 positional argument'
              806  RAISE_VARARGS_1       1  'exception instance'
              808  POP_BLOCK        
              810  LOAD_CONST               None
            812_0  COME_FROM_FINALLY   508  '508'
              812  LOAD_CONST               None
              814  STORE_FAST               'err'
              816  DELETE_FAST              'err'
              818  END_FINALLY      
              820  POP_EXCEPT       
              822  JUMP_FORWARD        886  'to 886'
            824_0  COME_FROM           498  '498'

 L. 190       824  DUP_TOP          
              826  LOAD_GLOBAL              socket
              828  LOAD_ATTR                error
              830  COMPARE_OP               exception-match
          832_834  POP_JUMP_IF_FALSE   884  'to 884'
              836  POP_TOP          
              838  STORE_FAST               'err'
              840  POP_TOP          
              842  SETUP_FINALLY       872  'to 872'

 L. 191       844  LOAD_FAST                'err'
              846  LOAD_ATTR                errno
              848  LOAD_GLOBAL              errno
              850  LOAD_ATTR                ECONNRESET
              852  COMPARE_OP               !=
          854_856  POP_JUMP_IF_FALSE   860  'to 860'

 L. 193       858  RAISE_VARARGS_0       0  'reraise'
            860_0  COME_FROM           854  '854'

 L. 194       860  LOAD_DEREF               'RetryDownload'
              862  LOAD_FAST                'err'
              864  CALL_FUNCTION_1       1  '1 positional argument'
              866  RAISE_VARARGS_1       1  'exception instance'
              868  POP_BLOCK        
              870  LOAD_CONST               None
            872_0  COME_FROM_FINALLY   842  '842'
              872  LOAD_CONST               None
              874  STORE_FAST               'err'
              876  DELETE_FAST              'err'
              878  END_FINALLY      
              880  POP_EXCEPT       
              882  JUMP_FORWARD        886  'to 886'
            884_0  COME_FROM           832  '832'
              884  END_FINALLY      
            886_0  COME_FROM           882  '882'
            886_1  COME_FROM           822  '822'

Parse error at or near `None' instruction at offset -1

        def download():
            data_len = ctx.data.info().get('Content-length', None)
            if is_test:
                if data_len is None or int(data_len) > self._TEST_FILE_SIZE:
                    data_len = self._TEST_FILE_SIZE
            if data_len is not None:
                data_len = int(data_len) + ctx.resume_len
                min_data_len = self.params.get('min_filesize')
                max_data_len = self.params.get('max_filesize')
                if min_data_len is not None:
                    if data_len < min_data_len:
                        self.to_screen('\r[download] File is smaller than min-filesize (%s bytes < %s bytes). Aborting.' % (data_len, min_data_len))
                        return False
                if max_data_len is not None:
                    if data_len > max_data_len:
                        self.to_screen('\r[download] File is larger than max-filesize (%s bytes > %s bytes). Aborting.' % (data_len, max_data_len))
                        return False
            byte_counter = 0 + ctx.resume_len
            block_size = ctx.block_size
            start = time.time()
            now = None
            before = start

            def retry(e):
                to_stdout = ctx.tmpfilename == '-'
                if ctx.stream is not None:
                    if not to_stdout:
                        ctx.stream.close()
                    ctx.stream = None
                ctx.resume_len = byte_counter if to_stdout else os.path.getsize(encodeFilename(ctx.tmpfilename))
                raise RetryDownload(e)

            while 1:
                try:
                    data_block = ctx.data.read(block_size if data_len is None else minblock_size(data_len - byte_counter))
                except socket.timeout as e:
                    try:
                        retry(e)
                    finally:
                        e = None
                        del e

                except socket.error as e:
                    try:
                        if e.errno in (errno.ECONNRESET, errno.ETIMEDOUT) or getattr(e, 'message', None) == 'The read operation timed out':
                            retry(e)
                        raise
                    finally:
                        e = None
                        del e

                byte_counter += len(data_block)
                if len(data_block) == 0:
                    break
                elif ctx.stream is None:
                    try:
                        ctx.stream, ctx.tmpfilename = sanitize_openctx.tmpfilenamectx.open_mode
                        assert ctx.stream is not None
                        ctx.filename = self.undo_temp_name(ctx.tmpfilename)
                        self.report_destination(ctx.filename)
                    except (OSError, IOError) as err:
                        try:
                            self.report_error('unable to open for writing: %s' % str(err))
                            return False
                        finally:
                            err = None
                            del err

                    if self.params.get('xattr_set_filesize', False):
                        if data_len is not None:
                            try:
                                write_xattr(ctx.tmpfilename, 'user.ytdl.filesize', str(data_len).encode('utf-8'))
                            except (XAttrUnavailableError, XAttrMetadataError) as err:
                                try:
                                    self.report_error('unable to set filesize xattr: %s' % str(err))
                                finally:
                                    err = None
                                    del err

                    try:
                        ctx.stream.write(data_block)
                    except (IOError, OSError) as err:
                        try:
                            self.to_stderr('\n')
                            self.report_error('unable to write data: %s' % str(err))
                            return False
                        finally:
                            err = None
                            del err

                    self.slow_down(start, now, byte_counter - ctx.resume_len)
                    now = time.time()
                    after = now
                    if not self.params.get('noresizebuffer', False):
                        block_size = self.best_block_size(after - before, len(data_block))
                    before = after
                    speed = self.calc_speed(start, now, byte_counter - ctx.resume_len)
                    if ctx.data_len is None:
                        eta = None
                else:
                    eta = self.calc_eta(start, time.time(), ctx.data_len - ctx.resume_len, byte_counter - ctx.resume_len)
                self._hook_progress({'status':'downloading', 
                 'downloaded_bytes':byte_counter, 
                 'total_bytes':ctx.data_len, 
                 'tmpfilename':ctx.tmpfilename, 
                 'filename':ctx.filename, 
                 'eta':eta, 
                 'speed':speed, 
                 'elapsed':now - ctx.start_time})
                if data_len is not None and byte_counter == data_len:
                    break

            if not is_test:
                if ctx.chunk_size and ctx.data_len is not None:
                    if byte_counter < ctx.data_len:
                        ctx.resume_len = byte_counter
                        raise NextFragment()
            else:
                if ctx.stream is None:
                    self.to_stderr('\n')
                    self.report_error('Did not get any data blocks')
                    return False
                if ctx.tmpfilename != '-':
                    ctx.stream.close()
                if data_len is not None and byte_counter != data_len:
                    err = ContentTooShortErrorbyte_counterint(data_len)
                    if count <= retries:
                        retry(err)
                    raise err
            self.try_rename(ctx.tmpfilename, ctx.filename)
            if self.params.get('updatetime', True):
                info_dict['filetime'] = self.try_utime(ctx.filename, ctx.data.info().get('last-modified', None))
            self._hook_progress({'downloaded_bytes':byte_counter, 
             'total_bytes':byte_counter, 
             'filename':ctx.filename, 
             'status':'finished', 
             'elapsed':time.time() - ctx.start_time})
            return True

        while count <= retries:
            try:
                establish_connection()
                return download()
            except RetryDownload as e:
                try:
                    count += 1
                    if count <= retries:
                        self.report_retry(e.source_error, count, retries)
                    continue
                finally:
                    e = None
                    del e

            except NextFragment:
                continue
            except SucceedDownload:
                return True

        self.report_error('giving up after %s retries' % retries)
        return False