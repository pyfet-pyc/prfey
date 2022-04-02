# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: keyboard\_keyboard_event.py
from time import time as now
import json
from ._canonical_names import canonical_names, normalize_name
try:
    basestring
except NameError:
    basestring = str

KEY_DOWN = 'down'
KEY_UP = 'up'

class KeyboardEvent(object):
    event_type = None
    scan_code = None
    name = None
    time = None
    device = None
    modifiers = None
    is_keypad = None

    def __init__(self, event_type, scan_code, name=None, time=None, device=None, modifiers=None, is_keypad=None):
        self.event_type = event_type
        self.scan_code = scan_code
        self.time = now() if time is None else time
        self.device = device
        self.is_keypad = is_keypad
        self.modifiers = modifiers
        if name:
            self.name = normalize_name(name)

    def to_json(self, ensure_ascii=False):
        attrs = dict(((attr, getattr(self, attr)) for attr in ('event_type', 'scan_code',
                                                               'name', 'time', 'device',
                                                               'is_keypad') if not attr.startswith('_') if getattr(self, attr) is not None))
        return json.dumps(attrs, ensure_ascii=ensure_ascii)

    def __repr__(self):
        return 'KeyboardEvent({} {})'.format(self.name or 'Unknown {}'.format(self.scan_code), self.event_type)

    def __eq__--- This code section failed: ---

 L.  46         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'other'
                4  LOAD_GLOBAL              KeyboardEvent
                6  CALL_FUNCTION_2       2  '2 positional arguments'
                8  JUMP_IF_FALSE_OR_POP    76  'to 76'

 L.  47        10  LOAD_FAST                'self'
               12  LOAD_ATTR                event_type
               14  LOAD_FAST                'other'
               16  LOAD_ATTR                event_type
               18  COMPARE_OP               ==
               20  JUMP_IF_FALSE_OR_POP    76  'to 76'

 L.  49        22  LOAD_FAST                'self'
               24  LOAD_ATTR                scan_code
               26  UNARY_NOT        
               28  POP_JUMP_IF_TRUE     50  'to 50'
               30  LOAD_FAST                'other'
               32  LOAD_ATTR                scan_code
               34  UNARY_NOT        
               36  POP_JUMP_IF_TRUE     50  'to 50'
               38  LOAD_FAST                'self'
               40  LOAD_ATTR                scan_code
               42  LOAD_FAST                'other'
               44  LOAD_ATTR                scan_code
               46  COMPARE_OP               ==
               48  JUMP_IF_FALSE_OR_POP    76  'to 76'
             50_0  COME_FROM            36  '36'
             50_1  COME_FROM            28  '28'

 L.  51        50  LOAD_FAST                'self'
               52  LOAD_ATTR                name
               54  UNARY_NOT        
               56  JUMP_IF_TRUE_OR_POP    76  'to 76'
               58  LOAD_FAST                'other'
               60  LOAD_ATTR                name
               62  UNARY_NOT        
               64  JUMP_IF_TRUE_OR_POP    76  'to 76'
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                name
               70  LOAD_FAST                'other'
               72  LOAD_ATTR                name
               74  COMPARE_OP               ==
             76_0  COME_FROM            64  '64'
             76_1  COME_FROM            56  '56'
             76_2  COME_FROM            48  '48'
             76_3  COME_FROM            20  '20'
             76_4  COME_FROM             8  '8'
               76  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 76_4