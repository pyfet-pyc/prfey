# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: hashlib.py
r"""hashlib module - A common interface to many hash functions.

new(name, data=b'', **kwargs) - returns a new hash object implementing the
                                given hash function; initializing the hash
                                using the given binary data.

Named constructor functions are also available, these are faster
than using new(name):

md5(), sha1(), sha224(), sha256(), sha384(), sha512(), blake2b(), blake2s(),
sha3_224, sha3_256, sha3_384, sha3_512, shake_128, and shake_256.

More algorithms may be available on your platform but the above are guaranteed
to exist.  See the algorithms_guaranteed and algorithms_available attributes
to find out what algorithm names can be passed to new().

NOTE: If you want the adler32 or crc32 hash functions they are available in
the zlib module.

Choose your hash function wisely.  Some have known collision weaknesses.
sha384 and sha512 will be slow on 32 bit platforms.

Hash objects have these methods:
 - update(data): Update the hash object with the bytes in data. Repeated calls
                 are equivalent to a single call with the concatenation of all
                 the arguments.
 - digest():     Return the digest of the bytes passed to the update() method
                 so far as a bytes object.
 - hexdigest():  Like digest() except the digest is returned as a string
                 of double length, containing only hexadecimal digits.
 - copy():       Return a copy (clone) of the hash object. This can be used to
                 efficiently compute the digests of datas that share a common
                 initial substring.

For example, to obtain the digest of the byte string 'Nobody inspects the
spammish repetition':

    >>> import hashlib
    >>> m = hashlib.md5()
    >>> m.update(b"Nobody inspects")
    >>> m.update(b" the spammish repetition")
    >>> m.digest()
    b'\xbbd\x9c\x83\xdd\x1e\xa5\xc9\xd9\xde\xc9\xa1\x8d\xf0\xff\xe9'

More condensed:

    >>> hashlib.sha224(b"Nobody inspects the spammish repetition").hexdigest()
    'a4337bc45a8fc544c03f52dc550cd6e1e87021bc896588bd79e901e2'

"""
__always_supported = ('md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'blake2b',
                      'blake2s', 'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512',
                      'shake_128', 'shake_256')
algorithms_guaranteed = set(__always_supported)
algorithms_available = set(__always_supported)
__all__ = __always_supported + ('new', 'algorithms_guaranteed', 'algorithms_available',
                                'pbkdf2_hmac')
__builtin_constructor_cache = {}
__block_openssl_constructor = {
 'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512',
 'shake_128', 'shake_256',
 'blake2b', 'blake2s'}

def __get_builtin_constructor(name):
    cache = __builtin_constructor_cache
    constructor = cache.get(name)
    if constructor is not None:
        return constructor
    try:
        if name in {'SHA1', 'sha1'}:
            import _sha1
            cache['SHA1'] = cache['sha1'] = _sha1.sha1
        else:
            if name in {'md5', 'MD5'}:
                import _md5
                cache['MD5'] = cache['md5'] = _md5.md5
            else:
                if name in {'sha224', 'sha256', 'SHA224', 'SHA256'}:
                    import _sha256
                    cache['SHA224'] = cache['sha224'] = _sha256.sha224
                    cache['SHA256'] = cache['sha256'] = _sha256.sha256
                else:
                    if name in {'sha512', 'SHA512', 'SHA384', 'sha384'}:
                        import _sha512
                        cache['SHA384'] = cache['sha384'] = _sha512.sha384
                        cache['SHA512'] = cache['sha512'] = _sha512.sha512
                    else:
                        if name in {'blake2b', 'blake2s'}:
                            import _blake2
                            cache['blake2b'] = _blake2.blake2b
                            cache['blake2s'] = _blake2.blake2s
                        else:
                            if name in {'sha3_512', 'sha3_256', 'sha3_384', 'sha3_224'}:
                                import _sha3
                                cache['sha3_224'] = _sha3.sha3_224
                                cache['sha3_256'] = _sha3.sha3_256
                                cache['sha3_384'] = _sha3.sha3_384
                                cache['sha3_512'] = _sha3.sha3_512
                            else:
                                if name in {'shake_128', 'shake_256'}:
                                    import _sha3
                                    cache['shake_128'] = _sha3.shake_128
                                    cache['shake_256'] = _sha3.shake_256
    except ImportError:
        pass
    else:
        constructor = cache.get(name)
        if constructor is not None:
            return constructor
        raise ValueError('unsupported hash type ' + name)


def __get_openssl_constructor--- This code section failed: ---

 L. 124         0  LOAD_FAST                'name'
                2  LOAD_GLOBAL              __block_openssl_constructor
                4  COMPARE_OP               in
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L. 126         8  LOAD_GLOBAL              __get_builtin_constructor
               10  LOAD_FAST                'name'
               12  CALL_FUNCTION_1       1  ''
               14  RETURN_VALUE     
             16_0  COME_FROM             6  '6'

 L. 127        16  SETUP_FINALLY        44  'to 44'

 L. 128        18  LOAD_GLOBAL              getattr
               20  LOAD_GLOBAL              _hashlib
               22  LOAD_STR                 'openssl_'
               24  LOAD_FAST                'name'
               26  BINARY_ADD       
               28  CALL_FUNCTION_2       2  ''
               30  STORE_FAST               'f'

 L. 131        32  LOAD_FAST                'f'
               34  CALL_FUNCTION_0       0  ''
               36  POP_TOP          

 L. 133        38  LOAD_FAST                'f'
               40  POP_BLOCK        
               42  RETURN_VALUE     
             44_0  COME_FROM_FINALLY    16  '16'

 L. 134        44  DUP_TOP          
               46  LOAD_GLOBAL              AttributeError
               48  LOAD_GLOBAL              ValueError
               50  BUILD_TUPLE_2         2 
               52  COMPARE_OP               exception-match
               54  POP_JUMP_IF_FALSE    74  'to 74'
               56  POP_TOP          
               58  POP_TOP          
               60  POP_TOP          

 L. 135        62  LOAD_GLOBAL              __get_builtin_constructor
               64  LOAD_FAST                'name'
               66  CALL_FUNCTION_1       1  ''
               68  ROT_FOUR         
               70  POP_EXCEPT       
               72  RETURN_VALUE     
             74_0  COME_FROM            54  '54'
               74  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 58


def __py_new(name, data=b'', **kwargs):
    """new(name, data=b'', **kwargs) - Return a new hashing object using the
    named algorithm; optionally initialized with data (which must be
    a bytes-like object).
    """
    return (__get_builtin_constructor(name))(data, **kwargs)


def __hash_new--- This code section failed: ---

 L. 150         0  LOAD_FAST                'name'
                2  LOAD_GLOBAL              __block_openssl_constructor
                4  COMPARE_OP               in
                6  POP_JUMP_IF_FALSE    24  'to 24'

 L. 155         8  LOAD_GLOBAL              __get_builtin_constructor
               10  LOAD_FAST                'name'
               12  CALL_FUNCTION_1       1  ''
               14  LOAD_FAST                'data'
               16  BUILD_TUPLE_1         1 
               18  LOAD_FAST                'kwargs'
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
             24_0  COME_FROM             6  '6'

 L. 156        24  SETUP_FINALLY        40  'to 40'

 L. 157        26  LOAD_GLOBAL              _hashlib
               28  LOAD_METHOD              new
               30  LOAD_FAST                'name'
               32  LOAD_FAST                'data'
               34  CALL_METHOD_2         2  ''
               36  POP_BLOCK        
               38  RETURN_VALUE     
             40_0  COME_FROM_FINALLY    24  '24'

 L. 158        40  DUP_TOP          
               42  LOAD_GLOBAL              ValueError
               44  COMPARE_OP               exception-match
               46  POP_JUMP_IF_FALSE    70  'to 70'
               48  POP_TOP          
               50  POP_TOP          
               52  POP_TOP          

 L. 163        54  LOAD_GLOBAL              __get_builtin_constructor
               56  LOAD_FAST                'name'
               58  CALL_FUNCTION_1       1  ''
               60  LOAD_FAST                'data'
               62  CALL_FUNCTION_1       1  ''
               64  ROT_FOUR         
               66  POP_EXCEPT       
               68  RETURN_VALUE     
             70_0  COME_FROM            46  '46'
               70  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 50


try:
    import _hashlib
    new = __hash_new
    __get_hash = __get_openssl_constructor
    algorithms_available = algorithms_available.union(_hashlib.openssl_md_meth_names)
except ImportError:
    new = __py_new
    __get_hash = __get_builtin_constructor

try:
    from _hashlib import pbkdf2_hmac
except ImportError:
    _trans_5C = bytes((x ^ 92 for x in range(256)))
    _trans_36 = bytes((x ^ 54 for x in range(256)))

    def pbkdf2_hmac(hash_name, password, salt, iterations, dklen=None):
        """Password based key derivation function 2 (PKCS #5 v2.0)

        This Python implementations based on the hmac module about as fast
        as OpenSSL's PKCS5_PBKDF2_HMAC for short passwords and much faster
        for long passwords.
        """
        if not isinstancehash_namestr:
            raise TypeError(hash_name)
        else:
            if not isinstancepassword(bytes, bytearray):
                password = bytes(memoryview(password))
            if not isinstancesalt(bytes, bytearray):
                salt = bytes(memoryview(salt))
            inner = new(hash_name)
            outer = new(hash_name)
            blocksize = getattr(inner, 'block_size', 64)
            if len(password) > blocksize:
                password = newhash_namepassword.digest()
            password = password + b'\x00' * (blocksize - len(password))
            inner.update(password.translate(_trans_36))
            outer.update(password.translate(_trans_5C))

            def prf(msg, inner=inner, outer=outer):
                icpy = inner.copy()
                ocpy = outer.copy()
                icpy.update(msg)
                ocpy.update(icpy.digest())
                return ocpy.digest()

            if iterations < 1:
                raise ValueError(iterations)
            if dklen is None:
                dklen = outer.digest_size
            if dklen < 1:
                raise ValueError(dklen)
            dkey = b''
            loop = 1
            from_bytes = int.from_bytes
            while True:
                if len(dkey) < dklen:
                    prev = prf(salt + loop.to_bytes(4, 'big'))
                    rkey = int.from_bytes(prev, 'big')
                    for i in range(iterations - 1):
                        prev = prf(prev)
                        rkey ^= from_bytesprev'big'
                    else:
                        loop += 1
                        dkey += rkey.to_bytes(inner.digest_size, 'big')

        return dkey[:dklen]


else:
    try:
        from _hashlib import scrypt
    except ImportError:
        pass
    else:
        for __func_name in __always_supported:
            try:
                globals()[__func_name] = __get_hash(__func_name)
            except ValueError:
                import logging
                logging.exception('code for hash %s was not found.', __func_name)

        else:
            del __always_supported
            del __func_name
            del __get_hash
            del __py_new
            del __hash_new
            del __get_openssl_constructor