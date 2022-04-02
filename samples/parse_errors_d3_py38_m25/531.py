# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
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

    def __init__(self, file=None):
        default_netrc = file is None
        if file is None:
            file = os.path.join(os.path.expanduser('~'), '.netrc')
        self.hosts = {}
        self.macros = {}
        with open(file) as fp:
            self._parse(file, fp, default_netrc)

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
             40_0  COME_FROM           690  '690'
             40_1  COME_FROM           334  '334'
             40_2  COME_FROM           228  '228'
             40_3  COME_FROM           208  '208'
             40_4  COME_FROM           112  '112'
             40_5  COME_FROM           100  '100'
             40_6  COME_FROM            88  '88'

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

 L.  41     62_64  JUMP_FORWARD        692  'to 692'
               66  BREAK_LOOP          250  'to 250'
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
               88  POP_JUMP_IF_FALSE_BACK    40  'to 40'
               90  LOAD_GLOBAL              len
               92  LOAD_FAST                'tt'
               94  CALL_FUNCTION_1       1  ''
               96  LOAD_CONST               1
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_FALSE_BACK    40  'to 40'

 L.  44       102  LOAD_FAST                'lexer'
              104  LOAD_ATTR                instream
              106  LOAD_METHOD              readline
              108  CALL_METHOD_0         0  ''
              110  POP_TOP          

 L.  45       112  JUMP_BACK            40  'to 40'
              114  BREAK_LOOP          250  'to 250'
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
            180_0  COME_FROM           226  '226'

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
              230  BREAK_LOOP          250  'to 250'
            232_0  COME_FROM           154  '154'

 L.  62       232  LOAD_GLOBAL              NetrcParseError

 L.  63       234  LOAD_STR                 'bad toplevel token %r'
              236  LOAD_FAST                'tt'
              238  BINARY_MODULO    

 L.  63       240  LOAD_FAST                'file'

 L.  63       242  LOAD_FAST                'lexer'
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
            272_0  COME_FROM           686  '686'
            272_1  COME_FROM           666  '666'
            272_2  COME_FROM           420  '420'
            272_3  COME_FROM           398  '398'
            272_4  COME_FROM           366  '366'
            272_5  COME_FROM           336  '336'

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
              296  COMPARE_OP               in

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

 L.  76       334  BREAK_LOOP           40  'to 40'
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

 L.  81       358  LOAD_FAST                'lexer'
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
          430_432  POP_JUMP_IF_FALSE   668  'to 668'

 L.  87       434  LOAD_GLOBAL              os
              436  LOAD_ATTR                name
              438  LOAD_STR                 'posix'
              440  COMPARE_OP               ==
          442_444  POP_JUMP_IF_FALSE   658  'to 658'
              446  LOAD_FAST                'default_netrc'
          448_450  POP_JUMP_IF_FALSE   658  'to 658'

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
          478_480  POP_JUMP_IF_FALSE   624  'to 624'

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
              510  JUMP_FORWARD        544  'to 544'
            512_0  COME_FROM_FINALLY   490  '490'

 L.  93       512  DUP_TOP          
              514  LOAD_GLOBAL              KeyError
              516  COMPARE_OP               exception-match
          518_520  POP_JUMP_IF_FALSE   542  'to 542'
              522  POP_TOP          
              524  POP_TOP          
              526  POP_TOP          

 L.  94       528  LOAD_STR                 'uid %s'
              530  LOAD_FAST                'prop'
              532  LOAD_ATTR                st_uid
              534  BINARY_MODULO    
              536  STORE_FAST               'fowner'
              538  POP_EXCEPT       
              540  JUMP_FORWARD        544  'to 544'
            542_0  COME_FROM           518  '518'
              542  END_FINALLY      
            544_0  COME_FROM           540  '540'
            544_1  COME_FROM           510  '510'

 L.  95       544  SETUP_FINALLY       568  'to 568'

 L.  96       546  LOAD_FAST                'pwd'
              548  LOAD_METHOD              getpwuid
              550  LOAD_GLOBAL              os
              552  LOAD_METHOD              getuid
              554  CALL_METHOD_0         0  ''
              556  CALL_METHOD_1         1  ''
              558  LOAD_CONST               0
              560  BINARY_SUBSCR    
              562  STORE_FAST               'user'
              564  POP_BLOCK        
              566  JUMP_FORWARD        602  'to 602'
            568_0  COME_FROM_FINALLY   544  '544'

 L.  97       568  DUP_TOP          
              570  LOAD_GLOBAL              KeyError
              572  COMPARE_OP               exception-match
          574_576  POP_JUMP_IF_FALSE   600  'to 600'
              578  POP_TOP          
              580  POP_TOP          
              582  POP_TOP          

 L.  98       584  LOAD_STR                 'uid %s'
              586  LOAD_GLOBAL              os
              588  LOAD_METHOD              getuid
              590  CALL_METHOD_0         0  ''
              592  BINARY_MODULO    
              594  STORE_FAST               'user'
              596  POP_EXCEPT       
              598  JUMP_FORWARD        602  'to 602'
            600_0  COME_FROM           574  '574'
              600  END_FINALLY      
            602_0  COME_FROM           598  '598'
            602_1  COME_FROM           566  '566'

 L.  99       602  LOAD_GLOBAL              NetrcParseError

 L. 100       604  LOAD_STR                 '~/.netrc file owner (%s) does not match current user (%s)'

 L. 101       606  LOAD_FAST                'fowner'
              608  LOAD_FAST                'user'
              610  BUILD_TUPLE_2         2 

 L. 100       612  BINARY_MODULO    

 L. 102       614  LOAD_FAST                'file'

 L. 102       616  LOAD_FAST                'lexer'
              618  LOAD_ATTR                lineno

 L.  99       620  CALL_FUNCTION_3       3  ''
              622  RAISE_VARARGS_1       1  'exception instance'
            624_0  COME_FROM           478  '478'

 L. 103       624  LOAD_FAST                'prop'
              626  LOAD_ATTR                st_mode
              628  LOAD_GLOBAL              stat
              630  LOAD_ATTR                S_IRWXG
              632  LOAD_GLOBAL              stat
              634  LOAD_ATTR                S_IRWXO
              636  BINARY_OR        
              638  BINARY_AND       
          640_642  POP_JUMP_IF_FALSE   658  'to 658'

 L. 104       644  LOAD_GLOBAL              NetrcParseError

 L. 105       646  LOAD_STR                 '~/.netrc access too permissive: access permissions must restrict access to only the owner'

 L. 107       648  LOAD_FAST                'file'

 L. 107       650  LOAD_FAST                'lexer'
              652  LOAD_ATTR                lineno

 L. 104       654  CALL_FUNCTION_3       3  ''
              656  RAISE_VARARGS_1       1  'exception instance'
            658_0  COME_FROM           640  '640'
            658_1  COME_FROM           448  '448'
            658_2  COME_FROM           442  '442'

 L. 108       658  LOAD_FAST                'lexer'
              660  LOAD_METHOD              get_token
              662  CALL_METHOD_0         0  ''
              664  STORE_FAST               'password'
              666  JUMP_BACK           272  'to 272'
            668_0  COME_FROM           430  '430'

 L. 110       668  LOAD_GLOBAL              NetrcParseError
              670  LOAD_STR                 'bad follower token %r'
              672  LOAD_FAST                'tt'
              674  BINARY_MODULO    

 L. 111       676  LOAD_FAST                'file'

 L. 111       678  LOAD_FAST                'lexer'
              680  LOAD_ATTR                lineno

 L. 110       682  CALL_FUNCTION_3       3  ''
              684  RAISE_VARARGS_1       1  'exception instance'
          686_688  JUMP_BACK           272  'to 272'
              690  JUMP_BACK            40  'to 40'
            692_0  COME_FROM            62  '62'

Parse error at or near `JUMP_BACK' instruction at offset 690

    def authenticators(self, host):
        """Return a (user, account, password) tuple for given host."""
        if host in self.hosts:
            return self.hosts[host]
        if 'default' in self.hosts:
            return self.hosts['default']
        return

    def __repr__(self):
        """Dump the class data in the format of a .netrc file."""
        rep = ''
        for host in self.hosts.keys:
            attrs = self.hosts[host]
            rep += f"machine {host}\n\tlogin {attrs[0]}\n"
            if attrs[1]:
                rep += f"\taccount {attrs[1]}\n"
            else:
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