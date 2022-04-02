# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: requests\utils.py
"""
requests.utils
~~~~~~~~~~~~~~

This module provides utility functions that are used within Requests
that are also useful for external consumption.
"""
import codecs, contextlib, io, os, re, socket, struct, sys, tempfile, warnings, zipfile
from collections import OrderedDict
from urllib3.util import make_headers
from .__version__ import __version__
from . import certs
from ._internal_utils import to_native_string
from .compat import parse_http_list as _parse_list_header
from .compat import quote, urlparse, bytes, str, unquote, getproxies, proxy_bypass, urlunparse, basestring, integer_types, is_py3, proxy_bypass_environment, getproxies_environment, Mapping
from .cookies import cookiejar_from_dict
from .structures import CaseInsensitiveDict
from .exceptions import InvalidURL, InvalidHeader, FileModeWarning, UnrewindableBodyError
NETRC_FILES = ('.netrc', '_netrc')
DEFAULT_CA_BUNDLE_PATH = certs.where()
DEFAULT_PORTS = {'http':80, 
 'https':443}
DEFAULT_ACCEPT_ENCODING = ', '.join(re.split(',\\s*', make_headers(accept_encoding=True)['accept-encoding']))
if sys.platform == 'win32':

    def proxy_bypass_registry--- This code section failed: ---

 L.  55         0  SETUP_FINALLY        28  'to 28'

 L.  56         2  LOAD_GLOBAL              is_py3
                4  POP_JUMP_IF_FALSE    16  'to 16'

 L.  57         6  LOAD_CONST               0
                8  LOAD_CONST               None
               10  IMPORT_NAME              winreg
               12  STORE_FAST               'winreg'
               14  JUMP_FORWARD         24  'to 24'
             16_0  COME_FROM             4  '4'

 L.  59        16  LOAD_CONST               0
               18  LOAD_CONST               None
               20  IMPORT_NAME              _winreg
               22  STORE_FAST               'winreg'
             24_0  COME_FROM            14  '14'
               24  POP_BLOCK        
               26  JUMP_FORWARD         48  'to 48'
             28_0  COME_FROM_FINALLY     0  '0'

 L.  60        28  DUP_TOP          
               30  LOAD_GLOBAL              ImportError
               32  <121>                46  ''
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L.  61        40  POP_EXCEPT       
               42  LOAD_CONST               False
               44  RETURN_VALUE     
               46  <48>             
             48_0  COME_FROM            26  '26'

 L.  63        48  SETUP_FINALLY       104  'to 104'

 L.  64        50  LOAD_FAST                'winreg'
               52  LOAD_METHOD              OpenKey
               54  LOAD_FAST                'winreg'
               56  LOAD_ATTR                HKEY_CURRENT_USER

 L.  65        58  LOAD_STR                 'Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings'

 L.  64        60  CALL_METHOD_2         2  ''
               62  STORE_FAST               'internetSettings'

 L.  67        64  LOAD_GLOBAL              int
               66  LOAD_FAST                'winreg'
               68  LOAD_METHOD              QueryValueEx
               70  LOAD_FAST                'internetSettings'

 L.  68        72  LOAD_STR                 'ProxyEnable'

 L.  67        74  CALL_METHOD_2         2  ''

 L.  68        76  LOAD_CONST               0

 L.  67        78  BINARY_SUBSCR    
               80  CALL_FUNCTION_1       1  ''
               82  STORE_FAST               'proxyEnable'

 L.  70        84  LOAD_FAST                'winreg'
               86  LOAD_METHOD              QueryValueEx
               88  LOAD_FAST                'internetSettings'

 L.  71        90  LOAD_STR                 'ProxyOverride'

 L.  70        92  CALL_METHOD_2         2  ''

 L.  71        94  LOAD_CONST               0

 L.  70        96  BINARY_SUBSCR    
               98  STORE_FAST               'proxyOverride'
              100  POP_BLOCK        
              102  JUMP_FORWARD        124  'to 124'
            104_0  COME_FROM_FINALLY    48  '48'

 L.  72       104  DUP_TOP          
              106  LOAD_GLOBAL              OSError
              108  <121>               122  ''
              110  POP_TOP          
              112  POP_TOP          
              114  POP_TOP          

 L.  73       116  POP_EXCEPT       
              118  LOAD_CONST               False
              120  RETURN_VALUE     
              122  <48>             
            124_0  COME_FROM           102  '102'

 L.  74       124  LOAD_FAST                'proxyEnable'
              126  POP_JUMP_IF_FALSE   132  'to 132'
              128  LOAD_FAST                'proxyOverride'
              130  POP_JUMP_IF_TRUE    136  'to 136'
            132_0  COME_FROM           126  '126'

 L.  75       132  LOAD_CONST               False
              134  RETURN_VALUE     
            136_0  COME_FROM           130  '130'

 L.  80       136  LOAD_FAST                'proxyOverride'
              138  LOAD_METHOD              split
              140  LOAD_STR                 ';'
              142  CALL_METHOD_1         1  ''
              144  STORE_FAST               'proxyOverride'

 L.  82       146  LOAD_FAST                'proxyOverride'
              148  GET_ITER         
            150_0  COME_FROM           226  '226'
              150  FOR_ITER            236  'to 236'
              152  STORE_FAST               'test'

 L.  83       154  LOAD_FAST                'test'
              156  LOAD_STR                 '<local>'
              158  COMPARE_OP               ==
              160  POP_JUMP_IF_FALSE   176  'to 176'

 L.  84       162  LOAD_STR                 '.'
              164  LOAD_FAST                'host'
              166  <118>                 1  ''
              168  POP_JUMP_IF_FALSE   176  'to 176'

 L.  85       170  POP_TOP          
              172  LOAD_CONST               True
              174  RETURN_VALUE     
            176_0  COME_FROM           168  '168'
            176_1  COME_FROM           160  '160'

 L.  86       176  LOAD_FAST                'test'
              178  LOAD_METHOD              replace
              180  LOAD_STR                 '.'
              182  LOAD_STR                 '\\.'
              184  CALL_METHOD_2         2  ''
              186  STORE_FAST               'test'

 L.  87       188  LOAD_FAST                'test'
              190  LOAD_METHOD              replace
              192  LOAD_STR                 '*'
              194  LOAD_STR                 '.*'
              196  CALL_METHOD_2         2  ''
              198  STORE_FAST               'test'

 L.  88       200  LOAD_FAST                'test'
              202  LOAD_METHOD              replace
              204  LOAD_STR                 '?'
              206  LOAD_STR                 '.'
              208  CALL_METHOD_2         2  ''
              210  STORE_FAST               'test'

 L.  89       212  LOAD_GLOBAL              re
              214  LOAD_METHOD              match
              216  LOAD_FAST                'test'
              218  LOAD_FAST                'host'
              220  LOAD_GLOBAL              re
              222  LOAD_ATTR                I
              224  CALL_METHOD_3         3  ''
              226  POP_JUMP_IF_FALSE   150  'to 150'

 L.  90       228  POP_TOP          
              230  LOAD_CONST               True
              232  RETURN_VALUE     
              234  JUMP_BACK           150  'to 150'

 L.  91       236  LOAD_CONST               False
              238  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 32


    def proxy_bypass(host):
        """Return True, if the host should be bypassed.

        Checks proxy settings gathered from the environment, if specified,
        or the registry.
        """
        if getproxies_environment():
            return proxy_bypass_environment(host)
        return proxy_bypass_registry(host)


def dict_to_sequence(d):
    """Returns an internal sequence dictionary update."""
    if hasattr(d, 'items'):
        d = d.items()
    return d


def super_len--- This code section failed: ---

 L. 115         0  LOAD_CONST               None
                2  STORE_FAST               'total_length'

 L. 116         4  LOAD_CONST               0
                6  STORE_FAST               'current_position'

 L. 118         8  LOAD_GLOBAL              hasattr
               10  LOAD_FAST                'o'
               12  LOAD_STR                 '__len__'
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_FALSE    28  'to 28'

 L. 119        18  LOAD_GLOBAL              len
               20  LOAD_FAST                'o'
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'total_length'
               26  JUMP_FORWARD        124  'to 124'
             28_0  COME_FROM            16  '16'

 L. 121        28  LOAD_GLOBAL              hasattr
               30  LOAD_FAST                'o'
               32  LOAD_STR                 'len'
               34  CALL_FUNCTION_2       2  ''
               36  POP_JUMP_IF_FALSE    46  'to 46'

 L. 122        38  LOAD_FAST                'o'
               40  LOAD_ATTR                len
               42  STORE_FAST               'total_length'
               44  JUMP_FORWARD        124  'to 124'
             46_0  COME_FROM            36  '36'

 L. 124        46  LOAD_GLOBAL              hasattr
               48  LOAD_FAST                'o'
               50  LOAD_STR                 'fileno'
               52  CALL_FUNCTION_2       2  ''
               54  POP_JUMP_IF_FALSE   124  'to 124'

 L. 125        56  SETUP_FINALLY        70  'to 70'

 L. 126        58  LOAD_FAST                'o'
               60  LOAD_METHOD              fileno
               62  CALL_METHOD_0         0  ''
               64  STORE_FAST               'fileno'
               66  POP_BLOCK        
               68  JUMP_FORWARD         90  'to 90'
             70_0  COME_FROM_FINALLY    56  '56'

 L. 127        70  DUP_TOP          
               72  LOAD_GLOBAL              io
               74  LOAD_ATTR                UnsupportedOperation
               76  <121>                88  ''
               78  POP_TOP          
               80  POP_TOP          
               82  POP_TOP          

 L. 128        84  POP_EXCEPT       
               86  JUMP_FORWARD        124  'to 124'
               88  <48>             
             90_0  COME_FROM            68  '68'

 L. 130        90  LOAD_GLOBAL              os
               92  LOAD_METHOD              fstat
               94  LOAD_FAST                'fileno'
               96  CALL_METHOD_1         1  ''
               98  LOAD_ATTR                st_size
              100  STORE_FAST               'total_length'

 L. 134       102  LOAD_STR                 'b'
              104  LOAD_FAST                'o'
              106  LOAD_ATTR                mode
              108  <118>                 1  ''
              110  POP_JUMP_IF_FALSE   124  'to 124'

 L. 135       112  LOAD_GLOBAL              warnings
              114  LOAD_METHOD              warn

 L. 136       116  LOAD_STR                 "Requests has determined the content-length for this request using the binary size of the file: however, the file has been opened in text mode (i.e. without the 'b' flag in the mode). This may lead to an incorrect content-length. In Requests 3.0, support will be removed for files in text mode."

 L. 142       118  LOAD_GLOBAL              FileModeWarning

 L. 135       120  CALL_METHOD_2         2  ''
              122  POP_TOP          
            124_0  COME_FROM           110  '110'
            124_1  COME_FROM            86  '86'
            124_2  COME_FROM            54  '54'
            124_3  COME_FROM            44  '44'
            124_4  COME_FROM            26  '26'

 L. 145       124  LOAD_GLOBAL              hasattr
              126  LOAD_FAST                'o'
              128  LOAD_STR                 'tell'
              130  CALL_FUNCTION_2       2  ''
          132_134  POP_JUMP_IF_FALSE   274  'to 274'

 L. 146       136  SETUP_FINALLY       150  'to 150'

 L. 147       138  LOAD_FAST                'o'
              140  LOAD_METHOD              tell
              142  CALL_METHOD_0         0  ''
              144  STORE_FAST               'current_position'
              146  POP_BLOCK        
              148  JUMP_FORWARD        184  'to 184'
            150_0  COME_FROM_FINALLY   136  '136'

 L. 148       150  DUP_TOP          
              152  LOAD_GLOBAL              OSError
              154  LOAD_GLOBAL              IOError
              156  BUILD_TUPLE_2         2 
              158  <121>               182  ''
              160  POP_TOP          
              162  POP_TOP          
              164  POP_TOP          

 L. 153       166  LOAD_FAST                'total_length'
              168  LOAD_CONST               None
              170  <117>                 1  ''
              172  POP_JUMP_IF_FALSE   178  'to 178'

 L. 154       174  LOAD_FAST                'total_length'
              176  STORE_FAST               'current_position'
            178_0  COME_FROM           172  '172'
              178  POP_EXCEPT       
              180  JUMP_FORWARD        274  'to 274'
              182  <48>             
            184_0  COME_FROM           148  '148'

 L. 156       184  LOAD_GLOBAL              hasattr
              186  LOAD_FAST                'o'
              188  LOAD_STR                 'seek'
              190  CALL_FUNCTION_2       2  ''
          192_194  POP_JUMP_IF_FALSE   274  'to 274'
              196  LOAD_FAST                'total_length'
              198  LOAD_CONST               None
              200  <117>                 0  ''
          202_204  POP_JUMP_IF_FALSE   274  'to 274'

 L. 158       206  SETUP_FINALLY       246  'to 246'

 L. 160       208  LOAD_FAST                'o'
              210  LOAD_METHOD              seek
              212  LOAD_CONST               0
              214  LOAD_CONST               2
              216  CALL_METHOD_2         2  ''
              218  POP_TOP          

 L. 161       220  LOAD_FAST                'o'
              222  LOAD_METHOD              tell
              224  CALL_METHOD_0         0  ''
              226  STORE_FAST               'total_length'

 L. 165       228  LOAD_FAST                'o'
              230  LOAD_METHOD              seek
              232  LOAD_FAST                'current_position'
              234  JUMP_IF_TRUE_OR_POP   238  'to 238'
              236  LOAD_CONST               0
            238_0  COME_FROM           234  '234'
              238  CALL_METHOD_1         1  ''
              240  POP_TOP          
              242  POP_BLOCK        
              244  JUMP_FORWARD        274  'to 274'
            246_0  COME_FROM_FINALLY   206  '206'

 L. 166       246  DUP_TOP          
              248  LOAD_GLOBAL              OSError
              250  LOAD_GLOBAL              IOError
              252  BUILD_TUPLE_2         2 
          254_256  <121>               272  ''
              258  POP_TOP          
              260  POP_TOP          
              262  POP_TOP          

 L. 167       264  LOAD_CONST               0
              266  STORE_FAST               'total_length'
              268  POP_EXCEPT       
              270  JUMP_FORWARD        274  'to 274'
              272  <48>             
            274_0  COME_FROM           270  '270'
            274_1  COME_FROM           244  '244'
            274_2  COME_FROM           202  '202'
            274_3  COME_FROM           192  '192'
            274_4  COME_FROM           180  '180'
            274_5  COME_FROM           132  '132'

 L. 169       274  LOAD_FAST                'total_length'
              276  LOAD_CONST               None
              278  <117>                 0  ''
          280_282  POP_JUMP_IF_FALSE   288  'to 288'

 L. 170       284  LOAD_CONST               0
              286  STORE_FAST               'total_length'
            288_0  COME_FROM           280  '280'

 L. 172       288  LOAD_GLOBAL              max
              290  LOAD_CONST               0
              292  LOAD_FAST                'total_length'
              294  LOAD_FAST                'current_position'
              296  BINARY_SUBTRACT  
              298  CALL_FUNCTION_2       2  ''
              300  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 76


def get_netrc_auth--- This code section failed: ---

 L. 178         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                environ
                4  LOAD_METHOD              get
                6  LOAD_STR                 'NETRC'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'netrc_file'

 L. 179        12  LOAD_FAST                'netrc_file'
               14  LOAD_CONST               None
               16  <117>                 1  ''
               18  POP_JUMP_IF_FALSE    28  'to 28'

 L. 180        20  LOAD_FAST                'netrc_file'
               22  BUILD_TUPLE_1         1 
               24  STORE_FAST               'netrc_locations'
               26  JUMP_FORWARD         42  'to 42'
             28_0  COME_FROM            18  '18'

 L. 182        28  LOAD_GENEXPR             '<code_object <genexpr>>'
               30  LOAD_STR                 'get_netrc_auth.<locals>.<genexpr>'
               32  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               34  LOAD_GLOBAL              NETRC_FILES
               36  GET_ITER         
               38  CALL_FUNCTION_1       1  ''
               40  STORE_FAST               'netrc_locations'
             42_0  COME_FROM            26  '26'

 L. 184     42_44  SETUP_FINALLY       298  'to 298'

 L. 185        46  LOAD_CONST               0
               48  LOAD_CONST               ('netrc', 'NetrcParseError')
               50  IMPORT_NAME              netrc
               52  IMPORT_FROM              netrc
               54  STORE_FAST               'netrc'
               56  IMPORT_FROM              NetrcParseError
               58  STORE_FAST               'NetrcParseError'
               60  POP_TOP          

 L. 187        62  LOAD_CONST               None
               64  STORE_FAST               'netrc_path'

 L. 189        66  LOAD_FAST                'netrc_locations'
               68  GET_ITER         
             70_0  COME_FROM           126  '126'
               70  FOR_ITER            138  'to 138'
               72  STORE_FAST               'f'

 L. 190        74  SETUP_FINALLY        92  'to 92'

 L. 191        76  LOAD_GLOBAL              os
               78  LOAD_ATTR                path
               80  LOAD_METHOD              expanduser
               82  LOAD_FAST                'f'
               84  CALL_METHOD_1         1  ''
               86  STORE_FAST               'loc'
               88  POP_BLOCK        
               90  JUMP_FORWARD        116  'to 116'
             92_0  COME_FROM_FINALLY    74  '74'

 L. 192        92  DUP_TOP          
               94  LOAD_GLOBAL              KeyError
               96  <121>               114  ''
               98  POP_TOP          
              100  POP_TOP          
              102  POP_TOP          

 L. 196       104  POP_EXCEPT       
              106  POP_TOP          
              108  POP_BLOCK        
              110  LOAD_CONST               None
              112  RETURN_VALUE     
              114  <48>             
            116_0  COME_FROM            90  '90'

 L. 198       116  LOAD_GLOBAL              os
              118  LOAD_ATTR                path
              120  LOAD_METHOD              exists
              122  LOAD_FAST                'loc'
              124  CALL_METHOD_1         1  ''
              126  POP_JUMP_IF_FALSE    70  'to 70'

 L. 199       128  LOAD_FAST                'loc'
              130  STORE_FAST               'netrc_path'

 L. 200       132  POP_TOP          
              134  BREAK_LOOP          138  'to 138'
              136  JUMP_BACK            70  'to 70'

 L. 203       138  LOAD_FAST                'netrc_path'
              140  LOAD_CONST               None
              142  <117>                 0  ''
              144  POP_JUMP_IF_FALSE   152  'to 152'

 L. 204       146  POP_BLOCK        
              148  LOAD_CONST               None
              150  RETURN_VALUE     
            152_0  COME_FROM           144  '144'

 L. 206       152  LOAD_GLOBAL              urlparse
              154  LOAD_FAST                'url'
              156  CALL_FUNCTION_1       1  ''
              158  STORE_FAST               'ri'

 L. 210       160  LOAD_CONST               b':'
              162  STORE_FAST               'splitstr'

 L. 211       164  LOAD_GLOBAL              isinstance
              166  LOAD_FAST                'url'
              168  LOAD_GLOBAL              str
              170  CALL_FUNCTION_2       2  ''
              172  POP_JUMP_IF_FALSE   184  'to 184'

 L. 212       174  LOAD_FAST                'splitstr'
              176  LOAD_METHOD              decode
              178  LOAD_STR                 'ascii'
              180  CALL_METHOD_1         1  ''
              182  STORE_FAST               'splitstr'
            184_0  COME_FROM           172  '172'

 L. 213       184  LOAD_FAST                'ri'
              186  LOAD_ATTR                netloc
              188  LOAD_METHOD              split
              190  LOAD_FAST                'splitstr'
              192  CALL_METHOD_1         1  ''
              194  LOAD_CONST               0
              196  BINARY_SUBSCR    
              198  STORE_FAST               'host'

 L. 215       200  SETUP_FINALLY       262  'to 262'

 L. 216       202  LOAD_FAST                'netrc'
              204  LOAD_FAST                'netrc_path'
              206  CALL_FUNCTION_1       1  ''
              208  LOAD_METHOD              authenticators
              210  LOAD_FAST                'host'
              212  CALL_METHOD_1         1  ''
              214  STORE_FAST               '_netrc'

 L. 217       216  LOAD_FAST                '_netrc'
          218_220  POP_JUMP_IF_FALSE   258  'to 258'

 L. 219       222  LOAD_FAST                '_netrc'
              224  LOAD_CONST               0
              226  BINARY_SUBSCR    
              228  POP_JUMP_IF_FALSE   234  'to 234'
              230  LOAD_CONST               0
              232  JUMP_FORWARD        236  'to 236'
            234_0  COME_FROM           228  '228'
              234  LOAD_CONST               1
            236_0  COME_FROM           232  '232'
              236  STORE_FAST               'login_i'

 L. 220       238  LOAD_FAST                '_netrc'
              240  LOAD_FAST                'login_i'
              242  BINARY_SUBSCR    
              244  LOAD_FAST                '_netrc'
              246  LOAD_CONST               2
              248  BINARY_SUBSCR    
              250  BUILD_TUPLE_2         2 
              252  POP_BLOCK        
              254  POP_BLOCK        
              256  RETURN_VALUE     
            258_0  COME_FROM           218  '218'
              258  POP_BLOCK        
              260  JUMP_FORWARD        294  'to 294'
            262_0  COME_FROM_FINALLY   200  '200'

 L. 221       262  DUP_TOP          
              264  LOAD_FAST                'NetrcParseError'
              266  LOAD_GLOBAL              IOError
              268  BUILD_TUPLE_2         2 
          270_272  <121>               292  ''
              274  POP_TOP          
              276  POP_TOP          
              278  POP_TOP          

 L. 224       280  LOAD_FAST                'raise_errors'
          282_284  POP_JUMP_IF_FALSE   288  'to 288'

 L. 225       286  RAISE_VARARGS_0       0  'reraise'
            288_0  COME_FROM           282  '282'
              288  POP_EXCEPT       
              290  JUMP_FORWARD        294  'to 294'
              292  <48>             
            294_0  COME_FROM           290  '290'
            294_1  COME_FROM           260  '260'
              294  POP_BLOCK        
              296  JUMP_FORWARD        322  'to 322'
            298_0  COME_FROM_FINALLY    42  '42'

 L. 228       298  DUP_TOP          
              300  LOAD_GLOBAL              ImportError
              302  LOAD_GLOBAL              AttributeError
              304  BUILD_TUPLE_2         2 
          306_308  <121>               320  ''
              310  POP_TOP          
              312  POP_TOP          
              314  POP_TOP          

 L. 229       316  POP_EXCEPT       
              318  JUMP_FORWARD        322  'to 322'
              320  <48>             
            322_0  COME_FROM           318  '318'
            322_1  COME_FROM           296  '296'

Parse error at or near `<117>' instruction at offset 16


def guess_filename(obj):
    """Tries to guess the filename of the given object."""
    name = getattr(obj, 'name', None)
    if name:
        if isinstance(name, basestring):
            if name[0] != '<':
                if name[(-1)] != '>':
                    return os.path.basename(name)


def extract_zipped_paths--- This code section failed: ---

 L. 245         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              exists
                6  LOAD_FAST                'path'
                8  CALL_METHOD_1         1  ''
               10  POP_JUMP_IF_FALSE    16  'to 16'

 L. 247        12  LOAD_FAST                'path'
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L. 251        16  LOAD_GLOBAL              os
               18  LOAD_ATTR                path
               20  LOAD_METHOD              split
               22  LOAD_FAST                'path'
               24  CALL_METHOD_1         1  ''
               26  UNPACK_SEQUENCE_2     2 
               28  STORE_FAST               'archive'
               30  STORE_FAST               'member'

 L. 252        32  LOAD_FAST                'archive'
               34  POP_JUMP_IF_FALSE    80  'to 80'
               36  LOAD_GLOBAL              os
               38  LOAD_ATTR                path
               40  LOAD_METHOD              exists
               42  LOAD_FAST                'archive'
               44  CALL_METHOD_1         1  ''
               46  POP_JUMP_IF_TRUE     80  'to 80'

 L. 253        48  LOAD_GLOBAL              os
               50  LOAD_ATTR                path
               52  LOAD_METHOD              split
               54  LOAD_FAST                'archive'
               56  CALL_METHOD_1         1  ''
               58  UNPACK_SEQUENCE_2     2 
               60  STORE_FAST               'archive'
               62  STORE_FAST               'prefix'

 L. 254        64  LOAD_STR                 '/'
               66  LOAD_METHOD              join
               68  LOAD_FAST                'prefix'
               70  LOAD_FAST                'member'
               72  BUILD_LIST_2          2 
               74  CALL_METHOD_1         1  ''
               76  STORE_FAST               'member'
               78  JUMP_BACK            32  'to 32'
             80_0  COME_FROM            46  '46'
             80_1  COME_FROM            34  '34'

 L. 256        80  LOAD_GLOBAL              zipfile
               82  LOAD_METHOD              is_zipfile
               84  LOAD_FAST                'archive'
               86  CALL_METHOD_1         1  ''
               88  POP_JUMP_IF_TRUE     94  'to 94'

 L. 257        90  LOAD_FAST                'path'
               92  RETURN_VALUE     
             94_0  COME_FROM            88  '88'

 L. 259        94  LOAD_GLOBAL              zipfile
               96  LOAD_METHOD              ZipFile
               98  LOAD_FAST                'archive'
              100  CALL_METHOD_1         1  ''
              102  STORE_FAST               'zip_file'

 L. 260       104  LOAD_FAST                'member'
              106  LOAD_FAST                'zip_file'
              108  LOAD_METHOD              namelist
              110  CALL_METHOD_0         0  ''
              112  <118>                 1  ''
              114  POP_JUMP_IF_FALSE   120  'to 120'

 L. 261       116  LOAD_FAST                'path'
              118  RETURN_VALUE     
            120_0  COME_FROM           114  '114'

 L. 264       120  LOAD_GLOBAL              tempfile
              122  LOAD_METHOD              gettempdir
              124  CALL_METHOD_0         0  ''
              126  STORE_FAST               'tmp'

 L. 265       128  LOAD_GLOBAL              os
              130  LOAD_ATTR                path
              132  LOAD_METHOD              join
              134  LOAD_FAST                'tmp'
              136  LOAD_FAST                'member'
              138  LOAD_METHOD              split
              140  LOAD_STR                 '/'
              142  CALL_METHOD_1         1  ''
              144  LOAD_CONST               -1
              146  BINARY_SUBSCR    
              148  CALL_METHOD_2         2  ''
              150  STORE_FAST               'extracted_path'

 L. 266       152  LOAD_GLOBAL              os
              154  LOAD_ATTR                path
              156  LOAD_METHOD              exists
              158  LOAD_FAST                'extracted_path'
              160  CALL_METHOD_1         1  ''
              162  POP_JUMP_IF_TRUE    220  'to 220'

 L. 268       164  LOAD_GLOBAL              atomic_open
              166  LOAD_FAST                'extracted_path'
              168  CALL_FUNCTION_1       1  ''
              170  SETUP_WITH          204  'to 204'
              172  STORE_FAST               'file_handler'

 L. 269       174  LOAD_FAST                'file_handler'
              176  LOAD_METHOD              write
              178  LOAD_FAST                'zip_file'
              180  LOAD_METHOD              read
              182  LOAD_FAST                'member'
              184  CALL_METHOD_1         1  ''
              186  CALL_METHOD_1         1  ''
              188  POP_TOP          
              190  POP_BLOCK        
              192  LOAD_CONST               None
              194  DUP_TOP          
              196  DUP_TOP          
              198  CALL_FUNCTION_3       3  ''
              200  POP_TOP          
              202  JUMP_FORWARD        220  'to 220'
            204_0  COME_FROM_WITH      170  '170'
              204  <49>             
              206  POP_JUMP_IF_TRUE    210  'to 210'
              208  <48>             
            210_0  COME_FROM           206  '206'
              210  POP_TOP          
              212  POP_TOP          
              214  POP_TOP          
              216  POP_EXCEPT       
              218  POP_TOP          
            220_0  COME_FROM           202  '202'
            220_1  COME_FROM           162  '162'

 L. 270       220  LOAD_FAST                'extracted_path'
              222  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 112


@contextlib.contextmanager
def atomic_open--- This code section failed: ---

 L. 276         0  LOAD_GLOBAL              sys
                2  LOAD_ATTR                version_info
                4  LOAD_CONST               0
                6  BINARY_SUBSCR    
                8  LOAD_CONST               2
               10  COMPARE_OP               ==
               12  POP_JUMP_IF_FALSE    20  'to 20'
               14  LOAD_GLOBAL              os
               16  LOAD_ATTR                rename
               18  JUMP_FORWARD         24  'to 24'
             20_0  COME_FROM            12  '12'
               20  LOAD_GLOBAL              os
               22  LOAD_ATTR                replace
             24_0  COME_FROM            18  '18'
               24  STORE_FAST               'replacer'

 L. 277        26  LOAD_GLOBAL              tempfile
               28  LOAD_ATTR                mkstemp
               30  LOAD_GLOBAL              os
               32  LOAD_ATTR                path
               34  LOAD_METHOD              dirname
               36  LOAD_FAST                'filename'
               38  CALL_METHOD_1         1  ''
               40  LOAD_CONST               ('dir',)
               42  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               44  UNPACK_SEQUENCE_2     2 
               46  STORE_FAST               'tmp_descriptor'
               48  STORE_FAST               'tmp_name'

 L. 278        50  SETUP_FINALLY       116  'to 116'

 L. 279        52  LOAD_GLOBAL              os
               54  LOAD_METHOD              fdopen
               56  LOAD_FAST                'tmp_descriptor'
               58  LOAD_STR                 'wb'
               60  CALL_METHOD_2         2  ''
               62  SETUP_WITH           86  'to 86'
               64  STORE_FAST               'tmp_handler'

 L. 280        66  LOAD_FAST                'tmp_handler'
               68  YIELD_VALUE      
               70  POP_TOP          
               72  POP_BLOCK        
               74  LOAD_CONST               None
               76  DUP_TOP          
               78  DUP_TOP          
               80  CALL_FUNCTION_3       3  ''
               82  POP_TOP          
               84  JUMP_FORWARD        102  'to 102'
             86_0  COME_FROM_WITH       62  '62'
               86  <49>             
               88  POP_JUMP_IF_TRUE     92  'to 92'
               90  <48>             
             92_0  COME_FROM            88  '88'
               92  POP_TOP          
               94  POP_TOP          
               96  POP_TOP          
               98  POP_EXCEPT       
              100  POP_TOP          
            102_0  COME_FROM            84  '84'

 L. 281       102  LOAD_FAST                'replacer'
              104  LOAD_FAST                'tmp_name'
              106  LOAD_FAST                'filename'
              108  CALL_FUNCTION_2       2  ''
              110  POP_TOP          
              112  POP_BLOCK        
              114  JUMP_FORWARD        146  'to 146'
            116_0  COME_FROM_FINALLY    50  '50'

 L. 282       116  DUP_TOP          
              118  LOAD_GLOBAL              BaseException
              120  <121>               144  ''
              122  POP_TOP          
              124  POP_TOP          
              126  POP_TOP          

 L. 283       128  LOAD_GLOBAL              os
              130  LOAD_METHOD              remove
              132  LOAD_FAST                'tmp_name'
              134  CALL_METHOD_1         1  ''
              136  POP_TOP          

 L. 284       138  RAISE_VARARGS_0       0  'reraise'
              140  POP_EXCEPT       
              142  JUMP_FORWARD        146  'to 146'
              144  <48>             
            146_0  COME_FROM           142  '142'
            146_1  COME_FROM           114  '114'

Parse error at or near `DUP_TOP' instruction at offset 76


def from_key_val_list--- This code section failed: ---

 L. 305         0  LOAD_FAST                'value'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 306         8  LOAD_CONST               None
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L. 308        12  LOAD_GLOBAL              isinstance
               14  LOAD_FAST                'value'
               16  LOAD_GLOBAL              str
               18  LOAD_GLOBAL              bytes
               20  LOAD_GLOBAL              bool
               22  LOAD_GLOBAL              int
               24  BUILD_TUPLE_4         4 
               26  CALL_FUNCTION_2       2  ''
               28  POP_JUMP_IF_FALSE    38  'to 38'

 L. 309        30  LOAD_GLOBAL              ValueError
               32  LOAD_STR                 'cannot encode objects that are not 2-tuples'
               34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            28  '28'

 L. 311        38  LOAD_GLOBAL              OrderedDict
               40  LOAD_FAST                'value'
               42  CALL_FUNCTION_1       1  ''
               44  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def to_key_val_list--- This code section failed: ---

 L. 331         0  LOAD_FAST                'value'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 332         8  LOAD_CONST               None
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L. 334        12  LOAD_GLOBAL              isinstance
               14  LOAD_FAST                'value'
               16  LOAD_GLOBAL              str
               18  LOAD_GLOBAL              bytes
               20  LOAD_GLOBAL              bool
               22  LOAD_GLOBAL              int
               24  BUILD_TUPLE_4         4 
               26  CALL_FUNCTION_2       2  ''
               28  POP_JUMP_IF_FALSE    38  'to 38'

 L. 335        30  LOAD_GLOBAL              ValueError
               32  LOAD_STR                 'cannot encode objects that are not 2-tuples'
               34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            28  '28'

 L. 337        38  LOAD_GLOBAL              isinstance
               40  LOAD_FAST                'value'
               42  LOAD_GLOBAL              Mapping
               44  CALL_FUNCTION_2       2  ''
               46  POP_JUMP_IF_FALSE    56  'to 56'

 L. 338        48  LOAD_FAST                'value'
               50  LOAD_METHOD              items
               52  CALL_METHOD_0         0  ''
               54  STORE_FAST               'value'
             56_0  COME_FROM            46  '46'

 L. 340        56  LOAD_GLOBAL              list
               58  LOAD_FAST                'value'
               60  CALL_FUNCTION_1       1  ''
               62  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def parse_list_header(value):
    """Parse lists as described by RFC 2068 Section 2.

    In particular, parse comma-separated lists where the elements of
    the list may include quoted-strings.  A quoted-string could
    contain a comma.  A non-quoted string could have quotes in the
    middle.  Quotes are removed automatically after parsing.

    It basically works like :func:`parse_set_header` just that items
    may appear multiple times and case sensitivity is preserved.

    The return value is a standard :class:`list`:

    >>> parse_list_header('token, "quoted value"')
    ['token', 'quoted value']

    To create a header from the :class:`list` again, use the
    :func:`dump_header` function.

    :param value: a string with a list header.
    :return: :class:`list`
    :rtype: list
    """
    result = []
    for item in _parse_list_header(value):
        if item[:1] == item[-1:] == '"':
            item = unquote_header_value(item[1:-1])
        result.append(item)
    else:
        return result


def parse_dict_header--- This code section failed: ---

 L. 398         0  BUILD_MAP_0           0 
                2  STORE_FAST               'result'

 L. 399         4  LOAD_GLOBAL              _parse_list_header
                6  LOAD_FAST                'value'
                8  CALL_FUNCTION_1       1  ''
               10  GET_ITER         
               12  FOR_ITER            116  'to 116'
               14  STORE_FAST               'item'

 L. 400        16  LOAD_STR                 '='
               18  LOAD_FAST                'item'
               20  <118>                 1  ''
               22  POP_JUMP_IF_FALSE    34  'to 34'

 L. 401        24  LOAD_CONST               None
               26  LOAD_FAST                'result'
               28  LOAD_FAST                'item'
               30  STORE_SUBSCR     

 L. 402        32  JUMP_BACK            12  'to 12'
             34_0  COME_FROM            22  '22'

 L. 403        34  LOAD_FAST                'item'
               36  LOAD_METHOD              split
               38  LOAD_STR                 '='
               40  LOAD_CONST               1
               42  CALL_METHOD_2         2  ''
               44  UNPACK_SEQUENCE_2     2 
               46  STORE_FAST               'name'
               48  STORE_FAST               'value'

 L. 404        50  LOAD_FAST                'value'
               52  LOAD_CONST               None
               54  LOAD_CONST               1
               56  BUILD_SLICE_2         2 
               58  BINARY_SUBSCR    
               60  LOAD_FAST                'value'
               62  LOAD_CONST               -1
               64  LOAD_CONST               None
               66  BUILD_SLICE_2         2 
               68  BINARY_SUBSCR    
               70  DUP_TOP          
               72  ROT_THREE        
               74  COMPARE_OP               ==
               76  POP_JUMP_IF_FALSE    86  'to 86'
               78  LOAD_STR                 '"'
               80  COMPARE_OP               ==
               82  POP_JUMP_IF_FALSE   106  'to 106'
               84  JUMP_FORWARD         90  'to 90'
             86_0  COME_FROM            76  '76'
               86  POP_TOP          
               88  JUMP_FORWARD        106  'to 106'
             90_0  COME_FROM            84  '84'

 L. 405        90  LOAD_GLOBAL              unquote_header_value
               92  LOAD_FAST                'value'
               94  LOAD_CONST               1
               96  LOAD_CONST               -1
               98  BUILD_SLICE_2         2 
              100  BINARY_SUBSCR    
              102  CALL_FUNCTION_1       1  ''
              104  STORE_FAST               'value'
            106_0  COME_FROM            88  '88'
            106_1  COME_FROM            82  '82'

 L. 406       106  LOAD_FAST                'value'
              108  LOAD_FAST                'result'
              110  LOAD_FAST                'name'
              112  STORE_SUBSCR     
              114  JUMP_BACK            12  'to 12'

 L. 407       116  LOAD_FAST                'result'
              118  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 20


def unquote_header_value(value, is_filename=False):
    """Unquotes a header value.  (Reversal of :func:`quote_header_value`).
    This does not use the real unquoting but what browsers are actually
    using for quoting.

    :param value: the header value to unquote.
    :rtype: str
    """
    if value:
        if value[0] == value[(-1)] == '"':
            value = value[1:-1]
            if is_filename:
                if value[:2] != '\\\\':
                    return value.replace('\\\\', '\\').replace('\\"', '"')
    return value


def dict_from_cookiejar(cj):
    """Returns a key/value dictionary from a CookieJar.

    :param cj: CookieJar object to extract cookies from.
    :rtype: dict
    """
    cookie_dict = {}
    for cookie in cj:
        cookie_dict[cookie.name] = cookie.value
    else:
        return cookie_dict


def add_dict_to_cookiejar(cj, cookie_dict):
    """Returns a CookieJar from a key/value dictionary.

    :param cj: CookieJar to insert cookies into.
    :param cookie_dict: Dict of key/values to insert into CookieJar.
    :rtype: CookieJar
    """
    return cookiejar_from_dict(cookie_dict, cj)


def get_encodings_from_content(content):
    """Returns encodings from given content string.

    :param content: bytestring to extract encodings from.
    """
    warnings.warn('In requests 3.0, get_encodings_from_content will be removed. For more information, please see the discussion on issue #2266. (This warning should only appear once.)', DeprecationWarning)
    charset_re = re.compile('<meta.*?charset=["\\\']*(.+?)["\\\'>]', flags=(re.I))
    pragma_re = re.compile('<meta.*?content=["\\\']*;?charset=(.+?)["\\\'>]', flags=(re.I))
    xml_re = re.compile('^<\\?xml.*?encoding=["\\\']*(.+?)["\\\'>]')
    return charset_re.findall(content) + pragma_re.findall(content) + xml_re.findall(content)


def _parse_content_type_header(header):
    """Returns content type and parameters from given header

    :param header: string
    :return: tuple containing content type and dictionary of
         parameters
    """
    tokens = header.split(';')
    content_type, params = tokens[0].strip(), tokens[1:]
    params_dict = {}
    items_to_strip = '"\' '
    for param in params:
        param = param.strip()
        if param:
            key, value = param, True
            index_of_equals = param.find('=')
            if index_of_equals != -1:
                key = param[:index_of_equals].strip(items_to_strip)
                value = param[index_of_equals + 1:].strip(items_to_strip)
            params_dict[key.lower()] = value
        return (
         content_type, params_dict)


def get_encoding_from_headers--- This code section failed: ---

 L. 514         0  LOAD_FAST                'headers'
                2  LOAD_METHOD              get
                4  LOAD_STR                 'content-type'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'content_type'

 L. 516        10  LOAD_FAST                'content_type'
               12  POP_JUMP_IF_TRUE     18  'to 18'

 L. 517        14  LOAD_CONST               None
               16  RETURN_VALUE     
             18_0  COME_FROM            12  '12'

 L. 519        18  LOAD_GLOBAL              _parse_content_type_header
               20  LOAD_FAST                'content_type'
               22  CALL_FUNCTION_1       1  ''
               24  UNPACK_SEQUENCE_2     2 
               26  STORE_FAST               'content_type'
               28  STORE_FAST               'params'

 L. 521        30  LOAD_STR                 'charset'
               32  LOAD_FAST                'params'
               34  <118>                 0  ''
               36  POP_JUMP_IF_FALSE    52  'to 52'

 L. 522        38  LOAD_FAST                'params'
               40  LOAD_STR                 'charset'
               42  BINARY_SUBSCR    
               44  LOAD_METHOD              strip
               46  LOAD_STR                 '\'"'
               48  CALL_METHOD_1         1  ''
               50  RETURN_VALUE     
             52_0  COME_FROM            36  '36'

 L. 524        52  LOAD_STR                 'text'
               54  LOAD_FAST                'content_type'
               56  <118>                 0  ''
               58  POP_JUMP_IF_FALSE    64  'to 64'

 L. 525        60  LOAD_STR                 'ISO-8859-1'
               62  RETURN_VALUE     
             64_0  COME_FROM            58  '58'

 L. 527        64  LOAD_STR                 'application/json'
               66  LOAD_FAST                'content_type'
               68  <118>                 0  ''
               70  POP_JUMP_IF_FALSE    76  'to 76'

 L. 529        72  LOAD_STR                 'utf-8'
               74  RETURN_VALUE     
             76_0  COME_FROM            70  '70'

Parse error at or near `<118>' instruction at offset 34


def stream_decode_response_unicode--- This code section failed: ---

 L. 535         0  LOAD_FAST                'r'
                2  LOAD_ATTR                encoding
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    30  'to 30'

 L. 536        10  LOAD_FAST                'iterator'
               12  GET_ITER         
               14  FOR_ITER             26  'to 26'
               16  STORE_FAST               'item'

 L. 537        18  LOAD_FAST                'item'
               20  YIELD_VALUE      
               22  POP_TOP          
               24  JUMP_BACK            14  'to 14'

 L. 538        26  LOAD_CONST               None
               28  RETURN_VALUE     
             30_0  COME_FROM             8  '8'

 L. 540        30  LOAD_GLOBAL              codecs
               32  LOAD_METHOD              getincrementaldecoder
               34  LOAD_FAST                'r'
               36  LOAD_ATTR                encoding
               38  CALL_METHOD_1         1  ''
               40  LOAD_STR                 'replace'
               42  LOAD_CONST               ('errors',)
               44  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               46  STORE_FAST               'decoder'

 L. 541        48  LOAD_FAST                'iterator'
               50  GET_ITER         
             52_0  COME_FROM            68  '68'
               52  FOR_ITER             78  'to 78'
               54  STORE_FAST               'chunk'

 L. 542        56  LOAD_FAST                'decoder'
               58  LOAD_METHOD              decode
               60  LOAD_FAST                'chunk'
               62  CALL_METHOD_1         1  ''
               64  STORE_FAST               'rv'

 L. 543        66  LOAD_FAST                'rv'
               68  POP_JUMP_IF_FALSE    52  'to 52'

 L. 544        70  LOAD_FAST                'rv'
               72  YIELD_VALUE      
               74  POP_TOP          
               76  JUMP_BACK            52  'to 52'

 L. 545        78  LOAD_FAST                'decoder'
               80  LOAD_ATTR                decode
               82  LOAD_CONST               b''
               84  LOAD_CONST               True
               86  LOAD_CONST               ('final',)
               88  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               90  STORE_FAST               'rv'

 L. 546        92  LOAD_FAST                'rv'
               94  POP_JUMP_IF_FALSE   102  'to 102'

 L. 547        96  LOAD_FAST                'rv'
               98  YIELD_VALUE      
              100  POP_TOP          
            102_0  COME_FROM            94  '94'

Parse error at or near `None' instruction at offset -1


def iter_slices--- This code section failed: ---

 L. 552         0  LOAD_CONST               0
                2  STORE_FAST               'pos'

 L. 553         4  LOAD_FAST                'slice_length'
                6  LOAD_CONST               None
                8  <117>                 0  ''
               10  POP_JUMP_IF_TRUE     20  'to 20'
               12  LOAD_FAST                'slice_length'
               14  LOAD_CONST               0
               16  COMPARE_OP               <=
               18  POP_JUMP_IF_FALSE    28  'to 28'
             20_0  COME_FROM            10  '10'

 L. 554        20  LOAD_GLOBAL              len
               22  LOAD_FAST                'string'
               24  CALL_FUNCTION_1       1  ''
               26  STORE_FAST               'slice_length'
             28_0  COME_FROM            18  '18'

 L. 555        28  LOAD_FAST                'pos'
               30  LOAD_GLOBAL              len
               32  LOAD_FAST                'string'
               34  CALL_FUNCTION_1       1  ''
               36  COMPARE_OP               <
               38  POP_JUMP_IF_FALSE    68  'to 68'

 L. 556        40  LOAD_FAST                'string'
               42  LOAD_FAST                'pos'
               44  LOAD_FAST                'pos'
               46  LOAD_FAST                'slice_length'
               48  BINARY_ADD       
               50  BUILD_SLICE_2         2 
               52  BINARY_SUBSCR    
               54  YIELD_VALUE      
               56  POP_TOP          

 L. 557        58  LOAD_FAST                'pos'
               60  LOAD_FAST                'slice_length'
               62  INPLACE_ADD      
               64  STORE_FAST               'pos'
               66  JUMP_BACK            28  'to 28'
             68_0  COME_FROM            38  '38'

Parse error at or near `<117>' instruction at offset 8


def get_unicode_from_response--- This code section failed: ---

 L. 572         0  LOAD_GLOBAL              warnings
                2  LOAD_METHOD              warn

 L. 573         4  LOAD_STR                 'In requests 3.0, get_unicode_from_response will be removed. For more information, please see the discussion on issue #2266. (This warning should only appear once.)'

 L. 576         6  LOAD_GLOBAL              DeprecationWarning

 L. 572         8  CALL_METHOD_2         2  ''
               10  POP_TOP          

 L. 578        12  BUILD_LIST_0          0 
               14  STORE_FAST               'tried_encodings'

 L. 581        16  LOAD_GLOBAL              get_encoding_from_headers
               18  LOAD_FAST                'r'
               20  LOAD_ATTR                headers
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'encoding'

 L. 583        26  LOAD_FAST                'encoding'
               28  POP_JUMP_IF_FALSE    74  'to 74'

 L. 584        30  SETUP_FINALLY        46  'to 46'

 L. 585        32  LOAD_GLOBAL              str
               34  LOAD_FAST                'r'
               36  LOAD_ATTR                content
               38  LOAD_FAST                'encoding'
               40  CALL_FUNCTION_2       2  ''
               42  POP_BLOCK        
               44  RETURN_VALUE     
             46_0  COME_FROM_FINALLY    30  '30'

 L. 586        46  DUP_TOP          
               48  LOAD_GLOBAL              UnicodeError
               50  <121>                72  ''
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          

 L. 587        58  LOAD_FAST                'tried_encodings'
               60  LOAD_METHOD              append
               62  LOAD_FAST                'encoding'
               64  CALL_METHOD_1         1  ''
               66  POP_TOP          
               68  POP_EXCEPT       
               70  JUMP_FORWARD         74  'to 74'
               72  <48>             
             74_0  COME_FROM            70  '70'
             74_1  COME_FROM            28  '28'

 L. 590        74  SETUP_FINALLY        94  'to 94'

 L. 591        76  LOAD_GLOBAL              str
               78  LOAD_FAST                'r'
               80  LOAD_ATTR                content
               82  LOAD_FAST                'encoding'
               84  LOAD_STR                 'replace'
               86  LOAD_CONST               ('errors',)
               88  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               90  POP_BLOCK        
               92  RETURN_VALUE     
             94_0  COME_FROM_FINALLY    74  '74'

 L. 592        94  DUP_TOP          
               96  LOAD_GLOBAL              TypeError
               98  <121>               116  ''
              100  POP_TOP          
              102  POP_TOP          
              104  POP_TOP          

 L. 593       106  LOAD_FAST                'r'
              108  LOAD_ATTR                content
              110  ROT_FOUR         
              112  POP_EXCEPT       
              114  RETURN_VALUE     
              116  <48>             

Parse error at or near `<121>' instruction at offset 50


UNRESERVED_SET = frozenset('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~')

def unquote_unreserved--- This code section failed: ---

 L. 607         0  LOAD_FAST                'uri'
                2  LOAD_METHOD              split
                4  LOAD_STR                 '%'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'parts'

 L. 608        10  LOAD_GLOBAL              range
               12  LOAD_CONST               1
               14  LOAD_GLOBAL              len
               16  LOAD_FAST                'parts'
               18  CALL_FUNCTION_1       1  ''
               20  CALL_FUNCTION_2       2  ''
               22  GET_ITER         
               24  FOR_ITER            184  'to 184'
               26  STORE_FAST               'i'

 L. 609        28  LOAD_FAST                'parts'
               30  LOAD_FAST                'i'
               32  BINARY_SUBSCR    
               34  LOAD_CONST               0
               36  LOAD_CONST               2
               38  BUILD_SLICE_2         2 
               40  BINARY_SUBSCR    
               42  STORE_FAST               'h'

 L. 610        44  LOAD_GLOBAL              len
               46  LOAD_FAST                'h'
               48  CALL_FUNCTION_1       1  ''
               50  LOAD_CONST               2
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_FALSE   166  'to 166'
               56  LOAD_FAST                'h'
               58  LOAD_METHOD              isalnum
               60  CALL_METHOD_0         0  ''
               62  POP_JUMP_IF_FALSE   166  'to 166'

 L. 611        64  SETUP_FINALLY        84  'to 84'

 L. 612        66  LOAD_GLOBAL              chr
               68  LOAD_GLOBAL              int
               70  LOAD_FAST                'h'
               72  LOAD_CONST               16
               74  CALL_FUNCTION_2       2  ''
               76  CALL_FUNCTION_1       1  ''
               78  STORE_FAST               'c'
               80  POP_BLOCK        
               82  JUMP_FORWARD        114  'to 114'
             84_0  COME_FROM_FINALLY    64  '64'

 L. 613        84  DUP_TOP          
               86  LOAD_GLOBAL              ValueError
               88  <121>               112  ''
               90  POP_TOP          
               92  POP_TOP          
               94  POP_TOP          

 L. 614        96  LOAD_GLOBAL              InvalidURL
               98  LOAD_STR                 "Invalid percent-escape sequence: '%s'"
              100  LOAD_FAST                'h'
              102  BINARY_MODULO    
              104  CALL_FUNCTION_1       1  ''
              106  RAISE_VARARGS_1       1  'exception instance'
              108  POP_EXCEPT       
              110  JUMP_FORWARD        114  'to 114'
              112  <48>             
            114_0  COME_FROM           110  '110'
            114_1  COME_FROM            82  '82'

 L. 616       114  LOAD_FAST                'c'
              116  LOAD_GLOBAL              UNRESERVED_SET
              118  <118>                 0  ''
              120  POP_JUMP_IF_FALSE   148  'to 148'

 L. 617       122  LOAD_FAST                'c'
              124  LOAD_FAST                'parts'
              126  LOAD_FAST                'i'
              128  BINARY_SUBSCR    
              130  LOAD_CONST               2
              132  LOAD_CONST               None
              134  BUILD_SLICE_2         2 
              136  BINARY_SUBSCR    
              138  BINARY_ADD       
              140  LOAD_FAST                'parts'
              142  LOAD_FAST                'i'
              144  STORE_SUBSCR     
              146  JUMP_ABSOLUTE       182  'to 182'
            148_0  COME_FROM           120  '120'

 L. 619       148  LOAD_STR                 '%'
              150  LOAD_FAST                'parts'
              152  LOAD_FAST                'i'
              154  BINARY_SUBSCR    
              156  BINARY_ADD       
              158  LOAD_FAST                'parts'
              160  LOAD_FAST                'i'
              162  STORE_SUBSCR     
              164  JUMP_BACK            24  'to 24'
            166_0  COME_FROM            62  '62'
            166_1  COME_FROM            54  '54'

 L. 621       166  LOAD_STR                 '%'
              168  LOAD_FAST                'parts'
              170  LOAD_FAST                'i'
              172  BINARY_SUBSCR    
              174  BINARY_ADD       
              176  LOAD_FAST                'parts'
              178  LOAD_FAST                'i'
              180  STORE_SUBSCR     
              182  JUMP_BACK            24  'to 24'

 L. 622       184  LOAD_STR                 ''
              186  LOAD_METHOD              join
              188  LOAD_FAST                'parts'
              190  CALL_METHOD_1         1  ''
              192  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 88


def requote_uri--- This code section failed: ---

 L. 633         0  LOAD_STR                 "!#$%&'()*+,/:;=?@[]~"
                2  STORE_FAST               'safe_with_percent'

 L. 634         4  LOAD_STR                 "!#$&'()*+,/:;=?@[]~"
                6  STORE_FAST               'safe_without_percent'

 L. 635         8  SETUP_FINALLY        28  'to 28'

 L. 639        10  LOAD_GLOBAL              quote
               12  LOAD_GLOBAL              unquote_unreserved
               14  LOAD_FAST                'uri'
               16  CALL_FUNCTION_1       1  ''
               18  LOAD_FAST                'safe_with_percent'
               20  LOAD_CONST               ('safe',)
               22  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               24  POP_BLOCK        
               26  RETURN_VALUE     
             28_0  COME_FROM_FINALLY     8  '8'

 L. 640        28  DUP_TOP          
               30  LOAD_GLOBAL              InvalidURL
               32  <121>                56  ''
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L. 644        40  LOAD_GLOBAL              quote
               42  LOAD_FAST                'uri'
               44  LOAD_FAST                'safe_without_percent'
               46  LOAD_CONST               ('safe',)
               48  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               50  ROT_FOUR         
               52  POP_EXCEPT       
               54  RETURN_VALUE     
               56  <48>             

Parse error at or near `<121>' instruction at offset 32


def address_in_network(ip, net):
    """This function allows you to check if an IP belongs to a network subnet

    Example: returns True if ip = 192.168.1.1 and net = 192.168.1.0/24
             returns False if ip = 192.168.1.1 and net = 192.168.100.0/24

    :rtype: bool
    """
    ipaddr = struct.unpack('=L', socket.inet_aton(ip))[0]
    netaddr, bits = net.split('/')
    netmask = struct.unpack('=L', socket.inet_aton(dotted_netmask(int(bits))))[0]
    network = struct.unpack('=L', socket.inet_aton(netaddr))[0] & netmask
    return ipaddr & netmask == network & netmask


def dotted_netmask(mask):
    """Converts mask from /xx format to xxx.xxx.xxx.xxx

    Example: if mask is 24 function returns 255.255.255.0

    :rtype: str
    """
    bits = 4294967295 ^ (1 << 32 - mask) - 1
    return socket.inet_ntoa(struct.pack('>I', bits))


def is_ipv4_address--- This code section failed: ---

 L. 677         0  SETUP_FINALLY        16  'to 16'

 L. 678         2  LOAD_GLOBAL              socket
                4  LOAD_METHOD              inet_aton
                6  LOAD_FAST                'string_ip'
                8  CALL_METHOD_1         1  ''
               10  POP_TOP          
               12  POP_BLOCK        
               14  JUMP_FORWARD         38  'to 38'
             16_0  COME_FROM_FINALLY     0  '0'

 L. 679        16  DUP_TOP          
               18  LOAD_GLOBAL              socket
               20  LOAD_ATTR                error
               22  <121>                36  ''
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 680        30  POP_EXCEPT       
               32  LOAD_CONST               False
               34  RETURN_VALUE     
               36  <48>             
             38_0  COME_FROM            14  '14'

 L. 681        38  LOAD_CONST               True
               40  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 22


def is_valid_cidr--- This code section failed: ---

 L. 690         0  LOAD_FAST                'string_network'
                2  LOAD_METHOD              count
                4  LOAD_STR                 '/'
                6  CALL_METHOD_1         1  ''
                8  LOAD_CONST               1
               10  COMPARE_OP               ==
               12  POP_JUMP_IF_FALSE   128  'to 128'

 L. 691        14  SETUP_FINALLY        38  'to 38'

 L. 692        16  LOAD_GLOBAL              int
               18  LOAD_FAST                'string_network'
               20  LOAD_METHOD              split
               22  LOAD_STR                 '/'
               24  CALL_METHOD_1         1  ''
               26  LOAD_CONST               1
               28  BINARY_SUBSCR    
               30  CALL_FUNCTION_1       1  ''
               32  STORE_FAST               'mask'
               34  POP_BLOCK        
               36  JUMP_FORWARD         58  'to 58'
             38_0  COME_FROM_FINALLY    14  '14'

 L. 693        38  DUP_TOP          
               40  LOAD_GLOBAL              ValueError
               42  <121>                56  ''
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L. 694        50  POP_EXCEPT       
               52  LOAD_CONST               False
               54  RETURN_VALUE     
               56  <48>             
             58_0  COME_FROM            36  '36'

 L. 696        58  LOAD_FAST                'mask'
               60  LOAD_CONST               1
               62  COMPARE_OP               <
               64  POP_JUMP_IF_TRUE     74  'to 74'
               66  LOAD_FAST                'mask'
               68  LOAD_CONST               32
               70  COMPARE_OP               >
               72  POP_JUMP_IF_FALSE    78  'to 78'
             74_0  COME_FROM            64  '64'

 L. 697        74  LOAD_CONST               False
               76  RETURN_VALUE     
             78_0  COME_FROM            72  '72'

 L. 699        78  SETUP_FINALLY       104  'to 104'

 L. 700        80  LOAD_GLOBAL              socket
               82  LOAD_METHOD              inet_aton
               84  LOAD_FAST                'string_network'
               86  LOAD_METHOD              split
               88  LOAD_STR                 '/'
               90  CALL_METHOD_1         1  ''
               92  LOAD_CONST               0
               94  BINARY_SUBSCR    
               96  CALL_METHOD_1         1  ''
               98  POP_TOP          
              100  POP_BLOCK        
              102  JUMP_ABSOLUTE       132  'to 132'
            104_0  COME_FROM_FINALLY    78  '78'

 L. 701       104  DUP_TOP          
              106  LOAD_GLOBAL              socket
              108  LOAD_ATTR                error
              110  <121>               124  ''
              112  POP_TOP          
              114  POP_TOP          
              116  POP_TOP          

 L. 702       118  POP_EXCEPT       
              120  LOAD_CONST               False
              122  RETURN_VALUE     
              124  <48>             
              126  JUMP_FORWARD        132  'to 132'
            128_0  COME_FROM            12  '12'

 L. 704       128  LOAD_CONST               False
              130  RETURN_VALUE     
            132_0  COME_FROM           126  '126'

 L. 705       132  LOAD_CONST               True
              134  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 42


@contextlib.contextmanager
def set_environ--- This code section failed: ---

 L. 716         0  LOAD_FAST                'value'
                2  LOAD_CONST               None
                4  <117>                 1  ''
                6  STORE_FAST               'value_changed'

 L. 717         8  LOAD_FAST                'value_changed'
               10  POP_JUMP_IF_FALSE    34  'to 34'

 L. 718        12  LOAD_GLOBAL              os
               14  LOAD_ATTR                environ
               16  LOAD_METHOD              get
               18  LOAD_FAST                'env_name'
               20  CALL_METHOD_1         1  ''
               22  STORE_FAST               'old_value'

 L. 719        24  LOAD_FAST                'value'
               26  LOAD_GLOBAL              os
               28  LOAD_ATTR                environ
               30  LOAD_FAST                'env_name'
               32  STORE_SUBSCR     
             34_0  COME_FROM            10  '10'

 L. 720        34  SETUP_FINALLY        78  'to 78'

 L. 721        36  LOAD_CONST               None
               38  YIELD_VALUE      
               40  POP_TOP          
               42  POP_BLOCK        

 L. 723        44  LOAD_FAST                'value_changed'
               46  POP_JUMP_IF_FALSE   112  'to 112'

 L. 724        48  LOAD_FAST                'old_value'
               50  LOAD_CONST               None
               52  <117>                 0  ''
               54  POP_JUMP_IF_FALSE    66  'to 66'

 L. 725        56  LOAD_GLOBAL              os
               58  LOAD_ATTR                environ
               60  LOAD_FAST                'env_name'
               62  DELETE_SUBSCR    
               64  JUMP_ABSOLUTE       112  'to 112'
             66_0  COME_FROM            54  '54'

 L. 727        66  LOAD_FAST                'old_value'
               68  LOAD_GLOBAL              os
               70  LOAD_ATTR                environ
               72  LOAD_FAST                'env_name'
               74  STORE_SUBSCR     
               76  JUMP_FORWARD        112  'to 112'
             78_0  COME_FROM_FINALLY    34  '34'

 L. 723        78  LOAD_FAST                'value_changed'
               80  POP_JUMP_IF_FALSE   110  'to 110'

 L. 724        82  LOAD_FAST                'old_value'
               84  LOAD_CONST               None
               86  <117>                 0  ''
               88  POP_JUMP_IF_FALSE   100  'to 100'

 L. 725        90  LOAD_GLOBAL              os
               92  LOAD_ATTR                environ
               94  LOAD_FAST                'env_name'
               96  DELETE_SUBSCR    
               98  JUMP_FORWARD        110  'to 110'
            100_0  COME_FROM            88  '88'

 L. 727       100  LOAD_FAST                'old_value'
              102  LOAD_GLOBAL              os
              104  LOAD_ATTR                environ
              106  LOAD_FAST                'env_name'
              108  STORE_SUBSCR     
            110_0  COME_FROM            98  '98'
            110_1  COME_FROM            80  '80'
              110  <48>             
            112_0  COME_FROM            76  '76'
            112_1  COME_FROM            46  '46'

Parse error at or near `None' instruction at offset -1


def should_bypass_proxies--- This code section failed: ---

 L. 738         0  LOAD_LAMBDA              '<code_object <lambda>>'
                2  LOAD_STR                 'should_bypass_proxies.<locals>.<lambda>'
                4  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                6  STORE_FAST               'get_proxy'

 L. 742         8  LOAD_FAST                'no_proxy'
               10  STORE_FAST               'no_proxy_arg'

 L. 743        12  LOAD_FAST                'no_proxy'
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    28  'to 28'

 L. 744        20  LOAD_FAST                'get_proxy'
               22  LOAD_STR                 'no_proxy'
               24  CALL_FUNCTION_1       1  ''
               26  STORE_FAST               'no_proxy'
             28_0  COME_FROM            18  '18'

 L. 745        28  LOAD_GLOBAL              urlparse
               30  LOAD_FAST                'url'
               32  CALL_FUNCTION_1       1  ''
               34  STORE_FAST               'parsed'

 L. 747        36  LOAD_FAST                'parsed'
               38  LOAD_ATTR                hostname
               40  LOAD_CONST               None
               42  <117>                 0  ''
               44  POP_JUMP_IF_FALSE    50  'to 50'

 L. 749        46  LOAD_CONST               True
               48  RETURN_VALUE     
             50_0  COME_FROM            44  '44'

 L. 751        50  LOAD_FAST                'no_proxy'
               52  POP_JUMP_IF_FALSE   214  'to 214'

 L. 754        54  LOAD_GENEXPR             '<code_object <genexpr>>'
               56  LOAD_STR                 'should_bypass_proxies.<locals>.<genexpr>'
               58  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 755        60  LOAD_FAST                'no_proxy'
               62  LOAD_METHOD              replace
               64  LOAD_STR                 ' '
               66  LOAD_STR                 ''
               68  CALL_METHOD_2         2  ''
               70  LOAD_METHOD              split
               72  LOAD_STR                 ','
               74  CALL_METHOD_1         1  ''

 L. 754        76  GET_ITER         
               78  CALL_FUNCTION_1       1  ''
               80  STORE_FAST               'no_proxy'

 L. 758        82  LOAD_GLOBAL              is_ipv4_address
               84  LOAD_FAST                'parsed'
               86  LOAD_ATTR                hostname
               88  CALL_FUNCTION_1       1  ''
               90  POP_JUMP_IF_FALSE   148  'to 148'

 L. 759        92  LOAD_FAST                'no_proxy'
               94  GET_ITER         
             96_0  COME_FROM           136  '136'
               96  FOR_ITER            146  'to 146'
               98  STORE_FAST               'proxy_ip'

 L. 760       100  LOAD_GLOBAL              is_valid_cidr
              102  LOAD_FAST                'proxy_ip'
              104  CALL_FUNCTION_1       1  ''
              106  POP_JUMP_IF_FALSE   128  'to 128'

 L. 761       108  LOAD_GLOBAL              address_in_network
              110  LOAD_FAST                'parsed'
              112  LOAD_ATTR                hostname
              114  LOAD_FAST                'proxy_ip'
              116  CALL_FUNCTION_2       2  ''
              118  POP_JUMP_IF_FALSE   144  'to 144'

 L. 762       120  POP_TOP          
              122  LOAD_CONST               True
              124  RETURN_VALUE     
              126  JUMP_BACK            96  'to 96'
            128_0  COME_FROM           106  '106'

 L. 763       128  LOAD_FAST                'parsed'
              130  LOAD_ATTR                hostname
              132  LOAD_FAST                'proxy_ip'
              134  COMPARE_OP               ==
              136  POP_JUMP_IF_FALSE    96  'to 96'

 L. 766       138  POP_TOP          
              140  LOAD_CONST               True
              142  RETURN_VALUE     
            144_0  COME_FROM           118  '118'
              144  JUMP_BACK            96  'to 96'
              146  JUMP_FORWARD        214  'to 214'
            148_0  COME_FROM            90  '90'

 L. 768       148  LOAD_FAST                'parsed'
              150  LOAD_ATTR                hostname
              152  STORE_FAST               'host_with_port'

 L. 769       154  LOAD_FAST                'parsed'
              156  LOAD_ATTR                port
              158  POP_JUMP_IF_FALSE   176  'to 176'

 L. 770       160  LOAD_FAST                'host_with_port'
              162  LOAD_STR                 ':{}'
              164  LOAD_METHOD              format
              166  LOAD_FAST                'parsed'
              168  LOAD_ATTR                port
              170  CALL_METHOD_1         1  ''
              172  INPLACE_ADD      
              174  STORE_FAST               'host_with_port'
            176_0  COME_FROM           158  '158'

 L. 772       176  LOAD_FAST                'no_proxy'
              178  GET_ITER         
            180_0  COME_FROM           204  '204'
              180  FOR_ITER            214  'to 214'
              182  STORE_FAST               'host'

 L. 773       184  LOAD_FAST                'parsed'
              186  LOAD_ATTR                hostname
              188  LOAD_METHOD              endswith
              190  LOAD_FAST                'host'
              192  CALL_METHOD_1         1  ''
              194  POP_JUMP_IF_TRUE    206  'to 206'
              196  LOAD_FAST                'host_with_port'
              198  LOAD_METHOD              endswith
              200  LOAD_FAST                'host'
              202  CALL_METHOD_1         1  ''
              204  POP_JUMP_IF_FALSE   180  'to 180'
            206_0  COME_FROM           194  '194'

 L. 776       206  POP_TOP          
              208  LOAD_CONST               True
              210  RETURN_VALUE     
              212  JUMP_BACK           180  'to 180'
            214_0  COME_FROM           146  '146'
            214_1  COME_FROM            52  '52'

 L. 778       214  LOAD_GLOBAL              set_environ
              216  LOAD_STR                 'no_proxy'
              218  LOAD_FAST                'no_proxy_arg'
              220  CALL_FUNCTION_2       2  ''
              222  SETUP_WITH          286  'to 286'
              224  POP_TOP          

 L. 780       226  SETUP_FINALLY       242  'to 242'

 L. 781       228  LOAD_GLOBAL              proxy_bypass
              230  LOAD_FAST                'parsed'
              232  LOAD_ATTR                hostname
              234  CALL_FUNCTION_1       1  ''
              236  STORE_FAST               'bypass'
              238  POP_BLOCK        
              240  JUMP_FORWARD        272  'to 272'
            242_0  COME_FROM_FINALLY   226  '226'

 L. 782       242  DUP_TOP          
              244  LOAD_GLOBAL              TypeError
              246  LOAD_GLOBAL              socket
              248  LOAD_ATTR                gaierror
              250  BUILD_TUPLE_2         2 
          252_254  <121>               270  ''
              256  POP_TOP          
              258  POP_TOP          
              260  POP_TOP          

 L. 783       262  LOAD_CONST               False
              264  STORE_FAST               'bypass'
              266  POP_EXCEPT       
              268  JUMP_FORWARD        272  'to 272'
              270  <48>             
            272_0  COME_FROM           268  '268'
            272_1  COME_FROM           240  '240'
              272  POP_BLOCK        
              274  LOAD_CONST               None
              276  DUP_TOP          
              278  DUP_TOP          
              280  CALL_FUNCTION_3       3  ''
              282  POP_TOP          
              284  JUMP_FORWARD        304  'to 304'
            286_0  COME_FROM_WITH      222  '222'
              286  <49>             
          288_290  POP_JUMP_IF_TRUE    294  'to 294'
              292  <48>             
            294_0  COME_FROM           288  '288'
              294  POP_TOP          
              296  POP_TOP          
              298  POP_TOP          
              300  POP_EXCEPT       
              302  POP_TOP          
            304_0  COME_FROM           284  '284'

 L. 785       304  LOAD_FAST                'bypass'
          306_308  POP_JUMP_IF_FALSE   314  'to 314'

 L. 786       310  LOAD_CONST               True
              312  RETURN_VALUE     
            314_0  COME_FROM           306  '306'

 L. 788       314  LOAD_CONST               False
              316  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 16


def get_environ_proxies(url, no_proxy=None):
    """
    Return a dict of environment proxies.

    :rtype: dict
    """
    if should_bypass_proxies(url, no_proxy=no_proxy):
        return {}
    return getproxies()


def select_proxy--- This code section failed: ---

 L. 809         0  LOAD_FAST                'proxies'
                2  JUMP_IF_TRUE_OR_POP     6  'to 6'
                4  BUILD_MAP_0           0 
              6_0  COME_FROM             2  '2'
                6  STORE_FAST               'proxies'

 L. 810         8  LOAD_GLOBAL              urlparse
               10  LOAD_FAST                'url'
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'urlparts'

 L. 811        16  LOAD_FAST                'urlparts'
               18  LOAD_ATTR                hostname
               20  LOAD_CONST               None
               22  <117>                 0  ''
               24  POP_JUMP_IF_FALSE    46  'to 46'

 L. 812        26  LOAD_FAST                'proxies'
               28  LOAD_METHOD              get
               30  LOAD_FAST                'urlparts'
               32  LOAD_ATTR                scheme
               34  LOAD_FAST                'proxies'
               36  LOAD_METHOD              get
               38  LOAD_STR                 'all'
               40  CALL_METHOD_1         1  ''
               42  CALL_METHOD_2         2  ''
               44  RETURN_VALUE     
             46_0  COME_FROM            24  '24'

 L. 815        46  LOAD_FAST                'urlparts'
               48  LOAD_ATTR                scheme
               50  LOAD_STR                 '://'
               52  BINARY_ADD       
               54  LOAD_FAST                'urlparts'
               56  LOAD_ATTR                hostname
               58  BINARY_ADD       

 L. 816        60  LOAD_FAST                'urlparts'
               62  LOAD_ATTR                scheme

 L. 817        64  LOAD_STR                 'all://'
               66  LOAD_FAST                'urlparts'
               68  LOAD_ATTR                hostname
               70  BINARY_ADD       

 L. 818        72  LOAD_STR                 'all'

 L. 814        74  BUILD_LIST_4          4 
               76  STORE_FAST               'proxy_keys'

 L. 820        78  LOAD_CONST               None
               80  STORE_FAST               'proxy'

 L. 821        82  LOAD_FAST                'proxy_keys'
               84  GET_ITER         
             86_0  COME_FROM            96  '96'
               86  FOR_ITER            112  'to 112'
               88  STORE_FAST               'proxy_key'

 L. 822        90  LOAD_FAST                'proxy_key'
               92  LOAD_FAST                'proxies'
               94  <118>                 0  ''
               96  POP_JUMP_IF_FALSE    86  'to 86'

 L. 823        98  LOAD_FAST                'proxies'
              100  LOAD_FAST                'proxy_key'
              102  BINARY_SUBSCR    
              104  STORE_FAST               'proxy'

 L. 824       106  POP_TOP          
              108  BREAK_LOOP          112  'to 112'
              110  JUMP_BACK            86  'to 86'

 L. 826       112  LOAD_FAST                'proxy'
              114  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 22


def default_user_agent(name='python-requests'):
    """
    Return a string representing the default user agent.

    :rtype: str
    """
    return '%s/%s' % (name, __version__)


def default_headers():
    """
    :rtype: requests.structures.CaseInsensitiveDict
    """
    return CaseInsensitiveDict({'User-Agent':default_user_agent(), 
     'Accept-Encoding':DEFAULT_ACCEPT_ENCODING, 
     'Accept':'*/*', 
     'Connection':'keep-alive'})


def parse_header_links--- This code section failed: ---

 L. 858         0  BUILD_LIST_0          0 
                2  STORE_FAST               'links'

 L. 860         4  LOAD_STR                 ' \'"'
                6  STORE_FAST               'replace_chars'

 L. 862         8  LOAD_FAST                'value'
               10  LOAD_METHOD              strip
               12  LOAD_FAST                'replace_chars'
               14  CALL_METHOD_1         1  ''
               16  STORE_FAST               'value'

 L. 863        18  LOAD_FAST                'value'
               20  POP_JUMP_IF_TRUE     26  'to 26'

 L. 864        22  LOAD_FAST                'links'
               24  RETURN_VALUE     
             26_0  COME_FROM            20  '20'

 L. 866        26  LOAD_GLOBAL              re
               28  LOAD_METHOD              split
               30  LOAD_STR                 ', *<'
               32  LOAD_FAST                'value'
               34  CALL_METHOD_2         2  ''
               36  GET_ITER         
               38  FOR_ITER            198  'to 198'
               40  STORE_FAST               'val'

 L. 867        42  SETUP_FINALLY        64  'to 64'

 L. 868        44  LOAD_FAST                'val'
               46  LOAD_METHOD              split
               48  LOAD_STR                 ';'
               50  LOAD_CONST               1
               52  CALL_METHOD_2         2  ''
               54  UNPACK_SEQUENCE_2     2 
               56  STORE_FAST               'url'
               58  STORE_FAST               'params'
               60  POP_BLOCK        
               62  JUMP_FORWARD         92  'to 92'
             64_0  COME_FROM_FINALLY    42  '42'

 L. 869        64  DUP_TOP          
               66  LOAD_GLOBAL              ValueError
               68  <121>                90  ''
               70  POP_TOP          
               72  POP_TOP          
               74  POP_TOP          

 L. 870        76  LOAD_FAST                'val'
               78  LOAD_STR                 ''
               80  ROT_TWO          
               82  STORE_FAST               'url'
               84  STORE_FAST               'params'
               86  POP_EXCEPT       
               88  JUMP_FORWARD         92  'to 92'
               90  <48>             
             92_0  COME_FROM            88  '88'
             92_1  COME_FROM            62  '62'

 L. 872        92  LOAD_STR                 'url'
               94  LOAD_FAST                'url'
               96  LOAD_METHOD              strip
               98  LOAD_STR                 '<> \'"'
              100  CALL_METHOD_1         1  ''
              102  BUILD_MAP_1           1 
              104  STORE_FAST               'link'

 L. 874       106  LOAD_FAST                'params'
              108  LOAD_METHOD              split
              110  LOAD_STR                 ';'
              112  CALL_METHOD_1         1  ''
              114  GET_ITER         
              116  FOR_ITER            186  'to 186'
              118  STORE_FAST               'param'

 L. 875       120  SETUP_FINALLY       140  'to 140'

 L. 876       122  LOAD_FAST                'param'
              124  LOAD_METHOD              split
              126  LOAD_STR                 '='
              128  CALL_METHOD_1         1  ''
              130  UNPACK_SEQUENCE_2     2 
              132  STORE_FAST               'key'
              134  STORE_FAST               'value'
              136  POP_BLOCK        
              138  JUMP_FORWARD        164  'to 164'
            140_0  COME_FROM_FINALLY   120  '120'

 L. 877       140  DUP_TOP          
              142  LOAD_GLOBAL              ValueError
              144  <121>               162  ''
              146  POP_TOP          
              148  POP_TOP          
              150  POP_TOP          

 L. 878       152  POP_EXCEPT       
              154  POP_TOP          
              156  BREAK_LOOP          186  'to 186'
              158  POP_EXCEPT       
              160  JUMP_FORWARD        164  'to 164'
              162  <48>             
            164_0  COME_FROM           160  '160'
            164_1  COME_FROM           138  '138'

 L. 880       164  LOAD_FAST                'value'
              166  LOAD_METHOD              strip
              168  LOAD_FAST                'replace_chars'
              170  CALL_METHOD_1         1  ''
              172  LOAD_FAST                'link'
              174  LOAD_FAST                'key'
              176  LOAD_METHOD              strip
              178  LOAD_FAST                'replace_chars'
              180  CALL_METHOD_1         1  ''
              182  STORE_SUBSCR     
              184  JUMP_BACK           116  'to 116'

 L. 882       186  LOAD_FAST                'links'
              188  LOAD_METHOD              append
              190  LOAD_FAST                'link'
              192  CALL_METHOD_1         1  ''
              194  POP_TOP          
              196  JUMP_BACK            38  'to 38'

 L. 884       198  LOAD_FAST                'links'
              200  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 68


_null = '\x00'.encode('ascii')
_null2 = _null * 2
_null3 = _null * 3

def guess_json_utf--- This code section failed: ---

 L. 900         0  LOAD_FAST                'data'
                2  LOAD_CONST               None
                4  LOAD_CONST               4
                6  BUILD_SLICE_2         2 
                8  BINARY_SUBSCR    
               10  STORE_FAST               'sample'

 L. 901        12  LOAD_FAST                'sample'
               14  LOAD_GLOBAL              codecs
               16  LOAD_ATTR                BOM_UTF32_LE
               18  LOAD_GLOBAL              codecs
               20  LOAD_ATTR                BOM_UTF32_BE
               22  BUILD_TUPLE_2         2 
               24  <118>                 0  ''
               26  POP_JUMP_IF_FALSE    32  'to 32'

 L. 902        28  LOAD_STR                 'utf-32'
               30  RETURN_VALUE     
             32_0  COME_FROM            26  '26'

 L. 903        32  LOAD_FAST                'sample'
               34  LOAD_CONST               None
               36  LOAD_CONST               3
               38  BUILD_SLICE_2         2 
               40  BINARY_SUBSCR    
               42  LOAD_GLOBAL              codecs
               44  LOAD_ATTR                BOM_UTF8
               46  COMPARE_OP               ==
               48  POP_JUMP_IF_FALSE    54  'to 54'

 L. 904        50  LOAD_STR                 'utf-8-sig'
               52  RETURN_VALUE     
             54_0  COME_FROM            48  '48'

 L. 905        54  LOAD_FAST                'sample'
               56  LOAD_CONST               None
               58  LOAD_CONST               2
               60  BUILD_SLICE_2         2 
               62  BINARY_SUBSCR    
               64  LOAD_GLOBAL              codecs
               66  LOAD_ATTR                BOM_UTF16_LE
               68  LOAD_GLOBAL              codecs
               70  LOAD_ATTR                BOM_UTF16_BE
               72  BUILD_TUPLE_2         2 
               74  <118>                 0  ''
               76  POP_JUMP_IF_FALSE    82  'to 82'

 L. 906        78  LOAD_STR                 'utf-16'
               80  RETURN_VALUE     
             82_0  COME_FROM            76  '76'

 L. 907        82  LOAD_FAST                'sample'
               84  LOAD_METHOD              count
               86  LOAD_GLOBAL              _null
               88  CALL_METHOD_1         1  ''
               90  STORE_FAST               'nullcount'

 L. 908        92  LOAD_FAST                'nullcount'
               94  LOAD_CONST               0
               96  COMPARE_OP               ==
               98  POP_JUMP_IF_FALSE   104  'to 104'

 L. 909       100  LOAD_STR                 'utf-8'
              102  RETURN_VALUE     
            104_0  COME_FROM            98  '98'

 L. 910       104  LOAD_FAST                'nullcount'
              106  LOAD_CONST               2
              108  COMPARE_OP               ==
              110  POP_JUMP_IF_FALSE   156  'to 156'

 L. 911       112  LOAD_FAST                'sample'
              114  LOAD_CONST               None
              116  LOAD_CONST               None
              118  LOAD_CONST               2
              120  BUILD_SLICE_3         3 
              122  BINARY_SUBSCR    
              124  LOAD_GLOBAL              _null2
              126  COMPARE_OP               ==
              128  POP_JUMP_IF_FALSE   134  'to 134'

 L. 912       130  LOAD_STR                 'utf-16-be'
              132  RETURN_VALUE     
            134_0  COME_FROM           128  '128'

 L. 913       134  LOAD_FAST                'sample'
              136  LOAD_CONST               1
              138  LOAD_CONST               None
              140  LOAD_CONST               2
              142  BUILD_SLICE_3         3 
              144  BINARY_SUBSCR    
              146  LOAD_GLOBAL              _null2
              148  COMPARE_OP               ==
              150  POP_JUMP_IF_FALSE   156  'to 156'

 L. 914       152  LOAD_STR                 'utf-16-le'
              154  RETURN_VALUE     
            156_0  COME_FROM           150  '150'
            156_1  COME_FROM           110  '110'

 L. 916       156  LOAD_FAST                'nullcount'
              158  LOAD_CONST               3
              160  COMPARE_OP               ==
              162  POP_JUMP_IF_FALSE   204  'to 204'

 L. 917       164  LOAD_FAST                'sample'
              166  LOAD_CONST               None
              168  LOAD_CONST               3
              170  BUILD_SLICE_2         2 
              172  BINARY_SUBSCR    
              174  LOAD_GLOBAL              _null3
              176  COMPARE_OP               ==
              178  POP_JUMP_IF_FALSE   184  'to 184'

 L. 918       180  LOAD_STR                 'utf-32-be'
              182  RETURN_VALUE     
            184_0  COME_FROM           178  '178'

 L. 919       184  LOAD_FAST                'sample'
              186  LOAD_CONST               1
              188  LOAD_CONST               None
              190  BUILD_SLICE_2         2 
              192  BINARY_SUBSCR    
              194  LOAD_GLOBAL              _null3
              196  COMPARE_OP               ==
              198  POP_JUMP_IF_FALSE   204  'to 204'

 L. 920       200  LOAD_STR                 'utf-32-le'
              202  RETURN_VALUE     
            204_0  COME_FROM           198  '198'
            204_1  COME_FROM           162  '162'

Parse error at or near `<118>' instruction at offset 24


def prepend_scheme_if_needed(url, new_scheme):
    """Given a URL that may or may not have a scheme, prepend the given scheme.
    Does not replace a present scheme with the one provided as an argument.

    :rtype: str
    """
    scheme, netloc, path, params, query, fragment = urlparse(url, new_scheme)
    if not netloc:
        netloc, path = path, netloc
    return urlunparse((scheme, netloc, path, params, query, fragment))


def get_auth_from_url--- This code section failed: ---

 L. 948         0  LOAD_GLOBAL              urlparse
                2  LOAD_FAST                'url'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'parsed'

 L. 950         8  SETUP_FINALLY        34  'to 34'

 L. 951        10  LOAD_GLOBAL              unquote
               12  LOAD_FAST                'parsed'
               14  LOAD_ATTR                username
               16  CALL_FUNCTION_1       1  ''
               18  LOAD_GLOBAL              unquote
               20  LOAD_FAST                'parsed'
               22  LOAD_ATTR                password
               24  CALL_FUNCTION_1       1  ''
               26  BUILD_TUPLE_2         2 
               28  STORE_FAST               'auth'
               30  POP_BLOCK        
               32  JUMP_FORWARD         60  'to 60'
             34_0  COME_FROM_FINALLY     8  '8'

 L. 952        34  DUP_TOP          
               36  LOAD_GLOBAL              AttributeError
               38  LOAD_GLOBAL              TypeError
               40  BUILD_TUPLE_2         2 
               42  <121>                58  ''
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          

 L. 953        50  LOAD_CONST               ('', '')
               52  STORE_FAST               'auth'
               54  POP_EXCEPT       
               56  JUMP_FORWARD         60  'to 60'
               58  <48>             
             60_0  COME_FROM            56  '56'
             60_1  COME_FROM            32  '32'

 L. 955        60  LOAD_FAST                'auth'
               62  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 42


_CLEAN_HEADER_REGEX_BYTE = re.compile(b'^\\S[^\\r\\n]*$|^$')
_CLEAN_HEADER_REGEX_STR = re.compile('^\\S[^\\r\\n]*$|^$')

def check_header_validity--- This code section failed: ---

 L. 970         0  LOAD_FAST                'header'
                2  UNPACK_SEQUENCE_2     2 
                4  STORE_FAST               'name'
                6  STORE_FAST               'value'

 L. 972         8  LOAD_GLOBAL              isinstance
               10  LOAD_FAST                'value'
               12  LOAD_GLOBAL              bytes
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_FALSE    24  'to 24'

 L. 973        18  LOAD_GLOBAL              _CLEAN_HEADER_REGEX_BYTE
               20  STORE_FAST               'pat'
               22  JUMP_FORWARD         28  'to 28'
             24_0  COME_FROM            16  '16'

 L. 975        24  LOAD_GLOBAL              _CLEAN_HEADER_REGEX_STR
               26  STORE_FAST               'pat'
             28_0  COME_FROM            22  '22'

 L. 976        28  SETUP_FINALLY        56  'to 56'

 L. 977        30  LOAD_FAST                'pat'
               32  LOAD_METHOD              match
               34  LOAD_FAST                'value'
               36  CALL_METHOD_1         1  ''
               38  POP_JUMP_IF_TRUE     52  'to 52'

 L. 978        40  LOAD_GLOBAL              InvalidHeader
               42  LOAD_STR                 'Invalid return character or leading space in header: %s'
               44  LOAD_FAST                'name'
               46  BINARY_MODULO    
               48  CALL_FUNCTION_1       1  ''
               50  RAISE_VARARGS_1       1  'exception instance'
             52_0  COME_FROM            38  '38'
               52  POP_BLOCK        
               54  JUMP_FORWARD         96  'to 96'
             56_0  COME_FROM_FINALLY    28  '28'

 L. 979        56  DUP_TOP          
               58  LOAD_GLOBAL              TypeError
               60  <121>                94  ''
               62  POP_TOP          
               64  POP_TOP          
               66  POP_TOP          

 L. 980        68  LOAD_GLOBAL              InvalidHeader
               70  LOAD_STR                 'Value for header {%s: %s} must be of type str or bytes, not %s'

 L. 981        72  LOAD_FAST                'name'
               74  LOAD_FAST                'value'
               76  LOAD_GLOBAL              type
               78  LOAD_FAST                'value'
               80  CALL_FUNCTION_1       1  ''
               82  BUILD_TUPLE_3         3 

 L. 980        84  BINARY_MODULO    
               86  CALL_FUNCTION_1       1  ''
               88  RAISE_VARARGS_1       1  'exception instance'
               90  POP_EXCEPT       
               92  JUMP_FORWARD         96  'to 96'
               94  <48>             
             96_0  COME_FROM            92  '92'
             96_1  COME_FROM            54  '54'

Parse error at or near `<121>' instruction at offset 60


def urldefragauth(url):
    """
    Given a url remove the fragment and the authentication part.

    :rtype: str
    """
    scheme, netloc, path, params, query, fragment = urlparse(url)
    if not netloc:
        netloc, path = path, netloc
    netloc = netloc.rsplit('@', 1)[(-1)]
    return urlunparse((scheme, netloc, path, params, query, ''))


def rewind_body--- This code section failed: ---

 L.1005         0  LOAD_GLOBAL              getattr
                2  LOAD_FAST                'prepared_request'
                4  LOAD_ATTR                body
                6  LOAD_STR                 'seek'
                8  LOAD_CONST               None
               10  CALL_FUNCTION_3       3  ''
               12  STORE_FAST               'body_seek'

 L.1006        14  LOAD_FAST                'body_seek'
               16  LOAD_CONST               None
               18  <117>                 1  ''
               20  POP_JUMP_IF_FALSE    82  'to 82'
               22  LOAD_GLOBAL              isinstance
               24  LOAD_FAST                'prepared_request'
               26  LOAD_ATTR                _body_position
               28  LOAD_GLOBAL              integer_types
               30  CALL_FUNCTION_2       2  ''
               32  POP_JUMP_IF_FALSE    82  'to 82'

 L.1007        34  SETUP_FINALLY        50  'to 50'

 L.1008        36  LOAD_FAST                'body_seek'
               38  LOAD_FAST                'prepared_request'
               40  LOAD_ATTR                _body_position
               42  CALL_FUNCTION_1       1  ''
               44  POP_TOP          
               46  POP_BLOCK        
               48  JUMP_ABSOLUTE        90  'to 90'
             50_0  COME_FROM_FINALLY    34  '34'

 L.1009        50  DUP_TOP          
               52  LOAD_GLOBAL              IOError
               54  LOAD_GLOBAL              OSError
               56  BUILD_TUPLE_2         2 
               58  <121>                78  ''
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L.1010        66  LOAD_GLOBAL              UnrewindableBodyError
               68  LOAD_STR                 'An error occurred when rewinding request body for redirect.'
               70  CALL_FUNCTION_1       1  ''
               72  RAISE_VARARGS_1       1  'exception instance'
               74  POP_EXCEPT       
               76  JUMP_ABSOLUTE        90  'to 90'
               78  <48>             
               80  JUMP_FORWARD         90  'to 90'
             82_0  COME_FROM            32  '32'
             82_1  COME_FROM            20  '20'

 L.1013        82  LOAD_GLOBAL              UnrewindableBodyError
               84  LOAD_STR                 'Unable to rewind request body for redirect.'
               86  CALL_FUNCTION_1       1  ''
               88  RAISE_VARARGS_1       1  'exception instance'
             90_0  COME_FROM_EXCEPT_CLAUSE    80  '80'
             90_1  COME_FROM_EXCEPT_CLAUSE    76  '76'

Parse error at or near `<117>' instruction at offset 18