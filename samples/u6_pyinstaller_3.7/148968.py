# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: distutils\archive_util.py
"""distutils.archive_util

Utility functions for creating archive files (tarballs, zip files,
that sort of thing)."""
import os
from warnings import warn
import sys
try:
    import zipfile
except ImportError:
    zipfile = None

from distutils.errors import DistutilsExecError
import distutils.spawn as spawn
from distutils.dir_util import mkpath
from distutils import log
try:
    from pwd import getpwnam
except ImportError:
    getpwnam = None

try:
    from grp import getgrnam
except ImportError:
    getgrnam = None

def _get_gid(name):
    """Returns a gid, given a group name."""
    if getgrnam is None or name is None:
        return
    try:
        result = getgrnam(name)
    except KeyError:
        result = None

    if result is not None:
        return result[2]


def _get_uid(name):
    """Returns an uid, given a user name."""
    if getpwnam is None or name is None:
        return
    try:
        result = getpwnam(name)
    except KeyError:
        result = None

    if result is not None:
        return result[2]


def make_tarball(base_name, base_dir, compress='gzip', verbose=0, dry_run=0, owner=None, group=None):
    """Create a (possibly compressed) tar file from all the files under
    'base_dir'.

    'compress' must be "gzip" (the default), "bzip2", "xz", "compress", or
    None.  ("compress" will be deprecated in Python 3.2)

    'owner' and 'group' can be used to define an owner and a group for the
    archive that is being built. If not provided, the current owner and group
    will be used.

    The output tar file will be named 'base_dir' +  ".tar", possibly plus
    the appropriate compression extension (".gz", ".bz2", ".xz" or ".Z").

    Returns the output filename.
    """
    tar_compression = {'gzip':'gz', 
     'bzip2':'bz2',  'xz':'xz',  None:'',  'compress':''}
    compress_ext = {'gzip':'.gz',  'bzip2':'.bz2',  'xz':'.xz',  'compress':'.Z'}
    if compress is not None:
        if compress not in compress_ext.keys():
            raise ValueError("bad value for 'compress': must be None, 'gzip', 'bzip2', 'xz' or 'compress'")
    archive_name = base_name + '.tar'
    if compress != 'compress':
        archive_name += compress_ext.get(compress, '')
    mkpath((os.path.dirname(archive_name)), dry_run=dry_run)
    import tarfile
    log.info('Creating tar archive')
    uid = _get_uid(owner)
    gid = _get_gid(group)

    def _set_uid_gid(tarinfo):
        if gid is not None:
            tarinfo.gid = gid
            tarinfo.gname = group
        if uid is not None:
            tarinfo.uid = uid
            tarinfo.uname = owner
        return tarinfo

    if not dry_run:
        tar = tarfile.open(archive_name, 'w|%s' % tar_compression[compress])
        try:
            tar.add(base_dir, filter=_set_uid_gid)
        finally:
            tar.close()

    if compress == 'compress':
        warn("'compress' will be deprecated.", PendingDeprecationWarning)
        compressed_name = archive_name + compress_ext[compress]
        if sys.platform == 'win32':
            cmd = [
             compress, archive_name, compressed_name]
        else:
            cmd = [
             compress, '-f', archive_name]
        spawn(cmd, dry_run=dry_run)
        return compressed_name
    return archive_name


def make_zipfile--- This code section failed: ---

 L. 136         0  LOAD_FAST                'base_name'
                2  LOAD_STR                 '.zip'
                4  BINARY_ADD       
                6  STORE_FAST               'zip_filename'

 L. 137         8  LOAD_GLOBAL              mkpath
               10  LOAD_GLOBAL              os
               12  LOAD_ATTR                path
               14  LOAD_METHOD              dirname
               16  LOAD_FAST                'zip_filename'
               18  CALL_METHOD_1         1  '1 positional argument'
               20  LOAD_FAST                'dry_run'
               22  LOAD_CONST               ('dry_run',)
               24  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               26  POP_TOP          

 L. 141        28  LOAD_GLOBAL              zipfile
               30  LOAD_CONST               None
               32  COMPARE_OP               is
               34  POP_JUMP_IF_FALSE   112  'to 112'

 L. 142        36  LOAD_FAST                'verbose'
               38  POP_JUMP_IF_FALSE    46  'to 46'

 L. 143        40  LOAD_STR                 '-r'
               42  STORE_FAST               'zipoptions'
               44  JUMP_FORWARD         50  'to 50'
             46_0  COME_FROM            38  '38'

 L. 145        46  LOAD_STR                 '-rq'
               48  STORE_FAST               'zipoptions'
             50_0  COME_FROM            44  '44'

 L. 147        50  SETUP_EXCEPT         76  'to 76'

 L. 148        52  LOAD_GLOBAL              spawn
               54  LOAD_STR                 'zip'
               56  LOAD_FAST                'zipoptions'
               58  LOAD_FAST                'zip_filename'
               60  LOAD_FAST                'base_dir'
               62  BUILD_LIST_4          4 

 L. 149        64  LOAD_FAST                'dry_run'
               66  LOAD_CONST               ('dry_run',)
               68  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               70  POP_TOP          
               72  POP_BLOCK        
               74  JUMP_FORWARD        426  'to 426'
             76_0  COME_FROM_EXCEPT     50  '50'

 L. 150        76  DUP_TOP          
               78  LOAD_GLOBAL              DistutilsExecError
               80  COMPARE_OP               exception-match
               82  POP_JUMP_IF_FALSE   106  'to 106'
               84  POP_TOP          
               86  POP_TOP          
               88  POP_TOP          

 L. 153        90  LOAD_GLOBAL              DistutilsExecError
               92  LOAD_STR                 "unable to create zip file '%s': could neither import the 'zipfile' module nor find a standalone zip utility"

 L. 155        94  LOAD_FAST                'zip_filename'
               96  BINARY_MODULO    
               98  CALL_FUNCTION_1       1  '1 positional argument'
              100  RAISE_VARARGS_1       1  'exception instance'
              102  POP_EXCEPT       
              104  JUMP_FORWARD        426  'to 426'
            106_0  COME_FROM            82  '82'
              106  END_FINALLY      
          108_110  JUMP_FORWARD        426  'to 426'
            112_0  COME_FROM            34  '34'

 L. 158       112  LOAD_GLOBAL              log
              114  LOAD_METHOD              info
              116  LOAD_STR                 "creating '%s' and adding '%s' to it"

 L. 159       118  LOAD_FAST                'zip_filename'
              120  LOAD_FAST                'base_dir'
              122  CALL_METHOD_3         3  '3 positional arguments'
              124  POP_TOP          

 L. 161       126  LOAD_FAST                'dry_run'
          128_130  POP_JUMP_IF_TRUE    426  'to 426'

 L. 162       132  SETUP_EXCEPT        156  'to 156'

 L. 163       134  LOAD_GLOBAL              zipfile
              136  LOAD_ATTR                ZipFile
              138  LOAD_FAST                'zip_filename'
              140  LOAD_STR                 'w'

 L. 164       142  LOAD_GLOBAL              zipfile
              144  LOAD_ATTR                ZIP_DEFLATED
              146  LOAD_CONST               ('compression',)
              148  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              150  STORE_FAST               'zip'
              152  POP_BLOCK        
              154  JUMP_FORWARD        194  'to 194'
            156_0  COME_FROM_EXCEPT    132  '132'

 L. 165       156  DUP_TOP          
              158  LOAD_GLOBAL              RuntimeError
              160  COMPARE_OP               exception-match
              162  POP_JUMP_IF_FALSE   192  'to 192'
              164  POP_TOP          
              166  POP_TOP          
              168  POP_TOP          

 L. 166       170  LOAD_GLOBAL              zipfile
              172  LOAD_ATTR                ZipFile
              174  LOAD_FAST                'zip_filename'
              176  LOAD_STR                 'w'

 L. 167       178  LOAD_GLOBAL              zipfile
              180  LOAD_ATTR                ZIP_STORED
              182  LOAD_CONST               ('compression',)
              184  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              186  STORE_FAST               'zip'
              188  POP_EXCEPT       
              190  JUMP_FORWARD        194  'to 194'
            192_0  COME_FROM           162  '162'
              192  END_FINALLY      
            194_0  COME_FROM           190  '190'
            194_1  COME_FROM           154  '154'

 L. 169       194  LOAD_FAST                'base_dir'
              196  LOAD_GLOBAL              os
              198  LOAD_ATTR                curdir
              200  COMPARE_OP               !=
              202  POP_JUMP_IF_FALSE   250  'to 250'

 L. 170       204  LOAD_GLOBAL              os
              206  LOAD_ATTR                path
              208  LOAD_METHOD              normpath
              210  LOAD_GLOBAL              os
              212  LOAD_ATTR                path
              214  LOAD_METHOD              join
              216  LOAD_FAST                'base_dir'
              218  LOAD_STR                 ''
              220  CALL_METHOD_2         2  '2 positional arguments'
              222  CALL_METHOD_1         1  '1 positional argument'
              224  STORE_FAST               'path'

 L. 171       226  LOAD_FAST                'zip'
              228  LOAD_METHOD              write
              230  LOAD_FAST                'path'
              232  LOAD_FAST                'path'
              234  CALL_METHOD_2         2  '2 positional arguments'
              236  POP_TOP          

 L. 172       238  LOAD_GLOBAL              log
              240  LOAD_METHOD              info
              242  LOAD_STR                 "adding '%s'"
              244  LOAD_FAST                'path'
              246  CALL_METHOD_2         2  '2 positional arguments'
              248  POP_TOP          
            250_0  COME_FROM           202  '202'

 L. 173       250  SETUP_LOOP          418  'to 418'
              252  LOAD_GLOBAL              os
              254  LOAD_METHOD              walk
              256  LOAD_FAST                'base_dir'
              258  CALL_METHOD_1         1  '1 positional argument'
              260  GET_ITER         
              262  FOR_ITER            416  'to 416'
              264  UNPACK_SEQUENCE_3     3 
              266  STORE_FAST               'dirpath'
              268  STORE_FAST               'dirnames'
              270  STORE_FAST               'filenames'

 L. 174       272  SETUP_LOOP          336  'to 336'
              274  LOAD_FAST                'dirnames'
              276  GET_ITER         
              278  FOR_ITER            334  'to 334'
              280  STORE_FAST               'name'

 L. 175       282  LOAD_GLOBAL              os
              284  LOAD_ATTR                path
              286  LOAD_METHOD              normpath
              288  LOAD_GLOBAL              os
              290  LOAD_ATTR                path
              292  LOAD_METHOD              join
              294  LOAD_FAST                'dirpath'
              296  LOAD_FAST                'name'
              298  LOAD_STR                 ''
              300  CALL_METHOD_3         3  '3 positional arguments'
              302  CALL_METHOD_1         1  '1 positional argument'
              304  STORE_FAST               'path'

 L. 176       306  LOAD_FAST                'zip'
              308  LOAD_METHOD              write
              310  LOAD_FAST                'path'
              312  LOAD_FAST                'path'
              314  CALL_METHOD_2         2  '2 positional arguments'
              316  POP_TOP          

 L. 177       318  LOAD_GLOBAL              log
              320  LOAD_METHOD              info
              322  LOAD_STR                 "adding '%s'"
              324  LOAD_FAST                'path'
              326  CALL_METHOD_2         2  '2 positional arguments'
              328  POP_TOP          
          330_332  JUMP_BACK           278  'to 278'
              334  POP_BLOCK        
            336_0  COME_FROM_LOOP      272  '272'

 L. 178       336  SETUP_LOOP          412  'to 412'
              338  LOAD_FAST                'filenames'
              340  GET_ITER         
            342_0  COME_FROM           378  '378'
              342  FOR_ITER            410  'to 410'
              344  STORE_FAST               'name'

 L. 179       346  LOAD_GLOBAL              os
              348  LOAD_ATTR                path
              350  LOAD_METHOD              normpath
              352  LOAD_GLOBAL              os
              354  LOAD_ATTR                path
              356  LOAD_METHOD              join
              358  LOAD_FAST                'dirpath'
              360  LOAD_FAST                'name'
              362  CALL_METHOD_2         2  '2 positional arguments'
              364  CALL_METHOD_1         1  '1 positional argument'
              366  STORE_FAST               'path'

 L. 180       368  LOAD_GLOBAL              os
              370  LOAD_ATTR                path
              372  LOAD_METHOD              isfile
              374  LOAD_FAST                'path'
              376  CALL_METHOD_1         1  '1 positional argument'
          378_380  POP_JUMP_IF_FALSE   342  'to 342'

 L. 181       382  LOAD_FAST                'zip'
              384  LOAD_METHOD              write
              386  LOAD_FAST                'path'
              388  LOAD_FAST                'path'
            390_0  COME_FROM            74  '74'
              390  CALL_METHOD_2         2  '2 positional arguments'
              392  POP_TOP          

 L. 182       394  LOAD_GLOBAL              log
              396  LOAD_METHOD              info
              398  LOAD_STR                 "adding '%s'"
              400  LOAD_FAST                'path'
              402  CALL_METHOD_2         2  '2 positional arguments'
              404  POP_TOP          
          406_408  JUMP_BACK           342  'to 342'
              410  POP_BLOCK        
            412_0  COME_FROM_LOOP      336  '336'
          412_414  JUMP_BACK           262  'to 262'
              416  POP_BLOCK        
            418_0  COME_FROM_LOOP      250  '250'

 L. 183       418  LOAD_FAST                'zip'
            420_0  COME_FROM           104  '104'
              420  LOAD_METHOD              close
              422  CALL_METHOD_0         0  '0 positional arguments'
              424  POP_TOP          
            426_0  COME_FROM           128  '128'
            426_1  COME_FROM           108  '108'

 L. 185       426  LOAD_FAST                'zip_filename'
              428  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 390_0


ARCHIVE_FORMATS = {'gztar':(
  make_tarball, [('compress', 'gzip')], "gzip'ed tar-file"), 
 'bztar':(
  make_tarball, [('compress', 'bzip2')], "bzip2'ed tar-file"), 
 'xztar':(
  make_tarball, [('compress', 'xz')], "xz'ed tar-file"), 
 'ztar':(
  make_tarball, [('compress', 'compress')], 'compressed tar file'), 
 'tar':(
  make_tarball, [('compress', None)], 'uncompressed tar file'), 
 'zip':(
  make_zipfile, [], 'ZIP file')}

def check_archive_formats(formats):
    """Returns the first format from the 'format' list that is unknown.

    If all formats are known, returns None
    """
    for format in formats:
        if format not in ARCHIVE_FORMATS:
            return format


def make_archive(base_name, format, root_dir=None, base_dir=None, verbose=0, dry_run=0, owner=None, group=None):
    """Create an archive file (eg. zip or tar).

    'base_name' is the name of the file to create, minus any format-specific
    extension; 'format' is the archive format: one of "zip", "tar", "gztar",
    "bztar", "xztar", or "ztar".

    'root_dir' is a directory that will be the root directory of the
    archive; ie. we typically chdir into 'root_dir' before creating the
    archive.  'base_dir' is the directory where we start archiving from;
    ie. 'base_dir' will be the common prefix of all files and
    directories in the archive.  'root_dir' and 'base_dir' both default
    to the current directory.  Returns the name of the archive file.

    'owner' and 'group' are used when creating a tar archive. By default,
    uses the current owner and group.
    """
    save_cwd = os.getcwd()
    if root_dir is not None:
        log.debug("changing into '%s'", root_dir)
        base_name = os.path.abspath(base_name)
        if not dry_run:
            os.chdir(root_dir)
    if base_dir is None:
        base_dir = os.curdir
    kwargs = {'dry_run': dry_run}
    try:
        format_info = ARCHIVE_FORMATS[format]
    except KeyError:
        raise ValueError("unknown archive format '%s'" % format)

    func = format_info[0]
    for arg, val in format_info[1]:
        kwargs[arg] = val

    if format != 'zip':
        kwargs['owner'] = owner
        kwargs['group'] = group
    try:
        filename = func(base_name, base_dir, **kwargs)
    finally:
        if root_dir is not None:
            log.debug("changing back to '%s'", save_cwd)
            os.chdir(save_cwd)

    return filename