# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: win32com\server\exception.py
"""Exception Handling

 Exceptions

         To better support COM exceptions, the framework allows for an instance to be
         raised.  This instance may have a certain number of known attributes, which are
         translated into COM exception details.
        
         This means, for example, that Python could raise a COM exception that includes details
         on a Help file and location, and a description for the user.
        
         This module provides a class which provides the necessary attributes.

"""
import sys, pythoncom

class COMException(pythoncom.com_error):
    __doc__ = 'An Exception object that is understood by the framework.\n\t\n\tIf the framework is presented with an exception of type class,\n\tit looks for certain known attributes on this class to provide rich\n\terror information to the caller.\n\n\tIt should be noted that the framework supports providing this error\n\tinformation via COM Exceptions, or via the ISupportErrorInfo interface.\n\n\tBy using this class, you automatically provide rich error information to the\n\tserver.\n\t'

    def __init__(self, description=None, scode=None, source=None, helpfile=None, helpContext=None, desc=None, hresult=None):
        """Initialize an exception
                **Params**

                description -- A string description for the exception.
                scode -- An integer scode to be returned to the server, if necessary.
                The pythoncom framework defaults this to be DISP_E_EXCEPTION if not specified otherwise.
                source -- A string which identifies the source of the error.
                helpfile -- A string which points to a help file which contains details on the error.
                helpContext -- An integer context in the help file.
                desc -- A short-cut for description.
                hresult -- A short-cut for scode.
                """
        scode = scode or hresult
        if scode:
            if scode != 1:
                if scode >= -32768:
                    if scode < 32768:
                        scode = -2147024896 | scode & 65535
        self.scode = scode
        self.description = description or desc
        if scode == 1 and not self.description:
            self.description = 'S_FALSE'
        elif scode:
            if not self.description:
                self.description = pythoncom.GetScodeString(scode)
        self.source = source
        self.helpfile = helpfile
        self.helpcontext = helpContext
        pythoncom.com_error.__init__(self, scode, self.description, None, -1)

    def __repr__(self):
        return '<COM Exception - scode=%s, desc=%s>' % (self.scode, self.description)


Exception = COMException

def IsCOMException(t=None):
    if t is None:
        t = sys.exc_info()[0]
    try:
        return issubclass(t, pythoncom.com_error)
    except TypeError:
        return t is pythoncon.com_error


def IsCOMServerException--- This code section failed: ---

 L.  86         0  LOAD_FAST                't'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    20  'to 20'

 L.  87         8  LOAD_GLOBAL              sys
               10  LOAD_METHOD              exc_info
               12  CALL_METHOD_0         0  ''
               14  LOAD_CONST               0
               16  BINARY_SUBSCR    
               18  STORE_FAST               't'
             20_0  COME_FROM             6  '6'

 L.  88        20  SETUP_FINALLY        34  'to 34'

 L.  89        22  LOAD_GLOBAL              issubclass
               24  LOAD_FAST                't'
               26  LOAD_GLOBAL              COMException
               28  CALL_FUNCTION_2       2  ''
               30  POP_BLOCK        
               32  RETURN_VALUE     
             34_0  COME_FROM_FINALLY    20  '20'

 L.  90        34  DUP_TOP          
               36  LOAD_GLOBAL              TypeError
               38  COMPARE_OP               exception-match
               40  POP_JUMP_IF_FALSE    54  'to 54'
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L.  91        48  POP_EXCEPT       
               50  LOAD_CONST               0
               52  RETURN_VALUE     
             54_0  COME_FROM            40  '40'
               54  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 50