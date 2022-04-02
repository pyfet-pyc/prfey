# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
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
locatestarttagend_tolerant = re.compile('\n  <[a-zA-Z][^\\t\\n\\r\\f />\\x00]*       # tag name\n  (?:[\\s/]*                          # optional whitespace before attribute name\n    (?:(?<=[\'"\\s/])[^\\s/>][^\\s/=>]*  # attribute name\n      (?:\\s*=+\\s*                    # value indicator\n        (?:\'[^\']*\'                   # LITA-enclosed value\n          |"[^"]*"                   # LIT-enclosed value\n          |(?![\'"])[^>\\s]*           # bare value\n         )\n        \\s*                          # possibly followed by a space\n       )?(?:\\s|/(?!>))*\n     )*\n   )?\n  \\s*                                # trailing whitespace\n', re.VERBOSE)
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
               14  CALL_FUNCTION_1       1  ''
               16  STORE_FAST               'n'
             18_0  COME_FROM           998  '998'
             18_1  COME_FROM           988  '988'
             18_2  COME_FROM           984  '984'
             18_3  COME_FROM           846  '846'
             18_4  COME_FROM           750  '750'
             18_5  COME_FROM           686  '686'
             18_6  COME_FROM           584  '584'

 L. 138        18  LOAD_FAST                'i'
               20  LOAD_FAST                'n'
               22  COMPARE_OP               <
            24_26  POP_JUMP_IF_FALSE  1000  'to 1000'

 L. 139        28  LOAD_FAST                'self'
               30  LOAD_ATTR                convert_charrefs
               32  POP_JUMP_IF_FALSE   118  'to 118'
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                cdata_elem
               38  POP_JUMP_IF_TRUE    118  'to 118'

 L. 140        40  LOAD_FAST                'rawdata'
               42  LOAD_METHOD              find
               44  LOAD_STR                 '<'
               46  LOAD_FAST                'i'
               48  CALL_METHOD_2         2  ''
               50  STORE_FAST               'j'

 L. 141        52  LOAD_FAST                'j'
               54  LOAD_CONST               0
               56  COMPARE_OP               <
               58  POP_JUMP_IF_FALSE   160  'to 160'

 L. 148        60  LOAD_FAST                'rawdata'
               62  LOAD_METHOD              rfind
               64  LOAD_STR                 '&'
               66  LOAD_GLOBAL              max
               68  LOAD_FAST                'i'
               70  LOAD_FAST                'n'
               72  LOAD_CONST               34
               74  BINARY_SUBTRACT  
               76  CALL_FUNCTION_2       2  ''
               78  CALL_METHOD_2         2  ''
               80  STORE_FAST               'amppos'

 L. 149        82  LOAD_FAST                'amppos'
               84  LOAD_CONST               0
               86  COMPARE_OP               >=
               88  POP_JUMP_IF_FALSE   112  'to 112'

 L. 150        90  LOAD_GLOBAL              re
               92  LOAD_METHOD              compile
               94  LOAD_STR                 '[\\s;]'
               96  CALL_METHOD_1         1  ''
               98  LOAD_METHOD              search
              100  LOAD_FAST                'rawdata'
              102  LOAD_FAST                'amppos'
              104  CALL_METHOD_2         2  ''

 L. 149       106  POP_JUMP_IF_TRUE    112  'to 112'

 L. 151   108_110  BREAK_LOOP         1000  'to 1000'
            112_0  COME_FROM           106  '106'
            112_1  COME_FROM            88  '88'

 L. 152       112  LOAD_FAST                'n'
              114  STORE_FAST               'j'
              116  JUMP_FORWARD        160  'to 160'
            118_0  COME_FROM            38  '38'
            118_1  COME_FROM            32  '32'

 L. 154       118  LOAD_FAST                'self'
              120  LOAD_ATTR                interesting
              122  LOAD_METHOD              search
              124  LOAD_FAST                'rawdata'
              126  LOAD_FAST                'i'
              128  CALL_METHOD_2         2  ''
              130  STORE_FAST               'match'

 L. 155       132  LOAD_FAST                'match'
              134  POP_JUMP_IF_FALSE   146  'to 146'

 L. 156       136  LOAD_FAST                'match'
              138  LOAD_METHOD              start
              140  CALL_METHOD_0         0  ''
              142  STORE_FAST               'j'
              144  JUMP_FORWARD        160  'to 160'
            146_0  COME_FROM           134  '134'

 L. 158       146  LOAD_FAST                'self'
              148  LOAD_ATTR                cdata_elem
              150  POP_JUMP_IF_FALSE   156  'to 156'

 L. 159   152_154  JUMP_FORWARD       1000  'to 1000'
            156_0  COME_FROM           150  '150'

 L. 160       156  LOAD_FAST                'n'
              158  STORE_FAST               'j'
            160_0  COME_FROM           144  '144'
            160_1  COME_FROM           116  '116'
            160_2  COME_FROM            58  '58'

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
              196  CALL_FUNCTION_1       1  ''
              198  CALL_METHOD_1         1  ''
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
              218  CALL_METHOD_1         1  ''
              220  POP_TOP          
            222_0  COME_FROM           202  '202'
            222_1  COME_FROM           166  '166'

 L. 166       222  LOAD_FAST                'self'
              224  LOAD_METHOD              updatepos
              226  LOAD_FAST                'i'
              228  LOAD_FAST                'j'
              230  CALL_METHOD_2         2  ''
              232  STORE_FAST               'i'

 L. 167       234  LOAD_FAST                'i'
              236  LOAD_FAST                'n'
              238  COMPARE_OP               ==
              240  POP_JUMP_IF_FALSE   246  'to 246'

 L. 167   242_244  JUMP_FORWARD       1000  'to 1000'
            246_0  COME_FROM           240  '240'

 L. 168       246  LOAD_FAST                'rawdata'
              248  LOAD_ATTR                startswith
              250  STORE_FAST               'startswith'

 L. 169       252  LOAD_FAST                'startswith'
              254  LOAD_STR                 '<'
              256  LOAD_FAST                'i'
              258  CALL_FUNCTION_2       2  ''
          260_262  POP_JUMP_IF_FALSE   586  'to 586'

 L. 170       264  LOAD_GLOBAL              starttagopen
              266  LOAD_METHOD              match
              268  LOAD_FAST                'rawdata'
              270  LOAD_FAST                'i'
              272  CALL_METHOD_2         2  ''
          274_276  POP_JUMP_IF_FALSE   290  'to 290'

 L. 171       278  LOAD_FAST                'self'
              280  LOAD_METHOD              parse_starttag
              282  LOAD_FAST                'i'
              284  CALL_METHOD_1         1  ''
              286  STORE_FAST               'k'
              288  JUMP_FORWARD        424  'to 424'
            290_0  COME_FROM           274  '274'

 L. 172       290  LOAD_FAST                'startswith'
              292  LOAD_STR                 '</'
              294  LOAD_FAST                'i'
              296  CALL_FUNCTION_2       2  ''
          298_300  POP_JUMP_IF_FALSE   314  'to 314'

 L. 173       302  LOAD_FAST                'self'
              304  LOAD_METHOD              parse_endtag
              306  LOAD_FAST                'i'
              308  CALL_METHOD_1         1  ''
              310  STORE_FAST               'k'
              312  JUMP_FORWARD        424  'to 424'
            314_0  COME_FROM           298  '298'

 L. 174       314  LOAD_FAST                'startswith'
              316  LOAD_STR                 '<!--'
              318  LOAD_FAST                'i'
              320  CALL_FUNCTION_2       2  ''
          322_324  POP_JUMP_IF_FALSE   338  'to 338'

 L. 175       326  LOAD_FAST                'self'
              328  LOAD_METHOD              parse_comment
              330  LOAD_FAST                'i'
              332  CALL_METHOD_1         1  ''
              334  STORE_FAST               'k'
              336  JUMP_FORWARD        424  'to 424'
            338_0  COME_FROM           322  '322'

 L. 176       338  LOAD_FAST                'startswith'
              340  LOAD_STR                 '<?'
              342  LOAD_FAST                'i'
              344  CALL_FUNCTION_2       2  ''
          346_348  POP_JUMP_IF_FALSE   362  'to 362'

 L. 177       350  LOAD_FAST                'self'
              352  LOAD_METHOD              parse_pi
              354  LOAD_FAST                'i'
              356  CALL_METHOD_1         1  ''
              358  STORE_FAST               'k'
              360  JUMP_FORWARD        424  'to 424'
            362_0  COME_FROM           346  '346'

 L. 178       362  LOAD_FAST                'startswith'
              364  LOAD_STR                 '<!'
              366  LOAD_FAST                'i'
              368  CALL_FUNCTION_2       2  ''
          370_372  POP_JUMP_IF_FALSE   386  'to 386'

 L. 179       374  LOAD_FAST                'self'
              376  LOAD_METHOD              parse_html_declaration
              378  LOAD_FAST                'i'
              380  CALL_METHOD_1         1  ''
              382  STORE_FAST               'k'
              384  JUMP_FORWARD        424  'to 424'
            386_0  COME_FROM           370  '370'

 L. 180       386  LOAD_FAST                'i'
              388  LOAD_CONST               1
              390  BINARY_ADD       
              392  LOAD_FAST                'n'
              394  COMPARE_OP               <
          396_398  POP_JUMP_IF_FALSE  1000  'to 1000'

 L. 181       400  LOAD_FAST                'self'
              402  LOAD_METHOD              handle_data
              404  LOAD_STR                 '<'
              406  CALL_METHOD_1         1  ''
              408  POP_TOP          

 L. 182       410  LOAD_FAST                'i'
              412  LOAD_CONST               1
              414  BINARY_ADD       
              416  STORE_FAST               'k'
              418  JUMP_FORWARD        424  'to 424'

 L. 184   420_422  JUMP_FORWARD       1000  'to 1000'
            424_0  COME_FROM           418  '418'
            424_1  COME_FROM           384  '384'
            424_2  COME_FROM           360  '360'
            424_3  COME_FROM           336  '336'
            424_4  COME_FROM           312  '312'
            424_5  COME_FROM           288  '288'

 L. 185       424  LOAD_FAST                'k'
              426  LOAD_CONST               0
              428  COMPARE_OP               <
          430_432  POP_JUMP_IF_FALSE   572  'to 572'

 L. 186       434  LOAD_FAST                'end'
          436_438  POP_JUMP_IF_TRUE    444  'to 444'

 L. 187   440_442  JUMP_FORWARD       1000  'to 1000'
            444_0  COME_FROM           436  '436'

 L. 188       444  LOAD_FAST                'rawdata'
              446  LOAD_METHOD              find
              448  LOAD_STR                 '>'
              450  LOAD_FAST                'i'
              452  LOAD_CONST               1
              454  BINARY_ADD       
              456  CALL_METHOD_2         2  ''
              458  STORE_FAST               'k'

 L. 189       460  LOAD_FAST                'k'
              462  LOAD_CONST               0
              464  COMPARE_OP               <
          466_468  POP_JUMP_IF_FALSE   506  'to 506'

 L. 190       470  LOAD_FAST                'rawdata'
              472  LOAD_METHOD              find
              474  LOAD_STR                 '<'
              476  LOAD_FAST                'i'
              478  LOAD_CONST               1
              480  BINARY_ADD       
              482  CALL_METHOD_2         2  ''
              484  STORE_FAST               'k'

 L. 191       486  LOAD_FAST                'k'
              488  LOAD_CONST               0
              490  COMPARE_OP               <
          492_494  POP_JUMP_IF_FALSE   514  'to 514'

 L. 192       496  LOAD_FAST                'i'
              498  LOAD_CONST               1
              500  BINARY_ADD       
              502  STORE_FAST               'k'
              504  JUMP_FORWARD        514  'to 514'
            506_0  COME_FROM           466  '466'

 L. 194       506  LOAD_FAST                'k'
              508  LOAD_CONST               1
              510  INPLACE_ADD      
              512  STORE_FAST               'k'
            514_0  COME_FROM           504  '504'
            514_1  COME_FROM           492  '492'

 L. 195       514  LOAD_FAST                'self'
              516  LOAD_ATTR                convert_charrefs
          518_520  POP_JUMP_IF_FALSE   554  'to 554'
              522  LOAD_FAST                'self'
              524  LOAD_ATTR                cdata_elem
          526_528  POP_JUMP_IF_TRUE    554  'to 554'

 L. 196       530  LOAD_FAST                'self'
              532  LOAD_METHOD              handle_data
              534  LOAD_GLOBAL              unescape
              536  LOAD_FAST                'rawdata'
              538  LOAD_FAST                'i'
              540  LOAD_FAST                'k'
              542  BUILD_SLICE_2         2 
              544  BINARY_SUBSCR    
              546  CALL_FUNCTION_1       1  ''
              548  CALL_METHOD_1         1  ''
              550  POP_TOP          
              552  JUMP_FORWARD        572  'to 572'
            554_0  COME_FROM           526  '526'
            554_1  COME_FROM           518  '518'

 L. 198       554  LOAD_FAST                'self'
              556  LOAD_METHOD              handle_data
              558  LOAD_FAST                'rawdata'
              560  LOAD_FAST                'i'
              562  LOAD_FAST                'k'
              564  BUILD_SLICE_2         2 
              566  BINARY_SUBSCR    
              568  CALL_METHOD_1         1  ''
              570  POP_TOP          
            572_0  COME_FROM           552  '552'
            572_1  COME_FROM           430  '430'

 L. 199       572  LOAD_FAST                'self'
              574  LOAD_METHOD              updatepos
              576  LOAD_FAST                'i'
              578  LOAD_FAST                'k'
              580  CALL_METHOD_2         2  ''
              582  STORE_FAST               'i'
              584  JUMP_BACK            18  'to 18'
            586_0  COME_FROM           260  '260'

 L. 200       586  LOAD_FAST                'startswith'
              588  LOAD_STR                 '&#'
              590  LOAD_FAST                'i'
              592  CALL_FUNCTION_2       2  ''
          594_596  POP_JUMP_IF_FALSE   752  'to 752'

 L. 201       598  LOAD_GLOBAL              charref
              600  LOAD_METHOD              match
              602  LOAD_FAST                'rawdata'
              604  LOAD_FAST                'i'
              606  CALL_METHOD_2         2  ''
              608  STORE_FAST               'match'

 L. 202       610  LOAD_FAST                'match'
          612_614  POP_JUMP_IF_FALSE   690  'to 690'

 L. 203       616  LOAD_FAST                'match'
              618  LOAD_METHOD              group
              620  CALL_METHOD_0         0  ''
              622  LOAD_CONST               2
              624  LOAD_CONST               -1
              626  BUILD_SLICE_2         2 
              628  BINARY_SUBSCR    
              630  STORE_FAST               'name'

 L. 204       632  LOAD_FAST                'self'
              634  LOAD_METHOD              handle_charref
              636  LOAD_FAST                'name'
              638  CALL_METHOD_1         1  ''
              640  POP_TOP          

 L. 205       642  LOAD_FAST                'match'
              644  LOAD_METHOD              end
              646  CALL_METHOD_0         0  ''
              648  STORE_FAST               'k'

 L. 206       650  LOAD_FAST                'startswith'
              652  LOAD_STR                 ';'
              654  LOAD_FAST                'k'
              656  LOAD_CONST               1
              658  BINARY_SUBTRACT  
              660  CALL_FUNCTION_2       2  ''
          662_664  POP_JUMP_IF_TRUE    674  'to 674'

 L. 207       666  LOAD_FAST                'k'
              668  LOAD_CONST               1
              670  BINARY_SUBTRACT  
              672  STORE_FAST               'k'
            674_0  COME_FROM           662  '662'

 L. 208       674  LOAD_FAST                'self'
              676  LOAD_METHOD              updatepos
              678  LOAD_FAST                'i'
              680  LOAD_FAST                'k'
              682  CALL_METHOD_2         2  ''
              684  STORE_FAST               'i'

 L. 209       686  JUMP_BACK            18  'to 18'
              688  BREAK_LOOP          750  'to 750'
            690_0  COME_FROM           612  '612'

 L. 211       690  LOAD_STR                 ';'
              692  LOAD_FAST                'rawdata'
              694  LOAD_FAST                'i'
              696  LOAD_CONST               None
              698  BUILD_SLICE_2         2 
              700  BINARY_SUBSCR    
              702  COMPARE_OP               in
          704_706  POP_JUMP_IF_FALSE  1000  'to 1000'

 L. 212       708  LOAD_FAST                'self'
              710  LOAD_METHOD              handle_data
              712  LOAD_FAST                'rawdata'
              714  LOAD_FAST                'i'
              716  LOAD_FAST                'i'
              718  LOAD_CONST               2
              720  BINARY_ADD       
              722  BUILD_SLICE_2         2 
              724  BINARY_SUBSCR    
              726  CALL_METHOD_1         1  ''
              728  POP_TOP          

 L. 213       730  LOAD_FAST                'self'
              732  LOAD_METHOD              updatepos
              734  LOAD_FAST                'i'
              736  LOAD_FAST                'i'
              738  LOAD_CONST               2
              740  BINARY_ADD       
              742  CALL_METHOD_2         2  ''
              744  STORE_FAST               'i'

 L. 214   746_748  JUMP_FORWARD       1000  'to 1000'
            750_0  COME_FROM           688  '688'
              750  JUMP_BACK            18  'to 18'
            752_0  COME_FROM           594  '594'

 L. 215       752  LOAD_FAST                'startswith'
              754  LOAD_STR                 '&'
              756  LOAD_FAST                'i'
              758  CALL_FUNCTION_2       2  ''
          760_762  POP_JUMP_IF_FALSE   986  'to 986'

 L. 216       764  LOAD_GLOBAL              entityref
              766  LOAD_METHOD              match
              768  LOAD_FAST                'rawdata'
              770  LOAD_FAST                'i'
              772  CALL_METHOD_2         2  ''
              774  STORE_FAST               'match'

 L. 217       776  LOAD_FAST                'match'
          778_780  POP_JUMP_IF_FALSE   848  'to 848'

 L. 218       782  LOAD_FAST                'match'
              784  LOAD_METHOD              group
              786  LOAD_CONST               1
              788  CALL_METHOD_1         1  ''
              790  STORE_FAST               'name'

 L. 219       792  LOAD_FAST                'self'
              794  LOAD_METHOD              handle_entityref
              796  LOAD_FAST                'name'
              798  CALL_METHOD_1         1  ''
              800  POP_TOP          

 L. 220       802  LOAD_FAST                'match'
              804  LOAD_METHOD              end
              806  CALL_METHOD_0         0  ''
              808  STORE_FAST               'k'

 L. 221       810  LOAD_FAST                'startswith'
              812  LOAD_STR                 ';'
              814  LOAD_FAST                'k'
              816  LOAD_CONST               1
              818  BINARY_SUBTRACT  
              820  CALL_FUNCTION_2       2  ''
          822_824  POP_JUMP_IF_TRUE    834  'to 834'

 L. 222       826  LOAD_FAST                'k'
              828  LOAD_CONST               1
              830  BINARY_SUBTRACT  
              832  STORE_FAST               'k'
            834_0  COME_FROM           822  '822'

 L. 223       834  LOAD_FAST                'self'
              836  LOAD_METHOD              updatepos
              838  LOAD_FAST                'i'
              840  LOAD_FAST                'k'
              842  CALL_METHOD_2         2  ''
              844  STORE_FAST               'i'

 L. 224       846  JUMP_BACK            18  'to 18'
            848_0  COME_FROM           778  '778'

 L. 225       848  LOAD_GLOBAL              incomplete
              850  LOAD_METHOD              match
              852  LOAD_FAST                'rawdata'
              854  LOAD_FAST                'i'
              856  CALL_METHOD_2         2  ''
              858  STORE_FAST               'match'

 L. 226       860  LOAD_FAST                'match'
          862_864  POP_JUMP_IF_FALSE   938  'to 938'

 L. 228       866  LOAD_FAST                'end'
          868_870  POP_JUMP_IF_FALSE  1000  'to 1000'
              872  LOAD_FAST                'match'
              874  LOAD_METHOD              group
              876  CALL_METHOD_0         0  ''
              878  LOAD_FAST                'rawdata'
              880  LOAD_FAST                'i'
              882  LOAD_CONST               None
              884  BUILD_SLICE_2         2 
              886  BINARY_SUBSCR    
              888  COMPARE_OP               ==
          890_892  POP_JUMP_IF_FALSE  1000  'to 1000'

 L. 229       894  LOAD_FAST                'match'
              896  LOAD_METHOD              end
              898  CALL_METHOD_0         0  ''
              900  STORE_FAST               'k'

 L. 230       902  LOAD_FAST                'k'
              904  LOAD_FAST                'i'
              906  COMPARE_OP               <=
          908_910  POP_JUMP_IF_FALSE   916  'to 916'

 L. 231       912  LOAD_FAST                'n'
              914  STORE_FAST               'k'
            916_0  COME_FROM           908  '908'

 L. 232       916  LOAD_FAST                'self'
              918  LOAD_METHOD              updatepos
              920  LOAD_FAST                'i'
              922  LOAD_FAST                'i'
              924  LOAD_CONST               1
              926  BINARY_ADD       
              928  CALL_METHOD_2         2  ''
              930  STORE_FAST               'i'

 L. 234   932_934  JUMP_FORWARD       1000  'to 1000'
              936  BREAK_LOOP          984  'to 984'
            938_0  COME_FROM           862  '862'

 L. 235       938  LOAD_FAST                'i'
              940  LOAD_CONST               1
              942  BINARY_ADD       
              944  LOAD_FAST                'n'
              946  COMPARE_OP               <
          948_950  POP_JUMP_IF_FALSE  1000  'to 1000'

 L. 238       952  LOAD_FAST                'self'
              954  LOAD_METHOD              handle_data
              956  LOAD_STR                 '&'
              958  CALL_METHOD_1         1  ''
              960  POP_TOP          

 L. 239       962  LOAD_FAST                'self'
              964  LOAD_METHOD              updatepos
              966  LOAD_FAST                'i'
              968  LOAD_FAST                'i'
              970  LOAD_CONST               1
              972  BINARY_ADD       
              974  CALL_METHOD_2         2  ''
              976  STORE_FAST               'i'
              978  JUMP_FORWARD        984  'to 984'

 L. 241   980_982  JUMP_FORWARD       1000  'to 1000'
            984_0  COME_FROM           978  '978'
            984_1  COME_FROM           936  '936'
              984  JUMP_BACK            18  'to 18'
            986_0  COME_FROM           760  '760'

 L. 243       986  LOAD_CONST               0
              988  POP_JUMP_IF_TRUE_BACK    18  'to 18'
              990  LOAD_GLOBAL              AssertionError
              992  LOAD_STR                 'interesting.search() lied'
              994  CALL_FUNCTION_1       1  ''
              996  RAISE_VARARGS_1       1  'exception instance'
              998  JUMP_BACK            18  'to 18'
           1000_0  COME_FROM           980  '980'
           1000_1  COME_FROM           948  '948'
           1000_2  COME_FROM           932  '932'
           1000_3  COME_FROM           890  '890'
           1000_4  COME_FROM           868  '868'
           1000_5  COME_FROM           746  '746'
           1000_6  COME_FROM           704  '704'
           1000_7  COME_FROM           440  '440'
           1000_8  COME_FROM           420  '420'
           1000_9  COME_FROM           396  '396'
          1000_10  COME_FROM           242  '242'
          1000_11  COME_FROM           152  '152'
          1000_12  COME_FROM           108  '108'
          1000_13  COME_FROM            24  '24'

 L. 245      1000  LOAD_FAST                'end'
         1002_1004  POP_JUMP_IF_FALSE  1094  'to 1094'
             1006  LOAD_FAST                'i'
             1008  LOAD_FAST                'n'
             1010  COMPARE_OP               <
         1012_1014  POP_JUMP_IF_FALSE  1094  'to 1094'
             1016  LOAD_FAST                'self'
             1018  LOAD_ATTR                cdata_elem
         1020_1022  POP_JUMP_IF_TRUE   1094  'to 1094'

 L. 246      1024  LOAD_FAST                'self'
             1026  LOAD_ATTR                convert_charrefs
         1028_1030  POP_JUMP_IF_FALSE  1064  'to 1064'
             1032  LOAD_FAST                'self'
             1034  LOAD_ATTR                cdata_elem
         1036_1038  POP_JUMP_IF_TRUE   1064  'to 1064'

 L. 247      1040  LOAD_FAST                'self'
             1042  LOAD_METHOD              handle_data
             1044  LOAD_GLOBAL              unescape
             1046  LOAD_FAST                'rawdata'
             1048  LOAD_FAST                'i'
             1050  LOAD_FAST                'n'
             1052  BUILD_SLICE_2         2 
             1054  BINARY_SUBSCR    
             1056  CALL_FUNCTION_1       1  ''
             1058  CALL_METHOD_1         1  ''
             1060  POP_TOP          
             1062  JUMP_FORWARD       1082  'to 1082'
           1064_0  COME_FROM          1036  '1036'
           1064_1  COME_FROM          1028  '1028'

 L. 249      1064  LOAD_FAST                'self'
             1066  LOAD_METHOD              handle_data
             1068  LOAD_FAST                'rawdata'
             1070  LOAD_FAST                'i'
             1072  LOAD_FAST                'n'
             1074  BUILD_SLICE_2         2 
             1076  BINARY_SUBSCR    
             1078  CALL_METHOD_1         1  ''
             1080  POP_TOP          
           1082_0  COME_FROM          1062  '1062'

 L. 250      1082  LOAD_FAST                'self'
             1084  LOAD_METHOD              updatepos
             1086  LOAD_FAST                'i'
             1088  LOAD_FAST                'n'
             1090  CALL_METHOD_2         2  ''
             1092  STORE_FAST               'i'
           1094_0  COME_FROM          1020  '1020'
           1094_1  COME_FROM          1012  '1012'
           1094_2  COME_FROM          1002  '1002'

 L. 251      1094  LOAD_FAST                'rawdata'
             1096  LOAD_FAST                'i'
             1098  LOAD_CONST               None
             1100  BUILD_SLICE_2         2 
             1102  BINARY_SUBSCR    
             1104  LOAD_FAST                'self'
             1106  STORE_ATTR               rawdata

Parse error at or near `COME_FROM' instruction at offset 752_0

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
        while True:
            if k < endpos:
                m = attrfind_tolerant.match(rawdata, k)
                if not m:
                    pass
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