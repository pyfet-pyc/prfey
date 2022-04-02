# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\numpy\distutils\from_template.py
r"""

process_file(filename)

  takes templated file .xxx.src and produces .xxx file where .xxx
  is .pyf .f90 or .f using the following template rules:

  '<..>' denotes a template.

  All function and subroutine blocks in a source file with names that
  contain '<..>' will be replicated according to the rules in '<..>'.

  The number of comma-separated words in '<..>' will determine the number of
  replicates.

  '<..>' may have two different forms, named and short. For example,

  named:
   <p=d,s,z,c> where anywhere inside a block '<p>' will be replaced with
   'd', 's', 'z', and 'c' for each replicate of the block.

   <_c>  is already defined: <_c=s,d,c,z>
   <_t>  is already defined: <_t=real,double precision,complex,double complex>

  short:
   <s,d,c,z>, a short form of the named, useful when no <p> appears inside
   a block.

  In general, '<..>' contains a comma separated list of arbitrary
  expressions. If these expression must contain a comma|leftarrow|rightarrow,
  then prepend the comma|leftarrow|rightarrow with a backslash.

  If an expression matches '\<index>' then it will be replaced
  by <index>-th expression.

  Note that all '<..>' forms in a block must have the same number of
  comma-separated entries.

 Predefined named template rules:
  <prefix=s,d,c,z>
  <ftype=real,double precision,complex,double complex>
  <ftypereal=real,double precision,\0,\1>
  <ctype=float,double,complex_float,complex_double>
  <ctypereal=float,double,\0,\1>

"""
__all__ = [
 'process_str', 'process_file']
import os, sys, re
routine_start_re = re.compile('(\\n|\\A)((     (\\$|\\*))|)\\s*(subroutine|function)\\b', re.I)
routine_end_re = re.compile('\\n\\s*end\\s*(subroutine|function)\\b.*(\\n|\\Z)', re.I)
function_start_re = re.compile('\\n     (\\$|\\*)\\s*function\\b', re.I)

def parse_structure--- This code section failed: ---

 L.  64         0  BUILD_LIST_0          0 
                2  STORE_FAST               'spanlist'

 L.  65         4  LOAD_CONST               0
                6  STORE_FAST               'ind'
              8_0  COME_FROM           174  '174'

 L.  67         8  LOAD_GLOBAL              routine_start_re
               10  LOAD_METHOD              search
               12  LOAD_FAST                'astr'
               14  LOAD_FAST                'ind'
               16  CALL_METHOD_2         2  ''
               18  STORE_FAST               'm'

 L.  68        20  LOAD_FAST                'm'
               22  LOAD_CONST               None
               24  COMPARE_OP               is
               26  POP_JUMP_IF_FALSE    30  'to 30'

 L.  69        28  JUMP_FORWARD        176  'to 176'
             30_0  COME_FROM            26  '26'

 L.  70        30  LOAD_FAST                'm'
               32  LOAD_METHOD              start
               34  CALL_METHOD_0         0  ''
               36  STORE_FAST               'start'

 L.  71        38  LOAD_GLOBAL              function_start_re
               40  LOAD_METHOD              match
               42  LOAD_FAST                'astr'
               44  LOAD_FAST                'start'
               46  LOAD_FAST                'm'
               48  LOAD_METHOD              end
               50  CALL_METHOD_0         0  ''
               52  CALL_METHOD_3         3  ''
               54  POP_JUMP_IF_FALSE   108  'to 108'
             56_0  COME_FROM           106  '106'
             56_1  COME_FROM           102  '102'

 L.  73        56  LOAD_FAST                'astr'
               58  LOAD_METHOD              rfind
               60  LOAD_STR                 '\n'
               62  LOAD_FAST                'ind'
               64  LOAD_FAST                'start'
               66  CALL_METHOD_3         3  ''
               68  STORE_FAST               'i'

 L.  74        70  LOAD_FAST                'i'
               72  LOAD_CONST               -1
               74  COMPARE_OP               ==
               76  POP_JUMP_IF_FALSE    80  'to 80'

 L.  75        78  JUMP_FORWARD        108  'to 108'
             80_0  COME_FROM            76  '76'

 L.  76        80  LOAD_FAST                'i'
               82  STORE_FAST               'start'

 L.  77        84  LOAD_FAST                'astr'
               86  LOAD_FAST                'i'
               88  LOAD_FAST                'i'
               90  LOAD_CONST               7
               92  BINARY_ADD       
               94  BUILD_SLICE_2         2 
               96  BINARY_SUBSCR    
               98  LOAD_STR                 '\n     $'
              100  COMPARE_OP               !=
              102  POP_JUMP_IF_FALSE_BACK    56  'to 56'

 L.  78       104  JUMP_FORWARD        108  'to 108'
              106  JUMP_BACK            56  'to 56'
            108_0  COME_FROM           104  '104'
            108_1  COME_FROM            78  '78'
            108_2  COME_FROM            54  '54'

 L.  79       108  LOAD_FAST                'start'
              110  LOAD_CONST               1
              112  INPLACE_ADD      
              114  STORE_FAST               'start'

 L.  80       116  LOAD_GLOBAL              routine_end_re
              118  LOAD_METHOD              search
              120  LOAD_FAST                'astr'
              122  LOAD_FAST                'm'
              124  LOAD_METHOD              end
              126  CALL_METHOD_0         0  ''
              128  CALL_METHOD_2         2  ''
              130  STORE_FAST               'm'

 L.  81       132  LOAD_FAST                'm'
              134  POP_JUMP_IF_FALSE   148  'to 148'
              136  LOAD_FAST                'm'
              138  LOAD_METHOD              end
              140  CALL_METHOD_0         0  ''
              142  LOAD_CONST               1
              144  BINARY_SUBTRACT  
              146  JUMP_IF_TRUE_OR_POP   154  'to 154'
            148_0  COME_FROM           134  '134'
              148  LOAD_GLOBAL              len
              150  LOAD_FAST                'astr'
              152  CALL_FUNCTION_1       1  ''
            154_0  COME_FROM           146  '146'
              154  DUP_TOP          
              156  STORE_FAST               'ind'
              158  STORE_FAST               'end'

 L.  82       160  LOAD_FAST                'spanlist'
              162  LOAD_METHOD              append
              164  LOAD_FAST                'start'
              166  LOAD_FAST                'end'
              168  BUILD_TUPLE_2         2 
              170  CALL_METHOD_1         1  ''
              172  POP_TOP          
              174  JUMP_BACK             8  'to 8'
            176_0  COME_FROM            28  '28'

 L.  83       176  LOAD_FAST                'spanlist'
              178  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 106


template_re = re.compile('<\\s*(\\w[\\w\\d]*)\\s*>')
named_re = re.compile('<\\s*(\\w[\\w\\d]*)\\s*=\\s*(.*?)\\s*>')
list_re = re.compile('<\\s*((.*?))\\s*>')

def find_repl_patterns(astr):
    reps = named_re.findall(astr)
    names = {}
    for rep in reps:
        name = rep[0].strip or unique_key(names)
        repl = rep[1].replace('\\,', '@comma@')
        thelist = conv(repl)
        names[name] = thelist
    else:
        return names


def find_and_remove_repl_patterns(astr):
    names = find_repl_patterns(astr)
    astr = re.subnnamed_re''astr[0]
    return (
     astr, names)


item_re = re.compile('\\A\\\\(?P<index>\\d+)\\Z')

def conv(astr):
    b = astr.split(',')
    l = [x.strip for x in b]
    for i in range(len(l)):
        m = item_re.match(l[i])
        if m:
            j = int(m.group('index'))
            l[i] = l[j]
    else:
        return ','.join(l)


def unique_key(adict):
    """ Obtain a unique key given a dictionary."""
    allkeys = list(adict.keys)
    done = False
    n = 1
    while True:
        while True:
            if not done:
                newkey = '__l%s' % n
                if newkey in allkeys:
                    n += 1

        done = True

    return newkey


template_name_re = re.compile('\\A\\s*(\\w[\\w\\d]*)\\s*\\Z')

def expand_sub(substr, names):
    substr = substr.replace('\\>', '@rightarrow@')
    substr = substr.replace('\\<', '@leftarrow@')
    lnames = find_repl_patterns(substr)
    substr = named_re.sub('<\\1>', substr)

    def listrepl(mobj):
        thelist = conv(mobj.group(1).replace('\\,', '@comma@'))
        if template_name_re.match(thelist):
            return '<%s>' % thelist
        name = None
        for key in lnames.keys:
            if lnames[key] == thelist:
                name = key
        else:
            if name is None:
                name = unique_key(lnames)
                lnames[name] = thelist
            return '<%s>' % name

    substr = list_re.sub(listrepl, substr)
    numsubs = None
    base_rule = None
    rules = {}
    for r in template_re.findall(substr):
        if r not in rules:
            thelist = lnames.get(r, names.get(r, None))
            if thelist is None:
                raise ValueError('No replicates found for <%s>' % r)
            if r not in names:
                if not thelist.startswith('_'):
                    names[r] = thelist
            rule = [i.replace('@comma@', ',') for i in thelist.split(',')]
            num = len(rule)
            if numsubs is None:
                numsubs = num
                rules[r] = rule
                base_rule = r
            else:
                if num == numsubs:
                    rules[r] = rule
                else:
                    print('Mismatch in number of replacements (base <%s=%s>) for <%s=%s>. Ignoring.' % (
                     base_rule, ','.join(rules[base_rule]), r, thelist))
    else:
        if not rules:
            return substr

        def namerepl(mobj):
            name = mobj.group(1)
            return rules.get(name, (k + 1) * [name])[k]

        newstr = ''
        for k in range(numsubs):
            newstr += template_re.sub(namerepl, substr) + '\n\n'
        else:
            newstr = newstr.replace('@rightarrow@', '>')
            newstr = newstr.replace('@leftarrow@', '<')
            return newstr


def process_str(allstr):
    newstr = allstr
    writestr = ''
    struct = parse_structure(newstr)
    oldend = 0
    names = {}
    names.update(_special_names)
    for sub in struct:
        cleanedstr, defs = find_and_remove_repl_patterns(newstr[oldend:sub[0]])
        writestr += cleanedstr
        names.update(defs)
        writestr += expand_sub(newstr[sub[0]:sub[1]], names)
        oldend = sub[1]
    else:
        writestr += newstr[oldend:]
        return writestr


include_src_re = re.compile('(\\n|\\A)\\s*include\\s*[\'\\"](?P<name>[\\w\\d./\\\\]+[.]src)[\'\\"]', re.I)

def resolve_includes(source):
    d = os.path.dirname(source)
    with open(source) as fid:
        lines = []
        for line in fid:
            m = include_src_re.match(line)
            if m:
                fn = m.group('name')
                if not os.path.isabs(fn):
                    fn = os.path.join(d, fn)
                elif os.path.isfile(fn):
                    print('Including file', fn)
                    lines.extend(resolve_includes(fn))
                else:
                    lines.append(line)
            else:
                lines.append(line)

    return lines


def process_file(source):
    lines = resolve_includes(source)
    return process_str(''.join(lines))


_special_names = find_repl_patterns('\n<_c=s,d,c,z>\n<_t=real,double precision,complex,double complex>\n<prefix=s,d,c,z>\n<ftype=real,double precision,complex,double complex>\n<ctype=float,double,complex_float,complex_double>\n<ftypereal=real,double precision,\\0,\\1>\n<ctypereal=float,double,\\0,\\1>\n')

def main():
    try:
        file = sys.argv[1]
    except IndexError:
        fid = sys.stdin
        outfile = sys.stdout
    else:
        fid = open(file, 'r')
        base, ext = os.path.splitext(file)
        newname = base
        outfile = open(newname, 'w')
    allstr = fid.read
    writestr = process_str(allstr)
    outfile.write(writestr)


if __name__ == '__main__':
    main()