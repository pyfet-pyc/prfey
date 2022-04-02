# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cryptography\hazmat\_oid.py
from __future__ import absolute_import, division, print_function
from cryptography import utils

class ObjectIdentifier(object):

    def __init__--- This code section failed: ---

 L.  12         0  LOAD_FAST                'dotted_string'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               _dotted_string

 L.  14         6  LOAD_FAST                'self'
                8  LOAD_ATTR                _dotted_string
               10  LOAD_METHOD              split
               12  LOAD_STR                 '.'
               14  CALL_METHOD_1         1  ''
               16  STORE_FAST               'nodes'

 L.  15        18  BUILD_LIST_0          0 
               20  STORE_FAST               'intnodes'

 L.  20        22  LOAD_FAST                'nodes'
               24  GET_ITER         
             26_0  COME_FROM           110  '110'
               26  FOR_ITER            112  'to 112'
               28  STORE_FAST               'node'

 L.  21        30  SETUP_FINALLY        46  'to 46'

 L.  22        32  LOAD_GLOBAL              int
               34  LOAD_FAST                'node'
               36  LOAD_CONST               10
               38  CALL_FUNCTION_2       2  ''
               40  STORE_FAST               'node_value'
               42  POP_BLOCK        
               44  JUMP_FORWARD         78  'to 78'
             46_0  COME_FROM_FINALLY    30  '30'

 L.  23        46  DUP_TOP          
               48  LOAD_GLOBAL              ValueError
               50  <121>                76  ''
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          

 L.  24        58  LOAD_GLOBAL              ValueError

 L.  25        60  LOAD_STR                 'Malformed OID: %s (non-integer nodes)'

 L.  26        62  LOAD_FAST                'self'
               64  LOAD_ATTR                _dotted_string

 L.  25        66  BINARY_MODULO    

 L.  24        68  CALL_FUNCTION_1       1  ''
               70  RAISE_VARARGS_1       1  'exception instance'
               72  POP_EXCEPT       
               74  JUMP_FORWARD         78  'to 78'
               76  <48>             
             78_0  COME_FROM            74  '74'
             78_1  COME_FROM            44  '44'

 L.  28        78  LOAD_FAST                'node_value'
               80  LOAD_CONST               0
               82  COMPARE_OP               <
               84  POP_JUMP_IF_FALSE   100  'to 100'

 L.  29        86  LOAD_GLOBAL              ValueError

 L.  30        88  LOAD_STR                 'Malformed OID: %s (negative-integer nodes)'

 L.  31        90  LOAD_FAST                'self'
               92  LOAD_ATTR                _dotted_string

 L.  30        94  BINARY_MODULO    

 L.  29        96  CALL_FUNCTION_1       1  ''
               98  RAISE_VARARGS_1       1  'exception instance'
            100_0  COME_FROM            84  '84'

 L.  33       100  LOAD_FAST                'intnodes'
              102  LOAD_METHOD              append
              104  LOAD_FAST                'node_value'
              106  CALL_METHOD_1         1  ''
              108  POP_TOP          
              110  JUMP_BACK            26  'to 26'
            112_0  COME_FROM            26  '26'

 L.  35       112  LOAD_GLOBAL              len
              114  LOAD_FAST                'nodes'
              116  CALL_FUNCTION_1       1  ''
              118  LOAD_CONST               2
              120  COMPARE_OP               <
              122  POP_JUMP_IF_FALSE   138  'to 138'

 L.  36       124  LOAD_GLOBAL              ValueError

 L.  37       126  LOAD_STR                 'Malformed OID: %s (insufficient number of nodes)'

 L.  38       128  LOAD_FAST                'self'
              130  LOAD_ATTR                _dotted_string

 L.  37       132  BINARY_MODULO    

 L.  36       134  CALL_FUNCTION_1       1  ''
              136  RAISE_VARARGS_1       1  'exception instance'
            138_0  COME_FROM           122  '122'

 L.  41       138  LOAD_FAST                'intnodes'
              140  LOAD_CONST               0
              142  BINARY_SUBSCR    
              144  LOAD_CONST               2
              146  COMPARE_OP               >
              148  POP_JUMP_IF_FALSE   164  'to 164'

 L.  42       150  LOAD_GLOBAL              ValueError

 L.  43       152  LOAD_STR                 'Malformed OID: %s (first node outside valid range)'

 L.  44       154  LOAD_FAST                'self'
              156  LOAD_ATTR                _dotted_string

 L.  43       158  BINARY_MODULO    

 L.  42       160  CALL_FUNCTION_1       1  ''
              162  RAISE_VARARGS_1       1  'exception instance'
            164_0  COME_FROM           148  '148'

 L.  47       164  LOAD_FAST                'intnodes'
              166  LOAD_CONST               0
              168  BINARY_SUBSCR    
              170  LOAD_CONST               2
              172  COMPARE_OP               <
              174  POP_JUMP_IF_FALSE   202  'to 202'
              176  LOAD_FAST                'intnodes'
              178  LOAD_CONST               1
              180  BINARY_SUBSCR    
              182  LOAD_CONST               40
              184  COMPARE_OP               >=
              186  POP_JUMP_IF_FALSE   202  'to 202'

 L.  48       188  LOAD_GLOBAL              ValueError

 L.  49       190  LOAD_STR                 'Malformed OID: %s (second node outside valid range)'

 L.  50       192  LOAD_FAST                'self'
              194  LOAD_ATTR                _dotted_string

 L.  49       196  BINARY_MODULO    

 L.  48       198  CALL_FUNCTION_1       1  ''
              200  RAISE_VARARGS_1       1  'exception instance'
            202_0  COME_FROM           186  '186'
            202_1  COME_FROM           174  '174'

Parse error at or near `<121>' instruction at offset 50

    def __eq__(self, other):
        if not isinstanceotherObjectIdentifier:
            return NotImplemented
        return self.dotted_string == other.dotted_string

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return '<ObjectIdentifier(oid={}, name={})>'.format(self.dotted_string, self._name)

    def __hash__(self):
        return hash(self.dotted_string)

    @property
    def _name(self):
        from cryptography.x509.oid import _OID_NAMES
        return _OID_NAMES.get(self, 'Unknown OID')

    dotted_string = utils.read_only_property('_dotted_string')