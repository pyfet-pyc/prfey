# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pyreadline\clipboard\__init__.py
from __future__ import print_function, unicode_literals, absolute_import
import sys
success = True
in_ironpython = 'IronPython' in sys.version
if in_ironpython:
    try:
        from .ironpython_clipboard import GetClipboardText, SetClipboardText
    except ImportError:
        from .no_clipboard import GetClipboardText, SetClipboardText

else:
    try:
        from .win32_clipboard import GetClipboardText, SetClipboardText
    except ImportError:
        from .no_clipboard import GetClipboardText, SetClipboardText
    else:

        def send_data(lists):
            SetClipboardText(make_tab(lists))


        def set_clipboard_text(toclipboard):
            SetClipboardText(str(toclipboard))


        def make_tab(lists):
            if hasattr(lists, 'tolist'):
                lists = lists.tolist()
            ut = []
            for rad in lists:
                if type(rad) in (list, tuple):
                    ut.append('\t'.join(['%s' % x for x in rad]))
                else:
                    ut.append('%s' % rad)
            else:
                return '\n'.join(ut)


        def make_list_of_list(txt):

            def make_num--- This code section failed: ---

 L.  38         0  SETUP_FINALLY        12  'to 12'

 L.  39         2  LOAD_GLOBAL              int
                4  LOAD_FAST                'x'
                6  CALL_FUNCTION_1       1  ''
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L.  40        12  DUP_TOP          
               14  LOAD_GLOBAL              ValueError
               16  COMPARE_OP               exception-match
               18  POP_JUMP_IF_FALSE   118  'to 118'
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L.  41        26  SETUP_FINALLY        42  'to 42'

 L.  42        28  LOAD_GLOBAL              float
               30  LOAD_FAST                'x'
               32  CALL_FUNCTION_1       1  ''
               34  POP_BLOCK        
               36  ROT_FOUR         
               38  POP_EXCEPT       
               40  RETURN_VALUE     
             42_0  COME_FROM_FINALLY    26  '26'

 L.  43        42  DUP_TOP          
               44  LOAD_GLOBAL              ValueError
               46  COMPARE_OP               exception-match
               48  POP_JUMP_IF_FALSE   112  'to 112'
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L.  44        56  SETUP_FINALLY        76  'to 76'

 L.  45        58  LOAD_GLOBAL              complex
               60  LOAD_FAST                'x'
               62  CALL_FUNCTION_1       1  ''
               64  POP_BLOCK        
               66  ROT_FOUR         
               68  POP_EXCEPT       
               70  ROT_FOUR         
               72  POP_EXCEPT       
               74  RETURN_VALUE     
             76_0  COME_FROM_FINALLY    56  '56'

 L.  46        76  DUP_TOP          
               78  LOAD_GLOBAL              ValueError
               80  COMPARE_OP               exception-match
               82  POP_JUMP_IF_FALSE   106  'to 106'
               84  POP_TOP          
               86  POP_TOP          
               88  POP_TOP          

 L.  47        90  LOAD_FAST                'x'
               92  ROT_FOUR         
               94  POP_EXCEPT       
               96  ROT_FOUR         
               98  POP_EXCEPT       
              100  ROT_FOUR         
              102  POP_EXCEPT       
              104  RETURN_VALUE     
            106_0  COME_FROM            82  '82'
              106  END_FINALLY      
              108  POP_EXCEPT       
              110  JUMP_FORWARD        114  'to 114'
            112_0  COME_FROM            48  '48'
              112  END_FINALLY      
            114_0  COME_FROM           110  '110'
              114  POP_EXCEPT       
              116  JUMP_FORWARD        120  'to 120'
            118_0  COME_FROM            18  '18'
              118  END_FINALLY      
            120_0  COME_FROM           116  '116'

 L.  48       120  LOAD_FAST                'x'
              122  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 22

            ut = []
            flag = False
            for rad in [x for x in txt.split('\r\n') if x != '']:
                raden = [make_num(x) for x in rad.split('\t')]
                if str in list(map(type, raden)):
                    flag = True
                ut.append(raden)
            else:
                return (
                 ut, flag)


        def get_clipboard_text_and_convert(paste_list=False):
            """Get txt from clipboard. if paste_list==True the convert tab separated 
    data to list of lists. Enclose list of list in array() if all elements are 
    numeric"""
            txt = GetClipboardText()
            if txt:
                if paste_list:
                    if '\t' in txt:
                        array, flag = make_list_of_list(txt)
                        if flag:
                            txt = repr(array)
                        else:
                            txt = 'array(%s)' % repr(array)
                        txt = ''.join([c for c in txt if c not in ' \t\r\n'])
            return txt