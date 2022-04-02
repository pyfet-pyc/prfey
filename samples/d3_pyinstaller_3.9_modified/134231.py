# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: fractions.py
"""Fraction, infinite-precision, real numbers."""
from decimal import Decimal
import math, numbers, operator, re, sys
__all__ = [
 'Fraction']
_PyHASH_MODULUS = sys.hash_info.modulus
_PyHASH_INF = sys.hash_info.inf
_RATIONAL_FORMAT = re.compile('\n    \\A\\s*                      # optional whitespace at the start, then\n    (?P<sign>[-+]?)            # an optional sign, then\n    (?=\\d|\\.\\d)                # lookahead for digit or .digit\n    (?P<num>\\d*)               # numerator (possibly empty)\n    (?:                        # followed by\n       (?:/(?P<denom>\\d+))?    # an optional denominator\n    |                          # or\n       (?:\\.(?P<decimal>\\d*))? # an optional fractional part\n       (?:E(?P<exp>[-+]?\\d+))? # and optional exponent\n    )\n    \\s*\\Z                      # and optional whitespace to finish\n', re.VERBOSE | re.IGNORECASE)

class Fraction(numbers.Rational):
    __doc__ = "This class implements rational numbers.\n\n    In the two-argument form of the constructor, Fraction(8, 6) will\n    produce a rational number equivalent to 4/3. Both arguments must\n    be Rational. The numerator defaults to 0 and the denominator\n    defaults to 1 so that Fraction(3) == 3 and Fraction() == 0.\n\n    Fractions can also be constructed from:\n\n      - numeric strings similar to those accepted by the\n        float constructor (for example, '-2.3' or '1e10')\n\n      - strings of the form '123/456'\n\n      - float and Decimal instances\n\n      - other Rational instances (including integers)\n\n    "
    __slots__ = ('_numerator', '_denominator')

    def __new__--- This code section failed: ---

 L.  93         0  LOAD_GLOBAL              super
                2  LOAD_GLOBAL              Fraction
                4  LOAD_FAST                'cls'
                6  CALL_FUNCTION_2       2  ''
                8  LOAD_METHOD              __new__
               10  LOAD_FAST                'cls'
               12  CALL_METHOD_1         1  ''
               14  STORE_FAST               'self'

 L.  95        16  LOAD_FAST                'denominator'
               18  LOAD_CONST               None
               20  <117>                 0  ''
            22_24  POP_JUMP_IF_FALSE   356  'to 356'

 L.  96        26  LOAD_GLOBAL              type
               28  LOAD_FAST                'numerator'
               30  CALL_FUNCTION_1       1  ''
               32  LOAD_GLOBAL              int
               34  <117>                 0  ''
               36  POP_JUMP_IF_FALSE    54  'to 54'

 L.  97        38  LOAD_FAST                'numerator'
               40  LOAD_FAST                'self'
               42  STORE_ATTR               _numerator

 L.  98        44  LOAD_CONST               1
               46  LOAD_FAST                'self'
               48  STORE_ATTR               _denominator

 L.  99        50  LOAD_FAST                'self'
               52  RETURN_VALUE     
             54_0  COME_FROM            36  '36'

 L. 101        54  LOAD_GLOBAL              isinstance
               56  LOAD_FAST                'numerator'
               58  LOAD_GLOBAL              numbers
               60  LOAD_ATTR                Rational
               62  CALL_FUNCTION_2       2  ''
               64  POP_JUMP_IF_FALSE    86  'to 86'

 L. 102        66  LOAD_FAST                'numerator'
               68  LOAD_ATTR                numerator
               70  LOAD_FAST                'self'
               72  STORE_ATTR               _numerator

 L. 103        74  LOAD_FAST                'numerator'
               76  LOAD_ATTR                denominator
               78  LOAD_FAST                'self'
               80  STORE_ATTR               _denominator

 L. 104        82  LOAD_FAST                'self'
               84  RETURN_VALUE     
             86_0  COME_FROM            64  '64'

 L. 106        86  LOAD_GLOBAL              isinstance
               88  LOAD_FAST                'numerator'
               90  LOAD_GLOBAL              float
               92  LOAD_GLOBAL              Decimal
               94  BUILD_TUPLE_2         2 
               96  CALL_FUNCTION_2       2  ''
               98  POP_JUMP_IF_FALSE   120  'to 120'

 L. 108       100  LOAD_FAST                'numerator'
              102  LOAD_METHOD              as_integer_ratio
              104  CALL_METHOD_0         0  ''
              106  UNPACK_SEQUENCE_2     2 
              108  LOAD_FAST                'self'
              110  STORE_ATTR               _numerator
              112  LOAD_FAST                'self'
              114  STORE_ATTR               _denominator

 L. 109       116  LOAD_FAST                'self'
              118  RETURN_VALUE     
            120_0  COME_FROM            98  '98'

 L. 111       120  LOAD_GLOBAL              isinstance
              122  LOAD_FAST                'numerator'
              124  LOAD_GLOBAL              str
              126  CALL_FUNCTION_2       2  ''
          128_130  POP_JUMP_IF_FALSE   346  'to 346'

 L. 113       132  LOAD_GLOBAL              _RATIONAL_FORMAT
              134  LOAD_METHOD              match
              136  LOAD_FAST                'numerator'
              138  CALL_METHOD_1         1  ''
              140  STORE_FAST               'm'

 L. 114       142  LOAD_FAST                'm'
              144  LOAD_CONST               None
              146  <117>                 0  ''
              148  POP_JUMP_IF_FALSE   162  'to 162'

 L. 115       150  LOAD_GLOBAL              ValueError
              152  LOAD_STR                 'Invalid literal for Fraction: %r'

 L. 116       154  LOAD_FAST                'numerator'

 L. 115       156  BINARY_MODULO    
              158  CALL_FUNCTION_1       1  ''
              160  RAISE_VARARGS_1       1  'exception instance'
            162_0  COME_FROM           148  '148'

 L. 117       162  LOAD_GLOBAL              int
              164  LOAD_FAST                'm'
              166  LOAD_METHOD              group
              168  LOAD_STR                 'num'
              170  CALL_METHOD_1         1  ''
              172  JUMP_IF_TRUE_OR_POP   176  'to 176'
              174  LOAD_STR                 '0'
            176_0  COME_FROM           172  '172'
              176  CALL_FUNCTION_1       1  ''
              178  STORE_FAST               'numerator'

 L. 118       180  LOAD_FAST                'm'
              182  LOAD_METHOD              group
              184  LOAD_STR                 'denom'
              186  CALL_METHOD_1         1  ''
              188  STORE_FAST               'denom'

 L. 119       190  LOAD_FAST                'denom'
              192  POP_JUMP_IF_FALSE   204  'to 204'

 L. 120       194  LOAD_GLOBAL              int
              196  LOAD_FAST                'denom'
              198  CALL_FUNCTION_1       1  ''
              200  STORE_FAST               'denominator'
              202  JUMP_FORWARD        322  'to 322'
            204_0  COME_FROM           192  '192'

 L. 122       204  LOAD_CONST               1
              206  STORE_FAST               'denominator'

 L. 123       208  LOAD_FAST                'm'
              210  LOAD_METHOD              group
              212  LOAD_STR                 'decimal'
              214  CALL_METHOD_1         1  ''
              216  STORE_FAST               'decimal'

 L. 124       218  LOAD_FAST                'decimal'
          220_222  POP_JUMP_IF_FALSE   260  'to 260'

 L. 125       224  LOAD_CONST               10
              226  LOAD_GLOBAL              len
              228  LOAD_FAST                'decimal'
              230  CALL_FUNCTION_1       1  ''
              232  BINARY_POWER     
              234  STORE_FAST               'scale'

 L. 126       236  LOAD_FAST                'numerator'
              238  LOAD_FAST                'scale'
              240  BINARY_MULTIPLY  
              242  LOAD_GLOBAL              int
              244  LOAD_FAST                'decimal'
              246  CALL_FUNCTION_1       1  ''
              248  BINARY_ADD       
              250  STORE_FAST               'numerator'

 L. 127       252  LOAD_FAST                'denominator'
              254  LOAD_FAST                'scale'
              256  INPLACE_MULTIPLY 
              258  STORE_FAST               'denominator'
            260_0  COME_FROM           220  '220'

 L. 128       260  LOAD_FAST                'm'
              262  LOAD_METHOD              group
              264  LOAD_STR                 'exp'
              266  CALL_METHOD_1         1  ''
              268  STORE_FAST               'exp'

 L. 129       270  LOAD_FAST                'exp'
          272_274  POP_JUMP_IF_FALSE   322  'to 322'

 L. 130       276  LOAD_GLOBAL              int
              278  LOAD_FAST                'exp'
              280  CALL_FUNCTION_1       1  ''
              282  STORE_FAST               'exp'

 L. 131       284  LOAD_FAST                'exp'
              286  LOAD_CONST               0
              288  COMPARE_OP               >=
          290_292  POP_JUMP_IF_FALSE   308  'to 308'

 L. 132       294  LOAD_FAST                'numerator'
              296  LOAD_CONST               10
              298  LOAD_FAST                'exp'
              300  BINARY_POWER     
              302  INPLACE_MULTIPLY 
              304  STORE_FAST               'numerator'
              306  JUMP_FORWARD        322  'to 322'
            308_0  COME_FROM           290  '290'

 L. 134       308  LOAD_FAST                'denominator'
              310  LOAD_CONST               10
              312  LOAD_FAST                'exp'
              314  UNARY_NEGATIVE   
              316  BINARY_POWER     
              318  INPLACE_MULTIPLY 
              320  STORE_FAST               'denominator'
            322_0  COME_FROM           306  '306'
            322_1  COME_FROM           272  '272'
            322_2  COME_FROM           202  '202'

 L. 135       322  LOAD_FAST                'm'
              324  LOAD_METHOD              group
              326  LOAD_STR                 'sign'
              328  CALL_METHOD_1         1  ''
              330  LOAD_STR                 '-'
              332  COMPARE_OP               ==
          334_336  POP_JUMP_IF_FALSE   354  'to 354'

 L. 136       338  LOAD_FAST                'numerator'
              340  UNARY_NEGATIVE   
              342  STORE_FAST               'numerator'
              344  JUMP_FORWARD        354  'to 354'
            346_0  COME_FROM           128  '128'

 L. 139       346  LOAD_GLOBAL              TypeError
              348  LOAD_STR                 'argument should be a string or a Rational instance'
              350  CALL_FUNCTION_1       1  ''
              352  RAISE_VARARGS_1       1  'exception instance'
            354_0  COME_FROM           344  '344'
            354_1  COME_FROM           334  '334'
              354  JUMP_FORWARD        458  'to 458'
            356_0  COME_FROM            22  '22'

 L. 142       356  LOAD_GLOBAL              type
              358  LOAD_FAST                'numerator'
              360  CALL_FUNCTION_1       1  ''
              362  LOAD_GLOBAL              int
              364  DUP_TOP          
              366  ROT_THREE        
              368  <117>                 0  ''
          370_372  POP_JUMP_IF_FALSE   388  'to 388'
              374  LOAD_GLOBAL              type
              376  LOAD_FAST                'denominator'
              378  CALL_FUNCTION_1       1  ''
              380  <117>                 0  ''
          382_384  POP_JUMP_IF_FALSE   394  'to 394'
              386  JUMP_FORWARD        392  'to 392'
            388_0  COME_FROM           370  '370'
              388  POP_TOP          
              390  JUMP_FORWARD        394  'to 394'
            392_0  COME_FROM           386  '386'

 L. 143       392  JUMP_FORWARD        458  'to 458'
            394_0  COME_FROM           390  '390'
            394_1  COME_FROM           382  '382'

 L. 145       394  LOAD_GLOBAL              isinstance
              396  LOAD_FAST                'numerator'
              398  LOAD_GLOBAL              numbers
              400  LOAD_ATTR                Rational
              402  CALL_FUNCTION_2       2  ''
          404_406  POP_JUMP_IF_FALSE   450  'to 450'

 L. 146       408  LOAD_GLOBAL              isinstance
              410  LOAD_FAST                'denominator'
              412  LOAD_GLOBAL              numbers
              414  LOAD_ATTR                Rational
              416  CALL_FUNCTION_2       2  ''

 L. 145   418_420  POP_JUMP_IF_FALSE   450  'to 450'

 L. 148       422  LOAD_FAST                'numerator'
              424  LOAD_ATTR                numerator
              426  LOAD_FAST                'denominator'
              428  LOAD_ATTR                denominator
              430  BINARY_MULTIPLY  

 L. 149       432  LOAD_FAST                'denominator'
              434  LOAD_ATTR                numerator
              436  LOAD_FAST                'numerator'
              438  LOAD_ATTR                denominator
              440  BINARY_MULTIPLY  

 L. 147       442  ROT_TWO          
              444  STORE_FAST               'numerator'
              446  STORE_FAST               'denominator'
              448  JUMP_FORWARD        458  'to 458'
            450_0  COME_FROM           418  '418'
            450_1  COME_FROM           404  '404'

 L. 152       450  LOAD_GLOBAL              TypeError
              452  LOAD_STR                 'both arguments should be Rational instances'
              454  CALL_FUNCTION_1       1  ''
              456  RAISE_VARARGS_1       1  'exception instance'
            458_0  COME_FROM           448  '448'
            458_1  COME_FROM           392  '392'
            458_2  COME_FROM           354  '354'

 L. 155       458  LOAD_FAST                'denominator'
              460  LOAD_CONST               0
              462  COMPARE_OP               ==
          464_466  POP_JUMP_IF_FALSE   480  'to 480'

 L. 156       468  LOAD_GLOBAL              ZeroDivisionError
              470  LOAD_STR                 'Fraction(%s, 0)'
              472  LOAD_FAST                'numerator'
              474  BINARY_MODULO    
              476  CALL_FUNCTION_1       1  ''
              478  RAISE_VARARGS_1       1  'exception instance'
            480_0  COME_FROM           464  '464'

 L. 157       480  LOAD_FAST                '_normalize'
          482_484  POP_JUMP_IF_FALSE   530  'to 530'

 L. 158       486  LOAD_GLOBAL              math
              488  LOAD_METHOD              gcd
              490  LOAD_FAST                'numerator'
              492  LOAD_FAST                'denominator'
              494  CALL_METHOD_2         2  ''
              496  STORE_FAST               'g'

 L. 159       498  LOAD_FAST                'denominator'
              500  LOAD_CONST               0
              502  COMPARE_OP               <
          504_506  POP_JUMP_IF_FALSE   514  'to 514'

 L. 160       508  LOAD_FAST                'g'
              510  UNARY_NEGATIVE   
              512  STORE_FAST               'g'
            514_0  COME_FROM           504  '504'

 L. 161       514  LOAD_FAST                'numerator'
              516  LOAD_FAST                'g'
              518  INPLACE_FLOOR_DIVIDE
              520  STORE_FAST               'numerator'

 L. 162       522  LOAD_FAST                'denominator'
              524  LOAD_FAST                'g'
              526  INPLACE_FLOOR_DIVIDE
              528  STORE_FAST               'denominator'
            530_0  COME_FROM           482  '482'

 L. 163       530  LOAD_FAST                'numerator'
              532  LOAD_FAST                'self'
              534  STORE_ATTR               _numerator

 L. 164       536  LOAD_FAST                'denominator'
              538  LOAD_FAST                'self'
              540  STORE_ATTR               _denominator

 L. 165       542  LOAD_FAST                'self'
              544  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 20

    @classmethod
    def from_float(cls, f):
        """Converts a finite float to a rational number, exactly.

        Beware that Fraction.from_float(0.3) != Fraction(3, 10).

        """
        if isinstance(f, numbers.Integral):
            return cls(f)
        if not isinstance(f, float):
            raise TypeError('%s.from_float() only takes floats, not %r (%s)' % (
             cls.__name__, f, type(f).__name__))
        return cls(*f.as_integer_ratio)

    @classmethod
    def from_decimal(cls, dec):
        """Converts a finite Decimal instance to a rational number, exactly."""
        from decimal import Decimal
        if isinstance(dec, numbers.Integral):
            dec = Decimal(int(dec))
        elif not isinstance(dec, Decimal):
            raise TypeError('%s.from_decimal() only takes Decimals, not %r (%s)' % (
             cls.__name__, dec, type(dec).__name__))
        return cls(*dec.as_integer_ratio)

    def as_integer_ratio(self):
        """Return the integer ratio as a tuple.

        Return a tuple of two integers, whose ratio is equal to the
        Fraction and with a positive denominator.
        """
        return (
         self._numerator, self._denominator)

    def limit_denominator(self, max_denominator=1000000):
        """Closest Fraction to self with denominator at most max_denominator.

        >>> Fraction('3.141592653589793').limit_denominator(10)
        Fraction(22, 7)
        >>> Fraction('3.141592653589793').limit_denominator(100)
        Fraction(311, 99)
        >>> Fraction(4321, 8765).limit_denominator(10000)
        Fraction(4321, 8765)

        """
        if max_denominator < 1:
            raise ValueError('max_denominator should be at least 1')
        if self._denominator <= max_denominator:
            return Fraction(self)
        p0, q0, p1, q1 = (0, 1, 1, 0)
        n, d = self._numerator, self._denominator
        while True:
            a = n // d
            q2 = q0 + a * q1
            if q2 > max_denominator:
                pass
            else:
                p0, q0, p1, q1 = (
                 p1, q1, p0 + a * p1, q2)
                n, d = d, n - a * d

        k = (max_denominator - q0) // q1
        bound1 = Fraction(p0 + k * p1, q0 + k * q1)
        bound2 = Fraction(p1, q1)
        if abs(bound2 - self) <= abs(bound1 - self):
            return bound2
        return bound1

    @property
    def numerator(a):
        return a._numerator

    @property
    def denominator(a):
        return a._denominator

    def __repr__(self):
        """repr(self)"""
        return '%s(%s, %s)' % (self.__class__.__name__,
         self._numerator, self._denominator)

    def __str__(self):
        """str(self)"""
        if self._denominator == 1:
            return str(self._numerator)
        return '%s/%s' % (self._numerator, self._denominator)

    def _operator_fallbacks(monomorphic_operator, fallback_operator):
        """Generates forward and reverse operators given a purely-rational
        operator and a function from the operator module.

        Use this like:
        __op__, __rop__ = _operator_fallbacks(just_rational_op, operator.op)

        In general, we want to implement the arithmetic operations so
        that mixed-mode operations either call an implementation whose
        author knew about the types of both arguments, or convert both
        to the nearest built in type and do the operation there. In
        Fraction, that means that we define __add__ and __radd__ as:

            def __add__(self, other):
                # Both types have numerators/denominator attributes,
                # so do the operation directly
                if isinstance(other, (int, Fraction)):
                    return Fraction(self.numerator * other.denominator +
                                    other.numerator * self.denominator,
                                    self.denominator * other.denominator)
                # float and complex don't have those operations, but we
                # know about those types, so special case them.
                elif isinstance(other, float):
                    return float(self) + other
                elif isinstance(other, complex):
                    return complex(self) + other
                # Let the other type take over.
                return NotImplemented

            def __radd__(self, other):
                # radd handles more types than add because there's
                # nothing left to fall back to.
                if isinstance(other, numbers.Rational):
                    return Fraction(self.numerator * other.denominator +
                                    other.numerator * self.denominator,
                                    self.denominator * other.denominator)
                elif isinstance(other, Real):
                    return float(other) + float(self)
                elif isinstance(other, Complex):
                    return complex(other) + complex(self)
                return NotImplemented

        There are 5 different cases for a mixed-type addition on
        Fraction. I'll refer to all of the above code that doesn't
        refer to Fraction, float, or complex as "boilerplate". 'r'
        will be an instance of Fraction, which is a subtype of
        Rational (r : Fraction <: Rational), and b : B <:
        Complex. The first three involve 'r + b':

            1. If B <: Fraction, int, float, or complex, we handle
               that specially, and all is well.
            2. If Fraction falls back to the boilerplate code, and it
               were to return a value from __add__, we'd miss the
               possibility that B defines a more intelligent __radd__,
               so the boilerplate should return NotImplemented from
               __add__. In particular, we don't handle Rational
               here, even though we could get an exact answer, in case
               the other type wants to do something special.
            3. If B <: Fraction, Python tries B.__radd__ before
               Fraction.__add__. This is ok, because it was
               implemented with knowledge of Fraction, so it can
               handle those instances before delegating to Real or
               Complex.

        The next two situations describe 'b + r'. We assume that b
        didn't know about Fraction in its implementation, and that it
        uses similar boilerplate code:

            4. If B <: Rational, then __radd_ converts both to the
               builtin rational type (hey look, that's us) and
               proceeds.
            5. Otherwise, __radd__ tries to find the nearest common
               base ABC, and fall back to its builtin type. Since this
               class doesn't subclass a concrete type, there's no
               implementation to fall back to, so we need to try as
               hard as possible to return an actual value, or the user
               will get a TypeError.

        """

        def forward(a, b):
            if isinstance(b, (int, Fraction)):
                return monomorphic_operator(a, b)
            if isinstance(b, float):
                return fallback_operator(float(a), b)
            if isinstance(b, complex):
                return fallback_operator(complex(a), b)
            return NotImplemented

        forward.__name__ = '__' + fallback_operator.__name__ + '__'
        forward.__doc__ = monomorphic_operator.__doc__

        def reverse(b, a):
            if isinstance(a, numbers.Rational):
                return monomorphic_operator(a, b)
            if isinstance(a, numbers.Real):
                return fallback_operator(float(a), float(b))
            if isinstance(a, numbers.Complex):
                return fallback_operator(complex(a), complex(b))
            return NotImplemented

        reverse.__name__ = '__r' + fallback_operator.__name__ + '__'
        reverse.__doc__ = monomorphic_operator.__doc__
        return (
         forward, reverse)

    def _add(a, b):
        """a + b"""
        da, db = a.denominator, b.denominator
        return Fraction(a.numerator * db + b.numerator * da, da * db)

    __add__, __radd__ = _operator_fallbacks(_add, operator.add)

    def _sub(a, b):
        """a - b"""
        da, db = a.denominator, b.denominator
        return Fraction(a.numerator * db - b.numerator * da, da * db)

    __sub__, __rsub__ = _operator_fallbacks(_sub, operator.sub)

    def _mul(a, b):
        """a * b"""
        return Fraction(a.numerator * b.numerator, a.denominator * b.denominator)

    __mul__, __rmul__ = _operator_fallbacks(_mul, operator.mul)

    def _div(a, b):
        """a / b"""
        return Fraction(a.numerator * b.denominator, a.denominator * b.numerator)

    __truediv__, __rtruediv__ = _operator_fallbacks(_div, operator.truediv)

    def _floordiv(a, b):
        """a // b"""
        return a.numerator * b.denominator // (a.denominator * b.numerator)

    __floordiv__, __rfloordiv__ = _operator_fallbacks(_floordiv, operator.floordiv)

    def _divmod(a, b):
        """(a // b, a % b)"""
        da, db = a.denominator, b.denominator
        div, n_mod = divmod(a.numerator * db, da * b.numerator)
        return (
         div, Fraction(n_mod, da * db))

    __divmod__, __rdivmod__ = _operator_fallbacks(_divmod, divmod)

    def _mod(a, b):
        """a % b"""
        da, db = a.denominator, b.denominator
        return Fraction(a.numerator * db % (b.numerator * da), da * db)

    __mod__, __rmod__ = _operator_fallbacks(_mod, operator.mod)

    def __pow__(a, b):
        """a ** b

        If b is not an integer, the result will be a float or complex
        since roots are generally irrational. If b is an integer, the
        result will be rational.

        """
        if isinstance(b, numbers.Rational):
            if b.denominator == 1:
                power = b.numerator
                if power >= 0:
                    return Fraction((a._numerator ** power), (a._denominator ** power),
                      _normalize=False)
                if a._numerator >= 0:
                    return Fraction((a._denominator ** (-power)), (a._numerator ** (-power)),
                      _normalize=False)
                return Fraction(((-a._denominator) ** (-power)), ((-a._numerator) ** (-power)),
                  _normalize=False)
            else:
                return float(a) ** float(b)
        else:
            return float(a) ** b

    def __rpow__(b, a):
        """a ** b"""
        if b._denominator == 1:
            if b._numerator >= 0:
                return a ** b._numerator
        if isinstance(a, numbers.Rational):
            return Fraction(a.numerator, a.denominator) ** b
        if b._denominator == 1:
            return a ** b._numerator
        return a ** float(b)

    def __pos__(a):
        """+a: Coerces a subclass instance to Fraction"""
        return Fraction((a._numerator), (a._denominator), _normalize=False)

    def __neg__(a):
        """-a"""
        return Fraction((-a._numerator), (a._denominator), _normalize=False)

    def __abs__(a):
        """abs(a)"""
        return Fraction((abs(a._numerator)), (a._denominator), _normalize=False)

    def __trunc__(a):
        """trunc(a)"""
        if a._numerator < 0:
            return -(-a._numerator // a._denominator)
        return a._numerator // a._denominator

    def __floor__(a):
        """math.floor(a)"""
        return a.numerator // a.denominator

    def __ceil__(a):
        """math.ceil(a)"""
        return -(-a.numerator // a.denominator)

    def __round__--- This code section failed: ---

 L. 510         0  LOAD_FAST                'ndigits'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    90  'to 90'

 L. 511         8  LOAD_GLOBAL              divmod
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                numerator
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                denominator
               18  CALL_FUNCTION_2       2  ''
               20  UNPACK_SEQUENCE_2     2 
               22  STORE_FAST               'floor'
               24  STORE_FAST               'remainder'

 L. 512        26  LOAD_FAST                'remainder'
               28  LOAD_CONST               2
               30  BINARY_MULTIPLY  
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                denominator
               36  COMPARE_OP               <
               38  POP_JUMP_IF_FALSE    44  'to 44'

 L. 513        40  LOAD_FAST                'floor'
               42  RETURN_VALUE     
             44_0  COME_FROM            38  '38'

 L. 514        44  LOAD_FAST                'remainder'
               46  LOAD_CONST               2
               48  BINARY_MULTIPLY  
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                denominator
               54  COMPARE_OP               >
               56  POP_JUMP_IF_FALSE    66  'to 66'

 L. 515        58  LOAD_FAST                'floor'
               60  LOAD_CONST               1
               62  BINARY_ADD       
               64  RETURN_VALUE     
             66_0  COME_FROM            56  '56'

 L. 517        66  LOAD_FAST                'floor'
               68  LOAD_CONST               2
               70  BINARY_MODULO    
               72  LOAD_CONST               0
               74  COMPARE_OP               ==
               76  POP_JUMP_IF_FALSE    82  'to 82'

 L. 518        78  LOAD_FAST                'floor'
               80  RETURN_VALUE     
             82_0  COME_FROM            76  '76'

 L. 520        82  LOAD_FAST                'floor'
               84  LOAD_CONST               1
               86  BINARY_ADD       
               88  RETURN_VALUE     
             90_0  COME_FROM             6  '6'

 L. 521        90  LOAD_CONST               10
               92  LOAD_GLOBAL              abs
               94  LOAD_FAST                'ndigits'
               96  CALL_FUNCTION_1       1  ''
               98  BINARY_POWER     
              100  STORE_FAST               'shift'

 L. 525       102  LOAD_FAST                'ndigits'
              104  LOAD_CONST               0
              106  COMPARE_OP               >
              108  POP_JUMP_IF_FALSE   128  'to 128'

 L. 526       110  LOAD_GLOBAL              Fraction
              112  LOAD_GLOBAL              round
              114  LOAD_FAST                'self'
              116  LOAD_FAST                'shift'
              118  BINARY_MULTIPLY  
              120  CALL_FUNCTION_1       1  ''
              122  LOAD_FAST                'shift'
              124  CALL_FUNCTION_2       2  ''
              126  RETURN_VALUE     
            128_0  COME_FROM           108  '108'

 L. 528       128  LOAD_GLOBAL              Fraction
              130  LOAD_GLOBAL              round
              132  LOAD_FAST                'self'
              134  LOAD_FAST                'shift'
              136  BINARY_TRUE_DIVIDE
              138  CALL_FUNCTION_1       1  ''
              140  LOAD_FAST                'shift'
              142  BINARY_MULTIPLY  
              144  CALL_FUNCTION_1       1  ''
              146  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1

    def __hash__--- This code section failed: ---

 L. 538         0  SETUP_FINALLY        20  'to 20'

 L. 539         2  LOAD_GLOBAL              pow
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                _denominator
                8  LOAD_CONST               -1
               10  LOAD_GLOBAL              _PyHASH_MODULUS
               12  CALL_FUNCTION_3       3  ''
               14  STORE_FAST               'dinv'
               16  POP_BLOCK        
               18  JUMP_FORWARD         42  'to 42'
             20_0  COME_FROM_FINALLY     0  '0'

 L. 540        20  DUP_TOP          
               22  LOAD_GLOBAL              ValueError
               24  <121>                40  ''
               26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 542        32  LOAD_GLOBAL              _PyHASH_INF
               34  STORE_FAST               'hash_'
               36  POP_EXCEPT       
               38  JUMP_FORWARD         64  'to 64'
               40  <48>             
             42_0  COME_FROM            18  '18'

 L. 559        42  LOAD_GLOBAL              hash
               44  LOAD_GLOBAL              hash
               46  LOAD_GLOBAL              abs
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                _numerator
               52  CALL_FUNCTION_1       1  ''
               54  CALL_FUNCTION_1       1  ''
               56  LOAD_FAST                'dinv'
               58  BINARY_MULTIPLY  
               60  CALL_FUNCTION_1       1  ''
               62  STORE_FAST               'hash_'
             64_0  COME_FROM            38  '38'

 L. 560        64  LOAD_FAST                'self'
               66  LOAD_ATTR                _numerator
               68  LOAD_CONST               0
               70  COMPARE_OP               >=
               72  POP_JUMP_IF_FALSE    78  'to 78'
               74  LOAD_FAST                'hash_'
               76  JUMP_FORWARD         82  'to 82'
             78_0  COME_FROM            72  '72'
               78  LOAD_FAST                'hash_'
               80  UNARY_NEGATIVE   
             82_0  COME_FROM            76  '76'
               82  STORE_FAST               'result'

 L. 561        84  LOAD_FAST                'result'
               86  LOAD_CONST               -1
               88  COMPARE_OP               ==
               90  POP_JUMP_IF_FALSE    96  'to 96'
               92  LOAD_CONST               -2
               94  RETURN_VALUE     
             96_0  COME_FROM            90  '90'
               96  LOAD_FAST                'result'
               98  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 24

    def __eq__--- This code section failed: ---

 L. 565         0  LOAD_GLOBAL              type
                2  LOAD_FAST                'b'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_GLOBAL              int
                8  <117>                 0  ''
               10  POP_JUMP_IF_FALSE    32  'to 32'

 L. 566        12  LOAD_FAST                'a'
               14  LOAD_ATTR                _numerator
               16  LOAD_FAST                'b'
               18  COMPARE_OP               ==
               20  JUMP_IF_FALSE_OR_POP    30  'to 30'
               22  LOAD_FAST                'a'
               24  LOAD_ATTR                _denominator
               26  LOAD_CONST               1
               28  COMPARE_OP               ==
             30_0  COME_FROM            20  '20'
               30  RETURN_VALUE     
             32_0  COME_FROM            10  '10'

 L. 567        32  LOAD_GLOBAL              isinstance
               34  LOAD_FAST                'b'
               36  LOAD_GLOBAL              numbers
               38  LOAD_ATTR                Rational
               40  CALL_FUNCTION_2       2  ''
               42  POP_JUMP_IF_FALSE    68  'to 68'

 L. 568        44  LOAD_FAST                'a'
               46  LOAD_ATTR                _numerator
               48  LOAD_FAST                'b'
               50  LOAD_ATTR                numerator
               52  COMPARE_OP               ==
               54  JUMP_IF_FALSE_OR_POP    66  'to 66'

 L. 569        56  LOAD_FAST                'a'
               58  LOAD_ATTR                _denominator
               60  LOAD_FAST                'b'
               62  LOAD_ATTR                denominator
               64  COMPARE_OP               ==
             66_0  COME_FROM            54  '54'

 L. 568        66  RETURN_VALUE     
             68_0  COME_FROM            42  '42'

 L. 570        68  LOAD_GLOBAL              isinstance
               70  LOAD_FAST                'b'
               72  LOAD_GLOBAL              numbers
               74  LOAD_ATTR                Complex
               76  CALL_FUNCTION_2       2  ''
               78  POP_JUMP_IF_FALSE    96  'to 96'
               80  LOAD_FAST                'b'
               82  LOAD_ATTR                imag
               84  LOAD_CONST               0
               86  COMPARE_OP               ==
               88  POP_JUMP_IF_FALSE    96  'to 96'

 L. 571        90  LOAD_FAST                'b'
               92  LOAD_ATTR                real
               94  STORE_FAST               'b'
             96_0  COME_FROM            88  '88'
             96_1  COME_FROM            78  '78'

 L. 572        96  LOAD_GLOBAL              isinstance
               98  LOAD_FAST                'b'
              100  LOAD_GLOBAL              float
              102  CALL_FUNCTION_2       2  ''
              104  POP_JUMP_IF_FALSE   150  'to 150'

 L. 573       106  LOAD_GLOBAL              math
              108  LOAD_METHOD              isnan
              110  LOAD_FAST                'b'
              112  CALL_METHOD_1         1  ''
              114  POP_JUMP_IF_TRUE    126  'to 126'
              116  LOAD_GLOBAL              math
              118  LOAD_METHOD              isinf
              120  LOAD_FAST                'b'
              122  CALL_METHOD_1         1  ''
              124  POP_JUMP_IF_FALSE   134  'to 134'
            126_0  COME_FROM           114  '114'

 L. 576       126  LOAD_CONST               0.0
              128  LOAD_FAST                'b'
              130  COMPARE_OP               ==
              132  RETURN_VALUE     
            134_0  COME_FROM           124  '124'

 L. 578       134  LOAD_FAST                'a'
              136  LOAD_FAST                'a'
              138  LOAD_METHOD              from_float
              140  LOAD_FAST                'b'
              142  CALL_METHOD_1         1  ''
              144  COMPARE_OP               ==
              146  RETURN_VALUE     
              148  JUMP_FORWARD        154  'to 154'
            150_0  COME_FROM           104  '104'

 L. 582       150  LOAD_GLOBAL              NotImplemented
              152  RETURN_VALUE     
            154_0  COME_FROM           148  '148'

Parse error at or near `None' instruction at offset -1

    def _richcmp(self, other, op):
        """Helper for comparison operators, for internal use only.

        Implement comparison between a Rational instance `self`, and
        either another Rational instance or a float `other`.  If
        `other` is not a Rational instance or a float, return
        NotImplemented. `op` should be one of the six standard
        comparison operators.

        """
        if isinstance(other, numbers.Rational):
            return op(self._numerator * other.denominator, self._denominator * other.numerator)
        if isinstance(other, float):
            if math.isnanother or (math.isinfother):
                return op(0.0, other)
            return op(self, self.from_floatother)
        else:
            return NotImplemented

    def __lt__(a, b):
        """a < b"""
        return a._richcmp(b, operator.lt)

    def __gt__(a, b):
        """a > b"""
        return a._richcmp(b, operator.gt)

    def __le__(a, b):
        """a <= b"""
        return a._richcmp(b, operator.le)

    def __ge__(a, b):
        """a >= b"""
        return a._richcmp(b, operator.ge)

    def __bool__(a):
        """a != 0"""
        return bool(a._numerator)

    def __reduce__(self):
        return (
         self.__class__, (str(self),))

    def __copy__(self):
        if type(self) == Fraction:
            return self
        return self.__class__(self._numerator, self._denominator)

    def __deepcopy__(self, memo):
        if type(self) == Fraction:
            return self
        return self.__class__(self._numerator, self._denominator)