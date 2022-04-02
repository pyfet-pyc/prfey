# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: html\parser.py
"""A parser for HTML and XHTML."""
import re, _markupbase
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

 L. 134         0  LOAD_FAST                'self'
                2  LOAD_ATTR                rawdata
                4  STORE_FAST               'rawdata'

 L. 135         6  LOAD_CONST               0
                8  STORE_FAST               'i'

 L. 136        10  LOAD_GLOBAL              len
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

 L. 137        18  LOAD_FAST                'i'
               20  LOAD_FAST                'n'
               22  COMPARE_OP               <
            24_26  POP_JUMP_IF_FALSE  1000  'to 1000'

 L. 138        28  LOAD_FAST                'self'
               30  LOAD_ATTR                convert_charrefs
               32  POP_JUMP_IF_FALSE   118  'to 118'
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                cdata_elem
               38  POP_JUMP_IF_TRUE    118  'to 118'

 L. 139        40  LOAD_FAST                'rawdata'
               42  LOAD_METHOD              find
               44  LOAD_STR                 '<'
               46  LOAD_FAST                'i'
               48  CALL_METHOD_2         2  ''
               50  STORE_FAST               'j'

 L. 140        52  LOAD_FAST                'j'
               54  LOAD_CONST               0
               56  COMPARE_OP               <
               58  POP_JUMP_IF_FALSE   160  'to 160'

 L. 147        60  LOAD_FAST                'rawdata'
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

 L. 148        82  LOAD_FAST                'amppos'
               84  LOAD_CONST               0
               86  COMPARE_OP               >=
               88  POP_JUMP_IF_FALSE   112  'to 112'

 L. 149        90  LOAD_GLOBAL              re
               92  LOAD_METHOD              compile
               94  LOAD_STR                 '[\\s;]'
               96  CALL_METHOD_1         1  ''
               98  LOAD_METHOD              search
              100  LOAD_FAST                'rawdata'
              102  LOAD_FAST                'amppos'
              104  CALL_METHOD_2         2  ''

 L. 148       106  POP_JUMP_IF_TRUE    112  'to 112'

 L. 150   108_110  BREAK_LOOP         1000  'to 1000'
            112_0  COME_FROM           106  '106'
            112_1  COME_FROM            88  '88'

 L. 151       112  LOAD_FAST                'n'
              114  STORE_FAST               'j'
              116  JUMP_FORWARD        160  'to 160'
            118_0  COME_FROM            38  '38'
            118_1  COME_FROM            32  '32'

 L. 153       118  LOAD_FAST                'self'
              120  LOAD_ATTR                interesting
              122  LOAD_METHOD              search
              124  LOAD_FAST                'rawdata'
              126  LOAD_FAST                'i'
              128  CALL_METHOD_2         2  ''
              130  STORE_FAST               'match'

 L. 154       132  LOAD_FAST                'match'
              134  POP_JUMP_IF_FALSE   146  'to 146'

 L. 155       136  LOAD_FAST                'match'
              138  LOAD_METHOD              start
              140  CALL_METHOD_0         0  ''
              142  STORE_FAST               'j'
              144  JUMP_FORWARD        160  'to 160'
            146_0  COME_FROM           134  '134'

 L. 157       146  LOAD_FAST                'self'
              148  LOAD_ATTR                cdata_elem
              150  POP_JUMP_IF_FALSE   156  'to 156'

 L. 158   152_154  JUMP_FORWARD       1000  'to 1000'
            156_0  COME_FROM           150  '150'

 L. 159       156  LOAD_FAST                'n'
              158  STORE_FAST               'j'
            160_0  COME_FROM           144  '144'
            160_1  COME_FROM           116  '116'
            160_2  COME_FROM            58  '58'

 L. 160       160  LOAD_FAST                'i'
              162  LOAD_FAST                'j'
              164  COMPARE_OP               <
              166  POP_JUMP_IF_FALSE   222  'to 222'

 L. 161       168  LOAD_FAST                'self'
              170  LOAD_ATTR                convert_charrefs
              172  POP_JUMP_IF_FALSE   204  'to 204'
              174  LOAD_FAST                'self'
              176  LOAD_ATTR                cdata_elem
              178  POP_JUMP_IF_TRUE    204  'to 204'

 L. 162       180  LOAD_FAST                'self'
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

 L. 164       204  LOAD_FAST                'self'
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

 L. 165       222  LOAD_FAST                'self'
              224  LOAD_METHOD              updatepos
              226  LOAD_FAST                'i'
              228  LOAD_FAST                'j'
              230  CALL_METHOD_2         2  ''
              232  STORE_FAST               'i'

 L. 166       234  LOAD_FAST                'i'
              236  LOAD_FAST                'n'
              238  COMPARE_OP               ==
              240  POP_JUMP_IF_FALSE   246  'to 246'
          242_244  JUMP_FORWARD       1000  'to 1000'
            246_0  COME_FROM           240  '240'

 L. 167       246  LOAD_FAST                'rawdata'
              248  LOAD_ATTR                startswith
              250  STORE_FAST               'startswith'

 L. 168       252  LOAD_FAST                'startswith'
              254  LOAD_STR                 '<'
              256  LOAD_FAST                'i'
              258  CALL_FUNCTION_2       2  ''
          260_262  POP_JUMP_IF_FALSE   586  'to 586'

 L. 169       264  LOAD_GLOBAL              starttagopen
              266  LOAD_METHOD              match
              268  LOAD_FAST                'rawdata'
              270  LOAD_FAST                'i'
              272  CALL_METHOD_2         2  ''
          274_276  POP_JUMP_IF_FALSE   290  'to 290'

 L. 170       278  LOAD_FAST                'self'
              280  LOAD_METHOD              parse_starttag
              282  LOAD_FAST                'i'
              284  CALL_METHOD_1         1  ''
              286  STORE_FAST               'k'
              288  JUMP_FORWARD        424  'to 424'
            290_0  COME_FROM           274  '274'

 L. 171       290  LOAD_FAST                'startswith'
              292  LOAD_STR                 '</'
              294  LOAD_FAST                'i'
              296  CALL_FUNCTION_2       2  ''
          298_300  POP_JUMP_IF_FALSE   314  'to 314'

 L. 172       302  LOAD_FAST                'self'
              304  LOAD_METHOD              parse_endtag
              306  LOAD_FAST                'i'
              308  CALL_METHOD_1         1  ''
              310  STORE_FAST               'k'
              312  JUMP_FORWARD        424  'to 424'
            314_0  COME_FROM           298  '298'

 L. 173       314  LOAD_FAST                'startswith'
              316  LOAD_STR                 '<!--'
              318  LOAD_FAST                'i'
              320  CALL_FUNCTION_2       2  ''
          322_324  POP_JUMP_IF_FALSE   338  'to 338'

 L. 174       326  LOAD_FAST                'self'
              328  LOAD_METHOD              parse_comment
              330  LOAD_FAST                'i'
              332  CALL_METHOD_1         1  ''
              334  STORE_FAST               'k'
              336  JUMP_FORWARD        424  'to 424'
            338_0  COME_FROM           322  '322'

 L. 175       338  LOAD_FAST                'startswith'
              340  LOAD_STR                 '<?'
              342  LOAD_FAST                'i'
              344  CALL_FUNCTION_2       2  ''
          346_348  POP_JUMP_IF_FALSE   362  'to 362'

 L. 176       350  LOAD_FAST                'self'
              352  LOAD_METHOD              parse_pi
              354  LOAD_FAST                'i'
              356  CALL_METHOD_1         1  ''
              358  STORE_FAST               'k'
              360  JUMP_FORWARD        424  'to 424'
            362_0  COME_FROM           346  '346'

 L. 177       362  LOAD_FAST                'startswith'
              364  LOAD_STR                 '<!'
              366  LOAD_FAST                'i'
              368  CALL_FUNCTION_2       2  ''
          370_372  POP_JUMP_IF_FALSE   386  'to 386'

 L. 178       374  LOAD_FAST                'self'
              376  LOAD_METHOD              parse_html_declaration
              378  LOAD_FAST                'i'
              380  CALL_METHOD_1         1  ''
              382  STORE_FAST               'k'
              384  JUMP_FORWARD        424  'to 424'
            386_0  COME_FROM           370  '370'

 L. 179       386  LOAD_FAST                'i'
              388  LOAD_CONST               1
              390  BINARY_ADD       
              392  LOAD_FAST                'n'
              394  COMPARE_OP               <
          396_398  POP_JUMP_IF_FALSE  1000  'to 1000'

 L. 180       400  LOAD_FAST                'self'
              402  LOAD_METHOD              handle_data
              404  LOAD_STR                 '<'
              406  CALL_METHOD_1         1  ''
              408  POP_TOP          

 L. 181       410  LOAD_FAST                'i'
              412  LOAD_CONST               1
              414  BINARY_ADD       
              416  STORE_FAST               'k'
              418  JUMP_FORWARD        424  'to 424'

 L. 183   420_422  JUMP_FORWARD       1000  'to 1000'
            424_0  COME_FROM           418  '418'
            424_1  COME_FROM           384  '384'
            424_2  COME_FROM           360  '360'
            424_3  COME_FROM           336  '336'
            424_4  COME_FROM           312  '312'
            424_5  COME_FROM           288  '288'

 L. 184       424  LOAD_FAST                'k'
              426  LOAD_CONST               0
              428  COMPARE_OP               <
          430_432  POP_JUMP_IF_FALSE   572  'to 572'

 L. 185       434  LOAD_FAST                'end'
          436_438  POP_JUMP_IF_TRUE    444  'to 444'

 L. 186   440_442  JUMP_FORWARD       1000  'to 1000'
            444_0  COME_FROM           436  '436'

 L. 187       444  LOAD_FAST                'rawdata'
              446  LOAD_METHOD              find
              448  LOAD_STR                 '>'
              450  LOAD_FAST                'i'
              452  LOAD_CONST               1
              454  BINARY_ADD       
              456  CALL_METHOD_2         2  ''
              458  STORE_FAST               'k'

 L. 188       460  LOAD_FAST                'k'
              462  LOAD_CONST               0
              464  COMPARE_OP               <
          466_468  POP_JUMP_IF_FALSE   506  'to 506'

 L. 189       470  LOAD_FAST                'rawdata'
              472  LOAD_METHOD              find
              474  LOAD_STR                 '<'
              476  LOAD_FAST                'i'
              478  LOAD_CONST               1
              480  BINARY_ADD       
              482  CALL_METHOD_2         2  ''
              484  STORE_FAST               'k'

 L. 190       486  LOAD_FAST                'k'
              488  LOAD_CONST               0
              490  COMPARE_OP               <
          492_494  POP_JUMP_IF_FALSE   514  'to 514'

 L. 191       496  LOAD_FAST                'i'
              498  LOAD_CONST               1
              500  BINARY_ADD       
              502  STORE_FAST               'k'
              504  JUMP_FORWARD        514  'to 514'
            506_0  COME_FROM           466  '466'

 L. 193       506  LOAD_FAST                'k'
              508  LOAD_CONST               1
              510  INPLACE_ADD      
              512  STORE_FAST               'k'
            514_0  COME_FROM           504  '504'
            514_1  COME_FROM           492  '492'

 L. 194       514  LOAD_FAST                'self'
              516  LOAD_ATTR                convert_charrefs
          518_520  POP_JUMP_IF_FALSE   554  'to 554'
              522  LOAD_FAST                'self'
              524  LOAD_ATTR                cdata_elem
          526_528  POP_JUMP_IF_TRUE    554  'to 554'

 L. 195       530  LOAD_FAST                'self'
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

 L. 197       554  LOAD_FAST                'self'
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

 L. 198       572  LOAD_FAST                'self'
              574  LOAD_METHOD              updatepos
              576  LOAD_FAST                'i'
              578  LOAD_FAST                'k'
              580  CALL_METHOD_2         2  ''
              582  STORE_FAST               'i'
              584  JUMP_BACK            18  'to 18'
            586_0  COME_FROM           260  '260'

 L. 199       586  LOAD_FAST                'startswith'
              588  LOAD_STR                 '&#'
              590  LOAD_FAST                'i'
              592  CALL_FUNCTION_2       2  ''
          594_596  POP_JUMP_IF_FALSE   752  'to 752'

 L. 200       598  LOAD_GLOBAL              charref
              600  LOAD_METHOD              match
              602  LOAD_FAST                'rawdata'
              604  LOAD_FAST                'i'
              606  CALL_METHOD_2         2  ''
              608  STORE_FAST               'match'

 L. 201       610  LOAD_FAST                'match'
          612_614  POP_JUMP_IF_FALSE   690  'to 690'

 L. 202       616  LOAD_FAST                'match'
              618  LOAD_METHOD              group
              620  CALL_METHOD_0         0  ''
              622  LOAD_CONST               2
              624  LOAD_CONST               -1
              626  BUILD_SLICE_2         2 
              628  BINARY_SUBSCR    
              630  STORE_FAST               'name'

 L. 203       632  LOAD_FAST                'self'
              634  LOAD_METHOD              handle_charref
              636  LOAD_FAST                'name'
              638  CALL_METHOD_1         1  ''
              640  POP_TOP          

 L. 204       642  LOAD_FAST                'match'
              644  LOAD_METHOD              end
              646  CALL_METHOD_0         0  ''
              648  STORE_FAST               'k'

 L. 205       650  LOAD_FAST                'startswith'
              652  LOAD_STR                 ';'
              654  LOAD_FAST                'k'
              656  LOAD_CONST               1
              658  BINARY_SUBTRACT  
              660  CALL_FUNCTION_2       2  ''
          662_664  POP_JUMP_IF_TRUE    674  'to 674'

 L. 206       666  LOAD_FAST                'k'
              668  LOAD_CONST               1
              670  BINARY_SUBTRACT  
              672  STORE_FAST               'k'
            674_0  COME_FROM           662  '662'

 L. 207       674  LOAD_FAST                'self'
              676  LOAD_METHOD              updatepos
              678  LOAD_FAST                'i'
              680  LOAD_FAST                'k'
              682  CALL_METHOD_2         2  ''
              684  STORE_FAST               'i'

 L. 208       686  JUMP_BACK            18  'to 18'
              688  BREAK_LOOP          750  'to 750'
            690_0  COME_FROM           612  '612'

 L. 210       690  LOAD_STR                 ';'
              692  LOAD_FAST                'rawdata'
              694  LOAD_FAST                'i'
              696  LOAD_CONST               None
              698  BUILD_SLICE_2         2 
              700  BINARY_SUBSCR    
              702  <118>                 0  ''
          704_706  POP_JUMP_IF_FALSE  1000  'to 1000'

 L. 211       708  LOAD_FAST                'self'
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

 L. 212       730  LOAD_FAST                'self'
              732  LOAD_METHOD              updatepos
              734  LOAD_FAST                'i'
              736  LOAD_FAST                'i'
              738  LOAD_CONST               2
              740  BINARY_ADD       
              742  CALL_METHOD_2         2  ''
              744  STORE_FAST               'i'

 L. 213   746_748  JUMP_FORWARD       1000  'to 1000'
            750_0  COME_FROM           688  '688'
              750  JUMP_BACK            18  'to 18'
            752_0  COME_FROM           594  '594'

 L. 214       752  LOAD_FAST                'startswith'
              754  LOAD_STR                 '&'
              756  LOAD_FAST                'i'
              758  CALL_FUNCTION_2       2  ''
          760_762  POP_JUMP_IF_FALSE   986  'to 986'

 L. 215       764  LOAD_GLOBAL              entityref
              766  LOAD_METHOD              match
              768  LOAD_FAST                'rawdata'
              770  LOAD_FAST                'i'
              772  CALL_METHOD_2         2  ''
              774  STORE_FAST               'match'

 L. 216       776  LOAD_FAST                'match'
          778_780  POP_JUMP_IF_FALSE   848  'to 848'

 L. 217       782  LOAD_FAST                'match'
              784  LOAD_METHOD              group
              786  LOAD_CONST               1
              788  CALL_METHOD_1         1  ''
              790  STORE_FAST               'name'

 L. 218       792  LOAD_FAST                'self'
              794  LOAD_METHOD              handle_entityref
              796  LOAD_FAST                'name'
              798  CALL_METHOD_1         1  ''
              800  POP_TOP          

 L. 219       802  LOAD_FAST                'match'
              804  LOAD_METHOD              end
              806  CALL_METHOD_0         0  ''
              808  STORE_FAST               'k'

 L. 220       810  LOAD_FAST                'startswith'
              812  LOAD_STR                 ';'
              814  LOAD_FAST                'k'
              816  LOAD_CONST               1
              818  BINARY_SUBTRACT  
              820  CALL_FUNCTION_2       2  ''
          822_824  POP_JUMP_IF_TRUE    834  'to 834'

 L. 221       826  LOAD_FAST                'k'
              828  LOAD_CONST               1
              830  BINARY_SUBTRACT  
              832  STORE_FAST               'k'
            834_0  COME_FROM           822  '822'

 L. 222       834  LOAD_FAST                'self'
              836  LOAD_METHOD              updatepos
              838  LOAD_FAST                'i'
              840  LOAD_FAST                'k'
              842  CALL_METHOD_2         2  ''
              844  STORE_FAST               'i'

 L. 223       846  JUMP_BACK            18  'to 18'
            848_0  COME_FROM           778  '778'

 L. 224       848  LOAD_GLOBAL              incomplete
              850  LOAD_METHOD              match
              852  LOAD_FAST                'rawdata'
              854  LOAD_FAST                'i'
              856  CALL_METHOD_2         2  ''
              858  STORE_FAST               'match'

 L. 225       860  LOAD_FAST                'match'
          862_864  POP_JUMP_IF_FALSE   938  'to 938'

 L. 227       866  LOAD_FAST                'end'
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

 L. 228       894  LOAD_FAST                'match'
              896  LOAD_METHOD              end
              898  CALL_METHOD_0         0  ''
              900  STORE_FAST               'k'

 L. 229       902  LOAD_FAST                'k'
              904  LOAD_FAST                'i'
              906  COMPARE_OP               <=
          908_910  POP_JUMP_IF_FALSE   916  'to 916'

 L. 230       912  LOAD_FAST                'n'
              914  STORE_FAST               'k'
            916_0  COME_FROM           908  '908'

 L. 231       916  LOAD_FAST                'self'
              918  LOAD_METHOD              updatepos
              920  LOAD_FAST                'i'
              922  LOAD_FAST                'i'
              924  LOAD_CONST               1
              926  BINARY_ADD       
              928  CALL_METHOD_2         2  ''
              930  STORE_FAST               'i'

 L. 233   932_934  JUMP_FORWARD       1000  'to 1000'
              936  BREAK_LOOP          984  'to 984'
            938_0  COME_FROM           862  '862'

 L. 234       938  LOAD_FAST                'i'
              940  LOAD_CONST               1
              942  BINARY_ADD       
              944  LOAD_FAST                'n'
              946  COMPARE_OP               <
          948_950  POP_JUMP_IF_FALSE  1000  'to 1000'

 L. 237       952  LOAD_FAST                'self'
              954  LOAD_METHOD              handle_data
              956  LOAD_STR                 '&'
              958  CALL_METHOD_1         1  ''
              960  POP_TOP          

 L. 238       962  LOAD_FAST                'self'
              964  LOAD_METHOD              updatepos
              966  LOAD_FAST                'i'
              968  LOAD_FAST                'i'
              970  LOAD_CONST               1
              972  BINARY_ADD       
              974  CALL_METHOD_2         2  ''
              976  STORE_FAST               'i'
              978  JUMP_FORWARD        984  'to 984'

 L. 240   980_982  JUMP_FORWARD       1000  'to 1000'
            984_0  COME_FROM           978  '978'
            984_1  COME_FROM           936  '936'
              984  JUMP_BACK            18  'to 18'
            986_0  COME_FROM           760  '760'

 L. 242       986  LOAD_CONST               0
              988  POP_JUMP_IF_TRUE_BACK    18  'to 18'
              990  <74>             
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

 L. 244      1000  LOAD_FAST                'end'
         1002_1004  POP_JUMP_IF_FALSE  1094  'to 1094'
             1006  LOAD_FAST                'i'
             1008  LOAD_FAST                'n'
             1010  COMPARE_OP               <
         1012_1014  POP_JUMP_IF_FALSE  1094  'to 1094'
             1016  LOAD_FAST                'self'
             1018  LOAD_ATTR                cdata_elem
         1020_1022  POP_JUMP_IF_TRUE   1094  'to 1094'

 L. 245      1024  LOAD_FAST                'self'
             1026  LOAD_ATTR                convert_charrefs
         1028_1030  POP_JUMP_IF_FALSE  1064  'to 1064'
             1032  LOAD_FAST                'self'
             1034  LOAD_ATTR                cdata_elem
         1036_1038  POP_JUMP_IF_TRUE   1064  'to 1064'

 L. 246      1040  LOAD_FAST                'self'
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

 L. 248      1064  LOAD_FAST                'self'
             1066  LOAD_METHOD              handle_data
             1068  LOAD_FAST                'rawdata'
             1070  LOAD_FAST                'i'
             1072  LOAD_FAST                'n'
             1074  BUILD_SLICE_2         2 
             1076  BINARY_SUBSCR    
             1078  CALL_METHOD_1         1  ''
             1080  POP_TOP          
           1082_0  COME_FROM          1062  '1062'

 L. 249      1082  LOAD_FAST                'self'
             1084  LOAD_METHOD              updatepos
             1086  LOAD_FAST                'i'
             1088  LOAD_FAST                'n'
             1090  CALL_METHOD_2         2  ''
             1092  STORE_FAST               'i'
           1094_0  COME_FROM          1020  '1020'
           1094_1  COME_FROM          1012  '1012'
           1094_2  COME_FROM          1002  '1002'

 L. 250      1094  LOAD_FAST                'rawdata'
             1096  LOAD_FAST                'i'
             1098  LOAD_CONST               None
             1100  BUILD_SLICE_2         2 
             1102  BINARY_SUBSCR    
             1104  LOAD_FAST                'self'
             1106  STORE_ATTR               rawdata

Parse error at or near `<118>' instruction at offset 702

    def parse_html_declaration--- This code section failed: ---

 L. 256         0  LOAD_FAST                'self'
                2  LOAD_ATTR                rawdata
                4  STORE_FAST               'rawdata'

 L. 257         6  LOAD_FAST                'rawdata'
                8  LOAD_FAST                'i'
               10  LOAD_FAST                'i'
               12  LOAD_CONST               2
               14  BINARY_ADD       
               16  BUILD_SLICE_2         2 
               18  BINARY_SUBSCR    
               20  LOAD_STR                 '<!'
               22  COMPARE_OP               ==
               24  POP_JUMP_IF_TRUE     34  'to 34'
               26  <74>             
               28  LOAD_STR                 'unexpected call to parse_html_declaration()'
               30  CALL_FUNCTION_1       1  ''
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            24  '24'

 L. 259        34  LOAD_FAST                'rawdata'
               36  LOAD_FAST                'i'
               38  LOAD_FAST                'i'
               40  LOAD_CONST               4
               42  BINARY_ADD       
               44  BUILD_SLICE_2         2 
               46  BINARY_SUBSCR    
               48  LOAD_STR                 '<!--'
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    64  'to 64'

 L. 261        54  LOAD_FAST                'self'
               56  LOAD_METHOD              parse_comment
               58  LOAD_FAST                'i'
               60  CALL_METHOD_1         1  ''
               62  RETURN_VALUE     
             64_0  COME_FROM            52  '52'

 L. 262        64  LOAD_FAST                'rawdata'
               66  LOAD_FAST                'i'
               68  LOAD_FAST                'i'
               70  LOAD_CONST               3
               72  BINARY_ADD       
               74  BUILD_SLICE_2         2 
               76  BINARY_SUBSCR    
               78  LOAD_STR                 '<!['
               80  COMPARE_OP               ==
               82  POP_JUMP_IF_FALSE    94  'to 94'

 L. 263        84  LOAD_FAST                'self'
               86  LOAD_METHOD              parse_marked_section
               88  LOAD_FAST                'i'
               90  CALL_METHOD_1         1  ''
               92  RETURN_VALUE     
             94_0  COME_FROM            82  '82'

 L. 264        94  LOAD_FAST                'rawdata'
               96  LOAD_FAST                'i'
               98  LOAD_FAST                'i'
              100  LOAD_CONST               9
              102  BINARY_ADD       
              104  BUILD_SLICE_2         2 
              106  BINARY_SUBSCR    
              108  LOAD_METHOD              lower
              110  CALL_METHOD_0         0  ''
              112  LOAD_STR                 '<!doctype'
              114  COMPARE_OP               ==
              116  POP_JUMP_IF_FALSE   176  'to 176'

 L. 266       118  LOAD_FAST                'rawdata'
              120  LOAD_METHOD              find
              122  LOAD_STR                 '>'
              124  LOAD_FAST                'i'
              126  LOAD_CONST               9
              128  BINARY_ADD       
              130  CALL_METHOD_2         2  ''
              132  STORE_FAST               'gtpos'

 L. 267       134  LOAD_FAST                'gtpos'
              136  LOAD_CONST               -1
              138  COMPARE_OP               ==
              140  POP_JUMP_IF_FALSE   146  'to 146'

 L. 268       142  LOAD_CONST               -1
              144  RETURN_VALUE     
            146_0  COME_FROM           140  '140'

 L. 269       146  LOAD_FAST                'self'
              148  LOAD_METHOD              handle_decl
              150  LOAD_FAST                'rawdata'
              152  LOAD_FAST                'i'
              154  LOAD_CONST               2
              156  BINARY_ADD       
              158  LOAD_FAST                'gtpos'
              160  BUILD_SLICE_2         2 
              162  BINARY_SUBSCR    
              164  CALL_METHOD_1         1  ''
              166  POP_TOP          

 L. 270       168  LOAD_FAST                'gtpos'
              170  LOAD_CONST               1
              172  BINARY_ADD       
              174  RETURN_VALUE     
            176_0  COME_FROM           116  '116'

 L. 272       176  LOAD_FAST                'self'
              178  LOAD_METHOD              parse_bogus_comment
              180  LOAD_FAST                'i'
              182  CALL_METHOD_1         1  ''
              184  RETURN_VALUE     

Parse error at or near `<74>' instruction at offset 26

    def parse_bogus_comment--- This code section failed: ---

 L. 277         0  LOAD_FAST                'self'
                2  LOAD_ATTR                rawdata
                4  STORE_FAST               'rawdata'

 L. 278         6  LOAD_FAST                'rawdata'
                8  LOAD_FAST                'i'
               10  LOAD_FAST                'i'
               12  LOAD_CONST               2
               14  BINARY_ADD       
               16  BUILD_SLICE_2         2 
               18  BINARY_SUBSCR    
               20  LOAD_CONST               ('<!', '</')
               22  <118>                 0  ''
               24  POP_JUMP_IF_TRUE     34  'to 34'
               26  <74>             
               28  LOAD_STR                 'unexpected call to parse_comment()'
               30  CALL_FUNCTION_1       1  ''
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            24  '24'

 L. 280        34  LOAD_FAST                'rawdata'
               36  LOAD_METHOD              find
               38  LOAD_STR                 '>'
               40  LOAD_FAST                'i'
               42  LOAD_CONST               2
               44  BINARY_ADD       
               46  CALL_METHOD_2         2  ''
               48  STORE_FAST               'pos'

 L. 281        50  LOAD_FAST                'pos'
               52  LOAD_CONST               -1
               54  COMPARE_OP               ==
               56  POP_JUMP_IF_FALSE    62  'to 62'

 L. 282        58  LOAD_CONST               -1
               60  RETURN_VALUE     
             62_0  COME_FROM            56  '56'

 L. 283        62  LOAD_FAST                'report'
               64  POP_JUMP_IF_FALSE    88  'to 88'

 L. 284        66  LOAD_FAST                'self'
               68  LOAD_METHOD              handle_comment
               70  LOAD_FAST                'rawdata'
               72  LOAD_FAST                'i'
               74  LOAD_CONST               2
               76  BINARY_ADD       
               78  LOAD_FAST                'pos'
               80  BUILD_SLICE_2         2 
               82  BINARY_SUBSCR    
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          
             88_0  COME_FROM            64  '64'

 L. 285        88  LOAD_FAST                'pos'
               90  LOAD_CONST               1
               92  BINARY_ADD       
               94  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 22

    def parse_pi--- This code section failed: ---

 L. 289         0  LOAD_FAST                'self'
                2  LOAD_ATTR                rawdata
                4  STORE_FAST               'rawdata'

 L. 290         6  LOAD_FAST                'rawdata'
                8  LOAD_FAST                'i'
               10  LOAD_FAST                'i'
               12  LOAD_CONST               2
               14  BINARY_ADD       
               16  BUILD_SLICE_2         2 
               18  BINARY_SUBSCR    
               20  LOAD_STR                 '<?'
               22  COMPARE_OP               ==
               24  POP_JUMP_IF_TRUE     34  'to 34'
               26  <74>             
               28  LOAD_STR                 'unexpected call to parse_pi()'
               30  CALL_FUNCTION_1       1  ''
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            24  '24'

 L. 291        34  LOAD_GLOBAL              piclose
               36  LOAD_METHOD              search
               38  LOAD_FAST                'rawdata'
               40  LOAD_FAST                'i'
               42  LOAD_CONST               2
               44  BINARY_ADD       
               46  CALL_METHOD_2         2  ''
               48  STORE_FAST               'match'

 L. 292        50  LOAD_FAST                'match'
               52  POP_JUMP_IF_TRUE     58  'to 58'

 L. 293        54  LOAD_CONST               -1
               56  RETURN_VALUE     
             58_0  COME_FROM            52  '52'

 L. 294        58  LOAD_FAST                'match'
               60  LOAD_METHOD              start
               62  CALL_METHOD_0         0  ''
               64  STORE_FAST               'j'

 L. 295        66  LOAD_FAST                'self'
               68  LOAD_METHOD              handle_pi
               70  LOAD_FAST                'rawdata'
               72  LOAD_FAST                'i'
               74  LOAD_CONST               2
               76  BINARY_ADD       
               78  LOAD_FAST                'j'
               80  BUILD_SLICE_2         2 
               82  BINARY_SUBSCR    
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          

 L. 296        88  LOAD_FAST                'match'
               90  LOAD_METHOD              end
               92  CALL_METHOD_0         0  ''
               94  STORE_FAST               'j'

 L. 297        96  LOAD_FAST                'j'
               98  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 26

    def parse_starttag--- This code section failed: ---

 L. 301         0  LOAD_CONST               None
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _HTMLParser__starttag_text

 L. 302         6  LOAD_FAST                'self'
                8  LOAD_METHOD              check_for_whole_start_tag
               10  LOAD_FAST                'i'
               12  CALL_METHOD_1         1  ''
               14  STORE_FAST               'endpos'

 L. 303        16  LOAD_FAST                'endpos'
               18  LOAD_CONST               0
               20  COMPARE_OP               <
               22  POP_JUMP_IF_FALSE    28  'to 28'

 L. 304        24  LOAD_FAST                'endpos'
               26  RETURN_VALUE     
             28_0  COME_FROM            22  '22'

 L. 305        28  LOAD_FAST                'self'
               30  LOAD_ATTR                rawdata
               32  STORE_FAST               'rawdata'

 L. 306        34  LOAD_FAST                'rawdata'
               36  LOAD_FAST                'i'
               38  LOAD_FAST                'endpos'
               40  BUILD_SLICE_2         2 
               42  BINARY_SUBSCR    
               44  LOAD_FAST                'self'
               46  STORE_ATTR               _HTMLParser__starttag_text

 L. 309        48  BUILD_LIST_0          0 
               50  STORE_FAST               'attrs'

 L. 310        52  LOAD_GLOBAL              tagfind_tolerant
               54  LOAD_METHOD              match
               56  LOAD_FAST                'rawdata'
               58  LOAD_FAST                'i'
               60  LOAD_CONST               1
               62  BINARY_ADD       
               64  CALL_METHOD_2         2  ''
               66  STORE_FAST               'match'

 L. 311        68  LOAD_FAST                'match'
               70  POP_JUMP_IF_TRUE     80  'to 80'
               72  <74>             
               74  LOAD_STR                 'unexpected call to parse_starttag()'
               76  CALL_FUNCTION_1       1  ''
               78  RAISE_VARARGS_1       1  'exception instance'
             80_0  COME_FROM            70  '70'

 L. 312        80  LOAD_FAST                'match'
               82  LOAD_METHOD              end
               84  CALL_METHOD_0         0  ''
               86  STORE_FAST               'k'

 L. 313        88  LOAD_FAST                'match'
               90  LOAD_METHOD              group
               92  LOAD_CONST               1
               94  CALL_METHOD_1         1  ''
               96  LOAD_METHOD              lower
               98  CALL_METHOD_0         0  ''
              100  DUP_TOP          
              102  LOAD_FAST                'self'
              104  STORE_ATTR               lasttag
              106  STORE_FAST               'tag'
            108_0  COME_FROM           300  '300'

 L. 314       108  LOAD_FAST                'k'
              110  LOAD_FAST                'endpos'
              112  COMPARE_OP               <
          114_116  POP_JUMP_IF_FALSE   302  'to 302'

 L. 315       118  LOAD_GLOBAL              attrfind_tolerant
              120  LOAD_METHOD              match
              122  LOAD_FAST                'rawdata'
              124  LOAD_FAST                'k'
              126  CALL_METHOD_2         2  ''
              128  STORE_FAST               'm'

 L. 316       130  LOAD_FAST                'm'
              132  POP_JUMP_IF_TRUE    138  'to 138'

 L. 317   134_136  JUMP_FORWARD        302  'to 302'
            138_0  COME_FROM           132  '132'

 L. 318       138  LOAD_FAST                'm'
              140  LOAD_METHOD              group
              142  LOAD_CONST               1
              144  LOAD_CONST               2
              146  LOAD_CONST               3
              148  CALL_METHOD_3         3  ''
              150  UNPACK_SEQUENCE_3     3 
              152  STORE_FAST               'attrname'
              154  STORE_FAST               'rest'
              156  STORE_FAST               'attrvalue'

 L. 319       158  LOAD_FAST                'rest'
              160  POP_JUMP_IF_TRUE    168  'to 168'

 L. 320       162  LOAD_CONST               None
              164  STORE_FAST               'attrvalue'
              166  JUMP_FORWARD        260  'to 260'
            168_0  COME_FROM           160  '160'

 L. 321       168  LOAD_FAST                'attrvalue'
              170  LOAD_CONST               None
              172  LOAD_CONST               1
              174  BUILD_SLICE_2         2 
              176  BINARY_SUBSCR    
              178  LOAD_STR                 "'"
              180  DUP_TOP          
              182  ROT_THREE        
              184  COMPARE_OP               ==
              186  POP_JUMP_IF_FALSE   204  'to 204'
              188  LOAD_FAST                'attrvalue'
              190  LOAD_CONST               -1
              192  LOAD_CONST               None
              194  BUILD_SLICE_2         2 
              196  BINARY_SUBSCR    
              198  COMPARE_OP               ==
              200  POP_JUMP_IF_TRUE    248  'to 248'
              202  JUMP_FORWARD        206  'to 206'
            204_0  COME_FROM           186  '186'
              204  POP_TOP          
            206_0  COME_FROM           202  '202'

 L. 322       206  LOAD_FAST                'attrvalue'
              208  LOAD_CONST               None
              210  LOAD_CONST               1
              212  BUILD_SLICE_2         2 
              214  BINARY_SUBSCR    
              216  LOAD_STR                 '"'

 L. 321       218  DUP_TOP          
              220  ROT_THREE        
              222  COMPARE_OP               ==
              224  POP_JUMP_IF_FALSE   244  'to 244'

 L. 322       226  LOAD_FAST                'attrvalue'
              228  LOAD_CONST               -1
              230  LOAD_CONST               None
              232  BUILD_SLICE_2         2 
              234  BINARY_SUBSCR    

 L. 321       236  COMPARE_OP               ==
          238_240  POP_JUMP_IF_FALSE   260  'to 260'
              242  JUMP_FORWARD        248  'to 248'
            244_0  COME_FROM           224  '224'
              244  POP_TOP          
              246  JUMP_FORWARD        260  'to 260'
            248_0  COME_FROM           242  '242'
            248_1  COME_FROM           200  '200'

 L. 323       248  LOAD_FAST                'attrvalue'
              250  LOAD_CONST               1
              252  LOAD_CONST               -1
              254  BUILD_SLICE_2         2 
              256  BINARY_SUBSCR    
              258  STORE_FAST               'attrvalue'
            260_0  COME_FROM           246  '246'
            260_1  COME_FROM           238  '238'
            260_2  COME_FROM           166  '166'

 L. 324       260  LOAD_FAST                'attrvalue'
          262_264  POP_JUMP_IF_FALSE   274  'to 274'

 L. 325       266  LOAD_GLOBAL              unescape
              268  LOAD_FAST                'attrvalue'
              270  CALL_FUNCTION_1       1  ''
              272  STORE_FAST               'attrvalue'
            274_0  COME_FROM           262  '262'

 L. 326       274  LOAD_FAST                'attrs'
              276  LOAD_METHOD              append
              278  LOAD_FAST                'attrname'
              280  LOAD_METHOD              lower
              282  CALL_METHOD_0         0  ''
              284  LOAD_FAST                'attrvalue'
              286  BUILD_TUPLE_2         2 
              288  CALL_METHOD_1         1  ''
              290  POP_TOP          

 L. 327       292  LOAD_FAST                'm'
              294  LOAD_METHOD              end
              296  CALL_METHOD_0         0  ''
              298  STORE_FAST               'k'
              300  JUMP_BACK           108  'to 108'
            302_0  COME_FROM           134  '134'
            302_1  COME_FROM           114  '114'

 L. 329       302  LOAD_FAST                'rawdata'
              304  LOAD_FAST                'k'
              306  LOAD_FAST                'endpos'
              308  BUILD_SLICE_2         2 
              310  BINARY_SUBSCR    
              312  LOAD_METHOD              strip
              314  CALL_METHOD_0         0  ''
              316  STORE_FAST               'end'

 L. 330       318  LOAD_FAST                'end'
              320  LOAD_CONST               ('>', '/>')
              322  <118>                 1  ''
          324_326  POP_JUMP_IF_FALSE   428  'to 428'

 L. 331       328  LOAD_FAST                'self'
              330  LOAD_METHOD              getpos
              332  CALL_METHOD_0         0  ''
              334  UNPACK_SEQUENCE_2     2 
              336  STORE_FAST               'lineno'
              338  STORE_FAST               'offset'

 L. 332       340  LOAD_STR                 '\n'
              342  LOAD_FAST                'self'
              344  LOAD_ATTR                _HTMLParser__starttag_text
              346  <118>                 0  ''
          348_350  POP_JUMP_IF_FALSE   392  'to 392'

 L. 333       352  LOAD_FAST                'lineno'
              354  LOAD_FAST                'self'
              356  LOAD_ATTR                _HTMLParser__starttag_text
              358  LOAD_METHOD              count
              360  LOAD_STR                 '\n'
              362  CALL_METHOD_1         1  ''
              364  BINARY_ADD       
              366  STORE_FAST               'lineno'

 L. 334       368  LOAD_GLOBAL              len
              370  LOAD_FAST                'self'
              372  LOAD_ATTR                _HTMLParser__starttag_text
              374  CALL_FUNCTION_1       1  ''

 L. 335       376  LOAD_FAST                'self'
              378  LOAD_ATTR                _HTMLParser__starttag_text
              380  LOAD_METHOD              rfind
              382  LOAD_STR                 '\n'
              384  CALL_METHOD_1         1  ''

 L. 334       386  BINARY_SUBTRACT  
              388  STORE_FAST               'offset'
              390  JUMP_FORWARD        406  'to 406'
            392_0  COME_FROM           348  '348'

 L. 337       392  LOAD_FAST                'offset'
              394  LOAD_GLOBAL              len
              396  LOAD_FAST                'self'
              398  LOAD_ATTR                _HTMLParser__starttag_text
              400  CALL_FUNCTION_1       1  ''
              402  BINARY_ADD       
              404  STORE_FAST               'offset'
            406_0  COME_FROM           390  '390'

 L. 338       406  LOAD_FAST                'self'
              408  LOAD_METHOD              handle_data
              410  LOAD_FAST                'rawdata'
              412  LOAD_FAST                'i'
              414  LOAD_FAST                'endpos'
              416  BUILD_SLICE_2         2 
              418  BINARY_SUBSCR    
              420  CALL_METHOD_1         1  ''
              422  POP_TOP          

 L. 339       424  LOAD_FAST                'endpos'
              426  RETURN_VALUE     
            428_0  COME_FROM           324  '324'

 L. 340       428  LOAD_FAST                'end'
              430  LOAD_METHOD              endswith
              432  LOAD_STR                 '/>'
              434  CALL_METHOD_1         1  ''
          436_438  POP_JUMP_IF_FALSE   454  'to 454'

 L. 342       440  LOAD_FAST                'self'
              442  LOAD_METHOD              handle_startendtag
              444  LOAD_FAST                'tag'
              446  LOAD_FAST                'attrs'
              448  CALL_METHOD_2         2  ''
              450  POP_TOP          
              452  JUMP_FORWARD        488  'to 488'
            454_0  COME_FROM           436  '436'

 L. 344       454  LOAD_FAST                'self'
              456  LOAD_METHOD              handle_starttag
              458  LOAD_FAST                'tag'
              460  LOAD_FAST                'attrs'
              462  CALL_METHOD_2         2  ''
              464  POP_TOP          

 L. 345       466  LOAD_FAST                'tag'
              468  LOAD_FAST                'self'
              470  LOAD_ATTR                CDATA_CONTENT_ELEMENTS
              472  <118>                 0  ''
          474_476  POP_JUMP_IF_FALSE   488  'to 488'

 L. 346       478  LOAD_FAST                'self'
              480  LOAD_METHOD              set_cdata_mode
              482  LOAD_FAST                'tag'
              484  CALL_METHOD_1         1  ''
              486  POP_TOP          
            488_0  COME_FROM           474  '474'
            488_1  COME_FROM           452  '452'

 L. 347       488  LOAD_FAST                'endpos'
              490  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 72

    def check_for_whole_start_tag--- This code section failed: ---

 L. 352         0  LOAD_FAST                'self'
                2  LOAD_ATTR                rawdata
                4  STORE_FAST               'rawdata'

 L. 353         6  LOAD_GLOBAL              locatestarttagend_tolerant
                8  LOAD_METHOD              match
               10  LOAD_FAST                'rawdata'
               12  LOAD_FAST                'i'
               14  CALL_METHOD_2         2  ''
               16  STORE_FAST               'm'

 L. 354        18  LOAD_FAST                'm'
               20  POP_JUMP_IF_FALSE   170  'to 170'

 L. 355        22  LOAD_FAST                'm'
               24  LOAD_METHOD              end
               26  CALL_METHOD_0         0  ''
               28  STORE_FAST               'j'

 L. 356        30  LOAD_FAST                'rawdata'
               32  LOAD_FAST                'j'
               34  LOAD_FAST                'j'
               36  LOAD_CONST               1
               38  BINARY_ADD       
               40  BUILD_SLICE_2         2 
               42  BINARY_SUBSCR    
               44  STORE_FAST               'next'

 L. 357        46  LOAD_FAST                'next'
               48  LOAD_STR                 '>'
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L. 358        54  LOAD_FAST                'j'
               56  LOAD_CONST               1
               58  BINARY_ADD       
               60  RETURN_VALUE     
             62_0  COME_FROM            52  '52'

 L. 359        62  LOAD_FAST                'next'
               64  LOAD_STR                 '/'
               66  COMPARE_OP               ==
               68  POP_JUMP_IF_FALSE   126  'to 126'

 L. 360        70  LOAD_FAST                'rawdata'
               72  LOAD_METHOD              startswith
               74  LOAD_STR                 '/>'
               76  LOAD_FAST                'j'
               78  CALL_METHOD_2         2  ''
               80  POP_JUMP_IF_FALSE    90  'to 90'

 L. 361        82  LOAD_FAST                'j'
               84  LOAD_CONST               2
               86  BINARY_ADD       
               88  RETURN_VALUE     
             90_0  COME_FROM            80  '80'

 L. 362        90  LOAD_FAST                'rawdata'
               92  LOAD_METHOD              startswith
               94  LOAD_STR                 '/'
               96  LOAD_FAST                'j'
               98  CALL_METHOD_2         2  ''
              100  POP_JUMP_IF_FALSE   106  'to 106'

 L. 364       102  LOAD_CONST               -1
              104  RETURN_VALUE     
            106_0  COME_FROM           100  '100'

 L. 366       106  LOAD_FAST                'j'
              108  LOAD_FAST                'i'
              110  COMPARE_OP               >
              112  POP_JUMP_IF_FALSE   118  'to 118'

 L. 367       114  LOAD_FAST                'j'
              116  RETURN_VALUE     
            118_0  COME_FROM           112  '112'

 L. 369       118  LOAD_FAST                'i'
              120  LOAD_CONST               1
              122  BINARY_ADD       
              124  RETURN_VALUE     
            126_0  COME_FROM            68  '68'

 L. 370       126  LOAD_FAST                'next'
              128  LOAD_STR                 ''
              130  COMPARE_OP               ==
              132  POP_JUMP_IF_FALSE   138  'to 138'

 L. 372       134  LOAD_CONST               -1
              136  RETURN_VALUE     
            138_0  COME_FROM           132  '132'

 L. 373       138  LOAD_FAST                'next'
              140  LOAD_STR                 'abcdefghijklmnopqrstuvwxyz=/ABCDEFGHIJKLMNOPQRSTUVWXYZ'
              142  <118>                 0  ''
              144  POP_JUMP_IF_FALSE   150  'to 150'

 L. 377       146  LOAD_CONST               -1
              148  RETURN_VALUE     
            150_0  COME_FROM           144  '144'

 L. 378       150  LOAD_FAST                'j'
              152  LOAD_FAST                'i'
              154  COMPARE_OP               >
              156  POP_JUMP_IF_FALSE   162  'to 162'

 L. 379       158  LOAD_FAST                'j'
              160  RETURN_VALUE     
            162_0  COME_FROM           156  '156'

 L. 381       162  LOAD_FAST                'i'
              164  LOAD_CONST               1
              166  BINARY_ADD       
              168  RETURN_VALUE     
            170_0  COME_FROM            20  '20'

 L. 382       170  LOAD_GLOBAL              AssertionError
              172  LOAD_STR                 'we should not get here!'
              174  CALL_FUNCTION_1       1  ''
              176  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<118>' instruction at offset 142

    def parse_endtag--- This code section failed: ---

 L. 386         0  LOAD_FAST                'self'
                2  LOAD_ATTR                rawdata
                4  STORE_FAST               'rawdata'

 L. 387         6  LOAD_FAST                'rawdata'
                8  LOAD_FAST                'i'
               10  LOAD_FAST                'i'
               12  LOAD_CONST               2
               14  BINARY_ADD       
               16  BUILD_SLICE_2         2 
               18  BINARY_SUBSCR    
               20  LOAD_STR                 '</'
               22  COMPARE_OP               ==
               24  POP_JUMP_IF_TRUE     34  'to 34'
               26  <74>             
               28  LOAD_STR                 'unexpected call to parse_endtag'
               30  CALL_FUNCTION_1       1  ''
               32  RAISE_VARARGS_1       1  'exception instance'
             34_0  COME_FROM            24  '24'

 L. 388        34  LOAD_GLOBAL              endendtag
               36  LOAD_METHOD              search
               38  LOAD_FAST                'rawdata'
               40  LOAD_FAST                'i'
               42  LOAD_CONST               1
               44  BINARY_ADD       
               46  CALL_METHOD_2         2  ''
               48  STORE_FAST               'match'

 L. 389        50  LOAD_FAST                'match'
               52  POP_JUMP_IF_TRUE     58  'to 58'

 L. 390        54  LOAD_CONST               -1
               56  RETURN_VALUE     
             58_0  COME_FROM            52  '52'

 L. 391        58  LOAD_FAST                'match'
               60  LOAD_METHOD              end
               62  CALL_METHOD_0         0  ''
               64  STORE_FAST               'gtpos'

 L. 392        66  LOAD_GLOBAL              endtagfind
               68  LOAD_METHOD              match
               70  LOAD_FAST                'rawdata'
               72  LOAD_FAST                'i'
               74  CALL_METHOD_2         2  ''
               76  STORE_FAST               'match'

 L. 393        78  LOAD_FAST                'match'
               80  POP_JUMP_IF_TRUE    220  'to 220'

 L. 394        82  LOAD_FAST                'self'
               84  LOAD_ATTR                cdata_elem
               86  LOAD_CONST               None
               88  <117>                 1  ''
               90  POP_JUMP_IF_FALSE   114  'to 114'

 L. 395        92  LOAD_FAST                'self'
               94  LOAD_METHOD              handle_data
               96  LOAD_FAST                'rawdata'
               98  LOAD_FAST                'i'
              100  LOAD_FAST                'gtpos'
              102  BUILD_SLICE_2         2 
              104  BINARY_SUBSCR    
              106  CALL_METHOD_1         1  ''
              108  POP_TOP          

 L. 396       110  LOAD_FAST                'gtpos'
              112  RETURN_VALUE     
            114_0  COME_FROM            90  '90'

 L. 398       114  LOAD_GLOBAL              tagfind_tolerant
              116  LOAD_METHOD              match
              118  LOAD_FAST                'rawdata'
              120  LOAD_FAST                'i'
              122  LOAD_CONST               2
              124  BINARY_ADD       
              126  CALL_METHOD_2         2  ''
              128  STORE_FAST               'namematch'

 L. 399       130  LOAD_FAST                'namematch'
              132  POP_JUMP_IF_TRUE    172  'to 172'

 L. 401       134  LOAD_FAST                'rawdata'
              136  LOAD_FAST                'i'
              138  LOAD_FAST                'i'
              140  LOAD_CONST               3
              142  BINARY_ADD       
              144  BUILD_SLICE_2         2 
              146  BINARY_SUBSCR    
              148  LOAD_STR                 '</>'
              150  COMPARE_OP               ==
              152  POP_JUMP_IF_FALSE   162  'to 162'

 L. 402       154  LOAD_FAST                'i'
              156  LOAD_CONST               3
              158  BINARY_ADD       
              160  RETURN_VALUE     
            162_0  COME_FROM           152  '152'

 L. 404       162  LOAD_FAST                'self'
              164  LOAD_METHOD              parse_bogus_comment
              166  LOAD_FAST                'i'
              168  CALL_METHOD_1         1  ''
              170  RETURN_VALUE     
            172_0  COME_FROM           132  '132'

 L. 405       172  LOAD_FAST                'namematch'
              174  LOAD_METHOD              group
              176  LOAD_CONST               1
              178  CALL_METHOD_1         1  ''
              180  LOAD_METHOD              lower
              182  CALL_METHOD_0         0  ''
              184  STORE_FAST               'tagname'

 L. 410       186  LOAD_FAST                'rawdata'
              188  LOAD_METHOD              find
              190  LOAD_STR                 '>'
              192  LOAD_FAST                'namematch'
              194  LOAD_METHOD              end
              196  CALL_METHOD_0         0  ''
              198  CALL_METHOD_2         2  ''
              200  STORE_FAST               'gtpos'

 L. 411       202  LOAD_FAST                'self'
              204  LOAD_METHOD              handle_endtag
              206  LOAD_FAST                'tagname'
              208  CALL_METHOD_1         1  ''
              210  POP_TOP          

 L. 412       212  LOAD_FAST                'gtpos'
              214  LOAD_CONST               1
              216  BINARY_ADD       
              218  RETURN_VALUE     
            220_0  COME_FROM            80  '80'

 L. 414       220  LOAD_FAST                'match'
              222  LOAD_METHOD              group
              224  LOAD_CONST               1
              226  CALL_METHOD_1         1  ''
              228  LOAD_METHOD              lower
              230  CALL_METHOD_0         0  ''
              232  STORE_FAST               'elem'

 L. 415       234  LOAD_FAST                'self'
              236  LOAD_ATTR                cdata_elem
              238  LOAD_CONST               None
              240  <117>                 1  ''
          242_244  POP_JUMP_IF_FALSE   280  'to 280'

 L. 416       246  LOAD_FAST                'elem'
              248  LOAD_FAST                'self'
              250  LOAD_ATTR                cdata_elem
              252  COMPARE_OP               !=
          254_256  POP_JUMP_IF_FALSE   280  'to 280'

 L. 417       258  LOAD_FAST                'self'
              260  LOAD_METHOD              handle_data
              262  LOAD_FAST                'rawdata'
              264  LOAD_FAST                'i'
              266  LOAD_FAST                'gtpos'
              268  BUILD_SLICE_2         2 
              270  BINARY_SUBSCR    
              272  CALL_METHOD_1         1  ''
              274  POP_TOP          

 L. 418       276  LOAD_FAST                'gtpos'
              278  RETURN_VALUE     
            280_0  COME_FROM           254  '254'
            280_1  COME_FROM           242  '242'

 L. 420       280  LOAD_FAST                'self'
              282  LOAD_METHOD              handle_endtag
              284  LOAD_FAST                'elem'
              286  CALL_METHOD_1         1  ''
              288  POP_TOP          

 L. 421       290  LOAD_FAST                'self'
              292  LOAD_METHOD              clear_cdata_mode
              294  CALL_METHOD_0         0  ''
              296  POP_TOP          

 L. 422       298  LOAD_FAST                'gtpos'
              300  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 26

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