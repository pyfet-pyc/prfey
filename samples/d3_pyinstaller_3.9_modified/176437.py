# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\ImageGrab.py
import sys
from . import Image
if sys.platform == 'darwin':
    import os, subprocess, tempfile

def grab--- This code section failed: ---

 L.  29         0  LOAD_FAST                'xdisplay'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE   246  'to 246'

 L.  30         8  LOAD_GLOBAL              sys
               10  LOAD_ATTR                platform
               12  LOAD_STR                 'darwin'
               14  COMPARE_OP               ==
               16  POP_JUMP_IF_FALSE   116  'to 116'

 L.  31        18  LOAD_GLOBAL              tempfile
               20  LOAD_METHOD              mkstemp
               22  LOAD_STR                 '.png'
               24  CALL_METHOD_1         1  ''
               26  UNPACK_SEQUENCE_2     2 
               28  STORE_FAST               'fh'
               30  STORE_FAST               'filepath'

 L.  32        32  LOAD_GLOBAL              os
               34  LOAD_METHOD              close
               36  LOAD_FAST                'fh'
               38  CALL_METHOD_1         1  ''
               40  POP_TOP          

 L.  33        42  LOAD_GLOBAL              subprocess
               44  LOAD_METHOD              call
               46  LOAD_STR                 'screencapture'
               48  LOAD_STR                 '-x'
               50  LOAD_FAST                'filepath'
               52  BUILD_LIST_3          3 
               54  CALL_METHOD_1         1  ''
               56  POP_TOP          

 L.  34        58  LOAD_GLOBAL              Image
               60  LOAD_METHOD              open
               62  LOAD_FAST                'filepath'
               64  CALL_METHOD_1         1  ''
               66  STORE_FAST               'im'

 L.  35        68  LOAD_FAST                'im'
               70  LOAD_METHOD              load
               72  CALL_METHOD_0         0  ''
               74  POP_TOP          

 L.  36        76  LOAD_GLOBAL              os
               78  LOAD_METHOD              unlink
               80  LOAD_FAST                'filepath'
               82  CALL_METHOD_1         1  ''
               84  POP_TOP          

 L.  37        86  LOAD_FAST                'bbox'
               88  POP_JUMP_IF_FALSE   112  'to 112'

 L.  38        90  LOAD_FAST                'im'
               92  LOAD_METHOD              crop
               94  LOAD_FAST                'bbox'
               96  CALL_METHOD_1         1  ''
               98  STORE_FAST               'im_cropped'

 L.  39       100  LOAD_FAST                'im'
              102  LOAD_METHOD              close
              104  CALL_METHOD_0         0  ''
              106  POP_TOP          

 L.  40       108  LOAD_FAST                'im_cropped'
              110  RETURN_VALUE     
            112_0  COME_FROM            88  '88'

 L.  41       112  LOAD_FAST                'im'
              114  RETURN_VALUE     
            116_0  COME_FROM            16  '16'

 L.  42       116  LOAD_GLOBAL              sys
              118  LOAD_ATTR                platform
              120  LOAD_STR                 'win32'
              122  COMPARE_OP               ==
              124  POP_JUMP_IF_FALSE   246  'to 246'

 L.  43       126  LOAD_GLOBAL              Image
              128  LOAD_ATTR                core
              130  LOAD_METHOD              grabscreen_win32

 L.  44       132  LOAD_FAST                'include_layered_windows'
              134  LOAD_FAST                'all_screens'

 L.  43       136  CALL_METHOD_2         2  ''
              138  UNPACK_SEQUENCE_3     3 
              140  STORE_FAST               'offset'
              142  STORE_FAST               'size'
              144  STORE_FAST               'data'

 L.  46       146  LOAD_GLOBAL              Image
              148  LOAD_METHOD              frombytes

 L.  47       150  LOAD_STR                 'RGB'

 L.  48       152  LOAD_FAST                'size'

 L.  49       154  LOAD_FAST                'data'

 L.  51       156  LOAD_STR                 'raw'

 L.  52       158  LOAD_STR                 'BGR'

 L.  53       160  LOAD_FAST                'size'
              162  LOAD_CONST               0
              164  BINARY_SUBSCR    
              166  LOAD_CONST               3
              168  BINARY_MULTIPLY  
              170  LOAD_CONST               3
              172  BINARY_ADD       
              174  LOAD_CONST               -4
              176  BINARY_AND       

 L.  54       178  LOAD_CONST               -1

 L.  46       180  CALL_METHOD_7         7  ''
              182  STORE_FAST               'im'

 L.  56       184  LOAD_FAST                'bbox'
              186  POP_JUMP_IF_FALSE   242  'to 242'

 L.  57       188  LOAD_FAST                'offset'
              190  UNPACK_SEQUENCE_2     2 
              192  STORE_FAST               'x0'
              194  STORE_FAST               'y0'

 L.  58       196  LOAD_FAST                'bbox'
              198  UNPACK_SEQUENCE_4     4 
              200  STORE_FAST               'left'
              202  STORE_FAST               'top'
              204  STORE_FAST               'right'
              206  STORE_FAST               'bottom'

 L.  59       208  LOAD_FAST                'im'
              210  LOAD_METHOD              crop
              212  LOAD_FAST                'left'
              214  LOAD_FAST                'x0'
              216  BINARY_SUBTRACT  
              218  LOAD_FAST                'top'
              220  LOAD_FAST                'y0'
              222  BINARY_SUBTRACT  
              224  LOAD_FAST                'right'
              226  LOAD_FAST                'x0'
              228  BINARY_SUBTRACT  
              230  LOAD_FAST                'bottom'
              232  LOAD_FAST                'y0'
              234  BINARY_SUBTRACT  
              236  BUILD_TUPLE_4         4 
              238  CALL_METHOD_1         1  ''
              240  STORE_FAST               'im'
            242_0  COME_FROM           186  '186'

 L.  60       242  LOAD_FAST                'im'
              244  RETURN_VALUE     
            246_0  COME_FROM           124  '124'
            246_1  COME_FROM             6  '6'

 L.  62       246  LOAD_GLOBAL              Image
              248  LOAD_ATTR                core
              250  LOAD_ATTR                HAVE_XCB
          252_254  POP_JUMP_IF_TRUE    264  'to 264'

 L.  63       256  LOAD_GLOBAL              OSError
              258  LOAD_STR                 'Pillow was built without XCB support'
              260  CALL_FUNCTION_1       1  ''
              262  RAISE_VARARGS_1       1  'exception instance'
            264_0  COME_FROM           252  '252'

 L.  64       264  LOAD_GLOBAL              Image
              266  LOAD_ATTR                core
              268  LOAD_METHOD              grabscreen_x11
              270  LOAD_FAST                'xdisplay'
              272  CALL_METHOD_1         1  ''
              274  UNPACK_SEQUENCE_2     2 
              276  STORE_FAST               'size'
              278  STORE_FAST               'data'

 L.  65       280  LOAD_GLOBAL              Image
              282  LOAD_METHOD              frombytes
              284  LOAD_STR                 'RGB'
              286  LOAD_FAST                'size'
              288  LOAD_FAST                'data'
              290  LOAD_STR                 'raw'
              292  LOAD_STR                 'BGRX'
              294  LOAD_FAST                'size'
              296  LOAD_CONST               0
              298  BINARY_SUBSCR    
              300  LOAD_CONST               4
              302  BINARY_MULTIPLY  
              304  LOAD_CONST               1
              306  CALL_METHOD_7         7  ''
              308  STORE_FAST               'im'

 L.  66       310  LOAD_FAST                'bbox'
          312_314  POP_JUMP_IF_FALSE   326  'to 326'

 L.  67       316  LOAD_FAST                'im'
              318  LOAD_METHOD              crop
              320  LOAD_FAST                'bbox'
              322  CALL_METHOD_1         1  ''
              324  STORE_FAST               'im'
            326_0  COME_FROM           312  '312'

 L.  68       326  LOAD_FAST                'im'
              328  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def grabclipboard():
    if sys.platform == 'darwin':
        fh, filepath = tempfile.mkstemp'.jpg'
        os.closefh
        commands = [
         'set theFile to (open for access POSIX file "' + filepath + '" with write permission)',
         'try',
         '    write (the clipboard as JPEG picture) to theFile',
         'end try',
         'close access theFile']
        script = [
         'osascript']
        for command in commands:
            script += ['-e', command]
        else:
            subprocess.callscript
            im = None
            if os.statfilepath.st_size != 0:
                im = Image.openfilepath
                im.load
            os.unlinkfilepath
            return im

    if sys.platform == 'win32':
        fmt, data = Image.core.grabclipboard_win32
        if fmt == 'file':
            import struct
            o = struct.unpack_from'I'data[0]
            if data[16] != 0:
                files = data[o:].decode'utf-16le'.split'\x00'
            else:
                files = data[o:].decode'mbcs'.split'\x00'
            return files[:files.index'']
        if isinstance(data, bytes):
            import io
            data = io.BytesIOdata
            if fmt == 'png':
                from . import PngImagePlugin
                return PngImagePlugin.PngImageFiledata
            if fmt == 'DIB':
                from . import BmpImagePlugin
                return BmpImagePlugin.DibImageFiledata
        return
    raise NotImplementedError('ImageGrab.grabclipboard() is macOS and Windows only')