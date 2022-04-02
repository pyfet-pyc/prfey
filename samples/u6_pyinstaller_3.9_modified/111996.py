# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: pywin\mfc\object.py
import sys, win32ui

class Object:

    def __init__--- This code section failed: ---

 L.   7         0  LOAD_FAST                'initObj'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                __dict__
                6  LOAD_STR                 '_obj_'
                8  STORE_SUBSCR     

 L.   9        10  LOAD_FAST                'initObj'
               12  LOAD_CONST               None
               14  <117>                 1  ''
               16  POP_JUMP_IF_FALSE    28  'to 28'
               18  LOAD_FAST                'initObj'
               20  LOAD_METHOD              AttachObject
               22  LOAD_FAST                'self'
               24  CALL_METHOD_1         1  ''
               26  POP_TOP          
             28_0  COME_FROM            16  '16'

Parse error at or near `<117>' instruction at offset 14

    def __del__(self):
        self.close()

    def __getattr__--- This code section failed: ---

 L.  14         0  LOAD_FAST                'attr'
                2  LOAD_METHOD              startswith
                4  LOAD_STR                 '__'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_TRUE     98  'to 98'

 L.  15        10  SETUP_FINALLY        80  'to 80'

 L.  16        12  LOAD_FAST                'self'
               14  LOAD_ATTR                __dict__
               16  LOAD_STR                 '_obj_'
               18  BINARY_SUBSCR    
               20  STORE_FAST               'o'

 L.  17        22  LOAD_FAST                'o'
               24  LOAD_CONST               None
               26  <117>                 1  ''
               28  POP_JUMP_IF_FALSE    42  'to 42'

 L.  18        30  LOAD_GLOBAL              getattr
               32  LOAD_FAST                'o'
               34  LOAD_FAST                'attr'
               36  CALL_FUNCTION_2       2  ''
               38  POP_BLOCK        
               40  RETURN_VALUE     
             42_0  COME_FROM            28  '28'

 L.  22        42  LOAD_FAST                'attr'
               44  LOAD_CONST               0
               46  BINARY_SUBSCR    
               48  LOAD_STR                 '_'
               50  COMPARE_OP               !=
               52  POP_JUMP_IF_FALSE    76  'to 76'
               54  LOAD_FAST                'attr'
               56  LOAD_CONST               -1
               58  BINARY_SUBSCR    
               60  LOAD_STR                 '_'
               62  COMPARE_OP               !=
               64  POP_JUMP_IF_FALSE    76  'to 76'

 L.  23        66  LOAD_GLOBAL              win32ui
               68  LOAD_METHOD              error
               70  LOAD_STR                 'The MFC object has died.'
               72  CALL_METHOD_1         1  ''
               74  RAISE_VARARGS_1       1  'exception instance'
             76_0  COME_FROM            64  '64'
             76_1  COME_FROM            52  '52'
               76  POP_BLOCK        
               78  JUMP_FORWARD         98  'to 98'
             80_0  COME_FROM_FINALLY    10  '10'

 L.  24        80  DUP_TOP          
               82  LOAD_GLOBAL              KeyError
               84  <121>                96  ''
               86  POP_TOP          
               88  POP_TOP          
               90  POP_TOP          

 L.  26        92  POP_EXCEPT       
               94  JUMP_FORWARD         98  'to 98'
               96  <48>             
             98_0  COME_FROM            94  '94'
             98_1  COME_FROM            78  '78'
             98_2  COME_FROM             8  '8'

 L.  27        98  LOAD_GLOBAL              AttributeError
              100  LOAD_FAST                'attr'
              102  CALL_FUNCTION_1       1  ''
              104  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `<117>' instruction at offset 26

    def OnAttachedObjectDeath(self):
        self._obj_ = None

    def close--- This code section failed: ---

 L.  33         0  LOAD_STR                 '_obj_'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                __dict__
                6  <118>                 0  ''
                8  POP_JUMP_IF_FALSE    38  'to 38'

 L.  34        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _obj_
               14  LOAD_CONST               None
               16  <117>                 1  ''
               18  POP_JUMP_IF_FALSE    38  'to 38'

 L.  35        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _obj_
               24  LOAD_METHOD              AttachObject
               26  LOAD_CONST               None
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L.  36        32  LOAD_CONST               None
               34  LOAD_FAST                'self'
               36  STORE_ATTR               _obj_
             38_0  COME_FROM            18  '18'
             38_1  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1


class CmdTarget(Object):

    def __init__(self, initObj):
        Object.__init__(self, initObj)

    def HookNotifyRange(self, handler, firstID, lastID):
        oldhandlers = []
        for i in range(firstID, lastID + 1):
            oldhandlers.appendself.HookNotify(handler, i)
        else:
            return oldhandlers

    def HookCommandRange(self, handler, firstID, lastID):
        oldhandlers = []
        for i in range(firstID, lastID + 1):
            oldhandlers.appendself.HookCommand(handler, i)
        else:
            return oldhandlers

    def HookCommandUpdateRange(self, handler, firstID, lastID):
        oldhandlers = []
        for i in range(firstID, lastID + 1):
            oldhandlers.appendself.HookCommandUpdate(handler, i)
        else:
            return oldhandlers