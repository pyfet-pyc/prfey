# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: signal.py
import _signal
from _signal import *
from functools import wraps as _wraps
from enum import IntEnum as _IntEnum
_globals = globals()
_IntEnum._convert_('Signals', __name__, lambda name: name.isupper() and name.startswith('SIG') and not name.startswith('SIG_') or name.startswith('CTRL_'))
_IntEnum._convert_('Handlers', __name__, lambda name: name in ('SIG_DFL', 'SIG_IGN'))
if 'pthread_sigmask' in _globals:
    _IntEnum._convert_('Sigmasks', __name__, lambda name: name in ('SIG_BLOCK', 'SIG_UNBLOCK', 'SIG_SETMASK'))

def _int_to_enum--- This code section failed: ---

 L.  29         0  SETUP_FINALLY        12  'to 12'

 L.  30         2  LOAD_FAST                'enum_klass'
                4  LOAD_FAST                'value'
                6  CALL_FUNCTION_1       1  ''
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L.  31        12  DUP_TOP          
               14  LOAD_GLOBAL              ValueError
               16  COMPARE_OP               exception-match
               18  POP_JUMP_IF_FALSE    34  'to 34'
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L.  32        26  LOAD_FAST                'value'
               28  ROT_FOUR         
               30  POP_EXCEPT       
               32  RETURN_VALUE     
             34_0  COME_FROM            18  '18'
               34  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 22


def _enum_to_int--- This code section failed: ---

 L.  39         0  SETUP_FINALLY        12  'to 12'

 L.  40         2  LOAD_GLOBAL              int
                4  LOAD_FAST                'value'
                6  CALL_FUNCTION_1       1  ''
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L.  41        12  DUP_TOP          
               14  LOAD_GLOBAL              ValueError
               16  LOAD_GLOBAL              TypeError
               18  BUILD_TUPLE_2         2 
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    38  'to 38'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L.  42        30  LOAD_FAST                'value'
               32  ROT_FOUR         
               34  POP_EXCEPT       
               36  RETURN_VALUE     
             38_0  COME_FROM            22  '22'
               38  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 26


@_wraps(_signal.signal)
def signal(signalnum, handler):
    handler = _signal.signal(_enum_to_int(signalnum), _enum_to_int(handler))
    return _int_to_enum(handler, Handlers)


@_wraps(_signal.getsignal)
def getsignal(signalnum):
    handler = _signal.getsignal(signalnum)
    return _int_to_enum(handler, Handlers)


if 'pthread_sigmask' in _globals:

    @_wraps(_signal.pthread_sigmask)
    def pthread_sigmask(how, mask):
        sigs_set = _signal.pthread_sigmask(how, mask)
        return set((_int_to_enum(x, Signals) for x in sigs_set))


    pthread_sigmask.__doc__ = _signal.pthread_sigmask.__doc__
if 'sigpending' in _globals:

    @_wraps(_signal.sigpending)
    def sigpending():
        return {_int_to_enum(x, Signals) for x in _signal.sigpending()}


if 'sigwait' in _globals:

    @_wraps(_signal.sigwait)
    def sigwait(sigset):
        retsig = _signal.sigwait(sigset)
        return _int_to_enum(retsig, Signals)


    sigwait.__doc__ = _signal.sigwait
if 'valid_signals' in _globals:

    @_wraps(_signal.valid_signals)
    def valid_signals():
        return {_int_to_enum(x, Signals) for x in _signal.valid_signals()}


del _globals
del _wraps