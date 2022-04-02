# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: stat.py
"""Constants/functions for interpreting results of os.stat() and os.lstat().

Suggested usage: from stat import *
"""
ST_MODE = 0
ST_INO = 1
ST_DEV = 2
ST_NLINK = 3
ST_UID = 4
ST_GID = 5
ST_SIZE = 6
ST_ATIME = 7
ST_MTIME = 8
ST_CTIME = 9

def S_IMODE(mode):
    """Return the portion of the file's mode that can be set by
    os.chmod().
    """
    return mode & 4095


def S_IFMT(mode):
    """Return the portion of the file's mode that describes the
    file type.
    """
    return mode & 61440


S_IFDIR = 16384
S_IFCHR = 8192
S_IFBLK = 24576
S_IFREG = 32768
S_IFIFO = 4096
S_IFLNK = 40960
S_IFSOCK = 49152
S_IFDOOR = 0
S_IFPORT = 0
S_IFWHT = 0

def S_ISDIR(mode):
    """Return True if mode is from a directory."""
    return S_IFMT(mode) == S_IFDIR


def S_ISCHR(mode):
    """Return True if mode is from a character special device file."""
    return S_IFMT(mode) == S_IFCHR


def S_ISBLK(mode):
    """Return True if mode is from a block special device file."""
    return S_IFMT(mode) == S_IFBLK


def S_ISREG(mode):
    """Return True if mode is from a regular file."""
    return S_IFMT(mode) == S_IFREG


def S_ISFIFO(mode):
    """Return True if mode is from a FIFO (named pipe)."""
    return S_IFMT(mode) == S_IFIFO


def S_ISLNK(mode):
    """Return True if mode is from a symbolic link."""
    return S_IFMT(mode) == S_IFLNK


def S_ISSOCK(mode):
    """Return True if mode is from a socket."""
    return S_IFMT(mode) == S_IFSOCK


def S_ISDOOR(mode):
    """Return True if mode is from a door."""
    return False


def S_ISPORT(mode):
    """Return True if mode is from an event port."""
    return False


def S_ISWHT(mode):
    """Return True if mode is from a whiteout."""
    return False


S_ISUID = 2048
S_ISGID = 1024
S_ENFMT = S_ISGID
S_ISVTX = 512
S_IREAD = 256
S_IWRITE = 128
S_IEXEC = 64
S_IRWXU = 448
S_IRUSR = 256
S_IWUSR = 128
S_IXUSR = 64
S_IRWXG = 56
S_IRGRP = 32
S_IWGRP = 16
S_IXGRP = 8
S_IRWXO = 7
S_IROTH = 4
S_IWOTH = 2
S_IXOTH = 1
UF_NODUMP = 1
UF_IMMUTABLE = 2
UF_APPEND = 4
UF_OPAQUE = 8
UF_NOUNLINK = 16
UF_COMPRESSED = 32
UF_HIDDEN = 32768
SF_ARCHIVED = 65536
SF_IMMUTABLE = 131072
SF_APPEND = 262144
SF_NOUNLINK = 1048576
SF_SNAPSHOT = 2097152
_filemode_table = (
 (
  (
   S_IFLNK, 'l'),
  (
   S_IFSOCK, 's'),
  (
   S_IFREG, '-'),
  (
   S_IFBLK, 'b'),
  (
   S_IFDIR, 'd'),
  (
   S_IFCHR, 'c'),
  (
   S_IFIFO, 'p')),
 (
  (
   S_IRUSR, 'r'),),
 (
  (
   S_IWUSR, 'w'),),
 (
  (
   S_IXUSR | S_ISUID, 's'),
  (
   S_ISUID, 'S'),
  (
   S_IXUSR, 'x')),
 (
  (
   S_IRGRP, 'r'),),
 (
  (
   S_IWGRP, 'w'),),
 (
  (
   S_IXGRP | S_ISGID, 's'),
  (
   S_ISGID, 'S'),
  (
   S_IXGRP, 'x')),
 (
  (
   S_IROTH, 'r'),),
 (
  (
   S_IWOTH, 'w'),),
 (
  (
   S_IXOTH | S_ISVTX, 't'),
  (
   S_ISVTX, 'T'),
  (
   S_IXOTH, 'x')))

def filemode--- This code section failed: ---

 L. 158         0  BUILD_LIST_0          0 
                2  STORE_FAST               'perm'

 L. 159         4  LOAD_GLOBAL              _filemode_table
                6  GET_ITER         
                8  FOR_ITER             64  'to 64'
               10  STORE_FAST               'table'

 L. 160        12  LOAD_FAST                'table'
               14  GET_ITER         
             16_0  COME_FROM            34  '34'
               16  FOR_ITER             52  'to 52'
               18  UNPACK_SEQUENCE_2     2 
               20  STORE_FAST               'bit'
               22  STORE_FAST               'char'

 L. 161        24  LOAD_FAST                'mode'
               26  LOAD_FAST                'bit'
               28  BINARY_AND       
               30  LOAD_FAST                'bit'
               32  COMPARE_OP               ==
               34  POP_JUMP_IF_FALSE    16  'to 16'

 L. 162        36  LOAD_FAST                'perm'
               38  LOAD_METHOD              append
               40  LOAD_FAST                'char'
               42  CALL_METHOD_1         1  ''
               44  POP_TOP          

 L. 163        46  POP_TOP          
               48  CONTINUE              8  'to 8'
               50  JUMP_BACK            16  'to 16'

 L. 165        52  LOAD_FAST                'perm'
               54  LOAD_METHOD              append
               56  LOAD_STR                 '-'
               58  CALL_METHOD_1         1  ''
               60  POP_TOP          
               62  JUMP_BACK             8  'to 8'

 L. 166        64  LOAD_STR                 ''
               66  LOAD_METHOD              join
               68  LOAD_FAST                'perm'
               70  CALL_METHOD_1         1  ''
               72  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CONTINUE' instruction at offset 48


FILE_ATTRIBUTE_ARCHIVE = 32
FILE_ATTRIBUTE_COMPRESSED = 2048
FILE_ATTRIBUTE_DEVICE = 64
FILE_ATTRIBUTE_DIRECTORY = 16
FILE_ATTRIBUTE_ENCRYPTED = 16384
FILE_ATTRIBUTE_HIDDEN = 2
FILE_ATTRIBUTE_INTEGRITY_STREAM = 32768
FILE_ATTRIBUTE_NORMAL = 128
FILE_ATTRIBUTE_NOT_CONTENT_INDEXED = 8192
FILE_ATTRIBUTE_NO_SCRUB_DATA = 131072
FILE_ATTRIBUTE_OFFLINE = 4096
FILE_ATTRIBUTE_READONLY = 1
FILE_ATTRIBUTE_REPARSE_POINT = 1024
FILE_ATTRIBUTE_SPARSE_FILE = 512
FILE_ATTRIBUTE_SYSTEM = 4
FILE_ATTRIBUTE_TEMPORARY = 256
FILE_ATTRIBUTE_VIRTUAL = 65536
try:
    from _stat import *
except ImportError:
    pass