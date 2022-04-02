# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\openpyxl\utils\cell.py
"""
Collection of utilities used within the package and also available for client code
"""
import re
from string import digits
from .exceptions import CellCoordinatesException
COORD_RE = re.compile('^[$]?([A-Za-z]{1,3})[$]?(\\d+)$')
COL_RANGE = '[A-Z]{1,3}:[A-Z]{1,3}:'
ROW_RANGE = '\\d+:\\d+:'
RANGE_EXPR = '\n[$]?(?P<min_col>[A-Za-z]{1,3})?\n[$]?(?P<min_row>\\d+)?\n(:[$]?(?P<max_col>[A-Za-z]{1,3})?\n[$]?(?P<max_row>\\d+)?)?\n'
ABSOLUTE_RE = re.compile('^' + RANGE_EXPR + '$', re.VERBOSE)
SHEET_TITLE = "\n(('(?P<quoted>([^']|'')*)')|(?P<notquoted>[^'^ ^!]*))!"
SHEETRANGE_RE = re.compile('{0}(?P<cells>{1})(?=,?)'.format(SHEET_TITLE, RANGE_EXPR), re.VERBOSE)

def get_column_interval(start, end):
    """
    Given the start and end columns, return all the columns in the series.

    The start and end columns can be either column letters or 1-based
    indexes.
    """
    if isinstance(start, str):
        start = column_index_from_string(start)
    if isinstance(end, str):
        end = column_index_from_string(end)
    return [get_column_letter(x) for x in range(start, end + 1)]


def coordinate_from_string(coord_string):
    """Convert a coordinate string like 'B12' to a tuple ('B', 12)"""
    match = COORD_RE.match(coord_string)
    if not match:
        msg = f"Invalid cell coordinates ({coord_string})"
        raise CellCoordinatesException(msg)
    column, row = match.groups()
    row = int(row)
    if not row:
        msg = f"There is no row 0 ({coord_string})"
        raise CellCoordinatesException(msg)
    return (
     column, row)


def absolute_coordinate(coord_string):
    """Convert a coordinate to an absolute coordinate string (B12 -> $B$12)"""
    m = ABSOLUTE_RE.match(coord_string)
    if not m:
        raise ValueError(f"{coord_string} is not a valid coordinate range")
    d = m.groupdict('')
    for k, v in d.items():
        if v:
            d[k] = f"${v}"
        if d['max_col'] or d['max_row']:
            fmt = '{min_col}{min_row}:{max_col}{max_row}'
        else:
            fmt = '{min_col}{min_row}'
        return (fmt.format)(**d)


def _get_column_letter(col_idx):
    """Convert a column number into a column letter (3 -> 'C')

    Right shift the column col_idx by 26 to find column letters in reverse
    order.  These numbers are 1-based, and can be converted to ASCII
    ordinals by adding 64.

    """
    if not 1 <= col_idx <= 18278:
        raise ValueError('Invalid column index {0}'.format(col_idx))
    else:
        letters = []
        while True:
            if col_idx > 0:
                col_idx, remainder = divmod(col_idx, 26)
                if remainder == 0:
                    remainder = 26
                    col_idx -= 1
                letters.append(chr(remainder + 64))

    return ''.join(reversed(letters))


_COL_STRING_CACHE = {}
_STRING_COL_CACHE = {}
for i in range(1, 18279):
    col = _get_column_letter(i)
    _STRING_COL_CACHE[i] = col
    _COL_STRING_CACHE[col] = i
else:

    def get_column_letter--- This code section failed: ---

 L. 109         0  SETUP_FINALLY        12  'to 12'

 L. 110         2  LOAD_GLOBAL              _STRING_COL_CACHE
                4  LOAD_FAST                'idx'
                6  BINARY_SUBSCR    
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L. 111        12  DUP_TOP          
               14  LOAD_GLOBAL              KeyError
               16  COMPARE_OP               exception-match
               18  POP_JUMP_IF_FALSE    44  'to 44'
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L. 112        26  LOAD_GLOBAL              ValueError
               28  LOAD_STR                 'Invalid column index {0}'
               30  LOAD_METHOD              format
               32  LOAD_FAST                'idx'
               34  CALL_METHOD_1         1  ''
               36  CALL_FUNCTION_1       1  ''
               38  RAISE_VARARGS_1       1  'exception instance'
               40  POP_EXCEPT       
               42  JUMP_FORWARD         46  'to 46'
             44_0  COME_FROM            18  '18'
               44  END_FINALLY      
             46_0  COME_FROM            42  '42'

Parse error at or near `POP_TOP' instruction at offset 22


    def column_index_from_string--- This code section failed: ---

 L. 120         0  SETUP_FINALLY        16  'to 16'

 L. 121         2  LOAD_GLOBAL              _COL_STRING_CACHE
                4  LOAD_FAST                'str_col'
                6  LOAD_METHOD              upper
                8  CALL_METHOD_0         0  ''
               10  BINARY_SUBSCR    
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L. 122        16  DUP_TOP          
               18  LOAD_GLOBAL              KeyError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    48  'to 48'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 123        30  LOAD_GLOBAL              ValueError
               32  LOAD_STR                 '{0} is not a valid column name'
               34  LOAD_METHOD              format
               36  LOAD_FAST                'str_col'
               38  CALL_METHOD_1         1  ''
               40  CALL_FUNCTION_1       1  ''
               42  RAISE_VARARGS_1       1  'exception instance'
               44  POP_EXCEPT       
               46  JUMP_FORWARD         50  'to 50'
             48_0  COME_FROM            22  '22'
               48  END_FINALLY      
             50_0  COME_FROM            46  '46'

Parse error at or near `POP_TOP' instruction at offset 26


    def range_boundaries(range_string):
        """
    Convert a range string into a tuple of boundaries:
    (min_col, min_row, max_col, max_row)
    Cell coordinates will be converted into a range with the cell at both end
    """
        msg = '{0} is not a valid coordinate or range'.format(range_string)
        m = ABSOLUTE_RE.match(range_string)
        if not m:
            raise ValueError(msg)
        else:
            min_col, min_row, sep, max_col, max_row = m.groups()
            if sep:
                cols = (
                 min_col, max_col)
                rows = (min_row, max_row)
                if all(cols + rows) or all(cols):
                    if any(rows):
                        if not all(rows) or any(cols):
                            raise ValueError(msg)
                else:
                    if min_col is not None:
                        min_col = column_index_from_string(min_col)
                    if min_row is not None:
                        min_row = int(min_row)
                    if max_col is not None:
                        max_col = column_index_from_string(max_col)
                    else:
                        max_col = min_col
                if max_row is not None:
                    max_row = int(max_row)
            else:
                max_row = min_row
        return (
         min_col, min_row, max_col, max_row)


    def rows_from_range(range_string):
        """
    Get individual addresses for every cell in a range.
    Yields one row at a time.
    """
        min_col, min_row, max_col, max_row = range_boundaries(range_string)
        rows = range(min_row, max_row + 1)
        cols = [get_column_letter(col) for col in range(min_col, max_col + 1)]
        for row in rows:
            (yield tuple(('{0}{1}'.format(col, row) for col in cols)))


    def cols_from_range(range_string):
        """
    Get individual addresses for every cell in a range.
    Yields one row at a time.
    """
        min_col, min_row, max_col, max_row = range_boundaries(range_string)
        rows = range(min_row, max_row + 1)
        cols = (get_column_letter(col) for col in range(min_col, max_col + 1))
        for col in cols:
            (yield tuple(('{0}{1}'.format(col, row) for row in rows)))


    def coordinate_to_tuple(coordinate):
        """
    Convert an Excel style coordinate to (row, colum) tuple
    """
        for idx, c in enumerate(coordinate):
            if c in digits:
                break
            col = coordinate[:idx].upper()
            row = coordinate[idx:]
            return (int(row), _COL_STRING_CACHE[col])


    def range_to_tuple(range_string):
        """
    Convert a worksheet range to the sheetname and maximum and minimum
    coordinate indices
    """
        m = SHEETRANGE_RE.match(range_string)
        if m is None:
            raise ValueError('Value must be of the form sheetname!A1:E4')
        sheetname = m.group('quoted') or m.group('notquoted')
        cells = m.group('cells')
        boundaries = range_boundaries(cells)
        return (sheetname, boundaries)


    def quote_sheetname(sheetname):
        """
    Add quotes around sheetnames if they contain spaces.
    """
        if "'" in sheetname:
            sheetname = sheetname.replace("'", "''")
        sheetname = "'{0}'".format(sheetname)
        return sheetname