# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\openpyxl\workbook\defined_name.py
import re
from openpyxl.descriptors.serialisable import Serialisable
from openpyxl.descriptors import Alias, Typed, String, Float, Integer, Bool, NoneSet, Set, Sequence, Descriptor
from openpyxl.compat import safe_string
from openpyxl.formula import Tokenizer
from openpyxl.utils.cell import SHEETRANGE_RE, SHEET_TITLE
RESERVED = frozenset(['Print_Area', 'Print_Titles', 'Criteria',
 '_FilterDatabase', 'Extract', 'Consolidate_Area',
 'Sheet_Title'])
_names = '|'.join(RESERVED)
RESERVED_REGEX = re.compile('^_xlnm\\.(?P<name>{0})'.format(_names))
COL_RANGE = '(?P<cols>[$]?[a-zA-Z]{1,3}:[$]?[a-zA-Z]{1,3})'
COL_RANGE_RE = re.compile(COL_RANGE)
ROW_RANGE = '(?P<rows>[$]?\\d+:[$]?\\d+)'
ROW_RANGE_RE = re.compile(ROW_RANGE)
TITLES_REGEX = re.compile('{0}{1}?,?{2}?'.format(SHEET_TITLE, ROW_RANGE, COL_RANGE), re.VERBOSE)

def _unpack_print_titles(defn):
    """
    Extract rows and or columns from print titles so that they can be
    assigned to a worksheet
    """
    scanner = TITLES_REGEX.finditer(defn.value)
    kw = dict(((k, v) for match in scanner for k, v in match.groupdict().items()))
    return (
     kw.get('rows'), kw.get('cols'))


def _unpack_print_area(defn):
    """
    Extract print area
    """
    new = []
    for m in SHEETRANGE_RE.finditer(defn.value):
        coord = m.group('cells')
        if coord:
            new.append(coord)
    else:
        return new


class DefinedName(Serialisable):
    tagname = 'definedName'
    name = String()
    comment = String(allow_none=True)
    customMenu = String(allow_none=True)
    description = String(allow_none=True)
    help = String(allow_none=True)
    statusBar = String(allow_none=True)
    localSheetId = Integer(allow_none=True)
    hidden = Bool(allow_none=True)
    function = Bool(allow_none=True)
    vbProcedure = Bool(allow_none=True)
    xlm = Bool(allow_none=True)
    functionGroupId = Integer(allow_none=True)
    shortcutKey = String(allow_none=True)
    publishToServer = Bool(allow_none=True)
    workbookParameter = Bool(allow_none=True)
    attr_text = Descriptor()
    value = Alias('attr_text')

    def __init__(self, name=None, comment=None, customMenu=None, description=None, help=None, statusBar=None, localSheetId=None, hidden=None, function=None, vbProcedure=None, xlm=None, functionGroupId=None, shortcutKey=None, publishToServer=None, workbookParameter=None, attr_text=None):
        self.name = name
        self.comment = comment
        self.customMenu = customMenu
        self.description = description
        self.help = help
        self.statusBar = statusBar
        self.localSheetId = localSheetId
        self.hidden = hidden
        self.function = function
        self.vbProcedure = vbProcedure
        self.xlm = xlm
        self.functionGroupId = functionGroupId
        self.shortcutKey = shortcutKey
        self.publishToServer = publishToServer
        self.workbookParameter = workbookParameter
        self.attr_text = attr_text

    @property
    def type(self):
        tok = Tokenizer('=' + self.value)
        parsed = tok.items[0]
        if parsed.type == 'OPERAND':
            return parsed.subtype
        return parsed.type

    @property
    def destinations(self):
        if self.type == 'RANGE':
            tok = Tokenizer('=' + self.value)
            for part in tok.items:
                if part.subtype == 'RANGE':
                    m = SHEETRANGE_RE.match(part.value)
                    sheetname = m.group('notquoted') or m.group('quoted')
                    yield (sheetname, m.group('cells'))

    @property
    def is_reserved(self):
        m = RESERVED_REGEX.match(self.name)
        if m:
            return m.group('name')

    @property
    def is_external(self):
        return re.compile('^\\[\\d+\\].*').match(self.value) is not None

    def __iter__(self):
        for key in self.__attrs__:
            if key == 'attr_text':
                pass
            else:
                v = getattr(self, key)
                if v is not None:
                    if v in RESERVED:
                        v = '_xlnm.' + v
                    else:
                        yield (
                         key, safe_string(v))


class DefinedNameList(Serialisable):
    tagname = 'definedNames'
    definedName = Sequence(expected_type=DefinedName)

    def __init__(self, definedName=()):
        self.definedName = definedName

    def _cleanup--- This code section failed: ---

 L. 182         0  BUILD_LIST_0          0 
                2  STORE_FAST               'valid_names'

 L. 183         4  LOAD_FAST                'self'
                6  LOAD_ATTR                definedName
                8  GET_ITER         
             10_0  COME_FROM            60  '60'
             10_1  COME_FROM            48  '48'
             10_2  COME_FROM            34  '34'
               10  FOR_ITER             62  'to 62'
               12  STORE_FAST               'n'

 L. 184        14  LOAD_FAST                'n'
               16  LOAD_ATTR                name
               18  LOAD_CONST               ('_xlnm.Print_Titles', '_xlnm.Print_Area')
               20  COMPARE_OP               in
               22  POP_JUMP_IF_FALSE    38  'to 38'
               24  LOAD_FAST                'n'
               26  LOAD_ATTR                localSheetId
               28  LOAD_CONST               None
               30  COMPARE_OP               is
               32  POP_JUMP_IF_FALSE    38  'to 38'

 L. 185        34  JUMP_BACK            10  'to 10'
               36  BREAK_LOOP           50  'to 50'
             38_0  COME_FROM            32  '32'
             38_1  COME_FROM            22  '22'

 L. 186        38  LOAD_FAST                'n'
               40  LOAD_ATTR                name
               42  LOAD_STR                 '_xlnm._FilterDatabase'
               44  COMPARE_OP               ==
               46  POP_JUMP_IF_FALSE    50  'to 50'

 L. 187        48  JUMP_BACK            10  'to 10'
             50_0  COME_FROM            46  '46'
             50_1  COME_FROM            36  '36'

 L. 188        50  LOAD_FAST                'valid_names'
               52  LOAD_METHOD              append
               54  LOAD_FAST                'n'
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          
               60  JUMP_BACK            10  'to 10'
             62_0  COME_FROM            10  '10'

 L. 189        62  LOAD_FAST                'valid_names'
               64  LOAD_FAST                'self'
               66  STORE_ATTR               definedName

Parse error at or near `LOAD_FAST' instruction at offset 62

    def _duplicate(self, defn):
        """
        Check for whether DefinedName with the same name and scope already
        exists
        """
        for d in self.definedName:
            if d.name == defn.name:
                if d.localSheetId == defn.localSheetId:
                    return True

    def append(self, defn):
        if not isinstance(defn, DefinedName):
            raise TypeError('You can only append DefinedNames')
        if self._duplicate(defn):
            raise ValueError('DefinedName with the same name and scope already exists')
        names = self.definedName[:]
        names.append(defn)
        self.definedName = names

    def __len__(self):
        return len(self.definedName)

    def __contains__(self, name):
        """
        See if a globaly defined name exists
        """
        for defn in self.definedName:
            if defn.name == name:
                if defn.localSheetId is None:
                    return True

    def __getitem__(self, name):
        """
        Get globally defined name
        """
        defn = self.get(name)
        if not defn:
            raise KeyError('No definition called {0}'.format(name))
        return defn

    def get(self, name, scope=None):
        """
        Get the name assigned to a specicic sheet or global
        """
        for defn in self.definedName:
            if defn.name == name:
                if defn.localSheetId == scope:
                    return defn

    def __delitem__(self, name):
        """
        Delete a globally defined name
        """
        if not self.delete(name):
            raise KeyError('No globally defined name {0}'.format(name))

    def delete(self, name, scope=None):
        """
        Delete a name assigned to a specific or global
        """
        for idx, defn in enumerate(self.definedName):
            if defn.name == name:
                if defn.localSheetId == scope:
                    del self.definedName[idx]
                    return True

    def localnames(self, scope):
        """
        Provide a list of all names for a particular worksheet
        """
        return [defn.name for defn in self.definedName if defn.localSheetId == scope]