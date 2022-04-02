# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
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

    def gotonext(self):
        """Skip white space and extract comments."""
        wslist = []
        while self.pos < len(self.field):
            if self.field[self.pos] in self.LWS + '\n\r':
                if self.field[self.pos] not in '\n\r':
                    wslist.append(self.field[self.pos])
                else:
                    self.pos += 1
            else:
                if self.field[self.pos] == '(':
                    self.commentlist.append(self.getcomment())
                else:
                    break

        return EMPTYSTRING.join(wslist)

    def getaddrlist(self):
        """Parse all addresses.

        Returns a list containing all of the addresses.
        """
        result = []
        while self.pos < len(self.field):
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
            while self.pos < len(self.field):
                self.gotonext()
                if self.pos < fieldlen:
                    if self.field[self.pos] == ';':
                        self.pos += 1
                        break
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
        while self.pos < len(self.field):
            if expectroute:
                self.getdomain()
                expectroute = False
            else:
                if self.field[self.pos] == '>':
                    self.pos += 1
                    break
                else:
                    if self.field[self.pos] == '@':
                        self.pos += 1
                        expectroute = True
                    else:
                        if self.field[self.pos] == ':':
                            self.pos += 1
                        else:
                            adlist = self.getaddrspec()
                            self.pos += 1
                            break
            self.gotonext()

        return adlist

    def getaddrspec(self):
        """Parse an RFC 2822 addr-spec."""
        aslist = []
        self.gotonext()
        while self.pos < len(self.field):
            preserve_ws = True
            if self.field[self.pos] == '.':
                if aslist:
                    if not aslist[(-1)].strip():
                        aslist.pop()
                    aslist.append('.')
                    self.pos += 1
                    preserve_ws = False
            else:
                if self.field[self.pos] == '"':
                    aslist.append('"%s"' % quote(self.getquote()))
                else:
                    if self.field[self.pos] in self.atomends:
                        if aslist:
                            if not aslist[(-1)].strip():
                                aslist.pop()
                            break
                    else:
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
        return EMPTYSTRING.join(aslist) + self.getdomain()

    def getdomain(self):
        """Get the complete domain name from an address."""
        sdlist = []
        while self.pos < len(self.field):
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
                            if self.field[self.pos] in self.atomends:
                                break
                            else:
                                sdlist.append(self.getatom())

        return EMPTYSTRING.join(sdlist)

    def getdelimited--- This code section failed: ---

 L. 416         0  LOAD_FAST                'self'
                2  LOAD_ATTR                field
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                pos
                8  BINARY_SUBSCR    
               10  LOAD_FAST                'beginchar'
               12  COMPARE_OP               !=
               14  POP_JUMP_IF_FALSE    20  'to 20'

 L. 417        16  LOAD_STR                 ''
               18  RETURN_VALUE     
             20_0  COME_FROM            14  '14'

 L. 419        20  LOAD_STR                 ''
               22  BUILD_LIST_1          1 
               24  STORE_FAST               'slist'

 L. 420        26  LOAD_CONST               False
               28  STORE_FAST               'quote'

 L. 421        30  LOAD_FAST                'self'
               32  DUP_TOP          
               34  LOAD_ATTR                pos
               36  LOAD_CONST               1
               38  INPLACE_ADD      
               40  ROT_TWO          
               42  STORE_ATTR               pos

 L. 422        44  SETUP_LOOP          220  'to 220'
             46_0  COME_FROM           216  '216'
             46_1  COME_FROM           158  '158'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                pos
               50  LOAD_GLOBAL              len
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                field
               56  CALL_FUNCTION_1       1  '1 positional argument'
               58  COMPARE_OP               <
               60  POP_JUMP_IF_FALSE   218  'to 218'

 L. 423        62  LOAD_FAST                'quote'
               64  POP_JUMP_IF_FALSE    90  'to 90'

 L. 424        66  LOAD_FAST                'slist'
               68  LOAD_METHOD              append
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                field
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                pos
               78  BINARY_SUBSCR    
               80  CALL_METHOD_1         1  '1 positional argument'
               82  POP_TOP          

 L. 425        84  LOAD_CONST               False
               86  STORE_FAST               'quote'
               88  JUMP_FORWARD        202  'to 202'
             90_0  COME_FROM            64  '64'

 L. 426        90  LOAD_FAST                'self'
               92  LOAD_ATTR                field
               94  LOAD_FAST                'self'
               96  LOAD_ATTR                pos
               98  BINARY_SUBSCR    
              100  LOAD_FAST                'endchars'
              102  COMPARE_OP               in
              104  POP_JUMP_IF_FALSE   124  'to 124'

 L. 427       106  LOAD_FAST                'self'
              108  DUP_TOP          
              110  LOAD_ATTR                pos
              112  LOAD_CONST               1
              114  INPLACE_ADD      
              116  ROT_TWO          
              118  STORE_ATTR               pos

 L. 428       120  BREAK_LOOP       
              122  JUMP_FORWARD        202  'to 202'
            124_0  COME_FROM           104  '104'

 L. 429       124  LOAD_FAST                'allowcomments'
              126  POP_JUMP_IF_FALSE   162  'to 162'
              128  LOAD_FAST                'self'
              130  LOAD_ATTR                field
              132  LOAD_FAST                'self'
              134  LOAD_ATTR                pos
              136  BINARY_SUBSCR    
              138  LOAD_STR                 '('
              140  COMPARE_OP               ==
              142  POP_JUMP_IF_FALSE   162  'to 162'

 L. 430       144  LOAD_FAST                'slist'
              146  LOAD_METHOD              append
              148  LOAD_FAST                'self'
              150  LOAD_METHOD              getcomment
              152  CALL_METHOD_0         0  '0 positional arguments'
              154  CALL_METHOD_1         1  '1 positional argument'
              156  POP_TOP          

 L. 431       158  CONTINUE             46  'to 46'
              160  JUMP_FORWARD        202  'to 202'
            162_0  COME_FROM           142  '142'
            162_1  COME_FROM           126  '126'

 L. 432       162  LOAD_FAST                'self'
              164  LOAD_ATTR                field
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                pos
              170  BINARY_SUBSCR    
              172  LOAD_STR                 '\\'
              174  COMPARE_OP               ==
              176  POP_JUMP_IF_FALSE   184  'to 184'

 L. 433       178  LOAD_CONST               True
              180  STORE_FAST               'quote'
              182  JUMP_FORWARD        202  'to 202'
            184_0  COME_FROM           176  '176'

 L. 435       184  LOAD_FAST                'slist'
              186  LOAD_METHOD              append
              188  LOAD_FAST                'self'
              190  LOAD_ATTR                field
              192  LOAD_FAST                'self'
              194  LOAD_ATTR                pos
              196  BINARY_SUBSCR    
              198  CALL_METHOD_1         1  '1 positional argument'
              200  POP_TOP          
            202_0  COME_FROM           182  '182'
            202_1  COME_FROM           160  '160'
            202_2  COME_FROM           122  '122'
            202_3  COME_FROM            88  '88'

 L. 436       202  LOAD_FAST                'self'
              204  DUP_TOP          
              206  LOAD_ATTR                pos
              208  LOAD_CONST               1
              210  INPLACE_ADD      
              212  ROT_TWO          
              214  STORE_ATTR               pos
              216  JUMP_BACK            46  'to 46'
            218_0  COME_FROM            60  '60'
              218  POP_BLOCK        
            220_0  COME_FROM_LOOP       44  '44'

 L. 438       220  LOAD_GLOBAL              EMPTYSTRING
              222  LOAD_METHOD              join
              224  LOAD_FAST                'slist'
              226  CALL_METHOD_1         1  '1 positional argument'
              228  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 202

    def getquote(self):
        """Get a quote-delimited fragment from self's field."""
        return self.getdelimited('"', '"\r', False)

    def getcomment(self):
        """Get a parenthesis-delimited fragment from self's field."""
        return self.getdelimited('(', ')\r', True)

    def getdomainliteral(self):
        """Parse an RFC 2822 domain-literal."""
        return '[%s]' % self.getdelimited('[', ']\r', False)

    def getatom(self, atomends=None):
        """Parse an RFC 2822 atom.

        Optional atomends specifies a different set of end token delimiters
        (the default is to use self.atomends).  This is used e.g. in
        getphraselist() since phrase endings must not include the `.' (which
        is legal in phrases)."""
        atomlist = [
         '']
        if atomends is None:
            atomends = self.atomends
        while self.pos < len(self.field):
            if self.field[self.pos] in atomends:
                break
            else:
                atomlist.append(self.field[self.pos])
            self.pos += 1

        return EMPTYSTRING.join(atomlist)

    def getphraselist(self):
        """Parse a sequence of RFC 2822 phrases.

        A phrase is a sequence of words, which are in turn either RFC 2822
        atoms or quoted-strings.  Phrases are canonicalized by squeezing all
        runs of continuous whitespace into one space.
        """
        plist = []
        while self.pos < len(self.field):
            if self.field[self.pos] in self.FWS:
                self.pos += 1
            else:
                if self.field[self.pos] == '"':
                    plist.append(self.getquote())
                else:
                    if self.field[self.pos] == '(':
                        self.commentlist.append(self.getcomment())
                    else:
                        if self.field[self.pos] in self.phraseends:
                            break
                        else:
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

        return newaddr

    def __iadd__(self, other):
        for x in other.addresslist:
            if x not in self.addresslist:
                self.addresslist.append(x)

        return self

    def __sub__(self, other):
        newaddr = AddressList(None)
        for x in self.addresslist:
            if x not in other.addresslist:
                newaddr.addresslist.append(x)

        return newaddr

    def __isub__(self, other):
        for x in other.addresslist:
            if x in self.addresslist:
                self.addresslist.remove(x)

        return self

    def __getitem__(self, index):
        return self.addresslist[index]