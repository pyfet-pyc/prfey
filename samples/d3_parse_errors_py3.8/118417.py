# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\webencodings\__init__.py
"""

    webencodings
    ~~~~~~~~~~~~

    This is a Python implementation of the `WHATWG Encoding standard
    <http://encoding.spec.whatwg.org/>`. See README for details.

    :copyright: Copyright 2012 by Simon Sapin
    :license: BSD, see LICENSE for details.

"""
from __future__ import unicode_literals
import codecs
from .labels import LABELS
VERSION = '0.5.1'
PYTHON_NAMES = {'iso-8859-8-i':'iso-8859-8', 
 'x-mac-cyrillic':'mac-cyrillic', 
 'macintosh':'mac-roman', 
 'windows-874':'cp874'}
CACHE = {}

def ascii_lower(string):
    r"""Transform (only) ASCII letters to lower case: A-Z is mapped to a-z.

    :param string: An Unicode string.
    :returns: A new Unicode string.

    This is used for `ASCII case-insensitive
    <http://encoding.spec.whatwg.org/#ascii-case-insensitive>`_
    matching of encoding labels.
    The same matching is also used, among other things,
    for `CSS keywords <http://dev.w3.org/csswg/css-values/#keywords>`_.

    This is different from the :meth:`~py:str.lower` method of Unicode strings
    which also affect non-ASCII characters,
    sometimes mapping them into the ASCII range:

        >>> keyword = u'Bac\N{KELVIN SIGN}ground'
        >>> assert keyword.lower() == u'background'
        >>> assert ascii_lower(keyword) != keyword.lower()
        >>> assert ascii_lower(keyword) == u'bac\N{KELVIN SIGN}ground'

    """
    return string.encode('utf8').lower().decode('utf8')


def lookup(label):
    """
    Look for an encoding by its label.
    This is the spec’s `get an encoding
    <http://encoding.spec.whatwg.org/#concept-encoding-get>`_ algorithm.
    Supported labels are listed there.

    :param label: A string.
    :returns:
        An :class:`Encoding` object, or :obj:`None` for an unknown label.

    """
    label = ascii_lower(label.strip('\t\n\x0c\r '))
    name = LABELS.get(label)
    if name is None:
        return
    encoding = CACHE.get(name)
    if encoding is None:
        if name == 'x-user-defined':
            from .x_user_defined import codec_info
        else:
            python_name = PYTHON_NAMES.get(name, name)
            codec_info = codecs.lookup(python_name)
        encoding = Encoding(name, codec_info)
        CACHE[name] = encoding
    return encoding


def _get_encoding(encoding_or_label):
    """
    Accept either an encoding object or label.

    :param encoding: An :class:`Encoding` object or a label string.
    :returns: An :class:`Encoding` object.
    :raises: :exc:`~exceptions.LookupError` for an unknown label.

    """
    if hasattr(encoding_or_label, 'codec_info'):
        return encoding_or_label
    encoding = lookup(encoding_or_label)
    if encoding is None:
        raise LookupError('Unknown encoding label: %r' % encoding_or_label)
    return encoding


class Encoding(object):
    __doc__ = 'Reresents a character encoding such as UTF-8,\n    that can be used for decoding or encoding.\n\n    .. attribute:: name\n\n        Canonical name of the encoding\n\n    .. attribute:: codec_info\n\n        The actual implementation of the encoding,\n        a stdlib :class:`~codecs.CodecInfo` object.\n        See :func:`codecs.register`.\n\n    '

    def __init__(self, name, codec_info):
        self.name = name
        self.codec_info = codec_info

    def __repr__(self):
        return '<Encoding %s>' % self.name


UTF8 = lookup('utf-8')
_UTF16LE = lookup('utf-16le')
_UTF16BE = lookup('utf-16be')

def decode(input, fallback_encoding, errors='replace'):
    """
    Decode a single string.

    :param input: A byte string
    :param fallback_encoding:
        An :class:`Encoding` object or a label string.
        The encoding to use if :obj:`input` does note have a BOM.
    :param errors: Type of error handling. See :func:`codecs.register`.
    :raises: :exc:`~exceptions.LookupError` for an unknown encoding label.
    :return:
        A ``(output, encoding)`` tuple of an Unicode string
        and an :obj:`Encoding`.

    """
    fallback_encoding = _get_encoding(fallback_encoding)
    bom_encoding, input = _detect_bom(input)
    encoding = bom_encoding or fallback_encoding
    return (
     encoding.codec_info.decode(input, errors)[0], encoding)


def _detect_bom(input):
    """Return (bom_encoding, input), with any BOM removed from the input."""
    if input.startswith(b'\xff\xfe'):
        return (_UTF16LE, input[2:])
    if input.startswith(b'\xfe\xff'):
        return (_UTF16BE, input[2:])
    if input.startswith(b'\xef\xbb\xbf'):
        return (UTF8, input[3:])
    return (None, input)


def encode(input, encoding=UTF8, errors='strict'):
    """
    Encode a single string.

    :param input: An Unicode string.
    :param encoding: An :class:`Encoding` object or a label string.
    :param errors: Type of error handling. See :func:`codecs.register`.
    :raises: :exc:`~exceptions.LookupError` for an unknown encoding label.
    :return: A byte string.

    """
    return _get_encoding(encoding).codec_info.encode(input, errors)[0]


def iter_decode(input, fallback_encoding, errors='replace'):
    """
    "Pull"-based decoder.

    :param input:
        An iterable of byte strings.

        The input is first consumed just enough to determine the encoding
        based on the precense of a BOM,
        then consumed on demand when the return value is.
    :param fallback_encoding:
        An :class:`Encoding` object or a label string.
        The encoding to use if :obj:`input` does note have a BOM.
    :param errors: Type of error handling. See :func:`codecs.register`.
    :raises: :exc:`~exceptions.LookupError` for an unknown encoding label.
    :returns:
        An ``(output, encoding)`` tuple.
        :obj:`output` is an iterable of Unicode strings,
        :obj:`encoding` is the :obj:`Encoding` that is being used.

    """
    decoder = IncrementalDecoder(fallback_encoding, errors)
    generator = _iter_decode_generator(input, decoder)
    encoding = next(generator)
    return (
     generator, encoding)


def _iter_decode_generator--- This code section failed: ---

 L. 219         0  LOAD_FAST                'decoder'
                2  LOAD_ATTR                decode
                4  STORE_FAST               'decode'

 L. 220         6  LOAD_GLOBAL              iter
                8  LOAD_FAST                'input'
               10  CALL_FUNCTION_1       1  ''
               12  STORE_FAST               'input'

 L. 221        14  LOAD_FAST                'input'
               16  GET_ITER         
             18_0  COME_FROM            66  '66'
             18_1  COME_FROM            32  '32'
               18  FOR_ITER             68  'to 68'
               20  STORE_FAST               'chunck'

 L. 222        22  LOAD_FAST                'decode'
               24  LOAD_FAST                'chunck'
               26  CALL_FUNCTION_1       1  ''
               28  STORE_FAST               'output'

 L. 223        30  LOAD_FAST                'output'
               32  POP_JUMP_IF_FALSE_BACK    18  'to 18'

 L. 224        34  LOAD_FAST                'decoder'
               36  LOAD_ATTR                encoding
               38  LOAD_CONST               None
               40  COMPARE_OP               is-not
               42  POP_JUMP_IF_TRUE     48  'to 48'
               44  LOAD_ASSERT              AssertionError
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            42  '42'

 L. 225        48  LOAD_FAST                'decoder'
               50  LOAD_ATTR                encoding
               52  YIELD_VALUE      
               54  POP_TOP          

 L. 226        56  LOAD_FAST                'output'
               58  YIELD_VALUE      
               60  POP_TOP          

 L. 227        62  POP_TOP          
               64  BREAK_LOOP          116  'to 116'
               66  JUMP_BACK            18  'to 18'
             68_0  COME_FROM            18  '18'

 L. 230        68  LOAD_FAST                'decode'
               70  LOAD_CONST               b''
               72  LOAD_CONST               True
               74  LOAD_CONST               ('final',)
               76  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               78  STORE_FAST               'output'

 L. 231        80  LOAD_FAST                'decoder'
               82  LOAD_ATTR                encoding
               84  LOAD_CONST               None
               86  COMPARE_OP               is-not
               88  POP_JUMP_IF_TRUE     94  'to 94'
               90  LOAD_ASSERT              AssertionError
               92  RAISE_VARARGS_1       1  'exception instance'
             94_0  COME_FROM            88  '88'

 L. 232        94  LOAD_FAST                'decoder'
               96  LOAD_ATTR                encoding
               98  YIELD_VALUE      
              100  POP_TOP          

 L. 233       102  LOAD_FAST                'output'
              104  POP_JUMP_IF_FALSE   112  'to 112'

 L. 234       106  LOAD_FAST                'output'
              108  YIELD_VALUE      
              110  POP_TOP          
            112_0  COME_FROM           104  '104'

 L. 235       112  LOAD_CONST               None
              114  RETURN_VALUE     
            116_0  COME_FROM            64  '64'

 L. 237       116  LOAD_FAST                'input'
              118  GET_ITER         
            120_0  COME_FROM           142  '142'
            120_1  COME_FROM           134  '134'
              120  FOR_ITER            144  'to 144'
              122  STORE_FAST               'chunck'

 L. 238       124  LOAD_FAST                'decode'
              126  LOAD_FAST                'chunck'
              128  CALL_FUNCTION_1       1  ''
              130  STORE_FAST               'output'

 L. 239       132  LOAD_FAST                'output'
              134  POP_JUMP_IF_FALSE_BACK   120  'to 120'

 L. 240       136  LOAD_FAST                'output'
              138  YIELD_VALUE      
              140  POP_TOP          
              142  JUMP_BACK           120  'to 120'
            144_0  COME_FROM           120  '120'

 L. 241       144  LOAD_FAST                'decode'
              146  LOAD_CONST               b''
              148  LOAD_CONST               True
              150  LOAD_CONST               ('final',)
              152  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              154  STORE_FAST               'output'

 L. 242       156  LOAD_FAST                'output'
              158  POP_JUMP_IF_FALSE   166  'to 166'

 L. 243       160  LOAD_FAST                'output'
              162  YIELD_VALUE      
              164  POP_TOP          
            166_0  COME_FROM           158  '158'

Parse error at or near `POP_TOP' instruction at offset 164


def iter_encode(input, encoding=UTF8, errors='strict'):
    """
    “Pull”-based encoder.

    :param input: An iterable of Unicode strings.
    :param encoding: An :class:`Encoding` object or a label string.
    :param errors: Type of error handling. See :func:`codecs.register`.
    :raises: :exc:`~exceptions.LookupError` for an unknown encoding label.
    :returns: An iterable of byte strings.

    """
    encode = IncrementalEncoder(encoding, errors).encode
    return _iter_encode_generator(input, encode)


def _iter_encode_generator(input, encode):
    for chunck in input:
        output = encode(chunck)
        if output:
            yield output
    else:
        output = encode('', final=True)
        if output:
            yield output


class IncrementalDecoder(object):
    __doc__ = '\n    “Push”-based decoder.\n\n    :param fallback_encoding:\n        An :class:`Encoding` object or a label string.\n        The encoding to use if :obj:`input` does note have a BOM.\n    :param errors: Type of error handling. See :func:`codecs.register`.\n    :raises: :exc:`~exceptions.LookupError` for an unknown encoding label.\n\n    '

    def __init__(self, fallback_encoding, errors='replace'):
        self._fallback_encoding = _get_encoding(fallback_encoding)
        self._errors = errors
        self._buffer = b''
        self._decoder = None
        self.encoding = None

    def decode(self, input, final=False):
        """Decode one chunk of the input.

        :param input: A byte string.
        :param final:
            Indicate that no more input is available.
            Must be :obj:`True` if this is the last call.
        :returns: An Unicode string.

        """
        decoder = self._decoder
        if decoder is not None:
            return decoder(input, final)
        input = self._buffer + input
        encoding, input = _detect_bom(input)
        if encoding is None:
            if len(input) < 3:
                if not final:
                    self._buffer = input
                    return ''
            encoding = self._fallback_encoding
        decoder = encoding.codec_info.incrementaldecoder(self._errors).decode
        self._decoder = decoder
        self.encoding = encoding
        return decoder(input, final)


class IncrementalEncoder(object):
    __doc__ = '\n    “Push”-based encoder.\n\n    :param encoding: An :class:`Encoding` object or a label string.\n    :param errors: Type of error handling. See :func:`codecs.register`.\n    :raises: :exc:`~exceptions.LookupError` for an unknown encoding label.\n\n    .. method:: encode(input, final=False)\n\n        :param input: An Unicode string.\n        :param final:\n            Indicate that no more input is available.\n            Must be :obj:`True` if this is the last call.\n        :returns: A byte string.\n\n    '

    def __init__(self, encoding=UTF8, errors='strict'):
        encoding = _get_encoding(encoding)
        self.encode = encoding.codec_info.incrementalencoder(errors).encode