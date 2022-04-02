# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: html\__init__.py
"""
General functions for HTML manipulation.
"""
import re as _re
import html.entities as _html5
__all__ = [
 'escape', 'unescape']

def escape(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace('&', '&amp;')
    s = s.replace('<', '&lt;')
    s = s.replace('>', '&gt;')
    if quote:
        s = s.replace('"', '&quot;')
        s = s.replace("'", '&#x27;')
    return s


_invalid_charrefs = {0:'�', 
 13:'\r', 
 128:'€', 
 129:'\x81', 
 130:'‚', 
 131:'ƒ', 
 132:'„', 
 133:'…', 
 134:'†', 
 135:'‡', 
 136:'ˆ', 
 137:'‰', 
 138:'Š', 
 139:'‹', 
 140:'Œ', 
 141:'\x8d', 
 142:'Ž', 
 143:'\x8f', 
 144:'\x90', 
 145:'‘', 
 146:'’', 
 147:'“', 
 148:'”', 
 149:'•', 
 150:'–', 
 151:'—', 
 152:'˜', 
 153:'™', 
 154:'š', 
 155:'›', 
 156:'œ', 
 157:'\x9d', 
 158:'ž', 
 159:'Ÿ'}
_invalid_codepoints = {
 1, 2, 3, 4, 5, 6, 7, 8,
 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
 26, 27, 28, 29, 30, 31,
 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138,
 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150,
 151, 152, 153, 154, 155, 156, 157, 158, 159,
 64976, 64977, 64978, 64979, 64980, 64981, 64982, 64983, 64984,
 64985, 64986, 64987, 64988, 64989, 64990, 64991, 64992, 64993,
 64994, 64995, 64996, 64997, 64998, 64999, 65000, 65001, 65002,
 65003, 65004, 65005, 65006, 65007,
 11, 65534, 65535, 131070, 131071, 196606, 196607, 262142, 262143,
 327678, 327679, 393214, 393215, 458750, 458751, 524286, 524287,
 589822, 589823, 655358, 655359, 720894, 720895, 786430, 786431,
 851966, 851967, 917502, 917503, 983038, 983039, 1048574, 1048575,
 1114110, 1114111}

def _replace_charref--- This code section failed: ---

 L.  92         0  LOAD_FAST                's'
                2  LOAD_METHOD              group
                4  LOAD_CONST               1
                6  CALL_METHOD_1         1  '1 positional argument'
                8  STORE_FAST               's'

 L.  93        10  LOAD_FAST                's'
               12  LOAD_CONST               0
               14  BINARY_SUBSCR    
               16  LOAD_STR                 '#'
               18  COMPARE_OP               ==
               20  POP_JUMP_IF_FALSE   152  'to 152'

 L.  95        22  LOAD_FAST                's'
               24  LOAD_CONST               1
               26  BINARY_SUBSCR    
               28  LOAD_STR                 'xX'
               30  COMPARE_OP               in
               32  POP_JUMP_IF_FALSE    60  'to 60'

 L.  96        34  LOAD_GLOBAL              int
               36  LOAD_FAST                's'
               38  LOAD_CONST               2
               40  LOAD_CONST               None
               42  BUILD_SLICE_2         2 
               44  BINARY_SUBSCR    
               46  LOAD_METHOD              rstrip
               48  LOAD_STR                 ';'
               50  CALL_METHOD_1         1  '1 positional argument'
               52  LOAD_CONST               16
               54  CALL_FUNCTION_2       2  '2 positional arguments'
               56  STORE_FAST               'num'
               58  JUMP_FORWARD         82  'to 82'
             60_0  COME_FROM            32  '32'

 L.  98        60  LOAD_GLOBAL              int
               62  LOAD_FAST                's'
               64  LOAD_CONST               1
               66  LOAD_CONST               None
               68  BUILD_SLICE_2         2 
               70  BINARY_SUBSCR    
               72  LOAD_METHOD              rstrip
               74  LOAD_STR                 ';'
               76  CALL_METHOD_1         1  '1 positional argument'
               78  CALL_FUNCTION_1       1  '1 positional argument'
               80  STORE_FAST               'num'
             82_0  COME_FROM            58  '58'

 L.  99        82  LOAD_FAST                'num'
               84  LOAD_GLOBAL              _invalid_charrefs
               86  COMPARE_OP               in
               88  POP_JUMP_IF_FALSE    98  'to 98'

 L. 100        90  LOAD_GLOBAL              _invalid_charrefs
               92  LOAD_FAST                'num'
               94  BINARY_SUBSCR    
               96  RETURN_VALUE     
             98_0  COME_FROM            88  '88'

 L. 101        98  LOAD_CONST               55296
              100  LOAD_FAST                'num'
              102  DUP_TOP          
              104  ROT_THREE        
              106  COMPARE_OP               <=
              108  POP_JUMP_IF_FALSE   118  'to 118'
              110  LOAD_CONST               57343
              112  COMPARE_OP               <=
              114  POP_JUMP_IF_TRUE    128  'to 128'
              116  JUMP_FORWARD        120  'to 120'
            118_0  COME_FROM           108  '108'
              118  POP_TOP          
            120_0  COME_FROM           116  '116'
              120  LOAD_FAST                'num'
              122  LOAD_CONST               1114111
              124  COMPARE_OP               >
              126  POP_JUMP_IF_FALSE   132  'to 132'
            128_0  COME_FROM           114  '114'

 L. 102       128  LOAD_STR                 '�'
              130  RETURN_VALUE     
            132_0  COME_FROM           126  '126'

 L. 103       132  LOAD_FAST                'num'
              134  LOAD_GLOBAL              _invalid_codepoints
              136  COMPARE_OP               in
              138  POP_JUMP_IF_FALSE   144  'to 144'

 L. 104       140  LOAD_STR                 ''
              142  RETURN_VALUE     
            144_0  COME_FROM           138  '138'

 L. 105       144  LOAD_GLOBAL              chr
              146  LOAD_FAST                'num'
              148  CALL_FUNCTION_1       1  '1 positional argument'
              150  RETURN_VALUE     
            152_0  COME_FROM            20  '20'

 L. 108       152  LOAD_FAST                's'
              154  LOAD_GLOBAL              _html5
              156  COMPARE_OP               in
              158  POP_JUMP_IF_FALSE   168  'to 168'

 L. 109       160  LOAD_GLOBAL              _html5
              162  LOAD_FAST                's'
              164  BINARY_SUBSCR    
              166  RETURN_VALUE     
            168_0  COME_FROM           158  '158'

 L. 111       168  SETUP_LOOP          250  'to 250'
              170  LOAD_GLOBAL              range
              172  LOAD_GLOBAL              len
              174  LOAD_FAST                's'
              176  CALL_FUNCTION_1       1  '1 positional argument'
              178  LOAD_CONST               1
              180  BINARY_SUBTRACT  
              182  LOAD_CONST               1
              184  LOAD_CONST               -1
              186  CALL_FUNCTION_3       3  '3 positional arguments'
              188  GET_ITER         
            190_0  COME_FROM           238  '238'
            190_1  COME_FROM           208  '208'
              190  FOR_ITER            240  'to 240'
              192  STORE_FAST               'x'

 L. 112       194  LOAD_FAST                's'
              196  LOAD_CONST               None
              198  LOAD_FAST                'x'
              200  BUILD_SLICE_2         2 
              202  BINARY_SUBSCR    
              204  LOAD_GLOBAL              _html5
              206  COMPARE_OP               in
              208  POP_JUMP_IF_FALSE_BACK   190  'to 190'

 L. 113       210  LOAD_GLOBAL              _html5
              212  LOAD_FAST                's'
              214  LOAD_CONST               None
              216  LOAD_FAST                'x'
              218  BUILD_SLICE_2         2 
              220  BINARY_SUBSCR    
              222  BINARY_SUBSCR    
              224  LOAD_FAST                's'
              226  LOAD_FAST                'x'
              228  LOAD_CONST               None
              230  BUILD_SLICE_2         2 
              232  BINARY_SUBSCR    
              234  BINARY_ADD       
              236  RETURN_VALUE     
              238  JUMP_BACK           190  'to 190'
              240  POP_BLOCK        

 L. 115       242  LOAD_STR                 '&'
              244  LOAD_FAST                's'
              246  BINARY_ADD       
              248  RETURN_VALUE     
            250_0  COME_FROM_LOOP      168  '168'

Parse error at or near `LOAD_FAST' instruction at offset 132


_charref = _re.compile('&(#[0-9]+;?|#[xX][0-9a-fA-F]+;?|[^\\t\\n\\f <&#;]{1,32};?)')

def unescape(s):
    """
    Convert all named and numeric character references (e.g. &gt;, &#62;,
    &x3e;) in the string s to the corresponding unicode characters.
    This function uses the rules defined by the HTML 5 standard
    for both valid and invalid character references, and the list of
    HTML 5 named character references defined in html.entities.html5.
    """
    if '&' not in s:
        return s
    return _charref.sub(_replace_charref, s)