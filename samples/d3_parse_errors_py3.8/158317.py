# decompyle3 version 3.7.5
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
            else:
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
                        else:
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
               52  POP_JUMP_IF_FALSE   242  'to 242'

 L. 149        54  LOAD_GLOBAL              max
               56  LOAD_GENEXPR             '<code_object <genexpr>>'
               58  LOAD_STR                 '_encode_text.<locals>.<genexpr>'
               60  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               62  LOAD_FAST                'lines'
               64  GET_ITER         
               66  CALL_FUNCTION_1       1  ''
               68  CALL_FUNCTION_1       1  ''
               70  LOAD_FAST                'policy'
               72  LOAD_ATTR                max_line_length
               74  COMPARE_OP               <=
               76  POP_JUMP_IF_FALSE   150  'to 150'

 L. 150        78  SETUP_FINALLY       100  'to 100'

 L. 151        80  LOAD_STR                 '7bit'
               82  LOAD_FAST                'normal_body'
               84  LOAD_FAST                'lines'
               86  CALL_FUNCTION_1       1  ''
               88  LOAD_METHOD              decode
               90  LOAD_STR                 'ascii'
               92  CALL_METHOD_1         1  ''
               94  BUILD_TUPLE_2         2 
               96  POP_BLOCK        
               98  RETURN_VALUE     
            100_0  COME_FROM_FINALLY    78  '78'

 L. 152       100  DUP_TOP          
              102  LOAD_GLOBAL              UnicodeDecodeError
              104  COMPARE_OP               exception-match
              106  POP_JUMP_IF_FALSE   118  'to 118'
              108  POP_TOP          
              110  POP_TOP          
              112  POP_TOP          

 L. 153       114  POP_EXCEPT       
              116  JUMP_FORWARD        120  'to 120'
            118_0  COME_FROM           106  '106'
              118  END_FINALLY      
            120_0  COME_FROM           116  '116'

 L. 154       120  LOAD_FAST                'policy'
              122  LOAD_ATTR                cte_type
              124  LOAD_STR                 '8bit'
              126  COMPARE_OP               ==
              128  POP_JUMP_IF_FALSE   150  'to 150'

 L. 155       130  LOAD_STR                 '8bit'
              132  LOAD_FAST                'normal_body'
              134  LOAD_FAST                'lines'
              136  CALL_FUNCTION_1       1  ''
              138  LOAD_METHOD              decode
              140  LOAD_STR                 'ascii'
              142  LOAD_STR                 'surrogateescape'
              144  CALL_METHOD_2         2  ''
              146  BUILD_TUPLE_2         2 
              148  RETURN_VALUE     
            150_0  COME_FROM           128  '128'
            150_1  COME_FROM            76  '76'

 L. 156       150  LOAD_FAST                'embedded_body'
              152  LOAD_FAST                'lines'
              154  LOAD_CONST               None
              156  LOAD_CONST               10
              158  BUILD_SLICE_2         2 
              160  BINARY_SUBSCR    
              162  CALL_FUNCTION_1       1  ''
              164  STORE_FAST               'sniff'

 L. 157       166  LOAD_GLOBAL              quoprimime
              168  LOAD_METHOD              body_encode
              170  LOAD_FAST                'sniff'
              172  LOAD_METHOD              decode
              174  LOAD_STR                 'latin-1'
              176  CALL_METHOD_1         1  ''

 L. 158       178  LOAD_FAST                'policy'
              180  LOAD_ATTR                max_line_length

 L. 157       182  CALL_METHOD_2         2  ''
              184  STORE_FAST               'sniff_qp'

 L. 159       186  LOAD_GLOBAL              binascii
              188  LOAD_METHOD              b2a_base64
              190  LOAD_FAST                'sniff'
              192  CALL_METHOD_1         1  ''
              194  STORE_FAST               'sniff_base64'

 L. 161       196  LOAD_GLOBAL              len
              198  LOAD_FAST                'sniff_qp'
              200  CALL_FUNCTION_1       1  ''
              202  LOAD_GLOBAL              len
              204  LOAD_FAST                'sniff_base64'
              206  CALL_FUNCTION_1       1  ''
              208  COMPARE_OP               >
              210  POP_JUMP_IF_FALSE   218  'to 218'

 L. 162       212  LOAD_STR                 'base64'
              214  STORE_FAST               'cte'
              216  JUMP_FORWARD        242  'to 242'
            218_0  COME_FROM           210  '210'

 L. 164       218  LOAD_STR                 'quoted-printable'
              220  STORE_FAST               'cte'

 L. 165       222  LOAD_GLOBAL              len
              224  LOAD_FAST                'lines'
              226  CALL_FUNCTION_1       1  ''
              228  LOAD_CONST               10
              230  COMPARE_OP               <=
              232  POP_JUMP_IF_FALSE   242  'to 242'

 L. 166       234  LOAD_FAST                'cte'
              236  LOAD_FAST                'sniff_qp'
              238  BUILD_TUPLE_2         2 
              240  RETURN_VALUE     
            242_0  COME_FROM           232  '232'
            242_1  COME_FROM           216  '216'
            242_2  COME_FROM            52  '52'

 L. 167       242  LOAD_FAST                'cte'
              244  LOAD_STR                 '7bit'
              246  COMPARE_OP               ==
          248_250  POP_JUMP_IF_FALSE   268  'to 268'

 L. 168       252  LOAD_FAST                'normal_body'
              254  LOAD_FAST                'lines'
              256  CALL_FUNCTION_1       1  ''
              258  LOAD_METHOD              decode
              260  LOAD_STR                 'ascii'
              262  CALL_METHOD_1         1  ''
              264  STORE_FAST               'data'
              266  JUMP_FORWARD        374  'to 374'
            268_0  COME_FROM           248  '248'

 L. 169       268  LOAD_FAST                'cte'
              270  LOAD_STR                 '8bit'
              272  COMPARE_OP               ==
          274_276  POP_JUMP_IF_FALSE   296  'to 296'

 L. 170       278  LOAD_FAST                'normal_body'
              280  LOAD_FAST                'lines'
              282  CALL_FUNCTION_1       1  ''
              284  LOAD_METHOD              decode
              286  LOAD_STR                 'ascii'
              288  LOAD_STR                 'surrogateescape'
              290  CALL_METHOD_2         2  ''
              292  STORE_FAST               'data'
              294  JUMP_FORWARD        374  'to 374'
            296_0  COME_FROM           274  '274'

 L. 171       296  LOAD_FAST                'cte'
              298  LOAD_STR                 'quoted-printable'
              300  COMPARE_OP               ==
          302_304  POP_JUMP_IF_FALSE   332  'to 332'

 L. 172       306  LOAD_GLOBAL              quoprimime
              308  LOAD_METHOD              body_encode
              310  LOAD_FAST                'normal_body'
              312  LOAD_FAST                'lines'
              314  CALL_FUNCTION_1       1  ''
              316  LOAD_METHOD              decode
              318  LOAD_STR                 'latin-1'
              320  CALL_METHOD_1         1  ''

 L. 173       322  LOAD_FAST                'policy'
              324  LOAD_ATTR                max_line_length

 L. 172       326  CALL_METHOD_2         2  ''
              328  STORE_FAST               'data'
              330  JUMP_FORWARD        374  'to 374'
            332_0  COME_FROM           302  '302'

 L. 174       332  LOAD_FAST                'cte'
              334  LOAD_STR                 'base64'
              336  COMPARE_OP               ==
          338_340  POP_JUMP_IF_FALSE   360  'to 360'

 L. 175       342  LOAD_GLOBAL              _encode_base64
              344  LOAD_FAST                'embedded_body'
              346  LOAD_FAST                'lines'
              348  CALL_FUNCTION_1       1  ''
              350  LOAD_FAST                'policy'
              352  LOAD_ATTR                max_line_length
              354  CALL_FUNCTION_2       2  ''
              356  STORE_FAST               'data'
              358  JUMP_FORWARD        374  'to 374'
            360_0  COME_FROM           338  '338'

 L. 177       360  LOAD_GLOBAL              ValueError
              362  LOAD_STR                 'Unknown content transfer encoding {}'
              364  LOAD_METHOD              format
              366  LOAD_FAST                'cte'
              368  CALL_METHOD_1         1  ''
              370  CALL_FUNCTION_1       1  ''
              372  RAISE_VARARGS_1       1  'exception instance'
            374_0  COME_FROM           358  '358'
            374_1  COME_FROM           330  '330'
            374_2  COME_FROM           294  '294'
            374_3  COME_FROM           266  '266'

 L. 178       374  LOAD_FAST                'cte'
              376  LOAD_FAST                'data'
              378  BUILD_TUPLE_2         2 
              380  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 118_0


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
            if subtype == 'rfc822':
                if cte not in (None, '7bit', '8bit', 'binary'):
                    raise ValueError('message/rfc822 parts do not support cte={}'.format(cte))
                cte = '8bit' if cte is None else cte
            elif subtype == 'external-body':
                if cte not in (None, '7bit'):
                    raise ValueError('message/external-body parts do not support cte={}'.format(cte))
                cte = '7bit'
            elif cte is None:
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
            elif cte == 'quoted-printable':
                data = binascii.b2a_qp(data, istext=False, header=False, quotetabs=True)
                data = data.decode('ascii')
            elif cte == '7bit':
                data.encode('ascii')
            elif cte in ('8bit', 'binary'):
                data = data.decode('ascii', 'surrogateescape')
            msg.set_payload(data)
            msg['Content-Transfer-Encoding'] = cte
            _finalize_set(msg, disposition, filename, cid, params)


        for typ in (bytes, bytearray, memoryview):
            raw_data_manager.add_set_handler(typ, set_bytes_content)