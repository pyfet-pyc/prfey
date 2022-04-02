# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
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


def open_binary(package: Package, resource: Resource) -> BinaryIO:
    """Return a file-like object opened for binary reading of the resource."""
    resource = _normalize_path(resource)
    package = _get_package(package)
    reader = _get_resource_reader(package)
    if reader is not None:
        return reader.open_resource(resource)
    _check_location(package)
    absolute_package_path = os.path.abspath(package.__spec__.origin)
    package_path = os.path.dirname(absolute_package_path)
    full_path = os.path.join(package_path, resource)
    try:
        return open(full_path, mode='rb')
    except OSError:
        loader = cast(ResourceLoader, package.__spec__.loader)
        data = None
        if hasattr(package.__spec__.loader, 'get_data'):
            with suppress(OSError):
                data = loader.get_data(full_path)
        if data is None:
            package_name = package.__spec__.name
            message = '{!r} resource not found in {!r}'.format(resource, package_name)
            raise FileNotFoundError(message)
        else:
            return BytesIO(data)


def open_text(package: Package, resource: Resource, encoding: str='utf-8', errors: str='strict') -> TextIO:
    """Return a file-like object opened for text reading of the resource."""
    resource = _normalize_path(resource)
    package = _get_package(package)
    reader = _get_resource_reader(package)
    if reader is not None:
        return TextIOWrapper(reader.open_resource(resource), encoding, errors)
    _check_location(package)
    absolute_package_path = os.path.abspath(package.__spec__.origin)
    package_path = os.path.dirname(absolute_package_path)
    full_path = os.path.join(package_path, resource)
    try:
        return open(full_path, mode='r', encoding=encoding, errors=errors)
    except OSError:
        loader = cast(ResourceLoader, package.__spec__.loader)
        data = None
        if hasattr(package.__spec__.loader, 'get_data'):
            with suppress(OSError):
                data = loader.get_data(full_path)
        if data is None:
            package_name = package.__spec__.name
            message = '{!r} resource not found in {!r}'.format(resource, package_name)
            raise FileNotFoundError(message)
        else:
            return TextIOWrapper(BytesIO(data), encoding, errors)


def read_binary(package: Package, resource: Resource) -> bytes:
    """Return the binary contents of the resource."""
    resource = _normalize_path(resource)
    package = _get_package(package)
    with open_binary(package, resource) as fp:
        return fp.read()


def read_text(package: Package, resource: Resource, encoding: str='utf-8', errors: str='strict') -> str:
    """Return the decoded string of the resource.

    The decoding-related arguments have the same semantics as those of
    bytes.decode().
    """
    resource = _normalize_path(resource)
    package = _get_package(package)
    with open_text(package, resource, encoding, errors) as fp:
        return fp.read()


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
               72  JUMP_FORWARD         86  'to 86'
             74_0  COME_FROM            62  '62'
               74  END_FINALLY      
               76  JUMP_FORWARD         86  'to 86'
             78_0  COME_FROM            30  '30'

 L. 193        78  LOAD_GLOBAL              _check_location
               80  LOAD_FAST                'package'
               82  CALL_FUNCTION_1       1  ''
               84  POP_TOP          
             86_0  COME_FROM            76  '76'
             86_1  COME_FROM            72  '72'

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

Parse error at or near `DUP_TOP' instruction at offset 56


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
        else:
            path = Path(package.__spec__.origin).parent / name
            return path.is_file()


def contents(package: Package) -> Iterable[str]:
    """Return an iterable of entries in 'package'.

    Note that not all entries are resources.  Specifically, directories are
    not considered resources.  Use `is_resource()` on each entry returned here
    to check if it is a resource or not.
    """
    package = _get_package(package)
    reader = _get_resource_reader(package)
    if reader is not None:
        return reader.contents()
    if not (package.__spec__.origin is None or package.__spec__.has_location):
        return ()
    package_directory = Path(package.__spec__.origin).parent
    return os.listdir(package_directory)