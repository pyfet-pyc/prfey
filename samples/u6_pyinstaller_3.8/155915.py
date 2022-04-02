# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: ctypes\macholib\dyld.py
"""
dyld emulation
"""
import os
from ctypes.macholib.framework import framework_info
from ctypes.macholib.dylib import dylib_info
from itertools import *
__all__ = [
 'dyld_find', 'framework_find',
 'framework_info', 'dylib_info']
DEFAULT_FRAMEWORK_FALLBACK = [
 os.path.expanduser('~/Library/Frameworks'),
 '/Library/Frameworks',
 '/Network/Library/Frameworks',
 '/System/Library/Frameworks']
DEFAULT_LIBRARY_FALLBACK = [
 os.path.expanduser('~/lib'),
 '/usr/local/lib',
 '/lib',
 '/usr/lib']

def dyld_env(env, var):
    if env is None:
        env = os.environ
    rval = env.get(var)
    if rval is None:
        return []
    return rval.split(':')


def dyld_image_suffix(env=None):
    if env is None:
        env = os.environ
    return env.get('DYLD_IMAGE_SUFFIX')


def dyld_framework_path(env=None):
    return dyld_env(env, 'DYLD_FRAMEWORK_PATH')


def dyld_library_path(env=None):
    return dyld_env(env, 'DYLD_LIBRARY_PATH')


def dyld_fallback_framework_path(env=None):
    return dyld_env(env, 'DYLD_FALLBACK_FRAMEWORK_PATH')


def dyld_fallback_library_path(env=None):
    return dyld_env(env, 'DYLD_FALLBACK_LIBRARY_PATH')


def dyld_image_suffix_search(iterator, env=None):
    """For a potential path iterator, add DYLD_IMAGE_SUFFIX semantics"""
    suffix = dyld_image_suffix(env)
    if suffix is None:
        return iterator

    def _inject(iterator=iterator, suffix=suffix):
        for path in iterator:
            if path.endswith('.dylib'):
                (yield path[:-len('.dylib')] + suffix + '.dylib')
            else:
                (yield path + suffix)
            (yield path)

    return _inject()


def dyld_override_search(name, env=None):
    framework = framework_info(name)
    if framework is not None:
        for path in dyld_framework_path(env):
            (yield os.path.join(path, framework['name']))

    for path in dyld_library_path(env):
        (yield os.path.join(path, os.path.basename(name)))


def dyld_executable_path_search(name, executable_path=None):
    if name.startswith('@executable_path/'):
        if executable_path is not None:
            (yield os.path.join(executable_path, name[len('@executable_path/'):]))


def dyld_default_search(name, env=None):
    (yield name)
    framework = framework_info(name)
    if framework is not None:
        fallback_framework_path = dyld_fallback_framework_path(env)
        for path in fallback_framework_path:
            (yield os.path.join(path, framework['name']))

    fallback_library_path = dyld_fallback_library_path(env)
    for path in fallback_library_path:
        (yield os.path.join(path, os.path.basename(name)))
    else:
        if framework is not None:
            if not fallback_framework_path:
                for path in DEFAULT_FRAMEWORK_FALLBACK:
                    (yield os.path.join(path, framework['name']))

        if not fallback_library_path:
            for path in DEFAULT_LIBRARY_FALLBACK:
                (yield os.path.join(path, os.path.basename(name)))


def dyld_find(name, executable_path=None, env=None):
    """
    Find a library or framework using dyld semantics
    """
    for path in dyld_image_suffix_search(chain(dyld_override_search(name, env), dyld_executable_path_search(name, executable_path), dyld_default_search(name, env)), env):
        if os.path.isfile(path):
            return path
    else:
        raise ValueError('dylib %s could not be found' % (name,))


def framework_find--- This code section failed: ---

 L. 138         0  LOAD_CONST               None
                2  STORE_FAST               'error'

 L. 139         4  SETUP_FINALLY        22  'to 22'

 L. 140         6  LOAD_GLOBAL              dyld_find
                8  LOAD_FAST                'fn'
               10  LOAD_FAST                'executable_path'
               12  LOAD_FAST                'env'
               14  LOAD_CONST               ('executable_path', 'env')
               16  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               18  POP_BLOCK        
               20  RETURN_VALUE     
             22_0  COME_FROM_FINALLY     4  '4'

 L. 141        22  DUP_TOP          
               24  LOAD_GLOBAL              ValueError
               26  COMPARE_OP               exception-match
               28  POP_JUMP_IF_FALSE    58  'to 58'
               30  POP_TOP          
               32  STORE_FAST               'e'
               34  POP_TOP          
               36  SETUP_FINALLY        46  'to 46'

 L. 142        38  LOAD_FAST                'e'
               40  STORE_FAST               'error'
               42  POP_BLOCK        
               44  BEGIN_FINALLY    
             46_0  COME_FROM_FINALLY    36  '36'
               46  LOAD_CONST               None
               48  STORE_FAST               'e'
               50  DELETE_FAST              'e'
               52  END_FINALLY      
               54  POP_EXCEPT       
               56  JUMP_FORWARD         60  'to 60'
             58_0  COME_FROM            28  '28'
               58  END_FINALLY      
             60_0  COME_FROM            56  '56'

 L. 143        60  LOAD_FAST                'fn'
               62  LOAD_METHOD              rfind
               64  LOAD_STR                 '.framework'
               66  CALL_METHOD_1         1  ''
               68  STORE_FAST               'fmwk_index'

 L. 144        70  LOAD_FAST                'fmwk_index'
               72  LOAD_CONST               -1
               74  COMPARE_OP               ==
               76  POP_JUMP_IF_FALSE    94  'to 94'

 L. 145        78  LOAD_GLOBAL              len
               80  LOAD_FAST                'fn'
               82  CALL_FUNCTION_1       1  ''
               84  STORE_FAST               'fmwk_index'

 L. 146        86  LOAD_FAST                'fn'
               88  LOAD_STR                 '.framework'
               90  INPLACE_ADD      
               92  STORE_FAST               'fn'
             94_0  COME_FROM            76  '76'

 L. 147        94  LOAD_GLOBAL              os
               96  LOAD_ATTR                path
               98  LOAD_METHOD              join
              100  LOAD_FAST                'fn'
              102  LOAD_GLOBAL              os
              104  LOAD_ATTR                path
              106  LOAD_METHOD              basename
              108  LOAD_FAST                'fn'
              110  LOAD_CONST               None
              112  LOAD_FAST                'fmwk_index'
              114  BUILD_SLICE_2         2 
              116  BINARY_SUBSCR    
              118  CALL_METHOD_1         1  ''
              120  CALL_METHOD_2         2  ''
              122  STORE_FAST               'fn'

 L. 148       124  SETUP_FINALLY       142  'to 142'

 L. 149       126  LOAD_GLOBAL              dyld_find
              128  LOAD_FAST                'fn'
              130  LOAD_FAST                'executable_path'
              132  LOAD_FAST                'env'
              134  LOAD_CONST               ('executable_path', 'env')
              136  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              138  POP_BLOCK        
              140  RETURN_VALUE     
            142_0  COME_FROM_FINALLY   124  '124'

 L. 150       142  DUP_TOP          
              144  LOAD_GLOBAL              ValueError
              146  COMPARE_OP               exception-match
              148  POP_JUMP_IF_FALSE   164  'to 164'
              150  POP_TOP          
              152  POP_TOP          
              154  POP_TOP          

 L. 151       156  LOAD_FAST                'error'
              158  RAISE_VARARGS_1       1  'exception instance'
              160  POP_EXCEPT       
              162  JUMP_FORWARD        166  'to 166'
            164_0  COME_FROM           148  '148'
              164  END_FINALLY      
            166_0  COME_FROM           162  '162'

Parse error at or near `POP_TOP' instruction at offset 152


def test_dyld_find():
    env = {}
    assert dyld_find('libSystem.dylib') == '/usr/lib/libSystem.dylib'
    assert dyld_find('System.framework/System') == '/System/Library/Frameworks/System.framework/System'


if __name__ == '__main__':
    test_dyld_find()