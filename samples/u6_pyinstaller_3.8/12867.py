# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: PIL\EpsImagePlugin.py
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
     72.0 * size[0] / (bbox[2] - bbox[0]),
     72.0 * size[1] / (bbox[3] - bbox[1]))
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
     f"-sOutputFile={outfile}",
     '-c',
     f"{-bbox[0]} {-bbox[1]} translate",
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
        out_im = Image.open(outfile)
        out_im.load()
    finally:
        try:
            os.unlink(outfile)
            if infile_temp:
                os.unlink(infile_temp)
        except OSError:
            pass

    im = out_im.im.copy()
    out_im.close()
    return im


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

 L. 207         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _find_offset
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                fp
                8  CALL_METHOD_1         1  ''
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'length'
               14  STORE_FAST               'offset'

 L. 211        16  LOAD_GLOBAL              PSFile
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                fp
               22  CALL_FUNCTION_1       1  ''
               24  STORE_FAST               'fp'

 L. 214        26  LOAD_FAST                'fp'
               28  LOAD_METHOD              seek
               30  LOAD_FAST                'offset'
               32  CALL_METHOD_1         1  ''
               34  POP_TOP          

 L. 216        36  LOAD_CONST               None
               38  STORE_FAST               'box'

 L. 218        40  LOAD_STR                 'RGB'
               42  LOAD_FAST                'self'
               44  STORE_ATTR               mode

 L. 219        46  LOAD_CONST               (1, 1)
               48  LOAD_FAST                'self'
               50  STORE_ATTR               _size

 L. 224        52  LOAD_FAST                'fp'
               54  LOAD_METHOD              readline
               56  CALL_METHOD_0         0  ''
               58  STORE_FAST               's_raw'

 L. 225        60  LOAD_FAST                's_raw'
               62  LOAD_METHOD              strip
               64  LOAD_STR                 '\r\n'
               66  CALL_METHOD_1         1  ''
               68  STORE_FAST               's'
             70_0  COME_FROM           472  '472'
             70_1  COME_FROM           456  '456'

 L. 227        70  LOAD_FAST                's_raw'
            72_74  POP_JUMP_IF_FALSE   480  'to 480'

 L. 228        76  LOAD_FAST                's'
            78_80  POP_JUMP_IF_FALSE   436  'to 436'

 L. 229        82  LOAD_GLOBAL              len
               84  LOAD_FAST                's'
               86  CALL_FUNCTION_1       1  ''
               88  LOAD_CONST               255
               90  COMPARE_OP               >
               92  POP_JUMP_IF_FALSE   102  'to 102'

 L. 230        94  LOAD_GLOBAL              SyntaxError
               96  LOAD_STR                 'not an EPS file'
               98  CALL_FUNCTION_1       1  ''
              100  RAISE_VARARGS_1       1  'exception instance'
            102_0  COME_FROM            92  '92'

 L. 232       102  SETUP_FINALLY       118  'to 118'

 L. 233       104  LOAD_GLOBAL              split
              106  LOAD_METHOD              match
              108  LOAD_FAST                's'
              110  CALL_METHOD_1         1  ''
              112  STORE_FAST               'm'
              114  POP_BLOCK        
              116  JUMP_FORWARD        164  'to 164'
            118_0  COME_FROM_FINALLY   102  '102'

 L. 234       118  DUP_TOP          
              120  LOAD_GLOBAL              re
              122  LOAD_ATTR                error
              124  COMPARE_OP               exception-match
              126  POP_JUMP_IF_FALSE   162  'to 162'
              128  POP_TOP          
              130  STORE_FAST               'e'
              132  POP_TOP          
              134  SETUP_FINALLY       150  'to 150'

 L. 235       136  LOAD_GLOBAL              SyntaxError
              138  LOAD_STR                 'not an EPS file'
              140  CALL_FUNCTION_1       1  ''
              142  LOAD_FAST                'e'
              144  RAISE_VARARGS_2       2  'exception instance with __cause__'
              146  POP_BLOCK        
              148  BEGIN_FINALLY    
            150_0  COME_FROM_FINALLY   134  '134'
              150  LOAD_CONST               None
              152  STORE_FAST               'e'
              154  DELETE_FAST              'e'
              156  END_FINALLY      
              158  POP_EXCEPT       
              160  JUMP_FORWARD        164  'to 164'
            162_0  COME_FROM           126  '126'
              162  END_FINALLY      
            164_0  COME_FROM           160  '160'
            164_1  COME_FROM           116  '116'

 L. 237       164  LOAD_FAST                'm'
          166_168  POP_JUMP_IF_FALSE   314  'to 314'

 L. 238       170  LOAD_FAST                'm'
              172  LOAD_METHOD              group
              174  LOAD_CONST               1
              176  LOAD_CONST               2
              178  CALL_METHOD_2         2  ''
              180  UNPACK_SEQUENCE_2     2 
              182  STORE_FAST               'k'
              184  STORE_FAST               'v'

 L. 239       186  LOAD_FAST                'v'
              188  LOAD_FAST                'self'
              190  LOAD_ATTR                info
              192  LOAD_FAST                'k'
              194  STORE_SUBSCR     

 L. 240       196  LOAD_FAST                'k'
              198  LOAD_STR                 'BoundingBox'
              200  COMPARE_OP               ==
          202_204  POP_JUMP_IF_FALSE   436  'to 436'

 L. 241       206  SETUP_FINALLY       290  'to 290'

 L. 245       208  LOAD_LISTCOMP            '<code_object <listcomp>>'
              210  LOAD_STR                 'EpsImageFile._open.<locals>.<listcomp>'
              212  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              214  LOAD_FAST                'v'
              216  LOAD_METHOD              split
              218  CALL_METHOD_0         0  ''
              220  GET_ITER         
              222  CALL_FUNCTION_1       1  ''
              224  STORE_FAST               'box'

 L. 246       226  LOAD_FAST                'box'
              228  LOAD_CONST               2
              230  BINARY_SUBSCR    
              232  LOAD_FAST                'box'
              234  LOAD_CONST               0
              236  BINARY_SUBSCR    
              238  BINARY_SUBTRACT  
              240  LOAD_FAST                'box'
              242  LOAD_CONST               3
              244  BINARY_SUBSCR    
              246  LOAD_FAST                'box'
              248  LOAD_CONST               1
              250  BINARY_SUBSCR    
              252  BINARY_SUBTRACT  
              254  BUILD_TUPLE_2         2 
              256  LOAD_FAST                'self'
              258  STORE_ATTR               _size

 L. 248       260  LOAD_STR                 'eps'
              262  LOAD_CONST               (0, 0)
              264  LOAD_FAST                'self'
              266  LOAD_ATTR                size
              268  BINARY_ADD       
              270  LOAD_FAST                'offset'
              272  LOAD_FAST                'length'
              274  LOAD_FAST                'box'
              276  BUILD_TUPLE_2         2 
              278  BUILD_TUPLE_4         4 

 L. 247       280  BUILD_LIST_1          1 
              282  LOAD_FAST                'self'
              284  STORE_ATTR               tile
              286  POP_BLOCK        
              288  JUMP_FORWARD        312  'to 312'
            290_0  COME_FROM_FINALLY   206  '206'

 L. 250       290  DUP_TOP          
              292  LOAD_GLOBAL              Exception
              294  COMPARE_OP               exception-match
          296_298  POP_JUMP_IF_FALSE   310  'to 310'
              300  POP_TOP          
              302  POP_TOP          
              304  POP_TOP          

 L. 251       306  POP_EXCEPT       
              308  JUMP_FORWARD        312  'to 312'
            310_0  COME_FROM           296  '296'
              310  END_FINALLY      
            312_0  COME_FROM           308  '308'
            312_1  COME_FROM           288  '288'
              312  JUMP_FORWARD        436  'to 436'
            314_0  COME_FROM           166  '166'

 L. 254       314  LOAD_GLOBAL              field
              316  LOAD_METHOD              match
              318  LOAD_FAST                's'
              320  CALL_METHOD_1         1  ''
              322  STORE_FAST               'm'

 L. 255       324  LOAD_FAST                'm'
          326_328  POP_JUMP_IF_FALSE   412  'to 412'

 L. 256       330  LOAD_FAST                'm'
              332  LOAD_METHOD              group
              334  LOAD_CONST               1
              336  CALL_METHOD_1         1  ''
              338  STORE_FAST               'k'

 L. 258       340  LOAD_FAST                'k'
              342  LOAD_STR                 'EndComments'
              344  COMPARE_OP               ==
          346_348  POP_JUMP_IF_FALSE   354  'to 354'

 L. 259   350_352  BREAK_LOOP          480  'to 480'
            354_0  COME_FROM           346  '346'

 L. 260       354  LOAD_FAST                'k'
              356  LOAD_CONST               None
              358  LOAD_CONST               8
              360  BUILD_SLICE_2         2 
              362  BINARY_SUBSCR    
              364  LOAD_STR                 'PS-Adobe'
              366  COMPARE_OP               ==
          368_370  POP_JUMP_IF_FALSE   400  'to 400'

 L. 261       372  LOAD_FAST                'k'
              374  LOAD_CONST               9
              376  LOAD_CONST               None
              378  BUILD_SLICE_2         2 
              380  BINARY_SUBSCR    
              382  LOAD_FAST                'self'
              384  LOAD_ATTR                info
              386  LOAD_FAST                'k'
              388  LOAD_CONST               None
              390  LOAD_CONST               8
              392  BUILD_SLICE_2         2 
              394  BINARY_SUBSCR    
              396  STORE_SUBSCR     
              398  JUMP_FORWARD        410  'to 410'
            400_0  COME_FROM           368  '368'

 L. 263       400  LOAD_STR                 ''
              402  LOAD_FAST                'self'
              404  LOAD_ATTR                info
              406  LOAD_FAST                'k'
              408  STORE_SUBSCR     
            410_0  COME_FROM           398  '398'
              410  JUMP_FORWARD        436  'to 436'
            412_0  COME_FROM           326  '326'

 L. 264       412  LOAD_FAST                's'
              414  LOAD_CONST               0
              416  BINARY_SUBSCR    
              418  LOAD_STR                 '%'
              420  COMPARE_OP               ==
          422_424  POP_JUMP_IF_FALSE   428  'to 428'

 L. 267       426  BREAK_LOOP          436  'to 436'
            428_0  COME_FROM           422  '422'

 L. 269       428  LOAD_GLOBAL              OSError
              430  LOAD_STR                 'bad EPS header'
              432  CALL_FUNCTION_1       1  ''
              434  RAISE_VARARGS_1       1  'exception instance'
            436_0  COME_FROM           426  '426'
            436_1  COME_FROM           410  '410'
            436_2  COME_FROM           312  '312'
            436_3  COME_FROM           202  '202'
            436_4  COME_FROM            78  '78'

 L. 271       436  LOAD_FAST                'fp'
              438  LOAD_METHOD              readline
              440  CALL_METHOD_0         0  ''
              442  STORE_FAST               's_raw'

 L. 272       444  LOAD_FAST                's_raw'
              446  LOAD_METHOD              strip
              448  LOAD_STR                 '\r\n'
              450  CALL_METHOD_1         1  ''
              452  STORE_FAST               's'

 L. 274       454  LOAD_FAST                's'
              456  POP_JUMP_IF_FALSE    70  'to 70'
              458  LOAD_FAST                's'
              460  LOAD_CONST               None
              462  LOAD_CONST               1
              464  BUILD_SLICE_2         2 
              466  BINARY_SUBSCR    
              468  LOAD_STR                 '%'
              470  COMPARE_OP               !=
              472  POP_JUMP_IF_FALSE    70  'to 70'

 L. 275   474_476  BREAK_LOOP          480  'to 480'
              478  JUMP_BACK            70  'to 70'
            480_0  COME_FROM           680  '680'
            480_1  COME_FROM            72  '72'

 L. 280       480  LOAD_FAST                's'
              482  LOAD_CONST               None
              484  LOAD_CONST               1
              486  BUILD_SLICE_2         2 
              488  BINARY_SUBSCR    
              490  LOAD_STR                 '%'
              492  COMPARE_OP               ==
          494_496  POP_JUMP_IF_FALSE   692  'to 692'

 L. 282       498  LOAD_GLOBAL              len
              500  LOAD_FAST                's'
              502  CALL_FUNCTION_1       1  ''
              504  LOAD_CONST               255
              506  COMPARE_OP               >
          508_510  POP_JUMP_IF_FALSE   520  'to 520'

 L. 283       512  LOAD_GLOBAL              SyntaxError
              514  LOAD_STR                 'not an EPS file'
              516  CALL_FUNCTION_1       1  ''
              518  RAISE_VARARGS_1       1  'exception instance'
            520_0  COME_FROM           508  '508'

 L. 285       520  LOAD_FAST                's'
              522  LOAD_CONST               None
              524  LOAD_CONST               11
              526  BUILD_SLICE_2         2 
              528  BINARY_SUBSCR    
              530  LOAD_STR                 '%ImageData:'
              532  COMPARE_OP               ==
          534_536  POP_JUMP_IF_FALSE   664  'to 664'

 L. 287       538  LOAD_FAST                's'
              540  LOAD_CONST               11
              542  LOAD_CONST               None
              544  BUILD_SLICE_2         2 
              546  BINARY_SUBSCR    
              548  LOAD_METHOD              split
              550  LOAD_CONST               None
              552  LOAD_CONST               7
              554  CALL_METHOD_2         2  ''
              556  LOAD_CONST               None
              558  LOAD_CONST               4
              560  BUILD_SLICE_2         2 
              562  BINARY_SUBSCR    
              564  UNPACK_SEQUENCE_4     4 
              566  STORE_FAST               'x'
              568  STORE_FAST               'y'
              570  STORE_FAST               'bi'
              572  STORE_FAST               'mo'

 L. 289       574  LOAD_GLOBAL              int
              576  LOAD_FAST                'bi'
              578  CALL_FUNCTION_1       1  ''
              580  LOAD_CONST               8
              582  COMPARE_OP               !=
          584_586  POP_JUMP_IF_FALSE   592  'to 592'

 L. 290   588_590  BREAK_LOOP          692  'to 692'
            592_0  COME_FROM           584  '584'

 L. 291       592  SETUP_FINALLY       614  'to 614'

 L. 292       594  LOAD_FAST                'self'
              596  LOAD_ATTR                mode_map
              598  LOAD_GLOBAL              int
              600  LOAD_FAST                'mo'
              602  CALL_FUNCTION_1       1  ''
              604  BINARY_SUBSCR    
              606  LOAD_FAST                'self'
              608  STORE_ATTR               mode
              610  POP_BLOCK        
              612  JUMP_FORWARD        642  'to 642'
            614_0  COME_FROM_FINALLY   592  '592'

 L. 293       614  DUP_TOP          
              616  LOAD_GLOBAL              ValueError
              618  COMPARE_OP               exception-match
          620_622  POP_JUMP_IF_FALSE   640  'to 640'
              624  POP_TOP          
              626  POP_TOP          
              628  POP_TOP          

 L. 294       630  POP_EXCEPT       
          632_634  JUMP_ABSOLUTE       692  'to 692'
              636  POP_EXCEPT       
              638  JUMP_FORWARD        642  'to 642'
            640_0  COME_FROM           620  '620'
              640  END_FINALLY      
            642_0  COME_FROM           638  '638'
            642_1  COME_FROM           612  '612'

 L. 296       642  LOAD_GLOBAL              int
              644  LOAD_FAST                'x'
              646  CALL_FUNCTION_1       1  ''
              648  LOAD_GLOBAL              int
              650  LOAD_FAST                'y'
              652  CALL_FUNCTION_1       1  ''
              654  BUILD_TUPLE_2         2 
              656  LOAD_FAST                'self'
              658  STORE_ATTR               _size

 L. 297       660  LOAD_CONST               None
              662  RETURN_VALUE     
            664_0  COME_FROM           534  '534'

 L. 299       664  LOAD_FAST                'fp'
              666  LOAD_METHOD              readline
              668  CALL_METHOD_0         0  ''
              670  LOAD_METHOD              strip
              672  LOAD_STR                 '\r\n'
              674  CALL_METHOD_1         1  ''
              676  STORE_FAST               's'

 L. 300       678  LOAD_FAST                's'
          680_682  POP_JUMP_IF_TRUE    480  'to 480'

 L. 301   684_686  BREAK_LOOP          692  'to 692'
          688_690  JUMP_BACK           480  'to 480'
            692_0  COME_FROM           494  '494'

 L. 303       692  LOAD_FAST                'box'
          694_696  POP_JUMP_IF_TRUE    706  'to 706'

 L. 304       698  LOAD_GLOBAL              OSError
              700  LOAD_STR                 'cannot determine EPS bounding box'
              702  CALL_FUNCTION_1       1  ''
              704  RAISE_VARARGS_1       1  'exception instance'
            706_0  COME_FROM           694  '694'

Parse error at or near `POP_EXCEPT' instruction at offset 636

    def _find_offset(self, fp):
        s = fp.read(160)
        if s[:4] == b'%!PS':
            fp.seek(0, io.SEEK_END)
            length = fp.tell()
            offset = 0
        else:
            if i32(s, 0) == 3335770309:
                offset = i32(s, 4)
                length = i32(s, 8)
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
        fp.write(f"/buf {im.size[0] * operator[1]} string def\n")
        fp.write('%d %d scale\n' % im.size)
        fp.write('%d %d 8\n' % im.size)
        fp.write(f"[{im.size[0]} 0 0 -{im.size[1]} 0 {im.size[1]}]\n")
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