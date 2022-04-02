# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\setuptools\extern\__init__.py
import sys

class VendorImporter:
    __doc__ = '\n    A PEP 302 meta path importer for finding optionally-vendored\n    or otherwise naturally-installed packages from root_name.\n    '

    def __init__(self, root_name, vendored_names=(), vendor_pkg=None):
        self.root_name = root_name
        self.vendored_names = set(vendored_names)
        self.vendor_pkg = vendor_pkg or root_name.replace('extern', '_vendor')

    @property
    def search_path(self):
        """
        Search first the vendor package then as a natural package.
        """
        yield self.vendor_pkg + '.'
        yield ''

    def find_module(self, fullname, path=None):
        """
        Return self when fullname starts with root_name and the
        target module is one vendored through this importer.
        """
        root, base, target = fullname.partition(self.root_name + '.')
        if root:
            return
        else:
            return any(map(target.startswith, self.vendored_names)) or None
        return self

    def load_module--- This code section failed: ---

 L.  39         0  LOAD_FAST                'fullname'
                2  LOAD_METHOD              partition
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                root_name
                8  LOAD_STR                 '.'
               10  BINARY_ADD       
               12  CALL_METHOD_1         1  ''
               14  UNPACK_SEQUENCE_3     3 
               16  STORE_FAST               'root'
               18  STORE_FAST               'base'
               20  STORE_FAST               'target'

 L.  40        22  LOAD_FAST                'self'
               24  LOAD_ATTR                search_path
               26  GET_ITER         
               28  FOR_ITER            120  'to 120'
               30  STORE_FAST               'prefix'

 L.  41        32  SETUP_FINALLY        98  'to 98'

 L.  42        34  LOAD_FAST                'prefix'
               36  LOAD_FAST                'target'
               38  BINARY_ADD       
               40  STORE_FAST               'extant'

 L.  43        42  LOAD_GLOBAL              __import__
               44  LOAD_FAST                'extant'
               46  CALL_FUNCTION_1       1  ''
               48  POP_TOP          

 L.  44        50  LOAD_GLOBAL              sys
               52  LOAD_ATTR                modules
               54  LOAD_FAST                'extant'
               56  BINARY_SUBSCR    
               58  STORE_FAST               'mod'

 L.  45        60  LOAD_FAST                'mod'
               62  LOAD_GLOBAL              sys
               64  LOAD_ATTR                modules
               66  LOAD_FAST                'fullname'
               68  STORE_SUBSCR     

 L.  51        70  LOAD_GLOBAL              sys
               72  LOAD_ATTR                version_info
               74  LOAD_CONST               (3,)
               76  COMPARE_OP               >=
               78  POP_JUMP_IF_FALSE    88  'to 88'

 L.  52        80  LOAD_GLOBAL              sys
               82  LOAD_ATTR                modules
               84  LOAD_FAST                'extant'
               86  DELETE_SUBSCR    
             88_0  COME_FROM            78  '78'

 L.  53        88  LOAD_FAST                'mod'
               90  POP_BLOCK        
               92  ROT_TWO          
               94  POP_TOP          
               96  RETURN_VALUE     
             98_0  COME_FROM_FINALLY    32  '32'

 L.  54        98  DUP_TOP          
              100  LOAD_GLOBAL              ImportError
              102  COMPARE_OP               exception-match
              104  POP_JUMP_IF_FALSE   116  'to 116'
              106  POP_TOP          
              108  POP_TOP          
              110  POP_TOP          

 L.  55       112  POP_EXCEPT       
              114  JUMP_BACK            28  'to 28'
            116_0  COME_FROM           104  '104'
              116  END_FINALLY      
              118  JUMP_BACK            28  'to 28'

 L.  57       120  LOAD_GLOBAL              ImportError

 L.  58       122  LOAD_STR                 "The '{target}' package is required; normally this is bundled with this package so if you get this warning, consult the packager of your distribution."
              124  LOAD_ATTR                format
              126  BUILD_TUPLE_0         0 

 L.  61       128  LOAD_GLOBAL              locals
              130  CALL_FUNCTION_0       0  ''

 L.  58       132  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'

 L.  57       134  CALL_FUNCTION_1       1  ''
              136  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `ROT_TWO' instruction at offset 92

    def install(self):
        """
        Install this importer into sys.meta_path if not already present.
        """
        if self not in sys.meta_path:
            sys.meta_path.append(self)


names = ('six', 'packaging', 'pyparsing')
VendorImporter(__name__, names, 'setuptools._vendor').install()