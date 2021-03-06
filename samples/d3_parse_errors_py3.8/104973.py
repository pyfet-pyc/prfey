# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: argparse.py
"""Command-line parsing library

This module is an optparse-inspired command-line parsing library that:

    - handles both optional and positional arguments
    - produces highly informative usage messages
    - supports parsers that dispatch to sub-parsers

The following is a simple usage example that sums integers from the
command-line and writes the result to a file::

    parser = argparse.ArgumentParser(
        description='sum the integers at the command line')
    parser.add_argument(
        'integers', metavar='int', nargs='+', type=int,
        help='an integer to be summed')
    parser.add_argument(
        '--log', default=sys.stdout, type=argparse.FileType('w'),
        help='the file where the sum should be written')
    args = parser.parse_args()
    args.log.write('%s' % sum(args.integers))
    args.log.close()

The module contains the following public classes:

    - ArgumentParser -- The main entry point for command-line parsing. As the
        example above shows, the add_argument() method is used to populate
        the parser with actions for optional and positional arguments. Then
        the parse_args() method is invoked to convert the args at the
        command-line into an object with attributes.

    - ArgumentError -- The exception raised by ArgumentParser objects when
        there are errors with the parser's actions. Errors raised while
        parsing the command-line are caught by ArgumentParser and emitted
        as command-line messages.

    - FileType -- A factory for defining types of files to be created. As the
        example above shows, instances of FileType are typically passed as
        the type= argument of add_argument() calls.

    - Action -- The base class for parser actions. Typically actions are
        selected by passing strings like 'store_true' or 'append_const' to
        the action= argument of add_argument(). However, for greater
        customization of ArgumentParser actions, subclasses of Action may
        be defined and passed as the action= argument.

    - HelpFormatter, RawDescriptionHelpFormatter, RawTextHelpFormatter,
        ArgumentDefaultsHelpFormatter -- Formatter classes which
        may be passed as the formatter_class= argument to the
        ArgumentParser constructor. HelpFormatter is the default,
        RawDescriptionHelpFormatter and RawTextHelpFormatter tell the parser
        not to change the formatting for help text, and
        ArgumentDefaultsHelpFormatter adds information about argument defaults
        to the help.

All other classes in this module are considered implementation details.
(Also note that HelpFormatter and RawDescriptionHelpFormatter are only
considered public as object names -- the API of the formatter objects is
still considered an implementation detail.)
"""
__version__ = '1.1'
__all__ = [
 'ArgumentParser',
 'ArgumentError',
 'ArgumentTypeError',
 'FileType',
 'HelpFormatter',
 'ArgumentDefaultsHelpFormatter',
 'RawDescriptionHelpFormatter',
 'RawTextHelpFormatter',
 'MetavarTypeHelpFormatter',
 'Namespace',
 'Action',
 'ONE_OR_MORE',
 'OPTIONAL',
 'PARSER',
 'REMAINDER',
 'SUPPRESS',
 'ZERO_OR_MORE']
import os as _os, re as _re, shutil as _shutil, sys as _sys
from gettext import gettext as _, ngettext
SUPPRESS = '==SUPPRESS=='
OPTIONAL = '?'
ZERO_OR_MORE = '*'
ONE_OR_MORE = '+'
PARSER = 'A...'
REMAINDER = '...'
_UNRECOGNIZED_ARGS_ATTR = '_unrecognized_args'

class _AttributeHolder(object):
    __doc__ = "Abstract base class that provides __repr__.\n\n    The __repr__ method returns a string in the format::\n        ClassName(attr=name, attr=name, ...)\n    The attributes are determined either by a class-level attribute,\n    '_kwarg_names', or by inspecting the instance __dict__.\n    "

    def __repr__(self):
        type_name = type(self).__name__
        arg_strings = []
        star_args = {}
        for arg in self._get_args():
            arg_strings.append(repr(arg))
        else:
            for name, value in self._get_kwargs():
                if name.isidentifier():
                    arg_strings.append('%s=%r' % (name, value))
                else:
                    star_args[name] = value
            else:
                if star_args:
                    arg_strings.append('**%s' % repr(star_args))
                return '%s(%s)' % (type_name, ', '.join(arg_strings))

    def _get_kwargs(self):
        return sorted(self.__dict__.items())

    def _get_args(self):
        return []


def _copy_items(items):
    if items is None:
        return []
    if type(items) is list:
        return items[:]
    import copy
    return copy.copy(items)


class HelpFormatter(object):
    __doc__ = 'Formatter for generating usage messages and argument help strings.\n\n    Only the name of this class is considered a public API. All the methods\n    provided by the class are considered an implementation detail.\n    '

    def __init__(self, prog, indent_increment=2, max_help_position=24, width=None):
        if width is None:
            width = _shutil.get_terminal_size().columns
            width -= 2
        self._prog = prog
        self._indent_increment = indent_increment
        self._max_help_position = min(max_help_position, max(width - 20, indent_increment * 2))
        self._width = width
        self._current_indent = 0
        self._level = 0
        self._action_max_length = 0
        self._root_section = self._Section(self, None)
        self._current_section = self._root_section
        self._whitespace_matcher = _re.compile('\\s+', _re.ASCII)
        self._long_break_matcher = _re.compile('\\n\\n\\n+')

    def _indent(self):
        self._current_indent += self._indent_increment
        self._level += 1

    def _dedent(self):
        self._current_indent -= self._indent_increment
        assert self._current_indent >= 0, 'Indent decreased below 0.'
        self._level -= 1

    class _Section(object):

        def __init__(self, formatter, parent, heading=None):
            self.formatter = formatter
            self.parent = parent
            self.heading = heading
            self.items = []

        def format_help(self):
            if self.parent is not None:
                self.formatter._indent()
            join = self.formatter._join_parts
            item_help = join([func(*args) for func, args in self.items])
            if self.parent is not None:
                self.formatter._dedent()
            if not item_help:
                return ''
            if self.heading is not SUPPRESS and self.heading is not None:
                current_indent = self.formatter._current_indent
                heading = '%*s%s:\n' % (current_indent, '', self.heading)
            else:
                heading = ''
            return join(['\n', heading, item_help, '\n'])

    def _add_item(self, func, args):
        self._current_section.items.append((func, args))

    def start_section(self, heading):
        self._indent()
        section = self._Section(self, self._current_section, heading)
        self._add_item(section.format_help, [])
        self._current_section = section

    def end_section(self):
        self._current_section = self._current_section.parent
        self._dedent()

    def add_text(self, text):
        if text is not SUPPRESS:
            if text is not None:
                self._add_item(self._format_text, [text])

    def add_usage(self, usage, actions, groups, prefix=None):
        if usage is not SUPPRESS:
            args = (
             usage, actions, groups, prefix)
            self._add_item(self._format_usage, args)

    def add_argument(self, action):
        if action.help is not SUPPRESS:
            get_invocation = self._format_action_invocation
            invocations = [get_invocation(action)]
            for subaction in self._iter_indented_subactions(action):
                invocations.append(get_invocation(subaction))
            else:
                invocation_length = max([len(s) for s in invocations])
                action_length = invocation_length + self._current_indent
                self._action_max_length = max(self._action_max_length, action_length)
                self._add_item(self._format_action, [action])

    def add_arguments(self, actions):
        for action in actions:
            self.add_argument(action)

    def format_help(self):
        help = self._root_section.format_help()
        if help:
            help = self._long_break_matcher.sub('\n\n', help)
            help = help.strip('\n') + '\n'
        return help

    def _join_parts(self, part_strings):
        return ''.join([part for part in part_strings if part if part is not SUPPRESS])

    def _format_usage(self, usage, actions, groups, prefix):
        if prefix is None:
            prefix = _('usage: ')
        if usage is not None:
            usage = usage % dict(prog=(self._prog))
        elif usage is None and not actions:
            usage = '%(prog)s' % dict(prog=(self._prog))
        elif usage is None:
            prog = '%(prog)s' % dict(prog=(self._prog))
            optionals = []
            positionals = []
            for action in actions:
                if action.option_strings:
                    optionals.append(action)
                else:
                    positionals.append(action)
            else:
                format = self._format_actions_usage
                action_usage = format(optionals + positionals, groups)
                usage = ' '.join([s for s in (prog, action_usage) if s])
                text_width = self._width - self._current_indent
                if len(prefix) + len(usage) > text_width:
                    part_regexp = '\\(.*?\\)+(?=\\s|$)|\\[.*?\\]+(?=\\s|$)|\\S+'
                    opt_usage = format(optionals, groups)
                    pos_usage = format(positionals, groups)
                    opt_parts = _re.findall(part_regexp, opt_usage)
                    pos_parts = _re.findall(part_regexp, pos_usage)
                    assert ' '.join(opt_parts) == opt_usage
                    assert ' '.join(pos_parts) == pos_usage

                    def get_lines(parts, indent, prefix=None):
                        lines = []
                        line = []
                        if prefix is not None:
                            line_len = len(prefix) - 1
                        else:
                            line_len = len(indent) - 1
                        for part in parts:
                            if line_len + 1 + len(part) > text_width:
                                if line:
                                    lines.append(indent + ' '.join(line))
                                    line = []
                                    line_len = len(indent) - 1
                            line.append(part)
                            line_len += len(part) + 1
                        else:
                            if line:
                                lines.append(indent + ' '.join(line))
                            if prefix is not None:
                                lines[0] = lines[0][len(indent):]
                            return lines

                    if len(prefix) + len(prog) <= 0.75 * text_width:
                        indent = ' ' * (len(prefix) + len(prog) + 1)
                        if opt_parts:
                            lines = get_lines([prog] + opt_parts, indent, prefix)
                            lines.extend(get_lines(pos_parts, indent))
                        elif pos_parts:
                            lines = get_lines([prog] + pos_parts, indent, prefix)
                        else:
                            lines = [
                             prog]
                    else:
                        indent = ' ' * len(prefix)
                        parts = opt_parts + pos_parts
                        lines = get_lines(parts, indent)
                        if len(lines) > 1:
                            lines = []
                            lines.extend(get_lines(opt_parts, indent))
                            lines.extend(get_lines(pos_parts, indent))
                        lines = [
                         prog] + lines
                    usage = '\n'.join(lines)

        return '%s%s\n\n' % (prefix, usage)

    def _format_actions_usage--- This code section failed: ---

 L. 391         0  LOAD_GLOBAL              set
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'group_actions'

 L. 392         6  BUILD_MAP_0           0 
                8  STORE_FAST               'inserts'

 L. 393        10  LOAD_FAST                'groups'
               12  GET_ITER         
             14_0  COME_FROM           296  '296'
             14_1  COME_FROM            96  '96'
             14_2  COME_FROM            62  '62'
             14_3  COME_FROM            58  '58'
            14_16  FOR_ITER            298  'to 298'
               18  STORE_FAST               'group'

 L. 394        20  SETUP_FINALLY        42  'to 42'

 L. 395        22  LOAD_FAST                'actions'
               24  LOAD_METHOD              index
               26  LOAD_FAST                'group'
               28  LOAD_ATTR                _group_actions
               30  LOAD_CONST               0
               32  BINARY_SUBSCR    
               34  CALL_METHOD_1         1  ''
               36  STORE_FAST               'start'
               38  POP_BLOCK        
               40  JUMP_FORWARD         66  'to 66'
             42_0  COME_FROM_FINALLY    20  '20'

 L. 396        42  DUP_TOP          
               44  LOAD_GLOBAL              ValueError
               46  COMPARE_OP               exception-match
               48  POP_JUMP_IF_FALSE    64  'to 64'
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L. 397        56  POP_EXCEPT       
               58  JUMP_BACK            14  'to 14'
               60  POP_EXCEPT       
               62  JUMP_BACK            14  'to 14'
             64_0  COME_FROM            48  '48'
               64  END_FINALLY      
             66_0  COME_FROM            40  '40'

 L. 399        66  LOAD_FAST                'start'
               68  LOAD_GLOBAL              len
               70  LOAD_FAST                'group'
               72  LOAD_ATTR                _group_actions
               74  CALL_FUNCTION_1       1  ''
               76  BINARY_ADD       
               78  STORE_FAST               'end'

 L. 400        80  LOAD_FAST                'actions'
               82  LOAD_FAST                'start'
               84  LOAD_FAST                'end'
               86  BUILD_SLICE_2         2 
               88  BINARY_SUBSCR    
               90  LOAD_FAST                'group'
               92  LOAD_ATTR                _group_actions
               94  COMPARE_OP               ==
               96  POP_JUMP_IF_FALSE_BACK    14  'to 14'

 L. 401        98  LOAD_FAST                'group'
              100  LOAD_ATTR                _group_actions
              102  GET_ITER         
            104_0  COME_FROM           118  '118'
              104  FOR_ITER            120  'to 120'
              106  STORE_FAST               'action'

 L. 402       108  LOAD_FAST                'group_actions'
              110  LOAD_METHOD              add
              112  LOAD_FAST                'action'
              114  CALL_METHOD_1         1  ''
              116  POP_TOP          
              118  JUMP_BACK           104  'to 104'
            120_0  COME_FROM           104  '104'

 L. 403       120  LOAD_FAST                'group'
              122  LOAD_ATTR                required
              124  POP_JUMP_IF_TRUE    196  'to 196'

 L. 404       126  LOAD_FAST                'start'
              128  LOAD_FAST                'inserts'
              130  COMPARE_OP               in
              132  POP_JUMP_IF_FALSE   152  'to 152'

 L. 405       134  LOAD_FAST                'inserts'
              136  LOAD_FAST                'start'
              138  DUP_TOP_TWO      
              140  BINARY_SUBSCR    
              142  LOAD_STR                 ' ['
              144  INPLACE_ADD      
              146  ROT_THREE        
              148  STORE_SUBSCR     
              150  JUMP_FORWARD        160  'to 160'
            152_0  COME_FROM           132  '132'

 L. 407       152  LOAD_STR                 '['
              154  LOAD_FAST                'inserts'
              156  LOAD_FAST                'start'
              158  STORE_SUBSCR     
            160_0  COME_FROM           150  '150'

 L. 408       160  LOAD_FAST                'end'
              162  LOAD_FAST                'inserts'
              164  COMPARE_OP               in
              166  POP_JUMP_IF_FALSE   186  'to 186'

 L. 409       168  LOAD_FAST                'inserts'
              170  LOAD_FAST                'end'
              172  DUP_TOP_TWO      
              174  BINARY_SUBSCR    
              176  LOAD_STR                 ']'
              178  INPLACE_ADD      
              180  ROT_THREE        
              182  STORE_SUBSCR     
              184  JUMP_FORWARD        194  'to 194'
            186_0  COME_FROM           166  '166'

 L. 411       186  LOAD_STR                 ']'
              188  LOAD_FAST                'inserts'
              190  LOAD_FAST                'end'
              192  STORE_SUBSCR     
            194_0  COME_FROM           184  '184'
              194  JUMP_FORWARD        266  'to 266'
            196_0  COME_FROM           124  '124'

 L. 413       196  LOAD_FAST                'start'
              198  LOAD_FAST                'inserts'
              200  COMPARE_OP               in
              202  POP_JUMP_IF_FALSE   222  'to 222'

 L. 414       204  LOAD_FAST                'inserts'
              206  LOAD_FAST                'start'
              208  DUP_TOP_TWO      
              210  BINARY_SUBSCR    
              212  LOAD_STR                 ' ('
              214  INPLACE_ADD      
              216  ROT_THREE        
              218  STORE_SUBSCR     
              220  JUMP_FORWARD        230  'to 230'
            222_0  COME_FROM           202  '202'

 L. 416       222  LOAD_STR                 '('
              224  LOAD_FAST                'inserts'
              226  LOAD_FAST                'start'
              228  STORE_SUBSCR     
            230_0  COME_FROM           220  '220'

 L. 417       230  LOAD_FAST                'end'
              232  LOAD_FAST                'inserts'
              234  COMPARE_OP               in
          236_238  POP_JUMP_IF_FALSE   258  'to 258'

 L. 418       240  LOAD_FAST                'inserts'
              242  LOAD_FAST                'end'
              244  DUP_TOP_TWO      
              246  BINARY_SUBSCR    
              248  LOAD_STR                 ')'
              250  INPLACE_ADD      
              252  ROT_THREE        
              254  STORE_SUBSCR     
              256  JUMP_FORWARD        266  'to 266'
            258_0  COME_FROM           236  '236'

 L. 420       258  LOAD_STR                 ')'
              260  LOAD_FAST                'inserts'
              262  LOAD_FAST                'end'
              264  STORE_SUBSCR     
            266_0  COME_FROM           256  '256'
            266_1  COME_FROM           194  '194'

 L. 421       266  LOAD_GLOBAL              range
              268  LOAD_FAST                'start'
              270  LOAD_CONST               1
              272  BINARY_ADD       
              274  LOAD_FAST                'end'
              276  CALL_FUNCTION_2       2  ''
              278  GET_ITER         
            280_0  COME_FROM           292  '292'
              280  FOR_ITER            296  'to 296'
              282  STORE_FAST               'i'

 L. 422       284  LOAD_STR                 '|'
              286  LOAD_FAST                'inserts'
              288  LOAD_FAST                'i'
              290  STORE_SUBSCR     
          292_294  JUMP_BACK           280  'to 280'
            296_0  COME_FROM           280  '280'
              296  JUMP_BACK            14  'to 14'
            298_0  COME_FROM            14  '14'

 L. 425       298  BUILD_LIST_0          0 
              300  STORE_FAST               'parts'

 L. 426       302  LOAD_GLOBAL              enumerate
              304  LOAD_FAST                'actions'
              306  CALL_FUNCTION_1       1  ''
              308  GET_ITER         
            310_0  COME_FROM           600  '600'
            310_1  COME_FROM           496  '496'
            310_2  COME_FROM           404  '404'
          310_312  FOR_ITER            604  'to 604'
              314  UNPACK_SEQUENCE_2     2 
              316  STORE_FAST               'i'
              318  STORE_FAST               'action'

 L. 430       320  LOAD_FAST                'action'
              322  LOAD_ATTR                help
              324  LOAD_GLOBAL              SUPPRESS
              326  COMPARE_OP               is
          328_330  POP_JUMP_IF_FALSE   406  'to 406'

 L. 431       332  LOAD_FAST                'parts'
              334  LOAD_METHOD              append
              336  LOAD_CONST               None
              338  CALL_METHOD_1         1  ''
              340  POP_TOP          

 L. 432       342  LOAD_FAST                'inserts'
              344  LOAD_METHOD              get
              346  LOAD_FAST                'i'
              348  CALL_METHOD_1         1  ''
              350  LOAD_STR                 '|'
              352  COMPARE_OP               ==
          354_356  POP_JUMP_IF_FALSE   370  'to 370'

 L. 433       358  LOAD_FAST                'inserts'
              360  LOAD_METHOD              pop
              362  LOAD_FAST                'i'
              364  CALL_METHOD_1         1  ''
              366  POP_TOP          
              368  JUMP_FORWARD        404  'to 404'
            370_0  COME_FROM           354  '354'

 L. 434       370  LOAD_FAST                'inserts'
              372  LOAD_METHOD              get
              374  LOAD_FAST                'i'
              376  LOAD_CONST               1
              378  BINARY_ADD       
              380  CALL_METHOD_1         1  ''
              382  LOAD_STR                 '|'
              384  COMPARE_OP               ==
          386_388  POP_JUMP_IF_FALSE   600  'to 600'

 L. 435       390  LOAD_FAST                'inserts'
              392  LOAD_METHOD              pop
              394  LOAD_FAST                'i'
              396  LOAD_CONST               1
              398  BINARY_ADD       
              400  CALL_METHOD_1         1  ''
              402  POP_TOP          
            404_0  COME_FROM           368  '368'
              404  JUMP_BACK           310  'to 310'
            406_0  COME_FROM           328  '328'

 L. 438       406  LOAD_FAST                'action'
              408  LOAD_ATTR                option_strings
          410_412  POP_JUMP_IF_TRUE    498  'to 498'

 L. 439       414  LOAD_FAST                'self'
              416  LOAD_METHOD              _get_default_metavar_for_positional
              418  LOAD_FAST                'action'
              420  CALL_METHOD_1         1  ''
              422  STORE_FAST               'default'

 L. 440       424  LOAD_FAST                'self'
              426  LOAD_METHOD              _format_args
              428  LOAD_FAST                'action'
              430  LOAD_FAST                'default'
              432  CALL_METHOD_2         2  ''
              434  STORE_FAST               'part'

 L. 443       436  LOAD_FAST                'action'
              438  LOAD_FAST                'group_actions'
              440  COMPARE_OP               in
          442_444  POP_JUMP_IF_FALSE   486  'to 486'

 L. 444       446  LOAD_FAST                'part'
              448  LOAD_CONST               0
              450  BINARY_SUBSCR    
              452  LOAD_STR                 '['
              454  COMPARE_OP               ==
          456_458  POP_JUMP_IF_FALSE   486  'to 486'
              460  LOAD_FAST                'part'
              462  LOAD_CONST               -1
              464  BINARY_SUBSCR    
              466  LOAD_STR                 ']'
              468  COMPARE_OP               ==
          470_472  POP_JUMP_IF_FALSE   486  'to 486'

 L. 445       474  LOAD_FAST                'part'
              476  LOAD_CONST               1
              478  LOAD_CONST               -1
              480  BUILD_SLICE_2         2 
              482  BINARY_SUBSCR    
              484  STORE_FAST               'part'
            486_0  COME_FROM           470  '470'
            486_1  COME_FROM           456  '456'
            486_2  COME_FROM           442  '442'

 L. 448       486  LOAD_FAST                'parts'
              488  LOAD_METHOD              append
              490  LOAD_FAST                'part'
              492  CALL_METHOD_1         1  ''
              494  POP_TOP          
              496  JUMP_BACK           310  'to 310'
            498_0  COME_FROM           410  '410'

 L. 452       498  LOAD_FAST                'action'
              500  LOAD_ATTR                option_strings
              502  LOAD_CONST               0
              504  BINARY_SUBSCR    
              506  STORE_FAST               'option_string'

 L. 456       508  LOAD_FAST                'action'
              510  LOAD_ATTR                nargs
              512  LOAD_CONST               0
              514  COMPARE_OP               ==
          516_518  POP_JUMP_IF_FALSE   530  'to 530'

 L. 457       520  LOAD_STR                 '%s'
              522  LOAD_FAST                'option_string'
              524  BINARY_MODULO    
              526  STORE_FAST               'part'
              528  JUMP_FORWARD        564  'to 564'
            530_0  COME_FROM           516  '516'

 L. 462       530  LOAD_FAST                'self'
              532  LOAD_METHOD              _get_default_metavar_for_optional
              534  LOAD_FAST                'action'
              536  CALL_METHOD_1         1  ''
              538  STORE_FAST               'default'

 L. 463       540  LOAD_FAST                'self'
              542  LOAD_METHOD              _format_args
              544  LOAD_FAST                'action'
              546  LOAD_FAST                'default'
              548  CALL_METHOD_2         2  ''
              550  STORE_FAST               'args_string'

 L. 464       552  LOAD_STR                 '%s %s'
              554  LOAD_FAST                'option_string'
              556  LOAD_FAST                'args_string'
              558  BUILD_TUPLE_2         2 
              560  BINARY_MODULO    
              562  STORE_FAST               'part'
            564_0  COME_FROM           528  '528'

 L. 467       564  LOAD_FAST                'action'
              566  LOAD_ATTR                required
          568_570  POP_JUMP_IF_TRUE    590  'to 590'
              572  LOAD_FAST                'action'
              574  LOAD_FAST                'group_actions'
              576  COMPARE_OP               not-in
          578_580  POP_JUMP_IF_FALSE   590  'to 590'

 L. 468       582  LOAD_STR                 '[%s]'
              584  LOAD_FAST                'part'
              586  BINARY_MODULO    
              588  STORE_FAST               'part'
            590_0  COME_FROM           578  '578'
            590_1  COME_FROM           568  '568'

 L. 471       590  LOAD_FAST                'parts'
              592  LOAD_METHOD              append
              594  LOAD_FAST                'part'
              596  CALL_METHOD_1         1  ''
              598  POP_TOP          
            600_0  COME_FROM           386  '386'
          600_602  JUMP_BACK           310  'to 310'
            604_0  COME_FROM           310  '310'

 L. 474       604  LOAD_GLOBAL              sorted
              606  LOAD_FAST                'inserts'
              608  LOAD_CONST               True
              610  LOAD_CONST               ('reverse',)
              612  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              614  GET_ITER         
            616_0  COME_FROM           638  '638'
              616  FOR_ITER            642  'to 642'
              618  STORE_FAST               'i'

 L. 475       620  LOAD_FAST                'inserts'
              622  LOAD_FAST                'i'
              624  BINARY_SUBSCR    
              626  BUILD_LIST_1          1 
              628  LOAD_FAST                'parts'
              630  LOAD_FAST                'i'
              632  LOAD_FAST                'i'
              634  BUILD_SLICE_2         2 
              636  STORE_SUBSCR     
          638_640  JUMP_BACK           616  'to 616'
            642_0  COME_FROM           616  '616'

 L. 478       642  LOAD_STR                 ' '
              644  LOAD_METHOD              join
              646  LOAD_LISTCOMP            '<code_object <listcomp>>'
              648  LOAD_STR                 'HelpFormatter._format_actions_usage.<locals>.<listcomp>'
              650  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              652  LOAD_FAST                'parts'
              654  GET_ITER         
              656  CALL_FUNCTION_1       1  ''
              658  CALL_METHOD_1         1  ''
              660  STORE_FAST               'text'

 L. 481       662  LOAD_STR                 '[\\[(]'
              664  STORE_FAST               'open'

 L. 482       666  LOAD_STR                 '[\\])]'
              668  STORE_FAST               'close'

 L. 483       670  LOAD_GLOBAL              _re
              672  LOAD_METHOD              sub
              674  LOAD_STR                 '(%s) '
              676  LOAD_FAST                'open'
              678  BINARY_MODULO    
              680  LOAD_STR                 '\\1'
              682  LOAD_FAST                'text'
              684  CALL_METHOD_3         3  ''
              686  STORE_FAST               'text'

 L. 484       688  LOAD_GLOBAL              _re
              690  LOAD_METHOD              sub
              692  LOAD_STR                 ' (%s)'
              694  LOAD_FAST                'close'
              696  BINARY_MODULO    
              698  LOAD_STR                 '\\1'
              700  LOAD_FAST                'text'
              702  CALL_METHOD_3         3  ''
              704  STORE_FAST               'text'

 L. 485       706  LOAD_GLOBAL              _re
              708  LOAD_METHOD              sub
              710  LOAD_STR                 '%s *%s'
              712  LOAD_FAST                'open'
              714  LOAD_FAST                'close'
              716  BUILD_TUPLE_2         2 
              718  BINARY_MODULO    
              720  LOAD_STR                 ''
              722  LOAD_FAST                'text'
              724  CALL_METHOD_3         3  ''
              726  STORE_FAST               'text'

 L. 486       728  LOAD_GLOBAL              _re
              730  LOAD_METHOD              sub
              732  LOAD_STR                 '\\(([^|]*)\\)'
              734  LOAD_STR                 '\\1'
              736  LOAD_FAST                'text'
              738  CALL_METHOD_3         3  ''
              740  STORE_FAST               'text'

 L. 487       742  LOAD_FAST                'text'
              744  LOAD_METHOD              strip
              746  CALL_METHOD_0         0  ''
              748  STORE_FAST               'text'

 L. 490       750  LOAD_FAST                'text'
              752  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 62

    def _format_text(self, text):
        if '%(prog)' in text:
            text = text % dict(prog=(self._prog))
        text_width = max(self._width - self._current_indent, 11)
        indent = ' ' * self._current_indent
        return self._fill_text(text, text_width, indent) + '\n\n'

    def _format_action(self, action):
        help_position = min(self._action_max_length + 2, self._max_help_position)
        help_width = max(self._width - help_position, 11)
        action_width = help_position - self._current_indent - 2
        action_header = self._format_action_invocation(action)
        if not action.help:
            tup = (
             self._current_indent, '', action_header)
            action_header = '%*s%s\n' % tup
        elif len(action_header) <= action_width:
            tup = (
             self._current_indent, '', action_width, action_header)
            action_header = '%*s%-*s  ' % tup
            indent_first = 0
        else:
            tup = (self._current_indent, '', action_header)
            action_header = '%*s%s\n' % tup
            indent_first = help_position
        parts = [
         action_header]
        if action.help:
            help_text = self._expand_help(action)
            help_lines = self._split_lines(help_text, help_width)
            parts.append('%*s%s\n' % (indent_first, '', help_lines[0]))
            for line in help_lines[1:]:
                parts.append('%*s%s\n' % (help_position, '', line))

        elif not action_header.endswith('\n'):
            parts.append('\n')
        for subaction in self._iter_indented_subactions(action):
            parts.append(self._format_action(subaction))
        else:
            return self._join_parts(parts)

    def _format_action_invocation(self, action):
        if not action.option_strings:
            default = self._get_default_metavar_for_positional(action)
            metavar, = self._metavar_formatter(action, default)(1)
            return metavar
        parts = []
        if action.nargs == 0:
            parts.extend(action.option_strings)
        else:
            default = self._get_default_metavar_for_optional(action)
            args_string = self._format_args(action, default)
        for option_string in action.option_strings:
            parts.append('%s %s' % (option_string, args_string))
        else:
            return ', '.join(parts)

    def _metavar_formatter(self, action, default_metavar):
        if action.metavar is not None:
            result = action.metavar
        elif action.choices is not None:
            choice_strs = [str(choice) for choice in action.choices]
            result = '{%s}' % ','.join(choice_strs)
        else:
            result = default_metavar

        def format(tuple_size):
            if isinstance(result, tuple):
                return result
            return (
             result,) * tuple_size

        return format

    def _format_args(self, action, default_metavar):
        get_metavar = self._metavar_formatter(action, default_metavar)
        if action.nargs is None:
            result = '%s' % get_metavar(1)
        else:
            pass
        if action.nargs == OPTIONAL:
            result = '[%s]' % get_metavar(1)
        elif action.nargs == ZERO_OR_MORE:
            result = '[%s [%s ...]]' % get_metavar(2)
        elif action.nargs == ONE_OR_MORE:
            result = '%s [%s ...]' % get_metavar(2)
        elif action.nargs == REMAINDER:
            result = '...'
        elif action.nargs == PARSER:
            result = '%s ...' % get_metavar(1)
        elif action.nargs == SUPPRESS:
            result = ''
        else:
            try:
                formats = ['%s' for _ in range(action.nargs)]
            except TypeError:
                raise ValueError('invalid nargs value') from None
            else:
                result = ' '.join(formats) % get_metavar(action.nargs)
        return result

    def _expand_help(self, action):
        params = dict((vars(action)), prog=(self._prog))
        for name in list(params):
            if params[name] is SUPPRESS:
                del params[name]
        else:
            for name in list(params):
                if hasattr(params[name], '__name__'):
                    params[name] = params[name].__name__
            else:
                if params.get('choices') is not None:
                    choices_str = ', '.join([str(c) for c in params['choices']])
                    params['choices'] = choices_str
                return self._get_help_string(action) % params

    def _iter_indented_subactions(self, action):
        try:
            get_subactions = action._get_subactions
        except AttributeError:
            pass
        else:
            self._indent()
            yield from get_subactions
            self._dedent()
        if False:
            yield None

    def _split_lines(self, text, width):
        text = self._whitespace_matcher.sub(' ', text).strip()
        import textwrap
        return textwrap.wrap(text, width)

    def _fill_text(self, text, width, indent):
        text = self._whitespace_matcher.sub(' ', text).strip()
        import textwrap
        return textwrap.fill(text, width, initial_indent=indent,
          subsequent_indent=indent)

    def _get_help_string(self, action):
        return action.help

    def _get_default_metavar_for_optional(self, action):
        return action.dest.upper()

    def _get_default_metavar_for_positional(self, action):
        return action.dest


class RawDescriptionHelpFormatter(HelpFormatter):
    __doc__ = 'Help message formatter which retains any formatting in descriptions.\n\n    Only the name of this class is considered a public API. All the methods\n    provided by the class are considered an implementation detail.\n    '

    def _fill_text(self, text, width, indent):
        return ''.join((indent + line for line in text.splitlines(keepends=True)))


class RawTextHelpFormatter(RawDescriptionHelpFormatter):
    __doc__ = 'Help message formatter which retains formatting of all help text.\n\n    Only the name of this class is considered a public API. All the methods\n    provided by the class are considered an implementation detail.\n    '

    def _split_lines(self, text, width):
        return text.splitlines()


class ArgumentDefaultsHelpFormatter(HelpFormatter):
    __doc__ = 'Help message formatter which adds default values to argument help.\n\n    Only the name of this class is considered a public API. All the methods\n    provided by the class are considered an implementation detail.\n    '

    def _get_help_string(self, action):
        help = action.help
        if not '%(default)' not in action.help or action.default is not SUPPRESS:
            defaulting_nargs = [
             OPTIONAL, ZERO_OR_MORE]
            if action.option_strings or (action.nargs in defaulting_nargs):
                help += ' (default: %(default)s)'
            return help


class MetavarTypeHelpFormatter(HelpFormatter):
    __doc__ = "Help message formatter which uses the argument 'type' as the default\n    metavar value (instead of the argument 'dest')\n\n    Only the name of this class is considered a public API. All the methods\n    provided by the class are considered an implementation detail.\n    "

    def _get_default_metavar_for_optional(self, action):
        return action.type.__name__

    def _get_default_metavar_for_positional(self, action):
        return action.type.__name__


def _get_action_name(argument):
    if argument is None:
        return
    if argument.option_strings:
        return '/'.join(argument.option_strings)
    if argument.metavar not in (None, SUPPRESS):
        return argument.metavar
    if argument.dest not in (None, SUPPRESS):
        return argument.dest
    return


class ArgumentError(Exception):
    __doc__ = 'An error from creating or using an argument (optional or positional).\n\n    The string value of this exception is the message, augmented with\n    information about the argument that caused it.\n    '

    def __init__(self, argument, message):
        self.argument_name = _get_action_name(argument)
        self.message = message

    def __str__(self):
        if self.argument_name is None:
            format = '%(message)s'
        else:
            format = 'argument %(argument_name)s: %(message)s'
        return format % dict(message=(self.message), argument_name=(self.argument_name))


class ArgumentTypeError(Exception):
    __doc__ = 'An error from trying to convert a command line string to a type.'


class Action(_AttributeHolder):
    __doc__ = "Information about how to convert command line strings to Python objects.\n\n    Action objects are used by an ArgumentParser to represent the information\n    needed to parse a single argument from one or more strings from the\n    command line. The keyword arguments to the Action constructor are also\n    all attributes of Action instances.\n\n    Keyword Arguments:\n\n        - option_strings -- A list of command-line option strings which\n            should be associated with this action.\n\n        - dest -- The name of the attribute to hold the created object(s)\n\n        - nargs -- The number of command-line arguments that should be\n            consumed. By default, one argument will be consumed and a single\n            value will be produced.  Other values include:\n                - N (an integer) consumes N arguments (and produces a list)\n                - '?' consumes zero or one arguments\n                - '*' consumes zero or more arguments (and produces a list)\n                - '+' consumes one or more arguments (and produces a list)\n            Note that the difference between the default and nargs=1 is that\n            with the default, a single value will be produced, while with\n            nargs=1, a list containing a single value will be produced.\n\n        - const -- The value to be produced if the option is specified and the\n            option uses an action that takes no values.\n\n        - default -- The value to be produced if the option is not specified.\n\n        - type -- A callable that accepts a single string argument, and\n            returns the converted value.  The standard Python types str, int,\n            float, and complex are useful examples of such callables.  If None,\n            str is used.\n\n        - choices -- A container of values that should be allowed. If not None,\n            after a command-line argument has been converted to the appropriate\n            type, an exception will be raised if it is not a member of this\n            collection.\n\n        - required -- True if the action must always be specified at the\n            command line. This is only meaningful for optional command-line\n            arguments.\n\n        - help -- The help string describing the argument.\n\n        - metavar -- The name to be used for the option's argument with the\n            help string. If None, the 'dest' value will be used as the name.\n    "

    def __init__(self, option_strings, dest, nargs=None, const=None, default=None, type=None, choices=None, required=False, help=None, metavar=None):
        self.option_strings = option_strings
        self.dest = dest
        self.nargs = nargs
        self.const = const
        self.default = default
        self.type = type
        self.choices = choices
        self.required = required
        self.help = help
        self.metavar = metavar

    def _get_kwargs(self):
        names = [
         'option_strings',
         'dest',
         'nargs',
         'const',
         'default',
         'type',
         'choices',
         'help',
         'metavar']
        return [(
         name, getattr(self, name)) for name in names]

    def __call__(self, parser, namespace, values, option_string=None):
        raise NotImplementedError(_('.__call__() not defined'))


class _StoreAction(Action):

    def __init__(self, option_strings, dest, nargs=None, const=None, default=None, type=None, choices=None, required=False, help=None, metavar=None):
        if nargs == 0:
            raise ValueError('nargs for store actions must be != 0; if you have nothing to store, actions such as store true or store const may be more appropriate')
        if const is not None:
            if nargs != OPTIONAL:
                raise ValueError('nargs must be %r to supply const' % OPTIONAL)
        super(_StoreAction, self).__init__(option_strings=option_strings,
          dest=dest,
          nargs=nargs,
          const=const,
          default=default,
          type=type,
          choices=choices,
          required=required,
          help=help,
          metavar=metavar)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


class _StoreConstAction(Action):

    def __init__(self, option_strings, dest, const, default=None, required=False, help=None, metavar=None):
        super(_StoreConstAction, self).__init__(option_strings=option_strings,
          dest=dest,
          nargs=0,
          const=const,
          default=default,
          required=required,
          help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, self.const)


class _StoreTrueAction(_StoreConstAction):

    def __init__(self, option_strings, dest, default=False, required=False, help=None):
        super(_StoreTrueAction, self).__init__(option_strings=option_strings,
          dest=dest,
          const=True,
          default=default,
          required=required,
          help=help)


class _StoreFalseAction(_StoreConstAction):

    def __init__(self, option_strings, dest, default=True, required=False, help=None):
        super(_StoreFalseAction, self).__init__(option_strings=option_strings,
          dest=dest,
          const=False,
          default=default,
          required=required,
          help=help)


class _AppendAction(Action):

    def __init__(self, option_strings, dest, nargs=None, const=None, default=None, type=None, choices=None, required=False, help=None, metavar=None):
        if nargs == 0:
            raise ValueError('nargs for append actions must be != 0; if arg strings are not supplying the value to append, the append const action may be more appropriate')
        if const is not None:
            if nargs != OPTIONAL:
                raise ValueError('nargs must be %r to supply const' % OPTIONAL)
        super(_AppendAction, self).__init__(option_strings=option_strings,
          dest=dest,
          nargs=nargs,
          const=const,
          default=default,
          type=type,
          choices=choices,
          required=required,
          help=help,
          metavar=metavar)

    def __call__(self, parser, namespace, values, option_string=None):
        items = getattr(namespace, self.dest, None)
        items = _copy_items(items)
        items.append(values)
        setattr(namespace, self.dest, items)


class _AppendConstAction(Action):

    def __init__(self, option_strings, dest, const, default=None, required=False, help=None, metavar=None):
        super(_AppendConstAction, self).__init__(option_strings=option_strings,
          dest=dest,
          nargs=0,
          const=const,
          default=default,
          required=required,
          help=help,
          metavar=metavar)

    def __call__(self, parser, namespace, values, option_string=None):
        items = getattr(namespace, self.dest, None)
        items = _copy_items(items)
        items.append(self.const)
        setattr(namespace, self.dest, items)


class _CountAction(Action):

    def __init__(self, option_strings, dest, default=None, required=False, help=None):
        super(_CountAction, self).__init__(option_strings=option_strings,
          dest=dest,
          nargs=0,
          default=default,
          required=required,
          help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        count = getattr(namespace, self.dest, None)
        if count is None:
            count = 0
        setattr(namespace, self.dest, count + 1)


class _HelpAction(Action):

    def __init__(self, option_strings, dest=SUPPRESS, default=SUPPRESS, help=None):
        super(_HelpAction, self).__init__(option_strings=option_strings,
          dest=dest,
          default=default,
          nargs=0,
          help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        parser.print_help()
        parser.exit()


class _VersionAction(Action):

    def __init__(self, option_strings, version=None, dest=SUPPRESS, default=SUPPRESS, help="show program's version number and exit"):
        super(_VersionAction, self).__init__(option_strings=option_strings,
          dest=dest,
          default=default,
          nargs=0,
          help=help)
        self.version = version

    def __call__(self, parser, namespace, values, option_string=None):
        version = self.version
        if version is None:
            version = parser.version
        formatter = parser._get_formatter()
        formatter.add_text(version)
        parser._print_message(formatter.format_help(), _sys.stdout)
        parser.exit()


class _SubParsersAction(Action):

    class _ChoicesPseudoAction(Action):

        def __init__(self, name, aliases, help):
            metavar = dest = name
            if aliases:
                metavar += ' (%s)' % ', '.join(aliases)
            sup = super(_SubParsersAction._ChoicesPseudoAction, self)
            sup.__init__(option_strings=[], dest=dest, help=help, metavar=metavar)

    def __init__(self, option_strings, prog, parser_class, dest=SUPPRESS, required=False, help=None, metavar=None):
        self._prog_prefix = prog
        self._parser_class = parser_class
        self._name_parser_map = {}
        self._choices_actions = []
        super(_SubParsersAction, self).__init__(option_strings=option_strings,
          dest=dest,
          nargs=PARSER,
          choices=(self._name_parser_map),
          required=required,
          help=help,
          metavar=metavar)

    def add_parser(self, name, **kwargs):
        if kwargs.get('prog') is None:
            kwargs['prog'] = '%s %s' % (self._prog_prefix, name)
        aliases = kwargs.pop('aliases', ())
        if 'help' in kwargs:
            help = kwargs.pop('help')
            choice_action = self._ChoicesPseudoAction(name, aliases, help)
            self._choices_actions.append(choice_action)
        parser = (self._parser_class)(**kwargs)
        self._name_parser_map[name] = parser
        for alias in aliases:
            self._name_parser_map[alias] = parser
        else:
            return parser

    def _get_subactions(self):
        return self._choices_actions

    def __call__(self, parser, namespace, values, option_string=None):
        parser_name = values[0]
        arg_strings = values[1:]
        if self.dest is not SUPPRESS:
            setattr(namespace, self.dest, parser_name)
        try:
            parser = self._name_parser_map[parser_name]
        except KeyError:
            args = {'parser_name':parser_name, 
             'choices':', '.join(self._name_parser_map)}
            msg = _('unknown parser %(parser_name)r (choices: %(choices)s)') % args
            raise ArgumentError(self, msg)
        else:
            subnamespace, arg_strings = parser.parse_known_args(arg_strings, None)
        for key, value in vars(subnamespace).items():
            setattr(namespace, key, value)
        else:
            if arg_strings:
                vars(namespace).setdefault(_UNRECOGNIZED_ARGS_ATTR, [])
                getattr(namespace, _UNRECOGNIZED_ARGS_ATTR).extend(arg_strings)


class _ExtendAction(_AppendAction):

    def __call__(self, parser, namespace, values, option_string=None):
        items = getattr(namespace, self.dest, None)
        items = _copy_items(items)
        items.extend(values)
        setattr(namespace, self.dest, items)


class FileType(object):
    __doc__ = "Factory for creating file object types\n\n    Instances of FileType are typically passed as type= arguments to the\n    ArgumentParser add_argument() method.\n\n    Keyword Arguments:\n        - mode -- A string indicating how the file is to be opened. Accepts the\n            same values as the builtin open() function.\n        - bufsize -- The file's desired buffer size. Accepts the same values as\n            the builtin open() function.\n        - encoding -- The file's encoding. Accepts the same values as the\n            builtin open() function.\n        - errors -- A string indicating how encoding and decoding errors are to\n            be handled. Accepts the same value as the builtin open() function.\n    "

    def __init__(self, mode='r', bufsize=-1, encoding=None, errors=None):
        self._mode = mode
        self._bufsize = bufsize
        self._encoding = encoding
        self._errors = errors

    def __call__(self, string):
        if string == '-':
            if 'r' in self._mode:
                return _sys.stdin
            if 'w' in self._mode:
                return _sys.stdout
            msg = _('argument "-" with mode %r') % self._mode
            raise ValueError(msg)
        try:
            return open(string, self._mode, self._bufsize, self._encoding, self._errors)
            except OSError as e:
            try:
                args = {'filename':string, 
                 'error':e}
                message = _("can't open '%(filename)s': %(error)s")
                raise ArgumentTypeError(message % args)
            finally:
                e = None
                del e

    def __repr__(self):
        args = (
         self._mode, self._bufsize)
        kwargs = [('encoding', self._encoding), ('errors', self._errors)]
        args_str = ', '.join([repr(arg) for arg in args if arg != -1] + ['%s=%r' % (kw, arg) for kw, arg in kwargs if arg is not None])
        return '%s(%s)' % (type(self).__name__, args_str)


class Namespace(_AttributeHolder):
    __doc__ = 'Simple object for storing attributes.\n\n    Implements equality by attribute names and values, and provides a simple\n    string representation.\n    '

    def __init__(self, **kwargs):
        for name in kwargs:
            setattr(self, name, kwargs[name])

    def __eq__(self, other):
        if not isinstance(other, Namespace):
            return NotImplemented
        return vars(self) == vars(other)

    def __contains__(self, key):
        return key in self.__dict__


class _ActionsContainer(object):

    def __init__(self, description, prefix_chars, argument_default, conflict_handler):
        super(_ActionsContainer, self).__init__()
        self.description = description
        self.argument_default = argument_default
        self.prefix_chars = prefix_chars
        self.conflict_handler = conflict_handler
        self._registries = {}
        self.register('action', None, _StoreAction)
        self.register('action', 'store', _StoreAction)
        self.register('action', 'store_const', _StoreConstAction)
        self.register('action', 'store_true', _StoreTrueAction)
        self.register('action', 'store_false', _StoreFalseAction)
        self.register('action', 'append', _AppendAction)
        self.register('action', 'append_const', _AppendConstAction)
        self.register('action', 'count', _CountAction)
        self.register('action', 'help', _HelpAction)
        self.register('action', 'version', _VersionAction)
        self.register('action', 'parsers', _SubParsersAction)
        self.register('action', 'extend', _ExtendAction)
        self._get_handler()
        self._actions = []
        self._option_string_actions = {}
        self._action_groups = []
        self._mutually_exclusive_groups = []
        self._defaults = {}
        self._negative_number_matcher = _re.compile('^-\\d+$|^-\\d*\\.\\d+$')
        self._has_negative_number_optionals = []

    def register(self, registry_name, value, object):
        registry = self._registries.setdefault(registry_name, {})
        registry[value] = object

    def _registry_get(self, registry_name, value, default=None):
        return self._registries[registry_name].get(value, default)

    def set_defaults(self, **kwargs):
        self._defaults.update(kwargs)
        for action in self._actions:
            if action.dest in kwargs:
                action.default = kwargs[action.dest]

    def get_default(self, dest):
        for action in self._actions:
            if action.dest == dest:
                if action.default is not None:
                    return action.default
        else:
            return self._defaults.get(dest, None)

    def add_argument(self, *args, **kwargs):
        """
        add_argument(dest, ..., name=value, ...)
        add_argument(option_string, option_string, ..., name=value, ...)
        """
        chars = self.prefix_chars
        if args:
            if not len(args) == 1 or args[0][0] not in chars:
                if args:
                    if 'dest' in kwargs:
                        raise ValueError('dest supplied twice for positional argument')
                kwargs = (self._get_positional_kwargs)(*args, **kwargs)
            else:
                kwargs = (self._get_optional_kwargs)(*args, **kwargs)
            if 'default' not in kwargs:
                dest = kwargs['dest']
                if dest in self._defaults:
                    kwargs['default'] = self._defaults[dest]
                elif self.argument_default is not None:
                    kwargs['default'] = self.argument_default
            action_class = self._pop_action_class(kwargs)
            if not callable(action_class):
                raise ValueError('unknown action "%s"' % (action_class,))
            action = action_class(**kwargs)
            type_func = self._registry_get('type', action.type, action.type)
            if not callable(type_func):
                raise ValueError('%r is not callable' % (type_func,))
            if type_func is FileType:
                raise ValueError('%r is a FileType class object, instance of it must be passed' % (
                 type_func,))
        if hasattr(self, '_get_formatter'):
            try:
                self._get_formatter()._format_args(action, None)
            except TypeError:
                raise ValueError('length of metavar tuple does not match nargs')

            return self._add_action(action)

    def add_argument_group(self, *args, **kwargs):
        group = _ArgumentGroup(self, *args, **kwargs)
        self._action_groups.append(group)
        return group

    def add_mutually_exclusive_group(self, **kwargs):
        group = _MutuallyExclusiveGroup(self, **kwargs)
        self._mutually_exclusive_groups.append(group)
        return group

    def _add_action(self, action):
        self._check_conflict(action)
        self._actions.append(action)
        action.container = self
        for option_string in action.option_strings:
            self._option_string_actions[option_string] = action
        else:
            for option_string in action.option_strings:
                if self._negative_number_matcher.match(option_string):
                    if not self._has_negative_number_optionals:
                        self._has_negative_number_optionals.append(True)
            else:
                return action

    def _remove_action(self, action):
        self._actions.remove(action)

    def _add_container_actions(self, container):
        title_group_map = {}
        for group in self._action_groups:
            if group.title in title_group_map:
                msg = _('cannot merge actions - two groups are named %r')
                raise ValueError(msg % group.title)
            else:
                title_group_map[group.title] = group
        else:
            group_map = {}
            for group in container._action_groups:
                if group.title not in title_group_map:
                    title_group_map[group.title] = self.add_argument_group(title=(group.title),
                      description=(group.description),
                      conflict_handler=(group.conflict_handler))
                else:
                    for action in group._group_actions:
                        group_map[action] = title_group_map[group.title]

            else:
                for group in container._mutually_exclusive_groups:
                    mutex_group = self.add_mutually_exclusive_group(required=(group.required))
                    for action in group._group_actions:
                        group_map[action] = mutex_group

                else:
                    for action in container._actions:
                        group_map.get(action, self)._add_action(action)

    def _get_positional_kwargs(self, dest, **kwargs):
        if 'required' in kwargs:
            msg = _("'required' is an invalid argument for positionals")
            raise TypeError(msg)
        if kwargs.get('nargs') not in (OPTIONAL, ZERO_OR_MORE):
            kwargs['required'] = True
        if kwargs.get('nargs') == ZERO_OR_MORE:
            if 'default' not in kwargs:
                kwargs['required'] = True
        return dict(kwargs, dest=dest, option_strings=[])

    def _get_optional_kwargs(self, *args, **kwargs):
        option_strings = []
        long_option_strings = []
        for option_string in args:
            if option_string[0] not in self.prefix_chars:
                args = {'option':option_string, 
                 'prefix_chars':self.prefix_chars}
                msg = _('invalid option string %(option)r: must start with a character %(prefix_chars)r')
                raise ValueError(msg % args)
            else:
                option_strings.append(option_string)
            if option_string[0] in self.prefix_chars:
                if len(option_string) > 1:
                    if option_string[1] in self.prefix_chars:
                        long_option_strings.append(option_string)
        else:
            dest = kwargs.pop('dest', None)
            if dest is None:
                if long_option_strings:
                    dest_option_string = long_option_strings[0]
                else:
                    dest_option_string = option_strings[0]
                dest = dest_option_string.lstrip(self.prefix_chars)
                if not dest:
                    msg = _('dest= is required for options like %r')
                    raise ValueError(msg % option_string)
                dest = dest.replace('-', '_')
            return dict(kwargs, dest=dest, option_strings=option_strings)

    def _pop_action_class(self, kwargs, default=None):
        action = kwargs.pop('action', default)
        return self._registry_get('action', action, action)

    def _get_handler(self):
        handler_func_name = '_handle_conflict_%s' % self.conflict_handler
        try:
            return getattr(self, handler_func_name)
        except AttributeError:
            msg = _('invalid conflict_resolution value: %r')
            raise ValueError(msg % self.conflict_handler)

    def _check_conflict(self, action):
        confl_optionals = []
        for option_string in action.option_strings:
            if option_string in self._option_string_actions:
                confl_optional = self._option_string_actions[option_string]
                confl_optionals.append((option_string, confl_optional))
        else:
            if confl_optionals:
                conflict_handler = self._get_handler()
                conflict_handler(action, confl_optionals)

    def _handle_conflict_error(self, action, conflicting_actions):
        message = ngettext('conflicting option string: %s', 'conflicting option strings: %s', len(conflicting_actions))
        conflict_string = ', '.join([option_string for option_string, action in conflicting_actions])
        raise ArgumentError(action, message % conflict_string)

    def _handle_conflict_resolve(self, action, conflicting_actions):
        for option_string, action in conflicting_actions:
            action.option_strings.remove(option_string)
            self._option_string_actions.pop(option_string, None)
            if not action.option_strings:
                action.container._remove_action(action)


class _ArgumentGroup(_ActionsContainer):

    def __init__(self, container, title=None, description=None, **kwargs):
        update = kwargs.setdefault
        update('conflict_handler', container.conflict_handler)
        update('prefix_chars', container.prefix_chars)
        update('argument_default', container.argument_default)
        super_init = super(_ArgumentGroup, self).__init__
        super_init(description=description, **kwargs)
        self.title = title
        self._group_actions = []
        self._registries = container._registries
        self._actions = container._actions
        self._option_string_actions = container._option_string_actions
        self._defaults = container._defaults
        self._has_negative_number_optionals = container._has_negative_number_optionals
        self._mutually_exclusive_groups = container._mutually_exclusive_groups

    def _add_action(self, action):
        action = super(_ArgumentGroup, self)._add_action(action)
        self._group_actions.append(action)
        return action

    def _remove_action(self, action):
        super(_ArgumentGroup, self)._remove_action(action)
        self._group_actions.remove(action)


class _MutuallyExclusiveGroup(_ArgumentGroup):

    def __init__(self, container, required=False):
        super(_MutuallyExclusiveGroup, self).__init__(container)
        self.required = required
        self._container = container

    def _add_action(self, action):
        if action.required:
            msg = _('mutually exclusive arguments must be optional')
            raise ValueError(msg)
        action = self._container._add_action(action)
        self._group_actions.append(action)
        return action

    def _remove_action(self, action):
        self._container._remove_action(action)
        self._group_actions.remove(action)


class ArgumentParser(_AttributeHolder, _ActionsContainer):
    __doc__ = 'Object for parsing command line strings into Python objects.\n\n    Keyword Arguments:\n        - prog -- The name of the program (default: sys.argv[0])\n        - usage -- A usage message (default: auto-generated from arguments)\n        - description -- A description of what the program does\n        - epilog -- Text following the argument descriptions\n        - parents -- Parsers whose arguments should be copied into this one\n        - formatter_class -- HelpFormatter class for printing help messages\n        - prefix_chars -- Characters that prefix optional arguments\n        - fromfile_prefix_chars -- Characters that prefix files containing\n            additional arguments\n        - argument_default -- The default value for all arguments\n        - conflict_handler -- String indicating how to handle conflicts\n        - add_help -- Add a -h/-help option\n        - allow_abbrev -- Allow long options to be abbreviated unambiguously\n    '

    def __init__(self, prog=None, usage=None, description=None, epilog=None, parents=[], formatter_class=HelpFormatter, prefix_chars='-', fromfile_prefix_chars=None, argument_default=None, conflict_handler='error', add_help=True, allow_abbrev=True):
        superinit = super(ArgumentParser, self).__init__
        superinit(description=description, prefix_chars=prefix_chars,
          argument_default=argument_default,
          conflict_handler=conflict_handler)
        if prog is None:
            prog = _os.path.basename(_sys.argv[0])
        self.prog = prog
        self.usage = usage
        self.epilog = epilog
        self.formatter_class = formatter_class
        self.fromfile_prefix_chars = fromfile_prefix_chars
        self.add_help = add_help
        self.allow_abbrev = allow_abbrev
        add_group = self.add_argument_group
        self._positionals = add_group(_('positional arguments'))
        self._optionals = add_group(_('optional arguments'))
        self._subparsers = None

        def identity(string):
            return string

        self.register('type', None, identity)
        default_prefix = '-' if '-' in prefix_chars else prefix_chars[0]
        if self.add_help:
            self.add_argument((default_prefix + 'h'),
              (default_prefix * 2 + 'help'), action='help',
              default=SUPPRESS,
              help=(_('show this help message and exit')))
        for parent in parents:
            self._add_container_actions(parent)
            try:
                defaults = parent._defaults
            except AttributeError:
                pass
            else:
                self._defaults.update(defaults)

    def _get_kwargs(self):
        names = [
         'prog',
         'usage',
         'description',
         'formatter_class',
         'conflict_handler',
         'add_help']
        return [(
         name, getattr(self, name)) for name in names]

    def add_subparsers(self, **kwargs):
        if self._subparsers is not None:
            self.error(_('cannot have multiple subparser arguments'))
        kwargs.setdefault('parser_class', type(self))
        if 'title' in kwargs or 'description' in kwargs:
            title = _(kwargs.pop('title', 'subcommands'))
            description = _(kwargs.pop('description', None))
            self._subparsers = self.add_argument_group(title, description)
        else:
            self._subparsers = self._positionals
        if kwargs.get('prog') is None:
            formatter = self._get_formatter()
            positionals = self._get_positional_actions()
            groups = self._mutually_exclusive_groups
            formatter.add_usage(self.usage, positionals, groups, '')
            kwargs['prog'] = formatter.format_help().strip()
        parsers_class = self._pop_action_class(kwargs, 'parsers')
        action = parsers_class(option_strings=[], **kwargs)
        self._subparsers._add_action(action)
        return action

    def _add_action(self, action):
        if action.option_strings:
            self._optionals._add_action(action)
        else:
            self._positionals._add_action(action)
        return action

    def _get_optional_actions(self):
        return [action for action in self._actions if action.option_strings]

    def _get_positional_actions(self):
        return [action for action in self._actions if not action.option_strings]

    def parse_args(self, args=None, namespace=None):
        args, argv = self.parse_known_args(args, namespace)
        if argv:
            msg = _('unrecognized arguments: %s')
            self.error(msg % ' '.join(argv))
        return args

    def parse_known_args(self, args=None, namespace=None):
        if args is None:
            args = _sys.argv[1:]
        else:
            args = list(args)
        if namespace is None:
            namespace = Namespace
        for action in self._actions:
            if action.dest is not SUPPRESS:
                if not hasattr(namespace, action.dest):
                    if action.default is not SUPPRESS:
                        setattr(namespace, action.dest, action.default)
        else:
            for dest in self._defaults:
                if not hasattr(namespace, dest):
                    setattr(namespace, dest, self._defaults[dest])
            else:
                try:
                    namespace, args = self._parse_known_args(args, namespace)
                    if hasattr(namespace, _UNRECOGNIZED_ARGS_ATTR):
                        args.extend(getattr(namespace, _UNRECOGNIZED_ARGS_ATTR))
                        delattr(namespace, _UNRECOGNIZED_ARGS_ATTR)
                    return (
                     namespace, args)
                except ArgumentError:
                    err = _sys.exc_info()[1]
                    self.error(str(err))

    def _parse_known_args--- This code section failed: ---

 L.1811         0  LOAD_DEREF               'self'
                2  LOAD_ATTR                fromfile_prefix_chars
                4  LOAD_CONST               None
                6  COMPARE_OP               is-not
                8  POP_JUMP_IF_FALSE    20  'to 20'

 L.1812        10  LOAD_DEREF               'self'
               12  LOAD_METHOD              _read_args_from_files
               14  LOAD_DEREF               'arg_strings'
               16  CALL_METHOD_1         1  ''
               18  STORE_DEREF              'arg_strings'
             20_0  COME_FROM             8  '8'

 L.1816        20  BUILD_MAP_0           0 
               22  STORE_DEREF              'action_conflicts'

 L.1817        24  LOAD_DEREF               'self'
               26  LOAD_ATTR                _mutually_exclusive_groups
               28  GET_ITER         
             30_0  COME_FROM           112  '112'
               30  FOR_ITER            114  'to 114'
               32  STORE_FAST               'mutex_group'

 L.1818        34  LOAD_FAST                'mutex_group'
               36  LOAD_ATTR                _group_actions
               38  STORE_FAST               'group_actions'

 L.1819        40  LOAD_GLOBAL              enumerate
               42  LOAD_FAST                'mutex_group'
               44  LOAD_ATTR                _group_actions
               46  CALL_FUNCTION_1       1  ''
               48  GET_ITER         
             50_0  COME_FROM           110  '110'
               50  FOR_ITER            112  'to 112'
               52  UNPACK_SEQUENCE_2     2 
               54  STORE_FAST               'i'
               56  STORE_FAST               'mutex_action'

 L.1820        58  LOAD_DEREF               'action_conflicts'
               60  LOAD_METHOD              setdefault
               62  LOAD_FAST                'mutex_action'
               64  BUILD_LIST_0          0 
               66  CALL_METHOD_2         2  ''
               68  STORE_FAST               'conflicts'

 L.1821        70  LOAD_FAST                'conflicts'
               72  LOAD_METHOD              extend
               74  LOAD_FAST                'group_actions'
               76  LOAD_CONST               None
               78  LOAD_FAST                'i'
               80  BUILD_SLICE_2         2 
               82  BINARY_SUBSCR    
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          

 L.1822        88  LOAD_FAST                'conflicts'
               90  LOAD_METHOD              extend
               92  LOAD_FAST                'group_actions'
               94  LOAD_FAST                'i'
               96  LOAD_CONST               1
               98  BINARY_ADD       
              100  LOAD_CONST               None
              102  BUILD_SLICE_2         2 
              104  BINARY_SUBSCR    
              106  CALL_METHOD_1         1  ''
              108  POP_TOP          
              110  JUMP_BACK            50  'to 50'
            112_0  COME_FROM            50  '50'
              112  JUMP_BACK            30  'to 30'
            114_0  COME_FROM            30  '30'

 L.1827       114  BUILD_MAP_0           0 
              116  STORE_DEREF              'option_string_indices'

 L.1828       118  BUILD_LIST_0          0 
              120  STORE_FAST               'arg_string_pattern_parts'

 L.1829       122  LOAD_GLOBAL              iter
              124  LOAD_DEREF               'arg_strings'
              126  CALL_FUNCTION_1       1  ''
              128  STORE_FAST               'arg_strings_iter'

 L.1830       130  LOAD_GLOBAL              enumerate
              132  LOAD_FAST                'arg_strings_iter'
              134  CALL_FUNCTION_1       1  ''
              136  GET_ITER         
            138_0  COME_FROM           232  '232'
            138_1  COME_FROM           184  '184'
              138  FOR_ITER            234  'to 234'
              140  UNPACK_SEQUENCE_2     2 
              142  STORE_FAST               'i'
              144  STORE_FAST               'arg_string'

 L.1833       146  LOAD_FAST                'arg_string'
              148  LOAD_STR                 '--'
              150  COMPARE_OP               ==
              152  POP_JUMP_IF_FALSE   186  'to 186'

 L.1834       154  LOAD_FAST                'arg_string_pattern_parts'
              156  LOAD_METHOD              append
              158  LOAD_STR                 '-'
              160  CALL_METHOD_1         1  ''
              162  POP_TOP          

 L.1835       164  LOAD_FAST                'arg_strings_iter'
              166  GET_ITER         
            168_0  COME_FROM           182  '182'
              168  FOR_ITER            184  'to 184'
              170  STORE_FAST               'arg_string'

 L.1836       172  LOAD_FAST                'arg_string_pattern_parts'
              174  LOAD_METHOD              append
              176  LOAD_STR                 'A'
              178  CALL_METHOD_1         1  ''
              180  POP_TOP          
              182  JUMP_BACK           168  'to 168'
            184_0  COME_FROM           168  '168'
              184  JUMP_BACK           138  'to 138'
            186_0  COME_FROM           152  '152'

 L.1841       186  LOAD_DEREF               'self'
              188  LOAD_METHOD              _parse_optional
              190  LOAD_FAST                'arg_string'
              192  CALL_METHOD_1         1  ''
              194  STORE_FAST               'option_tuple'

 L.1842       196  LOAD_FAST                'option_tuple'
              198  LOAD_CONST               None
              200  COMPARE_OP               is
              202  POP_JUMP_IF_FALSE   210  'to 210'

 L.1843       204  LOAD_STR                 'A'
              206  STORE_FAST               'pattern'
              208  JUMP_FORWARD        222  'to 222'
            210_0  COME_FROM           202  '202'

 L.1845       210  LOAD_FAST                'option_tuple'
              212  LOAD_DEREF               'option_string_indices'
              214  LOAD_FAST                'i'
              216  STORE_SUBSCR     

 L.1846       218  LOAD_STR                 'O'
              220  STORE_FAST               'pattern'
            222_0  COME_FROM           208  '208'

 L.1847       222  LOAD_FAST                'arg_string_pattern_parts'
              224  LOAD_METHOD              append
              226  LOAD_FAST                'pattern'
              228  CALL_METHOD_1         1  ''
              230  POP_TOP          
              232  JUMP_BACK           138  'to 138'
            234_0  COME_FROM           138  '138'

 L.1850       234  LOAD_STR                 ''
              236  LOAD_METHOD              join
              238  LOAD_FAST                'arg_string_pattern_parts'
              240  CALL_METHOD_1         1  ''
              242  STORE_DEREF              'arg_strings_pattern'

 L.1853       244  LOAD_GLOBAL              set
              246  CALL_FUNCTION_0       0  ''
              248  STORE_DEREF              'seen_actions'

 L.1854       250  LOAD_GLOBAL              set
              252  CALL_FUNCTION_0       0  ''
              254  STORE_DEREF              'seen_non_default_actions'

 L.1856       256  LOAD_CONST               (None,)
              258  LOAD_CLOSURE             'action_conflicts'
              260  LOAD_CLOSURE             'namespace'
              262  LOAD_CLOSURE             'seen_actions'
              264  LOAD_CLOSURE             'seen_non_default_actions'
              266  LOAD_CLOSURE             'self'
              268  BUILD_TUPLE_5         5 
              270  LOAD_CODE                <code_object take_action>
              272  LOAD_STR                 'ArgumentParser._parse_known_args.<locals>.take_action'
              274  MAKE_FUNCTION_9          'default, closure'
              276  STORE_DEREF              'take_action'

 L.1877       278  LOAD_CLOSURE             'arg_strings'
              280  LOAD_CLOSURE             'arg_strings_pattern'
              282  LOAD_CLOSURE             'extras'
              284  LOAD_CLOSURE             'option_string_indices'
              286  LOAD_CLOSURE             'self'
              288  LOAD_CLOSURE             'take_action'
              290  BUILD_TUPLE_6         6 
              292  LOAD_CODE                <code_object consume_optional>
              294  LOAD_STR                 'ArgumentParser._parse_known_args.<locals>.consume_optional'
              296  MAKE_FUNCTION_8          'closure'
              298  STORE_FAST               'consume_optional'

 L.1951       300  LOAD_DEREF               'self'
              302  LOAD_METHOD              _get_positional_actions
              304  CALL_METHOD_0         0  ''
              306  STORE_DEREF              'positionals'

 L.1954       308  LOAD_CLOSURE             'arg_strings'
              310  LOAD_CLOSURE             'arg_strings_pattern'
              312  LOAD_CLOSURE             'positionals'
              314  LOAD_CLOSURE             'self'
              316  LOAD_CLOSURE             'take_action'
              318  BUILD_TUPLE_5         5 
              320  LOAD_CODE                <code_object consume_positionals>
              322  LOAD_STR                 'ArgumentParser._parse_known_args.<locals>.consume_positionals'
              324  MAKE_FUNCTION_8          'closure'
              326  STORE_FAST               'consume_positionals'

 L.1974       328  BUILD_LIST_0          0 
              330  STORE_DEREF              'extras'

 L.1975       332  LOAD_CONST               0
              334  STORE_DEREF              'start_index'

 L.1976       336  LOAD_DEREF               'option_string_indices'
          338_340  POP_JUMP_IF_FALSE   352  'to 352'

 L.1977       342  LOAD_GLOBAL              max
              344  LOAD_DEREF               'option_string_indices'
              346  CALL_FUNCTION_1       1  ''
              348  STORE_FAST               'max_option_string_index'
              350  JUMP_FORWARD        356  'to 356'
            352_0  COME_FROM           338  '338'

 L.1979       352  LOAD_CONST               -1
              354  STORE_FAST               'max_option_string_index'
            356_0  COME_FROM           474  '474'
            356_1  COME_FROM           420  '420'
            356_2  COME_FROM           350  '350'

 L.1980       356  LOAD_DEREF               'start_index'
              358  LOAD_FAST                'max_option_string_index'
              360  COMPARE_OP               <=
          362_364  POP_JUMP_IF_FALSE   478  'to 478'

 L.1983       366  LOAD_GLOBAL              min
              368  LOAD_CLOSURE             'start_index'
              370  BUILD_TUPLE_1         1 
              372  LOAD_LISTCOMP            '<code_object <listcomp>>'
              374  LOAD_STR                 'ArgumentParser._parse_known_args.<locals>.<listcomp>'
              376  MAKE_FUNCTION_8          'closure'

 L.1985       378  LOAD_DEREF               'option_string_indices'

 L.1983       380  GET_ITER         
              382  CALL_FUNCTION_1       1  ''
              384  CALL_FUNCTION_1       1  ''
              386  STORE_FAST               'next_option_string_index'

 L.1987       388  LOAD_DEREF               'start_index'
              390  LOAD_FAST                'next_option_string_index'
              392  COMPARE_OP               !=
          394_396  POP_JUMP_IF_FALSE   430  'to 430'

 L.1988       398  LOAD_FAST                'consume_positionals'
              400  LOAD_DEREF               'start_index'
              402  CALL_FUNCTION_1       1  ''
              404  STORE_FAST               'positionals_end_index'

 L.1992       406  LOAD_FAST                'positionals_end_index'
              408  LOAD_DEREF               'start_index'
              410  COMPARE_OP               >
          412_414  POP_JUMP_IF_FALSE   426  'to 426'

 L.1993       416  LOAD_FAST                'positionals_end_index'
              418  STORE_DEREF              'start_index'

 L.1994   420_422  JUMP_BACK           356  'to 356'
              424  BREAK_LOOP          430  'to 430'
            426_0  COME_FROM           412  '412'

 L.1996       426  LOAD_FAST                'positionals_end_index'
              428  STORE_DEREF              'start_index'
            430_0  COME_FROM           424  '424'
            430_1  COME_FROM           394  '394'

 L.2000       430  LOAD_DEREF               'start_index'
              432  LOAD_DEREF               'option_string_indices'
              434  COMPARE_OP               not-in
          436_438  POP_JUMP_IF_FALSE   466  'to 466'

 L.2001       440  LOAD_DEREF               'arg_strings'
              442  LOAD_DEREF               'start_index'
              444  LOAD_FAST                'next_option_string_index'
              446  BUILD_SLICE_2         2 
              448  BINARY_SUBSCR    
              450  STORE_FAST               'strings'

 L.2002       452  LOAD_DEREF               'extras'
              454  LOAD_METHOD              extend
              456  LOAD_FAST                'strings'
              458  CALL_METHOD_1         1  ''
              460  POP_TOP          

 L.2003       462  LOAD_FAST                'next_option_string_index'
              464  STORE_DEREF              'start_index'
            466_0  COME_FROM           436  '436'

 L.2006       466  LOAD_FAST                'consume_optional'
              468  LOAD_DEREF               'start_index'
              470  CALL_FUNCTION_1       1  ''
              472  STORE_DEREF              'start_index'
          474_476  JUMP_BACK           356  'to 356'
            478_0  COME_FROM           362  '362'

 L.2009       478  LOAD_FAST                'consume_positionals'
              480  LOAD_DEREF               'start_index'
              482  CALL_FUNCTION_1       1  ''
              484  STORE_FAST               'stop_index'

 L.2012       486  LOAD_DEREF               'extras'
              488  LOAD_METHOD              extend
              490  LOAD_DEREF               'arg_strings'
              492  LOAD_FAST                'stop_index'
              494  LOAD_CONST               None
              496  BUILD_SLICE_2         2 
              498  BINARY_SUBSCR    
              500  CALL_METHOD_1         1  ''
              502  POP_TOP          

 L.2016       504  BUILD_LIST_0          0 
              506  STORE_FAST               'required_actions'

 L.2017       508  LOAD_DEREF               'self'
              510  LOAD_ATTR                _actions
              512  GET_ITER         
            514_0  COME_FROM           636  '636'
            514_1  COME_FROM           608  '608'
            514_2  COME_FROM           588  '588'
            514_3  COME_FROM           574  '574'
            514_4  COME_FROM           560  '560'
            514_5  COME_FROM           550  '550'
            514_6  COME_FROM           524  '524'
              514  FOR_ITER            640  'to 640'
              516  STORE_FAST               'action'

 L.2018       518  LOAD_FAST                'action'
              520  LOAD_DEREF               'seen_actions'
              522  COMPARE_OP               not-in
          524_526  POP_JUMP_IF_FALSE_BACK   514  'to 514'

 L.2019       528  LOAD_FAST                'action'
              530  LOAD_ATTR                required
          532_534  POP_JUMP_IF_FALSE   552  'to 552'

 L.2020       536  LOAD_FAST                'required_actions'
              538  LOAD_METHOD              append
              540  LOAD_GLOBAL              _get_action_name
              542  LOAD_FAST                'action'
              544  CALL_FUNCTION_1       1  ''
              546  CALL_METHOD_1         1  ''
              548  POP_TOP          
              550  JUMP_BACK           514  'to 514'
            552_0  COME_FROM           532  '532'

 L.2026       552  LOAD_FAST                'action'
              554  LOAD_ATTR                default
              556  LOAD_CONST               None
              558  COMPARE_OP               is-not
          560_562  POP_JUMP_IF_FALSE_BACK   514  'to 514'

 L.2027       564  LOAD_GLOBAL              isinstance
              566  LOAD_FAST                'action'
              568  LOAD_ATTR                default
              570  LOAD_GLOBAL              str
              572  CALL_FUNCTION_2       2  ''

 L.2026   574_576  POP_JUMP_IF_FALSE_BACK   514  'to 514'

 L.2028       578  LOAD_GLOBAL              hasattr
              580  LOAD_DEREF               'namespace'
              582  LOAD_FAST                'action'
              584  LOAD_ATTR                dest
              586  CALL_FUNCTION_2       2  ''

 L.2026   588_590  POP_JUMP_IF_FALSE_BACK   514  'to 514'

 L.2029       592  LOAD_FAST                'action'
              594  LOAD_ATTR                default
              596  LOAD_GLOBAL              getattr
              598  LOAD_DEREF               'namespace'
              600  LOAD_FAST                'action'
              602  LOAD_ATTR                dest
              604  CALL_FUNCTION_2       2  ''
              606  COMPARE_OP               is

 L.2026   608_610  POP_JUMP_IF_FALSE_BACK   514  'to 514'

 L.2030       612  LOAD_GLOBAL              setattr
              614  LOAD_DEREF               'namespace'
              616  LOAD_FAST                'action'
              618  LOAD_ATTR                dest

 L.2031       620  LOAD_DEREF               'self'
              622  LOAD_METHOD              _get_value
              624  LOAD_FAST                'action'
              626  LOAD_FAST                'action'
              628  LOAD_ATTR                default
              630  CALL_METHOD_2         2  ''

 L.2030       632  CALL_FUNCTION_3       3  ''
              634  POP_TOP          
          636_638  JUMP_BACK           514  'to 514'
            640_0  COME_FROM           514  '514'

 L.2033       640  LOAD_FAST                'required_actions'
          642_644  POP_JUMP_IF_FALSE   670  'to 670'

 L.2034       646  LOAD_DEREF               'self'
              648  LOAD_METHOD              error
              650  LOAD_GLOBAL              _
              652  LOAD_STR                 'the following arguments are required: %s'
              654  CALL_FUNCTION_1       1  ''

 L.2035       656  LOAD_STR                 ', '
              658  LOAD_METHOD              join
              660  LOAD_FAST                'required_actions'
              662  CALL_METHOD_1         1  ''

 L.2034       664  BINARY_MODULO    
              666  CALL_METHOD_1         1  ''
              668  POP_TOP          
            670_0  COME_FROM           642  '642'

 L.2038       670  LOAD_DEREF               'self'
              672  LOAD_ATTR                _mutually_exclusive_groups
              674  GET_ITER         
            676_0  COME_FROM           762  '762'
            676_1  COME_FROM           710  '710'
            676_2  COME_FROM           684  '684'
              676  FOR_ITER            766  'to 766'
              678  STORE_FAST               'group'

 L.2039       680  LOAD_FAST                'group'
              682  LOAD_ATTR                required
          684_686  POP_JUMP_IF_FALSE_BACK   676  'to 676'

 L.2040       688  LOAD_FAST                'group'
              690  LOAD_ATTR                _group_actions
              692  GET_ITER         
            694_0  COME_FROM           714  '714'
            694_1  COME_FROM           704  '704'
              694  FOR_ITER            718  'to 718'
              696  STORE_FAST               'action'

 L.2041       698  LOAD_FAST                'action'
              700  LOAD_DEREF               'seen_non_default_actions'
              702  COMPARE_OP               in
          704_706  POP_JUMP_IF_FALSE_BACK   694  'to 694'

 L.2042       708  POP_TOP          
          710_712  BREAK_LOOP          676  'to 676'
          714_716  JUMP_BACK           694  'to 694'
            718_0  COME_FROM           694  '694'

 L.2046       718  LOAD_LISTCOMP            '<code_object <listcomp>>'
              720  LOAD_STR                 'ArgumentParser._parse_known_args.<locals>.<listcomp>'
              722  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.2047       724  LOAD_FAST                'group'
              726  LOAD_ATTR                _group_actions

 L.2046       728  GET_ITER         
              730  CALL_FUNCTION_1       1  ''
              732  STORE_FAST               'names'

 L.2049       734  LOAD_GLOBAL              _
              736  LOAD_STR                 'one of the arguments %s is required'
              738  CALL_FUNCTION_1       1  ''
              740  STORE_FAST               'msg'

 L.2050       742  LOAD_DEREF               'self'
              744  LOAD_METHOD              error
              746  LOAD_FAST                'msg'
              748  LOAD_STR                 ' '
              750  LOAD_METHOD              join
              752  LOAD_FAST                'names'
              754  CALL_METHOD_1         1  ''
              756  BINARY_MODULO    
              758  CALL_METHOD_1         1  ''
              760  POP_TOP          
          762_764  JUMP_BACK           676  'to 676'
            766_0  COME_FROM           676  '676'

 L.2053       766  LOAD_DEREF               'namespace'
              768  LOAD_DEREF               'extras'
              770  BUILD_TUPLE_2         2 
              772  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 478

    def _read_args_from_files(self, arg_strings):
        new_arg_strings = []
        for arg_string in arg_strings:
            if arg_string:
                if arg_string[0] not in self.fromfile_prefix_chars:
                    new_arg_strings.append(arg_string)
                else:
                    try:
                        with open(arg_string[1:]) as args_file:
                            arg_strings = []
                            for arg_line in args_file.read().splitlines():
                                for arg in self.convert_arg_line_to_args(arg_line):
                                    arg_strings.append(arg)

                            else:
                                arg_strings = self._read_args_from_files(arg_strings)
                                new_arg_strings.extend(arg_strings)

                    except OSError:
                        err = _sys.exc_info()[1]
                        self.error(str(err))

        else:
            return new_arg_strings

    def convert_arg_line_to_args(self, arg_line):
        return [
         arg_line]

    def _match_argument(self, action, arg_strings_pattern):
        nargs_pattern = self._get_nargs_pattern(action)
        match = _re.match(nargs_pattern, arg_strings_pattern)
        if match is None:
            nargs_errors = {None: _('expected one argument'), 
             OPTIONAL: _('expected at most one argument'), 
             ONE_OR_MORE: _('expected at least one argument')}
            msg = nargs_errors.get(action.nargs)
            if msg is None:
                msg = ngettext('expected %s argument', 'expected %s arguments', action.nargs) % action.nargs
            raise ArgumentError(action, msg)
        return len(match.group(1))

    def _match_arguments_partial(self, actions, arg_strings_pattern):
        result = []
        for i in range(len(actions), 0, -1):
            actions_slice = actions[:i]
            pattern = ''.join([self._get_nargs_pattern(action) for action in actions_slice])
            match = _re.match(pattern, arg_strings_pattern)
            if match is not None:
                result.extend([len(string) for string in match.groups()])
                break
        else:
            return result

    def _parse_optional(self, arg_string):
        if not arg_string:
            return
        if arg_string[0] not in self.prefix_chars:
            return
        if arg_string in self._option_string_actions:
            action = self._option_string_actions[arg_string]
            return (
             action, arg_string, None)
        if len(arg_string) == 1:
            return
        if '=' in arg_string:
            option_string, explicit_arg = arg_string.split('=', 1)
            if option_string in self._option_string_actions:
                action = self._option_string_actions[option_string]
                return (
                 action, option_string, explicit_arg)
        option_tuples = self._get_option_tuples(arg_string)
        if len(option_tuples) > 1:
            options = ', '.join([option_string for action, option_string, explicit_arg in option_tuples])
            args = {'option':arg_string,  'matches':options}
            msg = _('ambiguous option: %(option)s could match %(matches)s')
            self.error(msg % args)
        elif len(option_tuples) == 1:
            option_tuple, = option_tuples
            return option_tuple
        if self._negative_number_matcher.match(arg_string):
            if not self._has_negative_number_optionals:
                return
            if ' ' in arg_string:
                return
            return (
             None, arg_string, None)

    def _get_option_tuples(self, option_string):
        result = []
        chars = self.prefix_chars
        if option_string[0] in chars and option_string[1] in chars:
            if self.allow_abbrev:
                if '=' in option_string:
                    option_prefix, explicit_arg = option_string.split('=', 1)
                else:
                    option_prefix = option_string
                    explicit_arg = None
                for option_string in self._option_string_actions:
                    if option_string.startswith(option_prefix):
                        action = self._option_string_actions[option_string]
                        tup = (action, option_string, explicit_arg)
                        result.append(tup)

        elif option_string[0] in chars and option_string[1] not in chars:
            option_prefix = option_string
            explicit_arg = None
            short_option_prefix = option_string[:2]
            short_explicit_arg = option_string[2:]
            for option_string in self._option_string_actions:
                if option_string == short_option_prefix:
                    action = self._option_string_actions[option_string]
                    tup = (action, option_string, short_explicit_arg)
                    result.append(tup)
                else:
                    if option_string.startswith(option_prefix):
                        action = self._option_string_actions[option_string]
                        tup = (action, option_string, explicit_arg)
                        result.append(tup)

        else:
            self.error(_('unexpected option string: %s') % option_string)
        return result

    def _get_nargs_pattern(self, action):
        nargs = action.nargs
        if nargs is None:
            nargs_pattern = '(-*A-*)'
        elif nargs == OPTIONAL:
            nargs_pattern = '(-*A?-*)'
        elif nargs == ZERO_OR_MORE:
            nargs_pattern = '(-*[A-]*)'
        elif nargs == ONE_OR_MORE:
            nargs_pattern = '(-*A[A-]*)'
        elif nargs == REMAINDER:
            nargs_pattern = '([-AO]*)'
        elif nargs == PARSER:
            nargs_pattern = '(-*A[-AO]*)'
        elif nargs == SUPPRESS:
            nargs_pattern = '(-*-*)'
        else:
            nargs_pattern = '(-*%s-*)' % '-*'.join('A' * nargs)
        if action.option_strings:
            nargs_pattern = nargs_pattern.replace('-*', '')
            nargs_pattern = nargs_pattern.replace('-', '')
        return nargs_pattern

    def parse_intermixed_args(self, args=None, namespace=None):
        args, argv = self.parse_known_intermixed_args(args, namespace)
        if argv:
            msg = _('unrecognized arguments: %s')
            self.error(msg % ' '.join(argv))
        return args

    def parse_known_intermixed_args(self, args=None, namespace=None):
        positionals = self._get_positional_actions()
        a = [action for action in positionals if action.nargs in (PARSER, REMAINDER)]
        if a:
            raise TypeError('parse_intermixed_args: positional arg with nargs=%s' % a[0].nargs)
        if [action.dest for group in self._mutually_exclusive_groups if action in positionals for action in group]:
            raise TypeError('parse_intermixed_args: positional in mutuallyExclusiveGroup')
        try:
            save_usage = self.usage
            try:
                if self.usage is None:
                    self.usage = self.format_usage()[7:]
                for action in positionals:
                    action.save_nargs = action.nargs
                    action.nargs = SUPPRESS
                    action.save_default = action.default
                    action.default = SUPPRESS
                else:
                    namespace, remaining_args = self.parse_known_args(args, namespace)
                    for action in positionals:
                        if hasattr(namespace, action.dest):
                            if getattr(namespace, action.dest) == []:
                                from warnings import warn
                                warn('Do not expect %s in %s' % (action.dest, namespace))
                                delattr(namespace, action.dest)

            finally:
                for action in positionals:
                    action.nargs = action.save_nargs
                    action.default = action.save_default

            optionals = self._get_optional_actions()
            try:
                for action in optionals:
                    action.save_required = action.required
                    action.required = False
                else:
                    for group in self._mutually_exclusive_groups:
                        group.save_required = group.required
                        group.required = False
                    else:
                        namespace, extras = self.parse_known_args(remaining_args, namespace)

            finally:
                for action in optionals:
                    action.required = action.save_required
                else:
                    for group in self._mutually_exclusive_groups:
                        group.required = group.save_required

        finally:
            self.usage = save_usage

        return (namespace, extras)

    def _get_values(self, action, arg_strings):
        if action.nargs not in (PARSER, REMAINDER):
            try:
                arg_strings.remove('--')
            except ValueError:
                pass
            else:
                if not arg_strings or action.nargs == OPTIONAL:
                    if action.option_strings:
                        value = action.const
                    else:
                        value = action.default
                    if isinstance(value, str):
                        value = self._get_value(action, value)
                        self._check_value(action, value)
                elif (arg_strings or action.nargs) == ZERO_OR_MORE and not action.option_strings:
                    if action.default is not None:
                        value = action.default
                    else:
                        value = arg_strings
                    self._check_value(action, value)
                elif len(arg_strings) == 1 and action.nargs in (None, OPTIONAL):
                    arg_string, = arg_strings
                    value = self._get_value(action, arg_string)
                    self._check_value(action, value)
                elif action.nargs == REMAINDER:
                    value = [self._get_value(action, v) for v in arg_strings]
                elif action.nargs == PARSER:
                    value = [self._get_value(action, v) for v in arg_strings]
                    self._check_value(action, value[0])
                elif action.nargs == SUPPRESS:
                    value = SUPPRESS
                else:
                    value = [self._get_value(action, v) for v in arg_strings]
                    for v in value:
                        self._check_value(action, v)

            return value

    def _get_value(self, action, arg_string):
        type_func = self._registry_get('type', action.type, action.type)
        if not callable(type_func):
            msg = _('%r is not callable')
            raise ArgumentError(action, msg % type_func)
        try:
            result = type_func(arg_string)
        except ArgumentTypeError:
            name = getattr(action.type, '__name__', repr(action.type))
            msg = str(_sys.exc_info()[1])
            raise ArgumentError(action, msg)
        except (TypeError, ValueError):
            name = getattr(action.type, '__name__', repr(action.type))
            args = {'type':name,  'value':arg_string}
            msg = _('invalid %(type)s value: %(value)r')
            raise ArgumentError(action, msg % args)
        else:
            return result

    def _check_value(self, action, value):
        if action.choices is not None:
            if value not in action.choices:
                args = {'value':value, 
                 'choices':', '.join(map(repr, action.choices))}
                msg = _('invalid choice: %(value)r (choose from %(choices)s)')
                raise ArgumentError(action, msg % args)

    def format_usage(self):
        formatter = self._get_formatter()
        formatter.add_usage(self.usage, self._actions, self._mutually_exclusive_groups)
        return formatter.format_help()

    def format_help(self):
        formatter = self._get_formatter()
        formatter.add_usage(self.usage, self._actions, self._mutually_exclusive_groups)
        formatter.add_text(self.description)
        for action_group in self._action_groups:
            formatter.start_section(action_group.title)
            formatter.add_text(action_group.description)
            formatter.add_arguments(action_group._group_actions)
            formatter.end_section()
        else:
            formatter.add_text(self.epilog)
            return formatter.format_help()

    def _get_formatter(self):
        return self.formatter_class(prog=(self.prog))

    def print_usage(self, file=None):
        if file is None:
            file = _sys.stdout
        self._print_message(self.format_usage(), file)

    def print_help(self, file=None):
        if file is None:
            file = _sys.stdout
        self._print_message(self.format_help(), file)

    def _print_message(self, message, file=None):
        if message:
            if file is None:
                file = _sys.stderr
            file.write(message)

    def exit(self, status=0, message=None):
        if message:
            self._print_message(message, _sys.stderr)
        _sys.exit(status)

    def error(self, message):
        """error(message: string)

        Prints a usage message incorporating the message to stderr and
        exits.

        If you override this in a subclass, it should not return -- it
        should either exit or raise an exception.
        """
        self.print_usage(_sys.stderr)
        args = {'prog':self.prog,  'message':message}
        self.exit(2, _('%(prog)s: error: %(message)s\n') % args)