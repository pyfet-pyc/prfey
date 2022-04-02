# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.11 (default, Sep  3 2021, 20:46:09) 
# [GCC 10.2.1 20210110]
# Embedded file name: setuptools\_vendor\pyparsing.py
"""
pyparsing module - Classes and methods to define and execute parsing grammars
=============================================================================

The pyparsing module is an alternative approach to creating and executing simple grammars,
vs. the traditional lex/yacc approach, or the use of regular expressions.  With pyparsing, you
don't need to learn a new syntax for defining grammars or matching expressions - the parsing module
provides a library of classes that you use to construct the grammar directly in Python.

Here is a program to parse "Hello, World!" (or any greeting of the form 
C{"<salutation>, <addressee>!"}), built up using L{Word}, L{Literal}, and L{And} elements 
(L{'+'<ParserElement.__add__>} operator gives L{And} expressions, strings are auto-converted to
L{Literal} expressions)::

    from pyparsing import Word, alphas

    # define grammar of a greeting
    greet = Word(alphas) + "," + Word(alphas) + "!"

    hello = "Hello, World!"
    print (hello, "->", greet.parseString(hello))

The program outputs the following::

    Hello, World! -> ['Hello', ',', 'World', '!']

The Python representation of the grammar is quite readable, owing to the self-explanatory
class names, and the use of '+', '|' and '^' operators.

The L{ParseResults} object returned from L{ParserElement.parseString<ParserElement.parseString>} can be accessed as a nested list, a dictionary, or an
object with named attributes.

The pyparsing module handles some of the problems that are typically vexing when writing text parsers:
 - extra or missing whitespace (the above program will also handle "Hello,World!", "Hello  ,  World  !", etc.)
 - quoted strings
 - embedded comments

Getting Started -
-----------------
Visit the classes L{ParserElement} and L{ParseResults} to see the base classes that most other pyparsing
classes inherit from. Use the docstrings for examples of how to:
 - construct literal match expressions from L{Literal} and L{CaselessLiteral} classes
 - construct character word-group expressions using the L{Word} class
 - see how to create repetitive expressions using L{ZeroOrMore} and L{OneOrMore} classes
 - use L{'+'<And>}, L{'|'<MatchFirst>}, L{'^'<Or>}, and L{'&'<Each>} operators to combine simple expressions into more complex ones
 - associate names with your parsed results using L{ParserElement.setResultsName}
 - find some helpful expression short-cuts like L{delimitedList} and L{oneOf}
 - find more useful common expressions in the L{pyparsing_common} namespace class
"""
__version__ = '2.2.1'
__versionTime__ = '18 Sep 2018 00:49 UTC'
__author__ = 'Paul McGuire <ptmcg@users.sourceforge.net>'
import string
from weakref import ref as wkref
import copy, sys, warnings, re, sre_constants, collections, pprint, traceback, types
from datetime import datetime
try:
    from _thread import RLock
except ImportError:
    from threading import RLock

try:
    from collections.abc import Iterable
    from collections.abc import MutableMapping
except ImportError:
    from collections import Iterable
    from collections import MutableMapping

try:
    from collections import OrderedDict as _OrderedDict
except ImportError:
    try:
        from ordereddict import OrderedDict as _OrderedDict
    except ImportError:
        _OrderedDict = None

__all__ = [
 'And', 'CaselessKeyword', 'CaselessLiteral', 'CharsNotIn', 'Combine', 'Dict', 'Each', 'Empty',
 'FollowedBy', 'Forward', 'GoToColumn', 'Group', 'Keyword', 'LineEnd', 'LineStart', 'Literal',
 'MatchFirst', 'NoMatch', 'NotAny', 'OneOrMore', 'OnlyOnce', 'Optional', 'Or',
 'ParseBaseException', 'ParseElementEnhance', 'ParseException', 'ParseExpression', 'ParseFatalException',
 'ParseResults', 'ParseSyntaxException', 'ParserElement', 'QuotedString', 'RecursiveGrammarException',
 'Regex', 'SkipTo', 'StringEnd', 'StringStart', 'Suppress', 'Token', 'TokenConverter',
 'White', 'Word', 'WordEnd', 'WordStart', 'ZeroOrMore',
 'alphanums', 'alphas', 'alphas8bit', 'anyCloseTag', 'anyOpenTag', 'cStyleComment', 'col',
 'commaSeparatedList', 'commonHTMLEntity', 'countedArray', 'cppStyleComment', 'dblQuotedString',
 'dblSlashComment', 'delimitedList', 'dictOf', 'downcaseTokens', 'empty', 'hexnums',
 'htmlComment', 'javaStyleComment', 'line', 'lineEnd', 'lineStart', 'lineno',
 'makeHTMLTags', 'makeXMLTags', 'matchOnlyAtCol', 'matchPreviousExpr', 'matchPreviousLiteral',
 'nestedExpr', 'nullDebugAction', 'nums', 'oneOf', 'opAssoc', 'operatorPrecedence', 'printables',
 'punc8bit', 'pythonStyleComment', 'quotedString', 'removeQuotes', 'replaceHTMLEntity',
 'replaceWith', 'restOfLine', 'sglQuotedString', 'srange', 'stringEnd',
 'stringStart', 'traceParseAction', 'unicodeString', 'upcaseTokens', 'withAttribute',
 'indentedBlock', 'originalTextFor', 'ungroup', 'infixNotation', 'locatedExpr', 'withClass',
 'CloseMatch', 'tokenMap', 'pyparsing_common']
system_version = tuple(sys.version_info)[:3]
PY_3 = system_version[0] == 3
if PY_3:
    _MAX_INT = sys.maxsize
    basestring = str
    unichr = chr
    _ustr = str
    singleArgBuiltins = [
     sum, len, sorted, reversed, list, tuple, set, any, all, min, max]
else:
    _MAX_INT = sys.maxint
    range = xrange

    def _ustr(obj):
        """Drop-in replacement for str(obj) that tries to be Unicode friendly. It first tries
           str(obj). If that fails with a UnicodeEncodeError, then it tries unicode(obj). It
           then < returns the unicode object | encodes it with the default encoding | ... >.
        """
        if isinstance(obj, unicode):
            return obj
        try:
            return str(obj)
        except UnicodeEncodeError:
            ret = unicode(obj).encode(sys.getdefaultencoding(), 'xmlcharrefreplace')
            xmlcharref = Regex('&#\\d+;')
            xmlcharref.setParseAction(lambda t: '\\u' + hex(int(t[0][2:-1]))[2:])
            return xmlcharref.transformString(ret)


    singleArgBuiltins = []
    import __builtin__
    for fname in 'sum len sorted reversed list tuple set any all min max'.split():
        try:
            singleArgBuiltins.append(getattr(__builtin__, fname))
        except AttributeError:
            continue

_generatorType = type((y for y in range(1)))

def _xml_escape(data):
    """Escape &, <, >, ", ', etc. in a string of data."""
    from_symbols = '&><"\''
    to_symbols = ('&' + s + ';' for s in 'amp gt lt quot apos'.split())
    for from_, to_ in zip(from_symbols, to_symbols):
        data = data.replace(from_, to_)

    return data


class _Constants(object):
    pass


alphas = string.ascii_uppercase + string.ascii_lowercase
nums = '0123456789'
hexnums = nums + 'ABCDEFabcdef'
alphanums = alphas + nums
_bslash = chr(92)
printables = ''.join((c for c in string.printable if c not in string.whitespace))

class ParseBaseException(Exception):
    __doc__ = 'base exception class for all parsing runtime exceptions'

    def __init__(self, pstr, loc=0, msg=None, elem=None):
        self.loc = loc
        if msg is None:
            self.msg = pstr
            self.pstr = ''
        else:
            self.msg = msg
            self.pstr = pstr
        self.parserElement = elem
        self.args = (pstr, loc, msg)

    @classmethod
    def _from_exception(cls, pe):
        """
        internal factory method to simplify creating one type of ParseException 
        from another - avoids having __init__ signature conflicts among subclasses
        """
        return cls(pe.pstr, pe.loc, pe.msg, pe.parserElement)

    def __getattr__(self, aname):
        """supported attributes by name are:
            - lineno - returns the line number of the exception text
            - col - returns the column number of the exception text
            - line - returns the line containing the exception text
        """
        if aname == 'lineno':
            return lineno(self.loc, self.pstr)
        if aname in ('col', 'column'):
            return col(self.loc, self.pstr)
        if aname == 'line':
            return line(self.loc, self.pstr)
        raise AttributeError(aname)

    def __str__(self):
        return '%s (at char %d), (line:%d, col:%d)' % (
         self.msg, self.loc, self.lineno, self.column)

    def __repr__(self):
        return _ustr(self)

    def markInputline(self, markerString='>!<'):
        """Extracts the exception line from the input string, and marks
           the location of the exception with a special symbol.
        """
        line_str = self.line
        line_column = self.column - 1
        if markerString:
            line_str = ''.join((line_str[:line_column],
             markerString, line_str[line_column:]))
        return line_str.strip()

    def __dir__(self):
        return 'lineno col line'.split() + dir(type(self))


class ParseException(ParseBaseException):
    __doc__ = '\n    Exception thrown when parse expressions don\'t match class;\n    supported attributes by name are:\n     - lineno - returns the line number of the exception text\n     - col - returns the column number of the exception text\n     - line - returns the line containing the exception text\n        \n    Example::\n        try:\n            Word(nums).setName("integer").parseString("ABC")\n        except ParseException as pe:\n            print(pe)\n            print("column: {}".format(pe.col))\n            \n    prints::\n       Expected integer (at char 0), (line:1, col:1)\n        column: 1\n    '


class ParseFatalException(ParseBaseException):
    __doc__ = 'user-throwable exception thrown when inconsistent parse content\n       is found; stops all parsing immediately'


class ParseSyntaxException(ParseFatalException):
    __doc__ = "just like L{ParseFatalException}, but thrown internally when an\n       L{ErrorStop<And._ErrorStop>} ('-' operator) indicates that parsing is to stop \n       immediately because an unbacktrackable syntax error has been found"


class RecursiveGrammarException(Exception):
    __doc__ = 'exception thrown by L{ParserElement.validate} if the grammar could be improperly recursive'

    def __init__(self, parseElementList):
        self.parseElementTrace = parseElementList

    def __str__(self):
        return 'RecursiveGrammarException: %s' % self.parseElementTrace


class _ParseResultsWithOffset(object):

    def __init__(self, p1, p2):
        self.tup = (
         p1, p2)

    def __getitem__(self, i):
        return self.tup[i]

    def __repr__(self):
        return repr(self.tup[0])

    def setOffset(self, i):
        self.tup = (self.tup[0], i)


class ParseResults(object):
    __doc__ = '\n    Structured parse results, to provide multiple means of access to the parsed data:\n       - as a list (C{len(results)})\n       - by list index (C{results[0], results[1]}, etc.)\n       - by attribute (C{results.<resultsName>} - see L{ParserElement.setResultsName})\n\n    Example::\n        integer = Word(nums)\n        date_str = (integer.setResultsName("year") + \'/\' \n                        + integer.setResultsName("month") + \'/\' \n                        + integer.setResultsName("day"))\n        # equivalent form:\n        # date_str = integer("year") + \'/\' + integer("month") + \'/\' + integer("day")\n\n        # parseString returns a ParseResults object\n        result = date_str.parseString("1999/12/31")\n\n        def test(s, fn=repr):\n            print("%s -> %s" % (s, fn(eval(s))))\n        test("list(result)")\n        test("result[0]")\n        test("result[\'month\']")\n        test("result.day")\n        test("\'month\' in result")\n        test("\'minutes\' in result")\n        test("result.dump()", str)\n    prints::\n        list(result) -> [\'1999\', \'/\', \'12\', \'/\', \'31\']\n        result[0] -> \'1999\'\n        result[\'month\'] -> \'12\'\n        result.day -> \'31\'\n        \'month\' in result -> True\n        \'minutes\' in result -> False\n        result.dump() -> [\'1999\', \'/\', \'12\', \'/\', \'31\']\n        - day: 31\n        - month: 12\n        - year: 1999\n    '

    def __new__(cls, toklist=None, name=None, asList=True, modal=True):
        if isinstance(toklist, cls):
            return toklist
        retobj = object.__new__(cls)
        retobj._ParseResults__doinit = True
        return retobj

    def __init__(self, toklist=None, name=None, asList=True, modal=True, isinstance=isinstance):
        if self._ParseResults__doinit:
            self._ParseResults__doinit = False
            self._ParseResults__name = None
            self._ParseResults__parent = None
            self._ParseResults__accumNames = {}
            self._ParseResults__asList = asList
            self._ParseResults__modal = modal
            if toklist is None:
                toklist = []
            elif isinstance(toklist, list):
                self._ParseResults__toklist = toklist[:]
            else:
                if isinstance(toklist, _generatorType):
                    self._ParseResults__toklist = list(toklist)
                else:
                    self._ParseResults__toklist = [
                     toklist]
            self._ParseResults__tokdict = dict()
        if name is not None and name:
            if not modal:
                self._ParseResults__accumNames[name] = 0
            else:
                if isinstance(name, int):
                    name = _ustr(name)
                self._ParseResults__name = name
                if not (isinstance(toklist, (type(None), basestring, list)) and toklist in (None, '', [])):
                    if isinstance(toklist, basestring):
                        toklist = [
                         toklist]
                    if asList:
                        if isinstance(toklist, ParseResults):
                            self[name] = _ParseResultsWithOffset(toklist.copy(), 0)
                else:
                    self[name] = _ParseResultsWithOffset(ParseResults(toklist[0]), 0)
            self[name]._ParseResults__name = name
        else:
            try:
                self[name] = toklist[0]
            except (KeyError, TypeError, IndexError):
                self[name] = toklist

    def __getitem__(self, i):
        if isinstance(i, (int, slice)):
            return self._ParseResults__toklist[i]
        if i not in self._ParseResults__accumNames:
            return self._ParseResults__tokdict[i][(-1)][0]
        return ParseResults([v[0] for v in self._ParseResults__tokdict[i]])

    def __setitem__(self, k, v, isinstance=isinstance):
        if isinstance(v, _ParseResultsWithOffset):
            self._ParseResults__tokdict[k] = self._ParseResults__tokdict.get(k, list()) + [v]
            sub = v[0]
        else:
            if isinstance(k, (int, slice)):
                self._ParseResults__toklist[k] = v
                sub = v
            else:
                self._ParseResults__tokdict[k] = self._ParseResults__tokdict.get(k, list()) + [_ParseResultsWithOffset(v, 0)]
                sub = v
        if isinstance(sub, ParseResults):
            sub._ParseResults__parent = wkref(self)

    def __delitem__(self, i):
        if isinstance(i, (int, slice)):
            mylen = len(self._ParseResults__toklist)
            del self._ParseResults__toklist[i]
            if isinstance(i, int):
                if i < 0:
                    i += mylen
                i = slice(i, i + 1)
            removed = list(range(*i.indices(mylen)))
            removed.reverse()
            for name, occurrences in self._ParseResults__tokdict.items():
                for j in removed:
                    for k, (value, position) in enumerate(occurrences):
                        occurrences[k] = _ParseResultsWithOffset(value, position - (position > j))

        else:
            del self._ParseResults__tokdict[i]

    def __contains__(self, k):
        return k in self._ParseResults__tokdict

    def __len__(self):
        return len(self._ParseResults__toklist)

    def __bool__(self):
        return not not self._ParseResults__toklist

    __nonzero__ = __bool__

    def __iter__(self):
        return iter(self._ParseResults__toklist)

    def __reversed__(self):
        return iter(self._ParseResults__toklist[::-1])

    def _iterkeys(self):
        if hasattr(self._ParseResults__tokdict, 'iterkeys'):
            return self._ParseResults__tokdict.iterkeys()
        return iter(self._ParseResults__tokdict)

    def _itervalues(self):
        return (self[k] for k in self._iterkeys())

    def _iteritems(self):
        return ((k, self[k]) for k in self._iterkeys())

    if PY_3:
        keys = _iterkeys
        values = _itervalues
        items = _iteritems
    else:
        iterkeys = _iterkeys
        itervalues = _itervalues
        iteritems = _iteritems

        def keys(self):
            """Returns all named result keys (as a list in Python 2.x, as an iterator in Python 3.x)."""
            return list(self.iterkeys())

        def values(self):
            """Returns all named result values (as a list in Python 2.x, as an iterator in Python 3.x)."""
            return list(self.itervalues())

        def items(self):
            """Returns all named result key-values (as a list of tuples in Python 2.x, as an iterator in Python 3.x)."""
            return list(self.iteritems())

    def haskeys(self):
        """Since keys() returns an iterator, this method is helpful in bypassing
           code that looks for the existence of any defined results names."""
        return bool(self._ParseResults__tokdict)

    def pop(self, *args, **kwargs):
        """
        Removes and returns item at specified index (default=C{last}).
        Supports both C{list} and C{dict} semantics for C{pop()}. If passed no
        argument or an integer argument, it will use C{list} semantics
        and pop tokens from the list of parsed tokens. If passed a 
        non-integer argument (most likely a string), it will use C{dict}
        semantics and pop the corresponding value from any defined 
        results names. A second default return value argument is 
        supported, just as in C{dict.pop()}.

        Example::
            def remove_first(tokens):
                tokens.pop(0)
            print(OneOrMore(Word(nums)).parseString("0 123 321")) # -> ['0', '123', '321']
            print(OneOrMore(Word(nums)).addParseAction(remove_first).parseString("0 123 321")) # -> ['123', '321']

            label = Word(alphas)
            patt = label("LABEL") + OneOrMore(Word(nums))
            print(patt.parseString("AAB 123 321").dump())

            # Use pop() in a parse action to remove named result (note that corresponding value is not
            # removed from list form of results)
            def remove_LABEL(tokens):
                tokens.pop("LABEL")
                return tokens
            patt.addParseAction(remove_LABEL)
            print(patt.parseString("AAB 123 321").dump())
        prints::
            ['AAB', '123', '321']
            - LABEL: AAB

            ['AAB', '123', '321']
        """
        if not args:
            args = [
             -1]
        for k, v in kwargs.items():
            if k == 'default':
                args = (
                 args[0], v)
            else:
                raise TypeError("pop() got an unexpected keyword argument '%s'" % k)

        if isinstance(args[0], int) or len(args) == 1 or args[0] in self:
            index = args[0]
            ret = self[index]
            del self[index]
            return ret
        defaultvalue = args[1]
        return defaultvalue

    def get(self, key, defaultValue=None):
        """
        Returns named result matching the given key, or if there is no
        such name, then returns the given C{defaultValue} or C{None} if no
        C{defaultValue} is specified.

        Similar to C{dict.get()}.
        
        Example::
            integer = Word(nums)
            date_str = integer("year") + '/' + integer("month") + '/' + integer("day")           

            result = date_str.parseString("1999/12/31")
            print(result.get("year")) # -> '1999'
            print(result.get("hour", "not specified")) # -> 'not specified'
            print(result.get("hour")) # -> None
        """
        if key in self:
            return self[key]
        return defaultValue

    def insert(self, index, insStr):
        """
        Inserts new element at location index in the list of parsed tokens.
        
        Similar to C{list.insert()}.

        Example::
            print(OneOrMore(Word(nums)).parseString("0 123 321")) # -> ['0', '123', '321']

            # use a parse action to insert the parse location in the front of the parsed results
            def insert_locn(locn, tokens):
                tokens.insert(0, locn)
            print(OneOrMore(Word(nums)).addParseAction(insert_locn).parseString("0 123 321")) # -> [0, '0', '123', '321']
        """
        self._ParseResults__toklist.insert(index, insStr)
        for name, occurrences in self._ParseResults__tokdict.items():
            for k, (value, position) in enumerate(occurrences):
                occurrences[k] = _ParseResultsWithOffset(value, position + (position > index))

    def append(self, item):
        """
        Add single element to end of ParseResults list of elements.

        Example::
            print(OneOrMore(Word(nums)).parseString("0 123 321")) # -> ['0', '123', '321']
            
            # use a parse action to compute the sum of the parsed integers, and add it to the end
            def append_sum(tokens):
                tokens.append(sum(map(int, tokens)))
            print(OneOrMore(Word(nums)).addParseAction(append_sum).parseString("0 123 321")) # -> ['0', '123', '321', 444]
        """
        self._ParseResults__toklist.append(item)

    def extend(self, itemseq):
        """
        Add sequence of elements to end of ParseResults list of elements.

        Example::
            patt = OneOrMore(Word(alphas))
            
            # use a parse action to append the reverse of the matched strings, to make a palindrome
            def make_palindrome(tokens):
                tokens.extend(reversed([t[::-1] for t in tokens]))
                return ''.join(tokens)
            print(patt.addParseAction(make_palindrome).parseString("lskdj sdlkjf lksd")) # -> 'lskdjsdlkjflksddsklfjkldsjdksl'
        """
        if isinstance(itemseq, ParseResults):
            self += itemseq
        else:
            self._ParseResults__toklist.extend(itemseq)

    def clear(self):
        """
        Clear all elements and results names.
        """
        del self._ParseResults__toklist[:]
        self._ParseResults__tokdict.clear()

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            return ''

        if name in self._ParseResults__tokdict:
            if name not in self._ParseResults__accumNames:
                return self._ParseResults__tokdict[name][(-1)][0]
            return ParseResults([v[0] for v in self._ParseResults__tokdict[name]])
        else:
            return ''

    def __add__(self, other):
        ret = self.copy()
        ret += other
        return ret

    def __iadd__(self, other):
        if other._ParseResults__tokdict:
            offset = len(self._ParseResults__toklist)
            addoffset = lambda a:             if a < 0:
offset # Avoid dead code: a + offset
            otheritems = other._ParseResults__tokdict.items()
            otherdictitems = [(k, _ParseResultsWithOffset(v[0], addoffset(v[1]))) for k, vlist in otheritems for v in vlist]
            for k, v in otherdictitems:
                self[k] = v
                if isinstance(v[0], ParseResults):
                    v[0]._ParseResults__parent = wkref(self)

        self._ParseResults__toklist += other._ParseResults__toklist
        self._ParseResults__accumNames.update(other._ParseResults__accumNames)
        return self

    def __radd__(self, other):
        if isinstance(other, int):
            if other == 0:
                return self.copy()
        return other + self

    def __repr__(self):
        return '(%s, %s)' % (repr(self._ParseResults__toklist), repr(self._ParseResults__tokdict))

    def __str__(self):
        return '[' + ', '.join(((_ustr(i) if isinstance(i, ParseResults) else repr(i)) for i in self._ParseResults__toklist)) + ']'

    def _asStringList(self, sep=''):
        out = []
        for item in self._ParseResults__toklist:
            if out:
                if sep:
                    out.append(sep)
            if isinstance(item, ParseResults):
                out += item._asStringList()
            else:
                out.append(_ustr(item))

        return out

    def asList(self):
        """
        Returns the parse results as a nested list of matching tokens, all converted to strings.

        Example::
            patt = OneOrMore(Word(alphas))
            result = patt.parseString("sldkj lsdkj sldkj")
            # even though the result prints in string-like form, it is actually a pyparsing ParseResults
            print(type(result), result) # -> <class 'pyparsing.ParseResults'> ['sldkj', 'lsdkj', 'sldkj']
            
            # Use asList() to create an actual list
            result_list = result.asList()
            print(type(result_list), result_list) # -> <class 'list'> ['sldkj', 'lsdkj', 'sldkj']
        """
        return [res.asList() if isinstance(res, ParseResults) else res for res in self._ParseResults__toklist]

    def asDict(self):
        """
        Returns the named parse results as a nested dictionary.

        Example::
            integer = Word(nums)
            date_str = integer("year") + '/' + integer("month") + '/' + integer("day")
            
            result = date_str.parseString('12/31/1999')
            print(type(result), repr(result)) # -> <class 'pyparsing.ParseResults'> (['12', '/', '31', '/', '1999'], {'day': [('1999', 4)], 'year': [('12', 0)], 'month': [('31', 2)]})
            
            result_dict = result.asDict()
            print(type(result_dict), repr(result_dict)) # -> <class 'dict'> {'day': '1999', 'year': '12', 'month': '31'}

            # even though a ParseResults supports dict-like access, sometime you just need to have a dict
            import json
            print(json.dumps(result)) # -> Exception: TypeError: ... is not JSON serializable
            print(json.dumps(result.asDict())) # -> {"month": "31", "day": "1999", "year": "12"}
        """
        if PY_3:
            item_fn = self.items
        else:
            item_fn = self.iteritems

        def toItem(obj):
            if isinstance(obj, ParseResults):
                if obj.haskeys():
                    return obj.asDict()
                return [toItem(v) for v in obj]
            else:
                return obj

        return dict(((k, toItem(v)) for k, v in item_fn()))

    def copy(self):
        """
        Returns a new copy of a C{ParseResults} object.
        """
        ret = ParseResults(self._ParseResults__toklist)
        ret._ParseResults__tokdict = self._ParseResults__tokdict.copy()
        ret._ParseResults__parent = self._ParseResults__parent
        ret._ParseResults__accumNames.update(self._ParseResults__accumNames)
        ret._ParseResults__name = self._ParseResults__name
        return ret

    def asXML(self, doctag=None, namedItemsOnly=False, indent='', formatted=True):
        """
        (Deprecated) Returns the parse results as XML. Tags are created for tokens and lists that have defined results names.
        """
        nl = '\n'
        out = []
        namedItems = dict(((v[1], k) for k, vlist in self._ParseResults__tokdict.items() for v in vlist))
        nextLevelIndent = indent + '  '
        if not formatted:
            indent = ''
            nextLevelIndent = ''
            nl = ''
        else:
            selfTag = None
            if doctag is not None:
                selfTag = doctag
            else:
                if self._ParseResults__name:
                    selfTag = self._ParseResults__name
        if not selfTag:
            if namedItemsOnly:
                return ''
            selfTag = 'ITEM'
        out += [nl, indent, '<', selfTag, '>']
        for i, res in enumerate(self._ParseResults__toklist):
            if isinstance(res, ParseResults):
                if i in namedItems:
                    out += [
                     res.asXML(namedItems[i], namedItemsOnly and doctag is None, nextLevelIndent, formatted)]
                else:
                    out += [
                     res.asXML(None, namedItemsOnly and doctag is None, nextLevelIndent, formatted)]
            else:
                resTag = None
                if i in namedItems:
                    resTag = namedItems[i]
                if not resTag:
                    if namedItemsOnly:
                        continue
                    else:
                        resTag = 'ITEM'
                xmlBodyText = _xml_escape(_ustr(res))
                out += [nl, nextLevelIndent, '<', resTag, '>',
                 xmlBodyText,
                 '</', resTag, '>']

        out += [nl, indent, '</', selfTag, '>']
        return ''.join(out)

    def __lookup(self, sub):
        for k, vlist in self._ParseResults__tokdict.items():
            for v, loc in vlist:
                if sub is v:
                    return k

    def getName(self):
        r"""
        Returns the results name for this token expression. Useful when several 
        different expressions might match at a particular location.

        Example::
            integer = Word(nums)
            ssn_expr = Regex(r"\d\d\d-\d\d-\d\d\d\d")
            house_number_expr = Suppress('#') + Word(nums, alphanums)
            user_data = (Group(house_number_expr)("house_number") 
                        | Group(ssn_expr)("ssn")
                        | Group(integer)("age"))
            user_info = OneOrMore(user_data)
            
            result = user_info.parseString("22 111-22-3333 #221B")
            for item in result:
                print(item.getName(), ':', item[0])
        prints::
            age : 22
            ssn : 111-22-3333
            house_number : 221B
        """
        if self._ParseResults__name:
            return self._ParseResults__name
            if self._ParseResults__parent:
                par = self._ParseResults__parent()
                if par:
                    return par._ParseResults__lookup(self)
                return
        else:
            if len(self) == 1:
                if len(self._ParseResults__tokdict) == 1:
                    if next(iter(self._ParseResults__tokdict.values()))[0][1] in (0,
                                                                                  -1):
                        return next(iter(self._ParseResults__tokdict.keys()))
            return

    def dump(self, indent='', depth=0, full=True):
        """
        Diagnostic method for listing out the contents of a C{ParseResults}.
        Accepts an optional C{indent} argument so that this string can be embedded
        in a nested display of other data.

        Example::
            integer = Word(nums)
            date_str = integer("year") + '/' + integer("month") + '/' + integer("day")
            
            result = date_str.parseString('12/31/1999')
            print(result.dump())
        prints::
            ['12', '/', '31', '/', '1999']
            - day: 1999
            - month: 31
            - year: 12
        """
        out = []
        NL = '\n'
        out.append(indent + _ustr(self.asList()))
        if full:
            if self.haskeys():
                items = sorted(((str(k), v) for k, v in self.items()))
                for k, v in items:
                    if out:
                        out.append(NL)
                    out.append('%s%s- %s: ' % (indent, '  ' * depth, k))
                    if isinstance(v, ParseResults):
                        if v:
                            out.append(v.dump(indent, depth + 1))
                        else:
                            out.append(_ustr(v))
                    else:
                        out.append(repr(v))

            else:
                if any((isinstance(vv, ParseResults) for vv in self)):
                    v = self
                    for i, vv in enumerate(v):
                        if isinstance(vv, ParseResults):
                            out.append('\n%s%s[%d]:\n%s%s%s' % (indent, '  ' * depth, i, indent, '  ' * (depth + 1), vv.dump(indent, depth + 1)))
                        else:
                            out.append('\n%s%s[%d]:\n%s%s%s' % (indent, '  ' * depth, i, indent, '  ' * (depth + 1), _ustr(vv)))

        return ''.join(out)

    def pprint(self, *args, **kwargs):
        """
        Pretty-printer for parsed results as a list, using the C{pprint} module.
        Accepts additional positional or keyword args as defined for the 
        C{pprint.pprint} method. (U{http://docs.python.org/3/library/pprint.html#pprint.pprint})

        Example::
            ident = Word(alphas, alphanums)
            num = Word(nums)
            func = Forward()
            term = ident | num | Group('(' + func + ')')
            func <<= ident + Group(Optional(delimitedList(term)))
            result = func.parseString("fna a,b,(fnb c,d,200),100")
            result.pprint(width=40)
        prints::
            ['fna',
             ['a',
              'b',
              ['(', 'fnb', ['c', 'd', '200'], ')'],
              '100']]
        """
        (pprint.pprint)(self.asList(), *args, **kwargs)

    def __getstate__(self):
        return (
         self._ParseResults__toklist,
         (
          self._ParseResults__tokdict.copy(),
          self._ParseResults__parent is not None and self._ParseResults__parent() or None,
          self._ParseResults__accumNames,
          self._ParseResults__name))

    def __setstate__(self, state):
        self._ParseResults__toklist = state[0]
        self._ParseResults__tokdict, par, inAccumNames, self._ParseResults__name = state[1]
        self._ParseResults__accumNames = {}
        self._ParseResults__accumNames.update(inAccumNames)
        if par is not None:
            self._ParseResults__parent = wkref(par)
        else:
            self._ParseResults__parent = None

    def __getnewargs__(self):
        return (self._ParseResults__toklist, self._ParseResults__name, self._ParseResults__asList, self._ParseResults__modal)

    def __dir__(self):
        return dir(type(self)) + list(self.keys())


MutableMapping.register(ParseResults)

def col(loc, strg):
    """Returns current column within a string, counting newlines as line separators.
   The first column is number 1.

   Note: the default parsing behavior is to expand tabs in the input string
   before starting the parsing process.  See L{I{ParserElement.parseString}<ParserElement.parseString>} for more information
   on parsing strings containing C{<TAB>}s, and suggested methods to maintain a
   consistent view of the parsed string, the parse location, and line and column
   positions within the parsed string.
   """
    s = strg
    if 0 < loc < len(s):
        if s[(loc - 1)] == '\n':
            return 1
    return loc - s.rfind('\n', 0, loc)


def lineno(loc, strg):
    """Returns current line number within a string, counting newlines as line separators.
   The first line is number 1.

   Note: the default parsing behavior is to expand tabs in the input string
   before starting the parsing process.  See L{I{ParserElement.parseString}<ParserElement.parseString>} for more information
   on parsing strings containing C{<TAB>}s, and suggested methods to maintain a
   consistent view of the parsed string, the parse location, and line and column
   positions within the parsed string.
   """
    return strg.count('\n', 0, loc) + 1


def line(loc, strg):
    """Returns the line of text containing loc within a string, counting newlines as line separators.
       """
    lastCR = strg.rfind('\n', 0, loc)
    nextCR = strg.find('\n', loc)
    if nextCR >= 0:
        return strg[lastCR + 1:nextCR]
    return strg[lastCR + 1:]


def _defaultStartDebugAction(instring, loc, expr):
    print('Match ' + _ustr(expr) + ' at loc ' + _ustr(loc) + '(%d,%d)' % (lineno(loc, instring), col(loc, instring)))


def _defaultSuccessDebugAction(instring, startloc, endloc, expr, toks):
    print('Matched ' + _ustr(expr) + ' -> ' + str(toks.asList()))


def _defaultExceptionDebugAction(instring, loc, expr, exc):
    print('Exception raised:' + _ustr(exc))


def nullDebugAction(*args):
    """'Do-nothing' debug action, to suppress debugging output during parsing."""
    pass


def _trim_arity(func, maxargs=2):
    if func in singleArgBuiltins:
        return lambda s, l, t: func(t)
    limit = [
     0]
    foundArity = [False]
    if system_version[:2] >= (3, 5):

        def extract_stack(limit=0):
            offset = -3 if system_version == (3, 5, 0) else -2
            frame_summary = traceback.extract_stack(limit=(-offset + limit - 1))[offset]
            return [frame_summary[:2]]

        def extract_tb(tb, limit=0):
            frames = traceback.extract_tb(tb, limit=limit)
            frame_summary = frames[(-1)]
            return [frame_summary[:2]]

    else:
        extract_stack = traceback.extract_stack
        extract_tb = traceback.extract_tb
    LINE_DIFF = 6
    this_line = extract_stack(limit=2)[(-1)]
    pa_call_line_synth = (this_line[0], this_line[1] + LINE_DIFF)

    def wrapper(*args):
        while True:
            try:
                ret = func(*args[limit[0]:])
                foundArity[0] = True
                return ret
            except TypeError:
                if foundArity[0]:
                    raise
                else:
                    try:
                        tb = sys.exc_info()[(-1)]
                        if not extract_tb(tb, limit=2)[(-1)][:2] == pa_call_line_synth:
                            raise
                    finally:
                        del tb

                if limit[0] <= maxargs:
                    limit[0] += 1
                    continue
                raise

    func_name = '<parse action>'
    try:
        func_name = getattr(func, '__name__', getattr(func, '__class__').__name__)
    except Exception:
        func_name = str(func)

    wrapper.__name__ = func_name
    return wrapper


class ParserElement(object):
    __doc__ = 'Abstract base level parser element class.'
    DEFAULT_WHITE_CHARS = ' \n\t\r'
    verbose_stacktrace = False

    @staticmethod
    def setDefaultWhitespaceChars(chars):
        r"""
        Overrides the default whitespace chars

        Example::
            # default whitespace chars are space, <TAB> and newline
            OneOrMore(Word(alphas)).parseString("abc def\nghi jkl")  # -> ['abc', 'def', 'ghi', 'jkl']
            
            # change to just treat newline as significant
            ParserElement.setDefaultWhitespaceChars(" \t")
            OneOrMore(Word(alphas)).parseString("abc def\nghi jkl")  # -> ['abc', 'def']
        """
        ParserElement.DEFAULT_WHITE_CHARS = chars

    @staticmethod
    def inlineLiteralsUsing(cls):
        """
        Set class to be used for inclusion of string literals into a parser.
        
        Example::
            # default literal class used is Literal
            integer = Word(nums)
            date_str = integer("year") + '/' + integer("month") + '/' + integer("day")           

            date_str.parseString("1999/12/31")  # -> ['1999', '/', '12', '/', '31']

            # change to Suppress
            ParserElement.inlineLiteralsUsing(Suppress)
            date_str = integer("year") + '/' + integer("month") + '/' + integer("day")           

            date_str.parseString("1999/12/31")  # -> ['1999', '12', '31']
        """
        ParserElement._literalStringClass = cls

    def __init__(self, savelist=False):
        self.parseAction = list()
        self.failAction = None
        self.strRepr = None
        self.resultsName = None
        self.saveAsList = savelist
        self.skipWhitespace = True
        self.whiteChars = ParserElement.DEFAULT_WHITE_CHARS
        self.copyDefaultWhiteChars = True
        self.mayReturnEmpty = False
        self.keepTabs = False
        self.ignoreExprs = list()
        self.debug = False
        self.streamlined = False
        self.mayIndexError = True
        self.errmsg = ''
        self.modalResults = True
        self.debugActions = (None, None, None)
        self.re = None
        self.callPreparse = True
        self.callDuringTry = False

    def copy(self):
        """
        Make a copy of this C{ParserElement}.  Useful for defining different parse actions
        for the same parsing pattern, using copies of the original parse element.
        
        Example::
            integer = Word(nums).setParseAction(lambda toks: int(toks[0]))
            integerK = integer.copy().addParseAction(lambda toks: toks[0]*1024) + Suppress("K")
            integerM = integer.copy().addParseAction(lambda toks: toks[0]*1024*1024) + Suppress("M")
            
            print(OneOrMore(integerK | integerM | integer).parseString("5K 100 640K 256M"))
        prints::
            [5120, 100, 655360, 268435456]
        Equivalent form of C{expr.copy()} is just C{expr()}::
            integerM = integer().addParseAction(lambda toks: toks[0]*1024*1024) + Suppress("M")
        """
        cpy = copy.copy(self)
        cpy.parseAction = self.parseAction[:]
        cpy.ignoreExprs = self.ignoreExprs[:]
        if self.copyDefaultWhiteChars:
            cpy.whiteChars = ParserElement.DEFAULT_WHITE_CHARS
        return cpy

    def setName(self, name):
        """
        Define name for this expression, makes debugging and exception messages clearer.
        
        Example::
            Word(nums).parseString("ABC")  # -> Exception: Expected W:(0123...) (at char 0), (line:1, col:1)
            Word(nums).setName("integer").parseString("ABC")  # -> Exception: Expected integer (at char 0), (line:1, col:1)
        """
        self.name = name
        self.errmsg = 'Expected ' + self.name
        if hasattr(self, 'exception'):
            self.exception.msg = self.errmsg
        return self

    def setResultsName(self, name, listAllMatches=False):
        """
        Define name for referencing matching tokens as a nested attribute
        of the returned parse results.
        NOTE: this returns a *copy* of the original C{ParserElement} object;
        this is so that the client can define a basic element, such as an
        integer, and reference it in multiple places with different names.

        You can also set results names using the abbreviated syntax,
        C{expr("name")} in place of C{expr.setResultsName("name")} - 
        see L{I{__call__}<__call__>}.

        Example::
            date_str = (integer.setResultsName("year") + '/' 
                        + integer.setResultsName("month") + '/' 
                        + integer.setResultsName("day"))

            # equivalent form:
            date_str = integer("year") + '/' + integer("month") + '/' + integer("day")
        """
        newself = self.copy()
        if name.endswith('*'):
            name = name[:-1]
            listAllMatches = True
        newself.resultsName = name
        newself.modalResults = not listAllMatches
        return newself

    def setBreak(self, breakFlag=True):
        """Method to invoke the Python pdb debugger when this element is
           about to be parsed. Set C{breakFlag} to True to enable, False to
           disable.
        """
        if breakFlag:
            _parseMethod = self._parse

            def breaker(instring, loc, doActions=True, callPreParse=True):
                import pdb
                pdb.set_trace()
                return _parseMethod(instring, loc, doActions, callPreParse)

            breaker._originalParseMethod = _parseMethod
            self._parse = breaker
        else:
            if hasattr(self._parse, '_originalParseMethod'):
                self._parse = self._parse._originalParseMethod
        return self

    def setParseAction(self, *fns, **kwargs):
        """
        Define one or more actions to perform when successfully matching parse element definition.
        Parse action fn is a callable method with 0-3 arguments, called as C{fn(s,loc,toks)},
        C{fn(loc,toks)}, C{fn(toks)}, or just C{fn()}, where:
         - s   = the original string being parsed (see note below)
         - loc = the location of the matching substring
         - toks = a list of the matched tokens, packaged as a C{L{ParseResults}} object
        If the functions in fns modify the tokens, they can return them as the return
        value from fn, and the modified list of tokens will replace the original.
        Otherwise, fn does not need to return any value.

        Optional keyword arguments:
         - callDuringTry = (default=C{False}) indicate if parse action should be run during lookaheads and alternate testing

        Note: the default parsing behavior is to expand tabs in the input string
        before starting the parsing process.  See L{I{parseString}<parseString>} for more information
        on parsing strings containing C{<TAB>}s, and suggested methods to maintain a
        consistent view of the parsed string, the parse location, and line and column
        positions within the parsed string.
        
        Example::
            integer = Word(nums)
            date_str = integer + '/' + integer + '/' + integer

            date_str.parseString("1999/12/31")  # -> ['1999', '/', '12', '/', '31']

            # use parse action to convert to ints at parse time
            integer = Word(nums).setParseAction(lambda toks: int(toks[0]))
            date_str = integer + '/' + integer + '/' + integer

            # note that integer fields are now ints, not strings
            date_str.parseString("1999/12/31")  # -> [1999, '/', 12, '/', 31]
        """
        self.parseAction = list(map(_trim_arity, list(fns)))
        self.callDuringTry = kwargs.get('callDuringTry', False)
        return self

    def addParseAction(self, *fns, **kwargs):
        """
        Add one or more parse actions to expression's list of parse actions. See L{I{setParseAction}<setParseAction>}.
        
        See examples in L{I{copy}<copy>}.
        """
        self.parseAction += list(map(_trim_arity, list(fns)))
        self.callDuringTry = self.callDuringTry or kwargs.get('callDuringTry', False)
        return self

    def addCondition(self, *fns, **kwargs):
        """Add a boolean predicate function to expression's list of parse actions. See 
        L{I{setParseAction}<setParseAction>} for function call signatures. Unlike C{setParseAction}, 
        functions passed to C{addCondition} need to return boolean success/fail of the condition.

        Optional keyword arguments:
         - message = define a custom message to be used in the raised exception
         - fatal   = if True, will raise ParseFatalException to stop parsing immediately; otherwise will raise ParseException
         
        Example::
            integer = Word(nums).setParseAction(lambda toks: int(toks[0]))
            year_int = integer.copy()
            year_int.addCondition(lambda toks: toks[0] >= 2000, message="Only support years 2000 and later")
            date_str = year_int + '/' + integer + '/' + integer

            result = date_str.parseString("1999/12/31")  # -> Exception: Only support years 2000 and later (at char 0), (line:1, col:1)
        """
        msg = kwargs.get('message', 'failed user-defined condition')
        exc_type = ParseFatalException if kwargs.get('fatal', False) else ParseException
        for fn in fns:

            def pa(s, l, t):
                if not bool(_trim_arity(fn)(s, l, t)):
                    raise exc_type(s, l, msg)

            self.parseAction.append(pa)

        self.callDuringTry = self.callDuringTry or kwargs.get('callDuringTry', False)
        return self

    def setFailAction(self, fn):
        """Define action to perform if parsing fails at this expression.
           Fail acton fn is a callable function that takes the arguments
           C{fn(s,loc,expr,err)} where:
            - s = string being parsed
            - loc = location where expression match was attempted and failed
            - expr = the parse expression that failed
            - err = the exception thrown
           The function returns no value.  It may throw C{L{ParseFatalException}}
           if it is desired to stop parsing immediately."""
        self.failAction = fn
        return self

    def _skipIgnorables(self, instring, loc):
        exprsFound = True
        while exprsFound:
            exprsFound = False
            for e in self.ignoreExprs:
                try:
                    while True:
                        loc, dummy = e._parse(instring, loc)
                        exprsFound = True

                except ParseException:
                    pass

        return loc

    def preParse(self, instring, loc):
        if self.ignoreExprs:
            loc = self._skipIgnorables(instring, loc)
        if self.skipWhitespace:
            wt = self.whiteChars
            instrlen = len(instring)
            while loc < instrlen and instring[loc] in wt:
                loc += 1

        return loc

    def parseImpl(self, instring, loc, doActions=True):
        return (
         loc, [])

    def postParse(self, instring, loc, tokenlist):
        return tokenlist

    def _parseNoCache(self, instring, loc, doActions=True, callPreParse=True):
        debugging = self.debug
        if debugging or self.failAction:
            if self.debugActions[0]:
                self.debugActions[0](instring, loc, self)
            else:
                if callPreParse and self.callPreparse:
                    preloc = self.preParse(instring, loc)
                else:
                    preloc = loc
                tokensStart = preloc
                try:
                    try:
                        loc, tokens = self.parseImpl(instring, preloc, doActions)
                    except IndexError:
                        raise ParseException(instring, len(instring), self.errmsg, self)

                except ParseBaseException as err:
                    try:
                        if self.debugActions[2]:
                            self.debugActions[2](instring, tokensStart, self, err)
                        if self.failAction:
                            self.failAction(instring, tokensStart, self, err)
                        raise
                    finally:
                        err = None
                        del err

        else:
            if callPreParse:
                if self.callPreparse:
                    preloc = self.preParse(instring, loc)
                else:
                    preloc = loc
                tokensStart = preloc
                if self.mayIndexError or preloc >= len(instring):
                    try:
                        loc, tokens = self.parseImpl(instring, preloc, doActions)
                    except IndexError:
                        raise ParseException(instring, len(instring), self.errmsg, self)

                else:
                    loc, tokens = self.parseImpl(instring, preloc, doActions)
            else:
                tokens = self.postParse(instring, loc, tokens)
                retTokens = ParseResults(tokens, (self.resultsName), asList=(self.saveAsList), modal=(self.modalResults))
                if self.parseAction and not doActions:
                    if self.callDuringTry:
                        if debugging:
                            try:
                                for fn in self.parseAction:
                                    tokens = fn(instring, tokensStart, retTokens)
                                    if tokens is not None:
                                        retTokens = ParseResults(tokens, (self.resultsName),
                                          asList=(self.saveAsList and isinstance(tokens, (ParseResults, list))),
                                          modal=(self.modalResults))

                            except ParseBaseException as err:
                                try:
                                    if self.debugActions[2]:
                                        self.debugActions[2](instring, tokensStart, self, err)
                                    raise
                                finally:
                                    err = None
                                    del err

                        else:
                            for fn in self.parseAction:
                                tokens = fn(instring, tokensStart, retTokens)
                                if tokens is not None:
                                    retTokens = ParseResults(tokens, (self.resultsName),
                                      asList=(self.saveAsList and isinstance(tokens, (ParseResults, list))),
                                      modal=(self.modalResults))

            if debugging:
                if self.debugActions[1]:
                    self.debugActions[1](instring, tokensStart, loc, self, retTokens)
            return (
             loc, retTokens)

    def tryParse(self, instring, loc):
        try:
            return self._parse(instring, loc, doActions=False)[0]
        except ParseFatalException:
            raise ParseException(instring, loc, self.errmsg, self)

    def canParseNext(self, instring, loc):
        try:
            self.tryParse(instring, loc)
        except (ParseException, IndexError):
            return False
        else:
            return True

    class _UnboundedCache(object):

        def __init__(self):
            cache = {}
            self.not_in_cache = not_in_cache = object()

            def get(self, key):
                return cache.get(key, not_in_cache)

            def set(self, key, value):
                cache[key] = value

            def clear(self):
                cache.clear()

            def cache_len(self):
                return len(cache)

            self.get = types.MethodType(get, self)
            self.set = types.MethodType(set, self)
            self.clear = types.MethodType(clear, self)
            self.__len__ = types.MethodType(cache_len, self)

    if _OrderedDict is not None:

        class _FifoCache(object):

            def __init__(self, size):
                self.not_in_cache = not_in_cache = object()
                cache = _OrderedDict()

                def get(self, key):
                    return cache.get(key, not_in_cache)

                def set(self, key, value):
                    cache[key] = value
                    while len(cache) > size:
                        try:
                            cache.popitem(False)
                        except KeyError:
                            pass

                def clear(self):
                    cache.clear()

                def cache_len(self):
                    return len(cache)

                self.get = types.MethodType(get, self)
                self.set = types.MethodType(set, self)
                self.clear = types.MethodType(clear, self)
                self.__len__ = types.MethodType(cache_len, self)

    else:

        class _FifoCache(object):

            def __init__(self, size):
                self.not_in_cache = not_in_cache = object()
                cache = {}
                key_fifo = collections.deque([], size)

                def get(self, key):
                    return cache.get(key, not_in_cache)

                def set(self, key, value):
                    cache[key] = value
                    while len(key_fifo) > size:
                        cache.pop(key_fifo.popleft(), None)

                    key_fifo.append(key)

                def clear(self):
                    cache.clear()
                    key_fifo.clear()

                def cache_len(self):
                    return len(cache)

                self.get = types.MethodType(get, self)
                self.set = types.MethodType(set, self)
                self.clear = types.MethodType(clear, self)
                self.__len__ = types.MethodType(cache_len, self)

    packrat_cache = {}
    packrat_cache_lock = RLock()
    packrat_cache_stats = [0, 0]

    def _parseCache(self, instring, loc, doActions=True, callPreParse=True):
        HIT, MISS = (0, 1)
        lookup = (self, instring, loc, callPreParse, doActions)
        with ParserElement.packrat_cache_lock:
            cache = ParserElement.packrat_cache
            value = cache.get(lookup)
            if value is cache.not_in_cache:
                ParserElement.packrat_cache_stats[MISS] += 1
                try:
                    value = self._parseNoCache(instring, loc, doActions, callPreParse)
                except ParseBaseException as pe:
                    try:
                        cache.set(lookup, (pe.__class__)(*pe.args))
                        raise
                    finally:
                        pe = None
                        del pe

                else:
                    cache.set(lookup, (value[0], value[1].copy()))
                    return value
            else:
                ParserElement.packrat_cache_stats[HIT] += 1
                if isinstance(value, Exception):
                    raise value
                return (
                 value[0], value[1].copy())

    _parse = _parseNoCache

    @staticmethod
    def resetCache():
        ParserElement.packrat_cache.clear()
        ParserElement.packrat_cache_stats[:] = [0] * len(ParserElement.packrat_cache_stats)

    _packratEnabled = False

    @staticmethod
    def enablePackrat(cache_size_limit=128):
        """Enables "packrat" parsing, which adds memoizing to the parsing logic.
           Repeated parse attempts at the same string location (which happens
           often in many complex grammars) can immediately return a cached value,
           instead of re-executing parsing/validating code.  Memoizing is done of
           both valid results and parsing exceptions.
           
           Parameters:
            - cache_size_limit - (default=C{128}) - if an integer value is provided
              will limit the size of the packrat cache; if None is passed, then
              the cache size will be unbounded; if 0 is passed, the cache will
              be effectively disabled.
            
           This speedup may break existing programs that use parse actions that
           have side-effects.  For this reason, packrat parsing is disabled when
           you first import pyparsing.  To activate the packrat feature, your
           program must call the class method C{ParserElement.enablePackrat()}.  If
           your program uses C{psyco} to "compile as you go", you must call
           C{enablePackrat} before calling C{psyco.full()}.  If you do not do this,
           Python will crash.  For best results, call C{enablePackrat()} immediately
           after importing pyparsing.
           
           Example::
               import pyparsing
               pyparsing.ParserElement.enablePackrat()
        """
        if not ParserElement._packratEnabled:
            ParserElement._packratEnabled = True
            if cache_size_limit is None:
                ParserElement.packrat_cache = ParserElement._UnboundedCache()
            else:
                ParserElement.packrat_cache = ParserElement._FifoCache(cache_size_limit)
            ParserElement._parse = ParserElement._parseCache

    def parseString(self, instring, parseAll=False):
        """
        Execute the parse expression with the given string.
        This is the main interface to the client code, once the complete
        expression has been built.

        If you want the grammar to require that the entire input string be
        successfully parsed, then set C{parseAll} to True (equivalent to ending
        the grammar with C{L{StringEnd()}}).

        Note: C{parseString} implicitly calls C{expandtabs()} on the input string,
        in order to report proper column numbers in parse actions.
        If the input string contains tabs and
        the grammar uses parse actions that use the C{loc} argument to index into the
        string being parsed, you can ensure you have a consistent view of the input
        string by:
         - calling C{parseWithTabs} on your grammar before calling C{parseString}
           (see L{I{parseWithTabs}<parseWithTabs>})
         - define your parse action using the full C{(s,loc,toks)} signature, and
           reference the input string using the parse action's C{s} argument
         - explictly expand the tabs in your input string before calling
           C{parseString}
        
        Example::
            Word('a').parseString('aaaaabaaa')  # -> ['aaaaa']
            Word('a').parseString('aaaaabaaa', parseAll=True)  # -> Exception: Expected end of text
        """
        ParserElement.resetCache()
        if not self.streamlined:
            self.streamline()
        for e in self.ignoreExprs:
            e.streamline()

        if not self.keepTabs:
            instring = instring.expandtabs()
        try:
            loc, tokens = self._parse(instring, 0)
            if parseAll:
                loc = self.preParse(instring, loc)
                se = Empty() + StringEnd()
                se._parse(instring, loc)
        except ParseBaseException as exc:
            try:
                if ParserElement.verbose_stacktrace:
                    raise
                else:
                    raise exc
            finally:
                exc = None
                del exc

        else:
            return tokens

    def scanString(self, instring, maxMatches=_MAX_INT, overlap=False):
        """
        Scan the input string for expression matches.  Each match will return the
        matching tokens, start location, and end location.  May be called with optional
        C{maxMatches} argument, to clip scanning after 'n' matches are found.  If
        C{overlap} is specified, then overlapping matches will be reported.

        Note that the start and end locations are reported relative to the string
        being parsed.  See L{I{parseString}<parseString>} for more information on parsing
        strings with embedded tabs.

        Example::
            source = "sldjf123lsdjjkf345sldkjf879lkjsfd987"
            print(source)
            for tokens,start,end in Word(alphas).scanString(source):
                print(' '*start + '^'*(end-start))
                print(' '*start + tokens[0])
        
        prints::
        
            sldjf123lsdjjkf345sldkjf879lkjsfd987
            ^^^^^
            sldjf
                    ^^^^^^^
                    lsdjjkf
                              ^^^^^^
                              sldkjf
                                       ^^^^^^
                                       lkjsfd
        """
        if not self.streamlined:
            self.streamline()
        else:
            for e in self.ignoreExprs:
                e.streamline()

            if not self.keepTabs:
                instring = _ustr(instring).expandtabs()
            instrlen = len(instring)
            loc = 0
            preparseFn = self.preParse
            parseFn = self._parse
            ParserElement.resetCache()
            matches = 0
            try:
                while loc <= instrlen:
                    if matches < maxMatches:
                        try:
                            preloc = preparseFn(instring, loc)
                            nextLoc, tokens = parseFn(instring, preloc, callPreParse=False)
                        except ParseException:
                            loc = preloc + 1
                        else:
                            if nextLoc > loc:
                                matches += 1
                                yield (tokens, preloc, nextLoc)
                                if overlap:
                                    nextloc = preparseFn(instring, loc)
                                    if nextloc > loc:
                                        loc = nextLoc
                                    else:
                                        loc += 1
                                else:
                                    loc = nextLoc
                    else:
                        loc = preloc + 1

            except ParseBaseException as exc:
                try:
                    if ParserElement.verbose_stacktrace:
                        raise
                    else:
                        raise exc
                finally:
                    exc = None
                    del exc

    def transformString(self, instring):
        """
        Extension to C{L{scanString}}, to modify matching text with modified tokens that may
        be returned from a parse action.  To use C{transformString}, define a grammar and
        attach a parse action to it that modifies the returned token list.
        Invoking C{transformString()} on a target string will then scan for matches,
        and replace the matched text patterns according to the logic in the parse
        action.  C{transformString()} returns the resulting transformed string.
        
        Example::
            wd = Word(alphas)
            wd.setParseAction(lambda toks: toks[0].title())
            
            print(wd.transformString("now is the winter of our discontent made glorious summer by this sun of york."))
        Prints::
            Now Is The Winter Of Our Discontent Made Glorious Summer By This Sun Of York.
        """
        out = []
        lastE = 0
        self.keepTabs = True
        try:
            for t, s, e in self.scanString(instring):
                out.append(instring[lastE:s])
                if t:
                    if isinstance(t, ParseResults):
                        out += t.asList()
                    else:
                        if isinstance(t, list):
                            out += t
                        else:
                            out.append(t)
                lastE = e

            out.append(instring[lastE:])
            out = [o for o in out if o]
            return ''.join(map(_ustr, _flatten(out)))
        except ParseBaseException as exc:
            try:
                if ParserElement.verbose_stacktrace:
                    raise
                else:
                    raise exc
            finally:
                exc = None
                del exc

    def searchString(self, instring, maxMatches=_MAX_INT):
        """
        Another extension to C{L{scanString}}, simplifying the access to the tokens found
        to match the given parse expression.  May be called with optional
        C{maxMatches} argument, to clip searching after 'n' matches are found.
        
        Example::
            # a capitalized word starts with an uppercase letter, followed by zero or more lowercase letters
            cap_word = Word(alphas.upper(), alphas.lower())
            
            print(cap_word.searchString("More than Iron, more than Lead, more than Gold I need Electricity"))

            # the sum() builtin can be used to merge results into a single ParseResults object
            print(sum(cap_word.searchString("More than Iron, more than Lead, more than Gold I need Electricity")))
        prints::
            [['More'], ['Iron'], ['Lead'], ['Gold'], ['I'], ['Electricity']]
            ['More', 'Iron', 'Lead', 'Gold', 'I', 'Electricity']
        """
        try:
            return ParseResults([t for t, s, e in self.scanString(instring, maxMatches)])
        except ParseBaseException as exc:
            try:
                if ParserElement.verbose_stacktrace:
                    raise
                else:
                    raise exc
            finally:
                exc = None
                del exc

    def split(self, instring, maxsplit=_MAX_INT, includeSeparators=False):
        """
        Generator method to split a string using the given expression as a separator.
        May be called with optional C{maxsplit} argument, to limit the number of splits;
        and the optional C{includeSeparators} argument (default=C{False}), if the separating
        matching text should be included in the split results.
        
        Example::        
            punc = oneOf(list(".,;:/-!?"))
            print(list(punc.split("This, this?, this sentence, is badly punctuated!")))
        prints::
            ['This', ' this', '', ' this sentence', ' is badly punctuated', '']
        """
        splits = 0
        last = 0
        for t, s, e in self.scanString(instring, maxMatches=maxsplit):
            yield instring[last:s]
            if includeSeparators:
                yield t[0]
            last = e

        yield instring[last:]

    def __add__(self, other):
        """
        Implementation of + operator - returns C{L{And}}. Adding strings to a ParserElement
        converts them to L{Literal}s by default.
        
        Example::
            greet = Word(alphas) + "," + Word(alphas) + "!"
            hello = "Hello, World!"
            print (hello, "->", greet.parseString(hello))
        Prints::
            Hello, World! -> ['Hello', ',', 'World', '!']
        """
        if isinstance(other, basestring):
            other = ParserElement._literalStringClass(other)
        else:
            isinstance(other, ParserElement) or warnings.warn(('Cannot combine element of type %s with ParserElement' % type(other)), SyntaxWarning,
              stacklevel=2)
            return
        return And([self, other])

    def __radd__(self, other):
        """
        Implementation of + operator when left operand is not a C{L{ParserElement}}
        """
        if isinstance(other, basestring):
            other = ParserElement._literalStringClass(other)
        else:
            isinstance(other, ParserElement) or warnings.warn(('Cannot combine element of type %s with ParserElement' % type(other)), SyntaxWarning,
              stacklevel=2)
            return
        return other + self

    def __sub__(self, other):
        """
        Implementation of - operator, returns C{L{And}} with error stop
        """
        if isinstance(other, basestring):
            other = ParserElement._literalStringClass(other)
        else:
            isinstance(other, ParserElement) or warnings.warn(('Cannot combine element of type %s with ParserElement' % type(other)), SyntaxWarning,
              stacklevel=2)
            return
        return self + And._ErrorStop() + other

    def __rsub__(self, other):
        """
        Implementation of - operator when left operand is not a C{L{ParserElement}}
        """
        if isinstance(other, basestring):
            other = ParserElement._literalStringClass(other)
        else:
            isinstance(other, ParserElement) or warnings.warn(('Cannot combine element of type %s with ParserElement' % type(other)), SyntaxWarning,
              stacklevel=2)
            return
        return other - self

    def __mul__(self, other):
        """
        Implementation of * operator, allows use of C{expr * 3} in place of
        C{expr + expr + expr}.  Expressions may also me multiplied by a 2-integer
        tuple, similar to C{{min,max}} multipliers in regular expressions.  Tuples
        may also include C{None} as in:
         - C{expr*(n,None)} or C{expr*(n,)} is equivalent
              to C{expr*n + L{ZeroOrMore}(expr)}
              (read as "at least n instances of C{expr}")
         - C{expr*(None,n)} is equivalent to C{expr*(0,n)}
              (read as "0 to n instances of C{expr}")
         - C{expr*(None,None)} is equivalent to C{L{ZeroOrMore}(expr)}
         - C{expr*(1,None)} is equivalent to C{L{OneOrMore}(expr)}

        Note that C{expr*(None,n)} does not raise an exception if
        more than n exprs exist in the input stream; that is,
        C{expr*(None,n)} does not enforce a maximum number of expr
        occurrences.  If this behavior is desired, then write
        C{expr*(None,n) + ~expr}
        """
        if isinstance(other, int):
            minElements, optElements = other, 0
        else:
            if isinstance(other, tuple):
                other = (other + (None, None))[:2]
                if other[0] is None:
                    other = (
                     0, other[1])
                if isinstance(other[0], int) and other[1] is None:
                    if other[0] == 0:
                        return ZeroOrMore(self)
                    if other[0] == 1:
                        return OneOrMore(self)
                    return self * other[0] + ZeroOrMore(self)
                elif isinstance(other[0], int):
                    if isinstance(other[1], int):
                        minElements, optElements = other
                        optElements -= minElements
                    else:
                        raise TypeError("cannot multiply 'ParserElement' and ('%s','%s') objects", type(other[0]), type(other[1]))
                else:
                    raise TypeError("cannot multiply 'ParserElement' and '%s' objects", type(other))
            else:
                if minElements < 0:
                    raise ValueError('cannot multiply ParserElement by negative value')
                if optElements < 0:
                    raise ValueError('second tuple value must be greater or equal to first tuple value')
                if minElements == optElements == 0:
                    raise ValueError('cannot multiply ParserElement by 0 or (0,0)')
            if optElements:

                def makeOptionalList(n):
                    if n > 1:
                        return Optional(self + makeOptionalList(n - 1))
                    return Optional(self)

                if minElements:
                    if minElements == 1:
                        ret = self + makeOptionalList(optElements)
                    else:
                        ret = And([self] * minElements) + makeOptionalList(optElements)
                else:
                    ret = makeOptionalList(optElements)
            else:
                if minElements == 1:
                    ret = self
                else:
                    ret = And([self] * minElements)
            return ret

    def __rmul__(self, other):
        return self.__mul__(other)

    def __or__(self, other):
        """
        Implementation of | operator - returns C{L{MatchFirst}}
        """
        if isinstance(other, basestring):
            other = ParserElement._literalStringClass(other)
        else:
            isinstance(other, ParserElement) or warnings.warn(('Cannot combine element of type %s with ParserElement' % type(other)), SyntaxWarning,
              stacklevel=2)
            return
        return MatchFirst([self, other])

    def __ror__(self, other):
        """
        Implementation of | operator when left operand is not a C{L{ParserElement}}
        """
        if isinstance(other, basestring):
            other = ParserElement._literalStringClass(other)
        else:
            isinstance(other, ParserElement) or warnings.warn(('Cannot combine element of type %s with ParserElement' % type(other)), SyntaxWarning,
              stacklevel=2)
            return
        return other | self

    def __xor__(self, other):
        """
        Implementation of ^ operator - returns C{L{Or}}
        """
        if isinstance(other, basestring):
            other = ParserElement._literalStringClass(other)
        else:
            isinstance(other, ParserElement) or warnings.warn(('Cannot combine element of type %s with ParserElement' % type(other)), SyntaxWarning,
              stacklevel=2)
            return
        return Or([self, other])

    def __rxor__(self, other):
        """
        Implementation of ^ operator when left operand is not a C{L{ParserElement}}
        """
        if isinstance(other, basestring):
            other = ParserElement._literalStringClass(other)
        else:
            isinstance(other, ParserElement) or warnings.warn(('Cannot combine element of type %s with ParserElement' % type(other)), SyntaxWarning,
              stacklevel=2)
            return
        return other ^ self

    def __and__(self, other):
        """
        Implementation of & operator - returns C{L{Each}}
        """
        if isinstance(other, basestring):
            other = ParserElement._literalStringClass(other)
        else:
            isinstance(other, ParserElement) or warnings.warn(('Cannot combine element of type %s with ParserElement' % type(other)), SyntaxWarning,
              stacklevel=2)
            return
        return Each([self, other])

    def __rand__(self, other):
        """
        Implementation of & operator when left operand is not a C{L{ParserElement}}
        """
        if isinstance(other, basestring):
            other = ParserElement._literalStringClass(other)
        else:
            isinstance(other, ParserElement) or warnings.warn(('Cannot combine element of type %s with ParserElement' % type(other)), SyntaxWarning,
              stacklevel=2)
            return
        return other & self

    def __invert__(self):
        """
        Implementation of ~ operator - returns C{L{NotAny}}
        """
        return NotAny(self)

    def __call__(self, name=None):
        """
        Shortcut for C{L{setResultsName}}, with C{listAllMatches=False}.
        
        If C{name} is given with a trailing C{'*'} character, then C{listAllMatches} will be
        passed as C{True}.
           
        If C{name} is omitted, same as calling C{L{copy}}.

        Example::
            # these are equivalent
            userdata = Word(alphas).setResultsName("name") + Word(nums+"-").setResultsName("socsecno")
            userdata = Word(alphas)("name") + Word(nums+"-")("socsecno")             
        """
        if name is not None:
            return self.setResultsName(name)
        return self.copy()

    def suppress(self):
        """
        Suppresses the output of this C{ParserElement}; useful to keep punctuation from
        cluttering up returned output.
        """
        return Suppress(self)

    def leaveWhitespace(self):
        """
        Disables the skipping of whitespace before matching the characters in the
        C{ParserElement}'s defined pattern.  This is normally only used internally by
        the pyparsing module, but may be needed in some whitespace-sensitive grammars.
        """
        self.skipWhitespace = False
        return self

    def setWhitespaceChars(self, chars):
        """
        Overrides the default whitespace chars
        """
        self.skipWhitespace = True
        self.whiteChars = chars
        self.copyDefaultWhiteChars = False
        return self

    def parseWithTabs(self):
        """
        Overrides default behavior to expand C{<TAB>}s to spaces before parsing the input string.
        Must be called before C{parseString} when the input grammar contains elements that
        match C{<TAB>} characters.
        """
        self.keepTabs = True
        return self

    def ignore(self, other):
        """
        Define expression to be ignored (e.g., comments) while doing pattern
        matching; may be called repeatedly, to define multiple comment or other
        ignorable patterns.
        
        Example::
            patt = OneOrMore(Word(alphas))
            patt.parseString('ablaj /* comment */ lskjd') # -> ['ablaj']
            
            patt.ignore(cStyleComment)
            patt.parseString('ablaj /* comment */ lskjd') # -> ['ablaj', 'lskjd']
        """
        if isinstance(other, basestring):
            other = Suppress(other)
        elif isinstance(other, Suppress):
            if other not in self.ignoreExprs:
                self.ignoreExprs.append(other)
        else:
            self.ignoreExprs.append(Suppress(other.copy()))
        return self

    def setDebugActions(self, startAction, successAction, exceptionAction):
        """
        Enable display of debugging messages while doing pattern matching.
        """
        self.debugActions = (
         startAction or _defaultStartDebugAction,
         successAction or _defaultSuccessDebugAction,
         exceptionAction or _defaultExceptionDebugAction)
        self.debug = True
        return self

    def setDebug(self, flag=True):
        """
        Enable display of debugging messages while doing pattern matching.
        Set C{flag} to True to enable, False to disable.

        Example::
            wd = Word(alphas).setName("alphaword")
            integer = Word(nums).setName("numword")
            term = wd | integer
            
            # turn on debugging for wd
            wd.setDebug()

            OneOrMore(term).parseString("abc 123 xyz 890")
        
        prints::
            Match alphaword at loc 0(1,1)
            Matched alphaword -> ['abc']
            Match alphaword at loc 3(1,4)
            Exception raised:Expected alphaword (at char 4), (line:1, col:5)
            Match alphaword at loc 7(1,8)
            Matched alphaword -> ['xyz']
            Match alphaword at loc 11(1,12)
            Exception raised:Expected alphaword (at char 12), (line:1, col:13)
            Match alphaword at loc 15(1,16)
            Exception raised:Expected alphaword (at char 15), (line:1, col:16)

        The output shown is that produced by the default debug actions - custom debug actions can be
        specified using L{setDebugActions}. Prior to attempting
        to match the C{wd} expression, the debugging message C{"Match <exprname> at loc <n>(<line>,<col>)"}
        is shown. Then if the parse succeeds, a C{"Matched"} message is shown, or an C{"Exception raised"}
        message is shown. Also note the use of L{setName} to assign a human-readable name to the expression,
        which makes debugging and exception messages easier to understand - for instance, the default
        name created for the C{Word} expression without calling C{setName} is C{"W:(ABCD...)"}.
        """
        if flag:
            self.setDebugActions(_defaultStartDebugAction, _defaultSuccessDebugAction, _defaultExceptionDebugAction)
        else:
            self.debug = False
        return self

    def __str__(self):
        return self.name

    def __repr__(self):
        return _ustr(self)

    def streamline(self):
        self.streamlined = True
        self.strRepr = None
        return self

    def checkRecursion(self, parseElementList):
        pass

    def validate(self, validateTrace=[]):
        """
        Check defined expressions for valid structure, check for infinite recursive definitions.
        """
        self.checkRecursion([])

    def parseFile(self, file_or_filename, parseAll=False):
        """
        Execute the parse expression on the given file or filename.
        If a filename is specified (instead of a file object),
        the entire file is opened, read, and closed before parsing.
        """
        try:
            file_contents = file_or_filename.read()
        except AttributeError:
            with open(file_or_filename, 'r') as (f):
                file_contents = f.read()

        try:
            return self.parseString(file_contents, parseAll)
        except ParseBaseException as exc:
            try:
                if ParserElement.verbose_stacktrace:
                    raise
                else:
                    raise exc
            finally:
                exc = None
                del exc

    def __eq__(self, other):
        if isinstance(other, ParserElement):
            return self is other or vars(self) == vars(other)
        if isinstance(other, basestring):
            return self.matches(other)
        return super(ParserElement, self) == other

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(id(self))

    def __req__(self, other):
        return self == other

    def __rne__(self, other):
        return not self == other

    def matches(self, testString, parseAll=True):
        """
        Method for quick testing of a parser against a test string. Good for simple 
        inline microtests of sub expressions while building up larger parser.
           
        Parameters:
         - testString - to test against this expression for a match
         - parseAll - (default=C{True}) - flag to pass to C{L{parseString}} when running tests
            
        Example::
            expr = Word(nums)
            assert expr.matches("100")
        """
        try:
            self.parseString((_ustr(testString)), parseAll=parseAll)
            return True
        except ParseBaseException:
            return False

    def runTests(self, tests, parseAll=True, comment='#', fullDump=True, printResults=True, failureTests=False):
        r"""
        Execute the parse expression on a series of test strings, showing each
        test, the parsed results or where the parse failed. Quick and easy way to
        run a parse expression against a list of sample strings.
           
        Parameters:
         - tests - a list of separate test strings, or a multiline string of test strings
         - parseAll - (default=C{True}) - flag to pass to C{L{parseString}} when running tests           
         - comment - (default=C{'#'}) - expression for indicating embedded comments in the test 
              string; pass None to disable comment filtering
         - fullDump - (default=C{True}) - dump results as list followed by results names in nested outline;
              if False, only dump nested list
         - printResults - (default=C{True}) prints test output to stdout
         - failureTests - (default=C{False}) indicates if these tests are expected to fail parsing

        Returns: a (success, results) tuple, where success indicates that all tests succeeded
        (or failed if C{failureTests} is True), and the results contain a list of lines of each 
        test's output
        
        Example::
            number_expr = pyparsing_common.number.copy()

            result = number_expr.runTests('''
                # unsigned integer
                100
                # negative integer
                -100
                # float with scientific notation
                6.02e23
                # integer with scientific notation
                1e-12
                ''')
            print("Success" if result[0] else "Failed!")

            result = number_expr.runTests('''
                # stray character
                100Z
                # missing leading digit before '.'
                -.100
                # too many '.'
                3.14.159
                ''', failureTests=True)
            print("Success" if result[0] else "Failed!")
        prints::
            # unsigned integer
            100
            [100]

            # negative integer
            -100
            [-100]

            # float with scientific notation
            6.02e23
            [6.02e+23]

            # integer with scientific notation
            1e-12
            [1e-12]

            Success
            
            # stray character
            100Z
               ^
            FAIL: Expected end of text (at char 3), (line:1, col:4)

            # missing leading digit before '.'
            -.100
            ^
            FAIL: Expected {real number with scientific notation | real number | signed integer} (at char 0), (line:1, col:1)

            # too many '.'
            3.14.159
                ^
            FAIL: Expected end of text (at char 4), (line:1, col:5)

            Success

        Each test string must be on a single line. If you want to test a string that spans multiple
        lines, create a test like this::

            expr.runTest(r"this is a test\n of strings that spans \n 3 lines")
        
        (Note that this is a raw string literal, you must include the leading 'r'.)
        """
        if isinstance(tests, basestring):
            tests = list(map(str.strip, tests.rstrip().splitlines()))
        if isinstance(comment, basestring):
            comment = Literal(comment)
        allResults = []
        comments = []
        success = True
        for t in tests:
            if not (comment is not None and comment.matches(t, False)):
                if comments:
                    if not t:
                        comments.append(t)
                        continue
                if not t:
                    continue
            else:
                out = [
                 '\n'.join(comments), t]
                comments = []
                try:
                    t = t.replace('\\n', '\n')
                    result = self.parseString(t, parseAll=parseAll)
                    out.append(result.dump(full=fullDump))
                    success = success and not failureTests
                except ParseBaseException as pe:
                    try:
                        fatal = '(FATAL)' if isinstance(pe, ParseFatalException) else ''
                        if '\n' in t:
                            out.append(line(pe.loc, t))
                            out.append(' ' * (col(pe.loc, t) - 1) + '^' + fatal)
                        else:
                            out.append(' ' * pe.loc + '^' + fatal)
                        out.append('FAIL: ' + str(pe))
                        success = success and failureTests
                        result = pe
                    finally:
                        pe = None
                        del pe

                except Exception as exc:
                    try:
                        out.append('FAIL-EXCEPTION: ' + str(exc))
                        success = success and failureTests
                        result = exc
                    finally:
                        exc = None
                        del exc

            if printResults:
                if fullDump:
                    out.append('')
                print('\n'.join(out))
            allResults.append((t, result))

        return (success, allResults)


class Token(ParserElement):
    __doc__ = '\n    Abstract C{ParserElement} subclass, for defining atomic matching patterns.\n    '

    def __init__(self):
        super(Token, self).__init__(savelist=False)


class Empty(Token):
    __doc__ = '\n    An empty token, will always match.\n    '

    def __init__(self):
        super(Empty, self).__init__()
        self.name = 'Empty'
        self.mayReturnEmpty = True
        self.mayIndexError = False


class NoMatch(Token):
    __doc__ = '\n    A token that will never match.\n    '

    def __init__(self):
        super(NoMatch, self).__init__()
        self.name = 'NoMatch'
        self.mayReturnEmpty = True
        self.mayIndexError = False
        self.errmsg = 'Unmatchable token'

    def parseImpl(self, instring, loc, doActions=True):
        raise ParseException(instring, loc, self.errmsg, self)


class Literal(Token):
    __doc__ = '\n    Token to exactly match a specified string.\n    \n    Example::\n        Literal(\'blah\').parseString(\'blah\')  # -> [\'blah\']\n        Literal(\'blah\').parseString(\'blahfooblah\')  # -> [\'blah\']\n        Literal(\'blah\').parseString(\'bla\')  # -> Exception: Expected "blah"\n    \n    For case-insensitive matching, use L{CaselessLiteral}.\n    \n    For keyword matching (force word break before and after the matched string),\n    use L{Keyword} or L{CaselessKeyword}.\n    '

    def __init__(self, matchString):
        super(Literal, self).__init__()
        self.match = matchString
        self.matchLen = len(matchString)
        try:
            self.firstMatchChar = matchString[0]
        except IndexError:
            warnings.warn('null string passed to Literal; use Empty() instead', SyntaxWarning,
              stacklevel=2)
            self.__class__ = Empty

        self.name = '"%s"' % _ustr(self.match)
        self.errmsg = 'Expected ' + self.name
        self.mayReturnEmpty = False
        self.mayIndexError = False

    def parseImpl(self, instring, loc, doActions=True):
        if instring[loc] == self.firstMatchChar:
            if self.matchLen == 1 or instring.startswith(self.match, loc):
                return (
                 loc + self.matchLen, self.match)
        raise ParseException(instring, loc, self.errmsg, self)


_L = Literal
ParserElement._literalStringClass = Literal

class Keyword(Token):
    __doc__ = '\n    Token to exactly match a specified string as a keyword, that is, it must be\n    immediately followed by a non-keyword character.  Compare with C{L{Literal}}:\n     - C{Literal("if")} will match the leading C{\'if\'} in C{\'ifAndOnlyIf\'}.\n     - C{Keyword("if")} will not; it will only match the leading C{\'if\'} in C{\'if x=1\'}, or C{\'if(y==2)\'}\n    Accepts two optional constructor arguments in addition to the keyword string:\n     - C{identChars} is a string of characters that would be valid identifier characters,\n          defaulting to all alphanumerics + "_" and "$"\n     - C{caseless} allows case-insensitive matching, default is C{False}.\n       \n    Example::\n        Keyword("start").parseString("start")  # -> [\'start\']\n        Keyword("start").parseString("starting")  # -> Exception\n\n    For case-insensitive matching, use L{CaselessKeyword}.\n    '
    DEFAULT_KEYWORD_CHARS = alphanums + '_$'

    def __init__(self, matchString, identChars=None, caseless=False):
        super(Keyword, self).__init__()
        if identChars is None:
            identChars = Keyword.DEFAULT_KEYWORD_CHARS
        self.match = matchString
        self.matchLen = len(matchString)
        try:
            self.firstMatchChar = matchString[0]
        except IndexError:
            warnings.warn('null string passed to Keyword; use Empty() instead', SyntaxWarning,
              stacklevel=2)

        self.name = '"%s"' % self.match
        self.errmsg = 'Expected ' + self.name
        self.mayReturnEmpty = False
        self.mayIndexError = False
        self.caseless = caseless
        if caseless:
            self.caselessmatch = matchString.upper()
            identChars = identChars.upper()
        self.identChars = set(identChars)

    def parseImpl(self, instring, loc, doActions=True):
        if self.caseless:
            if not instring[loc:loc + self.matchLen].upper() == self.caselessmatch or loc >= len(instring) - self.matchLen or instring[(loc + self.matchLen)].upper() not in self.identChars:
                if loc == 0 or instring[(loc - 1)].upper() not in self.identChars:
                    return (
                     loc + self.matchLen, self.match)
        elif instring[loc] == self.firstMatchChar:
            if self.matchLen == 1 or instring.startswith(self.match, loc):
                if loc >= len(instring) - self.matchLen or instring[(loc + self.matchLen)] not in self.identChars:
                    if loc == 0 or instring[(loc - 1)] not in self.identChars:
                        return (
                         loc + self.matchLen, self.match)
        raise ParseException(instring, loc, self.errmsg, self)

    def copy(self):
        c = super(Keyword, self).copy()
        c.identChars = Keyword.DEFAULT_KEYWORD_CHARS
        return c

    @staticmethod
    def setDefaultKeywordChars(chars):
        """Overrides the default Keyword chars
        """
        Keyword.DEFAULT_KEYWORD_CHARS = chars


class CaselessLiteral(Literal):
    __doc__ = '\n    Token to match a specified string, ignoring case of letters.\n    Note: the matched results will always be in the case of the given\n    match string, NOT the case of the input text.\n\n    Example::\n        OneOrMore(CaselessLiteral("CMD")).parseString("cmd CMD Cmd10") # -> [\'CMD\', \'CMD\', \'CMD\']\n        \n    (Contrast with example for L{CaselessKeyword}.)\n    '

    def __init__(self, matchString):
        super(CaselessLiteral, self).__init__(matchString.upper())
        self.returnString = matchString
        self.name = "'%s'" % self.returnString
        self.errmsg = 'Expected ' + self.name

    def parseImpl(self, instring, loc, doActions=True):
        if instring[loc:loc + self.matchLen].upper() == self.match:
            return (
             loc + self.matchLen, self.returnString)
        raise ParseException(instring, loc, self.errmsg, self)


class CaselessKeyword(Keyword):
    __doc__ = '\n    Caseless version of L{Keyword}.\n\n    Example::\n        OneOrMore(CaselessKeyword("CMD")).parseString("cmd CMD Cmd10") # -> [\'CMD\', \'CMD\']\n        \n    (Contrast with example for L{CaselessLiteral}.)\n    '

    def __init__(self, matchString, identChars=None):
        super(CaselessKeyword, self).__init__(matchString, identChars, caseless=True)

    def parseImpl(self, instring, loc, doActions=True):
        if instring[loc:loc + self.matchLen].upper() == self.caselessmatch:
            if loc >= len(instring) - self.matchLen or instring[(loc + self.matchLen)].upper() not in self.identChars:
                return (
                 loc + self.matchLen, self.match)
        raise ParseException(instring, loc, self.errmsg, self)


class CloseMatch(Token):
    __doc__ = '\n    A variation on L{Literal} which matches "close" matches, that is, \n    strings with at most \'n\' mismatching characters. C{CloseMatch} takes parameters:\n     - C{match_string} - string to be matched\n     - C{maxMismatches} - (C{default=1}) maximum number of mismatches allowed to count as a match\n    \n    The results from a successful parse will contain the matched text from the input string and the following named results:\n     - C{mismatches} - a list of the positions within the match_string where mismatches were found\n     - C{original} - the original match_string used to compare against the input string\n    \n    If C{mismatches} is an empty list, then the match was an exact match.\n    \n    Example::\n        patt = CloseMatch("ATCATCGAATGGA")\n        patt.parseString("ATCATCGAAXGGA") # -> ([\'ATCATCGAAXGGA\'], {\'mismatches\': [[9]], \'original\': [\'ATCATCGAATGGA\']})\n        patt.parseString("ATCAXCGAAXGGA") # -> Exception: Expected \'ATCATCGAATGGA\' (with up to 1 mismatches) (at char 0), (line:1, col:1)\n\n        # exact match\n        patt.parseString("ATCATCGAATGGA") # -> ([\'ATCATCGAATGGA\'], {\'mismatches\': [[]], \'original\': [\'ATCATCGAATGGA\']})\n\n        # close match allowing up to 2 mismatches\n        patt = CloseMatch("ATCATCGAATGGA", maxMismatches=2)\n        patt.parseString("ATCAXCGAAXGGA") # -> ([\'ATCAXCGAAXGGA\'], {\'mismatches\': [[4, 9]], \'original\': [\'ATCATCGAATGGA\']})\n    '

    def __init__(self, match_string, maxMismatches=1):
        super(CloseMatch, self).__init__()
        self.name = match_string
        self.match_string = match_string
        self.maxMismatches = maxMismatches
        self.errmsg = 'Expected %r (with up to %d mismatches)' % (self.match_string, self.maxMismatches)
        self.mayIndexError = False
        self.mayReturnEmpty = False

    def parseImpl(self, instring, loc, doActions=True):
        start = loc
        instrlen = len(instring)
        maxloc = start + len(self.match_string)
        if maxloc <= instrlen:
            match_string = self.match_string
            match_stringloc = 0
            mismatches = []
            maxMismatches = self.maxMismatches
            for match_stringloc, s_m in enumerate(zip(instring[loc:maxloc], self.match_string)):
                src, mat = s_m
                if src != mat:
                    mismatches.append(match_stringloc)
                    if len(mismatches) > maxMismatches:
                        break
            else:
                loc = match_stringloc + 1
                results = ParseResults([instring[start:loc]])
                results['original'] = self.match_string
                results['mismatches'] = mismatches
                return (loc, results)

        raise ParseException(instring, loc, self.errmsg, self)


class Word(Token):
    __doc__ = '\n    Token for matching words composed of allowed character sets.\n    Defined with string containing all allowed initial characters,\n    an optional string containing allowed body characters (if omitted,\n    defaults to the initial character set), and an optional minimum,\n    maximum, and/or exact length.  The default value for C{min} is 1 (a\n    minimum value < 1 is not valid); the default values for C{max} and C{exact}\n    are 0, meaning no maximum or exact length restriction. An optional\n    C{excludeChars} parameter can list characters that might be found in \n    the input C{bodyChars} string; useful to define a word of all printables\n    except for one or two characters, for instance.\n    \n    L{srange} is useful for defining custom character set strings for defining \n    C{Word} expressions, using range notation from regular expression character sets.\n    \n    A common mistake is to use C{Word} to match a specific literal string, as in \n    C{Word("Address")}. Remember that C{Word} uses the string argument to define\n    I{sets} of matchable characters. This expression would match "Add", "AAA",\n    "dAred", or any other word made up of the characters \'A\', \'d\', \'r\', \'e\', and \'s\'.\n    To match an exact literal string, use L{Literal} or L{Keyword}.\n\n    pyparsing includes helper strings for building Words:\n     - L{alphas}\n     - L{nums}\n     - L{alphanums}\n     - L{hexnums}\n     - L{alphas8bit} (alphabetic characters in ASCII range 128-255 - accented, tilded, umlauted, etc.)\n     - L{punc8bit} (non-alphabetic characters in ASCII range 128-255 - currency, symbols, superscripts, diacriticals, etc.)\n     - L{printables} (any non-whitespace character)\n\n    Example::\n        # a word composed of digits\n        integer = Word(nums) # equivalent to Word("0123456789") or Word(srange("0-9"))\n        \n        # a word with a leading capital, and zero or more lowercase\n        capital_word = Word(alphas.upper(), alphas.lower())\n\n        # hostnames are alphanumeric, with leading alpha, and \'-\'\n        hostname = Word(alphas, alphanums+\'-\')\n        \n        # roman numeral (not a strict parser, accepts invalid mix of characters)\n        roman = Word("IVXLCDM")\n        \n        # any string of non-whitespace characters, except for \',\'\n        csv_value = Word(printables, excludeChars=",")\n    '

    def __init__(self, initChars, bodyChars=None, min=1, max=0, exact=0, asKeyword=False, excludeChars=None):
        super(Word, self).__init__()
        if excludeChars:
            initChars = ''.join((c for c in initChars if c not in excludeChars))
            if bodyChars:
                bodyChars = ''.join((c for c in bodyChars if c not in excludeChars))
            else:
                self.initCharsOrig = initChars
                self.initChars = set(initChars)
                if bodyChars:
                    self.bodyCharsOrig = bodyChars
                    self.bodyChars = set(bodyChars)
                else:
                    self.bodyCharsOrig = initChars
                    self.bodyChars = set(initChars)
                self.maxSpecified = max > 0
                if min < 1:
                    raise ValueError('cannot specify a minimum length < 1; use Optional(Word()) if zero-length word is permitted')
                self.minLen = min
                if max > 0:
                    self.maxLen = max
                else:
                    self.maxLen = _MAX_INT
            if exact > 0:
                self.maxLen = exact
                self.minLen = exact
            self.name = _ustr(self)
            self.errmsg = 'Expected ' + self.name
            self.mayIndexError = False
            self.asKeyword = asKeyword
            if ' ' not in self.initCharsOrig + self.bodyCharsOrig and min == 1 and max == 0 and exact == 0:
                if self.bodyCharsOrig == self.initCharsOrig:
                    self.reString = '[%s]+' % _escapeRegexRangeChars(self.initCharsOrig)
        elif len(self.initCharsOrig) == 1:
            self.reString = '%s[%s]*' % (
             re.escape(self.initCharsOrig),
             _escapeRegexRangeChars(self.bodyCharsOrig))
        else:
            self.reString = '[%s][%s]*' % (
             _escapeRegexRangeChars(self.initCharsOrig),
             _escapeRegexRangeChars(self.bodyCharsOrig))
        if self.asKeyword:
            self.reString = '\\b' + self.reString + '\\b'
        try:
            self.re = re.compile(self.reString)
        except Exception:
            self.re = None

    def parseImpl(self, instring, loc, doActions=True):
        if self.re:
            result = self.re.match(instring, loc)
            if not result:
                raise ParseException(instring, loc, self.errmsg, self)
            loc = result.end()
            return (loc, result.group())
            if instring[loc] not in self.initChars:
                raise ParseException(instring, loc, self.errmsg, self)
            start = loc
            loc += 1
            instrlen = len(instring)
            bodychars = self.bodyChars
            maxloc = start + self.maxLen
            maxloc = min(maxloc, instrlen)
            while loc < maxloc and instring[loc] in bodychars:
                loc += 1

            throwException = False
            if loc - start < self.minLen:
                throwException = True
        elif self.maxSpecified:
            if loc < instrlen and instring[loc] in bodychars:
                throwException = True
        if self.asKeyword and not start > 0 and instring[(start - 1)] in bodychars:
            if loc < instrlen:
                if instring[loc] in bodychars:
                    throwException = True
            if throwException:
                raise ParseException(instring, loc, self.errmsg, self)
        return (
         loc, instring[start:loc])

    def __str__(self):
        try:
            return super(Word, self).__str__()
        except Exception:
            pass

        if self.strRepr is None:

            def charsAsStr(s):
                if len(s) > 4:
                    return s[:4] + '...'
                return s

            if self.initCharsOrig != self.bodyCharsOrig:
                self.strRepr = 'W:(%s,%s)' % (charsAsStr(self.initCharsOrig), charsAsStr(self.bodyCharsOrig))
            else:
                self.strRepr = 'W:(%s)' % charsAsStr(self.initCharsOrig)
        return self.strRepr


class Regex(Token):
    __doc__ = '\n    Token for matching strings that match a given regular expression.\n    Defined with string specifying the regular expression in a form recognized by the inbuilt Python re module.\n    If the given regex contains named groups (defined using C{(?P<name>...)}), these will be preserved as \n    named parse results.\n\n    Example::\n        realnum = Regex(r"[+-]?\\d+\\.\\d*")\n        date = Regex(r\'(?P<year>\\d{4})-(?P<month>\\d\\d?)-(?P<day>\\d\\d?)\')\n        # ref: http://stackoverflow.com/questions/267399/how-do-you-match-only-valid-roman-numerals-with-a-regular-expression\n        roman = Regex(r"M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})")\n    '
    compiledREtype = type(re.compile('[A-Z]'))

    def __init__(self, pattern, flags=0):
        """The parameters C{pattern} and C{flags} are passed to the C{re.compile()} function as-is. See the Python C{re} module for an explanation of the acceptable patterns and flags."""
        super(Regex, self).__init__()
        if isinstance(pattern, basestring):
            if not pattern:
                warnings.warn('null string passed to Regex; use Empty() instead', SyntaxWarning,
                  stacklevel=2)
            self.pattern = pattern
            self.flags = flags
            try:
                self.re = re.compile(self.pattern, self.flags)
                self.reString = self.pattern
            except sre_constants.error:
                warnings.warn(('invalid pattern (%s) passed to Regex' % pattern), SyntaxWarning,
                  stacklevel=2)
                raise

        else:
            if isinstance(pattern, Regex.compiledREtype):
                self.re = pattern
                self.pattern = self.reString = str(pattern)
                self.flags = flags
            else:
                raise ValueError('Regex may only be constructed with a string or a compiled RE object')
        self.name = _ustr(self)
        self.errmsg = 'Expected ' + self.name
        self.mayIndexError = False
        self.mayReturnEmpty = True

    def parseImpl(self, instring, loc, doActions=True):
        result = self.re.match(instring, loc)
        if not result:
            raise ParseException(instring, loc, self.errmsg, self)
        loc = result.end()
        d = result.groupdict()
        ret = ParseResults(result.group())
        if d:
            for k in d:
                ret[k] = d[k]

        return (
         loc, ret)

    def __str__(self):
        try:
            return super(Regex, self).__str__()
        except Exception:
            pass

        if self.strRepr is None:
            self.strRepr = 'Re:(%s)' % repr(self.pattern)
        return self.strRepr


class QuotedString(Token):
    __doc__ = '\n    Token for matching strings that are delimited by quoting characters.\n    \n    Defined with the following parameters:\n        - quoteChar - string of one or more characters defining the quote delimiting string\n        - escChar - character to escape quotes, typically backslash (default=C{None})\n        - escQuote - special quote sequence to escape an embedded quote string (such as SQL\'s "" to escape an embedded ") (default=C{None})\n        - multiline - boolean indicating whether quotes can span multiple lines (default=C{False})\n        - unquoteResults - boolean indicating whether the matched text should be unquoted (default=C{True})\n        - endQuoteChar - string of one or more characters defining the end of the quote delimited string (default=C{None} => same as quoteChar)\n        - convertWhitespaceEscapes - convert escaped whitespace (C{\'\\t\'}, C{\'\\n\'}, etc.) to actual whitespace (default=C{True})\n\n    Example::\n        qs = QuotedString(\'"\')\n        print(qs.searchString(\'lsjdf "This is the quote" sldjf\'))\n        complex_qs = QuotedString(\'{{\', endQuoteChar=\'}}\')\n        print(complex_qs.searchString(\'lsjdf {{This is the "quote"}} sldjf\'))\n        sql_qs = QuotedString(\'"\', escQuote=\'""\')\n        print(sql_qs.searchString(\'lsjdf "This is the quote with ""embedded"" quotes" sldjf\'))\n    prints::\n        [[\'This is the quote\']]\n        [[\'This is the "quote"\']]\n        [[\'This is the quote with "embedded" quotes\']]\n    '

    def __init__(self, quoteChar, escChar=None, escQuote=None, multiline=False, unquoteResults=True, endQuoteChar=None, convertWhitespaceEscapes=True):
        super(QuotedString, self).__init__()
        quoteChar = quoteChar.strip()
        if not quoteChar:
            warnings.warn('quoteChar cannot be the empty string', SyntaxWarning, stacklevel=2)
            raise SyntaxError()
        if endQuoteChar is None:
            endQuoteChar = quoteChar
        else:
            endQuoteChar = endQuoteChar.strip()
            if not endQuoteChar:
                warnings.warn('endQuoteChar cannot be the empty string', SyntaxWarning, stacklevel=2)
                raise SyntaxError()
            else:
                self.quoteChar = quoteChar
                self.quoteCharLen = len(quoteChar)
                self.firstQuoteChar = quoteChar[0]
                self.endQuoteChar = endQuoteChar
                self.endQuoteCharLen = len(endQuoteChar)
                self.escChar = escChar
                self.escQuote = escQuote
                self.unquoteResults = unquoteResults
                self.convertWhitespaceEscapes = convertWhitespaceEscapes
                if multiline:
                    self.flags = re.MULTILINE | re.DOTALL
                    self.pattern = '%s(?:[^%s%s]' % (
                     re.escape(self.quoteChar),
                     _escapeRegexRangeChars(self.endQuoteChar[0]),
                     escChar is not None and _escapeRegexRangeChars(escChar) or '')
                else:
                    self.flags = 0
                self.pattern = '%s(?:[^%s\\n\\r%s]' % (
                 re.escape(self.quoteChar),
                 _escapeRegexRangeChars(self.endQuoteChar[0]),
                 escChar is not None and _escapeRegexRangeChars(escChar) or '')
            if len(self.endQuoteChar) > 1:
                self.pattern += '|(?:' + ')|(?:'.join(('%s[^%s]' % (re.escape(self.endQuoteChar[:i]), _escapeRegexRangeChars(self.endQuoteChar[i])) for i in range(len(self.endQuoteChar) - 1, 0, -1))) + ')'
            if escQuote:
                self.pattern += '|(?:%s)' % re.escape(escQuote)
            if escChar:
                self.pattern += '|(?:%s.)' % re.escape(escChar)
                self.escCharReplacePattern = re.escape(self.escChar) + '(.)'
            self.pattern += ')*%s' % re.escape(self.endQuoteChar)
            try:
                self.re = re.compile(self.pattern, self.flags)
                self.reString = self.pattern
            except sre_constants.error:
                warnings.warn(('invalid pattern (%s) passed to Regex' % self.pattern), SyntaxWarning,
                  stacklevel=2)
                raise

            self.name = _ustr(self)
            self.errmsg = 'Expected ' + self.name
            self.mayIndexError = False
            self.mayReturnEmpty = True

    def parseImpl(self, instring, loc, doActions=True):
        result = instring[loc] == self.firstQuoteChar and self.re.match(instring, loc) or None
        if not result:
            raise ParseException(instring, loc, self.errmsg, self)
        loc = result.end()
        ret = result.group()
        if self.unquoteResults:
            ret = ret[self.quoteCharLen:-self.endQuoteCharLen]
            if isinstance(ret, basestring):
                if '\\' in ret:
                    if self.convertWhitespaceEscapes:
                        ws_map = {'\\t':'\t', 
                         '\\n':'\n', 
                         '\\f':'\x0c', 
                         '\\r':'\r'}
                        for wslit, wschar in ws_map.items():
                            ret = ret.replace(wslit, wschar)

                if self.escChar:
                    ret = re.sub(self.escCharReplacePattern, '\\g<1>', ret)
                if self.escQuote:
                    ret = ret.replace(self.escQuote, self.endQuoteChar)
        return (
         loc, ret)

    def __str__(self):
        try:
            return super(QuotedString, self).__str__()
        except Exception:
            pass

        if self.strRepr is None:
            self.strRepr = 'quoted string, starting with %s ending with %s' % (self.quoteChar, self.endQuoteChar)
        return self.strRepr


class CharsNotIn(Token):
    __doc__ = '\n    Token for matching words composed of characters I{not} in a given set (will\n    include whitespace in matched characters if not listed in the provided exclusion set - see example).\n    Defined with string containing all disallowed characters, and an optional\n    minimum, maximum, and/or exact length.  The default value for C{min} is 1 (a\n    minimum value < 1 is not valid); the default values for C{max} and C{exact}\n    are 0, meaning no maximum or exact length restriction.\n\n    Example::\n        # define a comma-separated-value as anything that is not a \',\'\n        csv_value = CharsNotIn(\',\')\n        print(delimitedList(csv_value).parseString("dkls,lsdkjf,s12 34,@!#,213"))\n    prints::\n        [\'dkls\', \'lsdkjf\', \'s12 34\', \'@!#\', \'213\']\n    '

    def __init__(self, notChars, min=1, max=0, exact=0):
        super(CharsNotIn, self).__init__()
        self.skipWhitespace = False
        self.notChars = notChars
        if min < 1:
            raise ValueError('cannot specify a minimum length < 1; use Optional(CharsNotIn()) if zero-length char group is permitted')
        else:
            self.minLen = min
            if max > 0:
                self.maxLen = max
            else:
                self.maxLen = _MAX_INT
        if exact > 0:
            self.maxLen = exact
            self.minLen = exact
        self.name = _ustr(self)
        self.errmsg = 'Expected ' + self.name
        self.mayReturnEmpty = self.minLen == 0
        self.mayIndexError = False

    def parseImpl(self, instring, loc, doActions=True):
        if instring[loc] in self.notChars:
            raise ParseException(instring, loc, self.errmsg, self)
        start = loc
        loc += 1
        notchars = self.notChars
        maxlen = min(start + self.maxLen, len(instring))
        while loc < maxlen and instring[loc] not in notchars:
            loc += 1

        if loc - start < self.minLen:
            raise ParseException(instring, loc, self.errmsg, self)
        return (loc, instring[start:loc])

    def __str__(self):
        try:
            return super(CharsNotIn, self).__str__()
        except Exception:
            pass

        if self.strRepr is None:
            if len(self.notChars) > 4:
                self.strRepr = '!W:(%s...)' % self.notChars[:4]
            else:
                self.strRepr = '!W:(%s)' % self.notChars
        return self.strRepr


class White(Token):
    __doc__ = '\n    Special matching class for matching whitespace.  Normally, whitespace is ignored\n    by pyparsing grammars.  This class is included when some whitespace structures\n    are significant.  Define with a string containing the whitespace characters to be\n    matched; default is C{" \\t\\r\\n"}.  Also takes optional C{min}, C{max}, and C{exact} arguments,\n    as defined for the C{L{Word}} class.\n    '
    whiteStrs = {' ':'<SPC>', 
     '\t':'<TAB>', 
     '\n':'<LF>', 
     '\r':'<CR>', 
     '\x0c':'<FF>'}

    def __init__(self, ws=' \t\r\n', min=1, max=0, exact=0):
        super(White, self).__init__()
        self.matchWhite = ws
        self.setWhitespaceChars(''.join((c for c in self.whiteChars if c not in self.matchWhite)))
        self.name = ''.join((White.whiteStrs[c] for c in self.matchWhite))
        self.mayReturnEmpty = True
        self.errmsg = 'Expected ' + self.name
        self.minLen = min
        if max > 0:
            self.maxLen = max
        else:
            self.maxLen = _MAX_INT
        if exact > 0:
            self.maxLen = exact
            self.minLen = exact

    def parseImpl(self, instring, loc, doActions=True):
        if instring[loc] not in self.matchWhite:
            raise ParseException(instring, loc, self.errmsg, self)
        start = loc
        loc += 1
        maxloc = start + self.maxLen
        maxloc = min(maxloc, len(instring))
        while loc < maxloc and instring[loc] in self.matchWhite:
            loc += 1

        if loc - start < self.minLen:
            raise ParseException(instring, loc, self.errmsg, self)
        return (loc, instring[start:loc])


class _PositionToken(Token):

    def __init__(self):
        super(_PositionToken, self).__init__()
        self.name = self.__class__.__name__
        self.mayReturnEmpty = True
        self.mayIndexError = False


class GoToColumn(_PositionToken):
    __doc__ = '\n    Token to advance to a specific column of input text; useful for tabular report scraping.\n    '

    def __init__(self, colno):
        super(GoToColumn, self).__init__()
        self.col = colno

    def preParse(self, instring, loc):
        if col(loc, instring) != self.col:
            instrlen = len(instring)
            if self.ignoreExprs:
                loc = self._skipIgnorables(instring, loc)
            while loc < instrlen and instring[loc].isspace() and col(loc, instring) != self.col:
                loc += 1

        return loc

    def parseImpl(self, instring, loc, doActions=True):
        thiscol = col(loc, instring)
        if thiscol > self.col:
            raise ParseException(instring, loc, 'Text not in expected column', self)
        newloc = loc + self.col - thiscol
        ret = instring[loc:newloc]
        return (newloc, ret)


class LineStart(_PositionToken):
    __doc__ = "\n    Matches if current position is at the beginning of a line within the parse string\n    \n    Example::\n    \n        test = '''        AAA this line\n        AAA and this line\n          AAA but not this one\n        B AAA and definitely not this one\n        '''\n\n        for t in (LineStart() + 'AAA' + restOfLine).searchString(test):\n            print(t)\n    \n    Prints::\n        ['AAA', ' this line']\n        ['AAA', ' and this line']    \n\n    "

    def __init__(self):
        super(LineStart, self).__init__()
        self.errmsg = 'Expected start of line'

    def parseImpl(self, instring, loc, doActions=True):
        if col(loc, instring) == 1:
            return (
             loc, [])
        raise ParseException(instring, loc, self.errmsg, self)


class LineEnd(_PositionToken):
    __doc__ = '\n    Matches if current position is at the end of a line within the parse string\n    '

    def __init__(self):
        super(LineEnd, self).__init__()
        self.setWhitespaceChars(ParserElement.DEFAULT_WHITE_CHARS.replace('\n', ''))
        self.errmsg = 'Expected end of line'

    def parseImpl(self, instring, loc, doActions=True):
        if loc < len(instring):
            if instring[loc] == '\n':
                return (
                 loc + 1, '\n')
            raise ParseException(instring, loc, self.errmsg, self)
        else:
            if loc == len(instring):
                return (
                 loc + 1, [])
            raise ParseException(instring, loc, self.errmsg, self)


class StringStart(_PositionToken):
    __doc__ = '\n    Matches if current position is at the beginning of the parse string\n    '

    def __init__(self):
        super(StringStart, self).__init__()
        self.errmsg = 'Expected start of text'

    def parseImpl(self, instring, loc, doActions=True):
        if loc != 0:
            if loc != self.preParse(instring, 0):
                raise ParseException(instring, loc, self.errmsg, self)
        return (
         loc, [])


class StringEnd(_PositionToken):
    __doc__ = '\n    Matches if current position is at the end of the parse string\n    '

    def __init__(self):
        super(StringEnd, self).__init__()
        self.errmsg = 'Expected end of text'

    def parseImpl(self, instring, loc, doActions=True):
        if loc < len(instring):
            raise ParseException(instring, loc, self.errmsg, self)
        else:
            if loc == len(instring):
                return (
                 loc + 1, [])
            if loc > len(instring):
                return (
                 loc, [])
            raise ParseException(instring, loc, self.errmsg, self)


class WordStart(_PositionToken):
    __doc__ = '\n    Matches if the current position is at the beginning of a Word, and\n    is not preceded by any character in a given set of C{wordChars}\n    (default=C{printables}). To emulate the C{\x08} behavior of regular expressions,\n    use C{WordStart(alphanums)}. C{WordStart} will also match at the beginning of\n    the string being parsed, or at the beginning of a line.\n    '

    def __init__(self, wordChars=printables):
        super(WordStart, self).__init__()
        self.wordChars = set(wordChars)
        self.errmsg = 'Not at the start of a word'

    def parseImpl(self, instring, loc, doActions=True):
        if loc != 0:
            if instring[(loc - 1)] in self.wordChars or instring[loc] not in self.wordChars:
                raise ParseException(instring, loc, self.errmsg, self)
        return (
         loc, [])


class WordEnd(_PositionToken):
    __doc__ = '\n    Matches if the current position is at the end of a Word, and\n    is not followed by any character in a given set of C{wordChars}\n    (default=C{printables}). To emulate the C{\x08} behavior of regular expressions,\n    use C{WordEnd(alphanums)}. C{WordEnd} will also match at the end of\n    the string being parsed, or at the end of a line.\n    '

    def __init__(self, wordChars=printables):
        super(WordEnd, self).__init__()
        self.wordChars = set(wordChars)
        self.skipWhitespace = False
        self.errmsg = 'Not at the end of a word'

    def parseImpl(self, instring, loc, doActions=True):
        instrlen = len(instring)
        if instrlen > 0:
            if loc < instrlen:
                if instring[loc] in self.wordChars or instring[(loc - 1)] not in self.wordChars:
                    raise ParseException(instring, loc, self.errmsg, self)
        return (
         loc, [])


class ParseExpression(ParserElement):
    __doc__ = '\n    Abstract subclass of ParserElement, for combining and post-processing parsed tokens.\n    '

    def __init__(self, exprs, savelist=False):
        super(ParseExpression, self).__init__(savelist)
        if isinstance(exprs, _generatorType):
            exprs = list(exprs)
        if isinstance(exprs, basestring):
            self.exprs = [
             ParserElement._literalStringClass(exprs)]
        else:
            if isinstance(exprs, Iterable):
                exprs = list(exprs)
                if all((isinstance(expr, basestring) for expr in exprs)):
                    exprs = map(ParserElement._literalStringClass, exprs)
                self.exprs = list(exprs)
            else:
                try:
                    self.exprs = list(exprs)
                except TypeError:
                    self.exprs = [
                     exprs]

                self.callPreparse = False

    def __getitem__(self, i):
        return self.exprs[i]

    def append(self, other):
        self.exprs.append(other)
        self.strRepr = None
        return self

    def leaveWhitespace(self):
        """Extends C{leaveWhitespace} defined in base class, and also invokes C{leaveWhitespace} on
           all contained expressions."""
        self.skipWhitespace = False
        self.exprs = [e.copy() for e in self.exprs]
        for e in self.exprs:
            e.leaveWhitespace()

        return self

    def ignore(self, other):
        if isinstance(other, Suppress):
            if other not in self.ignoreExprs:
                super(ParseExpression, self).ignore(other)
                for e in self.exprs:
                    e.ignore(self.ignoreExprs[(-1)])

        else:
            super(ParseExpression, self).ignore(other)
            for e in self.exprs:
                e.ignore(self.ignoreExprs[(-1)])

        return self

    def __str__(self):
        try:
            return super(ParseExpression, self).__str__()
        except Exception:
            pass

        if self.strRepr is None:
            self.strRepr = '%s:(%s)' % (self.__class__.__name__, _ustr(self.exprs))
        return self.strRepr

    def streamline(self):
        super(ParseExpression, self).streamline()
        for e in self.exprs:
            e.streamline()

        if len(self.exprs) == 2:
            other = self.exprs[0]
            if isinstance(other, self.__class__):
                if not other.parseAction:
                    if other.resultsName is None:
                        if not other.debug:
                            self.exprs = other.exprs[:] + [self.exprs[1]]
                            self.strRepr = None
                            self.mayReturnEmpty |= other.mayReturnEmpty
                            self.mayIndexError |= other.mayIndexError
            other = self.exprs[(-1)]
            if isinstance(other, self.__class__) and not other.parseAction:
                if other.resultsName is None:
                    if not other.debug:
                        self.exprs = self.exprs[:-1] + other.exprs[:]
                        self.strRepr = None
                        self.mayReturnEmpty |= other.mayReturnEmpty
                        self.mayIndexError |= other.mayIndexError
        self.errmsg = 'Expected ' + _ustr(self)
        return self

    def setResultsName(self, name, listAllMatches=False):
        ret = super(ParseExpression, self).setResultsName(name, listAllMatches)
        return ret

    def validate(self, validateTrace=[]):
        tmp = validateTrace[:] + [self]
        for e in self.exprs:
            e.validate(tmp)

        self.checkRecursion([])

    def copy(self):
        ret = super(ParseExpression, self).copy()
        ret.exprs = [e.copy() for e in self.exprs]
        return ret


class And(ParseExpression):
    __doc__ = '\n    Requires all given C{ParseExpression}s to be found in the given order.\n    Expressions may be separated by whitespace.\n    May be constructed using the C{\'+\'} operator.\n    May also be constructed using the C{\'-\'} operator, which will suppress backtracking.\n\n    Example::\n        integer = Word(nums)\n        name_expr = OneOrMore(Word(alphas))\n\n        expr = And([integer("id"),name_expr("name"),integer("age")])\n        # more easily written as:\n        expr = integer("id") + name_expr("name") + integer("age")\n    '

    class _ErrorStop(Empty):

        def __init__(self, *args, **kwargs):
            (super(And._ErrorStop, self).__init__)(*args, **kwargs)
            self.name = '-'
            self.leaveWhitespace()

    def __init__(self, exprs, savelist=True):
        super(And, self).__init__(exprs, savelist)
        self.mayReturnEmpty = all((e.mayReturnEmpty for e in self.exprs))
        self.setWhitespaceChars(self.exprs[0].whiteChars)
        self.skipWhitespace = self.exprs[0].skipWhitespace
        self.callPreparse = True

    def parseImpl(self, instring, loc, doActions=True):
        loc, resultlist = self.exprs[0]._parse(instring, loc, doActions, callPreParse=False)
        errorStop = False
        for e in self.exprs[1:]:
            if isinstance(e, And._ErrorStop):
                errorStop = True
                continue
            if errorStop:
                try:
                    loc, exprtokens = e._parse(instring, loc, doActions)
                except ParseSyntaxException:
                    raise
                except ParseBaseException as pe:
                    try:
                        pe.__traceback__ = None
                        raise ParseSyntaxException._from_exception(pe)
                    finally:
                        pe = None
                        del pe

                except IndexError:
                    raise ParseSyntaxException(instring, len(instring), self.errmsg, self)

            else:
                loc, exprtokens = e._parse(instring, loc, doActions)
            if exprtokens or exprtokens.haskeys():
                resultlist += exprtokens

        return (
         loc, resultlist)

    def __iadd__(self, other):
        if isinstance(other, basestring):
            other = ParserElement._literalStringClass(other)
        return self.append(other)

    def checkRecursion(self, parseElementList):
        subRecCheckList = parseElementList[:] + [self]
        for e in self.exprs:
            e.checkRecursion(subRecCheckList)
            if not e.mayReturnEmpty:
                break

    def __str__(self):
        if hasattr(self, 'name'):
            return self.name
        if self.strRepr is None:
            self.strRepr = '{' + ' '.join((_ustr(e) for e in self.exprs)) + '}'
        return self.strRepr


class Or(ParseExpression):
    __doc__ = '\n    Requires that at least one C{ParseExpression} is found.\n    If two expressions match, the expression that matches the longest string will be used.\n    May be constructed using the C{\'^\'} operator.\n\n    Example::\n        # construct Or using \'^\' operator\n        \n        number = Word(nums) ^ Combine(Word(nums) + \'.\' + Word(nums))\n        print(number.searchString("123 3.1416 789"))\n    prints::\n        [[\'123\'], [\'3.1416\'], [\'789\']]\n    '

    def __init__(self, exprs, savelist=False):
        super(Or, self).__init__(exprs, savelist)
        if self.exprs:
            self.mayReturnEmpty = any((e.mayReturnEmpty for e in self.exprs))
        else:
            self.mayReturnEmpty = True

    def parseImpl(self, instring, loc, doActions=True):
        maxExcLoc = -1
        maxException = None
        matches = []
        for e in self.exprs:
            try:
                loc2 = e.tryParse(instring, loc)
            except ParseException as err:
                try:
                    err.__traceback__ = None
                    if err.loc > maxExcLoc:
                        maxException = err
                        maxExcLoc = err.loc
                finally:
                    err = None
                    del err

            except IndexError:
                if len(instring) > maxExcLoc:
                    maxException = ParseException(instring, len(instring), e.errmsg, self)
                    maxExcLoc = len(instring)
            else:
                matches.append((loc2, e))

        if matches:
            matches.sort(key=(lambda x: -x[0]))
            for _, e in matches:
                try:
                    return e._parse(instring, loc, doActions)
                except ParseException as err:
                    try:
                        err.__traceback__ = None
                        if err.loc > maxExcLoc:
                            maxException = err
                            maxExcLoc = err.loc
                    finally:
                        err = None
                        del err

        elif maxException is not None:
            maxException.msg = self.errmsg
            raise maxException
        else:
            raise ParseException(instring, loc, 'no defined alternatives to match', self)

    def __ixor__(self, other):
        if isinstance(other, basestring):
            other = ParserElement._literalStringClass(other)
        return self.append(other)

    def __str__(self):
        if hasattr(self, 'name'):
            return self.name
        if self.strRepr is None:
            self.strRepr = '{' + ' ^ '.join((_ustr(e) for e in self.exprs)) + '}'
        return self.strRepr

    def checkRecursion(self, parseElementList):
        subRecCheckList = parseElementList[:] + [self]
        for e in self.exprs:
            e.checkRecursion(subRecCheckList)


class MatchFirst(ParseExpression):
    __doc__ = '\n    Requires that at least one C{ParseExpression} is found.\n    If two expressions match, the first one listed is the one that will match.\n    May be constructed using the C{\'|\'} operator.\n\n    Example::\n        # construct MatchFirst using \'|\' operator\n        \n        # watch the order of expressions to match\n        number = Word(nums) | Combine(Word(nums) + \'.\' + Word(nums))\n        print(number.searchString("123 3.1416 789")) #  Fail! -> [[\'123\'], [\'3\'], [\'1416\'], [\'789\']]\n\n        # put more selective expression first\n        number = Combine(Word(nums) + \'.\' + Word(nums)) | Word(nums)\n        print(number.searchString("123 3.1416 789")) #  Better -> [[\'123\'], [\'3.1416\'], [\'789\']]\n    '

    def __init__(self, exprs, savelist=False):
        super(MatchFirst, self).__init__(exprs, savelist)
        if self.exprs:
            self.mayReturnEmpty = any((e.mayReturnEmpty for e in self.exprs))
        else:
            self.mayReturnEmpty = True

    def parseImpl(self, instring, loc, doActions=True):
        maxExcLoc = -1
        maxException = None
        for e in self.exprs:
            try:
                ret = e._parse(instring, loc, doActions)
                return ret
            except ParseException as err:
                try:
                    if err.loc > maxExcLoc:
                        maxException = err
                        maxExcLoc = err.loc
                finally:
                    err = None
                    del err

            except IndexError:
                if len(instring) > maxExcLoc:
                    maxException = ParseException(instring, len(instring), e.errmsg, self)
                    maxExcLoc = len(instring)

        else:
            if maxException is not None:
                maxException.msg = self.errmsg
                raise maxException
            else:
                raise ParseException(instring, loc, 'no defined alternatives to match', self)

    def __ior__(self, other):
        if isinstance(other, basestring):
            other = ParserElement._literalStringClass(other)
        return self.append(other)

    def __str__(self):
        if hasattr(self, 'name'):
            return self.name
        if self.strRepr is None:
            self.strRepr = '{' + ' | '.join((_ustr(e) for e in self.exprs)) + '}'
        return self.strRepr

    def checkRecursion(self, parseElementList):
        subRecCheckList = parseElementList[:] + [self]
        for e in self.exprs:
            e.checkRecursion(subRecCheckList)


class Each(ParseExpression):
    __doc__ = '\n    Requires all given C{ParseExpression}s to be found, but in any order.\n    Expressions may be separated by whitespace.\n    May be constructed using the C{\'&\'} operator.\n\n    Example::\n        color = oneOf("RED ORANGE YELLOW GREEN BLUE PURPLE BLACK WHITE BROWN")\n        shape_type = oneOf("SQUARE CIRCLE TRIANGLE STAR HEXAGON OCTAGON")\n        integer = Word(nums)\n        shape_attr = "shape:" + shape_type("shape")\n        posn_attr = "posn:" + Group(integer("x") + \',\' + integer("y"))("posn")\n        color_attr = "color:" + color("color")\n        size_attr = "size:" + integer("size")\n\n        # use Each (using operator \'&\') to accept attributes in any order \n        # (shape and posn are required, color and size are optional)\n        shape_spec = shape_attr & posn_attr & Optional(color_attr) & Optional(size_attr)\n\n        shape_spec.runTests(\'\'\'\n            shape: SQUARE color: BLACK posn: 100, 120\n            shape: CIRCLE size: 50 color: BLUE posn: 50,80\n            color:GREEN size:20 shape:TRIANGLE posn:20,40\n            \'\'\'\n            )\n    prints::\n        shape: SQUARE color: BLACK posn: 100, 120\n        [\'shape:\', \'SQUARE\', \'color:\', \'BLACK\', \'posn:\', [\'100\', \',\', \'120\']]\n        - color: BLACK\n        - posn: [\'100\', \',\', \'120\']\n          - x: 100\n          - y: 120\n        - shape: SQUARE\n\n\n        shape: CIRCLE size: 50 color: BLUE posn: 50,80\n        [\'shape:\', \'CIRCLE\', \'size:\', \'50\', \'color:\', \'BLUE\', \'posn:\', [\'50\', \',\', \'80\']]\n        - color: BLUE\n        - posn: [\'50\', \',\', \'80\']\n          - x: 50\n          - y: 80\n        - shape: CIRCLE\n        - size: 50\n\n\n        color: GREEN size: 20 shape: TRIANGLE posn: 20,40\n        [\'color:\', \'GREEN\', \'size:\', \'20\', \'shape:\', \'TRIANGLE\', \'posn:\', [\'20\', \',\', \'40\']]\n        - color: GREEN\n        - posn: [\'20\', \',\', \'40\']\n          - x: 20\n          - y: 40\n        - shape: TRIANGLE\n        - size: 20\n    '

    def __init__(self, exprs, savelist=True):
        super(Each, self).__init__(exprs, savelist)
        self.mayReturnEmpty = all((e.mayReturnEmpty for e in self.exprs))
        self.skipWhitespace = True
        self.initExprGroups = True

    def parseImpl(self, instring, loc, doActions=True):
        if self.initExprGroups:
            self.opt1map = dict(((id(e.expr), e) for e in self.exprs if isinstance(e, Optional)))
            opt1 = [e.expr for e in self.exprs if isinstance(e, Optional)]
            opt2 = [e for e in self.exprs if e.mayReturnEmpty if not isinstance(e, Optional)]
            self.optionals = opt1 + opt2
            self.multioptionals = [e.expr for e in self.exprs if isinstance(e, ZeroOrMore)]
            self.multirequired = [e.expr for e in self.exprs if isinstance(e, OneOrMore)]
            self.required = [e for e in self.exprs if not isinstance(e, (Optional, ZeroOrMore, OneOrMore))]
            self.required += self.multirequired
            self.initExprGroups = False
        tmpLoc = loc
        tmpReqd = self.required[:]
        tmpOpt = self.optionals[:]
        matchOrder = []
        keepMatching = True
        while keepMatching:
            tmpExprs = tmpReqd + tmpOpt + self.multioptionals + self.multirequired
            failed = []
            for e in tmpExprs:
                try:
                    tmpLoc = e.tryParse(instring, tmpLoc)
                except ParseException:
                    failed.append(e)
                else:
                    matchOrder.append(self.opt1map.get(id(e), e))
                    if e in tmpReqd:
                        tmpReqd.remove(e)
                if e in tmpOpt:
                    tmpOpt.remove(e)

            if len(failed) == len(tmpExprs):
                keepMatching = False

        if tmpReqd:
            missing = ', '.join((_ustr(e) for e in tmpReqd))
            raise ParseException(instring, loc, 'Missing one or more required elements (%s)' % missing)
        matchOrder += [e for e in self.exprs if isinstance(e, Optional) if e.expr in tmpOpt]
        resultlist = []
        for e in matchOrder:
            loc, results = e._parse(instring, loc, doActions)
            resultlist.append(results)

        finalResults = sum(resultlist, ParseResults([]))
        return (loc, finalResults)

    def __str__(self):
        if hasattr(self, 'name'):
            return self.name
        if self.strRepr is None:
            self.strRepr = '{' + ' & '.join((_ustr(e) for e in self.exprs)) + '}'
        return self.strRepr

    def checkRecursion(self, parseElementList):
        subRecCheckList = parseElementList[:] + [self]
        for e in self.exprs:
            e.checkRecursion(subRecCheckList)


class ParseElementEnhance(ParserElement):
    __doc__ = '\n    Abstract subclass of C{ParserElement}, for combining and post-processing parsed tokens.\n    '

    def __init__(self, expr, savelist=False):
        super(ParseElementEnhance, self).__init__(savelist)
        if isinstance(expr, basestring):
            if issubclass(ParserElement._literalStringClass, Token):
                expr = ParserElement._literalStringClass(expr)
            else:
                expr = ParserElement._literalStringClass(Literal(expr))
        self.expr = expr
        self.strRepr = None
        if expr is not None:
            self.mayIndexError = expr.mayIndexError
            self.mayReturnEmpty = expr.mayReturnEmpty
            self.setWhitespaceChars(expr.whiteChars)
            self.skipWhitespace = expr.skipWhitespace
            self.saveAsList = expr.saveAsList
            self.callPreparse = expr.callPreparse
            self.ignoreExprs.extend(expr.ignoreExprs)

    def parseImpl(self, instring, loc, doActions=True):
        if self.expr is not None:
            return self.expr._parse(instring, loc, doActions, callPreParse=False)
        raise ParseException('', loc, self.errmsg, self)

    def leaveWhitespace(self):
        self.skipWhitespace = False
        self.expr = self.expr.copy()
        if self.expr is not None:
            self.expr.leaveWhitespace()
        return self

    def ignore(self, other):
        if isinstance(other, Suppress):
            if other not in self.ignoreExprs:
                super(ParseElementEnhance, self).ignore(other)
                if self.expr is not None:
                    self.expr.ignore(self.ignoreExprs[(-1)])
        else:
            super(ParseElementEnhance, self).ignore(other)
            if self.expr is not None:
                self.expr.ignore(self.ignoreExprs[(-1)])
        return self

    def streamline(self):
        super(ParseElementEnhance, self).streamline()
        if self.expr is not None:
            self.expr.streamline()
        return self

    def checkRecursion(self, parseElementList):
        if self in parseElementList:
            raise RecursiveGrammarException(parseElementList + [self])
        subRecCheckList = parseElementList[:] + [self]
        if self.expr is not None:
            self.expr.checkRecursion(subRecCheckList)

    def validate(self, validateTrace=[]):
        tmp = validateTrace[:] + [self]
        if self.expr is not None:
            self.expr.validate(tmp)
        self.checkRecursion([])

    def __str__(self):
        try:
            return super(ParseElementEnhance, self).__str__()
        except Exception:
            pass

        if self.strRepr is None:
            if self.expr is not None:
                self.strRepr = '%s:(%s)' % (self.__class__.__name__, _ustr(self.expr))
        return self.strRepr


class FollowedBy(ParseElementEnhance):
    __doc__ = '\n    Lookahead matching of the given parse expression.  C{FollowedBy}\n    does I{not} advance the parsing position within the input string, it only\n    verifies that the specified parse expression matches at the current\n    position.  C{FollowedBy} always returns a null token list.\n\n    Example::\n        # use FollowedBy to match a label only if it is followed by a \':\'\n        data_word = Word(alphas)\n        label = data_word + FollowedBy(\':\')\n        attr_expr = Group(label + Suppress(\':\') + OneOrMore(data_word, stopOn=label).setParseAction(\' \'.join))\n        \n        OneOrMore(attr_expr).parseString("shape: SQUARE color: BLACK posn: upper left").pprint()\n    prints::\n        [[\'shape\', \'SQUARE\'], [\'color\', \'BLACK\'], [\'posn\', \'upper left\']]\n    '

    def __init__(self, expr):
        super(FollowedBy, self).__init__(expr)
        self.mayReturnEmpty = True

    def parseImpl(self, instring, loc, doActions=True):
        self.expr.tryParse(instring, loc)
        return (loc, [])


class NotAny(ParseElementEnhance):
    __doc__ = "\n    Lookahead to disallow matching with the given parse expression.  C{NotAny}\n    does I{not} advance the parsing position within the input string, it only\n    verifies that the specified parse expression does I{not} match at the current\n    position.  Also, C{NotAny} does I{not} skip over leading whitespace. C{NotAny}\n    always returns a null token list.  May be constructed using the '~' operator.\n\n    Example::\n        \n    "

    def __init__(self, expr):
        super(NotAny, self).__init__(expr)
        self.skipWhitespace = False
        self.mayReturnEmpty = True
        self.errmsg = 'Found unwanted token, ' + _ustr(self.expr)

    def parseImpl(self, instring, loc, doActions=True):
        if self.expr.canParseNext(instring, loc):
            raise ParseException(instring, loc, self.errmsg, self)
        return (
         loc, [])

    def __str__(self):
        if hasattr(self, 'name'):
            return self.name
        if self.strRepr is None:
            self.strRepr = '~{' + _ustr(self.expr) + '}'
        return self.strRepr


class _MultipleMatch(ParseElementEnhance):

    def __init__(self, expr, stopOn=None):
        super(_MultipleMatch, self).__init__(expr)
        self.saveAsList = True
        ender = stopOn
        if isinstance(ender, basestring):
            ender = ParserElement._literalStringClass(ender)
        self.not_ender = ~ender if ender is not None else None

    def parseImpl(self, instring, loc, doActions=True):
        self_expr_parse = self.expr._parse
        self_skip_ignorables = self._skipIgnorables
        check_ender = self.not_ender is not None
        if check_ender:
            try_not_ender = self.not_ender.tryParse
        if check_ender:
            try_not_ender(instring, loc)
        loc, tokens = self_expr_parse(instring, loc, doActions, callPreParse=False)
        try:
            hasIgnoreExprs = not not self.ignoreExprs
            while 1:
                if check_ender:
                    try_not_ender(instring, loc)
                elif hasIgnoreExprs:
                    preloc = self_skip_ignorables(instring, loc)
                else:
                    preloc = loc
                loc, tmptokens = self_expr_parse(instring, preloc, doActions)
                if tmptokens or tmptokens.haskeys():
                    tokens += tmptokens

        except (ParseException, IndexError):
            pass

        return (
         loc, tokens)


class OneOrMore(_MultipleMatch):
    __doc__ = '\n    Repetition of one or more of the given expression.\n    \n    Parameters:\n     - expr - expression that must match one or more times\n     - stopOn - (default=C{None}) - expression for a terminating sentinel\n          (only required if the sentinel would ordinarily match the repetition \n          expression)          \n\n    Example::\n        data_word = Word(alphas)\n        label = data_word + FollowedBy(\':\')\n        attr_expr = Group(label + Suppress(\':\') + OneOrMore(data_word).setParseAction(\' \'.join))\n\n        text = "shape: SQUARE posn: upper left color: BLACK"\n        OneOrMore(attr_expr).parseString(text).pprint()  # Fail! read \'color\' as data instead of next label -> [[\'shape\', \'SQUARE color\']]\n\n        # use stopOn attribute for OneOrMore to avoid reading label string as part of the data\n        attr_expr = Group(label + Suppress(\':\') + OneOrMore(data_word, stopOn=label).setParseAction(\' \'.join))\n        OneOrMore(attr_expr).parseString(text).pprint() # Better -> [[\'shape\', \'SQUARE\'], [\'posn\', \'upper left\'], [\'color\', \'BLACK\']]\n        \n        # could also be written as\n        (attr_expr * (1,)).parseString(text).pprint()\n    '

    def __str__(self):
        if hasattr(self, 'name'):
            return self.name
        if self.strRepr is None:
            self.strRepr = '{' + _ustr(self.expr) + '}...'
        return self.strRepr


class ZeroOrMore(_MultipleMatch):
    __doc__ = '\n    Optional repetition of zero or more of the given expression.\n    \n    Parameters:\n     - expr - expression that must match zero or more times\n     - stopOn - (default=C{None}) - expression for a terminating sentinel\n          (only required if the sentinel would ordinarily match the repetition \n          expression)          \n\n    Example: similar to L{OneOrMore}\n    '

    def __init__(self, expr, stopOn=None):
        super(ZeroOrMore, self).__init__(expr, stopOn=stopOn)
        self.mayReturnEmpty = True

    def parseImpl(self, instring, loc, doActions=True):
        try:
            return super(ZeroOrMore, self).parseImpl(instring, loc, doActions)
        except (ParseException, IndexError):
            return (
             loc, [])

    def __str__(self):
        if hasattr(self, 'name'):
            return self.name
        if self.strRepr is None:
            self.strRepr = '[' + _ustr(self.expr) + ']...'
        return self.strRepr


class _NullToken(object):

    def __bool__(self):
        return False

    __nonzero__ = __bool__

    def __str__(self):
        return ''


_optionalNotMatched = _NullToken()

class Optional(ParseElementEnhance):
    __doc__ = "\n    Optional matching of the given expression.\n\n    Parameters:\n     - expr - expression that must match zero or more times\n     - default (optional) - value to be returned if the optional expression is not found.\n\n    Example::\n        # US postal code can be a 5-digit zip, plus optional 4-digit qualifier\n        zip = Combine(Word(nums, exact=5) + Optional('-' + Word(nums, exact=4)))\n        zip.runTests('''\n            # traditional ZIP code\n            12345\n            \n            # ZIP+4 form\n            12101-0001\n            \n            # invalid ZIP\n            98765-\n            ''')\n    prints::\n        # traditional ZIP code\n        12345\n        ['12345']\n\n        # ZIP+4 form\n        12101-0001\n        ['12101-0001']\n\n        # invalid ZIP\n        98765-\n             ^\n        FAIL: Expected end of text (at char 5), (line:1, col:6)\n    "

    def __init__(self, expr, default=_optionalNotMatched):
        super(Optional, self).__init__(expr, savelist=False)
        self.saveAsList = self.expr.saveAsList
        self.defaultValue = default
        self.mayReturnEmpty = True

    def parseImpl(self, instring, loc, doActions=True):
        try:
            loc, tokens = self.expr._parse(instring, loc, doActions, callPreParse=False)
        except (ParseException, IndexError):
            if self.defaultValue is not _optionalNotMatched:
                if self.expr.resultsName:
                    tokens = ParseResults([self.defaultValue])
                    tokens[self.expr.resultsName] = self.defaultValue
                else:
                    tokens = [
                     self.defaultValue]
            else:
                tokens = []

        return (
         loc, tokens)

    def __str__(self):
        if hasattr(self, 'name'):
            return self.name
        if self.strRepr is None:
            self.strRepr = '[' + _ustr(self.expr) + ']'
        return self.strRepr


class SkipTo(ParseElementEnhance):
    __doc__ = '\n    Token for skipping over all undefined text until the matched expression is found.\n\n    Parameters:\n     - expr - target expression marking the end of the data to be skipped\n     - include - (default=C{False}) if True, the target expression is also parsed \n          (the skipped text and target expression are returned as a 2-element list).\n     - ignore - (default=C{None}) used to define grammars (typically quoted strings and \n          comments) that might contain false matches to the target expression\n     - failOn - (default=C{None}) define expressions that are not allowed to be \n          included in the skipped test; if found before the target expression is found, \n          the SkipTo is not a match\n\n    Example::\n        report = \'\'\'\n            Outstanding Issues Report - 1 Jan 2000\n\n               # | Severity | Description                               |  Days Open\n            -----+----------+-------------------------------------------+-----------\n             101 | Critical | Intermittent system crash                 |          6\n              94 | Cosmetic | Spelling error on Login (\'log|n\')         |         14\n              79 | Minor    | System slow when running too many reports |         47\n            \'\'\'\n        integer = Word(nums)\n        SEP = Suppress(\'|\')\n        # use SkipTo to simply match everything up until the next SEP\n        # - ignore quoted strings, so that a \'|\' character inside a quoted string does not match\n        # - parse action will call token.strip() for each matched token, i.e., the description body\n        string_data = SkipTo(SEP, ignore=quotedString)\n        string_data.setParseAction(tokenMap(str.strip))\n        ticket_expr = (integer("issue_num") + SEP \n                      + string_data("sev") + SEP \n                      + string_data("desc") + SEP \n                      + integer("days_open"))\n        \n        for tkt in ticket_expr.searchString(report):\n            print tkt.dump()\n    prints::\n        [\'101\', \'Critical\', \'Intermittent system crash\', \'6\']\n        - days_open: 6\n        - desc: Intermittent system crash\n        - issue_num: 101\n        - sev: Critical\n        [\'94\', \'Cosmetic\', "Spelling error on Login (\'log|n\')", \'14\']\n        - days_open: 14\n        - desc: Spelling error on Login (\'log|n\')\n        - issue_num: 94\n        - sev: Cosmetic\n        [\'79\', \'Minor\', \'System slow when running too many reports\', \'47\']\n        - days_open: 47\n        - desc: System slow when running too many reports\n        - issue_num: 79\n        - sev: Minor\n    '

    def __init__(self, other, include=False, ignore=None, failOn=None):
        super(SkipTo, self).__init__(other)
        self.ignoreExpr = ignore
        self.mayReturnEmpty = True
        self.mayIndexError = False
        self.includeMatch = include
        self.asList = False
        if isinstance(failOn, basestring):
            self.failOn = ParserElement._literalStringClass(failOn)
        else:
            self.failOn = failOn
        self.errmsg = 'No match found for ' + _ustr(self.expr)

    def parseImpl(self, instring, loc, doActions=True):
        startloc = loc
        instrlen = len(instring)
        expr = self.expr
        expr_parse = self.expr._parse
        self_failOn_canParseNext = self.failOn.canParseNext if self.failOn is not None else None
        self_ignoreExpr_tryParse = self.ignoreExpr.tryParse if self.ignoreExpr is not None else None
        tmploc = loc
        while 1:
            if tmploc <= instrlen:
                if self_failOn_canParseNext is not None:
                    if self_failOn_canParseNext(instring, tmploc):
                        break
                else:
                    if self_ignoreExpr_tryParse is not None:
                        while True:
                            try:
                                tmploc = self_ignoreExpr_tryParse(instring, tmploc)
                            except ParseBaseException:
                                break

                    try:
                        expr_parse(instring, tmploc, doActions=False, callPreParse=False)
                    except (ParseException, IndexError):
                        tmploc += 1

                break
        else:
            raise ParseException(instring, loc, self.errmsg, self)

        loc = tmploc
        skiptext = instring[startloc:loc]
        skipresult = ParseResults(skiptext)
        if self.includeMatch:
            loc, mat = expr_parse(instring, loc, doActions, callPreParse=False)
            skipresult += mat
        return (loc, skipresult)


class Forward(ParseElementEnhance):
    __doc__ = "\n    Forward declaration of an expression to be defined later -\n    used for recursive grammars, such as algebraic infix notation.\n    When the expression is known, it is assigned to the C{Forward} variable using the '<<' operator.\n\n    Note: take care when assigning to C{Forward} not to overlook precedence of operators.\n    Specifically, '|' has a lower precedence than '<<', so that::\n        fwdExpr << a | b | c\n    will actually be evaluated as::\n        (fwdExpr << a) | b | c\n    thereby leaving b and c out as parseable alternatives.  It is recommended that you\n    explicitly group the values inserted into the C{Forward}::\n        fwdExpr << (a | b | c)\n    Converting to use the '<<=' operator instead will avoid this problem.\n\n    See L{ParseResults.pprint} for an example of a recursive parser created using\n    C{Forward}.\n    "

    def __init__(self, other=None):
        super(Forward, self).__init__(other, savelist=False)

    def __lshift__(self, other):
        if isinstance(other, basestring):
            other = ParserElement._literalStringClass(other)
        self.expr = other
        self.strRepr = None
        self.mayIndexError = self.expr.mayIndexError
        self.mayReturnEmpty = self.expr.mayReturnEmpty
        self.setWhitespaceChars(self.expr.whiteChars)
        self.skipWhitespace = self.expr.skipWhitespace
        self.saveAsList = self.expr.saveAsList
        self.ignoreExprs.extend(self.expr.ignoreExprs)
        return self

    def __ilshift__(self, other):
        return self << other

    def leaveWhitespace(self):
        self.skipWhitespace = False
        return self

    def streamline(self):
        if not self.streamlined:
            self.streamlined = True
            if self.expr is not None:
                self.expr.streamline()
        return self

    def validate(self, validateTrace=[]):
        if self not in validateTrace:
            tmp = validateTrace[:] + [self]
            if self.expr is not None:
                self.expr.validate(tmp)
        self.checkRecursion([])

    def __str__--- This code section failed: ---

 L.4198         0  LOAD_GLOBAL              hasattr
                2  LOAD_FAST                'self'
                4  LOAD_STR                 'name'
                6  CALL_FUNCTION_2       2  '2 positional arguments'
                8  POP_JUMP_IF_FALSE    16  'to 16'

 L.4199        10  LOAD_FAST                'self'
               12  LOAD_ATTR                name
               14  RETURN_VALUE     
             16_0  COME_FROM             8  '8'

 L.4200        16  LOAD_FAST                'self'
               18  LOAD_ATTR                __class__
               20  LOAD_ATTR                __name__
               22  LOAD_STR                 ': ...'
               24  BINARY_ADD       
               26  RETURN_VALUE     

 L.4209        28  LOAD_STR                 'None'
               30  STORE_FAST               'retString'
               32  POP_BLOCK        
               34  LOAD_CONST               None

 L.4211        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _revertClass
               40  LOAD_FAST                'self'
               42  STORE_ATTR               __class__
               44  END_FINALLY      

 L.4212        46  LOAD_FAST                'self'
               48  LOAD_ATTR                __class__
               50  LOAD_ATTR                __name__
               52  LOAD_STR                 ': '
               54  BINARY_ADD       
               56  LOAD_FAST                'retString'
               58  BINARY_ADD       
               60  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 32

    def copy(self):
        if self.expr is not None:
            return super(Forward, self).copy()
        ret = Forward()
        ret <<= self
        return ret


class _ForwardNoRecurse(Forward):

    def __str__(self):
        return '...'


class TokenConverter(ParseElementEnhance):
    __doc__ = '\n    Abstract subclass of C{ParseExpression}, for converting parsed results.\n    '

    def __init__(self, expr, savelist=False):
        super(TokenConverter, self).__init__(expr)
        self.saveAsList = False


class Combine(TokenConverter):
    __doc__ = "\n    Converter to concatenate all matching tokens to a single string.\n    By default, the matching patterns must also be contiguous in the input string;\n    this can be disabled by specifying C{'adjacent=False'} in the constructor.\n\n    Example::\n        real = Word(nums) + '.' + Word(nums)\n        print(real.parseString('3.1416')) # -> ['3', '.', '1416']\n        # will also erroneously match the following\n        print(real.parseString('3. 1416')) # -> ['3', '.', '1416']\n\n        real = Combine(Word(nums) + '.' + Word(nums))\n        print(real.parseString('3.1416')) # -> ['3.1416']\n        # no match when there are internal spaces\n        print(real.parseString('3. 1416')) # -> Exception: Expected W:(0123...)\n    "

    def __init__(self, expr, joinString='', adjacent=True):
        super(Combine, self).__init__(expr)
        if adjacent:
            self.leaveWhitespace()
        self.adjacent = adjacent
        self.skipWhitespace = True
        self.joinString = joinString
        self.callPreparse = True

    def ignore(self, other):
        if self.adjacent:
            ParserElement.ignore(self, other)
        else:
            super(Combine, self).ignore(other)
        return self

    def postParse(self, instring, loc, tokenlist):
        retToks = tokenlist.copy()
        del retToks[:]
        retToks += ParseResults([''.join(tokenlist._asStringList(self.joinString))], modal=(self.modalResults))
        if self.resultsName:
            if retToks.haskeys():
                return [
                 retToks]
        return retToks


class Group(TokenConverter):
    __doc__ = '\n    Converter to return the matched tokens as a list - useful for returning tokens of C{L{ZeroOrMore}} and C{L{OneOrMore}} expressions.\n\n    Example::\n        ident = Word(alphas)\n        num = Word(nums)\n        term = ident | num\n        func = ident + Optional(delimitedList(term))\n        print(func.parseString("fn a,b,100"))  # -> [\'fn\', \'a\', \'b\', \'100\']\n\n        func = ident + Group(Optional(delimitedList(term)))\n        print(func.parseString("fn a,b,100"))  # -> [\'fn\', [\'a\', \'b\', \'100\']]\n    '

    def __init__(self, expr):
        super(Group, self).__init__(expr)
        self.saveAsList = True

    def postParse(self, instring, loc, tokenlist):
        return [
         tokenlist]


class Dict(TokenConverter):
    __doc__ = '\n    Converter to return a repetitive expression as a list, but also as a dictionary.\n    Each element can also be referenced using the first token in the expression as its key.\n    Useful for tabular report scraping when the first column can be used as a item key.\n\n    Example::\n        data_word = Word(alphas)\n        label = data_word + FollowedBy(\':\')\n        attr_expr = Group(label + Suppress(\':\') + OneOrMore(data_word).setParseAction(\' \'.join))\n\n        text = "shape: SQUARE posn: upper left color: light blue texture: burlap"\n        attr_expr = (label + Suppress(\':\') + OneOrMore(data_word, stopOn=label).setParseAction(\' \'.join))\n        \n        # print attributes as plain groups\n        print(OneOrMore(attr_expr).parseString(text).dump())\n        \n        # instead of OneOrMore(expr), parse using Dict(OneOrMore(Group(expr))) - Dict will auto-assign names\n        result = Dict(OneOrMore(Group(attr_expr))).parseString(text)\n        print(result.dump())\n        \n        # access named fields as dict entries, or output as dict\n        print(result[\'shape\'])        \n        print(result.asDict())\n    prints::\n        [\'shape\', \'SQUARE\', \'posn\', \'upper left\', \'color\', \'light blue\', \'texture\', \'burlap\']\n\n        [[\'shape\', \'SQUARE\'], [\'posn\', \'upper left\'], [\'color\', \'light blue\'], [\'texture\', \'burlap\']]\n        - color: light blue\n        - posn: upper left\n        - shape: SQUARE\n        - texture: burlap\n        SQUARE\n        {\'color\': \'light blue\', \'posn\': \'upper left\', \'texture\': \'burlap\', \'shape\': \'SQUARE\'}\n    See more examples at L{ParseResults} of accessing fields by results name.\n    '

    def __init__(self, expr):
        super(Dict, self).__init__(expr)
        self.saveAsList = True

    def postParse(self, instring, loc, tokenlist):
        for i, tok in enumerate(tokenlist):
            if len(tok) == 0:
                continue
            else:
                ikey = tok[0]
                if isinstance(ikey, int):
                    ikey = _ustr(tok[0]).strip()
                if len(tok) == 1:
                    tokenlist[ikey] = _ParseResultsWithOffset('', i)
            if len(tok) == 2:
                if not isinstance(tok[1], ParseResults):
                    tokenlist[ikey] = _ParseResultsWithOffset(tok[1], i)
            dictvalue = tok.copy()
            del dictvalue[0]
            if not len(dictvalue) != 1:
                if isinstance(dictvalue, ParseResults):
                    if dictvalue.haskeys():
                        tokenlist[ikey] = _ParseResultsWithOffset(dictvalue, i)
                tokenlist[ikey] = _ParseResultsWithOffset(dictvalue[0], i)

        if self.resultsName:
            return [
             tokenlist]
        return tokenlist


class Suppress(TokenConverter):
    __doc__ = '\n    Converter for ignoring the results of a parsed expression.\n\n    Example::\n        source = "a, b, c,d"\n        wd = Word(alphas)\n        wd_list1 = wd + ZeroOrMore(\',\' + wd)\n        print(wd_list1.parseString(source))\n\n        # often, delimiters that are useful during parsing are just in the\n        # way afterward - use Suppress to keep them out of the parsed output\n        wd_list2 = wd + ZeroOrMore(Suppress(\',\') + wd)\n        print(wd_list2.parseString(source))\n    prints::\n        [\'a\', \',\', \'b\', \',\', \'c\', \',\', \'d\']\n        [\'a\', \'b\', \'c\', \'d\']\n    (See also L{delimitedList}.)\n    '

    def postParse(self, instring, loc, tokenlist):
        return []

    def suppress(self):
        return self


class OnlyOnce(object):
    __doc__ = '\n    Wrapper for parse actions, to ensure they are only called once.\n    '

    def __init__(self, methodCall):
        self.callable = _trim_arity(methodCall)
        self.called = False

    def __call__(self, s, l, t):
        if not self.called:
            results = self.callable(s, l, t)
            self.called = True
            return results
        raise ParseException(s, l, '')

    def reset(self):
        self.called = False


def traceParseAction(f):
    """
    Decorator for debugging parse actions. 
    
    When the parse action is called, this decorator will print C{">> entering I{method-name}(line:I{current_source_line}, I{parse_location}, I{matched_tokens})".}
    When the parse action completes, the decorator will print C{"<<"} followed by the returned value, or any exception that the parse action raised.

    Example::
        wd = Word(alphas)

        @traceParseAction
        def remove_duplicate_chars(tokens):
            return ''.join(sorted(set(''.join(tokens))))

        wds = OneOrMore(wd).setParseAction(remove_duplicate_chars)
        print(wds.parseString("slkdjs sld sldd sdlf sdljf"))
    prints::
        >>entering remove_duplicate_chars(line: 'slkdjs sld sldd sdlf sdljf', 0, (['slkdjs', 'sld', 'sldd', 'sdlf', 'sdljf'], {}))
        <<leaving remove_duplicate_chars (ret: 'dfjkls')
        ['dfjkls']
    """
    f = _trim_arity(f)

    def z(*paArgs):
        thisFunc = f.__name__
        s, l, t = paArgs[-3:]
        if len(paArgs) > 3:
            thisFunc = paArgs[0].__class__.__name__ + '.' + thisFunc
        sys.stderr.write(">>entering %s(line: '%s', %d, %r)\n" % (thisFunc, line(l, s), l, t))
        try:
            ret = f(*paArgs)
        except Exception as exc:
            try:
                sys.stderr.write('<<leaving %s (exception: %s)\n' % (thisFunc, exc))
                raise
            finally:
                exc = None
                del exc

        sys.stderr.write('<<leaving %s (ret: %r)\n' % (thisFunc, ret))
        return ret

    try:
        z.__name__ = f.__name__
    except AttributeError:
        pass

    return z


def delimitedList(expr, delim=',', combine=False):
    """
    Helper to define a delimited list of expressions - the delimiter defaults to ','.
    By default, the list elements and delimiters can have intervening whitespace, and
    comments, but this can be overridden by passing C{combine=True} in the constructor.
    If C{combine} is set to C{True}, the matching tokens are returned as a single token
    string, with the delimiters included; otherwise, the matching tokens are returned
    as a list of tokens, with the delimiters suppressed.

    Example::
        delimitedList(Word(alphas)).parseString("aa,bb,cc") # -> ['aa', 'bb', 'cc']
        delimitedList(Word(hexnums), delim=':', combine=True).parseString("AA:BB:CC:DD:EE") # -> ['AA:BB:CC:DD:EE']
    """
    dlName = _ustr(expr) + ' [' + _ustr(delim) + ' ' + _ustr(expr) + ']...'
    if combine:
        return Combine(expr + ZeroOrMore(delim + expr)).setName(dlName)
    return (expr + ZeroOrMore(Suppress(delim) + expr)).setName(dlName)


def countedArray(expr, intExpr=None):
    """
    Helper to define a counted list of expressions.
    This helper defines a pattern of the form::
        integer expr expr expr...
    where the leading integer tells how many expr expressions follow.
    The matched tokens returns the array of expr tokens as a list - the leading count token is suppressed.
    
    If C{intExpr} is specified, it should be a pyparsing expression that produces an integer value.

    Example::
        countedArray(Word(alphas)).parseString('2 ab cd ef')  # -> ['ab', 'cd']

        # in this parser, the leading integer value is given in binary,
        # '10' indicating that 2 values are in the array
        binaryConstant = Word('01').setParseAction(lambda t: int(t[0], 2))
        countedArray(Word(alphas), intExpr=binaryConstant).parseString('10 ab cd ef')  # -> ['ab', 'cd']
    """
    arrayExpr = Forward()

    def countFieldParseAction(s, l, t):
        n = t[0]
        arrayExpr << (n and Group(And([expr] * n)) or Group(empty))
        return []

    if intExpr is None:
        intExpr = Word(nums).setParseAction(lambda t: int(t[0]))
    else:
        intExpr = intExpr.copy()
    intExpr.setName('arrayLen')
    intExpr.addParseAction(countFieldParseAction, callDuringTry=True)
    return (intExpr + arrayExpr).setName('(len) ' + _ustr(expr) + '...')


def _flatten(L):
    ret = []
    for i in L:
        if isinstance(i, list):
            ret.extend(_flatten(i))
        else:
            ret.append(i)

    return ret


def matchPreviousLiteral(expr):
    """
    Helper to define an expression that is indirectly defined from
    the tokens matched in a previous expression, that is, it looks
    for a 'repeat' of a previous expression.  For example::
        first = Word(nums)
        second = matchPreviousLiteral(first)
        matchExpr = first + ":" + second
    will match C{"1:1"}, but not C{"1:2"}.  Because this matches a
    previous literal, will also match the leading C{"1:1"} in C{"1:10"}.
    If this is not desired, use C{matchPreviousExpr}.
    Do I{not} use with packrat parsing enabled.
    """
    rep = Forward()

    def copyTokenToRepeater(s, l, t):
        if t:
            if len(t) == 1:
                rep << t[0]
            else:
                tflat = _flatten(t.asList())
                rep << And((Literal(tt) for tt in tflat))
        else:
            rep << Empty()

    expr.addParseAction(copyTokenToRepeater, callDuringTry=True)
    rep.setName('(prev) ' + _ustr(expr))
    return rep


def matchPreviousExpr(expr):
    """
    Helper to define an expression that is indirectly defined from
    the tokens matched in a previous expression, that is, it looks
    for a 'repeat' of a previous expression.  For example::
        first = Word(nums)
        second = matchPreviousExpr(first)
        matchExpr = first + ":" + second
    will match C{"1:1"}, but not C{"1:2"}.  Because this matches by
    expressions, will I{not} match the leading C{"1:1"} in C{"1:10"};
    the expressions are evaluated first, and then compared, so
    C{"1"} is compared with C{"10"}.
    Do I{not} use with packrat parsing enabled.
    """
    rep = Forward()
    e2 = expr.copy()
    rep <<= e2

    def copyTokenToRepeater(s, l, t):
        matchTokens = _flatten(t.asList())

        def mustMatchTheseTokens(s, l, t):
            theseTokens = _flatten(t.asList())
            if theseTokens != matchTokens:
                raise ParseException('', 0, '')

        rep.setParseAction(mustMatchTheseTokens, callDuringTry=True)

    expr.addParseAction(copyTokenToRepeater, callDuringTry=True)
    rep.setName('(prev) ' + _ustr(expr))
    return rep


def _escapeRegexRangeChars(s):
    for c in '\\^-]':
        s = s.replace(c, _bslash + c)

    s = s.replace('\n', '\\n')
    s = s.replace('\t', '\\t')
    return _ustr(s)


def oneOf(strs, caseless=False, useRegex=True):
    """
    Helper to quickly define a set of alternative Literals, and makes sure to do
    longest-first testing when there is a conflict, regardless of the input order,
    but returns a C{L{MatchFirst}} for best performance.

    Parameters:
     - strs - a string of space-delimited literals, or a collection of string literals
     - caseless - (default=C{False}) - treat all literals as caseless
     - useRegex - (default=C{True}) - as an optimization, will generate a Regex
          object; otherwise, will generate a C{MatchFirst} object (if C{caseless=True}, or
          if creating a C{Regex} raises an exception)

    Example::
        comp_oper = oneOf("< = > <= >= !=")
        var = Word(alphas)
        number = Word(nums)
        term = var | number
        comparison_expr = term + comp_oper + term
        print(comparison_expr.searchString("B = 12  AA=23 B<=AA AA>12"))
    prints::
        [['B', '=', '12'], ['AA', '=', '23'], ['B', '<=', 'AA'], ['AA', '>', '12']]
    """
    if caseless:
        isequal = lambda a, b: a.upper() == b.upper()
        masks = lambda a, b: b.upper().startswith(a.upper())
        parseElementClass = CaselessLiteral
    else:
        isequal = lambda a, b: a == b
        masks = lambda a, b: b.startswith(a)
        parseElementClass = Literal
    symbols = []
    if isinstance(strs, basestring):
        symbols = strs.split()
    else:
        if isinstance(strs, Iterable):
            symbols = list(strs)
        else:
            warnings.warn('Invalid argument to oneOf, expected string or iterable', SyntaxWarning,
              stacklevel=2)
    if not symbols:
        return NoMatch()
    i = 0
    while i < len(symbols) - 1:
        cur = symbols[i]
        for j, other in enumerate(symbols[i + 1:]):
            if isequal(other, cur):
                del symbols[i + j + 1]
                break
            else:
                if masks(cur, other):
                    del symbols[i + j + 1]
                    symbols.insert(i, other)
                    cur = other
                    break
        else:
            i += 1

    if not caseless:
        if useRegex:
            try:
                if len(symbols) == len(''.join(symbols)):
                    return Regex('[%s]' % ''.join((_escapeRegexRangeChars(sym) for sym in symbols))).setName(' | '.join(symbols))
                return Regex('|'.join((re.escape(sym) for sym in symbols))).setName(' | '.join(symbols))
            except Exception:
                warnings.warn('Exception creating Regex for oneOf, building MatchFirst', SyntaxWarning,
                  stacklevel=2)

    return MatchFirst((parseElementClass(sym) for sym in symbols)).setName(' | '.join(symbols))


def dictOf(key, value):
    """
    Helper to easily and clearly define a dictionary by specifying the respective patterns
    for the key and value.  Takes care of defining the C{L{Dict}}, C{L{ZeroOrMore}}, and C{L{Group}} tokens
    in the proper order.  The key pattern can include delimiting markers or punctuation,
    as long as they are suppressed, thereby leaving the significant key text.  The value
    pattern can include named results, so that the C{Dict} results can include named token
    fields.

    Example::
        text = "shape: SQUARE posn: upper left color: light blue texture: burlap"
        attr_expr = (label + Suppress(':') + OneOrMore(data_word, stopOn=label).setParseAction(' '.join))
        print(OneOrMore(attr_expr).parseString(text).dump())
        
        attr_label = label
        attr_value = Suppress(':') + OneOrMore(data_word, stopOn=label).setParseAction(' '.join)

        # similar to Dict, but simpler call format
        result = dictOf(attr_label, attr_value).parseString(text)
        print(result.dump())
        print(result['shape'])
        print(result.shape)  # object attribute access works too
        print(result.asDict())
    prints::
        [['shape', 'SQUARE'], ['posn', 'upper left'], ['color', 'light blue'], ['texture', 'burlap']]
        - color: light blue
        - posn: upper left
        - shape: SQUARE
        - texture: burlap
        SQUARE
        SQUARE
        {'color': 'light blue', 'shape': 'SQUARE', 'posn': 'upper left', 'texture': 'burlap'}
    """
    return Dict(ZeroOrMore(Group(key + value)))


def originalTextFor(expr, asString=True):
    """
    Helper to return the original, untokenized text for a given expression.  Useful to
    restore the parsed fields of an HTML start tag into the raw tag text itself, or to
    revert separate tokens with intervening whitespace back to the original matching
    input text. By default, returns astring containing the original parsed text.  
       
    If the optional C{asString} argument is passed as C{False}, then the return value is a 
    C{L{ParseResults}} containing any results names that were originally matched, and a 
    single token containing the original matched text from the input string.  So if 
    the expression passed to C{L{originalTextFor}} contains expressions with defined
    results names, you must set C{asString} to C{False} if you want to preserve those
    results name values.

    Example::
        src = "this is test <b> bold <i>text</i> </b> normal text "
        for tag in ("b","i"):
            opener,closer = makeHTMLTags(tag)
            patt = originalTextFor(opener + SkipTo(closer) + closer)
            print(patt.searchString(src)[0])
    prints::
        ['<b> bold <i>text</i> </b>']
        ['<i>text</i>']
    """
    locMarker = Empty().setParseAction(lambda s, loc, t: loc)
    endlocMarker = locMarker.copy()
    endlocMarker.callPreparse = False
    matchExpr = locMarker('_original_start') + expr + endlocMarker('_original_end')
    if asString:
        extractText = lambda s, l, t: s[t._original_start:t._original_end]
    else:

        def extractText(s, l, t):
            t[:] = [
             s[t.pop('_original_start'):t.pop('_original_end')]]

    matchExpr.setParseAction(extractText)
    matchExpr.ignoreExprs = expr.ignoreExprs
    return matchExpr


def ungroup(expr):
    """
    Helper to undo pyparsing's default grouping of And expressions, even
    if all but one are non-empty.
    """
    return TokenConverter(expr).setParseAction(lambda t: t[0])


def locatedExpr(expr):
    """
    Helper to decorate a returned token with its starting and ending locations in the input string.
    This helper adds the following results names:
     - locn_start = location where matched expression begins
     - locn_end = location where matched expression ends
     - value = the actual parsed results

    Be careful if the input text contains C{<TAB>} characters, you may want to call
    C{L{ParserElement.parseWithTabs}}

    Example::
        wd = Word(alphas)
        for match in locatedExpr(wd).searchString("ljsdf123lksdjjf123lkkjj1222"):
            print(match)
    prints::
        [[0, 'ljsdf', 5]]
        [[8, 'lksdjjf', 15]]
        [[18, 'lkkjj', 23]]
    """
    locator = Empty().setParseAction(lambda s, l, t: l)
    return Group(locator('locn_start') + expr('value') + locator.copy().leaveWhitespace()('locn_end'))


empty = Empty().setName('empty')
lineStart = LineStart().setName('lineStart')
lineEnd = LineEnd().setName('lineEnd')
stringStart = StringStart().setName('stringStart')
stringEnd = StringEnd().setName('stringEnd')
_escapedPunc = Word(_bslash, '\\[]-*.$+^?()~ ', exact=2).setParseAction(lambda s, l, t: t[0][1])
_escapedHexChar = Regex('\\\\0?[xX][0-9a-fA-F]+').setParseAction(lambda s, l, t: unichr(int(t[0].lstrip('\\0x'), 16)))
_escapedOctChar = Regex('\\\\0[0-7]+').setParseAction(lambda s, l, t: unichr(int(t[0][1:], 8)))
_singleChar = _escapedPunc | _escapedHexChar | _escapedOctChar | CharsNotIn('\\]', exact=1)
_charRange = Group(_singleChar + Suppress('-') + _singleChar)
_reBracketExpr = Literal('[') + Optional('^').setResultsName('negate') + Group(OneOrMore(_charRange | _singleChar)).setResultsName('body') + ']'

def srange(s):
    r"""
    Helper to easily define string ranges for use in Word construction.  Borrows
    syntax from regexp '[]' string range definitions::
        srange("[0-9]")   -> "0123456789"
        srange("[a-z]")   -> "abcdefghijklmnopqrstuvwxyz"
        srange("[a-z$_]") -> "abcdefghijklmnopqrstuvwxyz$_"
    The input string must be enclosed in []'s, and the returned string is the expanded
    character set joined into a single string.
    The values enclosed in the []'s may be:
     - a single character
     - an escaped character with a leading backslash (such as C{\-} or C{\]})
     - an escaped hex character with a leading C{'\x'} (C{\x21}, which is a C{'!'} character) 
         (C{\0x##} is also supported for backwards compatibility) 
     - an escaped octal character with a leading C{'\0'} (C{\041}, which is a C{'!'} character)
     - a range of any of the above, separated by a dash (C{'a-z'}, etc.)
     - any combination of the above (C{'aeiouy'}, C{'a-zA-Z0-9_$'}, etc.)
    """
    _expanded = lambda p:     if not isinstance(p, ParseResults):
p # Avoid dead code: ''.join((unichr(c) for c in range(ord(p[0]), ord(p[1]) + 1)))
    try:
        return ''.join((_expanded(part) for part in _reBracketExpr.parseString(s).body))
    except Exception:
        return ''


def matchOnlyAtCol(n):
    """
    Helper method for defining parse actions that require matching at a specific
    column in the input text.
    """

    def verifyCol(strg, locn, toks):
        if col(locn, strg) != n:
            raise ParseException(strg, locn, 'matched token not at column %d' % n)

    return verifyCol


def replaceWith(replStr):
    """
    Helper method for common parse actions that simply return a literal value.  Especially
    useful when used with C{L{transformString<ParserElement.transformString>}()}.

    Example::
        num = Word(nums).setParseAction(lambda toks: int(toks[0]))
        na = oneOf("N/A NA").setParseAction(replaceWith(math.nan))
        term = na | num
        
        OneOrMore(term).parseString("324 234 N/A 234") # -> [324, 234, nan, 234]
    """
    return lambda s, l, t: [
     replStr]


def removeQuotes(s, l, t):
    """
    Helper parse action for removing quotation marks from parsed quoted strings.

    Example::
        # by default, quotation marks are included in parsed results
        quotedString.parseString("'Now is the Winter of our Discontent'") # -> ["'Now is the Winter of our Discontent'"]

        # use removeQuotes to strip quotation marks from parsed results
        quotedString.setParseAction(removeQuotes)
        quotedString.parseString("'Now is the Winter of our Discontent'") # -> ["Now is the Winter of our Discontent"]
    """
    return t[0][1:-1]


def tokenMap(func, *args):
    """
    Helper to define a parse action by mapping a function to all elements of a ParseResults list.If any additional 
    args are passed, they are forwarded to the given function as additional arguments after
    the token, as in C{hex_integer = Word(hexnums).setParseAction(tokenMap(int, 16))}, which will convert the
    parsed data to an integer using base 16.

    Example (compare the last to example in L{ParserElement.transformString}::
        hex_ints = OneOrMore(Word(hexnums)).setParseAction(tokenMap(int, 16))
        hex_ints.runTests('''
            00 11 22 aa FF 0a 0d 1a
            ''')
        
        upperword = Word(alphas).setParseAction(tokenMap(str.upper))
        OneOrMore(upperword).runTests('''
            my kingdom for a horse
            ''')

        wd = Word(alphas).setParseAction(tokenMap(str.title))
        OneOrMore(wd).setParseAction(' '.join).runTests('''
            now is the winter of our discontent made glorious summer by this sun of york
            ''')
    prints::
        00 11 22 aa FF 0a 0d 1a
        [0, 17, 34, 170, 255, 10, 13, 26]

        my kingdom for a horse
        ['MY', 'KINGDOM', 'FOR', 'A', 'HORSE']

        now is the winter of our discontent made glorious summer by this sun of york
        ['Now Is The Winter Of Our Discontent Made Glorious Summer By This Sun Of York']
    """

    def pa(s, l, t):
        return [func(tokn, *args) for tokn in t]

    try:
        func_name = getattr(func, '__name__', getattr(func, '__class__').__name__)
    except Exception:
        func_name = str(func)

    pa.__name__ = func_name
    return pa


upcaseTokens = tokenMap(lambda t: _ustr(t).upper())
downcaseTokens = tokenMap(lambda t: _ustr(t).lower())

def _makeTags(tagStr, xml):
    """Internal helper to construct opening and closing tag expressions, given a tag name"""
    if isinstance(tagStr, basestring):
        resname = tagStr
        tagStr = Keyword(tagStr, caseless=(not xml))
    else:
        resname = tagStr.name
    tagAttrName = Word(alphas, alphanums + '_-:')
    if xml:
        tagAttrValue = dblQuotedString.copy().setParseAction(removeQuotes)
        openTag = Suppress('<') + tagStr('tag') + Dict(ZeroOrMore(Group(tagAttrName + Suppress('=') + tagAttrValue))) + Optional('/', default=[False]).setResultsName('empty').setParseAction(lambda s, l, t: t[0] == '/') + Suppress('>')
    else:
        printablesLessRAbrack = ''.join((c for c in printables if c not in '>'))
        tagAttrValue = quotedString.copy().setParseAction(removeQuotes) | Word(printablesLessRAbrack)
        openTag = Suppress('<') + tagStr('tag') + Dict(ZeroOrMore(Group(tagAttrName.setParseAction(downcaseTokens) + Optional(Suppress('=') + tagAttrValue)))) + Optional('/', default=[False]).setResultsName('empty').setParseAction(lambda s, l, t: t[0] == '/') + Suppress('>')
    closeTag = Combine(_L('</') + tagStr + '>')
    openTag = openTag.setResultsName('start' + ''.join(resname.replace(':', ' ').title().split())).setName('<%s>' % resname)
    closeTag = closeTag.setResultsName('end' + ''.join(resname.replace(':', ' ').title().split())).setName('</%s>' % resname)
    openTag.tag = resname
    closeTag.tag = resname
    return (openTag, closeTag)


def makeHTMLTags(tagStr):
    """
    Helper to construct opening and closing tag expressions for HTML, given a tag name. Matches
    tags in either upper or lower case, attributes with namespaces and with quoted or unquoted values.

    Example::
        text = '<td>More info at the <a href="http://pyparsing.wikispaces.com">pyparsing</a> wiki page</td>'
        # makeHTMLTags returns pyparsing expressions for the opening and closing tags as a 2-tuple
        a,a_end = makeHTMLTags("A")
        link_expr = a + SkipTo(a_end)("link_text") + a_end
        
        for link in link_expr.searchString(text):
            # attributes in the <A> tag (like "href" shown here) are also accessible as named results
            print(link.link_text, '->', link.href)
    prints::
        pyparsing -> http://pyparsing.wikispaces.com
    """
    return _makeTags(tagStr, False)


def makeXMLTags(tagStr):
    """
    Helper to construct opening and closing tag expressions for XML, given a tag name. Matches
    tags only in the given upper/lower case.

    Example: similar to L{makeHTMLTags}
    """
    return _makeTags(tagStr, True)


def withAttribute(*args, **attrDict):
    """
    Helper to create a validating parse action to be used with start tags created
    with C{L{makeXMLTags}} or C{L{makeHTMLTags}}. Use C{withAttribute} to qualify a starting tag
    with a required attribute value, to avoid false matches on common tags such as
    C{<TD>} or C{<DIV>}.

    Call C{withAttribute} with a series of attribute names and values. Specify the list
    of filter attributes names and values as:
     - keyword arguments, as in C{(align="right")}, or
     - as an explicit dict with C{**} operator, when an attribute name is also a Python
          reserved word, as in C{**{"class":"Customer", "align":"right"}}
     - a list of name-value tuples, as in ( ("ns1:class", "Customer"), ("ns2:align","right") )
    For attribute names with a namespace prefix, you must use the second form.  Attribute
    names are matched insensitive to upper/lower case.
       
    If just testing for C{class} (with or without a namespace), use C{L{withClass}}.

    To verify that the attribute exists, but without specifying a value, pass
    C{withAttribute.ANY_VALUE} as the value.

    Example::
        html = '''
            <div>
            Some text
            <div type="grid">1 4 0 1 0</div>
            <div type="graph">1,3 2,3 1,1</div>
            <div>this has no type</div>
            </div>
                
        '''
        div,div_end = makeHTMLTags("div")

        # only match div tag having a type attribute with value "grid"
        div_grid = div().setParseAction(withAttribute(type="grid"))
        grid_expr = div_grid + SkipTo(div | div_end)("body")
        for grid_header in grid_expr.searchString(html):
            print(grid_header.body)
        
        # construct a match with any div tag having a type attribute, regardless of the value
        div_any_type = div().setParseAction(withAttribute(type=withAttribute.ANY_VALUE))
        div_expr = div_any_type + SkipTo(div | div_end)("body")
        for div_header in div_expr.searchString(html):
            print(div_header.body)
    prints::
        1 4 0 1 0

        1 4 0 1 0
        1,3 2,3 1,1
    """
    if args:
        attrs = args[:]
    else:
        attrs = attrDict.items()
    attrs = [(k, v) for k, v in attrs]

    def pa(s, l, tokens):
        for attrName, attrValue in attrs:
            if attrName not in tokens:
                raise ParseException(s, l, 'no matching attribute ' + attrName)
            if attrValue != withAttribute.ANY_VALUE and tokens[attrName] != attrValue:
                raise ParseException(s, l, "attribute '%s' has value '%s', must be '%s'" % (
                 attrName, tokens[attrName], attrValue))

    return pa


withAttribute.ANY_VALUE = object()

def withClass(classname, namespace=''):
    """
    Simplified version of C{L{withAttribute}} when matching on a div class - made
    difficult because C{class} is a reserved word in Python.

    Example::
        html = '''
            <div>
            Some text
            <div class="grid">1 4 0 1 0</div>
            <div class="graph">1,3 2,3 1,1</div>
            <div>this &lt;div&gt; has no class</div>
            </div>
                
        '''
        div,div_end = makeHTMLTags("div")
        div_grid = div().setParseAction(withClass("grid"))
        
        grid_expr = div_grid + SkipTo(div | div_end)("body")
        for grid_header in grid_expr.searchString(html):
            print(grid_header.body)
        
        div_any_type = div().setParseAction(withClass(withAttribute.ANY_VALUE))
        div_expr = div_any_type + SkipTo(div | div_end)("body")
        for div_header in div_expr.searchString(html):
            print(div_header.body)
    prints::
        1 4 0 1 0

        1 4 0 1 0
        1,3 2,3 1,1
    """
    classattr = '%s:class' % namespace if namespace else 'class'
    return withAttribute(**{classattr: classname})


opAssoc = _Constants()
opAssoc.LEFT = object()
opAssoc.RIGHT = object()

def infixNotation(baseExpr, opList, lpar=Suppress('('), rpar=Suppress(')')):
    """
    Helper method for constructing grammars of expressions made up of
    operators working in a precedence hierarchy.  Operators may be unary or
    binary, left- or right-associative.  Parse actions can also be attached
    to operator expressions. The generated parser will also recognize the use 
    of parentheses to override operator precedences (see example below).
    
    Note: if you define a deep operator list, you may see performance issues
    when using infixNotation. See L{ParserElement.enablePackrat} for a
    mechanism to potentially improve your parser performance.

    Parameters:
     - baseExpr - expression representing the most basic element for the nested
     - opList - list of tuples, one for each operator precedence level in the
      expression grammar; each tuple is of the form
      (opExpr, numTerms, rightLeftAssoc, parseAction), where:
       - opExpr is the pyparsing expression for the operator;
          may also be a string, which will be converted to a Literal;
          if numTerms is 3, opExpr is a tuple of two expressions, for the
          two operators separating the 3 terms
       - numTerms is the number of terms for this operator (must
          be 1, 2, or 3)
       - rightLeftAssoc is the indicator whether the operator is
          right or left associative, using the pyparsing-defined
          constants C{opAssoc.RIGHT} and C{opAssoc.LEFT}.
       - parseAction is the parse action to be associated with
          expressions matching this operator expression (the
          parse action tuple member may be omitted); if the parse action
          is passed a tuple or list of functions, this is equivalent to
          calling C{setParseAction(*fn)} (L{ParserElement.setParseAction})
     - lpar - expression for matching left-parentheses (default=C{Suppress('(')})
     - rpar - expression for matching right-parentheses (default=C{Suppress(')')})

    Example::
        # simple example of four-function arithmetic with ints and variable names
        integer = pyparsing_common.signed_integer
        varname = pyparsing_common.identifier 
        
        arith_expr = infixNotation(integer | varname,
            [
            ('-', 1, opAssoc.RIGHT),
            (oneOf('* /'), 2, opAssoc.LEFT),
            (oneOf('+ -'), 2, opAssoc.LEFT),
            ])
        
        arith_expr.runTests('''
            5+3*6
            (5+3)*6
            -2--11
            ''', fullDump=False)
    prints::
        5+3*6
        [[5, '+', [3, '*', 6]]]

        (5+3)*6
        [[[5, '+', 3], '*', 6]]

        -2--11
        [[['-', 2], '-', ['-', 11]]]
    """
    ret = Forward()
    lastExpr = baseExpr | lpar + ret + rpar
    for i, operDef in enumerate(opList):
        opExpr, arity, rightLeftAssoc, pa = (operDef + (None, ))[:4]
        termName = '%s term' % opExpr if arity < 3 else '%s%s term' % opExpr
        if arity == 3:
            if not opExpr is None:
                if len(opExpr) != 2:
                    raise ValueError('if numterms=3, opExpr must be a tuple or list of two expressions')
                opExpr1, opExpr2 = opExpr
            else:
                thisExpr = Forward().setName(termName)
                if rightLeftAssoc == opAssoc.LEFT:
                    if arity == 1:
                        matchExpr = FollowedBy(lastExpr + opExpr) + Group(lastExpr + OneOrMore(opExpr))
                    else:
                        if arity == 2:
                            if opExpr is not None:
                                matchExpr = FollowedBy(lastExpr + opExpr + lastExpr) + Group(lastExpr + OneOrMore(opExpr + lastExpr))
                            else:
                                matchExpr = FollowedBy(lastExpr + lastExpr) + Group(lastExpr + OneOrMore(lastExpr))
                        else:
                            if arity == 3:
                                matchExpr = FollowedBy(lastExpr + opExpr1 + lastExpr + opExpr2 + lastExpr) + Group(lastExpr + opExpr1 + lastExpr + opExpr2 + lastExpr)
                            else:
                                raise ValueError('operator must be unary (1), binary (2), or ternary (3)')
                else:
                    if rightLeftAssoc == opAssoc.RIGHT:
                        if arity == 1:
                            if not isinstance(opExpr, Optional):
                                opExpr = Optional(opExpr)
                            matchExpr = FollowedBy(opExpr.expr + thisExpr) + Group(opExpr + thisExpr)
                        else:
                            if arity == 2:
                                if opExpr is not None:
                                    matchExpr = FollowedBy(lastExpr + opExpr + thisExpr) + Group(lastExpr + OneOrMore(opExpr + thisExpr))
                                else:
                                    matchExpr = FollowedBy(lastExpr + thisExpr) + Group(lastExpr + OneOrMore(thisExpr))
                            else:
                                if arity == 3:
                                    matchExpr = FollowedBy(lastExpr + opExpr1 + thisExpr + opExpr2 + thisExpr) + Group(lastExpr + opExpr1 + thisExpr + opExpr2 + thisExpr)
                                else:
                                    raise ValueError('operator must be unary (1), binary (2), or ternary (3)')
                    else:
                        raise ValueError('operator must indicate right or left associativity')
            if pa:
                if isinstance(pa, (tuple, list)):
                    (matchExpr.setParseAction)(*pa)
        else:
            matchExpr.setParseAction(pa)
        thisExpr <<= matchExpr.setName(termName) | lastExpr
        lastExpr = thisExpr

    ret <<= lastExpr
    return ret


operatorPrecedence = infixNotation
dblQuotedString = Combine(Regex('"(?:[^"\\n\\r\\\\]|(?:"")|(?:\\\\(?:[^x]|x[0-9a-fA-F]+)))*') + '"').setName('string enclosed in double quotes')
sglQuotedString = Combine(Regex("'(?:[^'\\n\\r\\\\]|(?:'')|(?:\\\\(?:[^x]|x[0-9a-fA-F]+)))*") + "'").setName('string enclosed in single quotes')
quotedString = Combine(Regex('"(?:[^"\\n\\r\\\\]|(?:"")|(?:\\\\(?:[^x]|x[0-9a-fA-F]+)))*') + '"' | Regex("'(?:[^'\\n\\r\\\\]|(?:'')|(?:\\\\(?:[^x]|x[0-9a-fA-F]+)))*") + "'").setName('quotedString using single or double quotes')
unicodeString = Combine(_L('u') + quotedString.copy()).setName('unicode string literal')

def nestedExpr(opener='(', closer=')', content=None, ignoreExpr=quotedString.copy()):
    """
    Helper method for defining nested lists enclosed in opening and closing
    delimiters ("(" and ")" are the default).

    Parameters:
     - opener - opening character for a nested list (default=C{"("}); can also be a pyparsing expression
     - closer - closing character for a nested list (default=C{")"}); can also be a pyparsing expression
     - content - expression for items within the nested lists (default=C{None})
     - ignoreExpr - expression for ignoring opening and closing delimiters (default=C{quotedString})

    If an expression is not provided for the content argument, the nested
    expression will capture all whitespace-delimited content between delimiters
    as a list of separate values.

    Use the C{ignoreExpr} argument to define expressions that may contain
    opening or closing characters that should not be treated as opening
    or closing characters for nesting, such as quotedString or a comment
    expression.  Specify multiple expressions using an C{L{Or}} or C{L{MatchFirst}}.
    The default is L{quotedString}, but if no expressions are to be ignored,
    then pass C{None} for this argument.

    Example::
        data_type = oneOf("void int short long char float double")
        decl_data_type = Combine(data_type + Optional(Word('*')))
        ident = Word(alphas+'_', alphanums+'_')
        number = pyparsing_common.number
        arg = Group(decl_data_type + ident)
        LPAR,RPAR = map(Suppress, "()")

        code_body = nestedExpr('{', '}', ignoreExpr=(quotedString | cStyleComment))

        c_function = (decl_data_type("type") 
                      + ident("name")
                      + LPAR + Optional(delimitedList(arg), [])("args") + RPAR 
                      + code_body("body"))
        c_function.ignore(cStyleComment)
        
        source_code = '''
            int is_odd(int x) { 
                return (x%2); 
            }
                
            int dec_to_hex(char hchar) { 
                if (hchar >= '0' && hchar <= '9') { 
                    return (ord(hchar)-ord('0')); 
                } else { 
                    return (10+ord(hchar)-ord('A'));
                } 
            }
        '''
        for func in c_function.searchString(source_code):
            print("%(name)s (%(type)s) args: %(args)s" % func)

    prints::
        is_odd (int) args: [['int', 'x']]
        dec_to_hex (int) args: [['char', 'hchar']]
    """
    if opener == closer:
        raise ValueError('opening and closing strings cannot be the same')
    else:
        if content is None:
            if isinstance(opener, basestring) and isinstance(closer, basestring):
                if len(opener) == 1:
                    if len(closer) == 1:
                        if ignoreExpr is not None:
                            content = Combine(OneOrMore(~ignoreExpr + CharsNotIn((opener + closer + ParserElement.DEFAULT_WHITE_CHARS), exact=1))).setParseAction(lambda t: t[0].strip())
                    else:
                        content = empty.copy() + CharsNotIn(opener + closer + ParserElement.DEFAULT_WHITE_CHARS).setParseAction(lambda t: t[0].strip())
                else:
                    if ignoreExpr is not None:
                        content = Combine(OneOrMore(~ignoreExpr + ~Literal(opener) + ~Literal(closer) + CharsNotIn((ParserElement.DEFAULT_WHITE_CHARS), exact=1))).setParseAction(lambda t: t[0].strip())
                    else:
                        content = Combine(OneOrMore(~Literal(opener) + ~Literal(closer) + CharsNotIn((ParserElement.DEFAULT_WHITE_CHARS), exact=1))).setParseAction(lambda t: t[0].strip())
            else:
                raise ValueError('opening and closing arguments must be strings if no content expression is given')
        ret = Forward()
        if ignoreExpr is not None:
            ret <<= Group(Suppress(opener) + ZeroOrMore(ignoreExpr | ret | content) + Suppress(closer))
        else:
            ret <<= Group(Suppress(opener) + ZeroOrMore(ret | content) + Suppress(closer))
    ret.setName('nested %s%s expression' % (opener, closer))
    return ret


def indentedBlock(blockStatementExpr, indentStack, indent=True):
    """
    Helper method for defining space-delimited indentation blocks, such as
    those used to define block statements in Python source code.

    Parameters:
     - blockStatementExpr - expression defining syntax of statement that
            is repeated within the indented block
     - indentStack - list created by caller to manage indentation stack
            (multiple statementWithIndentedBlock expressions within a single grammar
            should share a common indentStack)
     - indent - boolean indicating whether block must be indented beyond the
            the current level; set to False for block of left-most statements
            (default=C{True})

    A valid block must contain at least one C{blockStatement}.

    Example::
        data = '''
        def A(z):
          A1
          B = 100
          G = A2
          A2
          A3
        B
        def BB(a,b,c):
          BB1
          def BBA():
            bba1
            bba2
            bba3
        C
        D
        def spam(x,y):
             def eggs(z):
                 pass
        '''

        indentStack = [1]
        stmt = Forward()

        identifier = Word(alphas, alphanums)
        funcDecl = ("def" + identifier + Group( "(" + Optional( delimitedList(identifier) ) + ")" ) + ":")
        func_body = indentedBlock(stmt, indentStack)
        funcDef = Group( funcDecl + func_body )

        rvalue = Forward()
        funcCall = Group(identifier + "(" + Optional(delimitedList(rvalue)) + ")")
        rvalue << (funcCall | identifier | Word(nums))
        assignment = Group(identifier + "=" + rvalue)
        stmt << ( funcDef | assignment | identifier )

        module_body = OneOrMore(stmt)

        parseTree = module_body.parseString(data)
        parseTree.pprint()
    prints::
        [['def',
          'A',
          ['(', 'z', ')'],
          ':',
          [['A1'], [['B', '=', '100']], [['G', '=', 'A2']], ['A2'], ['A3']]],
         'B',
         ['def',
          'BB',
          ['(', 'a', 'b', 'c', ')'],
          ':',
          [['BB1'], [['def', 'BBA', ['(', ')'], ':', [['bba1'], ['bba2'], ['bba3']]]]]],
         'C',
         'D',
         ['def',
          'spam',
          ['(', 'x', 'y', ')'],
          ':',
          [[['def', 'eggs', ['(', 'z', ')'], ':', [['pass']]]]]]] 
    """

    def checkPeerIndent(s, l, t):
        if l >= len(s):
            return
        curCol = col(l, s)
        if curCol != indentStack[(-1)]:
            if curCol > indentStack[(-1)]:
                raise ParseFatalException(s, l, 'illegal nesting')
            raise ParseException(s, l, 'not a peer entry')

    def checkSubIndent(s, l, t):
        curCol = col(l, s)
        if curCol > indentStack[(-1)]:
            indentStack.append(curCol)
        else:
            raise ParseException(s, l, 'not a subentry')

    def checkUnindent(s, l, t):
        if l >= len(s):
            return
        curCol = col(l, s)
        if not (indentStack and curCol < indentStack[(-1)] and curCol <= indentStack[(-2)]):
            raise ParseException(s, l, 'not an unindent')
        indentStack.pop()

    NL = OneOrMore(LineEnd().setWhitespaceChars('\t ').suppress())
    INDENT = (Empty() + Empty().setParseAction(checkSubIndent)).setName('INDENT')
    PEER = Empty().setParseAction(checkPeerIndent).setName('')
    UNDENT = Empty().setParseAction(checkUnindent).setName('UNINDENT')
    if indent:
        smExpr = Group(Optional(NL) + INDENT + OneOrMore(PEER + Group(blockStatementExpr) + Optional(NL)) + UNDENT)
    else:
        smExpr = Group(Optional(NL) + OneOrMore(PEER + Group(blockStatementExpr) + Optional(NL)))
    blockStatementExpr.ignore(_bslash + LineEnd())
    return smExpr.setName('indented block')


alphas8bit = srange('[\\0xc0-\\0xd6\\0xd8-\\0xf6\\0xf8-\\0xff]')
punc8bit = srange('[\\0xa1-\\0xbf\\0xd7\\0xf7]')
anyOpenTag, anyCloseTag = makeHTMLTags(Word(alphas, alphanums + '_:').setName('any tag'))
_htmlEntityMap = dict(zip('gt lt amp nbsp quot apos'.split(), '><& "\''))
commonHTMLEntity = Regex('&(?P<entity>' + '|'.join(_htmlEntityMap.keys()) + ');').setName('common HTML entity')

def replaceHTMLEntity(t):
    """Helper parser action to replace common HTML entities with their special characters"""
    return _htmlEntityMap.get(t.entity)


cStyleComment = Combine(Regex('/\\*(?:[^*]|\\*(?!/))*') + '*/').setName('C style comment')
htmlComment = Regex('<!--[\\s\\S]*?-->').setName('HTML comment')
restOfLine = Regex('.*').leaveWhitespace().setName('rest of line')
dblSlashComment = Regex('//(?:\\\\\\n|[^\\n])*').setName('// comment')
cppStyleComment = Combine(Regex('/\\*(?:[^*]|\\*(?!/))*') + '*/' | dblSlashComment).setName('C++ style comment')
javaStyleComment = cppStyleComment
pythonStyleComment = Regex('#.*').setName('Python style comment')
_commasepitem = Combine(OneOrMore(Word(printables, excludeChars=',') + Optional(Word(' \t') + ~Literal(',') + ~LineEnd()))).streamline().setName('commaItem')
commaSeparatedList = delimitedList(Optional((quotedString.copy() | _commasepitem), default='')).setName('commaSeparatedList')

class pyparsing_common:
    __doc__ = "\n    Here are some common low-level expressions that may be useful in jump-starting parser development:\n     - numeric forms (L{integers<integer>}, L{reals<real>}, L{scientific notation<sci_real>})\n     - common L{programming identifiers<identifier>}\n     - network addresses (L{MAC<mac_address>}, L{IPv4<ipv4_address>}, L{IPv6<ipv6_address>})\n     - ISO8601 L{dates<iso8601_date>} and L{datetime<iso8601_datetime>}\n     - L{UUID<uuid>}\n     - L{comma-separated list<comma_separated_list>}\n    Parse actions:\n     - C{L{convertToInteger}}\n     - C{L{convertToFloat}}\n     - C{L{convertToDate}}\n     - C{L{convertToDatetime}}\n     - C{L{stripHTMLTags}}\n     - C{L{upcaseTokens}}\n     - C{L{downcaseTokens}}\n\n    Example::\n        pyparsing_common.number.runTests('''\n            # any int or real number, returned as the appropriate type\n            100\n            -100\n            +100\n            3.14159\n            6.02e23\n            1e-12\n            ''')\n\n        pyparsing_common.fnumber.runTests('''\n            # any int or real number, returned as float\n            100\n            -100\n            +100\n            3.14159\n            6.02e23\n            1e-12\n            ''')\n\n        pyparsing_common.hex_integer.runTests('''\n            # hex numbers\n            100\n            FF\n            ''')\n\n        pyparsing_common.fraction.runTests('''\n            # fractions\n            1/2\n            -3/4\n            ''')\n\n        pyparsing_common.mixed_integer.runTests('''\n            # mixed fractions\n            1\n            1/2\n            -3/4\n            1-3/4\n            ''')\n\n        import uuid\n        pyparsing_common.uuid.setParseAction(tokenMap(uuid.UUID))\n        pyparsing_common.uuid.runTests('''\n            # uuid\n            12345678-1234-5678-1234-567812345678\n            ''')\n    prints::\n        # any int or real number, returned as the appropriate type\n        100\n        [100]\n\n        -100\n        [-100]\n\n        +100\n        [100]\n\n        3.14159\n        [3.14159]\n\n        6.02e23\n        [6.02e+23]\n\n        1e-12\n        [1e-12]\n\n        # any int or real number, returned as float\n        100\n        [100.0]\n\n        -100\n        [-100.0]\n\n        +100\n        [100.0]\n\n        3.14159\n        [3.14159]\n\n        6.02e23\n        [6.02e+23]\n\n        1e-12\n        [1e-12]\n\n        # hex numbers\n        100\n        [256]\n\n        FF\n        [255]\n\n        # fractions\n        1/2\n        [0.5]\n\n        -3/4\n        [-0.75]\n\n        # mixed fractions\n        1\n        [1]\n\n        1/2\n        [0.5]\n\n        -3/4\n        [-0.75]\n\n        1-3/4\n        [1.75]\n\n        # uuid\n        12345678-1234-5678-1234-567812345678\n        [UUID('12345678-1234-5678-1234-567812345678')]\n    "
    convertToInteger = tokenMap(int)
    convertToFloat = tokenMap(float)
    integer = Word(nums).setName('integer').setParseAction(convertToInteger)
    hex_integer = Word(hexnums).setName('hex integer').setParseAction(tokenMap(int, 16))
    signed_integer = Regex('[+-]?\\d+').setName('signed integer').setParseAction(convertToInteger)
    fraction = (signed_integer().setParseAction(convertToFloat) + '/' + signed_integer().setParseAction(convertToFloat)).setName('fraction')
    fraction.addParseAction(lambda t: t[0] / t[(-1)])
    mixed_integer = (fraction | signed_integer + Optional(Optional('-').suppress() + fraction)).setName('fraction or mixed integer-fraction')
    mixed_integer.addParseAction(sum)
    real = Regex('[+-]?\\d+\\.\\d*').setName('real number').setParseAction(convertToFloat)
    sci_real = Regex('[+-]?\\d+([eE][+-]?\\d+|\\.\\d*([eE][+-]?\\d+)?)').setName('real number with scientific notation').setParseAction(convertToFloat)
    number = (sci_real | real | signed_integer).streamline()
    fnumber = Regex('[+-]?\\d+\\.?\\d*([eE][+-]?\\d+)?').setName('fnumber').setParseAction(convertToFloat)
    identifier = Word(alphas + '_', alphanums + '_').setName('identifier')
    ipv4_address = Regex('(25[0-5]|2[0-4][0-9]|1?[0-9]{1,2})(\\.(25[0-5]|2[0-4][0-9]|1?[0-9]{1,2})){3}').setName('IPv4 address')
    _ipv6_part = Regex('[0-9a-fA-F]{1,4}').setName('hex_integer')
    _full_ipv6_address = (_ipv6_part + (':' + _ipv6_part) * 7).setName('full IPv6 address')
    _short_ipv6_address = (Optional(_ipv6_part + (':' + _ipv6_part) * (0, 6)) + '::' + Optional(_ipv6_part + (':' + _ipv6_part) * (0,
                                                                                                                                   6))).setName('short IPv6 address')
    _short_ipv6_address.addCondition(lambda t: sum((1 for tt in t if pyparsing_common._ipv6_part.matches(tt))) < 8)
    _mixed_ipv6_address = ('::ffff:' + ipv4_address).setName('mixed IPv6 address')
    ipv6_address = Combine((_full_ipv6_address | _mixed_ipv6_address | _short_ipv6_address).setName('IPv6 address')).setName('IPv6 address')
    mac_address = Regex('[0-9a-fA-F]{2}([:.-])[0-9a-fA-F]{2}(?:\\1[0-9a-fA-F]{2}){4}').setName('MAC address')

    @staticmethod
    def convertToDate(fmt='%Y-%m-%d'):
        """
        Helper to create a parse action for converting parsed date string to Python datetime.date

        Params -
         - fmt - format to be passed to datetime.strptime (default=C{"%Y-%m-%d"})

        Example::
            date_expr = pyparsing_common.iso8601_date.copy()
            date_expr.setParseAction(pyparsing_common.convertToDate())
            print(date_expr.parseString("1999-12-31"))
        prints::
            [datetime.date(1999, 12, 31)]
        """

        def cvt_fn(s, l, t):
            try:
                return datetime.strptime(t[0], fmt).date()
            except ValueError as ve:
                try:
                    raise ParseException(s, l, str(ve))
                finally:
                    ve = None
                    del ve

        return cvt_fn

    @staticmethod
    def convertToDatetime(fmt='%Y-%m-%dT%H:%M:%S.%f'):
        """
        Helper to create a parse action for converting parsed datetime string to Python datetime.datetime

        Params -
         - fmt - format to be passed to datetime.strptime (default=C{"%Y-%m-%dT%H:%M:%S.%f"})

        Example::
            dt_expr = pyparsing_common.iso8601_datetime.copy()
            dt_expr.setParseAction(pyparsing_common.convertToDatetime())
            print(dt_expr.parseString("1999-12-31T23:59:59.999"))
        prints::
            [datetime.datetime(1999, 12, 31, 23, 59, 59, 999000)]
        """

        def cvt_fn(s, l, t):
            try:
                return datetime.strptime(t[0], fmt)
            except ValueError as ve:
                try:
                    raise ParseException(s, l, str(ve))
                finally:
                    ve = None
                    del ve

        return cvt_fn

    iso8601_date = Regex('(?P<year>\\d{4})(?:-(?P<month>\\d\\d)(?:-(?P<day>\\d\\d))?)?').setName('ISO8601 date')
    iso8601_datetime = Regex('(?P<year>\\d{4})-(?P<month>\\d\\d)-(?P<day>\\d\\d)[T ](?P<hour>\\d\\d):(?P<minute>\\d\\d)(:(?P<second>\\d\\d(\\.\\d*)?)?)?(?P<tz>Z|[+-]\\d\\d:?\\d\\d)?').setName('ISO8601 datetime')
    uuid = Regex('[0-9a-fA-F]{8}(-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}').setName('UUID')
    _html_stripper = anyOpenTag.suppress() | anyCloseTag.suppress()

    @staticmethod
    def stripHTMLTags(s, l, tokens):
        """
        Parse action to remove HTML tags from web page HTML source

        Example::
            # strip HTML links from normal text 
            text = '<td>More info at the <a href="http://pyparsing.wikispaces.com">pyparsing</a> wiki page</td>'
            td,td_end = makeHTMLTags("TD")
            table_text = td + SkipTo(td_end).setParseAction(pyparsing_common.stripHTMLTags)("body") + td_end
            
            print(table_text.parseString(text).body) # -> 'More info at the pyparsing wiki page'
        """
        return pyparsing_common._html_stripper.transformString(tokens[0])

    _commasepitem = Combine(OneOrMore(~Literal(',') + ~LineEnd() + Word(printables, excludeChars=',') + Optional(White(' \t')))).streamline().setName('commaItem')
    comma_separated_list = delimitedList(Optional((quotedString.copy() | _commasepitem), default='')).setName('comma separated list')
    upcaseTokens = staticmethod(tokenMap(lambda t: _ustr(t).upper()))
    downcaseTokens = staticmethod(tokenMap(lambda t: _ustr(t).lower()))


if __name__ == '__main__':
    selectToken = CaselessLiteral('select')
    fromToken = CaselessLiteral('from')
    ident = Word(alphas, alphanums + '_$')
    columnName = delimitedList(ident, '.', combine=True).setParseAction(upcaseTokens)
    columnNameList = Group(delimitedList(columnName)).setName('columns')
    columnSpec = '*' | columnNameList
    tableName = delimitedList(ident, '.', combine=True).setParseAction(upcaseTokens)
    tableNameList = Group(delimitedList(tableName)).setName('tables')
    simpleSQL = selectToken('command') + columnSpec('columns') + fromToken + tableNameList('tables')
    simpleSQL.runTests('\n        # \'*\' as column list and dotted table name\n        select * from SYS.XYZZY\n\n        # caseless match on "SELECT", and casts back to "select"\n        SELECT * from XYZZY, ABC\n\n        # list of column names, and mixed case SELECT keyword\n        Select AA,BB,CC from Sys.dual\n\n        # multiple tables\n        Select A, B, C from Sys.dual, Table2\n\n        # invalid SELECT keyword - should fail\n        Xelect A, B, C from Sys.dual\n\n        # incomplete command - should fail\n        Select\n\n        # invalid column name - should fail\n        Select ^^^ frox Sys.dual\n\n        ')
    pyparsing_common.number.runTests('\n        100\n        -100\n        +100\n        3.14159\n        6.02e23\n        1e-12\n        ')
    pyparsing_common.fnumber.runTests('\n        100\n        -100\n        +100\n        3.14159\n        6.02e23\n        1e-12\n        ')
    pyparsing_common.hex_integer.runTests('\n        100\n        FF\n        ')
    import uuid
    pyparsing_common.uuid.setParseAction(tokenMap(uuid.UUID))
    pyparsing_common.uuid.runTests('\n        12345678-1234-5678-1234-567812345678\n        ')