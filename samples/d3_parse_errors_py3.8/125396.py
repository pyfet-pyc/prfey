# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
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
                4  COMPARE_OP               not-in
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
               54  COMPARE_OP               exception-match
               56  POP_JUMP_IF_FALSE    70  'to 70'
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          

 L.  36        64  POP_EXCEPT       
               66  LOAD_CONST               False
               68  RETURN_VALUE     
             70_0  COME_FROM            56  '56'
               70  END_FINALLY      

Parse error at or near `DUP_TOP' instruction at offset 50


def version_module(feature):
    """
    :param feature: The module to check for.
    :returns:
        The loaded version number as a string, or ``None`` if unknown or not available.
    :raises ValueError: If the module is not defined in this version of Pillow.
    """
    if not check_module(feature):
        return
    module, ver = modules[feature]
    if ver is None:
        return
    return getattr(__import__(module, fromlist=[ver]), ver)


def get_supported_modules():
    """
    :returns: A list of all supported modules.
    """
    return [f for f in modules if check_module(f)]


codecs = {'jpg':('jpeg', 'jpeglib'), 
 'jpg_2000':('jpeg2k', 'jp2klib'), 
 'zlib':('zip', 'zlib'), 
 'libtiff':('libtiff', 'libtiff')}

def check_codec(feature):
    """
    Checks if a codec is available.

    :param feature: The codec to check for.
    :returns: ``True`` if available, ``False`` otherwise.
    :raises ValueError: If the codec is not defined in this version of Pillow.
    """
    if feature not in codecs:
        raise ValueError(f"Unknown codec {feature}")
    codec, lib = codecs[feature]
    return codec + '_encoder' in dir(Image.core)


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
    version = getattr(Image.core, lib + '_version')
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
                4  COMPARE_OP               not-in
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
               68  COMPARE_OP               exception-match
               70  POP_JUMP_IF_FALSE    84  'to 84'
               72  POP_TOP          
               74  POP_TOP          
               76  POP_TOP          

 L. 144        78  POP_EXCEPT       
               80  LOAD_CONST               None
               82  RETURN_VALUE     
             84_0  COME_FROM            70  '70'
               84  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 80


def version_feature(feature):
    """
    :param feature: The feature to check for.
    :returns: The version number as a string, or ``None`` if not available.
    :raises ValueError: If the feature is not defined in this version of Pillow.
    """
    if not check_feature(feature):
        return
    module, flag, ver = features[feature]
    if ver is None:
        return
    return getattr(__import__(module, fromlist=[ver]), ver)


def get_supported_features():
    """
    :returns: A list of all supported features.
    """
    return [f for f in features if check_feature(f)]


def check(feature):
    """
    :param feature: A module, codec, or feature name.
    :returns:
        ``True`` if the module, codec, or feature is available,
        ``False`` or ``None`` otherwise.
    """
    if feature in modules:
        return check_module(feature)
    if feature in codecs:
        return check_codec(feature)
    if feature in features:
        return check_feature(feature)
    warnings.warn(f"Unknown feature '{feature}'.", stacklevel=2)
    return False


def version(feature):
    """
    :param feature:
        The module, codec, or feature to check for.
    :returns:
        The version number as a string, or ``None`` if unknown or not available.
    """
    if feature in modules:
        return version_module(feature)
    if feature in codecs:
        return version_codec(feature)
    if feature in features:
        return version_feature(feature)


def get_supported():
    """
    :returns: A list of all supported modules, features, and codecs.
    """
    ret = get_supported_modules()
    ret.extend(get_supported_features())
    ret.extend(get_supported_codecs())
    return ret


def pilinfo(out=None, supported_formats=True):
    """
    Prints information about this installation of Pillow.
    This function can be called with ``python -m PIL``.

    :param out:
        The output stream to print to. Defaults to ``sys.stdout`` if ``None``.
    :param supported_formats:
        If ``True``, a list of all supported image file formats will be printed.
    """
    if out is None:
        out = sys.stdout
    Image.init()
    print('--------------------------------------------------------------------', file=out)
    print(f"Pillow {PIL.__version__}", file=out)
    py_version = sys.version.splitlines()
    print(f"Python {py_version[0].strip()}", file=out)
    for py_version in py_version[1:]:
        print(f"       {py_version.strip()}", file=out)
    else:
        print('--------------------------------------------------------------------', file=out)
        print(f"Python modules loaded from {os.path.dirname(Image.__file__)}",
          file=out)
        print(f"Binary modules loaded from {os.path.dirname(Image.core.__file__)}",
          file=out)
        print('--------------------------------------------------------------------', file=out)
        for name, feature in (('pil', 'PIL CORE'), ('tkinter', 'TKINTER'), ('freetype2', 'FREETYPE2'),
                              ('littlecms2', 'LITTLECMS2'), ('webp', 'WEBP'), ('transp_webp', 'WEBP Transparency'),
                              ('webp_mux', 'WEBPMUX'), ('webp_anim', 'WEBP Animation'),
                              ('jpg', 'JPEG'), ('jpg_2000', 'OPENJPEG (JPEG2000)'),
                              ('zlib', 'ZLIB (PNG/ZIP)'), ('libtiff', 'LIBTIFF'),
                              ('raqm', 'RAQM (Bidirectional Text)'), ('libimagequant', 'LIBIMAGEQUANT (Quantization method)'),
                              ('xcb', 'XCB (X protocol)')):
            if check(name):
                if name == 'jpg' and check_feature('libjpeg_turbo'):
                    v = 'libjpeg-turbo ' + version_feature('libjpeg_turbo')
                else:
                    v = version(name)
                if v is not None:
                    version_static = name in ('pil', 'jpg')
                    if name == 'littlecms2':
                        version_static = tuple((int(x) for x in v.split('.'))) < (2,
                                                                                  7)
                    t = 'compiled for' if version_static else 'loaded'
                    print('---', feature, 'support ok,', t, v, file=out)
                else:
                    print('---', feature, 'support ok', file=out)
            else:
                print('***', feature, 'support not installed', file=out)
        else:
            print('--------------------------------------------------------------------', file=out)
            if supported_formats:
                extensions = collections.defaultdict(list)
                for ext, i in Image.EXTENSION.items():
                    extensions[i].append(ext)
                else:
                    for i in sorted(Image.ID):
                        line = f"{i}"
                        if i in Image.MIME:
                            line = f"{line} {Image.MIME[i]}"
                        else:
                            print(line, file=out)
                            if i in extensions:
                                print(('Extensions: {}'.format(', '.join(sorted(extensions[i])))),
                                  file=out)
                            features = []
                            if i in Image.OPEN:
                                features.append('open')
                            if i in Image.SAVE:
                                features.append('save')
                            if i in Image.SAVE_ALL:
                                features.append('save_all')
                            if i in Image.DECODERS:
                                features.append('decode')
                            if i in Image.ENCODERS:
                                features.append('encode')
                            print(('Features: {}'.format(', '.join(features))), file=out)
                            print('--------------------------------------------------------------------', file=out)