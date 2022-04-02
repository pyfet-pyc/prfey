# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\mechanize\_clientcookie.py
from __future__ import absolute_import
import re, time
from .polyglot import Cookie as _Cookie, CookieJar as CJ, MozillaCookieJar as MCJ, request_host as request_host_lc, DEFAULT_HTTP_PORT, CookiePolicy, DefaultCookiePolicy, FileCookieJar, LoadError, LWPCookieJar, _debug, domain_match, eff_request_host, escape_path, is_HDN, lwp_cookie_str, reach, request_path, request_port, user_domain_match, iteritems
__all__ = [
 'DEFAULT_HTTP_PORT', 'CookiePolicy', 'DefaultCookiePolicy',
 'request_host_lc', 'MozillaCookieJar', 'escape_path', 'is_HDN',
 'request_port', 'LWPCookieJar', 'LoadError', 'reach', 'FileCookieJar',
 'lwp_cookie_str', 'domain_match', 'request_path', 'user_domain_match']

def effective_request_host(request):
    """Return the effective request-host, as defined by RFC 2965."""
    return eff_request_host(request)[1]


def request_is_unverifiable(request):
    try:
        return request.is_unverifiable()
    except AttributeError:
        if hasattr(request, 'unverifiable'):
            return request.unverifiable
        raise


def cookies_equal(a, b):
    return all((getattr(a, x) == getattr(b, x) for x in Cookie._attrs))


class Cookie(_Cookie):
    _attrs = ('version', 'name', 'value', 'port', 'port_specified', 'domain', 'domain_specified',
              'domain_initial_dot', 'path', 'path_specified', 'secure', 'expires',
              'discard', 'comment', 'comment_url', 'rfc2109', '_rest')

    def __eq__(self, other):
        return all((getattr(self, a) == getattr(other, a) for a in self._attrs))

    def __ne__(self, other):
        return not self == other


class CookieJar(CJ):

    def __getstate__(self):
        ans = self.__dict__.copy()
        del ans['_cookies_lock']
        return ans

    def __setstate__(self, val):
        for k, v in iteritems(val):
            setattr(self, k, v)

    def cookies_for_request(self, request):
        """Return a list of cookies to be returned to server.

        The returned list of cookie instances is sorted in the order they
        should appear in the Cookie: header for return to the server.

        See add_cookie_header.__doc__ for the interface required of the
        request argument.
        """
        with self._cookies_lock:
            self._policy._now = self._now = int(time.time())
            cookies = self._cookies_for_request(request)

            def key(x):
                return len(x.path)

            cookies.sort(key=key, reverse=True)
            return cookies

    def get_policy(self):
        return self._policy

    def _normalized_cookie_tuples--- This code section failed: ---

 L.  99         0  BUILD_LIST_0          0 
                2  STORE_FAST               'cookie_tuples'

 L. 101         4  LOAD_CONST               ('discard', 'secure')
                6  STORE_FAST               'boolean_attrs'

 L. 102         8  LOAD_CONST               ('version', 'expires', 'max-age', 'domain', 'path', 'port', 'comment', 'commenturl')
               10  STORE_FAST               'value_attrs'

 L. 105        12  LOAD_FAST                'attrs_set'
               14  GET_ITER         
             16_0  COME_FROM           416  '416'
             16_1  COME_FROM           396  '396'
            16_18  FOR_ITER            418  'to 418'
               20  STORE_FAST               'cookie_attrs'

 L. 106        22  LOAD_FAST                'cookie_attrs'
               24  LOAD_CONST               0
               26  BINARY_SUBSCR    
               28  UNPACK_SEQUENCE_2     2 
               30  STORE_FAST               'name'
               32  STORE_FAST               'value'

 L. 116        34  LOAD_CONST               False
               36  STORE_FAST               'max_age_set'

 L. 118        38  LOAD_CONST               False
               40  STORE_FAST               'bad_cookie'

 L. 120        42  BUILD_MAP_0           0 
               44  STORE_FAST               'standard'

 L. 121        46  BUILD_MAP_0           0 
               48  STORE_FAST               'rest'

 L. 122        50  LOAD_FAST                'cookie_attrs'
               52  LOAD_CONST               1
               54  LOAD_CONST               None
               56  BUILD_SLICE_2         2 
               58  BINARY_SUBSCR    
               60  GET_ITER         
             62_0  COME_FROM           388  '388'
             62_1  COME_FROM           378  '378'
             62_2  COME_FROM           202  '202'
             62_3  COME_FROM           184  '184'
             62_4  COME_FROM           128  '128'
            62_64  FOR_ITER            390  'to 390'
               66  UNPACK_SEQUENCE_2     2 
               68  STORE_FAST               'k'
               70  STORE_FAST               'v'

 L. 123        72  LOAD_FAST                'k'
               74  LOAD_METHOD              lower
               76  CALL_METHOD_0         0  ''
               78  STORE_FAST               'lc'

 L. 125        80  LOAD_FAST                'lc'
               82  LOAD_FAST                'value_attrs'
               84  COMPARE_OP               in
               86  POP_JUMP_IF_TRUE     96  'to 96'
               88  LOAD_FAST                'lc'
               90  LOAD_FAST                'boolean_attrs'
               92  COMPARE_OP               in
               94  POP_JUMP_IF_FALSE   100  'to 100'
             96_0  COME_FROM            86  '86'

 L. 126        96  LOAD_FAST                'lc'
               98  STORE_FAST               'k'
            100_0  COME_FROM            94  '94'

 L. 127       100  LOAD_FAST                'k'
              102  LOAD_FAST                'boolean_attrs'
              104  COMPARE_OP               in
              106  POP_JUMP_IF_FALSE   120  'to 120'
              108  LOAD_FAST                'v'
              110  LOAD_CONST               None
              112  COMPARE_OP               is
              114  POP_JUMP_IF_FALSE   120  'to 120'

 L. 130       116  LOAD_CONST               True
              118  STORE_FAST               'v'
            120_0  COME_FROM           114  '114'
            120_1  COME_FROM           106  '106'

 L. 131       120  LOAD_FAST                'k'
              122  LOAD_FAST                'standard'
              124  COMPARE_OP               in
              126  POP_JUMP_IF_FALSE   130  'to 130'

 L. 133       128  JUMP_BACK            62  'to 62'
            130_0  COME_FROM           126  '126'

 L. 134       130  LOAD_FAST                'k'
              132  LOAD_STR                 'domain'
              134  COMPARE_OP               ==
              136  POP_JUMP_IF_FALSE   172  'to 172'

 L. 135       138  LOAD_FAST                'v'
              140  LOAD_CONST               None
              142  COMPARE_OP               is
              144  POP_JUMP_IF_FALSE   164  'to 164'

 L. 136       146  LOAD_GLOBAL              _debug
              148  LOAD_STR                 '   missing value for domain attribute'
              150  CALL_FUNCTION_1       1  ''
              152  POP_TOP          

 L. 137       154  LOAD_CONST               True
              156  STORE_FAST               'bad_cookie'

 L. 138       158  POP_TOP          
          160_162  JUMP_FORWARD        390  'to 390'
            164_0  COME_FROM           144  '144'

 L. 140       164  LOAD_FAST                'v'
              166  LOAD_METHOD              lower
              168  CALL_METHOD_0         0  ''
              170  STORE_FAST               'v'
            172_0  COME_FROM           136  '136'

 L. 141       172  LOAD_FAST                'k'
              174  LOAD_STR                 'expires'
              176  COMPARE_OP               ==
              178  POP_JUMP_IF_FALSE   204  'to 204'

 L. 142       180  LOAD_FAST                'max_age_set'
              182  POP_JUMP_IF_FALSE   186  'to 186'

 L. 144       184  JUMP_BACK            62  'to 62'
            186_0  COME_FROM           182  '182'

 L. 145       186  LOAD_FAST                'v'
              188  LOAD_CONST               None
              190  COMPARE_OP               is
              192  POP_JUMP_IF_FALSE   204  'to 204'

 L. 146       194  LOAD_GLOBAL              _debug
              196  LOAD_STR                 '   missing or invalid value for expires attribute: treating as session cookie'
              198  CALL_FUNCTION_1       1  ''
              200  POP_TOP          

 L. 148       202  JUMP_BACK            62  'to 62'
            204_0  COME_FROM           192  '192'
            204_1  COME_FROM           178  '178'

 L. 149       204  LOAD_FAST                'k'
              206  LOAD_STR                 'max-age'
              208  COMPARE_OP               ==
          210_212  POP_JUMP_IF_FALSE   288  'to 288'

 L. 150       214  LOAD_CONST               True
              216  STORE_FAST               'max_age_set'

 L. 151       218  SETUP_FINALLY       232  'to 232'

 L. 152       220  LOAD_GLOBAL              int
              222  LOAD_FAST                'v'
              224  CALL_FUNCTION_1       1  ''
              226  STORE_FAST               'v'
              228  POP_BLOCK        
              230  JUMP_FORWARD        274  'to 274'
            232_0  COME_FROM_FINALLY   218  '218'

 L. 153       232  DUP_TOP          
              234  LOAD_GLOBAL              ValueError
              236  COMPARE_OP               exception-match
          238_240  POP_JUMP_IF_FALSE   272  'to 272'
              242  POP_TOP          
              244  POP_TOP          
              246  POP_TOP          

 L. 154       248  LOAD_GLOBAL              _debug
              250  LOAD_STR                 '   missing or invalid (non-numeric) value for max-age attribute'
              252  CALL_FUNCTION_1       1  ''
              254  POP_TOP          

 L. 156       256  LOAD_CONST               True
              258  STORE_FAST               'bad_cookie'

 L. 157       260  POP_EXCEPT       
              262  POP_TOP          
          264_266  JUMP_FORWARD        390  'to 390'
              268  POP_EXCEPT       
              270  JUMP_FORWARD        274  'to 274'
            272_0  COME_FROM           238  '238'
              272  END_FINALLY      
            274_0  COME_FROM           270  '270'
            274_1  COME_FROM           230  '230'

 L. 162       274  LOAD_STR                 'expires'
              276  STORE_FAST               'k'

 L. 163       278  LOAD_FAST                'self'
              280  LOAD_ATTR                _now
              282  LOAD_FAST                'v'
              284  BINARY_ADD       
              286  STORE_FAST               'v'
            288_0  COME_FROM           210  '210'

 L. 164       288  LOAD_FAST                'v'
          290_292  POP_JUMP_IF_TRUE    308  'to 308'
              294  LOAD_FAST                'k'
              296  LOAD_STR                 'path'
              298  COMPARE_OP               ==
          300_302  POP_JUMP_IF_FALSE   308  'to 308'

 L. 166       304  LOAD_STR                 '/'
              306  STORE_FAST               'v'
            308_0  COME_FROM           300  '300'
            308_1  COME_FROM           290  '290'

 L. 167       308  LOAD_FAST                'k'
              310  LOAD_FAST                'value_attrs'
              312  COMPARE_OP               in
          314_316  POP_JUMP_IF_TRUE    328  'to 328'
              318  LOAD_FAST                'k'
              320  LOAD_FAST                'boolean_attrs'
              322  COMPARE_OP               in
          324_326  POP_JUMP_IF_FALSE   380  'to 380'
            328_0  COME_FROM           314  '314'

 L. 168       328  LOAD_FAST                'v'
              330  LOAD_CONST               None
              332  COMPARE_OP               is
          334_336  POP_JUMP_IF_FALSE   370  'to 370'

 L. 169       338  LOAD_FAST                'k'
              340  LOAD_CONST               ('port', 'comment', 'commenturl')
              342  COMPARE_OP               not-in

 L. 168   344_346  POP_JUMP_IF_FALSE   370  'to 370'

 L. 170       348  LOAD_GLOBAL              _debug
              350  LOAD_STR                 '   missing value for %s attribute'
              352  LOAD_FAST                'k'
              354  BINARY_MODULO    
              356  CALL_FUNCTION_1       1  ''
              358  POP_TOP          

 L. 171       360  LOAD_CONST               True
              362  STORE_FAST               'bad_cookie'

 L. 172       364  POP_TOP          
          366_368  JUMP_FORWARD        390  'to 390'
            370_0  COME_FROM           344  '344'
            370_1  COME_FROM           334  '334'

 L. 173       370  LOAD_FAST                'v'
              372  LOAD_FAST                'standard'
              374  LOAD_FAST                'k'
              376  STORE_SUBSCR     
              378  JUMP_BACK            62  'to 62'
            380_0  COME_FROM           324  '324'

 L. 175       380  LOAD_FAST                'v'
              382  LOAD_FAST                'rest'
              384  LOAD_FAST                'k'
              386  STORE_SUBSCR     
              388  JUMP_BACK            62  'to 62'
            390_0  COME_FROM           366  '366'
            390_1  COME_FROM           264  '264'
            390_2  COME_FROM           160  '160'
            390_3  COME_FROM            62  '62'

 L. 177       390  LOAD_FAST                'bad_cookie'
          392_394  POP_JUMP_IF_FALSE   398  'to 398'

 L. 178       396  JUMP_BACK            16  'to 16'
            398_0  COME_FROM           392  '392'

 L. 180       398  LOAD_FAST                'cookie_tuples'
              400  LOAD_METHOD              append
              402  LOAD_FAST                'name'
              404  LOAD_FAST                'value'
              406  LOAD_FAST                'standard'
              408  LOAD_FAST                'rest'
              410  BUILD_TUPLE_4         4 
              412  CALL_METHOD_1         1  ''
              414  POP_TOP          
              416  JUMP_BACK            16  'to 16'
            418_0  COME_FROM            16  '16'

 L. 182       418  LOAD_FAST                'cookie_tuples'
              420  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 160_162

    def __getitem__(self, i):
        for q, ans in enumerate(self):
            if q == i:
                return ans
        else:
            raise IndexError()


class MozillaCookieJar(MCJ):

    def _really_load(self, f, filename, ignore_discard, ignore_expires):
        now = time.time()
        magic = f.readline()
        if not re.search(self.magic_re, magic):
            f.close()
            raise LoadError('%r does not look like a Netscape format cookies file' % filename)
        try:
            while True:
                line = f.readline()
                if line == '':
                    pass
                else:
                    if line.endswith('\n'):
                        line = line[:-1]
                    if not line.strip().startswith(('#', '$')):
                        if line.strip() == '':
                            pass
                        else:
                            domain, domain_specified, path, secure, expires, name, value = line.split('\t', 6)
                            secure = secure == 'TRUE'
                            domain_specified = domain_specified == 'TRUE'
                            if name == '':
                                name = value
                                value = None
                            initial_dot = domain.startswith('.')
                            if domain_specified != initial_dot:
                                raise ValueError()
                            assert domain_specified == initial_dot
                            discard = False
                            if expires == '':
                                expires = None
                                discard = True
                            c = Cookie(0, name, value, None, False, domain, domain_specified, initial_dot, path, False, secure, expires, discard, None, None, {})
                            if not ignore_discard or c.discard:
                                pass
                            else:
                                if not ignore_expires or c.is_expired(now):
                                    pass
                                else:
                                    self.set_cookie(c)

        except IOError:
            raise
        except Exception:
            raise LoadError('invalid Netscape format cookies file %r: %r' % (
             filename, line))