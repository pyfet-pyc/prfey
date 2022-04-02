# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: _markupbase.py
"""Shared support for scanning document type declarations in HTML and XHTML.

This module is used as a foundation for the html.parser module.  It has no
documented public API and should not be used directly.

"""
import re
_declname_match = re.compile('[a-zA-Z][-_.a-zA-Z0-9]*\\s*').match
_declstringlit_match = re.compile('(\\\'[^\\\']*\\\'|"[^"]*")\\s*').match
_commentclose = re.compile('--\\s*>')
_markedsectionclose = re.compile(']\\s*]\\s*>')
_msmarkedsectionclose = re.compile(']\\s*>')
del re

class ParserBase:
    __doc__ = 'Parser base class which provides some common support methods used\n    by the SGML/HTML and XHTML parsers.'

    def __init__--- This code section failed: ---

 L.  28         0  LOAD_FAST                'self'
                2  LOAD_ATTR                __class__
                4  LOAD_GLOBAL              ParserBase
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L.  29        10  LOAD_GLOBAL              RuntimeError

 L.  30        12  LOAD_STR                 '_markupbase.ParserBase must be subclassed'

 L.  29        14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    def error(self, message):
        raise NotImplementedError('subclasses of ParserBase must override error()')

    def reset(self):
        self.lineno = 1
        self.offset = 0

    def getpos(self):
        """Return current line number and offset."""
        return (
         self.lineno, self.offset)

    def updatepos(self, i, j):
        if i >= j:
            return j
        else:
            rawdata = self.rawdata
            nlines = rawdata.count('\n', i, j)
            if nlines:
                self.lineno = self.lineno + nlines
                pos = rawdata.rindex('\n', i, j)
                self.offset = j - (pos + 1)
            else:
                self.offset = self.offset + j - i
        return j

    _decl_otherchars = ''

    def parse_declaration--- This code section failed: ---

 L.  75         0  LOAD_FAST                'self'
                2  LOAD_ATTR                rawdata
                4  STORE_FAST               'rawdata'

 L.  76         6  LOAD_FAST                'i'
                8  LOAD_CONST               2
               10  BINARY_ADD       
               12  STORE_FAST               'j'

 L.  77        14  LOAD_FAST                'rawdata'
               16  LOAD_FAST                'i'
               18  LOAD_FAST                'j'
               20  BUILD_SLICE_2         2 
               22  BINARY_SUBSCR    
               24  LOAD_STR                 '<!'
               26  COMPARE_OP               ==
               28  POP_JUMP_IF_TRUE     38  'to 38'
               30  <74>             
               32  LOAD_STR                 'unexpected call to parse_declaration'
               34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            28  '28'

 L.  78        38  LOAD_FAST                'rawdata'
               40  LOAD_FAST                'j'
               42  LOAD_FAST                'j'
               44  LOAD_CONST               1
               46  BINARY_ADD       
               48  BUILD_SLICE_2         2 
               50  BINARY_SUBSCR    
               52  LOAD_STR                 '>'
               54  COMPARE_OP               ==
               56  POP_JUMP_IF_FALSE    66  'to 66'

 L.  80        58  LOAD_FAST                'j'
               60  LOAD_CONST               1
               62  BINARY_ADD       
               64  RETURN_VALUE     
             66_0  COME_FROM            56  '56'

 L.  81        66  LOAD_FAST                'rawdata'
               68  LOAD_FAST                'j'
               70  LOAD_FAST                'j'
               72  LOAD_CONST               1
               74  BINARY_ADD       
               76  BUILD_SLICE_2         2 
               78  BINARY_SUBSCR    
               80  LOAD_CONST               ('-', '')
               82  <118>                 0  ''
               84  POP_JUMP_IF_FALSE    90  'to 90'

 L.  84        86  LOAD_CONST               -1
               88  RETURN_VALUE     
             90_0  COME_FROM            84  '84'

 L.  86        90  LOAD_GLOBAL              len
               92  LOAD_FAST                'rawdata'
               94  CALL_FUNCTION_1       1  ''
               96  STORE_FAST               'n'

 L.  87        98  LOAD_FAST                'rawdata'
              100  LOAD_FAST                'j'
              102  LOAD_FAST                'j'
              104  LOAD_CONST               2
              106  BINARY_ADD       
              108  BUILD_SLICE_2         2 
              110  BINARY_SUBSCR    
              112  LOAD_STR                 '--'
              114  COMPARE_OP               ==
              116  POP_JUMP_IF_FALSE   128  'to 128'

 L.  89       118  LOAD_FAST                'self'
              120  LOAD_METHOD              parse_comment
              122  LOAD_FAST                'i'
              124  CALL_METHOD_1         1  ''
              126  RETURN_VALUE     
            128_0  COME_FROM           116  '116'

 L.  90       128  LOAD_FAST                'rawdata'
              130  LOAD_FAST                'j'
              132  BINARY_SUBSCR    
              134  LOAD_STR                 '['
              136  COMPARE_OP               ==
              138  POP_JUMP_IF_FALSE   150  'to 150'

 L.  95       140  LOAD_FAST                'self'
              142  LOAD_METHOD              parse_marked_section
              144  LOAD_FAST                'i'
              146  CALL_METHOD_1         1  ''
              148  RETURN_VALUE     
            150_0  COME_FROM           138  '138'

 L.  97       150  LOAD_FAST                'self'
              152  LOAD_METHOD              _scan_name
              154  LOAD_FAST                'j'
              156  LOAD_FAST                'i'
              158  CALL_METHOD_2         2  ''
              160  UNPACK_SEQUENCE_2     2 
              162  STORE_FAST               'decltype'
              164  STORE_FAST               'j'

 L.  98       166  LOAD_FAST                'j'
              168  LOAD_CONST               0
              170  COMPARE_OP               <
              172  POP_JUMP_IF_FALSE   178  'to 178'

 L.  99       174  LOAD_FAST                'j'
              176  RETURN_VALUE     
            178_0  COME_FROM           172  '172'

 L. 100       178  LOAD_FAST                'decltype'
              180  LOAD_STR                 'doctype'
              182  COMPARE_OP               ==
              184  POP_JUMP_IF_FALSE   192  'to 192'

 L. 101       186  LOAD_STR                 ''
              188  LOAD_FAST                'self'
              190  STORE_ATTR               _decl_otherchars
            192_0  COME_FROM           466  '466'
            192_1  COME_FROM           184  '184'

 L. 102       192  LOAD_FAST                'j'
              194  LOAD_FAST                'n'
              196  COMPARE_OP               <
          198_200  POP_JUMP_IF_FALSE   474  'to 474'

 L. 103       202  LOAD_FAST                'rawdata'
              204  LOAD_FAST                'j'
              206  BINARY_SUBSCR    
              208  STORE_FAST               'c'

 L. 104       210  LOAD_FAST                'c'
              212  LOAD_STR                 '>'
              214  COMPARE_OP               ==
          216_218  POP_JUMP_IF_FALSE   276  'to 276'

 L. 106       220  LOAD_FAST                'rawdata'
              222  LOAD_FAST                'i'
              224  LOAD_CONST               2
              226  BINARY_ADD       
              228  LOAD_FAST                'j'
              230  BUILD_SLICE_2         2 
              232  BINARY_SUBSCR    
              234  STORE_FAST               'data'

 L. 107       236  LOAD_FAST                'decltype'
              238  LOAD_STR                 'doctype'
              240  COMPARE_OP               ==
          242_244  POP_JUMP_IF_FALSE   258  'to 258'

 L. 108       246  LOAD_FAST                'self'
              248  LOAD_METHOD              handle_decl
              250  LOAD_FAST                'data'
              252  CALL_METHOD_1         1  ''
              254  POP_TOP          
              256  JUMP_FORWARD        268  'to 268'
            258_0  COME_FROM           242  '242'

 L. 114       258  LOAD_FAST                'self'
              260  LOAD_METHOD              unknown_decl
              262  LOAD_FAST                'data'
              264  CALL_METHOD_1         1  ''
              266  POP_TOP          
            268_0  COME_FROM           256  '256'

 L. 115       268  LOAD_FAST                'j'
              270  LOAD_CONST               1
              272  BINARY_ADD       
              274  RETURN_VALUE     
            276_0  COME_FROM           216  '216'

 L. 116       276  LOAD_FAST                'c'
              278  LOAD_STR                 '"\''
              280  <118>                 0  ''
          282_284  POP_JUMP_IF_FALSE   316  'to 316'

 L. 117       286  LOAD_GLOBAL              _declstringlit_match
              288  LOAD_FAST                'rawdata'
              290  LOAD_FAST                'j'
              292  CALL_FUNCTION_2       2  ''
              294  STORE_FAST               'm'

 L. 118       296  LOAD_FAST                'm'
          298_300  POP_JUMP_IF_TRUE    306  'to 306'

 L. 119       302  LOAD_CONST               -1
              304  RETURN_VALUE     
            306_0  COME_FROM           298  '298'

 L. 120       306  LOAD_FAST                'm'
              308  LOAD_METHOD              end
              310  CALL_METHOD_0         0  ''
              312  STORE_FAST               'j'
              314  JUMP_FORWARD        460  'to 460'
            316_0  COME_FROM           282  '282'

 L. 121       316  LOAD_FAST                'c'
              318  LOAD_STR                 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
              320  <118>                 0  ''
          322_324  POP_JUMP_IF_FALSE   344  'to 344'

 L. 122       326  LOAD_FAST                'self'
              328  LOAD_METHOD              _scan_name
              330  LOAD_FAST                'j'
              332  LOAD_FAST                'i'
              334  CALL_METHOD_2         2  ''
              336  UNPACK_SEQUENCE_2     2 
              338  STORE_FAST               'name'
              340  STORE_FAST               'j'
              342  JUMP_FORWARD        460  'to 460'
            344_0  COME_FROM           322  '322'

 L. 123       344  LOAD_FAST                'c'
              346  LOAD_FAST                'self'
              348  LOAD_ATTR                _decl_otherchars
              350  <118>                 0  ''
          352_354  POP_JUMP_IF_FALSE   366  'to 366'

 L. 124       356  LOAD_FAST                'j'
              358  LOAD_CONST               1
              360  BINARY_ADD       
              362  STORE_FAST               'j'
              364  JUMP_FORWARD        460  'to 460'
            366_0  COME_FROM           352  '352'

 L. 125       366  LOAD_FAST                'c'
              368  LOAD_STR                 '['
              370  COMPARE_OP               ==
          372_374  POP_JUMP_IF_FALSE   442  'to 442'

 L. 127       376  LOAD_FAST                'decltype'
              378  LOAD_STR                 'doctype'
              380  COMPARE_OP               ==
          382_384  POP_JUMP_IF_FALSE   404  'to 404'

 L. 128       386  LOAD_FAST                'self'
              388  LOAD_METHOD              _parse_doctype_subset
              390  LOAD_FAST                'j'
              392  LOAD_CONST               1
              394  BINARY_ADD       
              396  LOAD_FAST                'i'
              398  CALL_METHOD_2         2  ''
              400  STORE_FAST               'j'
              402  JUMP_FORWARD        440  'to 440'
            404_0  COME_FROM           382  '382'

 L. 129       404  LOAD_FAST                'decltype'
              406  LOAD_CONST               frozenset({'element', 'attlist', 'linktype', 'link'})
              408  <118>                 0  ''
          410_412  POP_JUMP_IF_FALSE   430  'to 430'

 L. 134       414  LOAD_FAST                'self'
              416  LOAD_METHOD              error
              418  LOAD_STR                 "unsupported '[' char in %s declaration"
              420  LOAD_FAST                'decltype'
              422  BINARY_MODULO    
              424  CALL_METHOD_1         1  ''
              426  POP_TOP          
              428  JUMP_FORWARD        440  'to 440'
            430_0  COME_FROM           410  '410'

 L. 136       430  LOAD_FAST                'self'
              432  LOAD_METHOD              error
              434  LOAD_STR                 "unexpected '[' char in declaration"
              436  CALL_METHOD_1         1  ''
              438  POP_TOP          
            440_0  COME_FROM           428  '428'
            440_1  COME_FROM           402  '402'
              440  JUMP_FORWARD        460  'to 460'
            442_0  COME_FROM           372  '372'

 L. 138       442  LOAD_FAST                'self'
              444  LOAD_METHOD              error

 L. 139       446  LOAD_STR                 'unexpected %r char in declaration'
              448  LOAD_FAST                'rawdata'
              450  LOAD_FAST                'j'
              452  BINARY_SUBSCR    
              454  BINARY_MODULO    

 L. 138       456  CALL_METHOD_1         1  ''
              458  POP_TOP          
            460_0  COME_FROM           440  '440'
            460_1  COME_FROM           364  '364'
            460_2  COME_FROM           342  '342'
            460_3  COME_FROM           314  '314'

 L. 140       460  LOAD_FAST                'j'
              462  LOAD_CONST               0
              464  COMPARE_OP               <
              466  POP_JUMP_IF_FALSE   192  'to 192'

 L. 141       468  LOAD_FAST                'j'
              470  RETURN_VALUE     
              472  JUMP_BACK           192  'to 192'
            474_0  COME_FROM           198  '198'

 L. 142       474  LOAD_CONST               -1
              476  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 30

    def parse_marked_section--- This code section failed: ---

 L. 147         0  LOAD_FAST                'self'
                2  LOAD_ATTR                rawdata
                4  STORE_FAST               'rawdata'

 L. 148         6  LOAD_FAST                'rawdata'
                8  LOAD_FAST                'i'
               10  LOAD_FAST                'i'
               12  LOAD_CONST               3
               14  BINARY_ADD       
               16  BUILD_SLICE_2         2 
               18  BINARY_SUBSCR    
               20  LOAD_STR                 '<!['
               22  COMPARE_OP               ==
               24  POP_JUMP_IF_TRUE     34  'to 34'
               26  <74>             
               28  LOAD_STR                 'unexpected call to parse_marked_section()'
               30  CALL_FUNCTION_1       1  ''
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            24  '24'

 L. 149        34  LOAD_FAST                'self'
               36  LOAD_METHOD              _scan_name
               38  LOAD_FAST                'i'
               40  LOAD_CONST               3
               42  BINARY_ADD       
               44  LOAD_FAST                'i'
               46  CALL_METHOD_2         2  ''
               48  UNPACK_SEQUENCE_2     2 
               50  STORE_FAST               'sectName'
               52  STORE_FAST               'j'

 L. 150        54  LOAD_FAST                'j'
               56  LOAD_CONST               0
               58  COMPARE_OP               <
               60  POP_JUMP_IF_FALSE    66  'to 66'

 L. 151        62  LOAD_FAST                'j'
               64  RETURN_VALUE     
             66_0  COME_FROM            60  '60'

 L. 152        66  LOAD_FAST                'sectName'
               68  LOAD_CONST               frozenset({'cdata', 'ignore', 'temp', 'rcdata', 'include'})
               70  <118>                 0  ''
               72  POP_JUMP_IF_FALSE    92  'to 92'

 L. 154        74  LOAD_GLOBAL              _markedsectionclose
               76  LOAD_METHOD              search
               78  LOAD_FAST                'rawdata'
               80  LOAD_FAST                'i'
               82  LOAD_CONST               3
               84  BINARY_ADD       
               86  CALL_METHOD_2         2  ''
               88  STORE_FAST               'match'
               90  JUMP_FORWARD        144  'to 144'
             92_0  COME_FROM            72  '72'

 L. 155        92  LOAD_FAST                'sectName'
               94  LOAD_CONST               frozenset({'if', 'else', 'endif'})
               96  <118>                 0  ''
               98  POP_JUMP_IF_FALSE   118  'to 118'

 L. 157       100  LOAD_GLOBAL              _msmarkedsectionclose
              102  LOAD_METHOD              search
              104  LOAD_FAST                'rawdata'
              106  LOAD_FAST                'i'
              108  LOAD_CONST               3
              110  BINARY_ADD       
              112  CALL_METHOD_2         2  ''
              114  STORE_FAST               'match'
              116  JUMP_FORWARD        144  'to 144'
            118_0  COME_FROM            98  '98'

 L. 159       118  LOAD_FAST                'self'
              120  LOAD_METHOD              error
              122  LOAD_STR                 'unknown status keyword %r in marked section'
              124  LOAD_FAST                'rawdata'
              126  LOAD_FAST                'i'
              128  LOAD_CONST               3
              130  BINARY_ADD       
              132  LOAD_FAST                'j'
              134  BUILD_SLICE_2         2 
              136  BINARY_SUBSCR    
              138  BINARY_MODULO    
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          
            144_0  COME_FROM           116  '116'
            144_1  COME_FROM            90  '90'

 L. 160       144  LOAD_FAST                'match'
              146  POP_JUMP_IF_TRUE    152  'to 152'

 L. 161       148  LOAD_CONST               -1
              150  RETURN_VALUE     
            152_0  COME_FROM           146  '146'

 L. 162       152  LOAD_FAST                'report'
              154  POP_JUMP_IF_FALSE   188  'to 188'

 L. 163       156  LOAD_FAST                'match'
              158  LOAD_METHOD              start
              160  LOAD_CONST               0
              162  CALL_METHOD_1         1  ''
              164  STORE_FAST               'j'

 L. 164       166  LOAD_FAST                'self'
              168  LOAD_METHOD              unknown_decl
              170  LOAD_FAST                'rawdata'
              172  LOAD_FAST                'i'
              174  LOAD_CONST               3
              176  BINARY_ADD       
              178  LOAD_FAST                'j'
              180  BUILD_SLICE_2         2 
              182  BINARY_SUBSCR    
              184  CALL_METHOD_1         1  ''
              186  POP_TOP          
            188_0  COME_FROM           154  '154'

 L. 165       188  LOAD_FAST                'match'
              190  LOAD_METHOD              end
              192  LOAD_CONST               0
              194  CALL_METHOD_1         1  ''
              196  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 26

    def parse_comment(self, i, report=1):
        rawdata = self.rawdata
        if rawdata[i:i + 4] != '<!--':
            self.error('unexpected call to parse_comment()')
        else:
            match = _commentclose.searchrawdata(i + 4)
            return match or -1
        if report:
            j = match.start(0)
            self.handle_comment(rawdata[i + 4:j])
        return match.end(0)

    def _parse_doctype_subset--- This code section failed: ---

 L. 183         0  LOAD_FAST                'self'
                2  LOAD_ATTR                rawdata
                4  STORE_FAST               'rawdata'

 L. 184         6  LOAD_GLOBAL              len
                8  LOAD_FAST                'rawdata'
               10  CALL_FUNCTION_1       1  ''
               12  STORE_FAST               'n'

 L. 185        14  LOAD_FAST                'i'
               16  STORE_FAST               'j'
             18_0  COME_FROM           184  '184'

 L. 186        18  LOAD_FAST                'j'
               20  LOAD_FAST                'n'
               22  COMPARE_OP               <
            24_26  POP_JUMP_IF_FALSE   550  'to 550'

 L. 187        28  LOAD_FAST                'rawdata'
               30  LOAD_FAST                'j'
               32  BINARY_SUBSCR    
               34  STORE_FAST               'c'

 L. 188        36  LOAD_FAST                'c'
               38  LOAD_STR                 '<'
               40  COMPARE_OP               ==
            42_44  POP_JUMP_IF_FALSE   304  'to 304'

 L. 189        46  LOAD_FAST                'rawdata'
               48  LOAD_FAST                'j'
               50  LOAD_FAST                'j'
               52  LOAD_CONST               2
               54  BINARY_ADD       
               56  BUILD_SLICE_2         2 
               58  BINARY_SUBSCR    
               60  STORE_FAST               's'

 L. 190        62  LOAD_FAST                's'
               64  LOAD_STR                 '<'
               66  COMPARE_OP               ==
               68  POP_JUMP_IF_FALSE    74  'to 74'

 L. 192        70  LOAD_CONST               -1
               72  RETURN_VALUE     
             74_0  COME_FROM            68  '68'

 L. 193        74  LOAD_FAST                's'
               76  LOAD_STR                 '<!'
               78  COMPARE_OP               !=
               80  POP_JUMP_IF_FALSE   112  'to 112'

 L. 194        82  LOAD_FAST                'self'
               84  LOAD_METHOD              updatepos
               86  LOAD_FAST                'declstartpos'
               88  LOAD_FAST                'j'
               90  LOAD_CONST               1
               92  BINARY_ADD       
               94  CALL_METHOD_2         2  ''
               96  POP_TOP          

 L. 195        98  LOAD_FAST                'self'
              100  LOAD_METHOD              error
              102  LOAD_STR                 'unexpected char in internal subset (in %r)'
              104  LOAD_FAST                's'
              106  BINARY_MODULO    
              108  CALL_METHOD_1         1  ''
              110  POP_TOP          
            112_0  COME_FROM            80  '80'

 L. 196       112  LOAD_FAST                'j'
              114  LOAD_CONST               2
              116  BINARY_ADD       
              118  LOAD_FAST                'n'
              120  COMPARE_OP               ==
              122  POP_JUMP_IF_FALSE   128  'to 128'

 L. 198       124  LOAD_CONST               -1
              126  RETURN_VALUE     
            128_0  COME_FROM           122  '122'

 L. 199       128  LOAD_FAST                'j'
              130  LOAD_CONST               4
              132  BINARY_ADD       
              134  LOAD_FAST                'n'
              136  COMPARE_OP               >
              138  POP_JUMP_IF_FALSE   144  'to 144'

 L. 201       140  LOAD_CONST               -1
              142  RETURN_VALUE     
            144_0  COME_FROM           138  '138'

 L. 202       144  LOAD_FAST                'rawdata'
              146  LOAD_FAST                'j'
              148  LOAD_FAST                'j'
              150  LOAD_CONST               4
              152  BINARY_ADD       
              154  BUILD_SLICE_2         2 
              156  BINARY_SUBSCR    
              158  LOAD_STR                 '<!--'
              160  COMPARE_OP               ==
              162  POP_JUMP_IF_FALSE   192  'to 192'

 L. 203       164  LOAD_FAST                'self'
              166  LOAD_ATTR                parse_comment
              168  LOAD_FAST                'j'
              170  LOAD_CONST               0
              172  LOAD_CONST               ('report',)
              174  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              176  STORE_FAST               'j'

 L. 204       178  LOAD_FAST                'j'
              180  LOAD_CONST               0
              182  COMPARE_OP               <
              184  POP_JUMP_IF_FALSE    18  'to 18'

 L. 205       186  LOAD_FAST                'j'
              188  RETURN_VALUE     

 L. 206       190  JUMP_BACK            18  'to 18'
            192_0  COME_FROM           162  '162'

 L. 207       192  LOAD_FAST                'self'
              194  LOAD_METHOD              _scan_name
              196  LOAD_FAST                'j'
              198  LOAD_CONST               2
              200  BINARY_ADD       
              202  LOAD_FAST                'declstartpos'
              204  CALL_METHOD_2         2  ''
              206  UNPACK_SEQUENCE_2     2 
              208  STORE_FAST               'name'
              210  STORE_FAST               'j'

 L. 208       212  LOAD_FAST                'j'
              214  LOAD_CONST               -1
              216  COMPARE_OP               ==
              218  POP_JUMP_IF_FALSE   224  'to 224'

 L. 209       220  LOAD_CONST               -1
              222  RETURN_VALUE     
            224_0  COME_FROM           218  '218'

 L. 210       224  LOAD_FAST                'name'
              226  LOAD_CONST               frozenset({'element', 'attlist', 'entity', 'notation'})
              228  <118>                 1  ''
          230_232  POP_JUMP_IF_FALSE   264  'to 264'

 L. 211       234  LOAD_FAST                'self'
              236  LOAD_METHOD              updatepos
              238  LOAD_FAST                'declstartpos'
              240  LOAD_FAST                'j'
              242  LOAD_CONST               2
              244  BINARY_ADD       
              246  CALL_METHOD_2         2  ''
              248  POP_TOP          

 L. 212       250  LOAD_FAST                'self'
              252  LOAD_METHOD              error

 L. 213       254  LOAD_STR                 'unknown declaration %r in internal subset'
              256  LOAD_FAST                'name'
              258  BINARY_MODULO    

 L. 212       260  CALL_METHOD_1         1  ''
              262  POP_TOP          
            264_0  COME_FROM           230  '230'

 L. 215       264  LOAD_GLOBAL              getattr
              266  LOAD_FAST                'self'
              268  LOAD_STR                 '_parse_doctype_'
              270  LOAD_FAST                'name'
              272  BINARY_ADD       
              274  CALL_FUNCTION_2       2  ''
              276  STORE_FAST               'meth'

 L. 216       278  LOAD_FAST                'meth'
              280  LOAD_FAST                'j'
              282  LOAD_FAST                'declstartpos'
              284  CALL_FUNCTION_2       2  ''
              286  STORE_FAST               'j'

 L. 217       288  LOAD_FAST                'j'
              290  LOAD_CONST               0
              292  COMPARE_OP               <
          294_296  POP_JUMP_IF_FALSE   548  'to 548'

 L. 218       298  LOAD_FAST                'j'
              300  RETURN_VALUE     
              302  JUMP_BACK            18  'to 18'
            304_0  COME_FROM            42  '42'

 L. 219       304  LOAD_FAST                'c'
              306  LOAD_STR                 '%'
              308  COMPARE_OP               ==
          310_312  POP_JUMP_IF_FALSE   390  'to 390'

 L. 221       314  LOAD_FAST                'j'
              316  LOAD_CONST               1
              318  BINARY_ADD       
              320  LOAD_FAST                'n'
              322  COMPARE_OP               ==
          324_326  POP_JUMP_IF_FALSE   332  'to 332'

 L. 223       328  LOAD_CONST               -1
              330  RETURN_VALUE     
            332_0  COME_FROM           324  '324'

 L. 224       332  LOAD_FAST                'self'
              334  LOAD_METHOD              _scan_name
              336  LOAD_FAST                'j'
              338  LOAD_CONST               1
              340  BINARY_ADD       
              342  LOAD_FAST                'declstartpos'
              344  CALL_METHOD_2         2  ''
              346  UNPACK_SEQUENCE_2     2 
              348  STORE_FAST               's'
              350  STORE_FAST               'j'

 L. 225       352  LOAD_FAST                'j'
              354  LOAD_CONST               0
              356  COMPARE_OP               <
          358_360  POP_JUMP_IF_FALSE   366  'to 366'

 L. 226       362  LOAD_FAST                'j'
              364  RETURN_VALUE     
            366_0  COME_FROM           358  '358'

 L. 227       366  LOAD_FAST                'rawdata'
              368  LOAD_FAST                'j'
              370  BINARY_SUBSCR    
              372  LOAD_STR                 ';'
              374  COMPARE_OP               ==
          376_378  POP_JUMP_IF_FALSE   548  'to 548'

 L. 228       380  LOAD_FAST                'j'
              382  LOAD_CONST               1
              384  BINARY_ADD       
              386  STORE_FAST               'j'
              388  JUMP_BACK            18  'to 18'
            390_0  COME_FROM           310  '310'

 L. 229       390  LOAD_FAST                'c'
              392  LOAD_STR                 ']'
              394  COMPARE_OP               ==
          396_398  POP_JUMP_IF_FALSE   502  'to 502'

 L. 230       400  LOAD_FAST                'j'
              402  LOAD_CONST               1
              404  BINARY_ADD       
              406  STORE_FAST               'j'

 L. 231       408  LOAD_FAST                'j'
              410  LOAD_FAST                'n'
              412  COMPARE_OP               <
          414_416  POP_JUMP_IF_FALSE   444  'to 444'
              418  LOAD_FAST                'rawdata'
              420  LOAD_FAST                'j'
              422  BINARY_SUBSCR    
              424  LOAD_METHOD              isspace
              426  CALL_METHOD_0         0  ''
          428_430  POP_JUMP_IF_FALSE   444  'to 444'

 L. 232       432  LOAD_FAST                'j'
              434  LOAD_CONST               1
              436  BINARY_ADD       
              438  STORE_FAST               'j'
          440_442  JUMP_BACK           408  'to 408'
            444_0  COME_FROM           428  '428'
            444_1  COME_FROM           414  '414'

 L. 233       444  LOAD_FAST                'j'
              446  LOAD_FAST                'n'
              448  COMPARE_OP               <
          450_452  POP_JUMP_IF_FALSE   496  'to 496'

 L. 234       454  LOAD_FAST                'rawdata'
              456  LOAD_FAST                'j'
              458  BINARY_SUBSCR    
              460  LOAD_STR                 '>'
              462  COMPARE_OP               ==
          464_466  POP_JUMP_IF_FALSE   472  'to 472'

 L. 235       468  LOAD_FAST                'j'
              470  RETURN_VALUE     
            472_0  COME_FROM           464  '464'

 L. 236       472  LOAD_FAST                'self'
              474  LOAD_METHOD              updatepos
              476  LOAD_FAST                'declstartpos'
              478  LOAD_FAST                'j'
              480  CALL_METHOD_2         2  ''
              482  POP_TOP          

 L. 237       484  LOAD_FAST                'self'
              486  LOAD_METHOD              error
              488  LOAD_STR                 'unexpected char after internal subset'
              490  CALL_METHOD_1         1  ''
              492  POP_TOP          
              494  JUMP_FORWARD        500  'to 500'
            496_0  COME_FROM           450  '450'

 L. 239       496  LOAD_CONST               -1
              498  RETURN_VALUE     
            500_0  COME_FROM           494  '494'
              500  JUMP_BACK            18  'to 18'
            502_0  COME_FROM           396  '396'

 L. 240       502  LOAD_FAST                'c'
              504  LOAD_METHOD              isspace
              506  CALL_METHOD_0         0  ''
          508_510  POP_JUMP_IF_FALSE   522  'to 522'

 L. 241       512  LOAD_FAST                'j'
              514  LOAD_CONST               1
              516  BINARY_ADD       
              518  STORE_FAST               'j'
              520  JUMP_BACK            18  'to 18'
            522_0  COME_FROM           508  '508'

 L. 243       522  LOAD_FAST                'self'
              524  LOAD_METHOD              updatepos
              526  LOAD_FAST                'declstartpos'
              528  LOAD_FAST                'j'
              530  CALL_METHOD_2         2  ''
              532  POP_TOP          

 L. 244       534  LOAD_FAST                'self'
              536  LOAD_METHOD              error
              538  LOAD_STR                 'unexpected char %r in internal subset'
              540  LOAD_FAST                'c'
              542  BINARY_MODULO    
              544  CALL_METHOD_1         1  ''
              546  POP_TOP          
            548_0  COME_FROM           376  '376'
            548_1  COME_FROM           294  '294'
              548  JUMP_BACK            18  'to 18'
            550_0  COME_FROM            24  '24'

 L. 246       550  LOAD_CONST               -1
              552  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 228

    def _parse_doctype_element--- This code section failed: ---

 L. 250         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _scan_name
                4  LOAD_FAST                'i'
                6  LOAD_FAST                'declstartpos'
                8  CALL_METHOD_2         2  ''
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'name'
               14  STORE_FAST               'j'

 L. 251        16  LOAD_FAST                'j'
               18  LOAD_CONST               -1
               20  COMPARE_OP               ==
               22  POP_JUMP_IF_FALSE    28  'to 28'

 L. 252        24  LOAD_CONST               -1
               26  RETURN_VALUE     
             28_0  COME_FROM            22  '22'

 L. 254        28  LOAD_FAST                'self'
               30  LOAD_ATTR                rawdata
               32  STORE_FAST               'rawdata'

 L. 255        34  LOAD_STR                 '>'
               36  LOAD_FAST                'rawdata'
               38  LOAD_FAST                'j'
               40  LOAD_CONST               None
               42  BUILD_SLICE_2         2 
               44  BINARY_SUBSCR    
               46  <118>                 0  ''
               48  POP_JUMP_IF_FALSE    66  'to 66'

 L. 256        50  LOAD_FAST                'rawdata'
               52  LOAD_METHOD              find
               54  LOAD_STR                 '>'
               56  LOAD_FAST                'j'
               58  CALL_METHOD_2         2  ''
               60  LOAD_CONST               1
               62  BINARY_ADD       
               64  RETURN_VALUE     
             66_0  COME_FROM            48  '48'

 L. 257        66  LOAD_CONST               -1
               68  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 46

    def _parse_doctype_attlist--- This code section failed: ---

 L. 261         0  LOAD_FAST                'self'
                2  LOAD_ATTR                rawdata
                4  STORE_FAST               'rawdata'

 L. 262         6  LOAD_FAST                'self'
                8  LOAD_METHOD              _scan_name
               10  LOAD_FAST                'i'
               12  LOAD_FAST                'declstartpos'
               14  CALL_METHOD_2         2  ''
               16  UNPACK_SEQUENCE_2     2 
               18  STORE_FAST               'name'
               20  STORE_FAST               'j'

 L. 263        22  LOAD_FAST                'rawdata'
               24  LOAD_FAST                'j'
               26  LOAD_FAST                'j'
               28  LOAD_CONST               1
               30  BINARY_ADD       
               32  BUILD_SLICE_2         2 
               34  BINARY_SUBSCR    
               36  STORE_FAST               'c'

 L. 264        38  LOAD_FAST                'c'
               40  LOAD_STR                 ''
               42  COMPARE_OP               ==
               44  POP_JUMP_IF_FALSE    50  'to 50'

 L. 265        46  LOAD_CONST               -1
               48  RETURN_VALUE     
             50_0  COME_FROM            44  '44'

 L. 266        50  LOAD_FAST                'c'
               52  LOAD_STR                 '>'
               54  COMPARE_OP               ==
               56  POP_JUMP_IF_FALSE    66  'to 66'

 L. 267        58  LOAD_FAST                'j'
               60  LOAD_CONST               1
               62  BINARY_ADD       
               64  RETURN_VALUE     
             66_0  COME_FROM           422  '422'
             66_1  COME_FROM            56  '56'

 L. 271        66  LOAD_FAST                'self'
               68  LOAD_METHOD              _scan_name
               70  LOAD_FAST                'j'
               72  LOAD_FAST                'declstartpos'
               74  CALL_METHOD_2         2  ''
               76  UNPACK_SEQUENCE_2     2 
               78  STORE_FAST               'name'
               80  STORE_FAST               'j'

 L. 272        82  LOAD_FAST                'j'
               84  LOAD_CONST               0
               86  COMPARE_OP               <
               88  POP_JUMP_IF_FALSE    94  'to 94'

 L. 273        90  LOAD_FAST                'j'
               92  RETURN_VALUE     
             94_0  COME_FROM            88  '88'

 L. 274        94  LOAD_FAST                'rawdata'
               96  LOAD_FAST                'j'
               98  LOAD_FAST                'j'
              100  LOAD_CONST               1
              102  BINARY_ADD       
              104  BUILD_SLICE_2         2 
              106  BINARY_SUBSCR    
              108  STORE_FAST               'c'

 L. 275       110  LOAD_FAST                'c'
              112  LOAD_STR                 ''
              114  COMPARE_OP               ==
              116  POP_JUMP_IF_FALSE   122  'to 122'

 L. 276       118  LOAD_CONST               -1
              120  RETURN_VALUE     
            122_0  COME_FROM           116  '116'

 L. 277       122  LOAD_FAST                'c'
              124  LOAD_STR                 '('
              126  COMPARE_OP               ==
              128  POP_JUMP_IF_FALSE   216  'to 216'

 L. 279       130  LOAD_STR                 ')'
              132  LOAD_FAST                'rawdata'
              134  LOAD_FAST                'j'
              136  LOAD_CONST               None
              138  BUILD_SLICE_2         2 
              140  BINARY_SUBSCR    
              142  <118>                 0  ''
              144  POP_JUMP_IF_FALSE   164  'to 164'

 L. 280       146  LOAD_FAST                'rawdata'
              148  LOAD_METHOD              find
              150  LOAD_STR                 ')'
              152  LOAD_FAST                'j'
              154  CALL_METHOD_2         2  ''
              156  LOAD_CONST               1
              158  BINARY_ADD       
              160  STORE_FAST               'j'
              162  JUMP_FORWARD        168  'to 168'
            164_0  COME_FROM           144  '144'

 L. 282       164  LOAD_CONST               -1
              166  RETURN_VALUE     
            168_0  COME_FROM           162  '162'

 L. 283       168  LOAD_FAST                'rawdata'
              170  LOAD_FAST                'j'
              172  LOAD_FAST                'j'
              174  LOAD_CONST               1
              176  BINARY_ADD       
              178  BUILD_SLICE_2         2 
              180  BINARY_SUBSCR    
              182  LOAD_METHOD              isspace
              184  CALL_METHOD_0         0  ''
              186  POP_JUMP_IF_FALSE   198  'to 198'

 L. 284       188  LOAD_FAST                'j'
              190  LOAD_CONST               1
              192  BINARY_ADD       
              194  STORE_FAST               'j'
              196  JUMP_BACK           168  'to 168'
            198_0  COME_FROM           186  '186'

 L. 285       198  LOAD_FAST                'rawdata'
              200  LOAD_FAST                'j'
              202  LOAD_CONST               None
              204  BUILD_SLICE_2         2 
              206  BINARY_SUBSCR    
              208  POP_JUMP_IF_TRUE    232  'to 232'

 L. 287       210  LOAD_CONST               -1
              212  RETURN_VALUE     
              214  JUMP_FORWARD        232  'to 232'
            216_0  COME_FROM           128  '128'

 L. 289       216  LOAD_FAST                'self'
              218  LOAD_METHOD              _scan_name
              220  LOAD_FAST                'j'
              222  LOAD_FAST                'declstartpos'
              224  CALL_METHOD_2         2  ''
              226  UNPACK_SEQUENCE_2     2 
              228  STORE_FAST               'name'
              230  STORE_FAST               'j'
            232_0  COME_FROM           214  '214'
            232_1  COME_FROM           208  '208'

 L. 290       232  LOAD_FAST                'rawdata'
              234  LOAD_FAST                'j'
              236  LOAD_FAST                'j'
              238  LOAD_CONST               1
              240  BINARY_ADD       
              242  BUILD_SLICE_2         2 
              244  BINARY_SUBSCR    
              246  STORE_FAST               'c'

 L. 291       248  LOAD_FAST                'c'
          250_252  POP_JUMP_IF_TRUE    258  'to 258'

 L. 292       254  LOAD_CONST               -1
              256  RETURN_VALUE     
            258_0  COME_FROM           250  '250'

 L. 293       258  LOAD_FAST                'c'
              260  LOAD_STR                 '\'"'
              262  <118>                 0  ''
          264_266  POP_JUMP_IF_FALSE   324  'to 324'

 L. 294       268  LOAD_GLOBAL              _declstringlit_match
              270  LOAD_FAST                'rawdata'
              272  LOAD_FAST                'j'
              274  CALL_FUNCTION_2       2  ''
              276  STORE_FAST               'm'

 L. 295       278  LOAD_FAST                'm'
          280_282  POP_JUMP_IF_FALSE   294  'to 294'

 L. 296       284  LOAD_FAST                'm'
              286  LOAD_METHOD              end
              288  CALL_METHOD_0         0  ''
              290  STORE_FAST               'j'
              292  JUMP_FORWARD        298  'to 298'
            294_0  COME_FROM           280  '280'

 L. 298       294  LOAD_CONST               -1
              296  RETURN_VALUE     
            298_0  COME_FROM           292  '292'

 L. 299       298  LOAD_FAST                'rawdata'
              300  LOAD_FAST                'j'
              302  LOAD_FAST                'j'
              304  LOAD_CONST               1
              306  BINARY_ADD       
              308  BUILD_SLICE_2         2 
              310  BINARY_SUBSCR    
              312  STORE_FAST               'c'

 L. 300       314  LOAD_FAST                'c'
          316_318  POP_JUMP_IF_TRUE    324  'to 324'

 L. 301       320  LOAD_CONST               -1
              322  RETURN_VALUE     
            324_0  COME_FROM           316  '316'
            324_1  COME_FROM           264  '264'

 L. 302       324  LOAD_FAST                'c'
              326  LOAD_STR                 '#'
              328  COMPARE_OP               ==
          330_332  POP_JUMP_IF_FALSE   416  'to 416'

 L. 303       334  LOAD_FAST                'rawdata'
              336  LOAD_FAST                'j'
              338  LOAD_CONST               None
              340  BUILD_SLICE_2         2 
              342  BINARY_SUBSCR    
              344  LOAD_STR                 '#'
              346  COMPARE_OP               ==
          348_350  POP_JUMP_IF_FALSE   356  'to 356'

 L. 305       352  LOAD_CONST               -1
              354  RETURN_VALUE     
            356_0  COME_FROM           348  '348'

 L. 306       356  LOAD_FAST                'self'
              358  LOAD_METHOD              _scan_name
              360  LOAD_FAST                'j'
              362  LOAD_CONST               1
              364  BINARY_ADD       
              366  LOAD_FAST                'declstartpos'
              368  CALL_METHOD_2         2  ''
              370  UNPACK_SEQUENCE_2     2 
              372  STORE_FAST               'name'
              374  STORE_FAST               'j'

 L. 307       376  LOAD_FAST                'j'
              378  LOAD_CONST               0
              380  COMPARE_OP               <
          382_384  POP_JUMP_IF_FALSE   390  'to 390'

 L. 308       386  LOAD_FAST                'j'
              388  RETURN_VALUE     
            390_0  COME_FROM           382  '382'

 L. 309       390  LOAD_FAST                'rawdata'
              392  LOAD_FAST                'j'
              394  LOAD_FAST                'j'
              396  LOAD_CONST               1
              398  BINARY_ADD       
              400  BUILD_SLICE_2         2 
              402  BINARY_SUBSCR    
              404  STORE_FAST               'c'

 L. 310       406  LOAD_FAST                'c'
          408_410  POP_JUMP_IF_TRUE    416  'to 416'

 L. 311       412  LOAD_CONST               -1
              414  RETURN_VALUE     
            416_0  COME_FROM           408  '408'
            416_1  COME_FROM           330  '330'

 L. 312       416  LOAD_FAST                'c'
              418  LOAD_STR                 '>'
              420  COMPARE_OP               ==
              422  POP_JUMP_IF_FALSE    66  'to 66'

 L. 314       424  LOAD_FAST                'j'
              426  LOAD_CONST               1
              428  BINARY_ADD       
              430  RETURN_VALUE     
              432  JUMP_BACK            66  'to 66'

Parse error at or near `<118>' instruction at offset 142

    def _parse_doctype_notation--- This code section failed: ---

 L. 318         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _scan_name
                4  LOAD_FAST                'i'
                6  LOAD_FAST                'declstartpos'
                8  CALL_METHOD_2         2  ''
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'name'
               14  STORE_FAST               'j'

 L. 319        16  LOAD_FAST                'j'
               18  LOAD_CONST               0
               20  COMPARE_OP               <
               22  POP_JUMP_IF_FALSE    28  'to 28'

 L. 320        24  LOAD_FAST                'j'
               26  RETURN_VALUE     
             28_0  COME_FROM            22  '22'

 L. 321        28  LOAD_FAST                'self'
               30  LOAD_ATTR                rawdata
               32  STORE_FAST               'rawdata'
             34_0  COME_FROM           132  '132'

 L. 323        34  LOAD_FAST                'rawdata'
               36  LOAD_FAST                'j'
               38  LOAD_FAST                'j'
               40  LOAD_CONST               1
               42  BINARY_ADD       
               44  BUILD_SLICE_2         2 
               46  BINARY_SUBSCR    
               48  STORE_FAST               'c'

 L. 324        50  LOAD_FAST                'c'
               52  POP_JUMP_IF_TRUE     58  'to 58'

 L. 326        54  LOAD_CONST               -1
               56  RETURN_VALUE     
             58_0  COME_FROM            52  '52'

 L. 327        58  LOAD_FAST                'c'
               60  LOAD_STR                 '>'
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_FALSE    74  'to 74'

 L. 328        66  LOAD_FAST                'j'
               68  LOAD_CONST               1
               70  BINARY_ADD       
               72  RETURN_VALUE     
             74_0  COME_FROM            64  '64'

 L. 329        74  LOAD_FAST                'c'
               76  LOAD_STR                 '\'"'
               78  <118>                 0  ''
               80  POP_JUMP_IF_FALSE   110  'to 110'

 L. 330        82  LOAD_GLOBAL              _declstringlit_match
               84  LOAD_FAST                'rawdata'
               86  LOAD_FAST                'j'
               88  CALL_FUNCTION_2       2  ''
               90  STORE_FAST               'm'

 L. 331        92  LOAD_FAST                'm'
               94  POP_JUMP_IF_TRUE    100  'to 100'

 L. 332        96  LOAD_CONST               -1
               98  RETURN_VALUE     
            100_0  COME_FROM            94  '94'

 L. 333       100  LOAD_FAST                'm'
              102  LOAD_METHOD              end
              104  CALL_METHOD_0         0  ''
              106  STORE_FAST               'j'
              108  JUMP_BACK            34  'to 34'
            110_0  COME_FROM            80  '80'

 L. 335       110  LOAD_FAST                'self'
              112  LOAD_METHOD              _scan_name
              114  LOAD_FAST                'j'
              116  LOAD_FAST                'declstartpos'
              118  CALL_METHOD_2         2  ''
              120  UNPACK_SEQUENCE_2     2 
              122  STORE_FAST               'name'
              124  STORE_FAST               'j'

 L. 336       126  LOAD_FAST                'j'
              128  LOAD_CONST               0
              130  COMPARE_OP               <
              132  POP_JUMP_IF_FALSE    34  'to 34'

 L. 337       134  LOAD_FAST                'j'
              136  RETURN_VALUE     
              138  JUMP_BACK            34  'to 34'

Parse error at or near `<118>' instruction at offset 78

    def _parse_doctype_entity--- This code section failed: ---

 L. 341         0  LOAD_FAST                'self'
                2  LOAD_ATTR                rawdata
                4  STORE_FAST               'rawdata'

 L. 342         6  LOAD_FAST                'rawdata'
                8  LOAD_FAST                'i'
               10  LOAD_FAST                'i'
               12  LOAD_CONST               1
               14  BINARY_ADD       
               16  BUILD_SLICE_2         2 
               18  BINARY_SUBSCR    
               20  LOAD_STR                 '%'
               22  COMPARE_OP               ==
               24  POP_JUMP_IF_FALSE    82  'to 82'

 L. 343        26  LOAD_FAST                'i'
               28  LOAD_CONST               1
               30  BINARY_ADD       
               32  STORE_FAST               'j'

 L. 345        34  LOAD_FAST                'rawdata'
               36  LOAD_FAST                'j'
               38  LOAD_FAST                'j'
               40  LOAD_CONST               1
               42  BINARY_ADD       
               44  BUILD_SLICE_2         2 
               46  BINARY_SUBSCR    
               48  STORE_FAST               'c'

 L. 346        50  LOAD_FAST                'c'
               52  POP_JUMP_IF_TRUE     58  'to 58'

 L. 347        54  LOAD_CONST               -1
               56  RETURN_VALUE     
             58_0  COME_FROM            52  '52'

 L. 348        58  LOAD_FAST                'c'
               60  LOAD_METHOD              isspace
               62  CALL_METHOD_0         0  ''
               64  POP_JUMP_IF_FALSE    80  'to 80'

 L. 349        66  LOAD_FAST                'j'
               68  LOAD_CONST               1
               70  BINARY_ADD       
               72  STORE_FAST               'j'
               74  JUMP_BACK            34  'to 34'

 L. 351        76  BREAK_LOOP           86  'to 86'
               78  JUMP_BACK            34  'to 34'
             80_0  COME_FROM            64  '64'
               80  JUMP_FORWARD         86  'to 86'
             82_0  COME_FROM            24  '24'

 L. 353        82  LOAD_FAST                'i'
               84  STORE_FAST               'j'
             86_0  COME_FROM            80  '80'

 L. 354        86  LOAD_FAST                'self'
               88  LOAD_METHOD              _scan_name
               90  LOAD_FAST                'j'
               92  LOAD_FAST                'declstartpos'
               94  CALL_METHOD_2         2  ''
               96  UNPACK_SEQUENCE_2     2 
               98  STORE_FAST               'name'
              100  STORE_FAST               'j'

 L. 355       102  LOAD_FAST                'j'
              104  LOAD_CONST               0
              106  COMPARE_OP               <
              108  POP_JUMP_IF_FALSE   114  'to 114'

 L. 356       110  LOAD_FAST                'j'
              112  RETURN_VALUE     
            114_0  COME_FROM           216  '216'
            114_1  COME_FROM           108  '108'

 L. 358       114  LOAD_FAST                'self'
              116  LOAD_ATTR                rawdata
              118  LOAD_FAST                'j'
              120  LOAD_FAST                'j'
              122  LOAD_CONST               1
              124  BINARY_ADD       
              126  BUILD_SLICE_2         2 
              128  BINARY_SUBSCR    
              130  STORE_FAST               'c'

 L. 359       132  LOAD_FAST                'c'
              134  POP_JUMP_IF_TRUE    140  'to 140'

 L. 360       136  LOAD_CONST               -1
              138  RETURN_VALUE     
            140_0  COME_FROM           134  '134'

 L. 361       140  LOAD_FAST                'c'
              142  LOAD_STR                 '\'"'
              144  <118>                 0  ''
              146  POP_JUMP_IF_FALSE   178  'to 178'

 L. 362       148  LOAD_GLOBAL              _declstringlit_match
              150  LOAD_FAST                'rawdata'
              152  LOAD_FAST                'j'
              154  CALL_FUNCTION_2       2  ''
              156  STORE_FAST               'm'

 L. 363       158  LOAD_FAST                'm'
              160  POP_JUMP_IF_FALSE   172  'to 172'

 L. 364       162  LOAD_FAST                'm'
              164  LOAD_METHOD              end
              166  CALL_METHOD_0         0  ''
              168  STORE_FAST               'j'
              170  JUMP_ABSOLUTE       222  'to 222'
            172_0  COME_FROM           160  '160'

 L. 366       172  LOAD_CONST               -1
              174  RETURN_VALUE     
              176  JUMP_BACK           114  'to 114'
            178_0  COME_FROM           146  '146'

 L. 367       178  LOAD_FAST                'c'
              180  LOAD_STR                 '>'
              182  COMPARE_OP               ==
              184  POP_JUMP_IF_FALSE   194  'to 194'

 L. 368       186  LOAD_FAST                'j'
              188  LOAD_CONST               1
              190  BINARY_ADD       
              192  RETURN_VALUE     
            194_0  COME_FROM           184  '184'

 L. 370       194  LOAD_FAST                'self'
              196  LOAD_METHOD              _scan_name
              198  LOAD_FAST                'j'
              200  LOAD_FAST                'declstartpos'
              202  CALL_METHOD_2         2  ''
              204  UNPACK_SEQUENCE_2     2 
              206  STORE_FAST               'name'
              208  STORE_FAST               'j'

 L. 371       210  LOAD_FAST                'j'
              212  LOAD_CONST               0
              214  COMPARE_OP               <
              216  POP_JUMP_IF_FALSE   114  'to 114'

 L. 372       218  LOAD_FAST                'j'
              220  RETURN_VALUE     
              222  JUMP_BACK           114  'to 114'

Parse error at or near `COME_FROM' instruction at offset 82_0

    def _scan_name(self, i, declstartpos):
        rawdata = self.rawdata
        n = len(rawdata)
        if i == n:
            return (None, -1)
        m = _declname_match(rawdata, i)
        if m:
            s = m.group
            name = s.strip
            if i + len(s) == n:
                return (None, -1)
            return (
             name.lower, m.end)
        self.updateposdeclstartposi
        self.error('expected name token at %r' % rawdata[declstartpos:declstartpos + 20])

    def unknown_decl(self, data):
        pass