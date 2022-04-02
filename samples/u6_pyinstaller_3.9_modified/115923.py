# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: setuptools\dist.py
__all__ = ['Distribution']
import io, sys, re, os, warnings, numbers, distutils.log, distutils.core, distutils.cmd, distutils.dist
from distutils.util import strtobool
from distutils.debug import DEBUG
from distutils.fancy_getopt import translate_longopt
import itertools
from collections import defaultdict
from email import message_from_file
from distutils.errors import DistutilsOptionError, DistutilsSetupError
from distutils.util import rfc822_escape
from distutils.version import StrictVersion
from setuptools.extern import six
from setuptools.extern import packaging
from setuptools.extern import ordered_set
from setuptools.extern.six.moves import map, filter, filterfalse
from . import SetuptoolsDeprecationWarning
import setuptools
from setuptools import windows_support
from setuptools.monkey import get_unpatched
from setuptools.config import parse_configuration
import pkg_resources
__import__('setuptools.extern.packaging.specifiers')
__import__('setuptools.extern.packaging.version')

def _get_unpatched(cls):
    warnings.warn('Do not call this function', DistDeprecationWarning)
    return get_unpatched(cls)


def get_metadata_version--- This code section failed: ---

 L.  49         0  LOAD_GLOBAL              getattr
                2  LOAD_FAST                'self'
                4  LOAD_STR                 'metadata_version'
                6  LOAD_CONST               None
                8  CALL_FUNCTION_3       3  ''
               10  STORE_FAST               'mv'

 L.  51        12  LOAD_FAST                'mv'
               14  LOAD_CONST               None
               16  <117>                 0  ''
               18  POP_JUMP_IF_FALSE   148  'to 148'

 L.  52        20  LOAD_FAST                'self'
               22  LOAD_ATTR                long_description_content_type
               24  POP_JUMP_IF_TRUE     32  'to 32'
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                provides_extras
               30  POP_JUMP_IF_FALSE    42  'to 42'
             32_0  COME_FROM            24  '24'

 L.  53        32  LOAD_GLOBAL              StrictVersion
               34  LOAD_STR                 '2.1'
               36  CALL_FUNCTION_1       1  ''
               38  STORE_FAST               'mv'
               40  JUMP_FORWARD        142  'to 142'
             42_0  COME_FROM            30  '30'

 L.  54        42  LOAD_FAST                'self'
               44  LOAD_ATTR                maintainer
               46  LOAD_CONST               None
               48  <117>                 1  ''
               50  POP_JUMP_IF_TRUE     84  'to 84'

 L.  55        52  LOAD_FAST                'self'
               54  LOAD_ATTR                maintainer_email
               56  LOAD_CONST               None
               58  <117>                 1  ''

 L.  54        60  POP_JUMP_IF_TRUE     84  'to 84'

 L.  56        62  LOAD_GLOBAL              getattr
               64  LOAD_FAST                'self'
               66  LOAD_STR                 'python_requires'
               68  LOAD_CONST               None
               70  CALL_FUNCTION_3       3  ''
               72  LOAD_CONST               None
               74  <117>                 1  ''

 L.  54        76  POP_JUMP_IF_TRUE     84  'to 84'

 L.  57        78  LOAD_FAST                'self'
               80  LOAD_ATTR                project_urls

 L.  54        82  POP_JUMP_IF_FALSE    94  'to 94'
             84_0  COME_FROM            76  '76'
             84_1  COME_FROM            60  '60'
             84_2  COME_FROM            50  '50'

 L.  58        84  LOAD_GLOBAL              StrictVersion
               86  LOAD_STR                 '1.2'
               88  CALL_FUNCTION_1       1  ''
               90  STORE_FAST               'mv'
               92  JUMP_FORWARD        142  'to 142'
             94_0  COME_FROM            82  '82'

 L.  59        94  LOAD_FAST                'self'
               96  LOAD_ATTR                provides
               98  POP_JUMP_IF_TRUE    124  'to 124'
              100  LOAD_FAST                'self'
              102  LOAD_ATTR                requires
              104  POP_JUMP_IF_TRUE    124  'to 124'
              106  LOAD_FAST                'self'
              108  LOAD_ATTR                obsoletes
              110  POP_JUMP_IF_TRUE    124  'to 124'

 L.  60       112  LOAD_FAST                'self'
              114  LOAD_ATTR                classifiers

 L.  59       116  POP_JUMP_IF_TRUE    124  'to 124'

 L.  60       118  LOAD_FAST                'self'
              120  LOAD_ATTR                download_url

 L.  59       122  POP_JUMP_IF_FALSE   134  'to 134'
            124_0  COME_FROM           116  '116'
            124_1  COME_FROM           110  '110'
            124_2  COME_FROM           104  '104'
            124_3  COME_FROM            98  '98'

 L.  61       124  LOAD_GLOBAL              StrictVersion
              126  LOAD_STR                 '1.1'
              128  CALL_FUNCTION_1       1  ''
              130  STORE_FAST               'mv'
              132  JUMP_FORWARD        142  'to 142'
            134_0  COME_FROM           122  '122'

 L.  63       134  LOAD_GLOBAL              StrictVersion
              136  LOAD_STR                 '1.0'
              138  CALL_FUNCTION_1       1  ''
              140  STORE_FAST               'mv'
            142_0  COME_FROM           132  '132'
            142_1  COME_FROM            92  '92'
            142_2  COME_FROM            40  '40'

 L.  65       142  LOAD_FAST                'mv'
              144  LOAD_FAST                'self'
              146  STORE_ATTR               metadata_version
            148_0  COME_FROM            18  '18'

 L.  67       148  LOAD_FAST                'mv'
              150  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 16


def read_pkg_file--- This code section failed: ---

 L.  72         0  LOAD_GLOBAL              message_from_file
                2  LOAD_FAST                'file'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_DEREF              'msg'

 L.  74         8  LOAD_CLOSURE             'msg'
               10  BUILD_TUPLE_1         1 
               12  LOAD_CODE                <code_object _read_field>
               14  LOAD_STR                 'read_pkg_file.<locals>._read_field'
               16  MAKE_FUNCTION_8          'closure'
               18  STORE_FAST               '_read_field'

 L.  80        20  LOAD_CLOSURE             'msg'
               22  BUILD_TUPLE_1         1 
               24  LOAD_CODE                <code_object _read_list>
               26  LOAD_STR                 'read_pkg_file.<locals>._read_list'
               28  MAKE_FUNCTION_8          'closure'
               30  STORE_FAST               '_read_list'

 L.  86        32  LOAD_GLOBAL              StrictVersion
               34  LOAD_DEREF               'msg'
               36  LOAD_STR                 'metadata-version'
               38  BINARY_SUBSCR    
               40  CALL_FUNCTION_1       1  ''
               42  LOAD_FAST                'self'
               44  STORE_ATTR               metadata_version

 L.  87        46  LOAD_FAST                '_read_field'
               48  LOAD_STR                 'name'
               50  CALL_FUNCTION_1       1  ''
               52  LOAD_FAST                'self'
               54  STORE_ATTR               name

 L.  88        56  LOAD_FAST                '_read_field'
               58  LOAD_STR                 'version'
               60  CALL_FUNCTION_1       1  ''
               62  LOAD_FAST                'self'
               64  STORE_ATTR               version

 L.  89        66  LOAD_FAST                '_read_field'
               68  LOAD_STR                 'summary'
               70  CALL_FUNCTION_1       1  ''
               72  LOAD_FAST                'self'
               74  STORE_ATTR               description

 L.  91        76  LOAD_FAST                '_read_field'
               78  LOAD_STR                 'author'
               80  CALL_FUNCTION_1       1  ''
               82  LOAD_FAST                'self'
               84  STORE_ATTR               author

 L.  92        86  LOAD_CONST               None
               88  LOAD_FAST                'self'
               90  STORE_ATTR               maintainer

 L.  93        92  LOAD_FAST                '_read_field'
               94  LOAD_STR                 'author-email'
               96  CALL_FUNCTION_1       1  ''
               98  LOAD_FAST                'self'
              100  STORE_ATTR               author_email

 L.  94       102  LOAD_CONST               None
              104  LOAD_FAST                'self'
              106  STORE_ATTR               maintainer_email

 L.  95       108  LOAD_FAST                '_read_field'
              110  LOAD_STR                 'home-page'
              112  CALL_FUNCTION_1       1  ''
              114  LOAD_FAST                'self'
              116  STORE_ATTR               url

 L.  96       118  LOAD_FAST                '_read_field'
              120  LOAD_STR                 'license'
              122  CALL_FUNCTION_1       1  ''
              124  LOAD_FAST                'self'
              126  STORE_ATTR               license

 L.  98       128  LOAD_STR                 'download-url'
              130  LOAD_DEREF               'msg'
              132  <118>                 0  ''
              134  POP_JUMP_IF_FALSE   148  'to 148'

 L.  99       136  LOAD_FAST                '_read_field'
              138  LOAD_STR                 'download-url'
              140  CALL_FUNCTION_1       1  ''
              142  LOAD_FAST                'self'
              144  STORE_ATTR               download_url
              146  JUMP_FORWARD        154  'to 154'
            148_0  COME_FROM           134  '134'

 L. 101       148  LOAD_CONST               None
              150  LOAD_FAST                'self'
              152  STORE_ATTR               download_url
            154_0  COME_FROM           146  '146'

 L. 103       154  LOAD_FAST                '_read_field'
              156  LOAD_STR                 'description'
              158  CALL_FUNCTION_1       1  ''
              160  LOAD_FAST                'self'
              162  STORE_ATTR               long_description

 L. 104       164  LOAD_FAST                '_read_field'
              166  LOAD_STR                 'summary'
              168  CALL_FUNCTION_1       1  ''
              170  LOAD_FAST                'self'
              172  STORE_ATTR               description

 L. 106       174  LOAD_STR                 'keywords'
              176  LOAD_DEREF               'msg'
              178  <118>                 0  ''
              180  POP_JUMP_IF_FALSE   198  'to 198'

 L. 107       182  LOAD_FAST                '_read_field'
              184  LOAD_STR                 'keywords'
              186  CALL_FUNCTION_1       1  ''
              188  LOAD_METHOD              split
              190  LOAD_STR                 ','
              192  CALL_METHOD_1         1  ''
              194  LOAD_FAST                'self'
              196  STORE_ATTR               keywords
            198_0  COME_FROM           180  '180'

 L. 109       198  LOAD_FAST                '_read_list'
              200  LOAD_STR                 'platform'
              202  CALL_FUNCTION_1       1  ''
              204  LOAD_FAST                'self'
              206  STORE_ATTR               platforms

 L. 110       208  LOAD_FAST                '_read_list'
              210  LOAD_STR                 'classifier'
              212  CALL_FUNCTION_1       1  ''
              214  LOAD_FAST                'self'
              216  STORE_ATTR               classifiers

 L. 113       218  LOAD_FAST                'self'
              220  LOAD_ATTR                metadata_version
              222  LOAD_GLOBAL              StrictVersion
              224  LOAD_STR                 '1.1'
              226  CALL_FUNCTION_1       1  ''
              228  COMPARE_OP               ==
          230_232  POP_JUMP_IF_FALSE   266  'to 266'

 L. 114       234  LOAD_FAST                '_read_list'
              236  LOAD_STR                 'requires'
              238  CALL_FUNCTION_1       1  ''
              240  LOAD_FAST                'self'
              242  STORE_ATTR               requires

 L. 115       244  LOAD_FAST                '_read_list'
              246  LOAD_STR                 'provides'
              248  CALL_FUNCTION_1       1  ''
              250  LOAD_FAST                'self'
              252  STORE_ATTR               provides

 L. 116       254  LOAD_FAST                '_read_list'
              256  LOAD_STR                 'obsoletes'
              258  CALL_FUNCTION_1       1  ''
              260  LOAD_FAST                'self'
              262  STORE_ATTR               obsoletes
              264  JUMP_FORWARD        284  'to 284'
            266_0  COME_FROM           230  '230'

 L. 118       266  LOAD_CONST               None
              268  LOAD_FAST                'self'
              270  STORE_ATTR               requires

 L. 119       272  LOAD_CONST               None
              274  LOAD_FAST                'self'
              276  STORE_ATTR               provides

 L. 120       278  LOAD_CONST               None
              280  LOAD_FAST                'self'
              282  STORE_ATTR               obsoletes
            284_0  COME_FROM           264  '264'

Parse error at or near `<118>' instruction at offset 132


def write_pkg_file--- This code section failed: ---

 L. 127         0  LOAD_DEREF               'self'
                2  LOAD_METHOD              get_metadata_version
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'version'

 L. 129         8  LOAD_GLOBAL              six
               10  LOAD_ATTR                PY2
               12  POP_JUMP_IF_FALSE    30  'to 30'

 L. 130        14  LOAD_CLOSURE             'file'
               16  LOAD_CLOSURE             'self'
               18  BUILD_TUPLE_2         2 
               20  LOAD_CODE                <code_object write_field>
               22  LOAD_STR                 'write_pkg_file.<locals>.write_field'
               24  MAKE_FUNCTION_8          'closure'
               26  STORE_FAST               'write_field'
               28  JUMP_FORWARD         42  'to 42'
             30_0  COME_FROM            12  '12'

 L. 133        30  LOAD_CLOSURE             'file'
               32  BUILD_TUPLE_1         1 
               34  LOAD_CODE                <code_object write_field>
               36  LOAD_STR                 'write_pkg_file.<locals>.write_field'
               38  MAKE_FUNCTION_8          'closure'
               40  STORE_FAST               'write_field'
             42_0  COME_FROM            28  '28'

 L. 136        42  LOAD_FAST                'write_field'
               44  LOAD_STR                 'Metadata-Version'
               46  LOAD_GLOBAL              str
               48  LOAD_FAST                'version'
               50  CALL_FUNCTION_1       1  ''
               52  CALL_FUNCTION_2       2  ''
               54  POP_TOP          

 L. 137        56  LOAD_FAST                'write_field'
               58  LOAD_STR                 'Name'
               60  LOAD_DEREF               'self'
               62  LOAD_METHOD              get_name
               64  CALL_METHOD_0         0  ''
               66  CALL_FUNCTION_2       2  ''
               68  POP_TOP          

 L. 138        70  LOAD_FAST                'write_field'
               72  LOAD_STR                 'Version'
               74  LOAD_DEREF               'self'
               76  LOAD_METHOD              get_version
               78  CALL_METHOD_0         0  ''
               80  CALL_FUNCTION_2       2  ''
               82  POP_TOP          

 L. 139        84  LOAD_FAST                'write_field'
               86  LOAD_STR                 'Summary'
               88  LOAD_DEREF               'self'
               90  LOAD_METHOD              get_description
               92  CALL_METHOD_0         0  ''
               94  CALL_FUNCTION_2       2  ''
               96  POP_TOP          

 L. 140        98  LOAD_FAST                'write_field'
              100  LOAD_STR                 'Home-page'
              102  LOAD_DEREF               'self'
              104  LOAD_METHOD              get_url
              106  CALL_METHOD_0         0  ''
              108  CALL_FUNCTION_2       2  ''
              110  POP_TOP          

 L. 142       112  LOAD_FAST                'version'
              114  LOAD_GLOBAL              StrictVersion
              116  LOAD_STR                 '1.2'
              118  CALL_FUNCTION_1       1  ''
              120  COMPARE_OP               <
              122  POP_JUMP_IF_FALSE   154  'to 154'

 L. 143       124  LOAD_FAST                'write_field'
              126  LOAD_STR                 'Author'
              128  LOAD_DEREF               'self'
              130  LOAD_METHOD              get_contact
              132  CALL_METHOD_0         0  ''
              134  CALL_FUNCTION_2       2  ''
              136  POP_TOP          

 L. 144       138  LOAD_FAST                'write_field'
              140  LOAD_STR                 'Author-email'
              142  LOAD_DEREF               'self'
              144  LOAD_METHOD              get_contact_email
              146  CALL_METHOD_0         0  ''
              148  CALL_FUNCTION_2       2  ''
              150  POP_TOP          
              152  JUMP_FORWARD        200  'to 200'
            154_0  COME_FROM           122  '122'

 L. 146       154  LOAD_CONST               (('Author', 'author'), ('Author-email', 'author_email'), ('Maintainer', 'maintainer'), ('Maintainer-email', 'maintainer_email'))
              156  STORE_FAST               'optional_fields'

 L. 153       158  LOAD_FAST                'optional_fields'
              160  GET_ITER         
            162_0  COME_FROM           186  '186'
              162  FOR_ITER            200  'to 200'
              164  UNPACK_SEQUENCE_2     2 
              166  STORE_FAST               'field'
              168  STORE_FAST               'attr'

 L. 154       170  LOAD_GLOBAL              getattr
              172  LOAD_DEREF               'self'
              174  LOAD_FAST                'attr'
              176  CALL_FUNCTION_2       2  ''
              178  STORE_FAST               'attr_val'

 L. 156       180  LOAD_FAST                'attr_val'
              182  LOAD_CONST               None
              184  <117>                 1  ''
              186  POP_JUMP_IF_FALSE   162  'to 162'

 L. 157       188  LOAD_FAST                'write_field'
              190  LOAD_FAST                'field'
              192  LOAD_FAST                'attr_val'
              194  CALL_FUNCTION_2       2  ''
              196  POP_TOP          
              198  JUMP_BACK           162  'to 162'
            200_0  COME_FROM           152  '152'

 L. 159       200  LOAD_FAST                'write_field'
              202  LOAD_STR                 'License'
              204  LOAD_DEREF               'self'
              206  LOAD_METHOD              get_license
              208  CALL_METHOD_0         0  ''
              210  CALL_FUNCTION_2       2  ''
              212  POP_TOP          

 L. 160       214  LOAD_DEREF               'self'
              216  LOAD_ATTR                download_url
              218  POP_JUMP_IF_FALSE   232  'to 232'

 L. 161       220  LOAD_FAST                'write_field'
              222  LOAD_STR                 'Download-URL'
              224  LOAD_DEREF               'self'
              226  LOAD_ATTR                download_url
              228  CALL_FUNCTION_2       2  ''
              230  POP_TOP          
            232_0  COME_FROM           218  '218'

 L. 162       232  LOAD_DEREF               'self'
              234  LOAD_ATTR                project_urls
              236  LOAD_METHOD              items
              238  CALL_METHOD_0         0  ''
              240  GET_ITER         
              242  FOR_ITER            262  'to 262'
              244  STORE_FAST               'project_url'

 L. 163       246  LOAD_FAST                'write_field'
              248  LOAD_STR                 'Project-URL'
              250  LOAD_STR                 '%s, %s'
              252  LOAD_FAST                'project_url'
              254  BINARY_MODULO    
              256  CALL_FUNCTION_2       2  ''
              258  POP_TOP          
              260  JUMP_BACK           242  'to 242'

 L. 165       262  LOAD_GLOBAL              rfc822_escape
              264  LOAD_DEREF               'self'
              266  LOAD_METHOD              get_long_description
              268  CALL_METHOD_0         0  ''
              270  CALL_FUNCTION_1       1  ''
              272  STORE_FAST               'long_desc'

 L. 166       274  LOAD_FAST                'write_field'
              276  LOAD_STR                 'Description'
              278  LOAD_FAST                'long_desc'
              280  CALL_FUNCTION_2       2  ''
              282  POP_TOP          

 L. 168       284  LOAD_STR                 ','
              286  LOAD_METHOD              join
              288  LOAD_DEREF               'self'
              290  LOAD_METHOD              get_keywords
              292  CALL_METHOD_0         0  ''
              294  CALL_METHOD_1         1  ''
              296  STORE_FAST               'keywords'

 L. 169       298  LOAD_FAST                'keywords'
          300_302  POP_JUMP_IF_FALSE   314  'to 314'

 L. 170       304  LOAD_FAST                'write_field'
              306  LOAD_STR                 'Keywords'
              308  LOAD_FAST                'keywords'
              310  CALL_FUNCTION_2       2  ''
              312  POP_TOP          
            314_0  COME_FROM           300  '300'

 L. 172       314  LOAD_FAST                'version'
              316  LOAD_GLOBAL              StrictVersion
              318  LOAD_STR                 '1.2'
              320  CALL_FUNCTION_1       1  ''
              322  COMPARE_OP               >=
          324_326  POP_JUMP_IF_FALSE   356  'to 356'

 L. 173       328  LOAD_DEREF               'self'
              330  LOAD_METHOD              get_platforms
              332  CALL_METHOD_0         0  ''
              334  GET_ITER         
              336  FOR_ITER            354  'to 354'
              338  STORE_FAST               'platform'

 L. 174       340  LOAD_FAST                'write_field'
              342  LOAD_STR                 'Platform'
              344  LOAD_FAST                'platform'
              346  CALL_FUNCTION_2       2  ''
              348  POP_TOP          
          350_352  JUMP_BACK           336  'to 336'
              354  JUMP_FORWARD        374  'to 374'
            356_0  COME_FROM           324  '324'

 L. 176       356  LOAD_DEREF               'self'
              358  LOAD_METHOD              _write_list
              360  LOAD_DEREF               'file'
              362  LOAD_STR                 'Platform'
              364  LOAD_DEREF               'self'
              366  LOAD_METHOD              get_platforms
              368  CALL_METHOD_0         0  ''
              370  CALL_METHOD_3         3  ''
              372  POP_TOP          
            374_0  COME_FROM           354  '354'

 L. 178       374  LOAD_DEREF               'self'
              376  LOAD_METHOD              _write_list
              378  LOAD_DEREF               'file'
              380  LOAD_STR                 'Classifier'
              382  LOAD_DEREF               'self'
              384  LOAD_METHOD              get_classifiers
              386  CALL_METHOD_0         0  ''
              388  CALL_METHOD_3         3  ''
              390  POP_TOP          

 L. 181       392  LOAD_DEREF               'self'
              394  LOAD_METHOD              _write_list
              396  LOAD_DEREF               'file'
              398  LOAD_STR                 'Requires'
              400  LOAD_DEREF               'self'
              402  LOAD_METHOD              get_requires
              404  CALL_METHOD_0         0  ''
              406  CALL_METHOD_3         3  ''
              408  POP_TOP          

 L. 182       410  LOAD_DEREF               'self'
              412  LOAD_METHOD              _write_list
              414  LOAD_DEREF               'file'
              416  LOAD_STR                 'Provides'
              418  LOAD_DEREF               'self'
              420  LOAD_METHOD              get_provides
              422  CALL_METHOD_0         0  ''
              424  CALL_METHOD_3         3  ''
              426  POP_TOP          

 L. 183       428  LOAD_DEREF               'self'
              430  LOAD_METHOD              _write_list
              432  LOAD_DEREF               'file'
              434  LOAD_STR                 'Obsoletes'
              436  LOAD_DEREF               'self'
              438  LOAD_METHOD              get_obsoletes
              440  CALL_METHOD_0         0  ''
              442  CALL_METHOD_3         3  ''
              444  POP_TOP          

 L. 186       446  LOAD_GLOBAL              hasattr
              448  LOAD_DEREF               'self'
              450  LOAD_STR                 'python_requires'
              452  CALL_FUNCTION_2       2  ''
          454_456  POP_JUMP_IF_FALSE   470  'to 470'

 L. 187       458  LOAD_FAST                'write_field'
              460  LOAD_STR                 'Requires-Python'
              462  LOAD_DEREF               'self'
              464  LOAD_ATTR                python_requires
              466  CALL_FUNCTION_2       2  ''
              468  POP_TOP          
            470_0  COME_FROM           454  '454'

 L. 190       470  LOAD_DEREF               'self'
              472  LOAD_ATTR                long_description_content_type
          474_476  POP_JUMP_IF_FALSE   490  'to 490'

 L. 191       478  LOAD_FAST                'write_field'

 L. 192       480  LOAD_STR                 'Description-Content-Type'

 L. 193       482  LOAD_DEREF               'self'
              484  LOAD_ATTR                long_description_content_type

 L. 191       486  CALL_FUNCTION_2       2  ''
              488  POP_TOP          
            490_0  COME_FROM           474  '474'

 L. 195       490  LOAD_DEREF               'self'
              492  LOAD_ATTR                provides_extras
          494_496  POP_JUMP_IF_FALSE   522  'to 522'

 L. 196       498  LOAD_DEREF               'self'
              500  LOAD_ATTR                provides_extras
              502  GET_ITER         
              504  FOR_ITER            522  'to 522'
              506  STORE_FAST               'extra'

 L. 197       508  LOAD_FAST                'write_field'
              510  LOAD_STR                 'Provides-Extra'
              512  LOAD_FAST                'extra'
              514  CALL_FUNCTION_2       2  ''
              516  POP_TOP          
          518_520  JUMP_BACK           504  'to 504'
            522_0  COME_FROM           494  '494'

Parse error at or near `<117>' instruction at offset 184


sequence = (
 tuple, list)

def check_importable--- This code section failed: ---

 L. 204         0  SETUP_FINALLY        32  'to 32'

 L. 205         2  LOAD_GLOBAL              pkg_resources
                4  LOAD_ATTR                EntryPoint
                6  LOAD_METHOD              parse
                8  LOAD_STR                 'x='
               10  LOAD_FAST                'value'
               12  BINARY_ADD       
               14  CALL_METHOD_1         1  ''
               16  STORE_FAST               'ep'

 L. 206        18  LOAD_FAST                'ep'
               20  LOAD_ATTR                extras
               22  POP_JUMP_IF_FALSE    28  'to 28'
               24  <74>             
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            22  '22'
               28  POP_BLOCK        
               30  JUMP_FORWARD         94  'to 94'
             32_0  COME_FROM_FINALLY     0  '0'

 L. 207        32  DUP_TOP          
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

 L. 208        54  LOAD_GLOBAL              DistutilsSetupError

 L. 209        56  LOAD_STR                 "%r must be importable 'module:attrs' string (got %r)"

 L. 210        58  LOAD_FAST                'attr'
               60  LOAD_FAST                'value'
               62  BUILD_TUPLE_2         2 

 L. 209        64  BINARY_MODULO    

 L. 208        66  CALL_FUNCTION_1       1  ''

 L. 211        68  LOAD_FAST                'e'

 L. 208        70  RAISE_VARARGS_2       2  'exception instance with __cause__'
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

 L. 216         0  SETUP_FINALLY        42  'to 42'

 L. 219         2  LOAD_GLOBAL              isinstance
                4  LOAD_FAST                'value'
                6  LOAD_GLOBAL              list
                8  LOAD_GLOBAL              tuple
               10  BUILD_TUPLE_2         2 
               12  CALL_FUNCTION_2       2  ''
               14  POP_JUMP_IF_TRUE     20  'to 20'
               16  <74>             
               18  RAISE_VARARGS_1       1  'exception instance'
             20_0  COME_FROM            14  '14'

 L. 221        20  LOAD_STR                 ''
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

 L. 222        42  DUP_TOP          
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

 L. 223        64  LOAD_GLOBAL              DistutilsSetupError

 L. 224        66  LOAD_STR                 '%r must be a list of strings (got %r)'
               68  LOAD_FAST                'attr'
               70  LOAD_FAST                'value'
               72  BUILD_TUPLE_2         2 
               74  BINARY_MODULO    

 L. 223        76  CALL_FUNCTION_1       1  ''

 L. 225        78  LOAD_FAST                'e'

 L. 223        80  RAISE_VARARGS_2       2  'exception instance with __cause__'
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

 L. 230         0  LOAD_FAST                'value'
                2  STORE_FAST               'ns_packages'

 L. 231         4  LOAD_GLOBAL              assert_string_list
                6  LOAD_FAST                'dist'
                8  LOAD_FAST                'attr'
               10  LOAD_FAST                'ns_packages'
               12  CALL_FUNCTION_3       3  ''
               14  POP_TOP          

 L. 232        16  LOAD_FAST                'ns_packages'
               18  GET_ITER         
             20_0  COME_FROM            76  '76'
             20_1  COME_FROM            68  '68'
               20  FOR_ITER             96  'to 96'
               22  STORE_FAST               'nsp'

 L. 233        24  LOAD_FAST                'dist'
               26  LOAD_METHOD              has_contents_for
               28  LOAD_FAST                'nsp'
               30  CALL_METHOD_1         1  ''
               32  POP_JUMP_IF_TRUE     50  'to 50'

 L. 234        34  LOAD_GLOBAL              DistutilsSetupError

 L. 235        36  LOAD_STR                 'Distribution contains no modules or packages for '

 L. 236        38  LOAD_STR                 'namespace package %r'
               40  LOAD_FAST                'nsp'
               42  BINARY_MODULO    

 L. 235        44  BINARY_ADD       

 L. 234        46  CALL_FUNCTION_1       1  ''
               48  RAISE_VARARGS_1       1  'exception instance'
             50_0  COME_FROM            32  '32'

 L. 238        50  LOAD_FAST                'nsp'
               52  LOAD_METHOD              rpartition
               54  LOAD_STR                 '.'
               56  CALL_METHOD_1         1  ''
               58  UNPACK_SEQUENCE_3     3 
               60  STORE_FAST               'parent'
               62  STORE_FAST               'sep'
               64  STORE_FAST               'child'

 L. 239        66  LOAD_FAST                'parent'
               68  POP_JUMP_IF_FALSE    20  'to 20'
               70  LOAD_FAST                'parent'
               72  LOAD_FAST                'ns_packages'
               74  <118>                 1  ''
               76  POP_JUMP_IF_FALSE    20  'to 20'

 L. 240        78  LOAD_GLOBAL              distutils
               80  LOAD_ATTR                log
               82  LOAD_METHOD              warn

 L. 241        84  LOAD_STR                 'WARNING: %r is declared as a package namespace, but %r is not: please correct this in setup.py'

 L. 242        86  LOAD_FAST                'nsp'
               88  LOAD_FAST                'parent'

 L. 240        90  CALL_METHOD_3         3  ''
               92  POP_TOP          
               94  JUMP_BACK            20  'to 20'

Parse error at or near `<118>' instruction at offset 74


def check_extras--- This code section failed: ---

 L. 248         0  SETUP_FINALLY        26  'to 26'

 L. 249         2  LOAD_GLOBAL              list
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

 L. 250        26  DUP_TOP          
               28  LOAD_GLOBAL              TypeError
               30  LOAD_GLOBAL              ValueError
               32  LOAD_GLOBAL              AttributeError
               34  BUILD_TUPLE_3         3 
               36  <121>                76  ''
               38  POP_TOP          
               40  STORE_FAST               'e'
               42  POP_TOP          
               44  SETUP_FINALLY        68  'to 68'

 L. 251        46  LOAD_GLOBAL              DistutilsSetupError

 L. 252        48  LOAD_STR                 "'extras_require' must be a dictionary whose values are strings or lists of strings containing valid project/version requirement specifiers."

 L. 251        50  CALL_FUNCTION_1       1  ''

 L. 255        52  LOAD_FAST                'e'

 L. 251        54  RAISE_VARARGS_2       2  'exception instance with __cause__'
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
    name, sep, marker = extra.partition':'
    if marker:
        if pkg_resources.invalid_markermarker:
            raise DistutilsSetupError('Invalid environment marker: ' + marker)
    list(pkg_resources.parse_requirementsreqs)


def assert_bool(dist, attr, value):
    """Verify that value is True, False, 0, or 1"""
    if bool(value) != value:
        tmpl = '{attr!r} must be a boolean value (got {value!r})'
        raise DistutilsSetupError(tmpl.format(attr=attr, value=value))


def check_requirements--- This code section failed: ---

 L. 274         0  SETUP_FINALLY        42  'to 42'

 L. 275         2  LOAD_GLOBAL              list
                4  LOAD_GLOBAL              pkg_resources
                6  LOAD_METHOD              parse_requirements
                8  LOAD_FAST                'value'
               10  CALL_METHOD_1         1  ''
               12  CALL_FUNCTION_1       1  ''
               14  POP_TOP          

 L. 276        16  LOAD_GLOBAL              isinstance
               18  LOAD_FAST                'value'
               20  LOAD_GLOBAL              dict
               22  LOAD_GLOBAL              set
               24  BUILD_TUPLE_2         2 
               26  CALL_FUNCTION_2       2  ''
               28  POP_JUMP_IF_FALSE    38  'to 38'

 L. 277        30  LOAD_GLOBAL              TypeError
               32  LOAD_STR                 'Unordered types are not allowed'
               34  CALL_FUNCTION_1       1  ''
               36  RAISE_VARARGS_1       1  'exception instance'
             38_0  COME_FROM            28  '28'
               38  POP_BLOCK        
               40  JUMP_FORWARD        106  'to 106'
             42_0  COME_FROM_FINALLY     0  '0'

 L. 278        42  DUP_TOP          
               44  LOAD_GLOBAL              TypeError
               46  LOAD_GLOBAL              ValueError
               48  BUILD_TUPLE_2         2 
               50  <121>               104  ''
               52  POP_TOP          
               54  STORE_FAST               'error'
               56  POP_TOP          
               58  SETUP_FINALLY        96  'to 96'

 L. 280        60  LOAD_STR                 '{attr!r} must be a string or list of strings containing valid project/version requirement specifiers; {error}'

 L. 279        62  STORE_FAST               'tmpl'

 L. 283        64  LOAD_GLOBAL              DistutilsSetupError

 L. 284        66  LOAD_FAST                'tmpl'
               68  LOAD_ATTR                format
               70  LOAD_FAST                'attr'
               72  LOAD_FAST                'error'
               74  LOAD_CONST               ('attr', 'error')
               76  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 283        78  CALL_FUNCTION_1       1  ''

 L. 285        80  LOAD_FAST                'error'

 L. 283        82  RAISE_VARARGS_2       2  'exception instance with __cause__'
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

 L. 290         0  SETUP_FINALLY        18  'to 18'

 L. 291         2  LOAD_GLOBAL              packaging
                4  LOAD_ATTR                specifiers
                6  LOAD_METHOD              SpecifierSet
                8  LOAD_FAST                'value'
               10  CALL_METHOD_1         1  ''
               12  POP_TOP          
               14  POP_BLOCK        
               16  JUMP_FORWARD         82  'to 82'
             18_0  COME_FROM_FINALLY     0  '0'

 L. 292        18  DUP_TOP          
               20  LOAD_GLOBAL              packaging
               22  LOAD_ATTR                specifiers
               24  LOAD_ATTR                InvalidSpecifier
               26  <121>                80  ''
               28  POP_TOP          
               30  STORE_FAST               'error'
               32  POP_TOP          
               34  SETUP_FINALLY        72  'to 72'

 L. 294        36  LOAD_STR                 '{attr!r} must be a string containing valid version specifiers; {error}'

 L. 293        38  STORE_FAST               'tmpl'

 L. 297        40  LOAD_GLOBAL              DistutilsSetupError

 L. 298        42  LOAD_FAST                'tmpl'
               44  LOAD_ATTR                format
               46  LOAD_FAST                'attr'
               48  LOAD_FAST                'error'
               50  LOAD_CONST               ('attr', 'error')
               52  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 297        54  CALL_FUNCTION_1       1  ''

 L. 299        56  LOAD_FAST                'error'

 L. 297        58  RAISE_VARARGS_2       2  'exception instance with __cause__'
               60  POP_BLOCK        
               62  POP_EXCEPT       
               64  LOAD_CONST               None
               66  STORE_FAST               'error'
               68  DELETE_FAST              'error'
               70  JUMP_FORWARD         82  'to 82'
             72_0  COME_FROM_FINALLY    34  '34'
               72  LOAD_CONST               None
               74  STORE_FAST               'error'
               76  DELETE_FAST              'error'
               78  <48>             
               80  <48>             
             82_0  COME_FROM            70  '70'
             82_1  COME_FROM            16  '16'

Parse error at or near `<121>' instruction at offset 26


def check_entry_points--- This code section failed: ---

 L. 304         0  SETUP_FINALLY        18  'to 18'

 L. 305         2  LOAD_GLOBAL              pkg_resources
                4  LOAD_ATTR                EntryPoint
                6  LOAD_METHOD              parse_map
                8  LOAD_FAST                'value'
               10  CALL_METHOD_1         1  ''
               12  POP_TOP          
               14  POP_BLOCK        
               16  JUMP_FORWARD         64  'to 64'
             18_0  COME_FROM_FINALLY     0  '0'

 L. 306        18  DUP_TOP          
               20  LOAD_GLOBAL              ValueError
               22  <121>                62  ''
               24  POP_TOP          
               26  STORE_FAST               'e'
               28  POP_TOP          
               30  SETUP_FINALLY        54  'to 54'

 L. 307        32  LOAD_GLOBAL              DistutilsSetupError
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
    if not isinstancevaluesix.string_types:
        raise DistutilsSetupError('test_suite must be a string')


def check_package_data(dist, attr, value):
    """Verify that value is a dictionary of package names to glob lists"""
    if not isinstancevaluedict:
        raise DistutilsSetupError('{!r} must be a dictionary mapping package names to lists of string wildcard patterns'.formatattr)
    for k, v in value.items:
        if not isinstanceksix.string_types:
            raise DistutilsSetupError('keys of {!r} dict must be strings (got {!r})'.format(attr, k))
        assert_string_list(dist, 'values of {!r} dict'.formatattr, v)


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

 L. 408         0  LOAD_FAST                'attrs'
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

 L. 409        20  LOAD_CONST               None
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L. 410        24  LOAD_GLOBAL              pkg_resources
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

 L. 411        46  LOAD_GLOBAL              pkg_resources
               48  LOAD_ATTR                working_set
               50  LOAD_ATTR                by_key
               52  LOAD_METHOD              get
               54  LOAD_FAST                'key'
               56  CALL_METHOD_1         1  ''
               58  STORE_FAST               'dist'

 L. 412        60  LOAD_FAST                'dist'
               62  LOAD_CONST               None
               64  <117>                 1  ''
               66  POP_JUMP_IF_FALSE   104  'to 104'
               68  LOAD_FAST                'dist'
               70  LOAD_METHOD              has_metadata
               72  LOAD_STR                 'PKG-INFO'
               74  CALL_METHOD_1         1  ''
               76  POP_JUMP_IF_TRUE    104  'to 104'

 L. 413        78  LOAD_GLOBAL              pkg_resources
               80  LOAD_METHOD              safe_version
               82  LOAD_GLOBAL              str
               84  LOAD_FAST                'attrs'
               86  LOAD_STR                 'version'
               88  BINARY_SUBSCR    
               90  CALL_FUNCTION_1       1  ''
               92  CALL_METHOD_1         1  ''
               94  LOAD_FAST                'dist'
               96  STORE_ATTR               _version

 L. 414        98  LOAD_FAST                'dist'
              100  LOAD_FAST                'self'
              102  STORE_ATTR               _patched_dist
            104_0  COME_FROM            76  '76'
            104_1  COME_FROM            66  '66'

Parse error at or near `None' instruction at offset -1

    def __init__--- This code section failed: ---

 L. 417         0  LOAD_GLOBAL              hasattr
                2  LOAD_DEREF               'self'
                4  LOAD_STR                 'package_data'
                6  CALL_FUNCTION_2       2  ''
                8  STORE_FAST               'have_package_data'

 L. 418        10  LOAD_FAST                'have_package_data'
               12  POP_JUMP_IF_TRUE     20  'to 20'

 L. 419        14  BUILD_MAP_0           0 
               16  LOAD_DEREF               'self'
               18  STORE_ATTR               package_data
             20_0  COME_FROM            12  '12'

 L. 420        20  LOAD_FAST                'attrs'
               22  JUMP_IF_TRUE_OR_POP    26  'to 26'
               24  BUILD_MAP_0           0 
             26_0  COME_FROM            22  '22'
               26  STORE_FAST               'attrs'

 L. 421        28  BUILD_LIST_0          0 
               30  LOAD_DEREF               'self'
               32  STORE_ATTR               dist_files

 L. 423        34  LOAD_FAST                'attrs'
               36  LOAD_METHOD              pop
               38  LOAD_STR                 'src_root'
               40  LOAD_CONST               None
               42  CALL_METHOD_2         2  ''
               44  LOAD_DEREF               'self'
               46  STORE_ATTR               src_root

 L. 424        48  LOAD_DEREF               'self'
               50  LOAD_METHOD              patch_missing_pkg_info
               52  LOAD_FAST                'attrs'
               54  CALL_METHOD_1         1  ''
               56  POP_TOP          

 L. 425        58  LOAD_FAST                'attrs'
               60  LOAD_METHOD              pop
               62  LOAD_STR                 'dependency_links'
               64  BUILD_LIST_0          0 
               66  CALL_METHOD_2         2  ''
               68  LOAD_DEREF               'self'
               70  STORE_ATTR               dependency_links

 L. 426        72  LOAD_FAST                'attrs'
               74  LOAD_METHOD              pop
               76  LOAD_STR                 'setup_requires'
               78  BUILD_LIST_0          0 
               80  CALL_METHOD_2         2  ''
               82  LOAD_DEREF               'self'
               84  STORE_ATTR               setup_requires

 L. 427        86  LOAD_GLOBAL              pkg_resources
               88  LOAD_METHOD              iter_entry_points
               90  LOAD_STR                 'distutils.setup_keywords'
               92  CALL_METHOD_1         1  ''
               94  GET_ITER         
               96  FOR_ITER            120  'to 120'
               98  STORE_FAST               'ep'

 L. 428       100  LOAD_GLOBAL              vars
              102  LOAD_DEREF               'self'
              104  CALL_FUNCTION_1       1  ''
              106  LOAD_METHOD              setdefault
              108  LOAD_FAST                'ep'
              110  LOAD_ATTR                name
              112  LOAD_CONST               None
              114  CALL_METHOD_2         2  ''
              116  POP_TOP          
              118  JUMP_BACK            96  'to 96'

 L. 429       120  LOAD_GLOBAL              _Distribution
              122  LOAD_METHOD              __init__
              124  LOAD_DEREF               'self'
              126  LOAD_CLOSURE             'self'
              128  BUILD_TUPLE_1         1 
              130  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              132  LOAD_STR                 'Distribution.__init__.<locals>.<dictcomp>'
              134  MAKE_FUNCTION_8          'closure'

 L. 430       136  LOAD_FAST                'attrs'
              138  LOAD_METHOD              items
              140  CALL_METHOD_0         0  ''

 L. 429       142  GET_ITER         
              144  CALL_FUNCTION_1       1  ''
              146  CALL_METHOD_2         2  ''
              148  POP_TOP          

 L. 437       150  LOAD_DEREF               'self'
              152  LOAD_ATTR                _DISTUTILS_UNSUPPORTED_METADATA
              154  LOAD_METHOD              items
              156  CALL_METHOD_0         0  ''
              158  GET_ITER         
              160  FOR_ITER            236  'to 236'
              162  UNPACK_SEQUENCE_2     2 
              164  STORE_FAST               'option'
              166  STORE_FAST               'default'

 L. 438       168  LOAD_DEREF               'self'
              170  LOAD_ATTR                metadata
              172  LOAD_ATTR                __dict__
              174  LOAD_FAST                'attrs'
              176  BUILD_TUPLE_2         2 
              178  GET_ITER         
            180_0  COME_FROM           190  '190'
              180  FOR_ITER            206  'to 206'
              182  STORE_FAST               'source'

 L. 439       184  LOAD_FAST                'option'
              186  LOAD_FAST                'source'
              188  <118>                 0  ''
              190  POP_JUMP_IF_FALSE   180  'to 180'

 L. 440       192  LOAD_FAST                'source'
              194  LOAD_FAST                'option'
              196  BINARY_SUBSCR    
              198  STORE_FAST               'value'

 L. 441       200  POP_TOP          
              202  BREAK_LOOP          220  'to 220'
              204  JUMP_BACK           180  'to 180'

 L. 443       206  LOAD_FAST                'default'
              208  POP_JUMP_IF_FALSE   216  'to 216'
              210  LOAD_FAST                'default'
              212  CALL_FUNCTION_0       0  ''
              214  JUMP_FORWARD        218  'to 218'
            216_0  COME_FROM           208  '208'
              216  LOAD_CONST               None
            218_0  COME_FROM           214  '214'
              218  STORE_FAST               'value'

 L. 444       220  LOAD_GLOBAL              setattr
              222  LOAD_DEREF               'self'
              224  LOAD_ATTR                metadata
              226  LOAD_FAST                'option'
              228  LOAD_FAST                'value'
              230  CALL_FUNCTION_3       3  ''
              232  POP_TOP          
              234  JUMP_BACK           160  'to 160'

 L. 446       236  LOAD_DEREF               'self'
              238  LOAD_METHOD              _normalize_version

 L. 447       240  LOAD_DEREF               'self'
              242  LOAD_METHOD              _validate_version
              244  LOAD_DEREF               'self'
              246  LOAD_ATTR                metadata
              248  LOAD_ATTR                version
              250  CALL_METHOD_1         1  ''

 L. 446       252  CALL_METHOD_1         1  ''
              254  LOAD_DEREF               'self'
              256  LOAD_ATTR                metadata
              258  STORE_ATTR               version

 L. 448       260  LOAD_DEREF               'self'
              262  LOAD_METHOD              _finalize_requires
              264  CALL_METHOD_0         0  ''
              266  POP_TOP          

Parse error at or near `LOAD_DICTCOMP' instruction at offset 130

    @staticmethod
    def _normalize_version--- This code section failed: ---

 L. 452         0  LOAD_GLOBAL              isinstance
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

 L. 453        20  LOAD_FAST                'version'
               22  RETURN_VALUE     
             24_0  COME_FROM            18  '18'

 L. 455        24  LOAD_GLOBAL              str
               26  LOAD_GLOBAL              packaging
               28  LOAD_ATTR                version
               30  LOAD_METHOD              Version
               32  LOAD_FAST                'version'
               34  CALL_METHOD_1         1  ''
               36  CALL_FUNCTION_1       1  ''
               38  STORE_FAST               'normalized'

 L. 456        40  LOAD_FAST                'version'
               42  LOAD_FAST                'normalized'
               44  COMPARE_OP               !=
               46  POP_JUMP_IF_FALSE    80  'to 80'

 L. 457        48  LOAD_STR                 "Normalizing '{version}' to '{normalized}'"
               50  STORE_FAST               'tmpl'

 L. 458        52  LOAD_GLOBAL              warnings
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

 L. 459        76  LOAD_FAST                'normalized'
               78  RETURN_VALUE     
             80_0  COME_FROM            46  '46'

 L. 460        80  LOAD_FAST                'version'
               82  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @staticmethod
    def _validate_version--- This code section failed: ---

 L. 464         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'version'
                4  LOAD_GLOBAL              numbers
                6  LOAD_ATTR                Number
                8  CALL_FUNCTION_2       2  ''
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L. 466        12  LOAD_GLOBAL              str
               14  LOAD_FAST                'version'
               16  CALL_FUNCTION_1       1  ''
               18  STORE_FAST               'version'
             20_0  COME_FROM            10  '10'

 L. 468        20  LOAD_FAST                'version'
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE    96  'to 96'

 L. 469        28  SETUP_FINALLY        46  'to 46'

 L. 470        30  LOAD_GLOBAL              packaging
               32  LOAD_ATTR                version
               34  LOAD_METHOD              Version
               36  LOAD_FAST                'version'
               38  CALL_METHOD_1         1  ''
               40  POP_TOP          
               42  POP_BLOCK        
               44  JUMP_FORWARD         96  'to 96'
             46_0  COME_FROM_FINALLY    28  '28'

 L. 471        46  DUP_TOP          
               48  LOAD_GLOBAL              packaging
               50  LOAD_ATTR                version
               52  LOAD_ATTR                InvalidVersion
               54  LOAD_GLOBAL              TypeError
               56  BUILD_TUPLE_2         2 
               58  <121>                94  ''
               60  POP_TOP          
               62  POP_TOP          
               64  POP_TOP          

 L. 472        66  LOAD_GLOBAL              warnings
               68  LOAD_METHOD              warn

 L. 473        70  LOAD_STR                 'The version specified (%r) is an invalid version, this may not work as expected with newer versions of setuptools, pip, and PyPI. Please see PEP 440 for more details.'

 L. 476        72  LOAD_FAST                'version'

 L. 473        74  BINARY_MODULO    

 L. 472        76  CALL_METHOD_1         1  ''
               78  POP_TOP          

 L. 478        80  LOAD_GLOBAL              setuptools
               82  LOAD_METHOD              sic
               84  LOAD_FAST                'version'
               86  CALL_METHOD_1         1  ''
               88  ROT_FOUR         
               90  POP_EXCEPT       
               92  RETURN_VALUE     
               94  <48>             
             96_0  COME_FROM            44  '44'
             96_1  COME_FROM            26  '26'

 L. 479        96  LOAD_FAST                'version'
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
            for extra in self.extras_require.keys:
                extra = extra.split':'[0]
                if extra:
                    self.metadata.provides_extras.addextra

        self._convert_extras_requirements
        self._move_install_requirements_markers

    def _convert_extras_requirements(self):
        """
        Convert requirements in `extras_require` of the form
        `"extra": ["barbazquux; {marker}"]` to
        `"extra:{marker}": ["barbazquux"]`.
        """
        spec_ext_reqs = getattr(self, 'extras_require', None) or {}
        self._tmp_extras_require = defaultdict(list)
        for section, v in spec_ext_reqs.items:
            self._tmp_extras_require[section]
            for r in pkg_resources.parse_requirementsv:
                suffix = self._suffix_forr
                self._tmp_extras_require[(section + suffix)].appendr

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
        inst_reqs = list(pkg_resources.parse_requirementsspec_inst_reqs)
        simple_reqs = filteris_simple_reqinst_reqs
        complex_reqs = filterfalseis_simple_reqinst_reqs
        self.install_requires = list(mapstrsimple_reqs)
        for r in complex_reqs:
            self._tmp_extras_require[(':' + str(r.marker))].appendr
        else:
            self.extras_require = dict(((
             k, [str(r) for r in mapself._clean_reqv]) for k, v in self._tmp_extras_require.items))

    def _clean_req(self, req):
        """
        Given a Requirement, remove environment markers and return it.
        """
        req.marker = None
        return req

    def _parse_config_files--- This code section failed: ---

 L. 563         0  LOAD_CONST               0
                2  LOAD_CONST               ('ConfigParser',)
                4  IMPORT_NAME_ATTR         setuptools.extern.six.moves.configparser
                6  IMPORT_FROM              ConfigParser
                8  STORE_FAST               'ConfigParser'
               10  POP_TOP          

 L. 566        12  LOAD_GLOBAL              six
               14  LOAD_ATTR                PY2
               16  POP_JUMP_IF_TRUE     40  'to 40'
               18  LOAD_GLOBAL              sys
               20  LOAD_ATTR                prefix
               22  LOAD_GLOBAL              sys
               24  LOAD_ATTR                base_prefix
               26  COMPARE_OP               !=
               28  POP_JUMP_IF_FALSE    40  'to 40'

 L. 567        30  BUILD_LIST_0          0 
               32  LOAD_CONST               ('install-base', 'install-platbase', 'install-lib', 'install-platlib', 'install-purelib', 'install-headers', 'install-scripts', 'install-data', 'prefix', 'exec-prefix', 'home', 'user', 'root')
               34  CALL_FINALLY         37  'to 37'
               36  STORE_FAST               'ignore_options'
               38  JUMP_FORWARD         44  'to 44'
             40_0  COME_FROM            28  '28'
             40_1  COME_FROM            16  '16'

 L. 573        40  BUILD_LIST_0          0 
               42  STORE_FAST               'ignore_options'
             44_0  COME_FROM            38  '38'

 L. 575        44  LOAD_GLOBAL              frozenset
               46  LOAD_FAST                'ignore_options'
               48  CALL_FUNCTION_1       1  ''
               50  STORE_FAST               'ignore_options'

 L. 577        52  LOAD_FAST                'filenames'
               54  LOAD_CONST               None
               56  <117>                 0  ''
               58  POP_JUMP_IF_FALSE    68  'to 68'

 L. 578        60  LOAD_FAST                'self'
               62  LOAD_METHOD              find_config_files
               64  CALL_METHOD_0         0  ''
               66  STORE_FAST               'filenames'
             68_0  COME_FROM            58  '58'

 L. 580        68  LOAD_GLOBAL              DEBUG
               70  POP_JUMP_IF_FALSE    82  'to 82'

 L. 581        72  LOAD_FAST                'self'
               74  LOAD_METHOD              announce
               76  LOAD_STR                 'Distribution.parse_config_files():'
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          
             82_0  COME_FROM            70  '70'

 L. 583        82  LOAD_FAST                'ConfigParser'
               84  CALL_FUNCTION_0       0  ''
               86  STORE_FAST               'parser'

 L. 584        88  LOAD_FAST                'filenames'
               90  GET_ITER         
               92  FOR_ITER            304  'to 304'
               94  STORE_FAST               'filename'

 L. 585        96  LOAD_GLOBAL              io
               98  LOAD_ATTR                open
              100  LOAD_FAST                'filename'
              102  LOAD_STR                 'utf-8'
              104  LOAD_CONST               ('encoding',)
              106  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              108  SETUP_WITH          176  'to 176'
              110  STORE_FAST               'reader'

 L. 586       112  LOAD_GLOBAL              DEBUG
              114  POP_JUMP_IF_FALSE   140  'to 140'

 L. 587       116  LOAD_FAST                'self'
              118  LOAD_METHOD              announce
              120  LOAD_STR                 '  reading {filename}'
              122  LOAD_ATTR                format
              124  BUILD_TUPLE_0         0 
              126  BUILD_MAP_0           0 
              128  LOAD_GLOBAL              locals
              130  CALL_FUNCTION_0       0  ''
              132  <164>                 1  ''
              134  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              136  CALL_METHOD_1         1  ''
              138  POP_TOP          
            140_0  COME_FROM           114  '114'

 L. 588       140  LOAD_GLOBAL              six
              142  LOAD_ATTR                PY2
              144  POP_JUMP_IF_FALSE   152  'to 152'
              146  LOAD_FAST                'parser'
              148  LOAD_ATTR                readfp
              150  JUMP_FORWARD        156  'to 156'
            152_0  COME_FROM           144  '144'
              152  LOAD_FAST                'parser'
              154  LOAD_ATTR                read_file
            156_0  COME_FROM           150  '150'
              156  LOAD_FAST                'reader'
              158  CALL_FUNCTION_1       1  ''
              160  POP_TOP          
              162  POP_BLOCK        
              164  LOAD_CONST               None
              166  DUP_TOP          
              168  DUP_TOP          
              170  CALL_FUNCTION_3       3  ''
              172  POP_TOP          
              174  JUMP_FORWARD        192  'to 192'
            176_0  COME_FROM_WITH      108  '108'
              176  <49>             
              178  POP_JUMP_IF_TRUE    182  'to 182'
              180  <48>             
            182_0  COME_FROM           178  '178'
              182  POP_TOP          
              184  POP_TOP          
              186  POP_TOP          
              188  POP_EXCEPT       
              190  POP_TOP          
            192_0  COME_FROM           174  '174'

 L. 589       192  LOAD_FAST                'parser'
              194  LOAD_METHOD              sections
              196  CALL_METHOD_0         0  ''
              198  GET_ITER         
              200  FOR_ITER            294  'to 294'
              202  STORE_FAST               'section'

 L. 590       204  LOAD_FAST                'parser'
              206  LOAD_METHOD              options
              208  LOAD_FAST                'section'
              210  CALL_METHOD_1         1  ''
              212  STORE_FAST               'options'

 L. 591       214  LOAD_FAST                'self'
              216  LOAD_METHOD              get_option_dict
              218  LOAD_FAST                'section'
              220  CALL_METHOD_1         1  ''
              222  STORE_FAST               'opt_dict'

 L. 593       224  LOAD_FAST                'options'
              226  GET_ITER         
            228_0  COME_FROM           246  '246'
            228_1  COME_FROM           238  '238'
              228  FOR_ITER            292  'to 292'
              230  STORE_FAST               'opt'

 L. 594       232  LOAD_FAST                'opt'
              234  LOAD_STR                 '__name__'
              236  COMPARE_OP               !=
              238  POP_JUMP_IF_FALSE   228  'to 228'
              240  LOAD_FAST                'opt'
              242  LOAD_FAST                'ignore_options'
              244  <118>                 1  ''
              246  POP_JUMP_IF_FALSE   228  'to 228'

 L. 595       248  LOAD_FAST                'self'
              250  LOAD_METHOD              _try_str
              252  LOAD_FAST                'parser'
              254  LOAD_METHOD              get
              256  LOAD_FAST                'section'
              258  LOAD_FAST                'opt'
              260  CALL_METHOD_2         2  ''
              262  CALL_METHOD_1         1  ''
              264  STORE_FAST               'val'

 L. 596       266  LOAD_FAST                'opt'
              268  LOAD_METHOD              replace
              270  LOAD_STR                 '-'
              272  LOAD_STR                 '_'
              274  CALL_METHOD_2         2  ''
              276  STORE_FAST               'opt'

 L. 597       278  LOAD_FAST                'filename'
              280  LOAD_FAST                'val'
              282  BUILD_TUPLE_2         2 
              284  LOAD_FAST                'opt_dict'
              286  LOAD_FAST                'opt'
              288  STORE_SUBSCR     
              290  JUMP_BACK           228  'to 228'
              292  JUMP_BACK           200  'to 200'

 L. 601       294  LOAD_FAST                'parser'
              296  LOAD_METHOD              __init__
              298  CALL_METHOD_0         0  ''
              300  POP_TOP          
              302  JUMP_BACK            92  'to 92'

 L. 606       304  LOAD_STR                 'global'
              306  LOAD_FAST                'self'
              308  LOAD_ATTR                command_options
              310  <118>                 0  ''
          312_314  POP_JUMP_IF_FALSE   478  'to 478'

 L. 607       316  LOAD_FAST                'self'
              318  LOAD_ATTR                command_options
              320  LOAD_STR                 'global'
              322  BINARY_SUBSCR    
              324  LOAD_METHOD              items
              326  CALL_METHOD_0         0  ''
              328  GET_ITER         
              330  FOR_ITER            478  'to 478'
              332  UNPACK_SEQUENCE_2     2 
              334  STORE_FAST               'opt'
              336  UNPACK_SEQUENCE_2     2 
              338  STORE_FAST               'src'
              340  STORE_FAST               'val'

 L. 608       342  LOAD_FAST                'self'
              344  LOAD_ATTR                negative_opt
              346  LOAD_METHOD              get
              348  LOAD_FAST                'opt'
              350  CALL_METHOD_1         1  ''
              352  STORE_FAST               'alias'

 L. 609       354  SETUP_FINALLY       426  'to 426'

 L. 610       356  LOAD_FAST                'alias'
          358_360  POP_JUMP_IF_FALSE   382  'to 382'

 L. 611       362  LOAD_GLOBAL              setattr
              364  LOAD_FAST                'self'
              366  LOAD_FAST                'alias'
              368  LOAD_GLOBAL              strtobool
              370  LOAD_FAST                'val'
              372  CALL_FUNCTION_1       1  ''
              374  UNARY_NOT        
              376  CALL_FUNCTION_3       3  ''
              378  POP_TOP          
              380  JUMP_FORWARD        422  'to 422'
            382_0  COME_FROM           358  '358'

 L. 612       382  LOAD_FAST                'opt'
              384  LOAD_CONST               ('verbose', 'dry_run')
              386  <118>                 0  ''
          388_390  POP_JUMP_IF_FALSE   410  'to 410'

 L. 613       392  LOAD_GLOBAL              setattr
              394  LOAD_FAST                'self'
              396  LOAD_FAST                'opt'
              398  LOAD_GLOBAL              strtobool
              400  LOAD_FAST                'val'
              402  CALL_FUNCTION_1       1  ''
              404  CALL_FUNCTION_3       3  ''
              406  POP_TOP          
              408  JUMP_FORWARD        422  'to 422'
            410_0  COME_FROM           388  '388'

 L. 615       410  LOAD_GLOBAL              setattr
              412  LOAD_FAST                'self'
              414  LOAD_FAST                'opt'
              416  LOAD_FAST                'val'
              418  CALL_FUNCTION_3       3  ''
              420  POP_TOP          
            422_0  COME_FROM           408  '408'
            422_1  COME_FROM           380  '380'
              422  POP_BLOCK        
              424  JUMP_BACK           330  'to 330'
            426_0  COME_FROM_FINALLY   354  '354'

 L. 616       426  DUP_TOP          
              428  LOAD_GLOBAL              ValueError
          430_432  <121>               472  ''
              434  POP_TOP          
              436  STORE_FAST               'e'
              438  POP_TOP          
              440  SETUP_FINALLY       464  'to 464'

 L. 617       442  LOAD_GLOBAL              DistutilsOptionError
              444  LOAD_FAST                'e'
              446  CALL_FUNCTION_1       1  ''
              448  LOAD_FAST                'e'
              450  RAISE_VARARGS_2       2  'exception instance with __cause__'
              452  POP_BLOCK        
              454  POP_EXCEPT       
              456  LOAD_CONST               None
              458  STORE_FAST               'e'
              460  DELETE_FAST              'e'
              462  JUMP_BACK           330  'to 330'
            464_0  COME_FROM_FINALLY   440  '440'
              464  LOAD_CONST               None
              466  STORE_FAST               'e'
              468  DELETE_FAST              'e'
              470  <48>             
              472  <48>             
          474_476  JUMP_BACK           330  'to 330'
            478_0  COME_FROM           312  '312'

Parse error at or near `CALL_FINALLY' instruction at offset 34

    @staticmethod
    def _try_str--- This code section failed: ---

 L. 631         0  LOAD_GLOBAL              six
                2  LOAD_ATTR                PY2
                4  POP_JUMP_IF_TRUE     10  'to 10'

 L. 632         6  LOAD_FAST                'val'
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L. 633        10  SETUP_FINALLY        22  'to 22'

 L. 634        12  LOAD_FAST                'val'
               14  LOAD_METHOD              encode
               16  CALL_METHOD_0         0  ''
               18  POP_BLOCK        
               20  RETURN_VALUE     
             22_0  COME_FROM_FINALLY    10  '10'

 L. 635        22  DUP_TOP          
               24  LOAD_GLOBAL              UnicodeEncodeError
               26  <121>                38  ''
               28  POP_TOP          
               30  POP_TOP          
               32  POP_TOP          

 L. 636        34  POP_EXCEPT       
               36  JUMP_FORWARD         40  'to 40'
               38  <48>             
             40_0  COME_FROM            36  '36'

 L. 637        40  LOAD_FAST                'val'
               42  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<121>' instruction at offset 26

    def _set_command_options--- This code section failed: ---

 L. 651         0  LOAD_FAST                'command_obj'
                2  LOAD_METHOD              get_command_name
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'command_name'

 L. 652         8  LOAD_FAST                'option_dict'
               10  LOAD_CONST               None
               12  <117>                 0  ''
               14  POP_JUMP_IF_FALSE    26  'to 26'

 L. 653        16  LOAD_FAST                'self'
               18  LOAD_METHOD              get_option_dict
               20  LOAD_FAST                'command_name'
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'option_dict'
             26_0  COME_FROM            14  '14'

 L. 655        26  LOAD_GLOBAL              DEBUG
               28  POP_JUMP_IF_FALSE    44  'to 44'

 L. 656        30  LOAD_FAST                'self'
               32  LOAD_METHOD              announce
               34  LOAD_STR                 "  setting options for '%s' command:"
               36  LOAD_FAST                'command_name'
               38  BINARY_MODULO    
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          
             44_0  COME_FROM            28  '28'

 L. 657        44  LOAD_FAST                'option_dict'
               46  LOAD_METHOD              items
               48  CALL_METHOD_0         0  ''
               50  GET_ITER         
            52_54  FOR_ITER            346  'to 346'
               56  UNPACK_SEQUENCE_2     2 
               58  STORE_FAST               'option'
               60  UNPACK_SEQUENCE_2     2 
               62  STORE_FAST               'source'
               64  STORE_FAST               'value'

 L. 658        66  LOAD_GLOBAL              DEBUG
               68  POP_JUMP_IF_FALSE    90  'to 90'

 L. 659        70  LOAD_FAST                'self'
               72  LOAD_METHOD              announce
               74  LOAD_STR                 '    %s = %s (from %s)'
               76  LOAD_FAST                'option'
               78  LOAD_FAST                'value'

 L. 660        80  LOAD_FAST                'source'

 L. 659        82  BUILD_TUPLE_3         3 
               84  BINARY_MODULO    
               86  CALL_METHOD_1         1  ''
               88  POP_TOP          
             90_0  COME_FROM            68  '68'

 L. 661        90  SETUP_FINALLY       112  'to 112'

 L. 662        92  LOAD_LISTCOMP            '<code_object <listcomp>>'
               94  LOAD_STR                 'Distribution._set_command_options.<locals>.<listcomp>'
               96  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 663        98  LOAD_FAST                'command_obj'
              100  LOAD_ATTR                boolean_options

 L. 662       102  GET_ITER         
              104  CALL_FUNCTION_1       1  ''
              106  STORE_FAST               'bool_opts'
              108  POP_BLOCK        
              110  JUMP_FORWARD        134  'to 134'
            112_0  COME_FROM_FINALLY    90  '90'

 L. 664       112  DUP_TOP          
              114  LOAD_GLOBAL              AttributeError
              116  <121>               132  ''
              118  POP_TOP          
              120  POP_TOP          
              122  POP_TOP          

 L. 665       124  BUILD_LIST_0          0 
              126  STORE_FAST               'bool_opts'
              128  POP_EXCEPT       
              130  JUMP_FORWARD        134  'to 134'
              132  <48>             
            134_0  COME_FROM           130  '130'
            134_1  COME_FROM           110  '110'

 L. 666       134  SETUP_FINALLY       146  'to 146'

 L. 667       136  LOAD_FAST                'command_obj'
              138  LOAD_ATTR                negative_opt
              140  STORE_FAST               'neg_opt'
              142  POP_BLOCK        
              144  JUMP_FORWARD        168  'to 168'
            146_0  COME_FROM_FINALLY   134  '134'

 L. 668       146  DUP_TOP          
              148  LOAD_GLOBAL              AttributeError
              150  <121>               166  ''
              152  POP_TOP          
              154  POP_TOP          
              156  POP_TOP          

 L. 669       158  BUILD_MAP_0           0 
              160  STORE_FAST               'neg_opt'
              162  POP_EXCEPT       
              164  JUMP_FORWARD        168  'to 168'
              166  <48>             
            168_0  COME_FROM           164  '164'
            168_1  COME_FROM           144  '144'

 L. 671       168  SETUP_FINALLY       296  'to 296'

 L. 672       170  LOAD_GLOBAL              isinstance
              172  LOAD_FAST                'value'
              174  LOAD_GLOBAL              six
              176  LOAD_ATTR                string_types
              178  CALL_FUNCTION_2       2  ''
              180  STORE_FAST               'is_string'

 L. 673       182  LOAD_FAST                'option'
              184  LOAD_FAST                'neg_opt'
              186  <118>                 0  ''
              188  POP_JUMP_IF_FALSE   218  'to 218'
              190  LOAD_FAST                'is_string'
              192  POP_JUMP_IF_FALSE   218  'to 218'

 L. 674       194  LOAD_GLOBAL              setattr
              196  LOAD_FAST                'command_obj'
              198  LOAD_FAST                'neg_opt'
              200  LOAD_FAST                'option'
              202  BINARY_SUBSCR    
              204  LOAD_GLOBAL              strtobool
              206  LOAD_FAST                'value'
              208  CALL_FUNCTION_1       1  ''
              210  UNARY_NOT        
              212  CALL_FUNCTION_3       3  ''
              214  POP_TOP          
              216  JUMP_FORWARD        292  'to 292'
            218_0  COME_FROM           192  '192'
            218_1  COME_FROM           188  '188'

 L. 675       218  LOAD_FAST                'option'
              220  LOAD_FAST                'bool_opts'
              222  <118>                 0  ''
              224  POP_JUMP_IF_FALSE   248  'to 248'
              226  LOAD_FAST                'is_string'
              228  POP_JUMP_IF_FALSE   248  'to 248'

 L. 676       230  LOAD_GLOBAL              setattr
              232  LOAD_FAST                'command_obj'
              234  LOAD_FAST                'option'
              236  LOAD_GLOBAL              strtobool
              238  LOAD_FAST                'value'
              240  CALL_FUNCTION_1       1  ''
              242  CALL_FUNCTION_3       3  ''
              244  POP_TOP          
              246  JUMP_FORWARD        292  'to 292'
            248_0  COME_FROM           228  '228'
            248_1  COME_FROM           224  '224'

 L. 677       248  LOAD_GLOBAL              hasattr
              250  LOAD_FAST                'command_obj'
              252  LOAD_FAST                'option'
              254  CALL_FUNCTION_2       2  ''
          256_258  POP_JUMP_IF_FALSE   274  'to 274'

 L. 678       260  LOAD_GLOBAL              setattr
              262  LOAD_FAST                'command_obj'
              264  LOAD_FAST                'option'
              266  LOAD_FAST                'value'
              268  CALL_FUNCTION_3       3  ''
              270  POP_TOP          
              272  JUMP_FORWARD        292  'to 292'
            274_0  COME_FROM           256  '256'

 L. 680       274  LOAD_GLOBAL              DistutilsOptionError

 L. 681       276  LOAD_STR                 "error in %s: command '%s' has no such option '%s'"

 L. 682       278  LOAD_FAST                'source'
              280  LOAD_FAST                'command_name'
              282  LOAD_FAST                'option'
              284  BUILD_TUPLE_3         3 

 L. 681       286  BINARY_MODULO    

 L. 680       288  CALL_FUNCTION_1       1  ''
              290  RAISE_VARARGS_1       1  'exception instance'
            292_0  COME_FROM           272  '272'
            292_1  COME_FROM           246  '246'
            292_2  COME_FROM           216  '216'
              292  POP_BLOCK        
              294  JUMP_BACK            52  'to 52'
            296_0  COME_FROM_FINALLY   168  '168'

 L. 683       296  DUP_TOP          
              298  LOAD_GLOBAL              ValueError
          300_302  <121>               342  ''
              304  POP_TOP          
              306  STORE_FAST               'e'
              308  POP_TOP          
              310  SETUP_FINALLY       334  'to 334'

 L. 684       312  LOAD_GLOBAL              DistutilsOptionError
              314  LOAD_FAST                'e'
              316  CALL_FUNCTION_1       1  ''
              318  LOAD_FAST                'e'
              320  RAISE_VARARGS_2       2  'exception instance with __cause__'
              322  POP_BLOCK        
              324  POP_EXCEPT       
              326  LOAD_CONST               None
              328  STORE_FAST               'e'
              330  DELETE_FAST              'e'
              332  JUMP_BACK            52  'to 52'
            334_0  COME_FROM_FINALLY   310  '310'
              334  LOAD_CONST               None
              336  STORE_FAST               'e'
              338  DELETE_FAST              'e'
              340  <48>             
              342  <48>             
              344  JUMP_BACK            52  'to 52'

Parse error at or near `<117>' instruction at offset 12

    def parse_config_files(self, filenames=None, ignore_option_errors=False):
        """Parses configuration files from various levels
        and loads configuration.

        """
        self._parse_config_files(filenames=filenames)
        parse_configuration(self, (self.command_options), ignore_option_errors=ignore_option_errors)
        self._finalize_requires

    def fetch_build_eggs(self, requires):
        """Resolve pre-setup requirements"""
        resolved_dists = pkg_resources.working_set.resolve((pkg_resources.parse_requirementsrequires),
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

        eps = map(lambda e: e.load)pkg_resources.iter_entry_pointsgroup
        for ep in sorted(eps, key=by_order):
            ep(self)

    def _finalize_setup_keywords--- This code section failed: ---

 L. 724         0  LOAD_GLOBAL              pkg_resources
                2  LOAD_METHOD              iter_entry_points
                4  LOAD_STR                 'distutils.setup_keywords'
                6  CALL_METHOD_1         1  ''
                8  GET_ITER         
             10_0  COME_FROM            34  '34'
               10  FOR_ITER             70  'to 70'
               12  STORE_FAST               'ep'

 L. 725        14  LOAD_GLOBAL              getattr
               16  LOAD_FAST                'self'
               18  LOAD_FAST                'ep'
               20  LOAD_ATTR                name
               22  LOAD_CONST               None
               24  CALL_FUNCTION_3       3  ''
               26  STORE_FAST               'value'

 L. 726        28  LOAD_FAST                'value'
               30  LOAD_CONST               None
               32  <117>                 1  ''
               34  POP_JUMP_IF_FALSE    10  'to 10'

 L. 727        36  LOAD_FAST                'ep'
               38  LOAD_ATTR                require
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                fetch_build_egg
               44  LOAD_CONST               ('installer',)
               46  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               48  POP_TOP          

 L. 728        50  LOAD_FAST                'ep'
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
            self.convert_2to3_doctests = [os.path.abspathp for p in self.convert_2to3_doctests]
        else:
            self.convert_2to3_doctests = []

    def get_egg_cache_dir--- This code section failed: ---

 L. 741         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              join
                6  LOAD_GLOBAL              os
                8  LOAD_ATTR                curdir
               10  LOAD_STR                 '.eggs'
               12  CALL_METHOD_2         2  ''
               14  STORE_FAST               'egg_cache_dir'

 L. 742        16  LOAD_GLOBAL              os
               18  LOAD_ATTR                path
               20  LOAD_METHOD              exists
               22  LOAD_FAST                'egg_cache_dir'
               24  CALL_METHOD_1         1  ''
               26  POP_JUMP_IF_TRUE    134  'to 134'

 L. 743        28  LOAD_GLOBAL              os
               30  LOAD_METHOD              mkdir
               32  LOAD_FAST                'egg_cache_dir'
               34  CALL_METHOD_1         1  ''
               36  POP_TOP          

 L. 744        38  LOAD_GLOBAL              windows_support
               40  LOAD_METHOD              hide_file
               42  LOAD_FAST                'egg_cache_dir'
               44  CALL_METHOD_1         1  ''
               46  POP_TOP          

 L. 745        48  LOAD_GLOBAL              os
               50  LOAD_ATTR                path
               52  LOAD_METHOD              join
               54  LOAD_FAST                'egg_cache_dir'
               56  LOAD_STR                 'README.txt'
               58  CALL_METHOD_2         2  ''
               60  STORE_FAST               'readme_txt_filename'

 L. 746        62  LOAD_GLOBAL              open
               64  LOAD_FAST                'readme_txt_filename'
               66  LOAD_STR                 'w'
               68  CALL_FUNCTION_2       2  ''
               70  SETUP_WITH          118  'to 118'
               72  STORE_FAST               'f'

 L. 747        74  LOAD_FAST                'f'
               76  LOAD_METHOD              write
               78  LOAD_STR                 'This directory contains eggs that were downloaded by setuptools to build, test, and run plug-ins.\n\n'
               80  CALL_METHOD_1         1  ''
               82  POP_TOP          

 L. 749        84  LOAD_FAST                'f'
               86  LOAD_METHOD              write
               88  LOAD_STR                 'This directory caches those eggs to prevent repeated downloads.\n\n'
               90  CALL_METHOD_1         1  ''
               92  POP_TOP          

 L. 751        94  LOAD_FAST                'f'
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

 L. 753       134  LOAD_FAST                'egg_cache_dir'
              136  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `DUP_TOP' instruction at offset 108

    def fetch_build_egg(self, req):
        """Fetch an egg needed for building"""
        from setuptools.installer import fetch_build_egg
        return fetch_build_eggselfreq

    def get_command_class--- This code section failed: ---

 L. 762         0  LOAD_FAST                'command'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                cmdclass
                6  <118>                 0  ''
                8  POP_JUMP_IF_FALSE    20  'to 20'

 L. 763        10  LOAD_FAST                'self'
               12  LOAD_ATTR                cmdclass
               14  LOAD_FAST                'command'
               16  BINARY_SUBSCR    
               18  RETURN_VALUE     
             20_0  COME_FROM             8  '8'

 L. 765        20  LOAD_GLOBAL              pkg_resources
               22  LOAD_METHOD              iter_entry_points
               24  LOAD_STR                 'distutils.commands'
               26  LOAD_FAST                'command'
               28  CALL_METHOD_2         2  ''
               30  STORE_FAST               'eps'

 L. 766        32  LOAD_FAST                'eps'
               34  GET_ITER         
               36  FOR_ITER             80  'to 80'
               38  STORE_FAST               'ep'

 L. 767        40  LOAD_FAST                'ep'
               42  LOAD_ATTR                require
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                fetch_build_egg
               48  LOAD_CONST               ('installer',)
               50  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               52  POP_TOP          

 L. 768        54  LOAD_FAST                'ep'
               56  LOAD_METHOD              load
               58  CALL_METHOD_0         0  ''
               60  DUP_TOP          
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                cmdclass
               66  LOAD_FAST                'command'
               68  STORE_SUBSCR     
               70  STORE_FAST               'cmdclass'

 L. 769        72  LOAD_FAST                'cmdclass'
               74  ROT_TWO          
               76  POP_TOP          
               78  RETURN_VALUE     

 L. 771        80  LOAD_GLOBAL              _Distribution
               82  LOAD_METHOD              get_command_class
               84  LOAD_FAST                'self'
               86  LOAD_FAST                'command'
               88  CALL_METHOD_2         2  ''
               90  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def print_commands--- This code section failed: ---

 L. 774         0  LOAD_GLOBAL              pkg_resources
                2  LOAD_METHOD              iter_entry_points
                4  LOAD_STR                 'distutils.commands'
                6  CALL_METHOD_1         1  ''
                8  GET_ITER         
             10_0  COME_FROM            24  '24'
               10  FOR_ITER             48  'to 48'
               12  STORE_FAST               'ep'

 L. 775        14  LOAD_FAST                'ep'
               16  LOAD_ATTR                name
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                cmdclass
               22  <118>                 1  ''
               24  POP_JUMP_IF_FALSE    10  'to 10'

 L. 777        26  LOAD_FAST                'ep'
               28  LOAD_METHOD              resolve
               30  CALL_METHOD_0         0  ''
               32  STORE_FAST               'cmdclass'

 L. 778        34  LOAD_FAST                'cmdclass'
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                cmdclass
               40  LOAD_FAST                'ep'
               42  LOAD_ATTR                name
               44  STORE_SUBSCR     
               46  JUMP_BACK            10  'to 10'

 L. 779        48  LOAD_GLOBAL              _Distribution
               50  LOAD_METHOD              print_commands
               52  LOAD_FAST                'self'
               54  CALL_METHOD_1         1  ''
               56  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<118>' instruction at offset 22

    def get_command_list--- This code section failed: ---

 L. 782         0  LOAD_GLOBAL              pkg_resources
                2  LOAD_METHOD              iter_entry_points
                4  LOAD_STR                 'distutils.commands'
                6  CALL_METHOD_1         1  ''
                8  GET_ITER         
             10_0  COME_FROM            24  '24'
               10  FOR_ITER             48  'to 48'
               12  STORE_FAST               'ep'

 L. 783        14  LOAD_FAST                'ep'
               16  LOAD_ATTR                name
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                cmdclass
               22  <118>                 1  ''
               24  POP_JUMP_IF_FALSE    10  'to 10'

 L. 785        26  LOAD_FAST                'ep'
               28  LOAD_METHOD              resolve
               30  CALL_METHOD_0         0  ''
               32  STORE_FAST               'cmdclass'

 L. 786        34  LOAD_FAST                'cmdclass'
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                cmdclass
               40  LOAD_FAST                'ep'
               42  LOAD_ATTR                name
               44  STORE_SUBSCR     
               46  JUMP_BACK            10  'to 10'

 L. 787        48  LOAD_GLOBAL              _Distribution
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
        for k, v in attrs.items:
            include = getattr(self, '_include_' + k, None)
            if include:
                include(v)
            else:
                self._include_misc(k, v)

    def exclude_package(self, package):
        """Remove packages, modules, and extensions in named package"""
        pfx = package + '.'
        if self.packages:
            self.packages = [p for p in self.packages if p != package if not p.startswithpfx]
        if self.py_modules:
            self.py_modules = [p for p in self.py_modules if p != package if not p.startswithpfx]
        if self.ext_modules:
            self.ext_modules = [p for p in self.ext_modules if p.name != package if not p.name.startswithpfx]

    def has_contents_for(self, package):
        """Return true if 'exclude_package(package)' would do something"""
        pfx = package + '.'
        for p in self.iter_distribution_names:
            if p == package or p.startswithpfx:
                return True

    def _exclude_misc--- This code section failed: ---

 L. 844         0  LOAD_GLOBAL              isinstance
                2  LOAD_DEREF               'value'
                4  LOAD_GLOBAL              sequence
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     26  'to 26'

 L. 845        10  LOAD_GLOBAL              DistutilsSetupError

 L. 846        12  LOAD_STR                 '%s: setting must be a list or tuple (%r)'
               14  LOAD_FAST                'name'
               16  LOAD_DEREF               'value'
               18  BUILD_TUPLE_2         2 
               20  BINARY_MODULO    

 L. 845        22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM             8  '8'

 L. 848        26  SETUP_FINALLY        42  'to 42'

 L. 849        28  LOAD_GLOBAL              getattr
               30  LOAD_FAST                'self'
               32  LOAD_FAST                'name'
               34  CALL_FUNCTION_2       2  ''
               36  STORE_FAST               'old'
               38  POP_BLOCK        
               40  JUMP_FORWARD         92  'to 92'
             42_0  COME_FROM_FINALLY    26  '26'

 L. 850        42  DUP_TOP          
               44  LOAD_GLOBAL              AttributeError
               46  <121>                90  ''
               48  POP_TOP          
               50  STORE_FAST               'e'
               52  POP_TOP          
               54  SETUP_FINALLY        82  'to 82'

 L. 851        56  LOAD_GLOBAL              DistutilsSetupError

 L. 852        58  LOAD_STR                 '%s: No such distribution setting'
               60  LOAD_FAST                'name'
               62  BINARY_MODULO    

 L. 851        64  CALL_FUNCTION_1       1  ''

 L. 853        66  LOAD_FAST                'e'

 L. 851        68  RAISE_VARARGS_2       2  'exception instance with __cause__'
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

 L. 854        92  LOAD_FAST                'old'
               94  LOAD_CONST               None
               96  <117>                 1  ''
               98  POP_JUMP_IF_FALSE   124  'to 124'
              100  LOAD_GLOBAL              isinstance
              102  LOAD_FAST                'old'
              104  LOAD_GLOBAL              sequence
              106  CALL_FUNCTION_2       2  ''
              108  POP_JUMP_IF_TRUE    124  'to 124'

 L. 855       110  LOAD_GLOBAL              DistutilsSetupError

 L. 856       112  LOAD_FAST                'name'
              114  LOAD_STR                 ': this setting cannot be changed via include/exclude'
              116  BINARY_ADD       

 L. 855       118  CALL_FUNCTION_1       1  ''
              120  RAISE_VARARGS_1       1  'exception instance'
              122  JUMP_FORWARD        154  'to 154'
            124_0  COME_FROM           108  '108'
            124_1  COME_FROM            98  '98'

 L. 858       124  LOAD_FAST                'old'
              126  POP_JUMP_IF_FALSE   154  'to 154'

 L. 859       128  LOAD_GLOBAL              setattr
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

 L. 864         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'value'
                4  LOAD_GLOBAL              sequence
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_TRUE     26  'to 26'

 L. 865        10  LOAD_GLOBAL              DistutilsSetupError

 L. 866        12  LOAD_STR                 '%s: setting must be a list (%r)'
               14  LOAD_FAST                'name'
               16  LOAD_FAST                'value'
               18  BUILD_TUPLE_2         2 
               20  BINARY_MODULO    

 L. 865        22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM             8  '8'

 L. 868        26  SETUP_FINALLY        42  'to 42'

 L. 869        28  LOAD_GLOBAL              getattr
               30  LOAD_FAST                'self'
               32  LOAD_FAST                'name'
               34  CALL_FUNCTION_2       2  ''
               36  STORE_DEREF              'old'
               38  POP_BLOCK        
               40  JUMP_FORWARD         92  'to 92'
             42_0  COME_FROM_FINALLY    26  '26'

 L. 870        42  DUP_TOP          
               44  LOAD_GLOBAL              AttributeError
               46  <121>                90  ''
               48  POP_TOP          
               50  STORE_FAST               'e'
               52  POP_TOP          
               54  SETUP_FINALLY        82  'to 82'

 L. 871        56  LOAD_GLOBAL              DistutilsSetupError

 L. 872        58  LOAD_STR                 '%s: No such distribution setting'
               60  LOAD_FAST                'name'
               62  BINARY_MODULO    

 L. 871        64  CALL_FUNCTION_1       1  ''

 L. 873        66  LOAD_FAST                'e'

 L. 871        68  RAISE_VARARGS_2       2  'exception instance with __cause__'
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

 L. 874        92  LOAD_DEREF               'old'
               94  LOAD_CONST               None
               96  <117>                 0  ''
               98  POP_JUMP_IF_FALSE   114  'to 114'

 L. 875       100  LOAD_GLOBAL              setattr
              102  LOAD_FAST                'self'
              104  LOAD_FAST                'name'
              106  LOAD_FAST                'value'
              108  CALL_FUNCTION_3       3  ''
              110  POP_TOP          
              112  JUMP_FORWARD        172  'to 172'
            114_0  COME_FROM            98  '98'

 L. 876       114  LOAD_GLOBAL              isinstance
              116  LOAD_DEREF               'old'
              118  LOAD_GLOBAL              sequence
              120  CALL_FUNCTION_2       2  ''
              122  POP_JUMP_IF_TRUE    138  'to 138'

 L. 877       124  LOAD_GLOBAL              DistutilsSetupError

 L. 878       126  LOAD_FAST                'name'
              128  LOAD_STR                 ': this setting cannot be changed via include/exclude'
              130  BINARY_ADD       

 L. 877       132  CALL_FUNCTION_1       1  ''
              134  RAISE_VARARGS_1       1  'exception instance'
              136  JUMP_FORWARD        172  'to 172'
            138_0  COME_FROM           122  '122'

 L. 881       138  LOAD_CLOSURE             'old'
              140  BUILD_TUPLE_1         1 
              142  LOAD_LISTCOMP            '<code_object <listcomp>>'
              144  LOAD_STR                 'Distribution._include_misc.<locals>.<listcomp>'
              146  MAKE_FUNCTION_8          'closure'
              148  LOAD_FAST                'value'
              150  GET_ITER         
              152  CALL_FUNCTION_1       1  ''
              154  STORE_FAST               'new'

 L. 882       156  LOAD_GLOBAL              setattr
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
        for k, v in attrs.items:
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

 L. 916         0  LOAD_FAST                'self'
                2  LOAD_ATTR                __class__
                4  LOAD_ATTR                global_options
                6  LOAD_FAST                'self'
                8  STORE_ATTR               global_options

 L. 917        10  LOAD_FAST                'self'
               12  LOAD_ATTR                __class__
               14  LOAD_ATTR                negative_opt
               16  LOAD_FAST                'self'
               18  STORE_ATTR               negative_opt

 L. 920        20  LOAD_FAST                'args'
               22  LOAD_CONST               0
               24  BINARY_SUBSCR    
               26  STORE_FAST               'command'

 L. 921        28  LOAD_FAST                'self'
               30  LOAD_METHOD              get_option_dict
               32  LOAD_STR                 'aliases'
               34  CALL_METHOD_1         1  ''
               36  STORE_FAST               'aliases'

 L. 922        38  LOAD_FAST                'command'
               40  LOAD_FAST                'aliases'
               42  <118>                 0  ''
               44  POP_JUMP_IF_FALSE   102  'to 102'

 L. 923        46  LOAD_FAST                'aliases'
               48  LOAD_FAST                'command'
               50  BINARY_SUBSCR    
               52  UNPACK_SEQUENCE_2     2 
               54  STORE_FAST               'src'
               56  STORE_FAST               'alias'

 L. 924        58  LOAD_FAST                'aliases'
               60  LOAD_FAST                'command'
               62  DELETE_SUBSCR    

 L. 925        64  LOAD_CONST               0
               66  LOAD_CONST               None
               68  IMPORT_NAME              shlex
               70  STORE_FAST               'shlex'

 L. 926        72  LOAD_FAST                'shlex'
               74  LOAD_METHOD              split
               76  LOAD_FAST                'alias'
               78  LOAD_CONST               True
               80  CALL_METHOD_2         2  ''
               82  LOAD_FAST                'args'
               84  LOAD_CONST               None
               86  LOAD_CONST               1
               88  BUILD_SLICE_2         2 
               90  STORE_SUBSCR     

 L. 927        92  LOAD_FAST                'args'
               94  LOAD_CONST               0
               96  BINARY_SUBSCR    
               98  STORE_FAST               'command'
              100  JUMP_BACK            38  'to 38'
            102_0  COME_FROM            44  '44'

 L. 929       102  LOAD_GLOBAL              _Distribution
              104  LOAD_METHOD              _parse_command_opts
              106  LOAD_FAST                'self'
              108  LOAD_FAST                'parser'
              110  LOAD_FAST                'args'
              112  CALL_METHOD_3         3  ''
              114  STORE_FAST               'nargs'

 L. 932       116  LOAD_FAST                'self'
              118  LOAD_METHOD              get_command_class
              120  LOAD_FAST                'command'
              122  CALL_METHOD_1         1  ''
              124  STORE_FAST               'cmd_class'

 L. 933       126  LOAD_GLOBAL              getattr
              128  LOAD_FAST                'cmd_class'
              130  LOAD_STR                 'command_consumes_arguments'
              132  LOAD_CONST               None
              134  CALL_FUNCTION_3       3  ''
              136  POP_JUMP_IF_FALSE   168  'to 168'

 L. 934       138  LOAD_STR                 'command line'
              140  LOAD_FAST                'nargs'
              142  BUILD_TUPLE_2         2 
              144  LOAD_FAST                'self'
              146  LOAD_METHOD              get_option_dict
              148  LOAD_FAST                'command'
              150  CALL_METHOD_1         1  ''
              152  LOAD_STR                 'args'
              154  STORE_SUBSCR     

 L. 935       156  LOAD_FAST                'nargs'
              158  LOAD_CONST               None
              160  <117>                 1  ''
              162  POP_JUMP_IF_FALSE   168  'to 168'

 L. 936       164  BUILD_LIST_0          0 
              166  RETURN_VALUE     
            168_0  COME_FROM           162  '162'
            168_1  COME_FROM           136  '136'

 L. 938       168  LOAD_FAST                'nargs'
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
        for cmd, opts in self.command_options.items:
            for opt, (src, val) in opts.items:
                if src != 'command line':
                    pass
                else:
                    opt = opt.replace('_', '-')
                    if val == 0:
                        cmdobj = self.get_command_objcmd
                        neg_opt = self.negative_opt.copy
                        neg_opt.updategetattr(cmdobj, 'negative_opt', {})
                        for neg, pos in neg_opt.items:
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
                    if name.endswith'module':
                        name = name[:-6]
                    (yield name)

    def handle_display_options--- This code section failed: ---

 L.1004         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              sys
                6  STORE_FAST               'sys'

 L.1006         8  LOAD_GLOBAL              six
               10  LOAD_ATTR                PY2
               12  POP_JUMP_IF_TRUE     20  'to 20'
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                help_commands
               18  POP_JUMP_IF_FALSE    32  'to 32'
             20_0  COME_FROM            12  '12'

 L.1007        20  LOAD_GLOBAL              _Distribution
               22  LOAD_METHOD              handle_display_options
               24  LOAD_FAST                'self'
               26  LOAD_FAST                'option_order'
               28  CALL_METHOD_2         2  ''
               30  RETURN_VALUE     
             32_0  COME_FROM            18  '18'

 L.1010        32  LOAD_GLOBAL              isinstance
               34  LOAD_FAST                'sys'
               36  LOAD_ATTR                stdout
               38  LOAD_GLOBAL              io
               40  LOAD_ATTR                TextIOWrapper
               42  CALL_FUNCTION_2       2  ''
               44  POP_JUMP_IF_TRUE     58  'to 58'

 L.1011        46  LOAD_GLOBAL              _Distribution
               48  LOAD_METHOD              handle_display_options
               50  LOAD_FAST                'self'
               52  LOAD_FAST                'option_order'
               54  CALL_METHOD_2         2  ''
               56  RETURN_VALUE     
             58_0  COME_FROM            44  '44'

 L.1015        58  LOAD_FAST                'sys'
               60  LOAD_ATTR                stdout
               62  LOAD_ATTR                encoding
               64  LOAD_METHOD              lower
               66  CALL_METHOD_0         0  ''
               68  LOAD_CONST               ('utf-8', 'utf8')
               70  <118>                 0  ''
               72  POP_JUMP_IF_FALSE    86  'to 86'

 L.1016        74  LOAD_GLOBAL              _Distribution
               76  LOAD_METHOD              handle_display_options
               78  LOAD_FAST                'self'
               80  LOAD_FAST                'option_order'
               82  CALL_METHOD_2         2  ''
               84  RETURN_VALUE     
             86_0  COME_FROM            72  '72'

 L.1019        86  LOAD_FAST                'sys'
               88  LOAD_ATTR                stdout
               90  LOAD_ATTR                encoding
               92  STORE_FAST               'encoding'

 L.1020        94  LOAD_FAST                'sys'
               96  LOAD_ATTR                stdout
               98  LOAD_ATTR                errors
              100  STORE_FAST               'errors'

 L.1021       102  LOAD_FAST                'sys'
              104  LOAD_ATTR                platform
              106  LOAD_STR                 'win32'
              108  COMPARE_OP               !=
              110  POP_JUMP_IF_FALSE   116  'to 116'
              112  LOAD_STR                 '\n'
              114  JUMP_IF_TRUE_OR_POP   118  'to 118'
            116_0  COME_FROM           110  '110'
              116  LOAD_CONST               None
            118_0  COME_FROM           114  '114'
              118  STORE_FAST               'newline'

 L.1022       120  LOAD_FAST                'sys'
              122  LOAD_ATTR                stdout
              124  LOAD_ATTR                line_buffering
              126  STORE_FAST               'line_buffering'

 L.1024       128  LOAD_GLOBAL              io
              130  LOAD_METHOD              TextIOWrapper

 L.1025       132  LOAD_FAST                'sys'
              134  LOAD_ATTR                stdout
              136  LOAD_METHOD              detach
              138  CALL_METHOD_0         0  ''
              140  LOAD_STR                 'utf-8'
              142  LOAD_FAST                'errors'
              144  LOAD_FAST                'newline'
              146  LOAD_FAST                'line_buffering'

 L.1024       148  CALL_METHOD_5         5  ''
              150  LOAD_FAST                'sys'
              152  STORE_ATTR               stdout

 L.1026       154  SETUP_FINALLY       196  'to 196'

 L.1027       156  LOAD_GLOBAL              _Distribution
              158  LOAD_METHOD              handle_display_options
              160  LOAD_FAST                'self'
              162  LOAD_FAST                'option_order'
              164  CALL_METHOD_2         2  ''
              166  POP_BLOCK        

 L.1029       168  LOAD_GLOBAL              io
              170  LOAD_METHOD              TextIOWrapper

 L.1030       172  LOAD_FAST                'sys'
              174  LOAD_ATTR                stdout
              176  LOAD_METHOD              detach
              178  CALL_METHOD_0         0  ''
              180  LOAD_FAST                'encoding'
              182  LOAD_FAST                'errors'
              184  LOAD_FAST                'newline'
              186  LOAD_FAST                'line_buffering'

 L.1029       188  CALL_METHOD_5         5  ''
              190  LOAD_FAST                'sys'
              192  STORE_ATTR               stdout

 L.1027       194  RETURN_VALUE     
            196_0  COME_FROM_FINALLY   154  '154'

 L.1029       196  LOAD_GLOBAL              io
              198  LOAD_METHOD              TextIOWrapper

 L.1030       200  LOAD_FAST                'sys'
              202  LOAD_ATTR                stdout
              204  LOAD_METHOD              detach
              206  CALL_METHOD_0         0  ''
              208  LOAD_FAST                'encoding'
              210  LOAD_FAST                'errors'
              212  LOAD_FAST                'newline'
              214  LOAD_FAST                'line_buffering'

 L.1029       216  CALL_METHOD_5         5  ''
              218  LOAD_FAST                'sys'
              220  STORE_ATTR               stdout
              222  <48>             

Parse error at or near `<118>' instruction at offset 70


class DistDeprecationWarning(SetuptoolsDeprecationWarning):
    __doc__ = 'Class for warning about deprecations in dist in\n    setuptools. Not ignored by default, unlike DeprecationWarning.'