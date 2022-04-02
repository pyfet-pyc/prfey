# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: secretstorage\item.py
"""SecretStorage item contains a *secret*, some *attributes* and a
*label* visible to user. Editing all these properties and reading the
secret is possible only when the :doc:`collection <collection>` storing
the item is unlocked. The collection can be unlocked using collection's
:meth:`~secretstorage.collection.Collection.unlock` method."""
from typing import Dict, Optional
from jeepney.io.blocking import DBusConnection
from secretstorage.defines import SS_PREFIX
from secretstorage.dhcrypto import Session
from secretstorage.exceptions import LockedException, PromptDismissedException
from secretstorage.util import DBusAddressWrapper, exec_prompt, open_session, format_secret, unlock_objects
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
ITEM_IFACE = SS_PREFIX + 'Item'

class Item(object):
    __doc__ = 'Represents a secret item.'

    def __init__(self, connection: DBusConnection, item_path: str, session: Optional[Session]=None) -> None:
        self.item_path = item_path
        self._item = DBusAddressWrapper(item_path, ITEM_IFACE, connection)
        self._item.get_property('Label')
        self.session = session
        self.connection = connection

    def __eq__--- This code section failed: ---

 L.  36         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'other'
                4  LOAD_ATTR                item_path
                6  LOAD_GLOBAL              str
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_TRUE     16  'to 16'
               12  <74>             
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM            10  '10'

 L.  37        16  LOAD_FAST                'self'
               18  LOAD_ATTR                item_path
               20  LOAD_FAST                'other'
               22  LOAD_ATTR                item_path
               24  COMPARE_OP               ==
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def is_locked(self) -> bool:
        """Returns :const:`True` if item is locked, otherwise
                :const:`False`."""
        return bool(self._item.get_property('Locked'))

    def ensure_not_locked(self) -> None:
        """If collection is locked, raises
                :exc:`~secretstorage.exceptions.LockedException`."""
        if self.is_locked():
            raise LockedException('Item is locked!')

    def unlock(self) -> bool:
        """Requests unlocking the item. Usually, this means that the
                whole collection containing this item will be unlocked.

                Returns a boolean representing whether the prompt has been
                dismissed; that means :const:`False` on successful unlocking
                and :const:`True` if it has been dismissed.

                .. versionadded:: 2.1.2

                .. versionchanged:: 3.0
                   No longer accepts the ``callback`` argument.
                """
        return unlock_objectsself.connection[self.item_path]

    def get_attributes(self) -> Dict[(str, str)]:
        """Returns item attributes (dictionary)."""
        attrs = self._item.get_property('Attributes')
        return dict(attrs)

    def set_attributes(self, attributes: Dict[(str, str)]) -> None:
        """Sets item attributes to `attributes` (dictionary)."""
        self._item.set_property('Attributes', 'a{ss}', attributes)

    def get_label--- This code section failed: ---

 L.  76         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _item
                4  LOAD_METHOD              get_property
                6  LOAD_STR                 'Label'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'label'

 L.  77        12  LOAD_GLOBAL              isinstance
               14  LOAD_FAST                'label'
               16  LOAD_GLOBAL              str
               18  CALL_FUNCTION_2       2  ''
               20  POP_JUMP_IF_TRUE     26  'to 26'
               22  <74>             
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            20  '20'

 L.  78        26  LOAD_FAST                'label'
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 22

    def set_label(self, label: str) -> None:
        """Sets item label to `label`."""
        self.ensure_not_locked()
        self._item.set_property('Label', 's', label)

    def delete(self) -> None:
        """Deletes the item."""
        self.ensure_not_locked()
        prompt, = self._item.call('Delete', '')
        if prompt != '/':
            dismissed, _result = exec_promptself.connectionprompt
            if dismissed:
                raise PromptDismissedException('Prompt dismissed.')

    def get_secret--- This code section failed: ---

 L.  96         0  LOAD_FAST                'self'
                2  LOAD_METHOD              ensure_not_locked
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L.  97         8  LOAD_FAST                'self'
               10  LOAD_ATTR                session
               12  POP_JUMP_IF_TRUE     26  'to 26'

 L.  98        14  LOAD_GLOBAL              open_session
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                connection
               20  CALL_FUNCTION_1       1  ''
               22  LOAD_FAST                'self'
               24  STORE_ATTR               session
             26_0  COME_FROM            12  '12'

 L.  99        26  LOAD_FAST                'self'
               28  LOAD_ATTR                _item
               30  LOAD_METHOD              call
               32  LOAD_STR                 'GetSecret'
               34  LOAD_STR                 'o'
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                session
               40  LOAD_ATTR                object_path
               42  CALL_METHOD_3         3  ''
               44  UNPACK_SEQUENCE_1     1 
               46  STORE_FAST               'secret'

 L. 100        48  LOAD_FAST                'self'
               50  LOAD_ATTR                session
               52  LOAD_ATTR                encrypted
               54  POP_JUMP_IF_TRUE     68  'to 68'

 L. 101        56  LOAD_GLOBAL              bytes
               58  LOAD_FAST                'secret'
               60  LOAD_CONST               2
               62  BINARY_SUBSCR    
               64  CALL_FUNCTION_1       1  ''
               66  RETURN_VALUE     
             68_0  COME_FROM            54  '54'

 L. 102        68  LOAD_FAST                'self'
               70  LOAD_ATTR                session
               72  LOAD_ATTR                aes_key
               74  LOAD_CONST               None
               76  <117>                 1  ''
               78  POP_JUMP_IF_TRUE     84  'to 84'
               80  <74>             
               82  RAISE_VARARGS_1       1  'exception instance'
             84_0  COME_FROM            78  '78'

 L. 103        84  LOAD_GLOBAL              algorithms
               86  LOAD_METHOD              AES
               88  LOAD_FAST                'self'
               90  LOAD_ATTR                session
               92  LOAD_ATTR                aes_key
               94  CALL_METHOD_1         1  ''
               96  STORE_FAST               'aes'

 L. 104        98  LOAD_GLOBAL              bytes
              100  LOAD_FAST                'secret'
              102  LOAD_CONST               1
              104  BINARY_SUBSCR    
              106  CALL_FUNCTION_1       1  ''
              108  STORE_FAST               'aes_iv'

 L. 105       110  LOAD_GLOBAL              Cipher
              112  LOAD_FAST                'aes'
              114  LOAD_GLOBAL              modes
              116  LOAD_METHOD              CBC
              118  LOAD_FAST                'aes_iv'
              120  CALL_METHOD_1         1  ''
              122  LOAD_GLOBAL              default_backend
              124  CALL_FUNCTION_0       0  ''
              126  CALL_FUNCTION_3       3  ''
              128  LOAD_METHOD              decryptor
              130  CALL_METHOD_0         0  ''
              132  STORE_FAST               'decryptor'

 L. 106       134  LOAD_FAST                'secret'
              136  LOAD_CONST               2
              138  BINARY_SUBSCR    
              140  STORE_FAST               'encrypted_secret'

 L. 107       142  LOAD_FAST                'decryptor'
              144  LOAD_METHOD              update
              146  LOAD_GLOBAL              bytes
              148  LOAD_FAST                'encrypted_secret'
              150  CALL_FUNCTION_1       1  ''
              152  CALL_METHOD_1         1  ''
              154  LOAD_FAST                'decryptor'
              156  LOAD_METHOD              finalize
              158  CALL_METHOD_0         0  ''
              160  BINARY_ADD       
              162  STORE_FAST               'padded_secret'

 L. 108       164  LOAD_GLOBAL              isinstance
              166  LOAD_FAST                'padded_secret'
              168  LOAD_GLOBAL              bytes
              170  CALL_FUNCTION_2       2  ''
              172  POP_JUMP_IF_TRUE    178  'to 178'
              174  <74>             
              176  RAISE_VARARGS_1       1  'exception instance'
            178_0  COME_FROM           172  '172'

 L. 109       178  LOAD_FAST                'padded_secret'
              180  LOAD_CONST               None
              182  LOAD_FAST                'padded_secret'
              184  LOAD_CONST               -1
              186  BINARY_SUBSCR    
              188  UNARY_NEGATIVE   
              190  BUILD_SLICE_2         2 
              192  BINARY_SUBSCR    
              194  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 76

    def get_secret_content_type(self) -> str:
        """Returns content type of item secret (string)."""
        self.ensure_not_locked()
        if not self.session:
            self.session = open_session(self.connection)
        secret, = self._item.call('GetSecret', 'o', self.session.object_path)
        return str(secret[3])

    def set_secret(self, secret: bytes, content_type: str='text/plain') -> None:
        """Sets item secret to `secret`. If `content_type` is given,
                also sets the content type of the secret (``text/plain`` by
                default)."""
        self.ensure_not_locked()
        if not self.session:
            self.session = open_session(self.connection)
        _secret = format_secret(self.session, secret, content_type)
        self._item.call('SetSecret', '(oayays)', _secret)

    def get_created--- This code section failed: ---

 L. 135         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _item
                4  LOAD_METHOD              get_property
                6  LOAD_STR                 'Created'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'created'

 L. 136        12  LOAD_GLOBAL              isinstance
               14  LOAD_FAST                'created'
               16  LOAD_GLOBAL              int
               18  CALL_FUNCTION_2       2  ''
               20  POP_JUMP_IF_TRUE     26  'to 26'
               22  <74>             
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            20  '20'

 L. 137        26  LOAD_FAST                'created'
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 22

    def get_modified--- This code section failed: ---

 L. 142         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _item
                4  LOAD_METHOD              get_property
                6  LOAD_STR                 'Modified'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'modified'

 L. 143        12  LOAD_GLOBAL              isinstance
               14  LOAD_FAST                'modified'
               16  LOAD_GLOBAL              int
               18  CALL_FUNCTION_2       2  ''
               20  POP_JUMP_IF_TRUE     26  'to 26'
               22  <74>             
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            20  '20'

 L. 144        26  LOAD_FAST                'modified'
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<74>' instruction at offset 22