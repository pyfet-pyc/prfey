# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: setuptools\_imp.py
"""
Re-implementation of find_module and get_frozen_object
from the deprecated imp module.
"""
import os, importlib.util, importlib.machinery
from .py34compat import module_from_spec
PY_SOURCE = 1
PY_COMPILED = 2
C_EXTENSION = 3
C_BUILTIN = 6
PY_FROZEN = 7

def find_spec(module, paths):
    finder = importlib.machinery.PathFinder().find_spec if isinstance(paths, list) else importlib.util.find_spec
    return finder(module, paths)


def find_module--- This code section failed: ---

 L.  31         0  LOAD_GLOBAL              find_spec
                2  LOAD_FAST                'module'
                4  LOAD_FAST                'paths'
                6  CALL_FUNCTION_2       2  ''
                8  STORE_FAST               'spec'

 L.  32        10  LOAD_FAST                'spec'
               12  LOAD_CONST               None
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    30  'to 30'

 L.  33        18  LOAD_GLOBAL              ImportError
               20  LOAD_STR                 "Can't find %s"
               22  LOAD_FAST                'module'
               24  BINARY_MODULO    
               26  CALL_FUNCTION_1       1  ''
               28  RAISE_VARARGS_1       1  'exception instance'
             30_0  COME_FROM            16  '16'

 L.  34        30  LOAD_FAST                'spec'
               32  LOAD_ATTR                has_location
               34  POP_JUMP_IF_TRUE     62  'to 62'
               36  LOAD_GLOBAL              hasattr
               38  LOAD_FAST                'spec'
               40  LOAD_STR                 'submodule_search_locations'
               42  CALL_FUNCTION_2       2  ''
               44  POP_JUMP_IF_FALSE    62  'to 62'

 L.  35        46  LOAD_GLOBAL              importlib
               48  LOAD_ATTR                util
               50  LOAD_METHOD              spec_from_loader
               52  LOAD_STR                 '__init__.py'
               54  LOAD_FAST                'spec'
               56  LOAD_ATTR                loader
               58  CALL_METHOD_2         2  ''
               60  STORE_FAST               'spec'
             62_0  COME_FROM            44  '44'
             62_1  COME_FROM            34  '34'

 L.  37        62  LOAD_CONST               -1
               64  STORE_FAST               'kind'

 L.  38        66  LOAD_CONST               None
               68  STORE_FAST               'file'

 L.  39        70  LOAD_GLOBAL              isinstance
               72  LOAD_FAST                'spec'
               74  LOAD_ATTR                loader
               76  LOAD_GLOBAL              type
               78  CALL_FUNCTION_2       2  ''
               80  STORE_FAST               'static'

 L.  40        82  LOAD_FAST                'spec'
               84  LOAD_ATTR                origin
               86  LOAD_STR                 'frozen'
               88  COMPARE_OP               ==
               90  POP_JUMP_IF_TRUE    112  'to 112'
               92  LOAD_FAST                'static'
               94  POP_JUMP_IF_FALSE   130  'to 130'
               96  LOAD_GLOBAL              issubclass

 L.  41        98  LOAD_FAST                'spec'
              100  LOAD_ATTR                loader
              102  LOAD_GLOBAL              importlib
              104  LOAD_ATTR                machinery
              106  LOAD_ATTR                FrozenImporter

 L.  40       108  CALL_FUNCTION_2       2  ''
              110  POP_JUMP_IF_FALSE   130  'to 130'
            112_0  COME_FROM            90  '90'

 L.  42       112  LOAD_GLOBAL              PY_FROZEN
              114  STORE_FAST               'kind'

 L.  43       116  LOAD_CONST               None
              118  STORE_FAST               'path'

 L.  44       120  LOAD_STR                 ''
              122  DUP_TOP          
              124  STORE_FAST               'suffix'
              126  STORE_FAST               'mode'
              128  JUMP_FORWARD        322  'to 322'
            130_0  COME_FROM           110  '110'
            130_1  COME_FROM            94  '94'

 L.  45       130  LOAD_FAST                'spec'
              132  LOAD_ATTR                origin
              134  LOAD_STR                 'built-in'
              136  COMPARE_OP               ==
              138  POP_JUMP_IF_TRUE    160  'to 160'
              140  LOAD_FAST                'static'
              142  POP_JUMP_IF_FALSE   178  'to 178'
              144  LOAD_GLOBAL              issubclass

 L.  46       146  LOAD_FAST                'spec'
              148  LOAD_ATTR                loader
              150  LOAD_GLOBAL              importlib
              152  LOAD_ATTR                machinery
              154  LOAD_ATTR                BuiltinImporter

 L.  45       156  CALL_FUNCTION_2       2  ''
              158  POP_JUMP_IF_FALSE   178  'to 178'
            160_0  COME_FROM           138  '138'

 L.  47       160  LOAD_GLOBAL              C_BUILTIN
              162  STORE_FAST               'kind'

 L.  48       164  LOAD_CONST               None
              166  STORE_FAST               'path'

 L.  49       168  LOAD_STR                 ''
              170  DUP_TOP          
              172  STORE_FAST               'suffix'
              174  STORE_FAST               'mode'
              176  JUMP_FORWARD        322  'to 322'
            178_0  COME_FROM           158  '158'
            178_1  COME_FROM           142  '142'

 L.  50       178  LOAD_FAST                'spec'
              180  LOAD_ATTR                has_location
          182_184  POP_JUMP_IF_FALSE   310  'to 310'

 L.  51       186  LOAD_FAST                'spec'
              188  LOAD_ATTR                origin
              190  STORE_FAST               'path'

 L.  52       192  LOAD_GLOBAL              os
              194  LOAD_ATTR                path
              196  LOAD_METHOD              splitext
              198  LOAD_FAST                'path'
              200  CALL_METHOD_1         1  ''
              202  LOAD_CONST               1
              204  BINARY_SUBSCR    
              206  STORE_FAST               'suffix'

 L.  53       208  LOAD_FAST                'suffix'
              210  LOAD_GLOBAL              importlib
              212  LOAD_ATTR                machinery
              214  LOAD_ATTR                SOURCE_SUFFIXES
              216  <118>                 0  ''
              218  POP_JUMP_IF_FALSE   224  'to 224'
              220  LOAD_STR                 'r'
              222  JUMP_FORWARD        226  'to 226'
            224_0  COME_FROM           218  '218'
              224  LOAD_STR                 'rb'
            226_0  COME_FROM           222  '222'
              226  STORE_FAST               'mode'

 L.  55       228  LOAD_FAST                'suffix'
              230  LOAD_GLOBAL              importlib
              232  LOAD_ATTR                machinery
              234  LOAD_ATTR                SOURCE_SUFFIXES
              236  <118>                 0  ''
              238  POP_JUMP_IF_FALSE   246  'to 246'

 L.  56       240  LOAD_GLOBAL              PY_SOURCE
              242  STORE_FAST               'kind'
              244  JUMP_FORWARD        284  'to 284'
            246_0  COME_FROM           238  '238'

 L.  57       246  LOAD_FAST                'suffix'
              248  LOAD_GLOBAL              importlib
              250  LOAD_ATTR                machinery
              252  LOAD_ATTR                BYTECODE_SUFFIXES
              254  <118>                 0  ''
          256_258  POP_JUMP_IF_FALSE   266  'to 266'

 L.  58       260  LOAD_GLOBAL              PY_COMPILED
              262  STORE_FAST               'kind'
              264  JUMP_FORWARD        284  'to 284'
            266_0  COME_FROM           256  '256'

 L.  59       266  LOAD_FAST                'suffix'
              268  LOAD_GLOBAL              importlib
              270  LOAD_ATTR                machinery
              272  LOAD_ATTR                EXTENSION_SUFFIXES
              274  <118>                 0  ''
          276_278  POP_JUMP_IF_FALSE   284  'to 284'

 L.  60       280  LOAD_GLOBAL              C_EXTENSION
              282  STORE_FAST               'kind'
            284_0  COME_FROM           276  '276'
            284_1  COME_FROM           264  '264'
            284_2  COME_FROM           244  '244'

 L.  62       284  LOAD_FAST                'kind'
              286  LOAD_GLOBAL              PY_SOURCE
              288  LOAD_GLOBAL              PY_COMPILED
              290  BUILD_SET_2           2 
              292  <118>                 0  ''
          294_296  POP_JUMP_IF_FALSE   322  'to 322'

 L.  63       298  LOAD_GLOBAL              open
              300  LOAD_FAST                'path'
              302  LOAD_FAST                'mode'
              304  CALL_FUNCTION_2       2  ''
              306  STORE_FAST               'file'
              308  JUMP_FORWARD        322  'to 322'
            310_0  COME_FROM           182  '182'

 L.  65       310  LOAD_CONST               None
              312  STORE_FAST               'path'

 L.  66       314  LOAD_STR                 ''
              316  DUP_TOP          
              318  STORE_FAST               'suffix'
              320  STORE_FAST               'mode'
            322_0  COME_FROM           308  '308'
            322_1  COME_FROM           294  '294'
            322_2  COME_FROM           176  '176'
            322_3  COME_FROM           128  '128'

 L.  68       322  LOAD_FAST                'file'
              324  LOAD_FAST                'path'
              326  LOAD_FAST                'suffix'
              328  LOAD_FAST                'mode'
              330  LOAD_FAST                'kind'
              332  BUILD_TUPLE_3         3 
              334  BUILD_TUPLE_3         3 
              336  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 14


def get_frozen_object(module, paths=None):
    spec = find_spec(module, paths)
    if not spec:
        raise ImportError("Can't find %s" % module)
    return spec.loader.get_codemodule


def get_module(module, paths, info):
    spec = find_spec(module, paths)
    if not spec:
        raise ImportError("Can't find %s" % module)
    return module_from_spec(spec)