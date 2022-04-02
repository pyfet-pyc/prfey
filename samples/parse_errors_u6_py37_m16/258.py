# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.11 (default, Sep  3 2021, 20:46:09) 
# [GCC 10.2.1 20210110]
# Embedded file name: cffi\vengine_cpy.py
import sys, imp
from . import model
from .error import VerificationError

class VCPythonEngine(object):
    _class_key = 'x'
    _gen_python_module = True

    def __init__(self, verifier):
        self.verifier = verifier
        self.ffi = verifier.ffi
        self._struct_pending_verification = {}
        self._types_of_builtin_functions = {}

    def patch_extension_kwds(self, kwds):
        pass

    def find_module(self, module_name, path, so_suffixes):
        try:
            f, filename, descr = imp.find_module(module_name, path)
        except ImportError:
            return
        else:
            if f is not None:
                f.close()
            if descr[0] not in so_suffixes:
                return
            return filename

    def collect_types(self):
        self._typesdict = {}
        self._generate('collecttype')

    def _prnt(self, what=''):
        self._f.write(what + '\n')

    def _gettypenum(self, type):
        return self._typesdict[type]

    def _do_collect_type--- This code section failed: ---

 L.  48         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'tp'
                4  LOAD_GLOBAL              model
                6  LOAD_ATTR                PrimitiveType
                8  CALL_FUNCTION_2       2  '2 positional arguments'
               10  POP_JUMP_IF_FALSE    22  'to 22'

 L.  49        12  LOAD_FAST                'tp'
               14  LOAD_ATTR                name
               16  LOAD_STR                 'long double'
               18  COMPARE_OP               ==
               20  POP_JUMP_IF_FALSE    52  'to 52'
             22_0  COME_FROM            10  '10'

 L.  50        22  LOAD_FAST                'tp'
               24  LOAD_FAST                'self'
               26  LOAD_ATTR                _typesdict
               28  COMPARE_OP               not-in
               30  POP_JUMP_IF_FALSE    52  'to 52'

 L.  51        32  LOAD_GLOBAL              len
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                _typesdict
               38  CALL_FUNCTION_1       1  '1 positional argument'
               40  STORE_FAST               'num'

 L.  52        42  LOAD_FAST                'num'
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                _typesdict
               48  LOAD_FAST                'tp'
               50  STORE_SUBSCR     
             52_0  COME_FROM            30  '30'
             52_1  COME_FROM            20  '20'

Parse error at or near `COME_FROM' instruction at offset 52_0

    def write_source_to_f(self):
        self.collect_types()
        self._chained_list_constants = [
         '((void)lib,0)', '((void)lib,0)']
        prnt = self._prnt
        prnt(cffimod_header)
        prnt()
        prnt(self.verifier.preamble)
        prnt()
        self._generate('decl')
        self._generate_setup_custom()
        prnt()
        prnt('static PyMethodDef _cffi_methods[] = {')
        self._generate('method')
        prnt('  {"_cffi_setup", _cffi_setup, METH_VARARGS, NULL},')
        prnt('  {NULL, NULL, 0, NULL}    /* Sentinel */')
        prnt('};')
        prnt()
        modname = self.verifier.get_module_name()
        constants = self._chained_list_constants[False]
        prnt('#if PY_MAJOR_VERSION >= 3')
        prnt()
        prnt('static struct PyModuleDef _cffi_module_def = {')
        prnt('  PyModuleDef_HEAD_INIT,')
        prnt('  "%s",' % modname)
        prnt('  NULL,')
        prnt('  -1,')
        prnt('  _cffi_methods,')
        prnt('  NULL, NULL, NULL, NULL')
        prnt('};')
        prnt()
        prnt('PyMODINIT_FUNC')
        prnt('PyInit_%s(void)' % modname)
        prnt('{')
        prnt('  PyObject *lib;')
        prnt('  lib = PyModule_Create(&_cffi_module_def);')
        prnt('  if (lib == NULL)')
        prnt('    return NULL;')
        prnt('  if (%s < 0 || _cffi_init() < 0) {' % (constants,))
        prnt('    Py_DECREF(lib);')
        prnt('    return NULL;')
        prnt('  }')
        prnt('  return lib;')
        prnt('}')
        prnt()
        prnt('#else')
        prnt()
        prnt('PyMODINIT_FUNC')
        prnt('init%s(void)' % modname)
        prnt('{')
        prnt('  PyObject *lib;')
        prnt('  lib = Py_InitModule("%s", _cffi_methods);' % modname)
        prnt('  if (lib == NULL)')
        prnt('    return;')
        prnt('  if (%s < 0 || _cffi_init() < 0)' % (constants,))
        prnt('    return;')
        prnt('  return;')
        prnt('}')
        prnt()
        prnt('#endif')

    def load_library(self, flags=None):
        imp.acquire_lock()
        try:
            if hasattr(sys, 'getdlopenflags'):
                previous_flags = sys.getdlopenflags()
            try:
                try:
                    if hasattr(sys, 'setdlopenflags'):
                        if flags is not None:
                            sys.setdlopenflags(flags)
                    module = imp.load_dynamic(self.verifier.get_module_name(), self.verifier.modulefilename)
                except ImportError as e:
                    try:
                        error = 'importing %r: %s' % (self.verifier.modulefilename, e)
                        raise VerificationError(error)
                    finally:
                        e = None
                        del e

            finally:
                if hasattr(sys, 'setdlopenflags'):
                    sys.setdlopenflags(previous_flags)

        finally:
            imp.release_lock()

        self._load(module, 'loading')
        revmapping = dict([(value, key) for key, value in self._typesdict.items()])
        lst = [revmapping[i] for i in range(len(revmapping))]
        lst = list(map(self.ffi._get_cached_btype, lst))

        class FFILibrary(object):
            _cffi_python_module = module
            _cffi_ffi = self.ffi
            _cffi_dir = []

            def __dir__(self):
                return FFILibrary._cffi_dir + list(self.__dict__)

        library = FFILibrary()
        if module._cffi_setup(lst, VerificationError, library):
            import warnings
            warnings.warn('reimporting %r might overwrite older definitions' % self.verifier.get_module_name())
        self._load(module, 'loaded', library=library)
        module._cffi_original_ffi = self.ffi
        module._cffi_types_of_builtin_funcs = self._types_of_builtin_functions
        return library

    def _get_declarations(self):
        lst = [(key, tp) for key, (tp, qual) in self.ffi._parser._declarations.items()]
        lst.sort()
        return lst

    def _generate(self, step_name):
        for name, tp in self._get_declarations():
            kind, realname = name.split(' ', 1)
            try:
                method = getattr(self, '_generate_cpy_%s_%s' % (kind,
                 step_name))
            except AttributeError:
                raise VerificationError('not implemented in verify(): %r' % name)

            try:
                method(tp, realname)
            except Exception as e:
                try:
                    model.attach_exception_info(e, name)
                    raise
                finally:
                    e = None
                    del e

    def _load(self, module, step_name, **kwds):
        for name, tp in self._get_declarations():
            kind, realname = name.split(' ', 1)
            method = getattr(self, '_%s_cpy_%s' % (step_name, kind))
            try:
                method(tp, realname, module, **kwds)
            except Exception as e:
                try:
                    model.attach_exception_info(e, name)
                    raise
                finally:
                    e = None
                    del e

    def _generate_nothing(self, tp, name):
        pass

    def _loaded_noop(self, tp, name, module, **kwds):
        pass

    def _convert_funcarg_to_c(self, tp, fromvar, tovar, errcode):
        extraarg = ''
        if isinstance(tp, model.PrimitiveType):
            if tp.is_integer_type() and tp.name != '_Bool':
                converter = '_cffi_to_c_int'
                extraarg = ', %s' % tp.name
            else:
                converter = '(%s)_cffi_to_c_%s' % (tp.get_c_name(''),
                 tp.name.replace(' ', '_'))
            errvalue = '-1'
        else:
            if isinstance(tp, model.PointerType):
                self._convert_funcarg_to_c_ptr_or_array(tp, fromvar, tovar, errcode)
                return
            elif isinstance(tp, (model.StructOrUnion, model.EnumType)):
                self._prnt('  if (_cffi_to_c((char *)&%s, _cffi_type(%d), %s) < 0)' % (
                 tovar, self._gettypenum(tp), fromvar))
                self._prnt('    %s;' % errcode)
                return
                if isinstance(tp, model.FunctionPtrType):
                    converter = '(%s)_cffi_to_c_pointer' % tp.get_c_name('')
                    extraarg = ', _cffi_type(%d)' % self._gettypenum(tp)
                    errvalue = 'NULL'
            else:
                raise NotImplementedError(tp)
        self._prnt('  %s = %s(%s%s);' % (tovar, converter, fromvar, extraarg))
        self._prnt('  if (%s == (%s)%s && PyErr_Occurred())' % (
         tovar, tp.get_c_name(''), errvalue))
        self._prnt('    %s;' % errcode)

    def _extra_local_variables(self, tp, localvars, freelines):
        if isinstance(tp, model.PointerType):
            localvars.add('Py_ssize_t datasize')
            localvars.add('struct _cffi_freeme_s *large_args_free = NULL')
            freelines.add('if (large_args_free != NULL) _cffi_free_array_arguments(large_args_free);')

    def _convert_funcarg_to_c_ptr_or_array(self, tp, fromvar, tovar, errcode):
        self._prnt('  datasize = _cffi_prepare_pointer_call_argument(')
        self._prnt('      _cffi_type(%d), %s, (char **)&%s);' % (
         self._gettypenum(tp), fromvar, tovar))
        self._prnt('  if (datasize != 0) {')
        self._prnt('    %s = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;' % (
         tovar,))
        self._prnt('    if (_cffi_convert_array_argument(_cffi_type(%d), %s, (char **)&%s,' % (
         self._gettypenum(tp), fromvar, tovar))
        self._prnt('            datasize, &large_args_free) < 0)')
        self._prnt('      %s;' % errcode)
        self._prnt('  }')

    def _convert_expr_from_c(self, tp, var, context):
        if isinstance(tp, model.PrimitiveType):
            if tp.is_integer_type():
                if tp.name != '_Bool':
                    return '_cffi_from_c_int(%s, %s)' % (var, tp.name)
            if tp.name != 'long double':
                return '_cffi_from_c_%s(%s)' % (tp.name.replace(' ', '_'), var)
            return '_cffi_from_c_deref((char *)&%s, _cffi_type(%d))' % (
             var, self._gettypenum(tp))
        else:
            if isinstance(tp, (model.PointerType, model.FunctionPtrType)):
                return '_cffi_from_c_pointer((char *)%s, _cffi_type(%d))' % (
                 var, self._gettypenum(tp))
            if isinstance(tp, model.ArrayType):
                return '_cffi_from_c_pointer((char *)%s, _cffi_type(%d))' % (
                 var, self._gettypenum(model.PointerType(tp.item)))
            if isinstance(tp, model.StructOrUnion):
                if tp.fldnames is None:
                    raise TypeError("'%s' is used as %s, but is opaque" % (
                     tp._get_c_name(), context))
                return '_cffi_from_c_struct((char *)&%s, _cffi_type(%d))' % (
                 var, self._gettypenum(tp))
            if isinstance(tp, model.EnumType):
                return '_cffi_from_c_deref((char *)&%s, _cffi_type(%d))' % (
                 var, self._gettypenum(tp))
            raise NotImplementedError(tp)

    _generate_cpy_typedef_collecttype = _generate_nothing
    _generate_cpy_typedef_decl = _generate_nothing
    _generate_cpy_typedef_method = _generate_nothing
    _loading_cpy_typedef = _loaded_noop
    _loaded_cpy_typedef = _loaded_noop

    def _generate_cpy_function_collecttype(self, tp, name):
        if not isinstance(tp, model.FunctionPtrType):
            raise AssertionError
        elif tp.ellipsis:
            self._do_collect_type(tp)
        else:
            for type in tp.args:
                self._do_collect_type(type)

            self._do_collect_type(tp.result)

    def _generate_cpy_function_decl(self, tp, name):
        if not isinstance(tp, model.FunctionPtrType):
            raise AssertionError
        elif tp.ellipsis:
            self._generate_cpy_const(False, name, tp)
            return
            prnt = self._prnt
            numargs = len(tp.args)
            if numargs == 0:
                argname = 'noarg'
            else:
                if numargs == 1:
                    argname = 'arg0'
                else:
                    argname = 'args'
            prnt('static PyObject *')
            prnt('_cffi_f_%s(PyObject *self, PyObject *%s)' % (name, argname))
            prnt('{')
            context = 'argument of %s' % name
            for i, type in enumerate(tp.args):
                prnt('  %s;' % type.get_c_name(' x%d' % i, context))

            localvars = set()
            freelines = set()
            for type in tp.args:
                self._extra_local_variables(type, localvars, freelines)

            for decl in sorted(localvars):
                prnt('  %s;' % (decl,))

            if not isinstance(tp.result, model.VoidType):
                result_code = 'result = '
                context = 'result of %s' % name
                prnt('  %s;' % tp.result.get_c_name(' result', context))
                prnt('  PyObject *pyresult;')
            else:
                result_code = ''
            if len(tp.args) > 1:
                rng = range(len(tp.args))
                for i in rng:
                    prnt('  PyObject *arg%d;' % i)

                prnt()
                prnt('  if (!PyArg_ParseTuple(args, "%s:%s", %s))' % (
                 'O' * numargs, name, ', '.join(['&arg%d' % i for i in rng])))
                prnt('    return NULL;')
            prnt()
            for i, type in enumerate(tp.args):
                self._convert_funcarg_to_c(type, 'arg%d' % i, 'x%d' % i, 'return NULL')
                prnt()

            prnt('  Py_BEGIN_ALLOW_THREADS')
            prnt('  _cffi_restore_errno();')
            prnt('  { %s%s(%s); }' % (
             result_code, name,
             ', '.join(['x%d' % i for i in range(len(tp.args))])))
            prnt('  _cffi_save_errno();')
            prnt('  Py_END_ALLOW_THREADS')
            prnt()
            prnt('  (void)self; /* unused */')
            if numargs == 0:
                prnt('  (void)noarg; /* unused */')
            if result_code:
                prnt('  pyresult = %s;' % self._convert_expr_from_c(tp.result, 'result', 'result type'))
                for freeline in freelines:
                    prnt('  ' + freeline)

                prnt('  return pyresult;')
        else:
            for freeline in freelines:
                prnt('  ' + freeline)

            prnt('  Py_INCREF(Py_None);')
            prnt('  return Py_None;')
        prnt('}')
        prnt()

    def _generate_cpy_function_method(self, tp, name):
        if tp.ellipsis:
            return
        else:
            numargs = len(tp.args)
            if numargs == 0:
                meth = 'METH_NOARGS'
            else:
                if numargs == 1:
                    meth = 'METH_O'
                else:
                    meth = 'METH_VARARGS'
        self._prnt('  {"%s", _cffi_f_%s, %s, NULL},' % (name, name, meth))

    _loading_cpy_function = _loaded_noop

    def _loaded_cpy_function(self, tp, name, module, library):
        if tp.ellipsis:
            return
        func = getattr(module, name)
        setattr(library, name, func)
        self._types_of_builtin_functions[func] = tp

    _generate_cpy_struct_collecttype = _generate_nothing

    def _generate_cpy_struct_decl(self, tp, name):
        assert name == tp.name
        self._generate_struct_or_union_decl(tp, 'struct', name)

    def _generate_cpy_struct_method(self, tp, name):
        self._generate_struct_or_union_method(tp, 'struct', name)

    def _loading_cpy_struct(self, tp, name, module):
        self._loading_struct_or_union(tp, 'struct', name, module)

    def _loaded_cpy_struct(self, tp, name, module, **kwds):
        self._loaded_struct_or_union(tp)

    _generate_cpy_union_collecttype = _generate_nothing

    def _generate_cpy_union_decl(self, tp, name):
        assert name == tp.name
        self._generate_struct_or_union_decl(tp, 'union', name)

    def _generate_cpy_union_method(self, tp, name):
        self._generate_struct_or_union_method(tp, 'union', name)

    def _loading_cpy_union(self, tp, name, module):
        self._loading_struct_or_union(tp, 'union', name, module)

    def _loaded_cpy_union(self, tp, name, module, **kwds):
        self._loaded_struct_or_union(tp)

    def _generate_struct_or_union_decl(self, tp, prefix, name):
        if tp.fldnames is None:
            return
        checkfuncname = '_cffi_check_%s_%s' % (prefix, name)
        layoutfuncname = '_cffi_layout_%s_%s' % (prefix, name)
        cname = ('%s %s' % (prefix, name)).strip()
        prnt = self._prnt
        prnt('static void %s(%s *p)' % (checkfuncname, cname))
        prnt('{')
        prnt('  /* only to generate compile-time warnings or errors */')
        prnt('  (void)p;')
        for fname, ftype, fbitsize, fqual in tp.enumfields():
            if isinstance(ftype, model.PrimitiveType) and ftype.is_integer_type() or fbitsize >= 0:
                prnt('  (void)((p->%s) << 1);' % fname)
            else:
                try:
                    prnt('  { %s = &p->%s; (void)tmp; }' % (
                     ftype.get_c_name('*tmp', ('field %r' % fname), quals=fqual),
                     fname))
                except VerificationError as e:
                    try:
                        prnt('  /* %s */' % str(e))
                    finally:
                        e = None
                        del e

        prnt('}')
        prnt('static PyObject *')
        prnt('%s(PyObject *self, PyObject *noarg)' % (layoutfuncname,))
        prnt('{')
        prnt('  struct _cffi_aligncheck { char x; %s y; };' % cname)
        prnt('  static Py_ssize_t nums[] = {')
        prnt('    sizeof(%s),' % cname)
        prnt('    offsetof(struct _cffi_aligncheck, y),')
        for fname, ftype, fbitsize, fqual in tp.enumfields():
            if fbitsize >= 0:
                continue
            prnt('    offsetof(%s, %s),' % (cname, fname))
            if isinstance(ftype, model.ArrayType) and ftype.length is None:
                prnt('    0,  /* %s */' % ftype._get_c_name())
            else:
                prnt('    sizeof(((%s *)0)->%s),' % (cname, fname))

        prnt('    -1')
        prnt('  };')
        prnt('  (void)self; /* unused */')
        prnt('  (void)noarg; /* unused */')
        prnt('  return _cffi_get_struct_layout(nums);')
        prnt('  /* the next line is not executed, but compiled */')
        prnt('  %s(0);' % (checkfuncname,))
        prnt('}')
        prnt()

    def _generate_struct_or_union_method(self, tp, prefix, name):
        if tp.fldnames is None:
            return
        layoutfuncname = '_cffi_layout_%s_%s' % (prefix, name)
        self._prnt('  {"%s", %s, METH_NOARGS, NULL},' % (layoutfuncname,
         layoutfuncname))

    def _loading_struct_or_union(self, tp, prefix, name, module):
        if tp.fldnames is None:
            return
        layoutfuncname = '_cffi_layout_%s_%s' % (prefix, name)
        function = getattr(module, layoutfuncname)
        layout = function()
        if isinstance(tp, model.StructOrUnion) and tp.partial:
            totalsize = layout[0]
            totalalignment = layout[1]
            fieldofs = layout[2::2]
            fieldsize = layout[3::2]
            tp.force_flatten()
            assert len(fieldofs) == len(fieldsize) == len(tp.fldnames)
            tp.fixedlayout = (fieldofs, fieldsize, totalsize, totalalignment)
        else:
            cname = ('%s %s' % (prefix, name)).strip()
            self._struct_pending_verification[tp] = (layout, cname)

    def _loaded_struct_or_union(self, tp):
        if tp.fldnames is None:
            return
        self.ffi._get_cached_btype(tp)
        if tp in self._struct_pending_verification:

            def check(realvalue, expectedvalue, msg):
                if realvalue != expectedvalue:
                    raise VerificationError('%s (we have %d, but C compiler says %d)' % (
                     msg, expectedvalue, realvalue))

            ffi = self.ffi
            BStruct = ffi._get_cached_btype(tp)
            layout, cname = self._struct_pending_verification.pop(tp)
            check(layout[0], ffi.sizeof(BStruct), 'wrong total size')
            check(layout[1], ffi.alignof(BStruct), 'wrong total alignment')
            i = 2
            for fname, ftype, fbitsize, fqual in tp.enumfields():
                if fbitsize >= 0:
                    continue
                check(layout[i], ffi.offsetof(BStruct, fname), 'wrong offset for field %r' % (fname,))
                if layout[(i + 1)] != 0:
                    BField = ffi._get_cached_btype(ftype)
                    check(layout[(i + 1)], ffi.sizeof(BField), 'wrong size for field %r' % (fname,))
                i += 2

            assert i == len(layout)

    _generate_cpy_anonymous_collecttype = _generate_nothing

    def _generate_cpy_anonymous_decl(self, tp, name):
        if isinstance(tp, model.EnumType):
            self._generate_cpy_enum_decl(tp, name, '')
        else:
            self._generate_struct_or_union_decl(tp, '', name)

    def _generate_cpy_anonymous_method(self, tp, name):
        if not isinstance(tp, model.EnumType):
            self._generate_struct_or_union_method(tp, '', name)

    def _loading_cpy_anonymous(self, tp, name, module):
        if isinstance(tp, model.EnumType):
            self._loading_cpy_enum(tp, name, module)
        else:
            self._loading_struct_or_union(tp, '', name, module)

    def _loaded_cpy_anonymous(self, tp, name, module, **kwds):
        if isinstance(tp, model.EnumType):
            (self._loaded_cpy_enum)(tp, name, module, **kwds)
        else:
            self._loaded_struct_or_union(tp)

    def _generate_cpy_const(self, is_int, name, tp=None, category='const', vartp=None, delayed=True, size_too=False, check_value=None):
        prnt = self._prnt
        funcname = '_cffi_%s_%s' % (category, name)
        prnt('static int %s(PyObject *lib)' % funcname)
        prnt('{')
        prnt('  PyObject *o;')
        prnt('  int res;')
        if not is_int:
            prnt('  %s;' % (vartp or tp).get_c_name(' i', name))
        else:
            if not category == 'const':
                raise AssertionError
            elif check_value is not None:
                self._check_int_constant_value(name, check_value)
            else:
                if (is_int or category) == 'var':
                    realexpr = '&' + name
                else:
                    realexpr = name
                prnt('  i = (%s);' % (realexpr,))
                prnt('  o = %s;' % (
                 self._convert_expr_from_c(tp, 'i', 'variable type'),))
                if not delayed:
                    raise AssertionError
                else:
                    prnt('  o = _cffi_from_c_int_const(%s);' % name)
            prnt('  if (o == NULL)')
            prnt('    return -1;')
            if size_too:
                prnt('  {')
                prnt('    PyObject *o1 = o;')
                prnt('    o = Py_BuildValue("On", o1, (Py_ssize_t)sizeof(%s));' % (
                 name,))
                prnt('    Py_DECREF(o1);')
                prnt('    if (o == NULL)')
                prnt('      return -1;')
                prnt('  }')
            prnt('  res = PyObject_SetAttrString(lib, "%s", o);' % name)
            prnt('  Py_DECREF(o);')
            prnt('  if (res < 0)')
            prnt('    return -1;')
            prnt('  return %s;' % self._chained_list_constants[delayed])
            self._chained_list_constants[delayed] = funcname + '(lib)'
            prnt('}')
            prnt()

    def _generate_cpy_constant_collecttype(self, tp, name):
        is_int = isinstance(tp, model.PrimitiveType) and tp.is_integer_type()
        if not is_int:
            self._do_collect_type(tp)

    def _generate_cpy_constant_decl(self, tp, name):
        is_int = isinstance(tp, model.PrimitiveType) and tp.is_integer_type()
        self._generate_cpy_const(is_int, name, tp)

    _generate_cpy_constant_method = _generate_nothing
    _loading_cpy_constant = _loaded_noop
    _loaded_cpy_constant = _loaded_noop

    def _check_int_constant_value(self, name, value, err_prefix=''):
        prnt = self._prnt
        if value <= 0:
            prnt('  if ((%s) > 0 || (long)(%s) != %dL) {' % (
             name, name, value))
        else:
            prnt('  if ((%s) <= 0 || (unsigned long)(%s) != %dUL) {' % (
             name, name, value))
        prnt('    char buf[64];')
        prnt('    if ((%s) <= 0)' % name)
        prnt('        snprintf(buf, 63, "%%ld", (long)(%s));' % name)
        prnt('    else')
        prnt('        snprintf(buf, 63, "%%lu", (unsigned long)(%s));' % name)
        prnt('    PyErr_Format(_cffi_VerificationError,')
        prnt('                 "%s%s has the real value %s, not %s",')
        prnt('                 "%s", "%s", buf, "%d");' % (
         err_prefix, name, value))
        prnt('    return -1;')
        prnt('  }')

    def _enum_funcname(self, prefix, name):
        name = name.replace('$', '___D_')
        return '_cffi_e_%s_%s' % (prefix, name)

    def _generate_cpy_enum_decl(self, tp, name, prefix='enum'):
        if tp.partial:
            for enumerator in tp.enumerators:
                self._generate_cpy_const(True, enumerator, delayed=False)

            return
        funcname = self._enum_funcname(prefix, name)
        prnt = self._prnt
        prnt('static int %s(PyObject *lib)' % funcname)
        prnt('{')
        for enumerator, enumvalue in zip(tp.enumerators, tp.enumvalues):
            self._check_int_constant_value(enumerator, enumvalue, 'enum %s: ' % name)

        prnt('  return %s;' % self._chained_list_constants[True])
        self._chained_list_constants[True] = funcname + '(lib)'
        prnt('}')
        prnt()

    _generate_cpy_enum_collecttype = _generate_nothing
    _generate_cpy_enum_method = _generate_nothing

    def _loading_cpy_enum(self, tp, name, module):
        if tp.partial:
            enumvalues = [getattr(module, enumerator) for enumerator in tp.enumerators]
            tp.enumvalues = tuple(enumvalues)
            tp.partial_resolved = True

    def _loaded_cpy_enum(self, tp, name, module, library):
        for enumerator, enumvalue in zip(tp.enumerators, tp.enumvalues):
            setattr(library, enumerator, enumvalue)

    def _generate_cpy_macro_decl(self, tp, name):
        if tp == '...':
            check_value = None
        else:
            check_value = tp
        self._generate_cpy_const(True, name, check_value=check_value)

    _generate_cpy_macro_collecttype = _generate_nothing
    _generate_cpy_macro_method = _generate_nothing
    _loading_cpy_macro = _loaded_noop
    _loaded_cpy_macro = _loaded_noop

    def _generate_cpy_variable_collecttype(self, tp, name):
        if isinstance(tp, model.ArrayType):
            tp_ptr = model.PointerType(tp.item)
        else:
            tp_ptr = model.PointerType(tp)
        self._do_collect_type(tp_ptr)

    def _generate_cpy_variable_decl(self, tp, name):
        if isinstance(tp, model.ArrayType):
            tp_ptr = model.PointerType(tp.item)
            self._generate_cpy_const(False, name, tp, vartp=tp_ptr, size_too=(tp.length_is_unknown()))
        else:
            tp_ptr = model.PointerType(tp)
            self._generate_cpy_const(False, name, tp_ptr, category='var')

    _generate_cpy_variable_method = _generate_nothing
    _loading_cpy_variable = _loaded_noop

    def _loaded_cpy_variable(self, tp, name, module, library):
        value = getattr(library, name)
        if isinstance(tp, model.ArrayType):
            if tp.length_is_unknown():
                assert isinstance(value, tuple)
                value, size = value
                BItemType = self.ffi._get_cached_btype(tp.item)
                length, rest = divmod(size, self.ffi.sizeof(BItemType))
                if rest != 0:
                    raise VerificationError('bad size: %r does not seem to be an array of %s' % (
                     name, tp.item))
                tp = tp.resolve_length(length)
            if tp.length is not None:
                BArray = self.ffi._get_cached_btype(tp)
                value = self.ffi.cast(BArray, value)
                setattr(library, name, value)
            return
        ptr = value
        delattr(library, name)

        def getter(library):
            return ptr[0]

        def setter(library, value):
            ptr[0] = value

        setattr(type(library), name, property(getter, setter))
        type(library)._cffi_dir.append(name)

    def _generate_setup_custom(self):
        prnt = self._prnt
        prnt('static int _cffi_setup_custom(PyObject *lib)')
        prnt('{')
        prnt('  return %s;' % self._chained_list_constants[True])
        prnt('}')


cffimod_header = '\n#include <Python.h>\n#include <stddef.h>\n\n/* this block of #ifs should be kept exactly identical between\n   c/_cffi_backend.c, cffi/vengine_cpy.py, cffi/vengine_gen.py\n   and cffi/_cffi_include.h */\n#if defined(_MSC_VER)\n# include <malloc.h>   /* for alloca() */\n# if _MSC_VER < 1600   /* MSVC < 2010 */\n   typedef __int8 int8_t;\n   typedef __int16 int16_t;\n   typedef __int32 int32_t;\n   typedef __int64 int64_t;\n   typedef unsigned __int8 uint8_t;\n   typedef unsigned __int16 uint16_t;\n   typedef unsigned __int32 uint32_t;\n   typedef unsigned __int64 uint64_t;\n   typedef __int8 int_least8_t;\n   typedef __int16 int_least16_t;\n   typedef __int32 int_least32_t;\n   typedef __int64 int_least64_t;\n   typedef unsigned __int8 uint_least8_t;\n   typedef unsigned __int16 uint_least16_t;\n   typedef unsigned __int32 uint_least32_t;\n   typedef unsigned __int64 uint_least64_t;\n   typedef __int8 int_fast8_t;\n   typedef __int16 int_fast16_t;\n   typedef __int32 int_fast32_t;\n   typedef __int64 int_fast64_t;\n   typedef unsigned __int8 uint_fast8_t;\n   typedef unsigned __int16 uint_fast16_t;\n   typedef unsigned __int32 uint_fast32_t;\n   typedef unsigned __int64 uint_fast64_t;\n   typedef __int64 intmax_t;\n   typedef unsigned __int64 uintmax_t;\n# else\n#  include <stdint.h>\n# endif\n# if _MSC_VER < 1800   /* MSVC < 2013 */\n#  ifndef __cplusplus\n    typedef unsigned char _Bool;\n#  endif\n# endif\n#else\n# include <stdint.h>\n# if (defined (__SVR4) && defined (__sun)) || defined(_AIX) || defined(__hpux)\n#  include <alloca.h>\n# endif\n#endif\n\n#if PY_MAJOR_VERSION < 3\n# undef PyCapsule_CheckExact\n# undef PyCapsule_GetPointer\n# define PyCapsule_CheckExact(capsule) (PyCObject_Check(capsule))\n# define PyCapsule_GetPointer(capsule, name) \\\n    (PyCObject_AsVoidPtr(capsule))\n#endif\n\n#if PY_MAJOR_VERSION >= 3\n# define PyInt_FromLong PyLong_FromLong\n#endif\n\n#define _cffi_from_c_double PyFloat_FromDouble\n#define _cffi_from_c_float PyFloat_FromDouble\n#define _cffi_from_c_long PyInt_FromLong\n#define _cffi_from_c_ulong PyLong_FromUnsignedLong\n#define _cffi_from_c_longlong PyLong_FromLongLong\n#define _cffi_from_c_ulonglong PyLong_FromUnsignedLongLong\n#define _cffi_from_c__Bool PyBool_FromLong\n\n#define _cffi_to_c_double PyFloat_AsDouble\n#define _cffi_to_c_float PyFloat_AsDouble\n\n#define _cffi_from_c_int_const(x)                                        \\\n    (((x) > 0) ?                                                         \\\n        ((unsigned long long)(x) <= (unsigned long long)LONG_MAX) ?      \\\n            PyInt_FromLong((long)(x)) :                                  \\\n            PyLong_FromUnsignedLongLong((unsigned long long)(x)) :       \\\n        ((long long)(x) >= (long long)LONG_MIN) ?                        \\\n            PyInt_FromLong((long)(x)) :                                  \\\n            PyLong_FromLongLong((long long)(x)))\n\n#define _cffi_from_c_int(x, type)                                        \\\n    (((type)-1) > 0 ? /* unsigned */                                     \\\n        (sizeof(type) < sizeof(long) ?                                   \\\n            PyInt_FromLong((long)x) :                                    \\\n         sizeof(type) == sizeof(long) ?                                  \\\n            PyLong_FromUnsignedLong((unsigned long)x) :                  \\\n            PyLong_FromUnsignedLongLong((unsigned long long)x)) :        \\\n        (sizeof(type) <= sizeof(long) ?                                  \\\n            PyInt_FromLong((long)x) :                                    \\\n            PyLong_FromLongLong((long long)x)))\n\n#define _cffi_to_c_int(o, type)                                          \\\n    ((type)(                                                             \\\n     sizeof(type) == 1 ? (((type)-1) > 0 ? (type)_cffi_to_c_u8(o)        \\\n                                         : (type)_cffi_to_c_i8(o)) :     \\\n     sizeof(type) == 2 ? (((type)-1) > 0 ? (type)_cffi_to_c_u16(o)       \\\n                                         : (type)_cffi_to_c_i16(o)) :    \\\n     sizeof(type) == 4 ? (((type)-1) > 0 ? (type)_cffi_to_c_u32(o)       \\\n                                         : (type)_cffi_to_c_i32(o)) :    \\\n     sizeof(type) == 8 ? (((type)-1) > 0 ? (type)_cffi_to_c_u64(o)       \\\n                                         : (type)_cffi_to_c_i64(o)) :    \\\n     (Py_FatalError("unsupported size for type " #type), (type)0)))\n\n#define _cffi_to_c_i8                                                    \\\n                 ((int(*)(PyObject *))_cffi_exports[1])\n#define _cffi_to_c_u8                                                    \\\n                 ((int(*)(PyObject *))_cffi_exports[2])\n#define _cffi_to_c_i16                                                   \\\n                 ((int(*)(PyObject *))_cffi_exports[3])\n#define _cffi_to_c_u16                                                   \\\n                 ((int(*)(PyObject *))_cffi_exports[4])\n#define _cffi_to_c_i32                                                   \\\n                 ((int(*)(PyObject *))_cffi_exports[5])\n#define _cffi_to_c_u32                                                   \\\n                 ((unsigned int(*)(PyObject *))_cffi_exports[6])\n#define _cffi_to_c_i64                                                   \\\n                 ((long long(*)(PyObject *))_cffi_exports[7])\n#define _cffi_to_c_u64                                                   \\\n                 ((unsigned long long(*)(PyObject *))_cffi_exports[8])\n#define _cffi_to_c_char                                                  \\\n                 ((int(*)(PyObject *))_cffi_exports[9])\n#define _cffi_from_c_pointer                                             \\\n    ((PyObject *(*)(char *, CTypeDescrObject *))_cffi_exports[10])\n#define _cffi_to_c_pointer                                               \\\n    ((char *(*)(PyObject *, CTypeDescrObject *))_cffi_exports[11])\n#define _cffi_get_struct_layout                                          \\\n    ((PyObject *(*)(Py_ssize_t[]))_cffi_exports[12])\n#define _cffi_restore_errno                                              \\\n    ((void(*)(void))_cffi_exports[13])\n#define _cffi_save_errno                                                 \\\n    ((void(*)(void))_cffi_exports[14])\n#define _cffi_from_c_char                                                \\\n    ((PyObject *(*)(char))_cffi_exports[15])\n#define _cffi_from_c_deref                                               \\\n    ((PyObject *(*)(char *, CTypeDescrObject *))_cffi_exports[16])\n#define _cffi_to_c                                                       \\\n    ((int(*)(char *, CTypeDescrObject *, PyObject *))_cffi_exports[17])\n#define _cffi_from_c_struct                                              \\\n    ((PyObject *(*)(char *, CTypeDescrObject *))_cffi_exports[18])\n#define _cffi_to_c_wchar_t                                               \\\n    ((wchar_t(*)(PyObject *))_cffi_exports[19])\n#define _cffi_from_c_wchar_t                                             \\\n    ((PyObject *(*)(wchar_t))_cffi_exports[20])\n#define _cffi_to_c_long_double                                           \\\n    ((long double(*)(PyObject *))_cffi_exports[21])\n#define _cffi_to_c__Bool                                                 \\\n    ((_Bool(*)(PyObject *))_cffi_exports[22])\n#define _cffi_prepare_pointer_call_argument                              \\\n    ((Py_ssize_t(*)(CTypeDescrObject *, PyObject *, char **))_cffi_exports[23])\n#define _cffi_convert_array_from_object                                  \\\n    ((int(*)(char *, CTypeDescrObject *, PyObject *))_cffi_exports[24])\n#define _CFFI_NUM_EXPORTS 25\n\ntypedef struct _ctypedescr CTypeDescrObject;\n\nstatic void *_cffi_exports[_CFFI_NUM_EXPORTS];\nstatic PyObject *_cffi_types, *_cffi_VerificationError;\n\nstatic int _cffi_setup_custom(PyObject *lib);   /* forward */\n\nstatic PyObject *_cffi_setup(PyObject *self, PyObject *args)\n{\n    PyObject *library;\n    int was_alive = (_cffi_types != NULL);\n    (void)self; /* unused */\n    if (!PyArg_ParseTuple(args, "OOO", &_cffi_types, &_cffi_VerificationError,\n                                       &library))\n        return NULL;\n    Py_INCREF(_cffi_types);\n    Py_INCREF(_cffi_VerificationError);\n    if (_cffi_setup_custom(library) < 0)\n        return NULL;\n    return PyBool_FromLong(was_alive);\n}\n\nunion _cffi_union_alignment_u {\n    unsigned char m_char;\n    unsigned short m_short;\n    unsigned int m_int;\n    unsigned long m_long;\n    unsigned long long m_longlong;\n    float m_float;\n    double m_double;\n    long double m_longdouble;\n};\n\nstruct _cffi_freeme_s {\n    struct _cffi_freeme_s *next;\n    union _cffi_union_alignment_u alignment;\n};\n\n#ifdef __GNUC__\n  __attribute__((unused))\n#endif\nstatic int _cffi_convert_array_argument(CTypeDescrObject *ctptr, PyObject *arg,\n                                        char **output_data, Py_ssize_t datasize,\n                                        struct _cffi_freeme_s **freeme)\n{\n    char *p;\n    if (datasize < 0)\n        return -1;\n\n    p = *output_data;\n    if (p == NULL) {\n        struct _cffi_freeme_s *fp = (struct _cffi_freeme_s *)PyObject_Malloc(\n            offsetof(struct _cffi_freeme_s, alignment) + (size_t)datasize);\n        if (fp == NULL)\n            return -1;\n        fp->next = *freeme;\n        *freeme = fp;\n        p = *output_data = (char *)&fp->alignment;\n    }\n    memset((void *)p, 0, (size_t)datasize);\n    return _cffi_convert_array_from_object(p, ctptr, arg);\n}\n\n#ifdef __GNUC__\n  __attribute__((unused))\n#endif\nstatic void _cffi_free_array_arguments(struct _cffi_freeme_s *freeme)\n{\n    do {\n        void *p = (void *)freeme;\n        freeme = freeme->next;\n        PyObject_Free(p);\n    } while (freeme != NULL);\n}\n\nstatic int _cffi_init(void)\n{\n    PyObject *module, *c_api_object = NULL;\n\n    module = PyImport_ImportModule("_cffi_backend");\n    if (module == NULL)\n        goto failure;\n\n    c_api_object = PyObject_GetAttrString(module, "_C_API");\n    if (c_api_object == NULL)\n        goto failure;\n    if (!PyCapsule_CheckExact(c_api_object)) {\n        PyErr_SetNone(PyExc_ImportError);\n        goto failure;\n    }\n    memcpy(_cffi_exports, PyCapsule_GetPointer(c_api_object, "cffi"),\n           _CFFI_NUM_EXPORTS * sizeof(void *));\n\n    Py_DECREF(module);\n    Py_DECREF(c_api_object);\n    return 0;\n\n  failure:\n    Py_XDECREF(module);\n    Py_XDECREF(c_api_object);\n    return -1;\n}\n\n#define _cffi_type(num) ((CTypeDescrObject *)PyList_GET_ITEM(_cffi_types, num))\n\n/**********/\n'