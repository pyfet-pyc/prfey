# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\serial\__init__.py
import sys, importlib
from serial.serialutil import *
__version__ = '3.4'
VERSION = __version__
if sys.platform == 'cli':
    from serial.serialcli import Serial
else:
    import os
    if os.name == 'nt':
        from serial.serialwin32 import Serial
    elif os.name == 'posix':
        from serial.serialposix import Serial, PosixPollSerial, VTIMESerial
    elif os.name == 'java':
        from serial.serialjava import Serial
    else:
        raise ImportError("Sorry: no implementation for your platform ('{}') available".format(os.name))
protocol_handler_packages = [
 'serial.urlhandler']

def serial_for_url--- This code section failed: ---

 L.  57         0  LOAD_FAST                'kwargs'
                2  LOAD_METHOD              pop
                4  LOAD_STR                 'do_not_open'
                6  LOAD_CONST               False
                8  CALL_METHOD_2         2  ''
               10  UNARY_NOT        
               12  STORE_FAST               'do_open'

 L.  59        14  LOAD_GLOBAL              Serial
               16  STORE_FAST               'klass'

 L.  60        18  SETUP_FINALLY        32  'to 32'

 L.  61        20  LOAD_FAST                'url'
               22  LOAD_METHOD              lower
               24  CALL_METHOD_0         0  ''
               26  STORE_FAST               'url_lowercase'
               28  POP_BLOCK        
               30  JUMP_FORWARD         52  'to 52'
             32_0  COME_FROM_FINALLY    18  '18'

 L.  62        32  DUP_TOP          
               34  LOAD_GLOBAL              AttributeError
               36  COMPARE_OP               exception-match
               38  POP_JUMP_IF_FALSE    50  'to 50'
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L.  64        46  POP_EXCEPT       
               48  JUMP_FORWARD        198  'to 198'
             50_0  COME_FROM            38  '38'
               50  END_FINALLY      
             52_0  COME_FROM            30  '30'

 L.  67        52  LOAD_STR                 '://'
               54  LOAD_FAST                'url_lowercase'
               56  COMPARE_OP               in
               58  POP_JUMP_IF_FALSE   198  'to 198'

 L.  68        60  LOAD_FAST                'url_lowercase'
               62  LOAD_METHOD              split
               64  LOAD_STR                 '://'
               66  LOAD_CONST               1
               68  CALL_METHOD_2         2  ''
               70  LOAD_CONST               0
               72  BINARY_SUBSCR    
               74  STORE_FAST               'protocol'

 L.  69        76  LOAD_STR                 '.protocol_{}'
               78  LOAD_METHOD              format
               80  LOAD_FAST                'protocol'
               82  CALL_METHOD_1         1  ''
               84  STORE_FAST               'module_name'

 L.  70        86  LOAD_GLOBAL              protocol_handler_packages
               88  GET_ITER         
             90_0  COME_FROM           182  '182'
             90_1  COME_FROM           142  '142'
             90_2  COME_FROM           138  '138'
               90  FOR_ITER            184  'to 184'
               92  STORE_FAST               'package_name'

 L.  71        94  SETUP_FINALLY       122  'to 122'

 L.  72        96  LOAD_GLOBAL              importlib
               98  LOAD_METHOD              import_module
              100  LOAD_FAST                'package_name'
              102  CALL_METHOD_1         1  ''
              104  POP_TOP          

 L.  73       106  LOAD_GLOBAL              importlib
              108  LOAD_METHOD              import_module
              110  LOAD_FAST                'module_name'
              112  LOAD_FAST                'package_name'
              114  CALL_METHOD_2         2  ''
              116  STORE_FAST               'handler_module'
              118  POP_BLOCK        
              120  JUMP_FORWARD        146  'to 146'
            122_0  COME_FROM_FINALLY    94  '94'

 L.  74       122  DUP_TOP          
              124  LOAD_GLOBAL              ImportError
              126  COMPARE_OP               exception-match
              128  POP_JUMP_IF_FALSE   144  'to 144'
              130  POP_TOP          
              132  POP_TOP          
              134  POP_TOP          

 L.  75       136  POP_EXCEPT       
              138  JUMP_BACK            90  'to 90'
              140  POP_EXCEPT       
              142  JUMP_BACK            90  'to 90'
            144_0  COME_FROM           128  '128'
              144  END_FINALLY      
            146_0  COME_FROM           120  '120'

 L.  77       146  LOAD_GLOBAL              hasattr
              148  LOAD_FAST                'handler_module'
              150  LOAD_STR                 'serial_class_for_url'
              152  CALL_FUNCTION_2       2  ''
              154  POP_JUMP_IF_FALSE   172  'to 172'

 L.  78       156  LOAD_FAST                'handler_module'
              158  LOAD_METHOD              serial_class_for_url
              160  LOAD_FAST                'url'
              162  CALL_METHOD_1         1  ''
              164  UNPACK_SEQUENCE_2     2 
              166  STORE_FAST               'url'
              168  STORE_FAST               'klass'
              170  JUMP_FORWARD        178  'to 178'
            172_0  COME_FROM           154  '154'

 L.  80       172  LOAD_FAST                'handler_module'
              174  LOAD_ATTR                Serial
              176  STORE_FAST               'klass'
            178_0  COME_FROM           170  '170'

 L.  81       178  POP_TOP          
              180  BREAK_LOOP          198  'to 198'
              182  JUMP_BACK            90  'to 90'
            184_0  COME_FROM            90  '90'

 L.  83       184  LOAD_GLOBAL              ValueError
              186  LOAD_STR                 'invalid URL, protocol {!r} not known'
              188  LOAD_METHOD              format
              190  LOAD_FAST                'protocol'
              192  CALL_METHOD_1         1  ''
              194  CALL_FUNCTION_1       1  ''
              196  RAISE_VARARGS_1       1  'exception instance'
            198_0  COME_FROM           180  '180'
            198_1  COME_FROM            58  '58'
            198_2  COME_FROM            48  '48'

 L.  85       198  LOAD_FAST                'klass'
              200  LOAD_CONST               (None,)
              202  LOAD_FAST                'args'
              204  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
              206  LOAD_FAST                'kwargs'
              208  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              210  STORE_FAST               'instance'

 L.  86       212  LOAD_FAST                'url'
              214  LOAD_FAST                'instance'
              216  STORE_ATTR               port

 L.  87       218  LOAD_FAST                'do_open'
              220  POP_JUMP_IF_FALSE   230  'to 230'

 L.  88       222  LOAD_FAST                'instance'
              224  LOAD_METHOD              open
              226  CALL_METHOD_0         0  ''
              228  POP_TOP          
            230_0  COME_FROM           220  '220'

 L.  89       230  LOAD_FAST                'instance'
              232  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 142