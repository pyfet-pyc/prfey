# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: distutils\versionpredicate.py
"""Module for parsing and testing package version predicate strings.
"""
import re, distutils.version, operator
re_validPackage = re.compile('(?i)^\\s*([a-z_]\\w*(?:\\.[a-z_]\\w*)*)(.*)', re.ASCII)
re_paren = re.compile('^\\s*\\((.*)\\)\\s*$')
re_splitComparison = re.compile('^\\s*(<=|>=|<|>|!=|==)\\s*([^\\s,]+)\\s*$')

def splitUp(pred):
    """Parse a single version comparison.

    Return (comparison string, StrictVersion)
    """
    res = re_splitComparison.match(pred)
    if not res:
        raise ValueError('bad package restriction syntax: %r' % pred)
    comp, verStr = res.groups()
    return (comp, distutils.version.StrictVersion(verStr))


compmap = {'<':operator.lt, 
 '<=':operator.le,  '==':operator.eq,  '>':operator.gt, 
 '>=':operator.ge,  '!=':operator.ne}

class VersionPredicate:
    __doc__ = "Parse and test package version predicates.\n\n    >>> v = VersionPredicate('pyepat.abc (>1.0, <3333.3a1, !=1555.1b3)')\n\n    The `name` attribute provides the full dotted name that is given::\n\n    >>> v.name\n    'pyepat.abc'\n\n    The str() of a `VersionPredicate` provides a normalized\n    human-readable version of the expression::\n\n    >>> print(v)\n    pyepat.abc (> 1.0, < 3333.3a1, != 1555.1b3)\n\n    The `satisfied_by()` method can be used to determine with a given\n    version number is included in the set described by the version\n    restrictions::\n\n    >>> v.satisfied_by('1.1')\n    True\n    >>> v.satisfied_by('1.4')\n    True\n    >>> v.satisfied_by('1.0')\n    False\n    >>> v.satisfied_by('4444.4')\n    False\n    >>> v.satisfied_by('1555.1b3')\n    False\n\n    `VersionPredicate` is flexible in accepting extra whitespace::\n\n    >>> v = VersionPredicate(' pat( ==  0.1  )  ')\n    >>> v.name\n    'pat'\n    >>> v.satisfied_by('0.1')\n    True\n    >>> v.satisfied_by('0.2')\n    False\n\n    If any version numbers passed in do not conform to the\n    restrictions of `StrictVersion`, a `ValueError` is raised::\n\n    >>> v = VersionPredicate('p1.p2.p3.p4(>=1.0, <=1.3a1, !=1.2zb3)')\n    Traceback (most recent call last):\n      ...\n    ValueError: invalid version number '1.2zb3'\n\n    It the module or package name given does not conform to what's\n    allowed as a legal module or package name, `ValueError` is\n    raised::\n\n    >>> v = VersionPredicate('foo-bar')\n    Traceback (most recent call last):\n      ...\n    ValueError: expected parenthesized list: '-bar'\n\n    >>> v = VersionPredicate('foo bar (12.21)')\n    Traceback (most recent call last):\n      ...\n    ValueError: expected parenthesized list: 'bar (12.21)'\n\n    "

    def __init__(self, versionPredicateStr):
        """Parse a version predicate string.
        """
        versionPredicateStr = versionPredicateStr.strip()
        if not versionPredicateStr:
            raise ValueError('empty package restriction')
        else:
            match = re_validPackage.match(versionPredicateStr)
            if not match:
                raise ValueError('bad package name in %r' % versionPredicateStr)
            else:
                self.name, paren = match.groups()
                paren = paren.strip()
                if paren:
                    match = re_paren.match(paren)
                    if not match:
                        raise ValueError('expected parenthesized list: %r' % paren)
                    str = match.groups()[0]
                    self.pred = [splitUp(aPred) for aPred in str.split(',')]
                    assert self.pred, 'empty parenthesized list in %r' % versionPredicateStr
                else:
                    self.pred = []

    def __str__(self):
        if self.pred:
            seq = [cond + ' ' + str(ver) for cond, ver in self.pred]
            return self.name + ' (' + ', '.join(seq) + ')'
        return self.name

    def satisfied_by(self, version):
        """True if version is compatible with all the predicates in self.
        The parameter version must be acceptable to the StrictVersion
        constructor.  It may be either a string or StrictVersion.
        """
        for cond, ver in self.pred:
            if not compmap[cond](version, ver):
                return False
            return True


_provision_rx = None

def split_provision--- This code section failed: ---

 L. 155         0  LOAD_GLOBAL              _provision_rx
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    22  'to 22'

 L. 156         8  LOAD_GLOBAL              re
               10  LOAD_METHOD              compile

 L. 157        12  LOAD_STR                 '([a-zA-Z_]\\w*(?:\\.[a-zA-Z_]\\w*)*)(?:\\s*\\(\\s*([^)\\s]+)\\s*\\))?$'

 L. 158        14  LOAD_GLOBAL              re
               16  LOAD_ATTR                ASCII

 L. 156        18  CALL_METHOD_2         2  ''
               20  STORE_GLOBAL             _provision_rx
             22_0  COME_FROM             6  '6'

 L. 159        22  LOAD_FAST                'value'
               24  LOAD_METHOD              strip
               26  CALL_METHOD_0         0  ''
               28  STORE_FAST               'value'

 L. 160        30  LOAD_GLOBAL              _provision_rx
               32  LOAD_METHOD              match
               34  LOAD_FAST                'value'
               36  CALL_METHOD_1         1  ''
               38  STORE_FAST               'm'

 L. 161        40  LOAD_FAST                'm'
               42  POP_JUMP_IF_TRUE     56  'to 56'

 L. 162        44  LOAD_GLOBAL              ValueError
               46  LOAD_STR                 'illegal provides specification: %r'
               48  LOAD_FAST                'value'
               50  BINARY_MODULO    
               52  CALL_FUNCTION_1       1  ''
               54  RAISE_VARARGS_1       1  'exception instance'
             56_0  COME_FROM            42  '42'

 L. 163        56  LOAD_FAST                'm'
               58  LOAD_METHOD              group
               60  LOAD_CONST               2
               62  CALL_METHOD_1         1  ''
               64  JUMP_IF_TRUE_OR_POP    68  'to 68'
               66  LOAD_CONST               None
             68_0  COME_FROM            64  '64'
               68  STORE_FAST               'ver'

 L. 164        70  LOAD_FAST                'ver'
               72  POP_JUMP_IF_FALSE    86  'to 86'

 L. 165        74  LOAD_GLOBAL              distutils
               76  LOAD_ATTR                version
               78  LOAD_METHOD              StrictVersion
               80  LOAD_FAST                'ver'
               82  CALL_METHOD_1         1  ''
               84  STORE_FAST               'ver'
             86_0  COME_FROM            72  '72'

 L. 166        86  LOAD_FAST                'm'
               88  LOAD_METHOD              group
               90  LOAD_CONST               1
               92  CALL_METHOD_1         1  ''
               94  LOAD_FAST                'ver'
               96  BUILD_TUPLE_2         2 
               98  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


# global _provision_rx ## Warning: Unused global