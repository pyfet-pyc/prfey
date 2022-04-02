# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: numpy\polynomial\_polybase.py
"""
Abstract base class for the various polynomial Classes.

The ABCPolyBase class provides the methods needed to implement the common API
for the various polynomial classes. It operates as a mixin, but uses the
abc module from the stdlib, hence it is only available for Python >= 2.6.

"""
import os, abc, numbers, numpy as np
from . import polyutils as pu
__all__ = [
 'ABCPolyBase']

class ABCPolyBase(abc.ABC):
    __doc__ = "An abstract base class for immutable series classes.\n\n    ABCPolyBase provides the standard Python numerical methods\n    '+', '-', '*', '//', '%', 'divmod', '**', and '()' along with the\n    methods listed below.\n\n    .. versionadded:: 1.9.0\n\n    Parameters\n    ----------\n    coef : array_like\n        Series coefficients in order of increasing degree, i.e.,\n        ``(1, 2, 3)`` gives ``1*P_0(x) + 2*P_1(x) + 3*P_2(x)``, where\n        ``P_i`` is the basis polynomials of degree ``i``.\n    domain : (2,) array_like, optional\n        Domain to use. The interval ``[domain[0], domain[1]]`` is mapped\n        to the interval ``[window[0], window[1]]`` by shifting and scaling.\n        The default value is the derived class domain.\n    window : (2,) array_like, optional\n        Window, see domain for its use. The default value is the\n        derived class window.\n\n    Attributes\n    ----------\n    coef : (N,) ndarray\n        Series coefficients in order of increasing degree.\n    domain : (2,) ndarray\n        Domain that is mapped to window.\n    window : (2,) ndarray\n        Window that domain is mapped to.\n\n    Class Attributes\n    ----------------\n    maxpower : int\n        Maximum power allowed, i.e., the largest number ``n`` such that\n        ``p(x)**n`` is allowed. This is to limit runaway polynomial size.\n    domain : (2,) ndarray\n        Default domain of the class.\n    window : (2,) ndarray\n        Default window of the class.\n\n    "
    __hash__ = None
    __array_ufunc__ = None
    maxpower = 100
    _superscript_mapping = str.maketrans({'0':'⁰', 
     '1':'¹', 
     '2':'²', 
     '3':'³', 
     '4':'⁴', 
     '5':'⁵', 
     '6':'⁶', 
     '7':'⁷', 
     '8':'⁸', 
     '9':'⁹'})
    _subscript_mapping = str.maketrans({'0':'₀', 
     '1':'₁', 
     '2':'₂', 
     '3':'₃', 
     '4':'₄', 
     '5':'₅', 
     '6':'₆', 
     '7':'₇', 
     '8':'₈', 
     '9':'₉'})
    _use_unicode = not os.name == 'nt'

    @property
    @abc.abstractmethod
    def domain(self):
        pass

    @property
    @abc.abstractmethod
    def window(self):
        pass

    @property
    @abc.abstractmethod
    def basis_name(self):
        pass

    @staticmethod
    @abc.abstractmethod
    def _add(c1, c2):
        pass

    @staticmethod
    @abc.abstractmethod
    def _sub(c1, c2):
        pass

    @staticmethod
    @abc.abstractmethod
    def _mul(c1, c2):
        pass

    @staticmethod
    @abc.abstractmethod
    def _div(c1, c2):
        pass

    @staticmethod
    @abc.abstractmethod
    def _pow(c, pow, maxpower=None):
        pass

    @staticmethod
    @abc.abstractmethod
    def _val(x, c):
        pass

    @staticmethod
    @abc.abstractmethod
    def _int(c, m, k, lbnd, scl):
        pass

    @staticmethod
    @abc.abstractmethod
    def _der(c, m, scl):
        pass

    @staticmethod
    @abc.abstractmethod
    def _fit(x, y, deg, rcond, full):
        pass

    @staticmethod
    @abc.abstractmethod
    def _line(off, scl):
        pass

    @staticmethod
    @abc.abstractmethod
    def _roots(c):
        pass

    @staticmethod
    @abc.abstractmethod
    def _fromroots(r):
        pass

    def has_samecoef(self, other):
        """Check if coefficients match.

        .. versionadded:: 1.6.0

        Parameters
        ----------
        other : class instance
            The other class must have the ``coef`` attribute.

        Returns
        -------
        bool : boolean
            True if the coefficients are the same, False otherwise.

        """
        if len(self.coef) != len(other.coef):
            return False
        if not np.all(self.coef == other.coef):
            return False
        return True

    def has_samedomain(self, other):
        """Check if domains match.

        .. versionadded:: 1.6.0

        Parameters
        ----------
        other : class instance
            The other class must have the ``domain`` attribute.

        Returns
        -------
        bool : boolean
            True if the domains are the same, False otherwise.

        """
        return np.all(self.domain == other.domain)

    def has_samewindow(self, other):
        """Check if windows match.

        .. versionadded:: 1.6.0

        Parameters
        ----------
        other : class instance
            The other class must have the ``window`` attribute.

        Returns
        -------
        bool : boolean
            True if the windows are the same, False otherwise.

        """
        return np.all(self.window == other.window)

    def has_sametype(self, other):
        """Check if types match.

        .. versionadded:: 1.7.0

        Parameters
        ----------
        other : object
            Class instance.

        Returns
        -------
        bool : boolean
            True if other is same class as self

        """
        return isinstance(other, self.__class__)

    def _get_coefficients(self, other):
        """Interpret other as polynomial coefficients.

        The `other` argument is checked to see if it is of the same
        class as self with identical domain and window. If so,
        return its coefficients, otherwise return `other`.

        .. versionadded:: 1.9.0

        Parameters
        ----------
        other : anything
            Object to be checked.

        Returns
        -------
        coef
            The coefficients of`other` if it is a compatible instance,
            of ABCPolyBase, otherwise `other`.

        Raises
        ------
        TypeError
            When `other` is an incompatible instance of ABCPolyBase.

        """
        if isinstance(other, ABCPolyBase):
            if not isinstance(other, self.__class__):
                raise TypeError('Polynomial types differ')
            elif not np.all(self.domain == other.domain):
                raise TypeError('Domains differ')
            elif not np.all(self.window == other.window):
                raise TypeError('Windows differ')
            return other.coef
        return other

    def __init__--- This code section failed: ---

 L. 291         0  LOAD_GLOBAL              pu
                2  LOAD_ATTR                as_series
                4  LOAD_FAST                'coef'
                6  BUILD_LIST_1          1 
                8  LOAD_CONST               False
               10  LOAD_CONST               ('trim',)
               12  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               14  UNPACK_SEQUENCE_1     1 
               16  STORE_FAST               'coef'

 L. 292        18  LOAD_FAST                'coef'
               20  LOAD_FAST                'self'
               22  STORE_ATTR               coef

 L. 294        24  LOAD_FAST                'domain'
               26  LOAD_CONST               None
               28  <117>                 1  ''
               30  POP_JUMP_IF_FALSE    76  'to 76'

 L. 295        32  LOAD_GLOBAL              pu
               34  LOAD_ATTR                as_series
               36  LOAD_FAST                'domain'
               38  BUILD_LIST_1          1 
               40  LOAD_CONST               False
               42  LOAD_CONST               ('trim',)
               44  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               46  UNPACK_SEQUENCE_1     1 
               48  STORE_FAST               'domain'

 L. 296        50  LOAD_GLOBAL              len
               52  LOAD_FAST                'domain'
               54  CALL_FUNCTION_1       1  ''
               56  LOAD_CONST               2
               58  COMPARE_OP               !=
               60  POP_JUMP_IF_FALSE    70  'to 70'

 L. 297        62  LOAD_GLOBAL              ValueError
               64  LOAD_STR                 'Domain has wrong number of elements.'
               66  CALL_FUNCTION_1       1  ''
               68  RAISE_VARARGS_1       1  'exception instance'
             70_0  COME_FROM            60  '60'

 L. 298        70  LOAD_FAST                'domain'
               72  LOAD_FAST                'self'
               74  STORE_ATTR               domain
             76_0  COME_FROM            30  '30'

 L. 300        76  LOAD_FAST                'window'
               78  LOAD_CONST               None
               80  <117>                 1  ''
               82  POP_JUMP_IF_FALSE   128  'to 128'

 L. 301        84  LOAD_GLOBAL              pu
               86  LOAD_ATTR                as_series
               88  LOAD_FAST                'window'
               90  BUILD_LIST_1          1 
               92  LOAD_CONST               False
               94  LOAD_CONST               ('trim',)
               96  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               98  UNPACK_SEQUENCE_1     1 
              100  STORE_FAST               'window'

 L. 302       102  LOAD_GLOBAL              len
              104  LOAD_FAST                'window'
              106  CALL_FUNCTION_1       1  ''
              108  LOAD_CONST               2
              110  COMPARE_OP               !=
              112  POP_JUMP_IF_FALSE   122  'to 122'

 L. 303       114  LOAD_GLOBAL              ValueError
              116  LOAD_STR                 'Window has wrong number of elements.'
              118  CALL_FUNCTION_1       1  ''
              120  RAISE_VARARGS_1       1  'exception instance'
            122_0  COME_FROM           112  '112'

 L. 304       122  LOAD_FAST                'window'
              124  LOAD_FAST                'self'
              126  STORE_ATTR               window
            128_0  COME_FROM            82  '82'

Parse error at or near `<117>' instruction at offset 28

    def __repr__(self):
        coef = repr(self.coef)[6:-1]
        domain = repr(self.domain)[6:-1]
        window = repr(self.window)[6:-1]
        name = self.__class__.__name__
        return f"{name}({coef}, domain={domain}, window={window})"

    def __format__--- This code section failed: ---

 L. 314         0  LOAD_FAST                'fmt_str'
                2  LOAD_STR                 ''
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 315         8  LOAD_FAST                'self'
               10  LOAD_METHOD              __str__
               12  CALL_METHOD_0         0  ''
               14  RETURN_VALUE     
             16_0  COME_FROM             6  '6'

 L. 316        16  LOAD_FAST                'fmt_str'
               18  LOAD_CONST               ('ascii', 'unicode')
               20  <118>                 1  ''
               22  POP_JUMP_IF_FALSE    48  'to 48'

 L. 317        24  LOAD_GLOBAL              ValueError

 L. 318        26  LOAD_STR                 "Unsupported format string '"
               28  LOAD_FAST                'fmt_str'
               30  FORMAT_VALUE          0  ''
               32  LOAD_STR                 "' passed to "

 L. 319        34  LOAD_FAST                'self'
               36  LOAD_ATTR                __class__

 L. 318        38  FORMAT_VALUE          0  ''
               40  LOAD_STR                 ".__format__. Valid options are 'ascii' and 'unicode'"
               42  BUILD_STRING_5        5 

 L. 317        44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            22  '22'

 L. 322        48  LOAD_FAST                'fmt_str'
               50  LOAD_STR                 'ascii'
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_FALSE    68  'to 68'

 L. 323        56  LOAD_FAST                'self'
               58  LOAD_METHOD              _generate_string
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                _str_term_ascii
               64  CALL_METHOD_1         1  ''
               66  RETURN_VALUE     
             68_0  COME_FROM            54  '54'

 L. 324        68  LOAD_FAST                'self'
               70  LOAD_METHOD              _generate_string
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                _str_term_unicode
               76  CALL_METHOD_1         1  ''
               78  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 20

    def __str__(self):
        if self._use_unicode:
            return self._generate_string(self._str_term_unicode)
        return self._generate_string(self._str_term_ascii)

    def _generate_string--- This code section failed: ---

 L. 337         0  LOAD_GLOBAL              np
                2  LOAD_METHOD              get_printoptions
                4  CALL_METHOD_0         0  ''
                6  LOAD_METHOD              get
                8  LOAD_STR                 'linewidth'
               10  LOAD_CONST               75
               12  CALL_METHOD_2         2  ''
               14  STORE_FAST               'linewidth'

 L. 338        16  LOAD_FAST                'linewidth'
               18  LOAD_CONST               1
               20  COMPARE_OP               <
               22  POP_JUMP_IF_FALSE    28  'to 28'

 L. 339        24  LOAD_CONST               1
               26  STORE_FAST               'linewidth'
             28_0  COME_FROM            22  '22'

 L. 340        28  LOAD_FAST                'self'
               30  LOAD_ATTR                coef
               32  LOAD_CONST               0
               34  BINARY_SUBSCR    
               36  FORMAT_VALUE          0  ''
               38  STORE_FAST               'out'

 L. 341        40  LOAD_GLOBAL              enumerate
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                coef
               46  LOAD_CONST               1
               48  LOAD_CONST               None
               50  BUILD_SLICE_2         2 
               52  BINARY_SUBSCR    
               54  CALL_FUNCTION_1       1  ''
               56  GET_ITER         
             58_0  COME_FROM           256  '256'
               58  FOR_ITER            258  'to 258'
               60  UNPACK_SEQUENCE_2     2 
               62  STORE_FAST               'i'
               64  STORE_FAST               'coef'

 L. 342        66  LOAD_FAST                'out'
               68  LOAD_STR                 ' '
               70  INPLACE_ADD      
               72  STORE_FAST               'out'

 L. 343        74  LOAD_GLOBAL              str
               76  LOAD_FAST                'i'
               78  LOAD_CONST               1
               80  BINARY_ADD       
               82  CALL_FUNCTION_1       1  ''
               84  STORE_FAST               'power'

 L. 348        86  SETUP_FINALLY       124  'to 124'

 L. 349        88  LOAD_FAST                'coef'
               90  LOAD_CONST               0
               92  COMPARE_OP               >=
               94  POP_JUMP_IF_FALSE   108  'to 108'

 L. 350        96  LOAD_STR                 '+ '
               98  LOAD_FAST                'coef'
              100  FORMAT_VALUE          0  ''
              102  BUILD_STRING_2        2 
              104  STORE_FAST               'next_term'
              106  JUMP_FORWARD        120  'to 120'
            108_0  COME_FROM            94  '94'

 L. 352       108  LOAD_STR                 '- '
              110  LOAD_FAST                'coef'
              112  UNARY_NEGATIVE   
              114  FORMAT_VALUE          0  ''
              116  BUILD_STRING_2        2 
              118  STORE_FAST               'next_term'
            120_0  COME_FROM           106  '106'
              120  POP_BLOCK        
              122  JUMP_FORWARD        152  'to 152'
            124_0  COME_FROM_FINALLY    86  '86'

 L. 353       124  DUP_TOP          
              126  LOAD_GLOBAL              TypeError
              128  <121>               150  ''
              130  POP_TOP          
              132  POP_TOP          
              134  POP_TOP          

 L. 354       136  LOAD_STR                 '+ '
              138  LOAD_FAST                'coef'
              140  FORMAT_VALUE          0  ''
              142  BUILD_STRING_2        2 
              144  STORE_FAST               'next_term'
              146  POP_EXCEPT       
              148  JUMP_FORWARD        152  'to 152'
              150  <48>             
            152_0  COME_FROM           148  '148'
            152_1  COME_FROM           122  '122'

 L. 356       152  LOAD_FAST                'next_term'
              154  LOAD_FAST                'term_method'
              156  LOAD_FAST                'power'
              158  LOAD_STR                 'x'
              160  CALL_FUNCTION_2       2  ''
              162  INPLACE_ADD      
              164  STORE_FAST               'next_term'

 L. 358       166  LOAD_GLOBAL              len
              168  LOAD_FAST                'out'
              170  LOAD_METHOD              split
              172  LOAD_STR                 '\n'
              174  CALL_METHOD_1         1  ''
              176  LOAD_CONST               -1
              178  BINARY_SUBSCR    
              180  CALL_FUNCTION_1       1  ''
              182  LOAD_GLOBAL              len
              184  LOAD_FAST                'next_term'
              186  CALL_FUNCTION_1       1  ''
              188  BINARY_ADD       
              190  STORE_FAST               'line_len'

 L. 361       192  LOAD_FAST                'i'
              194  LOAD_GLOBAL              len
              196  LOAD_FAST                'self'
              198  LOAD_ATTR                coef
              200  LOAD_CONST               1
              202  LOAD_CONST               None
              204  BUILD_SLICE_2         2 
              206  BINARY_SUBSCR    
              208  CALL_FUNCTION_1       1  ''
              210  LOAD_CONST               1
              212  BINARY_SUBTRACT  
              214  COMPARE_OP               <
              216  POP_JUMP_IF_FALSE   226  'to 226'

 L. 362       218  LOAD_FAST                'line_len'
              220  LOAD_CONST               2
              222  INPLACE_ADD      
              224  STORE_FAST               'line_len'
            226_0  COME_FROM           216  '216'

 L. 364       226  LOAD_FAST                'line_len'
              228  LOAD_FAST                'linewidth'
              230  COMPARE_OP               >=
              232  POP_JUMP_IF_FALSE   248  'to 248'

 L. 365       234  LOAD_FAST                'next_term'
              236  LOAD_METHOD              replace
              238  LOAD_STR                 ' '
              240  LOAD_STR                 '\n'
              242  LOAD_CONST               1
              244  CALL_METHOD_3         3  ''
              246  STORE_FAST               'next_term'
            248_0  COME_FROM           232  '232'

 L. 366       248  LOAD_FAST                'out'
              250  LOAD_FAST                'next_term'
              252  INPLACE_ADD      
              254  STORE_FAST               'out'
              256  JUMP_BACK            58  'to 58'
            258_0  COME_FROM            58  '58'

 L. 367       258  LOAD_FAST                'out'
              260  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 128

    @classmethod
    def _str_term_unicode--- This code section failed: ---

 L. 375         0  LOAD_FAST                'cls'
                2  LOAD_ATTR                basis_name
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 376        10  LOAD_GLOBAL              NotImplementedError

 L. 377        12  LOAD_STR                 'Subclasses must define either a basis_name, or override _str_term_unicode(cls, i, arg_str)'

 L. 376        14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 380        18  LOAD_STR                 '·'
               20  LOAD_FAST                'cls'
               22  LOAD_ATTR                basis_name
               24  FORMAT_VALUE          0  ''
               26  LOAD_FAST                'i'
               28  LOAD_METHOD              translate
               30  LOAD_FAST                'cls'
               32  LOAD_ATTR                _subscript_mapping
               34  CALL_METHOD_1         1  ''
               36  FORMAT_VALUE          0  ''
               38  LOAD_STR                 '('

 L. 381        40  LOAD_FAST                'arg_str'

 L. 380        42  FORMAT_VALUE          0  ''
               44  LOAD_STR                 ')'
               46  BUILD_STRING_6        6 
               48  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @classmethod
    def _str_term_ascii--- This code section failed: ---

 L. 389         0  LOAD_FAST                'cls'
                2  LOAD_ATTR                basis_name
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 390        10  LOAD_GLOBAL              NotImplementedError

 L. 391        12  LOAD_STR                 'Subclasses must define either a basis_name, or override _str_term_ascii(cls, i, arg_str)'

 L. 390        14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 394        18  LOAD_STR                 ' '
               20  LOAD_FAST                'cls'
               22  LOAD_ATTR                basis_name
               24  FORMAT_VALUE          0  ''
               26  LOAD_STR                 '_'
               28  LOAD_FAST                'i'
               30  FORMAT_VALUE          0  ''
               32  LOAD_STR                 '('
               34  LOAD_FAST                'arg_str'
               36  FORMAT_VALUE          0  ''
               38  LOAD_STR                 ')'
               40  BUILD_STRING_7        7 
               42  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @classmethod
    def _repr_latex_term--- This code section failed: ---

 L. 398         0  LOAD_FAST                'cls'
                2  LOAD_ATTR                basis_name
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 399        10  LOAD_GLOBAL              NotImplementedError

 L. 400        12  LOAD_STR                 'Subclasses must define either a basis name, or override _repr_latex_term(i, arg_str, needs_parens)'

 L. 399        14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 403        18  LOAD_STR                 '{'
               20  LOAD_FAST                'cls'
               22  LOAD_ATTR                basis_name
               24  FORMAT_VALUE          0  ''
               26  LOAD_STR                 '}_{'
               28  LOAD_FAST                'i'
               30  FORMAT_VALUE          0  ''
               32  LOAD_STR                 '}('
               34  LOAD_FAST                'arg_str'
               36  FORMAT_VALUE          0  ''
               38  LOAD_STR                 ')'
               40  BUILD_STRING_7        7 
               42  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @staticmethod
    def _repr_latex_scalar(x):
        return '\\text{{{}}}'.format(x)

    def _repr_latex_(self):
        off, scale = self.mapparms
        if off == 0 and scale == 1:
            term = 'x'
            needs_parens = False
        elif scale == 1:
            term = f"{self._repr_latex_scalar(off)} + x"
            needs_parens = True
        elif off == 0:
            term = f"{self._repr_latex_scalar(scale)}x"
            needs_parens = True
        else:
            term = f"{self._repr_latex_scalar(off)} + {self._repr_latex_scalar(scale)}x"
            needs_parens = True
        mute = '\\color{{LightGray}}{{{}}}'.format
        parts = []
        for i, c in enumerate(self.coef):
            if i == 0:
                coef_str = f"{self._repr_latex_scalar(c)}"
            elif not isinstance(c, numbers.Real):
                coef_str = f" + ({self._repr_latex_scalar(c)})"
            elif not np.signbit(c):
                coef_str = f" + {self._repr_latex_scalar(c)}"
            else:
                coef_str = f" - {self._repr_latex_scalar(-c)}"
            term_str = self._repr_latex_termitermneeds_parens
            if term_str == '1':
                part = coef_str
            else:
                part = f"{coef_str}\\,{term_str}"
            if c == 0:
                part = mute(part)
            else:
                parts.append(part)
        else:
            if parts:
                body = ''.join(parts)
            else:
                body = '0'
            return f"$x \\mapsto {body}$"

    def __getstate__(self):
        ret = self.__dict__.copy
        ret['coef'] = self.coef.copy
        ret['domain'] = self.domain.copy
        ret['window'] = self.window.copy
        return ret

    def __setstate__(self, dict):
        self.__dict__ = dict

    def __call__(self, arg):
        off, scl = pu.mapparmsself.domainself.window
        arg = off + scl * arg
        return self._valargself.coef

    def __iter__(self):
        return iter(self.coef)

    def __len__(self):
        return len(self.coef)

    def __neg__(self):
        return self.__class__(-self.coef)self.domainself.window

    def __pos__(self):
        return self

    def __add__--- This code section failed: ---

 L. 500         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _get_coefficients
                4  LOAD_FAST                'other'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'othercoef'

 L. 501        10  SETUP_FINALLY        30  'to 30'

 L. 502        12  LOAD_FAST                'self'
               14  LOAD_METHOD              _add
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                coef
               20  LOAD_FAST                'othercoef'
               22  CALL_METHOD_2         2  ''
               24  STORE_FAST               'coef'
               26  POP_BLOCK        
               28  JUMP_FORWARD         52  'to 52'
             30_0  COME_FROM_FINALLY    10  '10'

 L. 503        30  DUP_TOP          
               32  LOAD_GLOBAL              Exception
               34  <121>                50  ''
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 504        42  LOAD_GLOBAL              NotImplemented
               44  ROT_FOUR         
               46  POP_EXCEPT       
               48  RETURN_VALUE     
               50  <48>             
             52_0  COME_FROM            28  '28'

 L. 505        52  LOAD_FAST                'self'
               54  LOAD_METHOD              __class__
               56  LOAD_FAST                'coef'
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                domain
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                window
               66  CALL_METHOD_3         3  ''
               68  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 34

    def __sub__--- This code section failed: ---

 L. 508         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _get_coefficients
                4  LOAD_FAST                'other'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'othercoef'

 L. 509        10  SETUP_FINALLY        30  'to 30'

 L. 510        12  LOAD_FAST                'self'
               14  LOAD_METHOD              _sub
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                coef
               20  LOAD_FAST                'othercoef'
               22  CALL_METHOD_2         2  ''
               24  STORE_FAST               'coef'
               26  POP_BLOCK        
               28  JUMP_FORWARD         52  'to 52'
             30_0  COME_FROM_FINALLY    10  '10'

 L. 511        30  DUP_TOP          
               32  LOAD_GLOBAL              Exception
               34  <121>                50  ''
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 512        42  LOAD_GLOBAL              NotImplemented
               44  ROT_FOUR         
               46  POP_EXCEPT       
               48  RETURN_VALUE     
               50  <48>             
             52_0  COME_FROM            28  '28'

 L. 513        52  LOAD_FAST                'self'
               54  LOAD_METHOD              __class__
               56  LOAD_FAST                'coef'
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                domain
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                window
               66  CALL_METHOD_3         3  ''
               68  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 34

    def __mul__--- This code section failed: ---

 L. 516         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _get_coefficients
                4  LOAD_FAST                'other'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'othercoef'

 L. 517        10  SETUP_FINALLY        30  'to 30'

 L. 518        12  LOAD_FAST                'self'
               14  LOAD_METHOD              _mul
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                coef
               20  LOAD_FAST                'othercoef'
               22  CALL_METHOD_2         2  ''
               24  STORE_FAST               'coef'
               26  POP_BLOCK        
               28  JUMP_FORWARD         52  'to 52'
             30_0  COME_FROM_FINALLY    10  '10'

 L. 519        30  DUP_TOP          
               32  LOAD_GLOBAL              Exception
               34  <121>                50  ''
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 520        42  LOAD_GLOBAL              NotImplemented
               44  ROT_FOUR         
               46  POP_EXCEPT       
               48  RETURN_VALUE     
               50  <48>             
             52_0  COME_FROM            28  '28'

 L. 521        52  LOAD_FAST                'self'
               54  LOAD_METHOD              __class__
               56  LOAD_FAST                'coef'
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                domain
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                window
               66  CALL_METHOD_3         3  ''
               68  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 34

    def __truediv__(self, other):
        if not isinstance(other, numbers.Number) or isinstance(other, bool):
            raise TypeError(f"unsupported types for true division: '{type(self)}', '{type(other)}'")
        return self.__floordiv__(other)

    def __floordiv__--- This code section failed: ---

 L. 535         0  LOAD_FAST                'self'
                2  LOAD_METHOD              __divmod__
                4  LOAD_FAST                'other'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'res'

 L. 536        10  LOAD_FAST                'res'
               12  LOAD_GLOBAL              NotImplemented
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    22  'to 22'

 L. 537        18  LOAD_FAST                'res'
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L. 538        22  LOAD_FAST                'res'
               24  LOAD_CONST               0
               26  BINARY_SUBSCR    
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 14

    def __mod__--- This code section failed: ---

 L. 541         0  LOAD_FAST                'self'
                2  LOAD_METHOD              __divmod__
                4  LOAD_FAST                'other'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'res'

 L. 542        10  LOAD_FAST                'res'
               12  LOAD_GLOBAL              NotImplemented
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    22  'to 22'

 L. 543        18  LOAD_FAST                'res'
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L. 544        22  LOAD_FAST                'res'
               24  LOAD_CONST               1
               26  BINARY_SUBSCR    
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 14

    def __divmod__--- This code section failed: ---

 L. 547         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _get_coefficients
                4  LOAD_FAST                'other'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'othercoef'

 L. 548        10  SETUP_FINALLY        34  'to 34'

 L. 549        12  LOAD_FAST                'self'
               14  LOAD_METHOD              _div
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                coef
               20  LOAD_FAST                'othercoef'
               22  CALL_METHOD_2         2  ''
               24  UNPACK_SEQUENCE_2     2 
               26  STORE_FAST               'quo'
               28  STORE_FAST               'rem'
               30  POP_BLOCK        
               32  JUMP_FORWARD         74  'to 74'
             34_0  COME_FROM_FINALLY    10  '10'

 L. 550        34  DUP_TOP          
               36  LOAD_GLOBAL              ZeroDivisionError
               38  <121>                52  ''
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L. 551        46  RAISE_VARARGS_0       0  'reraise'
               48  POP_EXCEPT       
               50  JUMP_FORWARD         74  'to 74'

 L. 552        52  DUP_TOP          
               54  LOAD_GLOBAL              Exception
               56  <121>                72  ''
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          

 L. 553        64  LOAD_GLOBAL              NotImplemented
               66  ROT_FOUR         
               68  POP_EXCEPT       
               70  RETURN_VALUE     
               72  <48>             
             74_0  COME_FROM            50  '50'
             74_1  COME_FROM            32  '32'

 L. 554        74  LOAD_FAST                'self'
               76  LOAD_METHOD              __class__
               78  LOAD_FAST                'quo'
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                domain
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                window
               88  CALL_METHOD_3         3  ''
               90  STORE_FAST               'quo'

 L. 555        92  LOAD_FAST                'self'
               94  LOAD_METHOD              __class__
               96  LOAD_FAST                'rem'
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                domain
              102  LOAD_FAST                'self'
              104  LOAD_ATTR                window
              106  CALL_METHOD_3         3  ''
              108  STORE_FAST               'rem'

 L. 556       110  LOAD_FAST                'quo'
              112  LOAD_FAST                'rem'
              114  BUILD_TUPLE_2         2 
              116  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 38

    def __pow__(self, other):
        coef = self._pow((self.coef), other, maxpower=(self.maxpower))
        res = self.__class__coefself.domainself.window
        return res

    def __radd__--- This code section failed: ---

 L. 564         0  SETUP_FINALLY        20  'to 20'

 L. 565         2  LOAD_FAST                'self'
                4  LOAD_METHOD              _add
                6  LOAD_FAST                'other'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                coef
               12  CALL_METHOD_2         2  ''
               14  STORE_FAST               'coef'
               16  POP_BLOCK        
               18  JUMP_FORWARD         42  'to 42'
             20_0  COME_FROM_FINALLY     0  '0'

 L. 566        20  DUP_TOP          
               22  LOAD_GLOBAL              Exception
               24  <121>                40  ''
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 567        32  LOAD_GLOBAL              NotImplemented
               34  ROT_FOUR         
               36  POP_EXCEPT       
               38  RETURN_VALUE     
               40  <48>             
             42_0  COME_FROM            18  '18'

 L. 568        42  LOAD_FAST                'self'
               44  LOAD_METHOD              __class__
               46  LOAD_FAST                'coef'
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                domain
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                window
               56  CALL_METHOD_3         3  ''
               58  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 24

    def __rsub__--- This code section failed: ---

 L. 571         0  SETUP_FINALLY        20  'to 20'

 L. 572         2  LOAD_FAST                'self'
                4  LOAD_METHOD              _sub
                6  LOAD_FAST                'other'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                coef
               12  CALL_METHOD_2         2  ''
               14  STORE_FAST               'coef'
               16  POP_BLOCK        
               18  JUMP_FORWARD         42  'to 42'
             20_0  COME_FROM_FINALLY     0  '0'

 L. 573        20  DUP_TOP          
               22  LOAD_GLOBAL              Exception
               24  <121>                40  ''
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 574        32  LOAD_GLOBAL              NotImplemented
               34  ROT_FOUR         
               36  POP_EXCEPT       
               38  RETURN_VALUE     
               40  <48>             
             42_0  COME_FROM            18  '18'

 L. 575        42  LOAD_FAST                'self'
               44  LOAD_METHOD              __class__
               46  LOAD_FAST                'coef'
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                domain
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                window
               56  CALL_METHOD_3         3  ''
               58  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 24

    def __rmul__--- This code section failed: ---

 L. 578         0  SETUP_FINALLY        20  'to 20'

 L. 579         2  LOAD_FAST                'self'
                4  LOAD_METHOD              _mul
                6  LOAD_FAST                'other'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                coef
               12  CALL_METHOD_2         2  ''
               14  STORE_FAST               'coef'
               16  POP_BLOCK        
               18  JUMP_FORWARD         42  'to 42'
             20_0  COME_FROM_FINALLY     0  '0'

 L. 580        20  DUP_TOP          
               22  LOAD_GLOBAL              Exception
               24  <121>                40  ''
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 581        32  LOAD_GLOBAL              NotImplemented
               34  ROT_FOUR         
               36  POP_EXCEPT       
               38  RETURN_VALUE     
               40  <48>             
             42_0  COME_FROM            18  '18'

 L. 582        42  LOAD_FAST                'self'
               44  LOAD_METHOD              __class__
               46  LOAD_FAST                'coef'
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                domain
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                window
               56  CALL_METHOD_3         3  ''
               58  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 24

    def __rdiv__(self, other):
        return self.__rfloordiv__(other)

    def __rtruediv__(self, other):
        return NotImplemented

    def __rfloordiv__--- This code section failed: ---

 L. 594         0  LOAD_FAST                'self'
                2  LOAD_METHOD              __rdivmod__
                4  LOAD_FAST                'other'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'res'

 L. 595        10  LOAD_FAST                'res'
               12  LOAD_GLOBAL              NotImplemented
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    22  'to 22'

 L. 596        18  LOAD_FAST                'res'
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L. 597        22  LOAD_FAST                'res'
               24  LOAD_CONST               0
               26  BINARY_SUBSCR    
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 14

    def __rmod__--- This code section failed: ---

 L. 600         0  LOAD_FAST                'self'
                2  LOAD_METHOD              __rdivmod__
                4  LOAD_FAST                'other'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'res'

 L. 601        10  LOAD_FAST                'res'
               12  LOAD_GLOBAL              NotImplemented
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    22  'to 22'

 L. 602        18  LOAD_FAST                'res'
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L. 603        22  LOAD_FAST                'res'
               24  LOAD_CONST               1
               26  BINARY_SUBSCR    
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 14

    def __rdivmod__--- This code section failed: ---

 L. 606         0  SETUP_FINALLY        24  'to 24'

 L. 607         2  LOAD_FAST                'self'
                4  LOAD_METHOD              _div
                6  LOAD_FAST                'other'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                coef
               12  CALL_METHOD_2         2  ''
               14  UNPACK_SEQUENCE_2     2 
               16  STORE_FAST               'quo'
               18  STORE_FAST               'rem'
               20  POP_BLOCK        
               22  JUMP_FORWARD         64  'to 64'
             24_0  COME_FROM_FINALLY     0  '0'

 L. 608        24  DUP_TOP          
               26  LOAD_GLOBAL              ZeroDivisionError
               28  <121>                42  ''
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L. 609        36  RAISE_VARARGS_0       0  'reraise'
               38  POP_EXCEPT       
               40  JUMP_FORWARD         64  'to 64'

 L. 610        42  DUP_TOP          
               44  LOAD_GLOBAL              Exception
               46  <121>                62  ''
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L. 611        54  LOAD_GLOBAL              NotImplemented
               56  ROT_FOUR         
               58  POP_EXCEPT       
               60  RETURN_VALUE     
               62  <48>             
             64_0  COME_FROM            40  '40'
             64_1  COME_FROM            22  '22'

 L. 612        64  LOAD_FAST                'self'
               66  LOAD_METHOD              __class__
               68  LOAD_FAST                'quo'
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                domain
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                window
               78  CALL_METHOD_3         3  ''
               80  STORE_FAST               'quo'

 L. 613        82  LOAD_FAST                'self'
               84  LOAD_METHOD              __class__
               86  LOAD_FAST                'rem'
               88  LOAD_FAST                'self'
               90  LOAD_ATTR                domain
               92  LOAD_FAST                'self'
               94  LOAD_ATTR                window
               96  CALL_METHOD_3         3  ''
               98  STORE_FAST               'rem'

 L. 614       100  LOAD_FAST                'quo'
              102  LOAD_FAST                'rem'
              104  BUILD_TUPLE_2         2 
              106  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 28

    def __eq__(self, other):
        res = isinstance(other, self.__class__) and np.all(self.domain == other.domain) and np.all(self.window == other.window) and self.coef.shape == other.coef.shape and np.all(self.coef == other.coef)
        return res

    def __ne__(self, other):
        return not self.__eq__(other)

    def copy(self):
        """Return a copy.

        Returns
        -------
        new_series : series
            Copy of self.

        """
        return self.__class__self.coefself.domainself.window

    def degree(self):
        """The degree of the series.

        .. versionadded:: 1.5.0

        Returns
        -------
        degree : int
            Degree of the series, one less than the number of coefficients.

        """
        return len(self) - 1

    def cutdeg(self, deg):
        """Truncate series to the given degree.

        Reduce the degree of the series to `deg` by discarding the
        high order terms. If `deg` is greater than the current degree a
        copy of the current series is returned. This can be useful in least
        squares where the coefficients of the high degree terms may be very
        small.

        .. versionadded:: 1.5.0

        Parameters
        ----------
        deg : non-negative int
            The series is reduced to degree `deg` by discarding the high
            order terms. The value of `deg` must be a non-negative integer.

        Returns
        -------
        new_series : series
            New instance of series with reduced degree.

        """
        return self.truncate(deg + 1)

    def trim(self, tol=0):
        """Remove trailing coefficients

        Remove trailing coefficients until a coefficient is reached whose
        absolute value greater than `tol` or the beginning of the series is
        reached. If all the coefficients would be removed the series is set
        to ``[0]``. A new series instance is returned with the new
        coefficients.  The current instance remains unchanged.

        Parameters
        ----------
        tol : non-negative number.
            All trailing coefficients less than `tol` will be removed.

        Returns
        -------
        new_series : series
            New instance of series with trimmed coefficients.

        """
        coef = pu.trimcoefself.coeftol
        return self.__class__coefself.domainself.window

    def truncate(self, size):
        """Truncate series to length `size`.

        Reduce the series to length `size` by discarding the high
        degree terms. The value of `size` must be a positive integer. This
        can be useful in least squares where the coefficients of the
        high degree terms may be very small.

        Parameters
        ----------
        size : positive int
            The series is reduced to length `size` by discarding the high
            degree terms. The value of `size` must be a positive integer.

        Returns
        -------
        new_series : series
            New instance of series with truncated coefficients.

        """
        isize = int(size)
        if isize != size or (isize < 1):
            raise ValueError('size must be a positive integer')
        if isize >= len(self.coef):
            coef = self.coef
        else:
            coef = self.coef[:isize]
        return self.__class__coefself.domainself.window

    def convert--- This code section failed: ---

 L. 761         0  LOAD_FAST                'kind'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 762         8  LOAD_FAST                'self'
               10  LOAD_ATTR                __class__
               12  STORE_FAST               'kind'
             14_0  COME_FROM             6  '6'

 L. 763        14  LOAD_FAST                'domain'
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_FALSE    28  'to 28'

 L. 764        22  LOAD_FAST                'kind'
               24  LOAD_ATTR                domain
               26  STORE_FAST               'domain'
             28_0  COME_FROM            20  '20'

 L. 765        28  LOAD_FAST                'window'
               30  LOAD_CONST               None
               32  <117>                 0  ''
               34  POP_JUMP_IF_FALSE    42  'to 42'

 L. 766        36  LOAD_FAST                'kind'
               38  LOAD_ATTR                window
               40  STORE_FAST               'window'
             42_0  COME_FROM            34  '34'

 L. 767        42  LOAD_FAST                'self'
               44  LOAD_FAST                'kind'
               46  LOAD_ATTR                identity
               48  LOAD_FAST                'domain'
               50  LOAD_FAST                'window'
               52  LOAD_CONST               ('window',)
               54  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               56  CALL_FUNCTION_1       1  ''
               58  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def mapparms(self):
        """Return the mapping parameters.

        The returned values define a linear map ``off + scl*x`` that is
        applied to the input arguments before the series is evaluated. The
        map depends on the ``domain`` and ``window``; if the current
        ``domain`` is equal to the ``window`` the resulting map is the
        identity.  If the coefficients of the series instance are to be
        used by themselves outside this class, then the linear function
        must be substituted for the ``x`` in the standard representation of
        the base polynomials.

        Returns
        -------
        off, scl : float or complex
            The mapping function is defined by ``off + scl*x``.

        Notes
        -----
        If the current domain is the interval ``[l1, r1]`` and the window
        is ``[l2, r2]``, then the linear mapping function ``L`` is
        defined by the equations::

            L(l1) = l2
            L(r1) = r2

        """
        return pu.mapparmsself.domainself.window

    def integ--- This code section failed: ---

 L. 823         0  LOAD_FAST                'self'
                2  LOAD_METHOD              mapparms
                4  CALL_METHOD_0         0  ''
                6  UNPACK_SEQUENCE_2     2 
                8  STORE_FAST               'off'
               10  STORE_FAST               'scl'

 L. 824        12  LOAD_FAST                'lbnd'
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    26  'to 26'

 L. 825        20  LOAD_CONST               0
               22  STORE_FAST               'lbnd'
               24  JUMP_FORWARD         38  'to 38'
             26_0  COME_FROM            18  '18'

 L. 827        26  LOAD_FAST                'off'
               28  LOAD_FAST                'scl'
               30  LOAD_FAST                'lbnd'
               32  BINARY_MULTIPLY  
               34  BINARY_ADD       
               36  STORE_FAST               'lbnd'
             38_0  COME_FROM            24  '24'

 L. 828        38  LOAD_FAST                'self'
               40  LOAD_METHOD              _int
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                coef
               46  LOAD_FAST                'm'
               48  LOAD_FAST                'k'
               50  LOAD_FAST                'lbnd'
               52  LOAD_CONST               1.0
               54  LOAD_FAST                'scl'
               56  BINARY_TRUE_DIVIDE
               58  CALL_METHOD_5         5  ''
               60  STORE_FAST               'coef'

 L. 829        62  LOAD_FAST                'self'
               64  LOAD_METHOD              __class__
               66  LOAD_FAST                'coef'
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                domain
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                window
               76  CALL_METHOD_3         3  ''
               78  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 16

    def deriv(self, m=1):
        """Differentiate.

        Return a series instance of that is the derivative of the current
        series.

        Parameters
        ----------
        m : non-negative int
            Find the derivative of order `m`.

        Returns
        -------
        new_series : series
            A new series representing the derivative. The domain is the same
            as the domain of the differentiated series.

        """
        off, scl = self.mapparms
        coef = self._derself.coefmscl
        return self.__class__coefself.domainself.window

    def roots(self):
        """Return the roots of the series polynomial.

        Compute the roots for the series. Note that the accuracy of the
        roots decrease the further outside the domain they lie.

        Returns
        -------
        roots : ndarray
            Array containing the roots of the series.

        """
        roots = self._roots(self.coef)
        return pu.mapdomainrootsself.windowself.domain

    def linspace--- This code section failed: ---

 L. 894         0  LOAD_FAST                'domain'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 895         8  LOAD_FAST                'self'
               10  LOAD_ATTR                domain
               12  STORE_FAST               'domain'
             14_0  COME_FROM             6  '6'

 L. 896        14  LOAD_GLOBAL              np
               16  LOAD_METHOD              linspace
               18  LOAD_FAST                'domain'
               20  LOAD_CONST               0
               22  BINARY_SUBSCR    
               24  LOAD_FAST                'domain'
               26  LOAD_CONST               1
               28  BINARY_SUBSCR    
               30  LOAD_FAST                'n'
               32  CALL_METHOD_3         3  ''
               34  STORE_FAST               'x'

 L. 897        36  LOAD_FAST                'self'
               38  LOAD_FAST                'x'
               40  CALL_FUNCTION_1       1  ''
               42  STORE_FAST               'y'

 L. 898        44  LOAD_FAST                'x'
               46  LOAD_FAST                'y'
               48  BUILD_TUPLE_2         2 
               50  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @classmethod
    def fit--- This code section failed: ---

 L. 971         0  LOAD_FAST                'domain'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    20  'to 20'

 L. 972         8  LOAD_GLOBAL              pu
               10  LOAD_METHOD              getdomain
               12  LOAD_FAST                'x'
               14  CALL_METHOD_1         1  ''
               16  STORE_FAST               'domain'
               18  JUMP_FORWARD         50  'to 50'
             20_0  COME_FROM             6  '6'

 L. 973        20  LOAD_GLOBAL              type
               22  LOAD_FAST                'domain'
               24  CALL_FUNCTION_1       1  ''
               26  LOAD_GLOBAL              list
               28  <117>                 0  ''
               30  POP_JUMP_IF_FALSE    50  'to 50'
               32  LOAD_GLOBAL              len
               34  LOAD_FAST                'domain'
               36  CALL_FUNCTION_1       1  ''
               38  LOAD_CONST               0
               40  COMPARE_OP               ==
               42  POP_JUMP_IF_FALSE    50  'to 50'

 L. 974        44  LOAD_FAST                'cls'
               46  LOAD_ATTR                domain
               48  STORE_FAST               'domain'
             50_0  COME_FROM            42  '42'
             50_1  COME_FROM            30  '30'
             50_2  COME_FROM            18  '18'

 L. 976        50  LOAD_FAST                'window'
               52  LOAD_CONST               None
               54  <117>                 0  ''
               56  POP_JUMP_IF_FALSE    64  'to 64'

 L. 977        58  LOAD_FAST                'cls'
               60  LOAD_ATTR                window
               62  STORE_FAST               'window'
             64_0  COME_FROM            56  '56'

 L. 979        64  LOAD_GLOBAL              pu
               66  LOAD_METHOD              mapdomain
               68  LOAD_FAST                'x'
               70  LOAD_FAST                'domain'
               72  LOAD_FAST                'window'
               74  CALL_METHOD_3         3  ''
               76  STORE_FAST               'xnew'

 L. 980        78  LOAD_FAST                'cls'
               80  LOAD_ATTR                _fit
               82  LOAD_FAST                'xnew'
               84  LOAD_FAST                'y'
               86  LOAD_FAST                'deg'
               88  LOAD_FAST                'w'
               90  LOAD_FAST                'rcond'
               92  LOAD_FAST                'full'
               94  LOAD_CONST               ('w', 'rcond', 'full')
               96  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
               98  STORE_FAST               'res'

 L. 981       100  LOAD_FAST                'full'
              102  POP_JUMP_IF_FALSE   130  'to 130'

 L. 982       104  LOAD_FAST                'res'
              106  UNPACK_SEQUENCE_2     2 
              108  STORE_FAST               'coef'
              110  STORE_FAST               'status'

 L. 983       112  LOAD_FAST                'cls'
              114  LOAD_FAST                'coef'
              116  LOAD_FAST                'domain'
              118  LOAD_FAST                'window'
              120  LOAD_CONST               ('domain', 'window')
              122  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              124  LOAD_FAST                'status'
              126  BUILD_TUPLE_2         2 
              128  RETURN_VALUE     
            130_0  COME_FROM           102  '102'

 L. 985       130  LOAD_FAST                'res'
              132  STORE_FAST               'coef'

 L. 986       134  LOAD_FAST                'cls'
              136  LOAD_FAST                'coef'
              138  LOAD_FAST                'domain'
              140  LOAD_FAST                'window'
              142  LOAD_CONST               ('domain', 'window')
              144  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              146  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1

    @classmethod
    def fromroots--- This code section failed: ---

 L.1014         0  LOAD_GLOBAL              pu
                2  LOAD_ATTR                as_series
                4  LOAD_FAST                'roots'
                6  BUILD_LIST_1          1 
                8  LOAD_CONST               False
               10  LOAD_CONST               ('trim',)
               12  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               14  UNPACK_SEQUENCE_1     1 
               16  STORE_FAST               'roots'

 L.1015        18  LOAD_FAST                'domain'
               20  LOAD_CONST               None
               22  <117>                 0  ''
               24  POP_JUMP_IF_FALSE    38  'to 38'

 L.1016        26  LOAD_GLOBAL              pu
               28  LOAD_METHOD              getdomain
               30  LOAD_FAST                'roots'
               32  CALL_METHOD_1         1  ''
               34  STORE_FAST               'domain'
               36  JUMP_FORWARD         68  'to 68'
             38_0  COME_FROM            24  '24'

 L.1017        38  LOAD_GLOBAL              type
               40  LOAD_FAST                'domain'
               42  CALL_FUNCTION_1       1  ''
               44  LOAD_GLOBAL              list
               46  <117>                 0  ''
               48  POP_JUMP_IF_FALSE    68  'to 68'
               50  LOAD_GLOBAL              len
               52  LOAD_FAST                'domain'
               54  CALL_FUNCTION_1       1  ''
               56  LOAD_CONST               0
               58  COMPARE_OP               ==
               60  POP_JUMP_IF_FALSE    68  'to 68'

 L.1018        62  LOAD_FAST                'cls'
               64  LOAD_ATTR                domain
               66  STORE_FAST               'domain'
             68_0  COME_FROM            60  '60'
             68_1  COME_FROM            48  '48'
             68_2  COME_FROM            36  '36'

 L.1020        68  LOAD_FAST                'window'
               70  LOAD_CONST               None
               72  <117>                 0  ''
               74  POP_JUMP_IF_FALSE    82  'to 82'

 L.1021        76  LOAD_FAST                'cls'
               78  LOAD_ATTR                window
               80  STORE_FAST               'window'
             82_0  COME_FROM            74  '74'

 L.1023        82  LOAD_GLOBAL              len
               84  LOAD_FAST                'roots'
               86  CALL_FUNCTION_1       1  ''
               88  STORE_FAST               'deg'

 L.1024        90  LOAD_GLOBAL              pu
               92  LOAD_METHOD              mapparms
               94  LOAD_FAST                'domain'
               96  LOAD_FAST                'window'
               98  CALL_METHOD_2         2  ''
              100  UNPACK_SEQUENCE_2     2 
              102  STORE_FAST               'off'
              104  STORE_FAST               'scl'

 L.1025       106  LOAD_FAST                'off'
              108  LOAD_FAST                'scl'
              110  LOAD_FAST                'roots'
              112  BINARY_MULTIPLY  
              114  BINARY_ADD       
              116  STORE_FAST               'rnew'

 L.1026       118  LOAD_FAST                'cls'
              120  LOAD_METHOD              _fromroots
              122  LOAD_FAST                'rnew'
              124  CALL_METHOD_1         1  ''
              126  LOAD_FAST                'scl'
              128  LOAD_FAST                'deg'
              130  BINARY_POWER     
              132  BINARY_TRUE_DIVIDE
              134  STORE_FAST               'coef'

 L.1027       136  LOAD_FAST                'cls'
              138  LOAD_FAST                'coef'
              140  LOAD_FAST                'domain'
              142  LOAD_FAST                'window'
              144  LOAD_CONST               ('domain', 'window')
              146  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              148  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 22

    @classmethod
    def identity--- This code section failed: ---

 L.1054         0  LOAD_FAST                'domain'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L.1055         8  LOAD_FAST                'cls'
               10  LOAD_ATTR                domain
               12  STORE_FAST               'domain'
             14_0  COME_FROM             6  '6'

 L.1056        14  LOAD_FAST                'window'
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_FALSE    28  'to 28'

 L.1057        22  LOAD_FAST                'cls'
               24  LOAD_ATTR                window
               26  STORE_FAST               'window'
             28_0  COME_FROM            20  '20'

 L.1058        28  LOAD_GLOBAL              pu
               30  LOAD_METHOD              mapparms
               32  LOAD_FAST                'window'
               34  LOAD_FAST                'domain'
               36  CALL_METHOD_2         2  ''
               38  UNPACK_SEQUENCE_2     2 
               40  STORE_FAST               'off'
               42  STORE_FAST               'scl'

 L.1059        44  LOAD_FAST                'cls'
               46  LOAD_METHOD              _line
               48  LOAD_FAST                'off'
               50  LOAD_FAST                'scl'
               52  CALL_METHOD_2         2  ''
               54  STORE_FAST               'coef'

 L.1060        56  LOAD_FAST                'cls'
               58  LOAD_FAST                'coef'
               60  LOAD_FAST                'domain'
               62  LOAD_FAST                'window'
               64  CALL_FUNCTION_3       3  ''
               66  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @classmethod
    def basis--- This code section failed: ---

 L.1091         0  LOAD_FAST                'domain'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L.1092         8  LOAD_FAST                'cls'
               10  LOAD_ATTR                domain
               12  STORE_FAST               'domain'
             14_0  COME_FROM             6  '6'

 L.1093        14  LOAD_FAST                'window'
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_FALSE    28  'to 28'

 L.1094        22  LOAD_FAST                'cls'
               24  LOAD_ATTR                window
               26  STORE_FAST               'window'
             28_0  COME_FROM            20  '20'

 L.1095        28  LOAD_GLOBAL              int
               30  LOAD_FAST                'deg'
               32  CALL_FUNCTION_1       1  ''
               34  STORE_FAST               'ideg'

 L.1097        36  LOAD_FAST                'ideg'
               38  LOAD_FAST                'deg'
               40  COMPARE_OP               !=
               42  POP_JUMP_IF_TRUE     52  'to 52'
               44  LOAD_FAST                'ideg'
               46  LOAD_CONST               0
               48  COMPARE_OP               <
               50  POP_JUMP_IF_FALSE    60  'to 60'
             52_0  COME_FROM            42  '42'

 L.1098        52  LOAD_GLOBAL              ValueError
               54  LOAD_STR                 'deg must be non-negative integer'
               56  CALL_FUNCTION_1       1  ''
               58  RAISE_VARARGS_1       1  'exception instance'
             60_0  COME_FROM            50  '50'

 L.1099        60  LOAD_FAST                'cls'
               62  LOAD_CONST               0
               64  BUILD_LIST_1          1 
               66  LOAD_FAST                'ideg'
               68  BINARY_MULTIPLY  
               70  LOAD_CONST               1
               72  BUILD_LIST_1          1 
               74  BINARY_ADD       
               76  LOAD_FAST                'domain'
               78  LOAD_FAST                'window'
               80  CALL_FUNCTION_3       3  ''
               82  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @classmethod
    def cast--- This code section failed: ---

 L.1137         0  LOAD_FAST                'domain'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L.1138         8  LOAD_FAST                'cls'
               10  LOAD_ATTR                domain
               12  STORE_FAST               'domain'
             14_0  COME_FROM             6  '6'

 L.1139        14  LOAD_FAST                'window'
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_FALSE    28  'to 28'

 L.1140        22  LOAD_FAST                'cls'
               24  LOAD_ATTR                window
               26  STORE_FAST               'window'
             28_0  COME_FROM            20  '20'

 L.1141        28  LOAD_FAST                'series'
               30  LOAD_METHOD              convert
               32  LOAD_FAST                'domain'
               34  LOAD_FAST                'cls'
               36  LOAD_FAST                'window'
               38  CALL_METHOD_3         3  ''
               40  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1