# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\dns\rdata.py
"""DNS rdata."""
from io import BytesIO
import base64, binascii, dns.exception, dns.name, dns.rdataclass, dns.rdatatype, dns.tokenizer, dns.wiredata
from ._compat import xrange, string_types, text_type
try:
    import threading as _threading
except ImportError:
    import dummy_threading as _threading
else:
    _hex_chunksize = 32

    def _hexify(data, chunksize=_hex_chunksize):
        """Convert a binary string into its hex encoding, broken up into chunks
    of chunksize characters separated by a space.
    """
        line = binascii.hexlify(data)
        return (b' ').join([line[i:i + chunksize] for i in range(0, len(line), chunksize)]).decode()


    _base64_chunksize = 32

    def _base64ify(data, chunksize=_base64_chunksize):
        """Convert a binary string into its base64 encoding, broken up into chunks
    of chunksize characters separated by a space.
    """
        line = base64.b64encode(data)
        return (b' ').join([line[i:i + chunksize] for i in range(0, len(line), chunksize)]).decode()


    __escaped = bytearray(b'"\\')

    def _escapify(qstring):
        """Escape the characters in a quoted string which need it."""
        if isinstance(qstring, text_type):
            qstring = qstring.encode()
        if not isinstance(qstring, bytearray):
            qstring = bytearray(qstring)
        text = ''
        for c in qstring:
            if c in __escaped:
                text += '\\' + chr(c)
            elif c >= 32 and c < 127:
                text += chr(c)
            else:
                text += '\\%03d' % c
        else:
            return text


    def _truncate_bitmap(what):
        """Determine the index of greatest byte that isn't all zeros, and
    return the bitmap that contains all the bytes less than that index.
    """
        for i in xrange(len(what) - 1, -1, -1):
            if what[i] != 0:
                return what[0:i + 1]
            return what[0:1]


    class Rdata(object):
        __doc__ = 'Base class for all DNS rdata types.'
        __slots__ = [
         'rdclass', 'rdtype']

        def __init__(self, rdclass, rdtype):
            """Initialize an rdata.

        *rdclass*, an ``int`` is the rdataclass of the Rdata.
        *rdtype*, an ``int`` is the rdatatype of the Rdata.
        """
            self.rdclass = rdclass
            self.rdtype = rdtype

        def covers(self):
            """Return the type a Rdata covers.

        DNS SIG/RRSIG rdatas apply to a specific type; this type is
        returned by the covers() function.  If the rdata type is not
        SIG or RRSIG, dns.rdatatype.NONE is returned.  This is useful when
        creating rdatasets, allowing the rdataset to contain only RRSIGs
        of a particular type, e.g. RRSIG(NS).

        Returns an ``int``.
        """
            return dns.rdatatype.NONE

        def extended_rdatatype(self):
            """Return a 32-bit type value, the least significant 16 bits of
        which are the ordinary DNS type, and the upper 16 bits of which are
        the "covered" type, if any.

        Returns an ``int``.
        """
            return self.covers() << 16 | self.rdtype

        def to_text(self, origin=None, relativize=True, **kw):
            """Convert an rdata to text format.

        Returns a ``text``.
        """
            raise NotImplementedError

        def to_wire(self, file, compress=None, origin=None):
            """Convert an rdata to wire format.

        Returns a ``binary``.
        """
            raise NotImplementedError

        def to_digestable(self, origin=None):
            """Convert rdata to a format suitable for digesting in hashes.  This
        is also the DNSSEC canonical form.

        Returns a ``binary``.
        """
            f = BytesIO()
            self.to_wire(f, None, origin)
            return f.getvalue()

        def validate(self):
            """Check that the current contents of the rdata's fields are
        valid.

        If you change an rdata by assigning to its fields,
        it is a good idea to call validate() when you are done making
        changes.

        Raises various exceptions if there are problems.

        Returns ``None``.
        """
            dns.rdata.from_text(self.rdclass, self.rdtype, self.to_text())

        def __repr__(self):
            covers = self.covers()
            if covers == dns.rdatatype.NONE:
                ctext = ''
            else:
                ctext = '(' + dns.rdatatype.to_text(covers) + ')'
            return '<DNS ' + dns.rdataclass.to_text(self.rdclass) + ' ' + dns.rdatatype.to_text(self.rdtype) + ctext + ' rdata: ' + str(self) + '>'

        def __str__(self):
            return self.to_text()

        def _cmp(self, other):
            """Compare an rdata with another rdata of the same rdtype and
        rdclass.

        Return < 0 if self < other in the DNSSEC ordering, 0 if self
        == other, and > 0 if self > other.

        """
            our = self.to_digestable(dns.name.root)
            their = other.to_digestable(dns.name.root)
            if our == their:
                return 0
            if our > their:
                return 1
            return -1

        def __eq__(self, other):
            if not isinstance(other, Rdata):
                return False
            if self.rdclass != other.rdclass or self.rdtype != other.rdtype:
                return False
            return self._cmp(other) == 0

        def __ne__(self, other):
            if not isinstance(other, Rdata):
                return True
            if self.rdclass != other.rdclass or self.rdtype != other.rdtype:
                return True
            return self._cmp(other) != 0

        def __lt__(self, other):
            if not isinstance(other, Rdata) or self.rdclass != other.rdclass or self.rdtype != other.rdtype:
                return NotImplemented
            return self._cmp(other) < 0

        def __le__(self, other):
            if not isinstance(other, Rdata) or self.rdclass != other.rdclass or self.rdtype != other.rdtype:
                return NotImplemented
            return self._cmp(other) <= 0

        def __ge__(self, other):
            if not isinstance(other, Rdata) or self.rdclass != other.rdclass or self.rdtype != other.rdtype:
                return NotImplemented
            return self._cmp(other) >= 0

        def __gt__(self, other):
            if not isinstance(other, Rdata) or self.rdclass != other.rdclass or self.rdtype != other.rdtype:
                return NotImplemented
            return self._cmp(other) > 0

        def __hash__(self):
            return hash(self.to_digestable(dns.name.root))

        @classmethod
        def from_text(cls, rdclass, rdtype, tok, origin=None, relativize=True):
            raise NotImplementedError

        @classmethod
        def from_wire(cls, rdclass, rdtype, wire, current, rdlen, origin=None):
            raise NotImplementedError

        def choose_relativity(self, origin=None, relativize=True):
            """Convert any domain names in the rdata to the specified
        relativization.
        """
            pass


    class GenericRdata(Rdata):
        __doc__ = 'Generic Rdata Class\n\n    This class is used for rdata types for which we have no better\n    implementation.  It implements the DNS "unknown RRs" scheme.\n    '
        __slots__ = [
         'data']

        def __init__(self, rdclass, rdtype, data):
            super(GenericRdata, self).__init__(rdclass, rdtype)
            self.data = data

        def to_text(self, origin=None, relativize=True, **kw):
            return '\\# %d ' % len(self.data) + _hexify(self.data)

        @classmethod
        def from_text(cls, rdclass, rdtype, tok, origin=None, relativize=True):
            token = tok.get()
            if not token.is_identifier() or token.value != '\\#':
                raise dns.exception.SyntaxError('generic rdata does not start with \\#')
            length = tok.get_int()
            chunks = []
            while True:
                token = tok.get()
                if token.is_eol_or_eof():
                    break
                chunks.append(token.value.encode())

            hex = (b'').join(chunks)
            data = binascii.unhexlify(hex)
            if len(data) != length:
                raise dns.exception.SyntaxError('generic rdata hex data has wrong length')
            return cls(rdclass, rdtype, data)

        def to_wire(self, file, compress=None, origin=None):
            file.write(self.data)

        @classmethod
        def from_wire(cls, rdclass, rdtype, wire, current, rdlen, origin=None):
            return cls(rdclass, rdtype, wire[current:current + rdlen])


    _rdata_modules = {}
    _module_prefix = 'dns.rdtypes'
    _import_lock = _threading.Lock()

    def get_rdata_class(rdclass, rdtype):

        def import_module--- This code section failed: ---

 L. 312         0  LOAD_GLOBAL              _import_lock
                2  SETUP_WITH           68  'to 68'
                4  POP_TOP          

 L. 313         6  LOAD_GLOBAL              __import__
                8  LOAD_FAST                'name'
               10  CALL_FUNCTION_1       1  ''
               12  STORE_FAST               'mod'

 L. 314        14  LOAD_FAST                'name'
               16  LOAD_METHOD              split
               18  LOAD_STR                 '.'
               20  CALL_METHOD_1         1  ''
               22  STORE_FAST               'components'

 L. 315        24  LOAD_FAST                'components'
               26  LOAD_CONST               1
               28  LOAD_CONST               None
               30  BUILD_SLICE_2         2 
               32  BINARY_SUBSCR    
               34  GET_ITER         
               36  FOR_ITER             52  'to 52'
               38  STORE_FAST               'comp'

 L. 316        40  LOAD_GLOBAL              getattr
               42  LOAD_FAST                'mod'
               44  LOAD_FAST                'comp'
               46  CALL_FUNCTION_2       2  ''
               48  STORE_FAST               'mod'
               50  JUMP_BACK            36  'to 36'

 L. 317        52  LOAD_FAST                'mod'
               54  POP_BLOCK        
               56  ROT_TWO          
               58  BEGIN_FINALLY    
               60  WITH_CLEANUP_START
               62  WITH_CLEANUP_FINISH
               64  POP_FINALLY           0  ''
               66  RETURN_VALUE     
             68_0  COME_FROM_WITH        2  '2'
               68  WITH_CLEANUP_START
               70  WITH_CLEANUP_FINISH
               72  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 56

        mod = _rdata_modules.get((rdclass, rdtype))
        rdclass_text = dns.rdataclass.to_text(rdclass)
        rdtype_text = dns.rdatatype.to_text(rdtype)
        rdtype_text = rdtype_text.replace('-', '_')
        if not mod:
            mod = _rdata_modules.get((dns.rdatatype.ANY, rdtype))
            if not mod:
                try:
                    mod = import_module('.'.join([_module_prefix,
                     rdclass_text, rdtype_text]))
                    _rdata_modules[(rdclass, rdtype)] = mod
                except ImportError:
                    try:
                        mod = import_module('.'.join([_module_prefix,
                         'ANY', rdtype_text]))
                        _rdata_modules[(dns.rdataclass.ANY, rdtype)] = mod
                    except ImportError:
                        mod = None

        elif mod:
            cls = getattr(mod, rdtype_text)
        else:
            cls = GenericRdata
        return cls


    def from_text(rdclass, rdtype, tok, origin=None, relativize=True):
        """Build an rdata object from text format.

    This function attempts to dynamically load a class which
    implements the specified rdata class and type.  If there is no
    class-and-type-specific implementation, the GenericRdata class
    is used.

    Once a class is chosen, its from_text() class method is called
    with the parameters to this function.

    If *tok* is a ``text``, then a tokenizer is created and the string
    is used as its input.

    *rdclass*, an ``int``, the rdataclass.

    *rdtype*, an ``int``, the rdatatype.

    *tok*, a ``dns.tokenizer.Tokenizer`` or a ``text``.

    *origin*, a ``dns.name.Name`` (or ``None``), the
    origin to use for relative names.

    *relativize*, a ``bool``.  If true, name will be relativized to
    the specified origin.

    Returns an instance of the chosen Rdata subclass.
    """
        if isinstance(tok, string_types):
            tok = dns.tokenizer.Tokenizer(tok)
        cls = get_rdata_class(rdclass, rdtype)
        if cls != GenericRdata:
            token = tok.get()
            tok.unget(token)
            if token.is_identifier():
                if token.value == '\\#':
                    rdata = GenericRdata.from_text(rdclass, rdtype, tok, origin, relativize)
                    return from_wire(rdclass, rdtype, rdata.data, 0, len(rdata.data), origin)
        return cls.from_text(rdclass, rdtype, tok, origin, relativize)


    def from_wire(rdclass, rdtype, wire, current, rdlen, origin=None):
        """Build an rdata object from wire format

    This function attempts to dynamically load a class which
    implements the specified rdata class and type.  If there is no
    class-and-type-specific implementation, the GenericRdata class
    is used.

    Once a class is chosen, its from_wire() class method is called
    with the parameters to this function.

    *rdclass*, an ``int``, the rdataclass.

    *rdtype*, an ``int``, the rdatatype.

    *wire*, a ``binary``, the wire-format message.

    *current*, an ``int``, the offset in wire of the beginning of
    the rdata.

    *rdlen*, an ``int``, the length of the wire-format rdata

    *origin*, a ``dns.name.Name`` (or ``None``).  If not ``None``,
    then names will be relativized to this origin.

    Returns an instance of the chosen Rdata subclass.
    """
        wire = dns.wiredata.maybe_wrap(wire)
        cls = get_rdata_class(rdclass, rdtype)
        return cls.from_wire(rdclass, rdtype, wire, current, rdlen, origin)


    class RdatatypeExists(dns.exception.DNSException):
        __doc__ = 'DNS rdatatype already exists.'
        supp_kwargs = {'rdclass', 'rdtype'}
        fmt = 'The rdata type with class {rdclass} and rdtype {rdtype} already exists.'


    def register_type(implementation, rdtype, rdtype_text, is_singleton=False, rdclass=dns.rdataclass.IN):
        """Dynamically register a module to handle an rdatatype.

    *implementation*, a module implementing the type in the usual dnspython
    way.

    *rdtype*, an ``int``, the rdatatype to register.

    *rdtype_text*, a ``text``, the textual form of the rdatatype.

    *is_singleton*, a ``bool``, indicating if the type is a singleton (i.e.
    RRsets of the type can have only one member.)

    *rdclass*, the rdataclass of the type, or ``dns.rdataclass.ANY`` if
    it applies to all classes.
    """
        existing_cls = get_rdata_class(rdclass, rdtype)
        if existing_cls != GenericRdata:
            raise RdatatypeExists(rdclass=rdclass, rdtype=rdtype)
        _rdata_modules[(rdclass, rdtype)] = implementation
        dns.rdatatype.register_type(rdtype, rdtype_text, is_singleton)