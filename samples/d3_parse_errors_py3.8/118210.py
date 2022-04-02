# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\mechanize\_form_controls.py
from __future__ import absolute_import
import random, re, sys, warnings
from io import BytesIO
from mimetypes import guess_type
from . import _request
from .polyglot import as_unicode, is_py2, iteritems, unicode_type, urlencode, urlparse, urlunparse
if is_py2:
    from cStringIO import StringIO
else:

    class StringIO(BytesIO):

        def write(self, x):
            if isinstance(x, str):
                x = x.encode('utf-8')
            BytesIO.write(self, x)


class Missing:
    pass


class LocateError(ValueError):
    pass


class AmbiguityError(LocateError):
    pass


class ControlNotFoundError(LocateError):
    pass


class ItemNotFoundError(LocateError):
    pass


class ItemCountError(ValueError):
    pass


_compress_re = re.compile('\\s+')

def deprecation(message, stack_offset=0):
    warnings.warn(message, DeprecationWarning, stacklevel=(3 + stack_offset))


def compress_whitespace(text):
    return re.sub('\\s+', ' ', text or '').strip()


def isstringlike--- This code section failed: ---

 L.  63         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'x'
                4  LOAD_GLOBAL              bytes
                6  LOAD_GLOBAL              unicode_type
                8  BUILD_TUPLE_2         2 
               10  CALL_FUNCTION_2       2  ''
               12  POP_JUMP_IF_FALSE    18  'to 18'

 L.  64        14  LOAD_CONST               True
               16  RETURN_VALUE     
             18_0  COME_FROM            12  '12'

 L.  65        18  SETUP_FINALLY        34  'to 34'

 L.  66        20  LOAD_FAST                'x'
               22  LOAD_STR                 ''
               24  BINARY_ADD       
               26  POP_TOP          

 L.  67        28  POP_BLOCK        
               30  LOAD_CONST               True
               32  RETURN_VALUE     
             34_0  COME_FROM_FINALLY    18  '18'

 L.  68        34  DUP_TOP          
               36  LOAD_GLOBAL              Exception
               38  COMPARE_OP               exception-match
               40  POP_JUMP_IF_FALSE    54  'to 54'
               42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L.  69        48  POP_EXCEPT       
               50  LOAD_CONST               False
               52  RETURN_VALUE     
             54_0  COME_FROM            40  '40'
               54  END_FINALLY      

Parse error at or near `DUP_TOP' instruction at offset 34


def choose_boundary():
    """Return a string usable as a multipart boundary."""
    nonce = ''.join((str(random.randint(0, sys.maxsize - 1)) for i in (0, 1, 2)))
    return '---------------------------' + nonce


class MimeWriter:
    __doc__ = "Generic MIME writer.\n\n    Methods:\n\n    __init__()\n    addheader()\n    flushheaders()\n    startbody()\n    startmultipartbody()\n    nextpart()\n    lastpart()\n\n    A MIME writer is much more primitive than a MIME parser.  It\n    doesn't seek around on the output file, and it doesn't use large\n    amounts of buffer space, so you have to write the parts in the\n    order they should occur on the output file.  It does buffer the\n    headers you add, allowing you to rearrange their order.\n\n    General usage is:\n\n    .. code-block:: python\n\n        f = <open the output file>\n        w = MimeWriter(f)\n        ...call w.addheader(key, value) 0 or more times...\n\n    followed by either:\n\n    .. code-block:: python\n\n        f = w.startbody(content_type)\n        ...call f.write(data) for body data...\n\n    or:\n\n    .. code-block:: python\n\n        w.startmultipartbody(subtype)\n        for each part:\n            subwriter = w.nextpart()\n            ...use the subwriter's methods to create the subpart...\n        w.lastpart()\n\n    The subwriter is another MimeWriter instance, and should be\n    treated in the same way as the toplevel MimeWriter.  This way,\n    writing recursive body parts is easy.\n\n    Warning: don't forget to call lastpart()!\n\n    XXX There should be more state so calls made in the wrong order\n    are detected.\n\n    Some special cases:\n\n    - startbody() just returns the file passed to the constructor;\n      but don't use this knowledge, as it may be changed.\n\n    - startmultipartbody() actually returns a file as well;\n      this can be used to write the initial 'if you can read this your\n      mailer is not MIME-aware' message.\n\n    - If you call flushheaders(), the headers accumulated so far are\n      written out (and forgotten); this is useful if you don't need a\n      body part at all, e.g. for a subpart of type message/rfc822\n      that's (mis)used to store some header-like information.\n\n    - Passing a keyword argument 'prefix=<flag>' to addheader(),\n      start*body() affects where the header is inserted; 0 means\n      append at the end, 1 means insert at the start; default is\n      append for addheader(), but insert for start*body(), which use\n      it to determine where the Content-type header goes.\n\n    "

    def __init__(self, fp, http_hdrs=None):
        self._http_hdrs = http_hdrs
        self._fp = fp
        self._headers = []
        self._boundary = []
        self._first_part = True

    def addheader(self, key, value, prefix=0, add_to_http_hdrs=0):
        """
        prefix is ignored if add_to_http_hdrs is true.
        """
        lines = value.split('\r\n')
        while True:
            if lines:
                del (lines[(-1)] or lines)[-1]

        while True:
            if lines:
                del (lines[0] or lines)[0]

        if add_to_http_hdrs:
            value = ''.join(lines)
            self._http_hdrs.append((key.capitalize(), value))
        else:
            for i in range(1, len(lines)):
                lines[i] = '    ' + lines[i].strip()
            else:
                value = '\r\n'.join(lines) + '\r\n'
                line = key.title() + ': ' + value
                if prefix:
                    self._headers.insert(0, line)
                else:
                    self._headers.append(line)

    def flushheaders(self):
        for line in self._headers:
            self._fp.write(line)
        else:
            self._headers = []

    def startbody(self, ctype=None, plist=[], prefix=1, add_to_http_hdrs=0, content_type=1):
        """
        prefix is ignored if add_to_http_hdrs is true.
        """
        if content_type:
            if ctype:
                for name, value in plist:
                    ctype = ctype + ';\r\n %s=%s' % (name, value)
                else:
                    self.addheader('Content-Type',
                      ctype,
                      prefix=prefix,
                      add_to_http_hdrs=add_to_http_hdrs)

        self.flushheaders()
        if not add_to_http_hdrs:
            self._fp.write('\r\n')
        self._first_part = True
        return self._fp

    def startmultipartbody(self, subtype, boundary=None, plist=[], prefix=1, add_to_http_hdrs=0, content_type=1):
        boundary = boundary or choose_boundary()
        self._boundary.append(boundary)
        return self.startbody(('multipart/' + subtype),
          ([('boundary', boundary)] + plist), prefix=prefix,
          add_to_http_hdrs=add_to_http_hdrs,
          content_type=content_type)

    def nextpart(self):
        boundary = self._boundary[(-1)]
        if self._first_part:
            self._first_part = False
        else:
            self._fp.write('\r\n')
        self._fp.write('--' + boundary + '\r\n')
        return self.__class__(self._fp)

    def lastpart(self):
        if self._first_part:
            self.nextpart()
        boundary = self._boundary.pop()
        self._fp.write('\r\n--' + boundary + '--\r\n')


class Label:

    def __init__(self, text, for_id=None):
        self.id = for_id
        self.text = compress_whitespace(text or '')

    def __repr__(self):
        return '<Label(id=%r, text=%r)>' % (self.id, self.text)

    __str__ = __repr__


def _get_label(attrs):
    text = attrs.get('__label')
    if text is not None:
        return Label(text)


class Control:
    __doc__ = "An HTML form control.\n\n    An HTMLForm contains a sequence of Controls.  The Controls in an HTMLForm\n    are accessed using the HTMLForm.find_control method or the\n    HTMLForm.controls attribute.\n\n    Control instances are usually constructed using the ParseFile /\n    ParseResponse functions.  If you use those functions, you can ignore the\n    rest of this paragraph.  A Control is only properly initialised after the\n    fixup method has been called.  In fact, this is only strictly necessary for\n    ListControl instances.  This is necessary because ListControls are built up\n    from ListControls each containing only a single item, and their initial\n    value(s) can only be known after the sequence is complete.\n\n    The types and values that are acceptable for assignment to the value\n    attribute are defined by subclasses.\n\n    If the disabled attribute is true, this represents the state typically\n    represented by browsers by 'greying out' a control.  If the disabled\n    attribute is true, the Control will raise AttributeError if an attempt is\n    made to change its value.  In addition, the control will not be considered\n    'successful' as defined by the W3C HTML 4 standard -- ie. it will\n    contribute no data to the return value of the HTMLForm.click* methods.  To\n    enable a control, set the disabled attribute to a false value.\n\n    If the readonly attribute is true, the Control will raise AttributeError if\n    an attempt is made to change its value.  To make a control writable, set\n    the readonly attribute to a false value.\n\n    All controls have the disabled and readonly attributes, not only those that\n    may have the HTML attributes of the same names.\n\n    On assignment to the value attribute, the following exceptions are raised:\n    TypeError, AttributeError (if the value attribute should not be assigned\n    to, because the control is disabled, for example) and ValueError.\n\n    If the name or value attributes are None, or the value is an empty list, or\n    if the control is disabled, the control is not successful.\n\n    Public attributes:\n\n    :ivar str type: string describing type of control (see the keys of the\n        HTMLForm.type2class dictionary for the allowable values) (readonly)\n    :ivar str name: name of control (readonly)\n    :ivar value: current value of control (subclasses may allow a single value,\n        a sequence of values, or either)\n    :ivar bool disabled: disabled state\n    :ivar bool readonly: readonly state\n    :ivar str id: value of id HTML attribute\n\n    "

    def __init__(self, type, name, attrs, index=None):
        """
        type: string describing type of control (see the keys of the
         HTMLForm.type2class dictionary for the allowable values)
        name: control name
        attrs: HTML attributes of control's HTML element

        """
        raise NotImplementedError()

    def add_to_form(self, form):
        self._form = form
        form.controls.append(self)

    def fixup(self):
        pass

    def is_of_kind(self, kind):
        raise NotImplementedError()

    def clear(self):
        raise NotImplementedError()

    def __getattr__(self, name):
        raise NotImplementedError()

    def __setattr__(self, name, value):
        raise NotImplementedError()

    def pairs(self):
        """Return list of (key, value) pairs suitable for passing to urlencode.
        """
        return [(
         k, v) for i, k, v in self._totally_ordered_pairs()]

    def _totally_ordered_pairs(self):
        """Return list of (key, value, index) tuples.

        Like pairs, but allows preserving correct ordering even where several
        controls are involved.

        """
        raise NotImplementedError()

    def _write_mime_data(self, mw, name, value):
        """Write data for a subitem of this control to a MimeWriter."""
        mw2 = mw.nextpart()
        mw2.addheader('Content-Disposition', 'form-data; name="%s"' % as_unicode(name), 1)
        f = mw2.startbody(prefix=0)
        f.write(value)

    def __str__(self):
        raise NotImplementedError()

    def get_labels(self):
        """Return all labels (Label instances) for this control.

        If the control was surrounded by a <label> tag, that will be the first
        label; all other labels, connected by 'for' and 'id', are in the order
        that appear in the HTML.

        """
        res = []
        if self._label:
            res.append(self._label)
        if self.id:
            res.extend(self._form._id_to_labels.get(self.id, ()))
        return res


class ScalarControl(Control):
    __doc__ = "Control whose value is not restricted to one of a prescribed set.\n\n    Some ScalarControls don't accept any value attribute.  Otherwise, takes a\n    single value, which must be string-like.\n\n    Additional read-only public attribute:\n\n    :ivar dict attrs: dictionary mapping the names of original HTML attributes\n        of the control to their values\n\n    "

    def __init__(self, type, name, attrs, index=None):
        self._index = index
        self._label = _get_label(attrs)
        self.__dict__['type'] = type.lower()
        self.__dict__['name'] = name
        self._value = attrs.get('value')
        self.disabled = 'disabled' in attrs
        self.readonly = 'readonly' in attrs
        self.id = attrs.get('id')
        self.attrs = dict(attrs)
        self._clicked = False
        self._urlparse = urlparse
        self._urlunparse = urlunparse

    def __getattr__(self, name):
        if name == 'value':
            return self.__dict__['_value']
        raise AttributeError("%s instance has no attribute '%s'" % (
         self.__class__.__name__, name))

    def __setattr__(self, name, value):
        if name == 'value':
            if not isstringlike(value):
                raise TypeError('must assign a string')
            elif self.readonly:
                raise AttributeError("control '%s' is readonly" % self.name)
            elif self.disabled:
                raise AttributeError("control '%s' is disabled" % self.name)
            self.__dict__['_value'] = value
        elif name in ('name', 'type'):
            raise AttributeError('%s attribute is readonly' % name)
        else:
            self.__dict__[name] = value

    def _totally_ordered_pairs(self):
        name = self.name
        value = self.value
        if not name is None:
            if value is None or (self.disabled):
                return []
            return [
             (
              self._index, name, value)]

    def clear(self):
        if self.readonly:
            raise AttributeError("control '%s' is readonly" % self.name)
        self.__dict__['_value'] = None

    def __str__(self):
        name = self.name
        value = self.value
        if name is None:
            name = '<None>'
        if value is None:
            value = '<None>'
        infos = []
        if self.disabled:
            infos.append('disabled')
        if self.readonly:
            infos.append('readonly')
        info = ', '.join(infos)
        if info:
            info = ' (%s)' % info
        return '<%s(%s=%s)%s>' % (self.__class__.__name__, name, value, info)


class TextControl(ScalarControl):
    __doc__ = 'Textual input control.\n\n    Covers HTML elements: INPUT/TEXT, INPUT/PASSWORD, INPUT/HIDDEN, TEXTAREA\n\n    '

    def __init__(self, type, name, attrs, index=None):
        ScalarControl.__init__(self, type, name, attrs, index)
        if self.type == 'hidden':
            self.readonly = True
        if self._value is None:
            self._value = ''

    def is_of_kind(self, kind):
        return kind == 'text'


class FileControl(ScalarControl):
    __doc__ = 'File upload with INPUT TYPE=FILE.\n\n    The value attribute of a FileControl is always None.  Use add_file instead.\n\n    Additional public method: :meth:`add_file`\n\n    '

    def __init__(self, type, name, attrs, index=None):
        ScalarControl.__init__(self, type, name, attrs, index)
        self._value = None
        self._upload_data = []

    def is_of_kind(self, kind):
        return kind == 'file'

    def clear(self):
        if self.readonly:
            raise AttributeError("control '%s' is readonly" % self.name)
        self._upload_data = []

    def __setattr__(self, name, value):
        if name in ('value', 'name', 'type'):
            raise AttributeError('%s attribute is readonly' % name)
        else:
            self.__dict__[name] = value

    def add_file(self, file_object, content_type=None, filename=None):
        """ Add data from the specified file to be uploaded. content_type and
        filename are sent in the HTTP headers if specified. """
        if not hasattr(file_object, 'read'):
            raise TypeError('file-like object must have read method')
        if content_type is not None:
            if not isstringlike(content_type):
                raise TypeError('content type must be None or string-like')
        if filename is not None:
            if not isstringlike(filename):
                raise TypeError('filename must be None or string-like')
            if content_type is None:
                if getattr(file_object, 'name', None):
                    content_type = guess_type(file_object.name)[0]
                content_type = content_type or 'application/octet-stream'
        self._upload_data.append((file_object, content_type, filename))

    def _totally_ordered_pairs(self):
        if self.name is None or (self.disabled):
            return []
        return [(self._index, self.name, '')]

    def _write_mime_data(self, mw, _name, _value):
        if len(self._upload_data) < 2:
            if len(self._upload_data) == 0:
                file_object = BytesIO()
                content_type = 'application/octet-stream'
                filename = ''
            else:
                file_object, content_type, filename = self._upload_data[0]
                if filename is None:
                    filename = ''
            mw2 = mw.nextpart()
            fn_part = '; filename="%s"' % filename
            disp = 'form-data; name="%s"%s' % (self.name, fn_part)
            mw2.addheader('Content-Disposition', disp, prefix=1)
            fh = mw2.startbody(content_type, prefix=0)
            fh.write(file_object.read())
        else:
            mw2 = mw.nextpart()
            disp = 'form-data; name="%s"' % self.name
            mw2.addheader('Content-Disposition', disp, prefix=1)
            fh = mw2.startmultipartbody('mixed', prefix=0)
            for file_object, content_type, filename in self._upload_data:
                mw3 = mw2.nextpart()
                if filename is None:
                    filename = ''
                else:
                    fn_part = '; filename="%s"' % filename
                    disp = 'file%s' % fn_part
                    mw3.addheader('Content-Disposition', disp, prefix=1)
                    fh2 = mw3.startbody(content_type, prefix=0)
                    fh2.write(file_object.read())
            else:
                mw2.lastpart()

    def __str__(self):
        name = self.name
        if name is None:
            name = '<None>'
        if not self._upload_data:
            value = '<No files added>'
        else:
            value = []
            for file, ctype, filename in self._upload_data:
                if filename is None:
                    value.append('<Unnamed file>')
                else:
                    value.append(filename)
                value = ', '.join(value)

        info = []
        if self.disabled:
            info.append('disabled')
        if self.readonly:
            info.append('readonly')
        info = ', '.join(info)
        if info:
            info = ' (%s)' % info
        return '<%s(%s=%s)%s>' % (self.__class__.__name__, name, value, info)


class IgnoreControl(ScalarControl):
    __doc__ = "Control that we're not interested in.\n\n    Covers html elements: INPUT/RESET, BUTTON/RESET, INPUT/BUTTON,\n    BUTTON/BUTTON\n\n    These controls are always unsuccessful, in the terminology of HTML 4 (ie.\n    they never require any information to be returned to the server).\n\n    BUTTON/BUTTON is used to generate events for script embedded in HTML.\n\n    The value attribute of IgnoreControl is always None.\n\n    "

    def __init__(self, type, name, attrs, index=None):
        ScalarControl.__init__(self, type, name, attrs, index)
        self._value = None

    def is_of_kind(self, kind):
        return False

    def __setattr__(self, name, value):
        if name == 'value':
            raise AttributeError("control '%s' is ignored, hence read-only" % self.name)
        elif name in ('name', 'type'):
            raise AttributeError('%s attribute is readonly' % name)
        else:
            self.__dict__[name] = value


class Item:

    def __init__(self, control, attrs, index=None):
        label = _get_label(attrs)
        self.__dict__.update({'name':attrs['value'], 
         '_labels':label and [label] or [], 
         'attrs':attrs, 
         '_control':control, 
         'disabled':'disabled' in attrs, 
         '_selected':False, 
         'id':attrs.get('id'), 
         '_index':index})
        control.items.append(self)

    def get_labels(self):
        """Return all labels (Label instances) for this item.

        For items that represent radio buttons or checkboxes, if the item was
        surrounded by a <label> tag, that will be the first label; all other
        labels, connected by 'for' and 'id', are in the order that appear in
        the HTML.

        For items that represent select options, if the option had a label
        attribute, that will be the first label.  If the option has contents
        (text within the option tags) and it is not the same as the label
        attribute (if any), that will be a label.  There is nothing in the
        spec to my knowledge that makes an option with an id unable to be the
        target of a label's for attribute, so those are included, if any, for
        the sake of consistency and completeness.

        """
        res = []
        res.extend(self._labels)
        if self.id:
            res.extend(self._control._form._id_to_labels.get(self.id, ()))
        return res

    def __getattr__(self, name):
        if name == 'selected':
            return self._selected
        raise AttributeError(name)

    def __setattr__(self, name, value):
        if name == 'selected':
            self._control._set_selected_state(self, value)
        elif name == 'disabled':
            self.__dict__['disabled'] = bool(value)
        else:
            raise AttributeError(name)

    def __str__(self):
        res = self.name
        if self.selected:
            res = '*' + res
        if self.disabled:
            res = '(%s)' % res
        return res

    def __repr__(self):
        attrs = [
         (
          'name', self.name), ('id', self.id)] + list(iteritems(self.attrs))
        return '<%s %s>' % (self.__class__.__name__,
         ' '.join(['%s=%r' % (k, v) for k, v in attrs]))


def disambiguate(items, nr, **kwds):
    msgs = []
    for key, value in iteritems(kwds):
        msgs.append('%s=%r' % (key, value))
    else:
        msg = ' '.join(msgs)
        if not items:
            raise ItemNotFoundError(msg)
        if nr is None:
            if len(items) > 1:
                raise AmbiguityError(msg)
            nr = 0
        if len(items) <= nr:
            raise ItemNotFoundError(msg)
        return items[nr]


class ListControl(Control):
    __doc__ = 'Control representing a sequence of items.\n\n    The value attribute of a ListControl represents the successful list items\n    in the control.  The successful list items are those that are selected and\n    not disabled.\n\n    ListControl implements both list controls that take a length-1 value\n    (single-selection) and those that take length >1 values\n    (multiple-selection).\n\n    ListControls accept sequence values only.  Some controls only accept\n    sequences of length 0 or 1 (RADIO, and single-selection SELECT).\n    In those cases, ItemCountError is raised if len(sequence) > 1.  CHECKBOXes\n    and multiple-selection SELECTs (those having the "multiple" HTML attribute)\n    accept sequences of any length.\n\n    Note the following mistake:\n\n    .. code-block:: python\n\n        control.value = some_value\n        assert control.value == some_value    # not necessarily true\n\n    The reason for this is that the value attribute always gives the list items\n    in the order they were listed in the HTML.\n\n    ListControl items can also be referred to by their labels instead of names.\n    Use the label argument to .get(), and the .set_value_by_label(),\n    .get_value_by_label() methods.\n\n    Note that, rather confusingly, though SELECT controls are represented in\n    HTML by SELECT elements (which contain OPTION elements, representing\n    individual list items), CHECKBOXes and RADIOs are not represented by *any*\n    element.  Instead, those controls are represented by a collection of INPUT\n    elements.  For example, this is a SELECT control, named "control1"::\n\n        <select name="control1">\n        <option>foo</option>\n        <option value="1">bar</option>\n        </select>\n\n    and this is a CHECKBOX control, named "control2"::\n\n        <input type="checkbox" name="control2" value="foo" id="cbe1">\n        <input type="checkbox" name="control2" value="bar" id="cbe2">\n\n    The id attribute of a CHECKBOX or RADIO ListControl is always that of its\n    first element (for example, "cbe1" above).\n\n\n    Additional read-only public attribute: multiple.\n\n    '
    _label = None

    def __init__(self, type, name, attrs={}, select_default=False, called_as_base_class=False, index=None):
        """
        select_default: for RADIO and multiple-selection SELECT controls, pick
         the first item as the default if no 'selected' HTML attribute is
         present

        """
        if not called_as_base_class:
            raise NotImplementedError()
        self.__dict__['type'] = type.lower()
        self.__dict__['name'] = name
        self._value = attrs.get('value')
        self.disabled = False
        self.readonly = False
        self.id = attrs.get('id')
        self._closed = False
        self.items = []
        self._form = None
        self._select_default = select_default
        self._clicked = False

    def clear(self):
        self.value = []

    def is_of_kind(self, kind):
        if kind == 'list':
            return True
        if kind == 'multilist':
            return bool(self.multiple)
        if kind == 'singlelist':
            return not self.multiple
        return False

    def get_items--- This code section failed: ---

 L. 863         0  LOAD_FAST                'name'
                2  LOAD_CONST               None
                4  COMPARE_OP               is-not
                6  POP_JUMP_IF_FALSE    24  'to 24'
                8  LOAD_GLOBAL              isstringlike
               10  LOAD_FAST                'name'
               12  CALL_FUNCTION_1       1  ''
               14  POP_JUMP_IF_TRUE     24  'to 24'

 L. 864        16  LOAD_GLOBAL              TypeError
               18  LOAD_STR                 'item name must be string-like'
               20  CALL_FUNCTION_1       1  ''
               22  RAISE_VARARGS_1       1  'exception instance'
             24_0  COME_FROM            14  '14'
             24_1  COME_FROM             6  '6'

 L. 865        24  LOAD_FAST                'label'
               26  LOAD_CONST               None
               28  COMPARE_OP               is-not
               30  POP_JUMP_IF_FALSE    48  'to 48'
               32  LOAD_GLOBAL              isstringlike
               34  LOAD_FAST                'label'
               36  CALL_FUNCTION_1       1  ''
               38  POP_JUMP_IF_TRUE     48  'to 48'

 L. 866        40  LOAD_GLOBAL              TypeError
               42  LOAD_STR                 'item label must be string-like'
               44  CALL_FUNCTION_1       1  ''
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            38  '38'
             48_1  COME_FROM            30  '30'

 L. 867        48  LOAD_FAST                'id'
               50  LOAD_CONST               None
               52  COMPARE_OP               is-not
               54  POP_JUMP_IF_FALSE    72  'to 72'
               56  LOAD_GLOBAL              isstringlike
               58  LOAD_FAST                'id'
               60  CALL_FUNCTION_1       1  ''
               62  POP_JUMP_IF_TRUE     72  'to 72'

 L. 868        64  LOAD_GLOBAL              TypeError
               66  LOAD_STR                 'item id must be string-like'
               68  CALL_FUNCTION_1       1  ''
               70  RAISE_VARARGS_1       1  'exception instance'
             72_0  COME_FROM            62  '62'
             72_1  COME_FROM            54  '54'

 L. 869        72  BUILD_LIST_0          0 
               74  STORE_FAST               'items'

 L. 870        76  LOAD_FAST                'self'
               78  LOAD_ATTR                items
               80  GET_ITER         
             82_0  COME_FROM           186  '186'
             82_1  COME_FROM           174  '174'
             82_2  COME_FROM           154  '154'
             82_3  COME_FROM           116  '116'
             82_4  COME_FROM            96  '96'
               82  FOR_ITER            188  'to 188'
               84  STORE_FAST               'o'

 L. 871        86  LOAD_FAST                'exclude_disabled'
               88  POP_JUMP_IF_FALSE    98  'to 98'
               90  LOAD_FAST                'o'
               92  LOAD_ATTR                disabled
               94  POP_JUMP_IF_FALSE    98  'to 98'

 L. 872        96  JUMP_BACK            82  'to 82'
             98_0  COME_FROM            94  '94'
             98_1  COME_FROM            88  '88'

 L. 873        98  LOAD_FAST                'name'
              100  LOAD_CONST               None
              102  COMPARE_OP               is-not
              104  POP_JUMP_IF_FALSE   118  'to 118'
              106  LOAD_FAST                'o'
              108  LOAD_ATTR                name
              110  LOAD_FAST                'name'
              112  COMPARE_OP               !=
              114  POP_JUMP_IF_FALSE   118  'to 118'

 L. 874       116  JUMP_BACK            82  'to 82'
            118_0  COME_FROM           114  '114'
            118_1  COME_FROM           104  '104'

 L. 875       118  LOAD_FAST                'label'
              120  LOAD_CONST               None
              122  COMPARE_OP               is-not
              124  POP_JUMP_IF_FALSE   156  'to 156'

 L. 876       126  LOAD_FAST                'o'
              128  LOAD_METHOD              get_labels
              130  CALL_METHOD_0         0  ''
              132  GET_ITER         
            134_0  COME_FROM           152  '152'
            134_1  COME_FROM           146  '146'
              134  FOR_ITER            154  'to 154'
              136  STORE_FAST               'l'

 L. 877       138  LOAD_FAST                'label'
              140  LOAD_FAST                'l'
              142  LOAD_ATTR                text
              144  COMPARE_OP               in
              146  POP_JUMP_IF_FALSE_BACK   134  'to 134'

 L. 878       148  POP_TOP          
              150  BREAK_LOOP          156  'to 156'
              152  JUMP_BACK           134  'to 134'
            154_0  COME_FROM           134  '134'

 L. 880       154  JUMP_BACK            82  'to 82'
            156_0  COME_FROM           150  '150'
            156_1  COME_FROM           124  '124'

 L. 881       156  LOAD_FAST                'id'
              158  LOAD_CONST               None
              160  COMPARE_OP               is-not
              162  POP_JUMP_IF_FALSE   176  'to 176'
              164  LOAD_FAST                'o'
              166  LOAD_ATTR                id
              168  LOAD_FAST                'id'
              170  COMPARE_OP               !=
              172  POP_JUMP_IF_FALSE   176  'to 176'

 L. 882       174  JUMP_BACK            82  'to 82'
            176_0  COME_FROM           172  '172'
            176_1  COME_FROM           162  '162'

 L. 883       176  LOAD_FAST                'items'
              178  LOAD_METHOD              append
              180  LOAD_FAST                'o'
              182  CALL_METHOD_1         1  ''
              184  POP_TOP          
              186  JUMP_BACK            82  'to 82'
            188_0  COME_FROM            82  '82'

 L. 884       188  LOAD_FAST                'items'
              190  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 188

    def get(self, name=None, label=None, id=None, nr=None, exclude_disabled=False):
        """Return item by name or label, disambiguating if necessary with nr.

        All arguments must be passed by name, with the exception of 'name',
        which may be used as a positional argument.

        If name is specified, then the item must have the indicated name.

        If label is specified, then the item must have a label whose
        whitespace-compressed, stripped, text substring-matches the indicated
        label string (e.g. label="please choose" will match
        "  Do  please  choose an item ").

        If id is specified, then the item must have the indicated id.

        nr is an optional 0-based index of the items matching the query.

        If nr is the default None value and more than item is found, raises
        AmbiguityError.

        If no item is found, or if items are found but nr is specified and not
        found, raises ItemNotFoundError.

        Optionally excludes disabled items.

        """
        items = self.get_items(name, label, id, exclude_disabled)
        return disambiguate(items, nr, name=name, label=label, id=id)

    def _get(self, name, by_label=False, nr=None, exclude_disabled=False):
        if by_label:
            name, label = None, name
        else:
            name, label = name, None
        return self.get(name, label, nr, exclude_disabled)

    def toggle(self, name, by_label=False, nr=None):
        """Deprecated: given a name or label and optional disambiguating index
        nr, toggle the matching item's selection.

        Selecting items follows the behavior described in the docstring of the
        'get' method.

        if the item is disabled, or this control is disabled or readonly,
        raise AttributeError.

        """
        deprecation('item = control.get(...); item.selected = not item.selected')
        o = self._get(name, by_label, nr)
        self._set_selected_state(o, not o.selected)

    def set(self, selected, name, by_label=False, nr=None):
        """Deprecated: given a name or label and optional disambiguating index
        nr, set the matching item's selection to the bool value of selected.

        Selecting items follows the behavior described in the docstring of the
        'get' method.

        if the item is disabled, or this control is disabled or readonly,
        raise AttributeError.

        """
        deprecation('control.get(...).selected = <boolean>')
        self._set_selected_state(self._get(name, by_label, nr), selected)

    def _set_selected_state(self, item, action):
        if self.disabled:
            raise AttributeError("control '%s' is disabled" % self.name)
        if self.readonly:
            raise AttributeError("control '%s' is readonly" % self.name)
        action == bool(action)
        if item.disabled:
            raise AttributeError('item is disabled')
        if self.multiple:
            item.__dict__['_selected'] = action
        elif not action:
            item.__dict__['_selected'] = False
        else:
            for o in self.items:
                o.__dict__['_selected'] = False
            else:
                item.__dict__['_selected'] = True

    def toggle_single(self, by_label=None):
        """Deprecated: toggle the selection of the single item in this control.

        Raises ItemCountError if the control does not contain only one item.

        by_label argument is ignored, and included only for backwards
        compatibility.

        """
        deprecation('control.items[0].selected = not control.items[0].selected')
        if len(self.items) != 1:
            raise ItemCountError("'%s' is not a single-item control" % self.name)
        item = self.items[0]
        self._set_selected_state(item, not item.selected)

    def set_single(self, selected, by_label=None):
        """Deprecated: set the selection of the single item in this control.

        Raises ItemCountError if the control does not contain only one item.

        by_label argument is ignored, and included only for backwards
        compatibility.

        """
        deprecation('control.items[0].selected = <boolean>')
        if len(self.items) != 1:
            raise ItemCountError("'%s' is not a single-item control" % self.name)
        self._set_selected_state(self.items[0], selected)

    def get_item_disabled(self, name, by_label=False, nr=None):
        """Get disabled state of named list item in a ListControl."""
        deprecation('control.get(...).disabled')
        return self._get(name, by_label, nr).disabled

    def set_item_disabled(self, disabled, name, by_label=False, nr=None):
        """Set disabled state of named list item in a ListControl.

        :arg disabled: boolean disabled state

        """
        deprecation('control.get(...).disabled = <boolean>')
        self._get(name, by_label, nr).disabled = disabled

    def set_all_items_disabled(self, disabled):
        """Set disabled state of all list items in a ListControl.

        :arg disabled: boolean disabled state

        """
        for o in self.items:
            o.disabled = disabled

    def get_item_attrs(self, name, by_label=False, nr=None):
        """Return dictionary of HTML attributes for a single ListControl item.

        The HTML element types that describe list items are: OPTION for SELECT
        controls, INPUT for the rest.  These elements have HTML attributes that
        you may occasionally want to know about -- for example, the "alt" HTML
        attribute gives a text string describing the item (graphical browsers
        usually display this as a tooltip).

        The returned dictionary maps HTML attribute names to values.  The names
        and values are taken from the original HTML.

        """
        deprecation('control.get(...).attrs')
        return self._get(name, by_label, nr).attrs

    def close_control(self):
        self._closed = True

    def add_to_form(self, form):
        if not self._form is None:
            assert form == self._form, "can't add control to more than one form"
        self._form = form
        if self.name is None:
            Control.add_to_form(self, form)
        else:
            for ii in range(len(form.controls) - 1, -1, -1):
                control = form.controls[ii]
                if control.name == self.name:
                    if control.type == self.type:
                        if control._closed:
                            Control.add_to_form(self, form)
                        else:
                            control.merge_control(self)
                        break
            else:
                Control.add_to_form(self, form)

    def merge_control(self, control):
        assert bool(control.multiple) == bool(self.multiple)
        self.items.extend(control.items)

    def fixup(self):
        """
        ListControls are built up from component list items (which are also
        ListControls) during parsing.  This method should be called after all
        items have been added.  See :class:`mechanize.ListControl` for the
        reason this is required.

        """
        for o in self.items:
            o.__dict__['_control'] = self

    def __getattr__(self, name):
        if name == 'value':
            if self.name is None:
                return []
            return [o.name for o in self.items if o.selected if not o.disabled]
        raise AttributeError("%s instance has no attribute '%s'" % (
         self.__class__.__name__, name))

    def __setattr__(self, name, value):
        if name == 'value':
            if self.disabled:
                raise AttributeError("control '%s' is disabled" % self.name)
            if self.readonly:
                raise AttributeError("control '%s' is readonly" % self.name)
            self._set_value(value)
        elif name in ('name', 'type', 'multiple'):
            raise AttributeError('%s attribute is readonly' % name)
        else:
            self.__dict__[name] = value

    def _set_value(self, value):
        if value is None or (isstringlike(value)):
            raise TypeError('ListControl, must set a sequence')
        if not value:
            for o in self.items:
                if not o.disabled:
                    o.selected = False

        elif self.multiple:
            self._multiple_set_value(value)
        elif len(value) > 1:
            raise ItemCountError('single selection list, must set sequence of length 0 or 1')
        else:
            self._single_set_value(value)

    def _get_items(self, name, target=1):
        all_items = self.get_items(name)
        items = [o for o in all_items if not o.disabled]
        if len(items) < target:
            if len(all_items) < target:
                raise ItemNotFoundError('insufficient items with name %r' % name)
            else:
                raise AttributeError('insufficient non-disabled items with name %s' % name)
        on = []
        off = []
        for o in items:
            if o.selected:
                on.append(o)
            else:
                off.append(o)
        else:
            return (
             on, off)

    def _single_set_value(self, value):
        assert len(value) == 1
        on, off = self._get_items(value[0])
        assert len(on) <= 1
        if not on:
            off[0].selected = True

    def _multiple_set_value(self, value):
        turn_on = []
        turn_off = [item for item in self.items if item.selected if not item.disabled]
        names = {}
        for nn in value:
            names[nn] = names.setdefault(nn, 0) + 1
        else:
            for name, count in iteritems(names):
                on, off = self._get_items(name, count)
                for i in range(count):
                    if on:
                        item = on[0]
                        del on[0]
                        del turn_off[turn_off.index(item)]
                    else:
                        item = off[0]
                        del off[0]
                        turn_on.append(item)

            else:
                for item in turn_off:
                    item.selected = False
                else:
                    for item in turn_on:
                        item.selected = True

    def set_value_by_label(self, value):
        """Set the value of control by item labels.

        value is expected to be an iterable of strings that are substrings of
        the item labels that should be selected.  Before substring matching is
        performed, the original label text is whitespace-compressed
        (consecutive whitespace characters are converted to a single space
        character) and leading and trailing whitespace is stripped. Ambiguous
        labels: it will not complain as long as all ambiguous labels share the
        same item name (e.g. OPTION value).

        """
        if isstringlike(value):
            raise TypeError(value)
        if not self.multiple:
            if len(value) > 1:
                raise ItemCountError('single selection list, must set sequence of length 0 or 1')
        items = []
        for nn in value:
            found = self.get_items(label=nn)
            if len(found) > 1:
                opt_name = found[0].name
                if [o for o in found[1:] if o.name != opt_name]:
                    raise AmbiguityError(nn)
            for o in found:
                if o not in items:
                    items.append(o)
                    break
            else:
                raise ItemNotFoundError(nn)

        else:
            self.value = []
            for o in items:
                o.selected = True

    def get_value_by_label(self):
        """Return the value of the control as given by normalized labels."""
        res = []
        for o in self.items:
            if not o.disabled:
                if o.selected:
                    for l in o.get_labels():
                        if l.text:
                            res.append(l.text)
                            break
                    else:
                        res.append(None)

        else:
            return res

    def possible_items(self, by_label=False):
        """Deprecated: return the names or labels of all possible items.

        Includes disabled items, which may be misleading for some use cases.

        """
        deprecation('[item.name for item in self.items]')
        if by_label:
            res = []
            for o in self.items:
                for l in o.get_labels():
                    if l.text:
                        res.append(l.text)
                        break
                    res.append(None)
                else:
                    return res

            return [o.name for o in self.items]

    def _totally_ordered_pairs(self):
        if self.disabled or (self.name is None):
            return []
        return [(
         o._index, self.name, o.name) for o in self.items if o.selected if not o.disabled]

    def __str__(self):
        name = self.name
        if name is None:
            name = '<None>'
        display = [str(o) for o in self.items]
        infos = []
        if self.disabled:
            infos.append('disabled')
        if self.readonly:
            infos.append('readonly')
        info = ', '.join(infos)
        if info:
            info = ' (%s)' % info
        return '<%s(%s=[%s])%s>' % (self.__class__.__name__, name,
         ', '.join(display), info)


class RadioControl(ListControl):
    __doc__ = '\n    Covers:\n\n    INPUT/RADIO\n\n    '

    def __init__(self, type, name, attrs, select_default=False, index=None):
        attrs.setdefault('value', 'on')
        ListControl.__init__(self,
          type,
          name,
          attrs,
          select_default,
          called_as_base_class=True,
          index=index)
        self.__dict__['multiple'] = False
        o = Item(self, attrs, index)
        o.__dict__['_selected'] = 'checked' in attrs

    def fixup(self):
        ListControl.fixup(self)
        found = [o for o in self.items if o.selected if not o.disabled]
        if not found:
            if self._select_default:
                for o in self.items:
                    if not o.disabled:
                        o.selected = True
                        break

        else:
            for o in found[:-1]:
                o.selected = False

    def get_labels(self):
        return []


class CheckboxControl(ListControl):
    __doc__ = '\n    Covers:\n\n    INPUT/CHECKBOX\n\n    '

    def __init__(self, type, name, attrs, select_default=False, index=None):
        attrs.setdefault('value', 'on')
        ListControl.__init__(self,
          type,
          name,
          attrs,
          select_default,
          called_as_base_class=True,
          index=index)
        self.__dict__['multiple'] = True
        o = Item(self, attrs, index)
        o.__dict__['_selected'] = 'checked' in attrs

    def get_labels(self):
        return []


class SelectControl(ListControl):
    __doc__ = '\n    Covers:\n\n    SELECT (and OPTION)\n\n\n    OPTION \'values\', in HTML parlance, are Item \'names\' in mechanize parlance.\n\n    SELECT control values and labels are subject to some messy defaulting\n    rules.  For example, if the HTML representation of the control is::\n\n        <SELECT name=year>\n            <OPTION value=0 label="2002">current year</OPTION>\n            <OPTION value=1>2001</OPTION>\n            <OPTION>2000</OPTION>\n        </SELECT>\n\n    The items, in order, have labels "2002", "2001" and "2000", whereas their\n    names (the OPTION values) are "0", "1" and "2000" respectively.  Note that\n    the value of the last OPTION in this example defaults to its contents, as\n    specified by RFC 1866, as do the labels of the second and third OPTIONs.\n\n    The OPTION labels are sometimes more meaningful than the OPTION values,\n    which can make for more maintainable code.\n\n    Additional read-only public attribute: attrs\n\n    The attrs attribute is a dictionary of the original HTML attributes of the\n    SELECT element.  Other ListControls do not have this attribute, because in\n    other cases the control as a whole does not correspond to any single HTML\n    element.  control.get(...).attrs may be used as usual to get at the HTML\n    attributes of the HTML elements corresponding to individual list items (for\n    SELECT controls, these are OPTION elements).\n\n    Another special case is that the Item.attrs dictionaries have a special key\n    "contents" which does not correspond to any real HTML attribute, but rather\n    contains the contents of the OPTION element::\n\n        <OPTION>this bit</OPTION>\n\n    '

    def __init__(self, type, name, attrs, select_default=False, index=None):
        self.attrs = dict(attrs['__select'])
        self.__dict__['_label'] = _get_label(self.attrs)
        self.__dict__['id'] = self.attrs.get('id')
        self.__dict__['multiple'] = 'multiple' in self.attrs
        contents = attrs.get('contents')
        attrs = dict(attrs)
        del attrs['__select']
        ListControl.__init__(self,
          type,
          name,
          (self.attrs),
          select_default,
          called_as_base_class=True,
          index=index)
        self.disabled = 'disabled' in self.attrs
        self.readonly = 'readonly' in self.attrs
        if 'value' in attrs:
            o = Item(self, attrs, index)
            o.__dict__['_selected'] = 'selected' in attrs
            label = attrs.get('label')
            if label:
                o._labels.append(Label(label))
                if not contents or contents != label:
                    o._labels.append(Label(contents))
            elif contents:
                o._labels.append(Label(contents))

    def fixup(self):
        ListControl.fixup(self)
        found = [o for o in self.items if o.selected]
        if not found:
            if not self.multiple or self._select_default:
                for o in self.items:
                    if not o.disabled:
                        was_disabled = self.disabled
                        self.disabled = False
                        try:
                            o.selected = True
                        finally:
                            o.disabled = was_disabled

                        break

        else:
            for o in self.multiple or found[:-1]:
                o.selected = False


class SubmitControl(ScalarControl):
    __doc__ = '\n    Covers:\n\n    INPUT/SUBMIT\n    BUTTON/SUBMIT\n\n    '

    def __init__(self, type, name, attrs, index=None):
        ScalarControl.__init__(self, type, name, attrs, index)
        if self.value is None:
            self.__dict__['_value'] = ''
        self.readonly = True

    def get_labels(self):
        res = []
        if self.value:
            res.append(Label(self.value))
        res.extend(ScalarControl.get_labels(self))
        return res

    def is_of_kind(self, kind):
        return kind == 'clickable'

    def _click(self, form, coord, return_type, request_class=_request.Request):
        self._clicked = coord
        r = form._switch_click(return_type, request_class)
        self._clicked = False
        return r

    def _totally_ordered_pairs(self):
        if not self._clicked:
            return []
        return ScalarControl._totally_ordered_pairs(self)


class ImageControl(SubmitControl):
    __doc__ = '\n    Covers:\n\n    INPUT/IMAGE\n\n    Coordinates are specified using one of the HTMLForm.click* methods.\n\n    '

    def __init__(self, type, name, attrs, index=None):
        SubmitControl.__init__(self, type, name, attrs, index)
        self.readonly = False

    def _totally_ordered_pairs(self):
        clicked = self._clicked
        if not (self.disabled or clicked):
            return []
        name = self.name
        if name is None:
            return []
        pairs = [(self._index, '%s.x' % name, str(clicked[0])),
         (
          self._index + 1, '%s.y' % name, str(clicked[1]))]
        value = self._value
        if value:
            pairs.append((self._index + 2, name, value))
        return pairs

    get_labels = ScalarControl.get_labels


class PasswordControl(TextControl):
    pass


class HiddenControl(TextControl):
    pass


class TextareaControl(TextControl):
    pass


class SubmitButtonControl(SubmitControl):
    pass


def is_listcontrol(control):
    return control.is_of_kind('list')


class HTMLForm:
    __doc__ = '\n    Represents a single HTML <form> ... </form> element.\n\n    A form consists of a sequence of controls that usually have names, and\n    which can take on various values.  The values of the various types of\n    controls represent variously: text, zero-or-one-of-many or many-of-many\n    choices, and files to be uploaded.  Some controls can be clicked on to\n    submit the form, and clickable controls\' values sometimes include the\n    coordinates of the click.\n\n    Forms can be filled in with data to be returned to the server, and then\n    submitted, using the click method to generate a request object suitable for\n    passing to :func:`mechanize.urlopen` (or the click_request_data or\n    click_pairs methods for integration with third-party code).\n\n    Usually, HTMLForm instances are not created directly.  Instead, they are\n    automatically created when visting a page with a mechanize Browser.  If you\n    do construct HTMLForm objects yourself, however, note that an HTMLForm\n    instance is only properly initialised after the fixup method has been\n    called.  See :class:`mechanize.ListControl` for the reason this is\n    required.\n\n    Indexing a form (form["control_name"]) returns the named Control\'s value\n    attribute.  Assignment to a form index (form["control_name"] = something)\n    is equivalent to assignment to the named Control\'s value attribute.  If you\n    need to be more specific than just supplying the control\'s name, use the\n    set_value and get_value methods.\n\n    ListControl values are lists of item names (specifically, the names of the\n    items that are selected and not disabled, and hence are "successful" -- ie.\n    cause data to be returned to the server).  The list item\'s name is the\n    value of the corresponding HTML element\'s"value" attribute.\n\n    Example::\n\n      <INPUT type="CHECKBOX" name="cheeses" value="leicester"></INPUT>\n      <INPUT type="CHECKBOX" name="cheeses" value="cheddar"></INPUT>\n\n    defines a CHECKBOX control with name "cheeses" which has two items, named\n    "leicester" and "cheddar".\n\n    Another example::\n\n      <SELECT name="more_cheeses">\n        <OPTION>1</OPTION>\n        <OPTION value="2" label="CHEDDAR">cheddar</OPTION>\n      </SELECT>\n\n    defines a SELECT control with name "more_cheeses" which has two items,\n    named "1" and "2" (because the OPTION element\'s value HTML attribute\n    defaults to the element contents -- see :class:`mechanize.SelectControl`\n    for more on these defaulting rules).\n\n    To select, deselect or otherwise manipulate individual list items, use the\n    :meth:`mechanize.HTMLForm.find_control()` and\n    :meth:`mechanize.ListControl.get()` methods.  To set the whole value, do as\n    for any other control: use indexing or the `set_value/get_value` methods.\n\n    Example:\n\n    .. code-block:: python\n\n        # select *only* the item named "cheddar"\n        form["cheeses"] = ["cheddar"]\n        # select "cheddar", leave other items unaffected\n        form.find_control("cheeses").get("cheddar").selected = True\n\n    Some controls (RADIO and SELECT without the multiple attribute) can only\n    have zero or one items selected at a time.  Some controls (CHECKBOX and\n    SELECT with the multiple attribute) can have multiple items selected at a\n    time.  To set the whole value of a ListControl, assign a sequence to a form\n    index:\n\n    .. code-block:: python\n\n        form["cheeses"] = ["cheddar", "leicester"]\n\n    If the ListControl is not multiple-selection, the assigned list must be of\n    length one.\n\n    To check if a control has an item, if an item is selected, or if an item is\n    successful (selected and not disabled), respectively:\n\n    .. code-block:: python\n\n        "cheddar" in [item.name for item in form.find_control("cheeses").items]\n        "cheddar" in [item.name for item in form.find_control("cheeses").items\n                        and item.selected]\n        "cheddar" in form["cheeses"]\n        # or\n        "cheddar" in form.get_value("cheeses")\n\n    Note that some list items may be disabled (see below).\n\n    Note the following mistake:\n\n    .. code-block:: python\n\n        form[control_name] = control_value\n        assert form[control_name] == control_value  # not necessarily true\n\n    The reason for this is that form[control_name] always gives the list items\n    in the order they were listed in the HTML.\n\n    List items (hence list values, too) can be referred to in terms of list\n    item labels rather than list item names using the appropriate label\n    arguments.  Note that each item may have several labels.\n\n    The question of default values of OPTION contents, labels and values is\n    somewhat complicated: see :class:`mechanize.SelectControl` and\n    :meth:`mechanize.ListControl.get_item_attrs()` if you think you need to\n    know.\n\n    Controls can be disabled or readonly.  In either case, the control\'s value\n    cannot be changed until you clear those flags (see example below).\n    Disabled is the state typically represented by browsers by \'greying out\' a\n    control.  Disabled controls are not \'successful\' -- they don\'t cause data\n    to get returned to the server.  Readonly controls usually appear in\n    browsers as read-only text boxes.  Readonly controls are successful.  List\n    items can also be disabled.  Attempts to select or deselect disabled items\n    fail with AttributeError.\n\n    If a lot of controls are readonly, it can be useful to do this:\n\n    .. code-block:: python\n\n        form.set_all_readonly(False)\n\n    To clear a control\'s value attribute, so that it is not successful (until a\n    value is subsequently set):\n\n    .. code-block:: python\n\n        form.clear("cheeses")\n\n    More examples:\n\n    .. code-block:: python\n\n        control = form.find_control("cheeses")\n        control.disabled = False\n        control.readonly = False\n        control.get("gruyere").disabled = True\n        control.items[0].selected = True\n\n    See the various Control classes for further documentation.  Many methods\n    take name, type, kind, id, label and nr arguments to specify the control to\n    be operated on: see :meth:`mechanize.HTMLForm.find_control()`.\n\n    ControlNotFoundError (subclass of ValueError) is raised if the specified\n    control can\'t be found.  This includes occasions where a non-ListControl\n    is found, but the method (set, for example) requires a ListControl.\n    ItemNotFoundError (subclass of ValueError) is raised if a list item can\'t\n    be found.  ItemCountError (subclass of ValueError) is raised if an attempt\n    is made to select more than one item and the control doesn\'t allow that, or\n    set/get_single are called and the control contains more than one item.\n    AttributeError is raised if a control or item is readonly or disabled and\n    an attempt is made to alter its value.\n\n    Security note: Remember that any passwords you store in HTMLForm instances\n    will be saved to disk in the clear if you pickle them (directly or\n    indirectly).  The simplest solution to this is to avoid pickling HTMLForm\n    objects.  You could also pickle before filling in any password, or just set\n    the password to "" before pickling.\n\n\n    Public attributes:\n\n    :ivar action: full (absolute URI) form action\n    :ivar method: "GET" or "POST"\n    :ivar enctype: form transfer encoding MIME type\n    :ivar name: name of form (None if no name was specified)\n    :ivar attrs: dictionary mapping original HTML form attributes to their\n        values\n    :ivar controls: list of Control instances; do not alter this list\n        (instead, call form.new_control to make a Control and add it to the\n        form, or control.add_to_form if you already have a Control instance)\n\n\n\n    Methods for form filling:\n\n    Most of the these methods have very similar arguments.  See\n    :meth:`mechanize.HTMLForm.find_control()` for details of the name, type,\n    kind, label and nr arguments.\n\n    .. code-block:: python\n\n        def find_control(self,\n                        name=None, type=None, kind=None, id=None,\n                        predicate=None, nr=None, label=None)\n\n        get_value(name=None, type=None, kind=None, id=None, nr=None,\n                by_label=False,  # by_label is deprecated\n                label=None)\n        set_value(value,\n                name=None, type=None, kind=None, id=None, nr=None,\n                by_label=False,  # by_label is deprecated\n                label=None)\n\n        clear_all()\n        clear(name=None, type=None, kind=None, id=None, nr=None, label=None)\n\n        set_all_readonly(readonly)\n\n\n    Method applying only to FileControls:\n\n    .. code-block:: python\n\n        add_file(file_object,\n             content_type="application/octet-stream", filename=None,\n             name=None, id=None, nr=None, label=None)\n\n\n    Methods applying only to clickable controls:\n\n    .. code-block:: python\n\n        click(name=None, type=None, id=None, nr=0, coord=(1,1), label=None)\n        click_request_data(name=None, type=None, id=None, nr=0, coord=(1,1),\n                        label=None)\n        click_pairs(name=None, type=None, id=None, nr=0, coord=(1,1),\n                        label=None)\n\n    '
    type2class = {'text':TextControl, 
     'password':PasswordControl, 
     'hidden':HiddenControl, 
     'textarea':TextareaControl, 
     'file':FileControl, 
     'button':IgnoreControl, 
     'buttonbutton':IgnoreControl, 
     'reset':IgnoreControl, 
     'resetbutton':IgnoreControl, 
     'submit':SubmitControl, 
     'submitbutton':SubmitButtonControl, 
     'image':ImageControl, 
     'radio':RadioControl, 
     'checkbox':CheckboxControl, 
     'select':SelectControl}

    def __init__(self, action, method='GET', enctype='application/x-www-form-urlencoded', name=None, attrs=None, request_class=_request.Request, forms=None, labels=None, id_to_labels=None, encoding=None):
        """
        In the usual case, use ParseResponse (or ParseFile) to create new
        HTMLForm objects.

        action: full (absolute URI) form action
        method: "GET" or "POST"
        enctype: form transfer encoding MIME type
        name: name of form
        attrs: dictionary mapping original HTML form attributes to their values

        """
        self.action = action
        self.method = method
        self.enctype = enctype
        self.form_encoding = encoding or 'utf-8'
        self.name = name
        if attrs is not None:
            self.attrs = dict(attrs)
        else:
            self.attrs = {}
        self.controls = []
        self._request_class = request_class
        self._forms = forms
        self._labels = labels
        self._id_to_labels = id_to_labels
        self._urlunparse = urlunparse
        self._urlparse = urlparse

    def new_control--- This code section failed: ---

 L.1904         0  LOAD_FAST                'type'
                2  LOAD_METHOD              lower
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'type'

 L.1905         8  LOAD_FAST                'self'
               10  LOAD_ATTR                type2class
               12  LOAD_METHOD              get
               14  LOAD_FAST                'type'
               16  CALL_METHOD_1         1  ''
               18  STORE_FAST               'klass'

 L.1906        20  LOAD_FAST                'klass'
               22  LOAD_CONST               None
               24  COMPARE_OP               is
               26  POP_JUMP_IF_FALSE    42  'to 42'

 L.1907        28  LOAD_FAST                'ignore_unknown'
               30  POP_JUMP_IF_FALSE    38  'to 38'

 L.1908        32  LOAD_GLOBAL              IgnoreControl
               34  STORE_FAST               'klass'
               36  JUMP_FORWARD         42  'to 42'
             38_0  COME_FROM            30  '30'

 L.1910        38  LOAD_GLOBAL              TextControl
               40  STORE_FAST               'klass'
             42_0  COME_FROM            36  '36'
             42_1  COME_FROM            26  '26'

 L.1912        42  LOAD_GLOBAL              dict
               44  LOAD_FAST                'attrs'
               46  CALL_FUNCTION_1       1  ''
               48  STORE_FAST               'a'

 L.1913        50  LOAD_GLOBAL              issubclass
               52  LOAD_FAST                'klass'
               54  LOAD_GLOBAL              ListControl
               56  CALL_FUNCTION_2       2  ''
               58  POP_JUMP_IF_FALSE    78  'to 78'

 L.1914        60  LOAD_FAST                'klass'
               62  LOAD_FAST                'type'
               64  LOAD_FAST                'name'
               66  LOAD_FAST                'a'
               68  LOAD_FAST                'select_default'
               70  LOAD_FAST                'index'
               72  CALL_FUNCTION_5       5  ''
               74  STORE_FAST               'control'
               76  JUMP_FORWARD         92  'to 92'
             78_0  COME_FROM            58  '58'

 L.1916        78  LOAD_FAST                'klass'
               80  LOAD_FAST                'type'
               82  LOAD_FAST                'name'
               84  LOAD_FAST                'a'
               86  LOAD_FAST                'index'
               88  CALL_FUNCTION_4       4  ''
               90  STORE_FAST               'control'
             92_0  COME_FROM            76  '76'

 L.1918        92  LOAD_FAST                'type'
               94  LOAD_STR                 'select'
               96  COMPARE_OP               ==
               98  POP_JUMP_IF_FALSE   172  'to 172'
              100  LOAD_GLOBAL              len
              102  LOAD_FAST                'attrs'
              104  CALL_FUNCTION_1       1  ''
              106  LOAD_CONST               1
              108  COMPARE_OP               ==
              110  POP_JUMP_IF_FALSE   172  'to 172'

 L.1919       112  LOAD_GLOBAL              range
              114  LOAD_GLOBAL              len
              116  LOAD_FAST                'self'
              118  LOAD_ATTR                controls
              120  CALL_FUNCTION_1       1  ''
              122  LOAD_CONST               1
              124  BINARY_SUBTRACT  
              126  LOAD_CONST               -1
              128  LOAD_CONST               -1
              130  CALL_FUNCTION_3       3  ''
              132  GET_ITER         
            134_0  COME_FROM           170  '170'
            134_1  COME_FROM           156  '156'
              134  FOR_ITER            172  'to 172'
              136  STORE_FAST               'ii'

 L.1920       138  LOAD_FAST                'self'
              140  LOAD_ATTR                controls
              142  LOAD_FAST                'ii'
              144  BINARY_SUBSCR    
              146  STORE_FAST               'ctl'

 L.1921       148  LOAD_FAST                'ctl'
              150  LOAD_ATTR                type
              152  LOAD_STR                 'select'
              154  COMPARE_OP               ==
              156  POP_JUMP_IF_FALSE_BACK   134  'to 134'

 L.1922       158  LOAD_FAST                'ctl'
              160  LOAD_METHOD              close_control
              162  CALL_METHOD_0         0  ''
              164  POP_TOP          

 L.1923       166  POP_TOP          
              168  BREAK_LOOP          172  'to 172'
              170  JUMP_BACK           134  'to 134'
            172_0  COME_FROM           168  '168'
            172_1  COME_FROM           134  '134'
            172_2  COME_FROM           110  '110'
            172_3  COME_FROM            98  '98'

 L.1925       172  LOAD_FAST                'control'
              174  LOAD_METHOD              add_to_form
              176  LOAD_FAST                'self'
              178  CALL_METHOD_1         1  ''
              180  POP_TOP          

 L.1926       182  LOAD_FAST                'self'
              184  LOAD_ATTR                _urlparse
              186  LOAD_FAST                'control'
              188  STORE_ATTR               _urlparse

 L.1927       190  LOAD_FAST                'self'
              192  LOAD_ATTR                _urlunparse
              194  LOAD_FAST                'control'
              196  STORE_ATTR               _urlunparse

Parse error at or near `LOAD_FAST' instruction at offset 194

    def fixup(self):
        """Normalise form after all controls have been added.

        This is usually called by ParseFile and ParseResponse.  Don't call it
        youself unless you're building your own Control instances.

        This method should only be called once, after all controls have been
        added to the form.

        """
        for control in self.controls:
            control.fixup()
            control.form_encoding = self.form_encoding

    def __str__(self):
        header = '%s%s %s %s' % ((self.name) and (self.name + ' ') or '',
         self.method, self.action, self.enctype)
        rep = [header]
        for control in self.controls:
            rep.append('  %s' % str(control))
        else:
            return '<%s>' % '\n'.join(rep)

    def __getitem__(self, name):
        return self.find_control(name).value

    def __contains__(self, name):
        return bool(self.find_control(name))

    def __setitem__(self, name, value):
        control = self.find_control(name)
        try:
            control.value = value
        except AttributeError as e:
            try:
                raise ValueError(str(e))
            finally:
                e = None
                del e

    def get_value(self, name=None, type=None, kind=None, id=None, nr=None, by_label=False, label=None):
        """Return value of control.

        If only name and value arguments are supplied, equivalent to

        .. code-block:: python

            form[name]

        """
        if by_label:
            deprecation('form.get_value_by_label(...)')
        c = self.find_control(name, type, kind, id, label=label, nr=nr)
        if by_label:
            try:
                meth = c.get_value_by_label
            except AttributeError:
                raise NotImplementedError("control '%s' does not yet support by_label" % c.name)
            else:
                return meth()
        else:
            return c.value

    def set_value(self, value, name=None, type=None, kind=None, id=None, nr=None, by_label=False, label=None):
        """Set value of control.

        If only name and value arguments are supplied, equivalent to

        .. code-block:: python

            form[name] = value

        """
        if by_label:
            deprecation('form.get_value_by_label(...)')
        c = self.find_control(name, type, kind, id, label=label, nr=nr)
        if by_label:
            try:
                meth = c.set_value_by_label
            except AttributeError:
                raise NotImplementedError("control '%s' does not yet support by_label" % c.name)
            else:
                meth(value)
        else:
            c.value = value

    def get_value_by_label(self, name=None, type=None, kind=None, id=None, label=None, nr=None):
        """

        All arguments should be passed by name.

        """
        c = self.find_control(name, type, kind, id, label=label, nr=nr)
        return c.get_value_by_label()

    def set_value_by_label(self, value, name=None, type=None, kind=None, id=None, label=None, nr=None):
        """

        All arguments should be passed by name.

        """
        c = self.find_control(name, type, kind, id, label=label, nr=nr)
        c.set_value_by_label(value)

    def set_all_readonly(self, readonly):
        for control in self.controls:
            control.readonly = bool(readonly)

    def clear_all(self):
        """Clear the value attributes of all controls in the form.

        See :meth:`mechanize.HTMLForm.clear()`

        """
        for control in self.controls:
            control.clear()

    def clear(self, name=None, type=None, kind=None, id=None, nr=None, label=None):
        """Clear the value attribute of a control.

        As a result, the affected control will not be successful until a value
        is subsequently set.  AttributeError is raised on readonly controls.

        """
        c = self.find_control(name, type, kind, id, label=label, nr=nr)
        c.clear()

    def possible_items(self, name=None, type=None, kind=None, id=None, nr=None, by_label=False, label=None):
        """Return a list of all values that the specified control can take."""
        c = self._find_list_control(name, type, kind, id, label, nr)
        return c.possible_items(by_label)

    def set(self, selected, item_name, name=None, type=None, kind=None, id=None, nr=None, by_label=False, label=None):
        """Select / deselect named list item.

        :arg selected: boolean selected state

        """
        self._find_list_control(name, type, kind, id, label, nr).set(selected, item_name, by_label)

    def toggle(self, item_name, name=None, type=None, kind=None, id=None, nr=None, by_label=False, label=None):
        """Toggle selected state of named list item."""
        self._find_list_control(name, type, kind, id, label, nr).toggle(item_name, by_label)

    def set_single(self, selected, name=None, type=None, kind=None, id=None, nr=None, by_label=None, label=None):
        """Select / deselect list item in a control having only one item.

        If the control has multiple list items, ItemCountError is raised.

        This is just a convenience method, so you don't need to know the item's
        name -- the item name in these single-item controls is usually
        something meaningless like "1" or "on".

        For example, if a checkbox has a single item named "on", the following
        two calls are equivalent:

        .. code-block:: python

            control.toggle("on")
            control.toggle_single()

        """
        self._find_list_control(name, type, kind, id, label, nr).set_single(selected)

    def toggle_single(self, name=None, type=None, kind=None, id=None, nr=None, by_label=None, label=None):
        """Toggle selected state of list item in control having only one item.

        The rest is as for :meth:`mechanize.HTMLForm.set_single()`

        """
        self._find_list_control(name, type, kind, id, label, nr).toggle_single()

    def add_file(self, file_object, content_type=None, filename=None, name=None, id=None, nr=None, label=None):
        """Add a file to be uploaded.

        :arg file_object: file-like object (with read method) from which to
            read data to upload
        :arg content_type: MIME content type of data to upload
        :arg filename: filename to pass to server

        If filename is None, no filename is sent to the server.

        If content_type is None, the content type is guessed based on the
        filename and the data from read from the file object.

        At the moment, guessed content type is always application/octet-stream.

        Note the following useful HTML attributes of file upload controls (see
        HTML 4.01 spec, section 17):

          * `accept`: comma-separated list of content types
             that the server will handle correctly;
             you can use this to filter out non-conforming files
          * `size`: XXX IIRC, this is indicative of whether form
             wants multiple or single files
          * `maxlength`: XXX hint of max content length in bytes?

        """
        self.find_control(name,
          'file', id=id, label=label, nr=nr).add_file(file_object, content_type, filename)

    def click(self, name=None, type=None, id=None, nr=0, coord=(1, 1), request_class=_request.Request, label=None):
        """Return request that would result from clicking on a control.

        The request object is a mechanize.Request instance, which you can pass
        to mechanize.urlopen.

        Only some control types (INPUT/SUBMIT & BUTTON/SUBMIT buttons and
        IMAGEs) can be clicked.

        Will click on the first clickable control, subject to the name, type
        and nr arguments (as for find_control).  If no name, type, id or number
        is specified and there are no clickable controls, a request will be
        returned for the form in its current, un-clicked, state.

        IndexError is raised if any of name, type, id or nr is specified but no
        matching control is found.  ValueError is raised if the HTMLForm has an
        enctype attribute that is not recognised.

        You can optionally specify a coordinate to click at, which only makes a
        difference if you clicked on an image.

        """
        return self._click(name, type, id, label, nr, coord, 'request', self._request_class)

    def click_request_data(self, name=None, type=None, id=None, nr=0, coord=(1, 1), request_class=_request.Request, label=None):
        """As for click method, but return a tuple (url, data, headers).

        You can use this data to send a request to the server.  This is useful
        if you're using httplib or urllib rather than mechanize.  Otherwise,
        use the click method.

        """
        return self._click(name, type, id, label, nr, coord, 'request_data', self._request_class)

    def click_pairs(self, name=None, type=None, id=None, nr=0, coord=(1, 1), label=None):
        """As for click_request_data, but returns a list of (key, value) pairs.

        You can use this list as an argument to urllib.urlencode.  This is
        usually only useful if you're using httplib or urllib rather than
        mechanize.  It may also be useful if you want to manually tweak the
        keys and/or values, but this should not be necessary.  Otherwise, use
        the click method.

        Note that this method is only useful for forms of MIME type
        x-www-form-urlencoded.  In particular, it does not return the
        information required for file upload.  If you need file upload and are
        not using mechanize, use click_request_data.
        """
        return self._click(name, type, id, label, nr, coord, 'pairs', self._request_class)

    def find_control(self, name=None, type=None, kind=None, id=None, predicate=None, nr=None, label=None):
        """Locate and return some specific control within the form.

        At least one of the name, type, kind, predicate and nr arguments must
        be supplied.  If no matching control is found, ControlNotFoundError is
        raised.

        If name is specified, then the control must have the indicated name.

        If type is specified then the control must have the specified type (in
        addition to the types possible for <input> HTML tags: "text",
        "password", "hidden", "submit", "image", "button", "radio", "checkbox",
        "file" we also have "reset", "buttonbutton", "submitbutton",
        "resetbutton", "textarea", "select").

        If kind is specified, then the control must fall into the specified
        group, each of which satisfies a particular interface.  The types are
        "text", "list", "multilist", "singlelist", "clickable" and "file".

        If id is specified, then the control must have the indicated id.

        If predicate is specified, then the control must match that function.
        The predicate function is passed the control as its single argument,
        and should return a boolean value indicating whether the control
        matched.

        nr, if supplied, is the sequence number of the control (where 0 is the
        first).  Note that control 0 is the first control matching all the
        other arguments (if supplied); it is not necessarily the first control
        in the form.  If no nr is supplied, AmbiguityError is raised if
        multiple controls match the other arguments.

        If label is specified, then the control must have this label.  Note
        that radio controls and checkboxes never have labels: their items do.

        """
        if name is None:
            if type is None:
                if kind is None:
                    if id is None:
                        if label is None:
                            if predicate is None:
                                if nr is None:
                                    raise ValueError('at least one argument must be supplied to specify control')
        return self._find_control(name, type, kind, id, label, predicate, nr)

    def _find_list_control(self, name=None, type=None, kind=None, id=None, label=None, nr=None):
        if name is None:
            if type is None:
                if kind is None:
                    if id is None:
                        if label is None:
                            if nr is None:
                                raise ValueError('at least one argument must be supplied to specify control')
        return self._find_control(name, type, kind, id, label, is_listcontrol, nr)

    def _find_control--- This code section failed: ---

 L.2376         0  LOAD_FAST                'name'
                2  LOAD_CONST               None
                4  COMPARE_OP               is-not
                6  POP_JUMP_IF_FALSE    32  'to 32'
                8  LOAD_FAST                'name'
               10  LOAD_GLOBAL              Missing
               12  COMPARE_OP               is-not
               14  POP_JUMP_IF_FALSE    32  'to 32'

 L.2377        16  LOAD_GLOBAL              isstringlike
               18  LOAD_FAST                'name'
               20  CALL_FUNCTION_1       1  ''

 L.2376        22  POP_JUMP_IF_TRUE     32  'to 32'

 L.2378        24  LOAD_GLOBAL              TypeError
               26  LOAD_STR                 'control name must be string-like'
               28  CALL_FUNCTION_1       1  ''
               30  RAISE_VARARGS_1       1  'exception instance'
             32_0  COME_FROM            22  '22'
             32_1  COME_FROM            14  '14'
             32_2  COME_FROM             6  '6'

 L.2379        32  LOAD_FAST                'type'
               34  LOAD_CONST               None
               36  COMPARE_OP               is-not
               38  POP_JUMP_IF_FALSE    56  'to 56'
               40  LOAD_GLOBAL              isstringlike
               42  LOAD_FAST                'type'
               44  CALL_FUNCTION_1       1  ''
               46  POP_JUMP_IF_TRUE     56  'to 56'

 L.2380        48  LOAD_GLOBAL              TypeError
               50  LOAD_STR                 'control type must be string-like'
               52  CALL_FUNCTION_1       1  ''
               54  RAISE_VARARGS_1       1  'exception instance'
             56_0  COME_FROM            46  '46'
             56_1  COME_FROM            38  '38'

 L.2381        56  LOAD_FAST                'kind'
               58  LOAD_CONST               None
               60  COMPARE_OP               is-not
               62  POP_JUMP_IF_FALSE    80  'to 80'
               64  LOAD_GLOBAL              isstringlike
               66  LOAD_FAST                'kind'
               68  CALL_FUNCTION_1       1  ''
               70  POP_JUMP_IF_TRUE     80  'to 80'

 L.2382        72  LOAD_GLOBAL              TypeError
               74  LOAD_STR                 'control kind must be string-like'
               76  CALL_FUNCTION_1       1  ''
               78  RAISE_VARARGS_1       1  'exception instance'
             80_0  COME_FROM            70  '70'
             80_1  COME_FROM            62  '62'

 L.2383        80  LOAD_FAST                'id'
               82  LOAD_CONST               None
               84  COMPARE_OP               is-not
               86  POP_JUMP_IF_FALSE   104  'to 104'
               88  LOAD_GLOBAL              isstringlike
               90  LOAD_FAST                'id'
               92  CALL_FUNCTION_1       1  ''
               94  POP_JUMP_IF_TRUE    104  'to 104'

 L.2384        96  LOAD_GLOBAL              TypeError
               98  LOAD_STR                 'control id must be string-like'
              100  CALL_FUNCTION_1       1  ''
              102  RAISE_VARARGS_1       1  'exception instance'
            104_0  COME_FROM            94  '94'
            104_1  COME_FROM            86  '86'

 L.2385       104  LOAD_FAST                'label'
              106  LOAD_CONST               None
              108  COMPARE_OP               is-not
              110  POP_JUMP_IF_FALSE   128  'to 128'
              112  LOAD_GLOBAL              isstringlike
              114  LOAD_FAST                'label'
              116  CALL_FUNCTION_1       1  ''
              118  POP_JUMP_IF_TRUE    128  'to 128'

 L.2386       120  LOAD_GLOBAL              TypeError
              122  LOAD_STR                 'control label must be string-like'
              124  CALL_FUNCTION_1       1  ''
              126  RAISE_VARARGS_1       1  'exception instance'
            128_0  COME_FROM           118  '118'
            128_1  COME_FROM           110  '110'

 L.2387       128  LOAD_FAST                'predicate'
              130  LOAD_CONST               None
              132  COMPARE_OP               is-not
              134  POP_JUMP_IF_FALSE   152  'to 152'
              136  LOAD_GLOBAL              callable
              138  LOAD_FAST                'predicate'
              140  CALL_FUNCTION_1       1  ''
              142  POP_JUMP_IF_TRUE    152  'to 152'

 L.2388       144  LOAD_GLOBAL              TypeError
              146  LOAD_STR                 'control predicate must be callable'
              148  CALL_FUNCTION_1       1  ''
              150  RAISE_VARARGS_1       1  'exception instance'
            152_0  COME_FROM           142  '142'
            152_1  COME_FROM           134  '134'

 L.2389       152  LOAD_FAST                'nr'
              154  LOAD_CONST               None
              156  COMPARE_OP               is-not
              158  POP_JUMP_IF_FALSE   176  'to 176'
              160  LOAD_FAST                'nr'
              162  LOAD_CONST               0
              164  COMPARE_OP               <
              166  POP_JUMP_IF_FALSE   176  'to 176'

 L.2390       168  LOAD_GLOBAL              ValueError
              170  LOAD_STR                 'control number must be a positive integer'
              172  CALL_FUNCTION_1       1  ''
              174  RAISE_VARARGS_1       1  'exception instance'
            176_0  COME_FROM           166  '166'
            176_1  COME_FROM           158  '158'

 L.2392       176  LOAD_FAST                'nr'
              178  STORE_FAST               'orig_nr'

 L.2393       180  LOAD_CONST               None
              182  STORE_FAST               'found'

 L.2394       184  LOAD_CONST               False
              186  STORE_FAST               'ambiguous'

 L.2396       188  LOAD_FAST                'self'
              190  LOAD_ATTR                controls
              192  GET_ITER         
            194_0  COME_FROM           432  '432'
            194_1  COME_FROM           410  '410'
            194_2  COME_FROM           372  '372'
            194_3  COME_FROM           324  '324'
            194_4  COME_FROM           306  '306'
            194_5  COME_FROM           282  '282'
            194_6  COME_FROM           258  '258'
            194_7  COME_FROM           234  '234'
            194_8  COME_FROM           222  '222'
              194  FOR_ITER            434  'to 434'
              196  STORE_FAST               'control'

 L.2397       198  LOAD_FAST                'name'
              200  LOAD_CONST               None
              202  COMPARE_OP               is-not
              204  POP_JUMP_IF_FALSE   236  'to 236'
              206  LOAD_FAST                'name'
              208  LOAD_FAST                'control'
              210  LOAD_ATTR                name
              212  COMPARE_OP               !=
              214  POP_JUMP_IF_FALSE   236  'to 236'

 L.2398       216  LOAD_FAST                'name'
              218  LOAD_GLOBAL              Missing
              220  COMPARE_OP               is-not

 L.2397       222  POP_JUMP_IF_TRUE_BACK   194  'to 194'

 L.2398       224  LOAD_FAST                'control'
              226  LOAD_ATTR                name
              228  LOAD_CONST               None
              230  COMPARE_OP               is-not

 L.2397       232  POP_JUMP_IF_FALSE   236  'to 236'

 L.2399       234  JUMP_BACK           194  'to 194'
            236_0  COME_FROM           232  '232'
            236_1  COME_FROM           214  '214'
            236_2  COME_FROM           204  '204'

 L.2400       236  LOAD_FAST                'type'
              238  LOAD_CONST               None
              240  COMPARE_OP               is-not
          242_244  POP_JUMP_IF_FALSE   260  'to 260'
              246  LOAD_FAST                'type'
              248  LOAD_FAST                'control'
              250  LOAD_ATTR                type
              252  COMPARE_OP               !=
          254_256  POP_JUMP_IF_FALSE   260  'to 260'

 L.2401       258  JUMP_BACK           194  'to 194'
            260_0  COME_FROM           254  '254'
            260_1  COME_FROM           242  '242'

 L.2402       260  LOAD_FAST                'kind'
              262  LOAD_CONST               None
              264  COMPARE_OP               is-not
          266_268  POP_JUMP_IF_FALSE   284  'to 284'
              270  LOAD_FAST                'control'
              272  LOAD_METHOD              is_of_kind
              274  LOAD_FAST                'kind'
              276  CALL_METHOD_1         1  ''
          278_280  POP_JUMP_IF_TRUE    284  'to 284'

 L.2403       282  JUMP_BACK           194  'to 194'
            284_0  COME_FROM           278  '278'
            284_1  COME_FROM           266  '266'

 L.2404       284  LOAD_FAST                'id'
              286  LOAD_CONST               None
              288  COMPARE_OP               is-not
          290_292  POP_JUMP_IF_FALSE   308  'to 308'
              294  LOAD_FAST                'id'
              296  LOAD_FAST                'control'
              298  LOAD_ATTR                id
              300  COMPARE_OP               !=
          302_304  POP_JUMP_IF_FALSE   308  'to 308'

 L.2405       306  JUMP_BACK           194  'to 194'
            308_0  COME_FROM           302  '302'
            308_1  COME_FROM           290  '290'

 L.2406       308  LOAD_FAST                'predicate'
          310_312  POP_JUMP_IF_FALSE   326  'to 326'
              314  LOAD_FAST                'predicate'
              316  LOAD_FAST                'control'
              318  CALL_FUNCTION_1       1  ''
          320_322  POP_JUMP_IF_TRUE    326  'to 326'

 L.2407       324  JUMP_BACK           194  'to 194'
            326_0  COME_FROM           320  '320'
            326_1  COME_FROM           310  '310'

 L.2408       326  LOAD_FAST                'label'
          328_330  POP_JUMP_IF_FALSE   374  'to 374'

 L.2409       332  LOAD_FAST                'control'
              334  LOAD_METHOD              get_labels
              336  CALL_METHOD_0         0  ''
              338  GET_ITER         
            340_0  COME_FROM           368  '368'
            340_1  COME_FROM           358  '358'
              340  FOR_ITER            372  'to 372'
              342  STORE_FAST               'l'

 L.2410       344  LOAD_FAST                'l'
              346  LOAD_ATTR                text
              348  LOAD_METHOD              find
              350  LOAD_FAST                'label'
              352  CALL_METHOD_1         1  ''
              354  LOAD_CONST               -1
              356  COMPARE_OP               >
          358_360  POP_JUMP_IF_FALSE_BACK   340  'to 340'

 L.2411       362  POP_TOP          
          364_366  BREAK_LOOP          374  'to 374'
          368_370  JUMP_BACK           340  'to 340'
            372_0  COME_FROM           340  '340'

 L.2413       372  JUMP_BACK           194  'to 194'
            374_0  COME_FROM           364  '364'
            374_1  COME_FROM           328  '328'

 L.2414       374  LOAD_FAST                'nr'
              376  LOAD_CONST               None
              378  COMPARE_OP               is-not
          380_382  POP_JUMP_IF_FALSE   412  'to 412'

 L.2415       384  LOAD_FAST                'nr'
              386  LOAD_CONST               0
              388  COMPARE_OP               ==
          390_392  POP_JUMP_IF_FALSE   402  'to 402'

 L.2416       394  LOAD_FAST                'control'
              396  ROT_TWO          
              398  POP_TOP          
              400  RETURN_VALUE     
            402_0  COME_FROM           390  '390'

 L.2417       402  LOAD_FAST                'nr'
              404  LOAD_CONST               1
              406  INPLACE_SUBTRACT 
              408  STORE_FAST               'nr'

 L.2418       410  JUMP_BACK           194  'to 194'
            412_0  COME_FROM           380  '380'

 L.2419       412  LOAD_FAST                'found'
          414_416  POP_JUMP_IF_FALSE   428  'to 428'

 L.2420       418  LOAD_CONST               True
              420  STORE_FAST               'ambiguous'

 L.2421       422  POP_TOP          
          424_426  BREAK_LOOP          434  'to 434'
            428_0  COME_FROM           414  '414'

 L.2422       428  LOAD_FAST                'control'
              430  STORE_FAST               'found'
              432  JUMP_BACK           194  'to 194'
            434_0  COME_FROM           424  '424'
            434_1  COME_FROM           194  '194'

 L.2424       434  LOAD_FAST                'found'
          436_438  POP_JUMP_IF_FALSE   450  'to 450'
              440  LOAD_FAST                'ambiguous'
          442_444  POP_JUMP_IF_TRUE    450  'to 450'

 L.2425       446  LOAD_FAST                'found'
              448  RETURN_VALUE     
            450_0  COME_FROM           442  '442'
            450_1  COME_FROM           436  '436'

 L.2427       450  BUILD_LIST_0          0 
              452  STORE_FAST               'description'

 L.2428       454  LOAD_FAST                'name'
              456  LOAD_CONST               None
              458  COMPARE_OP               is-not
          460_462  POP_JUMP_IF_FALSE   482  'to 482'

 L.2429       464  LOAD_FAST                'description'
              466  LOAD_METHOD              append
              468  LOAD_STR                 'name %s'
              470  LOAD_GLOBAL              repr
              472  LOAD_FAST                'name'
              474  CALL_FUNCTION_1       1  ''
              476  BINARY_MODULO    
              478  CALL_METHOD_1         1  ''
              480  POP_TOP          
            482_0  COME_FROM           460  '460'

 L.2430       482  LOAD_FAST                'type'
              484  LOAD_CONST               None
              486  COMPARE_OP               is-not
          488_490  POP_JUMP_IF_FALSE   506  'to 506'

 L.2431       492  LOAD_FAST                'description'
              494  LOAD_METHOD              append
              496  LOAD_STR                 "type '%s'"
              498  LOAD_FAST                'type'
              500  BINARY_MODULO    
              502  CALL_METHOD_1         1  ''
              504  POP_TOP          
            506_0  COME_FROM           488  '488'

 L.2432       506  LOAD_FAST                'kind'
              508  LOAD_CONST               None
              510  COMPARE_OP               is-not
          512_514  POP_JUMP_IF_FALSE   530  'to 530'

 L.2433       516  LOAD_FAST                'description'
              518  LOAD_METHOD              append
              520  LOAD_STR                 "kind '%s'"
              522  LOAD_FAST                'kind'
              524  BINARY_MODULO    
              526  CALL_METHOD_1         1  ''
              528  POP_TOP          
            530_0  COME_FROM           512  '512'

 L.2434       530  LOAD_FAST                'id'
              532  LOAD_CONST               None
              534  COMPARE_OP               is-not
          536_538  POP_JUMP_IF_FALSE   554  'to 554'

 L.2435       540  LOAD_FAST                'description'
              542  LOAD_METHOD              append
              544  LOAD_STR                 "id '%s'"
              546  LOAD_FAST                'id'
              548  BINARY_MODULO    
              550  CALL_METHOD_1         1  ''
              552  POP_TOP          
            554_0  COME_FROM           536  '536'

 L.2436       554  LOAD_FAST                'label'
              556  LOAD_CONST               None
              558  COMPARE_OP               is-not
          560_562  POP_JUMP_IF_FALSE   578  'to 578'

 L.2437       564  LOAD_FAST                'description'
              566  LOAD_METHOD              append
              568  LOAD_STR                 "label '%s'"
              570  LOAD_FAST                'label'
              572  BINARY_MODULO    
              574  CALL_METHOD_1         1  ''
              576  POP_TOP          
            578_0  COME_FROM           560  '560'

 L.2438       578  LOAD_FAST                'predicate'
              580  LOAD_CONST               None
              582  COMPARE_OP               is-not
          584_586  POP_JUMP_IF_FALSE   602  'to 602'

 L.2439       588  LOAD_FAST                'description'
              590  LOAD_METHOD              append
              592  LOAD_STR                 'predicate %s'
              594  LOAD_FAST                'predicate'
              596  BINARY_MODULO    
              598  CALL_METHOD_1         1  ''
              600  POP_TOP          
            602_0  COME_FROM           584  '584'

 L.2440       602  LOAD_FAST                'orig_nr'
          604_606  POP_JUMP_IF_FALSE   622  'to 622'

 L.2441       608  LOAD_FAST                'description'
              610  LOAD_METHOD              append
              612  LOAD_STR                 'nr %d'
              614  LOAD_FAST                'orig_nr'
              616  BINARY_MODULO    
              618  CALL_METHOD_1         1  ''
              620  POP_TOP          
            622_0  COME_FROM           604  '604'

 L.2442       622  LOAD_STR                 ', '
              624  LOAD_METHOD              join
              626  LOAD_FAST                'description'
              628  CALL_METHOD_1         1  ''
              630  STORE_FAST               'description'

 L.2444       632  LOAD_FAST                'ambiguous'
          634_636  POP_JUMP_IF_FALSE   652  'to 652'

 L.2445       638  LOAD_GLOBAL              AmbiguityError
              640  LOAD_STR                 'more than one control matching '

 L.2446       642  LOAD_FAST                'description'

 L.2445       644  BINARY_ADD       
              646  CALL_FUNCTION_1       1  ''
              648  RAISE_VARARGS_1       1  'exception instance'
              650  JUMP_FORWARD        670  'to 670'
            652_0  COME_FROM           634  '634'

 L.2447       652  LOAD_FAST                'found'
          654_656  POP_JUMP_IF_TRUE    670  'to 670'

 L.2448       658  LOAD_GLOBAL              ControlNotFoundError
              660  LOAD_STR                 'no control matching '
              662  LOAD_FAST                'description'
              664  BINARY_ADD       
              666  CALL_FUNCTION_1       1  ''
              668  RAISE_VARARGS_1       1  'exception instance'
            670_0  COME_FROM           654  '654'
            670_1  COME_FROM           650  '650'

 L.2449       670  LOAD_CONST               False
          672_674  POP_JUMP_IF_TRUE    680  'to 680'
              676  LOAD_ASSERT              AssertionError
              678  RAISE_VARARGS_1       1  'exception instance'
            680_0  COME_FROM           672  '672'

Parse error at or near `RAISE_VARARGS_1' instruction at offset 678

    def _click--- This code section failed: ---

 L.2460         0  SETUP_FINALLY        28  'to 28'

 L.2461         2  LOAD_FAST                'self'
                4  LOAD_METHOD              _find_control
                6  LOAD_FAST                'name'
                8  LOAD_FAST                'type'
               10  LOAD_STR                 'clickable'
               12  LOAD_FAST                'id'
               14  LOAD_FAST                'label'

 L.2462        16  LOAD_CONST               None

 L.2462        18  LOAD_FAST                'nr'

 L.2461        20  CALL_METHOD_7         7  ''
               22  STORE_FAST               'control'
               24  POP_BLOCK        
               26  JUMP_FORWARD        102  'to 102'
             28_0  COME_FROM_FINALLY     0  '0'

 L.2463        28  DUP_TOP          
               30  LOAD_GLOBAL              ControlNotFoundError
               32  COMPARE_OP               exception-match
               34  POP_JUMP_IF_FALSE   100  'to 100'
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L.2464        42  LOAD_FAST                'name'
               44  LOAD_CONST               None
               46  COMPARE_OP               is-not
               48  POP_JUMP_IF_TRUE     82  'to 82'
               50  LOAD_FAST                'type'
               52  LOAD_CONST               None
               54  COMPARE_OP               is-not
               56  POP_JUMP_IF_TRUE     82  'to 82'
               58  LOAD_FAST                'id'
               60  LOAD_CONST               None
               62  COMPARE_OP               is-not
               64  POP_JUMP_IF_TRUE     82  'to 82'

 L.2465        66  LOAD_FAST                'label'
               68  LOAD_CONST               None
               70  COMPARE_OP               is-not

 L.2464        72  POP_JUMP_IF_TRUE     82  'to 82'

 L.2465        74  LOAD_FAST                'nr'
               76  LOAD_CONST               0
               78  COMPARE_OP               !=

 L.2464        80  POP_JUMP_IF_FALSE    84  'to 84'
             82_0  COME_FROM            72  '72'
             82_1  COME_FROM            64  '64'
             82_2  COME_FROM            56  '56'
             82_3  COME_FROM            48  '48'

 L.2466        82  RAISE_VARARGS_0       0  'reraise'
             84_0  COME_FROM            80  '80'

 L.2469        84  LOAD_FAST                'self'
               86  LOAD_METHOD              _switch_click
               88  LOAD_FAST                'return_type'
               90  LOAD_FAST                'request_class'
               92  CALL_METHOD_2         2  ''
               94  ROT_FOUR         
               96  POP_EXCEPT       
               98  RETURN_VALUE     
            100_0  COME_FROM            34  '34'
              100  END_FINALLY      
            102_0  COME_FROM            26  '26'

 L.2471       102  LOAD_FAST                'self'
              104  LOAD_ATTR                method
              106  LOAD_FAST                'self'
              108  LOAD_ATTR                action
              110  LOAD_FAST                'self'
              112  LOAD_ATTR                enctype
              114  BUILD_TUPLE_3         3 
              116  STORE_FAST               'originals'

 L.2472       118  SETUP_FINALLY       210  'to 210'

 L.2473       120  LOAD_GLOBAL              isinstance
              122  LOAD_FAST                'control'
              124  LOAD_GLOBAL              ScalarControl
              126  CALL_FUNCTION_2       2  ''
              128  POP_JUMP_IF_FALSE   190  'to 190'

 L.2474       130  LOAD_FAST                'control'
              132  LOAD_ATTR                attrs
              134  LOAD_METHOD              get

 L.2475       136  LOAD_STR                 'formmethod'

 L.2474       138  CALL_METHOD_1         1  ''
              140  JUMP_IF_TRUE_OR_POP   146  'to 146'

 L.2475       142  LOAD_FAST                'self'
              144  LOAD_ATTR                method
            146_0  COME_FROM           140  '140'

 L.2474       146  LOAD_FAST                'self'
              148  STORE_ATTR               method

 L.2476       150  LOAD_FAST                'control'
              152  LOAD_ATTR                attrs
              154  LOAD_METHOD              get

 L.2477       156  LOAD_STR                 'formaction'

 L.2476       158  CALL_METHOD_1         1  ''
              160  JUMP_IF_TRUE_OR_POP   166  'to 166'

 L.2477       162  LOAD_FAST                'self'
              164  LOAD_ATTR                action
            166_0  COME_FROM           160  '160'

 L.2476       166  LOAD_FAST                'self'
              168  STORE_ATTR               action

 L.2478       170  LOAD_FAST                'control'
              172  LOAD_ATTR                attrs
              174  LOAD_METHOD              get

 L.2479       176  LOAD_STR                 'formenctype'

 L.2478       178  CALL_METHOD_1         1  ''
              180  JUMP_IF_TRUE_OR_POP   186  'to 186'

 L.2479       182  LOAD_FAST                'self'
              184  LOAD_ATTR                enctype
            186_0  COME_FROM           180  '180'

 L.2478       186  LOAD_FAST                'self'
              188  STORE_ATTR               enctype
            190_0  COME_FROM           128  '128'

 L.2480       190  LOAD_FAST                'control'
              192  LOAD_METHOD              _click
              194  LOAD_FAST                'self'
              196  LOAD_FAST                'coord'
              198  LOAD_FAST                'return_type'
              200  LOAD_FAST                'request_class'
              202  CALL_METHOD_4         4  ''
              204  POP_BLOCK        
              206  CALL_FINALLY        210  'to 210'
              208  RETURN_VALUE     
            210_0  COME_FROM           206  '206'
            210_1  COME_FROM_FINALLY   118  '118'

 L.2482       210  LOAD_FAST                'originals'
              212  UNPACK_SEQUENCE_3     3 
              214  LOAD_FAST                'self'
              216  STORE_ATTR               method
              218  LOAD_FAST                'self'
              220  STORE_ATTR               action
              222  LOAD_FAST                'self'
              224  STORE_ATTR               enctype
              226  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 206

    def _pairs(self):
        """Return sequence of (key, value) pairs suitable for urlencoding."""
        return [(
         k, v) for i, k, v, c_i in self._pairs_and_controls()]

    def _pairs_and_controls(self):
        """Return sequence of (index, key, value, control_index)
        of totally ordered pairs suitable for urlencoding.

        control_index is the index of the control in self.controls
        """
        pairs = []
        for control_index in range(len(self.controls)):
            control = self.controls[control_index]
            for ii, key, val in control._totally_ordered_pairs():
                if ii is None:
                    ii = -1
                else:
                    pairs.append((ii, key, val, control_index))

        else:
            pairs.sort()
            return pairs

    def _request_data(self):
        """Return a tuple (url, data, headers)."""
        method = self.method.upper()
        parts = self._urlparse(self.action)
        rest, (query, frag) = parts[:-2], parts[-2:]
        frag

        def encode_data(x):
            if isinstance(x, unicode_type):
                x = x.encode(self.form_encoding)
            return x

        def encode_query():
            p = [(
             encode_data(k), encode_data(v)) for k, v in self._pairs()]
            return urlencode(p)

        if method == 'GET':
            if self.enctype != 'application/x-www-form-urlencoded':
                raise ValueError("unknown GET form encoding type '%s'" % self.enctype)
            parts = rest + (encode_query(), None)
            uri = self._urlunparse(parts)
            return (
             uri, None, [])
        if method == 'POST':
            parts = rest + (query, None)
            uri = self._urlunparse(parts)
            if self.enctype == 'application/x-www-form-urlencoded':
                return (uri, encode_query(),
                 [
                  (
                   'Content-Type', self.enctype)])
            if self.enctype == 'multipart/form-data':
                data = StringIO()
                http_hdrs = []
                mw = MimeWriter(data, http_hdrs)
                mw.startmultipartbody('form-data',
                  add_to_http_hdrs=True, prefix=0)
                for ii, k, v, control_index in self._pairs_and_controls():
                    self.controls[control_index]._write_mime_data(mw, encode_data(k), encode_data(v))
                else:
                    mw.lastpart()
                    return (
                     uri, data.getvalue(), http_hdrs)

            raise ValueError("unknown POST form encoding type '%s'" % self.enctype)
        else:
            raise ValueError("Unknown method '%s'" % method)

    def _switch_click--- This code section failed: ---

 L.2556         0  LOAD_FAST                'return_type'
                2  LOAD_STR                 'pairs'
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE    16  'to 16'

 L.2557         8  LOAD_FAST                'self'
               10  LOAD_METHOD              _pairs
               12  CALL_METHOD_0         0  ''
               14  RETURN_VALUE     
             16_0  COME_FROM             6  '6'

 L.2558        16  LOAD_FAST                'return_type'
               18  LOAD_STR                 'request_data'
               20  COMPARE_OP               ==
               22  POP_JUMP_IF_FALSE    32  'to 32'

 L.2559        24  LOAD_FAST                'self'
               26  LOAD_METHOD              _request_data
               28  CALL_METHOD_0         0  ''
               30  RETURN_VALUE     
             32_0  COME_FROM            22  '22'

 L.2561        32  LOAD_FAST                'self'
               34  LOAD_METHOD              _request_data
               36  CALL_METHOD_0         0  ''
               38  STORE_FAST               'req_data'

 L.2562        40  LOAD_FAST                'request_class'
               42  LOAD_FAST                'req_data'
               44  LOAD_CONST               0
               46  BINARY_SUBSCR    
               48  LOAD_FAST                'req_data'
               50  LOAD_CONST               1
               52  BINARY_SUBSCR    
               54  CALL_FUNCTION_2       2  ''
               56  STORE_FAST               'req'

 L.2563        58  LOAD_FAST                'req_data'
               60  LOAD_CONST               2
               62  BINARY_SUBSCR    
               64  GET_ITER         
             66_0  COME_FROM           134  '134'
               66  FOR_ITER            136  'to 136'
               68  UNPACK_SEQUENCE_2     2 
               70  STORE_FAST               'key'
               72  STORE_FAST               'val'

 L.2564        74  LOAD_FAST                'req'
               76  LOAD_ATTR                add_header
               78  STORE_FAST               'add_hdr'

 L.2565        80  LOAD_FAST                'key'
               82  LOAD_METHOD              lower
               84  CALL_METHOD_0         0  ''
               86  LOAD_STR                 'content-type'
               88  COMPARE_OP               ==
               90  POP_JUMP_IF_FALSE   124  'to 124'

 L.2566        92  SETUP_FINALLY       104  'to 104'

 L.2567        94  LOAD_FAST                'req'
               96  LOAD_ATTR                add_unredirected_header
               98  STORE_FAST               'add_hdr'
              100  POP_BLOCK        
              102  JUMP_FORWARD        124  'to 124'
            104_0  COME_FROM_FINALLY    92  '92'

 L.2568       104  DUP_TOP          
              106  LOAD_GLOBAL              AttributeError
              108  COMPARE_OP               exception-match
              110  POP_JUMP_IF_FALSE   122  'to 122'
              112  POP_TOP          
              114  POP_TOP          
              116  POP_TOP          

 L.2570       118  POP_EXCEPT       
              120  BREAK_LOOP          124  'to 124'
            122_0  COME_FROM           110  '110'
              122  END_FINALLY      
            124_0  COME_FROM           120  '120'
            124_1  COME_FROM           102  '102'
            124_2  COME_FROM            90  '90'

 L.2571       124  LOAD_FAST                'add_hdr'
              126  LOAD_FAST                'key'
              128  LOAD_FAST                'val'
              130  CALL_FUNCTION_2       2  ''
              132  POP_TOP          
              134  JUMP_BACK            66  'to 66'
            136_0  COME_FROM            66  '66'

 L.2572       136  LOAD_FAST                'req'
              138  RETURN_VALUE     

Parse error at or near `END_FINALLY' instruction at offset 122