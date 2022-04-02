# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\mechanize\_form.py
from __future__ import absolute_import
import re
from collections import defaultdict
from ._form_controls import HTMLForm, Label
from ._request import Request
from .polyglot import urljoin, is_string, as_unicode

class SkipControl(ValueError):
    pass


def normalize_line_endings(text):
    return re.sub(as_unicode('(?:(?<!\\r)\\n)|(?:\\r(?!\\n))'), '\r\n', text)


def label_text(elem):
    ans = []
    if elem.text:
        ans.append(elem.text)
    for child in elem:
        if child.tail:
            ans.append(child.tail)
    else:
        return ''.join(ans)


def parse_control(elem, parent_of, default_type='text'):
    attrs = dict(elem.attrib)
    label_elem = parent_of(elem, 'label')
    if label_elem is not None:
        lt = label_text(label_elem)
        if lt:
            attrs['__label'] = lt
    ctype = attrs.get('type') or default_type
    return (
     ctype, attrs.get('name'), attrs)


def parse_input(elem, parent_of, *a):
    return parse_control(elem, parent_of)


def parse_button(elem, parent_of, *a):
    ctype, name, attrs = parse_control(elem, parent_of, default_type='submit')
    ctype += 'button'
    return (
     ctype, name, attrs)


def parse_option(elem, parent_of, attrs_map):
    ctype, name, attrs = parse_control(elem, parent_of)
    og = parent_of(elem, 'optgroup')
    contents = (elem.text or '').strip()
    attrs['contents'] = contents
    attrs['value'] = attrs.get('value', contents)
    attrs['label'] = attrs.get('label', contents)
    if og is not None:
        if og.get('disabled') is not None:
            attrs['disabled'] = 'disabled'
    sel = parent_of(elem, 'select')
    if sel is None:
        raise SkipControl()
    attrs['__select'] = sel = attrs_map[sel]['__select']
    return (
     'select', sel.get('name'), attrs)


def parse_textarea(elem, parent_of, *a):
    ctype, name, attrs = parse_control(elem, parent_of)
    ctype = 'textarea'
    attrs['value'] = normalize_line_endings(elem.text or '')
    return (
     ctype, name, attrs)


def parse_select(elem, parent_of, *a):
    ctype, name, attrs = parse_control(elem, parent_of)
    ctype = 'select'
    return (
     ctype, name, {'__select': attrs})


def parse_forms--- This code section failed: ---

 L.  80         0  LOAD_FAST                'request_class'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L.  81         8  LOAD_GLOBAL              Request
               10  STORE_FAST               'request_class'
             12_0  COME_FROM             6  '6'

 L.  82        12  LOAD_GLOBAL              HTMLForm
               14  LOAD_FAST                'base_url'
               16  LOAD_FAST                'encoding'
               18  LOAD_CONST               ('encoding',)
               20  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               22  STORE_FAST               'global_form'

 L.  83        24  BUILD_LIST_0          0 
               26  BUILD_LIST_0          0 
               28  ROT_TWO          
               30  STORE_FAST               'forms'
               32  STORE_FAST               'labels'

 L.  84        34  BUILD_LIST_0          0 
               36  STORE_FAST               'form_elems'

 L.  85        38  BUILD_MAP_0           0 
               40  STORE_FAST               'form_id_map'

 L.  86        42  LOAD_GLOBAL              tuple
               44  LOAD_GENEXPR             '<code_object <genexpr>>'
               46  LOAD_STR                 'parse_forms.<locals>.<genexpr>'
               48  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.  87        50  LOAD_FAST                'root'
               52  LOAD_METHOD              iter
               54  LOAD_STR                 '*'
               56  CALL_METHOD_1         1  ''

 L.  86        58  GET_ITER         
               60  CALL_FUNCTION_1       1  ''
               62  CALL_FUNCTION_1       1  ''
               64  STORE_FAST               'all_elems'

 L.  88        66  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               68  LOAD_STR                 'parse_forms.<locals>.<dictcomp>'
               70  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               72  LOAD_FAST                'all_elems'
               74  GET_ITER         
               76  CALL_FUNCTION_1       1  ''
               78  STORE_DEREF              'parent_map'

 L.  89        80  LOAD_GLOBAL              defaultdict
               82  LOAD_GLOBAL              list
               84  CALL_FUNCTION_1       1  ''
               86  STORE_FAST               'id_to_labels'

 L.  90        88  LOAD_FAST                'all_elems'
               90  GET_ITER         
             92_0  COME_FROM           236  '236'
             92_1  COME_FROM           220  '220'
             92_2  COME_FROM           212  '212'
             92_3  COME_FROM           146  '146'
               92  FOR_ITER            238  'to 238'
               94  STORE_FAST               'e'

 L.  91        96  LOAD_FAST                'e'
               98  LOAD_ATTR                tag
              100  LOAD_METHOD              lower
              102  CALL_METHOD_0         0  ''
              104  STORE_FAST               'q'

 L.  92       106  LOAD_FAST                'q'
              108  LOAD_STR                 'form'
              110  COMPARE_OP               ==
              112  POP_JUMP_IF_FALSE   148  'to 148'

 L.  93       114  LOAD_FAST                'form_elems'
              116  LOAD_METHOD              append
              118  LOAD_FAST                'e'
              120  CALL_METHOD_1         1  ''
              122  POP_TOP          

 L.  94       124  LOAD_FAST                'e'
              126  LOAD_METHOD              get
              128  LOAD_STR                 'id'
              130  CALL_METHOD_1         1  ''
              132  STORE_FAST               'fid'

 L.  95       134  LOAD_FAST                'fid'
              136  POP_JUMP_IF_FALSE   236  'to 236'

 L.  96       138  LOAD_FAST                'e'
              140  LOAD_FAST                'form_id_map'
              142  LOAD_FAST                'fid'
              144  STORE_SUBSCR     
              146  JUMP_BACK            92  'to 92'
            148_0  COME_FROM           112  '112'

 L.  97       148  LOAD_FAST                'q'
              150  LOAD_STR                 'label'
              152  COMPARE_OP               ==
              154  POP_JUMP_IF_FALSE   214  'to 214'

 L.  98       156  LOAD_FAST                'e'
              158  LOAD_METHOD              get
              160  LOAD_STR                 'for'
              162  CALL_METHOD_1         1  ''
              164  STORE_FAST               'for_id'

 L.  99       166  LOAD_FAST                'for_id'
              168  LOAD_CONST               None
              170  COMPARE_OP               is-not
              172  POP_JUMP_IF_FALSE   236  'to 236'

 L. 100       174  LOAD_GLOBAL              Label
              176  LOAD_GLOBAL              label_text
              178  LOAD_FAST                'e'
              180  CALL_FUNCTION_1       1  ''
              182  LOAD_FAST                'for_id'
              184  CALL_FUNCTION_2       2  ''
              186  STORE_FAST               'label'

 L. 101       188  LOAD_FAST                'labels'
              190  LOAD_METHOD              append
              192  LOAD_FAST                'label'
              194  CALL_METHOD_1         1  ''
              196  POP_TOP          

 L. 102       198  LOAD_FAST                'id_to_labels'
              200  LOAD_FAST                'for_id'
              202  BINARY_SUBSCR    
              204  LOAD_METHOD              append
              206  LOAD_FAST                'label'
              208  CALL_METHOD_1         1  ''
              210  POP_TOP          
              212  JUMP_BACK            92  'to 92'
            214_0  COME_FROM           154  '154'

 L. 103       214  LOAD_FAST                'q'
              216  LOAD_STR                 'base'
              218  COMPARE_OP               ==
              220  POP_JUMP_IF_FALSE_BACK    92  'to 92'

 L. 104       222  LOAD_FAST                'e'
              224  LOAD_METHOD              get
              226  LOAD_STR                 'href'
              228  CALL_METHOD_1         1  ''
              230  JUMP_IF_TRUE_OR_POP   234  'to 234'
              232  LOAD_FAST                'base_url'
            234_0  COME_FROM           230  '230'
              234  STORE_FAST               'base_url'
            236_0  COME_FROM           172  '172'
            236_1  COME_FROM           136  '136'
              236  JUMP_BACK            92  'to 92'
            238_0  COME_FROM            92  '92'

 L. 106       238  LOAD_CLOSURE             'parent_map'
              240  BUILD_TUPLE_1         1 
              242  LOAD_CODE                <code_object parent_of>
              244  LOAD_STR                 'parse_forms.<locals>.parent_of'
              246  MAKE_FUNCTION_8          'closure'
              248  STORE_FAST               'parent_of'

 L. 115       250  BUILD_MAP_0           0 
              252  STORE_FAST               'forms_map'

 L. 116       254  LOAD_FAST                'form_elems'
              256  GET_ITER         
            258_0  COME_FROM           396  '396'
              258  FOR_ITER            400  'to 400'
              260  STORE_FAST               'form_elem'

 L. 117       262  LOAD_FAST                'form_elem'
              264  LOAD_METHOD              get
              266  LOAD_STR                 'name'
              268  CALL_METHOD_1         1  ''
          270_272  JUMP_IF_TRUE_OR_POP   276  'to 276'
              274  LOAD_CONST               None
            276_0  COME_FROM           270  '270'
              276  STORE_FAST               'name'

 L. 118       278  LOAD_FAST                'form_elem'
              280  LOAD_METHOD              get
              282  LOAD_STR                 'action'
              284  CALL_METHOD_1         1  ''
          286_288  JUMP_IF_TRUE_OR_POP   292  'to 292'
              290  LOAD_CONST               None
            292_0  COME_FROM           286  '286'
              292  STORE_FAST               'action'

 L. 119       294  LOAD_FAST                'form_elem'
              296  LOAD_METHOD              get
              298  LOAD_STR                 'method'
              300  CALL_METHOD_1         1  ''
          302_304  JUMP_IF_TRUE_OR_POP   308  'to 308'
              306  LOAD_STR                 'GET'
            308_0  COME_FROM           302  '302'
              308  STORE_FAST               'method'

 L. 120       310  LOAD_FAST                'form_elem'
              312  LOAD_METHOD              get

 L. 121       314  LOAD_STR                 'enctype'

 L. 120       316  CALL_METHOD_1         1  ''
          318_320  JUMP_IF_TRUE_OR_POP   324  'to 324'

 L. 121       322  LOAD_STR                 'application/x-www-form-urlencoded'
            324_0  COME_FROM           318  '318'

 L. 120       324  STORE_FAST               'enctype'

 L. 122       326  LOAD_FAST                'action'
          328_330  POP_JUMP_IF_FALSE   344  'to 344'

 L. 123       332  LOAD_GLOBAL              urljoin
              334  LOAD_FAST                'base_url'
              336  LOAD_FAST                'action'
              338  CALL_FUNCTION_2       2  ''
              340  STORE_FAST               'action'
              342  JUMP_FORWARD        348  'to 348'
            344_0  COME_FROM           328  '328'

 L. 125       344  LOAD_FAST                'base_url'
              346  STORE_FAST               'action'
            348_0  COME_FROM           342  '342'

 L. 126       348  LOAD_GLOBAL              HTMLForm
              350  LOAD_FAST                'action'
              352  LOAD_FAST                'method'
              354  LOAD_FAST                'enctype'
              356  LOAD_FAST                'name'
              358  LOAD_FAST                'form_elem'
              360  LOAD_ATTR                attrib

 L. 127       362  LOAD_FAST                'request_class'

 L. 127       364  LOAD_FAST                'forms'

 L. 127       366  LOAD_FAST                'labels'

 L. 127       368  LOAD_FAST                'id_to_labels'

 L. 127       370  LOAD_FAST                'encoding'

 L. 126       372  LOAD_CONST               ('encoding',)
              374  CALL_FUNCTION_KW_10    10  '10 total positional and keyword args'
              376  STORE_FAST               'form'

 L. 128       378  LOAD_FAST                'form'
              380  LOAD_FAST                'forms_map'
              382  LOAD_FAST                'form_elem'
              384  STORE_SUBSCR     

 L. 129       386  LOAD_FAST                'forms'
              388  LOAD_METHOD              append
              390  LOAD_FAST                'form'
              392  CALL_METHOD_1         1  ''
              394  POP_TOP          
          396_398  JUMP_BACK           258  'to 258'
            400_0  COME_FROM           258  '258'

 L. 131       400  BUILD_MAP_0           0 
              402  STORE_FAST               'attrs_map'

 L. 133       404  LOAD_GLOBAL              parse_option

 L. 134       406  LOAD_GLOBAL              parse_button

 L. 135       408  LOAD_GLOBAL              parse_input

 L. 136       410  LOAD_GLOBAL              parse_textarea

 L. 137       412  LOAD_GLOBAL              parse_select

 L. 132       414  LOAD_CONST               ('option', 'button', 'input', 'textarea', 'select')
              416  BUILD_CONST_KEY_MAP_5     5 
              418  STORE_FAST               'control_names'

 L. 140       420  LOAD_GLOBAL              enumerate
              422  LOAD_FAST                'all_elems'
              424  CALL_FUNCTION_1       1  ''
              426  GET_ITER         
            428_0  COME_FROM           608  '608'
            428_1  COME_FROM           566  '566'
            428_2  COME_FROM           462  '462'
              428  FOR_ITER            612  'to 612'
              430  UNPACK_SEQUENCE_2     2 
              432  STORE_FAST               'i'
              434  STORE_FAST               'elem'

 L. 141       436  LOAD_FAST                'elem'
              438  LOAD_ATTR                tag
              440  LOAD_METHOD              lower
              442  CALL_METHOD_0         0  ''
              444  STORE_FAST               'q'

 L. 142       446  LOAD_FAST                'control_names'
              448  LOAD_METHOD              get
              450  LOAD_FAST                'q'
              452  CALL_METHOD_1         1  ''
              454  STORE_FAST               'cfunc'

 L. 143       456  LOAD_FAST                'cfunc'
              458  LOAD_CONST               None
              460  COMPARE_OP               is-not
          462_464  POP_JUMP_IF_FALSE_BACK   428  'to 428'

 L. 144       466  LOAD_FAST                'elem'
              468  LOAD_METHOD              get
              470  LOAD_STR                 'form'
              472  CALL_METHOD_1         1  ''
              474  STORE_FAST               'fid'

 L. 145       476  LOAD_FAST                'fid'
          478_480  POP_JUMP_IF_FALSE   502  'to 502'
              482  LOAD_FAST                'fid'
              484  LOAD_FAST                'form_id_map'
              486  COMPARE_OP               in
          488_490  POP_JUMP_IF_FALSE   502  'to 502'

 L. 146       492  LOAD_FAST                'form_id_map'
              494  LOAD_FAST                'fid'
              496  BINARY_SUBSCR    
              498  STORE_FAST               'form_elem'
              500  JUMP_FORWARD        512  'to 512'
            502_0  COME_FROM           488  '488'
            502_1  COME_FROM           478  '478'

 L. 148       502  LOAD_FAST                'parent_of'
              504  LOAD_FAST                'elem'
              506  LOAD_STR                 'form'
              508  CALL_FUNCTION_2       2  ''
              510  STORE_FAST               'form_elem'
            512_0  COME_FROM           500  '500'

 L. 149       512  LOAD_FAST                'forms_map'
              514  LOAD_METHOD              get
              516  LOAD_FAST                'form_elem'
              518  LOAD_FAST                'global_form'
              520  CALL_METHOD_2         2  ''
              522  STORE_FAST               'form'

 L. 150       524  SETUP_FINALLY       548  'to 548'

 L. 151       526  LOAD_FAST                'cfunc'
              528  LOAD_FAST                'elem'
              530  LOAD_FAST                'parent_of'

 L. 152       532  LOAD_FAST                'attrs_map'

 L. 151       534  CALL_FUNCTION_3       3  ''
              536  UNPACK_SEQUENCE_3     3 
              538  STORE_FAST               'control_type'
              540  STORE_FAST               'control_name'
              542  STORE_FAST               'attrs'
              544  POP_BLOCK        
              546  JUMP_FORWARD        576  'to 576'
            548_0  COME_FROM_FINALLY   524  '524'

 L. 153       548  DUP_TOP          
              550  LOAD_GLOBAL              SkipControl
              552  COMPARE_OP               exception-match
          554_556  POP_JUMP_IF_FALSE   574  'to 574'
              558  POP_TOP          
              560  POP_TOP          
              562  POP_TOP          

 L. 154       564  POP_EXCEPT       
          566_568  JUMP_BACK           428  'to 428'
              570  POP_EXCEPT       
              572  JUMP_FORWARD        576  'to 576'
            574_0  COME_FROM           554  '554'
              574  END_FINALLY      
            576_0  COME_FROM           572  '572'
            576_1  COME_FROM           546  '546'

 L. 155       576  LOAD_FAST                'attrs'
              578  LOAD_FAST                'attrs_map'
              580  LOAD_FAST                'elem'
              582  STORE_SUBSCR     

 L. 156       584  LOAD_FAST                'form'
              586  LOAD_ATTR                new_control

 L. 157       588  LOAD_FAST                'control_type'

 L. 158       590  LOAD_FAST                'control_name'

 L. 159       592  LOAD_FAST                'attrs'

 L. 160       594  LOAD_FAST                'i'
              596  LOAD_CONST               10
              598  BINARY_MULTIPLY  

 L. 161       600  LOAD_FAST                'select_default'

 L. 156       602  LOAD_CONST               ('index', 'select_default')
              604  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              606  POP_TOP          
          608_610  JUMP_BACK           428  'to 428'
            612_0  COME_FROM           428  '428'

 L. 163       612  LOAD_FAST                'forms'
              614  GET_ITER         
            616_0  COME_FROM           628  '628'
              616  FOR_ITER            632  'to 632'
              618  STORE_FAST               'form'

 L. 164       620  LOAD_FAST                'form'
              622  LOAD_METHOD              fixup
              624  CALL_METHOD_0         0  ''
              626  POP_TOP          
          628_630  JUMP_BACK           616  'to 616'
            632_0  COME_FROM           616  '616'

 L. 165       632  LOAD_FAST                'global_form'
              634  LOAD_METHOD              fixup
              636  CALL_METHOD_0         0  ''
              638  POP_TOP          

 L. 167       640  LOAD_FAST                'forms'
              642  LOAD_FAST                'global_form'
              644  BUILD_TUPLE_2         2 
              646  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 574_0