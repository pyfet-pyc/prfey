# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\bson\dbref.py
"""Tools for manipulating DBRefs (references to MongoDB documents)."""
from copy import deepcopy
from bson.py3compat import iteritems, string_type
from bson.son import SON

class DBRef(object):
    __doc__ = 'A reference to a document stored in MongoDB.\n    '
    _type_marker = 100

    def __init__(self, collection, id, database=None, _extra={}, **kwargs):
        """Initialize a new :class:`DBRef`.

        Raises :class:`TypeError` if `collection` or `database` is not
        an instance of :class:`basestring` (:class:`str` in python 3).
        `database` is optional and allows references to documents to work
        across databases. Any additional keyword arguments will create
        additional fields in the resultant embedded document.

        :Parameters:
          - `collection`: name of the collection the document is stored in
          - `id`: the value of the document's ``"_id"`` field
          - `database` (optional): name of the database to reference
          - `**kwargs` (optional): additional keyword arguments will
            create additional, custom fields

        .. mongodoc:: dbrefs
        """
        if not isinstance(collection, string_type):
            raise TypeError('collection must be an instance of %s' % string_type.__name__)
        if database is not None:
            if not isinstance(database, string_type):
                raise TypeError('database must be an instance of %s' % string_type.__name__)
        self._DBRef__collection = collection
        self._DBRef__id = id
        self._DBRef__database = database
        kwargs.update(_extra)
        self._DBRef__kwargs = kwargs

    @property
    def collection(self):
        """Get the name of this DBRef's collection as unicode.
        """
        return self._DBRef__collection

    @property
    def id(self):
        """Get this DBRef's _id.
        """
        return self._DBRef__id

    @property
    def database(self):
        """Get the name of this DBRef's database.

        Returns None if this DBRef doesn't specify a database.
        """
        return self._DBRef__database

    def __getattr__--- This code section failed: ---

 L.  82         0  SETUP_FINALLY        14  'to 14'

 L.  83         2  LOAD_FAST                'self'
                4  LOAD_ATTR                _DBRef__kwargs
                6  LOAD_FAST                'key'
                8  BINARY_SUBSCR    
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L.  84        14  DUP_TOP          
               16  LOAD_GLOBAL              KeyError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    40  'to 40'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L.  85        28  LOAD_GLOBAL              AttributeError
               30  LOAD_FAST                'key'
               32  CALL_FUNCTION_1       1  ''
               34  RAISE_VARARGS_1       1  'exception instance'
               36  POP_EXCEPT       
               38  JUMP_FORWARD         42  'to 42'
             40_0  COME_FROM            20  '20'
               40  END_FINALLY      
             42_0  COME_FROM            38  '38'

Parse error at or near `POP_TOP' instruction at offset 24

    def __setstate__(self, state):
        self.__dict__.update(state)

    def as_doc(self):
        """Get the SON document representation of this DBRef.

        Generally not needed by application developers
        """
        doc = SON([('$ref', self.collection),
         (
          '$id', self.id)])
        if self.database is not None:
            doc['$db'] = self.database
        doc.update(self._DBRef__kwargs)
        return doc

    def __repr__(self):
        extra = ''.join([', %s=%r' % (k, v) for k, v in iteritems(self._DBRef__kwargs)])
        if self.database is None:
            return 'DBRef(%r, %r%s)' % (self.collection, self.id, extra)
        return 'DBRef(%r, %r, %r%s)' % (self.collection, self.id,
         self.database, extra)

    def __eq__(self, other):
        if isinstance(other, DBRef):
            us = (
             self._DBRef__database, self._DBRef__collection,
             self._DBRef__id, self._DBRef__kwargs)
            them = (other._DBRef__database, other._DBRef__collection,
             other._DBRef__id, other._DBRef__kwargs)
            return us == them
        return NotImplemented

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        """Get a hash value for this :class:`DBRef`."""
        return hash((self._DBRef__collection, self._DBRef__id, self._DBRef__database,
         tuple(sorted(self._DBRef__kwargs.items()))))

    def __deepcopy__(self, memo):
        """Support function for `copy.deepcopy()`."""
        return DBRef(deepcopy(self._DBRef__collection, memo), deepcopy(self._DBRef__id, memo), deepcopy(self._DBRef__database, memo), deepcopy(self._DBRef__kwargs, memo))