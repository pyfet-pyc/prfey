# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
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

    def __init__(self):
        if self.__class__ is ParserBase:
            raise RuntimeError('_markupbase.ParserBase must be subclassed')

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

    def parse_declaration(self, i):
        rawdata = self.rawdata
        j = i + 2
        assert rawdata[i:j] == '<!', 'unexpected call to parse_declaration'
        if rawdata[j:j + 1] == '>':
            return j + 1
        if rawdata[j:j + 1] in ('-', ''):
            return -1
        n = len(rawdata)
        if rawdata[j:j + 2] == '--':
            return self.parse_comment(i)
        if rawdata[j] == '[':
            return self.parse_marked_section(i)
        decltype, j = self._scan_name(j, i)
        if j < 0:
            return j
        if decltype == 'doctype':
            self._decl_otherchars = ''
            while True:
                if j < n:
                    c = rawdata[j]
                    if c == '>':
                        data = rawdata[i + 2:j]
                        if decltype == 'doctype':
                            self.handle_decl(data)
                        else:
                            self.unknown_decl(data)
                        return j + 1
                    if c in '"\'':
                        m = _declstringlit_match(rawdata, j)
                        if not m:
                            return -1
                        j = m.end()
                    elif c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
                        name, j = self._scan_name(j, i)
                    elif c in self._decl_otherchars:
                        j = j + 1
                    elif c == '[':
                        if decltype == 'doctype':
                            j = self._parse_doctype_subset(j + 1, i)
                        elif decltype in frozenset({'linktype', 'element', 'link', 'attlist'}):
                            self.error("unsupported '[' char in %s declaration" % decltype)
                        else:
                            self.error("unexpected '[' char in declaration")
                    else:
                        self.error('unexpected %r char in declaration' % rawdata[j])
                    if j < 0:
                        return j

            return -1

    def parse_marked_section(self, i, report=1):
        rawdata = self.rawdata
        assert rawdata[i:i + 3] == '<![', 'unexpected call to parse_marked_section()'
        sectName, j = self._scan_name(i + 3, i)
        if j < 0:
            return j
        if sectName in frozenset({'include', 'rcdata', 'cdata', 'temp', 'ignore'}):
            match = _markedsectionclose.search(rawdata, i + 3)
        elif sectName in frozenset({'if', 'endif', 'else'}):
            match = _msmarkedsectionclose.search(rawdata, i + 3)
        else:
            self.error('unknown status keyword %r in marked section' % rawdata[i + 3:j])
        if not match:
            return -1
        if report:
            j = match.start(0)
            self.unknown_decl(rawdata[i + 3:j])
        return match.end(0)

    def parse_comment(self, i, report=1):
        rawdata = self.rawdata
        if rawdata[i:i + 4] != '<!--':
            self.error('unexpected call to parse_comment()')
        match = _commentclose.search(rawdata, i + 4)
        if not match:
            return -1
        if report:
            j = match.start(0)
            self.handle_comment(rawdata[i + 4:j])
        return match.end(0)

    def _parse_doctype_subset(self, i, declstartpos):
        rawdata = self.rawdata
        n = len(rawdata)
        j = i
        while j < n:
            c = rawdata[j]
            if c == '<':
                s = rawdata[j:j + 2]
                if s == '<':
                    return -1
                if s != '<!':
                    self.updatepos(declstartpos, j + 1)
                    self.error('unexpected char in internal subset (in %r)' % s)
                if j + 2 == n:
                    return -1
                if j + 4 > n:
                    return -1
                if rawdata[j:j + 4] == '<!--':
                    j = self.parse_comment(j, report=0)
                    if j < 0:
                        return j
                else:
                    name, j = self._scan_name(j + 2, declstartpos)
                    if j == -1:
                        return -1
                    if name not in frozenset({'element', 'entity', 'notation', 'attlist'}):
                        self.updatepos(declstartpos, j + 2)
                        self.error('unknown declaration %r in internal subset' % name)
                    meth = getattr(self, '_parse_doctype_' + name)
                    j = meth(j, declstartpos)
                    if j < 0:
                        return j
                if c == '%':
                    if j + 1 == n:
                        return -1
                    else:
                        s, j = self._scan_name(j + 1, declstartpos)
                        if j < 0:
                            return j
                        if rawdata[j] == ';':
                            j = j + 1
                else:
                    if c == ']':
                        j = j + 1
                        while j < n:
                            if rawdata[j].isspace():
                                j = j + 1

                        if j < n:
                            if rawdata[j] == '>':
                                return j
                            self.updatepos(declstartpos, j)
                            self.error('unexpected char after internal subset')
                        else:
                            return -1
                    else:
                        if c.isspace():
                            j = j + 1
                        else:
                            self.updatepos(declstartpos, j)
                            self.error('unexpected char %r in internal subset' % c)

        return -1

    def _parse_doctype_element(self, i, declstartpos):
        name, j = self._scan_name(i, declstartpos)
        if j == -1:
            return -1
        rawdata = self.rawdata
        if '>' in rawdata[j:]:
            return rawdata.find('>', j) + 1
        return -1

    def _parse_doctype_attlist(self, i, declstartpos):
        rawdata = self.rawdata
        name, j = self._scan_name(i, declstartpos)
        c = rawdata[j:j + 1]
        if c == '':
            return -1
        if c == '>':
            return j + 1
        while True:
            name, j = self._scan_name(j, declstartpos)
            if j < 0:
                return j
            c = rawdata[j:j + 1]
            if c == '':
                return -1
            if c == '(':
                if ')' in rawdata[j:]:
                    j = rawdata.find(')', j) + 1
                else:
                    return -1
                while True:
                    if rawdata[j:j + 1].isspace():
                        j = j + 1

                if not rawdata[j:]:
                    return -1
            else:
                name, j = self._scan_name(j, declstartpos)
            c = rawdata[j:j + 1]
            if not c:
                return -1
            if c in '\'"':
                m = _declstringlit_match(rawdata, j)
                if m:
                    j = m.end()
                else:
                    return -1
                c = rawdata[j:j + 1]
                if not c:
                    return -1
            if c == '#':
                if rawdata[j:] == '#':
                    return -1
                else:
                    name, j = self._scan_name(j + 1, declstartpos)
                    if j < 0:
                        return j
                    c = rawdata[j:j + 1]
                    if not c:
                        return -1
                if c == '>':
                    return j + 1

    def _parse_doctype_notation(self, i, declstartpos):
        name, j = self._scan_name(i, declstartpos)
        if j < 0:
            return j
        rawdata = self.rawdata
        while True:
            while True:
                c = rawdata[j:j + 1]
                if not c:
                    return -1
                else:
                    if c == '>':
                        return j + 1
                    if c in '\'"':
                        m = _declstringlit_match(rawdata, j)
                        if not m:
                            return -1
                        j = m.end()

            name, j = self._scan_name(j, declstartpos)
            if j < 0:
                return j

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
             34_0  COME_FROM            78  '78'
             34_1  COME_FROM            74  '74'

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

 L. 351        76  JUMP_FORWARD         86  'to 86'
               78  JUMP_BACK            34  'to 34'
             80_0  COME_FROM            64  '64'
               80  JUMP_FORWARD         86  'to 86'
             82_0  COME_FROM            24  '24'

 L. 353        82  LOAD_FAST                'i'
               84  STORE_FAST               'j'
             86_0  COME_FROM            80  '80'
             86_1  COME_FROM            76  '76'

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
            114_0  COME_FROM           222  '222'
            114_1  COME_FROM           216  '216'
            114_2  COME_FROM           176  '176'
            114_3  COME_FROM           108  '108'

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
              144  COMPARE_OP               in
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
              170  JUMP_FORWARD        222  'to 222'
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
              216  POP_JUMP_IF_FALSE_BACK   114  'to 114'

 L. 372       218  LOAD_FAST                'j'
              220  RETURN_VALUE     
            222_0  COME_FROM           170  '170'
              222  JUMP_BACK           114  'to 114'

Parse error at or near `JUMP_FORWARD' instruction at offset 80

    def _scan_name(self, i, declstartpos):
        rawdata = self.rawdata
        n = len(rawdata)
        if i == n:
            return (None, -1)
        m = _declname_match(rawdata, i)
        if m:
            s = m.group()
            name = s.strip()
            if i + len(s) == n:
                return (None, -1)
            return (name.lower(), m.end())
        self.updatepos(declstartpos, i)
        self.error('expected name token at %r' % rawdata[declstartpos:declstartpos + 20])

    def unknown_decl(self, data):
        pass