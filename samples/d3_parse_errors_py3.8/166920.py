# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: comtypes\client\_generate.py
import types, os, sys, comtypes.client, comtypes.tools.codegenerator, logging
logger = logging.getLogger(__name__)
if os.name == 'ce':
    PATH = [
     '\\Windows', '\\']
else:
    PATH = os.environ['PATH'].split(os.pathsep)

def _my_import(fullname):
    import comtypes.gen
    if comtypes.client.gen_dir:
        if comtypes.client.gen_dir not in comtypes.gen.__path__:
            comtypes.gen.__path__.append(comtypes.client.gen_dir)
    return __import__(fullname, globals(), locals(), ['DUMMY'])


def _name_module(tlib):
    libattr = tlib.GetLibAttr()
    modname = '_%s_%s_%s_%s' % (
     str(libattr.guid)[1:-1].replace('-', '_'),
     libattr.lcid,
     libattr.wMajorVerNum,
     libattr.wMinorVerNum)
    return 'comtypes.gen.' + modname


def GetModule(tlib):
    r"""Create a module wrapping a COM typelibrary on demand.

    'tlib' must be an ITypeLib COM pointer instance, the pathname of a
    type library, or a tuple/list specifying the arguments to a
    comtypes.typeinfo.LoadRegTypeLib call:

      (libid, wMajorVerNum, wMinorVerNum, lcid=0)

    Or it can be an object with _reg_libid_ and _reg_version_
    attributes.

    A relative pathname is interpreted as relative to the callers
    __file__, if this exists.

    This function determines the module name from the typelib
    attributes, then tries to import it.  If that fails because the
    module doesn't exist, the module is generated into the
    comtypes.gen package.

    It is possible to delete the whole comtypes\gen directory to
    remove all generated modules, the directory and the __init__.py
    file in it will be recreated when needed.

    If comtypes.gen __path__ is not a directory (in a frozen
    executable it lives in a zip archive), generated modules are only
    created in memory without writing them to the file system.

    Example:

        GetModule("shdocvw.dll")

    would create modules named

       comtypes.gen._EAB22AC0_30C1_11CF_A7EB_0000C05BAE0B_0_1_1
       comtypes.gen.SHDocVw

    containing the Python wrapper code for the type library used by
    Internet Explorer.  The former module contains all the code, the
    latter is a short stub loading the former.
    """
    pathname = None
    if isinstance(tlib, str):
        if not os.path.isabs(tlib):
            frame = sys._getframe(1)
            _file_ = frame.f_globals.get('__file__', None)
            if _file_ is not None:
                directory = os.path.dirname(os.path.abspath(_file_))
                abspath = os.path.normpath(os.path.join(directory, tlib))
                if os.path.isfile(abspath):
                    tlib = abspath
        logger.debug('GetModule(%s)', tlib)
        pathname = tlib
        tlib = comtypes.typeinfo.LoadTypeLibEx(tlib)
    elif isinstance(tlib, (tuple, list)):
        logger.debug('GetModule(%s)', (tlib,))
        tlib = (comtypes.typeinfo.LoadRegTypeLib)(comtypes.GUID(tlib[0]), *tlib[1:])
    elif hasattr(tlib, '_reg_libid_'):
        logger.debug('GetModule(%s)', tlib)
        tlib = (comtypes.typeinfo.LoadRegTypeLib)(comtypes.GUID(tlib._reg_libid_), *tlib._reg_version_)
    else:
        logger.debug('GetModule(%s)', tlib.GetLibAttr())
    mod = _CreateWrapper(tlib, pathname)
    try:
        modulename = tlib.GetDocumentation(-1)[0]
    except comtypes.COMError:
        return mod
    else:
        if modulename is None:
            return mod
        else:
            if sys.version_info < (3, 0):
                modulename = modulename.encode('mbcs')
            try:
                mod = _my_import('comtypes.gen.' + modulename)
            except Exception as details:
                try:
                    logger.info('Could not import comtypes.gen.%s: %s', modulename, details)
                finally:
                    details = None
                    del details

            else:
                return mod
            logger.info('# Generating comtypes.gen.%s', modulename)
            fullname = _name_module(tlib)
            modname = fullname.split('.')[(-1)]
            code = 'from comtypes.gen import %s\nglobals().update(%s.__dict__)\n' % (modname, modname)
            code += "__name__ = 'comtypes.gen.%s'" % modulename
            if comtypes.client.gen_dir is None:
                mod = types.ModuleType('comtypes.gen.' + modulename)
                mod.__file__ = os.path.join(os.path.abspath(comtypes.gen.__path__[0]), '<memory>')
                exec(code, mod.__dict__)
                sys.modules['comtypes.gen.' + modulename] = mod
                setattr(comtypes.gen, modulename, mod)
                return mod
            ofi = open(os.path.join(comtypes.client.gen_dir, modulename + '.py'), 'w')
            ofi.write(code)
            ofi.close()
            return _my_import('comtypes.gen.' + modulename)


def _CreateWrapper--- This code section failed: ---

 L. 150         0  LOAD_GLOBAL              _name_module
                2  LOAD_FAST                'tlib'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'fullname'

 L. 151         8  SETUP_FINALLY        22  'to 22'

 L. 152        10  LOAD_GLOBAL              sys
               12  LOAD_ATTR                modules
               14  LOAD_FAST                'fullname'
               16  BINARY_SUBSCR    
               18  POP_BLOCK        
               20  RETURN_VALUE     
             22_0  COME_FROM_FINALLY     8  '8'

 L. 153        22  DUP_TOP          
               24  LOAD_GLOBAL              KeyError
               26  COMPARE_OP               exception-match
               28  POP_JUMP_IF_FALSE    40  'to 40'
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L. 154        36  POP_EXCEPT       
               38  JUMP_FORWARD         42  'to 42'
             40_0  COME_FROM            28  '28'
               40  END_FINALLY      
             42_0  COME_FROM            38  '38'

 L. 156        42  LOAD_FAST                'fullname'
               44  LOAD_METHOD              split
               46  LOAD_STR                 '.'
               48  CALL_METHOD_1         1  ''
               50  LOAD_CONST               -1
               52  BINARY_SUBSCR    
               54  STORE_FAST               'modname'

 L. 158        56  SETUP_FINALLY        68  'to 68'

 L. 159        58  LOAD_GLOBAL              _my_import
               60  LOAD_FAST                'fullname'
               62  CALL_FUNCTION_1       1  ''
               64  POP_BLOCK        
               66  RETURN_VALUE     
             68_0  COME_FROM_FINALLY    56  '56'

 L. 160        68  DUP_TOP          
               70  LOAD_GLOBAL              Exception
               72  COMPARE_OP               exception-match
               74  POP_JUMP_IF_FALSE   114  'to 114'
               76  POP_TOP          
               78  STORE_FAST               'details'
               80  POP_TOP          
               82  SETUP_FINALLY       102  'to 102'

 L. 161        84  LOAD_GLOBAL              logger
               86  LOAD_METHOD              info
               88  LOAD_STR                 'Could not import %s: %s'
               90  LOAD_FAST                'fullname'
               92  LOAD_FAST                'details'
               94  CALL_METHOD_3         3  ''
               96  POP_TOP          
               98  POP_BLOCK        
              100  BEGIN_FINALLY    
            102_0  COME_FROM_FINALLY    82  '82'
              102  LOAD_CONST               None
              104  STORE_FAST               'details'
              106  DELETE_FAST              'details'
              108  END_FINALLY      
              110  POP_EXCEPT       
              112  JUMP_FORWARD        116  'to 116'
            114_0  COME_FROM            74  '74'
              114  END_FINALLY      
            116_0  COME_FROM           112  '112'

 L. 164       116  LOAD_CONST               0
              118  LOAD_CONST               ('generate_module',)
              120  IMPORT_NAME_ATTR         comtypes.tools.tlbparser
              122  IMPORT_FROM              generate_module
              124  STORE_FAST               'generate_module'
              126  POP_TOP          

 L. 165       128  LOAD_GLOBAL              comtypes
              130  LOAD_ATTR                client
              132  LOAD_ATTR                gen_dir
              134  LOAD_CONST               None
              136  COMPARE_OP               is
              138  POP_JUMP_IF_FALSE   158  'to 158'

 L. 166       140  LOAD_CONST               0
              142  LOAD_CONST               None
              144  IMPORT_NAME              io
              146  STORE_FAST               'io'

 L. 167       148  LOAD_FAST                'io'
              150  LOAD_METHOD              StringIO
              152  CALL_METHOD_0         0  ''
              154  STORE_FAST               'ofi'
              156  JUMP_FORWARD        186  'to 186'
            158_0  COME_FROM           138  '138'

 L. 169       158  LOAD_GLOBAL              open
              160  LOAD_GLOBAL              os
              162  LOAD_ATTR                path
              164  LOAD_METHOD              join
              166  LOAD_GLOBAL              comtypes
              168  LOAD_ATTR                client
              170  LOAD_ATTR                gen_dir
              172  LOAD_FAST                'modname'
              174  LOAD_STR                 '.py'
              176  BINARY_ADD       
              178  CALL_METHOD_2         2  ''
              180  LOAD_STR                 'w'
              182  CALL_FUNCTION_2       2  ''
              184  STORE_FAST               'ofi'
            186_0  COME_FROM           156  '156'

 L. 171       186  LOAD_GLOBAL              logger
              188  LOAD_METHOD              info
              190  LOAD_STR                 '# Generating comtypes.gen.%s'
              192  LOAD_FAST                'modname'
              194  CALL_METHOD_2         2  ''
              196  POP_TOP          

 L. 172       198  LOAD_FAST                'generate_module'
              200  LOAD_FAST                'tlib'
              202  LOAD_FAST                'ofi'
              204  LOAD_FAST                'pathname'
              206  CALL_FUNCTION_3       3  ''
              208  POP_TOP          

 L. 174       210  LOAD_GLOBAL              comtypes
              212  LOAD_ATTR                client
              214  LOAD_ATTR                gen_dir
              216  LOAD_CONST               None
              218  COMPARE_OP               is
          220_222  POP_JUMP_IF_FALSE   312  'to 312'

 L. 175       224  LOAD_FAST                'ofi'
              226  LOAD_METHOD              getvalue
              228  CALL_METHOD_0         0  ''
              230  STORE_FAST               'code'

 L. 176       232  LOAD_GLOBAL              types
              234  LOAD_METHOD              ModuleType
              236  LOAD_FAST                'fullname'
              238  CALL_METHOD_1         1  ''
              240  STORE_FAST               'mod'

 L. 177       242  LOAD_GLOBAL              os
              244  LOAD_ATTR                path
              246  LOAD_METHOD              join
              248  LOAD_GLOBAL              os
              250  LOAD_ATTR                path
              252  LOAD_METHOD              abspath
              254  LOAD_GLOBAL              comtypes
              256  LOAD_ATTR                gen
              258  LOAD_ATTR                __path__
              260  LOAD_CONST               0
              262  BINARY_SUBSCR    
              264  CALL_METHOD_1         1  ''

 L. 178       266  LOAD_STR                 '<memory>'

 L. 177       268  CALL_METHOD_2         2  ''
              270  LOAD_FAST                'mod'
              272  STORE_ATTR               __file__

 L. 179       274  LOAD_GLOBAL              exec
              276  LOAD_FAST                'code'
              278  LOAD_FAST                'mod'
              280  LOAD_ATTR                __dict__
              282  CALL_FUNCTION_2       2  ''
              284  POP_TOP          

 L. 180       286  LOAD_FAST                'mod'
              288  LOAD_GLOBAL              sys
              290  LOAD_ATTR                modules
              292  LOAD_FAST                'fullname'
              294  STORE_SUBSCR     

 L. 181       296  LOAD_GLOBAL              setattr
              298  LOAD_GLOBAL              comtypes
              300  LOAD_ATTR                gen
              302  LOAD_FAST                'modname'
              304  LOAD_FAST                'mod'
              306  CALL_FUNCTION_3       3  ''
              308  POP_TOP          
              310  JUMP_FORWARD        328  'to 328'
            312_0  COME_FROM           220  '220'

 L. 183       312  LOAD_FAST                'ofi'
              314  LOAD_METHOD              close
              316  CALL_METHOD_0         0  ''
              318  POP_TOP          

 L. 184       320  LOAD_GLOBAL              _my_import
              322  LOAD_FAST                'fullname'
              324  CALL_FUNCTION_1       1  ''
              326  STORE_FAST               'mod'
            328_0  COME_FROM           310  '310'

 L. 185       328  LOAD_FAST                'mod'
              330  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 40_0


if __name__ == '__main__':
    GetModule(sys.argv[1])