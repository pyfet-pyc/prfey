# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: numpy\lib\utils.py
import os, sys, textwrap, types, re, warnings
from numpy.core.numerictypes import issubclass_, issubsctype, issubdtype
from numpy.core.overrides import set_module
from numpy.core import ndarray, ufunc, asarray
import numpy as np
from numpy.compat import getargspec, formatargspec
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
            else:
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
                        else:
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
    else:
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

    return (
     a_low, a_high)


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
    else:
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
        else:
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
            else:
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
    else:
        return newstr


_namedict = None
_dictlist = None

def _makenamedict(module='numpy'):
    module = __import__(module, globals(), locals(), [])
    thedict = {module.__name__: module.__dict__}
    dictlist = [module.__name__]
    totraverse = [module.__dict__]
    while True:
        if len(totraverse) == 0:
            pass
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
    elif inspect.isfunction(object):
        name = object.__name__
        arguments = formatargspec(*getargspec(object))
        if len(name + arguments) > maxwidth:
            argstr = _split_line(name, arguments, maxwidth)
        else:
            argstr = name + arguments
        print((' ' + argstr + '\n'), file=output)
        print((inspect.getdoc(object)), file=output)
    elif inspect.isclass(object):
        name = object.__name__
        arguments = '()'
        try:
            if hasattr(object, '__init__'):
                arguments = formatargspec(*getargspec(object.__init__.__func__))
                arglist = arguments.split(', ')
                if len(arglist) > 1:
                    arglist[1] = '(' + arglist[1]
                    arguments = ', '.join(arglist[1:])
        except Exception:
            pass
        else:
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
            if methods != []:
                print('\n\nMethods:\n', file=output)
                for meth in methods:
                    if meth[0] == '_':
                        pass
                    else:
                        thisobj = getattr(object, meth, None)
                        if thisobj is not None:
                            methstr, other = pydoc.splitdoc(inspect.getdoc(thisobj) or 'None')
                        print(('  %s  --  %s' % (meth, methstr)), file=output)

    elif inspect.ismethod(object):
        name = object.__name__
        arguments = formatargspec(*getargspec(object.__func__))
        arglist = arguments.split(', ')
        if len(arglist) > 1:
            arglist[1] = '(' + arglist[1]
            arguments = ', '.join(arglist[1:])
        else:
            arguments = '()'
        if len(name + arguments) > maxwidth:
            argstr = _split_line(name, arguments, maxwidth)
        else:
            argstr = name + arguments
        print((' ' + argstr + '\n'), file=output)
        print((inspect.getdoc(object)), file=output)
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
            pass
        else:
            doc = docstring.lower()
            if all((w in doc for w in whats)):
                found.append(name)
    else:
        kind_relevance = {'func':1000,  'class':1000,  'module':-1000, 
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
            else:
                help_text.append('%s\n    %s' % (name, first_doc))
        else:
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

 L. 838         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              inspect
                6  STORE_FAST               'inspect'

 L. 840         8  LOAD_CONST               0
               10  LOAD_CONST               ('StringIO',)
               12  IMPORT_NAME              io
               14  IMPORT_FROM              StringIO
               16  STORE_FAST               'StringIO'
               18  POP_TOP          

 L. 842        20  LOAD_FAST                'module'
               22  LOAD_CONST               None
               24  COMPARE_OP               is
               26  POP_JUMP_IF_FALSE    32  'to 32'

 L. 843        28  LOAD_STR                 'numpy'
               30  STORE_FAST               'module'
             32_0  COME_FROM            26  '26'

 L. 845        32  LOAD_GLOBAL              isinstance
               34  LOAD_FAST                'module'
               36  LOAD_GLOBAL              str
               38  CALL_FUNCTION_2       2  ''
               40  POP_JUMP_IF_FALSE    92  'to 92'

 L. 846        42  SETUP_FINALLY        56  'to 56'

 L. 847        44  LOAD_GLOBAL              __import__
               46  LOAD_FAST                'module'
               48  CALL_FUNCTION_1       1  ''
               50  POP_TOP          
               52  POP_BLOCK        
               54  JUMP_FORWARD         80  'to 80'
             56_0  COME_FROM_FINALLY    42  '42'

 L. 848        56  DUP_TOP          
               58  LOAD_GLOBAL              ImportError
               60  COMPARE_OP               exception-match
               62  POP_JUMP_IF_FALSE    78  'to 78'
               64  POP_TOP          
               66  POP_TOP          
               68  POP_TOP          

 L. 849        70  BUILD_MAP_0           0 
               72  ROT_FOUR         
               74  POP_EXCEPT       
               76  RETURN_VALUE     
             78_0  COME_FROM            62  '62'
               78  END_FINALLY      
             80_0  COME_FROM            54  '54'

 L. 850        80  LOAD_GLOBAL              sys
               82  LOAD_ATTR                modules
               84  LOAD_FAST                'module'
               86  BINARY_SUBSCR    
               88  STORE_FAST               'module'
               90  JUMP_FORWARD        148  'to 148'
             92_0  COME_FROM            40  '40'

 L. 851        92  LOAD_GLOBAL              isinstance
               94  LOAD_FAST                'module'
               96  LOAD_GLOBAL              list
               98  CALL_FUNCTION_2       2  ''
              100  POP_JUMP_IF_TRUE    112  'to 112'
              102  LOAD_GLOBAL              isinstance
              104  LOAD_FAST                'module'
              106  LOAD_GLOBAL              tuple
              108  CALL_FUNCTION_2       2  ''
              110  POP_JUMP_IF_FALSE   148  'to 148'
            112_0  COME_FROM           100  '100'

 L. 852       112  BUILD_MAP_0           0 
              114  STORE_FAST               'cache'

 L. 853       116  LOAD_FAST                'module'
              118  GET_ITER         
            120_0  COME_FROM           142  '142'
              120  FOR_ITER            144  'to 144'
              122  STORE_FAST               'mod'

 L. 854       124  LOAD_FAST                'cache'
              126  LOAD_METHOD              update
              128  LOAD_GLOBAL              _lookfor_generate_cache
              130  LOAD_FAST                'mod'
              132  LOAD_FAST                'import_modules'

 L. 855       134  LOAD_FAST                'regenerate'

 L. 854       136  CALL_FUNCTION_3       3  ''
              138  CALL_METHOD_1         1  ''
              140  POP_TOP          
              142  JUMP_BACK           120  'to 120'
            144_0  COME_FROM           120  '120'

 L. 856       144  LOAD_FAST                'cache'
              146  RETURN_VALUE     
            148_0  COME_FROM           110  '110'
            148_1  COME_FROM            90  '90'

 L. 858       148  LOAD_GLOBAL              id
              150  LOAD_FAST                'module'
              152  CALL_FUNCTION_1       1  ''
              154  LOAD_GLOBAL              _lookfor_caches
              156  COMPARE_OP               in
              158  POP_JUMP_IF_FALSE   176  'to 176'
              160  LOAD_FAST                'regenerate'
              162  POP_JUMP_IF_TRUE    176  'to 176'

 L. 859       164  LOAD_GLOBAL              _lookfor_caches
              166  LOAD_GLOBAL              id
              168  LOAD_FAST                'module'
              170  CALL_FUNCTION_1       1  ''
              172  BINARY_SUBSCR    
              174  RETURN_VALUE     
            176_0  COME_FROM           162  '162'
            176_1  COME_FROM           158  '158'

 L. 862       176  BUILD_MAP_0           0 
              178  STORE_FAST               'cache'

 L. 863       180  LOAD_FAST                'cache'
              182  LOAD_GLOBAL              _lookfor_caches
              184  LOAD_GLOBAL              id
              186  LOAD_FAST                'module'
              188  CALL_FUNCTION_1       1  ''
              190  STORE_SUBSCR     

 L. 864       192  BUILD_MAP_0           0 
              194  STORE_FAST               'seen'

 L. 865       196  LOAD_CONST               0
              198  STORE_FAST               'index'

 L. 866       200  LOAD_FAST                'module'
              202  LOAD_ATTR                __name__
              204  LOAD_FAST                'module'
              206  BUILD_TUPLE_2         2 
              208  BUILD_LIST_1          1 
              210  STORE_FAST               'stack'
            212_0  COME_FROM           940  '940'
            212_1  COME_FROM           924  '924'
            212_2  COME_FROM           244  '244'

 L. 867       212  LOAD_FAST                'stack'
          214_216  POP_JUMP_IF_FALSE   942  'to 942'

 L. 868       218  LOAD_FAST                'stack'
              220  LOAD_METHOD              pop
              222  LOAD_CONST               0
              224  CALL_METHOD_1         1  ''
              226  UNPACK_SEQUENCE_2     2 
              228  STORE_FAST               'name'
              230  STORE_FAST               'item'

 L. 869       232  LOAD_GLOBAL              id
              234  LOAD_FAST                'item'
              236  CALL_FUNCTION_1       1  ''
              238  LOAD_FAST                'seen'
              240  COMPARE_OP               in
              242  POP_JUMP_IF_FALSE   246  'to 246'

 L. 870       244  JUMP_BACK           212  'to 212'
            246_0  COME_FROM           242  '242'

 L. 871       246  LOAD_CONST               True
              248  LOAD_FAST                'seen'
              250  LOAD_GLOBAL              id
              252  LOAD_FAST                'item'
              254  CALL_FUNCTION_1       1  ''
              256  STORE_SUBSCR     

 L. 873       258  LOAD_FAST                'index'
              260  LOAD_CONST               1
              262  INPLACE_ADD      
              264  STORE_FAST               'index'

 L. 874       266  LOAD_STR                 'object'
              268  STORE_FAST               'kind'

 L. 876       270  LOAD_FAST                'inspect'
              272  LOAD_METHOD              ismodule
              274  LOAD_FAST                'item'
              276  CALL_METHOD_1         1  ''
          278_280  POP_JUMP_IF_FALSE   800  'to 800'

 L. 877       282  LOAD_STR                 'module'
              284  STORE_FAST               'kind'

 L. 878       286  SETUP_FINALLY       298  'to 298'

 L. 879       288  LOAD_FAST                'item'
              290  LOAD_ATTR                __all__
              292  STORE_FAST               '_all'
              294  POP_BLOCK        
              296  JUMP_FORWARD        324  'to 324'
            298_0  COME_FROM_FINALLY   286  '286'

 L. 880       298  DUP_TOP          
              300  LOAD_GLOBAL              AttributeError
              302  COMPARE_OP               exception-match
          304_306  POP_JUMP_IF_FALSE   322  'to 322'
              308  POP_TOP          
              310  POP_TOP          
              312  POP_TOP          

 L. 881       314  LOAD_CONST               None
              316  STORE_FAST               '_all'
              318  POP_EXCEPT       
              320  JUMP_FORWARD        324  'to 324'
            322_0  COME_FROM           304  '304'
              322  END_FINALLY      
            324_0  COME_FROM           320  '320'
            324_1  COME_FROM           296  '296'

 L. 884       324  LOAD_FAST                'import_modules'
          326_328  POP_JUMP_IF_FALSE   580  'to 580'
              330  LOAD_GLOBAL              hasattr
              332  LOAD_FAST                'item'
              334  LOAD_STR                 '__path__'
              336  CALL_FUNCTION_2       2  ''
          338_340  POP_JUMP_IF_FALSE   580  'to 580'

 L. 885       342  LOAD_FAST                'item'
              344  LOAD_ATTR                __path__
              346  GET_ITER         
            348_0  COME_FROM           576  '576'
              348  FOR_ITER            580  'to 580'
              350  STORE_FAST               'pth'

 L. 886       352  LOAD_GLOBAL              os
              354  LOAD_METHOD              listdir
              356  LOAD_FAST                'pth'
              358  CALL_METHOD_1         1  ''
              360  GET_ITER         
            362_0  COME_FROM           572  '572'
            362_1  COME_FROM           568  '568'
            362_2  COME_FROM           562  '562'
            362_3  COME_FROM           542  '542'
            362_4  COME_FROM           470  '470'
            362_5  COME_FROM           456  '456'
            362_6  COME_FROM           446  '446'
              362  FOR_ITER            576  'to 576'
              364  STORE_FAST               'mod_path'

 L. 887       366  LOAD_GLOBAL              os
              368  LOAD_ATTR                path
              370  LOAD_METHOD              join
              372  LOAD_FAST                'pth'
              374  LOAD_FAST                'mod_path'
              376  CALL_METHOD_2         2  ''
              378  STORE_FAST               'this_py'

 L. 888       380  LOAD_GLOBAL              os
              382  LOAD_ATTR                path
              384  LOAD_METHOD              join
              386  LOAD_FAST                'pth'
              388  LOAD_FAST                'mod_path'
              390  LOAD_STR                 '__init__.py'
              392  CALL_METHOD_3         3  ''
              394  STORE_FAST               'init_py'

 L. 889       396  LOAD_GLOBAL              os
              398  LOAD_ATTR                path
              400  LOAD_METHOD              isfile
              402  LOAD_FAST                'this_py'
              404  CALL_METHOD_1         1  ''
          406_408  POP_JUMP_IF_FALSE   436  'to 436'

 L. 890       410  LOAD_FAST                'mod_path'
              412  LOAD_METHOD              endswith
              414  LOAD_STR                 '.py'
              416  CALL_METHOD_1         1  ''

 L. 889   418_420  POP_JUMP_IF_FALSE   436  'to 436'

 L. 891       422  LOAD_FAST                'mod_path'
              424  LOAD_CONST               None
              426  LOAD_CONST               -3
              428  BUILD_SLICE_2         2 
              430  BINARY_SUBSCR    
              432  STORE_FAST               'to_import'
              434  JUMP_FORWARD        460  'to 460'
            436_0  COME_FROM           418  '418'
            436_1  COME_FROM           406  '406'

 L. 892       436  LOAD_GLOBAL              os
              438  LOAD_ATTR                path
              440  LOAD_METHOD              isfile
              442  LOAD_FAST                'init_py'
              444  CALL_METHOD_1         1  ''
          446_448  POP_JUMP_IF_FALSE_BACK   362  'to 362'

 L. 893       450  LOAD_FAST                'mod_path'
              452  STORE_FAST               'to_import'
              454  JUMP_FORWARD        460  'to 460'

 L. 895   456_458  JUMP_BACK           362  'to 362'
            460_0  COME_FROM           454  '454'
            460_1  COME_FROM           434  '434'

 L. 896       460  LOAD_FAST                'to_import'
              462  LOAD_STR                 '__init__'
              464  COMPARE_OP               ==
          466_468  POP_JUMP_IF_FALSE   474  'to 474'

 L. 897   470_472  JUMP_BACK           362  'to 362'
            474_0  COME_FROM           466  '466'

 L. 899       474  SETUP_FINALLY       544  'to 544'

 L. 900       476  LOAD_GLOBAL              sys
              478  LOAD_ATTR                stdout
              480  STORE_FAST               'old_stdout'

 L. 901       482  LOAD_GLOBAL              sys
              484  LOAD_ATTR                stderr
              486  STORE_FAST               'old_stderr'

 L. 902       488  SETUP_FINALLY       526  'to 526'

 L. 903       490  LOAD_FAST                'StringIO'
              492  CALL_FUNCTION_0       0  ''
              494  LOAD_GLOBAL              sys
              496  STORE_ATTR               stdout

 L. 904       498  LOAD_FAST                'StringIO'
              500  CALL_FUNCTION_0       0  ''
              502  LOAD_GLOBAL              sys
              504  STORE_ATTR               stderr

 L. 905       506  LOAD_GLOBAL              __import__
              508  LOAD_STR                 '%s.%s'
              510  LOAD_FAST                'name'
              512  LOAD_FAST                'to_import'
              514  BUILD_TUPLE_2         2 
              516  BINARY_MODULO    
              518  CALL_FUNCTION_1       1  ''
              520  POP_TOP          
              522  POP_BLOCK        
              524  BEGIN_FINALLY    
            526_0  COME_FROM_FINALLY   488  '488'

 L. 907       526  LOAD_FAST                'old_stdout'
              528  LOAD_GLOBAL              sys
              530  STORE_ATTR               stdout

 L. 908       532  LOAD_FAST                'old_stderr'
              534  LOAD_GLOBAL              sys
              536  STORE_ATTR               stderr
              538  END_FINALLY      
              540  POP_BLOCK        
              542  JUMP_BACK           362  'to 362'
            544_0  COME_FROM_FINALLY   474  '474'

 L. 910       544  DUP_TOP          
              546  LOAD_GLOBAL              BaseException
              548  COMPARE_OP               exception-match
          550_552  POP_JUMP_IF_FALSE   570  'to 570'
              554  POP_TOP          
              556  POP_TOP          
              558  POP_TOP          

 L. 911       560  POP_EXCEPT       
          562_564  JUMP_BACK           362  'to 362'
              566  POP_EXCEPT       
              568  JUMP_BACK           362  'to 362'
            570_0  COME_FROM           550  '550'
              570  END_FINALLY      
          572_574  JUMP_BACK           362  'to 362'
            576_0  COME_FROM           362  '362'
          576_578  JUMP_BACK           348  'to 348'
            580_0  COME_FROM           348  '348'
            580_1  COME_FROM           338  '338'
            580_2  COME_FROM           326  '326'

 L. 913       580  LOAD_GLOBAL              _getmembers
              582  LOAD_FAST                'item'
              584  CALL_FUNCTION_1       1  ''
              586  GET_ITER         
            588_0  COME_FROM           794  '794'
            588_1  COME_FROM           768  '768'
            588_2  COME_FROM           730  '730'
            588_3  COME_FROM           724  '724'
              588  FOR_ITER            798  'to 798'
              590  UNPACK_SEQUENCE_2     2 
              592  STORE_FAST               'n'
              594  STORE_FAST               'v'

 L. 914       596  SETUP_FINALLY       634  'to 634'

 L. 915       598  LOAD_GLOBAL              getattr
              600  LOAD_FAST                'v'
              602  LOAD_STR                 '__name__'
              604  LOAD_STR                 '%s.%s'
              606  LOAD_FAST                'name'
              608  LOAD_FAST                'n'
              610  BUILD_TUPLE_2         2 
              612  BINARY_MODULO    
              614  CALL_FUNCTION_3       3  ''
              616  STORE_FAST               'item_name'

 L. 916       618  LOAD_GLOBAL              getattr
              620  LOAD_FAST                'v'
              622  LOAD_STR                 '__module__'
              624  LOAD_CONST               None
              626  CALL_FUNCTION_3       3  ''
              628  STORE_FAST               'mod_name'
              630  POP_BLOCK        
              632  JUMP_FORWARD        672  'to 672'
            634_0  COME_FROM_FINALLY   596  '596'

 L. 917       634  DUP_TOP          
              636  LOAD_GLOBAL              NameError
              638  COMPARE_OP               exception-match
          640_642  POP_JUMP_IF_FALSE   670  'to 670'
              644  POP_TOP          
              646  POP_TOP          
              648  POP_TOP          

 L. 920       650  LOAD_STR                 '%s.%s'
              652  LOAD_FAST                'name'
              654  LOAD_FAST                'n'
              656  BUILD_TUPLE_2         2 
              658  BINARY_MODULO    
              660  STORE_FAST               'item_name'

 L. 921       662  LOAD_CONST               None
              664  STORE_FAST               'mod_name'
              666  POP_EXCEPT       
              668  JUMP_FORWARD        672  'to 672'
            670_0  COME_FROM           640  '640'
              670  END_FINALLY      
            672_0  COME_FROM           668  '668'
            672_1  COME_FROM           632  '632'

 L. 922       672  LOAD_STR                 '.'
              674  LOAD_FAST                'item_name'
              676  COMPARE_OP               not-in
          678_680  POP_JUMP_IF_FALSE   700  'to 700'
              682  LOAD_FAST                'mod_name'
          684_686  POP_JUMP_IF_FALSE   700  'to 700'

 L. 923       688  LOAD_STR                 '%s.%s'
              690  LOAD_FAST                'mod_name'
              692  LOAD_FAST                'item_name'
              694  BUILD_TUPLE_2         2 
              696  BINARY_MODULO    
              698  STORE_FAST               'item_name'
            700_0  COME_FROM           684  '684'
            700_1  COME_FROM           678  '678'

 L. 925       700  LOAD_FAST                'item_name'
              702  LOAD_METHOD              startswith
              704  LOAD_FAST                'name'
              706  LOAD_STR                 '.'
              708  BINARY_ADD       
              710  CALL_METHOD_1         1  ''
          712_714  POP_JUMP_IF_TRUE    736  'to 736'

 L. 927       716  LOAD_GLOBAL              isinstance
              718  LOAD_FAST                'v'
              720  LOAD_GLOBAL              ufunc
              722  CALL_FUNCTION_2       2  ''
          724_726  POP_JUMP_IF_FALSE_BACK   588  'to 588'

 L. 929       728  JUMP_FORWARD        734  'to 734'

 L. 931   730_732  JUMP_BACK           588  'to 588'
            734_0  COME_FROM           728  '728'
              734  BREAK_LOOP          772  'to 772'
            736_0  COME_FROM           712  '712'

 L. 932       736  LOAD_FAST                'inspect'
              738  LOAD_METHOD              ismodule
              740  LOAD_FAST                'v'
              742  CALL_METHOD_1         1  ''
          744_746  POP_JUMP_IF_TRUE    772  'to 772'
              748  LOAD_FAST                '_all'
              750  LOAD_CONST               None
              752  COMPARE_OP               is
          754_756  POP_JUMP_IF_TRUE    772  'to 772'
              758  LOAD_FAST                'n'
              760  LOAD_FAST                '_all'
              762  COMPARE_OP               in
          764_766  POP_JUMP_IF_TRUE    772  'to 772'

 L. 933   768_770  JUMP_BACK           588  'to 588'
            772_0  COME_FROM           764  '764'
            772_1  COME_FROM           754  '754'
            772_2  COME_FROM           744  '744'
            772_3  COME_FROM           734  '734'

 L. 934       772  LOAD_FAST                'stack'
              774  LOAD_METHOD              append
              776  LOAD_STR                 '%s.%s'
              778  LOAD_FAST                'name'
              780  LOAD_FAST                'n'
              782  BUILD_TUPLE_2         2 
              784  BINARY_MODULO    
              786  LOAD_FAST                'v'
              788  BUILD_TUPLE_2         2 
              790  CALL_METHOD_1         1  ''
              792  POP_TOP          
          794_796  JUMP_BACK           588  'to 588'
            798_0  COME_FROM           588  '588'
              798  JUMP_FORWARD        876  'to 876'
            800_0  COME_FROM           278  '278'

 L. 935       800  LOAD_FAST                'inspect'
              802  LOAD_METHOD              isclass
              804  LOAD_FAST                'item'
              806  CALL_METHOD_1         1  ''
          808_810  POP_JUMP_IF_FALSE   860  'to 860'

 L. 936       812  LOAD_STR                 'class'
              814  STORE_FAST               'kind'

 L. 937       816  LOAD_GLOBAL              _getmembers
              818  LOAD_FAST                'item'
              820  CALL_FUNCTION_1       1  ''
              822  GET_ITER         
            824_0  COME_FROM           854  '854'
              824  FOR_ITER            858  'to 858'
              826  UNPACK_SEQUENCE_2     2 
              828  STORE_FAST               'n'
              830  STORE_FAST               'v'

 L. 938       832  LOAD_FAST                'stack'
              834  LOAD_METHOD              append
              836  LOAD_STR                 '%s.%s'
              838  LOAD_FAST                'name'
              840  LOAD_FAST                'n'
              842  BUILD_TUPLE_2         2 
              844  BINARY_MODULO    
              846  LOAD_FAST                'v'
              848  BUILD_TUPLE_2         2 
              850  CALL_METHOD_1         1  ''
              852  POP_TOP          
          854_856  JUMP_BACK           824  'to 824'
            858_0  COME_FROM           824  '824'
              858  JUMP_FORWARD        876  'to 876'
            860_0  COME_FROM           808  '808'

 L. 939       860  LOAD_GLOBAL              hasattr
              862  LOAD_FAST                'item'
              864  LOAD_STR                 '__call__'
              866  CALL_FUNCTION_2       2  ''
          868_870  POP_JUMP_IF_FALSE   876  'to 876'

 L. 940       872  LOAD_STR                 'func'
              874  STORE_FAST               'kind'
            876_0  COME_FROM           868  '868'
            876_1  COME_FROM           858  '858'
            876_2  COME_FROM           798  '798'

 L. 942       876  SETUP_FINALLY       892  'to 892'

 L. 943       878  LOAD_FAST                'inspect'
              880  LOAD_METHOD              getdoc
              882  LOAD_FAST                'item'
              884  CALL_METHOD_1         1  ''
              886  STORE_FAST               'doc'
              888  POP_BLOCK        
              890  JUMP_FORWARD        918  'to 918'
            892_0  COME_FROM_FINALLY   876  '876'

 L. 944       892  DUP_TOP          
              894  LOAD_GLOBAL              NameError
              896  COMPARE_OP               exception-match
          898_900  POP_JUMP_IF_FALSE   916  'to 916'
              902  POP_TOP          
              904  POP_TOP          
              906  POP_TOP          

 L. 946       908  LOAD_CONST               None
              910  STORE_FAST               'doc'
              912  POP_EXCEPT       
              914  JUMP_FORWARD        918  'to 918'
            916_0  COME_FROM           898  '898'
              916  END_FINALLY      
            918_0  COME_FROM           914  '914'
            918_1  COME_FROM           890  '890'

 L. 947       918  LOAD_FAST                'doc'
              920  LOAD_CONST               None
              922  COMPARE_OP               is-not
              924  POP_JUMP_IF_FALSE_BACK   212  'to 212'

 L. 948       926  LOAD_FAST                'doc'
              928  LOAD_FAST                'kind'
              930  LOAD_FAST                'index'
              932  BUILD_TUPLE_3         3 
              934  LOAD_FAST                'cache'
              936  LOAD_FAST                'name'
              938  STORE_SUBSCR     
              940  JUMP_BACK           212  'to 212'
            942_0  COME_FROM           214  '214'

 L. 950       942  LOAD_FAST                'cache'
              944  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 456_458


def _getmembers(item):
    import inspect
    try:
        members = inspect.getmembers(item)
    except Exception:
        members = [(
         x, getattr(item, x)) for x in dir(item) if hasattr(item, x)]
    else:
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