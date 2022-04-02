# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: mimetypes.py
"""Guess the MIME type of a file.

This module defines two useful functions:

guess_type(url, strict=True) -- guess the MIME type and encoding of a URL.

guess_extension(type, strict=True) -- guess the extension for a given MIME type.

It also contains the following, for tuning the behavior:

Data:

knownfiles -- list of files to parse
inited -- flag set when init() has been called
suffix_map -- dictionary mapping suffixes to suffixes
encodings_map -- dictionary mapping suffixes to encodings
types_map -- dictionary mapping suffixes to types

Functions:

init([files]) -- parse a list of files, default knownfiles (on Windows, the
  default values are taken from the registry)
read_mime_types(file) -- parse one file, return a dictionary or None
"""
import os, sys, posixpath, urllib.parse
try:
    import winreg as _winreg
except ImportError:
    _winreg = None

__all__ = [
 'knownfiles', 'inited', 'MimeTypes',
 'guess_type', 'guess_all_extensions', 'guess_extension',
 'add_type', 'init', 'read_mime_types',
 'suffix_map', 'encodings_map', 'types_map', 'common_types']
knownfiles = [
 '/etc/mime.types',
 '/etc/httpd/mime.types',
 '/etc/httpd/conf/mime.types',
 '/etc/apache/mime.types',
 '/etc/apache2/mime.types',
 '/usr/local/etc/httpd/conf/mime.types',
 '/usr/local/lib/netscape/mime.types',
 '/usr/local/etc/httpd/conf/mime.types',
 '/usr/local/etc/mime.types']
inited = False
_db = None

class MimeTypes:
    __doc__ = 'MIME-types datastore.\n\n    This datastore can handle information from mime.types-style files\n    and supports basic determination of MIME type from a filename or\n    URL, and can guess a reasonable extension given a MIME type.\n    '

    def __init__(self, filenames=(), strict=True):
        global inited
        if not inited:
            init()
        self.encodings_map = encodings_map.copy()
        self.suffix_map = suffix_map.copy()
        self.types_map = ({}, {})
        self.types_map_inv = ({}, {})
        for ext, type in types_map.items():
            self.add_type(type, ext, True)

        for ext, type in common_types.items():
            self.add_type(type, ext, False)

        for name in filenames:
            self.read(name, strict)

    def add_type(self, type, ext, strict=True):
        """Add a mapping between a type and an extension.

        When the extension is already known, the new
        type will replace the old one. When the type
        is already known the extension will be added
        to the list of known extensions.

        If strict is true, information will be added to
        list of standard types, else to the list of non-standard
        types.
        """
        self.types_map[strict][ext] = type
        exts = self.types_map_inv[strict].setdefault(type, [])
        if ext not in exts:
            exts.append(ext)

    def guess_type(self, url, strict=True):
        """Guess the type of a file based on its URL.

        Return value is a tuple (type, encoding) where type is None if
        the type can't be guessed (no or unknown suffix) or a string
        of the form type/subtype, usable for a MIME Content-type
        header; and encoding is None for no encoding or the name of
        the program used to encode (e.g. compress or gzip).  The
        mappings are table driven.  Encoding suffixes are case
        sensitive; type suffixes are first tried case sensitive, then
        case insensitive.

        The suffixes .tgz, .taz and .tz (case sensitive!) are all
        mapped to '.tar.gz'.  (This is table-driven too, using the
        dictionary suffix_map.)

        Optional `strict' argument when False adds a bunch of commonly found,
        but non-standard types.
        """
        scheme, url = urllib.parse.splittype(url)
        if scheme == 'data':
            comma = url.find(',')
            if comma < 0:
                return (None, None)
            semi = url.find(';', 0, comma)
            if semi >= 0:
                type = url[:semi]
            else:
                type = url[:comma]
            if '=' in type or ('/' not in type):
                type = 'text/plain'
            return (type, None)
        base, ext = posixpath.splitext(url)
        while ext in self.suffix_map:
            base, ext = posixpath.splitext(base + self.suffix_map[ext])

        if ext in self.encodings_map:
            encoding = self.encodings_map[ext]
            base, ext = posixpath.splitext(base)
        else:
            encoding = None
        types_map = self.types_map[True]
        if ext in types_map:
            return (types_map[ext], encoding)
        if ext.lower() in types_map:
            return (types_map[ext.lower()], encoding)
        if strict:
            return (None, encoding)
        types_map = self.types_map[False]
        if ext in types_map:
            return (types_map[ext], encoding)
        if ext.lower() in types_map:
            return (types_map[ext.lower()], encoding)
        return (
         None, encoding)

    def guess_all_extensions(self, type, strict=True):
        """Guess the extensions for a file based on its MIME type.

        Return value is a list of strings giving the possible filename
        extensions, including the leading dot ('.').  The extension is not
        guaranteed to have been associated with any particular data stream,
        but would be mapped to the MIME type `type' by guess_type().

        Optional `strict' argument when false adds a bunch of commonly found,
        but non-standard types.
        """
        type = type.lower()
        extensions = self.types_map_inv[True].get(type, [])
        if not strict:
            for ext in self.types_map_inv[False].get(type, []):
                if ext not in extensions:
                    extensions.append(ext)

        return extensions

    def guess_extension(self, type, strict=True):
        """Guess the extension for a file based on its MIME type.

        Return value is a string giving a filename extension,
        including the leading dot ('.').  The extension is not
        guaranteed to have been associated with any particular data
        stream, but would be mapped to the MIME type `type' by
        guess_type().  If no extension can be guessed for `type', None
        is returned.

        Optional `strict' argument when false adds a bunch of commonly found,
        but non-standard types.
        """
        extensions = self.guess_all_extensions(type, strict)
        if not extensions:
            return
        return extensions[0]

    def read(self, filename, strict=True):
        """
        Read a single mime.types-format file, specified by pathname.

        If strict is true, information will be added to
        list of standard types, else to the list of non-standard
        types.
        """
        with open(filename, encoding='utf-8') as fp:
            self.readfp(fp, strict)

    def readfp(self, fp, strict=True):
        """
        Read a single mime.types-format file.

        If strict is true, information will be added to
        list of standard types, else to the list of non-standard
        types.
        """
        while 1:
            line = fp.readline()
            if not line:
                break
            else:
                words = line.split()
                for i in range(len(words)):
                    if words[i][0] == '#':
                        del words[i:]
                        break

            if not words:
                continue
            else:
                type, suffixes = words[0], words[1:]
                for suff in suffixes:
                    self.add_type(type, '.' + suff, strict)

    def read_windows_registry--- This code section failed: ---

 L. 240         0  LOAD_GLOBAL              _winreg
                2  POP_JUMP_IF_TRUE      8  'to 8'

 L. 241         4  LOAD_CONST               None
                6  RETURN_VALUE     
              8_0  COME_FROM             2  '2'

 L. 243         8  LOAD_CODE                <code_object enum_types>
               10  LOAD_STR                 'MimeTypes.read_windows_registry.<locals>.enum_types'
               12  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               14  STORE_FAST               'enum_types'

 L. 255        16  LOAD_GLOBAL              _winreg
               18  LOAD_METHOD              OpenKey
               20  LOAD_GLOBAL              _winreg
               22  LOAD_ATTR                HKEY_CLASSES_ROOT
               24  LOAD_STR                 ''
               26  CALL_METHOD_2         2  '2 positional arguments'
               28  SETUP_WITH          160  'to 160'
               30  STORE_FAST               'hkcr'

 L. 256        32  SETUP_LOOP          156  'to 156'
               34  LOAD_FAST                'enum_types'
               36  LOAD_FAST                'hkcr'
               38  CALL_FUNCTION_1       1  '1 positional argument'
               40  GET_ITER         
             42_0  COME_FROM           152  '152'
             42_1  COME_FROM           148  '148'
             42_2  COME_FROM           144  '144'
             42_3  COME_FROM           128  '128'
             42_4  COME_FROM           100  '100'
             42_5  COME_FROM            72  '72'
               42  FOR_ITER            154  'to 154'
               44  STORE_FAST               'subkeyname'

 L. 257        46  SETUP_EXCEPT        130  'to 130'

 L. 258        48  LOAD_GLOBAL              _winreg
               50  LOAD_METHOD              OpenKey
               52  LOAD_FAST                'hkcr'
               54  LOAD_FAST                'subkeyname'
               56  CALL_METHOD_2         2  '2 positional arguments'
               58  SETUP_WITH          120  'to 120'
               60  STORE_FAST               'subkey'

 L. 260        62  LOAD_FAST                'subkeyname'
               64  LOAD_METHOD              startswith
               66  LOAD_STR                 '.'
               68  CALL_METHOD_1         1  '1 positional argument'
               70  POP_JUMP_IF_TRUE     74  'to 74'

 L. 261        72  CONTINUE_LOOP        42  'to 42'
             74_0  COME_FROM            70  '70'

 L. 263        74  LOAD_GLOBAL              _winreg
               76  LOAD_METHOD              QueryValueEx

 L. 264        78  LOAD_FAST                'subkey'
               80  LOAD_STR                 'Content Type'
               82  CALL_METHOD_2         2  '2 positional arguments'
               84  UNPACK_SEQUENCE_2     2 
               86  STORE_FAST               'mimetype'
               88  STORE_FAST               'datatype'

 L. 265        90  LOAD_FAST                'datatype'
               92  LOAD_GLOBAL              _winreg
               94  LOAD_ATTR                REG_SZ
               96  COMPARE_OP               !=
               98  POP_JUMP_IF_FALSE   102  'to 102'

 L. 266       100  CONTINUE_LOOP        42  'to 42'
            102_0  COME_FROM            98  '98'

 L. 267       102  LOAD_FAST                'self'
              104  LOAD_METHOD              add_type
              106  LOAD_FAST                'mimetype'
              108  LOAD_FAST                'subkeyname'
              110  LOAD_FAST                'strict'
              112  CALL_METHOD_3         3  '3 positional arguments'
              114  POP_TOP          
              116  POP_BLOCK        
              118  LOAD_CONST               None
            120_0  COME_FROM_WITH       58  '58'
              120  WITH_CLEANUP_START
              122  WITH_CLEANUP_FINISH
              124  END_FINALLY      
              126  POP_BLOCK        
              128  JUMP_BACK            42  'to 42'
            130_0  COME_FROM_EXCEPT     46  '46'

 L. 268       130  DUP_TOP          
              132  LOAD_GLOBAL              OSError
              134  COMPARE_OP               exception-match
              136  POP_JUMP_IF_FALSE   150  'to 150'
              138  POP_TOP          
              140  POP_TOP          
              142  POP_TOP          

 L. 269       144  CONTINUE_LOOP        42  'to 42'
              146  POP_EXCEPT       
              148  JUMP_BACK            42  'to 42'
            150_0  COME_FROM           136  '136'
              150  END_FINALLY      
              152  JUMP_BACK            42  'to 42'
              154  POP_BLOCK        
            156_0  COME_FROM_LOOP       32  '32'
              156  POP_BLOCK        
              158  LOAD_CONST               None
            160_0  COME_FROM_WITH       28  '28'
              160  WITH_CLEANUP_START
              162  WITH_CLEANUP_FINISH
              164  END_FINALLY      

Parse error at or near `CONTINUE_LOOP' instruction at offset 72


def guess_type(url, strict=True):
    """Guess the type of a file based on its URL.

    Return value is a tuple (type, encoding) where type is None if the
    type can't be guessed (no or unknown suffix) or a string of the
    form type/subtype, usable for a MIME Content-type header; and
    encoding is None for no encoding or the name of the program used
    to encode (e.g. compress or gzip).  The mappings are table
    driven.  Encoding suffixes are case sensitive; type suffixes are
    first tried case sensitive, then case insensitive.

    The suffixes .tgz, .taz and .tz (case sensitive!) are all mapped
    to ".tar.gz".  (This is table-driven too, using the dictionary
    suffix_map).

    Optional `strict' argument when false adds a bunch of commonly found, but
    non-standard types.
    """
    global _db
    if _db is None:
        init()
    return _db.guess_type(url, strict)


def guess_all_extensions(type, strict=True):
    """Guess the extensions for a file based on its MIME type.

    Return value is a list of strings giving the possible filename
    extensions, including the leading dot ('.').  The extension is not
    guaranteed to have been associated with any particular data
    stream, but would be mapped to the MIME type `type' by
    guess_type().  If no extension can be guessed for `type', None
    is returned.

    Optional `strict' argument when false adds a bunch of commonly found,
    but non-standard types.
    """
    if _db is None:
        init()
    return _db.guess_all_extensions(type, strict)


def guess_extension(type, strict=True):
    """Guess the extension for a file based on its MIME type.

    Return value is a string giving a filename extension, including the
    leading dot ('.').  The extension is not guaranteed to have been
    associated with any particular data stream, but would be mapped to the
    MIME type `type' by guess_type().  If no extension can be guessed for
    `type', None is returned.

    Optional `strict' argument when false adds a bunch of commonly found,
    but non-standard types.
    """
    if _db is None:
        init()
    return _db.guess_extension(type, strict)


def add_type(type, ext, strict=True):
    """Add a mapping between a type and an extension.

    When the extension is already known, the new
    type will replace the old one. When the type
    is already known the extension will be added
    to the list of known extensions.

    If strict is true, information will be added to
    list of standard types, else to the list of non-standard
    types.
    """
    if _db is None:
        init()
    return _db.add_type(type, ext, strict)


def init(files=None):
    global _db
    global common_types
    global encodings_map
    global inited
    global suffix_map
    global types_map
    inited = True
    db = MimeTypes()
    if files is None:
        if _winreg:
            db.read_windows_registry()
        files = knownfiles
    for file in files:
        if os.path.isfile(file):
            db.read(file)

    encodings_map = db.encodings_map
    suffix_map = db.suffix_map
    types_map = db.types_map[True]
    common_types = db.types_map[False]
    _db = db


def read_mime_types(file):
    try:
        f = open(file)
    except OSError:
        return
    else:
        with f:
            db = MimeTypes()
            db.readfp(f, True)
            return db.types_map[True]


def _default_mime_types():
    global common_types
    global encodings_map
    global suffix_map
    global types_map
    suffix_map = {'.svgz':'.svg.gz', 
     '.tgz':'.tar.gz', 
     '.taz':'.tar.gz', 
     '.tz':'.tar.gz', 
     '.tbz2':'.tar.bz2', 
     '.txz':'.tar.xz'}
    encodings_map = {'.gz':'gzip', 
     '.Z':'compress', 
     '.bz2':'bzip2', 
     '.xz':'xz'}
    types_map = {'.a':'application/octet-stream', 
     '.ai':'application/postscript', 
     '.aif':'audio/x-aiff', 
     '.aifc':'audio/x-aiff', 
     '.aiff':'audio/x-aiff', 
     '.au':'audio/basic', 
     '.avi':'video/x-msvideo', 
     '.bat':'text/plain', 
     '.bcpio':'application/x-bcpio', 
     '.bin':'application/octet-stream', 
     '.bmp':'image/bmp', 
     '.c':'text/plain', 
     '.cdf':'application/x-netcdf', 
     '.cpio':'application/x-cpio', 
     '.csh':'application/x-csh', 
     '.css':'text/css', 
     '.csv':'text/csv', 
     '.dll':'application/octet-stream', 
     '.doc':'application/msword', 
     '.dot':'application/msword', 
     '.dvi':'application/x-dvi', 
     '.eml':'message/rfc822', 
     '.eps':'application/postscript', 
     '.etx':'text/x-setext', 
     '.exe':'application/octet-stream', 
     '.gif':'image/gif', 
     '.gtar':'application/x-gtar', 
     '.h':'text/plain', 
     '.hdf':'application/x-hdf', 
     '.htm':'text/html', 
     '.html':'text/html', 
     '.ico':'image/vnd.microsoft.icon', 
     '.ief':'image/ief', 
     '.jpe':'image/jpeg', 
     '.jpeg':'image/jpeg', 
     '.jpg':'image/jpeg', 
     '.js':'application/javascript', 
     '.json':'application/json', 
     '.ksh':'text/plain', 
     '.latex':'application/x-latex', 
     '.m1v':'video/mpeg', 
     '.m3u':'application/vnd.apple.mpegurl', 
     '.m3u8':'application/vnd.apple.mpegurl', 
     '.man':'application/x-troff-man', 
     '.me':'application/x-troff-me', 
     '.mht':'message/rfc822', 
     '.mhtml':'message/rfc822', 
     '.mif':'application/x-mif', 
     '.mov':'video/quicktime', 
     '.movie':'video/x-sgi-movie', 
     '.mp2':'audio/mpeg', 
     '.mp3':'audio/mpeg', 
     '.mp4':'video/mp4', 
     '.mpa':'video/mpeg', 
     '.mpe':'video/mpeg', 
     '.mpeg':'video/mpeg', 
     '.mpg':'video/mpeg', 
     '.ms':'application/x-troff-ms', 
     '.nc':'application/x-netcdf', 
     '.nws':'message/rfc822', 
     '.o':'application/octet-stream', 
     '.obj':'application/octet-stream', 
     '.oda':'application/oda', 
     '.p12':'application/x-pkcs12', 
     '.p7c':'application/pkcs7-mime', 
     '.pbm':'image/x-portable-bitmap', 
     '.pdf':'application/pdf', 
     '.pfx':'application/x-pkcs12', 
     '.pgm':'image/x-portable-graymap', 
     '.pl':'text/plain', 
     '.png':'image/png', 
     '.pnm':'image/x-portable-anymap', 
     '.pot':'application/vnd.ms-powerpoint', 
     '.ppa':'application/vnd.ms-powerpoint', 
     '.ppm':'image/x-portable-pixmap', 
     '.pps':'application/vnd.ms-powerpoint', 
     '.ppt':'application/vnd.ms-powerpoint', 
     '.ps':'application/postscript', 
     '.pwz':'application/vnd.ms-powerpoint', 
     '.py':'text/x-python', 
     '.pyc':'application/x-python-code', 
     '.pyo':'application/x-python-code', 
     '.qt':'video/quicktime', 
     '.ra':'audio/x-pn-realaudio', 
     '.ram':'application/x-pn-realaudio', 
     '.ras':'image/x-cmu-raster', 
     '.rdf':'application/xml', 
     '.rgb':'image/x-rgb', 
     '.roff':'application/x-troff', 
     '.rtx':'text/richtext', 
     '.sgm':'text/x-sgml', 
     '.sgml':'text/x-sgml', 
     '.sh':'application/x-sh', 
     '.shar':'application/x-shar', 
     '.snd':'audio/basic', 
     '.so':'application/octet-stream', 
     '.src':'application/x-wais-source', 
     '.sv4cpio':'application/x-sv4cpio', 
     '.sv4crc':'application/x-sv4crc', 
     '.svg':'image/svg+xml', 
     '.swf':'application/x-shockwave-flash', 
     '.t':'application/x-troff', 
     '.tar':'application/x-tar', 
     '.tcl':'application/x-tcl', 
     '.tex':'application/x-tex', 
     '.texi':'application/x-texinfo', 
     '.texinfo':'application/x-texinfo', 
     '.tif':'image/tiff', 
     '.tiff':'image/tiff', 
     '.tr':'application/x-troff', 
     '.tsv':'text/tab-separated-values', 
     '.txt':'text/plain', 
     '.ustar':'application/x-ustar', 
     '.vcf':'text/x-vcard', 
     '.wav':'audio/x-wav', 
     '.webm':'video/webm', 
     '.wiz':'application/msword', 
     '.wsdl':'application/xml', 
     '.xbm':'image/x-xbitmap', 
     '.xlb':'application/vnd.ms-excel', 
     '.xls':'application/vnd.ms-excel', 
     '.xml':'text/xml', 
     '.xpdl':'application/xml', 
     '.xpm':'image/x-xpixmap', 
     '.xsl':'application/xml', 
     '.xwd':'image/x-xwindowdump', 
     '.zip':'application/zip'}
    common_types = {'.jpg':'image/jpg', 
     '.mid':'audio/midi', 
     '.midi':'audio/midi', 
     '.pct':'image/pict', 
     '.pic':'image/pict', 
     '.pict':'image/pict', 
     '.rtf':'application/rtf', 
     '.xul':'text/xul'}


_default_mime_types()
if __name__ == '__main__':
    import getopt
    USAGE = 'Usage: mimetypes.py [options] type\n\nOptions:\n    --help / -h       -- print this message and exit\n    --lenient / -l    -- additionally search of some common, but non-standard\n                         types.\n    --extension / -e  -- guess extension instead of type\n\nMore than one type argument may be given.\n'

    def usage(code, msg=''):
        print(USAGE)
        if msg:
            print(msg)
        sys.exit(code)


    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hle', [
         'help', 'lenient', 'extension'])
    except getopt.error as msg:
        try:
            usage(1, msg)
        finally:
            msg = None
            del msg

    strict = 1
    extension = 0
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage(0)
        else:
            if opt in ('-l', '--lenient'):
                strict = 0
        if opt in ('-e', '--extension'):
            extension = 1

    for gtype in args:
        if extension:
            guess = guess_extension(gtype, strict)
            if not guess:
                print("I don't know anything about type", gtype)
            else:
                print(guess)
        else:
            guess, encoding = guess_type(gtype, strict)
            if not guess:
                print("I don't know anything about type", gtype)
            else:
                print('type:', guess, 'encoding:', encoding)