# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: certifi\core.py
"""
certifi.py
~~~~~~~~~~

This module returns the installation location of cacert.pem or its contents.
"""
import os
try:
    from importlib.resources import read_text
except ImportError:

    def read_text--- This code section failed: ---

 L.  19         0  LOAD_GLOBAL              open
                2  LOAD_GLOBAL              where
                4  CALL_FUNCTION_0       0  ''
                6  LOAD_STR                 'r'
                8  LOAD_FAST                'encoding'
               10  LOAD_CONST               ('encoding',)
               12  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               14  SETUP_WITH           38  'to 38'
               16  STORE_FAST               'data'

 L.  20        18  LOAD_FAST                'data'
               20  LOAD_METHOD              read
               22  CALL_METHOD_0         0  ''
               24  POP_BLOCK        
               26  ROT_TWO          
               28  BEGIN_FINALLY    
               30  WITH_CLEANUP_START
               32  WITH_CLEANUP_FINISH
               34  POP_FINALLY           0  ''
               36  RETURN_VALUE     
             38_0  COME_FROM_WITH       14  '14'
               38  WITH_CLEANUP_START
               40  WITH_CLEANUP_FINISH
               42  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 26


else:

    def where():
        f = os.path.dirname(__file__)
        return os.path.join(f, 'cacert.pem')


    def contents():
        return read_text('certifi', 'cacert.pem', encoding='ascii')