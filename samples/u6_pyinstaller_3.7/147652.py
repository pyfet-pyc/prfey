# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: numpy\f2py\common_rules.py
"""

Build common block mechanism for f2py2e.

Copyright 2000 Pearu Peterson all rights reserved,
Pearu Peterson <pearu@ioc.ee>
Permission to use, modify, and distribute this software is given under the
terms of the NumPy License

NO WARRANTY IS EXPRESSED OR IMPLIED.  USE AT YOUR OWN RISK.
$Date: 2005/05/06 10:57:33 $
Pearu Peterson

"""
from . import __version__
f2py_version = __version__.version
from .auxfuncs import hasbody, hascommon, hasnote, isintent_hide, outmess
from . import capi_maps
from . import func2subr
from .crackfortran import rmbadname

def findcommonblocks--- This code section failed: ---

 L.  28         0  BUILD_LIST_0          0 
                2  STORE_FAST               'ret'

 L.  29         4  LOAD_GLOBAL              hascommon
                6  LOAD_DEREF               'block'
                8  CALL_FUNCTION_1       1  '1 positional argument'
               10  POP_JUMP_IF_FALSE    74  'to 74'

 L.  30        12  SETUP_LOOP          114  'to 114'
               14  LOAD_DEREF               'block'
               16  LOAD_STR                 'common'
               18  BINARY_SUBSCR    
               20  LOAD_METHOD              items
               22  CALL_METHOD_0         0  '0 positional arguments'
               24  GET_ITER         
               26  FOR_ITER             70  'to 70'
               28  UNPACK_SEQUENCE_2     2 
               30  STORE_FAST               'key'
               32  STORE_FAST               'value'

 L.  31        34  LOAD_CLOSURE             'block'
               36  BUILD_TUPLE_1         1 
               38  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               40  LOAD_STR                 'findcommonblocks.<locals>.<dictcomp>'
               42  MAKE_FUNCTION_8          'closure'
               44  LOAD_FAST                'value'
               46  GET_ITER         
               48  CALL_FUNCTION_1       1  '1 positional argument'
               50  STORE_FAST               'vars_'

 L.  32        52  LOAD_FAST                'ret'
               54  LOAD_METHOD              append
               56  LOAD_FAST                'key'
               58  LOAD_FAST                'value'
               60  LOAD_FAST                'vars_'
               62  BUILD_TUPLE_3         3 
               64  CALL_METHOD_1         1  '1 positional argument'
               66  POP_TOP          
               68  JUMP_BACK            26  'to 26'
               70  POP_BLOCK        
               72  JUMP_FORWARD        114  'to 114'
             74_0  COME_FROM            10  '10'

 L.  33        74  LOAD_GLOBAL              hasbody
               76  LOAD_DEREF               'block'
               78  CALL_FUNCTION_1       1  '1 positional argument'
               80  POP_JUMP_IF_FALSE   114  'to 114'

 L.  34        82  SETUP_LOOP          114  'to 114'
               84  LOAD_DEREF               'block'
               86  LOAD_STR                 'body'
               88  BINARY_SUBSCR    
               90  GET_ITER         
               92  FOR_ITER            112  'to 112'
               94  STORE_FAST               'b'

 L.  35        96  LOAD_FAST                'ret'
               98  LOAD_GLOBAL              findcommonblocks
              100  LOAD_FAST                'b'
              102  LOAD_CONST               0
              104  CALL_FUNCTION_2       2  '2 positional arguments'
              106  BINARY_ADD       
              108  STORE_FAST               'ret'
              110  JUMP_BACK            92  'to 92'
              112  POP_BLOCK        
            114_0  COME_FROM_LOOP       82  '82'
            114_1  COME_FROM            80  '80'
            114_2  COME_FROM            72  '72'
            114_3  COME_FROM_LOOP       12  '12'

 L.  36       114  LOAD_FAST                'top'
              116  POP_JUMP_IF_FALSE   180  'to 180'

 L.  37       118  BUILD_LIST_0          0 
              120  STORE_FAST               'tret'

 L.  38       122  BUILD_LIST_0          0 
              124  STORE_FAST               'names'

 L.  39       126  SETUP_LOOP          176  'to 176'
              128  LOAD_FAST                'ret'
              130  GET_ITER         
            132_0  COME_FROM           146  '146'
              132  FOR_ITER            174  'to 174'
              134  STORE_FAST               't'

 L.  40       136  LOAD_FAST                't'
              138  LOAD_CONST               0
              140  BINARY_SUBSCR    
              142  LOAD_FAST                'names'
              144  COMPARE_OP               not-in
              146  POP_JUMP_IF_FALSE   132  'to 132'

 L.  41       148  LOAD_FAST                'names'
              150  LOAD_METHOD              append
              152  LOAD_FAST                't'
              154  LOAD_CONST               0
              156  BINARY_SUBSCR    
              158  CALL_METHOD_1         1  '1 positional argument'
              160  POP_TOP          

 L.  42       162  LOAD_FAST                'tret'
              164  LOAD_METHOD              append
              166  LOAD_FAST                't'
              168  CALL_METHOD_1         1  '1 positional argument'
              170  POP_TOP          
              172  JUMP_BACK           132  'to 132'
              174  POP_BLOCK        
            176_0  COME_FROM_LOOP      126  '126'

 L.  43       176  LOAD_FAST                'tret'
              178  RETURN_VALUE     
            180_0  COME_FROM           116  '116'

 L.  44       180  LOAD_FAST                'ret'
              182  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 114_3


def buildhooks(m):
    ret = {'commonhooks':[],  'initcommonhooks':[],  'docs':[
      '"COMMON blocks:\\n"']}
    fwrap = ['']

    def fadd(line, s=fwrap):
        s[0] = '%s\n      %s' % (s[0], line)

    chooks = ['']

    def cadd(line, s=chooks):
        s[0] = '%s\n%s' % (s[0], line)

    ihooks = ['']

    def iadd(line, s=ihooks):
        s[0] = '%s\n%s' % (s[0], line)

    doc = ['']

    def dadd(line, s=doc):
        s[0] = '%s\n%s' % (s[0], line)

    for name, vnames, vars in findcommonblocks(m):
        lower_name = name.lower
        hnames, inames = [], []
        for n in vnames:
            if isintent_hide(vars[n]):
                hnames.appendn
            else:
                inames.appendn

        if hnames:
            outmess('\t\tConstructing COMMON block support for "%s"...\n\t\t  %s\n\t\t  Hidden: %s\n' % (
             name, ','.joininames, ','.joinhnames))
        else:
            outmess('\t\tConstructing COMMON block support for "%s"...\n\t\t  %s\n' % (
             name, ','.joininames))
        fadd('subroutine f2pyinit%s(setupfunc)' % name)
        fadd('external setupfunc')
        for n in vnames:
            fadd(func2subr.var2fixfortran(vars, n))

        if name == '_BLNK_':
            fadd('common %s' % ','.joinvnames)
        else:
            fadd('common /%s/ %s' % (name, ','.joinvnames))
        fadd('call setupfunc(%s)' % ','.joininames)
        fadd('end\n')
        cadd('static FortranDataDef f2py_%s_def[] = {' % name)
        idims = []
        for n in inames:
            ct = capi_maps.getctypevars[n]
            at = capi_maps.c2capi_map[ct]
            dm = capi_maps.getarrdims(n, vars[n])
            if dm['dims']:
                idims.append('(%s)' % dm['dims'])
            else:
                idims.append''
            dms = dm['dims'].strip
            if not dms:
                dms = '-1'
            cadd('\t{"%s",%s,{{%s}},%s},' % (n, dm['rank'], dms, at))

        cadd('\t{NULL}\n};')
        inames1 = rmbadname(inames)
        inames1_tps = ','.join['char *' + s for s in inames1]
        cadd('static void f2py_setup_%s(%s) {' % (name, inames1_tps))
        cadd('\tint i_f2py=0;')
        for n in inames1:
            cadd('\tf2py_%s_def[i_f2py++].data = %s;' % (name, n))

        cadd('}')
        if '_' in lower_name:
            F_FUNC = 'F_FUNC_US'
        else:
            F_FUNC = 'F_FUNC'
        cadd('extern void %s(f2pyinit%s,F2PYINIT%s)(void(*)(%s));' % (
         F_FUNC, lower_name, name.upper,
         ','.join(['char*'] * len(inames1))))
        cadd('static void f2py_init_%s(void) {' % name)
        cadd('\t%s(f2pyinit%s,F2PYINIT%s)(f2py_setup_%s);' % (
         F_FUNC, lower_name, name.upper, name))
        cadd('}\n')
        iadd('\ttmp = PyFortranObject_New(f2py_%s_def,f2py_init_%s);' % (name, name))
        iadd('\tF2PyDict_SetItemString(d, "%s", tmp);' % name)
        iadd('\tPy_DECREF(tmp);')
        tname = name.replace('_', '\\_')
        dadd('\\subsection{Common block \\texttt{%s}}\n' % tname)
        dadd('\\begin{description}')
        for n in inames:
            dadd('\\item[]{{}\\verb@%s@{}}' % capi_maps.getarrdocsign(n, vars[n]))
            if hasnote(vars[n]):
                note = vars[n]['note']
                if isinstancenotelist:
                    note = '\n'.joinnote
                dadd('--- %s' % note)

        dadd('\\end{description}')
        ret['docs'].append('"\t/%s/ %s\\n"' % (name, ','.joinmap(lambda v, d: v + d, inames, idims)))

    ret['commonhooks'] = chooks
    ret['initcommonhooks'] = ihooks
    ret['latexdoc'] = doc[0]
    if len(ret['docs']) <= 1:
        ret['docs'] = ''
    return (
     ret, fwrap[0])