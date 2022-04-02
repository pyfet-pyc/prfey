# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\requests\packages\urllib3\poolmanager.py
import logging
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin
else:
    from ._collections import RecentlyUsedContainer
    from .connectionpool import HTTPConnectionPool, HTTPSConnectionPool
    from .connectionpool import port_by_scheme
    from .exceptions import LocationValueError, MaxRetryError
    from .request import RequestMethods
    from util.url import parse_url
    from util.retry import Retry
    __all__ = [
     'PoolManager', 'ProxyManager', 'proxy_from_url']
    pool_classes_by_scheme = {'http':HTTPConnectionPool, 
     'https':HTTPSConnectionPool}
    log = logging.getLogger(__name__)
    SSL_KEYWORDS = ('key_file', 'cert_file', 'cert_reqs', 'ca_certs', 'ssl_version')

    class PoolManager(RequestMethods):
        __doc__ = "\n    Allows for arbitrary requests while transparently keeping track of\n    necessary connection pools for you.\n\n    :param num_pools:\n        Number of connection pools to cache before discarding the least\n        recently used pool.\n\n    :param headers:\n        Headers to include with all requests, unless other headers are given\n        explicitly.\n\n    :param \\**connection_pool_kw:\n        Additional parameters are used to create fresh\n        :class:`urllib3.connectionpool.ConnectionPool` instances.\n\n    Example::\n\n        >>> manager = PoolManager(num_pools=2)\n        >>> r = manager.request('GET', 'http://google.com/')\n        >>> r = manager.request('GET', 'http://google.com/mail')\n        >>> r = manager.request('GET', 'http://yahoo.com/')\n        >>> len(manager.pools)\n        2\n\n    "
        proxy = None

        def __init__(self, num_pools=10, headers=None, **connection_pool_kw):
            RequestMethods.__init__(self, headers)
            self.connection_pool_kw = connection_pool_kw
            self.pools = RecentlyUsedContainer(num_pools, dispose_func=(lambda p: p.close()))

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.clear()
            return False

        def _new_pool(self, scheme, host, port):
            """
        Create a new :class:`ConnectionPool` based on host, port and scheme.

        This method is used to actually create the connection pools handed out
        by :meth:`connection_from_url` and companion methods. It is intended
        to be overridden for customization.
        """
            pool_cls = pool_classes_by_scheme[scheme]
            kwargs = self.connection_pool_kw
            if scheme == 'http':
                kwargs = self.connection_pool_kw.copy()
                for kw in SSL_KEYWORDS:
                    kwargs.pop(kw, None)

            return pool_cls(host, port, **kwargs)

        def clear(self):
            """
        Empty our store of pools and direct them all to close.

        This will not affect in-flight connections, but they will not be
        re-used after completion.
        """
            self.pools.clear()

        def connection_from_host--- This code section failed: ---

 L. 109         0  LOAD_FAST                'host'
                2  POP_JUMP_IF_TRUE     12  'to 12'

 L. 110         4  LOAD_GLOBAL              LocationValueError
                6  LOAD_STR                 'No host specified.'
                8  CALL_FUNCTION_1       1  ''
               10  RAISE_VARARGS_1       1  'exception instance'
             12_0  COME_FROM             2  '2'

 L. 112        12  LOAD_FAST                'scheme'
               14  JUMP_IF_TRUE_OR_POP    18  'to 18'
               16  LOAD_STR                 'http'
             18_0  COME_FROM            14  '14'
               18  STORE_FAST               'scheme'

 L. 113        20  LOAD_FAST                'port'
               22  JUMP_IF_TRUE_OR_POP    34  'to 34'
               24  LOAD_GLOBAL              port_by_scheme
               26  LOAD_METHOD              get
               28  LOAD_FAST                'scheme'
               30  LOAD_CONST               80
               32  CALL_METHOD_2         2  ''
             34_0  COME_FROM            22  '22'
               34  STORE_FAST               'port'

 L. 114        36  LOAD_FAST                'scheme'
               38  LOAD_FAST                'host'
               40  LOAD_FAST                'port'
               42  BUILD_TUPLE_3         3 
               44  STORE_FAST               'pool_key'

 L. 116        46  LOAD_FAST                'self'
               48  LOAD_ATTR                pools
               50  LOAD_ATTR                lock
               52  SETUP_WITH          116  'to 116'
               54  POP_TOP          

 L. 119        56  LOAD_FAST                'self'
               58  LOAD_ATTR                pools
               60  LOAD_METHOD              get
               62  LOAD_FAST                'pool_key'
               64  CALL_METHOD_1         1  ''
               66  STORE_FAST               'pool'

 L. 120        68  LOAD_FAST                'pool'
               70  POP_JUMP_IF_FALSE    88  'to 88'

 L. 121        72  LOAD_FAST                'pool'
               74  POP_BLOCK        
               76  ROT_TWO          
               78  BEGIN_FINALLY    
               80  WITH_CLEANUP_START
               82  WITH_CLEANUP_FINISH
               84  POP_FINALLY           0  ''
               86  RETURN_VALUE     
             88_0  COME_FROM            70  '70'

 L. 124        88  LOAD_FAST                'self'
               90  LOAD_METHOD              _new_pool
               92  LOAD_FAST                'scheme'
               94  LOAD_FAST                'host'
               96  LOAD_FAST                'port'
               98  CALL_METHOD_3         3  ''
              100  STORE_FAST               'pool'

 L. 125       102  LOAD_FAST                'pool'
              104  LOAD_FAST                'self'
              106  LOAD_ATTR                pools
              108  LOAD_FAST                'pool_key'
              110  STORE_SUBSCR     
              112  POP_BLOCK        
              114  BEGIN_FINALLY    
            116_0  COME_FROM_WITH       52  '52'
              116  WITH_CLEANUP_START
              118  WITH_CLEANUP_FINISH
              120  END_FINALLY      

 L. 127       122  LOAD_FAST                'pool'
              124  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ROT_TWO' instruction at offset 76

        def connection_from_url(self, url):
            """
        Similar to :func:`urllib3.connectionpool.connection_from_url` but
        doesn't pass any additional parameters to the
        :class:`urllib3.connectionpool.ConnectionPool` constructor.

        Additional parameters are taken from the :class:`.PoolManager`
        constructor.
        """
            u = parse_url(url)
            return self.connection_from_host((u.host), port=(u.port), scheme=(u.scheme))

        def urlopen(self, method, url, redirect=True, **kw):
            """
        Same as :meth:`urllib3.connectionpool.HTTPConnectionPool.urlopen`
        with custom cross-host redirect logic and only sends the request-uri
        portion of the ``url``.

        The given ``url`` parameter must be absolute, such that an appropriate
        :class:`urllib3.connectionpool.ConnectionPool` can be chosen for it.
        """
            u = parse_url(url)
            conn = self.connection_from_host((u.host), port=(u.port), scheme=(u.scheme))
            kw['assert_same_host'] = False
            kw['redirect'] = False
            if 'headers' not in kw:
                kw['headers'] = self.headers
            else:
                if self.proxy is not None and u.scheme == 'http':
                    response = (conn.urlopen)(method, url, **kw)
                else:
                    response = (conn.urlopen)(method, (u.request_uri), **kw)
                redirect_location = redirect and response.get_redirect_location()
                return redirect_location or response
            redirect_location = urljoin(url, redirect_location)
            if response.status == 303:
                method = 'GET'
            retries = kw.get('retries')
            if not isinstance(retries, Retry):
                retries = Retry.from_int(retries, redirect=redirect)
            try:
                retries = retries.increment(method, url, response=response, _pool=conn)
            except MaxRetryError:
                if retries.raise_on_redirect:
                    raise
                return response
            else:
                kw['retries'] = retries
                kw['redirect'] = redirect
                log.info('Redirecting %s -> %s' % (url, redirect_location))
                return (self.urlopen)(method, redirect_location, **kw)


    class ProxyManager(PoolManager):
        __doc__ = "\n    Behaves just like :class:`PoolManager`, but sends all requests through\n    the defined proxy, using the CONNECT method for HTTPS URLs.\n\n    :param proxy_url:\n        The URL of the proxy to be used.\n\n    :param proxy_headers:\n        A dictionary contaning headers that will be sent to the proxy. In case\n        of HTTP they are being sent with each request, while in the\n        HTTPS/CONNECT case they are sent only once. Could be used for proxy\n        authentication.\n\n    Example:\n        >>> proxy = urllib3.ProxyManager('http://localhost:3128/')\n        >>> r1 = proxy.request('GET', 'http://google.com/')\n        >>> r2 = proxy.request('GET', 'http://httpbin.org/')\n        >>> len(proxy.pools)\n        1\n        >>> r3 = proxy.request('GET', 'https://httpbin.org/')\n        >>> r4 = proxy.request('GET', 'https://twitter.com/')\n        >>> len(proxy.pools)\n        3\n\n    "

        def __init__(self, proxy_url, num_pools=10, headers=None, proxy_headers=None, **connection_pool_kw):
            if isinstance(proxy_url, HTTPConnectionPool):
                proxy_url = '%s://%s:%i' % (proxy_url.scheme, proxy_url.host,
                 proxy_url.port)
            proxy = parse_url(proxy_url)
            if not proxy.port:
                port = port_by_scheme.get(proxy.scheme, 80)
                proxy = proxy._replace(port=port)
            assert proxy.scheme in ('http', 'https'), 'Not supported proxy scheme %s' % proxy.scheme
            self.proxy = proxy
            self.proxy_headers = proxy_headers or {}
            connection_pool_kw['_proxy'] = self.proxy
            connection_pool_kw['_proxy_headers'] = self.proxy_headers
            (super(ProxyManager, self).__init__)(
             num_pools, headers, **connection_pool_kw)

        def connection_from_host(self, host, port=None, scheme='http'):
            if scheme == 'https':
                return super(ProxyManager, self).connection_from_hosthostportscheme
            return super(ProxyManager, self).connection_from_hostself.proxy.hostself.proxy.portself.proxy.scheme

        def _set_proxy_headers(self, url, headers=None):
            """
        Sets headers needed by proxies: specifically, the Accept and Host
        headers. Only sets headers not provided by the user.
        """
            headers_ = {'Accept': '*/*'}
            netloc = parse_url(url).netloc
            if netloc:
                headers_['Host'] = netloc
            if headers:
                headers_.update(headers)
            return headers_

        def urlopen(self, method, url, redirect=True, **kw):
            """Same as HTTP(S)ConnectionPool.urlopen, ``url`` must be absolute."""
            u = parse_url(url)
            if u.scheme == 'http':
                headers = kw.get('headers', self.headers)
                kw['headers'] = self._set_proxy_headers(url, headers)
            return (super(ProxyManager, self).urlopen)(method, url, redirect=redirect, **kw)


    def proxy_from_url(url, **kw):
        return ProxyManager(proxy_url=url, **kw)