# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: numpy\lib\utils.py
import os, sys, textwrap, types, re, warnings
from numpy.core.numerictypes import issubclass_, issubsctype, issubdtype
from numpy.core.overrides import set_module
from numpy.core import ndarray, ufunc, asarray
import numpy as np
__all__ = [
 'issubclass_', 'issubsctype', 'issubdtype', 'deprecate',
 'deprecate_with_doc', 'get_include', 'info', 'source', 'who',
 'lookfor', 'byte_bounds', 'safe_eval']

def get_include():
    r"""
    Return the directory that contains the NumPy \*.h header files.

    Extension modules that need to compile against NumPy should use this
    function to locate the appropriate include directory.

    Notes
    -----
    When using ``distutils``, for example in ``setup.py``.
    ::

        import numpy as np
        ...
        Extension('extension_name', ...
                include_dirs=[np.get_include()])
        ...

    """
    import numpy
    if numpy.show_config is None:
        d = os.path.join(os.path.dirname(numpy.__file__), 'core', 'include')
    else:
        import numpy.core as core
        d = os.path.join(os.path.dirname(core.__file__), 'include')
    return d


def _set_function_name(func, name):
    func.__name__ = name
    return func


class _Deprecate:
    __doc__ = '\n    Decorator class to deprecate old functions.\n\n    Refer to `deprecate` for details.\n\n    See Also\n    --------\n    deprecate\n\n    '

    def __init__(self, old_name=None, new_name=None, message=None):
        self.old_name = old_name
        self.new_name = new_name
        self.message = message

    def __call__(self, func, *args, **kwargs):
        """
        Decorator call.  Refer to ``decorate``.

        """
        old_name = self.old_name
        new_name = self.new_name
        message = self.message
        if old_name is None:
            try:
                old_name = func.__name__
            except AttributeError:
                old_name = func.__name__

            if new_name is None:
                depdoc = '`%s` is deprecated!' % old_name
            else:
                depdoc = '`%s` is deprecated, use `%s` instead!' % (
                 old_name, new_name)
            if message is not None:
                depdoc += '\n' + message

            def newfunc(*args, **kwds):
                warnings.warn(depdoc, DeprecationWarning, stacklevel=2)
                return func(*args, **kwds)

            newfunc = _set_function_name(newfunc, old_name)
            doc = func.__doc__
            if doc is None:
                doc = depdoc
            else:
                lines = doc.expandtabs().split('\n')
                indent = _get_indent(lines[1:])
                if lines[0].lstrip():
                    doc = indent * ' ' + doc
                else:
                    skip = len(lines[0]) + 1
                    for line in lines[1:]:
                        if len(line) > indent:
                            break
                        else:
                            skip += len(line) + 1

                    doc = doc[skip:]
                depdoc = textwrap.indent(depdoc, ' ' * indent)
                doc = '\n\n'.join([depdoc, doc])
            newfunc.__doc__ = doc
            try:
                d = func.__dict__
            except AttributeError:
                pass
            else:
                newfunc.__dict__.update(d)

            return newfunc


def _get_indent(lines):
    """
    Determines the leading whitespace that could be removed from all the lines.
    """
    indent = sys.maxsize
    for line in lines:
        content = len(line.lstrip())
        if content:
            indent = min(indent, len(line) - content)

    if indent == sys.maxsize:
        indent = 0
    return indent


def deprecate(*args, **kwargs):
    """
    Issues a DeprecationWarning, adds warning to `old_name`'s
    docstring, rebinds ``old_name.__name__`` and returns the new
    function object.

    This function may also be used as a decorator.

    Parameters
    ----------
    func : function
        The function to be deprecated.
    old_name : str, optional
        The name of the function to be deprecated. Default is None, in
        which case the name of `func` is used.
    new_name : str, optional
        The new name for the function. Default is None, in which case the
        deprecation message is that `old_name` is deprecated. If given, the
        deprecation message is that `old_name` is deprecated and `new_name`
        should be used instead.
    message : str, optional
        Additional explanation of the deprecation.  Displayed in the
        docstring after the warning.

    Returns
    -------
    old_func : function
        The deprecated function.

    Examples
    --------
    Note that ``olduint`` returns a value after printing Deprecation
    Warning:

    >>> olduint = np.deprecate(np.uint)
    DeprecationWarning: `uint64` is deprecated! # may vary
    >>> olduint(6)
    6

    """
    if args:
        fn = args[0]
        args = args[1:]
        return _Deprecate(*args, **kwargs)(fn)
    return _Deprecate(*args, **kwargs)


deprecate_with_doc = lambda msg: _Deprecate(message=msg)

def byte_bounds(a):
    """
    Returns pointers to the end-points of an array.

    Parameters
    ----------
    a : ndarray
        Input array. It must conform to the Python-side of the array
        interface.

    Returns
    -------
    (low, high) : tuple of 2 integers
        The first integer is the first byte of the array, the second
        integer is just past the last byte of the array.  If `a` is not
        contiguous it will not use every byte between the (`low`, `high`)
        values.

    Examples
    --------
    >>> I = np.eye(2, dtype='f'); I.dtype
    dtype('float32')
    >>> low, high = np.byte_bounds(I)
    >>> high - low == I.size*I.itemsize
    True
    >>> I = np.eye(2); I.dtype
    dtype('float64')
    >>> low, high = np.byte_bounds(I)
    >>> high - low == I.size*I.itemsize
    True

    """
    ai = a.__array_interface__
    a_data = ai['data'][0]
    astrides = ai['strides']
    ashape = ai['shape']
    bytes_a = asarray(a).dtype.itemsize
    a_low = a_high = a_data
    if astrides is None:
        a_high += a.size * bytes_a
    else:
        for shape, stride in zip(ashape, astrides):
            if stride < 0:
                a_low += (shape - 1) * stride
            else:
                a_high += (shape - 1) * stride

        a_high += bytes_a
    return (a_low, a_high)


def who(vardict=None):
    """
    Print the NumPy arrays in the given dictionary.

    If there is no dictionary passed in or `vardict` is None then returns
    NumPy arrays in the globals() dictionary (all NumPy arrays in the
    namespace).

    Parameters
    ----------
    vardict : dict, optional
        A dictionary possibly containing ndarrays.  Default is globals().

    Returns
    -------
    out : None
        Returns 'None'.

    Notes
    -----
    Prints out the name, shape, bytes and type of all of the ndarrays
    present in `vardict`.

    Examples
    --------
    >>> a = np.arange(10)
    >>> b = np.ones(20)
    >>> np.who()
    Name            Shape            Bytes            Type
    ===========================================================
    a               10               80               int64
    b               20               160              float64
    Upper bound on total bytes  =       240

    >>> d = {'x': np.arange(2.0), 'y': np.arange(3.0), 'txt': 'Some str',
    ... 'idx':5}
    >>> np.who(d)
    Name            Shape            Bytes            Type
    ===========================================================
    x               2                16               float64
    y               3                24               float64
    Upper bound on total bytes  =       40

    """
    if vardict is None:
        frame = sys._getframe().f_back
        vardict = frame.f_globals
    sta = []
    cache = {}
    for name in vardict.keys():
        if isinstance(vardict[name], ndarray):
            var = vardict[name]
            idv = id(var)
            if idv in cache.keys():
                namestr = name + ' (%s)' % cache[idv]
                original = 0
            else:
                cache[idv] = name
                namestr = name
                original = 1
            shapestr = ' x '.join(map(str, var.shape))
            bytestr = str(var.nbytes)
            sta.append([namestr, shapestr, bytestr, var.dtype.name,
             original])

    maxname = 0
    maxshape = 0
    maxbyte = 0
    totalbytes = 0
    for k in range(len(sta)):
        val = sta[k]
        if maxname < len(val[0]):
            maxname = len(val[0])
        if maxshape < len(val[1]):
            maxshape = len(val[1])
        if maxbyte < len(val[2]):
            maxbyte = len(val[2])
        if val[4]:
            totalbytes += int(val[2])

    if len(sta) > 0:
        sp1 = max(10, maxname)
        sp2 = max(10, maxshape)
        sp3 = max(10, maxbyte)
        prval = 'Name %s Shape %s Bytes %s Type' % (sp1 * ' ', sp2 * ' ', sp3 * ' ')
        print(prval + '\n' + '=' * (len(prval) + 5) + '\n')
    for k in range(len(sta)):
        val = sta[k]
        print('%s %s %s %s %s %s %s' % (val[0], ' ' * (sp1 - len(val[0]) + 4),
         val[1], ' ' * (sp2 - len(val[1]) + 5),
         val[2], ' ' * (sp3 - len(val[2]) + 5),
         val[3]))

    print('\nUpper bound on total bytes  =       %d' % totalbytes)


def _split_line(name, arguments, width):
    firstwidth = len(name)
    k = firstwidth
    newstr = name
    sepstr = ', '
    arglist = arguments.split(sepstr)
    for argument in arglist:
        if k == firstwidth:
            addstr = ''
        else:
            addstr = sepstr
        k = k + len(argument) + len(addstr)
        if k > width:
            k = firstwidth + 1 + len(argument)
            newstr = newstr + ',\n' + ' ' * (firstwidth + 2) + argument
        else:
            newstr = newstr + addstr + argument

    return newstr


_namedict = None
_dictlist = None

def _makenamedict(module='numpy'):
    module = __import__(module, globals(), locals(), [])
    thedict = {module.__name__: module.__dict__}
    dictlist = [module.__name__]
    totraverse = [module.__dict__]
    while 1:
        if len(totraverse) == 0:
            break
        else:
            thisdict = totraverse.pop(0)
            for x in thisdict.keys():
                if isinstance(thisdict[x], types.ModuleType):
                    modname = thisdict[x].__name__
                    if modname not in dictlist:
                        moddict = thisdict[x].__dict__
                        dictlist.append(modname)
                        totraverse.append(moddict)
                        thedict[modname] = moddict

    return (
     thedict, dictlist)


def _info(obj, output=sys.stdout):
    """Provide information about ndarray obj.

    Parameters
    ----------
    obj : ndarray
        Must be ndarray, not checked.
    output
        Where printed output goes.

    Notes
    -----
    Copied over from the numarray module prior to its removal.
    Adapted somewhat as only numpy is an option now.

    Called by info.

    """
    extra = ''
    tic = ''
    bp = lambda x: x
    cls = getattr(obj, '__class__', type(obj))
    nm = getattr(cls, '__name__', cls)
    strides = obj.strides
    endian = obj.dtype.byteorder
    print('class: ', nm, file=output)
    print('shape: ', (obj.shape), file=output)
    print('strides: ', strides, file=output)
    print('itemsize: ', (obj.itemsize), file=output)
    print('aligned: ', (bp(obj.flags.aligned)), file=output)
    print('contiguous: ', (bp(obj.flags.contiguous)), file=output)
    print('fortran: ', (obj.flags.fortran), file=output)
    print(('data pointer: %s%s' % (hex(obj.ctypes._as_parameter_.value), extra)),
      file=output)
    print('byteorder: ', end=' ', file=output)
    if endian in ('|', '='):
        print(('%s%s%s' % (tic, sys.byteorder, tic)), file=output)
        byteswap = False
    elif endian == '>':
        print(('%sbig%s' % (tic, tic)), file=output)
        byteswap = sys.byteorder != 'big'
    else:
        print(('%slittle%s' % (tic, tic)), file=output)
        byteswap = sys.byteorder != 'little'
    print('byteswap: ', (bp(byteswap)), file=output)
    print(('type: %s' % obj.dtype), file=output)


@set_module('numpy')
def info(object=None, maxwidth=76, output=sys.stdout, toplevel='numpy'):
    """
    Get help information for a function, class, or module.

    Parameters
    ----------
    object : object or str, optional
        Input object or name to get information about. If `object` is a
        numpy object, its docstring is given. If it is a string, available
        modules are searched for matching objects.  If None, information
        about `info` itself is returned.
    maxwidth : int, optional
        Printing width.
    output : file like object, optional
        File like object that the output is written to, default is
        ``stdout``.  The object has to be opened in 'w' or 'a' mode.
    toplevel : str, optional
        Start search at this level.

    See Also
    --------
    source, lookfor

    Notes
    -----
    When used interactively with an object, ``np.info(obj)`` is equivalent
    to ``help(obj)`` on the Python prompt or ``obj?`` on the IPython
    prompt.

    Examples
    --------
    >>> np.info(np.polyval) # doctest: +SKIP
       polyval(p, x)
         Evaluate the polynomial p at x.
         ...

    When using a string for `object` it is possible to get multiple results.

    >>> np.info('fft') # doctest: +SKIP
         *** Found in numpy ***
    Core FFT routines
    ...
         *** Found in numpy.fft ***
     fft(a, n=None, axis=-1)
    ...
         *** Repeat reference found in numpy.fft.fftpack ***
         *** Total of 3 references found. ***

    """
    global _dictlist
    global _namedict
    import pydoc, inspect
    if hasattr(object, '_ppimport_importer') or hasattr(object, '_ppimport_module'):
        object = object._ppimport_module
    elif hasattr(object, '_ppimport_attr'):
        object = object._ppimport_attr
    if object is None:
        info(info)
    elif isinstance(object, ndarray):
        _info(object, output=output)
    elif isinstance(object, str):
        if _namedict is None:
            _namedict, _dictlist = _makenamedict(toplevel)
        numfound = 0
        objlist = []
        for namestr in _dictlist:
            try:
                obj = _namedict[namestr][object]
                if id(obj) in objlist:
                    print(('\n     *** Repeat reference found in %s *** ' % namestr),
                      file=output)
                else:
                    objlist.append(id(obj))
                    print(('     *** Found in %s ***' % namestr), file=output)
                    info(obj)
                    print(('-' * maxwidth), file=output)
                numfound += 1
            except KeyError:
                pass

        if numfound == 0:
            print(('Help for %s not found.' % object), file=output)
        else:
            print(('\n     *** Total of %d references found. ***' % numfound),
              file=output)
    elif inspect.isfunction(object) or inspect.ismethod(object):
        name = object.__name__
        try:
            arguments = str(inspect.signature(object))
        except Exception:
            arguments = '()'

        if len(name + arguments) > maxwidth:
            argstr = _split_line(name, arguments, maxwidth)
        else:
            argstr = name + arguments
        print((' ' + argstr + '\n'), file=output)
        print((inspect.getdoc(object)), file=output)
    elif inspect.isclass(object):
        name = object.__name__
        try:
            arguments = str(inspect.signature(object))
        except Exception:
            arguments = '()'

        if len(name + arguments) > maxwidth:
            argstr = _split_line(name, arguments, maxwidth)
        else:
            argstr = name + arguments
        print((' ' + argstr + '\n'), file=output)
        doc1 = inspect.getdoc(object)
        if doc1 is None:
            if hasattr(object, '__init__'):
                print((inspect.getdoc(object.__init__)), file=output)
        else:
            print((inspect.getdoc(object)), file=output)
        methods = pydoc.allmethods(object)
        public_methods = [meth for meth in methods if meth[0] != '_']
        if public_methods:
            print('\n\nMethods:\n', file=output)
            for meth in public_methods:
                thisobj = getattr(object, meth, None)
                if thisobj is not None:
                    methstr, other = pydoc.splitdoc(inspect.getdoc(thisobj) or 'None')
                else:
                    print(('  %s  --  %s' % (meth, methstr)), file=output)

    elif hasattr(object, '__doc__'):
        print((inspect.getdoc(object)), file=output)


@set_module('numpy')
def source(object, output=sys.stdout):
    '''
    Print or write to a file the source code for a NumPy object.

    The source code is only returned for objects written in Python. Many
    functions and classes are defined in C and will therefore not return
    useful information.

    Parameters
    ----------
    object : numpy object
        Input object. This can be any object (function, class, module,
        ...).
    output : file object, optional
        If `output` not supplied then source code is printed to screen
        (sys.stdout).  File object must be created with either write 'w' or
        append 'a' modes.

    See Also
    --------
    lookfor, info

    Examples
    --------
    >>> np.source(np.interp)                        #doctest: +SKIP
    In file: /usr/lib/python2.6/dist-packages/numpy/lib/function_base.py
    def interp(x, xp, fp, left=None, right=None):
        """.... (full docstring printed)"""
        if isinstance(x, (float, int, number)):
            return compiled_interp([x], xp, fp, left, right).item()
        else:
            return compiled_interp(x, xp, fp, left, right)

    The source code is only returned for objects written in Python.

    >>> np.source(np.array)                         #doctest: +SKIP
    Not available for this object.

    '''
    import inspect
    try:
        print(('In file: %s\n' % inspect.getsourcefile(object)), file=output)
        print((inspect.getsource(object)), file=output)
    except Exception:
        print('Not available for this object.', file=output)


_lookfor_caches = {}
_function_signature_re = re.compile('[a-z0-9_]+\\(.*[,=].*\\)', re.I)

@set_module('numpy')
def lookfor(what, module=None, import_modules=True, regenerate=False, output=None):
    """
    Do a keyword search on docstrings.

    A list of objects that matched the search is displayed,
    sorted by relevance. All given keywords need to be found in the
    docstring for it to be returned as a result, but the order does
    not matter.

    Parameters
    ----------
    what : str
        String containing words to look for.
    module : str or list, optional
        Name of module(s) whose docstrings to go through.
    import_modules : bool, optional
        Whether to import sub-modules in packages. Default is True.
    regenerate : bool, optional
        Whether to re-generate the docstring cache. Default is False.
    output : file-like, optional
        File-like object to write the output to. If omitted, use a pager.

    See Also
    --------
    source, info

    Notes
    -----
    Relevance is determined only roughly, by checking if the keywords occur
    in the function name, at the start of a docstring, etc.

    Examples
    --------
    >>> np.lookfor('binary representation') # doctest: +SKIP
    Search results for 'binary representation'
    ------------------------------------------
    numpy.binary_repr
        Return the binary representation of the input number as a string.
    numpy.core.setup_common.long_double_representation
        Given a binary dump as given by GNU od -b, look for long double
    numpy.base_repr
        Return a string representation of a number in the given base system.
    ...

    """
    import pydoc
    cache = _lookfor_generate_cache(module, import_modules, regenerate)
    found = []
    whats = str(what).lower().split()
    if not whats:
        return
    for name, (docstring, kind, index) in cache.items():
        if kind in ('module', 'object'):
            continue
        else:
            doc = docstring.lower()
        if all((w in doc for w in whats)):
            found.append(name)

    kind_relevance = {'func':1000, 
     'class':1000,  'module':-1000, 
     'object':-1000}

    def relevance(name, docstr, kind, index):
        r = 0
        first_doc = '\n'.join(docstr.lower().strip().split('\n')[:3])
        r += sum([200 for w in whats if w in first_doc])
        r += sum([30 for w in whats if w in name])
        r += -len(name) * 5
        r += kind_relevance.get(kind, -1000)
        r += -name.count('.') * 10
        r += max(-index / 100, -100)
        return r

    def relevance_value(a):
        return relevance(a, *cache[a])

    found.sort(key=relevance_value)
    s = "Search results for '%s'" % ' '.join(whats)
    help_text = [s, '-' * len(s)]
    for name in found[::-1]:
        doc, kind, ix = cache[name]
        doclines = [line.strip() for line in doc.strip().split('\n') if line.strip()]
        try:
            first_doc = doclines[0].strip()
            if _function_signature_re.search(first_doc):
                first_doc = doclines[1].strip()
        except IndexError:
            first_doc = ''

        help_text.append('%s\n    %s' % (name, first_doc))

    if not found:
        help_text.append('Nothing found.')
    if output is not None:
        output.write('\n'.join(help_text))
    elif len(help_text) > 10:
        pager = pydoc.getpager()
        pager('\n'.join(help_text))
    else:
        print('\n'.join(help_text))


def _lookfor_generate_cache--- This code section failed: ---

 L. 810         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              inspect
                6  STORE_FAST               'inspect'

 L. 812         8  LOAD_CONST               0
               10  LOAD_CONST               ('StringIO',)
               12  IMPORT_NAME              io
               14  IMPORT_FROM              StringIO
               16  STORE_FAST               'StringIO'
               18  POP_TOP          

 L. 814        20  LOAD_FAST                'module'
               22  LOAD_CONST               None
               24  COMPARE_OP               is
               26  POP_JUMP_IF_FALSE    32  'to 32'

 L. 815        28  LOAD_STR                 'numpy'
               30  STORE_FAST               'module'
             32_0  COME_FROM            26  '26'

 L. 817        32  LOAD_GLOBAL              isinstance
               34  LOAD_FAST                'module'
               36  LOAD_GLOBAL              str
               38  CALL_FUNCTION_2       2  '2 positional arguments'
               40  POP_JUMP_IF_FALSE    88  'to 88'

 L. 818        42  SETUP_EXCEPT         56  'to 56'

 L. 819        44  LOAD_GLOBAL              __import__
               46  LOAD_FAST                'module'
               48  CALL_FUNCTION_1       1  '1 positional argument'
               50  POP_TOP          
               52  POP_BLOCK        
               54  JUMP_FORWARD         76  'to 76'
             56_0  COME_FROM_EXCEPT     42  '42'

 L. 820        56  DUP_TOP          
               58  LOAD_GLOBAL              ImportError
               60  COMPARE_OP               exception-match
               62  POP_JUMP_IF_FALSE    74  'to 74'
               64  POP_TOP          
               66  POP_TOP          
               68  POP_TOP          

 L. 821        70  BUILD_MAP_0           0 
               72  RETURN_VALUE     
             74_0  COME_FROM            62  '62'
               74  END_FINALLY      
             76_0  COME_FROM            54  '54'

 L. 822        76  LOAD_GLOBAL              sys
               78  LOAD_ATTR                modules
               80  LOAD_FAST                'module'
               82  BINARY_SUBSCR    
               84  STORE_FAST               'module'
               86  JUMP_FORWARD        148  'to 148'
             88_0  COME_FROM            40  '40'

 L. 823        88  LOAD_GLOBAL              isinstance
               90  LOAD_FAST                'module'
               92  LOAD_GLOBAL              list
               94  CALL_FUNCTION_2       2  '2 positional arguments'
               96  POP_JUMP_IF_TRUE    108  'to 108'
               98  LOAD_GLOBAL              isinstance
              100  LOAD_FAST                'module'
              102  LOAD_GLOBAL              tuple
              104  CALL_FUNCTION_2       2  '2 positional arguments'
              106  POP_JUMP_IF_FALSE   148  'to 148'
            108_0  COME_FROM            96  '96'

 L. 824       108  BUILD_MAP_0           0 
              110  STORE_FAST               'cache'

 L. 825       112  SETUP_LOOP          144  'to 144'
              114  LOAD_FAST                'module'
              116  GET_ITER         
            118_0  COME_FROM           140  '140'
              118  FOR_ITER            142  'to 142'
              120  STORE_FAST               'mod'

 L. 826       122  LOAD_FAST                'cache'
              124  LOAD_METHOD              update
              126  LOAD_GLOBAL              _lookfor_generate_cache
              128  LOAD_FAST                'mod'
              130  LOAD_FAST                'import_modules'

 L. 827       132  LOAD_FAST                'regenerate'
              134  CALL_FUNCTION_3       3  '3 positional arguments'
              136  CALL_METHOD_1         1  '1 positional argument'
              138  POP_TOP          
              140  JUMP_BACK           118  'to 118'
              142  POP_BLOCK        
            144_0  COME_FROM_LOOP      112  '112'

 L. 828       144  LOAD_FAST                'cache'
              146  RETURN_VALUE     
            148_0  COME_FROM           106  '106'
            148_1  COME_FROM            86  '86'

 L. 830       148  LOAD_GLOBAL              id
              150  LOAD_FAST                'module'
              152  CALL_FUNCTION_1       1  '1 positional argument'
              154  LOAD_GLOBAL              _lookfor_caches
              156  COMPARE_OP               in
              158  POP_JUMP_IF_FALSE   176  'to 176'
              160  LOAD_FAST                'regenerate'
              162  POP_JUMP_IF_TRUE    176  'to 176'

 L. 831       164  LOAD_GLOBAL              _lookfor_caches
              166  LOAD_GLOBAL              id
              168  LOAD_FAST                'module'
              170  CALL_FUNCTION_1       1  '1 positional argument'
              172  BINARY_SUBSCR    
              174  RETURN_VALUE     
            176_0  COME_FROM           162  '162'
            176_1  COME_FROM           158  '158'

 L. 834       176  BUILD_MAP_0           0 
              178  STORE_FAST               'cache'

 L. 835       180  LOAD_FAST                'cache'
              182  LOAD_GLOBAL              _lookfor_caches
              184  LOAD_GLOBAL              id
              186  LOAD_FAST                'module'
              188  CALL_FUNCTION_1       1  '1 positional argument'
              190  STORE_SUBSCR     

 L. 836       192  BUILD_MAP_0           0 
              194  STORE_FAST               'seen'

 L. 837       196  LOAD_CONST               0
              198  STORE_FAST               'index'

 L. 838       200  LOAD_FAST                'module'
              202  LOAD_ATTR                __name__
              204  LOAD_FAST                'module'
              206  BUILD_TUPLE_2         2 
              208  BUILD_LIST_1          1 
              210  STORE_FAST               'stack'

 L. 839   212_214  SETUP_LOOP          962  'to 962'
            216_0  COME_FROM           958  '958'
            216_1  COME_FROM           942  '942'
            216_2  COME_FROM           248  '248'
              216  LOAD_FAST                'stack'
          218_220  POP_JUMP_IF_FALSE   960  'to 960'

 L. 840       222  LOAD_FAST                'stack'
              224  LOAD_METHOD              pop
              226  LOAD_CONST               0
              228  CALL_METHOD_1         1  '1 positional argument'
              230  UNPACK_SEQUENCE_2     2 
              232  STORE_FAST               'name'
              234  STORE_FAST               'item'

 L. 841       236  LOAD_GLOBAL              id
              238  LOAD_FAST                'item'
              240  CALL_FUNCTION_1       1  '1 positional argument'
              242  LOAD_FAST                'seen'
              244  COMPARE_OP               in
              246  POP_JUMP_IF_FALSE   250  'to 250'

 L. 842       248  CONTINUE            216  'to 216'
            250_0  COME_FROM           246  '246'

 L. 843       250  LOAD_CONST               True
              252  LOAD_FAST                'seen'
              254  LOAD_GLOBAL              id
              256  LOAD_FAST                'item'
              258  CALL_FUNCTION_1       1  '1 positional argument'
              260  STORE_SUBSCR     

 L. 845       262  LOAD_FAST                'index'
              264  LOAD_CONST               1
              266  INPLACE_ADD      
              268  STORE_FAST               'index'

 L. 846       270  LOAD_STR                 'object'
              272  STORE_FAST               'kind'

 L. 848       274  LOAD_FAST                'inspect'
              276  LOAD_METHOD              ismodule
              278  LOAD_FAST                'item'
              280  CALL_METHOD_1         1  '1 positional argument'
          282_284  POP_JUMP_IF_FALSE   814  'to 814'

 L. 849       286  LOAD_STR                 'module'
              288  STORE_FAST               'kind'

 L. 850       290  SETUP_EXCEPT        302  'to 302'

 L. 851       292  LOAD_FAST                'item'
              294  LOAD_ATTR                __all__
              296  STORE_FAST               '_all'
              298  POP_BLOCK        
              300  JUMP_FORWARD        328  'to 328'
            302_0  COME_FROM_EXCEPT    290  '290'

 L. 852       302  DUP_TOP          
              304  LOAD_GLOBAL              AttributeError
              306  COMPARE_OP               exception-match
          308_310  POP_JUMP_IF_FALSE   326  'to 326'
              312  POP_TOP          
              314  POP_TOP          
              316  POP_TOP          

 L. 853       318  LOAD_CONST               None
              320  STORE_FAST               '_all'
              322  POP_EXCEPT       
              324  JUMP_FORWARD        328  'to 328'
            326_0  COME_FROM           308  '308'
              326  END_FINALLY      
            328_0  COME_FROM           324  '324'
            328_1  COME_FROM           300  '300'

 L. 856       328  LOAD_FAST                'import_modules'
          330_332  POP_JUMP_IF_FALSE   590  'to 590'
              334  LOAD_GLOBAL              hasattr
              336  LOAD_FAST                'item'
              338  LOAD_STR                 '__path__'
              340  CALL_FUNCTION_2       2  '2 positional arguments'
          342_344  POP_JUMP_IF_FALSE   590  'to 590'

 L. 857       346  SETUP_LOOP          590  'to 590'
              348  LOAD_FAST                'item'
              350  LOAD_ATTR                __path__
              352  GET_ITER         
            354_0  COME_FROM           584  '584'
              354  FOR_ITER            588  'to 588'
              356  STORE_FAST               'pth'

 L. 858       358  SETUP_LOOP          584  'to 584'
              360  LOAD_GLOBAL              os
              362  LOAD_METHOD              listdir
              364  LOAD_FAST                'pth'
              366  CALL_METHOD_1         1  '1 positional argument'
              368  GET_ITER         
            370_0  COME_FROM           578  '578'
            370_1  COME_FROM           574  '574'
            370_2  COME_FROM           568  '568'
            370_3  COME_FROM           550  '550'
            370_4  COME_FROM           478  '478'
            370_5  COME_FROM           464  '464'
            370_6  COME_FROM           454  '454'
              370  FOR_ITER            582  'to 582'
              372  STORE_FAST               'mod_path'

 L. 859       374  LOAD_GLOBAL              os
              376  LOAD_ATTR                path
              378  LOAD_METHOD              join
              380  LOAD_FAST                'pth'
              382  LOAD_FAST                'mod_path'
              384  CALL_METHOD_2         2  '2 positional arguments'
              386  STORE_FAST               'this_py'

 L. 860       388  LOAD_GLOBAL              os
              390  LOAD_ATTR                path
              392  LOAD_METHOD              join
              394  LOAD_FAST                'pth'
              396  LOAD_FAST                'mod_path'
              398  LOAD_STR                 '__init__.py'
              400  CALL_METHOD_3         3  '3 positional arguments'
              402  STORE_FAST               'init_py'

 L. 861       404  LOAD_GLOBAL              os
              406  LOAD_ATTR                path
              408  LOAD_METHOD              isfile
              410  LOAD_FAST                'this_py'
              412  CALL_METHOD_1         1  '1 positional argument'
          414_416  POP_JUMP_IF_FALSE   444  'to 444'

 L. 862       418  LOAD_FAST                'mod_path'
              420  LOAD_METHOD              endswith
              422  LOAD_STR                 '.py'
              424  CALL_METHOD_1         1  '1 positional argument'
          426_428  POP_JUMP_IF_FALSE   444  'to 444'

 L. 863       430  LOAD_FAST                'mod_path'
              432  LOAD_CONST               None
              434  LOAD_CONST               -3
              436  BUILD_SLICE_2         2 
              438  BINARY_SUBSCR    
              440  STORE_FAST               'to_import'
              442  JUMP_FORWARD        468  'to 468'
            444_0  COME_FROM           426  '426'
            444_1  COME_FROM           414  '414'

 L. 864       444  LOAD_GLOBAL              os
              446  LOAD_ATTR                path
              448  LOAD_METHOD              isfile
              450  LOAD_FAST                'init_py'
              452  CALL_METHOD_1         1  '1 positional argument'
          454_456  POP_JUMP_IF_FALSE_BACK   370  'to 370'

 L. 865       458  LOAD_FAST                'mod_path'
              460  STORE_FAST               'to_import'
              462  JUMP_FORWARD        468  'to 468'

 L. 867   464_466  CONTINUE            370  'to 370'
            468_0  COME_FROM           462  '462'
            468_1  COME_FROM           442  '442'

 L. 868       468  LOAD_FAST                'to_import'
              470  LOAD_STR                 '__init__'
              472  COMPARE_OP               ==
          474_476  POP_JUMP_IF_FALSE   482  'to 482'

 L. 869   478_480  CONTINUE            370  'to 370'
            482_0  COME_FROM           474  '474'

 L. 871       482  SETUP_EXCEPT        552  'to 552'

 L. 872       484  LOAD_GLOBAL              sys
              486  LOAD_ATTR                stdout
              488  STORE_FAST               'old_stdout'

 L. 873       490  LOAD_GLOBAL              sys
              492  LOAD_ATTR                stderr
              494  STORE_FAST               'old_stderr'

 L. 874       496  SETUP_FINALLY       534  'to 534'

 L. 875       498  LOAD_FAST                'StringIO'
              500  CALL_FUNCTION_0       0  '0 positional arguments'
              502  LOAD_GLOBAL              sys
              504  STORE_ATTR               stdout

 L. 876       506  LOAD_FAST                'StringIO'
              508  CALL_FUNCTION_0       0  '0 positional arguments'
              510  LOAD_GLOBAL              sys
              512  STORE_ATTR               stderr

 L. 877       514  LOAD_GLOBAL              __import__
              516  LOAD_STR                 '%s.%s'
              518  LOAD_FAST                'name'
              520  LOAD_FAST                'to_import'
              522  BUILD_TUPLE_2         2 
              524  BINARY_MODULO    
              526  CALL_FUNCTION_1       1  '1 positional argument'
              528  POP_TOP          
              530  POP_BLOCK        
              532  LOAD_CONST               None
            534_0  COME_FROM_FINALLY   496  '496'

 L. 879       534  LOAD_FAST                'old_stdout'
              536  LOAD_GLOBAL              sys
              538  STORE_ATTR               stdout

 L. 880       540  LOAD_FAST                'old_stderr'
              542  LOAD_GLOBAL              sys
              544  STORE_ATTR               stderr
              546  END_FINALLY      
              548  POP_BLOCK        
              550  JUMP_BACK           370  'to 370'
            552_0  COME_FROM_EXCEPT    482  '482'

 L. 882       552  DUP_TOP          
              554  LOAD_GLOBAL              BaseException
              556  COMPARE_OP               exception-match
          558_560  POP_JUMP_IF_FALSE   576  'to 576'
              562  POP_TOP          
              564  POP_TOP          
              566  POP_TOP          

 L. 883   568_570  CONTINUE_LOOP       370  'to 370'
              572  POP_EXCEPT       
              574  JUMP_BACK           370  'to 370'
            576_0  COME_FROM           558  '558'
              576  END_FINALLY      
          578_580  JUMP_BACK           370  'to 370'
              582  POP_BLOCK        
            584_0  COME_FROM_LOOP      358  '358'
          584_586  JUMP_BACK           354  'to 354'
              588  POP_BLOCK        
            590_0  COME_FROM_LOOP      346  '346'
            590_1  COME_FROM           342  '342'
            590_2  COME_FROM           330  '330'

 L. 885       590  SETUP_LOOP          812  'to 812'
              592  LOAD_GLOBAL              _getmembers
              594  LOAD_FAST                'item'
              596  CALL_FUNCTION_1       1  '1 positional argument'
              598  GET_ITER         
            600_0  COME_FROM           806  '806'
            600_1  COME_FROM           780  '780'
            600_2  COME_FROM           742  '742'
            600_3  COME_FROM           736  '736'
              600  FOR_ITER            810  'to 810'
              602  UNPACK_SEQUENCE_2     2 
              604  STORE_FAST               'n'
              606  STORE_FAST               'v'

 L. 886       608  SETUP_EXCEPT        646  'to 646'

 L. 887       610  LOAD_GLOBAL              getattr
              612  LOAD_FAST                'v'
              614  LOAD_STR                 '__name__'
              616  LOAD_STR                 '%s.%s'
              618  LOAD_FAST                'name'
              620  LOAD_FAST                'n'
              622  BUILD_TUPLE_2         2 
              624  BINARY_MODULO    
              626  CALL_FUNCTION_3       3  '3 positional arguments'
              628  STORE_FAST               'item_name'

 L. 888       630  LOAD_GLOBAL              getattr
              632  LOAD_FAST                'v'
              634  LOAD_STR                 '__module__'
              636  LOAD_CONST               None
              638  CALL_FUNCTION_3       3  '3 positional arguments'
              640  STORE_FAST               'mod_name'
              642  POP_BLOCK        
              644  JUMP_FORWARD        684  'to 684'
            646_0  COME_FROM_EXCEPT    608  '608'

 L. 889       646  DUP_TOP          
              648  LOAD_GLOBAL              NameError
              650  COMPARE_OP               exception-match
          652_654  POP_JUMP_IF_FALSE   682  'to 682'
              656  POP_TOP          
              658  POP_TOP          
              660  POP_TOP          

 L. 892       662  LOAD_STR                 '%s.%s'
              664  LOAD_FAST                'name'
              666  LOAD_FAST                'n'
              668  BUILD_TUPLE_2         2 
              670  BINARY_MODULO    
              672  STORE_FAST               'item_name'

 L. 893       674  LOAD_CONST               None
              676  STORE_FAST               'mod_name'
              678  POP_EXCEPT       
              680  JUMP_FORWARD        684  'to 684'
            682_0  COME_FROM           652  '652'
              682  END_FINALLY      
            684_0  COME_FROM           680  '680'
            684_1  COME_FROM           644  '644'

 L. 894       684  LOAD_STR                 '.'
              686  LOAD_FAST                'item_name'
              688  COMPARE_OP               not-in
          690_692  POP_JUMP_IF_FALSE   712  'to 712'
              694  LOAD_FAST                'mod_name'
          696_698  POP_JUMP_IF_FALSE   712  'to 712'

 L. 895       700  LOAD_STR                 '%s.%s'
              702  LOAD_FAST                'mod_name'
              704  LOAD_FAST                'item_name'
              706  BUILD_TUPLE_2         2 
              708  BINARY_MODULO    
              710  STORE_FAST               'item_name'
            712_0  COME_FROM           696  '696'
            712_1  COME_FROM           690  '690'

 L. 897       712  LOAD_FAST                'item_name'
              714  LOAD_METHOD              startswith
              716  LOAD_FAST                'name'
              718  LOAD_STR                 '.'
              720  BINARY_ADD       
              722  CALL_METHOD_1         1  '1 positional argument'
          724_726  POP_JUMP_IF_TRUE    748  'to 748'

 L. 899       728  LOAD_GLOBAL              isinstance
              730  LOAD_FAST                'v'
              732  LOAD_GLOBAL              ufunc
              734  CALL_FUNCTION_2       2  '2 positional arguments'
          736_738  POP_JUMP_IF_FALSE_BACK   600  'to 600'

 L. 901       740  JUMP_FORWARD        746  'to 746'

 L. 903   742_744  CONTINUE            600  'to 600'
            746_0  COME_FROM           740  '740'
              746  JUMP_FORWARD        784  'to 784'
            748_0  COME_FROM           724  '724'

 L. 904       748  LOAD_FAST                'inspect'
              750  LOAD_METHOD              ismodule
              752  LOAD_FAST                'v'
              754  CALL_METHOD_1         1  '1 positional argument'
          756_758  POP_JUMP_IF_TRUE    784  'to 784'
              760  LOAD_FAST                '_all'
              762  LOAD_CONST               None
              764  COMPARE_OP               is
          766_768  POP_JUMP_IF_TRUE    784  'to 784'
              770  LOAD_FAST                'n'
              772  LOAD_FAST                '_all'
              774  COMPARE_OP               in
          776_778  POP_JUMP_IF_TRUE    784  'to 784'

 L. 905   780_782  CONTINUE            600  'to 600'
            784_0  COME_FROM           776  '776'
            784_1  COME_FROM           766  '766'
            784_2  COME_FROM           756  '756'
            784_3  COME_FROM           746  '746'

 L. 906       784  LOAD_FAST                'stack'
              786  LOAD_METHOD              append
              788  LOAD_STR                 '%s.%s'
              790  LOAD_FAST                'name'
              792  LOAD_FAST                'n'
              794  BUILD_TUPLE_2         2 
              796  BINARY_MODULO    
              798  LOAD_FAST                'v'
              800  BUILD_TUPLE_2         2 
              802  CALL_METHOD_1         1  '1 positional argument'
              804  POP_TOP          
          806_808  JUMP_BACK           600  'to 600'
              810  POP_BLOCK        
            812_0  COME_FROM_LOOP      590  '590'
              812  JUMP_FORWARD        894  'to 894'
            814_0  COME_FROM           282  '282'

 L. 907       814  LOAD_FAST                'inspect'
              816  LOAD_METHOD              isclass
              818  LOAD_FAST                'item'
              820  CALL_METHOD_1         1  '1 positional argument'
          822_824  POP_JUMP_IF_FALSE   878  'to 878'

 L. 908       826  LOAD_STR                 'class'
              828  STORE_FAST               'kind'

 L. 909       830  SETUP_LOOP          894  'to 894'
              832  LOAD_GLOBAL              _getmembers
              834  LOAD_FAST                'item'
              836  CALL_FUNCTION_1       1  '1 positional argument'
              838  GET_ITER         
            840_0  COME_FROM           870  '870'
              840  FOR_ITER            874  'to 874'
              842  UNPACK_SEQUENCE_2     2 
              844  STORE_FAST               'n'
              846  STORE_FAST               'v'

 L. 910       848  LOAD_FAST                'stack'
              850  LOAD_METHOD              append
              852  LOAD_STR                 '%s.%s'
              854  LOAD_FAST                'name'
              856  LOAD_FAST                'n'
              858  BUILD_TUPLE_2         2 
              860  BINARY_MODULO    
              862  LOAD_FAST                'v'
              864  BUILD_TUPLE_2         2 
              866  CALL_METHOD_1         1  '1 positional argument'
              868  POP_TOP          
          870_872  JUMP_BACK           840  'to 840'
              874  POP_BLOCK        
              876  JUMP_FORWARD        894  'to 894'
            878_0  COME_FROM           822  '822'

 L. 911       878  LOAD_GLOBAL              hasattr
              880  LOAD_FAST                'item'
              882  LOAD_STR                 '__call__'
              884  CALL_FUNCTION_2       2  '2 positional arguments'
          886_888  POP_JUMP_IF_FALSE   894  'to 894'

 L. 912       890  LOAD_STR                 'func'
              892  STORE_FAST               'kind'
            894_0  COME_FROM           886  '886'
            894_1  COME_FROM           876  '876'
            894_2  COME_FROM_LOOP      830  '830'
            894_3  COME_FROM           812  '812'

 L. 914       894  SETUP_EXCEPT        910  'to 910'

 L. 915       896  LOAD_FAST                'inspect'
              898  LOAD_METHOD              getdoc
              900  LOAD_FAST                'item'
              902  CALL_METHOD_1         1  '1 positional argument'
              904  STORE_FAST               'doc'
              906  POP_BLOCK        
              908  JUMP_FORWARD        936  'to 936'
            910_0  COME_FROM_EXCEPT    894  '894'

 L. 916       910  DUP_TOP          
              912  LOAD_GLOBAL              NameError
              914  COMPARE_OP               exception-match
          916_918  POP_JUMP_IF_FALSE   934  'to 934'
              920  POP_TOP          
              922  POP_TOP          
              924  POP_TOP          

 L. 918       926  LOAD_CONST               None
              928  STORE_FAST               'doc'
              930  POP_EXCEPT       
              932  JUMP_FORWARD        936  'to 936'
            934_0  COME_FROM           916  '916'
              934  END_FINALLY      
            936_0  COME_FROM           932  '932'
            936_1  COME_FROM           908  '908'

 L. 919       936  LOAD_FAST                'doc'
              938  LOAD_CONST               None
              940  COMPARE_OP               is-not
              942  POP_JUMP_IF_FALSE_BACK   216  'to 216'

 L. 920       944  LOAD_FAST                'doc'
              946  LOAD_FAST                'kind'
              948  LOAD_FAST                'index'
              950  BUILD_TUPLE_3         3 
              952  LOAD_FAST                'cache'
              954  LOAD_FAST                'name'
              956  STORE_SUBSCR     
              958  JUMP_BACK           216  'to 216'
            960_0  COME_FROM           218  '218'
              960  POP_BLOCK        
            962_0  COME_FROM_LOOP      212  '212'

 L. 922       962  LOAD_FAST                'cache'
              964  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CONTINUE' instruction at offset 464_466


def _getmembers(item):
    import inspect
    try:
        members = inspect.getmembers(item)
    except Exception:
        members = [(x, getattr(item, x)) for x in dir(item) if hasattr(item, x)]

    return members


def safe_eval(source):
    """
    Protected string evaluation.

    Evaluate a string containing a Python literal expression without
    allowing the execution of arbitrary non-literal code.

    Parameters
    ----------
    source : str
        The string to evaluate.

    Returns
    -------
    obj : object
       The result of evaluating `source`.

    Raises
    ------
    SyntaxError
        If the code has invalid Python syntax, or if it contains
        non-literal code.

    Examples
    --------
    >>> np.safe_eval('1')
    1
    >>> np.safe_eval('[1, 2, 3]')
    [1, 2, 3]
    >>> np.safe_eval('{"foo": ("bar", 10.0)}')
    {'foo': ('bar', 10.0)}

    >>> np.safe_eval('import os')
    Traceback (most recent call last):
      ...
    SyntaxError: invalid syntax

    >>> np.safe_eval('open("/home/user/.ssh/id_dsa").read()')
    Traceback (most recent call last):
      ...
    ValueError: malformed node or string: <_ast.Call object at 0x...>

    """
    import ast
    return ast.literal_eval(source)


def _median_nancheck(data, result, axis, out):
    """
    Utility function to check median result from data for NaN values at the end
    and return NaN in that case. Input result can also be a MaskedArray.

    Parameters
    ----------
    data : array
        Input data to median function
    result : Array or MaskedArray
        Result of median function
    axis : {int, sequence of int, None}, optional
        Axis or axes along which the median was computed.
    out : ndarray, optional
        Output array in which to place the result.
    Returns
    -------
    median : scalar or ndarray
        Median or NaN in axes which contained NaN in the input.
    """
    if data.size == 0:
        return result
    data = np.moveaxis(data, axis, -1)
    n = np.isnan(data[(Ellipsis, -1)])
    if np.ma.isMaskedArray(n):
        n = n.filled(False)
    if result.ndim == 0:
        if n == True:
            if out is not None:
                out[...] = data.dtype.type(np.nan)
                result = out
            else:
                result = data.dtype.type(np.nan)
    elif np.count_nonzero(n.ravel()) > 0:
        result[n] = np.nan
    return result