# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: distutils\file_util.py
"""distutils.file_util

Utility functions for operating on single files.
"""
import os
from distutils.errors import DistutilsFileError
from distutils import log
_copy_action = {None:'copying', 
 'hard':'hard linking', 
 'sym':'symbolically linking'}

def _copy_file_contents(src, dst, buffer_size=16384):
    """Copy the file 'src' to 'dst'; both must be filenames.  Any error
    opening either file, reading from 'src', or writing to 'dst', raises
    DistutilsFileError.  Data is read/written in chunks of 'buffer_size'
    bytes (default 16k).  No attempt is made to handle anything apart from
    regular files.
    """
    fsrc = None
    fdst = None
    try:
        try:
            fsrc = open(src, 'rb')
        except OSError as e:
            try:
                raise DistutilsFileError("could not open '%s': %s" % (src, e.strerror))
            finally:
                e = None
                del e

        else:
            if os.path.exists(dst):
                try:
                    os.unlink(dst)
                except OSError as e:
                    try:
                        raise DistutilsFileError("could not delete '%s': %s" % (dst, e.strerror))
                    finally:
                        e = None
                        del e

            try:
                fdst = open(dst, 'wb')
            except OSError as e:
                try:
                    raise DistutilsFileError("could not create '%s': %s" % (dst, e.strerror))
                finally:
                    e = None
                    del e

            else:
                while True:
                    try:
                        buf = fsrc.read(buffer_size)
                    except OSError as e:
                        try:
                            raise DistutilsFileError("could not read from '%s': %s" % (src, e.strerror))
                        finally:
                            e = None
                            del e

                    else:
                        if not buf:
                            break
                        try:
                            fdst.write(buf)
                        except OSError as e:
                            try:
                                raise DistutilsFileError("could not write to '%s': %s" % (dst, e.strerror))
                            finally:
                                e = None
                                del e

    finally:
        if fdst:
            fdst.close()
        if fsrc:
            fsrc.close()


def copy_file--- This code section failed: ---

 L. 100         0  LOAD_CONST               0
                2  LOAD_CONST               ('newer',)
                4  IMPORT_NAME_ATTR         distutils.dep_util
                6  IMPORT_FROM              newer
                8  STORE_FAST               'newer'
               10  POP_TOP          

 L. 101        12  LOAD_CONST               0
               14  LOAD_CONST               ('ST_ATIME', 'ST_MTIME', 'ST_MODE', 'S_IMODE')
               16  IMPORT_NAME              stat
               18  IMPORT_FROM              ST_ATIME
               20  STORE_FAST               'ST_ATIME'
               22  IMPORT_FROM              ST_MTIME
               24  STORE_FAST               'ST_MTIME'
               26  IMPORT_FROM              ST_MODE
               28  STORE_FAST               'ST_MODE'
               30  IMPORT_FROM              S_IMODE
               32  STORE_FAST               'S_IMODE'
               34  POP_TOP          

 L. 103        36  LOAD_GLOBAL              os
               38  LOAD_ATTR                path
               40  LOAD_METHOD              isfile
               42  LOAD_FAST                'src'
               44  CALL_METHOD_1         1  ''
               46  POP_JUMP_IF_TRUE     60  'to 60'

 L. 104        48  LOAD_GLOBAL              DistutilsFileError

 L. 105        50  LOAD_STR                 "can't copy '%s': doesn't exist or not a regular file"
               52  LOAD_FAST                'src'
               54  BINARY_MODULO    

 L. 104        56  CALL_FUNCTION_1       1  ''
               58  RAISE_VARARGS_1       1  'exception instance'
             60_0  COME_FROM            46  '46'

 L. 107        60  LOAD_GLOBAL              os
               62  LOAD_ATTR                path
               64  LOAD_METHOD              isdir
               66  LOAD_FAST                'dst'
               68  CALL_METHOD_1         1  ''
               70  POP_JUMP_IF_FALSE   100  'to 100'

 L. 108        72  LOAD_FAST                'dst'
               74  STORE_FAST               'dir'

 L. 109        76  LOAD_GLOBAL              os
               78  LOAD_ATTR                path
               80  LOAD_METHOD              join
               82  LOAD_FAST                'dst'
               84  LOAD_GLOBAL              os
               86  LOAD_ATTR                path
               88  LOAD_METHOD              basename
               90  LOAD_FAST                'src'
               92  CALL_METHOD_1         1  ''
               94  CALL_METHOD_2         2  ''
               96  STORE_FAST               'dst'
               98  JUMP_FORWARD        112  'to 112'
            100_0  COME_FROM            70  '70'

 L. 111       100  LOAD_GLOBAL              os
              102  LOAD_ATTR                path
              104  LOAD_METHOD              dirname
              106  LOAD_FAST                'dst'
              108  CALL_METHOD_1         1  ''
              110  STORE_FAST               'dir'
            112_0  COME_FROM            98  '98'

 L. 113       112  LOAD_FAST                'update'
              114  POP_JUMP_IF_FALSE   154  'to 154'
              116  LOAD_FAST                'newer'
              118  LOAD_FAST                'src'
              120  LOAD_FAST                'dst'
              122  CALL_FUNCTION_2       2  ''
              124  POP_JUMP_IF_TRUE    154  'to 154'

 L. 114       126  LOAD_FAST                'verbose'
              128  LOAD_CONST               1
              130  COMPARE_OP               >=
              132  POP_JUMP_IF_FALSE   146  'to 146'

 L. 115       134  LOAD_GLOBAL              log
              136  LOAD_METHOD              debug
              138  LOAD_STR                 'not copying %s (output up-to-date)'
              140  LOAD_FAST                'src'
              142  CALL_METHOD_2         2  ''
              144  POP_TOP          
            146_0  COME_FROM           132  '132'

 L. 116       146  LOAD_FAST                'dst'
              148  LOAD_CONST               0
              150  BUILD_TUPLE_2         2 
              152  RETURN_VALUE     
            154_0  COME_FROM           124  '124'
            154_1  COME_FROM           114  '114'

 L. 118       154  SETUP_FINALLY       168  'to 168'

 L. 119       156  LOAD_GLOBAL              _copy_action
              158  LOAD_FAST                'link'
              160  BINARY_SUBSCR    
              162  STORE_FAST               'action'
              164  POP_BLOCK        
              166  JUMP_FORWARD        200  'to 200'
            168_0  COME_FROM_FINALLY   154  '154'

 L. 120       168  DUP_TOP          
              170  LOAD_GLOBAL              KeyError
              172  COMPARE_OP               exception-match
              174  POP_JUMP_IF_FALSE   198  'to 198'
              176  POP_TOP          
              178  POP_TOP          
              180  POP_TOP          

 L. 121       182  LOAD_GLOBAL              ValueError
              184  LOAD_STR                 "invalid value '%s' for 'link' argument"
              186  LOAD_FAST                'link'
              188  BINARY_MODULO    
              190  CALL_FUNCTION_1       1  ''
              192  RAISE_VARARGS_1       1  'exception instance'
              194  POP_EXCEPT       
              196  JUMP_FORWARD        200  'to 200'
            198_0  COME_FROM           174  '174'
              198  END_FINALLY      
            200_0  COME_FROM           196  '196'
            200_1  COME_FROM           166  '166'

 L. 123       200  LOAD_FAST                'verbose'
              202  LOAD_CONST               1
              204  COMPARE_OP               >=
          206_208  POP_JUMP_IF_FALSE   268  'to 268'

 L. 124       210  LOAD_GLOBAL              os
              212  LOAD_ATTR                path
              214  LOAD_METHOD              basename
              216  LOAD_FAST                'dst'
              218  CALL_METHOD_1         1  ''
              220  LOAD_GLOBAL              os
              222  LOAD_ATTR                path
              224  LOAD_METHOD              basename
              226  LOAD_FAST                'src'
              228  CALL_METHOD_1         1  ''
              230  COMPARE_OP               ==
              232  POP_JUMP_IF_FALSE   252  'to 252'

 L. 125       234  LOAD_GLOBAL              log
              236  LOAD_METHOD              info
              238  LOAD_STR                 '%s %s -> %s'
              240  LOAD_FAST                'action'
              242  LOAD_FAST                'src'
              244  LOAD_FAST                'dir'
              246  CALL_METHOD_4         4  ''
              248  POP_TOP          
              250  JUMP_FORWARD        268  'to 268'
            252_0  COME_FROM           232  '232'

 L. 127       252  LOAD_GLOBAL              log
              254  LOAD_METHOD              info
              256  LOAD_STR                 '%s %s -> %s'
              258  LOAD_FAST                'action'
              260  LOAD_FAST                'src'
              262  LOAD_FAST                'dst'
              264  CALL_METHOD_4         4  ''
              266  POP_TOP          
            268_0  COME_FROM           250  '250'
            268_1  COME_FROM           206  '206'

 L. 129       268  LOAD_FAST                'dry_run'
          270_272  POP_JUMP_IF_FALSE   282  'to 282'

 L. 130       274  LOAD_FAST                'dst'
              276  LOAD_CONST               1
              278  BUILD_TUPLE_2         2 
              280  RETURN_VALUE     
            282_0  COME_FROM           270  '270'

 L. 134       282  LOAD_FAST                'link'
              284  LOAD_STR                 'hard'
              286  COMPARE_OP               ==
          288_290  POP_JUMP_IF_FALSE   370  'to 370'

 L. 135       292  LOAD_GLOBAL              os
              294  LOAD_ATTR                path
              296  LOAD_METHOD              exists
              298  LOAD_FAST                'dst'
              300  CALL_METHOD_1         1  ''
          302_304  POP_JUMP_IF_FALSE   322  'to 322'
              306  LOAD_GLOBAL              os
              308  LOAD_ATTR                path
              310  LOAD_METHOD              samefile
              312  LOAD_FAST                'src'
              314  LOAD_FAST                'dst'
              316  CALL_METHOD_2         2  ''
          318_320  POP_JUMP_IF_TRUE    430  'to 430'
            322_0  COME_FROM           302  '302'

 L. 136       322  SETUP_FINALLY       346  'to 346'

 L. 137       324  LOAD_GLOBAL              os
              326  LOAD_METHOD              link
              328  LOAD_FAST                'src'
              330  LOAD_FAST                'dst'
              332  CALL_METHOD_2         2  ''
              334  POP_TOP          

 L. 138       336  LOAD_FAST                'dst'
              338  LOAD_CONST               1
              340  BUILD_TUPLE_2         2 
              342  POP_BLOCK        
              344  RETURN_VALUE     
            346_0  COME_FROM_FINALLY   322  '322'

 L. 139       346  DUP_TOP          
              348  LOAD_GLOBAL              OSError
              350  COMPARE_OP               exception-match
          352_354  POP_JUMP_IF_FALSE   366  'to 366'
              356  POP_TOP          
              358  POP_TOP          
              360  POP_TOP          

 L. 143       362  POP_EXCEPT       
              364  JUMP_FORWARD        368  'to 368'
            366_0  COME_FROM           352  '352'
              366  END_FINALLY      
            368_0  COME_FROM           364  '364'
              368  JUMP_FORWARD        430  'to 430'
            370_0  COME_FROM           288  '288'

 L. 144       370  LOAD_FAST                'link'
              372  LOAD_STR                 'sym'
              374  COMPARE_OP               ==
          376_378  POP_JUMP_IF_FALSE   430  'to 430'

 L. 145       380  LOAD_GLOBAL              os
              382  LOAD_ATTR                path
              384  LOAD_METHOD              exists
              386  LOAD_FAST                'dst'
              388  CALL_METHOD_1         1  ''
          390_392  POP_JUMP_IF_FALSE   410  'to 410'
              394  LOAD_GLOBAL              os
              396  LOAD_ATTR                path
              398  LOAD_METHOD              samefile
              400  LOAD_FAST                'src'
              402  LOAD_FAST                'dst'
              404  CALL_METHOD_2         2  ''
          406_408  POP_JUMP_IF_TRUE    430  'to 430'
            410_0  COME_FROM           390  '390'

 L. 146       410  LOAD_GLOBAL              os
              412  LOAD_METHOD              symlink
              414  LOAD_FAST                'src'
              416  LOAD_FAST                'dst'
              418  CALL_METHOD_2         2  ''
              420  POP_TOP          

 L. 147       422  LOAD_FAST                'dst'
              424  LOAD_CONST               1
              426  BUILD_TUPLE_2         2 
              428  RETURN_VALUE     
            430_0  COME_FROM           406  '406'
            430_1  COME_FROM           376  '376'
            430_2  COME_FROM           368  '368'
            430_3  COME_FROM           318  '318'

 L. 151       430  LOAD_GLOBAL              _copy_file_contents
              432  LOAD_FAST                'src'
              434  LOAD_FAST                'dst'
              436  CALL_FUNCTION_2       2  ''
              438  POP_TOP          

 L. 152       440  LOAD_FAST                'preserve_mode'
          442_444  POP_JUMP_IF_TRUE    452  'to 452'
              446  LOAD_FAST                'preserve_times'
          448_450  POP_JUMP_IF_FALSE   518  'to 518'
            452_0  COME_FROM           442  '442'

 L. 153       452  LOAD_GLOBAL              os
              454  LOAD_METHOD              stat
              456  LOAD_FAST                'src'
              458  CALL_METHOD_1         1  ''
              460  STORE_FAST               'st'

 L. 157       462  LOAD_FAST                'preserve_times'
          464_466  POP_JUMP_IF_FALSE   492  'to 492'

 L. 158       468  LOAD_GLOBAL              os
              470  LOAD_METHOD              utime
              472  LOAD_FAST                'dst'
              474  LOAD_FAST                'st'
              476  LOAD_FAST                'ST_ATIME'
              478  BINARY_SUBSCR    
              480  LOAD_FAST                'st'
              482  LOAD_FAST                'ST_MTIME'
              484  BINARY_SUBSCR    
              486  BUILD_TUPLE_2         2 
              488  CALL_METHOD_2         2  ''
              490  POP_TOP          
            492_0  COME_FROM           464  '464'

 L. 159       492  LOAD_FAST                'preserve_mode'
          494_496  POP_JUMP_IF_FALSE   518  'to 518'

 L. 160       498  LOAD_GLOBAL              os
              500  LOAD_METHOD              chmod
              502  LOAD_FAST                'dst'
              504  LOAD_FAST                'S_IMODE'
              506  LOAD_FAST                'st'
              508  LOAD_FAST                'ST_MODE'
              510  BINARY_SUBSCR    
              512  CALL_FUNCTION_1       1  ''
              514  CALL_METHOD_2         2  ''
              516  POP_TOP          
            518_0  COME_FROM           494  '494'
            518_1  COME_FROM           448  '448'

 L. 162       518  LOAD_FAST                'dst'
              520  LOAD_CONST               1
              522  BUILD_TUPLE_2         2 
              524  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 358


def move_file(src, dst, verbose=1, dry_run=0):
    """Move a file 'src' to 'dst'.  If 'dst' is a directory, the file will
    be moved into it with the same name; otherwise, 'src' is just renamed
    to 'dst'.  Return the new full name of the file.

    Handles cross-device moves on Unix using 'copy_file()'.  What about
    other systems???
    """
    from os.path import exists, isfile, isdir, basename, dirname
    import errno
    if verbose >= 1:
        log.info('moving %s -> %s', src, dst)
    if dry_run:
        return dst
    if not isfile(src):
        raise DistutilsFileError("can't move '%s': not a regular file" % src)
    if isdir(dst):
        dst = os.path.joindstbasename(src)
    else:
        if exists(dst):
            raise DistutilsFileError("can't move '%s': destination '%s' already exists" % (
             src, dst))
        else:
            assert isdir(dirname(dst)), "can't move '%s': destination '%s' not a valid path" % (
             src, dst)
        copy_it = False
        try:
            os.renamesrcdst
        except OSError as e:
            try:
                num, msg = e.args
                if num == errno.EXDEV:
                    copy_it = True
                else:
                    raise DistutilsFileError("couldn't move '%s' to '%s': %s" % (src, dst, msg))
            finally:
                e = None
                del e

        else:
            if copy_it:
                copy_file(src, dst, verbose=verbose)
                try:
                    os.unlink(src)
                except OSError as e:
                    try:
                        num, msg = e.args
                        try:
                            os.unlink(dst)
                        except OSError:
                            pass
                        else:
                            raise DistutilsFileError("couldn't move '%s' to '%s' by copy/delete: delete '%s' failed: %s" % (
                             src, dst, src, msg))
                    finally:
                        e = None
                        del e

            return dst


def write_file(filename, contents):
    """Create a file with the specified name and write 'contents' (a
    sequence of strings without line terminators) to it.
    """
    f = open(filename, 'w')
    try:
        for line in contents:
            f.write(line + '\n')

    finally:
        f.close()