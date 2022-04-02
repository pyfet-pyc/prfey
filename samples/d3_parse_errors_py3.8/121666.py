# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
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
else:
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
            self.encodings_map = _encodings_map_default.copy()
            self.suffix_map = _suffix_map_default.copy()
            self.types_map = ({}, {})
            self.types_map_inv = ({}, {})
            for ext, type in _types_map_default.items():
                self.add_type(type, ext, True)
            else:
                for ext, type in _common_types_default.items():
                    self.add_type(type, ext, False)
                else:
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
            """Guess the type of a file which is either a URL or a path-like object.

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
            url = os.fspath(url)
            scheme, url = urllib.parse._splittype(url)
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
            while True:
                if ext in self.suffix_map:
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
            for ext in strict or self.types_map_inv[False].get(type, []):
                if ext not in extensions:
                    extensions.append(ext)
            else:
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
            while True:
                line = fp.readline()
                if not line:
                    pass
                else:
                    words = line.split()
                    for i in range(len(words)):
                        if words[i][0] == '#':
                            del words[i:]
                            break
                    else:
                        if not words:
                            pass
                        else:
                            type, suffixes = words[0], words[1:]
                        for suff in suffixes:
                            self.add_type(type, '.' + suff, strict)

        def read_windows_registry--- This code section failed: ---

 L. 241         0  LOAD_GLOBAL              _winreg
                2  POP_JUMP_IF_TRUE      8  'to 8'

 L. 242         4  LOAD_CONST               None
                6  RETURN_VALUE     
              8_0  COME_FROM             2  '2'

 L. 244         8  LOAD_CODE                <code_object enum_types>
               10  LOAD_STR                 'MimeTypes.read_windows_registry.<locals>.enum_types'
               12  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               14  STORE_FAST               'enum_types'

 L. 256        16  LOAD_GLOBAL              _winreg
               18  LOAD_METHOD              OpenKey
               20  LOAD_GLOBAL              _winreg
               22  LOAD_ATTR                HKEY_CLASSES_ROOT
               24  LOAD_STR                 ''
               26  CALL_METHOD_2         2  ''
               28  SETUP_WITH          182  'to 182'
               30  STORE_FAST               'hkcr'

 L. 257        32  LOAD_FAST                'enum_types'
               34  LOAD_FAST                'hkcr'
               36  CALL_FUNCTION_1       1  ''
               38  GET_ITER         
             40_0  COME_FROM           176  '176'
             40_1  COME_FROM           172  '172'
             40_2  COME_FROM           168  '168'
             40_3  COME_FROM           150  '150'
             40_4  COME_FROM           122  '122'
             40_5  COME_FROM            82  '82'
               40  FOR_ITER            178  'to 178'
               42  STORE_FAST               'subkeyname'

 L. 258        44  SETUP_FINALLY       152  'to 152'

 L. 259        46  LOAD_GLOBAL              _winreg
               48  LOAD_METHOD              OpenKey
               50  LOAD_FAST                'hkcr'
               52  LOAD_FAST                'subkeyname'
               54  CALL_METHOD_2         2  ''
               56  SETUP_WITH          142  'to 142'
               58  STORE_FAST               'subkey'

 L. 261        60  LOAD_FAST                'subkeyname'
               62  LOAD_METHOD              startswith
               64  LOAD_STR                 '.'
               66  CALL_METHOD_1         1  ''
               68  POP_JUMP_IF_TRUE     84  'to 84'

 L. 262        70  POP_BLOCK        
               72  BEGIN_FINALLY    
               74  WITH_CLEANUP_START
               76  WITH_CLEANUP_FINISH
               78  POP_FINALLY           0  ''
               80  POP_BLOCK        
               82  JUMP_BACK            40  'to 40'
             84_0  COME_FROM            68  '68'

 L. 264        84  LOAD_GLOBAL              _winreg
               86  LOAD_METHOD              QueryValueEx

 L. 265        88  LOAD_FAST                'subkey'

 L. 265        90  LOAD_STR                 'Content Type'

 L. 264        92  CALL_METHOD_2         2  ''
               94  UNPACK_SEQUENCE_2     2 
               96  STORE_FAST               'mimetype'
               98  STORE_FAST               'datatype'

 L. 266       100  LOAD_FAST                'datatype'
              102  LOAD_GLOBAL              _winreg
              104  LOAD_ATTR                REG_SZ
              106  COMPARE_OP               !=
              108  POP_JUMP_IF_FALSE   124  'to 124'

 L. 267       110  POP_BLOCK        
              112  BEGIN_FINALLY    
              114  WITH_CLEANUP_START
              116  WITH_CLEANUP_FINISH
              118  POP_FINALLY           0  ''
              120  POP_BLOCK        
              122  JUMP_BACK            40  'to 40'
            124_0  COME_FROM           108  '108'

 L. 268       124  LOAD_FAST                'self'
              126  LOAD_METHOD              add_type
              128  LOAD_FAST                'mimetype'
              130  LOAD_FAST                'subkeyname'
              132  LOAD_FAST                'strict'
              134  CALL_METHOD_3         3  ''
              136  POP_TOP          
              138  POP_BLOCK        
              140  BEGIN_FINALLY    
            142_0  COME_FROM_WITH       56  '56'
              142  WITH_CLEANUP_START
              144  WITH_CLEANUP_FINISH
              146  END_FINALLY      
              148  POP_BLOCK        
              150  JUMP_BACK            40  'to 40'
            152_0  COME_FROM_FINALLY    44  '44'

 L. 269       152  DUP_TOP          
              154  LOAD_GLOBAL              OSError
              156  COMPARE_OP               exception-match
              158  POP_JUMP_IF_FALSE   174  'to 174'
              160  POP_TOP          
              162  POP_TOP          
              164  POP_TOP          

 L. 270       166  POP_EXCEPT       
              168  JUMP_BACK            40  'to 40'
              170  POP_EXCEPT       
              172  JUMP_BACK            40  'to 40'
            174_0  COME_FROM           158  '158'
              174  END_FINALLY      
              176  JUMP_BACK            40  'to 40'
            178_0  COME_FROM            40  '40'
              178  POP_BLOCK        
              180  BEGIN_FINALLY    
            182_0  COME_FROM_WITH       28  '28'
              182  WITH_CLEANUP_START
              184  WITH_CLEANUP_FINISH
              186  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 72


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
        if files is None or _db is None:
            db = MimeTypes()
            if _winreg:
                db.read_windows_registry()
            if files is None:
                files = knownfiles
            else:
                files = knownfiles + list(files)
        else:
            db = _db
        for file in files:
            if os.path.isfile(file):
                db.read(file)
        else:
            encodings_map = db.encodings_map
            suffix_map = db.suffix_map
            types_map = db.types_map[True]
            common_types = db.types_map[False]
            _db = db


    def read_mime_types(file):
        try:
            f = open(file, encoding='utf-8')
        except OSError:
            return
        else:
            with f:
                db = MimeTypes()
                db.readfp(f, True)
                return db.types_map[True]


    def _default_mime_types():
        global _common_types_default
        global _encodings_map_default
        global _suffix_map_default
        global _types_map_default
        global common_types
        global encodings_map
        global suffix_map
        global types_map
        suffix_map = _suffix_map_default = {'.svgz':'.svg.gz', 
         '.tgz':'.tar.gz', 
         '.taz':'.tar.gz', 
         '.tz':'.tar.gz', 
         '.tbz2':'.tar.bz2', 
         '.txz':'.tar.xz'}
        encodings_map = _encodings_map_default = {'.gz':'gzip', 
         '.Z':'compress', 
         '.bz2':'bzip2', 
         '.xz':'xz'}
        types_map = _types_map_default = {'.js':'application/javascript', 
         '.mjs':'application/javascript', 
         '.json':'application/json', 
         '.webmanifest':'application/manifest+json', 
         '.doc':'application/msword', 
         '.dot':'application/msword', 
         '.wiz':'application/msword', 
         '.bin':'application/octet-stream', 
         '.a':'application/octet-stream', 
         '.dll':'application/octet-stream', 
         '.exe':'application/octet-stream', 
         '.o':'application/octet-stream', 
         '.obj':'application/octet-stream', 
         '.so':'application/octet-stream', 
         '.oda':'application/oda', 
         '.pdf':'application/pdf', 
         '.p7c':'application/pkcs7-mime', 
         '.ps':'application/postscript', 
         '.ai':'application/postscript', 
         '.eps':'application/postscript', 
         '.m3u':'application/vnd.apple.mpegurl', 
         '.m3u8':'application/vnd.apple.mpegurl', 
         '.xls':'application/vnd.ms-excel', 
         '.xlb':'application/vnd.ms-excel', 
         '.ppt':'application/vnd.ms-powerpoint', 
         '.pot':'application/vnd.ms-powerpoint', 
         '.ppa':'application/vnd.ms-powerpoint', 
         '.pps':'application/vnd.ms-powerpoint', 
         '.pwz':'application/vnd.ms-powerpoint', 
         '.wasm':'application/wasm', 
         '.bcpio':'application/x-bcpio', 
         '.cpio':'application/x-cpio', 
         '.csh':'application/x-csh', 
         '.dvi':'application/x-dvi', 
         '.gtar':'application/x-gtar', 
         '.hdf':'application/x-hdf', 
         '.h5':'application/x-hdf5', 
         '.latex':'application/x-latex', 
         '.mif':'application/x-mif', 
         '.cdf':'application/x-netcdf', 
         '.nc':'application/x-netcdf', 
         '.p12':'application/x-pkcs12', 
         '.pfx':'application/x-pkcs12', 
         '.ram':'application/x-pn-realaudio', 
         '.pyc':'application/x-python-code', 
         '.pyo':'application/x-python-code', 
         '.sh':'application/x-sh', 
         '.shar':'application/x-shar', 
         '.swf':'application/x-shockwave-flash', 
         '.sv4cpio':'application/x-sv4cpio', 
         '.sv4crc':'application/x-sv4crc', 
         '.tar':'application/x-tar', 
         '.tcl':'application/x-tcl', 
         '.tex':'application/x-tex', 
         '.texi':'application/x-texinfo', 
         '.texinfo':'application/x-texinfo', 
         '.roff':'application/x-troff', 
         '.t':'application/x-troff', 
         '.tr':'application/x-troff', 
         '.man':'application/x-troff-man', 
         '.me':'application/x-troff-me', 
         '.ms':'application/x-troff-ms', 
         '.ustar':'application/x-ustar', 
         '.src':'application/x-wais-source', 
         '.xsl':'application/xml', 
         '.rdf':'application/xml', 
         '.wsdl':'application/xml', 
         '.xpdl':'application/xml', 
         '.zip':'application/zip', 
         '.au':'audio/basic', 
         '.snd':'audio/basic', 
         '.mp3':'audio/mpeg', 
         '.mp2':'audio/mpeg', 
         '.aif':'audio/x-aiff', 
         '.aifc':'audio/x-aiff', 
         '.aiff':'audio/x-aiff', 
         '.ra':'audio/x-pn-realaudio', 
         '.wav':'audio/x-wav', 
         '.bmp':'image/bmp', 
         '.gif':'image/gif', 
         '.ief':'image/ief', 
         '.jpg':'image/jpeg', 
         '.jpe':'image/jpeg', 
         '.jpeg':'image/jpeg', 
         '.png':'image/png', 
         '.svg':'image/svg+xml', 
         '.tiff':'image/tiff', 
         '.tif':'image/tiff', 
         '.ico':'image/vnd.microsoft.icon', 
         '.ras':'image/x-cmu-raster', 
         '.bmp':'image/x-ms-bmp', 
         '.pnm':'image/x-portable-anymap', 
         '.pbm':'image/x-portable-bitmap', 
         '.pgm':'image/x-portable-graymap', 
         '.ppm':'image/x-portable-pixmap', 
         '.rgb':'image/x-rgb', 
         '.xbm':'image/x-xbitmap', 
         '.xpm':'image/x-xpixmap', 
         '.xwd':'image/x-xwindowdump', 
         '.eml':'message/rfc822', 
         '.mht':'message/rfc822', 
         '.mhtml':'message/rfc822', 
         '.nws':'message/rfc822', 
         '.css':'text/css', 
         '.csv':'text/csv', 
         '.html':'text/html', 
         '.htm':'text/html', 
         '.txt':'text/plain', 
         '.bat':'text/plain', 
         '.c':'text/plain', 
         '.h':'text/plain', 
         '.ksh':'text/plain', 
         '.pl':'text/plain', 
         '.rtx':'text/richtext', 
         '.tsv':'text/tab-separated-values', 
         '.py':'text/x-python', 
         '.etx':'text/x-setext', 
         '.sgm':'text/x-sgml', 
         '.sgml':'text/x-sgml', 
         '.vcf':'text/x-vcard', 
         '.xml':'text/xml', 
         '.mp4':'video/mp4', 
         '.mpeg':'video/mpeg', 
         '.m1v':'video/mpeg', 
         '.mpa':'video/mpeg', 
         '.mpe':'video/mpeg', 
         '.mpg':'video/mpeg', 
         '.mov':'video/quicktime', 
         '.qt':'video/quicktime', 
         '.webm':'video/webm', 
         '.avi':'video/x-msvideo', 
         '.movie':'video/x-sgi-movie'}
        common_types = _common_types_default = {'.rtf':'application/rtf', 
         '.midi':'audio/midi', 
         '.mid':'audio/midi', 
         '.jpg':'image/jpg', 
         '.pict':'image/pict', 
         '.pct':'image/pict', 
         '.pic':'image/pict', 
         '.xul':'text/xul'}


    _default_mime_types()

    def _main():
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

        else:
            strict = 1
            extension = 0
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                usage(0)
            else:
                if opt in ('-l', '--lenient'):
                    strict = 0
                else:
                    if opt in ('-e', '--extension'):
                        extension = 1
        else:
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


    if __name__ == '__main__':
        _main()