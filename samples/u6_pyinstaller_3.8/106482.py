# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\urllib3\packages\ssl_match_hostname\_implementation.py
"""The match_hostname() function from Python 3.3.3, essential when using SSL."""
import re, sys
try:
    import ipaddress
except ImportError:
    ipaddress = None
else:
    __version__ = '3.5.0.1'

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


    def _to_unicode(obj):
        if isinstance(obj, str):
            if sys.version_info < (3, ):
                obj = unicode(obj, encoding='ascii', errors='strict')
        return obj


    def _ipaddress_match(ipname, host_ip):
        """Exact matching of IP addresses.

    RFC 6125 explicitly doesn't define an algorithm for this
    (section 1.7.2 - "Out of Scope").
    """
        ip = ipaddress.ip_address(_to_unicode(ipname).rstrip())
        return ip == host_ip


    def match_hostname--- This code section failed: ---

 L. 105         0  LOAD_FAST                'cert'
                2  POP_JUMP_IF_TRUE     12  'to 12'

 L. 106         4  LOAD_GLOBAL              ValueError

 L. 107         6  LOAD_STR                 'empty or no certificate, match_hostname needs a SSL socket or SSL context with either CERT_OPTIONAL or CERT_REQUIRED'

 L. 106         8  CALL_FUNCTION_1       1  ''
               10  RAISE_VARARGS_1       1  'exception instance'
             12_0  COME_FROM             2  '2'

 L. 111        12  SETUP_FINALLY        32  'to 32'

 L. 113        14  LOAD_GLOBAL              ipaddress
               16  LOAD_METHOD              ip_address
               18  LOAD_GLOBAL              _to_unicode
               20  LOAD_FAST                'hostname'
               22  CALL_FUNCTION_1       1  ''
               24  CALL_METHOD_1         1  ''
               26  STORE_FAST               'host_ip'
               28  POP_BLOCK        
               30  JUMP_FORWARD        112  'to 112'
             32_0  COME_FROM_FINALLY    12  '12'

 L. 114        32  DUP_TOP          
               34  LOAD_GLOBAL              ValueError
               36  COMPARE_OP               exception-match
               38  POP_JUMP_IF_FALSE    54  'to 54'
               40  POP_TOP          
               42  POP_TOP          
               44  POP_TOP          

 L. 116        46  LOAD_CONST               None
               48  STORE_FAST               'host_ip'
               50  POP_EXCEPT       
               52  JUMP_FORWARD        112  'to 112'
             54_0  COME_FROM            38  '38'

 L. 117        54  DUP_TOP          
               56  LOAD_GLOBAL              UnicodeError
               58  COMPARE_OP               exception-match
               60  POP_JUMP_IF_FALSE    76  'to 76'
               62  POP_TOP          
               64  POP_TOP          
               66  POP_TOP          

 L. 121        68  LOAD_CONST               None
               70  STORE_FAST               'host_ip'
               72  POP_EXCEPT       
               74  JUMP_FORWARD        112  'to 112'
             76_0  COME_FROM            60  '60'

 L. 122        76  DUP_TOP          
               78  LOAD_GLOBAL              AttributeError
               80  COMPARE_OP               exception-match
               82  POP_JUMP_IF_FALSE   110  'to 110'
               84  POP_TOP          
               86  POP_TOP          
               88  POP_TOP          

 L. 124        90  LOAD_GLOBAL              ipaddress
               92  LOAD_CONST               None
               94  COMPARE_OP               is
               96  POP_JUMP_IF_FALSE   104  'to 104'

 L. 125        98  LOAD_CONST               None
              100  STORE_FAST               'host_ip'
              102  JUMP_FORWARD        106  'to 106'
            104_0  COME_FROM            96  '96'

 L. 127       104  RAISE_VARARGS_0       0  'reraise'
            106_0  COME_FROM           102  '102'
              106  POP_EXCEPT       
              108  JUMP_FORWARD        112  'to 112'
            110_0  COME_FROM            82  '82'
              110  END_FINALLY      
            112_0  COME_FROM           108  '108'
            112_1  COME_FROM            74  '74'
            112_2  COME_FROM            52  '52'
            112_3  COME_FROM            30  '30'

 L. 128       112  BUILD_LIST_0          0 
              114  STORE_FAST               'dnsnames'

 L. 129       116  LOAD_FAST                'cert'
              118  LOAD_METHOD              get
              120  LOAD_STR                 'subjectAltName'
              122  LOAD_CONST               ()
              124  CALL_METHOD_2         2  ''
              126  STORE_FAST               'san'

 L. 130       128  LOAD_FAST                'san'
              130  GET_ITER         
            132_0  COME_FROM           190  '190'
              132  FOR_ITER            228  'to 228'
              134  UNPACK_SEQUENCE_2     2 
              136  STORE_FAST               'key'
              138  STORE_FAST               'value'

 L. 131       140  LOAD_FAST                'key'
              142  LOAD_STR                 'DNS'
              144  COMPARE_OP               ==
              146  POP_JUMP_IF_FALSE   184  'to 184'

 L. 132       148  LOAD_FAST                'host_ip'
              150  LOAD_CONST               None
              152  COMPARE_OP               is
              154  POP_JUMP_IF_FALSE   172  'to 172'
              156  LOAD_GLOBAL              _dnsname_match
              158  LOAD_FAST                'value'
              160  LOAD_FAST                'hostname'
              162  CALL_FUNCTION_2       2  ''
              164  POP_JUMP_IF_FALSE   172  'to 172'

 L. 133       166  POP_TOP          
              168  LOAD_CONST               None
              170  RETURN_VALUE     
            172_0  COME_FROM           164  '164'
            172_1  COME_FROM           154  '154'

 L. 134       172  LOAD_FAST                'dnsnames'
              174  LOAD_METHOD              append
              176  LOAD_FAST                'value'
              178  CALL_METHOD_1         1  ''
              180  POP_TOP          
              182  JUMP_BACK           132  'to 132'
            184_0  COME_FROM           146  '146'

 L. 135       184  LOAD_FAST                'key'
              186  LOAD_STR                 'IP Address'
              188  COMPARE_OP               ==
              190  POP_JUMP_IF_FALSE   132  'to 132'

 L. 136       192  LOAD_FAST                'host_ip'
              194  LOAD_CONST               None
              196  COMPARE_OP               is-not
              198  POP_JUMP_IF_FALSE   216  'to 216'
              200  LOAD_GLOBAL              _ipaddress_match
              202  LOAD_FAST                'value'
              204  LOAD_FAST                'host_ip'
              206  CALL_FUNCTION_2       2  ''
              208  POP_JUMP_IF_FALSE   216  'to 216'

 L. 137       210  POP_TOP          
              212  LOAD_CONST               None
              214  RETURN_VALUE     
            216_0  COME_FROM           208  '208'
            216_1  COME_FROM           198  '198'

 L. 138       216  LOAD_FAST                'dnsnames'
              218  LOAD_METHOD              append
              220  LOAD_FAST                'value'
              222  CALL_METHOD_1         1  ''
              224  POP_TOP          
              226  JUMP_BACK           132  'to 132'

 L. 139       228  LOAD_FAST                'dnsnames'
          230_232  POP_JUMP_IF_TRUE    304  'to 304'

 L. 142       234  LOAD_FAST                'cert'
              236  LOAD_METHOD              get
              238  LOAD_STR                 'subject'
              240  LOAD_CONST               ()
              242  CALL_METHOD_2         2  ''
              244  GET_ITER         
              246  FOR_ITER            304  'to 304'
              248  STORE_FAST               'sub'

 L. 143       250  LOAD_FAST                'sub'
              252  GET_ITER         
            254_0  COME_FROM           268  '268'
              254  FOR_ITER            302  'to 302'
              256  UNPACK_SEQUENCE_2     2 
              258  STORE_FAST               'key'
              260  STORE_FAST               'value'

 L. 146       262  LOAD_FAST                'key'
              264  LOAD_STR                 'commonName'
              266  COMPARE_OP               ==
              268  POP_JUMP_IF_FALSE   254  'to 254'

 L. 147       270  LOAD_GLOBAL              _dnsname_match
              272  LOAD_FAST                'value'
              274  LOAD_FAST                'hostname'
              276  CALL_FUNCTION_2       2  ''
          278_280  POP_JUMP_IF_FALSE   290  'to 290'

 L. 148       282  POP_TOP          
              284  POP_TOP          
              286  LOAD_CONST               None
              288  RETURN_VALUE     
            290_0  COME_FROM           278  '278'

 L. 149       290  LOAD_FAST                'dnsnames'
              292  LOAD_METHOD              append
              294  LOAD_FAST                'value'
              296  CALL_METHOD_1         1  ''
              298  POP_TOP          
              300  JUMP_BACK           254  'to 254'
              302  JUMP_BACK           246  'to 246'
            304_0  COME_FROM           230  '230'

 L. 150       304  LOAD_GLOBAL              len
              306  LOAD_FAST                'dnsnames'
              308  CALL_FUNCTION_1       1  ''
              310  LOAD_CONST               1
              312  COMPARE_OP               >
          314_316  POP_JUMP_IF_FALSE   348  'to 348'

 L. 151       318  LOAD_GLOBAL              CertificateError

 L. 152       320  LOAD_STR                 "hostname %r doesn't match either of %s"

 L. 153       322  LOAD_FAST                'hostname'
              324  LOAD_STR                 ', '
              326  LOAD_METHOD              join
              328  LOAD_GLOBAL              map
              330  LOAD_GLOBAL              repr
              332  LOAD_FAST                'dnsnames'
              334  CALL_FUNCTION_2       2  ''
              336  CALL_METHOD_1         1  ''
              338  BUILD_TUPLE_2         2 

 L. 152       340  BINARY_MODULO    

 L. 151       342  CALL_FUNCTION_1       1  ''
              344  RAISE_VARARGS_1       1  'exception instance'
              346  JUMP_FORWARD        392  'to 392'
            348_0  COME_FROM           314  '314'

 L. 155       348  LOAD_GLOBAL              len
              350  LOAD_FAST                'dnsnames'
              352  CALL_FUNCTION_1       1  ''
              354  LOAD_CONST               1
              356  COMPARE_OP               ==
          358_360  POP_JUMP_IF_FALSE   384  'to 384'

 L. 156       362  LOAD_GLOBAL              CertificateError
              364  LOAD_STR                 "hostname %r doesn't match %r"
              366  LOAD_FAST                'hostname'
              368  LOAD_FAST                'dnsnames'
              370  LOAD_CONST               0
              372  BINARY_SUBSCR    
              374  BUILD_TUPLE_2         2 
              376  BINARY_MODULO    
              378  CALL_FUNCTION_1       1  ''
              380  RAISE_VARARGS_1       1  'exception instance'
              382  JUMP_FORWARD        392  'to 392'
            384_0  COME_FROM           358  '358'

 L. 158       384  LOAD_GLOBAL              CertificateError

 L. 159       386  LOAD_STR                 'no appropriate commonName or subjectAltName fields were found'

 L. 158       388  CALL_FUNCTION_1       1  ''
              390  RAISE_VARARGS_1       1  'exception instance'
            392_0  COME_FROM           382  '382'
            392_1  COME_FROM           346  '346'

Parse error at or near `JUMP_BACK' instruction at offset 302