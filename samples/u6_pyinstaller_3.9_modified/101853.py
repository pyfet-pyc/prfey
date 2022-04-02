# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: xml\dom\domreg.py
"""Registration facilities for DOM. This module should not be used
directly. Instead, the functions getDOMImplementation and
registerDOMImplementation should be imported from xml.dom."""
import sys
well_known_implementations = {'minidom':'xml.dom.minidom', 
 '4DOM':'xml.dom.DOMImplementation'}
registered = {}

def registerDOMImplementation(name, factory):
    """registerDOMImplementation(name, factory)

    Register the factory function with the name. The factory function
    should return an object which implements the DOMImplementation
    interface. The factory function can either return the same object,
    or a new one (e.g. if that implementation supports some
    customization)."""
    registered[name] = factory


def _good_enough(dom, features):
    """_good_enough(dom, features) -> Return 1 if the dom offers the features"""
    for f, v in features:
        if not dom.hasFeature(f, v):
            return 0
        return 1


def getDOMImplementation--- This code section failed: ---

 L.  52         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              os
                6  STORE_FAST               'os'

 L.  53         8  LOAD_CONST               None
               10  STORE_FAST               'creator'

 L.  54        12  LOAD_GLOBAL              well_known_implementations
               14  LOAD_METHOD              get
               16  LOAD_FAST                'name'
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'mod'

 L.  55        22  LOAD_FAST                'mod'
               24  POP_JUMP_IF_FALSE    50  'to 50'

 L.  56        26  LOAD_GLOBAL              __import__
               28  LOAD_FAST                'mod'
               30  BUILD_MAP_0           0 
               32  BUILD_MAP_0           0 
               34  LOAD_STR                 'getDOMImplementation'
               36  BUILD_LIST_1          1 
               38  CALL_FUNCTION_4       4  ''
               40  STORE_FAST               'mod'

 L.  57        42  LOAD_FAST                'mod'
               44  LOAD_METHOD              getDOMImplementation
               46  CALL_METHOD_0         0  ''
               48  RETURN_VALUE     
             50_0  COME_FROM            24  '24'

 L.  58        50  LOAD_FAST                'name'
               52  POP_JUMP_IF_FALSE    64  'to 64'

 L.  59        54  LOAD_GLOBAL              registered
               56  LOAD_FAST                'name'
               58  BINARY_SUBSCR    
               60  CALL_FUNCTION_0       0  ''
               62  RETURN_VALUE     
             64_0  COME_FROM            52  '52'

 L.  60        64  LOAD_GLOBAL              sys
               66  LOAD_ATTR                flags
               68  LOAD_ATTR                ignore_environment
               70  POP_JUMP_IF_TRUE     98  'to 98'
               72  LOAD_STR                 'PYTHON_DOM'
               74  LOAD_FAST                'os'
               76  LOAD_ATTR                environ
               78  <118>                 0  ''
               80  POP_JUMP_IF_FALSE    98  'to 98'

 L.  61        82  LOAD_GLOBAL              getDOMImplementation
               84  LOAD_FAST                'os'
               86  LOAD_ATTR                environ
               88  LOAD_STR                 'PYTHON_DOM'
               90  BINARY_SUBSCR    
               92  LOAD_CONST               ('name',)
               94  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               96  RETURN_VALUE     
             98_0  COME_FROM            80  '80'
             98_1  COME_FROM            70  '70'

 L.  65        98  LOAD_GLOBAL              isinstance
              100  LOAD_FAST                'features'
              102  LOAD_GLOBAL              str
              104  CALL_FUNCTION_2       2  ''
              106  POP_JUMP_IF_FALSE   116  'to 116'

 L.  66       108  LOAD_GLOBAL              _parse_feature_string
              110  LOAD_FAST                'features'
              112  CALL_FUNCTION_1       1  ''
              114  STORE_FAST               'features'
            116_0  COME_FROM           106  '106'

 L.  67       116  LOAD_GLOBAL              registered
              118  LOAD_METHOD              values
              120  CALL_METHOD_0         0  ''
              122  GET_ITER         
            124_0  COME_FROM           142  '142'
              124  FOR_ITER            154  'to 154'
              126  STORE_FAST               'creator'

 L.  68       128  LOAD_FAST                'creator'
              130  CALL_FUNCTION_0       0  ''
              132  STORE_FAST               'dom'

 L.  69       134  LOAD_GLOBAL              _good_enough
              136  LOAD_FAST                'dom'
              138  LOAD_FAST                'features'
              140  CALL_FUNCTION_2       2  ''
              142  POP_JUMP_IF_FALSE   124  'to 124'

 L.  70       144  LOAD_FAST                'dom'
              146  ROT_TWO          
              148  POP_TOP          
              150  RETURN_VALUE     
              152  JUMP_BACK           124  'to 124'

 L.  72       154  LOAD_GLOBAL              well_known_implementations
              156  LOAD_METHOD              keys
              158  CALL_METHOD_0         0  ''
              160  GET_ITER         
            162_0  COME_FROM           212  '212'
              162  FOR_ITER            224  'to 224'
              164  STORE_FAST               'creator'

 L.  73       166  SETUP_FINALLY       182  'to 182'

 L.  74       168  LOAD_GLOBAL              getDOMImplementation
              170  LOAD_FAST                'creator'
              172  LOAD_CONST               ('name',)
              174  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              176  STORE_FAST               'dom'
              178  POP_BLOCK        
              180  JUMP_FORWARD        204  'to 204'
            182_0  COME_FROM_FINALLY   166  '166'

 L.  75       182  DUP_TOP          
              184  LOAD_GLOBAL              Exception
              186  <121>               202  ''
              188  POP_TOP          
              190  POP_TOP          
              192  POP_TOP          

 L.  76       194  POP_EXCEPT       
              196  JUMP_BACK           162  'to 162'
              198  POP_EXCEPT       
              200  JUMP_FORWARD        204  'to 204'
              202  <48>             
            204_0  COME_FROM           200  '200'
            204_1  COME_FROM           180  '180'

 L.  77       204  LOAD_GLOBAL              _good_enough
              206  LOAD_FAST                'dom'
              208  LOAD_FAST                'features'
              210  CALL_FUNCTION_2       2  ''
              212  POP_JUMP_IF_FALSE   162  'to 162'

 L.  78       214  LOAD_FAST                'dom'
              216  ROT_TWO          
              218  POP_TOP          
              220  RETURN_VALUE     
              222  JUMP_BACK           162  'to 162'

 L.  80       224  LOAD_GLOBAL              ImportError
              226  LOAD_STR                 'no suitable DOM implementation found'
              228  CALL_FUNCTION_1       1  ''
              230  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<118>' instruction at offset 78


def _parse_feature_string--- This code section failed: ---

 L.  83         0  BUILD_LIST_0          0 
                2  STORE_FAST               'features'

 L.  84         4  LOAD_FAST                's'
                6  LOAD_METHOD              split
                8  CALL_METHOD_0         0  ''
               10  STORE_FAST               'parts'

 L.  85        12  LOAD_CONST               0
               14  STORE_FAST               'i'

 L.  86        16  LOAD_GLOBAL              len
               18  LOAD_FAST                'parts'
               20  CALL_FUNCTION_1       1  ''
               22  STORE_FAST               'length'

 L.  87        24  LOAD_FAST                'i'
               26  LOAD_FAST                'length'
               28  COMPARE_OP               <
               30  POP_JUMP_IF_FALSE   134  'to 134'

 L.  88        32  LOAD_FAST                'parts'
               34  LOAD_FAST                'i'
               36  BINARY_SUBSCR    
               38  STORE_FAST               'feature'

 L.  89        40  LOAD_FAST                'feature'
               42  LOAD_CONST               0
               44  BINARY_SUBSCR    
               46  LOAD_STR                 '0123456789'
               48  <118>                 0  ''
               50  POP_JUMP_IF_FALSE    66  'to 66'

 L.  90        52  LOAD_GLOBAL              ValueError
               54  LOAD_STR                 'bad feature name: %r'
               56  LOAD_FAST                'feature'
               58  BUILD_TUPLE_1         1 
               60  BINARY_MODULO    
               62  CALL_FUNCTION_1       1  ''
               64  RAISE_VARARGS_1       1  'exception instance'
             66_0  COME_FROM            50  '50'

 L.  91        66  LOAD_FAST                'i'
               68  LOAD_CONST               1
               70  BINARY_ADD       
               72  STORE_FAST               'i'

 L.  92        74  LOAD_CONST               None
               76  STORE_FAST               'version'

 L.  93        78  LOAD_FAST                'i'
               80  LOAD_FAST                'length'
               82  COMPARE_OP               <
               84  POP_JUMP_IF_FALSE   118  'to 118'

 L.  94        86  LOAD_FAST                'parts'
               88  LOAD_FAST                'i'
               90  BINARY_SUBSCR    
               92  STORE_FAST               'v'

 L.  95        94  LOAD_FAST                'v'
               96  LOAD_CONST               0
               98  BINARY_SUBSCR    
              100  LOAD_STR                 '0123456789'
              102  <118>                 0  ''
              104  POP_JUMP_IF_FALSE   118  'to 118'

 L.  96       106  LOAD_FAST                'i'
              108  LOAD_CONST               1
              110  BINARY_ADD       
              112  STORE_FAST               'i'

 L.  97       114  LOAD_FAST                'v'
              116  STORE_FAST               'version'
            118_0  COME_FROM           104  '104'
            118_1  COME_FROM            84  '84'

 L.  98       118  LOAD_FAST                'features'
              120  LOAD_METHOD              append
              122  LOAD_FAST                'feature'
              124  LOAD_FAST                'version'
              126  BUILD_TUPLE_2         2 
              128  CALL_METHOD_1         1  ''
              130  POP_TOP          
              132  JUMP_BACK            24  'to 24'
            134_0  COME_FROM            30  '30'

 L.  99       134  LOAD_GLOBAL              tuple
              136  LOAD_FAST                'features'
              138  CALL_FUNCTION_1       1  ''
              140  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 48