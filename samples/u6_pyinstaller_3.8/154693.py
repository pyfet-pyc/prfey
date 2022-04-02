# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\openpyxl\formula\translate.py
"""
This module contains code to translate formulae across cells in a worksheet.

The idea is that if A1 has formula "=B1+C1", then translating it to cell A2
results in formula "=B2+C2". The algorithm relies on the formula tokenizer
to identify the parts of the formula that need to change.

"""
import re
from .tokenizer import Tokenizer, Token
from openpyxl.utils import coordinate_to_tuple, column_index_from_string, get_column_letter

class TranslatorError(Exception):
    __doc__ = "\n    Raised when a formula can't be translated across cells.\n\n    This error arises when a formula's references would be translated outside\n    the worksheet's bounds on the top or left. Excel represents these\n    situations with a #REF! literal error. E.g., if the formula at B2 is\n    '=A1', attempting to translate the formula to B1 raises TranslatorError,\n    since there's no cell above A1. Similarly, translating the same formula\n    from B2 to A2 raises TranslatorError, since there's no cell to the left of\n    A1.\n\n    "


class Translator(object):
    __doc__ = "\n    Modifies a formula so that it can be translated from one cell to another.\n\n    `formula`: The str string to translate. Must include the leading '='\n               character.\n    `origin`: The cell address (in A1 notation) where this formula was\n              defined (excluding the worksheet name).\n\n    "

    def __init__(self, formula, origin):
        self.row, self.col = coordinate_to_tuple(origin)
        self.tokenizer = Tokenizer(formula)

    def get_tokens(self):
        """Returns a list with the tokens comprising the formula."""
        return self.tokenizer.items

    ROW_RANGE_RE = re.compile('(\\$?[1-9][0-9]{0,6}):(\\$?[1-9][0-9]{0,6})$')
    COL_RANGE_RE = re.compile('(\\$?[A-Za-z]{1,3}):(\\$?[A-Za-z]{1,3})$')
    CELL_REF_RE = re.compile('(\\$?[A-Za-z]{1,3})(\\$?[1-9][0-9]{0,6})$')

    @staticmethod
    def translate_row(row_str, rdelta):
        """
        Translate a range row-snippet by the given number of rows.
        """
        if row_str.startswith('$'):
            return row_str
        new_row = int(row_str) + rdelta
        if new_row <= 0:
            raise TranslatorError('Formula out of range')
        return str(new_row)

    @staticmethod
    def translate_col--- This code section failed: ---

 L.  78         0  LOAD_FAST                'col_str'
                2  LOAD_METHOD              startswith
                4  LOAD_STR                 '$'
                6  CALL_METHOD_1         1  ''
                8  POP_JUMP_IF_FALSE    14  'to 14'

 L.  79        10  LOAD_FAST                'col_str'
               12  RETURN_VALUE     
             14_0  COME_FROM             8  '8'

 L.  81        14  SETUP_FINALLY        34  'to 34'

 L.  82        16  LOAD_GLOBAL              get_column_letter

 L.  83        18  LOAD_GLOBAL              column_index_from_string
               20  LOAD_FAST                'col_str'
               22  CALL_FUNCTION_1       1  ''
               24  LOAD_FAST                'cdelta'
               26  BINARY_ADD       

 L.  82        28  CALL_FUNCTION_1       1  ''
               30  POP_BLOCK        
               32  RETURN_VALUE     
             34_0  COME_FROM_FINALLY    14  '14'

 L.  84        34  DUP_TOP          
               36  LOAD_GLOBAL              ValueError
               38  COMPARE_OP               exception-match
               40  POP_JUMP_IF_FALSE    60  'to 60'
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L.  85        48  LOAD_GLOBAL              TranslatorError
               50  LOAD_STR                 'Formula out of range'
               52  CALL_FUNCTION_1       1  ''
               54  RAISE_VARARGS_1       1  'exception instance'
               56  POP_EXCEPT       
               58  JUMP_FORWARD         62  'to 62'
             60_0  COME_FROM            40  '40'
               60  END_FINALLY      
             62_0  COME_FROM            58  '58'

Parse error at or near `POP_TOP' instruction at offset 44

    @staticmethod
    def strip_ws_name(range_str):
        """Splits out the worksheet reference, if any, from a range reference."""
        if '!' in range_str:
            sheet, range_str = range_str.rsplit('!', 1)
            return (sheet + '!', range_str)
        return (
         '', range_str)

    @classmethod
    def translate_range(cls, range_str, rdelta, cdelta):
        """
        Translate an A1-style range reference to the destination cell.

        `rdelta`: the row offset to add to the range
        `cdelta`: the column offset to add to the range
        `range_str`: an A1-style reference to a range. Potentially includes
                     the worksheet reference. Could also be a named range.

        """
        ws_part, range_str = cls.strip_ws_name(range_str)
        match = cls.ROW_RANGE_RE.match(range_str)
        if match is not None:
            return ws_part + cls.translate_row(match.group(1), rdelta) + ':' + cls.translate_row(match.group(2), rdelta)
        match = cls.COL_RANGE_RE.match(range_str)
        if match is not None:
            return ws_part + cls.translate_col(match.group(1), cdelta) + ':' + cls.translate_col(match.group(2), cdelta)
        if ':' in range_str:
            return ws_part + ':'.join((cls.translate_range(piece, rdelta, cdelta) for piece in range_str.split(':')))
        match = cls.CELL_REF_RE.match(range_str)
        if match is None:
            return range_str
        return ws_part + cls.translate_col(match.group(1), cdelta) + cls.translate_row(match.group(2), rdelta)

    def translate_formula(self, dest=None, row_delta=0, col_delta=0):
        """
        Convert the formula into A1 notation, or as row and column coordinates

        The formula is converted into A1 assuming it is assigned to the cell
        whose address is `dest` (no worksheet name).

        """
        tokens = self.get_tokens()
        if not tokens:
            return ''
        if tokens[0].type == Token.LITERAL:
            return tokens[0].value
        out = [
         '=']
        if dest:
            row, col = coordinate_to_tuple(dest)
            row_delta = row - self.row
            col_delta = col - self.col
        for token in tokens:
            if token.type == Token.OPERAND and token.subtype == Token.RANGE:
                out.append(self.translate_range(token.value, row_delta, col_delta))
            else:
                out.append(token.value)
        else:
            return ''.join(out)