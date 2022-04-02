# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: requests\packages\urllib3\poolmanager.py
from __future__ import absolute_import
import collections, functools, logging
from ._collections import RecentlyUsedContainer
from .connectionpool import HTTPConnectionPool, HTTPSConnectionPool
from .connectionpool import port_by_scheme
from .exceptions import LocationValueError, MaxRetryError, ProxySchemeUnknown
from packages.six.moves.urllib.parse import urljoin
from .request import RequestMethods
from util.url import parse_url
from util.retry import Retry
__all__ = [
 'PoolManager', 'ProxyManager', 'proxy_from_url']
log = logging.getLogger(__name__)
SSL_KEYWORDS = ('key_file', 'cert_file', 'cert_reqs', 'ca_certs', 'ssl_version', 'ca_cert_dir',
                'ssl_context')
BasePoolKey = collections.namedtuple('BasePoolKey', ('scheme', 'host', 'port'))
HTTPPoolKey = collections.namedtuple('HTTPPoolKey', BasePoolKey._fields + ('timeout',
                                                                           'retries',
                                                                           'strict',
                                                                           'block',
                                                                           'source_address'))
HTTPSPoolKey = collections.namedtuple('HTTPSPoolKey', HTTPPoolKey._fields + SSL_KEYWORDS)

def _default_key_normalizer(key_class, request_context):
    """
    Create a pool key of type ``key_class`` for a request.

    According to RFC 3986, both the scheme and host are case-insensitive.
    Therefore, this function normalizes both before constructing the pool
    key for an HTTPS request. If you wish to change this behaviour, provide
    alternate callables to ``key_fn_by_scheme``.

    :param key_class:
        The class to use when constructing the key. This should be a namedtuple
        with the ``scheme`` and ``host`` keys at a minimum.

    :param request_context:
        A dictionary-like object that contain the context for a request.
        It should contain a key for each field in the :class:`HTTPPoolKey`
    """
    context = {}
    for key in key_class._fields:
        context[key] = request_context.get(key)
    else:
        context['scheme'] = context['scheme'].lower()
        context['host'] = context['host'].lower()
        return key_class(**context)


key_fn_by_scheme = {'http':functools.partial(_default_key_normalizer, HTTPPoolKey), 
 'https':functools.partial(_default_key_normalizer, HTTPSPoolKey)}
pool_classes_by_scheme = {'http':HTTPConnectionPool, 
 'https':HTTPSConnectionPool}

class PoolManager(RequestMethods):
    __doc__ = "\n    Allows for arbitrary requests while transparently keeping track of\n    necessary connection pools for you.\n\n    :param num_pools:\n        Number of connection pools to cache before discarding the least\n        recently used pool.\n\n    :param headers:\n        Headers to include with all requests, unless other headers are given\n        explicitly.\n\n    :param \\**connection_pool_kw:\n        Additional parameters are used to create fresh\n        :class:`urllib3.connectionpool.ConnectionPool` instances.\n\n    Example::\n\n        >>> manager = PoolManager(num_pools=2)\n        >>> r = manager.request('GET', 'http://google.com/')\n        >>> r = manager.request('GET', 'http://google.com/mail')\n        >>> r = manager.request('GET', 'http://yahoo.com/')\n        >>> len(manager.pools)\n        2\n\n    "
    proxy = None

    def __init__(self, num_pools=10, headers=None, **connection_pool_kw):
        RequestMethods.__init__(self, headers)
        self.connection_pool_kw = connection_pool_kw
        self.pools = RecentlyUsedContainer(num_pools, dispose_func=(lambda p: p.close()))
        self.pool_classes_by_scheme = pool_classes_by_scheme
        self.key_fn_by_scheme = key_fn_by_scheme.copy()

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
        pool_cls = self.pool_classes_by_scheme[scheme]
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

    def connection_from_host(self, host, port=None, scheme='http'):
        """
        Get a :class:`ConnectionPool` based on the host, port, and scheme.

        If ``port`` isn't given, it will be derived from the ``scheme`` using
        ``urllib3.connectionpool.port_by_scheme``.
        """
        if not host:
            raise LocationValueError('No host specified.')
        request_context = self.connection_pool_kw.copy()
        request_context['scheme'] = scheme or 'http'
        if not port:
            port = port_by_scheme.get(request_context['scheme'].lower(), 80)
        request_context['port'] = port
        request_context['host'] = host
        return self.connection_from_context(request_context)

    def connection_from_context(self, request_context):
        """
        Get a :class:`ConnectionPool` based on the request context.

        ``request_context`` must at least contain the ``scheme`` key and its
        value must be a key in ``key_fn_by_scheme`` instance variable.
        """
        scheme = request_context['scheme'].lower()
        pool_key_constructor = self.key_fn_by_scheme[scheme]
        pool_key = pool_key_constructor(request_context)
        return self.connection_from_pool_key(pool_key)

    def connection_from_pool_key--- This code section failed: ---

 L. 199         0  LOAD_FAST                'self'
                2  LOAD_ATTR                pools
                4  LOAD_ATTR                lock
                6  SETUP_WITH           76  'to 76'
                8  POP_TOP          

 L. 202        10  LOAD_FAST                'self'
               12  LOAD_ATTR                pools
               14  LOAD_METHOD              get
               16  LOAD_FAST                'pool_key'
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'pool'

 L. 203        22  LOAD_FAST                'pool'
               24  POP_JUMP_IF_FALSE    42  'to 42'

 L. 204        26  LOAD_FAST                'pool'
               28  POP_BLOCK        
               30  ROT_TWO          
               32  BEGIN_FINALLY    
               34  WITH_CLEANUP_START
               36  WITH_CLEANUP_FINISH
               38  POP_FINALLY           0  ''
               40  RETURN_VALUE     
             42_0  COME_FROM            24  '24'

 L. 207        42  LOAD_FAST                'self'
               44  LOAD_METHOD              _new_pool
               46  LOAD_FAST                'pool_key'
               48  LOAD_ATTR                scheme
               50  LOAD_FAST                'pool_key'
               52  LOAD_ATTR                host
               54  LOAD_FAST                'pool_key'
               56  LOAD_ATTR                port
               58  CALL_METHOD_3         3  ''
               60  STORE_FAST               'pool'

 L. 208        62  LOAD_FAST                'pool'
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                pools
               68  LOAD_FAST                'pool_key'
               70  STORE_SUBSCR     
               72  POP_BLOCK        
               74  BEGIN_FINALLY    
             76_0  COME_FROM_WITH        6  '6'
               76  WITH_CLEANUP_START
               78  WITH_CLEANUP_FINISH
               80  END_FINALLY      

 L. 210        82  LOAD_FAST                'pool'
               84  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `ROT_TWO' instruction at offset 30

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
            log.info'Redirecting %s -> %s'urlredirect_location
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
        if proxy.scheme not in ('http', 'https'):
            raise ProxySchemeUnknown(proxy.scheme)
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