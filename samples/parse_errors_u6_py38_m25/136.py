# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: random.py
"""Random variable generators.

    integers
    --------
           uniform within range

    sequences
    ---------
           pick random element
           pick random sample
           pick weighted random sample
           generate random permutation

    distributions on the real line:
    ------------------------------
           uniform
           triangular
           normal (Gaussian)
           lognormal
           negative exponential
           gamma
           beta
           pareto
           Weibull

    distributions on the circle (angles 0 to 2pi)
    ---------------------------------------------
           circular uniform
           von Mises

General notes on the underlying Mersenne Twister core generator:

* The period is 2**19937-1.
* It is one of the most extensively tested generators in existence.
* The random() method is implemented in C, executes in a single Python step,
  and is, therefore, threadsafe.

"""
from warnings import warn as _warn
from math import log as _log, exp as _exp, pi as _pi, e as _e, ceil as _ceil
from math import sqrt as _sqrt, acos as _acos, cos as _cos, sin as _sin
from os import urandom as _urandom
from _collections_abc import Set as _Set, Sequence as _Sequence
from itertools import accumulate as _accumulate, repeat as _repeat
from bisect import bisect as _bisect
import os as _os
try:
    from _sha512 import sha512 as _sha512
except ImportError:
    from hashlib import sha512 as _sha512
else:
    __all__ = [
     'Random', 'seed', 'random', 'uniform', 'randint', 'choice', 'sample',
     'randrange', 'shuffle', 'normalvariate', 'lognormvariate',
     'expovariate', 'vonmisesvariate', 'gammavariate', 'triangular',
     'gauss', 'betavariate', 'paretovariate', 'weibullvariate',
     'getstate', 'setstate', 'getrandbits', 'choices',
     'SystemRandom']
    NV_MAGICCONST = 4 * _exp(-0.5) / _sqrt(2.0)
    TWOPI = 2.0 * _pi
    LOG4 = _log(4.0)
    SG_MAGICCONST = 1.0 + _log(4.5)
    BPF = 53
    RECIP_BPF = 2 ** (-BPF)
    import _random

    class Random(_random.Random):
        __doc__ = "Random number generator base class used by bound module functions.\n\n    Used to instantiate instances of Random to get generators that don't\n    share state.\n\n    Class Random can also be subclassed if you want to use a different basic\n    generator of your own devising: in that case, override the following\n    methods:  random(), seed(), getstate(), and setstate().\n    Optionally, implement a getrandbits() method so that randrange()\n    can cover arbitrarily large ranges.\n\n    "
        VERSION = 3

        def __init__(self, x=None):
            """Initialize an instance.

        Optional argument x controls seeding, as for Random.seed().
        """
            self.seed(x)
            self.gauss_next = None

        def __init_subclass__(cls, **kwargs):
            """Control how subclasses generate random integers.

        The algorithm a subclass can use depends on the random() and/or
        getrandbits() implementation available to it and determines
        whether it can generate random integers from arbitrarily large
        ranges.
        """
            for c in cls.__mro__:
                if '_randbelow' in c.__dict__:
                    break
                if 'getrandbits' in c.__dict__:
                    cls._randbelow = cls._randbelow_with_getrandbits
                    break
                if 'random' in c.__dict__:
                    cls._randbelow = cls._randbelow_without_getrandbits
                    break

        def seed(self, a=None, version=2):
            """Initialize internal state from hashable object.

        None or no argument seeds from current time or from an operating
        system specific randomness source if available.

        If *a* is an int, all bits are used.

        For version 2 (the default), all of the bits are used if *a* is a str,
        bytes, or bytearray.  For version 1 (provided for reproducing random
        sequences from older versions of Python), the algorithm for str and
        bytes generates a narrower range of seeds.

        """
            if version == 1:
                if isinstance(a, (str, bytes)):
                    a = a.decode('latin-1') if isinstance(a, bytes) else a
                    x = ord(a[0]) << 7 if a else 0
                    for c in map(ord, a):
                        x = (1000003 * x ^ c) & 18446744073709551615
                    else:
                        x ^= len(a)
                        a = -2 if x == -1 else x

            elif version == 2 and isinstance(a, (str, bytes, bytearray)):
                if isinstance(a, str):
                    a = a.encode()
                a += _sha512(a).digest()
                a = int.from_bytes(a, 'big')
            super().seed(a)
            self.gauss_next = None

        def getstate(self):
            return (
             self.VERSION, super().getstate(), self.gauss_next)

        def setstate(self, state):
            version = state[0]
            if version == 3:
                version, internalstate, self.gauss_next = state
                super().setstate(internalstate)
            else:
                if version == 2:
                    version, internalstate, self.gauss_next = state
                    try:
                        internalstate = tuple((x % 4294967296 for x in internalstate))
                    except ValueError as e:
                        try:
                            raise TypeError from e
                        finally:
                            e = None
                            del e

                    else:
                        super().setstate(internalstate)
                else:
                    raise ValueError('state with version %s passed to Random.setstate() of version %s' % (
                     version, self.VERSION))

        def __getstate__(self):
            return self.getstate()

        def __setstate__(self, state):
            self.setstate(state)

        def __reduce__(self):
            return (
             self.__class__, (), self.getstate())

        def randrange(self, start, stop=None, step=1, _int=int):
            """Choose a random item from range(start, stop[, step]).

        This fixes the problem with randint() which includes the
        endpoint; in Python this is usually not what you want.

        """
            istart = _int(start)
            if istart != start:
                raise ValueError('non-integer arg 1 for randrange()')
            if stop is None:
                if istart > 0:
                    return self._randbelow(istart)
                raise ValueError('empty range for randrange()')
            istop = _int(stop)
            if istop != stop:
                raise ValueError('non-integer stop for randrange()')
            else:
                width = istop - istart
                if step == 1:
                    if width > 0:
                        return istart + self._randbelow(width)
                else:
                    if step == 1:
                        raise ValueError('empty range for randrange() (%d, %d, %d)' % (istart, istop, width))
                    istep = _int(step)
                    if istep != step:
                        raise ValueError('non-integer step for randrange()')
                    if istep > 0:
                        n = (width + istep - 1) // istep
                    else:
                        if istep < 0:
                            n = (width + istep + 1) // istep
                        else:
                            raise ValueError('zero step for randrange()')
            if n <= 0:
                raise ValueError('empty range for randrange()')
            return istart + istep * self._randbelow(n)

        def randint(self, a, b):
            """Return random integer in range [a, b], including both end points.
        """
            return self.randrange(a, b + 1)

        def _randbelow_with_getrandbits(self, n):
            """Return a random int in the range [0,n).  Raises ValueError if n==0."""
            getrandbits = self.getrandbits
            k = n.bit_length()
            r = getrandbits(k)
            while r >= n:
                r = getrandbits(k)

            return r

        def _randbelow_without_getrandbits(self, n, int=int, maxsize=1 << BPF):
            """Return a random int in the range [0,n).  Raises ValueError if n==0.

        The implementation does not use getrandbits, but only random.
        """
            random = self.random
            if n >= maxsize:
                _warn('Underlying random() generator does not supply \nenough bits to choose from a population range this large.\nTo remove the range limitation, add a getrandbits() method.')
                return int(random() * n)
            else:
                if n == 0:
                    raise ValueError('Boundary cannot be zero')
                rem = maxsize % n
                limit = (maxsize - rem) / maxsize
                r = random()
                while True:
                    if r >= limit:
                        r = random()

            return int(r * maxsize) % n

        _randbelow = _randbelow_with_getrandbits

        def choice(self, seq):
            """Choose a random element from a non-empty sequence."""
            try:
                i = self._randbelow(len(seq))
            except ValueError:
                raise IndexError('Cannot choose from an empty sequence') from None
            else:
                return seq[i]

        def shuffle(self, x, random=None):
            """Shuffle list x in place, and return None.

        Optional argument random is a 0-argument function returning a
        random float in [0.0, 1.0); if it is the default None, the
        standard random.random will be used.

        """
            if random is None:
                randbelow = self._randbelow
                for i in reversed(range(1, len(x))):
                    j = randbelow(i + 1)
                    x[i], x[j] = x[j], x[i]

            else:
                _int = int
                for i in reversed(range(1, len(x))):
                    j = _int(random() * (i + 1))
                    x[i], x[j] = x[j], x[i]

        def sample(self, population, k):
            """Chooses k unique random elements from a population sequence or set.

        Returns a new list containing elements from the population while
        leaving the original population unchanged.  The resulting list is
        in selection order so that all sub-slices will also be valid random
        samples.  This allows raffle winners (the sample) to be partitioned
        into grand prize and second place winners (the subslices).

        Members of the population need not be hashable or unique.  If the
        population contains repeats, then each occurrence is a possible
        selection in the sample.

        To choose a sample in a range of integers, use range as an argument.
        This is especially fast and space efficient for sampling from a
        large population:   sample(range(10000000), 60)
        """
            if isinstance(population, _Set):
                population = tuple(population)
            if not isinstance(population, _Sequence):
                raise TypeError('Population must be a sequence or set.  For dicts, use list(d).')
            randbelow = self._randbelow
            n = len(population)
            if not 0 <= k <= n:
                raise ValueError('Sample larger than population or is negative')
            result = [
             None] * k
            setsize = 21
            if k > 5:
                setsize += 4 ** _ceil(_log(k * 3, 4))
            if n <= setsize:
                pool = list(population)
                for i in range(k):
                    j = randbelow(n - i)
                    result[i] = pool[j]
                    pool[j] = pool[(n - i - 1)]

            else:
                selected = set()
                selected_add = selected.add
                for i in range(k):
                    j = randbelow(n)
                    if j in selected:
                        j = randbelow(n)
                    else:
                        selected_add(j)
                        result[i] = population[j]
                    return result

        def choices(self, population, weights=None, *, cum_weights=None, k=1):
            """Return a k sized list of population elements chosen with replacement.

        If the relative weights or cumulative weights are not specified,
        the selections are made with equal probability.

        """
            random = self.random
            n = len(population)
            if cum_weights is None:
                if weights is None:
                    _int = int
                    n += 0.0
                    return [population[_int(random() * n)] for i in _repeat(None, k)]
                cum_weights = list(_accumulate(weights))
            else:
                if weights is not None:
                    raise TypeError('Cannot specify both weights and cumulative weights')
            if len(cum_weights) != n:
                raise ValueError('The number of weights does not match the population')
            bisect = _bisect
            total = cum_weights[(-1)] + 0.0
            hi = n - 1
            return [population[bisect(cum_weights, random() * total, 0, hi)] for i in _repeat(None, k)]

        def uniform(self, a, b):
            """Get a random number in the range [a, b) or [a, b] depending on rounding."""
            return a + (b - a) * self.random()

        def triangular(self, low=0.0, high=1.0, mode=None):
            """Triangular distribution.

        Continuous distribution bounded by given lower and upper limits,
        and having a given mode value in-between.

        http://en.wikipedia.org/wiki/Triangular_distribution

        """
            u = self.random()
            try:
                c = 0.5 if mode is None else (mode - low) / (high - low)
            except ZeroDivisionError:
                return low
            else:
                if u > c:
                    u = 1.0 - u
                    c = 1.0 - c
                    low, high = high, low
                return low + (high - low) * _sqrt(u * c)

        def normalvariate(self, mu, sigma):
            """Normal distribution.

        mu is the mean, and sigma is the standard deviation.

        """
            random = self.random
            while True:
                u1 = random()
                u2 = 1.0 - random()
                z = NV_MAGICCONST * (u1 - 0.5) / u2
                zz = z * z / 4.0
                if zz <= -_log(u2):
                    break

            return mu + z * sigma

        def lognormvariate(self, mu, sigma):
            """Log normal distribution.

        If you take the natural logarithm of this distribution, you'll get a
        normal distribution with mean mu and standard deviation sigma.
        mu can have any value, and sigma must be greater than zero.

        """
            return _exp(self.normalvariate(mu, sigma))

        def expovariate(self, lambd):
            """Exponential distribution.

        lambd is 1.0 divided by the desired mean.  It should be
        nonzero.  (The parameter would be called "lambda", but that is
        a reserved word in Python.)  Returned values range from 0 to
        positive infinity if lambd is positive, and from negative
        infinity to 0 if lambd is negative.

        """
            return -_log(1.0 - self.random()) / lambd

        def vonmisesvariate(self, mu, kappa):
            """Circular data distribution.

        mu is the mean angle, expressed in radians between 0 and 2*pi, and
        kappa is the concentration parameter, which must be greater than or
        equal to zero.  If kappa is equal to zero, this distribution reduces
        to a uniform random angle over the range 0 to 2*pi.

        """
            random = self.random
            if kappa <= 1e-06:
                return TWOPI * random()
                s = 0.5 / kappa
                r = s + _sqrt(1.0 + s * s)
                while True:
                    u1 = random()
                    z = _cos(_pi * u1)
                    d = z / (r + z)
                    u2 = random()
                    if not u2 < 1.0 - d * d:
                        if u2 <= (1.0 - d) * _exp(d):
                            break

            else:
                q = 1.0 / r
                f = (q + z) / (1.0 + q * z)
                u3 = random()
                if u3 > 0.5:
                    theta = (mu + _acos(f)) % TWOPI
                else:
                    theta = (mu - _acos(f)) % TWOPI
            return theta

        def gammavariate--- This code section failed: ---

 L. 564         0  LOAD_FAST                'alpha'
                2  LOAD_CONST               0.0
                4  COMPARE_OP               <=
                6  POP_JUMP_IF_TRUE     16  'to 16'
                8  LOAD_FAST                'beta'
               10  LOAD_CONST               0.0
               12  COMPARE_OP               <=
               14  POP_JUMP_IF_FALSE    24  'to 24'
             16_0  COME_FROM             6  '6'

 L. 565        16  LOAD_GLOBAL              ValueError
               18  LOAD_STR                 'gammavariate: alpha and beta must be > 0.0'
               20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            14  '14'

 L. 567        24  LOAD_FAST                'self'
               26  LOAD_ATTR                random
               28  STORE_FAST               'random'

 L. 568        30  LOAD_FAST                'alpha'
               32  LOAD_CONST               1.0
               34  COMPARE_OP               >
               36  POP_JUMP_IF_FALSE   214  'to 214'

 L. 574        38  LOAD_GLOBAL              _sqrt
               40  LOAD_CONST               2.0
               42  LOAD_FAST                'alpha'
               44  BINARY_MULTIPLY  
               46  LOAD_CONST               1.0
               48  BINARY_SUBTRACT  
               50  CALL_FUNCTION_1       1  ''
               52  STORE_FAST               'ainv'

 L. 575        54  LOAD_FAST                'alpha'
               56  LOAD_GLOBAL              LOG4
               58  BINARY_SUBTRACT  
               60  STORE_FAST               'bbb'

 L. 576        62  LOAD_FAST                'alpha'
               64  LOAD_FAST                'ainv'
               66  BINARY_ADD       
               68  STORE_FAST               'ccc'
             70_0  COME_FROM           200  '200'

 L. 579        70  LOAD_FAST                'random'
               72  CALL_FUNCTION_0       0  ''
               74  STORE_FAST               'u1'

 L. 580        76  LOAD_CONST               1e-07
               78  LOAD_FAST                'u1'
               80  DUP_TOP          
               82  ROT_THREE        
               84  COMPARE_OP               <
               86  POP_JUMP_IF_FALSE    96  'to 96'
               88  LOAD_CONST               0.9999999
               90  COMPARE_OP               <
               92  POP_JUMP_IF_TRUE    100  'to 100'
               94  JUMP_BACK            70  'to 70'
             96_0  COME_FROM            86  '86'
               96  POP_TOP          

 L. 581        98  JUMP_BACK            70  'to 70'
            100_0  COME_FROM            92  '92'

 L. 582       100  LOAD_CONST               1.0
              102  LOAD_FAST                'random'
              104  CALL_FUNCTION_0       0  ''
              106  BINARY_SUBTRACT  
              108  STORE_FAST               'u2'

 L. 583       110  LOAD_GLOBAL              _log
              112  LOAD_FAST                'u1'
              114  LOAD_CONST               1.0
              116  LOAD_FAST                'u1'
              118  BINARY_SUBTRACT  
              120  BINARY_TRUE_DIVIDE
              122  CALL_FUNCTION_1       1  ''
              124  LOAD_FAST                'ainv'
              126  BINARY_TRUE_DIVIDE
              128  STORE_FAST               'v'

 L. 584       130  LOAD_FAST                'alpha'
              132  LOAD_GLOBAL              _exp
              134  LOAD_FAST                'v'
              136  CALL_FUNCTION_1       1  ''
              138  BINARY_MULTIPLY  
              140  STORE_FAST               'x'

 L. 585       142  LOAD_FAST                'u1'
              144  LOAD_FAST                'u1'
              146  BINARY_MULTIPLY  
              148  LOAD_FAST                'u2'
              150  BINARY_MULTIPLY  
              152  STORE_FAST               'z'

 L. 586       154  LOAD_FAST                'bbb'
              156  LOAD_FAST                'ccc'
              158  LOAD_FAST                'v'
              160  BINARY_MULTIPLY  
              162  BINARY_ADD       
              164  LOAD_FAST                'x'
              166  BINARY_SUBTRACT  
              168  STORE_FAST               'r'

 L. 587       170  LOAD_FAST                'r'
              172  LOAD_GLOBAL              SG_MAGICCONST
              174  BINARY_ADD       
              176  LOAD_CONST               4.5
              178  LOAD_FAST                'z'
              180  BINARY_MULTIPLY  
              182  BINARY_SUBTRACT  
              184  LOAD_CONST               0.0
              186  COMPARE_OP               >=
              188  POP_JUMP_IF_TRUE    202  'to 202'
              190  LOAD_FAST                'r'
              192  LOAD_GLOBAL              _log
              194  LOAD_FAST                'z'
              196  CALL_FUNCTION_1       1  ''
              198  COMPARE_OP               >=
              200  POP_JUMP_IF_FALSE    70  'to 70'
            202_0  COME_FROM           188  '188'

 L. 588       202  LOAD_FAST                'x'
              204  LOAD_FAST                'beta'
              206  BINARY_MULTIPLY  
              208  RETURN_VALUE     
              210  JUMP_BACK            70  'to 70'
              212  JUMP_FORWARD        378  'to 378'
            214_0  COME_FROM            36  '36'

 L. 590       214  LOAD_FAST                'alpha'
              216  LOAD_CONST               1.0
              218  COMPARE_OP               ==
              220  POP_JUMP_IF_FALSE   242  'to 242'

 L. 592       222  LOAD_GLOBAL              _log
              224  LOAD_CONST               1.0
              226  LOAD_FAST                'random'
              228  CALL_FUNCTION_0       0  ''
              230  BINARY_SUBTRACT  
              232  CALL_FUNCTION_1       1  ''
              234  UNARY_NEGATIVE   
              236  LOAD_FAST                'beta'
              238  BINARY_MULTIPLY  
              240  RETURN_VALUE     
            242_0  COME_FROM           362  '362'
            242_1  COME_FROM           220  '220'

 L. 599       242  LOAD_FAST                'random'
              244  CALL_FUNCTION_0       0  ''
              246  STORE_FAST               'u'

 L. 600       248  LOAD_GLOBAL              _e
              250  LOAD_FAST                'alpha'
              252  BINARY_ADD       
              254  LOAD_GLOBAL              _e
              256  BINARY_TRUE_DIVIDE
              258  STORE_FAST               'b'

 L. 601       260  LOAD_FAST                'b'
              262  LOAD_FAST                'u'
              264  BINARY_MULTIPLY  
              266  STORE_FAST               'p'

 L. 602       268  LOAD_FAST                'p'
              270  LOAD_CONST               1.0
              272  COMPARE_OP               <=
          274_276  POP_JUMP_IF_FALSE   292  'to 292'

 L. 603       278  LOAD_FAST                'p'
              280  LOAD_CONST               1.0
              282  LOAD_FAST                'alpha'
              284  BINARY_TRUE_DIVIDE
              286  BINARY_POWER     
              288  STORE_FAST               'x'
              290  JUMP_FORWARD        310  'to 310'
            292_0  COME_FROM           274  '274'

 L. 605       292  LOAD_GLOBAL              _log
              294  LOAD_FAST                'b'
              296  LOAD_FAST                'p'
              298  BINARY_SUBTRACT  
              300  LOAD_FAST                'alpha'
              302  BINARY_TRUE_DIVIDE
              304  CALL_FUNCTION_1       1  ''
              306  UNARY_NEGATIVE   
              308  STORE_FAST               'x'
            310_0  COME_FROM           290  '290'

 L. 606       310  LOAD_FAST                'random'
              312  CALL_FUNCTION_0       0  ''
              314  STORE_FAST               'u1'

 L. 607       316  LOAD_FAST                'p'
              318  LOAD_CONST               1.0
              320  COMPARE_OP               >
          322_324  POP_JUMP_IF_FALSE   350  'to 350'

 L. 608       326  LOAD_FAST                'u1'
              328  LOAD_FAST                'x'
              330  LOAD_FAST                'alpha'
              332  LOAD_CONST               1.0
              334  BINARY_SUBTRACT  
              336  BINARY_POWER     
              338  COMPARE_OP               <=
          340_342  POP_JUMP_IF_FALSE   368  'to 368'

 L. 609   344_346  BREAK_LOOP          370  'to 370'
              348  JUMP_BACK           242  'to 242'
            350_0  COME_FROM           322  '322'

 L. 610       350  LOAD_FAST                'u1'
              352  LOAD_GLOBAL              _exp
              354  LOAD_FAST                'x'
              356  UNARY_NEGATIVE   
              358  CALL_FUNCTION_1       1  ''
              360  COMPARE_OP               <=
              362  POP_JUMP_IF_FALSE   242  'to 242'

 L. 611   364_366  BREAK_LOOP          370  'to 370'
            368_0  COME_FROM           340  '340'
              368  JUMP_BACK           242  'to 242'

 L. 612       370  LOAD_FAST                'x'
              372  LOAD_FAST                'beta'
              374  BINARY_MULTIPLY  
              376  RETURN_VALUE     
            378_0  COME_FROM           212  '212'

Parse error at or near `JUMP_BACK' instruction at offset 98

        def gauss(self, mu, sigma):
            """Gaussian distribution.

        mu is the mean, and sigma is the standard deviation.  This is
        slightly faster than the normalvariate() function.

        Not thread-safe without a lock around calls.

        """
            random = self.random
            z = self.gauss_next
            self.gauss_next = None
            if z is None:
                x2pi = random() * TWOPI
                g2rad = _sqrt(-2.0 * _log(1.0 - random()))
                z = _cos(x2pi) * g2rad
                self.gauss_next = _sin(x2pi) * g2rad
            return mu + z * sigma

        def betavariate(self, alpha, beta):
            """Beta distribution.

        Conditions on the parameters are alpha > 0 and beta > 0.
        Returned values range between 0 and 1.

        """
            y = self.gammavariate(alpha, 1.0)
            if y == 0:
                return 0.0
            return y / (y + self.gammavariate(beta, 1.0))

        def paretovariate(self, alpha):
            """Pareto distribution.  alpha is the shape parameter."""
            u = 1.0 - self.random()
            return 1.0 / u ** (1.0 / alpha)

        def weibullvariate(self, alpha, beta):
            """Weibull distribution.

        alpha is the scale parameter and beta is the shape parameter.

        """
            u = 1.0 - self.random()
            return alpha * (-_log(u)) ** (1.0 / beta)


    class SystemRandom(Random):
        __doc__ = 'Alternate random number generator using sources provided\n    by the operating system (such as /dev/urandom on Unix or\n    CryptGenRandom on Windows).\n\n     Not available on all systems (see os.urandom() for details).\n    '

        def random(self):
            """Get the next random number in the range [0.0, 1.0)."""
            return (int.from_bytes(_urandom(7), 'big') >> 3) * RECIP_BPF

        def getrandbits(self, k):
            """getrandbits(k) -> x.  Generates an int with k random bits."""
            if k <= 0:
                raise ValueError('number of bits must be greater than zero')
            numbytes = (k + 7) // 8
            x = int.from_bytes(_urandom(numbytes), 'big')
            return x >> numbytes * 8 - k

        def seed(self, *args, **kwds):
            """Stub method.  Not used for a system random number generator."""
            pass

        def _notimplemented(self, *args, **kwds):
            """Method should not be called for a system random number generator."""
            raise NotImplementedError('System entropy source does not have state.')

        getstate = setstate = _notimplemented


    def _test_generator(n, func, args):
        import time
        print(n, 'times', func.__name__)
        total = 0.0
        sqsum = 0.0
        smallest = 10000000000.0
        largest = -10000000000.0
        t0 = time.perf_counter()
        for i in range(n):
            x = func(*args)
            total += x
            sqsum = sqsum + x * x
            smallest = min(x, smallest)
            largest = max(x, largest)
        else:
            t1 = time.perf_counter()
            print((round(t1 - t0, 3)), 'sec,', end=' ')
            avg = total / n
            stddev = _sqrt(sqsum / n - avg * avg)
            print('avg %g, stddev %g, min %g, max %g\n' % (
             avg, stddev, smallest, largest))


    def _test(N=2000):
        _test_generator(N, random, ())
        _test_generator(N, normalvariate, (0.0, 1.0))
        _test_generator(N, lognormvariate, (0.0, 1.0))
        _test_generator(N, vonmisesvariate, (0.0, 1.0))
        _test_generator(N, gammavariate, (0.01, 1.0))
        _test_generator(N, gammavariate, (0.1, 1.0))
        _test_generator(N, gammavariate, (0.1, 2.0))
        _test_generator(N, gammavariate, (0.5, 1.0))
        _test_generator(N, gammavariate, (0.9, 1.0))
        _test_generator(N, gammavariate, (1.0, 1.0))
        _test_generator(N, gammavariate, (2.0, 1.0))
        _test_generator(N, gammavariate, (20.0, 1.0))
        _test_generator(N, gammavariate, (200.0, 1.0))
        _test_generator(N, gauss, (0.0, 1.0))
        _test_generator(N, betavariate, (3.0, 3.0))
        _test_generator(N, triangular, (0.0, 1.0, 0.3333333333333333))


    _inst = Random()
    seed = _inst.seed
    random = _inst.random
    uniform = _inst.uniform
    triangular = _inst.triangular
    randint = _inst.randint
    choice = _inst.choice
    randrange = _inst.randrange
    sample = _inst.sample
    shuffle = _inst.shuffle
    choices = _inst.choices
    normalvariate = _inst.normalvariate
    lognormvariate = _inst.lognormvariate
    expovariate = _inst.expovariate
    vonmisesvariate = _inst.vonmisesvariate
    gammavariate = _inst.gammavariate
    gauss = _inst.gauss
    betavariate = _inst.betavariate
    paretovariate = _inst.paretovariate
    weibullvariate = _inst.weibullvariate
    getstate = _inst.getstate
    setstate = _inst.setstate
    getrandbits = _inst.getrandbits
    if hasattr(_os, 'fork'):
        _os.register_at_fork(after_in_child=(_inst.seed))
    if __name__ == '__main__':
        _test()