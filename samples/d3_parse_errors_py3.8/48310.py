# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\comtypes\npsupport.py
""" Consolidation of numpy support utilities. """
import sys
try:
    import numpy
except ImportError:
    numpy = None
else:
    HAVE_NUMPY = numpy is not None
    is_64bits = sys.maxsize > 4294967296

    def _make_variant_dtype():
        """ Create a dtype for VARIANT. This requires support for Unions, which is
    available in numpy version 1.7 or greater.

    This does not support the decimal type.

    Returns None if the dtype cannot be created.

    """
        ptr_typecode = '<u8' if is_64bits else '<u4'
        _tagBRECORD_format = [
         (
          'pvRecord', ptr_typecode),
         (
          'pRecInfo', ptr_typecode)]
        U_VARIANT_format = dict(names=[
         'VT_BOOL', 'VT_I1', 'VT_I2', 'VT_I4', 'VT_I8', 'VT_INT', 'VT_UI1',
         'VT_UI2', 'VT_UI4', 'VT_UI8', 'VT_UINT', 'VT_R4', 'VT_R8', 'VT_CY',
         'c_wchar_p', 'c_void_p', 'pparray', 'bstrVal', '_tagBRECORD'],
          formats=[
         '<i2', '<i1', '<i2', '<i4', '<i8', '<i4', '<u1', '<u2', '<u4',
         '<u8', '<u4', '<f4', '<f8', '<i8', ptr_typecode, ptr_typecode,
         ptr_typecode, ptr_typecode, _tagBRECORD_format],
          offsets=([
         0] * 19))
        tagVARIANT_format = [
         ('vt', '<u2'),
         ('wReserved1', '<u2'),
         ('wReserved2', '<u2'),
         ('wReserved3', '<u2'),
         (
          '_', U_VARIANT_format)]
        return numpy.dtype(tagVARIANT_format)


    def isndarray(value):
        """ Check if a value is an ndarray.

    This cannot succeed if numpy is not available.

    """
        if not HAVE_NUMPY:
            return False
        return isinstance(value, numpy.ndarray)


    def isdatetime64(value):
        """ Check if a value is a datetime64.

    This cannot succeed if datetime64 is not available.

    """
        if not HAVE_NUMPY:
            return False
        return isinstance(value, datetime64)


    def _check_ctypeslib_typecodes--- This code section failed: ---

 L.  82         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              numpy
                6  STORE_FAST               'np'

 L.  83         8  LOAD_CONST               0
               10  LOAD_CONST               ('ctypeslib',)
               12  IMPORT_NAME              numpy
               14  IMPORT_FROM              ctypeslib
               16  STORE_FAST               'ctypeslib'
               18  POP_TOP          

 L.  84        20  SETUP_FINALLY        38  'to 38'

 L.  85        22  LOAD_CONST               0
               24  LOAD_CONST               ('_typecodes',)
               26  IMPORT_NAME_ATTR         numpy.ctypeslib
               28  IMPORT_FROM              _typecodes
               30  STORE_FAST               '_typecodes'
               32  POP_TOP          
               34  POP_BLOCK        
               36  JUMP_FORWARD        146  'to 146'
             38_0  COME_FROM_FINALLY    20  '20'

 L.  86        38  DUP_TOP          
               40  LOAD_GLOBAL              ImportError
               42  COMPARE_OP               exception-match
               44  POP_JUMP_IF_FALSE   144  'to 144'
               46  POP_TOP          
               48  POP_TOP          
               50  POP_TOP          

 L.  87        52  LOAD_CONST               0
               54  LOAD_CONST               ('as_ctypes_type',)
               56  IMPORT_NAME_ATTR         numpy.ctypeslib
               58  IMPORT_FROM              as_ctypes_type
               60  STORE_FAST               'as_ctypes_type'
               62  POP_TOP          

 L.  89        64  BUILD_MAP_0           0 
               66  STORE_FAST               'ctypes_to_dtypes'

 L.  91        68  LOAD_GLOBAL              set
               70  LOAD_FAST                'np'
               72  LOAD_ATTR                sctypeDict
               74  LOAD_METHOD              values
               76  CALL_METHOD_0         0  ''
               78  CALL_FUNCTION_1       1  ''
               80  GET_ITER         
             82_0  COME_FROM           132  '132'
             82_1  COME_FROM           128  '128'
             82_2  COME_FROM           124  '124'
             82_3  COME_FROM           106  '106'
               82  FOR_ITER            134  'to 134'
               84  STORE_FAST               'tp'

 L.  92        86  SETUP_FINALLY       108  'to 108'

 L.  93        88  LOAD_FAST                'as_ctypes_type'
               90  LOAD_FAST                'tp'
               92  CALL_FUNCTION_1       1  ''
               94  STORE_FAST               'ctype_for'

 L.  94        96  LOAD_FAST                'tp'
               98  LOAD_FAST                'ctypes_to_dtypes'
              100  LOAD_FAST                'ctype_for'
              102  STORE_SUBSCR     
              104  POP_BLOCK        
              106  JUMP_BACK            82  'to 82'
            108_0  COME_FROM_FINALLY    86  '86'

 L.  95       108  DUP_TOP          
              110  LOAD_GLOBAL              NotImplementedError
              112  COMPARE_OP               exception-match
              114  POP_JUMP_IF_FALSE   130  'to 130'
              116  POP_TOP          
              118  POP_TOP          
              120  POP_TOP          

 L.  96       122  POP_EXCEPT       
              124  JUMP_BACK            82  'to 82'
              126  POP_EXCEPT       
              128  JUMP_BACK            82  'to 82'
            130_0  COME_FROM           114  '114'
              130  END_FINALLY      
              132  JUMP_BACK            82  'to 82'
            134_0  COME_FROM            82  '82'

 L.  97       134  LOAD_FAST                'ctypes_to_dtypes'
              136  LOAD_FAST                'ctypeslib'
              138  STORE_ATTR               _typecodes
              140  POP_EXCEPT       
              142  JUMP_FORWARD        146  'to 146'
            144_0  COME_FROM            44  '44'
              144  END_FINALLY      
            146_0  COME_FROM           142  '142'
            146_1  COME_FROM            36  '36'

 L.  98       146  LOAD_FAST                'ctypeslib'
              148  LOAD_ATTR                _typecodes
              150  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 128


    com_null_date64 = None
    datetime64 = None
    VARIANT_dtype = None
    typecodes = {}
    if HAVE_NUMPY:
        typecodes = _check_ctypeslib_typecodes()
        try:
            VARIANT_dtype = _make_variant_dtype()
        except ValueError:
            pass

        try:
            from numpy import datetime64
        except ImportError:
            pass

        try:
            com_null_date64 = datetime64('1899-12-30T00:00:00', 'ns')
        except TypeError:
            pass