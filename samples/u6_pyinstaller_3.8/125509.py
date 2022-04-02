# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
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

 L.  59        62  LOAD_GLOBAL              UnrecognizedFormat

 L.  60        64  LOAD_STR                 'Not a recognized archive type: %s'
               66  LOAD_FAST                'filename'
               68  BINARY_MODULO    

 L.  59        70  CALL_FUNCTION_1       1  ''
               72  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `POP_EXCEPT' instruction at offset 48


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
    with zipfile.ZipFile(filename) as (z):
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
                        with open(target, 'wb') as (f):
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
               14  JUMP_FORWARD         68  'to 68'
             16_0  COME_FROM_FINALLY     0  '0'

 L. 137        16  DUP_TOP          
               18  LOAD_GLOBAL              tarfile
               20  LOAD_ATTR                TarError
               22  COMPARE_OP               exception-match
               24  POP_JUMP_IF_FALSE    66  'to 66'
               26  POP_TOP          
               28  STORE_FAST               'e'
               30  POP_TOP          
               32  SETUP_FINALLY        54  'to 54'

 L. 138        34  LOAD_GLOBAL              UnrecognizedFormat

 L. 139        36  LOAD_STR                 '%s is not a compressed or uncompressed tar file'
               38  LOAD_FAST                'filename'
               40  BUILD_TUPLE_1         1 
               42  BINARY_MODULO    

 L. 138        44  CALL_FUNCTION_1       1  ''

 L. 140        46  LOAD_FAST                'e'

 L. 138        48  RAISE_VARARGS_2       2  'exception instance with __cause__'
               50  POP_BLOCK        
               52  BEGIN_FINALLY    
             54_0  COME_FROM_FINALLY    32  '32'
               54  LOAD_CONST               None
               56  STORE_FAST               'e'
               58  DELETE_FAST              'e'
               60  END_FINALLY      
               62  POP_EXCEPT       
               64  JUMP_FORWARD         68  'to 68'
             66_0  COME_FROM            24  '24'
               66  END_FINALLY      
             68_0  COME_FROM            64  '64'
             68_1  COME_FROM            14  '14'

 L. 141        68  LOAD_GLOBAL              contextlib
               70  LOAD_METHOD              closing
               72  LOAD_FAST                'tarobj'
               74  CALL_METHOD_1         1  ''
            76_78  SETUP_WITH          364  'to 364'
               80  POP_TOP          

 L. 143        82  LOAD_LAMBDA              '<code_object <lambda>>'
               84  LOAD_STR                 'unpack_tarfile.<locals>.<lambda>'
               86  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               88  LOAD_FAST                'tarobj'
               90  STORE_ATTR               chown

 L. 144        92  LOAD_FAST                'tarobj'
               94  GET_ITER         
             96_0  COME_FROM           278  '278'
             96_1  COME_FROM           264  '264'
             96_2  COME_FROM           246  '246'
             96_3  COME_FROM           130  '130'
             96_4  COME_FROM           116  '116'
            96_98  FOR_ITER            350  'to 350'
              100  STORE_FAST               'member'

 L. 145       102  LOAD_FAST                'member'
              104  LOAD_ATTR                name
              106  STORE_FAST               'name'

 L. 147       108  LOAD_FAST                'name'
              110  LOAD_METHOD              startswith
              112  LOAD_STR                 '/'
              114  CALL_METHOD_1         1  ''
              116  POP_JUMP_IF_TRUE     96  'to 96'
              118  LOAD_STR                 '..'
              120  LOAD_FAST                'name'
              122  LOAD_METHOD              split
              124  LOAD_STR                 '/'
              126  CALL_METHOD_1         1  ''
              128  COMPARE_OP               not-in
              130  POP_JUMP_IF_FALSE    96  'to 96'

 L. 148       132  LOAD_GLOBAL              os
              134  LOAD_ATTR                path
              136  LOAD_ATTR                join
              138  LOAD_FAST                'extract_dir'
              140  BUILD_TUPLE_1         1 
              142  LOAD_FAST                'name'
              144  LOAD_METHOD              split
              146  LOAD_STR                 '/'
              148  CALL_METHOD_1         1  ''
              150  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
              152  CALL_FUNCTION_EX      0  'positional arguments only'
              154  STORE_FAST               'prelim_dst'

 L. 152       156  LOAD_FAST                'member'
              158  LOAD_CONST               None
              160  COMPARE_OP               is-not
              162  POP_JUMP_IF_FALSE   240  'to 240'

 L. 153       164  LOAD_FAST                'member'
              166  LOAD_METHOD              islnk
              168  CALL_METHOD_0         0  ''

 L. 152       170  POP_JUMP_IF_TRUE    180  'to 180'

 L. 153       172  LOAD_FAST                'member'
              174  LOAD_METHOD              issym
              176  CALL_METHOD_0         0  ''

 L. 152       178  POP_JUMP_IF_FALSE   240  'to 240'
            180_0  COME_FROM           170  '170'

 L. 154       180  LOAD_FAST                'member'
              182  LOAD_ATTR                linkname
              184  STORE_FAST               'linkpath'

 L. 155       186  LOAD_FAST                'member'
              188  LOAD_METHOD              issym
              190  CALL_METHOD_0         0  ''
              192  POP_JUMP_IF_FALSE   228  'to 228'

 L. 156       194  LOAD_GLOBAL              posixpath
              196  LOAD_METHOD              dirname
              198  LOAD_FAST                'member'
              200  LOAD_ATTR                name
              202  CALL_METHOD_1         1  ''
              204  STORE_FAST               'base'

 L. 157       206  LOAD_GLOBAL              posixpath
              208  LOAD_METHOD              join
              210  LOAD_FAST                'base'
              212  LOAD_FAST                'linkpath'
              214  CALL_METHOD_2         2  ''
              216  STORE_FAST               'linkpath'

 L. 158       218  LOAD_GLOBAL              posixpath
              220  LOAD_METHOD              normpath
              222  LOAD_FAST                'linkpath'
              224  CALL_METHOD_1         1  ''
              226  STORE_FAST               'linkpath'
            228_0  COME_FROM           192  '192'

 L. 159       228  LOAD_FAST                'tarobj'
              230  LOAD_METHOD              _getmember
              232  LOAD_FAST                'linkpath'
              234  CALL_METHOD_1         1  ''
              236  STORE_FAST               'member'
              238  JUMP_BACK           156  'to 156'
            240_0  COME_FROM           178  '178'
            240_1  COME_FROM           162  '162'

 L. 161       240  LOAD_FAST                'member'
              242  LOAD_CONST               None
              244  COMPARE_OP               is-not
              246  POP_JUMP_IF_FALSE    96  'to 96'
              248  LOAD_FAST                'member'
              250  LOAD_METHOD              isfile
              252  CALL_METHOD_0         0  ''
          254_256  POP_JUMP_IF_TRUE    266  'to 266'
              258  LOAD_FAST                'member'
              260  LOAD_METHOD              isdir
              262  CALL_METHOD_0         0  ''
              264  POP_JUMP_IF_FALSE    96  'to 96'
            266_0  COME_FROM           254  '254'

 L. 162       266  LOAD_FAST                'progress_filter'
              268  LOAD_FAST                'name'
              270  LOAD_FAST                'prelim_dst'
              272  CALL_FUNCTION_2       2  ''
              274  STORE_FAST               'final_dst'

 L. 163       276  LOAD_FAST                'final_dst'
              278  POP_JUMP_IF_FALSE    96  'to 96'

 L. 164       280  LOAD_FAST                'final_dst'
              282  LOAD_METHOD              endswith
              284  LOAD_GLOBAL              os
              286  LOAD_ATTR                sep
              288  CALL_METHOD_1         1  ''
          290_292  POP_JUMP_IF_FALSE   306  'to 306'

 L. 165       294  LOAD_FAST                'final_dst'
              296  LOAD_CONST               None
              298  LOAD_CONST               -1
              300  BUILD_SLICE_2         2 
              302  BINARY_SUBSCR    
              304  STORE_FAST               'final_dst'
            306_0  COME_FROM           290  '290'

 L. 166       306  SETUP_FINALLY       324  'to 324'

 L. 168       308  LOAD_FAST                'tarobj'
              310  LOAD_METHOD              _extract_member
              312  LOAD_FAST                'member'
              314  LOAD_FAST                'final_dst'
              316  CALL_METHOD_2         2  ''
              318  POP_TOP          
              320  POP_BLOCK        
              322  JUMP_BACK            96  'to 96'
            324_0  COME_FROM_FINALLY   306  '306'

 L. 169       324  DUP_TOP          
              326  LOAD_GLOBAL              tarfile
              328  LOAD_ATTR                ExtractError
              330  COMPARE_OP               exception-match
          332_334  POP_JUMP_IF_FALSE   346  'to 346'
              336  POP_TOP          
              338  POP_TOP          
              340  POP_TOP          

 L. 171       342  POP_EXCEPT       
              344  JUMP_BACK            96  'to 96'
            346_0  COME_FROM           332  '332'
              346  END_FINALLY      
              348  JUMP_BACK            96  'to 96'

 L. 172       350  POP_BLOCK        
              352  BEGIN_FINALLY    
              354  WITH_CLEANUP_START
              356  WITH_CLEANUP_FINISH
              358  POP_FINALLY           0  ''
              360  LOAD_CONST               True
              362  RETURN_VALUE     
            364_0  COME_FROM_WITH       76  '76'
              364  WITH_CLEANUP_START
              366  WITH_CLEANUP_FINISH
              368  END_FINALLY      

Parse error at or near `WITH_CLEANUP_START' instruction at offset 354


extraction_drivers = (
 unpack_directory, unpack_zipfile, unpack_tarfile)