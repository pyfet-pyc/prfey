# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: zipimport.py
"""zipimport provides support for importing Python modules from Zip archives.

This module exports three objects:
- zipimporter: a class; its constructor takes a path to a Zip archive.
- ZipImportError: exception raised by zipimporter objects. It's a
  subclass of ImportError, so it can be caught as ImportError, too.
- _zip_directory_cache: a dict, mapping archive paths to zip directory
  info dicts, as used in zipimporter._files.

It is usually not needed to use the zipimport module explicitly; it is
used by the builtin import mechanism for sys.path items that are paths
to Zip archives.
"""
import _frozen_importlib_external as _bootstrap_external
from _frozen_importlib_external import _unpack_uint16, _unpack_uint32
import _frozen_importlib as _bootstrap, _imp, _io, marshal, sys, time
__all__ = [
 'ZipImportError', 'zipimporter']
path_sep = _bootstrap_external.path_sep
alt_path_sep = _bootstrap_external.path_separators[1:]

class ZipImportError(ImportError):
    pass


_zip_directory_cache = {}
_module_type = type(sys)
END_CENTRAL_DIR_SIZE = 22
STRING_END_ARCHIVE = b'PK\x05\x06'
MAX_COMMENT_LEN = 65535

class zipimporter:
    __doc__ = "zipimporter(archivepath) -> zipimporter object\n\n    Create a new zipimporter instance. 'archivepath' must be a path to\n    a zipfile, or to a specific path inside a zipfile. For example, it can be\n    '/tmp/myimport.zip', or '/tmp/myimport.zip/mydirectory', if mydirectory is a\n    valid directory inside the archive.\n\n    'ZipImportError is raised if 'archivepath' doesn't point to a valid Zip\n    archive.\n\n    The 'archive' attribute of zipimporter objects contains the name of the\n    zipfile targeted.\n    "

    def __init__(self, path):
        if not isinstance(path, str):
            import os
            path = os.fsdecode(path)
        if not path:
            raise ZipImportError('archive path is empty', path=path)
        if alt_path_sep:
            path = path.replace(alt_path_sep, path_sep)
        prefix = []
        while True:
            try:
                st = _bootstrap_external._path_stat(path)
            except (OSError, ValueError):
                dirname, basename = _bootstrap_external._path_split(path)
                if dirname == path:
                    raise ZipImportError('not a Zip file', path=path)
                path = dirname
                prefix.append(basename)
            else:
                if st.st_mode & 61440 != 32768:
                    raise ZipImportError('not a Zip file', path=path)

        try:
            files = _zip_directory_cache[path]
        except KeyError:
            files = _read_directory(path)
            _zip_directory_cache[path] = files
        else:
            self._files = files
            self.archive = path
            self.prefix = (_bootstrap_external._path_join)(*prefix[::-1])
            if self.prefix:
                self.prefix += path_sep

    def find_loader(self, fullname, path=None):
        """find_loader(fullname, path=None) -> self, str or None.

        Search for a module specified by 'fullname'. 'fullname' must be the
        fully qualified (dotted) module name. It returns the zipimporter
        instance itself if the module was found, a string containing the
        full path name if it's possibly a portion of a namespace package,
        or None otherwise. The optional 'path' argument is ignored -- it's
        there for compatibility with the importer protocol.
        """
        mi = _get_module_info(self, fullname)
        if mi is not None:
            return (
             self, [])
        modpath = _get_module_path(self, fullname)
        if _is_dir(self, modpath):
            return (
             None, [f"{self.archive}{path_sep}{modpath}"])
        return (
         None, [])

    def find_module(self, fullname, path=None):
        """find_module(fullname, path=None) -> self or None.

        Search for a module specified by 'fullname'. 'fullname' must be the
        fully qualified (dotted) module name. It returns the zipimporter
        instance itself if the module was found, or None if it wasn't.
        The optional 'path' argument is ignored -- it's there for compatibility
        with the importer protocol.
        """
        return self.find_loader(fullname, path)[0]

    def get_code(self, fullname):
        """get_code(fullname) -> code object.

        Return the code object for the specified module. Raise ZipImportError
        if the module couldn't be found.
        """
        code, ispackage, modpath = _get_module_code(self, fullname)
        return code

    def get_data(self, pathname):
        """get_data(pathname) -> string with file data.

        Return the data associated with 'pathname'. Raise OSError if
        the file wasn't found.
        """
        if alt_path_sep:
            pathname = pathname.replace(alt_path_sep, path_sep)
        key = pathname
        if pathname.startswith(self.archive + path_sep):
            key = pathname[len(self.archive + path_sep):]
        try:
            toc_entry = self._files[key]
        except KeyError:
            raise OSError(0, '', key)
        else:
            return _get_data(self.archive, toc_entry)

    def get_filename(self, fullname):
        """get_filename(fullname) -> filename string.

        Return the filename for the specified module.
        """
        code, ispackage, modpath = _get_module_code(self, fullname)
        return modpath

    def get_source(self, fullname):
        """get_source(fullname) -> source string.

        Return the source code for the specified module. Raise ZipImportError
        if the module couldn't be found, return None if the archive does
        contain the module, but has no source for it.
        """
        mi = _get_module_info(self, fullname)
        if mi is None:
            raise ZipImportError(f"can't find module {fullname!r}", name=fullname)
        path = _get_module_path(self, fullname)
        if mi:
            fullpath = _bootstrap_external._path_join(path, '__init__.py')
        else:
            fullpath = f"{path}.py"
        try:
            toc_entry = self._files[fullpath]
        except KeyError:
            return
        else:
            return _get_data(self.archive, toc_entry).decode()

    def is_package(self, fullname):
        """is_package(fullname) -> bool.

        Return True if the module specified by fullname is a package.
        Raise ZipImportError if the module couldn't be found.
        """
        mi = _get_module_info(self, fullname)
        if mi is None:
            raise ZipImportError(f"can't find module {fullname!r}", name=fullname)
        return mi

    def load_module(self, fullname):
        """load_module(fullname) -> module.

        Load the module specified by 'fullname'. 'fullname' must be the
        fully qualified (dotted) module name. It returns the imported
        module, or raises ZipImportError if it wasn't found.
        """
        code, ispackage, modpath = _get_module_code(self, fullname)
        mod = sys.modules.get(fullname)
        if not (mod is None or isinstance(mod, _module_type)):
            mod = _module_type(fullname)
            sys.modules[fullname] = mod
        mod.__loader__ = self
        try:
            if ispackage:
                path = _get_module_path(self, fullname)
                fullpath = _bootstrap_external._path_join(self.archive, path)
                mod.__path__ = [fullpath]
            if not hasattr(mod, '__builtins__'):
                mod.__builtins__ = __builtins__
            _bootstrap_external._fix_up_module(mod.__dict__, fullname, modpath)
            exec(code, mod.__dict__)
        except:
            del sys.modules[fullname]
            raise
        else:
            try:
                mod = sys.modules[fullname]
            except KeyError:
                raise ImportError(f"Loaded module {fullname!r} not found in sys.modules")
            else:
                _bootstrap._verbose_message('import {} # loaded from Zip {}', fullname, modpath)
                return mod

    def get_resource_reader--- This code section failed: ---

 L. 278         0  SETUP_FINALLY        22  'to 22'

 L. 279         2  LOAD_FAST                'self'
                4  LOAD_METHOD              is_package
                6  LOAD_FAST                'fullname'
                8  CALL_METHOD_1         1  ''
               10  POP_JUMP_IF_TRUE     18  'to 18'

 L. 280        12  POP_BLOCK        
               14  LOAD_CONST               None
               16  RETURN_VALUE     
             18_0  COME_FROM            10  '10'
               18  POP_BLOCK        
               20  JUMP_FORWARD         44  'to 44'
             22_0  COME_FROM_FINALLY     0  '0'

 L. 281        22  DUP_TOP          
               24  LOAD_GLOBAL              ZipImportError
               26  COMPARE_OP               exception-match
               28  POP_JUMP_IF_FALSE    42  'to 42'
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L. 282        36  POP_EXCEPT       
               38  LOAD_CONST               None
               40  RETURN_VALUE     
             42_0  COME_FROM            28  '28'
               42  END_FINALLY      
             44_0  COME_FROM            20  '20'

 L. 283        44  LOAD_GLOBAL              _ZipImportResourceReader
               46  LOAD_ATTR                _registered
               48  POP_JUMP_IF_TRUE     78  'to 78'

 L. 284        50  LOAD_CONST               0
               52  LOAD_CONST               ('ResourceReader',)
               54  IMPORT_NAME_ATTR         importlib.abc
               56  IMPORT_FROM              ResourceReader
               58  STORE_FAST               'ResourceReader'
               60  POP_TOP          

 L. 285        62  LOAD_FAST                'ResourceReader'
               64  LOAD_METHOD              register
               66  LOAD_GLOBAL              _ZipImportResourceReader
               68  CALL_METHOD_1         1  ''
               70  POP_TOP          

 L. 286        72  LOAD_CONST               True
               74  LOAD_GLOBAL              _ZipImportResourceReader
               76  STORE_ATTR               _registered
             78_0  COME_FROM            48  '48'

 L. 287        78  LOAD_GLOBAL              _ZipImportResourceReader
               80  LOAD_FAST                'self'
               82  LOAD_FAST                'fullname'
               84  CALL_FUNCTION_2       2  ''
               86  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 14

    def __repr__(self):
        return f'<zipimporter object "{self.archive}{path_sep}{self.prefix}">'


_zip_searchorder = (
 (
  path_sep + '__init__.pyc', True, True),
 (
  path_sep + '__init__.py', False, True),
 ('.pyc', True, False),
 ('.py', False, False))

def _get_module_path(self, fullname):
    return self.prefix + fullname.rpartition('.')[2]


def _is_dir(self, path):
    dirpath = path + path_sep
    return dirpath in self._files


def _get_module_info(self, fullname):
    path = _get_module_path(self, fullname)
    for suffix, isbytecode, ispackage in _zip_searchorder:
        fullpath = path + suffix
        if fullpath in self._files:
            return ispackage


def _read_directory(archive):
    try:
        fp = _io.open_code(archive)
    except OSError:
        raise ZipImportError(f"can't open Zip file: {archive!r}", path=archive)
    else:
        with fp:
            try:
                fp.seek(-END_CENTRAL_DIR_SIZE, 2)
                header_position = fp.tell()
                buffer = fp.read(END_CENTRAL_DIR_SIZE)
            except OSError:
                raise ZipImportError(f"can't read Zip file: {archive!r}", path=archive)
            else:
                if len(buffer) != END_CENTRAL_DIR_SIZE:
                    raise ZipImportError(f"can't read Zip file: {archive!r}", path=archive)
                if buffer[:4] != STRING_END_ARCHIVE:
                    try:
                        fp.seek(0, 2)
                        file_size = fp.tell()
                    except OSError:
                        raise ZipImportError(f"can't read Zip file: {archive!r}", path=archive)
                    else:
                        max_comment_start = max(file_size - MAX_COMMENT_LEN - END_CENTRAL_DIR_SIZE, 0)
                        try:
                            fp.seek(max_comment_start)
                            data = fp.read()
                        except OSError:
                            raise ZipImportError(f"can't read Zip file: {archive!r}", path=archive)
                        else:
                            pos = data.rfind(STRING_END_ARCHIVE)
                            if pos < 0:
                                raise ZipImportError(f"not a Zip file: {archive!r}", path=archive)
                            buffer = data[pos:pos + END_CENTRAL_DIR_SIZE]
                            if len(buffer) != END_CENTRAL_DIR_SIZE:
                                raise ZipImportError(f"corrupt Zip file: {archive!r}", path=archive)
                            header_position = file_size - len(data) + pos
                        header_size = _unpack_uint32(buffer[12:16])
                        header_offset = _unpack_uint32(buffer[16:20])
                        if header_position < header_size:
                            raise ZipImportError(f"bad central directory size: {archive!r}", path=archive)
                        if header_position < header_offset:
                            raise ZipImportError(f"bad central directory offset: {archive!r}", path=archive)
                        header_position -= header_size
                        arc_offset = header_position - header_offset
                        if arc_offset < 0:
                            raise ZipImportError(f"bad central directory size or offset: {archive!r}", path=archive)
                files = {}
                count = 0
                try:
                    fp.seek(header_position)
                except OSError:
                    raise ZipImportError(f"can't read Zip file: {archive!r}", path=archive)
                else:
                    while True:
                        buffer = fp.read(46)
                        if len(buffer) < 4:
                            raise EOFError('EOF read where not expected')
                        if buffer[:4] != b'PK\x01\x02':
                            pass
                        else:
                            pass
                        if len(buffer) != 46:
                            raise EOFError('EOF read where not expected')
                        else:
                            flags = _unpack_uint16(buffer[8:10])
                            compress = _unpack_uint16(buffer[10:12])
                            time = _unpack_uint16(buffer[12:14])
                            date = _unpack_uint16(buffer[14:16])
                            crc = _unpack_uint32(buffer[16:20])
                            data_size = _unpack_uint32(buffer[20:24])
                            file_size = _unpack_uint32(buffer[24:28])
                            name_size = _unpack_uint16(buffer[28:30])
                            extra_size = _unpack_uint16(buffer[30:32])
                            comment_size = _unpack_uint16(buffer[32:34])
                            file_offset = _unpack_uint32(buffer[42:46])
                            header_size = name_size + extra_size + comment_size
                            if file_offset > header_offset:
                                raise ZipImportError(f"bad local header offset: {archive!r}", path=archive)
                            file_offset += arc_offset
                            try:
                                name = fp.read(name_size)
                            except OSError:
                                raise ZipImportError(f"can't read Zip file: {archive!r}", path=archive)
                            else:
                                if len(name) != name_size:
                                    raise ZipImportError(f"can't read Zip file: {archive!r}", path=archive)
                                try:
                                    if len(fp.read(header_size - name_size)) != header_size - name_size:
                                        raise ZipImportError(f"can't read Zip file: {archive!r}", path=archive)
                                except OSError:
                                    raise ZipImportError(f"can't read Zip file: {archive!r}", path=archive)
                                else:
                                    if flags & 2048:
                                        name = name.decode()
                                    else:
                                        pass
                                    try:
                                        name = name.decode('ascii')
                                    except UnicodeDecodeError:
                                        name = name.decode('latin1').translate(cp437_table)
                                    else:
                                        name = name.replace('/', path_sep)
                                        path = _bootstrap_external._path_join(archive, name)
                                        t = (path, compress, data_size, file_size, file_offset, time, date, crc)
                                        files[name] = t
                                        count += 1

        _bootstrap._verbose_message('zipimport: found {} names in {!r}', count, archive)
        return files


cp437_table = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7fÇüéâäàåçêëèïîìÄÅÉæÆôöòûùÿÖÜ¢£¥₧ƒáíóúñÑªº¿⌐¬½¼¡«»░▒▓│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀αßΓπΣσµτΦΘΩδ∞φε∩≡±≥≤⌠⌡÷≈°∙·√ⁿ²■\xa0'
_importing_zlib = False

def _get_decompress_func():
    global _importing_zlib
    if _importing_zlib:
        _bootstrap._verbose_message('zipimport: zlib UNAVAILABLE')
        raise ZipImportError("can't decompress data; zlib not available")
    _importing_zlib = True
    try:
        try:
            from zlib import decompress
        except Exception:
            _bootstrap._verbose_message('zipimport: zlib UNAVAILABLE')
            raise ZipImportError("can't decompress data; zlib not available")

    finally:
        _importing_zlib = False

    _bootstrap._verbose_message('zipimport: zlib available')
    return decompress


def _get_data(archive, toc_entry):
    datapath, compress, data_size, file_size, file_offset, time, date, crc = toc_entry
    if data_size < 0:
        raise ZipImportError('negative data size')
    with _io.open_code(archive) as fp:
        try:
            fp.seek(file_offset)
        except OSError:
            raise ZipImportError(f"can't read Zip file: {archive!r}", path=archive)
        else:
            buffer = fp.read(30)
            if len(buffer) != 30:
                raise EOFError('EOF read where not expected')
            if buffer[:4] != b'PK\x03\x04':
                raise ZipImportError(f"bad local file header: {archive!r}", path=archive)
            name_size = _unpack_uint16(buffer[26:28])
            extra_size = _unpack_uint16(buffer[28:30])
            header_size = 30 + name_size + extra_size
            file_offset += header_size
            try:
                fp.seek(file_offset)
            except OSError:
                raise ZipImportError(f"can't read Zip file: {archive!r}", path=archive)
            else:
                raw_data = fp.read(data_size)
                if len(raw_data) != data_size:
                    raise OSError("zipimport: can't read data")
    if compress == 0:
        return raw_data
    try:
        decompress = _get_decompress_func()
    except Exception:
        raise ZipImportError("can't decompress data; zlib not available")
    else:
        return decompress(raw_data, -15)


def _eq_mtime(t1, t2):
    return abs(t1 - t2) <= 1


def _unmarshal_code(self, pathname, fullpath, fullname, data):
    exc_details = {'name':fullname, 
     'path':fullpath}
    try:
        flags = _bootstrap_external._classify_pyc(data, fullname, exc_details)
    except ImportError:
        return
    else:
        hash_based = flags & 1 != 0
        if hash_based:
            check_source = flags & 2 != 0
            if _imp.check_hash_based_pycs != 'never':
                if check_source or (_imp.check_hash_based_pycs == 'always'):
                    source_bytes = _get_pyc_source(self, fullpath)
                    if source_bytes is not None:
                        source_hash = _imp.source_hash(_bootstrap_external._RAW_MAGIC_NUMBER, source_bytes)
                        try:
                            _bootstrap_external._validate_hash_pyc(data, source_hash, fullname, exc_details)
                        except ImportError:
                            return

                source_mtime, source_size = _get_mtime_and_size_of_source(self, fullpath)
                if source_mtime:
                    if not _eq_mtime(_unpack_uint32(data[8:12]), source_mtime) or _unpack_uint32(data[12:16]) != source_size:
                        _bootstrap._verbose_message(f"bytecode is stale for {fullname!r}")
                        return
            code = marshal.loads(data[16:])
            if not isinstance(code, _code_type):
                raise TypeError(f"compiled module {pathname!r} is not a code object")
            else:
                return code


_code_type = type(_unmarshal_code.__code__)

def _normalize_line_endings(source):
    source = source.replace(b'\r\n', b'\n')
    source = source.replace(b'\r', b'\n')
    return source


def _compile_source(pathname, source):
    source = _normalize_line_endings(source)
    return compile(source, pathname, 'exec', dont_inherit=True)


def _parse_dostime(d, t):
    return time.mktime((
     (d >> 9) + 1980,
     d >> 5 & 15,
     d & 31,
     t >> 11,
     t >> 5 & 63,
     (t & 31) * 2,
     -1, -1, -1))


def _get_mtime_and_size_of_source--- This code section failed: ---

 L. 665         0  SETUP_FINALLY        84  'to 84'

 L. 667         2  LOAD_FAST                'path'
                4  LOAD_CONST               -1
                6  LOAD_CONST               None
                8  BUILD_SLICE_2         2 
               10  BINARY_SUBSCR    
               12  LOAD_CONST               ('c', 'o')
               14  COMPARE_OP               in
               16  POP_JUMP_IF_TRUE     22  'to 22'
               18  LOAD_ASSERT              AssertionError
               20  RAISE_VARARGS_1       1  'exception instance'
             22_0  COME_FROM            16  '16'

 L. 668        22  LOAD_FAST                'path'
               24  LOAD_CONST               None
               26  LOAD_CONST               -1
               28  BUILD_SLICE_2         2 
               30  BINARY_SUBSCR    
               32  STORE_FAST               'path'

 L. 669        34  LOAD_FAST                'self'
               36  LOAD_ATTR                _files
               38  LOAD_FAST                'path'
               40  BINARY_SUBSCR    
               42  STORE_FAST               'toc_entry'

 L. 672        44  LOAD_FAST                'toc_entry'
               46  LOAD_CONST               5
               48  BINARY_SUBSCR    
               50  STORE_FAST               'time'

 L. 673        52  LOAD_FAST                'toc_entry'
               54  LOAD_CONST               6
               56  BINARY_SUBSCR    
               58  STORE_FAST               'date'

 L. 674        60  LOAD_FAST                'toc_entry'
               62  LOAD_CONST               3
               64  BINARY_SUBSCR    
               66  STORE_FAST               'uncompressed_size'

 L. 675        68  LOAD_GLOBAL              _parse_dostime
               70  LOAD_FAST                'date'
               72  LOAD_FAST                'time'
               74  CALL_FUNCTION_2       2  ''
               76  LOAD_FAST                'uncompressed_size'
               78  BUILD_TUPLE_2         2 
               80  POP_BLOCK        
               82  RETURN_VALUE     
             84_0  COME_FROM_FINALLY     0  '0'

 L. 676        84  DUP_TOP          
               86  LOAD_GLOBAL              KeyError
               88  LOAD_GLOBAL              IndexError
               90  LOAD_GLOBAL              TypeError
               92  BUILD_TUPLE_3         3 
               94  COMPARE_OP               exception-match
               96  POP_JUMP_IF_FALSE   110  'to 110'
               98  POP_TOP          
              100  POP_TOP          
              102  POP_TOP          

 L. 677       104  POP_EXCEPT       
              106  LOAD_CONST               (0, 0)
              108  RETURN_VALUE     
            110_0  COME_FROM            96  '96'
              110  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 106


def _get_pyc_source(self, path):
    assert path[-1:] in ('c', 'o')
    path = path[:-1]
    try:
        toc_entry = self._files[path]
    except KeyError:
        return
    else:
        return _get_data(self.archive, toc_entry)


def _get_module_code(self, fullname):
    path = _get_module_path(self, fullname)
    for suffix, isbytecode, ispackage in _zip_searchorder:
        fullpath = path + suffix
        _bootstrap._verbose_message('trying {}{}{}', (self.archive), path_sep, fullpath, verbosity=2)
        try:
            toc_entry = self._files[fullpath]
        except KeyError:
            pass
        else:
            modpath = toc_entry[0]
            data = _get_data(self.archive, toc_entry)
        if isbytecode:
            code = _unmarshal_code(self, modpath, fullpath, fullname, data)
        else:
            code = _compile_source(modpath, data)
        if code is None:
            pass
        else:
            modpath = toc_entry[0]
            return (
             code, ispackage, modpath)
    else:
        raise ZipImportError(f"can't find module {fullname!r}", name=fullname)


class _ZipImportResourceReader:
    __doc__ = 'Private class used to support ZipImport.get_resource_reader().\n\n    This class is allowed to reference all the innards and private parts of\n    the zipimporter.\n    '
    _registered = False

    def __init__(self, zipimporter, fullname):
        self.zipimporter = zipimporter
        self.fullname = fullname

    def open_resource(self, resource):
        fullname_as_path = self.fullname.replace('.', '/')
        path = f"{fullname_as_path}/{resource}"
        from io import BytesIO
        try:
            return BytesIO(self.zipimporter.get_data(path))
        except OSError:
            raise FileNotFoundError(path)

    def resource_path(self, resource):
        raise FileNotFoundError

    def is_resource(self, name):
        fullname_as_path = self.fullname.replace('.', '/')
        path = f"{fullname_as_path}/{name}"
        try:
            self.zipimporter.get_data(path)
        except OSError:
            return False
        else:
            return True

    def contents--- This code section failed: ---

 L. 770         0  LOAD_CONST               0
                2  LOAD_CONST               ('Path',)
                4  IMPORT_NAME              pathlib
                6  IMPORT_FROM              Path
                8  STORE_FAST               'Path'
               10  POP_TOP          

 L. 771        12  LOAD_FAST                'Path'
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                zipimporter
               18  LOAD_METHOD              get_filename
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                fullname
               24  CALL_METHOD_1         1  ''
               26  CALL_FUNCTION_1       1  ''
               28  STORE_FAST               'fullname_path'

 L. 772        30  LOAD_FAST                'fullname_path'
               32  LOAD_METHOD              relative_to
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                zipimporter
               38  LOAD_ATTR                archive
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'relative_path'

 L. 775        44  LOAD_FAST                'relative_path'
               46  LOAD_ATTR                name
               48  LOAD_STR                 '__init__.py'
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_TRUE     58  'to 58'
               54  LOAD_ASSERT              AssertionError
               56  RAISE_VARARGS_1       1  'exception instance'
             58_0  COME_FROM            52  '52'

 L. 776        58  LOAD_FAST                'relative_path'
               60  LOAD_ATTR                parent
               62  STORE_FAST               'package_path'

 L. 777        64  LOAD_GLOBAL              set
               66  CALL_FUNCTION_0       0  ''
               68  STORE_FAST               'subdirs_seen'

 L. 778        70  LOAD_FAST                'self'
               72  LOAD_ATTR                zipimporter
               74  LOAD_ATTR                _files
               76  GET_ITER         
             78_0  COME_FROM           180  '180'
             78_1  COME_FROM           162  '162'
             78_2  COME_FROM           154  '154'
             78_3  COME_FROM           118  '118'
               78  FOR_ITER            182  'to 182'
               80  STORE_FAST               'filename'

 L. 779        82  SETUP_FINALLY       102  'to 102'

 L. 780        84  LOAD_FAST                'Path'
               86  LOAD_FAST                'filename'
               88  CALL_FUNCTION_1       1  ''
               90  LOAD_METHOD              relative_to
               92  LOAD_FAST                'package_path'
               94  CALL_METHOD_1         1  ''
               96  STORE_FAST               'relative'
               98  POP_BLOCK        
              100  JUMP_FORWARD        126  'to 126'
            102_0  COME_FROM_FINALLY    82  '82'

 L. 781       102  DUP_TOP          
              104  LOAD_GLOBAL              ValueError
              106  COMPARE_OP               exception-match
              108  POP_JUMP_IF_FALSE   124  'to 124'
              110  POP_TOP          
              112  POP_TOP          
              114  POP_TOP          

 L. 782       116  POP_EXCEPT       
              118  JUMP_BACK            78  'to 78'
              120  POP_EXCEPT       
              122  JUMP_FORWARD        126  'to 126'
            124_0  COME_FROM           108  '108'
              124  END_FINALLY      
            126_0  COME_FROM           122  '122'
            126_1  COME_FROM           100  '100'

 L. 787       126  LOAD_FAST                'relative'
              128  LOAD_ATTR                parent
              130  LOAD_ATTR                name
              132  STORE_FAST               'parent_name'

 L. 788       134  LOAD_GLOBAL              len
              136  LOAD_FAST                'parent_name'
              138  CALL_FUNCTION_1       1  ''
              140  LOAD_CONST               0
              142  COMPARE_OP               ==
              144  POP_JUMP_IF_FALSE   156  'to 156'

 L. 789       146  LOAD_FAST                'relative'
              148  LOAD_ATTR                name
              150  YIELD_VALUE      
              152  POP_TOP          
              154  JUMP_BACK            78  'to 78'
            156_0  COME_FROM           144  '144'

 L. 790       156  LOAD_FAST                'parent_name'
              158  LOAD_FAST                'subdirs_seen'
              160  COMPARE_OP               not-in
              162  POP_JUMP_IF_FALSE_BACK    78  'to 78'

 L. 791       164  LOAD_FAST                'subdirs_seen'
              166  LOAD_METHOD              add
              168  LOAD_FAST                'parent_name'
              170  CALL_METHOD_1         1  ''
              172  POP_TOP          

 L. 792       174  LOAD_FAST                'parent_name'
              176  YIELD_VALUE      
              178  POP_TOP          
              180  JUMP_BACK            78  'to 78'
            182_0  COME_FROM            78  '78'

Parse error at or near `COME_FROM' instruction at offset 124_0