# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: importlib\_common.py
import os, pathlib, zipfile, tempfile, functools, contextlib

def from_package(package):
    """
    Return a Traversable object for the given package.

    """
    return fallback_resources(package.__spec__)


def fallback_resources--- This code section failed: ---

 L.  18         0  LOAD_GLOBAL              pathlib
                2  LOAD_METHOD              Path
                4  LOAD_FAST                'spec'
                6  LOAD_ATTR                origin
                8  CALL_METHOD_1         1  ''
               10  LOAD_ATTR                parent
               12  STORE_FAST               'package_directory'

 L.  19        14  SETUP_FINALLY        56  'to 56'

 L.  20        16  LOAD_FAST                'spec'
               18  LOAD_ATTR                loader
               20  LOAD_ATTR                archive
               22  STORE_FAST               'archive_path'

 L.  21        24  LOAD_FAST                'package_directory'
               26  LOAD_METHOD              relative_to
               28  LOAD_FAST                'archive_path'
               30  CALL_METHOD_1         1  ''
               32  STORE_FAST               'rel_path'

 L.  22        34  LOAD_GLOBAL              zipfile
               36  LOAD_METHOD              Path
               38  LOAD_FAST                'archive_path'
               40  LOAD_GLOBAL              str
               42  LOAD_FAST                'rel_path'
               44  CALL_FUNCTION_1       1  ''
               46  LOAD_STR                 '/'
               48  BINARY_ADD       
               50  CALL_METHOD_2         2  ''
               52  POP_BLOCK        
               54  RETURN_VALUE     
             56_0  COME_FROM_FINALLY    14  '14'

 L.  23        56  DUP_TOP          
               58  LOAD_GLOBAL              Exception
               60  <121>                72  ''
               62  POP_TOP          
               64  POP_TOP          
               66  POP_TOP          

 L.  24        68  POP_EXCEPT       
               70  JUMP_FORWARD         74  'to 74'
               72  <48>             
             74_0  COME_FROM            70  '70'

 L.  25        74  LOAD_FAST                'package_directory'
               76  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 60


@contextlib.contextmanager
def _tempfile--- This code section failed: ---

 L.  33         0  LOAD_GLOBAL              tempfile
                2  LOAD_ATTR                mkstemp
                4  LOAD_FAST                'suffix'
                6  LOAD_CONST               ('suffix',)
                8  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'fd'
               14  STORE_FAST               'raw_path'

 L.  34        16  SETUP_FINALLY        92  'to 92'

 L.  35        18  LOAD_GLOBAL              os
               20  LOAD_METHOD              write
               22  LOAD_FAST                'fd'
               24  LOAD_FAST                'reader'
               26  CALL_FUNCTION_0       0  ''
               28  CALL_METHOD_2         2  ''
               30  POP_TOP          

 L.  36        32  LOAD_GLOBAL              os
               34  LOAD_METHOD              close
               36  LOAD_FAST                'fd'
               38  CALL_METHOD_1         1  ''
               40  POP_TOP          

 L.  37        42  LOAD_GLOBAL              pathlib
               44  LOAD_METHOD              Path
               46  LOAD_FAST                'raw_path'
               48  CALL_METHOD_1         1  ''
               50  YIELD_VALUE      
               52  POP_TOP          
               54  POP_BLOCK        

 L.  39        56  SETUP_FINALLY        72  'to 72'

 L.  40        58  LOAD_GLOBAL              os
               60  LOAD_METHOD              remove
               62  LOAD_FAST                'raw_path'
               64  CALL_METHOD_1         1  ''
               66  POP_TOP          
               68  POP_BLOCK        
               70  JUMP_FORWARD        128  'to 128'
             72_0  COME_FROM_FINALLY    56  '56'

 L.  41        72  DUP_TOP          
               74  LOAD_GLOBAL              FileNotFoundError
               76  <121>                88  ''
               78  POP_TOP          
               80  POP_TOP          
               82  POP_TOP          

 L.  42        84  POP_EXCEPT       
               86  JUMP_FORWARD        128  'to 128'
               88  <48>             
               90  JUMP_FORWARD        128  'to 128'
             92_0  COME_FROM_FINALLY    16  '16'

 L.  39        92  SETUP_FINALLY       108  'to 108'

 L.  40        94  LOAD_GLOBAL              os
               96  LOAD_METHOD              remove
               98  LOAD_FAST                'raw_path'
              100  CALL_METHOD_1         1  ''
              102  POP_TOP          
              104  POP_BLOCK        
              106  JUMP_FORWARD        126  'to 126'
            108_0  COME_FROM_FINALLY    92  '92'

 L.  41       108  DUP_TOP          
              110  LOAD_GLOBAL              FileNotFoundError
              112  <121>               124  ''
              114  POP_TOP          
              116  POP_TOP          
              118  POP_TOP          

 L.  42       120  POP_EXCEPT       
              122  JUMP_FORWARD        126  'to 126'
              124  <48>             
            126_0  COME_FROM           122  '122'
            126_1  COME_FROM           106  '106'
              126  <48>             
            128_0  COME_FROM            90  '90'
            128_1  COME_FROM            86  '86'
            128_2  COME_FROM            70  '70'

Parse error at or near `SETUP_FINALLY' instruction at offset 56


@functools.singledispatch
@contextlib.contextmanager
def as_file--- This code section failed: ---

 L.  52         0  LOAD_GLOBAL              _tempfile
                2  LOAD_FAST                'path'
                4  LOAD_ATTR                read_bytes
                6  LOAD_FAST                'path'
                8  LOAD_ATTR                name
               10  LOAD_CONST               ('suffix',)
               12  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               14  SETUP_WITH           38  'to 38'
               16  STORE_FAST               'local'

 L.  53        18  LOAD_FAST                'local'
               20  YIELD_VALUE      
               22  POP_TOP          
               24  POP_BLOCK        
               26  LOAD_CONST               None
               28  DUP_TOP          
               30  DUP_TOP          
               32  CALL_FUNCTION_3       3  ''
               34  POP_TOP          
               36  JUMP_FORWARD         54  'to 54'
             38_0  COME_FROM_WITH       14  '14'
               38  <49>             
               40  POP_JUMP_IF_TRUE     44  'to 44'
               42  <48>             
             44_0  COME_FROM            40  '40'
               44  POP_TOP          
               46  POP_TOP          
               48  POP_TOP          
               50  POP_EXCEPT       
               52  POP_TOP          
             54_0  COME_FROM            36  '36'

Parse error at or near `DUP_TOP' instruction at offset 28


@as_file.register(pathlib.Path)
@contextlib.contextmanager
def _(path):
    """
    Degenerate behavior for pathlib.Path objects.
    """
    yield path