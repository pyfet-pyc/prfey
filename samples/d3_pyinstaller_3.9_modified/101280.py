# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: PIL\FtexImagePlugin.py
"""
A Pillow loader for .ftc and .ftu files (FTEX)
Jerome Leclanche <jerome@leclan.ch>

The contents of this file are hereby released in the public domain (CC0)
Full text of the CC0 license:
  https://creativecommons.org/publicdomain/zero/1.0/

Independence War 2: Edge Of Chaos - Texture File Format - 16 October 2001

The textures used for 3D objects in Independence War 2: Edge Of Chaos are in a
packed custom format called FTEX. This file format uses file extensions FTC
and FTU.
* FTC files are compressed textures (using standard texture compression).
* FTU files are not compressed.
Texture File Format
The FTC and FTU texture files both use the same format. This
has the following structure:
{header}
{format_directory}
{data}
Where:
{header} = {
    u32:magic,
    u32:version,
    u32:width,
    u32:height,
    u32:mipmap_count,
    u32:format_count
}

* The "magic" number is "FTEX".
* "width" and "height" are the dimensions of the texture.
* "mipmap_count" is the number of mipmaps in the texture.
* "format_count" is the number of texture formats (different versions of the
same texture) in this file.

{format_directory} = format_count * { u32:format, u32:where }

The format value is 0 for DXT1 compressed textures and 1 for 24-bit RGB
uncompressed textures.
The texture data for a format starts at the position "where" in the file.

Each set of texture data in the file has the following structure:
{data} = format_count * { u32:mipmap_size, mipmap_size * { u8 } }
* "mipmap_size" is the number of bytes in that mip level. For compressed
textures this is the size of the texture data compressed with DXT1. For 24 bit
uncompressed textures, this is 3 * width * height. Following this are the image
bytes for that mipmap level.

Note: All data is stored in little-Endian (Intel) byte order.
"""
import struct
from io import BytesIO
from . import Image, ImageFile
MAGIC = b'FTEX'
FORMAT_DXT1 = 0
FORMAT_UNCOMPRESSED = 1

class FtexImageFile(ImageFile.ImageFile):
    format = 'FTEX'
    format_description = 'Texture File Format (IW2:EOC)'

    def _open--- This code section failed: ---

 L.  69         0  LOAD_GLOBAL              struct
                2  LOAD_METHOD              unpack
                4  LOAD_STR                 '<I'
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                fp
               10  LOAD_METHOD              read
               12  LOAD_CONST               4
               14  CALL_METHOD_1         1  ''
               16  CALL_METHOD_2         2  ''
               18  POP_TOP          

 L.  70        20  LOAD_GLOBAL              struct
               22  LOAD_METHOD              unpack
               24  LOAD_STR                 '<i'
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                fp
               30  LOAD_METHOD              read
               32  LOAD_CONST               4
               34  CALL_METHOD_1         1  ''
               36  CALL_METHOD_2         2  ''
               38  POP_TOP          

 L.  71        40  LOAD_GLOBAL              struct
               42  LOAD_METHOD              unpack
               44  LOAD_STR                 '<2i'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                fp
               50  LOAD_METHOD              read
               52  LOAD_CONST               8
               54  CALL_METHOD_1         1  ''
               56  CALL_METHOD_2         2  ''
               58  LOAD_FAST                'self'
               60  STORE_ATTR               _size

 L.  72        62  LOAD_GLOBAL              struct
               64  LOAD_METHOD              unpack
               66  LOAD_STR                 '<2i'
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                fp
               72  LOAD_METHOD              read
               74  LOAD_CONST               8
               76  CALL_METHOD_1         1  ''
               78  CALL_METHOD_2         2  ''
               80  UNPACK_SEQUENCE_2     2 
               82  STORE_FAST               'mipmap_count'
               84  STORE_FAST               'format_count'

 L.  74        86  LOAD_STR                 'RGB'
               88  LOAD_FAST                'self'
               90  STORE_ATTR               mode

 L.  78        92  LOAD_FAST                'format_count'
               94  LOAD_CONST               1
               96  COMPARE_OP               ==
               98  POP_JUMP_IF_TRUE    104  'to 104'
              100  <74>             
              102  RAISE_VARARGS_1       1  'exception instance'
            104_0  COME_FROM            98  '98'

 L.  80       104  LOAD_GLOBAL              struct
              106  LOAD_METHOD              unpack
              108  LOAD_STR                 '<2i'
              110  LOAD_FAST                'self'
              112  LOAD_ATTR                fp
              114  LOAD_METHOD              read
              116  LOAD_CONST               8
              118  CALL_METHOD_1         1  ''
              120  CALL_METHOD_2         2  ''
              122  UNPACK_SEQUENCE_2     2 
              124  STORE_FAST               'format'
              126  STORE_FAST               'where'

 L.  81       128  LOAD_FAST                'self'
              130  LOAD_ATTR                fp
              132  LOAD_METHOD              seek
              134  LOAD_FAST                'where'
              136  CALL_METHOD_1         1  ''
              138  POP_TOP          

 L.  82       140  LOAD_GLOBAL              struct
              142  LOAD_METHOD              unpack
              144  LOAD_STR                 '<i'
              146  LOAD_FAST                'self'
              148  LOAD_ATTR                fp
              150  LOAD_METHOD              read
              152  LOAD_CONST               4
              154  CALL_METHOD_1         1  ''
              156  CALL_METHOD_2         2  ''
              158  UNPACK_SEQUENCE_1     1 
              160  STORE_FAST               'mipmap_size'

 L.  84       162  LOAD_FAST                'self'
              164  LOAD_ATTR                fp
              166  LOAD_METHOD              read
              168  LOAD_FAST                'mipmap_size'
              170  CALL_METHOD_1         1  ''
              172  STORE_FAST               'data'

 L.  86       174  LOAD_FAST                'format'
              176  LOAD_GLOBAL              FORMAT_DXT1
              178  COMPARE_OP               ==
              180  POP_JUMP_IF_FALSE   212  'to 212'

 L.  87       182  LOAD_STR                 'RGBA'
              184  LOAD_FAST                'self'
              186  STORE_ATTR               mode

 L.  88       188  LOAD_STR                 'bcn'
              190  LOAD_CONST               (0, 0)
              192  LOAD_FAST                'self'
              194  LOAD_ATTR                size
              196  BINARY_ADD       
              198  LOAD_CONST               0
              200  LOAD_CONST               1
              202  BUILD_TUPLE_4         4 
              204  BUILD_LIST_1          1 
              206  LOAD_FAST                'self'
              208  STORE_ATTR               tile
              210  JUMP_FORWARD        262  'to 262'
            212_0  COME_FROM           180  '180'

 L.  89       212  LOAD_FAST                'format'
              214  LOAD_GLOBAL              FORMAT_UNCOMPRESSED
              216  COMPARE_OP               ==
              218  POP_JUMP_IF_FALSE   244  'to 244'

 L.  90       220  LOAD_STR                 'raw'
              222  LOAD_CONST               (0, 0)
              224  LOAD_FAST                'self'
              226  LOAD_ATTR                size
              228  BINARY_ADD       
              230  LOAD_CONST               0
              232  LOAD_CONST               ('RGB', 0, 1)
              234  BUILD_TUPLE_4         4 
              236  BUILD_LIST_1          1 
              238  LOAD_FAST                'self'
              240  STORE_ATTR               tile
              242  JUMP_FORWARD        262  'to 262'
            244_0  COME_FROM           218  '218'

 L.  92       244  LOAD_GLOBAL              ValueError
              246  LOAD_STR                 'Invalid texture compression format: '
              248  LOAD_GLOBAL              repr
              250  LOAD_FAST                'format'
              252  CALL_FUNCTION_1       1  ''
              254  FORMAT_VALUE          0  ''
              256  BUILD_STRING_2        2 
              258  CALL_FUNCTION_1       1  ''
              260  RAISE_VARARGS_1       1  'exception instance'
            262_0  COME_FROM           242  '242'
            262_1  COME_FROM           210  '210'

 L.  94       262  LOAD_FAST                'self'
              264  LOAD_ATTR                fp
              266  LOAD_METHOD              close
              268  CALL_METHOD_0         0  ''
              270  POP_TOP          

 L.  95       272  LOAD_GLOBAL              BytesIO
              274  LOAD_FAST                'data'
              276  CALL_FUNCTION_1       1  ''
              278  LOAD_FAST                'self'
              280  STORE_ATTR               fp

Parse error at or near `<74>' instruction at offset 100

    def load_seek(self, pos):
        pass


def _validate(prefix):
    return prefix[:4] == MAGIC


Image.register_open(FtexImageFile.format, FtexImageFile, _validate)
Image.register_extensions(FtexImageFile.format, ['.ftc', '.ftu'])