# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\numpy\testing\_private\parameterized.py
"""
tl;dr: all code code is licensed under simplified BSD, unless stated otherwise.

Unless stated otherwise in the source files, all code is copyright 2010 David
Wolever <david@wolever.net>. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY <COPYRIGHT HOLDER> ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
EVENT SHALL <COPYRIGHT HOLDER> OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies,
either expressed or implied, of David Wolever.

"""
import re, sys, inspect, warnings
from functools import wraps
from types import MethodType
from collections import namedtuple
try:
    from collections import OrderedDict as MaybeOrderedDict
except ImportError:
    MaybeOrderedDict = dict
else:
    from unittest import TestCase
    PY2 = sys.version_info[0] == 2
    if PY2:
        from types import InstanceType
        lzip = zip
        text_type = unicode
        bytes_type = str
        string_types = (basestring,)

        def make_method(func, instance, type):
            return MethodType(func, instance, type)


    else:

        class InstanceType:
            pass


        lzip = lambda *a: list(zip(*a))
        text_type = str
        string_types = (str,)
        bytes_type = bytes

        def make_method(func, instance, type):
            if instance is None:
                return func
            return MethodType(func, instance)


    _param = namedtuple('param', 'args kwargs')

    class param(_param):
        __doc__ = ' Represents a single parameter to a test case.\n\n        For example::\n\n            >>> p = param("foo", bar=16)\n            >>> p\n            param("foo", bar=16)\n            >>> p.args\n            (\'foo\', )\n            >>> p.kwargs\n            {\'bar\': 16}\n\n        Intended to be used as an argument to ``@parameterized``::\n\n            @parameterized([\n                param("foo", bar=16),\n            ])\n            def test_stuff(foo, bar=16):\n                pass\n        '

        def __new__(cls, *args, **kwargs):
            return _param.__new__(cls, args, kwargs)

        @classmethod
        def explicit(cls, args=None, kwargs=None):
            """ Creates a ``param`` by explicitly specifying ``args`` and
            ``kwargs``::

                >>> param.explicit([1,2,3])
                param(*(1, 2, 3))
                >>> param.explicit(kwargs={"foo": 42})
                param(*(), **{"foo": "42"})
            """
            args = args or ()
            kwargs = kwargs or {}
            return cls(*args, **kwargs)

        @classmethod
        def from_decorator(cls, args):
            """ Returns an instance of ``param()`` for ``@parameterized`` argument
            ``args``::

                >>> param.from_decorator((42, ))
                param(args=(42, ), kwargs={})
                >>> param.from_decorator("foo")
                param(args=("foo", ), kwargs={})
            """
            if isinstance(args, param):
                return args
            if isinstance(args, string_types):
                args = (
                 args,)
            try:
                return cls(*args)
                    except TypeError as e:
                try:
                    if 'after * must be' not in str(e):
                        raise
                    raise TypeError("Parameters must be tuples, but %r is not (hint: use '(%r, )')" % (
                     args, args))
                finally:
                    e = None
                    del e

        def __repr__(self):
            return 'param(*%r, **%r)' % self


    class QuietOrderedDict(MaybeOrderedDict):
        __doc__ = ' When OrderedDict is available, use it to make sure that the kwargs in\n        doc strings are consistently ordered. '
        __str__ = dict.__str__
        __repr__ = dict.__repr__


    def parameterized_argument_value_pairs(func, p):
        """Return tuples of parameterized arguments and their values.

        This is useful if you are writing your own doc_func
        function and need to know the values for each parameter name::

            >>> def func(a, foo=None, bar=42, **kwargs): pass
            >>> p = param(1, foo=7, extra=99)
            >>> parameterized_argument_value_pairs(func, p)
            [("a", 1), ("foo", 7), ("bar", 42), ("**kwargs", {"extra": 99})]

        If the function's first argument is named ``self`` then it will be
        ignored::

            >>> def func(self, a): pass
            >>> p = param(1)
            >>> parameterized_argument_value_pairs(func, p)
            [("a", 1)]

        Additionally, empty ``*args`` or ``**kwargs`` will be ignored::

            >>> def func(foo, *args): pass
            >>> p = param(1)
            >>> parameterized_argument_value_pairs(func, p)
            [("foo", 1)]
            >>> p = param(1, 16)
            >>> parameterized_argument_value_pairs(func, p)
            [("foo", 1), ("*args", (16, ))]
    """
        argspec = inspect.getargspec(func)
        arg_offset = 1 if argspec.args[:1] == ['self'] else 0
        named_args = argspec.args[arg_offset:]
        result = lzip(named_args, p.args)
        named_args = argspec.args[len(result) + arg_offset:]
        varargs = p.args[len(result):]
        result.extend([(
         name, p.kwargs.get(name, default)) for name, default in zip(named_args, argspec.defaults or [])])
        seen_arg_names = {n for n, _ in result}
        keywords = QuietOrderedDict(sorted([(
         name, p.kwargs[name]) for name in p.kwargs if name not in seen_arg_names]))
        if varargs:
            result.append(('*%s' % (argspec.varargs,), tuple(varargs)))
        if keywords:
            result.append(('**%s' % (argspec.keywords,), keywords))
        return result


    def short_repr(x, n=64):
        """ A shortened repr of ``x`` which is guaranteed to be ``unicode``::

            >>> short_repr("foo")
            u"foo"
            >>> short_repr("123456789", n=4)
            u"12...89"
    """
        x_repr = repr(x)
        if isinstance(x_repr, bytes_type):
            try:
                x_repr = text_type(x_repr, 'utf-8')
            except UnicodeDecodeError:
                x_repr = text_type(x_repr, 'latin1')

        if len(x_repr) > n:
            x_repr = x_repr[:n // 2] + '...' + x_repr[len(x_repr) - n // 2:]
        return x_repr


    def default_doc_func(func, num, p):
        if func.__doc__ is None:
            return
        all_args_with_values = parameterized_argument_value_pairs(func, p)
        descs = ['%s=%s' % (n, short_repr(v)) for n, v in all_args_with_values]
        first, nl, rest = func.__doc__.lstrip().partition('\n')
        suffix = ''
        if first.endswith('.'):
            suffix = '.'
            first = first[:-1]
        args = '%s[with %s]' % (len(first) and ' ' or '', ', '.join(descs))
        return ''.join([first.rstrip(), args, suffix, nl, rest])


    def default_name_func(func, num, p):
        base_name = func.__name__
        name_suffix = '_%s' % (num,)
        if len(p.args) > 0:
            if isinstance(p.args[0], string_types):
                name_suffix += '_' + parameterized.to_safe_name(p.args[0])
        return base_name + name_suffix


    _test_runner_override = 'nose'
    _test_runner_guess = False
    _test_runners = set(['unittest', 'unittest2', 'nose', 'nose2', 'pytest'])
    _test_runner_aliases = {'_pytest': 'pytest'}

    def set_test_runner(name):
        global _test_runner_override
        if name not in _test_runners:
            raise TypeError('Invalid test runner: %r (must be one of: %s)' % (
             name, ', '.join(_test_runners)))
        _test_runner_override = name


    def detect_runner--- This code section failed: ---

 L. 276         0  LOAD_GLOBAL              _test_runner_override
                2  LOAD_CONST               None
                4  COMPARE_OP               is-not
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 277         8  LOAD_GLOBAL              _test_runner_override
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L. 279        12  LOAD_GLOBAL              _test_runner_guess
               14  LOAD_CONST               False
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE   130  'to 130'

 L. 280        20  LOAD_GLOBAL              inspect
               22  LOAD_METHOD              stack
               24  CALL_METHOD_0         0  ''
               26  STORE_FAST               'stack'

 L. 281        28  LOAD_GLOBAL              reversed
               30  LOAD_FAST                'stack'
               32  CALL_FUNCTION_1       1  ''
               34  GET_ITER         
             36_0  COME_FROM           114  '114'
               36  FOR_ITER            126  'to 126'
               38  STORE_FAST               'record'

 L. 282        40  LOAD_FAST                'record'
               42  LOAD_CONST               0
               44  BINARY_SUBSCR    
               46  STORE_FAST               'frame'

 L. 283        48  LOAD_FAST                'frame'
               50  LOAD_ATTR                f_globals
               52  LOAD_METHOD              get
               54  LOAD_STR                 '__name__'
               56  CALL_METHOD_1         1  ''
               58  LOAD_METHOD              partition
               60  LOAD_STR                 '.'
               62  CALL_METHOD_1         1  ''
               64  LOAD_CONST               0
               66  BINARY_SUBSCR    
               68  STORE_FAST               'module'

 L. 284        70  LOAD_FAST                'module'
               72  LOAD_GLOBAL              _test_runner_aliases
               74  COMPARE_OP               in
               76  POP_JUMP_IF_FALSE    86  'to 86'

 L. 285        78  LOAD_GLOBAL              _test_runner_aliases
               80  LOAD_FAST                'module'
               82  BINARY_SUBSCR    
               84  STORE_FAST               'module'
             86_0  COME_FROM            76  '76'

 L. 286        86  LOAD_FAST                'module'
               88  LOAD_GLOBAL              _test_runners
               90  COMPARE_OP               in
               92  POP_JUMP_IF_FALSE   102  'to 102'

 L. 287        94  LOAD_FAST                'module'
               96  STORE_GLOBAL             _test_runner_guess

 L. 288        98  POP_TOP          
              100  JUMP_ABSOLUTE       130  'to 130'
            102_0  COME_FROM            92  '92'

 L. 289       102  LOAD_FAST                'record'
              104  LOAD_CONST               1
              106  BINARY_SUBSCR    
              108  LOAD_METHOD              endswith
              110  LOAD_STR                 'python2.6/unittest.py'
              112  CALL_METHOD_1         1  ''
              114  POP_JUMP_IF_FALSE    36  'to 36'

 L. 290       116  LOAD_STR                 'unittest'
              118  STORE_GLOBAL             _test_runner_guess

 L. 291       120  POP_TOP          
              122  BREAK_LOOP          130  'to 130'
              124  JUMP_BACK            36  'to 36'

 L. 293       126  LOAD_CONST               None
              128  STORE_GLOBAL             _test_runner_guess
            130_0  COME_FROM            18  '18'

 L. 294       130  LOAD_GLOBAL              _test_runner_guess
              132  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 100


    class parameterized(object):
        __doc__ = ' Parameterize a test case::\n\n            class TestInt(object):\n                @parameterized([\n                    ("A", 10),\n                    ("F", 15),\n                    param("10", 42, base=42)\n                ])\n                def test_int(self, input, expected, base=16):\n                    actual = int(input, base=base)\n                    assert_equal(actual, expected)\n\n            @parameterized([\n                (2, 3, 5)\n                (3, 5, 8),\n            ])\n            def test_add(a, b, expected):\n                assert_equal(a + b, expected)\n        '

        def __init__(self, input, doc_func=None):
            self.get_input = self.input_as_callable(input)
            self.doc_func = doc_func or default_doc_func

        def __call__(self, test_func):
            self.assert_not_in_testcase_subclass()

            @wraps(test_func)
            def wrapper(test_self=None):
                test_cls = test_self and type(test_self)
                if test_self is not None:
                    if issubclass(test_cls, InstanceType):
                        raise TypeError("@parameterized can't be used with old-style classes, but %r has an old-style class. Consider using a new-style class, or '@parameterized.expand' (see http://stackoverflow.com/q/54867/71522 for more information on old-style classes)." % (
                         test_self,))
                original_doc = wrapper.__doc__
                for num, args in enumerate(wrapper.parameterized_input):
                    p = param.from_decorator(args)
                    unbound_func, nose_tuple = self.param_as_nose_tuple(test_self, test_func, num, p)
                    try:
                        wrapper.__doc__ = nose_tuple[0].__doc__
                        if test_self is not None:
                            setattr(test_cls, test_func.__name__, unbound_func)
                        (yield nose_tuple)
                    finally:
                        if test_self is not None:
                            delattr(test_cls, test_func.__name__)
                        wrapper.__doc__ = original_doc

            wrapper.parameterized_input = self.get_input()
            wrapper.parameterized_func = test_func
            test_func.__name__ = '_parameterized_original_%s' % (test_func.__name__,)
            return wrapper

        def param_as_nose_tuple(self, test_self, func, num, p):
            nose_func = wraps(func)(lambda *args: func(*args[:-1], **args[-1]))
            nose_func.__doc__ = self.doc_func(func, num, p)
            unbound_func = nose_func
            if test_self is not None:
                func_self = None if (PY2 and detect_runner() == 'nose') else test_self
                nose_func = make_method(nose_func, func_self, type(test_self))
            return (
             unbound_func, (nose_func,) + p.args + (p.kwargs or {},))

        def assert_not_in_testcase_subclass(self):
            parent_classes = self._terrible_magic_get_defining_classes()
            if any((issubclass(cls, TestCase) for cls in parent_classes)):
                raise Exception("Warning: '@parameterized' tests won't work inside subclasses of 'TestCase' - use '@parameterized.expand' instead.")

        def _terrible_magic_get_defining_classes(self):
            """ Returns the set of parent classes of the class currently being defined.
            Will likely only work if called from the ``parameterized`` decorator.
            This function is entirely @brandon_rhodes's fault, as he suggested
            the implementation: http://stackoverflow.com/a/8793684/71522
            """
            stack = inspect.stack()
            if len(stack) <= 4:
                return []
            else:
                frame = stack[4]
                code_context = frame[4] and frame[4][0].strip()
                return code_context and code_context.startswith('class ') or []
            _, _, parents = code_context.partition('(')
            parents, _, _ = parents.partition(')')
            return eval('[' + parents + ']', frame[0].f_globals, frame[0].f_locals)

        @classmethod
        def input_as_callable(cls, input):
            if callable(input):
                return lambda : cls.check_input_values(input())
            input_values = cls.check_input_values(input)
            return lambda : input_values

        @classmethod
        def check_input_values(cls, input_values):
            if not isinstance(input_values, list):
                input_values = list(input_values)
            return [param.from_decorator(p) for p in input_values]

        @classmethod
        def expand(cls, input, name_func=None, doc_func=None, **legacy):
            """ A "brute force" method of parameterizing test cases. Creates new
            test cases and injects them into the namespace that the wrapped
            function is being defined in. Useful for parameterizing tests in
            subclasses of 'UnitTest', where Nose test generators don't work.

            >>> @parameterized.expand([("foo", 1, 2)])
            ... def test_add1(name, input, expected):
            ...     actual = add1(input)
            ...     assert_equal(actual, expected)
            ...
            >>> locals()
            ... 'test_add1_foo_0': <function ...> ...
            >>>
            """
            if 'testcase_func_name' in legacy:
                warnings.warn('testcase_func_name= is deprecated; use name_func=', DeprecationWarning,
                  stacklevel=2)
                if not name_func:
                    name_func = legacy['testcase_func_name']
            if 'testcase_func_doc' in legacy:
                warnings.warn('testcase_func_doc= is deprecated; use doc_func=', DeprecationWarning,
                  stacklevel=2)
                if not doc_func:
                    doc_func = legacy['testcase_func_doc']
            doc_func = doc_func or default_doc_func
            name_func = name_func or default_name_func

            def parameterized_expand_wrapper(f, instance=None):
                stack = inspect.stack()
                frame = stack[1]
                frame_locals = frame[0].f_locals
                parameters = cls.input_as_callable(input)()
                for num, p in enumerate(parameters):
                    name = name_func(f, num, p)
                    frame_locals[name] = cls.param_as_standalone_func(p, f, name)
                    frame_locals[name].__doc__ = doc_func(f, num, p)
                else:
                    f.__test__ = False

            return parameterized_expand_wrapper

        @classmethod
        def param_as_standalone_func(cls, p, func, name):

            @wraps(func)
            def standalone_func(*a):
                return func(*a + (p.args), **p.kwargs)

            standalone_func.__name__ = name
            standalone_func.place_as = func
            try:
                del standalone_func.__wrapped__
            except AttributeError:
                pass
            else:
                return standalone_func

        @classmethod
        def to_safe_name(cls, s):
            return str(re.sub('[^a-zA-Z0-9_]+', '_', s))


# global _test_runner_guess ## Warning: Unused global