# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: distutils\extension.py
"""distutils.extension

Provides the Extension class, used to describe C/C++ extension
modules in setup scripts."""
import os, warnings

class Extension:
    __doc__ = 'Just a collection of attributes that describes an extension\n    module and everything needed to build it (hopefully in a portable\n    way, but there are hooks that let you be as unportable as you need).\n\n    Instance attributes:\n      name : string\n        the full name of the extension, including any packages -- ie.\n        *not* a filename or pathname, but Python dotted name\n      sources : [string]\n        list of source filenames, relative to the distribution root\n        (where the setup script lives), in Unix form (slash-separated)\n        for portability.  Source files may be C, C++, SWIG (.i),\n        platform-specific resource files, or whatever else is recognized\n        by the "build_ext" command as source for a Python extension.\n      include_dirs : [string]\n        list of directories to search for C/C++ header files (in Unix\n        form for portability)\n      define_macros : [(name : string, value : string|None)]\n        list of macros to define; each macro is defined using a 2-tuple,\n        where \'value\' is either the string to define it to or None to\n        define it without a particular value (equivalent of "#define\n        FOO" in source or -DFOO on Unix C compiler command line)\n      undef_macros : [string]\n        list of macros to undefine explicitly\n      library_dirs : [string]\n        list of directories to search for C/C++ libraries at link time\n      libraries : [string]\n        list of library names (not filenames or paths) to link against\n      runtime_library_dirs : [string]\n        list of directories to search for C/C++ libraries at run time\n        (for shared extensions, this is when the extension is loaded)\n      extra_objects : [string]\n        list of extra files to link with (eg. object files not implied\n        by \'sources\', static library that must be explicitly specified,\n        binary resource files, etc.)\n      extra_compile_args : [string]\n        any extra platform- and compiler-specific information to use\n        when compiling the source files in \'sources\'.  For platforms and\n        compilers where "command line" makes sense, this is typically a\n        list of command-line arguments, but for other platforms it could\n        be anything.\n      extra_link_args : [string]\n        any extra platform- and compiler-specific information to use\n        when linking object files together to create the extension (or\n        to create a new static Python interpreter).  Similar\n        interpretation as for \'extra_compile_args\'.\n      export_symbols : [string]\n        list of symbols to be exported from a shared extension.  Not\n        used on all platforms, and not generally necessary for Python\n        extensions, which typically export exactly one symbol: "init" +\n        extension_name.\n      swig_opts : [string]\n        any extra options to pass to SWIG if a source file has the .i\n        extension.\n      depends : [string]\n        list of files that the extension depends on\n      language : string\n        extension language (i.e. "c", "c++", "objc"). Will be detected\n        from the source extensions if not provided.\n      optional : boolean\n        specifies that a build failure in the extension should not abort the\n        build process, but simply not install the failing extension.\n    '

    def __init__(self, name, sources, include_dirs=None, define_macros=None, undef_macros=None, library_dirs=None, libraries=None, runtime_library_dirs=None, extra_objects=None, extra_compile_args=None, extra_link_args=None, export_symbols=None, swig_opts=None, depends=None, language=None, optional=None, **kw):
        assert isinstance(name, str), "'name' must be a string"
        if not (isinstance(sources, list) and all((isinstance(v, str) for v in sources))):
            raise AssertionError("'sources' must be a list of strings")
        self.name = name
        self.sources = sources
        self.include_dirs = include_dirs or []
        self.define_macros = define_macros or []
        self.undef_macros = undef_macros or []
        self.library_dirs = library_dirs or []
        self.libraries = libraries or []
        self.runtime_library_dirs = runtime_library_dirs or []
        self.extra_objects = extra_objects or []
        self.extra_compile_args = extra_compile_args or []
        self.extra_link_args = extra_link_args or []
        self.export_symbols = export_symbols or []
        self.swig_opts = swig_opts or []
        self.depends = depends or []
        self.language = language
        self.optional = optional
        if len(kw) > 0:
            options = [repr(option) for option in kw]
            options = ', '.join(sorted(options))
            msg = 'Unknown Extension options: %s' % options
            warnings.warn(msg)

    def __repr__(self):
        return '<%s.%s(%r) at %#x>' % (
         self.__class__.__module__,
         self.__class__.__qualname__,
         self.name,
         id(self))


def read_setup_file--- This code section failed: ---

 L. 143         0  LOAD_CONST               0
                2  LOAD_CONST               ('parse_makefile', 'expand_makefile_vars', '_variable_rx')
                4  IMPORT_NAME_ATTR         distutils.sysconfig
                6  IMPORT_FROM              parse_makefile
                8  STORE_FAST               'parse_makefile'
               10  IMPORT_FROM              expand_makefile_vars
               12  STORE_FAST               'expand_makefile_vars'
               14  IMPORT_FROM              _variable_rx
               16  STORE_FAST               '_variable_rx'
               18  POP_TOP          

 L. 146        20  LOAD_CONST               0
               22  LOAD_CONST               ('TextFile',)
               24  IMPORT_NAME_ATTR         distutils.text_file
               26  IMPORT_FROM              TextFile
               28  STORE_FAST               'TextFile'
               30  POP_TOP          

 L. 147        32  LOAD_CONST               0
               34  LOAD_CONST               ('split_quoted',)
               36  IMPORT_NAME_ATTR         distutils.util
               38  IMPORT_FROM              split_quoted
               40  STORE_FAST               'split_quoted'
               42  POP_TOP          

 L. 150        44  LOAD_FAST                'parse_makefile'
               46  LOAD_FAST                'filename'
               48  CALL_FUNCTION_1       1  ''
               50  STORE_FAST               'vars'

 L. 154        52  LOAD_FAST                'TextFile'
               54  LOAD_FAST                'filename'

 L. 155        56  LOAD_CONST               1
               58  LOAD_CONST               1
               60  LOAD_CONST               1

 L. 156        62  LOAD_CONST               1
               64  LOAD_CONST               1

 L. 154        66  LOAD_CONST               ('strip_comments', 'skip_blanks', 'join_lines', 'lstrip_ws', 'rstrip_ws')
               68  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
               70  STORE_FAST               'file'

 L. 157     72_74  SETUP_FINALLY       690  'to 690'

 L. 158        76  BUILD_LIST_0          0 
               78  STORE_FAST               'extensions'

 L. 161        80  LOAD_FAST                'file'
               82  LOAD_METHOD              readline
               84  CALL_METHOD_0         0  ''
               86  STORE_FAST               'line'

 L. 162        88  LOAD_FAST                'line'
               90  LOAD_CONST               None
               92  <117>                 0  ''
               94  POP_JUMP_IF_FALSE   100  'to 100'

 L. 163     96_98  BREAK_LOOP          678  'to 678'
            100_0  COME_FROM            94  '94'

 L. 164       100  LOAD_FAST                '_variable_rx'
              102  LOAD_METHOD              match
              104  LOAD_FAST                'line'
              106  CALL_METHOD_1         1  ''
              108  POP_JUMP_IF_FALSE   112  'to 112'

 L. 165       110  JUMP_BACK            80  'to 80'
            112_0  COME_FROM           108  '108'

 L. 167       112  LOAD_FAST                'line'
              114  LOAD_CONST               0
              116  BINARY_SUBSCR    
              118  LOAD_FAST                'line'
              120  LOAD_CONST               -1
              122  BINARY_SUBSCR    
              124  DUP_TOP          
              126  ROT_THREE        
              128  COMPARE_OP               ==
              130  POP_JUMP_IF_FALSE   140  'to 140'
              132  LOAD_STR                 '*'
              134  COMPARE_OP               ==
              136  POP_JUMP_IF_FALSE   160  'to 160'
              138  JUMP_FORWARD        144  'to 144'
            140_0  COME_FROM           130  '130'
              140  POP_TOP          
              142  JUMP_FORWARD        160  'to 160'
            144_0  COME_FROM           138  '138'

 L. 168       144  LOAD_FAST                'file'
              146  LOAD_METHOD              warn
              148  LOAD_STR                 "'%s' lines not handled yet"
              150  LOAD_FAST                'line'
              152  BINARY_MODULO    
              154  CALL_METHOD_1         1  ''
              156  POP_TOP          

 L. 169       158  JUMP_BACK            80  'to 80'
            160_0  COME_FROM           142  '142'
            160_1  COME_FROM           136  '136'

 L. 171       160  LOAD_FAST                'expand_makefile_vars'
              162  LOAD_FAST                'line'
              164  LOAD_FAST                'vars'
              166  CALL_FUNCTION_2       2  ''
              168  STORE_FAST               'line'

 L. 172       170  LOAD_FAST                'split_quoted'
              172  LOAD_FAST                'line'
              174  CALL_FUNCTION_1       1  ''
              176  STORE_FAST               'words'

 L. 180       178  LOAD_FAST                'words'
              180  LOAD_CONST               0
              182  BINARY_SUBSCR    
              184  STORE_FAST               'module'

 L. 181       186  LOAD_GLOBAL              Extension
              188  LOAD_FAST                'module'
              190  BUILD_LIST_0          0 
              192  CALL_FUNCTION_2       2  ''
              194  STORE_FAST               'ext'

 L. 182       196  LOAD_CONST               None
              198  STORE_FAST               'append_next_word'

 L. 184       200  LOAD_FAST                'words'
              202  LOAD_CONST               1
              204  LOAD_CONST               None
              206  BUILD_SLICE_2         2 
              208  BINARY_SUBSCR    
              210  GET_ITER         
          212_214  FOR_ITER            666  'to 666'
              216  STORE_FAST               'word'

 L. 185       218  LOAD_FAST                'append_next_word'
              220  LOAD_CONST               None
              222  <117>                 1  ''
              224  POP_JUMP_IF_FALSE   242  'to 242'

 L. 186       226  LOAD_FAST                'append_next_word'
              228  LOAD_METHOD              append
              230  LOAD_FAST                'word'
              232  CALL_METHOD_1         1  ''
              234  POP_TOP          

 L. 187       236  LOAD_CONST               None
              238  STORE_FAST               'append_next_word'

 L. 188       240  JUMP_BACK           212  'to 212'
            242_0  COME_FROM           224  '224'

 L. 190       242  LOAD_GLOBAL              os
              244  LOAD_ATTR                path
              246  LOAD_METHOD              splitext
              248  LOAD_FAST                'word'
              250  CALL_METHOD_1         1  ''
              252  LOAD_CONST               1
              254  BINARY_SUBSCR    
              256  STORE_FAST               'suffix'

 L. 191       258  LOAD_FAST                'word'
              260  LOAD_CONST               0
              262  LOAD_CONST               2
              264  BUILD_SLICE_2         2 
              266  BINARY_SUBSCR    
              268  STORE_FAST               'switch'
              270  LOAD_FAST                'word'
              272  LOAD_CONST               2
              274  LOAD_CONST               None
              276  BUILD_SLICE_2         2 
              278  BINARY_SUBSCR    
              280  STORE_FAST               'value'

 L. 193       282  LOAD_FAST                'suffix'
              284  LOAD_CONST               ('.c', '.cc', '.cpp', '.cxx', '.c++', '.m', '.mm')
              286  <118>                 0  ''
          288_290  POP_JUMP_IF_FALSE   306  'to 306'

 L. 197       292  LOAD_FAST                'ext'
              294  LOAD_ATTR                sources
              296  LOAD_METHOD              append
              298  LOAD_FAST                'word'
              300  CALL_METHOD_1         1  ''
              302  POP_TOP          
              304  JUMP_BACK           212  'to 212'
            306_0  COME_FROM           288  '288'

 L. 198       306  LOAD_FAST                'switch'
              308  LOAD_STR                 '-I'
              310  COMPARE_OP               ==
          312_314  POP_JUMP_IF_FALSE   330  'to 330'

 L. 199       316  LOAD_FAST                'ext'
              318  LOAD_ATTR                include_dirs
              320  LOAD_METHOD              append
              322  LOAD_FAST                'value'
              324  CALL_METHOD_1         1  ''
              326  POP_TOP          
              328  JUMP_BACK           212  'to 212'
            330_0  COME_FROM           312  '312'

 L. 200       330  LOAD_FAST                'switch'
              332  LOAD_STR                 '-D'
              334  COMPARE_OP               ==
          336_338  POP_JUMP_IF_FALSE   416  'to 416'

 L. 201       340  LOAD_FAST                'value'
              342  LOAD_METHOD              find
              344  LOAD_STR                 '='
              346  CALL_METHOD_1         1  ''
              348  STORE_FAST               'equals'

 L. 202       350  LOAD_FAST                'equals'
              352  LOAD_CONST               -1
              354  COMPARE_OP               ==
          356_358  POP_JUMP_IF_FALSE   378  'to 378'

 L. 203       360  LOAD_FAST                'ext'
              362  LOAD_ATTR                define_macros
              364  LOAD_METHOD              append
              366  LOAD_FAST                'value'
              368  LOAD_CONST               None
              370  BUILD_TUPLE_2         2 
              372  CALL_METHOD_1         1  ''
              374  POP_TOP          
              376  JUMP_FORWARD        414  'to 414'
            378_0  COME_FROM           356  '356'

 L. 205       378  LOAD_FAST                'ext'
              380  LOAD_ATTR                define_macros
              382  LOAD_METHOD              append
              384  LOAD_FAST                'value'
              386  LOAD_CONST               0
              388  LOAD_FAST                'equals'
              390  BUILD_SLICE_2         2 
              392  BINARY_SUBSCR    

 L. 206       394  LOAD_FAST                'value'
              396  LOAD_FAST                'equals'
              398  LOAD_CONST               2
              400  BINARY_ADD       
              402  LOAD_CONST               None
              404  BUILD_SLICE_2         2 
              406  BINARY_SUBSCR    

 L. 205       408  BUILD_TUPLE_2         2 
              410  CALL_METHOD_1         1  ''
              412  POP_TOP          
            414_0  COME_FROM           376  '376'
              414  JUMP_BACK           212  'to 212'
            416_0  COME_FROM           336  '336'

 L. 207       416  LOAD_FAST                'switch'
              418  LOAD_STR                 '-U'
              420  COMPARE_OP               ==
          422_424  POP_JUMP_IF_FALSE   440  'to 440'

 L. 208       426  LOAD_FAST                'ext'
              428  LOAD_ATTR                undef_macros
              430  LOAD_METHOD              append
              432  LOAD_FAST                'value'
              434  CALL_METHOD_1         1  ''
              436  POP_TOP          
              438  JUMP_BACK           212  'to 212'
            440_0  COME_FROM           422  '422'

 L. 209       440  LOAD_FAST                'switch'
              442  LOAD_STR                 '-C'
              444  COMPARE_OP               ==
          446_448  POP_JUMP_IF_FALSE   464  'to 464'

 L. 210       450  LOAD_FAST                'ext'
              452  LOAD_ATTR                extra_compile_args
              454  LOAD_METHOD              append
              456  LOAD_FAST                'word'
              458  CALL_METHOD_1         1  ''
              460  POP_TOP          
              462  JUMP_BACK           212  'to 212'
            464_0  COME_FROM           446  '446'

 L. 211       464  LOAD_FAST                'switch'
              466  LOAD_STR                 '-l'
              468  COMPARE_OP               ==
          470_472  POP_JUMP_IF_FALSE   488  'to 488'

 L. 212       474  LOAD_FAST                'ext'
              476  LOAD_ATTR                libraries
              478  LOAD_METHOD              append
              480  LOAD_FAST                'value'
              482  CALL_METHOD_1         1  ''
              484  POP_TOP          
              486  JUMP_BACK           212  'to 212'
            488_0  COME_FROM           470  '470'

 L. 213       488  LOAD_FAST                'switch'
              490  LOAD_STR                 '-L'
              492  COMPARE_OP               ==
          494_496  POP_JUMP_IF_FALSE   512  'to 512'

 L. 214       498  LOAD_FAST                'ext'
              500  LOAD_ATTR                library_dirs
              502  LOAD_METHOD              append
              504  LOAD_FAST                'value'
              506  CALL_METHOD_1         1  ''
              508  POP_TOP          
              510  JUMP_BACK           212  'to 212'
            512_0  COME_FROM           494  '494'

 L. 215       512  LOAD_FAST                'switch'
              514  LOAD_STR                 '-R'
              516  COMPARE_OP               ==
          518_520  POP_JUMP_IF_FALSE   536  'to 536'

 L. 216       522  LOAD_FAST                'ext'
              524  LOAD_ATTR                runtime_library_dirs
              526  LOAD_METHOD              append
              528  LOAD_FAST                'value'
              530  CALL_METHOD_1         1  ''
              532  POP_TOP          
              534  JUMP_BACK           212  'to 212'
            536_0  COME_FROM           518  '518'

 L. 217       536  LOAD_FAST                'word'
              538  LOAD_STR                 '-rpath'
              540  COMPARE_OP               ==
          542_544  POP_JUMP_IF_FALSE   554  'to 554'

 L. 218       546  LOAD_FAST                'ext'
              548  LOAD_ATTR                runtime_library_dirs
              550  STORE_FAST               'append_next_word'
              552  JUMP_BACK           212  'to 212'
            554_0  COME_FROM           542  '542'

 L. 219       554  LOAD_FAST                'word'
              556  LOAD_STR                 '-Xlinker'
              558  COMPARE_OP               ==
          560_562  POP_JUMP_IF_FALSE   572  'to 572'

 L. 220       564  LOAD_FAST                'ext'
              566  LOAD_ATTR                extra_link_args
              568  STORE_FAST               'append_next_word'
              570  JUMP_BACK           212  'to 212'
            572_0  COME_FROM           560  '560'

 L. 221       572  LOAD_FAST                'word'
              574  LOAD_STR                 '-Xcompiler'
              576  COMPARE_OP               ==
          578_580  POP_JUMP_IF_FALSE   590  'to 590'

 L. 222       582  LOAD_FAST                'ext'
              584  LOAD_ATTR                extra_compile_args
              586  STORE_FAST               'append_next_word'
              588  JUMP_BACK           212  'to 212'
            590_0  COME_FROM           578  '578'

 L. 223       590  LOAD_FAST                'switch'
              592  LOAD_STR                 '-u'
              594  COMPARE_OP               ==
          596_598  POP_JUMP_IF_FALSE   626  'to 626'

 L. 224       600  LOAD_FAST                'ext'
              602  LOAD_ATTR                extra_link_args
              604  LOAD_METHOD              append
              606  LOAD_FAST                'word'
              608  CALL_METHOD_1         1  ''
              610  POP_TOP          

 L. 225       612  LOAD_FAST                'value'
          614_616  POP_JUMP_IF_TRUE    664  'to 664'

 L. 226       618  LOAD_FAST                'ext'
              620  LOAD_ATTR                extra_link_args
              622  STORE_FAST               'append_next_word'
              624  JUMP_BACK           212  'to 212'
            626_0  COME_FROM           596  '596'

 L. 227       626  LOAD_FAST                'suffix'
              628  LOAD_CONST               ('.a', '.so', '.sl', '.o', '.dylib')
              630  <118>                 0  ''
          632_634  POP_JUMP_IF_FALSE   650  'to 650'

 L. 232       636  LOAD_FAST                'ext'
              638  LOAD_ATTR                extra_objects
              640  LOAD_METHOD              append
              642  LOAD_FAST                'word'
              644  CALL_METHOD_1         1  ''
              646  POP_TOP          
              648  JUMP_BACK           212  'to 212'
            650_0  COME_FROM           632  '632'

 L. 234       650  LOAD_FAST                'file'
              652  LOAD_METHOD              warn
              654  LOAD_STR                 "unrecognized argument '%s'"
              656  LOAD_FAST                'word'
              658  BINARY_MODULO    
              660  CALL_METHOD_1         1  ''
              662  POP_TOP          
            664_0  COME_FROM           614  '614'
              664  JUMP_BACK           212  'to 212'

 L. 236       666  LOAD_FAST                'extensions'
              668  LOAD_METHOD              append
              670  LOAD_FAST                'ext'
              672  CALL_METHOD_1         1  ''
              674  POP_TOP          
              676  JUMP_BACK            80  'to 80'
              678  POP_BLOCK        

 L. 238       680  LOAD_FAST                'file'
              682  LOAD_METHOD              close
              684  CALL_METHOD_0         0  ''
              686  POP_TOP          
              688  JUMP_FORWARD        700  'to 700'
            690_0  COME_FROM_FINALLY    72  '72'
              690  LOAD_FAST                'file'
              692  LOAD_METHOD              close
              694  CALL_METHOD_0         0  ''
              696  POP_TOP          
              698  <48>             
            700_0  COME_FROM           688  '688'

 L. 240       700  LOAD_FAST                'extensions'
              702  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 92