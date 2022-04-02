# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: cffi\error.py


class FFIError(Exception):
    __module__ = 'cffi'


class CDefError(Exception):
    __module__ = 'cffi'

    def __str__--- This code section failed: ---

 L.   8         0  SETUP_FINALLY        44  'to 44'

 L.   9         2  LOAD_FAST                'self'
                4  LOAD_ATTR                args
                6  LOAD_CONST               1
                8  BINARY_SUBSCR    
               10  STORE_FAST               'current_decl'

 L.  10        12  LOAD_FAST                'current_decl'
               14  LOAD_ATTR                coord
               16  LOAD_ATTR                file
               18  STORE_FAST               'filename'

 L.  11        20  LOAD_FAST                'current_decl'
               22  LOAD_ATTR                coord
               24  LOAD_ATTR                line
               26  STORE_FAST               'linenum'

 L.  12        28  LOAD_STR                 '%s:%d: '
               30  LOAD_FAST                'filename'
               32  LOAD_FAST                'linenum'
               34  BUILD_TUPLE_2         2 
               36  BINARY_MODULO    
               38  STORE_FAST               'prefix'
               40  POP_BLOCK        
               42  JUMP_FORWARD         72  'to 72'
             44_0  COME_FROM_FINALLY     0  '0'

 L.  13        44  DUP_TOP          
               46  LOAD_GLOBAL              AttributeError
               48  LOAD_GLOBAL              TypeError
               50  LOAD_GLOBAL              IndexError
               52  BUILD_TUPLE_3         3 
               54  <121>                70  ''
               56  POP_TOP          
               58  POP_TOP          
               60  POP_TOP          

 L.  14        62  LOAD_STR                 ''
               64  STORE_FAST               'prefix'
               66  POP_EXCEPT       
               68  JUMP_FORWARD         72  'to 72'
               70  <48>             
             72_0  COME_FROM            68  '68'
             72_1  COME_FROM            42  '42'

 L.  15        72  LOAD_STR                 '%s%s'
               74  LOAD_FAST                'prefix'
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                args
               80  LOAD_CONST               0
               82  BINARY_SUBSCR    
               84  BUILD_TUPLE_2         2 
               86  BINARY_MODULO    
               88  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 54


class VerificationError(Exception):
    __doc__ = ' An error raised when verification fails\n    '
    __module__ = 'cffi'


class VerificationMissing(Exception):
    __doc__ = ' An error raised when incomplete structures are passed into\n    cdef, but no verification has been done\n    '
    __module__ = 'cffi'


class PkgConfigError(Exception):
    __doc__ = ' An error raised for missing modules in pkg-config\n    '
    __module__ = 'cffi'