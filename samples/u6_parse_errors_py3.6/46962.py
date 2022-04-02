# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\websockets\uri.py
"""
The :mod:`websockets.uri` module implements parsing of WebSocket URIs
according to `section 3 of RFC 6455`_.

.. _section 3 of RFC 6455: http://tools.ietf.org/html/rfc6455#section-3

"""
import collections, urllib.parse
from .exceptions import InvalidURI
__all__ = [
 'parse_uri', 'WebSocketURI']
WebSocketURI = collections.namedtuple('WebSocketURI', ('secure', 'host', 'port', 'resource_name'))
WebSocketURI.__doc__ = "WebSocket URI.\n\n* ``secure`` is the secure flag\n* ``host`` is the lower-case host\n* ``port`` if the integer port, it's always provided even if it's the default\n* ``resource_name`` is the resource name, that is, the path and optional query\n\n"

def parse_uri--- This code section failed: ---

 L.  38         0  LOAD_GLOBAL              urllib
                2  LOAD_ATTR                parse
                4  LOAD_ATTR                urlparse
                6  LOAD_FAST                'uri'
                8  CALL_FUNCTION_1       1  '1 positional argument'
               10  STORE_FAST               'uri'

 L.  39        12  SETUP_EXCEPT        102  'to 102'

 L.  40        14  LOAD_FAST                'uri'
               16  LOAD_ATTR                scheme
               18  LOAD_CONST               ('ws', 'wss')
               20  COMPARE_OP               in
               22  POP_JUMP_IF_TRUE     28  'to 28'
               24  LOAD_ASSERT              AssertionError
               26  RAISE_VARARGS_1       1  'exception'
             28_0  COME_FROM            22  '22'

 L.  41        28  LOAD_FAST                'uri'
               30  LOAD_ATTR                params
               32  LOAD_STR                 ''
               34  COMPARE_OP               ==
               36  POP_JUMP_IF_TRUE     42  'to 42'
               38  LOAD_ASSERT              AssertionError
               40  RAISE_VARARGS_1       1  'exception'
             42_0  COME_FROM            36  '36'

 L.  42        42  LOAD_FAST                'uri'
               44  LOAD_ATTR                fragment
               46  LOAD_STR                 ''
               48  COMPARE_OP               ==
               50  POP_JUMP_IF_TRUE     56  'to 56'
               52  LOAD_ASSERT              AssertionError
               54  RAISE_VARARGS_1       1  'exception'
             56_0  COME_FROM            50  '50'

 L.  43        56  LOAD_FAST                'uri'
               58  LOAD_ATTR                username
               60  LOAD_CONST               None
               62  COMPARE_OP               is
               64  POP_JUMP_IF_TRUE     70  'to 70'
               66  LOAD_ASSERT              AssertionError
               68  RAISE_VARARGS_1       1  'exception'
             70_0  COME_FROM            64  '64'

 L.  44        70  LOAD_FAST                'uri'
               72  LOAD_ATTR                password
               74  LOAD_CONST               None
               76  COMPARE_OP               is
               78  POP_JUMP_IF_TRUE     84  'to 84'
               80  LOAD_ASSERT              AssertionError
               82  RAISE_VARARGS_1       1  'exception'
             84_0  COME_FROM            78  '78'

 L.  45        84  LOAD_FAST                'uri'
               86  LOAD_ATTR                hostname
               88  LOAD_CONST               None
               90  COMPARE_OP               is-not
               92  POP_JUMP_IF_TRUE     98  'to 98'
               94  LOAD_ASSERT              AssertionError
               96  RAISE_VARARGS_1       1  'exception'
             98_0  COME_FROM            92  '92'
               98  POP_BLOCK        
              100  JUMP_FORWARD        144  'to 144'
            102_0  COME_FROM_EXCEPT     12  '12'

 L.  46       102  DUP_TOP          
              104  LOAD_GLOBAL              AssertionError
              106  COMPARE_OP               exception-match
              108  POP_JUMP_IF_FALSE   142  'to 142'
              110  POP_TOP          
              112  STORE_FAST               'exc'
              114  POP_TOP          
              116  SETUP_FINALLY       132  'to 132'

 L.  47       118  LOAD_GLOBAL              InvalidURI
              120  CALL_FUNCTION_0       0  '0 positional arguments'
              122  LOAD_FAST                'exc'
              124  RAISE_VARARGS_2       2  'exception, parameter'
              126  POP_BLOCK        
              128  POP_EXCEPT       
              130  LOAD_CONST               None
            132_0  COME_FROM_FINALLY   116  '116'
              132  LOAD_CONST               None
              134  STORE_FAST               'exc'
              136  DELETE_FAST              'exc'
              138  END_FINALLY      
              140  JUMP_FORWARD        144  'to 144'
              142  END_FINALLY      
            144_0  COME_FROM           140  '140'
            144_1  COME_FROM           100  '100'

 L.  49       144  LOAD_FAST                'uri'
              146  LOAD_ATTR                scheme
              148  LOAD_STR                 'wss'
              150  COMPARE_OP               ==
              152  STORE_FAST               'secure'

 L.  50       154  LOAD_FAST                'uri'
              156  LOAD_ATTR                hostname
              158  STORE_FAST               'host'

 L.  51       160  LOAD_FAST                'uri'
              162  LOAD_ATTR                port
              164  JUMP_IF_TRUE_OR_POP   176  'to 176'
              166  LOAD_FAST                'secure'
              168  POP_JUMP_IF_FALSE   174  'to 174'
              170  LOAD_CONST               443
            172_0  COME_FROM           164  '164'
              172  JUMP_FORWARD        176  'to 176'
              174  ELSE                     '176'
              174  LOAD_CONST               80
            176_0  COME_FROM           172  '172'
              176  STORE_FAST               'port'

 L.  52       178  LOAD_FAST                'uri'
              180  LOAD_ATTR                path
              182  JUMP_IF_TRUE_OR_POP   186  'to 186'
              184  LOAD_STR                 '/'
            186_0  COME_FROM           182  '182'
              186  STORE_FAST               'resource_name'

 L.  53       188  LOAD_FAST                'uri'
              190  LOAD_ATTR                query
              192  POP_JUMP_IF_FALSE   208  'to 208'

 L.  54       194  LOAD_FAST                'resource_name'
              196  LOAD_STR                 '?'
              198  LOAD_FAST                'uri'
              200  LOAD_ATTR                query
              202  BINARY_ADD       
              204  INPLACE_ADD      
              206  STORE_FAST               'resource_name'
            208_0  COME_FROM           192  '192'

 L.  55       208  LOAD_GLOBAL              WebSocketURI
              210  LOAD_FAST                'secure'
              212  LOAD_FAST                'host'
              214  LOAD_FAST                'port'
              216  LOAD_FAST                'resource_name'
              218  CALL_FUNCTION_4       4  '4 positional arguments'
              220  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 172