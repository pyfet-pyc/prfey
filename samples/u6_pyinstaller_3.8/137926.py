# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: win32com\client\makepy.py
"""Generate a .py file from an OLE TypeLibrary file.

 This module is concerned only with the actual writing of
 a .py file.  It draws on the @build@ module, which builds 
 the knowledge of a COM interface.
 
"""
usageHelp = ' \nUsage:\n\n  makepy.py [-i] [-v|q] [-h] [-u] [-o output_file] [-d] [typelib, ...]\n  \n  -i    -- Show information for the specified typelib.\n  \n  -v    -- Verbose output.\n  \n  -q    -- Quiet output.\n  \n  -h    -- Do not generate hidden methods.\n  \n  -u    -- Python 1.5 and earlier: Do NOT convert all Unicode objects to \n           strings.\n                                   \n           Python 1.6 and later: Convert all Unicode objects to strings.\n  \n  -o    -- Create output in a specified output file.  If the path leading\n           to the file does not exist, any missing directories will be\n           created.\n           NOTE: -o cannot be used with -d.  This will generate an error.\n  \n  -d    -- Generate the base code now and the class code on demand.\n           Recommended for large type libraries.\n           \n  typelib -- A TLB, DLL, OCX or anything containing COM type information.\n             If a typelib is not specified, a window containing a textbox\n             will open from which you can select a registered type\n             library.\n               \nExamples:\n\n  makepy.py -d\n  \n    Presents a list of registered type libraries from which you can make\n    a selection.\n    \n  makepy.py -d "Microsoft Excel 8.0 Object Library"\n  \n    Generate support for the type library with the specified description\n    (in this case, the MS Excel object model).\n\n'
import sys, os, pythoncom
from win32com.client import genpy, selecttlb, gencache
from win32com.client import Dispatch
bForDemandDefault = 0
error = 'makepy.error'

def usage():
    sys.stderr.write(usageHelp)
    sys.exit(2)


def ShowInfo(spec):
    tlbSpec = spec or selecttlb.SelectTlb(excludeFlags=(selecttlb.FLAG_HIDDEN))
    if tlbSpec is None:
        return
        try:
            tlb = pythoncom.LoadRegTypeLib(tlbSpec.clsid, tlbSpec.major, tlbSpec.minor, tlbSpec.lcid)
        except pythoncom.com_error:
            sys.stderr.write("Warning - could not load registered typelib '%s'\n" % tlbSpec.clsid)
            tlb = None
        else:
            infos = [
             (
              tlb, tlbSpec)]
    else:
        infos = GetTypeLibsForSpec(spec)
    for tlb, tlbSpec in infos:
        desc = tlbSpec.desc
        if desc is None:
            if tlb is None:
                desc = '<Could not load typelib %s>' % tlbSpec.dll
            else:
                desc = tlb.GetDocumentation(-1)[0]
        print(desc)
        print(' %s, lcid=%s, major=%s, minor=%s' % (tlbSpec.clsid, tlbSpec.lcid, tlbSpec.major, tlbSpec.minor))
        print(' >>> # Use these commands in Python code to auto generate .py support')
        print(' >>> from win32com.client import gencache')
        print(" >>> gencache.EnsureModule('%s', %s, %s, %s)" % (tlbSpec.clsid, tlbSpec.lcid, tlbSpec.major, tlbSpec.minor))


class SimpleProgress(genpy.GeneratorProgress):
    __doc__ = 'A simple progress class prints its output to stderr\n\t'

    def __init__(self, verboseLevel):
        self.verboseLevel = verboseLevel

    def Close(self):
        pass

    def Finished(self):
        if self.verboseLevel > 1:
            sys.stderr.write('Generation complete..\n')

    def SetDescription(self, desc, maxticks=None):
        if self.verboseLevel:
            sys.stderr.write(desc + '\n')

    def Tick(self, desc=None):
        pass

    def VerboseProgress(self, desc, verboseLevel=2):
        if self.verboseLevel >= verboseLevel:
            sys.stderr.write(desc + '\n')

    def LogBeginGenerate(self, filename):
        self.VerboseProgress('Generating to %s' % filename, 1)

    def LogWarning(self, desc):
        self.VerboseProgress('WARNING: ' + desc, 1)


class GUIProgress(SimpleProgress):

    def __init__(self, verboseLevel):
        import win32ui, pywin
        SimpleProgress.__init__(self, verboseLevel)
        self.dialog = None

    def Close(self):
        if self.dialog is not None:
            self.dialog.Close()
            self.dialog = None

    def Starting(self, tlb_desc):
        SimpleProgress.Starting(self, tlb_desc)
        if self.dialog is None:
            from pywin.dialogs import status
            self.dialog = status.ThreadedStatusProgressDialog(tlb_desc)
        else:
            self.dialog.SetTitle(tlb_desc)

    def SetDescription(self, desc, maxticks=None):
        self.dialog.SetText(desc)
        if maxticks:
            self.dialog.SetMaxTicks(maxticks)

    def Tick(self, desc=None):
        self.dialog.Tick()
        if desc is not None:
            self.dialog.SetText(desc)


def GetTypeLibsForSpec--- This code section failed: ---

 L. 168         0  BUILD_LIST_0          0 
                2  STORE_FAST               'typelibs'

 L. 169       4_6  SETUP_FINALLY       346  'to 346'

 L. 170         8  SETUP_FINALLY        68  'to 68'

 L. 171        10  LOAD_GLOBAL              pythoncom
               12  LOAD_METHOD              LoadTypeLib
               14  LOAD_FAST                'arg'
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'tlb'

 L. 172        20  LOAD_GLOBAL              selecttlb
               22  LOAD_METHOD              TypelibSpec
               24  LOAD_CONST               None
               26  LOAD_CONST               0
               28  LOAD_CONST               0
               30  LOAD_CONST               0
               32  CALL_METHOD_4         4  ''
               34  STORE_FAST               'spec'

 L. 173        36  LOAD_FAST                'spec'
               38  LOAD_METHOD              FromTypelib
               40  LOAD_FAST                'tlb'
               42  LOAD_FAST                'arg'
               44  CALL_METHOD_2         2  ''
               46  POP_TOP          

 L. 174        48  LOAD_FAST                'typelibs'
               50  LOAD_METHOD              append
               52  LOAD_FAST                'tlb'
               54  LOAD_FAST                'spec'
               56  BUILD_TUPLE_2         2 
               58  CALL_METHOD_1         1  ''
               60  POP_TOP          
               62  POP_BLOCK        
            64_66  JUMP_FORWARD        340  'to 340'
             68_0  COME_FROM_FINALLY     8  '8'

 L. 175        68  DUP_TOP          
               70  LOAD_GLOBAL              pythoncom
               72  LOAD_ATTR                com_error
               74  COMPARE_OP               exception-match
            76_78  POP_JUMP_IF_FALSE   338  'to 338'
               80  POP_TOP          
               82  POP_TOP          
               84  POP_TOP          

 L. 177        86  LOAD_GLOBAL              selecttlb
               88  LOAD_METHOD              FindTlbsWithDescription
               90  LOAD_FAST                'arg'
               92  CALL_METHOD_1         1  ''
               94  STORE_FAST               'tlbs'

 L. 178        96  LOAD_GLOBAL              len
               98  LOAD_FAST                'tlbs'
              100  CALL_FUNCTION_1       1  ''
              102  LOAD_CONST               0
              104  COMPARE_OP               ==
              106  POP_JUMP_IF_FALSE   198  'to 198'

 L. 180       108  SETUP_FINALLY       176  'to 176'

 L. 181       110  LOAD_GLOBAL              Dispatch
              112  LOAD_FAST                'arg'
              114  CALL_FUNCTION_1       1  ''
              116  STORE_FAST               'ob'

 L. 183       118  LOAD_FAST                'ob'
              120  LOAD_ATTR                _oleobj_
              122  LOAD_METHOD              GetTypeInfo
              124  CALL_METHOD_0         0  ''
              126  LOAD_METHOD              GetContainingTypeLib
              128  CALL_METHOD_0         0  ''
              130  UNPACK_SEQUENCE_2     2 
              132  STORE_FAST               'tlb'
              134  STORE_FAST               'index'

 L. 184       136  LOAD_GLOBAL              selecttlb
              138  LOAD_METHOD              TypelibSpec
              140  LOAD_CONST               None
              142  LOAD_CONST               0
              144  LOAD_CONST               0
              146  LOAD_CONST               0
              148  CALL_METHOD_4         4  ''
              150  STORE_FAST               'spec'

 L. 185       152  LOAD_FAST                'spec'
              154  LOAD_METHOD              FromTypelib
              156  LOAD_FAST                'tlb'
              158  CALL_METHOD_1         1  ''
              160  POP_TOP          

 L. 186       162  LOAD_FAST                'tlbs'
              164  LOAD_METHOD              append
              166  LOAD_FAST                'spec'
              168  CALL_METHOD_1         1  ''
              170  POP_TOP          
              172  POP_BLOCK        
              174  JUMP_FORWARD        198  'to 198'
            176_0  COME_FROM_FINALLY   108  '108'

 L. 187       176  DUP_TOP          
              178  LOAD_GLOBAL              pythoncom
              180  LOAD_ATTR                com_error
              182  COMPARE_OP               exception-match
              184  POP_JUMP_IF_FALSE   196  'to 196'
              186  POP_TOP          
              188  POP_TOP          
              190  POP_TOP          

 L. 188       192  POP_EXCEPT       
              194  JUMP_FORWARD        198  'to 198'
            196_0  COME_FROM           184  '184'
              196  END_FINALLY      
            198_0  COME_FROM           194  '194'
            198_1  COME_FROM           174  '174'
            198_2  COME_FROM           106  '106'

 L. 189       198  LOAD_GLOBAL              len
              200  LOAD_FAST                'tlbs'
              202  CALL_FUNCTION_1       1  ''
              204  LOAD_CONST               0
              206  COMPARE_OP               ==
              208  POP_JUMP_IF_FALSE   222  'to 222'

 L. 190       210  LOAD_GLOBAL              print
              212  LOAD_STR                 "Could not locate a type library matching '%s'"
              214  LOAD_FAST                'arg'
              216  BINARY_MODULO    
              218  CALL_FUNCTION_1       1  ''
              220  POP_TOP          
            222_0  COME_FROM           208  '208'

 L. 191       222  LOAD_FAST                'tlbs'
              224  GET_ITER         
              226  FOR_ITER            334  'to 334'
              228  STORE_FAST               'spec'

 L. 194       230  LOAD_FAST                'spec'
              232  LOAD_ATTR                dll
              234  LOAD_CONST               None
              236  COMPARE_OP               is
          238_240  POP_JUMP_IF_FALSE   268  'to 268'

 L. 195       242  LOAD_GLOBAL              pythoncom
              244  LOAD_METHOD              LoadRegTypeLib
              246  LOAD_FAST                'spec'
              248  LOAD_ATTR                clsid
              250  LOAD_FAST                'spec'
              252  LOAD_ATTR                major
              254  LOAD_FAST                'spec'
              256  LOAD_ATTR                minor
              258  LOAD_FAST                'spec'
              260  LOAD_ATTR                lcid
              262  CALL_METHOD_4         4  ''
              264  STORE_FAST               'tlb'
              266  JUMP_FORWARD        280  'to 280'
            268_0  COME_FROM           238  '238'

 L. 197       268  LOAD_GLOBAL              pythoncom
              270  LOAD_METHOD              LoadTypeLib
              272  LOAD_FAST                'spec'
              274  LOAD_ATTR                dll
              276  CALL_METHOD_1         1  ''
              278  STORE_FAST               'tlb'
            280_0  COME_FROM           266  '266'

 L. 201       280  LOAD_FAST                'tlb'
              282  LOAD_METHOD              GetLibAttr
              284  CALL_METHOD_0         0  ''
              286  STORE_FAST               'attr'

 L. 202       288  LOAD_FAST                'attr'
              290  LOAD_CONST               3
              292  BINARY_SUBSCR    
              294  LOAD_FAST                'spec'
              296  STORE_ATTR               major

 L. 203       298  LOAD_FAST                'attr'
              300  LOAD_CONST               4
              302  BINARY_SUBSCR    
              304  LOAD_FAST                'spec'
              306  STORE_ATTR               minor

 L. 204       308  LOAD_FAST                'attr'
              310  LOAD_CONST               1
              312  BINARY_SUBSCR    
              314  LOAD_FAST                'spec'
              316  STORE_ATTR               lcid

 L. 205       318  LOAD_FAST                'typelibs'
              320  LOAD_METHOD              append
              322  LOAD_FAST                'tlb'
              324  LOAD_FAST                'spec'
              326  BUILD_TUPLE_2         2 
              328  CALL_METHOD_1         1  ''
              330  POP_TOP          
              332  JUMP_BACK           226  'to 226'
              334  POP_EXCEPT       
              336  JUMP_FORWARD        340  'to 340'
            338_0  COME_FROM            76  '76'
              338  END_FINALLY      
            340_0  COME_FROM           336  '336'
            340_1  COME_FROM            64  '64'

 L. 206       340  LOAD_FAST                'typelibs'
              342  POP_BLOCK        
              344  RETURN_VALUE     
            346_0  COME_FROM_FINALLY     4  '4'

 L. 207       346  DUP_TOP          
              348  LOAD_GLOBAL              pythoncom
              350  LOAD_ATTR                com_error
              352  COMPARE_OP               exception-match
          354_356  POP_JUMP_IF_FALSE   416  'to 416'
              358  POP_TOP          
              360  POP_TOP          
              362  POP_TOP          

 L. 208       364  LOAD_GLOBAL              sys
              366  LOAD_METHOD              exc_info
              368  CALL_METHOD_0         0  ''
              370  UNPACK_SEQUENCE_3     3 
              372  STORE_FAST               't'
              374  STORE_FAST               'v'
              376  STORE_FAST               'tb'

 L. 209       378  LOAD_GLOBAL              sys
              380  LOAD_ATTR                stderr
              382  LOAD_METHOD              write
              384  LOAD_STR                 "Unable to load type library from '%s' - %s\n"
              386  LOAD_FAST                'arg'
              388  LOAD_FAST                'v'
              390  BUILD_TUPLE_2         2 
              392  BINARY_MODULO    
              394  CALL_METHOD_1         1  ''
              396  POP_TOP          

 L. 210       398  LOAD_CONST               None
              400  STORE_FAST               'tb'

 L. 211       402  LOAD_GLOBAL              sys
              404  LOAD_METHOD              exit
              406  LOAD_CONST               1
              408  CALL_METHOD_1         1  ''
              410  POP_TOP          
              412  POP_EXCEPT       
              414  JUMP_FORWARD        418  'to 418'
            416_0  COME_FROM           354  '354'
              416  END_FINALLY      
            418_0  COME_FROM           414  '414'

Parse error at or near `POP_TOP' instruction at offset 360


def GenerateFromTypeLibSpec(typelibInfo, file=None, verboseLevel=None, progressInstance=None, bUnicodeToString=None, bForDemand=bForDemandDefault, bBuildHidden=1):
    if not bUnicodeToString is None:
        raise AssertionError('this is deprecated and will go away')
    elif verboseLevel is None:
        verboseLevel = 0
    elif bForDemand:
        if file is not None:
            raise RuntimeError('You can only perform a demand-build when the output goes to the gen_py directory')
    elif isinstance(typelibInfo, tuple):
        typelibCLSID, lcid, major, minor = typelibInfo
        tlb = pythoncom.LoadRegTypeLib(typelibCLSID, major, minor, lcid)
        spec = selecttlb.TypelibSpec(typelibCLSID, lcid, major, minor)
        spec.FromTypelib(tlb, str(typelibCLSID))
        typelibs = [(tlb, spec)]
    else:
        if isinstance(typelibInfo, selecttlb.TypelibSpec):
            if typelibInfo.dll is None:
                tlb = pythoncom.LoadRegTypeLib(typelibInfo.clsid, typelibInfo.major, typelibInfo.minor, typelibInfo.lcid)
            else:
                tlb = pythoncom.LoadTypeLib(typelibInfo.dll)
            typelibs = [
             (
              tlb, typelibInfo)]
        else:
            if hasattr(typelibInfo, 'GetLibAttr'):
                tla = typelibInfo.GetLibAttr()
                guid = tla[0]
                lcid = tla[1]
                major = tla[3]
                minor = tla[4]
                spec = selecttlb.TypelibSpec(guid, lcid, major, minor)
                typelibs = [(typelibInfo, spec)]
            else:
                typelibs = GetTypeLibsForSpec(typelibInfo)
    if progressInstance is None:
        progressInstance = SimpleProgress(verboseLevel)
    progress = progressInstance
    bToGenDir = file is None
    for typelib, info in typelibs:
        gen = genpy.Generator(typelib, (info.dll), progress, bBuildHidden=bBuildHidden)
        if file is None:
            this_name = gencache.GetGeneratedFileName(info.clsid, info.lcid, info.major, info.minor)
            full_name = os.path.join(gencache.GetGeneratePath(), this_name)
            if bForDemand:
                try:
                    os.unlink(full_name + '.py')
                except os.error:
                    pass
                else:
                    try:
                        os.unlink(full_name + '.pyc')
                    except os.error:
                        pass
                    else:
                        try:
                            os.unlink(full_name + '.pyo')
                        except os.error:
                            pass
                        else:
                            if not os.path.isdir(full_name):
                                os.mkdir(full_name)
                            outputName = os.path.join(full_name, '__init__.py')
            else:
                outputName = full_name + '.py'
            fileUse = gen.open_writer(outputName)
            progress.LogBeginGenerate(outputName)
        else:
            fileUse = file
        worked = False
        try:
            gen.generate(fileUse, bForDemand)
            worked = True
        finally:
            if file is None:
                gen.finish_writer(outputName, fileUse, worked)

        if bToGenDir:
            progress.SetDescription('Importing module')
            gencache.AddModuleToCache(info.clsid, info.lcid, info.major, info.minor)
        progress.Close()


def GenerateChildFromTypeLibSpec(child, typelibInfo, verboseLevel=None, progressInstance=None, bUnicodeToString=None):
    if not bUnicodeToString is None:
        raise AssertionError('this is deprecated and will go away')
    else:
        if verboseLevel is None:
            verboseLevel = 0
        if type(typelibInfo) == type(()):
            typelibCLSID, lcid, major, minor = typelibInfo
            tlb = pythoncom.LoadRegTypeLib(typelibCLSID, major, minor, lcid)
        else:
            tlb = typelibInfo
        tla = typelibInfo.GetLibAttr()
        typelibCLSID = tla[0]
        lcid = tla[1]
        major = tla[3]
        minor = tla[4]
    spec = selecttlb.TypelibSpec(typelibCLSID, lcid, major, minor)
    spec.FromTypelib(tlb, str(typelibCLSID))
    typelibs = [(tlb, spec)]
    if progressInstance is None:
        progressInstance = SimpleProgress(verboseLevel)
    progress = progressInstance
    for typelib, info in typelibs:
        dir_name = gencache.GetGeneratedFileName(info.clsid, info.lcid, info.major, info.minor)
        dir_path_name = os.path.join(gencache.GetGeneratePath(), dir_name)
        progress.LogBeginGenerate(dir_path_name)
        gen = genpy.Generator(typelib, info.dll, progress)
        gen.generate_child(child, dir_path_name)
        progress.SetDescription('Importing module')
        __import__('win32com.gen_py.' + dir_name + '.' + child)
    else:
        progress.Close()


def main():
    import getopt
    hiddenSpec = 1
    outputName = None
    verboseLevel = 1
    doit = 1
    bForDemand = bForDemandDefault
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'vo:huiqd')
        for o, v in opts:
            if o == '-h':
                hiddenSpec = 0
            elif o == '-o':
                outputName = v
            elif o == '-v':
                verboseLevel = verboseLevel + 1
            elif o == '-q':
                verboseLevel = verboseLevel - 1
            elif o == '-i':
                if len(args) == 0:
                    ShowInfo(None)
                else:
                    for arg in args:
                        ShowInfo(arg)

            else:
                doit = 0
        else:
            if o == '-d':
                bForDemand = not bForDemand

    except (getopt.error, error) as msg:
        try:
            sys.stderr.write(str(msg) + '\n')
            usage()
        finally:
            msg = None
            del msg

    else:
        if bForDemand:
            if outputName is not None:
                sys.stderr.write('Can not use -d and -o together\n')
                usage()
        elif not doit:
            return 0
            if len(args) == 0:
                rc = selecttlb.SelectTlb()
                if rc is None:
                    sys.exit(1)
                args = [
                 rc]
            if outputName is not None:
                path = os.path.dirname(outputName)
                if path != '':
                    if not os.path.exists(path):
                        os.makedirs(path)
            elif sys.version_info > (3, 0):
                f = open(outputName, 'wt', encoding='mbcs')
            else:
                import codecs
                f = codecs.open(outputName, 'w', 'mbcs')
        else:
            f = None
    for arg in args:
        GenerateFromTypeLibSpec(arg, f, verboseLevel=verboseLevel, bForDemand=bForDemand, bBuildHidden=hiddenSpec)
    else:
        if f:
            f.close()


if __name__ == '__main__':
    rc = main()
    if rc:
        sys.exit(rc)
    sys.exit(0)