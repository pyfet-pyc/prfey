# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: xml\etree\ElementPath.py
import re
xpath_tokenizer_re = re.compile('(\'[^\']*\'|\\"[^\\"]*\\"|::|//?|\\.\\.|\\(\\)|[/.*:\\[\\]\\(\\)@=])|((?:\\{[^}]+\\})?[^/\\[\\]\\(\\)@=\\s]+)|\\s+')

def xpath_tokenizer(pattern, namespaces=None):
    default_namespace = namespaces.get('') if namespaces else None
    parsing_attribute = False
    for token in xpath_tokenizer_re.findall(pattern):
        ttype, tag = token
        if tag and tag[0] != '{':
            if ':' in tag:
                prefix, uri = tag.split(':', 1)
                try:
                    if not namespaces:
                        raise KeyError
                    yield (
                     ttype, '{%s}%s' % (namespaces[prefix], uri))
                except KeyError:
                    raise SyntaxError('prefix %r not found in prefix map' % prefix) from None

            elif default_namespace and not parsing_attribute:
                yield (
                 ttype, '{%s}%s' % (default_namespace, tag))
            else:
                yield token
            parsing_attribute = False
        else:
            yield token
            parsing_attribute = ttype == '@'


def get_parent_map(context):
    parent_map = context.parent_map
    if parent_map is None:
        context.parent_map = parent_map = {}
        for p in context.root.iter():
            for e in p:
                parent_map[e] = p

        return parent_map


def _is_wildcard_tag(tag):
    return tag[:3] == '{*}' or tag[-2:] == '}*'


def _prepare_tag(tag):
    _isinstance, _str = isinstance, str
    if tag == '{*}*':

        def select(context, result):
            for elem in result:
                if _isinstance(elem.tag, _str):
                    yield elem

    elif tag == '{}*':

        def select(context, result):
            for elem in result:
                el_tag = elem.tag
                if _isinstance(el_tag, _str):
                    if el_tag[0] != '{':
                        yield elem

    elif tag[:3] == '{*}':
        suffix = tag[2:]
        no_ns = slice(-len(suffix), None)
        tag = tag[3:]

        def select(context, result):
            for elem in result:
                el_tag = elem.tag
                if not el_tag == tag:
                    if _isinstance(el_tag, _str):
                        if el_tag[no_ns] == suffix:
                            pass
                yield elem

    elif tag[-2:] == '}*':
        ns = tag[:-1]
        ns_only = slice(None, len(ns))

        def select(context, result):
            for elem in result:
                el_tag = elem.tag
                if _isinstance(el_tag, _str):
                    if el_tag[ns_only] == ns:
                        yield elem

    else:
        raise RuntimeError(f"internal parser error, got {tag}")
    return select


def prepare_child(next, token):
    tag = token[1]
    if _is_wildcard_tag(tag):
        select_tag = _prepare_tag(tag)

        def select(context, result):

            def select_child(result):
                for elem in result:
                    yield from elem

                if False:
                    yield None

            return select_tag(context, select_child(result))

    else:
        if tag[:2] == '{}':
            tag = tag[2:]

        def select(context, result):
            for elem in result:
                for e in elem:
                    if e.tag == tag:
                        yield e

    return select


def prepare_star(next, token):

    def select(context, result):
        for elem in result:
            yield from elem

        if False:
            yield None

    return select


def prepare_self(next, token):

    def select(context, result):
        yield from result
        if False:
            yield None

    return select


def prepare_descendant(next, token):
    try:
        token = next()
    except StopIteration:
        return
    else:
        if token[0] == '*':
            tag = '*'
        elif not token[0]:
            tag = token[1]
        else:
            raise SyntaxError('invalid descendant')
        if _is_wildcard_tag(tag):
            select_tag = _prepare_tag(tag)

            def select(context, result):

                def select_child(result):
                    for elem in result:
                        for e in elem.iter():
                            if e is not elem:
                                yield e

                return select_tag(context, select_child(result))

        else:
            if tag[:2] == '{}':
                tag = tag[2:]

            def select(context, result):
                for elem in result:
                    for e in elem.iter(tag):
                        if e is not elem:
                            yield e

        return select


def prepare_parent(next, token):

    def select(context, result):
        parent_map = get_parent_map(context)
        result_map = {}
        for elem in result:
            if elem in parent_map:
                parent = parent_map[elem]
                if parent not in result_map:
                    result_map[parent] = None
                    yield parent

    return select


def prepare_predicate(next, token):
    signature = []
    predicate = []
    while True:
        try:
            token = next()
        except StopIteration:
            return
        else:
            if token[0] == ']':
                pass
            else:
                if token == ('', ''):
                    pass
                else:
                    if token[0]:
                        if token[0][:1] in '\'"':
                            token = (
                             "'", token[0][1:-1])
                    signature.append(token[0] or '-')
                    predicate.append(token[1])

    signature = ''.join(signature)
    if signature == '@-':
        key = predicate[1]

        def select(context, result):
            for elem in result:
                if elem.get(key) is not None:
                    yield elem

        return select
    if signature == "@-='":
        key = predicate[1]
        value = predicate[(-1)]

        def select(context, result):
            for elem in result:
                if elem.get(key) == value:
                    yield elem

        return select
    if signature == '-':
        if not re.match('\\-?\\d+$', predicate[0]):
            tag = predicate[0]

            def select(context, result):
                for elem in result:
                    if elem.find(tag) is not None:
                        yield elem

            return select
        if signature == ".='" or signature == "-='" and not re.match('\\-?\\d+$', predicate[0]):
            tag = predicate[0]
            value = predicate[(-1)]
            if tag:

                def select(context, result):
                    for elem in result:
                        for e in elem.findall(tag):
                            if ''.join(e.itertext()) == value:
                                yield elem
                                break

            else:

                def select(context, result):
                    for elem in result:
                        if ''.join(elem.itertext()) == value:
                            yield elem

            return select
        if signature == '-' or signature == '-()' or signature == '-()-':
            if signature == '-':
                index = int(predicate[0]) - 1
                if index < 0:
                    raise SyntaxError('XPath position >= 1 expected')
            else:
                if predicate[0] != 'last':
                    raise SyntaxError('unsupported function')
                if signature == '-()-':
                    try:
                        index = int(predicate[2]) - 1
                    except ValueError:
                        raise SyntaxError('unsupported expression')
                    else:
                        if index > -2:
                            raise SyntaxError('XPath offset from last() must be negative')
                else:
                    index = -1

            def select(context, result):
                parent_map = get_parent_map(context)
                for elem in result:
                    try:
                        parent = parent_map[elem]
                        elems = list(parent.findall(elem.tag))
                        if elems[index] is elem:
                            yield elem
                    except (IndexError, KeyError):
                        pass

            return select
    raise SyntaxError('invalid predicate')


ops = {'':prepare_child, 
 '*':prepare_star, 
 '.':prepare_self, 
 '..':prepare_parent, 
 '//':prepare_descendant, 
 '[':prepare_predicate}
_cache = {}

class _SelectorContext:
    parent_map = None

    def __init__(self, root):
        self.root = root


def iterfind--- This code section failed: ---

 L. 346         0  LOAD_FAST                'path'
                2  LOAD_CONST               -1
                4  LOAD_CONST               None
                6  BUILD_SLICE_2         2 
                8  BINARY_SUBSCR    
               10  LOAD_STR                 '/'
               12  COMPARE_OP               ==
               14  POP_JUMP_IF_FALSE    24  'to 24'

 L. 347        16  LOAD_FAST                'path'
               18  LOAD_STR                 '*'
               20  BINARY_ADD       
               22  STORE_FAST               'path'
             24_0  COME_FROM            14  '14'

 L. 349        24  LOAD_FAST                'path'
               26  BUILD_TUPLE_1         1 
               28  STORE_FAST               'cache_key'

 L. 350        30  LOAD_FAST                'namespaces'
               32  POP_JUMP_IF_FALSE    54  'to 54'

 L. 351        34  LOAD_FAST                'cache_key'
               36  LOAD_GLOBAL              tuple
               38  LOAD_GLOBAL              sorted
               40  LOAD_FAST                'namespaces'
               42  LOAD_METHOD              items
               44  CALL_METHOD_0         0  ''
               46  CALL_FUNCTION_1       1  ''
               48  CALL_FUNCTION_1       1  ''
               50  INPLACE_ADD      
               52  STORE_FAST               'cache_key'
             54_0  COME_FROM            32  '32'

 L. 353        54  SETUP_FINALLY        70  'to 70'

 L. 354        56  LOAD_GLOBAL              _cache
               58  LOAD_FAST                'cache_key'
               60  BINARY_SUBSCR    
               62  STORE_FAST               'selector'
               64  POP_BLOCK        
            66_68  JUMP_FORWARD        322  'to 322'
             70_0  COME_FROM_FINALLY    54  '54'

 L. 355        70  DUP_TOP          
               72  LOAD_GLOBAL              KeyError
               74  COMPARE_OP               exception-match
            76_78  POP_JUMP_IF_FALSE   320  'to 320'
               80  POP_TOP          
               82  POP_TOP          
               84  POP_TOP          

 L. 356        86  LOAD_GLOBAL              len
               88  LOAD_GLOBAL              _cache
               90  CALL_FUNCTION_1       1  ''
               92  LOAD_CONST               100
               94  COMPARE_OP               >
               96  POP_JUMP_IF_FALSE   106  'to 106'

 L. 357        98  LOAD_GLOBAL              _cache
              100  LOAD_METHOD              clear
              102  CALL_METHOD_0         0  ''
              104  POP_TOP          
            106_0  COME_FROM            96  '96'

 L. 358       106  LOAD_FAST                'path'
              108  LOAD_CONST               None
              110  LOAD_CONST               1
              112  BUILD_SLICE_2         2 
              114  BINARY_SUBSCR    
              116  LOAD_STR                 '/'
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_FALSE   130  'to 130'

 L. 359       122  LOAD_GLOBAL              SyntaxError
              124  LOAD_STR                 'cannot use absolute path on element'
              126  CALL_FUNCTION_1       1  ''
              128  RAISE_VARARGS_1       1  'exception instance'
            130_0  COME_FROM           120  '120'

 L. 360       130  LOAD_GLOBAL              iter
              132  LOAD_GLOBAL              xpath_tokenizer
              134  LOAD_FAST                'path'
              136  LOAD_FAST                'namespaces'
              138  CALL_FUNCTION_2       2  ''
              140  CALL_FUNCTION_1       1  ''
              142  LOAD_ATTR                __next__
              144  STORE_FAST               'next'

 L. 361       146  SETUP_FINALLY       158  'to 158'

 L. 362       148  LOAD_FAST                'next'
              150  CALL_FUNCTION_0       0  ''
              152  STORE_FAST               'token'
              154  POP_BLOCK        
              156  JUMP_FORWARD        182  'to 182'
            158_0  COME_FROM_FINALLY   146  '146'

 L. 363       158  DUP_TOP          
              160  LOAD_GLOBAL              StopIteration
              162  COMPARE_OP               exception-match
              164  POP_JUMP_IF_FALSE   180  'to 180'
              166  POP_TOP          
              168  POP_TOP          
              170  POP_TOP          

 L. 364       172  POP_EXCEPT       
              174  POP_EXCEPT       
              176  LOAD_CONST               None
              178  RETURN_VALUE     
            180_0  COME_FROM           164  '164'
              180  END_FINALLY      
            182_0  COME_FROM           156  '156'

 L. 365       182  BUILD_LIST_0          0 
              184  STORE_FAST               'selector'
            186_0  COME_FROM           306  '306'
            186_1  COME_FROM           302  '302'
            186_2  COME_FROM           276  '276'

 L. 367       186  SETUP_FINALLY       216  'to 216'

 L. 368       188  LOAD_FAST                'selector'
              190  LOAD_METHOD              append
              192  LOAD_GLOBAL              ops
              194  LOAD_FAST                'token'
              196  LOAD_CONST               0
              198  BINARY_SUBSCR    
              200  BINARY_SUBSCR    
              202  LOAD_FAST                'next'
              204  LOAD_FAST                'token'
              206  CALL_FUNCTION_2       2  ''
              208  CALL_METHOD_1         1  ''
              210  POP_TOP          
              212  POP_BLOCK        
              214  JUMP_FORWARD        246  'to 246'
            216_0  COME_FROM_FINALLY   186  '186'

 L. 369       216  DUP_TOP          
              218  LOAD_GLOBAL              StopIteration
              220  COMPARE_OP               exception-match
              222  POP_JUMP_IF_FALSE   244  'to 244'
              224  POP_TOP          
              226  POP_TOP          
              228  POP_TOP          

 L. 370       230  LOAD_GLOBAL              SyntaxError
              232  LOAD_STR                 'invalid path'
              234  CALL_FUNCTION_1       1  ''
              236  LOAD_CONST               None
              238  RAISE_VARARGS_2       2  'exception instance with __cause__'
              240  POP_EXCEPT       
              242  JUMP_FORWARD        246  'to 246'
            244_0  COME_FROM           222  '222'
              244  END_FINALLY      
            246_0  COME_FROM           242  '242'
            246_1  COME_FROM           214  '214'

 L. 371       246  SETUP_FINALLY       278  'to 278'

 L. 372       248  LOAD_FAST                'next'
              250  CALL_FUNCTION_0       0  ''
              252  STORE_FAST               'token'

 L. 373       254  LOAD_FAST                'token'
              256  LOAD_CONST               0
              258  BINARY_SUBSCR    
              260  LOAD_STR                 '/'
              262  COMPARE_OP               ==
          264_266  POP_JUMP_IF_FALSE   274  'to 274'

 L. 374       268  LOAD_FAST                'next'
              270  CALL_FUNCTION_0       0  ''
              272  STORE_FAST               'token'
            274_0  COME_FROM           264  '264'
              274  POP_BLOCK        
              276  JUMP_BACK           186  'to 186'
            278_0  COME_FROM_FINALLY   246  '246'

 L. 375       278  DUP_TOP          
              280  LOAD_GLOBAL              StopIteration
              282  COMPARE_OP               exception-match
          284_286  POP_JUMP_IF_FALSE   304  'to 304'
              288  POP_TOP          
              290  POP_TOP          
              292  POP_TOP          

 L. 376       294  POP_EXCEPT       
          296_298  BREAK_LOOP          308  'to 308'
              300  POP_EXCEPT       
              302  JUMP_BACK           186  'to 186'
            304_0  COME_FROM           284  '284'
              304  END_FINALLY      
              306  JUMP_BACK           186  'to 186'
            308_0  COME_FROM           296  '296'

 L. 377       308  LOAD_FAST                'selector'
              310  LOAD_GLOBAL              _cache
              312  LOAD_FAST                'cache_key'
              314  STORE_SUBSCR     
              316  POP_EXCEPT       
              318  JUMP_FORWARD        322  'to 322'
            320_0  COME_FROM            76  '76'
              320  END_FINALLY      
            322_0  COME_FROM           318  '318'
            322_1  COME_FROM            66  '66'

 L. 379       322  LOAD_FAST                'elem'
              324  BUILD_LIST_1          1 
              326  STORE_FAST               'result'

 L. 380       328  LOAD_GLOBAL              _SelectorContext
              330  LOAD_FAST                'elem'
              332  CALL_FUNCTION_1       1  ''
              334  STORE_FAST               'context'

 L. 381       336  LOAD_FAST                'selector'
              338  GET_ITER         
            340_0  COME_FROM           354  '354'
              340  FOR_ITER            358  'to 358'
              342  STORE_FAST               'select'

 L. 382       344  LOAD_FAST                'select'
              346  LOAD_FAST                'context'
              348  LOAD_FAST                'result'
              350  CALL_FUNCTION_2       2  ''
              352  STORE_FAST               'result'
          354_356  JUMP_BACK           340  'to 340'
            358_0  COME_FROM           340  '340'

 L. 383       358  LOAD_FAST                'result'
              360  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 176


def find(elem, path, namespaces=None):
    return next(iterfind(elem, path, namespaces), None)


def findall(elem, path, namespaces=None):
    return list(iterfind(elem, path, namespaces))


def findtext(elem, path, default=None, namespaces=None):
    try:
        elem = next(iterfind(elem, path, namespaces))
        return elem.text or ''
    except StopIteration:
        return default