# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\openpyxl\reader\excel.py
"""Read an xlsx file into Python"""
from zipfile import ZipFile, ZIP_DEFLATED, BadZipfile
from sys import exc_info
from io import BytesIO
import os.path, warnings
from openpyxl.pivot.table import TableDefinition
try:
    from ..tests import KEEP_VBA
except ImportError:
    KEEP_VBA = False
else:
    from openpyxl.utils.exceptions import InvalidFileException
    from openpyxl.xml.constants import ARC_SHARED_STRINGS, ARC_CORE, ARC_CONTENT_TYPES, ARC_WORKBOOK, ARC_THEME, COMMENTS_NS, SHARED_STRINGS, EXTERNAL_LINK, XLTM, XLTX, XLSM, XLSX
    from openpyxl.cell import MergedCell
    from openpyxl.comments.comment_sheet import CommentSheet
    from .strings import read_string_table
    from .workbook import WorkbookParser
    from openpyxl.styles.stylesheet import apply_stylesheet
    from openpyxl.packaging.core import DocumentProperties
    from openpyxl.packaging.manifest import Manifest, Override
    from openpyxl.packaging.relationship import RelationshipList, get_dependents, get_rels_path
    from openpyxl.worksheet._read_only import ReadOnlyWorksheet
    from openpyxl.worksheet._reader import WorksheetReader
    from openpyxl.chartsheet import Chartsheet
    from openpyxl.worksheet.table import Table
    from openpyxl.drawing.spreadsheet_drawing import SpreadsheetDrawing
    from openpyxl.xml.functions import fromstring
    from .drawings import find_images
    SUPPORTED_FORMATS = ('.xlsx', '.xlsm', '.xltx', '.xltm')

    def _validate_archive(filename):
        """
    Does a first check whether filename is a string or a file-like
    object. If it is a string representing a filename, a check is done
    for supported formats by checking the given file-extension. If the
    file-extension is not in SUPPORTED_FORMATS an InvalidFileException
    will raised. Otherwise the filename (resp. file-like object) will
    forwarded to zipfile.ZipFile returning a ZipFile-Instance.
    """
        is_file_like = hasattr(filename, 'read')
        if not is_file_like:
            file_format = os.path.splitext(filename)[(-1)].lower()
            if file_format not in SUPPORTED_FORMATS:
                if file_format == '.xls':
                    msg = 'openpyxl does not support the old .xls file format, please use xlrd to read this file, or convert it to the more recent .xlsx file format.'
                else:
                    if file_format == '.xlsb':
                        msg = 'openpyxl does not support binary format .xlsb, please convert this file to .xlsx format if you want to open it with openpyxl'
                    else:
                        msg = 'openpyxl does not support %s file format, please check you can open it with Excel first. Supported formats are: %s' % (
                         file_format,
                         ','.join(SUPPORTED_FORMATS))
                raise InvalidFileException(msg)
        archive = ZipFile(filename, 'r')
        return archive


    def _find_workbook_part(package):
        workbook_types = [
         XLTM, XLTX, XLSM, XLSX]
        for ct in workbook_types:
            part = package.find(ct)
            if part:
                return part
        else:
            defaults = {p.ContentType for p in package.Default}
            workbook_type = defaults & set(workbook_types)
            if workbook_type:
                return Override('/' + ARC_WORKBOOK, workbook_type.pop())
            raise IOError('File contains no valid workbook part')


    class ExcelReader:
        __doc__ = '\n    Read an Excel package and dispatch the contents to the relevant modules\n    '

        def __init__(self, fn, read_only=False, keep_vba=KEEP_VBA, data_only=False, keep_links=True):
            self.archive = _validate_archive(fn)
            self.valid_files = self.archive.namelist()
            self.read_only = read_only
            self.keep_vba = keep_vba
            self.data_only = data_only
            self.keep_links = keep_links
            self.shared_strings = []

        def read_manifest(self):
            src = self.archive.read(ARC_CONTENT_TYPES)
            root = fromstring(src)
            self.package = Manifest.from_tree(root)

        def read_strings(self):
            ct = self.package.find(SHARED_STRINGS)
            if ct is not None:
                strings_path = ct.PartName[1:]
                with self.archive.open(strings_path) as (src):
                    self.shared_strings = read_string_table(src)

        def read_workbook(self):
            wb_part = _find_workbook_part(self.package)
            self.parser = WorkbookParser((self.archive), (wb_part.PartName[1:]), keep_links=(self.keep_links))
            self.parser.parse()
            wb = self.parser.wb
            wb._sheets = []
            wb._data_only = self.data_only
            wb._read_only = self.read_only
            wb.template = wb_part.ContentType in (XLTX, XLTM)
            if self.keep_vba:
                wb.vba_archive = ZipFile(BytesIO(), 'a', ZIP_DEFLATED)
                for name in self.valid_files:
                    wb.vba_archive.writestr(name, self.archive.read(name))

            if self.read_only:
                wb._archive = self.archive
            self.wb = wb

        def read_properties(self):
            if ARC_CORE in self.valid_files:
                src = fromstring(self.archive.read(ARC_CORE))
                self.wb.properties = DocumentProperties.from_tree(src)

        def read_theme(self):
            if ARC_THEME in self.valid_files:
                self.wb.loaded_theme = self.archive.read(ARC_THEME)

        def read_chartsheet(self, sheet, rel):
            sheet_path = rel.target
            rels_path = get_rels_path(sheet_path)
            rels = []
            if rels_path in self.valid_files:
                rels = get_dependents(self.archive, rels_path)
            with self.archive.open(sheet_path, 'r') as (src):
                xml = src.read()
            node = fromstring(xml)
            cs = Chartsheet.from_tree(node)
            cs._parent = self.wb
            cs.title = sheet.name
            self.wb._add_sheet(cs)
            drawings = rels.find(SpreadsheetDrawing._rel_type)
            for rel in drawings:
                charts, images = find_images(self.archive, rel.target)
                for c in charts:
                    cs.add_chart(c)

        def read_worksheets--- This code section failed: ---

 L. 204         0  LOAD_STR                 "Cell '{0}':{1} is part of a merged range but has a comment which will be removed because merged cells cannot contain any data."
                2  STORE_FAST               'comment_warning'

 L. 205         4  LOAD_FAST                'self'
                6  LOAD_ATTR                parser
                8  LOAD_METHOD              find_sheets
               10  CALL_METHOD_0         0  ''
               12  GET_ITER         
            14_16  FOR_ITER            638  'to 638'
               18  UNPACK_SEQUENCE_2     2 
               20  STORE_FAST               'sheet'
               22  STORE_FAST               'rel'

 L. 206        24  LOAD_FAST                'rel'
               26  LOAD_ATTR                target
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                valid_files
               32  COMPARE_OP               not-in
               34  POP_JUMP_IF_FALSE    38  'to 38'

 L. 207        36  JUMP_BACK            14  'to 14'
             38_0  COME_FROM            34  '34'

 L. 209        38  LOAD_STR                 'chartsheet'
               40  LOAD_FAST                'rel'
               42  LOAD_ATTR                Type
               44  COMPARE_OP               in
               46  POP_JUMP_IF_FALSE    62  'to 62'

 L. 210        48  LOAD_FAST                'self'
               50  LOAD_METHOD              read_chartsheet
               52  LOAD_FAST                'sheet'
               54  LOAD_FAST                'rel'
               56  CALL_METHOD_2         2  ''
               58  POP_TOP          

 L. 211        60  JUMP_BACK            14  'to 14'
             62_0  COME_FROM            46  '46'

 L. 213        62  LOAD_GLOBAL              get_rels_path
               64  LOAD_FAST                'rel'
               66  LOAD_ATTR                target
               68  CALL_FUNCTION_1       1  ''
               70  STORE_FAST               'rels_path'

 L. 214        72  LOAD_GLOBAL              RelationshipList
               74  CALL_FUNCTION_0       0  ''
               76  STORE_FAST               'rels'

 L. 215        78  LOAD_FAST                'rels_path'
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                valid_files
               84  COMPARE_OP               in
               86  POP_JUMP_IF_FALSE   100  'to 100'

 L. 216        88  LOAD_GLOBAL              get_dependents
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                archive
               94  LOAD_FAST                'rels_path'
               96  CALL_FUNCTION_2       2  ''
               98  STORE_FAST               'rels'
            100_0  COME_FROM            86  '86'

 L. 218       100  LOAD_FAST                'self'
              102  LOAD_ATTR                read_only
              104  POP_JUMP_IF_FALSE   154  'to 154'

 L. 219       106  LOAD_GLOBAL              ReadOnlyWorksheet
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                wb
              112  LOAD_FAST                'sheet'
              114  LOAD_ATTR                name
              116  LOAD_FAST                'rel'
              118  LOAD_ATTR                target
              120  LOAD_FAST                'self'
              122  LOAD_ATTR                shared_strings
              124  CALL_FUNCTION_4       4  ''
              126  STORE_FAST               'ws'

 L. 220       128  LOAD_FAST                'sheet'
              130  LOAD_ATTR                state
              132  LOAD_FAST                'ws'
              134  STORE_ATTR               sheet_state

 L. 221       136  LOAD_FAST                'self'
              138  LOAD_ATTR                wb
              140  LOAD_ATTR                _sheets
              142  LOAD_METHOD              append
              144  LOAD_FAST                'ws'
              146  CALL_METHOD_1         1  ''
              148  POP_TOP          

 L. 222       150  JUMP_BACK            14  'to 14'
              152  JUMP_FORWARD        214  'to 214'
            154_0  COME_FROM           104  '104'

 L. 224       154  LOAD_FAST                'self'
              156  LOAD_ATTR                archive
              158  LOAD_METHOD              open
              160  LOAD_FAST                'rel'
              162  LOAD_ATTR                target
              164  CALL_METHOD_1         1  ''
              166  STORE_FAST               'fh'

 L. 225       168  LOAD_FAST                'self'
              170  LOAD_ATTR                wb
              172  LOAD_METHOD              create_sheet
              174  LOAD_FAST                'sheet'
              176  LOAD_ATTR                name
              178  CALL_METHOD_1         1  ''
              180  STORE_FAST               'ws'

 L. 226       182  LOAD_FAST                'rels'
              184  LOAD_FAST                'ws'
              186  STORE_ATTR               _rels

 L. 227       188  LOAD_GLOBAL              WorksheetReader
              190  LOAD_FAST                'ws'
              192  LOAD_FAST                'fh'
              194  LOAD_FAST                'self'
              196  LOAD_ATTR                shared_strings
              198  LOAD_FAST                'self'
              200  LOAD_ATTR                data_only
              202  CALL_FUNCTION_4       4  ''
              204  STORE_FAST               'ws_parser'

 L. 228       206  LOAD_FAST                'ws_parser'
              208  LOAD_METHOD              bind_all
              210  CALL_METHOD_0         0  ''
              212  POP_TOP          
            214_0  COME_FROM           152  '152'

 L. 231       214  LOAD_FAST                'rels'
              216  LOAD_METHOD              find
              218  LOAD_GLOBAL              COMMENTS_NS
              220  CALL_METHOD_1         1  ''
              222  GET_ITER         
              224  FOR_ITER            362  'to 362'
              226  STORE_FAST               'r'

 L. 232       228  LOAD_FAST                'self'
              230  LOAD_ATTR                archive
              232  LOAD_METHOD              read
              234  LOAD_FAST                'r'
              236  LOAD_ATTR                target
              238  CALL_METHOD_1         1  ''
              240  STORE_FAST               'src'

 L. 233       242  LOAD_GLOBAL              CommentSheet
              244  LOAD_METHOD              from_tree
              246  LOAD_GLOBAL              fromstring
              248  LOAD_FAST                'src'
              250  CALL_FUNCTION_1       1  ''
              252  CALL_METHOD_1         1  ''
              254  STORE_FAST               'comment_sheet'

 L. 234       256  LOAD_FAST                'comment_sheet'
              258  LOAD_ATTR                comments
              260  GET_ITER         
              262  FOR_ITER            360  'to 360'
              264  UNPACK_SEQUENCE_2     2 
              266  STORE_FAST               'ref'
              268  STORE_FAST               'comment'

 L. 235       270  SETUP_FINALLY       286  'to 286'

 L. 236       272  LOAD_FAST                'comment'
              274  LOAD_FAST                'ws'
              276  LOAD_FAST                'ref'
              278  BINARY_SUBSCR    
              280  STORE_ATTR               comment
              282  POP_BLOCK        
              284  JUMP_BACK           262  'to 262'
            286_0  COME_FROM_FINALLY   270  '270'

 L. 237       286  DUP_TOP          
              288  LOAD_GLOBAL              AttributeError
              290  COMPARE_OP               exception-match
          292_294  POP_JUMP_IF_FALSE   354  'to 354'
              296  POP_TOP          
              298  POP_TOP          
              300  POP_TOP          

 L. 238       302  LOAD_FAST                'ws'
              304  LOAD_FAST                'ref'
              306  BINARY_SUBSCR    
              308  STORE_FAST               'c'

 L. 239       310  LOAD_GLOBAL              isinstance
              312  LOAD_FAST                'c'
              314  LOAD_GLOBAL              MergedCell
              316  CALL_FUNCTION_2       2  ''
          318_320  POP_JUMP_IF_FALSE   350  'to 350'

 L. 240       322  LOAD_GLOBAL              warnings
              324  LOAD_METHOD              warn
              326  LOAD_FAST                'comment_warning'
              328  LOAD_METHOD              format
              330  LOAD_FAST                'ws'
              332  LOAD_ATTR                title
              334  LOAD_FAST                'c'
              336  LOAD_ATTR                coordinate
              338  CALL_METHOD_2         2  ''
              340  CALL_METHOD_1         1  ''
              342  POP_TOP          

 L. 241       344  POP_EXCEPT       
          346_348  JUMP_BACK           262  'to 262'
            350_0  COME_FROM           318  '318'
              350  POP_EXCEPT       
              352  JUMP_BACK           262  'to 262'
            354_0  COME_FROM           292  '292'
              354  END_FINALLY      
          356_358  JUMP_BACK           262  'to 262'
              360  JUMP_BACK           224  'to 224'

 L. 244       362  LOAD_FAST                'self'
              364  LOAD_ATTR                wb
              366  LOAD_ATTR                vba_archive
          368_370  POP_JUMP_IF_FALSE   394  'to 394'
              372  LOAD_FAST                'ws'
              374  LOAD_ATTR                legacy_drawing
          376_378  POP_JUMP_IF_FALSE   394  'to 394'

 L. 245       380  LOAD_FAST                'rels'
              382  LOAD_FAST                'ws'
              384  LOAD_ATTR                legacy_drawing
              386  BINARY_SUBSCR    
              388  LOAD_ATTR                target
              390  LOAD_FAST                'ws'
              392  STORE_ATTR               legacy_drawing
            394_0  COME_FROM           376  '376'
            394_1  COME_FROM           368  '368'

 L. 247       394  LOAD_FAST                'ws_parser'
              396  LOAD_ATTR                tables
              398  GET_ITER         
              400  FOR_ITER            448  'to 448'
              402  STORE_FAST               't'

 L. 248       404  LOAD_FAST                'self'
              406  LOAD_ATTR                archive
              408  LOAD_METHOD              read
              410  LOAD_FAST                't'
              412  CALL_METHOD_1         1  ''
              414  STORE_FAST               'src'

 L. 249       416  LOAD_GLOBAL              fromstring
              418  LOAD_FAST                'src'
              420  CALL_FUNCTION_1       1  ''
              422  STORE_FAST               'xml'

 L. 250       424  LOAD_GLOBAL              Table
              426  LOAD_METHOD              from_tree
              428  LOAD_FAST                'xml'
              430  CALL_METHOD_1         1  ''
              432  STORE_FAST               'table'

 L. 251       434  LOAD_FAST                'ws'
              436  LOAD_METHOD              add_table
              438  LOAD_FAST                'table'
              440  CALL_METHOD_1         1  ''
              442  POP_TOP          
          444_446  JUMP_BACK           400  'to 400'

 L. 253       448  LOAD_FAST                'rels'
              450  LOAD_METHOD              find
              452  LOAD_GLOBAL              SpreadsheetDrawing
              454  LOAD_ATTR                _rel_type
              456  CALL_METHOD_1         1  ''
              458  STORE_FAST               'drawings'

 L. 254       460  LOAD_FAST                'drawings'
              462  GET_ITER         
              464  FOR_ITER            542  'to 542'
              466  STORE_FAST               'rel'

 L. 255       468  LOAD_GLOBAL              find_images
              470  LOAD_FAST                'self'
              472  LOAD_ATTR                archive
              474  LOAD_FAST                'rel'
              476  LOAD_ATTR                target
              478  CALL_FUNCTION_2       2  ''
              480  UNPACK_SEQUENCE_2     2 
              482  STORE_FAST               'charts'
              484  STORE_FAST               'images'

 L. 256       486  LOAD_FAST                'charts'
              488  GET_ITER         
              490  FOR_ITER            512  'to 512'
              492  STORE_FAST               'c'

 L. 257       494  LOAD_FAST                'ws'
              496  LOAD_METHOD              add_chart
              498  LOAD_FAST                'c'
              500  LOAD_FAST                'c'
              502  LOAD_ATTR                anchor
              504  CALL_METHOD_2         2  ''
              506  POP_TOP          
          508_510  JUMP_BACK           490  'to 490'

 L. 258       512  LOAD_FAST                'images'
              514  GET_ITER         
              516  FOR_ITER            538  'to 538'
              518  STORE_FAST               'im'

 L. 259       520  LOAD_FAST                'ws'
              522  LOAD_METHOD              add_image
              524  LOAD_FAST                'im'
              526  LOAD_FAST                'im'
              528  LOAD_ATTR                anchor
              530  CALL_METHOD_2         2  ''
              532  POP_TOP          
          534_536  JUMP_BACK           516  'to 516'
          538_540  JUMP_BACK           464  'to 464'

 L. 261       542  LOAD_FAST                'rels'
              544  LOAD_METHOD              find
              546  LOAD_GLOBAL              TableDefinition
              548  LOAD_ATTR                rel_type
              550  CALL_METHOD_1         1  ''
              552  STORE_FAST               'pivot_rel'

 L. 262       554  LOAD_FAST                'pivot_rel'
              556  GET_ITER         
              558  FOR_ITER            628  'to 628'
              560  STORE_FAST               'r'

 L. 263       562  LOAD_FAST                'r'
              564  LOAD_ATTR                Target
              566  STORE_FAST               'pivot_path'

 L. 264       568  LOAD_FAST                'self'
              570  LOAD_ATTR                archive
              572  LOAD_METHOD              read
              574  LOAD_FAST                'pivot_path'
              576  CALL_METHOD_1         1  ''
              578  STORE_FAST               'src'

 L. 265       580  LOAD_GLOBAL              fromstring
              582  LOAD_FAST                'src'
              584  CALL_FUNCTION_1       1  ''
              586  STORE_FAST               'tree'

 L. 266       588  LOAD_GLOBAL              TableDefinition
              590  LOAD_METHOD              from_tree
              592  LOAD_FAST                'tree'
              594  CALL_METHOD_1         1  ''
              596  STORE_FAST               'pivot'

 L. 267       598  LOAD_FAST                'self'
              600  LOAD_ATTR                parser
              602  LOAD_ATTR                pivot_caches
              604  LOAD_FAST                'pivot'
              606  LOAD_ATTR                cacheId
              608  BINARY_SUBSCR    
              610  LOAD_FAST                'pivot'
              612  STORE_ATTR               cache

 L. 268       614  LOAD_FAST                'ws'
              616  LOAD_METHOD              add_pivot
              618  LOAD_FAST                'pivot'
              620  CALL_METHOD_1         1  ''
              622  POP_TOP          
          624_626  JUMP_BACK           558  'to 558'

 L. 270       628  LOAD_FAST                'sheet'
              630  LOAD_ATTR                state
              632  LOAD_FAST                'ws'
              634  STORE_ATTR               sheet_state
              636  JUMP_BACK            14  'to 14'

Parse error at or near `JUMP_FORWARD' instruction at offset 152

        def read(self):
            self.read_manifest()
            self.read_strings()
            self.read_workbook()
            self.read_properties()
            self.read_theme()
            apply_stylesheet(self.archive, self.wb)
            self.read_worksheets()
            self.parser.assign_names()
            if not self.read_only:
                self.archive.close()


    def load_workbook(filename, read_only=False, keep_vba=KEEP_VBA, data_only=False, keep_links=True):
        """Open the given filename and return the workbook

    :param filename: the path to open or a file-like object
    :type filename: string or a file-like object open in binary mode c.f., :class:`zipfile.ZipFile`

    :param read_only: optimised for reading, content cannot be edited
    :type read_only: bool

    :param keep_vba: preseve vba content (this does NOT mean you can use it)
    :type keep_vba: bool

    :param data_only: controls whether cells with formulae have either the formula (default) or the value stored the last time Excel read the sheet
    :type data_only: bool

    :param keep_links: whether links to external workbooks should be preserved. The default is True
    :type keep_links: bool

    :rtype: :class:`openpyxl.workbook.Workbook`

    .. note::

        When using lazy load, all worksheets will be :class:`openpyxl.worksheet.iter_worksheet.IterableWorksheet`
        and the returned workbook will be read-only.

    """
        reader = ExcelReader(filename, read_only, keep_vba, data_only, keep_links)
        reader.read()
        return reader.wb