# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\win32com\client\gencache.py
"""Manages the cache of generated Python code.

Description
  This file manages the cache of generated Python code.  When run from the 
  command line, it also provides a number of options for managing that cache.
  
Implementation
  Each typelib is generated into a filename of format "{guid}x{lcid}x{major}x{minor}.py"
  
  An external persistant dictionary maps from all known IIDs in all known type libraries
  to the type library itself.
  
  Thus, whenever Python code knows the IID of an object, it can find the IID, LCID and version of
  the type library which supports it.  Given this information, it can find the Python module
  with the support.
  
  If necessary, this support can be generated on the fly.
  
Hacks, to do, etc
  Currently just uses a pickled dictionary, but should used some sort of indexed file.
  Maybe an OLE2 compound file, or a bsddb file?
"""
import pywintypes, os, sys, pythoncom, win32com, win32com.client, glob, traceback
from . import CLSIDToClass
import operator
try:
    from imp import reload
except:
    pass
else:
    bForDemandDefault = 0
    clsidToTypelib = {}
    versionRedirectMap = {}
    is_readonly = is_zip = hasattr(win32com, '__loader__') and hasattr(win32com.__loader__, 'archive')
    demandGeneratedTypeLibraries = {}
    import pickle

    def __init__():
        try:
            _LoadDicts()
        except IOError:
            Rebuild()


    pickleVersion = 1

    def _SaveDicts():
        global clsidToTypelib
        if is_readonly:
            raise RuntimeError("Trying to write to a readonly gencache ('%s')!" % win32com.__gen_path__)
        f = open(os.path.join(GetGeneratePath(), 'dicts.dat'), 'wb')
        try:
            p = pickle.Pickler(f)
            p.dump(pickleVersion)
            p.dump(clsidToTypelib)
        finally:
            f.close()


    def _LoadDicts():
        global clsidToTypelib
        if is_zip:
            import io
            loader = win32com.__loader__
            arc_path = loader.archive
            dicts_path = os.path.join(win32com.__gen_path__, 'dicts.dat')
            if dicts_path.startswith(arc_path):
                dicts_path = dicts_path[len(arc_path) + 1:]
            else:
                return
                try:
                    data = loader.get_data(dicts_path)
                except AttributeError:
                    return
                except IOError:
                    return
                else:
                    f = io.BytesIO(data)
        else:
            f = open(os.path.join(win32com.__gen_path__, 'dicts.dat'), 'rb')
        try:
            p = pickle.Unpickler(f)
            version = p.load()
            clsidToTypelib = p.load()
            versionRedirectMap.clear()
        finally:
            f.close()


    def GetGeneratedFileName(clsid, lcid, major, minor):
        """Given the clsid, lcid, major and  minor for a type lib, return
        the file name (no extension) providing this support.
        """
        return str(clsid).upper()[1:-1] + 'x%sx%sx%s' % (lcid, major, minor)


    def SplitGeneratedFileName(fname):
        """Reverse of GetGeneratedFileName()
        """
        return tuple(fname.split('x', 4))


    def GetGeneratePath():
        """Returns the name of the path to generate to.
        Checks the directory is OK.
        """
        if is_readonly:
            raise AssertionError('Why do you want the genpath for a readonly store?')
        try:
            os.makedirs(win32com.__gen_path__)
        except os.error:
            pass
        else:
            try:
                fname = os.path.join(win32com.__gen_path__, '__init__.py')
                os.stat(fname)
            except os.error:
                f = open(fname, 'w')
                f.write('# Generated file - this directory may be deleted to reset the COM cache...\n')
                f.write('import win32com\n')
                f.write('if __path__[:-1] != win32com.__gen_path__: __path__.append(win32com.__gen_path__)\n')
                f.close()
            else:
                return win32com.__gen_path__


    def GetClassForProgID(progid):
        """Get a Python class for a Program ID
        
        Given a Program ID, return a Python class which wraps the COM object
        
        Returns the Python class, or None if no module is available.
        
        Params
        progid -- A COM ProgramID or IID (eg, "Word.Application")
        """
        clsid = pywintypes.IID(progid)
        return GetClassForCLSID(clsid)


    def GetClassForCLSID--- This code section failed: ---

 L. 180         0  LOAD_GLOBAL              str
                2  LOAD_FAST                'clsid'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'clsid'

 L. 181         8  LOAD_GLOBAL              CLSIDToClass
               10  LOAD_METHOD              HasClass
               12  LOAD_FAST                'clsid'
               14  CALL_METHOD_1         1  ''
               16  POP_JUMP_IF_FALSE    28  'to 28'

 L. 182        18  LOAD_GLOBAL              CLSIDToClass
               20  LOAD_METHOD              GetClass
               22  LOAD_FAST                'clsid'
               24  CALL_METHOD_1         1  ''
               26  RETURN_VALUE     
             28_0  COME_FROM            16  '16'

 L. 183        28  LOAD_GLOBAL              GetModuleForCLSID
               30  LOAD_FAST                'clsid'
               32  CALL_FUNCTION_1       1  ''
               34  STORE_FAST               'mod'

 L. 184        36  LOAD_FAST                'mod'
               38  LOAD_CONST               None
               40  COMPARE_OP               is
               42  POP_JUMP_IF_FALSE    48  'to 48'

 L. 185        44  LOAD_CONST               None
               46  RETURN_VALUE     
             48_0  COME_FROM            42  '42'

 L. 186        48  SETUP_FINALLY        62  'to 62'

 L. 187        50  LOAD_GLOBAL              CLSIDToClass
               52  LOAD_METHOD              GetClass
               54  LOAD_FAST                'clsid'
               56  CALL_METHOD_1         1  ''
               58  POP_BLOCK        
               60  RETURN_VALUE     
             62_0  COME_FROM_FINALLY    48  '48'

 L. 188        62  DUP_TOP          
               64  LOAD_GLOBAL              KeyError
               66  COMPARE_OP               exception-match
               68  POP_JUMP_IF_FALSE    82  'to 82'
               70  POP_TOP          
               72  POP_TOP          
               74  POP_TOP          

 L. 189        76  POP_EXCEPT       
               78  LOAD_CONST               None
               80  RETURN_VALUE     
             82_0  COME_FROM            68  '68'
               82  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 72


    def GetModuleForProgID(progid):
        """Get a Python module for a Program ID
        
        Given a Program ID, return a Python module which contains the
        class which wraps the COM object.
        
        Returns the Python module, or None if no module is available.
        
        Params
        progid -- A COM ProgramID or IID (eg, "Word.Application")
        """
        try:
            iid = pywintypes.IID(progid)
        except pywintypes.com_error:
            return
        else:
            return GetModuleForCLSID(iid)


    def GetModuleForCLSID(clsid):
        """Get a Python module for a CLSID
        
        Given a CLSID, return a Python module which contains the
        class which wraps the COM object.
        
        Returns the Python module, or None if no module is available.
        
        Params
        progid -- A COM CLSID (ie, not the description)
        """
        clsid_str = str(clsid)
        try:
            typelibCLSID, lcid, major, minor = clsidToTypelib[clsid_str]
        except KeyError:
            return
        else:
            try:
                mod = GetModuleForTypelib(typelibCLSID, lcid, major, minor)
            except ImportError:
                mod = None
            else:
                if mod is not None:
                    sub_mod = mod.CLSIDToPackageMap.get(clsid_str)
                    if sub_mod is None:
                        sub_mod = mod.VTablesToPackageMap.get(clsid_str)
                    if sub_mod is not None:
                        sub_mod_name = mod.__name__ + '.' + sub_mod
                        try:
                            __import__(sub_mod_name)
                        except ImportError:
                            info = (
                             typelibCLSID, lcid, major, minor)
                            if info in demandGeneratedTypeLibraries:
                                info = demandGeneratedTypeLibraries[info]
                            from . import makepy
                            makepy.GenerateChildFromTypeLibSpec(sub_mod, info)
                        else:
                            mod = sys.modules[sub_mod_name]
                return mod


    def GetModuleForTypelib(typelibCLSID, lcid, major, minor):
        """Get a Python module for a type library ID
        
        Given the CLSID of a typelibrary, return an imported Python module, 
        else None
        
        Params
        typelibCLSID -- IID of the type library.
        major -- Integer major version.
        minor -- Integer minor version
        lcid -- Integer LCID for the library.
        """
        modName = GetGeneratedFileName(typelibCLSID, lcid, major, minor)
        mod = _GetModule(modName)
        if '_in_gencache_' not in mod.__dict__:
            AddModuleToCache(typelibCLSID, lcid, major, minor)
            assert '_in_gencache_' in mod.__dict__
        return mod


    def MakeModuleForTypelib(typelibCLSID, lcid, major, minor, progressInstance=None, bForDemand=bForDemandDefault, bBuildHidden=1):
        """Generate support for a type library.
        
        Given the IID, LCID and version information for a type library, generate
        and import the necessary support files.
        
        Returns the Python module.  No exceptions are caught.

        Params
        typelibCLSID -- IID of the type library.
        major -- Integer major version.
        minor -- Integer minor version.
        lcid -- Integer LCID for the library.
        progressInstance -- Instance to use as progress indicator, or None to
                            use the GUI progress bar.
        """
        from . import makepy
        makepy.GenerateFromTypeLibSpec((typelibCLSID, lcid, major, minor), progressInstance=progressInstance, bForDemand=bForDemand, bBuildHidden=bBuildHidden)
        return GetModuleForTypelib(typelibCLSID, lcid, major, minor)


    def MakeModuleForTypelibInterface(typelib_ob, progressInstance=None, bForDemand=bForDemandDefault, bBuildHidden=1):
        """Generate support for a type library.
        
        Given a PyITypeLib interface generate and import the necessary support files.  This is useful
        for getting makepy support for a typelibrary that is not registered - the caller can locate
        and load the type library itself, rather than relying on COM to find it.
        
        Returns the Python module.

        Params
        typelib_ob -- The type library itself
        progressInstance -- Instance to use as progress indicator, or None to
                            use the GUI progress bar.
        """
        from . import makepy
        try:
            makepy.GenerateFromTypeLibSpec(typelib_ob, progressInstance=progressInstance, bForDemand=bForDemandDefault, bBuildHidden=bBuildHidden)
        except pywintypes.com_error:
            return
        else:
            tla = typelib_ob.GetLibAttr()
            guid = tla[0]
            lcid = tla[1]
            major = tla[3]
            minor = tla[4]
            return GetModuleForTypelib(guid, lcid, major, minor)


    def EnsureModuleForTypelibInterface--- This code section failed: ---

 L. 331         0  LOAD_FAST                'typelib_ob'
                2  LOAD_METHOD              GetLibAttr
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'tla'

 L. 332         8  LOAD_FAST                'tla'
               10  LOAD_CONST               0
               12  BINARY_SUBSCR    
               14  STORE_FAST               'guid'

 L. 333        16  LOAD_FAST                'tla'
               18  LOAD_CONST               1
               20  BINARY_SUBSCR    
               22  STORE_FAST               'lcid'

 L. 334        24  LOAD_FAST                'tla'
               26  LOAD_CONST               3
               28  BINARY_SUBSCR    
               30  STORE_FAST               'major'

 L. 335        32  LOAD_FAST                'tla'
               34  LOAD_CONST               4
               36  BINARY_SUBSCR    
               38  STORE_FAST               'minor'

 L. 338        40  LOAD_FAST                'bForDemand'
               42  POP_JUMP_IF_FALSE    64  'to 64'

 L. 339        44  LOAD_FAST                'typelib_ob'
               46  LOAD_GLOBAL              demandGeneratedTypeLibraries
               48  LOAD_GLOBAL              str
               50  LOAD_FAST                'guid'
               52  CALL_FUNCTION_1       1  ''
               54  LOAD_FAST                'lcid'
               56  LOAD_FAST                'major'
               58  LOAD_FAST                'minor'
               60  BUILD_TUPLE_4         4 
               62  STORE_SUBSCR     
             64_0  COME_FROM            42  '42'

 L. 341        64  SETUP_FINALLY        82  'to 82'

 L. 342        66  LOAD_GLOBAL              GetModuleForTypelib
               68  LOAD_FAST                'guid'
               70  LOAD_FAST                'lcid'
               72  LOAD_FAST                'major'
               74  LOAD_FAST                'minor'
               76  CALL_FUNCTION_4       4  ''
               78  POP_BLOCK        
               80  RETURN_VALUE     
             82_0  COME_FROM_FINALLY    64  '64'

 L. 343        82  DUP_TOP          
               84  LOAD_GLOBAL              ImportError
               86  COMPARE_OP               exception-match
               88  POP_JUMP_IF_FALSE   100  'to 100'
               90  POP_TOP          
               92  POP_TOP          
               94  POP_TOP          

 L. 344        96  POP_EXCEPT       
               98  JUMP_FORWARD        102  'to 102'
            100_0  COME_FROM            88  '88'
              100  END_FINALLY      
            102_0  COME_FROM            98  '98'

 L. 346       102  LOAD_GLOBAL              MakeModuleForTypelibInterface
              104  LOAD_FAST                'typelib_ob'
              106  LOAD_FAST                'progressInstance'
              108  LOAD_FAST                'bForDemand'
              110  LOAD_FAST                'bBuildHidden'
              112  CALL_FUNCTION_4       4  ''
              114  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 92


    def ForgetAboutTypelibInterface(typelib_ob):
        """Drop any references to a typelib previously added with EnsureModuleForTypelibInterface and forDemand"""
        tla = typelib_ob.GetLibAttr()
        guid = tla[0]
        lcid = tla[1]
        major = tla[3]
        minor = tla[4]
        info = (str(guid), lcid, major, minor)
        try:
            del demandGeneratedTypeLibraries[info]
        except KeyError:
            print('ForgetAboutTypelibInterface:: Warning - type library with info %s is not being remembered!' % (info,))
        else:
            for key, val in list(versionRedirectMap.items()):
                if val == info:
                    del versionRedirectMap[key]


    def EnsureModule--- This code section failed: ---

 L. 388         0  LOAD_CONST               0
                2  STORE_FAST               'bReloadNeeded'

 L. 389       4_6  SETUP_FINALLY       842  'to 842'

 L. 390         8  SETUP_FINALLY        28  'to 28'

 L. 391        10  LOAD_GLOBAL              GetModuleForTypelib
               12  LOAD_FAST                'typelibCLSID'
               14  LOAD_FAST                'lcid'
               16  LOAD_FAST                'major'
               18  LOAD_FAST                'minor'
               20  CALL_FUNCTION_4       4  ''
               22  STORE_FAST               'module'
               24  POP_BLOCK        
               26  JUMP_FORWARD        184  'to 184'
             28_0  COME_FROM_FINALLY     8  '8'

 L. 392        28  DUP_TOP          
               30  LOAD_GLOBAL              ImportError
               32  COMPARE_OP               exception-match
               34  POP_JUMP_IF_FALSE   182  'to 182'
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 397        42  LOAD_CONST               None
               44  STORE_FAST               'module'

 L. 398        46  SETUP_FINALLY       156  'to 156'

 L. 399        48  LOAD_GLOBAL              pythoncom
               50  LOAD_METHOD              LoadRegTypeLib
               52  LOAD_FAST                'typelibCLSID'
               54  LOAD_FAST                'major'
               56  LOAD_FAST                'minor'
               58  LOAD_FAST                'lcid'
               60  CALL_METHOD_4         4  ''
               62  LOAD_METHOD              GetLibAttr
               64  CALL_METHOD_0         0  ''
               66  STORE_FAST               'tlbAttr'

 L. 402        68  LOAD_FAST                'tlbAttr'
               70  LOAD_CONST               1
               72  BINARY_SUBSCR    
               74  LOAD_FAST                'lcid'
               76  COMPARE_OP               !=
               78  POP_JUMP_IF_TRUE     92  'to 92'
               80  LOAD_FAST                'tlbAttr'
               82  LOAD_CONST               4
               84  BINARY_SUBSCR    
               86  LOAD_FAST                'minor'
               88  COMPARE_OP               !=
               90  POP_JUMP_IF_FALSE   152  'to 152'
             92_0  COME_FROM            78  '78'

 L. 404        92  SETUP_FINALLY       124  'to 124'

 L. 405        94  LOAD_GLOBAL              GetModuleForTypelib
               96  LOAD_FAST                'typelibCLSID'
               98  LOAD_FAST                'tlbAttr'
              100  LOAD_CONST               1
              102  BINARY_SUBSCR    
              104  LOAD_FAST                'tlbAttr'
              106  LOAD_CONST               3
              108  BINARY_SUBSCR    
              110  LOAD_FAST                'tlbAttr'
              112  LOAD_CONST               4
              114  BINARY_SUBSCR    
              116  CALL_FUNCTION_4       4  ''
              118  STORE_FAST               'module'
              120  POP_BLOCK        
              122  JUMP_FORWARD        152  'to 152'
            124_0  COME_FROM_FINALLY    92  '92'

 L. 406       124  DUP_TOP          
              126  LOAD_GLOBAL              ImportError
              128  COMPARE_OP               exception-match
              130  POP_JUMP_IF_FALSE   150  'to 150'
              132  POP_TOP          
              134  POP_TOP          
              136  POP_TOP          

 L. 409       138  LOAD_FAST                'tlbAttr'
              140  LOAD_CONST               4
              142  BINARY_SUBSCR    
              144  STORE_FAST               'minor'
              146  POP_EXCEPT       
              148  JUMP_FORWARD        152  'to 152'
            150_0  COME_FROM           130  '130'
              150  END_FINALLY      
            152_0  COME_FROM           148  '148'
            152_1  COME_FROM           122  '122'
            152_2  COME_FROM            90  '90'
              152  POP_BLOCK        
              154  JUMP_FORWARD        178  'to 178'
            156_0  COME_FROM_FINALLY    46  '46'

 L. 411       156  DUP_TOP          
              158  LOAD_GLOBAL              pythoncom
              160  LOAD_ATTR                com_error
              162  COMPARE_OP               exception-match
              164  POP_JUMP_IF_FALSE   176  'to 176'
              166  POP_TOP          
              168  POP_TOP          
              170  POP_TOP          

 L. 413       172  POP_EXCEPT       
              174  JUMP_FORWARD        178  'to 178'
            176_0  COME_FROM           164  '164'
              176  END_FINALLY      
            178_0  COME_FROM           174  '174'
            178_1  COME_FROM           154  '154'
              178  POP_EXCEPT       
              180  JUMP_FORWARD        184  'to 184'
            182_0  COME_FROM            34  '34'
              182  END_FINALLY      
            184_0  COME_FROM           180  '180'
            184_1  COME_FROM            26  '26'

 L. 414       184  LOAD_FAST                'module'
              186  LOAD_CONST               None
              188  COMPARE_OP               is-not
          190_192  POP_JUMP_IF_FALSE   376  'to 376'
              194  LOAD_FAST                'bValidateFile'
          196_198  POP_JUMP_IF_FALSE   376  'to 376'

 L. 415       200  LOAD_GLOBAL              is_readonly
              202  POP_JUMP_IF_FALSE   212  'to 212'
              204  LOAD_GLOBAL              AssertionError
              206  LOAD_STR                 "Can't validate in a read-only gencache"
              208  CALL_FUNCTION_1       1  ''
              210  RAISE_VARARGS_1       1  'exception instance'
            212_0  COME_FROM           202  '202'

 L. 416       212  SETUP_FINALLY       348  'to 348'

 L. 417       214  LOAD_GLOBAL              pythoncom
              216  LOAD_METHOD              QueryPathOfRegTypeLib
              218  LOAD_FAST                'typelibCLSID'
              220  LOAD_FAST                'major'
              222  LOAD_FAST                'minor'
              224  LOAD_FAST                'lcid'
              226  CALL_METHOD_4         4  ''
              228  STORE_FAST               'typLibPath'

 L. 420       230  LOAD_FAST                'typLibPath'
              232  LOAD_CONST               -1
              234  BINARY_SUBSCR    
              236  LOAD_STR                 '\x00'
              238  COMPARE_OP               ==
              240  POP_JUMP_IF_FALSE   254  'to 254'

 L. 421       242  LOAD_FAST                'typLibPath'
              244  LOAD_CONST               None
              246  LOAD_CONST               -1
              248  BUILD_SLICE_2         2 
              250  BINARY_SUBSCR    
              252  STORE_FAST               'typLibPath'
            254_0  COME_FROM           240  '240'

 L. 422       254  LOAD_GLOBAL              getattr
              256  LOAD_GLOBAL              os
              258  LOAD_ATTR                path
              260  LOAD_STR                 'supports_unicode_filenames'
              262  LOAD_CONST               0
              264  CALL_FUNCTION_3       3  ''
              266  STORE_FAST               'suf'

 L. 423       268  LOAD_FAST                'suf'
          270_272  POP_JUMP_IF_TRUE    324  'to 324'

 L. 425       274  SETUP_FINALLY       294  'to 294'

 L. 426       276  LOAD_FAST                'typLibPath'
              278  LOAD_METHOD              encode
              280  LOAD_GLOBAL              sys
              282  LOAD_METHOD              getfilesystemencoding
              284  CALL_METHOD_0         0  ''
              286  CALL_METHOD_1         1  ''
              288  STORE_FAST               'typLibPath'
              290  POP_BLOCK        
              292  JUMP_FORWARD        324  'to 324'
            294_0  COME_FROM_FINALLY   274  '274'

 L. 427       294  DUP_TOP          
              296  LOAD_GLOBAL              AttributeError
              298  COMPARE_OP               exception-match
          300_302  POP_JUMP_IF_FALSE   322  'to 322'
              304  POP_TOP          
              306  POP_TOP          
              308  POP_TOP          

 L. 428       310  LOAD_GLOBAL              str
              312  LOAD_FAST                'typLibPath'
              314  CALL_FUNCTION_1       1  ''
              316  STORE_FAST               'typLibPath'
              318  POP_EXCEPT       
              320  JUMP_FORWARD        324  'to 324'
            322_0  COME_FROM           300  '300'
              322  END_FINALLY      
            324_0  COME_FROM           320  '320'
            324_1  COME_FROM           292  '292'
            324_2  COME_FROM           270  '270'

 L. 429       324  LOAD_GLOBAL              pythoncom
              326  LOAD_METHOD              LoadRegTypeLib
              328  LOAD_FAST                'typelibCLSID'
              330  LOAD_FAST                'major'
              332  LOAD_FAST                'minor'
              334  LOAD_FAST                'lcid'
              336  CALL_METHOD_4         4  ''
              338  LOAD_METHOD              GetLibAttr
              340  CALL_METHOD_0         0  ''
              342  STORE_FAST               'tlbAttributes'
              344  POP_BLOCK        
              346  JUMP_FORWARD        376  'to 376'
            348_0  COME_FROM_FINALLY   212  '212'

 L. 430       348  DUP_TOP          
              350  LOAD_GLOBAL              pythoncom
              352  LOAD_ATTR                com_error
              354  COMPARE_OP               exception-match
          356_358  POP_JUMP_IF_FALSE   374  'to 374'
              360  POP_TOP          
              362  POP_TOP          
              364  POP_TOP          

 L. 434       366  LOAD_CONST               0
              368  STORE_FAST               'bValidateFile'
              370  POP_EXCEPT       
              372  JUMP_FORWARD        376  'to 376'
            374_0  COME_FROM           356  '356'
              374  END_FINALLY      
            376_0  COME_FROM           372  '372'
            376_1  COME_FROM           346  '346'
            376_2  COME_FROM           196  '196'
            376_3  COME_FROM           190  '190'

 L. 435       376  LOAD_FAST                'module'
              378  LOAD_CONST               None
              380  COMPARE_OP               is-not
          382_384  POP_JUMP_IF_FALSE   838  'to 838'
              386  LOAD_FAST                'bValidateFile'
          388_390  POP_JUMP_IF_FALSE   838  'to 838'

 L. 436       392  LOAD_GLOBAL              is_readonly
          394_396  POP_JUMP_IF_FALSE   406  'to 406'
              398  LOAD_GLOBAL              AssertionError
              400  LOAD_STR                 "Can't validate in a read-only gencache"
              402  CALL_FUNCTION_1       1  ''
              404  RAISE_VARARGS_1       1  'exception instance'
            406_0  COME_FROM           394  '394'

 L. 437       406  LOAD_STR                 '%s\\%s'
              408  LOAD_GLOBAL              GetGeneratePath
              410  CALL_FUNCTION_0       0  ''
              412  LOAD_GLOBAL              GetGeneratedFileName
              414  LOAD_FAST                'typelibCLSID'
              416  LOAD_FAST                'lcid'
              418  LOAD_FAST                'major'
              420  LOAD_FAST                'minor'
              422  CALL_FUNCTION_4       4  ''
              424  BUILD_TUPLE_2         2 
              426  BINARY_MODULO    
              428  STORE_FAST               'filePathPrefix'

 L. 438       430  LOAD_FAST                'filePathPrefix'
              432  LOAD_STR                 '.py'
              434  BINARY_ADD       
              436  STORE_FAST               'filePath'

 L. 439       438  LOAD_FAST                'filePathPrefix'
              440  LOAD_STR                 '.py'
              442  BINARY_ADD       
              444  STORE_FAST               'filePathPyc'

 L. 441       446  LOAD_FAST                'filePathPyc'
              448  LOAD_STR                 'c'
              450  BINARY_ADD       
              452  STORE_FAST               'filePathPyc'

 L. 446       454  LOAD_CONST               1
              456  LOAD_CONST               ('genpy',)
              458  IMPORT_NAME              
              460  IMPORT_FROM              genpy
              462  STORE_FAST               'genpy'
              464  POP_TOP          

 L. 447       466  LOAD_FAST                'module'
              468  LOAD_ATTR                MinorVersion
              470  LOAD_FAST                'tlbAttributes'
              472  LOAD_CONST               4
              474  BINARY_SUBSCR    
              476  COMPARE_OP               !=
          478_480  POP_JUMP_IF_TRUE    496  'to 496'
              482  LOAD_FAST                'genpy'
              484  LOAD_ATTR                makepy_version
              486  LOAD_FAST                'module'
              488  LOAD_ATTR                makepy_version
              490  COMPARE_OP               !=
          492_494  POP_JUMP_IF_FALSE   626  'to 626'
            496_0  COME_FROM           478  '478'

 L. 450       496  SETUP_FINALLY       512  'to 512'

 L. 451       498  LOAD_GLOBAL              os
              500  LOAD_METHOD              unlink
              502  LOAD_FAST                'filePath'
              504  CALL_METHOD_1         1  ''
              506  POP_TOP          
              508  POP_BLOCK        
              510  JUMP_FORWARD        536  'to 536'
            512_0  COME_FROM_FINALLY   496  '496'

 L. 452       512  DUP_TOP          
              514  LOAD_GLOBAL              os
              516  LOAD_ATTR                error
              518  COMPARE_OP               exception-match
          520_522  POP_JUMP_IF_FALSE   534  'to 534'
              524  POP_TOP          
              526  POP_TOP          
              528  POP_TOP          

 L. 453       530  POP_EXCEPT       
              532  JUMP_FORWARD        536  'to 536'
            534_0  COME_FROM           520  '520'
              534  END_FINALLY      
            536_0  COME_FROM           532  '532'
            536_1  COME_FROM           510  '510'

 L. 454       536  SETUP_FINALLY       552  'to 552'

 L. 455       538  LOAD_GLOBAL              os
              540  LOAD_METHOD              unlink
              542  LOAD_FAST                'filePathPyc'
              544  CALL_METHOD_1         1  ''
              546  POP_TOP          
              548  POP_BLOCK        
              550  JUMP_FORWARD        576  'to 576'
            552_0  COME_FROM_FINALLY   536  '536'

 L. 456       552  DUP_TOP          
              554  LOAD_GLOBAL              os
              556  LOAD_ATTR                error
              558  COMPARE_OP               exception-match
          560_562  POP_JUMP_IF_FALSE   574  'to 574'
              564  POP_TOP          
              566  POP_TOP          
              568  POP_TOP          

 L. 457       570  POP_EXCEPT       
              572  JUMP_FORWARD        576  'to 576'
            574_0  COME_FROM           560  '560'
              574  END_FINALLY      
            576_0  COME_FROM           572  '572'
            576_1  COME_FROM           550  '550'

 L. 458       576  LOAD_GLOBAL              os
              578  LOAD_ATTR                path
              580  LOAD_METHOD              isdir
              582  LOAD_FAST                'filePathPrefix'
              584  CALL_METHOD_1         1  ''
          586_588  POP_JUMP_IF_FALSE   608  'to 608'

 L. 459       590  LOAD_CONST               0
              592  LOAD_CONST               None
              594  IMPORT_NAME              shutil
              596  STORE_FAST               'shutil'

 L. 460       598  LOAD_FAST                'shutil'
              600  LOAD_METHOD              rmtree
              602  LOAD_FAST                'filePathPrefix'
              604  CALL_METHOD_1         1  ''
              606  POP_TOP          
            608_0  COME_FROM           586  '586'

 L. 461       608  LOAD_FAST                'tlbAttributes'
              610  LOAD_CONST               4
              612  BINARY_SUBSCR    
              614  STORE_FAST               'minor'

 L. 462       616  LOAD_CONST               None
              618  STORE_FAST               'module'

 L. 463       620  LOAD_CONST               1
              622  STORE_FAST               'bReloadNeeded'
              624  JUMP_FORWARD        838  'to 838'
            626_0  COME_FROM           492  '492'

 L. 465       626  LOAD_FAST                'module'
              628  LOAD_ATTR                MinorVersion
              630  STORE_FAST               'minor'

 L. 466       632  LOAD_STR                 '%s\\%s'
              634  LOAD_GLOBAL              GetGeneratePath
              636  CALL_FUNCTION_0       0  ''
              638  LOAD_GLOBAL              GetGeneratedFileName
              640  LOAD_FAST                'typelibCLSID'
              642  LOAD_FAST                'lcid'
              644  LOAD_FAST                'major'
              646  LOAD_FAST                'minor'
              648  CALL_FUNCTION_4       4  ''
              650  BUILD_TUPLE_2         2 
              652  BINARY_MODULO    
              654  STORE_FAST               'filePathPrefix'

 L. 467       656  LOAD_FAST                'filePathPrefix'
              658  LOAD_STR                 '.py'
              660  BINARY_ADD       
              662  STORE_FAST               'filePath'

 L. 468       664  LOAD_FAST                'filePathPrefix'
              666  LOAD_STR                 '.pyc'
              668  BINARY_ADD       
              670  STORE_FAST               'filePathPyc'

 L. 470       672  LOAD_CONST               0
              674  STORE_FAST               'fModTimeSet'

 L. 471       676  SETUP_FINALLY       700  'to 700'

 L. 472       678  LOAD_GLOBAL              os
              680  LOAD_METHOD              stat
              682  LOAD_FAST                'filePath'
              684  CALL_METHOD_1         1  ''
              686  LOAD_CONST               8
              688  BINARY_SUBSCR    
              690  STORE_FAST               'pyModTime'

 L. 473       692  LOAD_CONST               1
              694  STORE_FAST               'fModTimeSet'
              696  POP_BLOCK        
              698  JUMP_FORWARD        800  'to 800'
            700_0  COME_FROM_FINALLY   676  '676'

 L. 474       700  DUP_TOP          
              702  LOAD_GLOBAL              os
              704  LOAD_ATTR                error
              706  COMPARE_OP               exception-match
          708_710  POP_JUMP_IF_FALSE   798  'to 798'
              712  POP_TOP          
              714  STORE_FAST               'e'
              716  POP_TOP          
              718  SETUP_FINALLY       786  'to 786'

 L. 477       720  SETUP_FINALLY       744  'to 744'

 L. 478       722  LOAD_GLOBAL              os
              724  LOAD_METHOD              stat
              726  LOAD_FAST                'filePathPyc'
              728  CALL_METHOD_1         1  ''
              730  LOAD_CONST               8
              732  BINARY_SUBSCR    
              734  STORE_FAST               'pyModTime'

 L. 479       736  LOAD_CONST               1
              738  STORE_FAST               'fModTimeSet'
              740  POP_BLOCK        
              742  JUMP_FORWARD        782  'to 782'
            744_0  COME_FROM_FINALLY   720  '720'

 L. 480       744  DUP_TOP          
              746  LOAD_GLOBAL              os
              748  LOAD_ATTR                error
              750  COMPARE_OP               exception-match
          752_754  POP_JUMP_IF_FALSE   780  'to 780'
              756  POP_TOP          
              758  STORE_FAST               'e'
              760  POP_TOP          
              762  SETUP_FINALLY       768  'to 768'

 L. 481       764  POP_BLOCK        
              766  BEGIN_FINALLY    
            768_0  COME_FROM_FINALLY   762  '762'
              768  LOAD_CONST               None
              770  STORE_FAST               'e'
              772  DELETE_FAST              'e'
              774  END_FINALLY      
              776  POP_EXCEPT       
              778  JUMP_FORWARD        782  'to 782'
            780_0  COME_FROM           752  '752'
              780  END_FINALLY      
            782_0  COME_FROM           778  '778'
            782_1  COME_FROM           742  '742'
              782  POP_BLOCK        
              784  BEGIN_FINALLY    
            786_0  COME_FROM_FINALLY   718  '718'
              786  LOAD_CONST               None
              788  STORE_FAST               'e'
              790  DELETE_FAST              'e'
              792  END_FINALLY      
              794  POP_EXCEPT       
              796  JUMP_FORWARD        800  'to 800'
            798_0  COME_FROM           708  '708'
              798  END_FINALLY      
            800_0  COME_FROM           796  '796'
            800_1  COME_FROM           698  '698'

 L. 484       800  LOAD_GLOBAL              os
              802  LOAD_METHOD              stat
              804  LOAD_FAST                'typLibPath'
              806  CALL_METHOD_1         1  ''
              808  LOAD_CONST               8
              810  BINARY_SUBSCR    
              812  STORE_FAST               'typLibModTime'

 L. 485       814  LOAD_FAST                'fModTimeSet'
          816_818  POP_JUMP_IF_FALSE   838  'to 838'
              820  LOAD_FAST                'typLibModTime'
              822  LOAD_FAST                'pyModTime'
              824  COMPARE_OP               >
          826_828  POP_JUMP_IF_FALSE   838  'to 838'

 L. 486       830  LOAD_CONST               1
              832  STORE_FAST               'bReloadNeeded'

 L. 487       834  LOAD_CONST               None
              836  STORE_FAST               'module'
            838_0  COME_FROM           826  '826'
            838_1  COME_FROM           816  '816'
            838_2  COME_FROM           624  '624'
            838_3  COME_FROM           388  '388'
            838_4  COME_FROM           382  '382'
              838  POP_BLOCK        
              840  JUMP_FORWARD        874  'to 874'
            842_0  COME_FROM_FINALLY     4  '4'

 L. 488       842  DUP_TOP          
              844  LOAD_GLOBAL              ImportError
              846  LOAD_GLOBAL              os
              848  LOAD_ATTR                error
              850  BUILD_TUPLE_2         2 
              852  COMPARE_OP               exception-match
          854_856  POP_JUMP_IF_FALSE   872  'to 872'
              858  POP_TOP          
              860  POP_TOP          
              862  POP_TOP          

 L. 489       864  LOAD_CONST               None
              866  STORE_FAST               'module'
              868  POP_EXCEPT       
              870  JUMP_FORWARD        874  'to 874'
            872_0  COME_FROM           854  '854'
              872  END_FINALLY      
            874_0  COME_FROM           870  '870'
            874_1  COME_FROM           840  '840'

 L. 490       874  LOAD_FAST                'module'
              876  LOAD_CONST               None
              878  COMPARE_OP               is
          880_882  POP_JUMP_IF_FALSE  1130  'to 1130'

 L. 494       884  LOAD_GLOBAL              is_readonly
          886_888  POP_JUMP_IF_FALSE  1080  'to 1080'

 L. 495       890  LOAD_GLOBAL              str
              892  LOAD_FAST                'typelibCLSID'
              894  CALL_FUNCTION_1       1  ''
              896  LOAD_FAST                'lcid'
              898  LOAD_FAST                'major'
              900  LOAD_FAST                'minor'
              902  BUILD_TUPLE_4         4 
              904  STORE_FAST               'key'

 L. 497       906  SETUP_FINALLY       918  'to 918'

 L. 498       908  LOAD_GLOBAL              versionRedirectMap
              910  LOAD_FAST                'key'
              912  BINARY_SUBSCR    
              914  POP_BLOCK        
              916  RETURN_VALUE     
            918_0  COME_FROM_FINALLY   906  '906'

 L. 499       918  DUP_TOP          
              920  LOAD_GLOBAL              KeyError
              922  COMPARE_OP               exception-match
          924_926  POP_JUMP_IF_FALSE   938  'to 938'
              928  POP_TOP          
              930  POP_TOP          
              932  POP_TOP          

 L. 500       934  POP_EXCEPT       
              936  JUMP_FORWARD        940  'to 940'
            938_0  COME_FROM           924  '924'
              938  END_FINALLY      
            940_0  COME_FROM           936  '936'

 L. 502       940  BUILD_LIST_0          0 
              942  STORE_FAST               'items'

 L. 503       944  LOAD_GLOBAL              GetGeneratedInfos
              946  CALL_FUNCTION_0       0  ''
              948  GET_ITER         
            950_0  COME_FROM          1004  '1004'
            950_1  COME_FROM           986  '986'
            950_2  COME_FROM           968  '968'
              950  FOR_ITER           1022  'to 1022'
              952  STORE_FAST               'desc'

 L. 504       954  LOAD_FAST                'key'
              956  LOAD_CONST               0
              958  BINARY_SUBSCR    
              960  LOAD_FAST                'desc'
              962  LOAD_CONST               0
              964  BINARY_SUBSCR    
              966  COMPARE_OP               ==
          968_970  POP_JUMP_IF_FALSE   950  'to 950'
              972  LOAD_FAST                'key'
              974  LOAD_CONST               1
              976  BINARY_SUBSCR    
              978  LOAD_FAST                'desc'
              980  LOAD_CONST               1
              982  BINARY_SUBSCR    
              984  COMPARE_OP               ==
          986_988  POP_JUMP_IF_FALSE   950  'to 950'
              990  LOAD_FAST                'key'
              992  LOAD_CONST               2
              994  BINARY_SUBSCR    
              996  LOAD_FAST                'desc'
              998  LOAD_CONST               2
             1000  BINARY_SUBSCR    
             1002  COMPARE_OP               ==
         1004_1006  POP_JUMP_IF_FALSE   950  'to 950'

 L. 505      1008  LOAD_FAST                'items'
             1010  LOAD_METHOD              append
             1012  LOAD_FAST                'desc'
             1014  CALL_METHOD_1         1  ''
             1016  POP_TOP          
         1018_1020  JUMP_BACK           950  'to 950'

 L. 506      1022  LOAD_FAST                'items'
         1024_1026  POP_JUMP_IF_FALSE  1064  'to 1064'

 L. 509      1028  LOAD_FAST                'items'
             1030  LOAD_METHOD              sort
             1032  CALL_METHOD_0         0  ''
             1034  POP_TOP          

 L. 510      1036  LOAD_FAST                'items'
             1038  LOAD_CONST               -1
             1040  BINARY_SUBSCR    
             1042  LOAD_CONST               3
             1044  BINARY_SUBSCR    
             1046  STORE_FAST               'new_minor'

 L. 511      1048  LOAD_GLOBAL              GetModuleForTypelib
             1050  LOAD_FAST                'typelibCLSID'
             1052  LOAD_FAST                'lcid'
             1054  LOAD_FAST                'major'
             1056  LOAD_FAST                'new_minor'
             1058  CALL_FUNCTION_4       4  ''
             1060  STORE_FAST               'ret'
             1062  JUMP_FORWARD       1068  'to 1068'
           1064_0  COME_FROM          1024  '1024'

 L. 513      1064  LOAD_CONST               None
             1066  STORE_FAST               'ret'
           1068_0  COME_FROM          1062  '1062'

 L. 515      1068  LOAD_FAST                'ret'
             1070  LOAD_GLOBAL              versionRedirectMap
             1072  LOAD_FAST                'key'
             1074  STORE_SUBSCR     

 L. 516      1076  LOAD_FAST                'ret'
             1078  RETURN_VALUE     
           1080_0  COME_FROM           886  '886'

 L. 518      1080  LOAD_GLOBAL              MakeModuleForTypelib
             1082  LOAD_FAST                'typelibCLSID'
             1084  LOAD_FAST                'lcid'
             1086  LOAD_FAST                'major'
             1088  LOAD_FAST                'minor'
             1090  LOAD_FAST                'progressInstance'
             1092  LOAD_FAST                'bForDemand'
             1094  LOAD_FAST                'bBuildHidden'
             1096  LOAD_CONST               ('bForDemand', 'bBuildHidden')
             1098  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1100  STORE_FAST               'module'

 L. 520      1102  LOAD_FAST                'bReloadNeeded'
         1104_1106  POP_JUMP_IF_FALSE  1130  'to 1130'

 L. 521      1108  LOAD_GLOBAL              reload
             1110  LOAD_FAST                'module'
             1112  CALL_FUNCTION_1       1  ''
             1114  STORE_FAST               'module'

 L. 522      1116  LOAD_GLOBAL              AddModuleToCache
             1118  LOAD_FAST                'typelibCLSID'
             1120  LOAD_FAST                'lcid'
             1122  LOAD_FAST                'major'
             1124  LOAD_FAST                'minor'
             1126  CALL_FUNCTION_4       4  ''
             1128  POP_TOP          
           1130_0  COME_FROM          1104  '1104'
           1130_1  COME_FROM           880  '880'

 L. 523      1130  LOAD_FAST                'module'
             1132  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 930


    def EnsureDispatch(prog_id, bForDemand=1):
        """Given a COM prog_id, return an object that is using makepy support, building if necessary"""
        disp = win32com.client.Dispatch(prog_id)
        if not disp.__dict__.get('CLSID'):
            try:
                ti = disp._oleobj_.GetTypeInfo()
                disp_clsid = ti.GetTypeAttr()[0]
                tlb, index = ti.GetContainingTypeLib()
                tla = tlb.GetLibAttr()
                mod = EnsureModule((tla[0]), (tla[1]), (tla[3]), (tla[4]), bForDemand=bForDemand)
                GetModuleForCLSID(disp_clsid)
                from . import CLSIDToClass
                disp_class = CLSIDToClass.GetClass(str(disp_clsid))
                disp = disp_class(disp._oleobj_)
            except pythoncom.com_error:
                raise TypeError('This COM object can not automate the makepy process - please run makepy manually for this object')

        return disp


    def AddModuleToCache(typelibclsid, lcid, major, minor, verbose=1, bFlushNow=not is_readonly):
        """Add a newly generated file to the cache dictionary.
        """
        fname = GetGeneratedFileName(typelibclsid, lcid, major, minor)
        mod = _GetModule(fname)
        mod._in_gencache_ = 1
        dict = mod.CLSIDToClassMap
        info = (str(typelibclsid), lcid, major, minor)
        for clsid, cls in dict.items():
            clsidToTypelib[clsid] = info
        else:
            dict = mod.CLSIDToPackageMap
            for clsid, name in dict.items():
                clsidToTypelib[clsid] = info
            else:
                dict = mod.VTablesToClassMap
                for clsid, cls in dict.items():
                    clsidToTypelib[clsid] = info
                else:
                    dict = mod.VTablesToPackageMap
                    for clsid, cls in dict.items():
                        clsidToTypelib[clsid] = info
                    else:
                        if info in versionRedirectMap:
                            del versionRedirectMap[info]
                        if bFlushNow:
                            _SaveDicts()


    def GetGeneratedInfos--- This code section failed: ---

 L. 576         0  LOAD_GLOBAL              win32com
                2  LOAD_ATTR                __gen_path__
                4  LOAD_METHOD              find
                6  LOAD_STR                 '.zip\\'
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'zip_pos'

 L. 577        12  LOAD_FAST                'zip_pos'
               14  LOAD_CONST               0
               16  COMPARE_OP               >=
            18_20  POP_JUMP_IF_FALSE   294  'to 294'

 L. 578        22  LOAD_CONST               0
               24  LOAD_CONST               None
               26  IMPORT_NAME              zipfile
               28  STORE_FAST               'zipfile'

 L. 579        30  LOAD_GLOBAL              win32com
               32  LOAD_ATTR                __gen_path__
               34  LOAD_CONST               None
               36  LOAD_FAST                'zip_pos'
               38  LOAD_CONST               4
               40  BINARY_ADD       
               42  BUILD_SLICE_2         2 
               44  BINARY_SUBSCR    
               46  STORE_FAST               'zip_file'

 L. 580        48  LOAD_GLOBAL              win32com
               50  LOAD_ATTR                __gen_path__
               52  LOAD_FAST                'zip_pos'
               54  LOAD_CONST               5
               56  BINARY_ADD       
               58  LOAD_CONST               None
               60  BUILD_SLICE_2         2 
               62  BINARY_SUBSCR    
               64  LOAD_METHOD              replace
               66  LOAD_STR                 '\\'
               68  LOAD_STR                 '/'
               70  CALL_METHOD_2         2  ''
               72  STORE_FAST               'zip_path'

 L. 581        74  LOAD_FAST                'zipfile'
               76  LOAD_METHOD              ZipFile
               78  LOAD_FAST                'zip_file'
               80  CALL_METHOD_1         1  ''
               82  STORE_FAST               'zf'

 L. 582        84  BUILD_MAP_0           0 
               86  STORE_FAST               'infos'

 L. 583        88  LOAD_FAST                'zf'
               90  LOAD_METHOD              namelist
               92  CALL_METHOD_0         0  ''
               94  GET_ITER         
               96  FOR_ITER            274  'to 274'
               98  STORE_FAST               'n'

 L. 584       100  LOAD_FAST                'n'
              102  LOAD_METHOD              startswith
              104  LOAD_FAST                'zip_path'
              106  CALL_METHOD_1         1  ''
              108  POP_JUMP_IF_TRUE    112  'to 112'

 L. 585       110  JUMP_BACK            96  'to 96'
            112_0  COME_FROM           108  '108'

 L. 586       112  LOAD_FAST                'n'
              114  LOAD_GLOBAL              len
              116  LOAD_FAST                'zip_path'
              118  CALL_FUNCTION_1       1  ''
              120  LOAD_CONST               1
              122  BINARY_ADD       
              124  LOAD_CONST               None
              126  BUILD_SLICE_2         2 
              128  BINARY_SUBSCR    
              130  LOAD_METHOD              split
              132  LOAD_STR                 '/'
              134  CALL_METHOD_1         1  ''
              136  LOAD_CONST               0
              138  BINARY_SUBSCR    
              140  STORE_FAST               'base'

 L. 587       142  SETUP_FINALLY       208  'to 208'

 L. 588       144  LOAD_FAST                'base'
              146  LOAD_METHOD              split
              148  LOAD_STR                 'x'
              150  CALL_METHOD_1         1  ''
              152  UNPACK_SEQUENCE_4     4 
              154  STORE_FAST               'iid'
              156  STORE_FAST               'lcid'
              158  STORE_FAST               'major'
              160  STORE_FAST               'minor'

 L. 589       162  LOAD_GLOBAL              int
              164  LOAD_FAST                'lcid'
              166  CALL_FUNCTION_1       1  ''
              168  STORE_FAST               'lcid'

 L. 590       170  LOAD_GLOBAL              int
              172  LOAD_FAST                'major'
              174  CALL_FUNCTION_1       1  ''
              176  STORE_FAST               'major'

 L. 591       178  LOAD_GLOBAL              int
              180  LOAD_FAST                'minor'
              182  CALL_FUNCTION_1       1  ''
              184  STORE_FAST               'minor'

 L. 592       186  LOAD_GLOBAL              pywintypes
              188  LOAD_METHOD              IID
              190  LOAD_STR                 '{'
              192  LOAD_FAST                'iid'
              194  BINARY_ADD       
              196  LOAD_STR                 '}'
              198  BINARY_ADD       
              200  CALL_METHOD_1         1  ''
              202  STORE_FAST               'iid'
              204  POP_BLOCK        
              206  JUMP_FORWARD        256  'to 256'
            208_0  COME_FROM_FINALLY   142  '142'

 L. 593       208  DUP_TOP          
              210  LOAD_GLOBAL              ValueError
              212  COMPARE_OP               exception-match
              214  POP_JUMP_IF_FALSE   230  'to 230'
              216  POP_TOP          
              218  POP_TOP          
              220  POP_TOP          

 L. 594       222  POP_EXCEPT       
              224  JUMP_BACK            96  'to 96'
              226  POP_EXCEPT       
              228  JUMP_FORWARD        256  'to 256'
            230_0  COME_FROM           214  '214'

 L. 595       230  DUP_TOP          
              232  LOAD_GLOBAL              pywintypes
              234  LOAD_ATTR                com_error
              236  COMPARE_OP               exception-match
              238  POP_JUMP_IF_FALSE   254  'to 254'
              240  POP_TOP          
              242  POP_TOP          
              244  POP_TOP          

 L. 597       246  POP_EXCEPT       
              248  JUMP_BACK            96  'to 96'
              250  POP_EXCEPT       
              252  JUMP_FORWARD        256  'to 256'
            254_0  COME_FROM           238  '238'
              254  END_FINALLY      
            256_0  COME_FROM           252  '252'
            256_1  COME_FROM           228  '228'
            256_2  COME_FROM           206  '206'

 L. 598       256  LOAD_CONST               1
              258  LOAD_FAST                'infos'
              260  LOAD_FAST                'iid'
              262  LOAD_FAST                'lcid'
              264  LOAD_FAST                'major'
              266  LOAD_FAST                'minor'
              268  BUILD_TUPLE_4         4 
              270  STORE_SUBSCR     
              272  JUMP_BACK            96  'to 96'

 L. 599       274  LOAD_FAST                'zf'
              276  LOAD_METHOD              close
              278  CALL_METHOD_0         0  ''
              280  POP_TOP          

 L. 600       282  LOAD_GLOBAL              list
              284  LOAD_FAST                'infos'
              286  LOAD_METHOD              keys
              288  CALL_METHOD_0         0  ''
              290  CALL_FUNCTION_1       1  ''
              292  RETURN_VALUE     
            294_0  COME_FROM            18  '18'

 L. 603       294  LOAD_GLOBAL              glob
              296  LOAD_METHOD              glob
              298  LOAD_GLOBAL              win32com
              300  LOAD_ATTR                __gen_path__
              302  LOAD_STR                 '\\*'
              304  BINARY_ADD       
              306  CALL_METHOD_1         1  ''
              308  STORE_FAST               'files'

 L. 604       310  BUILD_LIST_0          0 
              312  STORE_FAST               'ret'

 L. 605       314  LOAD_FAST                'files'
              316  GET_ITER         
              318  FOR_ITER            534  'to 534'
              320  STORE_FAST               'file'

 L. 606       322  LOAD_GLOBAL              os
              324  LOAD_ATTR                path
              326  LOAD_METHOD              isdir
              328  LOAD_FAST                'file'
              330  CALL_METHOD_1         1  ''
          332_334  POP_JUMP_IF_TRUE    362  'to 362'
              336  LOAD_GLOBAL              os
              338  LOAD_ATTR                path
              340  LOAD_METHOD              splitext
              342  LOAD_FAST                'file'
              344  CALL_METHOD_1         1  ''
              346  LOAD_CONST               1
              348  BINARY_SUBSCR    
              350  LOAD_STR                 '.py'
              352  COMPARE_OP               ==
          354_356  POP_JUMP_IF_TRUE    362  'to 362'

 L. 607   358_360  JUMP_BACK           318  'to 318'
            362_0  COME_FROM           354  '354'
            362_1  COME_FROM           332  '332'

 L. 608       362  LOAD_GLOBAL              os
              364  LOAD_ATTR                path
              366  LOAD_METHOD              splitext
              368  LOAD_GLOBAL              os
              370  LOAD_ATTR                path
              372  LOAD_METHOD              split
              374  LOAD_FAST                'file'
              376  CALL_METHOD_1         1  ''
              378  LOAD_CONST               1
              380  BINARY_SUBSCR    
              382  CALL_METHOD_1         1  ''
              384  LOAD_CONST               0
              386  BINARY_SUBSCR    
              388  STORE_FAST               'name'

 L. 609       390  SETUP_FINALLY       456  'to 456'

 L. 610       392  LOAD_FAST                'name'
              394  LOAD_METHOD              split
              396  LOAD_STR                 'x'
              398  CALL_METHOD_1         1  ''
              400  UNPACK_SEQUENCE_4     4 
              402  STORE_FAST               'iid'
              404  STORE_FAST               'lcid'
              406  STORE_FAST               'major'
              408  STORE_FAST               'minor'

 L. 611       410  LOAD_GLOBAL              pywintypes
              412  LOAD_METHOD              IID
              414  LOAD_STR                 '{'
              416  LOAD_FAST                'iid'
              418  BINARY_ADD       
              420  LOAD_STR                 '}'
              422  BINARY_ADD       
              424  CALL_METHOD_1         1  ''
              426  STORE_FAST               'iid'

 L. 612       428  LOAD_GLOBAL              int
              430  LOAD_FAST                'lcid'
              432  CALL_FUNCTION_1       1  ''
              434  STORE_FAST               'lcid'

 L. 613       436  LOAD_GLOBAL              int
              438  LOAD_FAST                'major'
              440  CALL_FUNCTION_1       1  ''
              442  STORE_FAST               'major'

 L. 614       444  LOAD_GLOBAL              int
              446  LOAD_FAST                'minor'
              448  CALL_FUNCTION_1       1  ''
              450  STORE_FAST               'minor'
              452  POP_BLOCK        
              454  JUMP_FORWARD        512  'to 512'
            456_0  COME_FROM_FINALLY   390  '390'

 L. 615       456  DUP_TOP          
              458  LOAD_GLOBAL              ValueError
              460  COMPARE_OP               exception-match
          462_464  POP_JUMP_IF_FALSE   482  'to 482'
              466  POP_TOP          
              468  POP_TOP          
              470  POP_TOP          

 L. 616       472  POP_EXCEPT       
          474_476  JUMP_BACK           318  'to 318'
              478  POP_EXCEPT       
              480  JUMP_FORWARD        512  'to 512'
            482_0  COME_FROM           462  '462'

 L. 617       482  DUP_TOP          
              484  LOAD_GLOBAL              pywintypes
              486  LOAD_ATTR                com_error
              488  COMPARE_OP               exception-match
          490_492  POP_JUMP_IF_FALSE   510  'to 510'
              494  POP_TOP          
              496  POP_TOP          
              498  POP_TOP          

 L. 619       500  POP_EXCEPT       
          502_504  JUMP_BACK           318  'to 318'
              506  POP_EXCEPT       
              508  JUMP_FORWARD        512  'to 512'
            510_0  COME_FROM           490  '490'
              510  END_FINALLY      
            512_0  COME_FROM           508  '508'
            512_1  COME_FROM           480  '480'
            512_2  COME_FROM           454  '454'

 L. 620       512  LOAD_FAST                'ret'
              514  LOAD_METHOD              append
              516  LOAD_FAST                'iid'
              518  LOAD_FAST                'lcid'
              520  LOAD_FAST                'major'
              522  LOAD_FAST                'minor'
              524  BUILD_TUPLE_4         4 
              526  CALL_METHOD_1         1  ''
              528  POP_TOP          
          530_532  JUMP_BACK           318  'to 318'

 L. 621       534  LOAD_FAST                'ret'
              536  RETURN_VALUE     

Parse error at or near `POP_EXCEPT' instruction at offset 226


    def _GetModule(fname):
        """Given the name of a module in the gen_py directory, import and return it.
        """
        mod_name = 'win32com.gen_py.%s' % fname
        mod = __import__(mod_name)
        return sys.modules[mod_name]


    def Rebuild(verbose=1):
        """Rebuild the cache indexes from the file system.
        """
        clsidToTypelib.clear()
        infos = GetGeneratedInfos()
        if verbose:
            if len(infos):
                print('Rebuilding cache of generated files for COM support...')
        for info in infos:
            iid, lcid, major, minor = info
            if verbose:
                print('Checking', GetGeneratedFileName(*info))
            try:
                AddModuleToCache(iid, lcid, major, minor, verbose, 0)
            except:
                print('Could not add module %s - %s: %s' % (info, sys.exc_info()[0], sys.exc_info()[1]))

        else:
            if verbose:
                if len(infos):
                    print('Done.')
            _SaveDicts()


    def _Dump():
        print('Cache is in directory', win32com.__gen_path__)
        d = {}
        for clsid, (typelibCLSID, lcid, major, minor) in clsidToTypelib.items():
            d[(typelibCLSID, lcid, major, minor)] = None
        else:
            for typelibCLSID, lcid, major, minor in d.keys():
                mod = GetModuleForTypelib(typelibCLSID, lcid, major, minor)
                print('%s - %s' % (mod.__doc__, typelibCLSID))


    __init__()

    def usage():
        usageString = '\t  Usage: gencache [-q] [-d] [-r]\n\t  \n\t\t\t -q         - Quiet\n\t\t\t -d         - Dump the cache (typelibrary description and filename).\n\t\t\t -r         - Rebuild the cache dictionary from the existing .py files\n\t'
        print(usageString)
        sys.exit(1)


    if __name__ == '__main__':
        import getopt
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'qrd')
        except getopt.error as message:
            try:
                print(message)
                usage()
            finally:
                message = None
                del message

        else:
            if len(sys.argv) == 1 or args:
                print(usage())
            verbose = 1
            for opt, val in opts:
                if opt == '-d':
                    _Dump()
                if opt == '-r':
                    Rebuild(verbose)
                if opt == '-q':
                    verbose = 0