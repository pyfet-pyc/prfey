# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: csv.py
"""
csv.py - read/write/investigate CSV files
"""
import re
from _csv import Error, __version__, writer, reader, register_dialect, unregister_dialect, get_dialect, list_dialects, field_size_limit, QUOTE_MINIMAL, QUOTE_ALL, QUOTE_NONNUMERIC, QUOTE_NONE, __doc__
from _csv import Dialect as _Dialect
from io import StringIO
__all__ = [
 'QUOTE_MINIMAL', 'QUOTE_ALL', 'QUOTE_NONNUMERIC', 'QUOTE_NONE',
 'Error', 'Dialect', '__doc__', 'excel', 'excel_tab',
 'field_size_limit', 'reader', 'writer',
 'register_dialect', 'get_dialect', 'list_dialects', 'Sniffer',
 'unregister_dialect', '__version__', 'DictReader', 'DictWriter',
 'unix_dialect']

class Dialect:
    __doc__ = 'Describe a CSV dialect.\n\n    This must be subclassed (see csv.excel).  Valid attributes are:\n    delimiter, quotechar, escapechar, doublequote, skipinitialspace,\n    lineterminator, quoting.\n\n    '
    _name = ''
    _valid = False
    delimiter = None
    quotechar = None
    escapechar = None
    doublequote = None
    skipinitialspace = None
    lineterminator = None
    quoting = None

    def __init__(self):
        if self.__class__ != Dialect:
            self._valid = True
        self._validate()

    def _validate(self):
        try:
            _Dialect(self)
        except TypeError as e:
            try:
                raise Error(str(e))
            finally:
                e = None
                del e


class excel(Dialect):
    __doc__ = 'Describe the usual properties of Excel-generated CSV files.'
    delimiter = ','
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = QUOTE_MINIMAL


register_dialect('excel', excel)

class excel_tab(excel):
    __doc__ = 'Describe the usual properties of Excel-generated TAB-delimited files.'
    delimiter = '\t'


register_dialect('excel-tab', excel_tab)

class unix_dialect(Dialect):
    __doc__ = 'Describe the usual properties of Unix-generated CSV files.'
    delimiter = ','
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\n'
    quoting = QUOTE_ALL


register_dialect('unix', unix_dialect)

class DictReader:

    def __init__(self, f, fieldnames=None, restkey=None, restval=None, dialect='excel', *args, **kwds):
        self._fieldnames = fieldnames
        self.restkey = restkey
        self.restval = restval
        self.reader = reader(f, dialect, *args, **kwds)
        self.dialect = dialect
        self.line_num = 0

    def __iter__(self):
        return self

    @property
    def fieldnames(self):
        if self._fieldnames is None:
            try:
                self._fieldnames = next(self.reader)
            except StopIteration:
                pass
            else:
                self.line_num = self.reader.line_num
            return self._fieldnames

    @fieldnames.setter
    def fieldnames(self, value):
        self._fieldnames = value

    def __next__(self):
        if self.line_num == 0:
            self.fieldnames
        row = next(self.reader)
        self.line_num = self.reader.line_num
        while True:
            if row == []:
                row = next(self.reader)

        d = dict(zip(self.fieldnames, row))
        lf = len(self.fieldnames)
        lr = len(row)
        if lf < lr:
            d[self.restkey] = row[lf:]
        else:
            pass
        if lf > lr:
            for key in self.fieldnames[lr:]:
                d[key] = self.restval

            return d


class DictWriter:

    def __init__(self, f, fieldnames, restval='', extrasaction='raise', dialect='excel', *args, **kwds):
        self.fieldnames = fieldnames
        self.restval = restval
        if extrasaction.lower() not in ('raise', 'ignore'):
            raise ValueError("extrasaction (%s) must be 'raise' or 'ignore'" % extrasaction)
        self.extrasaction = extrasaction
        self.writer = writer(f, dialect, *args, **kwds)

    def writeheader(self):
        header = dict(zip(self.fieldnames, self.fieldnames))
        return self.writerow(header)

    def _dict_to_list(self, rowdict):
        if self.extrasaction == 'raise':
            wrong_fields = rowdict.keys() - self.fieldnames
            if wrong_fields:
                raise ValueError('dict contains fields not in fieldnames: ' + ', '.join([repr(x) for x in wrong_fields]))
        return (rowdict.get(key, self.restval) for key in self.fieldnames)

    def writerow(self, rowdict):
        return self.writer.writerow(self._dict_to_list(rowdict))

    def writerows(self, rowdicts):
        return self.writer.writerows(map(self._dict_to_list, rowdicts))


try:
    complex
except NameError:
    complex = float
else:

    class Sniffer:
        __doc__ = '\n    "Sniffs" the format of a CSV file (i.e. delimiter, quotechar)\n    Returns a Dialect object.\n    '

        def __init__(self):
            self.preferred = [
             ',', '\t', ';', ' ', ':']

        def sniff(self, sample, delimiters=None):
            """
        Returns a dialect (or None) corresponding to the sample
        """
            quotechar, doublequote, delimiter, skipinitialspace = self._guess_quote_and_delimiter(sample, delimiters)
            if not delimiter:
                delimiter, skipinitialspace = self._guess_delimiter(sample, delimiters)
            if not delimiter:
                raise Error('Could not determine delimiter')

            class dialect(Dialect):
                _name = 'sniffed'
                lineterminator = '\r\n'
                quoting = QUOTE_MINIMAL

            dialect.doublequote = doublequote
            dialect.delimiter = delimiter
            dialect.quotechar = quotechar or '"'
            dialect.skipinitialspace = skipinitialspace
            return dialect

        def _guess_quote_and_delimiter--- This code section failed: ---

 L. 216         0  BUILD_LIST_0          0 
                2  STORE_FAST               'matches'

 L. 217         4  LOAD_CONST               ('(?P<delim>[^\\w\\n"\\\'])(?P<space> ?)(?P<quote>["\\\']).*?(?P=quote)(?P=delim)', '(?:^|\\n)(?P<quote>["\\\']).*?(?P=quote)(?P<delim>[^\\w\\n"\\\'])(?P<space> ?)', '(?P<delim>[^\\w\\n"\\\'])(?P<space> ?)(?P<quote>["\\\']).*?(?P=quote)(?:$|\\n)', '(?:^|\\n)(?P<quote>["\\\']).*?(?P=quote)(?:$|\\n)')
                6  GET_ITER         
              8_0  COME_FROM            50  '50'
              8_1  COME_FROM            44  '44'
                8  FOR_ITER             52  'to 52'
               10  STORE_FAST               'restr'

 L. 221        12  LOAD_GLOBAL              re
               14  LOAD_METHOD              compile
               16  LOAD_FAST                'restr'
               18  LOAD_GLOBAL              re
               20  LOAD_ATTR                DOTALL
               22  LOAD_GLOBAL              re
               24  LOAD_ATTR                MULTILINE
               26  BINARY_OR        
               28  CALL_METHOD_2         2  ''
               30  STORE_FAST               'regexp'

 L. 222        32  LOAD_FAST                'regexp'
               34  LOAD_METHOD              findall
               36  LOAD_FAST                'data'
               38  CALL_METHOD_1         1  ''
               40  STORE_FAST               'matches'

 L. 223        42  LOAD_FAST                'matches'
               44  POP_JUMP_IF_FALSE_BACK     8  'to 8'

 L. 224        46  POP_TOP          
               48  BREAK_LOOP           52  'to 52'
               50  JUMP_BACK             8  'to 8'
             52_0  COME_FROM            48  '48'
             52_1  COME_FROM             8  '8'

 L. 226        52  LOAD_FAST                'matches'
               54  POP_JUMP_IF_TRUE     60  'to 60'

 L. 228        56  LOAD_CONST               ('', False, None, 0)
               58  RETURN_VALUE     
             60_0  COME_FROM            54  '54'

 L. 229        60  BUILD_MAP_0           0 
               62  STORE_FAST               'quotes'

 L. 230        64  BUILD_MAP_0           0 
               66  STORE_FAST               'delims'

 L. 231        68  LOAD_CONST               0
               70  STORE_FAST               'spaces'

 L. 232        72  LOAD_FAST                'regexp'
               74  LOAD_ATTR                groupindex
               76  STORE_FAST               'groupindex'

 L. 233        78  LOAD_FAST                'matches'
               80  GET_ITER         
             82_0  COME_FROM           280  '280'
             82_1  COME_FROM           270  '270'
             82_2  COME_FROM           256  '256'
             82_3  COME_FROM           172  '172'
               82  FOR_ITER            282  'to 282'
               84  STORE_FAST               'm'

 L. 234        86  LOAD_FAST                'groupindex'
               88  LOAD_STR                 'quote'
               90  BINARY_SUBSCR    
               92  LOAD_CONST               1
               94  BINARY_SUBTRACT  
               96  STORE_FAST               'n'

 L. 235        98  LOAD_FAST                'm'
              100  LOAD_FAST                'n'
              102  BINARY_SUBSCR    
              104  STORE_FAST               'key'

 L. 236       106  LOAD_FAST                'key'
              108  POP_JUMP_IF_FALSE   130  'to 130'

 L. 237       110  LOAD_FAST                'quotes'
              112  LOAD_METHOD              get
              114  LOAD_FAST                'key'
              116  LOAD_CONST               0
              118  CALL_METHOD_2         2  ''
              120  LOAD_CONST               1
              122  BINARY_ADD       
              124  LOAD_FAST                'quotes'
              126  LOAD_FAST                'key'
              128  STORE_SUBSCR     
            130_0  COME_FROM           108  '108'

 L. 238       130  SETUP_FINALLY       156  'to 156'

 L. 239       132  LOAD_FAST                'groupindex'
              134  LOAD_STR                 'delim'
              136  BINARY_SUBSCR    
              138  LOAD_CONST               1
              140  BINARY_SUBTRACT  
              142  STORE_FAST               'n'

 L. 240       144  LOAD_FAST                'm'
              146  LOAD_FAST                'n'
              148  BINARY_SUBSCR    
              150  STORE_FAST               'key'
              152  POP_BLOCK        
              154  JUMP_FORWARD        180  'to 180'
            156_0  COME_FROM_FINALLY   130  '130'

 L. 241       156  DUP_TOP          
              158  LOAD_GLOBAL              KeyError
              160  COMPARE_OP               exception-match
              162  POP_JUMP_IF_FALSE   178  'to 178'
              164  POP_TOP          
              166  POP_TOP          
              168  POP_TOP          

 L. 242       170  POP_EXCEPT       
              172  JUMP_BACK            82  'to 82'
              174  POP_EXCEPT       
              176  JUMP_FORWARD        180  'to 180'
            178_0  COME_FROM           162  '162'
              178  END_FINALLY      
            180_0  COME_FROM           176  '176'
            180_1  COME_FROM           154  '154'

 L. 243       180  LOAD_FAST                'key'
              182  POP_JUMP_IF_FALSE   220  'to 220'
              184  LOAD_FAST                'delimiters'
              186  LOAD_CONST               None
              188  COMPARE_OP               is
              190  POP_JUMP_IF_TRUE    200  'to 200'
              192  LOAD_FAST                'key'
              194  LOAD_FAST                'delimiters'
              196  COMPARE_OP               in
              198  POP_JUMP_IF_FALSE   220  'to 220'
            200_0  COME_FROM           190  '190'

 L. 244       200  LOAD_FAST                'delims'
              202  LOAD_METHOD              get
              204  LOAD_FAST                'key'
              206  LOAD_CONST               0
              208  CALL_METHOD_2         2  ''
              210  LOAD_CONST               1
              212  BINARY_ADD       
              214  LOAD_FAST                'delims'
              216  LOAD_FAST                'key'
              218  STORE_SUBSCR     
            220_0  COME_FROM           198  '198'
            220_1  COME_FROM           182  '182'

 L. 245       220  SETUP_FINALLY       238  'to 238'

 L. 246       222  LOAD_FAST                'groupindex'
              224  LOAD_STR                 'space'
              226  BINARY_SUBSCR    
              228  LOAD_CONST               1
              230  BINARY_SUBTRACT  
              232  STORE_FAST               'n'
              234  POP_BLOCK        
              236  JUMP_FORWARD        264  'to 264'
            238_0  COME_FROM_FINALLY   220  '220'

 L. 247       238  DUP_TOP          
              240  LOAD_GLOBAL              KeyError
              242  COMPARE_OP               exception-match
          244_246  POP_JUMP_IF_FALSE   262  'to 262'
              248  POP_TOP          
              250  POP_TOP          
              252  POP_TOP          

 L. 248       254  POP_EXCEPT       
              256  JUMP_BACK            82  'to 82'
              258  POP_EXCEPT       
              260  JUMP_FORWARD        264  'to 264'
            262_0  COME_FROM           244  '244'
              262  END_FINALLY      
            264_0  COME_FROM           260  '260'
            264_1  COME_FROM           236  '236'

 L. 249       264  LOAD_FAST                'm'
              266  LOAD_FAST                'n'
              268  BINARY_SUBSCR    
              270  POP_JUMP_IF_FALSE_BACK    82  'to 82'

 L. 250       272  LOAD_FAST                'spaces'
              274  LOAD_CONST               1
              276  INPLACE_ADD      
              278  STORE_FAST               'spaces'
              280  JUMP_BACK            82  'to 82'
            282_0  COME_FROM            82  '82'

 L. 252       282  LOAD_GLOBAL              max
              284  LOAD_FAST                'quotes'
              286  LOAD_FAST                'quotes'
              288  LOAD_ATTR                get
              290  LOAD_CONST               ('key',)
              292  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              294  STORE_FAST               'quotechar'

 L. 254       296  LOAD_FAST                'delims'
          298_300  POP_JUMP_IF_FALSE   344  'to 344'

 L. 255       302  LOAD_GLOBAL              max
              304  LOAD_FAST                'delims'
              306  LOAD_FAST                'delims'
              308  LOAD_ATTR                get
              310  LOAD_CONST               ('key',)
              312  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              314  STORE_FAST               'delim'

 L. 256       316  LOAD_FAST                'delims'
              318  LOAD_FAST                'delim'
              320  BINARY_SUBSCR    
              322  LOAD_FAST                'spaces'
              324  COMPARE_OP               ==
              326  STORE_FAST               'skipinitialspace'

 L. 257       328  LOAD_FAST                'delim'
              330  LOAD_STR                 '\n'
              332  COMPARE_OP               ==
          334_336  POP_JUMP_IF_FALSE   352  'to 352'

 L. 258       338  LOAD_STR                 ''
              340  STORE_FAST               'delim'
              342  JUMP_FORWARD        352  'to 352'
            344_0  COME_FROM           298  '298'

 L. 261       344  LOAD_STR                 ''
              346  STORE_FAST               'delim'

 L. 262       348  LOAD_CONST               0
              350  STORE_FAST               'skipinitialspace'
            352_0  COME_FROM           342  '342'
            352_1  COME_FROM           334  '334'

 L. 266       352  LOAD_GLOBAL              re
              354  LOAD_METHOD              compile

 L. 267       356  LOAD_STR                 '((%(delim)s)|^)\\W*%(quote)s[^%(delim)s\\n]*%(quote)s[^%(delim)s\\n]*%(quote)s\\W*((%(delim)s)|$)'

 L. 268       358  LOAD_GLOBAL              re
              360  LOAD_METHOD              escape
              362  LOAD_FAST                'delim'
              364  CALL_METHOD_1         1  ''
              366  LOAD_FAST                'quotechar'
              368  LOAD_CONST               ('delim', 'quote')
              370  BUILD_CONST_KEY_MAP_2     2 

 L. 267       372  BINARY_MODULO    

 L. 268       374  LOAD_GLOBAL              re
              376  LOAD_ATTR                MULTILINE

 L. 266       378  CALL_METHOD_2         2  ''
              380  STORE_FAST               'dq_regexp'

 L. 272       382  LOAD_FAST                'dq_regexp'
              384  LOAD_METHOD              search
              386  LOAD_FAST                'data'
              388  CALL_METHOD_1         1  ''
          390_392  POP_JUMP_IF_FALSE   400  'to 400'

 L. 273       394  LOAD_CONST               True
              396  STORE_FAST               'doublequote'
              398  JUMP_FORWARD        404  'to 404'
            400_0  COME_FROM           390  '390'

 L. 275       400  LOAD_CONST               False
              402  STORE_FAST               'doublequote'
            404_0  COME_FROM           398  '398'

 L. 277       404  LOAD_FAST                'quotechar'
              406  LOAD_FAST                'doublequote'
              408  LOAD_FAST                'delim'
              410  LOAD_FAST                'skipinitialspace'
              412  BUILD_TUPLE_4         4 
              414  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 178_0

        def _guess_delimiter--- This code section failed: ---

 L. 299         0  LOAD_GLOBAL              list
                2  LOAD_GLOBAL              filter
                4  LOAD_CONST               None
                6  LOAD_FAST                'data'
                8  LOAD_METHOD              split
               10  LOAD_STR                 '\n'
               12  CALL_METHOD_1         1  ''
               14  CALL_FUNCTION_2       2  ''
               16  CALL_FUNCTION_1       1  ''
               18  STORE_FAST               'data'

 L. 301        20  LOAD_LISTCOMP            '<code_object <listcomp>>'
               22  LOAD_STR                 'Sniffer._guess_delimiter.<locals>.<listcomp>'
               24  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               26  LOAD_GLOBAL              range
               28  LOAD_CONST               127
               30  CALL_FUNCTION_1       1  ''
               32  GET_ITER         
               34  CALL_FUNCTION_1       1  ''
               36  STORE_FAST               'ascii'

 L. 304        38  LOAD_GLOBAL              min
               40  LOAD_CONST               10
               42  LOAD_GLOBAL              len
               44  LOAD_FAST                'data'
               46  CALL_FUNCTION_1       1  ''
               48  CALL_FUNCTION_2       2  ''
               50  STORE_FAST               'chunkLength'

 L. 305        52  LOAD_CONST               0
               54  STORE_FAST               'iteration'

 L. 306        56  BUILD_MAP_0           0 
               58  STORE_FAST               'charFrequency'

 L. 307        60  BUILD_MAP_0           0 
               62  STORE_FAST               'modes'

 L. 308        64  BUILD_MAP_0           0 
               66  STORE_FAST               'delims'

 L. 309        68  LOAD_CONST               0
               70  LOAD_FAST                'chunkLength'
               72  ROT_TWO          
               74  STORE_FAST               'start'
               76  STORE_FAST               'end'
             78_0  COME_FROM           592  '592'

 L. 310        78  LOAD_FAST                'start'
               80  LOAD_GLOBAL              len
               82  LOAD_FAST                'data'
               84  CALL_FUNCTION_1       1  ''
               86  COMPARE_OP               <
            88_90  POP_JUMP_IF_FALSE   594  'to 594'

 L. 311        92  LOAD_FAST                'iteration'
               94  LOAD_CONST               1
               96  INPLACE_ADD      
               98  STORE_FAST               'iteration'

 L. 312       100  LOAD_FAST                'data'
              102  LOAD_FAST                'start'
              104  LOAD_FAST                'end'
              106  BUILD_SLICE_2         2 
              108  BINARY_SUBSCR    
              110  GET_ITER         
            112_0  COME_FROM           176  '176'
              112  FOR_ITER            178  'to 178'
              114  STORE_FAST               'line'

 L. 313       116  LOAD_FAST                'ascii'
              118  GET_ITER         
            120_0  COME_FROM           174  '174'
              120  FOR_ITER            176  'to 176'
              122  STORE_FAST               'char'

 L. 314       124  LOAD_FAST                'charFrequency'
              126  LOAD_METHOD              get
              128  LOAD_FAST                'char'
              130  BUILD_MAP_0           0 
              132  CALL_METHOD_2         2  ''
              134  STORE_FAST               'metaFrequency'

 L. 316       136  LOAD_FAST                'line'
              138  LOAD_METHOD              count
              140  LOAD_FAST                'char'
              142  CALL_METHOD_1         1  ''
              144  STORE_FAST               'freq'

 L. 318       146  LOAD_FAST                'metaFrequency'
              148  LOAD_METHOD              get
              150  LOAD_FAST                'freq'
              152  LOAD_CONST               0
              154  CALL_METHOD_2         2  ''
              156  LOAD_CONST               1
              158  BINARY_ADD       
              160  LOAD_FAST                'metaFrequency'
              162  LOAD_FAST                'freq'
              164  STORE_SUBSCR     

 L. 319       166  LOAD_FAST                'metaFrequency'
              168  LOAD_FAST                'charFrequency'
              170  LOAD_FAST                'char'
              172  STORE_SUBSCR     
              174  JUMP_BACK           120  'to 120'
            176_0  COME_FROM           120  '120'
              176  JUMP_BACK           112  'to 112'
            178_0  COME_FROM           112  '112'

 L. 321       178  LOAD_FAST                'charFrequency'
              180  LOAD_METHOD              keys
              182  CALL_METHOD_0         0  ''
              184  GET_ITER         
            186_0  COME_FROM           344  '344'
            186_1  COME_FROM           330  '330'
            186_2  COME_FROM           234  '234'
              186  FOR_ITER            346  'to 346'
              188  STORE_FAST               'char'

 L. 322       190  LOAD_GLOBAL              list
              192  LOAD_FAST                'charFrequency'
              194  LOAD_FAST                'char'
              196  BINARY_SUBSCR    
              198  LOAD_METHOD              items
              200  CALL_METHOD_0         0  ''
              202  CALL_FUNCTION_1       1  ''
              204  STORE_FAST               'items'

 L. 323       206  LOAD_GLOBAL              len
              208  LOAD_FAST                'items'
              210  CALL_FUNCTION_1       1  ''
              212  LOAD_CONST               1
              214  COMPARE_OP               ==
              216  POP_JUMP_IF_FALSE   236  'to 236'
              218  LOAD_FAST                'items'
              220  LOAD_CONST               0
              222  BINARY_SUBSCR    
              224  LOAD_CONST               0
              226  BINARY_SUBSCR    
              228  LOAD_CONST               0
              230  COMPARE_OP               ==
              232  POP_JUMP_IF_FALSE   236  'to 236'

 L. 324       234  JUMP_BACK           186  'to 186'
            236_0  COME_FROM           232  '232'
            236_1  COME_FROM           216  '216'

 L. 326       236  LOAD_GLOBAL              len
              238  LOAD_FAST                'items'
              240  CALL_FUNCTION_1       1  ''
              242  LOAD_CONST               1
              244  COMPARE_OP               >
          246_248  POP_JUMP_IF_FALSE   332  'to 332'

 L. 327       250  LOAD_GLOBAL              max
              252  LOAD_FAST                'items'
              254  LOAD_LAMBDA              '<code_object <lambda>>'
              256  LOAD_STR                 'Sniffer._guess_delimiter.<locals>.<lambda>'
              258  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              260  LOAD_CONST               ('key',)
              262  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              264  LOAD_FAST                'modes'
              266  LOAD_FAST                'char'
              268  STORE_SUBSCR     

 L. 330       270  LOAD_FAST                'items'
              272  LOAD_METHOD              remove
              274  LOAD_FAST                'modes'
              276  LOAD_FAST                'char'
              278  BINARY_SUBSCR    
              280  CALL_METHOD_1         1  ''
              282  POP_TOP          

 L. 331       284  LOAD_FAST                'modes'
              286  LOAD_FAST                'char'
              288  BINARY_SUBSCR    
              290  LOAD_CONST               0
              292  BINARY_SUBSCR    
              294  LOAD_FAST                'modes'
              296  LOAD_FAST                'char'
              298  BINARY_SUBSCR    
              300  LOAD_CONST               1
              302  BINARY_SUBSCR    

 L. 332       304  LOAD_GLOBAL              sum
              306  LOAD_GENEXPR             '<code_object <genexpr>>'
              308  LOAD_STR                 'Sniffer._guess_delimiter.<locals>.<genexpr>'
              310  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              312  LOAD_FAST                'items'
              314  GET_ITER         
              316  CALL_FUNCTION_1       1  ''
              318  CALL_FUNCTION_1       1  ''

 L. 331       320  BINARY_SUBTRACT  
              322  BUILD_TUPLE_2         2 
              324  LOAD_FAST                'modes'
              326  LOAD_FAST                'char'
              328  STORE_SUBSCR     
              330  JUMP_BACK           186  'to 186'
            332_0  COME_FROM           246  '246'

 L. 334       332  LOAD_FAST                'items'
              334  LOAD_CONST               0
              336  BINARY_SUBSCR    
              338  LOAD_FAST                'modes'
              340  LOAD_FAST                'char'
              342  STORE_SUBSCR     
              344  JUMP_BACK           186  'to 186'
            346_0  COME_FROM           186  '186'

 L. 337       346  LOAD_FAST                'modes'
              348  LOAD_METHOD              items
              350  CALL_METHOD_0         0  ''
              352  STORE_FAST               'modeList'

 L. 338       354  LOAD_GLOBAL              float
              356  LOAD_GLOBAL              min
              358  LOAD_FAST                'chunkLength'
              360  LOAD_FAST                'iteration'
              362  BINARY_MULTIPLY  
              364  LOAD_GLOBAL              len
              366  LOAD_FAST                'data'
              368  CALL_FUNCTION_1       1  ''
              370  CALL_FUNCTION_2       2  ''
              372  CALL_FUNCTION_1       1  ''
              374  STORE_FAST               'total'

 L. 340       376  LOAD_CONST               1.0
              378  STORE_FAST               'consistency'

 L. 342       380  LOAD_CONST               0.9
              382  STORE_FAST               'threshold'
            384_0  COME_FROM           506  '506'

 L. 343       384  LOAD_GLOBAL              len
              386  LOAD_FAST                'delims'
              388  CALL_FUNCTION_1       1  ''
              390  LOAD_CONST               0
              392  COMPARE_OP               ==
          394_396  POP_JUMP_IF_FALSE   510  'to 510'
              398  LOAD_FAST                'consistency'
              400  LOAD_FAST                'threshold'
              402  COMPARE_OP               >=
          404_406  POP_JUMP_IF_FALSE   510  'to 510'

 L. 344       408  LOAD_FAST                'modeList'
              410  GET_ITER         
            412_0  COME_FROM           494  '494'
            412_1  COME_FROM           482  '482'
            412_2  COME_FROM           462  '462'
            412_3  COME_FROM           444  '444'
            412_4  COME_FROM           430  '430'
              412  FOR_ITER            498  'to 498'
              414  UNPACK_SEQUENCE_2     2 
              416  STORE_FAST               'k'
              418  STORE_FAST               'v'

 L. 345       420  LOAD_FAST                'v'
              422  LOAD_CONST               0
              424  BINARY_SUBSCR    
              426  LOAD_CONST               0
              428  COMPARE_OP               >
          430_432  POP_JUMP_IF_FALSE_BACK   412  'to 412'
              434  LOAD_FAST                'v'
              436  LOAD_CONST               1
              438  BINARY_SUBSCR    
              440  LOAD_CONST               0
              442  COMPARE_OP               >
          444_446  POP_JUMP_IF_FALSE_BACK   412  'to 412'

 L. 346       448  LOAD_FAST                'v'
              450  LOAD_CONST               1
              452  BINARY_SUBSCR    
              454  LOAD_FAST                'total'
              456  BINARY_TRUE_DIVIDE
              458  LOAD_FAST                'consistency'
              460  COMPARE_OP               >=
          462_464  POP_JUMP_IF_FALSE_BACK   412  'to 412'

 L. 347       466  LOAD_FAST                'delimiters'
              468  LOAD_CONST               None
              470  COMPARE_OP               is

 L. 346   472_474  POP_JUMP_IF_TRUE    486  'to 486'

 L. 347       476  LOAD_FAST                'k'
              478  LOAD_FAST                'delimiters'
              480  COMPARE_OP               in

 L. 346   482_484  POP_JUMP_IF_FALSE_BACK   412  'to 412'
            486_0  COME_FROM           472  '472'

 L. 348       486  LOAD_FAST                'v'
              488  LOAD_FAST                'delims'
              490  LOAD_FAST                'k'
              492  STORE_SUBSCR     
          494_496  JUMP_BACK           412  'to 412'
            498_0  COME_FROM           412  '412'

 L. 349       498  LOAD_FAST                'consistency'
              500  LOAD_CONST               0.01
              502  INPLACE_SUBTRACT 
              504  STORE_FAST               'consistency'
          506_508  JUMP_BACK           384  'to 384'
            510_0  COME_FROM           404  '404'
            510_1  COME_FROM           394  '394'

 L. 351       510  LOAD_GLOBAL              len
              512  LOAD_FAST                'delims'
              514  CALL_FUNCTION_1       1  ''
              516  LOAD_CONST               1
              518  COMPARE_OP               ==
          520_522  POP_JUMP_IF_FALSE   580  'to 580'

 L. 352       524  LOAD_GLOBAL              list
              526  LOAD_FAST                'delims'
              528  LOAD_METHOD              keys
              530  CALL_METHOD_0         0  ''
              532  CALL_FUNCTION_1       1  ''
              534  LOAD_CONST               0
              536  BINARY_SUBSCR    
              538  STORE_FAST               'delim'

 L. 353       540  LOAD_FAST                'data'
              542  LOAD_CONST               0
              544  BINARY_SUBSCR    
              546  LOAD_METHOD              count
              548  LOAD_FAST                'delim'
              550  CALL_METHOD_1         1  ''

 L. 354       552  LOAD_FAST                'data'
              554  LOAD_CONST               0
              556  BINARY_SUBSCR    
              558  LOAD_METHOD              count
              560  LOAD_STR                 '%c '
              562  LOAD_FAST                'delim'
              564  BINARY_MODULO    
              566  CALL_METHOD_1         1  ''

 L. 353       568  COMPARE_OP               ==
              570  STORE_FAST               'skipinitialspace'

 L. 355       572  LOAD_FAST                'delim'
              574  LOAD_FAST                'skipinitialspace'
              576  BUILD_TUPLE_2         2 
              578  RETURN_VALUE     
            580_0  COME_FROM           520  '520'

 L. 358       580  LOAD_FAST                'end'
              582  STORE_FAST               'start'

 L. 359       584  LOAD_FAST                'end'
              586  LOAD_FAST                'chunkLength'
              588  INPLACE_ADD      
              590  STORE_FAST               'end'
              592  JUMP_BACK            78  'to 78'
            594_0  COME_FROM            88  '88'

 L. 361       594  LOAD_FAST                'delims'
          596_598  POP_JUMP_IF_TRUE    604  'to 604'

 L. 362       600  LOAD_CONST               ('', 0)
              602  RETURN_VALUE     
            604_0  COME_FROM           596  '596'

 L. 365       604  LOAD_GLOBAL              len
              606  LOAD_FAST                'delims'
              608  CALL_FUNCTION_1       1  ''
              610  LOAD_CONST               1
              612  COMPARE_OP               >
          614_616  POP_JUMP_IF_FALSE   690  'to 690'

 L. 366       618  LOAD_FAST                'self'
              620  LOAD_ATTR                preferred
              622  GET_ITER         
            624_0  COME_FROM           686  '686'
            624_1  COME_FROM           638  '638'
              624  FOR_ITER            690  'to 690'
              626  STORE_FAST               'd'

 L. 367       628  LOAD_FAST                'd'
              630  LOAD_FAST                'delims'
              632  LOAD_METHOD              keys
              634  CALL_METHOD_0         0  ''
              636  COMPARE_OP               in
          638_640  POP_JUMP_IF_FALSE_BACK   624  'to 624'

 L. 368       642  LOAD_FAST                'data'
              644  LOAD_CONST               0
              646  BINARY_SUBSCR    
              648  LOAD_METHOD              count
              650  LOAD_FAST                'd'
              652  CALL_METHOD_1         1  ''

 L. 369       654  LOAD_FAST                'data'
              656  LOAD_CONST               0
              658  BINARY_SUBSCR    
              660  LOAD_METHOD              count
              662  LOAD_STR                 '%c '
              664  LOAD_FAST                'd'
              666  BINARY_MODULO    
              668  CALL_METHOD_1         1  ''

 L. 368       670  COMPARE_OP               ==
              672  STORE_FAST               'skipinitialspace'

 L. 370       674  LOAD_FAST                'd'
              676  LOAD_FAST                'skipinitialspace'
              678  BUILD_TUPLE_2         2 
              680  ROT_TWO          
              682  POP_TOP          
              684  RETURN_VALUE     
          686_688  JUMP_BACK           624  'to 624'
            690_0  COME_FROM           624  '624'
            690_1  COME_FROM           614  '614'

 L. 374       690  LOAD_LISTCOMP            '<code_object <listcomp>>'
              692  LOAD_STR                 'Sniffer._guess_delimiter.<locals>.<listcomp>'
              694  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              696  LOAD_FAST                'delims'
              698  LOAD_METHOD              items
              700  CALL_METHOD_0         0  ''
              702  GET_ITER         
              704  CALL_FUNCTION_1       1  ''
              706  STORE_FAST               'items'

 L. 375       708  LOAD_FAST                'items'
              710  LOAD_METHOD              sort
              712  CALL_METHOD_0         0  ''
              714  POP_TOP          

 L. 376       716  LOAD_FAST                'items'
              718  LOAD_CONST               -1
              720  BINARY_SUBSCR    
              722  LOAD_CONST               1
              724  BINARY_SUBSCR    
              726  STORE_FAST               'delim'

 L. 378       728  LOAD_FAST                'data'
              730  LOAD_CONST               0
              732  BINARY_SUBSCR    
              734  LOAD_METHOD              count
              736  LOAD_FAST                'delim'
              738  CALL_METHOD_1         1  ''

 L. 379       740  LOAD_FAST                'data'
              742  LOAD_CONST               0
              744  BINARY_SUBSCR    
              746  LOAD_METHOD              count
              748  LOAD_STR                 '%c '
              750  LOAD_FAST                'delim'
              752  BINARY_MODULO    
              754  CALL_METHOD_1         1  ''

 L. 378       756  COMPARE_OP               ==
              758  STORE_FAST               'skipinitialspace'

 L. 380       760  LOAD_FAST                'delim'
              762  LOAD_FAST                'skipinitialspace'
              764  BUILD_TUPLE_2         2 
              766  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 766

        def has_header--- This code section failed: ---

 L. 393         0  LOAD_GLOBAL              reader
                2  LOAD_GLOBAL              StringIO
                4  LOAD_FAST                'sample'
                6  CALL_FUNCTION_1       1  ''
                8  LOAD_FAST                'self'
               10  LOAD_METHOD              sniff
               12  LOAD_FAST                'sample'
               14  CALL_METHOD_1         1  ''
               16  CALL_FUNCTION_2       2  ''
               18  STORE_FAST               'rdr'

 L. 395        20  LOAD_GLOBAL              next
               22  LOAD_FAST                'rdr'
               24  CALL_FUNCTION_1       1  ''
               26  STORE_FAST               'header'

 L. 397        28  LOAD_GLOBAL              len
               30  LOAD_FAST                'header'
               32  CALL_FUNCTION_1       1  ''
               34  STORE_FAST               'columns'

 L. 398        36  BUILD_MAP_0           0 
               38  STORE_FAST               'columnTypes'

 L. 399        40  LOAD_GLOBAL              range
               42  LOAD_FAST                'columns'
               44  CALL_FUNCTION_1       1  ''
               46  GET_ITER         
             48_0  COME_FROM            60  '60'
               48  FOR_ITER             62  'to 62'
               50  STORE_FAST               'i'

 L. 399        52  LOAD_CONST               None
               54  LOAD_FAST                'columnTypes'
               56  LOAD_FAST                'i'
               58  STORE_SUBSCR     
               60  JUMP_BACK            48  'to 48'
             62_0  COME_FROM            48  '48'

 L. 401        62  LOAD_CONST               0
               64  STORE_FAST               'checked'

 L. 402        66  LOAD_FAST                'rdr'
               68  GET_ITER         
             70_0  COME_FROM           242  '242'
             70_1  COME_FROM           106  '106'
               70  FOR_ITER            244  'to 244'
               72  STORE_FAST               'row'

 L. 404        74  LOAD_FAST                'checked'
               76  LOAD_CONST               20
               78  COMPARE_OP               >
               80  POP_JUMP_IF_FALSE    86  'to 86'

 L. 405        82  POP_TOP          
               84  BREAK_LOOP          244  'to 244'
             86_0  COME_FROM            80  '80'

 L. 406        86  LOAD_FAST                'checked'
               88  LOAD_CONST               1
               90  INPLACE_ADD      
               92  STORE_FAST               'checked'

 L. 408        94  LOAD_GLOBAL              len
               96  LOAD_FAST                'row'
               98  CALL_FUNCTION_1       1  ''
              100  LOAD_FAST                'columns'
              102  COMPARE_OP               !=
              104  POP_JUMP_IF_FALSE   108  'to 108'

 L. 409       106  JUMP_BACK            70  'to 70'
            108_0  COME_FROM           104  '104'

 L. 411       108  LOAD_GLOBAL              list
              110  LOAD_FAST                'columnTypes'
              112  LOAD_METHOD              keys
              114  CALL_METHOD_0         0  ''
              116  CALL_FUNCTION_1       1  ''
              118  GET_ITER         
            120_0  COME_FROM           240  '240'
            120_1  COME_FROM           232  '232'
            120_2  COME_FROM           210  '210'
              120  FOR_ITER            242  'to 242'
              122  STORE_FAST               'col'

 L. 413       124  LOAD_GLOBAL              int
              126  LOAD_GLOBAL              float
              128  LOAD_GLOBAL              complex
              130  BUILD_TUPLE_3         3 
              132  GET_ITER         
            134_0  COME_FROM           186  '186'
            134_1  COME_FROM           182  '182'
            134_2  COME_FROM           160  '160'
              134  FOR_ITER            188  'to 188'
              136  STORE_FAST               'thisType'

 L. 414       138  SETUP_FINALLY       162  'to 162'

 L. 415       140  LOAD_FAST                'thisType'
              142  LOAD_FAST                'row'
              144  LOAD_FAST                'col'
              146  BINARY_SUBSCR    
              148  CALL_FUNCTION_1       1  ''
              150  POP_TOP          

 L. 416       152  POP_BLOCK        
              154  POP_TOP          
              156  JUMP_FORWARD        200  'to 200'
              158  POP_BLOCK        
              160  JUMP_BACK           134  'to 134'
            162_0  COME_FROM_FINALLY   138  '138'

 L. 417       162  DUP_TOP          
              164  LOAD_GLOBAL              ValueError
              166  LOAD_GLOBAL              OverflowError
              168  BUILD_TUPLE_2         2 
              170  COMPARE_OP               exception-match
              172  POP_JUMP_IF_FALSE   184  'to 184'
              174  POP_TOP          
              176  POP_TOP          
              178  POP_TOP          

 L. 418       180  POP_EXCEPT       
              182  JUMP_BACK           134  'to 134'
            184_0  COME_FROM           172  '172'
              184  END_FINALLY      
              186  JUMP_BACK           134  'to 134'
            188_0  COME_FROM           134  '134'

 L. 421       188  LOAD_GLOBAL              len
              190  LOAD_FAST                'row'
              192  LOAD_FAST                'col'
              194  BINARY_SUBSCR    
              196  CALL_FUNCTION_1       1  ''
              198  STORE_FAST               'thisType'
            200_0  COME_FROM           156  '156'

 L. 423       200  LOAD_FAST                'thisType'
              202  LOAD_FAST                'columnTypes'
              204  LOAD_FAST                'col'
              206  BINARY_SUBSCR    
              208  COMPARE_OP               !=
              210  POP_JUMP_IF_FALSE_BACK   120  'to 120'

 L. 424       212  LOAD_FAST                'columnTypes'
              214  LOAD_FAST                'col'
              216  BINARY_SUBSCR    
              218  LOAD_CONST               None
              220  COMPARE_OP               is
              222  POP_JUMP_IF_FALSE   234  'to 234'

 L. 425       224  LOAD_FAST                'thisType'
              226  LOAD_FAST                'columnTypes'
              228  LOAD_FAST                'col'
              230  STORE_SUBSCR     
              232  JUMP_BACK           120  'to 120'
            234_0  COME_FROM           222  '222'

 L. 429       234  LOAD_FAST                'columnTypes'
              236  LOAD_FAST                'col'
              238  DELETE_SUBSCR    
              240  JUMP_BACK           120  'to 120'
            242_0  COME_FROM           120  '120'
              242  JUMP_BACK            70  'to 70'
            244_0  COME_FROM            84  '84'
            244_1  COME_FROM            70  '70'

 L. 433       244  LOAD_CONST               0
              246  STORE_FAST               'hasHeader'

 L. 434       248  LOAD_FAST                'columnTypes'
              250  LOAD_METHOD              items
              252  CALL_METHOD_0         0  ''
              254  GET_ITER         
            256_0  COME_FROM           380  '380'
            256_1  COME_FROM           368  '368'
            256_2  COME_FROM           318  '318'
              256  FOR_ITER            384  'to 384'
              258  UNPACK_SEQUENCE_2     2 
              260  STORE_FAST               'col'
              262  STORE_FAST               'colType'

 L. 435       264  LOAD_GLOBAL              type
              266  LOAD_FAST                'colType'
              268  CALL_FUNCTION_1       1  ''
              270  LOAD_GLOBAL              type
              272  LOAD_CONST               0
              274  CALL_FUNCTION_1       1  ''
              276  COMPARE_OP               ==
          278_280  POP_JUMP_IF_FALSE   320  'to 320'

 L. 436       282  LOAD_GLOBAL              len
              284  LOAD_FAST                'header'
              286  LOAD_FAST                'col'
              288  BINARY_SUBSCR    
              290  CALL_FUNCTION_1       1  ''
              292  LOAD_FAST                'colType'
              294  COMPARE_OP               !=
          296_298  POP_JUMP_IF_FALSE   310  'to 310'

 L. 437       300  LOAD_FAST                'hasHeader'
              302  LOAD_CONST               1
              304  INPLACE_ADD      
              306  STORE_FAST               'hasHeader'
              308  JUMP_FORWARD        318  'to 318'
            310_0  COME_FROM           296  '296'

 L. 439       310  LOAD_FAST                'hasHeader'
              312  LOAD_CONST               1
              314  INPLACE_SUBTRACT 
              316  STORE_FAST               'hasHeader'
            318_0  COME_FROM           308  '308'
              318  JUMP_BACK           256  'to 256'
            320_0  COME_FROM           278  '278'

 L. 441       320  SETUP_FINALLY       338  'to 338'

 L. 442       322  LOAD_FAST                'colType'
              324  LOAD_FAST                'header'
              326  LOAD_FAST                'col'
              328  BINARY_SUBSCR    
              330  CALL_FUNCTION_1       1  ''
              332  POP_TOP          
              334  POP_BLOCK        
              336  JUMP_FORWARD        372  'to 372'
            338_0  COME_FROM_FINALLY   320  '320'

 L. 443       338  DUP_TOP          
              340  LOAD_GLOBAL              ValueError
              342  LOAD_GLOBAL              TypeError
              344  BUILD_TUPLE_2         2 
              346  COMPARE_OP               exception-match
          348_350  POP_JUMP_IF_FALSE   370  'to 370'
              352  POP_TOP          
              354  POP_TOP          
              356  POP_TOP          

 L. 444       358  LOAD_FAST                'hasHeader'
              360  LOAD_CONST               1
              362  INPLACE_ADD      
              364  STORE_FAST               'hasHeader'
              366  POP_EXCEPT       
              368  JUMP_BACK           256  'to 256'
            370_0  COME_FROM           348  '348'
              370  END_FINALLY      
            372_0  COME_FROM           336  '336'

 L. 446       372  LOAD_FAST                'hasHeader'
              374  LOAD_CONST               1
              376  INPLACE_SUBTRACT 
              378  STORE_FAST               'hasHeader'
          380_382  JUMP_BACK           256  'to 256'
            384_0  COME_FROM           256  '256'

 L. 448       384  LOAD_FAST                'hasHeader'
              386  LOAD_CONST               0
              388  COMPARE_OP               >
              390  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 390