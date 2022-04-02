# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\youtube_dl\swfinterp.py
from __future__ import unicode_literals
import collections, io, zlib
from .compat import compat_str, compat_struct_unpack
from .utils import ExtractorError

def _extract_tags(file_contents):
    if file_contents[1:3] != b'WS':
        raise ExtractorError('Not an SWF file; header is %r' % file_contents[:3])
    elif file_contents[:1] == b'C':
        content = zlib.decompress(file_contents[8:])
    else:
        raise NotImplementedError('Unsupported compression format %r' % file_contents[:1])
    framesize_nbits = compat_struct_unpack('!B', content[:1])[0] >> 3
    framesize_len = (5 + 4 * framesize_nbits + 7) // 8
    pos = framesize_len + 2 + 2
    while pos < len(content):
        header16 = compat_struct_unpack('<H', content[pos:pos + 2])[0]
        pos += 2
        tag_code = header16 >> 6
        tag_len = header16 & 63
        if tag_len == 63:
            tag_len = compat_struct_unpack('<I', content[pos:pos + 4])[0]
            pos += 4
        assert pos + tag_len <= len(content), "Tag %d ends at %d+%d - that's longer than the file (%d)" % (
         tag_code, pos, tag_len, len(content))
        yield (tag_code, content[pos:pos + tag_len])
        pos += tag_len


class _AVMClass_Object(object):

    def __init__(self, avm_class):
        self.avm_class = avm_class

    def __repr__(self):
        return '%s#%x' % (self.avm_class.name, id(self))


class _ScopeDict(dict):

    def __init__(self, avm_class):
        super(_ScopeDict, self).__init__()
        self.avm_class = avm_class

    def __repr__(self):
        return '%s__Scope(%s)' % (
         self.avm_class.name,
         super(_ScopeDict, self).__repr__())


class _AVMClass(object):

    def __init__(self, name_idx, name, static_properties=None):
        self.name_idx = name_idx
        self.name = name
        self.method_names = {}
        self.method_idxs = {}
        self.methods = {}
        self.method_pyfunctions = {}
        self.static_properties = static_properties if static_properties else {}
        self.variables = _ScopeDict(self)
        self.constants = {}

    def make_object(self):
        return _AVMClass_Object(self)

    def __repr__(self):
        return '_AVMClass(%s)' % self.name

    def register_methods(self, methods):
        self.method_names.update(methods.items())
        self.method_idxs.update(dict(((idx, name) for name, idx in methods.items())))


class _Multiname(object):

    def __init__(self, kind):
        self.kind = kind

    def __repr__(self):
        return '[MULTINAME kind: 0x%x]' % self.kind


def _read_int(reader):
    res = 0
    shift = 0
    for _ in range(5):
        buf = reader.read(1)
        assert len(buf) == 1
        b = compat_struct_unpack('<B', buf)[0]
        res = res | (b & 127) << shift
        if b & 128 == 0:
            break
        shift += 7

    return res


def _u30(reader):
    res = _read_int(reader)
    assert res & 4026531840 == 0
    return res


_u32 = _read_int

def _s32(reader):
    v = _read_int(reader)
    if v & 2147483648 != 0:
        v = -((v ^ 4294967295) + 1)
    return v


def _s24(reader):
    bs = reader.read(3)
    assert len(bs) == 3
    last_byte = b'\xff' if ord(bs[2:3]) >= 128 else b'\x00'
    return compat_struct_unpack('<i', bs + last_byte)[0]


def _read_string(reader):
    slen = _u30(reader)
    resb = reader.read(slen)
    assert len(resb) == slen
    return resb.decode('utf-8')


def _read_bytes(count, reader):
    assert count >= 0
    resb = reader.read(count)
    assert len(resb) == count
    return resb


def _read_byte(reader):
    resb = _read_bytes(1, reader=reader)
    res = compat_struct_unpack('<B', resb)[0]
    return res


StringClass = _AVMClass('(no name idx)', 'String')
ByteArrayClass = _AVMClass('(no name idx)', 'ByteArray')
TimerClass = _AVMClass('(no name idx)', 'Timer')
TimerEventClass = _AVMClass('(no name idx)', 'TimerEvent', {'TIMER': 'timer'})
_builtin_classes = {StringClass.name: StringClass, 
 ByteArrayClass.name: ByteArrayClass, 
 TimerClass.name: TimerClass, 
 TimerEventClass.name: TimerEventClass}

class _Undefined(object):

    def __bool__(self):
        return False

    __nonzero__ = __bool__

    def __hash__(self):
        return 0

    def __str__(self):
        return 'undefined'

    __repr__ = __str__


undefined = _Undefined()

class SWFInterpreter(object):

    def __init__(self, file_contents):
        self._patched_functions = {(
 TimerClass, 'addEventListener'): lambda params: undefined}
        code_tag = next((tag for tag_code, tag in _extract_tags(file_contents) if tag_code == 82))
        p = code_tag.index(b'\x00', 4) + 1
        code_reader = io.BytesIO(code_tag[p:])
        u30 = lambda *args: _u30(*args, **{'reader': code_reader})
        s32 = lambda *args: _s32(*args, **{'reader': code_reader})
        u32 = lambda *args: _u32(*args, **{'reader': code_reader})
        read_bytes = lambda *args: _read_bytes(*args, **{'reader': code_reader})
        read_byte = lambda *args: _read_byte(*args, **{'reader': code_reader})
        read_bytes(4)
        int_count = u30()
        self.constant_ints = [0]
        for _c in range(1, int_count):
            self.constant_ints.append(s32())

        self.constant_uints = [
         0]
        uint_count = u30()
        for _c in range(1, uint_count):
            self.constant_uints.append(u32())

        double_count = u30()
        read_bytes(max(0, double_count - 1) * 8)
        string_count = u30()
        self.constant_strings = ['']
        for _c in range(1, string_count):
            s = _read_string(code_reader)
            self.constant_strings.append(s)

        namespace_count = u30()
        for _c in range(1, namespace_count):
            read_bytes(1)
            u30()

        ns_set_count = u30()
        for _c in range(1, ns_set_count):
            count = u30()
            for _c2 in range(count):
                u30()

        multiname_count = u30()
        MULTINAME_SIZES = {7:2, 
         13:2, 
         15:1, 
         16:1, 
         17:0, 
         18:0, 
         9:2, 
         14:2, 
         27:1, 
         28:1}
        self.multinames = [
         '']
        for _c in range(1, multiname_count):
            kind = u30()
            assert kind in MULTINAME_SIZES, 'Invalid multiname kind %r' % kind
            if kind == 7:
                u30()
                name_idx = u30()
                self.multinames.append(self.constant_strings[name_idx])
            elif kind == 9:
                name_idx = u30()
                u30()
                self.multinames.append(self.constant_strings[name_idx])
            else:
                self.multinames.append(_Multiname(kind))
                for _c2 in range(MULTINAME_SIZES[kind]):
                    u30()

        method_count = u30()
        MethodInfo = collections.namedtuple('MethodInfo', [
         'NEED_ARGUMENTS', 'NEED_REST'])
        method_infos = []
        for method_id in range(method_count):
            param_count = u30()
            u30()
            for _ in range(param_count):
                u30()

            u30()
            flags = read_byte()
            if flags & 8 != 0:
                option_count = u30()
                for c in range(option_count):
                    u30()
                    read_bytes(1)

            if flags & 128 != 0:
                for _ in range(param_count):
                    u30()

            mi = MethodInfo(flags & 1 != 0, flags & 4 != 0)
            method_infos.append(mi)

        metadata_count = u30()
        for _c in range(metadata_count):
            u30()
            item_count = u30()
            for _c2 in range(item_count):
                u30()
                u30()

        def parse_traits_info():
            trait_name_idx = u30()
            kind_full = read_byte()
            kind = kind_full & 15
            attrs = kind_full >> 4
            methods = {}
            constants = None
            if kind == 0:
                u30()
                u30()
                vindex = u30()
                if vindex != 0:
                    read_byte()
            else:
                if kind == 6:
                    u30()
                    u30()
                    vindex = u30()
                    vkind = 'any'
                    if vindex != 0:
                        vkind = read_byte()
                    elif vkind == 3:
                        value = self.constant_ints[vindex]
                    else:
                        if vkind == 4:
                            value = self.constant_uints[vindex]
                        else:
                            return ({}, None)
                    constants = {self.multinames[trait_name_idx]: value}
                else:
                    if kind in (1, 2, 3):
                        u30()
                        method_idx = u30()
                        methods[self.multinames[trait_name_idx]] = method_idx
                    else:
                        if kind == 4:
                            u30()
                            u30()
                        else:
                            if kind == 5:
                                u30()
                                function_idx = u30()
                                methods[function_idx] = self.multinames[trait_name_idx]
                            else:
                                raise ExtractorError('Unsupported trait kind %d' % kind)
            if attrs & 4 != 0:
                metadata_count = u30()
                for _c3 in range(metadata_count):
                    u30()

            return (
             methods, constants)

        class_count = u30()
        classes = []
        for class_id in range(class_count):
            name_idx = u30()
            cname = self.multinames[name_idx]
            avm_class = _AVMClass(name_idx, cname)
            classes.append(avm_class)
            u30()
            flags = read_byte()
            if flags & 8 != 0:
                u30()
            intrf_count = u30()
            for _c2 in range(intrf_count):
                u30()

            u30()
            trait_count = u30()
            for _c2 in range(trait_count):
                trait_methods, trait_constants = parse_traits_info()
                avm_class.register_methods(trait_methods)
                if trait_constants:
                    avm_class.constants.update(trait_constants)

        assert len(classes) == class_count
        self._classes_by_name = dict(((c.name, c) for c in classes))
        for avm_class in classes:
            avm_class.cinit_idx = u30()
            trait_count = u30()
            for _c2 in range(trait_count):
                trait_methods, trait_constants = parse_traits_info()
                avm_class.register_methods(trait_methods)
                if trait_constants:
                    avm_class.constants.update(trait_constants)

        script_count = u30()
        for _c in range(script_count):
            u30()
            trait_count = u30()
            for _c2 in range(trait_count):
                parse_traits_info()

        method_body_count = u30()
        Method = collections.namedtuple('Method', ['code', 'local_count'])
        self._all_methods = []
        for _c in range(method_body_count):
            method_idx = u30()
            u30()
            local_count = u30()
            u30()
            u30()
            code_length = u30()
            code = read_bytes(code_length)
            m = Method(code, local_count)
            self._all_methods.append(m)
            for avm_class in classes:
                if method_idx in avm_class.method_idxs:
                    avm_class.methods[avm_class.method_idxs[method_idx]] = m

            exception_count = u30()
            for _c2 in range(exception_count):
                u30()
                u30()
                u30()
                u30()
                u30()

            trait_count = u30()
            for _c2 in range(trait_count):
                parse_traits_info()

        assert p + code_reader.tell() == len(code_tag)

    def patch_function(self, avm_class, func_name, f):
        self._patched_functions[(avm_class, func_name)] = f

    def extract_class(self, class_name, call_cinit=True):
        try:
            res = self._classes_by_name[class_name]
        except KeyError:
            raise ExtractorError('Class %r not found' % class_name)

        if call_cinit:
            if hasattr(res, 'cinit_idx'):
                res.register_methods({'$cinit': res.cinit_idx})
                res.methods['$cinit'] = self._all_methods[res.cinit_idx]
                cinit = self.extract_function(res, '$cinit')
                cinit([])
        return res

    def extract_function(self, avm_class, func_name):
        p = self._patched_functions.get((avm_class, func_name))
        if p:
            return p
        if func_name in avm_class.method_pyfunctions:
            return avm_class.method_pyfunctions[func_name]
        if func_name in self._classes_by_name:
            return self._classes_by_name[func_name].make_object()
        if func_name not in avm_class.methods:
            raise ExtractorError('Cannot find function %s.%s' % (
             avm_class.name, func_name))
        m = avm_class.methods[func_name]

        def resfunc--- This code section failed: ---

 L. 453         0  LOAD_GLOBAL              io
                2  LOAD_METHOD              BytesIO
                4  LOAD_DEREF               'm'
                6  LOAD_ATTR                code
                8  CALL_METHOD_1         1  '1 positional argument'
               10  STORE_DEREF              'coder'

 L. 454        12  LOAD_CLOSURE             'coder'
               14  BUILD_TUPLE_1         1 
               16  LOAD_LAMBDA              '<code_object <lambda>>'
               18  LOAD_STR                 'SWFInterpreter.extract_function.<locals>.resfunc.<locals>.<lambda>'
               20  MAKE_FUNCTION_8          'closure'
               22  STORE_FAST               's24'

 L. 455        24  LOAD_CLOSURE             'coder'
               26  BUILD_TUPLE_1         1 
               28  LOAD_LAMBDA              '<code_object <lambda>>'
               30  LOAD_STR                 'SWFInterpreter.extract_function.<locals>.resfunc.<locals>.<lambda>'
               32  MAKE_FUNCTION_8          'closure'
               34  STORE_FAST               'u30'

 L. 457        36  LOAD_DEREF               'avm_class'
               38  LOAD_ATTR                variables
               40  BUILD_LIST_1          1 
               42  LOAD_GLOBAL              list
               44  LOAD_FAST                'args'
               46  CALL_FUNCTION_1       1  '1 positional argument'
               48  BINARY_ADD       
               50  LOAD_CONST               None
               52  BUILD_LIST_1          1 
               54  LOAD_DEREF               'm'
               56  LOAD_ATTR                local_count
               58  BINARY_MULTIPLY  
               60  BINARY_ADD       
               62  STORE_FAST               'registers'

 L. 458        64  BUILD_LIST_0          0 
               66  STORE_DEREF              'stack'

 L. 459        68  LOAD_GLOBAL              collections
               70  LOAD_METHOD              deque

 L. 460        72  LOAD_DEREF               'self'
               74  LOAD_ATTR                _classes_by_name
               76  LOAD_DEREF               'avm_class'
               78  LOAD_ATTR                constants
               80  LOAD_DEREF               'avm_class'
               82  LOAD_ATTR                variables
               84  BUILD_LIST_3          3 
               86  CALL_METHOD_1         1  '1 positional argument'
               88  STORE_FAST               'scopes'

 L. 461     90_92  SETUP_LOOP         3672  'to 3672'
             94_0  COME_FROM          1898  '1898'
             94_1  COME_FROM          1832  '1832'

 L. 462        94  LOAD_GLOBAL              _read_byte
               96  LOAD_DEREF               'coder'
               98  CALL_FUNCTION_1       1  '1 positional argument'
              100  STORE_FAST               'opcode'

 L. 463       102  LOAD_FAST                'opcode'
              104  LOAD_CONST               9
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_FALSE   112  'to 112'

 L. 464       110  CONTINUE             94  'to 94'
            112_0  COME_FROM           108  '108'

 L. 465       112  LOAD_FAST                'opcode'
              114  LOAD_CONST               16
              116  COMPARE_OP               ==
              118  POP_JUMP_IF_FALSE   146  'to 146'

 L. 466       120  LOAD_FAST                's24'
              122  CALL_FUNCTION_0       0  '0 positional arguments'
              124  STORE_FAST               'offset'

 L. 467       126  LOAD_DEREF               'coder'
              128  LOAD_METHOD              seek
              130  LOAD_DEREF               'coder'
              132  LOAD_METHOD              tell
              134  CALL_METHOD_0         0  '0 positional arguments'
              136  LOAD_FAST                'offset'
              138  BINARY_ADD       
              140  CALL_METHOD_1         1  '1 positional argument'
              142  POP_TOP          
              144  JUMP_BACK            94  'to 94'
            146_0  COME_FROM           118  '118'

 L. 468       146  LOAD_FAST                'opcode'
              148  LOAD_CONST               17
              150  COMPARE_OP               ==
              152  POP_JUMP_IF_FALSE   192  'to 192'

 L. 469       154  LOAD_FAST                's24'
              156  CALL_FUNCTION_0       0  '0 positional arguments'
              158  STORE_FAST               'offset'

 L. 470       160  LOAD_DEREF               'stack'
              162  LOAD_METHOD              pop
              164  CALL_METHOD_0         0  '0 positional arguments'
              166  STORE_FAST               'value'

 L. 471       168  LOAD_FAST                'value'
              170  POP_JUMP_IF_FALSE   190  'to 190'

 L. 472       172  LOAD_DEREF               'coder'
              174  LOAD_METHOD              seek
              176  LOAD_DEREF               'coder'
              178  LOAD_METHOD              tell
              180  CALL_METHOD_0         0  '0 positional arguments'
              182  LOAD_FAST                'offset'
              184  BINARY_ADD       
              186  CALL_METHOD_1         1  '1 positional argument'
              188  POP_TOP          
            190_0  COME_FROM           170  '170'
              190  JUMP_BACK            94  'to 94'
            192_0  COME_FROM           152  '152'

 L. 473       192  LOAD_FAST                'opcode'
              194  LOAD_CONST               18
              196  COMPARE_OP               ==
              198  POP_JUMP_IF_FALSE   238  'to 238'

 L. 474       200  LOAD_FAST                's24'
              202  CALL_FUNCTION_0       0  '0 positional arguments'
              204  STORE_FAST               'offset'

 L. 475       206  LOAD_DEREF               'stack'
              208  LOAD_METHOD              pop
              210  CALL_METHOD_0         0  '0 positional arguments'
              212  STORE_FAST               'value'

 L. 476       214  LOAD_FAST                'value'
              216  POP_JUMP_IF_TRUE    236  'to 236'

 L. 477       218  LOAD_DEREF               'coder'
              220  LOAD_METHOD              seek
              222  LOAD_DEREF               'coder'
              224  LOAD_METHOD              tell
              226  CALL_METHOD_0         0  '0 positional arguments'
              228  LOAD_FAST                'offset'
              230  BINARY_ADD       
              232  CALL_METHOD_1         1  '1 positional argument'
              234  POP_TOP          
            236_0  COME_FROM           216  '216'
              236  JUMP_BACK            94  'to 94'
            238_0  COME_FROM           198  '198'

 L. 478       238  LOAD_FAST                'opcode'
              240  LOAD_CONST               19
              242  COMPARE_OP               ==
          244_246  POP_JUMP_IF_FALSE   300  'to 300'

 L. 479       248  LOAD_FAST                's24'
              250  CALL_FUNCTION_0       0  '0 positional arguments'
              252  STORE_FAST               'offset'

 L. 480       254  LOAD_DEREF               'stack'
              256  LOAD_METHOD              pop
              258  CALL_METHOD_0         0  '0 positional arguments'
              260  STORE_FAST               'value2'

 L. 481       262  LOAD_DEREF               'stack'
              264  LOAD_METHOD              pop
              266  CALL_METHOD_0         0  '0 positional arguments'
              268  STORE_FAST               'value1'

 L. 482       270  LOAD_FAST                'value2'
              272  LOAD_FAST                'value1'
              274  COMPARE_OP               ==
          276_278  POP_JUMP_IF_FALSE  3668  'to 3668'

 L. 483       280  LOAD_DEREF               'coder'
              282  LOAD_METHOD              seek
              284  LOAD_DEREF               'coder'
              286  LOAD_METHOD              tell
              288  CALL_METHOD_0         0  '0 positional arguments'
              290  LOAD_FAST                'offset'
              292  BINARY_ADD       
              294  CALL_METHOD_1         1  '1 positional argument'
              296  POP_TOP          
              298  JUMP_BACK            94  'to 94'
            300_0  COME_FROM           244  '244'

 L. 484       300  LOAD_FAST                'opcode'
              302  LOAD_CONST               20
              304  COMPARE_OP               ==
          306_308  POP_JUMP_IF_FALSE   362  'to 362'

 L. 485       310  LOAD_FAST                's24'
              312  CALL_FUNCTION_0       0  '0 positional arguments'
              314  STORE_FAST               'offset'

 L. 486       316  LOAD_DEREF               'stack'
              318  LOAD_METHOD              pop
              320  CALL_METHOD_0         0  '0 positional arguments'
              322  STORE_FAST               'value2'

 L. 487       324  LOAD_DEREF               'stack'
              326  LOAD_METHOD              pop
              328  CALL_METHOD_0         0  '0 positional arguments'
              330  STORE_FAST               'value1'

 L. 488       332  LOAD_FAST                'value2'
              334  LOAD_FAST                'value1'
              336  COMPARE_OP               !=
          338_340  POP_JUMP_IF_FALSE  3668  'to 3668'

 L. 489       342  LOAD_DEREF               'coder'
              344  LOAD_METHOD              seek
              346  LOAD_DEREF               'coder'
              348  LOAD_METHOD              tell
              350  CALL_METHOD_0         0  '0 positional arguments'
              352  LOAD_FAST                'offset'
              354  BINARY_ADD       
              356  CALL_METHOD_1         1  '1 positional argument'
              358  POP_TOP          
              360  JUMP_BACK            94  'to 94'
            362_0  COME_FROM           306  '306'

 L. 490       362  LOAD_FAST                'opcode'
              364  LOAD_CONST               21
              366  COMPARE_OP               ==
          368_370  POP_JUMP_IF_FALSE   424  'to 424'

 L. 491       372  LOAD_FAST                's24'
              374  CALL_FUNCTION_0       0  '0 positional arguments'
              376  STORE_FAST               'offset'

 L. 492       378  LOAD_DEREF               'stack'
              380  LOAD_METHOD              pop
              382  CALL_METHOD_0         0  '0 positional arguments'
              384  STORE_FAST               'value2'

 L. 493       386  LOAD_DEREF               'stack'
              388  LOAD_METHOD              pop
              390  CALL_METHOD_0         0  '0 positional arguments'
              392  STORE_FAST               'value1'

 L. 494       394  LOAD_FAST                'value1'
              396  LOAD_FAST                'value2'
              398  COMPARE_OP               <
          400_402  POP_JUMP_IF_FALSE  3668  'to 3668'

 L. 495       404  LOAD_DEREF               'coder'
              406  LOAD_METHOD              seek
              408  LOAD_DEREF               'coder'
              410  LOAD_METHOD              tell
              412  CALL_METHOD_0         0  '0 positional arguments'
              414  LOAD_FAST                'offset'
              416  BINARY_ADD       
              418  CALL_METHOD_1         1  '1 positional argument'
              420  POP_TOP          
              422  JUMP_BACK            94  'to 94'
            424_0  COME_FROM           368  '368'

 L. 496       424  LOAD_FAST                'opcode'
              426  LOAD_CONST               32
              428  COMPARE_OP               ==
          430_432  POP_JUMP_IF_FALSE   446  'to 446'

 L. 497       434  LOAD_DEREF               'stack'
              436  LOAD_METHOD              append
              438  LOAD_CONST               None
              440  CALL_METHOD_1         1  '1 positional argument'
              442  POP_TOP          
              444  JUMP_BACK            94  'to 94'
            446_0  COME_FROM           430  '430'

 L. 498       446  LOAD_FAST                'opcode'
              448  LOAD_CONST               33
              450  COMPARE_OP               ==
          452_454  POP_JUMP_IF_FALSE   468  'to 468'

 L. 499       456  LOAD_DEREF               'stack'
              458  LOAD_METHOD              append
              460  LOAD_GLOBAL              undefined
              462  CALL_METHOD_1         1  '1 positional argument'
              464  POP_TOP          
              466  JUMP_BACK            94  'to 94'
            468_0  COME_FROM           452  '452'

 L. 500       468  LOAD_FAST                'opcode'
              470  LOAD_CONST               36
              472  COMPARE_OP               ==
          474_476  POP_JUMP_IF_FALSE   498  'to 498'

 L. 501       478  LOAD_GLOBAL              _read_byte
              480  LOAD_DEREF               'coder'
              482  CALL_FUNCTION_1       1  '1 positional argument'
              484  STORE_FAST               'v'

 L. 502       486  LOAD_DEREF               'stack'
              488  LOAD_METHOD              append
              490  LOAD_FAST                'v'
              492  CALL_METHOD_1         1  '1 positional argument'
              494  POP_TOP          
              496  JUMP_BACK            94  'to 94'
            498_0  COME_FROM           474  '474'

 L. 503       498  LOAD_FAST                'opcode'
              500  LOAD_CONST               37
              502  COMPARE_OP               ==
          504_506  POP_JUMP_IF_FALSE   526  'to 526'

 L. 504       508  LOAD_FAST                'u30'
              510  CALL_FUNCTION_0       0  '0 positional arguments'
              512  STORE_FAST               'v'

 L. 505       514  LOAD_DEREF               'stack'
              516  LOAD_METHOD              append
              518  LOAD_FAST                'v'
              520  CALL_METHOD_1         1  '1 positional argument'
              522  POP_TOP          
              524  JUMP_BACK            94  'to 94'
            526_0  COME_FROM           504  '504'

 L. 506       526  LOAD_FAST                'opcode'
              528  LOAD_CONST               38
              530  COMPARE_OP               ==
          532_534  POP_JUMP_IF_FALSE   548  'to 548'

 L. 507       536  LOAD_DEREF               'stack'
              538  LOAD_METHOD              append
              540  LOAD_CONST               True
              542  CALL_METHOD_1         1  '1 positional argument'
              544  POP_TOP          
              546  JUMP_BACK            94  'to 94'
            548_0  COME_FROM           532  '532'

 L. 508       548  LOAD_FAST                'opcode'
              550  LOAD_CONST               39
              552  COMPARE_OP               ==
          554_556  POP_JUMP_IF_FALSE   570  'to 570'

 L. 509       558  LOAD_DEREF               'stack'
              560  LOAD_METHOD              append
              562  LOAD_CONST               False
              564  CALL_METHOD_1         1  '1 positional argument'
              566  POP_TOP          
              568  JUMP_BACK            94  'to 94'
            570_0  COME_FROM           554  '554'

 L. 510       570  LOAD_FAST                'opcode'
              572  LOAD_CONST               40
              574  COMPARE_OP               ==
          576_578  POP_JUMP_IF_FALSE   596  'to 596'

 L. 511       580  LOAD_DEREF               'stack'
              582  LOAD_METHOD              append
              584  LOAD_GLOBAL              float
              586  LOAD_STR                 'NaN'
              588  CALL_FUNCTION_1       1  '1 positional argument'
              590  CALL_METHOD_1         1  '1 positional argument'
              592  POP_TOP          
              594  JUMP_BACK            94  'to 94'
            596_0  COME_FROM           576  '576'

 L. 512       596  LOAD_FAST                'opcode'
              598  LOAD_CONST               42
              600  COMPARE_OP               ==
          602_604  POP_JUMP_IF_FALSE   626  'to 626'

 L. 513       606  LOAD_DEREF               'stack'
              608  LOAD_CONST               -1
              610  BINARY_SUBSCR    
              612  STORE_FAST               'value'

 L. 514       614  LOAD_DEREF               'stack'
              616  LOAD_METHOD              append
              618  LOAD_FAST                'value'
              620  CALL_METHOD_1         1  '1 positional argument'
              622  POP_TOP          
              624  JUMP_BACK            94  'to 94'
            626_0  COME_FROM           602  '602'

 L. 515       626  LOAD_FAST                'opcode'
              628  LOAD_CONST               44
              630  COMPARE_OP               ==
          632_634  POP_JUMP_IF_FALSE   660  'to 660'

 L. 516       636  LOAD_FAST                'u30'
              638  CALL_FUNCTION_0       0  '0 positional arguments'
              640  STORE_FAST               'idx'

 L. 517       642  LOAD_DEREF               'stack'
              644  LOAD_METHOD              append
              646  LOAD_DEREF               'self'
              648  LOAD_ATTR                constant_strings
              650  LOAD_FAST                'idx'
              652  BINARY_SUBSCR    
              654  CALL_METHOD_1         1  '1 positional argument'
              656  POP_TOP          
              658  JUMP_BACK            94  'to 94'
            660_0  COME_FROM           632  '632'

 L. 518       660  LOAD_FAST                'opcode'
              662  LOAD_CONST               48
              664  COMPARE_OP               ==
          666_668  POP_JUMP_IF_FALSE   690  'to 690'

 L. 519       670  LOAD_DEREF               'stack'
              672  LOAD_METHOD              pop
              674  CALL_METHOD_0         0  '0 positional arguments'
              676  STORE_FAST               'new_scope'

 L. 520       678  LOAD_FAST                'scopes'
              680  LOAD_METHOD              append
              682  LOAD_FAST                'new_scope'
              684  CALL_METHOD_1         1  '1 positional argument'
              686  POP_TOP          
              688  JUMP_BACK            94  'to 94'
            690_0  COME_FROM           666  '666'

 L. 521       690  LOAD_FAST                'opcode'
              692  LOAD_CONST               66
              694  COMPARE_OP               ==
          696_698  POP_JUMP_IF_FALSE   766  'to 766'

 L. 522       700  LOAD_FAST                'u30'
              702  CALL_FUNCTION_0       0  '0 positional arguments'
              704  STORE_FAST               'arg_count'

 L. 523       706  LOAD_GLOBAL              list
              708  LOAD_GLOBAL              reversed

 L. 524       710  LOAD_CLOSURE             'stack'
              712  BUILD_TUPLE_1         1 
              714  LOAD_LISTCOMP            '<code_object <listcomp>>'
              716  LOAD_STR                 'SWFInterpreter.extract_function.<locals>.resfunc.<locals>.<listcomp>'
              718  MAKE_FUNCTION_8          'closure'
              720  LOAD_GLOBAL              range
              722  LOAD_FAST                'arg_count'
              724  CALL_FUNCTION_1       1  '1 positional argument'
              726  GET_ITER         
              728  CALL_FUNCTION_1       1  '1 positional argument'
              730  CALL_FUNCTION_1       1  '1 positional argument'
              732  CALL_FUNCTION_1       1  '1 positional argument'
              734  STORE_FAST               'args'

 L. 525       736  LOAD_DEREF               'stack'
              738  LOAD_METHOD              pop
              740  CALL_METHOD_0         0  '0 positional arguments'
              742  STORE_FAST               'obj'

 L. 526       744  LOAD_FAST                'obj'
              746  LOAD_ATTR                avm_class
              748  LOAD_METHOD              make_object
              750  CALL_METHOD_0         0  '0 positional arguments'
              752  STORE_FAST               'res'

 L. 527       754  LOAD_DEREF               'stack'
              756  LOAD_METHOD              append
              758  LOAD_FAST                'res'
              760  CALL_METHOD_1         1  '1 positional argument'
              762  POP_TOP          
              764  JUMP_BACK            94  'to 94'
            766_0  COME_FROM           696  '696'

 L. 528       766  LOAD_FAST                'opcode'
              768  LOAD_CONST               70
              770  COMPARE_OP               ==
          772_774  POP_JUMP_IF_FALSE  1524  'to 1524'

 L. 529       776  LOAD_FAST                'u30'
              778  CALL_FUNCTION_0       0  '0 positional arguments'
              780  STORE_FAST               'index'

 L. 530       782  LOAD_DEREF               'self'
              784  LOAD_ATTR                multinames
              786  LOAD_FAST                'index'
              788  BINARY_SUBSCR    
              790  STORE_FAST               'mname'

 L. 531       792  LOAD_FAST                'u30'
              794  CALL_FUNCTION_0       0  '0 positional arguments'
              796  STORE_FAST               'arg_count'

 L. 532       798  LOAD_GLOBAL              list
              800  LOAD_GLOBAL              reversed

 L. 533       802  LOAD_CLOSURE             'stack'
              804  BUILD_TUPLE_1         1 
              806  LOAD_LISTCOMP            '<code_object <listcomp>>'
              808  LOAD_STR                 'SWFInterpreter.extract_function.<locals>.resfunc.<locals>.<listcomp>'
              810  MAKE_FUNCTION_8          'closure'
              812  LOAD_GLOBAL              range
              814  LOAD_FAST                'arg_count'
              816  CALL_FUNCTION_1       1  '1 positional argument'
              818  GET_ITER         
              820  CALL_FUNCTION_1       1  '1 positional argument'
              822  CALL_FUNCTION_1       1  '1 positional argument'
              824  CALL_FUNCTION_1       1  '1 positional argument'
              826  STORE_FAST               'args'

 L. 534       828  LOAD_DEREF               'stack'
              830  LOAD_METHOD              pop
              832  CALL_METHOD_0         0  '0 positional arguments'
              834  STORE_FAST               'obj'

 L. 536       836  LOAD_FAST                'obj'
              838  LOAD_GLOBAL              StringClass
              840  COMPARE_OP               ==
          842_844  POP_JUMP_IF_FALSE   962  'to 962'

 L. 537       846  LOAD_FAST                'mname'
              848  LOAD_STR                 'String'
              850  COMPARE_OP               ==
          852_854  POP_JUMP_IF_FALSE   946  'to 946'

 L. 538       856  LOAD_GLOBAL              len
              858  LOAD_FAST                'args'
              860  CALL_FUNCTION_1       1  '1 positional argument'
              862  LOAD_CONST               1
              864  COMPARE_OP               ==
          866_868  POP_JUMP_IF_TRUE    874  'to 874'
              870  LOAD_ASSERT              AssertionError
              872  RAISE_VARARGS_1       1  'exception instance'
            874_0  COME_FROM           866  '866'

 L. 539       874  LOAD_GLOBAL              isinstance
              876  LOAD_FAST                'args'
              878  LOAD_CONST               0
              880  BINARY_SUBSCR    

 L. 540       882  LOAD_GLOBAL              int
              884  LOAD_GLOBAL              compat_str
              886  LOAD_GLOBAL              _Undefined
              888  BUILD_TUPLE_3         3 
              890  CALL_FUNCTION_2       2  '2 positional arguments'
          892_894  POP_JUMP_IF_TRUE    900  'to 900'
              896  LOAD_ASSERT              AssertionError
              898  RAISE_VARARGS_1       1  'exception instance'
            900_0  COME_FROM           892  '892'

 L. 541       900  LOAD_FAST                'args'
              902  LOAD_CONST               0
              904  BINARY_SUBSCR    
              906  LOAD_GLOBAL              undefined
              908  COMPARE_OP               ==
          910_912  POP_JUMP_IF_FALSE   920  'to 920'

 L. 542       914  LOAD_STR                 'undefined'
              916  STORE_FAST               'res'
              918  JUMP_FORWARD        932  'to 932'
            920_0  COME_FROM           910  '910'

 L. 544       920  LOAD_GLOBAL              compat_str
              922  LOAD_FAST                'args'
              924  LOAD_CONST               0
              926  BINARY_SUBSCR    
              928  CALL_FUNCTION_1       1  '1 positional argument'
              930  STORE_FAST               'res'
            932_0  COME_FROM           918  '918'

 L. 545       932  LOAD_DEREF               'stack'
              934  LOAD_METHOD              append
              936  LOAD_FAST                'res'
              938  CALL_METHOD_1         1  '1 positional argument'
              940  POP_TOP          

 L. 546       942  CONTINUE             94  'to 94'
              944  JUMP_FORWARD       1506  'to 1506'
            946_0  COME_FROM           852  '852'

 L. 548       946  LOAD_GLOBAL              NotImplementedError

 L. 549       948  LOAD_STR                 'Function String.%s is not yet implemented'

 L. 550       950  LOAD_FAST                'mname'
              952  BINARY_MODULO    
              954  CALL_FUNCTION_1       1  '1 positional argument'
              956  RAISE_VARARGS_1       1  'exception instance'
          958_960  JUMP_FORWARD       1506  'to 1506'
            962_0  COME_FROM           842  '842'

 L. 551       962  LOAD_GLOBAL              isinstance
              964  LOAD_FAST                'obj'
              966  LOAD_GLOBAL              _AVMClass_Object
              968  CALL_FUNCTION_2       2  '2 positional arguments'
          970_972  POP_JUMP_IF_FALSE  1012  'to 1012'

 L. 552       974  LOAD_DEREF               'self'
              976  LOAD_METHOD              extract_function
              978  LOAD_FAST                'obj'
              980  LOAD_ATTR                avm_class
              982  LOAD_FAST                'mname'
              984  CALL_METHOD_2         2  '2 positional arguments'
              986  STORE_FAST               'func'

 L. 553       988  LOAD_FAST                'func'
              990  LOAD_FAST                'args'
              992  CALL_FUNCTION_1       1  '1 positional argument'
              994  STORE_FAST               'res'

 L. 554       996  LOAD_DEREF               'stack'
              998  LOAD_METHOD              append
             1000  LOAD_FAST                'res'
             1002  CALL_METHOD_1         1  '1 positional argument'
             1004  POP_TOP          

 L. 555      1006  CONTINUE             94  'to 94'
         1008_1010  JUMP_FORWARD       1506  'to 1506'
           1012_0  COME_FROM           970  '970'

 L. 556      1012  LOAD_GLOBAL              isinstance
             1014  LOAD_FAST                'obj'
             1016  LOAD_GLOBAL              _AVMClass
             1018  CALL_FUNCTION_2       2  '2 positional arguments'
         1020_1022  POP_JUMP_IF_FALSE  1060  'to 1060'

 L. 557      1024  LOAD_DEREF               'self'
             1026  LOAD_METHOD              extract_function
             1028  LOAD_FAST                'obj'
             1030  LOAD_FAST                'mname'
             1032  CALL_METHOD_2         2  '2 positional arguments'
             1034  STORE_FAST               'func'

 L. 558      1036  LOAD_FAST                'func'
             1038  LOAD_FAST                'args'
             1040  CALL_FUNCTION_1       1  '1 positional argument'
             1042  STORE_FAST               'res'

 L. 559      1044  LOAD_DEREF               'stack'
             1046  LOAD_METHOD              append
             1048  LOAD_FAST                'res'
             1050  CALL_METHOD_1         1  '1 positional argument'
             1052  POP_TOP          

 L. 560      1054  CONTINUE             94  'to 94'
         1056_1058  JUMP_FORWARD       1506  'to 1506'
           1060_0  COME_FROM          1020  '1020'

 L. 561      1060  LOAD_GLOBAL              isinstance
             1062  LOAD_FAST                'obj'
             1064  LOAD_GLOBAL              _ScopeDict
             1066  CALL_FUNCTION_2       2  '2 positional arguments'
         1068_1070  POP_JUMP_IF_FALSE  1134  'to 1134'

 L. 562      1072  LOAD_FAST                'mname'
             1074  LOAD_FAST                'obj'
             1076  LOAD_ATTR                avm_class
             1078  LOAD_ATTR                method_names
             1080  COMPARE_OP               in
         1082_1084  POP_JUMP_IF_FALSE  1110  'to 1110'

 L. 563      1086  LOAD_DEREF               'self'
             1088  LOAD_METHOD              extract_function
             1090  LOAD_FAST                'obj'
             1092  LOAD_ATTR                avm_class
             1094  LOAD_FAST                'mname'
             1096  CALL_METHOD_2         2  '2 positional arguments'
             1098  STORE_FAST               'func'

 L. 564      1100  LOAD_FAST                'func'
             1102  LOAD_FAST                'args'
             1104  CALL_FUNCTION_1       1  '1 positional argument'
             1106  STORE_FAST               'res'
             1108  JUMP_FORWARD       1118  'to 1118'
           1110_0  COME_FROM          1082  '1082'

 L. 566      1110  LOAD_FAST                'obj'
             1112  LOAD_FAST                'mname'
             1114  BINARY_SUBSCR    
             1116  STORE_FAST               'res'
           1118_0  COME_FROM          1108  '1108'

 L. 567      1118  LOAD_DEREF               'stack'
             1120  LOAD_METHOD              append
             1122  LOAD_FAST                'res'
             1124  CALL_METHOD_1         1  '1 positional argument'
             1126  POP_TOP          

 L. 568      1128  CONTINUE             94  'to 94'
         1130_1132  JUMP_FORWARD       1506  'to 1506'
           1134_0  COME_FROM          1068  '1068'

 L. 569      1134  LOAD_GLOBAL              isinstance
             1136  LOAD_FAST                'obj'
             1138  LOAD_GLOBAL              compat_str
             1140  CALL_FUNCTION_2       2  '2 positional arguments'
         1142_1144  POP_JUMP_IF_FALSE  1342  'to 1342'

 L. 570      1146  LOAD_FAST                'mname'
             1148  LOAD_STR                 'split'
             1150  COMPARE_OP               ==
         1152_1154  POP_JUMP_IF_FALSE  1246  'to 1246'

 L. 571      1156  LOAD_GLOBAL              len
             1158  LOAD_FAST                'args'
             1160  CALL_FUNCTION_1       1  '1 positional argument'
             1162  LOAD_CONST               1
             1164  COMPARE_OP               ==
         1166_1168  POP_JUMP_IF_TRUE   1174  'to 1174'
             1170  LOAD_ASSERT              AssertionError
             1172  RAISE_VARARGS_1       1  'exception instance'
           1174_0  COME_FROM          1166  '1166'

 L. 572      1174  LOAD_GLOBAL              isinstance
             1176  LOAD_FAST                'args'
             1178  LOAD_CONST               0
             1180  BINARY_SUBSCR    
             1182  LOAD_GLOBAL              compat_str
             1184  CALL_FUNCTION_2       2  '2 positional arguments'
         1186_1188  POP_JUMP_IF_TRUE   1194  'to 1194'
             1190  LOAD_ASSERT              AssertionError
             1192  RAISE_VARARGS_1       1  'exception instance'
           1194_0  COME_FROM          1186  '1186'

 L. 573      1194  LOAD_FAST                'args'
             1196  LOAD_CONST               0
             1198  BINARY_SUBSCR    
             1200  LOAD_STR                 ''
             1202  COMPARE_OP               ==
         1204_1206  POP_JUMP_IF_FALSE  1218  'to 1218'

 L. 574      1208  LOAD_GLOBAL              list
             1210  LOAD_FAST                'obj'
             1212  CALL_FUNCTION_1       1  '1 positional argument'
             1214  STORE_FAST               'res'
             1216  JUMP_FORWARD       1232  'to 1232'
           1218_0  COME_FROM          1204  '1204'

 L. 576      1218  LOAD_FAST                'obj'
             1220  LOAD_METHOD              split
             1222  LOAD_FAST                'args'
             1224  LOAD_CONST               0
             1226  BINARY_SUBSCR    
             1228  CALL_METHOD_1         1  '1 positional argument'
             1230  STORE_FAST               'res'
           1232_0  COME_FROM          1216  '1216'

 L. 577      1232  LOAD_DEREF               'stack'
             1234  LOAD_METHOD              append
             1236  LOAD_FAST                'res'
             1238  CALL_METHOD_1         1  '1 positional argument'
             1240  POP_TOP          

 L. 578      1242  CONTINUE             94  'to 94'
             1244  JUMP_FORWARD       1340  'to 1340'
           1246_0  COME_FROM          1152  '1152'

 L. 579      1246  LOAD_FAST                'mname'
             1248  LOAD_STR                 'charCodeAt'
             1250  COMPARE_OP               ==
         1252_1254  POP_JUMP_IF_FALSE  1506  'to 1506'

 L. 580      1256  LOAD_GLOBAL              len
             1258  LOAD_FAST                'args'
             1260  CALL_FUNCTION_1       1  '1 positional argument'
             1262  LOAD_CONST               1
             1264  COMPARE_OP               <=
         1266_1268  POP_JUMP_IF_TRUE   1274  'to 1274'
             1270  LOAD_ASSERT              AssertionError
             1272  RAISE_VARARGS_1       1  'exception instance'
           1274_0  COME_FROM          1266  '1266'

 L. 581      1274  LOAD_GLOBAL              len
             1276  LOAD_FAST                'args'
             1278  CALL_FUNCTION_1       1  '1 positional argument'
             1280  LOAD_CONST               0
             1282  COMPARE_OP               ==
         1284_1286  POP_JUMP_IF_FALSE  1292  'to 1292'
             1288  LOAD_CONST               0
             1290  JUMP_FORWARD       1298  'to 1298'
           1292_0  COME_FROM          1284  '1284'
             1292  LOAD_FAST                'args'
             1294  LOAD_CONST               0
             1296  BINARY_SUBSCR    
           1298_0  COME_FROM          1290  '1290'
             1298  STORE_FAST               'idx'

 L. 582      1300  LOAD_GLOBAL              isinstance
             1302  LOAD_FAST                'idx'
             1304  LOAD_GLOBAL              int
             1306  CALL_FUNCTION_2       2  '2 positional arguments'
         1308_1310  POP_JUMP_IF_TRUE   1316  'to 1316'
             1312  LOAD_ASSERT              AssertionError
             1314  RAISE_VARARGS_1       1  'exception instance'
           1316_0  COME_FROM          1308  '1308'

 L. 583      1316  LOAD_GLOBAL              ord
             1318  LOAD_FAST                'obj'
             1320  LOAD_FAST                'idx'
             1322  BINARY_SUBSCR    
             1324  CALL_FUNCTION_1       1  '1 positional argument'
             1326  STORE_FAST               'res'

 L. 584      1328  LOAD_DEREF               'stack'
             1330  LOAD_METHOD              append
             1332  LOAD_FAST                'res'
             1334  CALL_METHOD_1         1  '1 positional argument'
             1336  POP_TOP          

 L. 585      1338  CONTINUE             94  'to 94'
           1340_0  COME_FROM          1244  '1244'
             1340  JUMP_FORWARD       1506  'to 1506'
           1342_0  COME_FROM          1142  '1142'

 L. 586      1342  LOAD_GLOBAL              isinstance
             1344  LOAD_FAST                'obj'
             1346  LOAD_GLOBAL              list
             1348  CALL_FUNCTION_2       2  '2 positional arguments'
         1350_1352  POP_JUMP_IF_FALSE  1506  'to 1506'

 L. 587      1354  LOAD_FAST                'mname'
             1356  LOAD_STR                 'slice'
             1358  COMPARE_OP               ==
         1360_1362  POP_JUMP_IF_FALSE  1432  'to 1432'

 L. 588      1364  LOAD_GLOBAL              len
             1366  LOAD_FAST                'args'
             1368  CALL_FUNCTION_1       1  '1 positional argument'
             1370  LOAD_CONST               1
             1372  COMPARE_OP               ==
         1374_1376  POP_JUMP_IF_TRUE   1382  'to 1382'
             1378  LOAD_ASSERT              AssertionError
             1380  RAISE_VARARGS_1       1  'exception instance'
           1382_0  COME_FROM          1374  '1374'

 L. 589      1382  LOAD_GLOBAL              isinstance
             1384  LOAD_FAST                'args'
             1386  LOAD_CONST               0
             1388  BINARY_SUBSCR    
             1390  LOAD_GLOBAL              int
             1392  CALL_FUNCTION_2       2  '2 positional arguments'
         1394_1396  POP_JUMP_IF_TRUE   1402  'to 1402'
             1398  LOAD_ASSERT              AssertionError
             1400  RAISE_VARARGS_1       1  'exception instance'
           1402_0  COME_FROM          1394  '1394'

 L. 590      1402  LOAD_FAST                'obj'
             1404  LOAD_FAST                'args'
             1406  LOAD_CONST               0
             1408  BINARY_SUBSCR    
             1410  LOAD_CONST               None
             1412  BUILD_SLICE_2         2 
             1414  BINARY_SUBSCR    
             1416  STORE_FAST               'res'

 L. 591      1418  LOAD_DEREF               'stack'
             1420  LOAD_METHOD              append
             1422  LOAD_FAST                'res'
             1424  CALL_METHOD_1         1  '1 positional argument'
             1426  POP_TOP          

 L. 592      1428  CONTINUE             94  'to 94'
             1430  JUMP_FORWARD       1506  'to 1506'
           1432_0  COME_FROM          1360  '1360'

 L. 593      1432  LOAD_FAST                'mname'
             1434  LOAD_STR                 'join'
             1436  COMPARE_OP               ==
         1438_1440  POP_JUMP_IF_FALSE  1506  'to 1506'

 L. 594      1442  LOAD_GLOBAL              len
             1444  LOAD_FAST                'args'
             1446  CALL_FUNCTION_1       1  '1 positional argument'
             1448  LOAD_CONST               1
             1450  COMPARE_OP               ==
         1452_1454  POP_JUMP_IF_TRUE   1460  'to 1460'
             1456  LOAD_ASSERT              AssertionError
             1458  RAISE_VARARGS_1       1  'exception instance'
           1460_0  COME_FROM          1452  '1452'

 L. 595      1460  LOAD_GLOBAL              isinstance
             1462  LOAD_FAST                'args'
             1464  LOAD_CONST               0
             1466  BINARY_SUBSCR    
             1468  LOAD_GLOBAL              compat_str
             1470  CALL_FUNCTION_2       2  '2 positional arguments'
         1472_1474  POP_JUMP_IF_TRUE   1480  'to 1480'
             1476  LOAD_ASSERT              AssertionError
             1478  RAISE_VARARGS_1       1  'exception instance'
           1480_0  COME_FROM          1472  '1472'

 L. 596      1480  LOAD_FAST                'args'
             1482  LOAD_CONST               0
             1484  BINARY_SUBSCR    
             1486  LOAD_METHOD              join
             1488  LOAD_FAST                'obj'
           1490_0  COME_FROM           944  '944'
             1490  CALL_METHOD_1         1  '1 positional argument'
             1492  STORE_FAST               'res'

 L. 597      1494  LOAD_DEREF               'stack'
             1496  LOAD_METHOD              append
             1498  LOAD_FAST                'res'
             1500  CALL_METHOD_1         1  '1 positional argument'
             1502  POP_TOP          

 L. 598      1504  CONTINUE             94  'to 94'
           1506_0  COME_FROM          1438  '1438'
           1506_1  COME_FROM          1430  '1430'
           1506_2  COME_FROM          1350  '1350'
           1506_3  COME_FROM          1340  '1340'
           1506_4  COME_FROM          1252  '1252'
           1506_5  COME_FROM          1130  '1130'
           1506_6  COME_FROM          1056  '1056'
           1506_7  COME_FROM          1008  '1008'
           1506_8  COME_FROM           958  '958'

 L. 599      1506  LOAD_GLOBAL              NotImplementedError

 L. 600      1508  LOAD_STR                 'Unsupported property %r on %r'

 L. 601      1510  LOAD_FAST                'mname'
             1512  LOAD_FAST                'obj'
             1514  BUILD_TUPLE_2         2 
             1516  BINARY_MODULO    
             1518  CALL_FUNCTION_1       1  '1 positional argument'
             1520  RAISE_VARARGS_1       1  'exception instance'
             1522  JUMP_BACK            94  'to 94'
           1524_0  COME_FROM           772  '772'

 L. 602      1524  LOAD_FAST                'opcode'
             1526  LOAD_CONST               71
             1528  COMPARE_OP               ==
         1530_1532  POP_JUMP_IF_FALSE  1542  'to 1542'

 L. 603      1534  LOAD_GLOBAL              undefined
             1536  STORE_FAST               'res'

 L. 604      1538  LOAD_FAST                'res'
             1540  RETURN_VALUE     
           1542_0  COME_FROM          1530  '1530'

 L. 605      1542  LOAD_FAST                'opcode'
             1544  LOAD_CONST               72
             1546  COMPARE_OP               ==
         1548_1550  POP_JUMP_IF_FALSE  1564  'to 1564'

 L. 606      1552  LOAD_DEREF               'stack'
             1554  LOAD_METHOD              pop
             1556  CALL_METHOD_0         0  '0 positional arguments'
             1558  STORE_FAST               'res'

 L. 607      1560  LOAD_FAST                'res'
             1562  RETURN_VALUE     
           1564_0  COME_FROM          1548  '1548'

 L. 608      1564  LOAD_FAST                'opcode'
             1566  LOAD_CONST               73
             1568  COMPARE_OP               ==
         1570_1572  POP_JUMP_IF_FALSE  1620  'to 1620'

 L. 610      1574  LOAD_FAST                'u30'
             1576  CALL_FUNCTION_0       0  '0 positional arguments'
             1578  STORE_FAST               'arg_count'

 L. 611      1580  LOAD_GLOBAL              list
             1582  LOAD_GLOBAL              reversed

 L. 612      1584  LOAD_CLOSURE             'stack'
             1586  BUILD_TUPLE_1         1 
             1588  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1590  LOAD_STR                 'SWFInterpreter.extract_function.<locals>.resfunc.<locals>.<listcomp>'
             1592  MAKE_FUNCTION_8          'closure'
             1594  LOAD_GLOBAL              range
             1596  LOAD_FAST                'arg_count'
             1598  CALL_FUNCTION_1       1  '1 positional argument'
             1600  GET_ITER         
             1602  CALL_FUNCTION_1       1  '1 positional argument'
             1604  CALL_FUNCTION_1       1  '1 positional argument'
             1606  CALL_FUNCTION_1       1  '1 positional argument'
             1608  STORE_FAST               'args'

 L. 613      1610  LOAD_DEREF               'stack'
             1612  LOAD_METHOD              pop
             1614  CALL_METHOD_0         0  '0 positional arguments'
             1616  STORE_FAST               'obj'
             1618  JUMP_BACK            94  'to 94'
           1620_0  COME_FROM          1570  '1570'

 L. 614      1620  LOAD_FAST                'opcode'
             1622  LOAD_CONST               74
             1624  COMPARE_OP               ==
         1626_1628  POP_JUMP_IF_FALSE  1722  'to 1722'

 L. 615      1630  LOAD_FAST                'u30'
             1632  CALL_FUNCTION_0       0  '0 positional arguments'
             1634  STORE_FAST               'index'

 L. 616      1636  LOAD_FAST                'u30'
             1638  CALL_FUNCTION_0       0  '0 positional arguments'
             1640  STORE_FAST               'arg_count'

 L. 617      1642  LOAD_GLOBAL              list
             1644  LOAD_GLOBAL              reversed

 L. 618      1646  LOAD_CLOSURE             'stack'
             1648  BUILD_TUPLE_1         1 
             1650  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1652  LOAD_STR                 'SWFInterpreter.extract_function.<locals>.resfunc.<locals>.<listcomp>'
             1654  MAKE_FUNCTION_8          'closure'
             1656  LOAD_GLOBAL              range
             1658  LOAD_FAST                'arg_count'
             1660  CALL_FUNCTION_1       1  '1 positional argument'
             1662  GET_ITER         
             1664  CALL_FUNCTION_1       1  '1 positional argument'
             1666  CALL_FUNCTION_1       1  '1 positional argument'
             1668  CALL_FUNCTION_1       1  '1 positional argument'
             1670  STORE_FAST               'args'

 L. 619      1672  LOAD_DEREF               'stack'
             1674  LOAD_METHOD              pop
             1676  CALL_METHOD_0         0  '0 positional arguments'
             1678  STORE_FAST               'obj'

 L. 621      1680  LOAD_DEREF               'self'
             1682  LOAD_ATTR                multinames
             1684  LOAD_FAST                'index'
             1686  BINARY_SUBSCR    
             1688  STORE_FAST               'mname'

 L. 622      1690  LOAD_GLOBAL              isinstance
             1692  LOAD_FAST                'obj'
             1694  LOAD_GLOBAL              _AVMClass
             1696  CALL_FUNCTION_2       2  '2 positional arguments'
         1698_1700  POP_JUMP_IF_TRUE   1706  'to 1706'
             1702  LOAD_ASSERT              AssertionError
             1704  RAISE_VARARGS_1       1  'exception instance'
           1706_0  COME_FROM          1698  '1698'

 L. 626      1706  LOAD_DEREF               'stack'
             1708  LOAD_METHOD              append
             1710  LOAD_FAST                'obj'
             1712  LOAD_METHOD              make_object
             1714  CALL_METHOD_0         0  '0 positional arguments'
             1716  CALL_METHOD_1         1  '1 positional argument'
             1718  POP_TOP          
             1720  JUMP_BACK            94  'to 94'
           1722_0  COME_FROM          1626  '1626'

 L. 627      1722  LOAD_FAST                'opcode'
             1724  LOAD_CONST               79
             1726  COMPARE_OP               ==
         1728_1730  POP_JUMP_IF_FALSE  1960  'to 1960'

 L. 628      1732  LOAD_FAST                'u30'
             1734  CALL_FUNCTION_0       0  '0 positional arguments'
             1736  STORE_FAST               'index'

 L. 629      1738  LOAD_DEREF               'self'
             1740  LOAD_ATTR                multinames
             1742  LOAD_FAST                'index'
             1744  BINARY_SUBSCR    
             1746  STORE_FAST               'mname'

 L. 630      1748  LOAD_FAST                'u30'
             1750  CALL_FUNCTION_0       0  '0 positional arguments'
             1752  STORE_FAST               'arg_count'

 L. 631      1754  LOAD_GLOBAL              list
             1756  LOAD_GLOBAL              reversed

 L. 632      1758  LOAD_CLOSURE             'stack'
             1760  BUILD_TUPLE_1         1 
             1762  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1764  LOAD_STR                 'SWFInterpreter.extract_function.<locals>.resfunc.<locals>.<listcomp>'
             1766  MAKE_FUNCTION_8          'closure'
             1768  LOAD_GLOBAL              range
             1770  LOAD_FAST                'arg_count'
             1772  CALL_FUNCTION_1       1  '1 positional argument'
             1774  GET_ITER         
             1776  CALL_FUNCTION_1       1  '1 positional argument'
             1778  CALL_FUNCTION_1       1  '1 positional argument'
             1780  CALL_FUNCTION_1       1  '1 positional argument'
             1782  STORE_FAST               'args'

 L. 633      1784  LOAD_DEREF               'stack'
             1786  LOAD_METHOD              pop
             1788  CALL_METHOD_0         0  '0 positional arguments'
             1790  STORE_FAST               'obj'

 L. 634      1792  LOAD_GLOBAL              isinstance
             1794  LOAD_FAST                'obj'
             1796  LOAD_GLOBAL              _AVMClass_Object
             1798  CALL_FUNCTION_2       2  '2 positional arguments'
         1800_1802  POP_JUMP_IF_FALSE  1840  'to 1840'

 L. 635      1804  LOAD_DEREF               'self'
             1806  LOAD_METHOD              extract_function
             1808  LOAD_FAST                'obj'
             1810  LOAD_ATTR                avm_class
             1812  LOAD_FAST                'mname'
             1814  CALL_METHOD_2         2  '2 positional arguments'
             1816  STORE_FAST               'func'

 L. 636      1818  LOAD_FAST                'func'
             1820  LOAD_FAST                'args'
             1822  CALL_FUNCTION_1       1  '1 positional argument'
             1824  STORE_FAST               'res'

 L. 637      1826  LOAD_FAST                'res'
             1828  LOAD_GLOBAL              undefined
             1830  COMPARE_OP               is
             1832  POP_JUMP_IF_TRUE     94  'to 94'
             1834  LOAD_GLOBAL              AssertionError
             1836  RAISE_VARARGS_1       1  'exception instance'

 L. 638      1838  CONTINUE             94  'to 94'
           1840_0  COME_FROM          1800  '1800'

 L. 639      1840  LOAD_GLOBAL              isinstance
             1842  LOAD_FAST                'obj'
             1844  LOAD_GLOBAL              _ScopeDict
             1846  CALL_FUNCTION_2       2  '2 positional arguments'
         1848_1850  POP_JUMP_IF_FALSE  1906  'to 1906'

 L. 640      1852  LOAD_FAST                'mname'
             1854  LOAD_FAST                'obj'
             1856  LOAD_ATTR                avm_class
             1858  LOAD_ATTR                method_names
             1860  COMPARE_OP               in
         1862_1864  POP_JUMP_IF_TRUE   1870  'to 1870'
             1866  LOAD_ASSERT              AssertionError
             1868  RAISE_VARARGS_1       1  'exception instance'
           1870_0  COME_FROM          1862  '1862'

 L. 641      1870  LOAD_DEREF               'self'
             1872  LOAD_METHOD              extract_function
             1874  LOAD_FAST                'obj'
             1876  LOAD_ATTR                avm_class
             1878  LOAD_FAST                'mname'
             1880  CALL_METHOD_2         2  '2 positional arguments'
             1882  STORE_FAST               'func'

 L. 642      1884  LOAD_FAST                'func'
             1886  LOAD_FAST                'args'
             1888  CALL_FUNCTION_1       1  '1 positional argument'
             1890  STORE_FAST               'res'

 L. 643      1892  LOAD_FAST                'res'
             1894  LOAD_GLOBAL              undefined
             1896  COMPARE_OP               is
             1898  POP_JUMP_IF_TRUE     94  'to 94'
             1900  LOAD_GLOBAL              AssertionError
             1902  RAISE_VARARGS_1       1  'exception instance'

 L. 644      1904  CONTINUE             94  'to 94'
           1906_0  COME_FROM          1848  '1848'

 L. 645      1906  LOAD_FAST                'mname'
             1908  LOAD_STR                 'reverse'
             1910  COMPARE_OP               ==
         1912_1914  POP_JUMP_IF_FALSE  1942  'to 1942'

 L. 646      1916  LOAD_GLOBAL              isinstance
             1918  LOAD_FAST                'obj'
             1920  LOAD_GLOBAL              list
             1922  CALL_FUNCTION_2       2  '2 positional arguments'
         1924_1926  POP_JUMP_IF_TRUE   1932  'to 1932'
             1928  LOAD_ASSERT              AssertionError
             1930  RAISE_VARARGS_1       1  'exception instance'
           1932_0  COME_FROM          1924  '1924'

 L. 647      1932  LOAD_FAST                'obj'
             1934  LOAD_METHOD              reverse
             1936  CALL_METHOD_0         0  '0 positional arguments'
             1938  POP_TOP          
             1940  JUMP_FORWARD       1958  'to 1958'
           1942_0  COME_FROM          1912  '1912'

 L. 649      1942  LOAD_GLOBAL              NotImplementedError

 L. 650      1944  LOAD_STR                 'Unsupported (void) property %r on %r'

 L. 651      1946  LOAD_FAST                'mname'
             1948  LOAD_FAST                'obj'
             1950  BUILD_TUPLE_2         2 
             1952  BINARY_MODULO    
             1954  CALL_FUNCTION_1       1  '1 positional argument'
             1956  RAISE_VARARGS_1       1  'exception instance'
           1958_0  COME_FROM          1940  '1940'
             1958  JUMP_BACK            94  'to 94'
           1960_0  COME_FROM          1728  '1728'

 L. 652      1960  LOAD_FAST                'opcode'
             1962  LOAD_CONST               86
             1964  COMPARE_OP               ==
         1966_1968  POP_JUMP_IF_FALSE  2040  'to 2040'

 L. 653      1970  LOAD_FAST                'u30'
             1972  CALL_FUNCTION_0       0  '0 positional arguments'
             1974  STORE_FAST               'arg_count'

 L. 654      1976  BUILD_LIST_0          0 
             1978  STORE_FAST               'arr'

 L. 655      1980  SETUP_LOOP         2014  'to 2014'
             1982  LOAD_GLOBAL              range
             1984  LOAD_FAST                'arg_count'
             1986  CALL_FUNCTION_1       1  '1 positional argument'
             1988  GET_ITER         
             1990  FOR_ITER           2012  'to 2012'
             1992  STORE_FAST               'i'

 L. 656      1994  LOAD_FAST                'arr'
             1996  LOAD_METHOD              append
             1998  LOAD_DEREF               'stack'
             2000  LOAD_METHOD              pop
             2002  CALL_METHOD_0         0  '0 positional arguments'
             2004  CALL_METHOD_1         1  '1 positional argument'
             2006  POP_TOP          
         2008_2010  JUMP_BACK          1990  'to 1990'
             2012  POP_BLOCK        
           2014_0  COME_FROM_LOOP     1980  '1980'

 L. 657      2014  LOAD_FAST                'arr'
             2016  LOAD_CONST               None
             2018  LOAD_CONST               None
             2020  LOAD_CONST               -1
             2022  BUILD_SLICE_3         3 
             2024  BINARY_SUBSCR    
             2026  STORE_FAST               'arr'

 L. 658      2028  LOAD_DEREF               'stack'
             2030  LOAD_METHOD              append
             2032  LOAD_FAST                'arr'
             2034  CALL_METHOD_1         1  '1 positional argument'
             2036  POP_TOP          
             2038  JUMP_BACK            94  'to 94'
           2040_0  COME_FROM          1966  '1966'

 L. 659      2040  LOAD_FAST                'opcode'
             2042  LOAD_CONST               93
             2044  COMPARE_OP               ==
         2046_2048  POP_JUMP_IF_FALSE  2162  'to 2162'

 L. 660      2050  LOAD_FAST                'u30'
             2052  CALL_FUNCTION_0       0  '0 positional arguments'
             2054  STORE_FAST               'index'

 L. 661      2056  LOAD_DEREF               'self'
             2058  LOAD_ATTR                multinames
             2060  LOAD_FAST                'index'
             2062  BINARY_SUBSCR    
             2064  STORE_FAST               'mname'

 L. 662      2066  SETUP_LOOP         2110  'to 2110'
             2068  LOAD_GLOBAL              reversed
             2070  LOAD_FAST                'scopes'
             2072  CALL_FUNCTION_1       1  '1 positional argument'
             2074  GET_ITER         
           2076_0  COME_FROM          2086  '2086'
             2076  FOR_ITER           2100  'to 2100'
             2078  STORE_FAST               's'

 L. 663      2080  LOAD_FAST                'mname'
             2082  LOAD_FAST                's'
             2084  COMPARE_OP               in
         2086_2088  POP_JUMP_IF_FALSE  2076  'to 2076'

 L. 664      2090  LOAD_FAST                's'
             2092  STORE_FAST               'res'

 L. 665      2094  BREAK_LOOP       
         2096_2098  JUMP_BACK          2076  'to 2076'
             2100  POP_BLOCK        

 L. 667      2102  LOAD_FAST                'scopes'
             2104  LOAD_CONST               0
             2106  BINARY_SUBSCR    
             2108  STORE_FAST               'res'
           2110_0  COME_FROM_LOOP     2066  '2066'

 L. 668      2110  LOAD_FAST                'mname'
             2112  LOAD_FAST                'res'
             2114  COMPARE_OP               not-in
         2116_2118  POP_JUMP_IF_FALSE  2146  'to 2146'
             2120  LOAD_FAST                'mname'
             2122  LOAD_GLOBAL              _builtin_classes
             2124  COMPARE_OP               in
         2126_2128  POP_JUMP_IF_FALSE  2146  'to 2146'

 L. 669      2130  LOAD_DEREF               'stack'
             2132  LOAD_METHOD              append
             2134  LOAD_GLOBAL              _builtin_classes
             2136  LOAD_FAST                'mname'
             2138  BINARY_SUBSCR    
             2140  CALL_METHOD_1         1  '1 positional argument'
             2142  POP_TOP          
             2144  JUMP_FORWARD       2160  'to 2160'
           2146_0  COME_FROM          2126  '2126'
           2146_1  COME_FROM          2116  '2116'

 L. 671      2146  LOAD_DEREF               'stack'
             2148  LOAD_METHOD              append
             2150  LOAD_FAST                'res'
             2152  LOAD_FAST                'mname'
             2154  BINARY_SUBSCR    
             2156  CALL_METHOD_1         1  '1 positional argument'
             2158  POP_TOP          
           2160_0  COME_FROM          2144  '2144'
             2160  JUMP_BACK            94  'to 94'
           2162_0  COME_FROM          2046  '2046'

 L. 672      2162  LOAD_FAST                'opcode'
             2164  LOAD_CONST               94
             2166  COMPARE_OP               ==
         2168_2170  POP_JUMP_IF_FALSE  2242  'to 2242'

 L. 673      2172  LOAD_FAST                'u30'
             2174  CALL_FUNCTION_0       0  '0 positional arguments'
             2176  STORE_FAST               'index'

 L. 674      2178  LOAD_DEREF               'self'
             2180  LOAD_ATTR                multinames
             2182  LOAD_FAST                'index'
             2184  BINARY_SUBSCR    
             2186  STORE_FAST               'mname'

 L. 675      2188  SETUP_LOOP         2230  'to 2230'
             2190  LOAD_GLOBAL              reversed
             2192  LOAD_FAST                'scopes'
             2194  CALL_FUNCTION_1       1  '1 positional argument'
             2196  GET_ITER         
           2198_0  COME_FROM          2208  '2208'
             2198  FOR_ITER           2222  'to 2222'
             2200  STORE_FAST               's'

 L. 676      2202  LOAD_FAST                'mname'
             2204  LOAD_FAST                's'
             2206  COMPARE_OP               in
         2208_2210  POP_JUMP_IF_FALSE  2198  'to 2198'

 L. 677      2212  LOAD_FAST                's'
             2214  STORE_FAST               'res'

 L. 678      2216  BREAK_LOOP       
         2218_2220  JUMP_BACK          2198  'to 2198'
             2222  POP_BLOCK        

 L. 680      2224  LOAD_DEREF               'avm_class'
             2226  LOAD_ATTR                variables
             2228  STORE_FAST               'res'
           2230_0  COME_FROM_LOOP     2188  '2188'

 L. 681      2230  LOAD_DEREF               'stack'
             2232  LOAD_METHOD              append
             2234  LOAD_FAST                'res'
             2236  CALL_METHOD_1         1  '1 positional argument'
             2238  POP_TOP          
             2240  JUMP_BACK            94  'to 94'
           2242_0  COME_FROM          2168  '2168'

 L. 682      2242  LOAD_FAST                'opcode'
             2244  LOAD_CONST               96
             2246  COMPARE_OP               ==
         2248_2250  POP_JUMP_IF_FALSE  2366  'to 2366'

 L. 683      2252  LOAD_FAST                'u30'
             2254  CALL_FUNCTION_0       0  '0 positional arguments'
             2256  STORE_FAST               'index'

 L. 684      2258  LOAD_DEREF               'self'
             2260  LOAD_ATTR                multinames
             2262  LOAD_FAST                'index'
             2264  BINARY_SUBSCR    
             2266  STORE_FAST               'mname'

 L. 685      2268  SETUP_LOOP         2310  'to 2310'
             2270  LOAD_GLOBAL              reversed
             2272  LOAD_FAST                'scopes'
             2274  CALL_FUNCTION_1       1  '1 positional argument'
             2276  GET_ITER         
           2278_0  COME_FROM          2288  '2288'
             2278  FOR_ITER           2302  'to 2302'
             2280  STORE_FAST               's'

 L. 686      2282  LOAD_FAST                'mname'
             2284  LOAD_FAST                's'
             2286  COMPARE_OP               in
         2288_2290  POP_JUMP_IF_FALSE  2278  'to 2278'

 L. 687      2292  LOAD_FAST                's'
             2294  STORE_FAST               'scope'

 L. 688      2296  BREAK_LOOP       
         2298_2300  JUMP_BACK          2278  'to 2278'
             2302  POP_BLOCK        

 L. 690      2304  LOAD_DEREF               'avm_class'
             2306  LOAD_ATTR                variables
             2308  STORE_FAST               'scope'
           2310_0  COME_FROM_LOOP     2268  '2268'

 L. 692      2310  LOAD_FAST                'mname'
             2312  LOAD_FAST                'scope'
             2314  COMPARE_OP               in
         2316_2318  POP_JUMP_IF_FALSE  2330  'to 2330'

 L. 693      2320  LOAD_FAST                'scope'
             2322  LOAD_FAST                'mname'
             2324  BINARY_SUBSCR    
             2326  STORE_FAST               'res'
             2328  JUMP_FORWARD       2354  'to 2354'
           2330_0  COME_FROM          2316  '2316'

 L. 694      2330  LOAD_FAST                'mname'
             2332  LOAD_GLOBAL              _builtin_classes
             2334  COMPARE_OP               in
         2336_2338  POP_JUMP_IF_FALSE  2350  'to 2350'

 L. 695      2340  LOAD_GLOBAL              _builtin_classes
             2342  LOAD_FAST                'mname'
             2344  BINARY_SUBSCR    
             2346  STORE_FAST               'res'
             2348  JUMP_FORWARD       2354  'to 2354'
           2350_0  COME_FROM          2336  '2336'

 L. 699      2350  LOAD_GLOBAL              undefined
             2352  STORE_FAST               'res'
           2354_0  COME_FROM          2348  '2348'
           2354_1  COME_FROM          2328  '2328'

 L. 700      2354  LOAD_DEREF               'stack'
             2356  LOAD_METHOD              append
             2358  LOAD_FAST                'res'
             2360  CALL_METHOD_1         1  '1 positional argument'
             2362  POP_TOP          
             2364  JUMP_BACK            94  'to 94'
           2366_0  COME_FROM          2248  '2248'

 L. 701      2366  LOAD_FAST                'opcode'
             2368  LOAD_CONST               97
             2370  COMPARE_OP               ==
         2372_2374  POP_JUMP_IF_FALSE  2438  'to 2438'

 L. 702      2376  LOAD_FAST                'u30'
             2378  CALL_FUNCTION_0       0  '0 positional arguments'
             2380  STORE_FAST               'index'

 L. 703      2382  LOAD_DEREF               'stack'
             2384  LOAD_METHOD              pop
             2386  CALL_METHOD_0         0  '0 positional arguments'
             2388  STORE_FAST               'value'

 L. 704      2390  LOAD_DEREF               'self'
             2392  LOAD_ATTR                multinames
             2394  LOAD_FAST                'index'
             2396  BINARY_SUBSCR    
             2398  STORE_FAST               'idx'

 L. 705      2400  LOAD_GLOBAL              isinstance
             2402  LOAD_FAST                'idx'
             2404  LOAD_GLOBAL              _Multiname
             2406  CALL_FUNCTION_2       2  '2 positional arguments'
         2408_2410  POP_JUMP_IF_FALSE  2420  'to 2420'

 L. 706      2412  LOAD_DEREF               'stack'
             2414  LOAD_METHOD              pop
             2416  CALL_METHOD_0         0  '0 positional arguments'
             2418  STORE_FAST               'idx'
           2420_0  COME_FROM          2408  '2408'

 L. 707      2420  LOAD_DEREF               'stack'
             2422  LOAD_METHOD              pop
             2424  CALL_METHOD_0         0  '0 positional arguments'
             2426  STORE_FAST               'obj'

 L. 708      2428  LOAD_FAST                'value'
             2430  LOAD_FAST                'obj'
             2432  LOAD_FAST                'idx'
             2434  STORE_SUBSCR     
             2436  JUMP_BACK            94  'to 94'
           2438_0  COME_FROM          2372  '2372'

 L. 709      2438  LOAD_FAST                'opcode'
             2440  LOAD_CONST               98
             2442  COMPARE_OP               ==
         2444_2446  POP_JUMP_IF_FALSE  2470  'to 2470'

 L. 710      2448  LOAD_FAST                'u30'
             2450  CALL_FUNCTION_0       0  '0 positional arguments'
             2452  STORE_FAST               'index'

 L. 711      2454  LOAD_DEREF               'stack'
             2456  LOAD_METHOD              append
             2458  LOAD_FAST                'registers'
             2460  LOAD_FAST                'index'
             2462  BINARY_SUBSCR    
             2464  CALL_METHOD_1         1  '1 positional argument'
             2466  POP_TOP          
             2468  JUMP_BACK            94  'to 94'
           2470_0  COME_FROM          2444  '2444'

 L. 712      2470  LOAD_FAST                'opcode'
             2472  LOAD_CONST               99
             2474  COMPARE_OP               ==
         2476_2478  POP_JUMP_IF_FALSE  2504  'to 2504'

 L. 713      2480  LOAD_FAST                'u30'
             2482  CALL_FUNCTION_0       0  '0 positional arguments'
             2484  STORE_FAST               'index'

 L. 714      2486  LOAD_DEREF               'stack'
             2488  LOAD_METHOD              pop
             2490  CALL_METHOD_0         0  '0 positional arguments'
             2492  STORE_FAST               'value'

 L. 715      2494  LOAD_FAST                'value'
             2496  LOAD_FAST                'registers'
             2498  LOAD_FAST                'index'
             2500  STORE_SUBSCR     
             2502  JUMP_BACK            94  'to 94'
           2504_0  COME_FROM          2476  '2476'

 L. 716      2504  LOAD_FAST                'opcode'
             2506  LOAD_CONST               102
             2508  COMPARE_OP               ==
         2510_2512  POP_JUMP_IF_FALSE  2758  'to 2758'

 L. 717      2514  LOAD_FAST                'u30'
             2516  CALL_FUNCTION_0       0  '0 positional arguments'
             2518  STORE_FAST               'index'

 L. 718      2520  LOAD_DEREF               'self'
             2522  LOAD_ATTR                multinames
             2524  LOAD_FAST                'index'
             2526  BINARY_SUBSCR    
             2528  STORE_FAST               'pname'

 L. 719      2530  LOAD_FAST                'pname'
             2532  LOAD_STR                 'length'
             2534  COMPARE_OP               ==
         2536_2538  POP_JUMP_IF_FALSE  2584  'to 2584'

 L. 720      2540  LOAD_DEREF               'stack'
             2542  LOAD_METHOD              pop
             2544  CALL_METHOD_0         0  '0 positional arguments'
             2546  STORE_FAST               'obj'

 L. 721      2548  LOAD_GLOBAL              isinstance
             2550  LOAD_FAST                'obj'
             2552  LOAD_GLOBAL              compat_str
             2554  LOAD_GLOBAL              list
             2556  BUILD_TUPLE_2         2 
             2558  CALL_FUNCTION_2       2  '2 positional arguments'
         2560_2562  POP_JUMP_IF_TRUE   2568  'to 2568'
             2564  LOAD_ASSERT              AssertionError
             2566  RAISE_VARARGS_1       1  'exception instance'
           2568_0  COME_FROM          2560  '2560'

 L. 722      2568  LOAD_DEREF               'stack'
             2570  LOAD_METHOD              append
             2572  LOAD_GLOBAL              len
             2574  LOAD_FAST                'obj'
             2576  CALL_FUNCTION_1       1  '1 positional argument'
             2578  CALL_METHOD_1         1  '1 positional argument'
             2580  POP_TOP          
             2582  JUMP_FORWARD       2756  'to 2756'
           2584_0  COME_FROM          2536  '2536'

 L. 723      2584  LOAD_GLOBAL              isinstance
             2586  LOAD_FAST                'pname'
             2588  LOAD_GLOBAL              compat_str
             2590  CALL_FUNCTION_2       2  '2 positional arguments'
         2592_2594  POP_JUMP_IF_FALSE  2694  'to 2694'

 L. 724      2596  LOAD_DEREF               'stack'
             2598  LOAD_METHOD              pop
             2600  CALL_METHOD_0         0  '0 positional arguments'
             2602  STORE_FAST               'obj'

 L. 725      2604  LOAD_GLOBAL              isinstance
             2606  LOAD_FAST                'obj'
             2608  LOAD_GLOBAL              _AVMClass
             2610  CALL_FUNCTION_2       2  '2 positional arguments'
         2612_2614  POP_JUMP_IF_FALSE  2638  'to 2638'

 L. 726      2616  LOAD_FAST                'obj'
             2618  LOAD_ATTR                static_properties
             2620  LOAD_FAST                'pname'
             2622  BINARY_SUBSCR    
             2624  STORE_FAST               'res'

 L. 727      2626  LOAD_DEREF               'stack'
             2628  LOAD_METHOD              append
             2630  LOAD_FAST                'res'
             2632  CALL_METHOD_1         1  '1 positional argument'
             2634  POP_TOP          

 L. 728      2636  CONTINUE             94  'to 94'
           2638_0  COME_FROM          2612  '2612'

 L. 730      2638  LOAD_GLOBAL              isinstance
             2640  LOAD_FAST                'obj'
             2642  LOAD_GLOBAL              dict
             2644  LOAD_GLOBAL              _ScopeDict
             2646  BUILD_TUPLE_2         2 
             2648  CALL_FUNCTION_2       2  '2 positional arguments'
         2650_2652  POP_JUMP_IF_TRUE   2670  'to 2670'
             2654  LOAD_ASSERT              AssertionError

 L. 731      2656  LOAD_STR                 'Accessing member %r on %r'
             2658  LOAD_FAST                'pname'
             2660  LOAD_FAST                'obj'
             2662  BUILD_TUPLE_2         2 
             2664  BINARY_MODULO    
             2666  CALL_FUNCTION_1       1  '1 positional argument'
             2668  RAISE_VARARGS_1       1  'exception instance'
           2670_0  COME_FROM          2650  '2650'

 L. 732      2670  LOAD_FAST                'obj'
             2672  LOAD_METHOD              get
             2674  LOAD_FAST                'pname'
             2676  LOAD_GLOBAL              undefined
             2678  CALL_METHOD_2         2  '2 positional arguments'
             2680  STORE_FAST               'res'

 L. 733      2682  LOAD_DEREF               'stack'
             2684  LOAD_METHOD              append
             2686  LOAD_FAST                'res'
             2688  CALL_METHOD_1         1  '1 positional argument'
             2690  POP_TOP          
             2692  JUMP_FORWARD       2756  'to 2756'
           2694_0  COME_FROM          2592  '2592'

 L. 735      2694  LOAD_DEREF               'stack'
             2696  LOAD_METHOD              pop
             2698  CALL_METHOD_0         0  '0 positional arguments'
             2700  STORE_FAST               'idx'

 L. 736      2702  LOAD_GLOBAL              isinstance
             2704  LOAD_FAST                'idx'
             2706  LOAD_GLOBAL              int
             2708  CALL_FUNCTION_2       2  '2 positional arguments'
         2710_2712  POP_JUMP_IF_TRUE   2718  'to 2718'
             2714  LOAD_ASSERT              AssertionError
             2716  RAISE_VARARGS_1       1  'exception instance'
           2718_0  COME_FROM          2710  '2710'

 L. 737      2718  LOAD_DEREF               'stack'
             2720  LOAD_METHOD              pop
             2722  CALL_METHOD_0         0  '0 positional arguments'
             2724  STORE_FAST               'obj'

 L. 738      2726  LOAD_GLOBAL              isinstance
             2728  LOAD_FAST                'obj'
             2730  LOAD_GLOBAL              list
             2732  CALL_FUNCTION_2       2  '2 positional arguments'
         2734_2736  POP_JUMP_IF_TRUE   2742  'to 2742'
             2738  LOAD_ASSERT              AssertionError
             2740  RAISE_VARARGS_1       1  'exception instance'
           2742_0  COME_FROM          2734  '2734'

 L. 739      2742  LOAD_DEREF               'stack'
             2744  LOAD_METHOD              append
             2746  LOAD_FAST                'obj'
             2748  LOAD_FAST                'idx'
             2750  BINARY_SUBSCR    
             2752  CALL_METHOD_1         1  '1 positional argument'
             2754  POP_TOP          
           2756_0  COME_FROM          2692  '2692'
           2756_1  COME_FROM          2582  '2582'
             2756  JUMP_BACK            94  'to 94'
           2758_0  COME_FROM          2510  '2510'

 L. 740      2758  LOAD_FAST                'opcode'
             2760  LOAD_CONST               104
             2762  COMPARE_OP               ==
         2764_2766  POP_JUMP_IF_FALSE  2830  'to 2830'

 L. 741      2768  LOAD_FAST                'u30'
             2770  CALL_FUNCTION_0       0  '0 positional arguments'
             2772  STORE_FAST               'index'

 L. 742      2774  LOAD_DEREF               'stack'
             2776  LOAD_METHOD              pop
             2778  CALL_METHOD_0         0  '0 positional arguments'
             2780  STORE_FAST               'value'

 L. 743      2782  LOAD_DEREF               'self'
             2784  LOAD_ATTR                multinames
             2786  LOAD_FAST                'index'
             2788  BINARY_SUBSCR    
             2790  STORE_FAST               'idx'

 L. 744      2792  LOAD_GLOBAL              isinstance
             2794  LOAD_FAST                'idx'
             2796  LOAD_GLOBAL              _Multiname
             2798  CALL_FUNCTION_2       2  '2 positional arguments'
         2800_2802  POP_JUMP_IF_FALSE  2812  'to 2812'

 L. 745      2804  LOAD_DEREF               'stack'
             2806  LOAD_METHOD              pop
             2808  CALL_METHOD_0         0  '0 positional arguments'
             2810  STORE_FAST               'idx'
           2812_0  COME_FROM          2800  '2800'

 L. 746      2812  LOAD_DEREF               'stack'
             2814  LOAD_METHOD              pop
             2816  CALL_METHOD_0         0  '0 positional arguments'
             2818  STORE_FAST               'obj'

 L. 747      2820  LOAD_FAST                'value'
             2822  LOAD_FAST                'obj'
             2824  LOAD_FAST                'idx'
             2826  STORE_SUBSCR     
             2828  JUMP_BACK            94  'to 94'
           2830_0  COME_FROM          2764  '2764'

 L. 748      2830  LOAD_FAST                'opcode'
             2832  LOAD_CONST               115
             2834  COMPARE_OP               ==
         2836_2838  POP_JUMP_IF_FALSE  2868  'to 2868'

 L. 749      2840  LOAD_DEREF               'stack'
             2842  LOAD_METHOD              pop
             2844  CALL_METHOD_0         0  '0 positional arguments'
             2846  STORE_FAST               'value'

 L. 750      2848  LOAD_GLOBAL              int
             2850  LOAD_FAST                'value'
             2852  CALL_FUNCTION_1       1  '1 positional argument'
             2854  STORE_FAST               'intvalue'

 L. 751      2856  LOAD_DEREF               'stack'
             2858  LOAD_METHOD              append
             2860  LOAD_FAST                'intvalue'
             2862  CALL_METHOD_1         1  '1 positional argument'
             2864  POP_TOP          
             2866  JUMP_BACK            94  'to 94'
           2868_0  COME_FROM          2836  '2836'

 L. 752      2868  LOAD_FAST                'opcode'
             2870  LOAD_CONST               128
             2872  COMPARE_OP               ==
         2874_2876  POP_JUMP_IF_FALSE  2886  'to 2886'

 L. 753      2878  LOAD_FAST                'u30'
             2880  CALL_FUNCTION_0       0  '0 positional arguments'
             2882  POP_TOP          
             2884  JUMP_BACK            94  'to 94'
           2886_0  COME_FROM          2874  '2874'

 L. 754      2886  LOAD_FAST                'opcode'
             2888  LOAD_CONST               130
             2890  COMPARE_OP               ==
         2892_2894  POP_JUMP_IF_FALSE  2916  'to 2916'

 L. 755      2896  LOAD_DEREF               'stack'
             2898  LOAD_METHOD              pop
             2900  CALL_METHOD_0         0  '0 positional arguments'
             2902  STORE_FAST               'value'

 L. 757      2904  LOAD_DEREF               'stack'
             2906  LOAD_METHOD              append
             2908  LOAD_FAST                'value'
             2910  CALL_METHOD_1         1  '1 positional argument'
             2912  POP_TOP          
             2914  JUMP_BACK            94  'to 94'
           2916_0  COME_FROM          2892  '2892'

 L. 758      2916  LOAD_FAST                'opcode'
             2918  LOAD_CONST               133
             2920  COMPARE_OP               ==
         2922_2924  POP_JUMP_IF_FALSE  2956  'to 2956'

 L. 759      2926  LOAD_GLOBAL              isinstance
             2928  LOAD_DEREF               'stack'
             2930  LOAD_CONST               -1
             2932  BINARY_SUBSCR    
             2934  LOAD_GLOBAL              type
             2936  LOAD_CONST               None
             2938  CALL_FUNCTION_1       1  '1 positional argument'
             2940  LOAD_GLOBAL              compat_str
             2942  BUILD_TUPLE_2         2 
             2944  CALL_FUNCTION_2       2  '2 positional arguments'
         2946_2948  POP_JUMP_IF_TRUE   3668  'to 3668'
             2950  LOAD_ASSERT              AssertionError
             2952  RAISE_VARARGS_1       1  'exception instance'
             2954  JUMP_BACK            94  'to 94'
           2956_0  COME_FROM          2922  '2922'

 L. 760      2956  LOAD_FAST                'opcode'
             2958  LOAD_CONST               147
             2960  COMPARE_OP               ==
         2962_2964  POP_JUMP_IF_FALSE  3006  'to 3006'

 L. 761      2966  LOAD_DEREF               'stack'
             2968  LOAD_METHOD              pop
             2970  CALL_METHOD_0         0  '0 positional arguments'
             2972  STORE_FAST               'value'

 L. 762      2974  LOAD_GLOBAL              isinstance
             2976  LOAD_FAST                'value'
             2978  LOAD_GLOBAL              int
             2980  CALL_FUNCTION_2       2  '2 positional arguments'
         2982_2984  POP_JUMP_IF_TRUE   2990  'to 2990'
             2986  LOAD_ASSERT              AssertionError
             2988  RAISE_VARARGS_1       1  'exception instance'
           2990_0  COME_FROM          2982  '2982'

 L. 763      2990  LOAD_DEREF               'stack'
             2992  LOAD_METHOD              append
             2994  LOAD_FAST                'value'
             2996  LOAD_CONST               1
             2998  BINARY_SUBTRACT  
             3000  CALL_METHOD_1         1  '1 positional argument'
             3002  POP_TOP          
             3004  JUMP_BACK            94  'to 94'
           3006_0  COME_FROM          2962  '2962'

 L. 764      3006  LOAD_FAST                'opcode'
             3008  LOAD_CONST               149
             3010  COMPARE_OP               ==
         3012_3014  POP_JUMP_IF_FALSE  3052  'to 3052'

 L. 765      3016  LOAD_DEREF               'stack'
             3018  LOAD_METHOD              pop
             3020  CALL_METHOD_0         0  '0 positional arguments'
             3022  STORE_FAST               'value'

 L. 767      3024  LOAD_GLOBAL              _Undefined
             3026  LOAD_STR                 'undefined'

 L. 768      3028  LOAD_GLOBAL              compat_str
             3030  LOAD_STR                 'String'

 L. 769      3032  LOAD_GLOBAL              int
             3034  LOAD_STR                 'Number'

 L. 770      3036  LOAD_GLOBAL              float
             3038  LOAD_STR                 'Number'
             3040  BUILD_MAP_4           4 

 L. 771      3042  LOAD_GLOBAL              type
             3044  LOAD_FAST                'value'
             3046  CALL_FUNCTION_1       1  '1 positional argument'
             3048  BINARY_SUBSCR    
             3050  RETURN_VALUE     
           3052_0  COME_FROM          3012  '3012'

 L. 772      3052  LOAD_FAST                'opcode'
             3054  LOAD_CONST               160
             3056  COMPARE_OP               ==
         3058_3060  POP_JUMP_IF_FALSE  3098  'to 3098'

 L. 773      3062  LOAD_DEREF               'stack'
             3064  LOAD_METHOD              pop
             3066  CALL_METHOD_0         0  '0 positional arguments'
             3068  STORE_FAST               'value2'

 L. 774      3070  LOAD_DEREF               'stack'
             3072  LOAD_METHOD              pop
             3074  CALL_METHOD_0         0  '0 positional arguments'
             3076  STORE_FAST               'value1'

 L. 775      3078  LOAD_FAST                'value1'
             3080  LOAD_FAST                'value2'
             3082  BINARY_ADD       
             3084  STORE_FAST               'res'

 L. 776      3086  LOAD_DEREF               'stack'
             3088  LOAD_METHOD              append
             3090  LOAD_FAST                'res'
             3092  CALL_METHOD_1         1  '1 positional argument'
             3094  POP_TOP          
             3096  JUMP_BACK            94  'to 94'
           3098_0  COME_FROM          3058  '3058'

 L. 777      3098  LOAD_FAST                'opcode'
             3100  LOAD_CONST               161
             3102  COMPARE_OP               ==
         3104_3106  POP_JUMP_IF_FALSE  3144  'to 3144'

 L. 778      3108  LOAD_DEREF               'stack'
             3110  LOAD_METHOD              pop
             3112  CALL_METHOD_0         0  '0 positional arguments'
             3114  STORE_FAST               'value2'

 L. 779      3116  LOAD_DEREF               'stack'
             3118  LOAD_METHOD              pop
             3120  CALL_METHOD_0         0  '0 positional arguments'
             3122  STORE_FAST               'value1'

 L. 780      3124  LOAD_FAST                'value1'
             3126  LOAD_FAST                'value2'
             3128  BINARY_SUBTRACT  
             3130  STORE_FAST               'res'

 L. 781      3132  LOAD_DEREF               'stack'
             3134  LOAD_METHOD              append
             3136  LOAD_FAST                'res'
             3138  CALL_METHOD_1         1  '1 positional argument'
             3140  POP_TOP          
             3142  JUMP_BACK            94  'to 94'
           3144_0  COME_FROM          3104  '3104'

 L. 782      3144  LOAD_FAST                'opcode'
             3146  LOAD_CONST               162
             3148  COMPARE_OP               ==
         3150_3152  POP_JUMP_IF_FALSE  3190  'to 3190'

 L. 783      3154  LOAD_DEREF               'stack'
             3156  LOAD_METHOD              pop
             3158  CALL_METHOD_0         0  '0 positional arguments'
             3160  STORE_FAST               'value2'

 L. 784      3162  LOAD_DEREF               'stack'
             3164  LOAD_METHOD              pop
             3166  CALL_METHOD_0         0  '0 positional arguments'
             3168  STORE_FAST               'value1'

 L. 785      3170  LOAD_FAST                'value1'
             3172  LOAD_FAST                'value2'
             3174  BINARY_MULTIPLY  
             3176  STORE_FAST               'res'

 L. 786      3178  LOAD_DEREF               'stack'
             3180  LOAD_METHOD              append
             3182  LOAD_FAST                'res'
             3184  CALL_METHOD_1         1  '1 positional argument'
             3186  POP_TOP          
             3188  JUMP_BACK            94  'to 94'
           3190_0  COME_FROM          3150  '3150'

 L. 787      3190  LOAD_FAST                'opcode'
             3192  LOAD_CONST               164
             3194  COMPARE_OP               ==
         3196_3198  POP_JUMP_IF_FALSE  3236  'to 3236'

 L. 788      3200  LOAD_DEREF               'stack'
             3202  LOAD_METHOD              pop
             3204  CALL_METHOD_0         0  '0 positional arguments'
             3206  STORE_FAST               'value2'

 L. 789      3208  LOAD_DEREF               'stack'
             3210  LOAD_METHOD              pop
             3212  CALL_METHOD_0         0  '0 positional arguments'
             3214  STORE_FAST               'value1'

 L. 790      3216  LOAD_FAST                'value1'
             3218  LOAD_FAST                'value2'
             3220  BINARY_MODULO    
             3222  STORE_FAST               'res'

 L. 791      3224  LOAD_DEREF               'stack'
             3226  LOAD_METHOD              append
             3228  LOAD_FAST                'res'
             3230  CALL_METHOD_1         1  '1 positional argument'
             3232  POP_TOP          
             3234  JUMP_BACK            94  'to 94'
           3236_0  COME_FROM          3196  '3196'

 L. 792      3236  LOAD_FAST                'opcode'
             3238  LOAD_CONST               168
             3240  COMPARE_OP               ==
         3242_3244  POP_JUMP_IF_FALSE  3314  'to 3314'

 L. 793      3246  LOAD_DEREF               'stack'
             3248  LOAD_METHOD              pop
             3250  CALL_METHOD_0         0  '0 positional arguments'
             3252  STORE_FAST               'value2'

 L. 794      3254  LOAD_DEREF               'stack'
             3256  LOAD_METHOD              pop
             3258  CALL_METHOD_0         0  '0 positional arguments'
             3260  STORE_FAST               'value1'

 L. 795      3262  LOAD_GLOBAL              isinstance
             3264  LOAD_FAST                'value1'
             3266  LOAD_GLOBAL              int
             3268  CALL_FUNCTION_2       2  '2 positional arguments'
         3270_3272  POP_JUMP_IF_TRUE   3278  'to 3278'
             3274  LOAD_ASSERT              AssertionError
             3276  RAISE_VARARGS_1       1  'exception instance'
           3278_0  COME_FROM          3270  '3270'

 L. 796      3278  LOAD_GLOBAL              isinstance
             3280  LOAD_FAST                'value2'
             3282  LOAD_GLOBAL              int
             3284  CALL_FUNCTION_2       2  '2 positional arguments'
         3286_3288  POP_JUMP_IF_TRUE   3294  'to 3294'
             3290  LOAD_ASSERT              AssertionError
             3292  RAISE_VARARGS_1       1  'exception instance'
           3294_0  COME_FROM          3286  '3286'

 L. 797      3294  LOAD_FAST                'value1'
             3296  LOAD_FAST                'value2'
             3298  BINARY_AND       
             3300  STORE_FAST               'res'

 L. 798      3302  LOAD_DEREF               'stack'
             3304  LOAD_METHOD              append
             3306  LOAD_FAST                'res'
             3308  CALL_METHOD_1         1  '1 positional argument'
             3310  POP_TOP          
             3312  JUMP_BACK            94  'to 94'
           3314_0  COME_FROM          3242  '3242'

 L. 799      3314  LOAD_FAST                'opcode'
             3316  LOAD_CONST               171
             3318  COMPARE_OP               ==
         3320_3322  POP_JUMP_IF_FALSE  3360  'to 3360'

 L. 800      3324  LOAD_DEREF               'stack'
             3326  LOAD_METHOD              pop
             3328  CALL_METHOD_0         0  '0 positional arguments'
             3330  STORE_FAST               'value2'

 L. 801      3332  LOAD_DEREF               'stack'
             3334  LOAD_METHOD              pop
             3336  CALL_METHOD_0         0  '0 positional arguments'
             3338  STORE_FAST               'value1'

 L. 802      3340  LOAD_FAST                'value1'
             3342  LOAD_FAST                'value2'
             3344  COMPARE_OP               ==
             3346  STORE_FAST               'result'

 L. 803      3348  LOAD_DEREF               'stack'
             3350  LOAD_METHOD              append
             3352  LOAD_FAST                'result'
             3354  CALL_METHOD_1         1  '1 positional argument'
             3356  POP_TOP          
             3358  JUMP_BACK            94  'to 94'
           3360_0  COME_FROM          3320  '3320'

 L. 804      3360  LOAD_FAST                'opcode'
             3362  LOAD_CONST               175
             3364  COMPARE_OP               ==
         3366_3368  POP_JUMP_IF_FALSE  3406  'to 3406'

 L. 805      3370  LOAD_DEREF               'stack'
             3372  LOAD_METHOD              pop
             3374  CALL_METHOD_0         0  '0 positional arguments'
             3376  STORE_FAST               'value2'

 L. 806      3378  LOAD_DEREF               'stack'
             3380  LOAD_METHOD              pop
             3382  CALL_METHOD_0         0  '0 positional arguments'
             3384  STORE_FAST               'value1'

 L. 807      3386  LOAD_FAST                'value1'
             3388  LOAD_FAST                'value2'
             3390  COMPARE_OP               >=
             3392  STORE_FAST               'result'

 L. 808      3394  LOAD_DEREF               'stack'
             3396  LOAD_METHOD              append
             3398  LOAD_FAST                'result'
             3400  CALL_METHOD_1         1  '1 positional argument'
             3402  POP_TOP          
             3404  JUMP_BACK            94  'to 94'
           3406_0  COME_FROM          3366  '3366'

 L. 809      3406  LOAD_FAST                'opcode'
             3408  LOAD_CONST               192
             3410  COMPARE_OP               ==
         3412_3414  POP_JUMP_IF_FALSE  3456  'to 3456'

 L. 810      3416  LOAD_DEREF               'stack'
             3418  LOAD_METHOD              pop
             3420  CALL_METHOD_0         0  '0 positional arguments'
             3422  STORE_FAST               'value'

 L. 811      3424  LOAD_GLOBAL              isinstance
             3426  LOAD_FAST                'value'
             3428  LOAD_GLOBAL              int
             3430  CALL_FUNCTION_2       2  '2 positional arguments'
         3432_3434  POP_JUMP_IF_TRUE   3440  'to 3440'
             3436  LOAD_ASSERT              AssertionError
             3438  RAISE_VARARGS_1       1  'exception instance'
           3440_0  COME_FROM          3432  '3432'

 L. 812      3440  LOAD_DEREF               'stack'
             3442  LOAD_METHOD              append
             3444  LOAD_FAST                'value'
             3446  LOAD_CONST               1
             3448  BINARY_ADD       
             3450  CALL_METHOD_1         1  '1 positional argument'
             3452  POP_TOP          
             3454  JUMP_BACK            94  'to 94'
           3456_0  COME_FROM          3412  '3412'

 L. 813      3456  LOAD_FAST                'opcode'
             3458  LOAD_CONST               208
             3460  COMPARE_OP               ==
         3462_3464  POP_JUMP_IF_FALSE  3482  'to 3482'

 L. 814      3466  LOAD_DEREF               'stack'
             3468  LOAD_METHOD              append
             3470  LOAD_FAST                'registers'
             3472  LOAD_CONST               0
             3474  BINARY_SUBSCR    
             3476  CALL_METHOD_1         1  '1 positional argument'
             3478  POP_TOP          
             3480  JUMP_BACK            94  'to 94'
           3482_0  COME_FROM          3462  '3462'

 L. 815      3482  LOAD_FAST                'opcode'
             3484  LOAD_CONST               209
             3486  COMPARE_OP               ==
         3488_3490  POP_JUMP_IF_FALSE  3508  'to 3508'

 L. 816      3492  LOAD_DEREF               'stack'
             3494  LOAD_METHOD              append
             3496  LOAD_FAST                'registers'
             3498  LOAD_CONST               1
             3500  BINARY_SUBSCR    
             3502  CALL_METHOD_1         1  '1 positional argument'
             3504  POP_TOP          
             3506  JUMP_BACK            94  'to 94'
           3508_0  COME_FROM          3488  '3488'

 L. 817      3508  LOAD_FAST                'opcode'
             3510  LOAD_CONST               210
             3512  COMPARE_OP               ==
         3514_3516  POP_JUMP_IF_FALSE  3534  'to 3534'

 L. 818      3518  LOAD_DEREF               'stack'
             3520  LOAD_METHOD              append
             3522  LOAD_FAST                'registers'
             3524  LOAD_CONST               2
             3526  BINARY_SUBSCR    
             3528  CALL_METHOD_1         1  '1 positional argument'
             3530  POP_TOP          
             3532  JUMP_BACK            94  'to 94'
           3534_0  COME_FROM          3514  '3514'

 L. 819      3534  LOAD_FAST                'opcode'
             3536  LOAD_CONST               211
             3538  COMPARE_OP               ==
         3540_3542  POP_JUMP_IF_FALSE  3560  'to 3560'

 L. 820      3544  LOAD_DEREF               'stack'
             3546  LOAD_METHOD              append
             3548  LOAD_FAST                'registers'
             3550  LOAD_CONST               3
             3552  BINARY_SUBSCR    
             3554  CALL_METHOD_1         1  '1 positional argument'
             3556  POP_TOP          
             3558  JUMP_BACK            94  'to 94'
           3560_0  COME_FROM          3540  '3540'

 L. 821      3560  LOAD_FAST                'opcode'
             3562  LOAD_CONST               212
             3564  COMPARE_OP               ==
         3566_3568  POP_JUMP_IF_FALSE  3584  'to 3584'

 L. 822      3570  LOAD_DEREF               'stack'
             3572  LOAD_METHOD              pop
             3574  CALL_METHOD_0         0  '0 positional arguments'
             3576  LOAD_FAST                'registers'
             3578  LOAD_CONST               0
             3580  STORE_SUBSCR     
             3582  JUMP_BACK            94  'to 94'
           3584_0  COME_FROM          3566  '3566'

 L. 823      3584  LOAD_FAST                'opcode'
             3586  LOAD_CONST               213
             3588  COMPARE_OP               ==
         3590_3592  POP_JUMP_IF_FALSE  3608  'to 3608'

 L. 824      3594  LOAD_DEREF               'stack'
             3596  LOAD_METHOD              pop
             3598  CALL_METHOD_0         0  '0 positional arguments'
             3600  LOAD_FAST                'registers'
             3602  LOAD_CONST               1
             3604  STORE_SUBSCR     
             3606  JUMP_BACK            94  'to 94'
           3608_0  COME_FROM          3590  '3590'

 L. 825      3608  LOAD_FAST                'opcode'
             3610  LOAD_CONST               214
             3612  COMPARE_OP               ==
         3614_3616  POP_JUMP_IF_FALSE  3632  'to 3632'

 L. 826      3618  LOAD_DEREF               'stack'
             3620  LOAD_METHOD              pop
             3622  CALL_METHOD_0         0  '0 positional arguments'
             3624  LOAD_FAST                'registers'
             3626  LOAD_CONST               2
             3628  STORE_SUBSCR     
             3630  JUMP_BACK            94  'to 94'
           3632_0  COME_FROM          3614  '3614'

 L. 827      3632  LOAD_FAST                'opcode'
             3634  LOAD_CONST               215
             3636  COMPARE_OP               ==
         3638_3640  POP_JUMP_IF_FALSE  3656  'to 3656'

 L. 828      3642  LOAD_DEREF               'stack'
             3644  LOAD_METHOD              pop
             3646  CALL_METHOD_0         0  '0 positional arguments'
             3648  LOAD_FAST                'registers'
             3650  LOAD_CONST               3
             3652  STORE_SUBSCR     
             3654  JUMP_BACK            94  'to 94'
           3656_0  COME_FROM          3638  '3638'

 L. 830      3656  LOAD_GLOBAL              NotImplementedError

 L. 831      3658  LOAD_STR                 'Unsupported opcode %d'
             3660  LOAD_FAST                'opcode'
             3662  BINARY_MODULO    
             3664  CALL_FUNCTION_1       1  '1 positional argument'
             3666  RAISE_VARARGS_1       1  'exception instance'
           3668_0  COME_FROM          2946  '2946'
           3668_1  COME_FROM           400  '400'
           3668_2  COME_FROM           338  '338'
           3668_3  COME_FROM           276  '276'
             3668  JUMP_BACK            94  'to 94'
             3670  POP_BLOCK        
           3672_0  COME_FROM_LOOP       90  '90'

Parse error at or near `COME_FROM' instruction at offset 1490_0

        avm_class.method_pyfunctions[func_name] = resfunc
        return resfunc