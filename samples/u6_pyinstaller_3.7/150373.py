# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
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

def has_ghostscript():
    if gs_windows_binary:
        return True
    if not sys.platform.startswith('win'):
        try:
            subprocess.check_call(['gs', '--version'], stdout=(subprocess.DEVNULL))
            return True
        except OSError:
            pass

    return False


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
                8  CALL_METHOD_1         1  '1 positional argument'
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'length'
               14  STORE_FAST               'offset'

 L. 211        16  LOAD_GLOBAL              PSFile
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                fp
               22  CALL_FUNCTION_1       1  '1 positional argument'
               24  STORE_FAST               'fp'

 L. 214        26  LOAD_FAST                'fp'
               28  LOAD_METHOD              seek
               30  LOAD_FAST                'offset'
               32  CALL_METHOD_1         1  '1 positional argument'
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
               56  CALL_METHOD_0         0  '0 positional arguments'
               58  STORE_FAST               's_raw'

 L. 225        60  LOAD_FAST                's_raw'
               62  LOAD_METHOD              strip
               64  LOAD_STR                 '\r\n'
               66  CALL_METHOD_1         1  '1 positional argument'
               68  STORE_FAST               's'

 L. 227     70_72  SETUP_LOOP          482  'to 482'
             74_0  COME_FROM           474  '474'
             74_1  COME_FROM           458  '458'
               74  LOAD_FAST                's_raw'
            76_78  POP_JUMP_IF_FALSE   480  'to 480'

 L. 228        80  LOAD_FAST                's'
            82_84  POP_JUMP_IF_FALSE   438  'to 438'

 L. 229        86  LOAD_GLOBAL              len
               88  LOAD_FAST                's'
               90  CALL_FUNCTION_1       1  '1 positional argument'
               92  LOAD_CONST               255
               94  COMPARE_OP               >
               96  POP_JUMP_IF_FALSE   106  'to 106'

 L. 230        98  LOAD_GLOBAL              SyntaxError
              100  LOAD_STR                 'not an EPS file'
              102  CALL_FUNCTION_1       1  '1 positional argument'
              104  RAISE_VARARGS_1       1  'exception instance'
            106_0  COME_FROM            96  '96'

 L. 232       106  SETUP_EXCEPT        122  'to 122'

 L. 233       108  LOAD_GLOBAL              split
              110  LOAD_METHOD              match
              112  LOAD_FAST                's'
              114  CALL_METHOD_1         1  '1 positional argument'
              116  STORE_FAST               'm'
              118  POP_BLOCK        
              120  JUMP_FORWARD        168  'to 168'
            122_0  COME_FROM_EXCEPT    106  '106'

 L. 234       122  DUP_TOP          
              124  LOAD_GLOBAL              re
              126  LOAD_ATTR                error
              128  COMPARE_OP               exception-match
              130  POP_JUMP_IF_FALSE   166  'to 166'
              132  POP_TOP          
              134  STORE_FAST               'e'
              136  POP_TOP          
              138  SETUP_FINALLY       154  'to 154'

 L. 235       140  LOAD_GLOBAL              SyntaxError
              142  LOAD_STR                 'not an EPS file'
              144  CALL_FUNCTION_1       1  '1 positional argument'
              146  LOAD_FAST                'e'
              148  RAISE_VARARGS_2       2  'exception instance with __cause__'
              150  POP_BLOCK        
              152  LOAD_CONST               None
            154_0  COME_FROM_FINALLY   138  '138'
              154  LOAD_CONST               None
              156  STORE_FAST               'e'
              158  DELETE_FAST              'e'
              160  END_FINALLY      
              162  POP_EXCEPT       
              164  JUMP_FORWARD        168  'to 168'
            166_0  COME_FROM           130  '130'
              166  END_FINALLY      
            168_0  COME_FROM           164  '164'
            168_1  COME_FROM           120  '120'

 L. 237       168  LOAD_FAST                'm'
          170_172  POP_JUMP_IF_FALSE   318  'to 318'

 L. 238       174  LOAD_FAST                'm'
              176  LOAD_METHOD              group
              178  LOAD_CONST               1
              180  LOAD_CONST               2
              182  CALL_METHOD_2         2  '2 positional arguments'
              184  UNPACK_SEQUENCE_2     2 
              186  STORE_FAST               'k'
              188  STORE_FAST               'v'

 L. 239       190  LOAD_FAST                'v'
              192  LOAD_FAST                'self'
              194  LOAD_ATTR                info
              196  LOAD_FAST                'k'
              198  STORE_SUBSCR     

 L. 240       200  LOAD_FAST                'k'
              202  LOAD_STR                 'BoundingBox'
              204  COMPARE_OP               ==
          206_208  POP_JUMP_IF_FALSE   438  'to 438'

 L. 241       210  SETUP_EXCEPT        294  'to 294'

 L. 245       212  LOAD_LISTCOMP            '<code_object <listcomp>>'
              214  LOAD_STR                 'EpsImageFile._open.<locals>.<listcomp>'
              216  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              218  LOAD_FAST                'v'
              220  LOAD_METHOD              split
              222  CALL_METHOD_0         0  '0 positional arguments'
              224  GET_ITER         
              226  CALL_FUNCTION_1       1  '1 positional argument'
              228  STORE_FAST               'box'

 L. 246       230  LOAD_FAST                'box'
              232  LOAD_CONST               2
              234  BINARY_SUBSCR    
              236  LOAD_FAST                'box'
              238  LOAD_CONST               0
              240  BINARY_SUBSCR    
              242  BINARY_SUBTRACT  
              244  LOAD_FAST                'box'
              246  LOAD_CONST               3
              248  BINARY_SUBSCR    
              250  LOAD_FAST                'box'
              252  LOAD_CONST               1
              254  BINARY_SUBSCR    
              256  BINARY_SUBTRACT  
              258  BUILD_TUPLE_2         2 
              260  LOAD_FAST                'self'
              262  STORE_ATTR               _size

 L. 248       264  LOAD_STR                 'eps'
              266  LOAD_CONST               (0, 0)
              268  LOAD_FAST                'self'
              270  LOAD_ATTR                size
              272  BINARY_ADD       
              274  LOAD_FAST                'offset'
              276  LOAD_FAST                'length'
              278  LOAD_FAST                'box'
              280  BUILD_TUPLE_2         2 
              282  BUILD_TUPLE_4         4 
              284  BUILD_LIST_1          1 
              286  LOAD_FAST                'self'
              288  STORE_ATTR               tile
              290  POP_BLOCK        
              292  JUMP_FORWARD        316  'to 316'
            294_0  COME_FROM_EXCEPT    210  '210'

 L. 250       294  DUP_TOP          
              296  LOAD_GLOBAL              Exception
              298  COMPARE_OP               exception-match
          300_302  POP_JUMP_IF_FALSE   314  'to 314'
              304  POP_TOP          
              306  POP_TOP          
              308  POP_TOP          

 L. 251       310  POP_EXCEPT       
              312  JUMP_FORWARD        316  'to 316'
            314_0  COME_FROM           300  '300'
              314  END_FINALLY      
            316_0  COME_FROM           312  '312'
            316_1  COME_FROM           292  '292'
              316  JUMP_FORWARD        438  'to 438'
            318_0  COME_FROM           170  '170'

 L. 254       318  LOAD_GLOBAL              field
              320  LOAD_METHOD              match
              322  LOAD_FAST                's'
              324  CALL_METHOD_1         1  '1 positional argument'
              326  STORE_FAST               'm'

 L. 255       328  LOAD_FAST                'm'
          330_332  POP_JUMP_IF_FALSE   414  'to 414'

 L. 256       334  LOAD_FAST                'm'
              336  LOAD_METHOD              group
              338  LOAD_CONST               1
              340  CALL_METHOD_1         1  '1 positional argument'
              342  STORE_FAST               'k'

 L. 258       344  LOAD_FAST                'k'
              346  LOAD_STR                 'EndComments'
              348  COMPARE_OP               ==
          350_352  POP_JUMP_IF_FALSE   356  'to 356'

 L. 259       354  BREAK_LOOP       
            356_0  COME_FROM           350  '350'

 L. 260       356  LOAD_FAST                'k'
              358  LOAD_CONST               None
              360  LOAD_CONST               8
              362  BUILD_SLICE_2         2 
              364  BINARY_SUBSCR    
              366  LOAD_STR                 'PS-Adobe'
              368  COMPARE_OP               ==
          370_372  POP_JUMP_IF_FALSE   402  'to 402'

 L. 261       374  LOAD_FAST                'k'
              376  LOAD_CONST               9
              378  LOAD_CONST               None
              380  BUILD_SLICE_2         2 
              382  BINARY_SUBSCR    
              384  LOAD_FAST                'self'
              386  LOAD_ATTR                info
              388  LOAD_FAST                'k'
              390  LOAD_CONST               None
              392  LOAD_CONST               8
              394  BUILD_SLICE_2         2 
              396  BINARY_SUBSCR    
              398  STORE_SUBSCR     
              400  JUMP_FORWARD        412  'to 412'
            402_0  COME_FROM           370  '370'

 L. 263       402  LOAD_STR                 ''
              404  LOAD_FAST                'self'
              406  LOAD_ATTR                info
              408  LOAD_FAST                'k'
              410  STORE_SUBSCR     
            412_0  COME_FROM           400  '400'
              412  JUMP_FORWARD        438  'to 438'
            414_0  COME_FROM           330  '330'

 L. 264       414  LOAD_FAST                's'
              416  LOAD_CONST               0
              418  BINARY_SUBSCR    
              420  LOAD_STR                 '%'
              422  COMPARE_OP               ==
          424_426  POP_JUMP_IF_FALSE   430  'to 430'

 L. 267       428  JUMP_FORWARD        438  'to 438'
            430_0  COME_FROM           424  '424'

 L. 269       430  LOAD_GLOBAL              OSError
              432  LOAD_STR                 'bad EPS header'
              434  CALL_FUNCTION_1       1  '1 positional argument'
              436  RAISE_VARARGS_1       1  'exception instance'
            438_0  COME_FROM           428  '428'
            438_1  COME_FROM           412  '412'
            438_2  COME_FROM           316  '316'
            438_3  COME_FROM           206  '206'
            438_4  COME_FROM            82  '82'

 L. 271       438  LOAD_FAST                'fp'
              440  LOAD_METHOD              readline
              442  CALL_METHOD_0         0  '0 positional arguments'
              444  STORE_FAST               's_raw'

 L. 272       446  LOAD_FAST                's_raw'
              448  LOAD_METHOD              strip
              450  LOAD_STR                 '\r\n'
              452  CALL_METHOD_1         1  '1 positional argument'
              454  STORE_FAST               's'

 L. 274       456  LOAD_FAST                's'
              458  POP_JUMP_IF_FALSE    74  'to 74'
              460  LOAD_FAST                's'
              462  LOAD_CONST               None
              464  LOAD_CONST               1
              466  BUILD_SLICE_2         2 
              468  BINARY_SUBSCR    
              470  LOAD_STR                 '%'
              472  COMPARE_OP               !=
              474  POP_JUMP_IF_FALSE    74  'to 74'

 L. 275       476  BREAK_LOOP       
              478  JUMP_BACK            74  'to 74'
            480_0  COME_FROM            76  '76'
              480  POP_BLOCK        
            482_0  COME_FROM_LOOP       70  '70'

 L. 280       482  SETUP_LOOP          690  'to 690'
            484_0  COME_FROM           678  '678'
              484  LOAD_FAST                's'
              486  LOAD_CONST               None
              488  LOAD_CONST               1
              490  BUILD_SLICE_2         2 
              492  BINARY_SUBSCR    
              494  LOAD_STR                 '%'
              496  COMPARE_OP               ==
          498_500  POP_JUMP_IF_FALSE   688  'to 688'

 L. 282       502  LOAD_GLOBAL              len
              504  LOAD_FAST                's'
              506  CALL_FUNCTION_1       1  '1 positional argument'
              508  LOAD_CONST               255
              510  COMPARE_OP               >
          512_514  POP_JUMP_IF_FALSE   524  'to 524'

 L. 283       516  LOAD_GLOBAL              SyntaxError
              518  LOAD_STR                 'not an EPS file'
              520  CALL_FUNCTION_1       1  '1 positional argument'
              522  RAISE_VARARGS_1       1  'exception instance'
            524_0  COME_FROM           512  '512'

 L. 285       524  LOAD_FAST                's'
              526  LOAD_CONST               None
              528  LOAD_CONST               11
              530  BUILD_SLICE_2         2 
              532  BINARY_SUBSCR    
              534  LOAD_STR                 '%ImageData:'
              536  COMPARE_OP               ==
          538_540  POP_JUMP_IF_FALSE   662  'to 662'

 L. 287       542  LOAD_FAST                's'
              544  LOAD_CONST               11
              546  LOAD_CONST               None
              548  BUILD_SLICE_2         2 
              550  BINARY_SUBSCR    
              552  LOAD_METHOD              split
              554  LOAD_CONST               None
              556  LOAD_CONST               7
              558  CALL_METHOD_2         2  '2 positional arguments'
              560  LOAD_CONST               None
              562  LOAD_CONST               4
              564  BUILD_SLICE_2         2 
              566  BINARY_SUBSCR    
              568  UNPACK_SEQUENCE_4     4 
              570  STORE_FAST               'x'
              572  STORE_FAST               'y'
              574  STORE_FAST               'bi'
              576  STORE_FAST               'mo'

 L. 289       578  LOAD_GLOBAL              int
              580  LOAD_FAST                'bi'
              582  CALL_FUNCTION_1       1  '1 positional argument'
              584  LOAD_CONST               8
              586  COMPARE_OP               !=
          588_590  POP_JUMP_IF_FALSE   594  'to 594'

 L. 290       592  BREAK_LOOP       
            594_0  COME_FROM           588  '588'

 L. 291       594  SETUP_EXCEPT        616  'to 616'

 L. 292       596  LOAD_FAST                'self'
              598  LOAD_ATTR                mode_map
              600  LOAD_GLOBAL              int
              602  LOAD_FAST                'mo'
              604  CALL_FUNCTION_1       1  '1 positional argument'
              606  BINARY_SUBSCR    
              608  LOAD_FAST                'self'
              610  STORE_ATTR               mode
              612  POP_BLOCK        
              614  JUMP_FORWARD        640  'to 640'
            616_0  COME_FROM_EXCEPT    594  '594'

 L. 293       616  DUP_TOP          
              618  LOAD_GLOBAL              ValueError
              620  COMPARE_OP               exception-match
          622_624  POP_JUMP_IF_FALSE   638  'to 638'
              626  POP_TOP          
              628  POP_TOP          
              630  POP_TOP          

 L. 294       632  BREAK_LOOP       
              634  POP_EXCEPT       
              636  JUMP_FORWARD        640  'to 640'
            638_0  COME_FROM           622  '622'
              638  END_FINALLY      
            640_0  COME_FROM           636  '636'
            640_1  COME_FROM           614  '614'

 L. 296       640  LOAD_GLOBAL              int
              642  LOAD_FAST                'x'
              644  CALL_FUNCTION_1       1  '1 positional argument'
              646  LOAD_GLOBAL              int
              648  LOAD_FAST                'y'
              650  CALL_FUNCTION_1       1  '1 positional argument'
              652  BUILD_TUPLE_2         2 
              654  LOAD_FAST                'self'
              656  STORE_ATTR               _size

 L. 297       658  LOAD_CONST               None
              660  RETURN_VALUE     
            662_0  COME_FROM           538  '538'

 L. 299       662  LOAD_FAST                'fp'
              664  LOAD_METHOD              readline
              666  CALL_METHOD_0         0  '0 positional arguments'
              668  LOAD_METHOD              strip
              670  LOAD_STR                 '\r\n'
              672  CALL_METHOD_1         1  '1 positional argument'
              674  STORE_FAST               's'

 L. 300       676  LOAD_FAST                's'
          678_680  POP_JUMP_IF_TRUE    484  'to 484'

 L. 301       682  BREAK_LOOP       
          684_686  JUMP_BACK           484  'to 484'
            688_0  COME_FROM           498  '498'
              688  POP_BLOCK        
            690_0  COME_FROM_LOOP      482  '482'

 L. 303       690  LOAD_FAST                'box'
          692_694  POP_JUMP_IF_TRUE    704  'to 704'

 L. 304       696  LOAD_GLOBAL              OSError
              698  LOAD_STR                 'cannot determine EPS bounding box'
              700  CALL_FUNCTION_1       1  '1 positional argument'
              702  RAISE_VARARGS_1       1  'exception instance'
            704_0  COME_FROM           692  '692'

Parse error at or near `POP_BLOCK' instruction at offset 688

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