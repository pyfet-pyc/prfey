# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: setuptools\namespaces.py
import os
from distutils import log
import itertools
flatten = itertools.chain.from_iterable

class Installer:
    nspkg_ext = '-nspkg.pth'

    def install_namespaces--- This code section failed: ---

 L.  14         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _get_all_ns_packages
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'nsp'

 L.  15         8  LOAD_FAST                'nsp'
               10  POP_JUMP_IF_TRUE     16  'to 16'

 L.  16        12  LOAD_CONST               None
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L.  17        16  LOAD_GLOBAL              os
               18  LOAD_ATTR                path
               20  LOAD_METHOD              splitext
               22  LOAD_FAST                'self'
               24  LOAD_METHOD              _get_target
               26  CALL_METHOD_0         0  ''
               28  CALL_METHOD_1         1  ''
               30  UNPACK_SEQUENCE_2     2 
               32  STORE_FAST               'filename'
               34  STORE_FAST               'ext'

 L.  18        36  LOAD_FAST                'filename'
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                nspkg_ext
               42  INPLACE_ADD      
               44  STORE_FAST               'filename'

 L.  19        46  LOAD_FAST                'self'
               48  LOAD_ATTR                outputs
               50  LOAD_METHOD              append
               52  LOAD_FAST                'filename'
               54  CALL_METHOD_1         1  ''
               56  POP_TOP          

 L.  20        58  LOAD_GLOBAL              log
               60  LOAD_METHOD              info
               62  LOAD_STR                 'Installing %s'
               64  LOAD_FAST                'filename'
               66  CALL_METHOD_2         2  ''
               68  POP_TOP          

 L.  21        70  LOAD_GLOBAL              map
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                _gen_nspkg_line
               76  LOAD_FAST                'nsp'
               78  CALL_FUNCTION_2       2  ''
               80  STORE_FAST               'lines'

 L.  23        82  LOAD_FAST                'self'
               84  LOAD_ATTR                dry_run
               86  POP_JUMP_IF_FALSE   100  'to 100'

 L.  25        88  LOAD_GLOBAL              list
               90  LOAD_FAST                'lines'
               92  CALL_FUNCTION_1       1  ''
               94  POP_TOP          

 L.  26        96  LOAD_CONST               None
               98  RETURN_VALUE     
            100_0  COME_FROM            86  '86'

 L.  28       100  LOAD_GLOBAL              open
              102  LOAD_FAST                'filename'
              104  LOAD_STR                 'wt'
              106  CALL_FUNCTION_2       2  ''
              108  SETUP_WITH          136  'to 136'
              110  STORE_FAST               'f'

 L.  29       112  LOAD_FAST                'f'
              114  LOAD_METHOD              writelines
              116  LOAD_FAST                'lines'
              118  CALL_METHOD_1         1  ''
              120  POP_TOP          
              122  POP_BLOCK        
              124  LOAD_CONST               None
              126  DUP_TOP          
              128  DUP_TOP          
              130  CALL_FUNCTION_3       3  ''
              132  POP_TOP          
              134  JUMP_FORWARD        152  'to 152'
            136_0  COME_FROM_WITH      108  '108'
              136  <49>             
              138  POP_JUMP_IF_TRUE    142  'to 142'
              140  <48>             
            142_0  COME_FROM           138  '138'
              142  POP_TOP          
              144  POP_TOP          
              146  POP_TOP          
              148  POP_EXCEPT       
              150  POP_TOP          
            152_0  COME_FROM           134  '134'

Parse error at or near `DUP_TOP' instruction at offset 126

    def uninstall_namespaces(self):
        filename, ext = os.path.splitextself._get_target
        filename += self.nspkg_ext
        if not os.path.existsfilename:
            return
        log.info'Removing %s'filename
        os.removefilename

    def _get_target(self):
        return self.target

    _nspkg_tmpl = ('import sys, types, os', 'has_mfs = sys.version_info > (3, 5)',
                   'p = os.path.join(%(root)s, *%(pth)r)', "importlib = has_mfs and __import__('importlib.util')",
                   "has_mfs and __import__('importlib.machinery')", 'm = has_mfs and sys.modules.setdefault(%(pkg)r, importlib.util.module_from_spec(importlib.machinery.PathFinder.find_spec(%(pkg)r, [os.path.dirname(p)])))',
                   'm = m or sys.modules.setdefault(%(pkg)r, types.ModuleType(%(pkg)r))',
                   "mp = (m or []) and m.__dict__.setdefault('__path__',[])", '(p not in mp) and mp.append(p)')
    _nspkg_tmpl_multi = ('m and setattr(sys.modules[%(parent)r], %(child)r, m)', )

    def _get_root(self):
        return "sys._getframe(1).f_locals['sitedir']"

    def _gen_nspkg_line(self, pkg):
        pth = tuple(pkg.split'.')
        root = self._get_root
        tmpl_lines = self._nspkg_tmpl
        parent, sep, child = pkg.rpartition'.'
        if parent:
            tmpl_lines += self._nspkg_tmpl_multi
        return ';'.jointmpl_lines % locals() + '\n'

    def _get_all_ns_packages(self):
        """Return sorted list of all package namespaces"""
        pkgs = self.distribution.namespace_packages or []
        return sorted(flatten(map(self._pkg_names, pkgs)))

    @staticmethod
    def _pkg_names(pkg):
        """
        Given a namespace package, yield the components of that
        package.

        >>> names = Installer._pkg_names('a.b.c')
        >>> set(names) == set(['a', 'a.b', 'a.b.c'])
        True
        """
        parts = pkg.split'.'
        while parts:
            (yield '.'.joinparts)
            parts.pop


class DevelopInstaller(Installer):

    def _get_root(self):
        return repr(str(self.egg_path))

    def _get_target(self):
        return self.egg_link