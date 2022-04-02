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
    if not executable_path:
        import sys
        if sys.prefix:
            executable_path = os.path.join(sys.prefix, 'bin')
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

 L. 142         0  LOAD_CONST               None
                2  STORE_FAST               'error'

 L. 143         4  SETUP_FINALLY        22  'to 22'

 L. 144         6  LOAD_GLOBAL              dyld_find
                8  LOAD_FAST                'fn'
               10  LOAD_FAST                'executable_path'
               12  LOAD_FAST                'env'
               14  LOAD_CONST               ('executable_path', 'env')
               16  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               18  POP_BLOCK        
               20  RETURN_VALUE     
             22_0  COME_FROM_FINALLY     4  '4'

 L. 145        22  DUP_TOP          
               24  LOAD_GLOBAL              ValueError
               26  COMPARE_OP               exception-match
               28  POP_JUMP_IF_FALSE    58  'to 58'
               30  POP_TOP          
               32  STORE_FAST               'e'
               34  POP_TOP          
               36  SETUP_FINALLY        46  'to 46'

 L. 146        38  LOAD_FAST                'e'
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

 L. 147        60  LOAD_FAST                'fn'
               62  LOAD_METHOD              rfind
               64  LOAD_STR                 '.framework'
               66  CALL_METHOD_1         1  ''
               68  STORE_FAST               'fmwk_index'

 L. 148        70  LOAD_FAST                'fmwk_index'
               72  LOAD_CONST               -1
               74  COMPARE_OP               ==
               76  POP_JUMP_IF_FALSE    94  'to 94'

 L. 149        78  LOAD_GLOBAL              len
               80  LOAD_FAST                'fn'
               82  CALL_FUNCTION_1       1  ''
               84  STORE_FAST               'fmwk_index'

 L. 150        86  LOAD_FAST                'fn'
               88  LOAD_STR                 '.framework'
               90  INPLACE_ADD      
               92  STORE_FAST               'fn'
             94_0  COME_FROM            76  '76'

 L. 151        94  LOAD_GLOBAL              os
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

 L. 152       124  SETUP_FINALLY       176  'to 176'
              126  SETUP_FINALLY       148  'to 148'

 L. 153       128  LOAD_GLOBAL              dyld_find
              130  LOAD_FAST                'fn'
              132  LOAD_FAST                'executable_path'
              134  LOAD_FAST                'env'
              136  LOAD_CONST               ('executable_path', 'env')
              138  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              140  POP_BLOCK        
              142  POP_BLOCK        
              144  CALL_FINALLY        176  'to 176'
              146  RETURN_VALUE     
            148_0  COME_FROM_FINALLY   126  '126'

 L. 154       148  DUP_TOP          
              150  LOAD_GLOBAL              ValueError
              152  COMPARE_OP               exception-match
              154  POP_JUMP_IF_FALSE   170  'to 170'
              156  POP_TOP          
              158  POP_TOP          
              160  POP_TOP          

 L. 155       162  LOAD_FAST                'error'
              164  RAISE_VARARGS_1       1  'exception instance'
              166  POP_EXCEPT       
              168  JUMP_FORWARD        172  'to 172'
            170_0  COME_FROM           154  '154'
              170  END_FINALLY      
            172_0  COME_FROM           168  '168'
              172  POP_BLOCK        
              174  BEGIN_FINALLY    
            176_0  COME_FROM           144  '144'
            176_1  COME_FROM_FINALLY   124  '124'

 L. 157       176  LOAD_CONST               None
              178  STORE_FAST               'error'
              180  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 142


def test_dyld_find():
    env = {}
    assert dyld_find('libSystem.dylib') == '/usr/lib/libSystem.dylib'
    assert dyld_find('System.framework/System') == '/System/Library/Frameworks/System.framework/System'


if __name__ == '__main__':
    test_dyld_find()