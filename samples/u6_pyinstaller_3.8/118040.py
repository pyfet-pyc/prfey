# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\dns\resolver.py
"""DNS stub resolver."""
import socket, sys, time, random
try:
    import threading as _threading
except ImportError:
    import dummy_threading as _threading
else:
    import dns.exception, dns.flags, dns.ipv4, dns.ipv6, dns.message, dns.name, dns.query, dns.rcode, dns.rdataclass, dns.rdatatype, dns.reversename, dns.tsig
    from ._compat import xrange, string_types
    if sys.platform == 'win32':
        try:
            import winreg as _winreg
        except ImportError:
            import _winreg

    class NXDOMAIN(dns.exception.DNSException):
        __doc__ = 'The DNS query name does not exist.'
        supp_kwargs = {'qnames', 'responses'}
        fmt = None

        def _check_kwargs(self, qnames, responses=None):
            if not isinstance(qnames, (list, tuple, set)):
                raise AttributeError('qnames must be a list, tuple or set')
            elif len(qnames) == 0:
                raise AttributeError('qnames must contain at least one element')
            elif responses is None:
                responses = {}
            else:
                assert isinstance(responses, dict), 'responses must be a dict(qname=response)'
            kwargs = dict(qnames=qnames, responses=responses)
            return kwargs

        def __str__(self):
            if 'qnames' not in self.kwargs:
                return super(NXDOMAIN, self).__str__()
            else:
                qnames = self.kwargs['qnames']
                if len(qnames) > 1:
                    msg = 'None of DNS query names exist'
                else:
                    msg = 'The DNS query name does not exist'
            qnames = ', '.join(map(str, qnames))
            return '{}: {}'.format(msg, qnames)

        def canonical_name(self):
            if 'qnames' not in self.kwargs:
                raise TypeError('parametrized exception required')
            IN = dns.rdataclass.IN
            CNAME = dns.rdatatype.CNAME
            cname = None
            for qname in self.kwargs['qnames']:
                response = self.kwargs['responses'][qname]

            for answer in response.answer:
                if not answer.rdtype != CNAME:
                    if answer.rdclass != IN:
                        pass
                    else:
                        cname = answer.items[0].target.to_text()
                if cname is not None:
                    return dns.name.from_text(cname)
                return self.kwargs['qnames'][0]

        canonical_name = property(canonical_name, doc='Return the unresolved canonical name.')

        def __add__(self, e_nx):
            """Augment by results from another NXDOMAIN exception."""
            qnames0 = list(self.kwargs.get('qnames', []))
            responses0 = dict(self.kwargs.get('responses', {}))
            responses1 = e_nx.kwargs.get('responses', {})
            for qname1 in e_nx.kwargs.get('qnames', []):
                if qname1 not in qnames0:
                    qnames0.append(qname1)
                if qname1 in responses1:
                    responses0[qname1] = responses1[qname1]
                return NXDOMAIN(qnames=qnames0, responses=responses0)

        def qnames(self):
            """All of the names that were tried.

        Returns a list of ``dns.name.Name``.
        """
            return self.kwargs['qnames']

        def responses(self):
            """A map from queried names to their NXDOMAIN responses.

        Returns a dict mapping a ``dns.name.Name`` to a
        ``dns.message.Message``.
        """
            return self.kwargs['responses']

        def response(self, qname):
            """The response for query *qname*.

        Returns a ``dns.message.Message``.
        """
            return self.kwargs['responses'][qname]


    class YXDOMAIN(dns.exception.DNSException):
        __doc__ = 'The DNS query name is too long after DNAME substitution.'


    Timeout = dns.exception.Timeout

    class NoAnswer(dns.exception.DNSException):
        __doc__ = 'The DNS response does not contain an answer to the question.'
        fmt = 'The DNS response does not contain an answer to the question: {query}'
        supp_kwargs = {
         'response'}

        def _fmt_kwargs(self, **kwargs):
            return super(NoAnswer, self)._fmt_kwargs(query=(kwargs['response'].question))


    class NoNameservers(dns.exception.DNSException):
        __doc__ = 'All nameservers failed to answer the query.\n\n    errors: list of servers and respective errors\n    The type of errors is\n    [(server IP address, any object convertible to string)].\n    Non-empty errors list will add explanatory message ()\n    '
        msg = 'All nameservers failed to answer the query.'
        fmt = '%s {query}: {errors}' % msg[:-1]
        supp_kwargs = {'request', 'errors'}

        def _fmt_kwargs(self, **kwargs):
            srv_msgs = []
            for err in kwargs['errors']:
                srv_msgs.append('Server {} {} port {} answered {}'.format(err[0], 'TCP' if err[1] else 'UDP', err[2], err[3]))
            else:
                return super(NoNameservers, self)._fmt_kwargs(query=(kwargs['request'].question),
                  errors=('; '.join(srv_msgs)))


    class NotAbsolute(dns.exception.DNSException):
        __doc__ = 'An absolute domain name is required but a relative name was provided.'


    class NoRootSOA(dns.exception.DNSException):
        __doc__ = 'There is no SOA RR at the DNS root name. This should never happen!'


    class NoMetaqueries(dns.exception.DNSException):
        __doc__ = 'DNS metaqueries are not allowed.'


    class Answer(object):
        __doc__ = "DNS stub resolver answer.\n\n    Instances of this class bundle up the result of a successful DNS\n    resolution.\n\n    For convenience, the answer object implements much of the sequence\n    protocol, forwarding to its ``rrset`` attribute.  E.g.\n    ``for a in answer`` is equivalent to ``for a in answer.rrset``.\n    ``answer[i]`` is equivalent to ``answer.rrset[i]``, and\n    ``answer[i:j]`` is equivalent to ``answer.rrset[i:j]``.\n\n    Note that CNAMEs or DNAMEs in the response may mean that answer\n    RRset's name might not be the query name.\n    "

        def __init__--- This code section failed: ---

 L. 204         0  LOAD_FAST                'qname'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               qname

 L. 205         6  LOAD_FAST                'rdtype'
                8  LOAD_FAST                'self'
               10  STORE_ATTR               rdtype

 L. 206        12  LOAD_FAST                'rdclass'
               14  LOAD_FAST                'self'
               16  STORE_ATTR               rdclass

 L. 207        18  LOAD_FAST                'response'
               20  LOAD_FAST                'self'
               22  STORE_ATTR               response

 L. 208        24  LOAD_CONST               -1
               26  STORE_FAST               'min_ttl'

 L. 209        28  LOAD_CONST               None
               30  STORE_FAST               'rrset'

 L. 210        32  LOAD_GLOBAL              xrange
               34  LOAD_CONST               0
               36  LOAD_CONST               15
               38  CALL_FUNCTION_2       2  ''
               40  GET_ITER         
               42  FOR_ITER            266  'to 266'
               44  STORE_FAST               'count'

 L. 211        46  SETUP_FINALLY       102  'to 102'

 L. 212        48  LOAD_FAST                'response'
               50  LOAD_METHOD              find_rrset
               52  LOAD_FAST                'response'
               54  LOAD_ATTR                answer
               56  LOAD_FAST                'qname'

 L. 213        58  LOAD_FAST                'rdclass'

 L. 213        60  LOAD_FAST                'rdtype'

 L. 212        62  CALL_METHOD_4         4  ''
               64  STORE_FAST               'rrset'

 L. 214        66  LOAD_FAST                'min_ttl'
               68  LOAD_CONST               -1
               70  COMPARE_OP               ==
               72  POP_JUMP_IF_TRUE     84  'to 84'
               74  LOAD_FAST                'rrset'
               76  LOAD_ATTR                ttl
               78  LOAD_FAST                'min_ttl'
               80  COMPARE_OP               <
               82  POP_JUMP_IF_FALSE    90  'to 90'
             84_0  COME_FROM            72  '72'

 L. 215        84  LOAD_FAST                'rrset'
               86  LOAD_ATTR                ttl
               88  STORE_FAST               'min_ttl'
             90_0  COME_FROM            82  '82'

 L. 216        90  POP_BLOCK        
               92  POP_TOP          
            94_96  BREAK_LOOP          266  'to 266'
               98  POP_BLOCK        
              100  JUMP_BACK            42  'to 42'
            102_0  COME_FROM_FINALLY    46  '46'

 L. 217       102  DUP_TOP          
              104  LOAD_GLOBAL              KeyError
              106  COMPARE_OP               exception-match
          108_110  POP_JUMP_IF_FALSE   262  'to 262'
              112  POP_TOP          
              114  POP_TOP          
              116  POP_TOP          

 L. 218       118  LOAD_FAST                'rdtype'
              120  LOAD_GLOBAL              dns
              122  LOAD_ATTR                rdatatype
              124  LOAD_ATTR                CNAME
              126  COMPARE_OP               !=
              128  POP_JUMP_IF_FALSE   242  'to 242'

 L. 219       130  SETUP_FINALLY       208  'to 208'

 L. 220       132  LOAD_FAST                'response'
              134  LOAD_METHOD              find_rrset
              136  LOAD_FAST                'response'
              138  LOAD_ATTR                answer

 L. 221       140  LOAD_FAST                'qname'

 L. 222       142  LOAD_FAST                'rdclass'

 L. 223       144  LOAD_GLOBAL              dns
              146  LOAD_ATTR                rdatatype
              148  LOAD_ATTR                CNAME

 L. 220       150  CALL_METHOD_4         4  ''
              152  STORE_FAST               'crrset'

 L. 224       154  LOAD_FAST                'min_ttl'
              156  LOAD_CONST               -1
              158  COMPARE_OP               ==
              160  POP_JUMP_IF_TRUE    172  'to 172'
              162  LOAD_FAST                'crrset'
              164  LOAD_ATTR                ttl
              166  LOAD_FAST                'min_ttl'
              168  COMPARE_OP               <
              170  POP_JUMP_IF_FALSE   178  'to 178'
            172_0  COME_FROM           160  '160'

 L. 225       172  LOAD_FAST                'crrset'
              174  LOAD_ATTR                ttl
              176  STORE_FAST               'min_ttl'
            178_0  COME_FROM           170  '170'

 L. 226       178  LOAD_FAST                'crrset'
              180  GET_ITER         
              182  FOR_ITER            198  'to 198'
              184  STORE_FAST               'rd'

 L. 227       186  LOAD_FAST                'rd'
              188  LOAD_ATTR                target
              190  STORE_FAST               'qname'

 L. 228       192  POP_TOP          
              194  BREAK_LOOP          198  'to 198'
              196  JUMP_BACK           182  'to 182'

 L. 229       198  POP_BLOCK        
              200  POP_EXCEPT       
              202  JUMP_BACK            42  'to 42'
              204  POP_BLOCK        
              206  JUMP_FORWARD        242  'to 242'
            208_0  COME_FROM_FINALLY   130  '130'

 L. 230       208  DUP_TOP          
              210  LOAD_GLOBAL              KeyError
              212  COMPARE_OP               exception-match
              214  POP_JUMP_IF_FALSE   240  'to 240'
              216  POP_TOP          
              218  POP_TOP          
              220  POP_TOP          

 L. 231       222  LOAD_FAST                'raise_on_no_answer'
              224  POP_JUMP_IF_FALSE   236  'to 236'

 L. 232       226  LOAD_GLOBAL              NoAnswer
              228  LOAD_FAST                'response'
              230  LOAD_CONST               ('response',)
              232  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              234  RAISE_VARARGS_1       1  'exception instance'
            236_0  COME_FROM           224  '224'
              236  POP_EXCEPT       
              238  JUMP_FORWARD        242  'to 242'
            240_0  COME_FROM           214  '214'
              240  END_FINALLY      
            242_0  COME_FROM           238  '238'
            242_1  COME_FROM           206  '206'
            242_2  COME_FROM           128  '128'

 L. 233       242  LOAD_FAST                'raise_on_no_answer'
          244_246  POP_JUMP_IF_FALSE   258  'to 258'

 L. 234       248  LOAD_GLOBAL              NoAnswer
              250  LOAD_FAST                'response'
              252  LOAD_CONST               ('response',)
              254  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              256  RAISE_VARARGS_1       1  'exception instance'
            258_0  COME_FROM           244  '244'
              258  POP_EXCEPT       
              260  JUMP_BACK            42  'to 42'
            262_0  COME_FROM           108  '108'
              262  END_FINALLY      
              264  JUMP_BACK            42  'to 42'

 L. 235       266  LOAD_FAST                'rrset'
              268  LOAD_CONST               None
              270  COMPARE_OP               is
          272_274  POP_JUMP_IF_FALSE   292  'to 292'
              276  LOAD_FAST                'raise_on_no_answer'
          278_280  POP_JUMP_IF_FALSE   292  'to 292'

 L. 236       282  LOAD_GLOBAL              NoAnswer
              284  LOAD_FAST                'response'
              286  LOAD_CONST               ('response',)
              288  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              290  RAISE_VARARGS_1       1  'exception instance'
            292_0  COME_FROM           278  '278'
            292_1  COME_FROM           272  '272'

 L. 237       292  LOAD_FAST                'qname'
              294  LOAD_FAST                'self'
              296  STORE_ATTR               canonical_name

 L. 238       298  LOAD_FAST                'rrset'
              300  LOAD_FAST                'self'
              302  STORE_ATTR               rrset

 L. 239       304  LOAD_FAST                'rrset'
              306  LOAD_CONST               None
              308  COMPARE_OP               is
          310_312  POP_JUMP_IF_FALSE   476  'to 476'

 L. 243       314  SETUP_FINALLY       402  'to 402'

 L. 244       316  LOAD_FAST                'response'
              318  LOAD_METHOD              find_rrset
              320  LOAD_FAST                'response'
              322  LOAD_ATTR                authority
              324  LOAD_FAST                'qname'

 L. 245       326  LOAD_FAST                'rdclass'

 L. 245       328  LOAD_GLOBAL              dns
              330  LOAD_ATTR                rdatatype
              332  LOAD_ATTR                SOA

 L. 244       334  CALL_METHOD_4         4  ''
              336  STORE_FAST               'srrset'

 L. 246       338  LOAD_FAST                'min_ttl'
              340  LOAD_CONST               -1
              342  COMPARE_OP               ==
          344_346  POP_JUMP_IF_TRUE    360  'to 360'
              348  LOAD_FAST                'srrset'
              350  LOAD_ATTR                ttl
              352  LOAD_FAST                'min_ttl'
              354  COMPARE_OP               <
          356_358  POP_JUMP_IF_FALSE   366  'to 366'
            360_0  COME_FROM           344  '344'

 L. 247       360  LOAD_FAST                'srrset'
              362  LOAD_ATTR                ttl
              364  STORE_FAST               'min_ttl'
            366_0  COME_FROM           356  '356'

 L. 248       366  LOAD_FAST                'srrset'
              368  LOAD_CONST               0
              370  BINARY_SUBSCR    
              372  LOAD_ATTR                minimum
              374  LOAD_FAST                'min_ttl'
              376  COMPARE_OP               <
          378_380  POP_JUMP_IF_FALSE   392  'to 392'

 L. 249       382  LOAD_FAST                'srrset'
              384  LOAD_CONST               0
              386  BINARY_SUBSCR    
              388  LOAD_ATTR                minimum
              390  STORE_FAST               'min_ttl'
            392_0  COME_FROM           378  '378'

 L. 250       392  POP_BLOCK        
          394_396  JUMP_ABSOLUTE       476  'to 476'
              398  POP_BLOCK        
              400  JUMP_BACK           314  'to 314'
            402_0  COME_FROM_FINALLY   314  '314'

 L. 251       402  DUP_TOP          
              404  LOAD_GLOBAL              KeyError
              406  COMPARE_OP               exception-match
          408_410  POP_JUMP_IF_FALSE   470  'to 470'
              412  POP_TOP          
              414  POP_TOP          
              416  POP_TOP          

 L. 252       418  SETUP_FINALLY       432  'to 432'

 L. 253       420  LOAD_FAST                'qname'
              422  LOAD_METHOD              parent
              424  CALL_METHOD_0         0  ''
              426  STORE_FAST               'qname'
              428  POP_BLOCK        
              430  JUMP_FORWARD        466  'to 466'
            432_0  COME_FROM_FINALLY   418  '418'

 L. 254       432  DUP_TOP          
              434  LOAD_GLOBAL              dns
              436  LOAD_ATTR                name
              438  LOAD_ATTR                NoParent
              440  COMPARE_OP               exception-match
          442_444  POP_JUMP_IF_FALSE   464  'to 464'
              446  POP_TOP          
              448  POP_TOP          
              450  POP_TOP          

 L. 255       452  POP_EXCEPT       
              454  POP_EXCEPT       
          456_458  JUMP_ABSOLUTE       476  'to 476'
              460  POP_EXCEPT       
              462  JUMP_FORWARD        466  'to 466'
            464_0  COME_FROM           442  '442'
              464  END_FINALLY      
            466_0  COME_FROM           462  '462'
            466_1  COME_FROM           430  '430'
              466  POP_EXCEPT       
              468  JUMP_BACK           314  'to 314'
            470_0  COME_FROM           408  '408'
              470  END_FINALLY      
          472_474  JUMP_BACK           314  'to 314'
            476_0  COME_FROM           310  '310'

 L. 256       476  LOAD_GLOBAL              time
              478  LOAD_METHOD              time
              480  CALL_METHOD_0         0  ''
              482  LOAD_FAST                'min_ttl'
              484  BINARY_ADD       
              486  LOAD_FAST                'self'
              488  STORE_ATTR               expiration

Parse error at or near `JUMP_BACK' instruction at offset 202

        def __getattr__(self, attr):
            if attr == 'name':
                return self.rrset.name
            if attr == 'ttl':
                return self.rrset.ttl
            if attr == 'covers':
                return self.rrset.covers
            if attr == 'rdclass':
                return self.rrset.rdclass
            if attr == 'rdtype':
                return self.rrset.rdtype
            raise AttributeError(attr)

        def __len__(self):
            return self.rrset and len(self.rrset) or 0

        def __iter__(self):
            return self.rrset and iter(self.rrset) or iter(tuple())

        def __getitem__(self, i):
            if self.rrset is None:
                raise IndexError
            return self.rrset[i]

        def __delitem__(self, i):
            if self.rrset is None:
                raise IndexError
            del self.rrset[i]


    class Cache(object):
        __doc__ = 'Simple thread-safe DNS answer cache.'

        def __init__(self, cleaning_interval=300.0):
            """*cleaning_interval*, a ``float`` is the number of seconds between
        periodic cleanings.
        """
            self.data = {}
            self.cleaning_interval = cleaning_interval
            self.next_cleaning = time.time() + self.cleaning_interval
            self.lock = _threading.Lock()

        def _maybe_clean(self):
            """Clean the cache if it's time to do so."""
            now = time.time()
            if self.next_cleaning <= now:
                keys_to_delete = []
                for k, v in self.data.items():
                    if v.expiration <= now:
                        keys_to_delete.append(k)
                    for k in keys_to_delete:
                        del self.data[k]
                    else:
                        now = time.time()
                        self.next_cleaning = now + self.cleaning_interval

        def get--- This code section failed: ---

 L. 327         0  SETUP_FINALLY        70  'to 70'

 L. 328         2  LOAD_FAST                'self'
                4  LOAD_ATTR                lock
                6  LOAD_METHOD              acquire
                8  CALL_METHOD_0         0  ''
               10  POP_TOP          

 L. 329        12  LOAD_FAST                'self'
               14  LOAD_METHOD              _maybe_clean
               16  CALL_METHOD_0         0  ''
               18  POP_TOP          

 L. 330        20  LOAD_FAST                'self'
               22  LOAD_ATTR                data
               24  LOAD_METHOD              get
               26  LOAD_FAST                'key'
               28  CALL_METHOD_1         1  ''
               30  STORE_FAST               'v'

 L. 331        32  LOAD_FAST                'v'
               34  LOAD_CONST               None
               36  COMPARE_OP               is
               38  POP_JUMP_IF_TRUE     54  'to 54'
               40  LOAD_FAST                'v'
               42  LOAD_ATTR                expiration
               44  LOAD_GLOBAL              time
               46  LOAD_METHOD              time
               48  CALL_METHOD_0         0  ''
               50  COMPARE_OP               <=
               52  POP_JUMP_IF_FALSE    62  'to 62'
             54_0  COME_FROM            38  '38'

 L. 332        54  POP_BLOCK        
               56  CALL_FINALLY         70  'to 70'
               58  LOAD_CONST               None
               60  RETURN_VALUE     
             62_0  COME_FROM            52  '52'

 L. 333        62  LOAD_FAST                'v'
               64  POP_BLOCK        
               66  CALL_FINALLY         70  'to 70'
               68  RETURN_VALUE     
             70_0  COME_FROM            66  '66'
             70_1  COME_FROM            56  '56'
             70_2  COME_FROM_FINALLY     0  '0'

 L. 335        70  LOAD_FAST                'self'
               72  LOAD_ATTR                lock
               74  LOAD_METHOD              release
               76  CALL_METHOD_0         0  ''
               78  POP_TOP          
               80  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 56

        def put(self, key, value):
            """Associate key and value in the cache.

        *key*, a ``(dns.name.Name, int, int)`` tuple whose values are the
        query name, rdtype, and rdclass respectively.

        *value*, a ``dns.resolver.Answer``, the answer.
        """
            try:
                self.lock.acquire()
                self._maybe_clean()
                self.data[key] = value
            finally:
                self.lock.release()

        def flush(self, key=None):
            """Flush the cache.

        If *key* is not ``None``, only that item is flushed.  Otherwise
        the entire cache is flushed.

        *key*, a ``(dns.name.Name, int, int)`` tuple whose values are the
        query name, rdtype, and rdclass respectively.
        """
            try:
                self.lock.acquire()
                if key is not None:
                    if key in self.data:
                        del self.data[key]
                else:
                    self.data = {}
                    self.next_cleaning = time.time() + self.cleaning_interval
            finally:
                self.lock.release()


    class LRUCacheNode(object):
        __doc__ = 'LRUCache node.'

        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.prev = self
            self.next = self

        def link_before(self, node):
            self.prev = node.prev
            self.next = node
            node.prev.next = self
            node.prev = self

        def link_after(self, node):
            self.prev = node
            self.next = node.next
            node.next.prev = self
            node.next = self

        def unlink(self):
            self.next.prev = self.prev
            self.prev.next = self.next


    class LRUCache(object):
        __doc__ = "Thread-safe, bounded, least-recently-used DNS answer cache.\n\n    This cache is better than the simple cache (above) if you're\n    running a web crawler or other process that does a lot of\n    resolutions.  The LRUCache has a maximum number of nodes, and when\n    it is full, the least-recently used node is removed to make space\n    for a new one.\n    "

        def __init__(self, max_size=100000):
            """*max_size*, an ``int``, is the maximum number of nodes to cache;
        it must be greater than 0.
        """
            self.data = {}
            self.set_max_size(max_size)
            self.sentinel = LRUCacheNode(None, None)
            self.lock = _threading.Lock()

        def set_max_size(self, max_size):
            if max_size < 1:
                max_size = 1
            self.max_size = max_size

        def get--- This code section failed: ---

 L. 437         0  SETUP_FINALLY       104  'to 104'

 L. 438         2  LOAD_FAST                'self'
                4  LOAD_ATTR                lock
                6  LOAD_METHOD              acquire
                8  CALL_METHOD_0         0  ''
               10  POP_TOP          

 L. 439        12  LOAD_FAST                'self'
               14  LOAD_ATTR                data
               16  LOAD_METHOD              get
               18  LOAD_FAST                'key'
               20  CALL_METHOD_1         1  ''
               22  STORE_FAST               'node'

 L. 440        24  LOAD_FAST                'node'
               26  LOAD_CONST               None
               28  COMPARE_OP               is
               30  POP_JUMP_IF_FALSE    40  'to 40'

 L. 441        32  POP_BLOCK        
               34  CALL_FINALLY        104  'to 104'
               36  LOAD_CONST               None
               38  RETURN_VALUE     
             40_0  COME_FROM            30  '30'

 L. 444        40  LOAD_FAST                'node'
               42  LOAD_METHOD              unlink
               44  CALL_METHOD_0         0  ''
               46  POP_TOP          

 L. 445        48  LOAD_FAST                'node'
               50  LOAD_ATTR                value
               52  LOAD_ATTR                expiration
               54  LOAD_GLOBAL              time
               56  LOAD_METHOD              time
               58  CALL_METHOD_0         0  ''
               60  COMPARE_OP               <=
               62  POP_JUMP_IF_FALSE    82  'to 82'

 L. 446        64  LOAD_FAST                'self'
               66  LOAD_ATTR                data
               68  LOAD_FAST                'node'
               70  LOAD_ATTR                key
               72  DELETE_SUBSCR    

 L. 447        74  POP_BLOCK        
               76  CALL_FINALLY        104  'to 104'
               78  LOAD_CONST               None
               80  RETURN_VALUE     
             82_0  COME_FROM            62  '62'

 L. 448        82  LOAD_FAST                'node'
               84  LOAD_METHOD              link_after
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                sentinel
               90  CALL_METHOD_1         1  ''
               92  POP_TOP          

 L. 449        94  LOAD_FAST                'node'
               96  LOAD_ATTR                value
               98  POP_BLOCK        
              100  CALL_FINALLY        104  'to 104'
              102  RETURN_VALUE     
            104_0  COME_FROM           100  '100'
            104_1  COME_FROM            76  '76'
            104_2  COME_FROM            34  '34'
            104_3  COME_FROM_FINALLY     0  '0'

 L. 451       104  LOAD_FAST                'self'
              106  LOAD_ATTR                lock
              108  LOAD_METHOD              release
              110  CALL_METHOD_0         0  ''
              112  POP_TOP          
              114  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 34

        def put(self, key, value):
            """Associate key and value in the cache.

        *key*, a ``(dns.name.Name, int, int)`` tuple whose values are the
        query name, rdtype, and rdclass respectively.

        *value*, a ``dns.resolver.Answer``, the answer.
        """
            try:
                self.lock.acquire()
                node = self.data.get(key)
                if node is not None:
                    node.unlink()
                    del self.data[node.key]
                while len(self.data) >= self.max_size:
                    node = self.sentinel.prev
                    node.unlink()
                    del self.data[node.key]

                node = LRUCacheNode(key, value)
                node.link_after(self.sentinel)
                self.data[key] = node
            finally:
                self.lock.release()

        def flush(self, key=None):
            """Flush the cache.

        If *key* is not ``None``, only that item is flushed.  Otherwise
        the entire cache is flushed.

        *key*, a ``(dns.name.Name, int, int)`` tuple whose values are the
        query name, rdtype, and rdclass respectively.
        """
            try:
                self.lock.acquire()
                if key is not None:
                    node = self.data.get(key)
                    if node is not None:
                        node.unlink()
                        del self.data[node.key]
                else:
                    node = self.sentinel.next
                    while node != self.sentinel:
                        next = node.next
                        node.prev = None
                        node.next = None
                        node = next

                    self.data = {}
            finally:
                self.lock.release()


    class Resolver(object):
        __doc__ = 'DNS stub resolver.'

        def __init__(self, filename='/etc/resolv.conf', configure=True):
            """*filename*, a ``text`` or file object, specifying a file
        in standard /etc/resolv.conf format.  This parameter is meaningful
        only when *configure* is true and the platform is POSIX.

        *configure*, a ``bool``.  If True (the default), the resolver
        instance is configured in the normal fashion for the operating
        system the resolver is running on.  (I.e. by reading a
        /etc/resolv.conf file on POSIX systems and from the registry
        on Windows systems.)
        """
            self.domain = None
            self.nameservers = None
            self.nameserver_ports = None
            self.port = None
            self.search = None
            self.timeout = None
            self.lifetime = None
            self.keyring = None
            self.keyname = None
            self.keyalgorithm = None
            self.edns = None
            self.ednsflags = None
            self.payload = None
            self.cache = None
            self.flags = None
            self.retry_servfail = False
            self.rotate = False
            self.reset()
            if configure:
                if sys.platform == 'win32':
                    self.read_registry()
                else:
                    if filename:
                        self.read_resolv_conf(filename)

        def reset(self):
            """Reset all resolver configuration to the defaults."""
            self.domain = dns.name.Name(dns.name.from_text(socket.gethostname())[1:])
            if len(self.domain) == 0:
                self.domain = dns.name.root
            self.nameservers = []
            self.nameserver_ports = {}
            self.port = 53
            self.search = []
            self.timeout = 2.0
            self.lifetime = 30.0
            self.keyring = None
            self.keyname = None
            self.keyalgorithm = dns.tsig.default_algorithm
            self.edns = -1
            self.ednsflags = 0
            self.payload = 0
            self.cache = None
            self.flags = None
            self.retry_servfail = False
            self.rotate = False

        def read_resolv_conf--- This code section failed: ---

 L. 576         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'f'
                4  LOAD_GLOBAL              string_types
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    62  'to 62'

 L. 577        10  SETUP_FINALLY        26  'to 26'

 L. 578        12  LOAD_GLOBAL              open
               14  LOAD_FAST                'f'
               16  LOAD_STR                 'r'
               18  CALL_FUNCTION_2       2  ''
               20  STORE_FAST               'f'
               22  POP_BLOCK        
               24  JUMP_FORWARD         56  'to 56'
             26_0  COME_FROM_FINALLY    10  '10'

 L. 579        26  DUP_TOP          
               28  LOAD_GLOBAL              IOError
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    54  'to 54'
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L. 582        40  LOAD_STR                 '127.0.0.1'
               42  BUILD_LIST_1          1 
               44  LOAD_FAST                'self'
               46  STORE_ATTR               nameservers

 L. 583        48  POP_EXCEPT       
               50  LOAD_CONST               None
               52  RETURN_VALUE     
             54_0  COME_FROM            32  '32'
               54  END_FINALLY      
             56_0  COME_FROM            24  '24'

 L. 584        56  LOAD_CONST               True
               58  STORE_FAST               'want_close'
               60  JUMP_FORWARD         66  'to 66'
             62_0  COME_FROM             8  '8'

 L. 586        62  LOAD_CONST               False
               64  STORE_FAST               'want_close'
             66_0  COME_FROM            60  '60'

 L. 587        66  SETUP_FINALLY       290  'to 290'

 L. 588        68  LOAD_FAST                'f'
               70  GET_ITER         
             72_0  COME_FROM           276  '276'
             72_1  COME_FROM           260  '260'
             72_2  COME_FROM            98  '98'
             72_3  COME_FROM            86  '86'
               72  FOR_ITER            286  'to 286'
               74  STORE_FAST               'l'

 L. 589        76  LOAD_GLOBAL              len
               78  LOAD_FAST                'l'
               80  CALL_FUNCTION_1       1  ''
               82  LOAD_CONST               0
               84  COMPARE_OP               ==
               86  POP_JUMP_IF_TRUE     72  'to 72'
               88  LOAD_FAST                'l'
               90  LOAD_CONST               0
               92  BINARY_SUBSCR    
               94  LOAD_STR                 '#'
               96  COMPARE_OP               ==
               98  POP_JUMP_IF_TRUE     72  'to 72'
              100  LOAD_FAST                'l'
              102  LOAD_CONST               0
              104  BINARY_SUBSCR    
              106  LOAD_STR                 ';'
              108  COMPARE_OP               ==
              110  POP_JUMP_IF_FALSE   114  'to 114'

 L. 590       112  JUMP_BACK            72  'to 72'
            114_0  COME_FROM           110  '110'

 L. 591       114  LOAD_FAST                'l'
              116  LOAD_METHOD              split
              118  CALL_METHOD_0         0  ''
              120  STORE_FAST               'tokens'

 L. 594       122  LOAD_GLOBAL              len
              124  LOAD_FAST                'tokens'
              126  CALL_FUNCTION_1       1  ''
              128  LOAD_CONST               2
              130  COMPARE_OP               <
              132  POP_JUMP_IF_FALSE   136  'to 136'

 L. 595       134  JUMP_BACK            72  'to 72'
            136_0  COME_FROM           132  '132'

 L. 597       136  LOAD_FAST                'tokens'
              138  LOAD_CONST               0
              140  BINARY_SUBSCR    
              142  LOAD_STR                 'nameserver'
              144  COMPARE_OP               ==
              146  POP_JUMP_IF_FALSE   166  'to 166'

 L. 598       148  LOAD_FAST                'self'
              150  LOAD_ATTR                nameservers
              152  LOAD_METHOD              append
              154  LOAD_FAST                'tokens'
              156  LOAD_CONST               1
              158  BINARY_SUBSCR    
              160  CALL_METHOD_1         1  ''
              162  POP_TOP          
              164  JUMP_BACK            72  'to 72'
            166_0  COME_FROM           146  '146'

 L. 599       166  LOAD_FAST                'tokens'
              168  LOAD_CONST               0
              170  BINARY_SUBSCR    
              172  LOAD_STR                 'domain'
              174  COMPARE_OP               ==
              176  POP_JUMP_IF_FALSE   198  'to 198'

 L. 600       178  LOAD_GLOBAL              dns
              180  LOAD_ATTR                name
              182  LOAD_METHOD              from_text
              184  LOAD_FAST                'tokens'
              186  LOAD_CONST               1
              188  BINARY_SUBSCR    
              190  CALL_METHOD_1         1  ''
              192  LOAD_FAST                'self'
              194  STORE_ATTR               domain
              196  JUMP_BACK            72  'to 72'
            198_0  COME_FROM           176  '176'

 L. 601       198  LOAD_FAST                'tokens'
              200  LOAD_CONST               0
              202  BINARY_SUBSCR    
              204  LOAD_STR                 'search'
              206  COMPARE_OP               ==
              208  POP_JUMP_IF_FALSE   250  'to 250'

 L. 602       210  LOAD_FAST                'tokens'
              212  LOAD_CONST               1
              214  LOAD_CONST               None
              216  BUILD_SLICE_2         2 
              218  BINARY_SUBSCR    
              220  GET_ITER         
              222  FOR_ITER            248  'to 248'
              224  STORE_FAST               'suffix'

 L. 603       226  LOAD_FAST                'self'
              228  LOAD_ATTR                search
              230  LOAD_METHOD              append
              232  LOAD_GLOBAL              dns
              234  LOAD_ATTR                name
              236  LOAD_METHOD              from_text
              238  LOAD_FAST                'suffix'
              240  CALL_METHOD_1         1  ''
              242  CALL_METHOD_1         1  ''
              244  POP_TOP          
              246  JUMP_BACK           222  'to 222'
              248  JUMP_BACK            72  'to 72'
            250_0  COME_FROM           208  '208'

 L. 604       250  LOAD_FAST                'tokens'
              252  LOAD_CONST               0
              254  BINARY_SUBSCR    
              256  LOAD_STR                 'options'
              258  COMPARE_OP               ==
              260  POP_JUMP_IF_FALSE    72  'to 72'

 L. 605       262  LOAD_STR                 'rotate'
              264  LOAD_FAST                'tokens'
              266  LOAD_CONST               1
              268  LOAD_CONST               None
              270  BUILD_SLICE_2         2 
              272  BINARY_SUBSCR    
              274  COMPARE_OP               in
              276  POP_JUMP_IF_FALSE    72  'to 72'

 L. 606       278  LOAD_CONST               True
              280  LOAD_FAST                'self'
              282  STORE_ATTR               rotate
              284  JUMP_BACK            72  'to 72'
              286  POP_BLOCK        
              288  BEGIN_FINALLY    
            290_0  COME_FROM_FINALLY    66  '66'

 L. 608       290  LOAD_FAST                'want_close'
          292_294  POP_JUMP_IF_FALSE   304  'to 304'

 L. 609       296  LOAD_FAST                'f'
              298  LOAD_METHOD              close
              300  CALL_METHOD_0         0  ''
              302  POP_TOP          
            304_0  COME_FROM           292  '292'
              304  END_FINALLY      

 L. 610       306  LOAD_GLOBAL              len
              308  LOAD_FAST                'self'
              310  LOAD_ATTR                nameservers
              312  CALL_FUNCTION_1       1  ''
              314  LOAD_CONST               0
              316  COMPARE_OP               ==
          318_320  POP_JUMP_IF_FALSE   334  'to 334'

 L. 611       322  LOAD_FAST                'self'
              324  LOAD_ATTR                nameservers
              326  LOAD_METHOD              append
              328  LOAD_STR                 '127.0.0.1'
              330  CALL_METHOD_1         1  ''
              332  POP_TOP          
            334_0  COME_FROM           318  '318'

Parse error at or near `LOAD_CONST' instruction at offset 50

        def _determine_split_char(self, entry):
            if entry.find(' ') >= 0:
                split_char = ' '
            else:
                if entry.find(',') >= 0:
                    split_char = ','
                else:
                    split_char = ' '
            return split_char

        def _config_win32_nameservers(self, nameservers):
            nameservers = str(nameservers)
            split_char = self._determine_split_char(nameservers)
            ns_list = nameservers.split(split_char)
            for ns in ns_list:
                if ns not in self.nameservers:
                    self.nameservers.append(ns)

        def _config_win32_domain(self, domain):
            self.domain = dns.name.from_text(str(domain))

        def _config_win32_search(self, search):
            search = str(search)
            split_char = self._determine_split_char(search)
            search_list = search.split(split_char)
            for s in search_list:
                if s not in self.search:
                    self.search.append(dns.name.from_text(s))

        def _config_win32_fromkey(self, key, always_try_domain):
            try:
                servers, rtype = _winreg.QueryValueEx(key, 'NameServer')
            except WindowsError:
                servers = None
            else:
                if servers:
                    self._config_win32_nameservers(servers)
                elif servers or always_try_domain:
                    try:
                        dom, rtype = _winreg.QueryValueEx(key, 'Domain')
                        if dom:
                            self._config_win32_domain(dom)
                    except WindowsError:
                        pass

                else:
                    try:
                        servers, rtype = _winreg.QueryValueEx(key, 'DhcpNameServer')
                    except WindowsError:
                        servers = None
                    else:
                        if servers:
                            self._config_win32_nameservers(servers)
                            try:
                                dom, rtype = _winreg.QueryValueEx(key, 'DhcpDomain')
                                if dom:
                                    self._config_win32_domain(dom)
                            except WindowsError:
                                pass

                        try:
                            search, rtype = _winreg.QueryValueEx(key, 'SearchList')
                        except WindowsError:
                            search = None
                        else:
                            if search:
                                self._config_win32_search(search)

        def read_registry--- This code section failed: ---

 L. 687         0  LOAD_GLOBAL              _winreg
                2  LOAD_METHOD              ConnectRegistry
                4  LOAD_CONST               None
                6  LOAD_GLOBAL              _winreg
                8  LOAD_ATTR                HKEY_LOCAL_MACHINE
               10  CALL_METHOD_2         2  ''
               12  STORE_FAST               'lm'

 L. 688        14  LOAD_CONST               False
               16  STORE_FAST               'want_scan'

 L. 689        18  SETUP_FINALLY       252  'to 252'

 L. 690        20  SETUP_FINALLY        42  'to 42'

 L. 692        22  LOAD_GLOBAL              _winreg
               24  LOAD_METHOD              OpenKey
               26  LOAD_FAST                'lm'

 L. 693        28  LOAD_STR                 'SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters'

 L. 692        30  CALL_METHOD_2         2  ''
               32  STORE_FAST               'tcp_params'

 L. 695        34  LOAD_CONST               True
               36  STORE_FAST               'want_scan'
               38  POP_BLOCK        
               40  JUMP_FORWARD         74  'to 74'
             42_0  COME_FROM_FINALLY    20  '20'

 L. 696        42  DUP_TOP          
               44  LOAD_GLOBAL              EnvironmentError
               46  COMPARE_OP               exception-match
               48  POP_JUMP_IF_FALSE    72  'to 72'
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L. 698        56  LOAD_GLOBAL              _winreg
               58  LOAD_METHOD              OpenKey
               60  LOAD_FAST                'lm'

 L. 699        62  LOAD_STR                 'SYSTEM\\CurrentControlSet\\Services\\VxD\\MSTCP'

 L. 698        64  CALL_METHOD_2         2  ''
               66  STORE_FAST               'tcp_params'
               68  POP_EXCEPT       
               70  JUMP_FORWARD         74  'to 74'
             72_0  COME_FROM            48  '48'
               72  END_FINALLY      
             74_0  COME_FROM            70  '70'
             74_1  COME_FROM            40  '40'

 L. 701        74  SETUP_FINALLY        92  'to 92'

 L. 702        76  LOAD_FAST                'self'
               78  LOAD_METHOD              _config_win32_fromkey
               80  LOAD_FAST                'tcp_params'
               82  LOAD_CONST               True
               84  CALL_METHOD_2         2  ''
               86  POP_TOP          
               88  POP_BLOCK        
               90  BEGIN_FINALLY    
             92_0  COME_FROM_FINALLY    74  '74'

 L. 704        92  LOAD_FAST                'tcp_params'
               94  LOAD_METHOD              Close
               96  CALL_METHOD_0         0  ''
               98  POP_TOP          
              100  END_FINALLY      

 L. 705       102  LOAD_FAST                'want_scan'
              104  POP_JUMP_IF_FALSE   248  'to 248'

 L. 706       106  LOAD_GLOBAL              _winreg
              108  LOAD_METHOD              OpenKey
              110  LOAD_FAST                'lm'

 L. 707       112  LOAD_STR                 'SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces'

 L. 706       114  CALL_METHOD_2         2  ''
              116  STORE_FAST               'interfaces'

 L. 710       118  SETUP_FINALLY       238  'to 238'

 L. 711       120  LOAD_CONST               0
              122  STORE_FAST               'i'

 L. 713       124  SETUP_FINALLY       208  'to 208'

 L. 714       126  LOAD_GLOBAL              _winreg
              128  LOAD_METHOD              EnumKey
              130  LOAD_FAST                'interfaces'
              132  LOAD_FAST                'i'
              134  CALL_METHOD_2         2  ''
              136  STORE_FAST               'guid'

 L. 715       138  LOAD_FAST                'i'
              140  LOAD_CONST               1
              142  INPLACE_ADD      
              144  STORE_FAST               'i'

 L. 716       146  LOAD_GLOBAL              _winreg
              148  LOAD_METHOD              OpenKey
              150  LOAD_FAST                'interfaces'
              152  LOAD_FAST                'guid'
              154  CALL_METHOD_2         2  ''
              156  STORE_FAST               'key'

 L. 717       158  LOAD_FAST                'self'
              160  LOAD_METHOD              _win32_is_nic_enabled
              162  LOAD_FAST                'lm'
              164  LOAD_FAST                'guid'
              166  LOAD_FAST                'key'
              168  CALL_METHOD_3         3  ''
              170  POP_JUMP_IF_TRUE    176  'to 176'

 L. 718       172  POP_BLOCK        
              174  JUMP_BACK           124  'to 124'
            176_0  COME_FROM           170  '170'

 L. 719       176  SETUP_FINALLY       194  'to 194'

 L. 720       178  LOAD_FAST                'self'
              180  LOAD_METHOD              _config_win32_fromkey
              182  LOAD_FAST                'key'
              184  LOAD_CONST               False
              186  CALL_METHOD_2         2  ''
              188  POP_TOP          
              190  POP_BLOCK        
              192  BEGIN_FINALLY    
            194_0  COME_FROM_FINALLY   176  '176'

 L. 722       194  LOAD_FAST                'key'
              196  LOAD_METHOD              Close
              198  CALL_METHOD_0         0  ''
              200  POP_TOP          
              202  END_FINALLY      
              204  POP_BLOCK        
              206  JUMP_BACK           124  'to 124'
            208_0  COME_FROM_FINALLY   124  '124'

 L. 723       208  DUP_TOP          
              210  LOAD_GLOBAL              EnvironmentError
              212  COMPARE_OP               exception-match
              214  POP_JUMP_IF_FALSE   230  'to 230'
              216  POP_TOP          
              218  POP_TOP          
              220  POP_TOP          

 L. 724       222  POP_EXCEPT       
              224  BREAK_LOOP          234  'to 234'
              226  POP_EXCEPT       
              228  JUMP_BACK           124  'to 124'
            230_0  COME_FROM           214  '214'
              230  END_FINALLY      
              232  JUMP_BACK           124  'to 124'
            234_0  COME_FROM_EXCEPT_CLAUSE   224  '224'
              234  POP_BLOCK        
              236  BEGIN_FINALLY    
            238_0  COME_FROM_FINALLY   118  '118'

 L. 726       238  LOAD_FAST                'interfaces'
              240  LOAD_METHOD              Close
              242  CALL_METHOD_0         0  ''
              244  POP_TOP          
              246  END_FINALLY      
            248_0  COME_FROM           104  '104'
              248  POP_BLOCK        
              250  BEGIN_FINALLY    
            252_0  COME_FROM_FINALLY    18  '18'

 L. 728       252  LOAD_FAST                'lm'
              254  LOAD_METHOD              Close
              256  CALL_METHOD_0         0  ''
              258  POP_TOP          
              260  END_FINALLY      

Parse error at or near `JUMP_BACK' instruction at offset 174

        def _win32_is_nic_enabled--- This code section failed: ---

 L. 736         0  SETUP_FINALLY       146  'to 146'

 L. 739         2  LOAD_GLOBAL              _winreg
                4  LOAD_METHOD              OpenKey

 L. 740         6  LOAD_FAST                'lm'

 L. 741         8  LOAD_STR                 'SYSTEM\\CurrentControlSet\\Control\\Network\\{4D36E972-E325-11CE-BFC1-08002BE10318}\\%s\\Connection'

 L. 743        10  LOAD_FAST                'guid'

 L. 741        12  BINARY_MODULO    

 L. 739        14  CALL_METHOD_2         2  ''
               16  STORE_FAST               'connection_key'

 L. 745        18  SETUP_FINALLY       132  'to 132'

 L. 747        20  LOAD_GLOBAL              _winreg
               22  LOAD_METHOD              QueryValueEx

 L. 748        24  LOAD_FAST                'connection_key'

 L. 748        26  LOAD_STR                 'PnpInstanceID'

 L. 747        28  CALL_METHOD_2         2  ''
               30  UNPACK_SEQUENCE_2     2 
               32  STORE_FAST               'pnp_id'
               34  STORE_FAST               'ttype'

 L. 750        36  LOAD_FAST                'ttype'
               38  LOAD_GLOBAL              _winreg
               40  LOAD_ATTR                REG_SZ
               42  COMPARE_OP               !=
               44  POP_JUMP_IF_FALSE    50  'to 50'

 L. 751        46  LOAD_GLOBAL              ValueError
               48  RAISE_VARARGS_1       1  'exception instance'
             50_0  COME_FROM            44  '44'

 L. 753        50  LOAD_GLOBAL              _winreg
               52  LOAD_METHOD              OpenKey

 L. 754        54  LOAD_FAST                'lm'

 L. 754        56  LOAD_STR                 'SYSTEM\\CurrentControlSet\\Enum\\%s'
               58  LOAD_FAST                'pnp_id'
               60  BINARY_MODULO    

 L. 753        62  CALL_METHOD_2         2  ''
               64  STORE_FAST               'device_key'

 L. 756        66  SETUP_FINALLY       118  'to 118'

 L. 758        68  LOAD_GLOBAL              _winreg
               70  LOAD_METHOD              QueryValueEx

 L. 759        72  LOAD_FAST                'device_key'

 L. 759        74  LOAD_STR                 'ConfigFlags'

 L. 758        76  CALL_METHOD_2         2  ''
               78  UNPACK_SEQUENCE_2     2 
               80  STORE_FAST               'flags'
               82  STORE_FAST               'ttype'

 L. 761        84  LOAD_FAST                'ttype'
               86  LOAD_GLOBAL              _winreg
               88  LOAD_ATTR                REG_DWORD
               90  COMPARE_OP               !=
               92  POP_JUMP_IF_FALSE    98  'to 98'

 L. 762        94  LOAD_GLOBAL              ValueError
               96  RAISE_VARARGS_1       1  'exception instance'
             98_0  COME_FROM            92  '92'

 L. 766        98  LOAD_FAST                'flags'
              100  LOAD_CONST               1
              102  BINARY_AND       
              104  UNARY_NOT        
              106  POP_BLOCK        
              108  CALL_FINALLY        118  'to 118'
              110  POP_BLOCK        
              112  CALL_FINALLY        132  'to 132'
              114  POP_BLOCK        
              116  RETURN_VALUE     
            118_0  COME_FROM           108  '108'
            118_1  COME_FROM_FINALLY    66  '66'

 L. 769       118  LOAD_FAST                'device_key'
              120  LOAD_METHOD              Close
              122  CALL_METHOD_0         0  ''
              124  POP_TOP          
              126  END_FINALLY      
              128  POP_BLOCK        
              130  BEGIN_FINALLY    
            132_0  COME_FROM           112  '112'
            132_1  COME_FROM_FINALLY    18  '18'

 L. 771       132  LOAD_FAST                'connection_key'
              134  LOAD_METHOD              Close
              136  CALL_METHOD_0         0  ''
              138  POP_TOP          
              140  END_FINALLY      
              142  POP_BLOCK        
              144  JUMP_FORWARD        226  'to 226'
            146_0  COME_FROM_FINALLY     0  '0'

 L. 772       146  DUP_TOP          
              148  LOAD_GLOBAL              EnvironmentError
              150  LOAD_GLOBAL              ValueError
              152  BUILD_TUPLE_2         2 
              154  COMPARE_OP               exception-match
              156  POP_JUMP_IF_FALSE   224  'to 224'
              158  POP_TOP          
              160  POP_TOP          
              162  POP_TOP          

 L. 778       164  SETUP_FINALLY       196  'to 196'

 L. 779       166  LOAD_GLOBAL              _winreg
              168  LOAD_METHOD              QueryValueEx
              170  LOAD_FAST                'interface_key'

 L. 780       172  LOAD_STR                 'NTEContextList'

 L. 779       174  CALL_METHOD_2         2  ''
              176  UNPACK_SEQUENCE_2     2 
              178  STORE_FAST               'nte'
              180  STORE_FAST               'ttype'

 L. 781       182  LOAD_FAST                'nte'
              184  LOAD_CONST               None
              186  COMPARE_OP               is-not
              188  POP_BLOCK        
              190  ROT_FOUR         
              192  POP_EXCEPT       
              194  RETURN_VALUE     
            196_0  COME_FROM_FINALLY   164  '164'

 L. 782       196  DUP_TOP          
              198  LOAD_GLOBAL              WindowsError
              200  COMPARE_OP               exception-match
              202  POP_JUMP_IF_FALSE   218  'to 218'
              204  POP_TOP          
              206  POP_TOP          
              208  POP_TOP          

 L. 783       210  POP_EXCEPT       
              212  POP_EXCEPT       
              214  LOAD_CONST               False
              216  RETURN_VALUE     
            218_0  COME_FROM           202  '202'
              218  END_FINALLY      
              220  POP_EXCEPT       
              222  JUMP_FORWARD        226  'to 226'
            224_0  COME_FROM           156  '156'
              224  END_FINALLY      
            226_0  COME_FROM           222  '222'
            226_1  COME_FROM           144  '144'

Parse error at or near `CALL_FINALLY' instruction at offset 108

        def _compute_timeout(self, start, lifetime=None):
            lifetime = self.lifetime if lifetime is None else lifetime
            now = time.time()
            duration = now - start
            if duration < 0:
                if duration < -1:
                    raise Timeout(timeout=duration)
                else:
                    now = start
            if duration >= lifetime:
                raise Timeout(timeout=duration)
            return min(lifetime - duration, self.timeout)

        def query--- This code section failed: ---

 L. 847         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'qname'
                4  LOAD_GLOBAL              string_types
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    24  'to 24'

 L. 848        10  LOAD_GLOBAL              dns
               12  LOAD_ATTR                name
               14  LOAD_METHOD              from_text
               16  LOAD_FAST                'qname'
               18  LOAD_CONST               None
               20  CALL_METHOD_2         2  ''
               22  STORE_FAST               'qname'
             24_0  COME_FROM             8  '8'

 L. 849        24  LOAD_GLOBAL              isinstance
               26  LOAD_FAST                'rdtype'
               28  LOAD_GLOBAL              string_types
               30  CALL_FUNCTION_2       2  ''
               32  POP_JUMP_IF_FALSE    46  'to 46'

 L. 850        34  LOAD_GLOBAL              dns
               36  LOAD_ATTR                rdatatype
               38  LOAD_METHOD              from_text
               40  LOAD_FAST                'rdtype'
               42  CALL_METHOD_1         1  ''
               44  STORE_FAST               'rdtype'
             46_0  COME_FROM            32  '32'

 L. 851        46  LOAD_GLOBAL              dns
               48  LOAD_ATTR                rdatatype
               50  LOAD_METHOD              is_metatype
               52  LOAD_FAST                'rdtype'
               54  CALL_METHOD_1         1  ''
               56  POP_JUMP_IF_FALSE    62  'to 62'

 L. 852        58  LOAD_GLOBAL              NoMetaqueries
               60  RAISE_VARARGS_1       1  'exception instance'
             62_0  COME_FROM            56  '56'

 L. 853        62  LOAD_GLOBAL              isinstance
               64  LOAD_FAST                'rdclass'
               66  LOAD_GLOBAL              string_types
               68  CALL_FUNCTION_2       2  ''
               70  POP_JUMP_IF_FALSE    84  'to 84'

 L. 854        72  LOAD_GLOBAL              dns
               74  LOAD_ATTR                rdataclass
               76  LOAD_METHOD              from_text
               78  LOAD_FAST                'rdclass'
               80  CALL_METHOD_1         1  ''
               82  STORE_FAST               'rdclass'
             84_0  COME_FROM            70  '70'

 L. 855        84  LOAD_GLOBAL              dns
               86  LOAD_ATTR                rdataclass
               88  LOAD_METHOD              is_metaclass
               90  LOAD_FAST                'rdclass'
               92  CALL_METHOD_1         1  ''
               94  POP_JUMP_IF_FALSE   100  'to 100'

 L. 856        96  LOAD_GLOBAL              NoMetaqueries
               98  RAISE_VARARGS_1       1  'exception instance'
            100_0  COME_FROM            94  '94'

 L. 857       100  BUILD_LIST_0          0 
              102  STORE_FAST               'qnames_to_try'

 L. 858       104  LOAD_FAST                'qname'
              106  LOAD_METHOD              is_absolute
              108  CALL_METHOD_0         0  ''
              110  POP_JUMP_IF_FALSE   124  'to 124'

 L. 859       112  LOAD_FAST                'qnames_to_try'
              114  LOAD_METHOD              append
              116  LOAD_FAST                'qname'
              118  CALL_METHOD_1         1  ''
              120  POP_TOP          
              122  JUMP_FORWARD        210  'to 210'
            124_0  COME_FROM           110  '110'

 L. 861       124  LOAD_GLOBAL              len
              126  LOAD_FAST                'qname'
              128  CALL_FUNCTION_1       1  ''
              130  LOAD_CONST               1
              132  COMPARE_OP               >
              134  POP_JUMP_IF_FALSE   156  'to 156'

 L. 862       136  LOAD_FAST                'qnames_to_try'
              138  LOAD_METHOD              append
              140  LOAD_FAST                'qname'
              142  LOAD_METHOD              concatenate
              144  LOAD_GLOBAL              dns
              146  LOAD_ATTR                name
              148  LOAD_ATTR                root
              150  CALL_METHOD_1         1  ''
              152  CALL_METHOD_1         1  ''
              154  POP_TOP          
            156_0  COME_FROM           134  '134'

 L. 863       156  LOAD_FAST                'self'
              158  LOAD_ATTR                search
              160  POP_JUMP_IF_FALSE   192  'to 192'

 L. 864       162  LOAD_FAST                'self'
              164  LOAD_ATTR                search
              166  GET_ITER         
              168  FOR_ITER            190  'to 190'
              170  STORE_FAST               'suffix'

 L. 865       172  LOAD_FAST                'qnames_to_try'
              174  LOAD_METHOD              append
              176  LOAD_FAST                'qname'
              178  LOAD_METHOD              concatenate
              180  LOAD_FAST                'suffix'
              182  CALL_METHOD_1         1  ''
              184  CALL_METHOD_1         1  ''
              186  POP_TOP          
              188  JUMP_BACK           168  'to 168'
              190  JUMP_FORWARD        210  'to 210'
            192_0  COME_FROM           160  '160'

 L. 867       192  LOAD_FAST                'qnames_to_try'
              194  LOAD_METHOD              append
              196  LOAD_FAST                'qname'
              198  LOAD_METHOD              concatenate
              200  LOAD_FAST                'self'
              202  LOAD_ATTR                domain
              204  CALL_METHOD_1         1  ''
              206  CALL_METHOD_1         1  ''
              208  POP_TOP          
            210_0  COME_FROM           190  '190'
            210_1  COME_FROM           122  '122'

 L. 868       210  LOAD_CONST               True
              212  STORE_FAST               'all_nxdomain'

 L. 869       214  BUILD_MAP_0           0 
              216  STORE_FAST               'nxdomain_responses'

 L. 870       218  LOAD_GLOBAL              time
              220  LOAD_METHOD              time
              222  CALL_METHOD_0         0  ''
              224  STORE_FAST               'start'

 L. 871       226  LOAD_CONST               None
              228  STORE_FAST               '_qname'

 L. 872       230  LOAD_FAST                'qnames_to_try'
              232  GET_ITER         
          234_236  FOR_ITER           1234  'to 1234'
              238  STORE_FAST               '_qname'

 L. 873       240  LOAD_FAST                'self'
              242  LOAD_ATTR                cache
          244_246  POP_JUMP_IF_FALSE   316  'to 316'

 L. 874       248  LOAD_FAST                'self'
              250  LOAD_ATTR                cache
              252  LOAD_METHOD              get
              254  LOAD_FAST                '_qname'
              256  LOAD_FAST                'rdtype'
              258  LOAD_FAST                'rdclass'
              260  BUILD_TUPLE_3         3 
              262  CALL_METHOD_1         1  ''
              264  STORE_FAST               'answer'

 L. 875       266  LOAD_FAST                'answer'
              268  LOAD_CONST               None
              270  COMPARE_OP               is-not
          272_274  POP_JUMP_IF_FALSE   316  'to 316'

 L. 876       276  LOAD_FAST                'answer'
              278  LOAD_ATTR                rrset
              280  LOAD_CONST               None
              282  COMPARE_OP               is
          284_286  POP_JUMP_IF_FALSE   308  'to 308'
              288  LOAD_FAST                'raise_on_no_answer'
          290_292  POP_JUMP_IF_FALSE   308  'to 308'

 L. 877       294  LOAD_GLOBAL              NoAnswer
              296  LOAD_FAST                'answer'
              298  LOAD_ATTR                response
              300  LOAD_CONST               ('response',)
              302  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              304  RAISE_VARARGS_1       1  'exception instance'
              306  JUMP_FORWARD        316  'to 316'
            308_0  COME_FROM           290  '290'
            308_1  COME_FROM           284  '284'

 L. 879       308  LOAD_FAST                'answer'
              310  ROT_TWO          
              312  POP_TOP          
              314  RETURN_VALUE     
            316_0  COME_FROM           306  '306'
            316_1  COME_FROM           272  '272'
            316_2  COME_FROM           244  '244'

 L. 880       316  LOAD_GLOBAL              dns
              318  LOAD_ATTR                message
              320  LOAD_METHOD              make_query
              322  LOAD_FAST                '_qname'
              324  LOAD_FAST                'rdtype'
              326  LOAD_FAST                'rdclass'
              328  CALL_METHOD_3         3  ''
              330  STORE_FAST               'request'

 L. 881       332  LOAD_FAST                'self'
              334  LOAD_ATTR                keyname
              336  LOAD_CONST               None
              338  COMPARE_OP               is-not
          340_342  POP_JUMP_IF_FALSE   366  'to 366'

 L. 882       344  LOAD_FAST                'request'
              346  LOAD_ATTR                use_tsig
              348  LOAD_FAST                'self'
              350  LOAD_ATTR                keyring
              352  LOAD_FAST                'self'
              354  LOAD_ATTR                keyname

 L. 883       356  LOAD_FAST                'self'
              358  LOAD_ATTR                keyalgorithm

 L. 882       360  LOAD_CONST               ('algorithm',)
              362  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              364  POP_TOP          
            366_0  COME_FROM           340  '340'

 L. 884       366  LOAD_FAST                'request'
              368  LOAD_METHOD              use_edns
              370  LOAD_FAST                'self'
              372  LOAD_ATTR                edns
              374  LOAD_FAST                'self'
              376  LOAD_ATTR                ednsflags
              378  LOAD_FAST                'self'
              380  LOAD_ATTR                payload
              382  CALL_METHOD_3         3  ''
              384  POP_TOP          

 L. 885       386  LOAD_FAST                'self'
              388  LOAD_ATTR                flags
              390  LOAD_CONST               None
              392  COMPARE_OP               is-not
          394_396  POP_JUMP_IF_FALSE   406  'to 406'

 L. 886       398  LOAD_FAST                'self'
              400  LOAD_ATTR                flags
              402  LOAD_FAST                'request'
              404  STORE_ATTR               flags
            406_0  COME_FROM           394  '394'

 L. 887       406  LOAD_CONST               None
              408  STORE_FAST               'response'

 L. 891       410  LOAD_FAST                'self'
              412  LOAD_ATTR                nameservers
              414  LOAD_CONST               None
              416  LOAD_CONST               None
              418  BUILD_SLICE_2         2 
              420  BINARY_SUBSCR    
              422  STORE_FAST               'nameservers'

 L. 892       424  BUILD_LIST_0          0 
              426  STORE_FAST               'errors'

 L. 893       428  LOAD_FAST                'self'
              430  LOAD_ATTR                rotate
          432_434  POP_JUMP_IF_FALSE   446  'to 446'

 L. 894       436  LOAD_GLOBAL              random
              438  LOAD_METHOD              shuffle
              440  LOAD_FAST                'nameservers'
              442  CALL_METHOD_1         1  ''
              444  POP_TOP          
            446_0  COME_FROM           432  '432'

 L. 895       446  LOAD_CONST               0.1
              448  STORE_FAST               'backoff'
            450_0  COME_FROM          1146  '1146'

 L. 896       450  LOAD_FAST                'response'
              452  LOAD_CONST               None
              454  COMPARE_OP               is
          456_458  POP_JUMP_IF_FALSE  1194  'to 1194'

 L. 897       460  LOAD_GLOBAL              len
              462  LOAD_FAST                'nameservers'
              464  CALL_FUNCTION_1       1  ''
              466  LOAD_CONST               0
              468  COMPARE_OP               ==
          470_472  POP_JUMP_IF_FALSE   486  'to 486'

 L. 898       474  LOAD_GLOBAL              NoNameservers
              476  LOAD_FAST                'request'
              478  LOAD_FAST                'errors'
              480  LOAD_CONST               ('request', 'errors')
              482  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              484  RAISE_VARARGS_1       1  'exception instance'
            486_0  COME_FROM           470  '470'

 L. 899       486  LOAD_FAST                'nameservers'
              488  LOAD_CONST               None
              490  LOAD_CONST               None
              492  BUILD_SLICE_2         2 
              494  BINARY_SUBSCR    
              496  GET_ITER         
          498_500  FOR_ITER           1122  'to 1122'
              502  STORE_FAST               'nameserver'

 L. 900       504  LOAD_FAST                'self'
              506  LOAD_METHOD              _compute_timeout
              508  LOAD_FAST                'start'
              510  LOAD_FAST                'lifetime'
              512  CALL_METHOD_2         2  ''
              514  STORE_FAST               'timeout'

 L. 901       516  LOAD_FAST                'self'
              518  LOAD_ATTR                nameserver_ports
              520  LOAD_METHOD              get
              522  LOAD_FAST                'nameserver'
              524  LOAD_FAST                'self'
              526  LOAD_ATTR                port
              528  CALL_METHOD_2         2  ''
              530  STORE_FAST               'port'

 L. 902       532  SETUP_FINALLY       656  'to 656'

 L. 903       534  LOAD_FAST                'tcp'
              536  STORE_FAST               'tcp_attempt'

 L. 904       538  LOAD_FAST                'tcp'
          540_542  POP_JUMP_IF_FALSE   570  'to 570'

 L. 905       544  LOAD_GLOBAL              dns
              546  LOAD_ATTR                query
              548  LOAD_ATTR                tcp
              550  LOAD_FAST                'request'
              552  LOAD_FAST                'nameserver'

 L. 906       554  LOAD_FAST                'timeout'

 L. 906       556  LOAD_FAST                'port'

 L. 907       558  LOAD_FAST                'source'

 L. 908       560  LOAD_FAST                'source_port'

 L. 905       562  LOAD_CONST               ('source', 'source_port')
              564  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              566  STORE_FAST               'response'
              568  JUMP_FORWARD        650  'to 650'
            570_0  COME_FROM           540  '540'

 L. 910       570  LOAD_GLOBAL              dns
              572  LOAD_ATTR                query
              574  LOAD_ATTR                udp
              576  LOAD_FAST                'request'
              578  LOAD_FAST                'nameserver'

 L. 911       580  LOAD_FAST                'timeout'

 L. 911       582  LOAD_FAST                'port'

 L. 912       584  LOAD_FAST                'source'

 L. 913       586  LOAD_FAST                'source_port'

 L. 910       588  LOAD_CONST               ('source', 'source_port')
              590  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              592  STORE_FAST               'response'

 L. 914       594  LOAD_FAST                'response'
              596  LOAD_ATTR                flags
              598  LOAD_GLOBAL              dns
              600  LOAD_ATTR                flags
              602  LOAD_ATTR                TC
              604  BINARY_AND       
          606_608  POP_JUMP_IF_FALSE   650  'to 650'

 L. 916       610  LOAD_CONST               True
              612  STORE_FAST               'tcp_attempt'

 L. 917       614  LOAD_FAST                'self'
              616  LOAD_METHOD              _compute_timeout
              618  LOAD_FAST                'start'
              620  LOAD_FAST                'lifetime'
              622  CALL_METHOD_2         2  ''
              624  STORE_FAST               'timeout'

 L. 919       626  LOAD_GLOBAL              dns
              628  LOAD_ATTR                query
              630  LOAD_ATTR                tcp
              632  LOAD_FAST                'request'
              634  LOAD_FAST                'nameserver'

 L. 920       636  LOAD_FAST                'timeout'

 L. 920       638  LOAD_FAST                'port'

 L. 921       640  LOAD_FAST                'source'

 L. 922       642  LOAD_FAST                'source_port'

 L. 919       644  LOAD_CONST               ('source', 'source_port')
              646  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'

 L. 918       648  STORE_FAST               'response'
            650_0  COME_FROM           606  '606'
            650_1  COME_FROM           568  '568'
              650  POP_BLOCK        
          652_654  JUMP_FORWARD        968  'to 968'
            656_0  COME_FROM_FINALLY   532  '532'

 L. 923       656  DUP_TOP          
              658  LOAD_GLOBAL              socket
              660  LOAD_ATTR                error
              662  LOAD_GLOBAL              dns
              664  LOAD_ATTR                exception
              666  LOAD_ATTR                Timeout
              668  BUILD_TUPLE_2         2 
              670  COMPARE_OP               exception-match
          672_674  POP_JUMP_IF_FALSE   734  'to 734'
              676  POP_TOP          
              678  STORE_FAST               'ex'
              680  POP_TOP          
              682  SETUP_FINALLY       722  'to 722'

 L. 928       684  LOAD_FAST                'errors'
              686  LOAD_METHOD              append
              688  LOAD_FAST                'nameserver'
              690  LOAD_FAST                'tcp_attempt'
              692  LOAD_FAST                'port'
              694  LOAD_FAST                'ex'

 L. 929       696  LOAD_FAST                'response'

 L. 928       698  BUILD_TUPLE_5         5 
              700  CALL_METHOD_1         1  ''
              702  POP_TOP          

 L. 930       704  LOAD_CONST               None
              706  STORE_FAST               'response'

 L. 931       708  POP_BLOCK        
              710  POP_EXCEPT       
              712  CALL_FINALLY        722  'to 722'
          714_716  JUMP_BACK           498  'to 498'
              718  POP_BLOCK        
              720  BEGIN_FINALLY    
            722_0  COME_FROM           712  '712'
            722_1  COME_FROM_FINALLY   682  '682'
              722  LOAD_CONST               None
              724  STORE_FAST               'ex'
              726  DELETE_FAST              'ex'
              728  END_FINALLY      
              730  POP_EXCEPT       
              732  JUMP_FORWARD        968  'to 968'
            734_0  COME_FROM           672  '672'

 L. 932       734  DUP_TOP          
              736  LOAD_GLOBAL              dns
              738  LOAD_ATTR                query
              740  LOAD_ATTR                UnexpectedSource
              742  COMPARE_OP               exception-match
          744_746  POP_JUMP_IF_FALSE   806  'to 806'
              748  POP_TOP          
              750  STORE_FAST               'ex'
              752  POP_TOP          
              754  SETUP_FINALLY       794  'to 794'

 L. 936       756  LOAD_FAST                'errors'
              758  LOAD_METHOD              append
              760  LOAD_FAST                'nameserver'
              762  LOAD_FAST                'tcp_attempt'
              764  LOAD_FAST                'port'
              766  LOAD_FAST                'ex'

 L. 937       768  LOAD_FAST                'response'

 L. 936       770  BUILD_TUPLE_5         5 
              772  CALL_METHOD_1         1  ''
              774  POP_TOP          

 L. 938       776  LOAD_CONST               None
              778  STORE_FAST               'response'

 L. 939       780  POP_BLOCK        
              782  POP_EXCEPT       
              784  CALL_FINALLY        794  'to 794'
          786_788  JUMP_BACK           498  'to 498'
              790  POP_BLOCK        
              792  BEGIN_FINALLY    
            794_0  COME_FROM           784  '784'
            794_1  COME_FROM_FINALLY   754  '754'
              794  LOAD_CONST               None
              796  STORE_FAST               'ex'
              798  DELETE_FAST              'ex'
              800  END_FINALLY      
              802  POP_EXCEPT       
              804  JUMP_FORWARD        968  'to 968'
            806_0  COME_FROM           744  '744'

 L. 940       806  DUP_TOP          
              808  LOAD_GLOBAL              dns
              810  LOAD_ATTR                exception
              812  LOAD_ATTR                FormError
              814  COMPARE_OP               exception-match
          816_818  POP_JUMP_IF_FALSE   888  'to 888'
              820  POP_TOP          
              822  STORE_FAST               'ex'
              824  POP_TOP          
              826  SETUP_FINALLY       876  'to 876'

 L. 946       828  LOAD_FAST                'nameservers'
              830  LOAD_METHOD              remove
              832  LOAD_FAST                'nameserver'
              834  CALL_METHOD_1         1  ''
              836  POP_TOP          

 L. 947       838  LOAD_FAST                'errors'
              840  LOAD_METHOD              append
              842  LOAD_FAST                'nameserver'
              844  LOAD_FAST                'tcp_attempt'
              846  LOAD_FAST                'port'
              848  LOAD_FAST                'ex'

 L. 948       850  LOAD_FAST                'response'

 L. 947       852  BUILD_TUPLE_5         5 
              854  CALL_METHOD_1         1  ''
              856  POP_TOP          

 L. 949       858  LOAD_CONST               None
              860  STORE_FAST               'response'

 L. 950       862  POP_BLOCK        
              864  POP_EXCEPT       
              866  CALL_FINALLY        876  'to 876'
          868_870  JUMP_BACK           498  'to 498'
              872  POP_BLOCK        
              874  BEGIN_FINALLY    
            876_0  COME_FROM           866  '866'
            876_1  COME_FROM_FINALLY   826  '826'
              876  LOAD_CONST               None
              878  STORE_FAST               'ex'
              880  DELETE_FAST              'ex'
              882  END_FINALLY      
              884  POP_EXCEPT       
              886  JUMP_FORWARD        968  'to 968'
            888_0  COME_FROM           816  '816'

 L. 951       888  DUP_TOP          
              890  LOAD_GLOBAL              EOFError
              892  COMPARE_OP               exception-match
          894_896  POP_JUMP_IF_FALSE   966  'to 966'
              898  POP_TOP          
              900  STORE_FAST               'ex'
              902  POP_TOP          
              904  SETUP_FINALLY       954  'to 954'

 L. 958       906  LOAD_FAST                'nameservers'
              908  LOAD_METHOD              remove
              910  LOAD_FAST                'nameserver'
              912  CALL_METHOD_1         1  ''
              914  POP_TOP          

 L. 959       916  LOAD_FAST                'errors'
              918  LOAD_METHOD              append
              920  LOAD_FAST                'nameserver'
              922  LOAD_FAST                'tcp_attempt'
              924  LOAD_FAST                'port'
              926  LOAD_FAST                'ex'

 L. 960       928  LOAD_FAST                'response'

 L. 959       930  BUILD_TUPLE_5         5 
              932  CALL_METHOD_1         1  ''
              934  POP_TOP          

 L. 961       936  LOAD_CONST               None
              938  STORE_FAST               'response'

 L. 962       940  POP_BLOCK        
              942  POP_EXCEPT       
              944  CALL_FINALLY        954  'to 954'
          946_948  JUMP_BACK           498  'to 498'
              950  POP_BLOCK        
              952  BEGIN_FINALLY    
            954_0  COME_FROM           944  '944'
            954_1  COME_FROM_FINALLY   904  '904'
              954  LOAD_CONST               None
              956  STORE_FAST               'ex'
              958  DELETE_FAST              'ex'
              960  END_FINALLY      
              962  POP_EXCEPT       
              964  JUMP_FORWARD        968  'to 968'
            966_0  COME_FROM           894  '894'
              966  END_FINALLY      
            968_0  COME_FROM           964  '964'
            968_1  COME_FROM           886  '886'
            968_2  COME_FROM           804  '804'
            968_3  COME_FROM           732  '732'
            968_4  COME_FROM           652  '652'

 L. 963       968  LOAD_FAST                'response'
              970  LOAD_METHOD              rcode
              972  CALL_METHOD_0         0  ''
              974  STORE_FAST               'rcode'

 L. 964       976  LOAD_FAST                'rcode'
              978  LOAD_GLOBAL              dns
              980  LOAD_ATTR                rcode
              982  LOAD_ATTR                YXDOMAIN
              984  COMPARE_OP               ==
          986_988  POP_JUMP_IF_FALSE  1020  'to 1020'

 L. 965       990  LOAD_GLOBAL              YXDOMAIN
              992  CALL_FUNCTION_0       0  ''
              994  STORE_FAST               'ex'

 L. 966       996  LOAD_FAST                'errors'
              998  LOAD_METHOD              append
             1000  LOAD_FAST                'nameserver'
             1002  LOAD_FAST                'tcp_attempt'
             1004  LOAD_FAST                'port'
             1006  LOAD_FAST                'ex'

 L. 967      1008  LOAD_FAST                'response'

 L. 966      1010  BUILD_TUPLE_5         5 
             1012  CALL_METHOD_1         1  ''
             1014  POP_TOP          

 L. 968      1016  LOAD_FAST                'ex'
             1018  RAISE_VARARGS_1       1  'exception instance'
           1020_0  COME_FROM           986  '986'

 L. 969      1020  LOAD_FAST                'rcode'
             1022  LOAD_GLOBAL              dns
             1024  LOAD_ATTR                rcode
             1026  LOAD_ATTR                NOERROR
             1028  COMPARE_OP               ==
         1030_1032  POP_JUMP_IF_TRUE   1048  'to 1048'

 L. 970      1034  LOAD_FAST                'rcode'
             1036  LOAD_GLOBAL              dns
             1038  LOAD_ATTR                rcode
             1040  LOAD_ATTR                NXDOMAIN
             1042  COMPARE_OP               ==

 L. 969  1044_1046  POP_JUMP_IF_FALSE  1054  'to 1054'
           1048_0  COME_FROM          1030  '1030'

 L. 971      1048  POP_TOP          
         1050_1052  JUMP_ABSOLUTE      1122  'to 1122'
           1054_0  COME_FROM          1044  '1044'

 L. 977      1054  LOAD_FAST                'rcode'
             1056  LOAD_GLOBAL              dns
             1058  LOAD_ATTR                rcode
             1060  LOAD_ATTR                SERVFAIL
             1062  COMPARE_OP               !=
         1064_1066  POP_JUMP_IF_TRUE   1076  'to 1076'
             1068  LOAD_FAST                'self'
             1070  LOAD_ATTR                retry_servfail
         1072_1074  POP_JUMP_IF_TRUE   1086  'to 1086'
           1076_0  COME_FROM          1064  '1064'

 L. 978      1076  LOAD_FAST                'nameservers'
             1078  LOAD_METHOD              remove
             1080  LOAD_FAST                'nameserver'
             1082  CALL_METHOD_1         1  ''
             1084  POP_TOP          
           1086_0  COME_FROM          1072  '1072'

 L. 979      1086  LOAD_FAST                'errors'
             1088  LOAD_METHOD              append
             1090  LOAD_FAST                'nameserver'
             1092  LOAD_FAST                'tcp_attempt'
             1094  LOAD_FAST                'port'

 L. 980      1096  LOAD_GLOBAL              dns
             1098  LOAD_ATTR                rcode
             1100  LOAD_METHOD              to_text
             1102  LOAD_FAST                'rcode'
             1104  CALL_METHOD_1         1  ''

 L. 980      1106  LOAD_FAST                'response'

 L. 979      1108  BUILD_TUPLE_5         5 
             1110  CALL_METHOD_1         1  ''
             1112  POP_TOP          

 L. 981      1114  LOAD_CONST               None
             1116  STORE_FAST               'response'
         1118_1120  JUMP_BACK           498  'to 498'

 L. 982      1122  LOAD_FAST                'response'
             1124  LOAD_CONST               None
             1126  COMPARE_OP               is-not
         1128_1130  POP_JUMP_IF_FALSE  1136  'to 1136'

 L. 983  1132_1134  BREAK_LOOP         1194  'to 1194'
           1136_0  COME_FROM          1128  '1128'

 L. 987      1136  LOAD_GLOBAL              len
             1138  LOAD_FAST                'nameservers'
             1140  CALL_FUNCTION_1       1  ''
             1142  LOAD_CONST               0
             1144  COMPARE_OP               >
         1146_1148  POP_JUMP_IF_FALSE   450  'to 450'

 L. 992      1150  LOAD_FAST                'self'
             1152  LOAD_METHOD              _compute_timeout
             1154  LOAD_FAST                'start'
             1156  LOAD_FAST                'lifetime'
             1158  CALL_METHOD_2         2  ''
             1160  STORE_FAST               'timeout'

 L. 993      1162  LOAD_GLOBAL              min
             1164  LOAD_FAST                'timeout'
             1166  LOAD_FAST                'backoff'
             1168  CALL_FUNCTION_2       2  ''
             1170  STORE_FAST               'sleep_time'

 L. 994      1172  LOAD_FAST                'backoff'
             1174  LOAD_CONST               2
             1176  INPLACE_MULTIPLY 
             1178  STORE_FAST               'backoff'

 L. 995      1180  LOAD_GLOBAL              time
             1182  LOAD_METHOD              sleep
             1184  LOAD_FAST                'sleep_time'
             1186  CALL_METHOD_1         1  ''
             1188  POP_TOP          
         1190_1192  JUMP_BACK           450  'to 450'
           1194_0  COME_FROM           456  '456'

 L. 996      1194  LOAD_FAST                'response'
             1196  LOAD_METHOD              rcode
             1198  CALL_METHOD_0         0  ''
             1200  LOAD_GLOBAL              dns
             1202  LOAD_ATTR                rcode
             1204  LOAD_ATTR                NXDOMAIN
             1206  COMPARE_OP               ==
         1208_1210  POP_JUMP_IF_FALSE  1222  'to 1222'

 L. 997      1212  LOAD_FAST                'response'
             1214  LOAD_FAST                'nxdomain_responses'
             1216  LOAD_FAST                '_qname'
             1218  STORE_SUBSCR     

 L. 998      1220  JUMP_BACK           234  'to 234'
           1222_0  COME_FROM          1208  '1208'

 L. 999      1222  LOAD_CONST               False
             1224  STORE_FAST               'all_nxdomain'

 L.1000      1226  POP_TOP          
         1228_1230  BREAK_LOOP         1234  'to 1234'
             1232  JUMP_BACK           234  'to 234'

 L.1001      1234  LOAD_FAST                'all_nxdomain'
         1236_1238  POP_JUMP_IF_FALSE  1252  'to 1252'

 L.1002      1240  LOAD_GLOBAL              NXDOMAIN
             1242  LOAD_FAST                'qnames_to_try'
             1244  LOAD_FAST                'nxdomain_responses'
             1246  LOAD_CONST               ('qnames', 'responses')
             1248  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1250  RAISE_VARARGS_1       1  'exception instance'
           1252_0  COME_FROM          1236  '1236'

 L.1003      1252  LOAD_GLOBAL              Answer
             1254  LOAD_FAST                '_qname'
             1256  LOAD_FAST                'rdtype'
             1258  LOAD_FAST                'rdclass'
             1260  LOAD_FAST                'response'

 L.1004      1262  LOAD_FAST                'raise_on_no_answer'

 L.1003      1264  CALL_FUNCTION_5       5  ''
             1266  STORE_FAST               'answer'

 L.1005      1268  LOAD_FAST                'self'
             1270  LOAD_ATTR                cache
         1272_1274  POP_JUMP_IF_FALSE  1296  'to 1296'

 L.1006      1276  LOAD_FAST                'self'
             1278  LOAD_ATTR                cache
             1280  LOAD_METHOD              put
             1282  LOAD_FAST                '_qname'
             1284  LOAD_FAST                'rdtype'
             1286  LOAD_FAST                'rdclass'
             1288  BUILD_TUPLE_3         3 
             1290  LOAD_FAST                'answer'
             1292  CALL_METHOD_2         2  ''
             1294  POP_TOP          
           1296_0  COME_FROM          1272  '1272'

 L.1007      1296  LOAD_FAST                'answer'
             1298  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 712

        def use_tsig(self, keyring, keyname=None, algorithm=dns.tsig.default_algorithm):
            """Add a TSIG signature to the query.

        See the documentation of the Message class for a complete
        description of the keyring dictionary.

        *keyring*, a ``dict``, the TSIG keyring to use.  If a
        *keyring* is specified but a *keyname* is not, then the key
        used will be the first key in the *keyring*.  Note that the
        order of keys in a dictionary is not defined, so applications
        should supply a keyname when a keyring is used, unless they
        know the keyring contains only one key.

        *keyname*, a ``dns.name.Name`` or ``None``, the name of the TSIG key
        to use; defaults to ``None``. The key must be defined in the keyring.

        *algorithm*, a ``dns.name.Name``, the TSIG algorithm to use.
        """
            self.keyring = keyring
            if keyname is None:
                self.keyname = list(self.keyring.keys())[0]
            else:
                self.keyname = keyname
            self.keyalgorithm = algorithm

        def use_edns(self, edns, ednsflags, payload):
            """Configure EDNS behavior.

        *edns*, an ``int``, is the EDNS level to use.  Specifying
        ``None``, ``False``, or ``-1`` means "do not use EDNS", and in this case
        the other parameters are ignored.  Specifying ``True`` is
        equivalent to specifying 0, i.e. "use EDNS0".

        *ednsflags*, an ``int``, the EDNS flag values.

        *payload*, an ``int``, is the EDNS sender's payload field, which is the
        maximum size of UDP datagram the sender can handle.  I.e. how big
        a response to this message can be.
        """
            if edns is None:
                edns = -1
            self.edns = edns
            self.ednsflags = ednsflags
            self.payload = payload

        def set_flags(self, flags):
            """Overrides the default flags with your own.

        *flags*, an ``int``, the message flags to use.
        """
            self.flags = flags


    default_resolver = None

    def get_default_resolver():
        """Get the default resolver, initializing it if necessary."""
        global default_resolver
        if default_resolver is None:
            reset_default_resolver()
        return default_resolver


    def reset_default_resolver():
        """Re-initialize default resolver.

    Note that the resolver configuration (i.e. /etc/resolv.conf on UNIX
    systems) will be re-read immediately.
    """
        global default_resolver
        default_resolver = Resolver()


    def query(qname, rdtype=dns.rdatatype.A, rdclass=dns.rdataclass.IN, tcp=False, source=None, raise_on_no_answer=True, source_port=0, lifetime=None):
        """Query nameservers to find the answer to the question.

    This is a convenience function that uses the default resolver
    object to make the query.

    See ``dns.resolver.Resolver.query`` for more information on the
    parameters.
    """
        return get_default_resolver().query(qname, rdtype, rdclass, tcp, source, raise_on_no_answer, source_port, lifetime)


    def zone_for_name(name, rdclass=dns.rdataclass.IN, tcp=False, resolver=None):
        """Find the name of the zone which contains the specified name.

    *name*, an absolute ``dns.name.Name`` or ``text``, the query name.

    *rdclass*, an ``int``, the query class.

    *tcp*, a ``bool``.  If ``True``, use TCP to make the query.

    *resolver*, a ``dns.resolver.Resolver`` or ``None``, the resolver to use.
    If ``None``, the default resolver is used.

    Raises ``dns.resolver.NoRootSOA`` if there is no SOA RR at the DNS
    root.  (This is only likely to happen if you're using non-default
    root servers in your network and they are misconfigured.)

    Returns a ``dns.name.Name``.
    """
        if isinstance(name, string_types):
            name = dns.name.from_text(name, dns.name.root)
        else:
            if resolver is None:
                resolver = get_default_resolver()
            assert name.is_absolute(), name
        while True:
            try:
                answer = resolver.query(name, dns.rdatatype.SOA, rdclass, tcp)
                if answer.rrset.name == name:
                    return name
            except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
                pass
            else:
                try:
                    name = name.parent()
                except dns.name.NoParent:
                    raise NoRootSOA


    _protocols_for_socktype = {socket.SOCK_DGRAM: [socket.SOL_UDP], 
     socket.SOCK_STREAM: [socket.SOL_TCP]}
    _resolver = None
    _original_getaddrinfo = socket.getaddrinfo
    _original_getnameinfo = socket.getnameinfo
    _original_getfqdn = socket.getfqdn
    _original_gethostbyname = socket.gethostbyname
    _original_gethostbyname_ex = socket.gethostbyname_ex
    _original_gethostbyaddr = socket.gethostbyaddr

    def _getaddrinfo(host=None, service=None, family=socket.AF_UNSPEC, socktype=0, proto=0, flags=0):
        global _resolver
        if flags & (socket.AI_ADDRCONFIG | socket.AI_V4MAPPED) != 0:
            raise NotImplementedError
        if host is None:
            if service is None:
                raise socket.gaierror(socket.EAI_NONAME)
        v6addrs = []
        v4addrs = []
        canonical_name = None
        try:
            if host is None:
                canonical_name = 'localhost'
                if flags & socket.AI_PASSIVE != 0:
                    v6addrs.append('::')
                    v4addrs.append('0.0.0.0')
                else:
                    v6addrs.append('::1')
                    v4addrs.append('127.0.0.1')
            else:
                parts = host.split('%')
                if len(parts) == 2:
                    ahost = parts[0]
                else:
                    ahost = host
                addr = dns.ipv6.inet_aton(ahost)
                v6addrs.append(host)
                canonical_name = host
        except Exception:
            try:
                addr = dns.ipv4.inet_aton(host)
                v4addrs.append(host)
                canonical_name = host
            except Exception:
                if flags & socket.AI_NUMERICHOST == 0:
                    try:
                        if family == socket.AF_INET6 or family == socket.AF_UNSPEC:
                            v6 = _resolver.query(host, (dns.rdatatype.AAAA), raise_on_no_answer=False)
                            host = v6.qname
                            canonical_name = v6.canonical_name.to_text(True)
                            if v6.rrset is not None:
                                for rdata in v6.rrset:
                                    v6addrs.append(rdata.address)

                        if family == socket.AF_INET or family == socket.AF_UNSPEC:
                            v4 = _resolver.query(host, (dns.rdatatype.A), raise_on_no_answer=False)
                            host = v4.qname
                            canonical_name = v4.canonical_name.to_text(True)
                            if v4.rrset is not None:
                                for rdata in v4.rrset:
                                    v4addrs.append(rdata.address)

                    except dns.resolver.NXDOMAIN:
                        raise socket.gaierror(socket.EAI_NONAME)
                    except Exception:
                        raise socket.gaierror(socket.EAI_SYSTEM)

        else:
            port = None
            try:
                if service is None:
                    port = 0
                else:
                    port = int(service)
            except Exception:
                if flags & socket.AI_NUMERICSERV == 0:
                    try:
                        port = socket.getservbyname(service)
                    except Exception:
                        pass

            else:
                if port is None:
                    raise socket.gaierror(socket.EAI_NONAME)
                else:
                    tuples = []
                    if socktype == 0:
                        socktypes = [
                         socket.SOCK_DGRAM, socket.SOCK_STREAM]
                    else:
                        socktypes = [
                         socktype]
                    if flags & socket.AI_CANONNAME != 0:
                        cname = canonical_name
                    else:
                        cname = ''
            if family == socket.AF_INET6 or family == socket.AF_UNSPEC:
                for addr in v6addrs:
                    for socktype in socktypes:
                        for proto in _protocols_for_socktype[socktype]:
                            tuples.append((socket.AF_INET6, socktype, proto,
                             cname, (addr, port, 0, 0)))

            elif family == socket.AF_INET or family == socket.AF_UNSPEC:
                for addr in v4addrs:
                    for socktype in socktypes:
                        for proto in _protocols_for_socktype[socktype]:
                            tuples.append((socket.AF_INET, socktype, proto,
                             cname, (addr, port)))

            else:
                if len(tuples) == 0:
                    raise socket.gaierror(socket.EAI_NONAME)
                return tuples


    def _getnameinfo(sockaddr, flags=0):
        host = sockaddr[0]
        port = sockaddr[1]
        if len(sockaddr) == 4:
            scope = sockaddr[3]
            family = socket.AF_INET6
        else:
            scope = None
            family = socket.AF_INET
        tuples = _getaddrinfo(host, port, family, socket.SOCK_STREAM, socket.SOL_TCP, 0)
        if len(tuples) > 1:
            raise socket.error('sockaddr resolved to multiple addresses')
        else:
            addr = tuples[0][4][0]
            if flags & socket.NI_DGRAM:
                pname = 'udp'
            else:
                pname = 'tcp'
        qname = dns.reversename.from_address(addr)
        if flags & socket.NI_NUMERICHOST == 0:
            try:
                answer = _resolver.query(qname, 'PTR')
                hostname = answer.rrset[0].target.to_text(True)
            except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
                if flags & socket.NI_NAMEREQD:
                    raise socket.gaierror(socket.EAI_NONAME)
                hostname = addr
                if scope is not None:
                    hostname += '%' + str(scope)

        else:
            hostname = addr
            if scope is not None:
                hostname += '%' + str(scope)
            elif flags & socket.NI_NUMERICSERV:
                service = str(port)
            else:
                service = socket.getservbyport(port, pname)
            return (
             hostname, service)


    def _getfqdn--- This code section failed: ---

 L.1303         0  LOAD_FAST                'name'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L.1304         8  LOAD_GLOBAL              socket
               10  LOAD_METHOD              gethostname
               12  CALL_METHOD_0         0  ''
               14  STORE_FAST               'name'
             16_0  COME_FROM             6  '6'

 L.1305        16  SETUP_FINALLY        46  'to 46'

 L.1306        18  LOAD_GLOBAL              _getnameinfo
               20  LOAD_GLOBAL              _getaddrinfo
               22  LOAD_FAST                'name'
               24  LOAD_CONST               80
               26  CALL_FUNCTION_2       2  ''
               28  LOAD_CONST               0
               30  BINARY_SUBSCR    
               32  LOAD_CONST               4
               34  BINARY_SUBSCR    
               36  CALL_FUNCTION_1       1  ''
               38  LOAD_CONST               0
               40  BINARY_SUBSCR    
               42  POP_BLOCK        
               44  RETURN_VALUE     
             46_0  COME_FROM_FINALLY    16  '16'

 L.1307        46  DUP_TOP          
               48  LOAD_GLOBAL              Exception
               50  COMPARE_OP               exception-match
               52  POP_JUMP_IF_FALSE    68  'to 68'
               54  POP_TOP          
               56  POP_TOP          
               58  POP_TOP          

 L.1308        60  LOAD_FAST                'name'
               62  ROT_FOUR         
               64  POP_EXCEPT       
               66  RETURN_VALUE     
             68_0  COME_FROM            52  '52'
               68  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 56


    def _gethostbyname(name):
        return _gethostbyname_ex(name)[2][0]


    def _gethostbyname_ex(name):
        aliases = []
        addresses = []
        tuples = _getaddrinfo(name, 0, socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP, socket.AI_CANONNAME)
        canonical = tuples[0][3]
        for item in tuples:
            addresses.append(item[4][0])
        else:
            return (
             canonical, aliases, addresses)


    def _gethostbyaddr(ip):
        try:
            dns.ipv6.inet_aton(ip)
            sockaddr = (ip, 80, 0, 0)
            family = socket.AF_INET6
        except Exception:
            sockaddr = (
             ip, 80)
            family = socket.AF_INET
        else:
            name, port = _getnameinfo(sockaddr, socket.NI_NAMEREQD)
            aliases = []
            addresses = []
            tuples = _getaddrinfo(name, 0, family, socket.SOCK_STREAM, socket.SOL_TCP, socket.AI_CANONNAME)
            canonical = tuples[0][3]
            for item in tuples:
                addresses.append(item[4][0])
            else:
                return (
                 canonical, aliases, addresses)


    def override_system_resolver(resolver=None):
        """Override the system resolver routines in the socket module with
    versions which use dnspython's resolver.

    This can be useful in testing situations where you want to control
    the resolution behavior of python code without having to change
    the system's resolver settings (e.g. /etc/resolv.conf).

    The resolver to use may be specified; if it's not, the default
    resolver will be used.

    resolver, a ``dns.resolver.Resolver`` or ``None``, the resolver to use.
    """
        global _resolver
        if resolver is None:
            resolver = get_default_resolver()
        _resolver = resolver
        socket.getaddrinfo = _getaddrinfo
        socket.getnameinfo = _getnameinfo
        socket.getfqdn = _getfqdn
        socket.gethostbyname = _gethostbyname
        socket.gethostbyname_ex = _gethostbyname_ex
        socket.gethostbyaddr = _gethostbyaddr


    def restore_system_resolver():
        """Undo the effects of prior override_system_resolver()."""
        global _resolver
        _resolver = None
        socket.getaddrinfo = _original_getaddrinfo
        socket.getnameinfo = _original_getnameinfo
        socket.getfqdn = _original_getfqdn
        socket.gethostbyname = _original_gethostbyname
        socket.gethostbyname_ex = _original_gethostbyname_ex
        socket.gethostbyaddr = _original_gethostbyaddr