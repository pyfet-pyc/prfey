# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: setuptools\dist.py
__all__ = ['Distribution']
import io, sys, re, os, warnings, numbers, distutils.log, distutils.core, distutils.cmd, distutils.dist, distutils.command
from distutils.util import strtobool
from distutils.debug import DEBUG
from distutils.fancy_getopt import translate_longopt
import itertools, textwrap
from typing import List, Optional, TYPE_CHECKING
from collections import defaultdict
from email import message_from_file
from distutils.errors import DistutilsOptionError, DistutilsSetupError
from distutils.util import rfc822_escape
from distutils.version import StrictVersion
from setuptools.extern import packaging
from setuptools.extern import ordered_set
from . import SetuptoolsDeprecationWarning
import setuptools, setuptools.command
from setuptools import windows_support
from setuptools.monkey import get_unpatched
from setuptools.config import parse_configuration
import pkg_resources
if TYPE_CHECKING:
    from email.message import Message
__import__('setuptools.extern.packaging.specifiers')
__import__('setuptools.extern.packaging.version')

def _get_unpatched(cls):
    warnings.warn('Do not call this function', DistDeprecationWarning)
    return get_unpatched(cls)


def get_metadata_version--- This code section failed: ---

 L.  54         0  LOAD_GLOBAL              getattr
                2  LOAD_FAST                'self'
                4  LOAD_STR                 'metadata_version'
                6  LOAD_CONST               None
                8  CALL_FUNCTION_3       3  ''
               10  STORE_FAST               'mv'

 L.  55        12  LOAD_FAST                'mv'
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    34  'to 34'

 L.  56        20  LOAD_GLOBAL              StrictVersion
               22  LOAD_STR                 '2.1'
               24  CALL_FUNCTION_1       1  ''
               26  STORE_FAST               'mv'

 L.  57        28  LOAD_FAST                'mv'
               30  LOAD_FAST                'self'
               32  STORE_ATTR               metadata_version
             34_0  COME_FROM            18  '18'

 L.  58        34  LOAD_FAST                'mv'
               36  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 16


def rfc822_unescape(content: str) -> str:
    """Reverse RFC-822 escaping by removing leading whitespaces from content."""
    lines = content.splitlines()
    if len(lines) == 1:
        return lines[0].lstrip()
    return '\n'.join((
     lines[0].lstrip(),
     textwrap.dedent('\n'.join(lines[1:]))))


def _read_field_from_msg(msg: 'Message', field: str) -> Optional[str]:
    """Read Message header field."""
    value = msg[field]
    if value == 'UNKNOWN':
        return
    return value


def _read_field_unescaped_from_msg--- This code section failed: ---

 L.  81         0  LOAD_GLOBAL              _read_field_from_msg
                2  LOAD_FAST                'msg'
                4  LOAD_FAST                'field'
                6  CALL_FUNCTION_2       2  ''
                8  STORE_FAST               'value'

 L.  82        10  LOAD_FAST                'value'
               12  LOAD_CONST               None
               14  <117>                 0  ''
               16  POP_JUMP_IF_FALSE    22  'to 22'

 L.  83        18  LOAD_FAST                'value'
               20  RETURN_VALUE     
             22_0  COME_FROM            16  '16'

 L.  84        22  LOAD_GLOBAL              rfc822_unescape
               24  LOAD_FAST                'value'
               26  CALL_FUNCTION_1       1  ''
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 14


def _read_list_from_msg(msg: 'Message', field: str) -> Optional[List[str]]:
    """Read Message header field and return all results as list."""
    values = msg.get_all(field, None)
    if values == []:
        return
    return values


def read_pkg_file--- This code section failed: ---

 L.  97         0  LOAD_GLOBAL              message_from_file
                2  LOAD_FAST                'file'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'msg'

 L.  99         8  LOAD_GLOBAL              StrictVersion
               10  LOAD_FAST                'msg'
               12  LOAD_STR                 'metadata-version'
               14  BINARY_SUBSCR    
               16  CALL_FUNCTION_1       1  ''
               18  LOAD_FAST                'self'
               20  STORE_ATTR               metadata_version

 L. 100        22  LOAD_GLOBAL              _read_field_from_msg
               24  LOAD_FAST                'msg'
               26  LOAD_STR                 'name'
               28  CALL_FUNCTION_2       2  ''
               30  LOAD_FAST                'self'
               32  STORE_ATTR               name

 L. 101        34  LOAD_GLOBAL              _read_field_from_msg
               36  LOAD_FAST                'msg'
               38  LOAD_STR                 'version'
               40  CALL_FUNCTION_2       2  ''
               42  LOAD_FAST                'self'
               44  STORE_ATTR               version

 L. 102        46  LOAD_GLOBAL              _read_field_from_msg
               48  LOAD_FAST                'msg'
               50  LOAD_STR                 'summary'
               52  CALL_FUNCTION_2       2  ''
               54  LOAD_FAST                'self'
               56  STORE_ATTR               description

 L. 104        58  LOAD_GLOBAL              _read_field_from_msg
               60  LOAD_FAST                'msg'
               62  LOAD_STR                 'author'
               64  CALL_FUNCTION_2       2  ''
               66  LOAD_FAST                'self'
               68  STORE_ATTR               author

 L. 105        70  LOAD_CONST               None
               72  LOAD_FAST                'self'
               74  STORE_ATTR               maintainer

 L. 106        76  LOAD_GLOBAL              _read_field_from_msg
               78  LOAD_FAST                'msg'
               80  LOAD_STR                 'author-email'
               82  CALL_FUNCTION_2       2  ''
               84  LOAD_FAST                'self'
               86  STORE_ATTR               author_email

 L. 107        88  LOAD_CONST               None
               90  LOAD_FAST                'self'
               92  STORE_ATTR               maintainer_email

 L. 108        94  LOAD_GLOBAL              _read_field_from_msg
               96  LOAD_FAST                'msg'
               98  LOAD_STR                 'home-page'
              100  CALL_FUNCTION_2       2  ''
              102  LOAD_FAST                'self'
              104  STORE_ATTR               url

 L. 109       106  LOAD_GLOBAL              _read_field_unescaped_from_msg
              108  LOAD_FAST                'msg'
              110  LOAD_STR                 'license'
              112  CALL_FUNCTION_2       2  ''
              114  LOAD_FAST                'self'
              116  STORE_ATTR               license

 L. 111       118  LOAD_STR                 'download-url'
              120  LOAD_FAST                'msg'
              122  <118>                 0  ''
              124  POP_JUMP_IF_FALSE   140  'to 140'

 L. 112       126  LOAD_GLOBAL              _read_field_from_msg
              128  LOAD_FAST                'msg'
              130  LOAD_STR                 'download-url'
              132  CALL_FUNCTION_2       2  ''
              134  LOAD_FAST                'self'
              136  STORE_ATTR               download_url
              138  JUMP_FORWARD        146  'to 146'
            140_0  COME_FROM           124  '124'

 L. 114       140  LOAD_CONST               None
              142  LOAD_FAST                'self'
              144  STORE_ATTR               download_url
            146_0  COME_FROM           138  '138'

 L. 116       146  LOAD_GLOBAL              _read_field_unescaped_from_msg
              148  LOAD_FAST                'msg'
              150  LOAD_STR                 'description'
              152  CALL_FUNCTION_2       2  ''
              154  LOAD_FAST                'self'
              156  STORE_ATTR               long_description

 L. 117       158  LOAD_GLOBAL              _read_field_from_msg
              160  LOAD_FAST                'msg'
              162  LOAD_STR                 'summary'
              164  CALL_FUNCTION_2       2  ''
              166  LOAD_FAST                'self'
              168  STORE_ATTR               description

 L. 119       170  LOAD_STR                 'keywords'
              172  LOAD_FAST                'msg'
              174  <118>                 0  ''
              176  POP_JUMP_IF_FALSE   196  'to 196'

 L. 120       178  LOAD_GLOBAL              _read_field_from_msg
              180  LOAD_FAST                'msg'
              182  LOAD_STR                 'keywords'
              184  CALL_FUNCTION_2       2  ''
              186  LOAD_METHOD              split
              188  LOAD_STR                 ','
              190  CALL_METHOD_1         1  ''
              192  LOAD_FAST                'self'
              194  STORE_ATTR               keywords
            196_0  COME_FROM           176  '176'

 L. 122       196  LOAD_GLOBAL              _read_list_from_msg
              198  LOAD_FAST                'msg'
              200  LOAD_STR                 'platform'
              202  CALL_FUNCTION_2       2  ''
              204  LOAD_FAST                'self'
              206  STORE_ATTR               platforms

 L. 123       208  LOAD_GLOBAL              _read_list_from_msg
              210  LOAD_FAST                'msg'
              212  LOAD_STR                 'classifier'
              214  CALL_FUNCTION_2       2  ''
              216  LOAD_FAST                'self'
              218  STORE_ATTR               classifiers

 L. 126       220  LOAD_FAST                'self'
              222  LOAD_ATTR                metadata_version
              224  LOAD_GLOBAL              StrictVersion
              226  LOAD_STR                 '1.1'
              228  CALL_FUNCTION_1       1  ''
              230  COMPARE_OP               ==
          232_234  POP_JUMP_IF_FALSE   274  'to 274'

 L. 127       236  LOAD_GLOBAL              _read_list_from_msg
              238  LOAD_FAST                'msg'
              240  LOAD_STR                 'requires'
              242  CALL_FUNCTION_2       2  ''
              244  LOAD_FAST                'self'
              246  STORE_ATTR               requires

 L. 128       248  LOAD_GLOBAL              _read_list_from_msg
              250  LOAD_FAST                'msg'
              252  LOAD_STR                 'provides'
              254  CALL_FUNCTION_2       2  ''
              256  LOAD_FAST                'self'
              258  STORE_ATTR               provides

 L. 129       260  LOAD_GLOBAL              _read_list_from_msg
              262  LOAD_FAST                'msg'
              264  LOAD_STR                 'obsoletes'
              266  CALL_FUNCTION_2       2  ''
              268  LOAD_FAST                'self'
              270  STORE_ATTR               obsoletes
              272  JUMP_FORWARD        292  'to 292'
            274_0  COME_FROM           232  '232'

 L. 131       274  LOAD_CONST               None
              276  LOAD_FAST                'self'
              278  STORE_ATTR               requires

 L. 132       280  LOAD_CONST               None
              282  LOAD_FAST                'self'
              284  STORE_ATTR               provides

 L. 133       286  LOAD_CONST               None
              288  LOAD_FAST                'self'
              290  STORE_ATTR               obsoletes
            292_0  COME_FROM           272  '272'

Parse error at or near `<118>' instruction at offset 122


def single_line--- This code section failed: ---

 L. 138         0  LOAD_STR                 '\n'
                2  LOAD_FAST                'val'
                4  <118>                 0  ''
                6  POP_JUMP_IF_FALSE    30  'to 30'

 L. 140         8  LOAD_GLOBAL              warnings
               10  LOAD_METHOD              warn
               12  LOAD_STR                 'newlines not allowed and will break in the future'
               14  CALL_METHOD_1         1  ''
               16  POP_TOP          

 L. 141        18  LOAD_FAST                'val'
               20  LOAD_METHOD              replace
               22  LOAD_STR                 '\n'
               24  LOAD_STR                 ' '
               26  CALL_METHOD_2         2  ''
               28  STORE_FAST               'val'
             30_0  COME_FROM             6  '6'

 L. 142        30  LOAD_FAST                'val'
               32  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def write_pkg_file--- This code section failed: ---

 L. 149         0  LOAD_FAST                'self'
                2  LOAD_METHOD              get_metadata_version
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'version'

 L. 151         8  LOAD_CLOSURE             'file'
               10  BUILD_TUPLE_1         1 
               12  LOAD_CODE                <code_object write_field>
               14  LOAD_STR                 'write_pkg_file.<locals>.write_field'
               16  MAKE_FUNCTION_8          'closure'
               18  STORE_FAST               'write_field'

 L. 154        20  LOAD_FAST                'write_field'
               22  LOAD_STR                 'Metadata-Version'
               24  LOAD_GLOBAL              str
               26  LOAD_FAST                'version'
               28  CALL_FUNCTION_1       1  ''
               30  CALL_FUNCTION_2       2  ''
               32  POP_TOP          

 L. 155        34  LOAD_FAST                'write_field'
               36  LOAD_STR                 'Name'
               38  LOAD_FAST                'self'
               40  LOAD_METHOD              get_name
               42  CALL_METHOD_0         0  ''
               44  CALL_FUNCTION_2       2  ''
               46  POP_TOP          

 L. 156        48  LOAD_FAST                'write_field'
               50  LOAD_STR                 'Version'
               52  LOAD_FAST                'self'
               54  LOAD_METHOD              get_version
               56  CALL_METHOD_0         0  ''
               58  CALL_FUNCTION_2       2  ''
               60  POP_TOP          

 L. 157        62  LOAD_FAST                'write_field'
               64  LOAD_STR                 'Summary'
               66  LOAD_GLOBAL              single_line
               68  LOAD_FAST                'self'
               70  LOAD_METHOD              get_description
               72  CALL_METHOD_0         0  ''
               74  CALL_FUNCTION_1       1  ''
               76  CALL_FUNCTION_2       2  ''
               78  POP_TOP          

 L. 158        80  LOAD_FAST                'write_field'
               82  LOAD_STR                 'Home-page'
               84  LOAD_FAST                'self'
               86  LOAD_METHOD              get_url
               88  CALL_METHOD_0         0  ''
               90  CALL_FUNCTION_2       2  ''
               92  POP_TOP          

 L. 160        94  LOAD_CONST               (('Author', 'author'), ('Author-email', 'author_email'), ('Maintainer', 'maintainer'), ('Maintainer-email', 'maintainer_email'))
               96  STORE_FAST               'optional_fields'

 L. 167        98  LOAD_FAST                'optional_fields'
              100  GET_ITER         
            102_0  COME_FROM           128  '128'
              102  FOR_ITER            142  'to 142'
              104  UNPACK_SEQUENCE_2     2 
              106  STORE_FAST               'field'
              108  STORE_FAST               'attr'

 L. 168       110  LOAD_GLOBAL              getattr
              112  LOAD_FAST                'self'
              114  LOAD_FAST                'attr'
              116  LOAD_CONST               None
              118  CALL_FUNCTION_3       3  ''
              120  STORE_FAST               'attr_val'

 L. 169       122  LOAD_FAST                'attr_val'
              124  LOAD_CONST               None
              126  <117>                 1  ''
              128  POP_JUMP_IF_FALSE   102  'to 102'

 L. 170       130  LOAD_FAST                'write_field'
              132  LOAD_FAST                'field'
              134  LOAD_FAST                'attr_val'
              136  CALL_FUNCTION_2       2  ''
              138  POP_TOP          
              140  JUMP_BACK           102  'to 102'

 L. 172       142  LOAD_GLOBAL              rfc822_escape
              144  LOAD_FAST                'self'
              146  LOAD_METHOD              get_license
              148  CALL_METHOD_0         0  ''
              150  CALL_FUNCTION_1       1  ''
              152  STORE_FAST               'license'

 L. 173       154  LOAD_FAST                'write_field'
              156  LOAD_STR                 'License'
              158  LOAD_FAST                'license'
              160  CALL_FUNCTION_2       2  ''
              162  POP_TOP          

 L. 174       164  LOAD_FAST                'self'
              166  LOAD_ATTR                download_url
              168  POP_JUMP_IF_FALSE   182  'to 182'

 L. 175       170  LOAD_FAST                'write_field'
              172  LOAD_STR                 'Download-URL'
              174  LOAD_FAST                'self'
              176  LOAD_ATTR                download_url
              178  CALL_FUNCTION_2       2  ''
              180  POP_TOP          
            182_0  COME_FROM           168  '168'

 L. 176       182  LOAD_FAST                'self'
              184  LOAD_ATTR                project_urls
              186  LOAD_METHOD              items
              188  CALL_METHOD_0         0  ''
              190  GET_ITER         
              192  FOR_ITER            212  'to 212'
              194  STORE_FAST               'project_url'

 L. 177       196  LOAD_FAST                'write_field'
              198  LOAD_STR                 'Project-URL'
              200  LOAD_STR                 '%s, %s'
              202  LOAD_FAST                'project_url'
              204  BINARY_MODULO    
              206  CALL_FUNCTION_2       2  ''
              208  POP_TOP          
              210  JUMP_BACK           192  'to 192'

 L. 179       212  LOAD_GLOBAL              rfc822_escape
              214  LOAD_FAST                'self'
              216  LOAD_METHOD              get_long_description
              218  CALL_METHOD_0         0  ''
              220  CALL_FUNCTION_1       1  ''
              222  STORE_FAST               'long_desc'

 L. 180       224  LOAD_FAST                'write_field'
              226  LOAD_STR                 'Description'
              228  LOAD_FAST                'long_desc'
              230  CALL_FUNCTION_2       2  ''
              232  POP_TOP          

 L. 182       234  LOAD_STR                 ','
              236  LOAD_METHOD              join
              238  LOAD_FAST                'self'
              240  LOAD_METHOD              get_keywords
              242  CALL_METHOD_0         0  ''
              244  CALL_METHOD_1         1  ''
              246  STORE_FAST               'keywords'

 L. 183       248  LOAD_FAST                'keywords'
          250_252  POP_JUMP_IF_FALSE   264  'to 264'

 L. 184       254  LOAD_FAST                'write_field'
              256  LOAD_STR                 'Keywords'
              258  LOAD_FAST                'keywords'
              260  CALL_FUNCTION_2       2  ''
              262  POP_TOP          
            264_0  COME_FROM           250  '250'

 L. 186       264  LOAD_FAST                'self'
              266  LOAD_METHOD              get_platforms
              268  CALL_METHOD_0         0  ''
              270  GET_ITER         
              272  FOR_ITER            290  'to 290'
              274  STORE_FAST               'platform'

 L. 187       276  LOAD_FAST                'write_field'
              278  LOAD_STR                 'Platform'
              280  LOAD_FAST                'platform'
              282  CALL_FUNCTION_2       2  ''
              284  POP_TOP          
          286_288  JUMP_BACK           272  'to 272'

 L. 189       290  LOAD_FAST                'self'
              292  LOAD_METHOD              _write_list
              294  LOAD_DEREF               'file'
              296  LOAD_STR                 'Classifier'
              298  LOAD_FAST                'self'
              300  LOAD_METHOD              get_classifiers
              302  CALL_METHOD_0         0  ''
              304  CALL_METHOD_3         3  ''
              306  POP_TOP          

 L. 192       308  LOAD_FAST                'self'
              310  LOAD_METHOD              _write_list
              312  LOAD_DEREF               'file'
              314  LOAD_STR                 'Requires'
              316  LOAD_FAST                'self'
              318  LOAD_METHOD              get_requires
              320  CALL_METHOD_0         0  ''
              322  CALL_METHOD_3         3  ''
              324  POP_TOP          

 L. 193       326  LOAD_FAST                'self'
              328  LOAD_METHOD              _write_list
              330  LOAD_DEREF               'file'
              332  LOAD_STR                 'Provides'
              334  LOAD_FAST                'self'
              336  LOAD_METHOD              get_provides
              338  CALL_METHOD_0         0  ''
              340  CALL_METHOD_3         3  ''
              342  POP_TOP          

 L. 194       344  LOAD_FAST                'self'
              346  LOAD_METHOD              _write_list
              348  LOAD_DEREF               'file'
              350  LOAD_STR                 'Obsoletes'
              352  LOAD_FAST                'self'
              354  LOAD_METHOD              get_obsoletes
              356  CALL_METHOD_0         0  ''
              358  CALL_METHOD_3         3  ''
              360  POP_TOP          

 L. 197       362  LOAD_GLOBAL              hasattr
              364  LOAD_FAST                'self'
              366  LOAD_STR                 'python_requires'
              368  CALL_FUNCTION_2       2  ''
          370_372  POP_JUMP_IF_FALSE   386  'to 386'

 L. 198       374  LOAD_FAST                'write_field'
              376  LOAD_STR                 'Requires-Python'
              378  LOAD_FAST                'self'
              380  LOAD_ATTR                python_requires
              382  CALL_FUNCTION_2       2  ''
              384  POP_TOP          
            386_0  COME_FROM           370  '370'

 L. 201       386  LOAD_FAST                'self'
              388  LOAD_ATTR                long_description_content_type
          390_392  POP_JUMP_IF_FALSE   406  'to 406'

 L. 202       394  LOAD_FAST                'write_field'

 L. 203       396  LOAD_STR                 'Description-Content-Type'

 L. 204       398  LOAD_FAST                'self'
              400  LOAD_ATTR                long_description_content_type

 L. 202       402  CALL_FUNCTION_2       2  ''
              404  POP_TOP          
            406_0  COME_FROM           390  '390'

 L. 206       406  LOAD_FAST                'self'
              408  LOAD_ATTR                provides_extras
          410_412  POP_JUMP_IF_FALSE   438  'to 438'

 L. 207       414  LOAD_FAST                'self'
              416  LOAD_ATTR                provides_extras
              418  GET_ITER         
              420  FOR_ITER            438  'to 438'
              422  STORE_FAST               'extra'

 L. 208       424  LOAD_FAST                'write_field'
              426  LOAD_STR                 'Provides-Extra'
              428  LOAD_FAST                'extra'
              430  CALL_FUNCTION_2       2  ''
              432  POP_TOP          
          434_436  JUMP_BACK           420  'to 420'
            438_0  COME_FROM           410  '410'

Parse error at or near `<117>' instruction at offset 126


sequence = (
 tuple, list)

def check_importable--- This code section failed: ---

 L. 215         0  SETUP_FINALLY        32  'to 32'

 L. 216         2  LOAD_GLOBAL              pkg_resources
                4  LOAD_ATTR                EntryPoint
                6  LOAD_METHOD              parse
                8  LOAD_STR                 'x='
               10  LOAD_FAST                'value'
               12  BINARY_ADD       
               14  CALL_METHOD_1         1  ''
               16  STORE_FAST               'ep'

 L. 217        18  LOAD_FAST                'ep'
               20  LOAD_ATTR                extras
               22  POP_JUMP_IF_FALSE    28  'to 28'
               24  <74>             
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            22  '22'
               28  POP_BLOCK        
               30  JUMP_FORWARD         94  'to 94'
             32_0  COME_FROM_FINALLY     0  '0'

 L. 218        32  DUP_TOP          
               34  LOAD_GLOBAL              TypeError
               36  LOAD_GLOBAL              ValueError
               38  LOAD_GLOBAL              AttributeError
               40  LOAD_GLOBAL              AssertionError
               42  BUILD_TUPLE_4         4 
               44  <121>                92  ''
               46  POP_TOP          
               48  STORE_FAST               'e'
               50  POP_TOP          
               52  SETUP_FINALLY        84  'to 84'

 L. 219        54  LOAD_GLOBAL              DistutilsSetupError

 L. 220        56  LOAD_STR                 "%r must be importable 'module:attrs' string (got %r)"

 L. 221        58  LOAD_FAST                'attr'
               60  LOAD_FAST                'value'
               62  BUILD_TUPLE_2         2 

 L. 220        64  BINARY_MODULO    

 L. 219        66  CALL_FUNCTION_1       1  ''

 L. 222        68  LOAD_FAST                'e'

 L. 219        70  RAISE_VARARGS_2       2  'exception instance with __cause__'
               72  POP_BLOCK        
               74  POP_EXCEPT       
               76  LOAD_CONST               None
               78  STORE_FAST               'e'
               80  DELETE_FAST              'e'
               82  JUMP_FORWARD         94  'to 94'
             84_0  COME_FROM_FINALLY    52  '52'
               84  LOAD_CONST               None
               86  STORE_FAST               'e'
               88  DELETE_FAST              'e'
               90  <48>             
               92  <48>             
             94_0  COME_FROM            82  '82'
             94_1  COME_FROM            30  '30'

Parse error at or near `<74>' instruction at offset 24


def assert_string_list--- This code section failed: ---

 L. 227         0  SETUP_FINALLY        42  'to 42'

 L. 230         2  LOAD_GLOBAL              isinstance
                4  LOAD_FAST                'value'
                6  LOAD_GLOBAL              list
                8  LOAD_GLOBAL              tuple
               10  BUILD_TUPLE_2         2 
               12  CALL_FUNCTION_2       2  ''
               14  POP_JUMP_IF_TRUE     20  'to 20'
               16  <74>             
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            14  '14'

 L. 232        20  LOAD_STR                 ''
               22  LOAD_METHOD              join
               24  LOAD_FAST                'value'
               26  CALL_METHOD_1         1  ''
               28  LOAD_FAST                'value'
               30  COMPARE_OP               !=
               32  POP_JUMP_IF_TRUE     38  'to 38'
               34  <74>             
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            32  '32'
               38  POP_BLOCK        
               40  JUMP_FORWARD        104  'to 104'
             42_0  COME_FROM_FINALLY     0  '0'

 L. 233        42  DUP_TOP          
               44  LOAD_GLOBAL              TypeError
               46  LOAD_GLOBAL              ValueError
               48  LOAD_GLOBAL              AttributeError
               50  LOAD_GLOBAL              AssertionError
               52  BUILD_TUPLE_4         4 
               54  <121>               102  ''
               56  POP_TOP          
               58  STORE_FAST               'e'
               60  POP_TOP          
               62  SETUP_FINALLY        94  'to 94'

 L. 234        64  LOAD_GLOBAL              DistutilsSetupError

 L. 235        66  LOAD_STR                 '%r must be a list of strings (got %r)'
               68  LOAD_FAST                'attr'
               70  LOAD_FAST                'value'
               72  BUILD_TUPLE_2         2 
               74  BINARY_MODULO    

 L. 234        76  CALL_FUNCTION_1       1  ''

 L. 236        78  LOAD_FAST                'e'

 L. 234        80  RAISE_VARARGS_2       2  'exception instance with __cause__'
               82  POP_BLOCK        
               84  POP_EXCEPT       
               86  LOAD_CONST               None
               88  STORE_FAST               'e'
               90  DELETE_FAST              'e'
               92  JUMP_FORWARD        104  'to 104'
             94_0  COME_FROM_FINALLY    62  '62'
               94  LOAD_CONST               None
               96  STORE_FAST               'e'
               98  DELETE_FAST              'e'
              100  <48>             
              102  <48>             
            104_0  COME_FROM            92  '92'
            104_1  COME_FROM            40  '40'

Parse error at or near `<74>' instruction at offset 16


def check_nsp--- This code section failed: ---

 L. 241         0  LOAD_FAST                'value'
                2  STORE_FAST               'ns_packages'

 L. 242         4  LOAD_GLOBAL              assert_string_list
                6  LOAD_FAST                'dist'
                8  LOAD_FAST                'attr'
               10  LOAD_FAST                'ns_packages'
               12  CALL_FUNCTION_3       3  ''
               14  POP_TOP          

 L. 243        16  LOAD_FAST                'ns_packages'
               18  GET_ITER         
             20_0  COME_FROM            76  '76'
             20_1  COME_FROM            68  '68'
               20  FOR_ITER             96  'to 96'
               22  STORE_FAST               'nsp'

 L. 244        24  LOAD_FAST                'dist'
               26  LOAD_METHOD              has_contents_for
               28  LOAD_FAST                'nsp'
               30  CALL_METHOD_1         1  ''
               32  POP_JUMP_IF_TRUE     50  'to 50'

 L. 245        34  LOAD_GLOBAL              DistutilsSetupError

 L. 246        36  LOAD_STR                 'Distribution contains no modules or packages for '

 L. 247        38  LOAD_STR                 'namespace package %r'
               40  LOAD_FAST                'nsp'
               42  BINARY_MODULO    

 L. 246        44  BINARY_ADD       

 L. 245        46  CALL_FUNCTION_1       1  ''
               48  RAISE_VARARGS_1       1  'exception instance'
             50_0  COME_FROM            32  '32'

 L. 249        50  LOAD_FAST                'nsp'
               52  LOAD_METHOD              rpartition
               54  LOAD_STR                 '.'
               56  CALL_METHOD_1         1  ''
               58  UNPACK_SEQUENCE_3     3 
               60  STORE_FAST               'parent'
               62  STORE_FAST               'sep'
               64  STORE_FAST               'child'

 L. 250        66  LOAD_FAST                'parent'
               68  POP_JUMP_IF_FALSE    20  'to 20'
               70  LOAD_FAST                'parent'
               72  LOAD_FAST                'ns_packages'
               74  <118>                 1  ''
               76  POP_JUMP_IF_FALSE    20  'to 20'

 L. 251        78  LOAD_GLOBAL              distutils
               80  LOAD_ATTR                log
               82  LOAD_METHOD              warn

 L. 252        84  LOAD_STR                 'WARNING: %r is declared as a package namespace, but %r is not: please correct this in setup.py'

 L. 253        86  LOAD_FAST                'nsp'
               88  LOAD_FAST                'parent'

 L. 251        90  CALL_METHOD_3         3  ''
               92  POP_TOP          
               94  JUMP_BACK            20  'to 20'

Parse error at or near `<118>' instruction at offset 74


def check_extras--- This code section failed: ---

 L. 259         0  SETUP_FINALLY        26  'to 26'

 L. 260         2  LOAD_GLOBAL              list
                4  LOAD_GLOBAL              itertools
                6  LOAD_METHOD              starmap
                8  LOAD_GLOBAL              _check_extra
               10  LOAD_FAST                'value'
               12  LOAD_METHOD              items
               14  CALL_METHOD_0         0  ''
               16  CALL_METHOD_2         2  ''
               18  CALL_FUNCTION_1       1  ''
               20  POP_TOP          
               22  POP_BLOCK        
               24  JUMP_FORWARD         78  'to 78'
             26_0  COME_FROM_FINALLY     0  '0'

 L. 261        26  DUP_TOP          
               28  LOAD_GLOBAL              TypeError
               30  LOAD_GLOBAL              ValueError
               32  LOAD_GLOBAL              AttributeError
               34  BUILD_TUPLE_3         3 
               36  <121>                76  ''
               38  POP_TOP          
               40  STORE_FAST               'e'
               42  POP_TOP          
               44  SETUP_FINALLY        68  'to 68'

 L. 262        46  LOAD_GLOBAL              DistutilsSetupError

 L. 263        48  LOAD_STR                 "'extras_require' must be a dictionary whose values are strings or lists of strings containing valid project/version requirement specifiers."

 L. 262        50  CALL_FUNCTION_1       1  ''

 L. 266        52  LOAD_FAST                'e'

 L. 262        54  RAISE_VARARGS_2       2  'exception instance with __cause__'
               56  POP_BLOCK        
               58  POP_EXCEPT       
               60  LOAD_CONST               None
               62  STORE_FAST               'e'
               64  DELETE_FAST              'e'
               66  JUMP_FORWARD         78  'to 78'
             68_0  COME_FROM_FINALLY    44  '44'
               68  LOAD_CONST               None
               70  STORE_FAST               'e'
               72  DELETE_FAST              'e'
               74  <48>             
               76  <48>             
             78_0  COME_FROM            66  '66'
             78_1  COME_FROM            24  '24'

Parse error at or near `<121>' instruction at offset 36


def _check_extra(extra, reqs):
    name, sep, marker = extra.partition(':')
    if marker:
        if pkg_resources.invalid_marker(marker):
            raise DistutilsSetupError('Invalid environment marker: ' + marker)
    list(pkg_resources.parse_requirements(reqs))


def assert_bool(dist, attr, value):
    """Verify that value is True, False, 0, or 1"""
    if bool(value) != value:
        tmpl = '{attr!r} must be a boolean value (got {value!r})'
        raise DistutilsSetupError(tmpl.format(attr=attr, value=value))


def check_requirements--- This code section failed: ---

 L. 285         0  SETUP_FINALLY        42  'to 42'

 L. 286         2  LOAD_GLOBAL              list
                4  LOAD_GLOBAL              pkg_resources
                6  LOAD_METHOD              parse_requirements
                8  LOAD_FAST                'value'
               10  CALL_METHOD_1         1  ''
               12  CALL_FUNCTION_1       1  ''
               14  POP_TOP          

 L. 287        16  LOAD_GLOBAL              isinstance
               18  LOAD_FAST                'value'
               20  LOAD_GLOBAL              dict
               22  LOAD_GLOBAL              set
               24  BUILD_TUPLE_2         2 
               26  CALL_FUNCTION_2       2  ''
               28  POP_JUMP_IF_FALSE    38  'to 38'

 L. 288        30  LOAD_GLOBAL              TypeError
               32  LOAD_STR                 'Unordered types are not allowed'
               34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            28  '28'
               38  POP_BLOCK        
               40  JUMP_FORWARD        106  'to 106'
             42_0  COME_FROM_FINALLY     0  '0'

 L. 289        42  DUP_TOP          
               44  LOAD_GLOBAL              TypeError
               46  LOAD_GLOBAL              ValueError
               48  BUILD_TUPLE_2         2 
               50  <121>               104  ''
               52  POP_TOP          
               54  STORE_FAST               'error'
               56  POP_TOP          
               58  SETUP_FINALLY        96  'to 96'

 L. 291        60  LOAD_STR                 '{attr!r} must be a string or list of strings containing valid project/version requirement specifiers; {error}'

 L. 290        62  STORE_FAST               'tmpl'

 L. 294        64  LOAD_GLOBAL              DistutilsSetupError

 L. 295        66  LOAD_FAST                'tmpl'
               68  LOAD_ATTR                format
               70  LOAD_FAST                'attr'
               72  LOAD_FAST                'error'
               74  LOAD_CONST               ('attr', 'error')
               76  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 294        78  CALL_FUNCTION_1       1  ''

 L. 296        80  LOAD_FAST                'error'

 L. 294        82  RAISE_VARARGS_2       2  'exception instance with __cause__'
               84  POP_BLOCK        
               86  POP_EXCEPT       
               88  LOAD_CONST               None
               90  STORE_FAST               'error'
               92  DELETE_FAST              'error'
               94  JUMP_FORWARD        106  'to 106'
             96_0  COME_FROM_FINALLY    58  '58'
               96  LOAD_CONST               None
               98  STORE_FAST               'error'
              100  DELETE_FAST              'error'
              102  <48>             
              104  <48>             
            106_0  COME_FROM            94  '94'
            106_1  COME_FROM            40  '40'

Parse error at or near `<121>' instruction at offset 50


def check_specifier--- This code section failed: ---

 L. 301         0  SETUP_FINALLY        18  'to 18'

 L. 302         2  LOAD_GLOBAL              packaging
                4  LOAD_ATTR                specifiers
                6  LOAD_METHOD              SpecifierSet
                8  LOAD_FAST                'value'
               10  CALL_METHOD_1         1  ''
               12  POP_TOP          
               14  POP_BLOCK        
               16  JUMP_FORWARD         86  'to 86'
             18_0  COME_FROM_FINALLY     0  '0'

 L. 303        18  DUP_TOP          
               20  LOAD_GLOBAL              packaging
               22  LOAD_ATTR                specifiers
               24  LOAD_ATTR                InvalidSpecifier
               26  LOAD_GLOBAL              AttributeError
               28  BUILD_TUPLE_2         2 
               30  <121>                84  ''
               32  POP_TOP          
               34  STORE_FAST               'error'
               36  POP_TOP          
               38  SETUP_FINALLY        76  'to 76'

 L. 305        40  LOAD_STR                 '{attr!r} must be a string containing valid version specifiers; {error}'

 L. 304        42  STORE_FAST               'tmpl'

 L. 308        44  LOAD_GLOBAL              DistutilsSetupError

 L. 309        46  LOAD_FAST                'tmpl'
               48  LOAD_ATTR                format
               50  LOAD_FAST                'attr'
               52  LOAD_FAST                'error'
               54  LOAD_CONST               ('attr', 'error')
               56  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 308        58  CALL_FUNCTION_1       1  ''

 L. 310        60  LOAD_FAST                'error'

 L. 308        62  RAISE_VARARGS_2       2  'exception instance with __cause__'
               64  POP_BLOCK        
               66  POP_EXCEPT       
               68  LOAD_CONST               None
               70  STORE_FAST               'error'
               72  DELETE_FAST              'error'
               74  JUMP_FORWARD         86  'to 86'
             76_0  COME_FROM_FINALLY    38  '38'
               76  LOAD_CONST               None
               78  STORE_FAST               'error'
               80  DELETE_FAST              'error'
               82  <48>             
               84  <48>             
             86_0  COME_FROM            74  '74'
             86_1  COME_FROM            16  '16'

Parse error at or near `<121>' instruction at offset 30


def check_entry_points--- This code section failed: ---

 L. 315         0  SETUP_FINALLY        18  'to 18'

 L. 316         2  LOAD_GLOBAL              pkg_resources
                4  LOAD_ATTR                EntryPoint
                6  LOAD_METHOD              parse_map
                8  LOAD_FAST                'value'
               10  CALL_METHOD_1         1  ''
               12  POP_TOP          
               14  POP_BLOCK        
               16  JUMP_FORWARD         64  'to 64'
             18_0  COME_FROM_FINALLY     0  '0'

 L. 317        18  DUP_TOP          
               20  LOAD_GLOBAL              ValueError
               22  <121>                62  ''
               24  POP_TOP          
               26  STORE_FAST               'e'
               28  POP_TOP          
               30  SETUP_FINALLY        54  'to 54'

 L. 318        32  LOAD_GLOBAL              DistutilsSetupError
               34  LOAD_FAST                'e'
               36  CALL_FUNCTION_1       1  ''
               38  LOAD_FAST                'e'
               40  RAISE_VARARGS_2       2  'exception instance with __cause__'
               42  POP_BLOCK        
               44  POP_EXCEPT       
               46  LOAD_CONST               None
               48  STORE_FAST               'e'
               50  DELETE_FAST              'e'
               52  JUMP_FORWARD         64  'to 64'
             54_0  COME_FROM_FINALLY    30  '30'
               54  LOAD_CONST               None
               56  STORE_FAST               'e'
               58  DELETE_FAST              'e'
               60  <48>             
               62  <48>             
             64_0  COME_FROM            52  '52'
             64_1  COME_FROM            16  '16'

Parse error at or near `<121>' instruction at offset 22


def check_test_suite(dist, attr, value):
    if not isinstancevaluestr:
        raise DistutilsSetupError('test_suite must be a string')


def check_package_data(dist, attr, value):
    """Verify that value is a dictionary of package names to glob lists"""
    if not isinstancevaluedict:
        raise DistutilsSetupError('{!r} must be a dictionary mapping package names to lists of string wildcard patterns'.format(attr))
    for k, v in value.items():
        if not isinstancekstr:
            raise DistutilsSetupError('keys of {!r} dict must be strings (got {!r})'.format(attr, k))
        assert_string_list(dist, 'values of {!r} dict'.format(attr), v)


def check_packages(dist, attr, value):
    for pkgname in value:
        if not re.match('\\w+(\\.\\w+)*', pkgname):
            distutils.log.warn('WARNING: %r not a valid package name; please use only .-separated package names in setup.py', pkgname)


_Distribution = get_unpatched(distutils.core.Distribution)

class Distribution(_Distribution):
    __doc__ = 'Distribution with support for tests and package data\n\n    This is an enhanced version of \'distutils.dist.Distribution\' that\n    effectively adds the following new optional keyword arguments to \'setup()\':\n\n     \'install_requires\' -- a string or sequence of strings specifying project\n        versions that the distribution requires when installed, in the format\n        used by \'pkg_resources.require()\'.  They will be installed\n        automatically when the package is installed.  If you wish to use\n        packages that are not available in PyPI, or want to give your users an\n        alternate download location, you can add a \'find_links\' option to the\n        \'[easy_install]\' section of your project\'s \'setup.cfg\' file, and then\n        setuptools will scan the listed web pages for links that satisfy the\n        requirements.\n\n     \'extras_require\' -- a dictionary mapping names of optional "extras" to the\n        additional requirement(s) that using those extras incurs. For example,\n        this::\n\n            extras_require = dict(reST = ["docutils>=0.3", "reSTedit"])\n\n        indicates that the distribution can optionally provide an extra\n        capability called "reST", but it can only be used if docutils and\n        reSTedit are installed.  If the user installs your package using\n        EasyInstall and requests one of your extras, the corresponding\n        additional requirements will be installed if needed.\n\n     \'test_suite\' -- the name of a test suite to run for the \'test\' command.\n        If the user runs \'python setup.py test\', the package will be installed,\n        and the named test suite will be run.  The format is the same as\n        would be used on a \'unittest.py\' command line.  That is, it is the\n        dotted name of an object to import and call to generate a test suite.\n\n     \'package_data\' -- a dictionary mapping package names to lists of filenames\n        or globs to use to find data files contained in the named packages.\n        If the dictionary has filenames or globs listed under \'""\' (the empty\n        string), those names will be searched for in every package, in addition\n        to any names for the specific package.  Data files found using these\n        names/globs will be installed along with the package, in the same\n        location as the package.  Note that globs are allowed to reference\n        the contents of non-package subdirectories, as long as you use \'/\' as\n        a path separator.  (Globs are automatically converted to\n        platform-specific paths at runtime.)\n\n    In addition to these new keywords, this class also has several new methods\n    for manipulating the distribution\'s contents.  For example, the \'include()\'\n    and \'exclude()\' methods can be thought of as in-place add and subtract\n    commands that add or remove packages, modules, extensions, and so on from\n    the distribution.\n    '
    _DISTUTILS_UNSUPPORTED_METADATA = {'long_description_content_type':None, 
     'project_urls':dict, 
     'provides_extras':ordered_set.OrderedSet, 
     'license_files':ordered_set.OrderedSet}
    _patched_dist = None

    def patch_missing_pkg_info--- This code section failed: ---

 L. 419         0  LOAD_FAST                'attrs'
                2  POP_JUMP_IF_FALSE    20  'to 20'
                4  LOAD_STR                 'name'
                6  LOAD_FAST                'attrs'
                8  <118>                 1  ''
               10  POP_JUMP_IF_TRUE     20  'to 20'
               12  LOAD_STR                 'version'
               14  LOAD_FAST                'attrs'
               16  <118>                 1  ''
               18  POP_JUMP_IF_FALSE    24  'to 24'
             20_0  COME_FROM            10  '10'
             20_1  COME_FROM             2  '2'

 L. 420        20  LOAD_CONST               None
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L. 421        24  LOAD_GLOBAL              pkg_resources
               26  LOAD_METHOD              safe_name
               28  LOAD_GLOBAL              str
               30  LOAD_FAST                'attrs'
               32  LOAD_STR                 'name'
               34  BINARY_SUBSCR    
               36  CALL_FUNCTION_1       1  ''
               38  CALL_METHOD_1         1  ''
               40  LOAD_METHOD              lower
               42  CALL_METHOD_0         0  ''
               44  STORE_FAST               'key'

 L. 422        46  LOAD_GLOBAL              pkg_resources
               48  LOAD_ATTR                working_set
               50  LOAD_ATTR                by_key
               52  LOAD_METHOD              get
               54  LOAD_FAST                'key'
               56  CALL_METHOD_1         1  ''
               58  STORE_FAST               'dist'

 L. 423        60  LOAD_FAST                'dist'
               62  LOAD_CONST               None
               64  <117>                 1  ''
               66  POP_JUMP_IF_FALSE   104  'to 104'
               68  LOAD_FAST                'dist'
               70  LOAD_METHOD              has_metadata
               72  LOAD_STR                 'PKG-INFO'
               74  CALL_METHOD_1         1  ''
               76  POP_JUMP_IF_TRUE    104  'to 104'

 L. 424        78  LOAD_GLOBAL              pkg_resources
               80  LOAD_METHOD              safe_version
               82  LOAD_GLOBAL              str
               84  LOAD_FAST                'attrs'
               86  LOAD_STR                 'version'
               88  BINARY_SUBSCR    
               90  CALL_FUNCTION_1       1  ''
               92  CALL_METHOD_1         1  ''
               94  LOAD_FAST                'dist'
               96  STORE_ATTR               _version

 L. 425        98  LOAD_FAST                'dist'
              100  LOAD_FAST                'self'
              102  STORE_ATTR               _patched_dist
            104_0  COME_FROM            76  '76'
            104_1  COME_FROM            66  '66'

Parse error at or near `None' instruction at offset -1

    def __init__--- This code section failed: ---

 L. 428         0  LOAD_GLOBAL              hasattr
                2  LOAD_DEREF               'self'
                4  LOAD_STR                 'package_data'
                6  CALL_FUNCTION_2       2  ''
                8  STORE_FAST               'have_package_data'

 L. 429        10  LOAD_FAST                'have_package_data'
               12  POP_JUMP_IF_TRUE     20  'to 20'

 L. 430        14  BUILD_MAP_0           0 
               16  LOAD_DEREF               'self'
               18  STORE_ATTR               package_data
             20_0  COME_FROM            12  '12'

 L. 431        20  LOAD_FAST                'attrs'
               22  JUMP_IF_TRUE_OR_POP    26  'to 26'
               24  BUILD_MAP_0           0 
             26_0  COME_FROM            22  '22'
               26  STORE_FAST               'attrs'

 L. 432        28  BUILD_LIST_0          0 
               30  LOAD_DEREF               'self'
               32  STORE_ATTR               dist_files

 L. 434        34  LOAD_FAST                'attrs'
               36  LOAD_METHOD              pop
               38  LOAD_STR                 'src_root'
               40  LOAD_CONST               None
               42  CALL_METHOD_2         2  ''
               44  LOAD_DEREF               'self'
               46  STORE_ATTR               src_root

 L. 435        48  LOAD_DEREF               'self'
               50  LOAD_METHOD              patch_missing_pkg_info
               52  LOAD_FAST                'attrs'
               54  CALL_METHOD_1         1  ''
               56  POP_TOP          

 L. 436        58  LOAD_FAST                'attrs'
               60  LOAD_METHOD              pop
               62  LOAD_STR                 'dependency_links'
               64  BUILD_LIST_0          0 
               66  CALL_METHOD_2         2  ''
               68  LOAD_DEREF               'self'
               70  STORE_ATTR               dependency_links

 L. 437        72  LOAD_FAST                'attrs'
               74  LOAD_METHOD              pop
               76  LOAD_STR                 'setup_requires'
               78  BUILD_LIST_0          0 
               80  CALL_METHOD_2         2  ''
               82  LOAD_DEREF               'self'
               84  STORE_ATTR               setup_requires

 L. 438        86  LOAD_GLOBAL              pkg_resources
               88  LOAD_METHOD              iter_entry_points
               90  LOAD_STR                 'distutils.setup_keywords'
               92  CALL_METHOD_1         1  ''
               94  GET_ITER         
               96  FOR_ITER            120  'to 120'
               98  STORE_FAST               'ep'

 L. 439       100  LOAD_GLOBAL              vars
              102  LOAD_DEREF               'self'
              104  CALL_FUNCTION_1       1  ''
              106  LOAD_METHOD              setdefault
              108  LOAD_FAST                'ep'
              110  LOAD_ATTR                name
              112  LOAD_CONST               None
              114  CALL_METHOD_2         2  ''
              116  POP_TOP          
              118  JUMP_BACK            96  'to 96'

 L. 440       120  LOAD_GLOBAL              _Distribution
              122  LOAD_METHOD              __init__
              124  LOAD_DEREF               'self'
              126  LOAD_CLOSURE             'self'
              128  BUILD_TUPLE_1         1 
              130  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              132  LOAD_STR                 'Distribution.__init__.<locals>.<dictcomp>'
              134  MAKE_FUNCTION_8          'closure'

 L. 441       136  LOAD_FAST                'attrs'
              138  LOAD_METHOD              items
              140  CALL_METHOD_0         0  ''

 L. 440       142  GET_ITER         
              144  CALL_FUNCTION_1       1  ''
              146  CALL_METHOD_2         2  ''
              148  POP_TOP          

 L. 448       150  LOAD_DEREF               'self'
              152  LOAD_ATTR                _DISTUTILS_UNSUPPORTED_METADATA
              154  LOAD_METHOD              items
              156  CALL_METHOD_0         0  ''
              158  GET_ITER         
              160  FOR_ITER            236  'to 236'
              162  UNPACK_SEQUENCE_2     2 
              164  STORE_FAST               'option'
              166  STORE_FAST               'default'

 L. 449       168  LOAD_DEREF               'self'
              170  LOAD_ATTR                metadata
              172  LOAD_ATTR                __dict__
              174  LOAD_FAST                'attrs'
              176  BUILD_TUPLE_2         2 
              178  GET_ITER         
            180_0  COME_FROM           190  '190'
              180  FOR_ITER            206  'to 206'
              182  STORE_FAST               'source'

 L. 450       184  LOAD_FAST                'option'
              186  LOAD_FAST                'source'
              188  <118>                 0  ''
              190  POP_JUMP_IF_FALSE   180  'to 180'

 L. 451       192  LOAD_FAST                'source'
              194  LOAD_FAST                'option'
              196  BINARY_SUBSCR    
              198  STORE_FAST               'value'

 L. 452       200  POP_TOP          
              202  BREAK_LOOP          220  'to 220'
              204  JUMP_BACK           180  'to 180'

 L. 454       206  LOAD_FAST                'default'
              208  POP_JUMP_IF_FALSE   216  'to 216'
              210  LOAD_FAST                'default'
              212  CALL_FUNCTION_0       0  ''
              214  JUMP_FORWARD        218  'to 218'
            216_0  COME_FROM           208  '208'
              216  LOAD_CONST               None
            218_0  COME_FROM           214  '214'
              218  STORE_FAST               'value'

 L. 455       220  LOAD_GLOBAL              setattr
              222  LOAD_DEREF               'self'
              224  LOAD_ATTR                metadata
              226  LOAD_FAST                'option'
              228  LOAD_FAST                'value'
              230  CALL_FUNCTION_3       3  ''
              232  POP_TOP          
              234  JUMP_BACK           160  'to 160'

 L. 457       236  LOAD_DEREF               'self'
              238  LOAD_METHOD              _normalize_version

 L. 458       240  LOAD_DEREF               'self'
              242  LOAD_METHOD              _validate_version
              244  LOAD_DEREF               'self'
              246  LOAD_ATTR                metadata
              248  LOAD_ATTR                version
              250  CALL_METHOD_1         1  ''

 L. 457       252  CALL_METHOD_1         1  ''
              254  LOAD_DEREF               'self'
              256  LOAD_ATTR                metadata
              258  STORE_ATTR               version

 L. 459       260  LOAD_DEREF               'self'
              262  LOAD_METHOD              _finalize_requires
              264  CALL_METHOD_0         0  ''
              266  POP_TOP          

Parse error at or near `LOAD_DICTCOMP' instruction at offset 130

    @staticmethod
    def _normalize_version--- This code section failed: ---

 L. 463         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'version'
                4  LOAD_GLOBAL              setuptools
                6  LOAD_ATTR                sic
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_TRUE     20  'to 20'
               12  LOAD_FAST                'version'
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE    24  'to 24'
             20_0  COME_FROM            10  '10'

 L. 464        20  LOAD_FAST                'version'
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L. 466        24  LOAD_GLOBAL              str
               26  LOAD_GLOBAL              packaging
               28  LOAD_ATTR                version
               30  LOAD_METHOD              Version
               32  LOAD_FAST                'version'
               34  CALL_METHOD_1         1  ''
               36  CALL_FUNCTION_1       1  ''
               38  STORE_FAST               'normalized'

 L. 467        40  LOAD_FAST                'version'
               42  LOAD_FAST                'normalized'
               44  COMPARE_OP               !=
               46  POP_JUMP_IF_FALSE    80  'to 80'

 L. 468        48  LOAD_STR                 "Normalizing '{version}' to '{normalized}'"
               50  STORE_FAST               'tmpl'

 L. 469        52  LOAD_GLOBAL              warnings
               54  LOAD_METHOD              warn
               56  LOAD_FAST                'tmpl'
               58  LOAD_ATTR                format
               60  BUILD_TUPLE_0         0 
               62  BUILD_MAP_0           0 
               64  LOAD_GLOBAL              locals
               66  CALL_FUNCTION_0       0  ''
               68  <164>                 1  ''
               70  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               72  CALL_METHOD_1         1  ''
               74  POP_TOP          

 L. 470        76  LOAD_FAST                'normalized'
               78  RETURN_VALUE     
             80_0  COME_FROM            46  '46'

 L. 471        80  LOAD_FAST                'version'
               82  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @staticmethod
    def _validate_version--- This code section failed: ---

 L. 475         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'version'
                4  LOAD_GLOBAL              numbers
                6  LOAD_ATTR                Number
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 477        12  LOAD_GLOBAL              str
               14  LOAD_FAST                'version'
               16  CALL_FUNCTION_1       1  ''
               18  STORE_FAST               'version'
             20_0  COME_FROM            10  '10'

 L. 479        20  LOAD_FAST                'version'
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    96  'to 96'

 L. 480        28  SETUP_FINALLY        46  'to 46'

 L. 481        30  LOAD_GLOBAL              packaging
               32  LOAD_ATTR                version
               34  LOAD_METHOD              Version
               36  LOAD_FAST                'version'
               38  CALL_METHOD_1         1  ''
               40  POP_TOP          
               42  POP_BLOCK        
               44  JUMP_FORWARD         96  'to 96'
             46_0  COME_FROM_FINALLY    28  '28'

 L. 482        46  DUP_TOP          
               48  LOAD_GLOBAL              packaging
               50  LOAD_ATTR                version
               52  LOAD_ATTR                InvalidVersion
               54  LOAD_GLOBAL              TypeError
               56  BUILD_TUPLE_2         2 
               58  <121>                94  ''
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L. 483        66  LOAD_GLOBAL              warnings
               68  LOAD_METHOD              warn

 L. 484        70  LOAD_STR                 'The version specified (%r) is an invalid version, this may not work as expected with newer versions of setuptools, pip, and PyPI. Please see PEP 440 for more details.'

 L. 487        72  LOAD_FAST                'version'

 L. 484        74  BINARY_MODULO    

 L. 483        76  CALL_METHOD_1         1  ''
               78  POP_TOP          

 L. 489        80  LOAD_GLOBAL              setuptools
               82  LOAD_METHOD              sic
               84  LOAD_FAST                'version'
               86  CALL_METHOD_1         1  ''
               88  ROT_FOUR         
               90  POP_EXCEPT       
               92  RETURN_VALUE     
               94  <48>             
             96_0  COME_FROM            44  '44'
             96_1  COME_FROM            26  '26'

 L. 490        96  LOAD_FAST                'version'
               98  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 24

    def _finalize_requires(self):
        """
        Set `metadata.python_requires` and fix environment markers
        in `install_requires` and `extras_require`.
        """
        if getattr(self, 'python_requires', None):
            self.metadata.python_requires = self.python_requires
        if getattr(self, 'extras_require', None):
            for extra in self.extras_require.keys():
                extra = extra.split(':')[0]
                if extra:
                    self.metadata.provides_extras.add(extra)

        self._convert_extras_requirements()
        self._move_install_requirements_markers()

    def _convert_extras_requirements(self):
        """
        Convert requirements in `extras_require` of the form
        `"extra": ["barbazquux; {marker}"]` to
        `"extra:{marker}": ["barbazquux"]`.
        """
        spec_ext_reqs = getattr(self, 'extras_require', None) or {}
        self._tmp_extras_require = defaultdict(list)
        for section, v in spec_ext_reqs.items():
            self._tmp_extras_require[section]
            for r in pkg_resources.parse_requirements(v):
                suffix = self._suffix_for(r)
                self._tmp_extras_require[(section + suffix)].append(r)

    @staticmethod
    def _suffix_for(req):
        """
        For a requirement, return the 'extras_require' suffix for
        that requirement.
        """
        if req.marker:
            return ':' + str(req.marker)
        return ''

    def _move_install_requirements_markers(self):
        """
        Move requirements in `install_requires` that are using environment
        markers `extras_require`.
        """

        def is_simple_req(req):
            return not req.marker

        spec_inst_reqs = getattr(self, 'install_requires', None) or ()
        inst_reqs = list(pkg_resources.parse_requirements(spec_inst_reqs))
        simple_reqs = filteris_simple_reqinst_reqs
        complex_reqs = itertools.filterfalse(is_simple_req, inst_reqs)
        self.install_requires = list(mapstrsimple_reqs)
        for r in complex_reqs:
            self._tmp_extras_require[(':' + str(r.marker))].append(r)
        else:
            self.extras_require = dict(((
             k, [str(r) for r in mapself._clean_reqv]) for k, v in self._tmp_extras_require.items()))

    def _clean_req(self, req):
        """
        Given a Requirement, remove environment markers and return it.
        """
        req.marker = None
        return req

    def _parse_config_files--- This code section failed: ---

 L. 575         0  LOAD_CONST               0
                2  LOAD_CONST               ('ConfigParser',)
                4  IMPORT_NAME              configparser
                6  IMPORT_FROM              ConfigParser
                8  STORE_FAST               'ConfigParser'
               10  POP_TOP          

 L. 578        12  LOAD_GLOBAL              sys
               14  LOAD_ATTR                prefix
               16  LOAD_GLOBAL              sys
               18  LOAD_ATTR                base_prefix
               20  COMPARE_OP               ==
               22  POP_JUMP_IF_FALSE    28  'to 28'
               24  BUILD_LIST_0          0 
               26  JUMP_FORWARD         34  'to 34'
             28_0  COME_FROM            22  '22'
               28  BUILD_LIST_0          0 
               30  LOAD_CONST               ('install-base', 'install-platbase', 'install-lib', 'install-platlib', 'install-purelib', 'install-headers', 'install-scripts', 'install-data', 'prefix', 'exec-prefix', 'home', 'user', 'root')
               32  CALL_FINALLY         35  'to 35'
             34_0  COME_FROM            26  '26'
               34  STORE_FAST               'ignore_options'

 L. 585        36  LOAD_GLOBAL              frozenset
               38  LOAD_FAST                'ignore_options'
               40  CALL_FUNCTION_1       1  ''
               42  STORE_FAST               'ignore_options'

 L. 587        44  LOAD_FAST                'filenames'
               46  LOAD_CONST               None
               48  <117>                 0  ''
               50  POP_JUMP_IF_FALSE    60  'to 60'

 L. 588        52  LOAD_FAST                'self'
               54  LOAD_METHOD              find_config_files
               56  CALL_METHOD_0         0  ''
               58  STORE_FAST               'filenames'
             60_0  COME_FROM            50  '50'

 L. 590        60  LOAD_GLOBAL              DEBUG
               62  POP_JUMP_IF_FALSE    74  'to 74'

 L. 591        64  LOAD_FAST                'self'
               66  LOAD_METHOD              announce
               68  LOAD_STR                 'Distribution.parse_config_files():'
               70  CALL_METHOD_1         1  ''
               72  POP_TOP          
             74_0  COME_FROM            62  '62'

 L. 593        74  LOAD_FAST                'ConfigParser'
               76  CALL_FUNCTION_0       0  ''
               78  STORE_FAST               'parser'

 L. 594        80  LOAD_GLOBAL              str
               82  LOAD_FAST                'parser'
               84  STORE_ATTR               optionxform

 L. 595        86  LOAD_FAST                'filenames'
               88  GET_ITER         
               90  FOR_ITER            298  'to 298'
               92  STORE_FAST               'filename'

 L. 596        94  LOAD_GLOBAL              io
               96  LOAD_ATTR                open
               98  LOAD_FAST                'filename'
              100  LOAD_STR                 'utf-8'
              102  LOAD_CONST               ('encoding',)
              104  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              106  SETUP_WITH          162  'to 162'
              108  STORE_FAST               'reader'

 L. 597       110  LOAD_GLOBAL              DEBUG
              112  POP_JUMP_IF_FALSE   138  'to 138'

 L. 598       114  LOAD_FAST                'self'
              116  LOAD_METHOD              announce
              118  LOAD_STR                 '  reading {filename}'
              120  LOAD_ATTR                format
              122  BUILD_TUPLE_0         0 
              124  BUILD_MAP_0           0 
              126  LOAD_GLOBAL              locals
              128  CALL_FUNCTION_0       0  ''
              130  <164>                 1  ''
              132  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              134  CALL_METHOD_1         1  ''
              136  POP_TOP          
            138_0  COME_FROM           112  '112'

 L. 599       138  LOAD_FAST                'parser'
              140  LOAD_METHOD              read_file
              142  LOAD_FAST                'reader'
              144  CALL_METHOD_1         1  ''
              146  POP_TOP          
              148  POP_BLOCK        
              150  LOAD_CONST               None
              152  DUP_TOP          
              154  DUP_TOP          
              156  CALL_FUNCTION_3       3  ''
              158  POP_TOP          
              160  JUMP_FORWARD        178  'to 178'
            162_0  COME_FROM_WITH      106  '106'
              162  <49>             
              164  POP_JUMP_IF_TRUE    168  'to 168'
              166  <48>             
            168_0  COME_FROM           164  '164'
              168  POP_TOP          
              170  POP_TOP          
              172  POP_TOP          
              174  POP_EXCEPT       
              176  POP_TOP          
            178_0  COME_FROM           160  '160'

 L. 600       178  LOAD_FAST                'parser'
              180  LOAD_METHOD              sections
              182  CALL_METHOD_0         0  ''
              184  GET_ITER         
              186  FOR_ITER            288  'to 288'
              188  STORE_FAST               'section'

 L. 601       190  LOAD_FAST                'parser'
              192  LOAD_METHOD              options
              194  LOAD_FAST                'section'
              196  CALL_METHOD_1         1  ''
              198  STORE_FAST               'options'

 L. 602       200  LOAD_FAST                'self'
              202  LOAD_METHOD              get_option_dict
              204  LOAD_FAST                'section'
              206  CALL_METHOD_1         1  ''
              208  STORE_FAST               'opt_dict'

 L. 604       210  LOAD_FAST                'options'
              212  GET_ITER         
            214_0  COME_FROM           224  '224'
              214  FOR_ITER            286  'to 286'
              216  STORE_FAST               'opt'

 L. 605       218  LOAD_FAST                'opt'
              220  LOAD_STR                 '__name__'
              222  COMPARE_OP               ==
              224  POP_JUMP_IF_TRUE    214  'to 214'
              226  LOAD_FAST                'opt'
              228  LOAD_FAST                'ignore_options'
              230  <118>                 0  ''
              232  POP_JUMP_IF_FALSE   236  'to 236'

 L. 606       234  JUMP_BACK           214  'to 214'
            236_0  COME_FROM           232  '232'

 L. 608       236  LOAD_FAST                'parser'
              238  LOAD_METHOD              get
              240  LOAD_FAST                'section'
              242  LOAD_FAST                'opt'
              244  CALL_METHOD_2         2  ''
              246  STORE_FAST               'val'

 L. 609       248  LOAD_FAST                'self'
              250  LOAD_METHOD              warn_dash_deprecation
              252  LOAD_FAST                'opt'
              254  LOAD_FAST                'section'
              256  CALL_METHOD_2         2  ''
              258  STORE_FAST               'opt'

 L. 610       260  LOAD_FAST                'self'
              262  LOAD_METHOD              make_option_lowercase
              264  LOAD_FAST                'opt'
              266  LOAD_FAST                'section'
              268  CALL_METHOD_2         2  ''
              270  STORE_FAST               'opt'

 L. 611       272  LOAD_FAST                'filename'
              274  LOAD_FAST                'val'
              276  BUILD_TUPLE_2         2 
              278  LOAD_FAST                'opt_dict'
              280  LOAD_FAST                'opt'
              282  STORE_SUBSCR     
              284  JUMP_BACK           214  'to 214'
              286  JUMP_BACK           186  'to 186'

 L. 615       288  LOAD_FAST                'parser'
              290  LOAD_METHOD              __init__
              292  CALL_METHOD_0         0  ''
              294  POP_TOP          
              296  JUMP_BACK            90  'to 90'

 L. 617       298  LOAD_STR                 'global'
              300  LOAD_FAST                'self'
              302  LOAD_ATTR                command_options
              304  <118>                 1  ''
          306_308  POP_JUMP_IF_FALSE   314  'to 314'

 L. 618       310  LOAD_CONST               None
              312  RETURN_VALUE     
            314_0  COME_FROM           306  '306'

 L. 623       314  LOAD_FAST                'self'
              316  LOAD_ATTR                command_options
              318  LOAD_STR                 'global'
              320  BINARY_SUBSCR    
              322  LOAD_METHOD              items
              324  CALL_METHOD_0         0  ''
              326  GET_ITER         
              328  FOR_ITER            464  'to 464'
              330  UNPACK_SEQUENCE_2     2 
              332  STORE_FAST               'opt'
              334  UNPACK_SEQUENCE_2     2 
              336  STORE_FAST               'src'
              338  STORE_FAST               'val'

 L. 624       340  LOAD_FAST                'self'
              342  LOAD_ATTR                negative_opt
              344  LOAD_METHOD              get
              346  LOAD_FAST                'opt'
              348  CALL_METHOD_1         1  ''
              350  STORE_FAST               'alias'

 L. 625       352  LOAD_FAST                'alias'
          354_356  POP_JUMP_IF_FALSE   370  'to 370'

 L. 626       358  LOAD_GLOBAL              strtobool
              360  LOAD_FAST                'val'
              362  CALL_FUNCTION_1       1  ''
              364  UNARY_NOT        
              366  STORE_FAST               'val'
              368  JUMP_FORWARD        388  'to 388'
            370_0  COME_FROM           354  '354'

 L. 627       370  LOAD_FAST                'opt'
              372  LOAD_CONST               ('verbose', 'dry_run')
              374  <118>                 0  ''
          376_378  POP_JUMP_IF_FALSE   388  'to 388'

 L. 628       380  LOAD_GLOBAL              strtobool
              382  LOAD_FAST                'val'
              384  CALL_FUNCTION_1       1  ''
              386  STORE_FAST               'val'
            388_0  COME_FROM           376  '376'
            388_1  COME_FROM           368  '368'

 L. 630       388  SETUP_FINALLY       412  'to 412'

 L. 631       390  LOAD_GLOBAL              setattr
              392  LOAD_FAST                'self'
              394  LOAD_FAST                'alias'
          396_398  JUMP_IF_TRUE_OR_POP   402  'to 402'
              400  LOAD_FAST                'opt'
            402_0  COME_FROM           396  '396'
              402  LOAD_FAST                'val'
              404  CALL_FUNCTION_3       3  ''
              406  POP_TOP          
              408  POP_BLOCK        
              410  JUMP_BACK           328  'to 328'
            412_0  COME_FROM_FINALLY   388  '388'

 L. 632       412  DUP_TOP          
              414  LOAD_GLOBAL              ValueError
          416_418  <121>               458  ''
              420  POP_TOP          
              422  STORE_FAST               'e'
              424  POP_TOP          
              426  SETUP_FINALLY       450  'to 450'

 L. 633       428  LOAD_GLOBAL              DistutilsOptionError
              430  LOAD_FAST                'e'
              432  CALL_FUNCTION_1       1  ''
              434  LOAD_FAST                'e'
              436  RAISE_VARARGS_2       2  'exception instance with __cause__'
              438  POP_BLOCK        
              440  POP_EXCEPT       
              442  LOAD_CONST               None
              444  STORE_FAST               'e'
              446  DELETE_FAST              'e'
              448  JUMP_BACK           328  'to 328'
            450_0  COME_FROM_FINALLY   426  '426'
              450  LOAD_CONST               None
              452  STORE_FAST               'e'
              454  DELETE_FAST              'e'
              456  <48>             
              458  <48>             
          460_462  JUMP_BACK           328  'to 328'

Parse error at or near `CALL_FINALLY' instruction at offset 32

    def warn_dash_deprecation--- This code section failed: ---

 L. 636         0  LOAD_FAST                'section'
                2  LOAD_CONST               ('options.extras_require', 'options.data_files')
                4  <118>                 0  ''
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 639         8  LOAD_FAST                'opt'
               10  RETURN_VALUE     
             12_0  COME_FROM             6  '6'

 L. 641        12  LOAD_FAST                'opt'
               14  LOAD_METHOD              replace
               16  LOAD_STR                 '-'
               18  LOAD_STR                 '_'
               20  CALL_METHOD_2         2  ''
               22  STORE_FAST               'underscore_opt'

 L. 642        24  LOAD_GLOBAL              distutils
               26  LOAD_ATTR                command
               28  LOAD_ATTR                __all__
               30  LOAD_GLOBAL              setuptools
               32  LOAD_ATTR                command
               34  LOAD_ATTR                __all__
               36  BINARY_ADD       
               38  STORE_FAST               'commands'

 L. 643        40  LOAD_FAST                'section'
               42  LOAD_METHOD              startswith
               44  LOAD_STR                 'options'
               46  CALL_METHOD_1         1  ''
               48  POP_JUMP_IF_TRUE     70  'to 70'
               50  LOAD_FAST                'section'
               52  LOAD_STR                 'metadata'
               54  COMPARE_OP               !=
               56  POP_JUMP_IF_FALSE    70  'to 70'

 L. 644        58  LOAD_FAST                'section'
               60  LOAD_FAST                'commands'
               62  <118>                 1  ''

 L. 643        64  POP_JUMP_IF_FALSE    70  'to 70'

 L. 645        66  LOAD_FAST                'underscore_opt'
               68  RETURN_VALUE     
             70_0  COME_FROM            64  '64'
             70_1  COME_FROM            56  '56'
             70_2  COME_FROM            48  '48'

 L. 647        70  LOAD_STR                 '-'
               72  LOAD_FAST                'opt'
               74  <118>                 0  ''
               76  POP_JUMP_IF_FALSE    96  'to 96'

 L. 648        78  LOAD_GLOBAL              warnings
               80  LOAD_METHOD              warn

 L. 649        82  LOAD_STR                 "Usage of dash-separated '%s' will not be supported in future versions. Please use the underscore name '%s' instead"

 L. 651        84  LOAD_FAST                'opt'
               86  LOAD_FAST                'underscore_opt'
               88  BUILD_TUPLE_2         2 

 L. 649        90  BINARY_MODULO    

 L. 648        92  CALL_METHOD_1         1  ''
               94  POP_TOP          
             96_0  COME_FROM            76  '76'

 L. 652        96  LOAD_FAST                'underscore_opt'
               98  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def make_option_lowercase(self, opt, section):
        if section != 'metadata' or opt.islower():
            return opt
        lowercase_opt = opt.lower()
        warnings.warn("Usage of uppercase key '%s' in '%s' will be deprecated in future versions. Please use lowercase '%s' instead" % (
         opt, section, lowercase_opt))
        return lowercase_opt

    def _set_command_options--- This code section failed: ---

 L. 679         0  LOAD_FAST                'command_obj'
                2  LOAD_METHOD              get_command_name
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'command_name'

 L. 680         8  LOAD_FAST                'option_dict'
               10  LOAD_CONST               None
               12  <117>                 0  ''
               14  POP_JUMP_IF_FALSE    26  'to 26'

 L. 681        16  LOAD_FAST                'self'
               18  LOAD_METHOD              get_option_dict
               20  LOAD_FAST                'command_name'
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'option_dict'
             26_0  COME_FROM            14  '14'

 L. 683        26  LOAD_GLOBAL              DEBUG
               28  POP_JUMP_IF_FALSE    44  'to 44'

 L. 684        30  LOAD_FAST                'self'
               32  LOAD_METHOD              announce
               34  LOAD_STR                 "  setting options for '%s' command:"
               36  LOAD_FAST                'command_name'
               38  BINARY_MODULO    
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          
             44_0  COME_FROM            28  '28'

 L. 685        44  LOAD_FAST                'option_dict'
               46  LOAD_METHOD              items
               48  CALL_METHOD_0         0  ''
               50  GET_ITER         
            52_54  FOR_ITER            344  'to 344'
               56  UNPACK_SEQUENCE_2     2 
               58  STORE_FAST               'option'
               60  UNPACK_SEQUENCE_2     2 
               62  STORE_FAST               'source'
               64  STORE_FAST               'value'

 L. 686        66  LOAD_GLOBAL              DEBUG
               68  POP_JUMP_IF_FALSE    90  'to 90'

 L. 687        70  LOAD_FAST                'self'
               72  LOAD_METHOD              announce
               74  LOAD_STR                 '    %s = %s (from %s)'
               76  LOAD_FAST                'option'
               78  LOAD_FAST                'value'

 L. 688        80  LOAD_FAST                'source'

 L. 687        82  BUILD_TUPLE_3         3 
               84  BINARY_MODULO    
               86  CALL_METHOD_1         1  ''
               88  POP_TOP          
             90_0  COME_FROM            68  '68'

 L. 689        90  SETUP_FINALLY       112  'to 112'

 L. 690        92  LOAD_LISTCOMP            '<code_object <listcomp>>'
               94  LOAD_STR                 'Distribution._set_command_options.<locals>.<listcomp>'
               96  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 691        98  LOAD_FAST                'command_obj'
              100  LOAD_ATTR                boolean_options

 L. 690       102  GET_ITER         
              104  CALL_FUNCTION_1       1  ''
              106  STORE_FAST               'bool_opts'
              108  POP_BLOCK        
              110  JUMP_FORWARD        134  'to 134'
            112_0  COME_FROM_FINALLY    90  '90'

 L. 692       112  DUP_TOP          
              114  LOAD_GLOBAL              AttributeError
              116  <121>               132  ''
              118  POP_TOP          
              120  POP_TOP          
              122  POP_TOP          

 L. 693       124  BUILD_LIST_0          0 
              126  STORE_FAST               'bool_opts'
              128  POP_EXCEPT       
              130  JUMP_FORWARD        134  'to 134'
              132  <48>             
            134_0  COME_FROM           130  '130'
            134_1  COME_FROM           110  '110'

 L. 694       134  SETUP_FINALLY       146  'to 146'

 L. 695       136  LOAD_FAST                'command_obj'
              138  LOAD_ATTR                negative_opt
              140  STORE_FAST               'neg_opt'
              142  POP_BLOCK        
              144  JUMP_FORWARD        168  'to 168'
            146_0  COME_FROM_FINALLY   134  '134'

 L. 696       146  DUP_TOP          
              148  LOAD_GLOBAL              AttributeError
              150  <121>               166  ''
              152  POP_TOP          
              154  POP_TOP          
              156  POP_TOP          

 L. 697       158  BUILD_MAP_0           0 
              160  STORE_FAST               'neg_opt'
              162  POP_EXCEPT       
              164  JUMP_FORWARD        168  'to 168'
              166  <48>             
            168_0  COME_FROM           164  '164'
            168_1  COME_FROM           144  '144'

 L. 699       168  SETUP_FINALLY       294  'to 294'

 L. 700       170  LOAD_GLOBAL              isinstance
              172  LOAD_FAST                'value'
              174  LOAD_GLOBAL              str
              176  CALL_FUNCTION_2       2  ''
              178  STORE_FAST               'is_string'

 L. 701       180  LOAD_FAST                'option'
              182  LOAD_FAST                'neg_opt'
              184  <118>                 0  ''
              186  POP_JUMP_IF_FALSE   216  'to 216'
              188  LOAD_FAST                'is_string'
              190  POP_JUMP_IF_FALSE   216  'to 216'

 L. 702       192  LOAD_GLOBAL              setattr
              194  LOAD_FAST                'command_obj'
              196  LOAD_FAST                'neg_opt'
              198  LOAD_FAST                'option'
              200  BINARY_SUBSCR    
              202  LOAD_GLOBAL              strtobool
              204  LOAD_FAST                'value'
              206  CALL_FUNCTION_1       1  ''
              208  UNARY_NOT        
              210  CALL_FUNCTION_3       3  ''
              212  POP_TOP          
              214  JUMP_FORWARD        290  'to 290'
            216_0  COME_FROM           190  '190'
            216_1  COME_FROM           186  '186'

 L. 703       216  LOAD_FAST                'option'
              218  LOAD_FAST                'bool_opts'
              220  <118>                 0  ''
              222  POP_JUMP_IF_FALSE   246  'to 246'
              224  LOAD_FAST                'is_string'
              226  POP_JUMP_IF_FALSE   246  'to 246'

 L. 704       228  LOAD_GLOBAL              setattr
              230  LOAD_FAST                'command_obj'
              232  LOAD_FAST                'option'
              234  LOAD_GLOBAL              strtobool
              236  LOAD_FAST                'value'
              238  CALL_FUNCTION_1       1  ''
              240  CALL_FUNCTION_3       3  ''
              242  POP_TOP          
              244  JUMP_FORWARD        290  'to 290'
            246_0  COME_FROM           226  '226'
            246_1  COME_FROM           222  '222'

 L. 705       246  LOAD_GLOBAL              hasattr
              248  LOAD_FAST                'command_obj'
              250  LOAD_FAST                'option'
              252  CALL_FUNCTION_2       2  ''
          254_256  POP_JUMP_IF_FALSE   272  'to 272'

 L. 706       258  LOAD_GLOBAL              setattr
              260  LOAD_FAST                'command_obj'
              262  LOAD_FAST                'option'
              264  LOAD_FAST                'value'
              266  CALL_FUNCTION_3       3  ''
              268  POP_TOP          
              270  JUMP_FORWARD        290  'to 290'
            272_0  COME_FROM           254  '254'

 L. 708       272  LOAD_GLOBAL              DistutilsOptionError

 L. 709       274  LOAD_STR                 "error in %s: command '%s' has no such option '%s'"

 L. 710       276  LOAD_FAST                'source'
              278  LOAD_FAST                'command_name'
              280  LOAD_FAST                'option'
              282  BUILD_TUPLE_3         3 

 L. 709       284  BINARY_MODULO    

 L. 708       286  CALL_FUNCTION_1       1  ''
              288  RAISE_VARARGS_1       1  'exception instance'
            290_0  COME_FROM           270  '270'
            290_1  COME_FROM           244  '244'
            290_2  COME_FROM           214  '214'
              290  POP_BLOCK        
              292  JUMP_BACK            52  'to 52'
            294_0  COME_FROM_FINALLY   168  '168'

 L. 711       294  DUP_TOP          
              296  LOAD_GLOBAL              ValueError
          298_300  <121>               340  ''
              302  POP_TOP          
              304  STORE_FAST               'e'
              306  POP_TOP          
              308  SETUP_FINALLY       332  'to 332'

 L. 712       310  LOAD_GLOBAL              DistutilsOptionError
              312  LOAD_FAST                'e'
              314  CALL_FUNCTION_1       1  ''
              316  LOAD_FAST                'e'
              318  RAISE_VARARGS_2       2  'exception instance with __cause__'
              320  POP_BLOCK        
              322  POP_EXCEPT       
              324  LOAD_CONST               None
              326  STORE_FAST               'e'
              328  DELETE_FAST              'e'
              330  JUMP_BACK            52  'to 52'
            332_0  COME_FROM_FINALLY   308  '308'
              332  LOAD_CONST               None
              334  STORE_FAST               'e'
              336  DELETE_FAST              'e'
              338  <48>             
              340  <48>             
              342  JUMP_BACK            52  'to 52'

Parse error at or near `<117>' instruction at offset 12

    def parse_config_files(self, filenames=None, ignore_option_errors=False):
        """Parses configuration files from various levels
        and loads configuration.

        """
        self._parse_config_files(filenames=filenames)
        parse_configuration(self, (self.command_options), ignore_option_errors=ignore_option_errors)
        self._finalize_requires()

    def fetch_build_eggs(self, requires):
        """Resolve pre-setup requirements"""
        resolved_dists = pkg_resources.working_set.resolve((pkg_resources.parse_requirements(requires)),
          installer=(self.fetch_build_egg),
          replace_conflicting=True)
        for dist in resolved_dists:
            pkg_resources.working_set.add(dist, replace=True)
        else:
            return resolved_dists

    def finalize_options(self):
        """
        Allow plugins to apply arbitrary operations to the
        distribution. Each hook may optionally define a 'order'
        to influence the order of execution. Smaller numbers
        go first and the default is 0.
        """
        group = 'setuptools.finalize_distribution_options'

        def by_order(hook):
            return getattr(hook, 'order', 0)

        eps = map(lambda e: e.load())pkg_resources.iter_entry_points(group)
        for ep in sorted(eps, key=by_order):
            ep(self)

    def _finalize_setup_keywords--- This code section failed: ---

 L. 752         0  LOAD_GLOBAL              pkg_resources
                2  LOAD_METHOD              iter_entry_points
                4  LOAD_STR                 'distutils.setup_keywords'
                6  CALL_METHOD_1         1  ''
                8  GET_ITER         
             10_0  COME_FROM            34  '34'
               10  FOR_ITER             70  'to 70'
               12  STORE_FAST               'ep'

 L. 753        14  LOAD_GLOBAL              getattr
               16  LOAD_FAST                'self'
               18  LOAD_FAST                'ep'
               20  LOAD_ATTR                name
               22  LOAD_CONST               None
               24  CALL_FUNCTION_3       3  ''
               26  STORE_FAST               'value'

 L. 754        28  LOAD_FAST                'value'
               30  LOAD_CONST               None
               32  <117>                 1  ''
               34  POP_JUMP_IF_FALSE    10  'to 10'

 L. 755        36  LOAD_FAST                'ep'
               38  LOAD_ATTR                require
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                fetch_build_egg
               44  LOAD_CONST               ('installer',)
               46  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               48  POP_TOP          

 L. 756        50  LOAD_FAST                'ep'
               52  LOAD_METHOD              load
               54  CALL_METHOD_0         0  ''
               56  LOAD_FAST                'self'
               58  LOAD_FAST                'ep'
               60  LOAD_ATTR                name
               62  LOAD_FAST                'value'
               64  CALL_FUNCTION_3       3  ''
               66  POP_TOP          
               68  JUMP_BACK            10  'to 10'

Parse error at or near `<117>' instruction at offset 32

    def _finalize_2to3_doctests(self):
        if getattr(self, 'convert_2to3_doctests', None):
            self.convert_2to3_doctests = [os.path.abspath(p) for p in self.convert_2to3_doctests]
        else:
            self.convert_2to3_doctests = []

    def get_egg_cache_dir--- This code section failed: ---

 L. 769         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              join
                6  LOAD_GLOBAL              os
                8  LOAD_ATTR                curdir
               10  LOAD_STR                 '.eggs'
               12  CALL_METHOD_2         2  ''
               14  STORE_FAST               'egg_cache_dir'

 L. 770        16  LOAD_GLOBAL              os
               18  LOAD_ATTR                path
               20  LOAD_METHOD              exists
               22  LOAD_FAST                'egg_cache_dir'
               24  CALL_METHOD_1         1  ''
               26  POP_JUMP_IF_TRUE    134  'to 134'

 L. 771        28  LOAD_GLOBAL              os
               30  LOAD_METHOD              mkdir
               32  LOAD_FAST                'egg_cache_dir'
               34  CALL_METHOD_1         1  ''
               36  POP_TOP          

 L. 772        38  LOAD_GLOBAL              windows_support
               40  LOAD_METHOD              hide_file
               42  LOAD_FAST                'egg_cache_dir'
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          

 L. 773        48  LOAD_GLOBAL              os
               50  LOAD_ATTR                path
               52  LOAD_METHOD              join
               54  LOAD_FAST                'egg_cache_dir'
               56  LOAD_STR                 'README.txt'
               58  CALL_METHOD_2         2  ''
               60  STORE_FAST               'readme_txt_filename'

 L. 774        62  LOAD_GLOBAL              open
               64  LOAD_FAST                'readme_txt_filename'
               66  LOAD_STR                 'w'
               68  CALL_FUNCTION_2       2  ''
               70  SETUP_WITH          118  'to 118'
               72  STORE_FAST               'f'

 L. 775        74  LOAD_FAST                'f'
               76  LOAD_METHOD              write
               78  LOAD_STR                 'This directory contains eggs that were downloaded by setuptools to build, test, and run plug-ins.\n\n'
               80  CALL_METHOD_1         1  ''
               82  POP_TOP          

 L. 777        84  LOAD_FAST                'f'
               86  LOAD_METHOD              write
               88  LOAD_STR                 'This directory caches those eggs to prevent repeated downloads.\n\n'
               90  CALL_METHOD_1         1  ''
               92  POP_TOP          

 L. 779        94  LOAD_FAST                'f'
               96  LOAD_METHOD              write
               98  LOAD_STR                 'However, it is safe to delete this directory.\n\n'
              100  CALL_METHOD_1         1  ''
              102  POP_TOP          
              104  POP_BLOCK        
              106  LOAD_CONST               None
              108  DUP_TOP          
              110  DUP_TOP          
              112  CALL_FUNCTION_3       3  ''
              114  POP_TOP          
              116  JUMP_FORWARD        134  'to 134'
            118_0  COME_FROM_WITH       70  '70'
              118  <49>             
              120  POP_JUMP_IF_TRUE    124  'to 124'
              122  <48>             
            124_0  COME_FROM           120  '120'
              124  POP_TOP          
              126  POP_TOP          
              128  POP_TOP          
              130  POP_EXCEPT       
              132  POP_TOP          
            134_0  COME_FROM           116  '116'
            134_1  COME_FROM            26  '26'

 L. 781       134  LOAD_FAST                'egg_cache_dir'
              136  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 108

    def fetch_build_egg(self, req):
        """Fetch an egg needed for building"""
        from setuptools.installer import fetch_build_egg
        return fetch_build_eggselfreq

    def get_command_class--- This code section failed: ---

 L. 790         0  LOAD_FAST                'command'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                cmdclass
                6  <118>                 0  ''
                8  POP_JUMP_IF_FALSE    20  'to 20'

 L. 791        10  LOAD_FAST                'self'
               12  LOAD_ATTR                cmdclass
               14  LOAD_FAST                'command'
               16  BINARY_SUBSCR    
               18  RETURN_VALUE     
             20_0  COME_FROM             8  '8'

 L. 793        20  LOAD_GLOBAL              pkg_resources
               22  LOAD_METHOD              iter_entry_points
               24  LOAD_STR                 'distutils.commands'
               26  LOAD_FAST                'command'
               28  CALL_METHOD_2         2  ''
               30  STORE_FAST               'eps'

 L. 794        32  LOAD_FAST                'eps'
               34  GET_ITER         
               36  FOR_ITER             80  'to 80'
               38  STORE_FAST               'ep'

 L. 795        40  LOAD_FAST                'ep'
               42  LOAD_ATTR                require
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                fetch_build_egg
               48  LOAD_CONST               ('installer',)
               50  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               52  POP_TOP          

 L. 796        54  LOAD_FAST                'ep'
               56  LOAD_METHOD              load
               58  CALL_METHOD_0         0  ''
               60  DUP_TOP          
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                cmdclass
               66  LOAD_FAST                'command'
               68  STORE_SUBSCR     
               70  STORE_FAST               'cmdclass'

 L. 797        72  LOAD_FAST                'cmdclass'
               74  ROT_TWO          
               76  POP_TOP          
               78  RETURN_VALUE     

 L. 799        80  LOAD_GLOBAL              _Distribution
               82  LOAD_METHOD              get_command_class
               84  LOAD_FAST                'self'
               86  LOAD_FAST                'command'
               88  CALL_METHOD_2         2  ''
               90  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def print_commands--- This code section failed: ---

 L. 802         0  LOAD_GLOBAL              pkg_resources
                2  LOAD_METHOD              iter_entry_points
                4  LOAD_STR                 'distutils.commands'
                6  CALL_METHOD_1         1  ''
                8  GET_ITER         
             10_0  COME_FROM            24  '24'
               10  FOR_ITER             48  'to 48'
               12  STORE_FAST               'ep'

 L. 803        14  LOAD_FAST                'ep'
               16  LOAD_ATTR                name
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                cmdclass
               22  <118>                 1  ''
               24  POP_JUMP_IF_FALSE    10  'to 10'

 L. 805        26  LOAD_FAST                'ep'
               28  LOAD_METHOD              resolve
               30  CALL_METHOD_0         0  ''
               32  STORE_FAST               'cmdclass'

 L. 806        34  LOAD_FAST                'cmdclass'
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                cmdclass
               40  LOAD_FAST                'ep'
               42  LOAD_ATTR                name
               44  STORE_SUBSCR     
               46  JUMP_BACK            10  'to 10'

 L. 807        48  LOAD_GLOBAL              _Distribution
               50  LOAD_METHOD              print_commands
               52  LOAD_FAST                'self'
               54  CALL_METHOD_1         1  ''
               56  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 22

    def get_command_list--- This code section failed: ---

 L. 810         0  LOAD_GLOBAL              pkg_resources
                2  LOAD_METHOD              iter_entry_points
                4  LOAD_STR                 'distutils.commands'
                6  CALL_METHOD_1         1  ''
                8  GET_ITER         
             10_0  COME_FROM            24  '24'
               10  FOR_ITER             48  'to 48'
               12  STORE_FAST               'ep'

 L. 811        14  LOAD_FAST                'ep'
               16  LOAD_ATTR                name
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                cmdclass
               22  <118>                 1  ''
               24  POP_JUMP_IF_FALSE    10  'to 10'

 L. 813        26  LOAD_FAST                'ep'
               28  LOAD_METHOD              resolve
               30  CALL_METHOD_0         0  ''
               32  STORE_FAST               'cmdclass'

 L. 814        34  LOAD_FAST                'cmdclass'
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                cmdclass
               40  LOAD_FAST                'ep'
               42  LOAD_ATTR                name
               44  STORE_SUBSCR     
               46  JUMP_BACK            10  'to 10'

 L. 815        48  LOAD_GLOBAL              _Distribution
               50  LOAD_METHOD              get_command_list
               52  LOAD_FAST                'self'
               54  CALL_METHOD_1         1  ''
               56  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 22

    def include(self, **attrs):
        """Add items to distribution that are named in keyword arguments

        For example, 'dist.include(py_modules=["x"])' would add 'x' to
        the distribution's 'py_modules' attribute, if it was not already
        there.

        Currently, this method only supports inclusion for attributes that are
        lists or tuples.  If you need to add support for adding to other
        attributes in this or a subclass, you can add an '_include_X' method,
        where 'X' is the name of the attribute.  The method will be called with
        the value passed to 'include()'.  So, 'dist.include(foo={"bar":"baz"})'
        will try to call 'dist._include_foo({"bar":"baz"})', which can then
        handle whatever special inclusion logic is needed.
        """
        for k, v in attrs.items():
            include = getattr(self, '_include_' + k, None)
            if include:
                include(v)
            else:
                self._include_misc(k, v)

    def exclude_package(self, package):
        """Remove packages, modules, and extensions in named package"""
        pfx = package + '.'
        if self.packages:
            self.packages = [p for p in self.packages if p != package if not p.startswith(pfx)]
        if self.py_modules:
            self.py_modules = [p for p in self.py_modules if p != package if not p.startswith(pfx)]
        if self.ext_modules:
            self.ext_modules = [p for p in self.ext_modules if p.name != package if not p.name.startswith(pfx)]

    def has_contents_for(self, package):
        """Return true if 'exclude_package(package)' would do something"""
        pfx = package + '.'
        for p in self.iter_distribution_names():
            if p == package or p.startswith(pfx):
                return True

    def _exclude_misc--- This code section failed: ---

 L. 872         0  LOAD_GLOBAL              isinstance
                2  LOAD_DEREF               'value'
                4  LOAD_GLOBAL              sequence
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     26  'to 26'

 L. 873        10  LOAD_GLOBAL              DistutilsSetupError

 L. 874        12  LOAD_STR                 '%s: setting must be a list or tuple (%r)'
               14  LOAD_FAST                'name'
               16  LOAD_DEREF               'value'
               18  BUILD_TUPLE_2         2 
               20  BINARY_MODULO    

 L. 873        22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM             8  '8'

 L. 876        26  SETUP_FINALLY        42  'to 42'

 L. 877        28  LOAD_GLOBAL              getattr
               30  LOAD_FAST                'self'
               32  LOAD_FAST                'name'
               34  CALL_FUNCTION_2       2  ''
               36  STORE_FAST               'old'
               38  POP_BLOCK        
               40  JUMP_FORWARD         92  'to 92'
             42_0  COME_FROM_FINALLY    26  '26'

 L. 878        42  DUP_TOP          
               44  LOAD_GLOBAL              AttributeError
               46  <121>                90  ''
               48  POP_TOP          
               50  STORE_FAST               'e'
               52  POP_TOP          
               54  SETUP_FINALLY        82  'to 82'

 L. 879        56  LOAD_GLOBAL              DistutilsSetupError

 L. 880        58  LOAD_STR                 '%s: No such distribution setting'
               60  LOAD_FAST                'name'
               62  BINARY_MODULO    

 L. 879        64  CALL_FUNCTION_1       1  ''

 L. 881        66  LOAD_FAST                'e'

 L. 879        68  RAISE_VARARGS_2       2  'exception instance with __cause__'
               70  POP_BLOCK        
               72  POP_EXCEPT       
               74  LOAD_CONST               None
               76  STORE_FAST               'e'
               78  DELETE_FAST              'e'
               80  JUMP_FORWARD         92  'to 92'
             82_0  COME_FROM_FINALLY    54  '54'
               82  LOAD_CONST               None
               84  STORE_FAST               'e'
               86  DELETE_FAST              'e'
               88  <48>             
               90  <48>             
             92_0  COME_FROM            80  '80'
             92_1  COME_FROM            40  '40'

 L. 882        92  LOAD_FAST                'old'
               94  LOAD_CONST               None
               96  <117>                 1  ''
               98  POP_JUMP_IF_FALSE   124  'to 124'
              100  LOAD_GLOBAL              isinstance
              102  LOAD_FAST                'old'
              104  LOAD_GLOBAL              sequence
              106  CALL_FUNCTION_2       2  ''
              108  POP_JUMP_IF_TRUE    124  'to 124'

 L. 883       110  LOAD_GLOBAL              DistutilsSetupError

 L. 884       112  LOAD_FAST                'name'
              114  LOAD_STR                 ': this setting cannot be changed via include/exclude'
              116  BINARY_ADD       

 L. 883       118  CALL_FUNCTION_1       1  ''
              120  RAISE_VARARGS_1       1  'exception instance'
              122  JUMP_FORWARD        154  'to 154'
            124_0  COME_FROM           108  '108'
            124_1  COME_FROM            98  '98'

 L. 886       124  LOAD_FAST                'old'
              126  POP_JUMP_IF_FALSE   154  'to 154'

 L. 887       128  LOAD_GLOBAL              setattr
              130  LOAD_FAST                'self'
              132  LOAD_FAST                'name'
              134  LOAD_CLOSURE             'value'
              136  BUILD_TUPLE_1         1 
              138  LOAD_LISTCOMP            '<code_object <listcomp>>'
              140  LOAD_STR                 'Distribution._exclude_misc.<locals>.<listcomp>'
              142  MAKE_FUNCTION_8          'closure'
              144  LOAD_FAST                'old'
              146  GET_ITER         
              148  CALL_FUNCTION_1       1  ''
              150  CALL_FUNCTION_3       3  ''
              152  POP_TOP          
            154_0  COME_FROM           126  '126'
            154_1  COME_FROM           122  '122'

Parse error at or near `<121>' instruction at offset 46

    def _include_misc--- This code section failed: ---

 L. 892         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'value'
                4  LOAD_GLOBAL              sequence
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     26  'to 26'

 L. 893        10  LOAD_GLOBAL              DistutilsSetupError

 L. 894        12  LOAD_STR                 '%s: setting must be a list (%r)'
               14  LOAD_FAST                'name'
               16  LOAD_FAST                'value'
               18  BUILD_TUPLE_2         2 
               20  BINARY_MODULO    

 L. 893        22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM             8  '8'

 L. 896        26  SETUP_FINALLY        42  'to 42'

 L. 897        28  LOAD_GLOBAL              getattr
               30  LOAD_FAST                'self'
               32  LOAD_FAST                'name'
               34  CALL_FUNCTION_2       2  ''
               36  STORE_DEREF              'old'
               38  POP_BLOCK        
               40  JUMP_FORWARD         92  'to 92'
             42_0  COME_FROM_FINALLY    26  '26'

 L. 898        42  DUP_TOP          
               44  LOAD_GLOBAL              AttributeError
               46  <121>                90  ''
               48  POP_TOP          
               50  STORE_FAST               'e'
               52  POP_TOP          
               54  SETUP_FINALLY        82  'to 82'

 L. 899        56  LOAD_GLOBAL              DistutilsSetupError

 L. 900        58  LOAD_STR                 '%s: No such distribution setting'
               60  LOAD_FAST                'name'
               62  BINARY_MODULO    

 L. 899        64  CALL_FUNCTION_1       1  ''

 L. 901        66  LOAD_FAST                'e'

 L. 899        68  RAISE_VARARGS_2       2  'exception instance with __cause__'
               70  POP_BLOCK        
               72  POP_EXCEPT       
               74  LOAD_CONST               None
               76  STORE_FAST               'e'
               78  DELETE_FAST              'e'
               80  JUMP_FORWARD         92  'to 92'
             82_0  COME_FROM_FINALLY    54  '54'
               82  LOAD_CONST               None
               84  STORE_FAST               'e'
               86  DELETE_FAST              'e'
               88  <48>             
               90  <48>             
             92_0  COME_FROM            80  '80'
             92_1  COME_FROM            40  '40'

 L. 902        92  LOAD_DEREF               'old'
               94  LOAD_CONST               None
               96  <117>                 0  ''
               98  POP_JUMP_IF_FALSE   114  'to 114'

 L. 903       100  LOAD_GLOBAL              setattr
              102  LOAD_FAST                'self'
              104  LOAD_FAST                'name'
              106  LOAD_FAST                'value'
              108  CALL_FUNCTION_3       3  ''
              110  POP_TOP          
              112  JUMP_FORWARD        172  'to 172'
            114_0  COME_FROM            98  '98'

 L. 904       114  LOAD_GLOBAL              isinstance
              116  LOAD_DEREF               'old'
              118  LOAD_GLOBAL              sequence
              120  CALL_FUNCTION_2       2  ''
              122  POP_JUMP_IF_TRUE    138  'to 138'

 L. 905       124  LOAD_GLOBAL              DistutilsSetupError

 L. 906       126  LOAD_FAST                'name'
              128  LOAD_STR                 ': this setting cannot be changed via include/exclude'
              130  BINARY_ADD       

 L. 905       132  CALL_FUNCTION_1       1  ''
              134  RAISE_VARARGS_1       1  'exception instance'
              136  JUMP_FORWARD        172  'to 172'
            138_0  COME_FROM           122  '122'

 L. 909       138  LOAD_CLOSURE             'old'
              140  BUILD_TUPLE_1         1 
              142  LOAD_LISTCOMP            '<code_object <listcomp>>'
              144  LOAD_STR                 'Distribution._include_misc.<locals>.<listcomp>'
              146  MAKE_FUNCTION_8          'closure'
              148  LOAD_FAST                'value'
              150  GET_ITER         
              152  CALL_FUNCTION_1       1  ''
              154  STORE_FAST               'new'

 L. 910       156  LOAD_GLOBAL              setattr
              158  LOAD_FAST                'self'
              160  LOAD_FAST                'name'
              162  LOAD_DEREF               'old'
              164  LOAD_FAST                'new'
              166  BINARY_ADD       
              168  CALL_FUNCTION_3       3  ''
              170  POP_TOP          
            172_0  COME_FROM           136  '136'
            172_1  COME_FROM           112  '112'

Parse error at or near `<121>' instruction at offset 46

    def exclude(self, **attrs):
        """Remove items from distribution that are named in keyword arguments

        For example, 'dist.exclude(py_modules=["x"])' would remove 'x' from
        the distribution's 'py_modules' attribute.  Excluding packages uses
        the 'exclude_package()' method, so all of the package's contained
        packages, modules, and extensions are also excluded.

        Currently, this method only supports exclusion from attributes that are
        lists or tuples.  If you need to add support for excluding from other
        attributes in this or a subclass, you can add an '_exclude_X' method,
        where 'X' is the name of the attribute.  The method will be called with
        the value passed to 'exclude()'.  So, 'dist.exclude(foo={"bar":"baz"})'
        will try to call 'dist._exclude_foo({"bar":"baz"})', which can then
        handle whatever special exclusion logic is needed.
        """
        for k, v in attrs.items():
            exclude = getattr(self, '_exclude_' + k, None)
            if exclude:
                exclude(v)
            else:
                self._exclude_misc(k, v)

    def _exclude_packages(self, packages):
        if not isinstancepackagessequence:
            raise DistutilsSetupError('packages: setting must be a list or tuple (%r)' % (packages,))
        list(mapself.exclude_packagepackages)

    def _parse_command_opts--- This code section failed: ---

 L. 944         0  LOAD_FAST                'self'
                2  LOAD_ATTR                __class__
                4  LOAD_ATTR                global_options
                6  LOAD_FAST                'self'
                8  STORE_ATTR               global_options

 L. 945        10  LOAD_FAST                'self'
               12  LOAD_ATTR                __class__
               14  LOAD_ATTR                negative_opt
               16  LOAD_FAST                'self'
               18  STORE_ATTR               negative_opt

 L. 948        20  LOAD_FAST                'args'
               22  LOAD_CONST               0
               24  BINARY_SUBSCR    
               26  STORE_FAST               'command'

 L. 949        28  LOAD_FAST                'self'
               30  LOAD_METHOD              get_option_dict
               32  LOAD_STR                 'aliases'
               34  CALL_METHOD_1         1  ''
               36  STORE_FAST               'aliases'

 L. 950        38  LOAD_FAST                'command'
               40  LOAD_FAST                'aliases'
               42  <118>                 0  ''
               44  POP_JUMP_IF_FALSE   102  'to 102'

 L. 951        46  LOAD_FAST                'aliases'
               48  LOAD_FAST                'command'
               50  BINARY_SUBSCR    
               52  UNPACK_SEQUENCE_2     2 
               54  STORE_FAST               'src'
               56  STORE_FAST               'alias'

 L. 952        58  LOAD_FAST                'aliases'
               60  LOAD_FAST                'command'
               62  DELETE_SUBSCR    

 L. 953        64  LOAD_CONST               0
               66  LOAD_CONST               None
               68  IMPORT_NAME              shlex
               70  STORE_FAST               'shlex'

 L. 954        72  LOAD_FAST                'shlex'
               74  LOAD_METHOD              split
               76  LOAD_FAST                'alias'
               78  LOAD_CONST               True
               80  CALL_METHOD_2         2  ''
               82  LOAD_FAST                'args'
               84  LOAD_CONST               None
               86  LOAD_CONST               1
               88  BUILD_SLICE_2         2 
               90  STORE_SUBSCR     

 L. 955        92  LOAD_FAST                'args'
               94  LOAD_CONST               0
               96  BINARY_SUBSCR    
               98  STORE_FAST               'command'
              100  JUMP_BACK            38  'to 38'
            102_0  COME_FROM            44  '44'

 L. 957       102  LOAD_GLOBAL              _Distribution
              104  LOAD_METHOD              _parse_command_opts
              106  LOAD_FAST                'self'
              108  LOAD_FAST                'parser'
              110  LOAD_FAST                'args'
              112  CALL_METHOD_3         3  ''
              114  STORE_FAST               'nargs'

 L. 960       116  LOAD_FAST                'self'
              118  LOAD_METHOD              get_command_class
              120  LOAD_FAST                'command'
              122  CALL_METHOD_1         1  ''
              124  STORE_FAST               'cmd_class'

 L. 961       126  LOAD_GLOBAL              getattr
              128  LOAD_FAST                'cmd_class'
              130  LOAD_STR                 'command_consumes_arguments'
              132  LOAD_CONST               None
              134  CALL_FUNCTION_3       3  ''
              136  POP_JUMP_IF_FALSE   168  'to 168'

 L. 962       138  LOAD_STR                 'command line'
              140  LOAD_FAST                'nargs'
              142  BUILD_TUPLE_2         2 
              144  LOAD_FAST                'self'
              146  LOAD_METHOD              get_option_dict
              148  LOAD_FAST                'command'
              150  CALL_METHOD_1         1  ''
              152  LOAD_STR                 'args'
              154  STORE_SUBSCR     

 L. 963       156  LOAD_FAST                'nargs'
              158  LOAD_CONST               None
              160  <117>                 1  ''
              162  POP_JUMP_IF_FALSE   168  'to 168'

 L. 964       164  BUILD_LIST_0          0 
              166  RETURN_VALUE     
            168_0  COME_FROM           162  '162'
            168_1  COME_FROM           136  '136'

 L. 966       168  LOAD_FAST                'nargs'
              170  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 42

    def get_cmdline_options(self):
        """Return a '{cmd: {opt:val}}' map of all command-line options

        Option names are all long, but do not include the leading '--', and
        contain dashes rather than underscores.  If the option doesn't take
        an argument (e.g. '--quiet'), the 'val' is 'None'.

        Note that options provided by config files are intentionally excluded.
        """
        d = {}
        for cmd, opts in self.command_options.items():
            for opt, (src, val) in opts.items():
                if src != 'command line':
                    pass
                else:
                    opt = opt.replace('_', '-')
                    if val == 0:
                        cmdobj = self.get_command_obj(cmd)
                        neg_opt = self.negative_opt.copy()
                        neg_opt.update(getattr(cmdobj, 'negative_opt', {}))
                        for neg, pos in neg_opt.items():
                            if pos == opt:
                                opt = neg
                                val = None
                                break
                        else:
                            raise AssertionError("Shouldn't be able to get here")

                    else:
                        if val == 1:
                            val = None
                    d.setdefault(cmd, {})[opt] = val
            else:
                return d

    def iter_distribution_names(self):
        """Yield all packages, modules, and extension names in distribution"""
        for pkg in self.packages or ():
            (yield pkg)
        else:
            for module in self.py_modules or ():
                (yield module)
            else:
                for ext in self.ext_modules or ():
                    if isinstanceexttuple:
                        name, buildinfo = ext
                    else:
                        name = ext.name
                    if name.endswith('module'):
                        name = name[:-6]
                    (yield name)

    def handle_display_options--- This code section failed: ---

 L.1032         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              sys
                6  STORE_FAST               'sys'

 L.1034         8  LOAD_FAST                'self'
               10  LOAD_ATTR                help_commands
               12  POP_JUMP_IF_FALSE    26  'to 26'

 L.1035        14  LOAD_GLOBAL              _Distribution
               16  LOAD_METHOD              handle_display_options
               18  LOAD_FAST                'self'
               20  LOAD_FAST                'option_order'
               22  CALL_METHOD_2         2  ''
               24  RETURN_VALUE     
             26_0  COME_FROM            12  '12'

 L.1038        26  LOAD_GLOBAL              isinstance
               28  LOAD_FAST                'sys'
               30  LOAD_ATTR                stdout
               32  LOAD_GLOBAL              io
               34  LOAD_ATTR                TextIOWrapper
               36  CALL_FUNCTION_2       2  ''
               38  POP_JUMP_IF_TRUE     52  'to 52'

 L.1039        40  LOAD_GLOBAL              _Distribution
               42  LOAD_METHOD              handle_display_options
               44  LOAD_FAST                'self'
               46  LOAD_FAST                'option_order'
               48  CALL_METHOD_2         2  ''
               50  RETURN_VALUE     
             52_0  COME_FROM            38  '38'

 L.1043        52  LOAD_FAST                'sys'
               54  LOAD_ATTR                stdout
               56  LOAD_ATTR                encoding
               58  LOAD_METHOD              lower
               60  CALL_METHOD_0         0  ''
               62  LOAD_CONST               ('utf-8', 'utf8')
               64  <118>                 0  ''
               66  POP_JUMP_IF_FALSE    80  'to 80'

 L.1044        68  LOAD_GLOBAL              _Distribution
               70  LOAD_METHOD              handle_display_options
               72  LOAD_FAST                'self'
               74  LOAD_FAST                'option_order'
               76  CALL_METHOD_2         2  ''
               78  RETURN_VALUE     
             80_0  COME_FROM            66  '66'

 L.1047        80  LOAD_FAST                'sys'
               82  LOAD_ATTR                stdout
               84  LOAD_ATTR                encoding
               86  STORE_FAST               'encoding'

 L.1048        88  LOAD_FAST                'sys'
               90  LOAD_ATTR                stdout
               92  LOAD_ATTR                errors
               94  STORE_FAST               'errors'

 L.1049        96  LOAD_FAST                'sys'
               98  LOAD_ATTR                platform
              100  LOAD_STR                 'win32'
              102  COMPARE_OP               !=
              104  POP_JUMP_IF_FALSE   110  'to 110'
              106  LOAD_STR                 '\n'
              108  JUMP_IF_TRUE_OR_POP   112  'to 112'
            110_0  COME_FROM           104  '104'
              110  LOAD_CONST               None
            112_0  COME_FROM           108  '108'
              112  STORE_FAST               'newline'

 L.1050       114  LOAD_FAST                'sys'
              116  LOAD_ATTR                stdout
              118  LOAD_ATTR                line_buffering
              120  STORE_FAST               'line_buffering'

 L.1052       122  LOAD_GLOBAL              io
              124  LOAD_METHOD              TextIOWrapper

 L.1053       126  LOAD_FAST                'sys'
              128  LOAD_ATTR                stdout
              130  LOAD_METHOD              detach
              132  CALL_METHOD_0         0  ''
              134  LOAD_STR                 'utf-8'
              136  LOAD_FAST                'errors'
              138  LOAD_FAST                'newline'
              140  LOAD_FAST                'line_buffering'

 L.1052       142  CALL_METHOD_5         5  ''
              144  LOAD_FAST                'sys'
              146  STORE_ATTR               stdout

 L.1054       148  SETUP_FINALLY       190  'to 190'

 L.1055       150  LOAD_GLOBAL              _Distribution
              152  LOAD_METHOD              handle_display_options
              154  LOAD_FAST                'self'
              156  LOAD_FAST                'option_order'
              158  CALL_METHOD_2         2  ''
              160  POP_BLOCK        

 L.1057       162  LOAD_GLOBAL              io
              164  LOAD_METHOD              TextIOWrapper

 L.1058       166  LOAD_FAST                'sys'
              168  LOAD_ATTR                stdout
              170  LOAD_METHOD              detach
              172  CALL_METHOD_0         0  ''
              174  LOAD_FAST                'encoding'
              176  LOAD_FAST                'errors'
              178  LOAD_FAST                'newline'
              180  LOAD_FAST                'line_buffering'

 L.1057       182  CALL_METHOD_5         5  ''
              184  LOAD_FAST                'sys'
              186  STORE_ATTR               stdout

 L.1055       188  RETURN_VALUE     
            190_0  COME_FROM_FINALLY   148  '148'

 L.1057       190  LOAD_GLOBAL              io
              192  LOAD_METHOD              TextIOWrapper

 L.1058       194  LOAD_FAST                'sys'
              196  LOAD_ATTR                stdout
              198  LOAD_METHOD              detach
              200  CALL_METHOD_0         0  ''
              202  LOAD_FAST                'encoding'
              204  LOAD_FAST                'errors'
              206  LOAD_FAST                'newline'
              208  LOAD_FAST                'line_buffering'

 L.1057       210  CALL_METHOD_5         5  ''
              212  LOAD_FAST                'sys'
              214  STORE_ATTR               stdout
              216  <48>             

Parse error at or near `<118>' instruction at offset 64


class DistDeprecationWarning(SetuptoolsDeprecationWarning):
    __doc__ = 'Class for warning about deprecations in dist in\n    setuptools. Not ignored by default, unlike DeprecationWarning.'