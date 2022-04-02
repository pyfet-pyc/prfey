# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
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
import os as _os, re as _re, sys as _sys
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

        for name, value in self._get_kwargs():
            if name.isidentifier():
                arg_strings.append('%s=%r' % (name, value))
            else:
                star_args[name] = value

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
            try:
                width = int(_os.environ['COLUMNS'])
            except (KeyError, ValueError):
                width = 80

            width -= 2
        self._prog = prog
        self._indent_increment = indent_increment
        self._max_help_position = max_help_position
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
            else:
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
        else:
            if usage is None:
                usage = actions or '%(prog)s' % dict(prog=(self._prog))
            else:
                if usage is None:
                    prog = '%(prog)s' % dict(prog=(self._prog))
                    optionals = []
                    positionals = []
                    for action in actions:
                        if action.option_strings:
                            optionals.append(action)
                        else:
                            positionals.append(action)

                    format = self._format_actions_usage
                    action_usage = format(optionals + positionals, groups)
                    usage = ' '.join([s for s in [prog, action_usage] if s])
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
                            else:
                                if pos_parts:
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

 L. 393         0  LOAD_GLOBAL              set
                2  CALL_FUNCTION_0       0  '0 positional arguments'
                4  STORE_FAST               'group_actions'

 L. 394         6  BUILD_MAP_0           0 
                8  STORE_FAST               'inserts'

 L. 395     10_12  SETUP_LOOP          310  'to 310'
               14  LOAD_FAST                'groups'
               16  GET_ITER         
             18_0  COME_FROM            98  '98'
            18_20  FOR_ITER            308  'to 308'
               22  STORE_FAST               'group'

 L. 396        24  SETUP_EXCEPT         46  'to 46'

 L. 397        26  LOAD_FAST                'actions'
               28  LOAD_METHOD              index
               30  LOAD_FAST                'group'
               32  LOAD_ATTR                _group_actions
               34  LOAD_CONST               0
               36  BINARY_SUBSCR    
               38  CALL_METHOD_1         1  '1 positional argument'
               40  STORE_FAST               'start'
               42  POP_BLOCK        
               44  JUMP_FORWARD         68  'to 68'
             46_0  COME_FROM_EXCEPT     24  '24'

 L. 398        46  DUP_TOP          
               48  LOAD_GLOBAL              ValueError
               50  COMPARE_OP               exception-match
               52  POP_JUMP_IF_FALSE    66  'to 66'
               54  POP_TOP          
               56  POP_TOP          
               58  POP_TOP          

 L. 399        60  CONTINUE_LOOP        18  'to 18'
               62  POP_EXCEPT       
               64  JUMP_BACK            18  'to 18'
             66_0  COME_FROM            52  '52'
               66  END_FINALLY      
             68_0  COME_FROM            44  '44'

 L. 401        68  LOAD_FAST                'start'
               70  LOAD_GLOBAL              len
               72  LOAD_FAST                'group'
               74  LOAD_ATTR                _group_actions
               76  CALL_FUNCTION_1       1  '1 positional argument'
               78  BINARY_ADD       
               80  STORE_FAST               'end'

 L. 402        82  LOAD_FAST                'actions'
               84  LOAD_FAST                'start'
               86  LOAD_FAST                'end'
               88  BUILD_SLICE_2         2 
               90  BINARY_SUBSCR    
               92  LOAD_FAST                'group'
               94  LOAD_ATTR                _group_actions
               96  COMPARE_OP               ==
               98  POP_JUMP_IF_FALSE    18  'to 18'

 L. 403       100  SETUP_LOOP          126  'to 126'
              102  LOAD_FAST                'group'
              104  LOAD_ATTR                _group_actions
              106  GET_ITER         
              108  FOR_ITER            124  'to 124'
              110  STORE_FAST               'action'

 L. 404       112  LOAD_FAST                'group_actions'
              114  LOAD_METHOD              add
              116  LOAD_FAST                'action'
              118  CALL_METHOD_1         1  '1 positional argument'
              120  POP_TOP          
              122  JUMP_BACK           108  'to 108'
              124  POP_BLOCK        
            126_0  COME_FROM_LOOP      100  '100'

 L. 405       126  LOAD_FAST                'group'
              128  LOAD_ATTR                required
              130  POP_JUMP_IF_TRUE    202  'to 202'

 L. 406       132  LOAD_FAST                'start'
              134  LOAD_FAST                'inserts'
              136  COMPARE_OP               in
              138  POP_JUMP_IF_FALSE   158  'to 158'

 L. 407       140  LOAD_FAST                'inserts'
              142  LOAD_FAST                'start'
              144  DUP_TOP_TWO      
              146  BINARY_SUBSCR    
              148  LOAD_STR                 ' ['
              150  INPLACE_ADD      
              152  ROT_THREE        
              154  STORE_SUBSCR     
              156  JUMP_FORWARD        166  'to 166'
            158_0  COME_FROM           138  '138'

 L. 409       158  LOAD_STR                 '['
              160  LOAD_FAST                'inserts'
              162  LOAD_FAST                'start'
              164  STORE_SUBSCR     
            166_0  COME_FROM           156  '156'

 L. 410       166  LOAD_FAST                'end'
              168  LOAD_FAST                'inserts'
              170  COMPARE_OP               in
              172  POP_JUMP_IF_FALSE   192  'to 192'

 L. 411       174  LOAD_FAST                'inserts'
              176  LOAD_FAST                'end'
              178  DUP_TOP_TWO      
              180  BINARY_SUBSCR    
              182  LOAD_STR                 ']'
              184  INPLACE_ADD      
              186  ROT_THREE        
              188  STORE_SUBSCR     
              190  JUMP_FORWARD        200  'to 200'
            192_0  COME_FROM           172  '172'

 L. 413       192  LOAD_STR                 ']'
              194  LOAD_FAST                'inserts'
              196  LOAD_FAST                'end'
              198  STORE_SUBSCR     
            200_0  COME_FROM           190  '190'
              200  JUMP_FORWARD        272  'to 272'
            202_0  COME_FROM           130  '130'

 L. 415       202  LOAD_FAST                'start'
              204  LOAD_FAST                'inserts'
              206  COMPARE_OP               in
              208  POP_JUMP_IF_FALSE   228  'to 228'

 L. 416       210  LOAD_FAST                'inserts'
              212  LOAD_FAST                'start'
              214  DUP_TOP_TWO      
              216  BINARY_SUBSCR    
              218  LOAD_STR                 ' ('
              220  INPLACE_ADD      
              222  ROT_THREE        
              224  STORE_SUBSCR     
              226  JUMP_FORWARD        236  'to 236'
            228_0  COME_FROM           208  '208'

 L. 418       228  LOAD_STR                 '('
              230  LOAD_FAST                'inserts'
              232  LOAD_FAST                'start'
              234  STORE_SUBSCR     
            236_0  COME_FROM           226  '226'

 L. 419       236  LOAD_FAST                'end'
              238  LOAD_FAST                'inserts'
              240  COMPARE_OP               in
          242_244  POP_JUMP_IF_FALSE   264  'to 264'

 L. 420       246  LOAD_FAST                'inserts'
              248  LOAD_FAST                'end'
              250  DUP_TOP_TWO      
              252  BINARY_SUBSCR    
              254  LOAD_STR                 ')'
              256  INPLACE_ADD      
              258  ROT_THREE        
              260  STORE_SUBSCR     
              262  JUMP_FORWARD        272  'to 272'
            264_0  COME_FROM           242  '242'

 L. 422       264  LOAD_STR                 ')'
              266  LOAD_FAST                'inserts'
              268  LOAD_FAST                'end'
              270  STORE_SUBSCR     
            272_0  COME_FROM           262  '262'
            272_1  COME_FROM           200  '200'

 L. 423       272  SETUP_LOOP          306  'to 306'
              274  LOAD_GLOBAL              range
              276  LOAD_FAST                'start'
              278  LOAD_CONST               1
              280  BINARY_ADD       
              282  LOAD_FAST                'end'
              284  CALL_FUNCTION_2       2  '2 positional arguments'
              286  GET_ITER         
              288  FOR_ITER            304  'to 304'
              290  STORE_FAST               'i'

 L. 424       292  LOAD_STR                 '|'
              294  LOAD_FAST                'inserts'
              296  LOAD_FAST                'i'
              298  STORE_SUBSCR     
          300_302  JUMP_BACK           288  'to 288'
              304  POP_BLOCK        
            306_0  COME_FROM_LOOP      272  '272'
              306  JUMP_BACK            18  'to 18'
              308  POP_BLOCK        
            310_0  COME_FROM_LOOP       10  '10'

 L. 427       310  BUILD_LIST_0          0 
              312  STORE_FAST               'parts'

 L. 428   314_316  SETUP_LOOP          622  'to 622'
              318  LOAD_GLOBAL              enumerate
              320  LOAD_FAST                'actions'
              322  CALL_FUNCTION_1       1  '1 positional argument'
              324  GET_ITER         
          326_328  FOR_ITER            620  'to 620'
              330  UNPACK_SEQUENCE_2     2 
              332  STORE_FAST               'i'
              334  STORE_FAST               'action'

 L. 432       336  LOAD_FAST                'action'
              338  LOAD_ATTR                help
              340  LOAD_GLOBAL              SUPPRESS
              342  COMPARE_OP               is
          344_346  POP_JUMP_IF_FALSE   422  'to 422'

 L. 433       348  LOAD_FAST                'parts'
              350  LOAD_METHOD              append
              352  LOAD_CONST               None
              354  CALL_METHOD_1         1  '1 positional argument'
              356  POP_TOP          

 L. 434       358  LOAD_FAST                'inserts'
              360  LOAD_METHOD              get
              362  LOAD_FAST                'i'
              364  CALL_METHOD_1         1  '1 positional argument'
              366  LOAD_STR                 '|'
              368  COMPARE_OP               ==
          370_372  POP_JUMP_IF_FALSE   386  'to 386'

 L. 435       374  LOAD_FAST                'inserts'
              376  LOAD_METHOD              pop
              378  LOAD_FAST                'i'
              380  CALL_METHOD_1         1  '1 positional argument'
              382  POP_TOP          
              384  JUMP_FORWARD        420  'to 420'
            386_0  COME_FROM           370  '370'

 L. 436       386  LOAD_FAST                'inserts'
              388  LOAD_METHOD              get
              390  LOAD_FAST                'i'
              392  LOAD_CONST               1
              394  BINARY_ADD       
              396  CALL_METHOD_1         1  '1 positional argument'
              398  LOAD_STR                 '|'
              400  COMPARE_OP               ==
          402_404  POP_JUMP_IF_FALSE   616  'to 616'

 L. 437       406  LOAD_FAST                'inserts'
              408  LOAD_METHOD              pop
              410  LOAD_FAST                'i'
              412  LOAD_CONST               1
              414  BINARY_ADD       
              416  CALL_METHOD_1         1  '1 positional argument'
              418  POP_TOP          
            420_0  COME_FROM           384  '384'
              420  JUMP_BACK           326  'to 326'
            422_0  COME_FROM           344  '344'

 L. 440       422  LOAD_FAST                'action'
              424  LOAD_ATTR                option_strings
          426_428  POP_JUMP_IF_TRUE    514  'to 514'

 L. 441       430  LOAD_FAST                'self'
              432  LOAD_METHOD              _get_default_metavar_for_positional
              434  LOAD_FAST                'action'
              436  CALL_METHOD_1         1  '1 positional argument'
              438  STORE_FAST               'default'

 L. 442       440  LOAD_FAST                'self'
              442  LOAD_METHOD              _format_args
              444  LOAD_FAST                'action'
              446  LOAD_FAST                'default'
              448  CALL_METHOD_2         2  '2 positional arguments'
              450  STORE_FAST               'part'

 L. 445       452  LOAD_FAST                'action'
              454  LOAD_FAST                'group_actions'
              456  COMPARE_OP               in
          458_460  POP_JUMP_IF_FALSE   502  'to 502'

 L. 446       462  LOAD_FAST                'part'
              464  LOAD_CONST               0
              466  BINARY_SUBSCR    
              468  LOAD_STR                 '['
              470  COMPARE_OP               ==
          472_474  POP_JUMP_IF_FALSE   502  'to 502'
              476  LOAD_FAST                'part'
              478  LOAD_CONST               -1
              480  BINARY_SUBSCR    
              482  LOAD_STR                 ']'
              484  COMPARE_OP               ==
          486_488  POP_JUMP_IF_FALSE   502  'to 502'

 L. 447       490  LOAD_FAST                'part'
              492  LOAD_CONST               1
              494  LOAD_CONST               -1
              496  BUILD_SLICE_2         2 
              498  BINARY_SUBSCR    
              500  STORE_FAST               'part'
            502_0  COME_FROM           486  '486'
            502_1  COME_FROM           472  '472'
            502_2  COME_FROM           458  '458'

 L. 450       502  LOAD_FAST                'parts'
              504  LOAD_METHOD              append
              506  LOAD_FAST                'part'
              508  CALL_METHOD_1         1  '1 positional argument'
              510  POP_TOP          
              512  JUMP_BACK           326  'to 326'
            514_0  COME_FROM           426  '426'

 L. 454       514  LOAD_FAST                'action'
              516  LOAD_ATTR                option_strings
              518  LOAD_CONST               0
              520  BINARY_SUBSCR    
              522  STORE_FAST               'option_string'

 L. 458       524  LOAD_FAST                'action'
              526  LOAD_ATTR                nargs
              528  LOAD_CONST               0
              530  COMPARE_OP               ==
          532_534  POP_JUMP_IF_FALSE   546  'to 546'

 L. 459       536  LOAD_STR                 '%s'
              538  LOAD_FAST                'option_string'
              540  BINARY_MODULO    
              542  STORE_FAST               'part'
              544  JUMP_FORWARD        580  'to 580'
            546_0  COME_FROM           532  '532'

 L. 464       546  LOAD_FAST                'self'
              548  LOAD_METHOD              _get_default_metavar_for_optional
              550  LOAD_FAST                'action'
              552  CALL_METHOD_1         1  '1 positional argument'
              554  STORE_FAST               'default'

 L. 465       556  LOAD_FAST                'self'
              558  LOAD_METHOD              _format_args
              560  LOAD_FAST                'action'
              562  LOAD_FAST                'default'
              564  CALL_METHOD_2         2  '2 positional arguments'
              566  STORE_FAST               'args_string'

 L. 466       568  LOAD_STR                 '%s %s'
              570  LOAD_FAST                'option_string'
              572  LOAD_FAST                'args_string'
              574  BUILD_TUPLE_2         2 
              576  BINARY_MODULO    
              578  STORE_FAST               'part'
            580_0  COME_FROM           544  '544'

 L. 469       580  LOAD_FAST                'action'
              582  LOAD_ATTR                required
          584_586  POP_JUMP_IF_TRUE    606  'to 606'
              588  LOAD_FAST                'action'
              590  LOAD_FAST                'group_actions'
              592  COMPARE_OP               not-in
          594_596  POP_JUMP_IF_FALSE   606  'to 606'

 L. 470       598  LOAD_STR                 '[%s]'
              600  LOAD_FAST                'part'
              602  BINARY_MODULO    
              604  STORE_FAST               'part'
            606_0  COME_FROM           594  '594'
            606_1  COME_FROM           584  '584'

 L. 473       606  LOAD_FAST                'parts'
              608  LOAD_METHOD              append
              610  LOAD_FAST                'part'
              612  CALL_METHOD_1         1  '1 positional argument'
              614  POP_TOP          
            616_0  COME_FROM           402  '402'
          616_618  JUMP_BACK           326  'to 326'
              620  POP_BLOCK        
            622_0  COME_FROM_LOOP      314  '314'

 L. 476       622  SETUP_LOOP          664  'to 664'
              624  LOAD_GLOBAL              sorted
              626  LOAD_FAST                'inserts'
              628  LOAD_CONST               True
              630  LOAD_CONST               ('reverse',)
              632  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              634  GET_ITER         
              636  FOR_ITER            662  'to 662'
              638  STORE_FAST               'i'

 L. 477       640  LOAD_FAST                'inserts'
              642  LOAD_FAST                'i'
              644  BINARY_SUBSCR    
              646  BUILD_LIST_1          1 
              648  LOAD_FAST                'parts'
              650  LOAD_FAST                'i'
              652  LOAD_FAST                'i'
              654  BUILD_SLICE_2         2 
              656  STORE_SUBSCR     
          658_660  JUMP_BACK           636  'to 636'
              662  POP_BLOCK        
            664_0  COME_FROM_LOOP      622  '622'

 L. 480       664  LOAD_STR                 ' '
              666  LOAD_METHOD              join
              668  LOAD_LISTCOMP            '<code_object <listcomp>>'
              670  LOAD_STR                 'HelpFormatter._format_actions_usage.<locals>.<listcomp>'
              672  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              674  LOAD_FAST                'parts'
              676  GET_ITER         
              678  CALL_FUNCTION_1       1  '1 positional argument'
              680  CALL_METHOD_1         1  '1 positional argument'
              682  STORE_FAST               'text'

 L. 483       684  LOAD_STR                 '[\\[(]'
              686  STORE_FAST               'open'

 L. 484       688  LOAD_STR                 '[\\])]'
              690  STORE_FAST               'close'

 L. 485       692  LOAD_GLOBAL              _re
              694  LOAD_METHOD              sub
              696  LOAD_STR                 '(%s) '
              698  LOAD_FAST                'open'
              700  BINARY_MODULO    
              702  LOAD_STR                 '\\1'
              704  LOAD_FAST                'text'
              706  CALL_METHOD_3         3  '3 positional arguments'
              708  STORE_FAST               'text'

 L. 486       710  LOAD_GLOBAL              _re
              712  LOAD_METHOD              sub
              714  LOAD_STR                 ' (%s)'
              716  LOAD_FAST                'close'
              718  BINARY_MODULO    
              720  LOAD_STR                 '\\1'
              722  LOAD_FAST                'text'
              724  CALL_METHOD_3         3  '3 positional arguments'
              726  STORE_FAST               'text'

 L. 487       728  LOAD_GLOBAL              _re
              730  LOAD_METHOD              sub
              732  LOAD_STR                 '%s *%s'
              734  LOAD_FAST                'open'
              736  LOAD_FAST                'close'
              738  BUILD_TUPLE_2         2 
              740  BINARY_MODULO    
              742  LOAD_STR                 ''
              744  LOAD_FAST                'text'
              746  CALL_METHOD_3         3  '3 positional arguments'
              748  STORE_FAST               'text'

 L. 488       750  LOAD_GLOBAL              _re
              752  LOAD_METHOD              sub
              754  LOAD_STR                 '\\(([^|]*)\\)'
              756  LOAD_STR                 '\\1'
              758  LOAD_FAST                'text'
              760  CALL_METHOD_3         3  '3 positional arguments'
              762  STORE_FAST               'text'

 L. 489       764  LOAD_FAST                'text'
              766  LOAD_METHOD              strip
              768  CALL_METHOD_0         0  '0 positional arguments'
              770  STORE_FAST               'text'

 L. 492       772  LOAD_FAST                'text'
              774  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 620

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
        else:
            if len(action_header) <= action_width:
                tup = (
                 self._current_indent, '', action_width, action_header)
                action_header = '%*s%-*s  ' % tup
                indent_first = 0
            else:
                tup = (self._current_indent, '', action_header)
                action_header = '%*s%s\n' % tup
                indent_first = help_position
        parts = [action_header]
        if action.help:
            help_text = self._expand_help(action)
            help_lines = self._split_lines(help_text, help_width)
            parts.append('%*s%s\n' % (indent_first, '', help_lines[0]))
            for line in help_lines[1:]:
                parts.append('%*s%s\n' % (help_position, '', line))

        else:
            if not action_header.endswith('\n'):
                parts.append('\n')
        for subaction in self._iter_indented_subactions(action):
            parts.append(self._format_action(subaction))

        return self._join_parts(parts)

    def _format_action_invocation(self, action):
        if not action.option_strings:
            default = self._get_default_metavar_for_positional(action)
            metavar, = self._metavar_formatter(action, default)(1)
            return metavar
        else:
            parts = []
            if action.nargs == 0:
                parts.extend(action.option_strings)
            else:
                default = self._get_default_metavar_for_optional(action)
                args_string = self._format_args(action, default)
                for option_string in action.option_strings:
                    parts.append('%s %s' % (option_string, args_string))

        return ', '.join(parts)

    def _metavar_formatter(self, action, default_metavar):
        if action.metavar is not None:
            result = action.metavar
        else:
            if action.choices is not None:
                choice_strs = [str(choice) for choice in action.choices]
                result = '{%s}' % ','.join(choice_strs)
            else:
                result = default_metavar

        def format(tuple_size):
            if isinstance(result, tuple):
                return result
            return (result,) * tuple_size

        return format

    def _format_args(self, action, default_metavar):
        get_metavar = self._metavar_formatter(action, default_metavar)
        if action.nargs is None:
            result = '%s' % get_metavar(1)
        else:
            if action.nargs == OPTIONAL:
                result = '[%s]' % get_metavar(1)
            else:
                if action.nargs == ZERO_OR_MORE:
                    result = '[%s [%s ...]]' % get_metavar(2)
                else:
                    if action.nargs == ONE_OR_MORE:
                        result = '%s [%s ...]' % get_metavar(2)
                    else:
                        if action.nargs == REMAINDER:
                            result = '...'
                        else:
                            if action.nargs == PARSER:
                                result = '%s ...' % get_metavar(1)
                            else:
                                if action.nargs == SUPPRESS:
                                    result = ''
                                else:
                                    formats = ['%s' for _ in range(action.nargs)]
                                    result = ' '.join(formats) % get_metavar(action.nargs)
        return result

    def _expand_help(self, action):
        params = dict((vars(action)), prog=(self._prog))
        for name in list(params):
            if params[name] is SUPPRESS:
                del params[name]

        for name in list(params):
            if hasattr(params[name], '__name__'):
                params[name] = params[name].__name__

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
        if '%(default)' not in action.help:
            if action.default is not SUPPRESS:
                defaulting_nargs = [
                 OPTIONAL, ZERO_OR_MORE]
                if action.option_strings or action.nargs in defaulting_nargs:
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
        return [(name, getattr(self, name)) for name in names]

    def __call__(self, parser, namespace, values, option_string=None):
        raise NotImplementedError(_('.__call__() not defined'))


class _StoreAction(Action):

    def __init__(self, option_strings, dest, nargs=None, const=None, default=None, type=None, choices=None, required=False, help=None, metavar=None):
        if nargs == 0:
            raise ValueError('nargs for store actions must be > 0; if you have nothing to store, actions such as store true or store const may be more appropriate')
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
            raise ValueError('nargs for append actions must be > 0; if arg strings are not supplying the value to append, the append const action may be more appropriate')
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

        subnamespace, arg_strings = parser.parse_known_args(arg_strings, None)
        for key, value in vars(subnamespace).items():
            setattr(namespace, key, value)

        if arg_strings:
            vars(namespace).setdefault(_UNRECOGNIZED_ARGS_ATTR, [])
            getattr(namespace, _UNRECOGNIZED_ARGS_ATTR).extend(arg_strings)


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
                message = _("can't open '%s': %s")
                raise ArgumentTypeError(message % (string, e))
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
            if action.dest == dest and action.default is not None:
                return action.default

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

        for option_string in action.option_strings:
            if self._negative_number_matcher.match(option_string):
                self._has_negative_number_optionals or self._has_negative_number_optionals.append(True)

        return action

    def _remove_action(self, action):
        self._actions.remove(action)

    def _add_container_actions(self, container):
        title_group_map = {}
        for group in self._action_groups:
            if group.title in title_group_map:
                msg = _('cannot merge actions - two groups are named %r')
                raise ValueError(msg % group.title)
            title_group_map[group.title] = group

        group_map = {}
        for group in container._action_groups:
            if group.title not in title_group_map:
                title_group_map[group.title] = self.add_argument_group(title=(group.title),
                  description=(group.description),
                  conflict_handler=(group.conflict_handler))
            for action in group._group_actions:
                group_map[action] = title_group_map[group.title]

        for group in container._mutually_exclusive_groups:
            mutex_group = self.add_mutually_exclusive_group(required=(group.required))
            for action in group._group_actions:
                group_map[action] = mutex_group

        for action in container._actions:
            group_map.get(action, self)._add_action(action)

    def _get_positional_kwargs(self, dest, **kwargs):
        if 'required' in kwargs:
            msg = _("'required' is an invalid argument for positionals")
            raise TypeError(msg)
        else:
            if kwargs.get('nargs') not in [OPTIONAL, ZERO_OR_MORE]:
                kwargs['required'] = True
            if kwargs.get('nargs') == ZERO_OR_MORE and 'default' not in kwargs:
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
            option_strings.append(option_string)
            if option_string[0] in self.prefix_chars and len(option_string) > 1 and option_string[1] in self.prefix_chars:
                long_option_strings.append(option_string)

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
        return [(name, getattr(self, name)) for name in names]

    def add_subparsers(self, **kwargs):
        if self._subparsers is not None:
            self.error(_('cannot have multiple subparser arguments'))
        else:
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
            if action.dest is not SUPPRESS and not hasattr(namespace, action.dest):
                if action.default is not SUPPRESS:
                    setattr(namespace, action.dest, action.default)

        for dest in self._defaults:
            if not hasattr(namespace, dest):
                setattr(namespace, dest, self._defaults[dest])

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

    def _parse_known_args(self, arg_strings, namespace):
        if self.fromfile_prefix_chars is not None:
            arg_strings = self._read_args_from_files(arg_strings)
        else:
            action_conflicts = {}
            for mutex_group in self._mutually_exclusive_groups:
                group_actions = mutex_group._group_actions
                for i, mutex_action in enumerate(mutex_group._group_actions):
                    conflicts = action_conflicts.setdefault(mutex_action, [])
                    conflicts.extend(group_actions[:i])
                    conflicts.extend(group_actions[i + 1:])

            option_string_indices = {}
            arg_string_pattern_parts = []
            arg_strings_iter = iter(arg_strings)
            for i, arg_string in enumerate(arg_strings_iter):
                if arg_string == '--':
                    arg_string_pattern_parts.append('-')
                    for arg_string in arg_strings_iter:
                        arg_string_pattern_parts.append('A')

                else:
                    option_tuple = self._parse_optional(arg_string)
                    if option_tuple is None:
                        pattern = 'A'
                    else:
                        option_string_indices[i] = option_tuple
                        pattern = 'O'
                    arg_string_pattern_parts.append(pattern)

            arg_strings_pattern = ''.join(arg_string_pattern_parts)
            seen_actions = set
            seen_non_default_actions = set

            def take_action(action, argument_strings, option_string=None):
                seen_actions.add(action)
                argument_values = self._get_values(action, argument_strings)
                if argument_values is not action.default:
                    seen_non_default_actions.add(action)
                    for conflict_action in action_conflicts.get(action, []):
                        if conflict_action in seen_non_default_actions:
                            msg = _('not allowed with argument %s')
                            action_name = _get_action_name(conflict_action)
                            raise ArgumentError(action, msg % action_name)

                if argument_values is not SUPPRESS:
                    action(self, namespace, argument_values, option_string)

            def consume_optional(start_index):
                option_tuple = option_string_indices[start_index]
                action, option_string, explicit_arg = option_tuple
                match_argument = self._match_argument
                action_tuples = []
                while action is None:
                    extras.append(arg_strings[start_index])
                    return start_index + 1
                    if explicit_arg is not None:
                        arg_count = match_argument(action, 'A')
                        chars = self.prefix_chars
                        if arg_count == 0 and option_string[1] not in chars:
                            action_tuples.append((action, [], option_string))
                            char = option_string[0]
                            option_string = char + explicit_arg[0]
                            new_explicit_arg = explicit_arg[1:] or None
                            optionals_map = self._option_string_actions
                            if option_string in optionals_map:
                                action = optionals_map[option_string]
                                explicit_arg = new_explicit_arg
                            else:
                                msg = _('ignored explicit argument %r')
                                raise ArgumentError(action, msg % explicit_arg)
                        else:
                            if arg_count == 1:
                                stop = start_index + 1
                                args = [explicit_arg]
                                action_tuples.append((action, args, option_string))
                                break
                            else:
                                msg = _('ignored explicit argument %r')
                                raise ArgumentError(action, msg % explicit_arg)
                    else:
                        start = start_index + 1
                        selected_patterns = arg_strings_pattern[start:]
                        arg_count = match_argument(action, selected_patterns)
                        stop = start + arg_count
                        args = arg_strings[start:stop]
                        action_tuples.append((action, args, option_string))
                        break

                assert action_tuples
                for action, args, option_string in action_tuples:
                    take_action(action, args, option_string)

                return stop

            positionals = self._get_positional_actions()

            def consume_positionals(start_index):
                match_partial = self._match_arguments_partial
                selected_pattern = arg_strings_pattern[start_index:]
                arg_counts = match_partial(positionals, selected_pattern)
                for action, arg_count in zip(positionals, arg_counts):
                    args = arg_strings[start_index:start_index + arg_count]
                    start_index += arg_count
                    take_action(action, args)

                positionals[:] = positionals[len(arg_counts):]
                return start_index

            extras = []
            start_index = 0
            if option_string_indices:
                max_option_string_index = max(option_string_indices)
            else:
                max_option_string_index = -1
        while start_index <= max_option_string_index:
            next_option_string_index = min([index for index in option_string_indices if index >= start_index])
            if start_index != next_option_string_index:
                positionals_end_index = consume_positionals(start_index)
                if positionals_end_index > start_index:
                    start_index = positionals_end_index
                    continue
                else:
                    start_index = positionals_end_index
            if start_index not in option_string_indices:
                strings = arg_strings[start_index:next_option_string_index]
                extras.extend(strings)
                start_index = next_option_string_index
            start_index = consume_optional(start_index)

        stop_index = consume_positionals(start_index)
        extras.extend(arg_strings[stop_index:])
        required_actions = []
        for action in self._actions:
            if action not in seen_actions:
                if action.required:
                    required_actions.append(_get_action_name(action))
                elif action.default is not None and isinstance(action.default, str) and hasattr(namespace, action.dest) and action.default is getattr(namespace, action.dest):
                    setattr(namespace, action.dest, self._get_value(action, action.default))

        if required_actions:
            self.error(_('the following arguments are required: %s') % ', '.join(required_actions))
        for group in self._mutually_exclusive_groups:
            if group.required:
                for action in group._group_actions:
                    if action in seen_non_default_actions:
                        break
                else:
                    names = [_get_action_name(action) for action in group._group_actions if action.help is not SUPPRESS]
                    msg = _('one of the arguments %s is required')
                    self.error(msg % ' '.join(names))

        return (
         namespace, extras)

    def _read_args_from_files(self, arg_strings):
        new_arg_strings = []
        for arg_string in arg_strings:
            if not arg_string or arg_string[0] not in self.fromfile_prefix_chars:
                new_arg_strings.append(arg_string)
            else:
                try:
                    with open(arg_string[1:]) as (args_file):
                        arg_strings = []
                        for arg_line in args_file.read().splitlines():
                            for arg in self.convert_arg_line_to_args(arg_line):
                                arg_strings.append(arg)

                        arg_strings = self._read_args_from_files(arg_strings)
                        new_arg_strings.extend(arg_strings)
                except OSError:
                    err = _sys.exc_info()[1]
                    self.error(str(err))

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

        return result

    def _parse_optional(self, arg_string):
        if not arg_string:
            return
            if arg_string[0] not in self.prefix_chars:
                return
            if arg_string in self._option_string_actions:
                action = self._option_string_actions[arg_string]
                return (action, arg_string, None)
            if len(arg_string) == 1:
                return
        else:
            if '=' in arg_string:
                option_string, explicit_arg = arg_string.split('=', 1)
                if option_string in self._option_string_actions:
                    action = self._option_string_actions[option_string]
                    return (action, option_string, explicit_arg)
            elif self.allow_abbrev:
                option_tuples = self._get_option_tuples(arg_string)
                if len(option_tuples) > 1:
                    options = ', '.join([option_string for action, option_string, explicit_arg in option_tuples])
                    args = {'option':arg_string,  'matches':options}
                    msg = _('ambiguous option: %(option)s could match %(matches)s')
                    self.error(msg % args)
                else:
                    if len(option_tuples) == 1:
                        option_tuple, = option_tuples
                        return option_tuple
            if self._negative_number_matcher.match(arg_string):
                return self._has_negative_number_optionals or None
        if ' ' in arg_string:
            return
        return (
         None, arg_string, None)

    def _get_option_tuples(self, option_string):
        result = []
        chars = self.prefix_chars
        if option_string[0] in chars and option_string[1] in chars:
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

        else:
            if option_string[0] in chars and option_string[1] not in chars:
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
        else:
            if nargs == OPTIONAL:
                nargs_pattern = '(-*A?-*)'
            else:
                if nargs == ZERO_OR_MORE:
                    nargs_pattern = '(-*[A-]*)'
                else:
                    if nargs == ONE_OR_MORE:
                        nargs_pattern = '(-*A[A-]*)'
                    else:
                        if nargs == REMAINDER:
                            nargs_pattern = '([-AO]*)'
                        else:
                            if nargs == PARSER:
                                nargs_pattern = '(-*A[-AO]*)'
                            else:
                                if nargs == SUPPRESS:
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
        a = [action for action in positionals if action.nargs in [PARSER, REMAINDER]]
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

                namespace, remaining_args = self.parse_known_args(args, namespace)
                for action in positionals:
                    if hasattr(namespace, action.dest) and getattr(namespace, action.dest) == []:
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

                for group in self._mutually_exclusive_groups:
                    group.save_required = group.required
                    group.required = False

                namespace, extras = self.parse_known_args(remaining_args, namespace)
            finally:
                for action in optionals:
                    action.required = action.save_required

                for group in self._mutually_exclusive_groups:
                    group.required = group.save_required

        finally:
            self.usage = save_usage

        return (
         namespace, extras)

    def _get_values(self, action, arg_strings):
        if action.nargs not in [PARSER, REMAINDER]:
            try:
                arg_strings.remove('--')
            except ValueError:
                pass

        if (arg_strings or action.nargs) == OPTIONAL:
            if action.option_strings:
                value = action.const
            else:
                value = action.default
            if isinstance(value, str):
                value = self._get_value(action, value)
                self._check_value(action, value)
        else:
            if (arg_strings or action.nargs) == ZERO_OR_MORE:
                if (action.option_strings or action.default) is not None:
                    value = action.default
                else:
                    value = arg_strings
                self._check_value(action, value)
            else:
                if len(arg_strings) == 1 and action.nargs in [None, OPTIONAL]:
                    arg_string, = arg_strings
                    value = self._get_value(action, arg_string)
                    self._check_value(action, value)
                else:
                    if action.nargs == REMAINDER:
                        value = [self._get_value(action, v) for v in arg_strings]
                    else:
                        if action.nargs == PARSER:
                            value = [self._get_value(action, v) for v in arg_strings]
                            self._check_value(action, value[0])
                        else:
                            if action.nargs == SUPPRESS:
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