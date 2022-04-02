# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\pymongo\ssl_match_hostname.py
import re, sys
try:
    from ipaddress import ip_address
except ImportError:
    ip_address = lambda address: None
else:
    if sys.version_info[0] < 3:
        _unicode = unicode
    else:
        _unicode = lambda value: value

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


    def _ipaddress_match(ipname, host_ip):
        """Exact matching of IP addresses.

    RFC 6125 explicitly doesn't define an algorithm for this
    (section 1.7.2 - "Out of Scope").
    """
        ip = ip_address(_unicode(ipname).rstrip())
        return ip == host_ip


    def match_hostname--- This code section failed: ---

 L.  94         0  LOAD_FAST                'cert'
                2  POP_JUMP_IF_TRUE     12  'to 12'

 L.  95         4  LOAD_GLOBAL              ValueError
                6  LOAD_STR                 'empty or no certificate, match_hostname needs a SSL socket or SSL context with either CERT_OPTIONAL or CERT_REQUIRED'
                8  CALL_FUNCTION_1       1  ''
               10  RAISE_VARARGS_1       1  'exception instance'
             12_0  COME_FROM             2  '2'

 L.  98        12  SETUP_FINALLY        30  'to 30'

 L.  99        14  LOAD_GLOBAL              ip_address
               16  LOAD_GLOBAL              _unicode
               18  LOAD_FAST                'hostname'
               20  CALL_FUNCTION_1       1  ''
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'host_ip'
               26  POP_BLOCK        
               28  JUMP_FORWARD         58  'to 58'
             30_0  COME_FROM_FINALLY    12  '12'

 L. 100        30  DUP_TOP          
               32  LOAD_GLOBAL              ValueError
               34  LOAD_GLOBAL              UnicodeError
               36  BUILD_TUPLE_2         2 
               38  COMPARE_OP               exception-match
               40  POP_JUMP_IF_FALSE    56  'to 56'
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L. 102        48  LOAD_CONST               None
               50  STORE_FAST               'host_ip'
               52  POP_EXCEPT       
               54  JUMP_FORWARD         58  'to 58'
             56_0  COME_FROM            40  '40'
               56  END_FINALLY      
             58_0  COME_FROM            54  '54'
             58_1  COME_FROM            28  '28'

 L. 103        58  BUILD_LIST_0          0 
               60  STORE_FAST               'dnsnames'

 L. 104        62  LOAD_FAST                'cert'
               64  LOAD_METHOD              get
               66  LOAD_STR                 'subjectAltName'
               68  LOAD_CONST               ()
               70  CALL_METHOD_2         2  ''
               72  STORE_FAST               'san'

 L. 105        74  LOAD_FAST                'san'
               76  GET_ITER         
             78_0  COME_FROM           136  '136'
               78  FOR_ITER            174  'to 174'
               80  UNPACK_SEQUENCE_2     2 
               82  STORE_FAST               'key'
               84  STORE_FAST               'value'

 L. 106        86  LOAD_FAST                'key'
               88  LOAD_STR                 'DNS'
               90  COMPARE_OP               ==
               92  POP_JUMP_IF_FALSE   130  'to 130'

 L. 107        94  LOAD_FAST                'host_ip'
               96  LOAD_CONST               None
               98  COMPARE_OP               is
              100  POP_JUMP_IF_FALSE   118  'to 118'
              102  LOAD_GLOBAL              _dnsname_match
              104  LOAD_FAST                'value'
              106  LOAD_FAST                'hostname'
              108  CALL_FUNCTION_2       2  ''
              110  POP_JUMP_IF_FALSE   118  'to 118'

 L. 108       112  POP_TOP          
              114  LOAD_CONST               None
              116  RETURN_VALUE     
            118_0  COME_FROM           110  '110'
            118_1  COME_FROM           100  '100'

 L. 109       118  LOAD_FAST                'dnsnames'
              120  LOAD_METHOD              append
              122  LOAD_FAST                'value'
              124  CALL_METHOD_1         1  ''
              126  POP_TOP          
              128  JUMP_BACK            78  'to 78'
            130_0  COME_FROM            92  '92'

 L. 110       130  LOAD_FAST                'key'
              132  LOAD_STR                 'IP Address'
              134  COMPARE_OP               ==
              136  POP_JUMP_IF_FALSE    78  'to 78'

 L. 111       138  LOAD_FAST                'host_ip'
              140  LOAD_CONST               None
              142  COMPARE_OP               is-not
              144  POP_JUMP_IF_FALSE   162  'to 162'
              146  LOAD_GLOBAL              _ipaddress_match
              148  LOAD_FAST                'value'
              150  LOAD_FAST                'host_ip'
              152  CALL_FUNCTION_2       2  ''
              154  POP_JUMP_IF_FALSE   162  'to 162'

 L. 112       156  POP_TOP          
              158  LOAD_CONST               None
              160  RETURN_VALUE     
            162_0  COME_FROM           154  '154'
            162_1  COME_FROM           144  '144'

 L. 113       162  LOAD_FAST                'dnsnames'
              164  LOAD_METHOD              append
              166  LOAD_FAST                'value'
              168  CALL_METHOD_1         1  ''
              170  POP_TOP          
              172  JUMP_BACK            78  'to 78'

 L. 114       174  LOAD_FAST                'dnsnames'
              176  POP_JUMP_IF_TRUE    246  'to 246'

 L. 117       178  LOAD_FAST                'cert'
              180  LOAD_METHOD              get
              182  LOAD_STR                 'subject'
              184  LOAD_CONST               ()
              186  CALL_METHOD_2         2  ''
              188  GET_ITER         
              190  FOR_ITER            246  'to 246'
              192  STORE_FAST               'sub'

 L. 118       194  LOAD_FAST                'sub'
              196  GET_ITER         
            198_0  COME_FROM           212  '212'
              198  FOR_ITER            244  'to 244'
              200  UNPACK_SEQUENCE_2     2 
              202  STORE_FAST               'key'
              204  STORE_FAST               'value'

 L. 121       206  LOAD_FAST                'key'
              208  LOAD_STR                 'commonName'
              210  COMPARE_OP               ==
              212  POP_JUMP_IF_FALSE   198  'to 198'

 L. 122       214  LOAD_GLOBAL              _dnsname_match
              216  LOAD_FAST                'value'
              218  LOAD_FAST                'hostname'
              220  CALL_FUNCTION_2       2  ''
              222  POP_JUMP_IF_FALSE   232  'to 232'

 L. 123       224  POP_TOP          
              226  POP_TOP          
              228  LOAD_CONST               None
              230  RETURN_VALUE     
            232_0  COME_FROM           222  '222'

 L. 124       232  LOAD_FAST                'dnsnames'
              234  LOAD_METHOD              append
              236  LOAD_FAST                'value'
              238  CALL_METHOD_1         1  ''
              240  POP_TOP          
              242  JUMP_BACK           198  'to 198'
              244  JUMP_BACK           190  'to 190'
            246_0  COME_FROM           176  '176'

 L. 125       246  LOAD_GLOBAL              len
              248  LOAD_FAST                'dnsnames'
              250  CALL_FUNCTION_1       1  ''
              252  LOAD_CONST               1
              254  COMPARE_OP               >
          256_258  POP_JUMP_IF_FALSE   290  'to 290'

 L. 126       260  LOAD_GLOBAL              CertificateError
              262  LOAD_STR                 "hostname %r doesn't match either of %s"

 L. 128       264  LOAD_FAST                'hostname'
              266  LOAD_STR                 ', '
              268  LOAD_METHOD              join
              270  LOAD_GLOBAL              map
              272  LOAD_GLOBAL              repr
              274  LOAD_FAST                'dnsnames'
              276  CALL_FUNCTION_2       2  ''
              278  CALL_METHOD_1         1  ''
              280  BUILD_TUPLE_2         2 

 L. 126       282  BINARY_MODULO    
              284  CALL_FUNCTION_1       1  ''
              286  RAISE_VARARGS_1       1  'exception instance'
              288  JUMP_FORWARD        334  'to 334'
            290_0  COME_FROM           256  '256'

 L. 129       290  LOAD_GLOBAL              len
              292  LOAD_FAST                'dnsnames'
              294  CALL_FUNCTION_1       1  ''
              296  LOAD_CONST               1
              298  COMPARE_OP               ==
          300_302  POP_JUMP_IF_FALSE   326  'to 326'

 L. 130       304  LOAD_GLOBAL              CertificateError
              306  LOAD_STR                 "hostname %r doesn't match %r"

 L. 132       308  LOAD_FAST                'hostname'
              310  LOAD_FAST                'dnsnames'
              312  LOAD_CONST               0
              314  BINARY_SUBSCR    
              316  BUILD_TUPLE_2         2 

 L. 130       318  BINARY_MODULO    
              320  CALL_FUNCTION_1       1  ''
              322  RAISE_VARARGS_1       1  'exception instance'
              324  JUMP_FORWARD        334  'to 334'
            326_0  COME_FROM           300  '300'

 L. 134       326  LOAD_GLOBAL              CertificateError
              328  LOAD_STR                 'no appropriate commonName or subjectAltName fields were found'
              330  CALL_FUNCTION_1       1  ''
              332  RAISE_VARARGS_1       1  'exception instance'
            334_0  COME_FROM           324  '324'
            334_1  COME_FROM           288  '288'

Parse error at or near `JUMP_BACK' instruction at offset 244