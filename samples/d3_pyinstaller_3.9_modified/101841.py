# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: urllib3\util\proxy.py
from .ssl_ import create_urllib3_context, resolve_cert_reqs, resolve_ssl_version

def connection_requires_http_tunnel--- This code section failed: ---

 L.  18         0  LOAD_FAST                'proxy_url'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L.  19         8  LOAD_CONST               False
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L.  22        12  LOAD_FAST                'destination_scheme'
               14  LOAD_STR                 'http'
               16  COMPARE_OP               ==
               18  POP_JUMP_IF_FALSE    24  'to 24'

 L.  23        20  LOAD_CONST               False
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L.  27        24  LOAD_FAST                'proxy_url'
               26  LOAD_ATTR                scheme
               28  LOAD_STR                 'https'
               30  COMPARE_OP               ==

 L.  26        32  POP_JUMP_IF_FALSE    48  'to 48'

 L.  28        34  LOAD_FAST                'proxy_config'

 L.  26        36  POP_JUMP_IF_FALSE    48  'to 48'

 L.  29        38  LOAD_FAST                'proxy_config'
               40  LOAD_ATTR                use_forwarding_for_https

 L.  26        42  POP_JUMP_IF_FALSE    48  'to 48'

 L.  31        44  LOAD_CONST               False
               46  RETURN_VALUE     
             48_0  COME_FROM            42  '42'
             48_1  COME_FROM            36  '36'
             48_2  COME_FROM            32  '32'

 L.  34        48  LOAD_CONST               True
               50  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def create_proxy_ssl_context(ssl_version, cert_reqs, ca_certs=None, ca_cert_dir=None, ca_cert_data=None):
    """
    Generates a default proxy ssl context if one hasn't been provided by the
    user.
    """
    ssl_context = create_urllib3_context(ssl_version=(resolve_ssl_version(ssl_version)),
      cert_reqs=(resolve_cert_reqs(cert_reqs)))
    if not ca_certs:
        if not ca_cert_dir:
            if not ca_cert_data:
                if hasattr(ssl_context, 'load_default_certs'):
                    ssl_context.load_default_certs()
        return ssl_context