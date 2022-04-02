# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\selenium\webdriver\firefox\firefox_profile.py
from __future__ import with_statement
import base64, copy, json, os, re, shutil, sys, tempfile, zipfile
try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO
else:
    from xml.dom import minidom
    from selenium.webdriver.common.proxy import ProxyType
    from selenium.common.exceptions import WebDriverException
    WEBDRIVER_EXT = 'webdriver.xpi'
    WEBDRIVER_PREFERENCES = 'webdriver_prefs.json'
    EXTENSION_NAME = 'fxdriver@googlecode.com'

    class AddonFormatError(Exception):
        __doc__ = 'Exception for not well-formed add-on manifest files'


    class FirefoxProfile(object):
        ANONYMOUS_PROFILE_NAME = 'WEBDRIVER_ANONYMOUS_PROFILE'
        DEFAULT_PREFERENCES = None

        def __init__(self, profile_directory=None):
            """
        Initialises a new instance of a Firefox Profile

        :args:
         - profile_directory: Directory of profile that you want to use. If a
           directory is passed in it will be cloned and the cloned directory
           will be used by the driver when instantiated.
           This defaults to None and will create a new
           directory when object is created.
        """
            if not FirefoxProfile.DEFAULT_PREFERENCES:
                with open(os.path.join(os.path.dirname(__file__), WEBDRIVER_PREFERENCES)) as default_prefs:
                    FirefoxProfile.DEFAULT_PREFERENCES = json.load(default_prefs)
            self.default_preferences = copy.deepcopy(FirefoxProfile.DEFAULT_PREFERENCES['mutable'])
            self.native_events_enabled = True
            self.profile_dir = profile_directory
            self.tempfolder = None
            if self.profile_dir is None:
                self.profile_dir = self._create_tempfolder()
            else:
                self.tempfolder = tempfile.mkdtemp()
                newprof = os.path.join(self.tempfolder, 'webdriver-py-profilecopy')
                shutil.copytree((self.profile_dir), newprof, ignore=(shutil.ignore_patterns('parent.lock', 'lock', '.parentlock')))
                self.profile_dir = newprof
                os.chmod(self.profile_dir, 493)
                self._read_existing_userjs(os.path.join(self.profile_dir, 'user.js'))
            self.extensionsDir = os.path.join(self.profile_dir, 'extensions')
            self.userPrefs = os.path.join(self.profile_dir, 'user.js')
            if os.path.isfile(self.userPrefs):
                os.chmod(self.userPrefs, 420)

        def set_preference(self, key, value):
            """
        sets the preference that we want in the profile.
        """
            self.default_preferences[key] = value

        def add_extension(self, extension=WEBDRIVER_EXT):
            self._install_extension(extension)

        def update_preferences(self):
            for key, value in FirefoxProfile.DEFAULT_PREFERENCES['frozen'].items():
                self.default_preferences[key] = value
            else:
                self._write_user_prefs(self.default_preferences)

        @property
        def path(self):
            """
        Gets the profile directory that is currently being used
        """
            return self.profile_dir

        @property
        def port(self):
            """
        Gets the port that WebDriver is working on
        """
            return self._port

        @port.setter
        def port(self, port):
            """
        Sets the port that WebDriver will be running on
        """
            if not isinstance(port, int):
                raise WebDriverException('Port needs to be an integer')
            try:
                port = int(port)
                if port < 1 or (port > 65535):
                    raise WebDriverException('Port number must be in the range 1..65535')
            except (ValueError, TypeError):
                raise WebDriverException('Port needs to be an integer')
            else:
                self._port = port
                self.set_preference('webdriver_firefox_port', self._port)

        @property
        def accept_untrusted_certs(self):
            return self.default_preferences['webdriver_accept_untrusted_certs']

        @accept_untrusted_certs.setter
        def accept_untrusted_certs(self, value):
            if value not in (True, False):
                raise WebDriverException('Please pass in a Boolean to this call')
            self.set_preference('webdriver_accept_untrusted_certs', value)

        @property
        def assume_untrusted_cert_issuer(self):
            return self.default_preferences['webdriver_assume_untrusted_issuer']

        @assume_untrusted_cert_issuer.setter
        def assume_untrusted_cert_issuer(self, value):
            if value not in (True, False):
                raise WebDriverException('Please pass in a Boolean to this call')
            self.set_preference('webdriver_assume_untrusted_issuer', value)

        @property
        def native_events_enabled(self):
            return self.default_preferences['webdriver_enable_native_events']

        @native_events_enabled.setter
        def native_events_enabled(self, value):
            if value not in (True, False):
                raise WebDriverException('Please pass in a Boolean to this call')
            self.set_preference('webdriver_enable_native_events', value)

        @property
        def encoded(self):
            """
        A zipped, base64 encoded string of profile directory
        for use with remote WebDriver JSON wire protocol
        """
            self.update_preferences()
            fp = BytesIO()
            zipped = zipfile.ZipFile(fp, 'w', zipfile.ZIP_DEFLATED)
            path_root = len(self.path) + 1
            for base, dirs, files in os.walk(self.path):
                for fyle in files:
                    filename = os.path.join(base, fyle)
                    zipped.write(filename, filename[path_root:])

            else:
                zipped.close()
                return base64.b64encode(fp.getvalue()).decode('UTF-8')

        def set_proxy(self, proxy):
            import warnings
            warnings.warn('This method has been deprecated. Please pass in the proxy object to the Driver Object',
              DeprecationWarning,
              stacklevel=2)
            if proxy is None:
                raise ValueError('proxy can not be None')
            if proxy.proxy_type is ProxyType.UNSPECIFIED:
                return
            self.set_preference('network.proxy.type', proxy.proxy_type['ff_value'])
            if proxy.proxy_type is ProxyType.MANUAL:
                self.set_preference('network.proxy.no_proxies_on', proxy.no_proxy)
                self._set_manual_proxy_preference('ftp', proxy.ftp_proxy)
                self._set_manual_proxy_preference('http', proxy.http_proxy)
                self._set_manual_proxy_preference('ssl', proxy.ssl_proxy)
                self._set_manual_proxy_preference('socks', proxy.socks_proxy)
            elif proxy.proxy_type is ProxyType.PAC:
                self.set_preference('network.proxy.autoconfig_url', proxy.proxy_autoconfig_url)

        def _set_manual_proxy_preference(self, key, setting):
            if setting is None or (setting is ''):
                return
            host_details = setting.split(':')
            self.set_preference('network.proxy.%s' % key, host_details[0])
            if len(host_details) > 1:
                self.set_preference('network.proxy.%s_port' % key, int(host_details[1]))

        def _create_tempfolder(self):
            """
        Creates a temp folder to store User.js and the extension
        """
            return tempfile.mkdtemp()

        def _write_user_prefs(self, user_prefs):
            """
        writes the current user prefs dictionary to disk
        """
            with open(self.userPrefs, 'w') as f:
                for key, value in user_prefs.items():
                    f.write('user_pref("%s", %s);\n' % (key, json.dumps(value)))

        def _read_existing_userjs(self, userjs):
            import warnings
            PREF_RE = re.compile('user_pref\\("(.*)",\\s(.*)\\)')
            try:
                with open(userjs) as f:
                    for usr in f:
                        matches = re.search(PREF_RE, usr)
                        try:
                            self.default_preferences[matches.group(1)] = json.loads(matches.group(2))
                        except Exception:
                            warnings.warn('(skipping) failed to json.loads existing preference: ' + matches.group(1) + matches.group(2))

            except Exception:
                pass

        def _install_extension(self, addon, unpack=True):
            """
            Installs addon from a filepath, url
            or directory of addons in the profile.
            - path: url, absolute path to .xpi, or directory of addons
            - unpack: whether to unpack unless specified otherwise in the install.rdf
        """
            if addon == WEBDRIVER_EXT:
                addon = os.path.join(os.path.dirname(__file__), WEBDRIVER_EXT)
            tmpdir = None
            xpifile = None
            if addon.endswith('.xpi'):
                tmpdir = tempfile.mkdtemp(suffix=('.' + os.path.split(addon)[(-1)]))
                compressed_file = zipfile.ZipFile(addon, 'r')
                for name in compressed_file.namelist():
                    if name.endswith('/'):
                        if not os.path.isdir(os.path.join(tmpdir, name)):
                            os.makedirs(os.path.join(tmpdir, name))
                    else:
                        if not os.path.isdir(os.path.dirname(os.path.join(tmpdir, name))):
                            os.makedirs(os.path.dirname(os.path.join(tmpdir, name)))
                        data = compressed_file.read(name)
                        with open(os.path.join(tmpdir, name), 'wb') as f:
                            f.write(data)
                    xpifile = addon
                    addon = tmpdir

                addon_details = self._addon_details(addon)
                addon_id = addon_details.get('id')
                assert addon_id, 'The addon id could not be found: %s' % addon
                addon_path = os.path.join(self.extensionsDir, addon_id)
                if not (unpack or addon_details['unpack']) or xpifile:
                    if not os.path.exists(self.extensionsDir):
                        os.makedirs(self.extensionsDir)
                        os.chmod(self.extensionsDir, 493)
                    shutil.copy(xpifile, addon_path + '.xpi')
                elif not os.path.exists(addon_path):
                    shutil.copytree(addon, addon_path, symlinks=True)
                if tmpdir:
                    shutil.rmtree(tmpdir)

        def _addon_details--- This code section failed: ---

 L. 310         0  LOAD_CONST               None

 L. 311         2  LOAD_CONST               False

 L. 312         4  LOAD_CONST               None

 L. 313         6  LOAD_CONST               None

 L. 309         8  LOAD_CONST               ('id', 'unpack', 'name', 'version')
               10  BUILD_CONST_KEY_MAP_4     4 
               12  STORE_FAST               'details'

 L. 316        14  LOAD_CODE                <code_object get_namespace_id>
               16  LOAD_STR                 'FirefoxProfile._addon_details.<locals>.get_namespace_id'
               18  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               20  STORE_FAST               'get_namespace_id'

 L. 327        22  LOAD_CODE                <code_object get_text>
               24  LOAD_STR                 'FirefoxProfile._addon_details.<locals>.get_text'
               26  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               28  STORE_FAST               'get_text'

 L. 335        30  LOAD_CODE                <code_object parse_manifest_json>
               32  LOAD_STR                 'FirefoxProfile._addon_details.<locals>.parse_manifest_json'
               34  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               36  STORE_FAST               'parse_manifest_json'

 L. 349        38  LOAD_GLOBAL              os
               40  LOAD_ATTR                path
               42  LOAD_METHOD              exists
               44  LOAD_FAST                'addon_path'
               46  CALL_METHOD_1         1  ''
               48  POP_JUMP_IF_TRUE     62  'to 62'

 L. 350        50  LOAD_GLOBAL              IOError
               52  LOAD_STR                 'Add-on path does not exist: %s'
               54  LOAD_FAST                'addon_path'
               56  BINARY_MODULO    
               58  CALL_FUNCTION_1       1  ''
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            48  '48'

 L. 352        62  SETUP_FINALLY       288  'to 288'

 L. 353        64  LOAD_GLOBAL              zipfile
               66  LOAD_METHOD              is_zipfile
               68  LOAD_FAST                'addon_path'
               70  CALL_METHOD_1         1  ''
               72  POP_JUMP_IF_FALSE   146  'to 146'

 L. 356        74  SETUP_FINALLY       134  'to 134'

 L. 357        76  LOAD_GLOBAL              zipfile
               78  LOAD_METHOD              ZipFile
               80  LOAD_FAST                'addon_path'
               82  LOAD_STR                 'r'
               84  CALL_METHOD_2         2  ''
               86  STORE_FAST               'compressed_file'

 L. 358        88  LOAD_STR                 'manifest.json'
               90  LOAD_FAST                'compressed_file'
               92  LOAD_METHOD              namelist
               94  CALL_METHOD_0         0  ''
               96  COMPARE_OP               in
               98  POP_JUMP_IF_FALSE   120  'to 120'

 L. 359       100  LOAD_FAST                'parse_manifest_json'
              102  LOAD_FAST                'compressed_file'
              104  LOAD_METHOD              read
              106  LOAD_STR                 'manifest.json'
              108  CALL_METHOD_1         1  ''
              110  CALL_FUNCTION_1       1  ''
              112  POP_BLOCK        
              114  CALL_FINALLY        134  'to 134'
              116  POP_BLOCK        
              118  RETURN_VALUE     
            120_0  COME_FROM            98  '98'

 L. 361       120  LOAD_FAST                'compressed_file'
              122  LOAD_METHOD              read
              124  LOAD_STR                 'install.rdf'
              126  CALL_METHOD_1         1  ''
              128  STORE_FAST               'manifest'
              130  POP_BLOCK        
              132  BEGIN_FINALLY    
            134_0  COME_FROM           114  '114'
            134_1  COME_FROM_FINALLY    74  '74'

 L. 363       134  LOAD_FAST                'compressed_file'
              136  LOAD_METHOD              close
              138  CALL_METHOD_0         0  ''
              140  POP_TOP          
              142  END_FINALLY      
              144  JUMP_FORWARD        284  'to 284'
            146_0  COME_FROM            72  '72'

 L. 364       146  LOAD_GLOBAL              os
              148  LOAD_ATTR                path
              150  LOAD_METHOD              isdir
              152  LOAD_FAST                'addon_path'
              154  CALL_METHOD_1         1  ''
          156_158  POP_JUMP_IF_FALSE   272  'to 272'

 L. 365       160  LOAD_GLOBAL              os
              162  LOAD_ATTR                path
              164  LOAD_METHOD              join
              166  LOAD_FAST                'addon_path'
              168  LOAD_STR                 'manifest.json'
              170  CALL_METHOD_2         2  ''
              172  STORE_FAST               'manifest_json_filename'

 L. 366       174  LOAD_GLOBAL              os
              176  LOAD_ATTR                path
              178  LOAD_METHOD              exists
              180  LOAD_FAST                'manifest_json_filename'
              182  CALL_METHOD_1         1  ''
              184  POP_JUMP_IF_FALSE   230  'to 230'

 L. 367       186  LOAD_GLOBAL              open
              188  LOAD_FAST                'manifest_json_filename'
              190  LOAD_STR                 'r'
              192  CALL_FUNCTION_2       2  ''
              194  SETUP_WITH          224  'to 224'
              196  STORE_FAST               'f'

 L. 368       198  LOAD_FAST                'parse_manifest_json'
              200  LOAD_FAST                'f'
              202  LOAD_METHOD              read
              204  CALL_METHOD_0         0  ''
              206  CALL_FUNCTION_1       1  ''
              208  POP_BLOCK        
              210  ROT_TWO          
              212  BEGIN_FINALLY    
              214  WITH_CLEANUP_START
              216  WITH_CLEANUP_FINISH
              218  POP_FINALLY           0  ''
              220  POP_BLOCK        
              222  RETURN_VALUE     
            224_0  COME_FROM_WITH      194  '194'
              224  WITH_CLEANUP_START
              226  WITH_CLEANUP_FINISH
              228  END_FINALLY      
            230_0  COME_FROM           184  '184'

 L. 370       230  LOAD_GLOBAL              open
              232  LOAD_GLOBAL              os
              234  LOAD_ATTR                path
              236  LOAD_METHOD              join
              238  LOAD_FAST                'addon_path'
              240  LOAD_STR                 'install.rdf'
              242  CALL_METHOD_2         2  ''
              244  LOAD_STR                 'r'
              246  CALL_FUNCTION_2       2  ''
              248  SETUP_WITH          264  'to 264'
              250  STORE_FAST               'f'

 L. 371       252  LOAD_FAST                'f'
              254  LOAD_METHOD              read
              256  CALL_METHOD_0         0  ''
              258  STORE_FAST               'manifest'
              260  POP_BLOCK        
              262  BEGIN_FINALLY    
            264_0  COME_FROM_WITH      248  '248'
              264  WITH_CLEANUP_START
              266  WITH_CLEANUP_FINISH
              268  END_FINALLY      
              270  JUMP_FORWARD        284  'to 284'
            272_0  COME_FROM           156  '156'

 L. 373       272  LOAD_GLOBAL              IOError
              274  LOAD_STR                 'Add-on path is neither an XPI nor a directory: %s'
              276  LOAD_FAST                'addon_path'
              278  BINARY_MODULO    
              280  CALL_FUNCTION_1       1  ''
              282  RAISE_VARARGS_1       1  'exception instance'
            284_0  COME_FROM           270  '270'
            284_1  COME_FROM           144  '144'
              284  POP_BLOCK        
              286  JUMP_FORWARD        350  'to 350'
            288_0  COME_FROM_FINALLY    62  '62'

 L. 374       288  DUP_TOP          
              290  LOAD_GLOBAL              IOError
              292  LOAD_GLOBAL              KeyError
              294  BUILD_TUPLE_2         2 
              296  COMPARE_OP               exception-match
          298_300  POP_JUMP_IF_FALSE   348  'to 348'
              302  POP_TOP          
              304  STORE_FAST               'e'
              306  POP_TOP          
              308  SETUP_FINALLY       336  'to 336'

 L. 375       310  LOAD_GLOBAL              AddonFormatError
              312  LOAD_GLOBAL              str
              314  LOAD_FAST                'e'
              316  CALL_FUNCTION_1       1  ''
              318  LOAD_GLOBAL              sys
              320  LOAD_METHOD              exc_info
              322  CALL_METHOD_0         0  ''
              324  LOAD_CONST               2
              326  BINARY_SUBSCR    
              328  CALL_FUNCTION_2       2  ''
              330  RAISE_VARARGS_1       1  'exception instance'
              332  POP_BLOCK        
              334  BEGIN_FINALLY    
            336_0  COME_FROM_FINALLY   308  '308'
              336  LOAD_CONST               None
              338  STORE_FAST               'e'
              340  DELETE_FAST              'e'
              342  END_FINALLY      
              344  POP_EXCEPT       
              346  JUMP_FORWARD        350  'to 350'
            348_0  COME_FROM           298  '298'
              348  END_FINALLY      
            350_0  COME_FROM           346  '346'
            350_1  COME_FROM           286  '286'

 L. 377       350  SETUP_FINALLY       572  'to 572'

 L. 378       352  LOAD_GLOBAL              minidom
              354  LOAD_METHOD              parseString
              356  LOAD_FAST                'manifest'
              358  CALL_METHOD_1         1  ''
              360  STORE_FAST               'doc'

 L. 381       362  LOAD_FAST                'get_namespace_id'
              364  LOAD_FAST                'doc'
              366  LOAD_STR                 'http://www.mozilla.org/2004/em-rdf#'
              368  CALL_FUNCTION_2       2  ''
              370  STORE_FAST               'em'

 L. 382       372  LOAD_FAST                'get_namespace_id'
              374  LOAD_FAST                'doc'
              376  LOAD_STR                 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
              378  CALL_FUNCTION_2       2  ''
              380  STORE_FAST               'rdf'

 L. 384       382  LOAD_FAST                'doc'
              384  LOAD_METHOD              getElementsByTagName
              386  LOAD_FAST                'rdf'
              388  LOAD_STR                 'Description'
              390  BINARY_ADD       
              392  CALL_METHOD_1         1  ''
              394  LOAD_METHOD              item
              396  LOAD_CONST               0
              398  CALL_METHOD_1         1  ''
              400  STORE_FAST               'description'

 L. 385       402  LOAD_FAST                'description'
              404  LOAD_CONST               None
              406  COMPARE_OP               is
          408_410  POP_JUMP_IF_FALSE   428  'to 428'

 L. 386       412  LOAD_FAST                'doc'
              414  LOAD_METHOD              getElementsByTagName
              416  LOAD_STR                 'Description'
              418  CALL_METHOD_1         1  ''
              420  LOAD_METHOD              item
              422  LOAD_CONST               0
              424  CALL_METHOD_1         1  ''
              426  STORE_FAST               'description'
            428_0  COME_FROM           408  '408'

 L. 387       428  LOAD_FAST                'description'
              430  LOAD_ATTR                childNodes
              432  GET_ITER         
            434_0  COME_FROM           484  '484'
            434_1  COME_FROM           462  '462'
              434  FOR_ITER            488  'to 488'
              436  STORE_FAST               'node'

 L. 389       438  LOAD_FAST                'node'
              440  LOAD_ATTR                nodeName
              442  LOAD_METHOD              replace
              444  LOAD_FAST                'em'
              446  LOAD_STR                 ''
              448  CALL_METHOD_2         2  ''
              450  STORE_FAST               'entry'

 L. 390       452  LOAD_FAST                'entry'
              454  LOAD_FAST                'details'
              456  LOAD_METHOD              keys
              458  CALL_METHOD_0         0  ''
              460  COMPARE_OP               in
          462_464  POP_JUMP_IF_FALSE_BACK   434  'to 434'

 L. 391       466  LOAD_FAST                'details'
              468  LOAD_METHOD              update
              470  LOAD_FAST                'entry'
              472  LOAD_FAST                'get_text'
              474  LOAD_FAST                'node'
              476  CALL_FUNCTION_1       1  ''
              478  BUILD_MAP_1           1 
              480  CALL_METHOD_1         1  ''
              482  POP_TOP          
          484_486  JUMP_BACK           434  'to 434'
            488_0  COME_FROM           434  '434'

 L. 392       488  LOAD_FAST                'details'
              490  LOAD_METHOD              get
              492  LOAD_STR                 'id'
              494  CALL_METHOD_1         1  ''
              496  LOAD_CONST               None
              498  COMPARE_OP               is
          500_502  POP_JUMP_IF_FALSE   568  'to 568'

 L. 393       504  LOAD_GLOBAL              range
              506  LOAD_FAST                'description'
              508  LOAD_ATTR                attributes
              510  LOAD_ATTR                length
              512  CALL_FUNCTION_1       1  ''
              514  GET_ITER         
            516_0  COME_FROM           564  '564'
            516_1  COME_FROM           544  '544'
              516  FOR_ITER            568  'to 568'
              518  STORE_FAST               'i'

 L. 394       520  LOAD_FAST                'description'
              522  LOAD_ATTR                attributes
              524  LOAD_METHOD              item
              526  LOAD_FAST                'i'
              528  CALL_METHOD_1         1  ''
              530  STORE_FAST               'attribute'

 L. 395       532  LOAD_FAST                'attribute'
              534  LOAD_ATTR                name
              536  LOAD_FAST                'em'
              538  LOAD_STR                 'id'
              540  BINARY_ADD       
              542  COMPARE_OP               ==
          544_546  POP_JUMP_IF_FALSE_BACK   516  'to 516'

 L. 396       548  LOAD_FAST                'details'
              550  LOAD_METHOD              update
              552  LOAD_STR                 'id'
              554  LOAD_FAST                'attribute'
              556  LOAD_ATTR                value
              558  BUILD_MAP_1           1 
              560  CALL_METHOD_1         1  ''
              562  POP_TOP          
          564_566  JUMP_BACK           516  'to 516'
            568_0  COME_FROM           516  '516'
            568_1  COME_FROM           500  '500'
              568  POP_BLOCK        
              570  JUMP_FORWARD        630  'to 630'
            572_0  COME_FROM_FINALLY   350  '350'

 L. 397       572  DUP_TOP          
              574  LOAD_GLOBAL              Exception
              576  COMPARE_OP               exception-match
          578_580  POP_JUMP_IF_FALSE   628  'to 628'
              582  POP_TOP          
              584  STORE_FAST               'e'
              586  POP_TOP          
              588  SETUP_FINALLY       616  'to 616'

 L. 398       590  LOAD_GLOBAL              AddonFormatError
              592  LOAD_GLOBAL              str
              594  LOAD_FAST                'e'
              596  CALL_FUNCTION_1       1  ''
              598  LOAD_GLOBAL              sys
              600  LOAD_METHOD              exc_info
              602  CALL_METHOD_0         0  ''
              604  LOAD_CONST               2
              606  BINARY_SUBSCR    
              608  CALL_FUNCTION_2       2  ''
              610  RAISE_VARARGS_1       1  'exception instance'
              612  POP_BLOCK        
              614  BEGIN_FINALLY    
            616_0  COME_FROM_FINALLY   588  '588'
              616  LOAD_CONST               None
              618  STORE_FAST               'e'
              620  DELETE_FAST              'e'
              622  END_FINALLY      
              624  POP_EXCEPT       
              626  JUMP_FORWARD        630  'to 630'
            628_0  COME_FROM           578  '578'
              628  END_FINALLY      
            630_0  COME_FROM           626  '626'
            630_1  COME_FROM           570  '570'

 L. 401       630  LOAD_GLOBAL              isinstance
              632  LOAD_FAST                'details'
              634  LOAD_STR                 'unpack'
              636  BINARY_SUBSCR    
              638  LOAD_GLOBAL              str
              640  CALL_FUNCTION_2       2  ''
          642_644  POP_JUMP_IF_FALSE   666  'to 666'

 L. 402       646  LOAD_FAST                'details'
              648  LOAD_STR                 'unpack'
              650  BINARY_SUBSCR    
              652  LOAD_METHOD              lower
              654  CALL_METHOD_0         0  ''
              656  LOAD_STR                 'true'
              658  COMPARE_OP               ==
              660  LOAD_FAST                'details'
              662  LOAD_STR                 'unpack'
              664  STORE_SUBSCR     
            666_0  COME_FROM           642  '642'

 L. 405       666  LOAD_FAST                'details'
              668  LOAD_METHOD              get
              670  LOAD_STR                 'id'
              672  CALL_METHOD_1         1  ''
              674  LOAD_CONST               None
              676  COMPARE_OP               is
          678_680  POP_JUMP_IF_FALSE   690  'to 690'

 L. 406       682  LOAD_GLOBAL              AddonFormatError
              684  LOAD_STR                 'Add-on id could not be found.'
              686  CALL_FUNCTION_1       1  ''
              688  RAISE_VARARGS_1       1  'exception instance'
            690_0  COME_FROM           678  '678'

 L. 408       690  LOAD_FAST                'details'
              692  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 114