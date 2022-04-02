# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\numpy\f2py\common_rules.py
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
                8  CALL_FUNCTION_1       1  ''
               10  POP_JUMP_IF_FALSE    70  'to 70'

 L.  30        12  LOAD_DEREF               'block'
               14  LOAD_STR                 'common'
               16  BINARY_SUBSCR    
               18  LOAD_METHOD              items
               20  CALL_METHOD_0         0  ''
               22  GET_ITER         
               24  FOR_ITER             68  'to 68'
               26  UNPACK_SEQUENCE_2     2 
               28  STORE_FAST               'key'
               30  STORE_FAST               'value'

 L.  31        32  LOAD_CLOSURE             'block'
               34  BUILD_TUPLE_1         1 
               36  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               38  LOAD_STR                 'findcommonblocks.<locals>.<dictcomp>'
               40  MAKE_FUNCTION_8          'closure'
               42  LOAD_FAST                'value'
               44  GET_ITER         
               46  CALL_FUNCTION_1       1  ''
               48  STORE_FAST               'vars_'

 L.  32        50  LOAD_FAST                'ret'
               52  LOAD_METHOD              append
               54  LOAD_FAST                'key'
               56  LOAD_FAST                'value'
               58  LOAD_FAST                'vars_'
               60  BUILD_TUPLE_3         3 
               62  CALL_METHOD_1         1  ''
               64  POP_TOP          
               66  JUMP_BACK            24  'to 24'
               68  JUMP_FORWARD        106  'to 106'
             70_0  COME_FROM            10  '10'

 L.  33        70  LOAD_GLOBAL              hasbody
               72  LOAD_DEREF               'block'
               74  CALL_FUNCTION_1       1  ''
               76  POP_JUMP_IF_FALSE   106  'to 106'

 L.  34        78  LOAD_DEREF               'block'
               80  LOAD_STR                 'body'
               82  BINARY_SUBSCR    
               84  GET_ITER         
               86  FOR_ITER            106  'to 106'
               88  STORE_FAST               'b'

 L.  35        90  LOAD_FAST                'ret'
               92  LOAD_GLOBAL              findcommonblocks
               94  LOAD_FAST                'b'
               96  LOAD_CONST               0
               98  CALL_FUNCTION_2       2  ''
              100  BINARY_ADD       
              102  STORE_FAST               'ret'
              104  JUMP_BACK            86  'to 86'
            106_0  COME_FROM            76  '76'
            106_1  COME_FROM            68  '68'

 L.  36       106  LOAD_FAST                'top'
              108  POP_JUMP_IF_FALSE   168  'to 168'

 L.  37       110  BUILD_LIST_0          0 
              112  STORE_FAST               'tret'

 L.  38       114  BUILD_LIST_0          0 
              116  STORE_FAST               'names'

 L.  39       118  LOAD_FAST                'ret'
              120  GET_ITER         
            122_0  COME_FROM           136  '136'
              122  FOR_ITER            164  'to 164'
              124  STORE_FAST               't'

 L.  40       126  LOAD_FAST                't'
              128  LOAD_CONST               0
              130  BINARY_SUBSCR    
              132  LOAD_FAST                'names'
              134  COMPARE_OP               not-in
              136  POP_JUMP_IF_FALSE   122  'to 122'

 L.  41       138  LOAD_FAST                'names'
              140  LOAD_METHOD              append
              142  LOAD_FAST                't'
              144  LOAD_CONST               0
              146  BINARY_SUBSCR    
              148  CALL_METHOD_1         1  ''
              150  POP_TOP          

 L.  42       152  LOAD_FAST                'tret'
              154  LOAD_METHOD              append
              156  LOAD_FAST                't'
              158  CALL_METHOD_1         1  ''
              160  POP_TOP          
              162  JUMP_BACK           122  'to 122'

 L.  43       164  LOAD_FAST                'tret'
              166  RETURN_VALUE     
            168_0  COME_FROM           108  '108'

 L.  44       168  LOAD_FAST                'ret'
              170  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 36


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
    else:
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
        else:
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
            else:
                cadd('\t{NULL}\n};')
                inames1 = rmbadname(inames)
                inames1_tps = ','.join['char *' + s for s in inames1]
                cadd('static void f2py_setup_%s(%s) {' % (name, inames1_tps))
                cadd('\tint i_f2py=0;')
                for n in inames1:
                    cadd('\tf2py_%s_def[i_f2py++].data = %s;' % (name, n))
                else:
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
                    else:
                        ret['commonhooks'] = chooks
                        ret['initcommonhooks'] = ihooks
                        ret['latexdoc'] = doc[0]
                        if len(ret['docs']) <= 1:
                            ret['docs'] = ''
                        return (
                         ret, fwrap[0])