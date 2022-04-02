# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: importlib\resources.py
import os, tempfile
from . import abc as resources_abc
from contextlib import contextmanager, suppress
from importlib import import_module
from importlib.abc import ResourceLoader
from io import BytesIO, TextIOWrapper
from pathlib import Path
from types import ModuleType
from typing import Iterable, Iterator, Optional, Set, Union
from typing import cast
from typing.io import BinaryIO, TextIO
from zipimport import ZipImportError
__all__ = [
 'Package',
 'Resource',
 'contents',
 'is_resource',
 'open_binary',
 'open_text',
 'path',
 'read_binary',
 'read_text']
Package = Union[(str, ModuleType)]
Resource = Union[(str, os.PathLike)]

def _get_package(package) -> ModuleType:
    """Take a package name or module object and return the module.

    If a name, the module is imported.  If the passed or imported module
    object is not a package, raise an exception.
    """
    if hasattr(package, '__spec__'):
        if package.__spec__.submodule_search_locations is None:
            raise TypeError('{!r} is not a package'.format(package.__spec__.name))
        else:
            return package
    else:
        module = import_module(package)
        if module.__spec__.submodule_search_locations is None:
            raise TypeError('{!r} is not a package'.format(package))
        else:
            return module


def _normalize_path(path) -> str:
    """Normalize a path by ensuring it is a string.

    If the resulting string contains path separators, an exception is raised.
    """
    parent, file_name = os.path.split(path)
    if parent:
        raise ValueError('{!r} must be only a file name'.format(path))
    else:
        return file_name


def _get_resource_reader(package: ModuleType) -> Optional[resources_abc.ResourceReader]:
    spec = package.__spec__
    if hasattr(spec.loader, 'get_resource_reader'):
        return cast(resources_abc.ResourceReader, spec.loader.get_resource_reader(spec.name))


def _check_location(package):
    if not (package.__spec__.origin is None or package.__spec__.has_location):
        raise FileNotFoundError(f"Package has no location {package!r}")


def open_binary--- This code section failed: ---

 L.  87         0  LOAD_GLOBAL              _normalize_path
                2  LOAD_FAST                'resource'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'resource'

 L.  88         8  LOAD_GLOBAL              _get_package
               10  LOAD_FAST                'package'
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'package'

 L.  89        16  LOAD_GLOBAL              _get_resource_reader
               18  LOAD_FAST                'package'
               20  CALL_FUNCTION_1       1  ''
               22  STORE_FAST               'reader'

 L.  90        24  LOAD_FAST                'reader'
               26  LOAD_CONST               None
               28  COMPARE_OP               is-not
               30  POP_JUMP_IF_FALSE    42  'to 42'

 L.  91        32  LOAD_FAST                'reader'
               34  LOAD_METHOD              open_resource
               36  LOAD_FAST                'resource'
               38  CALL_METHOD_1         1  ''
               40  RETURN_VALUE     
             42_0  COME_FROM            30  '30'

 L.  92        42  LOAD_GLOBAL              _check_location
               44  LOAD_FAST                'package'
               46  CALL_FUNCTION_1       1  ''
               48  POP_TOP          

 L.  93        50  LOAD_GLOBAL              os
               52  LOAD_ATTR                path
               54  LOAD_METHOD              abspath
               56  LOAD_FAST                'package'
               58  LOAD_ATTR                __spec__
               60  LOAD_ATTR                origin
               62  CALL_METHOD_1         1  ''
               64  STORE_FAST               'absolute_package_path'

 L.  94        66  LOAD_GLOBAL              os
               68  LOAD_ATTR                path
               70  LOAD_METHOD              dirname
               72  LOAD_FAST                'absolute_package_path'
               74  CALL_METHOD_1         1  ''
               76  STORE_FAST               'package_path'

 L.  95        78  LOAD_GLOBAL              os
               80  LOAD_ATTR                path
               82  LOAD_METHOD              join
               84  LOAD_FAST                'package_path'
               86  LOAD_FAST                'resource'
               88  CALL_METHOD_2         2  ''
               90  STORE_FAST               'full_path'

 L.  96        92  SETUP_FINALLY       108  'to 108'

 L.  97        94  LOAD_GLOBAL              open
               96  LOAD_FAST                'full_path'
               98  LOAD_STR                 'rb'
              100  LOAD_CONST               ('mode',)
              102  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              104  POP_BLOCK        
              106  RETURN_VALUE     
            108_0  COME_FROM_FINALLY    92  '92'

 L.  98       108  DUP_TOP          
              110  LOAD_GLOBAL              OSError
              112  COMPARE_OP               exception-match
              114  POP_JUMP_IF_FALSE   238  'to 238'
              116  POP_TOP          
              118  POP_TOP          
              120  POP_TOP          

 L. 102       122  LOAD_GLOBAL              cast
              124  LOAD_GLOBAL              ResourceLoader
              126  LOAD_FAST                'package'
              128  LOAD_ATTR                __spec__
              130  LOAD_ATTR                loader
              132  CALL_FUNCTION_2       2  ''
              134  STORE_FAST               'loader'

 L. 103       136  LOAD_CONST               None
              138  STORE_FAST               'data'

 L. 104       140  LOAD_GLOBAL              hasattr
              142  LOAD_FAST                'package'
              144  LOAD_ATTR                __spec__
              146  LOAD_ATTR                loader
              148  LOAD_STR                 'get_data'
              150  CALL_FUNCTION_2       2  ''
              152  POP_JUMP_IF_FALSE   184  'to 184'

 L. 105       154  LOAD_GLOBAL              suppress
              156  LOAD_GLOBAL              OSError
              158  CALL_FUNCTION_1       1  ''
              160  SETUP_WITH          178  'to 178'
              162  POP_TOP          

 L. 106       164  LOAD_FAST                'loader'
              166  LOAD_METHOD              get_data
              168  LOAD_FAST                'full_path'
              170  CALL_METHOD_1         1  ''
              172  STORE_FAST               'data'
              174  POP_BLOCK        
              176  BEGIN_FINALLY    
            178_0  COME_FROM_WITH      160  '160'
              178  WITH_CLEANUP_START
              180  WITH_CLEANUP_FINISH
              182  END_FINALLY      
            184_0  COME_FROM           152  '152'

 L. 107       184  LOAD_FAST                'data'
              186  LOAD_CONST               None
              188  COMPARE_OP               is
              190  POP_JUMP_IF_FALSE   222  'to 222'

 L. 108       192  LOAD_FAST                'package'
              194  LOAD_ATTR                __spec__
              196  LOAD_ATTR                name
              198  STORE_FAST               'package_name'

 L. 109       200  LOAD_STR                 '{!r} resource not found in {!r}'
              202  LOAD_METHOD              format

 L. 110       204  LOAD_FAST                'resource'

 L. 110       206  LOAD_FAST                'package_name'

 L. 109       208  CALL_METHOD_2         2  ''
              210  STORE_FAST               'message'

 L. 111       212  LOAD_GLOBAL              FileNotFoundError
              214  LOAD_FAST                'message'
              216  CALL_FUNCTION_1       1  ''
              218  RAISE_VARARGS_1       1  'exception instance'
              220  JUMP_FORWARD        234  'to 234'
            222_0  COME_FROM           190  '190'

 L. 113       222  LOAD_GLOBAL              BytesIO
              224  LOAD_FAST                'data'
              226  CALL_FUNCTION_1       1  ''
              228  ROT_FOUR         
              230  POP_EXCEPT       
              232  RETURN_VALUE     
            234_0  COME_FROM           220  '220'
              234  POP_EXCEPT       
              236  JUMP_FORWARD        240  'to 240'
            238_0  COME_FROM           114  '114'
              238  END_FINALLY      
            240_0  COME_FROM           236  '236'

Parse error at or near `POP_TOP' instruction at offset 118


def open_text--- This code section failed: ---

 L. 121         0  LOAD_GLOBAL              _normalize_path
                2  LOAD_FAST                'resource'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'resource'

 L. 122         8  LOAD_GLOBAL              _get_package
               10  LOAD_FAST                'package'
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'package'

 L. 123        16  LOAD_GLOBAL              _get_resource_reader
               18  LOAD_FAST                'package'
               20  CALL_FUNCTION_1       1  ''
               22  STORE_FAST               'reader'

 L. 124        24  LOAD_FAST                'reader'
               26  LOAD_CONST               None
               28  COMPARE_OP               is-not
               30  POP_JUMP_IF_FALSE    50  'to 50'

 L. 125        32  LOAD_GLOBAL              TextIOWrapper
               34  LOAD_FAST                'reader'
               36  LOAD_METHOD              open_resource
               38  LOAD_FAST                'resource'
               40  CALL_METHOD_1         1  ''
               42  LOAD_FAST                'encoding'
               44  LOAD_FAST                'errors'
               46  CALL_FUNCTION_3       3  ''
               48  RETURN_VALUE     
             50_0  COME_FROM            30  '30'

 L. 126        50  LOAD_GLOBAL              _check_location
               52  LOAD_FAST                'package'
               54  CALL_FUNCTION_1       1  ''
               56  POP_TOP          

 L. 127        58  LOAD_GLOBAL              os
               60  LOAD_ATTR                path
               62  LOAD_METHOD              abspath
               64  LOAD_FAST                'package'
               66  LOAD_ATTR                __spec__
               68  LOAD_ATTR                origin
               70  CALL_METHOD_1         1  ''
               72  STORE_FAST               'absolute_package_path'

 L. 128        74  LOAD_GLOBAL              os
               76  LOAD_ATTR                path
               78  LOAD_METHOD              dirname
               80  LOAD_FAST                'absolute_package_path'
               82  CALL_METHOD_1         1  ''
               84  STORE_FAST               'package_path'

 L. 129        86  LOAD_GLOBAL              os
               88  LOAD_ATTR                path
               90  LOAD_METHOD              join
               92  LOAD_FAST                'package_path'
               94  LOAD_FAST                'resource'
               96  CALL_METHOD_2         2  ''
               98  STORE_FAST               'full_path'

 L. 130       100  SETUP_FINALLY       120  'to 120'

 L. 131       102  LOAD_GLOBAL              open
              104  LOAD_FAST                'full_path'
              106  LOAD_STR                 'r'
              108  LOAD_FAST                'encoding'
              110  LOAD_FAST                'errors'
              112  LOAD_CONST               ('mode', 'encoding', 'errors')
              114  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              116  POP_BLOCK        
              118  RETURN_VALUE     
            120_0  COME_FROM_FINALLY   100  '100'

 L. 132       120  DUP_TOP          
              122  LOAD_GLOBAL              OSError
              124  COMPARE_OP               exception-match
          126_128  POP_JUMP_IF_FALSE   260  'to 260'
              130  POP_TOP          
              132  POP_TOP          
              134  POP_TOP          

 L. 136       136  LOAD_GLOBAL              cast
              138  LOAD_GLOBAL              ResourceLoader
              140  LOAD_FAST                'package'
              142  LOAD_ATTR                __spec__
              144  LOAD_ATTR                loader
              146  CALL_FUNCTION_2       2  ''
              148  STORE_FAST               'loader'

 L. 137       150  LOAD_CONST               None
              152  STORE_FAST               'data'

 L. 138       154  LOAD_GLOBAL              hasattr
              156  LOAD_FAST                'package'
              158  LOAD_ATTR                __spec__
              160  LOAD_ATTR                loader
              162  LOAD_STR                 'get_data'
              164  CALL_FUNCTION_2       2  ''
              166  POP_JUMP_IF_FALSE   198  'to 198'

 L. 139       168  LOAD_GLOBAL              suppress
              170  LOAD_GLOBAL              OSError
              172  CALL_FUNCTION_1       1  ''
              174  SETUP_WITH          192  'to 192'
              176  POP_TOP          

 L. 140       178  LOAD_FAST                'loader'
              180  LOAD_METHOD              get_data
              182  LOAD_FAST                'full_path'
              184  CALL_METHOD_1         1  ''
              186  STORE_FAST               'data'
              188  POP_BLOCK        
              190  BEGIN_FINALLY    
            192_0  COME_FROM_WITH      174  '174'
              192  WITH_CLEANUP_START
              194  WITH_CLEANUP_FINISH
              196  END_FINALLY      
            198_0  COME_FROM           166  '166'

 L. 141       198  LOAD_FAST                'data'
              200  LOAD_CONST               None
              202  COMPARE_OP               is
              204  POP_JUMP_IF_FALSE   236  'to 236'

 L. 142       206  LOAD_FAST                'package'
              208  LOAD_ATTR                __spec__
              210  LOAD_ATTR                name
              212  STORE_FAST               'package_name'

 L. 143       214  LOAD_STR                 '{!r} resource not found in {!r}'
              216  LOAD_METHOD              format

 L. 144       218  LOAD_FAST                'resource'

 L. 144       220  LOAD_FAST                'package_name'

 L. 143       222  CALL_METHOD_2         2  ''
              224  STORE_FAST               'message'

 L. 145       226  LOAD_GLOBAL              FileNotFoundError
              228  LOAD_FAST                'message'
              230  CALL_FUNCTION_1       1  ''
              232  RAISE_VARARGS_1       1  'exception instance'
              234  JUMP_FORWARD        256  'to 256'
            236_0  COME_FROM           204  '204'

 L. 147       236  LOAD_GLOBAL              TextIOWrapper
              238  LOAD_GLOBAL              BytesIO
              240  LOAD_FAST                'data'
              242  CALL_FUNCTION_1       1  ''
              244  LOAD_FAST                'encoding'
              246  LOAD_FAST                'errors'
              248  CALL_FUNCTION_3       3  ''
              250  ROT_FOUR         
              252  POP_EXCEPT       
              254  RETURN_VALUE     
            256_0  COME_FROM           234  '234'
              256  POP_EXCEPT       
              258  JUMP_FORWARD        262  'to 262'
            260_0  COME_FROM           126  '126'
              260  END_FINALLY      
            262_0  COME_FROM           258  '258'

Parse error at or near `POP_TOP' instruction at offset 132


def read_binary--- This code section failed: ---

 L. 152         0  LOAD_GLOBAL              _normalize_path
                2  LOAD_FAST                'resource'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'resource'

 L. 153         8  LOAD_GLOBAL              _get_package
               10  LOAD_FAST                'package'
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'package'

 L. 154        16  LOAD_GLOBAL              open_binary
               18  LOAD_FAST                'package'
               20  LOAD_FAST                'resource'
               22  CALL_FUNCTION_2       2  ''
               24  SETUP_WITH           48  'to 48'
               26  STORE_FAST               'fp'

 L. 155        28  LOAD_FAST                'fp'
               30  LOAD_METHOD              read
               32  CALL_METHOD_0         0  ''
               34  POP_BLOCK        
               36  ROT_TWO          
               38  BEGIN_FINALLY    
               40  WITH_CLEANUP_START
               42  WITH_CLEANUP_FINISH
               44  POP_FINALLY           0  ''
               46  RETURN_VALUE     
             48_0  COME_FROM_WITH       24  '24'
               48  WITH_CLEANUP_START
               50  WITH_CLEANUP_FINISH
               52  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 36


def read_text--- This code section failed: ---

 L. 167         0  LOAD_GLOBAL              _normalize_path
                2  LOAD_FAST                'resource'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'resource'

 L. 168         8  LOAD_GLOBAL              _get_package
               10  LOAD_FAST                'package'
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'package'

 L. 169        16  LOAD_GLOBAL              open_text
               18  LOAD_FAST                'package'
               20  LOAD_FAST                'resource'
               22  LOAD_FAST                'encoding'
               24  LOAD_FAST                'errors'
               26  CALL_FUNCTION_4       4  ''
               28  SETUP_WITH           52  'to 52'
               30  STORE_FAST               'fp'

 L. 170        32  LOAD_FAST                'fp'
               34  LOAD_METHOD              read
               36  CALL_METHOD_0         0  ''
               38  POP_BLOCK        
               40  ROT_TWO          
               42  BEGIN_FINALLY    
               44  WITH_CLEANUP_START
               46  WITH_CLEANUP_FINISH
               48  POP_FINALLY           0  ''
               50  RETURN_VALUE     
             52_0  COME_FROM_WITH       28  '28'
               52  WITH_CLEANUP_START
               54  WITH_CLEANUP_FINISH
               56  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 40


@contextmanager
def path--- This code section failed: ---

 L. 183         0  LOAD_GLOBAL              _normalize_path
                2  LOAD_FAST                'resource'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'resource'

 L. 184         8  LOAD_GLOBAL              _get_package
               10  LOAD_FAST                'package'
               12  CALL_FUNCTION_1       1  ''
               14  STORE_FAST               'package'

 L. 185        16  LOAD_GLOBAL              _get_resource_reader
               18  LOAD_FAST                'package'
               20  CALL_FUNCTION_1       1  ''
               22  STORE_FAST               'reader'

 L. 186        24  LOAD_FAST                'reader'
               26  LOAD_CONST               None
               28  COMPARE_OP               is-not
               30  POP_JUMP_IF_FALSE    78  'to 78'

 L. 187        32  SETUP_FINALLY        56  'to 56'

 L. 188        34  LOAD_GLOBAL              Path
               36  LOAD_FAST                'reader'
               38  LOAD_METHOD              resource_path
               40  LOAD_FAST                'resource'
               42  CALL_METHOD_1         1  ''
               44  CALL_FUNCTION_1       1  ''
               46  YIELD_VALUE      
               48  POP_TOP          

 L. 189        50  POP_BLOCK        
               52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM_FINALLY    32  '32'

 L. 190        56  DUP_TOP          
               58  LOAD_GLOBAL              FileNotFoundError
               60  COMPARE_OP               exception-match
               62  POP_JUMP_IF_FALSE    74  'to 74'
               64  POP_TOP          
               66  POP_TOP          
               68  POP_TOP          

 L. 191        70  POP_EXCEPT       
               72  JUMP_ABSOLUTE        86  'to 86'
             74_0  COME_FROM            62  '62'
               74  END_FINALLY      
               76  JUMP_FORWARD         86  'to 86'
             78_0  COME_FROM            30  '30'

 L. 193        78  LOAD_GLOBAL              _check_location
               80  LOAD_FAST                'package'
               82  CALL_FUNCTION_1       1  ''
               84  POP_TOP          
             86_0  COME_FROM            76  '76'

 L. 196        86  LOAD_CONST               None
               88  STORE_FAST               'file_path'

 L. 197        90  LOAD_FAST                'package'
               92  LOAD_ATTR                __spec__
               94  LOAD_ATTR                origin
               96  LOAD_CONST               None
               98  COMPARE_OP               is-not
              100  POP_JUMP_IF_FALSE   124  'to 124'

 L. 198       102  LOAD_GLOBAL              Path
              104  LOAD_FAST                'package'
              106  LOAD_ATTR                __spec__
              108  LOAD_ATTR                origin
              110  CALL_FUNCTION_1       1  ''
              112  LOAD_ATTR                parent
              114  STORE_FAST               'package_directory'

 L. 199       116  LOAD_FAST                'package_directory'
              118  LOAD_FAST                'resource'
              120  BINARY_TRUE_DIVIDE
              122  STORE_FAST               'file_path'
            124_0  COME_FROM           100  '100'

 L. 200       124  LOAD_FAST                'file_path'
              126  LOAD_CONST               None
              128  COMPARE_OP               is-not
              130  POP_JUMP_IF_FALSE   148  'to 148'
              132  LOAD_FAST                'file_path'
              134  LOAD_METHOD              exists
              136  CALL_METHOD_0         0  ''
              138  POP_JUMP_IF_FALSE   148  'to 148'

 L. 201       140  LOAD_FAST                'file_path'
              142  YIELD_VALUE      
              144  POP_TOP          
              146  JUMP_FORWARD        268  'to 268'
            148_0  COME_FROM           138  '138'
            148_1  COME_FROM           130  '130'

 L. 203       148  LOAD_GLOBAL              open_binary
              150  LOAD_FAST                'package'
              152  LOAD_FAST                'resource'
              154  CALL_FUNCTION_2       2  ''
              156  SETUP_WITH          172  'to 172'
              158  STORE_FAST               'fp'

 L. 204       160  LOAD_FAST                'fp'
              162  LOAD_METHOD              read
              164  CALL_METHOD_0         0  ''
              166  STORE_FAST               'data'
              168  POP_BLOCK        
              170  BEGIN_FINALLY    
            172_0  COME_FROM_WITH      156  '156'
              172  WITH_CLEANUP_START
              174  WITH_CLEANUP_FINISH
              176  END_FINALLY      

 L. 208       178  LOAD_GLOBAL              tempfile
              180  LOAD_METHOD              mkstemp
              182  CALL_METHOD_0         0  ''
              184  UNPACK_SEQUENCE_2     2 
              186  STORE_FAST               'fd'
              188  STORE_FAST               'raw_path'

 L. 209       190  SETUP_FINALLY       228  'to 228'

 L. 210       192  LOAD_GLOBAL              os
              194  LOAD_METHOD              write
              196  LOAD_FAST                'fd'
              198  LOAD_FAST                'data'
              200  CALL_METHOD_2         2  ''
              202  POP_TOP          

 L. 211       204  LOAD_GLOBAL              os
              206  LOAD_METHOD              close
              208  LOAD_FAST                'fd'
              210  CALL_METHOD_1         1  ''
              212  POP_TOP          

 L. 212       214  LOAD_GLOBAL              Path
              216  LOAD_FAST                'raw_path'
              218  CALL_FUNCTION_1       1  ''
              220  YIELD_VALUE      
              222  POP_TOP          
              224  POP_BLOCK        
              226  BEGIN_FINALLY    
            228_0  COME_FROM_FINALLY   190  '190'

 L. 214       228  SETUP_FINALLY       244  'to 244'

 L. 215       230  LOAD_GLOBAL              os
              232  LOAD_METHOD              remove
              234  LOAD_FAST                'raw_path'
              236  CALL_METHOD_1         1  ''
              238  POP_TOP          
              240  POP_BLOCK        
              242  JUMP_FORWARD        266  'to 266'
            244_0  COME_FROM_FINALLY   228  '228'

 L. 216       244  DUP_TOP          
              246  LOAD_GLOBAL              FileNotFoundError
              248  COMPARE_OP               exception-match
          250_252  POP_JUMP_IF_FALSE   264  'to 264'
              254  POP_TOP          
              256  POP_TOP          
              258  POP_TOP          

 L. 217       260  POP_EXCEPT       
              262  JUMP_FORWARD        266  'to 266'
            264_0  COME_FROM           250  '250'
              264  END_FINALLY      
            266_0  COME_FROM           262  '262'
            266_1  COME_FROM           242  '242'
              266  END_FINALLY      
            268_0  COME_FROM           146  '146'

Parse error at or near `RETURN_VALUE' instruction at offset 54


def is_resource(package: Package, name: str) -> bool:
    """True if 'name' is a resource inside 'package'.

    Directories are *not* resources.
    """
    package = _get_package(package)
    _normalize_path(name)
    reader = _get_resource_reader(package)
    if reader is not None:
        return reader.is_resource(name)
    try:
        package_contents = set(contents(package))
    except (NotADirectoryError, FileNotFoundError):
        return False
    else:
        if name not in package_contents:
            return False
        path = Path(package.__spec__.origin).parent / name
        return path.is_file


def contents(package: Package) -> Iterable[str]:
    """Return an iterable of entries in 'package'.

    Note that not all entries are resources.  Specifically, directories are
    not considered resources.  Use `is_resource()` on each entry returned here
    to check if it is a resource or not.
    """
    package = _get_package(package)
    reader = _get_resource_reader(package)
    if reader is not None:
        return reader.contents
    else:
        return package.__spec__.origin is None or package.__spec__.has_location or ()
    package_directory = Path(package.__spec__.origin).parent
    return os.listdir(package_directory)