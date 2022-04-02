# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: xml\sax\saxutils.py
"""A library of useful helper classes to the SAX classes, for the
convenience of application and driver writers.
"""
import os, urllib.parse, urllib.request, io, codecs
from . import handler
from . import xmlreader

def __dict_replace(s, d):
    """Replace substrings of a string using a dictionary."""
    for key, value in d.items():
        s = s.replace(key, value)
    else:
        return s


def escape(data, entities={}):
    """Escape &, <, and > in a string of data.

    You can escape other strings of data by passing a dictionary as
    the optional entities parameter.  The keys and values must all be
    strings; each key will be replaced with its corresponding value.
    """
    data = data.replace('&', '&amp;')
    data = data.replace('>', '&gt;')
    data = data.replace('<', '&lt;')
    if entities:
        data = __dict_replace(data, entities)
    return data


def unescape(data, entities={}):
    """Unescape &amp;, &lt;, and &gt; in a string of data.

    You can unescape other strings of data by passing a dictionary as
    the optional entities parameter.  The keys and values must all be
    strings; each key will be replaced with its corresponding value.
    """
    data = data.replace('&lt;', '<')
    data = data.replace('&gt;', '>')
    if entities:
        data = __dict_replace(data, entities)
    return data.replace('&amp;', '&')


def quoteattr--- This code section failed: ---

 L.  59         0  BUILD_MAP_0           0 
                2  LOAD_FAST                'entities'
                4  <165>                 1  ''
                6  LOAD_STR                 '&#10;'
                8  LOAD_STR                 '&#13;'
               10  LOAD_STR                 '&#9;'
               12  LOAD_CONST               ('\n', '\r', '\t')
               14  BUILD_CONST_KEY_MAP_3     3 
               16  <165>                 1  ''
               18  STORE_FAST               'entities'

 L.  60        20  LOAD_GLOBAL              escape
               22  LOAD_FAST                'data'
               24  LOAD_FAST                'entities'
               26  CALL_FUNCTION_2       2  ''
               28  STORE_FAST               'data'

 L.  61        30  LOAD_STR                 '"'
               32  LOAD_FAST                'data'
               34  <118>                 0  ''
               36  POP_JUMP_IF_FALSE    74  'to 74'

 L.  62        38  LOAD_STR                 "'"
               40  LOAD_FAST                'data'
               42  <118>                 0  ''
               44  POP_JUMP_IF_FALSE    64  'to 64'

 L.  63        46  LOAD_STR                 '"%s"'
               48  LOAD_FAST                'data'
               50  LOAD_METHOD              replace
               52  LOAD_STR                 '"'
               54  LOAD_STR                 '&quot;'
               56  CALL_METHOD_2         2  ''
               58  BINARY_MODULO    
               60  STORE_FAST               'data'
               62  JUMP_FORWARD         82  'to 82'
             64_0  COME_FROM            44  '44'

 L.  65        64  LOAD_STR                 "'%s'"
               66  LOAD_FAST                'data'
               68  BINARY_MODULO    
               70  STORE_FAST               'data'
               72  JUMP_FORWARD         82  'to 82'
             74_0  COME_FROM            36  '36'

 L.  67        74  LOAD_STR                 '"%s"'
               76  LOAD_FAST                'data'
               78  BINARY_MODULO    
               80  STORE_FAST               'data'
             82_0  COME_FROM            72  '72'
             82_1  COME_FROM            62  '62'

 L.  68        82  LOAD_FAST                'data'
               84  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def _gettextwriter--- This code section failed: ---

 L.  72         0  LOAD_DEREF               'out'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    22  'to 22'

 L.  73         8  LOAD_CONST               0
               10  LOAD_CONST               None
               12  IMPORT_NAME              sys
               14  STORE_FAST               'sys'

 L.  74        16  LOAD_FAST                'sys'
               18  LOAD_ATTR                stdout
               20  RETURN_VALUE     
             22_0  COME_FROM             6  '6'

 L.  76        22  LOAD_GLOBAL              isinstance
               24  LOAD_DEREF               'out'
               26  LOAD_GLOBAL              io
               28  LOAD_ATTR                TextIOBase
               30  CALL_FUNCTION_2       2  ''
               32  POP_JUMP_IF_FALSE    38  'to 38'

 L.  78        34  LOAD_DEREF               'out'
               36  RETURN_VALUE     
             38_0  COME_FROM            32  '32'

 L.  80        38  LOAD_GLOBAL              isinstance
               40  LOAD_DEREF               'out'
               42  LOAD_GLOBAL              codecs
               44  LOAD_ATTR                StreamWriter
               46  LOAD_GLOBAL              codecs
               48  LOAD_ATTR                StreamReaderWriter
               50  BUILD_TUPLE_2         2 
               52  CALL_FUNCTION_2       2  ''
               54  POP_JUMP_IF_FALSE    60  'to 60'

 L.  82        56  LOAD_DEREF               'out'
               58  RETURN_VALUE     
             60_0  COME_FROM            54  '54'

 L.  85        60  LOAD_GLOBAL              isinstance
               62  LOAD_DEREF               'out'
               64  LOAD_GLOBAL              io
               66  LOAD_ATTR                RawIOBase
               68  CALL_FUNCTION_2       2  ''
               70  POP_JUMP_IF_FALSE   108  'to 108'

 L.  88        72  LOAD_BUILD_CLASS 
               74  LOAD_CLOSURE             'out'
               76  BUILD_TUPLE_1         1 
               78  LOAD_CODE                <code_object _wrapper>
               80  LOAD_STR                 '_wrapper'
               82  MAKE_FUNCTION_8          'closure'
               84  LOAD_STR                 '_wrapper'
               86  CALL_FUNCTION_2       2  ''
               88  STORE_FAST               '_wrapper'

 L.  92        90  LOAD_FAST                '_wrapper'
               92  CALL_FUNCTION_0       0  ''
               94  STORE_FAST               'buffer'

 L.  93        96  LOAD_LAMBDA              '<code_object <lambda>>'
               98  LOAD_STR                 '_gettextwriter.<locals>.<lambda>'
              100  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              102  LOAD_FAST                'buffer'
              104  STORE_ATTR               close
              106  JUMP_FORWARD        174  'to 174'
            108_0  COME_FROM            70  '70'

 L.  97       108  LOAD_GLOBAL              io
              110  LOAD_METHOD              BufferedIOBase
              112  CALL_METHOD_0         0  ''
              114  STORE_FAST               'buffer'

 L.  98       116  LOAD_LAMBDA              '<code_object <lambda>>'
              118  LOAD_STR                 '_gettextwriter.<locals>.<lambda>'
              120  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              122  LOAD_FAST                'buffer'
              124  STORE_ATTR               writable

 L.  99       126  LOAD_DEREF               'out'
              128  LOAD_ATTR                write
              130  LOAD_FAST                'buffer'
              132  STORE_ATTR               write

 L. 100       134  SETUP_FINALLY       156  'to 156'

 L. 103       136  LOAD_DEREF               'out'
              138  LOAD_ATTR                seekable
              140  LOAD_FAST                'buffer'
              142  STORE_ATTR               seekable

 L. 104       144  LOAD_DEREF               'out'
              146  LOAD_ATTR                tell
              148  LOAD_FAST                'buffer'
              150  STORE_ATTR               tell
              152  POP_BLOCK        
              154  JUMP_FORWARD        174  'to 174'
            156_0  COME_FROM_FINALLY   134  '134'

 L. 105       156  DUP_TOP          
              158  LOAD_GLOBAL              AttributeError
              160  <121>               172  ''
              162  POP_TOP          
              164  POP_TOP          
              166  POP_TOP          

 L. 106       168  POP_EXCEPT       
              170  JUMP_FORWARD        174  'to 174'
              172  <48>             
            174_0  COME_FROM           170  '170'
            174_1  COME_FROM           154  '154'
            174_2  COME_FROM           106  '106'

 L. 107       174  LOAD_GLOBAL              io
              176  LOAD_ATTR                TextIOWrapper
              178  LOAD_FAST                'buffer'
              180  LOAD_FAST                'encoding'

 L. 108       182  LOAD_STR                 'xmlcharrefreplace'

 L. 109       184  LOAD_STR                 '\n'

 L. 110       186  LOAD_CONST               True

 L. 107       188  LOAD_CONST               ('encoding', 'errors', 'newline', 'write_through')
              190  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              192  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class XMLGenerator(handler.ContentHandler):

    def __init__(self, out=None, encoding='iso-8859-1', short_empty_elements=False):
        handler.ContentHandler.__init__(self)
        out = _gettextwriter(out, encoding)
        self._write = out.write
        self._flush = out.flush
        self._ns_contexts = [{}]
        self._current_context = self._ns_contexts[(-1)]
        self._undeclared_ns_maps = []
        self._encoding = encoding
        self._short_empty_elements = short_empty_elements
        self._pending_start_element = False

    def _qname(self, name):
        """Builds a qualified name from a (ns_url, localname) pair"""
        if name[0]:
            if 'http://www.w3.org/XML/1998/namespace' == name[0]:
                return 'xml:' + name[1]
            prefix = self._current_context[name[0]]
            if prefix:
                return prefix + ':' + name[1]
        return name[1]

    def _finish_pending_start_element(self, endElement=False):
        if self._pending_start_element:
            self._write('>')
            self._pending_start_element = False

    def startDocument(self):
        self._write('<?xml version="1.0" encoding="%s"?>\n' % self._encoding)

    def endDocument(self):
        self._flush()

    def startPrefixMapping(self, prefix, uri):
        self._ns_contexts.append(self._current_context.copy())
        self._current_context[uri] = prefix
        self._undeclared_ns_maps.append((prefix, uri))

    def endPrefixMapping(self, prefix):
        self._current_context = self._ns_contexts[(-1)]
        del self._ns_contexts[-1]

    def startElement(self, name, attrs):
        self._finish_pending_start_element()
        self._write('<' + name)
        for name, value in attrs.items():
            self._write(' %s=%s' % (name, quoteattr(value)))
        else:
            if self._short_empty_elements:
                self._pending_start_element = True
            else:
                self._write('>')

    def endElement(self, name):
        if self._pending_start_element:
            self._write('/>')
            self._pending_start_element = False
        else:
            self._write('</%s>' % name)

    def startElementNS(self, name, qname, attrs):
        self._finish_pending_start_element()
        self._write('<' + self._qname(name))
        for prefix, uri in self._undeclared_ns_maps:
            if prefix:
                self._write(' xmlns:%s="%s"' % (prefix, uri))
            else:
                self._write(' xmlns="%s"' % uri)
        else:
            self._undeclared_ns_maps = []
            for name, value in attrs.items():
                self._write(' %s=%s' % (self._qname(name), quoteattr(value)))
            else:
                if self._short_empty_elements:
                    self._pending_start_element = True
                else:
                    self._write('>')

    def endElementNS(self, name, qname):
        if self._pending_start_element:
            self._write('/>')
            self._pending_start_element = False
        else:
            self._write('</%s>' % self._qname(name))

    def characters(self, content):
        if content:
            self._finish_pending_start_element()
            if not isinstance(content, str):
                content = str(content, self._encoding)
            self._write(escape(content))

    def ignorableWhitespace(self, content):
        if content:
            self._finish_pending_start_element()
            if not isinstance(content, str):
                content = str(content, self._encoding)
            self._write(content)

    def processingInstruction(self, target, data):
        self._finish_pending_start_element()
        self._write('<?%s %s?>' % (target, data))


class XMLFilterBase(xmlreader.XMLReader):
    __doc__ = "This class is designed to sit between an XMLReader and the\n    client application's event handlers.  By default, it does nothing\n    but pass requests up to the reader and events on to the handlers\n    unmodified, but subclasses can override specific methods to modify\n    the event stream or the configuration requests as they pass\n    through."

    def __init__(self, parent=None):
        xmlreader.XMLReader.__init__(self)
        self._parent = parent

    def error(self, exception):
        self._err_handler.error(exception)

    def fatalError(self, exception):
        self._err_handler.fatalError(exception)

    def warning(self, exception):
        self._err_handler.warning(exception)

    def setDocumentLocator(self, locator):
        self._cont_handler.setDocumentLocator(locator)

    def startDocument(self):
        self._cont_handler.startDocument()

    def endDocument(self):
        self._cont_handler.endDocument()

    def startPrefixMapping(self, prefix, uri):
        self._cont_handler.startPrefixMapping(prefix, uri)

    def endPrefixMapping(self, prefix):
        self._cont_handler.endPrefixMapping(prefix)

    def startElement(self, name, attrs):
        self._cont_handler.startElement(name, attrs)

    def endElement(self, name):
        self._cont_handler.endElement(name)

    def startElementNS(self, name, qname, attrs):
        self._cont_handler.startElementNS(name, qname, attrs)

    def endElementNS(self, name, qname):
        self._cont_handler.endElementNS(name, qname)

    def characters(self, content):
        self._cont_handler.characters(content)

    def ignorableWhitespace(self, chars):
        self._cont_handler.ignorableWhitespace(chars)

    def processingInstruction(self, target, data):
        self._cont_handler.processingInstruction(target, data)

    def skippedEntity(self, name):
        self._cont_handler.skippedEntity(name)

    def notationDecl(self, name, publicId, systemId):
        self._dtd_handler.notationDecl(name, publicId, systemId)

    def unparsedEntityDecl(self, name, publicId, systemId, ndata):
        self._dtd_handler.unparsedEntityDecl(name, publicId, systemId, ndata)

    def resolveEntity(self, publicId, systemId):
        return self._ent_handler.resolveEntity(publicId, systemId)

    def parse(self, source):
        self._parent.setContentHandler(self)
        self._parent.setErrorHandler(self)
        self._parent.setEntityResolver(self)
        self._parent.setDTDHandler(self)
        self._parent.parse(source)

    def setLocale(self, locale):
        self._parent.setLocale(locale)

    def getFeature(self, name):
        return self._parent.getFeature(name)

    def setFeature(self, name, state):
        self._parent.setFeature(name, state)

    def getProperty(self, name):
        return self._parent.getProperty(name)

    def setProperty(self, name, value):
        self._parent.setProperty(name, value)

    def getParent(self):
        return self._parent

    def setParent(self, parent):
        self._parent = parent


def prepare_input_source--- This code section failed: ---

 L. 342         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'source'
                4  LOAD_GLOBAL              os
                6  LOAD_ATTR                PathLike
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_FALSE    22  'to 22'

 L. 343        12  LOAD_GLOBAL              os
               14  LOAD_METHOD              fspath
               16  LOAD_FAST                'source'
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'source'
             22_0  COME_FROM            10  '10'

 L. 344        22  LOAD_GLOBAL              isinstance
               24  LOAD_FAST                'source'
               26  LOAD_GLOBAL              str
               28  CALL_FUNCTION_2       2  ''
               30  POP_JUMP_IF_FALSE    44  'to 44'

 L. 345        32  LOAD_GLOBAL              xmlreader
               34  LOAD_METHOD              InputSource
               36  LOAD_FAST                'source'
               38  CALL_METHOD_1         1  ''
               40  STORE_FAST               'source'
               42  JUMP_FORWARD        138  'to 138'
             44_0  COME_FROM            30  '30'

 L. 346        44  LOAD_GLOBAL              hasattr
               46  LOAD_FAST                'source'
               48  LOAD_STR                 'read'
               50  CALL_FUNCTION_2       2  ''
               52  POP_JUMP_IF_FALSE   138  'to 138'

 L. 347        54  LOAD_FAST                'source'
               56  STORE_FAST               'f'

 L. 348        58  LOAD_GLOBAL              xmlreader
               60  LOAD_METHOD              InputSource
               62  CALL_METHOD_0         0  ''
               64  STORE_FAST               'source'

 L. 349        66  LOAD_GLOBAL              isinstance
               68  LOAD_FAST                'f'
               70  LOAD_METHOD              read
               72  LOAD_CONST               0
               74  CALL_METHOD_1         1  ''
               76  LOAD_GLOBAL              str
               78  CALL_FUNCTION_2       2  ''
               80  POP_JUMP_IF_FALSE    94  'to 94'

 L. 350        82  LOAD_FAST                'source'
               84  LOAD_METHOD              setCharacterStream
               86  LOAD_FAST                'f'
               88  CALL_METHOD_1         1  ''
               90  POP_TOP          
               92  JUMP_FORWARD        104  'to 104'
             94_0  COME_FROM            80  '80'

 L. 352        94  LOAD_FAST                'source'
               96  LOAD_METHOD              setByteStream
               98  LOAD_FAST                'f'
              100  CALL_METHOD_1         1  ''
              102  POP_TOP          
            104_0  COME_FROM            92  '92'

 L. 353       104  LOAD_GLOBAL              hasattr
              106  LOAD_FAST                'f'
              108  LOAD_STR                 'name'
              110  CALL_FUNCTION_2       2  ''
              112  POP_JUMP_IF_FALSE   138  'to 138'
              114  LOAD_GLOBAL              isinstance
              116  LOAD_FAST                'f'
              118  LOAD_ATTR                name
              120  LOAD_GLOBAL              str
              122  CALL_FUNCTION_2       2  ''
              124  POP_JUMP_IF_FALSE   138  'to 138'

 L. 354       126  LOAD_FAST                'source'
              128  LOAD_METHOD              setSystemId
              130  LOAD_FAST                'f'
              132  LOAD_ATTR                name
              134  CALL_METHOD_1         1  ''
              136  POP_TOP          
            138_0  COME_FROM           124  '124'
            138_1  COME_FROM           112  '112'
            138_2  COME_FROM            52  '52'
            138_3  COME_FROM            42  '42'

 L. 356       138  LOAD_FAST                'source'
              140  LOAD_METHOD              getCharacterStream
              142  CALL_METHOD_0         0  ''
              144  LOAD_CONST               None
              146  <117>                 0  ''
          148_150  POP_JUMP_IF_FALSE   288  'to 288'
              152  LOAD_FAST                'source'
              154  LOAD_METHOD              getByteStream
              156  CALL_METHOD_0         0  ''
              158  LOAD_CONST               None
              160  <117>                 0  ''
          162_164  POP_JUMP_IF_FALSE   288  'to 288'

 L. 357       166  LOAD_FAST                'source'
              168  LOAD_METHOD              getSystemId
              170  CALL_METHOD_0         0  ''
              172  STORE_FAST               'sysid'

 L. 358       174  LOAD_GLOBAL              os
              176  LOAD_ATTR                path
              178  LOAD_METHOD              dirname
              180  LOAD_GLOBAL              os
              182  LOAD_ATTR                path
              184  LOAD_METHOD              normpath
              186  LOAD_FAST                'base'
              188  CALL_METHOD_1         1  ''
              190  CALL_METHOD_1         1  ''
              192  STORE_FAST               'basehead'

 L. 359       194  LOAD_GLOBAL              os
              196  LOAD_ATTR                path
              198  LOAD_METHOD              join
              200  LOAD_FAST                'basehead'
              202  LOAD_FAST                'sysid'
              204  CALL_METHOD_2         2  ''
              206  STORE_FAST               'sysidfilename'

 L. 360       208  LOAD_GLOBAL              os
              210  LOAD_ATTR                path
              212  LOAD_METHOD              isfile
              214  LOAD_FAST                'sysidfilename'
              216  CALL_METHOD_1         1  ''
              218  POP_JUMP_IF_FALSE   242  'to 242'

 L. 361       220  LOAD_FAST                'source'
              222  LOAD_METHOD              setSystemId
              224  LOAD_FAST                'sysidfilename'
              226  CALL_METHOD_1         1  ''
              228  POP_TOP          

 L. 362       230  LOAD_GLOBAL              open
              232  LOAD_FAST                'sysidfilename'
              234  LOAD_STR                 'rb'
              236  CALL_FUNCTION_2       2  ''
              238  STORE_FAST               'f'
              240  JUMP_FORWARD        278  'to 278'
            242_0  COME_FROM           218  '218'

 L. 364       242  LOAD_FAST                'source'
              244  LOAD_METHOD              setSystemId
              246  LOAD_GLOBAL              urllib
              248  LOAD_ATTR                parse
              250  LOAD_METHOD              urljoin
              252  LOAD_FAST                'base'
              254  LOAD_FAST                'sysid'
              256  CALL_METHOD_2         2  ''
              258  CALL_METHOD_1         1  ''
              260  POP_TOP          

 L. 365       262  LOAD_GLOBAL              urllib
              264  LOAD_ATTR                request
              266  LOAD_METHOD              urlopen
              268  LOAD_FAST                'source'
              270  LOAD_METHOD              getSystemId
              272  CALL_METHOD_0         0  ''
              274  CALL_METHOD_1         1  ''
              276  STORE_FAST               'f'
            278_0  COME_FROM           240  '240'

 L. 367       278  LOAD_FAST                'source'
              280  LOAD_METHOD              setByteStream
              282  LOAD_FAST                'f'
              284  CALL_METHOD_1         1  ''
              286  POP_TOP          
            288_0  COME_FROM           162  '162'
            288_1  COME_FROM           148  '148'

 L. 369       288  LOAD_FAST                'source'
              290  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 146