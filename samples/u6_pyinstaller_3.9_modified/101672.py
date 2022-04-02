# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: distutils\filelist.py
"""distutils.filelist

Provides the FileList class, used for poking about the filesystem
and building lists of files.
"""
import os, re, fnmatch, functools
from distutils.util import convert_path
from distutils.errors import DistutilsTemplateError, DistutilsInternalError
from distutils import log

class FileList:
    __doc__ = "A list of files built by on exploring the filesystem and filtered by\n    applying various patterns to what we find there.\n\n    Instance attributes:\n      dir\n        directory from which files will be taken -- only used if\n        'allfiles' not supplied to constructor\n      files\n        list of filenames currently being built/filtered/manipulated\n      allfiles\n        complete list of files under consideration (ie. without any\n        filtering applied)\n    "

    def __init__(self, warn=None, debug_print=None):
        self.allfiles = None
        self.files = []

    def set_allfiles(self, allfiles):
        self.allfiles = allfiles

    def findall(self, dir=os.curdir):
        self.allfiles = findall(dir)

    def debug_print(self, msg):
        """Print 'msg' to stdout if the global DEBUG (taken from the
        DISTUTILS_DEBUG environment variable) flag is true.
        """
        from distutils.debug import DEBUG
        if DEBUG:
            print(msg)

    def append(self, item):
        self.files.append(item)

    def extend(self, items):
        self.files.extend(items)

    def sort(self):
        sortable_files = sorted(map(os.path.split, self.files))
        self.files = []
        for sort_tuple in sortable_files:
            self.files.append((os.path.join)(*sort_tuple))

    def remove_duplicates(self):
        for i in range(len(self.files) - 1, 0, -1):
            if self.files[i] == self.files[(i - 1)]:
                del self.files[i]

    def _parse_template_line--- This code section failed: ---

 L.  77         0  LOAD_FAST                'line'
                2  LOAD_METHOD              split
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'words'

 L.  78         8  LOAD_FAST                'words'
               10  LOAD_CONST               0
               12  BINARY_SUBSCR    
               14  STORE_FAST               'action'

 L.  80        16  LOAD_CONST               None
               18  DUP_TOP          
               20  STORE_FAST               'patterns'
               22  DUP_TOP          
               24  STORE_FAST               'dir'
               26  STORE_FAST               'dir_pattern'

 L.  82        28  LOAD_FAST                'action'
               30  LOAD_CONST               ('include', 'exclude', 'global-include', 'global-exclude')
               32  <118>                 0  ''
               34  POP_JUMP_IF_FALSE    84  'to 84'

 L.  84        36  LOAD_GLOBAL              len
               38  LOAD_FAST                'words'
               40  CALL_FUNCTION_1       1  ''
               42  LOAD_CONST               2
               44  COMPARE_OP               <
               46  POP_JUMP_IF_FALSE    60  'to 60'

 L.  85        48  LOAD_GLOBAL              DistutilsTemplateError

 L.  86        50  LOAD_STR                 "'%s' expects <pattern1> <pattern2> ..."
               52  LOAD_FAST                'action'
               54  BINARY_MODULO    

 L.  85        56  CALL_FUNCTION_1       1  ''
               58  RAISE_VARARGS_1       1  'exception instance'
             60_0  COME_FROM            46  '46'

 L.  87        60  LOAD_LISTCOMP            '<code_object <listcomp>>'
               62  LOAD_STR                 'FileList._parse_template_line.<locals>.<listcomp>'
               64  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               66  LOAD_FAST                'words'
               68  LOAD_CONST               1
               70  LOAD_CONST               None
               72  BUILD_SLICE_2         2 
               74  BINARY_SUBSCR    
               76  GET_ITER         
               78  CALL_FUNCTION_1       1  ''
               80  STORE_FAST               'patterns'
               82  JUMP_FORWARD        210  'to 210'
             84_0  COME_FROM            34  '34'

 L.  88        84  LOAD_FAST                'action'
               86  LOAD_CONST               ('recursive-include', 'recursive-exclude')
               88  <118>                 0  ''
               90  POP_JUMP_IF_FALSE   152  'to 152'

 L.  89        92  LOAD_GLOBAL              len
               94  LOAD_FAST                'words'
               96  CALL_FUNCTION_1       1  ''
               98  LOAD_CONST               3
              100  COMPARE_OP               <
              102  POP_JUMP_IF_FALSE   116  'to 116'

 L.  90       104  LOAD_GLOBAL              DistutilsTemplateError

 L.  91       106  LOAD_STR                 "'%s' expects <dir> <pattern1> <pattern2> ..."
              108  LOAD_FAST                'action'
              110  BINARY_MODULO    

 L.  90       112  CALL_FUNCTION_1       1  ''
              114  RAISE_VARARGS_1       1  'exception instance'
            116_0  COME_FROM           102  '102'

 L.  92       116  LOAD_GLOBAL              convert_path
              118  LOAD_FAST                'words'
              120  LOAD_CONST               1
              122  BINARY_SUBSCR    
              124  CALL_FUNCTION_1       1  ''
              126  STORE_FAST               'dir'

 L.  93       128  LOAD_LISTCOMP            '<code_object <listcomp>>'
              130  LOAD_STR                 'FileList._parse_template_line.<locals>.<listcomp>'
              132  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              134  LOAD_FAST                'words'
              136  LOAD_CONST               2
              138  LOAD_CONST               None
              140  BUILD_SLICE_2         2 
              142  BINARY_SUBSCR    
              144  GET_ITER         
              146  CALL_FUNCTION_1       1  ''
              148  STORE_FAST               'patterns'
              150  JUMP_FORWARD        210  'to 210'
            152_0  COME_FROM            90  '90'

 L.  94       152  LOAD_FAST                'action'
              154  LOAD_CONST               ('graft', 'prune')
              156  <118>                 0  ''
              158  POP_JUMP_IF_FALSE   198  'to 198'

 L.  95       160  LOAD_GLOBAL              len
              162  LOAD_FAST                'words'
              164  CALL_FUNCTION_1       1  ''
              166  LOAD_CONST               2
              168  COMPARE_OP               !=
              170  POP_JUMP_IF_FALSE   184  'to 184'

 L.  96       172  LOAD_GLOBAL              DistutilsTemplateError

 L.  97       174  LOAD_STR                 "'%s' expects a single <dir_pattern>"
              176  LOAD_FAST                'action'
              178  BINARY_MODULO    

 L.  96       180  CALL_FUNCTION_1       1  ''
              182  RAISE_VARARGS_1       1  'exception instance'
            184_0  COME_FROM           170  '170'

 L.  98       184  LOAD_GLOBAL              convert_path
              186  LOAD_FAST                'words'
              188  LOAD_CONST               1
              190  BINARY_SUBSCR    
              192  CALL_FUNCTION_1       1  ''
              194  STORE_FAST               'dir_pattern'
              196  JUMP_FORWARD        210  'to 210'
            198_0  COME_FROM           158  '158'

 L. 100       198  LOAD_GLOBAL              DistutilsTemplateError
              200  LOAD_STR                 "unknown action '%s'"
              202  LOAD_FAST                'action'
              204  BINARY_MODULO    
              206  CALL_FUNCTION_1       1  ''
              208  RAISE_VARARGS_1       1  'exception instance'
            210_0  COME_FROM           196  '196'
            210_1  COME_FROM           150  '150'
            210_2  COME_FROM            82  '82'

 L. 102       210  LOAD_FAST                'action'
              212  LOAD_FAST                'patterns'
              214  LOAD_FAST                'dir'
              216  LOAD_FAST                'dir_pattern'
              218  BUILD_TUPLE_4         4 
              220  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 32

    def process_template_line(self, line):
        action, patterns, dir, dir_pattern = self._parse_template_line(line)
        if action == 'include':
            self.debug_print('include ' + ' '.join(patterns))
            for pattern in patterns:
                if not self.include_pattern(pattern, anchor=1):
                    log.warn("warning: no files found matching '%s'", pattern)

        else:
            if action == 'exclude':
                self.debug_print('exclude ' + ' '.join(patterns))
                for pattern in patterns:
                    if not self.exclude_pattern(pattern, anchor=1):
                        log.warn("warning: no previously-included files found matching '%s'", pattern)

            else:
                if action == 'global-include':
                    self.debug_print('global-include ' + ' '.join(patterns))
                    for pattern in patterns:
                        if not self.include_pattern(pattern, anchor=0):
                            log.warn("warning: no files found matching '%s' anywhere in distribution", pattern)

                else:
                    if action == 'global-exclude':
                        self.debug_print('global-exclude ' + ' '.join(patterns))
                        for pattern in patterns:
                            if not self.exclude_pattern(pattern, anchor=0):
                                log.warn("warning: no previously-included files matching '%s' found anywhere in distribution", pattern)

                    else:
                        if action == 'recursive-include':
                            self.debug_print('recursive-include %s %s' % (
                             dir, ' '.join(patterns)))
                            for pattern in patterns:
                                if not self.include_pattern(pattern, prefix=dir):
                                    log.warn("warning: no files found matching '%s' under directory '%s'", pattern, dir)

                        else:
                            if action == 'recursive-exclude':
                                self.debug_print('recursive-exclude %s %s' % (
                                 dir, ' '.join(patterns)))
                                for pattern in patterns:
                                    if not self.exclude_pattern(pattern, prefix=dir):
                                        log.warn("warning: no previously-included files matching '%s' found under directory '%s'", pattern, dir)

                            else:
                                if action == 'graft':
                                    self.debug_print('graft ' + dir_pattern)
                                    self.include_pattern(None, prefix=dir_pattern) or log.warn("warning: no directories found matching '%s'", dir_pattern)
                                else:
                                    if action == 'prune':
                                        self.debug_print('prune ' + dir_pattern)
                                        self.exclude_pattern(None, prefix=dir_pattern) or log.warn("no previously-included directories found matching '%s'", dir_pattern)
                                    else:
                                        raise DistutilsInternalError("this cannot happen: invalid action '%s'" % action)

    def include_pattern--- This code section failed: ---

 L. 206         0  LOAD_CONST               False
                2  STORE_FAST               'files_found'

 L. 207         4  LOAD_GLOBAL              translate_pattern
                6  LOAD_FAST                'pattern'
                8  LOAD_FAST                'anchor'
               10  LOAD_FAST                'prefix'
               12  LOAD_FAST                'is_regex'
               14  CALL_FUNCTION_4       4  ''
               16  STORE_FAST               'pattern_re'

 L. 208        18  LOAD_FAST                'self'
               20  LOAD_METHOD              debug_print
               22  LOAD_STR                 "include_pattern: applying regex r'%s'"

 L. 209        24  LOAD_FAST                'pattern_re'
               26  LOAD_ATTR                pattern

 L. 208        28  BINARY_MODULO    
               30  CALL_METHOD_1         1  ''
               32  POP_TOP          

 L. 212        34  LOAD_FAST                'self'
               36  LOAD_ATTR                allfiles
               38  LOAD_CONST               None
               40  <117>                 0  ''
               42  POP_JUMP_IF_FALSE    52  'to 52'

 L. 213        44  LOAD_FAST                'self'
               46  LOAD_METHOD              findall
               48  CALL_METHOD_0         0  ''
               50  POP_TOP          
             52_0  COME_FROM            42  '42'

 L. 215        52  LOAD_FAST                'self'
               54  LOAD_ATTR                allfiles
               56  GET_ITER         
             58_0  COME_FROM            70  '70'
               58  FOR_ITER            104  'to 104'
               60  STORE_FAST               'name'

 L. 216        62  LOAD_FAST                'pattern_re'
               64  LOAD_METHOD              search
               66  LOAD_FAST                'name'
               68  CALL_METHOD_1         1  ''
               70  POP_JUMP_IF_FALSE    58  'to 58'

 L. 217        72  LOAD_FAST                'self'
               74  LOAD_METHOD              debug_print
               76  LOAD_STR                 ' adding '
               78  LOAD_FAST                'name'
               80  BINARY_ADD       
               82  CALL_METHOD_1         1  ''
               84  POP_TOP          

 L. 218        86  LOAD_FAST                'self'
               88  LOAD_ATTR                files
               90  LOAD_METHOD              append
               92  LOAD_FAST                'name'
               94  CALL_METHOD_1         1  ''
               96  POP_TOP          

 L. 219        98  LOAD_CONST               True
              100  STORE_FAST               'files_found'
              102  JUMP_BACK            58  'to 58'

 L. 220       104  LOAD_FAST                'files_found'
              106  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 40

    def exclude_pattern(self, pattern, anchor=1, prefix=None, is_regex=0):
        """Remove strings (presumably filenames) from 'files' that match
        'pattern'.  Other parameters are the same as for
        'include_pattern()', above.
        The list 'self.files' is modified in place.
        Return True if files are found, False otherwise.
        """
        files_found = False
        pattern_re = translate_patternpatternanchorprefixis_regex
        self.debug_print("exclude_pattern: applying regex r'%s'" % pattern_re.pattern)
        for i in range(len(self.files) - 1, -1, -1):
            if pattern_re.search(self.files[i]):
                self.debug_print(' removing ' + self.files[i])
                del self.files[i]
                files_found = True
            return files_found


def _find_all_simple(path):
    """
    Find all files under 'path'
    """
    results = (os.path.join(base, file) for base, dirs, files in os.walk(path, followlinks=True) for file in files)
    return filter(os.path.isfile, results)


def findall(dir=os.curdir):
    """
    Find all files under 'dir' and return the list of full filenames.
    Unless dir is '.', return full filenames with dir prepended.
    """
    files = _find_all_simple(dir)
    if dir == os.curdir:
        make_rel = functools.partial((os.path.relpath), start=dir)
        files = map(make_rel, files)
    return list(files)


def glob_to_re(pattern):
    """Translate a shell-like glob pattern to a regular expression; return
    a string containing the regex.  Differs from 'fnmatch.translate()' in
    that '*' does not match "special characters" (which are
    platform-specific).
    """
    pattern_re = fnmatch.translate(pattern)
    sep = os.sep
    if os.sep == '\\':
        sep = '\\\\\\\\'
    escaped = '\\1[^%s]' % sep
    pattern_re = re.sub('((?<!\\\\)(\\\\\\\\)*)\\.', escaped, pattern_re)
    return pattern_re


def translate_pattern--- This code section failed: ---

 L. 299         0  LOAD_FAST                'is_regex'
                2  POP_JUMP_IF_FALSE    28  'to 28'

 L. 300         4  LOAD_GLOBAL              isinstance
                6  LOAD_FAST                'pattern'
                8  LOAD_GLOBAL              str
               10  CALL_FUNCTION_2       2  ''
               12  POP_JUMP_IF_FALSE    24  'to 24'

 L. 301        14  LOAD_GLOBAL              re
               16  LOAD_METHOD              compile
               18  LOAD_FAST                'pattern'
               20  CALL_METHOD_1         1  ''
               22  RETURN_VALUE     
             24_0  COME_FROM            12  '12'

 L. 303        24  LOAD_FAST                'pattern'
               26  RETURN_VALUE     
             28_0  COME_FROM             2  '2'

 L. 306        28  LOAD_GLOBAL              glob_to_re
               30  LOAD_STR                 '_'
               32  CALL_FUNCTION_1       1  ''
               34  LOAD_METHOD              partition
               36  LOAD_STR                 '_'
               38  CALL_METHOD_1         1  ''
               40  UNPACK_SEQUENCE_3     3 
               42  STORE_FAST               'start'
               44  STORE_FAST               '_'
               46  STORE_FAST               'end'

 L. 308        48  LOAD_FAST                'pattern'
               50  POP_JUMP_IF_FALSE    86  'to 86'

 L. 309        52  LOAD_GLOBAL              glob_to_re
               54  LOAD_FAST                'pattern'
               56  CALL_FUNCTION_1       1  ''
               58  STORE_FAST               'pattern_re'

 L. 310        60  LOAD_FAST                'pattern_re'
               62  LOAD_METHOD              startswith
               64  LOAD_FAST                'start'
               66  CALL_METHOD_1         1  ''
               68  POP_JUMP_IF_FALSE    80  'to 80'
               70  LOAD_FAST                'pattern_re'
               72  LOAD_METHOD              endswith
               74  LOAD_FAST                'end'
               76  CALL_METHOD_1         1  ''
               78  POP_JUMP_IF_TRUE     90  'to 90'
             80_0  COME_FROM            68  '68'
               80  <74>             
               82  RAISE_VARARGS_1       1  'exception instance'
               84  JUMP_FORWARD         90  'to 90'
             86_0  COME_FROM            50  '50'

 L. 312        86  LOAD_STR                 ''
               88  STORE_FAST               'pattern_re'
             90_0  COME_FROM            84  '84'
             90_1  COME_FROM            78  '78'

 L. 314        90  LOAD_FAST                'prefix'
               92  LOAD_CONST               None
               94  <117>                 1  ''
               96  POP_JUMP_IF_FALSE   226  'to 226'

 L. 315        98  LOAD_GLOBAL              glob_to_re
              100  LOAD_FAST                'prefix'
              102  CALL_FUNCTION_1       1  ''
              104  STORE_FAST               'prefix_re'

 L. 316       106  LOAD_FAST                'prefix_re'
              108  LOAD_METHOD              startswith
              110  LOAD_FAST                'start'
              112  CALL_METHOD_1         1  ''
              114  POP_JUMP_IF_FALSE   126  'to 126'
              116  LOAD_FAST                'prefix_re'
              118  LOAD_METHOD              endswith
              120  LOAD_FAST                'end'
              122  CALL_METHOD_1         1  ''
              124  POP_JUMP_IF_TRUE    130  'to 130'
            126_0  COME_FROM           114  '114'
              126  <74>             
              128  RAISE_VARARGS_1       1  'exception instance'
            130_0  COME_FROM           124  '124'

 L. 317       130  LOAD_FAST                'prefix_re'
              132  LOAD_GLOBAL              len
              134  LOAD_FAST                'start'
              136  CALL_FUNCTION_1       1  ''
              138  LOAD_GLOBAL              len
              140  LOAD_FAST                'prefix_re'
              142  CALL_FUNCTION_1       1  ''
              144  LOAD_GLOBAL              len
              146  LOAD_FAST                'end'
              148  CALL_FUNCTION_1       1  ''
              150  BINARY_SUBTRACT  
              152  BUILD_SLICE_2         2 
              154  BINARY_SUBSCR    
              156  STORE_FAST               'prefix_re'

 L. 318       158  LOAD_GLOBAL              os
              160  LOAD_ATTR                sep
              162  STORE_FAST               'sep'

 L. 319       164  LOAD_GLOBAL              os
              166  LOAD_ATTR                sep
              168  LOAD_STR                 '\\'
              170  COMPARE_OP               ==
              172  POP_JUMP_IF_FALSE   178  'to 178'

 L. 320       174  LOAD_STR                 '\\\\'
              176  STORE_FAST               'sep'
            178_0  COME_FROM           172  '172'

 L. 321       178  LOAD_FAST                'pattern_re'
              180  LOAD_GLOBAL              len
              182  LOAD_FAST                'start'
              184  CALL_FUNCTION_1       1  ''
              186  LOAD_GLOBAL              len
              188  LOAD_FAST                'pattern_re'
              190  CALL_FUNCTION_1       1  ''
              192  LOAD_GLOBAL              len
              194  LOAD_FAST                'end'
              196  CALL_FUNCTION_1       1  ''
              198  BINARY_SUBTRACT  
              200  BUILD_SLICE_2         2 
              202  BINARY_SUBSCR    
              204  STORE_FAST               'pattern_re'

 L. 322       206  LOAD_STR                 '%s\\A%s%s.*%s%s'
              208  LOAD_FAST                'start'
              210  LOAD_FAST                'prefix_re'
              212  LOAD_FAST                'sep'
              214  LOAD_FAST                'pattern_re'
              216  LOAD_FAST                'end'
              218  BUILD_TUPLE_5         5 
              220  BINARY_MODULO    
              222  STORE_FAST               'pattern_re'
              224  JUMP_FORWARD        256  'to 256'
            226_0  COME_FROM            96  '96'

 L. 324       226  LOAD_FAST                'anchor'
          228_230  POP_JUMP_IF_FALSE   256  'to 256'

 L. 325       232  LOAD_STR                 '%s\\A%s'
              234  LOAD_FAST                'start'
              236  LOAD_FAST                'pattern_re'
              238  LOAD_GLOBAL              len
              240  LOAD_FAST                'start'
              242  CALL_FUNCTION_1       1  ''
              244  LOAD_CONST               None
              246  BUILD_SLICE_2         2 
              248  BINARY_SUBSCR    
              250  BUILD_TUPLE_2         2 
              252  BINARY_MODULO    
              254  STORE_FAST               'pattern_re'
            256_0  COME_FROM           228  '228'
            256_1  COME_FROM           224  '224'

 L. 327       256  LOAD_GLOBAL              re
              258  LOAD_METHOD              compile
              260  LOAD_FAST                'pattern_re'
              262  CALL_METHOD_1         1  ''
              264  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 80