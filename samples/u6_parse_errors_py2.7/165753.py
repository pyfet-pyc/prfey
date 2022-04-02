# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\future\standard_library\__init__.py
"""
Python 3 reorganized the standard library (PEP 3108). This module exposes
several standard library modules to Python 2 under their new Python 3
names.

It is designed to be used as follows::

    from future import standard_library
    standard_library.install_aliases()

And then these normal Py3 imports work on both Py3 and Py2::

    import builtins
    import copyreg
    import queue
    import reprlib
    import socketserver
    import winreg    # on Windows only
    import test.support
    import html, html.parser, html.entites
    import http, http.client, http.server
    import http.cookies, http.cookiejar
    import urllib.parse, urllib.request, urllib.response, urllib.error, urllib.robotparser
    import xmlrpc.client, xmlrpc.server

    import _thread
    import _dummy_thread
    import _markupbase

    from itertools import filterfalse, zip_longest
    from sys import intern
    from collections import UserDict, UserList, UserString
    from collections import OrderedDict, Counter     # even on Py2.6
    from subprocess import getoutput, getstatusoutput
    from subprocess import check_output              # even on Py2.6

(The renamed modules and functions are still available under their old
names on Python 2.)

This is a cleaner alternative to this idiom (see
http://docs.pythonsprints.com/python3_porting/py-porting.html)::

    try:
        import queue
    except ImportError:
        import Queue as queue

Limitations
-----------
We don't currently support these modules, but would like to::

    import dbm
    import dbm.dumb
    import dbm.gnu
    import collections.abc  # on Py33
    import pickle     # should (optionally) bring in cPickle on Python 2

"""
from __future__ import absolute_import, division, print_function
import sys, logging, imp, contextlib, types, copy, os
flog = logging.getLogger('future_stdlib')
_formatter = logging.Formatter(logging.BASIC_FORMAT)
_handler = logging.StreamHandler()
_handler.setFormatter(_formatter)
flog.addHandler(_handler)
flog.setLevel(logging.WARN)
from future.utils import PY2, PY3
REPLACED_MODULES = set(['test', 'urllib', 'pickle', 'dbm'])
RENAMES = {'__builtin__': 'builtins', 
   'copy_reg': 'copyreg', 
   'Queue': 'queue', 
   'future.moves.socketserver': 'socketserver', 
   'ConfigParser': 'configparser', 
   'repr': 'reprlib', 
   '_winreg': 'winreg', 
   'thread': '_thread', 
   'dummy_thread': '_dummy_thread', 
   'future.moves.xmlrpc': 'xmlrpc', 
   'future.moves.html': 'html', 
   'future.moves.http': 'http', 
   'future.moves._markupbase': '_markupbase'}
assert len(set(RENAMES.values()) & set(REPLACED_MODULES)) == 0
MOVES = [
 ('collections', 'UserList', 'UserList', 'UserList'),
 ('collections', 'UserDict', 'UserDict', 'UserDict'),
 ('collections', 'UserString', 'UserString', 'UserString'),
 ('itertools', 'filterfalse', 'itertools', 'ifilterfalse'),
 ('itertools', 'zip_longest', 'itertools', 'izip_longest'),
 ('sys', 'intern', '__builtin__', 'intern'),
 ('re', 'ASCII', 'stat', 'ST_MODE'),
 ('base64', 'encodebytes', 'base64', 'encodestring'),
 ('base64', 'decodebytes', 'base64', 'decodestring'),
 ('subprocess', 'getoutput', 'commands', 'getoutput'),
 ('subprocess', 'getstatusoutput', 'commands', 'getstatusoutput'),
 ('subprocess', 'check_output', 'future.backports.misc', 'check_output'),
 ('math', 'ceil', 'future.backports.misc', 'ceil'),
 ('collections', 'OrderedDict', 'future.backports.misc', 'OrderedDict'),
 ('collections', 'Counter', 'future.backports.misc', 'Counter'),
 ('itertools', 'count', 'future.backports.misc', 'count'),
 ('reprlib', 'recursive_repr', 'future.backports.misc', 'recursive_repr'),
 ('functools', 'cmp_to_key', 'future.backports.misc', 'cmp_to_key')]

class RenameImport(object):
    """
    A class for import hooks mapping Py3 module names etc. to the Py2 equivalents.
    """
    RENAMER = True

    def __init__--- This code section failed: ---

 L. 248         0  LOAD_FAST             1  'old_to_new'
                3  LOAD_FAST             0  'self'
                6  STORE_ATTR            0  'old_to_new'

 L. 249         9  LOAD_GLOBAL           1  'set'
               12  LOAD_FAST             1  'old_to_new'
               15  LOAD_ATTR             2  'keys'
               18  CALL_FUNCTION_0       0  None
               21  CALL_FUNCTION_1       1  None
               24  LOAD_GLOBAL           1  'set'
               27  LOAD_FAST             1  'old_to_new'
               30  LOAD_ATTR             3  'values'
               33  CALL_FUNCTION_0       0  None
               36  CALL_FUNCTION_1       1  None
               39  BINARY_AND       
               40  STORE_FAST            2  'both'

 L. 250        43  LOAD_GLOBAL           4  'len'
               46  LOAD_FAST             2  'both'
               49  CALL_FUNCTION_1       1  None
               52  LOAD_CONST               0
               55  COMPARE_OP            2  ==
               58  POP_JUMP_IF_FALSE   103  'to 103'

 L. 251        61  LOAD_GLOBAL           4  'len'
               64  LOAD_GLOBAL           1  'set'
               67  LOAD_FAST             1  'old_to_new'
               70  LOAD_ATTR             3  'values'
               73  CALL_FUNCTION_0       0  None
               76  CALL_FUNCTION_1       1  None
               79  CALL_FUNCTION_1       1  None
               82  LOAD_GLOBAL           4  'len'
               85  LOAD_FAST             1  'old_to_new'
               88  LOAD_ATTR             3  'values'
               91  CALL_FUNCTION_0       0  None
               94  CALL_FUNCTION_1       1  None
               97  COMPARE_OP            2  ==
            100_0  COME_FROM            58  '58'
              100  POP_JUMP_IF_TRUE    112  'to 112'
              103  LOAD_ASSERT              AssertionError

 L. 252       106  LOAD_CONST               'Ambiguity in renaming (handler not implemented)'
              109  RAISE_VARARGS_2       2  None

 L. 253       112  LOAD_GLOBAL           6  'dict'
              115  LOAD_GENEXPR             '<code_object <genexpr>>'
              118  MAKE_FUNCTION_0       0  None
              121  LOAD_FAST             1  'old_to_new'
              124  LOAD_ATTR             7  'items'
              127  CALL_FUNCTION_0       0  None
              130  GET_ITER         
              131  CALL_FUNCTION_1       1  None
              134  CALL_FUNCTION_1       1  None
              137  LOAD_FAST             0  'self'
              140  STORE_ATTR            8  'new_to_old'

Parse error at or near `LOAD_FAST' instruction at offset 137

    def find_module(self, fullname, path=None):
        new_base_names = set([ s.split('.')[0] for s in self.new_to_old ])
        if fullname in new_base_names:
            return self
        else:
            return

    def load_module(self, name):
        path = None
        if name in sys.modules:
            return sys.modules[name]
        else:
            if name in self.new_to_old:
                oldname = self.new_to_old[name]
                module = self._find_and_load_module(oldname)
            else:
                module = self._find_and_load_module(name)
            sys.modules[name] = module
            return module

    def _find_and_load_module(self, name, path=None):
        """
        Finds and loads it. But if there's a . in the name, handles it
        properly.
        """
        bits = name.split('.')
        while len(bits) > 1:
            packagename = bits.pop(0)
            package = self._find_and_load_module(packagename, path)
            try:
                path = package.__path__
            except AttributeError:
                flog.debug(('Package {0} has no __path__.').format(package))
                if name in sys.modules:
                    return sys.modules[name]
                flog.debug('What to do here?')

        name = bits[0]
        module_info = imp.find_module(name, path)
        return imp.load_module(name, *module_info)


class hooks(object):
    """
    Acts as a context manager. Saves the state of sys.modules and restores it
    after the 'with' block.

    Use like this:

    >>> from future import standard_library
    >>> with standard_library.hooks():
    ...     import http.client
    >>> import requests

    For this to work, http.client will be scrubbed from sys.modules after the
    'with' block. That way the modules imported in the 'with' block will
    continue to be accessible in the current namespace but not from any
    imported modules (like requests).
    """

    def __enter__(self):
        self.old_sys_modules = copy.copy(sys.modules)
        self.hooks_were_installed = detect_hooks()
        install_hooks()
        return self

    def __exit__(self, *args):
        if not self.hooks_were_installed:
            remove_hooks()


if PY2:
    assert len(set(RENAMES.values()) & set(sys.builtin_module_names)) == 0

    def is_py2_stdlib_module(m):
        """
    Tries to infer whether the module m is from the Python 2 standard library.
    This may not be reliable on all systems.
    """
        if PY3:
            return False
        if 'stdlib_path' not in is_py2_stdlib_module.__dict__:
            stdlib_files = [
             contextlib.__file__, os.__file__, copy.__file__]
            stdlib_paths = [ os.path.split(f)[0] for f in stdlib_files ]
            if not len(set(stdlib_paths)) == 1:
                flog.warn('Multiple locations found for the Python standard library: %s' % stdlib_paths)
            is_py2_stdlib_module.stdlib_path = stdlib_paths[0]
        if m.__name__ in sys.builtin_module_names:
            return True
        if hasattr(m, '__file__'):
            modpath = os.path.split(m.__file__)
            if modpath[0].startswith(is_py2_stdlib_module.stdlib_path) and 'site-packages' not in modpath[0]:
                return True
        return False


    def scrub_py2_sys_modules():
        """
    Removes any Python 2 standard library modules from ``sys.modules`` that
    would interfere with Py3-style imports using import hooks. Examples are
    modules with the same names (like urllib or email).

    (Note that currently import hooks are disabled for modules like these
    with ambiguous names anyway ...)
    """
        if PY3:
            return {}
        scrubbed = {}
        for modulename in REPLACED_MODULES & set(RENAMES.keys()):
            if modulename not in sys.modules:
                continue
            module = sys.modules[modulename]
            if is_py2_stdlib_module(module):
                flog.debug(('Deleting (Py2) {} from sys.modules').format(modulename))
                scrubbed[modulename] = sys.modules[modulename]
                del sys.modules[modulename]

        return scrubbed


    def scrub_future_sys_modules():
        """
    Deprecated.
    """
        return {}


    class suspend_hooks(object):
        """
    Acts as a context manager. Use like this:

    >>> from future import standard_library
    >>> standard_library.install_hooks()
    >>> import http.client
    >>> # ...
    >>> with standard_library.suspend_hooks():
    >>>     import requests     # incompatible with ``future``'s standard library hooks

    If the hooks were disabled before the context, they are not installed when
    the context is left.
    """

        def __enter__(self):
            self.hooks_were_installed = detect_hooks()
            remove_hooks()
            return self

        def __exit__(self, *args):
            if self.hooks_were_installed:
                install_hooks()


    def restore_sys_modules(scrubbed):
        """
    Add any previously scrubbed modules back to the sys.modules cache,
    but only if it's safe to do so.
    """
        clash = set(sys.modules) & set(scrubbed)
        if len(clash) != 0:
            first = list(clash)[0]
            raise ImportError(('future module {} clashes with Py2 module').format(first))
        sys.modules.update(scrubbed)


    def install_aliases():
        """
    Monkey-patches the standard library in Py2.6/7 to provide
    aliases for better Py3 compatibility.
    """
        if PY3:
            return
        for newmodname, newobjname, oldmodname, oldobjname in MOVES:
            __import__(newmodname)
            newmod = sys.modules[newmodname]
            __import__(oldmodname)
            oldmod = sys.modules[oldmodname]
            obj = getattr(oldmod, oldobjname)
            setattr(newmod, newobjname, obj)

        import urllib
        from future.backports.urllib import request
        from future.backports.urllib import response
        from future.backports.urllib import parse
        from future.backports.urllib import error
        from future.backports.urllib import robotparser
        urllib.request = request
        urllib.response = response
        urllib.parse = parse
        urllib.error = error
        urllib.robotparser = robotparser
        sys.modules['urllib.request'] = request
        sys.modules['urllib.response'] = response
        sys.modules['urllib.parse'] = parse
        sys.modules['urllib.error'] = error
        sys.modules['urllib.robotparser'] = robotparser
        try:
            import test
        except ImportError:
            pass

        try:
            from future.moves.test import support
        except ImportError:
            pass
        else:
            test.support = support
            sys.modules['test.support'] = support

        try:
            import dbm
        except ImportError:
            pass
        else:
            from future.moves.dbm import dumb
            dbm.dumb = dumb
            sys.modules['dbm.dumb'] = dumb
            try:
                from future.moves.dbm import gnu
            except ImportError:
                pass
            else:
                dbm.gnu = gnu
                sys.modules['dbm.gnu'] = gnu

            try:
                from future.moves.dbm import ndbm
            except ImportError:
                pass
            else:
                dbm.ndbm = ndbm
                sys.modules['dbm.ndbm'] = ndbm


    def install_hooks():
        """
    This function installs the future.standard_library import hook into
    sys.meta_path.
    """
        if PY3:
            return
        install_aliases()
        flog.debug(('sys.meta_path was: {0}').format(sys.meta_path))
        flog.debug('Installing hooks ...')
        newhook = RenameImport(RENAMES)
        if not detect_hooks():
            sys.meta_path.append(newhook)
        flog.debug(('sys.meta_path is now: {0}').format(sys.meta_path))


    def enable_hooks():
        """
    Deprecated. Use install_hooks() instead. This will be removed by
    ``future`` v1.0.
    """
        install_hooks()


    def remove_hooks(scrub_sys_modules=False):
        """
    This function removes the import hook from sys.meta_path.
    """
        if PY3:
            return
        flog.debug('Uninstalling hooks ...')
        for i, hook in list(enumerate(sys.meta_path))[::-1]:
            if hasattr(hook, 'RENAMER'):
                del sys.meta_path[i]

        if scrub_sys_modules:
            scrub_future_sys_modules()


    def disable_hooks():
        """
    Deprecated. Use remove_hooks() instead. This will be removed by
    ``future`` v1.0.
    """
        remove_hooks()


    def detect_hooks():
        """
    Returns True if the import hooks are installed, False if not.
    """
        flog.debug('Detecting hooks ...')
        present = any([ hasattr(hook, 'RENAMER') for hook in sys.meta_path ])
        if present:
            flog.debug('Detected.')
        else:
            flog.debug('Not detected.')
        return present


    sys.py2_modules = hasattr(sys, 'py2_modules') or {}

def cache_py2_modules():
    """
    Currently this function is unneeded, as we are not attempting to provide import hooks
    for modules with ambiguous names: email, urllib, pickle.
    """
    if len(sys.py2_modules) != 0:
        return
    assert not detect_hooks()
    import urllib
    sys.py2_modules['urllib'] = urllib
    import email
    sys.py2_modules['email'] = email
    import pickle
    sys.py2_modules['pickle'] = pickle


def import_(module_name, backport=False):
    """
    Pass a (potentially dotted) module name of a Python 3 standard library
    module. This function imports the module compatibly on Py2 and Py3 and
    returns the top-level module.

    Example use:
        >>> http = import_('http.client')
        >>> http = import_('http.server')
        >>> urllib = import_('urllib.request')

    Then:
        >>> conn = http.client.HTTPConnection(...)
        >>> response = urllib.request.urlopen('http://mywebsite.com')
        >>> # etc.

    Use as follows:
        >>> package_name = import_(module_name)

    On Py3, equivalent to this:

        >>> import module_name

    On Py2, equivalent to this if backport=False:

        >>> from future.moves import module_name

    or to this if backport=True:

        >>> from future.backports import module_name

    except that it also handles dotted module names such as ``http.client``
    The effect then is like this:

        >>> from future.backports import module
        >>> from future.backports.module import submodule
        >>> module.submodule = submodule

    Note that this would be a SyntaxError in Python:

        >>> from future.backports import http.client

    """
    import importlib
    if PY3:
        return __import__(module_name)
    else:
        if backport:
            prefix = 'future.backports'
        else:
            prefix = 'future.moves'
        parts = prefix.split('.') + module_name.split('.')
        modules = []
        for i, part in enumerate(parts):
            sofar = ('.').join(parts[:i + 1])
            modules.append(importlib.import_module(sofar))

        for i, part in reversed(list(enumerate(parts))):
            if i == 0:
                break
            setattr(modules[(i - 1)], part, modules[i])

        return modules[2]


def from_import(module_name, *symbol_names, **kwargs):
    """
    Example use:
        >>> HTTPConnection = from_import('http.client', 'HTTPConnection')
        >>> HTTPServer = from_import('http.server', 'HTTPServer')
        >>> urlopen, urlparse = from_import('urllib.request', 'urlopen', 'urlparse')

    Equivalent to this on Py3:

        >>> from module_name import symbol_names[0], symbol_names[1], ...

    and this on Py2:

        >>> from future.moves.module_name import symbol_names[0], ...

    or:

        >>> from future.backports.module_name import symbol_names[0], ...

    except that it also handles dotted module names such as ``http.client``.
    """
    if PY3:
        return __import__(module_name)
    else:
        if 'backport' in kwargs and bool(kwargs['backport']):
            prefix = 'future.backports'
        else:
            prefix = 'future.moves'
        parts = prefix.split('.') + module_name.split('.')
        module = importlib.import_module(prefix + '.' + module_name)
        output = [ getattr(module, name) for name in symbol_names ]
        if len(output) == 1:
            return output[0]
        return output


class exclude_local_folder_imports(object):
    """
    A context-manager that prevents standard library modules like configparser
    from being imported from the local python-future source folder on Py3.

    (This was need prior to v0.16.0 because the presence of a configparser
    folder would otherwise have prevented setuptools from running on Py3. Maybe
    it's not needed any more?)
    """

    def __init__(self, *args):
        assert len(args) > 0
        self.module_names = args
        if any([ '.' in m for m in self.module_names ]):
            raise NotImplementedError('Dotted module names are not supported')

    def __enter__(self):
        self.old_sys_path = copy.copy(sys.path)
        self.old_sys_modules = copy.copy(sys.modules)
        if sys.version_info[0] < 3:
            return
        FUTURE_SOURCE_SUBFOLDERS = [
         'future', 'past', 'libfuturize', 'libpasteurize', 'builtins']
        for folder in self.old_sys_path:
            if all([ os.path.exists(os.path.join(folder, subfolder)) for subfolder in FUTURE_SOURCE_SUBFOLDERS
                   ]):
                sys.path.remove(folder)

        for m in self.module_names:
            try:
                module = __import__(m, level=0)
            except ImportError:
                pass

    def __exit__(self, *args):
        sys.path = self.old_sys_path
        for m in set(self.old_sys_modules.keys()) - set(sys.modules.keys()):
            sys.modules[m] = self.old_sys_modules[m]


TOP_LEVEL_MODULES = ['builtins',
 'copyreg',
 'html',
 'http',
 'queue',
 'reprlib',
 'socketserver',
 'test',
 'tkinter',
 'winreg',
 'xmlrpc',
 '_dummy_thread',
 '_markupbase',
 '_thread']

def import_top_level_modules():
    with exclude_local_folder_imports(*TOP_LEVEL_MODULES):
        for m in TOP_LEVEL_MODULES:
            try:
                __import__(m)
            except ImportError:
                pass