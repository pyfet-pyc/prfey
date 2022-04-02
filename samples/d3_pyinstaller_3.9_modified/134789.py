# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: secretstorage\collection.py
"""Collection is a place where secret items are stored. Normally, only
the default collection should be used, but this module allows to use any
registered collection. Use :func:`get_default_collection` to get the
default collection (and create it, if necessary).

Collections are usually automatically unlocked when user logs in, but
collections can also be locked and unlocked using
:meth:`Collection.lock` and :meth:`Collection.unlock` methods (unlocking
requires showing the unlocking prompt to user and can be synchronous or
asynchronous). Creating new items and editing existing ones is possible
only in unlocked collection."""
from typing import Dict, Iterator, Optional
from jeepney.io.blocking import DBusConnection
from secretstorage.defines import SS_PREFIX, SS_PATH
from secretstorage.dhcrypto import Session
from secretstorage.exceptions import LockedException, ItemNotFoundException, PromptDismissedException
from secretstorage.item import Item
from secretstorage.util import DBusAddressWrapper, exec_prompt, format_secret, open_session, unlock_objects
COLLECTION_IFACE = SS_PREFIX + 'Collection'
SERVICE_IFACE = SS_PREFIX + 'Service'
DEFAULT_COLLECTION = '/org/freedesktop/secrets/aliases/default'
SESSION_COLLECTION = '/org/freedesktop/secrets/collection/session'

class Collection(object):
    __doc__ = 'Represents a collection.'

    def __init__(self, connection: DBusConnection, collection_path: str=DEFAULT_COLLECTION, session: Optional[Session]=None) -> None:
        self.connection = connection
        self.session = session
        self.collection_path = collection_path
        self._collection = DBusAddressWrapper(collection_path, COLLECTION_IFACE, connection)
        self._collection.get_property('Label')

    def is_locked(self) -> bool:
        """Returns :const:`True` if item is locked, otherwise
                :const:`False`."""
        return bool(self._collection.get_property('Locked'))

    def ensure_not_locked(self) -> None:
        """If collection is locked, raises
                :exc:`~secretstorage.exceptions.LockedException`."""
        if self.is_locked():
            raise LockedException('Collection is locked!')

    def unlock(self) -> bool:
        """Requests unlocking the collection.

                Returns a boolean representing whether the prompt has been
                dismissed; that means :const:`False` on successful unlocking
                and :const:`True` if it has been dismissed.

                .. versionchanged:: 3.0
                   No longer accepts the ``callback`` argument.
                """
        return unlock_objects(self.connection, [self.collection_path])

    def lock(self) -> None:
        """Locks the collection."""
        service = DBusAddressWrapper(SS_PATH, SERVICE_IFACE, self.connection)
        service.call('Lock', 'ao', [self.collection_path])

    def delete(self) -> None:
        """Deletes the collection and all items inside it."""
        self.ensure_not_locked()
        prompt, = self._collection.call('Delete', '')
        if prompt != '/':
            dismissed, _result = exec_prompt(self.connection, prompt)
            if dismissed:
                raise PromptDismissedException('Prompt dismissed.')

    def get_all_items(self) -> Iterator[Item]:
        """Returns a generator of all items in the collection."""
        for item_path in self._collection.get_property('Items'):
            yield Item(self.connection, item_path, self.session)

    def search_items(self, attributes: Dict[(str, str)]) -> Iterator[Item]:
        """Returns a generator of items with the given attributes.
                `attributes` should be a dictionary."""
        result, = self._collection.call('SearchItems', 'a{ss}', attributes)
        for item_path in result:
            yield Item(self.connection, item_path, self.session)

    def get_label--- This code section failed: ---

 L.  97         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _collection
                4  LOAD_METHOD              get_property
                6  LOAD_STR                 'Label'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'label'

 L.  98        12  LOAD_GLOBAL              isinstance
               14  LOAD_FAST                'label'
               16  LOAD_GLOBAL              str
               18  CALL_FUNCTION_2       2  ''
               20  POP_JUMP_IF_TRUE     26  'to 26'
               22  <74>             
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            20  '20'

 L.  99        26  LOAD_FAST                'label'
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 22

    def set_label(self, label: str) -> None:
        """Sets collection label to `label`."""
        self.ensure_not_locked()
        self._collection.set_property('Label', 's', label)

    def create_item(self, label: str, attributes: Dict[(str, str)], secret: bytes, replace: bool=False, content_type: str='text/plain') -> Item:
        """Creates a new :class:`~secretstorage.item.Item` with given
                `label` (unicode string), `attributes` (dictionary) and `secret`
                (bytestring). If `replace` is :const:`True`, replaces the existing
                item with the same attributes. If `content_type` is given, also
                sets the content type of the secret (``text/plain`` by default).
                Returns the created item."""
        self.ensure_not_locked()
        if not self.session:
            self.session = open_session(self.connection)
        _secret = format_secret(self.session, secret, content_type)
        properties = {SS_PREFIX + 'Item.Label': ('s', label), 
         SS_PREFIX + 'Item.Attributes': ('a{ss}', attributes)}
        new_item, prompt = self._collection.call('CreateItem', 'a{sv}(oayays)b', properties, _secret, replace)
        return Item(self.connection, new_item, self.session)


def create_collection--- This code section failed: ---

 L. 135         0  LOAD_FAST                'session'
                2  POP_JUMP_IF_TRUE     12  'to 12'

 L. 136         4  LOAD_GLOBAL              open_session
                6  LOAD_FAST                'connection'
                8  CALL_FUNCTION_1       1  ''
               10  STORE_FAST               'session'
             12_0  COME_FROM             2  '2'

 L. 137        12  LOAD_GLOBAL              SS_PREFIX
               14  LOAD_STR                 'Collection.Label'
               16  BINARY_ADD       
               18  LOAD_STR                 's'
               20  LOAD_FAST                'label'
               22  BUILD_TUPLE_2         2 
               24  BUILD_MAP_1           1 
               26  STORE_FAST               'properties'

 L. 138        28  LOAD_GLOBAL              DBusAddressWrapper
               30  LOAD_GLOBAL              SS_PATH
               32  LOAD_GLOBAL              SERVICE_IFACE
               34  LOAD_FAST                'connection'
               36  CALL_FUNCTION_3       3  ''
               38  STORE_FAST               'service'

 L. 139        40  LOAD_FAST                'service'
               42  LOAD_METHOD              call
               44  LOAD_STR                 'CreateCollection'
               46  LOAD_STR                 'a{sv}s'

 L. 140        48  LOAD_FAST                'properties'
               50  LOAD_FAST                'alias'

 L. 139        52  CALL_METHOD_4         4  ''
               54  UNPACK_SEQUENCE_2     2 
               56  STORE_FAST               'collection_path'
               58  STORE_FAST               'prompt'

 L. 141        60  LOAD_GLOBAL              len
               62  LOAD_FAST                'collection_path'
               64  CALL_FUNCTION_1       1  ''
               66  LOAD_CONST               1
               68  COMPARE_OP               >
               70  POP_JUMP_IF_FALSE    86  'to 86'

 L. 142        72  LOAD_GLOBAL              Collection
               74  LOAD_FAST                'connection'
               76  LOAD_FAST                'collection_path'
               78  LOAD_FAST                'session'
               80  LOAD_CONST               ('session',)
               82  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               84  RETURN_VALUE     
             86_0  COME_FROM            70  '70'

 L. 143        86  LOAD_GLOBAL              exec_prompt
               88  LOAD_FAST                'connection'
               90  LOAD_FAST                'prompt'
               92  CALL_FUNCTION_2       2  ''
               94  UNPACK_SEQUENCE_2     2 
               96  STORE_FAST               'dismissed'
               98  STORE_FAST               'result'

 L. 144       100  LOAD_FAST                'dismissed'
              102  POP_JUMP_IF_FALSE   112  'to 112'

 L. 145       104  LOAD_GLOBAL              PromptDismissedException
              106  LOAD_STR                 'Prompt dismissed.'
              108  CALL_FUNCTION_1       1  ''
              110  RAISE_VARARGS_1       1  'exception instance'
            112_0  COME_FROM           102  '102'

 L. 146       112  LOAD_FAST                'result'
              114  UNPACK_SEQUENCE_2     2 
              116  STORE_FAST               'signature'
              118  STORE_FAST               'collection_path'

 L. 147       120  LOAD_FAST                'signature'
              122  LOAD_STR                 'o'
              124  COMPARE_OP               ==
              126  POP_JUMP_IF_TRUE    132  'to 132'
              128  <74>             
              130  RAISE_VARARGS_1       1  'exception instance'
            132_0  COME_FROM           126  '126'

 L. 148       132  LOAD_GLOBAL              Collection
              134  LOAD_FAST                'connection'
              136  LOAD_FAST                'collection_path'
              138  LOAD_FAST                'session'
              140  LOAD_CONST               ('session',)
              142  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              144  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 128


def get_all_collections(connection: DBusConnection) -> Iterator[Collection]:
    """Returns a generator of all available collections."""
    service = DBusAddressWrapper(SS_PATH, SERVICE_IFACE, connection)
    for collection_path in service.get_property('Collections'):
        yield Collection(connection, collection_path)


def get_default_collection--- This code section failed: ---

 L. 160         0  SETUP_FINALLY        12  'to 12'

 L. 161         2  LOAD_GLOBAL              Collection
                4  LOAD_FAST                'connection'
                6  CALL_FUNCTION_1       1  ''
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L. 162        12  DUP_TOP          
               14  LOAD_GLOBAL              ItemNotFoundException
               16  <121>                42  ''
               18  POP_TOP          
               20  POP_TOP          
               22  POP_TOP          

 L. 163        24  LOAD_GLOBAL              create_collection
               26  LOAD_FAST                'connection'
               28  LOAD_STR                 'Default'

 L. 164        30  LOAD_STR                 'default'
               32  LOAD_FAST                'session'

 L. 163        34  CALL_FUNCTION_4       4  ''
               36  ROT_FOUR         
               38  POP_EXCEPT       
               40  RETURN_VALUE     
               42  <48>             

Parse error at or near `<121>' instruction at offset 16


def get_any_collection--- This code section failed: ---

 L. 172         0  SETUP_FINALLY        12  'to 12'

 L. 173         2  LOAD_GLOBAL              Collection
                4  LOAD_FAST                'connection'
                6  CALL_FUNCTION_1       1  ''
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L. 174        12  DUP_TOP          
               14  LOAD_GLOBAL              ItemNotFoundException
               16  <121>                28  ''
               18  POP_TOP          
               20  POP_TOP          
               22  POP_TOP          

 L. 175        24  POP_EXCEPT       
               26  JUMP_FORWARD         30  'to 30'
               28  <48>             
             30_0  COME_FROM            26  '26'

 L. 176        30  SETUP_FINALLY        44  'to 44'

 L. 179        32  LOAD_GLOBAL              Collection
               34  LOAD_FAST                'connection'
               36  LOAD_GLOBAL              SESSION_COLLECTION
               38  CALL_FUNCTION_2       2  ''
               40  POP_BLOCK        
               42  RETURN_VALUE     
             44_0  COME_FROM_FINALLY    30  '30'

 L. 180        44  DUP_TOP          
               46  LOAD_GLOBAL              ItemNotFoundException
               48  <121>                60  ''
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L. 181        56  POP_EXCEPT       
               58  JUMP_FORWARD         62  'to 62'
               60  <48>             
             62_0  COME_FROM            58  '58'

 L. 182        62  LOAD_GLOBAL              list
               64  LOAD_GLOBAL              get_all_collections
               66  LOAD_FAST                'connection'
               68  CALL_FUNCTION_1       1  ''
               70  CALL_FUNCTION_1       1  ''
               72  STORE_FAST               'collections'

 L. 183        74  LOAD_FAST                'collections'
               76  POP_JUMP_IF_FALSE    86  'to 86'

 L. 184        78  LOAD_FAST                'collections'
               80  LOAD_CONST               0
               82  BINARY_SUBSCR    
               84  RETURN_VALUE     
             86_0  COME_FROM            76  '76'

 L. 186        86  LOAD_GLOBAL              ItemNotFoundException
               88  LOAD_STR                 'No collections found.'
               90  CALL_FUNCTION_1       1  ''
               92  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<121>' instruction at offset 16


def get_collection_by_alias(connection: DBusConnection, alias: str) -> Collection:
    """Returns the collection with the given `alias`. If there is no
        such collection, raises
        :exc:`~secretstorage.exceptions.ItemNotFoundException`."""
    service = DBusAddressWrapper(SS_PATH, SERVICE_IFACE, connection)
    collection_path, = service.call('ReadAlias', 's', alias)
    if len(collection_path) <= 1:
        raise ItemNotFoundException('No collection with such alias.')
    return Collection(connection, collection_path)


def search_items(connection: DBusConnection, attributes: Dict[(str, str)]) -> Iterator[Item]:
    """Returns a generator of items in all collections with the given
        attributes. `attributes` should be a dictionary."""
    service = DBusAddressWrapper(SS_PATH, SERVICE_IFACE, connection)
    locked, unlocked = service.call('SearchItems', 'a{ss}', attributes)
    for item_path in locked + unlocked:
        yield Item(connection, item_path)