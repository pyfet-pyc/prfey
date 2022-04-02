# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\features.py
import collections, os, sys, warnings, PIL
from . import Image
modules = {'pil':('PIL._imaging', 'PILLOW_VERSION'), 
 'tkinter':('PIL._tkinter_finder', 'tk_version'), 
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
 'fribidi':('PIL._imagingft', 'HAVE_FRIBIDI', 'fribidi_version'), 
 'harfbuzz':('PIL._imagingft', 'HAVE_HARFBUZZ', 'harfbuzz_version'), 
 'libjpeg_turbo':('PIL._imaging', 'HAVE_LIBJPEGTURBO', 'libjpeg_turbo_version'), 
 'libimagequant':('PIL._imaging', 'HAVE_LIBIMAGEQUANT', 'imagequant_version'), 
 'xcb':('PIL._imaging', 'HAVE_XCB', None)}

def check_feature--- This code section failed: ---

 L. 137         0  LOAD_FAST                'feature'
                2  LOAD_GLOBAL              features
                4  <118>                 1  ''
                6  POP_JUMP_IF_FALSE    22  'to 22'

 L. 138         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 'Unknown feature '
               12  LOAD_FAST                'feature'
               14  FORMAT_VALUE          0  ''
               16  BUILD_STRING_2        2 
               18  CALL_FUNCTION_1       1  ''
               20  RAISE_VARARGS_1       1  'exception instance'
             22_0  COME_FROM             6  '6'

 L. 140        22  LOAD_GLOBAL              features
               24  LOAD_FAST                'feature'
               26  BINARY_SUBSCR    
               28  UNPACK_SEQUENCE_3     3 
               30  STORE_FAST               'module'
               32  STORE_FAST               'flag'
               34  STORE_FAST               'ver'

 L. 142        36  SETUP_FINALLY        64  'to 64'

 L. 143        38  LOAD_GLOBAL              __import__
               40  LOAD_FAST                'module'
               42  LOAD_STR                 'PIL'
               44  BUILD_LIST_1          1 
               46  LOAD_CONST               ('fromlist',)
               48  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               50  STORE_FAST               'imported_module'

 L. 144        52  LOAD_GLOBAL              getattr
               54  LOAD_FAST                'imported_module'
               56  LOAD_FAST                'flag'
               58  CALL_FUNCTION_2       2  ''
               60  POP_BLOCK        
               62  RETURN_VALUE     
             64_0  COME_FROM_FINALLY    36  '36'

 L. 145        64  DUP_TOP          
               66  LOAD_GLOBAL              ImportError
               68  <121>                82  ''
               70  POP_TOP          
               72  POP_TOP          
               74  POP_TOP          

 L. 146        76  POP_EXCEPT       
               78  LOAD_CONST               None
               80  RETURN_VALUE     
               82  <48>             

Parse error at or near `None' instruction at offset -1


def version_feature--- This code section failed: ---

 L. 155         0  LOAD_GLOBAL              check_feature
                2  LOAD_FAST                'feature'
                4  CALL_FUNCTION_1       1  ''
                6  POP_JUMP_IF_TRUE     12  'to 12'

 L. 156         8  LOAD_CONST               None
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L. 158        12  LOAD_GLOBAL              features
               14  LOAD_FAST                'feature'
               16  BINARY_SUBSCR    
               18  UNPACK_SEQUENCE_3     3 
               20  STORE_FAST               'module'
               22  STORE_FAST               'flag'
               24  STORE_FAST               'ver'

 L. 160        26  LOAD_FAST                'ver'
               28  LOAD_CONST               None
               30  <117>                 0  ''
               32  POP_JUMP_IF_FALSE    38  'to 38'

 L. 161        34  LOAD_CONST               None
               36  RETURN_VALUE     
             38_0  COME_FROM            32  '32'

 L. 163        38  LOAD_GLOBAL              getattr
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

 L. 181         0  LOAD_FAST                'feature'
                2  LOAD_GLOBAL              modules
                4  <118>                 0  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 182         8  LOAD_GLOBAL              check_module
               10  LOAD_FAST                'feature'
               12  CALL_FUNCTION_1       1  ''
               14  RETURN_VALUE     
             16_0  COME_FROM             6  '6'

 L. 183        16  LOAD_FAST                'feature'
               18  LOAD_GLOBAL              codecs
               20  <118>                 0  ''
               22  POP_JUMP_IF_FALSE    32  'to 32'

 L. 184        24  LOAD_GLOBAL              check_codec
               26  LOAD_FAST                'feature'
               28  CALL_FUNCTION_1       1  ''
               30  RETURN_VALUE     
             32_0  COME_FROM            22  '22'

 L. 185        32  LOAD_FAST                'feature'
               34  LOAD_GLOBAL              features
               36  <118>                 0  ''
               38  POP_JUMP_IF_FALSE    48  'to 48'

 L. 186        40  LOAD_GLOBAL              check_feature
               42  LOAD_FAST                'feature'
               44  CALL_FUNCTION_1       1  ''
               46  RETURN_VALUE     
             48_0  COME_FROM            38  '38'

 L. 187        48  LOAD_GLOBAL              warnings
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

 L. 188        70  LOAD_CONST               False
               72  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def version--- This code section failed: ---

 L. 198         0  LOAD_FAST                'feature'
                2  LOAD_GLOBAL              modules
                4  <118>                 0  ''
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 199         8  LOAD_GLOBAL              version_module
               10  LOAD_FAST                'feature'
               12  CALL_FUNCTION_1       1  ''
               14  RETURN_VALUE     
             16_0  COME_FROM             6  '6'

 L. 200        16  LOAD_FAST                'feature'
               18  LOAD_GLOBAL              codecs
               20  <118>                 0  ''
               22  POP_JUMP_IF_FALSE    32  'to 32'

 L. 201        24  LOAD_GLOBAL              version_codec
               26  LOAD_FAST                'feature'
               28  CALL_FUNCTION_1       1  ''
               30  RETURN_VALUE     
             32_0  COME_FROM            22  '22'

 L. 202        32  LOAD_FAST                'feature'
               34  LOAD_GLOBAL              features
               36  <118>                 0  ''
               38  POP_JUMP_IF_FALSE    48  'to 48'

 L. 203        40  LOAD_GLOBAL              version_feature
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

 L. 229         0  LOAD_FAST                'out'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 230         8  LOAD_GLOBAL              sys
               10  LOAD_ATTR                stdout
               12  STORE_FAST               'out'
             14_0  COME_FROM             6  '6'

 L. 232        14  LOAD_GLOBAL              Image
               16  LOAD_METHOD              init
               18  CALL_METHOD_0         0  ''
               20  POP_TOP          

 L. 234        22  LOAD_GLOBAL              print
               24  LOAD_STR                 '--------------------------------------------------------------------'
               26  LOAD_FAST                'out'
               28  LOAD_CONST               ('file',)
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  POP_TOP          

 L. 235        34  LOAD_GLOBAL              print
               36  LOAD_STR                 'Pillow '
               38  LOAD_GLOBAL              PIL
               40  LOAD_ATTR                __version__
               42  FORMAT_VALUE          0  ''
               44  BUILD_STRING_2        2 
               46  LOAD_FAST                'out'
               48  LOAD_CONST               ('file',)
               50  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               52  POP_TOP          

 L. 236        54  LOAD_GLOBAL              sys
               56  LOAD_ATTR                version
               58  LOAD_METHOD              splitlines
               60  CALL_METHOD_0         0  ''
               62  STORE_FAST               'py_version'

 L. 237        64  LOAD_GLOBAL              print
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

 L. 238        90  LOAD_FAST                'py_version'
               92  LOAD_CONST               1
               94  LOAD_CONST               None
               96  BUILD_SLICE_2         2 
               98  BINARY_SUBSCR    
              100  GET_ITER         
              102  FOR_ITER            130  'to 130'
              104  STORE_FAST               'py_version'

 L. 239       106  LOAD_GLOBAL              print
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

 L. 240       130  LOAD_GLOBAL              print
              132  LOAD_STR                 '--------------------------------------------------------------------'
              134  LOAD_FAST                'out'
              136  LOAD_CONST               ('file',)
              138  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              140  POP_TOP          

 L. 241       142  LOAD_GLOBAL              print

 L. 242       144  LOAD_STR                 'Python modules loaded from '
              146  LOAD_GLOBAL              os
              148  LOAD_ATTR                path
              150  LOAD_METHOD              dirname
              152  LOAD_GLOBAL              Image
              154  LOAD_ATTR                __file__
              156  CALL_METHOD_1         1  ''
              158  FORMAT_VALUE          0  ''
              160  BUILD_STRING_2        2 

 L. 243       162  LOAD_FAST                'out'

 L. 241       164  LOAD_CONST               ('file',)
              166  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              168  POP_TOP          

 L. 245       170  LOAD_GLOBAL              print

 L. 246       172  LOAD_STR                 'Binary modules loaded from '
              174  LOAD_GLOBAL              os
              176  LOAD_ATTR                path
              178  LOAD_METHOD              dirname
              180  LOAD_GLOBAL              Image
              182  LOAD_ATTR                core
              184  LOAD_ATTR                __file__
              186  CALL_METHOD_1         1  ''
              188  FORMAT_VALUE          0  ''
              190  BUILD_STRING_2        2 

 L. 247       192  LOAD_FAST                'out'

 L. 245       194  LOAD_CONST               ('file',)
              196  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              198  POP_TOP          

 L. 249       200  LOAD_GLOBAL              print
              202  LOAD_STR                 '--------------------------------------------------------------------'
              204  LOAD_FAST                'out'
              206  LOAD_CONST               ('file',)
              208  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              210  POP_TOP          

 L. 251       212  LOAD_CONST               (('pil', 'PIL CORE'), ('tkinter', 'TKINTER'), ('freetype2', 'FREETYPE2'), ('littlecms2', 'LITTLECMS2'), ('webp', 'WEBP'), ('transp_webp', 'WEBP Transparency'), ('webp_mux', 'WEBPMUX'), ('webp_anim', 'WEBP Animation'), ('jpg', 'JPEG'), ('jpg_2000', 'OPENJPEG (JPEG2000)'), ('zlib', 'ZLIB (PNG/ZIP)'), ('libtiff', 'LIBTIFF'), ('raqm', 'RAQM (Bidirectional Text)'), ('libimagequant', 'LIBIMAGEQUANT (Quantization method)'), ('xcb', 'XCB (X protocol)'))
              214  GET_ITER         
              216  FOR_ITER            464  'to 464'
              218  UNPACK_SEQUENCE_2     2 
              220  STORE_FAST               'name'
              222  STORE_FAST               'feature'

 L. 268       224  LOAD_GLOBAL              check
              226  LOAD_FAST                'name'
              228  CALL_FUNCTION_1       1  ''
          230_232  POP_JUMP_IF_FALSE   446  'to 446'

 L. 269       234  LOAD_FAST                'name'
              236  LOAD_STR                 'jpg'
              238  COMPARE_OP               ==
          240_242  POP_JUMP_IF_FALSE   268  'to 268'
              244  LOAD_GLOBAL              check_feature
              246  LOAD_STR                 'libjpeg_turbo'
              248  CALL_FUNCTION_1       1  ''
          250_252  POP_JUMP_IF_FALSE   268  'to 268'

 L. 270       254  LOAD_STR                 'libjpeg-turbo '
              256  LOAD_GLOBAL              version_feature
              258  LOAD_STR                 'libjpeg_turbo'
              260  CALL_FUNCTION_1       1  ''
              262  BINARY_ADD       
              264  STORE_FAST               'v'
              266  JUMP_FORWARD        276  'to 276'
            268_0  COME_FROM           250  '250'
            268_1  COME_FROM           240  '240'

 L. 272       268  LOAD_GLOBAL              version
              270  LOAD_FAST                'name'
              272  CALL_FUNCTION_1       1  ''
              274  STORE_FAST               'v'
            276_0  COME_FROM           266  '266'

 L. 273       276  LOAD_FAST                'v'
              278  LOAD_CONST               None
              280  <117>                 1  ''
          282_284  POP_JUMP_IF_FALSE   428  'to 428'

 L. 274       286  LOAD_FAST                'name'
              288  LOAD_CONST               ('pil', 'jpg')
              290  <118>                 0  ''
              292  STORE_FAST               'version_static'

 L. 275       294  LOAD_FAST                'name'
              296  LOAD_STR                 'littlecms2'
              298  COMPARE_OP               ==
          300_302  POP_JUMP_IF_FALSE   332  'to 332'

 L. 277       304  LOAD_GLOBAL              tuple
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

 L. 278       332  LOAD_FAST                'version_static'
          334_336  POP_JUMP_IF_FALSE   342  'to 342'
              338  LOAD_STR                 'compiled for'
              340  JUMP_FORWARD        344  'to 344'
            342_0  COME_FROM           334  '334'
              342  LOAD_STR                 'loaded'
            344_0  COME_FROM           340  '340'
              344  STORE_FAST               't'

 L. 279       346  LOAD_FAST                'name'
              348  LOAD_STR                 'raqm'
              350  COMPARE_OP               ==
          352_354  POP_JUMP_IF_FALSE   406  'to 406'

 L. 280       356  LOAD_CONST               ('fribidi', 'harfbuzz')
              358  GET_ITER         
            360_0  COME_FROM           378  '378'
              360  FOR_ITER            406  'to 406'
              362  STORE_FAST               'f'

 L. 281       364  LOAD_GLOBAL              version_feature
              366  LOAD_FAST                'f'
              368  CALL_FUNCTION_1       1  ''
              370  STORE_FAST               'v2'

 L. 282       372  LOAD_FAST                'v2'
              374  LOAD_CONST               None
              376  <117>                 1  ''
          378_380  POP_JUMP_IF_FALSE   360  'to 360'

 L. 283       382  LOAD_FAST                'v'
              384  LOAD_STR                 ', '
              386  LOAD_FAST                'f'
              388  FORMAT_VALUE          0  ''
              390  LOAD_STR                 ' '
              392  LOAD_FAST                'v2'
              394  FORMAT_VALUE          0  ''
              396  BUILD_STRING_4        4 
              398  INPLACE_ADD      
              400  STORE_FAST               'v'
          402_404  JUMP_BACK           360  'to 360'
            406_0  COME_FROM           352  '352'

 L. 284       406  LOAD_GLOBAL              print
              408  LOAD_STR                 '---'
              410  LOAD_FAST                'feature'
              412  LOAD_STR                 'support ok,'
              414  LOAD_FAST                't'
              416  LOAD_FAST                'v'
              418  LOAD_FAST                'out'
              420  LOAD_CONST               ('file',)
              422  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              424  POP_TOP          
              426  JUMP_FORWARD        444  'to 444'
            428_0  COME_FROM           282  '282'

 L. 286       428  LOAD_GLOBAL              print
              430  LOAD_STR                 '---'
              432  LOAD_FAST                'feature'
              434  LOAD_STR                 'support ok'
              436  LOAD_FAST                'out'
              438  LOAD_CONST               ('file',)
              440  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              442  POP_TOP          
            444_0  COME_FROM           426  '426'
              444  JUMP_BACK           216  'to 216'
            446_0  COME_FROM           230  '230'

 L. 288       446  LOAD_GLOBAL              print
              448  LOAD_STR                 '***'
              450  LOAD_FAST                'feature'
              452  LOAD_STR                 'support not installed'
              454  LOAD_FAST                'out'
              456  LOAD_CONST               ('file',)
              458  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              460  POP_TOP          
              462  JUMP_BACK           216  'to 216'

 L. 289       464  LOAD_GLOBAL              print
              466  LOAD_STR                 '--------------------------------------------------------------------'
              468  LOAD_FAST                'out'
              470  LOAD_CONST               ('file',)
              472  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              474  POP_TOP          

 L. 291       476  LOAD_FAST                'supported_formats'
          478_480  POP_JUMP_IF_FALSE   788  'to 788'

 L. 292       482  LOAD_GLOBAL              collections
              484  LOAD_METHOD              defaultdict
              486  LOAD_GLOBAL              list
              488  CALL_METHOD_1         1  ''
              490  STORE_FAST               'extensions'

 L. 293       492  LOAD_GLOBAL              Image
              494  LOAD_ATTR                EXTENSION
              496  LOAD_METHOD              items
              498  CALL_METHOD_0         0  ''
              500  GET_ITER         
              502  FOR_ITER            528  'to 528'
              504  UNPACK_SEQUENCE_2     2 
              506  STORE_FAST               'ext'
              508  STORE_FAST               'i'

 L. 294       510  LOAD_FAST                'extensions'
              512  LOAD_FAST                'i'
              514  BINARY_SUBSCR    
              516  LOAD_METHOD              append
              518  LOAD_FAST                'ext'
              520  CALL_METHOD_1         1  ''
              522  POP_TOP          
          524_526  JUMP_BACK           502  'to 502'

 L. 296       528  LOAD_GLOBAL              sorted
              530  LOAD_GLOBAL              Image
              532  LOAD_ATTR                ID
              534  CALL_FUNCTION_1       1  ''
              536  GET_ITER         
              538  FOR_ITER            788  'to 788'
              540  STORE_FAST               'i'

 L. 297       542  LOAD_FAST                'i'
              544  FORMAT_VALUE          0  ''
              546  STORE_FAST               'line'

 L. 298       548  LOAD_FAST                'i'
              550  LOAD_GLOBAL              Image
              552  LOAD_ATTR                MIME
              554  <118>                 0  ''
          556_558  POP_JUMP_IF_FALSE   580  'to 580'

 L. 299       560  LOAD_FAST                'line'
              562  FORMAT_VALUE          0  ''
              564  LOAD_STR                 ' '
              566  LOAD_GLOBAL              Image
              568  LOAD_ATTR                MIME
              570  LOAD_FAST                'i'
              572  BINARY_SUBSCR    
              574  FORMAT_VALUE          0  ''
              576  BUILD_STRING_3        3 
              578  STORE_FAST               'line'
            580_0  COME_FROM           556  '556'

 L. 300       580  LOAD_GLOBAL              print
              582  LOAD_FAST                'line'
              584  LOAD_FAST                'out'
              586  LOAD_CONST               ('file',)
              588  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              590  POP_TOP          

 L. 302       592  LOAD_FAST                'i'
              594  LOAD_FAST                'extensions'
              596  <118>                 0  ''
          598_600  POP_JUMP_IF_FALSE   634  'to 634'

 L. 303       602  LOAD_GLOBAL              print

 L. 304       604  LOAD_STR                 'Extensions: {}'
              606  LOAD_METHOD              format
              608  LOAD_STR                 ', '
              610  LOAD_METHOD              join
              612  LOAD_GLOBAL              sorted
              614  LOAD_FAST                'extensions'
              616  LOAD_FAST                'i'
              618  BINARY_SUBSCR    
              620  CALL_FUNCTION_1       1  ''
              622  CALL_METHOD_1         1  ''
              624  CALL_METHOD_1         1  ''
              626  LOAD_FAST                'out'

 L. 303       628  LOAD_CONST               ('file',)
              630  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              632  POP_TOP          
            634_0  COME_FROM           598  '598'

 L. 307       634  BUILD_LIST_0          0 
              636  STORE_FAST               'features'

 L. 308       638  LOAD_FAST                'i'
              640  LOAD_GLOBAL              Image
              642  LOAD_ATTR                OPEN
              644  <118>                 0  ''
          646_648  POP_JUMP_IF_FALSE   660  'to 660'

 L. 309       650  LOAD_FAST                'features'
              652  LOAD_METHOD              append
              654  LOAD_STR                 'open'
              656  CALL_METHOD_1         1  ''
              658  POP_TOP          
            660_0  COME_FROM           646  '646'

 L. 310       660  LOAD_FAST                'i'
              662  LOAD_GLOBAL              Image
              664  LOAD_ATTR                SAVE
              666  <118>                 0  ''
          668_670  POP_JUMP_IF_FALSE   682  'to 682'

 L. 311       672  LOAD_FAST                'features'
              674  LOAD_METHOD              append
              676  LOAD_STR                 'save'
              678  CALL_METHOD_1         1  ''
              680  POP_TOP          
            682_0  COME_FROM           668  '668'

 L. 312       682  LOAD_FAST                'i'
              684  LOAD_GLOBAL              Image
              686  LOAD_ATTR                SAVE_ALL
              688  <118>                 0  ''
          690_692  POP_JUMP_IF_FALSE   704  'to 704'

 L. 313       694  LOAD_FAST                'features'
              696  LOAD_METHOD              append
              698  LOAD_STR                 'save_all'
              700  CALL_METHOD_1         1  ''
              702  POP_TOP          
            704_0  COME_FROM           690  '690'

 L. 314       704  LOAD_FAST                'i'
              706  LOAD_GLOBAL              Image
              708  LOAD_ATTR                DECODERS
              710  <118>                 0  ''
          712_714  POP_JUMP_IF_FALSE   726  'to 726'

 L. 315       716  LOAD_FAST                'features'
              718  LOAD_METHOD              append
              720  LOAD_STR                 'decode'
              722  CALL_METHOD_1         1  ''
              724  POP_TOP          
            726_0  COME_FROM           712  '712'

 L. 316       726  LOAD_FAST                'i'
              728  LOAD_GLOBAL              Image
              730  LOAD_ATTR                ENCODERS
              732  <118>                 0  ''
          734_736  POP_JUMP_IF_FALSE   748  'to 748'

 L. 317       738  LOAD_FAST                'features'
              740  LOAD_METHOD              append
              742  LOAD_STR                 'encode'
              744  CALL_METHOD_1         1  ''
              746  POP_TOP          
            748_0  COME_FROM           734  '734'

 L. 319       748  LOAD_GLOBAL              print
              750  LOAD_STR                 'Features: {}'
              752  LOAD_METHOD              format
              754  LOAD_STR                 ', '
              756  LOAD_METHOD              join
              758  LOAD_FAST                'features'
              760  CALL_METHOD_1         1  ''
              762  CALL_METHOD_1         1  ''
              764  LOAD_FAST                'out'
              766  LOAD_CONST               ('file',)
              768  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              770  POP_TOP          

 L. 320       772  LOAD_GLOBAL              print
              774  LOAD_STR                 '--------------------------------------------------------------------'
              776  LOAD_FAST                'out'
              778  LOAD_CONST               ('file',)
              780  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              782  POP_TOP          
          784_786  JUMP_BACK           538  'to 538'
            788_0  COME_FROM           478  '478'

Parse error at or near `None' instruction at offset -1