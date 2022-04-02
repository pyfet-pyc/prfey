# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\numpy\f2py\cb_rules.py
"""

Build call-back mechanism for f2py2e.

Copyright 2000 Pearu Peterson all rights reserved,
Pearu Peterson <pearu@ioc.ee>
Permission to use, modify, and distribute this software is given under the
terms of the NumPy License.

NO WARRANTY IS EXPRESSED OR IMPLIED.  USE AT YOUR OWN RISK.
$Date: 2005/07/20 11:27:58 $
Pearu Peterson

"""
from __future__ import division, absolute_import, print_function
from . import __version__
from .auxfuncs import applyrules, debugcapi, dictappend, errmess, getargs, hasnote, isarray, iscomplex, iscomplexarray, iscomplexfunction, isfunction, isintent_c, isintent_hide, isintent_in, isintent_inout, isintent_nothide, isintent_out, isoptional, isrequired, isscalar, isstring, isstringfunction, issubroutine, l_and, l_not, l_or, outmess, replace, stripcomma, throw_error
from . import cfuncs
f2py_version = __version__.version
cb_routine_rules = {'cbtypedefs':'typedef #rctype#(*#name#_typedef)(#optargs_td##args_td##strarglens_td##noargs#);', 
 'body':'\n#begintitle#\nPyObject *#name#_capi = NULL;/*was Py_None*/\nPyTupleObject *#name#_args_capi = NULL;\nint #name#_nofargs = 0;\njmp_buf #name#_jmpbuf;\n/*typedef #rctype#(*#name#_typedef)(#optargs_td##args_td##strarglens_td##noargs#);*/\n#static# #rctype# #callbackname# (#optargs##args##strarglens##noargs#) {\n\tPyTupleObject *capi_arglist = #name#_args_capi;\n\tPyObject *capi_return = NULL;\n\tPyObject *capi_tmp = NULL;\n\tPyObject *capi_arglist_list = NULL;\n\tint capi_j,capi_i = 0;\n\tint capi_longjmp_ok = 1;\n#decl#\n#ifdef F2PY_REPORT_ATEXIT\nf2py_cb_start_clock();\n#endif\n\tCFUNCSMESS("cb:Call-back function #name# (maxnofargs=#maxnofargs#(-#nofoptargs#))\\n");\n\tCFUNCSMESSPY("cb:#name#_capi=",#name#_capi);\n\tif (#name#_capi==NULL) {\n\t\tcapi_longjmp_ok = 0;\n\t\t#name#_capi = PyObject_GetAttrString(#modulename#_module,"#argname#");\n\t}\n\tif (#name#_capi==NULL) {\n\t\tPyErr_SetString(#modulename#_error,"cb: Callback #argname# not defined (as an argument or module #modulename# attribute).\\n");\n\t\tgoto capi_fail;\n\t}\n\tif (F2PyCapsule_Check(#name#_capi)) {\n\t#name#_typedef #name#_cptr;\n\t#name#_cptr = F2PyCapsule_AsVoidPtr(#name#_capi);\n\t#returncptr#(*#name#_cptr)(#optargs_nm##args_nm##strarglens_nm#);\n\t#return#\n\t}\n\tif (capi_arglist==NULL) {\n\t\tcapi_longjmp_ok = 0;\n\t\tcapi_tmp = PyObject_GetAttrString(#modulename#_module,"#argname#_extra_args");\n\t\tif (capi_tmp) {\n\t\t\tcapi_arglist = (PyTupleObject *)PySequence_Tuple(capi_tmp);\n\t\t\tif (capi_arglist==NULL) {\n\t\t\t\tPyErr_SetString(#modulename#_error,"Failed to convert #modulename#.#argname#_extra_args to tuple.\\n");\n\t\t\t\tgoto capi_fail;\n\t\t\t}\n\t\t} else {\n\t\t\tPyErr_Clear();\n\t\t\tcapi_arglist = (PyTupleObject *)Py_BuildValue("()");\n\t\t}\n\t}\n\tif (capi_arglist == NULL) {\n\t\tPyErr_SetString(#modulename#_error,"Callback #argname# argument list is not set.\\n");\n\t\tgoto capi_fail;\n\t}\n#setdims#\n#ifdef PYPY_VERSION\n#define CAPI_ARGLIST_SETITEM(idx, value) PyList_SetItem((PyObject *)capi_arglist_list, idx, value)\n\tcapi_arglist_list = PySequence_List(capi_arglist);\n\tif (capi_arglist_list == NULL) goto capi_fail;\n#else\n#define CAPI_ARGLIST_SETITEM(idx, value) PyTuple_SetItem((PyObject *)capi_arglist, idx, value)\n#endif\n#pyobjfrom#\n#undef CAPI_ARGLIST_SETITEM\n#ifdef PYPY_VERSION\n\tCFUNCSMESSPY("cb:capi_arglist=",capi_arglist_list);\n#else\n\tCFUNCSMESSPY("cb:capi_arglist=",capi_arglist);\n#endif\n\tCFUNCSMESS("cb:Call-back calling Python function #argname#.\\n");\n#ifdef F2PY_REPORT_ATEXIT\nf2py_cb_start_call_clock();\n#endif\n#ifdef PYPY_VERSION\n\tcapi_return = PyObject_CallObject(#name#_capi,(PyObject *)capi_arglist_list);\n\tPy_DECREF(capi_arglist_list);\n\tcapi_arglist_list = NULL;\n#else\n\tcapi_return = PyObject_CallObject(#name#_capi,(PyObject *)capi_arglist);\n#endif\n#ifdef F2PY_REPORT_ATEXIT\nf2py_cb_stop_call_clock();\n#endif\n\tCFUNCSMESSPY("cb:capi_return=",capi_return);\n\tif (capi_return == NULL) {\n\t\tfprintf(stderr,"capi_return is NULL\\n");\n\t\tgoto capi_fail;\n\t}\n\tif (capi_return == Py_None) {\n\t\tPy_DECREF(capi_return);\n\t\tcapi_return = Py_BuildValue("()");\n\t}\n\telse if (!PyTuple_Check(capi_return)) {\n\t\tcapi_return = Py_BuildValue("(N)",capi_return);\n\t}\n\tcapi_j = PyTuple_Size(capi_return);\n\tcapi_i = 0;\n#frompyobj#\n\tCFUNCSMESS("cb:#name#:successful\\n");\n\tPy_DECREF(capi_return);\n#ifdef F2PY_REPORT_ATEXIT\nf2py_cb_stop_clock();\n#endif\n\tgoto capi_return_pt;\ncapi_fail:\n\tfprintf(stderr,"Call-back #name# failed.\\n");\n\tPy_XDECREF(capi_return);\n\tPy_XDECREF(capi_arglist_list);\n\tif (capi_longjmp_ok)\n\t\tlongjmp(#name#_jmpbuf,-1);\ncapi_return_pt:\n\t;\n#return#\n}\n#endtitle#\n', 
 'need':[
  'setjmp.h', 'CFUNCSMESS'], 
 'maxnofargs':'#maxnofargs#', 
 'nofoptargs':'#nofoptargs#', 
 'docstr':'\tdef #argname#(#docsignature#): return #docreturn#\\n\\\n#docstrsigns#', 
 'latexdocstr':'\n{{}\\verb@def #argname#(#latexdocsignature#): return #docreturn#@{}}\n#routnote#\n\n#latexdocstrsigns#', 
 'docstrshort':'def #argname#(#docsignature#): return #docreturn#'}
cb_rout_rules = [
 {'separatorsfor':{'decl':'\n', 
   'args':',', 
   'optargs':'',  'pyobjfrom':'\n',  'freemem':'\n',  'args_td':',', 
   'optargs_td':'',  'args_nm':',', 
   'optargs_nm':'',  'frompyobj':'\n', 
   'setdims':'\n',  'docstrsigns':'\\n"\n"', 
   'latexdocstrsigns':'\n', 
   'latexdocstrreq':'\n', 
   'latexdocstropt':'\n',  'latexdocstrout':'\n', 
   'latexdocstrcbs':'\n'}, 
  'decl':'/*decl*/', 
  'pyobjfrom':'/*pyobjfrom*/',  'frompyobj':'/*frompyobj*/',  'args':[],  'optargs':'', 
  'return':'',  'strarglens':'',  'freemem':'/*freemem*/',  'args_td':[],  'optargs_td':'', 
  'strarglens_td':'',  'args_nm':[],  'optargs_nm':'', 
  'strarglens_nm':'',  'noargs':'', 
  'setdims':'/*setdims*/', 
  'docstrsigns':'', 
  'latexdocstrsigns':'',  'docstrreq':'\tRequired arguments:', 
  'docstropt':'\tOptional arguments:', 
  'docstrout':'\tReturn objects:', 
  'docstrcbs':'\tCall-back functions:', 
  'docreturn':'', 
  'docsign':'',  'docsignopt':'',  'latexdocstrreq':'\\noindent Required arguments:', 
  'latexdocstropt':'\\noindent Optional arguments:', 
  'latexdocstrout':'\\noindent Return objects:', 
  'latexdocstrcbs':'\\noindent Call-back functions:', 
  'routnote':{hasnote: '--- #note#', l_not(hasnote): ''}},
 {'decl':'\t#ctype# return_value;', 
  'frompyobj':[
   {debugcapi: '\tCFUNCSMESS("cb:Getting return_value->");'},
   '\tif (capi_j>capi_i)\n\t\tGETSCALARFROMPYTUPLE(capi_return,capi_i++,&return_value,#ctype#,"#ctype#_from_pyobj failed in converting return_value of call-back function #name# to C #ctype#\\n");',
   {debugcapi: '\tfprintf(stderr,"#showvalueformat#.\\n",return_value);'}], 
  'need':[
   '#ctype#_from_pyobj', {debugcapi: 'CFUNCSMESS'}, 'GETSCALARFROMPYTUPLE'], 
  'return':'\treturn return_value;', 
  '_check':l_and(isfunction, l_not(isstringfunction), l_not(iscomplexfunction))},
 {'pyobjfrom':{debugcapi: '\tfprintf(stderr,"debug-capi:cb:#name#:%d:\\n",return_value_len);'}, 
  'args':'#ctype# return_value,int return_value_len', 
  'args_nm':'return_value,&return_value_len', 
  'args_td':'#ctype# ,int', 
  'frompyobj':[
   {debugcapi: '\tCFUNCSMESS("cb:Getting return_value->\\"");'},
   '\tif (capi_j>capi_i)\n\t\tGETSTRFROMPYTUPLE(capi_return,capi_i++,return_value,return_value_len);',
   {debugcapi: '\tfprintf(stderr,"#showvalueformat#\\".\\n",return_value);'}], 
  'need':[
   '#ctype#_from_pyobj', {debugcapi: 'CFUNCSMESS'},
   'string.h', 'GETSTRFROMPYTUPLE'], 
  'return':'return;', 
  '_check':isstringfunction},
 {'optargs':'\n#ifndef F2PY_CB_RETURNCOMPLEX\n#ctype# *return_value\n#endif\n', 
  'optargs_nm':'\n#ifndef F2PY_CB_RETURNCOMPLEX\nreturn_value\n#endif\n', 
  'optargs_td':'\n#ifndef F2PY_CB_RETURNCOMPLEX\n#ctype# *\n#endif\n', 
  'decl':'\n#ifdef F2PY_CB_RETURNCOMPLEX\n\t#ctype# return_value;\n#endif\n', 
  'frompyobj':[
   {debugcapi: '\tCFUNCSMESS("cb:Getting return_value->");'},
   '\tif (capi_j>capi_i)\n#ifdef F2PY_CB_RETURNCOMPLEX\n\t\tGETSCALARFROMPYTUPLE(capi_return,capi_i++,&return_value,#ctype#,"#ctype#_from_pyobj failed in converting return_value of call-back function #name# to C #ctype#\\n");\n#else\n\t\tGETSCALARFROMPYTUPLE(capi_return,capi_i++,return_value,#ctype#,"#ctype#_from_pyobj failed in converting return_value of call-back function #name# to C #ctype#\\n");\n#endif\n',
   {debugcapi: '\n#ifdef F2PY_CB_RETURNCOMPLEX\n\tfprintf(stderr,"#showvalueformat#.\\n",(return_value).r,(return_value).i);\n#else\n\tfprintf(stderr,"#showvalueformat#.\\n",(*return_value).r,(*return_value).i);\n#endif\n\n'}], 
  'return':'\n#ifdef F2PY_CB_RETURNCOMPLEX\n\treturn return_value;\n#else\n\treturn;\n#endif\n', 
  'need':[
   '#ctype#_from_pyobj', {debugcapi: 'CFUNCSMESS'},
   'string.h', 'GETSCALARFROMPYTUPLE', '#ctype#'], 
  '_check':iscomplexfunction},
 {'docstrout':'\t\t#pydocsignout#', 
  'latexdocstrout':[
   '\\item[]{{}\\verb@#pydocsignout#@{}}',
   {hasnote: '--- #note#'}], 
  'docreturn':'#rname#,', 
  '_check':isfunction},
 {'_check':issubroutine, 
  'return':'return;'}]
cb_arg_rules = [
 {'docstropt':{l_and(isoptional, isintent_nothide): '\t\t#pydocsign#'}, 
  'docstrreq':{l_and(isrequired, isintent_nothide): '\t\t#pydocsign#'}, 
  'docstrout':{isintent_out: '\t\t#pydocsignout#'}, 
  'latexdocstropt':{l_and(isoptional, isintent_nothide): ['\\item[]{{}\\verb@#pydocsign#@{}}',
                                         {hasnote: '--- #note#'}]}, 
  'latexdocstrreq':{l_and(isrequired, isintent_nothide): ['\\item[]{{}\\verb@#pydocsign#@{}}',
                                         {hasnote: '--- #note#'}]}, 
  'latexdocstrout':{isintent_out: ['\\item[]{{}\\verb@#pydocsignout#@{}}',
                  {l_and(hasnote, isintent_hide): '--- #note#', 
                   l_and(hasnote, isintent_nothide): '--- See above.'}]}, 
  'docsign':{l_and(isrequired, isintent_nothide): '#varname#,'}, 
  'docsignopt':{l_and(isoptional, isintent_nothide): '#varname#,'}, 
  'depend':''},
 {'args':{l_and(isscalar, isintent_c): '#ctype# #varname_i#', 
   l_and(isscalar, l_not(isintent_c)): '#ctype# *#varname_i#_cb_capi', 
   isarray: '#ctype# *#varname_i#', 
   isstring: '#ctype# #varname_i#'}, 
  'args_nm':{l_and(isscalar, isintent_c): '#varname_i#', 
   l_and(isscalar, l_not(isintent_c)): '#varname_i#_cb_capi', 
   isarray: '#varname_i#', 
   isstring: '#varname_i#'}, 
  'args_td':{l_and(isscalar, isintent_c): '#ctype#', 
   l_and(isscalar, l_not(isintent_c)): '#ctype# *', 
   isarray: '#ctype# *', 
   isstring: '#ctype#'}, 
  'strarglens':{isstring: ',int #varname_i#_cb_len'}, 
  'strarglens_td':{isstring: ',int'}, 
  'strarglens_nm':{isstring: ',#varname_i#_cb_len'}},
 {'decl':{l_not(isintent_c): '\t#ctype# #varname_i#=(*#varname_i#_cb_capi);'}, 
  'error':{l_and(isintent_c, isintent_out, throw_error('intent(c,out) is forbidden for callback scalar arguments')): ''}, 
  'frompyobj':[
   {debugcapi: '\tCFUNCSMESS("cb:Getting #varname#->");'},
   {isintent_out: '\tif (capi_j>capi_i)\n\t\tGETSCALARFROMPYTUPLE(capi_return,capi_i++,#varname_i#_cb_capi,#ctype#,"#ctype#_from_pyobj failed in converting argument #varname# of call-back function #name# to C #ctype#\\n");'},
   {l_and(debugcapi, l_and(l_not(iscomplex), isintent_c)): '\tfprintf(stderr,"#showvalueformat#.\\n",#varname_i#);'},
   {l_and(debugcapi, l_and(l_not(iscomplex), l_not(isintent_c))): '\tfprintf(stderr,"#showvalueformat#.\\n",*#varname_i#_cb_capi);'},
   {l_and(debugcapi, l_and(iscomplex, isintent_c)): '\tfprintf(stderr,"#showvalueformat#.\\n",(#varname_i#).r,(#varname_i#).i);'},
   {l_and(debugcapi, l_and(iscomplex, l_not(isintent_c))): '\tfprintf(stderr,"#showvalueformat#.\\n",(*#varname_i#_cb_capi).r,(*#varname_i#_cb_capi).i);'}], 
  'need':[
   {isintent_out: ['#ctype#_from_pyobj', 'GETSCALARFROMPYTUPLE']},
   {debugcapi: 'CFUNCSMESS'}], 
  '_check':isscalar},
 {'pyobjfrom':[
   {isintent_in: '\tif (#name#_nofargs>capi_i)\n\t\tif (CAPI_ARGLIST_SETITEM(capi_i++,pyobj_from_#ctype#1(#varname_i#)))\n\t\t\tgoto capi_fail;'},
   {isintent_inout: '\tif (#name#_nofargs>capi_i)\n\t\tif (CAPI_ARGLIST_SETITEM(capi_i++,pyarr_from_p_#ctype#1(#varname_i#_cb_capi)))\n\t\t\tgoto capi_fail;'}], 
  'need':[
   {isintent_in: 'pyobj_from_#ctype#1'},
   {isintent_inout: 'pyarr_from_p_#ctype#1'},
   {iscomplex: '#ctype#'}], 
  '_check':l_and(isscalar, isintent_nothide), 
  '_optional':''},
 {'frompyobj':[
   {debugcapi: '\tCFUNCSMESS("cb:Getting #varname#->\\"");'},
   '\tif (capi_j>capi_i)\n\t\tGETSTRFROMPYTUPLE(capi_return,capi_i++,#varname_i#,#varname_i#_cb_len);',
   {debugcapi: '\tfprintf(stderr,"#showvalueformat#\\":%d:.\\n",#varname_i#,#varname_i#_cb_len);'}], 
  'need':[
   '#ctype#', 'GETSTRFROMPYTUPLE',
   {debugcapi: 'CFUNCSMESS'}, 'string.h'], 
  '_check':l_and(isstring, isintent_out)},
 {'pyobjfrom':[
   {debugcapi: '\tfprintf(stderr,"debug-capi:cb:#varname#=\\"#showvalueformat#\\":%d:\\n",#varname_i#,#varname_i#_cb_len);'},
   {isintent_in: '\tif (#name#_nofargs>capi_i)\n\t\tif (CAPI_ARGLIST_SETITEM(capi_i++,pyobj_from_#ctype#1size(#varname_i#,#varname_i#_cb_len)))\n\t\t\tgoto capi_fail;'},
   {isintent_inout: '\tif (#name#_nofargs>capi_i) {\n\t\tint #varname_i#_cb_dims[] = {#varname_i#_cb_len};\n\t\tif (CAPI_ARGLIST_SETITEM(capi_i++,pyarr_from_p_#ctype#1(#varname_i#,#varname_i#_cb_dims)))\n\t\t\tgoto capi_fail;\n\t}'}], 
  'need':[
   {isintent_in: 'pyobj_from_#ctype#1size'},
   {isintent_inout: 'pyarr_from_p_#ctype#1'}], 
  '_check':l_and(isstring, isintent_nothide), 
  '_optional':''},
 {'decl':'\tnpy_intp #varname_i#_Dims[#rank#] = {#rank*[-1]#};', 
  'setdims':'\t#cbsetdims#;', 
  '_check':isarray, 
  '_depend':''},
 {'pyobjfrom':[
   {debugcapi: '\tfprintf(stderr,"debug-capi:cb:#varname#\\n");'},
   {isintent_c: '\tif (#name#_nofargs>capi_i) {\n\t\tint itemsize_ = #atype# == NPY_STRING ? 1 : 0;\n\t\t/*XXX: Hmm, what will destroy this array??? */\n\t\tPyArrayObject *tmp_arr = (PyArrayObject *)PyArray_New(&PyArray_Type,#rank#,#varname_i#_Dims,#atype#,NULL,(char*)#varname_i#,itemsize_,NPY_ARRAY_CARRAY,NULL);\n', 
    l_not(isintent_c): '\tif (#name#_nofargs>capi_i) {\n\t\tint itemsize_ = #atype# == NPY_STRING ? 1 : 0;\n\t\t/*XXX: Hmm, what will destroy this array??? */\n\t\tPyArrayObject *tmp_arr = (PyArrayObject *)PyArray_New(&PyArray_Type,#rank#,#varname_i#_Dims,#atype#,NULL,(char*)#varname_i#,itemsize_,NPY_ARRAY_FARRAY,NULL);\n'},
   '\n\t\tif (tmp_arr==NULL)\n\t\t\tgoto capi_fail;\n\t\tif (CAPI_ARGLIST_SETITEM(capi_i++,(PyObject *)tmp_arr))\n\t\t\tgoto capi_fail;\n}'], 
  '_check':l_and(isarray, isintent_nothide, l_or(isintent_in, isintent_inout)), 
  '_optional':''},
 {'frompyobj':[
   {debugcapi: '\tCFUNCSMESS("cb:Getting #varname#->");'},
   '\tif (capi_j>capi_i) {\n\t\tPyArrayObject *rv_cb_arr = NULL;\n\t\tif ((capi_tmp = PyTuple_GetItem(capi_return,capi_i++))==NULL) goto capi_fail;\n\t\trv_cb_arr =  array_from_pyobj(#atype#,#varname_i#_Dims,#rank#,F2PY_INTENT_IN',
   {isintent_c: '|F2PY_INTENT_C'},
   ',capi_tmp);\n\t\tif (rv_cb_arr == NULL) {\n\t\t\tfprintf(stderr,"rv_cb_arr is NULL\\n");\n\t\t\tgoto capi_fail;\n\t\t}\n\t\tMEMCOPY(#varname_i#,PyArray_DATA(rv_cb_arr),PyArray_NBYTES(rv_cb_arr));\n\t\tif (capi_tmp != (PyObject *)rv_cb_arr) {\n\t\t\tPy_DECREF(rv_cb_arr);\n\t\t}\n\t}',
   {debugcapi: '\tfprintf(stderr,"<-.\\n");'}], 
  'need':[
   'MEMCOPY', {iscomplexarray: '#ctype#'}], 
  '_check':l_and(isarray, isintent_out)},
 {'docreturn':'#varname#,', 
  '_check':isintent_out}]
cb_map = {}

def buildcallbacks(m):
    global cb_map
    cb_map[m['name']] = []
    for bi in m['body']:
        if bi['block'] == 'interface':
            for b in bi['body']:
                if b:
                    buildcallback(b, m['name'])
                else:
                    errmess('warning: empty body for %s\n' % m['name'])


def buildcallback--- This code section failed: ---

 L. 454         0  LOAD_CONST               1
                2  LOAD_CONST               ('capi_maps',)
                4  IMPORT_NAME              
                6  IMPORT_FROM              capi_maps
                8  STORE_FAST               'capi_maps'
               10  POP_TOP          

 L. 456        12  LOAD_GLOBAL              outmess
               14  LOAD_STR                 '\tConstructing call-back function "cb_%s_in_%s"\n'

 L. 457        16  LOAD_FAST                'rout'
               18  LOAD_STR                 'name'
               20  BINARY_SUBSCR    
               22  LOAD_FAST                'um'
               24  BUILD_TUPLE_2         2 

 L. 456        26  BINARY_MODULO    
               28  CALL_FUNCTION_1       1  ''
               30  POP_TOP          

 L. 458        32  LOAD_GLOBAL              getargs
               34  LOAD_FAST                'rout'
               36  CALL_FUNCTION_1       1  ''
               38  UNPACK_SEQUENCE_2     2 
               40  STORE_FAST               'args'
               42  STORE_FAST               'depargs'

 L. 459        44  LOAD_FAST                'depargs'
               46  LOAD_FAST                'capi_maps'
               48  STORE_ATTR               depargs

 L. 460        50  LOAD_FAST                'rout'
               52  LOAD_STR                 'vars'
               54  BINARY_SUBSCR    
               56  STORE_FAST               'var'

 L. 461        58  LOAD_FAST                'capi_maps'
               60  LOAD_METHOD              cb_routsign2map
               62  LOAD_FAST                'rout'
               64  LOAD_FAST                'um'
               66  CALL_METHOD_2         2  ''
               68  STORE_FAST               'vrd'

 L. 462        70  LOAD_GLOBAL              dictappend
               72  BUILD_MAP_0           0 
               74  LOAD_FAST                'vrd'
               76  CALL_FUNCTION_2       2  ''
               78  STORE_FAST               'rd'

 L. 463        80  LOAD_GLOBAL              cb_map
               82  LOAD_FAST                'um'
               84  BINARY_SUBSCR    
               86  LOAD_METHOD              append
               88  LOAD_FAST                'rout'
               90  LOAD_STR                 'name'
               92  BINARY_SUBSCR    
               94  LOAD_FAST                'rd'
               96  LOAD_STR                 'name'
               98  BINARY_SUBSCR    
              100  BUILD_LIST_2          2 
              102  CALL_METHOD_1         1  ''
              104  POP_TOP          

 L. 464       106  LOAD_GLOBAL              cb_rout_rules
              108  GET_ITER         
            110_0  COME_FROM           164  '164'
            110_1  COME_FROM           140  '140'
              110  FOR_ITER            166  'to 166'
              112  STORE_FAST               'r'

 L. 465       114  LOAD_STR                 '_check'
              116  LOAD_FAST                'r'
              118  COMPARE_OP               in
              120  POP_JUMP_IF_FALSE   134  'to 134'
              122  LOAD_FAST                'r'
              124  LOAD_STR                 '_check'
              126  BINARY_SUBSCR    
              128  LOAD_FAST                'rout'
              130  CALL_FUNCTION_1       1  ''
              132  POP_JUMP_IF_TRUE    142  'to 142'
            134_0  COME_FROM           120  '120'
              134  LOAD_STR                 '_check'
              136  LOAD_FAST                'r'
              138  COMPARE_OP               not-in
              140  POP_JUMP_IF_FALSE_BACK   110  'to 110'
            142_0  COME_FROM           132  '132'

 L. 466       142  LOAD_GLOBAL              applyrules
              144  LOAD_FAST                'r'
              146  LOAD_FAST                'vrd'
              148  LOAD_FAST                'rout'
              150  CALL_FUNCTION_3       3  ''
              152  STORE_FAST               'ar'

 L. 467       154  LOAD_GLOBAL              dictappend
              156  LOAD_FAST                'rd'
              158  LOAD_FAST                'ar'
              160  CALL_FUNCTION_2       2  ''
              162  STORE_FAST               'rd'
              164  JUMP_BACK           110  'to 110'
            166_0  COME_FROM           110  '110'

 L. 468       166  BUILD_MAP_0           0 
              168  STORE_FAST               'savevrd'

 L. 469       170  LOAD_GLOBAL              enumerate
              172  LOAD_FAST                'args'
              174  CALL_FUNCTION_1       1  ''
              176  GET_ITER         
            178_0  COME_FROM           330  '330'
            178_1  COME_FROM           326  '326'
              178  FOR_ITER            332  'to 332'
              180  UNPACK_SEQUENCE_2     2 
              182  STORE_FAST               'i'
              184  STORE_FAST               'a'

 L. 470       186  LOAD_FAST                'capi_maps'
              188  LOAD_ATTR                cb_sign2map
              190  LOAD_FAST                'a'
              192  LOAD_FAST                'var'
              194  LOAD_FAST                'a'
              196  BINARY_SUBSCR    
              198  LOAD_FAST                'i'
              200  LOAD_CONST               ('index',)
              202  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              204  STORE_FAST               'vrd'

 L. 471       206  LOAD_FAST                'vrd'
              208  LOAD_FAST                'savevrd'
              210  LOAD_FAST                'a'
              212  STORE_SUBSCR     

 L. 472       214  LOAD_GLOBAL              cb_arg_rules
              216  GET_ITER         
            218_0  COME_FROM           328  '328'
            218_1  COME_FROM           322  '322'
            218_2  COME_FROM           288  '288'
            218_3  COME_FROM           252  '252'
            218_4  COME_FROM           230  '230'
              218  FOR_ITER            330  'to 330'
              220  STORE_FAST               'r'

 L. 473       222  LOAD_STR                 '_depend'
              224  LOAD_FAST                'r'
              226  COMPARE_OP               in
              228  POP_JUMP_IF_FALSE   232  'to 232'

 L. 474       230  JUMP_BACK           218  'to 218'
            232_0  COME_FROM           228  '228'

 L. 475       232  LOAD_STR                 '_optional'
              234  LOAD_FAST                'r'
              236  COMPARE_OP               in
              238  POP_JUMP_IF_FALSE   254  'to 254'
              240  LOAD_GLOBAL              isoptional
              242  LOAD_FAST                'var'
              244  LOAD_FAST                'a'
              246  BINARY_SUBSCR    
              248  CALL_FUNCTION_1       1  ''
              250  POP_JUMP_IF_FALSE   254  'to 254'

 L. 476       252  JUMP_BACK           218  'to 218'
            254_0  COME_FROM           250  '250'
            254_1  COME_FROM           238  '238'

 L. 477       254  LOAD_STR                 '_check'
              256  LOAD_FAST                'r'
              258  COMPARE_OP               in
          260_262  POP_JUMP_IF_FALSE   282  'to 282'
              264  LOAD_FAST                'r'
              266  LOAD_STR                 '_check'
              268  BINARY_SUBSCR    
              270  LOAD_FAST                'var'
              272  LOAD_FAST                'a'
              274  BINARY_SUBSCR    
              276  CALL_FUNCTION_1       1  ''
          278_280  POP_JUMP_IF_TRUE    290  'to 290'
            282_0  COME_FROM           260  '260'
              282  LOAD_STR                 '_check'
              284  LOAD_FAST                'r'
              286  COMPARE_OP               not-in
              288  POP_JUMP_IF_FALSE_BACK   218  'to 218'
            290_0  COME_FROM           278  '278'

 L. 478       290  LOAD_GLOBAL              applyrules
              292  LOAD_FAST                'r'
              294  LOAD_FAST                'vrd'
              296  LOAD_FAST                'var'
              298  LOAD_FAST                'a'
              300  BINARY_SUBSCR    
              302  CALL_FUNCTION_3       3  ''
              304  STORE_FAST               'ar'

 L. 479       306  LOAD_GLOBAL              dictappend
              308  LOAD_FAST                'rd'
              310  LOAD_FAST                'ar'
              312  CALL_FUNCTION_2       2  ''
              314  STORE_FAST               'rd'

 L. 480       316  LOAD_STR                 '_break'
              318  LOAD_FAST                'r'
              320  COMPARE_OP               in
              322  POP_JUMP_IF_FALSE_BACK   218  'to 218'

 L. 481       324  POP_TOP          
              326  BREAK_LOOP          178  'to 178'
              328  JUMP_BACK           218  'to 218'
            330_0  COME_FROM           218  '218'
              330  JUMP_BACK           178  'to 178'
            332_0  COME_FROM           178  '178'

 L. 482       332  LOAD_FAST                'args'
              334  GET_ITER         
            336_0  COME_FROM           492  '492'
            336_1  COME_FROM           484  '484'
              336  FOR_ITER            496  'to 496'
              338  STORE_FAST               'a'

 L. 483       340  LOAD_FAST                'savevrd'
              342  LOAD_FAST                'a'
              344  BINARY_SUBSCR    
              346  STORE_FAST               'vrd'

 L. 484       348  LOAD_GLOBAL              cb_arg_rules
              350  GET_ITER         
            352_0  COME_FROM           488  '488'
            352_1  COME_FROM           478  '478'
            352_2  COME_FROM           442  '442'
            352_3  COME_FROM           404  '404'
            352_4  COME_FROM           376  '376'
            352_5  COME_FROM           366  '366'
              352  FOR_ITER            492  'to 492'
              354  STORE_FAST               'r'

 L. 485       356  LOAD_STR                 '_depend'
              358  LOAD_FAST                'r'
              360  COMPARE_OP               in
          362_364  POP_JUMP_IF_FALSE   370  'to 370'

 L. 486   366_368  JUMP_BACK           352  'to 352'
            370_0  COME_FROM           362  '362'

 L. 487       370  LOAD_STR                 '_optional'
              372  LOAD_FAST                'r'
              374  COMPARE_OP               not-in
          376_378  POP_JUMP_IF_TRUE_BACK   352  'to 352'
              380  LOAD_STR                 '_optional'
              382  LOAD_FAST                'r'
              384  COMPARE_OP               in
          386_388  POP_JUMP_IF_FALSE   408  'to 408'
              390  LOAD_GLOBAL              isrequired
              392  LOAD_FAST                'var'
              394  LOAD_FAST                'a'
              396  BINARY_SUBSCR    
              398  CALL_FUNCTION_1       1  ''
          400_402  POP_JUMP_IF_FALSE   408  'to 408'

 L. 488   404_406  JUMP_BACK           352  'to 352'
            408_0  COME_FROM           400  '400'
            408_1  COME_FROM           386  '386'

 L. 489       408  LOAD_STR                 '_check'
              410  LOAD_FAST                'r'
              412  COMPARE_OP               in
          414_416  POP_JUMP_IF_FALSE   436  'to 436'
              418  LOAD_FAST                'r'
              420  LOAD_STR                 '_check'
              422  BINARY_SUBSCR    
              424  LOAD_FAST                'var'
              426  LOAD_FAST                'a'
              428  BINARY_SUBSCR    
              430  CALL_FUNCTION_1       1  ''
          432_434  POP_JUMP_IF_TRUE    446  'to 446'
            436_0  COME_FROM           414  '414'
              436  LOAD_STR                 '_check'
              438  LOAD_FAST                'r'
              440  COMPARE_OP               not-in
          442_444  POP_JUMP_IF_FALSE_BACK   352  'to 352'
            446_0  COME_FROM           432  '432'

 L. 490       446  LOAD_GLOBAL              applyrules
              448  LOAD_FAST                'r'
              450  LOAD_FAST                'vrd'
              452  LOAD_FAST                'var'
              454  LOAD_FAST                'a'
              456  BINARY_SUBSCR    
              458  CALL_FUNCTION_3       3  ''
              460  STORE_FAST               'ar'

 L. 491       462  LOAD_GLOBAL              dictappend
              464  LOAD_FAST                'rd'
              466  LOAD_FAST                'ar'
              468  CALL_FUNCTION_2       2  ''
              470  STORE_FAST               'rd'

 L. 492       472  LOAD_STR                 '_break'
              474  LOAD_FAST                'r'
              476  COMPARE_OP               in
          478_480  POP_JUMP_IF_FALSE_BACK   352  'to 352'

 L. 493       482  POP_TOP          
          484_486  BREAK_LOOP          336  'to 336'
          488_490  JUMP_BACK           352  'to 352'
            492_0  COME_FROM           352  '352'
          492_494  JUMP_BACK           336  'to 336'
            496_0  COME_FROM           336  '336'

 L. 494       496  LOAD_FAST                'depargs'
              498  GET_ITER         
            500_0  COME_FROM           632  '632'
            500_1  COME_FROM           624  '624'
              500  FOR_ITER            636  'to 636'
              502  STORE_FAST               'a'

 L. 495       504  LOAD_FAST                'savevrd'
              506  LOAD_FAST                'a'
              508  BINARY_SUBSCR    
              510  STORE_FAST               'vrd'

 L. 496       512  LOAD_GLOBAL              cb_arg_rules
              514  GET_ITER         
            516_0  COME_FROM           628  '628'
            516_1  COME_FROM           618  '618'
            516_2  COME_FROM           582  '582'
            516_3  COME_FROM           544  '544'
            516_4  COME_FROM           530  '530'
              516  FOR_ITER            632  'to 632'
              518  STORE_FAST               'r'

 L. 497       520  LOAD_STR                 '_depend'
              522  LOAD_FAST                'r'
              524  COMPARE_OP               not-in
          526_528  POP_JUMP_IF_FALSE   534  'to 534'

 L. 498   530_532  JUMP_BACK           516  'to 516'
            534_0  COME_FROM           526  '526'

 L. 499       534  LOAD_STR                 '_optional'
              536  LOAD_FAST                'r'
              538  COMPARE_OP               in
          540_542  POP_JUMP_IF_FALSE   548  'to 548'

 L. 500   544_546  JUMP_BACK           516  'to 516'
            548_0  COME_FROM           540  '540'

 L. 501       548  LOAD_STR                 '_check'
              550  LOAD_FAST                'r'
              552  COMPARE_OP               in
          554_556  POP_JUMP_IF_FALSE   576  'to 576'
              558  LOAD_FAST                'r'
              560  LOAD_STR                 '_check'
              562  BINARY_SUBSCR    
              564  LOAD_FAST                'var'
              566  LOAD_FAST                'a'
              568  BINARY_SUBSCR    
              570  CALL_FUNCTION_1       1  ''
          572_574  POP_JUMP_IF_TRUE    586  'to 586'
            576_0  COME_FROM           554  '554'
              576  LOAD_STR                 '_check'
              578  LOAD_FAST                'r'
              580  COMPARE_OP               not-in
          582_584  POP_JUMP_IF_FALSE_BACK   516  'to 516'
            586_0  COME_FROM           572  '572'

 L. 502       586  LOAD_GLOBAL              applyrules
              588  LOAD_FAST                'r'
              590  LOAD_FAST                'vrd'
              592  LOAD_FAST                'var'
              594  LOAD_FAST                'a'
              596  BINARY_SUBSCR    
              598  CALL_FUNCTION_3       3  ''
              600  STORE_FAST               'ar'

 L. 503       602  LOAD_GLOBAL              dictappend
              604  LOAD_FAST                'rd'
              606  LOAD_FAST                'ar'
              608  CALL_FUNCTION_2       2  ''
              610  STORE_FAST               'rd'

 L. 504       612  LOAD_STR                 '_break'
              614  LOAD_FAST                'r'
              616  COMPARE_OP               in
          618_620  POP_JUMP_IF_FALSE_BACK   516  'to 516'

 L. 505       622  POP_TOP          
          624_626  BREAK_LOOP          500  'to 500'
          628_630  JUMP_BACK           516  'to 516'
            632_0  COME_FROM           516  '516'
          632_634  JUMP_BACK           500  'to 500'
            636_0  COME_FROM           500  '500'

 L. 506       636  LOAD_STR                 'args'
              638  LOAD_FAST                'rd'
              640  COMPARE_OP               in
          642_644  POP_JUMP_IF_FALSE   726  'to 726'
              646  LOAD_STR                 'optargs'
              648  LOAD_FAST                'rd'
              650  COMPARE_OP               in
          652_654  POP_JUMP_IF_FALSE   726  'to 726'

 L. 507       656  LOAD_GLOBAL              isinstance
              658  LOAD_FAST                'rd'
              660  LOAD_STR                 'optargs'
              662  BINARY_SUBSCR    
              664  LOAD_GLOBAL              list
              666  CALL_FUNCTION_2       2  ''
          668_670  POP_JUMP_IF_FALSE   726  'to 726'

 L. 508       672  LOAD_FAST                'rd'
              674  LOAD_STR                 'optargs'
              676  BINARY_SUBSCR    
              678  LOAD_STR                 '\n#ifndef F2PY_CB_RETURNCOMPLEX\n,\n#endif\n'
              680  BUILD_LIST_1          1 
              682  BINARY_ADD       
              684  LOAD_FAST                'rd'
              686  LOAD_STR                 'optargs'
              688  STORE_SUBSCR     

 L. 513       690  LOAD_FAST                'rd'
              692  LOAD_STR                 'optargs_nm'
              694  BINARY_SUBSCR    
              696  LOAD_STR                 '\n#ifndef F2PY_CB_RETURNCOMPLEX\n,\n#endif\n'
              698  BUILD_LIST_1          1 
              700  BINARY_ADD       
              702  LOAD_FAST                'rd'
              704  LOAD_STR                 'optargs_nm'
              706  STORE_SUBSCR     

 L. 518       708  LOAD_FAST                'rd'
              710  LOAD_STR                 'optargs_td'
              712  BINARY_SUBSCR    
              714  LOAD_STR                 '\n#ifndef F2PY_CB_RETURNCOMPLEX\n,\n#endif\n'
              716  BUILD_LIST_1          1 
              718  BINARY_ADD       
              720  LOAD_FAST                'rd'
              722  LOAD_STR                 'optargs_td'
              724  STORE_SUBSCR     
            726_0  COME_FROM           668  '668'
            726_1  COME_FROM           652  '652'
            726_2  COME_FROM           642  '642'

 L. 523       726  LOAD_GLOBAL              isinstance
              728  LOAD_FAST                'rd'
              730  LOAD_STR                 'docreturn'
              732  BINARY_SUBSCR    
              734  LOAD_GLOBAL              list
              736  CALL_FUNCTION_2       2  ''
          738_740  POP_JUMP_IF_FALSE   768  'to 768'

 L. 524       742  LOAD_GLOBAL              stripcomma

 L. 525       744  LOAD_GLOBAL              replace
              746  LOAD_STR                 '#docreturn#'
              748  LOAD_STR                 'docreturn'
              750  LOAD_FAST                'rd'
              752  LOAD_STR                 'docreturn'
              754  BINARY_SUBSCR    
              756  BUILD_MAP_1           1 
              758  CALL_FUNCTION_2       2  ''

 L. 524       760  CALL_FUNCTION_1       1  ''
              762  LOAD_FAST                'rd'
              764  LOAD_STR                 'docreturn'
              766  STORE_SUBSCR     
            768_0  COME_FROM           738  '738'

 L. 526       768  LOAD_GLOBAL              stripcomma
              770  LOAD_GLOBAL              replace
              772  LOAD_STR                 '#docsignopt#'

 L. 527       774  LOAD_STR                 'docsignopt'
              776  LOAD_FAST                'rd'
              778  LOAD_STR                 'docsignopt'
              780  BINARY_SUBSCR    
              782  BUILD_MAP_1           1 

 L. 526       784  CALL_FUNCTION_2       2  ''
              786  CALL_FUNCTION_1       1  ''
              788  STORE_FAST               'optargs'

 L. 529       790  LOAD_FAST                'optargs'
              792  LOAD_STR                 ''
              794  COMPARE_OP               ==
          796_798  POP_JUMP_IF_FALSE   828  'to 828'

 L. 530       800  LOAD_GLOBAL              stripcomma

 L. 531       802  LOAD_GLOBAL              replace
              804  LOAD_STR                 '#docsign#'
              806  LOAD_STR                 'docsign'
              808  LOAD_FAST                'rd'
              810  LOAD_STR                 'docsign'
              812  BINARY_SUBSCR    
              814  BUILD_MAP_1           1 
              816  CALL_FUNCTION_2       2  ''

 L. 530       818  CALL_FUNCTION_1       1  ''
              820  LOAD_FAST                'rd'
              822  LOAD_STR                 'docsignature'
              824  STORE_SUBSCR     
              826  JUMP_FORWARD        852  'to 852'
            828_0  COME_FROM           796  '796'

 L. 533       828  LOAD_GLOBAL              replace
              830  LOAD_STR                 '#docsign#[#docsignopt#]'

 L. 534       832  LOAD_FAST                'rd'
              834  LOAD_STR                 'docsign'
              836  BINARY_SUBSCR    

 L. 535       838  LOAD_FAST                'optargs'

 L. 534       840  LOAD_CONST               ('docsign', 'docsignopt')
              842  BUILD_CONST_KEY_MAP_2     2 

 L. 533       844  CALL_FUNCTION_2       2  ''
              846  LOAD_FAST                'rd'
              848  LOAD_STR                 'docsignature'
              850  STORE_SUBSCR     
            852_0  COME_FROM           826  '826'

 L. 537       852  LOAD_FAST                'rd'
              854  LOAD_STR                 'docsignature'
              856  BINARY_SUBSCR    
              858  LOAD_METHOD              replace
              860  LOAD_STR                 '_'
              862  LOAD_STR                 '\\_'
              864  CALL_METHOD_2         2  ''
              866  LOAD_FAST                'rd'
              868  LOAD_STR                 'latexdocsignature'
              870  STORE_SUBSCR     

 L. 538       872  LOAD_FAST                'rd'
              874  LOAD_STR                 'latexdocsignature'
              876  BINARY_SUBSCR    
              878  LOAD_METHOD              replace
              880  LOAD_STR                 ','
              882  LOAD_STR                 ', '
              884  CALL_METHOD_2         2  ''
              886  LOAD_FAST                'rd'
              888  LOAD_STR                 'latexdocsignature'
              890  STORE_SUBSCR     

 L. 539       892  BUILD_LIST_0          0 
              894  LOAD_FAST                'rd'
              896  LOAD_STR                 'docstrsigns'
              898  STORE_SUBSCR     

 L. 540       900  BUILD_LIST_0          0 
              902  LOAD_FAST                'rd'
              904  LOAD_STR                 'latexdocstrsigns'
              906  STORE_SUBSCR     

 L. 541       908  LOAD_CONST               ('docstrreq', 'docstropt', 'docstrout', 'docstrcbs')
              910  GET_ITER         
            912_0  COME_FROM          1052  '1052'
            912_1  COME_FROM           992  '992'
            912_2  COME_FROM           976  '976'
              912  FOR_ITER           1056  'to 1056'
              914  STORE_FAST               'k'

 L. 542       916  LOAD_FAST                'k'
              918  LOAD_FAST                'rd'
              920  COMPARE_OP               in
          922_924  POP_JUMP_IF_FALSE   962  'to 962'
              926  LOAD_GLOBAL              isinstance
              928  LOAD_FAST                'rd'
              930  LOAD_FAST                'k'
              932  BINARY_SUBSCR    
              934  LOAD_GLOBAL              list
              936  CALL_FUNCTION_2       2  ''
          938_940  POP_JUMP_IF_FALSE   962  'to 962'

 L. 543       942  LOAD_FAST                'rd'
              944  LOAD_STR                 'docstrsigns'
              946  BINARY_SUBSCR    
              948  LOAD_FAST                'rd'
              950  LOAD_FAST                'k'
              952  BINARY_SUBSCR    
              954  BINARY_ADD       
              956  LOAD_FAST                'rd'
              958  LOAD_STR                 'docstrsigns'
              960  STORE_SUBSCR     
            962_0  COME_FROM           938  '938'
            962_1  COME_FROM           922  '922'

 L. 544       962  LOAD_STR                 'latex'
              964  LOAD_FAST                'k'
              966  BINARY_ADD       
              968  STORE_FAST               'k'

 L. 545       970  LOAD_FAST                'k'
              972  LOAD_FAST                'rd'
              974  COMPARE_OP               in
          976_978  POP_JUMP_IF_FALSE_BACK   912  'to 912'
              980  LOAD_GLOBAL              isinstance
              982  LOAD_FAST                'rd'
              984  LOAD_FAST                'k'
              986  BINARY_SUBSCR    
              988  LOAD_GLOBAL              list
              990  CALL_FUNCTION_2       2  ''
          992_994  POP_JUMP_IF_FALSE_BACK   912  'to 912'

 L. 546       996  LOAD_FAST                'rd'
              998  LOAD_STR                 'latexdocstrsigns'
             1000  BINARY_SUBSCR    
             1002  LOAD_FAST                'rd'
             1004  LOAD_FAST                'k'
             1006  BINARY_SUBSCR    
             1008  LOAD_CONST               0
             1010  LOAD_CONST               1
             1012  BUILD_SLICE_2         2 
             1014  BINARY_SUBSCR    
             1016  BINARY_ADD       

 L. 547      1018  LOAD_STR                 '\\begin{description}'
             1020  BUILD_LIST_1          1 

 L. 546      1022  BINARY_ADD       

 L. 547      1024  LOAD_FAST                'rd'
             1026  LOAD_FAST                'k'
             1028  BINARY_SUBSCR    
             1030  LOAD_CONST               1
             1032  LOAD_CONST               None
             1034  BUILD_SLICE_2         2 
             1036  BINARY_SUBSCR    

 L. 546      1038  BINARY_ADD       

 L. 548      1040  LOAD_STR                 '\\end{description}'
             1042  BUILD_LIST_1          1 

 L. 546      1044  BINARY_ADD       
             1046  LOAD_FAST                'rd'
             1048  LOAD_STR                 'latexdocstrsigns'
             1050  STORE_SUBSCR     
         1052_1054  JUMP_BACK           912  'to 912'
           1056_0  COME_FROM           912  '912'

 L. 549      1056  LOAD_STR                 'args'
             1058  LOAD_FAST                'rd'
             1060  COMPARE_OP               not-in
         1062_1064  POP_JUMP_IF_FALSE  1090  'to 1090'

 L. 550      1066  LOAD_STR                 ''
             1068  LOAD_FAST                'rd'
             1070  LOAD_STR                 'args'
             1072  STORE_SUBSCR     

 L. 551      1074  LOAD_STR                 ''
             1076  LOAD_FAST                'rd'
             1078  LOAD_STR                 'args_td'
             1080  STORE_SUBSCR     

 L. 552      1082  LOAD_STR                 ''
             1084  LOAD_FAST                'rd'
             1086  LOAD_STR                 'args_nm'
             1088  STORE_SUBSCR     
           1090_0  COME_FROM          1062  '1062'

 L. 553      1090  LOAD_FAST                'rd'
             1092  LOAD_METHOD              get
             1094  LOAD_STR                 'args'
             1096  CALL_METHOD_1         1  ''
         1098_1100  POP_JUMP_IF_TRUE   1134  'to 1134'
             1102  LOAD_FAST                'rd'
             1104  LOAD_METHOD              get
             1106  LOAD_STR                 'optargs'
             1108  CALL_METHOD_1         1  ''
         1110_1112  POP_JUMP_IF_TRUE   1134  'to 1134'
             1114  LOAD_FAST                'rd'
             1116  LOAD_METHOD              get
             1118  LOAD_STR                 'strarglens'
             1120  CALL_METHOD_1         1  ''
         1122_1124  POP_JUMP_IF_TRUE   1134  'to 1134'

 L. 554      1126  LOAD_STR                 'void'
             1128  LOAD_FAST                'rd'
             1130  LOAD_STR                 'noargs'
             1132  STORE_SUBSCR     
           1134_0  COME_FROM          1122  '1122'
           1134_1  COME_FROM          1110  '1110'
           1134_2  COME_FROM          1098  '1098'

 L. 556      1134  LOAD_GLOBAL              applyrules
             1136  LOAD_GLOBAL              cb_routine_rules
             1138  LOAD_FAST                'rd'
             1140  CALL_FUNCTION_2       2  ''
             1142  STORE_FAST               'ar'

 L. 557      1144  LOAD_FAST                'ar'
             1146  LOAD_STR                 'body'
             1148  BINARY_SUBSCR    
             1150  LOAD_GLOBAL              cfuncs
             1152  LOAD_ATTR                callbacks
             1154  LOAD_FAST                'rd'
             1156  LOAD_STR                 'name'
             1158  BINARY_SUBSCR    
             1160  STORE_SUBSCR     

 L. 558      1162  LOAD_GLOBAL              isinstance
             1164  LOAD_FAST                'ar'
             1166  LOAD_STR                 'need'
             1168  BINARY_SUBSCR    
             1170  LOAD_GLOBAL              str
             1172  CALL_FUNCTION_2       2  ''
         1174_1176  POP_JUMP_IF_FALSE  1192  'to 1192'

 L. 559      1178  LOAD_FAST                'ar'
             1180  LOAD_STR                 'need'
             1182  BINARY_SUBSCR    
             1184  BUILD_LIST_1          1 
             1186  LOAD_FAST                'ar'
             1188  LOAD_STR                 'need'
             1190  STORE_SUBSCR     
           1192_0  COME_FROM          1174  '1174'

 L. 561      1192  LOAD_STR                 'need'
             1194  LOAD_FAST                'rd'
             1196  COMPARE_OP               in
         1198_1200  POP_JUMP_IF_FALSE  1248  'to 1248'

 L. 562      1202  LOAD_GLOBAL              cfuncs
             1204  LOAD_ATTR                typedefs
             1206  LOAD_METHOD              keys
             1208  CALL_METHOD_0         0  ''
             1210  GET_ITER         
           1212_0  COME_FROM          1244  '1244'
           1212_1  COME_FROM          1226  '1226'
             1212  FOR_ITER           1248  'to 1248'
             1214  STORE_FAST               't'

 L. 563      1216  LOAD_FAST                't'
             1218  LOAD_FAST                'rd'
             1220  LOAD_STR                 'need'
             1222  BINARY_SUBSCR    
             1224  COMPARE_OP               in
         1226_1228  POP_JUMP_IF_FALSE_BACK  1212  'to 1212'

 L. 564      1230  LOAD_FAST                'ar'
             1232  LOAD_STR                 'need'
             1234  BINARY_SUBSCR    
             1236  LOAD_METHOD              append
             1238  LOAD_FAST                't'
             1240  CALL_METHOD_1         1  ''
             1242  POP_TOP          
         1244_1246  JUMP_BACK          1212  'to 1212'
           1248_0  COME_FROM          1212  '1212'
           1248_1  COME_FROM          1198  '1198'

 L. 566      1248  LOAD_FAST                'ar'
             1250  LOAD_STR                 'cbtypedefs'
             1252  BINARY_SUBSCR    
             1254  LOAD_GLOBAL              cfuncs
             1256  LOAD_ATTR                typedefs_generated
             1258  LOAD_FAST                'rd'
             1260  LOAD_STR                 'name'
             1262  BINARY_SUBSCR    
             1264  LOAD_STR                 '_typedef'
             1266  BINARY_ADD       
             1268  STORE_SUBSCR     

 L. 567      1270  LOAD_FAST                'ar'
             1272  LOAD_STR                 'need'
             1274  BINARY_SUBSCR    
             1276  LOAD_METHOD              append
             1278  LOAD_FAST                'rd'
             1280  LOAD_STR                 'name'
             1282  BINARY_SUBSCR    
             1284  LOAD_STR                 '_typedef'
             1286  BINARY_ADD       
             1288  CALL_METHOD_1         1  ''
             1290  POP_TOP          

 L. 568      1292  LOAD_FAST                'ar'
             1294  LOAD_STR                 'need'
             1296  BINARY_SUBSCR    
             1298  LOAD_GLOBAL              cfuncs
             1300  LOAD_ATTR                needs
             1302  LOAD_FAST                'rd'
             1304  LOAD_STR                 'name'
             1306  BINARY_SUBSCR    
             1308  STORE_SUBSCR     

 L. 570      1310  LOAD_FAST                'ar'
             1312  LOAD_STR                 'maxnofargs'
             1314  BINARY_SUBSCR    

 L. 571      1316  LOAD_FAST                'ar'
             1318  LOAD_STR                 'nofoptargs'
             1320  BINARY_SUBSCR    

 L. 572      1322  LOAD_FAST                'ar'
             1324  LOAD_STR                 'docstr'
             1326  BINARY_SUBSCR    

 L. 573      1328  LOAD_FAST                'ar'
             1330  LOAD_STR                 'latexdocstr'
             1332  BINARY_SUBSCR    

 L. 574      1334  LOAD_FAST                'rd'
             1336  LOAD_STR                 'argname'
             1338  BINARY_SUBSCR    

 L. 570      1340  LOAD_CONST               ('maxnofargs', 'nofoptargs', 'docstr', 'latexdocstr', 'argname')
             1342  BUILD_CONST_KEY_MAP_5     5 
             1344  LOAD_FAST                'capi_maps'
             1346  LOAD_ATTR                lcb2_map
             1348  LOAD_FAST                'rd'
             1350  LOAD_STR                 'name'
             1352  BINARY_SUBSCR    
             1354  STORE_SUBSCR     

 L. 576      1356  LOAD_GLOBAL              outmess
             1358  LOAD_STR                 '\t  %s\n'
             1360  LOAD_FAST                'ar'
             1362  LOAD_STR                 'docstrshort'
             1364  BINARY_SUBSCR    
             1366  BINARY_MODULO    
             1368  CALL_FUNCTION_1       1  ''
             1370  POP_TOP          

Parse error at or near `CALL_FUNCTION_1' instruction at offset 1368