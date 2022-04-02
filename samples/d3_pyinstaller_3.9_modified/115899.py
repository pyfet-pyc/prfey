# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: pkg_resources\_vendor\packaging\specifiers.py
from __future__ import absolute_import, division, print_function
import abc, functools, itertools, re
from ._compat import string_types, with_metaclass
from .version import Version, LegacyVersion, parse

class InvalidSpecifier(ValueError):
    __doc__ = '\n    An invalid specifier was found, users should refer to PEP 440.\n    '


class BaseSpecifier(with_metaclass(abc.ABCMeta, object)):

    @abc.abstractmethod
    def __str__(self):
        """
        Returns the str representation of this Specifier like object. This
        should be representative of the Specifier itself.
        """
        pass

    @abc.abstractmethod
    def __hash__(self):
        """
        Returns a hash value for this Specifier like object.
        """
        pass

    @abc.abstractmethod
    def __eq__(self, other):
        """
        Returns a boolean representing whether or not the two Specifier like
        objects are equal.
        """
        pass

    @abc.abstractmethod
    def __ne__(self, other):
        """
        Returns a boolean representing whether or not the two Specifier like
        objects are not equal.
        """
        pass

    @abc.abstractproperty
    def prereleases(self):
        """
        Returns whether or not pre-releases as a whole are allowed by this
        specifier.
        """
        pass

    @prereleases.setter
    def prereleases(self, value):
        """
        Sets whether or not pre-releases as a whole are allowed by this
        specifier.
        """
        pass

    @abc.abstractmethod
    def contains(self, item, prereleases=None):
        """
        Determines if the given item is contained within this specifier.
        """
        pass

    @abc.abstractmethod
    def filter(self, iterable, prereleases=None):
        """
        Takes an iterable of items and filters them so that only items which
        are contained within this specifier are allowed in it.
        """
        pass


class _IndividualSpecifier(BaseSpecifier):
    _operators = {}

    def __init__(self, spec='', prereleases=None):
        match = self._regex.search(spec)
        if not match:
            raise InvalidSpecifier("Invalid specifier: '{0}'".format(spec))
        self._spec = (match.group('operator').strip(), match.group('version').strip())
        self._prereleases = prereleases

    def __repr__--- This code section failed: ---

 L.  94         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _prereleases
                4  LOAD_CONST               None
                6  <117>                 1  ''

 L.  93         8  POP_JUMP_IF_FALSE    22  'to 22'
               10  LOAD_STR                 ', prereleases={0!r}'
               12  LOAD_METHOD              format
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                prereleases
               18  CALL_METHOD_1         1  ''
               20  JUMP_FORWARD         24  'to 24'
             22_0  COME_FROM             8  '8'

 L.  95        22  LOAD_STR                 ''
             24_0  COME_FROM            20  '20'

 L.  92        24  STORE_FAST               'pre'

 L.  98        26  LOAD_STR                 '<{0}({1!r}{2})>'
               28  LOAD_METHOD              format
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                __class__
               34  LOAD_ATTR                __name__
               36  LOAD_GLOBAL              str
               38  LOAD_FAST                'self'
               40  CALL_FUNCTION_1       1  ''
               42  LOAD_FAST                'pre'
               44  CALL_METHOD_3         3  ''
               46  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def __str__(self):
        return ('{0}{1}'.format)(*self._spec)

    def __hash__(self):
        return hash(self._spec)

    def __eq__--- This code section failed: ---

 L. 107         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'other'
                4  LOAD_GLOBAL              string_types
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    50  'to 50'

 L. 108        10  SETUP_FINALLY        26  'to 26'

 L. 109        12  LOAD_FAST                'self'
               14  LOAD_METHOD              __class__
               16  LOAD_FAST                'other'
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'other'
               22  POP_BLOCK        
               24  JUMP_FORWARD         66  'to 66'
             26_0  COME_FROM_FINALLY    10  '10'

 L. 110        26  DUP_TOP          
               28  LOAD_GLOBAL              InvalidSpecifier
               30  <121>                46  ''
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L. 111        38  LOAD_GLOBAL              NotImplemented
               40  ROT_FOUR         
               42  POP_EXCEPT       
               44  RETURN_VALUE     
               46  <48>             
               48  JUMP_FORWARD         66  'to 66'
             50_0  COME_FROM             8  '8'

 L. 112        50  LOAD_GLOBAL              isinstance
               52  LOAD_FAST                'other'
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                __class__
               58  CALL_FUNCTION_2       2  ''
               60  POP_JUMP_IF_TRUE     66  'to 66'

 L. 113        62  LOAD_GLOBAL              NotImplemented
               64  RETURN_VALUE     
             66_0  COME_FROM            60  '60'
             66_1  COME_FROM            48  '48'
             66_2  COME_FROM            24  '24'

 L. 115        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _spec
               70  LOAD_FAST                'other'
               72  LOAD_ATTR                _spec
               74  COMPARE_OP               ==
               76  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 30

    def __ne__--- This code section failed: ---

 L. 118         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'other'
                4  LOAD_GLOBAL              string_types
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    50  'to 50'

 L. 119        10  SETUP_FINALLY        26  'to 26'

 L. 120        12  LOAD_FAST                'self'
               14  LOAD_METHOD              __class__
               16  LOAD_FAST                'other'
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'other'
               22  POP_BLOCK        
               24  JUMP_FORWARD         66  'to 66'
             26_0  COME_FROM_FINALLY    10  '10'

 L. 121        26  DUP_TOP          
               28  LOAD_GLOBAL              InvalidSpecifier
               30  <121>                46  ''
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L. 122        38  LOAD_GLOBAL              NotImplemented
               40  ROT_FOUR         
               42  POP_EXCEPT       
               44  RETURN_VALUE     
               46  <48>             
               48  JUMP_FORWARD         66  'to 66'
             50_0  COME_FROM             8  '8'

 L. 123        50  LOAD_GLOBAL              isinstance
               52  LOAD_FAST                'other'
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                __class__
               58  CALL_FUNCTION_2       2  ''
               60  POP_JUMP_IF_TRUE     66  'to 66'

 L. 124        62  LOAD_GLOBAL              NotImplemented
               64  RETURN_VALUE     
             66_0  COME_FROM            60  '60'
             66_1  COME_FROM            48  '48'
             66_2  COME_FROM            24  '24'

 L. 126        66  LOAD_FAST                'self'
               68  LOAD_ATTR                _spec
               70  LOAD_FAST                'other'
               72  LOAD_ATTR                _spec
               74  COMPARE_OP               !=
               76  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 30

    def _get_operator(self, op):
        return getattr(self, '_compare_{0}'.format(self._operators[op]))

    def _coerce_version(self, version):
        if not isinstance(version, (LegacyVersion, Version)):
            version = parse(version)
        return version

    @property
    def operator(self):
        return self._spec[0]

    @property
    def version(self):
        return self._spec[1]

    @property
    def prereleases(self):
        return self._prereleases

    @prereleases.setter
    def prereleases(self, value):
        self._prereleases = value

    def __contains__(self, item):
        return self.contains(item)

    def contains--- This code section failed: ---

 L. 157         0  LOAD_FAST                'prereleases'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 158         8  LOAD_FAST                'self'
               10  LOAD_ATTR                prereleases
               12  STORE_FAST               'prereleases'
             14_0  COME_FROM             6  '6'

 L. 162        14  LOAD_FAST                'self'
               16  LOAD_METHOD              _coerce_version
               18  LOAD_FAST                'item'
               20  CALL_METHOD_1         1  ''
               22  STORE_FAST               'item'

 L. 167        24  LOAD_FAST                'item'
               26  LOAD_ATTR                is_prerelease
               28  POP_JUMP_IF_FALSE    38  'to 38'
               30  LOAD_FAST                'prereleases'
               32  POP_JUMP_IF_TRUE     38  'to 38'

 L. 168        34  LOAD_CONST               False
               36  RETURN_VALUE     
             38_0  COME_FROM            32  '32'
             38_1  COME_FROM            28  '28'

 L. 172        38  LOAD_FAST                'self'
               40  LOAD_METHOD              _get_operator
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                operator
               46  CALL_METHOD_1         1  ''
               48  LOAD_FAST                'item'
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                version
               54  CALL_FUNCTION_2       2  ''
               56  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def filter--- This code section failed: ---

 L. 175         0  LOAD_CONST               False
                2  STORE_FAST               'yielded'

 L. 176         4  BUILD_LIST_0          0 
                6  STORE_FAST               'found_prereleases'

 L. 178         8  LOAD_STR                 'prereleases'
               10  LOAD_FAST                'prereleases'
               12  LOAD_CONST               None
               14  <117>                 1  ''
               16  POP_JUMP_IF_FALSE    22  'to 22'
               18  LOAD_FAST                'prereleases'
               20  JUMP_FORWARD         24  'to 24'
             22_0  COME_FROM            16  '16'
               22  LOAD_CONST               True
             24_0  COME_FROM            20  '20'
               24  BUILD_MAP_1           1 
               26  STORE_FAST               'kw'

 L. 182        28  LOAD_FAST                'iterable'
               30  GET_ITER         
             32_0  COME_FROM           102  '102'
             32_1  COME_FROM            90  '90'
             32_2  COME_FROM            62  '62'
               32  FOR_ITER            104  'to 104'
               34  STORE_FAST               'version'

 L. 183        36  LOAD_FAST                'self'
               38  LOAD_METHOD              _coerce_version
               40  LOAD_FAST                'version'
               42  CALL_METHOD_1         1  ''
               44  STORE_FAST               'parsed_version'

 L. 185        46  LOAD_FAST                'self'
               48  LOAD_ATTR                contains
               50  LOAD_FAST                'parsed_version'
               52  BUILD_TUPLE_1         1 
               54  BUILD_MAP_0           0 
               56  LOAD_FAST                'kw'
               58  <164>                 1  ''
               60  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               62  POP_JUMP_IF_FALSE_BACK    32  'to 32'

 L. 189        64  LOAD_FAST                'parsed_version'
               66  LOAD_ATTR                is_prerelease
               68  POP_JUMP_IF_FALSE    92  'to 92'

 L. 190        70  LOAD_FAST                'prereleases'

 L. 189        72  POP_JUMP_IF_TRUE     92  'to 92'

 L. 190        74  LOAD_FAST                'self'
               76  LOAD_ATTR                prereleases

 L. 189        78  POP_JUMP_IF_TRUE     92  'to 92'

 L. 192        80  LOAD_FAST                'found_prereleases'
               82  LOAD_METHOD              append
               84  LOAD_FAST                'version'
               86  CALL_METHOD_1         1  ''
               88  POP_TOP          
               90  JUMP_BACK            32  'to 32'
             92_0  COME_FROM            78  '78'
             92_1  COME_FROM            72  '72'
             92_2  COME_FROM            68  '68'

 L. 196        92  LOAD_CONST               True
               94  STORE_FAST               'yielded'

 L. 197        96  LOAD_FAST                'version'
               98  YIELD_VALUE      
              100  POP_TOP          
              102  JUMP_BACK            32  'to 32'
            104_0  COME_FROM            32  '32'

 L. 202       104  LOAD_FAST                'yielded'
              106  POP_JUMP_IF_TRUE    128  'to 128'
              108  LOAD_FAST                'found_prereleases'
              110  POP_JUMP_IF_FALSE   128  'to 128'

 L. 203       112  LOAD_FAST                'found_prereleases'
              114  GET_ITER         
            116_0  COME_FROM           126  '126'
              116  FOR_ITER            128  'to 128'
              118  STORE_FAST               'version'

 L. 204       120  LOAD_FAST                'version'
              122  YIELD_VALUE      
              124  POP_TOP          
              126  JUMP_BACK           116  'to 116'
            128_0  COME_FROM           116  '116'
            128_1  COME_FROM           110  '110'
            128_2  COME_FROM           106  '106'

Parse error at or near `<117>' instruction at offset 14


class LegacySpecifier(_IndividualSpecifier):
    _regex_str = '\n        (?P<operator>(==|!=|<=|>=|<|>))\n        \\s*\n        (?P<version>\n            [^,;\\s)]* # Since this is a "legacy" specifier, and the version\n                      # string can be just about anything, we match everything\n                      # except for whitespace, a semi-colon for marker support,\n                      # a closing paren since versions can be enclosed in\n                      # them, and a comma since it\'s a version separator.\n        )\n        '
    _regex = re.compile('^\\s*' + _regex_str + '\\s*$', re.VERBOSE | re.IGNORECASE)
    _operators = {'==':'equal', 
     '!=':'not_equal', 
     '<=':'less_than_equal', 
     '>=':'greater_than_equal', 
     '<':'less_than', 
     '>':'greater_than'}

    def _coerce_version(self, version):
        if not isinstance(version, LegacyVersion):
            version = LegacyVersion(str(version))
        return version

    def _compare_equal(self, prospective, spec):
        return prospective == self._coerce_version(spec)

    def _compare_not_equal(self, prospective, spec):
        return prospective != self._coerce_version(spec)

    def _compare_less_than_equal(self, prospective, spec):
        return prospective <= self._coerce_version(spec)

    def _compare_greater_than_equal(self, prospective, spec):
        return prospective >= self._coerce_version(spec)

    def _compare_less_than(self, prospective, spec):
        return prospective < self._coerce_version(spec)

    def _compare_greater_than(self, prospective, spec):
        return prospective > self._coerce_version(spec)


def _require_version_compare(fn):

    @functools.wraps(fn)
    def wrapped(self, prospective, spec):
        if not isinstance(prospective, Version):
            return False
        return fn(self, prospective, spec)

    return wrapped


class Specifier(_IndividualSpecifier):
    _regex_str = "\n        (?P<operator>(~=|==|!=|<=|>=|<|>|===))\n        (?P<version>\n            (?:\n                # The identity operators allow for an escape hatch that will\n                # do an exact string match of the version you wish to install.\n                # This will not be parsed by PEP 440 and we cannot determine\n                # any semantic meaning from it. This operator is discouraged\n                # but included entirely as an escape hatch.\n                (?<====)  # Only match for the identity operator\n                \\s*\n                [^\\s]*    # We just match everything, except for whitespace\n                          # since we are only testing for strict identity.\n            )\n            |\n            (?:\n                # The (non)equality operators allow for wild card and local\n                # versions to be specified so we have to define these two\n                # operators separately to enable that.\n                (?<===|!=)            # Only match for equals and not equals\n\n                \\s*\n                v?\n                (?:[0-9]+!)?          # epoch\n                [0-9]+(?:\\.[0-9]+)*   # release\n                (?:                   # pre release\n                    [-_\\.]?\n                    (a|b|c|rc|alpha|beta|pre|preview)\n                    [-_\\.]?\n                    [0-9]*\n                )?\n                (?:                   # post release\n                    (?:-[0-9]+)|(?:[-_\\.]?(post|rev|r)[-_\\.]?[0-9]*)\n                )?\n\n                # You cannot use a wild card and a dev or local version\n                # together so group them with a | and make them optional.\n                (?:\n                    (?:[-_\\.]?dev[-_\\.]?[0-9]*)?         # dev release\n                    (?:\\+[a-z0-9]+(?:[-_\\.][a-z0-9]+)*)? # local\n                    |\n                    \\.\\*  # Wild card syntax of .*\n                )?\n            )\n            |\n            (?:\n                # The compatible operator requires at least two digits in the\n                # release segment.\n                (?<=~=)               # Only match for the compatible operator\n\n                \\s*\n                v?\n                (?:[0-9]+!)?          # epoch\n                [0-9]+(?:\\.[0-9]+)+   # release  (We have a + instead of a *)\n                (?:                   # pre release\n                    [-_\\.]?\n                    (a|b|c|rc|alpha|beta|pre|preview)\n                    [-_\\.]?\n                    [0-9]*\n                )?\n                (?:                                   # post release\n                    (?:-[0-9]+)|(?:[-_\\.]?(post|rev|r)[-_\\.]?[0-9]*)\n                )?\n                (?:[-_\\.]?dev[-_\\.]?[0-9]*)?          # dev release\n            )\n            |\n            (?:\n                # All other operators only allow a sub set of what the\n                # (non)equality operators do. Specifically they do not allow\n                # local versions to be specified nor do they allow the prefix\n                # matching wild cards.\n                (?<!==|!=|~=)         # We have special cases for these\n                                      # operators so we want to make sure they\n                                      # don't match here.\n\n                \\s*\n                v?\n                (?:[0-9]+!)?          # epoch\n                [0-9]+(?:\\.[0-9]+)*   # release\n                (?:                   # pre release\n                    [-_\\.]?\n                    (a|b|c|rc|alpha|beta|pre|preview)\n                    [-_\\.]?\n                    [0-9]*\n                )?\n                (?:                                   # post release\n                    (?:-[0-9]+)|(?:[-_\\.]?(post|rev|r)[-_\\.]?[0-9]*)\n                )?\n                (?:[-_\\.]?dev[-_\\.]?[0-9]*)?          # dev release\n            )\n        )\n        "
    _regex = re.compile('^\\s*' + _regex_str + '\\s*$', re.VERBOSE | re.IGNORECASE)
    _operators = {'~=':'compatible', 
     '==':'equal', 
     '!=':'not_equal', 
     '<=':'less_than_equal', 
     '>=':'greater_than_equal', 
     '<':'less_than', 
     '>':'greater_than', 
     '===':'arbitrary'}

    @_require_version_compare
    def _compare_compatible(self, prospective, spec):
        prefix = '.'.join(list(itertools.takewhile(lambda x: not x.startswith('post') and not x.startswith('dev'), _version_split(spec)))[:-1])
        prefix += '.*'
        return self._get_operator('>=')(prospective, spec) and self._get_operator('==')(prospective, prefix)

    @_require_version_compare
    def _compare_equal(self, prospective, spec):
        if spec.endswith('.*'):
            prospective = Version(prospective.public)
            spec = _version_split(spec[:-2])
            prospective = _version_split(str(prospective))
            prospective = prospective[:len(spec)]
            spec, prospective = _pad_version(spec, prospective)
        else:
            spec = Version(spec)
            if not spec.local:
                prospective = Version(prospective.public)
        return prospective == spec

    @_require_version_compare
    def _compare_not_equal(self, prospective, spec):
        return not self._compare_equal(prospective, spec)

    @_require_version_compare
    def _compare_less_than_equal(self, prospective, spec):
        return prospective <= Version(spec)

    @_require_version_compare
    def _compare_greater_than_equal(self, prospective, spec):
        return prospective >= Version(spec)

    @_require_version_compare
    def _compare_less_than(self, prospective, spec):
        spec = Version(spec)
        if not prospective < spec:
            return False
        if not spec.is_prerelease:
            if prospective.is_prerelease:
                if Version(prospective.base_version) == Version(spec.base_version):
                    return False
        return True

    @_require_version_compare
    def _compare_greater_than--- This code section failed: ---

 L. 477         0  LOAD_GLOBAL              Version
                2  LOAD_FAST                'spec'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'spec'

 L. 482         8  LOAD_FAST                'prospective'
               10  LOAD_FAST                'spec'
               12  COMPARE_OP               >
               14  POP_JUMP_IF_TRUE     20  'to 20'

 L. 483        16  LOAD_CONST               False
               18  RETURN_VALUE     
             20_0  COME_FROM            14  '14'

 L. 489        20  LOAD_FAST                'spec'
               22  LOAD_ATTR                is_postrelease
               24  POP_JUMP_IF_TRUE     56  'to 56'
               26  LOAD_FAST                'prospective'
               28  LOAD_ATTR                is_postrelease
               30  POP_JUMP_IF_FALSE    56  'to 56'

 L. 490        32  LOAD_GLOBAL              Version
               34  LOAD_FAST                'prospective'
               36  LOAD_ATTR                base_version
               38  CALL_FUNCTION_1       1  ''
               40  LOAD_GLOBAL              Version
               42  LOAD_FAST                'spec'
               44  LOAD_ATTR                base_version
               46  CALL_FUNCTION_1       1  ''
               48  COMPARE_OP               ==
               50  POP_JUMP_IF_FALSE    56  'to 56'

 L. 491        52  LOAD_CONST               False
               54  RETURN_VALUE     
             56_0  COME_FROM            50  '50'
             56_1  COME_FROM            30  '30'
             56_2  COME_FROM            24  '24'

 L. 495        56  LOAD_FAST                'prospective'
               58  LOAD_ATTR                local
               60  LOAD_CONST               None
               62  <117>                 1  ''
               64  POP_JUMP_IF_FALSE    90  'to 90'

 L. 496        66  LOAD_GLOBAL              Version
               68  LOAD_FAST                'prospective'
               70  LOAD_ATTR                base_version
               72  CALL_FUNCTION_1       1  ''
               74  LOAD_GLOBAL              Version
               76  LOAD_FAST                'spec'
               78  LOAD_ATTR                base_version
               80  CALL_FUNCTION_1       1  ''
               82  COMPARE_OP               ==
               84  POP_JUMP_IF_FALSE    90  'to 90'

 L. 497        86  LOAD_CONST               False
               88  RETURN_VALUE     
             90_0  COME_FROM            84  '84'
             90_1  COME_FROM            64  '64'

 L. 502        90  LOAD_CONST               True
               92  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 62

    def _compare_arbitrary(self, prospective, spec):
        return str(prospective).lower() == str(spec).lower()

    @property
    def prereleases--- This code section failed: ---

 L. 511         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _prereleases
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    16  'to 16'

 L. 512        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _prereleases
               14  RETURN_VALUE     
             16_0  COME_FROM             8  '8'

 L. 517        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _spec
               20  UNPACK_SEQUENCE_2     2 
               22  STORE_FAST               'operator'
               24  STORE_FAST               'version'

 L. 518        26  LOAD_FAST                'operator'
               28  LOAD_CONST               ('==', '>=', '<=', '~=', '===')
               30  <118>                 0  ''
               32  POP_JUMP_IF_FALSE    78  'to 78'

 L. 521        34  LOAD_FAST                'operator'
               36  LOAD_STR                 '=='
               38  COMPARE_OP               ==
               40  POP_JUMP_IF_FALSE    64  'to 64'
               42  LOAD_FAST                'version'
               44  LOAD_METHOD              endswith
               46  LOAD_STR                 '.*'
               48  CALL_METHOD_1         1  ''
               50  POP_JUMP_IF_FALSE    64  'to 64'

 L. 522        52  LOAD_FAST                'version'
               54  LOAD_CONST               None
               56  LOAD_CONST               -2
               58  BUILD_SLICE_2         2 
               60  BINARY_SUBSCR    
               62  STORE_FAST               'version'
             64_0  COME_FROM            50  '50'
             64_1  COME_FROM            40  '40'

 L. 526        64  LOAD_GLOBAL              parse
               66  LOAD_FAST                'version'
               68  CALL_FUNCTION_1       1  ''
               70  LOAD_ATTR                is_prerelease
               72  POP_JUMP_IF_FALSE    78  'to 78'

 L. 527        74  LOAD_CONST               True
               76  RETURN_VALUE     
             78_0  COME_FROM            72  '72'
             78_1  COME_FROM            32  '32'

 L. 529        78  LOAD_CONST               False
               80  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @prereleases.setter
    def prereleases(self, value):
        self._prereleases = value


_prefix_regex = re.compile('^([0-9]+)((?:a|b|c|rc)[0-9]+)$')

def _version_split(version):
    result = []
    for item in version.split('.'):
        match = _prefix_regex.search(item)
        if match:
            result.extend(match.groups())
        else:
            result.append(item)
    else:
        return result


def _pad_version(left, right):
    left_split, right_split = [], []
    left_split.append(list(itertools.takewhile(lambda x: x.isdigit(), left)))
    right_split.append(list(itertools.takewhile(lambda x: x.isdigit(), right)))
    left_split.append(left[len(left_split[0]):])
    right_split.append(right[len(right_split[0]):])
    left_split.insert(1, ['0'] * max(0, len(right_split[0]) - len(left_split[0])))
    right_split.insert(1, ['0'] * max(0, len(left_split[0]) - len(right_split[0])))
    return (
     list((itertools.chain)(*left_split)), list((itertools.chain)(*right_split)))


class SpecifierSet(BaseSpecifier):

    def __init__--- This code section failed: ---

 L. 572         0  LOAD_LISTCOMP            '<code_object <listcomp>>'
                2  LOAD_STR                 'SpecifierSet.__init__.<locals>.<listcomp>'
                4  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                6  LOAD_FAST                'specifiers'
                8  LOAD_METHOD              split
               10  LOAD_STR                 ','
               12  CALL_METHOD_1         1  ''
               14  GET_ITER         
               16  CALL_FUNCTION_1       1  ''
               18  STORE_FAST               'specifiers'

 L. 576        20  LOAD_GLOBAL              set
               22  CALL_FUNCTION_0       0  ''
               24  STORE_FAST               'parsed'

 L. 577        26  LOAD_FAST                'specifiers'
               28  GET_ITER         
             30_0  COME_FROM            86  '86'
             30_1  COME_FROM            82  '82'
             30_2  COME_FROM            52  '52'
               30  FOR_ITER             88  'to 88'
               32  STORE_FAST               'specifier'

 L. 578        34  SETUP_FINALLY        54  'to 54'

 L. 579        36  LOAD_FAST                'parsed'
               38  LOAD_METHOD              add
               40  LOAD_GLOBAL              Specifier
               42  LOAD_FAST                'specifier'
               44  CALL_FUNCTION_1       1  ''
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          
               50  POP_BLOCK        
               52  JUMP_BACK            30  'to 30'
             54_0  COME_FROM_FINALLY    34  '34'

 L. 580        54  DUP_TOP          
               56  LOAD_GLOBAL              InvalidSpecifier
               58  <121>                84  ''
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L. 581        66  LOAD_FAST                'parsed'
               68  LOAD_METHOD              add
               70  LOAD_GLOBAL              LegacySpecifier
               72  LOAD_FAST                'specifier'
               74  CALL_FUNCTION_1       1  ''
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          
               80  POP_EXCEPT       
               82  JUMP_BACK            30  'to 30'
               84  <48>             
               86  JUMP_BACK            30  'to 30'
             88_0  COME_FROM            30  '30'

 L. 584        88  LOAD_GLOBAL              frozenset
               90  LOAD_FAST                'parsed'
               92  CALL_FUNCTION_1       1  ''
               94  LOAD_FAST                'self'
               96  STORE_ATTR               _specs

 L. 588        98  LOAD_FAST                'prereleases'
              100  LOAD_FAST                'self'
              102  STORE_ATTR               _prereleases

Parse error at or near `<121>' instruction at offset 58

    def __repr__--- This code section failed: ---

 L. 593         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _prereleases
                4  LOAD_CONST               None
                6  <117>                 1  ''

 L. 592         8  POP_JUMP_IF_FALSE    22  'to 22'
               10  LOAD_STR                 ', prereleases={0!r}'
               12  LOAD_METHOD              format
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                prereleases
               18  CALL_METHOD_1         1  ''
               20  JUMP_FORWARD         24  'to 24'
             22_0  COME_FROM             8  '8'

 L. 594        22  LOAD_STR                 ''
             24_0  COME_FROM            20  '20'

 L. 591        24  STORE_FAST               'pre'

 L. 597        26  LOAD_STR                 '<SpecifierSet({0!r}{1})>'
               28  LOAD_METHOD              format
               30  LOAD_GLOBAL              str
               32  LOAD_FAST                'self'
               34  CALL_FUNCTION_1       1  ''
               36  LOAD_FAST                'pre'
               38  CALL_METHOD_2         2  ''
               40  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def __str__(self):
        return ','.join(sorted((str(s) for s in self._specs)))

    def __hash__(self):
        return hash(self._specs)

    def __and__--- This code section failed: ---

 L. 606         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'other'
                4  LOAD_GLOBAL              string_types
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    20  'to 20'

 L. 607        10  LOAD_GLOBAL              SpecifierSet
               12  LOAD_FAST                'other'
               14  CALL_FUNCTION_1       1  ''
               16  STORE_FAST               'other'
               18  JUMP_FORWARD         34  'to 34'
             20_0  COME_FROM             8  '8'

 L. 608        20  LOAD_GLOBAL              isinstance
               22  LOAD_FAST                'other'
               24  LOAD_GLOBAL              SpecifierSet
               26  CALL_FUNCTION_2       2  ''
               28  POP_JUMP_IF_TRUE     34  'to 34'

 L. 609        30  LOAD_GLOBAL              NotImplemented
               32  RETURN_VALUE     
             34_0  COME_FROM            28  '28'
             34_1  COME_FROM            18  '18'

 L. 611        34  LOAD_GLOBAL              SpecifierSet
               36  CALL_FUNCTION_0       0  ''
               38  STORE_FAST               'specifier'

 L. 612        40  LOAD_GLOBAL              frozenset
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                _specs
               46  LOAD_FAST                'other'
               48  LOAD_ATTR                _specs
               50  BINARY_OR        
               52  CALL_FUNCTION_1       1  ''
               54  LOAD_FAST                'specifier'
               56  STORE_ATTR               _specs

 L. 614        58  LOAD_FAST                'self'
               60  LOAD_ATTR                _prereleases
               62  LOAD_CONST               None
               64  <117>                 0  ''
               66  POP_JUMP_IF_FALSE    88  'to 88'
               68  LOAD_FAST                'other'
               70  LOAD_ATTR                _prereleases
               72  LOAD_CONST               None
               74  <117>                 1  ''
               76  POP_JUMP_IF_FALSE    88  'to 88'

 L. 615        78  LOAD_FAST                'other'
               80  LOAD_ATTR                _prereleases
               82  LOAD_FAST                'specifier'
               84  STORE_ATTR               _prereleases
               86  JUMP_FORWARD        148  'to 148'
             88_0  COME_FROM            76  '76'
             88_1  COME_FROM            66  '66'

 L. 616        88  LOAD_FAST                'self'
               90  LOAD_ATTR                _prereleases
               92  LOAD_CONST               None
               94  <117>                 1  ''
               96  POP_JUMP_IF_FALSE   118  'to 118'
               98  LOAD_FAST                'other'
              100  LOAD_ATTR                _prereleases
              102  LOAD_CONST               None
              104  <117>                 0  ''
              106  POP_JUMP_IF_FALSE   118  'to 118'

 L. 617       108  LOAD_FAST                'self'
              110  LOAD_ATTR                _prereleases
              112  LOAD_FAST                'specifier'
              114  STORE_ATTR               _prereleases
              116  JUMP_FORWARD        148  'to 148'
            118_0  COME_FROM           106  '106'
            118_1  COME_FROM            96  '96'

 L. 618       118  LOAD_FAST                'self'
              120  LOAD_ATTR                _prereleases
              122  LOAD_FAST                'other'
              124  LOAD_ATTR                _prereleases
              126  COMPARE_OP               ==
              128  POP_JUMP_IF_FALSE   140  'to 140'

 L. 619       130  LOAD_FAST                'self'
              132  LOAD_ATTR                _prereleases
              134  LOAD_FAST                'specifier'
              136  STORE_ATTR               _prereleases
              138  JUMP_FORWARD        148  'to 148'
            140_0  COME_FROM           128  '128'

 L. 621       140  LOAD_GLOBAL              ValueError

 L. 622       142  LOAD_STR                 'Cannot combine SpecifierSets with True and False prerelease overrides.'

 L. 621       144  CALL_FUNCTION_1       1  ''
              146  RAISE_VARARGS_1       1  'exception instance'
            148_0  COME_FROM           138  '138'
            148_1  COME_FROM           116  '116'
            148_2  COME_FROM            86  '86'

 L. 626       148  LOAD_FAST                'specifier'
              150  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 64

    def __eq__(self, other):
        if isinstance(other, string_types):
            other = SpecifierSet(other)
        elif isinstance(other, _IndividualSpecifier):
            other = SpecifierSet(str(other))
        elif not isinstance(other, SpecifierSet):
            return NotImplemented
        return self._specs == other._specs

    def __ne__(self, other):
        if isinstance(other, string_types):
            other = SpecifierSet(other)
        elif isinstance(other, _IndividualSpecifier):
            other = SpecifierSet(str(other))
        elif not isinstance(other, SpecifierSet):
            return NotImplemented
        return self._specs != other._specs

    def __len__(self):
        return len(self._specs)

    def __iter__(self):
        return iter(self._specs)

    @property
    def prereleases--- This code section failed: ---

 L. 658         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _prereleases
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    16  'to 16'

 L. 659        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _prereleases
               14  RETURN_VALUE     
             16_0  COME_FROM             8  '8'

 L. 664        16  LOAD_FAST                'self'
               18  LOAD_ATTR                _specs
               20  POP_JUMP_IF_TRUE     26  'to 26'

 L. 665        22  LOAD_CONST               None
               24  RETURN_VALUE     
             26_0  COME_FROM            20  '20'

 L. 669        26  LOAD_GLOBAL              any
               28  LOAD_GENEXPR             '<code_object <genexpr>>'
               30  LOAD_STR                 'SpecifierSet.prereleases.<locals>.<genexpr>'
               32  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                _specs
               38  GET_ITER         
               40  CALL_FUNCTION_1       1  ''
               42  CALL_FUNCTION_1       1  ''
               44  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @prereleases.setter
    def prereleases(self, value):
        self._prereleases = value

    def __contains__(self, item):
        return self.contains(item)

    def contains--- This code section failed: ---

 L. 680         0  LOAD_GLOBAL              isinstance
                2  LOAD_DEREF               'item'
                4  LOAD_GLOBAL              LegacyVersion
                6  LOAD_GLOBAL              Version
                8  BUILD_TUPLE_2         2 
               10  CALL_FUNCTION_2       2  ''
               12  POP_JUMP_IF_TRUE     22  'to 22'

 L. 681        14  LOAD_GLOBAL              parse
               16  LOAD_DEREF               'item'
               18  CALL_FUNCTION_1       1  ''
               20  STORE_DEREF              'item'
             22_0  COME_FROM            12  '12'

 L. 686        22  LOAD_DEREF               'prereleases'
               24  LOAD_CONST               None
               26  <117>                 0  ''
               28  POP_JUMP_IF_FALSE    36  'to 36'

 L. 687        30  LOAD_FAST                'self'
               32  LOAD_ATTR                prereleases
               34  STORE_DEREF              'prereleases'
             36_0  COME_FROM            28  '28'

 L. 695        36  LOAD_DEREF               'prereleases'
               38  POP_JUMP_IF_TRUE     50  'to 50'
               40  LOAD_DEREF               'item'
               42  LOAD_ATTR                is_prerelease
               44  POP_JUMP_IF_FALSE    50  'to 50'

 L. 696        46  LOAD_CONST               False
               48  RETURN_VALUE     
             50_0  COME_FROM            44  '44'
             50_1  COME_FROM            38  '38'

 L. 702        50  LOAD_GLOBAL              all
               52  LOAD_CLOSURE             'item'
               54  LOAD_CLOSURE             'prereleases'
               56  BUILD_TUPLE_2         2 
               58  LOAD_GENEXPR             '<code_object <genexpr>>'
               60  LOAD_STR                 'SpecifierSet.contains.<locals>.<genexpr>'
               62  MAKE_FUNCTION_8          'closure'
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                _specs
               68  GET_ITER         
               70  CALL_FUNCTION_1       1  ''
               72  CALL_FUNCTION_1       1  ''
               74  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 26

    def filter--- This code section failed: ---

 L. 708         0  LOAD_FAST                'prereleases'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 709         8  LOAD_FAST                'self'
               10  LOAD_ATTR                prereleases
               12  STORE_FAST               'prereleases'
             14_0  COME_FROM             6  '6'

 L. 714        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _specs
               18  POP_JUMP_IF_FALSE    54  'to 54'

 L. 715        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _specs
               24  GET_ITER         
             26_0  COME_FROM            48  '48'
               26  FOR_ITER             50  'to 50'
               28  STORE_FAST               'spec'

 L. 716        30  LOAD_FAST                'spec'
               32  LOAD_ATTR                filter
               34  LOAD_FAST                'iterable'
               36  LOAD_GLOBAL              bool
               38  LOAD_FAST                'prereleases'
               40  CALL_FUNCTION_1       1  ''
               42  LOAD_CONST               ('prereleases',)
               44  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               46  STORE_FAST               'iterable'
               48  JUMP_BACK            26  'to 26'
             50_0  COME_FROM            26  '26'

 L. 717        50  LOAD_FAST                'iterable'
               52  RETURN_VALUE     
             54_0  COME_FROM            18  '18'

 L. 722        54  BUILD_LIST_0          0 
               56  STORE_FAST               'filtered'

 L. 723        58  BUILD_LIST_0          0 
               60  STORE_FAST               'found_prereleases'

 L. 725        62  LOAD_FAST                'iterable'
               64  GET_ITER         
             66_0  COME_FROM           146  '146'
             66_1  COME_FROM           134  '134'
             66_2  COME_FROM           108  '108'
               66  FOR_ITER            148  'to 148'
               68  STORE_FAST               'item'

 L. 727        70  LOAD_GLOBAL              isinstance
               72  LOAD_FAST                'item'
               74  LOAD_GLOBAL              LegacyVersion
               76  LOAD_GLOBAL              Version
               78  BUILD_TUPLE_2         2 
               80  CALL_FUNCTION_2       2  ''
               82  POP_JUMP_IF_TRUE     94  'to 94'

 L. 728        84  LOAD_GLOBAL              parse
               86  LOAD_FAST                'item'
               88  CALL_FUNCTION_1       1  ''
               90  STORE_FAST               'parsed_version'
               92  JUMP_FORWARD         98  'to 98'
             94_0  COME_FROM            82  '82'

 L. 730        94  LOAD_FAST                'item'
               96  STORE_FAST               'parsed_version'
             98_0  COME_FROM            92  '92'

 L. 733        98  LOAD_GLOBAL              isinstance
              100  LOAD_FAST                'parsed_version'
              102  LOAD_GLOBAL              LegacyVersion
              104  CALL_FUNCTION_2       2  ''
              106  POP_JUMP_IF_FALSE   110  'to 110'

 L. 734       108  JUMP_BACK            66  'to 66'
            110_0  COME_FROM           106  '106'

 L. 738       110  LOAD_FAST                'parsed_version'
              112  LOAD_ATTR                is_prerelease
              114  POP_JUMP_IF_FALSE   136  'to 136'
              116  LOAD_FAST                'prereleases'
              118  POP_JUMP_IF_TRUE    136  'to 136'

 L. 739       120  LOAD_FAST                'filtered'
              122  POP_JUMP_IF_TRUE    146  'to 146'

 L. 740       124  LOAD_FAST                'found_prereleases'
              126  LOAD_METHOD              append
              128  LOAD_FAST                'item'
              130  CALL_METHOD_1         1  ''
              132  POP_TOP          
              134  JUMP_BACK            66  'to 66'
            136_0  COME_FROM           118  '118'
            136_1  COME_FROM           114  '114'

 L. 742       136  LOAD_FAST                'filtered'
              138  LOAD_METHOD              append
              140  LOAD_FAST                'item'
              142  CALL_METHOD_1         1  ''
              144  POP_TOP          
            146_0  COME_FROM           122  '122'
              146  JUMP_BACK            66  'to 66'
            148_0  COME_FROM            66  '66'

 L. 746       148  LOAD_FAST                'filtered'
              150  POP_JUMP_IF_TRUE    168  'to 168'
              152  LOAD_FAST                'found_prereleases'
              154  POP_JUMP_IF_FALSE   168  'to 168'
              156  LOAD_FAST                'prereleases'
              158  LOAD_CONST               None
              160  <117>                 0  ''
              162  POP_JUMP_IF_FALSE   168  'to 168'

 L. 747       164  LOAD_FAST                'found_prereleases'
              166  RETURN_VALUE     
            168_0  COME_FROM           162  '162'
            168_1  COME_FROM           154  '154'
            168_2  COME_FROM           150  '150'

 L. 749       168  LOAD_FAST                'filtered'
              170  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1