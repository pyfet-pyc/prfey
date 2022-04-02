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


def unpack_tarfile--- This code section failed: ---

 L. 135         0  SETUP_FINALLY        16  'to 16'

 L. 136         2  LOAD_GLOBAL              tarfile
                4  LOAD_METHOD              open
                6  LOAD_FAST                'filename'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'tarobj'
               12  POP_BLOCK        
               14  JUMP_FORWARD         52  'to 52'
             16_0  COME_FROM_FINALLY     0  '0'

 L. 137        16  DUP_TOP          
               18  LOAD_GLOBAL              tarfile
               20  LOAD_ATTR                TarError
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    50  'to 50'
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 138        32  LOAD_GLOBAL              UnrecognizedFormat

 L. 139        34  LOAD_STR                 '%s is not a compressed or uncompressed tar file'
               36  LOAD_FAST                'filename'
               38  BUILD_TUPLE_1         1 
               40  BINARY_MODULO    

 L. 138        42  CALL_FUNCTION_1       1  ''
               44  RAISE_VARARGS_1       1  'exception instance'
               46  POP_EXCEPT       
               48  JUMP_FORWARD         52  'to 52'
             50_0  COME_FROM            24  '24'
               50  END_FINALLY      
             52_0  COME_FROM            48  '48'
             52_1  COME_FROM            14  '14'

 L. 141        52  LOAD_GLOBAL              contextlib
               54  LOAD_METHOD              closing
               56  LOAD_FAST                'tarobj'
               58  CALL_METHOD_1         1  ''
            60_62  SETUP_WITH          348  'to 348'
               64  POP_TOP          

 L. 143        66  LOAD_LAMBDA              '<code_object <lambda>>'
               68  LOAD_STR                 'unpack_tarfile.<locals>.<lambda>'
               70  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               72  LOAD_FAST                'tarobj'
               74  STORE_ATTR               chown

 L. 144        76  LOAD_FAST                'tarobj'
               78  GET_ITER         
             80_0  COME_FROM           332  '332'
             80_1  COME_FROM           328  '328'
             80_2  COME_FROM           306  '306'
             80_3  COME_FROM           262  '262'
             80_4  COME_FROM           248  '248'
             80_5  COME_FROM           230  '230'
             80_6  COME_FROM           114  '114'
             80_7  COME_FROM           100  '100'
            80_82  FOR_ITER            334  'to 334'
               84  STORE_FAST               'member'

 L. 145        86  LOAD_FAST                'member'
               88  LOAD_ATTR                name
               90  STORE_FAST               'name'

 L. 147        92  LOAD_FAST                'name'
               94  LOAD_METHOD              startswith
               96  LOAD_STR                 '/'
               98  CALL_METHOD_1         1  ''
              100  POP_JUMP_IF_TRUE_BACK    80  'to 80'
              102  LOAD_STR                 '..'
              104  LOAD_FAST                'name'
              106  LOAD_METHOD              split
              108  LOAD_STR                 '/'
              110  CALL_METHOD_1         1  ''
              112  COMPARE_OP               not-in
              114  POP_JUMP_IF_FALSE_BACK    80  'to 80'

 L. 148       116  LOAD_GLOBAL              os
              118  LOAD_ATTR                path
              120  LOAD_ATTR                join
              122  LOAD_FAST                'extract_dir'
              124  BUILD_TUPLE_1         1 
              126  LOAD_FAST                'name'
              128  LOAD_METHOD              split
              130  LOAD_STR                 '/'
              132  CALL_METHOD_1         1  ''
              134  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
              136  CALL_FUNCTION_EX      0  'positional arguments only'
              138  STORE_FAST               'prelim_dst'
            140_0  COME_FROM           222  '222'

 L. 152       140  LOAD_FAST                'member'
              142  LOAD_CONST               None
              144  COMPARE_OP               is-not
              146  POP_JUMP_IF_FALSE   224  'to 224'

 L. 153       148  LOAD_FAST                'member'
              150  LOAD_METHOD              islnk
              152  CALL_METHOD_0         0  ''

 L. 152       154  POP_JUMP_IF_TRUE    164  'to 164'

 L. 153       156  LOAD_FAST                'member'
              158  LOAD_METHOD              issym
              160  CALL_METHOD_0         0  ''

 L. 152       162  POP_JUMP_IF_FALSE   224  'to 224'
            164_0  COME_FROM           154  '154'

 L. 154       164  LOAD_FAST                'member'
              166  LOAD_ATTR                linkname
              168  STORE_FAST               'linkpath'

 L. 155       170  LOAD_FAST                'member'
              172  LOAD_METHOD              issym
              174  CALL_METHOD_0         0  ''
              176  POP_JUMP_IF_FALSE   212  'to 212'

 L. 156       178  LOAD_GLOBAL              posixpath
              180  LOAD_METHOD              dirname
              182  LOAD_FAST                'member'
              184  LOAD_ATTR                name
              186  CALL_METHOD_1         1  ''
              188  STORE_FAST               'base'

 L. 157       190  LOAD_GLOBAL              posixpath
              192  LOAD_METHOD              join
              194  LOAD_FAST                'base'
              196  LOAD_FAST                'linkpath'
              198  CALL_METHOD_2         2  ''
              200  STORE_FAST               'linkpath'

 L. 158       202  LOAD_GLOBAL              posixpath
              204  LOAD_METHOD              normpath
              206  LOAD_FAST                'linkpath'
              208  CALL_METHOD_1         1  ''
              210  STORE_FAST               'linkpath'
            212_0  COME_FROM           176  '176'

 L. 159       212  LOAD_FAST                'tarobj'
              214  LOAD_METHOD              _getmember
              216  LOAD_FAST                'linkpath'
              218  CALL_METHOD_1         1  ''
              220  STORE_FAST               'member'
              222  JUMP_BACK           140  'to 140'
            224_0  COME_FROM           162  '162'
            224_1  COME_FROM           146  '146'

 L. 161       224  LOAD_FAST                'member'
              226  LOAD_CONST               None
              228  COMPARE_OP               is-not
              230  POP_JUMP_IF_FALSE_BACK    80  'to 80'
              232  LOAD_FAST                'member'
              234  LOAD_METHOD              isfile
              236  CALL_METHOD_0         0  ''
          238_240  POP_JUMP_IF_TRUE    250  'to 250'
              242  LOAD_FAST                'member'
              244  LOAD_METHOD              isdir
              246  CALL_METHOD_0         0  ''
              248  POP_JUMP_IF_FALSE_BACK    80  'to 80'
            250_0  COME_FROM           238  '238'

 L. 162       250  LOAD_FAST                'progress_filter'
              252  LOAD_FAST                'name'
              254  LOAD_FAST                'prelim_dst'
              256  CALL_FUNCTION_2       2  ''
              258  STORE_FAST               'final_dst'

 L. 163       260  LOAD_FAST                'final_dst'
              262  POP_JUMP_IF_FALSE_BACK    80  'to 80'

 L. 164       264  LOAD_FAST                'final_dst'
              266  LOAD_METHOD              endswith
              268  LOAD_GLOBAL              os
              270  LOAD_ATTR                sep
              272  CALL_METHOD_1         1  ''
          274_276  POP_JUMP_IF_FALSE   290  'to 290'

 L. 165       278  LOAD_FAST                'final_dst'
              280  LOAD_CONST               None
              282  LOAD_CONST               -1
              284  BUILD_SLICE_2         2 
              286  BINARY_SUBSCR    
              288  STORE_FAST               'final_dst'
            290_0  COME_FROM           274  '274'

 L. 166       290  SETUP_FINALLY       308  'to 308'

 L. 168       292  LOAD_FAST                'tarobj'
              294  LOAD_METHOD              _extract_member
              296  LOAD_FAST                'member'
              298  LOAD_FAST                'final_dst'
              300  CALL_METHOD_2         2  ''
              302  POP_TOP          
              304  POP_BLOCK        
              306  JUMP_BACK            80  'to 80'
            308_0  COME_FROM_FINALLY   290  '290'

 L. 169       308  DUP_TOP          
              310  LOAD_GLOBAL              tarfile
              312  LOAD_ATTR                ExtractError
              314  COMPARE_OP               exception-match
          316_318  POP_JUMP_IF_FALSE   330  'to 330'
              320  POP_TOP          
              322  POP_TOP          
              324  POP_TOP          

 L. 171       326  POP_EXCEPT       
              328  JUMP_BACK            80  'to 80'
            330_0  COME_FROM           316  '316'
              330  END_FINALLY      
              332  JUMP_BACK            80  'to 80'
            334_0  COME_FROM            80  '80'

 L. 172       334  POP_BLOCK        
              336  BEGIN_FINALLY    
              338  WITH_CLEANUP_START
              340  WITH_CLEANUP_FINISH
              342  POP_FINALLY           0  ''
              344  LOAD_CONST               True
              346  RETURN_VALUE     
            348_0  COME_FROM_WITH       60  '60'
              348  WITH_CLEANUP_START
              350  WITH_CLEANUP_FINISH
              352  END_FINALLY      

Parse error at or near `WITH_CLEANUP_START' instruction at offset 338


extraction_drivers = (
 unpack_directory, unpack_zipfile, unpack_tarfile)