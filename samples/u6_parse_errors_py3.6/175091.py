# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: electrum\paymentrequest.py
import hashlib, sys, time, traceback, json, certifi, urllib.parse, aiohttp
try:
    from . import paymentrequest_pb2 as pb2
except ImportError:
    sys.exit("Error: could not find paymentrequest_pb2.py. Create it with 'protoc --proto_path=electrum/ --python_out=electrum/ electrum/paymentrequest.proto'")

from . import bitcoin, ecc, util, transaction, x509, rsakey
from .util import print_error, bh2u, bfh, export_meta, import_meta, make_aiohttp_session
from .crypto import sha256
from .bitcoin import TYPE_ADDRESS
from .transaction import TxOutput
from .network import Network
REQUEST_HEADERS = {'Accept':'application/bitcoin-paymentrequest', 
 'User-Agent':'Electrum'}
ACK_HEADERS = {'Content-Type':'application/bitcoin-payment',  'Accept':'application/bitcoin-paymentack',  'User-Agent':'Electrum'}
ca_path = certifi.where()
ca_list = None
ca_keyID = None

def load_ca_list():
    global ca_keyID
    global ca_list
    if ca_list is None:
        ca_list, ca_keyID = x509.load_certificates(ca_path)


PR_UNPAID = 0
PR_EXPIRED = 1
PR_UNKNOWN = 2
PR_PAID = 3

async def get_payment_request(url: str) -> 'PaymentRequest':
    u = urllib.parse.urlparse(url)
    error = None
    if u.scheme in ('http', 'https'):
        resp_content = None
        try:
            proxy = Network.get_instance().proxy
            async with make_aiohttp_session(proxy, headers=REQUEST_HEADERS) as session:
                async with session.get(url) as response:
                    resp_content = await response.read()
                    response.raise_for_status()
                    if 'Content-Type' not in response.headers or response.headers['Content-Type'] != 'application/bitcoin-paymentrequest':
                        data = None
                        error = 'payment URL not pointing to a payment request handling server'
                    else:
                        data = resp_content
                    data_len = len(data) if data is not None else None
                    print_error('fetched payment request', url, data_len)
        except aiohttp.ClientError as e:
            error = f"Error while contacting payment URL:\n{repr(e)}"
            if isinstance(e, aiohttp.ClientResponseError) and e.status == 400:
                if resp_content:
                    error += '\n' + resp_content.decode('utf8')
            data = None

    else:
        if u.scheme == 'file':
            try:
                with open((u.path), 'r', encoding='utf-8') as (f):
                    data = f.read()
            except IOError:
                data = None
                error = 'payment URL not pointing to a valid file'

        else:
            data = None
            error = f"Unknown scheme for payment request. URL: {url}"
        pr = PaymentRequest(data, error)
        return pr


class PaymentRequest:

    def __init__(self, data, error=None):
        self.raw = data
        self.error = error
        self.parse(data)
        self.requestor = None
        self.tx = None

    def __str__(self):
        return str(self.raw)

    def parse(self, r):
        if self.error:
            return
        self.id = bh2u(sha256(r)[0:16])
        try:
            self.data = pb2.PaymentRequest()
            self.data.ParseFromString(r)
        except:
            self.error = 'cannot parse payment request'
            return
        else:
            self.details = pb2.PaymentDetails()
            self.details.ParseFromString(self.data.serialized_payment_details)
            self.outputs = []
            for o in self.details.outputs:
                type_, addr = transaction.get_address_from_output_script(o.script)
                if type_ != TYPE_ADDRESS:
                    self.error = 'only addresses are allowed as outputs'
                    return
                self.outputs.append(TxOutput(type_, addr, o.amount))

            self.memo = self.details.memo
            self.payment_url = self.details.payment_url

    def is_pr(self):
        return self.get_amount() != 0

    def verify(self, contacts):
        if self.error:
            return False
        else:
            if not self.raw:
                self.error = 'Empty request'
                return False
            else:
                pr = pb2.PaymentRequest()
                try:
                    pr.ParseFromString(self.raw)
                except:
                    self.error = 'Error: Cannot parse payment request'
                    return False
                else:
                    if not pr.signature:
                        self.requestor = None
                        return True
                    if pr.pki_type in ('x509+sha256', 'x509+sha1'):
                        return self.verify_x509(pr)
                    if pr.pki_type in ('dnssec+btc', 'dnssec+ecdsa'):
                        return self.verify_dnssec(pr, contacts)
            self.error = 'ERROR: Unsupported PKI Type for Message Signature'
            return False

    def verify_x509(self, paymntreq):
        load_ca_list()
        if not ca_list:
            self.error = 'Trusted certificate authorities list not found'
            return False
        else:
            cert = pb2.X509Certificates()
            cert.ParseFromString(paymntreq.pki_data)
            try:
                x, ca = verify_cert_chain(cert.certificate)
            except BaseException as e:
                traceback.print_exc(file=(sys.stderr))
                self.error = str(e)
                return False

            self.requestor = x.get_common_name()
            if self.requestor.startswith('*.'):
                self.requestor = self.requestor[2:]
            pubkey0 = rsakey.RSAKey(x.modulus, x.exponent)
            sig = paymntreq.signature
            paymntreq.signature = b''
            s = paymntreq.SerializeToString()
            sigBytes = bytearray(sig)
            msgBytes = bytearray(s)
            if paymntreq.pki_type == 'x509+sha256':
                hashBytes = bytearray(hashlib.sha256(msgBytes).digest())
                verify = pubkey0.verify(sigBytes, x509.PREFIX_RSA_SHA256 + hashBytes)
            else:
                if paymntreq.pki_type == 'x509+sha1':
                    verify = pubkey0.hashAndVerify(sigBytes, msgBytes)
                else:
                    self.error = f"ERROR: unknown pki_type {paymntreq.pki_type} in Payment Request"
                    return False
            if not verify:
                self.error = 'ERROR: Invalid Signature for Payment Request Data'
                return False
            self.error = 'Signed by Trusted CA: ' + ca.get_common_name()
            return True

    def verify_dnssec(self, pr, contacts):
        sig = pr.signature
        alias = pr.pki_data
        info = contacts.resolve(alias)
        if info.get('validated') is not True:
            self.error = 'Alias verification failed (DNSSEC)'
            return False
        else:
            if pr.pki_type == 'dnssec+btc':
                self.requestor = alias
                address = info.get('address')
                pr.signature = b''
                message = pr.SerializeToString()
                if ecc.verify_message_with_address(address, sig, message):
                    self.error = 'Verified with DNSSEC'
                    return True
                else:
                    self.error = 'verify failed'
                    return False
            else:
                self.error = 'unknown algo'
            return False

    def has_expired(self):
        return self.details.expires and self.details.expires < int(time.time())

    def get_expiration_date(self):
        return self.details.expires

    def get_amount(self):
        return sum(map(lambda x: x[2], self.outputs))

    def get_address(self):
        o = self.outputs[0]
        assert o.type == TYPE_ADDRESS
        return o.address

    def get_requestor(self):
        if self.requestor:
            return self.requestor
        else:
            return self.get_address()

    def get_verify_status(self):
        if self.requestor:
            return self.error
        else:
            return 'No Signature'

    def get_memo(self):
        return self.memo

    def get_dict(self):
        return {'requestor':self.get_requestor(), 
         'memo':self.get_memo(), 
         'exp':self.get_expiration_date(), 
         'amount':self.get_amount(), 
         'signature':self.get_verify_status(), 
         'txid':self.tx, 
         'outputs':self.get_outputs()}

    def get_id(self):
        if self.requestor:
            return self.id
        else:
            return self.get_address()

    def get_outputs(self):
        return self.outputs[:]

    async def send_payment_and_receive_paymentack--- This code section failed: ---

 L. 275         0  LOAD_FAST                'self'
                2  LOAD_ATTR                details
                4  STORE_FAST               'pay_det'

 L. 276         6  LOAD_FAST                'self'
                8  LOAD_ATTR                details
               10  LOAD_ATTR                payment_url
               12  POP_JUMP_IF_TRUE     18  'to 18'

 L. 277        14  LOAD_CONST               (False, 'no url')
               16  RETURN_END_IF    
             18_0  COME_FROM            12  '12'

 L. 278        18  LOAD_GLOBAL              pb2
               20  LOAD_ATTR                Payment
               22  CALL_FUNCTION_0       0  '0 positional arguments'
               24  STORE_FAST               'paymnt'

 L. 279        26  LOAD_FAST                'pay_det'
               28  LOAD_ATTR                merchant_data
               30  LOAD_FAST                'paymnt'
               32  STORE_ATTR               merchant_data

 L. 280        34  LOAD_FAST                'paymnt'
               36  LOAD_ATTR                transactions
               38  LOAD_ATTR                append
               40  LOAD_GLOBAL              bfh
               42  LOAD_FAST                'raw_tx'
               44  CALL_FUNCTION_1       1  '1 positional argument'
               46  CALL_FUNCTION_1       1  '1 positional argument'
               48  POP_TOP          

 L. 281        50  LOAD_FAST                'paymnt'
               52  LOAD_ATTR                refund_to
               54  LOAD_ATTR                add
               56  CALL_FUNCTION_0       0  '0 positional arguments'
               58  STORE_FAST               'ref_out'

 L. 282        60  LOAD_GLOBAL              util
               62  LOAD_ATTR                bfh
               64  LOAD_GLOBAL              transaction
               66  LOAD_ATTR                Transaction
               68  LOAD_ATTR                pay_script
               70  LOAD_GLOBAL              TYPE_ADDRESS
               72  LOAD_FAST                'refund_addr'
               74  CALL_FUNCTION_2       2  '2 positional arguments'
               76  CALL_FUNCTION_1       1  '1 positional argument'
               78  LOAD_FAST                'ref_out'
               80  STORE_ATTR               script

 L. 283        82  LOAD_STR                 'Paid using Electrum'
               84  LOAD_FAST                'paymnt'
               86  STORE_ATTR               memo

 L. 284        88  LOAD_FAST                'paymnt'
               90  LOAD_ATTR                SerializeToString
               92  CALL_FUNCTION_0       0  '0 positional arguments'
               94  STORE_FAST               'pm'

 L. 285        96  LOAD_GLOBAL              urllib
               98  LOAD_ATTR                parse
              100  LOAD_ATTR                urlparse
              102  LOAD_FAST                'pay_det'
              104  LOAD_ATTR                payment_url
              106  CALL_FUNCTION_1       1  '1 positional argument'
              108  STORE_FAST               'payurl'

 L. 286       110  LOAD_CONST               None
              112  STORE_FAST               'resp_content'

 L. 287       114  SETUP_EXCEPT        300  'to 300'

 L. 288       116  LOAD_GLOBAL              Network
              118  LOAD_ATTR                get_instance
              120  CALL_FUNCTION_0       0  '0 positional arguments'
              122  LOAD_ATTR                proxy
              124  STORE_FAST               'proxy'

 L. 289       126  LOAD_GLOBAL              make_aiohttp_session
              128  LOAD_FAST                'proxy'
              130  LOAD_GLOBAL              ACK_HEADERS
              132  LOAD_CONST               ('headers',)
              134  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              136  BEFORE_ASYNC_WITH
              138  GET_AWAITABLE    
              140  LOAD_CONST               None
              142  YIELD_FROM       
              144  SETUP_ASYNC_WITH    284  'to 284'
              146  STORE_FAST               'session'

 L. 290       148  LOAD_FAST                'session'
              150  LOAD_ATTR                post
              152  LOAD_FAST                'payurl'
              154  LOAD_ATTR                geturl
              156  CALL_FUNCTION_0       0  '0 positional arguments'
              158  LOAD_FAST                'pm'
              160  LOAD_CONST               ('data',)
              162  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              164  BEFORE_ASYNC_WITH
              166  GET_AWAITABLE    
              168  LOAD_CONST               None
              170  YIELD_FROM       
              172  SETUP_ASYNC_WITH    268  'to 268'
              174  STORE_FAST               'response'

 L. 291       176  LOAD_FAST                'response'
              178  LOAD_ATTR                read
              180  CALL_FUNCTION_0       0  '0 positional arguments'
              182  GET_AWAITABLE    
              184  LOAD_CONST               None
              186  YIELD_FROM       
              188  STORE_FAST               'resp_content'

 L. 292       190  LOAD_FAST                'response'
              192  LOAD_ATTR                raise_for_status
              194  CALL_FUNCTION_0       0  '0 positional arguments'
              196  POP_TOP          

 L. 293       198  SETUP_EXCEPT        222  'to 222'

 L. 294       200  LOAD_GLOBAL              pb2
              202  LOAD_ATTR                PaymentACK
              204  CALL_FUNCTION_0       0  '0 positional arguments'
              206  STORE_FAST               'paymntack'

 L. 295       208  LOAD_FAST                'paymntack'
              210  LOAD_ATTR                ParseFromString
              212  LOAD_FAST                'resp_content'
              214  CALL_FUNCTION_1       1  '1 positional argument'
              216  POP_TOP          
              218  POP_BLOCK        
              220  JUMP_FORWARD        242  'to 242'
            222_0  COME_FROM_EXCEPT    198  '198'

 L. 296       222  DUP_TOP          
              224  LOAD_GLOBAL              Exception
              226  COMPARE_OP               exception-match
              228  POP_JUMP_IF_FALSE   240  'to 240'
              230  POP_TOP          
              232  POP_TOP          
              234  POP_TOP          

 L. 297       236  LOAD_CONST               (False, 'PaymentACK could not be processed. Payment was sent; please manually verify that payment was received.')
              238  RETURN_VALUE     
            240_0  COME_FROM           228  '228'
              240  END_FINALLY      
            242_0  COME_FROM           220  '220'

 L. 298       242  LOAD_GLOBAL              print
              244  LOAD_STR                 'PaymentACK message received: '
              246  LOAD_FAST                'paymntack'
              248  LOAD_ATTR                memo
              250  FORMAT_VALUE          0  ''
              252  BUILD_STRING_2        2 
              254  CALL_FUNCTION_1       1  '1 positional argument'
              256  POP_TOP          

 L. 299       258  LOAD_CONST               True
              260  LOAD_FAST                'paymntack'
              262  LOAD_ATTR                memo
              264  BUILD_TUPLE_2         2 
              266  RETURN_VALUE     
            268_0  COME_FROM_ASYNC_WITH   172  '172'
              268  WITH_CLEANUP_START
              270  GET_AWAITABLE    
              272  LOAD_CONST               None
              274  YIELD_FROM       
              276  WITH_CLEANUP_FINISH
              278  END_FINALLY      
              280  POP_BLOCK        
              282  LOAD_CONST               None
            284_0  COME_FROM_ASYNC_WITH   144  '144'
              284  WITH_CLEANUP_START
              286  GET_AWAITABLE    
              288  LOAD_CONST               None
              290  YIELD_FROM       
              292  WITH_CLEANUP_FINISH
              294  END_FINALLY      
              296  POP_BLOCK        
              298  JUMP_FORWARD        404  'to 404'
            300_0  COME_FROM_EXCEPT    114  '114'

 L. 300       300  DUP_TOP          
              302  LOAD_GLOBAL              aiohttp
              304  LOAD_ATTR                ClientError
              306  COMPARE_OP               exception-match
              308  POP_JUMP_IF_FALSE   402  'to 402'
              312  POP_TOP          
              314  STORE_FAST               'e'
              316  POP_TOP          
              318  SETUP_FINALLY       392  'to 392'

 L. 301       320  LOAD_STR                 'Payment Message/PaymentACK Failed:\n'
              322  LOAD_GLOBAL              repr
              324  LOAD_FAST                'e'
              326  CALL_FUNCTION_1       1  '1 positional argument'
              328  FORMAT_VALUE          0  ''
              330  BUILD_STRING_2        2 
              332  STORE_FAST               'error'

 L. 302       334  LOAD_GLOBAL              isinstance
              336  LOAD_FAST                'e'
              338  LOAD_GLOBAL              aiohttp
              340  LOAD_ATTR                ClientResponseError
              342  CALL_FUNCTION_2       2  '2 positional arguments'
              344  POP_JUMP_IF_FALSE   384  'to 384'
              348  LOAD_FAST                'e'
              350  LOAD_ATTR                status
              352  LOAD_CONST               400
              354  COMPARE_OP               ==
              356  POP_JUMP_IF_FALSE   384  'to 384'
              360  LOAD_FAST                'resp_content'
              362  POP_JUMP_IF_FALSE   384  'to 384'

 L. 303       366  LOAD_FAST                'error'
              368  LOAD_STR                 '\n'
              370  LOAD_FAST                'resp_content'
              372  LOAD_ATTR                decode
              374  LOAD_STR                 'utf8'
              376  CALL_FUNCTION_1       1  '1 positional argument'
              378  BINARY_ADD       
              380  INPLACE_ADD      
              382  STORE_FAST               'error'
            384_0  COME_FROM           362  '362'
            384_1  COME_FROM           356  '356'
            384_2  COME_FROM           344  '344'

 L. 304       384  LOAD_CONST               False
              386  LOAD_FAST                'error'
              388  BUILD_TUPLE_2         2 
              390  RETURN_VALUE     
            392_0  COME_FROM_FINALLY   318  '318'
              392  LOAD_CONST               None
              394  STORE_FAST               'e'
              396  DELETE_FAST              'e'
              398  END_FINALLY      
              400  JUMP_FORWARD        404  'to 404'
              402  END_FINALLY      
            404_0  COME_FROM           400  '400'
            404_1  COME_FROM           298  '298'

Parse error at or near `JUMP_FORWARD' instruction at offset 298


def make_unsigned_request(req):
    from .transaction import Transaction
    addr = req['address']
    time = req.get('time', 0)
    exp = req.get('exp', 0)
    if time:
        if type(time) != int:
            time = 0
    if exp:
        if type(exp) != int:
            exp = 0
    amount = req['amount']
    if amount is None:
        amount = 0
    memo = req['memo']
    script = bfh(Transaction.pay_script(TYPE_ADDRESS, addr))
    outputs = [(script, amount)]
    pd = pb2.PaymentDetails()
    for script, amount in outputs:
        pd.outputs.add(amount=amount, script=script)

    pd.time = time
    pd.expires = time + exp if exp else 0
    pd.memo = memo
    pr = pb2.PaymentRequest()
    pr.serialized_payment_details = pd.SerializeToString()
    pr.signature = util.to_bytes('')
    return pr


def sign_request_with_alias(pr, alias, alias_privkey):
    pr.pki_type = 'dnssec+btc'
    pr.pki_data = str(alias)
    message = pr.SerializeToString()
    ec_key = ecc.ECPrivkey(alias_privkey)
    compressed = bitcoin.is_compressed_privkey(alias_privkey)
    pr.signature = ec_key.sign_message(message, compressed)


def verify_cert_chain(chain):
    """ Verify a chain of certificates. The last certificate is the CA"""
    load_ca_list()
    cert_num = len(chain)
    x509_chain = []
    for i in range(cert_num):
        x = x509.X509(bytearray(chain[i]))
        x509_chain.append(x)
        if i == 0:
            x.check_date()
        else:
            if not x.check_ca():
                raise Exception('ERROR: Supplied CA Certificate Error')

    if not cert_num > 1:
        raise Exception('ERROR: CA Certificate Chain Not Provided by Payment Processor')
    ca = x509_chain[(cert_num - 1)]
    if ca.getFingerprint() not in ca_list:
        keyID = ca.get_issuer_keyID()
        f = ca_keyID.get(keyID)
        if f:
            root = ca_list[f]
            x509_chain.append(root)
        else:
            raise Exception('Supplied CA Not Found in Trusted CA Store.')
    cert_num = len(x509_chain)
    for i in range(1, cert_num):
        x = x509_chain[i]
        prev_x = x509_chain[(i - 1)]
        algo, sig, data = prev_x.get_signature()
        sig = bytearray(sig)
        pubkey = rsakey.RSAKey(x.modulus, x.exponent)
        if algo == x509.ALGO_RSA_SHA1:
            verify = pubkey.hashAndVerify(sig, data)
        else:
            if algo == x509.ALGO_RSA_SHA256:
                hashBytes = bytearray(hashlib.sha256(data).digest())
                verify = pubkey.verify(sig, x509.PREFIX_RSA_SHA256 + hashBytes)
            else:
                if algo == x509.ALGO_RSA_SHA384:
                    hashBytes = bytearray(hashlib.sha384(data).digest())
                    verify = pubkey.verify(sig, x509.PREFIX_RSA_SHA384 + hashBytes)
                else:
                    if algo == x509.ALGO_RSA_SHA512:
                        hashBytes = bytearray(hashlib.sha512(data).digest())
                        verify = pubkey.verify(sig, x509.PREFIX_RSA_SHA512 + hashBytes)
                    else:
                        raise Exception('Algorithm not supported: {}'.format(algo))
        if not verify:
            raise Exception('Certificate not Signed by Provided CA Certificate Chain')

    return (
     x509_chain[0], ca)


def check_ssl_config(config):
    from . import pem
    key_path = config.get('ssl_privkey')
    cert_path = config.get('ssl_chain')
    with open(key_path, 'r', encoding='utf-8') as (f):
        params = pem.parse_private_key(f.read())
    with open(cert_path, 'r', encoding='utf-8') as (f):
        s = f.read()
    bList = pem.dePemList(s, 'CERTIFICATE')
    x, ca = verify_cert_chain(bList)
    privkey = (rsakey.RSAKey)(*params)
    pubkey = rsakey.RSAKey(x.modulus, x.exponent)
    if not x.modulus == params[0]:
        raise AssertionError
    elif not x.exponent == params[1]:
        raise AssertionError
    requestor = x.get_common_name()
    if requestor.startswith('*.'):
        requestor = requestor[2:]
    return requestor


def sign_request_with_x509(pr, key_path, cert_path):
    from . import pem
    with open(key_path, 'r', encoding='utf-8') as (f):
        params = pem.parse_private_key(f.read())
        privkey = (rsakey.RSAKey)(*params)
    with open(cert_path, 'r', encoding='utf-8') as (f):
        s = f.read()
        bList = pem.dePemList(s, 'CERTIFICATE')
    certificates = pb2.X509Certificates()
    certificates.certificate.extend(map(bytes, bList))
    pr.pki_type = 'x509+sha256'
    pr.pki_data = certificates.SerializeToString()
    msgBytes = bytearray(pr.SerializeToString())
    hashBytes = bytearray(hashlib.sha256(msgBytes).digest())
    sig = privkey.sign(x509.PREFIX_RSA_SHA256 + hashBytes)
    pr.signature = bytes(sig)


def serialize_request(req):
    pr = make_unsigned_request(req)
    signature = req.get('sig')
    requestor = req.get('name')
    if requestor:
        if signature:
            pr.signature = bfh(signature)
            pr.pki_type = 'dnssec+btc'
            pr.pki_data = str(requestor)
    return pr


def make_request(config, req):
    pr = make_unsigned_request(req)
    key_path = config.get('ssl_privkey')
    cert_path = config.get('ssl_chain')
    if key_path:
        if cert_path:
            sign_request_with_x509(pr, key_path, cert_path)
    return pr


class InvoiceStore(object):

    def __init__(self, storage):
        self.storage = storage
        self.invoices = {}
        self.paid = {}
        d = self.storage.get('invoices', {})
        self.load(d)

    def set_paid(self, pr, txid):
        pr.tx = txid
        pr_id = pr.get_id()
        self.paid[txid] = pr_id
        if pr_id not in self.invoices:
            self.add(pr)

    def load(self, d):
        for k, v in d.items():
            try:
                pr = PaymentRequest(bfh(v.get('hex')))
                pr.tx = v.get('txid')
                pr.requestor = v.get('requestor')
                self.invoices[k] = pr
                if pr.tx:
                    self.paid[pr.tx] = k
            except:
                continue

    def import_file(self, path):

        def validate(data):
            return data

        import_meta(path, validate, self.on_import)

    def on_import(self, data):
        self.load(data)
        self.save()

    def export_file(self, filename):
        export_meta(self.dump(), filename)

    def dump(self):
        d = {}
        for k, pr in self.invoices.items():
            d[k] = {'hex':bh2u(pr.raw), 
             'requestor':pr.requestor, 
             'txid':pr.tx}

        return d

    def save(self):
        self.storage.put('invoices', self.dump())

    def get_status(self, key):
        pr = self.get(key)
        if pr is None:
            print_error("[InvoiceStore] get_status() can't find pr for", key)
            return
        if pr.tx is not None:
            return PR_PAID
        else:
            if pr.has_expired():
                return PR_EXPIRED
            return PR_UNPAID

    def add(self, pr):
        key = pr.get_id()
        self.invoices[key] = pr
        self.save()
        return key

    def remove(self, key):
        self.invoices.pop(key)
        self.save()

    def get(self, k):
        return self.invoices.get(k)

    def sorted_list(self):
        return self.invoices.values()

    def unpaid_invoices(self):
        return [self.invoices[k] for k in filter(lambda x: self.get_status(x) != PR_PAID, self.invoices.keys())]