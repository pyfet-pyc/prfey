# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\PIL\EpsImagePlugin.py
import io, os, re, subprocess, sys, tempfile
from . import Image, ImageFile
from ._binary import i32le as i32
split = re.compile('^%%([^:]*):[ \\t]*(.*)[ \\t]*$')
field = re.compile('^%[%!\\w]([^:]*)[ \\t]*$')
gs_windows_binary = None
if sys.platform.startswith('win'):
    import shutil
    for binary in ('gswin32c', 'gswin64c', 'gs'):
        if shutil.which(binary) is not None:
            gs_windows_binary = binary
            break
    else:
        gs_windows_binary = False

def has_ghostscript--- This code section failed: ---

 L.  52         0  LOAD_GLOBAL              gs_windows_binary
                2  POP_JUMP_IF_FALSE     8  'to 8'

 L.  53         4  LOAD_CONST               True
                6  RETURN_VALUE     
              8_0  COME_FROM             2  '2'

 L.  54         8  LOAD_GLOBAL              sys
               10  LOAD_ATTR                platform
               12  LOAD_METHOD              startswith
               14  LOAD_STR                 'win'
               16  CALL_METHOD_1         1  ''
               18  POP_JUMP_IF_TRUE     68  'to 68'

 L.  55        20  SETUP_FINALLY        48  'to 48'

 L.  56        22  LOAD_GLOBAL              subprocess
               24  LOAD_ATTR                check_call
               26  LOAD_STR                 'gs'
               28  LOAD_STR                 '--version'
               30  BUILD_LIST_2          2 
               32  LOAD_GLOBAL              subprocess
               34  LOAD_ATTR                DEVNULL
               36  LOAD_CONST               ('stdout',)
               38  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               40  POP_TOP          

 L.  57        42  POP_BLOCK        
               44  LOAD_CONST               True
               46  RETURN_VALUE     
             48_0  COME_FROM_FINALLY    20  '20'

 L.  58        48  DUP_TOP          
               50  LOAD_GLOBAL              OSError
               52  COMPARE_OP               exception-match
               54  POP_JUMP_IF_FALSE    66  'to 66'
               56  POP_TOP          
               58  POP_TOP          
               60  POP_TOP          

 L.  60        62  POP_EXCEPT       
               64  JUMP_FORWARD         68  'to 68'
             66_0  COME_FROM            54  '54'
               66  END_FINALLY      
             68_0  COME_FROM            64  '64'
             68_1  COME_FROM            18  '18'

 L.  61        68  LOAD_CONST               False
               70  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 46


def Ghostscript(tile, size, fp, scale=1):
    """Render an image using Ghostscript"""
    decoder, tile, offset, data = tile[0]
    length, bbox = data
    scale = int(scale) or 1
    size = (
     size[0] * scale, size[1] * scale)
    res = (
     float(72.0 * size[0] / (bbox[2] - bbox[0])),
     float(72.0 * size[1] / (bbox[3] - bbox[1])))
    out_fd, outfile = tempfile.mkstemp()
    os.close(out_fd)
    infile_temp = None
    if hasattr(fp, 'name') and os.path.exists(fp.name):
        infile = fp.name
    else:
        in_fd, infile_temp = tempfile.mkstemp()
        os.close(in_fd)
        infile = infile_temp
        with open(infile_temp, 'wb') as (f):
            fp.seek(0, io.SEEK_END)
            fsize = fp.tell()
            fp.seek(0)
            lengthfile = fsize
            while lengthfile > 0:
                s = fp.read(min(lengthfile, 102400))
                if not s:
                    break
                lengthfile -= len(s)
                f.write(s)

    command = ['gs',
     '-q',
     '-g%dx%d' % size,
     '-r%fx%f' % res,
     '-dBATCH',
     '-dNOPAUSE',
     '-dSAFER',
     '-sDEVICE=ppmraw',
     '-sOutputFile=%s' % outfile,
     '-c',
     '%d %d translate' % (-bbox[0], -bbox[1]),
     '-f',
     infile,
     '-c',
     'showpage']
    if gs_windows_binary is not None:
        if not gs_windows_binary:
            raise OSError('Unable to locate Ghostscript on paths')
        command[0] = gs_windows_binary
    try:
        startupinfo = None
        if sys.platform.startswith('win'):
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.check_call(command, startupinfo=startupinfo)
        im = Image.open(outfile)
        im.load()
    finally:
        try:
            os.unlink(outfile)
            if infile_temp:
                os.unlink(infile_temp)
        except OSError:
            pass

    return im.im.copy()


class PSFile:
    __doc__ = '\n    Wrapper for bytesio object that treats either CR or LF as end of line.\n    '

    def __init__(self, fp):
        self.fp = fp
        self.char = None

    def seek(self, offset, whence=io.SEEK_SET):
        self.char = None
        self.fp.seek(offset, whence)

    def readline(self):
        s = self.char or b''
        self.char = None
        c = self.fp.read(1)
        while c not in b'\r\n':
            s = s + c
            c = self.fp.read(1)

        self.char = self.fp.read(1)
        if self.char in b'\r\n':
            self.char = None
        return s.decode('latin-1')


def _accept(prefix):
    return prefix[:4] == b'%!PS' or len(prefix) >= 4 and i32(prefix) == 3335770309


class EpsImageFile(ImageFile.ImageFile):
    __doc__ = 'EPS File Parser for the Python Imaging Library'
    format = 'EPS'
    format_description = 'Encapsulated Postscript'
    mode_map = {1:'L', 
     2:'LAB',  3:'RGB',  4:'CMYK'}

    def _open--- This code section failed: ---

 L. 205         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _find_offset
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                fp
                8  CALL_METHOD_1         1  ''
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'length'
               14  STORE_FAST               'offset'

 L. 209        16  LOAD_GLOBAL              PSFile
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                fp
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'fp'

 L. 212        26  LOAD_FAST                'fp'
               28  LOAD_METHOD              seek
               30  LOAD_FAST                'offset'
               32  CALL_METHOD_1         1  ''
               34  POP_TOP          

 L. 214        36  LOAD_CONST               None
               38  STORE_FAST               'box'

 L. 216        40  LOAD_STR                 'RGB'
               42  LOAD_FAST                'self'
               44  STORE_ATTR               mode

 L. 217        46  LOAD_CONST               (1, 1)
               48  LOAD_FAST                'self'
               50  STORE_ATTR               _size

 L. 222        52  LOAD_FAST                'fp'
               54  LOAD_METHOD              readline
               56  CALL_METHOD_0         0  ''
               58  STORE_FAST               's_raw'

 L. 223        60  LOAD_FAST                's_raw'
               62  LOAD_METHOD              strip
               64  LOAD_STR                 '\r\n'
               66  CALL_METHOD_1         1  ''
               68  STORE_FAST               's'
             70_0  COME_FROM           456  '456'
             70_1  COME_FROM           440  '440'

 L. 225        70  LOAD_FAST                's_raw'
            72_74  POP_JUMP_IF_FALSE   464  'to 464'

 L. 226        76  LOAD_FAST                's'
            78_80  POP_JUMP_IF_FALSE   420  'to 420'

 L. 227        82  LOAD_GLOBAL              len
               84  LOAD_FAST                's'
               86  CALL_FUNCTION_1       1  ''
               88  LOAD_CONST               255
               90  COMPARE_OP               >
               92  POP_JUMP_IF_FALSE   102  'to 102'

 L. 228        94  LOAD_GLOBAL              SyntaxError
               96  LOAD_STR                 'not an EPS file'
               98  CALL_FUNCTION_1       1  ''
              100  RAISE_VARARGS_1       1  'exception instance'
            102_0  COME_FROM            92  '92'

 L. 230       102  SETUP_FINALLY       118  'to 118'

 L. 231       104  LOAD_GLOBAL              split
              106  LOAD_METHOD              match
              108  LOAD_FAST                's'
              110  CALL_METHOD_1         1  ''
              112  STORE_FAST               'm'
              114  POP_BLOCK        
              116  JUMP_FORWARD        148  'to 148'
            118_0  COME_FROM_FINALLY   102  '102'

 L. 232       118  DUP_TOP          
              120  LOAD_GLOBAL              re
              122  LOAD_ATTR                error
              124  COMPARE_OP               exception-match
              126  POP_JUMP_IF_FALSE   146  'to 146'
              128  POP_TOP          
              130  POP_TOP          
              132  POP_TOP          

 L. 233       134  LOAD_GLOBAL              SyntaxError
              136  LOAD_STR                 'not an EPS file'
              138  CALL_FUNCTION_1       1  ''
              140  RAISE_VARARGS_1       1  'exception instance'
              142  POP_EXCEPT       
              144  JUMP_FORWARD        148  'to 148'
            146_0  COME_FROM           126  '126'
              146  END_FINALLY      
            148_0  COME_FROM           144  '144'
            148_1  COME_FROM           116  '116'

 L. 235       148  LOAD_FAST                'm'
          150_152  POP_JUMP_IF_FALSE   298  'to 298'

 L. 236       154  LOAD_FAST                'm'
              156  LOAD_METHOD              group
              158  LOAD_CONST               1
              160  LOAD_CONST               2
              162  CALL_METHOD_2         2  ''
              164  UNPACK_SEQUENCE_2     2 
              166  STORE_FAST               'k'
              168  STORE_FAST               'v'

 L. 237       170  LOAD_FAST                'v'
              172  LOAD_FAST                'self'
              174  LOAD_ATTR                info
              176  LOAD_FAST                'k'
              178  STORE_SUBSCR     

 L. 238       180  LOAD_FAST                'k'
              182  LOAD_STR                 'BoundingBox'
              184  COMPARE_OP               ==
          186_188  POP_JUMP_IF_FALSE   420  'to 420'

 L. 239       190  SETUP_FINALLY       274  'to 274'

 L. 243       192  LOAD_LISTCOMP            '<code_object <listcomp>>'
              194  LOAD_STR                 'EpsImageFile._open.<locals>.<listcomp>'
              196  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              198  LOAD_FAST                'v'
              200  LOAD_METHOD              split
              202  CALL_METHOD_0         0  ''
              204  GET_ITER         
              206  CALL_FUNCTION_1       1  ''
              208  STORE_FAST               'box'

 L. 244       210  LOAD_FAST                'box'
              212  LOAD_CONST               2
              214  BINARY_SUBSCR    
              216  LOAD_FAST                'box'
              218  LOAD_CONST               0
              220  BINARY_SUBSCR    
              222  BINARY_SUBTRACT  
              224  LOAD_FAST                'box'
              226  LOAD_CONST               3
              228  BINARY_SUBSCR    
              230  LOAD_FAST                'box'
              232  LOAD_CONST               1
              234  BINARY_SUBSCR    
              236  BINARY_SUBTRACT  
              238  BUILD_TUPLE_2         2 
              240  LOAD_FAST                'self'
              242  STORE_ATTR               _size

 L. 246       244  LOAD_STR                 'eps'
              246  LOAD_CONST               (0, 0)
              248  LOAD_FAST                'self'
              250  LOAD_ATTR                size
              252  BINARY_ADD       
              254  LOAD_FAST                'offset'
              256  LOAD_FAST                'length'
              258  LOAD_FAST                'box'
              260  BUILD_TUPLE_2         2 
              262  BUILD_TUPLE_4         4 

 L. 245       264  BUILD_LIST_1          1 
              266  LOAD_FAST                'self'
              268  STORE_ATTR               tile
              270  POP_BLOCK        
              272  JUMP_FORWARD        296  'to 296'
            274_0  COME_FROM_FINALLY   190  '190'

 L. 248       274  DUP_TOP          
              276  LOAD_GLOBAL              Exception
              278  COMPARE_OP               exception-match
          280_282  POP_JUMP_IF_FALSE   294  'to 294'
              284  POP_TOP          
              286  POP_TOP          
              288  POP_TOP          

 L. 249       290  POP_EXCEPT       
              292  JUMP_FORWARD        296  'to 296'
            294_0  COME_FROM           280  '280'
              294  END_FINALLY      
            296_0  COME_FROM           292  '292'
            296_1  COME_FROM           272  '272'
              296  JUMP_FORWARD        420  'to 420'
            298_0  COME_FROM           150  '150'

 L. 252       298  LOAD_GLOBAL              field
              300  LOAD_METHOD              match
              302  LOAD_FAST                's'
              304  CALL_METHOD_1         1  ''
              306  STORE_FAST               'm'

 L. 253       308  LOAD_FAST                'm'
          310_312  POP_JUMP_IF_FALSE   396  'to 396'

 L. 254       314  LOAD_FAST                'm'
              316  LOAD_METHOD              group
              318  LOAD_CONST               1
              320  CALL_METHOD_1         1  ''
              322  STORE_FAST               'k'

 L. 256       324  LOAD_FAST                'k'
              326  LOAD_STR                 'EndComments'
              328  COMPARE_OP               ==
          330_332  POP_JUMP_IF_FALSE   338  'to 338'

 L. 257   334_336  BREAK_LOOP          464  'to 464'
            338_0  COME_FROM           330  '330'

 L. 258       338  LOAD_FAST                'k'
              340  LOAD_CONST               None
              342  LOAD_CONST               8
              344  BUILD_SLICE_2         2 
              346  BINARY_SUBSCR    
              348  LOAD_STR                 'PS-Adobe'
              350  COMPARE_OP               ==
          352_354  POP_JUMP_IF_FALSE   384  'to 384'

 L. 259       356  LOAD_FAST                'k'
              358  LOAD_CONST               9
              360  LOAD_CONST               None
              362  BUILD_SLICE_2         2 
              364  BINARY_SUBSCR    
              366  LOAD_FAST                'self'
              368  LOAD_ATTR                info
              370  LOAD_FAST                'k'
              372  LOAD_CONST               None
              374  LOAD_CONST               8
              376  BUILD_SLICE_2         2 
              378  BINARY_SUBSCR    
              380  STORE_SUBSCR     
              382  JUMP_FORWARD        394  'to 394'
            384_0  COME_FROM           352  '352'

 L. 261       384  LOAD_STR                 ''
              386  LOAD_FAST                'self'
              388  LOAD_ATTR                info
              390  LOAD_FAST                'k'
              392  STORE_SUBSCR     
            394_0  COME_FROM           382  '382'
              394  JUMP_FORWARD        420  'to 420'
            396_0  COME_FROM           310  '310'

 L. 262       396  LOAD_FAST                's'
              398  LOAD_CONST               0
              400  BINARY_SUBSCR    
              402  LOAD_STR                 '%'
              404  COMPARE_OP               ==
          406_408  POP_JUMP_IF_FALSE   412  'to 412'

 L. 265       410  BREAK_LOOP          420  'to 420'
            412_0  COME_FROM           406  '406'

 L. 267       412  LOAD_GLOBAL              OSError
              414  LOAD_STR                 'bad EPS header'
              416  CALL_FUNCTION_1       1  ''
              418  RAISE_VARARGS_1       1  'exception instance'
            420_0  COME_FROM           410  '410'
            420_1  COME_FROM           394  '394'
            420_2  COME_FROM           296  '296'
            420_3  COME_FROM           186  '186'
            420_4  COME_FROM            78  '78'

 L. 269       420  LOAD_FAST                'fp'
              422  LOAD_METHOD              readline
              424  CALL_METHOD_0         0  ''
              426  STORE_FAST               's_raw'

 L. 270       428  LOAD_FAST                's_raw'
              430  LOAD_METHOD              strip
              432  LOAD_STR                 '\r\n'
              434  CALL_METHOD_1         1  ''
              436  STORE_FAST               's'

 L. 272       438  LOAD_FAST                's'
              440  POP_JUMP_IF_FALSE    70  'to 70'
              442  LOAD_FAST                's'
              444  LOAD_CONST               None
              446  LOAD_CONST               1
              448  BUILD_SLICE_2         2 
              450  BINARY_SUBSCR    
              452  LOAD_STR                 '%'
              454  COMPARE_OP               !=
              456  POP_JUMP_IF_FALSE    70  'to 70'

 L. 273   458_460  BREAK_LOOP          464  'to 464'
              462  JUMP_BACK            70  'to 70'
            464_0  COME_FROM           664  '664'
            464_1  COME_FROM            72  '72'

 L. 278       464  LOAD_FAST                's'
              466  LOAD_CONST               None
              468  LOAD_CONST               1
              470  BUILD_SLICE_2         2 
              472  BINARY_SUBSCR    
              474  LOAD_STR                 '%'
              476  COMPARE_OP               ==
          478_480  POP_JUMP_IF_FALSE   676  'to 676'

 L. 280       482  LOAD_GLOBAL              len
              484  LOAD_FAST                's'
              486  CALL_FUNCTION_1       1  ''
              488  LOAD_CONST               255
              490  COMPARE_OP               >
          492_494  POP_JUMP_IF_FALSE   504  'to 504'

 L. 281       496  LOAD_GLOBAL              SyntaxError
              498  LOAD_STR                 'not an EPS file'
              500  CALL_FUNCTION_1       1  ''
              502  RAISE_VARARGS_1       1  'exception instance'
            504_0  COME_FROM           492  '492'

 L. 283       504  LOAD_FAST                's'
              506  LOAD_CONST               None
              508  LOAD_CONST               11
              510  BUILD_SLICE_2         2 
              512  BINARY_SUBSCR    
              514  LOAD_STR                 '%ImageData:'
              516  COMPARE_OP               ==
          518_520  POP_JUMP_IF_FALSE   648  'to 648'

 L. 285       522  LOAD_FAST                's'
              524  LOAD_CONST               11
              526  LOAD_CONST               None
              528  BUILD_SLICE_2         2 
              530  BINARY_SUBSCR    
              532  LOAD_METHOD              split
              534  LOAD_CONST               None
              536  LOAD_CONST               7
              538  CALL_METHOD_2         2  ''
              540  LOAD_CONST               None
              542  LOAD_CONST               4
              544  BUILD_SLICE_2         2 
              546  BINARY_SUBSCR    
              548  UNPACK_SEQUENCE_4     4 
              550  STORE_FAST               'x'
              552  STORE_FAST               'y'
              554  STORE_FAST               'bi'
              556  STORE_FAST               'mo'

 L. 287       558  LOAD_GLOBAL              int
              560  LOAD_FAST                'bi'
              562  CALL_FUNCTION_1       1  ''
              564  LOAD_CONST               8
              566  COMPARE_OP               !=
          568_570  POP_JUMP_IF_FALSE   576  'to 576'

 L. 288   572_574  BREAK_LOOP          676  'to 676'
            576_0  COME_FROM           568  '568'

 L. 289       576  SETUP_FINALLY       598  'to 598'

 L. 290       578  LOAD_FAST                'self'
              580  LOAD_ATTR                mode_map
              582  LOAD_GLOBAL              int
              584  LOAD_FAST                'mo'
              586  CALL_FUNCTION_1       1  ''
              588  BINARY_SUBSCR    
              590  LOAD_FAST                'self'
              592  STORE_ATTR               mode
              594  POP_BLOCK        
              596  JUMP_FORWARD        626  'to 626'
            598_0  COME_FROM_FINALLY   576  '576'

 L. 291       598  DUP_TOP          
              600  LOAD_GLOBAL              ValueError
              602  COMPARE_OP               exception-match
          604_606  POP_JUMP_IF_FALSE   624  'to 624'
              608  POP_TOP          
              610  POP_TOP          
              612  POP_TOP          

 L. 292       614  POP_EXCEPT       
          616_618  JUMP_ABSOLUTE       676  'to 676'
              620  POP_EXCEPT       
              622  JUMP_FORWARD        626  'to 626'
            624_0  COME_FROM           604  '604'
              624  END_FINALLY      
            626_0  COME_FROM           622  '622'
            626_1  COME_FROM           596  '596'

 L. 294       626  LOAD_GLOBAL              int
              628  LOAD_FAST                'x'
              630  CALL_FUNCTION_1       1  ''
              632  LOAD_GLOBAL              int
              634  LOAD_FAST                'y'
              636  CALL_FUNCTION_1       1  ''
              638  BUILD_TUPLE_2         2 
              640  LOAD_FAST                'self'
              642  STORE_ATTR               _size

 L. 295       644  LOAD_CONST               None
              646  RETURN_VALUE     
            648_0  COME_FROM           518  '518'

 L. 297       648  LOAD_FAST                'fp'
              650  LOAD_METHOD              readline
              652  CALL_METHOD_0         0  ''
              654  LOAD_METHOD              strip
              656  LOAD_STR                 '\r\n'
              658  CALL_METHOD_1         1  ''
              660  STORE_FAST               's'

 L. 298       662  LOAD_FAST                's'
          664_666  POP_JUMP_IF_TRUE    464  'to 464'

 L. 299   668_670  BREAK_LOOP          676  'to 676'
          672_674  JUMP_BACK           464  'to 464'
            676_0  COME_FROM           478  '478'

 L. 301       676  LOAD_FAST                'box'
          678_680  POP_JUMP_IF_TRUE    690  'to 690'

 L. 302       682  LOAD_GLOBAL              OSError
              684  LOAD_STR                 'cannot determine EPS bounding box'
              686  CALL_FUNCTION_1       1  ''
              688  RAISE_VARARGS_1       1  'exception instance'
            690_0  COME_FROM           678  '678'

Parse error at or near `POP_EXCEPT' instruction at offset 620

    def _find_offset(self, fp):
        s = fp.read(160)
        if s[:4] == b'%!PS':
            fp.seek(0, io.SEEK_END)
            length = fp.tell()
            offset = 0
        else:
            if i32(s[0:4]) == 3335770309:
                offset = i32(s[4:8])
                length = i32(s[8:12])
            else:
                raise SyntaxError('not an EPS file')
        return (
         length, offset)

    def load(self, scale=1):
        if not self.tile:
            return
        self.im = Ghostscript(self.tile, self.size, self.fp, scale)
        self.mode = self.im.mode
        self._size = self.im.size
        self.tile = []

    def load_seek(self, *args, **kwargs):
        pass


def _save(im, fp, filename, eps=1):
    """EPS Writer for the Python Imaging Library."""
    im.load()
    if im.mode == 'L':
        operator = (8, 1, 'image')
    else:
        if im.mode == 'RGB':
            operator = (8, 3, 'false 3 colorimage')
        else:
            if im.mode == 'CMYK':
                operator = (8, 4, 'false 4 colorimage')
            else:
                raise ValueError('image mode is not supported')
    base_fp = fp
    wrapped_fp = False
    if fp != sys.stdout:
        fp = io.TextIOWrapper(fp, encoding='latin-1')
        wrapped_fp = True
    try:
        if eps:
            fp.write('%!PS-Adobe-3.0 EPSF-3.0\n')
            fp.write('%%Creator: PIL 0.1 EpsEncode\n')
            fp.write('%%%%BoundingBox: 0 0 %d %d\n' % im.size)
            fp.write('%%Pages: 1\n')
            fp.write('%%EndComments\n')
            fp.write('%%Page: 1 1\n')
            fp.write('%%ImageData: %d %d ' % im.size)
            fp.write('%d %d 0 1 1 "%s"\n' % operator)
        fp.write('gsave\n')
        fp.write('10 dict begin\n')
        fp.write('/buf %d string def\n' % (im.size[0] * operator[1]))
        fp.write('%d %d scale\n' % im.size)
        fp.write('%d %d 8\n' % im.size)
        fp.write('[%d 0 0 -%d 0 %d]\n' % (im.size[0], im.size[1], im.size[1]))
        fp.write('{ currentfile buf readhexstring pop } bind\n')
        fp.write(operator[2] + '\n')
        if hasattr(fp, 'flush'):
            fp.flush()
        ImageFile._save(im, base_fp, [('eps', (0, 0) + im.size, 0, None)])
        fp.write('\n%%%%EndBinary\n')
        fp.write('grestore end\n')
        if hasattr(fp, 'flush'):
            fp.flush()
    finally:
        if wrapped_fp:
            fp.detach()


Image.register_open(EpsImageFile.format, EpsImageFile, _accept)
Image.register_save(EpsImageFile.format, _save)
Image.register_extensions(EpsImageFile.format, ['.ps', '.eps'])
Image.register_mime(EpsImageFile.format, 'application/postscript')