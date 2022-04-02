# uncompyle6 version 3.7.4
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
import abc, numbers, numpy as np
from . import polyutils as pu
__all__ = [
 'ABCPolyBase']

class ABCPolyBase(abc.ABC):
    __doc__ = "An abstract base class for immutable series classes.\n\n    ABCPolyBase provides the standard Python numerical methods\n    '+', '-', '*', '//', '%', 'divmod', '**', and '()' along with the\n    methods listed below.\n\n    .. versionadded:: 1.9.0\n\n    Parameters\n    ----------\n    coef : array_like\n        Series coefficients in order of increasing degree, i.e.,\n        ``(1, 2, 3)`` gives ``1*P_0(x) + 2*P_1(x) + 3*P_2(x)``, where\n        ``P_i`` is the basis polynomials of degree ``i``.\n    domain : (2,) array_like, optional\n        Domain to use. The interval ``[domain[0], domain[1]]`` is mapped\n        to the interval ``[window[0], window[1]]`` by shifting and scaling.\n        The default value is the derived class domain.\n    window : (2,) array_like, optional\n        Window, see domain for its use. The default value is the\n        derived class window.\n\n    Attributes\n    ----------\n    coef : (N,) ndarray\n        Series coefficients in order of increasing degree.\n    domain : (2,) ndarray\n        Domain that is mapped to window.\n    window : (2,) ndarray\n        Window that domain is mapped to.\n\n    Class Attributes\n    ----------------\n    maxpower : int\n        Maximum power allowed, i.e., the largest number ``n`` such that\n        ``p(x)**n`` is allowed. This is to limit runaway polynomial size.\n    domain : (2,) ndarray\n        Default domain of the class.\n    window : (2,) ndarray\n        Default window of the class.\n\n    "
    __hash__ = None
    __array_ufunc__ = None
    maxpower = 100

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
    def nickname(self):
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
        else:
            return np.all(self.coef == other.coef) or False
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
            else:
                if not np.all(self.domain == other.domain):
                    raise TypeError('Domains differ')
                else:
                    if not np.all(self.window == other.window):
                        raise TypeError('Windows differ')
            return other.coef
        return other

    def __init__--- This code section failed: ---

 L. 264         0  LOAD_GLOBAL              pu
                2  LOAD_ATTR                as_series
                4  LOAD_FAST                'coef'
                6  BUILD_LIST_1          1 
                8  LOAD_CONST               False
               10  LOAD_CONST               ('trim',)
               12  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               14  UNPACK_SEQUENCE_1     1 
               16  STORE_FAST               'coef'

 L. 265        18  LOAD_FAST                'coef'
               20  LOAD_FAST                'self'
               22  STORE_ATTR               coef

 L. 267        24  LOAD_FAST                'domain'
               26  LOAD_CONST               None
               28  <117>                 1  ''
               30  POP_JUMP_IF_FALSE    76  'to 76'

 L. 268        32  LOAD_GLOBAL              pu
               34  LOAD_ATTR                as_series
               36  LOAD_FAST                'domain'
               38  BUILD_LIST_1          1 
               40  LOAD_CONST               False
               42  LOAD_CONST               ('trim',)
               44  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               46  UNPACK_SEQUENCE_1     1 
               48  STORE_FAST               'domain'

 L. 269        50  LOAD_GLOBAL              len
               52  LOAD_FAST                'domain'
               54  CALL_FUNCTION_1       1  ''
               56  LOAD_CONST               2
               58  COMPARE_OP               !=
               60  POP_JUMP_IF_FALSE    70  'to 70'

 L. 270        62  LOAD_GLOBAL              ValueError
               64  LOAD_STR                 'Domain has wrong number of elements.'
               66  CALL_FUNCTION_1       1  ''
               68  RAISE_VARARGS_1       1  'exception instance'
             70_0  COME_FROM            60  '60'

 L. 271        70  LOAD_FAST                'domain'
               72  LOAD_FAST                'self'
               74  STORE_ATTR               domain
             76_0  COME_FROM            30  '30'

 L. 273        76  LOAD_FAST                'window'
               78  LOAD_CONST               None
               80  <117>                 1  ''
               82  POP_JUMP_IF_FALSE   128  'to 128'

 L. 274        84  LOAD_GLOBAL              pu
               86  LOAD_ATTR                as_series
               88  LOAD_FAST                'window'
               90  BUILD_LIST_1          1 
               92  LOAD_CONST               False
               94  LOAD_CONST               ('trim',)
               96  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               98  UNPACK_SEQUENCE_1     1 
              100  STORE_FAST               'window'

 L. 275       102  LOAD_GLOBAL              len
              104  LOAD_FAST                'window'
              106  CALL_FUNCTION_1       1  ''
              108  LOAD_CONST               2
              110  COMPARE_OP               !=
              112  POP_JUMP_IF_FALSE   122  'to 122'

 L. 276       114  LOAD_GLOBAL              ValueError
              116  LOAD_STR                 'Window has wrong number of elements.'
              118  CALL_FUNCTION_1       1  ''
              120  RAISE_VARARGS_1       1  'exception instance'
            122_0  COME_FROM           112  '112'

 L. 277       122  LOAD_FAST                'window'
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

    def __str__(self):
        coef = str(self.coef)
        name = self.nickname
        return f"{name}({coef})"

    @classmethod
    def _repr_latex_term--- This code section failed: ---

 L. 293         0  LOAD_FAST                'cls'
                2  LOAD_ATTR                basis_name
                4  LOAD_CONST               None
                6  <117>                 0  ''
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 294        10  LOAD_GLOBAL              NotImplementedError

 L. 295        12  LOAD_STR                 'Subclasses must define either a basis name, or override _repr_latex_term(i, arg_str, needs_parens)'

 L. 294        14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 298        18  LOAD_STR                 '{'
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
        off, scale = self.mapparms()
        if off == 0 and scale == 1:
            term = 'x'
            needs_parens = False
        else:
            if scale == 1:
                term = f"{self._repr_latex_scalar(off)} + x"
                needs_parens = True
            else:
                if off == 0:
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
            else:
                if not isinstance(c, numbers.Real):
                    coef_str = f" + ({self._repr_latex_scalar(c)})"
                else:
                    if not np.signbit(c):
                        coef_str = f" + {self._repr_latex_scalar(c)}"
                    else:
                        coef_str = f" - {self._repr_latex_scalar(-c)}"
            term_str = self._repr_latex_term(i, term, needs_parens)
            if term_str == '1':
                part = coef_str
            else:
                part = f"{coef_str}\\,{term_str}"
            if c == 0:
                part = mute(part)
            parts.append(part)
        else:
            if parts:
                body = ''.join(parts)
            else:
                body = '0'
            return f"$x \\mapsto {body}$"

    def __getstate__(self):
        ret = self.__dict__.copy()
        ret['coef'] = self.coef.copy()
        ret['domain'] = self.domain.copy()
        ret['window'] = self.window.copy()
        return ret

    def __setstate__(self, dict):
        self.__dict__ = dict

    def __call__(self, arg):
        off, scl = pu.mapparms(self.domain, self.window)
        arg = off + scl * arg
        return self._val(arg, self.coef)

    def __iter__(self):
        return iter(self.coef)

    def __len__(self):
        return len(self.coef)

    def __neg__(self):
        return self.__class__(-self.coef, self.domain, self.window)

    def __pos__(self):
        return self

    def __add__--- This code section failed: ---

 L. 395         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _get_coefficients
                4  LOAD_FAST                'other'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'othercoef'

 L. 396        10  SETUP_FINALLY        30  'to 30'

 L. 397        12  LOAD_FAST                'self'
               14  LOAD_METHOD              _add
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                coef
               20  LOAD_FAST                'othercoef'
               22  CALL_METHOD_2         2  ''
               24  STORE_FAST               'coef'
               26  POP_BLOCK        
               28  JUMP_FORWARD         52  'to 52'
             30_0  COME_FROM_FINALLY    10  '10'

 L. 398        30  DUP_TOP          
               32  LOAD_GLOBAL              Exception
               34  <121>                50  ''
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 399        42  LOAD_GLOBAL              NotImplemented
               44  ROT_FOUR         
               46  POP_EXCEPT       
               48  RETURN_VALUE     
               50  <48>             
             52_0  COME_FROM            28  '28'

 L. 400        52  LOAD_FAST                'self'
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

 L. 403         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _get_coefficients
                4  LOAD_FAST                'other'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'othercoef'

 L. 404        10  SETUP_FINALLY        30  'to 30'

 L. 405        12  LOAD_FAST                'self'
               14  LOAD_METHOD              _sub
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                coef
               20  LOAD_FAST                'othercoef'
               22  CALL_METHOD_2         2  ''
               24  STORE_FAST               'coef'
               26  POP_BLOCK        
               28  JUMP_FORWARD         52  'to 52'
             30_0  COME_FROM_FINALLY    10  '10'

 L. 406        30  DUP_TOP          
               32  LOAD_GLOBAL              Exception
               34  <121>                50  ''
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 407        42  LOAD_GLOBAL              NotImplemented
               44  ROT_FOUR         
               46  POP_EXCEPT       
               48  RETURN_VALUE     
               50  <48>             
             52_0  COME_FROM            28  '28'

 L. 408        52  LOAD_FAST                'self'
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

 L. 411         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _get_coefficients
                4  LOAD_FAST                'other'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'othercoef'

 L. 412        10  SETUP_FINALLY        30  'to 30'

 L. 413        12  LOAD_FAST                'self'
               14  LOAD_METHOD              _mul
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                coef
               20  LOAD_FAST                'othercoef'
               22  CALL_METHOD_2         2  ''
               24  STORE_FAST               'coef'
               26  POP_BLOCK        
               28  JUMP_FORWARD         52  'to 52'
             30_0  COME_FROM_FINALLY    10  '10'

 L. 414        30  DUP_TOP          
               32  LOAD_GLOBAL              Exception
               34  <121>                50  ''
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 415        42  LOAD_GLOBAL              NotImplemented
               44  ROT_FOUR         
               46  POP_EXCEPT       
               48  RETURN_VALUE     
               50  <48>             
             52_0  COME_FROM            28  '28'

 L. 416        52  LOAD_FAST                'self'
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

 L. 430         0  LOAD_FAST                'self'
                2  LOAD_METHOD              __divmod__
                4  LOAD_FAST                'other'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'res'

 L. 431        10  LOAD_FAST                'res'
               12  LOAD_GLOBAL              NotImplemented
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    22  'to 22'

 L. 432        18  LOAD_FAST                'res'
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L. 433        22  LOAD_FAST                'res'
               24  LOAD_CONST               0
               26  BINARY_SUBSCR    
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 14

    def __mod__--- This code section failed: ---

 L. 436         0  LOAD_FAST                'self'
                2  LOAD_METHOD              __divmod__
                4  LOAD_FAST                'other'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'res'

 L. 437        10  LOAD_FAST                'res'
               12  LOAD_GLOBAL              NotImplemented
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    22  'to 22'

 L. 438        18  LOAD_FAST                'res'
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L. 439        22  LOAD_FAST                'res'
               24  LOAD_CONST               1
               26  BINARY_SUBSCR    
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 14

    def __divmod__--- This code section failed: ---

 L. 442         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _get_coefficients
                4  LOAD_FAST                'other'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'othercoef'

 L. 443        10  SETUP_FINALLY        34  'to 34'

 L. 444        12  LOAD_FAST                'self'
               14  LOAD_METHOD              _div
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                coef
               20  LOAD_FAST                'othercoef'
               22  CALL_METHOD_2         2  ''
               24  UNPACK_SEQUENCE_2     2 
               26  STORE_FAST               'quo'
               28  STORE_FAST               'rem'
               30  POP_BLOCK        
               32  JUMP_FORWARD         94  'to 94'
             34_0  COME_FROM_FINALLY    10  '10'

 L. 445        34  DUP_TOP          
               36  LOAD_GLOBAL              ZeroDivisionError
               38  <121>                72  ''
               40  POP_TOP          
               42  STORE_FAST               'e'
               44  POP_TOP          
               46  SETUP_FINALLY        64  'to 64'

 L. 446        48  LOAD_FAST                'e'
               50  RAISE_VARARGS_1       1  'exception instance'
               52  POP_BLOCK        
               54  POP_EXCEPT       
               56  LOAD_CONST               None
               58  STORE_FAST               'e'
               60  DELETE_FAST              'e'
               62  JUMP_FORWARD         94  'to 94'
             64_0  COME_FROM_FINALLY    46  '46'
               64  LOAD_CONST               None
               66  STORE_FAST               'e'
               68  DELETE_FAST              'e'
               70  <48>             

 L. 447        72  DUP_TOP          
               74  LOAD_GLOBAL              Exception
               76  <121>                92  ''
               78  POP_TOP          
               80  POP_TOP          
               82  POP_TOP          

 L. 448        84  LOAD_GLOBAL              NotImplemented
               86  ROT_FOUR         
               88  POP_EXCEPT       
               90  RETURN_VALUE     
               92  <48>             
             94_0  COME_FROM            62  '62'
             94_1  COME_FROM            32  '32'

 L. 449        94  LOAD_FAST                'self'
               96  LOAD_METHOD              __class__
               98  LOAD_FAST                'quo'
              100  LOAD_FAST                'self'
              102  LOAD_ATTR                domain
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                window
              108  CALL_METHOD_3         3  ''
              110  STORE_FAST               'quo'

 L. 450       112  LOAD_FAST                'self'
              114  LOAD_METHOD              __class__
              116  LOAD_FAST                'rem'
              118  LOAD_FAST                'self'
              120  LOAD_ATTR                domain
              122  LOAD_FAST                'self'
              124  LOAD_ATTR                window
              126  CALL_METHOD_3         3  ''
              128  STORE_FAST               'rem'

 L. 451       130  LOAD_FAST                'quo'
              132  LOAD_FAST                'rem'
              134  BUILD_TUPLE_2         2 
              136  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 38

    def __pow__(self, other):
        coef = self._pow((self.coef), other, maxpower=(self.maxpower))
        res = self.__class__(coef, self.domain, self.window)
        return res

    def __radd__--- This code section failed: ---

 L. 459         0  SETUP_FINALLY        20  'to 20'

 L. 460         2  LOAD_FAST                'self'
                4  LOAD_METHOD              _add
                6  LOAD_FAST                'other'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                coef
               12  CALL_METHOD_2         2  ''
               14  STORE_FAST               'coef'
               16  POP_BLOCK        
               18  JUMP_FORWARD         42  'to 42'
             20_0  COME_FROM_FINALLY     0  '0'

 L. 461        20  DUP_TOP          
               22  LOAD_GLOBAL              Exception
               24  <121>                40  ''
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 462        32  LOAD_GLOBAL              NotImplemented
               34  ROT_FOUR         
               36  POP_EXCEPT       
               38  RETURN_VALUE     
               40  <48>             
             42_0  COME_FROM            18  '18'

 L. 463        42  LOAD_FAST                'self'
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

 L. 466         0  SETUP_FINALLY        20  'to 20'

 L. 467         2  LOAD_FAST                'self'
                4  LOAD_METHOD              _sub
                6  LOAD_FAST                'other'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                coef
               12  CALL_METHOD_2         2  ''
               14  STORE_FAST               'coef'
               16  POP_BLOCK        
               18  JUMP_FORWARD         42  'to 42'
             20_0  COME_FROM_FINALLY     0  '0'

 L. 468        20  DUP_TOP          
               22  LOAD_GLOBAL              Exception
               24  <121>                40  ''
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 469        32  LOAD_GLOBAL              NotImplemented
               34  ROT_FOUR         
               36  POP_EXCEPT       
               38  RETURN_VALUE     
               40  <48>             
             42_0  COME_FROM            18  '18'

 L. 470        42  LOAD_FAST                'self'
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

 L. 473         0  SETUP_FINALLY        20  'to 20'

 L. 474         2  LOAD_FAST                'self'
                4  LOAD_METHOD              _mul
                6  LOAD_FAST                'other'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                coef
               12  CALL_METHOD_2         2  ''
               14  STORE_FAST               'coef'
               16  POP_BLOCK        
               18  JUMP_FORWARD         42  'to 42'
             20_0  COME_FROM_FINALLY     0  '0'

 L. 475        20  DUP_TOP          
               22  LOAD_GLOBAL              Exception
               24  <121>                40  ''
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 476        32  LOAD_GLOBAL              NotImplemented
               34  ROT_FOUR         
               36  POP_EXCEPT       
               38  RETURN_VALUE     
               40  <48>             
             42_0  COME_FROM            18  '18'

 L. 477        42  LOAD_FAST                'self'
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

 L. 489         0  LOAD_FAST                'self'
                2  LOAD_METHOD              __rdivmod__
                4  LOAD_FAST                'other'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'res'

 L. 490        10  LOAD_FAST                'res'
               12  LOAD_GLOBAL              NotImplemented
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    22  'to 22'

 L. 491        18  LOAD_FAST                'res'
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L. 492        22  LOAD_FAST                'res'
               24  LOAD_CONST               0
               26  BINARY_SUBSCR    
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 14

    def __rmod__--- This code section failed: ---

 L. 495         0  LOAD_FAST                'self'
                2  LOAD_METHOD              __rdivmod__
                4  LOAD_FAST                'other'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'res'

 L. 496        10  LOAD_FAST                'res'
               12  LOAD_GLOBAL              NotImplemented
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    22  'to 22'

 L. 497        18  LOAD_FAST                'res'
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L. 498        22  LOAD_FAST                'res'
               24  LOAD_CONST               1
               26  BINARY_SUBSCR    
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 14

    def __rdivmod__--- This code section failed: ---

 L. 501         0  SETUP_FINALLY        24  'to 24'

 L. 502         2  LOAD_FAST                'self'
                4  LOAD_METHOD              _div
                6  LOAD_FAST                'other'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                coef
               12  CALL_METHOD_2         2  ''
               14  UNPACK_SEQUENCE_2     2 
               16  STORE_FAST               'quo'
               18  STORE_FAST               'rem'
               20  POP_BLOCK        
               22  JUMP_FORWARD         84  'to 84'
             24_0  COME_FROM_FINALLY     0  '0'

 L. 503        24  DUP_TOP          
               26  LOAD_GLOBAL              ZeroDivisionError
               28  <121>                62  ''
               30  POP_TOP          
               32  STORE_FAST               'e'
               34  POP_TOP          
               36  SETUP_FINALLY        54  'to 54'

 L. 504        38  LOAD_FAST                'e'
               40  RAISE_VARARGS_1       1  'exception instance'
               42  POP_BLOCK        
               44  POP_EXCEPT       
               46  LOAD_CONST               None
               48  STORE_FAST               'e'
               50  DELETE_FAST              'e'
               52  JUMP_FORWARD         84  'to 84'
             54_0  COME_FROM_FINALLY    36  '36'
               54  LOAD_CONST               None
               56  STORE_FAST               'e'
               58  DELETE_FAST              'e'
               60  <48>             

 L. 505        62  DUP_TOP          
               64  LOAD_GLOBAL              Exception
               66  <121>                82  ''
               68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          

 L. 506        74  LOAD_GLOBAL              NotImplemented
               76  ROT_FOUR         
               78  POP_EXCEPT       
               80  RETURN_VALUE     
               82  <48>             
             84_0  COME_FROM            52  '52'
             84_1  COME_FROM            22  '22'

 L. 507        84  LOAD_FAST                'self'
               86  LOAD_METHOD              __class__
               88  LOAD_FAST                'quo'
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                domain
               94  LOAD_FAST                'self'
               96  LOAD_ATTR                window
               98  CALL_METHOD_3         3  ''
              100  STORE_FAST               'quo'

 L. 508       102  LOAD_FAST                'self'
              104  LOAD_METHOD              __class__
              106  LOAD_FAST                'rem'
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                domain
              112  LOAD_FAST                'self'
              114  LOAD_ATTR                window
              116  CALL_METHOD_3         3  ''
              118  STORE_FAST               'rem'

 L. 509       120  LOAD_FAST                'quo'
              122  LOAD_FAST                'rem'
              124  BUILD_TUPLE_2         2 
              126  RETURN_VALUE     
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
        return self.__class__(self.coef, self.domain, self.window)

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
            Contains the new set of coefficients.

        """
        coef = pu.trimcoef(self.coef, tol)
        return self.__class__(coef, self.domain, self.window)

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
        if isize != size or isize < 1:
            raise ValueError('size must be a positive integer')
        elif isize >= len(self.coef):
            coef = self.coef
        else:
            coef = self.coef[:isize]
        return self.__class__(coef, self.domain, self.window)

    def convert--- This code section failed: ---

 L. 659         0  LOAD_FAST                'kind'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 660         8  LOAD_FAST                'self'
               10  LOAD_ATTR                __class__
               12  STORE_FAST               'kind'
             14_0  COME_FROM             6  '6'

 L. 661        14  LOAD_FAST                'domain'
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_FALSE    28  'to 28'

 L. 662        22  LOAD_FAST                'kind'
               24  LOAD_ATTR                domain
               26  STORE_FAST               'domain'
             28_0  COME_FROM            20  '20'

 L. 663        28  LOAD_FAST                'window'
               30  LOAD_CONST               None
               32  <117>                 0  ''
               34  POP_JUMP_IF_FALSE    42  'to 42'

 L. 664        36  LOAD_FAST                'kind'
               38  LOAD_ATTR                window
               40  STORE_FAST               'window'
             42_0  COME_FROM            34  '34'

 L. 665        42  LOAD_FAST                'self'
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
        return pu.mapparms(self.domain, self.window)

    def integ--- This code section failed: ---

 L. 721         0  LOAD_FAST                'self'
                2  LOAD_METHOD              mapparms
                4  CALL_METHOD_0         0  ''
                6  UNPACK_SEQUENCE_2     2 
                8  STORE_FAST               'off'
               10  STORE_FAST               'scl'

 L. 722        12  LOAD_FAST                'lbnd'
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    26  'to 26'

 L. 723        20  LOAD_CONST               0
               22  STORE_FAST               'lbnd'
               24  JUMP_FORWARD         38  'to 38'
             26_0  COME_FROM            18  '18'

 L. 725        26  LOAD_FAST                'off'
               28  LOAD_FAST                'scl'
               30  LOAD_FAST                'lbnd'
               32  BINARY_MULTIPLY  
               34  BINARY_ADD       
               36  STORE_FAST               'lbnd'
             38_0  COME_FROM            24  '24'

 L. 726        38  LOAD_FAST                'self'
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

 L. 727        62  LOAD_FAST                'self'
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
        off, scl = self.mapparms()
        coef = self._der(self.coef, m, scl)
        return self.__class__(coef, self.domain, self.window)

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
        return pu.mapdomain(roots, self.window, self.domain)

    def linspace--- This code section failed: ---

 L. 792         0  LOAD_FAST                'domain'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 793         8  LOAD_FAST                'self'
               10  LOAD_ATTR                domain
               12  STORE_FAST               'domain'
             14_0  COME_FROM             6  '6'

 L. 794        14  LOAD_GLOBAL              np
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

 L. 795        36  LOAD_FAST                'self'
               38  LOAD_FAST                'x'
               40  CALL_FUNCTION_1       1  ''
               42  STORE_FAST               'y'

 L. 796        44  LOAD_FAST                'x'
               46  LOAD_FAST                'y'
               48  BUILD_TUPLE_2         2 
               50  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @classmethod
    def fit--- This code section failed: ---

 L. 871         0  LOAD_FAST                'domain'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    20  'to 20'

 L. 872         8  LOAD_GLOBAL              pu
               10  LOAD_METHOD              getdomain
               12  LOAD_FAST                'x'
               14  CALL_METHOD_1         1  ''
               16  STORE_FAST               'domain'
               18  JUMP_FORWARD         50  'to 50'
             20_0  COME_FROM             6  '6'

 L. 873        20  LOAD_GLOBAL              type
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

 L. 874        44  LOAD_FAST                'cls'
               46  LOAD_ATTR                domain
               48  STORE_FAST               'domain'
             50_0  COME_FROM            42  '42'
             50_1  COME_FROM            30  '30'
             50_2  COME_FROM            18  '18'

 L. 876        50  LOAD_FAST                'window'
               52  LOAD_CONST               None
               54  <117>                 0  ''
               56  POP_JUMP_IF_FALSE    64  'to 64'

 L. 877        58  LOAD_FAST                'cls'
               60  LOAD_ATTR                window
               62  STORE_FAST               'window'
             64_0  COME_FROM            56  '56'

 L. 879        64  LOAD_GLOBAL              pu
               66  LOAD_METHOD              mapdomain
               68  LOAD_FAST                'x'
               70  LOAD_FAST                'domain'
               72  LOAD_FAST                'window'
               74  CALL_METHOD_3         3  ''
               76  STORE_FAST               'xnew'

 L. 880        78  LOAD_FAST                'cls'
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

 L. 881       100  LOAD_FAST                'full'
              102  POP_JUMP_IF_FALSE   130  'to 130'

 L. 882       104  LOAD_FAST                'res'
              106  UNPACK_SEQUENCE_2     2 
              108  STORE_FAST               'coef'
              110  STORE_FAST               'status'

 L. 883       112  LOAD_FAST                'cls'
              114  LOAD_FAST                'coef'
              116  LOAD_FAST                'domain'
              118  LOAD_FAST                'window'
              120  LOAD_CONST               ('domain', 'window')
              122  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              124  LOAD_FAST                'status'
              126  BUILD_TUPLE_2         2 
              128  RETURN_VALUE     
            130_0  COME_FROM           102  '102'

 L. 885       130  LOAD_FAST                'res'
              132  STORE_FAST               'coef'

 L. 886       134  LOAD_FAST                'cls'
              136  LOAD_FAST                'coef'
              138  LOAD_FAST                'domain'
              140  LOAD_FAST                'window'
              142  LOAD_CONST               ('domain', 'window')
              144  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              146  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1

    @classmethod
    def fromroots--- This code section failed: ---

 L. 914         0  LOAD_GLOBAL              pu
                2  LOAD_ATTR                as_series
                4  LOAD_FAST                'roots'
                6  BUILD_LIST_1          1 
                8  LOAD_CONST               False
               10  LOAD_CONST               ('trim',)
               12  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               14  UNPACK_SEQUENCE_1     1 
               16  STORE_FAST               'roots'

 L. 915        18  LOAD_FAST                'domain'
               20  LOAD_CONST               None
               22  <117>                 0  ''
               24  POP_JUMP_IF_FALSE    38  'to 38'

 L. 916        26  LOAD_GLOBAL              pu
               28  LOAD_METHOD              getdomain
               30  LOAD_FAST                'roots'
               32  CALL_METHOD_1         1  ''
               34  STORE_FAST               'domain'
               36  JUMP_FORWARD         68  'to 68'
             38_0  COME_FROM            24  '24'

 L. 917        38  LOAD_GLOBAL              type
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

 L. 918        62  LOAD_FAST                'cls'
               64  LOAD_ATTR                domain
               66  STORE_FAST               'domain'
             68_0  COME_FROM            60  '60'
             68_1  COME_FROM            48  '48'
             68_2  COME_FROM            36  '36'

 L. 920        68  LOAD_FAST                'window'
               70  LOAD_CONST               None
               72  <117>                 0  ''
               74  POP_JUMP_IF_FALSE    82  'to 82'

 L. 921        76  LOAD_FAST                'cls'
               78  LOAD_ATTR                window
               80  STORE_FAST               'window'
             82_0  COME_FROM            74  '74'

 L. 923        82  LOAD_GLOBAL              len
               84  LOAD_FAST                'roots'
               86  CALL_FUNCTION_1       1  ''
               88  STORE_FAST               'deg'

 L. 924        90  LOAD_GLOBAL              pu
               92  LOAD_METHOD              mapparms
               94  LOAD_FAST                'domain'
               96  LOAD_FAST                'window'
               98  CALL_METHOD_2         2  ''
              100  UNPACK_SEQUENCE_2     2 
              102  STORE_FAST               'off'
              104  STORE_FAST               'scl'

 L. 925       106  LOAD_FAST                'off'
              108  LOAD_FAST                'scl'
              110  LOAD_FAST                'roots'
              112  BINARY_MULTIPLY  
              114  BINARY_ADD       
              116  STORE_FAST               'rnew'

 L. 926       118  LOAD_FAST                'cls'
              120  LOAD_METHOD              _fromroots
              122  LOAD_FAST                'rnew'
              124  CALL_METHOD_1         1  ''
              126  LOAD_FAST                'scl'
              128  LOAD_FAST                'deg'
              130  BINARY_POWER     
              132  BINARY_TRUE_DIVIDE
              134  STORE_FAST               'coef'

 L. 927       136  LOAD_FAST                'cls'
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

 L. 954         0  LOAD_FAST                'domain'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 955         8  LOAD_FAST                'cls'
               10  LOAD_ATTR                domain
               12  STORE_FAST               'domain'
             14_0  COME_FROM             6  '6'

 L. 956        14  LOAD_FAST                'window'
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_FALSE    28  'to 28'

 L. 957        22  LOAD_FAST                'cls'
               24  LOAD_ATTR                window
               26  STORE_FAST               'window'
             28_0  COME_FROM            20  '20'

 L. 958        28  LOAD_GLOBAL              pu
               30  LOAD_METHOD              mapparms
               32  LOAD_FAST                'window'
               34  LOAD_FAST                'domain'
               36  CALL_METHOD_2         2  ''
               38  UNPACK_SEQUENCE_2     2 
               40  STORE_FAST               'off'
               42  STORE_FAST               'scl'

 L. 959        44  LOAD_FAST                'cls'
               46  LOAD_METHOD              _line
               48  LOAD_FAST                'off'
               50  LOAD_FAST                'scl'
               52  CALL_METHOD_2         2  ''
               54  STORE_FAST               'coef'

 L. 960        56  LOAD_FAST                'cls'
               58  LOAD_FAST                'coef'
               60  LOAD_FAST                'domain'
               62  LOAD_FAST                'window'
               64  CALL_FUNCTION_3       3  ''
               66  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @classmethod
    def basis--- This code section failed: ---

 L. 991         0  LOAD_FAST                'domain'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L. 992         8  LOAD_FAST                'cls'
               10  LOAD_ATTR                domain
               12  STORE_FAST               'domain'
             14_0  COME_FROM             6  '6'

 L. 993        14  LOAD_FAST                'window'
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_FALSE    28  'to 28'

 L. 994        22  LOAD_FAST                'cls'
               24  LOAD_ATTR                window
               26  STORE_FAST               'window'
             28_0  COME_FROM            20  '20'

 L. 995        28  LOAD_GLOBAL              int
               30  LOAD_FAST                'deg'
               32  CALL_FUNCTION_1       1  ''
               34  STORE_FAST               'ideg'

 L. 997        36  LOAD_FAST                'ideg'
               38  LOAD_FAST                'deg'
               40  COMPARE_OP               !=
               42  POP_JUMP_IF_TRUE     52  'to 52'
               44  LOAD_FAST                'ideg'
               46  LOAD_CONST               0
               48  COMPARE_OP               <
               50  POP_JUMP_IF_FALSE    60  'to 60'
             52_0  COME_FROM            42  '42'

 L. 998        52  LOAD_GLOBAL              ValueError
               54  LOAD_STR                 'deg must be non-negative integer'
               56  CALL_FUNCTION_1       1  ''
               58  RAISE_VARARGS_1       1  'exception instance'
             60_0  COME_FROM            50  '50'

 L. 999        60  LOAD_FAST                'cls'
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

 L.1037         0  LOAD_FAST                'domain'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L.1038         8  LOAD_FAST                'cls'
               10  LOAD_ATTR                domain
               12  STORE_FAST               'domain'
             14_0  COME_FROM             6  '6'

 L.1039        14  LOAD_FAST                'window'
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_FALSE    28  'to 28'

 L.1040        22  LOAD_FAST                'cls'
               24  LOAD_ATTR                window
               26  STORE_FAST               'window'
             28_0  COME_FROM            20  '20'

 L.1041        28  LOAD_FAST                'series'
               30  LOAD_METHOD              convert
               32  LOAD_FAST                'domain'
               34  LOAD_FAST                'cls'
               36  LOAD_FAST                'window'
               38  CALL_METHOD_3         3  ''
               40  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1