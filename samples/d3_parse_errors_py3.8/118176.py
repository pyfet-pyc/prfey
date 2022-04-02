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

 L. 196        86  LOAD_GLOBAL              Path
               88  LOAD_FAST                'package'
               90  LOAD_ATTR                __spec__
               92  LOAD_ATTR                origin
               94  CALL_FUNCTION_1       1  ''
               96  LOAD_ATTR                parent
               98  STORE_FAST               'package_directory'

 L. 197       100  LOAD_FAST                'package_directory'
              102  LOAD_FAST                'resource'
              104  BINARY_TRUE_DIVIDE
              106  STORE_FAST               'file_path'

 L. 198       108  LOAD_FAST                'file_path'
              110  LOAD_METHOD              exists
              112  CALL_METHOD_0         0  ''
              114  POP_JUMP_IF_FALSE   124  'to 124'

 L. 199       116  LOAD_FAST                'file_path'
              118  YIELD_VALUE      
              120  POP_TOP          
              122  JUMP_FORWARD        242  'to 242'
            124_0  COME_FROM           114  '114'

 L. 201       124  LOAD_GLOBAL              open_binary
              126  LOAD_FAST                'package'
              128  LOAD_FAST                'resource'
              130  CALL_FUNCTION_2       2  ''
              132  SETUP_WITH          148  'to 148'
              134  STORE_FAST               'fp'

 L. 202       136  LOAD_FAST                'fp'
              138  LOAD_METHOD              read
              140  CALL_METHOD_0         0  ''
              142  STORE_FAST               'data'
              144  POP_BLOCK        
              146  BEGIN_FINALLY    
            148_0  COME_FROM_WITH      132  '132'
              148  WITH_CLEANUP_START
              150  WITH_CLEANUP_FINISH
              152  END_FINALLY      

 L. 206       154  LOAD_GLOBAL              tempfile
              156  LOAD_METHOD              mkstemp
              158  CALL_METHOD_0         0  ''
              160  UNPACK_SEQUENCE_2     2 
              162  STORE_FAST               'fd'
              164  STORE_FAST               'raw_path'

 L. 207       166  SETUP_FINALLY       204  'to 204'

 L. 208       168  LOAD_GLOBAL              os
              170  LOAD_METHOD              write
              172  LOAD_FAST                'fd'
              174  LOAD_FAST                'data'
              176  CALL_METHOD_2         2  ''
              178  POP_TOP          

 L. 209       180  LOAD_GLOBAL              os
              182  LOAD_METHOD              close
              184  LOAD_FAST                'fd'
              186  CALL_METHOD_1         1  ''
              188  POP_TOP          

 L. 210       190  LOAD_GLOBAL              Path
              192  LOAD_FAST                'raw_path'
              194  CALL_FUNCTION_1       1  ''
              196  YIELD_VALUE      
              198  POP_TOP          
              200  POP_BLOCK        
              202  BEGIN_FINALLY    
            204_0  COME_FROM_FINALLY   166  '166'

 L. 212       204  SETUP_FINALLY       220  'to 220'

 L. 213       206  LOAD_GLOBAL              os
              208  LOAD_METHOD              remove
              210  LOAD_FAST                'raw_path'
              212  CALL_METHOD_1         1  ''
              214  POP_TOP          
              216  POP_BLOCK        
              218  JUMP_FORWARD        240  'to 240'
            220_0  COME_FROM_FINALLY   204  '204'

 L. 214       220  DUP_TOP          
              222  LOAD_GLOBAL              FileNotFoundError
              224  COMPARE_OP               exception-match
              226  POP_JUMP_IF_FALSE   238  'to 238'
              228  POP_TOP          
              230  POP_TOP          
              232  POP_TOP          

 L. 215       234  POP_EXCEPT       
              236  JUMP_FORWARD        240  'to 240'
            238_0  COME_FROM           226  '226'
              238  END_FINALLY      
            240_0  COME_FROM           236  '236'
            240_1  COME_FROM           218  '218'
              240  END_FINALLY      
            242_0  COME_FROM           122  '122'

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