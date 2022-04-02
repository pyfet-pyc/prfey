# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\bson\objectid.py
"""Tools for working with MongoDB `ObjectIds
<http://dochub.mongodb.org/core/objectids>`_.
"""
import binascii, calendar, datetime, os, struct, threading, time
from random import SystemRandom
from bson.errors import InvalidId
from bson.py3compat import PY3, bytes_from_hex, string_type, text_type
from bson.tz_util import utc
_MAX_COUNTER_VALUE = 16777215

def _raise_invalid_id(oid):
    raise InvalidId('%r is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string' % oid)


def _random_bytes():
    """Get the 5-byte random field of an ObjectId."""
    return os.urandom(5)


class ObjectId(object):
    __doc__ = 'A MongoDB ObjectId.\n    '
    _pid = os.getpid()
    _inc = SystemRandom().randint(0, _MAX_COUNTER_VALUE)
    _inc_lock = threading.Lock()
    _ObjectId__random = _random_bytes()
    __slots__ = ('__id', )
    _type_marker = 7

    def __init__(self, oid=None):
        """Initialize a new ObjectId.

        An ObjectId is a 12-byte unique identifier consisting of:

          - a 4-byte value representing the seconds since the Unix epoch,
          - a 5-byte random value,
          - a 3-byte counter, starting with a random value.

        By default, ``ObjectId()`` creates a new unique identifier. The
        optional parameter `oid` can be an :class:`ObjectId`, or any 12
        :class:`bytes` or, in Python 2, any 12-character :class:`str`.

        For example, the 12 bytes b'foo-bar-quux' do not follow the ObjectId
        specification but they are acceptable input::

          >>> ObjectId(b'foo-bar-quux')
          ObjectId('666f6f2d6261722d71757578')

        `oid` can also be a :class:`unicode` or :class:`str` of 24 hex digits::

          >>> ObjectId('0123456789ab0123456789ab')
          ObjectId('0123456789ab0123456789ab')
          >>>
          >>> # A u-prefixed unicode literal:
          >>> ObjectId(u'0123456789ab0123456789ab')
          ObjectId('0123456789ab0123456789ab')

        Raises :class:`~bson.errors.InvalidId` if `oid` is not 12 bytes nor
        24 hex digits, or :class:`TypeError` if `oid` is not an accepted type.

        :Parameters:
          - `oid` (optional): a valid ObjectId.

        .. mongodoc:: objectids

        .. versionchanged:: 3.8
           :class:`~bson.objectid.ObjectId` now implements the `ObjectID
           specification version 0.2
           <https://github.com/mongodb/specifications/blob/master/source/
           objectid.rst>`_.
        """
        if oid is None:
            self._ObjectId__generate()
        elif isinstance(oid, bytes) and len(oid) == 12:
            self._ObjectId__id = oid
        else:
            self._ObjectId__validate(oid)

    @classmethod
    def from_datetime(cls, generation_time):
        """Create a dummy ObjectId instance with a specific generation time.

        This method is useful for doing range queries on a field
        containing :class:`ObjectId` instances.

        .. warning::
           It is not safe to insert a document containing an ObjectId
           generated using this method. This method deliberately
           eliminates the uniqueness guarantee that ObjectIds
           generally provide. ObjectIds generated with this method
           should be used exclusively in queries.

        `generation_time` will be converted to UTC. Naive datetime
        instances will be treated as though they already contain UTC.

        An example using this helper to get documents where ``"_id"``
        was generated before January 1, 2010 would be:

        >>> gen_time = datetime.datetime(2010, 1, 1)
        >>> dummy_id = ObjectId.from_datetime(gen_time)
        >>> result = collection.find({"_id": {"$lt": dummy_id}})

        :Parameters:
          - `generation_time`: :class:`~datetime.datetime` to be used
            as the generation time for the resulting ObjectId.
        """
        if generation_time.utcoffset() is not None:
            generation_time = generation_time - generation_time.utcoffset()
        timestamp = calendar.timegm(generation_time.timetuple())
        oid = struct.pack('>I', int(timestamp)) + b'\x00\x00\x00\x00\x00\x00\x00\x00'
        return cls(oid)

    @classmethod
    def is_valid--- This code section failed: ---

 L. 156         0  LOAD_FAST                'oid'
                2  POP_JUMP_IF_TRUE      8  'to 8'

 L. 157         4  LOAD_CONST               False
                6  RETURN_VALUE     
              8_0  COME_FROM             2  '2'

 L. 159         8  SETUP_FINALLY        24  'to 24'

 L. 160        10  LOAD_GLOBAL              ObjectId
               12  LOAD_FAST                'oid'
               14  CALL_FUNCTION_1       1  ''
               16  POP_TOP          

 L. 161        18  POP_BLOCK        
               20  LOAD_CONST               True
               22  RETURN_VALUE     
             24_0  COME_FROM_FINALLY     8  '8'

 L. 162        24  DUP_TOP          
               26  LOAD_GLOBAL              InvalidId
               28  LOAD_GLOBAL              TypeError
               30  BUILD_TUPLE_2         2 
               32  COMPARE_OP               exception-match
               34  POP_JUMP_IF_FALSE    48  'to 48'
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 163        42  POP_EXCEPT       
               44  LOAD_CONST               False
               46  RETURN_VALUE     
             48_0  COME_FROM            34  '34'
               48  END_FINALLY      

Parse error at or near `DUP_TOP' instruction at offset 24

    @classmethod
    def _random(cls):
        """Generate a 5-byte random number once per process.
        """
        pid = os.getpid()
        if pid != cls._pid:
            cls._pid = pid
            cls._ObjectId__random = _random_bytes()
        return cls._ObjectId__random

    def __generate(self):
        """Generate a new value for this ObjectId.
        """
        oid = struct.pack('>I', int(time.time()))
        oid += ObjectId._random()
        with ObjectId._inc_lock:
            oid += struct.pack('>I', ObjectId._inc)[1:4]
            ObjectId._inc = (ObjectId._inc + 1) % (_MAX_COUNTER_VALUE + 1)
        self._ObjectId__id = oid

    def __validate(self, oid):
        """Validate and use the given id for this ObjectId.

        Raises TypeError if id is not an instance of
        (:class:`basestring` (:class:`str` or :class:`bytes`
        in python 3), ObjectId) and InvalidId if it is not a
        valid ObjectId.

        :Parameters:
          - `oid`: a valid ObjectId
        """
        if isinstance(oid, ObjectId):
            self._ObjectId__id = oid.binary
        elif isinstance(oid, string_type):
            if len(oid) == 24:
                try:
                    self._ObjectId__id = bytes_from_hex(oid)
                except (TypeError, ValueError):
                    _raise_invalid_id(oid)

            else:
                _raise_invalid_id(oid)
        else:
            raise TypeError('id must be an instance of (bytes, %s, ObjectId), not %s' % (
             text_type.__name__, type(oid)))

    @property
    def binary(self):
        """12-byte binary representation of this ObjectId.
        """
        return self._ObjectId__id

    @property
    def generation_time(self):
        """A :class:`datetime.datetime` instance representing the time of
        generation for this :class:`ObjectId`.

        The :class:`datetime.datetime` is timezone aware, and
        represents the generation time in UTC. It is precise to the
        second.
        """
        timestamp = struct.unpack('>I', self._ObjectId__id[0:4])[0]
        return datetime.datetime.fromtimestamp(timestamp, utc)

    def __getstate__(self):
        """return value of object for pickling.
        needed explicitly because __slots__() defined.
        """
        return self._ObjectId__id

    def __setstate__(self, value):
        """explicit state set from pickling
        """
        if isinstance(value, dict):
            oid = value['_ObjectId__id']
        else:
            oid = value
        if PY3 and isinstance(oid, text_type):
            self._ObjectId__id = oid.encode('latin-1')
        else:
            self._ObjectId__id = oid

    def __str__(self):
        if PY3:
            return binascii.hexlify(self._ObjectId__id).decode()
        return binascii.hexlify(self._ObjectId__id)

    def __repr__(self):
        return "ObjectId('%s')" % (str(self),)

    def __eq__(self, other):
        if isinstance(other, ObjectId):
            return self._ObjectId__id == other.binary
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, ObjectId):
            return self._ObjectId__id != other.binary
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, ObjectId):
            return self._ObjectId__id < other.binary
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, ObjectId):
            return self._ObjectId__id <= other.binary
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, ObjectId):
            return self._ObjectId__id > other.binary
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, ObjectId):
            return self._ObjectId__id >= other.binary
        return NotImplemented

    def __hash__(self):
        """Get a hash value for this :class:`ObjectId`."""
        return hash(self._ObjectId__id)