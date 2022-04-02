# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: json\decoder.py
"""Implementation of JSONDecoder
"""
import re
from json import scanner
try:
    from _json import scanstring as c_scanstring
except ImportError:
    c_scanstring = None
else:
    __all__ = [
     'JSONDecoder', 'JSONDecodeError']
    FLAGS = re.VERBOSE | re.MULTILINE | re.DOTALL
    NaN = float('nan')
    PosInf = float('inf')
    NegInf = float('-inf')

    class JSONDecodeError(ValueError):
        __doc__ = 'Subclass of ValueError with the following additional properties:\n\n    msg: The unformatted error message\n    doc: The JSON document being parsed\n    pos: The start index of doc where parsing failed\n    lineno: The line corresponding to pos\n    colno: The column corresponding to pos\n\n    '

        def __init__(self, msg, doc, pos):
            lineno = doc.count('\n', 0, pos) + 1
            colno = pos - doc.rfind('\n', 0, pos)
            errmsg = '%s: line %d column %d (char %d)' % (msg, lineno, colno, pos)
            ValueError.__init__(self, errmsg)
            self.msg = msg
            self.doc = doc
            self.pos = pos
            self.lineno = lineno
            self.colno = colno

        def __reduce__(self):
            return (
             self.__class__, (self.msg, self.doc, self.pos))


    _CONSTANTS = {'-Infinity':NegInf, 
     'Infinity':PosInf, 
     'NaN':NaN}
    STRINGCHUNK = re.compile('(.*?)(["\\\\\\x00-\\x1f])', FLAGS)
    BACKSLASH = {'"':'"', 
     '\\':'\\',  '/':'/',  'b':'\x08', 
     'f':'\x0c',  'n':'\n',  'r':'\r',  't':'\t'}

    def _decode_uXXXX--- This code section failed: ---

 L.  60         0  LOAD_FAST                's'
                2  LOAD_FAST                'pos'
                4  LOAD_CONST               1
                6  BINARY_ADD       
                8  LOAD_FAST                'pos'
               10  LOAD_CONST               5
               12  BINARY_ADD       
               14  BUILD_SLICE_2         2 
               16  BINARY_SUBSCR    
               18  STORE_FAST               'esc'

 L.  61        20  LOAD_GLOBAL              len
               22  LOAD_FAST                'esc'
               24  CALL_FUNCTION_1       1  ''
               26  LOAD_CONST               4
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_FALSE    78  'to 78'
               32  LOAD_FAST                'esc'
               34  LOAD_CONST               1
               36  BINARY_SUBSCR    
               38  LOAD_STR                 'xX'
               40  COMPARE_OP               not-in
               42  POP_JUMP_IF_FALSE    78  'to 78'

 L.  62        44  SETUP_FINALLY        58  'to 58'

 L.  63        46  LOAD_GLOBAL              int
               48  LOAD_FAST                'esc'
               50  LOAD_CONST               16
               52  CALL_FUNCTION_2       2  ''
               54  POP_BLOCK        
               56  RETURN_VALUE     
             58_0  COME_FROM_FINALLY    44  '44'

 L.  64        58  DUP_TOP          
               60  LOAD_GLOBAL              ValueError
               62  COMPARE_OP               exception-match
               64  POP_JUMP_IF_FALSE    76  'to 76'
               66  POP_TOP          
               68  POP_TOP          
               70  POP_TOP          

 L.  65        72  POP_EXCEPT       
               74  JUMP_FORWARD         78  'to 78'
             76_0  COME_FROM            64  '64'
               76  END_FINALLY      
             78_0  COME_FROM            74  '74'
             78_1  COME_FROM            42  '42'
             78_2  COME_FROM            30  '30'

 L.  66        78  LOAD_STR                 'Invalid \\uXXXX escape'
               80  STORE_FAST               'msg'

 L.  67        82  LOAD_GLOBAL              JSONDecodeError
               84  LOAD_FAST                'msg'
               86  LOAD_FAST                's'
               88  LOAD_FAST                'pos'
               90  CALL_FUNCTION_3       3  ''
               92  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `COME_FROM' instruction at offset 76_0


    def py_scanstring(s, end, strict=True, _b=BACKSLASH, _m=STRINGCHUNK.match):
        """Scan the string s for a JSON string. End is the index of the
    character in s after the quote that started the JSON string.
    Unescapes all valid JSON string escape sequences and raises ValueError
    on attempt to decode an invalid string. If strict is False then literal
    control characters are allowed in the string.

    Returns a tuple of the decoded string and the index of the character in s
    after the end quote."""
        chunks = []
        _append = chunks.append
        begin = end - 1
        while True:
            while True:
                chunk = _msend
                if chunk is None:
                    raise JSONDecodeError('Unterminated string starting at', s, begin)
                else:
                    end = chunk.end()
                    content, terminator = chunk.groups()
                    if content:
                        _append(content)
                    if terminator == '"':
                        pass
                    else:
                        break
                    if terminator != '\\':
                        if strict:
                            msg = 'Invalid control character {0!r} at'.format(terminator)
                            raise JSONDecodeError(msg, s, end)
                        else:
                            _append(terminator)

            try:
                esc = s[end]
            except IndexError:
                raise JSONDecodeError('Unterminated string starting at', s, begin) from None
            else:
                if esc != 'u':
                    try:
                        char = _b[esc]
                    except KeyError:
                        msg = 'Invalid \\escape: {0!r}'.format(esc)
                        raise JSONDecodeError(msg, s, end)
                    else:
                        end += 1
                else:
                    uni = _decode_uXXXXsend
                    end += 5
                    if 55296 <= uni <= 56319:
                        if s[end:end + 2] == '\\u':
                            uni2 = _decode_uXXXXs(end + 1)
                            if 56320 <= uni2 <= 57343:
                                uni = 65536 + (uni - 55296 << 10 | uni2 - 56320)
                                end += 6
                    char = chr(uni)
                _append(char)

        return (
         ''.join(chunks), end)


    scanstring = c_scanstring or py_scanstring
    WHITESPACE = re.compile('[ \\t\\n\\r]*', FLAGS)
    WHITESPACE_STR = ' \t\n\r'

    def JSONObject--- This code section failed: ---

 L. 138         0  LOAD_FAST                's_and_end'
                2  UNPACK_SEQUENCE_2     2 
                4  STORE_FAST               's'
                6  STORE_FAST               'end'

 L. 139         8  BUILD_LIST_0          0 
               10  STORE_FAST               'pairs'

 L. 140        12  LOAD_FAST                'pairs'
               14  LOAD_ATTR                append
               16  STORE_FAST               'pairs_append'

 L. 142        18  LOAD_FAST                'memo'
               20  LOAD_CONST               None
               22  COMPARE_OP               is
               24  POP_JUMP_IF_FALSE    30  'to 30'

 L. 143        26  BUILD_MAP_0           0 
               28  STORE_FAST               'memo'
             30_0  COME_FROM            24  '24'

 L. 144        30  LOAD_FAST                'memo'
               32  LOAD_ATTR                setdefault
               34  STORE_FAST               'memo_get'

 L. 147        36  LOAD_FAST                's'
               38  LOAD_FAST                'end'
               40  LOAD_FAST                'end'
               42  LOAD_CONST               1
               44  BINARY_ADD       
               46  BUILD_SLICE_2         2 
               48  BINARY_SUBSCR    
               50  STORE_FAST               'nextchar'

 L. 149        52  LOAD_FAST                'nextchar'
               54  LOAD_STR                 '"'
               56  COMPARE_OP               !=
               58  POP_JUMP_IF_FALSE   186  'to 186'

 L. 150        60  LOAD_FAST                'nextchar'
               62  LOAD_FAST                '_ws'
               64  COMPARE_OP               in
               66  POP_JUMP_IF_FALSE    98  'to 98'

 L. 151        68  LOAD_FAST                '_w'
               70  LOAD_FAST                's'
               72  LOAD_FAST                'end'
               74  CALL_FUNCTION_2       2  ''
               76  LOAD_METHOD              end
               78  CALL_METHOD_0         0  ''
               80  STORE_FAST               'end'

 L. 152        82  LOAD_FAST                's'
               84  LOAD_FAST                'end'
               86  LOAD_FAST                'end'
               88  LOAD_CONST               1
               90  BINARY_ADD       
               92  BUILD_SLICE_2         2 
               94  BINARY_SUBSCR    
               96  STORE_FAST               'nextchar'
             98_0  COME_FROM            66  '66'

 L. 154        98  LOAD_FAST                'nextchar'
              100  LOAD_STR                 '}'
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_FALSE   166  'to 166'

 L. 155       106  LOAD_FAST                'object_pairs_hook'
              108  LOAD_CONST               None
              110  COMPARE_OP               is-not
              112  POP_JUMP_IF_FALSE   134  'to 134'

 L. 156       114  LOAD_FAST                'object_pairs_hook'
              116  LOAD_FAST                'pairs'
              118  CALL_FUNCTION_1       1  ''
              120  STORE_FAST               'result'

 L. 157       122  LOAD_FAST                'result'
              124  LOAD_FAST                'end'
              126  LOAD_CONST               1
              128  BINARY_ADD       
              130  BUILD_TUPLE_2         2 
              132  RETURN_VALUE     
            134_0  COME_FROM           112  '112'

 L. 158       134  BUILD_MAP_0           0 
              136  STORE_FAST               'pairs'

 L. 159       138  LOAD_FAST                'object_hook'
              140  LOAD_CONST               None
              142  COMPARE_OP               is-not
              144  POP_JUMP_IF_FALSE   154  'to 154'

 L. 160       146  LOAD_FAST                'object_hook'
              148  LOAD_FAST                'pairs'
              150  CALL_FUNCTION_1       1  ''
              152  STORE_FAST               'pairs'
            154_0  COME_FROM           144  '144'

 L. 161       154  LOAD_FAST                'pairs'
              156  LOAD_FAST                'end'
              158  LOAD_CONST               1
              160  BINARY_ADD       
              162  BUILD_TUPLE_2         2 
              164  RETURN_VALUE     
            166_0  COME_FROM           104  '104'

 L. 162       166  LOAD_FAST                'nextchar'
              168  LOAD_STR                 '"'
              170  COMPARE_OP               !=
              172  POP_JUMP_IF_FALSE   186  'to 186'

 L. 163       174  LOAD_GLOBAL              JSONDecodeError

 L. 164       176  LOAD_STR                 'Expecting property name enclosed in double quotes'

 L. 164       178  LOAD_FAST                's'

 L. 164       180  LOAD_FAST                'end'

 L. 163       182  CALL_FUNCTION_3       3  ''
              184  RAISE_VARARGS_1       1  'exception instance'
            186_0  COME_FROM           172  '172'
            186_1  COME_FROM            58  '58'

 L. 165       186  LOAD_FAST                'end'
              188  LOAD_CONST               1
              190  INPLACE_ADD      
              192  STORE_FAST               'end'
            194_0  COME_FROM           652  '652'
            194_1  COME_FROM           634  '634'

 L. 167       194  LOAD_GLOBAL              scanstring
              196  LOAD_FAST                's'
              198  LOAD_FAST                'end'
              200  LOAD_FAST                'strict'
              202  CALL_FUNCTION_3       3  ''
              204  UNPACK_SEQUENCE_2     2 
              206  STORE_FAST               'key'
              208  STORE_FAST               'end'

 L. 168       210  LOAD_FAST                'memo_get'
              212  LOAD_FAST                'key'
              214  LOAD_FAST                'key'
              216  CALL_FUNCTION_2       2  ''
              218  STORE_FAST               'key'

 L. 171       220  LOAD_FAST                's'
              222  LOAD_FAST                'end'
              224  LOAD_FAST                'end'
              226  LOAD_CONST               1
              228  BINARY_ADD       
              230  BUILD_SLICE_2         2 
              232  BINARY_SUBSCR    
              234  LOAD_STR                 ':'
              236  COMPARE_OP               !=
          238_240  POP_JUMP_IF_FALSE   290  'to 290'

 L. 172       242  LOAD_FAST                '_w'
              244  LOAD_FAST                's'
              246  LOAD_FAST                'end'
              248  CALL_FUNCTION_2       2  ''
              250  LOAD_METHOD              end
              252  CALL_METHOD_0         0  ''
              254  STORE_FAST               'end'

 L. 173       256  LOAD_FAST                's'
              258  LOAD_FAST                'end'
              260  LOAD_FAST                'end'
              262  LOAD_CONST               1
              264  BINARY_ADD       
              266  BUILD_SLICE_2         2 
              268  BINARY_SUBSCR    
              270  LOAD_STR                 ':'
              272  COMPARE_OP               !=
          274_276  POP_JUMP_IF_FALSE   290  'to 290'

 L. 174       278  LOAD_GLOBAL              JSONDecodeError
              280  LOAD_STR                 "Expecting ':' delimiter"
              282  LOAD_FAST                's'
              284  LOAD_FAST                'end'
              286  CALL_FUNCTION_3       3  ''
              288  RAISE_VARARGS_1       1  'exception instance'
            290_0  COME_FROM           274  '274'
            290_1  COME_FROM           238  '238'

 L. 175       290  LOAD_FAST                'end'
              292  LOAD_CONST               1
              294  INPLACE_ADD      
              296  STORE_FAST               'end'

 L. 177       298  SETUP_FINALLY       358  'to 358'

 L. 178       300  LOAD_FAST                's'
              302  LOAD_FAST                'end'
              304  BINARY_SUBSCR    
              306  LOAD_FAST                '_ws'
              308  COMPARE_OP               in
          310_312  POP_JUMP_IF_FALSE   354  'to 354'

 L. 179       314  LOAD_FAST                'end'
              316  LOAD_CONST               1
              318  INPLACE_ADD      
              320  STORE_FAST               'end'

 L. 180       322  LOAD_FAST                's'
              324  LOAD_FAST                'end'
              326  BINARY_SUBSCR    
              328  LOAD_FAST                '_ws'
              330  COMPARE_OP               in
          332_334  POP_JUMP_IF_FALSE   354  'to 354'

 L. 181       336  LOAD_FAST                '_w'
              338  LOAD_FAST                's'
              340  LOAD_FAST                'end'
              342  LOAD_CONST               1
              344  BINARY_ADD       
              346  CALL_FUNCTION_2       2  ''
              348  LOAD_METHOD              end
              350  CALL_METHOD_0         0  ''
              352  STORE_FAST               'end'
            354_0  COME_FROM           332  '332'
            354_1  COME_FROM           310  '310'
              354  POP_BLOCK        
              356  JUMP_FORWARD        380  'to 380'
            358_0  COME_FROM_FINALLY   298  '298'

 L. 182       358  DUP_TOP          
              360  LOAD_GLOBAL              IndexError
              362  COMPARE_OP               exception-match
          364_366  POP_JUMP_IF_FALSE   378  'to 378'
              368  POP_TOP          
              370  POP_TOP          
              372  POP_TOP          

 L. 183       374  POP_EXCEPT       
              376  BREAK_LOOP          380  'to 380'
            378_0  COME_FROM           364  '364'
              378  END_FINALLY      
            380_0  COME_FROM           376  '376'
            380_1  COME_FROM           356  '356'

 L. 185       380  SETUP_FINALLY       400  'to 400'

 L. 186       382  LOAD_FAST                'scan_once'
              384  LOAD_FAST                's'
              386  LOAD_FAST                'end'
              388  CALL_FUNCTION_2       2  ''
              390  UNPACK_SEQUENCE_2     2 
              392  STORE_FAST               'value'
              394  STORE_FAST               'end'
              396  POP_BLOCK        
              398  JUMP_FORWARD        452  'to 452'
            400_0  COME_FROM_FINALLY   380  '380'

 L. 187       400  DUP_TOP          
              402  LOAD_GLOBAL              StopIteration
              404  COMPARE_OP               exception-match
          406_408  POP_JUMP_IF_FALSE   450  'to 450'
              410  POP_TOP          
              412  STORE_FAST               'err'
              414  POP_TOP          
              416  SETUP_FINALLY       438  'to 438'

 L. 188       418  LOAD_GLOBAL              JSONDecodeError
              420  LOAD_STR                 'Expecting value'
              422  LOAD_FAST                's'
              424  LOAD_FAST                'err'
              426  LOAD_ATTR                value
              428  CALL_FUNCTION_3       3  ''
              430  LOAD_CONST               None
              432  RAISE_VARARGS_2       2  'exception instance with __cause__'
              434  POP_BLOCK        
              436  BEGIN_FINALLY    
            438_0  COME_FROM_FINALLY   416  '416'
              438  LOAD_CONST               None
              440  STORE_FAST               'err'
              442  DELETE_FAST              'err'
              444  END_FINALLY      
              446  POP_EXCEPT       
              448  JUMP_FORWARD        452  'to 452'
            450_0  COME_FROM           406  '406'
              450  END_FINALLY      
            452_0  COME_FROM           448  '448'
            452_1  COME_FROM           398  '398'

 L. 189       452  LOAD_FAST                'pairs_append'
              454  LOAD_FAST                'key'
              456  LOAD_FAST                'value'
              458  BUILD_TUPLE_2         2 
              460  CALL_FUNCTION_1       1  ''
              462  POP_TOP          

 L. 190       464  SETUP_FINALLY       514  'to 514'

 L. 191       466  LOAD_FAST                's'
              468  LOAD_FAST                'end'
              470  BINARY_SUBSCR    
              472  STORE_FAST               'nextchar'

 L. 192       474  LOAD_FAST                'nextchar'
              476  LOAD_FAST                '_ws'
              478  COMPARE_OP               in
          480_482  POP_JUMP_IF_FALSE   510  'to 510'

 L. 193       484  LOAD_FAST                '_w'
              486  LOAD_FAST                's'
              488  LOAD_FAST                'end'
              490  LOAD_CONST               1
              492  BINARY_ADD       
              494  CALL_FUNCTION_2       2  ''
              496  LOAD_METHOD              end
              498  CALL_METHOD_0         0  ''
              500  STORE_FAST               'end'

 L. 194       502  LOAD_FAST                's'
              504  LOAD_FAST                'end'
              506  BINARY_SUBSCR    
              508  STORE_FAST               'nextchar'
            510_0  COME_FROM           480  '480'
              510  POP_BLOCK        
              512  JUMP_FORWARD        540  'to 540'
            514_0  COME_FROM_FINALLY   464  '464'

 L. 195       514  DUP_TOP          
              516  LOAD_GLOBAL              IndexError
              518  COMPARE_OP               exception-match
          520_522  POP_JUMP_IF_FALSE   538  'to 538'
              524  POP_TOP          
              526  POP_TOP          
              528  POP_TOP          

 L. 196       530  LOAD_STR                 ''
              532  STORE_FAST               'nextchar'
              534  POP_EXCEPT       
              536  JUMP_FORWARD        540  'to 540'
            538_0  COME_FROM           520  '520'
              538  END_FINALLY      
            540_0  COME_FROM           536  '536'
            540_1  COME_FROM           512  '512'

 L. 197       540  LOAD_FAST                'end'
              542  LOAD_CONST               1
              544  INPLACE_ADD      
              546  STORE_FAST               'end'

 L. 199       548  LOAD_FAST                'nextchar'
              550  LOAD_STR                 '}'
              552  COMPARE_OP               ==
          554_556  POP_JUMP_IF_FALSE   564  'to 564'

 L. 200   558_560  JUMP_FORWARD        654  'to 654'
              562  BREAK_LOOP          590  'to 590'
            564_0  COME_FROM           554  '554'

 L. 201       564  LOAD_FAST                'nextchar'
              566  LOAD_STR                 ','
              568  COMPARE_OP               !=
          570_572  POP_JUMP_IF_FALSE   590  'to 590'

 L. 202       574  LOAD_GLOBAL              JSONDecodeError
              576  LOAD_STR                 "Expecting ',' delimiter"
              578  LOAD_FAST                's'
              580  LOAD_FAST                'end'
              582  LOAD_CONST               1
              584  BINARY_SUBTRACT  
              586  CALL_FUNCTION_3       3  ''
              588  RAISE_VARARGS_1       1  'exception instance'
            590_0  COME_FROM           570  '570'
            590_1  COME_FROM           562  '562'

 L. 203       590  LOAD_FAST                '_w'
              592  LOAD_FAST                's'
              594  LOAD_FAST                'end'
              596  CALL_FUNCTION_2       2  ''
              598  LOAD_METHOD              end
              600  CALL_METHOD_0         0  ''
              602  STORE_FAST               'end'

 L. 204       604  LOAD_FAST                's'
              606  LOAD_FAST                'end'
              608  LOAD_FAST                'end'
              610  LOAD_CONST               1
              612  BINARY_ADD       
              614  BUILD_SLICE_2         2 
              616  BINARY_SUBSCR    
              618  STORE_FAST               'nextchar'

 L. 205       620  LOAD_FAST                'end'
              622  LOAD_CONST               1
              624  INPLACE_ADD      
              626  STORE_FAST               'end'

 L. 206       628  LOAD_FAST                'nextchar'
              630  LOAD_STR                 '"'
              632  COMPARE_OP               !=
              634  POP_JUMP_IF_FALSE_BACK   194  'to 194'

 L. 207       636  LOAD_GLOBAL              JSONDecodeError

 L. 208       638  LOAD_STR                 'Expecting property name enclosed in double quotes'

 L. 208       640  LOAD_FAST                's'

 L. 208       642  LOAD_FAST                'end'
              644  LOAD_CONST               1
              646  BINARY_SUBTRACT  

 L. 207       648  CALL_FUNCTION_3       3  ''
              650  RAISE_VARARGS_1       1  'exception instance'
              652  JUMP_BACK           194  'to 194'
            654_0  COME_FROM           558  '558'

 L. 209       654  LOAD_FAST                'object_pairs_hook'
              656  LOAD_CONST               None
              658  COMPARE_OP               is-not
          660_662  POP_JUMP_IF_FALSE   680  'to 680'

 L. 210       664  LOAD_FAST                'object_pairs_hook'
              666  LOAD_FAST                'pairs'
              668  CALL_FUNCTION_1       1  ''
              670  STORE_FAST               'result'

 L. 211       672  LOAD_FAST                'result'
              674  LOAD_FAST                'end'
              676  BUILD_TUPLE_2         2 
              678  RETURN_VALUE     
            680_0  COME_FROM           660  '660'

 L. 212       680  LOAD_GLOBAL              dict
              682  LOAD_FAST                'pairs'
              684  CALL_FUNCTION_1       1  ''
              686  STORE_FAST               'pairs'

 L. 213       688  LOAD_FAST                'object_hook'
              690  LOAD_CONST               None
              692  COMPARE_OP               is-not
          694_696  POP_JUMP_IF_FALSE   706  'to 706'

 L. 214       698  LOAD_FAST                'object_hook'
              700  LOAD_FAST                'pairs'
              702  CALL_FUNCTION_1       1  ''
              704  STORE_FAST               'pairs'
            706_0  COME_FROM           694  '694'

 L. 215       706  LOAD_FAST                'pairs'
              708  LOAD_FAST                'end'
              710  BUILD_TUPLE_2         2 
              712  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `END_FINALLY' instruction at offset 378


    def JSONArray(s_and_end, scan_once, _w=WHITESPACE.match, _ws=WHITESPACE_STR):
        s, end = s_and_end
        values = []
        nextchar = s[end:end + 1]
        if nextchar in _ws:
            end = _ws(end + 1).end()
            nextchar = s[end:end + 1]
        if nextchar == ']':
            return (values, end + 1)
        _append = values.append
        while True:
            try:
                value, end = scan_oncesend
            except StopIteration as err:
                try:
                    raise JSONDecodeError('Expecting value', s, err.value) from None
                finally:
                    err = None
                    del err

            else:
                _append(value)
                nextchar = s[end:end + 1]
                if nextchar in _ws:
                    end = _ws(end + 1).end()
                    nextchar = s[end:end + 1]
                end += 1
                if nextchar == ']':
                    pass
                else:
                    break
                if nextchar != ',':
                    raise JSONDecodeError("Expecting ',' delimiter", s, end - 1)
            try:
                if s[end] in _ws:
                    end += 1
                    if s[end] in _ws:
                        end = _ws(end + 1).end()
            except IndexError:
                pass

        return (
         values, end)


    class JSONDecoder(object):
        __doc__ = 'Simple JSON <http://json.org> decoder\n\n    Performs the following translations in decoding by default:\n\n    +---------------+-------------------+\n    | JSON          | Python            |\n    +===============+===================+\n    | object        | dict              |\n    +---------------+-------------------+\n    | array         | list              |\n    +---------------+-------------------+\n    | string        | str               |\n    +---------------+-------------------+\n    | number (int)  | int               |\n    +---------------+-------------------+\n    | number (real) | float             |\n    +---------------+-------------------+\n    | true          | True              |\n    +---------------+-------------------+\n    | false         | False             |\n    +---------------+-------------------+\n    | null          | None              |\n    +---------------+-------------------+\n\n    It also understands ``NaN``, ``Infinity``, and ``-Infinity`` as\n    their corresponding ``float`` values, which is outside the JSON spec.\n\n    '

        def __init__(self, *, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, strict=True, object_pairs_hook=None):
            r"""``object_hook``, if specified, will be called with the result
        of every JSON object decoded and its return value will be used in
        place of the given ``dict``.  This can be used to provide custom
        deserializations (e.g. to support JSON-RPC class hinting).

        ``object_pairs_hook``, if specified will be called with the result of
        every JSON object decoded with an ordered list of pairs.  The return
        value of ``object_pairs_hook`` will be used instead of the ``dict``.
        This feature can be used to implement custom decoders.
        If ``object_hook`` is also defined, the ``object_pairs_hook`` takes
        priority.

        ``parse_float``, if specified, will be called with the string
        of every JSON float to be decoded. By default this is equivalent to
        float(num_str). This can be used to use another datatype or parser
        for JSON floats (e.g. decimal.Decimal).

        ``parse_int``, if specified, will be called with the string
        of every JSON int to be decoded. By default this is equivalent to
        int(num_str). This can be used to use another datatype or parser
        for JSON integers (e.g. float).

        ``parse_constant``, if specified, will be called with one of the
        following strings: -Infinity, Infinity, NaN.
        This can be used to raise an exception if invalid JSON numbers
        are encountered.

        If ``strict`` is false (true is the default), then control
        characters will be allowed inside strings.  Control characters in
        this context are those with character codes in the 0-31 range,
        including ``'\t'`` (tab), ``'\n'``, ``'\r'`` and ``'\0'``.
        """
            self.object_hook = object_hook
            self.parse_float = parse_float or float
            self.parse_int = parse_int or int
            self.parse_constant = parse_constant or _CONSTANTS.__getitem__
            self.strict = strict
            self.object_pairs_hook = object_pairs_hook
            self.parse_object = JSONObject
            self.parse_array = JSONArray
            self.parse_string = scanstring
            self.memo = {}
            self.scan_once = scanner.make_scanner(self)

        def decode(self, s, _w=WHITESPACE.match):
            """Return the Python representation of ``s`` (a ``str`` instance
        containing a JSON document).

        """
            obj, end = self.raw_decode(s, idx=(_ws0.end()))
            end = _wsend.end()
            if end != len(s):
                raise JSONDecodeError('Extra data', s, end)
            return obj

        def raw_decode(self, s, idx=0):
            """Decode a JSON document from ``s`` (a ``str`` beginning with
        a JSON document) and return a 2-tuple of the Python
        representation and the index in ``s`` where the document ended.

        This can be used to decode a JSON document from a string that may
        have extraneous data at the end.

        """
            try:
                obj, end = self.scan_once(s, idx)
            except StopIteration as err:
                try:
                    raise JSONDecodeError('Expecting value', s, err.value) from None
                finally:
                    err = None
                    del err

            else:
                return (
                 obj, end)