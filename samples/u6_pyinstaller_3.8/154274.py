# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
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
                6  POP_JUMP_IF_FALSE    20  'to 20'

 L.  28         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 'Unknown module %s'
               12  LOAD_FAST                'feature'
               14  BINARY_MODULO    
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM             6  '6'

 L.  30        20  LOAD_GLOBAL              modules
               22  LOAD_FAST                'feature'
               24  BINARY_SUBSCR    
               26  UNPACK_SEQUENCE_2     2 
               28  STORE_FAST               'module'
               30  STORE_FAST               'ver'

 L.  32        32  SETUP_FINALLY        48  'to 48'

 L.  33        34  LOAD_GLOBAL              __import__
               36  LOAD_FAST                'module'
               38  CALL_FUNCTION_1       1  ''
               40  POP_TOP          

 L.  34        42  POP_BLOCK        
               44  LOAD_CONST               True
               46  RETURN_VALUE     
             48_0  COME_FROM_FINALLY    32  '32'

 L.  35        48  DUP_TOP          
               50  LOAD_GLOBAL              ImportError
               52  COMPARE_OP               exception-match
               54  POP_JUMP_IF_FALSE    68  'to 68'
               56  POP_TOP          
               58  POP_TOP          
               60  POP_TOP          

 L.  36        62  POP_EXCEPT       
               64  LOAD_CONST               False
               66  RETURN_VALUE     
             68_0  COME_FROM            54  '54'
               68  END_FINALLY      

Parse error at or near `RETURN_VALUE' instruction at offset 46


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
        raise ValueError('Unknown codec %s' % feature)
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
                6  POP_JUMP_IF_FALSE    20  'to 20'

 L. 136         8  LOAD_GLOBAL              ValueError
               10  LOAD_STR                 'Unknown feature %s'
               12  LOAD_FAST                'feature'
               14  BINARY_MODULO    
               16  CALL_FUNCTION_1       1  ''
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM             6  '6'

 L. 138        20  LOAD_GLOBAL              features
               22  LOAD_FAST                'feature'
               24  BINARY_SUBSCR    
               26  UNPACK_SEQUENCE_3     3 
               28  STORE_FAST               'module'
               30  STORE_FAST               'flag'
               32  STORE_FAST               'ver'

 L. 140        34  SETUP_FINALLY        62  'to 62'

 L. 141        36  LOAD_GLOBAL              __import__
               38  LOAD_FAST                'module'
               40  LOAD_STR                 'PIL'
               42  BUILD_LIST_1          1 
               44  LOAD_CONST               ('fromlist',)
               46  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               48  STORE_FAST               'imported_module'

 L. 142        50  LOAD_GLOBAL              getattr
               52  LOAD_FAST                'imported_module'
               54  LOAD_FAST                'flag'
               56  CALL_FUNCTION_2       2  ''
               58  POP_BLOCK        
               60  RETURN_VALUE     
             62_0  COME_FROM_FINALLY    34  '34'

 L. 143        62  DUP_TOP          
               64  LOAD_GLOBAL              ImportError
               66  COMPARE_OP               exception-match
               68  POP_JUMP_IF_FALSE    82  'to 82'
               70  POP_TOP          
               72  POP_TOP          
               74  POP_TOP          

 L. 144        76  POP_EXCEPT       
               78  LOAD_CONST               None
               80  RETURN_VALUE     
             82_0  COME_FROM            68  '68'
               82  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 72


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
    warnings.warn(("Unknown feature '%s'." % feature), stacklevel=2)
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
    print(('Pillow {}'.format(PIL.__version__)), file=out)
    py_version = sys.version.splitlines()
    print(('Python {}'.format(py_version[0].strip())), file=out)
    for py_version in py_version[1:]:
        print(('       {}'.format(py_version.strip())), file=out)
    else:
        print('--------------------------------------------------------------------', file=out)
        print(('Python modules loaded from {}'.format(os.path.dirname(Image.__file__))),
          file=out)
        print(('Binary modules loaded from {}'.format(os.path.dirname(Image.core.__file__))),
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
                if name == 'jpg':
                    if check_feature('libjpeg_turbo'):
                        v = 'libjpeg-turbo ' + version_feature('libjpeg_turbo')
                    else:
                        v = version(name)
                elif v is not None:
                    t = 'compiled for' if name in ('pil', 'jpg') else 'loaded'
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
                        line = '{}'.format(i)
                        if i in Image.MIME:
                            line = '{} {}'.format(line, Image.MIME[i])
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