# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: setuptools\archive_util.py
"""Utilities for extracting common archive formats"""
import zipfile, tarfile, os, shutil, posixpath, contextlib
from distutils.errors import DistutilsError
from pkg_resources import ensure_directory
__all__ = [
 'unpack_archive', 'unpack_zipfile', 'unpack_tarfile', 'default_filter',
 'UnrecognizedFormat', 'extraction_drivers', 'unpack_directory']

class UnrecognizedFormat(DistutilsError):
    __doc__ = "Couldn't recognize the archive type"


def default_filter(src, dst):
    """The default progress/filter callback; returns True for all files"""
    return dst


def unpack_archive--- This code section failed: ---

 L.  51         0  LOAD_FAST                'drivers'
                2  JUMP_IF_TRUE_OR_POP     6  'to 6'
                4  LOAD_GLOBAL              extraction_drivers
              6_0  COME_FROM             2  '2'
                6  GET_ITER         
              8_0  COME_FROM            60  '60'
              8_1  COME_FROM            50  '50'
              8_2  COME_FROM            46  '46'
                8  FOR_ITER             62  'to 62'
               10  STORE_FAST               'driver'

 L.  52        12  SETUP_FINALLY        30  'to 30'

 L.  53        14  LOAD_FAST                'driver'
               16  LOAD_FAST                'filename'
               18  LOAD_FAST                'extract_dir'
               20  LOAD_FAST                'progress_filter'
               22  CALL_FUNCTION_3       3  ''
               24  POP_TOP          
               26  POP_BLOCK        
               28  JUMP_FORWARD         54  'to 54'
             30_0  COME_FROM_FINALLY    12  '12'

 L.  54        30  DUP_TOP          
               32  LOAD_GLOBAL              UnrecognizedFormat
               34  COMPARE_OP               exception-match
               36  POP_JUMP_IF_FALSE    52  'to 52'
               38  POP_TOP          
               40  POP_TOP          
               42  POP_TOP          

 L.  55        44  POP_EXCEPT       
               46  JUMP_BACK             8  'to 8'
               48  POP_EXCEPT       
               50  JUMP_BACK             8  'to 8'
             52_0  COME_FROM            36  '36'
               52  END_FINALLY      
             54_0  COME_FROM            28  '28'

 L.  57        54  POP_TOP          
               56  LOAD_CONST               None
               58  RETURN_VALUE     
               60  JUMP_BACK             8  'to 8'
             62_0  COME_FROM             8  '8'

 L.  59        62  LOAD_GLOBAL              UnrecognizedFormat

 L.  60        64  LOAD_STR                 'Not a recognized archive type: %s'
               66  LOAD_FAST                'filename'
               68  BINARY_MODULO    

 L.  59        70  CALL_FUNCTION_1       1  ''
               72  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `JUMP_BACK' instruction at offset 50


def unpack_directory(filename, extract_dir, progress_filter=default_filter):
    """"Unpack" a directory, using the same interface as for archives

    Raises ``UnrecognizedFormat`` if `filename` is not a directory
    """
    if not os.path.isdir(filename):
        raise UnrecognizedFormat('%s is not a directory' % filename)
    paths = {filename: ('', extract_dir)}
    for base, dirs, files in os.walk(filename):
        src, dst = paths[base]
        for d in dirs:
            paths[os.path.join(base, d)] = (
             src + d + '/', os.path.join(dst, d))

    else:
        for f in files:
            target = os.path.join(dst, f)
            target = progress_filter(src + f, target)
            if not target:
                pass
            else:
                ensure_directory(target)
                f = os.path.join(base, f)
                shutil.copyfile(f, target)
                shutil.copystat(f, target)


def unpack_zipfile(filename, extract_dir, progress_filter=default_filter):
    """Unpack zip `filename` to `extract_dir`

    Raises ``UnrecognizedFormat`` if `filename` is not a zipfile (as determined
    by ``zipfile.is_zipfile()``).  See ``unpack_archive()`` for an explanation
    of the `progress_filter` argument.
    """
    if not zipfile.is_zipfile(filename):
        raise UnrecognizedFormat('%s is not a zip file' % (filename,))
    with zipfile.ZipFile(filename) as z:
        for info in z.infolist():
            name = info.filename
            if not name.startswith('/'):
                if '..' in name.split('/'):
                    pass
                else:
                    target = (os.path.join)(extract_dir, *name.split('/'))
                    target = progress_filter(name, target)
            if not target:
                pass
            else:
                if name.endswith('/'):
                    ensure_directory(target)
                else:
                    ensure_directory(target)
                    data = z.read(info.filename)
                    with open(target, 'wb') as f:
                        f.write(data)
                unix_attributes = info.external_attr >> 16
                if unix_attributes:
                    os.chmod(target, unix_attributes)


def _resolve_tar_file_or_dir(tar_obj, tar_member_obj):
    """Resolve any links and extract link targets as normal files."""
    while True:
        if tar_member_obj is not None:
            if tar_member_obj.islnk() or (tar_member_obj.issym()):
                linkpath = tar_member_obj.linkname
                if tar_member_obj.issym():
                    base = posixpath.dirname(tar_member_obj.name)
                    linkpath = posixpath.join(base, linkpath)
                    linkpath = posixpath.normpath(linkpath)
            tar_member_obj = tar_obj._getmember(linkpath)

    is_file_or_dir = (tar_member_obj is not None) and ((tar_member_obj.isfile()) or (tar_member_obj.isdir()))
    if is_file_or_dir:
        return tar_member_obj
    raise LookupError('Got unknown file type')


def _iter_open_tar--- This code section failed: ---

 L. 152         0  LOAD_LAMBDA              '<code_object <lambda>>'
                2  LOAD_STR                 '_iter_open_tar.<locals>.<lambda>'
                4  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                6  LOAD_FAST                'tar_obj'
                8  STORE_ATTR               chown

 L. 154        10  LOAD_GLOBAL              contextlib
               12  LOAD_METHOD              closing
               14  LOAD_FAST                'tar_obj'
               16  CALL_METHOD_1         1  ''
               18  SETUP_WITH          182  'to 182'
               20  POP_TOP          

 L. 155        22  LOAD_FAST                'tar_obj'
               24  GET_ITER         
             26_0  COME_FROM           176  '176'
             26_1  COME_FROM           140  '140'
             26_2  COME_FROM           118  '118'
             26_3  COME_FROM            60  '60'
             26_4  COME_FROM            44  '44'
               26  FOR_ITER            178  'to 178'
               28  STORE_FAST               'member'

 L. 156        30  LOAD_FAST                'member'
               32  LOAD_ATTR                name
               34  STORE_FAST               'name'

 L. 158        36  LOAD_FAST                'name'
               38  LOAD_METHOD              startswith
               40  LOAD_STR                 '/'
               42  CALL_METHOD_1         1  ''
               44  POP_JUMP_IF_TRUE_BACK    26  'to 26'
               46  LOAD_STR                 '..'
               48  LOAD_FAST                'name'
               50  LOAD_METHOD              split
               52  LOAD_STR                 '/'
               54  CALL_METHOD_1         1  ''
               56  COMPARE_OP               in
               58  POP_JUMP_IF_FALSE    62  'to 62'

 L. 159        60  JUMP_BACK            26  'to 26'
             62_0  COME_FROM            58  '58'

 L. 161        62  LOAD_GLOBAL              os
               64  LOAD_ATTR                path
               66  LOAD_ATTR                join
               68  LOAD_FAST                'extract_dir'
               70  BUILD_TUPLE_1         1 
               72  LOAD_FAST                'name'
               74  LOAD_METHOD              split
               76  LOAD_STR                 '/'
               78  CALL_METHOD_1         1  ''
               80  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
               82  CALL_FUNCTION_EX      0  'positional arguments only'
               84  STORE_FAST               'prelim_dst'

 L. 163        86  SETUP_FINALLY       102  'to 102'

 L. 164        88  LOAD_GLOBAL              _resolve_tar_file_or_dir
               90  LOAD_FAST                'tar_obj'
               92  LOAD_FAST                'member'
               94  CALL_FUNCTION_2       2  ''
               96  STORE_FAST               'member'
               98  POP_BLOCK        
              100  JUMP_FORWARD        126  'to 126'
            102_0  COME_FROM_FINALLY    86  '86'

 L. 165       102  DUP_TOP          
              104  LOAD_GLOBAL              LookupError
              106  COMPARE_OP               exception-match
              108  POP_JUMP_IF_FALSE   124  'to 124'
              110  POP_TOP          
              112  POP_TOP          
              114  POP_TOP          

 L. 166       116  POP_EXCEPT       
              118  JUMP_BACK            26  'to 26'
              120  POP_EXCEPT       
              122  JUMP_FORWARD        126  'to 126'
            124_0  COME_FROM           108  '108'
              124  END_FINALLY      
            126_0  COME_FROM           122  '122'
            126_1  COME_FROM           100  '100'

 L. 168       126  LOAD_FAST                'progress_filter'
              128  LOAD_FAST                'name'
              130  LOAD_FAST                'prelim_dst'
              132  CALL_FUNCTION_2       2  ''
              134  STORE_FAST               'final_dst'

 L. 169       136  LOAD_FAST                'final_dst'
              138  POP_JUMP_IF_TRUE    142  'to 142'

 L. 170       140  JUMP_BACK            26  'to 26'
            142_0  COME_FROM           138  '138'

 L. 172       142  LOAD_FAST                'final_dst'
              144  LOAD_METHOD              endswith
              146  LOAD_GLOBAL              os
              148  LOAD_ATTR                sep
              150  CALL_METHOD_1         1  ''
              152  POP_JUMP_IF_FALSE   166  'to 166'

 L. 173       154  LOAD_FAST                'final_dst'
              156  LOAD_CONST               None
              158  LOAD_CONST               -1
              160  BUILD_SLICE_2         2 
              162  BINARY_SUBSCR    
              164  STORE_FAST               'final_dst'
            166_0  COME_FROM           152  '152'

 L. 175       166  LOAD_FAST                'member'
              168  LOAD_FAST                'final_dst'
              170  BUILD_TUPLE_2         2 
              172  YIELD_VALUE      
              174  POP_TOP          
              176  JUMP_BACK            26  'to 26'
            178_0  COME_FROM            26  '26'
              178  POP_BLOCK        
              180  BEGIN_FINALLY    
            182_0  COME_FROM_WITH       18  '18'
              182  WITH_CLEANUP_START
              184  WITH_CLEANUP_FINISH
              186  END_FINALLY      

Parse error at or near `COME_FROM' instruction at offset 124_0


def unpack_tarfile(filename, extract_dir, progress_filter=default_filter):
    """Unpack tar/tar.gz/tar.bz2 `filename` to `extract_dir`

    Raises ``UnrecognizedFormat`` if `filename` is not a tarfile (as determined
    by ``tarfile.open()``).  See ``unpack_archive()`` for an explanation
    of the `progress_filter` argument.
    """
    try:
        tarobj = tarfile.open(filename)
    except tarfile.TarError as e:
        try:
            raise UnrecognizedFormat('%s is not a compressed or uncompressed tar file' % (filename,)) from e
        finally:
            e = None
            del e

    else:
        for member, final_dst in _iter_open_tar(tarobj, extract_dir, progress_filter):
            try:
                tarobj._extract_member(member, final_dst)
            except tarfile.ExtractError:
                pass

        else:
            return True


extraction_drivers = (unpack_directory, unpack_zipfile, unpack_tarfile)