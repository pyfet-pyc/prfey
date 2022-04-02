# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: fangcore.py
"""
November 2020 - FangCore - Jacob Scrapchansky
FangCore is a python library built for creating highly customizable Operating systems.
It has incredibly high-level command parsing, script management, remote terminal, and distributed processing tools
"""
VERSION = 'v1.2Beta'
import socket, threading, ssl

class FangCore:

    def __init__(self, *enabled_builtins):
        self.command_bindings = []
        self.load_defines = {}
        self.extension_defines = {}
        self.extensions = []
        self.appfiles = []
        self.limitlist_function = None
        if 'load' in enabled_builtins:
            self.bind_command('load', self._default_appfile_loader)
        if 'quit' in enabled_builtins:
            self.bind_command('quit', quit)

    def command--- This code section failed: ---

 L.  45         0  SETUP_FINALLY        38  'to 38'

 L.  46         2  LOAD_FAST                'string'
                4  LOAD_METHOD              strip
                6  CALL_METHOD_0         0  ''
                8  STORE_FAST               'string'

 L.  47        10  LOAD_FAST                'string'
               12  LOAD_METHOD              replace
               14  LOAD_STR                 '\r\n'
               16  LOAD_STR                 ' '
               18  CALL_METHOD_2         2  ''
               20  STORE_FAST               'string'

 L.  48        22  LOAD_FAST                'string'
               24  LOAD_METHOD              replace
               26  LOAD_STR                 '\n'
               28  LOAD_STR                 ' '
               30  CALL_METHOD_2         2  ''
               32  STORE_FAST               'string'
               34  POP_BLOCK        
               36  JUMP_FORWARD         60  'to 60'
             38_0  COME_FROM_FINALLY     0  '0'

 L.  49        38  DUP_TOP          
               40  LOAD_GLOBAL              Exception
               42  COMPARE_OP               exception-match
               44  POP_JUMP_IF_FALSE    58  'to 58'
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L.  50        52  POP_EXCEPT       
               54  LOAD_CONST               None
               56  RETURN_VALUE     
             58_0  COME_FROM            44  '44'
               58  END_FINALLY      
             60_0  COME_FROM            36  '36'

 L.  52        60  BUILD_LIST_0          0 
               62  BUILD_LIST_0          0 
               64  LOAD_STR                 ''
               66  LOAD_STR                 ''
               68  BUILD_LIST_4          4 
               70  STORE_FAST               'parsed'

 L.  53        72  LOAD_CONST               0
               74  STORE_FAST               'letter_number'

 L.  54        76  LOAD_STR                 ''
               78  STORE_FAST               'letter'

 L.  55        80  LOAD_CONST               False
               82  STORE_FAST               'ignore_state'

 L.  56        84  LOAD_CONST               False
               86  STORE_FAST               'last_letter_space'

 L.  57        88  LOAD_CONST               False
               90  STORE_FAST               'option_state'

 L.  58        92  LOAD_STR                 ''
               94  STORE_FAST               'temp_split_parse'
             96_0  COME_FROM           400  '400'
             96_1  COME_FROM           344  '344'

 L.  61        96  LOAD_FAST                'string'
               98  LOAD_FAST                'letter_number'
              100  BINARY_SUBSCR    
              102  STORE_FAST               'letter'

 L.  62       104  LOAD_FAST                'letter'
              106  LOAD_STR                 '\\'
              108  COMPARE_OP               ==
              110  POP_JUMP_IF_FALSE   134  'to 134'

 L.  63       112  LOAD_FAST                'ignore_state'
              114  POP_JUMP_IF_FALSE   130  'to 130'

 L.  64       116  LOAD_FAST                'temp_split_parse'
              118  LOAD_STR                 '\\'
              120  INPLACE_ADD      
              122  STORE_FAST               'temp_split_parse'

 L.  65       124  LOAD_CONST               False
              126  STORE_FAST               'ignore_state'
              128  JUMP_FORWARD        134  'to 134'
            130_0  COME_FROM           114  '114'

 L.  67       130  LOAD_CONST               True
              132  STORE_FAST               'ignore_state'
            134_0  COME_FROM           128  '128'
            134_1  COME_FROM           110  '110'

 L.  69       134  LOAD_FAST                'letter'
              136  LOAD_STR                 ' '
              138  COMPARE_OP               ==
              140  POP_JUMP_IF_FALSE   214  'to 214'

 L.  70       142  LOAD_FAST                'last_letter_space'
              144  POP_JUMP_IF_TRUE    194  'to 194'
              146  LOAD_FAST                'ignore_state'
              148  POP_JUMP_IF_TRUE    194  'to 194'

 L.  71       150  LOAD_FAST                'option_state'
              152  POP_JUMP_IF_FALSE   170  'to 170'

 L.  72       154  LOAD_FAST                'parsed'
              156  LOAD_CONST               1
              158  BINARY_SUBSCR    
              160  LOAD_METHOD              append
              162  LOAD_FAST                'temp_split_parse'
              164  CALL_METHOD_1         1  ''
              166  POP_TOP          
              168  JUMP_FORWARD        184  'to 184'
            170_0  COME_FROM           152  '152'

 L.  74       170  LOAD_FAST                'parsed'
              172  LOAD_CONST               0
              174  BINARY_SUBSCR    
              176  LOAD_METHOD              append
              178  LOAD_FAST                'temp_split_parse'
              180  CALL_METHOD_1         1  ''
              182  POP_TOP          
            184_0  COME_FROM           168  '168'

 L.  75       184  LOAD_STR                 ''
              186  STORE_FAST               'temp_split_parse'

 L.  76       188  LOAD_CONST               False
              190  STORE_FAST               'option_state'
              192  JUMP_FORWARD        214  'to 214'
            194_0  COME_FROM           148  '148'
            194_1  COME_FROM           144  '144'

 L.  78       194  LOAD_FAST                'ignore_state'
              196  POP_JUMP_IF_FALSE   210  'to 210'

 L.  79       198  LOAD_FAST                'temp_split_parse'
              200  LOAD_STR                 ' '
              202  INPLACE_ADD      
              204  STORE_FAST               'temp_split_parse'

 L.  80       206  LOAD_CONST               False
              208  STORE_FAST               'ignore_state'
            210_0  COME_FROM           196  '196'

 L.  81       210  LOAD_FAST                'last_letter_space'
              212  POP_JUMP_IF_FALSE   214  'to 214'
            214_0  COME_FROM           212  '212'
            214_1  COME_FROM           192  '192'
            214_2  COME_FROM           140  '140'

 L.  85       214  LOAD_FAST                'letter'
              216  LOAD_STR                 '-'
              218  COMPARE_OP               ==
          220_222  POP_JUMP_IF_FALSE   284  'to 284'

 L.  86       224  LOAD_FAST                'option_state'
              226  POP_JUMP_IF_FALSE   236  'to 236'

 L.  87       228  LOAD_FAST                'temp_split_parse'
              230  LOAD_FAST                'letter'
              232  INPLACE_ADD      
              234  STORE_FAST               'temp_split_parse'
            236_0  COME_FROM           226  '226'

 L.  88       236  LOAD_FAST                'ignore_state'
          238_240  POP_JUMP_IF_TRUE    272  'to 272'
              242  LOAD_FAST                'option_state'
          244_246  POP_JUMP_IF_TRUE    272  'to 272'

 L.  89       248  LOAD_CONST               True
              250  STORE_FAST               'option_state'

 L.  90       252  LOAD_FAST                'parsed'
              254  LOAD_CONST               0
              256  BINARY_SUBSCR    
              258  LOAD_METHOD              append
              260  LOAD_FAST                'temp_split_parse'
              262  CALL_METHOD_1         1  ''
              264  POP_TOP          

 L.  91       266  LOAD_STR                 ''
              268  STORE_FAST               'temp_split_parse'
              270  JUMP_FORWARD        284  'to 284'
            272_0  COME_FROM           244  '244'
            272_1  COME_FROM           238  '238'

 L.  93       272  LOAD_FAST                'temp_split_parse'
              274  LOAD_FAST                'letter'
              276  INPLACE_ADD      
              278  STORE_FAST               'temp_split_parse'

 L.  94       280  LOAD_CONST               False
              282  STORE_FAST               'ignore_state'
            284_0  COME_FROM           270  '270'
            284_1  COME_FROM           220  '220'

 L.  96       284  LOAD_FAST                'letter'
              286  LOAD_STR                 ' '
              288  COMPARE_OP               !=
          290_292  POP_JUMP_IF_FALSE   326  'to 326'
              294  LOAD_FAST                'letter'
              296  LOAD_STR                 '\\'
              298  COMPARE_OP               !=
          300_302  POP_JUMP_IF_FALSE   326  'to 326'
              304  LOAD_FAST                'letter'
              306  LOAD_STR                 '-'
              308  COMPARE_OP               !=
          310_312  POP_JUMP_IF_FALSE   326  'to 326'

 L.  97       314  LOAD_FAST                'temp_split_parse'
              316  LOAD_FAST                'letter'
              318  INPLACE_ADD      
              320  STORE_FAST               'temp_split_parse'

 L.  98       322  LOAD_CONST               False
              324  STORE_FAST               'last_letter_space'
            326_0  COME_FROM           310  '310'
            326_1  COME_FROM           300  '300'
            326_2  COME_FROM           290  '290'

 L. 100       326  LOAD_FAST                'letter_number'
              328  LOAD_CONST               1
              330  INPLACE_ADD      
              332  STORE_FAST               'letter_number'

 L. 101       334  LOAD_FAST                'letter_number'
              336  LOAD_GLOBAL              len
              338  LOAD_FAST                'string'
              340  CALL_FUNCTION_1       1  ''
              342  COMPARE_OP               ==
              344  POP_JUMP_IF_FALSE_BACK    96  'to 96'

 L. 102       346  LOAD_FAST                'temp_split_parse'
              348  LOAD_METHOD              strip
              350  CALL_METHOD_0         0  ''
              352  LOAD_STR                 ''
              354  COMPARE_OP               ==
          356_358  POP_JUMP_IF_TRUE    402  'to 402'

 L. 103       360  LOAD_FAST                'option_state'
          362_364  POP_JUMP_IF_FALSE   382  'to 382'

 L. 104       366  LOAD_FAST                'parsed'
              368  LOAD_CONST               1
              370  BINARY_SUBSCR    
              372  LOAD_METHOD              append
              374  LOAD_FAST                'temp_split_parse'
              376  CALL_METHOD_1         1  ''
              378  POP_TOP          
              380  JUMP_FORWARD        402  'to 402'
            382_0  COME_FROM           362  '362'

 L. 106       382  LOAD_FAST                'parsed'
              384  LOAD_CONST               0
              386  BINARY_SUBSCR    
              388  LOAD_METHOD              append
              390  LOAD_FAST                'temp_split_parse'
              392  CALL_METHOD_1         1  ''
              394  POP_TOP          

 L. 107   396_398  JUMP_FORWARD        402  'to 402'
              400  JUMP_BACK            96  'to 96'
            402_0  COME_FROM           396  '396'
            402_1  COME_FROM           380  '380'
            402_2  COME_FROM           356  '356'

 L. 108       402  LOAD_GLOBAL              len
              404  LOAD_FAST                'parsed'
              406  LOAD_CONST               0
              408  BINARY_SUBSCR    
              410  CALL_FUNCTION_1       1  ''
              412  LOAD_CONST               1
              414  COMPARE_OP               >=
          416_418  POP_JUMP_IF_FALSE   474  'to 474'

 L. 109       420  LOAD_FAST                'parsed'
              422  LOAD_CONST               0
              424  BINARY_SUBSCR    
              426  LOAD_CONST               0
              428  BINARY_SUBSCR    
              430  LOAD_FAST                'parsed'
              432  LOAD_CONST               2
              434  STORE_SUBSCR     

 L. 110       436  LOAD_FAST                'string'
              438  LOAD_GLOBAL              len
              440  LOAD_FAST                'parsed'
              442  LOAD_CONST               0
              444  BINARY_SUBSCR    
              446  LOAD_CONST               0
              448  BINARY_SUBSCR    
              450  CALL_FUNCTION_1       1  ''
              452  LOAD_CONST               None
              454  BUILD_SLICE_2         2 
              456  BINARY_SUBSCR    
              458  LOAD_FAST                'parsed'
              460  LOAD_CONST               3
              462  STORE_SUBSCR     

 L. 111       464  LOAD_FAST                'parsed'
              466  LOAD_CONST               0
              468  BINARY_SUBSCR    
              470  LOAD_CONST               0
              472  DELETE_SUBSCR    
            474_0  COME_FROM           416  '416'

 L. 113       474  LOAD_FAST                'whitelist'
          476_478  POP_JUMP_IF_FALSE   484  'to 484'

 L. 114       480  LOAD_CONST               None
              482  STORE_FAST               'blacklist'
            484_0  COME_FROM           476  '476'

 L. 116       484  LOAD_FAST                'self'
              486  LOAD_ATTR                limitlist_function
          488_490  POP_JUMP_IF_FALSE   560  'to 560'

 L. 117       492  LOAD_FAST                'whitelist'
          494_496  POP_JUMP_IF_FALSE   526  'to 526'

 L. 118       498  LOAD_FAST                'parsed'
              500  LOAD_CONST               2
              502  BINARY_SUBSCR    
              504  LOAD_FAST                'whitelist'
              506  COMPARE_OP               not-in
          508_510  POP_JUMP_IF_FALSE   526  'to 526'

 L. 119       512  LOAD_FAST                'self'
              514  LOAD_METHOD              limitlist_function
              516  LOAD_FAST                'parsed'
              518  CALL_METHOD_1         1  ''
              520  POP_TOP          

 L. 120       522  LOAD_FAST                'parsed'
              524  RETURN_VALUE     
            526_0  COME_FROM           508  '508'
            526_1  COME_FROM           494  '494'

 L. 123       526  LOAD_FAST                'blacklist'
          528_530  POP_JUMP_IF_FALSE   560  'to 560'

 L. 124       532  LOAD_FAST                'parsed'
              534  LOAD_CONST               2
              536  BINARY_SUBSCR    
              538  LOAD_FAST                'blacklist'
              540  COMPARE_OP               in
          542_544  POP_JUMP_IF_FALSE   560  'to 560'

 L. 125       546  LOAD_FAST                'self'
              548  LOAD_METHOD              limitlist_function
              550  LOAD_FAST                'parsed'
              552  CALL_METHOD_1         1  ''
              554  POP_TOP          

 L. 126       556  LOAD_FAST                'parsed'
              558  RETURN_VALUE     
            560_0  COME_FROM           542  '542'
            560_1  COME_FROM           528  '528'
            560_2  COME_FROM           488  '488'

 L. 128       560  LOAD_FAST                'self'
              562  LOAD_ATTR                limitlist_function
          564_566  POP_JUMP_IF_TRUE    616  'to 616'

 L. 129       568  LOAD_FAST                'whitelist'
          570_572  POP_JUMP_IF_FALSE   592  'to 592'

 L. 130       574  LOAD_FAST                'parsed'
              576  LOAD_CONST               2
              578  BINARY_SUBSCR    
              580  LOAD_FAST                'whitelist'
              582  COMPARE_OP               not-in
          584_586  POP_JUMP_IF_FALSE   592  'to 592'

 L. 131       588  LOAD_FAST                'parsed'
              590  RETURN_VALUE     
            592_0  COME_FROM           584  '584'
            592_1  COME_FROM           570  '570'

 L. 134       592  LOAD_FAST                'blacklist'
          594_596  POP_JUMP_IF_FALSE   616  'to 616'

 L. 135       598  LOAD_FAST                'parsed'
              600  LOAD_CONST               2
              602  BINARY_SUBSCR    
              604  LOAD_FAST                'blacklist'
              606  COMPARE_OP               in
          608_610  POP_JUMP_IF_FALSE   616  'to 616'

 L. 136       612  LOAD_FAST                'parsed'
              614  RETURN_VALUE     
            616_0  COME_FROM           608  '608'
            616_1  COME_FROM           594  '594'
            616_2  COME_FROM           564  '564'

 L. 139       616  LOAD_FAST                'self'
              618  LOAD_ATTR                command_bindings
              620  GET_ITER         
            622_0  COME_FROM           808  '808'
            622_1  COME_FROM           640  '640'
              622  FOR_ITER            812  'to 812'
              624  STORE_FAST               'command_binding'

 L. 141       626  LOAD_FAST                'parsed'
              628  LOAD_CONST               2
              630  BINARY_SUBSCR    
              632  LOAD_FAST                'command_binding'
              634  LOAD_CONST               2
              636  BINARY_SUBSCR    
              638  COMPARE_OP               ==
          640_642  POP_JUMP_IF_FALSE_BACK   622  'to 622'

 L. 142       644  LOAD_FAST                'command_binding'
              646  LOAD_CONST               0
              648  BINARY_SUBSCR    
          650_652  POP_JUMP_IF_FALSE   752  'to 752'

 L. 143       654  SETUP_FINALLY       678  'to 678'

 L. 144       656  LOAD_FAST                'command_binding'
              658  LOAD_CONST               1
              660  BINARY_SUBSCR    
              662  LOAD_FAST                'parsed'
              664  LOAD_FAST                'command_binding'
              666  LOAD_CONST               0
              668  BINARY_SUBSCR    
              670  CALL_FUNCTION_2       2  ''
              672  POP_TOP          
              674  POP_BLOCK        
              676  JUMP_FORWARD        750  'to 750'
            678_0  COME_FROM_FINALLY   654  '654'

 L. 145       678  DUP_TOP          
              680  LOAD_GLOBAL              Exception
              682  COMPARE_OP               exception-match
          684_686  POP_JUMP_IF_FALSE   748  'to 748'
              688  POP_TOP          
              690  POP_TOP          
              692  POP_TOP          

 L. 146       694  SETUP_FINALLY       712  'to 712'

 L. 147       696  LOAD_FAST                'command_binding'
              698  LOAD_CONST               1
              700  BINARY_SUBSCR    
              702  LOAD_FAST                'parsed'
              704  CALL_FUNCTION_1       1  ''
              706  POP_TOP          
              708  POP_BLOCK        
              710  JUMP_FORWARD        744  'to 744'
            712_0  COME_FROM_FINALLY   694  '694'

 L. 148       712  DUP_TOP          
              714  LOAD_GLOBAL              Exception
              716  COMPARE_OP               exception-match
          718_720  POP_JUMP_IF_FALSE   742  'to 742'
              722  POP_TOP          
              724  POP_TOP          
              726  POP_TOP          

 L. 149       728  LOAD_FAST                'command_binding'
              730  LOAD_CONST               1
              732  BINARY_SUBSCR    
              734  CALL_FUNCTION_0       0  ''
              736  POP_TOP          
              738  POP_EXCEPT       
              740  JUMP_FORWARD        744  'to 744'
            742_0  COME_FROM           718  '718'
              742  END_FINALLY      
            744_0  COME_FROM           740  '740'
            744_1  COME_FROM           710  '710'
              744  POP_EXCEPT       
              746  JUMP_FORWARD        750  'to 750'
            748_0  COME_FROM           684  '684'
              748  END_FINALLY      
            750_0  COME_FROM           746  '746'
            750_1  COME_FROM           676  '676'
              750  JUMP_FORWARD        802  'to 802'
            752_0  COME_FROM           650  '650'

 L. 151       752  SETUP_FINALLY       770  'to 770'

 L. 152       754  LOAD_FAST                'command_binding'
              756  LOAD_CONST               1
              758  BINARY_SUBSCR    
              760  LOAD_FAST                'parsed'
              762  CALL_FUNCTION_1       1  ''
              764  POP_TOP          
              766  POP_BLOCK        
              768  JUMP_FORWARD        802  'to 802'
            770_0  COME_FROM_FINALLY   752  '752'

 L. 153       770  DUP_TOP          
              772  LOAD_GLOBAL              Exception
              774  COMPARE_OP               exception-match
          776_778  POP_JUMP_IF_FALSE   800  'to 800'
              780  POP_TOP          
              782  POP_TOP          
              784  POP_TOP          

 L. 154       786  LOAD_FAST                'command_binding'
              788  LOAD_CONST               1
              790  BINARY_SUBSCR    
              792  CALL_FUNCTION_0       0  ''
              794  POP_TOP          
              796  POP_EXCEPT       
              798  JUMP_FORWARD        802  'to 802'
            800_0  COME_FROM           776  '776'
              800  END_FINALLY      
            802_0  COME_FROM           798  '798'
            802_1  COME_FROM           768  '768'
            802_2  COME_FROM           750  '750'

 L. 155       802  POP_TOP          
              804  LOAD_CONST               False
              806  RETURN_VALUE     
          808_810  JUMP_BACK           622  'to 622'
            812_0  COME_FROM           622  '622'

 L. 156       812  LOAD_FAST                'parsed'
              814  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 814

    def bind_command(self, command, call_function, call_function_param=None):
        if call_function_param == None:
            param_driven = False
        else:
            param_driven = str(call_function_param)
        self.command_bindings.append[param_driven, call_function, str(command)]

    def set_limit_list_function(self, function):
        self.limitlist_function = function

    def set_load_print_pipe(self, print_function):
        self.load_defines['print'] = print_function

    def set_load_input_pipe(self, input_function):
        self.load_defines['input'] = input_function

    def set_extension_print_pipe(self, print_function):
        self.extension_defines['print'] = print_function

    def set_extension_input_pipe(self, input_function):
        self.extension_defines['input'] = input_function

    def extension_define(self, string, function):
        self.extension_defines[str(string)] = function

    def extension_define_delete(self, string):
        try:
            del self.extension_defines[str(string)]
        except Exception:
            pass

    def load_define(self, string, function):
        self.load_defines[str(string)] = function

    def load_define_delete(self, string, function):
        try:
            del self.load_defines[str(string)]
        except Exception:
            pass

    def create_extension(self, callsign, string, call_enable=True):
        self.extensions.append[str(callsign), str(string)]
        if call_enable:
            self.bind_command(str(callsign), self._internal_extension_loader, str(callsign))

    def delete_extension(self, callsign):
        for extension in range(len(self.extensions)):
            if self.extensions[extension][0] == str(callsign):
                del self.extensions[extension]
                return None

    def clear_extensions(self):
        self.extensions = []

    def create_appfile(self, name, string, loadable=True):
        self.appfiles.append[str(name), str(string), bool(loadable)]

    def delete_appfile(self, name):
        for appfile in range(len(self.appfiles)):
            if self.appfiles[appfile][0] == str(name):
                del self.appfiles[appfile]
                return None

    def clear_appfiles(self):
        self.appfiles = []

    def run_extension(self, callsign, args=None, print_pipe=None, input_pipe=None, other_redefinitions=None):
        if args == None:
            args = [[], [], str(callsign), '']
        extension_definitions = self.extension_defines
        extension_definitions['args'] = args
        if print_pipe:
            extension_definitions['print'] = print_pipe
        if input_pipe:
            extension_definitions['input'] = input_pipe
        if other_redefinitions:
            extension_definitions += other_redefinitions
        for extension in self.extensions:
            if extension[0] == str(callsign):
                exec(extension[1], extension_definitions)

    def run_appfile(self, name, print_pipe=None, input_pipe=None, other_redefinitions=None):
        load_definitions = self.load_defines
        if print_pipe:
            load_definitions['print'] = print_pipe
        if input_pipe:
            load_definitions['input'] = input_pipe
        if other_redefinitions:
            load_definitions += other_redefinitions
        for appfile in self.appfiles:
            if appfile[0] == str(name):
                if appfile[2]:
                    exec(appfile[1], load_definitions)
                    return True
                else:
                    return False
        else:
            return False

    def set_defaults(self):
        self.extension_defines['print'] = print
        self.extension_defines['input'] = input
        self.load_defines['print'] = print
        self.load_defines['input'] = input

    def _internal_extension_loader(self, args, param):
        self.run_extension(param, args)

    def _default_appfile_loader(self, args):
        try:
            self.run_appfileargs[0][0]
        except Exception:
            pass


fang = FangCore

class FangCoreTerminal:
    __doc__ = '\n\tFangTerminal protocol\n\t5|priHello\n\t5|inpHello\n\t5|retHello\n\t14|redlocalhost 9000\n\t0|clr\n\t0|cte\n\t0|cre\n\t0|cls\n\t0|rfi\n\t0|refdata\n\t0|nre\n\t0|sfiname data\n\t'

    def __init__(self, IP, Port, listener_max=10):
        self.IP = IP
        self.port = Port
        self.request_buffer = []
        self.max_listen = listener_max

    def start_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(self.IP, self.port)
        self.server.listenself.max_listen

    def close_server(self):
        self.server.shutdownsocket.SHUT_RDWR
        self.server.close

    def await_connection--- This code section failed: ---

 L. 315         0  LOAD_FAST                'timeout'
                2  POP_JUMP_IF_FALSE    16  'to 16'

 L. 316         4  LOAD_FAST                'self'
                6  LOAD_ATTR                server
                8  LOAD_METHOD              settimeout
               10  LOAD_FAST                'timeout'
               12  CALL_METHOD_1         1  ''
               14  POP_TOP          
             16_0  COME_FROM             2  '2'

 L. 318        16  SETUP_FINALLY        44  'to 44'

 L. 319        18  LOAD_FAST                'self'
               20  LOAD_ATTR                server
               22  LOAD_METHOD              accept
               24  CALL_METHOD_0         0  ''
               26  UNPACK_SEQUENCE_2     2 
               28  STORE_FAST               'client'
               30  STORE_FAST               'address'

 L. 320        32  LOAD_GLOBAL              _Fang_Terminal_Server_Client
               34  LOAD_FAST                'client'
               36  LOAD_FAST                'address'
               38  CALL_FUNCTION_2       2  ''
               40  POP_BLOCK        
               42  RETURN_VALUE     
             44_0  COME_FROM_FINALLY    16  '16'

 L. 321        44  DUP_TOP          
               46  LOAD_GLOBAL              Exception
               48  COMPARE_OP               exception-match
               50  POP_JUMP_IF_FALSE    64  'to 64'
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          

 L. 322        58  POP_EXCEPT       
               60  LOAD_CONST               False
               62  RETURN_VALUE     
             64_0  COME_FROM            50  '50'
               64  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 60


class _Fang_Terminal_Server_Client:

    def __init__(self, client, address):
        self.client = client
        self.address = address
        self.connection_open = True

    def print(self, string):
        string = str(string)
        try:
            self.client.sendallstr(str(len(string)) + '|pri' + string).encode
        except Exception:
            self.connection_open = False

    def input--- This code section failed: ---

 L. 339         0  LOAD_FAST                'self'
                2  LOAD_METHOD              send
                4  LOAD_GLOBAL              str
                6  LOAD_GLOBAL              len
                8  LOAD_FAST                'string'
               10  CALL_FUNCTION_1       1  ''
               12  CALL_FUNCTION_1       1  ''
               14  LOAD_STR                 '|inp'
               16  BINARY_ADD       
               18  LOAD_GLOBAL              str
               20  LOAD_FAST                'string'
               22  CALL_FUNCTION_1       1  ''
               24  BINARY_ADD       
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          

 L. 340        30  SETUP_FINALLY       244  'to 244'

 L. 341        32  LOAD_FAST                'timeout'
               34  POP_JUMP_IF_FALSE   158  'to 158'

 L. 342        36  SETUP_FINALLY       130  'to 130'

 L. 343        38  LOAD_STR                 ''
               40  STORE_FAST               'number'
             42_0  COME_FROM            74  '74'
             42_1  COME_FROM            64  '64'

 L. 345        42  LOAD_FAST                'self'
               44  LOAD_METHOD              recv
               46  LOAD_CONST               1
               48  LOAD_FAST                'timeout'
               50  CALL_METHOD_2         2  ''
               52  STORE_FAST               'rec'

 L. 346        54  LOAD_FAST                'rec'
               56  LOAD_STR                 '|'
               58  COMPARE_OP               ==
               60  POP_JUMP_IF_FALSE    66  'to 66'

 L. 347        62  JUMP_FORWARD         76  'to 76'
               64  JUMP_BACK            42  'to 42'
             66_0  COME_FROM            60  '60'

 L. 349        66  LOAD_FAST                'number'
               68  LOAD_FAST                'rec'
               70  INPLACE_ADD      
               72  STORE_FAST               'number'
               74  JUMP_BACK            42  'to 42'
             76_0  COME_FROM            62  '62'

 L. 350        76  LOAD_FAST                'self'
               78  LOAD_METHOD              recv
               80  LOAD_CONST               3
               82  CALL_METHOD_1         1  ''
               84  LOAD_STR                 'ret'
               86  COMPARE_OP               ==
               88  POP_JUMP_IF_FALSE   108  'to 108'

 L. 351        90  LOAD_FAST                'self'
               92  LOAD_METHOD              recv
               94  LOAD_GLOBAL              int
               96  LOAD_FAST                'number'
               98  CALL_FUNCTION_1       1  ''
              100  CALL_METHOD_1         1  ''
              102  POP_BLOCK        
              104  POP_BLOCK        
              106  RETURN_VALUE     
            108_0  COME_FROM            88  '88'

 L. 353       108  LOAD_FAST                'self'
              110  LOAD_METHOD              recv
              112  LOAD_FAST                'number'
              114  CALL_METHOD_1         1  ''
              116  POP_TOP          

 L. 354       118  POP_BLOCK        
              120  POP_BLOCK        
              122  LOAD_STR                 ''
              124  RETURN_VALUE     
              126  POP_BLOCK        
              128  JUMP_FORWARD        240  'to 240'
            130_0  COME_FROM_FINALLY    36  '36'

 L. 355       130  DUP_TOP          
              132  LOAD_GLOBAL              socket
              134  LOAD_ATTR                timeout
              136  COMPARE_OP               exception-match
              138  POP_JUMP_IF_FALSE   154  'to 154'
              140  POP_TOP          
              142  POP_TOP          
              144  POP_TOP          

 L. 356       146  POP_EXCEPT       
              148  POP_BLOCK        
              150  LOAD_CONST               False
              152  RETURN_VALUE     
            154_0  COME_FROM           138  '138'
              154  END_FINALLY      
              156  JUMP_FORWARD        240  'to 240'
            158_0  COME_FROM            34  '34'

 L. 358       158  LOAD_STR                 ''
              160  STORE_FAST               'number'
            162_0  COME_FROM           192  '192'
            162_1  COME_FROM           182  '182'

 L. 360       162  LOAD_FAST                'self'
              164  LOAD_METHOD              recv
              166  LOAD_CONST               1
              168  CALL_METHOD_1         1  ''
              170  STORE_FAST               'rec'

 L. 361       172  LOAD_FAST                'rec'
              174  LOAD_STR                 '|'
              176  COMPARE_OP               ==
              178  POP_JUMP_IF_FALSE   184  'to 184'

 L. 362       180  JUMP_FORWARD        194  'to 194'
              182  JUMP_BACK           162  'to 162'
            184_0  COME_FROM           178  '178'

 L. 364       184  LOAD_FAST                'number'
              186  LOAD_FAST                'rec'
              188  INPLACE_ADD      
              190  STORE_FAST               'number'
              192  JUMP_BACK           162  'to 162'
            194_0  COME_FROM           180  '180'

 L. 365       194  LOAD_FAST                'self'
              196  LOAD_METHOD              recv
              198  LOAD_CONST               3
              200  CALL_METHOD_1         1  ''
              202  LOAD_STR                 'ret'
              204  COMPARE_OP               ==
              206  POP_JUMP_IF_FALSE   224  'to 224'

 L. 366       208  LOAD_FAST                'self'
              210  LOAD_METHOD              recv
              212  LOAD_GLOBAL              int
              214  LOAD_FAST                'number'
              216  CALL_FUNCTION_1       1  ''
              218  CALL_METHOD_1         1  ''
              220  POP_BLOCK        
              222  RETURN_VALUE     
            224_0  COME_FROM           206  '206'

 L. 368       224  LOAD_FAST                'self'
              226  LOAD_METHOD              recv
              228  LOAD_FAST                'number'
              230  CALL_METHOD_1         1  ''
              232  POP_TOP          

 L. 369       234  POP_BLOCK        
              236  LOAD_STR                 ''
              238  RETURN_VALUE     
            240_0  COME_FROM           156  '156'
            240_1  COME_FROM           128  '128'
              240  POP_BLOCK        
              242  JUMP_FORWARD        274  'to 274'
            244_0  COME_FROM_FINALLY    30  '30'

 L. 370       244  DUP_TOP          
              246  LOAD_GLOBAL              TypeError
              248  COMPARE_OP               exception-match
          250_252  POP_JUMP_IF_FALSE   272  'to 272'
              254  POP_TOP          
              256  POP_TOP          
              258  POP_TOP          

 L. 371       260  LOAD_CONST               False
              262  LOAD_FAST                'self'
              264  STORE_ATTR               connection_open

 L. 372       266  POP_EXCEPT       
              268  LOAD_CONST               False
              270  RETURN_VALUE     
            272_0  COME_FROM           250  '250'
              272  END_FINALLY      
            274_0  COME_FROM           242  '242'

Parse error at or near `POP_BLOCK' instruction at offset 104

    def clear(self):
        self.send'0|clr'

    def redirect(self, IP, port):
        sended = str(IP) + ' ' + str(port)
        self.send(str(len(sended)) + '|red' + sended)

    def request_file--- This code section failed: ---

 L. 383         0  LOAD_FAST                'self'
                2  LOAD_METHOD              send
                4  LOAD_STR                 '0|rfi'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 384     10_12  SETUP_FINALLY       272  'to 272'

 L. 385        14  LOAD_FAST                'timeout'
               16  POP_JUMP_IF_FALSE   162  'to 162'

 L. 386        18  SETUP_FINALLY       134  'to 134'

 L. 387        20  LOAD_STR                 ''
               22  STORE_FAST               'number'
             24_0  COME_FROM            56  '56'
             24_1  COME_FROM            46  '46'

 L. 389        24  LOAD_FAST                'self'
               26  LOAD_METHOD              recv
               28  LOAD_CONST               1
               30  LOAD_FAST                'timeout'
               32  CALL_METHOD_2         2  ''
               34  STORE_FAST               'rec'

 L. 390        36  LOAD_FAST                'rec'
               38  LOAD_STR                 '|'
               40  COMPARE_OP               ==
               42  POP_JUMP_IF_FALSE    48  'to 48'

 L. 391        44  JUMP_FORWARD         58  'to 58'
               46  JUMP_BACK            24  'to 24'
             48_0  COME_FROM            42  '42'

 L. 393        48  LOAD_FAST                'number'
               50  LOAD_FAST                'rec'
               52  INPLACE_ADD      
               54  STORE_FAST               'number'
               56  JUMP_BACK            24  'to 24'
             58_0  COME_FROM            44  '44'

 L. 394        58  LOAD_FAST                'self'
               60  LOAD_METHOD              recv
               62  LOAD_CONST               3
               64  CALL_METHOD_1         1  ''
               66  LOAD_STR                 'ref'
               68  COMPARE_OP               ==
               70  POP_JUMP_IF_FALSE   110  'to 110'

 L. 395        72  LOAD_FAST                'self'
               74  LOAD_ATTR                client
               76  LOAD_METHOD              recv
               78  LOAD_GLOBAL              int
               80  LOAD_FAST                'number'
               82  CALL_FUNCTION_1       1  ''
               84  CALL_METHOD_1         1  ''
               86  STORE_FAST               'recved'

 L. 396        88  LOAD_FAST                'recved'
               90  POP_JUMP_IF_TRUE    100  'to 100'

 L. 397        92  POP_BLOCK        
               94  POP_BLOCK        
               96  LOAD_CONST               False
               98  RETURN_VALUE     
            100_0  COME_FROM            90  '90'

 L. 399       100  LOAD_FAST                'recved'
              102  POP_BLOCK        
              104  POP_BLOCK        
              106  RETURN_VALUE     
              108  JUMP_FORWARD        130  'to 130'
            110_0  COME_FROM            70  '70'

 L. 401       110  LOAD_FAST                'self'
              112  LOAD_ATTR                client
              114  LOAD_METHOD              recv
              116  LOAD_FAST                'number'
              118  CALL_METHOD_1         1  ''
              120  POP_TOP          

 L. 402       122  POP_BLOCK        
              124  POP_BLOCK        
              126  LOAD_CONST               False
              128  RETURN_VALUE     
            130_0  COME_FROM           108  '108'
              130  POP_BLOCK        
              132  JUMP_FORWARD        160  'to 160'
            134_0  COME_FROM_FINALLY    18  '18'

 L. 403       134  DUP_TOP          
              136  LOAD_GLOBAL              socket
              138  LOAD_ATTR                timeout
              140  COMPARE_OP               exception-match
              142  POP_JUMP_IF_FALSE   158  'to 158'
              144  POP_TOP          
              146  POP_TOP          
              148  POP_TOP          

 L. 404       150  POP_EXCEPT       
              152  POP_BLOCK        
              154  LOAD_CONST               False
              156  RETURN_VALUE     
            158_0  COME_FROM           142  '142'
              158  END_FINALLY      
            160_0  COME_FROM           132  '132'
              160  JUMP_FORWARD        268  'to 268'
            162_0  COME_FROM            16  '16'

 L. 406       162  LOAD_STR                 ''
              164  STORE_FAST               'number'
            166_0  COME_FROM           198  '198'
            166_1  COME_FROM           188  '188'

 L. 408       166  LOAD_FAST                'self'
              168  LOAD_METHOD              recv
              170  LOAD_CONST               1
              172  LOAD_FAST                'timeout'
              174  CALL_METHOD_2         2  ''
              176  STORE_FAST               'rec'

 L. 409       178  LOAD_FAST                'rec'
              180  LOAD_STR                 '|'
              182  COMPARE_OP               ==
              184  POP_JUMP_IF_FALSE   190  'to 190'

 L. 410       186  JUMP_FORWARD        200  'to 200'
              188  JUMP_BACK           166  'to 166'
            190_0  COME_FROM           184  '184'

 L. 412       190  LOAD_FAST                'number'
              192  LOAD_FAST                'rec'
              194  INPLACE_ADD      
              196  STORE_FAST               'number'
              198  JUMP_BACK           166  'to 166'
            200_0  COME_FROM           186  '186'

 L. 413       200  LOAD_FAST                'self'
              202  LOAD_METHOD              recv
              204  LOAD_CONST               3
              206  CALL_METHOD_1         1  ''
              208  LOAD_STR                 'ref'
              210  COMPARE_OP               ==
          212_214  POP_JUMP_IF_FALSE   250  'to 250'

 L. 414       216  LOAD_FAST                'self'
              218  LOAD_ATTR                client
              220  LOAD_METHOD              recv
              222  LOAD_GLOBAL              int
              224  LOAD_FAST                'number'
              226  CALL_FUNCTION_1       1  ''
              228  CALL_METHOD_1         1  ''
              230  STORE_FAST               'recved'

 L. 415       232  LOAD_FAST                'recved'
              234  POP_JUMP_IF_TRUE    242  'to 242'

 L. 416       236  POP_BLOCK        
              238  LOAD_CONST               False
              240  RETURN_VALUE     
            242_0  COME_FROM           234  '234'

 L. 418       242  LOAD_FAST                'recved'
              244  POP_BLOCK        
              246  RETURN_VALUE     
              248  JUMP_FORWARD        268  'to 268'
            250_0  COME_FROM           212  '212'

 L. 420       250  LOAD_FAST                'self'
              252  LOAD_ATTR                client
              254  LOAD_METHOD              recv
              256  LOAD_FAST                'number'
              258  CALL_METHOD_1         1  ''
              260  POP_TOP          

 L. 421       262  POP_BLOCK        
              264  LOAD_CONST               False
              266  RETURN_VALUE     
            268_0  COME_FROM           248  '248'
            268_1  COME_FROM           160  '160'
              268  POP_BLOCK        
              270  JUMP_FORWARD        302  'to 302'
            272_0  COME_FROM_FINALLY    10  '10'

 L. 422       272  DUP_TOP          
              274  LOAD_GLOBAL              TypeError
              276  COMPARE_OP               exception-match
          278_280  POP_JUMP_IF_FALSE   300  'to 300'
              282  POP_TOP          
              284  POP_TOP          
              286  POP_TOP          

 L. 423       288  LOAD_CONST               False
              290  LOAD_FAST                'self'
              292  STORE_ATTR               connection_open

 L. 424       294  POP_EXCEPT       
              296  LOAD_CONST               False
              298  RETURN_VALUE     
            300_0  COME_FROM           278  '278'
              300  END_FINALLY      
            302_0  COME_FROM           270  '270'

Parse error at or near `POP_BLOCK' instruction at offset 94

    def close(self):
        self.send'0|cls'
        self.client.close
        self.connection_open = False

    def get_address(self):
        return self.address

    def test_connection--- This code section failed: ---

 L. 438         0  LOAD_FAST                'self'
                2  LOAD_METHOD              send
                4  LOAD_STR                 '0|cte'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 439        10  LOAD_FAST                'timeout'
               12  POP_JUMP_IF_FALSE    26  'to 26'

 L. 440        14  LOAD_FAST                'self'
               16  LOAD_ATTR                client
               18  LOAD_METHOD              settimeout
               20  LOAD_FAST                'timeout'
               22  CALL_METHOD_1         1  ''
               24  POP_TOP          
             26_0  COME_FROM            12  '12'

 L. 441        26  SETUP_FINALLY        68  'to 68'

 L. 442        28  LOAD_FAST                'self'
               30  LOAD_ATTR                client
               32  LOAD_METHOD              recv
               34  LOAD_CONST               5
               36  CALL_METHOD_1         1  ''
               38  LOAD_METHOD              decode
               40  CALL_METHOD_0         0  ''
               42  LOAD_METHOD              strip
               44  CALL_METHOD_0         0  ''
               46  LOAD_STR                 '0|cre'
               48  COMPARE_OP               ==
               50  POP_JUMP_IF_FALSE    58  'to 58'

 L. 443        52  POP_BLOCK        
               54  LOAD_CONST               True
               56  RETURN_VALUE     
             58_0  COME_FROM            50  '50'

 L. 445        58  POP_BLOCK        
               60  LOAD_CONST               False
               62  RETURN_VALUE     
               64  POP_BLOCK        
               66  JUMP_FORWARD        112  'to 112'
             68_0  COME_FROM_FINALLY    26  '26'

 L. 446        68  DUP_TOP          
               70  LOAD_GLOBAL              socket
               72  LOAD_ATTR                timeout
               74  COMPARE_OP               exception-match
               76  POP_JUMP_IF_FALSE    90  'to 90'
               78  POP_TOP          
               80  POP_TOP          
               82  POP_TOP          

 L. 447        84  POP_EXCEPT       
               86  LOAD_CONST               False
               88  RETURN_VALUE     
             90_0  COME_FROM            76  '76'

 L. 449        90  DUP_TOP          
               92  LOAD_GLOBAL              Exception
               94  COMPARE_OP               exception-match
               96  POP_JUMP_IF_FALSE   110  'to 110'
               98  POP_TOP          
              100  POP_TOP          
              102  POP_TOP          

 L. 450       104  POP_EXCEPT       
              106  LOAD_CONST               False
              108  RETURN_VALUE     
            110_0  COME_FROM            96  '96'

 L. 451       110  END_FINALLY      
            112_0  COME_FROM            66  '66'

Parse error at or near `LOAD_CONST' instruction at offset 54

    def connection_status(self):
        return self.connection_open

    def send(self, string):
        try:
            self.client.sendallstr(string).encode
        except Exception:
            self.connection_open = False

    def recv(self, number, timeout=None):
        if timeout:
            self.client.settimeouttimeout
        recieved = None
        try:
            recieved = self.client.recvnumber
        except socket.timeout:
            return False
        except Exception:
            pass
        else:
            if not recieved:
                self.connection_open = False
                return False
            return recieved.decode


class FangCoreTerminalClient:
    __doc__ = '\n\tFangTerminal protocol\n\t5|priHello\n\t5|inpHello\n\t5|retHello\n\t14|redlocalhost 9000\n\t0|clr\n\t0|cte\n\t0|cre\n\t0|cls\n\t'

    def __init__(self):
        self.print_method = self._placeholder_method
        self.input_method = self._placeholder_method
        self.clear_method = self._placeholder_method
        self.file_request_method = self._placeholder_method
        self.connected_ip = None
        self.connected_port = None
        self.client = None
        self.connected = False
        self.connection_handler = threading.Thread(target=(self._backround_connection_handler))

    def connect--- This code section failed: ---

 L. 503         0  SETUP_FINALLY        78  'to 78'

 L. 504         2  LOAD_GLOBAL              socket
                4  LOAD_METHOD              socket
                6  LOAD_GLOBAL              socket
                8  LOAD_ATTR                AF_INET
               10  LOAD_GLOBAL              socket
               12  LOAD_ATTR                SOCK_STREAM
               14  CALL_METHOD_2         2  ''
               16  LOAD_FAST                'self'
               18  STORE_ATTR               client

 L. 505        20  LOAD_FAST                'self'
               22  LOAD_ATTR                client
               24  LOAD_METHOD              connect
               26  LOAD_FAST                'IP'
               28  LOAD_GLOBAL              int
               30  LOAD_FAST                'port'
               32  CALL_FUNCTION_1       1  ''
               34  BUILD_TUPLE_2         2 
               36  CALL_METHOD_1         1  ''
               38  POP_TOP          

 L. 506        40  LOAD_FAST                'IP'
               42  LOAD_FAST                'self'
               44  STORE_ATTR               connected_ip

 L. 507        46  LOAD_GLOBAL              int
               48  LOAD_FAST                'port'
               50  CALL_FUNCTION_1       1  ''
               52  LOAD_FAST                'self'
               54  STORE_ATTR               connected_port

 L. 508        56  LOAD_CONST               True
               58  LOAD_FAST                'self'
               60  STORE_ATTR               connected

 L. 509        62  LOAD_FAST                'self'
               64  LOAD_ATTR                connection_handler
               66  LOAD_METHOD              start
               68  CALL_METHOD_0         0  ''
               70  POP_TOP          

 L. 510        72  POP_BLOCK        
               74  LOAD_CONST               True
               76  RETURN_VALUE     
             78_0  COME_FROM_FINALLY     0  '0'

 L. 511        78  DUP_TOP          
               80  LOAD_GLOBAL              Exception
               82  COMPARE_OP               exception-match
               84  POP_JUMP_IF_FALSE    98  'to 98'
               86  POP_TOP          
               88  POP_TOP          
               90  POP_TOP          

 L. 512        92  POP_EXCEPT       
               94  LOAD_CONST               False
               96  RETURN_VALUE     
             98_0  COME_FROM            84  '84'
               98  END_FINALLY      

Parse error at or near `DUP_TOP' instruction at offset 78

    def disconnect(self):
        self.client.close
        self.connected_ip = None
        self.connected_port = None
        self.connected = False

    def connection_status(self):
        return self.connected

    def set_print_method(self, function):
        self.print_method = function

    def set_input_method(self, function):
        self.input_method = function

    def set_clear_method(self, function):
        self.clear_method = function

    def set_file_request_method(self, function):
        self.file_request_method = function

    def _backround_connection_handler(self):
        while True:
            if self.connected:
                try:
                    number = 0
                    while True:
                        while True:
                            val = self.client.recv1.decode
                            if val == '|':
                                pass

                        number = int(str(number) + val)

                    keyword = self.client.recv3.decode
                    message = self.client.recvnumber.decode
                    if keyword == 'pri':
                        self.print_methodmessage
                    if keyword == 'inp':
                        returner = str(self.input_methodmessage)
                        self.client.sendallstr(str(len(returner)) + '|ret' + returner).encode
                    if keyword == 'clr':
                        self.clear_method
                    if keyword == 'cte':
                        self.client.sendallb'0|cre'
                    if keyword == 'cls':
                        self.connected = False
                        self.connected_ip = None
                        self.connected_port = None
                        self.client.close
                        break
                    if keyword == 'red':
                        self.disconnect
                        self.connect(message.split[0], int(message.split[1]))
                    if keyword == 'rfi':
                        returner = self.file_request_method
                        if not returner:
                            returner = b''
                        message = str(str(len(returner)) + '|ref').encode + returner
                        self.client.sendallmessage
                except ConnectionResetError:
                    self.connected = False
                    self.connected_ip = None
                    self.connected_port = None
                    break

    def _placeholder_method(self, *args):
        pass


class HTTPServer:

    def __init__(self):
        self.http_ip = None
        self.http_port = None
        self.http_sock = None
        self.http_running = False
        self.http_awaiting_connections = []
        self.response_method = None
        self.https_ip = None
        self.https_port = None
        self.https_esock = None
        self.https_sock = None
        self.https_running = False
        self.https_certchain = None
        self.https_private_key = None
        self.https_ssl_context = None
        self.https_awaiting_connections = []

    def set_response_method(self, method):
        self.response_method = method

    def start_http_server(self, IP, port, service_threads=1, listen=10, recv_max=8192, buffer=False, reuse_socket=True):
        if not buffer:
            buffer = recv_max
        self.http_ip = str(IP)
        self.http_port = int(port)
        self.http_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if reuse_socket:
            self.http_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.http_sock.bind(self.http_ip, self.http_port)
        self.http_sock.listenint(listen)
        self.http_running = True
        self.current_id = 0
        thread = threading.Thread(target=(self._http_connection_handler))
        thread.start
        for iden in range(int(service_threads)):
            thread = threading.Thread(target=(self._http_connection_servicer), args=(iden, service_threads - 1, recv_max, buffer))
            thread.start

    def stop_http_server(self):
        self.http_running = False

    def start_https_server(self, IP, port, certchain, private_key, ciphers, service_threads=1, listen=10, recv_max=8192, buffer=False, reuse_socket=True):
        if not buffer:
            buffer = recv_max
        if certchain:
            if private_key:
                self.https_certchain = certchain
                self.https_private_key = private_key
        self.https_ip = str(IP)
        self.https_port = int(port)
        self.https_esock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.https_esock.bind(self.https_ip, self.https_port)
        self.https_esock.listenint(listen)
        self.https_sock = ssl.wrap_socket((self.https_esock), server_side=True, ciphers=ciphers, keyfile=private_key, certfile=certchain)
        self.https_running = True
        self.current_id = 0
        thread = threading.Thread(target=(self._https_connection_handler))
        thread.start
        for iden in range(int(service_threads)):
            thread = threading.Thread(target=(self._https_connection_servicer), args=(iden, service_threads - 1, recv_max, buffer))
            thread.start

    def stop_https_server(self):
        self.https_running = False

    def _https_connection_handler(self):
        while True:
            if self.https_running:
                client, address = self.https_sock.accept
                self.https_awaiting_connections.append[client, address]

    def _https_connection_servicer(self, iden, max_id, max_recv, buffer):
        while True:
            if self.https_running:
                send = True
            else:
                while len(self.https_awaiting_connections) == 0 or self.current_id != iden:
                    if not self.https_running:
                        return

                try:
                    current = self.https_awaiting_connections[0]
                    del self.https_awaiting_connections[0]
                except Exception:
                    send = False
                else:
                    if self.current_id == max_id:
                        self.current_id = -1
                    else:
                        self.current_id += 1
                    if send:
                        try:
                            client_obj = _HTTP_client(current[1], current[0], 'HTTP', max_recv, buffer)
                            self.response_methodclient_obj
                            current[0].sendclient_obj._render_page
                            current[0].close
                        except Exception:
                            pass

    def _http_connection_handler(self):
        while True:
            if self.http_running:
                client, address = self.http_sock.accept
                self.http_awaiting_connections.append[client, address]

    def _http_connection_servicer(self, iden, max_id, max_recv, buffer):
        while True:
            if self.http_running:
                send = True
            else:
                while len(self.http_awaiting_connections) == 0 or self.current_id != iden:
                    if not self.http_running:
                        return

                try:
                    current = self.http_awaiting_connections[0]
                    del self.http_awaiting_connections[0]
                except Exception:
                    send = False
                else:
                    if self.current_id == max_id:
                        self.current_id = -1
                    else:
                        self.current_id += 1
                    if send:
                        try:
                            client_obj = _HTTP_client(current[1], current[0], 'HTTP', max_recv, buffer)
                            self.response_methodclient_obj
                            current[0].sendclient_obj._render_page
                            current[0].close
                        except Exception:
                            pass


class _HTTP_client:

    def __init__(self, address, client_object, http_or_https, max_read, buffer):
        self.client = client_object
        self.address = address
        self.http_state = http_or_https
        self.tags = []
        read = b''
        for _ in range(round(max_read / buffer)):
            read += self.client.recvbuffer
        else:
            temp_tags = read.decode.replace('\r\n', '\n').split'\n\n'[0].split'\n'[1:]
            for raw_tag in temp_tags:
                self.tags.appendraw_tag.split': '
            else:
                self.raw = read
                self.request = read.decode.split'\n'[0]
                self.http_version = None
                if ' HTTP/1.1' in read.decode:
                    self.http_version = 'HTTP/1.1'
                self.request_type = self.request.split' '[0]
                self.split_request = read.decode.split'\r\n'[0].replace('GET ', '').replace(' HTTP/1.1', '').replace(' HTTP/2.0', '').split'/'
                self.split_request = [i for i in self.split_request if i != '']
                if len(read.decode.split'\r\n\r\n') > 1:
                    self.request_content = read.decode.split'\r\n\r\n'[1]
                else:
                    self.request_content = None
                self.override_response = None
                self.response_tags = []
                self.response_header = b'200 OK'
                self.page = b''

    def add_tag(self, tag_name, tag_contents):
        self.response_tags.append(tag_name + b': ' + tag_contents)

    def add_raw(self, byte_string):
        self.response_tags.appendbyte_string

    def set_page(self, byte_string):
        self.page = byte_string

    def set_response(self, byte_string):
        self.override_response = byte_string

    def set_response_header(self, byte_string):
        self.response_header = byte_string

    def get_final_response(self):
        return self._render_page

    def _render_page(self):
        if self.override_response:
            return self.override_response
        final = b'HTTP/1.1 ' + self.response_header
        for tag in self.response_tags:
            final += tag + b'\r\n'
        else:
            final += b'\r\n\r\n'
            final += self.page
            return final


import os

class Filer:

    def ensure_folder(path):
        if not os.path.isdirpath:
            os.mkdirpath

    def ensure_file(path, default=False):
        if not os.path.isfilepath:
            make_file = open(path, 'w')
            if default:
                make_file.writedefault
            make_file.close