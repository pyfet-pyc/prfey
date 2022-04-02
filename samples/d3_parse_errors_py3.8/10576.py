# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: urllib3\poolmanager.py
from __future__ import absolute_import
import collections, functools, logging, warnings
from ._collections import RecentlyUsedContainer
from .connectionpool import HTTPConnectionPool, HTTPSConnectionPool
from .connectionpool import port_by_scheme
from .exceptions import LocationValueError, MaxRetryError, ProxySchemeUnknown, InvalidProxyConfigurationWarning
from .packages import six
from packages.six.moves.urllib.parse import urljoin
from .request import RequestMethods
from util.url import parse_url
from util.retry import Retry
__all__ = [
 'PoolManager', 'ProxyManager', 'proxy_from_url']
log = logging.getLogger(__name__)
SSL_KEYWORDS = ('key_file', 'cert_file', 'cert_reqs', 'ca_certs', 'ssl_version', 'ca_cert_dir',
                'ssl_context', 'key_password')
_key_fields = ('key_scheme', 'key_host', 'key_port', 'key_timeout', 'key_retries',
               'key_strict', 'key_block', 'key_source_address', 'key_key_file', 'key_key_password',
               'key_cert_file', 'key_cert_reqs', 'key_ca_certs', 'key_ssl_version',
               'key_ca_cert_dir', 'key_ssl_context', 'key_maxsize', 'key_headers',
               'key__proxy', 'key__proxy_headers', 'key_socket_options', 'key__socks_options',
               'key_assert_hostname', 'key_assert_fingerprint', 'key_server_hostname')
PoolKey = collections.namedtuple('PoolKey', _key_fields)

def _default_key_normalizer(key_class, request_context):
    """
    Create a pool key out of a request context dictionary.

    According to RFC 3986, both the scheme and host are case-insensitive.
    Therefore, this function normalizes both before constructing the pool
    key for an HTTPS request. If you wish to change this behaviour, provide
    alternate callables to ``key_fn_by_scheme``.

    :param key_class:
        The class to use when constructing the key. This should be a namedtuple
        with the ``scheme`` and ``host`` keys at a minimum.
    :type  key_class: namedtuple
    :param request_context:
        A dictionary-like object that contain the context for a request.
    :type  request_context: dict

    :return: A namedtuple that can be used as a connection pool key.
    :rtype:  PoolKey
    """
    context = request_context.copy()
    context['scheme'] = context['scheme'].lower()
    context['host'] = context['host'].lower()
    for key in ('headers', '_proxy_headers', '_socks_options'):
        if key in context:
            if context[key] is not None:
                context[key] = frozenset(context[key].items())
    else:
        socket_opts = context.get('socket_options')
        if socket_opts is not None:
            context['socket_options'] = tuple(socket_opts)

    for key in list(context.keys()):
        context['key_' + key] = context.pop(key)
    else:
        for field in key_class._fields:
            if field not in context:
                context[field] = None
        else:
            return key_class(**context)


key_fn_by_scheme = {'http':functools.partial(_default_key_normalizer, PoolKey), 
 'https':functools.partial(_default_key_normalizer, PoolKey)}
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

    def _new_pool(self, scheme, host, port, request_context=None):
        """
        Create a new :class:`ConnectionPool` based on host, port, scheme, and
        any additional pool keyword arguments.

        If ``request_context`` is provided, it is provided as keyword arguments
        to the pool class used. This method is used to actually create the
        connection pools handed out by :meth:`connection_from_url` and
        companion methods. It is intended to be overridden for customization.
        """
        pool_cls = self.pool_classes_by_scheme[scheme]
        if request_context is None:
            request_context = self.connection_pool_kw.copy()
        for key in ('scheme', 'host', 'port'):
            request_context.pop(key, None)
        else:
            if scheme == 'http':
                for kw in SSL_KEYWORDS:
                    request_context.pop(kw, None)

                return pool_cls(host, port, **request_context)

    def clear(self):
        """
        Empty our store of pools and direct them all to close.

        This will not affect in-flight connections, but they will not be
        re-used after completion.
        """
        self.pools.clear()

    def connection_from_host(self, host, port=None, scheme='http', pool_kwargs=None):
        """
        Get a :class:`ConnectionPool` based on the host, port, and scheme.

        If ``port`` isn't given, it will be derived from the ``scheme`` using
        ``urllib3.connectionpool.port_by_scheme``. If ``pool_kwargs`` is
        provided, it is merged with the instance's ``connection_pool_kw``
        variable and used to create the new connection pool, if one is
        needed.
        """
        if not host:
            raise LocationValueError('No host specified.')
        request_context = self._merge_pool_kwargs(pool_kwargs)
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
        return self.connection_from_pool_key(pool_key, request_context=request_context)

    def connection_from_pool_key(self, pool_key, request_context=None):
        """
        Get a :class:`ConnectionPool` based on the provided pool key.

        ``pool_key`` should be a namedtuple that only contains immutable
        objects. At a minimum it must have the ``scheme``, ``host``, and
        ``port`` fields.
        """
        with self.pools.lock:
            pool = self.pools.get(pool_key)
            if pool:
                return pool
            scheme = request_context['scheme']
            host = request_context['host']
            port = request_context['port']
            pool = self._new_pool(scheme, host, port, request_context=request_context)
            self.pools[pool_key] = pool
        return pool

    def connection_from_url(self, url, pool_kwargs=None):
        """
        Similar to :func:`urllib3.connectionpool.connection_from_url`.

        If ``pool_kwargs`` is not provided and a new pool needs to be
        constructed, ``self.connection_pool_kw`` is used to initialize
        the :class:`urllib3.connectionpool.ConnectionPool`. If ``pool_kwargs``
        is provided, it is used instead. Note that if a new pool does not
        need to be created for the request, the provided ``pool_kwargs`` are
        not used.
        """
        u = parse_url(url)
        return self.connection_from_host((u.host),
          port=(u.port), scheme=(u.scheme), pool_kwargs=pool_kwargs)

    def _merge_pool_kwargs--- This code section failed: ---

 L. 303         0  LOAD_FAST                'self'
                2  LOAD_ATTR                connection_pool_kw
                4  LOAD_METHOD              copy
                6  CALL_METHOD_0         0  ''
                8  STORE_FAST               'base_pool_kwargs'

 L. 304        10  LOAD_FAST                'override'
               12  POP_JUMP_IF_FALSE    82  'to 82'

 L. 305        14  LOAD_FAST                'override'
               16  LOAD_METHOD              items
               18  CALL_METHOD_0         0  ''
               20  GET_ITER         
             22_0  COME_FROM            80  '80'
             22_1  COME_FROM            70  '70'
               22  FOR_ITER             82  'to 82'
               24  UNPACK_SEQUENCE_2     2 
               26  STORE_FAST               'key'
               28  STORE_FAST               'value'

 L. 306        30  LOAD_FAST                'value'
               32  LOAD_CONST               None
               34  COMPARE_OP               is
               36  POP_JUMP_IF_FALSE    72  'to 72'

 L. 307        38  SETUP_FINALLY        50  'to 50'

 L. 308        40  LOAD_FAST                'base_pool_kwargs'
               42  LOAD_FAST                'key'
               44  DELETE_SUBSCR    
               46  POP_BLOCK        
               48  JUMP_FORWARD         80  'to 80'
             50_0  COME_FROM_FINALLY    38  '38'

 L. 309        50  DUP_TOP          
               52  LOAD_GLOBAL              KeyError
               54  COMPARE_OP               exception-match
               56  POP_JUMP_IF_FALSE    68  'to 68'
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          

 L. 310        64  POP_EXCEPT       
               66  BREAK_LOOP           80  'to 80'
             68_0  COME_FROM            56  '56'
               68  END_FINALLY      
               70  JUMP_BACK            22  'to 22'
             72_0  COME_FROM            36  '36'

 L. 312        72  LOAD_FAST                'value'
               74  LOAD_FAST                'base_pool_kwargs'
               76  LOAD_FAST                'key'
               78  STORE_SUBSCR     
             80_0  COME_FROM            66  '66'
             80_1  COME_FROM            48  '48'
               80  JUMP_BACK            22  'to 22'
             82_0  COME_FROM            22  '22'
             82_1  COME_FROM            12  '12'

 L. 313        82  LOAD_FAST                'base_pool_kwargs'
               84  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `END_FINALLY' instruction at offset 68

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
            kw['headers'] = self.headers.copy()
        if self.proxy is not None and u.scheme == 'http':
            response = (conn.urlopen)(method, url, **kw)
        else:
            response = (conn.urlopen)(method, (u.request_uri), **kw)
        redirect_location = redirect and response.get_redirect_location()
        if not redirect_location:
            return response
        redirect_location = urljoin(url, redirect_location)
        if response.status == 303:
            method = 'GET'
        retries = kw.get('retries')
        if not isinstance(retries, Retry):
            retries = Retry.from_int(retries, redirect=redirect)
        if retries.remove_headers_on_redirect:
            if not conn.is_same_host(redirect_location):
                headers = list(six.iterkeys(kw['headers']))
                for header in headers:
                    if header.lower() in retries.remove_headers_on_redirect:
                        kw['headers'].pop(header, None)

        try:
            retries = retries.increment(method, url, response=response, _pool=conn)
        except MaxRetryError:
            if retries.raise_on_redirect:
                response.drain_conn()
                raise
            return response
        else:
            kw['retries'] = retries
            kw['redirect'] = redirect
            log.info('Redirecting %s -> %s', url, redirect_location)
            response.drain_conn()
            return (self.urlopen)(method, redirect_location, **kw)


class ProxyManager(PoolManager):
    __doc__ = "\n    Behaves just like :class:`PoolManager`, but sends all requests through\n    the defined proxy, using the CONNECT method for HTTPS URLs.\n\n    :param proxy_url:\n        The URL of the proxy to be used.\n\n    :param proxy_headers:\n        A dictionary containing headers that will be sent to the proxy. In case\n        of HTTP they are being sent with each request, while in the\n        HTTPS/CONNECT case they are sent only once. Could be used for proxy\n        authentication.\n\n    Example:\n        >>> proxy = urllib3.ProxyManager('http://localhost:3128/')\n        >>> r1 = proxy.request('GET', 'http://google.com/')\n        >>> r2 = proxy.request('GET', 'http://httpbin.org/')\n        >>> len(proxy.pools)\n        1\n        >>> r3 = proxy.request('GET', 'https://httpbin.org/')\n        >>> r4 = proxy.request('GET', 'https://twitter.com/')\n        >>> len(proxy.pools)\n        3\n\n    "

    def __init__(self, proxy_url, num_pools=10, headers=None, proxy_headers=None, **connection_pool_kw):
        if isinstance(proxy_url, HTTPConnectionPool):
            proxy_url = '%s://%s:%i' % (
             proxy_url.scheme,
             proxy_url.host,
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
        (super(ProxyManager, self).__init__)(num_pools, headers, **connection_pool_kw)

    def connection_from_host(self, host, port=None, scheme='http', pool_kwargs=None):
        if scheme == 'https':
            return super(ProxyManager, self).connection_from_host(host,
              port, scheme, pool_kwargs=pool_kwargs)
        return super(ProxyManager, self).connection_from_host((self.proxy.host),
          (self.proxy.port), (self.proxy.scheme), pool_kwargs=pool_kwargs)

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

    def _validate_proxy_scheme_url_selection(self, url_scheme):
        if url_scheme == 'https':
            if self.proxy.scheme == 'https':
                warnings.warn('Your proxy configuration specified an HTTPS scheme for the proxy. Are you sure you want to use HTTPS to contact the proxy? This most likely indicates an error in your configuration. Read this issue for more info: https://github.com/urllib3/urllib3/issues/1850',
                  InvalidProxyConfigurationWarning,
                  stacklevel=3)

    def urlopen(self, method, url, redirect=True, **kw):
        """Same as HTTP(S)ConnectionPool.urlopen, ``url`` must be absolute."""
        u = parse_url(url)
        self._validate_proxy_scheme_url_selection(u.scheme)
        if u.scheme == 'http':
            headers = kw.get('headers', self.headers)
            kw['headers'] = self._set_proxy_headers(url, headers)
        return (super(ProxyManager, self).urlopen)(method, url, redirect=redirect, **kw)


def proxy_from_url(url, **kw):
    return ProxyManager(proxy_url=url, **kw)