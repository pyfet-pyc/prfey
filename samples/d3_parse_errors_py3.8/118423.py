# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\websockets\headers.py
"""
:mod:`websockets.headers` provides parsers and serializers for HTTP headers
used in WebSocket handshake messages.

These APIs cannot be imported from :mod:`websockets`. They must be imported
from :mod:`websockets.headers`.

"""
import base64, binascii, re
from typing import Callable, List, NewType, Optional, Sequence, Tuple, TypeVar, cast
from .exceptions import InvalidHeaderFormat, InvalidHeaderValue
from .typing import ExtensionHeader, ExtensionName, ExtensionParameter, Subprotocol
__all__ = [
 'parse_connection',
 'parse_upgrade',
 'parse_extension',
 'build_extension',
 'parse_subprotocol',
 'build_subprotocol',
 'build_www_authenticate_basic',
 'parse_authorization_basic',
 'build_authorization_basic']
T = TypeVar('T')
ConnectionOption = NewType('ConnectionOption', str)
UpgradeProtocol = NewType('UpgradeProtocol', str)

def peek_ahead(header: str, pos: int) -> Optional[str]:
    """
    Return the next character from ``header`` at the given position.

    Return ``None`` at the end of ``header``.

    We never need to peek more than one character ahead.

    """
    if pos == len(header):
        return
    return header[pos]


_OWS_re = re.compile('[\\t ]*')

def parse_OWS(header: str, pos: int) -> int:
    """
    Parse optional whitespace from ``header`` at the given position.

    Return the new position.

    The whitespace itself isn't returned because it isn't significant.

    """
    match = _OWS_re.match(header, pos)
    assert match is not None
    return match.end()


_token_re = re.compile("[-!#$%&\\'*+.^_`|~0-9a-zA-Z]+")

def parse_token(header: str, pos: int, header_name: str) -> Tuple[(str, int)]:
    """
    Parse a token from ``header`` at the given position.

    Return the token value and the new position.

    :raises ~websockets.exceptions.InvalidHeaderFormat: on invalid inputs.

    """
    match = _token_re.match(header, pos)
    if match is None:
        raise InvalidHeaderFormat(header_name, 'expected token', header, pos)
    return (match.group(), match.end())


_quoted_string_re = re.compile('"(?:[\\x09\\x20-\\x21\\x23-\\x5b\\x5d-\\x7e]|\\\\[\\x09\\x20-\\x7e\\x80-\\xff])*"')
_unquote_re = re.compile('\\\\([\\x09\\x20-\\x7e\\x80-\\xff])')

def parse_quoted_string(header: str, pos: int, header_name: str) -> Tuple[(str, int)]:
    """
    Parse a quoted string from ``header`` at the given position.

    Return the unquoted value and the new position.

    :raises ~websockets.exceptions.InvalidHeaderFormat: on invalid inputs.

    """
    match = _quoted_string_re.match(header, pos)
    if match is None:
        raise InvalidHeaderFormat(header_name, 'expected quoted string', header, pos)
    return (_unquote_re.sub('\\1', match.group()[1:-1]), match.end())


_quotable_re = re.compile('[\\x09\\x20-\\x7e\\x80-\\xff]*')
_quote_re = re.compile('([\\x22\\x5c])')

def build_quoted_string(value: str) -> str:
    """
    Format ``value`` as a quoted string.

    This is the reverse of :func:`parse_quoted_string`.

    """
    match = _quotable_re.fullmatch(value)
    if match is None:
        raise ValueError('invalid characters for quoted-string encoding')
    return '"' + _quote_re.sub('\\\\\\1', value) + '"'


def parse_list--- This code section failed: ---
              0_0  COME_FROM            28  '28'

 L. 163         0  LOAD_GLOBAL              peek_ahead
                2  LOAD_FAST                'header'
                4  LOAD_FAST                'pos'
                6  CALL_FUNCTION_2       2  ''
                8  LOAD_STR                 ','
               10  COMPARE_OP               ==
               12  POP_JUMP_IF_FALSE    30  'to 30'

 L. 164        14  LOAD_GLOBAL              parse_OWS
               16  LOAD_FAST                'header'
               18  LOAD_FAST                'pos'
               20  LOAD_CONST               1
               22  BINARY_ADD       
               24  CALL_FUNCTION_2       2  ''
               26  STORE_FAST               'pos'
               28  JUMP_BACK             0  'to 0'
             30_0  COME_FROM            12  '12'

 L. 166        30  BUILD_LIST_0          0 
               32  STORE_FAST               'items'
             34_0  COME_FROM           172  '172'
             34_1  COME_FROM           168  '168'

 L. 169        34  LOAD_FAST                'parse_item'
               36  LOAD_FAST                'header'
               38  LOAD_FAST                'pos'
               40  LOAD_FAST                'header_name'
               42  CALL_FUNCTION_3       3  ''
               44  UNPACK_SEQUENCE_2     2 
               46  STORE_FAST               'item'
               48  STORE_FAST               'pos'

 L. 170        50  LOAD_FAST                'items'
               52  LOAD_METHOD              append
               54  LOAD_FAST                'item'
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          

 L. 171        60  LOAD_GLOBAL              parse_OWS
               62  LOAD_FAST                'header'
               64  LOAD_FAST                'pos'
               66  CALL_FUNCTION_2       2  ''
               68  STORE_FAST               'pos'

 L. 174        70  LOAD_FAST                'pos'
               72  LOAD_GLOBAL              len
               74  LOAD_FAST                'header'
               76  CALL_FUNCTION_1       1  ''
               78  COMPARE_OP               ==
               80  POP_JUMP_IF_FALSE    84  'to 84'

 L. 175        82  JUMP_FORWARD        174  'to 174'
             84_0  COME_FROM            80  '80'

 L. 178        84  LOAD_GLOBAL              peek_ahead
               86  LOAD_FAST                'header'
               88  LOAD_FAST                'pos'
               90  CALL_FUNCTION_2       2  ''
               92  LOAD_STR                 ','
               94  COMPARE_OP               ==
               96  POP_JUMP_IF_FALSE   114  'to 114'

 L. 179        98  LOAD_GLOBAL              parse_OWS
              100  LOAD_FAST                'header'
              102  LOAD_FAST                'pos'
              104  LOAD_CONST               1
              106  BINARY_ADD       
              108  CALL_FUNCTION_2       2  ''
              110  STORE_FAST               'pos'
              112  JUMP_FORWARD        128  'to 128'
            114_0  COME_FROM            96  '96'

 L. 181       114  LOAD_GLOBAL              InvalidHeaderFormat
              116  LOAD_FAST                'header_name'
              118  LOAD_STR                 'expected comma'
              120  LOAD_FAST                'header'
              122  LOAD_FAST                'pos'
              124  CALL_FUNCTION_4       4  ''
              126  RAISE_VARARGS_1       1  'exception instance'
            128_0  COME_FROM           156  '156'
            128_1  COME_FROM           112  '112'

 L. 184       128  LOAD_GLOBAL              peek_ahead
              130  LOAD_FAST                'header'
              132  LOAD_FAST                'pos'
              134  CALL_FUNCTION_2       2  ''
              136  LOAD_STR                 ','
              138  COMPARE_OP               ==
              140  POP_JUMP_IF_FALSE   158  'to 158'

 L. 185       142  LOAD_GLOBAL              parse_OWS
              144  LOAD_FAST                'header'
              146  LOAD_FAST                'pos'
              148  LOAD_CONST               1
              150  BINARY_ADD       
              152  CALL_FUNCTION_2       2  ''
              154  STORE_FAST               'pos'
              156  JUMP_BACK           128  'to 128'
            158_0  COME_FROM           140  '140'

 L. 188       158  LOAD_FAST                'pos'
              160  LOAD_GLOBAL              len
              162  LOAD_FAST                'header'
              164  CALL_FUNCTION_1       1  ''
              166  COMPARE_OP               ==
              168  POP_JUMP_IF_FALSE_BACK    34  'to 34'

 L. 189       170  JUMP_FORWARD        174  'to 174'
              172  JUMP_BACK            34  'to 34'
            174_0  COME_FROM           170  '170'
            174_1  COME_FROM            82  '82'

 L. 193       174  LOAD_FAST                'pos'
              176  LOAD_GLOBAL              len
              178  LOAD_FAST                'header'
              180  CALL_FUNCTION_1       1  ''
              182  COMPARE_OP               ==
              184  POP_JUMP_IF_TRUE    190  'to 190'
              186  LOAD_ASSERT              AssertionError
              188  RAISE_VARARGS_1       1  'exception instance'
            190_0  COME_FROM           184  '184'

 L. 195       190  LOAD_FAST                'items'
              192  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 172


def parse_connection_option(header: str, pos: int, header_name: str) -> Tuple[(ConnectionOption, int)]:
    """
    Parse a Connection option from ``header`` at the given position.

    Return the protocol value and the new position.

    :raises ~websockets.exceptions.InvalidHeaderFormat: on invalid inputs.

    """
    item, pos = parse_tokenheaderposheader_name
    return (
     cast(ConnectionOption, item), pos)


def parse_connection(header: str) -> List[ConnectionOption]:
    """
    Parse a ``Connection`` header.

    Return a list of HTTP connection options.

    :param header: value of the ``Connection`` header
    :raises ~websockets.exceptions.InvalidHeaderFormat: on invalid inputs.

    """
    return parse_list(parse_connection_option, header, 0, 'Connection')


_protocol_re = re.compile("[-!#$%&\\'*+.^_`|~0-9a-zA-Z]+(?:/[-!#$%&\\'*+.^_`|~0-9a-zA-Z]+)?")

def parse_upgrade_protocol(header: str, pos: int, header_name: str) -> Tuple[(UpgradeProtocol, int)]:
    """
    Parse an Upgrade protocol from ``header`` at the given position.

    Return the protocol value and the new position.

    :raises ~websockets.exceptions.InvalidHeaderFormat: on invalid inputs.

    """
    match = _protocol_re.match(header, pos)
    if match is None:
        raise InvalidHeaderFormat(header_name, 'expected protocol', header, pos)
    return (cast(UpgradeProtocol, match.group()), match.end())


def parse_upgrade(header: str) -> List[UpgradeProtocol]:
    """
    Parse an ``Upgrade`` header.

    Return a list of HTTP protocols.

    :param header: value of the ``Upgrade`` header
    :raises ~websockets.exceptions.InvalidHeaderFormat: on invalid inputs.

    """
    return parse_list(parse_upgrade_protocol, header, 0, 'Upgrade')


def parse_extension_item_param(header: str, pos: int, header_name: str) -> Tuple[(ExtensionParameter, int)]:
    """
    Parse a single extension parameter from ``header`` at the given position.

    Return a ``(name, value)`` pair and the new position.

    :raises ~websockets.exceptions.InvalidHeaderFormat: on invalid inputs.

    """
    name, pos = parse_tokenheaderposheader_name
    pos = parse_OWS(header, pos)
    value = None
    if peek_ahead(header, pos) == '=':
        pos = parse_OWS(header, pos + 1)
        if peek_ahead(header, pos) == '"':
            pos_before = pos
            value, pos = parse_quoted_stringheaderposheader_name
            if _token_re.fullmatch(value) is None:
                raise InvalidHeaderFormat(header_name, 'invalid quoted header content', header, pos_before)
        else:
            value, pos = parse_tokenheaderposheader_name
        pos = parse_OWS(header, pos)
    return (
     (
      name, value), pos)


def parse_extension_item(header: str, pos: int, header_name: str) -> Tuple[(ExtensionHeader, int)]:
    """
    Parse an extension definition from ``header`` at the given position.

    Return an ``(extension name, parameters)`` pair, where ``parameters`` is a
    list of ``(name, value)`` pairs, and the new position.

    :raises ~websockets.exceptions.InvalidHeaderFormat: on invalid inputs.

    """
    name, pos = parse_tokenheaderposheader_name
    pos = parse_OWS(header, pos)
    parameters = []
    while True:
        if peek_ahead(header, pos) == ';':
            pos = parse_OWS(header, pos + 1)
            parameter, pos = parse_extension_item_paramheaderposheader_name
            parameters.append(parameter)

    return (
     (
      cast(ExtensionName, name), parameters), pos)


def parse_extension(header: str) -> List[ExtensionHeader]:
    """
    Parse a ``Sec-WebSocket-Extensions`` header.

    Return a list of WebSocket extensions and their parameters in this format::

        [
            (
                'extension name',
                [
                    ('parameter name', 'parameter value'),
                    ....
                ]
            ),
            ...
        ]

    Parameter values are ``None`` when no value is provided.

    :raises ~websockets.exceptions.InvalidHeaderFormat: on invalid inputs.

    """
    return parse_list(parse_extension_item, header, 0, 'Sec-WebSocket-Extensions')


parse_extension_list = parse_extension

def build_extension_item(name: ExtensionName, parameters: List[ExtensionParameter]) -> str:
    """
    Build an extension definition.

    This is the reverse of :func:`parse_extension_item`.

    """
    return '; '.join([
     cast(str, name)] + [name if value is None else f"{name}={value}" for name, value in parameters])


def build_extension(extensions: Sequence[ExtensionHeader]) -> str:
    """
    Build a ``Sec-WebSocket-Extensions`` header.

    This is the reverse of :func:`parse_extension`.

    """
    return ', '.join((build_extension_item(name, parameters) for name, parameters in extensions))


build_extension_list = build_extension

def parse_subprotocol_item(header: str, pos: int, header_name: str) -> Tuple[(Subprotocol, int)]:
    """
    Parse a subprotocol from ``header`` at the given position.

    Return the subprotocol value and the new position.

    :raises ~websockets.exceptions.InvalidHeaderFormat: on invalid inputs.

    """
    item, pos = parse_tokenheaderposheader_name
    return (
     cast(Subprotocol, item), pos)


def parse_subprotocol(header: str) -> List[Subprotocol]:
    """
    Parse a ``Sec-WebSocket-Protocol`` header.

    Return a list of WebSocket subprotocols.

    :raises ~websockets.exceptions.InvalidHeaderFormat: on invalid inputs.

    """
    return parse_list(parse_subprotocol_item, header, 0, 'Sec-WebSocket-Protocol')


parse_subprotocol_list = parse_subprotocol

def build_subprotocol(protocols: Sequence[Subprotocol]) -> str:
    """
    Build a ``Sec-WebSocket-Protocol`` header.

    This is the reverse of :func:`parse_subprotocol`.

    """
    return ', '.join(protocols)


build_subprotocol_list = build_subprotocol

def build_www_authenticate_basic(realm: str) -> str:
    """
    Build a ``WWW-Authenticate`` header for HTTP Basic Auth.

    :param realm: authentication realm

    """
    realm = build_quoted_string(realm)
    charset = build_quoted_string('UTF-8')
    return f"Basic realm={realm}, charset={charset}"


_token68_re = re.compile('[A-Za-z0-9-._~+/]+=*')

def parse_token68(header: str, pos: int, header_name: str) -> Tuple[(str, int)]:
    """
    Parse a token68 from ``header`` at the given position.

    Return the token value and the new position.

    :raises ~websockets.exceptions.InvalidHeaderFormat: on invalid inputs.

    """
    match = _token68_re.match(header, pos)
    if match is None:
        raise InvalidHeaderFormat(header_name, 'expected token68', header, pos)
    return (match.group(), match.end())


def parse_end(header: str, pos: int, header_name: str) -> None:
    """
    Check that parsing reached the end of header.

    """
    if pos < len(header):
        raise InvalidHeaderFormat(header_name, 'trailing data', header, pos)


def parse_authorization_basic(header: str) -> Tuple[(str, str)]:
    """
    Parse an ``Authorization`` header for HTTP Basic Auth.

    Return a ``(username, password)`` tuple.

    :param header: value of the ``Authorization`` header
    :raises InvalidHeaderFormat: on invalid inputs
    :raises InvalidHeaderValue: on unsupported inputs

    """
    scheme, pos = parse_tokenheader0'Authorization'
    if scheme.lower() != 'basic':
        raise InvalidHeaderValue('Authorization', f"unsupported scheme: {scheme}")
    if peek_ahead(header, pos) != ' ':
        raise InvalidHeaderFormat('Authorization', 'expected space after scheme', header, pos)
    pos += 1
    basic_credentials, pos = parse_token68headerpos'Authorization'
    parse_endheaderpos'Authorization'
    try:
        user_pass = base64.b64decode(basic_credentials.encode()).decode()
    except binascii.Error:
        raise InvalidHeaderValue('Authorization', 'expected base64-encoded credentials') from None
    else:
        try:
            username, password = user_pass.split(':', 1)
        except ValueError:
            raise InvalidHeaderValue('Authorization', 'expected username:password credentials') from None
        else:
            return (
             username, password)


def build_authorization_basic(username: str, password: str) -> str:
    """
    Build an ``Authorization`` header for HTTP Basic Auth.

    This is the reverse of :func:`parse_authorization_basic`.

    """
    assert ':' not in username
    user_pass = f"{username}:{password}"
    basic_credentials = base64.b64encode(user_pass.encode()).decode()
    return 'Basic ' + basic_credentials