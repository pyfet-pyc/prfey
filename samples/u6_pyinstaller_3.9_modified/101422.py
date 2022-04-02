# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: netrc.py
"""An object-oriented interface to .netrc files."""
import os, shlex, stat
__all__ = [
 'netrc', 'NetrcParseError']

class NetrcParseError(Exception):
    __doc__ = 'Exception raised on syntax errors in the .netrc file.'

    def __init__(self, msg, filename=None, lineno=None):
        self.filename = filename
        self.lineno = lineno
        self.msg = msg
        Exception.__init__(self, msg)

    def __str__(self):
        return '%s (%s, line %s)' % (self.msg, self.filename, self.lineno)


class netrc:

    def __init__--- This code section failed: ---

 L.  24         0  LOAD_FAST                'file'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  STORE_FAST               'default_netrc'

 L.  25         8  LOAD_FAST                'file'
               10  LOAD_CONST               None
               12  <117>                 0  ''
               14  POP_JUMP_IF_FALSE    38  'to 38'

 L.  26        16  LOAD_GLOBAL              os
               18  LOAD_ATTR                path
               20  LOAD_METHOD              join
               22  LOAD_GLOBAL              os
               24  LOAD_ATTR                path
               26  LOAD_METHOD              expanduser
               28  LOAD_STR                 '~'
               30  CALL_METHOD_1         1  ''
               32  LOAD_STR                 '.netrc'
               34  CALL_METHOD_2         2  ''
               36  STORE_FAST               'file'
             38_0  COME_FROM            14  '14'

 L.  27        38  BUILD_MAP_0           0 
               40  LOAD_FAST                'self'
               42  STORE_ATTR               hosts

 L.  28        44  BUILD_MAP_0           0 
               46  LOAD_FAST                'self'
               48  STORE_ATTR               macros

 L.  29        50  LOAD_GLOBAL              open
               52  LOAD_FAST                'file'
               54  CALL_FUNCTION_1       1  ''
               56  SETUP_WITH           88  'to 88'
               58  STORE_FAST               'fp'

 L.  30        60  LOAD_FAST                'self'
               62  LOAD_METHOD              _parse
               64  LOAD_FAST                'file'
               66  LOAD_FAST                'fp'
               68  LOAD_FAST                'default_netrc'
               70  CALL_METHOD_3         3  ''
               72  POP_TOP          
               74  POP_BLOCK        
               76  LOAD_CONST               None
               78  DUP_TOP          
               80  DUP_TOP          
               82  CALL_FUNCTION_3       3  ''
               84  POP_TOP          
               86  JUMP_FORWARD        104  'to 104'
             88_0  COME_FROM_WITH       56  '56'
               88  <49>             
               90  POP_JUMP_IF_TRUE     94  'to 94'
               92  <48>             
             94_0  COME_FROM            90  '90'
               94  POP_TOP          
               96  POP_TOP          
               98  POP_TOP          
              100  POP_EXCEPT       
              102  POP_TOP          
            104_0  COME_FROM            86  '86'

Parse error at or near `None' instruction at offset -1

    def _parse--- This code section failed: ---

 L.  33         0  LOAD_GLOBAL              shlex
                2  LOAD_METHOD              shlex
                4  LOAD_FAST                'fp'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'lexer'

 L.  34        10  LOAD_FAST                'lexer'
               12  DUP_TOP          
               14  LOAD_ATTR                wordchars
               16  LOAD_STR                 '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
               18  INPLACE_ADD      
               20  ROT_TWO          
               22  STORE_ATTR               wordchars

 L.  35        24  LOAD_FAST                'lexer'
               26  LOAD_ATTR                commenters
               28  LOAD_METHOD              replace
               30  LOAD_STR                 '#'
               32  LOAD_STR                 ''
               34  CALL_METHOD_2         2  ''
               36  LOAD_FAST                'lexer'
               38  STORE_ATTR               commenters
             40_0  COME_FROM           100  '100'
             40_1  COME_FROM            88  '88'

 L.  38        40  LOAD_FAST                'lexer'
               42  LOAD_ATTR                lineno
               44  STORE_FAST               'saved_lineno'

 L.  39        46  LOAD_FAST                'lexer'
               48  LOAD_METHOD              get_token
               50  CALL_METHOD_0         0  ''
               52  DUP_TOP          
               54  STORE_FAST               'toplevel'
               56  STORE_FAST               'tt'

 L.  40        58  LOAD_FAST                'tt'
               60  POP_JUMP_IF_TRUE     68  'to 68'

 L.  41     62_64  BREAK_LOOP          688  'to 688'
               66  JUMP_FORWARD        250  'to 250'
             68_0  COME_FROM            60  '60'

 L.  42        68  LOAD_FAST                'tt'
               70  LOAD_CONST               0
               72  BINARY_SUBSCR    
               74  LOAD_STR                 '#'
               76  COMPARE_OP               ==
               78  POP_JUMP_IF_FALSE   116  'to 116'

 L.  43        80  LOAD_FAST                'lexer'
               82  LOAD_ATTR                lineno
               84  LOAD_FAST                'saved_lineno'
               86  COMPARE_OP               ==
               88  POP_JUMP_IF_FALSE    40  'to 40'
               90  LOAD_GLOBAL              len
               92  LOAD_FAST                'tt'
               94  CALL_FUNCTION_1       1  ''
               96  LOAD_CONST               1
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_FALSE    40  'to 40'

 L.  44       102  LOAD_FAST                'lexer'
              104  LOAD_ATTR                instream
              106  LOAD_METHOD              readline
              108  CALL_METHOD_0         0  ''
              110  POP_TOP          

 L.  45       112  JUMP_BACK            40  'to 40'
              114  JUMP_FORWARD        250  'to 250'
            116_0  COME_FROM            78  '78'

 L.  46       116  LOAD_FAST                'tt'
              118  LOAD_STR                 'machine'
              120  COMPARE_OP               ==
              122  POP_JUMP_IF_FALSE   134  'to 134'

 L.  47       124  LOAD_FAST                'lexer'
              126  LOAD_METHOD              get_token
              128  CALL_METHOD_0         0  ''
              130  STORE_FAST               'entryname'
              132  JUMP_FORWARD        250  'to 250'
            134_0  COME_FROM           122  '122'

 L.  48       134  LOAD_FAST                'tt'
              136  LOAD_STR                 'default'
              138  COMPARE_OP               ==
              140  POP_JUMP_IF_FALSE   148  'to 148'

 L.  49       142  LOAD_STR                 'default'
              144  STORE_FAST               'entryname'
              146  JUMP_FORWARD        250  'to 250'
            148_0  COME_FROM           140  '140'

 L.  50       148  LOAD_FAST                'tt'
              150  LOAD_STR                 'macdef'
              152  COMPARE_OP               ==
              154  POP_JUMP_IF_FALSE   232  'to 232'

 L.  51       156  LOAD_FAST                'lexer'
              158  LOAD_METHOD              get_token
              160  CALL_METHOD_0         0  ''
              162  STORE_FAST               'entryname'

 L.  52       164  BUILD_LIST_0          0 
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                macros
              170  LOAD_FAST                'entryname'
              172  STORE_SUBSCR     

 L.  53       174  LOAD_STR                 ' \t'
              176  LOAD_FAST                'lexer'
              178  STORE_ATTR               whitespace

 L.  55       180  LOAD_FAST                'lexer'
              182  LOAD_ATTR                instream
              184  LOAD_METHOD              readline
              186  CALL_METHOD_0         0  ''
              188  STORE_FAST               'line'

 L.  56       190  LOAD_FAST                'line'
              192  POP_JUMP_IF_FALSE   202  'to 202'
              194  LOAD_FAST                'line'
              196  LOAD_STR                 '\n'
              198  COMPARE_OP               ==
              200  POP_JUMP_IF_FALSE   210  'to 210'
            202_0  COME_FROM           192  '192'

 L.  57       202  LOAD_STR                 ' \t\r\n'
              204  LOAD_FAST                'lexer'
              206  STORE_ATTR               whitespace

 L.  58       208  JUMP_BACK            40  'to 40'
            210_0  COME_FROM           200  '200'

 L.  59       210  LOAD_FAST                'self'
              212  LOAD_ATTR                macros
              214  LOAD_FAST                'entryname'
              216  BINARY_SUBSCR    
              218  LOAD_METHOD              append
              220  LOAD_FAST                'line'
              222  CALL_METHOD_1         1  ''
              224  POP_TOP          
              226  JUMP_BACK           180  'to 180'

 L.  60       228  JUMP_BACK            40  'to 40'
              230  JUMP_FORWARD        250  'to 250'
            232_0  COME_FROM           154  '154'

 L.  62       232  LOAD_GLOBAL              NetrcParseError

 L.  63       234  LOAD_STR                 'bad toplevel token %r'
              236  LOAD_FAST                'tt'
              238  BINARY_MODULO    
              240  LOAD_FAST                'file'
              242  LOAD_FAST                'lexer'
              244  LOAD_ATTR                lineno

 L.  62       246  CALL_FUNCTION_3       3  ''
              248  RAISE_VARARGS_1       1  'exception instance'
            250_0  COME_FROM           230  '230'
            250_1  COME_FROM           146  '146'
            250_2  COME_FROM           132  '132'
            250_3  COME_FROM           114  '114'
            250_4  COME_FROM            66  '66'

 L.  66       250  LOAD_STR                 ''
              252  STORE_FAST               'login'

 L.  67       254  LOAD_CONST               None
              256  DUP_TOP          
              258  STORE_FAST               'account'
              260  STORE_FAST               'password'

 L.  68       262  BUILD_MAP_0           0 
              264  LOAD_FAST                'self'
              266  LOAD_ATTR                hosts
              268  LOAD_FAST                'entryname'
              270  STORE_SUBSCR     

 L.  70       272  LOAD_FAST                'lexer'
              274  LOAD_METHOD              get_token
              276  CALL_METHOD_0         0  ''
              278  STORE_FAST               'tt'

 L.  71       280  LOAD_FAST                'tt'
              282  LOAD_METHOD              startswith
              284  LOAD_STR                 '#'
              286  CALL_METHOD_1         1  ''
          288_290  POP_JUMP_IF_TRUE    302  'to 302'

 L.  72       292  LOAD_FAST                'tt'
              294  LOAD_CONST               frozenset({'', 'default', 'machine', 'macdef'})
              296  <118>                 0  ''

 L.  71   298_300  POP_JUMP_IF_FALSE   370  'to 370'
            302_0  COME_FROM           288  '288'

 L.  73       302  LOAD_FAST                'password'
          304_306  POP_JUMP_IF_FALSE   338  'to 338'

 L.  74       308  LOAD_FAST                'login'
              310  LOAD_FAST                'account'
              312  LOAD_FAST                'password'
              314  BUILD_TUPLE_3         3 
              316  LOAD_FAST                'self'
              318  LOAD_ATTR                hosts
              320  LOAD_FAST                'entryname'
              322  STORE_SUBSCR     

 L.  75       324  LOAD_FAST                'lexer'
              326  LOAD_METHOD              push_token
              328  LOAD_FAST                'tt'
              330  CALL_METHOD_1         1  ''
              332  POP_TOP          

 L.  76       334  CONTINUE             40  'to 40'
              336  JUMP_BACK           272  'to 272'
            338_0  COME_FROM           304  '304'

 L.  78       338  LOAD_GLOBAL              NetrcParseError

 L.  79       340  LOAD_STR                 'malformed %s entry %s terminated by %s'

 L.  80       342  LOAD_FAST                'toplevel'
              344  LOAD_FAST                'entryname'
              346  LOAD_GLOBAL              repr
              348  LOAD_FAST                'tt'
              350  CALL_FUNCTION_1       1  ''
              352  BUILD_TUPLE_3         3 

 L.  79       354  BINARY_MODULO    

 L.  81       356  LOAD_FAST                'file'
              358  LOAD_FAST                'lexer'
              360  LOAD_ATTR                lineno

 L.  78       362  CALL_FUNCTION_3       3  ''
              364  RAISE_VARARGS_1       1  'exception instance'
          366_368  JUMP_BACK           272  'to 272'
            370_0  COME_FROM           298  '298'

 L.  82       370  LOAD_FAST                'tt'
              372  LOAD_STR                 'login'
              374  COMPARE_OP               ==
          376_378  POP_JUMP_IF_TRUE    390  'to 390'
              380  LOAD_FAST                'tt'
              382  LOAD_STR                 'user'
              384  COMPARE_OP               ==
          386_388  POP_JUMP_IF_FALSE   402  'to 402'
            390_0  COME_FROM           376  '376'

 L.  83       390  LOAD_FAST                'lexer'
              392  LOAD_METHOD              get_token
              394  CALL_METHOD_0         0  ''
              396  STORE_FAST               'login'
          398_400  JUMP_BACK           272  'to 272'
            402_0  COME_FROM           386  '386'

 L.  84       402  LOAD_FAST                'tt'
              404  LOAD_STR                 'account'
              406  COMPARE_OP               ==
          408_410  POP_JUMP_IF_FALSE   424  'to 424'

 L.  85       412  LOAD_FAST                'lexer'
              414  LOAD_METHOD              get_token
              416  CALL_METHOD_0         0  ''
              418  STORE_FAST               'account'
          420_422  JUMP_BACK           272  'to 272'
            424_0  COME_FROM           408  '408'

 L.  86       424  LOAD_FAST                'tt'
              426  LOAD_STR                 'password'
              428  COMPARE_OP               ==
          430_432  POP_JUMP_IF_FALSE   664  'to 664'

 L.  87       434  LOAD_GLOBAL              os
              436  LOAD_ATTR                name
              438  LOAD_STR                 'posix'
              440  COMPARE_OP               ==
          442_444  POP_JUMP_IF_FALSE   654  'to 654'
              446  LOAD_FAST                'default_netrc'
          448_450  POP_JUMP_IF_FALSE   654  'to 654'

 L.  88       452  LOAD_GLOBAL              os
              454  LOAD_METHOD              fstat
              456  LOAD_FAST                'fp'
              458  LOAD_METHOD              fileno
              460  CALL_METHOD_0         0  ''
              462  CALL_METHOD_1         1  ''
              464  STORE_FAST               'prop'

 L.  89       466  LOAD_FAST                'prop'
              468  LOAD_ATTR                st_uid
              470  LOAD_GLOBAL              os
              472  LOAD_METHOD              getuid
              474  CALL_METHOD_0         0  ''
              476  COMPARE_OP               !=
          478_480  POP_JUMP_IF_FALSE   620  'to 620'

 L.  90       482  LOAD_CONST               0
              484  LOAD_CONST               None
              486  IMPORT_NAME              pwd
              488  STORE_FAST               'pwd'

 L.  91       490  SETUP_FINALLY       512  'to 512'

 L.  92       492  LOAD_FAST                'pwd'
              494  LOAD_METHOD              getpwuid
              496  LOAD_FAST                'prop'
              498  LOAD_ATTR                st_uid
              500  CALL_METHOD_1         1  ''
              502  LOAD_CONST               0
              504  BINARY_SUBSCR    
              506  STORE_FAST               'fowner'
              508  POP_BLOCK        
              510  JUMP_FORWARD        542  'to 542'
            512_0  COME_FROM_FINALLY   490  '490'

 L.  93       512  DUP_TOP          
              514  LOAD_GLOBAL              KeyError
          516_518  <121>               540  ''
              520  POP_TOP          
              522  POP_TOP          
              524  POP_TOP          

 L.  94       526  LOAD_STR                 'uid %s'
              528  LOAD_FAST                'prop'
              530  LOAD_ATTR                st_uid
              532  BINARY_MODULO    
              534  STORE_FAST               'fowner'
              536  POP_EXCEPT       
              538  JUMP_FORWARD        542  'to 542'
              540  <48>             
            542_0  COME_FROM           538  '538'
            542_1  COME_FROM           510  '510'

 L.  95       542  SETUP_FINALLY       566  'to 566'

 L.  96       544  LOAD_FAST                'pwd'
              546  LOAD_METHOD              getpwuid
              548  LOAD_GLOBAL              os
              550  LOAD_METHOD              getuid
              552  CALL_METHOD_0         0  ''
              554  CALL_METHOD_1         1  ''
              556  LOAD_CONST               0
              558  BINARY_SUBSCR    
              560  STORE_FAST               'user'
              562  POP_BLOCK        
              564  JUMP_FORWARD        598  'to 598'
            566_0  COME_FROM_FINALLY   542  '542'

 L.  97       566  DUP_TOP          
              568  LOAD_GLOBAL              KeyError
          570_572  <121>               596  ''
              574  POP_TOP          
              576  POP_TOP          
              578  POP_TOP          

 L.  98       580  LOAD_STR                 'uid %s'
              582  LOAD_GLOBAL              os
              584  LOAD_METHOD              getuid
              586  CALL_METHOD_0         0  ''
              588  BINARY_MODULO    
              590  STORE_FAST               'user'
              592  POP_EXCEPT       
              594  JUMP_FORWARD        598  'to 598'
              596  <48>             
            598_0  COME_FROM           594  '594'
            598_1  COME_FROM           564  '564'

 L.  99       598  LOAD_GLOBAL              NetrcParseError

 L. 100       600  LOAD_STR                 '~/.netrc file owner (%s) does not match current user (%s)'

 L. 101       602  LOAD_FAST                'fowner'
              604  LOAD_FAST                'user'
              606  BUILD_TUPLE_2         2 

 L. 100       608  BINARY_MODULO    

 L. 102       610  LOAD_FAST                'file'
              612  LOAD_FAST                'lexer'
              614  LOAD_ATTR                lineno

 L.  99       616  CALL_FUNCTION_3       3  ''
              618  RAISE_VARARGS_1       1  'exception instance'
            620_0  COME_FROM           478  '478'

 L. 103       620  LOAD_FAST                'prop'
              622  LOAD_ATTR                st_mode
              624  LOAD_GLOBAL              stat
              626  LOAD_ATTR                S_IRWXG
              628  LOAD_GLOBAL              stat
              630  LOAD_ATTR                S_IRWXO
              632  BINARY_OR        
              634  BINARY_AND       
          636_638  POP_JUMP_IF_FALSE   654  'to 654'

 L. 104       640  LOAD_GLOBAL              NetrcParseError

 L. 105       642  LOAD_STR                 '~/.netrc access too permissive: access permissions must restrict access to only the owner'

 L. 107       644  LOAD_FAST                'file'
              646  LOAD_FAST                'lexer'
              648  LOAD_ATTR                lineno

 L. 104       650  CALL_FUNCTION_3       3  ''
              652  RAISE_VARARGS_1       1  'exception instance'
            654_0  COME_FROM           636  '636'
            654_1  COME_FROM           448  '448'
            654_2  COME_FROM           442  '442'

 L. 108       654  LOAD_FAST                'lexer'
              656  LOAD_METHOD              get_token
              658  CALL_METHOD_0         0  ''
              660  STORE_FAST               'password'
              662  JUMP_BACK           272  'to 272'
            664_0  COME_FROM           430  '430'

 L. 110       664  LOAD_GLOBAL              NetrcParseError
              666  LOAD_STR                 'bad follower token %r'
              668  LOAD_FAST                'tt'
              670  BINARY_MODULO    

 L. 111       672  LOAD_FAST                'file'
              674  LOAD_FAST                'lexer'
              676  LOAD_ATTR                lineno

 L. 110       678  CALL_FUNCTION_3       3  ''
              680  RAISE_VARARGS_1       1  'exception instance'
          682_684  JUMP_BACK           272  'to 272'
              686  JUMP_BACK            40  'to 40'

Parse error at or near `JUMP_FORWARD' instruction at offset 230

    def authenticators--- This code section failed: ---

 L. 115         0  LOAD_FAST                'host'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                hosts
                6  <118>                 0  ''
                8  POP_JUMP_IF_FALSE    20  'to 20'

 L. 116        10  LOAD_FAST                'self'
               12  LOAD_ATTR                hosts
               14  LOAD_FAST                'host'
               16  BINARY_SUBSCR    
               18  RETURN_VALUE     
             20_0  COME_FROM             8  '8'

 L. 117        20  LOAD_STR                 'default'
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                hosts
               26  <118>                 0  ''
               28  POP_JUMP_IF_FALSE    40  'to 40'

 L. 118        30  LOAD_FAST                'self'
               32  LOAD_ATTR                hosts
               34  LOAD_STR                 'default'
               36  BINARY_SUBSCR    
               38  RETURN_VALUE     
             40_0  COME_FROM            28  '28'

 L. 120        40  LOAD_CONST               None
               42  RETURN_VALUE     

Parse error at or near `None' instruction at offset -1

    def __repr__(self):
        """Dump the class data in the format of a .netrc file."""
        rep = ''
        for host in self.hosts.keys:
            attrs = self.hosts[host]
            rep += f"machine {host}\n\tlogin {attrs[0]}\n"
            if attrs[1]:
                rep += f"\taccount {attrs[1]}\n"
            rep += f"\tpassword {attrs[2]}\n"
        else:
            for macro in self.macros.keys:
                rep += f"macdef {macro}\n"
                for line in self.macros[macro]:
                    rep += line
                else:
                    rep += '\n'

            else:
                return rep


if __name__ == '__main__':
    print(netrc())