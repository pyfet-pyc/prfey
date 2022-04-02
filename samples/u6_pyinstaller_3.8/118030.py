# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\dns\name.py
"""DNS Names.
"""
from io import BytesIO
import struct, sys, copy, encodings.idna
try:
    import idna
    have_idna_2008 = True
except ImportError:
    have_idna_2008 = False
else:
    import dns.exception, dns.wiredata
    from ._compat import long, binary_type, text_type, unichr, maybe_decode
    try:
        maxint = sys.maxint
    except AttributeError:
        maxint = (1 << 8 * struct.calcsize('P')) // 2 - 1
    else:
        NAMERELN_NONE = 0
        NAMERELN_SUPERDOMAIN = 1
        NAMERELN_SUBDOMAIN = 2
        NAMERELN_EQUAL = 3
        NAMERELN_COMMONANCESTOR = 4

        class EmptyLabel(dns.exception.SyntaxError):
            __doc__ = 'A DNS label is empty.'


        class BadEscape(dns.exception.SyntaxError):
            __doc__ = 'An escaped code in a text format of DNS name is invalid.'


        class BadPointer(dns.exception.FormError):
            __doc__ = 'A DNS compression pointer points forward instead of backward.'


        class BadLabelType(dns.exception.FormError):
            __doc__ = 'The label type in DNS name wire format is unknown.'


        class NeedAbsoluteNameOrOrigin(dns.exception.DNSException):
            __doc__ = 'An attempt was made to convert a non-absolute name to\n    wire when there was also a non-absolute (or missing) origin.'


        class NameTooLong(dns.exception.FormError):
            __doc__ = 'A DNS name is > 255 octets long.'


        class LabelTooLong(dns.exception.SyntaxError):
            __doc__ = 'A DNS label is > 63 octets long.'


        class AbsoluteConcatenation(dns.exception.DNSException):
            __doc__ = 'An attempt was made to append anything other than the\n    empty name to an absolute DNS name.'


        class NoParent(dns.exception.DNSException):
            __doc__ = 'An attempt was made to get the parent of the root name\n    or the empty name.'


        class NoIDNA2008(dns.exception.DNSException):
            __doc__ = 'IDNA 2008 processing was requested but the idna module is not\n    available.'


        class IDNAException(dns.exception.DNSException):
            __doc__ = 'IDNA processing raised an exception.'
            supp_kwargs = {
             'idna_exception'}
            fmt = 'IDNA processing exception: {idna_exception}'


        class IDNACodec(object):
            __doc__ = 'Abstract base class for IDNA encoder/decoders.'

            def __init__(self):
                pass

            def encode(self, label):
                raise NotImplementedError

            def decode(self, label):
                downcased = label.lower()
                if downcased.startswith(b'xn--'):
                    try:
                        label = downcased[4:].decode('punycode')
                    except Exception as e:
                        try:
                            raise IDNAException(idna_exception=e)
                        finally:
                            e = None
                            del e

                else:
                    label = maybe_decode(label)
                return _escapify(label, True)


        class IDNA2003Codec(IDNACodec):
            __doc__ = 'IDNA 2003 encoder/decoder.'

            def __init__(self, strict_decode=False):
                """Initialize the IDNA 2003 encoder/decoder.

        *strict_decode* is a ``bool``. If `True`, then IDNA2003 checking
        is done when decoding.  This can cause failures if the name
        was encoded with IDNA2008.  The default is `False`.
        """
                super(IDNA2003Codec, self).__init__()
                self.strict_decode = strict_decode

            def encode--- This code section failed: ---

 L. 146         0  LOAD_FAST                'label'
                2  LOAD_STR                 ''
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 147         8  LOAD_CONST               b''
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L. 148        12  SETUP_FINALLY        28  'to 28'

 L. 149        14  LOAD_GLOBAL              encodings
               16  LOAD_ATTR                idna
               18  LOAD_METHOD              ToASCII
               20  LOAD_FAST                'label'
               22  CALL_METHOD_1         1  ''
               24  POP_BLOCK        
               26  RETURN_VALUE     
             28_0  COME_FROM_FINALLY    12  '12'

 L. 150        28  DUP_TOP          
               30  LOAD_GLOBAL              UnicodeError
               32  COMPARE_OP               exception-match
               34  POP_JUMP_IF_FALSE    50  'to 50'
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 151        42  LOAD_GLOBAL              LabelTooLong
               44  RAISE_VARARGS_1       1  'exception instance'
               46  POP_EXCEPT       
               48  JUMP_FORWARD         52  'to 52'
             50_0  COME_FROM            34  '34'
               50  END_FINALLY      
             52_0  COME_FROM            48  '48'

Parse error at or near `POP_TOP' instruction at offset 38

            def decode(self, label):
                if not self.strict_decode:
                    return super(IDNA2003Codec, self).decode(label)
                if label == b'':
                    return ''
                try:
                    return _escapify(encodings.idna.ToUnicode(label), True)
                            except Exception as e:
                    try:
                        raise IDNAException(idna_exception=e)
                    finally:
                        e = None
                        del e


        class IDNA2008Codec(IDNACodec):
            __doc__ = 'IDNA 2008 encoder/decoder.\n\n        *uts_46* is a ``bool``.  If True, apply Unicode IDNA\n        compatibility processing as described in Unicode Technical\n        Standard #46 (http://unicode.org/reports/tr46/).\n        If False, do not apply the mapping.  The default is False.\n\n        *transitional* is a ``bool``: If True, use the\n        "transitional" mode described in Unicode Technical Standard\n        #46.  The default is False.\n\n        *allow_pure_ascii* is a ``bool``.  If True, then a label which\n        consists of only ASCII characters is allowed.  This is less\n        strict than regular IDNA 2008, but is also necessary for mixed\n        names, e.g. a name with starting with "_sip._tcp." and ending\n        in an IDN suffix which would otherwise be disallowed.  The\n        default is False.\n\n        *strict_decode* is a ``bool``: If True, then IDNA2008 checking\n        is done when decoding.  This can cause failures if the name\n        was encoded with IDNA2003.  The default is False.\n        '

            def __init__(self, uts_46=False, transitional=False, allow_pure_ascii=False, strict_decode=False):
                """Initialize the IDNA 2008 encoder/decoder."""
                super(IDNA2008Codec, self).__init__()
                self.uts_46 = uts_46
                self.transitional = transitional
                self.allow_pure_ascii = allow_pure_ascii
                self.strict_decode = strict_decode

            def is_all_ascii(self, label):
                for c in label:
                    if ord(c) > 127:
                        return False
                    return True

            def encode(self, label):
                if label == '':
                    return b''
                else:
                    if self.allow_pure_ascii:
                        if self.is_all_ascii(label):
                            return label.encode('ascii')
                    assert have_idna_2008
                try:
                    if self.uts_46:
                        label = idna.uts46_remap(label, False, self.transitional)
                    return idna.alabel(label)
                            except idna.IDNAError as e:
                    try:
                        raise IDNAException(idna_exception=e)
                    finally:
                        e = None
                        del e

            def decode(self, label):
                if not self.strict_decode:
                    return super(IDNA2008Codec, self).decode(label)
                else:
                    if label == b'':
                        return ''
                    assert have_idna_2008
                try:
                    if self.uts_46:
                        label = idna.uts46_remap(label, False, False)
                    return _escapify(idna.ulabel(label), True)
                            except idna.IDNAError as e:
                    try:
                        raise IDNAException(idna_exception=e)
                    finally:
                        e = None
                        del e


        _escaped = bytearray(b'"().;\\@$')
        IDNA_2003_Practical = IDNA2003Codec(False)
        IDNA_2003_Strict = IDNA2003Codec(True)
        IDNA_2003 = IDNA_2003_Practical
        IDNA_2008_Practical = IDNA2008Codec(True, False, True, False)
        IDNA_2008_UTS_46 = IDNA2008Codec(True, False, False, False)
        IDNA_2008_Strict = IDNA2008Codec(False, False, False, True)
        IDNA_2008_Transitional = IDNA2008Codec(True, True, False, False)
        IDNA_2008 = IDNA_2008_Practical

        def _escapify(label, unicode_mode=False):
            """Escape the characters in label which need it.
    @param unicode_mode: escapify only special and whitespace (<= 0x20)
    characters
    @returns: the escaped string
    @rtype: string"""
            text = unicode_mode or ''
            if isinstance(label, text_type):
                label = label.encode()
            for c in bytearray(label):
                if c in _escaped:
                    text += '\\' + chr(c)
                elif c > 32 and c < 127:
                    text += chr(c)
                else:
                    text += '\\%03d' % c
            else:
                return text.encode()
                text = ''
                if isinstance(label, binary_type):
                    label = label.decode()
                for c in label:
                    if c > ' ' and c < '\x7f':
                        text += c
                    elif c >= '\x7f':
                        text += c
                    else:
                        text += '\\%03d' % ord(c)
                else:
                    return text


        def _validate_labels(labels):
            """Check for empty labels in the middle of a label sequence,
    labels that are too long, and for too many labels.

    Raises ``dns.name.NameTooLong`` if the name as a whole is too long.

    Raises ``dns.name.EmptyLabel`` if a label is empty (i.e. the root
    label) and appears in a position other than the end of the label
    sequence

    """
            l = len(labels)
            total = 0
            i = -1
            j = 0
            for label in labels:
                ll = len(label)
                total += ll + 1
                if ll > 63:
                    raise LabelTooLong
                if i < 0:
                    if label == b'':
                        i = j
                j += 1
            else:
                if total > 255:
                    raise NameTooLong
                if i >= 0:
                    if i != l - 1:
                        raise EmptyLabel


        def _maybe_convert_to_binary(label):
            """If label is ``text``, convert it to ``binary``.  If it is already
    ``binary`` just return it.

    """
            if isinstance(label, binary_type):
                return label
            if isinstance(label, text_type):
                return label.encode()
            raise ValueError


        class Name(object):
            __doc__ = 'A DNS name.\n\n    The dns.name.Name class represents a DNS name as a tuple of\n    labels.  Each label is a `binary` in DNS wire format.  Instances\n    of the class are immutable.\n    '
            __slots__ = [
             'labels']

            def __init__(self, labels):
                labels = [_maybe_convert_to_binary(x) for x in labels]
                super(Name, self).__setattr__('labels', tuple(labels))
                _validate_labels(self.labels)

            def __setattr__(self, name, value):
                raise TypeError("object doesn't support attribute assignment")

            def __copy__(self):
                return Name(self.labels)

            def __deepcopy__(self, memo):
                return Name(copy.deepcopy(self.labels, memo))

            def __getstate__(self):
                return {'labels': self.labels}

            def __setstate__(self, state):
                super(Name, self).__setattr__('labels', state['labels'])
                _validate_labels(self.labels)

            def is_absolute(self):
                """Is the most significant label of this name the root label?

        Returns a ``bool``.
        """
                return len(self.labels) > 0 and self.labels[(-1)] == b''

            def is_wild(self):
                """Is this name wild?  (I.e. Is the least significant label '*'?)

        Returns a ``bool``.
        """
                return len(self.labels) > 0 and self.labels[0] == b'*'

            def __hash__(self):
                """Return a case-insensitive hash of the name.

        Returns an ``int``.
        """
                h = long(0)
                for label in self.labels:
                    for c in bytearray(label.lower()):
                        h += (h << 3) + c
                    else:
                        return int(h % maxint)

            def fullcompare(self, other):
                """Compare two names, returning a 3-tuple
        ``(relation, order, nlabels)``.

        *relation* describes the relation ship between the names,
        and is one of: ``dns.name.NAMERELN_NONE``,
        ``dns.name.NAMERELN_SUPERDOMAIN``, ``dns.name.NAMERELN_SUBDOMAIN``,
        ``dns.name.NAMERELN_EQUAL``, or ``dns.name.NAMERELN_COMMONANCESTOR``.

        *order* is < 0 if *self* < *other*, > 0 if *self* > *other*, and ==
        0 if *self* == *other*.  A relative name is always less than an
        absolute name.  If both names have the same relativity, then
        the DNSSEC order relation is used to order them.

        *nlabels* is the number of significant labels that the two names
        have in common.

        Here are some examples.  Names ending in "." are absolute names,
        those not ending in "." are relative names.

        =============  =============  ===========  =====  =======
        self           other          relation     order  nlabels
        =============  =============  ===========  =====  =======
        www.example.   www.example.   equal        0      3
        www.example.   example.       subdomain    > 0    2
        example.       www.example.   superdomain  < 0    2
        example1.com.  example2.com.  common anc.  < 0    2
        example1       example2.      none         < 0    0
        example1.      example2       none         > 0    0
        =============  =============  ===========  =====  =======
        """
                sabs = self.is_absolute()
                oabs = other.is_absolute()
                if sabs != oabs:
                    if sabs:
                        return (
                         NAMERELN_NONE, 1, 0)
                else:
                    return (
                     NAMERELN_NONE, -1, 0)
                    l1 = len(self.labels)
                    l2 = len(other.labels)
                    ldiff = l1 - l2
                    if ldiff < 0:
                        l = l1
                    else:
                        l = l2
                order = 0
                nlabels = 0
                namereln = NAMERELN_NONE
                if l > 0:
                    l -= 1
                    l1 -= 1
                    l2 -= 1
                    label1 = self.labels[l1].lower()
                    label2 = other.labels[l2].lower()
                    if label1 < label2:
                        order = -1
                        if nlabels > 0:
                            namereln = NAMERELN_COMMONANCESTOR
                        return (
                         namereln, order, nlabels)
                        if label1 > label2:
                            order = 1
                            if nlabels > 0:
                                namereln = NAMERELN_COMMONANCESTOR
                            return (
                             namereln, order, nlabels)
                        nlabels += 1
                    else:
                        order = ldiff
                        if ldiff < 0:
                            namereln = NAMERELN_SUPERDOMAIN
                elif ldiff > 0:
                    namereln = NAMERELN_SUBDOMAIN
                else:
                    namereln = NAMERELN_EQUAL
                return (
                 namereln, order, nlabels)

            def is_subdomain(self, other):
                """Is self a subdomain of other?

        Note that the notion of subdomain includes equality, e.g.
        "dnpython.org" is a subdomain of itself.

        Returns a ``bool``.
        """
                nr, o, nl = self.fullcompare(other)
                if nr == NAMERELN_SUBDOMAIN or nr == NAMERELN_EQUAL:
                    return True
                return False

            def is_superdomain(self, other):
                """Is self a superdomain of other?

        Note that the notion of superdomain includes equality, e.g.
        "dnpython.org" is a superdomain of itself.

        Returns a ``bool``.
        """
                nr, o, nl = self.fullcompare(other)
                if nr == NAMERELN_SUPERDOMAIN or nr == NAMERELN_EQUAL:
                    return True
                return False

            def canonicalize(self):
                """Return a name which is equal to the current name, but is in
        DNSSEC canonical form.
        """
                return Name([x.lower() for x in self.labels])

            def __eq__(self, other):
                if isinstance(other, Name):
                    return self.fullcompare(other)[1] == 0
                return False

            def __ne__(self, other):
                if isinstance(other, Name):
                    return self.fullcompare(other)[1] != 0
                return True

            def __lt__(self, other):
                if isinstance(other, Name):
                    return self.fullcompare(other)[1] < 0
                return NotImplemented

            def __le__(self, other):
                if isinstance(other, Name):
                    return self.fullcompare(other)[1] <= 0
                return NotImplemented

            def __ge__(self, other):
                if isinstance(other, Name):
                    return self.fullcompare(other)[1] >= 0
                return NotImplemented

            def __gt__(self, other):
                if isinstance(other, Name):
                    return self.fullcompare(other)[1] > 0
                return NotImplemented

            def __repr__(self):
                return '<DNS name ' + self.__str__() + '>'

            def __str__(self):
                return self.to_text(False)

            def to_text(self, omit_final_dot=False):
                """Convert name to DNS text format.

        *omit_final_dot* is a ``bool``.  If True, don't emit the final
        dot (denoting the root label) for absolute names.  The default
        is False.

        Returns a ``text``.
        """
                if len(self.labels) == 0:
                    return maybe_decode(b'@')
                if len(self.labels) == 1:
                    if self.labels[0] == b'':
                        return maybe_decode(b'.')
                if omit_final_dot and self.is_absolute():
                    l = self.labels[:-1]
                else:
                    l = self.labels
                s = (b'.').join(map(_escapify, l))
                return maybe_decode(s)

            def to_unicode(self, omit_final_dot=False, idna_codec=None):
                """Convert name to Unicode text format.

        IDN ACE labels are converted to Unicode.

        *omit_final_dot* is a ``bool``.  If True, don't emit the final
        dot (denoting the root label) for absolute names.  The default
        is False.
        *idna_codec* specifies the IDNA encoder/decoder.  If None, the
        dns.name.IDNA_2003_Practical encoder/decoder is used.
        The IDNA_2003_Practical decoder does
        not impose any policy, it just decodes punycode, so if you
        don't want checking for compliance, you can use this decoder
        for IDNA2008 as well.

        Returns a ``text``.
        """
                if len(self.labels) == 0:
                    return '@'
                if len(self.labels) == 1:
                    if self.labels[0] == b'':
                        return '.'
                if omit_final_dot and self.is_absolute():
                    l = self.labels[:-1]
                else:
                    l = self.labels
                if idna_codec is None:
                    idna_codec = IDNA_2003_Practical
                return '.'.join([idna_codec.decode(x) for x in l])

            def to_digestable(self, origin=None):
                """Convert name to a format suitable for digesting in hashes.

        The name is canonicalized and converted to uncompressed wire
        format.  All names in wire format are absolute.  If the name
        is a relative name, then an origin must be supplied.

        *origin* is a ``dns.name.Name`` or ``None``.  If the name is
        relative and origin is not ``None``, then origin will be appended
        to the name.

        Raises ``dns.name.NeedAbsoluteNameOrOrigin`` if the name is
        relative and no origin was provided.

        Returns a ``binary``.
        """
                if not self.is_absolute():
                    if not (origin is None or origin.is_absolute()):
                        raise NeedAbsoluteNameOrOrigin
                    labels = list(self.labels)
                    labels.extend(list(origin.labels))
                else:
                    labels = self.labels
                dlabels = [struct.pack('!B%ds' % len(x), len(x), x.lower()) for x in labels]
                return (b'').join(dlabels)

            def to_wire(self, file=None, compress=None, origin=None):
                """Convert name to wire format, possibly compressing it.

        *file* is the file where the name is emitted (typically a
        BytesIO file).  If ``None`` (the default), a ``binary``
        containing the wire name will be returned.

        *compress*, a ``dict``, is the compression table to use.  If
        ``None`` (the default), names will not be compressed.

        *origin* is a ``dns.name.Name`` or ``None``.  If the name is
        relative and origin is not ``None``, then *origin* will be appended
        to it.

        Raises ``dns.name.NeedAbsoluteNameOrOrigin`` if the name is
        relative and no origin was provided.

        Returns a ``binary`` or ``None``.
        """
                if file is None:
                    file = BytesIO()
                    want_return = True
                else:
                    want_return = False
                if not self.is_absolute():
                    if not (origin is None or origin.is_absolute()):
                        raise NeedAbsoluteNameOrOrigin
                    labels = list(self.labels)
                    labels.extend(list(origin.labels))
                else:
                    labels = self.labels
                i = 0
                for label in labels:
                    n = Name(labels[i:])
                    i += 1
                    if compress is not None:
                        pos = compress.get(n)
                    else:
                        pos = None
                    if pos is not None:
                        value = 49152 + pos
                        s = struct.pack('!H', value)
                        file.write(s)
                        break
                else:
                    if compress is not None:
                        if len(n) > 1:
                            pos = file.tell()
                            if pos <= 16383:
                                compress[n] = pos
                    l = len(label)
                    file.write(struct.pack('!B', l))
                    if l > 0:
                        file.write(label)
                    if want_return:
                        return file.getvalue()

            def __len__(self):
                """The length of the name (in labels).

        Returns an ``int``.
        """
                return len(self.labels)

            def __getitem__(self, index):
                return self.labels[index]

            def __add__(self, other):
                return self.concatenate(other)

            def __sub__(self, other):
                return self.relativize(other)

            def split(self, depth):
                """Split a name into a prefix and suffix names at the specified depth.

        *depth* is an ``int`` specifying the number of labels in the suffix

        Raises ``ValueError`` if *depth* was not >= 0 and <= the length of the
        name.

        Returns the tuple ``(prefix, suffix)``.
        """
                l = len(self.labels)
                if depth == 0:
                    return (
                     self, dns.name.empty)
                if depth == l:
                    return (
                     dns.name.empty, self)
                if depth < 0 or depth > l:
                    raise ValueError('depth must be >= 0 and <= the length of the name')
                return (
                 Name(self[:-depth]), Name(self[-depth:]))

            def concatenate(self, other):
                """Return a new name which is the concatenation of self and other.

        Raises ``dns.name.AbsoluteConcatenation`` if the name is
        absolute and *other* is not the empty name.

        Returns a ``dns.name.Name``.
        """
                if self.is_absolute():
                    if len(other) > 0:
                        raise AbsoluteConcatenation
                labels = list(self.labels)
                labels.extend(list(other.labels))
                return Name(labels)

            def relativize(self, origin):
                """If the name is a subdomain of *origin*, return a new name which is
        the name relative to origin.  Otherwise return the name.

        For example, relativizing ``www.dnspython.org.`` to origin
        ``dnspython.org.`` returns the name ``www``.  Relativizing ``example.``
        to origin ``dnspython.org.`` returns ``example.``.

        Returns a ``dns.name.Name``.
        """
                if origin is not None:
                    if self.is_subdomain(origin):
                        return Name(self[:-len(origin)])
                return self

            def derelativize(self, origin):
                """If the name is a relative name, return a new name which is the
        concatenation of the name and origin.  Otherwise return the name.

        For example, derelativizing ``www`` to origin ``dnspython.org.``
        returns the name ``www.dnspython.org.``.  Derelativizing ``example.``
        to origin ``dnspython.org.`` returns ``example.``.

        Returns a ``dns.name.Name``.
        """
                if not self.is_absolute():
                    return self.concatenate(origin)
                return self

            def choose_relativity(self, origin=None, relativize=True):
                """Return a name with the relativity desired by the caller.

        If *origin* is ``None``, then the name is returned.
        Otherwise, if *relativize* is ``True`` the name is
        relativized, and if *relativize* is ``False`` the name is
        derelativized.

        Returns a ``dns.name.Name``.
        """
                if origin:
                    if relativize:
                        return self.relativize(origin)
                    return self.derelativize(origin)
                else:
                    return self

            def parent(self):
                """Return the parent of the name.

        For example, the parent of ``www.dnspython.org.`` is ``dnspython.org``.

        Raises ``dns.name.NoParent`` if the name is either the root name or the
        empty name, and thus has no parent.

        Returns a ``dns.name.Name``.
        """
                if self == root or self == empty:
                    raise NoParent
                return Name(self.labels[1:])


        root = Name([b''])
        empty = Name([])

        def from_unicode(text, origin=root, idna_codec=None):
            """Convert unicode text into a Name object.

    Labels are encoded in IDN ACE form according to rules specified by
    the IDNA codec.

    *text*, a ``text``, is the text to convert into a name.

    *origin*, a ``dns.name.Name``, specifies the origin to
    append to non-absolute names.  The default is the root name.

    *idna_codec*, a ``dns.name.IDNACodec``, specifies the IDNA
    encoder/decoder.  If ``None``, the default IDNA 2003 encoder/decoder
    is used.

    Returns a ``dns.name.Name``.
    """
            if not isinstance(text, text_type):
                raise ValueError('input to from_unicode() must be a unicode string')
            else:
                if not origin is None:
                    if not isinstance(origin, Name):
                        raise ValueError('origin must be a Name or None')
                else:
                    labels = []
                    label = ''
                    escaping = False
                    edigits = 0
                    total = 0
                    if idna_codec is None:
                        idna_codec = IDNA_2003
                    if text == '@':
                        text = ''
                    if text:
                        if text == '.':
                            return Name([b''])
                            for c in text:
                                if escaping:
                                    if edigits == 0:
                                        if c.isdigit():
                                            total = int(c)
                                            edigits += 1
                                        else:
                                            label += c
                                            escaping = False
                                    else:
                                        if not c.isdigit():
                                            raise BadEscape
                                        total *= 10
                                        total += int(c)
                                        edigits += 1
                                    if edigits == 3:
                                        escaping = False
                                        label += unichr(total)
                                    elif c in ('.', '。', '．', '｡'):
                                        if len(label) == 0:
                                            raise EmptyLabel
                                        labels.append(idna_codec.encode(label))
                                        label = ''
                                elif c == '\\':
                                    escaping = True
                                    edigits = 0
                                    total = 0
                                else:
                                    label += c
                            else:
                                if escaping:
                                    raise BadEscape

                            if len(label) > 0:
                                labels.append(idna_codec.encode(label))
                        else:
                            labels.append(b'')
                if len(labels) == 0 or labels[(-1)] != b'':
                    if origin is not None:
                        labels.extend(list(origin.labels))
            return Name(labels)


        def from_text(text, origin=root, idna_codec=None):
            """Convert text into a Name object.

    *text*, a ``text``, is the text to convert into a name.

    *origin*, a ``dns.name.Name``, specifies the origin to
    append to non-absolute names.  The default is the root name.

    *idna_codec*, a ``dns.name.IDNACodec``, specifies the IDNA
    encoder/decoder.  If ``None``, the default IDNA 2003 encoder/decoder
    is used.

    Returns a ``dns.name.Name``.
    """
            if isinstance(text, text_type):
                return from_unicode(text, origin, idna_codec)
                if not isinstance(text, binary_type):
                    raise ValueError('input to from_text() must be a string')
                if not origin is None:
                    if not isinstance(origin, Name):
                        raise ValueError('origin must be a Name or None')
                labels = []
                label = b''
                escaping = False
                edigits = 0
                total = 0
                if text == b'@':
                    text = b''
                if text:
                    if text == b'.':
                        return Name([b''])
                    else:
                        for c in bytearray(text):
                            byte_ = struct.pack('!B', c)
                            if escaping:
                                if edigits == 0:
                                    if byte_.isdigit():
                                        total = int(byte_)
                                        edigits += 1
                                    else:
                                        label += byte_
                                        escaping = False
                                else:
                                    if not byte_.isdigit():
                                        raise BadEscape
                                    total *= 10
                                    total += int(byte_)
                                    edigits += 1
                                    if edigits == 3:
                                        escaping = False
                                        label += struct.pack('!B', total)
                                    elif byte_ == b'.':
                                        if len(label) == 0:
                                            raise EmptyLabel
                                        labels.append(label)
                                        label = b''
                                    else:
                                        if byte_ == b'\\':
                                            escaping = True
                                            edigits = 0
                                            total = 0
                            else:
                                label += byte_
                        else:
                            if escaping:
                                raise BadEscape
                            if len(label) > 0:
                                labels.append(label)
                            else:
                                labels.append(b'')

            elif len(labels) == 0 or labels[(-1)] != b'':
                if origin is not None:
                    labels.extend(list(origin.labels))
            return Name(labels)


        def from_wire(message, current):
            """Convert possibly compressed wire format into a Name.

    *message* is a ``binary`` containing an entire DNS message in DNS
    wire form.

    *current*, an ``int``, is the offset of the beginning of the name
    from the start of the message

    Raises ``dns.name.BadPointer`` if a compression pointer did not
    point backwards in the message.

    Raises ``dns.name.BadLabelType`` if an invalid label type was encountered.

    Returns a ``(dns.name.Name, int)`` tuple consisting of the name
    that was read and the number of bytes of the wire format message
    which were consumed reading it.
    """
            if not isinstance(message, binary_type):
                raise ValueError('input to from_wire() must be a byte string')
            else:
                message = dns.wiredata.maybe_wrap(message)
                labels = []
                biggest_pointer = current
                hops = 0
                count = message[current]
                current += 1
                cused = 1
                while True:
                    if count != 0:
                        if count < 64:
                            labels.append(message[current:current + count].unwrap())
                            current += count
                            if hops == 0:
                                cused += count
                        elif count >= 192:
                            current = (count & 63) * 256 + message[current]
                            if hops == 0:
                                cused += 1
                            if current >= biggest_pointer:
                                raise BadPointer
                            biggest_pointer = current
                            hops += 1
                        else:
                            raise BadLabelType
                        count = message[current]
                        current += 1
                        if hops == 0:
                            cused += 1

            labels.append('')
            return (Name(labels), cused)