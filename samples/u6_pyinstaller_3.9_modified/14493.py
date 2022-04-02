# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: urllib3\fields.py
from __future__ import absolute_import
import email.utils, mimetypes
from .packages import six

def guess_content_type(filename, default='application/octet-stream'):
    """
    Guess the "Content-Type" of a file.

    :param filename:
        The filename to guess the "Content-Type" of using :mod:`mimetypes`.
    :param default:
        If no "Content-Type" can be guessed, default to `default`.
    """
    if filename:
        return mimetypes.guess_type(filename)[0] or default
    return default


def format_header_param--- This code section failed: ---

 L.  35         0  LOAD_GLOBAL              any
                2  LOAD_CLOSURE             'value'
                4  BUILD_TUPLE_1         1 
                6  LOAD_GENEXPR             '<code_object <genexpr>>'
                8  LOAD_STR                 'format_header_param.<locals>.<genexpr>'
               10  MAKE_FUNCTION_8          'closure'
               12  LOAD_STR                 '"\\\r\n'
               14  GET_ITER         
               16  CALL_FUNCTION_1       1  ''
               18  CALL_FUNCTION_1       1  ''
               20  POP_JUMP_IF_TRUE     76  'to 76'

 L.  36        22  LOAD_STR                 '%s="%s"'
               24  LOAD_FAST                'name'
               26  LOAD_DEREF               'value'
               28  BUILD_TUPLE_2         2 
               30  BINARY_MODULO    
               32  STORE_FAST               'result'

 L.  37        34  SETUP_FINALLY        50  'to 50'

 L.  38        36  LOAD_FAST                'result'
               38  LOAD_METHOD              encode
               40  LOAD_STR                 'ascii'
               42  CALL_METHOD_1         1  ''
               44  POP_TOP          
               46  POP_BLOCK        
               48  JUMP_FORWARD         72  'to 72'
             50_0  COME_FROM_FINALLY    34  '34'

 L.  39        50  DUP_TOP          
               52  LOAD_GLOBAL              UnicodeEncodeError
               54  LOAD_GLOBAL              UnicodeDecodeError
               56  BUILD_TUPLE_2         2 
               58  <121>                70  ''
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L.  40        66  POP_EXCEPT       
               68  JUMP_FORWARD         76  'to 76'
               70  <48>             
             72_0  COME_FROM            48  '48'

 L.  42        72  LOAD_FAST                'result'
               74  RETURN_VALUE     
             76_0  COME_FROM            68  '68'
             76_1  COME_FROM            20  '20'

 L.  43        76  LOAD_GLOBAL              six
               78  LOAD_ATTR                PY3
               80  POP_JUMP_IF_TRUE    104  'to 104'
               82  LOAD_GLOBAL              isinstance
               84  LOAD_DEREF               'value'
               86  LOAD_GLOBAL              six
               88  LOAD_ATTR                text_type
               90  CALL_FUNCTION_2       2  ''
               92  POP_JUMP_IF_FALSE   104  'to 104'

 L.  44        94  LOAD_DEREF               'value'
               96  LOAD_METHOD              encode
               98  LOAD_STR                 'utf-8'
              100  CALL_METHOD_1         1  ''
              102  STORE_DEREF              'value'
            104_0  COME_FROM            92  '92'
            104_1  COME_FROM            80  '80'

 L.  45       104  LOAD_GLOBAL              email
              106  LOAD_ATTR                utils
              108  LOAD_METHOD              encode_rfc2231
              110  LOAD_DEREF               'value'
              112  LOAD_STR                 'utf-8'
              114  CALL_METHOD_2         2  ''
              116  STORE_DEREF              'value'

 L.  46       118  LOAD_STR                 '%s*=%s'
              120  LOAD_FAST                'name'
              122  LOAD_DEREF               'value'
              124  BUILD_TUPLE_2         2 
              126  BINARY_MODULO    
              128  STORE_DEREF              'value'

 L.  47       130  LOAD_DEREF               'value'
              132  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 58


class RequestField(object):
    __doc__ = '\n    A data container for request body parameters.\n\n    :param name:\n        The name of this request field.\n    :param data:\n        The data/value body.\n    :param filename:\n        An optional filename of the request field.\n    :param headers:\n        An optional dict-like object of headers to initially use for the field.\n    '

    def __init__(self, name, data, filename=None, headers=None):
        self._name = name
        self._filename = filename
        self.data = data
        self.headers = {}
        if headers:
            self.headers = dict(headers)

    @classmethod
    def from_tuples(cls, fieldname, value):
        """
        A :class:`~urllib3.fields.RequestField` factory from old-style tuple parameters.

        Supports constructing :class:`~urllib3.fields.RequestField` from
        parameter of key/value strings AND key/filetuple. A filetuple is a
        (filename, data, MIME type) tuple where the MIME type is optional.
        For example::

            'foo': 'bar',
            'fakefile': ('foofile.txt', 'contents of foofile'),
            'realfile': ('barfile.txt', open('realfile').read()),
            'typedfile': ('bazfile.bin', open('bazfile').read(), 'image/jpeg'),
            'nonamefile': 'contents of nonamefile field',

        Field names and filenames must be unicode.
        """
        if isinstancevaluetuple:
            if len(value) == 3:
                filename, data, content_type = value
            else:
                filename, data = value
                content_type = guess_content_type(filename)
        else:
            filename = None
            content_type = None
            data = value
        request_param = cls(fieldname, data, filename=filename)
        request_param.make_multipart(content_type=content_type)
        return request_param

    def _render_part(self, name, value):
        """
        Overridable helper function to format a single header parameter.

        :param name:
            The name of the parameter, a string expected to be ASCII only.
        :param value:
            The value of the parameter, provided as a unicode string.
        """
        return format_header_paramnamevalue

    def _render_parts--- This code section failed: ---

 L. 127         0  BUILD_LIST_0          0 
                2  STORE_FAST               'parts'

 L. 128         4  LOAD_FAST                'header_parts'
                6  STORE_FAST               'iterable'

 L. 129         8  LOAD_GLOBAL              isinstance
               10  LOAD_FAST                'header_parts'
               12  LOAD_GLOBAL              dict
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_FALSE    26  'to 26'

 L. 130        18  LOAD_FAST                'header_parts'
               20  LOAD_METHOD              items
               22  CALL_METHOD_0         0  ''
               24  STORE_FAST               'iterable'
             26_0  COME_FROM            16  '16'

 L. 132        26  LOAD_FAST                'iterable'
               28  GET_ITER         
             30_0  COME_FROM            44  '44'
               30  FOR_ITER             66  'to 66'
               32  UNPACK_SEQUENCE_2     2 
               34  STORE_FAST               'name'
               36  STORE_FAST               'value'

 L. 133        38  LOAD_FAST                'value'
               40  LOAD_CONST               None
               42  <117>                 1  ''
               44  POP_JUMP_IF_FALSE    30  'to 30'

 L. 134        46  LOAD_FAST                'parts'
               48  LOAD_METHOD              append
               50  LOAD_FAST                'self'
               52  LOAD_METHOD              _render_part
               54  LOAD_FAST                'name'
               56  LOAD_FAST                'value'
               58  CALL_METHOD_2         2  ''
               60  CALL_METHOD_1         1  ''
               62  POP_TOP          
               64  JUMP_BACK            30  'to 30'

 L. 136        66  LOAD_STR                 '; '
               68  LOAD_METHOD              join
               70  LOAD_FAST                'parts'
               72  CALL_METHOD_1         1  ''
               74  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 42

    def render_headers--- This code section failed: ---

 L. 142         0  BUILD_LIST_0          0 
                2  STORE_FAST               'lines'

 L. 144         4  BUILD_LIST_0          0 
                6  LOAD_CONST               ('Content-Disposition', 'Content-Type', 'Content-Location')
                8  CALL_FINALLY         11  'to 11'
               10  STORE_FAST               'sort_keys'

 L. 145        12  LOAD_FAST                'sort_keys'
               14  GET_ITER         
             16_0  COME_FROM            32  '32'
               16  FOR_ITER             60  'to 60'
               18  STORE_FAST               'sort_key'

 L. 146        20  LOAD_FAST                'self'
               22  LOAD_ATTR                headers
               24  LOAD_METHOD              get
               26  LOAD_FAST                'sort_key'
               28  LOAD_CONST               False
               30  CALL_METHOD_2         2  ''
               32  POP_JUMP_IF_FALSE    16  'to 16'

 L. 147        34  LOAD_FAST                'lines'
               36  LOAD_METHOD              append
               38  LOAD_STR                 '%s: %s'
               40  LOAD_FAST                'sort_key'
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                headers
               46  LOAD_FAST                'sort_key'
               48  BINARY_SUBSCR    
               50  BUILD_TUPLE_2         2 
               52  BINARY_MODULO    
               54  CALL_METHOD_1         1  ''
               56  POP_TOP          
               58  JUMP_BACK            16  'to 16'

 L. 149        60  LOAD_FAST                'self'
               62  LOAD_ATTR                headers
               64  LOAD_METHOD              items
               66  CALL_METHOD_0         0  ''
               68  GET_ITER         
             70_0  COME_FROM            88  '88'
             70_1  COME_FROM            84  '84'
               70  FOR_ITER            110  'to 110'
               72  UNPACK_SEQUENCE_2     2 
               74  STORE_FAST               'header_name'
               76  STORE_FAST               'header_value'

 L. 150        78  LOAD_FAST                'header_name'
               80  LOAD_FAST                'sort_keys'
               82  <118>                 1  ''
               84  POP_JUMP_IF_FALSE    70  'to 70'

 L. 151        86  LOAD_FAST                'header_value'
               88  POP_JUMP_IF_FALSE    70  'to 70'

 L. 152        90  LOAD_FAST                'lines'
               92  LOAD_METHOD              append
               94  LOAD_STR                 '%s: %s'
               96  LOAD_FAST                'header_name'
               98  LOAD_FAST                'header_value'
              100  BUILD_TUPLE_2         2 
              102  BINARY_MODULO    
              104  CALL_METHOD_1         1  ''
              106  POP_TOP          
              108  JUMP_BACK            70  'to 70'

 L. 154       110  LOAD_FAST                'lines'
              112  LOAD_METHOD              append
              114  LOAD_STR                 '\r\n'
              116  CALL_METHOD_1         1  ''
              118  POP_TOP          

 L. 155       120  LOAD_STR                 '\r\n'
              122  LOAD_METHOD              join
              124  LOAD_FAST                'lines'
              126  CALL_METHOD_1         1  ''
              128  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 8

    def make_multipart(self, content_disposition=None, content_type=None, content_location=None):
        """
        Makes this request field into a multipart request field.

        This method overrides "Content-Disposition", "Content-Type" and
        "Content-Location" headers to the request parameter.

        :param content_type:
            The 'Content-Type' of the request body.
        :param content_location:
            The 'Content-Location' of the request body.

        """
        self.headers['Content-Disposition'] = content_disposition or 'form-data'
        self.headers['Content-Disposition'] += '; '.join([
         '',
         self._render_parts((
          (
           'name', self._name), ('filename', self._filename)))])
        self.headers['Content-Type'] = content_type
        self.headers['Content-Location'] = content_location