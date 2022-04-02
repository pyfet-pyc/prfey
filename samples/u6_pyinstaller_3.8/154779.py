# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\openpyxl\xml\__init__.py
"""Collection of XML resources compatible across different Python versions"""
import os

def lxml_available--- This code section failed: ---

 L.   9         0  SETUP_FINALLY        60  'to 60'

 L.  10         2  LOAD_CONST               0
                4  LOAD_CONST               ('LXML_VERSION',)
                6  IMPORT_NAME_ATTR         lxml.etree
                8  IMPORT_FROM              LXML_VERSION
               10  STORE_FAST               'LXML_VERSION'
               12  POP_TOP          

 L.  11        14  LOAD_FAST                'LXML_VERSION'
               16  LOAD_CONST               (3, 3, 1, 0)
               18  COMPARE_OP               >=
               20  STORE_FAST               'LXML'

 L.  12        22  LOAD_FAST                'LXML'
               24  POP_JUMP_IF_TRUE     50  'to 50'

 L.  13        26  LOAD_CONST               0
               28  LOAD_CONST               None
               30  IMPORT_NAME              warnings
               32  STORE_FAST               'warnings'

 L.  14        34  LOAD_FAST                'warnings'
               36  LOAD_METHOD              warn
               38  LOAD_STR                 'The installed version of lxml is too old to be used with openpyxl'
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          

 L.  15        44  POP_BLOCK        
               46  LOAD_CONST               False
               48  RETURN_VALUE     
             50_0  COME_FROM            24  '24'

 L.  17        50  POP_BLOCK        
               52  LOAD_CONST               True
               54  RETURN_VALUE     
               56  POP_BLOCK        
               58  JUMP_FORWARD         82  'to 82'
             60_0  COME_FROM_FINALLY     0  '0'

 L.  18        60  DUP_TOP          
               62  LOAD_GLOBAL              ImportError
               64  COMPARE_OP               exception-match
               66  POP_JUMP_IF_FALSE    80  'to 80'
               68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          

 L.  19        74  POP_EXCEPT       
               76  LOAD_CONST               False
               78  RETURN_VALUE     
             80_0  COME_FROM            66  '66'
               80  END_FINALLY      
             82_0  COME_FROM            58  '58'

Parse error at or near `LOAD_CONST' instruction at offset 46


def lxml_env_set():
    return os.environ.get('OPENPYXL_LXML', 'True') == 'True'


LXML = lxml_available() and lxml_env_set()

def defusedxml_available():
    try:
        import defusedxml
    except ImportError:
        return False
    else:
        return True


def defusedxml_env_set():
    return os.environ.get('OPENPYXL_DEFUSEDXML', 'True') == 'True'


DEFUSEDXML = defusedxml_available() and defusedxml_env_set()