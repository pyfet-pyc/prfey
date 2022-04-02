# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: xml\dom\pulldom.py
import xml.sax, xml.sax.handler
START_ELEMENT = 'START_ELEMENT'
END_ELEMENT = 'END_ELEMENT'
COMMENT = 'COMMENT'
START_DOCUMENT = 'START_DOCUMENT'
END_DOCUMENT = 'END_DOCUMENT'
PROCESSING_INSTRUCTION = 'PROCESSING_INSTRUCTION'
IGNORABLE_WHITESPACE = 'IGNORABLE_WHITESPACE'
CHARACTERS = 'CHARACTERS'

class PullDOM(xml.sax.ContentHandler):
    _locator = None
    document = None

    def __init__--- This code section failed: ---

 L.  18         0  LOAD_CONST               0
                2  LOAD_CONST               ('XML_NAMESPACE',)
                4  IMPORT_NAME_ATTR         xml.dom
                6  IMPORT_FROM              XML_NAMESPACE
                8  STORE_FAST               'XML_NAMESPACE'
               10  POP_TOP          

 L.  19        12  LOAD_FAST                'documentFactory'
               14  LOAD_FAST                'self'
               16  STORE_ATTR               documentFactory

 L.  20        18  LOAD_CONST               None
               20  LOAD_CONST               None
               22  BUILD_LIST_2          2 
               24  LOAD_FAST                'self'
               26  STORE_ATTR               firstEvent

 L.  21        28  LOAD_FAST                'self'
               30  LOAD_ATTR                firstEvent
               32  LOAD_FAST                'self'
               34  STORE_ATTR               lastEvent

 L.  22        36  BUILD_LIST_0          0 
               38  LOAD_FAST                'self'
               40  STORE_ATTR               elementStack

 L.  23        42  LOAD_FAST                'self'
               44  LOAD_ATTR                elementStack
               46  LOAD_ATTR                append
               48  LOAD_FAST                'self'
               50  STORE_ATTR               push

 L.  24        52  SETUP_FINALLY        68  'to 68'

 L.  25        54  LOAD_FAST                'self'
               56  LOAD_ATTR                elementStack
               58  LOAD_ATTR                pop
               60  LOAD_FAST                'self'
               62  STORE_ATTR               pop
               64  POP_BLOCK        
               66  JUMP_FORWARD         86  'to 86'
             68_0  COME_FROM_FINALLY    52  '52'

 L.  26        68  DUP_TOP          
               70  LOAD_GLOBAL              AttributeError
               72  <121>                84  ''
               74  POP_TOP          
               76  POP_TOP          
               78  POP_TOP          

 L.  28        80  POP_EXCEPT       
               82  JUMP_FORWARD         86  'to 86'
               84  <48>             
             86_0  COME_FROM            82  '82'
             86_1  COME_FROM            66  '66'

 L.  29        86  LOAD_FAST                'XML_NAMESPACE'
               88  LOAD_STR                 'xml'
               90  BUILD_MAP_1           1 
               92  BUILD_LIST_1          1 
               94  LOAD_FAST                'self'
               96  STORE_ATTR               _ns_contexts

 L.  30        98  LOAD_FAST                'self'
              100  LOAD_ATTR                _ns_contexts
              102  LOAD_CONST               -1
              104  BINARY_SUBSCR    
              106  LOAD_FAST                'self'
              108  STORE_ATTR               _current_context

 L.  31       110  BUILD_LIST_0          0 
              112  LOAD_FAST                'self'
              114  STORE_ATTR               pending_events

Parse error at or near `<121>' instruction at offset 72

    def pop(self):
        result = self.elementStack[(-1)]
        del self.elementStack[-1]
        return result

    def setDocumentLocator(self, locator):
        self._locator = locator

    def startPrefixMapping(self, prefix, uri):
        if not hasattr(self, '_xmlns_attrs'):
            self._xmlns_attrs = []
        self._xmlns_attrs.append((prefix or 'xmlns', uri))
        self._ns_contexts.append(self._current_context.copy())
        self._current_context[uri] = prefix or None

    def endPrefixMapping(self, prefix):
        self._current_context = self._ns_contexts.pop()

    def startElementNS--- This code section failed: ---

 L.  53         0  LOAD_STR                 'http://www.w3.org/2000/xmlns/'
                2  STORE_FAST               'xmlns_uri'

 L.  54         4  LOAD_GLOBAL              getattr
                6  LOAD_FAST                'self'
                8  LOAD_STR                 '_xmlns_attrs'
               10  LOAD_CONST               None
               12  CALL_FUNCTION_3       3  ''
               14  STORE_FAST               'xmlns_attrs'

 L.  55        16  LOAD_FAST                'xmlns_attrs'
               18  LOAD_CONST               None
               20  <117>                 1  ''
               22  POP_JUMP_IF_FALSE    58  'to 58'

 L.  56        24  LOAD_FAST                'xmlns_attrs'
               26  GET_ITER         
               28  FOR_ITER             52  'to 52'
               30  UNPACK_SEQUENCE_2     2 
               32  STORE_FAST               'aname'
               34  STORE_FAST               'value'

 L.  57        36  LOAD_FAST                'value'
               38  LOAD_FAST                'attrs'
               40  LOAD_ATTR                _attrs
               42  LOAD_FAST                'xmlns_uri'
               44  LOAD_FAST                'aname'
               46  BUILD_TUPLE_2         2 
               48  STORE_SUBSCR     
               50  JUMP_BACK            28  'to 28'

 L.  58        52  BUILD_LIST_0          0 
               54  LOAD_FAST                'self'
               56  STORE_ATTR               _xmlns_attrs
             58_0  COME_FROM            22  '22'

 L.  59        58  LOAD_FAST                'name'
               60  UNPACK_SEQUENCE_2     2 
               62  STORE_FAST               'uri'
               64  STORE_FAST               'localname'

 L.  60        66  LOAD_FAST                'uri'
               68  POP_JUMP_IF_FALSE   146  'to 146'

 L.  64        70  LOAD_FAST                'tagName'
               72  LOAD_CONST               None
               74  <117>                 0  ''
               76  POP_JUMP_IF_FALSE   110  'to 110'

 L.  65        78  LOAD_FAST                'self'
               80  LOAD_ATTR                _current_context
               82  LOAD_FAST                'uri'
               84  BINARY_SUBSCR    
               86  STORE_FAST               'prefix'

 L.  66        88  LOAD_FAST                'prefix'
               90  POP_JUMP_IF_FALSE   106  'to 106'

 L.  67        92  LOAD_FAST                'prefix'
               94  LOAD_STR                 ':'
               96  BINARY_ADD       
               98  LOAD_FAST                'localname'
              100  BINARY_ADD       
              102  STORE_FAST               'tagName'
              104  JUMP_FORWARD        110  'to 110'
            106_0  COME_FROM            90  '90'

 L.  69       106  LOAD_FAST                'localname'
              108  STORE_FAST               'tagName'
            110_0  COME_FROM           104  '104'
            110_1  COME_FROM            76  '76'

 L.  70       110  LOAD_FAST                'self'
              112  LOAD_ATTR                document
              114  POP_JUMP_IF_FALSE   132  'to 132'

 L.  71       116  LOAD_FAST                'self'
              118  LOAD_ATTR                document
              120  LOAD_METHOD              createElementNS
              122  LOAD_FAST                'uri'
              124  LOAD_FAST                'tagName'
              126  CALL_METHOD_2         2  ''
              128  STORE_FAST               'node'
              130  JUMP_ABSOLUTE       178  'to 178'
            132_0  COME_FROM           114  '114'

 L.  73       132  LOAD_FAST                'self'
              134  LOAD_METHOD              buildDocument
              136  LOAD_FAST                'uri'
              138  LOAD_FAST                'tagName'
              140  CALL_METHOD_2         2  ''
              142  STORE_FAST               'node'
              144  JUMP_FORWARD        178  'to 178'
            146_0  COME_FROM            68  '68'

 L.  77       146  LOAD_FAST                'self'
              148  LOAD_ATTR                document
              150  POP_JUMP_IF_FALSE   166  'to 166'

 L.  78       152  LOAD_FAST                'self'
              154  LOAD_ATTR                document
              156  LOAD_METHOD              createElement
              158  LOAD_FAST                'localname'
              160  CALL_METHOD_1         1  ''
              162  STORE_FAST               'node'
              164  JUMP_FORWARD        178  'to 178'
            166_0  COME_FROM           150  '150'

 L.  80       166  LOAD_FAST                'self'
              168  LOAD_METHOD              buildDocument
              170  LOAD_CONST               None
              172  LOAD_FAST                'localname'
              174  CALL_METHOD_2         2  ''
              176  STORE_FAST               'node'
            178_0  COME_FROM           164  '164'
            178_1  COME_FROM           144  '144'

 L.  82       178  LOAD_FAST                'attrs'
              180  LOAD_METHOD              items
              182  CALL_METHOD_0         0  ''
              184  GET_ITER         
              186  FOR_ITER            356  'to 356'
              188  UNPACK_SEQUENCE_2     2 
              190  STORE_FAST               'aname'
              192  STORE_FAST               'value'

 L.  83       194  LOAD_FAST                'aname'
              196  UNPACK_SEQUENCE_2     2 
              198  STORE_FAST               'a_uri'
              200  STORE_FAST               'a_localname'

 L.  84       202  LOAD_FAST                'a_uri'
              204  LOAD_FAST                'xmlns_uri'
              206  COMPARE_OP               ==
          208_210  POP_JUMP_IF_FALSE   260  'to 260'

 L.  85       212  LOAD_FAST                'a_localname'
              214  LOAD_STR                 'xmlns'
              216  COMPARE_OP               ==
              218  POP_JUMP_IF_FALSE   226  'to 226'

 L.  86       220  LOAD_FAST                'a_localname'
              222  STORE_FAST               'qname'
              224  JUMP_FORWARD        234  'to 234'
            226_0  COME_FROM           218  '218'

 L.  88       226  LOAD_STR                 'xmlns:'
              228  LOAD_FAST                'a_localname'
              230  BINARY_ADD       
              232  STORE_FAST               'qname'
            234_0  COME_FROM           224  '224'

 L.  89       234  LOAD_FAST                'self'
              236  LOAD_ATTR                document
              238  LOAD_METHOD              createAttributeNS
              240  LOAD_FAST                'a_uri'
              242  LOAD_FAST                'qname'
              244  CALL_METHOD_2         2  ''
              246  STORE_FAST               'attr'

 L.  90       248  LOAD_FAST                'node'
              250  LOAD_METHOD              setAttributeNodeNS
              252  LOAD_FAST                'attr'
              254  CALL_METHOD_1         1  ''
              256  POP_TOP          
              258  JUMP_FORWARD        348  'to 348'
            260_0  COME_FROM           208  '208'

 L.  91       260  LOAD_FAST                'a_uri'
          262_264  POP_JUMP_IF_FALSE   326  'to 326'

 L.  92       266  LOAD_FAST                'self'
              268  LOAD_ATTR                _current_context
              270  LOAD_FAST                'a_uri'
              272  BINARY_SUBSCR    
              274  STORE_FAST               'prefix'

 L.  93       276  LOAD_FAST                'prefix'
          278_280  POP_JUMP_IF_FALSE   296  'to 296'

 L.  94       282  LOAD_FAST                'prefix'
              284  LOAD_STR                 ':'
              286  BINARY_ADD       
              288  LOAD_FAST                'a_localname'
              290  BINARY_ADD       
              292  STORE_FAST               'qname'
              294  JUMP_FORWARD        300  'to 300'
            296_0  COME_FROM           278  '278'

 L.  96       296  LOAD_FAST                'a_localname'
              298  STORE_FAST               'qname'
            300_0  COME_FROM           294  '294'

 L.  97       300  LOAD_FAST                'self'
              302  LOAD_ATTR                document
              304  LOAD_METHOD              createAttributeNS
              306  LOAD_FAST                'a_uri'
              308  LOAD_FAST                'qname'
              310  CALL_METHOD_2         2  ''
              312  STORE_FAST               'attr'

 L.  98       314  LOAD_FAST                'node'
              316  LOAD_METHOD              setAttributeNodeNS
              318  LOAD_FAST                'attr'
              320  CALL_METHOD_1         1  ''
              322  POP_TOP          
              324  JUMP_FORWARD        348  'to 348'
            326_0  COME_FROM           262  '262'

 L. 100       326  LOAD_FAST                'self'
              328  LOAD_ATTR                document
              330  LOAD_METHOD              createAttribute
              332  LOAD_FAST                'a_localname'
              334  CALL_METHOD_1         1  ''
              336  STORE_FAST               'attr'

 L. 101       338  LOAD_FAST                'node'
              340  LOAD_METHOD              setAttributeNode
              342  LOAD_FAST                'attr'
              344  CALL_METHOD_1         1  ''
              346  POP_TOP          
            348_0  COME_FROM           324  '324'
            348_1  COME_FROM           258  '258'

 L. 102       348  LOAD_FAST                'value'
              350  LOAD_FAST                'attr'
              352  STORE_ATTR               value
              354  JUMP_BACK           186  'to 186'

 L. 104       356  LOAD_GLOBAL              START_ELEMENT
              358  LOAD_FAST                'node'
              360  BUILD_TUPLE_2         2 
              362  LOAD_CONST               None
              364  BUILD_LIST_2          2 
              366  LOAD_FAST                'self'
              368  LOAD_ATTR                lastEvent
              370  LOAD_CONST               1
              372  STORE_SUBSCR     

 L. 105       374  LOAD_FAST                'self'
              376  LOAD_ATTR                lastEvent
              378  LOAD_CONST               1
              380  BINARY_SUBSCR    
              382  LOAD_FAST                'self'
              384  STORE_ATTR               lastEvent

 L. 106       386  LOAD_FAST                'self'
              388  LOAD_METHOD              push
              390  LOAD_FAST                'node'
              392  CALL_METHOD_1         1  ''
              394  POP_TOP          

Parse error at or near `<117>' instruction at offset 20

    def endElementNS(self, name, tagName):
        self.lastEvent[1] = [
         (
          END_ELEMENT, self.pop()), None]
        self.lastEvent = self.lastEvent[1]

    def startElement(self, name, attrs):
        if self.document:
            node = self.document.createElement(name)
        else:
            node = self.buildDocumentNonename
        for aname, value in attrs.items():
            attr = self.document.createAttribute(aname)
            attr.value = value
            node.setAttributeNode(attr)
        else:
            self.lastEvent[1] = [
             (
              START_ELEMENT, node), None]
            self.lastEvent = self.lastEvent[1]
            self.push(node)

    def endElement(self, name):
        self.lastEvent[1] = [(END_ELEMENT, self.pop()), None]
        self.lastEvent = self.lastEvent[1]

    def comment(self, s):
        if self.document:
            node = self.document.createComment(s)
            self.lastEvent[1] = [(COMMENT, node), None]
            self.lastEvent = self.lastEvent[1]
        else:
            event = [
             (
              COMMENT, s), None]
            self.pending_events.append(event)

    def processingInstruction(self, target, data):
        if self.document:
            node = self.document.createProcessingInstructiontargetdata
            self.lastEvent[1] = [(PROCESSING_INSTRUCTION, node), None]
            self.lastEvent = self.lastEvent[1]
        else:
            event = [
             (
              PROCESSING_INSTRUCTION, target, data), None]
            self.pending_events.append(event)

    def ignorableWhitespace(self, chars):
        node = self.document.createTextNode(chars)
        self.lastEvent[1] = [(IGNORABLE_WHITESPACE, node), None]
        self.lastEvent = self.lastEvent[1]

    def characters(self, chars):
        node = self.document.createTextNode(chars)
        self.lastEvent[1] = [(CHARACTERS, node), None]
        self.lastEvent = self.lastEvent[1]

    def startDocument--- This code section failed: ---

 L. 160         0  LOAD_FAST                'self'
                2  LOAD_ATTR                documentFactory
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    32  'to 32'

 L. 161        10  LOAD_CONST               0
               12  LOAD_CONST               None
               14  IMPORT_NAME_ATTR         xml.dom.minidom
               16  STORE_FAST               'xml'

 L. 162        18  LOAD_FAST                'xml'
               20  LOAD_ATTR                dom
               22  LOAD_ATTR                minidom
               24  LOAD_ATTR                Document
               26  LOAD_ATTR                implementation
               28  LOAD_FAST                'self'
               30  STORE_ATTR               documentFactory
             32_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    def buildDocument(self, uri, tagname):
        node = self.documentFactory.createDocument(uri, tagname, None)
        self.document = node
        self.lastEvent[1] = [(START_DOCUMENT, node), None]
        self.lastEvent = self.lastEvent[1]
        self.push(node)
        for e in self.pending_events:
            if e[0][0] == PROCESSING_INSTRUCTION:
                _, target, data = e[0]
                n = self.document.createProcessingInstructiontargetdata
                e[0] = (PROCESSING_INSTRUCTION, n)
            else:
                if e[0][0] == COMMENT:
                    n = self.document.createComment(e[0][1])
                    e[0] = (COMMENT, n)
                else:
                    raise AssertionError('Unknown pending event ', e[0][0])
            self.lastEvent[1] = e
            self.lastEvent = e
        else:
            self.pending_events = None
            return node.firstChild

    def endDocument(self):
        self.lastEvent[1] = [(END_DOCUMENT, self.document), None]
        self.pop()

    def clear(self):
        """clear(): Explicitly release parsing structures"""
        self.document = None


class ErrorHandler:

    def warning(self, exception):
        print(exception)

    def error(self, exception):
        raise exception

    def fatalError(self, exception):
        raise exception


class DOMEventStream:

    def __init__(self, stream, parser, bufsize):
        self.stream = stream
        self.parser = parser
        self.bufsize = bufsize
        if not hasattr(self.parser, 'feed'):
            self.getEvent = self._slurp
        self.reset()

    def reset(self):
        self.pulldom = PullDOM()
        self.parser.setFeaturexml.sax.handler.feature_namespaces1
        self.parser.setContentHandler(self.pulldom)

    def __getitem__(self, pos):
        import warnings
        warnings.warn("DOMEventStream's __getitem__ method ignores 'pos' parameter. Use iterator protocol instead.",
          DeprecationWarning,
          stacklevel=2)
        rc = self.getEvent()
        if rc:
            return rc
        raise IndexError

    def __next__(self):
        rc = self.getEvent()
        if rc:
            return rc
        raise StopIteration

    def __iter__(self):
        return self

    def expandNode--- This code section failed: ---

 L. 242         0  LOAD_FAST                'self'
                2  LOAD_METHOD              getEvent
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'event'

 L. 243         8  LOAD_FAST                'node'
               10  BUILD_LIST_1          1 
               12  STORE_FAST               'parents'

 L. 244        14  LOAD_FAST                'event'
               16  POP_JUMP_IF_FALSE   104  'to 104'

 L. 245        18  LOAD_FAST                'event'
               20  UNPACK_SEQUENCE_2     2 
               22  STORE_FAST               'token'
               24  STORE_FAST               'cur_node'

 L. 246        26  LOAD_FAST                'cur_node'
               28  LOAD_FAST                'node'
               30  <117>                 0  ''
               32  POP_JUMP_IF_FALSE    38  'to 38'

 L. 247        34  LOAD_CONST               None
               36  RETURN_VALUE     
             38_0  COME_FROM            32  '32'

 L. 248        38  LOAD_FAST                'token'
               40  LOAD_GLOBAL              END_ELEMENT
               42  COMPARE_OP               !=
               44  POP_JUMP_IF_FALSE    60  'to 60'

 L. 249        46  LOAD_FAST                'parents'
               48  LOAD_CONST               -1
               50  BINARY_SUBSCR    
               52  LOAD_METHOD              appendChild
               54  LOAD_FAST                'cur_node'
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          
             60_0  COME_FROM            44  '44'

 L. 250        60  LOAD_FAST                'token'
               62  LOAD_GLOBAL              START_ELEMENT
               64  COMPARE_OP               ==
               66  POP_JUMP_IF_FALSE    80  'to 80'

 L. 251        68  LOAD_FAST                'parents'
               70  LOAD_METHOD              append
               72  LOAD_FAST                'cur_node'
               74  CALL_METHOD_1         1  ''
               76  POP_TOP          
               78  JUMP_FORWARD         94  'to 94'
             80_0  COME_FROM            66  '66'

 L. 252        80  LOAD_FAST                'token'
               82  LOAD_GLOBAL              END_ELEMENT
               84  COMPARE_OP               ==
               86  POP_JUMP_IF_FALSE    94  'to 94'

 L. 253        88  LOAD_FAST                'parents'
               90  LOAD_CONST               -1
               92  DELETE_SUBSCR    
             94_0  COME_FROM            86  '86'
             94_1  COME_FROM            78  '78'

 L. 254        94  LOAD_FAST                'self'
               96  LOAD_METHOD              getEvent
               98  CALL_METHOD_0         0  ''
              100  STORE_FAST               'event'
              102  JUMP_BACK            14  'to 14'
            104_0  COME_FROM            16  '16'

Parse error at or near `<117>' instruction at offset 30

    def getEvent(self):
        if not self.pulldom.firstEvent[1]:
            self.pulldom.lastEvent = self.pulldom.firstEvent
        else:
            while True:
                if not self.pulldom.firstEvent[1]:
                    buf = self.stream.read(self.bufsize)
                    if not buf:
                        self.parser.close()
                        return None
                    self.parser.feed(buf)

        rc = self.pulldom.firstEvent[1][0]
        self.pulldom.firstEvent[1] = self.pulldom.firstEvent[1][1]
        return rc

    def _slurp(self):
        """ Fallback replacement for getEvent() using the
            standard SAX2 interface, which means we slurp the
            SAX events into memory (no performance gain, but
            we are compatible to all SAX parsers).
        """
        self.parser.parse(self.stream)
        self.getEvent = self._emit
        return self._emit()

    def _emit(self):
        """ Fallback replacement for getEvent() that emits
            the events that _slurp() read previously.
        """
        rc = self.pulldom.firstEvent[1][0]
        self.pulldom.firstEvent[1] = self.pulldom.firstEvent[1][1]
        return rc

    def clear(self):
        """clear(): Explicitly release parsing objects"""
        self.pulldom.clear()
        del self.pulldom
        self.parser = None
        self.stream = None


class SAX2DOM(PullDOM):

    def startElementNS(self, name, tagName, attrs):
        PullDOM.startElementNS(self, name, tagName, attrs)
        curNode = self.elementStack[(-1)]
        parentNode = self.elementStack[(-2)]
        parentNode.appendChild(curNode)

    def startElement(self, name, attrs):
        PullDOM.startElement(self, name, attrs)
        curNode = self.elementStack[(-1)]
        parentNode = self.elementStack[(-2)]
        parentNode.appendChild(curNode)

    def processingInstruction(self, target, data):
        PullDOM.processingInstruction(self, target, data)
        node = self.lastEvent[0][1]
        parentNode = self.elementStack[(-1)]
        parentNode.appendChild(node)

    def ignorableWhitespace(self, chars):
        PullDOM.ignorableWhitespaceselfchars
        node = self.lastEvent[0][1]
        parentNode = self.elementStack[(-1)]
        parentNode.appendChild(node)

    def characters(self, chars):
        PullDOM.charactersselfchars
        node = self.lastEvent[0][1]
        parentNode = self.elementStack[(-1)]
        parentNode.appendChild(node)


default_bufsize = 16364

def parse--- This code section failed: ---

 L. 332         0  LOAD_FAST                'bufsize'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 333         8  LOAD_GLOBAL              default_bufsize
               10  STORE_FAST               'bufsize'
             12_0  COME_FROM             6  '6'

 L. 334        12  LOAD_GLOBAL              isinstance
               14  LOAD_FAST                'stream_or_string'
               16  LOAD_GLOBAL              str
               18  CALL_FUNCTION_2       2  ''
               20  POP_JUMP_IF_FALSE    34  'to 34'

 L. 335        22  LOAD_GLOBAL              open
               24  LOAD_FAST                'stream_or_string'
               26  LOAD_STR                 'rb'
               28  CALL_FUNCTION_2       2  ''
               30  STORE_FAST               'stream'
               32  JUMP_FORWARD         38  'to 38'
             34_0  COME_FROM            20  '20'

 L. 337        34  LOAD_FAST                'stream_or_string'
               36  STORE_FAST               'stream'
             38_0  COME_FROM            32  '32'

 L. 338        38  LOAD_FAST                'parser'
               40  POP_JUMP_IF_TRUE     52  'to 52'

 L. 339        42  LOAD_GLOBAL              xml
               44  LOAD_ATTR                sax
               46  LOAD_METHOD              make_parser
               48  CALL_METHOD_0         0  ''
               50  STORE_FAST               'parser'
             52_0  COME_FROM            40  '40'

 L. 340        52  LOAD_GLOBAL              DOMEventStream
               54  LOAD_FAST                'stream'
               56  LOAD_FAST                'parser'
               58  LOAD_FAST                'bufsize'
               60  CALL_FUNCTION_3       3  ''
               62  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def parseString(string, parser=None):
    from io import StringIO
    bufsize = len(string)
    buf = StringIO(string)
    if not parser:
        parser = xml.sax.make_parser()
    return DOMEventStream(buf, parser, bufsize)