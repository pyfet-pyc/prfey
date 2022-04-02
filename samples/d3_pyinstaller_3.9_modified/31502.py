# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: Crypto\Util\Padding.py
__all__ = [
 'pad', 'unpad']
from Crypto.Util.py3compat import *

def pad(data_to_pad, block_size, style='pkcs7'):
    """Apply standard padding.

    Args:
      data_to_pad (byte string):
        The data that needs to be padded.
      block_size (integer):
        The block boundary to use for padding. The output length is guaranteed
        to be a multiple of :data:`block_size`.
      style (string):
        Padding algorithm. It can be *'pkcs7'* (default), *'iso7816'* or *'x923'*.

    Return:
      byte string : the original data with the appropriate padding added at the end.
    """
    padding_len = block_size - len(data_to_pad) % block_size
    if style == 'pkcs7':
        padding = bchr(padding_len) * padding_len
    elif style == 'x923':
        padding = bchr(0) * (padding_len - 1) + bchr(padding_len)
    elif style == 'iso7816':
        padding = bchr(128) + bchr(0) * (padding_len - 1)
    else:
        raise ValueError('Unknown padding style')
    return data_to_pad + padding


def unpad--- This code section failed: ---

 L.  84         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'padded_data'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'pdata_len'

 L.  85         8  LOAD_FAST                'pdata_len'
               10  LOAD_FAST                'block_size'
               12  BINARY_MODULO    
               14  POP_JUMP_IF_FALSE    24  'to 24'

 L.  86        16  LOAD_GLOBAL              ValueError
               18  LOAD_STR                 'Input data is not padded'
               20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            14  '14'

 L.  87        24  LOAD_FAST                'style'
               26  LOAD_CONST               ('pkcs7', 'x923')
               28  <118>                 0  ''
               30  POP_JUMP_IF_FALSE   158  'to 158'

 L.  88        32  LOAD_GLOBAL              bord
               34  LOAD_FAST                'padded_data'
               36  LOAD_CONST               -1
               38  BINARY_SUBSCR    
               40  CALL_FUNCTION_1       1  ''
               42  STORE_FAST               'padding_len'

 L.  89        44  LOAD_FAST                'padding_len'
               46  LOAD_CONST               1
               48  COMPARE_OP               <
               50  POP_JUMP_IF_TRUE     66  'to 66'
               52  LOAD_FAST                'padding_len'
               54  LOAD_GLOBAL              min
               56  LOAD_FAST                'block_size'
               58  LOAD_FAST                'pdata_len'
               60  CALL_FUNCTION_2       2  ''
               62  COMPARE_OP               >
               64  POP_JUMP_IF_FALSE    74  'to 74'
             66_0  COME_FROM            50  '50'

 L.  90        66  LOAD_GLOBAL              ValueError
               68  LOAD_STR                 'Padding is incorrect.'
               70  CALL_FUNCTION_1       1  ''
               72  RAISE_VARARGS_1       1  'exception instance'
             74_0  COME_FROM            64  '64'

 L.  91        74  LOAD_FAST                'style'
               76  LOAD_STR                 'pkcs7'
               78  COMPARE_OP               ==
               80  POP_JUMP_IF_FALSE   118  'to 118'

 L.  92        82  LOAD_FAST                'padded_data'
               84  LOAD_FAST                'padding_len'
               86  UNARY_NEGATIVE   
               88  LOAD_CONST               None
               90  BUILD_SLICE_2         2 
               92  BINARY_SUBSCR    
               94  LOAD_GLOBAL              bchr
               96  LOAD_FAST                'padding_len'
               98  CALL_FUNCTION_1       1  ''
              100  LOAD_FAST                'padding_len'
              102  BINARY_MULTIPLY  
              104  COMPARE_OP               !=
              106  POP_JUMP_IF_FALSE   156  'to 156'

 L.  93       108  LOAD_GLOBAL              ValueError
              110  LOAD_STR                 'PKCS#7 padding is incorrect.'
              112  CALL_FUNCTION_1       1  ''
              114  RAISE_VARARGS_1       1  'exception instance'
              116  JUMP_FORWARD        156  'to 156'
            118_0  COME_FROM            80  '80'

 L.  95       118  LOAD_FAST                'padded_data'
              120  LOAD_FAST                'padding_len'
              122  UNARY_NEGATIVE   
              124  LOAD_CONST               -1
              126  BUILD_SLICE_2         2 
              128  BINARY_SUBSCR    
              130  LOAD_GLOBAL              bchr
              132  LOAD_CONST               0
              134  CALL_FUNCTION_1       1  ''
              136  LOAD_FAST                'padding_len'
              138  LOAD_CONST               1
              140  BINARY_SUBTRACT  
              142  BINARY_MULTIPLY  
              144  COMPARE_OP               !=
              146  POP_JUMP_IF_FALSE   156  'to 156'

 L.  96       148  LOAD_GLOBAL              ValueError
              150  LOAD_STR                 'ANSI X.923 padding is incorrect.'
              152  CALL_FUNCTION_1       1  ''
              154  RAISE_VARARGS_1       1  'exception instance'
            156_0  COME_FROM           146  '146'
            156_1  COME_FROM           116  '116'
            156_2  COME_FROM           106  '106'
              156  JUMP_FORWARD        278  'to 278'
            158_0  COME_FROM            30  '30'

 L.  97       158  LOAD_FAST                'style'
              160  LOAD_STR                 'iso7816'
              162  COMPARE_OP               ==
          164_166  POP_JUMP_IF_FALSE   270  'to 270'

 L.  98       168  LOAD_FAST                'pdata_len'
              170  LOAD_FAST                'padded_data'
              172  LOAD_METHOD              rfind
              174  LOAD_GLOBAL              bchr
              176  LOAD_CONST               128
              178  CALL_FUNCTION_1       1  ''
              180  CALL_METHOD_1         1  ''
              182  BINARY_SUBTRACT  
              184  STORE_FAST               'padding_len'

 L.  99       186  LOAD_FAST                'padding_len'
              188  LOAD_CONST               1
              190  COMPARE_OP               <
              192  POP_JUMP_IF_TRUE    208  'to 208'
              194  LOAD_FAST                'padding_len'
              196  LOAD_GLOBAL              min
              198  LOAD_FAST                'block_size'
              200  LOAD_FAST                'pdata_len'
              202  CALL_FUNCTION_2       2  ''
              204  COMPARE_OP               >
              206  POP_JUMP_IF_FALSE   216  'to 216'
            208_0  COME_FROM           192  '192'

 L. 100       208  LOAD_GLOBAL              ValueError
              210  LOAD_STR                 'Padding is incorrect.'
              212  CALL_FUNCTION_1       1  ''
              214  RAISE_VARARGS_1       1  'exception instance'
            216_0  COME_FROM           206  '206'

 L. 101       216  LOAD_FAST                'padding_len'
              218  LOAD_CONST               1
              220  COMPARE_OP               >
          222_224  POP_JUMP_IF_FALSE   278  'to 278'
              226  LOAD_FAST                'padded_data'
              228  LOAD_CONST               1
              230  LOAD_FAST                'padding_len'
              232  BINARY_SUBTRACT  
              234  LOAD_CONST               None
              236  BUILD_SLICE_2         2 
              238  BINARY_SUBSCR    
              240  LOAD_GLOBAL              bchr
              242  LOAD_CONST               0
              244  CALL_FUNCTION_1       1  ''
              246  LOAD_FAST                'padding_len'
              248  LOAD_CONST               1
              250  BINARY_SUBTRACT  
              252  BINARY_MULTIPLY  
              254  COMPARE_OP               !=
          256_258  POP_JUMP_IF_FALSE   278  'to 278'

 L. 102       260  LOAD_GLOBAL              ValueError
              262  LOAD_STR                 'ISO 7816-4 padding is incorrect.'
              264  CALL_FUNCTION_1       1  ''
              266  RAISE_VARARGS_1       1  'exception instance'
              268  JUMP_FORWARD        278  'to 278'
            270_0  COME_FROM           164  '164'

 L. 104       270  LOAD_GLOBAL              ValueError
              272  LOAD_STR                 'Unknown padding style'
              274  CALL_FUNCTION_1       1  ''
              276  RAISE_VARARGS_1       1  'exception instance'
            278_0  COME_FROM           268  '268'
            278_1  COME_FROM           256  '256'
            278_2  COME_FROM           222  '222'
            278_3  COME_FROM           156  '156'

 L. 105       278  LOAD_FAST                'padded_data'
              280  LOAD_CONST               None
              282  LOAD_FAST                'padding_len'
              284  UNARY_NEGATIVE   
              286  BUILD_SLICE_2         2 
              288  BINARY_SUBSCR    
              290  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 28