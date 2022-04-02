# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
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
else:
    from distutils.errors import DistutilsExecError
    import distutils.spawn as spawn
    from distutils.dir_util import mkpath
    from distutils import log
try:
    from pwd import getpwnam
except ImportError:
    getpwnam = None
else:
    try:
        from grp import getgrnam
    except ImportError:
        getgrnam = None
    else:

        def _get_gid(name):
            """Returns a gid, given a group name."""
            if getgrnam is None or name is None:
                return
            try:
                result = getgrnam(name)
            except KeyError:
                result = None
            else:
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
            else:
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
               18  CALL_METHOD_1         1  ''
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

 L. 147        50  SETUP_FINALLY        76  'to 76'

 L. 148        52  LOAD_GLOBAL              spawn
               54  LOAD_STR                 'zip'
               56  LOAD_FAST                'zipoptions'
               58  LOAD_FAST                'zip_filename'
               60  LOAD_FAST                'base_dir'
               62  BUILD_LIST_4          4 

 L. 149        64  LOAD_FAST                'dry_run'

 L. 148        66  LOAD_CONST               ('dry_run',)
               68  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               70  POP_TOP          
               72  POP_BLOCK        
               74  JUMP_FORWARD        424  'to 424'
             76_0  COME_FROM_FINALLY    50  '50'

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

 L. 153        96  BINARY_MODULO    
               98  CALL_FUNCTION_1       1  ''
              100  RAISE_VARARGS_1       1  'exception instance'
              102  POP_EXCEPT       
              104  JUMP_FORWARD        424  'to 424'
            106_0  COME_FROM            82  '82'
              106  END_FINALLY      
          108_110  JUMP_FORWARD        424  'to 424'
            112_0  COME_FROM            34  '34'

 L. 158       112  LOAD_GLOBAL              log
              114  LOAD_METHOD              info
              116  LOAD_STR                 "creating '%s' and adding '%s' to it"

 L. 159       118  LOAD_FAST                'zip_filename'

 L. 159       120  LOAD_FAST                'base_dir'

 L. 158       122  CALL_METHOD_3         3  ''
              124  POP_TOP          

 L. 161       126  LOAD_FAST                'dry_run'
          128_130  POP_JUMP_IF_TRUE    424  'to 424'

 L. 162       132  SETUP_FINALLY       156  'to 156'

 L. 163       134  LOAD_GLOBAL              zipfile
              136  LOAD_ATTR                ZipFile
              138  LOAD_FAST                'zip_filename'
              140  LOAD_STR                 'w'

 L. 164       142  LOAD_GLOBAL              zipfile
              144  LOAD_ATTR                ZIP_DEFLATED

 L. 163       146  LOAD_CONST               ('compression',)
              148  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              150  STORE_FAST               'zip'
              152  POP_BLOCK        
              154  JUMP_FORWARD        194  'to 194'
            156_0  COME_FROM_FINALLY   132  '132'

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

 L. 166       182  LOAD_CONST               ('compression',)
              184  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              186  STORE_FAST               'zip'
              188  POP_EXCEPT       
              190  JUMP_FORWARD        194  'to 194'
            192_0  COME_FROM           162  '162'
              192  END_FINALLY      
            194_0  COME_FROM           190  '190'
            194_1  COME_FROM           154  '154'

 L. 169       194  LOAD_FAST                'zip'
              196  SETUP_WITH          418  'to 418'
              198  POP_TOP          

 L. 170       200  LOAD_FAST                'base_dir'
              202  LOAD_GLOBAL              os
              204  LOAD_ATTR                curdir
              206  COMPARE_OP               !=
          208_210  POP_JUMP_IF_FALSE   258  'to 258'

 L. 171       212  LOAD_GLOBAL              os
              214  LOAD_ATTR                path
              216  LOAD_METHOD              normpath
              218  LOAD_GLOBAL              os
              220  LOAD_ATTR                path
              222  LOAD_METHOD              join
              224  LOAD_FAST                'base_dir'
              226  LOAD_STR                 ''
              228  CALL_METHOD_2         2  ''
              230  CALL_METHOD_1         1  ''
              232  STORE_FAST               'path'

 L. 172       234  LOAD_FAST                'zip'
              236  LOAD_METHOD              write
              238  LOAD_FAST                'path'
              240  LOAD_FAST                'path'
              242  CALL_METHOD_2         2  ''
              244  POP_TOP          

 L. 173       246  LOAD_GLOBAL              log
              248  LOAD_METHOD              info
              250  LOAD_STR                 "adding '%s'"
              252  LOAD_FAST                'path'
              254  CALL_METHOD_2         2  ''
              256  POP_TOP          
            258_0  COME_FROM           208  '208'

 L. 174       258  LOAD_GLOBAL              os
              260  LOAD_METHOD              walk
              262  LOAD_FAST                'base_dir'
              264  CALL_METHOD_1         1  ''
              266  GET_ITER         
              268  FOR_ITER            414  'to 414'
              270  UNPACK_SEQUENCE_3     3 
              272  STORE_FAST               'dirpath'
              274  STORE_FAST               'dirnames'
              276  STORE_FAST               'filenames'

 L. 175       278  LOAD_FAST                'dirnames'
              280  GET_ITER         
              282  FOR_ITER            338  'to 338'
              284  STORE_FAST               'name'

 L. 176       286  LOAD_GLOBAL              os
              288  LOAD_ATTR                path
              290  LOAD_METHOD              normpath
              292  LOAD_GLOBAL              os
              294  LOAD_ATTR                path
              296  LOAD_METHOD              join
              298  LOAD_FAST                'dirpath'
              300  LOAD_FAST                'name'
              302  LOAD_STR                 ''
              304  CALL_METHOD_3         3  ''
              306  CALL_METHOD_1         1  ''
              308  STORE_FAST               'path'

 L. 177       310  LOAD_FAST                'zip'
              312  LOAD_METHOD              write
              314  LOAD_FAST                'path'
              316  LOAD_FAST                'path'
              318  CALL_METHOD_2         2  ''
              320  POP_TOP          

 L. 178       322  LOAD_GLOBAL              log
              324  LOAD_METHOD              info
              326  LOAD_STR                 "adding '%s'"
              328  LOAD_FAST                'path'
              330  CALL_METHOD_2         2  ''
              332  POP_TOP          
          334_336  JUMP_BACK           282  'to 282'

 L. 179       338  LOAD_FAST                'filenames'
              340  GET_ITER         
            342_0  COME_FROM           378  '378'
              342  FOR_ITER            410  'to 410'
              344  STORE_FAST               'name'

 L. 180       346  LOAD_GLOBAL              os
              348  LOAD_ATTR                path
              350  LOAD_METHOD              normpath
              352  LOAD_GLOBAL              os
              354  LOAD_ATTR                path
              356  LOAD_METHOD              join
              358  LOAD_FAST                'dirpath'
              360  LOAD_FAST                'name'
              362  CALL_METHOD_2         2  ''
              364  CALL_METHOD_1         1  ''
              366  STORE_FAST               'path'

 L. 181       368  LOAD_GLOBAL              os
              370  LOAD_ATTR                path
              372  LOAD_METHOD              isfile
              374  LOAD_FAST                'path'
              376  CALL_METHOD_1         1  ''
          378_380  POP_JUMP_IF_FALSE   342  'to 342'

 L. 182       382  LOAD_FAST                'zip'
              384  LOAD_METHOD              write
              386  LOAD_FAST                'path'
            388_0  COME_FROM            74  '74'
              388  LOAD_FAST                'path'
              390  CALL_METHOD_2         2  ''
              392  POP_TOP          

 L. 183       394  LOAD_GLOBAL              log
              396  LOAD_METHOD              info
              398  LOAD_STR                 "adding '%s'"
              400  LOAD_FAST                'path'
              402  CALL_METHOD_2         2  ''
              404  POP_TOP          
          406_408  JUMP_BACK           342  'to 342'
          410_412  JUMP_BACK           268  'to 268'
              414  POP_BLOCK        
              416  BEGIN_FINALLY    
            418_0  COME_FROM_WITH      196  '196'
            418_1  COME_FROM           104  '104'
              418  WITH_CLEANUP_START
              420  WITH_CLEANUP_FINISH
              422  END_FINALLY      
            424_0  COME_FROM           128  '128'
            424_1  COME_FROM           108  '108'

 L. 185       424  LOAD_FAST                'zip_filename'
              426  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 388_0


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
            else:
                func = format_info[0]
                for arg, val in format_info[1]:
                    kwargs[arg] = val
                else:
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