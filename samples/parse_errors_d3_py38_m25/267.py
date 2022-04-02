# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: xml\etree\ElementInclude.py
import copy
from . import ElementTree
XINCLUDE = '{http://www.w3.org/2001/XInclude}'
XINCLUDE_INCLUDE = XINCLUDE + 'include'
XINCLUDE_FALLBACK = XINCLUDE + 'fallback'

class FatalIncludeError(SyntaxError):
    pass


def default_loader(href, parse, encoding=None):
    if parse == 'xml':
        with open(href, 'rb') as file:
            data = ElementTree.parse(file).getroot()
    else:
        if not encoding:
            encoding = 'UTF-8'
        with open(href, 'r', encoding=encoding) as file:
            data = file.read()
    return data


def include--- This code section failed: ---

 L. 100         0  LOAD_FAST                'loader'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 101         8  LOAD_GLOBAL              default_loader
               10  STORE_FAST               'loader'
             12_0  COME_FROM             6  '6'

 L. 103        12  LOAD_CONST               0
               14  STORE_FAST               'i'
             16_0  COME_FROM           354  '354'
             16_1  COME_FROM           290  '290'

 L. 104        16  LOAD_FAST                'i'
               18  LOAD_GLOBAL              len
               20  LOAD_FAST                'elem'
               22  CALL_FUNCTION_1       1  ''
               24  COMPARE_OP               <
            26_28  POP_JUMP_IF_FALSE   356  'to 356'

 L. 105        30  LOAD_FAST                'elem'
               32  LOAD_FAST                'i'
               34  BINARY_SUBSCR    
               36  STORE_FAST               'e'

 L. 106        38  LOAD_FAST                'e'
               40  LOAD_ATTR                tag
               42  LOAD_GLOBAL              XINCLUDE_INCLUDE
               44  COMPARE_OP               ==
            46_48  POP_JUMP_IF_FALSE   308  'to 308'

 L. 108        50  LOAD_FAST                'e'
               52  LOAD_METHOD              get
               54  LOAD_STR                 'href'
               56  CALL_METHOD_1         1  ''
               58  STORE_FAST               'href'

 L. 109        60  LOAD_FAST                'e'
               62  LOAD_METHOD              get
               64  LOAD_STR                 'parse'
               66  LOAD_STR                 'xml'
               68  CALL_METHOD_2         2  ''
               70  STORE_FAST               'parse'

 L. 110        72  LOAD_FAST                'parse'
               74  LOAD_STR                 'xml'
               76  COMPARE_OP               ==
               78  POP_JUMP_IF_FALSE   158  'to 158'

 L. 111        80  LOAD_FAST                'loader'
               82  LOAD_FAST                'href'
               84  LOAD_FAST                'parse'
               86  CALL_FUNCTION_2       2  ''
               88  STORE_FAST               'node'

 L. 112        90  LOAD_FAST                'node'
               92  LOAD_CONST               None
               94  COMPARE_OP               is
               96  POP_JUMP_IF_FALSE   114  'to 114'

 L. 113        98  LOAD_GLOBAL              FatalIncludeError

 L. 114       100  LOAD_STR                 'cannot load %r as %r'
              102  LOAD_FAST                'href'
              104  LOAD_FAST                'parse'
              106  BUILD_TUPLE_2         2 
              108  BINARY_MODULO    

 L. 113       110  CALL_FUNCTION_1       1  ''
              112  RAISE_VARARGS_1       1  'exception instance'
            114_0  COME_FROM            96  '96'

 L. 116       114  LOAD_GLOBAL              copy
              116  LOAD_METHOD              copy
              118  LOAD_FAST                'node'
              120  CALL_METHOD_1         1  ''
              122  STORE_FAST               'node'

 L. 117       124  LOAD_FAST                'e'
              126  LOAD_ATTR                tail
              128  POP_JUMP_IF_FALSE   148  'to 148'

 L. 118       130  LOAD_FAST                'node'
              132  LOAD_ATTR                tail
              134  JUMP_IF_TRUE_OR_POP   138  'to 138'
              136  LOAD_STR                 ''
            138_0  COME_FROM           134  '134'
              138  LOAD_FAST                'e'
              140  LOAD_ATTR                tail
              142  BINARY_ADD       
              144  LOAD_FAST                'node'
              146  STORE_ATTR               tail
            148_0  COME_FROM           128  '128'

 L. 119       148  LOAD_FAST                'node'
              150  LOAD_FAST                'elem'
              152  LOAD_FAST                'i'
              154  STORE_SUBSCR     
              156  JUMP_FORWARD        306  'to 306'
            158_0  COME_FROM            78  '78'

 L. 120       158  LOAD_FAST                'parse'
              160  LOAD_STR                 'text'
              162  COMPARE_OP               ==
          164_166  POP_JUMP_IF_FALSE   294  'to 294'

 L. 121       168  LOAD_FAST                'loader'
              170  LOAD_FAST                'href'
              172  LOAD_FAST                'parse'
              174  LOAD_FAST                'e'
              176  LOAD_METHOD              get
              178  LOAD_STR                 'encoding'
              180  CALL_METHOD_1         1  ''
              182  CALL_FUNCTION_3       3  ''
              184  STORE_FAST               'text'

 L. 122       186  LOAD_FAST                'text'
              188  LOAD_CONST               None
              190  COMPARE_OP               is
              192  POP_JUMP_IF_FALSE   210  'to 210'

 L. 123       194  LOAD_GLOBAL              FatalIncludeError

 L. 124       196  LOAD_STR                 'cannot load %r as %r'
              198  LOAD_FAST                'href'
              200  LOAD_FAST                'parse'
              202  BUILD_TUPLE_2         2 
              204  BINARY_MODULO    

 L. 123       206  CALL_FUNCTION_1       1  ''
              208  RAISE_VARARGS_1       1  'exception instance'
            210_0  COME_FROM           192  '192'

 L. 126       210  LOAD_FAST                'i'
              212  POP_JUMP_IF_FALSE   254  'to 254'

 L. 127       214  LOAD_FAST                'elem'
              216  LOAD_FAST                'i'
              218  LOAD_CONST               1
              220  BINARY_SUBTRACT  
              222  BINARY_SUBSCR    
              224  STORE_FAST               'node'

 L. 128       226  LOAD_FAST                'node'
              228  LOAD_ATTR                tail
              230  JUMP_IF_TRUE_OR_POP   234  'to 234'
              232  LOAD_STR                 ''
            234_0  COME_FROM           230  '230'
              234  LOAD_FAST                'text'
              236  BINARY_ADD       
              238  LOAD_FAST                'e'
              240  LOAD_ATTR                tail
              242  JUMP_IF_TRUE_OR_POP   246  'to 246'
              244  LOAD_STR                 ''
            246_0  COME_FROM           242  '242'
              246  BINARY_ADD       
              248  LOAD_FAST                'node'
              250  STORE_ATTR               tail
              252  JUMP_FORWARD        284  'to 284'
            254_0  COME_FROM           212  '212'

 L. 130       254  LOAD_FAST                'elem'
              256  LOAD_ATTR                text
          258_260  JUMP_IF_TRUE_OR_POP   264  'to 264'
              262  LOAD_STR                 ''
            264_0  COME_FROM           258  '258'
              264  LOAD_FAST                'text'
              266  BINARY_ADD       
              268  LOAD_FAST                'e'
              270  LOAD_ATTR                tail
          272_274  JUMP_IF_TRUE_OR_POP   278  'to 278'
              276  LOAD_STR                 ''
            278_0  COME_FROM           272  '272'
              278  BINARY_ADD       
              280  LOAD_FAST                'elem'
              282  STORE_ATTR               text
            284_0  COME_FROM           252  '252'

 L. 131       284  LOAD_FAST                'elem'
              286  LOAD_FAST                'i'
              288  DELETE_SUBSCR    

 L. 132       290  JUMP_BACK            16  'to 16'
              292  BREAK_LOOP          306  'to 306'
            294_0  COME_FROM           164  '164'

 L. 134       294  LOAD_GLOBAL              FatalIncludeError

 L. 135       296  LOAD_STR                 'unknown parse type in xi:include tag (%r)'
              298  LOAD_FAST                'parse'
              300  BINARY_MODULO    

 L. 134       302  CALL_FUNCTION_1       1  ''
              304  RAISE_VARARGS_1       1  'exception instance'
            306_0  COME_FROM           292  '292'
            306_1  COME_FROM           156  '156'
              306  JUMP_FORWARD        346  'to 346'
            308_0  COME_FROM            46  '46'

 L. 137       308  LOAD_FAST                'e'
              310  LOAD_ATTR                tag
              312  LOAD_GLOBAL              XINCLUDE_FALLBACK
              314  COMPARE_OP               ==
          316_318  POP_JUMP_IF_FALSE   336  'to 336'

 L. 138       320  LOAD_GLOBAL              FatalIncludeError

 L. 139       322  LOAD_STR                 'xi:fallback tag must be child of xi:include (%r)'
              324  LOAD_FAST                'e'
              326  LOAD_ATTR                tag
              328  BINARY_MODULO    

 L. 138       330  CALL_FUNCTION_1       1  ''
              332  RAISE_VARARGS_1       1  'exception instance'
              334  JUMP_FORWARD        346  'to 346'
            336_0  COME_FROM           316  '316'

 L. 142       336  LOAD_GLOBAL              include
              338  LOAD_FAST                'e'
              340  LOAD_FAST                'loader'
              342  CALL_FUNCTION_2       2  ''
              344  POP_TOP          
            346_0  COME_FROM           334  '334'
            346_1  COME_FROM           306  '306'

 L. 143       346  LOAD_FAST                'i'
              348  LOAD_CONST               1
              350  BINARY_ADD       
              352  STORE_FAST               'i'
              354  JUMP_BACK            16  'to 16'
            356_0  COME_FROM            26  '26'

Parse error at or near `JUMP_FORWARD' instruction at offset 306