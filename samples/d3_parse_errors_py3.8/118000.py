# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\discord\ext\commands\cooldowns.py
"""
The MIT License (MIT)

Copyright (c) 2015-2020 Rapptz

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
from discord.enums import Enum
import time, asyncio
from collections import deque
from ...abc import PrivateChannel
from .errors import MaxConcurrencyReached
__all__ = ('BucketType', 'Cooldown', 'CooldownMapping', 'MaxConcurrency')

class BucketType(Enum):
    default = 0
    user = 1
    guild = 2
    channel = 3
    member = 4
    category = 5
    role = 6

    def get_key(self, msg):
        if self is BucketType.user:
            return msg.author.id
        if self is BucketType.guild:
            return (msg.guild or msg.author).id
        if self is BucketType.channel:
            return msg.channel.id
        if self is BucketType.member:
            return (msg.guild and msg.guild.id, msg.author.id)
        if self is BucketType.category:
            return (msg.channel.category or msg.channel).id
        if self is BucketType.role:
            return (msg.channel if isinstance(msg.channel, PrivateChannel) else msg.author.top_role).id


class Cooldown:
    __slots__ = ('rate', 'per', 'type', '_window', '_tokens', '_last')

    def __init__(self, rate, per, type):
        self.rate = int(rate)
        self.per = float(per)
        self.type = type
        self._window = 0.0
        self._tokens = self.rate
        self._last = 0.0
        if not isinstance(self.type, BucketType):
            raise TypeError('Cooldown type must be a BucketType')

    def get_tokens(self, current=None):
        if not current:
            current = time.time()
        tokens = self._tokens
        if current > self._window + self.per:
            tokens = self.rate
        return tokens

    def update_rate_limit(self, current=None):
        current = current or time.time()
        self._last = current
        self._tokens = self.get_tokens(current)
        if self._tokens == self.rate:
            self._window = current
        if self._tokens == 0:
            return self.per - (current - self._window)
        self._tokens -= 1
        if self._tokens == 0:
            self._window = current

    def reset(self):
        self._tokens = self.rate
        self._last = 0.0

    def copy(self):
        return Cooldown(self.rate, self.per, self.type)

    def __repr__(self):
        return '<Cooldown rate: {0.rate} per: {0.per} window: {0._window} tokens: {0._tokens}>'.format(self)


class CooldownMapping:

    def __init__(self, original):
        self._cache = {}
        self._cooldown = original

    def copy(self):
        ret = CooldownMapping(self._cooldown)
        ret._cache = self._cache.copy()
        return ret

    @property
    def valid(self):
        return self._cooldown is not None

    @classmethod
    def from_cooldown(cls, rate, per, type):
        return cls(Cooldown(rate, per, type))

    def _bucket_key(self, msg):
        return self._cooldown.type.get_key(msg)

    def _verify_cache_integrity(self, current=None):
        current = current or time.time()
        dead_keys = [k for k, v in self._cache.items() if current > v._last + v.per]
        for k in dead_keys:
            del self._cache[k]

    def get_bucket(self, message, current=None):
        if self._cooldown.type is BucketType.default:
            return self._cooldown
        self._verify_cache_integrity(current)
        key = self._bucket_key(message)
        if key not in self._cache:
            bucket = self._cooldown.copy()
            self._cache[key] = bucket
        else:
            bucket = self._cache[key]
        return bucket

    def update_rate_limit(self, message, current=None):
        bucket = self.get_bucket(message, current)
        return bucket.update_rate_limit(current)


class _Semaphore:
    __doc__ = "This class is a version of a semaphore.\n\n    If you're wondering why asyncio.Semaphore isn't being used,\n    it's because it doesn't expose the internal value. This internal\n    value is necessary because I need to support both `wait=True` and\n    `wait=False`.\n\n    An asyncio.Queue could have been used to do this as well -- but it is\n    not as inefficient since internally that uses two queues and is a bit\n    overkill for what is basically a counter.\n    "
    __slots__ = ('value', 'loop', '_waiters')

    def __init__(self, number):
        self.value = number
        self.loop = asyncio.get_event_loop()
        self._waiters = deque()

    def __repr__(self):
        return '<_Semaphore value={0.value} waiters={1}>'.format(self, len(self._waiters))

    def locked(self):
        return self.value == 0

    def is_active(self):
        return len(self._waiters) > 0

    def wake_up(self):
        while True:
            if self._waiters:
                future = self._waiters.popleft()
                if not future.done():
                    future.set_result(None)
                return

    async def acquire--- This code section failed: ---

 L. 211         0  LOAD_FAST                'wait'
                2  POP_JUMP_IF_TRUE     18  'to 18'
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                value
                8  LOAD_CONST               0
               10  COMPARE_OP               <=
               12  POP_JUMP_IF_FALSE    18  'to 18'

 L. 213        14  LOAD_CONST               False
               16  RETURN_VALUE     
             18_0  COME_FROM           114  '114'
             18_1  COME_FROM           110  '110'
             18_2  COME_FROM            64  '64'
             18_3  COME_FROM            12  '12'
             18_4  COME_FROM             2  '2'

 L. 215        18  LOAD_FAST                'self'
               20  LOAD_ATTR                value
               22  LOAD_CONST               0
               24  COMPARE_OP               <=
               26  POP_JUMP_IF_FALSE   116  'to 116'

 L. 216        28  LOAD_FAST                'self'
               30  LOAD_ATTR                loop
               32  LOAD_METHOD              create_future
               34  CALL_METHOD_0         0  ''
               36  STORE_FAST               'future'

 L. 217        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _waiters
               42  LOAD_METHOD              append
               44  LOAD_FAST                'future'
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          

 L. 218        50  SETUP_FINALLY        66  'to 66'

 L. 219        52  LOAD_FAST                'future'
               54  GET_AWAITABLE    
               56  LOAD_CONST               None
               58  YIELD_FROM       
               60  POP_TOP          
               62  POP_BLOCK        
               64  JUMP_BACK            18  'to 18'
             66_0  COME_FROM_FINALLY    50  '50'

 L. 220        66  POP_TOP          
               68  POP_TOP          
               70  POP_TOP          

 L. 221        72  LOAD_FAST                'future'
               74  LOAD_METHOD              cancel
               76  CALL_METHOD_0         0  ''
               78  POP_TOP          

 L. 222        80  LOAD_FAST                'self'
               82  LOAD_ATTR                value
               84  LOAD_CONST               0
               86  COMPARE_OP               >
               88  POP_JUMP_IF_FALSE   106  'to 106'
               90  LOAD_FAST                'future'
               92  LOAD_METHOD              cancelled
               94  CALL_METHOD_0         0  ''
               96  POP_JUMP_IF_TRUE    106  'to 106'

 L. 223        98  LOAD_FAST                'self'
              100  LOAD_METHOD              wake_up
              102  CALL_METHOD_0         0  ''
              104  POP_TOP          
            106_0  COME_FROM            96  '96'
            106_1  COME_FROM            88  '88'

 L. 224       106  RAISE_VARARGS_0       0  'reraise'
              108  POP_EXCEPT       
              110  JUMP_BACK            18  'to 18'
              112  END_FINALLY      
              114  JUMP_BACK            18  'to 18'
            116_0  COME_FROM            26  '26'

 L. 226       116  LOAD_FAST                'self'
              118  DUP_TOP          
              120  LOAD_ATTR                value
              122  LOAD_CONST               1
              124  INPLACE_SUBTRACT 
              126  ROT_TWO          
              128  STORE_ATTR               value

 L. 227       130  LOAD_CONST               True
              132  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 110

    def release(self):
        self.value += 1
        self.wake_up()


class MaxConcurrency:
    __slots__ = ('number', 'per', 'wait', '_mapping')

    def __init__(self, number, *, per, wait):
        self._mapping = {}
        self.per = per
        self.number = number
        self.wait = wait
        if number <= 0:
            raise ValueError("max_concurrency 'number' cannot be less than 1")
        if not isinstance(per, BucketType):
            raise TypeError("max_concurrency 'per' must be of type BucketType not %r" % type(per))

    def copy(self):
        return self.__class__((self.number), per=(self.per), wait=(self.wait))

    def __repr__(self):
        return '<MaxConcurrency per={0.per!r} number={0.number} wait={0.wait}>'.format(self)

    def get_key(self, message):
        return self.per.get_key(message)

    async def acquire(self, message):
        key = self.get_key(message)
        try:
            sem = self._mapping[key]
        except KeyError:
            self._mapping[key] = sem = _Semaphore(self.number)
        else:
            acquired = await sem.acquire(wait=(self.wait))
            if not acquired:
                raise MaxConcurrencyReached(self.number, self.per)

    async def release(self, message):
        key = self.get_key(message)
        try:
            sem = self._mapping[key]
        except KeyError:
            return
        else:
            sem.release()
            if sem.value >= self.number:
                if not sem.is_active():
                    del self._mapping[key]