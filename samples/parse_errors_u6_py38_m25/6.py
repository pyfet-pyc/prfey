# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: email\_policybase.py
"""Policy framework for the email package.

Allows fine grained feature control of how the package parses and emits data.
"""
import abc
from email import header
from email import charset as _charset
from email.utils import _has_surrogates
__all__ = [
 'Policy',
 'Compat32',
 'compat32']

class _PolicyBase:
    __doc__ = 'Policy Object basic framework.\n\n    This class is useless unless subclassed.  A subclass should define\n    class attributes with defaults for any values that are to be\n    managed by the Policy object.  The constructor will then allow\n    non-default values to be set for these attributes at instance\n    creation time.  The instance will be callable, taking these same\n    attributes keyword arguments, and returning a new instance\n    identical to the called instance except for those values changed\n    by the keyword arguments.  Instances may be added, yielding new\n    instances with any non-default values from the right hand\n    operand overriding those in the left hand operand.  That is,\n\n        A + B == A(<non-default values of B>)\n\n    The repr of an instance can be used to reconstruct the object\n    if and only if the repr of the values can be used to reconstruct\n    those values.\n\n    '

    def __init__(self, **kw):
        for name, value in kw.items():
            if hasattr(self, name):
                super(_PolicyBase, self).__setattr__(name, value)
            else:
                raise TypeError('{!r} is an invalid keyword argument for {}'.format(name, self.__class__.__name__))

    def __repr__(self):
        args = ['{}={!r}'.format(name, value) for name, value in self.__dict__.items()]
        return '{}({})'.format(self.__class__.__name__, ', '.join(args))

    def clone(self, **kw):
        """Return a new instance with specified attributes changed.

        The new instance has the same attribute values as the current object,
        except for the changes passed in as keyword arguments.

        """
        newpolicy = self.__class__.__new__(self.__class__)
        for attr, value in self.__dict__.items():
            object.__setattr__(newpolicy, attr, value)
        else:
            for attr, value in kw.items():
                if not hasattr(self, attr):
                    raise TypeError('{!r} is an invalid keyword argument for {}'.format(attr, self.__class__.__name__))
                object.__setattr__(newpolicy, attr, value)
            else:
                return newpolicy

    def __setattr__(self, name, value):
        if hasattr(self, name):
            msg = '{!r} object attribute {!r} is read-only'
        else:
            msg = '{!r} object has no attribute {!r}'
        raise AttributeError(msg.format(self.__class__.__name__, name))

    def __add__(self, other):
        """Non-default values from right operand override those from left.

        The object returned is a new instance of the subclass.

        """
        return (self.clone)(**other.__dict__)


def _append_doc(doc, added_doc):
    doc = doc.rsplit('\n', 1)[0]
    added_doc = added_doc.split('\n', 1)[1]
    return doc + '\n' + added_doc


def _extend_docstrings--- This code section failed: ---

 L. 100         0  LOAD_FAST                'cls'
                2  LOAD_ATTR                __doc__
                4  POP_JUMP_IF_FALSE    40  'to 40'
                6  LOAD_FAST                'cls'
                8  LOAD_ATTR                __doc__
               10  LOAD_METHOD              startswith
               12  LOAD_STR                 '+'
               14  CALL_METHOD_1         1  ''
               16  POP_JUMP_IF_FALSE    40  'to 40'

 L. 101        18  LOAD_GLOBAL              _append_doc
               20  LOAD_FAST                'cls'
               22  LOAD_ATTR                __bases__
               24  LOAD_CONST               0
               26  BINARY_SUBSCR    
               28  LOAD_ATTR                __doc__
               30  LOAD_FAST                'cls'
               32  LOAD_ATTR                __doc__
               34  CALL_FUNCTION_2       2  ''
               36  LOAD_FAST                'cls'
               38  STORE_ATTR               __doc__
             40_0  COME_FROM            16  '16'
             40_1  COME_FROM             4  '4'

 L. 102        40  LOAD_FAST                'cls'
               42  LOAD_ATTR                __dict__
               44  LOAD_METHOD              items
               46  CALL_METHOD_0         0  ''
               48  GET_ITER         
             50_0  COME_FROM            74  '74'
             50_1  COME_FROM            62  '62'
               50  FOR_ITER            138  'to 138'
               52  UNPACK_SEQUENCE_2     2 
               54  STORE_FAST               'name'
               56  STORE_FAST               'attr'

 L. 103        58  LOAD_FAST                'attr'
               60  LOAD_ATTR                __doc__
               62  POP_JUMP_IF_FALSE    50  'to 50'
               64  LOAD_FAST                'attr'
               66  LOAD_ATTR                __doc__
               68  LOAD_METHOD              startswith
               70  LOAD_STR                 '+'
               72  CALL_METHOD_1         1  ''
               74  POP_JUMP_IF_FALSE    50  'to 50'

 L. 104        76  LOAD_GENEXPR             '<code_object <genexpr>>'
               78  LOAD_STR                 '_extend_docstrings.<locals>.<genexpr>'
               80  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               82  LOAD_FAST                'cls'
               84  LOAD_ATTR                __bases__
               86  GET_ITER         
               88  CALL_FUNCTION_1       1  ''
               90  GET_ITER         
             92_0  COME_FROM           114  '114'
               92  FOR_ITER            136  'to 136'
               94  STORE_FAST               'c'

 L. 105        96  LOAD_GLOBAL              getattr
               98  LOAD_GLOBAL              getattr
              100  LOAD_FAST                'c'
              102  LOAD_FAST                'name'
              104  CALL_FUNCTION_2       2  ''
              106  LOAD_STR                 '__doc__'
              108  CALL_FUNCTION_2       2  ''
              110  STORE_FAST               'doc'

 L. 106       112  LOAD_FAST                'doc'
              114  POP_JUMP_IF_FALSE    92  'to 92'

 L. 107       116  LOAD_GLOBAL              _append_doc
              118  LOAD_FAST                'doc'
              120  LOAD_FAST                'attr'
              122  LOAD_ATTR                __doc__
              124  CALL_FUNCTION_2       2  ''
              126  LOAD_FAST                'attr'
              128  STORE_ATTR               __doc__

 L. 108       130  POP_TOP          
              132  CONTINUE             50  'to 50'
              134  JUMP_BACK            92  'to 92'
              136  JUMP_BACK            50  'to 50'

 L. 109       138  LOAD_FAST                'cls'
              140  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CONTINUE' instruction at offset 132


class Policy(_PolicyBase, metaclass=abc.ABCMeta):
    __doc__ = "Controls for how messages are interpreted and formatted.\n\n    Most of the classes and many of the methods in the email package accept\n    Policy objects as parameters.  A Policy object contains a set of values and\n    functions that control how input is interpreted and how output is rendered.\n    For example, the parameter 'raise_on_defect' controls whether or not an RFC\n    violation results in an error being raised or not, while 'max_line_length'\n    controls the maximum length of output lines when a Message is serialized.\n\n    Any valid attribute may be overridden when a Policy is created by passing\n    it as a keyword argument to the constructor.  Policy objects are immutable,\n    but a new Policy object can be created with only certain values changed by\n    calling the Policy instance with keyword arguments.  Policy objects can\n    also be added, producing a new Policy object in which the non-default\n    attributes set in the right hand operand overwrite those specified in the\n    left operand.\n\n    Settable attributes:\n\n    raise_on_defect     -- If true, then defects should be raised as errors.\n                           Default: False.\n\n    linesep             -- string containing the value to use as separation\n                           between output lines.  Default '\\n'.\n\n    cte_type            -- Type of allowed content transfer encodings\n\n                           7bit  -- ASCII only\n                           8bit  -- Content-Transfer-Encoding: 8bit is allowed\n\n                           Default: 8bit.  Also controls the disposition of\n                           (RFC invalid) binary data in headers; see the\n                           documentation of the binary_fold method.\n\n    max_line_length     -- maximum length of lines, excluding 'linesep',\n                           during serialization.  None or 0 means no line\n                           wrapping is done.  Default is 78.\n\n    mangle_from_        -- a flag that, when True escapes From_ lines in the\n                           body of the message by putting a `>' in front of\n                           them. This is used when the message is being\n                           serialized by a generator. Default: True.\n\n    message_factory     -- the class to use to create new message objects.\n                           If the value is None, the default is Message.\n\n    "
    raise_on_defect = False
    linesep = '\n'
    cte_type = '8bit'
    max_line_length = 78
    mangle_from_ = False
    message_factory = None

    def handle_defect(self, obj, defect):
        """Based on policy, either raise defect or call register_defect.

            handle_defect(obj, defect)

        defect should be a Defect subclass, but in any case must be an
        Exception subclass.  obj is the object on which the defect should be
        registered if it is not raised.  If the raise_on_defect is True, the
        defect is raised as an error, otherwise the object and the defect are
        passed to register_defect.

        This method is intended to be called by parsers that discover defects.
        The email package parsers always call it with Defect instances.

        """
        if self.raise_on_defect:
            raise defect
        self.register_defect(obj, defect)

    def register_defect(self, obj, defect):
        """Record 'defect' on 'obj'.

        Called by handle_defect if raise_on_defect is False.  This method is
        part of the Policy API so that Policy subclasses can implement custom
        defect handling.  The default implementation calls the append method of
        the defects attribute of obj.  The objects used by the email package by
        default that get passed to this method will always have a defects
        attribute with an append method.

        """
        obj.defects.append(defect)

    def header_max_count(self, name):
        """Return the maximum allowed number of headers named 'name'.

        Called when a header is added to a Message object.  If the returned
        value is not 0 or None, and there are already a number of headers with
        the name 'name' equal to the value returned, a ValueError is raised.

        Because the default behavior of Message's __setitem__ is to append the
        value to the list of headers, it is easy to create duplicate headers
        without realizing it.  This method allows certain headers to be limited
        in the number of instances of that header that may be added to a
        Message programmatically.  (The limit is not observed by the parser,
        which will faithfully produce as many headers as exist in the message
        being parsed.)

        The default implementation returns None for all header names.
        """
        pass

    @abc.abstractmethod
    def header_source_parse(self, sourcelines):
        """Given a list of linesep terminated strings constituting the lines of
        a single header, return the (name, value) tuple that should be stored
        in the model.  The input lines should retain their terminating linesep
        characters.  The lines passed in by the email package may contain
        surrogateescaped binary data.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def header_store_parse(self, name, value):
        """Given the header name and the value provided by the application
        program, return the (name, value) that should be stored in the model.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def header_fetch_parse(self, name, value):
        """Given the header name and the value from the model, return the value
        to be returned to the application program that is requesting that
        header.  The value passed in by the email package may contain
        surrogateescaped binary data if the lines were parsed by a BytesParser.
        The returned value should not contain any surrogateescaped data.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def fold(self, name, value):
        """Given the header name and the value from the model, return a string
        containing linesep characters that implement the folding of the header
        according to the policy controls.  The value passed in by the email
        package may contain surrogateescaped binary data if the lines were
        parsed by a BytesParser.  The returned value should not contain any
        surrogateescaped data.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def fold_binary(self, name, value):
        """Given the header name and the value from the model, return binary
        data containing linesep characters that implement the folding of the
        header according to the policy controls.  The value passed in by the
        email package may contain surrogateescaped binary data.

        """
        raise NotImplementedError


@_extend_docstrings
class Compat32(Policy):
    __doc__ = '+\n    This particular policy is the backward compatibility Policy.  It\n    replicates the behavior of the email package version 5.1.\n    '
    mangle_from_ = True

    def _sanitize_header(self, name, value):
        if not isinstance(value, str):
            return value
        if _has_surrogates(value):
            return header.Header(value, charset=(_charset.UNKNOWN8BIT), header_name=name)
        return value

    def header_source_parse(self, sourcelines):
        """+
        The name is parsed as everything up to the ':' and returned unmodified.
        The value is determined by stripping leading whitespace off the
        remainder of the first line, joining all subsequent lines together, and
        stripping any trailing carriage return or linefeed characters.

        """
        name, value = sourcelines[0].split(':', 1)
        value = value.lstrip(' \t') + ''.join(sourcelines[1:])
        return (name, value.rstrip('\r\n'))

    def header_store_parse(self, name, value):
        """+
        The name and value are returned unmodified.
        """
        return (
         name, value)

    def header_fetch_parse(self, name, value):
        """+
        If the value contains binary data, it is converted into a Header object
        using the unknown-8bit charset.  Otherwise it is returned unmodified.
        """
        return self._sanitize_header(name, value)

    def fold(self, name, value):
        """+
        Headers are folded using the Header folding algorithm, which preserves
        existing line breaks in the value, and wraps each resulting line to the
        max_line_length.  Non-ASCII binary data are CTE encoded using the
        unknown-8bit charset.

        """
        return self._fold(name, value, sanitize=True)

    def fold_binary(self, name, value):
        """+
        Headers are folded using the Header folding algorithm, which preserves
        existing line breaks in the value, and wraps each resulting line to the
        max_line_length.  If cte_type is 7bit, non-ascii binary data is CTE
        encoded using the unknown-8bit charset.  Otherwise the original source
        header is used, with its existing line breaks and/or binary data.

        """
        folded = self._fold(name, value, sanitize=(self.cte_type == '7bit'))
        return folded.encode('ascii', 'surrogateescape')

    def _fold(self, name, value, sanitize):
        parts = []
        parts.append('%s: ' % name)
        if isinstance(value, str):
            if _has_surrogates(value):
                if sanitize:
                    h = header.Header(value, charset=(_charset.UNKNOWN8BIT),
                      header_name=name)
                else:
                    parts.append(value)
                    h = None
            else:
                h = header.Header(value, header_name=name)
        else:
            h = value
        if h is not None:
            maxlinelen = 0
            if self.max_line_length is not None:
                maxlinelen = self.max_line_length
            parts.append(h.encode(linesep=(self.linesep), maxlinelen=maxlinelen))
        parts.append(self.linesep)
        return ''.join(parts)


compat32 = Compat32()