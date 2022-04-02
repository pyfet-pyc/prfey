# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\youtube_dl\extractor\adobepass.py
from __future__ import unicode_literals
import re, time
import xml.etree.ElementTree as etree
from .common import InfoExtractor
from ..compat import compat_kwargs, compat_urlparse
from ..utils import unescapeHTML, urlencode_postdata, unified_timestamp, ExtractorError, NO_DEFAULT
MSO_INFO = {'DTV':{'name':'DIRECTV', 
  'username_field':'username', 
  'password_field':'password'}, 
 'ATT':{'name':'AT&T U-verse', 
  'username_field':'userid', 
  'password_field':'password'}, 
 'ATTOTT':{'name':'DIRECTV NOW', 
  'username_field':'email', 
  'password_field':'loginpassword'}, 
 'Rogers':{'name':'Rogers', 
  'username_field':'UserName', 
  'password_field':'UserPassword'}, 
 'Comcast_SSO':{'name':'Comcast XFINITY', 
  'username_field':'user', 
  'password_field':'passwd'}, 
 'TWC':{'name':'Time Warner Cable | Spectrum', 
  'username_field':'Ecom_User_ID', 
  'password_field':'Ecom_Password'}, 
 'Brighthouse':{'name':'Bright House Networks | Spectrum', 
  'username_field':'j_username', 
  'password_field':'j_password'}, 
 'Charter_Direct':{'name':'Charter Spectrum', 
  'username_field':'IDToken1', 
  'password_field':'IDToken2'}, 
 'Verizon':{'name':'Verizon FiOS', 
  'username_field':'IDToken1', 
  'password_field':'IDToken2'}, 
 'thr030':{'name': '3 Rivers Communications'}, 
 'com140':{'name': 'Access Montana'}, 
 'acecommunications':{'name': 'AcenTek'}, 
 'acm010':{'name': 'Acme Communications'}, 
 'ada020':{'name': 'Adams Cable Service'}, 
 'alb020':{'name': 'Albany Mutual Telephone'}, 
 'algona':{'name': 'Algona Municipal Utilities'}, 
 'allwest':{'name': 'All West Communications'}, 
 'all025':{'name': "Allen's Communications"}, 
 'spl010':{'name': 'Alliance Communications'}, 
 'all070':{'name': 'ALLO Communications'}, 
 'alpine':{'name': 'Alpine Communications'}, 
 'hun015':{'name': 'American Broadband'}, 
 'nwc010':{'name': 'American Broadband Missouri'}, 
 'com130-02':{'name': 'American Community Networks'}, 
 'com130-01':{'name': 'American Warrior Networks'}, 
 'tom020':{'name': 'Amherst Telephone/Tomorrow Valley'}, 
 'tvc020':{'name': 'Andycable'}, 
 'arkwest':{'name': 'Arkwest Communications'}, 
 'art030':{'name': 'Arthur Mutual Telephone Company'}, 
 'arvig':{'name': 'Arvig'}, 
 'nttcash010':{'name': 'Ashland Home Net'}, 
 'astound':{'name': 'Astound (now Wave)'}, 
 'dix030':{'name': 'ATC Broadband'}, 
 'ara010':{'name': 'ATC Communications'}, 
 'she030-02':{'name': 'Ayersville Communications'}, 
 'baldwin':{'name': 'Baldwin Lightstream'}, 
 'bal040':{'name': 'Ballard TV'}, 
 'cit025':{'name': 'Bardstown Cable TV'}, 
 'bay030':{'name': 'Bay Country Communications'}, 
 'tel095':{'name': 'Beaver Creek Cooperative Telephone'}, 
 'bea020':{'name': 'Beaver Valley Cable'}, 
 'bee010':{'name': 'Bee Line Cable'}, 
 'wir030':{'name': 'Beehive Broadband'}, 
 'bra020':{'name': 'BELD'}, 
 'bel020':{'name': 'Bellevue Municipal Cable'}, 
 'vol040-01':{'name': 'Ben Lomand Connect / BLTV'}, 
 'bev010':{'name': 'BEVCOMM'}, 
 'big020':{'name': 'Big Sandy Broadband'}, 
 'ble020':{'name': 'Bledsoe Telephone Cooperative'}, 
 'bvt010':{'name': 'Blue Valley Tele-Communications'}, 
 'bra050':{'name': 'Brandenburg Telephone Co.'}, 
 'bte010':{'name': 'Bristol Tennessee Essential Services'}, 
 'annearundel':{'name': 'Broadstripe'}, 
 'btc010':{'name': 'BTC Communications'}, 
 'btc040':{'name': 'BTC Vision - Nahunta'}, 
 'bul010':{'name': 'Bulloch Telephone Cooperative'}, 
 'but010':{'name': 'Butler-Bremer Communications'}, 
 'tel160-csp':{'name': 'C Spire SNAP'}, 
 'csicable':{'name': 'Cable Services Inc.'}, 
 'cableamerica':{'name': 'CableAmerica'}, 
 'cab038':{'name': 'CableSouth Media 3'}, 
 'weh010-camtel':{'name': 'Cam-Tel Company'}, 
 'car030':{'name': 'Cameron Communications'}, 
 'canbytel':{'name': 'Canby Telcom'}, 
 'crt020':{'name': 'CapRock Tv'}, 
 'car050':{'name': 'Carnegie Cable'}, 
 'cas':{'name': 'CAS Cable'}, 
 'casscomm':{'name': 'CASSCOMM'}, 
 'mid180-02':{'name': 'Catalina Broadband Solutions'}, 
 'cccomm':{'name': 'CC Communications'}, 
 'nttccde010':{'name': 'CDE Lightband'}, 
 'cfunet':{'name': 'Cedar Falls Utilities'}, 
 'dem010-01':{'name': 'Celect-Bloomer Telephone Area'}, 
 'dem010-02':{'name': 'Celect-Bruce Telephone Area'}, 
 'dem010-03':{'name': 'Celect-Citizens Connected Area'}, 
 'dem010-04':{'name': 'Celect-Elmwood/Spring Valley Area'}, 
 'dem010-06':{'name': 'Celect-Mosaic Telecom'}, 
 'dem010-05':{'name': 'Celect-West WI Telephone Area'}, 
 'net010-02':{'name': 'Cellcom/Nsight Telservices'}, 
 'cen100':{'name': 'CentraCom'}, 
 'nttccst010':{'name': 'Central Scott / CSTV'}, 
 'cha035':{'name': 'Chaparral CableVision'}, 
 'cha050':{'name': 'Chariton Valley Communication Corporation, Inc.'}, 
 'cha060':{'name': 'Chatmoss Cablevision'}, 
 'nttcche010':{'name': 'Cherokee Communications'}, 
 'che050':{'name': 'Chesapeake Bay Communications'}, 
 'cimtel':{'name': 'Cim-Tel Cable, LLC.'}, 
 'cit180':{'name': 'Citizens Cablevision - Floyd, VA'}, 
 'cit210':{'name': 'Citizens Cablevision, Inc.'}, 
 'cit040':{'name': 'Citizens Fiber'}, 
 'cit250':{'name': 'Citizens Mutual'}, 
 'war040':{'name': 'Citizens Telephone Corporation'}, 
 'wat025':{'name': 'City Of Monroe'}, 
 'wadsworth':{'name': 'CityLink'}, 
 'nor100':{'name': 'CL Tel'}, 
 'cla010':{'name': 'Clarence Telephone and Cedar Communications'}, 
 'ser060':{'name': 'Clear Choice Communications'}, 
 'tac020':{'name': 'Click! Cable TV'}, 
 'war020':{'name': 'CLICK1.NET'}, 
 'cml010':{'name': 'CML Telephone Cooperative Association'}, 
 'cns':{'name': 'CNS'}, 
 'com160':{'name': 'Co-Mo Connect'}, 
 'coa020':{'name': 'Coast Communications'}, 
 'coa030':{'name': 'Coaxial Cable TV'}, 
 'mid055':{'name': 'Cobalt TV (Mid-State Community TV)'}, 
 'col070':{'name': 'Columbia Power & Water Systems'}, 
 'col080':{'name': 'Columbus Telephone'}, 
 'nor105':{'name': 'Communications 1 Cablevision, Inc.'}, 
 'com150':{'name': 'Community Cable & Broadband'}, 
 'com020':{'name': 'Community Communications Company'}, 
 'coy010':{'name': 'commZoom'}, 
 'com025':{'name': 'Complete Communication Services'}, 
 'cat020':{'name': 'Comporium'}, 
 'com071':{'name': 'ComSouth Telesys'}, 
 'consolidatedcable':{'name': 'Consolidated'}, 
 'conwaycorp':{'name': 'Conway Corporation'}, 
 'coo050':{'name': 'Coon Valley Telecommunications Inc'}, 
 'coo080':{'name': 'Cooperative Telephone Company'}, 
 'cpt010':{'name': 'CP-TEL'}, 
 'cra010':{'name': 'Craw-Kan Telephone'}, 
 'crestview':{'name': 'Crestview Cable Communications'}, 
 'cross':{'name': 'Cross TV'}, 
 'cro030':{'name': 'Crosslake Communications'}, 
 'ctc040':{'name': 'CTC - Brainerd MN'}, 
 'phe030':{'name': 'CTV-Beam - East Alabama'}, 
 'cun010':{'name': 'Cunningham Telephone & Cable'}, 
 'dpc010':{'name': 'D & P Communications'}, 
 'dak030':{'name': 'Dakota Central Telecommunications'}, 
 'nttcdel010':{'name': 'Delcambre Telephone LLC'}, 
 'tel160-del':{'name': 'Delta Telephone Company'}, 
 'sal040':{'name': 'DiamondNet'}, 
 'ind060-dc':{'name': 'Direct Communications'}, 
 'doy010':{'name': 'Doylestown Cable TV'}, 
 'dic010':{'name': 'DRN'}, 
 'dtc020':{'name': 'DTC'}, 
 'dtc010':{'name': 'DTC Cable (Delhi)'}, 
 'dum010':{'name': 'Dumont Telephone Company'}, 
 'dun010':{'name': 'Dunkerton Telephone Cooperative'}, 
 'cci010':{'name': 'Duo County Telecom'}, 
 'eagle':{'name': 'Eagle Communications'}, 
 'weh010-east':{'name': 'East Arkansas Cable TV'}, 
 'eatel':{'name': 'EATEL Video, LLC'}, 
 'ell010':{'name': 'ECTA'}, 
 'emerytelcom':{'name': 'Emery Telcom Video LLC'}, 
 'nor200':{'name': 'Empire Access'}, 
 'endeavor':{'name': 'Endeavor Communications'}, 
 'sun045':{'name': 'Enhanced Telecommunications Corporation'}, 
 'mid030':{'name': 'enTouch'}, 
 'epb020':{'name': 'EPB Smartnet'}, 
 'jea010':{'name': 'EPlus Broadband'}, 
 'com065':{'name': 'ETC'}, 
 'ete010':{'name': 'Etex Communications'}, 
 'fbc-tele':{'name': 'F&B Communications'}, 
 'fal010':{'name': 'Falcon Broadband'}, 
 'fam010':{'name': 'FamilyView CableVision'}, 
 'far020':{'name': 'Farmers Mutual Telephone Company'}, 
 'fay010':{'name': 'Fayetteville Public Utilities'}, 
 'sal060':{'name': 'fibrant'}, 
 'fid010':{'name': 'Fidelity Communications'}, 
 'for030':{'name': 'FJ Communications'}, 
 'fli020':{'name': 'Flint River Communications'}, 
 'far030':{'name': 'FMT - Jesup'}, 
 'foo010':{'name': 'Foothills Communications'}, 
 'for080':{'name': 'Forsyth CableNet'}, 
 'fbcomm':{'name': 'Frankfort Plant Board'}, 
 'tel160-fra':{'name': 'Franklin Telephone Company'}, 
 'nttcftc010':{'name': 'FTC'}, 
 'fullchannel':{'name': 'Full Channel, Inc.'}, 
 'gar040':{'name': 'Gardonville Cooperative Telephone Association'}, 
 'gbt010':{'name': 'GBT Communications, Inc.'}, 
 'tec010':{'name': 'Genuine Telecom'}, 
 'clr010':{'name': 'Giant Communications'}, 
 'gla010':{'name': 'Glasgow EPB'}, 
 'gle010':{'name': 'Glenwood Telecommunications'}, 
 'gra060':{'name': 'GLW Broadband Inc.'}, 
 'goldenwest':{'name': 'Golden West Cablevision'}, 
 'vis030':{'name': 'Grantsburg Telcom'}, 
 'gpcom':{'name': 'Great Plains Communications'}, 
 'gri010':{'name': 'Gridley Cable Inc'}, 
 'hbc010':{'name': 'H&B Cable Services'}, 
 'hae010':{'name': 'Haefele TV Inc.'}, 
 'htc010':{'name': 'Halstad Telephone Company'}, 
 'har005':{'name': 'Harlan Municipal Utilities'}, 
 'har020':{'name': 'Hart Communications'}, 
 'ced010':{'name': 'Hartelco TV'}, 
 'hea040':{'name': 'Heart of Iowa Communications Cooperative'}, 
 'htc020':{'name': 'Hickory Telephone Company'}, 
 'nttchig010':{'name': 'Highland Communication Services'}, 
 'hig030':{'name': 'Highland Media'}, 
 'spc010':{'name': 'Hilliary Communications'}, 
 'hin020':{'name': 'Hinton CATV Co.'}, 
 'hometel':{'name': 'HomeTel Entertainment, Inc.'}, 
 'hoodcanal':{'name': 'Hood Canal Communications'}, 
 'weh010-hope':{'name': 'Hope - Prescott Cable TV'}, 
 'horizoncable':{'name': 'Horizon Cable TV, Inc.'}, 
 'hor040':{'name': 'Horizon Chillicothe Telephone'}, 
 'htc030':{'name': 'HTC Communications Co. - IL'}, 
 'htccomm':{'name': 'HTC Communications, Inc. - IA'}, 
 'wal005':{'name': 'Huxley Communications'}, 
 'imon':{'name': 'ImOn Communications'}, 
 'ind040':{'name': 'Independence Telecommunications'}, 
 'rrc010':{'name': 'Inland Networks'}, 
 'stc020':{'name': 'Innovative Cable TV St Croix'}, 
 'car100':{'name': 'Innovative Cable TV St Thomas-St John'}, 
 'icc010':{'name': 'Inside Connect Cable'}, 
 'int100':{'name': 'Integra Telecom'}, 
 'int050':{'name': 'Interstate Telecommunications Coop'}, 
 'irv010':{'name': 'Irvine Cable'}, 
 'k2c010':{'name': 'K2 Communications'}, 
 'kal010':{'name': 'Kalida Telephone Company, Inc.'}, 
 'kal030':{'name': 'Kalona Cooperative Telephone Company'}, 
 'kmt010':{'name': 'KMTelecom'}, 
 'kpu010':{'name': 'KPU Telecommunications'}, 
 'kuh010':{'name': 'Kuhn Communications, Inc.'}, 
 'lak130':{'name': 'Lakeland Communications'}, 
 'lan010':{'name': 'Langco'}, 
 'lau020':{'name': 'Laurel Highland Total Communications, Inc.'}, 
 'leh010':{'name': 'Lehigh Valley Cooperative Telephone'}, 
 'bra010':{'name': 'Limestone Cable/Bracken Cable'}, 
 'loc020':{'name': 'LISCO'}, 
 'lit020':{'name': 'Litestream'}, 
 'tel140':{'name': 'LivCom'}, 
 'loc010':{'name': 'LocalTel Communications'}, 
 'weh010-longview':{'name': 'Longview - Kilgore Cable TV'}, 
 'lon030':{'name': 'Lonsdale Video Ventures, LLC'}, 
 'lns010':{'name': 'Lost Nation-Elwood Telephone Co.'}, 
 'nttclpc010':{'name': 'LPC Connect'}, 
 'lumos':{'name': 'Lumos Networks'}, 
 'madison':{'name': 'Madison Communications'}, 
 'mad030':{'name': 'Madison County Cable Inc.'}, 
 'nttcmah010':{'name': 'Mahaska Communication Group'}, 
 'mar010':{'name': 'Marne & Elk Horn Telephone Company'}, 
 'mcc040':{'name': 'McClure Telephone Co.'}, 
 'mctv':{'name': 'MCTV'}, 
 'merrimac':{'name': 'Merrimac Communications Ltd.'}, 
 'metronet':{'name': 'Metronet'}, 
 'mhtc':{'name': 'MHTC'}, 
 'midhudson':{'name': 'Mid-Hudson Cable'}, 
 'midrivers':{'name': 'Mid-Rivers Communications'}, 
 'mid045':{'name': 'Midstate Communications'}, 
 'mil080':{'name': 'Milford Communications'}, 
 'min030':{'name': 'MINET'}, 
 'nttcmin010':{'name': 'Minford TV'}, 
 'san040-02':{'name': 'Mitchell Telecom'}, 
 'mlg010':{'name': 'MLGC'}, 
 'mon060':{'name': 'Mon-Cre TVE'}, 
 'mou110':{'name': 'Mountain Telephone'}, 
 'mou050':{'name': 'Mountain Village Cable'}, 
 'mtacomm':{'name': 'MTA Communications, LLC'}, 
 'mtc010':{'name': 'MTC Cable'}, 
 'med040':{'name': 'MTC Technologies'}, 
 'man060':{'name': 'MTCC'}, 
 'mtc030':{'name': 'MTCO Communications'}, 
 'mul050':{'name': 'Mulberry Telecommunications'}, 
 'mur010':{'name': 'Murray Electric System'}, 
 'musfiber':{'name': 'MUS FiberNET'}, 
 'mpw':{'name': 'Muscatine Power & Water'}, 
 'nttcsli010':{'name': 'myEVTV.com'}, 
 'nor115':{'name': 'NCC'}, 
 'nor260':{'name': 'NDTC'}, 
 'nctc':{'name': 'Nebraska Central Telecom, Inc.'}, 
 'nel020':{'name': 'Nelsonville TV Cable'}, 
 'nem010':{'name': 'Nemont'}, 
 'new075':{'name': 'New Hope Telephone Cooperative'}, 
 'nor240':{'name': 'NICP'}, 
 'cic010':{'name': 'NineStar Connect'}, 
 'nktelco':{'name': 'NKTelco'}, 
 'nortex':{'name': 'Nortex Communications'}, 
 'nor140':{'name': 'North Central Telephone Cooperative'}, 
 'nor030':{'name': 'Northland Communications'}, 
 'nor075':{'name': 'Northwest Communications'}, 
 'nor125':{'name': 'Norwood Light Broadband'}, 
 'net010':{'name': 'Nsight Telservices'}, 
 'dur010':{'name': 'Ntec'}, 
 'nts010':{'name': 'NTS Communications'}, 
 'new045':{'name': 'NU-Telecom'}, 
 'nulink':{'name': 'NuLink'}, 
 'jam030':{'name': 'NVC'}, 
 'far035':{'name': 'OmniTel Communications'}, 
 'onesource':{'name': 'OneSource Communications'}, 
 'cit230':{'name': 'Opelika Power Services'}, 
 'daltonutilities':{'name': 'OptiLink'}, 
 'mid140':{'name': 'OPTURA'}, 
 'ote010':{'name': 'OTEC Communication Company'}, 
 'cci020':{'name': 'Packerland Broadband'}, 
 'pan010':{'name': 'Panora Telco/Guthrie Center Communications'}, 
 'otter':{'name': 'Park Region Telephone & Otter Tail Telcom'}, 
 'mid050':{'name': 'Partner Communications Cooperative'}, 
 'fib010':{'name': 'Pathway'}, 
 'paulbunyan':{'name': 'Paul Bunyan Communications'}, 
 'pem020':{'name': 'Pembroke Telephone Company'}, 
 'mck010':{'name': 'Peoples Rural Telephone Cooperative'}, 
 'pul010':{'name': 'PES Energize'}, 
 'phi010':{'name': 'Philippi Communications System'}, 
 'phonoscope':{'name': 'Phonoscope Cable'}, 
 'pin070':{'name': 'Pine Belt Communications, Inc.'}, 
 'weh010-pine':{'name': 'Pine Bluff Cable TV'}, 
 'pin060':{'name': 'Pineland Telephone Cooperative'}, 
 'cam010':{'name': 'Pinpoint Communications'}, 
 'pio060':{'name': 'Pioneer Broadband'}, 
 'pioncomm':{'name': 'Pioneer Communications'}, 
 'pioneer':{'name': 'Pioneer DTV'}, 
 'pla020':{'name': 'Plant TiftNet, Inc.'}, 
 'par010':{'name': 'PLWC'}, 
 'pro035':{'name': 'PMT'}, 
 'vik011':{'name': 'Polar Cablevision'}, 
 'pottawatomie':{'name': 'Pottawatomie Telephone Co.'}, 
 'premiercomm':{'name': 'Premier Communications'}, 
 'psc010':{'name': 'PSC'}, 
 'pan020':{'name': 'PTCI'}, 
 'qco010':{'name': 'QCOL'}, 
 'qua010':{'name': 'Quality Cablevision'}, 
 'rad010':{'name': 'Radcliffe Telephone Company'}, 
 'car040':{'name': 'Rainbow Communications'}, 
 'rai030':{'name': 'Rainier Connect'}, 
 'ral010':{'name': 'Ralls Technologies'}, 
 'rct010':{'name': 'RC Technologies'}, 
 'red040':{'name': 'Red River Communications'}, 
 'ree010':{'name': 'Reedsburg Utility Commission'}, 
 'mol010':{'name': 'Reliance Connects- Oregon'}, 
 'res020':{'name': 'Reserve Telecommunications'}, 
 'weh010-resort':{'name': 'Resort TV Cable'}, 
 'rld010':{'name': 'Richland Grant Telephone Cooperative, Inc.'}, 
 'riv030':{'name': 'River Valley Telecommunications Coop'}, 
 'rockportcable':{'name': 'Rock Port Cablevision'}, 
 'rsf010':{'name': 'RS Fiber'}, 
 'rtc':{'name': 'RTC Communication Corp'}, 
 'res040':{'name': 'RTC-Reservation Telephone Coop.'}, 
 'rte010':{'name': 'RTEC Communications'}, 
 'stc010':{'name': 'S&T'}, 
 'san020':{'name': 'San Bruno Cable TV'}, 
 'san040-01':{'name': 'Santel'}, 
 'sav010':{'name': 'SCI Broadband-Savage Communications Inc.'}, 
 'sco050':{'name': 'Scottsboro Electric Power Board'}, 
 'scr010':{'name': 'Scranton Telephone Company'}, 
 'selco':{'name': 'SELCO'}, 
 'she010':{'name': 'Shentel'}, 
 'she030':{'name': 'Sherwood Mutual Telephone Association, Inc.'}, 
 'ind060-ssc':{'name': 'Silver Star Communications'}, 
 'sjoberg':{'name': "Sjoberg's Inc."}, 
 'sou025':{'name': 'SKT'}, 
 'sky050':{'name': 'SkyBest TV'}, 
 'nttcsmi010':{'name': 'Smithville Communications'}, 
 'woo010':{'name': 'Solarus'}, 
 'sou075':{'name': 'South Central Rural Telephone Cooperative'}, 
 'sou065':{'name': 'South Holt Cablevision, Inc.'}, 
 'sou035':{'name': 'South Slope Cooperative Communications'}, 
 'spa020':{'name': 'Spanish Fork Community Network'}, 
 'spe010':{'name': 'Spencer Municipal Utilities'}, 
 'spi005':{'name': 'Spillway Communications, Inc.'}, 
 'srt010':{'name': 'SRT'}, 
 'cccsmc010':{'name': 'St. Maarten Cable TV'}, 
 'sta025':{'name': 'Star Communications'}, 
 'sco020':{'name': 'STE'}, 
 'uin010':{'name': 'STRATA Networks'}, 
 'sum010':{'name': 'Sumner Cable TV'}, 
 'pie010':{'name': 'Surry TV/PCSI TV'}, 
 'swa010':{'name': 'Swayzee Communications'}, 
 'sweetwater':{'name': 'Sweetwater Cable Television Co'}, 
 'weh010-talequah':{'name': 'Tahlequah Cable TV'}, 
 'tct':{'name': 'TCT'}, 
 'tel050':{'name': 'Tele-Media Company'}, 
 'com050':{'name': 'The Community Agency'}, 
 'thr020':{'name': 'Three River'}, 
 'cab140':{'name': 'Town & Country Technologies'}, 
 'tra010':{'name': 'Trans-Video'}, 
 'tre010':{'name': 'Trenton TV Cable Company'}, 
 'tcc':{'name': 'Tri County Communications Cooperative'}, 
 'tri025':{'name': 'TriCounty Telecom'}, 
 'tri110':{'name': 'TrioTel Communications, Inc.'}, 
 'tro010':{'name': 'Troy Cablevision, Inc.'}, 
 'tsc':{'name': 'TSC'}, 
 'cit220':{'name': 'Tullahoma Utilities Board'}, 
 'tvc030':{'name': 'TV Cable of Rensselaer'}, 
 'tvc015':{'name': 'TVC Cable'}, 
 'cab180':{'name': 'TVision'}, 
 'twi040':{'name': 'Twin Lakes'}, 
 'tvtinc':{'name': 'Twin Valley'}, 
 'uis010':{'name': 'Union Telephone Company'}, 
 'uni110':{'name': 'United Communications - TN'}, 
 'uni120':{'name': 'United Services'}, 
 'uss020':{'name': 'US Sonet'}, 
 'cab060':{'name': 'USA Communications'}, 
 'she005':{'name': 'USA Communications/Shellsburg, IA'}, 
 'val040':{'name': 'Valley TeleCom Group'}, 
 'val025':{'name': 'Valley Telecommunications'}, 
 'val030':{'name': 'Valparaiso Broadband'}, 
 'cla050':{'name': 'Vast Broadband'}, 
 'sul015':{'name': 'Venture Communications Cooperative, Inc.'}, 
 'ver025':{'name': 'Vernon Communications Co-op'}, 
 'weh010-vicksburg':{'name': 'Vicksburg Video'}, 
 'vis070':{'name': 'Vision Communications'}, 
 'volcanotel':{'name': 'Volcano Vision, Inc.'}, 
 'vol040-02':{'name': 'VolFirst / BLTV'}, 
 'ver070':{'name': 'VTel'}, 
 'nttcvtx010':{'name': 'VTX1'}, 
 'bci010-02':{'name': 'Vyve Broadband'}, 
 'wab020':{'name': 'Wabash Mutual Telephone'}, 
 'waitsfield':{'name': 'Waitsfield Cable'}, 
 'wal010':{'name': 'Walnut Communications'}, 
 'wavebroadband':{'name': 'Wave'}, 
 'wav030':{'name': 'Waverly Communications Utility'}, 
 'wbi010':{'name': 'WBI'}, 
 'web020':{'name': 'Webster-Calhoun Cooperative Telephone Association'}, 
 'wes005':{'name': 'West Alabama TV Cable'}, 
 'carolinata':{'name': 'West Carolina Communications'}, 
 'wct010':{'name': 'West Central Telephone Association'}, 
 'wes110':{'name': 'West River Cooperative Telephone Company'}, 
 'ani030':{'name': 'WesTel Systems'}, 
 'westianet':{'name': 'Western Iowa Networks'}, 
 'nttcwhi010':{'name': 'Whidbey Telecom'}, 
 'weh010-white':{'name': 'White County Cable TV'}, 
 'wes130':{'name': 'Wiatel'}, 
 'wik010':{'name': 'Wiktel'}, 
 'wil070':{'name': 'Wilkes Communications, Inc./RiverStreet Networks'}, 
 'wil015':{'name': 'Wilson Communications'}, 
 'win010':{'name': 'Windomnet/SMBS'}, 
 'win090':{'name': 'Windstream Cable TV'}, 
 'wcta':{'name': 'Winnebago Cooperative Telecom Association'}, 
 'wtc010':{'name': 'WTC'}, 
 'wil040':{'name': 'WTC Communications, Inc.'}, 
 'wya010':{'name': 'Wyandotte Cable'}, 
 'hin020-02':{'name': 'X-Stream Services'}, 
 'xit010':{'name': 'XIT Communications'}, 
 'yel010':{'name': 'Yelcot Communications'}, 
 'mid180-01':{'name': 'yondoo'}, 
 'cou060':{'name': 'Zito Media'}}

class AdobePassIE(InfoExtractor):
    _SERVICE_PROVIDER_TEMPLATE = 'https://sp.auth.adobe.com/adobe-services/%s'
    _USER_AGENT = 'Mozilla/5.0 (X11; Linux i686; rv:47.0) Gecko/20100101 Firefox/47.0'
    _MVPD_CACHE = 'ap-mvpd'
    _DOWNLOADING_LOGIN_PAGE = 'Downloading Provider Login Page'

    def _download_webpage_handle(self, *args, **kwargs):
        headers = self.geo_verification_headers()
        headers.update(kwargs.get('headers', {}))
        kwargs['headers'] = headers
        return (super(AdobePassIE, self)._download_webpage_handle)(*args, **compat_kwargs(kwargs))

    @staticmethod
    def _get_mvpd_resource(provider_id, title, guid, rating):
        channel = etree.Element('channel')
        channel_title = etree.SubElement(channel, 'title')
        channel_title.text = provider_id
        item = etree.SubElement(channel, 'item')
        resource_title = etree.SubElement(item, 'title')
        resource_title.text = title
        resource_guid = etree.SubElement(item, 'guid')
        resource_guid.text = guid
        resource_rating = etree.SubElement(item, 'media:rating')
        resource_rating.attrib = {'scheme': 'urn:v-chip'}
        resource_rating.text = rating
        return '<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/">' + etree.tostring(channel).decode() + '</rss>'

    def _extract_mvpd_auth--- This code section failed: ---

 L.1355         0  LOAD_CLOSURE             'self'
                2  BUILD_TUPLE_1         1 
                4  LOAD_CODE                <code_object xml_text>
                6  LOAD_STR                 'AdobePassIE._extract_mvpd_auth.<locals>.xml_text'
                8  MAKE_FUNCTION_8          'closure'
               10  STORE_DEREF              'xml_text'

 L.1359        12  LOAD_CLOSURE             'xml_text'
               14  BUILD_TUPLE_1         1 
               16  LOAD_CODE                <code_object is_expired>
               18  LOAD_STR                 'AdobePassIE._extract_mvpd_auth.<locals>.is_expired'
               20  MAKE_FUNCTION_8          'closure'
               22  STORE_FAST               'is_expired'

 L.1363        24  BUILD_MAP_0           0 
               26  BUILD_TUPLE_1         1 
               28  LOAD_CLOSURE             'self'
               30  LOAD_CLOSURE             'video_id'
               32  BUILD_TUPLE_2         2 
               34  LOAD_CODE                <code_object post_form>
               36  LOAD_STR                 'AdobePassIE._extract_mvpd_auth.<locals>.post_form'
               38  MAKE_FUNCTION_9          'default, closure'
               40  STORE_FAST               'post_form'

 L.1375        42  LOAD_CODE                <code_object raise_mvpd_required>
               44  LOAD_STR                 'AdobePassIE._extract_mvpd_auth.<locals>.raise_mvpd_required'
               46  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               48  STORE_FAST               'raise_mvpd_required'

 L.1381        50  LOAD_CONST               (None, False)
               52  LOAD_CLOSURE             'self'
               54  BUILD_TUPLE_1         1 
               56  LOAD_CODE                <code_object extract_redirect_url>
               58  LOAD_STR                 'AdobePassIE._extract_mvpd_auth.<locals>.extract_redirect_url'
               60  MAKE_FUNCTION_9          'default, closure'
               62  STORE_FAST               'extract_redirect_url'

 L.1397        64  LOAD_STR                 'anonymous'

 L.1398        66  LOAD_STR                 'Linux i686'

 L.1399        68  LOAD_DEREF               'self'
               70  LOAD_ATTR                _USER_AGENT

 L.1400        72  LOAD_DEREF               'self'
               74  LOAD_ATTR                _USER_AGENT
               76  LOAD_CONST               ('ap_42', 'ap_11', 'ap_z', 'User-Agent')
               78  BUILD_CONST_KEY_MAP_4     4 
               80  STORE_FAST               'mvpd_headers'

 L.1403        82  LOAD_STR                 '<'
               84  LOAD_FAST                'resource'
               86  COMPARE_OP               in
               88  POP_JUMP_IF_FALSE   100  'to 100'
               90  LOAD_DEREF               'xml_text'
               92  LOAD_FAST                'resource'
               94  LOAD_STR                 'guid'
               96  CALL_FUNCTION_2       2  '2 positional arguments'
               98  JUMP_FORWARD        102  'to 102'
            100_0  COME_FROM            88  '88'
              100  LOAD_FAST                'resource'
            102_0  COME_FROM            98  '98'
              102  STORE_FAST               'guid'

 L.1404       104  LOAD_CONST               0
              106  STORE_FAST               'count'

 L.1405   108_110  SETUP_LOOP         1216  'to 1216'
              112  LOAD_FAST                'count'
              114  LOAD_CONST               2
              116  COMPARE_OP               <
          118_120  POP_JUMP_IF_FALSE  1214  'to 1214'

 L.1406       122  LOAD_DEREF               'self'
              124  LOAD_ATTR                _downloader
              126  LOAD_ATTR                cache
              128  LOAD_METHOD              load
              130  LOAD_DEREF               'self'
              132  LOAD_ATTR                _MVPD_CACHE
              134  LOAD_FAST                'requestor_id'
              136  CALL_METHOD_2         2  '2 positional arguments'
              138  JUMP_IF_TRUE_OR_POP   142  'to 142'
              140  BUILD_MAP_0           0 
            142_0  COME_FROM           138  '138'
              142  STORE_FAST               'requestor_info'

 L.1407       144  LOAD_FAST                'requestor_info'
              146  LOAD_METHOD              get
              148  LOAD_STR                 'authn_token'
              150  CALL_METHOD_1         1  '1 positional argument'
              152  STORE_FAST               'authn_token'

 L.1408       154  LOAD_FAST                'authn_token'
              156  POP_JUMP_IF_FALSE   172  'to 172'
              158  LOAD_FAST                'is_expired'
              160  LOAD_FAST                'authn_token'
              162  LOAD_STR                 'simpleTokenExpires'
              164  CALL_FUNCTION_2       2  '2 positional arguments'
              166  POP_JUMP_IF_FALSE   172  'to 172'

 L.1409       168  LOAD_CONST               None
              170  STORE_FAST               'authn_token'
            172_0  COME_FROM           166  '166'
            172_1  COME_FROM           156  '156'

 L.1410       172  LOAD_FAST                'authn_token'
          174_176  POP_JUMP_IF_TRUE    900  'to 900'

 L.1412       178  LOAD_DEREF               'self'
              180  LOAD_ATTR                _downloader
              182  LOAD_ATTR                params
              184  LOAD_METHOD              get
              186  LOAD_STR                 'ap_mso'
              188  CALL_METHOD_1         1  '1 positional argument'
              190  STORE_FAST               'mso_id'

 L.1413       192  LOAD_FAST                'mso_id'
              194  POP_JUMP_IF_TRUE    202  'to 202'

 L.1414       196  LOAD_FAST                'raise_mvpd_required'
              198  CALL_FUNCTION_0       0  '0 positional arguments'
              200  POP_TOP          
            202_0  COME_FROM           194  '194'

 L.1415       202  LOAD_DEREF               'self'
              204  LOAD_METHOD              _get_login_info
              206  LOAD_STR                 'ap_username'
              208  LOAD_STR                 'ap_password'
              210  LOAD_FAST                'mso_id'
              212  CALL_METHOD_3         3  '3 positional arguments'
              214  UNPACK_SEQUENCE_2     2 
              216  STORE_FAST               'username'
              218  STORE_FAST               'password'

 L.1416       220  LOAD_FAST                'username'
              222  POP_JUMP_IF_FALSE   228  'to 228'
              224  LOAD_FAST                'password'
              226  POP_JUMP_IF_TRUE    234  'to 234'
            228_0  COME_FROM           222  '222'

 L.1417       228  LOAD_FAST                'raise_mvpd_required'
              230  CALL_FUNCTION_0       0  '0 positional arguments'
              232  POP_TOP          
            234_0  COME_FROM           226  '226'

 L.1418       234  LOAD_GLOBAL              MSO_INFO
              236  LOAD_FAST                'mso_id'
              238  BINARY_SUBSCR    
              240  STORE_FAST               'mso_info'

 L.1420       242  LOAD_DEREF               'self'
              244  LOAD_ATTR                _download_webpage_handle

 L.1421       246  LOAD_DEREF               'self'
              248  LOAD_ATTR                _SERVICE_PROVIDER_TEMPLATE
              250  LOAD_STR                 'authenticate/saml'
              252  BINARY_MODULO    
              254  LOAD_DEREF               'video_id'

 L.1422       256  LOAD_STR                 'Downloading Provider Redirect Page'

 L.1423       258  LOAD_STR                 'true'

 L.1424       260  LOAD_FAST                'mso_id'

 L.1425       262  LOAD_FAST                'requestor_id'

 L.1426       264  LOAD_STR                 'false'

 L.1427       266  LOAD_STR                 'adobe.com'

 L.1428       268  LOAD_FAST                'url'
              270  LOAD_CONST               ('noflash', 'mso_id', 'requestor_id', 'no_iframe', 'domain_name', 'redirect_url')
              272  BUILD_CONST_KEY_MAP_6     6 
              274  LOAD_CONST               ('query',)
              276  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              278  STORE_FAST               'provider_redirect_page_res'

 L.1431       280  LOAD_FAST                'mso_id'
              282  LOAD_STR                 'Comcast_SSO'
              284  COMPARE_OP               ==
          286_288  POP_JUMP_IF_FALSE   466  'to 466'

 L.1434       290  LOAD_FAST                'provider_redirect_page_res'
              292  UNPACK_SEQUENCE_2     2 
              294  STORE_FAST               'provider_redirect_page'
              296  STORE_FAST               'urlh'

 L.1435       298  LOAD_STR                 'automatically signing you in'
              300  LOAD_FAST                'provider_redirect_page'
              302  COMPARE_OP               in
          304_306  POP_JUMP_IF_FALSE   338  'to 338'

 L.1436       308  LOAD_DEREF               'self'
              310  LOAD_METHOD              _html_search_regex

 L.1437       312  LOAD_STR                 'window\\.location\\s*=\\s*[\\\'"]([^\\\'"]+)'

 L.1438       314  LOAD_FAST                'provider_redirect_page'
              316  LOAD_STR                 'oauth redirect'
              318  CALL_METHOD_3         3  '3 positional arguments'
              320  STORE_FAST               'oauth_redirect_url'

 L.1439       322  LOAD_DEREF               'self'
              324  LOAD_METHOD              _download_webpage

 L.1440       326  LOAD_FAST                'oauth_redirect_url'
              328  LOAD_DEREF               'video_id'
              330  LOAD_STR                 'Confirming auto login'
              332  CALL_METHOD_3         3  '3 positional arguments'
              334  POP_TOP          
              336  JUMP_FORWARD        782  'to 782'
            338_0  COME_FROM           304  '304'

 L.1442       338  LOAD_STR                 '<form name="signin"'
              340  LOAD_FAST                'provider_redirect_page'
              342  COMPARE_OP               in
          344_346  POP_JUMP_IF_FALSE   354  'to 354'

 L.1443       348  LOAD_FAST                'provider_redirect_page_res'
              350  STORE_FAST               'provider_login_page_res'
              352  JUMP_FORWARD        406  'to 406'
            354_0  COME_FROM           344  '344'

 L.1444       354  LOAD_STR                 'http-equiv="refresh"'
              356  LOAD_FAST                'provider_redirect_page'
              358  COMPARE_OP               in
          360_362  POP_JUMP_IF_FALSE   394  'to 394'

 L.1445       364  LOAD_FAST                'extract_redirect_url'

 L.1446       366  LOAD_FAST                'provider_redirect_page'
              368  LOAD_CONST               True
              370  LOAD_CONST               ('fatal',)
              372  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              374  STORE_FAST               'oauth_redirect_url'

 L.1447       376  LOAD_DEREF               'self'
              378  LOAD_METHOD              _download_webpage_handle

 L.1448       380  LOAD_FAST                'oauth_redirect_url'
              382  LOAD_DEREF               'video_id'

 L.1449       384  LOAD_DEREF               'self'
              386  LOAD_ATTR                _DOWNLOADING_LOGIN_PAGE
              388  CALL_METHOD_3         3  '3 positional arguments'
              390  STORE_FAST               'provider_login_page_res'
              392  JUMP_FORWARD        406  'to 406'
            394_0  COME_FROM           360  '360'

 L.1451       394  LOAD_FAST                'post_form'

 L.1452       396  LOAD_FAST                'provider_redirect_page_res'

 L.1453       398  LOAD_DEREF               'self'
              400  LOAD_ATTR                _DOWNLOADING_LOGIN_PAGE
              402  CALL_FUNCTION_2       2  '2 positional arguments'
              404  STORE_FAST               'provider_login_page_res'
            406_0  COME_FROM           392  '392'
            406_1  COME_FROM           352  '352'

 L.1455       406  LOAD_FAST                'post_form'

 L.1456       408  LOAD_FAST                'provider_login_page_res'
              410  LOAD_STR                 'Logging in'

 L.1457       412  LOAD_FAST                'mso_info'
              414  LOAD_STR                 'username_field'
              416  BINARY_SUBSCR    
              418  LOAD_FAST                'username'

 L.1458       420  LOAD_FAST                'mso_info'
              422  LOAD_STR                 'password_field'
              424  BINARY_SUBSCR    
              426  LOAD_FAST                'password'
              428  BUILD_MAP_2           2 
              430  CALL_FUNCTION_3       3  '3 positional arguments'
              432  STORE_FAST               'mvpd_confirm_page_res'

 L.1460       434  LOAD_FAST                'mvpd_confirm_page_res'
              436  UNPACK_SEQUENCE_2     2 
              438  STORE_FAST               'mvpd_confirm_page'
              440  STORE_FAST               'urlh'

 L.1461       442  LOAD_STR                 '<button class="submit" value="Resume">Resume</button>'
              444  LOAD_FAST                'mvpd_confirm_page'
              446  COMPARE_OP               in
          448_450  POP_JUMP_IF_FALSE   782  'to 782'

 L.1462       452  LOAD_FAST                'post_form'
              454  LOAD_FAST                'mvpd_confirm_page_res'
              456  LOAD_STR                 'Confirming Login'
              458  CALL_FUNCTION_2       2  '2 positional arguments'
              460  POP_TOP          
          462_464  JUMP_FORWARD        782  'to 782'
            466_0  COME_FROM           286  '286'

 L.1463       466  LOAD_FAST                'mso_id'
              468  LOAD_STR                 'Verizon'
              470  COMPARE_OP               ==
          472_474  POP_JUMP_IF_FALSE   670  'to 670'

 L.1466       476  LOAD_FAST                'provider_redirect_page_res'
              478  UNPACK_SEQUENCE_2     2 
              480  STORE_FAST               'provider_redirect_page'
              482  STORE_FAST               'urlh'

 L.1467       484  LOAD_STR                 'Please wait ...'
              486  LOAD_FAST                'provider_redirect_page'
              488  COMPARE_OP               in
          490_492  POP_JUMP_IF_FALSE   528  'to 528'

 L.1468       494  LOAD_DEREF               'self'
              496  LOAD_ATTR                _html_search_regex

 L.1469       498  LOAD_STR                 'self\\.parent\\.location=(["\\\'])(?P<url>.+?)\\1'

 L.1470       500  LOAD_FAST                'provider_redirect_page'

 L.1471       502  LOAD_STR                 'SAML Redirect URL'
              504  LOAD_STR                 'url'
              506  LOAD_CONST               ('group',)
              508  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              510  STORE_FAST               'saml_redirect_url'

 L.1472       512  LOAD_DEREF               'self'
              514  LOAD_METHOD              _download_webpage

 L.1473       516  LOAD_FAST                'saml_redirect_url'
              518  LOAD_DEREF               'video_id'

 L.1474       520  LOAD_STR                 'Downloading SAML Login Page'
              522  CALL_METHOD_3         3  '3 positional arguments'
              524  STORE_FAST               'saml_login_page'
              526  JUMP_FORWARD        582  'to 582'
            528_0  COME_FROM           490  '490'

 L.1476       528  LOAD_FAST                'post_form'

 L.1477       530  LOAD_FAST                'provider_redirect_page_res'
              532  LOAD_STR                 'Logging in'

 L.1478       534  LOAD_FAST                'mso_info'
              536  LOAD_STR                 'username_field'
              538  BINARY_SUBSCR    
              540  LOAD_FAST                'username'

 L.1479       542  LOAD_FAST                'mso_info'
              544  LOAD_STR                 'password_field'
              546  BINARY_SUBSCR    
              548  LOAD_FAST                'password'
              550  BUILD_MAP_2           2 
              552  CALL_FUNCTION_3       3  '3 positional arguments'
              554  STORE_FAST               'saml_login_page_res'

 L.1481       556  LOAD_FAST                'saml_login_page_res'
              558  UNPACK_SEQUENCE_2     2 
              560  STORE_FAST               'saml_login_page'
              562  STORE_FAST               'urlh'

 L.1482       564  LOAD_STR                 'Please try again.'
              566  LOAD_FAST                'saml_login_page'
              568  COMPARE_OP               in
          570_572  POP_JUMP_IF_FALSE   582  'to 582'

 L.1483       574  LOAD_GLOBAL              ExtractorError

 L.1484       576  LOAD_STR                 "We're sorry, but either the User ID or Password entered is not correct."
              578  CALL_FUNCTION_1       1  '1 positional argument'
              580  RAISE_VARARGS_1       1  'exception instance'
            582_0  COME_FROM           570  '570'
            582_1  COME_FROM           526  '526'

 L.1485       582  LOAD_DEREF               'self'
              584  LOAD_ATTR                _search_regex

 L.1486       586  LOAD_STR                 'xmlHttp\\.open\\("POST"\\s*,\\s*(["\\\'])(?P<url>.+?)\\1'

 L.1487       588  LOAD_FAST                'saml_login_page'
              590  LOAD_STR                 'SAML Login URL'
              592  LOAD_STR                 'url'
              594  LOAD_CONST               ('group',)
              596  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              598  STORE_FAST               'saml_login_url'

 L.1488       600  LOAD_DEREF               'self'
              602  LOAD_ATTR                _download_json

 L.1489       604  LOAD_FAST                'saml_login_url'
              606  LOAD_DEREF               'video_id'
              608  LOAD_STR                 'Downloading SAML Response'

 L.1490       610  LOAD_STR                 'Content-Type'
              612  LOAD_STR                 'text/xml'
              614  BUILD_MAP_1           1 
              616  LOAD_CONST               ('headers',)
              618  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              620  STORE_FAST               'saml_response_json'

 L.1491       622  LOAD_DEREF               'self'
              624  LOAD_ATTR                _download_webpage

 L.1492       626  LOAD_FAST                'saml_response_json'
              628  LOAD_STR                 'targetValue'
              630  BINARY_SUBSCR    
              632  LOAD_DEREF               'video_id'

 L.1493       634  LOAD_STR                 'Confirming Login'
              636  LOAD_GLOBAL              urlencode_postdata

 L.1494       638  LOAD_FAST                'saml_response_json'
              640  LOAD_STR                 'SAMLResponse'
              642  BINARY_SUBSCR    

 L.1495       644  LOAD_FAST                'saml_response_json'
              646  LOAD_STR                 'RelayState'
              648  BINARY_SUBSCR    
              650  LOAD_CONST               ('SAMLResponse', 'RelayState')
              652  BUILD_CONST_KEY_MAP_2     2 
            654_0  COME_FROM           336  '336'
              654  CALL_FUNCTION_1       1  '1 positional argument'

 L.1497       656  LOAD_STR                 'Content-Type'
              658  LOAD_STR                 'application/x-www-form-urlencoded'
              660  BUILD_MAP_1           1 
              662  LOAD_CONST               ('data', 'headers')
              664  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              666  POP_TOP          
              668  JUMP_FORWARD        782  'to 782'
            670_0  COME_FROM           472  '472'

 L.1502       670  LOAD_FAST                'provider_redirect_page_res'
              672  UNPACK_SEQUENCE_2     2 
              674  STORE_FAST               'provider_redirect_page'
              676  STORE_FAST               'urlh'

 L.1503       678  LOAD_FAST                'extract_redirect_url'

 L.1504       680  LOAD_FAST                'provider_redirect_page'
              682  LOAD_FAST                'urlh'
              684  LOAD_METHOD              geturl
              686  CALL_METHOD_0         0  '0 positional arguments'
              688  LOAD_CONST               ('url',)
              690  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              692  STORE_FAST               'provider_refresh_redirect_url'

 L.1505       694  LOAD_FAST                'provider_refresh_redirect_url'
          696_698  POP_JUMP_IF_FALSE   714  'to 714'

 L.1506       700  LOAD_DEREF               'self'
              702  LOAD_METHOD              _download_webpage_handle

 L.1507       704  LOAD_FAST                'provider_refresh_redirect_url'
              706  LOAD_DEREF               'video_id'

 L.1508       708  LOAD_STR                 'Downloading Provider Redirect Page (meta refresh)'
              710  CALL_METHOD_3         3  '3 positional arguments'
              712  STORE_FAST               'provider_redirect_page_res'
            714_0  COME_FROM           696  '696'

 L.1509       714  LOAD_FAST                'post_form'

 L.1510       716  LOAD_FAST                'provider_redirect_page_res'
              718  LOAD_DEREF               'self'
              720  LOAD_ATTR                _DOWNLOADING_LOGIN_PAGE
              722  CALL_FUNCTION_2       2  '2 positional arguments'
              724  STORE_FAST               'provider_login_page_res'

 L.1511       726  LOAD_FAST                'post_form'
              728  LOAD_FAST                'provider_login_page_res'
              730  LOAD_STR                 'Logging in'

 L.1512       732  LOAD_FAST                'mso_info'
              734  LOAD_METHOD              get
              736  LOAD_STR                 'username_field'
              738  LOAD_STR                 'username'
              740  CALL_METHOD_2         2  '2 positional arguments'
              742  LOAD_FAST                'username'

 L.1513       744  LOAD_FAST                'mso_info'
              746  LOAD_METHOD              get
              748  LOAD_STR                 'password_field'
              750  LOAD_STR                 'password'
              752  CALL_METHOD_2         2  '2 positional arguments'
              754  LOAD_FAST                'password'
              756  BUILD_MAP_2           2 
              758  CALL_FUNCTION_3       3  '3 positional arguments'
              760  STORE_FAST               'mvpd_confirm_page_res'

 L.1515       762  LOAD_FAST                'mso_id'
              764  LOAD_STR                 'Rogers'
              766  COMPARE_OP               !=
          768_770  POP_JUMP_IF_FALSE   782  'to 782'

 L.1516       772  LOAD_FAST                'post_form'
              774  LOAD_FAST                'mvpd_confirm_page_res'
              776  LOAD_STR                 'Confirming Login'
              778  CALL_FUNCTION_2       2  '2 positional arguments'
              780  POP_TOP          
            782_0  COME_FROM           768  '768'
            782_1  COME_FROM           668  '668'
            782_2  COME_FROM           462  '462'
            782_3  COME_FROM           448  '448'

 L.1518       782  LOAD_DEREF               'self'
              784  LOAD_ATTR                _download_webpage

 L.1519       786  LOAD_DEREF               'self'
              788  LOAD_ATTR                _SERVICE_PROVIDER_TEMPLATE
              790  LOAD_STR                 'session'
              792  BINARY_MODULO    
              794  LOAD_DEREF               'video_id'

 L.1520       796  LOAD_STR                 'Retrieving Session'
              798  LOAD_GLOBAL              urlencode_postdata

 L.1521       800  LOAD_STR                 'GET'

 L.1522       802  LOAD_FAST                'requestor_id'
              804  LOAD_CONST               ('_method', 'requestor_id')
              806  BUILD_CONST_KEY_MAP_2     2 
              808  CALL_FUNCTION_1       1  '1 positional argument'

 L.1523       810  LOAD_FAST                'mvpd_headers'
              812  LOAD_CONST               ('data', 'headers')
              814  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              816  STORE_FAST               'session'

 L.1524       818  LOAD_STR                 '<pendingLogout'
              820  LOAD_FAST                'session'
              822  COMPARE_OP               in
          824_826  POP_JUMP_IF_FALSE   858  'to 858'

 L.1525       828  LOAD_DEREF               'self'
              830  LOAD_ATTR                _downloader
              832  LOAD_ATTR                cache
              834  LOAD_METHOD              store
              836  LOAD_DEREF               'self'
              838  LOAD_ATTR                _MVPD_CACHE
              840  LOAD_FAST                'requestor_id'
              842  BUILD_MAP_0           0 
              844  CALL_METHOD_3         3  '3 positional arguments'
              846  POP_TOP          

 L.1526       848  LOAD_FAST                'count'
              850  LOAD_CONST               1
              852  INPLACE_ADD      
              854  STORE_FAST               'count'

 L.1527       856  CONTINUE            112  'to 112'
            858_0  COME_FROM           824  '824'

 L.1528       858  LOAD_GLOBAL              unescapeHTML
              860  LOAD_DEREF               'xml_text'
              862  LOAD_FAST                'session'
              864  LOAD_STR                 'authnToken'
              866  CALL_FUNCTION_2       2  '2 positional arguments'
              868  CALL_FUNCTION_1       1  '1 positional argument'
              870  STORE_FAST               'authn_token'

 L.1529       872  LOAD_FAST                'authn_token'
              874  LOAD_FAST                'requestor_info'
              876  LOAD_STR                 'authn_token'
              878  STORE_SUBSCR     

 L.1530       880  LOAD_DEREF               'self'
              882  LOAD_ATTR                _downloader
              884  LOAD_ATTR                cache
              886  LOAD_METHOD              store
              888  LOAD_DEREF               'self'
              890  LOAD_ATTR                _MVPD_CACHE
              892  LOAD_FAST                'requestor_id'
              894  LOAD_FAST                'requestor_info'
              896  CALL_METHOD_3         3  '3 positional arguments'
              898  POP_TOP          
            900_0  COME_FROM           174  '174'

 L.1532       900  LOAD_FAST                'requestor_info'
              902  LOAD_METHOD              get
              904  LOAD_FAST                'guid'
              906  CALL_METHOD_1         1  '1 positional argument'
              908  STORE_FAST               'authz_token'

 L.1533       910  LOAD_FAST                'authz_token'
          912_914  POP_JUMP_IF_FALSE   932  'to 932'
              916  LOAD_FAST                'is_expired'
              918  LOAD_FAST                'authz_token'
              920  LOAD_STR                 'simpleTokenTTL'
              922  CALL_FUNCTION_2       2  '2 positional arguments'
          924_926  POP_JUMP_IF_FALSE   932  'to 932'

 L.1534       928  LOAD_CONST               None
              930  STORE_FAST               'authz_token'
            932_0  COME_FROM           924  '924'
            932_1  COME_FROM           912  '912'

 L.1535       932  LOAD_FAST                'authz_token'
          934_936  POP_JUMP_IF_TRUE   1096  'to 1096'

 L.1536       938  LOAD_DEREF               'self'
              940  LOAD_ATTR                _download_webpage

 L.1537       942  LOAD_DEREF               'self'
              944  LOAD_ATTR                _SERVICE_PROVIDER_TEMPLATE
              946  LOAD_STR                 'authorize'
              948  BINARY_MODULO    
              950  LOAD_DEREF               'video_id'

 L.1538       952  LOAD_STR                 'Retrieving Authorization Token'
              954  LOAD_GLOBAL              urlencode_postdata

 L.1539       956  LOAD_FAST                'resource'

 L.1540       958  LOAD_FAST                'requestor_id'

 L.1541       960  LOAD_FAST                'authn_token'

 L.1542       962  LOAD_DEREF               'xml_text'
              964  LOAD_FAST                'authn_token'
              966  LOAD_STR                 'simpleTokenMsoID'
              968  CALL_FUNCTION_2       2  '2 positional arguments'

 L.1543       970  LOAD_STR                 '1'
              972  LOAD_CONST               ('resource_id', 'requestor_id', 'authentication_token', 'mso_id', 'userMeta')
              974  BUILD_CONST_KEY_MAP_5     5 
              976  CALL_FUNCTION_1       1  '1 positional argument'

 L.1544       978  LOAD_FAST                'mvpd_headers'
              980  LOAD_CONST               ('data', 'headers')
              982  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              984  STORE_FAST               'authorize'

 L.1545       986  LOAD_STR                 '<pendingLogout'
              988  LOAD_FAST                'authorize'
              990  COMPARE_OP               in
          992_994  POP_JUMP_IF_FALSE  1026  'to 1026'

 L.1546       996  LOAD_DEREF               'self'
              998  LOAD_ATTR                _downloader
             1000  LOAD_ATTR                cache
             1002  LOAD_METHOD              store
             1004  LOAD_DEREF               'self'
             1006  LOAD_ATTR                _MVPD_CACHE
             1008  LOAD_FAST                'requestor_id'
             1010  BUILD_MAP_0           0 
             1012  CALL_METHOD_3         3  '3 positional arguments'
             1014  POP_TOP          

 L.1547      1016  LOAD_FAST                'count'
             1018  LOAD_CONST               1
             1020  INPLACE_ADD      
             1022  STORE_FAST               'count'

 L.1548      1024  CONTINUE            112  'to 112'
           1026_0  COME_FROM           992  '992'

 L.1549      1026  LOAD_STR                 '<error'
             1028  LOAD_FAST                'authorize'
             1030  COMPARE_OP               in
         1032_1034  POP_JUMP_IF_FALSE  1054  'to 1054'

 L.1550      1036  LOAD_GLOBAL              ExtractorError
             1038  LOAD_DEREF               'xml_text'
             1040  LOAD_FAST                'authorize'
             1042  LOAD_STR                 'details'
             1044  CALL_FUNCTION_2       2  '2 positional arguments'
             1046  LOAD_CONST               True
             1048  LOAD_CONST               ('expected',)
             1050  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1052  RAISE_VARARGS_1       1  'exception instance'
           1054_0  COME_FROM          1032  '1032'

 L.1551      1054  LOAD_GLOBAL              unescapeHTML
             1056  LOAD_DEREF               'xml_text'
             1058  LOAD_FAST                'authorize'
             1060  LOAD_STR                 'authzToken'
             1062  CALL_FUNCTION_2       2  '2 positional arguments'
             1064  CALL_FUNCTION_1       1  '1 positional argument'
             1066  STORE_FAST               'authz_token'

 L.1552      1068  LOAD_FAST                'authz_token'
             1070  LOAD_FAST                'requestor_info'
             1072  LOAD_FAST                'guid'
             1074  STORE_SUBSCR     

 L.1553      1076  LOAD_DEREF               'self'
             1078  LOAD_ATTR                _downloader
             1080  LOAD_ATTR                cache
             1082  LOAD_METHOD              store
             1084  LOAD_DEREF               'self'
             1086  LOAD_ATTR                _MVPD_CACHE
             1088  LOAD_FAST                'requestor_id'
             1090  LOAD_FAST                'requestor_info'
             1092  CALL_METHOD_3         3  '3 positional arguments'
             1094  POP_TOP          
           1096_0  COME_FROM           934  '934'

 L.1555      1096  LOAD_FAST                'mvpd_headers'
             1098  LOAD_METHOD              update

 L.1556      1100  LOAD_DEREF               'xml_text'
             1102  LOAD_FAST                'authn_token'
             1104  LOAD_STR                 'simpleSamlNameID'
             1106  CALL_FUNCTION_2       2  '2 positional arguments'

 L.1557      1108  LOAD_DEREF               'xml_text'
             1110  LOAD_FAST                'authn_token'
             1112  LOAD_STR                 'simpleSamlSessionIndex'
             1114  CALL_FUNCTION_2       2  '2 positional arguments'
             1116  LOAD_CONST               ('ap_19', 'ap_23')
             1118  BUILD_CONST_KEY_MAP_2     2 
             1120  CALL_METHOD_1         1  '1 positional argument'
             1122  POP_TOP          

 L.1560      1124  LOAD_DEREF               'self'
             1126  LOAD_ATTR                _download_webpage

 L.1561      1128  LOAD_DEREF               'self'
             1130  LOAD_ATTR                _SERVICE_PROVIDER_TEMPLATE
             1132  LOAD_STR                 'shortAuthorize'
             1134  BINARY_MODULO    

 L.1562      1136  LOAD_DEREF               'video_id'
             1138  LOAD_STR                 'Retrieving Media Token'
             1140  LOAD_GLOBAL              urlencode_postdata

 L.1563      1142  LOAD_FAST                'authz_token'

 L.1564      1144  LOAD_FAST                'requestor_id'

 L.1565      1146  LOAD_DEREF               'xml_text'
             1148  LOAD_FAST                'authn_token'
             1150  LOAD_STR                 'simpleTokenAuthenticationGuid'
             1152  CALL_FUNCTION_2       2  '2 positional arguments'

 L.1566      1154  LOAD_STR                 'false'
             1156  LOAD_CONST               ('authz_token', 'requestor_id', 'session_guid', 'hashed_guid')
             1158  BUILD_CONST_KEY_MAP_4     4 
             1160  CALL_FUNCTION_1       1  '1 positional argument'

 L.1567      1162  LOAD_FAST                'mvpd_headers'
             1164  LOAD_CONST               ('data', 'headers')
             1166  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1168  STORE_FAST               'short_authorize'

 L.1568      1170  LOAD_STR                 '<pendingLogout'
             1172  LOAD_FAST                'short_authorize'
             1174  COMPARE_OP               in
         1176_1178  POP_JUMP_IF_FALSE  1210  'to 1210'

 L.1569      1180  LOAD_DEREF               'self'
             1182  LOAD_ATTR                _downloader
             1184  LOAD_ATTR                cache
             1186  LOAD_METHOD              store
             1188  LOAD_DEREF               'self'
             1190  LOAD_ATTR                _MVPD_CACHE
             1192  LOAD_FAST                'requestor_id'
             1194  BUILD_MAP_0           0 
             1196  CALL_METHOD_3         3  '3 positional arguments'
             1198  POP_TOP          

 L.1570      1200  LOAD_FAST                'count'
             1202  LOAD_CONST               1
             1204  INPLACE_ADD      
             1206  STORE_FAST               'count'

 L.1571      1208  CONTINUE            112  'to 112'
           1210_0  COME_FROM          1176  '1176'

 L.1572      1210  LOAD_FAST                'short_authorize'
             1212  RETURN_VALUE     
           1214_0  COME_FROM           118  '118'
             1214  POP_BLOCK        
           1216_0  COME_FROM_LOOP      108  '108'

Parse error at or near `COME_FROM' instruction at offset 654_0