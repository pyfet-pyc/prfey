# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: win32com\client\makepy.py
"""Generate a .py file from an OLE TypeLibrary file.

 This module is concerned only with the actual writing of
 a .py file.  It draws on the @build@ module, which builds
 the knowledge of a COM interface.

"""
usageHelp = ' \nUsage:\n\n  makepy.py [-i] [-v|q] [-h] [-u] [-o output_file] [-d] [typelib, ...]\n\n  -i    -- Show information for the specified typelib.\n\n  -v    -- Verbose output.\n\n  -q    -- Quiet output.\n\n  -h    -- Do not generate hidden methods.\n\n  -u    -- Python 1.5 and earlier: Do NOT convert all Unicode objects to\n           strings.\n\n           Python 1.6 and later: Convert all Unicode objects to strings.\n\n  -o    -- Create output in a specified output file.  If the path leading\n           to the file does not exist, any missing directories will be\n           created.\n           NOTE: -o cannot be used with -d.  This will generate an error.\n\n  -d    -- Generate the base code now and the class code on demand.\n           Recommended for large type libraries.\n\n  typelib -- A TLB, DLL, OCX or anything containing COM type information.\n             If a typelib is not specified, a window containing a textbox\n             will open from which you can select a registered type\n             library.\n\nExamples:\n\n  makepy.py -d\n\n    Presents a list of registered type libraries from which you can make\n    a selection.\n\n  makepy.py -d "Microsoft Excel 8.0 Object Library"\n\n    Generate support for the type library with the specified description\n    (in this case, the MS Excel object model).\n\n'
import sys, os, importlib, pythoncom
from win32com.client import genpy, selecttlb, gencache
from win32com.client import Dispatch
bForDemandDefault = 0
error = 'makepy.error'

def usage():
    sys.stderr.write(usageHelp)
    sys.exit(2)


def ShowInfo--- This code section failed: ---

 L.  82         0  LOAD_FAST                'spec'
                2  POP_JUMP_IF_TRUE    114  'to 114'

 L.  83         4  LOAD_GLOBAL              selecttlb
                6  LOAD_ATTR                SelectTlb
                8  LOAD_GLOBAL              selecttlb
               10  LOAD_ATTR                FLAG_HIDDEN
               12  LOAD_CONST               ('excludeFlags',)
               14  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               16  STORE_FAST               'tlbSpec'

 L.  84        18  LOAD_FAST                'tlbSpec'
               20  LOAD_CONST               None
               22  <117>                 0  ''
               24  POP_JUMP_IF_FALSE    30  'to 30'

 L.  85        26  LOAD_CONST               None
               28  RETURN_VALUE     
             30_0  COME_FROM            24  '24'

 L.  86        30  SETUP_FINALLY        60  'to 60'

 L.  87        32  LOAD_GLOBAL              pythoncom
               34  LOAD_METHOD              LoadRegTypeLib
               36  LOAD_FAST                'tlbSpec'
               38  LOAD_ATTR                clsid
               40  LOAD_FAST                'tlbSpec'
               42  LOAD_ATTR                major
               44  LOAD_FAST                'tlbSpec'
               46  LOAD_ATTR                minor
               48  LOAD_FAST                'tlbSpec'
               50  LOAD_ATTR                lcid
               52  CALL_METHOD_4         4  ''
               54  STORE_FAST               'tlb'
               56  POP_BLOCK        
               58  JUMP_FORWARD        102  'to 102'
             60_0  COME_FROM_FINALLY    30  '30'

 L.  88        60  DUP_TOP          
               62  LOAD_GLOBAL              pythoncom
               64  LOAD_ATTR                com_error
               66  <121>               100  ''
               68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          

 L.  89        74  LOAD_GLOBAL              sys
               76  LOAD_ATTR                stderr
               78  LOAD_METHOD              write
               80  LOAD_STR                 "Warning - could not load registered typelib '%s'\n"
               82  LOAD_FAST                'tlbSpec'
               84  LOAD_ATTR                clsid
               86  BINARY_MODULO    
               88  CALL_METHOD_1         1  ''
               90  POP_TOP          

 L.  90        92  LOAD_CONST               None
               94  STORE_FAST               'tlb'
               96  POP_EXCEPT       
               98  JUMP_FORWARD        102  'to 102'
              100  <48>             
            102_0  COME_FROM            98  '98'
            102_1  COME_FROM            58  '58'

 L.  92       102  LOAD_FAST                'tlb'
              104  LOAD_FAST                'tlbSpec'
              106  BUILD_TUPLE_2         2 
              108  BUILD_LIST_1          1 
              110  STORE_FAST               'infos'
              112  JUMP_FORWARD        122  'to 122'
            114_0  COME_FROM             2  '2'

 L.  94       114  LOAD_GLOBAL              GetTypeLibsForSpec
              116  LOAD_FAST                'spec'
              118  CALL_FUNCTION_1       1  ''
              120  STORE_FAST               'infos'
            122_0  COME_FROM           112  '112'

 L.  95       122  LOAD_FAST                'infos'
              124  GET_ITER         
            126_0  COME_FROM           262  '262'
              126  FOR_ITER            264  'to 264'
              128  UNPACK_SEQUENCE_2     2 
              130  STORE_FAST               'tlb'
              132  STORE_FAST               'tlbSpec'

 L.  96       134  LOAD_FAST                'tlbSpec'
              136  LOAD_ATTR                desc
              138  STORE_FAST               'desc'

 L.  97       140  LOAD_FAST                'desc'
              142  LOAD_CONST               None
              144  <117>                 0  ''
              146  POP_JUMP_IF_FALSE   182  'to 182'

 L.  98       148  LOAD_FAST                'tlb'
              150  LOAD_CONST               None
              152  <117>                 0  ''
              154  POP_JUMP_IF_FALSE   168  'to 168'

 L.  99       156  LOAD_STR                 '<Could not load typelib %s>'
              158  LOAD_FAST                'tlbSpec'
              160  LOAD_ATTR                dll
              162  BINARY_MODULO    
              164  STORE_FAST               'desc'
              166  JUMP_FORWARD        182  'to 182'
            168_0  COME_FROM           154  '154'

 L. 101       168  LOAD_FAST                'tlb'
              170  LOAD_METHOD              GetDocumentation
              172  LOAD_CONST               -1
              174  CALL_METHOD_1         1  ''
              176  LOAD_CONST               0
              178  BINARY_SUBSCR    
              180  STORE_FAST               'desc'
            182_0  COME_FROM           166  '166'
            182_1  COME_FROM           146  '146'

 L. 102       182  LOAD_GLOBAL              print
              184  LOAD_FAST                'desc'
              186  CALL_FUNCTION_1       1  ''
              188  POP_TOP          

 L. 103       190  LOAD_GLOBAL              print
              192  LOAD_STR                 ' %s, lcid=%s, major=%s, minor=%s'
              194  LOAD_FAST                'tlbSpec'
              196  LOAD_ATTR                clsid
              198  LOAD_FAST                'tlbSpec'
              200  LOAD_ATTR                lcid
              202  LOAD_FAST                'tlbSpec'
              204  LOAD_ATTR                major
              206  LOAD_FAST                'tlbSpec'
              208  LOAD_ATTR                minor
              210  BUILD_TUPLE_4         4 
              212  BINARY_MODULO    
              214  CALL_FUNCTION_1       1  ''
              216  POP_TOP          

 L. 104       218  LOAD_GLOBAL              print
              220  LOAD_STR                 ' >>> # Use these commands in Python code to auto generate .py support'
              222  CALL_FUNCTION_1       1  ''
              224  POP_TOP          

 L. 105       226  LOAD_GLOBAL              print
              228  LOAD_STR                 ' >>> from win32com.client import gencache'
              230  CALL_FUNCTION_1       1  ''
              232  POP_TOP          

 L. 106       234  LOAD_GLOBAL              print
              236  LOAD_STR                 " >>> gencache.EnsureModule('%s', %s, %s, %s)"
              238  LOAD_FAST                'tlbSpec'
              240  LOAD_ATTR                clsid
              242  LOAD_FAST                'tlbSpec'
              244  LOAD_ATTR                lcid
              246  LOAD_FAST                'tlbSpec'
              248  LOAD_ATTR                major
              250  LOAD_FAST                'tlbSpec'
              252  LOAD_ATTR                minor
              254  BUILD_TUPLE_4         4 
              256  BINARY_MODULO    
              258  CALL_FUNCTION_1       1  ''
              260  POP_TOP          
              262  JUMP_BACK           126  'to 126'
            264_0  COME_FROM           126  '126'

Parse error at or near `<117>' instruction at offset 22


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

    def Close--- This code section failed: ---

 L. 142         0  LOAD_FAST                'self'
                2  LOAD_ATTR                dialog
                4  LOAD_CONST               None
                6  <117>                 1  ''
                8  POP_JUMP_IF_FALSE    26  'to 26'

 L. 143        10  LOAD_FAST                'self'
               12  LOAD_ATTR                dialog
               14  LOAD_METHOD              Close
               16  CALL_METHOD_0         0  ''
               18  POP_TOP          

 L. 144        20  LOAD_CONST               None
               22  LOAD_FAST                'self'
               24  STORE_ATTR               dialog
             26_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1

    def Starting--- This code section failed: ---

 L. 147         0  LOAD_GLOBAL              SimpleProgress
                2  LOAD_METHOD              Starting
                4  LOAD_FAST                'self'
                6  LOAD_FAST                'tlb_desc'
                8  CALL_METHOD_2         2  ''
               10  POP_TOP          

 L. 148        12  LOAD_FAST                'self'
               14  LOAD_ATTR                dialog
               16  LOAD_CONST               None
               18  <117>                 0  ''
               20  POP_JUMP_IF_FALSE    48  'to 48'

 L. 149        22  LOAD_CONST               0
               24  LOAD_CONST               ('status',)
               26  IMPORT_NAME_ATTR         pywin.dialogs
               28  IMPORT_FROM              status
               30  STORE_FAST               'status'
               32  POP_TOP          

 L. 150        34  LOAD_FAST                'status'
               36  LOAD_METHOD              ThreadedStatusProgressDialog
               38  LOAD_FAST                'tlb_desc'
               40  CALL_METHOD_1         1  ''
               42  LOAD_FAST                'self'
               44  STORE_ATTR               dialog
               46  JUMP_FORWARD         60  'to 60'
             48_0  COME_FROM            20  '20'

 L. 152        48  LOAD_FAST                'self'
               50  LOAD_ATTR                dialog
               52  LOAD_METHOD              SetTitle
               54  LOAD_FAST                'tlb_desc'
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          
             60_0  COME_FROM            46  '46'

Parse error at or near `<117>' instruction at offset 18

    def SetDescription(self, desc, maxticks=None):
        self.dialog.SetText(desc)
        if maxticks:
            self.dialog.SetMaxTicks(maxticks)

    def Tick--- This code section failed: ---

 L. 160         0  LOAD_FAST                'self'
                2  LOAD_ATTR                dialog
                4  LOAD_METHOD              Tick
                6  CALL_METHOD_0         0  ''
                8  POP_TOP          

 L. 161        10  LOAD_FAST                'desc'
               12  LOAD_CONST               None
               14  <117>                 1  ''
               16  POP_JUMP_IF_FALSE    30  'to 30'

 L. 162        18  LOAD_FAST                'self'
               20  LOAD_ATTR                dialog
               22  LOAD_METHOD              SetText
               24  LOAD_FAST                'desc'
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
             30_0  COME_FROM            16  '16'

Parse error at or near `<117>' instruction at offset 14


def GetTypeLibsForSpec--- This code section failed: ---

 L. 168         0  BUILD_LIST_0          0 
                2  STORE_FAST               'typelibs'

 L. 169       4_6  SETUP_FINALLY       342  'to 342'

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
            64_66  JUMP_FORWARD        336  'to 336'
             68_0  COME_FROM_FINALLY     8  '8'

 L. 175        68  DUP_TOP          
               70  LOAD_GLOBAL              pythoncom
               72  LOAD_ATTR                com_error
            74_76  <121>               334  ''
               78  POP_TOP          
               80  POP_TOP          
               82  POP_TOP          

 L. 177        84  LOAD_GLOBAL              selecttlb
               86  LOAD_METHOD              FindTlbsWithDescription
               88  LOAD_FAST                'arg'
               90  CALL_METHOD_1         1  ''
               92  STORE_FAST               'tlbs'

 L. 178        94  LOAD_GLOBAL              len
               96  LOAD_FAST                'tlbs'
               98  CALL_FUNCTION_1       1  ''
              100  LOAD_CONST               0
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_FALSE   194  'to 194'

 L. 180       106  SETUP_FINALLY       174  'to 174'

 L. 181       108  LOAD_GLOBAL              Dispatch
              110  LOAD_FAST                'arg'
              112  CALL_FUNCTION_1       1  ''
              114  STORE_FAST               'ob'

 L. 183       116  LOAD_FAST                'ob'
              118  LOAD_ATTR                _oleobj_
              120  LOAD_METHOD              GetTypeInfo
              122  CALL_METHOD_0         0  ''
              124  LOAD_METHOD              GetContainingTypeLib
              126  CALL_METHOD_0         0  ''
              128  UNPACK_SEQUENCE_2     2 
              130  STORE_FAST               'tlb'
              132  STORE_FAST               'index'

 L. 184       134  LOAD_GLOBAL              selecttlb
              136  LOAD_METHOD              TypelibSpec
              138  LOAD_CONST               None
              140  LOAD_CONST               0
              142  LOAD_CONST               0
              144  LOAD_CONST               0
              146  CALL_METHOD_4         4  ''
              148  STORE_FAST               'spec'

 L. 185       150  LOAD_FAST                'spec'
              152  LOAD_METHOD              FromTypelib
              154  LOAD_FAST                'tlb'
              156  CALL_METHOD_1         1  ''
              158  POP_TOP          

 L. 186       160  LOAD_FAST                'tlbs'
              162  LOAD_METHOD              append
              164  LOAD_FAST                'spec'
              166  CALL_METHOD_1         1  ''
              168  POP_TOP          
              170  POP_BLOCK        
              172  JUMP_FORWARD        194  'to 194'
            174_0  COME_FROM_FINALLY   106  '106'

 L. 187       174  DUP_TOP          
              176  LOAD_GLOBAL              pythoncom
              178  LOAD_ATTR                com_error
              180  <121>               192  ''
              182  POP_TOP          
              184  POP_TOP          
              186  POP_TOP          

 L. 188       188  POP_EXCEPT       
              190  JUMP_FORWARD        194  'to 194'
              192  <48>             
            194_0  COME_FROM           190  '190'
            194_1  COME_FROM           172  '172'
            194_2  COME_FROM           104  '104'

 L. 189       194  LOAD_GLOBAL              len
              196  LOAD_FAST                'tlbs'
              198  CALL_FUNCTION_1       1  ''
              200  LOAD_CONST               0
              202  COMPARE_OP               ==
              204  POP_JUMP_IF_FALSE   218  'to 218'

 L. 190       206  LOAD_GLOBAL              print
              208  LOAD_STR                 "Could not locate a type library matching '%s'"
              210  LOAD_FAST                'arg'
              212  BINARY_MODULO    
              214  CALL_FUNCTION_1       1  ''
              216  POP_TOP          
            218_0  COME_FROM           204  '204'

 L. 191       218  LOAD_FAST                'tlbs'
              220  GET_ITER         
            222_0  COME_FROM           328  '328'
              222  FOR_ITER            330  'to 330'
              224  STORE_FAST               'spec'

 L. 194       226  LOAD_FAST                'spec'
              228  LOAD_ATTR                dll
              230  LOAD_CONST               None
              232  <117>                 0  ''
          234_236  POP_JUMP_IF_FALSE   264  'to 264'

 L. 195       238  LOAD_GLOBAL              pythoncom
              240  LOAD_METHOD              LoadRegTypeLib
              242  LOAD_FAST                'spec'
              244  LOAD_ATTR                clsid
              246  LOAD_FAST                'spec'
              248  LOAD_ATTR                major
              250  LOAD_FAST                'spec'
              252  LOAD_ATTR                minor
              254  LOAD_FAST                'spec'
              256  LOAD_ATTR                lcid
              258  CALL_METHOD_4         4  ''
              260  STORE_FAST               'tlb'
              262  JUMP_FORWARD        276  'to 276'
            264_0  COME_FROM           234  '234'

 L. 197       264  LOAD_GLOBAL              pythoncom
              266  LOAD_METHOD              LoadTypeLib
              268  LOAD_FAST                'spec'
              270  LOAD_ATTR                dll
              272  CALL_METHOD_1         1  ''
              274  STORE_FAST               'tlb'
            276_0  COME_FROM           262  '262'

 L. 201       276  LOAD_FAST                'tlb'
              278  LOAD_METHOD              GetLibAttr
              280  CALL_METHOD_0         0  ''
              282  STORE_FAST               'attr'

 L. 202       284  LOAD_FAST                'attr'
              286  LOAD_CONST               3
              288  BINARY_SUBSCR    
              290  LOAD_FAST                'spec'
              292  STORE_ATTR               major

 L. 203       294  LOAD_FAST                'attr'
              296  LOAD_CONST               4
              298  BINARY_SUBSCR    
              300  LOAD_FAST                'spec'
              302  STORE_ATTR               minor

 L. 204       304  LOAD_FAST                'attr'
              306  LOAD_CONST               1
              308  BINARY_SUBSCR    
              310  LOAD_FAST                'spec'
              312  STORE_ATTR               lcid

 L. 205       314  LOAD_FAST                'typelibs'
              316  LOAD_METHOD              append
              318  LOAD_FAST                'tlb'
              320  LOAD_FAST                'spec'
              322  BUILD_TUPLE_2         2 
              324  CALL_METHOD_1         1  ''
              326  POP_TOP          
              328  JUMP_BACK           222  'to 222'
            330_0  COME_FROM           222  '222'
              330  POP_EXCEPT       
              332  JUMP_FORWARD        336  'to 336'
              334  <48>             
            336_0  COME_FROM           332  '332'
            336_1  COME_FROM            64  '64'

 L. 206       336  LOAD_FAST                'typelibs'
              338  POP_BLOCK        
              340  RETURN_VALUE     
            342_0  COME_FROM_FINALLY     4  '4'

 L. 207       342  DUP_TOP          
              344  LOAD_GLOBAL              pythoncom
              346  LOAD_ATTR                com_error
          348_350  <121>               410  ''
              352  POP_TOP          
              354  POP_TOP          
              356  POP_TOP          

 L. 208       358  LOAD_GLOBAL              sys
              360  LOAD_METHOD              exc_info
              362  CALL_METHOD_0         0  ''
              364  UNPACK_SEQUENCE_3     3 
              366  STORE_FAST               't'
              368  STORE_FAST               'v'
              370  STORE_FAST               'tb'

 L. 209       372  LOAD_GLOBAL              sys
              374  LOAD_ATTR                stderr
              376  LOAD_METHOD              write
              378  LOAD_STR                 "Unable to load type library from '%s' - %s\n"
              380  LOAD_FAST                'arg'
              382  LOAD_FAST                'v'
              384  BUILD_TUPLE_2         2 
              386  BINARY_MODULO    
              388  CALL_METHOD_1         1  ''
              390  POP_TOP          

 L. 210       392  LOAD_CONST               None
              394  STORE_FAST               'tb'

 L. 211       396  LOAD_GLOBAL              sys
              398  LOAD_METHOD              exit
              400  LOAD_CONST               1
              402  CALL_METHOD_1         1  ''
              404  POP_TOP          
              406  POP_EXCEPT       
              408  JUMP_FORWARD        412  'to 412'
              410  <48>             
            412_0  COME_FROM           408  '408'

Parse error at or near `<121>' instruction at offset 74_76


def GenerateFromTypeLibSpec--- This code section failed: ---

 L. 214         0  LOAD_FAST                'bUnicodeToString'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_TRUE     16  'to 16'
                8  <74>             
               10  LOAD_STR                 'this is deprecated and will go away'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 215        16  LOAD_FAST                'verboseLevel'
               18  LOAD_CONST               None
               20  <117>                 0  ''
               22  POP_JUMP_IF_FALSE    28  'to 28'

 L. 216        24  LOAD_CONST               0
               26  STORE_FAST               'verboseLevel'
             28_0  COME_FROM            22  '22'

 L. 218        28  LOAD_FAST                'bForDemand'
               30  POP_JUMP_IF_FALSE    48  'to 48'
               32  LOAD_FAST                'file'
               34  LOAD_CONST               None
               36  <117>                 1  ''
               38  POP_JUMP_IF_FALSE    48  'to 48'

 L. 219        40  LOAD_GLOBAL              RuntimeError
               42  LOAD_STR                 'You can only perform a demand-build when the output goes to the gen_py directory'
               44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            38  '38'
             48_1  COME_FROM            30  '30'

 L. 220        48  LOAD_GLOBAL              isinstance
               50  LOAD_FAST                'typelibInfo'
               52  LOAD_GLOBAL              tuple
               54  CALL_FUNCTION_2       2  ''
               56  POP_JUMP_IF_FALSE   130  'to 130'

 L. 222        58  LOAD_FAST                'typelibInfo'
               60  UNPACK_SEQUENCE_4     4 
               62  STORE_FAST               'typelibCLSID'
               64  STORE_FAST               'lcid'
               66  STORE_FAST               'major'
               68  STORE_FAST               'minor'

 L. 223        70  LOAD_GLOBAL              pythoncom
               72  LOAD_METHOD              LoadRegTypeLib
               74  LOAD_FAST                'typelibCLSID'
               76  LOAD_FAST                'major'
               78  LOAD_FAST                'minor'
               80  LOAD_FAST                'lcid'
               82  CALL_METHOD_4         4  ''
               84  STORE_FAST               'tlb'

 L. 224        86  LOAD_GLOBAL              selecttlb
               88  LOAD_METHOD              TypelibSpec
               90  LOAD_FAST                'typelibCLSID'
               92  LOAD_FAST                'lcid'
               94  LOAD_FAST                'major'
               96  LOAD_FAST                'minor'
               98  CALL_METHOD_4         4  ''
              100  STORE_FAST               'spec'

 L. 225       102  LOAD_FAST                'spec'
              104  LOAD_METHOD              FromTypelib
              106  LOAD_FAST                'tlb'
              108  LOAD_GLOBAL              str
              110  LOAD_FAST                'typelibCLSID'
              112  CALL_FUNCTION_1       1  ''
              114  CALL_METHOD_2         2  ''
              116  POP_TOP          

 L. 226       118  LOAD_FAST                'tlb'
              120  LOAD_FAST                'spec'
              122  BUILD_TUPLE_2         2 
              124  BUILD_LIST_1          1 
              126  STORE_FAST               'typelibs'
              128  JUMP_FORWARD        290  'to 290'
            130_0  COME_FROM            56  '56'

 L. 227       130  LOAD_GLOBAL              isinstance
              132  LOAD_FAST                'typelibInfo'
              134  LOAD_GLOBAL              selecttlb
              136  LOAD_ATTR                TypelibSpec
              138  CALL_FUNCTION_2       2  ''
              140  POP_JUMP_IF_FALSE   202  'to 202'

 L. 228       142  LOAD_FAST                'typelibInfo'
              144  LOAD_ATTR                dll
              146  LOAD_CONST               None
              148  <117>                 0  ''
              150  POP_JUMP_IF_FALSE   178  'to 178'

 L. 230       152  LOAD_GLOBAL              pythoncom
              154  LOAD_METHOD              LoadRegTypeLib
              156  LOAD_FAST                'typelibInfo'
              158  LOAD_ATTR                clsid
              160  LOAD_FAST                'typelibInfo'
              162  LOAD_ATTR                major
              164  LOAD_FAST                'typelibInfo'
              166  LOAD_ATTR                minor
              168  LOAD_FAST                'typelibInfo'
              170  LOAD_ATTR                lcid
              172  CALL_METHOD_4         4  ''
              174  STORE_FAST               'tlb'
              176  JUMP_FORWARD        190  'to 190'
            178_0  COME_FROM           150  '150'

 L. 232       178  LOAD_GLOBAL              pythoncom
              180  LOAD_METHOD              LoadTypeLib
              182  LOAD_FAST                'typelibInfo'
              184  LOAD_ATTR                dll
              186  CALL_METHOD_1         1  ''
              188  STORE_FAST               'tlb'
            190_0  COME_FROM           176  '176'

 L. 233       190  LOAD_FAST                'tlb'
              192  LOAD_FAST                'typelibInfo'
              194  BUILD_TUPLE_2         2 
              196  BUILD_LIST_1          1 
              198  STORE_FAST               'typelibs'
              200  JUMP_FORWARD        290  'to 290'
            202_0  COME_FROM           140  '140'

 L. 234       202  LOAD_GLOBAL              hasattr
              204  LOAD_FAST                'typelibInfo'
              206  LOAD_STR                 'GetLibAttr'
              208  CALL_FUNCTION_2       2  ''
          210_212  POP_JUMP_IF_FALSE   282  'to 282'

 L. 238       214  LOAD_FAST                'typelibInfo'
              216  LOAD_METHOD              GetLibAttr
              218  CALL_METHOD_0         0  ''
              220  STORE_FAST               'tla'

 L. 239       222  LOAD_FAST                'tla'
              224  LOAD_CONST               0
              226  BINARY_SUBSCR    
              228  STORE_FAST               'guid'

 L. 240       230  LOAD_FAST                'tla'
              232  LOAD_CONST               1
              234  BINARY_SUBSCR    
              236  STORE_FAST               'lcid'

 L. 241       238  LOAD_FAST                'tla'
              240  LOAD_CONST               3
              242  BINARY_SUBSCR    
              244  STORE_FAST               'major'

 L. 242       246  LOAD_FAST                'tla'
              248  LOAD_CONST               4
              250  BINARY_SUBSCR    
              252  STORE_FAST               'minor'

 L. 243       254  LOAD_GLOBAL              selecttlb
              256  LOAD_METHOD              TypelibSpec
              258  LOAD_FAST                'guid'
              260  LOAD_FAST                'lcid'
              262  LOAD_FAST                'major'
              264  LOAD_FAST                'minor'
              266  CALL_METHOD_4         4  ''
              268  STORE_FAST               'spec'

 L. 244       270  LOAD_FAST                'typelibInfo'
              272  LOAD_FAST                'spec'
              274  BUILD_TUPLE_2         2 
              276  BUILD_LIST_1          1 
              278  STORE_FAST               'typelibs'
              280  JUMP_FORWARD        290  'to 290'
            282_0  COME_FROM           210  '210'

 L. 246       282  LOAD_GLOBAL              GetTypeLibsForSpec
              284  LOAD_FAST                'typelibInfo'
              286  CALL_FUNCTION_1       1  ''
              288  STORE_FAST               'typelibs'
            290_0  COME_FROM           280  '280'
            290_1  COME_FROM           200  '200'
            290_2  COME_FROM           128  '128'

 L. 248       290  LOAD_FAST                'progressInstance'
              292  LOAD_CONST               None
              294  <117>                 0  ''
          296_298  POP_JUMP_IF_FALSE   308  'to 308'

 L. 249       300  LOAD_GLOBAL              SimpleProgress
              302  LOAD_FAST                'verboseLevel'
              304  CALL_FUNCTION_1       1  ''
              306  STORE_FAST               'progressInstance'
            308_0  COME_FROM           296  '296'

 L. 250       308  LOAD_FAST                'progressInstance'
              310  STORE_FAST               'progress'

 L. 252       312  LOAD_FAST                'file'
              314  LOAD_CONST               None
              316  <117>                 0  ''
              318  STORE_FAST               'bToGenDir'

 L. 254       320  LOAD_FAST                'typelibs'
              322  GET_ITER         
            324_0  COME_FROM           736  '736'
            324_1  COME_FROM           698  '698'
          324_326  FOR_ITER            740  'to 740'
              328  UNPACK_SEQUENCE_2     2 
              330  STORE_FAST               'typelib'
              332  STORE_FAST               'info'

 L. 255       334  LOAD_GLOBAL              genpy
              336  LOAD_ATTR                Generator
              338  LOAD_FAST                'typelib'
              340  LOAD_FAST                'info'
              342  LOAD_ATTR                dll
              344  LOAD_FAST                'progress'
              346  LOAD_FAST                'bBuildHidden'
              348  LOAD_CONST               ('bBuildHidden',)
              350  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              352  STORE_FAST               'gen'

 L. 257       354  LOAD_FAST                'file'
              356  LOAD_CONST               None
              358  <117>                 0  ''
          360_362  POP_JUMP_IF_FALSE   608  'to 608'

 L. 258       364  LOAD_GLOBAL              gencache
              366  LOAD_METHOD              GetGeneratedFileName
              368  LOAD_FAST                'info'
              370  LOAD_ATTR                clsid
              372  LOAD_FAST                'info'
              374  LOAD_ATTR                lcid
              376  LOAD_FAST                'info'
              378  LOAD_ATTR                major
              380  LOAD_FAST                'info'
              382  LOAD_ATTR                minor
              384  CALL_METHOD_4         4  ''
              386  STORE_FAST               'this_name'

 L. 259       388  LOAD_GLOBAL              os
              390  LOAD_ATTR                path
              392  LOAD_METHOD              join
              394  LOAD_GLOBAL              gencache
              396  LOAD_METHOD              GetGeneratePath
              398  CALL_METHOD_0         0  ''
              400  LOAD_FAST                'this_name'
              402  CALL_METHOD_2         2  ''
              404  STORE_FAST               'full_name'

 L. 260       406  LOAD_FAST                'bForDemand'
          408_410  POP_JUMP_IF_FALSE   578  'to 578'

 L. 261       412  SETUP_FINALLY       432  'to 432'
              414  LOAD_GLOBAL              os
              416  LOAD_METHOD              unlink
              418  LOAD_FAST                'full_name'
              420  LOAD_STR                 '.py'
              422  BINARY_ADD       
              424  CALL_METHOD_1         1  ''
              426  POP_TOP          
              428  POP_BLOCK        
              430  JUMP_FORWARD        454  'to 454'
            432_0  COME_FROM_FINALLY   412  '412'

 L. 262       432  DUP_TOP          
              434  LOAD_GLOBAL              os
              436  LOAD_ATTR                error
          438_440  <121>               452  ''
              442  POP_TOP          
              444  POP_TOP          
              446  POP_TOP          
              448  POP_EXCEPT       
              450  JUMP_FORWARD        454  'to 454'
              452  <48>             
            454_0  COME_FROM           450  '450'
            454_1  COME_FROM           430  '430'

 L. 263       454  SETUP_FINALLY       474  'to 474'
              456  LOAD_GLOBAL              os
              458  LOAD_METHOD              unlink
              460  LOAD_FAST                'full_name'
              462  LOAD_STR                 '.pyc'
              464  BINARY_ADD       
              466  CALL_METHOD_1         1  ''
              468  POP_TOP          
              470  POP_BLOCK        
              472  JUMP_FORWARD        496  'to 496'
            474_0  COME_FROM_FINALLY   454  '454'

 L. 264       474  DUP_TOP          
              476  LOAD_GLOBAL              os
              478  LOAD_ATTR                error
          480_482  <121>               494  ''
              484  POP_TOP          
              486  POP_TOP          
              488  POP_TOP          
              490  POP_EXCEPT       
              492  JUMP_FORWARD        496  'to 496'
              494  <48>             
            496_0  COME_FROM           492  '492'
            496_1  COME_FROM           472  '472'

 L. 265       496  SETUP_FINALLY       516  'to 516'
              498  LOAD_GLOBAL              os
              500  LOAD_METHOD              unlink
              502  LOAD_FAST                'full_name'
              504  LOAD_STR                 '.pyo'
              506  BINARY_ADD       
              508  CALL_METHOD_1         1  ''
              510  POP_TOP          
              512  POP_BLOCK        
              514  JUMP_FORWARD        538  'to 538'
            516_0  COME_FROM_FINALLY   496  '496'

 L. 266       516  DUP_TOP          
              518  LOAD_GLOBAL              os
              520  LOAD_ATTR                error
          522_524  <121>               536  ''
              526  POP_TOP          
              528  POP_TOP          
              530  POP_TOP          
              532  POP_EXCEPT       
              534  JUMP_FORWARD        538  'to 538'
              536  <48>             
            538_0  COME_FROM           534  '534'
            538_1  COME_FROM           514  '514'

 L. 267       538  LOAD_GLOBAL              os
              540  LOAD_ATTR                path
              542  LOAD_METHOD              isdir
              544  LOAD_FAST                'full_name'
              546  CALL_METHOD_1         1  ''
          548_550  POP_JUMP_IF_TRUE    562  'to 562'

 L. 268       552  LOAD_GLOBAL              os
              554  LOAD_METHOD              mkdir
              556  LOAD_FAST                'full_name'
              558  CALL_METHOD_1         1  ''
              560  POP_TOP          
            562_0  COME_FROM           548  '548'

 L. 269       562  LOAD_GLOBAL              os
              564  LOAD_ATTR                path
              566  LOAD_METHOD              join
              568  LOAD_FAST                'full_name'
              570  LOAD_STR                 '__init__.py'
              572  CALL_METHOD_2         2  ''
              574  STORE_FAST               'outputName'
              576  JUMP_FORWARD        586  'to 586'
            578_0  COME_FROM           408  '408'

 L. 271       578  LOAD_FAST                'full_name'
              580  LOAD_STR                 '.py'
              582  BINARY_ADD       
              584  STORE_FAST               'outputName'
            586_0  COME_FROM           576  '576'

 L. 272       586  LOAD_FAST                'gen'
              588  LOAD_METHOD              open_writer
              590  LOAD_FAST                'outputName'
              592  CALL_METHOD_1         1  ''
              594  STORE_FAST               'fileUse'

 L. 273       596  LOAD_FAST                'progress'
              598  LOAD_METHOD              LogBeginGenerate
              600  LOAD_FAST                'outputName'
              602  CALL_METHOD_1         1  ''
              604  POP_TOP          
              606  JUMP_FORWARD        612  'to 612'
            608_0  COME_FROM           360  '360'

 L. 275       608  LOAD_FAST                'file'
              610  STORE_FAST               'fileUse'
            612_0  COME_FROM           606  '606'

 L. 277       612  LOAD_CONST               False
              614  STORE_FAST               'worked'

 L. 278       616  SETUP_FINALLY       662  'to 662'

 L. 279       618  LOAD_FAST                'gen'
              620  LOAD_METHOD              generate
              622  LOAD_FAST                'fileUse'
              624  LOAD_FAST                'bForDemand'
              626  CALL_METHOD_2         2  ''
              628  POP_TOP          

 L. 280       630  LOAD_CONST               True
              632  STORE_FAST               'worked'
              634  POP_BLOCK        

 L. 282       636  LOAD_FAST                'file'
              638  LOAD_CONST               None
              640  <117>                 0  ''
          642_644  POP_JUMP_IF_FALSE   688  'to 688'

 L. 283       646  LOAD_FAST                'gen'
              648  LOAD_METHOD              finish_writer
              650  LOAD_FAST                'outputName'
              652  LOAD_FAST                'fileUse'
              654  LOAD_FAST                'worked'
              656  CALL_METHOD_3         3  ''
              658  POP_TOP          
              660  JUMP_FORWARD        688  'to 688'
            662_0  COME_FROM_FINALLY   616  '616'

 L. 282       662  LOAD_FAST                'file'
              664  LOAD_CONST               None
              666  <117>                 0  ''
          668_670  POP_JUMP_IF_FALSE   686  'to 686'

 L. 283       672  LOAD_FAST                'gen'
              674  LOAD_METHOD              finish_writer
              676  LOAD_FAST                'outputName'
              678  LOAD_FAST                'fileUse'
              680  LOAD_FAST                'worked'
              682  CALL_METHOD_3         3  ''
              684  POP_TOP          
            686_0  COME_FROM           668  '668'
              686  <48>             
            688_0  COME_FROM           660  '660'
            688_1  COME_FROM           642  '642'

 L. 284       688  LOAD_GLOBAL              importlib
              690  LOAD_METHOD              invalidate_caches
              692  CALL_METHOD_0         0  ''
              694  POP_TOP          

 L. 285       696  LOAD_FAST                'bToGenDir'
          698_700  POP_JUMP_IF_FALSE_BACK   324  'to 324'

 L. 286       702  LOAD_FAST                'progress'
              704  LOAD_METHOD              SetDescription
              706  LOAD_STR                 'Importing module'
              708  CALL_METHOD_1         1  ''
              710  POP_TOP          

 L. 287       712  LOAD_GLOBAL              gencache
              714  LOAD_METHOD              AddModuleToCache
              716  LOAD_FAST                'info'
              718  LOAD_ATTR                clsid
              720  LOAD_FAST                'info'
              722  LOAD_ATTR                lcid
              724  LOAD_FAST                'info'
              726  LOAD_ATTR                major
              728  LOAD_FAST                'info'
              730  LOAD_ATTR                minor
              732  CALL_METHOD_4         4  ''
              734  POP_TOP          
          736_738  JUMP_BACK           324  'to 324'
            740_0  COME_FROM           324  '324'

 L. 289       740  LOAD_FAST                'progress'
              742  LOAD_METHOD              Close
              744  CALL_METHOD_0         0  ''
              746  POP_TOP          

Parse error at or near `None' instruction at offset -1


def GenerateChildFromTypeLibSpec--- This code section failed: ---

 L. 292         0  LOAD_FAST                'bUnicodeToString'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_TRUE     16  'to 16'
                8  <74>             
               10  LOAD_STR                 'this is deprecated and will go away'
               12  CALL_FUNCTION_1       1  ''
               14  RAISE_VARARGS_1       1  'exception instance'
             16_0  COME_FROM             6  '6'

 L. 293        16  LOAD_FAST                'verboseLevel'
               18  LOAD_CONST               None
               20  <117>                 0  ''
               22  POP_JUMP_IF_FALSE    28  'to 28'

 L. 294        24  LOAD_CONST               0
               26  STORE_FAST               'verboseLevel'
             28_0  COME_FROM            22  '22'

 L. 295        28  LOAD_GLOBAL              type
               30  LOAD_FAST                'typelibInfo'
               32  CALL_FUNCTION_1       1  ''
               34  LOAD_GLOBAL              type
               36  LOAD_CONST               ()
               38  CALL_FUNCTION_1       1  ''
               40  COMPARE_OP               ==
               42  POP_JUMP_IF_FALSE    74  'to 74'

 L. 296        44  LOAD_FAST                'typelibInfo'
               46  UNPACK_SEQUENCE_4     4 
               48  STORE_FAST               'typelibCLSID'
               50  STORE_FAST               'lcid'
               52  STORE_FAST               'major'
               54  STORE_FAST               'minor'

 L. 297        56  LOAD_GLOBAL              pythoncom
               58  LOAD_METHOD              LoadRegTypeLib
               60  LOAD_FAST                'typelibCLSID'
               62  LOAD_FAST                'major'
               64  LOAD_FAST                'minor'
               66  LOAD_FAST                'lcid'
               68  CALL_METHOD_4         4  ''
               70  STORE_FAST               'tlb'
               72  JUMP_FORWARD        118  'to 118'
             74_0  COME_FROM            42  '42'

 L. 299        74  LOAD_FAST                'typelibInfo'
               76  STORE_FAST               'tlb'

 L. 300        78  LOAD_FAST                'typelibInfo'
               80  LOAD_METHOD              GetLibAttr
               82  CALL_METHOD_0         0  ''
               84  STORE_FAST               'tla'

 L. 301        86  LOAD_FAST                'tla'
               88  LOAD_CONST               0
               90  BINARY_SUBSCR    
               92  STORE_FAST               'typelibCLSID'

 L. 302        94  LOAD_FAST                'tla'
               96  LOAD_CONST               1
               98  BINARY_SUBSCR    
              100  STORE_FAST               'lcid'

 L. 303       102  LOAD_FAST                'tla'
              104  LOAD_CONST               3
              106  BINARY_SUBSCR    
              108  STORE_FAST               'major'

 L. 304       110  LOAD_FAST                'tla'
              112  LOAD_CONST               4
              114  BINARY_SUBSCR    
              116  STORE_FAST               'minor'
            118_0  COME_FROM            72  '72'

 L. 305       118  LOAD_GLOBAL              selecttlb
              120  LOAD_METHOD              TypelibSpec
              122  LOAD_FAST                'typelibCLSID'
              124  LOAD_FAST                'lcid'
              126  LOAD_FAST                'major'
              128  LOAD_FAST                'minor'
              130  CALL_METHOD_4         4  ''
              132  STORE_FAST               'spec'

 L. 306       134  LOAD_FAST                'spec'
              136  LOAD_METHOD              FromTypelib
              138  LOAD_FAST                'tlb'
              140  LOAD_GLOBAL              str
              142  LOAD_FAST                'typelibCLSID'
              144  CALL_FUNCTION_1       1  ''
              146  CALL_METHOD_2         2  ''
              148  POP_TOP          

 L. 307       150  LOAD_FAST                'tlb'
              152  LOAD_FAST                'spec'
              154  BUILD_TUPLE_2         2 
              156  BUILD_LIST_1          1 
              158  STORE_FAST               'typelibs'

 L. 309       160  LOAD_FAST                'progressInstance'
              162  LOAD_CONST               None
              164  <117>                 0  ''
              166  POP_JUMP_IF_FALSE   176  'to 176'

 L. 310       168  LOAD_GLOBAL              SimpleProgress
              170  LOAD_FAST                'verboseLevel'
              172  CALL_FUNCTION_1       1  ''
              174  STORE_FAST               'progressInstance'
            176_0  COME_FROM           166  '166'

 L. 311       176  LOAD_FAST                'progressInstance'
              178  STORE_FAST               'progress'

 L. 313       180  LOAD_FAST                'typelibs'
              182  GET_ITER         
            184_0  COME_FROM           310  '310'
              184  FOR_ITER            312  'to 312'
              186  UNPACK_SEQUENCE_2     2 
              188  STORE_FAST               'typelib'
              190  STORE_FAST               'info'

 L. 314       192  LOAD_GLOBAL              gencache
              194  LOAD_METHOD              GetGeneratedFileName
              196  LOAD_FAST                'info'
              198  LOAD_ATTR                clsid
              200  LOAD_FAST                'info'
              202  LOAD_ATTR                lcid
              204  LOAD_FAST                'info'
              206  LOAD_ATTR                major
              208  LOAD_FAST                'info'
              210  LOAD_ATTR                minor
              212  CALL_METHOD_4         4  ''
              214  STORE_FAST               'dir_name'

 L. 315       216  LOAD_GLOBAL              os
              218  LOAD_ATTR                path
              220  LOAD_METHOD              join
              222  LOAD_GLOBAL              gencache
              224  LOAD_METHOD              GetGeneratePath
              226  CALL_METHOD_0         0  ''
              228  LOAD_FAST                'dir_name'
              230  CALL_METHOD_2         2  ''
              232  STORE_FAST               'dir_path_name'

 L. 316       234  LOAD_FAST                'progress'
              236  LOAD_METHOD              LogBeginGenerate
              238  LOAD_FAST                'dir_path_name'
              240  CALL_METHOD_1         1  ''
              242  POP_TOP          

 L. 318       244  LOAD_GLOBAL              genpy
              246  LOAD_METHOD              Generator
              248  LOAD_FAST                'typelib'
              250  LOAD_FAST                'info'
              252  LOAD_ATTR                dll
              254  LOAD_FAST                'progress'
              256  CALL_METHOD_3         3  ''
              258  STORE_FAST               'gen'

 L. 319       260  LOAD_FAST                'gen'
              262  LOAD_METHOD              generate_child
              264  LOAD_FAST                'child'
              266  LOAD_FAST                'dir_path_name'
              268  CALL_METHOD_2         2  ''
              270  POP_TOP          

 L. 320       272  LOAD_FAST                'progress'
              274  LOAD_METHOD              SetDescription
              276  LOAD_STR                 'Importing module'
              278  CALL_METHOD_1         1  ''
              280  POP_TOP          

 L. 321       282  LOAD_GLOBAL              importlib
              284  LOAD_METHOD              invalidate_caches
              286  CALL_METHOD_0         0  ''
              288  POP_TOP          

 L. 322       290  LOAD_GLOBAL              __import__
              292  LOAD_STR                 'win32com.gen_py.'
              294  LOAD_FAST                'dir_name'
              296  BINARY_ADD       
              298  LOAD_STR                 '.'
              300  BINARY_ADD       
              302  LOAD_FAST                'child'
              304  BINARY_ADD       
              306  CALL_FUNCTION_1       1  ''
              308  POP_TOP          
              310  JUMP_BACK           184  'to 184'
            312_0  COME_FROM           184  '184'

 L. 323       312  LOAD_FAST                'progress'
              314  LOAD_METHOD              Close
              316  CALL_METHOD_0         0  ''
              318  POP_TOP          

Parse error at or near `None' instruction at offset -1


def main--- This code section failed: ---

 L. 326         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              getopt
                6  STORE_FAST               'getopt'

 L. 327         8  LOAD_CONST               1
               10  STORE_FAST               'hiddenSpec'

 L. 328        12  LOAD_CONST               None
               14  STORE_FAST               'outputName'

 L. 329        16  LOAD_CONST               1
               18  STORE_FAST               'verboseLevel'

 L. 330        20  LOAD_CONST               1
               22  STORE_FAST               'doit'

 L. 331        24  LOAD_GLOBAL              bForDemandDefault
               26  STORE_FAST               'bForDemand'

 L. 332        28  SETUP_FINALLY       206  'to 206'

 L. 333        30  LOAD_FAST                'getopt'
               32  LOAD_METHOD              getopt
               34  LOAD_GLOBAL              sys
               36  LOAD_ATTR                argv
               38  LOAD_CONST               1
               40  LOAD_CONST               None
               42  BUILD_SLICE_2         2 
               44  BINARY_SUBSCR    
               46  LOAD_STR                 'vo:huiqd'
               48  CALL_METHOD_2         2  ''
               50  UNPACK_SEQUENCE_2     2 
               52  STORE_FAST               'opts'
               54  STORE_FAST               'args'

 L. 334        56  LOAD_FAST                'opts'
               58  GET_ITER         
             60_0  COME_FROM           200  '200'
             60_1  COME_FROM           192  '192'
             60_2  COME_FROM           184  '184'
             60_3  COME_FROM           130  '130'
             60_4  COME_FROM           112  '112'
             60_5  COME_FROM            94  '94'
             60_6  COME_FROM            80  '80'
               60  FOR_ITER            202  'to 202'
               62  UNPACK_SEQUENCE_2     2 
               64  STORE_FAST               'o'
               66  STORE_FAST               'v'

 L. 335        68  LOAD_FAST                'o'
               70  LOAD_STR                 '-h'
               72  COMPARE_OP               ==
               74  POP_JUMP_IF_FALSE    82  'to 82'

 L. 336        76  LOAD_CONST               0
               78  STORE_FAST               'hiddenSpec'
               80  JUMP_BACK            60  'to 60'
             82_0  COME_FROM            74  '74'

 L. 337        82  LOAD_FAST                'o'
               84  LOAD_STR                 '-o'
               86  COMPARE_OP               ==
               88  POP_JUMP_IF_FALSE    96  'to 96'

 L. 338        90  LOAD_FAST                'v'
               92  STORE_FAST               'outputName'
               94  JUMP_BACK            60  'to 60'
             96_0  COME_FROM            88  '88'

 L. 339        96  LOAD_FAST                'o'
               98  LOAD_STR                 '-v'
              100  COMPARE_OP               ==
              102  POP_JUMP_IF_FALSE   114  'to 114'

 L. 340       104  LOAD_FAST                'verboseLevel'
              106  LOAD_CONST               1
              108  BINARY_ADD       
              110  STORE_FAST               'verboseLevel'
              112  JUMP_BACK            60  'to 60'
            114_0  COME_FROM           102  '102'

 L. 341       114  LOAD_FAST                'o'
              116  LOAD_STR                 '-q'
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_FALSE   132  'to 132'

 L. 342       122  LOAD_FAST                'verboseLevel'
              124  LOAD_CONST               1
              126  BINARY_SUBTRACT  
              128  STORE_FAST               'verboseLevel'
              130  JUMP_BACK            60  'to 60'
            132_0  COME_FROM           120  '120'

 L. 343       132  LOAD_FAST                'o'
              134  LOAD_STR                 '-i'
              136  COMPARE_OP               ==
              138  POP_JUMP_IF_FALSE   186  'to 186'

 L. 344       140  LOAD_GLOBAL              len
              142  LOAD_FAST                'args'
              144  CALL_FUNCTION_1       1  ''
              146  LOAD_CONST               0
              148  COMPARE_OP               ==
              150  POP_JUMP_IF_FALSE   162  'to 162'

 L. 345       152  LOAD_GLOBAL              ShowInfo
              154  LOAD_CONST               None
              156  CALL_FUNCTION_1       1  ''
              158  POP_TOP          
              160  JUMP_FORWARD        180  'to 180'
            162_0  COME_FROM           150  '150'

 L. 347       162  LOAD_FAST                'args'
              164  GET_ITER         
            166_0  COME_FROM           178  '178'
              166  FOR_ITER            180  'to 180'
              168  STORE_FAST               'arg'

 L. 348       170  LOAD_GLOBAL              ShowInfo
              172  LOAD_FAST                'arg'
              174  CALL_FUNCTION_1       1  ''
              176  POP_TOP          
              178  JUMP_BACK           166  'to 166'
            180_0  COME_FROM           166  '166'
            180_1  COME_FROM           160  '160'

 L. 349       180  LOAD_CONST               0
              182  STORE_FAST               'doit'
              184  JUMP_BACK            60  'to 60'
            186_0  COME_FROM           138  '138'

 L. 350       186  LOAD_FAST                'o'
              188  LOAD_STR                 '-d'
              190  COMPARE_OP               ==
              192  POP_JUMP_IF_FALSE_BACK    60  'to 60'

 L. 351       194  LOAD_FAST                'bForDemand'
              196  UNARY_NOT        
              198  STORE_FAST               'bForDemand'
              200  JUMP_BACK            60  'to 60'
            202_0  COME_FROM            60  '60'
              202  POP_BLOCK        
              204  JUMP_FORWARD        276  'to 276'
            206_0  COME_FROM_FINALLY    28  '28'

 L. 353       206  DUP_TOP          
              208  LOAD_FAST                'getopt'
              210  LOAD_ATTR                error
              212  LOAD_GLOBAL              error
              214  BUILD_TUPLE_2         2 
          216_218  <121>               274  ''
              220  POP_TOP          
              222  STORE_FAST               'msg'
              224  POP_TOP          
              226  SETUP_FINALLY       266  'to 266'

 L. 354       228  LOAD_GLOBAL              sys
              230  LOAD_ATTR                stderr
              232  LOAD_METHOD              write
              234  LOAD_GLOBAL              str
              236  LOAD_FAST                'msg'
              238  CALL_FUNCTION_1       1  ''
              240  LOAD_STR                 '\n'
              242  BINARY_ADD       
              244  CALL_METHOD_1         1  ''
              246  POP_TOP          

 L. 355       248  LOAD_GLOBAL              usage
              250  CALL_FUNCTION_0       0  ''
              252  POP_TOP          
              254  POP_BLOCK        
              256  POP_EXCEPT       
              258  LOAD_CONST               None
              260  STORE_FAST               'msg'
              262  DELETE_FAST              'msg'
              264  JUMP_FORWARD        276  'to 276'
            266_0  COME_FROM_FINALLY   226  '226'
              266  LOAD_CONST               None
              268  STORE_FAST               'msg'
              270  DELETE_FAST              'msg'
              272  <48>             
              274  <48>             
            276_0  COME_FROM           264  '264'
            276_1  COME_FROM           204  '204'

 L. 357       276  LOAD_FAST                'bForDemand'
          278_280  POP_JUMP_IF_FALSE   310  'to 310'
              282  LOAD_FAST                'outputName'
              284  LOAD_CONST               None
              286  <117>                 1  ''
          288_290  POP_JUMP_IF_FALSE   310  'to 310'

 L. 358       292  LOAD_GLOBAL              sys
              294  LOAD_ATTR                stderr
              296  LOAD_METHOD              write
              298  LOAD_STR                 'Can not use -d and -o together\n'
              300  CALL_METHOD_1         1  ''
              302  POP_TOP          

 L. 359       304  LOAD_GLOBAL              usage
              306  CALL_FUNCTION_0       0  ''
              308  POP_TOP          
            310_0  COME_FROM           288  '288'
            310_1  COME_FROM           278  '278'

 L. 361       310  LOAD_FAST                'doit'
          312_314  POP_JUMP_IF_TRUE    320  'to 320'

 L. 362       316  LOAD_CONST               0
              318  RETURN_VALUE     
            320_0  COME_FROM           312  '312'

 L. 363       320  LOAD_GLOBAL              len
              322  LOAD_FAST                'args'
              324  CALL_FUNCTION_1       1  ''
              326  LOAD_CONST               0
              328  COMPARE_OP               ==
          330_332  POP_JUMP_IF_FALSE   368  'to 368'

 L. 364       334  LOAD_GLOBAL              selecttlb
              336  LOAD_METHOD              SelectTlb
              338  CALL_METHOD_0         0  ''
              340  STORE_FAST               'rc'

 L. 365       342  LOAD_FAST                'rc'
              344  LOAD_CONST               None
              346  <117>                 0  ''
          348_350  POP_JUMP_IF_FALSE   362  'to 362'

 L. 366       352  LOAD_GLOBAL              sys
              354  LOAD_METHOD              exit
              356  LOAD_CONST               1
              358  CALL_METHOD_1         1  ''
              360  POP_TOP          
            362_0  COME_FROM           348  '348'

 L. 367       362  LOAD_FAST                'rc'
              364  BUILD_LIST_1          1 
              366  STORE_FAST               'args'
            368_0  COME_FROM           330  '330'

 L. 369       368  LOAD_FAST                'outputName'
              370  LOAD_CONST               None
              372  <117>                 1  ''
          374_376  POP_JUMP_IF_FALSE   476  'to 476'

 L. 370       378  LOAD_GLOBAL              os
              380  LOAD_ATTR                path
              382  LOAD_METHOD              dirname
              384  LOAD_FAST                'outputName'
              386  CALL_METHOD_1         1  ''
              388  STORE_FAST               'path'

 L. 371       390  LOAD_FAST                'path'
              392  LOAD_STR                 ''
              394  COMPARE_OP               !=
          396_398  POP_JUMP_IF_FALSE   424  'to 424'
              400  LOAD_GLOBAL              os
              402  LOAD_ATTR                path
              404  LOAD_METHOD              exists
              406  LOAD_FAST                'path'
              408  CALL_METHOD_1         1  ''
          410_412  POP_JUMP_IF_TRUE    424  'to 424'

 L. 372       414  LOAD_GLOBAL              os
              416  LOAD_METHOD              makedirs
              418  LOAD_FAST                'path'
              420  CALL_METHOD_1         1  ''
              422  POP_TOP          
            424_0  COME_FROM           410  '410'
            424_1  COME_FROM           396  '396'

 L. 373       424  LOAD_GLOBAL              sys
              426  LOAD_ATTR                version_info
              428  LOAD_CONST               (3, 0)
              430  COMPARE_OP               >
          432_434  POP_JUMP_IF_FALSE   452  'to 452'

 L. 374       436  LOAD_GLOBAL              open
              438  LOAD_FAST                'outputName'
              440  LOAD_STR                 'wt'
              442  LOAD_STR                 'mbcs'
              444  LOAD_CONST               ('encoding',)
              446  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              448  STORE_FAST               'f'
              450  JUMP_FORWARD        474  'to 474'
            452_0  COME_FROM           432  '432'

 L. 376       452  LOAD_CONST               0
              454  LOAD_CONST               None
              456  IMPORT_NAME              codecs
              458  STORE_FAST               'codecs'

 L. 377       460  LOAD_FAST                'codecs'
              462  LOAD_METHOD              open
              464  LOAD_FAST                'outputName'
              466  LOAD_STR                 'w'
              468  LOAD_STR                 'mbcs'
              470  CALL_METHOD_3         3  ''
              472  STORE_FAST               'f'
            474_0  COME_FROM           450  '450'
              474  JUMP_FORWARD        480  'to 480'
            476_0  COME_FROM           374  '374'

 L. 379       476  LOAD_CONST               None
              478  STORE_FAST               'f'
            480_0  COME_FROM           474  '474'

 L. 381       480  LOAD_FAST                'args'
              482  GET_ITER         
            484_0  COME_FROM           506  '506'
              484  FOR_ITER            510  'to 510'
              486  STORE_FAST               'arg'

 L. 382       488  LOAD_GLOBAL              GenerateFromTypeLibSpec
              490  LOAD_FAST                'arg'
              492  LOAD_FAST                'f'
              494  LOAD_FAST                'verboseLevel'
              496  LOAD_FAST                'bForDemand'
              498  LOAD_FAST                'hiddenSpec'
              500  LOAD_CONST               ('verboseLevel', 'bForDemand', 'bBuildHidden')
              502  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              504  POP_TOP          
          506_508  JUMP_BACK           484  'to 484'
            510_0  COME_FROM           484  '484'

 L. 384       510  LOAD_FAST                'f'
          512_514  POP_JUMP_IF_FALSE   524  'to 524'

 L. 385       516  LOAD_FAST                'f'
              518  LOAD_METHOD              close
              520  CALL_METHOD_0         0  ''
              522  POP_TOP          
            524_0  COME_FROM           512  '512'

Parse error at or near `<121>' instruction at offset 216_218


if __name__ == '__main__':
    rc = main()
    if rc:
        sys.exit(rc)
    sys.exit(0)