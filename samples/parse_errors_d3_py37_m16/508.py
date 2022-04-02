# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.11 (default, Sep  3 2021, 20:46:09) 
# [GCC 10.2.1 20210110]
# Embedded file name: html\parser.py
"""A parser for HTML and XHTML."""
import re, warnings, _markupbase
from html import unescape
__all__ = [
 'HTMLParser']
interesting_normal = re.compile('[&<]')
incomplete = re.compile('&[a-zA-Z#]')
entityref = re.compile('&([a-zA-Z][-.a-zA-Z0-9]*)[^a-zA-Z0-9]')
charref = re.compile('&#(?:[0-9]+|[xX][0-9a-fA-F]+)[^0-9a-fA-F]')
starttagopen = re.compile('<[a-zA-Z]')
piclose = re.compile('>')
commentclose = re.compile('--\\s*>')
tagfind_tolerant = re.compile('([a-zA-Z][^\\t\\n\\r\\f />\\x00]*)(?:\\s|/(?!>))*')
attrfind_tolerant = re.compile('((?<=[\\\'"\\s/])[^\\s/>][^\\s/=>]*)(\\s*=+\\s*(\\\'[^\\\']*\\\'|"[^"]*"|(?![\\\'"])[^>\\s]*))?(?:\\s|/(?!>))*')
locatestarttagend_tolerant = re.compile('\n  <[a-zA-Z][^\\t\\n\\r\\f />\\x00]*       # tag name\n  (?:[\\s/]*                          # optional whitespace before attribute name\n    (?:(?<=[\'"\\s/])[^\\s/>][^\\s/=>]*  # attribute name\n      (?:\\s*=+\\s*                    # value indicator\n        (?:\'[^\']*\'                   # LITA-enclosed value\n          |"[^"]*"                   # LIT-enclosed value\n          |(?![\'"])[^>\\s]*           # bare value\n         )\n         (?:\\s*,)*                   # possibly followed by a comma\n       )?(?:\\s|/(?!>))*\n     )*\n   )?\n  \\s*                                # trailing whitespace\n', re.VERBOSE)
endendtag = re.compile('>')
endtagfind = re.compile('</\\s*([a-zA-Z][-.a-zA-Z0-9:_]*)\\s*>')

class HTMLParser(_markupbase.ParserBase):
    __doc__ = 'Find tags and other markup and call handler functions.\n\n    Usage:\n        p = HTMLParser()\n        p.feed(data)\n        ...\n        p.close()\n\n    Start tags are handled by calling self.handle_starttag() or\n    self.handle_startendtag(); end tags by self.handle_endtag().  The\n    data between tags is passed from the parser to the derived class\n    by calling self.handle_data() with the data as argument (the data\n    may be split up in arbitrary chunks).  If convert_charrefs is\n    True the character references are converted automatically to the\n    corresponding Unicode character (and self.handle_data() is no\n    longer split in chunks), otherwise they are passed by calling\n    self.handle_entityref() or self.handle_charref() with the string\n    containing respectively the named or numeric reference as the\n    argument.\n    '
    CDATA_CONTENT_ELEMENTS = ('script', 'style')

    def __init__(self, *, convert_charrefs=True):
        """Initialize and reset this instance.

        If convert_charrefs is True (the default), all character references
        are automatically converted to the corresponding Unicode characters.
        """
        self.convert_charrefs = convert_charrefs
        self.reset()

    def reset(self):
        """Reset this instance.  Loses all unprocessed data."""
        self.rawdata = ''
        self.lasttag = '???'
        self.interesting = interesting_normal
        self.cdata_elem = None
        _markupbase.ParserBase.reset(self)

    def feed(self, data):
        r"""Feed data to the parser.

        Call this as often as you want, with as little or as much text
        as you want (may include '\n').
        """
        self.rawdata = self.rawdata + data
        self.goahead(0)

    def close(self):
        """Handle any buffered data."""
        self.goahead(1)

    _HTMLParser__starttag_text = None

    def get_starttag_text(self):
        """Return full source of start tag: '<...>'."""
        return self._HTMLParser__starttag_text

    def set_cdata_mode(self, elem):
        self.cdata_elem = elem.lower()
        self.interesting = re.compile('</\\s*%s\\s*>' % self.cdata_elem, re.I)

    def clear_cdata_mode(self):
        self.interesting = interesting_normal
        self.cdata_elem = None

    def goahead--- This code section failed: ---

 L. 135         0  LOAD_FAST                'self'
                2  LOAD_ATTR                rawdata
                4  STORE_FAST               'rawdata'

 L. 136         6  LOAD_CONST               0
                8  STORE_FAST               'i'

 L. 137        10  LOAD_GLOBAL              len
               12  LOAD_FAST                'rawdata'
               14  CALL_FUNCTION_1       1  '1 positional argument'
               16  STORE_FAST               'n'

 L. 138     18_20  SETUP_LOOP          990  'to 990'
             22_0  COME_FROM           986  '986'
             22_1  COME_FROM           976  '976'
             22_2  COME_FROM           972  '972'
             22_3  COME_FROM           838  '838'
             22_4  COME_FROM           742  '742'
             22_5  COME_FROM           680  '680'
             22_6  COME_FROM           578  '578'
               22  LOAD_FAST                'i'
               24  LOAD_FAST                'n'
               26  COMPARE_OP               <
            28_30  POP_JUMP_IF_FALSE   988  'to 988'

 L. 139        32  LOAD_FAST                'self'
               34  LOAD_ATTR                convert_charrefs
               36  POP_JUMP_IF_FALSE   120  'to 120'
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                cdata_elem
               42  POP_JUMP_IF_TRUE    120  'to 120'

 L. 140        44  LOAD_FAST                'rawdata'
               46  LOAD_METHOD              find
               48  LOAD_STR                 '<'
               50  LOAD_FAST                'i'
               52  CALL_METHOD_2         2  '2 positional arguments'
               54  STORE_FAST               'j'

 L. 141        56  LOAD_FAST                'j'
               58  LOAD_CONST               0
               60  COMPARE_OP               <
               62  POP_JUMP_IF_FALSE   160  'to 160'

 L. 148        64  LOAD_FAST                'rawdata'
               66  LOAD_METHOD              rfind
               68  LOAD_STR                 '&'
               70  LOAD_GLOBAL              max
               72  LOAD_FAST                'i'
               74  LOAD_FAST                'n'
               76  LOAD_CONST               34
               78  BINARY_SUBTRACT  
               80  CALL_FUNCTION_2       2  '2 positional arguments'
               82  CALL_METHOD_2         2  '2 positional arguments'
               84  STORE_FAST               'amppos'

 L. 149        86  LOAD_FAST                'amppos'
               88  LOAD_CONST               0
               90  COMPARE_OP               >=
               92  POP_JUMP_IF_FALSE   114  'to 114'

 L. 150        94  LOAD_GLOBAL              re
               96  LOAD_METHOD              compile
               98  LOAD_STR                 '[\\s;]'
              100  CALL_METHOD_1         1  '1 positional argument'
              102  LOAD_METHOD              search
              104  LOAD_FAST                'rawdata'
              106  LOAD_FAST                'amppos'
              108  CALL_METHOD_2         2  '2 positional arguments'
              110  POP_JUMP_IF_TRUE    114  'to 114'

 L. 151       112  BREAK_LOOP       
            114_0  COME_FROM           110  '110'
            114_1  COME_FROM            92  '92'

 L. 152       114  LOAD_FAST                'n'
              116  STORE_FAST               'j'
              118  JUMP_FORWARD        160  'to 160'
            120_0  COME_FROM            42  '42'
            120_1  COME_FROM            36  '36'

 L. 154       120  LOAD_FAST                'self'
              122  LOAD_ATTR                interesting
              124  LOAD_METHOD              search
              126  LOAD_FAST                'rawdata'
              128  LOAD_FAST                'i'
              130  CALL_METHOD_2         2  '2 positional arguments'
              132  STORE_FAST               'match'

 L. 155       134  LOAD_FAST                'match'
              136  POP_JUMP_IF_FALSE   148  'to 148'

 L. 156       138  LOAD_FAST                'match'
              140  LOAD_METHOD              start
              142  CALL_METHOD_0         0  '0 positional arguments'
              144  STORE_FAST               'j'
              146  JUMP_FORWARD        160  'to 160'
            148_0  COME_FROM           136  '136'

 L. 158       148  LOAD_FAST                'self'
              150  LOAD_ATTR                cdata_elem
              152  POP_JUMP_IF_FALSE   156  'to 156'

 L. 159       154  BREAK_LOOP       
            156_0  COME_FROM           152  '152'

 L. 160       156  LOAD_FAST                'n'
              158  STORE_FAST               'j'
            160_0  COME_FROM           146  '146'
            160_1  COME_FROM           118  '118'
            160_2  COME_FROM            62  '62'

 L. 161       160  LOAD_FAST                'i'
              162  LOAD_FAST                'j'
              164  COMPARE_OP               <
              166  POP_JUMP_IF_FALSE   222  'to 222'

 L. 162       168  LOAD_FAST                'self'
              170  LOAD_ATTR                convert_charrefs
              172  POP_JUMP_IF_FALSE   204  'to 204'
              174  LOAD_FAST                'self'
              176  LOAD_ATTR                cdata_elem
              178  POP_JUMP_IF_TRUE    204  'to 204'

 L. 163       180  LOAD_FAST                'self'
              182  LOAD_METHOD              handle_data
              184  LOAD_GLOBAL              unescape
              186  LOAD_FAST                'rawdata'
              188  LOAD_FAST                'i'
              190  LOAD_FAST                'j'
              192  BUILD_SLICE_2         2 
              194  BINARY_SUBSCR    
              196  CALL_FUNCTION_1       1  '1 positional argument'
              198  CALL_METHOD_1         1  '1 positional argument'
              200  POP_TOP          
              202  JUMP_FORWARD        222  'to 222'
            204_0  COME_FROM           178  '178'
            204_1  COME_FROM           172  '172'

 L. 165       204  LOAD_FAST                'self'
              206  LOAD_METHOD              handle_data
              208  LOAD_FAST                'rawdata'
              210  LOAD_FAST                'i'
              212  LOAD_FAST                'j'
              214  BUILD_SLICE_2         2 
              216  BINARY_SUBSCR    
              218  CALL_METHOD_1         1  '1 positional argument'
              220  POP_TOP          
            222_0  COME_FROM           202  '202'
            222_1  COME_FROM           166  '166'

 L. 166       222  LOAD_FAST                'self'
              224  LOAD_METHOD              updatepos
              226  LOAD_FAST                'i'
              228  LOAD_FAST                'j'
              230  CALL_METHOD_2         2  '2 positional arguments'
              232  STORE_FAST               'i'

 L. 167       234  LOAD_FAST                'i'
              236  LOAD_FAST                'n'
              238  COMPARE_OP               ==
              240  POP_JUMP_IF_FALSE   244  'to 244'

 L. 167       242  BREAK_LOOP       
            244_0  COME_FROM           240  '240'

 L. 168       244  LOAD_FAST                'rawdata'
              246  LOAD_ATTR                startswith
              248  STORE_FAST               'startswith'

 L. 169       250  LOAD_FAST                'startswith'
              252  LOAD_STR                 '<'
              254  LOAD_FAST                'i'
              256  CALL_FUNCTION_2       2  '2 positional arguments'
          258_260  POP_JUMP_IF_FALSE   580  'to 580'

 L. 170       262  LOAD_GLOBAL              starttagopen
              264  LOAD_METHOD              match
              266  LOAD_FAST                'rawdata'
              268  LOAD_FAST                'i'
              270  CALL_METHOD_2         2  '2 positional arguments'
          272_274  POP_JUMP_IF_FALSE   288  'to 288'

 L. 171       276  LOAD_FAST                'self'
              278  LOAD_METHOD              parse_starttag
              280  LOAD_FAST                'i'
              282  CALL_METHOD_1         1  '1 positional argument'
              284  STORE_FAST               'k'
              286  JUMP_FORWARD        420  'to 420'
            288_0  COME_FROM           272  '272'

 L. 172       288  LOAD_FAST                'startswith'
              290  LOAD_STR                 '</'
              292  LOAD_FAST                'i'
              294  CALL_FUNCTION_2       2  '2 positional arguments'
          296_298  POP_JUMP_IF_FALSE   312  'to 312'

 L. 173       300  LOAD_FAST                'self'
              302  LOAD_METHOD              parse_endtag
              304  LOAD_FAST                'i'
              306  CALL_METHOD_1         1  '1 positional argument'
              308  STORE_FAST               'k'
              310  JUMP_FORWARD        420  'to 420'
            312_0  COME_FROM           296  '296'

 L. 174       312  LOAD_FAST                'startswith'
              314  LOAD_STR                 '<!--'
              316  LOAD_FAST                'i'
              318  CALL_FUNCTION_2       2  '2 positional arguments'
          320_322  POP_JUMP_IF_FALSE   336  'to 336'

 L. 175       324  LOAD_FAST                'self'
              326  LOAD_METHOD              parse_comment
              328  LOAD_FAST                'i'
              330  CALL_METHOD_1         1  '1 positional argument'
              332  STORE_FAST               'k'
              334  JUMP_FORWARD        420  'to 420'
            336_0  COME_FROM           320  '320'

 L. 176       336  LOAD_FAST                'startswith'
              338  LOAD_STR                 '<?'
              340  LOAD_FAST                'i'
              342  CALL_FUNCTION_2       2  '2 positional arguments'
          344_346  POP_JUMP_IF_FALSE   360  'to 360'

 L. 177       348  LOAD_FAST                'self'
              350  LOAD_METHOD              parse_pi
              352  LOAD_FAST                'i'
              354  CALL_METHOD_1         1  '1 positional argument'
              356  STORE_FAST               'k'
              358  JUMP_FORWARD        420  'to 420'
            360_0  COME_FROM           344  '344'

 L. 178       360  LOAD_FAST                'startswith'
              362  LOAD_STR                 '<!'
              364  LOAD_FAST                'i'
              366  CALL_FUNCTION_2       2  '2 positional arguments'
          368_370  POP_JUMP_IF_FALSE   384  'to 384'

 L. 179       372  LOAD_FAST                'self'
              374  LOAD_METHOD              parse_html_declaration
              376  LOAD_FAST                'i'
              378  CALL_METHOD_1         1  '1 positional argument'
              380  STORE_FAST               'k'
              382  JUMP_FORWARD        420  'to 420'
            384_0  COME_FROM           368  '368'

 L. 180       384  LOAD_FAST                'i'
              386  LOAD_CONST               1
              388  BINARY_ADD       
              390  LOAD_FAST                'n'
              392  COMPARE_OP               <
          394_396  POP_JUMP_IF_FALSE   418  'to 418'

 L. 181       398  LOAD_FAST                'self'
              400  LOAD_METHOD              handle_data
              402  LOAD_STR                 '<'
              404  CALL_METHOD_1         1  '1 positional argument'
              406  POP_TOP          

 L. 182       408  LOAD_FAST                'i'
              410  LOAD_CONST               1
              412  BINARY_ADD       
              414  STORE_FAST               'k'
              416  JUMP_FORWARD        420  'to 420'
            418_0  COME_FROM           394  '394'

 L. 184       418  BREAK_LOOP       
            420_0  COME_FROM           416  '416'
            420_1  COME_FROM           382  '382'
            420_2  COME_FROM           358  '358'
            420_3  COME_FROM           334  '334'
            420_4  COME_FROM           310  '310'
            420_5  COME_FROM           286  '286'

 L. 185       420  LOAD_FAST                'k'
              422  LOAD_CONST               0
              424  COMPARE_OP               <
          426_428  POP_JUMP_IF_FALSE   566  'to 566'

 L. 186       430  LOAD_FAST                'end'
          432_434  POP_JUMP_IF_TRUE    438  'to 438'

 L. 187       436  BREAK_LOOP       
            438_0  COME_FROM           432  '432'

 L. 188       438  LOAD_FAST                'rawdata'
              440  LOAD_METHOD              find
              442  LOAD_STR                 '>'
              444  LOAD_FAST                'i'
              446  LOAD_CONST               1
              448  BINARY_ADD       
              450  CALL_METHOD_2         2  '2 positional arguments'
              452  STORE_FAST               'k'

 L. 189       454  LOAD_FAST                'k'
              456  LOAD_CONST               0
              458  COMPARE_OP               <
          460_462  POP_JUMP_IF_FALSE   500  'to 500'

 L. 190       464  LOAD_FAST                'rawdata'
              466  LOAD_METHOD              find
              468  LOAD_STR                 '<'
              470  LOAD_FAST                'i'
              472  LOAD_CONST               1
              474  BINARY_ADD       
              476  CALL_METHOD_2         2  '2 positional arguments'
              478  STORE_FAST               'k'

 L. 191       480  LOAD_FAST                'k'
              482  LOAD_CONST               0
              484  COMPARE_OP               <
          486_488  POP_JUMP_IF_FALSE   508  'to 508'

 L. 192       490  LOAD_FAST                'i'
              492  LOAD_CONST               1
              494  BINARY_ADD       
              496  STORE_FAST               'k'
              498  JUMP_FORWARD        508  'to 508'
            500_0  COME_FROM           460  '460'

 L. 194       500  LOAD_FAST                'k'
              502  LOAD_CONST               1
              504  INPLACE_ADD      
              506  STORE_FAST               'k'
            508_0  COME_FROM           498  '498'
            508_1  COME_FROM           486  '486'

 L. 195       508  LOAD_FAST                'self'
              510  LOAD_ATTR                convert_charrefs
          512_514  POP_JUMP_IF_FALSE   548  'to 548'
              516  LOAD_FAST                'self'
              518  LOAD_ATTR                cdata_elem
          520_522  POP_JUMP_IF_TRUE    548  'to 548'

 L. 196       524  LOAD_FAST                'self'
              526  LOAD_METHOD              handle_data
              528  LOAD_GLOBAL              unescape
              530  LOAD_FAST                'rawdata'
              532  LOAD_FAST                'i'
              534  LOAD_FAST                'k'
              536  BUILD_SLICE_2         2 
              538  BINARY_SUBSCR    
              540  CALL_FUNCTION_1       1  '1 positional argument'
              542  CALL_METHOD_1         1  '1 positional argument'
              544  POP_TOP          
              546  JUMP_FORWARD        566  'to 566'
            548_0  COME_FROM           520  '520'
            548_1  COME_FROM           512  '512'

 L. 198       548  LOAD_FAST                'self'
              550  LOAD_METHOD              handle_data
              552  LOAD_FAST                'rawdata'
              554  LOAD_FAST                'i'
              556  LOAD_FAST                'k'
              558  BUILD_SLICE_2         2 
              560  BINARY_SUBSCR    
              562  CALL_METHOD_1         1  '1 positional argument'
              564  POP_TOP          
            566_0  COME_FROM           546  '546'
            566_1  COME_FROM           426  '426'

 L. 199       566  LOAD_FAST                'self'
              568  LOAD_METHOD              updatepos
              570  LOAD_FAST                'i'
              572  LOAD_FAST                'k'
              574  CALL_METHOD_2         2  '2 positional arguments'
              576  STORE_FAST               'i'
              578  JUMP_BACK            22  'to 22'
            580_0  COME_FROM           258  '258'

 L. 200       580  LOAD_FAST                'startswith'
              582  LOAD_STR                 '&#'
              584  LOAD_FAST                'i'
              586  CALL_FUNCTION_2       2  '2 positional arguments'
          588_590  POP_JUMP_IF_FALSE   744  'to 744'

 L. 201       592  LOAD_GLOBAL              charref
              594  LOAD_METHOD              match
              596  LOAD_FAST                'rawdata'
              598  LOAD_FAST                'i'
              600  CALL_METHOD_2         2  '2 positional arguments'
              602  STORE_FAST               'match'

 L. 202       604  LOAD_FAST                'match'
          606_608  POP_JUMP_IF_FALSE   684  'to 684'

 L. 203       610  LOAD_FAST                'match'
              612  LOAD_METHOD              group
              614  CALL_METHOD_0         0  '0 positional arguments'
              616  LOAD_CONST               2
              618  LOAD_CONST               -1
              620  BUILD_SLICE_2         2 
              622  BINARY_SUBSCR    
              624  STORE_FAST               'name'

 L. 204       626  LOAD_FAST                'self'
              628  LOAD_METHOD              handle_charref
              630  LOAD_FAST                'name'
              632  CALL_METHOD_1         1  '1 positional argument'
              634  POP_TOP          

 L. 205       636  LOAD_FAST                'match'
              638  LOAD_METHOD              end
              640  CALL_METHOD_0         0  '0 positional arguments'
              642  STORE_FAST               'k'

 L. 206       644  LOAD_FAST                'startswith'
              646  LOAD_STR                 ';'
              648  LOAD_FAST                'k'
              650  LOAD_CONST               1
              652  BINARY_SUBTRACT  
              654  CALL_FUNCTION_2       2  '2 positional arguments'
          656_658  POP_JUMP_IF_TRUE    668  'to 668'

 L. 207       660  LOAD_FAST                'k'
              662  LOAD_CONST               1
              664  BINARY_SUBTRACT  
              666  STORE_FAST               'k'
            668_0  COME_FROM           656  '656'

 L. 208       668  LOAD_FAST                'self'
              670  LOAD_METHOD              updatepos
              672  LOAD_FAST                'i'
              674  LOAD_FAST                'k'
              676  CALL_METHOD_2         2  '2 positional arguments'
              678  STORE_FAST               'i'

 L. 209       680  CONTINUE             22  'to 22'
              682  JUMP_FORWARD        742  'to 742'
            684_0  COME_FROM           606  '606'

 L. 211       684  LOAD_STR                 ';'
              686  LOAD_FAST                'rawdata'
              688  LOAD_FAST                'i'
              690  LOAD_CONST               None
              692  BUILD_SLICE_2         2 
              694  BINARY_SUBSCR    
              696  COMPARE_OP               in
          698_700  POP_JUMP_IF_FALSE   740  'to 740'

 L. 212       702  LOAD_FAST                'self'
              704  LOAD_METHOD              handle_data
              706  LOAD_FAST                'rawdata'
              708  LOAD_FAST                'i'
              710  LOAD_FAST                'i'
              712  LOAD_CONST               2
              714  BINARY_ADD       
              716  BUILD_SLICE_2         2 
              718  BINARY_SUBSCR    
              720  CALL_METHOD_1         1  '1 positional argument'
              722  POP_TOP          

 L. 213       724  LOAD_FAST                'self'
              726  LOAD_METHOD              updatepos
              728  LOAD_FAST                'i'
              730  LOAD_FAST                'i'
              732  LOAD_CONST               2
              734  BINARY_ADD       
              736  CALL_METHOD_2         2  '2 positional arguments'
              738  STORE_FAST               'i'
            740_0  COME_FROM           698  '698'

 L. 214       740  BREAK_LOOP       
            742_0  COME_FROM           682  '682'
              742  JUMP_BACK            22  'to 22'
            744_0  COME_FROM           588  '588'

 L. 215       744  LOAD_FAST                'startswith'
              746  LOAD_STR                 '&'
              748  LOAD_FAST                'i'
              750  CALL_FUNCTION_2       2  '2 positional arguments'
          752_754  POP_JUMP_IF_FALSE   974  'to 974'

 L. 216       756  LOAD_GLOBAL              entityref
              758  LOAD_METHOD              match
              760  LOAD_FAST                'rawdata'
              762  LOAD_FAST                'i'
              764  CALL_METHOD_2         2  '2 positional arguments'
              766  STORE_FAST               'match'

 L. 217       768  LOAD_FAST                'match'
          770_772  POP_JUMP_IF_FALSE   840  'to 840'

 L. 218       774  LOAD_FAST                'match'
              776  LOAD_METHOD              group
              778  LOAD_CONST               1
              780  CALL_METHOD_1         1  '1 positional argument'
              782  STORE_FAST               'name'

 L. 219       784  LOAD_FAST                'self'
              786  LOAD_METHOD              handle_entityref
              788  LOAD_FAST                'name'
              790  CALL_METHOD_1         1  '1 positional argument'
              792  POP_TOP          

 L. 220       794  LOAD_FAST                'match'
              796  LOAD_METHOD              end
              798  CALL_METHOD_0         0  '0 positional arguments'
              800  STORE_FAST               'k'

 L. 221       802  LOAD_FAST                'startswith'
              804  LOAD_STR                 ';'
              806  LOAD_FAST                'k'
              808  LOAD_CONST               1
              810  BINARY_SUBTRACT  
              812  CALL_FUNCTION_2       2  '2 positional arguments'
          814_816  POP_JUMP_IF_TRUE    826  'to 826'

 L. 222       818  LOAD_FAST                'k'
              820  LOAD_CONST               1
              822  BINARY_SUBTRACT  
              824  STORE_FAST               'k'
            826_0  COME_FROM           814  '814'

 L. 223       826  LOAD_FAST                'self'
              828  LOAD_METHOD              updatepos
              830  LOAD_FAST                'i'
              832  LOAD_FAST                'k'
              834  CALL_METHOD_2         2  '2 positional arguments'
              836  STORE_FAST               'i'

 L. 224       838  CONTINUE             22  'to 22'
            840_0  COME_FROM           770  '770'

 L. 225       840  LOAD_GLOBAL              incomplete
              842  LOAD_METHOD              match
              844  LOAD_FAST                'rawdata'
              846  LOAD_FAST                'i'
              848  CALL_METHOD_2         2  '2 positional arguments'
              850  STORE_FAST               'match'

 L. 226       852  LOAD_FAST                'match'
          854_856  POP_JUMP_IF_FALSE   928  'to 928'

 L. 228       858  LOAD_FAST                'end'
          860_862  POP_JUMP_IF_FALSE   924  'to 924'
              864  LOAD_FAST                'match'
              866  LOAD_METHOD              group
              868  CALL_METHOD_0         0  '0 positional arguments'
              870  LOAD_FAST                'rawdata'
              872  LOAD_FAST                'i'
              874  LOAD_CONST               None
              876  BUILD_SLICE_2         2 
              878  BINARY_SUBSCR    
              880  COMPARE_OP               ==
          882_884  POP_JUMP_IF_FALSE   924  'to 924'

 L. 229       886  LOAD_FAST                'match'
              888  LOAD_METHOD              end
              890  CALL_METHOD_0         0  '0 positional arguments'
              892  STORE_FAST               'k'

 L. 230       894  LOAD_FAST                'k'
              896  LOAD_FAST                'i'
              898  COMPARE_OP               <=
          900_902  POP_JUMP_IF_FALSE   908  'to 908'

 L. 231       904  LOAD_FAST                'n'
              906  STORE_FAST               'k'
            908_0  COME_FROM           900  '900'

 L. 232       908  LOAD_FAST                'self'
              910  LOAD_METHOD              updatepos
              912  LOAD_FAST                'i'
              914  LOAD_FAST                'i'
              916  LOAD_CONST               1
              918  BINARY_ADD       
              920  CALL_METHOD_2         2  '2 positional arguments'
              922  STORE_FAST               'i'
            924_0  COME_FROM           882  '882'
            924_1  COME_FROM           860  '860'

 L. 234       924  BREAK_LOOP       
              926  JUMP_FORWARD        972  'to 972'
            928_0  COME_FROM           854  '854'

 L. 235       928  LOAD_FAST                'i'
              930  LOAD_CONST               1
              932  BINARY_ADD       
              934  LOAD_FAST                'n'
              936  COMPARE_OP               <
          938_940  POP_JUMP_IF_FALSE   970  'to 970'

 L. 238       942  LOAD_FAST                'self'
              944  LOAD_METHOD              handle_data
              946  LOAD_STR                 '&'
              948  CALL_METHOD_1         1  '1 positional argument'
              950  POP_TOP          

 L. 239       952  LOAD_FAST                'self'
              954  LOAD_METHOD              updatepos
              956  LOAD_FAST                'i'
              958  LOAD_FAST                'i'
              960  LOAD_CONST               1
              962  BINARY_ADD       
              964  CALL_METHOD_2         2  '2 positional arguments'
              966  STORE_FAST               'i'
              968  JUMP_FORWARD        972  'to 972'
            970_0  COME_FROM           938  '938'

 L. 241       970  BREAK_LOOP       
            972_0  COME_FROM           968  '968'
            972_1  COME_FROM           926  '926'
              972  JUMP_BACK            22  'to 22'
            974_0  COME_FROM           752  '752'

 L. 243       974  LOAD_CONST               0
              976  POP_JUMP_IF_TRUE_BACK    22  'to 22'
              978  LOAD_GLOBAL              AssertionError
              980  LOAD_STR                 'interesting.search() lied'
              982  CALL_FUNCTION_1       1  '1 positional argument'
              984  RAISE_VARARGS_1       1  'exception instance'
              986  JUMP_BACK            22  'to 22'
            988_0  COME_FROM            28  '28'
              988  POP_BLOCK        
            990_0  COME_FROM_LOOP       18  '18'

 L. 245       990  LOAD_FAST                'end'
          992_994  POP_JUMP_IF_FALSE  1084  'to 1084'
              996  LOAD_FAST                'i'
              998  LOAD_FAST                'n'
             1000  COMPARE_OP               <
         1002_1004  POP_JUMP_IF_FALSE  1084  'to 1084'
             1006  LOAD_FAST                'self'
             1008  LOAD_ATTR                cdata_elem
         1010_1012  POP_JUMP_IF_TRUE   1084  'to 1084'

 L. 246      1014  LOAD_FAST                'self'
             1016  LOAD_ATTR                convert_charrefs
         1018_1020  POP_JUMP_IF_FALSE  1054  'to 1054'
             1022  LOAD_FAST                'self'
             1024  LOAD_ATTR                cdata_elem
         1026_1028  POP_JUMP_IF_TRUE   1054  'to 1054'

 L. 247      1030  LOAD_FAST                'self'
             1032  LOAD_METHOD              handle_data
             1034  LOAD_GLOBAL              unescape
             1036  LOAD_FAST                'rawdata'
             1038  LOAD_FAST                'i'
             1040  LOAD_FAST                'n'
             1042  BUILD_SLICE_2         2 
             1044  BINARY_SUBSCR    
             1046  CALL_FUNCTION_1       1  '1 positional argument'
             1048  CALL_METHOD_1         1  '1 positional argument'
             1050  POP_TOP          
             1052  JUMP_FORWARD       1072  'to 1072'
           1054_0  COME_FROM          1026  '1026'
           1054_1  COME_FROM          1018  '1018'

 L. 249      1054  LOAD_FAST                'self'
             1056  LOAD_METHOD              handle_data
             1058  LOAD_FAST                'rawdata'
             1060  LOAD_FAST                'i'
             1062  LOAD_FAST                'n'
             1064  BUILD_SLICE_2         2 
             1066  BINARY_SUBSCR    
             1068  CALL_METHOD_1         1  '1 positional argument'
             1070  POP_TOP          
           1072_0  COME_FROM          1052  '1052'

 L. 250      1072  LOAD_FAST                'self'
             1074  LOAD_METHOD              updatepos
             1076  LOAD_FAST                'i'
             1078  LOAD_FAST                'n'
             1080  CALL_METHOD_2         2  '2 positional arguments'
             1082  STORE_FAST               'i'
           1084_0  COME_FROM          1010  '1010'
           1084_1  COME_FROM          1002  '1002'
           1084_2  COME_FROM           992  '992'

 L. 251      1084  LOAD_FAST                'rawdata'
             1086  LOAD_FAST                'i'
             1088  LOAD_CONST               None
             1090  BUILD_SLICE_2         2 
             1092  BINARY_SUBSCR    
             1094  LOAD_FAST                'self'
             1096  STORE_ATTR               rawdata

Parse error at or near `LOAD_FAST' instruction at offset 160

    def parse_html_declaration(self, i):
        rawdata = self.rawdata
        assert rawdata[i:i + 2] == '<!', 'unexpected call to parse_html_declaration()'
        if rawdata[i:i + 4] == '<!--':
            return self.parse_comment(i)
        if rawdata[i:i + 3] == '<![':
            return self.parse_marked_section(i)
        if rawdata[i:i + 9].lower() == '<!doctype':
            gtpos = rawdata.find('>', i + 9)
            if gtpos == -1:
                return -1
            self.handle_decl(rawdata[i + 2:gtpos])
            return gtpos + 1
        return self.parse_bogus_comment(i)

    def parse_bogus_comment(self, i, report=1):
        rawdata = self.rawdata
        assert rawdata[i:i + 2] in ('<!', '</'), 'unexpected call to parse_comment()'
        pos = rawdata.find('>', i + 2)
        if pos == -1:
            return -1
        if report:
            self.handle_comment(rawdata[i + 2:pos])
        return pos + 1

    def parse_pi(self, i):
        rawdata = self.rawdata
        assert rawdata[i:i + 2] == '<?', 'unexpected call to parse_pi()'
        match = piclose.search(rawdata, i + 2)
        if not match:
            return -1
        j = match.start()
        self.handle_pi(rawdata[i + 2:j])
        j = match.end()
        return j

    def parse_starttag(self, i):
        self._HTMLParser__starttag_text = None
        endpos = self.check_for_whole_start_tag(i)
        if endpos < 0:
            return endpos
        rawdata = self.rawdata
        self._HTMLParser__starttag_text = rawdata[i:endpos]
        attrs = []
        match = tagfind_tolerant.match(rawdata, i + 1)
        assert match, 'unexpected call to parse_starttag()'
        k = match.end()
        self.lasttag = tag = match.group(1).lower()
        while k < endpos:
            m = attrfind_tolerant.match(rawdata, k)
            if not m:
                break
            else:
                attrname, rest, attrvalue = m.group(1, 2, 3)
                if not rest:
                    attrvalue = None
                elif not attrvalue[:1] == "'" == attrvalue[-1:]:
                    if attrvalue[:1] == '"' == attrvalue[-1:]:
                        attrvalue = attrvalue[1:-1]
                if attrvalue:
                    attrvalue = unescape(attrvalue)
                attrs.append((attrname.lower(), attrvalue))
                k = m.end()

        end = rawdata[k:endpos].strip()
        if end not in ('>', '/>'):
            lineno, offset = self.getpos()
            if '\n' in self._HTMLParser__starttag_text:
                lineno = lineno + self._HTMLParser__starttag_text.count('\n')
                offset = len(self._HTMLParser__starttag_text) - self._HTMLParser__starttag_text.rfind('\n')
            else:
                offset = offset + len(self._HTMLParser__starttag_text)
            self.handle_data(rawdata[i:endpos])
            return endpos
        if end.endswith('/>'):
            self.handle_startendtag(tag, attrs)
        else:
            self.handle_starttag(tag, attrs)
            if tag in self.CDATA_CONTENT_ELEMENTS:
                self.set_cdata_mode(tag)
        return endpos

    def check_for_whole_start_tag(self, i):
        rawdata = self.rawdata
        m = locatestarttagend_tolerant.match(rawdata, i)
        if m:
            j = m.end()
            next = rawdata[j:j + 1]
            if next == '>':
                return j + 1
            if next == '/':
                if rawdata.startswith('/>', j):
                    return j + 2
                if rawdata.startswith('/', j):
                    return -1
                if j > i:
                    return j
                return i + 1
            if next == '':
                return -1
            if next in 'abcdefghijklmnopqrstuvwxyz=/ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                return -1
            if j > i:
                return j
            return i + 1
        raise AssertionError('we should not get here!')

    def parse_endtag(self, i):
        rawdata = self.rawdata
        assert rawdata[i:i + 2] == '</', 'unexpected call to parse_endtag'
        match = endendtag.search(rawdata, i + 1)
        if not match:
            return -1
        gtpos = match.end()
        match = endtagfind.match(rawdata, i)
        if not match:
            if self.cdata_elem is not None:
                self.handle_data(rawdata[i:gtpos])
                return gtpos
            namematch = tagfind_tolerant.match(rawdata, i + 2)
            if not namematch:
                if rawdata[i:i + 3] == '</>':
                    return i + 3
                return self.parse_bogus_comment(i)
            tagname = namematch.group(1).lower()
            gtpos = rawdata.find('>', namematch.end())
            self.handle_endtag(tagname)
            return gtpos + 1
        elem = match.group(1).lower()
        if self.cdata_elem is not None:
            if elem != self.cdata_elem:
                self.handle_data(rawdata[i:gtpos])
                return gtpos
        self.handle_endtag(elem)
        self.clear_cdata_mode()
        return gtpos

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def handle_charref(self, name):
        pass

    def handle_entityref(self, name):
        pass

    def handle_data(self, data):
        pass

    def handle_comment(self, data):
        pass

    def handle_decl(self, decl):
        pass

    def handle_pi(self, data):
        pass

    def unknown_decl(self, data):
        pass

    def unescape(self, s):
        warnings.warn('The unescape method is deprecated and will be removed in 3.5, use html.unescape() instead.', DeprecationWarning,
          stacklevel=2)
        return unescape(s)