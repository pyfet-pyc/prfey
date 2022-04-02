# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\openpyxl\cell\_writer.py
from openpyxl.compat import safe_string
from openpyxl.xml.functions import Element, SubElement, whitespace, XML_NS, REL_NS
from openpyxl import LXML
from openpyxl.utils.datetime import to_excel, days_to_time
from datetime import timedelta

def _set_attributes(cell, styled=None):
    """
    Set coordinate and datatype
    """
    coordinate = cell.coordinate
    attrs = {'r': coordinate}
    if styled:
        attrs['s'] = f"{cell.style_id}"
    if cell.data_type == 's':
        attrs['t'] = 'inlineStr'
    elif cell.data_type != 'f':
        attrs['t'] = cell.data_type
    value = cell._value
    if cell.data_type == 'd':
        if cell.parent.parent.iso_dates:
            if isinstance(value, timedelta):
                value = days_to_time(value)
            value = value.isoformat()
        else:
            attrs['t'] = 'n'
            value = to_excel(value, cell.parent.parent.epoch)
    if cell.hyperlink:
        cell.parent._hyperlinks.append(cell.hyperlink)
    return (
     value, attrs)


def etree_write_cell(xf, worksheet, cell, styled=None):
    value, attributes = _set_attributes(cell, styled)
    el = Element('c', attributes)
    if value is None or (value == ''):
        xf.write(el)
        return
    if cell.data_type == 'f':
        shared_formula = worksheet.formula_attributes.get(cell.coordinate, {})
        formula = SubElement(el, 'f', shared_formula)
        if value is not None:
            formula.text = value[1:]
            value = None
    if cell.data_type == 's':
        inline_string = SubElement(el, 'is')
        text = SubElement(inline_string, 't')
        text.text = value
        whitespace(text)
    else:
        cell_content = SubElement(el, 'v')
        if value is not None:
            cell_content.text = safe_string(value)
    xf.write(el)


def lxml_write_cell--- This code section failed: ---

 L.  73         0  LOAD_GLOBAL              _set_attributes
                2  LOAD_FAST                'cell'
                4  LOAD_FAST                'styled'
                6  CALL_FUNCTION_2       2  ''
                8  UNPACK_SEQUENCE_2     2 
               10  STORE_FAST               'value'
               12  STORE_FAST               'attributes'

 L.  75        14  LOAD_FAST                'value'
               16  LOAD_STR                 ''
               18  COMPARE_OP               ==
               20  POP_JUMP_IF_TRUE     30  'to 30'
               22  LOAD_FAST                'value'
               24  LOAD_CONST               None
               26  COMPARE_OP               is
               28  POP_JUMP_IF_FALSE    64  'to 64'
             30_0  COME_FROM            20  '20'

 L.  76        30  LOAD_FAST                'xf'
               32  LOAD_METHOD              element
               34  LOAD_STR                 'c'
               36  LOAD_FAST                'attributes'
               38  CALL_METHOD_2         2  ''
               40  SETUP_WITH           58  'to 58'
               42  POP_TOP          

 L.  77        44  POP_BLOCK        
               46  BEGIN_FINALLY    
               48  WITH_CLEANUP_START
               50  WITH_CLEANUP_FINISH
               52  POP_FINALLY           0  ''
               54  LOAD_CONST               None
               56  RETURN_VALUE     
             58_0  COME_FROM_WITH       40  '40'
               58  WITH_CLEANUP_START
               60  WITH_CLEANUP_FINISH
               62  END_FINALLY      
             64_0  COME_FROM            28  '28'

 L.  79        64  LOAD_FAST                'xf'
               66  LOAD_METHOD              element
               68  LOAD_STR                 'c'
               70  LOAD_FAST                'attributes'
               72  CALL_METHOD_2         2  ''
               74  SETUP_WITH          296  'to 296'
               76  POP_TOP          

 L.  80        78  LOAD_FAST                'cell'
               80  LOAD_ATTR                data_type
               82  LOAD_STR                 'f'
               84  COMPARE_OP               ==
               86  POP_JUMP_IF_FALSE   158  'to 158'

 L.  81        88  LOAD_FAST                'worksheet'
               90  LOAD_ATTR                formula_attributes
               92  LOAD_METHOD              get
               94  LOAD_FAST                'cell'
               96  LOAD_ATTR                coordinate
               98  BUILD_MAP_0           0 
              100  CALL_METHOD_2         2  ''
              102  STORE_FAST               'shared_formula'

 L.  82       104  LOAD_FAST                'xf'
              106  LOAD_METHOD              element
              108  LOAD_STR                 'f'
              110  LOAD_FAST                'shared_formula'
              112  CALL_METHOD_2         2  ''
              114  SETUP_WITH          152  'to 152'
              116  POP_TOP          

 L.  83       118  LOAD_FAST                'value'
              120  LOAD_CONST               None
              122  COMPARE_OP               is-not
              124  POP_JUMP_IF_FALSE   148  'to 148'

 L.  84       126  LOAD_FAST                'xf'
              128  LOAD_METHOD              write
              130  LOAD_FAST                'value'
              132  LOAD_CONST               1
              134  LOAD_CONST               None
              136  BUILD_SLICE_2         2 
              138  BINARY_SUBSCR    
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          

 L.  85       144  LOAD_CONST               None
              146  STORE_FAST               'value'
            148_0  COME_FROM           124  '124'
              148  POP_BLOCK        
              150  BEGIN_FINALLY    
            152_0  COME_FROM_WITH      114  '114'
              152  WITH_CLEANUP_START
              154  WITH_CLEANUP_FINISH
              156  END_FINALLY      
            158_0  COME_FROM            86  '86'

 L.  87       158  LOAD_FAST                'cell'
              160  LOAD_ATTR                data_type
              162  LOAD_STR                 's'
              164  COMPARE_OP               ==
              166  POP_JUMP_IF_FALSE   246  'to 246'

 L.  88       168  LOAD_FAST                'xf'
              170  LOAD_METHOD              element
              172  LOAD_STR                 'is'
              174  CALL_METHOD_1         1  ''
              176  SETUP_WITH          238  'to 238'
              178  POP_TOP          

 L.  89       180  BUILD_MAP_0           0 
              182  STORE_FAST               'attrs'

 L.  90       184  LOAD_FAST                'value'
              186  LOAD_FAST                'value'
              188  LOAD_METHOD              strip
              190  CALL_METHOD_0         0  ''
              192  COMPARE_OP               !=
              194  POP_JUMP_IF_FALSE   208  'to 208'

 L.  91       196  LOAD_STR                 'preserve'
              198  LOAD_FAST                'attrs'
              200  LOAD_STR                 '{%s}space'
              202  LOAD_GLOBAL              XML_NS
              204  BINARY_MODULO    
              206  STORE_SUBSCR     
            208_0  COME_FROM           194  '194'

 L.  92       208  LOAD_GLOBAL              Element
              210  LOAD_STR                 't'
              212  LOAD_FAST                'attrs'
              214  CALL_FUNCTION_2       2  ''
              216  STORE_FAST               'el'

 L.  93       218  LOAD_FAST                'value'
              220  LOAD_FAST                'el'
              222  STORE_ATTR               text

 L.  94       224  LOAD_FAST                'xf'
              226  LOAD_METHOD              write
              228  LOAD_FAST                'el'
              230  CALL_METHOD_1         1  ''
              232  POP_TOP          
              234  POP_BLOCK        
              236  BEGIN_FINALLY    
            238_0  COME_FROM_WITH      176  '176'
              238  WITH_CLEANUP_START
              240  WITH_CLEANUP_FINISH
              242  END_FINALLY      
              244  JUMP_FORWARD        292  'to 292'
            246_0  COME_FROM           166  '166'

 L.  98       246  LOAD_FAST                'xf'
              248  LOAD_METHOD              element
              250  LOAD_STR                 'v'
              252  CALL_METHOD_1         1  ''
              254  SETUP_WITH          286  'to 286'
              256  POP_TOP          

 L.  99       258  LOAD_FAST                'value'
              260  LOAD_CONST               None
              262  COMPARE_OP               is-not
          264_266  POP_JUMP_IF_FALSE   282  'to 282'

 L. 100       268  LOAD_FAST                'xf'
              270  LOAD_METHOD              write
              272  LOAD_GLOBAL              safe_string
              274  LOAD_FAST                'value'
              276  CALL_FUNCTION_1       1  ''
              278  CALL_METHOD_1         1  ''
              280  POP_TOP          
            282_0  COME_FROM           264  '264'
              282  POP_BLOCK        
              284  BEGIN_FINALLY    
            286_0  COME_FROM_WITH      254  '254'
              286  WITH_CLEANUP_START
              288  WITH_CLEANUP_FINISH
              290  END_FINALLY      
            292_0  COME_FROM           244  '244'
              292  POP_BLOCK        
              294  BEGIN_FINALLY    
            296_0  COME_FROM_WITH       74  '74'
              296  WITH_CLEANUP_START
              298  WITH_CLEANUP_FINISH
              300  END_FINALLY      

Parse error at or near `WITH_CLEANUP_START' instruction at offset 48


if LXML:
    write_cell = lxml_write_cell
else:
    write_cell = etree_write_cell