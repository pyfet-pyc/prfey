# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\requests\packages\urllib3\packages\ssl_match_hostname\_implementation.py
"""The match_hostname() function from Python 3.3.3, essential when using SSL."""
import re
__version__ = '3.4.0.2'

class CertificateError(ValueError):
    pass


def _dnsname_match(dn, hostname, max_wildcards=1):
    """Matching according to RFC 6125, section 6.4.3

    http://tools.ietf.org/html/rfc6125#section-6.4.3
    """
    pats = []
    if not dn:
        return False
    parts = dn.split('.')
    leftmost = parts[0]
    remainder = parts[1:]
    wildcards = leftmost.count('*')
    if wildcards > max_wildcards:
        raise CertificateError('too many wildcards in certificate DNS name: ' + repr(dn))
    elif not wildcards:
        return dn.lower() == hostname.lower()
        if leftmost == '*':
            pats.append('[^.]+')
    elif leftmost.startswith('xn--') or hostname.startswith('xn--'):
        pats.append(re.escape(leftmost))
    else:
        pats.append(re.escape(leftmost).replace('\\*', '[^.]*'))
    for frag in remainder:
        pats.append(re.escape(frag))
    else:
        pat = re.compile('\\A' + '\\.'.join(pats) + '\\Z', re.IGNORECASE)
        return pat.match(hostname)


def match_hostname--- This code section failed: ---

 L.  75         0  LOAD_FAST                'cert'
                2  POP_JUMP_IF_TRUE     12  'to 12'

 L.  76         4  LOAD_GLOBAL              ValueError
                6  LOAD_STR                 'empty or no certificate'
                8  CALL_FUNCTION_1       1  ''
               10  RAISE_VARARGS_1       1  'exception instance'
             12_0  COME_FROM             2  '2'

 L.  77        12  BUILD_LIST_0          0 
               14  STORE_FAST               'dnsnames'

 L.  78        16  LOAD_FAST                'cert'
               18  LOAD_METHOD              get
               20  LOAD_STR                 'subjectAltName'
               22  LOAD_CONST               ()
               24  CALL_METHOD_2         2  ''
               26  STORE_FAST               'san'

 L.  79        28  LOAD_FAST                'san'
               30  GET_ITER         
             32_0  COME_FROM            46  '46'
               32  FOR_ITER             76  'to 76'
               34  UNPACK_SEQUENCE_2     2 
               36  STORE_FAST               'key'
               38  STORE_FAST               'value'

 L.  80        40  LOAD_FAST                'key'
               42  LOAD_STR                 'DNS'
               44  COMPARE_OP               ==
               46  POP_JUMP_IF_FALSE    32  'to 32'

 L.  81        48  LOAD_GLOBAL              _dnsname_match
               50  LOAD_FAST                'value'
               52  LOAD_FAST                'hostname'
               54  CALL_FUNCTION_2       2  ''
               56  POP_JUMP_IF_FALSE    64  'to 64'

 L.  82        58  POP_TOP          
               60  LOAD_CONST               None
               62  RETURN_VALUE     
             64_0  COME_FROM            56  '56'

 L.  83        64  LOAD_FAST                'dnsnames'
               66  LOAD_METHOD              append
               68  LOAD_FAST                'value'
               70  CALL_METHOD_1         1  ''
               72  POP_TOP          
               74  JUMP_BACK            32  'to 32'

 L.  84        76  LOAD_FAST                'dnsnames'
               78  POP_JUMP_IF_TRUE    148  'to 148'

 L.  87        80  LOAD_FAST                'cert'
               82  LOAD_METHOD              get
               84  LOAD_STR                 'subject'
               86  LOAD_CONST               ()
               88  CALL_METHOD_2         2  ''
               90  GET_ITER         
               92  FOR_ITER            148  'to 148'
               94  STORE_FAST               'sub'

 L.  88        96  LOAD_FAST                'sub'
               98  GET_ITER         
            100_0  COME_FROM           114  '114'
              100  FOR_ITER            146  'to 146'
              102  UNPACK_SEQUENCE_2     2 
              104  STORE_FAST               'key'
              106  STORE_FAST               'value'

 L.  91       108  LOAD_FAST                'key'
              110  LOAD_STR                 'commonName'
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   100  'to 100'

 L.  92       116  LOAD_GLOBAL              _dnsname_match
              118  LOAD_FAST                'value'
              120  LOAD_FAST                'hostname'
              122  CALL_FUNCTION_2       2  ''
              124  POP_JUMP_IF_FALSE   134  'to 134'

 L.  93       126  POP_TOP          
              128  POP_TOP          
              130  LOAD_CONST               None
              132  RETURN_VALUE     
            134_0  COME_FROM           124  '124'

 L.  94       134  LOAD_FAST                'dnsnames'
              136  LOAD_METHOD              append
              138  LOAD_FAST                'value'
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          
              144  JUMP_BACK           100  'to 100'
              146  JUMP_BACK            92  'to 92'
            148_0  COME_FROM            78  '78'

 L.  95       148  LOAD_GLOBAL              len
              150  LOAD_FAST                'dnsnames'
              152  CALL_FUNCTION_1       1  ''
              154  LOAD_CONST               1
              156  COMPARE_OP               >
              158  POP_JUMP_IF_FALSE   190  'to 190'

 L.  96       160  LOAD_GLOBAL              CertificateError
              162  LOAD_STR                 "hostname %r doesn't match either of %s"

 L.  98       164  LOAD_FAST                'hostname'
              166  LOAD_STR                 ', '
              168  LOAD_METHOD              join
              170  LOAD_GLOBAL              map
              172  LOAD_GLOBAL              repr
              174  LOAD_FAST                'dnsnames'
              176  CALL_FUNCTION_2       2  ''
              178  CALL_METHOD_1         1  ''
              180  BUILD_TUPLE_2         2 

 L.  96       182  BINARY_MODULO    
              184  CALL_FUNCTION_1       1  ''
              186  RAISE_VARARGS_1       1  'exception instance'
              188  JUMP_FORWARD        232  'to 232'
            190_0  COME_FROM           158  '158'

 L.  99       190  LOAD_GLOBAL              len
              192  LOAD_FAST                'dnsnames'
              194  CALL_FUNCTION_1       1  ''
              196  LOAD_CONST               1
              198  COMPARE_OP               ==
              200  POP_JUMP_IF_FALSE   224  'to 224'

 L. 100       202  LOAD_GLOBAL              CertificateError
              204  LOAD_STR                 "hostname %r doesn't match %r"

 L. 102       206  LOAD_FAST                'hostname'
              208  LOAD_FAST                'dnsnames'
              210  LOAD_CONST               0
              212  BINARY_SUBSCR    
              214  BUILD_TUPLE_2         2 

 L. 100       216  BINARY_MODULO    
              218  CALL_FUNCTION_1       1  ''
              220  RAISE_VARARGS_1       1  'exception instance'
              222  JUMP_FORWARD        232  'to 232'
            224_0  COME_FROM           200  '200'

 L. 104       224  LOAD_GLOBAL              CertificateError
              226  LOAD_STR                 'no appropriate commonName or subjectAltName fields were found'
              228  CALL_FUNCTION_1       1  ''
              230  RAISE_VARARGS_1       1  'exception instance'
            232_0  COME_FROM           222  '222'
            232_1  COME_FROM           188  '188'

Parse error at or near `JUMP_BACK' instruction at offset 146