# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\features.py
import collections, os, sys, warnings, PIL
from . import Image
modules = {'pil':('PIL._imaging', 'PILLOW_VERSION'), 
 'tkinter':('PIL._tkinter_finder', None), 
 'freetype2':('PIL._imagingft', 'freetype2_version'), 
 'littlecms2':('PIL._imagingcms', 'littlecms_version'), 
 'webp':('PIL._webp', 'webpdecoder_version')}

def check_module--- This code section failed: ---

 L.  27         0  LOAD_FAST                'feature'
                2  LOAD_GLOBAL              modules
                4  <118>                 1  ''
                6  POP_JUMP_IF_FALSE    22  'to 22'

 L.  28         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 'Unknown module '
               12  LOAD_FAST                'feature'
               14  FORMAT_VALUE          0  ''
               16  BUILD_STRING_2        2 
               18  CALL_FUNCTION_1       1  ''
               20  RAISE_VARARGS_1       1  'exception instance'
             22_0  COME_FROM             6  '6'

 L.  30        22  LOAD_GLOBAL              modules
               24  LOAD_FAST                'feature'
               26  BINARY_SUBSCR    
               28  UNPACK_SEQUENCE_2     2 
               30  STORE_FAST               'module'
               32  STORE_FAST               'ver'

 L.  32        34  SETUP_FINALLY        50  'to 50'

 L.  33        36  LOAD_GLOBAL              __import__
               38  LOAD_FAST                'module'
               40  CALL_FUNCTION_1       1  ''
               42  POP_TOP          

 L.  34        44  POP_BLOCK        
               46  LOAD_CONST               True
               48  RETURN_VALUE     
             50_0  COME_FROM_FINALLY    34  '34'

 L.  35        50  DUP_TOP          
               52  LOAD_GLOBAL              ImportError
               54  <121>                68  ''
               56  POP_TOP          
               58  POP_TOP          
               60  POP_TOP          

 L.  36        62  POP_EXCEPT       
               64  LOAD_CONST               False
               66  RETURN_VALUE     
               68  <48>             

Parse error at or near `None' instruction at offset -1


def version_module--- This code section failed: ---

 L.  46         0  LOAD_GLOBAL              check_module
                2  LOAD_FAST                'feature'
                4  CALL_FUNCTION_1       1  ''
                6  POP_JUMP_IF_TRUE     12  'to 12'

 L.  47         8  LOAD_CONST               None
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L.  49        12  LOAD_GLOBAL              modules
               14  LOAD_FAST                'feature'
               16  BINARY_SUBSCR    
               18  UNPACK_SEQUENCE_2     2 
               20  STORE_FAST               'module'
               22  STORE_FAST               'ver'

 L.  51        24  LOAD_FAST                'ver'
               26  LOAD_CONST               None
               28  <117>                 0  ''
               30  POP_JUMP_IF_FALSE    36  'to 36'

 L.  52        32  LOAD_CONST               None
               34  RETURN_VALUE     
             36_0  COME_FROM            30  '30'

 L.  54        36  LOAD_GLOBAL              getattr
               38  LOAD_GLOBAL              __import__
               40  LOAD_FAST                'module'
               42  LOAD_FAST                'ver'
               44  BUILD_LIST_1          1 
               46  LOAD_CONST               ('fromlist',)
               48  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               50  LOAD_FAST                'ver'
               52  CALL_FUNCTION_2       2  ''
               54  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 28


def get_supported_modules():
    """
    :returns: A list of all supported modules.
    """
    return [f for f in modules if check_module(f)]


codecs = {'jpg':('jpeg', 'jpeglib'), 
 'jpg_2000':('jpeg2k', 'jp2klib'), 
 'zlib':('zip', 'zlib'), 
 'libtiff':('libtiff', 'libtiff')}

def check_codec--- This code section failed: ---

 L.  80         0  LOAD_FAST                'feature'
                2  LOAD_GLOBAL              codecs
                4  <118>                 1  ''
                6  POP_JUMP_IF_FALSE    22  'to 22'

 L.  81         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 'Unknown codec '
               12  LOAD_FAST                'feature'
               14  FORMAT_VALUE          0  ''
               16  BUILD_STRING_2        2 
               18  CALL_FUNCTION_1       1  ''
               20  RAISE_VARARGS_1       1  'exception instance'
             22_0  COME_FROM             6  '6'

 L.  83        22  LOAD_GLOBAL              codecs
               24  LOAD_FAST                'feature'
               26  BINARY_SUBSCR    
               28  UNPACK_SEQUENCE_2     2 
               30  STORE_FAST               'codec'
               32  STORE_FAST               'lib'

 L.  85        34  LOAD_FAST                'codec'
               36  LOAD_STR                 '_encoder'
               38  BINARY_ADD       
               40  LOAD_GLOBAL              dir
               42  LOAD_GLOBAL              Image
               44  LOAD_ATTR                core
               46  CALL_FUNCTION_1       1  ''
               48  <118>                 0  ''
               50  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def version_codec(feature):
    """
    :param feature: The codec to check for.
    :returns:
        The version number as a string, or ``None`` if not available.
        Checked at compile time for ``jpg``, run-time otherwise.
    :raises ValueError: If the codec is not defined in this version of Pillow.
    """
    if not check_codec(feature):
        return
    codec, lib = codecs[feature]
    version = getattrImage.core(lib + '_version')
    if feature == 'libtiff':
        return version.split('\n')[0].split('Version ')[1]
    return version


def get_supported_codecs():
    """
    :returns: A list of all supported codecs.
    """
    return [f for f in codecs if check_codec(f)]


features = {'webp_anim':('PIL._webp', 'HAVE_WEBPANIM', None), 
 'webp_mux':('PIL._webp', 'HAVE_WEBPMUX', None), 
 'transp_webp':('PIL._webp', 'HAVE_TRANSPARENCY', None), 
 'raqm':('PIL._imagingft', 'HAVE_RAQM', 'raqm_version'), 
 'libjpeg_turbo':('PIL._imaging', 'HAVE_LIBJPEGTURBO', 'libjpeg_turbo_version'), 
 'libimagequant':('PIL._imaging', 'HAVE_LIBIMAGEQUANT', 'imagequant_version'), 
 'xcb':('PIL._imaging', 'HAVE_XCB', None)}

def check_feature--- This code section failed: ---

 L. 135         0  LOAD_FAST                'feature'
                2  LOAD_GLOBAL              features
                4  <118>                 1  ''
                6  POP_JUMP_IF_FALSE    22  'to 22'

 L. 136         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 'Unknown feature '
               12  LOAD_FAST                'feature'
               14  FORMAT_VALUE          0  ''
               16  BUILD_STRING_2        2 
               18  CALL_FUNCTION_1       1  ''
               20  RAISE_VARARGS_1       1  'exception instance'
             22_0  COME_FROM             6  '6'

 L. 138        22  LOAD_GLOBAL              features
               24  LOAD_FAST                'feature'
               26  BINARY_SUBSCR    
               28  UNPACK_SEQUENCE_3     3 
               30  STORE_FAST               'module'
               32  STORE_FAST               'flag'
               34  STORE_FAST               'ver'

 L. 140        36  SETUP_FINALLY        64  'to 64'

 L. 141        38  LOAD_GLOBAL              __import__
               40  LOAD_FAST                'module'
               42  LOAD_STR                 'PIL'
               44  BUILD_LIST_1          1 
               46  LOAD_CONST               ('fromlist',)
               48  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               50  STORE_FAST               'imported_module'

 L. 142        52  LOAD_GLOBAL              getattr
               54  LOAD_FAST                'imported_module'
               56  LOAD_FAST                'flag'
               58  CALL_FUNCTION_2       2  ''
               60  POP_BLOCK        
               62  RETURN_VALUE     
             64_0  COME_FROM_FINALLY    36  '36'

 L. 143        64  DUP_TOP          
               66  LOAD_GLOBAL              ImportError
               68  <121>                82  ''
               70  POP_TOP          
               72  POP_TOP          
               74  POP_TOP          

 L. 144        76  POP_EXCEPT       
               78  LOAD_CONST               None
               80  RETURN_VALUE     
               82  <48>             

Parse error at or near `None' instruction at offset -1


def version_feature--- This code section failed: ---

 L. 153         0  LOAD_GLOBAL              check_feature
                2  LOAD_FAST                'feature'
                4  CALL_FUNCTION_1       1  ''
                6  POP_JUMP_IF_TRUE     12  'to 12'

 L. 154         8  LOAD_CONST               None
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L. 156        12  LOAD_GLOBAL              features
               14  LOAD_FAST                'feature'
               16  BINARY_SUBSCR    
               18  UNPACK_SEQUENCE_3     3 
               20  STORE_FAST               'module'
               22  STORE_FAST               'flag'
               24  STORE_FAST               'ver'

 L. 158        26  LOAD_FAST                'ver'
               28  LOAD_CONST               None
               30  <117>                 0  ''
               32  POP_JUMP_IF_FALSE    38  'to 38'

 L. 159        34  LOAD_CONST               None
               36  RETURN_VALUE     
             38_0  COME_FROM            32  '32'

 L. 161        38  LOAD_GLOBAL              getattr
               40  LOAD_GLOBAL              __import__
               42  LOAD_FAST                'module'
               44  LOAD_FAST                'ver'
               46  BUILD_LIST_1          1 
               48  LOAD_CONST               ('fromlist',)
               50  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               52  LOAD_FAST                'ver'
               54  CALL_FUNCTION_2       2  ''
               56  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 30


def get_supported_features():
    """
    :returns: A list of all supported features.
    """
    return [f for f in features if check_feature(f)]


def check--- This code section failed: ---

 L. 179         0  LOAD_FAST                'feature'
                2  LOAD_GLOBAL              modules
                4  <118>                 0  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 180         8  LOAD_GLOBAL              check_module
               10  LOAD_FAST                'feature'
               12  CALL_FUNCTION_1       1  ''
               14  RETURN_VALUE     
             16_0  COME_FROM             6  '6'

 L. 181        16  LOAD_FAST                'feature'
               18  LOAD_GLOBAL              codecs
               20  <118>                 0  ''
               22  POP_JUMP_IF_FALSE    32  'to 32'

 L. 182        24  LOAD_GLOBAL              check_codec
               26  LOAD_FAST                'feature'
               28  CALL_FUNCTION_1       1  ''
               30  RETURN_VALUE     
             32_0  COME_FROM            22  '22'

 L. 183        32  LOAD_FAST                'feature'
               34  LOAD_GLOBAL              features
               36  <118>                 0  ''
               38  POP_JUMP_IF_FALSE    48  'to 48'

 L. 184        40  LOAD_GLOBAL              check_feature
               42  LOAD_FAST                'feature'
               44  CALL_FUNCTION_1       1  ''
               46  RETURN_VALUE     
             48_0  COME_FROM            38  '38'

 L. 185        48  LOAD_GLOBAL              warnings
               50  LOAD_ATTR                warn
               52  LOAD_STR                 "Unknown feature '"
               54  LOAD_FAST                'feature'
               56  FORMAT_VALUE          0  ''
               58  LOAD_STR                 "'."
               60  BUILD_STRING_3        3 
               62  LOAD_CONST               2
               64  LOAD_CONST               ('stacklevel',)
               66  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               68  POP_TOP          

 L. 186        70  LOAD_CONST               False
               72  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def version--- This code section failed: ---

 L. 196         0  LOAD_FAST                'feature'
                2  LOAD_GLOBAL              modules
                4  <118>                 0  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 197         8  LOAD_GLOBAL              version_module
               10  LOAD_FAST                'feature'
               12  CALL_FUNCTION_1       1  ''
               14  RETURN_VALUE     
             16_0  COME_FROM             6  '6'

 L. 198        16  LOAD_FAST                'feature'
               18  LOAD_GLOBAL              codecs
               20  <118>                 0  ''
               22  POP_JUMP_IF_FALSE    32  'to 32'

 L. 199        24  LOAD_GLOBAL              version_codec
               26  LOAD_FAST                'feature'
               28  CALL_FUNCTION_1       1  ''
               30  RETURN_VALUE     
             32_0  COME_FROM            22  '22'

 L. 200        32  LOAD_FAST                'feature'
               34  LOAD_GLOBAL              features
               36  <118>                 0  ''
               38  POP_JUMP_IF_FALSE    48  'to 48'

 L. 201        40  LOAD_GLOBAL              version_feature
               42  LOAD_FAST                'feature'
               44  CALL_FUNCTION_1       1  ''
               46  RETURN_VALUE     
             48_0  COME_FROM            38  '38'

Parse error at or near `None' instruction at offset -1


def get_supported():
    """
    :returns: A list of all supported modules, features, and codecs.
    """
    ret = get_supported_modules()
    ret.extend(get_supported_features())
    ret.extend(get_supported_codecs())
    return ret


def pilinfo--- This code section failed: ---

 L. 227         0  LOAD_FAST                'out'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 228         8  LOAD_GLOBAL              sys
               10  LOAD_ATTR                stdout
               12  STORE_FAST               'out'
             14_0  COME_FROM             6  '6'

 L. 230        14  LOAD_GLOBAL              Image
               16  LOAD_METHOD              init
               18  CALL_METHOD_0         0  ''
               20  POP_TOP          

 L. 232        22  LOAD_GLOBAL              print
               24  LOAD_STR                 '--------------------------------------------------------------------'
               26  LOAD_FAST                'out'
               28  LOAD_CONST               ('file',)
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  POP_TOP          

 L. 233        34  LOAD_GLOBAL              print
               36  LOAD_STR                 'Pillow '
               38  LOAD_GLOBAL              PIL
               40  LOAD_ATTR                __version__
               42  FORMAT_VALUE          0  ''
               44  BUILD_STRING_2        2 
               46  LOAD_FAST                'out'
               48  LOAD_CONST               ('file',)
               50  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               52  POP_TOP          

 L. 234        54  LOAD_GLOBAL              sys
               56  LOAD_ATTR                version
               58  LOAD_METHOD              splitlines
               60  CALL_METHOD_0         0  ''
               62  STORE_FAST               'py_version'

 L. 235        64  LOAD_GLOBAL              print
               66  LOAD_STR                 'Python '
               68  LOAD_FAST                'py_version'
               70  LOAD_CONST               0
               72  BINARY_SUBSCR    
               74  LOAD_METHOD              strip
               76  CALL_METHOD_0         0  ''
               78  FORMAT_VALUE          0  ''
               80  BUILD_STRING_2        2 
               82  LOAD_FAST                'out'
               84  LOAD_CONST               ('file',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  POP_TOP          

 L. 236        90  LOAD_FAST                'py_version'
               92  LOAD_CONST               1
               94  LOAD_CONST               None
               96  BUILD_SLICE_2         2 
               98  BINARY_SUBSCR    
              100  GET_ITER         
            102_0  COME_FROM           128  '128'
              102  FOR_ITER            130  'to 130'
              104  STORE_FAST               'py_version'

 L. 237       106  LOAD_GLOBAL              print
              108  LOAD_STR                 '       '
              110  LOAD_FAST                'py_version'
              112  LOAD_METHOD              strip
              114  CALL_METHOD_0         0  ''
              116  FORMAT_VALUE          0  ''
              118  BUILD_STRING_2        2 
              120  LOAD_FAST                'out'
              122  LOAD_CONST               ('file',)
              124  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              126  POP_TOP          
              128  JUMP_BACK           102  'to 102'
            130_0  COME_FROM           102  '102'

 L. 238       130  LOAD_GLOBAL              print
              132  LOAD_STR                 '--------------------------------------------------------------------'
              134  LOAD_FAST                'out'
              136  LOAD_CONST               ('file',)
              138  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              140  POP_TOP          

 L. 239       142  LOAD_GLOBAL              print

 L. 240       144  LOAD_STR                 'Python modules loaded from '
              146  LOAD_GLOBAL              os
              148  LOAD_ATTR                path
              150  LOAD_METHOD              dirname
              152  LOAD_GLOBAL              Image
              154  LOAD_ATTR                __file__
              156  CALL_METHOD_1         1  ''
              158  FORMAT_VALUE          0  ''
              160  BUILD_STRING_2        2 

 L. 241       162  LOAD_FAST                'out'

 L. 239       164  LOAD_CONST               ('file',)
              166  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              168  POP_TOP          

 L. 243       170  LOAD_GLOBAL              print

 L. 244       172  LOAD_STR                 'Binary modules loaded from '
              174  LOAD_GLOBAL              os
              176  LOAD_ATTR                path
              178  LOAD_METHOD              dirname
              180  LOAD_GLOBAL              Image
              182  LOAD_ATTR                core
              184  LOAD_ATTR                __file__
              186  CALL_METHOD_1         1  ''
              188  FORMAT_VALUE          0  ''
              190  BUILD_STRING_2        2 

 L. 245       192  LOAD_FAST                'out'

 L. 243       194  LOAD_CONST               ('file',)
              196  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              198  POP_TOP          

 L. 247       200  LOAD_GLOBAL              print
              202  LOAD_STR                 '--------------------------------------------------------------------'
              204  LOAD_FAST                'out'
              206  LOAD_CONST               ('file',)
              208  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              210  POP_TOP          

 L. 249       212  LOAD_CONST               (('pil', 'PIL CORE'), ('tkinter', 'TKINTER'), ('freetype2', 'FREETYPE2'), ('littlecms2', 'LITTLECMS2'), ('webp', 'WEBP'), ('transp_webp', 'WEBP Transparency'), ('webp_mux', 'WEBPMUX'), ('webp_anim', 'WEBP Animation'), ('jpg', 'JPEG'), ('jpg_2000', 'OPENJPEG (JPEG2000)'), ('zlib', 'ZLIB (PNG/ZIP)'), ('libtiff', 'LIBTIFF'), ('raqm', 'RAQM (Bidirectional Text)'), ('libimagequant', 'LIBIMAGEQUANT (Quantization method)'), ('xcb', 'XCB (X protocol)'))
              214  GET_ITER         
            216_0  COME_FROM           402  '402'
            216_1  COME_FROM           384  '384'
              216  FOR_ITER            404  'to 404'
              218  UNPACK_SEQUENCE_2     2 
              220  STORE_FAST               'name'
              222  STORE_FAST               'feature'

 L. 266       224  LOAD_GLOBAL              check
              226  LOAD_FAST                'name'
              228  CALL_FUNCTION_1       1  ''
          230_232  POP_JUMP_IF_FALSE   386  'to 386'

 L. 267       234  LOAD_FAST                'name'
              236  LOAD_STR                 'jpg'
              238  COMPARE_OP               ==
          240_242  POP_JUMP_IF_FALSE   268  'to 268'
              244  LOAD_GLOBAL              check_feature
              246  LOAD_STR                 'libjpeg_turbo'
              248  CALL_FUNCTION_1       1  ''
          250_252  POP_JUMP_IF_FALSE   268  'to 268'

 L. 268       254  LOAD_STR                 'libjpeg-turbo '
              256  LOAD_GLOBAL              version_feature
              258  LOAD_STR                 'libjpeg_turbo'
              260  CALL_FUNCTION_1       1  ''
              262  BINARY_ADD       
              264  STORE_FAST               'v'
              266  JUMP_FORWARD        276  'to 276'
            268_0  COME_FROM           250  '250'
            268_1  COME_FROM           240  '240'

 L. 270       268  LOAD_GLOBAL              version
              270  LOAD_FAST                'name'
              272  CALL_FUNCTION_1       1  ''
              274  STORE_FAST               'v'
            276_0  COME_FROM           266  '266'

 L. 271       276  LOAD_FAST                'v'
              278  LOAD_CONST               None
              280  <117>                 1  ''
          282_284  POP_JUMP_IF_FALSE   368  'to 368'

 L. 272       286  LOAD_FAST                'name'
              288  LOAD_CONST               ('pil', 'jpg')
              290  <118>                 0  ''
              292  STORE_FAST               'version_static'

 L. 273       294  LOAD_FAST                'name'
              296  LOAD_STR                 'littlecms2'
              298  COMPARE_OP               ==
          300_302  POP_JUMP_IF_FALSE   332  'to 332'

 L. 275       304  LOAD_GLOBAL              tuple
              306  LOAD_GENEXPR             '<code_object <genexpr>>'
              308  LOAD_STR                 'pilinfo.<locals>.<genexpr>'
              310  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              312  LOAD_FAST                'v'
              314  LOAD_METHOD              split
              316  LOAD_STR                 '.'
              318  CALL_METHOD_1         1  ''
              320  GET_ITER         
              322  CALL_FUNCTION_1       1  ''
              324  CALL_FUNCTION_1       1  ''
              326  LOAD_CONST               (2, 7)
              328  COMPARE_OP               <
              330  STORE_FAST               'version_static'
            332_0  COME_FROM           300  '300'

 L. 276       332  LOAD_FAST                'version_static'
          334_336  POP_JUMP_IF_FALSE   342  'to 342'
              338  LOAD_STR                 'compiled for'
              340  JUMP_FORWARD        344  'to 344'
            342_0  COME_FROM           334  '334'
              342  LOAD_STR                 'loaded'
            344_0  COME_FROM           340  '340'
              344  STORE_FAST               't'

 L. 277       346  LOAD_GLOBAL              print
              348  LOAD_STR                 '---'
              350  LOAD_FAST                'feature'
              352  LOAD_STR                 'support ok,'
              354  LOAD_FAST                't'
              356  LOAD_FAST                'v'
              358  LOAD_FAST                'out'
              360  LOAD_CONST               ('file',)
              362  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              364  POP_TOP          
              366  JUMP_FORWARD        384  'to 384'
            368_0  COME_FROM           282  '282'

 L. 279       368  LOAD_GLOBAL              print
              370  LOAD_STR                 '---'
              372  LOAD_FAST                'feature'
              374  LOAD_STR                 'support ok'
              376  LOAD_FAST                'out'
              378  LOAD_CONST               ('file',)
              380  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              382  POP_TOP          
            384_0  COME_FROM           366  '366'
              384  JUMP_BACK           216  'to 216'
            386_0  COME_FROM           230  '230'

 L. 281       386  LOAD_GLOBAL              print
              388  LOAD_STR                 '***'
              390  LOAD_FAST                'feature'
              392  LOAD_STR                 'support not installed'
              394  LOAD_FAST                'out'
              396  LOAD_CONST               ('file',)
              398  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              400  POP_TOP          
              402  JUMP_BACK           216  'to 216'
            404_0  COME_FROM           216  '216'

 L. 282       404  LOAD_GLOBAL              print
              406  LOAD_STR                 '--------------------------------------------------------------------'
              408  LOAD_FAST                'out'
              410  LOAD_CONST               ('file',)
              412  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              414  POP_TOP          

 L. 284       416  LOAD_FAST                'supported_formats'
          418_420  POP_JUMP_IF_FALSE   728  'to 728'

 L. 285       422  LOAD_GLOBAL              collections
              424  LOAD_METHOD              defaultdict
              426  LOAD_GLOBAL              list
              428  CALL_METHOD_1         1  ''
              430  STORE_FAST               'extensions'

 L. 286       432  LOAD_GLOBAL              Image
              434  LOAD_ATTR                EXTENSION
              436  LOAD_METHOD              items
              438  CALL_METHOD_0         0  ''
              440  GET_ITER         
            442_0  COME_FROM           464  '464'
              442  FOR_ITER            468  'to 468'
              444  UNPACK_SEQUENCE_2     2 
              446  STORE_FAST               'ext'
              448  STORE_FAST               'i'

 L. 287       450  LOAD_FAST                'extensions'
              452  LOAD_FAST                'i'
              454  BINARY_SUBSCR    
              456  LOAD_METHOD              append
              458  LOAD_FAST                'ext'
              460  CALL_METHOD_1         1  ''
              462  POP_TOP          
          464_466  JUMP_BACK           442  'to 442'
            468_0  COME_FROM           442  '442'

 L. 289       468  LOAD_GLOBAL              sorted
              470  LOAD_GLOBAL              Image
              472  LOAD_ATTR                ID
              474  CALL_FUNCTION_1       1  ''
              476  GET_ITER         
            478_0  COME_FROM           724  '724'
              478  FOR_ITER            728  'to 728'
              480  STORE_FAST               'i'

 L. 290       482  LOAD_FAST                'i'
              484  FORMAT_VALUE          0  ''
              486  STORE_FAST               'line'

 L. 291       488  LOAD_FAST                'i'
              490  LOAD_GLOBAL              Image
              492  LOAD_ATTR                MIME
              494  <118>                 0  ''
          496_498  POP_JUMP_IF_FALSE   520  'to 520'

 L. 292       500  LOAD_FAST                'line'
              502  FORMAT_VALUE          0  ''
              504  LOAD_STR                 ' '
              506  LOAD_GLOBAL              Image
              508  LOAD_ATTR                MIME
              510  LOAD_FAST                'i'
              512  BINARY_SUBSCR    
              514  FORMAT_VALUE          0  ''
              516  BUILD_STRING_3        3 
              518  STORE_FAST               'line'
            520_0  COME_FROM           496  '496'

 L. 293       520  LOAD_GLOBAL              print
              522  LOAD_FAST                'line'
              524  LOAD_FAST                'out'
              526  LOAD_CONST               ('file',)
              528  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              530  POP_TOP          

 L. 295       532  LOAD_FAST                'i'
              534  LOAD_FAST                'extensions'
              536  <118>                 0  ''
          538_540  POP_JUMP_IF_FALSE   574  'to 574'

 L. 296       542  LOAD_GLOBAL              print

 L. 297       544  LOAD_STR                 'Extensions: {}'
              546  LOAD_METHOD              format
              548  LOAD_STR                 ', '
              550  LOAD_METHOD              join
              552  LOAD_GLOBAL              sorted
              554  LOAD_FAST                'extensions'
              556  LOAD_FAST                'i'
              558  BINARY_SUBSCR    
              560  CALL_FUNCTION_1       1  ''
              562  CALL_METHOD_1         1  ''
              564  CALL_METHOD_1         1  ''
              566  LOAD_FAST                'out'

 L. 296       568  LOAD_CONST               ('file',)
              570  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              572  POP_TOP          
            574_0  COME_FROM           538  '538'

 L. 300       574  BUILD_LIST_0          0 
              576  STORE_FAST               'features'

 L. 301       578  LOAD_FAST                'i'
              580  LOAD_GLOBAL              Image
              582  LOAD_ATTR                OPEN
              584  <118>                 0  ''
          586_588  POP_JUMP_IF_FALSE   600  'to 600'

 L. 302       590  LOAD_FAST                'features'
              592  LOAD_METHOD              append
              594  LOAD_STR                 'open'
              596  CALL_METHOD_1         1  ''
              598  POP_TOP          
            600_0  COME_FROM           586  '586'

 L. 303       600  LOAD_FAST                'i'
              602  LOAD_GLOBAL              Image
              604  LOAD_ATTR                SAVE
              606  <118>                 0  ''
          608_610  POP_JUMP_IF_FALSE   622  'to 622'

 L. 304       612  LOAD_FAST                'features'
              614  LOAD_METHOD              append
              616  LOAD_STR                 'save'
              618  CALL_METHOD_1         1  ''
              620  POP_TOP          
            622_0  COME_FROM           608  '608'

 L. 305       622  LOAD_FAST                'i'
              624  LOAD_GLOBAL              Image
              626  LOAD_ATTR                SAVE_ALL
              628  <118>                 0  ''
          630_632  POP_JUMP_IF_FALSE   644  'to 644'

 L. 306       634  LOAD_FAST                'features'
              636  LOAD_METHOD              append
              638  LOAD_STR                 'save_all'
              640  CALL_METHOD_1         1  ''
              642  POP_TOP          
            644_0  COME_FROM           630  '630'

 L. 307       644  LOAD_FAST                'i'
              646  LOAD_GLOBAL              Image
              648  LOAD_ATTR                DECODERS
              650  <118>                 0  ''
          652_654  POP_JUMP_IF_FALSE   666  'to 666'

 L. 308       656  LOAD_FAST                'features'
              658  LOAD_METHOD              append
              660  LOAD_STR                 'decode'
              662  CALL_METHOD_1         1  ''
              664  POP_TOP          
            666_0  COME_FROM           652  '652'

 L. 309       666  LOAD_FAST                'i'
              668  LOAD_GLOBAL              Image
              670  LOAD_ATTR                ENCODERS
              672  <118>                 0  ''
          674_676  POP_JUMP_IF_FALSE   688  'to 688'

 L. 310       678  LOAD_FAST                'features'
              680  LOAD_METHOD              append
              682  LOAD_STR                 'encode'
              684  CALL_METHOD_1         1  ''
              686  POP_TOP          
            688_0  COME_FROM           674  '674'

 L. 312       688  LOAD_GLOBAL              print
              690  LOAD_STR                 'Features: {}'
              692  LOAD_METHOD              format
              694  LOAD_STR                 ', '
              696  LOAD_METHOD              join
              698  LOAD_FAST                'features'
              700  CALL_METHOD_1         1  ''
              702  CALL_METHOD_1         1  ''
              704  LOAD_FAST                'out'
              706  LOAD_CONST               ('file',)
              708  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              710  POP_TOP          

 L. 313       712  LOAD_GLOBAL              print
              714  LOAD_STR                 '--------------------------------------------------------------------'
              716  LOAD_FAST                'out'
              718  LOAD_CONST               ('file',)
              720  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              722  POP_TOP          
          724_726  JUMP_BACK           478  'to 478'
            728_0  COME_FROM           478  '478'
            728_1  COME_FROM           418  '418'

Parse error at or near `None' instruction at offset -1