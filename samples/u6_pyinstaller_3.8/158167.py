# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: cffi\verifier.py
import sys, os, binascii, shutil, io
from . import __version_verifier_modules__
from . import ffiplatform
from .error import VerificationError
if sys.version_info >= (3, 3):
    import importlib.machinery

    def _extension_suffixes():
        return importlib.machinery.EXTENSION_SUFFIXES[:]


else:
    import imp

    def _extension_suffixes():
        return [suffix for suffix, _, type in imp.get_suffixes() if type == imp.C_EXTENSION]


if sys.version_info >= (3, ):
    NativeIO = io.StringIO
else:

    class NativeIO(io.BytesIO):

        def write(self, s):
            if isinstance(s, unicode):
                s = s.encode('ascii')
            super(NativeIO, self).write(s)


class Verifier(object):

    def __init__(self, ffi, preamble, tmpdir=None, modulename=None, ext_package=None, tag='', force_generic_engine=False, source_extension='.c', flags=None, relative_to=None, **kwds):
        if ffi._parser._uses_new_feature:
            raise VerificationError('feature not supported with ffi.verify(), but only with ffi.set_source(): %s' % (
             ffi._parser._uses_new_feature,))
        else:
            self.ffi = ffi
            self.preamble = preamble
            if not modulename:
                flattened_kwds = ffiplatform.flatten(kwds)
            vengine_class = _locate_engine_class(ffi, force_generic_engine)
            self._vengine = vengine_class(self)
            self._vengine.patch_extension_kwds(kwds)
            self.flags = flags
            self.kwds = self.make_relative_to(kwds, relative_to)
            if modulename:
                if tag:
                    raise TypeError("can't specify both 'modulename' and 'tag'")
            else:
                key = '\x00'.join([sys.version[:3], __version_verifier_modules__,
                 preamble, flattened_kwds] + ffi._cdefsources)
                if sys.version_info >= (3, ):
                    key = key.encode('utf-8')
            k1 = hex(binascii.crc32(key[0::2]) & 4294967295)
            k1 = k1.lstrip('0x').rstrip('L')
            k2 = hex(binascii.crc32(key[1::2]) & 4294967295)
            k2 = k2.lstrip('0').rstrip('L')
            modulename = '_cffi_%s_%s%s%s' % (tag, self._vengine._class_key,
             k1, k2)
        suffix = _get_so_suffixes()[0]
        self.tmpdir = tmpdir or _caller_dir_pycache()
        self.sourcefilename = os.path.join(self.tmpdir, modulename + source_extension)
        self.modulefilename = os.path.join(self.tmpdir, modulename + suffix)
        self.ext_package = ext_package
        self._has_source = False
        self._has_module = False

    def write_source(self, file=None):
        """Write the C source code.  It is produced in 'self.sourcefilename',
        which can be tweaked beforehand."""
        with self.ffi._lock:
            if self._has_source:
                if file is None:
                    raise VerificationError('source code already written')
            self._write_source(file)

    def compile_module(self):
        """Write the C source code (if not done already) and compile it.
        This produces a dynamic link library in 'self.modulefilename'."""
        with self.ffi._lock:
            if self._has_module:
                raise VerificationError('module already compiled')
            if not self._has_source:
                self._write_source()
            self._compile_module()

    def load_library--- This code section failed: ---

 L.  98         0  LOAD_FAST                'self'
                2  LOAD_ATTR                ffi
                4  LOAD_ATTR                _lock
                6  SETUP_WITH           72  'to 72'
                8  POP_TOP          

 L.  99        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _has_module
               14  POP_JUMP_IF_TRUE     52  'to 52'

 L. 100        16  LOAD_FAST                'self'
               18  LOAD_METHOD              _locate_module
               20  CALL_METHOD_0         0  ''
               22  POP_TOP          

 L. 101        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _has_module
               28  POP_JUMP_IF_TRUE     52  'to 52'

 L. 102        30  LOAD_FAST                'self'
               32  LOAD_ATTR                _has_source
               34  POP_JUMP_IF_TRUE     44  'to 44'

 L. 103        36  LOAD_FAST                'self'
               38  LOAD_METHOD              _write_source
               40  CALL_METHOD_0         0  ''
               42  POP_TOP          
             44_0  COME_FROM            34  '34'

 L. 104        44  LOAD_FAST                'self'
               46  LOAD_METHOD              _compile_module
               48  CALL_METHOD_0         0  ''
               50  POP_TOP          
             52_0  COME_FROM            28  '28'
             52_1  COME_FROM            14  '14'

 L. 105        52  LOAD_FAST                'self'
               54  LOAD_METHOD              _load_library
               56  CALL_METHOD_0         0  ''
               58  POP_BLOCK        
               60  ROT_TWO          
               62  BEGIN_FINALLY    
               64  WITH_CLEANUP_START
               66  WITH_CLEANUP_FINISH
               68  POP_FINALLY           0  ''
               70  RETURN_VALUE     
             72_0  COME_FROM_WITH        6  '6'
               72  WITH_CLEANUP_START
               74  WITH_CLEANUP_FINISH
               76  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 60

    def get_module_name(self):
        basename = os.path.basename(self.modulefilename)
        basename = basename.split('.', 1)[0]
        if basename.endswith('_d'):
            if hasattr(sys, 'gettotalrefcount'):
                basename = basename[:-2]
        return basename

    def get_extension(self):
        ffiplatform._hack_at_distutils()
        if not self._has_source:
            with self.ffi._lock:
                if not self._has_source:
                    self._write_source()
        sourcename = ffiplatform.maybe_relative_path(self.sourcefilename)
        modname = self.get_module_name()
        return (ffiplatform.get_extension)(sourcename, modname, **self.kwds)

    def generates_python_module(self):
        return self._vengine._gen_python_module

    def make_relative_to(self, kwds, relative_to):
        if relative_to:
            if os.path.dirname(relative_to):
                dirname = os.path.dirname(relative_to)
                kwds = kwds.copy()
                for key in ffiplatform.LIST_OF_FILE_NAMES:
                    if key in kwds:
                        lst = kwds[key]
                        if not isinstance(lst, (list, tuple)):
                            raise TypeError("keyword '%s' should be a list or tuple" % (
                             key,))
                        lst = [os.path.join(dirname, fn) for fn in lst]
                        kwds[key] = lst

        return kwds

    def _locate_module(self):
        if not os.path.isfile(self.modulefilename):
            if self.ext_package:
                try:
                    pkg = __import__(self.ext_package, None, None, ['__doc__'])
                except ImportError:
                    return
                else:
                    path = pkg.__path__
            else:
                path = None
            filename = self._vengine.find_module(self.get_module_name(), path, _get_so_suffixes())
            if filename is None:
                return
            self.modulefilename = filename
        self._vengine.collect_types()
        self._has_module = True

    def _write_source_to(self, file):
        self._vengine._f = file
        try:
            self._vengine.write_source_to_f()
        finally:
            del self._vengine._f

    def _write_source(self, file=None):
        if file is not None:
            self._write_source_to(file)
        else:
            f = NativeIO()
            self._write_source_to(f)
            source_data = f.getvalue()
            if os.path.exists(self.sourcefilename):
                with open(self.sourcefilename, 'r') as (fp):
                    needs_written = not fp.read() == source_data
            else:
                needs_written = True
            if needs_written:
                _ensure_dir(self.sourcefilename)
                with open(self.sourcefilename, 'w') as (fp):
                    fp.write(source_data)
            self._has_source = True

    def _compile_module(self):
        tmpdir = os.path.dirname(self.sourcefilename)
        outputfilename = ffiplatform.compile(tmpdir, self.get_extension())
        try:
            same = ffiplatform.samefile(outputfilename, self.modulefilename)
        except OSError:
            same = False
        else:
            if not same:
                _ensure_dir(self.modulefilename)
                shutil.move(outputfilename, self.modulefilename)
            self._has_module = True

    def _load_library(self):
        assert self._has_module
        if self.flags is not None:
            return self._vengine.load_library(self.flags)
        return self._vengine.load_library()


_FORCE_GENERIC_ENGINE = False

def _locate_engine_class(ffi, force_generic_engine):
    if _FORCE_GENERIC_ENGINE:
        force_generic_engine = True
    if (force_generic_engine or '__pypy__') in sys.builtin_module_names:
        force_generic_engine = True
    else:
        try:
            import _cffi_backend
        except ImportError:
            _cffi_backend = '?'
        else:
            if ffi._backend is not _cffi_backend:
                force_generic_engine = True
            from . import vengine_cpy
            return vengine_cpy.VCPythonEngine


_TMPDIR = None

def _caller_dir_pycache():
    global _TMPDIR
    if _TMPDIR:
        return _TMPDIR
    result = os.environ.get('CFFI_TMPDIR')
    if result:
        return result
    filename = sys._getframe(2).f_code.co_filename
    return os.path.abspath(os.path.join(os.path.dirname(filename), '__pycache__'))


def set_tmpdir(dirname):
    """Set the temporary directory to use instead of __pycache__."""
    global _TMPDIR
    _TMPDIR = dirname


def cleanup_tmpdir(tmpdir=None, keep_so=False):
    """Clean up the temporary directory by removing all files in it
    called `_cffi_*.{c,so}` as well as the `build` subdirectory."""
    tmpdir = tmpdir or _caller_dir_pycache()
    try:
        filelist = os.listdir(tmpdir)
    except OSError:
        return
    else:
        if keep_so:
            suffix = '.c'
        else:
            suffix = _get_so_suffixes()[0].lower()
        for fn in filelist:
            if not fn.lower().startswith('_cffi_') or fn.lower().endswith(suffix) or fn.lower().endswith('.c'):
                try:
                    os.unlink(os.path.join(tmpdir, fn))
                except OSError:
                    pass

        else:
            clean_dir = [
             os.path.join(tmpdir, 'build')]
            for dir in clean_dir:
                try:
                    for fn in os.listdir(dir):
                        fn = os.path.join(dir, fn)
                        if os.path.isdir(fn):
                            clean_dir.append(fn)
                        else:
                            os.unlink(fn)

                except OSError:
                    pass


def _get_so_suffixes():
    suffixes = _extension_suffixes()
    if not suffixes:
        if sys.platform == 'win32':
            suffixes = [
             '.pyd']
        else:
            suffixes = [
             '.so']
    return suffixes


def _ensure_dir(filename):
    dirname = os.path.dirname(filename)
    if dirname:
        if not os.path.isdir(dirname):
            os.makedirs(dirname)