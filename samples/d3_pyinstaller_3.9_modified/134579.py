# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: dhooks\utils.py
from base64 import b64encode
import types, functools

def copy_func(f):
    g = types.FunctionType((f.__code__), (f.__globals__), name=(f.__name__), argdefs=(f.__defaults__),
      closure=(f.__closure__))
    g = functools.update_wrapper(g, f)
    g.__kwdefaults__ = f.__kwdefaults__
    return g


def alias(*aliases):

    def decorator(func):
        new_func = copy_func(func)
        new_func.__doc__ = 'Alias for :meth:`{0.__name__}`.'.format(func)
        func._aliases = {new_func:a for a in aliases}
        return func

    return decorator


def aliased--- This code section failed: ---

 L.  26         0  LOAD_FAST                'cls'
                2  LOAD_ATTR                __dict__
                4  LOAD_METHOD              copy
                6  CALL_METHOD_0         0  ''
                8  STORE_FAST               'original_methods'

 L.  27        10  LOAD_FAST                'original_methods'
               12  LOAD_METHOD              values
               14  CALL_METHOD_0         0  ''
               16  GET_ITER         
             18_0  COME_FROM            94  '94'
             18_1  COME_FROM            30  '30'
               18  FOR_ITER             96  'to 96'
               20  STORE_FAST               'method'

 L.  28        22  LOAD_GLOBAL              hasattr
               24  LOAD_FAST                'method'
               26  LOAD_STR                 '_aliases'
               28  CALL_FUNCTION_2       2  ''
               30  POP_JUMP_IF_FALSE_BACK    18  'to 18'

 L.  29        32  LOAD_FAST                'method'
               34  LOAD_ATTR                _aliases
               36  LOAD_METHOD              items
               38  CALL_METHOD_0         0  ''
               40  GET_ITER         
             42_0  COME_FROM            92  '92'
               42  FOR_ITER             94  'to 94'
               44  UNPACK_SEQUENCE_2     2 
               46  STORE_FAST               'name'
               48  STORE_FAST               'func'

 L.  30        50  LOAD_FAST                'name'
               52  LOAD_FAST                'original_methods'
               54  LOAD_METHOD              keys
               56  CALL_METHOD_0         0  ''
               58  <118>                 0  ''
               60  POP_JUMP_IF_FALSE    80  'to 80'

 L.  31        62  LOAD_GLOBAL              ValueError
               64  LOAD_STR                 '{} already existed in {}, cannot create alias.'
               66  LOAD_METHOD              format

 L.  33        68  LOAD_FAST                'name'
               70  LOAD_FAST                'cls'
               72  LOAD_ATTR                __name__

 L.  31        74  CALL_METHOD_2         2  ''
               76  CALL_FUNCTION_1       1  ''
               78  RAISE_VARARGS_1       1  'exception instance'
             80_0  COME_FROM            60  '60'

 L.  34        80  LOAD_GLOBAL              setattr
               82  LOAD_FAST                'cls'
               84  LOAD_FAST                'name'
               86  LOAD_FAST                'func'
               88  CALL_FUNCTION_3       3  ''
               90  POP_TOP          
               92  JUMP_BACK            42  'to 42'
             94_0  COME_FROM            42  '42'
               94  JUMP_BACK            18  'to 18'
             96_0  COME_FROM            18  '18'

 L.  35        96  LOAD_FAST                'cls'
               98  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 58


def mime_type(data):
    if data.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'image/png'
    if data.startswith(b'\xff\xd8'):
        if data.rstrip(b'\x00').endswith(b'\xff\xd9'):
            return 'image/jpeg'
    if data.startswith(b'GIF87a') or (data.startswith(b'GIF89a')):
        return 'image/gif'
    raise ValueError('Unsupported image type given.')


def bytes_to_base64_data(data):
    fmt = 'data:{mime};base64,{data}'
    mime = mime_type(data)
    b64 = b64encode(data).decode('ascii')
    return fmt.format(mime=mime, data=b64)