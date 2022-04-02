# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: numpy\polynomial\__init__.py
"""
A sub-package for efficiently dealing with polynomials.

Within the documentation for this sub-package, a "finite power series,"
i.e., a polynomial (also referred to simply as a "series") is represented
by a 1-D numpy array of the polynomial's coefficients, ordered from lowest
order term to highest.  For example, array([1,2,3]) represents
``P_0 + 2*P_1 + 3*P_2``, where P_n is the n-th order basis polynomial
applicable to the specific module in question, e.g., `polynomial` (which
"wraps" the "standard" basis) or `chebyshev`.  For optimal performance,
all operations on polynomials, including evaluation at an argument, are
implemented as operations on the coefficients.  Additional (module-specific)
information can be found in the docstring for the module of interest.

This package provides *convenience classes* for each of six different kinds
of polynomials:

         ============    ================
         **Name**        **Provides**
         ============    ================
         Polynomial      Power series
         Chebyshev       Chebyshev series
         Legendre        Legendre series
         Laguerre        Laguerre series
         Hermite         Hermite series
         HermiteE        HermiteE series
         ============    ================

These *convenience classes* provide a consistent interface for creating,
manipulating, and fitting data with polynomials of different bases.
The convenience classes are the preferred interface for the `~numpy.polynomial`
package, and are available from the `numpy.polynomial` namespace.
This eliminates the need to
navigate to the corresponding submodules, e.g. ``np.polynomial.Polynomial``
or ``np.polynomial.Chebyshev`` instead of
``np.polynomial.polynomial.Polynomial`` or 
``np.polynomial.chebyshev.Chebyshev``, respectively.
The classes provide a more consistent and concise interface than the
type-specific functions defined in the submodules for each type of polynomial.
For example, to fit a Chebyshev polynomial with degree ``1`` to data given
by arrays ``xdata`` and ``ydata``, the 
`~chebyshev.Chebyshev.fit` class method::

    >>> from numpy.polynomial import Chebyshev
    >>> c = Chebyshev.fit(xdata, ydata, deg=1)

is preferred over the `chebyshev.chebfit` function from the 
`numpy.polynomial.chebyshev` module::

    >>> from numpy.polynomial.chebyshev import chebfit
    >>> c = chebfit(xdata, ydata, deg=1)

See :doc:`routines.polynomials.classes` for more details.

Convenience Classes
===================

The following lists the various constants and methods common to all of
the classes representing the various kinds of polynomials. In the following,
the term ``Poly`` represents any one of the convenience classes (e.g.
``Polynomial``, ``Chebyshev``, ``Hermite``, etc.) while the lowercase ``p``
represents an **instance** of a polynomial class.

Constants
---------

- ``Poly.domain``     -- Default domain
- ``Poly.window``     -- Default window
- ``Poly.basis_name`` -- String used to represent the basis
- ``Poly.maxpower``   -- Maximum value ``n`` such that ``p**n`` is allowed
- ``Poly.nickname``   -- String used in printing

Creation
--------

Methods for creating polynomial instances.

- ``Poly.basis(degree)``    -- Basis polynomial of given degree
- ``Poly.identity()``       -- ``p`` where ``p(x) = x`` for all ``x``
- ``Poly.fit(x, y, deg)``   -- ``p`` of degree ``deg`` with coefficients 
  determined by the least-squares fit to the data ``x``, ``y``
- ``Poly.fromroots(roots)`` -- ``p`` with specified roots
- ``p.copy()``              -- Create a copy of ``p``

Conversion
----------

Methods for converting a polynomial instance of one kind to another.

- ``p.cast(Poly)``    -- Convert ``p`` to instance of kind ``Poly``
- ``p.convert(Poly)`` -- Convert ``p`` to instance of kind ``Poly`` or map
  between ``domain`` and ``window``

Calculus
--------
- ``p.deriv()`` -- Take the derivative of ``p``
- ``p.integ()`` -- Integrate ``p``

Validation
----------
- ``Poly.has_samecoef(p1, p2)``   -- Check if coefficients match
- ``Poly.has_samedomain(p1, p2)`` -- Check if domains match
- ``Poly.has_sametype(p1, p2)``   -- Check if types match
- ``Poly.has_samewindow(p1, p2)`` -- Check if windows match

Misc
----
- ``p.linspace()`` -- Return ``x, p(x)`` at equally-spaced points in ``domain``
- ``p.mapparms()`` -- Return the parameters for the linear mapping between
  ``domain`` and ``window``.
- ``p.roots()``    -- Return the roots of `p`.
- ``p.trim()``     -- Remove trailing coefficients.
- ``p.cutdeg(degree)`` -- Truncate p to given degree
- ``p.truncate(size)`` -- Truncate p to given size

"""
from .polynomial import Polynomial
from .chebyshev import Chebyshev
from .legendre import Legendre
from .hermite import Hermite
from .hermite_e import HermiteE
from .laguerre import Laguerre

def set_default_printstyle--- This code section failed: ---

 L. 162         0  LOAD_FAST                'style'
                2  LOAD_CONST               ('unicode', 'ascii')
                4  <118>                 1  ''
                6  POP_JUMP_IF_FALSE    24  'to 24'

 L. 163         8  LOAD_GLOBAL              ValueError

 L. 164        10  LOAD_STR                 "Unsupported format string '"
               12  LOAD_FAST                'style'
               14  FORMAT_VALUE          0  ''
               16  LOAD_STR                 "'. Valid options are 'ascii' and 'unicode'"
               18  BUILD_STRING_3        3 

 L. 163        20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM             6  '6'

 L. 167        24  LOAD_CONST               True
               26  STORE_FAST               '_use_unicode'

 L. 168        28  LOAD_FAST                'style'
               30  LOAD_STR                 'ascii'
               32  COMPARE_OP               ==
               34  POP_JUMP_IF_FALSE    40  'to 40'

 L. 169        36  LOAD_CONST               False
               38  STORE_FAST               '_use_unicode'
             40_0  COME_FROM            34  '34'

 L. 170        40  LOAD_CONST               1
               42  LOAD_CONST               ('ABCPolyBase',)
               44  IMPORT_NAME              _polybase
               46  IMPORT_FROM              ABCPolyBase
               48  STORE_FAST               'ABCPolyBase'
               50  POP_TOP          

 L. 171        52  LOAD_FAST                '_use_unicode'
               54  LOAD_FAST                'ABCPolyBase'
               56  STORE_ATTR               _use_unicode

Parse error at or near `None' instruction at offset -1


from numpy._pytesttester import PytestTester
test = PytestTester(__name__)
del PytestTester