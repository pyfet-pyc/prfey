# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: requests\auth.py
"""
requests.auth
~~~~~~~~~~~~~

This module contains the authentication handlers for Requests.
"""
import os, re, time, hashlib, threading, warnings
from base64 import b64encode
from .compat import urlparse, str, basestring
from .cookies import extract_cookies_to_jar
from ._internal_utils import to_native_string
from .utils import parse_dict_header
CONTENT_TYPE_FORM_URLENCODED = 'application/x-www-form-urlencoded'
CONTENT_TYPE_MULTI_PART = 'multipart/form-data'

def _basic_auth_str(username, password):
    """Returns a Basic Auth string."""
    if not isinstance(username, basestring):
        warnings.warn(("Non-string usernames will no longer be supported in Requests 3.0.0. Please convert the object you've passed in ({!r}) to a string or bytes object in the near future to avoid problems.".format(username)),
          category=DeprecationWarning)
        username = str(username)
    if not isinstance(password, basestring):
        warnings.warn(("Non-string passwords will no longer be supported in Requests 3.0.0. Please convert the object you've passed in ({!r}) to a string or bytes object in the near future to avoid problems.".format(type(password))),
          category=DeprecationWarning)
        password = str(password)
    if isinstance(username, str):
        username = username.encode('latin1')
    if isinstance(password, str):
        password = password.encode('latin1')
    authstr = 'Basic ' + to_native_string(b64encode((b':').join((username, password))).strip())
    return authstr


class AuthBase(object):
    __doc__ = 'Base class that all auth implementations derive from'

    def __call__(self, r):
        raise NotImplementedError('Auth hooks must be callable.')


class HTTPBasicAuth(AuthBase):
    __doc__ = 'Attaches HTTP Basic Authentication to the given Request object.'

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __eq__(self, other):
        return all([
         self.username == getattr(other, 'username', None),
         self.password == getattr(other, 'password', None)])

    def __ne__(self, other):
        return not self == other

    def __call__(self, r):
        r.headers['Authorization'] = _basic_auth_str(self.username, self.password)
        return r


class HTTPProxyAuth(HTTPBasicAuth):
    __doc__ = 'Attaches HTTP Proxy Authentication to a given Request object.'

    def __call__(self, r):
        r.headers['Proxy-Authorization'] = _basic_auth_str(self.username, self.password)
        return r


class HTTPDigestAuth(AuthBase):
    __doc__ = 'Attaches HTTP Digest Authentication to the given Request object.'

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self._thread_local = threading.local()

    def init_per_thread_state(self):
        if not hasattr(self._thread_local, 'init'):
            self._thread_local.init = True
            self._thread_local.last_nonce = ''
            self._thread_local.nonce_count = 0
            self._thread_local.chal = {}
            self._thread_local.pos = None
            self._thread_local.num_401_calls = None

    def build_digest_header--- This code section failed: ---

 L. 132         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _thread_local
                4  LOAD_ATTR                chal
                6  LOAD_STR                 'realm'
                8  BINARY_SUBSCR    
               10  STORE_FAST               'realm'

 L. 133        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _thread_local
               16  LOAD_ATTR                chal
               18  LOAD_STR                 'nonce'
               20  BINARY_SUBSCR    
               22  STORE_FAST               'nonce'

 L. 134        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _thread_local
               28  LOAD_ATTR                chal
               30  LOAD_METHOD              get
               32  LOAD_STR                 'qop'
               34  CALL_METHOD_1         1  ''
               36  STORE_FAST               'qop'

 L. 135        38  LOAD_FAST                'self'
               40  LOAD_ATTR                _thread_local
               42  LOAD_ATTR                chal
               44  LOAD_METHOD              get
               46  LOAD_STR                 'algorithm'
               48  CALL_METHOD_1         1  ''
               50  STORE_FAST               'algorithm'

 L. 136        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _thread_local
               56  LOAD_ATTR                chal
               58  LOAD_METHOD              get
               60  LOAD_STR                 'opaque'
               62  CALL_METHOD_1         1  ''
               64  STORE_FAST               'opaque'

 L. 137        66  LOAD_CONST               None
               68  STORE_DEREF              'hash_utf8'

 L. 139        70  LOAD_FAST                'algorithm'
               72  LOAD_CONST               None
               74  <117>                 0  ''
               76  POP_JUMP_IF_FALSE    84  'to 84'

 L. 140        78  LOAD_STR                 'MD5'
               80  STORE_FAST               '_algorithm'
               82  JUMP_FORWARD         92  'to 92'
             84_0  COME_FROM            76  '76'

 L. 142        84  LOAD_FAST                'algorithm'
               86  LOAD_METHOD              upper
               88  CALL_METHOD_0         0  ''
               90  STORE_FAST               '_algorithm'
             92_0  COME_FROM            82  '82'

 L. 144        92  LOAD_FAST                '_algorithm'
               94  LOAD_STR                 'MD5'
               96  COMPARE_OP               ==
               98  POP_JUMP_IF_TRUE    108  'to 108'
              100  LOAD_FAST                '_algorithm'
              102  LOAD_STR                 'MD5-SESS'
              104  COMPARE_OP               ==
              106  POP_JUMP_IF_FALSE   122  'to 122'
            108_0  COME_FROM            98  '98'

 L. 145       108  LOAD_CODE                <code_object md5_utf8>
              110  LOAD_STR                 'HTTPDigestAuth.build_digest_header.<locals>.md5_utf8'
              112  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              114  STORE_FAST               'md5_utf8'

 L. 149       116  LOAD_FAST                'md5_utf8'
              118  STORE_DEREF              'hash_utf8'
              120  JUMP_FORWARD        186  'to 186'
            122_0  COME_FROM           106  '106'

 L. 150       122  LOAD_FAST                '_algorithm'
              124  LOAD_STR                 'SHA'
              126  COMPARE_OP               ==
              128  POP_JUMP_IF_FALSE   144  'to 144'

 L. 151       130  LOAD_CODE                <code_object sha_utf8>
              132  LOAD_STR                 'HTTPDigestAuth.build_digest_header.<locals>.sha_utf8'
              134  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              136  STORE_FAST               'sha_utf8'

 L. 155       138  LOAD_FAST                'sha_utf8'
              140  STORE_DEREF              'hash_utf8'
              142  JUMP_FORWARD        186  'to 186'
            144_0  COME_FROM           128  '128'

 L. 156       144  LOAD_FAST                '_algorithm'
              146  LOAD_STR                 'SHA-256'
              148  COMPARE_OP               ==
              150  POP_JUMP_IF_FALSE   166  'to 166'

 L. 157       152  LOAD_CODE                <code_object sha256_utf8>
              154  LOAD_STR                 'HTTPDigestAuth.build_digest_header.<locals>.sha256_utf8'
              156  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              158  STORE_FAST               'sha256_utf8'

 L. 161       160  LOAD_FAST                'sha256_utf8'
              162  STORE_DEREF              'hash_utf8'
              164  JUMP_FORWARD        186  'to 186'
            166_0  COME_FROM           150  '150'

 L. 162       166  LOAD_FAST                '_algorithm'
              168  LOAD_STR                 'SHA-512'
              170  COMPARE_OP               ==
              172  POP_JUMP_IF_FALSE   186  'to 186'

 L. 163       174  LOAD_CODE                <code_object sha512_utf8>
              176  LOAD_STR                 'HTTPDigestAuth.build_digest_header.<locals>.sha512_utf8'
              178  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              180  STORE_FAST               'sha512_utf8'

 L. 167       182  LOAD_FAST                'sha512_utf8'
              184  STORE_DEREF              'hash_utf8'
            186_0  COME_FROM           172  '172'
            186_1  COME_FROM           164  '164'
            186_2  COME_FROM           142  '142'
            186_3  COME_FROM           120  '120'

 L. 169       186  LOAD_CLOSURE             'hash_utf8'
              188  BUILD_TUPLE_1         1 
              190  LOAD_LAMBDA              '<code_object <lambda>>'
              192  LOAD_STR                 'HTTPDigestAuth.build_digest_header.<locals>.<lambda>'
              194  MAKE_FUNCTION_8          'closure'
              196  STORE_FAST               'KD'

 L. 171       198  LOAD_DEREF               'hash_utf8'
              200  LOAD_CONST               None
              202  <117>                 0  ''
              204  POP_JUMP_IF_FALSE   210  'to 210'

 L. 172       206  LOAD_CONST               None
              208  RETURN_VALUE     
            210_0  COME_FROM           204  '204'

 L. 175       210  LOAD_CONST               None
              212  STORE_FAST               'entdig'

 L. 176       214  LOAD_GLOBAL              urlparse
              216  LOAD_FAST                'url'
              218  CALL_FUNCTION_1       1  ''
              220  STORE_FAST               'p_parsed'

 L. 178       222  LOAD_FAST                'p_parsed'
              224  LOAD_ATTR                path
              226  JUMP_IF_TRUE_OR_POP   230  'to 230'
              228  LOAD_STR                 '/'
            230_0  COME_FROM           226  '226'
              230  STORE_FAST               'path'

 L. 179       232  LOAD_FAST                'p_parsed'
              234  LOAD_ATTR                query
              236  POP_JUMP_IF_FALSE   252  'to 252'

 L. 180       238  LOAD_FAST                'path'
              240  LOAD_STR                 '?'
              242  LOAD_FAST                'p_parsed'
              244  LOAD_ATTR                query
              246  BINARY_ADD       
              248  INPLACE_ADD      
              250  STORE_FAST               'path'
            252_0  COME_FROM           236  '236'

 L. 182       252  LOAD_STR                 '%s:%s:%s'
              254  LOAD_FAST                'self'
              256  LOAD_ATTR                username
              258  LOAD_FAST                'realm'
              260  LOAD_FAST                'self'
              262  LOAD_ATTR                password
              264  BUILD_TUPLE_3         3 
              266  BINARY_MODULO    
              268  STORE_FAST               'A1'

 L. 183       270  LOAD_STR                 '%s:%s'
              272  LOAD_FAST                'method'
              274  LOAD_FAST                'path'
              276  BUILD_TUPLE_2         2 
              278  BINARY_MODULO    
              280  STORE_FAST               'A2'

 L. 185       282  LOAD_DEREF               'hash_utf8'
              284  LOAD_FAST                'A1'
              286  CALL_FUNCTION_1       1  ''
              288  STORE_FAST               'HA1'

 L. 186       290  LOAD_DEREF               'hash_utf8'
              292  LOAD_FAST                'A2'
              294  CALL_FUNCTION_1       1  ''
              296  STORE_FAST               'HA2'

 L. 188       298  LOAD_FAST                'nonce'
              300  LOAD_FAST                'self'
              302  LOAD_ATTR                _thread_local
              304  LOAD_ATTR                last_nonce
              306  COMPARE_OP               ==
          308_310  POP_JUMP_IF_FALSE   330  'to 330'

 L. 189       312  LOAD_FAST                'self'
              314  LOAD_ATTR                _thread_local
              316  DUP_TOP          
              318  LOAD_ATTR                nonce_count
              320  LOAD_CONST               1
              322  INPLACE_ADD      
              324  ROT_TWO          
              326  STORE_ATTR               nonce_count
              328  JUMP_FORWARD        338  'to 338'
            330_0  COME_FROM           308  '308'

 L. 191       330  LOAD_CONST               1
              332  LOAD_FAST                'self'
              334  LOAD_ATTR                _thread_local
              336  STORE_ATTR               nonce_count
            338_0  COME_FROM           328  '328'

 L. 192       338  LOAD_STR                 '%08x'
              340  LOAD_FAST                'self'
              342  LOAD_ATTR                _thread_local
              344  LOAD_ATTR                nonce_count
              346  BINARY_MODULO    
              348  STORE_FAST               'ncvalue'

 L. 193       350  LOAD_GLOBAL              str
              352  LOAD_FAST                'self'
              354  LOAD_ATTR                _thread_local
              356  LOAD_ATTR                nonce_count
              358  CALL_FUNCTION_1       1  ''
              360  LOAD_METHOD              encode
              362  LOAD_STR                 'utf-8'
              364  CALL_METHOD_1         1  ''
              366  STORE_FAST               's'

 L. 194       368  LOAD_FAST                's'
              370  LOAD_FAST                'nonce'
              372  LOAD_METHOD              encode
              374  LOAD_STR                 'utf-8'
              376  CALL_METHOD_1         1  ''
              378  INPLACE_ADD      
              380  STORE_FAST               's'

 L. 195       382  LOAD_FAST                's'
              384  LOAD_GLOBAL              time
              386  LOAD_METHOD              ctime
              388  CALL_METHOD_0         0  ''
              390  LOAD_METHOD              encode
              392  LOAD_STR                 'utf-8'
              394  CALL_METHOD_1         1  ''
              396  INPLACE_ADD      
              398  STORE_FAST               's'

 L. 196       400  LOAD_FAST                's'
              402  LOAD_GLOBAL              os
              404  LOAD_METHOD              urandom
              406  LOAD_CONST               8
              408  CALL_METHOD_1         1  ''
              410  INPLACE_ADD      
              412  STORE_FAST               's'

 L. 198       414  LOAD_GLOBAL              hashlib
              416  LOAD_METHOD              sha1
              418  LOAD_FAST                's'
              420  CALL_METHOD_1         1  ''
              422  LOAD_METHOD              hexdigest
              424  CALL_METHOD_0         0  ''
              426  LOAD_CONST               None
              428  LOAD_CONST               16
              430  BUILD_SLICE_2         2 
              432  BINARY_SUBSCR    
              434  STORE_FAST               'cnonce'

 L. 199       436  LOAD_FAST                '_algorithm'
              438  LOAD_STR                 'MD5-SESS'
              440  COMPARE_OP               ==
          442_444  POP_JUMP_IF_FALSE   464  'to 464'

 L. 200       446  LOAD_DEREF               'hash_utf8'
              448  LOAD_STR                 '%s:%s:%s'
              450  LOAD_FAST                'HA1'
              452  LOAD_FAST                'nonce'
              454  LOAD_FAST                'cnonce'
              456  BUILD_TUPLE_3         3 
              458  BINARY_MODULO    
              460  CALL_FUNCTION_1       1  ''
              462  STORE_FAST               'HA1'
            464_0  COME_FROM           442  '442'

 L. 202       464  LOAD_FAST                'qop'
          466_468  POP_JUMP_IF_TRUE    490  'to 490'

 L. 203       470  LOAD_FAST                'KD'
              472  LOAD_FAST                'HA1'
              474  LOAD_STR                 '%s:%s'
              476  LOAD_FAST                'nonce'
              478  LOAD_FAST                'HA2'
              480  BUILD_TUPLE_2         2 
              482  BINARY_MODULO    
              484  CALL_FUNCTION_2       2  ''
              486  STORE_FAST               'respdig'
              488  JUMP_FORWARD        550  'to 550'
            490_0  COME_FROM           466  '466'

 L. 204       490  LOAD_FAST                'qop'
              492  LOAD_STR                 'auth'
              494  COMPARE_OP               ==
          496_498  POP_JUMP_IF_TRUE    516  'to 516'
              500  LOAD_STR                 'auth'
              502  LOAD_FAST                'qop'
              504  LOAD_METHOD              split
              506  LOAD_STR                 ','
              508  CALL_METHOD_1         1  ''
              510  <118>                 0  ''
          512_514  POP_JUMP_IF_FALSE   546  'to 546'
            516_0  COME_FROM           496  '496'

 L. 205       516  LOAD_STR                 '%s:%s:%s:%s:%s'

 L. 206       518  LOAD_FAST                'nonce'
              520  LOAD_FAST                'ncvalue'
              522  LOAD_FAST                'cnonce'
              524  LOAD_STR                 'auth'
              526  LOAD_FAST                'HA2'

 L. 205       528  BUILD_TUPLE_5         5 
              530  BINARY_MODULO    
              532  STORE_FAST               'noncebit'

 L. 208       534  LOAD_FAST                'KD'
              536  LOAD_FAST                'HA1'
              538  LOAD_FAST                'noncebit'
              540  CALL_FUNCTION_2       2  ''
              542  STORE_FAST               'respdig'
              544  JUMP_FORWARD        550  'to 550'
            546_0  COME_FROM           512  '512'

 L. 211       546  LOAD_CONST               None
              548  RETURN_VALUE     
            550_0  COME_FROM           544  '544'
            550_1  COME_FROM           488  '488'

 L. 213       550  LOAD_FAST                'nonce'
              552  LOAD_FAST                'self'
              554  LOAD_ATTR                _thread_local
              556  STORE_ATTR               last_nonce

 L. 216       558  LOAD_STR                 'username="%s", realm="%s", nonce="%s", uri="%s", response="%s"'

 L. 217       560  LOAD_FAST                'self'
              562  LOAD_ATTR                username
              564  LOAD_FAST                'realm'
              566  LOAD_FAST                'nonce'
              568  LOAD_FAST                'path'
              570  LOAD_FAST                'respdig'
              572  BUILD_TUPLE_5         5 

 L. 216       574  BINARY_MODULO    
              576  STORE_FAST               'base'

 L. 218       578  LOAD_FAST                'opaque'
          580_582  POP_JUMP_IF_FALSE   596  'to 596'

 L. 219       584  LOAD_FAST                'base'
              586  LOAD_STR                 ', opaque="%s"'
              588  LOAD_FAST                'opaque'
              590  BINARY_MODULO    
              592  INPLACE_ADD      
              594  STORE_FAST               'base'
            596_0  COME_FROM           580  '580'

 L. 220       596  LOAD_FAST                'algorithm'
          598_600  POP_JUMP_IF_FALSE   614  'to 614'

 L. 221       602  LOAD_FAST                'base'
              604  LOAD_STR                 ', algorithm="%s"'
              606  LOAD_FAST                'algorithm'
              608  BINARY_MODULO    
              610  INPLACE_ADD      
              612  STORE_FAST               'base'
            614_0  COME_FROM           598  '598'

 L. 222       614  LOAD_FAST                'entdig'
          616_618  POP_JUMP_IF_FALSE   632  'to 632'

 L. 223       620  LOAD_FAST                'base'
              622  LOAD_STR                 ', digest="%s"'
              624  LOAD_FAST                'entdig'
              626  BINARY_MODULO    
              628  INPLACE_ADD      
              630  STORE_FAST               'base'
            632_0  COME_FROM           616  '616'

 L. 224       632  LOAD_FAST                'qop'
          634_636  POP_JUMP_IF_FALSE   654  'to 654'

 L. 225       638  LOAD_FAST                'base'
              640  LOAD_STR                 ', qop="auth", nc=%s, cnonce="%s"'
              642  LOAD_FAST                'ncvalue'
              644  LOAD_FAST                'cnonce'
              646  BUILD_TUPLE_2         2 
              648  BINARY_MODULO    
              650  INPLACE_ADD      
              652  STORE_FAST               'base'
            654_0  COME_FROM           634  '634'

 L. 227       654  LOAD_STR                 'Digest %s'
              656  LOAD_FAST                'base'
              658  BINARY_MODULO    
              660  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 74

    def handle_redirect(self, r, **kwargs):
        """Reset num_401_calls counter on redirects."""
        if r.is_redirect:
            self._thread_local.num_401_calls = 1

    def handle_401--- This code section failed: ---

 L. 243         0  LOAD_CONST               400
                2  LOAD_FAST                'r'
                4  LOAD_ATTR                status_code
                6  DUP_TOP          
                8  ROT_THREE        
               10  COMPARE_OP               <=
               12  POP_JUMP_IF_FALSE    22  'to 22'
               14  LOAD_CONST               500
               16  COMPARE_OP               <
               18  POP_JUMP_IF_TRUE     36  'to 36'
               20  JUMP_FORWARD         24  'to 24'
             22_0  COME_FROM            12  '12'
               22  POP_TOP          
             24_0  COME_FROM            20  '20'

 L. 244        24  LOAD_CONST               1
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                _thread_local
               30  STORE_ATTR               num_401_calls

 L. 245        32  LOAD_FAST                'r'
               34  RETURN_VALUE     
             36_0  COME_FROM            18  '18'

 L. 247        36  LOAD_FAST                'self'
               38  LOAD_ATTR                _thread_local
               40  LOAD_ATTR                pos
               42  LOAD_CONST               None
               44  <117>                 1  ''
               46  POP_JUMP_IF_FALSE    66  'to 66'

 L. 250        48  LOAD_FAST                'r'
               50  LOAD_ATTR                request
               52  LOAD_ATTR                body
               54  LOAD_METHOD              seek
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                _thread_local
               60  LOAD_ATTR                pos
               62  CALL_METHOD_1         1  ''
               64  POP_TOP          
             66_0  COME_FROM            46  '46'

 L. 251        66  LOAD_FAST                'r'
               68  LOAD_ATTR                headers
               70  LOAD_METHOD              get
               72  LOAD_STR                 'www-authenticate'
               74  LOAD_STR                 ''
               76  CALL_METHOD_2         2  ''
               78  STORE_FAST               's_auth'

 L. 253        80  LOAD_STR                 'digest'
               82  LOAD_FAST                's_auth'
               84  LOAD_METHOD              lower
               86  CALL_METHOD_0         0  ''
               88  <118>                 0  ''
            90_92  POP_JUMP_IF_FALSE   282  'to 282'
               94  LOAD_FAST                'self'
               96  LOAD_ATTR                _thread_local
               98  LOAD_ATTR                num_401_calls
              100  LOAD_CONST               2
              102  COMPARE_OP               <
          104_106  POP_JUMP_IF_FALSE   282  'to 282'

 L. 255       108  LOAD_FAST                'self'
              110  LOAD_ATTR                _thread_local
              112  DUP_TOP          
              114  LOAD_ATTR                num_401_calls
              116  LOAD_CONST               1
              118  INPLACE_ADD      
              120  ROT_TWO          
              122  STORE_ATTR               num_401_calls

 L. 256       124  LOAD_GLOBAL              re
              126  LOAD_ATTR                compile
              128  LOAD_STR                 'digest '
              130  LOAD_GLOBAL              re
              132  LOAD_ATTR                IGNORECASE
              134  LOAD_CONST               ('flags',)
              136  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              138  STORE_FAST               'pat'

 L. 257       140  LOAD_GLOBAL              parse_dict_header
              142  LOAD_FAST                'pat'
              144  LOAD_ATTR                sub
              146  LOAD_STR                 ''
              148  LOAD_FAST                's_auth'
              150  LOAD_CONST               1
              152  LOAD_CONST               ('count',)
              154  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              156  CALL_FUNCTION_1       1  ''
              158  LOAD_FAST                'self'
              160  LOAD_ATTR                _thread_local
              162  STORE_ATTR               chal

 L. 261       164  LOAD_FAST                'r'
              166  LOAD_ATTR                content
              168  POP_TOP          

 L. 262       170  LOAD_FAST                'r'
              172  LOAD_METHOD              close
              174  CALL_METHOD_0         0  ''
              176  POP_TOP          

 L. 263       178  LOAD_FAST                'r'
              180  LOAD_ATTR                request
              182  LOAD_METHOD              copy
              184  CALL_METHOD_0         0  ''
              186  STORE_FAST               'prep'

 L. 264       188  LOAD_GLOBAL              extract_cookies_to_jar
              190  LOAD_FAST                'prep'
              192  LOAD_ATTR                _cookies
              194  LOAD_FAST                'r'
              196  LOAD_ATTR                request
              198  LOAD_FAST                'r'
              200  LOAD_ATTR                raw
              202  CALL_FUNCTION_3       3  ''
              204  POP_TOP          

 L. 265       206  LOAD_FAST                'prep'
              208  LOAD_METHOD              prepare_cookies
              210  LOAD_FAST                'prep'
              212  LOAD_ATTR                _cookies
              214  CALL_METHOD_1         1  ''
              216  POP_TOP          

 L. 267       218  LOAD_FAST                'self'
              220  LOAD_METHOD              build_digest_header

 L. 268       222  LOAD_FAST                'prep'
              224  LOAD_ATTR                method
              226  LOAD_FAST                'prep'
              228  LOAD_ATTR                url

 L. 267       230  CALL_METHOD_2         2  ''
              232  LOAD_FAST                'prep'
              234  LOAD_ATTR                headers
              236  LOAD_STR                 'Authorization'
              238  STORE_SUBSCR     

 L. 269       240  LOAD_FAST                'r'
              242  LOAD_ATTR                connection
              244  LOAD_ATTR                send
              246  LOAD_FAST                'prep'
              248  BUILD_TUPLE_1         1 
              250  BUILD_MAP_0           0 
              252  LOAD_FAST                'kwargs'
              254  <164>                 1  ''
              256  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              258  STORE_FAST               '_r'

 L. 270       260  LOAD_FAST                '_r'
              262  LOAD_ATTR                history
              264  LOAD_METHOD              append
              266  LOAD_FAST                'r'
              268  CALL_METHOD_1         1  ''
              270  POP_TOP          

 L. 271       272  LOAD_FAST                'prep'
              274  LOAD_FAST                '_r'
              276  STORE_ATTR               request

 L. 273       278  LOAD_FAST                '_r'
              280  RETURN_VALUE     
            282_0  COME_FROM           104  '104'
            282_1  COME_FROM            90  '90'

 L. 275       282  LOAD_CONST               1
              284  LOAD_FAST                'self'
              286  LOAD_ATTR                _thread_local
              288  STORE_ATTR               num_401_calls

 L. 276       290  LOAD_FAST                'r'
              292  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 44

    def __call__--- This code section failed: ---

 L. 280         0  LOAD_FAST                'self'
                2  LOAD_METHOD              init_per_thread_state
                4  CALL_METHOD_0         0  ''
                6  POP_TOP          

 L. 282         8  LOAD_FAST                'self'
               10  LOAD_ATTR                _thread_local
               12  LOAD_ATTR                last_nonce
               14  POP_JUMP_IF_FALSE    38  'to 38'

 L. 283        16  LOAD_FAST                'self'
               18  LOAD_METHOD              build_digest_header
               20  LOAD_FAST                'r'
               22  LOAD_ATTR                method
               24  LOAD_FAST                'r'
               26  LOAD_ATTR                url
               28  CALL_METHOD_2         2  ''
               30  LOAD_FAST                'r'
               32  LOAD_ATTR                headers
               34  LOAD_STR                 'Authorization'
               36  STORE_SUBSCR     
             38_0  COME_FROM            14  '14'

 L. 284        38  SETUP_FINALLY        58  'to 58'

 L. 285        40  LOAD_FAST                'r'
               42  LOAD_ATTR                body
               44  LOAD_METHOD              tell
               46  CALL_METHOD_0         0  ''
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                _thread_local
               52  STORE_ATTR               pos
               54  POP_BLOCK        
               56  JUMP_FORWARD         84  'to 84'
             58_0  COME_FROM_FINALLY    38  '38'

 L. 286        58  DUP_TOP          
               60  LOAD_GLOBAL              AttributeError
               62  <121>                82  ''
               64  POP_TOP          
               66  POP_TOP          
               68  POP_TOP          

 L. 291        70  LOAD_CONST               None
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                _thread_local
               76  STORE_ATTR               pos
               78  POP_EXCEPT       
               80  JUMP_FORWARD         84  'to 84'
               82  <48>             
             84_0  COME_FROM            80  '80'
             84_1  COME_FROM            56  '56'

 L. 292        84  LOAD_FAST                'r'
               86  LOAD_METHOD              register_hook
               88  LOAD_STR                 'response'
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                handle_401
               94  CALL_METHOD_2         2  ''
               96  POP_TOP          

 L. 293        98  LOAD_FAST                'r'
              100  LOAD_METHOD              register_hook
              102  LOAD_STR                 'response'
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                handle_redirect
              108  CALL_METHOD_2         2  ''
              110  POP_TOP          

 L. 294       112  LOAD_CONST               1
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                _thread_local
              118  STORE_ATTR               num_401_calls

 L. 296       120  LOAD_FAST                'r'
              122  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 62

    def __eq__(self, other):
        return all([
         self.username == getattr(other, 'username', None),
         self.password == getattr(other, 'password', None)])

    def __ne__(self, other):
        return not self == other