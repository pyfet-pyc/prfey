# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: email\_parseaddr.py
"""Email address parsing code.

Lifted directly from rfc822.py.  This should eventually be rewritten.
"""
__all__ = [
 'mktime_tz',
 'parsedate',
 'parsedate_tz',
 'quote']
import time, calendar
SPACE = ' '
EMPTYSTRING = ''
COMMASPACE = ', '
_monthnames = [
 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul',
 'aug', 'sep', 'oct', 'nov', 'dec',
 'january', 'february', 'march', 'april', 'may', 'june', 'july',
 'august', 'september', 'october', 'november', 'december']
_daynames = [
 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
_timezones = {'UT':0, 
 'UTC':0,  'GMT':0,  'Z':0,  'AST':-400, 
 'ADT':-300,  'EST':-500, 
 'EDT':-400,  'CST':-600, 
 'CDT':-500,  'MST':-700, 
 'MDT':-600,  'PST':-800, 
 'PDT':-700}

def parsedate_tz(data):
    """Convert a date string to a time tuple.

    Accounts for military timezones.
    """
    res = _parsedate_tz(data)
    if not res:
        return
    if res[9] is None:
        res[9] = 0
    return tuple(res)


def _parsedate_tz(data):
    """Convert date to extended time tuple.

    The last (additional) element is the time zone offset in seconds, except if
    the timezone was specified as -0000.  In that case the last element is
    None.  This indicates a UTC timestamp that explicitly declaims knowledge of
    the source timezone, as opposed to a +0000 timestamp that indicates the
    source timezone really was UTC.

    """
    if not data:
        return
    data = data.split()
    if data[0].endswith(',') or data[0].lower() in _daynames:
        del data[0]
    else:
        i = data[0].rfind(',')
        if i >= 0:
            data[0] = data[0][i + 1:]
    if len(data) == 3:
        stuff = data[0].split('-')
        if len(stuff) == 3:
            data = stuff + data[1:]
    if len(data) == 4:
        s = data[3]
        i = s.find('+')
        if i == -1:
            i = s.find('-')
        if i > 0:
            data[3:] = [
             s[:i], s[i:]]
        else:
            data.append('')
    if len(data) < 5:
        return
    data = data[:5]
    dd, mm, yy, tm, tz = data
    mm = mm.lower()
    if mm not in _monthnames:
        dd, mm = mm, dd.lower()
        if mm not in _monthnames:
            return
    mm = _monthnames.index(mm) + 1
    if mm > 12:
        mm -= 12
    if dd[(-1)] == ',':
        dd = dd[:-1]
    i = yy.find(':')
    if i > 0:
        yy, tm = tm, yy
    if yy[(-1)] == ',':
        yy = yy[:-1]
    if not yy[0].isdigit():
        yy, tz = tz, yy
    if tm[(-1)] == ',':
        tm = tm[:-1]
    tm = tm.split(':')
    if len(tm) == 2:
        thh, tmm = tm
        tss = '0'
    elif len(tm) == 3:
        thh, tmm, tss = tm
    elif len(tm) == 1 and '.' in tm[0]:
        tm = tm[0].split('.')
        if len(tm) == 2:
            thh, tmm = tm
            tss = 0
        elif len(tm) == 3:
            thh, tmm, tss = tm
    else:
        return
    try:
        yy = int(yy)
        dd = int(dd)
        thh = int(thh)
        tmm = int(tmm)
        tss = int(tss)
    except ValueError:
        return
    else:
        if yy < 100:
            if yy > 68:
                yy += 1900
            else:
                yy += 2000
        tzoffset = None
        tz = tz.upper()
        if tz in _timezones:
            tzoffset = _timezones[tz]
        else:
            try:
                tzoffset = int(tz)
            except ValueError:
                pass
            else:
                if tzoffset == 0:
                    if tz.startswith('-'):
                        tzoffset = None
            if tzoffset:
                if tzoffset < 0:
                    tzsign = -1
                    tzoffset = -tzoffset
                else:
                    tzsign = 1
                tzoffset = tzsign * (tzoffset // 100 * 3600 + tzoffset % 100 * 60)
            return [
             yy, mm, dd, thh, tmm, tss, 0, 1, -1, tzoffset]


def parsedate(data):
    """Convert a time string to a time tuple."""
    t = parsedate_tz(data)
    if isinstance(t, tuple):
        return t[:9]
    return t


def mktime_tz(data):
    """Turn a 10-tuple as returned by parsedate_tz() into a POSIX timestamp."""
    if data[9] is None:
        return time.mktime(data[:8] + (-1, ))
    t = calendar.timegm(data)
    return t - data[9]


def quote(str):
    """Prepare string to be used in a quoted string.

    Turns backslash and double quote characters into quoted pairs.  These
    are the only characters that need to be quoted inside a quoted string.
    Does not add the surrounding double quotes.
    """
    return str.replace('\\', '\\\\').replace('"', '\\"')


class AddrlistClass:
    __doc__ = 'Address parser class by Ben Escoto.\n\n    To understand what this class does, it helps to have a copy of RFC 2822 in\n    front of you.\n\n    Note: this class interface is deprecated and may be removed in the future.\n    Use email.utils.AddressList instead.\n    '

    def __init__(self, field):
        """Initialize a new instance.

        `field' is an unparsed address header field, containing
        one or more addresses.
        """
        self.specials = '()<>@,:;."[]'
        self.pos = 0
        self.LWS = ' \t'
        self.CR = '\r\n'
        self.FWS = self.LWS + self.CR
        self.atomends = self.specials + self.LWS + self.CR
        self.phraseends = self.atomends.replace('.', '')
        self.field = field
        self.commentlist = []

    def gotonext--- This code section failed: ---

 L. 234         0  BUILD_LIST_0          0 
                2  STORE_FAST               'wslist'
              4_0  COME_FROM           128  '128'
              4_1  COME_FROM           124  '124'
              4_2  COME_FROM            90  '90'

 L. 235         4  LOAD_FAST                'self'
                6  LOAD_ATTR                pos
                8  LOAD_GLOBAL              len
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                field
               14  CALL_FUNCTION_1       1  ''
               16  COMPARE_OP               <
               18  POP_JUMP_IF_FALSE   130  'to 130'

 L. 236        20  LOAD_FAST                'self'
               22  LOAD_ATTR                field
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                pos
               28  BINARY_SUBSCR    
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                LWS
               34  LOAD_STR                 '\n\r'
               36  BINARY_ADD       
               38  COMPARE_OP               in
               40  POP_JUMP_IF_FALSE    92  'to 92'

 L. 237        42  LOAD_FAST                'self'
               44  LOAD_ATTR                field
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                pos
               50  BINARY_SUBSCR    
               52  LOAD_STR                 '\n\r'
               54  COMPARE_OP               not-in
               56  POP_JUMP_IF_FALSE    76  'to 76'

 L. 238        58  LOAD_FAST                'wslist'
               60  LOAD_METHOD              append
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                field
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                pos
               70  BINARY_SUBSCR    
               72  CALL_METHOD_1         1  ''
               74  POP_TOP          
             76_0  COME_FROM            56  '56'

 L. 239        76  LOAD_FAST                'self'
               78  DUP_TOP          
               80  LOAD_ATTR                pos
               82  LOAD_CONST               1
               84  INPLACE_ADD      
               86  ROT_TWO          
               88  STORE_ATTR               pos
               90  JUMP_BACK             4  'to 4'
             92_0  COME_FROM            40  '40'

 L. 240        92  LOAD_FAST                'self'
               94  LOAD_ATTR                field
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                pos
              100  BINARY_SUBSCR    
              102  LOAD_STR                 '('
              104  COMPARE_OP               ==
              106  POP_JUMP_IF_FALSE   130  'to 130'

 L. 241       108  LOAD_FAST                'self'
              110  LOAD_ATTR                commentlist
              112  LOAD_METHOD              append
              114  LOAD_FAST                'self'
              116  LOAD_METHOD              getcomment
              118  CALL_METHOD_0         0  ''
              120  CALL_METHOD_1         1  ''
              122  POP_TOP          
              124  JUMP_BACK             4  'to 4'

 L. 243       126  JUMP_FORWARD        130  'to 130'
              128  JUMP_BACK             4  'to 4'
            130_0  COME_FROM           126  '126'
            130_1  COME_FROM           106  '106'
            130_2  COME_FROM            18  '18'

 L. 244       130  LOAD_GLOBAL              EMPTYSTRING
              132  LOAD_METHOD              join
              134  LOAD_FAST                'wslist'
              136  CALL_METHOD_1         1  ''
              138  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 128

    def getaddrlist(self):
        """Parse all addresses.

        Returns a list containing all of the addresses.
        """
        result = []
        while True:
            if self.pos < len(self.field):
                ad = self.getaddress()
                if ad:
                    result += ad
                else:
                    result.append(('', ''))

        return result

    def getaddress(self):
        """Parse the next address."""
        self.commentlist = []
        self.gotonext()
        oldpos = self.pos
        oldcl = self.commentlist
        plist = self.getphraselist()
        self.gotonext()
        returnlist = []
        if self.pos >= len(self.field):
            if plist:
                returnlist = [
                 (
                  SPACE.join(self.commentlist), plist[0])]
        elif self.field[self.pos] in '.@':
            self.pos = oldpos
            self.commentlist = oldcl
            addrspec = self.getaddrspec()
            returnlist = [(SPACE.join(self.commentlist), addrspec)]
        elif self.field[self.pos] == ':':
            returnlist = []
            fieldlen = len(self.field)
            self.pos += 1
            while True:
                if self.pos < len(self.field):
                    self.gotonext()
                    if self.pos < fieldlen and self.field[self.pos] == ';':
                        self.pos += 1
                    else:
                        returnlist = returnlist + self.getaddress()

        elif self.field[self.pos] == '<':
            routeaddr = self.getrouteaddr()
            if self.commentlist:
                returnlist = [(SPACE.join(plist) + ' (' + ' '.join(self.commentlist) + ')', routeaddr)]
            else:
                returnlist = [
                 (
                  SPACE.join(plist), routeaddr)]
        elif plist:
            returnlist = [
             (
              SPACE.join(self.commentlist), plist[0])]
        elif self.field[self.pos] in self.specials:
            self.pos += 1
        self.gotonext()
        if self.pos < len(self.field):
            if self.field[self.pos] == ',':
                self.pos += 1
        return returnlist

    def getrouteaddr(self):
        """Parse a route address (Return-path value).

        This method just skips all the route stuff and returns the addrspec.
        """
        if self.field[self.pos] != '<':
            return
        expectroute = False
        self.pos += 1
        self.gotonext()
        adlist = ''
        while True:
            if self.pos < len(self.field):
                if expectroute:
                    self.getdomain()
                    expectroute = False
                else:
                    if self.field[self.pos] == '>':
                        self.pos += 1
                    else:
                        break
                    if self.field[self.pos] == '@':
                        self.pos += 1
                        expectroute = True
                    elif self.field[self.pos] == ':':
                        self.pos += 1
                    else:
                        adlist = self.getaddrspec()
                        self.pos += 1
            else:
                pass
            self.gotonext()

        return adlist

    def getaddrspec(self):
        """Parse an RFC 2822 addr-spec."""
        aslist = []
        self.gotonext()
        while True:
            if self.pos < len(self.field):
                preserve_ws = True
                if self.field[self.pos] == '.':
                    if aslist:
                        if not aslist[(-1)].strip():
                            aslist.pop()
                    aslist.append('.')
                    self.pos += 1
                    preserve_ws = False
                elif self.field[self.pos] == '"':
                    aslist.append('"%s"' % quote(self.getquote()))
                else:
                    if self.field[self.pos] in self.atomends:
                        if aslist:
                            aslist[(-1)].strip() or aslist.pop()
                    else:
                        break
                    aslist.append(self.getatom())
                ws = self.gotonext()
                if preserve_ws:
                    if ws:
                        aslist.append(ws)

        if self.pos >= len(self.field) or (self.field[self.pos] != '@'):
            return EMPTYSTRING.join(aslist)
        aslist.append('@')
        self.pos += 1
        self.gotonext()
        domain = self.getdomain()
        if not domain:
            return EMPTYSTRING
        return EMPTYSTRING.join(aslist) + domain

    def getdomain(self):
        """Get the complete domain name from an address."""
        sdlist = []
        while True:
            if self.pos < len(self.field):
                if self.field[self.pos] in self.LWS:
                    self.pos += 1
                else:
                    if self.field[self.pos] == '(':
                        self.commentlist.append(self.getcomment())
                    else:
                        if self.field[self.pos] == '[':
                            sdlist.append(self.getdomainliteral())
                        else:
                            if self.field[self.pos] == '.':
                                self.pos += 1
                                sdlist.append('.')
                            else:
                                if self.field[self.pos] == '@':
                                    return EMPTYSTRING
                                if self.field[self.pos] in self.atomends:
                                    pass
                            sdlist.append(self.getatom())

        return EMPTYSTRING.join(sdlist)

    def getdelimited--- This code section failed: ---

 L. 425         0  LOAD_FAST                'self'
                2  LOAD_ATTR                field
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                pos
                8  BINARY_SUBSCR    
               10  LOAD_FAST                'beginchar'
               12  COMPARE_OP               !=
               14  POP_JUMP_IF_FALSE    20  'to 20'

 L. 426        16  LOAD_STR                 ''
               18  RETURN_VALUE     
             20_0  COME_FROM            14  '14'

 L. 428        20  LOAD_STR                 ''
               22  BUILD_LIST_1          1 
               24  STORE_FAST               'slist'

 L. 429        26  LOAD_CONST               False
               28  STORE_FAST               'quote'

 L. 430        30  LOAD_FAST                'self'
               32  DUP_TOP          
               34  LOAD_ATTR                pos
               36  LOAD_CONST               1
               38  INPLACE_ADD      
               40  ROT_TWO          
               42  STORE_ATTR               pos
             44_0  COME_FROM           214  '214'
             44_1  COME_FROM           156  '156'

 L. 431        44  LOAD_FAST                'self'
               46  LOAD_ATTR                pos
               48  LOAD_GLOBAL              len
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                field
               54  CALL_FUNCTION_1       1  ''
               56  COMPARE_OP               <
               58  POP_JUMP_IF_FALSE   216  'to 216'

 L. 432        60  LOAD_FAST                'quote'
               62  POP_JUMP_IF_FALSE    88  'to 88'

 L. 433        64  LOAD_FAST                'slist'
               66  LOAD_METHOD              append
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                field
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                pos
               76  BINARY_SUBSCR    
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          

 L. 434        82  LOAD_CONST               False
               84  STORE_FAST               'quote'
               86  JUMP_FORWARD        200  'to 200'
             88_0  COME_FROM            62  '62'

 L. 435        88  LOAD_FAST                'self'
               90  LOAD_ATTR                field
               92  LOAD_FAST                'self'
               94  LOAD_ATTR                pos
               96  BINARY_SUBSCR    
               98  LOAD_FAST                'endchars'
              100  COMPARE_OP               in
              102  POP_JUMP_IF_FALSE   122  'to 122'

 L. 436       104  LOAD_FAST                'self'
              106  DUP_TOP          
              108  LOAD_ATTR                pos
              110  LOAD_CONST               1
              112  INPLACE_ADD      
              114  ROT_TWO          
              116  STORE_ATTR               pos

 L. 437       118  JUMP_FORWARD        216  'to 216'
              120  BREAK_LOOP          200  'to 200'
            122_0  COME_FROM           102  '102'

 L. 438       122  LOAD_FAST                'allowcomments'
              124  POP_JUMP_IF_FALSE   160  'to 160'
              126  LOAD_FAST                'self'
              128  LOAD_ATTR                field
              130  LOAD_FAST                'self'
              132  LOAD_ATTR                pos
              134  BINARY_SUBSCR    
              136  LOAD_STR                 '('
              138  COMPARE_OP               ==
              140  POP_JUMP_IF_FALSE   160  'to 160'

 L. 439       142  LOAD_FAST                'slist'
              144  LOAD_METHOD              append
              146  LOAD_FAST                'self'
              148  LOAD_METHOD              getcomment
              150  CALL_METHOD_0         0  ''
              152  CALL_METHOD_1         1  ''
              154  POP_TOP          

 L. 440       156  JUMP_BACK            44  'to 44'
              158  BREAK_LOOP          200  'to 200'
            160_0  COME_FROM           140  '140'
            160_1  COME_FROM           124  '124'

 L. 441       160  LOAD_FAST                'self'
              162  LOAD_ATTR                field
              164  LOAD_FAST                'self'
              166  LOAD_ATTR                pos
              168  BINARY_SUBSCR    
              170  LOAD_STR                 '\\'
              172  COMPARE_OP               ==
              174  POP_JUMP_IF_FALSE   182  'to 182'

 L. 442       176  LOAD_CONST               True
              178  STORE_FAST               'quote'
              180  JUMP_FORWARD        200  'to 200'
            182_0  COME_FROM           174  '174'

 L. 444       182  LOAD_FAST                'slist'
              184  LOAD_METHOD              append
              186  LOAD_FAST                'self'
              188  LOAD_ATTR                field
              190  LOAD_FAST                'self'
              192  LOAD_ATTR                pos
              194  BINARY_SUBSCR    
              196  CALL_METHOD_1         1  ''
              198  POP_TOP          
            200_0  COME_FROM           180  '180'
            200_1  COME_FROM           158  '158'
            200_2  COME_FROM           120  '120'
            200_3  COME_FROM            86  '86'

 L. 445       200  LOAD_FAST                'self'
              202  DUP_TOP          
              204  LOAD_ATTR                pos
              206  LOAD_CONST               1
              208  INPLACE_ADD      
              210  ROT_TWO          
              212  STORE_ATTR               pos
              214  JUMP_BACK            44  'to 44'
            216_0  COME_FROM           118  '118'
            216_1  COME_FROM            58  '58'

 L. 447       216  LOAD_GLOBAL              EMPTYSTRING
              218  LOAD_METHOD              join
              220  LOAD_FAST                'slist'
              222  CALL_METHOD_1         1  ''
              224  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_GLOBAL' instruction at offset 216

    def getquote(self):
        """Get a quote-delimited fragment from self's field."""
        return self.getdelimited('"', '"\r', False)

    def getcomment(self):
        """Get a parenthesis-delimited fragment from self's field."""
        return self.getdelimited('(', ')\r', True)

    def getdomainliteral(self):
        """Parse an RFC 2822 domain-literal."""
        return '[%s]' % self.getdelimited('[', ']\r', False)

    def getatom--- This code section failed: ---

 L. 468         0  LOAD_STR                 ''
                2  BUILD_LIST_1          1 
                4  STORE_FAST               'atomlist'

 L. 469         6  LOAD_FAST                'atomends'
                8  LOAD_CONST               None
               10  COMPARE_OP               is
               12  POP_JUMP_IF_FALSE    20  'to 20'

 L. 470        14  LOAD_FAST                'self'
               16  LOAD_ATTR                atomends
               18  STORE_FAST               'atomends'
             20_0  COME_FROM            88  '88'
             20_1  COME_FROM            12  '12'

 L. 472        20  LOAD_FAST                'self'
               22  LOAD_ATTR                pos
               24  LOAD_GLOBAL              len
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                field
               30  CALL_FUNCTION_1       1  ''
               32  COMPARE_OP               <
               34  POP_JUMP_IF_FALSE    90  'to 90'

 L. 473        36  LOAD_FAST                'self'
               38  LOAD_ATTR                field
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                pos
               44  BINARY_SUBSCR    
               46  LOAD_FAST                'atomends'
               48  COMPARE_OP               in
               50  POP_JUMP_IF_FALSE    56  'to 56'

 L. 474        52  JUMP_FORWARD         90  'to 90'
               54  BREAK_LOOP           74  'to 74'
             56_0  COME_FROM            50  '50'

 L. 476        56  LOAD_FAST                'atomlist'
               58  LOAD_METHOD              append
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                field
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                pos
               68  BINARY_SUBSCR    
               70  CALL_METHOD_1         1  ''
               72  POP_TOP          
             74_0  COME_FROM            54  '54'

 L. 477        74  LOAD_FAST                'self'
               76  DUP_TOP          
               78  LOAD_ATTR                pos
               80  LOAD_CONST               1
               82  INPLACE_ADD      
               84  ROT_TWO          
               86  STORE_ATTR               pos
               88  JUMP_BACK            20  'to 20'
             90_0  COME_FROM            52  '52'
             90_1  COME_FROM            34  '34'

 L. 479        90  LOAD_GLOBAL              EMPTYSTRING
               92  LOAD_METHOD              join
               94  LOAD_FAST                'atomlist'
               96  CALL_METHOD_1         1  ''
               98  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_GLOBAL' instruction at offset 90

    def getphraselist(self):
        """Parse a sequence of RFC 2822 phrases.

        A phrase is a sequence of words, which are in turn either RFC 2822
        atoms or quoted-strings.  Phrases are canonicalized by squeezing all
        runs of continuous whitespace into one space.
        """
        plist = []
        while True:
            if self.pos < len(self.field):
                if self.field[self.pos] in self.FWS:
                    self.pos += 1
                else:
                    if self.field[self.pos] == '"':
                        plist.append(self.getquote())
                    else:
                        if self.field[self.pos] == '(':
                            self.commentlist.append(self.getcomment())
                        elif self.field[self.pos] in self.phraseends:
                            pass
                        plist.append(self.getatom(self.phraseends))

        return plist


class AddressList(AddrlistClass):
    __doc__ = 'An AddressList encapsulates a list of parsed RFC 2822 addresses.'

    def __init__(self, field):
        AddrlistClass.__init__(self, field)
        if field:
            self.addresslist = self.getaddrlist()
        else:
            self.addresslist = []

    def __len__(self):
        return len(self.addresslist)

    def __add__(self, other):
        newaddr = AddressList(None)
        newaddr.addresslist = self.addresslist[:]
        for x in other.addresslist:
            if x not in self.addresslist:
                newaddr.addresslist.append(x)
        else:
            return newaddr

    def __iadd__(self, other):
        for x in other.addresslist:
            if x not in self.addresslist:
                self.addresslist.append(x)
        else:
            return self

    def __sub__(self, other):
        newaddr = AddressList(None)
        for x in self.addresslist:
            if x not in other.addresslist:
                newaddr.addresslist.append(x)
        else:
            return newaddr

    def __isub__(self, other):
        for x in other.addresslist:
            if x in self.addresslist:
                self.addresslist.remove(x)
        else:
            return self

    def __getitem__(self, index):
        return self.addresslist[index]