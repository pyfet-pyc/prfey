# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\funcy\simple_funcs.py
from functools import partial
from .primitives import EMPTY
__all__ = [
 'identity', 'constantly', 'caller',
 'partial', 'rpartial', 'func_partial',
 'curry', 'rcurry', 'autocurry',
 'iffy']

def identity(x):
    return x


def constantly(x):
    return lambda *a, **kw: x


def caller(*a, **kw):
    return lambda f: f(*a, **kw)


def func_partial(func, *args, **kwargs):
    """
    A functools.partial alternative, which returns a real function.
    Can be used to construct methods.
    """
    return lambda *a, **kw: func(*(args + a), **dict(kwargs, **kw))


def rpartial(func, *args):
    return lambda *a: func(*(a + args))


def curry(func, n=EMPTY):
    if n is EMPTY:
        n = func.__code__.co_argcount
    if n <= 1:
        return func
    else:
        if n == 2:
            return lambda x: lambda y: func(x, y)
        return lambda x: curry(partial(func, x), n - 1)


def rcurry(func, n=EMPTY):
    if n is EMPTY:
        n = func.__code__.co_argcount
    if n <= 1:
        return func
    else:
        if n == 2:
            return lambda x: lambda y: func(y, x)
        return lambda x: rcurry(rpartial(func, x), n - 1)


def autocurry(func, n=EMPTY, _args=(), _kwargs={}):
    if n is EMPTY:
        n = func.__code__.co_argcount

    def autocurried(*a, **kw):
        args = _args + a
        kwargs = _kwargs.copy()
        kwargs.update(kw)
        if len(args) + len(kwargs) >= n:
            return func(*args, **kwargs)
        else:
            return autocurry(func, n, _args=args, _kwargs=kwargs)

    return autocurried


def iffy(pred, action=EMPTY, default=identity):
    if action is EMPTY:
        return iffy(bool, pred)
    else:
        return --- This code section failed: ---

 L.  79         0  LOAD_DEREF            2  'pred'
                3  LOAD_FAST             0  'v'
                6  CALL_FUNCTION_1       1  None
                9  POP_JUMP_IF_FALSE    22  'to 22'
               12  LOAD_DEREF            0  'action'
               15  LOAD_FAST             0  'v'
               18  CALL_FUNCTION_1       1  None
               21  RETURN_END_IF_LAMBDA
             22_0  COME_FROM             9  '9'

 L.  80        22  LOAD_GLOBAL           0  'callable'
               25  LOAD_DEREF            1  'default'
               28  CALL_FUNCTION_1       1  None
               31  POP_JUMP_IF_FALSE    44  'to 44'
               34  LOAD_DEREF            1  'default'
               37  LOAD_FAST             0  'v'
               40  CALL_FUNCTION_1       1  None
               43  RETURN_END_IF_LAMBDA
             44_0  COME_FROM            31  '31'

 L.  81        44  LOAD_DEREF            1  'default'
               47  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `RETURN_END_IF_LAMBDA' instruction at offset 43