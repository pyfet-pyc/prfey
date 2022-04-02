# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: keyboard\_nixkeyboard.py
import struct, traceback
from time import time as now
from collections import namedtuple
from ._keyboard_event import KeyboardEvent, KEY_DOWN, KEY_UP
from ._canonical_names import all_modifiers, normalize_name
from ._nixcommon import EV_KEY, aggregate_devices, ensure_root

def cleanup_key(name):
    """ Formats a dumpkeys format to our standard. """
    name = name.lstrip('+')
    is_keypad = name.startswith('KP_')
    for mod in ('Meta_', 'Control_', 'dead_', 'KP_'):
        if name.startswith(mod):
            name = name[len(mod):]
    else:
        if name == 'Remove':
            name = 'Delete'
        elif name == 'Delete':
            name = 'Backspace'
        if name.endswith('_r'):
            name = 'right ' + name[:-2]
        if name.endswith('_l'):
            name = 'left ' + name[:-2]
        return (
         normalize_name(name), is_keypad)


def cleanup_modifier--- This code section failed: ---

 L.  36         0  LOAD_GLOBAL              normalize_name
                2  LOAD_FAST                'modifier'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'modifier'

 L.  37         8  LOAD_FAST                'modifier'
               10  LOAD_GLOBAL              all_modifiers
               12  <118>                 0  ''
               14  POP_JUMP_IF_FALSE    20  'to 20'

 L.  38        16  LOAD_FAST                'modifier'
               18  RETURN_VALUE     
             20_0  COME_FROM            14  '14'

 L.  39        20  LOAD_FAST                'modifier'
               22  LOAD_CONST               None
               24  LOAD_CONST               -1
               26  BUILD_SLICE_2         2 
               28  BINARY_SUBSCR    
               30  LOAD_GLOBAL              all_modifiers
               32  <118>                 0  ''
               34  POP_JUMP_IF_FALSE    48  'to 48'

 L.  40        36  LOAD_FAST                'modifier'
               38  LOAD_CONST               None
               40  LOAD_CONST               -1
               42  BUILD_SLICE_2         2 
               44  BINARY_SUBSCR    
               46  RETURN_VALUE     
             48_0  COME_FROM            34  '34'

 L.  41        48  LOAD_GLOBAL              ValueError
               50  LOAD_STR                 'Unknown modifier {}'
               52  LOAD_METHOD              format
               54  LOAD_FAST                'modifier'
               56  CALL_METHOD_1         1  ''
               58  CALL_FUNCTION_1       1  ''
               60  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<118>' instruction at offset 12


from subprocess import check_output
from collections import defaultdict
import re
to_name = defaultdict(list)
from_name = defaultdict(list)
keypad_scan_codes = set()

def register_key--- This code section failed: ---

 L.  57         0  LOAD_FAST                'name'
                2  LOAD_GLOBAL              to_name
                4  LOAD_FAST                'key_and_modifiers'
                6  BINARY_SUBSCR    
                8  <118>                 1  ''
               10  POP_JUMP_IF_FALSE    26  'to 26'

 L.  58        12  LOAD_GLOBAL              to_name
               14  LOAD_FAST                'key_and_modifiers'
               16  BINARY_SUBSCR    
               18  LOAD_METHOD              append
               20  LOAD_FAST                'name'
               22  CALL_METHOD_1         1  ''
               24  POP_TOP          
             26_0  COME_FROM            10  '10'

 L.  59        26  LOAD_FAST                'key_and_modifiers'
               28  LOAD_GLOBAL              from_name
               30  LOAD_FAST                'name'
               32  BINARY_SUBSCR    
               34  <118>                 1  ''
               36  POP_JUMP_IF_FALSE    52  'to 52'

 L.  60        38  LOAD_GLOBAL              from_name
               40  LOAD_FAST                'name'
               42  BINARY_SUBSCR    
               44  LOAD_METHOD              append
               46  LOAD_FAST                'key_and_modifiers'
               48  CALL_METHOD_1         1  ''
               50  POP_TOP          
             52_0  COME_FROM            36  '36'

Parse error at or near `None' instruction at offset -1


def build_tables--- This code section failed: ---

 L.  63         0  LOAD_GLOBAL              to_name
                2  POP_JUMP_IF_FALSE    12  'to 12'
                4  LOAD_GLOBAL              from_name
                6  POP_JUMP_IF_FALSE    12  'to 12'
                8  LOAD_CONST               None
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'
             12_1  COME_FROM             2  '2'

 L.  64        12  LOAD_GLOBAL              ensure_root
               14  CALL_FUNCTION_0       0  ''
               16  POP_TOP          

 L.  67        18  LOAD_CONST               1

 L.  68        20  LOAD_CONST               2

 L.  69        22  LOAD_CONST               4

 L.  70        24  LOAD_CONST               8

 L.  66        26  LOAD_CONST               ('shift', 'alt gr', 'ctrl', 'alt')
               28  BUILD_CONST_KEY_MAP_4     4 
               30  STORE_FAST               'modifiers_bits'

 L.  72        32  LOAD_STR                 '^keycode\\s+(\\d+)\\s+=(.*?)$'
               34  STORE_FAST               'keycode_template'

 L.  73        36  LOAD_GLOBAL              check_output
               38  LOAD_STR                 'dumpkeys'
               40  LOAD_STR                 '--keys-only'
               42  BUILD_LIST_2          2 
               44  LOAD_CONST               True
               46  LOAD_CONST               ('universal_newlines',)
               48  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               50  STORE_FAST               'dump'

 L.  74        52  LOAD_GLOBAL              re
               54  LOAD_METHOD              findall
               56  LOAD_FAST                'keycode_template'
               58  LOAD_FAST                'dump'
               60  LOAD_GLOBAL              re
               62  LOAD_ATTR                MULTILINE
               64  CALL_METHOD_3         3  ''
               66  GET_ITER         
             68_0  COME_FROM           198  '198'
               68  FOR_ITER            200  'to 200'
               70  UNPACK_SEQUENCE_2     2 
               72  STORE_FAST               'str_scan_code'
               74  STORE_FAST               'str_names'

 L.  75        76  LOAD_GLOBAL              int
               78  LOAD_FAST                'str_scan_code'
               80  CALL_FUNCTION_1       1  ''
               82  STORE_FAST               'scan_code'

 L.  76        84  LOAD_GLOBAL              enumerate
               86  LOAD_FAST                'str_names'
               88  LOAD_METHOD              strip
               90  CALL_METHOD_0         0  ''
               92  LOAD_METHOD              split
               94  CALL_METHOD_0         0  ''
               96  CALL_FUNCTION_1       1  ''
               98  GET_ITER         
            100_0  COME_FROM           196  '196'
            100_1  COME_FROM           166  '166'
              100  FOR_ITER            198  'to 198'
              102  UNPACK_SEQUENCE_2     2 
              104  STORE_DEREF              'i'
              106  STORE_FAST               'str_name'

 L.  77       108  LOAD_GLOBAL              tuple
              110  LOAD_GLOBAL              sorted
              112  LOAD_CLOSURE             'i'
              114  BUILD_TUPLE_1         1 
              116  LOAD_GENEXPR             '<code_object <genexpr>>'
              118  LOAD_STR                 'build_tables.<locals>.<genexpr>'
              120  MAKE_FUNCTION_8          'closure'
              122  LOAD_FAST                'modifiers_bits'
              124  LOAD_METHOD              items
              126  CALL_METHOD_0         0  ''
              128  GET_ITER         
              130  CALL_FUNCTION_1       1  ''
              132  CALL_FUNCTION_1       1  ''
              134  CALL_FUNCTION_1       1  ''
              136  STORE_FAST               'modifiers'

 L.  78       138  LOAD_GLOBAL              cleanup_key
              140  LOAD_FAST                'str_name'
              142  CALL_FUNCTION_1       1  ''
              144  UNPACK_SEQUENCE_2     2 
              146  STORE_FAST               'name'
              148  STORE_FAST               'is_keypad'

 L.  79       150  LOAD_GLOBAL              register_key
              152  LOAD_FAST                'scan_code'
              154  LOAD_FAST                'modifiers'
              156  BUILD_TUPLE_2         2 
              158  LOAD_FAST                'name'
              160  CALL_FUNCTION_2       2  ''
              162  POP_TOP          

 L.  80       164  LOAD_FAST                'is_keypad'
              166  POP_JUMP_IF_FALSE_BACK   100  'to 100'

 L.  81       168  LOAD_GLOBAL              keypad_scan_codes
              170  LOAD_METHOD              add
              172  LOAD_FAST                'scan_code'
              174  CALL_METHOD_1         1  ''
              176  POP_TOP          

 L.  82       178  LOAD_GLOBAL              register_key
              180  LOAD_FAST                'scan_code'
              182  LOAD_FAST                'modifiers'
              184  BUILD_TUPLE_2         2 
              186  LOAD_STR                 'keypad '
              188  LOAD_FAST                'name'
              190  BINARY_ADD       
              192  CALL_FUNCTION_2       2  ''
              194  POP_TOP          
              196  JUMP_BACK           100  'to 100'
            198_0  COME_FROM           100  '100'
              198  JUMP_BACK            68  'to 68'
            200_0  COME_FROM            68  '68'

 L.  87       200  LOAD_CONST               (125, ())
              202  LOAD_GLOBAL              to_name
              204  <118>                 1  ''
              206  POP_JUMP_IF_TRUE    220  'to 220'
              208  LOAD_GLOBAL              to_name
              210  LOAD_CONST               (125, ())
              212  BINARY_SUBSCR    
              214  LOAD_STR                 'alt'
              216  COMPARE_OP               ==
              218  POP_JUMP_IF_FALSE   230  'to 230'
            220_0  COME_FROM           206  '206'

 L.  88       220  LOAD_GLOBAL              register_key
              222  LOAD_CONST               (125, ())
              224  LOAD_STR                 'windows'
              226  CALL_FUNCTION_2       2  ''
              228  POP_TOP          
            230_0  COME_FROM           218  '218'

 L.  89       230  LOAD_CONST               (126, ())
              232  LOAD_GLOBAL              to_name
              234  <118>                 1  ''
              236  POP_JUMP_IF_TRUE    252  'to 252'
              238  LOAD_GLOBAL              to_name
              240  LOAD_CONST               (126, ())
              242  BINARY_SUBSCR    
              244  LOAD_STR                 'alt'
              246  COMPARE_OP               ==
          248_250  POP_JUMP_IF_FALSE   262  'to 262'
            252_0  COME_FROM           236  '236'

 L.  90       252  LOAD_GLOBAL              register_key
              254  LOAD_CONST               (126, ())
              256  LOAD_STR                 'windows'
              258  CALL_FUNCTION_2       2  ''
              260  POP_TOP          
            262_0  COME_FROM           248  '248'

 L.  93       262  LOAD_CONST               (127, ())
              264  LOAD_GLOBAL              to_name
              266  <118>                 1  ''
          268_270  POP_JUMP_IF_FALSE   282  'to 282'

 L.  94       272  LOAD_GLOBAL              register_key
              274  LOAD_CONST               (127, ())
              276  LOAD_STR                 'menu'
              278  CALL_FUNCTION_2       2  ''
              280  POP_TOP          
            282_0  COME_FROM           268  '268'

 L.  96       282  LOAD_STR                 '^(\\S+)\\s+for (.+)$'
              284  STORE_FAST               'synonyms_template'

 L.  97       286  LOAD_GLOBAL              check_output
              288  LOAD_STR                 'dumpkeys'
              290  LOAD_STR                 '--long-info'
              292  BUILD_LIST_2          2 
              294  LOAD_CONST               True
              296  LOAD_CONST               ('universal_newlines',)
              298  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              300  STORE_FAST               'dump'

 L.  98       302  LOAD_GLOBAL              re
              304  LOAD_METHOD              findall
              306  LOAD_FAST                'synonyms_template'
              308  LOAD_FAST                'dump'
              310  LOAD_GLOBAL              re
              312  LOAD_ATTR                MULTILINE
              314  CALL_METHOD_3         3  ''
              316  GET_ITER         
            318_0  COME_FROM           396  '396'
            318_1  COME_FROM           356  '356'
              318  FOR_ITER            400  'to 400'
              320  UNPACK_SEQUENCE_2     2 
              322  STORE_FAST               'synonym_str'
              324  STORE_FAST               'original_str'

 L.  99       326  LOAD_GLOBAL              cleanup_key
              328  LOAD_FAST                'synonym_str'
              330  CALL_FUNCTION_1       1  ''
              332  UNPACK_SEQUENCE_2     2 
              334  STORE_FAST               'synonym'
              336  STORE_FAST               '_'

 L. 100       338  LOAD_GLOBAL              cleanup_key
              340  LOAD_FAST                'original_str'
              342  CALL_FUNCTION_1       1  ''
              344  UNPACK_SEQUENCE_2     2 
              346  STORE_FAST               'original'
              348  STORE_FAST               '_'

 L. 101       350  LOAD_FAST                'synonym'
              352  LOAD_FAST                'original'
              354  COMPARE_OP               !=
          356_358  POP_JUMP_IF_FALSE_BACK   318  'to 318'

 L. 102       360  LOAD_GLOBAL              from_name
              362  LOAD_FAST                'original'
              364  BINARY_SUBSCR    
              366  LOAD_METHOD              extend
              368  LOAD_GLOBAL              from_name
              370  LOAD_FAST                'synonym'
              372  BINARY_SUBSCR    
              374  CALL_METHOD_1         1  ''
              376  POP_TOP          

 L. 103       378  LOAD_GLOBAL              from_name
              380  LOAD_FAST                'synonym'
              382  BINARY_SUBSCR    
              384  LOAD_METHOD              extend
              386  LOAD_GLOBAL              from_name
              388  LOAD_FAST                'original'
              390  BINARY_SUBSCR    
              392  CALL_METHOD_1         1  ''
              394  POP_TOP          
          396_398  JUMP_BACK           318  'to 318'
            400_0  COME_FROM           318  '318'

Parse error at or near `<118>' instruction at offset 204


device = None

def build_device():
    global device
    if device:
        return
    ensure_root()
    device = aggregate_devices('kbd')


def init():
    build_device()
    build_tables()


pressed_modifiers = set()

def listen--- This code section failed: ---

 L. 119         0  LOAD_GLOBAL              build_device
                2  CALL_FUNCTION_0       0  ''
                4  POP_TOP          

 L. 120         6  LOAD_GLOBAL              build_tables
                8  CALL_FUNCTION_0       0  ''
               10  POP_TOP          
             12_0  COME_FROM           178  '178'
             12_1  COME_FROM            38  '38'

 L. 123        12  LOAD_GLOBAL              device
               14  LOAD_METHOD              read_event
               16  CALL_METHOD_0         0  ''
               18  UNPACK_SEQUENCE_5     5 
               20  STORE_FAST               'time'
               22  STORE_FAST               'type'
               24  STORE_FAST               'code'
               26  STORE_FAST               'value'
               28  STORE_FAST               'device_id'

 L. 124        30  LOAD_FAST                'type'
               32  LOAD_GLOBAL              EV_KEY
               34  COMPARE_OP               !=
               36  POP_JUMP_IF_FALSE    40  'to 40'

 L. 125        38  JUMP_BACK            12  'to 12'
             40_0  COME_FROM            36  '36'

 L. 127        40  LOAD_FAST                'code'
               42  STORE_FAST               'scan_code'

 L. 128        44  LOAD_FAST                'value'
               46  POP_JUMP_IF_FALSE    52  'to 52'
               48  LOAD_GLOBAL              KEY_DOWN
               50  JUMP_FORWARD         54  'to 54'
             52_0  COME_FROM            46  '46'
               52  LOAD_GLOBAL              KEY_UP
             54_0  COME_FROM            50  '50'
               54  STORE_FAST               'event_type'

 L. 130        56  LOAD_GLOBAL              tuple
               58  LOAD_GLOBAL              sorted
               60  LOAD_GLOBAL              pressed_modifiers
               62  CALL_FUNCTION_1       1  ''
               64  CALL_FUNCTION_1       1  ''
               66  STORE_FAST               'pressed_modifiers_tuple'

 L. 131        68  LOAD_GLOBAL              to_name
               70  LOAD_FAST                'scan_code'
               72  LOAD_FAST                'pressed_modifiers_tuple'
               74  BUILD_TUPLE_2         2 
               76  BINARY_SUBSCR    
               78  JUMP_IF_TRUE_OR_POP    96  'to 96'
               80  LOAD_GLOBAL              to_name
               82  LOAD_FAST                'scan_code'
               84  LOAD_CONST               ()
               86  BUILD_TUPLE_2         2 
               88  BINARY_SUBSCR    
               90  JUMP_IF_TRUE_OR_POP    96  'to 96'
               92  LOAD_STR                 'unknown'
               94  BUILD_LIST_1          1 
             96_0  COME_FROM            90  '90'
             96_1  COME_FROM            78  '78'
               96  STORE_FAST               'names'

 L. 132        98  LOAD_FAST                'names'
              100  LOAD_CONST               0
              102  BINARY_SUBSCR    
              104  STORE_FAST               'name'

 L. 134       106  LOAD_FAST                'name'
              108  LOAD_GLOBAL              all_modifiers
              110  <118>                 0  ''
              112  POP_JUMP_IF_FALSE   144  'to 144'

 L. 135       114  LOAD_FAST                'event_type'
              116  LOAD_GLOBAL              KEY_DOWN
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_FALSE   134  'to 134'

 L. 136       122  LOAD_GLOBAL              pressed_modifiers
              124  LOAD_METHOD              add
              126  LOAD_FAST                'name'
              128  CALL_METHOD_1         1  ''
              130  POP_TOP          
              132  JUMP_FORWARD        144  'to 144'
            134_0  COME_FROM           120  '120'

 L. 138       134  LOAD_GLOBAL              pressed_modifiers
              136  LOAD_METHOD              discard
              138  LOAD_FAST                'name'
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          
            144_0  COME_FROM           132  '132'
            144_1  COME_FROM           112  '112'

 L. 140       144  LOAD_FAST                'scan_code'
              146  LOAD_GLOBAL              keypad_scan_codes
              148  <118>                 0  ''
              150  STORE_FAST               'is_keypad'

 L. 141       152  LOAD_FAST                'callback'
              154  LOAD_GLOBAL              KeyboardEvent
              156  LOAD_FAST                'event_type'
              158  LOAD_FAST                'scan_code'
              160  LOAD_FAST                'name'
              162  LOAD_FAST                'time'
              164  LOAD_FAST                'device_id'
              166  LOAD_FAST                'is_keypad'
              168  LOAD_FAST                'pressed_modifiers_tuple'
              170  LOAD_CONST               ('event_type', 'scan_code', 'name', 'time', 'device', 'is_keypad', 'modifiers')
              172  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              174  CALL_FUNCTION_1       1  ''
              176  POP_TOP          
              178  JUMP_BACK            12  'to 12'

Parse error at or near `<118>' instruction at offset 110


def write_event(scan_code, is_down):
    build_device()
    device.write_eventEV_KEYscan_codeint(is_down)


def map_name--- This code section failed: ---

 L. 148         0  LOAD_GLOBAL              build_tables
                2  CALL_FUNCTION_0       0  ''
                4  POP_TOP          

 L. 149         6  LOAD_GLOBAL              from_name
                8  LOAD_FAST                'name'
               10  BINARY_SUBSCR    
               12  GET_ITER         
             14_0  COME_FROM            24  '24'
               14  FOR_ITER             26  'to 26'
               16  STORE_FAST               'entry'

 L. 150        18  LOAD_FAST                'entry'
               20  YIELD_VALUE      
               22  POP_TOP          
               24  JUMP_BACK            14  'to 14'
             26_0  COME_FROM            14  '14'

 L. 152        26  LOAD_FAST                'name'
               28  LOAD_METHOD              split
               30  LOAD_STR                 ' '
               32  LOAD_CONST               1
               34  CALL_METHOD_2         2  ''
               36  STORE_FAST               'parts'

 L. 153        38  LOAD_GLOBAL              len
               40  LOAD_FAST                'parts'
               42  CALL_FUNCTION_1       1  ''
               44  LOAD_CONST               1
               46  COMPARE_OP               >
               48  POP_JUMP_IF_FALSE    86  'to 86'
               50  LOAD_FAST                'parts'
               52  LOAD_CONST               0
               54  BINARY_SUBSCR    
               56  LOAD_CONST               ('left', 'right')
               58  <118>                 0  ''
               60  POP_JUMP_IF_FALSE    86  'to 86'

 L. 154        62  LOAD_GLOBAL              from_name
               64  LOAD_FAST                'parts'
               66  LOAD_CONST               1
               68  BINARY_SUBSCR    
               70  BINARY_SUBSCR    
               72  GET_ITER         
             74_0  COME_FROM            84  '84'
               74  FOR_ITER             86  'to 86'
               76  STORE_FAST               'entry'

 L. 155        78  LOAD_FAST                'entry'
               80  YIELD_VALUE      
               82  POP_TOP          
               84  JUMP_BACK            74  'to 74'
             86_0  COME_FROM            74  '74'
             86_1  COME_FROM            60  '60'
             86_2  COME_FROM            48  '48'

Parse error at or near `<118>' instruction at offset 58


def press(scan_code):
    write_eventscan_codeTrue


def release(scan_code):
    write_eventscan_codeFalse


def type_unicode(character):
    codepoint = ord(character)
    hexadecimal = hex(codepoint)[len('0x'):]
    for key in ('ctrl', 'shift', 'u'):
        scan_code, _ = next(map_name(key))
        press(scan_code)
    else:
        for key in hexadecimal:
            scan_code, _ = next(map_name(key))
            press(scan_code)
            release(scan_code)
        else:
            for key in ('ctrl', 'shift', 'u'):
                scan_code, _ = next(map_name(key))
                release(scan_code)


if __name__ == '__main__':

    def p(e):
        print(e)


    listen(p)