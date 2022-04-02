# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pymongo\__init__.py
"""Python driver for MongoDB."""
ASCENDING = 1
DESCENDING = -1
GEO2D = '2d'
GEOHAYSTACK = 'geoHaystack'
GEOSPHERE = '2dsphere'
HASHED = 'hashed'
TEXT = 'text'
OFF = 0
SLOW_ONLY = 1
ALL = 2
version_tuple = (3, 10, 1)

def get_version_string():
    if isinstance(version_tuple[(-1)], str):
        return '.'.join(map(str, version_tuple[:-1])) + version_tuple[(-1)]
    return '.'.join(map(str, version_tuple))


__version__ = version = get_version_string()
from pymongo.collection import ReturnDocument
from pymongo.common import MIN_SUPPORTED_WIRE_VERSION, MAX_SUPPORTED_WIRE_VERSION
from pymongo.cursor import CursorType
from pymongo.mongo_client import MongoClient
from pymongo.mongo_replica_set_client import MongoReplicaSetClient
from pymongo.operations import IndexModel, InsertOne, DeleteOne, DeleteMany, UpdateOne, UpdateMany, ReplaceOne
from pymongo.read_preferences import ReadPreference
from pymongo.write_concern import WriteConcern

def has_c--- This code section failed: ---

 L.  95         0  SETUP_FINALLY        20  'to 20'

 L.  96         2  LOAD_CONST               0
                4  LOAD_CONST               ('_cmessage',)
                6  IMPORT_NAME              pymongo
                8  IMPORT_FROM              _cmessage
               10  STORE_FAST               '_cmessage'
               12  POP_TOP          

 L.  97        14  POP_BLOCK        
               16  LOAD_CONST               True
               18  RETURN_VALUE     
             20_0  COME_FROM_FINALLY     0  '0'

 L.  98        20  DUP_TOP          
               22  LOAD_GLOBAL              ImportError
               24  COMPARE_OP               exception-match
               26  POP_JUMP_IF_FALSE    40  'to 40'
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L.  99        34  POP_EXCEPT       
               36  LOAD_CONST               False
               38  RETURN_VALUE     
             40_0  COME_FROM            26  '26'
               40  END_FINALLY      

Parse error at or near `DUP_TOP' instruction at offset 20