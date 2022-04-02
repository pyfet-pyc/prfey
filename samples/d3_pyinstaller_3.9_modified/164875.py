# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: urllib3\filepost.py
from __future__ import absolute_import
import binascii, codecs, os
from io import BytesIO
from .packages import six
from packages.six import b
from .fields import RequestField
writer = codecs.lookup('utf-8')[3]

def choose_boundary():
    """
    Our embarrassingly-simple replacement for mimetools.choose_boundary.
    """
    boundary = binascii.hexlify(os.urandom(16))
    if not six.PY2:
        boundary = boundary.decode('ascii')
    return boundary


def iter_field_objects(fields):
    """
    Iterate over fields.

    Supports list of (k, v) tuples and dicts, and lists of
    :class:`~urllib3.fields.RequestField`.

    """
    if isinstance(fields, dict):
        i = six.iteritems(fields)
    else:
        i = iter(fields)
    for field in i:
        if isinstance(field, RequestField):
            yield field
        else:
            yield (RequestField.from_tuples)(*field)


def iter_fields(fields):
    """
    .. deprecated:: 1.6

    Iterate over fields.

    The addition of :class:`~urllib3.fields.RequestField` makes this function
    obsolete. Instead, use :func:`iter_field_objects`, which returns
    :class:`~urllib3.fields.RequestField` objects.

    Supports list of (k, v) tuples and dicts.
    """
    if isinstance(fields, dict):
        return ((k, v) for k, v in six.iteritems(fields))
    return ((k, v) for k, v in fields)


def encode_multipart_formdata--- This code section failed: ---

 L.  74         0  LOAD_GLOBAL              BytesIO
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'body'

 L.  75         6  LOAD_FAST                'boundary'
                8  LOAD_CONST               None
               10  <117>                 0  ''
               12  POP_JUMP_IF_FALSE    20  'to 20'

 L.  76        14  LOAD_GLOBAL              choose_boundary
               16  CALL_FUNCTION_0       0  ''
               18  STORE_FAST               'boundary'
             20_0  COME_FROM            12  '12'

 L.  78        20  LOAD_GLOBAL              iter_field_objects
               22  LOAD_FAST                'fields'
               24  CALL_FUNCTION_1       1  ''
               26  GET_ITER         
             28_0  COME_FROM           140  '140'
               28  FOR_ITER            142  'to 142'
               30  STORE_FAST               'field'

 L.  79        32  LOAD_FAST                'body'
               34  LOAD_METHOD              write
               36  LOAD_GLOBAL              b
               38  LOAD_STR                 '--%s\r\n'
               40  LOAD_FAST                'boundary'
               42  BINARY_MODULO    
               44  CALL_FUNCTION_1       1  ''
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          

 L.  81        50  LOAD_GLOBAL              writer
               52  LOAD_FAST                'body'
               54  CALL_FUNCTION_1       1  ''
               56  LOAD_METHOD              write
               58  LOAD_FAST                'field'
               60  LOAD_METHOD              render_headers
               62  CALL_METHOD_0         0  ''
               64  CALL_METHOD_1         1  ''
               66  POP_TOP          

 L.  82        68  LOAD_FAST                'field'
               70  LOAD_ATTR                data
               72  STORE_FAST               'data'

 L.  84        74  LOAD_GLOBAL              isinstance
               76  LOAD_FAST                'data'
               78  LOAD_GLOBAL              int
               80  CALL_FUNCTION_2       2  ''
               82  POP_JUMP_IF_FALSE    92  'to 92'

 L.  85        84  LOAD_GLOBAL              str
               86  LOAD_FAST                'data'
               88  CALL_FUNCTION_1       1  ''
               90  STORE_FAST               'data'
             92_0  COME_FROM            82  '82'

 L.  87        92  LOAD_GLOBAL              isinstance
               94  LOAD_FAST                'data'
               96  LOAD_GLOBAL              six
               98  LOAD_ATTR                text_type
              100  CALL_FUNCTION_2       2  ''
              102  POP_JUMP_IF_FALSE   120  'to 120'

 L.  88       104  LOAD_GLOBAL              writer
              106  LOAD_FAST                'body'
              108  CALL_FUNCTION_1       1  ''
              110  LOAD_METHOD              write
              112  LOAD_FAST                'data'
              114  CALL_METHOD_1         1  ''
              116  POP_TOP          
              118  JUMP_FORWARD        130  'to 130'
            120_0  COME_FROM           102  '102'

 L.  90       120  LOAD_FAST                'body'
              122  LOAD_METHOD              write
              124  LOAD_FAST                'data'
              126  CALL_METHOD_1         1  ''
              128  POP_TOP          
            130_0  COME_FROM           118  '118'

 L.  92       130  LOAD_FAST                'body'
              132  LOAD_METHOD              write
              134  LOAD_CONST               b'\r\n'
              136  CALL_METHOD_1         1  ''
              138  POP_TOP          
              140  JUMP_BACK            28  'to 28'
            142_0  COME_FROM            28  '28'

 L.  94       142  LOAD_FAST                'body'
              144  LOAD_METHOD              write
              146  LOAD_GLOBAL              b
              148  LOAD_STR                 '--%s--\r\n'
              150  LOAD_FAST                'boundary'
              152  BINARY_MODULO    
              154  CALL_FUNCTION_1       1  ''
              156  CALL_METHOD_1         1  ''
              158  POP_TOP          

 L.  96       160  LOAD_GLOBAL              str
              162  LOAD_STR                 'multipart/form-data; boundary=%s'
              164  LOAD_FAST                'boundary'
              166  BINARY_MODULO    
              168  CALL_FUNCTION_1       1  ''
              170  STORE_FAST               'content_type'

 L.  98       172  LOAD_FAST                'body'
              174  LOAD_METHOD              getvalue
              176  CALL_METHOD_0         0  ''
              178  LOAD_FAST                'content_type'
              180  BUILD_TUPLE_2         2 
              182  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 10