# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: pkg_resources\extern\__init__.py
import importlib.util, sys

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

    def _module_matches_namespace(self, fullname):
        """Figure out if the target module is vendored."""
        root, base, target = fullname.partition(self.root_name + '.')
        return not root and any(map(target.startswith, self.vendored_names))

    def load_module--- This code section failed: ---

 L.  33         0  LOAD_FAST                'fullname'
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

 L.  34        22  LOAD_FAST                'self'
               24  LOAD_ATTR                search_path
               26  GET_ITER         
               28  FOR_ITER            100  'to 100'
               30  STORE_FAST               'prefix'

 L.  35        32  SETUP_FINALLY        80  'to 80'

 L.  36        34  LOAD_FAST                'prefix'
               36  LOAD_FAST                'target'
               38  BINARY_ADD       
               40  STORE_FAST               'extant'

 L.  37        42  LOAD_GLOBAL              __import__
               44  LOAD_FAST                'extant'
               46  CALL_FUNCTION_1       1  ''
               48  POP_TOP          

 L.  38        50  LOAD_GLOBAL              sys
               52  LOAD_ATTR                modules
               54  LOAD_FAST                'extant'
               56  BINARY_SUBSCR    
               58  STORE_FAST               'mod'

 L.  39        60  LOAD_FAST                'mod'
               62  LOAD_GLOBAL              sys
               64  LOAD_ATTR                modules
               66  LOAD_FAST                'fullname'
               68  STORE_SUBSCR     

 L.  40        70  LOAD_FAST                'mod'
               72  POP_BLOCK        
               74  ROT_TWO          
               76  POP_TOP          
               78  RETURN_VALUE     
             80_0  COME_FROM_FINALLY    32  '32'

 L.  41        80  DUP_TOP          
               82  LOAD_GLOBAL              ImportError
               84  <121>                96  ''
               86  POP_TOP          
               88  POP_TOP          
               90  POP_TOP          

 L.  42        92  POP_EXCEPT       
               94  JUMP_BACK            28  'to 28'
               96  <48>             
               98  JUMP_BACK            28  'to 28'

 L.  44       100  LOAD_GLOBAL              ImportError

 L.  45       102  LOAD_STR                 "The '{target}' package is required; normally this is bundled with this package so if you get this warning, consult the packager of your distribution."
              104  LOAD_ATTR                format
              106  BUILD_TUPLE_0         0 
              108  BUILD_MAP_0           0 

 L.  48       110  LOAD_GLOBAL              locals
              112  CALL_FUNCTION_0       0  ''

 L.  45       114  <164>                 1  ''
              116  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'

 L.  44       118  CALL_FUNCTION_1       1  ''
              120  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `ROT_TWO' instruction at offset 74

    def create_module(self, spec):
        return self.load_module(spec.name)

    def exec_module(self, module):
        pass

    def find_spec(self, fullname, path=None, target=None):
        """Return a module spec for vendored names."""
        if self._module_matches_namespace(fullname):
            return importlib.util.spec_from_loader(fullname, self)

    def install--- This code section failed: ---

 L.  68         0  LOAD_FAST                'self'
                2  LOAD_GLOBAL              sys
                4  LOAD_ATTR                meta_path
                6  <118>                 1  ''
                8  POP_JUMP_IF_FALSE    22  'to 22'

 L.  69        10  LOAD_GLOBAL              sys
               12  LOAD_ATTR                meta_path
               14  LOAD_METHOD              append
               16  LOAD_FAST                'self'
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          
             22_0  COME_FROM             8  '8'

Parse error at or near `None' instruction at offset -1


names = ('packaging', 'pyparsing', 'appdirs')
VendorImporter(__name__, names).install()