# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: email\contentmanager.py
import binascii, email.charset, email.message, email.errors
from email import quoprimime

class ContentManager:

    def __init__(self):
        self.get_handlers = {}
        self.set_handlers = {}

    def add_get_handler(self, key, handler):
        self.get_handlers[key] = handler

    def get_content(self, msg, *args, **kw):
        content_type = msg.get_content_type()
        if content_type in self.get_handlers:
            return (self.get_handlers[content_type])(msg, *args, **kw)
        maintype = msg.get_content_maintype()
        if maintype in self.get_handlers:
            return (self.get_handlers[maintype])(msg, *args, **kw)
        if '' in self.get_handlers:
            return (self.get_handlers[''])(msg, *args, **kw)
        raise KeyError(content_type)

    def add_set_handler(self, typekey, handler):
        self.set_handlers[typekey] = handler

    def set_content(self, msg, obj, *args, **kw):
        if msg.get_content_maintype() == 'multipart':
            raise TypeError('set_content not valid on multipart')
        handler = self._find_set_handler(msg, obj)
        msg.clear_content()
        handler(msg, obj, *args, **kw)

    def _find_set_handler(self, msg, obj):
        full_path_for_error = None
        for typ in type(obj).__mro__:
            if typ in self.set_handlers:
                return self.set_handlers[typ]
            qname = typ.__qualname__
            modname = getattr(typ, '__module__', '')
            full_path = '.'.join((modname, qname)) if modname else qname
            if full_path_for_error is None:
                full_path_for_error = full_path
            if full_path in self.set_handlers:
                return self.set_handlers[full_path]
            if qname in self.set_handlers:
                return self.set_handlers[qname]
            name = typ.__name__
            if name in self.set_handlers:
                return self.set_handlers[name]
        else:
            if None in self.set_handlers:
                return self.set_handlers[None]
            raise KeyError(full_path_for_error)


raw_data_manager = ContentManager()

def get_text_content(msg, errors='replace'):
    content = msg.get_payload(decode=True)
    charset = msg.get_param('charset', 'ASCII')
    return content.decode(charset, errors=errors)


raw_data_manager.add_get_handler('text', get_text_content)

def get_non_text_content(msg):
    return msg.get_payload(decode=True)


for maintype in 'audio image video application'.split():
    raw_data_manager.add_get_handler(maintype, get_non_text_content)
else:

    def get_message_content(msg):
        return msg.get_payload(0)


    for subtype in 'rfc822 external-body'.split():
        raw_data_manager.add_get_handler('message/' + subtype, get_message_content)
    else:

        def get_and_fixup_unknown_message_content(msg):
            return bytes(msg.get_payload(0))


        raw_data_manager.add_get_handler('message', get_and_fixup_unknown_message_content)

        def _prepare_set(msg, maintype, subtype, headers):
            msg['Content-Type'] = '/'.join((maintype, subtype))
            if headers:
                if not hasattr(headers[0], 'name'):
                    mp = msg.policy
                    headers = [(mp.header_factory)(*mp.header_source_parse([header])) for header in headers]
                try:
                    for header in headers:
                        if header.defects:
                            raise header.defects[0]
                        msg[header.name] = header

                except email.errors.HeaderDefect as exc:
                    try:
                        raise ValueError('Invalid header: {}'.format(header.fold(policy=(msg.policy)))) from exc
                    finally:
                        exc = None
                        del exc


        def _finalize_set(msg, disposition, filename, cid, params):
            if disposition is None:
                if filename is not None:
                    disposition = 'attachment'
            else:
                if disposition is not None:
                    msg['Content-Disposition'] = disposition
                if filename is not None:
                    msg.set_param('filename', filename,
                      header='Content-Disposition',
                      replace=True)
                if cid is not None:
                    msg['Content-ID'] = cid
                if params is not None:
                    for key, value in params.items():
                        msg.set_param(key, value)


        def _encode_base64(data, max_line_length):
            encoded_lines = []
            unencoded_bytes_per_line = max_line_length // 4 * 3
            for i in range(0, len(data), unencoded_bytes_per_line):
                thisline = data[i:i + unencoded_bytes_per_line]
                encoded_lines.append(binascii.b2a_base64(thisline).decode('ascii'))
            else:
                return ''.join(encoded_lines)


        def _encode_text--- This code section failed: ---

 L. 143         0  LOAD_FAST                'string'
                2  LOAD_METHOD              encode
                4  LOAD_FAST                'charset'
                6  CALL_METHOD_1         1  ''
                8  LOAD_METHOD              splitlines
               10  CALL_METHOD_0         0  ''
               12  STORE_FAST               'lines'

 L. 144        14  LOAD_FAST                'policy'
               16  LOAD_ATTR                linesep
               18  LOAD_METHOD              encode
               20  LOAD_STR                 'ascii'
               22  CALL_METHOD_1         1  ''
               24  STORE_DEREF              'linesep'

 L. 145        26  LOAD_CLOSURE             'linesep'
               28  BUILD_TUPLE_1         1 
               30  LOAD_CODE                <code_object embedded_body>
               32  LOAD_STR                 '_encode_text.<locals>.embedded_body'
               34  MAKE_FUNCTION_8          'closure'
               36  STORE_FAST               'embedded_body'

 L. 146        38  LOAD_CODE                <code_object normal_body>
               40  LOAD_STR                 '_encode_text.<locals>.normal_body'
               42  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               44  STORE_FAST               'normal_body'

 L. 147        46  LOAD_FAST                'cte'
               48  LOAD_CONST               None
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE   246  'to 246'

 L. 149        54  LOAD_GLOBAL              max
               56  LOAD_GENEXPR             '<code_object <genexpr>>'
               58  LOAD_STR                 '_encode_text.<locals>.<genexpr>'
               60  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               62  LOAD_FAST                'lines'
               64  GET_ITER         
               66  CALL_FUNCTION_1       1  ''
               68  LOAD_CONST               0
               70  LOAD_CONST               ('default',)
               72  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               74  LOAD_FAST                'policy'
               76  LOAD_ATTR                max_line_length
               78  COMPARE_OP               <=
               80  POP_JUMP_IF_FALSE   154  'to 154'

 L. 150        82  SETUP_FINALLY       104  'to 104'

 L. 151        84  LOAD_STR                 '7bit'
               86  LOAD_FAST                'normal_body'
               88  LOAD_FAST                'lines'
               90  CALL_FUNCTION_1       1  ''
               92  LOAD_METHOD              decode
               94  LOAD_STR                 'ascii'
               96  CALL_METHOD_1         1  ''
               98  BUILD_TUPLE_2         2 
              100  POP_BLOCK        
              102  RETURN_VALUE     
            104_0  COME_FROM_FINALLY    82  '82'

 L. 152       104  DUP_TOP          
              106  LOAD_GLOBAL              UnicodeDecodeError
              108  COMPARE_OP               exception-match
              110  POP_JUMP_IF_FALSE   122  'to 122'
              112  POP_TOP          
              114  POP_TOP          
              116  POP_TOP          

 L. 153       118  POP_EXCEPT       
              120  JUMP_FORWARD        124  'to 124'
            122_0  COME_FROM           110  '110'
              122  END_FINALLY      
            124_0  COME_FROM           120  '120'

 L. 154       124  LOAD_FAST                'policy'
              126  LOAD_ATTR                cte_type
              128  LOAD_STR                 '8bit'
              130  COMPARE_OP               ==
              132  POP_JUMP_IF_FALSE   154  'to 154'

 L. 155       134  LOAD_STR                 '8bit'
              136  LOAD_FAST                'normal_body'
              138  LOAD_FAST                'lines'
              140  CALL_FUNCTION_1       1  ''
              142  LOAD_METHOD              decode
              144  LOAD_STR                 'ascii'
              146  LOAD_STR                 'surrogateescape'
              148  CALL_METHOD_2         2  ''
              150  BUILD_TUPLE_2         2 
              152  RETURN_VALUE     
            154_0  COME_FROM           132  '132'
            154_1  COME_FROM            80  '80'

 L. 156       154  LOAD_FAST                'embedded_body'
              156  LOAD_FAST                'lines'
              158  LOAD_CONST               None
              160  LOAD_CONST               10
              162  BUILD_SLICE_2         2 
              164  BINARY_SUBSCR    
              166  CALL_FUNCTION_1       1  ''
              168  STORE_FAST               'sniff'

 L. 157       170  LOAD_GLOBAL              quoprimime
              172  LOAD_METHOD              body_encode
              174  LOAD_FAST                'sniff'
              176  LOAD_METHOD              decode
              178  LOAD_STR                 'latin-1'
              180  CALL_METHOD_1         1  ''

 L. 158       182  LOAD_FAST                'policy'
              184  LOAD_ATTR                max_line_length

 L. 157       186  CALL_METHOD_2         2  ''
              188  STORE_FAST               'sniff_qp'

 L. 159       190  LOAD_GLOBAL              binascii
              192  LOAD_METHOD              b2a_base64
              194  LOAD_FAST                'sniff'
              196  CALL_METHOD_1         1  ''
              198  STORE_FAST               'sniff_base64'

 L. 161       200  LOAD_GLOBAL              len
              202  LOAD_FAST                'sniff_qp'
              204  CALL_FUNCTION_1       1  ''
              206  LOAD_GLOBAL              len
              208  LOAD_FAST                'sniff_base64'
              210  CALL_FUNCTION_1       1  ''
              212  COMPARE_OP               >
              214  POP_JUMP_IF_FALSE   222  'to 222'

 L. 162       216  LOAD_STR                 'base64'
              218  STORE_FAST               'cte'
              220  JUMP_FORWARD        246  'to 246'
            222_0  COME_FROM           214  '214'

 L. 164       222  LOAD_STR                 'quoted-printable'
              224  STORE_FAST               'cte'

 L. 165       226  LOAD_GLOBAL              len
              228  LOAD_FAST                'lines'
              230  CALL_FUNCTION_1       1  ''
              232  LOAD_CONST               10
              234  COMPARE_OP               <=
              236  POP_JUMP_IF_FALSE   246  'to 246'

 L. 166       238  LOAD_FAST                'cte'
              240  LOAD_FAST                'sniff_qp'
              242  BUILD_TUPLE_2         2 
              244  RETURN_VALUE     
            246_0  COME_FROM           236  '236'
            246_1  COME_FROM           220  '220'
            246_2  COME_FROM            52  '52'

 L. 167       246  LOAD_FAST                'cte'
              248  LOAD_STR                 '7bit'
              250  COMPARE_OP               ==
          252_254  POP_JUMP_IF_FALSE   272  'to 272'

 L. 168       256  LOAD_FAST                'normal_body'
              258  LOAD_FAST                'lines'
              260  CALL_FUNCTION_1       1  ''
              262  LOAD_METHOD              decode
              264  LOAD_STR                 'ascii'
              266  CALL_METHOD_1         1  ''
              268  STORE_FAST               'data'
              270  JUMP_FORWARD        378  'to 378'
            272_0  COME_FROM           252  '252'

 L. 169       272  LOAD_FAST                'cte'
              274  LOAD_STR                 '8bit'
              276  COMPARE_OP               ==
          278_280  POP_JUMP_IF_FALSE   300  'to 300'

 L. 170       282  LOAD_FAST                'normal_body'
              284  LOAD_FAST                'lines'
              286  CALL_FUNCTION_1       1  ''
              288  LOAD_METHOD              decode
              290  LOAD_STR                 'ascii'
              292  LOAD_STR                 'surrogateescape'
              294  CALL_METHOD_2         2  ''
              296  STORE_FAST               'data'
              298  JUMP_FORWARD        378  'to 378'
            300_0  COME_FROM           278  '278'

 L. 171       300  LOAD_FAST                'cte'
              302  LOAD_STR                 'quoted-printable'
              304  COMPARE_OP               ==
          306_308  POP_JUMP_IF_FALSE   336  'to 336'

 L. 172       310  LOAD_GLOBAL              quoprimime
              312  LOAD_METHOD              body_encode
              314  LOAD_FAST                'normal_body'
              316  LOAD_FAST                'lines'
              318  CALL_FUNCTION_1       1  ''
              320  LOAD_METHOD              decode
              322  LOAD_STR                 'latin-1'
              324  CALL_METHOD_1         1  ''

 L. 173       326  LOAD_FAST                'policy'
              328  LOAD_ATTR                max_line_length

 L. 172       330  CALL_METHOD_2         2  ''
              332  STORE_FAST               'data'
              334  JUMP_FORWARD        378  'to 378'
            336_0  COME_FROM           306  '306'

 L. 174       336  LOAD_FAST                'cte'
              338  LOAD_STR                 'base64'
              340  COMPARE_OP               ==
          342_344  POP_JUMP_IF_FALSE   364  'to 364'

 L. 175       346  LOAD_GLOBAL              _encode_base64
              348  LOAD_FAST                'embedded_body'
              350  LOAD_FAST                'lines'
              352  CALL_FUNCTION_1       1  ''
              354  LOAD_FAST                'policy'
              356  LOAD_ATTR                max_line_length
              358  CALL_FUNCTION_2       2  ''
              360  STORE_FAST               'data'
              362  JUMP_FORWARD        378  'to 378'
            364_0  COME_FROM           342  '342'

 L. 177       364  LOAD_GLOBAL              ValueError
              366  LOAD_STR                 'Unknown content transfer encoding {}'
              368  LOAD_METHOD              format
              370  LOAD_FAST                'cte'
              372  CALL_METHOD_1         1  ''
              374  CALL_FUNCTION_1       1  ''
              376  RAISE_VARARGS_1       1  'exception instance'
            378_0  COME_FROM           362  '362'
            378_1  COME_FROM           334  '334'
            378_2  COME_FROM           298  '298'
            378_3  COME_FROM           270  '270'

 L. 178       378  LOAD_FAST                'cte'
              380  LOAD_FAST                'data'
              382  BUILD_TUPLE_2         2 
              384  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 114


        def set_text_content(msg, string, subtype='plain', charset='utf-8', cte=None, disposition=None, filename=None, cid=None, params=None, headers=None):
            _prepare_set(msg, 'text', subtype, headers)
            cte, payload = _encode_text(string, charset, cte, msg.policy)
            msg.set_payload(payload)
            msg.set_param('charset', (email.charset.ALIASES.get(charset, charset)),
              replace=True)
            msg['Content-Transfer-Encoding'] = cte
            _finalize_set(msg, disposition, filename, cid, params)


        raw_data_manager.add_set_handler(str, set_text_content)

        def set_message_content(msg, message, subtype='rfc822', cte=None, disposition=None, filename=None, cid=None, params=None, headers=None):
            if subtype == 'partial':
                raise ValueError('message/partial is not supported for Message objects')
            elif subtype == 'rfc822':
                if cte not in (None, '7bit', '8bit', 'binary'):
                    raise ValueError('message/rfc822 parts do not support cte={}'.format(cte))
                cte = '8bit' if cte is None else cte
            else:
                if subtype == 'external-body':
                    if cte not in (None, '7bit'):
                        raise ValueError('message/external-body parts do not support cte={}'.format(cte))
                    cte = '7bit'
                else:
                    if cte is None:
                        cte = '7bit'
            _prepare_set(msg, 'message', subtype, headers)
            msg.set_payload([message])
            msg['Content-Transfer-Encoding'] = cte
            _finalize_set(msg, disposition, filename, cid, params)


        raw_data_manager.add_set_handler(email.message.Message, set_message_content)

        def set_bytes_content(msg, data, maintype, subtype, cte='base64', disposition=None, filename=None, cid=None, params=None, headers=None):
            _prepare_set(msg, maintype, subtype, headers)
            if cte == 'base64':
                data = _encode_base64(data, max_line_length=(msg.policy.max_line_length))
            else:
                if cte == 'quoted-printable':
                    data = binascii.b2a_qp(data, istext=False, header=False, quotetabs=True)
                    data = data.decode('ascii')
                else:
                    if cte == '7bit':
                        data.encode('ascii')
                    else:
                        if cte in ('8bit', 'binary'):
                            data = data.decode('ascii', 'surrogateescape')
            msg.set_payload(data)
            msg['Content-Transfer-Encoding'] = cte
            _finalize_set(msg, disposition, filename, cid, params)


        for typ in (bytes, bytearray, memoryview):
            raw_data_manager.add_set_handler(typ, set_bytes_content)